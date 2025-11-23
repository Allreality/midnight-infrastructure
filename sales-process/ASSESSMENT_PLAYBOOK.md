# Security Assessment Playbook
**When a prospect requests an assessment**

---

## IMMEDIATE RESPONSE (Within 2 Hours)

### Email Template
```
Subject: Re: Security Assessment Request - Next Steps

Hi [Name],

Thanks for your interest in our security assessment!

I'd like to schedule a 30-minute discovery call to understand your environment before running the assessment. This ensures our AI agents focus on what matters most to you.

Are you available:
- [Day] at [Time]
- [Day] at [Time]  
- [Day] at [Time]

Or feel free to suggest times that work better for you.

In the meantime, here's what to expect:

**Discovery Call (30 min):**
- Understand your current security posture
- Identify compliance requirements
- Discuss your infrastructure

**Assessment Phase (48 hours):**
- Our AI agents analyze your environment
- Gap analysis across 14 NIST control families
- Risk prioritization

**Results Review (45 min):**
- Walk through findings
- Discuss recommendations
- Answer questions
- Explore next steps (no pressure)

Looking forward to connecting!

Best,
Akil Hashim
Founder, Total Reality Global
akilhashim1@gmail.com
(508) 631-1683
```

---

## PHASE 1: DISCOVERY CALL (30 minutes)

### Preparation
- [ ] Review their LinkedIn/website
- [ ] Google their company + "ransomware" or "breach"
- [ ] Understand their industry
- [ ] Have NIST gap analysis agent ready

### Call Structure

**Opening (2 min)**
"Thanks for taking the time [Name]. Before we dive into the technical assessment, I'd like to understand your specific situation so our AI agents can focus on what matters most to you. Sound good?"

**Discovery Questions (15 min)**

1. **Current State**
   - "Walk me through your current security architecture."
   - "What security tools are you using today?"
   - "How do you currently handle compliance?"

2. **Pain Points**
   - "What prompted you to reach out now?"
   - "Have you experienced any security incidents?"
   - "What keeps you up at night about your security?"

3. **Requirements**
   - "Do you need to meet NIST 800-171? By when?"
   - "Are you subject to other compliance frameworks?" (HIPAA, CMMC, etc.)
   - "What are your RTO/RPO requirements?"

4. **Environment**
   - "How many servers/endpoints are we talking about?"
   - "Cloud, on-prem, or hybrid?"
   - "What's your virtualization platform?"

5. **Decision Process**
   - "Who else is involved in security decisions?"
   - "What's your typical procurement process?"
   - "What budget cycle are you in?"

**What You Can Offer (10 min)**

"Based on what you've shared, here's how our assessment will work:

**Phase 1 - Automated Discovery (You provide):**
- Network diagram (if available)
- Current security tool list
- Compliance requirements documentation

**Phase 2 - AI Analysis (We do):**
- Our agents analyze against all 14 NIST 800-171 control families
- Identify gaps and prioritize by risk
- Generate detailed report with specific recommendations

**Phase 3 - Results Review (We present):**
- 45-minute walkthrough of findings
- Specific remediation steps
- Implementation roadmap
- Cost estimates

**Timeline:**
- You send info: Today/Tomorrow
- We run assessment: 48 hours
- Results review: Within 1 week

No cost, no obligation. You'll walk away with a comprehensive gap analysis even if you don't move forward with us."

**Closing (3 min)**
"Does this approach make sense? Any questions?"

"Great! I'll send you an email right after this call with:
1. Information request list
2. NDA (if needed)
3. Calendar link for results review

Looking forward to showing you what our AI agents can find."

---

## PHASE 2: INFORMATION GATHERING

### Email After Discovery Call
```
Subject: Next Steps - Security Assessment for [Company]

Hi [Name],

Great talking with you! Here's what I need to run the assessment:

**Required Information:**
1. Network architecture diagram (high-level is fine)
2. List of current security tools
3. Compliance requirements (NIST 800-171, HIPAA, etc.)
4. Number of users/endpoints

**Optional (but helpful):**
5. Recent security audit results (if any)
6. Current incident response plan
7. Data classification policy

**If you need an NDA:**
I've attached our standard mutual NDA. Once signed, you can share the information securely.

**Upload Location:**
[Create a secure SharePoint/Drive folder or use email]

Once I have this info, I'll have results ready within 48 hours.

Best,
Akil
```

