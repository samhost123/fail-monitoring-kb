---
title: "Copilot Prompts for Settlements Associates"
aliases: ["Copilot Prompts", "AI Prompts", "Fail Resolution Prompts"]
tags:
  - reference/prompts
  - workflow/copilot
created: 2026-02-05
status: final
---

# Copilot Prompts for Settlements Associates

Step-by-step prompts to help resolve fails using the knowledge base.

---

## Quick Reference Card

| # | Prompt | When to Use |
|---|--------|-------------|
| 1 | [[#1. FTD/FTR Offset Matching]] | Find matching positions to offset |
| 2 | [[#2. Corporate Action Impact Research]] | Suspect CA is affecting fail |
| 3 | [[#3. SSI Validation & Mismatch Resolution]] | Delivery rejection, SSI issue |
| 4 | [[#4. Reg SHO Close-Out Deadline Calculator]] | Determine regulatory urgency |
| 5 | [[#5. Priority Score & Escalation Assessment]] | Calculate priority, escalation |
| 6 | [[#6. CNS vs Obligation Warehouse Eligibility]] | Verify settlement path |
| 7 | [[#7. Chain Fail & Upstream FTR Analysis]] | Upstream failure blocking me |
| 8 | [[#8. Buy-In Decision Support]] | Evaluate buy-in options |
| 9 | [[#9. Aged Fail Capital Impact Calculator]] | Calculate haircuts/charges |
| 10 | [[#10. IMS Delivery Troubleshooting]] | Delivery not processing |
| 11 | [[#11. Stock Loan Recall Processing]] | Process incoming recall |
| 12 | [[#12. Reclaim Resolution Processing]] | Resolve delivery reversal |
| 13 | [[#13. Counterparty Outreach Communication]] | Draft CP communication |

---

## 1. FTD/FTR Offset Matching

**Use Case:** Find matching positions to offset and reduce exposure

```
Help me find offset matches for my Fail-to-Deliver.

**Step 1 - My Fail Details:**
- CUSIP: [enter 9-character CUSIP]
- Quantity: [enter share count]
- Settlement Date: [enter date]
- Counterparty: [enter name or ID]
- Current Age: [enter days]

**Step 2 - Search for FTR Matches:**
Using offset-matching.md criteria, search for FTR positions where:
- CUSIP matches exactly
- Settlement date is on or before my FTD settlement date
- Counterparty is same or affiliated

**Step 3 - Prioritize Matches:**
Rank found matches by:
1. Exact quantity match (best)
2. Oldest fail first
3. Earliest settlement date

**Step 4 - Calculate Offset:**
For each potential match, tell me:
- Full offset possible? (quantities equal)
- Partial offset? (show remaining exposure)
- Impact on aging clock (offset resets age)

**Step 5 - Recommend Action:**
Which match should I use and why?
```

**Related:** [[offset-matching]] | [[fail-to-deliver]] | [[fail-to-receive]]

---

## 2. Corporate Action Impact Research

**Use Case:** Check if CA is causing or affecting a fail

```
Help me investigate if a corporate action is impacting my fail.

**Step 1 - My Fail Details:**
- CUSIP: [enter CUSIP]
- Security Name: [enter name]
- Settlement Date: [enter date]
- Fail Type: [FTD or FTR]
- When Fail Started: [date first failed]

**Step 2 - Check for Pending CA Events:**
Search for:
- Reorganizations (mergers, spin-offs, acquisitions)
- Stock dividends or splits
- Mandatory exchanges
- Rights distributions
- Any announced ex-date near my settlement date

**Step 3 - Determine CA Priority Status:**
- Has this position been elevated to Priority Group 1 (CA priority)?
- Did the CA change the CUSIP? (old CUSIP → new CUSIP)

**Step 4 - Check Settlement Path:**
- Did this security exit CNS due to the CA?
- Is it now in Obligation Warehouse?
- Can it be rescued back to CNS after CA processes?

**Step 5 - Recommend Action:**
- Should I wait for CA to process? (if yes, expected timeline)
- Should I take action now? (if yes, what action)
- Do I need to update any records with new CUSIP?
```

**Related:** [[priority-groups]] | [[cns-eligibility-scan]] | [[obligation-warehouse]]

---

## 3. SSI Validation & Mismatch Resolution

**Use Case:** Troubleshoot delivery rejections from SSI mismatches

```
Help me diagnose a potential SSI mismatch causing my fail.

**Step 1 - Delivery Details:**
- CUSIP: [enter CUSIP]
- Counterparty: [enter name]
- DTC Participant Number: [enter 4-digit number]
- Agent Bank/Custodian: [enter name if known]
- Sub-Account: [enter if applicable]

**Step 2 - Check Rejection Info (if available):**
- DTC Reason Code: [enter code or "none"]
- Rejection Message: [enter text or "none"]

**Step 3 - Validate SSI Components:**
Using ssi-mismatches.md, check:
☐ Is DTC participant number valid in DTC directory?
☐ Is the agent bank currently active?
☐ Is the SSI less than 90 days old (stale check)?
☐ Is sub-account routing correct?

**Step 4 - Identify Mismatch Category:**
Which category does this fall into?
- DTC Account Mismatch (wrong/obsolete number)
- Agent Bank Mismatch (wrong custodian, custodian change)
- Sub-Account Routing Issue
- Missing SSI (new counterparty or security type)

**Step 5 - Resolution Steps:**
Based on category, provide:
1. Immediate correction action
2. Who to contact (counterparty, custodian, internal team)
3. SSI update process
4. How to resend delivery after correction
```

**Related:** [[ssi-mismatches]] | [[dtc-reason-codes]] | [[dk-processing]]

---

## 4. Reg SHO Close-Out Deadline Calculator

**Use Case:** Determine urgency based on regulatory deadlines

```
Calculate my Reg SHO deadline and required actions.

**Step 1 - My Fail Details:**
- Fail Type: [FTD or FTR]
- Sale Type: [Short Sale / Long Sale / Market Maker]
- Settlement Date: [enter date]
- Is Security on Threshold List: [Yes / No / Unknown]
- Today's Date: [enter today]

**Step 2 - Calculate Deadline:**
Using reg-sho-rule-204.md timelines:
- Short Sale FTD: S+1 (market open 9:30 AM ET next day)
- Long Sale FTD: S+3 (market open)
- Market Maker: S+3 extended
- Threshold Security: S+13 (mandatory purchase, no borrow allowed)

Calculate my specific deadline date and time.

**Step 3 - Determine Current Status:**
- Days since settlement date: [calculate]
- Days remaining until deadline: [calculate]
- Am I past deadline? [Yes/No]

**Step 4 - Assess Penalty Box Risk:**
If deadline missed or approaching:
- Would my firm enter penalty box for this security?
- What is the penalty box impact? (pre-borrow required for ALL short sales)
- Current borrow cost estimate for this security?

**Step 5 - Recommend Priority Level:**
Based on deadline proximity:
- CRITICAL: Past deadline or <1 day remaining
- HIGH: 1-2 days remaining
- MEDIUM: 3-5 days remaining
- STANDARD: >5 days remaining

What action should I take immediately?
```

**Related:** [[reg-sho-rule-204]] | [[threshold-securities]] | [[penalty-box]] | [[close-out-matrix]]

---

## 5. Priority Score & Escalation Assessment

**Use Case:** Calculate priority score and determine escalation level

```
Calculate the priority score for my fail and determine escalation.

**Step 1 - Fail Information:**
- Age (days since settlement): [enter days]
- Current Market Value: $[enter amount]
- Is Threshold Security: [Yes / No]
- Reg SHO Status: [No concern / Approaching deadline / Close-out required]
- Counterparty 15-day Fail Rate: [enter % or "unknown"]

**Step 2 - Coverage Information:**
- Inventory Coverage Percentage: [enter % or "unknown"]
  (What % of this position is covered by box, loan, or pending receives?)

**Step 3 - Calculate Base Score:**
Using priority-score-formula.md:
- Age Factor (0-100, weight 0.30): [based on days]
- Value Factor (0-100, weight 0.25): [based on $ amount]
- Regulatory Factor (0-100, weight 0.35): [based on Reg SHO status]
- CP History Factor (0-100, weight 0.10): [based on fail rate]

Base Score = (Age × 0.30) + (Value × 0.25) + (Reg × 0.35) + (CP × 0.10)

**Step 4 - Apply Modifiers:**
- Inventory Modifier: [0.50 if 100% covered → 1.00 if <25% covered]
- Concentration Modifier: [1.00 base, ×1.20 if threshold, ×1.15 if non-CNS, cap 1.50]

Final Score = Base Score × Inventory Modifier × Concentration Modifier

**Step 5 - Determine Escalation:**
| Score | Tier | Escalation Level | Response Time |
|-------|------|------------------|---------------|
| 0-25 | Low | Standard monitoring | 4 hours |
| 26-50 | Medium | L1 (Ops Analyst) | 2 business days |
| 51-75 | High | L2 (Senior Ops) | 1 business day |
| 76-100 | Critical | L3 (Management) | Same day |

My score, tier, and required escalation action?
```

**Related:** [[priority-score-formula]] | [[escalation-paths]] | [[prioritization-logic]]

---

## 6. CNS vs Obligation Warehouse Eligibility

**Use Case:** Verify settlement path eligibility

```
Check CNS eligibility for my position and settlement path options.

**Step 1 - Position Details:**
- CUSIP: [enter CUSIP]
- Security Name: [enter name]
- Counterparty Name: [enter name]
- Counterparty NSCC ID: [enter 5-digit ID or "unknown"]
- Trade Type: [Standard equity / Ex-clearing / Repo / Other]

**Step 2 - Security Eligibility Check:**
Using cns-cp-eligibility.md, verify:
☐ Valid 9-character CUSIP?
☐ USD-denominated?
☐ DTC-eligible (book-entry)?
☐ No trading restrictions or halts?

**Step 3 - Member Eligibility Check:**
☐ Counterparty is active NSCC member?
☐ Not suspended?
☐ Adequate clearing fund?

**Step 4 - Trade Eligibility Check:**
☐ Standard equity trade type?
☐ Not marked for ex-clearing?
☐ Both parties matched/confirmed?
☐ Submitted before cutoff?

**Step 5 - Determine Settlement Path:**
If ALL checks pass → CNS eligible (CCP guarantee, net booking, favorable capital)

If ANY check fails → Obligation Warehouse path:
- Identify which check failed
- Explain OW implications: No CCP guarantee, gross booking, higher capital charge
- Can this be "rescued" to CNS? (via eligibility scan if security becomes eligible)

**Step 6 - Recommend Action:**
What should I do based on eligibility status?
```

**Related:** [[cns-cp-eligibility]] | [[cns-system]] | [[obligation-warehouse]] | [[cns-eligibility-scan]]

---

## 7. Chain Fail & Upstream FTR Analysis

**Use Case:** Trace upstream failures blocking delivery

```
Help me analyze a chain failure blocking my delivery.

**Step 1 - My Delivery Position:**
- My Position Type: FTD (I need to deliver but can't)
- CUSIP: [enter CUSIP]
- Quantity I Need to Deliver: [enter shares]
- Who I'm Delivering To: [counterparty name]
- My Settlement Date: [enter date]

**Step 2 - My Expected Receive:**
- Am I expecting to receive these shares from another party? [Yes / No]
- If Yes:
  - Receiving From: [counterparty name]
  - Expected Receive Date: [enter date]
  - Receive Quantity: [enter shares]
  - Current Status of Receive: [Pending / Failed / Unknown]

**Step 3 - Trace the Chain:**
Using fail-to-receive.md chain effect logic:
- Is my FTD caused by an upstream FTR? [determine]
- How many links in the chain? (me ← counterparty ← their counterparty...)
- Is there visibility into upstream status?

**Step 4 - Assess Chain Impact:**
- If upstream resolves, will my position auto-settle?
- Are there multiple upstream sources that could cover my need?
- What is the oldest age in the chain?

**Step 5 - Recommend Resolution Path:**
Priority order:
1. Wait for upstream? (if resolution imminent, provide timeline)
2. Find alternative inventory? (box, borrow, or other pending)
3. Escalate to counterparty? (contact info and talking points)
4. Consider buy-in? (if aged and no upstream progress)

Which path should I take and why?
```

**Related:** [[fail-to-receive]] | [[fail-to-deliver]] | [[stock-borrow-program]]

---

## 8. Buy-In Decision Support

**Use Case:** Evaluate whether to initiate a buy-in

```
Help me evaluate buy-in options for my fail.

**Step 1 - Fail Details:**
- Fail Type: [FTD receiving an FTR / Standalone FTR]
- CUSIP: [enter CUSIP]
- Quantity: [enter shares]
- Age: [enter days]
- Market Value: $[enter amount]
- Settlement Path: [CNS / Bilateral]

**Step 2 - Current Status:**
- Have I already contacted counterparty? [Yes / No]
- Any expected resolution from counterparty? [Yes / No / Unknown]
- Is security hard-to-borrow? [Yes / No / Unknown]

**Step 3 - Evaluate CNS Buy-In (if CNS path):**
Using buy-in-mechanics.md - NSCC Rule 11 process:
1. Submit Buy-In Intent → Position moves to PG2
2. NSCC attempts allocation in next cycle
3. If unresolved → Retransmittal Notice issued
4. If still unresolved → Market execution, bill to failing party

Timeline and costs for CNS path?

**Step 4 - Evaluate Bilateral Buy-In (if Bilateral path):**
Using buy-in-mechanics.md - FINRA Rule 11810 process:
1. Written notice required (12:00 PM ET, T-2 before execution)
2. Check if securities in-transit (7-day extension if yes)
3. Execute purchase in open market
4. Bill price difference to failing party

Notice deadline and process for bilateral path?

**Step 5 - Cost-Benefit Analysis:**
- Cost of buy-in execution (market impact, spread)
- Cost of waiting (capital charges, regulatory risk)
- Probability of natural settlement if I wait

**Step 6 - Recommend Action:**
- Should I initiate buy-in? [Yes / No]
- Which type? [CNS / Bilateral]
- Next immediate step?
```

**Related:** [[buy-in-mechanics]] | [[priority-groups]] | [[cns-fails-charge]]

---

## 9. Aged Fail Capital Impact Calculator

**Use Case:** Calculate haircuts and financial impact of aging fail

```
Calculate the capital deduction and financial impact of my aged fail.

**Step 1 - Fail Details:**
- Settlement Date: [enter date]
- Current Age: [enter days since settlement]
- Current Market Value: $[enter amount]
- Position Type: [CNS / Bilateral (OW)]

**Step 2 - Calculate Rule 15c3-1 Haircut:**
Using aged-fail-deductions.md:
| Age | Haircut % | My Deduction |
|-----|-----------|--------------|
| S+5 | Monitoring begins | $0 |
| S+7 | 15% | $[calculate] |
| S+14 | 25% | $[calculate] |
| S+21 | 100% | $[calculate] |

What is my CURRENT haircut deduction?

**Step 3 - Calculate CNS Fails Charge (if CNS):**
Using cns-fails-charge.md:
| Age | Charge % | Daily Cost |
|-----|----------|------------|
| Days 1-4 | 5% | $[calculate] |
| Days 5-10 | 15% | $[calculate] |
| Days 11-20 | 20% | $[calculate] |
| Days 21+ | 100% | $[calculate] |

What is my CURRENT fails charge?

**Step 4 - Project Next Threshold:**
- Days until next haircut increase: [calculate]
- Projected deduction at next threshold: $[calculate]
- Total cumulative cost if not resolved: $[calculate]

**Step 5 - Break-Even Analysis:**
At what point does the cost of buy-in/resolution become less than continued capital charges?

**Step 6 - Recommend Action:**
Based on costs, what is the economically optimal resolution timing?
```

**Related:** [[aged-fail-deductions]] | [[cns-fails-charge]] | [[fail-charge-schedule]]

---

## 10. IMS Delivery Troubleshooting

**Use Case:** Diagnose why delivery isn't processing

```
Help me diagnose why my delivery isn't processing through IMS.

**Step 1 - Delivery Details:**
- CUSIP: [enter CUSIP]
- Quantity: [enter shares]
- Market Value: $[enter amount]
- Delivery Direction: [Deliver to / Receive from] [counterparty]
- Attempt Time: [enter time if known]

**Step 2 - Current Status:**
- IMS Profile: [Green / Yellow / Red / Unknown]
- Error or Status Message: [enter if known]
- Is this stuck behind other items? [Yes / No / Unknown]

**Step 3 - Check IMS Controls:**
Using ims-profiles.md and related docs, diagnose:

☐ **Profile Issue:**
- Green profile: Auto-skips blocked items (is something ahead of this blocking?)
- Yellow profile: Strict sequencing (is top item failing?)
- Red profile: Manual intervention required

☐ **Collateral Monitor:**
- Is there insufficient collateral causing a "chill"?

☐ **Net Debit Cap:**
- Would this delivery exceed the $2.15B individual limit?
- Or the $2.85B family limit?

☐ **RAD Threshold:**
- Is this delivery above counterparty's RAD limit?
- Requires receiver authorization?

☐ **Look-Ahead Gridlock:**
- Is this caught in circular dependency?
- Has mini-netting been attempted?

**Step 4 - Identify Root Cause:**
Based on checks above, what is blocking the delivery?

**Step 5 - Resolution Options:**
For each potential blocker, provide:
1. Profile change recommendation
2. SPP funding action (if liquidity issue)
3. Counterparty contact (if authorization needed)
4. Manual override process (if applicable)
```

**Related:** [[ims-profiles]] | [[collateral-monitor]] | [[net-debit-cap]] | [[rad-thresholds]] | [[look-ahead-process]]

---

## 11. Stock Loan Recall Processing

**Use Case:** Process an incoming recall and determine Reg SHO implications

```
Help me process a stock loan recall and determine my Reg SHO status.

**Step 1 - Recall Details:**
- Security CUSIP: [enter CUSIP]
- Quantity Recalled: [enter shares]
- Recall Notice Received: [enter date and time]
- Lender Name: [enter name]

**Step 2 - Determine Bona Fide Deadline:**
Using recalls.md:
- T+1 era deadline: **11:59 PM on Trade Date (T)**

Is my recall received before or after this deadline?
- Received BEFORE deadline: Bona fide recall → Deemed to Own eligible
- Received AFTER deadline: Late recall → Must mark as Short Sale

**Step 3 - Determine Order Marking:**
Based on recall timing:

| Recall Status | I Can Mark As | Close-Out Deadline |
|---------------|---------------|-------------------|
| Bona fide (on time) | LONG | Standard (no Reg SHO pressure) |
| Late | SHORT | S+1 (immediate close-out required) |
| No recall received | SHORT | S+1 (immediate close-out required) |

What should my order marking be?

**Step 4 - Assess Response Timeline:**
- Hours available to respond: [calculate from recall time to deadline]
- Is automation critical? (T+1 = ~12 hours vs T+2 = ~24 hours)

**Step 5 - Recommend Action:**
1. If bona fide: Process return, can sell position as Long if needed
2. If late: Immediately assess inventory for close-out
3. Contact stock loan desk: [talking points]
4. Escalation if cannot satisfy recall: [next steps]
```

**Related:** [[recalls]] | [[reg-sho-rule-204]] | [[fail-to-deliver]]

---

## 12. Reclaim Resolution Processing

**Use Case:** Process an incoming reclaim and resolve delivery reversal

```
Help me process and resolve a reclaim on an erroneous delivery.

**Step 1 - Reclaim Details:**
- CUSIP: [enter CUSIP]
- Quantity: [enter shares]
- Original Delivery Date: [enter date]
- Reclaim Reason Code: [enter code: 41-44 for DK, 45 for physical, 87-88 for timing]
- Counterparty: [enter name]

**Step 2 - Decode Reason Code:**
Using reclaim-reason-codes.md:

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| 41 | Unknown trade | Trade comparison issue |
| 42 | Wrong quantity | Quantity mismatch |
| 43 | Wrong price | Price mismatch |
| 44 | Wrong security | CUSIP error |
| 45 | Mutilated/Wrong certificate | Physical/data issue |
| 87 | Late delivery | Timing issue |
| 88 | Stale dated | Instruction expired |

What does my code mean and what caused it?

**Step 3 - Determine Reclaim Type:**
- Is this a MATCHED reclaim? (counterparty acknowledges the error)
  → RAD exempt, processes immediately
- Is this an UNMATCHED reclaim? (counterparty disputes)
  → Subject to RAD limits, may be blocked

**Step 4 - Check RAD Status (if unmatched):**
Using rad-thresholds.md:
- Is reclaim amount within RAD limits?
- If over threshold: requires receiver authorization

**Step 5 - Resolution Steps by Code:**

For DK codes (41-44):
1. Pull original trade details
2. Verify trade comparison
3. Amend [quantity/price/CUSIP] as needed
4. Resubmit corrected delivery

For Physical issue (45):
1. Request physical inspection details
2. Coordinate replacement delivery

For Timing issues (87-88):
1. Review delivery timing
2. Refresh instruction and resubmit

**Step 6 - Recommend Action:**
What specific correction is needed and who should I contact?
```

**Related:** [[reclaims]] | [[reclaim-reason-codes]] | [[dk-processing]] | [[rad-thresholds]]

---

## 13. Counterparty Outreach Communication

**Use Case:** Draft professional outreach to counterparty for fail resolution

```
Help me draft a counterparty outreach communication for fail resolution.

**Step 1 - Fail Details:**
- CUSIP: [enter CUSIP]
- Security Name: [enter name]
- Quantity: [enter shares]
- Settlement Date: [enter date]
- Age: [enter days]
- My Position: [I'm waiting to receive (FTR) / They're waiting to receive (FTD)]

**Step 2 - Counterparty Info:**
- Counterparty Name: [enter name]
- Contact Name (if known): [enter or "unknown"]
- Previous Contact Attempts: [None / [date and outcome]]

**Step 3 - Urgency Level:**
- Reg SHO deadline: [Not applicable / Approaching / Past due]
- Capital impact: [Low / Medium / High]
- Escalation level: [Standard / Elevated / Critical]

**Step 4 - Communication Purpose:**
What am I requesting?
- Status update on their delivery
- Request they prioritize this settlement
- Notify of pending buy-in
- Request SSI confirmation
- Resolve trade discrepancy
- Other: [specify]

**Step 5 - Draft Communication:**
Generate a professional email/message that includes:
- Clear subject line with CUSIP and urgency
- Brief background (trade details, current status)
- Specific ask (what action I need from them)
- Deadline (if applicable)
- Contact info for response

Tone: [Routine / Urgent / Escalation]

**Step 6 - Follow-Up Plan:**
- If no response within: [hours/days], then: [next action]
- Escalation contact if primary unresponsive
- Documentation requirements
```

**Related:** [[escalation-paths]] | [[buy-in-mechanics]]

---

## How to Use These Prompts

1. **Select the right prompt** from the Quick Reference Card based on your situation
2. **Copy the prompt template** and paste into Copilot
3. **Fill in the [bracketed] placeholders** with your specific fail data
4. **Review Copilot's response** and follow the recommended actions
5. **Iterate if needed** - add more details or ask follow-up questions

> [!tip] Pro Tips
> - Have your fail data ready before starting
> - Use exact values (CUSIP, dates, amounts) for accurate guidance
> - If Copilot's response seems incomplete, re-prompt with more context
> - Save frequently-used prompts as templates

---

## Related

- [[_INDEX]] - Main navigation
- [[new-fail-triage]] - Triage decision tree
- [[settlement-lifecycle]] - Full settlement flow
- [[_MOC-exceptions]] - Exception handling overview
