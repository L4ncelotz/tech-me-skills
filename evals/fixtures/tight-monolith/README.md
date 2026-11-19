# Tight Monolith Fixture (Eval Fixture Only)

Synthetic fixture repository for evaluating Tech-Me's read-only architecture review and boundary analysis.

## Overview

Single Node.js/TypeScript process handling orders, billing, and inventory against one shared PostgreSQL database. Modules import each other's internals and query shared tables directly.