---

## PHASE 3: RUNNING THE ASSESSMENT

### What You Actually Do

**Option A: Manual Analysis (Current capability)**
```bash
cd /mnt/c/projects/Security/nist-agents/nist-agents

# 1. Create customer folder
mkdir -p assessments/[company-name]
cd assessments/[company-name]

# 2. Document their current state
cat > environment.txt << 'ENV'
Company: [Name]
Industry: [Healthcare/Finance/etc]
Users: [Number]
Servers: [Number]
Cloud: [AWS/Azure/On-prem]
Current Security: [List their tools]
Compliance Need: [NIST 800-171/HIPAA/etc]
Timeline: [Their deadline]
ENV

# 3. Run NIST compliance analyzer
cd ../..
python3 agents/intelligence/nist_compliance_analyzer.py > assessments/[company-name]/gap_analysis.txt

# 4. Research their specific needs
python3 << 'ANALYSIS'
from agents.intelligence.midnight_researcher import MidnightResearchAgent

agent = MidnightResearchAgent()

# Search for controls relevant to their industry
results = agent.find_compliance_docs("healthcare HIPAA NIST")
# Or "financial services" or "government contractor"

# Save results
with open('assessments/[company-name]/specific_requirements.txt', 'w') as f:
    for result in results:
        f.write(f"Document: {result['file']}\n")
        f.write(f"Preview: {result['preview']}\n\n")
ANALYSIS

# 5. Create assessment report (see template below)
```

**Option B: Using Knowledge Base API**
```bash
# Query for industry-specific controls
curl -X POST http://localhost:5002/api/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query":"healthcare ransomware prevention"}' > healthcare_controls.json

curl -X POST http://localhost:5002/api/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query":"NIST 800-171 implementation"}' > nist_implementation.json
```

---

## PHASE 4: CREATING THE ASSESSMENT REPORT

### Report Template

Create a document (Word/Google Docs) with this structure:
```markdown
# CONFIDENTIAL
## Security Assessment Report
**Company:** [Name]
**Date:** [Date]
**Prepared by:** Akil Hashim, Total Reality Global

---

## EXECUTIVE SUMMARY

[Company] currently has [X/14] NIST 800-171 control families implemented.

**Key Findings:**
- [Gap 1] - HIGH RISK
- [Gap 2] - MEDIUM RISK  
- [Gap 3] - MEDIUM RISK

**Estimated Risk Exposure:** $[X]M annually
**Recommended Investment:** $[Amount]
**ROI:** [X]x over 5 years

---

## CURRENT STATE ASSESSMENT

**Infrastructure:**
- [Number] servers
- [Number] endpoints
- [Cloud/On-prem]

**Security Tools:**
- [List what they have]

**Compliance Status:**
- NIST 800-171: [X/14] control families
- [Other frameworks]: [Status]

---

## GAP ANALYSIS

### Critical Gaps (High Priority)

#### 1. Access Control (3.1)
**Current State:** [What they have]
**Gap:** [What's missing]
**Risk:** Unauthorized access, privilege escalation
**Solution:** [Specific recommendation]
**Cost:** $[Estimate]

#### 2. Audit & Accountability (3.3)
**Current State:** [What they have]
**Gap:** Logs can be deleted by attackers
**Risk:** No forensics after breach
**Solution:** Blockchain immutable audit trails
**Cost:** $[Estimate]

[Continue for each gap...]

### Medium Priority Gaps
[List 3-5 medium priority items]

### Low Priority Gaps
[List remaining items]

---

## RANSOMWARE RISK ASSESSMENT

**Current Vulnerability:**
Based on your environment, you are vulnerable to:
- Lateral movement after initial compromise
- Memory-based attacks bypassing antivirus
- Log deletion hiding attacker activity
- Data exfiltration before encryption

**Likelihood:** HIGH (60% annually for [industry])
**Impact:** $[Average for their size/industry]M
**Expected Annual Cost:** $[Likelihood x Impact]M

---

## RECOMMENDED SOLUTION

### Phase 1: Immediate (30 days)
**Priorities:** [Top 3 gaps]
**Investment:** $[Amount]
**Risk Reduction:** [X]%

### Phase 2: Short-term (90 days)
**Priorities:** [Next 5 gaps]
**Investment:** $[Amount]
**Risk Reduction:** [X]%

### Phase 3: Long-term (6-12 months)
**Priorities:** [Remaining gaps]
**Investment:** $[Amount]
**Risk Reduction:** [X]%

### Total Reality Global Solution

Our hardware-enforced approach addresses [X] of your [Y] gaps:

**Included:**
- AMD EPYC SEV-SNP hardware (isolates workloads)
- Midnight blockchain (immutable audit trails)
- AI compliance monitoring (continuous verification)
- Complete NIST 800-171 coverage

**Investment:**
- Enterprise: $500,000
- Professional: $50,000 (consultation only)

**ROI:** [X]x over 5 years vs. expected breach costs

---

## IMPLEMENTATION ROADMAP

**Week 1:** Discovery and design
**Week 2-3:** Hardware procurement
**Week 4-5:** Implementation
**Week 6:** Validation and training

**Total Timeline:** 30-45 days to operational

---

## NEXT STEPS

**Option 1: Full Implementation**
Proceed with enterprise deployment ($500K)

**Option 2: Phased Approach**
Start with assessment + consultation ($50K)

**Option 3: Do Nothing**
Accept $[X]M annual risk exposure

**Recommended:** [Your recommendation]

---

## APPENDIX

### A. NIST 800-171 Control Coverage
[Detailed breakdown of 14 control families]

### B. Compliance Timeline
[Their specific deadlines - e.g., NIH Jan 25]

### C. References
[Link to relevant compliance docs from knowledge base]

---

**Questions?**
Akil Hashim
akilhashim1@gmail.com
(508) 631-1683
```

