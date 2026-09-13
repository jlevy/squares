---
type: is
id: is-01m2b80wcx8cm9vb2m97cx7s4s
title: Best-of-k is one draw with no spread; report it over disjoint blocks
kind: bug
status: open
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels:
  - workbench-roadmap
  - workbench-phase-1
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2b80wrktzpknr73k8s3vkwm
  - type: blocks
    target: is-01m2ckzy45b1b28pvt1nbh4gdm
created_at: 2026-09-12T16:43:15.228Z
updated_at: 2026-09-13T05:43:45.315Z
---
Phase 1 measurement repair. Implement a committed reporter for attempted/completed/accepted/rejected counts, explicitly denominated rates, absolute/relative excess and guarded grid-to-reference normalization, CPU work, and disjoint-block best-of-k distributions with block counts and uncertainty. Include unsuccessful blocks rather than silently resampling accepted trials; label conditional metrics and prefix observations. Recover raw inputs or a compact lossless/durable equivalent before claiming old numerical tables reproduce; retained summaries cannot reconstruct disjoint blocks. Acceptance: recorded seed/block/work manifest and known synthetic mixed/empty/zero-gap controls reproduce expected results. The supplied handoff tables remain unverified observations until durable inputs support them.

## Notes

2026-09-12 review: raw files used for the pasted block table are absent from this Git tree; summaries alone do not recover block extrema or pose-level checks. Recover retained raw artifacts or replay the exact frozen instrument/seed ranges; retain a reusable aggregator plus block/sample/seed manifest and output. Mark prefix ladders as one prefix observation meanwhile, distinguish planned budget from completed counts, exclude rejected trials from the budget-success denominator only when the metric explicitly calls for conditional validity. See updated annealing plan.
