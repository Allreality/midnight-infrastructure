# File: tools/wallet_checker.py
# Location: crewai-project/tools/wallet_checker.py

from tools.file_reader import read_json_file
from tools.claim_logger import append_eligible, append_ineligible, append_error

def verify_wallets(eligibility_path, output_path):
    # your verification logic here
    ...

def validate_wallets(eligibility_path):
    try:
        data = read_json_file(eligibility_path)
        wallets = data.get("wallets", [])
        for wallet in wallets:
            address = wallet.get("address")
            if not address:
                append_error("Missing wallet address in eligibility entry")
                continue

            if wallet.get("blacklisted", False):
                append_ineligible(address, "Blacklisted")
            elif wallet.get("balance", 0) <= 0:
                append_ineligible(address, "Zero balance")
            elif not wallet.get("whitelisted", False):
                append_ineligible(address, "Not whitelisted")
            else:
                append_eligible(address)

    except Exception as e:
        append_error(f"Validation failed: {str(e)}")
    
__all__ = ["verify_wallets"]