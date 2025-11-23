# File: routes/claims_verify.py

from flask import Blueprint, request, jsonify
import hashlib

claims_verify_bp = Blueprint("claims_verify", __name__)

@claims_verify_bp.route("/api/claims/verify", methods=["POST"])
def verify_claim():
    data = request.get_json()

    required = ["address", "wallet", "phase", "timestamp", "cid"]
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    raw = f"{data['address']}|{data['wallet']}|{data['phase']}|{data['timestamp']}"
    expected_cid = hashlib.sha256(raw.encode()).hexdigest()

    verified = expected_cid == data["cid"]
    return jsonify({
        "verified": verified,
        "expected_cid": expected_cid,
        "provided_cid": data["cid"]
    }), 200