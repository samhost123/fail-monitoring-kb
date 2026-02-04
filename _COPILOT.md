# COPILOT INSTRUCTIONS

## RULES - READ THESE FIRST
- NO essays. NO walls of text.
- Maximum 10 bullet points per response
- NO introductions like "Great question!" or "Sure, I can help with that!"
- NO summaries at the end
- NO repeating what I just said back to me
- If I ask for a list, give me a list. Not paragraphs.
- If I ask a yes/no question, start with yes or no.
- Use code blocks for any structured output
- When unsure, ask ONE clarifying question. Not five.
- DO NOT explain concepts I already know - assume I understand the domain

## PROJECT CONTEXT
Settlement fail monitoring and prioritization for correspondent clearing.

**Scope:** CNS, IMS, Obligation Warehouse, DTC bilateral
**Business:** Clear for market makers/execution brokers. Manage settlement. Fails occur when counterparties don't deliver. Reg SHO has deadlines.

## KEY TERMS (don't explain these)
- DVP/RVP: Delivery/Receive vs Payment
- CNS: Continuous Net Settlement (NSCC)
- IMS: Inventory Management System (DTC)
- OW: Obligation Warehouse
- Novation: CCP transformation
- Netting: Gross-to-net reduction
- Priority Groups: CNS allocation hierarchy (1-4)
- Affirmation: Trade matching status
- Fail: Missed settlement date
- Correspondent: Client broker we clear for

## FOLDER STRUCTURE
```
00-index/       → Navigation hub, MOCs
01-data-model/  → Entities, data sources
02-business-rules/ → Prioritization, Reg SHO, offsets
03-decision-trees/ → Triage, escalation, lifecycle
04-sessions/    → Meeting notes
05-systems/     → CNS, IMS, OW documentation
06-regulations/ → Reg SHO, Rule 15c3-1
07-reference/   → Timelines, formulas, codes
```

## CURRENT FOCUS
Working on: _______________
Reference: [[filename]]

## OUTPUT FORMAT
- Obsidian markdown
- [[wiki links]] for references
- Tables over paragraphs
- Callouts: > [!note] or > [!warning]
- Mermaid diagrams for workflows

## IF YOU START RAMBLING
Stop. Use a table. Or bullets. Or a code block.
