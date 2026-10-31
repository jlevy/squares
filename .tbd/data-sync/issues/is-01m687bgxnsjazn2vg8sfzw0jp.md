---
type: is
id: is-01m687bgxnsjazn2vg8sfzw0jp
title: Review Daniel's 172, 204, 260, 293 certificates (stage 4) and adopt all four with both regularizations (#845)
kind: task
status: open
priority: 1
version: 1
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m685ngekhjw1cxgta3763s3s
created_at: 2026-10-31T05:36:39.349Z
updated_at: 2026-10-31T05:36:39.349Z
---
Stage 4 review of Evan Daniel's #845 certificates at 172, 204, 260 and 293 (T-256 on the lane's branch) and the adoption at all four, where each is the smallest reported side.

## Validation
- Claim: s(172) <= 2723587139676283080823463207799/(2*10^29) (exact KKT point), s(204) <= 14807627471881579627471866771703/10^30, s(260) <= 8316991251060941991251052624833/(5*10^29) and s(293) <= 8816991251061390991251052573823/(5*10^29) (dilation certificates), search/packer/candidates/s*_1028.cert at evand/square-packing d2d5dd9 (unchanged at the pin 0e76d9f), packet evand-issue845-2026-10-29; checkers: the two maintained exact routes (done, with sharp controls) and a clean-room exact checker written by the reviewer.
- Run: a tbd-strong-max review sub-agent in its own worktree reading the packet as data; then the adoption at 172, 204, 260 and 293 with both strong generators (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, the render step and the flip, in one pull request; withdraw the conjectured optimum 17.63414634146341 at 293, which the new house is below.
- Cost: the review about 0.05 CPU-hours; the regularization 20 to 100 CPU-minutes for four counts; an estimate.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: a strong-tier review lane the coordinator launches.
- Done when: the review is mapped on the entry, check_results derives V3/C3, and the four counts are adopted and regularized with default_drawings --check-state --base-ref origin/main and flip_regularization --check passing.
- Machine note: minutes of CPU for the review; run the regularization apart from a gate.
