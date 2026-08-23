---
type: is
id: is-01m0p49tf4hqd8d8v13hcgxhyj
title: "meter: pair-tests as the budget currency"
kind: task
status: open
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p4at6z9sdaabcqmave9t9d
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T01:38:28.964Z
updated_at: 2026-08-23T01:41:01.168Z
---
Review R-10. Thread a pair-test counter through the pipeline and have sqsearch emit it. Switch budgets, saturation thresholds and every proposer comparison to pair-tests (tiers S/M/L = 1e9/1e11/1e13); report wall clock alongside as a courtesy. Necessary as soon as proposers with different move semantics are compared. Update campaign/README.md's metric vector and accept rule to match.
