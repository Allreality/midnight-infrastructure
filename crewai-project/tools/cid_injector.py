# File: tools/cid_injector.py
# Location: crewai-project/tools/cid_injector.py

from tools.file_reader import read_json_file
from tools.file_writer import write_json_file
from tools.claim_logger import append_cid, append_error

def inject_provenance(registry_path, eligible_wallets):
    try:
        registry = read_json_file(registry_path)
        claims = registry.get("claims", [])
        cid_prefix = "bafybeigdyrmidnightglacier"

        for i, claim in enumerate(claims):
            wallet = claim.get("wallet")
            if wallet in eligible_wallets:
                cid = f"{cid_prefix}{str(i+1).zfill(3)}"
                claim["cid"] = cid
                append_cid(wallet, cid)

        write_json_file(registry_path, {"claims": claims})

    except Exception as e:
        append_error(f"CID injection failed: {str(e)}")