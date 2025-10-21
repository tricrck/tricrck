#!/usr/bin/env python3
"""
📜 RSS Feed Dark Scroll Parser
Extracts ancient knowledge from RSS feeds
"""

import os
import json
import feedparser
from datetime import datetime
from dateutil import parser as date_parser

# Add the scoring functions and dictionaries here (before the class)
CHAOS_KEYWORDS = {
    'brick': 10, 'bricks': 10, 'bricked': 10, 'failure': 8, 'crash': 8, 
    'broken': 7, 'disrupt': 6, 'disruption': 6, 'chaos': 9, 'collapse': 8,
    'meltdown': 9, 'failure': 7, 'error': 6, 'bug': 5, 'glitch': 5,
    'down': 4, 'outage': 7, 'crisis': 8, 'emergency': 6, 'riot': 9,
    'protest': 7, 'revolt': 8, 'breakdown': 7, 'malfunction': 6
}

ANARCHY_KEYWORDS = {
    'anarchy': 10, 'anarchist': 9, 'rebel': 8, 'rebellion': 9, 'revolution': 9,
    'anti-establishment': 10, 'anti-government': 9, 'subversive': 8,
    'radical': 7, 'insurrection': 10, 'mutiny': 9, 'overthrow': 9,
    'dissident': 7, 'defiance': 7, 'resistance': 6, 'underground': 6,
    'counterculture': 7, 'autonomous': 6, 'stateless': 8, 'unregulated': 7
}

SOURCE_SCORES = {
    'arstechnica.com': {'chaos': 6, 'anarchy': 4},
    'schneier.com': {'chaos': 5, 'anarchy': 5},
    'techcrunch.com': {'chaos': 3, 'anarchy': 2},
    'steveblank.com': {'chaos': 2, 'anarchy': 3},
    'chezsoi.org': {'chaos': 1, 'anarchy': 1},
    'sqliteonline.com': {'chaos': 1, 'anarchy': 1},
    'ycombinator.com': {'chaos': 4, 'anarchy': 3}
}

def extract_domain(url):
    """Extract domain from URL"""
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    return domain.replace('www.', '')

def calculate_theme_score(text, keyword_dict, source_domain, theme_type):
    """Calculate score for a specific theme"""
    if not text:
        return 0, []
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Keyword frequency with weights
    keyword_score = 0
    found_keywords = []
    
    for word in words:
        if word in keyword_dict:
            keyword_score += keyword_dict[word]
            found_keywords.append(word)
    
    # Normalize by text length (prevent bias for long texts)
    if len(words) > 0:
        keyword_score = (keyword_score / len(words)) * 100
    
    # Source authority
    source_score = SOURCE_SCORES.get(source_domain, {'chaos': 1, 'anarchy': 1})[theme_type] * 10
    
    # Final score (70% keywords, 30% source authority)
    final_score = (keyword_score * 0.7) + (source_score * 0.3)
    
    return min(final_score, 100), found_keywords

def analyze_articles(articles_data):
    """Analyze all articles and return ranked lists for both themes"""
    scored_articles = []
    
    for article in articles_data:
        # Combine title and summary for analysis
        content = f"{article.get('title', '')} {article.get('summary', '')}"
        domain = extract_domain(article['link'])
        
        # Calculate chaos score
        chaos_score, chaos_keywords = calculate_theme_score(
            content, CHAOS_KEYWORDS, domain, 'chaos'
        )
        
        # Calculate anarchy score  
        anarchy_score, anarchy_keywords = calculate_theme_score(
            content, ANARCHY_KEYWORDS, domain, 'anarchy'
        )
        
        # Overall metal/gloom score (average of both)
        overall_score = (chaos_score + anarchy_score) / 2
        
        scored_article = {
            'title': article.get('title', ''),
            'link': article['link'],
            'summary': article.get('summary', ''),
            'published': article.get('published', ''),
            'domain': domain,
            'scores': {
                'chaos': round(chaos_score, 1),
                'anarchy': round(anarchy_score, 1),
                'overall': round(overall_score, 1)
            },
            'keywords': {
                'chaos': chaos_keywords,
                'anarchy': anarchy_keywords
            }
        }
        
        scored_articles.append(scored_article)
    
    # Sort by different criteria
    chaos_ranked = sorted(scored_articles, key=lambda x: x['scores']['chaos'], reverse=True)
    anarchy_ranked = sorted(scored_articles, key=lambda x: x['scores']['anarchy'], reverse=True)
    overall_ranked = sorted(scored_articles, key=lambda x: x['scores']['overall'], reverse=True)
    
    return {
        'chaos_ranked': chaos_ranked,
        'anarchy_ranked': anarchy_ranked, 
        'overall_ranked': overall_ranked,
        'all_articles': scored_articles
    }

