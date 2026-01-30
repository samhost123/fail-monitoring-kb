# Prioritization Logic

## Overview
Defines how fails are scored and prioritized for attention.

## Priority Score Calculation

```
Priority Score = (Age Factor × 30) + (Value Factor × 25) + (Reg Factor × 35) + (CP Factor × 10)
```

### Factor Definitions

#### Age Factor (0-100)
| Days Aged | Score |
|-----------|-------|
| 1-3 | 10 |
| 4-6 | 30 |
| 7-9 | 60 |
| 10-12 | 80 |
| 13+ | 100 |

#### Value Factor (0-100)
| Market Value | Score |
|--------------|-------|
| < $100K | 10 |
| $100K - $500K | 30 |
| $500K - $1M | 50 |
| $1M - $5M | 70 |
| > $5M | 100 |

#### Regulatory Factor (0-100)
| Condition | Score |
|-----------|-------|
| No regulatory concern | 0 |
| Approaching Reg SHO threshold | 50 |
| Threshold security | 80 |
| Close-out required | 100 |

#### Counterparty Factor (0-100)
| History | Score |
|---------|-------|
| No prior issues | 10 |
| Occasional fails | 30 |
| Frequent fails | 60 |
| Known problem CP | 100 |

## Priority Tiers

| Score Range | Tier | Action |
|-------------|------|--------|
| 0-25 | Low | Standard monitoring |
| 26-50 | Medium | Daily review |
| 51-75 | High | Active management |
| 76-100 | Critical | Immediate escalation |

## Override Rules
1. Any fail > 10 days automatically becomes High priority minimum
2. Threshold securities automatically become Critical
3. Manual escalation overrides calculated score
