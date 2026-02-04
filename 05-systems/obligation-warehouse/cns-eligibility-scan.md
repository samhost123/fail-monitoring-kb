---
title: "CNS Eligibility Scan"
aliases: ["OW Rescue", "Eligibility Scan"]
tags:
  - system/ow
  - concept/process
created: 2026-02-03
status: final
source: "Raw research/Analyzing Obligation Warehouse Operations.md"
---

# CNS Eligibility Scan

Daily process to identify [[obligation-warehouse]] positions that have become CNS-eligible for "rescue" to CNS.

---

## Mechanism

```mermaid
flowchart LR
    OW["OW Position"]
    SCAN["Daily Eligibility Scan"]
    CHECK{CNS<br/>Eligible?}
    RESCUE["Move to CNS"]
    STAY["Remain in OW"]

    OW --> SCAN
    SCAN --> CHECK
    CHECK --> |Yes| RESCUE
    CHECK --> |No| STAY

    style OW fill:#f3e5f5
    style SCAN fill:#b2dfdb
    style CHECK fill:#b2dfdb
    style RESCUE fill:#c8e6c9
    style STAY fill:#e1bee7
```

---

## Eligibility Factors

| Factor | Requirement |
|--------|-------------|
| Security | CNS-eligible (registered) |
| Member | CNS participant |
| Trade type | Not explicitly ex-cleared |

---

## Rescue Benefits

| Benefit | Description |
|---------|-------------|
| CCP guarantee | NSCC backs position |
| [[netting]] | Join CNS netting |
| Capital | Net vs. gross treatment |
| Margin offset | Available in CNS |

---

## Timing

| Aspect | Detail |
|--------|--------|
| Frequency | Daily |
| Timing | Prior to [[night-cycle]] |
| Effect | Immediate CNS inclusion |

---

## Related
- [[obligation-warehouse]] - Source system
- [[cns-system]] - Destination system
- [[recaps]] - Alternative (stay in OW)
