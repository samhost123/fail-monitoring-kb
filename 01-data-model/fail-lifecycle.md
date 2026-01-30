# Fail Lifecycle

## Overview
Documents the states and transitions a fail moves through from creation to resolution.

## Fail States

```
┌─────────────┐
│   PENDING   │  Trade expected to settle
└──────┬──────┘
       │ Settlement date passes without delivery
       ▼
┌─────────────┐
│    OPEN     │  Active fail, being monitored
└──────┬──────┘
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
┌─────────────┐                        ┌─────────────┐
│  ESCALATED  │  Requires attention    │   OFFSET    │  Matched against opposite fail
└──────┬──────┘                        └──────┬──────┘
       │                                      │
       ▼                                      ▼
┌─────────────┐                        ┌─────────────┐
│   CLOSED    │  Resolved              │   CLOSED    │
└─────────────┘                        └─────────────┘
```

## State Definitions

| State | Description | Exit Criteria |
|-------|-------------|---------------|
| PENDING | Trade has not yet reached settlement date | Settlement date arrives |
| OPEN | Fail is active, settlement did not occur | Resolution or escalation |
| ESCALATED | Fail requires manual intervention | Resolution |
| OFFSET | Fail has been matched for netting | Netting completion |
| CLOSED | Fail has been resolved | N/A (terminal state) |

## Aging Rules
- **Day 1-3:** Standard monitoring
- **Day 4-9:** Increased priority
- **Day 10+:** Escalation required (Reg SHO)
- **Day 13+:** Mandatory close-out

## Transition Triggers
1. **PENDING → OPEN:** Settlement date passes without settlement confirmation
2. **OPEN → ESCALATED:** Aging threshold exceeded or manual flag
3. **OPEN → OFFSET:** Matching opposite fail identified
4. **ESCALATED → CLOSED:** Manual resolution confirmed
5. **OFFSET → CLOSED:** Netting cycle completes
