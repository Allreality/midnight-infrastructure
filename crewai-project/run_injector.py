# File: run_injector.py
# Location: midnight-infrastructure/crewai-project/run_injector.py

from tools.cid_injector import inject_provenance
from tools.file_reader import read_json_file

log = read_json_file("outputs/claim_verification_logs.json")
eligible_wallets = log.get("eligible_wallets", [])
inject_provenance("data/registry/claims.json", eligible_wallets)