#!/usr/bin/env python3
"""
🦇 GitHub Data Necromancer
Extracts soul data from GitHub's dark realm
"""

import os
import json
import requests
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from github import Github
import sys

class GitHubNecromancer:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.username = os.getenv('GITHUB_USERNAME', 'tricrck')
        
        if not self.token:
            print("⚠️ No GITHUB_TOKEN found, using limited public API")
            self.gh = Github()
        else:
            self.gh = Github(self.token)
        
        self.user = self.gh.get_user(self.username)
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        
    def extract_language_souls(self):
        """Extract language usage from all repositories"""
        print("🔮 Extracting language souls...")
        lang_stats = Counter()
        lang_bytes = Counter()
        
        repos = list(self.user.get_repos())
        for repo in repos:
            if not repo.fork:  # Skip forked repos
                try:
                    languages = repo.get_languages()
                    for lang, bytes_code in languages.items():
                        lang_stats[lang] += 1
                        lang_bytes[lang] += bytes_code
                except Exception as e:
                    print(f"  ⚠️ Skipped {repo.name}: {e}")
        
        return dict(lang_stats), dict(lang_bytes)
    
    def calculate_contribution_streak(self):
        """Calculate the darkest contribution streak"""
        print("⚔️ Calculating contribution streaks...")
        
        # Get contribution data from events
        events = list(self.user.get_events())
        dates = set()
        
        for event in events[:300]:  # Last 300 events
            dates.add(event.created_at.date())
        
        if not dates:
            return {"current": 0, "longest": 0, "total_days": 0}
        
        sorted_dates = sorted(dates, reverse=True)
        
        # Calculate current streak
        current_streak = 0
        today = datetime.now().date()
        
        for i, date in enumerate(sorted_dates):
            expected_date = today - timedelta(days=i)
            if date == expected_date or (i == 0 and (today - date).days <= 1):
                current_streak += 1
            else:
                break
        
        # Calculate longest streak
        longest_streak = 1
        temp_streak = 1
        
        for i in range(len(sorted_dates) - 1):
            if (sorted_dates[i] - sorted_dates[i + 1]).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
        
        return {
            "current": current_streak,
            "longest": longest_streak,
            "total_days": len(dates)
        }
    
    def extract_commit_patterns(self):
        """Analyze commit patterns and dark coding hours"""
        print("🌙 Analyzing nocturnal coding patterns...")
        
        hour_distribution = Counter()
        day_distribution = Counter()
        
        repos = list(self.user.get_repos())[:20]  # Top 20 repos
        
        for repo in repos:
            try:
                if not repo.fork:
                    commits = list(repo.get_commits(author=self.username))[:100]
                    for commit in commits:
                        hour = commit.commit.author.date.hour
                        day = commit.commit.author.date.strftime('%A')
                        hour_distribution[hour] += 1
                        day_distribution[day] += 1
            except Exception as e:
                print(f"  ⚠️ Error processing {repo.name}: {e}")
        
        return {
            "hour_distribution": dict(hour_distribution),
            "day_distribution": dict(day_distribution),
            "darkest_hour": hour_distribution.most_common(1)[0][0] if hour_distribution else 0
        }
    
    def get_repository_stats(self):
        """Gather repository statistics"""
        print("📊 Summoning repository statistics...")
        
        repos = list(self.user.get_repos())
        
        stats = {
            "total": len(repos),
            "own": len([r for r in repos if not r.fork]),
            "forked": len([r for r in repos if r.fork]),
            "total_stars": sum(r.stargazers_count for r in repos),
            "total_forks": sum(r.forks_count for r in repos),
            "languages": {},
            "top_repos": []
        }
        
        # Get top repos by stars
        own_repos = [r for r in repos if not r.fork]
        top_repos = sorted(own_repos, key=lambda x: x.stargazers_count, reverse=True)[:5]
        
        for repo in top_repos:
            stats["top_repos"].append({
                "name": repo.name,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "url": repo.html_url,
                "description": repo.description or "Ancient code without description"
            })
        
        return stats
    
    def save_dark_data(self):
        """Save all extracted data to JSON grimoires"""
        print("\n💾 Writing to dark grimoires...")
        
        # Language data
        lang_count, lang_bytes = self.extract_language_souls()
        
        # Contribution streaks
        streaks = self.calculate_contribution_streak()
        
        # Commit patterns
        patterns = self.extract_commit_patterns()
        
        # Repository stats
        repo_stats = self.get_repository_stats()
        
        # Compile master data
        master_data = {
            "last_updated": datetime.now().isoformat(),
            "username": self.username,
            "profile_url": f"https://github.com/{self.username}",
            "languages": {
                "by_repos": lang_count,
                "by_bytes": lang_bytes
            },
            "streaks": streaks,
            "patterns": patterns,
            "repositories": repo_stats,
            "total_contributions": self.user.public_repos + self.user.public_gists,
            "followers": self.user.followers,
            "following": self.user.following
        }
        
        # Save main data
        with open(f'{self.data_dir}/github_data.json', 'w') as f:
            json.dump(master_data, f, indent=2)
        
        print(f"✅ Data saved to {self.data_dir}/github_data.json")
        print(f"   📈 Languages tracked: {len(lang_count)}")
        print(f"   🔥 Current streak: {streaks['current']} days")
        print(f"   ⭐ Total stars: {repo_stats['total_stars']}")
        
        return master_data

def main():
    print("🦇" * 30)
    print("   GITHUB NECROMANCY RITUAL INITIATED")
    print("🦇" * 30 + "\n")
    
    try:
        necromancer = GitHubNecromancer()
        data = necromancer.save_dark_data()
        
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