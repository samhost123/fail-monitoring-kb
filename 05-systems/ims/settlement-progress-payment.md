---
title: "Settlement Progress Payment"
aliases: ["SPP", "Intraday Liquidity"]
tags:
  - system/ims
  - concept/liquidity
created: 2026-02-03
status: final
source: "Raw research/Fin Ops IMS Equity Settlement Analysis.md"
---

# Settlement Progress Payment (SPP)

Intraday Fedwire mechanism to release cash and avoid [[net-debit-cap]] constraints.

---

## Mechanism

```mermaid
flowchart LR
    NDC["Approaching NDC"]
    SPP["SPP Request"]
    FEDWIRE["Fedwire Payment"]
    RELEASE["Cash Released to DTC"]
    CONTINUE["Settlement Continues"]

    NDC --> SPP
    SPP --> FEDWIRE
    FEDWIRE --> RELEASE
    RELEASE --> CONTINUE

    style NDC fill:#ffcdd2
    style SPP fill:#fff3e0
    style FEDWIRE fill:#bbdefb
    style RELEASE fill:#c8e6c9
    style CONTINUE fill:#c8e6c9
```

---

## Trigger Conditions

| Condition | Action |
|-----------|--------|
| Net debit approaching NDC | Consider SPP |
| High-priority deliveries blocked | Request SPP |
| End-of-day settlement push | SPP to clear backlog |

---

## Characteristics

| Aspect | Detail |
|--------|--------|
| Mechanism | Fedwire payment |
| Timing | Intraday |
| Purpose | Release cash to DTC |
| Effect | Reduce net debit position |

---

## Related
- [[ims-profiles]] - IMS profile system
- [[net-debit-cap]] - NDC constraint
- [[collateral-monitor]] - Solvency check
- [[look-ahead-process]] - Alternative resolution
