---
title: "Novation"
aliases: ["CCP Transformation"]
tags:
  - system/cns
  - concept/legal
created: 2026-02-03
status: final
source: "Raw research/Fin Ops Analysis_ CNS Settlement Workflow.md"
---

# Novation

Legal transformation of bilateral trade obligations into CCP-guaranteed obligations through NSCC.

---

## Transformation

```mermaid
flowchart LR
    subgraph BEFORE["Before Novation"]
        A1["Party A"] <-->|"Bilateral<br/>Contract"| B1["Party B"]
    end

    subgraph AFTER["After Novation"]
        A2["Party A"] <-->|"Guaranteed"| CCP["NSCC<br/>(CCP)"]
        CCP <-->|"Guaranteed"| B2["Party B"]
    end

    BEFORE --> |Novation| AFTER

    style A1 fill:#fff3e0
    style B1 fill:#fff3e0
    style A2 fill:#c8e6c9
    style B2 fill:#c8e6c9
    style CCP fill:#b2dfdb
```

| Aspect | Before | After |
|--------|--------|-------|
| Counterparty | Known (Party B) | Anonymous (NSCC) |
| Guarantee | None | CCP guarantee |
| Default risk | Direct exposure | Loss mutualization |
| Settlement | Bilateral | Centralized |

---

## Benefits

| Benefit | Description |
|---------|-------------|
| Anonymity | Trading counterparty hidden |
| Guarantee | NSCC backs all positions |
| [[netting]] | 98% gross-to-net reduction |
| Capital efficiency | Net exposure only |
| Margin offsets | Long/short position offsets |

---

## Timing

| Event | Timing |
|-------|--------|
| Trade execution | T |
| Trade comparison | T (real-time) |
| Novation | Upon comparison match |
| Settlement | T+1 |

---

## Legal Effect

> [!info] Contract Replacement
> Original bilateral contract is extinguished and replaced with two separate contracts: Party A ↔ NSCC and NSCC ↔ Party B.

---

## Related
- [[cns-system]] - CNS architecture
- [[netting]] - Post-novation netting
- [[obligation-warehouse]] - Non-novated alternative
