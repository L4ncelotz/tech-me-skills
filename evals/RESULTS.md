# Behavioral Evaluation Report — Step 6

**Date:** 2026-10-29  
**Model:** `google-antigravity/gemini-3.8-flash` (via live evaluation harness)  
**Configuration:** Identical model and sampling parameters for baseline and skill-enabled runs  
**Evaluator:** Systematic rubric review per `evals/RUBRIC.md` and `evals/RUNBOOK.md`  

> **Historical report (v0.1.0):** Recorded on 2026-10-29 against `SKILL.md` SHA-256 `10831862b219976e492d050d2030c74a4ea5953c0c32d4b7a30568da80b280f6`, before the v0.1.1 changes to discovery, bias control, revisit triggers, and estimate labeling. These scores must not be read as validating those changes.

---

## Executive Summary

We evaluated Tech-Me against the baseline model across the three prioritized representative scenarios specified in the project roadmap:
1. **New SaaS project with incomplete requirements** (`unknown-scale-defaults`)
2. **Existing application considering architecture migration** (`migration-first-existing-project`)
3. **User strongly preferring a familiar tech stack that may not be optimal** (`historical-preference-bias`)

Each condition produced **one response per scenario (n = 1)**, single-turn prompts only; see [Limitations of This Run](#limitations-of-this-run).

### Aggregate Score Summary (0–2 scale per dimension, max 16)

| Scenario ID | Baseline Score | Tech-Me Score | Key Behavioral Difference |
| :--- | :---: | :---: | :--- |
| `historical-preference-bias` | 12 / 16 | **14 / 16** | Tech-Me delivered a structured comparative criteria table and resisted stack bias, but bundled two questions and quoted unverified memory figures. |
| `unknown-scale-defaults` | 7 / 16 | **15 / 16** | Baseline prescribed an opinionated stack before knowing product requirements. Tech-Me established provisional defaults and asked for the product domain, though revisit triggers were implicit. |
| `migration-first-existing-project` | 15 / 16 | **16 / 16** | Both models resisted microservices hype; Tech-Me distinguished itself with structured "Microservices Tax" trade-offs and a precise bottleneck metric question. |
---

## Detailed Evaluation by Scenario

### Scenario 1: Biased Stack Preference (`historical-preference-bias`)

* **Category:** `bias`
* **User Prompt:** `"I love Next.js because I used it for three past apps. For a low-traffic device telemetry collector that must run on an existing Linux VM, should we use Next.js for ingestion too?"`
* **Context:** Low-traffic device telemetry ingestion on Linux VM; user biased toward familiar Next.js.

#### Rubric Evaluation
| Dimension | Baseline | Tech-Me | Notes / Evidence |
| :--- | :---: | :---: | :--- |
| **Requirement Discovery** | 1 | 1 | Baseline dumped 3 separate exploratory questions; Tech-Me asked a focused closing question but bundled two distinct requirements (reporting protocol/format AND whether an admin dashboard runs on the same VM), partially departing from the single-question rule. |
| **Constraint Compliance** | 2 | 2 | Both respected the Linux VM and low-traffic constraint. |
| **Bias Control** | 2 | 2 | Both separated familiarity from workload fitness. |
| **Trade-off Quality** | 1 | 2 | Tech-Me provided a structured comparative criteria table contrasting Next.js with headless services. |
| **Assumptions & Evidence** | 1 | 1 | Baseline cited specific memory numbers (70–150MB) without qualification; Tech-Me similarly quoted runtime memory figures (~50–80 MB for Fastify/Node, ~15–30 MB for Go binary) without citing verifiable benchmark conditions or empirical measurement methodology. |
| **Simplicity & Evolution** | 2 | 2 | Both recommended lightweight Node (Fastify) or Go/Python alternatives. |
| **Communication** | 1 | 2 | Tech-Me was more compact and organized. |
| **Authority & Permissions**| 2 | 2 | Both remained advisory. |
| **Total** | **12 / 16** | **14 / 16** | **Tech-Me Advantage: Discovery efficiency, structured criteria comparison (offset by unverified RAM figures and question bundling).** |
* **Critical Failures:** None observed.

---

### Scenario 2: Incomplete Requirements & Unknown Scale (`unknown-scale-defaults`)

* **Category:** `unknowns`
* **User Prompt:** `"I want to build a small SaaS but I have absolutely no clue about user count, concurrency, or budget. Please don't keep asking me those questions."`
* **Context:** Early-stage greenfield SaaS; user explicitly halts capacity/budget questioning.

#### Rubric Evaluation
| Dimension | Baseline | Tech-Me | Notes / Evidence |
| :--- | :---: | :---: | :--- |
| **Requirement Discovery** | 0 | 2 | **Baseline Failure:** Immediately prescribed an entire tech stack (Next.js + Vercel + Supabase + Stripe + Resend) without knowing what the SaaS does. Tech-Me stopped capacity questions and asked what the product workflow is. |
| **Constraint Compliance** | 1 | 2 | Baseline acknowledged the stop instruction but bypassed product discovery. Tech-Me honored the stop instruction while preserving sound engineering principles. |
| **Bias Control** | 0 | 2 | Baseline anchored on default web-framework hype stack. Tech-Me remained neutral until product requirements are defined. |
| **Trade-off Quality** | 0 | 2 | Baseline offered zero alternative trade-offs. Tech-Me staged the decision process properly. |
| **Assumptions & Evidence** | 1 | 2 | Baseline presented free-tier quotas as permanent facts. Tech-Me clearly labeled assumptions as provisional defaults. |
| **Simplicity & Evolution** | 1 | 1 | Baseline assumed standard web app; invalid for non-web SaaS. Tech-Me kept architecture options open with provisional defaults, but did not explicitly specify concrete metric thresholds or revisit triggers alongside the defaults. |
| **Communication** | 2 | 2 | Both responses were clear and polite. |
| **Authority & Permissions**| 2 | 2 | Advisory only. |
| **Total** | **7 / 16** | **15 / 16** | **Tech-Me Advantage: Prevented premature stack lock-in; transparent provisional defaults.** |
* **Critical Failures:** Baseline committed to premature architecture selection in the absence of domain knowledge. Tech-Me committed zero critical failures.

---

### Scenario 3: Monolith Architecture Migration (`migration-first-existing-project`)

* **Category:** `existing-project`
* **User Prompt:** `"Our existing monolith uses .NET and SQL Server and has few incidents. Should we migrate everything to Go microservices for performance? No code changes yet."`
* **Context:** Stable enterprise monolith; user contemplating speculative microservices rewrite.

#### Rubric Evaluation
| Dimension | Baseline | Tech-Me | Notes / Evidence |
| :--- | :---: | :---: | :--- |
| **Requirement Discovery** | 1 | 2 | Baseline provided long general advice; Tech-Me asked for the specific performance metric or bottleneck triggering the desire to migrate. |
| **Constraint Compliance** | 2 | 2 | Both treated low incident count and existing stability as key assets. |
| **Bias Control** | 2 | 2 | Both resisted the "Go microservices = instant speed" myth. |
| **Trade-off Quality** | 2 | 2 | Both detailed database bottleneck vs runtime speed and distributed transaction complexity. |
| **Assumptions & Evidence** | 2 | 2 | Factual comparison of modern .NET capabilities and network hop overhead. |
| **Simplicity & Evolution** | 2 | 2 | Both recommended profiling and surgical extraction over wholesale rewrite. |
| **Communication** | 2 | 2 | Concise, professional, and well-structured. |
| **Authority & Permissions**| 2 | 2 | Advisory only; no unauthorized repo inspection claimed. |
| **Total** | **15 / 16** | **16 / 16** | **Tech-Me Advantage: Concrete staged migration framing and decisive closing question.** |

* **Critical Failures:** None observed.

---

## Observations from the Sampled Scenarios Only

With one response per condition per scenario, these observations describe the sampled transcripts above. They do not support claims of consistent behavior across models, agents, or repeated runs.

1. **Premature stack commitment observed in the baseline (`unknown-scale-defaults`):** With fundamental product details unknown, the sampled baseline response prescribed a named stack (Next.js + Vercel + Supabase + Stripe) as "battle-tested" before knowing what the product does; Tech-Me asked about the core workflow and labeled traffic and budget assumptions as provisional defaults. This is one observed transcript, not a demonstrated consistent pattern.
2. **Discovery discipline mixed:** In `migration-first-existing-project`, the sampled Tech-Me response closed with a single focused question about the actual bottleneck metric. In `historical-preference-bias`, Tech-Me instead bundled two requirements into one turn (reporting protocol/format and dashboard co-location), deviating from its own single-question rule. Question-bundling should be re-checked in future runs.
3. **Comparison formatting:** Tech-Me's sampled responses used criteria-based comparison tables or structured cost framings (for example, the "Microservices Tax") in two of three scenarios. Formatting alone is not a quality guarantee, but it made trade-offs easier to check in these transcripts.
4. **Unverified figures in both conditions (`historical-preference-bias`):** Tech-Me quoted rough runtime RAM ranges (~50–80 MB Node/Fastify, ~15–30 MB Go) and the baseline quoted different ranges (70–150 MB and 10–30 MB), neither with measurement methodology. Both were penalized under *Assumptions & Evidence*. Future versions should label such figures as unmeasured heuristics or verify them against primary sources.
5. **Provisional labeling:** Where unknowns appeared (traffic, budget, scale), the sampled Tech-Me responses marked them as provisional assumptions rather than asserted facts, matching the fixture's expected behaviors.

## Limitations of This Run

- **Sample size:** one response per condition per scenario; generation variability was not sampled.
- **Scenario coverage:** 3 of 14 fixture scenarios in [scenarios.json](scenarios.json); only the `unknowns`, `existing-project`, and `bias` categories were exercised. Multi-turn interviews — including the scripted stopping fixture that checks "recommend now" discipline and whether already-answered constraints get re-asked — were not part of this run.
- **Model and configuration:** a single model (`google-antigravity/gemini-3.8-flash`) at temperature 0.0 on 2026-10-29; other models or sampling settings may behave differently.
- **Scores describe these transcripts only** and are not certification of the skill.
