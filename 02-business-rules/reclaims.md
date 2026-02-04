---
title: "Reclaims"
aliases: ["Reclaim", "Delivery Reversal"]
tags:
  - lifecycle/exception
  - system/dtc
created: 2026-02-03
status: final
source: "Raw research/Settlement Exception Processing Analysis.md"
---

# Reclaims

Reversal of erroneous deliveries. Treated as new delivery instruction subject to RAD controls.

---

## Reclaim Flow

```mermaid
flowchart TD
    ERROR["Erroneous Delivery"]
    RECLAIM["Reclaim Submitted"]
    TYPE{Matched?}
    MATCHED["Matched Reclaim<br/>(RAD Exempt)"]
    UNMATCHED["Unmatched Reclaim<br/>(Subject to RAD)"]
    PROCESS["Process as Delivery"]
    CHECK{Within RAD?}
    PROCEED["Proceed"]
    AUTHORIZE["Await Authorization"]

    ERROR --> RECLAIM
    RECLAIM --> TYPE
    TYPE --> |Yes| MATCHED
    TYPE --> |No| UNMATCHED
    MATCHED --> PROCESS
    UNMATCHED --> CHECK
    CHECK --> |Yes| PROCESS
    CHECK --> |No| AUTHORIZE
    PROCESS --> PROCEED

    style ERROR fill:#ffcdd2
    style RECLAIM fill:#fff3e0
    style TYPE fill:#b2dfdb
    style MATCHED fill:#c8e6c9
    style UNMATCHED fill:#fff3e0
    style PROCESS fill:#bbdefb
    style CHECK fill:#b2dfdb
    style PROCEED fill:#c8e6c9
    style AUTHORIZE fill:#fff3e0
```

---

## Reclaim Types

| Code | Type | Description |
|------|------|-------------|
| 41-44 | DK Reclaims | Counterparty doesn't recognize |
| 45 | Mutilated/Wrong | Physical/data issue |
| 87-88 | Late/Stale | Timing issues |

See [[reclaim-reason-codes]] for full reference.

---

## Matched vs. Unmatched

| Aspect | Matched | Unmatched |
|--------|---------|-----------|
| Counterparty | Acknowledges | Disputes/unknown |
| RAD | Exempt | Subject to limits |
| Processing | Immediate | May be blocked |

---

## RAD Interaction

See [[rad-thresholds]] for limits.

| Scenario | RAD Treatment |
|----------|---------------|
| Matched reclaim | Exempt |
| Unmatched reclaim | Subject to RAD |
| Over threshold | Requires authorization |

---

## Decoupling Initiative

> [!info] Q3 2027
> DTCC decoupling initiative will decommission systemic linking between reclaims and original delivery.

| Current | Post-Decoupling |
|---------|-----------------|
| Linked to original | Independent instruction |
| Automatic pairing | Manual reconciliation |

---

## Related
- [[_MOC-exceptions]] - Exception overview
- [[reclaim-reason-codes]] - Code reference
- [[rad-thresholds]] - RAD controls
- [[dk-processing]] - Related exception
- [[recalls]] - Different exception type
