---
type: is
id: is-01m0r4jb9qj3fk9sjm9senp9gz
title: negctl leaves the repo holding a deliberate sabotage if it is interrupted
kind: bug
status: open
priority: 0
version: 12
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0pqfp4rm5r4fy7ys6t03h0w
created_at: 2026-08-23T20:21:37.206Z
updated_at: 2026-08-23T23:47:52.532Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
D-035. The in-place negative-control harness saves exact bytes and restores them in finally, but an interrupted process can leave a deliberate mutation behind. Treat this as a cooperative workflow robustness problem, not an adversarial security boundary. Keep the solution small: visible transaction state before mutation, bounded checker timeouts with child cleanup, signal-aware restoration, conservative startup recovery/refusal, and focused crash rehearsals. Do not add per-run worktrees, repository-copy isolation, capability tokens, or a general lease protocol unless measured evidence later requires them.

## Notes

2026-08-23 scope reset. The large isolation/activity-lease implementation and its claims were backed out and preserved in stash@{0}. The stable pushed checkpoint remains a7e7adc: 108-second normal gate, 24 controls, 65 defects. D-035 stays open only for focused cooperative crash recovery and per-control timeout behavior.

Reopened: Reopened under the cooperative-workflow scope: focused interruption recovery and per-control timeout only; no hostile-isolation subsystem.
