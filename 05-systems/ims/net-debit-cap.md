---
title: "Net Debit Cap"
aliases: ["NDC", "Debit Cap"]
tags:
  - system/ims
  - concept/limit
created: 2026-02-03
status: final
source: "Raw research/Fin Ops IMS Equity Settlement Analysis.md"
---

# Net Debit Cap (NDC)

DTC liquidity limit constraining maximum net debit position during settlement.

---

## Limits

| Type | Limit |
|------|-------|
| Individual member | $2.15 billion |
| Family (affiliates) | $2.85 billion |

---

## Mechanism

```mermaid
flowchart TD
    DELIVERY["Delivery Request"]
    CALC["Calculate Post-Delivery<br/>Net Debit"]
    CHECK{Within NDC?}
    PROCEED["Proceed"]
    BLOCK["Block Until<br/>Cash Received"]
    SPP["[[settlement-progress-payment|SPP]] Option"]

    DELIVERY --> CALC
    CALC --> CHECK
    CHECK --> |Yes| PROCEED
    CHECK --> |No| BLOCK
    BLOCK --> SPP

    style DELIVERY fill:#bbdefb
    style CALC fill:#b2dfdb
    style CHECK fill:#b2dfdb
    style PROCEED fill:#c8e6c9
    style BLOCK fill:#ffcdd2
    style SPP fill:#fff3e0
```

---

## NDC vs. Collateral Monitor

| Aspect | [[collateral-monitor\|CM]] | NDC |
|--------|-----|-----|
| Purpose | Solvency | Liquidity |
| Constraint | Collateral value | Cash flow |
| Threshold | Value-based | Dollar cap |

---

## Approaching NDC

| Action | Purpose |
|--------|---------|
| [[settlement-progress-payment\|SPP]] | Release cash via Fedwire |
| Delay deliveries | Reduce outflows |
| Prioritize receipts | Increase inflows |

---

## Related
- [[ims-profiles]] - IMS profile system
- [[collateral-monitor]] - Solvency constraint
- [[settlement-progress-payment]] - Liquidity release
- [[look-ahead-process]] - Gridlock resolution
