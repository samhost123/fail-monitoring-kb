---
title: "Priority Score Formula"
aliases: ["Scoring Formula", "Fail Scoring Algorithm"]
tags:
  - reference/formula
  - python/formula
created: 2026-02-03
updated: 2026-02-03
status: final
source: "02-business-rules/prioritization-logic.md"
---

# Priority Score Formula

Weighted calculation for fail prioritization using multiplicative modifiers.

---

## Formula

```
Final Score = Base Score × Inventory Modifier × Concentration Modifier
```

### Base Score (0-100)
```
Base Score = (Age × 0.30) + (Value × 0.25) + (Regulatory × 0.35) + (CP History × 0.10)
```

### Modifiers
| Modifier | Range | Effect |
|----------|-------|--------|
| Inventory | 0.50–1.00 | Reduces score when coverable |
| Concentration | 1.00–1.50 | Increases score for high-fail securities |

---

## Base Factor Tables

### Age Factor (0-100)
| Days Aged | Score | Financial Impact |
|-----------|-------|------------------|
| 1-3 | 10 | [[cns-fails-charge]]: 5% |
| 4-6 | 30 | [[cns-fails-charge]]: 5% |
| 7-9 | 60 | [[cns-fails-charge]]: 15% |
| 10-12 | 80 | [[aged-fail-deductions]] begin |
| 13+ | 100 | [[threshold-securities|Threshold]] deadline |

### Value Factor (0-100)
| Market Value | Score |
|--------------|-------|
| < $100K | 10 |
| $100K - $500K | 30 |
| $500K - $1M | 50 |
| $1M - $5M | 70 |
| > $5M | 100 |

### Regulatory Factor (0-100)
| Condition | Score | Reference |
|-----------|-------|-----------|
| No regulatory concern | 0 | |
| Approaching [[reg-sho-rule-204|Reg SHO]] deadline | 50 | [[close-out-matrix]] |
| [[threshold-securities|Threshold security]] | 80 | S+13 deadline |
| Close-out required | 100 | [[penalty-box]] risk |

### Counterparty History Factor (0-100)
Based on **15-day rolling** fail rate against this broker.

| Fail Rate (15-day) | Score | Classification |
|--------------------|-------|----------------|
| < 1% of trades | 10 | Normal |
| 1-3% of trades | 30 | Elevated |
| 3-5% of trades | 60 | Frequent |
| > 5% of trades | 100 | Problem CP |

Calculation: `cp_fail_rate = fail_count / trade_count` (15-day window)

---

## Modifier Tables

### Inventory Modifier (0.50–1.00)
Reduces priority when inventory is available to cover the fail.

**Inventory Sources:**
- **Box**: Settled long positions
- **Stock Loan**: Active borrows
- **Pending Receives**: Expected inbound (T+1 receives, recalls)

| Coverage Level | Modifier | Effect |
|----------------|----------|--------|
| ≥ 100% covered | 0.50 | Score halved |
| 75-99% covered | 0.65 | Significant reduction |
| 50-74% covered | 0.80 | Moderate reduction |
| 25-49% covered | 0.90 | Minor reduction |
| < 25% covered | 1.00 | No reduction |

Calculation: `coverage_pct = (box + stock_loan + pending_receives) / fail_qty`

### Concentration Modifier (1.00–1.50)
Increases priority for securities/counterparties with elevated risk characteristics.

| Condition | Modifier | Trigger |
|-----------|----------|---------|
| Normal | 1.00 | Baseline |
| [[threshold-securities\|Threshold list]] | 1.20 | On FINRA/NYSE/NASDAQ/CBOE list |
| **Non-CNS eligible** | 1.15 | Bilateral settlement required |
| Security fail rate > 2% ADV | 1.15 | High concentration |
| Broker fail rate > 5% | 1.15 | Problem CP pattern |

**Stacking Rules:**
- Multiple conditions multiply (e.g., 1.20 × 1.15 = 1.38)
- **Maximum modifier capped at 1.50**

