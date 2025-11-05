# agents/claimAgent.py
import json
import os
from datetime import datetime

CLAIM_LOG_PATH = "registry/claimAttempts.json"

def log_claim_attempt(address, agent_id, status, tx_hash=None):
    """Log a claim attempt"""
    
    # Ensure directory exists
    os.makedirs("registry", exist_ok=True)
    
    # Load existing attempts
    if os.path.exists(CLAIM_LOG_PATH):
        with open(CLAIM_LOG_PATH, 'r') as f:
            attempts = json.load(f)
    else:
        attempts = []
    
    # Create new attempt
    attempt = {
        "address": address,
        "agent_id": agent_id,
        "status": status,
        "tx_hash": tx_hash,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    attempts.append(attempt)
    
    # Save
    with open(CLAIM_LOG_PATH, 'w') as f:
        json.dump(attempts, f, indent=2)
    
    return attempt
