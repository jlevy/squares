---
type: is
id: is-01m2ymzj2ts1jh3bn536pkhtrp
title: "PR 199: port computational boundary repairs and pass the full checkpoint"
kind: task
status: open
priority: 1
version: 2
labels:
  - correctness
dependencies:
  - type: blocks
    target: is-01m2ymzy4tz2n47g8ttd8qspv0
parent_id: is-01m2ymyd4zef0ckcx8gvq3p5dx
created_at: 2026-09-20T05:35:17.593Z
updated_at: 2026-09-20T05:35:29.945Z
---
Start from current PR199 and the preserved reviewed head c877006b. Port the earliest-layer corrections from PR202: 181 steps imply 182 half-tangents and 363 doubled directions; preserve solver-status diagnostics and allow only explicit infeasible status to mean solver infeasibility; validate raw marginal shape/finiteness before clipping; reject unsupported integral-piercing angle limits and column multiplicities. Include the initial point-LP boundary and regression controls for failures, malformed vectors and both infinity signs. Reconcile T027-era counts at this layer without importing future T028–T030 results. Preserve certificate payloads and accepted claims. Done when the complete incremental diff is independently reviewed, the retained T027 decision remains valid, current head/main identity is recorded, and matching fast plus substantive deferred checkpoint receipts cover the full validation set at that revision. Push fixes in the owning branch, preserve unrelated commits, and hand its new head to the PR200 bead. Do not merge.
