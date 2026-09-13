---
type: is
id: is-01m2ctdap5jwdr8h4qb8dxwt8z
title: Integrate accepted BC329 calibration tooling onto PR156
kind: task
status: in_progress
priority: 1
version: 6
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
updated_at: 2026-09-13T07:56:48.878Z
---
Merge the independently accepted calibration branch, observed-worker-topology implementation, and maintained three-profile coordinator onto the current PR156 leaf. Resolve overlap by preserving the accepted CAL-5 ownership/lifecycle controls and the newer topology/coordinator contracts; run focused and edit-tier validation on the combined head; obtain source-distinct exact-head reviews for topology and coordinator/reader boundaries; update the run-sheet/docs and PR body; push and wait for hosted CI. Do not execute any positive full-shape profile or BC329 scientific target.

## Notes

Local PR156 now includes accepted calibration, worker topology, coordinator, and the coordinator topology-consumer repair through commit 0cc0311a. Root target-free integrated validation: 242 passed in 24.59s; focused Ruff check/format and BasedPyright are clean. The independent reader, exact-head reviews, durable run sheet, docs, push, PR body, and hosted CI remain. Remote PR156 is still 52e4ab65; PR148/149/156 remain open and their current hosted checks are green. No profile or BC329 ran.
