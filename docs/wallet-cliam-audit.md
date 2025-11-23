# 🧊 Midnight Glacier Drop: Wallet Reliability & Claim Flow Audit

This document captures observed issues, wallet lineage, and governance implications from Akil Hashim’s participation in the Midnight Glacier Drop (Phases 1 & 2). It supports the case for agentic tooling and reproducible governance infrastructure.

---

## 🔐 Registered Wallets

| Wallet | Address |
|--------|---------|
| Nami   | addr1q96d08t9ewwatpacat7gntaz7yxljuz636pjkp995sg6zu6she9wyxestaml8uwhgadanxye4uqyea6xg8vmge3kr5nqyzd775 |
| Yoroi  | addr1qy8ykv5lu26myhwjmr46de7aykqphjjlfdadd8l8lenu79s070clupcy9lj75jkzwueakva4yame25867u8fy807hpzsy7e3pt |

---

## ⚠️ Observed Issues

### Phase 1
- Lace wallet failed to connect
- Payload signing consistently failed
- No fallback CLI or agentic flow available

### Phase 2
- Cache corruption in Lace
- Eligibility inconsistencies across migrated wallets
- Broken redirects and unclear UX

### Wallet Integration
- Yoroi and Nami addresses migrated into Lace
- Derivation path mismatches caused stake key confusion
- Nami extension interfered with Lace browser flow

---

## 🧠 Governance Implications

- Lack of reproducibility across wallets and claim flows
- No transparent lineage tracking for migrated addresses
- No agentic fallback for verifying eligibility or signing claims
- Snapshot eligibility logic is opaque and not user-verifiable

---

## 🛠️ Proposed Solutions

- Scaffold a **Claim Agent** to verify eligibility and sign payloads
- Add `/api/claims/attempts` endpoint to log claim attempts
- Publish wallet lineage and reliability reports for governance-grade transparency
- Create `registry/claimAttempts.json` to track claim outcomes per address

---

## 📁 File Placement

- Documentation: `docs/wallet-claim-audit.md`
- Registry: `registry/claimAttempts.json`
- Agent module: `agents/claimAgent.py`
- Logging route: `routes/claims.py`

---

## 🧭 Next Steps

- Validate snapshot eligibility for both addresses
- Log failed claim attempts with timestamps and notes
- Scaffold agentic fallback for future drops and governance flows