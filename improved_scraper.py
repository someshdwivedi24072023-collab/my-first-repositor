import os
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScrapestackScraper:
    """Improved web scraper using Scrapestack API with better error handling and security."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize scraper with API key from environment or parameter."""
        self.api_key = api_key or os.getenv('SCRAPESTACK_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided via parameter or SCRAPESTACK_API_KEY environment variable")
        
        self.base_url = "http://api.scrapestack.com/scrape"
        self.timeout = 30  # seconds
        self.max_retries = 3
    
    def scrape_url(self, url: str) -> Optional[str]:
        """
        Scrape a URL using Scrapestack API with proper error handling.
        
        Args:
            url: The URL to scrape
            
        Returns:
            HTML content as string, or None if failed
        """
        params = {
            'access_key': self.api_key,
            'url': url
        }
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Scraping {url} (attempt {attempt + 1}/{self.max_retries})")
                
                response = requests.get(
                    self.base_url, 
                    params=params, 
                    timeout=self.timeout,
                    verify=True  # ✅ Enable SSL verification
                )
                
                # Check for API errors
                if response.status_code == 200:
                    # Check if response contains error message
                    if 'error' in response.text.lower() and len(response.text) < 1000:
                        logger.error(f"API Error: {response.text}")
                        return None
                    
                    logger.info("Successfully scraped content")
                    return response.text
                
                elif response.status_code == 429:
                    logger.warning("Rate limit exceeded, waiting before retry...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
                else:
                    logger.error(f"HTTP Error {response.status_code}: {response.text}")
                    return None
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                return None
        
        logger.error("All retry attempts failed")
        return None

    def extract_articles(self, html_content: str, base_domain: str = "https://www.newscientist.com") -> List[Dict[str, str]]:
        """
        Extract article information from HTML content.
        
        Args:
            html_content: Raw HTML content
            base_domain: Base domain for relative URL conversion
            
        Returns:
            List of dictionaries containing article title and URL
        """
        articles = []
        
        if not html_content:
            logger.error("No HTML content provided")
            return articles
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.info("Parsing HTML content...")
            
            # Multiple selectors for New Scientist articles
            selectors = [
                '.CardLink',
                'a[href*="/article/"]',
                'article a[href*="/article/"]',
                '.Card a[href*="/article/"]'
            ]
            
            for selector in selectors:
                try:
                    logger.debug(f"Trying selector: {selector}")
                    elements = soup.select(selector)
                    logger.debug(f"Found {len(elements)} potential elements")
                    
                    for element in elements:
                        try:
                            # Extract URL
                            url = element.get('href', '')
                            
                            # Extract title - try multiple title selectors
                            title = self._extract_title(element)
                            
                            # Normalize URL
                            if url and not url.startswith("http"):
                                url = f"{base_domain}{url}"
                            
                            if title and url and "/article/" in url:
                                # Avoid duplicates
                                if not any(article['url'] == url for article in articles):
                                    articles.append({
                                        "title": title,
                                        "url": url
                                    })
                                    logger.debug(f"Found article: {title[:60]}...")
                            
                        except Exception as elem_err:
                            logger.warning(f"Element parsing error: {elem_err}")
                            continue
                    
                    if articles:
                        logger.info(f"Successfully found {len(articles)} articles with {selector}")
                        break
                        
                except Exception as e:
                    logger.warning(f"Error with selector {selector}: {str(e)}")
                    continue
            
            if not articles:
                logger.warning("No articles found in HTML content")
                # Optionally save debug HTML to temp directory
                self._save_debug_html(html_content)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return []

    def _extract_title(self, element) -> Optional[str]:
        """Extract title from an element using multiple strategies."""
        title_selectors = [
            '.Card__Title', 
            'h3', 
            'h2',
            '.title',
            '[class*="title"]'
        ]
        
        for title_selector in title_selectors:
            title_elem = element.select_one(title_selector)
            if title_elem and title_elem.get_text().strip():
                return title_elem.get_text().strip()
        
        # If no title found in nested elements, try the link text itself
        if element.get_text().strip():
            return element.get_text().strip()
        
        return None

    def _save_debug_html(self, html_content: str):
        """Save HTML content for debugging purposes."""
        try:
            debug_dir = "/tmp"  # Use temp directory instead of current directory
            debug_file = os.path.join(debug_dir, f"debug_html_{int(time.time())}.html")
            
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"HTML content saved to {debug_file} for inspection")
            
        except Exception as e:
            logger.error(f"Failed to save debug HTML: {e}")


def main():
    """Main function demonstrating usage."""
    try:
        # ✅ Try to get API key from environment first
        scraper = ScrapestackScraper()
        
        url = "https://www.newscientist.com/article-topic/quantum-science/"
        
        # Scrape content
        html_content = scraper.scrape_url(url)
        
        if html_content:
            # Extract articles
            articles = scraper.extract_articles(html_content)
            
            print(f"\n🎉 Successfully found {len(articles)} articles:")
            for i, article in enumerate(articles, 1):
                print(f"{i:2d}. {article['title']}")
                print(f"    URL: {article['url']}\n")
        else:
            print("❌ Failed to scrape content")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Set your API key as environment variable: export SCRAPESTACK_API_KEY='your_key_here'")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()