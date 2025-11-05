from flask import Blueprint, jsonify
from datetime import datetime

bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'midnight-infrastructure',
        'timestamp': datetime.now().isoformat()
    })

@bp.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'ok',
        'service': 'midnight-infrastructure',
        'timestamp': datetime.now().isoformat()
    })