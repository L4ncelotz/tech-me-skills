# Database & Storage Playbook

Load only when comparing databases, storage engines, caching, or persistence trade-offs. Do not invent prices, quotas, or benchmark numbers.

## Questions that split options

Ask at most one per turn (0 in `quick` mode), and only if it changes the recommendation:

1. **Write concurrency & topology:** Single-writer local/VM app, or multiple app instances writing concurrently?
2. **Consistency & transactions:** Strict ACID transactions (money, inventory, booking locks), or eventual consistency / append-only logs acceptable?
3. **Persistence environment:** Persistent disk on a VM/volume, or ephemeral serverless/container filesystem?
4. **Data shape & access:** Structured relational joins, blob/media files, full-text/vector search, or time-series aggregation?

## Option comparison

| Option | Strongest fit | Weakest fit / disqualifier | Revisit trigger |
| :--- | :--- | :--- | :--- |
| **SQLite (embedded)** | Single-node app, CLI/desktop, offline-first, low-to-moderate concurrent writes, minimal ops | Multiple stateless app servers sharing one DB, ephemeral container disks without persistent volume, heavy parallel write contention | Sustained write-lock errors (`SQLITE_BUSY`) after WAL tuning, or horizontal multi-instance scaling required |
| **PostgreSQL (single primary)** | Multi-instance web apps, strict ACID, relational + JSONB + basic search/queues in one system | Offline desktop/embedded tools where running a DB server adds unjustified friction | Read saturation after query/index tuning (add read replica), or specialized analytical/search latency bottleneck |
| **Managed / Specialized (Object storage, Redis, Search)** | Blobs/files (object storage), ephemeral rate-limits/sessions (cache), high-scale full-text/analytics | Adding extra datastores on day one before primary DB proves insufficient | Measured latency, storage cost, or query failure that the primary relational DB cannot absorb cleanly |

## Common traps

- **Adding Redis/queues/search on day one** when one relational database handles early workload and simplifies backups/consistency.
- **Confusing registered users with concurrent writers:** 10,000 total users rarely equals heavy concurrent writes.
- **Putting SQLite on ephemeral hosting** where redeploys wipe local disk.
- **Storing large binary blobs inside the database** instead of object storage or filesystem + metadata pointer.

## Evidence to check

- Actual write rate and lock behavior in the target workload (not generic microbenchmarks).
- Backup, point-in-time recovery, and restore drill requirements.
- Estimated monthly data growth and retention window (label unmeasured figures **estimate — not measured**).
