# agent_service.py — Agent registration, lookup, and role validation
# Location: /mnt/c/projects/midnight-infrastructure/app/services/agent_service.py

import json
import os
from jsonschema import validate, ValidationError

AGENT_REGISTRY = "agentRegistry.json"

agent_schema = {
    "type": "object",
    "properties": {
        "agent_id": {"type": "string"},
        "role": {"type": "string", "enum": ["architect", "steward", "auditor"]},
        "wallet": {"type": "string"},
        "cid": {"type": "string"}
    },
    "required": ["agent_id", "role", "wallet", "cid"]
}

def load_registry():
    if os.path.exists(AGENT_REGISTRY):
        with open(AGENT_REGISTRY, "r") as f:
            return json.load(f)
    return []

def save_registry(data):
    with open(AGENT_REGISTRY, "w") as f:
        json.dump(data, f, indent=2)

def register_agent(data):
    try:
        validate(instance=data, schema=agent_schema)
        registry = load_registry()
        registry.append(data)
        save_registry(registry)
        return {"status": "registered", "agent": data}, 201
    except ValidationError as e:
        return {"error": str(e)}, 400

def get_agent(agent_id):
    registry = load_registry()
    for agent in registry:
        if agent["agent_id"] == agent_id:
            return agent
    return None

def has_role(agent_id, role):
    agent = get_agent(agent_id)
    return agent and agent.get("role") == role

def register_agent(data):
    try:
        print("Incoming data:", data)
        validate(instance=data, schema=agent_schema)
        registry = load_registry()
        print("Loaded registry:", registry)
        registry.append(data)
        save_registry(registry)
        return {"status": "registered", "agent": data}, 201
    except ValidationError as e:
        print("Validation error:", e)
        return {"error": str(e)}, 400
    except Exception as e:
        print("Unexpected error:", e)
        return {"error": "Internal server error"}, 500