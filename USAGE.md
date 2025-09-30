# 🚀 Quick Usage Guide

## Setup Environment
```bash
# Set up API keys (run once per session)
source setup_env.sh
```

## Basic Usage

### 1. Scrape Specific URL
```bash
python scrape_page.py "https://www.newscientist.com/article-topic/quantum-science/page/10/"
```

### 2. Run Full Intelligent Filter
```bash
python intelligent_filter.py
```

### 3. Run Original Scraper
```bash
python improved_scraper.py
```

### 4. Run Tests
```bash
python test_filter.py
```

### 5. Interactive Demo
```bash
python demo.py
```

### 6. Automated Demo
```bash
python demo_auto.py
```

## Example Output for Page 10

✅ **Successfully scraped 14 articles**  
🤖 **AI filtered 11 articles as highly relevant**  
📊 **Relevance scores: 0.80 - 1.00**  

### Top Results:
- Closing the last loophole for unhackable quantum security (1.00)
- Quantum technology set to hit the streets within two years (1.00)
- Basic quantum computation achieved with silicon for first time (1.00)
- Where does quantum weirdness end? (1.00)
- Quantum weirdness proved real in first loophole-free experiment (1.00)

## Configuration

Edit `filter_config.json` to customize:
- Keywords to match
- Relevance threshold
- Maximum articles to process
- LLM model settings

## Troubleshooting

### API Key Issues
```bash
# Check if keys are set
echo $SCRAPESTACK_API_KEY
echo $GROQ_API_KEY

# Re-run setup if needed
source setup_env.sh
```

### Dependencies
```bash
pip install -r requirements.txt
```