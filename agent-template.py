#!/usr/bin/env python3
"""
Midnight Infrastructure - AI Agent Template
Version 1.0 - Modular Agent Framework

This template provides a base structure for quickly spinning up specialized AI agents
for research, monitoring, analysis, and automation tasks.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from flask import Flask, render_template_string, jsonify, request

# Original:
# class BaseAgent(ABC):

# Modified to include payment capabilities:
class BaseAgent(ABC, X402PaymentMixin):
    """
    Base class for all AI agents in the Midnight Infrastructure ecosystem.
    Inherit from this class to create specialized agents.
    """
    def __init__(self, agent_id: str, role: str, wallet: str, api_key: str):
        # Initialize the X402 Payment Mixin first
        X402PaymentMixin.__init__(self, agent_id, api_key) 
        
        # Initialize the BaseAgent properties
        self.agent_id = agent_id
        self.role = role
        self.wallet = wallet
        self.status = "INIT"
        
        # Agents MUST register themselves on startup
        if not self.register_agent(role, wallet, "initial_cid_placeholder"):
            raise ConnectionError(f"Failed to register agent {agent_id} with Midnight API.")
            
        print(f"Agent {self.agent_id} ({self.role}) successfully registered.")

    @abstractmethod
    def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Abstract method that specialized agents must implement to process work."""
        pass
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the agent with configuration.
        
        Args:
            config: Dictionary containing agent configuration
                - name: Agent name
                - version: Agent version
                - description: What this agent does
                - port: Port to run on
                - capabilities: List of agent capabilities
                - data_sources: Where agent gets data from
        """
        self.config = config
        self.name = config.get('name', 'Unnamed Agent')
        self.version = config.get('version', '1.0')
        self.description = config.get('description', 'AI Agent')
        self.port = config.get('port', 5000)
        self.capabilities = config.get('capabilities', [])
        self.data_sources = config.get('data_sources', [])
        self.status = 'initialized'
        self.startup_time = datetime.now()
        
        # Flask app for web interface
        self.app = Flask(self.name)
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup standard routes for all agents"""
        
        @self.app.route('/')
        def index():
            return self._render_dashboard()
        
        @self.app.route('/health')
        def health():
            return jsonify(self.get_health_status())
        
        @self.app.route('/api/info')
        def info():
            return jsonify(self.get_agent_info())
        
        @self.app.route('/api/capabilities')
        def capabilities():
            return jsonify(self.get_capabilities())
        
        @self.app.route('/api/execute', methods=['POST'])
        def execute():
            task = request.json
            result = self.execute_task(task)
            return jsonify(result)
    
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific task. Override this in subclasses.
        
        Args:
            task: Dictionary containing task parameters
        
        Returns:
            Dictionary with task results
        """
        pass
    
    @abstractmethod
    def _render_dashboard(self) -> str:
        """
        Render the agent's web dashboard. Override this in subclasses.
        
        Returns:
            HTML string for the dashboard
        """
        pass
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health status"""
        return {
            'status': 'healthy',
            'agent': self.name,
            'version': self.version,
            'port': self.port,
            'uptime': str(datetime.now() - self.startup_time),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get detailed agent information"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'port': self.port,
            'status': self.status,
            'startup_time': self.startup_time.isoformat(),
            'capabilities': self.capabilities,
            'data_sources': self.data_sources,
            'config': self.config
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            'agent': self.name,
            'capabilities': self.capabilities,
            'timestamp': datetime.now().isoformat()
        }
    
    def log(self, message: str, level: str = 'INFO'):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{self.name}] [{level}] {message}")
    
    def run(self, host: str = '0.0.0.0', debug: bool = True):
        """
        Start the agent's web server
        
        Args:
            host: Host to bind to
            debug: Enable debug mode
        """
        self.status = 'running'
        self.log(f"Starting {self.name} v{self.version} on port {self.port}")
        self.log(f"Description: {self.description}")
        self.log(f"Capabilities: {', '.join(self.capabilities)}")
        
        self.app.run(
            host=host,
            port=self.port,
            debug=debug,
            use_reloader=False
        )


