---
type: is
id: is-01m0t6bjk2tasawtxth6pz5fbg
title: Record per-event wall time in basin archives
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-efficiency
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T15:31:21.301Z
updated_at: 2026-08-24T15:32:12.370Z
closed_at: 2026-08-24T15:32:12.369Z
close_reason: "D-167 fixed: each basin event now retains monotonic wall_seconds; replay requires a finite nonnegative value and selftest rejects a negative mutation. The precommit n=3 data was moved to /tmp and will be regenerated from the clean committed tool."
resolution: null
duplicate_of: null
---
D-167. BasinEvent/v2 retained LP counts but omitted per-event wall seconds, so the autonomous loop could not price or adapt the n sequence from its own evidence. Add finite nonnegative wall_seconds measured around each quench and replay validation. Acceptance: every event retains wall seconds; malformed values fail replay; the first n=3 block reports measured total and per-seed cost.
