# Session: Prioritization Logic Design
**Date:** 2025-01-30

## Objective
Define the prioritization algorithm for fail monitoring.

## Discussion Points

### 1. Scoring Factors
- Age is the most critical factor (regulatory deadlines)
- Value impacts business risk
- Regulatory status (threshold securities) requires special handling
- Counterparty history informs likelihood of resolution

### 2. Weight Distribution
Initial proposal:
- Age: 30%
- Value: 25%
- Regulatory: 35%
- Counterparty: 10%

Rationale: Regulatory compliance is non-negotiable, hence highest weight.

### 3. Tier Definitions
- Low (0-25): Monitor only
- Medium (26-50): Daily attention
- High (51-75): Active management
- Critical (76-100): Immediate action

## Decisions Made
1. Adopt weighted scoring model
2. Regulatory factor gets highest weight
3. Implement automatic escalation for 10+ day fails
4. Threshold securities always Critical priority

## Open Questions
- Should we factor in historical resolution time by counterparty?
- How to handle fails approaching close-out deadline?
- What override authority should analysts have?

## Next Steps
1. Implement scoring algorithm
2. Build priority dashboard view
3. Create escalation workflow

## Related Documents
- [Prioritization Logic](../02-business-rules/prioritization-logic.md)
- [Escalation Paths](../03-decision-trees/escalation-paths.md)
