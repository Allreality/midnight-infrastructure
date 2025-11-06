# File: routes/claim_initial_state.py

from flask import Blueprint, request, jsonify

claim_state_bp = Blueprint("claim_state", __name__)

@claim_state_bp.route("/claim/initialState", methods=["GET"])
def get_initial_state():
    address = request.args.get("address")

    # Placeholder logic — replace with real lookup
    if address:
        state = {
            "address": address,
            "phase": "glacier-drop",
            "status": "pending",
            "agent_id": "agent-001"
        }
    else:
        state = {
            "phase": "glacier-drop",
            "status": "uninitialized",
            "agent_id": None
        }

    return jsonify(state)