#### Threshold List Sources
Must aggregate from all four SRO sources daily:

| Source | Coverage | Format |
|--------|----------|--------|
| FINRA | OTC/ADF | CSV |
| NYSE | NYSE-listed | CSV/Excel |
| NASDAQ | NASDAQ-listed | Text |
| CBOE | BZX/BYX/EDGX/EDGA | CSV |

See [[threshold-securities]] for URLs and details.

#### Non-CNS Eligibility
Non-CNS securities settle via [[obligation-warehouse]]:
- No CCP guarantee → higher counterparty risk
- Gross balance sheet exposure (no netting)
- Higher capital treatment
- **+15% concentration modifier**

See [[cns-cp-eligibility]] for eligibility rules.

#### Security Fail Concentration
```
security_fail_rate = (15_day_fail_qty_for_cusip) / (15_day_adv_for_cusip)
```

| % of ADV Failing | Modifier |
|------------------|----------|
| < 1% | 1.00 |
| 1-2% | 1.00 |
| > 2% | 1.15 |

---

## Priority Tiers

| Score | Tier | Action | [[escalation-paths|Escalation]] |
|-------|------|--------|------------|
| 0-25 | Low | Standard monitoring | None |
| 26-50 | Medium | Daily review | Level 1 |
| 51-75 | High | Active management | Level 2 |
| 76-100 | Critical | Immediate escalation | Level 3+ |

> [!note] Final Score Cap
> Final score after modifiers is capped at 100.

---

