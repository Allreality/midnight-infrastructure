from flask import Blueprint, jsonify, request
import os
import json

knowledge_bp = Blueprint("knowledge", __name__, url_prefix="/api/knowledge")
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
                doc_count = 0
                size_bytes = 0
                for root, dirs, files in os.walk(cat_path):
                    for file in files:
                        if file.endswith(('.md', '.txt', '.pdf')):
                            doc_count += 1
                            file_path = os.path.join(root, file)
                            size_bytes += os.path.getsize(file_path)
                
                categories[category] = {
                    "documents": doc_count,
                    "size_bytes": size_bytes
                }
                total_docs += doc_count
                total_size += size_bytes
        
        return jsonify({
            "total_documents": total_docs,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "categories": len(categories),
            "category_breakdown": categories
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@knowledge_bp.route("/categories", methods=["GET"])
def get_categories():
    """List all categories with document counts"""
    try:
        categories = {}
        for category in os.listdir(KB_PATH):
            cat_path = os.path.join(KB_PATH, category)
            if os.path.isdir(cat_path):
                doc_count = 0
                size_bytes = 0
                for root, dirs, files in os.walk(cat_path):
                    for file in files:
                        if file.endswith(('.md', '.txt', '.pdf')):
                            doc_count += 1
                            file_path = os.path.join(root, file)
                            size_bytes += os.path.getsize(file_path)
                
                categories[category] = {
                    "name": category,
                    "documents": doc_count,
                    "size_bytes": size_bytes
                }
        
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@knowledge_bp.route("/category/<category_name>", methods=["GET"])
def get_category_documents(category_name):
    """Get all documents in a specific category"""
    try:
        cat_path = os.path.join(KB_PATH, category_name)
        if not os.path.exists(cat_path):
            return jsonify({"error": "Category not found"}), 404
        
        documents = []
        for root, dirs, files in os.walk(cat_path):
            for file in files:
                if file.endswith(('.md', '.txt', '.pdf')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, KB_PATH)
                    size = os.path.getsize(file_path)
                    documents.append({
                        "name": file,
                        "path": rel_path,
                        "size_bytes": size,
                        "category": category_name
                    })
        
        return jsonify({
            "category": category_name,
            "documents": documents,
            "count": len(documents)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@knowledge_bp.route("/search", methods=["GET"])
def search_knowledge():
    """Search knowledge base"""
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    results = []
    try:
        for root, dirs, files in os.walk(KB_PATH):
            for file in files:
                if file.endswith(('.md', '.txt')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if query in content.lower():
                            category = os.path.basename(os.path.dirname(file_path))
                            # Get preview
                            lines = content.split('\n')
                            preview = ' '.join(lines[:3])[:200] + '...'
                            results.append({
                                "file": file,
                                "category": category,
                                "path": os.path.relpath(file_path, KB_PATH),
                                "preview": preview
                            })
        
        return jsonify({"results": results, "results_count": len(results)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@knowledge_bp.route("/document", methods=["POST"])
def get_document():
    """Get full document content"""
    data = request.json
    filepath = data.get('filepath', '')
    
    try:
        full_path = os.path.join(KB_PATH, filepath)
        if not os.path.exists(full_path):
            return jsonify({"error": "Document not found"}), 404
        
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return jsonify({"content": content, "path": filepath}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500