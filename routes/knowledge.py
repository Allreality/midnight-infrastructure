# routes/knowledge.py
from flask import Blueprint, jsonify, request
import os
import json
from pathlib import Path

knowledge_bp = Blueprint("knowledge", __name__, url_prefix="/api/knowledge")

KNOWLEDGE_BASE = "knowledge-base"

@knowledge_bp.route("/search", methods=["POST"])
def search_knowledge():
    """Search knowledge base by keywords"""
    data = request.json
    query = data.get("query", "").lower()
    
    if not query:
        return jsonify({"error": "Query required"}), 400
    
    results = []
    
    # Search through all markdown files
    for root, dirs, files in os.walk(KNOWLEDGE_BASE):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query in content.lower():
                            results.append({
                                "file": file,
                                "path": filepath,
                                "category": Path(root).name,
                                "preview": content[:200] + "..."
                            })
                except Exception as e:
                    continue
    
    return jsonify({
        "query": query,
        "results_count": len(results),
        "results": results
    }), 200

@knowledge_bp.route("/categories", methods=["GET"])
def get_categories():
    """Get all knowledge categories"""
    categories = []
    
    for item in os.listdir(KNOWLEDGE_BASE):
        item_path = os.path.join(KNOWLEDGE_BASE, item)
        if os.path.isdir(item_path):
            file_count = sum(1 for f in Path(item_path).rglob('*.md'))
            categories.append({
                "name": item,
                "document_count": file_count
            })
    
    return jsonify({"categories": categories}), 200

@knowledge_bp.route("/documents/<category>", methods=["GET"])
def get_documents_by_category(category):
    """Get all documents in a category"""
    category_path = os.path.join(KNOWLEDGE_BASE, category)
    
    if not os.path.exists(category_path):
        return jsonify({"error": "Category not found"}), 404
    
    documents = []
    for file in Path(category_path).rglob('*.md'):
        documents.append({
            "name": file.name,
            "path": str(file),
            "size": file.stat().st_size
        })
    
    return jsonify({
        "category": category,
        "documents": documents
    }), 200

@knowledge_bp.route("/document", methods=["POST"])
def get_document_content():
    """Get content of a specific document"""
    data = request.json
    filepath = data.get("filepath")
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            "filepath": filepath,
            "content": content
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@knowledge_bp.route("/stats", methods=["GET"])
def get_stats():
    """Get knowledge base statistics"""
    total_files = sum(1 for _ in Path(KNOWLEDGE_BASE).rglob('*.md'))
    total_size = sum(f.stat().st_size for f in Path(KNOWLEDGE_BASE).rglob('*.md'))
    
    return jsonify({
        "total_documents": total_files,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / 1024 / 1024, 2)
    }), 200
