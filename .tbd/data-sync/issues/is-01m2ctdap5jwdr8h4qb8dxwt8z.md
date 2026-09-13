---
type: is
id: is-01m2ctdap5jwdr8h4qb8dxwt8z
title: Integrate accepted BC329 calibration tooling onto PR156
kind: task
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - integration
dependencies:
  - type: blocks
    target: is-01m2b884n0ms50xp93q6aaps1g
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
child_order_hints:
  - is-01m2cv85q2ajjgsnx7076ta8cp
created_at: 2026-09-13T07:23:51.876Z
updated_at: 2026-09-13T07:38:31.521Z
---
Merge the independently accepted calibration branch, observed-worker-topology implementation, and maintained three-profile coordinator onto the current PR156 leaf. Resolve overlap by preserving the accepted CAL-5 ownership/lifecycle controls and the newer topology/coordinator contracts; run focused and edit-tier validation on the combined head; obtain source-distinct exact-head reviews for topology and coordinator/reader boundaries; update the run-sheet/docs and PR body; push and wait for hosted CI. Do not execute any positive full-shape profile or BC329 scientific target.

## Notes

Integrated calibration cd02a0cd, observed topology 087905cb, and profile coordinator 88f55cfd onto PR156 at clean local head faa4085db8fb4cf42154afec0022a0585f59196d. Conflict resolution retained PR156 runner hardening and exact CAL-5 staging ownership while combining topology sidecars. Target-free integrated suite: 226 passed in 26.78s. Edit tier: all 45 selected steps passed in 75.78s; Ruff 1791 files clean and BasedPyright zero. Three source-distinct exact-head reviews are active. No positive profile or BC329 target ran.
