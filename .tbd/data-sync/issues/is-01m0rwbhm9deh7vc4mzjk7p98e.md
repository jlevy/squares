---
type: is
id: is-01m0rwbhm9deh7vc4mzjk7p98e
title: Repair H-028 continuity-impossible uniqueness criterion
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - focus-soundness
  - research
dependencies: []
parent_id: is-01m0rpqqcarvbbtswbgnxd7cvp
created_at: 2026-08-24T03:17:20.136Z
updated_at: 2026-08-24T03:27:15.298Z
closed_at: 2026-08-24T03:27:15.297Z
close_reason: H-028 now asks for one refined local minimizer recovered near the reference plus a boundary gap, not uniqueness of a grid point inside a positive value tolerance. D-119 records the validity error; schemas, ledger, synopsis, format checks and the 118-second full gate pass.
resolution: null
duplicate_of: null
---
H-028 currently requires the published angle point to be the only refined-grid point within a fixed 1e-5 objective tolerance. Any continuous value sheet has arbitrarily close neighboring points inside that tolerance, so refinement makes the accept rule impossible. Replace it with a declared angular exclusion radius, a boundary margin, and local-minimum/feature checks; record the error in the defect log and reconcile the strategy review.
