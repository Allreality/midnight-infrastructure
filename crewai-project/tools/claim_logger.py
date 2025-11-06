# File: tools/claim_logger.py
# Location: crewai-project/tools/claim_logger.py
from tools.file_reader import read_json_file
import os
import json

LOG_PATH = "outputs/claim_verification_logs.json"

def init_log():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "eligible_wallets": [],
            "ineligible_wallets": [],
            "cid_injections": [],
            "errors": []
        }, f, indent=2)

def append_eligible(wallet):
    _update_log("eligible_wallets", wallet)

def append_ineligible(wallet, reason):
    _update_log("ineligible_wallets", [wallet, reason])

def append_cid(wallet, cid):
    _update_log("cid_injections", [wallet, cid])

def append_error(message):
    _update_log("errors", message)

def _update_log(key, entry):
    try:
        with open(LOG_PATH, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault(key, []).append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    except Exception as e:
        print(f"Log update failed: {e}")