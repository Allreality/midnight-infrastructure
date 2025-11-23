# File: audit_report.py
# Location: crewai-project/tools/audit_report.py

import json
from datetime import datetime

def generate_audit_report(log_path, output_path):
    try:
        with open(log_path, "r") as f:
            log = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read verification log: {e}")
        return

    eligible = log.get("eligible_wallets", [])
    ineligible = log.get("ineligible_wallets", [])
    errors = log.get("errors", [])
    timestamp = datetime.utcnow().isoformat()

    lines = [
        f"# Midnight Glacier Drop Audit Report",
        f"**Generated:** {timestamp} UTC\n",
        f"## ✅ Eligible Wallets",
    ]
    lines += [f"- {addr}" for addr in eligible] or ["_None_"]

    lines.append("\n## ❌ Ineligible Wallets")
    lines += [f"- {addr}" for addr in ineligible] or ["_None_"]

    lines.append("\n## 🧬 CID Injections")
    if "cid_injections" in log:
        cid_map = log["cid_injections"]
        if isinstance(cid_map, list) and cid_map:
            for entry in cid_map:
                if isinstance(entry, dict):
                    addr = entry.get("address", "UNKNOWN")
                    cid = entry.get("cid", "MISSING")
                elif isinstance(entry, list) and len(entry) == 2:
                    addr, cid = entry
                else:
                    addr, cid = "MALFORMED", "MISSING"
                lines.append(f"- {addr}: `{cid}`")
        else:
            lines.append("_None_")
    else:
        lines.append("_None_")

    lines.append("\n## ⚠️ Errors")
    lines += [f"- {err}" for err in errors] or ["_None_"]

    try:
        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        print(f"✅ Audit report written to {output_path}")
    except Exception as e:
        print(f"❌ Failed to write audit report: {e}")