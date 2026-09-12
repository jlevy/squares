---
type: is
id: is-01m2ayh5000tkvsjyk2tt3tvxv
title: Enforce BC329 external deadline across process launch and wait
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T13:57:22.559Z
updated_at: 2026-09-12T14:33:18.232Z
---
Independent review of c516a592 showed supervise_worker computes remaining time before Popen and reuses that stale value in process.wait. A launch that consumes seven seconds under a ten-second allowance can therefore receive eight more seconds instead of one. Recompute remaining immediately after launch, terminate or classify unresolved when the deadline is exhausted, and add a deterministic clock-advance control. Decide and document the narrower boundary for an operating-system Popen call itself, or introduce a separately bounded launcher if a true end-to-end guarantee is retained. Verify clocks, cleanup, receipt classification, focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.

## Notes

Repair committed as 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe. supervise_worker now checks the deadline before launch, recomputes the remaining allowance after Popen, and terminates/reaps the new process group when launch consumes the budget. The schema and docs explicitly scope the operating-system Popen call as an unbounded interval; enforcement resumes immediately on return and termination grace follows the deadline. Deterministic clock controls cover both reduced wait and post-launch exhaustion. Validation: 98 fixed-core tests passed in 11.40 s; repository Ruff and BasedPyright reported zero findings; packing-validate --edit passed in 55.66 s. Keep open pending source-distinct review. BC329 was not registered or run.
