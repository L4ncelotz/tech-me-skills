# Recommendation and documentation patterns

## Short answer (simple decision)

**Recommendation:** <option> because <decisive project-specific reason>.

**Why not <alternative>:** <specific trade-off>.

**Assumption / verification:** <most important unknown and how to check it>.

**Revisit when:** <observable trigger — a metric threshold, growth event, or constraint change — that would reopen this decision>.

## Adaptive technical decision report (complex decision)

1. **Recommendation first:** proposed architecture and stack; what it solves; whether the choice is definitive or conditional.
2. **Decision context:** confirmed facts and hard constraints; primary priorities.
3. **Assumptions:** explicit provisional defaults, each with its observable revisit condition; avoid fabricated quantities and obligations.
4. **Alternatives:** 2–3 credible options with constraint fit, strengths, trade-offs and when to prefer them.
5. **Rationale:** why the recommendation wins for *these* requirements; where historical/tool familiarity factored in.
6. **Risks and validation:** important unresolved issues; feasible checks or measurements; distinguish examined from unexamined.
7. **Evolution:** observable triggers for revisiting a decision and likely migration path when warranted.

Skip headings that would be empty or redundant. The report is a decision aid, not a long boilerplate document.

## Existing system change review

Show **stay vs incremental change vs replacement** where plausible. Mention integration compatibility, migration effort, rollback, downtime exposure, and operational ownership. A new stack is not a benefit in itself.

## ADR output

When requested and permitted, follow [ADR template](../assets/adr-template.md). Keep file count proportional to project complexity. Mark proposed decisions as **proposed** until the user approves them; do not equate an AI recommendation with organizational approval.
