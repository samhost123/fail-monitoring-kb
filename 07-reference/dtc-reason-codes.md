---
title: "DTC Reason Codes"
aliases: ["Reason Codes", "DTC Codes"]
tags:
  - reference/codes
  - system/dtc
created: 2026-02-03
status: final
source: "Raw research/Settlement Exception Processing Analysis.md"
---

# DTC Reason Codes

Comprehensive reference for DTC settlement reason codes.

---

## Code Categories

### Reclaim Codes (41-88)
| Range | Category |
|-------|----------|
| 41-44 | DK (Don't Know) |
| 45 | Physical/Data |
| 87-88 | Timing |

See [[reclaim-reason-codes]] for details.

### OW Reclaim Codes (621-628)
| Code | Meaning |
|------|---------|
| 621 | OW position reclaim |
| 622 | OW quantity dispute |
| 623 | OW price dispute |
| 624 | OW security mismatch |
| 625-628 | Reserved |

### Rejection Codes
| Code | Meaning |
|------|---------|
| 01 | Insufficient position |
| 02 | Account frozen |
| 03 | Invalid CUSIP |
| 04 | Invalid account |

---

## Usage in Exception Processing

| Process | Relevant Codes |
|---------|----------------|
| [[reclaims]] | 41-88 |
| [[dk-processing]] | 41-44, 621-624 |
| Delivery rejection | 01-04 |

---

## Related
- [[reclaim-reason-codes]] - Reclaim subset
- [[reclaims]] - Reclaim mechanics
- [[dk-processing]] - DK resolution
- [[obligation-warehouse]] - OW codes
