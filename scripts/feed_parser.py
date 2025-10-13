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

class FeedNecromancer:
    def __init__(self):
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        
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
        
        output_file = f'{self.data_dir}/blog_posts.json'
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Saved {len(articles)} articles to {output_file}")
        print(f"   📊 Feeds processed: {stats['successful']}/{stats['total_feeds']}")
        
        return data

def main():
    print("📜" * 30)
    print("   RSS NECROMANCY RITUAL")
    print("📜" * 30 + "\n")
    
    try:
        necromancer = FeedNecromancer()
        data = necromancer.save_articles()
        
        print("\n" + "⚰️" * 30)
        print("   SCROLLS ARCHIVED")
        print("⚰️" * 30)
        
        return 0
    except Exception as e:
        print(f"\n💀 RITUAL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())