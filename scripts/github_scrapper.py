#!/usr/bin/env python3
"""
🦇 GitHub Data Necromancer
Extracts soul data from GitHub's dark realm

Optional environment variables:
  GITHUB_TOKEN               token for the REST + GraphQL APIs (needed for real
                             contribution counts and to avoid the 60 req/hr limit)
  GITHUB_USERNAME            account to profile (default: tricrck)
  LANG_BYTES_CAP_PER_REPO    max bytes one language can contribute from a single
                             repo, so vendored/generated files don't dominate
                             (default: 1000000; 0 disables the cap)
  EXCLUDED_LANGUAGES         comma-separated languages to ignore entirely
  EXCLUDED_REPOS             comma-separated repo names to ignore for language stats
  PROFILE_TIMEZONE           IANA zone for commit-hour stats, e.g. Africa/Nairobi
                             (default: UTC)
"""

import os
import json
import sys
from datetime import datetime, timedelta, timezone
from collections import Counter

import requests
from github import Github, Auth

GRAPHQL_URL = "https://api.github.com/graphql"

CONTRIBUTIONS_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def _env_list(name):
    return {v.strip() for v in os.getenv(name, '').split(',') if v.strip()}


def _profile_tz():
    name = os.getenv('PROFILE_TIMEZONE', 'UTC').strip() or 'UTC'
    if name.upper() == 'UTC':
        return timezone.utc, 'UTC'
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name), name
    except Exception as e:
        print(f"⚠️ Unknown PROFILE_TIMEZONE '{name}' ({e}); using UTC")
        return timezone.utc, 'UTC'


def compute_streaks(active_dates, today):
    """Current and longest run of consecutive active days.

    The current streak counts if the latest active day is today or yesterday
    (today may simply not have activity yet).
    """
    if not active_dates:
        return {"current": 0, "longest": 0, "total_days": 0}

    sorted_dates = sorted(set(active_dates), reverse=True)

    current = 0
    if (today - sorted_dates[0]).days <= 1:
        current = 1
        for i in range(len(sorted_dates) - 1):
            if (sorted_dates[i] - sorted_dates[i + 1]).days == 1:
                current += 1
            else:
                break

    longest = temp = 1
    for i in range(len(sorted_dates) - 1):
        if (sorted_dates[i] - sorted_dates[i + 1]).days == 1:
            temp += 1
            longest = max(longest, temp)
        else:
            temp = 1

    return {"current": current, "longest": longest, "total_days": len(sorted_dates)}


