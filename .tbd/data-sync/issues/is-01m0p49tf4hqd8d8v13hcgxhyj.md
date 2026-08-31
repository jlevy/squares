---
type: is
id: is-01m0p49tf4hqd8d8v13hcgxhyj
title: "meter: pair-tests as the budget currency"
kind: task
status: open
priority: 2
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p4at6z9sdaabcqmave9t9d
parent_id: is-01m0p49s01h862tq6wp0dd085c
child_order_hints:
  - is-01m0wa24fag1y7x34bs3qs6s76
created_at: 2026-08-23T01:38:28.964Z
updated_at: 2026-08-25T11:16:37.905Z
---
Review R-10. Thread a pair-test counter through the pipeline and have sqsearch emit it. Switch budgets, saturation thresholds and every proposer comparison to pair-tests (tiers S/M/L = 1e9/1e11/1e13); report wall clock alongside as a courtesy. Necessary as soon as proposers with different move semantics are compared. Update campaign/README.md's metric vector and accept rule to match.

## Notes

Checkpoint a9330d6 completes the exact Rust meter seam only: one pair_test is one actual search-side pair_depth evaluation; ordinary and basin-entry Outcomes/JSONL/summaries emit checked counts, with fixed setup and verifier work excluded. Session-011 order 7 then compared archived baseline 2eda548 to meter a9330d6: deterministic ordinary and basin-entry JSON matched exactly after deleting only timing/new-meter fields; independent counts matched n=11 (640,004,455), n=4, overshoot and zero-budget controls. The predeclared 04:13 PT host guard rejected timing (load >2, idle 38-70%, one 60% CPU competitor), so overhead remains unmeasured and no performance retention claim is made. Full pair-budget enforcement, S/M/L tiers, saturation thresholds, campaign schemas/adapters, cross-proposer comparisons, and first unmetered adapter quench_experiment.anneal remain open. Child think-dprg/D-283 tracks zero-step nontermination found by the count review.
