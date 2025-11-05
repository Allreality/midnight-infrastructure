# agents/discordParser.py
"""
Parse Discord announcements for structured data
"""
import re
import json
from datetime import datetime

class DiscordParser:
    def __init__(self):
        self.patterns = {
            'snapshot_date': r'snapshot.*?(\d{4}-\d{2}-\d{2}|\w+ \d{1,2},? \d{4})',
            'eligibility': r'eligible.*?if.*?[:\-](.+?)(?:\n|$)',
            'allocation': r'allocation.*?(\d+(?:,\d+)?)\s*(\w+)',
            'claim_period': r'claim.*?(\d{4}-\d{2}-\d{2}).*?(\d{4}-\d{2}-\d{2})',
            'wallet_address': r'addr1[a-z0-9]{98}'
        }
    
    def parse_announcement(self, content):
        """Extract structured data from Discord announcement"""
        extracted = {
            "parsed_at": datetime.utcnow().isoformat(),
            "raw_content": content
        }
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                extracted[key] = match.group(1) if match.groups() else match.group(0)
        
        return extracted
    
    def extract_eligibility_criteria(self, content):
        """Extract eligibility rules"""
        criteria = []
        
        # Look for common patterns
        if 'held' in content.lower() and 'ada' in content.lower():
            criteria.append("ADA holder")
        
        if 'snapshot' in content.lower():
            criteria.append("Snapshot participant")
        
        if 'staked' in content.lower():
            criteria.append("Staking required")
        
        return criteria

parser = DiscordParser()
