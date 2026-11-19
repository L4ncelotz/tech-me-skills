# Hosting & Compute Playbook

Load only when choosing where and how to deploy, scale, or operate workloads. Verify current hosting limits and pricing against primary docs if tools permit; never invent current tiers.

## Questions that split options

Ask at most one per turn (0 in `quick` mode), and only if it changes the recommendation:

1. **Existing infrastructure / compliance:** Must it run on an existing VM/on-prem server or inside a specific cloud/region?
2. **Workload shape:** Request/response web API, long-running background jobs/WebSockets, or scheduled batch work?
3. **Operations capacity:** Who patches OS, TLS, backups, and restarts if something breaks at 2 AM?

## Option comparison

| Option | Strongest fit | Weakest fit / disqualifier | Revisit trigger |
| :--- | :--- | :--- | :--- |
| **Existing VM / Single VPS (+ Compose)** | Steady internal tools, predictable cost, stateful monolith + DB on one host, team knows basic Linux | Zero ops capacity for OS/security patching, or multi-region low-latency mandate | CPU/memory headroom consistently >70–80% (**estimate — not measured**; basis: burst and OS page-cache headroom, confirm on host metrics) or availability requires multi-node failover |
| **Managed PaaS (containers/apps)** | Small teams wanting git-push deploys, managed TLS/rollbacks, and minimal server maintenance | Strict on-prem/air-gapped requirements, or predictable high-baseline compute where managed markup dominates | Managed tier cost/egress exceeds self-managed threshold or platform execution limits block a core workflow |
| **Serverless Functions** | Event-driven/bursty workloads, webhooks, low idle traffic, stateless short-lived requests | Long-running workers, persistent WebSockets, cold-start-sensitive flows, heavy stateful DB pooling | Cold-start p95 violates user SLA, or execution duration/connection limits force awkward workarounds |
| **Kubernetes / Multi-service Orchestration** | Multiple independent teams/services needing custom scheduling, isolation, and dedicated platform ops | Small teams (<10 devs) or 1–3 deployables without dedicated platform engineering | Only adopt when organizational/deployment coupling genuinely exceeds simpler single-host or PaaS tooling |

## Common traps

- **Defaulting to Kubernetes** for a 1–2 service app when a single VPS or managed PaaS meets every requirement at a fraction of the ops burden.
- **Picking Serverless for a stateful monolith** and then bolting on external connection poolers, queues, and workarounds for timeouts.
- **Ignoring operational ownership:** "cheap VPS" is not cheap if nobody maintains backups, firewalls, and security updates.

## Evidence to check

- Current vendor pricing, free-tier quotas, execution timeouts, and egress terms (never cite from memory).
- Deployment frequency, rollback speed, and backup/restore procedure.
