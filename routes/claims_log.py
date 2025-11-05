from flask import Blueprint, request, jsonify
from agents.claimAgent import log_claim_attempt
from services.eligibility import verify_snapshot_eligibility  # ✅ make sure this is imported

claims_log_bp = Blueprint("claims_log", __name__)

@claims_log_bp.route("/api/claims/log", methods=["POST"])
def log_claim():
    data = request.get_json()

    required_fields = ["address", "wallet", "phase", "status", "notes"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # ✅ Enforce eligibility before logging
    if not verify_snapshot_eligibility(data["address"]):
        return jsonify({
            "error": "Wallet is not eligible to claim",
            "address": data["address"],
            "status": "rejected"
        }), 403

    attempt = log_claim_attempt(
        address=data["address"],
        wallet=data["wallet"],
        phase=data["phase"],
        status=data["status"],
        notes=data["notes"]
    )
    return jsonify(attempt), 201