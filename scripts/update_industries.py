#!/usr/bin/env python3
"""
Update industry knowledge with latest Midnight documentation
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

def scrape_midnight_use_cases():
    """Scrape official Midnight use cases"""
    url = "https://docs.midnight.network/learn/introduction/use-cases/"
    
    try:
        print(f"📡 Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save to knowledge base
        data = {
            "source": url,
            "scraped_at": datetime.utcnow().isoformat(),
            "title": "Midnight Use Cases",
            "content": soup.get_text()[:5000]
        }
        
        os.makedirs("knowledge-base/midnight", exist_ok=True)
        filename = f"knowledge-base/midnight/use_cases_update_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🌙 Updating Midnight Industry Knowledge...\n")
    scrape_midnight_use_cases()
    print("\n✅ Update complete!")
