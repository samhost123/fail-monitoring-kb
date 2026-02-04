---
title: "Partial Settlement"
aliases: ["Partial Delivery"]
tags:
  - system/cns
  - lifecycle/settlement
created: 2026-02-03
status: final
source: "Raw research/Fin Ops Analysis_ CNS Settlement Workflow.md"
---

# Partial Settlement

Delivery of available shares when full quantity unavailable. Reduces fail magnitude incrementally.

---

## Mechanism

```mermaid
flowchart LR
    OBLIGATION["Obligation: 1,000 shares"]
    AVAILABLE["Available: 600 shares"]

    subgraph PARTIAL["Partial Settlement"]
        DELIVER["Deliver: 600 shares"]
        REMAIN["Remaining: 400 shares"]
    end

    OBLIGATION --> PARTIAL
    AVAILABLE --> PARTIAL
    REMAIN --> FAIL["Continue as Fail"]

    style OBLIGATION fill:#bbdefb
    style AVAILABLE fill:#fff3e0
    style DELIVER fill:#c8e6c9
    style REMAIN fill:#ffcdd2
    style FAIL fill:#ffcdd2
```

| Component | Shares |
|-----------|--------|
| Original obligation | 1,000 |
| Partial delivery | 600 |
| Remaining fail | 400 |

---

## Benefits

| Benefit | Description |
|---------|-------------|
| Reduced exposure | Smaller fail balance |
| Counterparty credit | Partial receives |
| [[cns-fails-charge]] | Charges on remainder only |

---

## Processing

| Timing | Action |
|--------|--------|
| [[day-cycle]] | Continuous partial delivery |
| End of day | Remaining becomes fail |
| Next day | Rolls into [[night-cycle]] |

---

## Related
- [[cns-system]] - CNS architecture
- [[day-cycle]] - Processing timing
- [[stock-borrow-program]] - Alternative mitigation
- [[cns-fails-charge]] - Cost on remainder
