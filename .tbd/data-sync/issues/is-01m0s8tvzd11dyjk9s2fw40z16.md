---
type: is
id: is-01m0s8tvzd11dyjk9s2fw40z16
title: Bound and terminate individual negative-control checks
kind: bug
status: closed
priority: 2
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - packing
  - focus-infrastructure
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T06:55:25.164Z
updated_at: 2026-08-24T22:55:29.695Z
closed_at: 2026-08-24T22:55:29.694Z
close_reason: Every mutation-control command now has a finite deadline, isolated process group, TERM then KILL cleanup and reaping, plus a TERM-ignoring-child test. Fresh per-control bytecode roots also prevent same-size rapid mutations from executing stale code. All 38 controls pass with one and ten workers.
resolution: null
duplicate_of: null
---
Private snapshots close D-035's live-tree sabotage path, but tools/negctl.py still gives each checker no deadline and shell grandchildren no bounded cleanup. Add a per-control timeout expressed in the control contract or one documented default, launch each checker in its own process group, terminate and reap that group on timeout/interruption, record the timeout as a control failure, and rehearse a TERM-ignoring child. Keep this cooperative and local; no repository lease or adversarial capability system.