---

## PHASE 5: RESULTS REVIEW CALL (45 minutes)

### Preparation
- [ ] Send report 24 hours before call
- [ ] Review their discovery notes
- [ ] Prepare specific examples from their environment
- [ ] Have ROI calculator ready

### Call Structure

**Opening (5 min)**
"Thanks for reviewing the report. Before I walk through the findings, what jumped out at you? Any questions so far?"

**Findings Walkthrough (20 min)**

For each HIGH priority gap:
1. "Here's what we found..."
2. "Here's why it matters..."
3. "Here's what happens if not addressed..."
4. "Here's how we fix it..."

Use THEIR examples:
- "Remember you mentioned [X]? That's vulnerable because..."
- "Your [specific tool] doesn't protect against [specific threat]..."

**Solution Overview (10 min)**

"Our approach solves [X] of these [Y] gaps with one integrated system:

**Hardware Layer:** AMD EPYC stops attacks even with admin access
**Blockchain Layer:** Immutable logs ransomware can't delete
**AI Layer:** Continuous monitoring without manual work

**Specific to you:**
- [Gap 1] → Solved by [specific feature]
- [Gap 2] → Solved by [specific feature]
- [Gap 3] → Solved by [specific feature]"

**Business Case (5 min)**

"Let's talk numbers:

**Your Risk:**
- $[X]M average attack cost for [their size]
- 60% probability
- = $[Y]M expected annual cost

**Our Solution:**
- $500K implementation
- $100K/year support
- = $1.3M over 5 years

**ROI:** One prevented attack pays for itself twice over.

Plus:
- Insurance premium reduction: 40-60%
- Compliance certification: [Their specific need]
- Peace of mind: 24/7 automated protection"

**Closing (5 min)**

**If they're interested:**
"What would you like to do next? I can have a detailed proposal and SOW to you within 48 hours."

**If they need time:**
"What concerns do you need to address? Who else needs to be involved? What's your timeline for deciding?"

**If they're hesitant:**
"I understand this is a significant investment. What if we started with the professional tier at $50K? You get:
- Detailed implementation roadmap
- 6-month monitoring trial
- Full access to compliance documentation
- Then decide about full deployment"

---

## PHASE 6: PROPOSAL & CLOSING

