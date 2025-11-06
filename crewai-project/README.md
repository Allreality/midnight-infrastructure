🧩 Project Structure

crewai-project/
├── main.py                         # CLI entrypoint
├── .env                            # Environment variables (excluded from Git)
├── tools/                          # Modular tool scripts
│   ├── cid_injector.py             # Injects CID into registry
│   ├── claim_endpoint.py           # Processes wallet claims
│   ├── wallet_checker.py           # Verifies wallet eligibility
│   └── audit_report.py             # Generates Markdown audit report
├── data/
│   └── registry/claims.json        # CID registry
├── outputs/
│   ├── claim_verification_logs.json  # Wallet verification log
│   └── midnight_glacier_audit_v2.md # Markdown audit report
└── main_cli.md                     # CLI cheat sheet

⚙️ Setup
- Install dependencies:
pip install python-dotenv

- Create .env file:
REGISTRY_PATH=data/registry/claims.json
VERIFICATION_LOG=outputs/claim_verification_logs.json
AUDIT_REPORT=outputs/midnight_glacier_audit_v2.md

- Optional .gitignore:  (Use it)
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore

🚀 CLI Usage
Run from the root of crewai-project/:
|  |  | 
| python main.py inject WALLET_ADDRESS | Injects CID for wallet | 
| python main.py claim | Prompts for wallet and registers claim| 
| python main.py verify | Verifies wallets and logs results | 
| python main.py report | Generates Markdown audit report | 


See main_cli.md for full usage examples.

🧾 Reproducibility Principles
- No destructive writes — all claims and logs are additive
- CID provenance — every claim is traceable via injected CID
- Audit-grade reporting — Markdown logs for transparency
- Modular architecture — each tool is independently testable and replaceable

🤝 Contributing
- Fork and clone the repo
- Add new tools to tools/
- Extend CLI logic in main.py
- Submit PRs with clear commit messages and reproducibility notes
