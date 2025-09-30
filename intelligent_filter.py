import os
import json
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import requests
from improved_scraper import ScrapestackScraper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FilterConfig:
    """Configuration for article filtering."""
    primary_keyword: str
    additional_keywords: List[str]
    exclusion_keywords: List[str] = None
    relevance_threshold: float = 0.7
    max_articles_to_process: int = 50
    
    def __post_init__(self):
        """Initialize exclusion_keywords as empty list if None."""
        if self.exclusion_keywords is None:
            self.exclusion_keywords = []

class GroqLLMFilter:
    """Intelligent article filter using Groq LLM API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Groq LLM filter."""
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("Groq API key must be provided via parameter or GROQ_API_KEY environment variable")
        
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"  # Fast and efficient model
        self.timeout = 30
        
    def filter_articles(self, articles: List[Dict[str, str]], config: FilterConfig) -> List[Dict[str, Any]]:
        """
        Filter articles using Groq LLM based on keyword relevance.
        
        Args:
            articles: List of articles with 'title' and 'url' keys
            config: Filter configuration with keywords and thresholds
            
        Returns:
            List of filtered articles with relevance scores and reasoning
        """
        if not articles:
            logger.warning("No articles provided for filtering")
            return []
        
        logger.info(f"Filtering {len(articles)} articles using Groq LLM...")
        filtered_articles = []
        
        # Process articles in batches to avoid overwhelming the API
        batch_size = min(5, len(articles))
        
        for i in range(0, min(len(articles), config.max_articles_to_process), batch_size):
            batch = articles[i:i + batch_size]
            try:
                batch_results = self._process_batch(batch, config)
                filtered_articles.extend(batch_results)
                logger.info(f"Processed batch {i//batch_size + 1}, found {len(batch_results)} relevant articles")
            except Exception as e:
                logger.error(f"Error processing batch {i//batch_size + 1}: {e}")
                continue
        
        # Sort by relevance score (highest first)
        filtered_articles.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        logger.info(f"Filtering complete: {len(filtered_articles)} relevant articles found")
        return filtered_articles
    
    def _process_batch(self, articles: List[Dict[str, str]], config: FilterConfig) -> List[Dict[str, Any]]:
        """Process a batch of articles through the LLM."""
        # Create the prompt for the LLM
        prompt = self._create_filtering_prompt(articles, config)
        
        try:
            response = self._call_groq_api(prompt)
            return self._parse_llm_response(response, articles)
        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            return []
    
    def _create_filtering_prompt(self, articles: List[Dict[str, str]], config: FilterConfig) -> str:
        """Create a structured prompt for the LLM to analyze articles."""
        articles_text = ""
        for i, article in enumerate(articles, 1):
            articles_text += f"{i}. Title: {article['title']}\n   URL: {article['url']}\n\n"
        
        additional_keywords_str = ", ".join(config.additional_keywords)
        exclusion_keywords_str = ", ".join(config.exclusion_keywords) if config.exclusion_keywords else "None"
        
        exclusion_section = ""
        if config.exclusion_keywords:
            exclusion_section = f"""
EXCLUSION CRITERIA:
- EXCLUDE articles primarily about: {exclusion_keywords_str}
- EXCLUDE theoretical quantum physics without practical applications
- EXCLUDE pure quantum computing research without energy/sensing applications
"""
        
        prompt = f"""You are an expert content analyst specializing in scientific and technology articles. Your task is to analyze the following articles and determine their relevance based on specific keywords while excluding certain topics.

PRIMARY KEYWORD: "{config.primary_keyword}"
ADDITIONAL KEYWORDS: {additional_keywords_str}{exclusion_section}

ARTICLES TO ANALYZE:
{articles_text}

INSTRUCTIONS:
1. For each article, analyze the title for relevance to the primary keyword "{config.primary_keyword}"
2. Check if the article also relates to any of the additional keywords: {additional_keywords_str}
3. IMPORTANT: EXCLUDE articles that are primarily about: {exclusion_keywords_str}
4. EXCLUDE articles about theoretical quantum physics without practical applications
5. Assign a relevance score from 0.0 to 1.0 where:
   - 1.0 = Highly relevant (directly about {config.primary_keyword} AND mentions additional keywords, NOT excluded topics)
   - 0.8 = Very relevant (directly about {config.primary_keyword} with some connection to additional keywords, NOT excluded topics)
   - 0.6 = Moderately relevant (about {config.primary_keyword} but limited connection to additional keywords, NOT excluded topics)
   - 0.4 = Somewhat relevant (mentions {config.primary_keyword} but not the main focus, NOT excluded topics)
   - 0.2 = Barely relevant (tangential mention of {config.primary_keyword}, NOT excluded topics)
   - 0.0 = Not relevant OR excluded topic (no meaningful connection to {config.primary_keyword} OR matches exclusion criteria)

6. Only include articles with relevance score >= {config.relevance_threshold}
7. Provide a brief reasoning for each relevant article

RESPOND IN VALID JSON FORMAT:
{{
    "filtered_articles": [
        {{
            "article_number": 1,
            "relevance_score": 0.9,
            "reasoning": "Brief explanation of why this article is relevant and not excluded",
            "matched_keywords": ["keyword1", "keyword2"]
        }}
    ]
}}

Only include articles that meet the relevance threshold of {config.relevance_threshold} or higher AND do not match exclusion criteria."""
        
        return prompt
    
    def _call_groq_api(self, prompt: str) -> Dict[str, Any]:
        """Make API call to Groq."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a precise content analyst. Always respond with valid JSON format as requested."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,  # Low temperature for consistent analysis
            "max_tokens": 2000,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Groq API error {response.status_code}: {response.text}")
                raise Exception(f"API call failed with status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Groq API failed: {e}")
            raise
    
    def _parse_llm_response(self, response: Dict[str, Any], original_articles: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Parse the LLM response and match with original articles."""
        try:
            content = response['choices'][0]['message']['content']
            
            # Try to extract JSON from the response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in LLM response")
                return []
            
            json_content = content[json_start:json_end]
            parsed_response = json.loads(json_content)
            
            filtered_results = []
            
            for item in parsed_response.get('filtered_articles', []):
                article_num = item.get('article_number', 0) - 1  # Convert to 0-based index
                
                if 0 <= article_num < len(original_articles):
                    original_article = original_articles[article_num]
                    
                    filtered_article = {
                        'title': original_article['title'],
                        'url': original_article['url'],
                        'relevance_score': item.get('relevance_score', 0.0),
                        'reasoning': item.get('reasoning', 'No reasoning provided'),
                        'matched_keywords': item.get('matched_keywords', [])
                    }
                    
                    filtered_results.append(filtered_article)
            
            return filtered_results
            
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.error(f"Error parsing LLM response: {e}")
            logger.debug(f"Raw response: {response}")
            return []