### Proposal Template
```markdown
# PROPOSAL
## Security Implementation - [Company]

**Prepared for:** [Name, Title]
**Date:** [Date]
**Valid through:** [Date + 30 days]

---

## SCOPE OF WORK

Based on our assessment, we propose implementing our patent-pending hardware-enforced security architecture to address [X] identified gaps.

**Deliverables:**
1. AMD EPYC SEV-SNP server deployment ([Number] servers)
2. Midnight blockchain attestation layer (3-node cluster)
3. AI compliance monitoring system
4. Complete NIST 800-171 documentation
5. Staff training (8 hours)
6. 30-day post-deployment support

**Timeline:** 6 weeks from contract signature

---

## INVESTMENT

**Implementation:** $500,000
Includes:
- Hardware (AMD EPYC servers)
- Software licenses
- Integration & configuration
- Testing & validation
- Training & documentation

**Ongoing (Annual):** $100,000
- 24/7 monitoring
- Quarterly compliance audits
- Software updates
- Support (email/phone)

**Optional Add-ons:**
- Additional servers: $50K each
- Extended support: $5K/month
- Training refreshers: $10K per session

---

## PAYMENT TERMS

**Option A: Full Payment**
- $500K at contract signing
- 5% discount = $475K

**Option B: Phased**
- 50% ($250K) at contract signing
- 25% ($125K) at hardware delivery
- 25% ($125K) at go-live

**Option C: Subscription** (if they prefer)
- $150K/year for 5 years
- Includes all hardware, software, support

---

## TERMS & CONDITIONS

- Net 30 payment terms
- Travel expenses billed separately
- Change orders require written approval
- 90-day warranty on implementation
- Cancellation clause: [Details]

---

## NEXT STEPS

1. Review and approve proposal
2. Execute Master Services Agreement
3. Issue PO or wire first payment
4. Kickoff meeting (Week 1)
5. Implementation begins

**Questions?**
Akil Hashim
akilhashim1@gmail.com
(508) 631-1683

---

**Signature:**

_____________________________  Date: ________
[Client Name, Title]

_____________________________  Date: ________
Akil Hashim, Founder
Total Reality Global
```

---

## OBJECTION HANDLING

### "That's expensive"
**Response:** "I appreciate $500K is significant. Let's compare to alternatives:

- Do nothing: $5M+ expected breach cost
- Traditional solutions: $300-400K but software-only (bypassable)
- Our solution: $500K but hardware-enforced (cannot bypass)

Which would you prefer: spending $500K now with guaranteed protection, or risking $5M+ if attacked?"

**Alternative:** "What if we started with the $50K professional tier? You get the roadmap and can phase the investment."

### "We need to get other quotes"
**Response:** "Absolutely, you should! Here's what makes us unique:

- Patent-pending (no one else has this combination)
- Hardware-enforced (others are software-only)
- 14/14 NIST coverage (most do 8-10)
- Blockchain audit trails (immutable)

When you compare, ask vendors:
1. Can ransomware bypass their solution with admin access?
2. Can attackers delete their audit logs?
3. Do they cover all 14 NIST control families?

We're confident in our differentiation."

### "We need more time"
**Response:** "I understand. What's your timeline?

Keep in mind:
- NIH mandate is January 25, 2025
- Implementation takes 6 weeks
- That means you need to decide by [Date - 6 weeks before deadline]

I'm happy to follow up in [timeframe]. What specific concerns do you need to address?"

### "Our budget is only $X"
**Response:** "Let's work with that. For $[their budget]:

If < $50K: "I can provide consultation and roadmap"
If $50-200K: "We can do partial implementation—focus on your top 3 gaps"
If $200-400K: "We can phase it—deploy critical systems first, add more later"

What matters most to you?"

---

## FOLLOW-UP CADENCE

**After Assessment:**
- Day 1: Thank you email with report
- Day 3: "Any questions?" email
- Day 7: Phone check-in
- Day 14: "Just following up" email
- Day 30: "Circling back" email

**After Proposal:**
- Day 1: Confirm receipt
- Day 3: "Any questions?" call
- Day 7: Check-in email
- Day 14: "Deadline approaching" email
- Day 30: Final follow-up

**Don't burn bridges:** If they say no, end with:
"I understand this isn't the right time. Would it be okay if I checked back in [3/6/12] months? Things may have changed by then."

---

## SUCCESS METRICS

Track for each assessment:
- [ ] Discovery call completed
- [ ] Assessment delivered on time
- [ ] Results review completed
- [ ] Proposal sent
- [ ] Follow-up cadence executed
- [ ] Win/loss documented
- [ ] Lessons learned noted

---

**Remember:** The goal isn't to sell everyone. The goal is to:
1. Provide genuine value (they get free assessment)
2. Build relationship (they remember you)
3. Convert qualified prospects (right fit, right time, right budget)

You're solving real problems. Be confident in the solution.

