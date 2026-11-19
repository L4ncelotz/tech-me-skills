# Multi-Service Compose Fixture (Eval Fixture Only)

Synthetic fixture repository with a Node.js API, a Python background worker, PostgreSQL, and Redis orchestrated via `docker-compose.yml`.

## Overview

Handles webhook ingestion (`api`) and asynchronous notification/report jobs (`worker`) queued through Redis, persisting state in PostgreSQL.
