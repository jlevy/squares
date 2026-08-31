---
type: is
id: is-01m0r7rab2j8krgraey9a810x9
title: Build a resumable sharded executor for packing campaigns
kind: feature
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T21:17:18.561Z
updated_at: 2026-08-23T21:17:18.561Z
---
Provide a common batch executor for proposer, quench, pair-test, and certification jobs with deterministic seed assignment, explicit resource budgets, bounded concurrency, atomic artifacts, retry classification, resumable manifests, and shard reconciliation.

Acceptance: representative campaigns resume without duplicate or lost trials; serial and parallel runs agree after canonical ordering; crashes leave valid completed artifacts and explicit failed work; throughput and utilization are benchmarked against the single-process control; and provenance reaches the campaign ledger.
