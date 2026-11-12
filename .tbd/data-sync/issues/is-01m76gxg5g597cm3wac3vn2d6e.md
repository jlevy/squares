---
type: is
id: is-01m76gxg5g597cm3wac3vn2d6e
title: "Import #962: Doğa Özden's s(269) <= 16.899469075856 (kenaznia-doga/s269-upper-bound-16899469076 @ fdab2c00), 1.526e-3 below his own T-290"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l120
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-12T00:00:58.544Z
updated_at: 2026-11-12T01:50:32.932Z
started_at: 2026-11-12T00:43:45.124Z
---

## Notes

## Lane L120 (bold-ritchie-l120), 12 November 2026

Branch `claude/bold-ritchie-xo28us-l120`, cut from `origin/main` `75cce00b6`. Draft PR #966 (https://github.com/jlevy/squares/pull/966), head 972f73d6e after merging main 0352d7554 (#965: conflicts in result-requests.yaml #958 notes and the pin, both kept) and re-pinning.

**Stage 2, retained.** `ozden-s269-issue962-2026-11-11` (same-day name collision with T-290's `ozden-s269-upper-bound-2026-11-11`, named as L107 named #959's), pinned at kenaznia-doga/s269-upper-bound-16899469076 fdab2c0 (23:34:47Z, 17 s before the issue; #947 comment 6809799112 six seconds after). Both stated digests hold (candidate 54b408b2...6b26b, JSON 4b7ac2a7...9cc0); acquire_source --check PACKET_MATCHES_ITS_CONTRACT. Pinned-only: diff PNG by digest; verifier/README.md, sqcheck.py, Evan Daniel's MIT notice identical_to the s299, s232 and evand-issue845 copies. CC BY 4.0 data / MIT code. House T-290 (author's own #947).

**Stage 4 replay (blind to L117).** Controls plan before any run (scratch l120/notes/controls-plan.md, SHA-256 4484bf96...3b84, 00:46:52Z). certify 3 jobs, 216,276 pair decisions, 59.25 route CPU-s; check --replay passed; sharp-controls 11, all as expected (square 103 already touches its wall). 11 wall contacts (103 bottom, 155 top, 158 and 160-167 left); least pair gap 2.034e-13 (squares 10, 13). Intake commit cb2955e8c, before the review branch was read.

**Measurements.** Gain 1.5255e-3 below T-290 (2.045e-3 below T-174). T-290 margin 3.238228e-12 (1-lambda* 2.036494e-13, pair 119-202), gain/margin 4.71e8, within_margin false: RV-3 not reached. Own margin 3.234057e-12 (pair 10-13), contracted side 16.89946907585181 (not registered, RV-3). Identity vs T-290: not one to one; 115 beyond 0.1, 134 beyond 0.01, 230 beyond 1e-3, largest 1.12355; 116 turned >1 deg (centred); 45 tilted >1 deg (+1 at 0.55, 46 beyond 0.5, 16 at -42.88) vs T-290's 100. vs T-174: new, 65 beyond 0.1. House witness same; regularized view same but 112 beyond 0.1. L-step scan identical to main's.

**Review mapped (L117, 1b37943b9, merge b6af9163c).** Accepted, 12 findings all notes, S3. Reconciliation: least pair gap, T-290 and own contraction receipts (margin, lambda*, pair, contracted side) and measure_identity receipts (T-290, T-174, tilts) equal exactly. V-ozden-962-review-check, E-ozden-962-review-exact-feasibility, external_review, document map, T-296 reviews. F2-F12 folded; F10 think-71uq (review named think-mdxq, closed 4 Nov); six questions in packet README, entry, requests notes.

**Adopted and regularized (56277b01c).** 269 from T-290 to T-296 on 12 Nov; T-290 no house source, superseded (test_result_status); T-290 next_rung updated. Credit phrase names seed packings' improvers. grid-slack 1-degree view drawn (17,52,29,54,19 -> 1,3,0,24,19; 651/826 -> 836/854), mirror across rising diagonal; Evan Daniel same-side refused (unmatched rotation); KKT solve 3.39e-12 below side (1.05 of own margin) held row 3 (RV-3). Rigidity 217 translate (195 before); gate n=1..324 2,482/6,421. Custody 74 houses, 248 inputs, 80 mutations refused. stamp_landed --apply done (269: T-296, 2026-11-12). Release record 2026-11-12-bold-ritchie-l120-962-t296.yaml. Re-pin f6efb568a.

**Held / for the coordinator.** check_results contiguity red until T-294 (#964) and T-295 (#963) merge; then merge main again (conflicts expected: upper_bound_reports HOUSES, tests roster, results.yaml last_reviewed/regularized_drawings, upper_bound_houses LATER_PASSES "2026-11-12", prior-state archive 2026-11-12 (L107 also writes it), document map, flowmarkignore, workflow paths, SYNOPSIS counts, validate SCREEN_FINDINGS, resources README, site_resources, landings, release pin), rederive, re-pin. Bead tree was red on main's #958 entry naming think-bcfs until #965; green after the merge. Main has unformatted n-132.md, n-157.md, think-bcfs README from #961 (not touched here).
