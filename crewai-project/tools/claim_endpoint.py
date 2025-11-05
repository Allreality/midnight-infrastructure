# File: tools/claim_endpoint.py
# Location: crewai-project/tools/claim_endpoint.py

from tools.registry_precheck import is_wallet_eligible
from tools.cid_injector import inject_provenance
from tools.claim_logger import append_error
from tools.file_reader import read_json_file

def process_claim(wallet_address, registry_path="data/registry/claims.json", log_path="outputs/claim_verification_logs.json"):
    status = is_wallet_eligible(wallet_address, log_path)

    if status is True:
        inject_provenance(registry_path, [wallet_address])
        return f"✅ Claim accepted for {wallet_address}"
    elif status is False:
        return f"❌ Claim rejected for {wallet_address} — not eligible"
    else:
        append_error(f"⚠️ Claim attempt by unknown wallet: {wallet_address}")
        return f"⚠️ Claim rejected — wallet {wallet_address} not found in verification log"