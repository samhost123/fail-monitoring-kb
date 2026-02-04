---
title: "Regulation SHO Rule 204"
aliases: ["Rule 204", "Close-Out Requirements"]
tags:
  - regulation/reg-sho
  - lifecycle/close-out
  - python/rule
created: 2026-02-03
status: final
source: "Raw research/Regulation SHO FinOps Analysis.md"
---

# Regulation SHO Rule 204

SEC mandatory close-out requirements for settlement failures. Delivery-centric model - hard deadlines override trading discretion.

---

## Close-Out Matrix

```mermaid
flowchart LR
    subgraph SHORT["Short Sale (S+1 Close-Out)"]
        T1["T<br/>Trade"] --> S1["T+1 (S)<br/>Settlement"] --> C1["S+1<br/>Close-Out"]
    end

    subgraph LONG["Long Sale (S+3 Close-Out)"]
        T2["T<br/>Trade"] --> S2["T+1 (S)<br/>Settlement"] --> G2["S+1 to S+2<br/>Grace"] --> C2["S+3<br/>Close-Out"]
    end

    subgraph THRESH["Threshold Security (S+13)"]
        S3["S<br/>Settlement"] --> TH["S+1 to S+12<br/>Consecutive Days"] --> MP["S+13<br/>Mandatory Purchase"]
    end

    style C1 fill:#ffcdd2
    style C2 fill:#ffcdd2
    style TH fill:#bbdefb
    style MP fill:#ffcdd2
```

| Position Type | Deadline | Timing | Failure Result |
|---------------|----------|--------|----------------|
| Short sale fail | S+1 | Market open | [[penalty-box]] |
| Long sale fail | S+3 | Market open | [[penalty-box]] |
| Market maker | S+3 | Extended | [[penalty-box]] |
| [[threshold-securities\|Threshold]] | S+13 | Intraday | Mandatory purchase |

---

## Short Sale Close-Out (S+1)

> [!danger] Hard Deadline
> Short sale fails must be closed out by **market open on S+1**. No exceptions. Failure triggers immediate Penalty Box.

| Aspect | Requirement |
|--------|-------------|
| Position type | Short sale (Rule 200 marking) |
| Deadline | S+1 market open (9:30 AM ET) |
| Resolution | "Cleared and settled" shares |
| Failure | [[penalty-box]] - pre-borrow required |

### Resolution Requirements
- Must be "cleared and settled" - no recursive failures
- Borrow does NOT satisfy (must be purchase or actual delivery)
- ETF conversion relief available for hard-to-borrow

---

## Long Sale Close-Out (S+3)

| Aspect | Requirement |
|--------|-------------|
| Position type | Long sale fail |
| Deadline | S+3 market open |
| Resolution | "Cleared and settled" shares |
| Failure | [[penalty-box]] |

### Market Maker Extended Deadline
Bona fide market makers receive extended S+3 deadline for market making activity (not proprietary trading).

---

## Threshold Securities (S+13)

See [[threshold-securities]] for list criteria.

> [!warning] Mandatory Purchase
> Threshold securities require **purchase** (not borrow) close-out by Day 13. No exceptions.

| Day | Action Required |
|-----|-----------------|
| Day 1-12 | Standard resolution efforts |
| Day 13 | Mandatory purchase required |
| Failure | Continued Penalty Box + regulatory scrutiny |

---

## Penalty Box Mechanics

See [[penalty-box]] for details.

```mermaid
flowchart TD
    FAIL["Close-Out Failure"] --> PENALTYBOX["Penalty Box<br/>(Security-specific)"]
    PENALTYBOX --> PREBORROW["Pre-Borrow Required<br/>for ALL short sales"]
    PREBORROW --> COST["Cost: 10-100%+ APR<br/>(HTB securities)"]
    PREBORROW --> EXIT{Exit Condition}
    EXIT --> |"Cleared & Settled"| CLEAR["Exit Penalty Box"]
    EXIT --> |"Borrow/Locate"| STAY["Remain in Box"]

    style PENALTYBOX fill:#ffcdd2
    style COST fill:#ffcdd2
```

| Aspect | Impact |
|--------|--------|
| Scope | Firm-wide for specific security |
| Duration | Until "cleared and settled" delivery |
| Cost | Pre-borrow vs. locate (10-100%+ APR for HTB) |
| Trading | Destroys market maker economics |

---

## Locate vs. Pre-Borrow

| Aspect | Locate | Pre-Borrow (Penalty Box) |
|--------|--------|--------------------------|
| Timing | Before short sale | Before short sale |
| Requirement | "Reasonable grounds" | Actual borrow in hand |
| Cost | Minimal | Full borrow rate |
| HTB Impact | Manageable | 10-100%+ APR |

---

## Financial Implications

### Direct Costs
| Cost Type | Driver |
|-----------|--------|
| [[cns-fails-charge]] | 5-100% CMV by age |
| Pre-borrow cost | HTB rate × position size |
| Buy-in execution | Market impact |

### Capital Impact
See [[aged-fail-deductions]] for Rule 15c3-1 haircuts.

| Age | Deduction |
|-----|-----------|
| S+5 | Begins |
| S+7 | 15% |
| S+14 | 25% |
| S+21 | 100% |

---

## Compliance Checklist

| Check | Frequency | Action |
|-------|-----------|--------|
| Short sale fails | Daily | Monitor for S+1 deadline |
| Long sale fails | Daily | Monitor for S+3 deadline |
| Threshold list | Daily | Check SEC list |
| Penalty Box status | Real-time | Track securities in box |
| Close-out execution | As needed | Document "cleared and settled" |

---

## Integration Points

| System | Integration |
|--------|-------------|
| [[prioritization-logic]] | Regulatory Factor = 100 for close-out required |
| [[new-fail-triage]] | Auto-flag approaching deadlines |
| [[escalation-paths]] | Immediate escalation for Reg SHO risk |
| [[settlement-lifecycle]] | Node 6 (Reg SHO Close-Out) |

---

## Related
- [[_MOC-regulations]] - Regulatory framework
- [[penalty-box]] - Penalty Box mechanics
- [[threshold-securities]] - Threshold list criteria
- [[aged-fail-deductions]] - Capital impact
- [[cns-fails-charge]] - Cost calculation
- [[buy-in-mechanics]] - Resolution mechanism
- [[close-out-matrix]] - Quick reference
