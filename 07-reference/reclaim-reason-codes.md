---
title: "Reclaim Reason Codes"
aliases: ["Reclaim Codes"]
tags:
  - reference/codes
  - system/dtc
created: 2026-02-03
status: final
source: "Raw research/Settlement Exception Processing Analysis.md"
---

# Reclaim Reason Codes

DTC reason codes for reclaim processing.

---

## Code Reference

### DK Reclaims (41-44)
| Code | Meaning | Resolution |
|------|---------|------------|
| 41 | Unknown trade | Verify trade comparison |
| 42 | Wrong quantity | Amend quantity |
| 43 | Wrong price | Amend price |
| 44 | Wrong security | Amend CUSIP |

### Physical/Data Issues (45)
| Code | Meaning | Resolution |
|------|---------|------------|
| 45 | Mutilated/Wrong certificate | Physical inspection |

### Timing Issues (87-88)
| Code | Meaning | Resolution |
|------|---------|------------|
| 87 | Late delivery | Review timing |
| 88 | Stale dated | Refresh instruction |

---

## Processing Behavior

| Code Range | RAD Treatment | Typical Cause |
|------------|---------------|---------------|
| 41-44 | Subject to RAD if unmatched | Trade discrepancy |
| 45 | Subject to RAD | Physical issue |
| 87-88 | Subject to RAD | Operational delay |

---

## Related
- [[reclaims]] - Reclaim mechanics
- [[dtc-reason-codes]] - Full code reference
- [[dk-processing]] - DK resolution
