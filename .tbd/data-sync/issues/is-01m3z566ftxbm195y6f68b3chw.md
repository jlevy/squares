---
type: is
id: is-01m3z566ftxbm195y6f68b3chw
title: "W2: reference timing route for verify.cpp at any direction"
kind: task
status: open
priority: 3
version: 1
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T20:34:14.137Z
updated_at: 2026-10-02T20:34:14.137Z
---
benchmarks/bench_measure_verifier.py times verify.cpp per direction through audit_wand125_rectangles --control, which refuses directions where its scale-weights mutation premise fails (n32@r50, every n61 cell). Whole-certificate --replay works but costs hours. A single-direction replay option in the audit tool (owned by the coordinator, since its internals are off-limits to W2) would let the campaign time any cell.
