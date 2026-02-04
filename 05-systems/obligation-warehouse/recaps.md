---
title: "RECAPS"
aliases: ["Reconfirmation and Pricing Service", "Mark-to-Market"]
tags:
  - system/ow
  - concept/process
created: 2026-02-03
status: final
source: "Raw research/Analyzing Obligation Warehouse Operations.md"
---

# RECAPS

Reconfirmation and Pricing Service - mark-to-market cycle for [[obligation-warehouse]] positions.

---

## Mechanism

```mermaid
flowchart LR
    POSITION["OW Position<br/>Original Price: $100"]
    RECAPS["RECAPS Cycle"]
    CURRENT["Current Price: $105"]

    subgraph ADJUSTMENT["Adjustment"]
        DIFF["Difference: $5"]
        CASH["Cash Payment"]
        RESET["Price Reset to $105"]
    end

    POSITION --> RECAPS
    CURRENT --> RECAPS
    RECAPS --> ADJUSTMENT

    style POSITION fill:#f3e5f5
    style RECAPS fill:#e1bee7
    style CURRENT fill:#bbdefb
    style DIFF fill:#fff3e0
    style CASH fill:#c8e6c9
    style RESET fill:#e1bee7
```

---

## Cycle Frequency

| Historical | Current Trend |
|------------|---------------|
| Quarterly | Monthly/biweekly |

> [!info] Increased Frequency
> RECAPS frequency has increased to force more frequent realization of gains/losses.

---

## Process

| Step | Action |
|------|--------|
| 1 | Identify OW positions |
| 2 | Determine current market price |
| 3 | Calculate difference from book price |
| 4 | Cash adjustment (payment/receipt) |
| 5 | Reset position to current price |

---

## Risk Implications

| Risk | Description |
|------|-------------|
| Mark-to-market loss | Cash outflow on price increase (short) |
| Counterparty default | Clawback risk before settlement |
| Liquidity | Cash requirement on repricing |

---

## Related
- [[obligation-warehouse]] - Parent system
- [[cns-eligibility-scan]] - Alternative (CNS rescue)
- [[dk-processing]] - Position validation
