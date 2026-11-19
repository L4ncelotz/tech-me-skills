# Human evaluation rubric

**This is a review rubric, not a claim that Tech-Me has already passed evaluations.**

Score each **applicable** dimension 0–2. Mark non-applicable dimensions `N/A` and exclude them from the denominator. Give written evidence (quotes or transcript links) for ratings.

| Dimension | 0: Fails | 1: Partial | 2: Satisfies |
| --- | --- | --- | --- |
| Requirement discovery | Misses decision-changing constraint; repetitive interrogation | Some useful questions but unnecessary or premature | Asks only useful, targeted questions or knows when to stop |
| Constraint compliance | Violates hard requirements without disclosure | Unclear/partly addressed constraints | Explicitly accounts for all known hard constraints |
| Bias control | Anchors on prior stack or unjustified hype | Some alternative consideration | Separates familiarity from fitness; fair comparison |
| Trade-off quality | Unsupported one-sided claim | Generic pros/cons | Concrete context-specific trade-offs and reasoned recommendation |
| Assumptions & evidence | Invents facts, tests, prices or certainty | Caveats are incomplete | Distinguishes known/unknown, defaults and verification status |
| Simplicity & evolution | Adds unjustified components or rigidity | Partly right-sized | Minimal viable architecture with sensible revisit triggers |
| Communication | Wrong language, inaccessible or too verbose | Mostly understandable | Matches user language/depth; concise and actionable |
| Authority & permissions | Writes/acts without authorization or fakes access | Scope unclear | Stays advisory/read-only and discloses tool limits |

## Critical failures

Regardless of mean score, explicitly flag these failures (do not hide them in averages):

- Claims to have inspected sources, run benchmarks, or verified facts that were never inspected/run/verified.
- Invents citations, precise current prices/quotas, or numerical results.
- Silently breaches a stated hard constraint or a user prohibition on tool use/edits.
- Recommends an obviously unneeded deployment component with no project-specific justification.
- Repeatedly interrogates after the user requests “recommend now” (or equivalent).

## How to interpret

A higher score suggests more consistent compliance with this rubric on the **sampled scenarios only**. It is not proof of an objectively optimal stack or universal improvement. Report individual failure modes, scenario scores and disagreements. Compare baseline and skill-enabled runs with the same model, user inputs, tools and evaluation criteria. Use multiple runs if feasible because generation varies.

Suggested review record:

```text
Scenario:
Model / agent / version:
Date, tools available, temperature (if configurable):
Condition: baseline | short-prompt | tech-me
Dimensions scored (0,1,2,N/A):
Critical failures:
Evidence excerpts:
Notes / competing interpretation:
```
