# Offset Matching

## Overview
Offset matching pairs receive fails (FTR) with deliver fails (FTD) to reduce net exposure.

## Matching Criteria

### Required Matches (All Must Match)
| Field | Description |
|-------|-------------|
| CUSIP | Same security |
| Settlement Date | Same or compatible dates |
| Counterparty | Same or affiliated entities |

### Optional Optimization
| Field | Preference |
|-------|------------|
| Quantity | Exact match preferred |
| Age | Older fails prioritized |

## Matching Algorithm

```
FOR each FTD fail:
    candidates = FTR fails WHERE
        cusip = FTD.cusip AND
        settlement_date <= FTD.settlement_date AND
        counterparty IN (FTD.counterparty, affiliated_entities)

    SORT candidates BY:
        1. Exact quantity match (DESC)
        2. Age (DESC - older first)
        3. Settlement date (ASC - earlier first)

    FOR each candidate:
        IF candidate.quantity == FTD.remaining_quantity:
            FULL OFFSET
        ELSE:
            PARTIAL OFFSET (min of both quantities)

        UPDATE both fails
        IF FTD fully offset: BREAK
```

## Offset Types

### Full Offset
Both fails completely cancelled against each other.

```
FTD: 1000 shares AAPL  ──┐
                        ├──> Net: 0
FTR: 1000 shares AAPL  ──┘
```

### Partial Offset
Larger fail reduced by smaller fail amount.

```
FTD: 1000 shares AAPL  ──┐
                        ├──> FTD: 400 shares remaining
FTR:  600 shares AAPL  ──┘     FTR: 0 (closed)
```

## Business Rules

1. **Same-Day Priority:** Offsets for same settlement date processed first
2. **Aging Benefit:** Offset resets aging clock for remaining position
3. **Audit Trail:** All offsets must be logged with timestamps
4. **Reversibility:** Offsets can be reversed if settlement fails

## Reporting
- Daily offset report showing matches attempted and completed
- Net exposure report after offset processing
- Failed offset attempts with rejection reasons
