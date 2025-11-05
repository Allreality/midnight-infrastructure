# File: /mnt/c/projects/midnight-infrastructure/routes/agents.py

from flask import Blueprint, request, jsonify
from services.registry import load_registry, save_registry, AGENT_REGISTRY
from jsonschema import validate, ValidationError

agents_bp = Blueprint("agents", __name__, url_prefix="/api/agents")

agent_schema = {
    "type": "object",
    "properties": {
        "agent_id": {"type": "string"},
        "role": {"type": "string"},
        "wallet": {"type": "string"},
        "cid": {"type": "string"}
    },
    "required": ["agent_id", "role", "wallet", "cid"]
}

@agents_bp.route("/register", methods=["POST"])
def register_agent():
    data = request.json
    try:
        validate(instance=data, schema=agent_schema)
        registry = load_registry(AGENT_REGISTRY)
        registry.append(data)
        save_registry(AGENT_REGISTRY, registry)
        return jsonify({"status": "registered", "agent": data}), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

@agents_bp.route("/<agent_id>", methods=["GET"])
def get_agent(agent_id):
    registry = load_registry(AGENT_REGISTRY)
    for agent in registry:
        if agent.get("agent_id") == agent_id:
            return jsonify({"agent": agent}), 200
    return jsonify({"error": "Agent not found"}), 404