# File: /mnt/c/projects/midnight-infrastructure/routes/donations.py

from flask import Blueprint, request, jsonify
from services.registry import load_registry, save_registry, DONATION_REGISTRY
from services.auth import require_role
from datetime import datetime

donations_bp = Blueprint("donations", __name__, url_prefix="/api/donations")

@donations_bp.route("/route", methods=["POST"])
@require_role("architect")
def route_donation():
    ...
    payload = request.json
    payload["timestamp"] = datetime.utcnow().isoformat()
    registry = load_registry(DONATION_REGISTRY)
    registry.append(payload)
    save_registry(DONATION_REGISTRY, registry)
    return jsonify({"status": "received", "payload": payload}), 202