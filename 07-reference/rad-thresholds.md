---
title: "RAD Thresholds"
aliases: ["Receiver Authorized Delivery", "RAD"]
tags:
  - reference/limits
  - system/ims
created: 2026-02-03
status: final
source: "Raw research/Fin Ops IMS Equity Settlement Analysis.md"
---

# RAD Thresholds

Receiver Authorized Delivery limits controlling large incoming deliveries.

---

## Purpose

| Function | Description |
|----------|-------------|
| Prevent "dumping" | Block unwanted large deliveries |
| Balance sheet control | Receiver controls exposure |
| Authorization | Large deliveries need approval |

---

## Threshold Structure

| Category | Typical Limit |
|----------|---------------|
| Per-security | Member-defined |
| Per-counterparty | Member-defined |
| Daily aggregate | Member-defined |

> [!info] Member-Configured
> Each member sets own RAD thresholds based on risk appetite.

---

## RAD Behavior

```mermaid
flowchart TD
    DELIVERY["Incoming Delivery"]
    CHECK{Within RAD?}
    PROCEED["Auto-Accept"]
    HOLD["Hold for Authorization"]
    AUTHORIZE{Approved?}
    ACCEPT["Accept"]
    REJECT["Reject"]

    DELIVERY --> CHECK
    CHECK --> |Yes| PROCEED
    CHECK --> |No| HOLD
    HOLD --> AUTHORIZE
    AUTHORIZE --> |Yes| ACCEPT
    AUTHORIZE --> |No| REJECT

    style DELIVERY fill:#bbdefb
    style CHECK fill:#b2dfdb
    style PROCEED fill:#c8e6c9
    style HOLD fill:#fff3e0
    style AUTHORIZE fill:#b2dfdb
    style ACCEPT fill:#c8e6c9
    style REJECT fill:#ffcdd2
```

---

## Exemptions

| Scenario | RAD Applied? |
|----------|--------------|
| Matched [[reclaims]] | Exempt |
| Unmatched reclaims | Subject to RAD |
| Regular deliveries | Subject to RAD |

---

## Related
- [[ims-profiles]] - IMS profile system
- [[reclaims]] - Reclaim RAD behavior
- [[collateral-monitor]] - Complementary control
