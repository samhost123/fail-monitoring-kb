---
title: "Day Cycle"
aliases: ["Day Cycle Allocation", "Settlement Day Processing"]
tags:
  - system/cns
  - lifecycle/settlement
created: 2026-02-03
status: final
source: "Raw research/Fin Ops Analysis_ CNS Settlement Workflow.md"
---

# Day Cycle

Continuous CNS allocation on settlement date. Processes positions not filled in [[night-cycle]].

---

## Timeline

| Time | Event |
|------|-------|
| 6:00 AM ET | Day Cycle start |
| Continuous | Recycling as inventory arrives |
| 3:00 PM ET | Settlement cutoff |
| 3:30 PM ET | Money settlement finality |

---

## Processing Logic

```mermaid
flowchart TD
    UNFILLED["Unfilled from Night Cycle"]
    INVENTORY["New Inventory Arrives"]
    RECYCLE["Recycling Engine"]

    subgraph CONTINUOUS["Continuous Processing"]
        CHECK{Inventory<br/>Available?}
        ALLOC["Allocate per Priority Groups"]
        WAIT["Wait for Next Receipt"]
    end

    CUTOFF["3:00 PM Cutoff"]
    FAIL["Fail Established"]
    SETTLE["Settlement Complete"]

    UNFILLED --> CONTINUOUS
    INVENTORY --> CONTINUOUS
    CHECK --> |Yes| ALLOC
    CHECK --> |No| WAIT
    ALLOC --> SETTLE
    WAIT --> CHECK
    CUTOFF --> FAIL

    style UNFILLED fill:#fff3e0
    style INVENTORY fill:#bbdefb
    style RECYCLE fill:#b2dfdb
    style CHECK fill:#b2dfdb
    style ALLOC fill:#b2dfdb
    style WAIT fill:#fff3e0
    style CUTOFF fill:#ffcdd2
    style FAIL fill:#ffcdd2
    style SETTLE fill:#c8e6c9
```

---

## Key Characteristics

| Aspect | Day Cycle |
|--------|-----------|
| Processing | Continuous (not batch) |
| Trigger | Inventory arrival |
| Priority | Same [[priority-groups]] |
| Duration | 6:00 AM - 3:00 PM ET |

---

## Inventory Sources

| Source | Description |
|--------|-------------|
| Inbound deliveries | Counterparty settlements |
| Recalls returned | [[recalls]] satisfied |
| Borrows | [[stock-borrow-program]] |
| Purchases | Market acquisitions |

---

## Fail Establishment

> [!warning] 3:00 PM Cutoff
> Positions not settled by 3:00 PM ET become official fails. [[cns-fails-charge]] clock starts.

| Pre-Cutoff | Post-Cutoff |
|------------|-------------|
| Position pending | Fail recorded |
| No charge | Charge accrues |
| Settlement possible | Next day earliest |

---

## Related
- [[cns-system]] - CNS architecture
- [[night-cycle]] - Prior cycle
- [[priority-groups]] - Allocation hierarchy
- [[cns-fails-charge]] - Post-fail charges
- [[settlement-lifecycle]] - Node 4 (Day Cycle)
