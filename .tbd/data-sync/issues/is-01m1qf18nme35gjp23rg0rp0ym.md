---
type: is
id: is-01m1qf18nme35gjp23rg0rp0ym
title: "Exact sweep: bound the worker count by memory and cores, and replace the forced fork context with a safe fallback"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T00:20:59.187Z
updated_at: 2026-09-05T00:20:59.187Z
---
PR 80 replaces the exact sweep's forced fork context (chosen on this branch because Python 3.14's forkserver re-imports __main__ and a stdin or REPL caller has none) with: the platform default context, a serial fallback when __main__ is not an importable file (_process_pool_is_safe), a worker cap of 4, and a concurrent-grid memory budget of 512 MiB estimated from (2N+2)^2 * 8 bytes per direction. Its argument -- forcing fork from library code is unsafe when the host process has threads -- is sound; the cost is that a threaded host or a large certificate runs serially where it ran in parallel. Decide with a measurement: the n = 20 decision at 4 workers versus 1 on this box, and whether any caller runs with threads. Port the memory bound either way.
