# File: scripts/test_log_claim.py

from agents.claimAgent import log_claim_attempt

log = log_claim_attempt(
    address="addr1qtestxyz...",
    wallet="agent-001",
    phase="glacier-drop",
    status="success",
    notes="Injected via test script"
)

print("Logged claim attempt:")
print(log)