---
type: is
id: is-01m5q623ssynf7fnwc7m8pqpqr
title: "OR-1: move the pose-by-pose identity measurement and the sharp controls into devtools"
kind: task
status: open
priority: 3
version: 1
labels:
  - tooling
  - packing
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T14:46:57.081Z
updated_at: 2026-10-24T14:46:57.081Z
---
Five upper-bound packets now carry their own copy of the same two measurements: measure/identity.py (evand-regularized-2026-10-20 holds the measures; mishapolk-n204-2026-10-22, amundsk-n303-2026-10-23 and evand-kaggle-descents-2026-10-24 load them by file path, and the T-240 review wrote a clean-room one) and receipts/sharp_controls.py (mishapolk-n204-2026-10-22, amundsk-n303-2026-10-23/replay, and evand-kaggle-descents-2026-10-24, which takes --packet and --n). OR-1: build the tool once.

Done looks like: devtools.measure_identity (nearest centre under the eight symmetries via check_half_angle_area.arrangement_gap, plus the optimal assignment, over packets read through upper_bound_reports.read_facts and binary64 x-y-degrees inputs) and a sharp-controls subcommand of devtools.upper_bound_reports writing receipts/sharp-controls[-nNNN].json, each with tests; the retained per-packet programs stay as written (their receipts are bound to them), and later packets call the tools. The triage of think-6r5p proposed the same (devtools.measure_identity).
