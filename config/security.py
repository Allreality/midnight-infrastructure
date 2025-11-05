"""
Production Security Configuration
"""
import os
from functools import wraps
from flask import request, jsonify

# Rate limiting
REQUEST_LIMITS = {
    'free': 100,
    'professional': 1000,
    'enterprise': 10000
}

# CORS configuration
ALLOWED_ORIGINS = [
    'https://midnight-compliance.io',
    'https://www.midnight-compliance.io'
]

def secure_headers(response):
    """Add security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

def rate_limit(tier='free'):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implement rate limiting logic
            return f(*args, **kwargs)
        return decorated_function
    return decorator
