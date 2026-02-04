---
title: "Netting"
aliases: ["Continuous Netting", "Multilateral Netting"]
tags:
  - system/cns
  - concept/process
created: 2026-02-03
status: final
source: "Raw research/Fin Ops Analysis_ CNS Settlement Workflow.md"
---

# Netting

Continuous reduction of gross settlement obligations to net positions. CNS achieves ~98% gross-to-net reduction.

---

## Netting Process

```mermaid
flowchart TD
    subgraph GROSS["Gross Obligations"]
        BUY1["Buy: 1,000 shares"]
        BUY2["Buy: 500 shares"]
        SELL1["Sell: 800 shares"]
        SELL2["Sell: 400 shares"]
    end

    subgraph CALC["Netting Calculation"]
        TOTAL_BUY["Total Buy: 1,500"]
        TOTAL_SELL["Total Sell: 1,200"]
        NET["Net: Long 300"]
    end

    subgraph RESULT["Net Obligation"]
        FINAL["Receive 300 shares"]
    end

    GROSS --> CALC
    CALC --> RESULT

    style BUY1 fill:#c8e6c9
    style BUY2 fill:#c8e6c9
    style SELL1 fill:#ffcdd2
    style SELL2 fill:#ffcdd2
    style TOTAL_BUY fill:#c8e6c9
    style TOTAL_SELL fill:#ffcdd2
    style NET fill:#b2dfdb
    style FINAL fill:#a5d6a7
```

| Metric | Value |
|--------|-------|
| Gross obligations | 2,700 shares |
| Net obligation | 300 shares |
| Reduction | 89% |
| Typical CNS average | ~98% |

---

## Netting Components

### Settling Trades
| Source | Timing |
|--------|--------|
| New trades | T+0 comparison |
| Compared | Matched trades |

### Closing Positions
| Source | Timing |
|--------|--------|
| Prior day fails | Rolled forward |
| Resubmitted | After processing |

---

## Financial Impact

| Aspect | Gross | Net |
|--------|-------|-----|
| Deliveries | Each trade | Net position |
| Payments | Each trade | Net payment |
| Balance sheet | Sum of trades | Net exposure |
| Capital | Gross exposure | Net exposure |

---

## Netting Cycles

| Cycle | Timing | Purpose |
|-------|--------|---------|
| Intraday | Continuous | Real-time netting |
| [[night-cycle]] | 11:30 PM ET | End-of-day positions |
| [[day-cycle]] | 6:00 AM - 3:00 PM | Settlement day |

---

## Related
- [[cns-system]] - CNS architecture
- [[novation]] - Pre-netting transformation
- [[night-cycle]] - Night netting cycle
- [[day-cycle]] - Day netting cycle
