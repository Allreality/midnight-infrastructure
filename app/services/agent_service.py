import os
import json
from jsonschema import validate, ValidationError

AGENT_REGISTRY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../agentRegistry.json"))
AGENT_REGISTRY = os.path.join(os.path.dirname(__file__), "../../agentRegistry.json")
AGENT_REGISTRY = os.path.abspath(AGENT_REGISTRY)

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
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_registry(data):
    with open(AGENT_REGISTRY, "w") as f:
        json.dump(data, f, indent=2)

def register_agent(data):
    try:
        print("Incoming data:", data)
        validate(instance=data, schema=agent_schema)
        registry = load_registry()
        print("Loaded registry:", registry)
        registry.append(data)
        save_registry(registry)
        print("Saved registry:", registry)
        return {"status": "registered", "agent": data}, 201
    except ValidationError as e:
        print("Validation error:", e)
        return {"error": str(e)}, 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": "Internal server error"}, 500

def get_agent(agent_id):
    registry = load_registry()
    for agent in registry:
        if agent["agent_id"] == agent_id:
            return agent
    return None

def has_role(agent_id, role):
    agent = get_agent(agent_id)
    return agent and agent.get("role") == role