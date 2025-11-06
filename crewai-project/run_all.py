# File: run_all.py
# Location: crewai-project/run_all.py

from tools.claim_logger import init_log
from tools.wallet_checker import validate_wallets
from tools.cid_injector import inject_provenance
from tools.file_reader import read_json_file
from tools.markdown_reporter import generate_audit_report

# Step 1: Reset log
init_log()

# Step 2: Validate wallets
validate_wallets("data/wallets/eligibility.json")

# Step 3: Inject CIDs
log = read_json_file("outputs/claim_verification_logs.json")
eligible_wallets = log.get("eligible_wallets", [])
inject_provenance("data/registry/claims.json", eligible_wallets)

# Step 4: Generate Markdown report
generate_audit_report(log, "outputs/midnight_glacier_audit_v1.md")