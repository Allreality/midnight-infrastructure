# File: routes/claims_agents.py

from flask import Blueprint, jsonify
from services.registry import load_registry
from collections import defaultdict
import os

claims_agents_bp = Blueprint("claims_agents", __name__)

CLAIM_REGISTRY = "registry/claimAttempts.json"

@claims_agents_bp.route("/api/claims/agents", methods=["GET"])
def get_agent_stats():
    registry = load_registry(CLAIM_REGISTRY)
    agents = defaultdict(lambda: {"successful_claims": 0, "failed_claims": 0, "last_active": None})

    for entry in registry:
        agent_id = entry.get("wallet", "unknown-agent")
        status = entry.get("status")
        timestamp = entry.get("timestamp")

        if status == "success":
            agents[agent_id]["successful_claims"] += 1
        else:
            agents[agent_id]["failed_claims"] += 1

        if not agents[agent_id]["last_active"] or timestamp > agents[agent_id]["last_active"]:
            agents[agent_id]["last_active"] = timestamp

    # Format for frontend
    formatted = [
        {
            "agent_id": agent,
            "successful_claims": data["successful_claims"],
            "failed_claims": data["failed_claims"],
            "last_active": data["last_active"]
        }
        for agent, data in agents.items()
    ]

    return jsonify(formatted)