# File: run_claim.py
# Location: crewai-project/run_claim.py

from tools.claim_endpoint import process_claim

if __name__ == "__main__":
    wallet = input("Enter wallet address to claim: ").strip()
    result = process_claim(wallet)
    print(result)