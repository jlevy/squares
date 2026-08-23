---
type: is
id: is-01m0rbwvahqzsexrv6kwgv35g0
title: "D072: exercise the real crash and concurrency lifecycle"
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:41.328Z
updated_at: 2026-08-23T22:29:41.328Z
---
The current crash selftest bypasses the standalone lease and checker subprocess, while the atomic control tests an already-held marker rather than simultaneous acquisition. Replace these with end-to-end process death and exactly-one-winner rehearsals.
