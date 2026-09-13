---
type: is
id: is-01m2ctdap5jwdr8h4qb8dxwt8z
title: Integrate accepted BC329 calibration tooling onto PR156
kind: task
status: in_progress
priority: 1
version: 8
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
updated_at: 2026-09-13T18:02:48.182Z
---
Merge the independently accepted calibration branch, observed-worker-topology implementation, and maintained three-profile coordinator onto the current PR156 leaf. Resolve overlap by preserving the accepted CAL-5 ownership/lifecycle controls and the newer topology/coordinator contracts; run focused and edit-tier validation on the combined head; obtain source-distinct exact-head reviews for topology and coordinator/reader boundaries; update the run-sheet/docs and PR body; push and wait for hosted CI. Do not execute any positive full-shape profile or BC329 scientific target.

## Notes

Local PR156 head fc3e314d includes accepted CAL1-7 calibration, observed topology, maintained coordinator, source-distinct reader, and coordinator repair; remote PR156 remains older at 52e4ab65. Root 121 focused tests and static gates passed after repair; records/edit tiers passed before final documentation formatting. Independent reader review REFUSED six admission boundaries; repair and exact-head rereview active. Coordinator exact rereview and T1 independent review active. Run sheet and docs drafted but uncommitted; PR body, push, hosted CI remain. No positive profile or BC329 target ran.
