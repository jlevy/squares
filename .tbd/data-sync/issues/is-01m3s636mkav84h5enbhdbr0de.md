---
type: is
id: is-01m3s636mkav84h5enbhdbr0de
title: Audit Rust rectangle exact clipping broad phase
kind: task
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rcka78kmcccpetknr2mswh
created_at: 2026-09-30T12:54:37.970Z
updated_at: 2026-09-30T12:54:55.742Z
closed_at: 2026-09-30T12:54:55.741Z
close_reason: Existing exact polygon AABB broad phase fully covers the proposed optimization; stopped without redundant code or benchmark.
resolution: null
duplicate_of: null
---
Read-only assessment of proposed exact bounding-box prefilter before changing the frozen Rust geometry backend. Stop without a diagnostic if the current coverage kernel already computes each polygon bounding box once and skips all density rectangles whose closed projections cannot have positive-area overlap.

## Notes

Stopped at static precondition check. Rust sqverify_exact/src/lib.rs SHA07fc7c68c1a13a498f88a31f893b7703b51b2499cb9f8441982a8a2669e1a6d0, coverage() lines274-296: after degenerate rejection, computes polygon min/max x/y exactly once (lines277-285); every rectangle is skipped before intersection_area when right<=left, left>=right, top<=bottom, or bottom>=top (lines287-295). Boundary equality is already skipped as zero area. Python rectangle_density.py lines604-620 has the same broad phase. Proposed absent-filter optimization is already implemented, so no alternative code, focused controls, or speed comparison was run; a paired old-vs-proposed result would compare identical algorithms. Prior fixed-work batching diagnostic think-48gl found no material transport gain; child arithmetic remains the broad measured cost, but a finer hot-path profile is required before choosing a different optimization. No proof source changed.
