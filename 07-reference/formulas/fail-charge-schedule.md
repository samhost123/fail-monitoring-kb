---
title: "Fail Charge Schedule"
aliases: ["CNS Fails Charge Table"]
tags:
  - reference/formula
  - python/formula
created: 2026-02-03
status: final
source: "Raw research/Regulation SHO FinOps Analysis.md"
---

# Fail Charge Schedule

CNS Fails Charge rates by age (2025 revision).

---

## Rate Table

| Age (Days) | Rate | Factor |
|------------|------|--------|
| 1-4 | 5% | 0.05 |
| 5-10 | 15% | 0.15 |
| 11-20 | 20% | 0.20 |
| 21+ | 100% | 1.00 |

---

## Calculation

```python
def cns_fails_charge(cmv: float, age_days: int) -> float:
    """Calculate CNS Fails Charge.

    Args:
        cmv: Current Market Value
        age_days: Days since settlement date

    Returns:
        Daily charge amount
    """
    if age_days <= 4:
        rate = 0.05
    elif age_days <= 10:
        rate = 0.15
    elif age_days <= 20:
        rate = 0.20
    else:
        rate = 1.00

    return cmv * rate
```

---

## Examples

| CMV | Age | Rate | Charge |
|-----|-----|------|--------|
| $1,000,000 | Day 3 | 5% | $50,000 |
| $1,000,000 | Day 7 | 15% | $150,000 |
| $1,000,000 | Day 15 | 20% | $200,000 |
| $1,000,000 | Day 25 | 100% | $1,000,000 |

---

## Related
- [[cns-fails-charge]] - Full details
- [[aged-fail-deductions]] - Capital charges
- [[priority-score-formula]] - Age factor in scoring
