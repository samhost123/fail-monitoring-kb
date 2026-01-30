# Data Sources

## Overview
This document catalogs all data sources feeding into the fail monitoring system.

## Primary Sources

### 1. DTC Settlement Files
- **Frequency:** Daily
- **Format:** Fixed-width text files
- **Key Fields:** CUSIP, quantity, counterparty, settlement date
- **Use:** Identifies settled and failed transactions

### 2. CNS Position Reports
- **Frequency:** Daily
- **Format:** CSV
- **Key Fields:** Net position, obligation type, aging
- **Use:** Tracks CNS fail positions and aging

### 3. Internal Trade System
- **Frequency:** Real-time
- **Format:** API/Database
- **Key Fields:** Trade ID, execution date, expected settlement
- **Use:** Links fails to original trade details

## Secondary Sources

### 4. Threshold Security List
- **Source:** SEC/FINRA
- **Frequency:** Daily
- **Use:** Identifies securities with enhanced close-out requirements

### 5. Corporate Actions Feed
- **Frequency:** As announced
- **Use:** Identifies fails affected by corporate actions

## Data Flow Diagram
```
[DTC] ──────┐
            │
[CNS] ──────┼──> [Fail Monitor] ──> [Dashboard]
            │
[Trades] ───┘
```

## Data Quality Rules
- All CUSIPs must be 9 characters
- Settlement dates cannot be in the future
- Quantities must be non-negative
