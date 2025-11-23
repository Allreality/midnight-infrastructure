"""
Access Control Middleware
Protects routes based on subscription tier
"""
from functools import wraps
from flask import request, jsonify
from services.payment.subscription_manager import subscription_manager

def require_subscription(tier='free'):
    """
    Decorator to require specific subscription tier
    Usage: @require_subscription('professional')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get wallet from request
            wallet = request.headers.get('X-Wallet-Address')
            
            if not wallet:
                return jsonify({
                    "error": "Wallet address required",
                    "message": "Include X-Wallet-Address header"
                }), 401
            
            # Check subscription
            subscription = subscription_manager.get_subscription(wallet)
            
            # Define tier hierarchy
            tier_levels = {
                'free': 0,
                'professional': 1,
                'enterprise': 2
            }
            
            user_level = tier_levels.get(subscription['tier'], 0)
            required_level = tier_levels.get(tier, 0)
            
            if user_level < required_level:
                return jsonify({
                    "error": "Insufficient subscription",
                    "required_tier": tier,
                    "current_tier": subscription['tier'],
                    "upgrade_url": "/api/payment/pricing"
                }), 403
            
            # Check if subscription is expired
            if subscription.get('status') == 'expired':
                return jsonify({
                    "error": "Subscription expired",
                    "expired_at": subscription.get('expires_at'),
                    "renew_url": "/api/payment/renew"
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
