---
type: is
id: is-01m7669mgkdahg27hv3qp6dckm
title: Import de Winter's s(132) <= 11.976048383604 and s(157) <= 12.993302611344 (JoostdeWinter/square-packing a491dad/6617869, no issue; report by first commit)
kind: task
status: closed
priority: 1
version: 8
delegate: bold-ritchie-l104
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T20:55:21.870Z
updated_at: 2026-11-12T01:41:03.026Z
started_at: 2026-11-11T20:55:27.152Z
closed_at: 2026-11-12T01:41:03.026Z
close_reason: "Done: #961 merged (75cce00b6), T-292/T-293 houses at 132/157; 958 final reply posted and closed, recorded by #965 (0352d7554); check_bead_tree --before-close ok."
resolution: null
duplicate_of: null
---

## Notes

Lane L104 (bold-ritchie-l104), 11 November 2026.

Issue jlevy/squares#958 (20:56:18Z), registration request at JoostdeWinter/square-packing 6617869; folders first committed at a491dad (20:49:44Z). Push not read; ledger dates by the issue with first commit kept (no other report at 132/157 in the window).

Claims and state:
- T-292: s(132) <= 11.9760483836034076, V3/C3, S3 (review-confirmed). New arrangement, 9.63e-03 below T-174. Adopted as the house at 132 on 11 November 2026.
- T-293: s(157) <= 12.9933026113432237, V3/C3, S3. First below the grid 13 (k = 13 for s(k^2-k+1) < k). Adopted as the house at 157; integer conjecture withdrawn.
- Credit: de Winter after Samanyu-dev (pinwheel at 109).
- Margins: T-174 and grid margins 0 (RV-3 n/a); own margins 1.248e-59 / 1.349e-59.

Review: L105 (docs/project/reviews/review-2026-11-11-dewinter-132-157.md) accepted both, 14 notes; mapped (V-de-winter-958-review-check, E-de-winter-s132/s157-review-exact-feasibility, external_review on four atoms, reviews on T-292/T-293). F11/F14/F12 (think-71uq)/F8-F10 and the six questions folded in.

Regularization: grid-slack 0.5-degree views at both counts (packing/cases/regularized_drawings/think-bcfs-2026-11-11/); Daniel's solves above the sides, held at row 4.

PR https://github.com/jlevy/squares/pull/961 (draft), head 245aaabc9, hosted CI green (31 success, 28 skipped). Merged L100's head and main through 2fe557598 (#955, which records #954's final reply). Senior review fixes done; landed stamped 2026-11-12.

Next: the replies lane answers #958 after merge (findings F8-F10 and six questions for the author). Landed 2026-11-12; if merged on a later day, stamp_landed --apply and re-pin.
