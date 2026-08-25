---
type: is
id: is-01m0p49tf4hqd8d8v13hcgxhyj
title: "meter: pair-tests as the budget currency"
kind: task
status: open
priority: 2
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p4at6z9sdaabcqmave9t9d
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T01:38:28.964Z
updated_at: 2026-08-25T10:52:13.947Z
---
Review R-10. Thread a pair-test counter through the pipeline and have sqsearch emit it. Switch budgets, saturation thresholds and every proposer comparison to pair-tests (tiers S/M/L = 1e9/1e11/1e13); report wall clock alongside as a courtesy. Necessary as soon as proposers with different move semantics are compared. Update campaign/README.md's metric vector and accept rule to match.

## Notes

Checkpoint a9330d6 completes the exact Rust meter seam only: one pair_test is one actual search-side pair_depth evaluation; ordinary and basin-entry Outcomes/JSONL/summaries emit checked counts, with fixed setup and verifier work excluded. Full pair-budget enforcement, S/M/L tiers, saturation thresholds, campaign schemas/adapters, and cross-proposer comparisons remain open. First unmetered adapter: quench_experiment.anneal discards the all-chain summary.
