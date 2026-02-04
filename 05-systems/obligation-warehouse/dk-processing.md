---
title: "DK Processing"
aliases: ["Don't Know", "Trade Rejection"]
tags:
  - system/ow
  - lifecycle/exception
created: 2026-02-03
status: final
source: "Raw research/Analyzing Obligation Warehouse Operations.md"
---

# DK Processing

"Don't Know" resolution for trades where counterparty doesn't recognize the obligation.

---

## DK Flow

```mermaid
flowchart TD
    TRADE["Trade Submitted"]
    MATCH{"Counterparty<br/>Confirms?"}
    MATCHED["Matched<br/>(Settlement Path)"]
    DK["DK Status"]
    INVESTIGATE["Middle Office<br/>Investigation"]

    subgraph RESOLUTION["Resolution"]
        AMEND["Amendment"]
        CANCEL["Cancellation"]
        CONFIRM["Counterparty Confirms"]
    end

    RESUBMIT["Resubmit"]

    TRADE --> MATCH
    MATCH --> |Yes| MATCHED
    MATCH --> |No/Reject| DK
    DK --> INVESTIGATE
    INVESTIGATE --> RESOLUTION
    RESOLUTION --> RESUBMIT

    style TRADE fill:#bbdefb
    style MATCH fill:#b2dfdb
    style MATCHED fill:#c8e6c9
    style DK fill:#ffcdd2
    style INVESTIGATE fill:#fff3e0
    style AMEND fill:#c8e6c9
    style CANCEL fill:#ffcdd2
    style CONFIRM fill:#c8e6c9
    style RESUBMIT fill:#c8e6c9
```

---

## DK Reason Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| 41 | Unknown trade | Trade comparison |
| 42 | Wrong quantity | Amendment |
| 43 | Wrong price | Amendment |
| 44 | Wrong security | Amendment |

See [[dtc-reason-codes]] for full reference.

---

## Investigation Steps

| Step | Action |
|------|--------|
| 1 | Receive DK notification |
| 2 | Identify reason code |
| 3 | Compare trade details |
| 4 | Contact counterparty |
| 5 | Agree on correction |
| 6 | Submit amendment or cancel |

---

## T+1 Impact

> [!warning] Compressed Timeline
> T+1 settlement compresses DK resolution time. Automation critical.

| T+2 Era | T+1 Era |
|---------|---------|
| Next-day resolution | Same-day resolution |
| Manual acceptable | Automation required |

---

## Related
- [[obligation-warehouse]] - Parent system
- [[dtc-reason-codes]] - Code reference
- [[_MOC-exceptions]] - Exception overview
- [[reclaims]] - Related exception type
