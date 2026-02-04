---
title: "IMS Profiles"
aliases: ["IMS", "Inventory Management System", "Green/Yellow/Red"]
tags:
  - system/ims
  - lifecycle/settlement
  - python/rule
created: 2026-02-03
status: final
source: "Raw research/Fin Ops IMS Equity Settlement Analysis.md"
---

# IMS Profiles

DTC's Inventory Management System controls delivery sequencing via Green/Yellow/Red profile automation levels.

---

## Profile Overview

```mermaid
flowchart LR
    subgraph GREEN["Green Profile"]
        G1["High Automation"]
        G2["Immediate Processing"]
        G3["Skip Blocked Items"]
    end

    subgraph YELLOW["Yellow Profile"]
        Y1["Conditional Automation"]
        Y2["Strict Sequencing"]
        Y3["Block if Top Fails"]
    end

    subgraph RED["Red Profile"]
        R1["Manual Intervention"]
        R2["Explicit Release"]
        R3["Crisis Management"]
    end

    INSTRUCTION["Delivery<br/>Instruction"] --> DECISION{Risk<br/>Assessment}

    DECISION --> |"Low Risk<br/>High Volume"| GREEN
    DECISION --> |"Inventory<br/>Scarcity"| YELLOW
    DECISION --> |"High Value<br/>Sensitive"| RED

    style GREEN fill:#c8e6c9
    style YELLOW fill:#fff9c4
    style RED fill:#ffcdd2
```

---

## Profile Definitions

### Green Profile (High Automation)
| Aspect | Behavior |
|--------|----------|
| Processing | Immediate, automated |
| Sequencing | No preference |
| Blocked items | Skip and continue |
| Use case | High-volume, low-risk |

**Characteristics:**
- Maximum throughput
- No manual intervention required
- Failed items don't block queue
- Typical for liquid securities

### Yellow Profile (Conditional)
| Aspect | Behavior |
|--------|----------|
| Processing | Conditional automation |
| Sequencing | Strict (top-of-queue first) |
| Blocked items | Block entire queue |
| Use case | Inventory management |

**Characteristics:**
- Reserved sequencing preferences
- Top-of-queue failure blocks all
- Useful for scarce inventory
- Prevents "cherry-picking"

### Red Profile (Manual)
| Aspect | Behavior |
|--------|----------|
| Processing | Manual release only |
| Sequencing | Explicit control |
| Blocked items | Held until released |
| Use case | High-value, crisis |

**Characteristics:**
- Full manual control
- Explicit authorization required
- Used for sensitive situations
- Crisis management mode

---

## Switch-To/Switch-Back Strategy

> [!info] Dynamic Profiling
> Members can dynamically switch profiles based on inventory conditions.

```mermaid
sequenceDiagram
    participant OPS as Operations
    participant IMS as IMS System
    participant DTC as DTC Settlement

    OPS->>IMS: Morning: Set Yellow (inventory scarce)
    IMS->>DTC: Strict sequencing active

    Note over OPS,DTC: Midday inventory arrives

    OPS->>IMS: Switch to Green
    IMS->>DTC: High automation active
    DTC->>DTC: Process backlog rapidly

    Note over OPS,DTC: Inventory depleted

    OPS->>IMS: Switch back to Yellow
    IMS->>DTC: Strict sequencing resumed
```

| Phase | Profile | Reason |
|-------|---------|--------|
| Morning (scarce) | Yellow | Preserve inventory |
| Post-receipt | Green | Process rapidly |
| Inventory depleted | Yellow | Resume control |

---

## Authorization Modes

### Passive Authorization
| Mode | Behavior |
|------|----------|
| Default | System processes per profile |
| No action | Delivery proceeds |
| Override | Manual intervention available |

### Active Authorization
| Mode | Behavior |
|------|----------|
| Required | Explicit release needed |
| Hold | Delivery queued pending approval |
| Release | Manual trigger to proceed |

---

## IMS Controls

### Collateral Monitor (CM)
See [[collateral-monitor]] for details.

| Function | Purpose |
|----------|---------|
| Solvency check | Ensure adequate collateral |
| Haircut calculation | Risk-adjusted values |
| Threshold | Minimum collateral requirement |

### Net Debit Cap (NDC)
See [[net-debit-cap]] for details.

| Limit | Value |
|-------|-------|
| Individual | $2.15B |
| Family | $2.85B |
| Purpose | Liquidity constraint |

### Receiver Authorized Delivery (RAD)
See [[rad-thresholds]] for details.

| Function | Purpose |
|----------|---------|
| Threshold limits | Prevent "dumping" |
| Authorization | Receiver controls large deliveries |
| Override | Manual approval for over-threshold |

---

## Look-Ahead Process

See [[look-ahead-process]] for details.

```mermaid
flowchart TD
    GRIDLOCK["Settlement Gridlock<br/>(Circular dependencies)"]
    LOOKAHEAD["Look-Ahead Process<br/>(2-minute intervals)"]
    MINI["Mini-Netting<br/>(Bypass individual blockage)"]
    RESOLVE["Gridlock Resolved"]

    GRIDLOCK --> LOOKAHEAD
    LOOKAHEAD --> MINI
    MINI --> RESOLVE

    style GRIDLOCK fill:#ffcdd2
    style LOOKAHEAD fill:#b2dfdb
    style MINI fill:#b2dfdb
    style RESOLVE fill:#c8e6c9
```

| Aspect | Detail |
|--------|--------|
| Frequency | Every 2 minutes |
| Function | Identify gridlock patterns |
| Resolution | Mini-netting bypasses blockage |
| Override | Ignores individual sequencing |

---

## Settlement Progress Payment (SPP)

See [[settlement-progress-payment]] for details.

| Function | Mechanism |
|----------|-----------|
| Intraday liquidity | Fedwire payment valve |
| Trigger | Net debit approaching cap |
| Effect | Release cash to continue settlement |

---

## Cost Implications

| Outcome | Cost |
|---------|------|
| STP delivery | $0.37 |
| Failed delivery | $30-50 |
| Fail escalation | [[cns-fails-charge]] + [[aged-fail-deductions]] |

---

## Profile Selection Guidelines

| Condition | Recommended Profile |
|-----------|---------------------|
| High-volume, liquid | Green |
| Scarce inventory | Yellow |
| Customer settlement priority | Yellow |
| High-value position | Yellow/Red |
| Crisis/incident | Red |
| End-of-day push | Green |

---

## Related
- [[_MOC-settlement]] - Settlement systems
- [[cns-system]] - Upstream CNS allocation
- [[collateral-monitor]] - CM solvency check
- [[net-debit-cap]] - NDC liquidity limit
- [[look-ahead-process]] - Gridlock resolution
- [[settlement-progress-payment]] - SPP liquidity
- [[rad-thresholds]] - RAD controls
