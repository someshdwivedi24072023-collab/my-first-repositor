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

### Before Exclusion Filtering:
✅ **Successfully scraped 14 articles**  
🤖 **AI filtered 11 articles as highly relevant (79% relevance rate)**  
📊 **Relevance scores: 0.80 - 1.00**  

### After Exclusion Filtering:
✅ **Successfully scraped 14 articles**  
🤖 **AI filtered 2 articles as highly relevant (14% relevance rate, 85% exclusion rate)**  
📊 **Relevance scores: 1.00**  

### Top Results (Post-Exclusion):
- Closing the last loophole for unhackable quantum security (1.00)
- Quantum technology set to hit the streets within two years (1.00)

**Successfully Excluded**: Quantum computing articles, theoretical physics papers, and qubit research

## Configuration

Edit `filter_config.json` to customize:
- **Primary keyword**: Main topic to search for (e.g., "quantum")
- **Additional keywords**: Related terms to boost relevance (e.g., "energy", "battery", "sensor")
- **Exclusion keywords**: Topics to exclude (e.g., "quantum computing", "qubits", "QPU")
- **Relevance threshold**: Minimum score to include articles (0.0-1.0)
- **Maximum articles to process**: Limit for batch processing

### Exclusion Filtering
The system now supports intelligent exclusion of unwanted topics:
```json
{
    "exclusion_keywords": [
        "quantum computing",
        "qubits", 
        "QPU",
        "theoretical physics"
    ]
}
```

This dramatically improves filtering precision by excluding articles about:
- Pure quantum computing research
- Theoretical quantum physics without practical applications
- Quantum processor/qubit development

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