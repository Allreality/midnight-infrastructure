from flask import Flask
from routes.health import health_bp
from routes.claims_stats import claims_stats_bp
from routes.claim_initial_state import claim_state_bp
from routes.claims_log import claims_log_bp  # ← this is the agentic POST route
from routes.claims_verify import claims_verify_bp
from routes.claims_eligibility import claims_eligibility_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(health_bp)
    app.register_blueprint(claims_stats_bp)
    app.register_blueprint(claim_state_bp)
    app.register_blueprint(claims_log_bp)  # ← ✅ register this too
    app.register_blueprint(claims_verify_bp)
    app.register_blueprint(claims_eligibility_bp)


    return app