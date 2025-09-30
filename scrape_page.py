#!/usr/bin/env python3
"""
Script to scrape a specific URL and apply intelligent filtering.
Usage: python scrape_page.py <url>
"""

import sys
import os
from improved_scraper import ScrapestackScraper
from intelligent_filter import GroqLLMFilter, load_config_from_file

def scrape_specific_url(url: str):
    """Scrape articles from a specific URL and apply intelligent filtering."""
    
    print(f"🔍 Scraping articles from: {url}")
    print("=" * 80)
    
    # Initialize scraper
    try:
        scraper = ScrapestackScraper()
        print("✅ Scraper initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing scraper: {e}")
        return
    
    # Scrape articles
    try:
        # First scrape the HTML content
        html_content = scraper.scrape_url(url)
        if not html_content:
            print("❌ Failed to scrape HTML content")
            return
        
        # Then extract articles from the HTML
        articles = scraper.extract_articles(html_content)
        print(f"📰 Found {len(articles)} articles")
        
        if not articles:
            print("❌ No articles found")
            return
            
    except Exception as e:
        print(f"❌ Error scraping articles: {e}")
        return
    
    # Display basic articles first
    print("\n📋 All Articles Found:")
    print("-" * 50)
    for i, article in enumerate(articles, 1):
        print(f"{i:2d}. {article['title']}")
        print(f"    🔗 {article['url']}")
        print()
    
    # Check if Groq API key is available for intelligent filtering
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️  GROQ_API_KEY not set - skipping intelligent filtering")
        print("💡 To enable AI filtering, set: export GROQ_API_KEY='your_key'")
        return
    
    # Apply intelligent filtering
    print("\n🤖 Applying AI-Powered Intelligent Filtering...")
    print("=" * 80)
    
    try:
        # Load configuration
        config = load_config_from_file()
        print(f"📋 Using configuration:")
        print(f"   Primary keyword: '{config.primary_keyword}'")
        print(f"   Additional keywords: {len(config.additional_keywords)} terms")
        print(f"   Relevance threshold: {config.relevance_threshold}")
        print()
        
        # Initialize filter
        llm_filter = GroqLLMFilter()
        
        # Filter articles
        filtered_articles = llm_filter.filter_articles(articles, config)
        
        if not filtered_articles:
            print("❌ No articles met the relevance criteria")
            print(f"💡 Try lowering the relevance threshold (currently {config.relevance_threshold})")
            return
        
        print(f"🎯 Found {len(filtered_articles)} highly relevant articles:")
        print()
        
        # Display filtered results
        for i, article in enumerate(filtered_articles, 1):
            print("=" * 80)
            print(f"{i}. 📰 {article['title']}")
            print(f"   🔗 {article['url']}")
            print(f"   📊 Relevance Score: {article['relevance_score']:.2f}")
            print(f"   🎯 Matched Keywords: {', '.join(article['matched_keywords'])}")
            print(f"   💭 Reasoning: {article['reasoning']}")
            print("-" * 80)
            
    except Exception as e:
        print(f"❌ Error during intelligent filtering: {e}")

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python scrape_page.py <url>")
        print("Example: python scrape_page.py 'https://www.newscientist.com/article-topic/quantum-science/page/10/'")
        sys.exit(1)
    
    url = sys.argv[1]
    scrape_specific_url(url)

if __name__ == "__main__":
    main()