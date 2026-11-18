---
description: Draft an Architecture Decision Record (ADR) from the current decision (chat-first).
argument-hint: [decision summary or target path]
---

Load the `tech-me` skill (via the `Skill` tool if available) and execute **`adr`** mode:

- **Chat-first & permissioned:** Draft the ADR in chat first with `Status: Proposed`. Do **not** write any file to disk unless the user explicitly authorizes file creation in `Context` below or after reviewing the draft.
- **Required structure** (matching the `tech-me` ADR template):
  - `# ADR-XXX: <Short Decision Title>`
  - `Date: YYYY-MM-DD` · `Status: Proposed`
  - `## Context and Problem` (confirmed constraints vs assumptions)
  - `## Decision` (recommended architecture/stack and rationale)
  - `## Alternatives Considered` (2–3 credible options and why they lost for *this* context)
  - `## Consequences and Risks` (trade-offs, operational/migration costs, validation steps)
  - `## Assumptions and Revisit Triggers` (each provisional default + observable condition that reopens the decision)
- **Honesty:** Do not invent benchmark numbers, prices, or organizational sign-off; label any unmeasured figure **estimate — not measured**.

Context: $ARGUMENTS
