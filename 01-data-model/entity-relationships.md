# Entity Relationships

## Core Entities

### Fail
The central entity representing a settlement failure.

| Field | Type | Description |
|-------|------|-------------|
| fail_id | UUID | Unique identifier |
| trade_id | UUID | Link to originating trade |
| cusip | VARCHAR(9) | Security identifier |
| quantity | INTEGER | Number of shares |
| counterparty_id | UUID | Other party to the trade |
| fail_type | ENUM | FTD (deliver) or FTR (receive) |
| settlement_date | DATE | Original expected settlement |
| status | ENUM | Current lifecycle state |
| created_at | TIMESTAMP | When fail was created |
| updated_at | TIMESTAMP | Last modification |

### Trade
The original transaction that resulted in a fail.

| Field | Type | Description |
|-------|------|-------------|
| trade_id | UUID | Unique identifier |
| execution_date | DATE | When trade was executed |
| settlement_date | DATE | Expected settlement date |
| cusip | VARCHAR(9) | Security identifier |
| quantity | INTEGER | Number of shares |
| price | DECIMAL | Execution price |
| side | ENUM | BUY or SELL |

### Counterparty
External party involved in the trade.

| Field | Type | Description |
|-------|------|-------------|
| counterparty_id | UUID | Unique identifier |
| name | VARCHAR | Legal name |
| dtc_number | VARCHAR(4) | DTC participant number |
| contact_email | VARCHAR | Operations contact |

## Relationships

```
┌───────────┐       ┌───────────┐       ┌──────────────┐
│   Trade   │ 1───* │   Fail    │ *───1 │ Counterparty │
└───────────┘       └───────────┘       └──────────────┘
                          │
                          │ *
                          │
                    ┌─────┴─────┐
                    │  Action   │
                    └───────────┘
```

- One Trade can have multiple Fails (partial settlements)
- One Fail belongs to one Counterparty
- One Fail can have multiple Actions (audit trail)

## Indexes
- `idx_fail_cusip` - For security-based lookups
- `idx_fail_status` - For status-based filtering
- `idx_fail_counterparty` - For counterparty analysis
- `idx_fail_settlement_date` - For aging calculations
