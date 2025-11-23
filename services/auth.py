# services/auth.py

from functools import wraps
from flask import request, jsonify
from services.registry import load_registry, AGENT_REGISTRY

def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.json
            agent_id = data.get("agent_id")
            registry = load_registry(AGENT_REGISTRY)
            for agent in registry:
                if agent.get("agent_id") == agent_id and agent.get("role") == required_role:
                    return f(*args, **kwargs)
            return jsonify({"error": "Unauthorized"}), 403
        return wrapper
    return decorator