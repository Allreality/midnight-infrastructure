# Inside ResearchCuratorAgent's run_task method (a specialized BaseAgent)

def run_task(self, task_data: dict, agent_pool: dict) -> dict:
    """Decomposes task and delegates to specialized worker agents."""
    
    # 1. Decomposition (e.g., using an LLM call to break down the task)
    sub_tasks = self.decompose_task(task_data['topic']) 
    
    research_results = []
    for sub_task in sub_tasks:
        
        # 2. Selection (Simple heuristic for demonstration)
        # In reality, this would be a complex lookup based on agent capabilities.
        if "policy" in sub_task['keywords']:
            target_agent = agent_pool['cardano_policy_agent_id']
        elif "ZK" in sub_task['keywords']:
            target_agent = agent_pool['zk_proof_analyzer_id']
        else:
            target_agent = agent_pool['general_research_agent_id']
        
        # 3. Delegation
        print(f"  > Delegating '{sub_task['name']}' to {target_agent.role}...")
        
        # This call executes the specialized agent's logic, including its potential
        # internal call to self.pay_for_service() via the x402 mixin.
        result = target_agent.run_task(sub_task)
        
        research_results.append(result)
        
    # 4. Synthesis
    return self.synthesize_results(research_results) # Use an internal LLM call to summarize