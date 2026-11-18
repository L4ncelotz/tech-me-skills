---
description: Evaluate a proposed architecture or stack migration (cost, downtime, rollback, staged path).
argument-hint: <from X to Y or migration question>
---

Load the `tech-me` skill (via the `Skill` tool if available) and execute **`migrate`** mode for the proposed transition below:

- **Inspect first (if in a repository):** Read manifests, README/ARCHITECTURE docs, and deployment configs first (read-only; skip `.env`/secrets, lockfiles, and `node_modules`).
- **Compare stay vs staged vs rewrite:** Weigh staying on the current system (with targeted fixes), incremental/staged extraction (e.g., modular boundaries, expand/contract, strangler pattern), and full migration.
- **Migration risk gate:** Address actual bottleneck evidence, migration effort, data backfill/consistency, downtime exposure, **rollback plan**, and observable revisit triggers. Label any unmeasured figure **estimate — not measured**.
- **If context is missing:** Ask at most **one** high-impact question (such as the specific bottleneck metric driving the migration), or give a conditional recommendation if the user asked to decide immediately.

Proposed migration: $ARGUMENTS
