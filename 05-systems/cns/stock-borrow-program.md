---
title: "Stock Borrow Program"
aliases: ["SBP", "NSCC Stock Borrow"]
tags:
  - system/cns
  - lifecycle/fail
created: 2026-02-03
status: final
source: "Raw research/Analyzing Fail Management and Settlement.md"
---

# Stock Borrow Program (SBP)

NSCC's securities lending facility to cover short positions and prevent fails. Usage declined 95% since mid-2000s.

---

## Mechanism

```mermaid
flowchart LR
    SHORT["Short Position<br/>(Failing)"]
    SBP["Stock Borrow Program"]
    LENDER["Lending Member"]
    SETTLE["Settlement"]

    SHORT --> |Borrow Request| SBP
    SBP --> |Locate Lender| LENDER
    LENDER --> |Securities| SBP
    SBP --> |Delivery| SETTLE

    style SHORT fill:#ffcdd2
    style SBP fill:#b2dfdb
    style LENDER fill:#bbdefb
    style SETTLE fill:#c8e6c9
```

---

## Key Characteristics

| Aspect | Detail |
|--------|--------|
| Purpose | Cover short positions |
| Operator | NSCC |
| Voluntary | Lender participation optional |
| Decline | Down 95% since mid-2000s |

---

## Decline Factors

| Factor | Impact |
|--------|--------|
| Bilateral lending efficiency | More attractive terms |
| Direct relationships | Bypasses SBP |
| Market evolution | Better alternatives |

---

## Liability Note

> [!warning] Borrower Remains Liable
> SBP borrow does NOT extinguish the underlying obligation. The failing member remains liable to return securities.

---

## Related
- [[cns-system]] - Parent system
- [[partial-settlement]] - Alternative mitigation
- [[cns-fails-charge]] - Fail cost if SBP insufficient
