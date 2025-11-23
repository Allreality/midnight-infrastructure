# File: routes/claims_agents.py

from flask import Blueprint, jsonify

claims_agents_bp = Blueprint("claims_agents", __name__)

@claims_agents_bp.route("/api/claims/agents", methods=["GET"])
def get_agent_stats():
    agents = [
        {
            "agent_id": "agent-001",
            "successful_claims": 42,
            "failed_claims": 8,
            "last_active": "2025-11-02T15:30:00Z"
        },
        {
            "agent_id": "agent-002",
            "successful_claims": 28,
            "failed_claims": 12,
            "last_active": "2025-11-02T14:45:00Z"
        },
        {
            "agent_id": "agent-003",
            "successful_claims": 17,
            "failed_claims": 3,
            "last_active": "2025-11-02T13:10:00Z"
        }
    ]
    return jsonify(agents)