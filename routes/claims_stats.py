# File: routes/claims_stats.py

from flask import Blueprint, jsonify

claims_stats_bp = Blueprint("claims_stats", __name__)

@claims_stats_bp.route("/api/claims/stats", methods=["GET"])
def get_claim_stats():
    stats = {
        "total_attempts": 124,
        "successful_claims": 87,
        "failed_claims": 37,
        "retry_rate": round(37 / 124, 2),
        "agents_active": 12
    }
    return jsonify(stats)