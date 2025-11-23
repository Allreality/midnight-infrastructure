# File: routes/registry_routes.py

from flask import Blueprint, jsonify
import os
import json

registry_bp = Blueprint("registry", __name__)

REGISTRY_PATH = "registry/claimRegistry.json"  # Adjust if needed

@registry_bp.route("/api/claims/registry", methods=["GET"])
def get_claim_registry():
    if not os.path.exists(REGISTRY_PATH):
        return jsonify([]), 200  # Return empty list instead of 404

    try:
        with open(REGISTRY_PATH, "r") as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500