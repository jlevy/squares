---
type: is
id: is-01m2ctdap5jwdr8h4qb8dxwt8z
title: Integrate accepted BC329 calibration tooling onto PR156
kind: task
status: in_progress
priority: 1
version: 11
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
  - is-01m2e0e4ct972w6eapcr8c3xjz
  - is-01m2e7adq6sc2j6mzgsx89sg8h
created_at: 2026-09-13T07:23:51.876Z
updated_at: 2026-09-13T23:52:26.658Z
---
Merge the independently accepted calibration branch, observed-worker-topology implementation, and maintained three-profile coordinator onto the current PR156 leaf. Resolve overlap by preserving the accepted CAL-5 ownership/lifecycle controls and the newer topology/coordinator contracts; run focused and edit-tier validation on the combined head; obtain source-distinct exact-head reviews for topology and coordinator/reader boundaries; update the run-sheet/docs and PR body; push and wait for hosted CI. Do not execute any positive full-shape profile or BC329 scientific target.

## Notes

Local PR156 head fc3e314d is 21 commits ahead of remote 52e4ab65 and includes accepted CAL1-7, topology, coordinator, and source-distinct reader. Independent reader REFUSE at 212e0dfc identified six admission classes (child beads think-14qi/a43a/un4u/cxdu/pt2f/b6tb); independent coordinator rereview REFUSE at fc3e314d found three further classes (think-3291/ind2/d9xh). Separate Sol agents repairing disjoint source/test files. Root added durable reviews and target-free run sheet to dirty docs; documentation map/link check passes. PR body, final gates, push, and hosted CI remain; current remote green checks apply only to old head. No positive profile or BC329 ran.
