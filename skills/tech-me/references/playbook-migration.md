# Boundary & Migration Playbook

Load only when evaluating monolith vs modular monolith vs microservices, or migrating an existing system (`X -> Y`). Never propose a rewrite without observed constraint/bottleneck evidence.

## Questions that split options

Ask at most one per turn (0 in `quick` mode), and only if it changes the recommendation:

1. **Observed bottleneck or pain:** What measurable problem triggers this change (p95 latency, DB contention, deploy coupling across teams, compliance boundary)?
2. **Coupling & schema state:** Are modules sharing database tables directly, or already behind clean interfaces?
3. **Downtime & rollback tolerance:** Can the system take a scheduled maintenance window, and how will you roll back if migration fails?

## Decision ladder (least disruptive first)

1. **Stay + targeted fix:** Profile queries, add indexes, fix N+1s, or tune worker concurrency when the current stack is stable and bottlenecks are localized.
2. **Modularize in-place (Modular Monolith):** Enforce module boundaries and separate schemas/interfaces inside one deployable before splitting network boundaries.
3. **Incremental extraction (Strangler / Expand-Contract):** Extract only the specific component with isolated scaling, security, or runtime requirements behind a stable contract.
4. **Full migration / rewrite:** Last resort when the current platform is EOL, legally blocked, or fundamentally incapable after targeted fixes.

## Mandatory migration risk checklist

- **Data backfill & parity:** How existing records move and how consistency is verified (dual-write, CDC, or batch backfill + checksums).
- **Expand-contract schema changes:** Add new columns/tables → dual-read/write → backfill → switch readers → drop old columns only after soak period.
- **Rollback path:** Explicit trigger and steps to revert traffic/schema without data loss.
- **Dual-system tax:** Operating old + new systems simultaneously doubles monitoring, auth, and debugging surface during transition.

## Common traps

- **Rewriting languages for "speed"** (e.g., `.NET/Node -> Go`) when the measured bottleneck is unindexed SQL queries or external API latency.
- **Splitting microservices with a shared database** — gains distributed network latency while keeping monolithic coupling.
- **Big-bang cutover** with no incremental validation or tested rollback plan.

## Evidence to check

- Profiler/APM traces showing where time is actually spent (app CPU vs DB vs network).
- Dependency map across modules/tables (`ARCHITECTURE.md`, manifests, or entrypoints).
- Measured incident rate and deployment lead time on the existing system.
