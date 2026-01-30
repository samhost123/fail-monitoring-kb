# Fail Monitoring Knowledge Base - Copilot Context

## Project Overview
This knowledge base documents the fail monitoring system for securities settlement operations.

## How to Use This Repository
1. Start each Copilot session by referencing this file
2. Check `_GLOSSARY.md` for domain-specific terminology
3. Review `_SESSION_LOG.md` for recent changes and context
4. Navigate to specific folders for detailed documentation

## Key Concepts
- **Fail**: A trade that did not settle on the expected settlement date
- **Reg SHO**: SEC regulation governing short sales and fail-to-delivers
- **CNS**: Continuous Net Settlement system operated by NSCC

## Repository Structure
- `/01-data-model/` - Data sources, entity relationships, fail lifecycle
- `/02-business-rules/` - Prioritization logic, regulatory timelines, offset matching
- `/03-decision-trees/` - Triage workflows and escalation paths
- `/04-sessions/` - Copilot session logs and conversation history

## Context for AI Assistants
When working in this codebase:
- Always check the glossary for unfamiliar terms
- Reference the session log to understand recent changes
- Follow established patterns in decision trees
- Maintain consistency with existing business rules