class IntelligentNewsScraper:
    """Combined scraper and intelligent filter."""
    
    def __init__(self, scrapestack_api_key: Optional[str] = None, groq_api_key: Optional[str] = None):
        """Initialize the intelligent news scraper."""
        self.scraper = ScrapestackScraper(scrapestack_api_key)
        self.filter = GroqLLMFilter(groq_api_key)
    
    def scrape_and_filter(self, url: str, filter_config: FilterConfig) -> List[Dict[str, Any]]:
        """
        Scrape articles from URL and filter them using LLM.
        
        Args:
            url: URL to scrape
            filter_config: Configuration for filtering
            
        Returns:
            List of filtered and scored articles
        """
        logger.info("Starting intelligent news scraping and filtering...")
        
        # Step 1: Scrape articles
        logger.info("Step 1: Scraping articles...")
        html_content = self.scraper.scrape_url(url)
        
        if not html_content:
            logger.error("Failed to scrape content")
            return []
        
        articles = self.scraper.extract_articles(html_content)
        
        if not articles:
            logger.error("No articles extracted")
            return []
        
        logger.info(f"Scraped {len(articles)} articles")
        
        # Step 2: Filter articles using LLM
        logger.info("Step 2: Filtering articles with LLM...")
        filtered_articles = self.filter.filter_articles(articles, filter_config)
        
        return filtered_articles

def load_config_from_file(config_file: str = "filter_config.json") -> FilterConfig:
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return FilterConfig(
            primary_keyword=config_data["primary_keyword"],
            additional_keywords=config_data["additional_keywords"],
            exclusion_keywords=config_data.get("exclusion_keywords", []),
            relevance_threshold=config_data.get("relevance_threshold", 0.6),
            max_articles_to_process=config_data.get("max_articles_to_process", 20)
        )
    except FileNotFoundError:
        logger.warning(f"Config file {config_file} not found, using default configuration")
        return FilterConfig(
            primary_keyword="quantum",
            additional_keywords=["energy", "battery", "solar", "sensor", "engine", "refrigerator", "sensing", "storage", "efficiency"],
            exclusion_keywords=[],
            relevance_threshold=0.6,
            max_articles_to_process=20
        )
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        raise

def main():
    """Main function demonstrating the intelligent filtering."""
    try:
        # Load configuration from file
        filter_config = load_config_from_file()
        
        logger.info(f"Using filter configuration:")
        logger.info(f"  Primary keyword: {filter_config.primary_keyword}")
        logger.info(f"  Additional keywords: {', '.join(filter_config.additional_keywords)}")
        logger.info(f"  Relevance threshold: {filter_config.relevance_threshold}")
        logger.info(f"  Max articles to process: {filter_config.max_articles_to_process}")
        
        # Initialize the intelligent scraper
        intelligent_scraper = IntelligentNewsScraper()
        
        # URL to scrape
        url = "https://www.newscientist.com/article-topic/quantum-science/"
        
        # Scrape and filter
        filtered_articles = intelligent_scraper.scrape_and_filter(url, filter_config)
        
        # Display results
        if filtered_articles:
            print(f"\n🎯 Found {len(filtered_articles)} highly relevant articles:\n")
            print("=" * 80)
            
            for i, article in enumerate(filtered_articles, 1):
                print(f"\n{i}. 📰 {article['title']}")
                print(f"   🔗 {article['url']}")
                print(f"   📊 Relevance Score: {article['relevance_score']:.2f}")
                print(f"   🎯 Matched Keywords: {', '.join(article['matched_keywords'])}")
                print(f"   💭 Reasoning: {article['reasoning']}")
                print("-" * 80)
        else:
            print("❌ No articles met the relevance criteria")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Required environment variables:")
        print("   - SCRAPESTACK_API_KEY: Your ScrapeStack API key")
        print("   - GROQ_API_KEY: Your Groq API key")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()