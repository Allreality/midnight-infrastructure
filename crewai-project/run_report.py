# File: run_report.py
# Location: crewai-project/run_report.py

from tools.file_reader import read_json_file
from tools.markdown_reporter import generate_audit_report

# Load verification log
log = read_json_file("outputs/claim_verification_logs.json")

# Generate Markdown report
generate_audit_report(log, "outputs/midnight_glacier_audit_v1.md")