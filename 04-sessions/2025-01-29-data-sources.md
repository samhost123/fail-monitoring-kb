# Session: Data Sources Review
**Date:** 2025-01-29

## Objective
Document and validate data sources for the fail monitoring system.

## Discussion Points

### 1. Primary Data Feeds
- Confirmed DTC settlement files as primary source
- CNS position reports provide aging information
- Internal trade system links fails to original trades

### 2. Data Quality Concerns
- Occasional late file delivery from DTC
- Need reconciliation process for discrepancies
- Corporate actions can cause temporary mismatches

### 3. Integration Architecture
- Files processed via overnight batch
- Real-time updates from internal systems
- Dashboard refreshes every 15 minutes

## Decisions Made
1. Implement file arrival monitoring with alerts
2. Build reconciliation report for DTC vs internal
3. Add corporate action flag to fail records

## Action Items
- [ ] Document file formats in detail
- [ ] Create data flow diagram
- [ ] Define reconciliation tolerance thresholds

## Questions for Follow-up
- What is the SLA for DTC file delivery?
- How are partial settlements reported?
- What triggers a CNS position adjustment?

## Related Documents
- [Data Sources](../01-data-model/data-sources.md)
- [Entity Relationships](../01-data-model/entity-relationships.md)
