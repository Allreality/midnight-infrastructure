import os
import json

AGENT_REGISTRY = "agentRegistry.json"
CID_REGISTRY = "projectRegistry.json"
DONATION_REGISTRY = "donationRegistry.json"

def load_registry(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_registry(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)