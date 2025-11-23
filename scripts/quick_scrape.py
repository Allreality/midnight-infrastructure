#!/usr/bin/env python3
"""
Quick scraper for Midnight sources
"""
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def scrape_midnight_blog():
    """Scrape Midnight blog for latest posts"""
    url = "https://docs.midnight.network/blog"
    
    try:
        print(f"📡 Scraping: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save the content
        os.makedirs("knowledge-base/research", exist_ok=True)
        
        data = {
            "url": url,
            "scraped_at": datetime.utcnow().isoformat(),
            "title": soup.find('title').get_text() if soup.find('title') else "Midnight Blog",
            "content": soup.get_text()[:3000]
        }
        
        filename = f"knowledge-base/research/midnight_blog_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def scrape_whitepaper():
    """Get whitepaper info"""
    url = "https://midnight.network/whitepaper"
    
    try:
        print(f"📡 Scraping: {url}")
        response = requests.get(url, timeout=10)
        
        os.makedirs("knowledge-base/blockchain", exist_ok=True)
        
        data = {
            "url": url,
            "scraped_at": datetime.utcnow().isoformat(),
            "title": "Midnight Whitepaper",
            "status": response.status_code
        }
        
        filename = f"knowledge-base/blockchain/whitepaper_ref_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🌙 Starting Midnight Data Collection...")
    print()
    
    scrape_midnight_blog()
    scrape_whitepaper()
    
    print()
    print("✅ Scraping complete!")