## Python Implementation

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PriorityTier(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FailContext:
    """Input context for priority calculation."""
    # Basic fail info
    age_days: int
    market_value: float
    fail_qty: int
    cusip: str
    counterparty_id: str

    # Regulatory flags
    is_threshold_security: bool = False  # On FINRA/NYSE/NASDAQ/CBOE list
    close_out_required: bool = False

    # CNS eligibility (for concentration modifier)
    is_cns_eligible: bool = True  # False = bilateral/OW settlement

    # Inventory (for modifier)
    box_qty: int = 0
    stock_loan_qty: int = 0
    pending_receive_qty: int = 0

    # Historical data (15-day rolling)
    cp_fail_count_15d: int = 0
    cp_trade_count_15d: int = 1  # Avoid division by zero
    security_fail_qty_15d: int = 0
    security_adv_15d: float = 1.0  # Avoid division by zero


@dataclass
class PriorityResult:
    """Output of priority calculation."""
    base_score: float
    inventory_modifier: float
    concentration_modifier: float
    final_score: int
    tier: PriorityTier
    factors: dict


def calculate_age_score(age_days: int) -> int:
    """Age factor: 0-100 based on days aged."""
    if age_days <= 3:
        return 10
    elif age_days <= 6:
        return 30
    elif age_days <= 9:
        return 60
    elif age_days <= 12:
        return 80
    else:
        return 100


def calculate_value_score(market_value: float) -> int:
    """Value factor: 0-100 based on market value."""
    if market_value < 100_000:
        return 10
    elif market_value < 500_000:
        return 30
    elif market_value < 1_000_000:
        return 50
    elif market_value < 5_000_000:
        return 70
    else:
        return 100


def calculate_regulatory_score(
    is_threshold: bool,
    close_out_required: bool,
    age_days: int
) -> int:
    """Regulatory factor: 0-100 based on reg status."""
    if close_out_required:
        return 100
    elif is_threshold:
        return 80
    elif age_days >= 10:  # Approaching threshold deadline
        return 50
    else:
        return 0


def calculate_cp_history_score(
    fail_count_15d: int,
    trade_count_15d: int
) -> int:
    """CP history factor: 0-100 based on 15-day fail rate."""
    if trade_count_15d == 0:
        return 10

    fail_rate = fail_count_15d / trade_count_15d

    if fail_rate < 0.01:
        return 10
    elif fail_rate < 0.03:
        return 30
    elif fail_rate < 0.05:
        return 60
    else:
        return 100


def calculate_inventory_modifier(
    fail_qty: int,
    box_qty: int,
    stock_loan_qty: int,
    pending_receive_qty: int
) -> float:
    """Inventory modifier: 0.50-1.00 based on coverage."""
    if fail_qty <= 0:
        return 1.0

    total_inventory = box_qty + stock_loan_qty + pending_receive_qty
    coverage_pct = total_inventory / fail_qty

    if coverage_pct >= 1.0:
        return 0.50
    elif coverage_pct >= 0.75:
        return 0.65
    elif coverage_pct >= 0.50:
        return 0.80
    elif coverage_pct >= 0.25:
        return 0.90
    else:
        return 1.00


def calculate_concentration_modifier(
    is_threshold: bool,
    is_cns_eligible: bool,
    security_fail_qty_15d: int,
    security_adv_15d: float,
    cp_fail_count_15d: int,
    cp_trade_count_15d: int
) -> float:
    """Concentration modifier: 1.00-1.50 based on risk characteristics."""
    modifier = 1.0

    # Threshold list (FINRA/NYSE/NASDAQ/CBOE): +20%
    if is_threshold:
        modifier *= 1.20

    # Non-CNS eligible (bilateral/OW settlement): +15%
    if not is_cns_eligible:
        modifier *= 1.15

    # Security fail concentration: +15% if > 2% of ADV
    if security_adv_15d > 0:
        security_fail_rate = security_fail_qty_15d / security_adv_15d
        if security_fail_rate > 0.02:
            modifier *= 1.15

    # Broker fail rate: +15% if > 5%
    if cp_trade_count_15d > 0:
        cp_fail_rate = cp_fail_count_15d / cp_trade_count_15d
        if cp_fail_rate > 0.05:
            modifier *= 1.15

    # Cap at 1.50
    return min(modifier, 1.50)


def calculate_priority_score(ctx: FailContext) -> PriorityResult:
    """
    Calculate fail priority score with modifiers.

    Formula: Final = Base × Inventory × Concentration

    Args:
        ctx: FailContext with all required inputs

    Returns:
        PriorityResult with scores and tier
    """
    # Calculate base factors
    age_score = calculate_age_score(ctx.age_days)
    value_score = calculate_value_score(ctx.market_value)
    reg_score = calculate_regulatory_score(
        ctx.is_threshold_security,
        ctx.close_out_required,
        ctx.age_days
    )
    cp_score = calculate_cp_history_score(
        ctx.cp_fail_count_15d,
        ctx.cp_trade_count_15d
    )

    # Base score (weighted sum)
    base_score = (
        age_score * 0.30 +
        value_score * 0.25 +
        reg_score * 0.35 +
        cp_score * 0.10
    )

    # Calculate modifiers
    inv_modifier = calculate_inventory_modifier(
        ctx.fail_qty,
        ctx.box_qty,
        ctx.stock_loan_qty,
        ctx.pending_receive_qty
    )

    conc_modifier = calculate_concentration_modifier(
        ctx.is_threshold_security,
        ctx.is_cns_eligible,
        ctx.security_fail_qty_15d,
        ctx.security_adv_15d,
        ctx.cp_fail_count_15d,
        ctx.cp_trade_count_15d
    )

    # Final score (capped at 100)
    final_score = min(int(base_score * inv_modifier * conc_modifier), 100)

    # Determine tier
    if final_score <= 25:
        tier = PriorityTier.LOW
    elif final_score <= 50:
        tier = PriorityTier.MEDIUM
    elif final_score <= 75:
        tier = PriorityTier.HIGH
    else:
        tier = PriorityTier.CRITICAL

    return PriorityResult(
        base_score=round(base_score, 2),
        inventory_modifier=inv_modifier,
        concentration_modifier=round(conc_modifier, 2),
        final_score=final_score,
        tier=tier,
        factors={
            "age": age_score,
            "value": value_score,
            "regulatory": reg_score,
            "cp_history": cp_score,
            "coverage_pct": (ctx.box_qty + ctx.stock_loan_qty + ctx.pending_receive_qty) / max(ctx.fail_qty, 1),
            "is_threshold": ctx.is_threshold_security,
            "is_cns_eligible": ctx.is_cns_eligible
        }
    )
```

---

## Override Rules

| Condition | Override | Reference |
|-----------|----------|-----------|
| Age > 10 days | Minimum High priority | [[aged-fail-deductions]] |
| [[threshold-securities]] | Critical if close-out due | [[reg-sho-rule-204]] |
| Manual escalation | Overrides calculation | [[escalation-paths]] |

```python
def apply_overrides(result: PriorityResult, ctx: FailContext) -> PriorityResult:
    """Apply business rule overrides to calculated score."""

    # Age override: 10+ days = minimum High
    if ctx.age_days >= 10 and result.tier in (PriorityTier.LOW, PriorityTier.MEDIUM):
        result.final_score = max(result.final_score, 51)
        result.tier = PriorityTier.HIGH

    # Threshold + close-out = Critical
    if ctx.is_threshold_security and ctx.close_out_required:
        result.final_score = max(result.final_score, 76)
        result.tier = PriorityTier.CRITICAL

    return result
```

---

## Data Dependencies

### Required Feeds
| Data | Source | Frequency | Reference |
|------|--------|-----------|-----------|
| Fail details | DTC/CNS | Daily | [[data-sources]] |
| Market prices | Pricing service | Real-time | |
| Threshold lists | FINRA, NYSE, NASDAQ, CBOE | Daily | [[threshold-securities]] |
| CNS eligibility | Security master | Daily | [[cns-cp-eligibility]] |
| Box positions | Position system | Real-time | |
| Stock loan | Loan system | Real-time | |
| Pending receives | Settlement system | Intraday | [[settlement-lifecycle]] |
| CP fail history | Internal | Daily (15-day rolling) | [[cns-cp-eligibility]] |
| Security ADV | Market data | Daily (15-day rolling) | |

### Threshold List Aggregation
```python
def aggregate_threshold_lists() -> set[str]:
    """Aggregate CUSIPs from all 4 SRO threshold lists."""
    sources = {
        "FINRA": "https://www.finra.org/...",
        "NYSE": "https://www.nyse.com/...",
        "NASDAQ": "https://www.nasdaqtrader.com/...",
        "CBOE": "https://www.cboe.com/...",
    }
    threshold_cusips = set()
    for source, url in sources.items():
        cusips = fetch_threshold_list(url)  # Implementation varies by format
        threshold_cusips.update(cusips)
    return threshold_cusips
```

### Calculated Aggregates
```sql
-- 15-day CP fail rate
SELECT
    counterparty_id,
    COUNT(*) FILTER (WHERE status = 'FAILED') as fail_count,
    COUNT(*) as trade_count
FROM trades
WHERE settlement_date >= CURRENT_DATE - INTERVAL '15 days'
GROUP BY counterparty_id;

-- 15-day security fail concentration
SELECT
    cusip,
    SUM(fail_qty) as total_fail_qty,
    AVG(daily_volume) as adv_15d
FROM (
    SELECT cusip, trade_date, SUM(quantity) as daily_volume
    FROM trades
    WHERE trade_date >= CURRENT_DATE - INTERVAL '15 days'
    GROUP BY cusip, trade_date
) volumes
JOIN fails f USING (cusip)
WHERE f.created_at >= CURRENT_DATE - INTERVAL '15 days'
GROUP BY cusip;
```

---

## Related
- [[prioritization-logic]] - Full business rules
- [[new-fail-triage]] - Triage application
- [[escalation-paths]] - Escalation triggers
- [[threshold-securities]] - Concentration factor
- [[cns-cp-eligibility]] - CP data
- [[data-sources]] - Input feeds
