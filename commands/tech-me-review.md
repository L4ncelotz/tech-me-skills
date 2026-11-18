---
description: Read-only Tech-Me architecture review of the current repository (manifests and configs first).
argument-hint: [focus area or path]
---

Load the `tech-me` skill (via the `Skill` tool if available) and execute **`review`** mode on the current workspace:

- **Fast inspect order (read-only):**
  1. Package/dependency manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.)
  2. `README.md`, `ARCHITECTURE.md` / `docs/adr/` (if present), and deployment/infra configs (`docker-compose*`, `Dockerfile`, CI workflows)
  3. Only the specific entrypoints or interfaces required to verify an architectural claim
- **Strict exclusions:** Never read or quote `.env` or secret files, `node_modules`, build outputs, or lockfiles. Never claim to have inspected files you did not actually open.
- **Output:** State confirmed repo findings separately from assumptions, evaluate bottlenecks/overengineering/risks against actual constraints (do not propose a rewrite without evidence), label unmeasured figures **estimate — not measured**, and include observable revisit triggers.

Focus (optional): $ARGUMENTS
