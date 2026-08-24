---
type: is
id: is-01m0s8tvzd11dyjk9s2fw40z16
title: Bound and terminate individual negative-control checks
kind: bug
status: open
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - packing
  - focus-infrastructure
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T06:55:25.164Z
updated_at: 2026-08-24T21:22:12.589Z
---
Private snapshots close D-035's live-tree sabotage path, but tools/negctl.py still gives each checker no deadline and shell grandchildren no bounded cleanup. Add a per-control timeout expressed in the control contract or one documented default, launch each checker in its own process group, terminate and reap that group on timeout/interruption, record the timeout as a control failure, and rehearse a TERM-ignoring child. Keep this cooperative and local; no repository lease or adversarial capability system.
