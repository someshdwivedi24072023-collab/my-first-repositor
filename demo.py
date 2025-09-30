#!/usr/bin/env python3
"""
Demo script showing the evolution from basic scraping to AI-powered filtering.
This script demonstrates all three approaches:
1. Original scraper (basic functionality)
2. Improved scraper (enhanced security and reliability)
3. Intelligent filter (AI-powered relevance filtering)
"""

import os
import sys
from typing import List, Dict, Any

def demo_original_scraper():
    """Demo the original scraper functionality."""
    print("🔧 DEMO 1: Original Scraper")
    print("=" * 50)
    print("Features:")
    print("- Basic web scraping functionality")
    print("- Hardcoded API key (security risk)")
    print("- Disabled SSL verification (security risk)")
    print("- No error handling")
    print("- Simple output format")
    print("\n⚠️  Not recommended for production use due to security issues")
    print("📁 File: scrapstack.py")
    print()

def demo_improved_scraper():
    """Demo the improved scraper functionality."""
    print("🚀 DEMO 2: Improved Scraper")
    print("=" * 50)
    print("Features:")
    print("✅ Secure API key management (environment variables)")
    print("✅ SSL certificate verification enabled")
    print("✅ Comprehensive error handling")
    print("✅ Request timeouts and retry logic")
    print("✅ Professional logging")
    print("✅ Class-based architecture")
    print("✅ Type hints and documentation")
    
    try:
        from improved_scraper import ScrapestackScraper
        
        if not os.getenv('SCRAPESTACK_API_KEY'):
            print("\n⚠️  SCRAPESTACK_API_KEY not set - demo will show structure only")
            scraper = None
        else:
            scraper = ScrapestackScraper()
            print("\n✅ Scraper initialized successfully")
        
        print("📁 File: improved_scraper.py")
        print("🔧 Usage: python improved_scraper.py")
        
    except Exception as e:
        print(f"\n❌ Error initializing improved scraper: {e}")
    
    print()

def demo_intelligent_filter():
    """Demo the intelligent filtering functionality."""
    print("🤖 DEMO 3: AI-Powered Intelligent Filter")
    print("=" * 50)
    print("Features:")
    print("🧠 Groq LLM integration for intelligent content analysis")
    print("🎯 Keyword-based relevance scoring (0.0-1.0)")
    print("⚙️  Configurable filtering parameters")
    print("📊 Detailed reasoning for each filtered article")
    print("🔄 Batch processing with rate limiting")
    print("📝 Comprehensive logging and error handling")
    print("🧪 Built-in testing suite")
    
    try:
        from intelligent_filter import load_config_from_file, FilterConfig
        
        # Load and display configuration
        config = load_config_from_file()
        print(f"\n📋 Current Configuration:")
        print(f"   Primary keyword: '{config.primary_keyword}'")
        print(f"   Additional keywords: {len(config.additional_keywords)} terms")
        print(f"   Relevance threshold: {config.relevance_threshold}")
        print(f"   Max articles to process: {config.max_articles_to_process}")
        
        # Check API key availability
        if not os.getenv('GROQ_API_KEY'):
            print("\n⚠️  GROQ_API_KEY not set - demo will show structure only")
        else:
            print("\n✅ Groq API key configured")
        
        if not os.getenv('SCRAPESTACK_API_KEY'):
            print("⚠️  SCRAPESTACK_API_KEY not set - scraping functionality limited")
        else:
            print("✅ ScrapeStack API key configured")
        
        print("\n📁 Files:")
        print("   - intelligent_filter.py (main functionality)")
        print("   - filter_config.json (configuration)")
        print("   - test_filter.py (testing suite)")
        print("\n🔧 Usage:")
        print("   - python intelligent_filter.py (run full pipeline)")
        print("   - python test_filter.py (run tests)")
        
    except Exception as e:
        print(f"\n❌ Error loading intelligent filter: {e}")
    
    print()

def demo_configuration_customization():
    """Demo how to customize the filtering configuration."""
    print("⚙️  DEMO 4: Configuration Customization")
    print("=" * 50)
    print("The intelligent filter uses a flexible JSON configuration system.")
    print("You can easily customize filtering by editing filter_config.json:")
    print()
    
    try:
        import json
        with open("filter_config.json", 'r') as f:
            config = json.load(f)
        
        print("📄 Current Configuration:")
        print(json.dumps(config, indent=2))
        
        print("\n💡 Customization Examples:")
        print("1. Change primary keyword: 'quantum' → 'artificial intelligence'")
        print("2. Add new keywords: ['machine learning', 'neural networks']")
        print("3. Adjust threshold: 0.6 → 0.8 (more strict filtering)")
        print("4. Increase processing limit: 20 → 50 articles")
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
    
    print()

def demo_workflow_comparison():
    """Demo showing the workflow evolution."""
    print("📈 DEMO 5: Workflow Evolution")
    print("=" * 50)
    
    workflows = [
        {
            "name": "Original Workflow",
            "steps": [
                "1. Hardcode API key in script",
                "2. Make HTTP request (no SSL verification)",
                "3. Parse HTML content",
                "4. Extract all articles",
                "5. Print results"
            ],
            "issues": ["Security risks", "No error handling", "All articles returned"]
        },
        {
            "name": "Improved Workflow", 
            "steps": [
                "1. Load API key from environment",
                "2. Make secure HTTP request with retries",
                "3. Parse HTML with error handling",
                "4. Extract articles with validation",
                "5. Log results professionally"
            ],
            "benefits": ["Secure", "Reliable", "Professional logging"]
        },
        {
            "name": "Intelligent Workflow",
            "steps": [
                "1. Load configuration from JSON",
                "2. Scrape articles securely",
                "3. Send to Groq LLM for analysis",
                "4. Filter by relevance score",
                "5. Return ranked, relevant articles"
            ],
            "benefits": ["AI-powered", "Configurable", "Relevance scoring", "Detailed reasoning"]
        }
    ]
    
    for i, workflow in enumerate(workflows, 1):
        print(f"\n{workflow['name']}:")
        for step in workflow['steps']:
            print(f"   {step}")
        
        if 'issues' in workflow:
            print(f"   ❌ Issues: {', '.join(workflow['issues'])}")
        if 'benefits' in workflow:
            print(f"   ✅ Benefits: {', '.join(workflow['benefits'])}")
    
    print()

def main():
    """Run all demos."""
    print("🎬 Web Scraping Evolution Demo")
    print("=" * 60)
    print("This demo showcases the evolution from basic web scraping")
    print("to AI-powered intelligent article filtering.")
    print("=" * 60)
    print()
    
    demos = [
        demo_original_scraper,
        demo_improved_scraper,
        demo_intelligent_filter,
        demo_configuration_customization,
        demo_workflow_comparison
    ]
    
    for demo in demos:
        demo()
        input("Press Enter to continue to next demo...")
        print()
    
    print("🎉 Demo Complete!")
    print("=" * 60)
    print("Next Steps:")
    print("1. Set up your API keys:")
    print("   export SCRAPESTACK_API_KEY='your_key_here'")
    print("   export GROQ_API_KEY='your_key_here'")
    print()
    print("2. Run the intelligent filter:")
    print("   python intelligent_filter.py")
    print()
    print("3. Customize the configuration:")
    print("   Edit filter_config.json to match your interests")
    print()
    print("4. Run tests to verify everything works:")
    print("   python test_filter.py")

if __name__ == "__main__":
    main()