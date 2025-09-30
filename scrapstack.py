import requests
from bs4 import BeautifulSoup
def scrape_with_scrapestack(url):
    api_key = "c050c2e9b44f69e6e2ff7982ac1afff9"
    api_url = f"http://api.scrapestack.com/scrape?access_key={api_key}&url={url}"

    response = requests.get(api_url, verify=False)
    return response.text


def scrape_titles_from_html(html_content):
    """Parse HTML content and extract article titles and URLs"""
    articles = []
    
    try:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("🔍 Parsing HTML content...")
        
        # Multiple selectors for New Scientist articles
        selectors = [
            '.CardLink',
            'a[href*="/article/"]',
            'article a[href*="/article/"]',
            '.Card a[href*="/article/"]'
        ]
        
        for selector in selectors:
            try:
                print(f"Trying selector: {selector}")
                elements = soup.select(selector)
                print(f"Found {len(elements)} potential elements")
                
                for element in elements:
                    try:
                        # Extract URL
                        url = element.get('href', '')
                        
                        # Extract title - try multiple title selectors
                        title = None
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
                                title = title_elem.get_text().strip()
                                break
                        
                        # If no title found in nested elements, try the link text itself
                        if not title and element.get_text().strip():
                            title = element.get_text().strip()
                        
                        # Normalize URL
                        if url and not url.startswith("http"):
                            url = f"https://www.newscientist.com{url}"
                        
                        if title and url and "/article/" in url:
                            # Avoid duplicates
                            if not any(article['url'] == url for article in articles):
                                articles.append({
                                    "title": title,
                                    "url": url
                                })
                                print(f"✅ Found article: {title[:60]}...")
                        
                    except Exception as elem_err:
                        print(f"⚠️ Element error: {elem_err}")
                        continue
                
                if articles:
                    print(f"✅ Found {len(articles)} articles with {selector}")
                    break
                    
            except Exception as e:
                print(f"⚠️ Error with selector {selector}: {str(e)}")
                continue
        
        if not articles:
            print("❌ No articles found in HTML content")
            # Save HTML for debugging
            with open("debug_html.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("📄 HTML content saved to debug_html.html for inspection")
        
        return articles
        
    except Exception as e:
        print(f"❌ Error parsing HTML: {e}")
        return []



# Example usage
if __name__ == "__main__":
    url = "https://www.newscientist.com/article-topic/quantum-science/"
    html_content = scrape_with_scrapestack(url)
    articles = scrape_titles_from_html(html_content)
    print(f"Found {len(articles)} articles:", articles)