---
type: is
id: is-01m0vcsx46hxye3g2f1h0s6tme
title: Use the gate-managed Python environment for focused negative controls
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex@spud10
labels:
  - packing
  - validity
dependencies: []
parent_id: is-01m0vbg75b3j30f9eq2j678b9j
hold: null
hold_until: null
created_at: 2026-08-25T02:43:16.742Z
updated_at: 2026-08-25T02:44:51.758Z
started_at: 2026-08-25T02:43:21.508Z
closed_at: 2026-08-25T02:44:51.757Z
close_reason: Discarded the invalid dependency-incomplete focused transcript, logged D-224, and reran through the pinned uv environment; all 55 negative controls fired as expected in 10 wall-seconds.
resolution: null
duplicate_of: null
---
A merge-review focused command launched tools/negctl.py via an absolute virtualenv interpreter without putting that environment on PATH. The private snapshots therefore resolved their configured python3 commands to a dependency-incomplete system interpreter and emitted 42 irrelevant tracebacks. Record the attempt as invalid evidence, rerun through the same uv/gate environment as test.sh, and retain only the correctly receipted result.
