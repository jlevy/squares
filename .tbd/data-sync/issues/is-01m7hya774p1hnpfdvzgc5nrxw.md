---
type: is
id: is-01m7hya774p1hnpfdvzgc5nrxw
title: "Intake: record JonathanGun 5971b95 local-minimum/ section and #1001 comment 6912585795; correct no-KKT-claim statements for T-305..T-309; compare with held KKT candidates"
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l188
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-16T10:26:45.603Z
updated_at: 2026-11-16T10:54:30.378Z
started_at: 2026-11-16T10:26:49.172Z
---

## Notes

L188 (bold-ritchie-l188), 16 November 2026, from 10:26Z, worktree branch claude/bold-ritchie-xo28us-l188 from origin/main d451e3d83.

Read: JonathanGun/square-packing-upper-bounds cloned at 10:27Z, ls-remote head 5971b95f7141bb9bd1bac4b501bc3a094fb84822 (09:28:39Z), only child of 0aac839e; it adds local-minimum/ (28 files) and edits README.md and LICENSE.md; every other blob unchanged, the five candidate SHA-256 equal #1001's list. #1001 comment 6912585795 (09:29:26Z) and body edit (09:29:27Z) read; the body drops "We make no optimality, rigidity or KKT claim.", certificate line still 0aac839e.

Retained: packet joegun-local-minimum-2026-11-16 (acquire_source, 31 files, 30 retained, Evan Daniel's notice pinned against evand-issue845 LICENSE); acquire_source --check PACKET_MATCHES_ITS_CONTRACT.

KKT comparison (test_the_sources_local_minimum_check_reaches_the_points_the_driver_holds): the author's exactsolve reports, read through regularize_evand.solve_block, equal the think-0y9m driver's held solves at 127, 232, 264, 305 in status, gate, S_exact (every printed digit, 63/63/62/63 decimals), S_cert (as fraction = solved view side), free, promoted (22 at 232), second_order (52/110/155/132 flat motions), vv_milp_dS; both fail at 204 with the same free squares. Inputs differ (author from decimal poses at evand 6067db5, driver from certificates at 675a5ea). Gaps below certificates 1.2175e-10, 4.0164e-9, 1.9066e-11, 1.9146e-10 as the record prints. Nothing registered; KKT sides stay held for RV-3 (think-ruu2).

Corrected no-KKT statements: earlier packet README, its declaration+sources claims (identical edit, --check passes), evidence E-joegun-1001-certificate-report limitations, results.yaml T-305..T-309 claim + notes (RESULTS.md regenerated), bibliography note, resources README row, source-coverage notes, result-requests #1001 (read_through 09:29:26Z, result local-minimum-check not_registered, beads +think-664l, notes). Case records n-127..n-305 unchanged: their generated sentence says the proof says nothing about optimality, which stays true. intake-watch: a read at 5971b95 was drafted and dropped because intake_sweep notes a packet now pins the head and its changed paths are retained (read can be removed); L187's 0aac839e read stays.

Validation so far: packing-validate --records 55/55 after render_results --update; 889 + 304 tests in touched modules pass; suite_files check passes; intake_sweep lists no 5971b95 or #1001 comment item.
