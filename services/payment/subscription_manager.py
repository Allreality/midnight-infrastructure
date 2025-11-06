"""
Subscription Management System
Tracks active subscriptions and access levels
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class SubscriptionManager:
    def __init__(self):
        self.db_path = "data/subscriptions.json"
        os.makedirs("data", exist_ok=True)
        
        # Load existing subscriptions
        self.subscriptions = self._load_subscriptions()
    
    def _load_subscriptions(self):
        """Load subscriptions from file"""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_subscriptions(self):
        """Save subscriptions to file"""
        with open(self.db_path, 'w') as f:
            json.dump(self.subscriptions, f, indent=2)
    
    def create_subscription(self, wallet_address, tier, tx_hash):
        """
        Create new subscription after payment verification
        """
        # Calculate expiration (30 days for monthly)
        expiration = (datetime.utcnow() + timedelta(days=30)).isoformat()
        
        subscription = {
            'wallet': wallet_address,
            'tier': tier,
            'tx_hash': tx_hash,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': expiration,
            'status': 'active',
            'auto_renew': False
        }
        
        self.subscriptions[wallet_address] = subscription
        self._save_subscriptions()
        
        return subscription
    
    def get_subscription(self, wallet_address):
        """Get subscription details for wallet"""
        sub = self.subscriptions.get(wallet_address)
        
        if not sub:
            return {
                'tier': 'free',
                'status': 'none',
                'expires_at': None
            }
        
        # Check if expired
        if datetime.fromisoformat(sub['expires_at']) < datetime.utcnow():
            sub['status'] = 'expired'
            self._save_subscriptions()
        
        return sub
    
    def check_access(self, wallet_address, feature):
        """
        Check if wallet has access to specific feature
        """
        sub = self.get_subscription(wallet_address)
        tier = sub['tier']
        
        # Load tier features
        with open('config/access_tiers.json', 'r') as f:
            tiers = json.load(f)['tiers']
        
        tier_features = tiers.get(tier, {}).get('features', [])
        
        # Check if feature is included
        return any(feature.lower() in f.lower() for f in tier_features)
    
    def get_rate_limit(self, wallet_address):
        """Get rate limit for wallet's tier"""
        sub = self.get_subscription(wallet_address)
        tier = sub['tier']
        
        with open('config/access_tiers.json', 'r') as f:
            tiers = json.load(f)['tiers']
        
        return tiers.get(tier, {}).get('rate_limits', {})
    
    def renew_subscription(self, wallet_address, tx_hash):
        """Renew existing subscription"""
        sub = self.subscriptions.get(wallet_address)
        
        if sub:
            # Extend expiration by 30 days
            current_expiry = datetime.fromisoformat(sub['expires_at'])
            new_expiry = current_expiry + timedelta(days=30)
            
            sub['expires_at'] = new_expiry.isoformat()
            sub['status'] = 'active'
            sub['last_renewal_tx'] = tx_hash
            
            self._save_subscriptions()
        
        return sub

subscription_manager = SubscriptionManager()
