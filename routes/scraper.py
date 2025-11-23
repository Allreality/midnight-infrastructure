# routes/scraper.py
from flask import Blueprint, jsonify, request
from agents.webScraper import scraper
import json
import os

scraper_bp = Blueprint("scraper", __name__, url_prefix="/api/scraper")

@scraper_bp.route("/run", methods=["POST"])
def run_scraper():
    """Trigger scraping of all sources"""
    try:
        results = scraper.scrape_all_sources()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scraper_bp.route("/sources", methods=["GET"])
def get_sources():
    """Get all configured sources"""
    with open('config/midnight_sources.json', 'r') as f:
        sources = json.load(f)
    return jsonify(sources), 200

@scraper_bp.route("/summary", methods=["GET"])
def get_summary():
    """Get last scrape summary"""
    summary_path = "knowledge-base/scrape_summary.json"
    
    if not os.path.exists(summary_path):
        return jsonify({"message": "No scrapes yet"}), 200
    
    with open(summary_path, 'r') as f:
        summary = json.load(f)
    
    return jsonify(summary), 200

@scraper_bp.route("/scrape/<category>", methods=["POST"])
def scrape_category(category):
    """Scrape specific category only"""
    data = request.json
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "URL required"}), 400
    
    result = scraper.scrape_page(url, category)
    
    if result:
        return jsonify({"status": "success", "data": result}), 200
    else:
        return jsonify({"status": "failed"}), 500