class GitHubNecromancer:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.username = os.getenv('GITHUB_USERNAME', 'tricrck')

        if not self.token:
            print("⚠️ No GITHUB_TOKEN found, using limited public API (60 requests/hour)")
            self.gh = Github()
        else:
            self.gh = Github(auth=Auth.Token(self.token))

        self.user = self.gh.get_user(self.username)
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)

        self.lang_cap = int(os.getenv('LANG_BYTES_CAP_PER_REPO', '1000000') or 0)
        self.excluded_langs = _env_list('EXCLUDED_LANGUAGES')
        self.excluded_repos = _env_list('EXCLUDED_REPOS')
        self.tz, self.tz_name = _profile_tz()

        self._repos = None

    # ------------------------------------------------------------------ repos
    @property
    def repos(self):
        """All public repos, fetched once and reused by every extractor."""
        if self._repos is None:
            self._repos = list(self.user.get_repos())
        return self._repos

    @property
    def own_repos(self):
        return [r for r in self.repos if not r.fork]

    # -------------------------------------------------------------- languages
    def extract_language_souls(self):
        """Extract language usage from non-fork repositories.

        Each language's bytes are capped per repo so a single repo full of
        generated/vendored files (e.g. exported HTML reports) can't dominate.
        """
        print("🔮 Extracting language souls...")
        lang_repos = Counter()
        lang_bytes = Counter()
        raw_bytes = Counter()
        capped = []

        for repo in self.own_repos:
            if repo.name in self.excluded_repos:
                continue
            try:
                languages = repo.get_languages()
            except Exception as e:
                print(f"  ⚠️ Skipped {repo.name}: {e}")
                continue

            for lang, size in languages.items():
                if not isinstance(size, int) or lang in self.excluded_langs:
                    continue
                counted = min(size, self.lang_cap) if self.lang_cap > 0 else size
                lang_repos[lang] += 1
                lang_bytes[lang] += counted
                raw_bytes[lang] += size
                if counted < size:
                    capped.append({"repo": repo.name, "language": lang,
                                   "raw_bytes": size, "counted_bytes": counted})

        for c in capped:
            print(f"  ✂️ Capped {c['language']} in {c['repo']}: "
                  f"{c['raw_bytes']:,} → {c['counted_bytes']:,} bytes")

        return dict(lang_repos), dict(lang_bytes), dict(raw_bytes), capped

    # ---------------------------------------------------------- contributions
    def fetch_contribution_calendar(self):
        """Real contribution calendar for the past year (GraphQL, needs a token)."""
        if not self.token:
            return None
        try:
            resp = requests.post(
                GRAPHQL_URL,
                json={"query": CONTRIBUTIONS_QUERY, "variables": {"login": self.username}},
                headers={"Authorization": f"bearer {self.token}"},
                timeout=30,
            )
            resp.raise_for_status()
            payload = resp.json()
            if payload.get('errors'):
                raise RuntimeError(payload['errors'][0].get('message'))
            calendar = payload['data']['user']['contributionsCollection']['contributionCalendar']
            days = {
                day['date']: day['contributionCount']
                for week in calendar['weeks'] for day in week['contributionDays']
            }
            return {"total": calendar['totalContributions'], "days": days}
        except Exception as e:
            print(f"  ⚠️ Contribution calendar unavailable ({e}); falling back to events")
            return None

    def calculate_contribution_streak(self, calendar=None):
        """Contribution streaks, from the calendar when available, else events."""
        print("⚔️ Calculating contribution streaks...")
        today_utc = datetime.now(timezone.utc).date()

        if calendar:
            active = [datetime.strptime(d, '%Y-%m-%d').date()
                      for d, count in calendar['days'].items() if count > 0]
            # Calendar days are in the account's own timezone; allow "today"
            # to be one day ahead of UTC.
            latest_day = max((datetime.strptime(d, '%Y-%m-%d').date()
                              for d in calendar['days']), default=today_utc)
            result = compute_streaks(active, max(today_utc, latest_day))
            result["source"] = "contribution_calendar"
            return result

        # Fallback: public events (last ~90 days, includes non-code events)
        events = self.user.get_events()
        dates = []
        for i, event in enumerate(events):
            if i >= 300:
                break
            dates.append(event.created_at.astimezone(timezone.utc).date())
        result = compute_streaks(dates, today_utc)
        result["source"] = "public_events"
        return result

    # --------------------------------------------------------------- patterns
    def extract_commit_patterns(self):
        """Analyze commit hours/days in PROFILE_TIMEZONE"""
        print(f"🌙 Analyzing nocturnal coding patterns ({self.tz_name})...")

        hour_distribution = Counter()
        day_distribution = Counter()

        # 20 most recently pushed non-fork repos
        recent = sorted(self.own_repos,
                        key=lambda r: r.pushed_at or datetime.min.replace(tzinfo=timezone.utc),
                        reverse=True)[:20]

        for repo in recent:
            try:
                commits = repo.get_commits(author=self.username)
                for i, commit in enumerate(commits):  # paginates lazily
                    if i >= 100:
                        break
                    when = commit.commit.author.date
                    if when.tzinfo is None:
                        when = when.replace(tzinfo=timezone.utc)
                    when = when.astimezone(self.tz)
                    hour_distribution[when.hour] += 1
                    day_distribution[when.strftime('%A')] += 1
            except Exception as e:
                print(f"  ⚠️ Error processing {repo.name}: {e}")

        return {
            "timezone": self.tz_name,
            "hour_distribution": dict(hour_distribution),
            "day_distribution": dict(day_distribution),
            "darkest_hour": hour_distribution.most_common(1)[0][0] if hour_distribution else 0
        }

    # ------------------------------------------------------------ repo stats
    def get_repository_stats(self):
        """Gather repository statistics (stars/forks count own repos only)"""
        print("📊 Summoning repository statistics...")

        own = self.own_repos
        stats = {
            "total": len(self.repos),
            "own": len(own),
            "forked": len(self.repos) - len(own),
            "total_stars": sum(r.stargazers_count for r in own),
            "total_forks": sum(r.forks_count for r in own),
            "top_repos": []
        }

        for repo in sorted(own, key=lambda x: x.stargazers_count, reverse=True)[:5]:
            stats["top_repos"].append({
                "name": repo.name,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "url": repo.html_url,
                "description": repo.description or "Ancient code without description"
            })

        return stats

    # ------------------------------------------------------------------- save
    def save_dark_data(self):
        """Save all extracted data to JSON grimoires"""
        print("\n💾 Writing to dark grimoires...")

        lang_count, lang_bytes, raw_bytes, capped = self.extract_language_souls()
        calendar = self.fetch_contribution_calendar()
        streaks = self.calculate_contribution_streak(calendar)
        patterns = self.extract_commit_patterns()
        repo_stats = self.get_repository_stats()

        master_data = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "username": self.username,
            "profile_url": f"https://github.com/{self.username}",
            "languages": {
                "by_repos": lang_count,
                "by_bytes": lang_bytes,
                "by_bytes_raw": raw_bytes,
                "cap_per_repo": self.lang_cap,
                "capped": capped,
            },
            "streaks": streaks,
            "patterns": patterns,
            "repositories": repo_stats,
            # Real contributions in the past year (None without a token)
            "total_contributions": calendar['total'] if calendar else None,
            "contributions_period": "past_year" if calendar else None,
            "public_repos": self.user.public_repos,
            "public_gists": self.user.public_gists,
            "followers": self.user.followers,
            "following": self.user.following
        }

        with open(f'{self.data_dir}/github_data.json', 'w', encoding='utf-8') as f:
            json.dump(master_data, f, indent=2)

        print(f"✅ Data saved to {self.data_dir}/github_data.json")
        print(f"   📈 Languages tracked: {len(lang_count)}")
        print(f"   🔥 Current streak: {streaks['current']} days ({streaks['source']})")
        print(f"   🧮 Contributions (past year): {master_data['total_contributions']}")
        print(f"   ⭐ Total stars: {repo_stats['total_stars']}")

        return master_data


def main():
    print("🦇" * 30)
    print("   GITHUB NECROMANCY RITUAL INITIATED")
    print("🦇" * 30 + "\n")

    try:
        necromancer = GitHubNecromancer()
        necromancer.save_dark_data()

        print("\n" + "🗡️" * 30)
        print("   RITUAL COMPLETE - SOULS CAPTURED")
        print("🗡️" * 30)

        return 0
    except Exception as e:
        print(f"\n💀 DARK RITUAL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
