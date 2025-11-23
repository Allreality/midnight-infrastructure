# File: tools/registry_precheck.py
# Location: crewai-project/tools/registry_precheck.py

from tools.file_reader import read_json_file

def is_wallet_eligible(wallet_address, log_path="outputs/claim_verification_logs.json"):
    try:
        log = read_json_file(log_path)
        eligible = log.get("eligible_wallets", [])
        ineligible = [entry[0] for entry in log.get("ineligible_wallets", [])]

        if wallet_address in eligible:
            return True
        elif wallet_address in ineligible:
            return False
        else:
            return None  # Not found in either list

    except Exception as e:
        print(f"Precheck failed: {e}")
        return None