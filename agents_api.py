from flask import Blueprint, jsonify, request
import os
import sys

# Add agents to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

agents_bp = Blueprint('agents', __name__, url_prefix='/api/agents')

@agents_bp.route('/status', methods=['GET'])
def get_agent_status():
    """Get status of all agents"""
    
    status = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "agents": {}
    }
    
    # Check each agent
    agents_config = {
        "midnight_kb_connector": {
            "name": "Knowledge Base Connector",
            "description": "Searches 151 compliance documents",
            "requires": []
        },
        "claimAgent": {
            "name": "Claim Logger",
            "description": "Logs blockchain claim attempts",
            "requires": []
        },
        "documentationAgent": {
            "name": "Documentation Generator",
            "description": "Generates compliance docs using Claude",
            "requires": ["ANTHROPIC_API_KEY"]
        },
        "discordBot": {
            "name": "Discord Monitor",
            "description": "Monitors Midnight Discord for announcements",
            "requires": ["DISCORD_TOKEN"]
        },
        "webScraper": {
            "name": "Web Scraper",
            "description": "Scrapes official Midnight sources",
            "requires": ["requests"]
        },
        "research_curator_agent": {
            "name": "Research Curator",
            "description": "Orchestrates research delegation",
            "requires": []
        }
    }
    
    for agent_id, config in agents_config.items():
        agent_status = {
            "name": config["name"],
            "description": config["description"],
            "status": "unknown",
            "missing_requirements": []
        }
        
        # Check requirements
        all_requirements_met = True
        for req in config["requires"]:
            if req.isupper():  # Environment variable
                if not os.environ.get(req):
                    agent_status["missing_requirements"].append(req)
                    all_requirements_met = False
            else:  # Python module
                try:
                    __import__(req)
                except ImportError:
                    agent_status["missing_requirements"].append(req)
                    all_requirements_met = False
        
        # Try to import agent
        try:
            __import__(agent_id)
            if all_requirements_met:
                agent_status["status"] = "ready"
            else:
                agent_status["status"] = "missing_dependencies"
        except Exception as e:
            agent_status["status"] = "error"
            agent_status["error"] = str(e)
        
        status["agents"][agent_id] = agent_status
    
    return jsonify(status), 200

@agents_bp.route('/search', methods=['GET'])
def search_knowledge_base():
    """Search knowledge base using midnight_kb_connector"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400
    
    try:
        from midnight_kb_connector import MidnightKnowledgeBase
        kb = MidnightKnowledgeBase()
        results = kb.search(query)
        
        return jsonify({
            "query": query,
            "results_count": len(results),
            "results": results[:20]  # Limit to 20 results
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@agents_bp.route('/generate-doc', methods=['POST'])
def generate_documentation():
    """Generate compliance documentation using documentationAgent"""
    data = request.json
    industry = data.get('industry')
    framework = data.get('framework')
    
    if not industry or not framework:
        return jsonify({"error": "Both 'industry' and 'framework' required"}), 400
    
    try:
        from documentationAgent import DocumentationAgent
        agent = DocumentationAgent()
        result = agent.generate_industry_guide(industry, framework)
        
        return jsonify({
            "industry": industry,
            "framework": framework,
            "documentation": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500