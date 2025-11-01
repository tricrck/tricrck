import json
import os
import re
from datetime import datetime

def generate_news_section():
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    output_file = f'{data_dir}/blog_posts.json'
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    top_stories = data['chaos_ranked'][:2]

    news_section = "## 🚨 Tech Stories\n\n"

    for story in top_stories:
        pub_date = datetime.fromisoformat(story['published'].replace('Z', '+00:00'))
        formatted_date = pub_date.strftime("%B %d, %Y")

        news_section += f"### {story['title']}\n"
        news_section += f"- **Published**: {formatted_date}\n"

        summary_text = story['summary']
        if '<a href=' in summary_text:
            summary_text = summary_text.split('>', 2)[-1] if '>' in summary_text else summary_text

        news_section += f"- **Summary**: {summary_text[:150]}...\n"

        if story['keywords']['chaos']:
            news_section += f"- **Keywords**: {', '.join(story['keywords']['chaos'])}\n"

        news_section += f"- [Read more]({story['link']})\n\n"

    news_section += "---\n\n"
    return news_section


def update_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except UnicodeDecodeError:
        with open('README.md', 'r', encoding='latin-1') as f:
            readme_content = f.read()

    news_section = generate_news_section()

    readme_content = re.sub(
        r'## 🚨 Tech Stories.*?(?=### 🔮 Elemental Affinities|$)',
        '',
        readme_content,
        flags=re.DOTALL
    )
    
    # Clean up any orphaned "---" separators that might be left
    readme_content = re.sub(r'\n---\n---\n', '\n---\n', readme_content)
    
    # Clean up multiple consecutive newlines (more than 2)
    readme_content = re.sub(r'\n{3,}', '\n\n', readme_content)
    # Ensure there's a newline before and after the news section
    parts = readme_content.split('---', 2)
    
    if len(parts) >= 3:
        # Reassemble: header section + news section + rest
        updated_content = parts[0] + '---' + parts[1] + '---\n\n' + news_section + parts[2]
    else:
        # Fallback: insert before Elemental Affinities
        if "### 🔮 Elemental Affinities" in readme_content:
            updated_content = readme_content.replace(
                "### 🔮 Elemental Affinities",
                news_section + "### 🔮 Elemental Affinities",
                1
            )
        else:
            updated_content = readme_content.rstrip() + "\n\n" + news_section

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("✅ README updated with latest news (replaced old section).")
    

if __name__ == "__main__":
    update_readme()