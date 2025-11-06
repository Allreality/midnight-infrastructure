"""
Knowledge Base API Routes
Lazy loading for performance
"""
from flask import Blueprint, jsonify, request
import os
from pathlib import Path

knowledge_bp = Blueprint("knowledge", __name__, url_prefix="/api/knowledge")

# DON'T load all files on import - load on demand
KB_PATH = "knowledge-base"

@knowledge_bp.route("/stats", methods=["GET"])
def get_stats():
    """Get knowledge base statistics"""
    try:
        total_docs = 0
        total_size = 0
        categories = {}
        
        for category in os.listdir(KB_PATH):
            cat_path = os.path.join(KB_PATH, category)
            if os.path.isdir(cat_path):
                files = list(Path(cat_path).rglob('*.md'))
                doc_count = len(files)
                total_docs += doc_count
                
                # Calculate size
                cat_size = sum(f.stat().st_size for f in files)
                total_size += cat_size
                
                categories[category] = {
                    "documents": doc_count,
                    "size_bytes": cat_size
                }
        
        return jsonify({
            "total_documents": total_docs,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "categories": len(categories),
            "category_breakdown": categories
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@knowledge_bp.route("/search", methods=["GET"])
def search():
    """Search knowledge base"""
    query = request.args.get('q', '')
    # Implement search logic
    return jsonify({"query": query, "results": []}), 200

@knowledge_bp.route("/categories", methods=["GET"])
def get_categories():
    """List all categories"""
    try:
        categories = []
        for category in os.listdir(KB_PATH):
            cat_path = os.path.join(KB_PATH, category)
            if os.path.isdir(cat_path):
                categories.append(category)
        
        return jsonify({"categories": sorted(categories)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
