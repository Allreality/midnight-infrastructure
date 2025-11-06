# File: /mnt/c/projects/midnight-infrastructure/routes/cid.py

from flask import Blueprint, request, jsonify
from services.registry import load_registry, save_registry, CID_REGISTRY
from services.auth import require_role
from jsonschema import validate, ValidationError
from datetime import datetime

cid_bp = Blueprint("cid", __name__, url_prefix="/api/cid")

cid_schema = {
    "type": "object",
    "properties": {
        "cid": {"type": "string"},
        "agent_id": {"type": "string"},
        "timestamp": {"type": "string"}
    },
    "required": ["cid", "agent_id"]
}

@cid_bp.route("/track", methods=["POST"])
@require_role("steward")
def track_cid():
    data = request.json
    try:
        validate(instance=data, schema=cid_schema)
        data["timestamp"] = datetime.utcnow().isoformat()
        registry = load_registry(CID_REGISTRY)
        registry.append(data)
        save_registry(CID_REGISTRY, registry)
        return jsonify({"status": "tracked", "cid": data}), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    
    @cid_bp.route("/list", methods=["GET"])
    def list_tracked_cids():
        registry = load_registry(CID_REGISTRY)
    if isinstance(registry, list):
        return jsonify({"cids": registry}), 200
    return jsonify({"error": "CID registry is not a list"}), 500