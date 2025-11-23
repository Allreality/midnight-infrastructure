🧩 Midnight Glacier Drop CLI — Cheat Sheet

Location: 

Purpose: Modular CLI for agentic claim orchestration, CID injection, wallet verification, and audit reporting.



⚙️ Setup

1\. 	Install dependencies:



pip install python-dotenv



**- Create .env file at project root**

**REGISTRY\_PATH=data/registry/claims.json**

**VERIFICATION\_LOG=outputs/claim\_verification\_logs.json**

**AUDIT\_REPORT=outputs/midnight\_glacier\_audit\_v2.md**



**3. 	Optional :.gitignore   (I did add it)**

**echo ".env" >> .gitignore**

**echo "\_\_pycache\_\_/" >> .gitignore**

**echo "\*.pyc" >> .gitignore**



**🚀 CLI Commands**

**Run from the root of :crewai-project**

**🧬 Inject CID for Wallet**

**python main.py inject WALLET\_ADDRESS**



**Injects CID into claims.json for the given wallet.**

**🌙 Submit Claim**



**python main.py claim**



**Prompts for wallet address and registers claim if eligible.**

**✅ Verify Wallets**



**python main.py verify**

**Checks wallet eligibility and logs results to .**

**📜 Generate Audit Report**



**python main.py report**

**Creates Markdown report from verification log**



**📁 Key Files**

**|  |  |** 

**| .env |  |** 

**| main.py |  |** 

**| data/registry/claims.json |  |** 

**| outputs/claim\_verification\_logs.json |  |** 

**| outputs/midnight\_glacier\_audit\_v2.md |  |** 







**🧾 Example Flow**

**python main.py verify**

**python main.py inject 8pwcfgJNu37Ksnjod1TMXjuQnHhVoSWawZZR96LSx2aj**

**python main.py claim**

**python main.py report**



