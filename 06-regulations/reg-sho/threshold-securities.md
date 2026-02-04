---
title: "Threshold Securities"
aliases: ["Threshold List", "Rule 203"]
tags:
  - regulation/reg-sho
  - lifecycle/fail
created: 2026-02-03
status: final
source: "Raw research/Regulation SHO FinOps Analysis.md"
---

# Threshold Securities

Securities with significant aggregate fail-to-deliver positions. Subject to mandatory 13-day close-out.

---

## Threshold Criteria

| Criterion | Requirement |
|-----------|-------------|
| FTD quantity | ≥ 10,000 shares |
| FTD percentage | ≥ 0.5% of shares outstanding |
| Duration | 5 consecutive settlement days |

---

## 13-Day Rule

```mermaid
flowchart LR
    subgraph STANDARD["Standard Close-Out"]
        S1["S<br/>Settlement"]
        S2["S+1<br/>Short Close-Out"]
        S3["S+3<br/>Long Close-Out"]
    end

    subgraph THRESHOLD["Threshold Security"]
        T1["S<br/>Settlement"]
        T2["S+1 to S+12<br/>Resolution Efforts"]
        T3["S+13<br/>Mandatory Purchase"]
    end

    S1 --> S2 --> S3
    T1 --> T2 --> T3

    style S2 fill:#fff3e0
    style S3 fill:#fff3e0
    style T2 fill:#bbdefb
    style T3 fill:#ffcdd2
```

> [!danger] Mandatory Purchase
> Day 13 requires **purchase** - borrow does NOT satisfy requirement.

| Day | Requirement |
|-----|-------------|
| 1-12 | Standard resolution efforts |
| 13 | Mandatory purchase |
| Post-13 | Continued [[penalty-box]] + regulatory scrutiny |

---

## Threshold List Sources

Each SRO (Self-Regulatory Organization) publishes its own threshold list for securities traded on their exchange.

### FINRA Threshold List
| Aspect | Detail |
|--------|--------|
| Publisher | FINRA |
| Frequency | Daily (by 4:00 PM ET) |
| URL | `https://www.finra.org/finra-data/short-sale-volume-data` |
| Coverage | OTC securities, ADF-reported |
| Format | CSV |

### NYSE Threshold List
| Aspect | Detail |
|--------|--------|
| Publisher | NYSE |
| Frequency | Daily |
| URL | `https://www.nyse.com/regulation/threshold-securities` |
| Coverage | NYSE-listed securities |
| Format | CSV/Excel |

### NASDAQ Threshold List
| Aspect | Detail |
|--------|--------|
| Publisher | NASDAQ |
| Frequency | Daily |
| URL | `https://www.nasdaqtrader.com/Trader.aspx?id=RegSHOThreshold` |
| Coverage | NASDAQ-listed securities |
| Format | Text file |

### CBOE Threshold List
| Aspect | Detail |
|--------|--------|
| Publisher | CBOE |
| Frequency | Daily |
| URL | `https://www.cboe.com/us/equities/regulation/regsho/` |
| Coverage | CBOE BZX/BYX/EDGX/EDGA traded |
| Format | CSV |

### Aggregation Requirement
| Aspect | Detail |
|--------|--------|
| Consolidation | Must check ALL lists daily |
| Timing | Before market open |
| Action | Flag any CUSIP on ANY list |

---

## Impact

| Aspect | Threshold vs. Non-Threshold |
|--------|----------------------------|
| Close-out | S+13 mandatory | S+1/S+3 |
| Resolution | Purchase only | Borrow acceptable |
| Scrutiny | High | Standard |
| Prioritization | Critical | Per [[prioritization-logic]] |

---

## Monitoring Integration

| Action | System |
|--------|--------|
| Daily list check | Compliance |
| Auto-flag positions | [[new-fail-triage]] |
| Critical priority | [[prioritization-logic]] |
| Immediate escalation | [[escalation-paths]] |

---

## Related
- [[reg-sho-rule-204]] - Close-out requirements
- [[penalty-box]] - Restriction mechanics
- [[prioritization-logic]] - Regulatory factor = Critical
- [[close-out-matrix]] - Timeline reference
