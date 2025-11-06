from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)

# Import all routes
from routes.health import bp as health_bp
from routes.agents import agents_bp
from routes.cid import cid_bp
from routes.donations import donations_bp
from routes.claims import claims_bp
from routes.registry_routes import registry_bp

# Check if new routes exist before importing
try:
    from routes.payment import payment_bp
    app.register_blueprint(payment_bp)
    print("✅ Payment routes loaded")
except ImportError as e:
    print(f"⚠️  Payment routes error: {e}")

try:
    from routes.research import research_bp
    app.register_blueprint(research_bp)
except ImportError:
    print("⚠️  Research routes not found")

try:
    from routes.knowledge import knowledge_bp
    app.register_blueprint(knowledge_bp)
except ImportError:
    print("⚠️  Knowledge routes not found")

try:
    from routes.scraper import scraper_bp
    app.register_blueprint(scraper_bp)
except ImportError:
    print("⚠️  Scraper routes not found")

try:
    from routes.manual_ingest import manual_bp
    app.register_blueprint(manual_bp)
except ImportError:
    print("⚠️  Manual ingest routes not found")

try:
    from routes.discord import discord_bp
    app.register_blueprint(discord_bp)
except ImportError:
    print("⚠️  Discord routes not found")

# Register core blueprints
app.register_blueprint(health_bp)
app.register_blueprint(agents_bp)
app.register_blueprint(cid_bp)
app.register_blueprint(donations_bp)
app.register_blueprint(claims_bp)
app.register_blueprint(registry_bp)

if __name__ == "__main__":
    print("=" * 60)
    print("🌙 Midnight Infrastructure - Airdrop Agent System")
    print("=" * 60)
    print("🌐 URL: http://localhost:5002")
    print("🤖 Agents: Lookup, Eligibility, Claim")
    print("💰 Wallet: addr1q9np4m2eg4xtr8...")
    print("=" * 60)
    print()
    app.run(host='0.0.0.0', port=5002, debug=False)
