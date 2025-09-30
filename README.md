# Web Scraper for New Scientist Articles

This repository contains web scraping tools to extract article information from New Scientist's quantum science section using the ScrapeStack API.

## Files

- `scrapstack.py` - Original scraper implementation
- `improved_scraper.py` - Enhanced version with better security and error handling
- `intelligent_filter.py` - AI-powered article filtering using Groq LLM
- `filter_config.json` - Configuration file for filtering parameters
- `test_filter.py` - Test suite for the intelligent filtering functionality
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API keys as environment variables:
```bash
export SCRAPESTACK_API_KEY="your_scrapestack_api_key_here"
export GROQ_API_KEY="your_groq_api_key_here"  # Required for intelligent filtering
```

## Usage

### Original Scraper
```bash
python scrapstack.py
```

### Improved Scraper (Recommended)
```bash
python improved_scraper.py
```

### Intelligent Article Filtering (AI-Powered)
```bash
python intelligent_filter.py
```

### Test the Intelligent Filter
```bash
python test_filter.py
```

## 🤖 Intelligent Article Filtering

The `intelligent_filter.py` module combines web scraping with AI-powered content analysis using Groq's LLM API to intelligently filter articles based on keyword relevance.

### Key Features

- **AI-Powered Analysis**: Uses Groq's Llama3 model for intelligent content analysis
- **Keyword-Based Filtering**: Filters articles based on primary and additional keywords
- **Relevance Scoring**: Assigns relevance scores (0.0-1.0) to each article
- **Batch Processing**: Efficiently processes articles in batches
- **Detailed Reasoning**: Provides explanations for why articles are considered relevant

### Configuration

The filter uses a configurable keyword system defined in `filter_config.json`:

```json
{
    "primary_keyword": "quantum",
    "additional_keywords": [
        "energy", "battery", "solar", "sensor", 
        "engine", "refrigerator", "sensing", 
        "storage", "efficiency"
    ],
    "relevance_threshold": 0.6,
    "max_articles_to_process": 20
}
```

You can easily customize the filtering by editing this configuration file to match your specific interests.

### Sample Output

```
🎯 Found 3 highly relevant articles:

1. 📰 Quantum sensors could revolutionize energy storage systems
   🔗 https://www.newscientist.com/article/...
   📊 Relevance Score: 0.95
   🎯 Matched Keywords: quantum, energy, storage, sensor
   💭 Reasoning: Directly discusses quantum technology applications in energy storage with sensor integration

2. 📰 New quantum battery design promises ultra-fast charging
   🔗 https://www.newscientist.com/article/...
   📊 Relevance Score: 0.88
   🎯 Matched Keywords: quantum, battery, energy, efficiency
   💭 Reasoning: Focuses on quantum battery technology with emphasis on energy efficiency
```

## Improvements in Enhanced Version

### Security Enhancements
- ✅ API key loaded from environment variables (no hardcoded secrets)
- ✅ SSL certificate verification enabled
- ✅ Debug files saved to temp directory instead of current directory

### Reliability Improvements
- ✅ Comprehensive error handling for API failures
- ✅ Request timeout handling (30 seconds)
- ✅ Retry logic with exponential backoff
- ✅ Rate limit handling
- ✅ Proper HTTP status code checking

### Code Quality
- ✅ Professional logging with different levels
- ✅ Type hints for better code maintainability
- ✅ Class-based design for better organization
- ✅ Comprehensive docstrings
- ✅ Input validation

### Features
- ✅ Configurable timeout and retry settings
- ✅ Better article extraction with multiple fallback strategies
- ✅ Duplicate prevention
- ✅ Structured output with numbered results

## Example Output

```
🎉 Successfully found 14 articles:
 1. Making atoms self-magnify reveals their quantum wave functions
    URL: https://www.newscientist.com/article/2496211-making-atoms-self-magnify-reveals-their-quantum-wave-functions/

 2. At last, we are discovering what quantum computers will be useful for
    URL: https://www.newscientist.com/article/2484176-at-last-we-are-discovering-what-quantum-computers-will-be-useful-for/
...
```

## Security Notes

- Never commit API keys to version control
- Always use environment variables for sensitive configuration
- The improved scraper follows security best practices