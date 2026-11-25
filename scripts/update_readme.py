import html
import json
import os
import re
import sys
from datetime import datetime

NEWS_HEADING = "## 🚨 Tech Stories"
NEXT_HEADING = "### 🔮 Elemental Affinities"


def clean_summary(text):
    """Strip HTML tags/entities and collapse whitespace."""
    text = re.sub(r'<[^>]+>', ' ', text or '')
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip().rstrip('.').rstrip()


def format_date(published):
    if not published:
        return None
    try:
        return datetime.fromisoformat(published.replace('Z', '+00:00')).strftime("%B %d, %Y")
    except ValueError:
        return None


def generate_news_section():
    data_file = os.path.join('data', 'blog_posts.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    top_stories = data.get('chaos_ranked', [])[:2]
    if not top_stories:
        return None

    news_section = f"{NEWS_HEADING}\n\n"

    for story in top_stories:
        news_section += f"### {story.get('title', 'Untitled')}\n"

        formatted_date = format_date(story.get('published'))
        if formatted_date:
            news_section += f"- **Published**: {formatted_date}\n"

        summary_text = clean_summary(story.get('summary', ''))
        if summary_text:
            if len(summary_text) > 150:
                summary_text = summary_text[:150].rstrip() + '...'
            news_section += f"- **Summary**: {summary_text}\n"

        keywords = story.get('keywords', {}).get('chaos') or []
        if keywords:
            news_section += f"- **Keywords**: {', '.join(sorted(set(keywords)))}\n"

        news_section += f"- [Read more]({story.get('link', '#')})\n\n"

    news_section += "---\n\n"
    return news_section


def update_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()

    news_section = generate_news_section()
    if news_section is None:
        print("⚠️ No stories available - README left unchanged.")
        return 0

    start = readme_content.find(NEWS_HEADING)
    end = readme_content.find(NEXT_HEADING)

    if start != -1 and end != -1 and start < end:
        # Replace only the existing news block
        updated = readme_content[:start] + news_section + readme_content[end:]
    elif start != -1:
        # News heading exists but the following heading is missing: refuse to
        # guess where the block ends rather than risk deleting content.
        print(f"❌ Found '{NEWS_HEADING}' but not '{NEXT_HEADING}' after it - README left unchanged.")
        return 1
    elif end != -1:
        updated = readme_content[:end] + news_section + readme_content[end:]
    else:
        updated = readme_content.rstrip() + "\n\n" + news_section

    # Tidy: collapse repeated horizontal rules and excess blank lines
    updated = re.sub(r'(?:^---\s*\n\s*){2,}', '---\n\n', updated, flags=re.MULTILINE)
    updated = re.sub(r'\n{3,}', '\n\n', updated)

    with open('README.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write(updated)

    print("✅ README updated with latest news.")
    return 0


if __name__ == "__main__":
    sys.exit(update_readme())
