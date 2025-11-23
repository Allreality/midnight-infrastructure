from flask import Blueprint, request, jsonify
from services.auth import require_role
from services.registry import load_registry, save_registry


claims_bp = Blueprint("claims_bp", __name__, url_prefix="/api/claims")

@claims_bp.route("/attempts", methods=["POST"])
#@require_role("steward")
def log_claim_attempt():
    data = request.get_json()
    registry = load_registry("registry/claimAttempts.json")
    registry.append(data)
    save_registry("registry/claimAttempts.json", registry)
    return jsonify({"status": "logged", "attempt": data}), 201

@claims_bp.route("/attempts", methods=["GET"])
def get_claim_attempts():
    registry = load_registry("registry/claimAttempts.json")
    return jsonify({"claims": registry}), 200

{
  "agent_id": "akil-hashim",
  "address": "addr1q96d08t9ewwatpacat7gntaz7yxljuz636pjkp995sg6zu6she9wyxestaml8uwhgadanxye4uqyea6xg8vmge3kr5nqyzd775",
  "wallet": "Nami",
  "phase": "Phase 2",
  "timestamp": "2025-11-02T12:11:00Z",
  "status": "failed",
  "notes": "Lace integration failed to sign payload"
}

TEST_MODE = True

def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if TEST_MODE:
                return f(*args, **kwargs)
            # ... existing role check logic
        return wrapper
    return decorator