---
type: is
id: is-01m5qc91rje7cqb1gaebmnqdpw
title: "Register the regularizer's views of T-240 found by #794: at 303 (3.63e-12 below T-240; driver reports cert_valid false, so it must be certified first) and at 268 (exactly T-242's side; first_certified_in: T-242); retire think-8r5w's 303 candidate (now 2.78e-3 above the house)"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T16:35:35.826Z
updated_at: 2026-10-25T04:57:41.970Z
---

## Notes

2026-10-25, c-h2-268-1025 (H2, think-3anz; PR https://github.com/jlevy/squares/pull/807, merges on or after 2026-10-26T00:00Z):

The 268 part of this bead settles with the adoption of 26 October. T-242 becomes the house best packing at 268, at exactly 8437180857934672912242411148233/(5*10^29). #794's regularizer view of T-240's witness at 268 lies at exactly that side, so once the PR lands it is no longer below the house best packing. Under the house rule, only a regularized view below the house is a smaller packing to register, so this view is no register candidate. The regularized layer at 268 now regularizes T-242's own witness: grid-slack's 1-degree view is admitted at row 10. Evan Daniel's regularizer, run again on T-242's witness, solves it to a certified KKT local minimum within the source's padding, about 1.7e-19 below the side, and draws its view at the house's side (row 7, review queue). No view is below the house (packing/cases/regularized_drawings/think-3anz-2026-10-25/README.md).

What would remain at 268 is an optional record of the old view: a regularization of T-240's retired witness at the side T-242 first states (first_certified_in: T-242). It proves no bound beyond T-242 and no rule requires it. Dropping it from this bead's scope is the recommended course, pending the coordinator's word.

Not taken on here: the 303 view (3.63e-12 below T-240, cert_valid false, to be certified first) and the retirement of think-8r5w's 303 candidate. Both stay with this bead.
