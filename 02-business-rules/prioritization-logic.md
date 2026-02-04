---
title: "Prioritization Logic"
aliases: ["Priority Score", "Fail Scoring"]
tags:
  - python/rule
  - lifecycle/triage
created: 2025-01-29
updated: 2026-02-03
status: final
---

# Prioritization Logic

Defines how fails are scored and prioritized for attention. See [[priority-score-formula]] for Python implementation.

---

## Priority Score Calculation

```
Final Score = Base Score × Inventory Modifier × Concentration Modifier
```

### Base Score (0-100)
```
Base Score = (Age × 0.30) + (Value × 0.25) + (Regulatory × 0.35) + (CP History × 0.10)
```

| Factor | Weight | Range | Reference |
|--------|--------|-------|-----------|
| Age | 30% | 0-100 | [[fail-lifecycle]] |
| Value | 25% | 0-100 | Market value |
| Regulatory | 35% | 0-100 | [[reg-sho-rule-204]], [[threshold-securities]] |
| CP History | 10% | 0-100 | 15-day fail rate vs broker |

### Modifiers (Multiplicative)
| Modifier | Range | Effect |
|----------|-------|--------|
| Inventory | 0.5–1.0 | Reduces score when position is coverable |
| Concentration | 1.0–1.5 | Increases score for high-fail securities/brokers |

See [[priority-score-formula]] for detailed calculations.

---

## Factor Definitions

### Age Factor (0-100)
| Days Aged | Score | Financial Impact |
|-----------|-------|------------------|
| 1-3 | 10 | [[cns-fails-charge]]: 5% |
| 4-6 | 30 | [[cns-fails-charge]]: 5% |
| 7-9 | 60 | [[cns-fails-charge]]: 15% |
| 10-12 | 80 | [[aged-fail-deductions]] begin |
| 13+ | 100 | [[threshold-securities\|Threshold]] deadline |

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
| Approaching [[reg-sho-rule-204\|Reg SHO]] | 50 | [[close-out-matrix]] |
| [[threshold-securities\|Threshold security]] | 80 | S+13 deadline |
| Close-out required | 100 | [[penalty-box]] risk |

### Counterparty Factor (0-100)
Based on 15-day rolling fail history against this broker.

| Fail Rate (15-day) | Score | Classification |
|--------------------|-------|----------------|
| < 1% of trades | 10 | Normal |
| 1-3% of trades | 30 | Elevated |
| 3-5% of trades | 60 | Frequent |
| > 5% of trades | 100 | Problem CP |

---

## Modifier Factors

### Inventory Modifier (0.5–1.0)
Reduces priority when inventory is available to cover the fail. Sources: Box + Stock Loan + Pending Receives.

| Coverage Level | Modifier | Effect |
|----------------|----------|--------|
| 100%+ covered | 0.50 | Score halved (easy resolution) |
| 75-99% covered | 0.65 | Significant reduction |
| 50-74% covered | 0.80 | Moderate reduction |
| 25-49% covered | 0.90 | Minor reduction |
| < 25% covered | 1.00 | No reduction (difficult) |

> [!note] Inventory Sources
> - **Box**: Settled long positions
> - **Stock Loan**: Active borrows
> - **Pending Receives**: Expected inbound (T+1 receives, recalls)

### Concentration Modifier (1.0–1.5)
Increases priority for securities or counterparties with elevated risk characteristics.

| Condition | Modifier | Trigger |
|-----------|----------|---------|
| Normal | 1.00 | Baseline |
| Security on [[threshold-securities\|Threshold List]] | 1.20 | FINRA/NYSE/NASDAQ/CBOE lists |
| **Non-CNS eligible security** | 1.15 | Bilateral settlement required |
| Security fail rate > 2% ADV (15-day) | 1.15 | High concentration |
| Broker fail rate > 5% (15-day) | 1.15 | Problem CP |
| Multiple conditions | Multiplicative | Stack effects |

**Maximum Concentration Modifier**: 1.50 (capped)

#### Threshold List Sources
Must aggregate from all four SRO sources. See [[threshold-securities]] for URLs.

| Source | Coverage |
|--------|----------|
| FINRA | OTC/ADF securities |
| NYSE | NYSE-listed |
| NASDAQ | NASDAQ-listed |
| CBOE | BZX/BYX/EDGX/EDGA |

