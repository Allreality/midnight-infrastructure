# File: tools/markdown_reporter.py
# Location: crewai-project/tools/markdown_reporter.py
from tools.file_reader import read_json_file
import os
from datetime import datetime

def generate_audit_report(data, output_path):
    lines = [
        f"# Midnight Glacier Drop Audit Report",
        f"**Generated:** {datetime.utcnow().isoformat()} UTC\n",
        "## ✅ Eligible Wallets",
        "\n".join(f"- {w}" for w in data.get("eligible_wallets", [])),
        "\n## ❌ Ineligible Wallets",
        "\n".join(f"- {w} ({r})" for w, r in data.get("ineligible_wallets", [])),
        "\n## 🧬 CID Injections",
        "\n".join(f"- {w}: {cid}" for w, cid in data.get("cid_injections", [])),
        "\n## ⚠️ Errors",
        "\n".join(f"- {e}" for e in data.get("errors", []))
    ]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")