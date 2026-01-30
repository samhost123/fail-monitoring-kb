# Escalation Paths

## Overview
Defines when and how to escalate fail issues to appropriate parties.

## Escalation Matrix

```
                         ┌─────────────────────────────────────────┐
                         │           ESCALATION LEVELS             │
                         ├─────────┬─────────┬─────────┬───────────┤
                         │ Level 1 │ Level 2 │ Level 3 │ Level 4   │
                         │ Ops     │ Senior  │ Mgmt    │ Compliance│
                         │ Analyst │ Ops     │         │ /Legal    │
┌────────────────────────┼─────────┼─────────┼─────────┼───────────┤
│ Age > 10 days          │    ✓    │         │         │           │
│ Age > 13 days          │         │    ✓    │         │           │
│ Age > 20 days          │         │         │    ✓    │           │
│ Age > 30 days          │         │         │         │     ✓     │
├────────────────────────┼─────────┼─────────┼─────────┼───────────┤
│ Value > $1M            │    ✓    │         │         │           │
│ Value > $5M            │         │    ✓    │         │           │
│ Value > $10M           │         │         │    ✓    │           │
├────────────────────────┼─────────┼─────────┼─────────┼───────────┤
│ Threshold security     │         │    ✓    │         │           │
│ Close-out required     │         │         │    ✓    │           │
│ Regulatory inquiry     │         │         │         │     ✓     │
└────────────────────────┴─────────┴─────────┴─────────┴───────────┘
```

## Escalation Procedures

### Level 1: Operations Analyst
**Trigger:** Standard fail requiring attention
**Actions:**
1. Review fail details
2. Contact counterparty
3. Identify resolution path
4. Document actions taken

### Level 2: Senior Operations
**Trigger:** Elevated risk or unresolved Level 1
**Actions:**
1. Review analyst actions
2. Direct counterparty escalation
3. Evaluate offset opportunities
4. Initiate borrow if needed

### Level 3: Management
**Trigger:** Significant exposure or regulatory deadline
**Actions:**
1. Approve close-out purchases
2. Authorize extraordinary measures
3. Notify risk management
4. Prepare for regulatory reporting

### Level 4: Compliance/Legal
**Trigger:** Regulatory violation imminent or inquiry received
**Actions:**
1. Prepare regulatory response
2. Document compliance efforts
3. Engage legal counsel if needed
4. File required reports

## Notification Templates

### Email Subject Lines
- L1: `[FAIL ALERT] {CUSIP} - {Counterparty} - Age {N} days`
- L2: `[URGENT] Fail Escalation - {CUSIP} - ${Value}M`
- L3: `[CRITICAL] Management Review Required - {CUSIP}`
- L4: `[COMPLIANCE] Regulatory Action Required - {CUSIP}`

## Response SLAs

| Level | Initial Response | Resolution Target |
|-------|------------------|-------------------|
| 1 | 4 hours | 2 business days |
| 2 | 2 hours | 1 business day |
| 3 | 1 hour | Same day |
| 4 | 30 minutes | Immediate |
