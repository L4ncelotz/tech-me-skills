---
description: Fast-forward Tech-Me architecture recommendation with zero discovery questions.
argument-hint: <question or stack comparison>
---

Load the `tech-me` skill (via the `Skill` tool if available) and execute **`quick`** mode for the request below:

- **Zero questions:** Do not ask any clarifying questions. Lead directly with a practical recommendation (or a clearly conditional recommendation if a critical unknown makes a single answer unsafe).
- **Bias & constraint check:** Separate hard constraints from user familiarity/history. Ask: *Would this still be the right choice if the user had a different technical background, while holding actual team, migration, and operating costs fixed?*
- **Transparent defaults & estimates:** Mark every gap-filling default as a provisional assumption with an observable revisit trigger (`Revisit when: ...`). Label any unmeasured numeric figure **estimate — not measured** with its basis.
- **Read-only:** Do not edit files, install packages, or run deployments.

Request: $ARGUMENTS
