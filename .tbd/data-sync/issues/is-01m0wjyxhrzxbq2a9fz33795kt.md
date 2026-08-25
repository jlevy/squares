---
type: is
id: is-01m0wjyxhrzxbq2a9fz33795kt
title: Record recurrence of explicit Flowmark target on generated ledger
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/agent-sessions/session-012-eight-hour-final-continuation.md
delegate: codex-subagent
labels:
  - packing
  - bookkeeping
  - process
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T13:50:06.904Z
updated_at: 2026-08-25T13:52:24.230Z
closed_at: 2026-08-25T13:52:24.229Z
close_reason: Recorded D-313, regenerated ledger through canonical renderer, and all focused checks pass.
resolution: null
duplicate_of: null
---
A checkpoint command explicitly passed generated campaign/ledger.md to Flowmark, bypassing .flowmarkignore and reproducing D-259. Record the recurrence in defects.yaml, regenerate the ledger, synchronize derived counts and exact mutation anchors, add the bounded correction to session 012, run focused checks, and close only after freshness and controls pass.
