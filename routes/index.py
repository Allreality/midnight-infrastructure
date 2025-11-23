from flask import Blueprint, send_from_directory

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    """Serve the main index page"""
    return send_from_directory('static', 'index.html')

@index_bp.route('/knowledge')
def knowledge():
    """Serve the knowledge base interface"""
    return send_from_directory('static', 'knowledge.html')

@index_bp.route('/claims')
def claims():
    """Serve the claims interface"""
    return send_from_directory('static', 'claims.html')

@index_bp.route('/landing')
def landing():
    """Serve the landing page"""
    return send_from_directory('static', 'landing.html')
