# agents/webScraper.py
"""
Web scraper for official Midnight sources
"""
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse

class MidnightWebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'MidnightResearchBot/1.0'
        }
        self.base_dir = "knowledge-base"
        
    def scrape_page(self, url, category="general"):
        """Scrape a single page"""
        try:
            print(f"🔍 Scraping: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract content
            data = {
                "url": url,
                "scraped_at": datetime.utcnow().isoformat(),
                "title": self.extract_title(soup),
                "content": self.extract_content(soup),
                "links": self.extract_links(soup, url),
                "category": category
            }
            
            # Save
            self.save_scraped_data(data, category)
            
            return data
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return None
    
    def extract_title(self, soup):
        """Extract page title"""
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        return "Untitled"
    
    def extract_content(self, soup):
        """Extract main content"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to first 5000 chars
    
    def extract_links(self, soup, base_url):
        """Extract all links"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only keep midnight.network links
            if 'midnight' in full_url.lower():
                links.append({
                    "text": link.get_text().strip(),
                    "url": full_url
                })
        
        return links[:20]  # Limit to 20 links
    
    def save_scraped_data(self, data, category):
        """Save scraped data"""
        # Create directory
        dir_path = os.path.join(self.base_dir, "scraped", category)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create filename from URL
        parsed = urlparse(data['url'])
        filename = f"{parsed.netloc}_{parsed.path.replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
        filename = filename.replace('..', '_')
        
        filepath = os.path.join(dir_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved: {filepath}")
    
    def scrape_all_sources(self):
        """Scrape all configured sources"""
        with open('config/midnight_sources.json', 'r') as f:
            sources = json.load(f)
        
        results = {
            "scraped_at": datetime.utcnow().isoformat(),
            "successful": 0,
            "failed": 0,
            "sources": []
        }
        
        for category, items in sources['official_sources'].items():
            for item in items:
                if item.get('scrape', False):
                    data = self.scrape_page(item['url'], category)
                    
                    if data:
                        results['successful'] += 1
                        results['sources'].append({
                            "name": item['name'],
                            "url": item['url'],
                            "status": "success"
                        })
                    else:
                        results['failed'] += 1
                        results['sources'].append({
                            "name": item['name'],
                            "url": item['url'],
                            "status": "failed"
                        })
        
        # Save summary
        summary_path = os.path.join(self.base_dir, "scrape_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results

scraper = MidnightWebScraper()

if __name__ == "__main__":
    results = scraper.scrape_all_sources()
    print(f"\n✅ Scraping complete!")
    print(f"   Successful: {results['successful']}")
    print(f"   Failed: {results['failed']}")
