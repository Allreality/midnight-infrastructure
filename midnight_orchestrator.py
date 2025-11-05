# midnight_orchestrator.py

import json
from agent_defs import AGENT_CONFIGS # Assume a config file holds the 20 roles
from agent_template import BaseAgent, ResearchCuratorAgent, DocumentationWriterAgent # Import your specialized classes

# --- Agent Initialization ---
def initialize_agents(config_data: dict) -> dict:
    """Initializes all 20 agents based on configuration."""
    agent_pool = {}
    for agent_id, details in config_data.items():
        # Dynamically create the agent instance based on its specialized class
        # This assumes you have specialized classes (e.g., ResearchCuratorAgent) inheriting BaseAgent
        AgentClass = globals().get(details['class'], BaseAgent) 
        
        # BaseAgent constructor handles registration via the x402 Mixin
        try:
            agent = AgentClass(
                agent_id=agent_id,
                role=details['role'],
                wallet=details['wallet'],
                api_key=details['api_key']
            )
            agent_pool[agent_id] = agent
        except ConnectionError as e:
            print(f"CRITICAL: Failed to initialize {agent_id}. Error: {e}")
            # Decide: stop the system or log and continue without this agent
            continue
            
    # Assign the core roles for easy access in the loop
    return {
        "pool": agent_pool,
        "curator": agent_pool['research_curator_id'],
        "writer": agent_pool['doc_writer_id'],
        "maintainer": agent_pool['kb_maintainer_id']
    }

# Load the configuration (You will create this file: agent_defs.json or .py)
with open('agent_configs.json', 'r') as f:
    ALL_AGENT_CONFIGS = json.load(f)

AGENTS = initialize_agents(ALL_AGENT_CONFIGS)

def run_knowledge_workflow(initial_task: dict, agent_data: dict) -> dict:
    """
    Manages the 6-step knowledge generation workflow using the agent crew.
    """
    curator = agent_data['curator']
    writer = agent_data['writer']
    maintainer = agent_data['maintainer']
    agent_pool = agent_data['pool']
    
    # --- Step 1 & 2: Task Creation & Approval (Assumed complete via Dashboard) ---
    print(f"\n[ORCHESTRATOR] Starting workflow for task: {initial_task['topic']}")

    # --- Step 3: Research Phase (Delegation to the Crew) ---
    print(f"\n[ORCHESTRATOR] STEP 3: Delegating research via Research Curator...")
    
    # The Curator's run_task method will contain the complex logic:
    # 1. Decompose 'topic' into 5-10 smaller, specific research tasks.
    # 2. Iterate through the AGENTS pool and select the best specialized agent for each sub-task.
    # 3. For each sub-task, the Curator sends the work to the specialized agent's run_task.
    # 4. CRITICAL: The specialized agent, during its run_task, may call pay_for_service() 
    #    (layered on the x402 mixin) to buy premium data access.
    # 5. The Curator gathers all 5-10 sub-results into a single raw research packet.
    
    raw_research_packet = curator.run_task(initial_task, agent_pool)
    
    if not raw_research_packet or raw_research_packet.get("status") == "failed":
        print("[ORCHESTRATOR] Research phase failed. Aborting workflow.")
        return {"status": "failed", "error": "Research incomplete."}
    
    # --- Step 4: Documentation Synthesis ---
    print("\n[ORCHESTRATOR] STEP 4: Documentation Writer synthesizing report...")
    
    final_document = writer.run_task(raw_research_packet)
    
    if final_document:
        # Document Writer must track the final output CID
        writer.track_cid_provenance(final_document.get("final_cid"))
        
        # --- Step 5: Organization and Indexing ---
        print("\n[ORCHESTRATOR] STEP 5: KB Maintainer indexing content...")
        
        kb_index_update = maintainer.run_task(final_document)
        
        # --- Step 6: Publication & Final Accounting ---
        print("\n[ORCHESTRATOR] STEP 6: Publication and Final Accounting.")
        
        # The Treasury Agent (a specialized worker) may get called here to log earnings
        # if the service was for a paying client.
        
        return {"status": "success", "final_document_cid": final_document.get("final_cid")}
        
    return {"status": "failed", "error": "Documentation phase failed."}
