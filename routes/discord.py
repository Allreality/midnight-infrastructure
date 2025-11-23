# routes/discord.py
from flask import Blueprint, jsonify
import os
import json
from pathlib import Path

discord_bp = Blueprint("discord", __name__, url_prefix="/api/discord")

@discord_bp.route("/announcements", methods=["GET"])
def get_announcements():
    """Get all Discord announcements"""
    announcements_dir = "knowledge-base/airdrop/discord"
    
    if not os.path.exists(announcements_dir):
        return jsonify({"announcements": []}), 200
    
    announcements = []
    for file in Path(announcements_dir).glob("*.json"):
        with open(file, 'r') as f:
            data = json.load(f)
            announcements.append(data)
    
    # Sort by timestamp, newest first
    announcements.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({
        "count": len(announcements),
        "announcements": announcements[:50]  # Last 50
    }), 200

@discord_bp.route("/latest", methods=["GET"])
def get_latest():
    """Get latest announcement"""
    announcements_dir = "knowledge-base/airdrop/discord"
    
    if not os.path.exists(announcements_dir):
        return jsonify({"message": "No announcements yet"}), 200
    
    files = list(Path(announcements_dir).glob("*.json"))
    if not files:
        return jsonify({"message": "No announcements yet"}), 200
    
    latest = max(files, key=lambda f: f.stat().st_mtime)
    
    with open(latest, 'r') as f:
        data = json.load(f)
    
    return jsonify(data), 200