class ResearchAgent(BaseAgent):
    """
    Specialized agent for research tasks like:
    - Paper tracking
    - Citation analysis
    - Research trend identification
    - Gap discovery
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.research_domains = config.get('research_domains', [])
        self.papers_tracked = 0
        self.citations_analyzed = 0
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research-related tasks"""
        task_type = task.get('type', 'unknown')
        
        if task_type == 'search_papers':
            return self._search_papers(task.get('query', ''))
        elif task_type == 'analyze_citations':
            return self._analyze_citations(task.get('paper_id', ''))
        elif task_type == 'identify_gaps':
            return self._identify_gaps(task.get('domain', ''))
        else:
            return {'error': f'Unknown task type: {task_type}'}
    
    def _search_papers(self, query: str) -> Dict[str, Any]:
        """Search for research papers"""
        self.log(f"Searching papers for: {query}")
        # Implementation would go here
        return {
            'task': 'search_papers',
            'query': query,
            'results': [],
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_citations(self, paper_id: str) -> Dict[str, Any]:
        """Analyze paper citations"""
        self.log(f"Analyzing citations for paper: {paper_id}")
        # Implementation would go here
        return {
            'task': 'analyze_citations',
            'paper_id': paper_id,
            'citations': [],
            'timestamp': datetime.now().isoformat()
        }
    
    def _identify_gaps(self, domain: str) -> Dict[str, Any]:
        """Identify research gaps in a domain"""
        self.log(f"Identifying gaps in domain: {domain}")
        # Implementation would go here
        return {
            'task': 'identify_gaps',
            'domain': domain,
            'gaps': [],
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_dashboard(self) -> str:
        """Render research agent dashboard"""
        return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ name }} - Research Agent</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 20px; }
        .header { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 2em; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
        .stat-card h3 { margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.7; }
        .stat-card .value { font-size: 2em; font-weight: bold; }
        .section { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 {{ name }}</h1>
        <p>{{ description }}</p>
    </div>
    <div class="stats">
        <div class="stat-card">
            <h3>Papers Tracked</h3>
            <div class="value">{{ papers_tracked }}</div>
        </div>
        <div class="stat-card">
            <h3>Citations Analyzed</h3>
            <div class="value">{{ citations_analyzed }}</div>
        </div>
        <div class="stat-card">
            <h3>Research Domains</h3>
            <div class="value">{{ domain_count }}</div>
        </div>
    </div>
    <div class="section">
        <h2>Research Domains</h2>
        <ul>
        {% for domain in domains %}
            <li>{{ domain }}</li>
        {% endfor %}
        </ul>
    </div>
    <div class="section">
        <h2>Capabilities</h2>
        <ul>
        {% for cap in capabilities %}
            <li>{{ cap }}</li>
        {% endfor %}
        </ul>
    </div>
</body>
</html>
        """, 
            name=self.name,
            description=self.description,
            papers_tracked=self.papers_tracked,
            citations_analyzed=self.citations_analyzed,
            domain_count=len(self.research_domains),
            domains=self.research_domains,
            capabilities=self.capabilities
        )


class MonitoringAgent(BaseAgent):
    """
    Specialized agent for monitoring tasks like:
    - Implementation tracking
    - Network monitoring
    - Performance metrics
    - Alert generation
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.monitored_items = config.get('monitored_items', [])
        self.alerts = []
        self.metrics = {}
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute monitoring tasks"""
        task_type = task.get('type', 'unknown')
        
        if task_type == 'check_status':
            return self._check_status(task.get('target', ''))
        elif task_type == 'generate_alert':
            return self._generate_alert(task.get('alert', {}))
        elif task_type == 'collect_metrics':
            return self._collect_metrics()
        else:
            return {'error': f'Unknown task type: {task_type}'}
    
    def _check_status(self, target: str) -> Dict[str, Any]:
        """Check status of monitored target"""
        self.log(f"Checking status of: {target}")
        return {
            'task': 'check_status',
            'target': target,
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_alert(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an alert"""
        self.alerts.append(alert)
        self.log(f"Alert generated: {alert.get('message', '')}", 'WARNING')
        return {
            'task': 'generate_alert',
            'alert': alert,
            'timestamp': datetime.now().isoformat()
        }
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect current metrics"""
        self.log("Collecting metrics")
        return {
            'task': 'collect_metrics',
            'metrics': self.metrics,
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_dashboard(self) -> str:
        """Render monitoring agent dashboard"""
        return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ name }} - Monitoring Agent</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 20px; }
        .header { background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 2em; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
        .stat-card h3 { margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.7; }
        .stat-card .value { font-size: 2em; font-weight: bold; }
        .section { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .alert { background: rgba(239, 68, 68, 0.2); border-left: 4px solid #ef4444; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {{ name }}</h1>
        <p>{{ description }}</p>
    </div>
    <div class="stats">
        <div class="stat-card">
            <h3>Monitored Items</h3>
            <div class="value">{{ item_count }}</div>
        </div>
        <div class="stat-card">
            <h3>Active Alerts</h3>
            <div class="value">{{ alert_count }}</div>
        </div>
        <div class="stat-card">
            <h3>Uptime</h3>
            <div class="value">{{ uptime }}</div>
        </div>
    </div>
    <div class="section">
        <h2>Monitored Items</h2>
        <ul>
        {% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    </div>
    {% if alerts %}
    <div class="section">
        <h2>Recent Alerts</h2>
        {% for alert in alerts %}
        <div class="alert">{{ alert }}</div>
        {% endfor %}
    </div>
    {% endif %}
</body>
</html>
        """, 
            name=self.name,
            description=self.description,
            item_count=len(self.monitored_items),
            alert_count=len(self.alerts),
            uptime=str(datetime.now() - self.startup_time),
            items=self.monitored_items,
            alerts=self.alerts
        )


class AnalyticsAgent(BaseAgent):
    """
    Specialized agent for analytics tasks like:
    - Data analysis
    - Trend identification
    - Report generation
    - Visualization
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.datasets = config.get('datasets', [])
        self.reports_generated = 0
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analytics tasks"""
        task_type = task.get('type', 'unknown')
        
        if task_type == 'analyze_data':
            return self._analyze_data(task.get('dataset', ''))
        elif task_type == 'generate_report':
            return self._generate_report(task.get('params', {}))
        elif task_type == 'identify_trends':
            return self._identify_trends(task.get('timeframe', ''))
        else:
            return {'error': f'Unknown task type: {task_type}'}
    
    def _analyze_data(self, dataset: str) -> Dict[str, Any]:
        """Analyze a dataset"""
        self.log(f"Analyzing dataset: {dataset}")
        return {
            'task': 'analyze_data',
            'dataset': dataset,
            'analysis': {},
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an analytics report"""
        self.log("Generating report")
        self.reports_generated += 1
        return {
            'task': 'generate_report',
            'report': {},
            'timestamp': datetime.now().isoformat()
        }
    
    def _identify_trends(self, timeframe: str) -> Dict[str, Any]:
        """Identify trends in data"""
        self.log(f"Identifying trends for timeframe: {timeframe}")
        return {
            'task': 'identify_trends',
            'timeframe': timeframe,
            'trends': [],
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_dashboard(self) -> str:
        """Render analytics agent dashboard"""
        return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ name }} - Analytics Agent</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 20px; }
        .header { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 2em; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
        .stat-card h3 { margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.7; }
        .stat-card .value { font-size: 2em; font-weight: bold; }
        .section { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 {{ name }}</h1>
        <p>{{ description }}</p>
    </div>
    <div class="stats">
        <div class="stat-card">
            <h3>Datasets</h3>
            <div class="value">{{ dataset_count }}</div>
        </div>
        <div class="stat-card">
            <h3>Reports Generated</h3>
            <div class="value">{{ reports_generated }}</div>
        </div>
        <div class="stat-card">
            <h3>Capabilities</h3>
            <div class="value">{{ capability_count }}</div>
        </div>
    </div>
    <div class="section">
        <h2>Available Datasets</h2>
        <ul>
        {% for dataset in datasets %}
            <li>{{ dataset }}</li>
        {% endfor %}
        </ul>
    </div>
</body>
</html>
        """, 
            name=self.name,
            description=self.description,
            dataset_count=len(self.datasets),
            reports_generated=self.reports_generated,
            capability_count=len(self.capabilities),
            datasets=self.datasets
        )


# Example usage and configuration templates
if __name__ == '__main__':
    print("Midnight Infrastructure - AI Agent Template")
    print("=" * 60)
    print("\nThis is the base template. Create specific agents by:")
    print("1. Importing the agent classes")
    print("2. Creating a configuration")
    print("3. Instantiating and running the agent")
    print("\nSee example_agents.py for practical examples.")