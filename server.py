from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "midnight-compliance"}), 200

@app.route('/')
def root():
    return jsonify({"message": "Midnight Compliance Infrastructure", "status": "running"}), 200

@app.route('/api/payment/pricing')
def pricing():
    return jsonify({
        "treasury_address": os.getenv("TREASURY_ADDRESS", ""),
        "tiers": {
            "free": {"cost_ada": 0},
            "professional": {"cost_ada": 500},
            "enterprise": {"cost_ada": 5000}
        }
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