def print_analysis_results(analysis):
    """Print formatted results in two blocks"""
    
    print("\n" + "🔥" * 80)
    print("CHAOS RANKING - System failures, breakdowns, malfunctions")
    print("🔥" * 80)
    for i, article in enumerate(analysis['chaos_ranked'][:5], 1):
        print(f"{i}. {article['title'][:60]}...")
        print(f"   Chaos Score: {article['scores']['chaos']} | Anarchy Score: {article['scores']['anarchy']}")
        if article['keywords']['chaos']:
            print(f"   Keywords: {', '.join(article['keywords']['chaos'])}")
        print(f"   Source: {article['domain']}")
        print()
    
    print("⚡" * 80)
    print("ANARCHY RANKING - Rebellion, anti-establishment, revolution")
    print("⚡" * 80)
    for i, article in enumerate(analysis['anarchy_ranked'][:5], 1):
        print(f"{i}. {article['title'][:60]}...")
        print(f"   Anarchy Score: {article['scores']['anarchy']} | Chaos Score: {article['scores']['chaos']}")
        if article['keywords']['anarchy']:
            print(f"   Keywords: {', '.join(article['keywords']['anarchy'])}")
        print(f"   Source: {article['domain']}")
        print()

class FeedNecromancer:
    def __init__(self):
        
        
        # Add your blog/medium RSS feeds here
        self.feeds = [
            "https://techcrunch.com/feed/",  # Your dev.to feed
            "https://news.ycombinator.com/rss",  # Your Medium feed
            # Add more feeds as needed
        ]
    
    def parse_feed(self, feed_url):
        """Parse a single RSS feed"""
        try:
            print(f"📖 Reading scroll: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            articles = []
            for entry in feed.entries[:5]:  # Get last 5 articles
                try:
                    # Parse publication date
                    pub_date = None
                    if hasattr(entry, 'published'):
                        pub_date = date_parser.parse(entry.published)
                    elif hasattr(entry, 'updated'):
                        pub_date = date_parser.parse(entry.updated)
                    
                    article = {
                        "title": entry.get('title', 'Untitled Scroll'),
                        "link": entry.get('link', '#'),
                        "summary": entry.get('summary', '')[:200] + '...',
                        "published": pub_date.isoformat() if pub_date else None,
                        "tags": [tag.term for tag in entry.get('tags', [])]
                    }
                    articles.append(article)
                except Exception as e:
                    print(f"  ⚠️ Error parsing entry: {e}")
            
            return articles
        except Exception as e:
            print(f"  💀 Failed to parse {feed_url}: {e}")
            return []
    
    def extract_all_feeds(self):
        """Extract all RSS feeds"""
        print("🔮 Summoning RSS dark scrolls...\n")
        
        all_articles = []
        feed_stats = {
            "total_feeds": len(self.feeds),
            "successful": 0,
            "failed": 0,
            "total_articles": 0
        }
        
        for feed_url in self.feeds:
            articles = self.parse_feed(feed_url)
            if articles:
                all_articles.extend(articles)
                feed_stats["successful"] += 1
                feed_stats["total_articles"] += len(articles)
            else:
                feed_stats["failed"] += 1
        
        # Sort by date (most recent first)
        all_articles.sort(
            key=lambda x: x['published'] if x['published'] else '', 
            reverse=True
        )
        
        return all_articles[:10], feed_stats  # Return top 10 most recent
    
    def save_articles(self):
        """Save parsed articles to JSON"""
        articles, stats = self.extract_all_feeds()
        
        data = {
            "last_updated": datetime.now().isoformat(),
            "stats": stats,
            "articles": articles
        }
        
        return data

def main():
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    print("📜" * 30)
    print("   RSS NECROMANCY RITUAL")
    print("📜" * 30 + "\n")
    
    try:
        necromancer = FeedNecromancer()
        data = necromancer.save_articles()
        
        # 🔥 ADD THIS PART - Analyze the articles for chaos/anarchy
        print("\n" + "🧨" * 40)
        print("   ANALYZING FOR CHAOS & ANARCHY")
        print("🧨" * 40)
        
        analysis = analyze_articles(data['articles'])
        print_analysis_results(analysis)
        
        # Print summary statistics
        print("📊" * 40)
        print("SUMMARY STATISTICS")
        print("📊" * 40)
        print(f"Total articles analyzed: {len(analysis['all_articles'])}")
        
        avg_chaos = sum(a['scores']['chaos'] for a in analysis['all_articles']) / len(analysis['all_articles'])
        avg_anarchy = sum(a['scores']['anarchy'] for a in analysis['all_articles']) / len(analysis['all_articles'])
        
        print(f"Average Chaos Score: {avg_chaos:.1f}")
        print(f"Average Anarchy Score: {avg_anarchy:.1f}")
        
        # Find highest scoring articles
        top_chaos = analysis['chaos_ranked'][0]
        top_anarchy = analysis['anarchy_ranked'][0]
        
        output_file = f'{data_dir}/blog_posts.json'
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print("\n" + "⚰️" * 30)
        print("   SCROLLS ARCHIVED & ANALYZED")
        print("⚰️" * 30)
        
        return 0
    except Exception as e:
        print(f"\n💀 RITUAL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import re  # Make sure re is imported for the regex functions
    import sys
    sys.exit(main())