#### Non-CNS Eligibility Impact
Non-CNS eligible securities settle bilaterally via [[obligation-warehouse]], introducing:
- No CCP guarantee (counterparty risk)
- No netting benefit (gross exposure)
- Higher capital treatment
- Manual resolution often required

See [[cns-cp-eligibility]] for eligibility rules.

#### Security Fail Concentration
Calculated as: `(15-day fail qty for CUSIP) / (15-day ADV for CUSIP)`

| % of ADV Failing | Impact |
|------------------|--------|
| < 1% | Normal |
| 1-2% | Elevated awareness |
| > 2% | +15% modifier applied |

---

## Priority Tiers

| Score | Tier | Action | [[escalation-paths\|Escalation]] |
|-------|------|--------|------------|
| 0-25 | Low | Standard monitoring | None |
| 26-50 | Medium | Daily review | Level 1 |
| 51-75 | High | Active management | Level 2 |
| 76-100 | Critical | Immediate escalation | Level 3+ |

---

## Override Rules

| Condition | Override | Reference |
|-----------|----------|-----------|
| Age > 10 days | → High minimum | [[aged-fail-deductions]] |
| [[threshold-securities]] | → Critical | [[reg-sho-rule-204]] |
| Close-out required | → Critical | [[penalty-box]] |
| Manual escalation | Overrides score | [[escalation-paths]] |

---

## Data Requirements

### Real-Time Inputs
| Data Element | Source | Refresh |
|--------------|--------|---------|
| Fail details | [[data-sources\|DTC/CNS feeds]] | Daily |
| Market value | Pricing service | Real-time |
| Threshold list | SEC/FINRA | Daily |
| Inventory (Box) | Position system | Real-time |
| Inventory (Loan) | Stock loan system | Real-time |
| Pending receives | [[settlement-lifecycle]] | Intraday |

### Calculated Metrics (15-Day Rolling)
| Metric | Calculation | Storage |
|--------|-------------|---------|
| Security fail rate | `fail_qty / ADV` per CUSIP | Daily refresh |
| Broker fail rate | `fail_count / trade_count` per CP | Daily refresh |
| ADV | 15-day average daily volume | Daily refresh |

---

## Integration Points

| System | Usage |
|--------|-------|
| [[new-fail-triage]] | Initial scoring |
| [[escalation-paths]] | Tier-based routing |
| [[fail-lifecycle]] | State transitions |
| [[settlement-lifecycle]] | Node 5 processing |
| [[threshold-securities]] | Concentration modifier input |
| [[cns-cp-eligibility]] | CP history lookup |

---

## Example Calculations

### Example 1: High-Value, Covered Position
```
Base Score = (30×0.30) + (70×0.25) + (0×0.35) + (10×0.10) = 9 + 17.5 + 0 + 1 = 27.5
Inventory Modifier = 0.65 (80% covered)
Concentration Modifier = 1.00 (normal)
Final Score = 27.5 × 0.65 × 1.00 = 17.9 → Low Priority
```

### Example 2: Threshold Security, Uncovered
```
Base Score = (60×0.30) + (50×0.25) + (80×0.35) + (30×0.10) = 18 + 12.5 + 28 + 3 = 61.5
Inventory Modifier = 1.00 (0% covered)
Concentration Modifier = 1.20 (threshold list)
Final Score = 61.5 × 1.00 × 1.20 = 73.8 → High Priority
```

### Example 3: Problem Broker, High Concentration
```
Base Score = (80×0.30) + (100×0.25) + (50×0.35) + (100×0.10) = 24 + 25 + 17.5 + 10 = 76.5
Inventory Modifier = 0.90 (40% covered)
Concentration Modifier = 1.35 (threshold + problem CP, capped)
Final Score = 76.5 × 0.90 × 1.35 = 92.9 → Critical
```

---

## Related
- [[priority-score-formula]] - Python implementation
- [[new-fail-triage]] - Triage application
- [[escalation-paths]] - Escalation routing
- [[cns-fails-charge]] - Age cost factor
- [[aged-fail-deductions]] - Capital impact
- [[reg-sho-rule-204]] - Regulatory driver
- [[threshold-securities]] - Concentration factor
- [[cns-cp-eligibility]] - CP data quality
