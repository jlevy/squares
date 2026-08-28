---
type: is
id: is-01m135srx94798mfge4jfc17jv
title: "PR #43 review L1-L6: low-severity Motion Lab cleanups"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m135s5773qphv8g2qf3c999v
created_at: 2026-08-28T03:14:47.848Z
updated_at: 2026-08-28T03:14:47.848Z
---
L1 hard-coded palette modulus (free-quench.js:59); L2 dead substring-matched stop outcome (quench.py:1157); L3 stale download filename inputs (free-quench.js:678); L4 revokeObjectURL race (line 680); L5 unannotated _emit_observation params; L6 in-place snapping-toggle mutation (line 367) and forced re-enable (line 394).
