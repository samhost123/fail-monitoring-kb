---
title: "CNS Fails Charge"
aliases: ["Fails Charge", "Duration-Based Penalty"]
tags:
  - regulation/nscc
  - lifecycle/fail
  - python/formula
created: 2026-02-03
status: final
source: "Raw research/Regulation SHO FinOps Analysis.md"
---

# CNS Fails Charge

Duration-based penalty charged to failing members. 2025 revision eliminated CRRM-based calculation.

---

## Charge Schedule

```mermaid
flowchart LR
    D1["Days 1-4<br/>5%"] --> D5["Days 5-10<br/>15%"] --> D11["Days 11-20<br/>20%"] --> D21["Days 21+<br/>100%"]

    style D1 fill:#c8e6c9
    style D5 fill:#fff3e0
    style D11 fill:#ffcdd2
    style D21 fill:#b71c1c,color:#fff
```

| Age (Days) | Rate | Example ($1M CMV) |
|------------|------|-------------------|
| 1-4 | 5% | $50,000 |
| 5-10 | 15% | $150,000 |
| 11-20 | 20% | $200,000 |
| 21+ | 100% | $1,000,000 |

---

## Calculation

```
Daily Charge = CMV × Aging Factor
```

| Variable | Definition |
|----------|------------|
| CMV | Current Market Value |
| Aging Factor | Rate from schedule above |

---

## 2025 Revision

| Aspect | Previous | Current |
|--------|----------|---------|
| Basis | CRRM (risk-based) | Duration (age-based) |
| Complexity | Variable | Fixed schedule |
| Predictability | Lower | Higher |

---

## Charge Trigger

| Event | Timing |
|-------|--------|
| Fail established | 3:00 PM ET cutoff |
| Charge starts | Day 1 |
| Daily accrual | Each fail day |

---

## Mitigation

| Action | Effect |
|--------|--------|
| Deliver shares | Stop accrual |
| [[partial-settlement]] | Reduce base CMV |
| [[stock-borrow-program\|SBP]] | Cover position |
| [[buy-in-mechanics\|Buy-in]] | Force resolution |

---

## Related
- [[cns-system]] - CNS architecture
- [[aged-fail-deductions]] - Additional capital impact
- [[settlement-lifecycle]] - Node 5 (Fail Established)
- [[fail-to-deliver]] - FTD lifecycle
- [[prioritization-logic]] - Cost in prioritization
