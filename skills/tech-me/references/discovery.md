# Adaptive discovery guide

Load only when the user's requirements are incomplete or an interview is useful. **This is a menu of possible dimensions, not a script or mandatory questionnaire.**

## Prioritize information by decision impact

1. **Use case and critical workflow:** What must users do? What is a failure? Is it internal or public?
2. **Current reality:** greenfield or existing? Current architecture, infrastructure, datastore, integrations, team and migration constraints?
3. **Traffic shape:** peak concurrent operations / request rate / job volume rather than only total or monthly users. If the user cannot estimate, label an assumption and note what to measure.
4. **Data:** structure, retention, transaction and consistency requirements, regional restrictions. Avoid inventing legal/compliance obligations.
5. **Quality attributes:** response time (what operation, at what percentile?), uptime/recovery, privacy/security requirements, offline/real-time needs.
6. **Operations and budget:** who supports it, deploy target, ability to manage stateful services, hard cost limits, skills/learning cost.
7. **Future changes:** credible growth hypotheses, irreversible choices, practical migration triggers.

## How to ask

- Ask one question at a time, phrased in the user's language. One turn covers one decision; if two unknowns are independent, ask them in separate turns. Mention why it matters only when non-obvious.
- If they don't understand a term, explain it in one or two sentences and give a concrete example.
- Prefer a question that splits viable architectures (e.g., “must it run on your existing server?”) over a detailed question that would not change the answer.
- Do not ask “what throughput?” when the user cannot reasonably know; use the simplest safe provisional baseline and define how to measure later.
- If they mention a preferred stack, distinguish “must use,” “already deployed,” “team knows,” and “I like it.” All are different inputs.

## Stop / default decision

Stop asking and begin comparing when:

- The user asks to stop or get a recommendation; **or**
- Hard constraints and decision-driving priorities are sufficiently clear, and the remaining unknowns can be explicitly assumed without distorting the conclusion.

For each significant unknown, record:

| Field | What to capture |
| --- | --- |
| Unknown | What is missing? |
| Default | What is the minimal defensible **provisional** assumption? |
| Risk | Could being wrong change the design? |
| Verify | Which question, metric, or test would resolve it? |
| Revisit when | Observable trigger (metric threshold, growth event, or constraint change) that would reopen this default |

A provisional assumption must be understandable and reversible. If unknowns could materially change a high-risk or irreversible decision, make the recommendation **conditional** and identify the blocking evidence. Never pretend to know exact scale, traffic, budgets, or compliance rules.

## Example

**User:** “It should support lots of people.”

**Bad:** “So 100,000 concurrent users and Kubernetes.”

**Better:** “Is this more like a small internal tool or a public service with unpredictable peak traffic? The peak workload matters more than total signups. If you don't know yet, I can recommend a simple starting architecture and specify what we'd measure before scaling.”
