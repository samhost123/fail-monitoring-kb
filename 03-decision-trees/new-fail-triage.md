# New Fail Triage

## Overview
Decision tree for processing newly identified fails.

## Triage Flow

```
                    ┌─────────────────┐
                    │  New Fail Alert │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Is it a valid   │
                    │ fail? (not a    │───No──→ [Mark as False Positive]
                    │ data error)     │
                    └────────┬────────┘
                             │ Yes
                             ▼
                    ┌─────────────────┐
                    │ Is security on  │
                    │ Threshold List? │───Yes──→ [Flag as Threshold]
                    └────────┬────────┘                    │
                             │ No                          │
                             ▼                             │
                    ┌─────────────────┐                    │
                    │ Is fail value   │                    │
                    │ > $1M?          │───Yes──→ [High Value Flag] ◄─┘
                    └────────┬────────┘                    │
                             │ No                          │
                             ▼                             │
                    ┌─────────────────┐                    │
                    │ Known problem   │                    │
                    │ counterparty?   │───Yes──→ [Escalate to Supervisor]
                    └────────┬────────┘                    │
                             │ No                          │
                             ▼                             ▼
                    ┌─────────────────┐         ┌─────────────────┐
                    │ Calculate       │         │ Calculate       │
                    │ Priority Score  │         │ Priority Score  │
                    └────────┬────────┘         └────────┬────────┘
                             │                           │
                             ▼                           ▼
                    ┌─────────────────┐         ┌─────────────────┐
                    │ Add to Monitor  │         │ Add to Critical │
                    │ Queue           │         │ Queue           │
                    └─────────────────┘         └─────────────────┘
```

## Validation Checks

### Data Quality
- [ ] CUSIP exists in security master
- [ ] Quantity is positive integer
- [ ] Settlement date is valid business day
- [ ] Counterparty exists in reference data

### Duplicate Detection
- [ ] Not already in fail inventory
- [ ] Not a reversal of existing fail
- [ ] Not a corporate action adjustment

## Initial Actions

| Condition | Immediate Action |
|-----------|------------------|
| Valid fail | Create fail record |
| Threshold security | Add regulatory flag |
| High value | Notify senior ops |
| Problem CP | Auto-escalate |

## System Updates
1. Create fail record in database
2. Calculate initial priority score
3. Assign to appropriate queue
4. Send notifications as needed
5. Log triage decision and rationale
