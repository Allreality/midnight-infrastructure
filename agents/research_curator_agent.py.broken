# agents/research_curator_agent.py

# agents/research_curator_agent.py

from agent_template import BaseAgent
from typing import Dict, Any, List
import hashlib # Added import for the helper function

class ResearchCuratorAgent(BaseAgent):
    # ... (Other methods, including __init__, are defined here) ...

    def decompose_task(self, topic: str) -> List[Dict[str, Any]]:
        # ... (Decomposition logic is fine where it is) ...
        # ...

    # --- MUST BE INDENTED 4 SPACES TO BE INSIDE THE CLASS ---
    def run_task(self, initial_task: dict, agent_pool: dict) -> Dict[str, Any]:
        # ... (Delegation logic) ...

    # --- MUST BE INDENTED 4 SPACES TO BE INSIDE THE CLASS ---
    def synthesize_results(self, research_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        # ... (Synthesis and provenance logic) ...

    # --- MUST BE INDENTED 4 SPACES TO BE INSIDE THE CLASS ---
    def generate_cid(self, data: str) -> str:
        # ... (Helper function logic) ...
    
    # ... (Other methods, including __init__, are defined here) ...

    def decompose_task(self, topic: str) -> List[Dict[str, Any]]:
        """
        Uses an internal LLM call (e.g., Claude) to break down the task.
        Example output structure: [{'name': 'Analyze ZKP implementation', 'keywords': ['ZK', 'privacy', 'crypto']}, ...]
        """
        print(f"Curator is decomposing task: {topic}...")
        
        # --- Placeholder for the LLM Decomposition Call ---
        # In a real system, this would call Claude/Gemini with a prompt
        # instructing it to generate a structured JSON list of sub-tasks and keywords.
        
        # --- Hardcoded Example Output for Structure ---
        return [
            {"name": "Midnight Smart Contract Patterns", "keywords": ["Midnight", "smart contract", "dev", "solidity"]},
            {"name": "HIPAA Compliance Requirements", "keywords": ["HIPAA", "health", "compliance", "regulatory"]},
            {"name": "Competitive ZK-Proof Analysis", "keywords": ["ZK", "crypto", "security", "competitor"]},
            {"name": "Labor Market Data Aggregation", "keywords": ["labor", "market", "data", "finance"]},
            {"name": "Regulatory Changes in EU", "keywords": ["regulatory", "policy", "EU", "reg_policy"]}
        ]
        
def run_task(self, initial_task: dict, agent_pool: dict) -> Dict[str, Any]:
        """
        Manages micro-delegation: breaks the task, selects the specialized worker, 
        sends the sub-task, and awaits the result.
        """
        
        # 1. Decomposition
        sub_tasks = self.decompose_task(initial_task['topic'])
        research_results = []
        
        # Pre-filter pool for easy selection (you would pre-load this lookup table)
        AGENT_ROLES_LOOKUP = {
            "Midnight": agent_pool["dev_smart_contract_02"],
            "HIPAA": agent_pool["health_hipaa_05"],
            "regulatory": agent_pool["reg_policy_15"],
            "ZK": agent_pool["dev_zkp_analyzer_03"],
            "labor": agent_pool["market_data_12"],
            "security": agent_pool["security_auditor_14"]
            # ... 14 more explicit keyword-to-agent mappings ...
        }
        
        # 2. Iterative Delegation
        for sub_task in sub_tasks:
            
            # --- AGENT SELECTION HEURISTIC ---
            target_agent = None
            
            # Find the best match by iterating through the sub-task keywords
            for keyword in sub_task['keywords']:
                if keyword in AGENT_ROLES_LOOKUP:
                    target_agent = AGENT_ROLES_LOOKUP[keyword]
                    break  # Found the most specialized agent, stop searching keywords

            # If no specialized agent is found, default to a general one (if available)
            if target_agent is None:
                print(f"  > No specialized agent found for: {sub_task['name']}. Skipping.")
                continue # Or delegate to a 'General Researcher'
                
            print(f"  > Delegating '{sub_task['name']}' to {target_agent.role} ({target_agent.agent_id})...")

            # 3. Execution (The call runs the worker agent's run_task method)
            # The worker agent may internally call self.pay_for_service() here.
            result = target_agent.run_task(sub_task) 
            
            if result and result.get("status") == "complete":
                research_results.append(result)
            else:
                print(f"  > Delegation to {target_agent.agent_id} failed or returned empty.")

        # 4. Synthesis
        return self.synthesize_results(research_results)
    
def synthesize_results(self, research_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Gathers raw results from the crew, synthesizes them into a coherent packet,
        and tracks the final output CID.
        """
        if not research_results:
            return {"status": "failed", "error": "No successful research results gathered."}

        # --- Placeholder for LLM Synthesis Call ---
        # Call Claude/Gemini to write a comprehensive summary based on all research_results.
        synthesized_text = "Synthesized Report:\n"
        for result in research_results:
            synthesized_text += f"--- Source ({result.get('source_agent_id', 'Unknown')}) ---\n"
            synthesized_text += result.get('raw_output', '[Data not available]') + "\n\n"
        
        final_cid = self.generate_cid(synthesized_text) # Assumed utility function

        # Track the synthesized packet's provenance before passing it on
        self.track_cid_provenance(final_cid) 
        
        print(f"\n[Curator] Synthesis complete. CID tracked: {final_cid}")
        
        return {
            "status": "complete",
            "topic": "Synthesized Research Packet",
            "content": synthesized_text,
            "final_cid": final_cid
        }

    # Assumed helper method (implementation not shown)
def generate_cid(self, data: str) -> str:
        """Stub for actual IPFS CID generation."""
        import hashlib
        return "cidv1_" + hashlib.sha256(data.encode()).hexdigest()[:16]
    
    # The worker agent may internally call self.pay_for_service() here.
result = target_agent.run_task(sub_task)