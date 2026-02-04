---
title: "MOC: Regulatory Framework"
aliases: ["Regulations MOC", "Compliance Overview"]
tags:
  - moc
  - regulation/overview
created: 2026-02-03
status: final
---

# Regulatory Framework

Map of Content for settlement regulations: Reg SHO, Rule 15c3-1, NSCC/FINRA rules.

---

## Regulatory Hierarchy

```mermaid
flowchart TB
    SEC["SEC"] --> REGSHO["Regulation SHO"]
    SEC --> RULE15["Rule 15c3-1"]

    NSCC["NSCC"] --> RULE11["Rule 11 (Buy-Ins)"]
    NSCC --> FAILCHARGE["CNS Fails Charge"]

    FINRA["FINRA"] --> RULE11810["Rule 11810"]

    subgraph "Close-Out Requirements"
        REGSHO --> R204["[[reg-sho-rule-204|Rule 204]]"]
        R204 --> SHORT["S+1 (Short)"]
        R204 --> LONG["S+3 (Long)"]
        R204 --> THRESH["S+13 (Threshold)"]
    end

    subgraph "Capital Impact"
        RULE15 --> AGED["[[aged-fail-deductions|Aged Fail Haircuts]]"]
        AGED --> S5["S+5: Begin"]
        AGED --> S21["S+21: Full"]
    end

    style SEC fill:#e1bee7
    style NSCC fill:#b2dfdb
    style FINRA fill:#bbdefb
    style REGSHO fill:#e1bee7
    style RULE15 fill:#e1bee7
    style RULE11 fill:#b2dfdb
    style FAILCHARGE fill:#ffcdd2
    style RULE11810 fill:#bbdefb
    style R204 fill:#e1bee7
    style SHORT fill:#ffcdd2
    style LONG fill:#fff3e0
    style THRESH fill:#ffcdd2
    style AGED fill:#ffcdd2
    style S5 fill:#fff3e0
    style S21 fill:#ffcdd2
```

---

## Regulation SHO

> [!warning] Delivery-Centric Model
> Reg SHO shifted from "locate-centric" to "delivery-centric" - hard close-out requirements override trading discretion.

### Core Rules
| Rule | Page | Function |
|------|------|----------|
| 200 | [[reg-sho-rule-200]] | Order marking (Long/Short/Short Exempt) |
| 203 | [[threshold-securities]] | Locate & threshold list |
| 204 | [[reg-sho-rule-204]] | Mandatory close-out deadlines |

### Close-Out Matrix
| Position Type | Deadline | Consequence |
|---------------|----------|-------------|
| Short sale fail | S+1 market open | [[penalty-box]] |
| Long sale fail | S+3 market open | [[penalty-box]] |
| Market maker | S+3 (extended) | [[penalty-box]] |
| [[threshold-securities\|Threshold]] | S+13 | Mandatory purchase |

### Penalty Box
See [[penalty-box]] for pre-borrow restriction mechanics:
- Destroys trading economics (10-100%+ APR for HTB)
- Applies firm-wide per security
- Exit only via "cleared and settled" delivery

---

## Rule 15c3-1 (Net Capital)

> [!danger] Capital at Risk
> Aged fails trigger capital deductions that can force business cessation.

### Haircut Schedule
| Age | Deduction | Page |
|-----|-----------|------|
| S+5 | Begins | [[aged-fail-deductions]] |
| S+7 | 15% | [[aged-fail-deductions]] |
| S+14 | 25% | [[aged-fail-deductions]] |
| S+21 | 100% | [[aged-fail-deductions]] |

### Impact
- Reduces excess net capital
- May trigger early warning thresholds
- Affects business capacity

---

## NSCC Rules

### Rule 11: CNS Buy-Ins
See [[buy-in-mechanics]] for CNS buy-in workflow:
1. Submit Buy-In Intent
2. Position elevated to [[priority-groups|Priority Group 2]]
3. Retransmittal Notice to oldest short
4. Market execution if unresolved

### CNS Fails Charge
See [[cns-fails-charge]] for duration-based penalties:

| Age | Rate |
|-----|------|
| 1-4 days | 5% |
| 5-10 days | 15% |
| 11-20 days | 20% |
| 21+ days | 100% |

---

## FINRA Rules

### Rule 11810: Bilateral Buy-Ins
See [[buy-in-mechanics]] for bilateral process:
- 2-business-day written notice required
- 7-day extension if securities "in transit"
- Difference billed to failing party

---

## Compliance Timelines

```mermaid
flowchart LR
    subgraph REGSHO["Reg SHO"]
        RS1["S+1<br/>Short Close-Out"]
        RS3["S+3<br/>Long Close-Out"]
    end

    subgraph CAPITAL["Rule 15c3-1"]
        C5["S+5<br/>Haircut Begins"]
        C14["S+14<br/>25% Haircut"]
        C21["S+21<br/>100% Haircut"]
    end

    subgraph THRESH["Threshold"]
        T13["S+13<br/>Mandatory Purchase"]
    end

    RS1 --> RS3
    C5 --> C14 --> C21

    style RS1 fill:#ffcdd2
    style RS3 fill:#ffcdd2
    style C5 fill:#fff3e0
    style C14 fill:#ffcdd2
    style C21 fill:#b71c1c,color:#fff
    style T13 fill:#ffcdd2
```

---

## Related
- [[_MOC-settlement]] - Settlement systems subject to regulations
- [[_MOC-exceptions]] - Exception processing for compliance
- [[close-out-matrix]] - Quick reference for all deadlines
