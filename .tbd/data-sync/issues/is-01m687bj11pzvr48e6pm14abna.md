---
type: is
id: is-01m687bj11pzvr48e6pm14abna
title: "Review Polkovskyi's 23 October and #846 refinements (stage 4) and adopt at 15 counts with both regularizations"
kind: task
status: open
priority: 1
version: 2
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m685njhfc113wb8prbg15npb
created_at: 2026-10-31T05:36:40.481Z
updated_at: 2026-10-31T07:29:23.075Z
---
Stage 4 review of Mykhailo Polkovskyi's certificates of 23 October (T-252 on the lane's branch: 154, 155, 183, 211, 227, 236, 237, 241 and 271, each about 1.3e-19 to 1.7e-19 below its house) and of #846 (T-258: 105, 146, 156, 229 and 308, 1e-21 to 1e-41 below each house, and 130, a 2e-14 dilation of Couzo's #843 packing 2.08e-12 below it), and the adoption at each of the fifteen counts where it is the smallest validated side, crediting each packing to its finder and the refinement to Polkovskyi.

## Validation
- Claim: the fifteen exact headers of certificates/0000-0999/nN.cert at Mishapolk/square-packing-records 52aa267 (packets mishapolk-1023-refinements-2026-10-30 and mishapolk-issue846-2026-10-30); checkers: the two maintained exact routes (done, with sharp controls, whose contact margins at 1e-20 to 1e-40 are what the review should read) and a clean-room exact checker written by the reviewer.
- Run: a tbd-strong-max review sub-agent in its own worktree reading both packets as data, with the identity of each certificate against its house (measure/identity-nNNN.json); then the adoption at the fifteen counts with both strong generators (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, the render step and the flip, in one pull request, or split by the runbook if the runs pass the cap.
- Cost: the review about 0.1 CPU-hours for fifteen certificates; the regularization 75 to 375 CPU-minutes (1.25 to 6.25 CPU-hours) for fifteen counts by the runbook's receipts; an estimate.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: a strong-tier review lane the coordinator launches; the owner may rule that sub-print re-certifications in the corpus are restatements (think-fwa9's answer was given for rows beyond 324), which would drop these entries instead.
- Done when: the review is mapped on both entries, check_results derives V3/C3, and each count is adopted and regularized with default_drawings --check-state --base-ref origin/main and flip_regularization --check passing.
- Machine note: the regularization runs are hours of CPU on a shared 4-core host; at most two cores, apart from a gate.

## Notes

2026-10-31: renumbered on the branch after #851's T-252: the 23 October refinements are T-253 and #846's are T-259 (were T-252 and T-258).
