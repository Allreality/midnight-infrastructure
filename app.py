from flask import Flask
from routes.health import health_bp
from routes.claims_stats import claims_stats_bp
from routes.claim_initial_state import claim_state_bp
from routes.claims_log import claims_log_bp
from routes.claims_verify import claims_verify_bp
from routes.claims_eligibility import claims_eligibility_bp
from routes.index import index_bp
from routes.knowledge import knowledge_bp

def create_app():
    app = Flask(__name__)
    
    # Register all blueprints
    app.register_blueprint(index_bp)  # Main pages
    app.register_blueprint(knowledge_bp)  # Knowledge base API ⭐ ADDED
    app.register_blueprint(health_bp)
    app.register_blueprint(claims_stats_bp)
    app.register_blueprint(claim_state_bp)
    app.register_blueprint(claims_log_bp)
    app.register_blueprint(claims_verify_bp)
    app.register_blueprint(claims_eligibility_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🌙 Midnight Infrastructure starting on port 5002...")
    print("📚 Knowledge Base: http://localhost:5002/knowledge")
    print("📋 Claims: http://localhost:5002/claims")
    print("🏠 Landing: http://localhost:5002/landing")
    print("🔍 Knowledge API: http://localhost:5002/api/knowledge/stats")
    app.run(host='0.0.0.0', port=5002, debug=True)
