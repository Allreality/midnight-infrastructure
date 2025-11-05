# File: routes/claims_eligibility.py

# File: routes/claims_eligibility.py

from flask import Blueprint, request, jsonify
from services.eligibility import verify_snapshot_eligibility

claims_eligibility_bp = Blueprint("claims_eligibility", __name__)

@claims_eligibility_bp.route("/api/claims/eligibility", methods=["POST"])
def check_eligibility():
    data = request.get_json()
    address = data.get("address")

    if not address:
        return jsonify({"error": "Missing address"}), 400

    eligible = verify_snapshot_eligibility(address)
    return jsonify({
        "address": address,
        "eligible": eligible,
        "status": "ok" if eligible else "rejected"
    }), 200