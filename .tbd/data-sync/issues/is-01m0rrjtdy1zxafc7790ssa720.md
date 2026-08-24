---
type: is
id: is-01m0rrjtdy1zxafc7790ssa720
title: Record why -C target-cpu=native is deliberately off
kind: chore
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:11:24.221Z
updated_at: 2026-08-24T02:11:24.221Z
---
sqsearch has no .cargo/config.toml and no target-cpu setting. On this float-heavy kernel native codegen would plausibly be worth 10-30%, and it is the obvious thing for a future reader to reach for.

It must stay off, and the reason should be written down where that reader will look: enabling it lets the compiler contract multiplies and adds into FMAs, which changes float results. This project keys determinism on (seed, chain) and records an engine_commit so a configuration can be regenerated from the numbers in its artifact. A binary whose arithmetic depends on the host CPU breaks that, and would also break the byte-frozen golden (think-lwao) on any machine but the one that generated it.

Put it in sqsearch/Cargo.toml next to the existing lint-floor rationale.
