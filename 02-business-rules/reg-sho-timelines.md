# Reg SHO Timelines

## Overview
Regulation SHO establishes close-out requirements for fail-to-deliver positions.

## Key Timelines

### Standard Securities

```
T+1  T+2  T+3  T+4  T+5  T+6  T+7  T+8  T+9  T+10  T+11  T+12  T+13
 │    │    │    │    │    │    │    │    │    │     │     │     │
 SD   │    │    │    │    │    │    │    │    │     │     │     │
      └────┴────┴────┴────┴────┴────┴────┴────┴─────┴─────┴─────┘
                    Grace Period                    │ Close-out
                                                    │ Required
```

- **Settlement Date (SD):** T+1 for most equity trades
- **Grace Period:** T+4 through T+12
- **Close-out Deadline:** Beginning of T+13

### Threshold Securities

```
T+1  T+2  T+3  T+4  T+5  T+6
 │    │    │    │    │    │
 SD   │    │    │    │    │
      └────┴────┴────┴────┘
           Grace Period   │ Close-out
                          │ Required
```

- **Close-out Deadline:** Beginning of T+6

## Date Calculation Rules

1. **Business Days Only:** All calculations use settlement calendar
2. **Holidays Excluded:** SIFMA holidays do not count
3. **Weekend Handling:** Saturday/Sunday are not settlement days

## Close-out Requirements

### Mandatory Close-out Actions
1. Purchase equivalent securities in the open market
2. Borrow securities to make delivery
3. Arrange for buying-in by counterparty

### Penalties for Non-Compliance
- Pre-borrow requirement imposed
- Trading restrictions
- Regulatory reporting required

## Monitoring Triggers

| Days to Close-out | Action Required |
|-------------------|-----------------|
| 5+ days | Standard monitoring |
| 3-4 days | Alert operations |
| 2 days | Escalate to supervisor |
| 1 day | Initiate close-out process |
| 0 days | Execute close-out |
