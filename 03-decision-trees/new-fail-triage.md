---
title: "New Fail Triage"
aliases: ["Triage", "Fail Processing"]
tags:
  - lifecycle/triage
  - decision-tree
  - python/rule
created: 2025-01-29
updated: 2026-02-03
status: final
---

# New Fail Triage

Decision tree for processing newly identified fails.

---

## Triage Flow

```mermaid
flowchart TD
    NEW["New Fail Alert"]
    VALID{Valid Fail?<br/>Not data error}
    FP["Mark as<br/>False Positive"]
    THRESH{[[threshold-securities|Threshold<br/>Security?]]}
    CRITICAL1["CRITICAL Priority<br/>Flag as Threshold"]
    VALUE{Value > $1M?}
    HIGH1["HIGH Priority<br/>High Value Flag"]
    REGSHO{Approaching<br/>[[reg-sho-rule-204|Reg SHO]]?}
    HIGH2["HIGH Priority<br/>Reg SHO Flag"]
    CP{Known Problem<br/>Counterparty?}
    ESCALATE["Escalate to<br/>Supervisor"]
    CALC["Calculate<br/>[[prioritization-logic|Priority Score]]"]

    subgraph QUEUES["Queue Assignment"]
        SCORE{Score?}
        CRIT_Q["Critical Queue<br/>(76-100)"]
        HIGH_Q["High Queue<br/>(51-75)"]
        MED_Q["Medium Queue<br/>(26-50)"]
        LOW_Q["Low Queue<br/>(0-25)"]
    end

    NEW --> VALID
    VALID --> |No| FP
    VALID --> |Yes| THRESH
    THRESH --> |Yes| CRITICAL1
    THRESH --> |No| VALUE
    VALUE --> |Yes| HIGH1
    VALUE --> |No| REGSHO
    REGSHO --> |Yes| HIGH2
    REGSHO --> |No| CP
    CP --> |Yes| ESCALATE
    CP --> |No| CALC
    CRITICAL1 --> CALC
    HIGH1 --> CALC
    HIGH2 --> CALC
    ESCALATE --> CALC
    CALC --> SCORE
    SCORE --> |76-100| CRIT_Q
    SCORE --> |51-75| HIGH_Q
    SCORE --> |26-50| MED_Q
    SCORE --> |0-25| LOW_Q

    style CRITICAL1 fill:#ffcdd2
    style HIGH1 fill:#fff3e0
    style HIGH2 fill:#fff3e0
    style CRIT_Q fill:#ffcdd2
    style HIGH_Q fill:#fff3e0
```

---

## Validation Checks

### Data Quality
| Check | Validation |
|-------|------------|
| CUSIP | Exists in security master, 9 characters |
| Quantity | Positive integer |
| Settlement date | Valid business day, not future |
| Counterparty | Exists in reference data |

### Duplicate Detection
| Check | Action if True |
|-------|----------------|
| Already in fail inventory | Skip (not new fail) |
| Reversal of existing fail | Update existing record |
| Corporate action adjustment | Route to [[priority-groups\|Priority Group 1]] |

---

## Priority Override Rules

| Condition | Override | Reference |
|-----------|----------|-----------|
| [[threshold-securities\|Threshold security]] | → Critical | [[reg-sho-rule-204]] |
| Value > $1M | → High minimum | [[prioritization-logic]] |
| Age > 10 days | → High minimum | [[prioritization-logic]] |
| Close-out required | → Critical | [[reg-sho-rule-204]] |

---

## Initial Actions

| Condition | Immediate Action | System |
|-----------|------------------|--------|
| Valid fail | Create fail record | [[entity-relationships]] |
| [[threshold-securities]] | Add regulatory flag | [[reg-sho-rule-204]] |
| High value | Notify senior ops | [[escalation-paths]] |
| Problem CP | Auto-escalate | [[escalation-paths]] |
| Approaching Reg SHO | Alert operations | [[close-out-matrix]] |

---

## System Updates

| Step | Action | Related |
|------|--------|---------|
| 1 | Create fail record | [[fail-lifecycle]] → OPEN |
| 2 | Calculate [[prioritization-logic\|priority score]] | [[priority-score-formula]] |
| 3 | Assign to queue | Based on score |
| 4 | Send notifications | [[escalation-paths]] |
| 5 | Log triage decision | Audit trail |

---

## Integration Points

| System | Integration |
|--------|-------------|
| [[data-sources]] | Fail alert input |
| [[prioritization-logic]] | Score calculation |
| [[escalation-paths]] | Queue routing |
| [[fail-lifecycle]] | State management |
| [[settlement-lifecycle]] | Node 5 entry |

---

## Related
- [[prioritization-logic]] - Score calculation
- [[escalation-paths]] - Post-triage routing
- [[fail-lifecycle]] - State transitions
- [[settlement-lifecycle]] - Overall flow
- [[threshold-securities]] - Critical flag trigger
- [[reg-sho-rule-204]] - Regulatory urgency
