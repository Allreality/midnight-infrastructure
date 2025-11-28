"""
Analytics and Tracking System for Midnight X402
Captures all user interactions and business metrics
"""

import json
from datetime import datetime
import os

# Analytics storage (use database in production)
analytics_events = []
user_sessions = {}

class AnalyticsTracker:
    """Track user interactions and business metrics"""
    
    @staticmethod
    def track_event(event_type, data, user_id=None):
        """Track any event with metadata"""
        event = {
            'event_id': f"evt_{int(datetime.utcnow().timestamp() * 1000)}",
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'data': data
        }
        analytics_events.append(event)
        
        # Also save to file for persistence
        log_file = '/mnt/c/projects/midnight-infrastructure/analytics_log.jsonl'
        with open(log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        return event
    
    @staticmethod
    def track_purchase_attempt(payment_id, service_id, amount_sol, user_wallet):
        """Track purchase attempts"""
        return AnalyticsTracker.track_event('purchase_attempt', {
            'payment_id': payment_id,
            'service_id': service_id,
            'amount_sol': amount_sol,
            'amount_usd': amount_sol * 136.82
        }, user_wallet)
    
    @staticmethod
    def track_purchase_success(payment_id, service_id, amount_sol, user_wallet, tx_signature):
        """Track successful purchases"""
        return AnalyticsTracker.track_event('purchase_success', {
            'payment_id': payment_id,
            'service_id': service_id,
            'amount_sol': amount_sol,
            'amount_usd': amount_sol * 136.82,
            'transaction_signature': tx_signature
        }, user_wallet)
    
    @staticmethod
    def track_file_download(filename, service_id, user_wallet):
        """Track file downloads"""
        return AnalyticsTracker.track_event('file_download', {
            'filename': filename,
            'service_id': service_id,
            'file_type': filename.split('.')[-1]
        }, user_wallet)
    
    @staticmethod
    def get_analytics_summary():
        """Get analytics summary"""
        total_events = len(analytics_events)
        
        # Count by event type
        events_by_type = {}
        for event in analytics_events:
            event_type = event['event_type']
            events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
        
        # Calculate revenue
        purchase_events = [e for e in analytics_events if e['event_type'] == 'purchase_success']
        total_revenue_sol = sum(e['data']['amount_sol'] for e in purchase_events)
        total_revenue_usd = sum(e['data']['amount_usd'] for e in purchase_events)
        
        # Unique users
        unique_wallets = set(e['user_id'] for e in analytics_events if e['user_id'])
        
        # Conversion rate
        attempts = events_by_type.get('purchase_attempt', 0)
        successes = events_by_type.get('purchase_success', 0)
        conversion_rate = (successes / attempts * 100) if attempts > 0 else 0
        
        # Service popularity
        service_purchases = {}
        for event in purchase_events:
            service_id = event['data']['service_id']
            service_purchases[service_id] = service_purchases.get(service_id, 0) + 1
        
        return {
            'total_events': total_events,
            'events_by_type': events_by_type,
            'unique_users': len(unique_wallets),
            'total_purchases': successes,
            'total_revenue': {
                'sol': total_revenue_sol,
                'usd': total_revenue_usd
            },
            'conversion_rate': f"{conversion_rate:.2f}%",
            'service_popularity': service_purchases,
            'period': 'all_time'
        }

def init_analytics():
    """Initialize analytics system"""
    # Create analytics log file if it doesn't exist
    log_file = '/mnt/c/projects/midnight-infrastructure/analytics_log.jsonl'
    if not os.path.exists(log_file):
        open(log_file, 'w').close()
    
    # Load existing events
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    analytics_events.append(event)
    except:
        pass