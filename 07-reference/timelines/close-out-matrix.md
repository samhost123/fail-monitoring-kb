---
title: "Close-Out Matrix"
aliases: ["Reg SHO Deadlines", "Close-Out Deadlines"]
tags:
  - reference/timeline
  - regulation/reg-sho
created: 2026-02-03
status: final
source: "Raw research/Regulation SHO FinOps Analysis.md"
---

# Close-Out Matrix

Quick reference for all Reg SHO close-out deadlines.

---

## Standard Close-Outs

| Position Type | Deadline | Timing | Consequence |
|---------------|----------|--------|-------------|
| **Short sale** | S+1 | Market open (9:30 AM) | [[penalty-box]] |
| **Long sale** | S+3 | Market open (9:30 AM) | [[penalty-box]] |
| **Market maker** | S+3 | Extended | [[penalty-box]] |
| **[[threshold-securities\|Threshold]]** | S+13 | Intraday | Mandatory purchase |

---

## Visual Timeline

```mermaid
flowchart LR
    subgraph SHORT["Short Sale"]
        SS["S"] --> S1["S+1<br/>Close-Out"]
    end

    subgraph LONG["Long Sale"]
        LS["S"] --> G["S+1 to S+2<br/>Grace"] --> L3["S+3<br/>Close-Out"]
    end

    subgraph THRESH["Threshold Security"]
        TS["S"] --> TC["S+1 to S+12<br/>Consecutive"] --> T13["S+13<br/>Purchase"]
    end

    style S1 fill:#ffcdd2
    style L3 fill:#ffcdd2
    style TC fill:#bbdefb
    style T13 fill:#ffcdd2
```

---

## Capital Deduction Timeline

| Age | Deduction | Reference |
|-----|-----------|-----------|
| S+5 | Begins | [[aged-fail-deductions]] |
| S+7 | 15% | [[aged-fail-deductions]] |
| S+14 | 25% | [[aged-fail-deductions]] |
| S+21 | 100% | [[aged-fail-deductions]] |

---

## Resolution Requirements

| Deadline | Acceptable Resolution |
|----------|----------------------|
| S+1/S+3 | "Cleared and settled" delivery |
| S+13 (Threshold) | **Purchase only** (borrow NOT acceptable) |

---

## Related
- [[reg-sho-rule-204]] - Full rule details
- [[penalty-box]] - Consequence of miss
- [[threshold-securities]] - 13-day rule
- [[t1-critical-deadlines]] - All deadlines
