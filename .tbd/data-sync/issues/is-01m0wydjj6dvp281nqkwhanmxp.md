---
type: is
id: is-01m0wydjj6dvp281nqkwhanmxp
title: Make deep golden comparison semantic across YAML wrapping
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - ci
  - tests
dependencies: []
parent_id: is-01m0wqx97nb22qwx8v47hrpfqk
created_at: 2026-08-25T17:10:21.509Z
updated_at: 2026-08-25T17:23:24.394Z
closed_at: 2026-08-25T17:23:24.393Z
close_reason: "PR #39 CI/review repairs: deep golden comparison now uses parsed YAML semantics with real-drift diffs; the SIGINT cleanup test synchronizes from the child instead of polling a timer; the synopsis interpretation now matches the canonical detector/class data. Focused deep validation, five repeated interruption runs, the fast gate, and the complete 32-surface gate pass."
resolution: null
duplicate_of: null
---
PR #39 macOS CI passed the complete packing gate, then failed the focused deep golden check solely because PyYAML wrapped one note at a different column. Replace byte equality with parsed YAML equality for the generated basin map, preserve readable diffs for semantic drift, add a regression test for wrapping-only changes, record the defect, and rerun deep/local/CI checks.
