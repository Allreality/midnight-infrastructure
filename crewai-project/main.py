# File: main.py
# Location: crewai-project/main.py

from dotenv import load_dotenv
import os
import sys
from tools.cid_injector import inject_provenance
from tools.claim_endpoint import process_claim
from tools.wallet_checker import verify_wallets
from tools.audit_report import generate_audit_report

load_dotenv()
REGISTRY_PATH = os.getenv("REGISTRY_PATH")
VERIFICATION_LOG = os.getenv("VERIFICATION_LOG")
AUDIT_REPORT = os.getenv("AUDIT_REPORT")

def run_tool(tool_name, *args):
    if tool_name == "inject":
        inject_provenance(REGISTRY_PATH, args)
    elif tool_name == "claim":
        wallet = args[0] if args else input("Enter wallet address: ").strip()
        print(process_claim(wallet))
    elif tool_name == "verify":
        verify_wallets("data/wallets/eligibility.json", VERIFICATION_LOG)
    elif tool_name == "report":
        generate_audit_report(VERIFICATION_LOG, AUDIT_REPORT)
    else:
        print(f"Unknown tool: {tool_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [inject|claim|verify|report] [args...]")
    else:
        run_tool(sys.argv[1], *sys.argv[2:])