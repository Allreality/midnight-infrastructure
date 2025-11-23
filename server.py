from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import glob

app = Flask(__name__)
CORS(app)

KB_PATH = "knowledge-base"

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "midnight-compliance"}), 200

@app.route('/')
def root():
    return send_from_directory('static', 'landing.html')

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

@app.route('/api/knowledge/stats')
def kb_stats():
    """Get knowledge base statistics"""
    total_docs = len(list(glob.glob(f"{KB_PATH}/**/*.md", recursive=True)))
    total_size = sum(os.path.getsize(f) for f in glob.glob(f"{KB_PATH}/**/*.md", recursive=True))
    return jsonify({
        "total_documents": total_docs,
        "total_size_mb": round(total_size / (1024*1024), 2)
    }), 200

@app.route('/api/knowledge/categories')
def kb_categories():
    """Get all categories and document counts"""
    categories = []
    for cat_path in glob.glob(f"{KB_PATH}/*/"):
        cat_name = os.path.basename(cat_path.rstrip('/'))
        doc_count = len(list(glob.glob(f"{cat_path}*.md")))
        if doc_count > 0:
            categories.append({
                "name": cat_name,
                "document_count": doc_count
            })
    return jsonify({"categories": sorted(categories, key=lambda x: x['document_count'], reverse=True)}), 200

@app.route('/api/knowledge/search', methods=['POST'])
def kb_search():
    """Search knowledge base"""
    data = request.get_json()
    query = data.get('query', '').lower()
    results = []
    
    for filepath in glob.glob(f"{KB_PATH}/**/*.md", recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if query in content.lower():
                    preview = content[:200] + "..." if len(content) > 200 else content
                    results.append({
                        "file": os.path.basename(filepath),
                        "path": filepath,
                        "category": filepath.split('/')[1] if '/' in filepath else "root",
                        "preview": preview
                    })
        except:
            pass
    
    return jsonify({"results": results[:50], "results_count": len(results)}), 200

@app.route('/api/knowledge/document', methods=['POST'])
def kb_document():
    """Get full document content"""
    data = request.get_json()
    filepath = data.get('filepath', '')
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content, "filepath": filepath}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🌙 Midnight Compliance API starting on port {port}")
    print(f"📚 Knowledge base: {KB_PATH} ({len(list(glob.glob(f'{KB_PATH}/**/*.md', recursive=True)))} documents)")
    app.run(host='0.0.0.0', port=port, debug=False)
@app.route('/api/knowledge/advanced_search', methods=['POST'])
def kb_advanced_search():
    """Advanced search with filters"""
    data = request.get_json()
    query = data.get('query', '').lower()
    category = data.get('category', None)
    limit = data.get('limit', 50)
    
    results = []
    search_path = f"{KB_PATH}/{category}/**/*.md" if category else f"{KB_PATH}/**/*.md"
    
    for filepath in glob.glob(search_path, recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if query in content.lower():
                    # Count occurrences
                    count = content.lower().count(query)
                    results.append({
                        "file": os.path.basename(filepath),
                        "path": filepath,
                        "category": filepath.split('/')[1] if '/' in filepath else "root",
                        "occurrences": count,
                        "preview": content[:300]
                    })
        except:
            pass
    
    # Sort by relevance (occurrences)
    results.sort(key=lambda x: x['occurrences'], reverse=True)
    
    return jsonify({
        "results": results[:limit],
        "total_found": len(results),
        "query": query
    }), 200
