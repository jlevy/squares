---
type: is
id: is-01m0wypgrdq63wm2xtdxvvktnt
title: Remove timer race from SIGINT process-cleanup regression
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - tests
  - ci
dependencies: []
parent_id: is-01m0wqx97nb22qwx8v47hrpfqk
created_at: 2026-08-25T17:15:14.571Z
updated_at: 2026-08-25T17:23:24.403Z
closed_at: 2026-08-25T17:23:24.403Z
close_reason: "PR #39 CI/review repairs: deep golden comparison now uses parsed YAML semantics with real-drift diffs; the SIGINT cleanup test synchronizes from the child instead of polling a timer; the synopsis interpretation now matches the canonical detector/class data. Focused deep validation, five repeated interruption runs, the fast gate, and the complete 32-surface gate pass."
resolution: null
duplicate_of: null
---
PR #39's fast suite failed because test_run_selected_interrupt_stops_detached_production_process sent SIGINT after a two-second polling deadline even when the child start marker was absent, then asserted the marker existed. Make the child write its marker and signal the parent itself, preserving real process-group cleanup assertions without scheduler-dependent polling; record and validate the recurrence.
