---
type: is
id: is-01m2dzaq79t4tthvy0z800752y
title: "Coordinator: bind result.json bytes across inventory readback"
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b883ztxn7qazs98bndea6b
hold: blocked
hold_until: null
created_at: 2026-09-13T18:09:03.720Z
updated_at: 2026-09-13T18:13:03.254Z
---
Independent exact-head review at fc3e314 found a second read of result.json after preflight could accept symlink or same-size JSON swap, yielding inconsistent receipt/artifact digests. Use one safe retained byte snapshot or identity-bind reopens and add race controls.
