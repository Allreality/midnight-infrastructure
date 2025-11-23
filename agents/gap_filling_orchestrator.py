"""
Gap-Filling Orchestrator
Coordinates AI agents to research and fill compliance gaps
"""
import sys
import os
import json
from datetime import datetime
from typing import List, Dict

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# Verify API key loaded
if not os.environ.get('ANTHROPIC_API_KEY'):
    print("❌ ERROR: ANTHROPIC_API_KEY not found in .env")
    print("Please check your .env file contains: ANTHROPIC_API_KEY=your-key-here")
    sys.exit(1)

sys.path.append(os.path.dirname(__file__))

from midnight_kb_connector import MidnightKnowledgeBase
from documentationAgent import DocumentationAgent

class GapFillingOrchestrator:
    """Orchestrates agents to fill compliance gaps"""
    
    def __init__(self):
        self.kb = MidnightKnowledgeBase()
        self.doc_agent = DocumentationAgent()
        self.results_dir = "knowledge-base/nist-gap-filling/automated-solutions"
        os.makedirs(self.results_dir, exist_ok=True)
        print(f"✅ API Key loaded: {os.environ.get('ANTHROPIC_API_KEY')[:15]}...")
        
    def extract_gaps_from_analysis(self, analysis_file: str) -> List[Dict]:
        """Extract individual gaps from the gap analysis report"""
        # NIST 800-171 has 14 control families
        control_families = [
            {"family": "Access Control (AC)", "priority": "critical"},
            {"family": "Audit and Accountability (AU)", "priority": "high"},
            {"family": "Configuration Management (CM)", "priority": "high"},
            {"family": "Identification and Authentication (IA)", "priority": "critical"},
            {"family": "System and Communications Protection (SC)", "priority": "critical"},
            {"family": "System and Information Integrity (SI)", "priority": "critical"},
            {"family": "Media Protection (MP)", "priority": "medium"},
            {"family": "Physical Protection (PE)", "priority": "medium"},
            {"family": "Personnel Security (PS)", "priority": "medium"},
            {"family": "Risk Assessment (RA)", "priority": "high"},
            {"family": "Security Assessment (CA)", "priority": "high"},
            {"family": "System and Services Acquisition (SA)", "priority": "medium"},
            {"family": "Incident Response (IR)", "priority": "critical"},
            {"family": "Maintenance (MA)", "priority": "low"}
        ]
        
        return control_families
    
    def research_gap_solution(self, gap: Dict) -> Dict:
        """Use agents to research solutions for a specific gap"""
        print(f"\n🔍 Researching: {gap['family']}")
        
        # Step 1: Search existing knowledge base
        family_code = gap['family'].split('(')[1].strip(')')
        kb_results = self.kb.search(family_code)
        existing_knowledge = len(kb_results)
        print(f"  ✅ Found {existing_knowledge} existing documents")
        
        # Step 2: Generate comprehensive solution using Claude
        family_name = gap['family'].split('(')[0].strip()
        
        prompt = f"""Generate a comprehensive Midnight blockchain compliance solution for NIST 800-171 control family: {family_name}

Include:

1. CONTROL FAMILY OVERVIEW
   - Requirements summary
   - Current compliance challenges

2. MIDNIGHT BLOCKCHAIN SOLUTION
   - How Midnight's privacy features address requirements
   - Zero-knowledge proof applications
   - Smart contract implementations

3. AMD SEV-SNP HARDWARE ENFORCEMENT
   - Hardware-level security controls
   - Memory encryption benefits
   - Ransomware prevention mechanisms

4. IMPLEMENTATION GUIDE
   - Step-by-step deployment
   - Code examples where applicable
   - Configuration requirements

5. VERIFICATION & AUDIT
   - How to prove compliance
   - Audit trail generation
   - Reporting mechanisms

Make it technical, actionable, and specific to Midnight + AMD SEV-SNP architecture.
Limit response to 5000 characters maximum."""

        try:
            response = self.doc_agent.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            solution = response.content[0].text
            print(f"  ✅ Generated {len(solution)} character solution")
            
            return {
                "gap": gap,
                "existing_docs": existing_knowledge,
                "solution": solution,
                "generated_at": datetime.now().isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return {
                "gap": gap,
                "status": "error",
                "error": str(e)
            }
    
    def save_solution(self, result: Dict):
        """Save the gap-filling solution to knowledge base"""
        if result['status'] != 'completed':
            return
        
        family_code = result['gap']['family'].split('(')[1].strip(')')
        filename = f"{family_code}_Midnight_Solution_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(self.results_dir, filename)
        
        # Create markdown document
        content = f"""---
control_family: "{result['gap']['family']}"
solution_type: "Midnight Blockchain + AMD SEV-SNP"
generated: "{result['generated_at']}"
existing_docs_referenced: {result['existing_docs']}
priority: "{result['gap']['priority']}"
status: "AI Generated - Requires Review"
---

# {result['gap']['family']} - Midnight Compliance Solution

{result['solution']}

---
*Generated by Midnight Infrastructure AI Agent System*
*Date: {result['generated_at']}*
*Requires technical review and validation before implementation*
"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"  💾 Saved to: {filename}")
        return filepath
    
    def run_gap_filling_campaign(self, analysis_file: str, max_gaps: int = None):
        """Run complete gap-filling campaign"""
        print("=" * 80)
        print("MIDNIGHT INFRASTRUCTURE - GAP FILLING CAMPAIGN")
        print("=" * 80)
        print(f"\nStarted: {datetime.now().isoformat()}")
        print("")
        
        # Extract gaps
        gaps = self.extract_gaps_from_analysis(analysis_file)
        if max_gaps:
            gaps = gaps[:max_gaps]
        
        print(f"📋 Addressing {len(gaps)} NIST 800-171 control families")
        print("")
        
        results = []
        for i, gap in enumerate(gaps, 1):
            print(f"\n[{i}/{len(gaps)}] {gap['family']} (Priority: {gap['priority']})")
            print("-" * 80)
            
            # Research solution
            result = self.research_gap_solution(gap)
            
            # Save if successful
            if result['status'] == 'completed':
                filepath = self.save_solution(result)
                result['saved_to'] = filepath
            
            results.append(result)
            
            print("-" * 80)
        
        # Generate summary
        completed = sum(1 for r in results if r['status'] == 'completed')
        errors = sum(1 for r in results if r['status'] == 'error')
        
        print("\n" + "=" * 80)
        print("CAMPAIGN SUMMARY")
        print("=" * 80)
        print(f"Total gaps addressed: {len(gaps)}")
        print(f"✅ Successfully completed: {completed}")
        print(f"❌ Errors: {errors}")
        print(f"📁 Solutions saved to: {self.results_dir}")
        print("=" * 80)
        
        # Save summary report
        summary_file = f"gap_filling_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump({
                "campaign_date": datetime.now().isoformat(),
                "total_gaps": len(gaps),
                "completed": completed,
                "errors": errors,
                "results": [
                    {
                        "family": r['gap']['family'],
                        "priority": r['gap']['priority'],
                        "status": r['status'],
                        "file": r.get('saved_to', None)
                    }
                    for r in results
                ]
            }, f, indent=2)
        
        print(f"\n📊 Summary saved to: {summary_file}")
        return results

if __name__ == "__main__":
    orchestrator = GapFillingOrchestrator()
    
    # Run gap-filling campaign
    # Start with just 3 gaps as a test
    results = orchestrator.run_gap_filling_campaign(
        analysis_file="FRESH_GAP_ANALYSIS_2025.md",
        max_gaps=14  # Increase this to process more control families
    )
    
    print("\n✅ Gap-filling campaign complete!")
    print("Review generated solutions and increase max_gaps to process more families.")
