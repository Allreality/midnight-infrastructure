"""
Midnight Knowledge Base Connector for NIST Agents
Connects agents to the 136 compliance documents
"""
import os
import glob
import json

class MidnightKnowledgeBase:
    def __init__(self, kb_path="/mnt/c/projects/midnight-infrastructure/knowledge-base"):
        self.kb_path = kb_path
        
    def search(self, query):
        """Search all documents for a term"""
        results = []
        for filepath in glob.glob(f"{self.kb_path}/**/*.md", recursive=True):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        results.append({
                            "file": os.path.basename(filepath),
                            "path": filepath,
                            "category": filepath.split('/')[1] if '/' in filepath else "root",
                            "preview": content[:300]
                        })
            except:
                pass
        return results
    
    def get_categories(self):
        """Get all categories"""
        categories = []
        for cat_path in glob.glob(f"{self.kb_path}/*/"):
            cat_name = os.path.basename(cat_path.rstrip('/'))
            doc_count = len(list(glob.glob(f"{cat_path}*.md")))
            if doc_count > 0:
                categories.append({"name": cat_name, "count": doc_count})
        return categories
    
    def get_document(self, filepath):
        """Read full document"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def find_nist_docs(self):
        """Find all NIST-related documents"""
        return self.search("NIST")

# Example usage
if __name__ == "__main__":
    kb = MidnightKnowledgeBase()
    
    print("📚 Knowledge Base Stats:")
    cats = kb.get_categories()
    print(f"  Categories: {len(cats)}")
    print(f"  Total docs: {sum(c['count'] for c in cats)}")
    
    print("\n🔍 Searching for 'NIST'...")
    results = kb.find_nist_docs()
    print(f"  Found {len(results)} documents")
    for r in results[:5]:
        print(f"  - {r['file']} ({r['category']})")
