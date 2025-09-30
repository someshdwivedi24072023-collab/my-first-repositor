# Web Scraper for New Scientist Articles

This repository contains web scraping tools to extract article information from New Scientist's quantum science section using the ScrapeStack API.

## Files

- `scrapstack.py` - Original scraper implementation
- `improved_scraper.py` - Enhanced version with better security and error handling
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your ScrapeStack API key as an environment variable:
```bash
export SCRAPESTACK_API_KEY="your_api_key_here"
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