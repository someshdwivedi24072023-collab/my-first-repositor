#!/bin/bash
# Setup script for environment variables
# Usage: source setup_env.sh

echo "🔧 Setting up environment variables for intelligent scraping..."

# ScrapeStack API Key
export SCRAPESTACK_API_KEY="c050c2e9b44f69e6e2ff7982ac1afff9"
echo "✅ SCRAPESTACK_API_KEY set"

# Groq API Key  
export GROQ_API_KEY="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"
echo "✅ GROQ_API_KEY set"

echo ""
echo "🎯 Environment ready! You can now run:"
echo "   python improved_scraper.py"
echo "   python intelligent_filter.py"
echo "   python scrape_page.py '<url>'"
echo "   python test_filter.py"
echo "   python demo_auto.py"
echo ""
echo "💡 To verify setup:"
echo "   echo \$SCRAPESTACK_API_KEY"
echo "   echo \$GROQ_API_KEY"