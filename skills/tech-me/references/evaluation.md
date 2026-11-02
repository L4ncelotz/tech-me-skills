# Constraint-first evaluation and evidence

## 1. Build a decision frame

- **Decision**: one clearly scoped question; avoid redesigning an entire system for a narrow choice.
- **Hard constraints**: must be true, e.g., OS, required legacy integration, legally mandated hosting, offline operation, explicit budget ceiling.
- **Primary priorities**: most relevant outcomes and operations concerns.
- **Secondary preferences**: familiar tools, developer ergonomics, aesthetics, or nice-to-haves.
- **Evidence**: direct codebase observation, user report, current documentation, tested behavior, benchmark, or unverified model knowledge. Don't conflate them.

Reject an option only for a real disqualifier. If all options violate a hard constraint, don't silently weaken it. Request an explicit trade-off or state the infeasibility.

## 2. Compare credible candidates

Use 2–3 alternatives when meaningful. Consider:

- **Fitness** for business workflow, concurrency, transactions, latency and availability.
- **Delivery cost** in team effort, complexity and dependency management.
- **Operations**: monitoring, recovery, backups, upgrades, failure modes.
- **Ecosystem**: integration support, maturity, security maintenance, documentation.
- **Change cost**: data migration, vendor lock-in, deployment migration, team onboarding.

Do not compare “Go is fast” with “Node is popular” as if they were equivalent measures. Connect any claimed advantage to the user's workload, environment, and priorities. A validated existing system may be better than a theoretically superior greenfield stack.

## 3. Evidence hierarchy (context dependent)

- **Direct constraints / repo findings**: inspect permitted files for the actual current state; explain which files substantiate a conclusion.
- **Primary documentation**: use current official docs for version, platform compatibility, support policies, pricing, limits and features.
- **Representative workload measurements**: prefer measured results from the user's workload and environment, with configurations disclosed.
- **Case studies / third-party tests**: provide limitations; results may not transfer.
- **General reasoning**: useful for design trade-offs but not proof of a numerical claim.

If web access is missing, state that version, prices or support lifecycle were not verified. Time-sensitive claims should not be asserted as confirmed from memory. Treat benchmark rankings as context, not architecture decisions.

## 4. Bias challenge

For the leading candidate, ask the canonical check used across this skill:

**Would this still be the right choice if the user had a different technical background, while holding actual team, migration, and operating costs fixed?**

Supporting checks:

- Was it preferred because it is fashionable, heavily represented in training data, or used by this user previously?
- Did I fairly consider a plausible alternative that fulfills the same constraints?
- Am I overestimating future load, adding unnecessary services, or overlooking operations cost?
- Are we improperly assuming monolith, microservices, managed cloud, SQL or NoSQL is always best?

Note: prior experience can legitimately reduce delivery risk, so removing its effect entirely is not required or desirable.

## 5. Evaluation and validation outputs

A concise comparison can contain:

| Option | Constraint fit | Best reason to choose | Main cost / risk | When it wins |
| --- | --- | --- | --- | --- |
| A | Pass / Fail / Unknown | Workload-specific | Concrete | Conditions |
| B | Pass / Fail / Unknown | Workload-specific | Concrete | Conditions |

Avoid unsupported 9/10 scores, invented percentages, and false precision. Prefer stated conditionals over numeric confidence scores. Every unmeasured number you introduce must be labeled **estimate — not measured** with its basis, or replaced by a relative/qualitative comparison; do not present plausible-sounding figures as measured facts. For consequential unresolved issues, propose a small PoC, compatibility test, cost estimate or representative load test with a clear pass/fail measure.
