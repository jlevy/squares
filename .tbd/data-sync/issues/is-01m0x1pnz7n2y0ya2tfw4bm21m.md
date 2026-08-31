---
type: is
id: is-01m0x1pnz7n2y0ya2tfw4bm21m
title: Golden note's committed form depends on a soft-wrap boundary; emit unwrapped or assert in the generator
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-08-25T18:07:45.639Z
updated_at: 2026-08-25T19:05:43.613Z
closed_at: 2026-08-25T19:05:43.579Z
close_reason: "Resolved by the landed frontier contract: #31's semantic golden comparison (its D-320/D-324 work) closes the wrap-sensitivity class outright."
resolution: null
duplicate_of: null
---
Follow-up to D-329 (bead think-d2ah): the golden basin-map note is a constant string whose committed bytes depend on where yaml.safe_dump(width=100) breaks the line, so any future edit to that sentence re-arms the same trap, and only the macOS deep step can see it. Two hardening options from the PR 33 thread: emit the note unwrapped (width=inf or a literal block scalar), or assert the canonical rendering inside check_golden_basins so every platform's normal gate catches drift. Also record: PyYAML 6.0.1 and 6.0.3 wrap this exact string differently, so any regeneration must run under the uv.lock-pinned version (6.0.3) - a local system python can produce wrong bytes. The same latent drift exists on the branch carrying f31c490 and will fail the deep step when it merges.
