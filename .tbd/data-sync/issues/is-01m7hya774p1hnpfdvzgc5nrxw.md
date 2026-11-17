---
type: is
id: is-01m7hya774p1hnpfdvzgc5nrxw
title: "Intake: record JonathanGun 5971b95 local-minimum/ section and #1001 comment 6912585795; correct no-KKT-claim statements for T-305..T-309; compare with held KKT candidates"
kind: task
status: closed
priority: 1
version: 7
delegate: bold-ritchie-l188
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-16T10:26:45.603Z
updated_at: 2026-11-16T12:31:18.388Z
started_at: 2026-11-16T10:26:49.172Z
closed_at: 2026-11-16T12:31:18.388Z
close_reason: "Done: #1002 (T-305..T-309 at 127/204/232/264/305) and #1003 (local-minimum read, corrections) merged; #1001 reply posted and recorded in #1004 (merged f9ddfeeef)."
resolution: null
duplicate_of: null
---

## Notes

L188 (bold-ritchie-l188), 16 November 2026, from 10:26Z, worktree branch claude/bold-ritchie-xo28us-l188 from origin/main d451e3d83.

Read: JonathanGun/square-packing-upper-bounds cloned at 10:27Z, ls-remote head 5971b95f7141bb9bd1bac4b501bc3a094fb84822 (09:28:39Z), only child of 0aac839e; it adds local-minimum/ (28 files) and edits README.md and LICENSE.md; every other blob unchanged, the five candidate SHA-256 equal #1001's list. #1001 comment 6912585795 (09:29:26Z) and body edit (09:29:27Z) read; the body drops "We make no optimality, rigidity or KKT claim.", certificate line still 0aac839e.

Retained: packet joegun-local-minimum-2026-11-16 (acquire_source, 31 files, 30 retained, Evan Daniel's notice pinned against evand-issue845 LICENSE); acquire_source --check PACKET_MATCHES_ITS_CONTRACT.

KKT comparison (test_the_sources_local_minimum_check_reaches_the_points_the_driver_holds): the author's exactsolve reports, read through regularize_evand.solve_block, equal the think-0y9m driver's held solves at 127, 232, 264, 305 in status, gate, S_exact (every printed digit, 63/63/62/63 decimals), S_cert (as fraction = solved view side), free, promoted (22 at 232), second_order (52/110/155/132 flat motions), vv_milp_dS; both fail at 204 with the same free squares. Inputs differ (author from decimal poses at evand 6067db5, driver from certificates at 675a5ea). Gaps below certificates 1.2175e-10, 4.0164e-9, 1.9066e-11, 1.9146e-10 as the record prints. Nothing registered; KKT sides stay held for RV-3 (think-ruu2).

Corrected no-KKT statements: earlier packet README, its declaration+sources claims (identical edit, --check passes), evidence E-joegun-1001-certificate-report limitations, results.yaml T-305..T-309 claim + notes (RESULTS.md regenerated), bibliography note, resources README row, source-coverage notes, result-requests #1001 (read_through 09:29:26Z, result local-minimum-check not_registered, beads +think-664l, notes). Case records n-127..n-305 unchanged: their generated sentence says the proof says nothing about optimality, which stays true. intake-watch: a read at 5971b95 was drafted and dropped because intake_sweep notes a packet now pins the head and its changed paths are retained (read can be removed); L187's 0aac839e read stays.

Validation so far: packing-validate --records 55/55 after render_results --update; 889 + 304 tests in touched modules pass; suite_files check passes; intake_sweep lists no 5971b95 or #1001 comment item.

Coordinator's scope addition (11:0xZ): #914 issuecomment-6914444483 (10:55:42Z) and #927 issuecomment-6914444869 (10:55:43Z) recorded as kind: follow-up replies, reported T-268 / T-275 only (V3/C3, confirmed, superseded), no corrects, notes paragraphs; read_through unchanged. Sweep: items without an owning bead 2 -> 0; no #914/#927 follow-up rows.

Incident: a compare_paper_renders run was stopped (TaskStop) mid-run after the follow-up edit; its finally-restore did not run, leaving origin/main's copies of results.yaml, result-requests.yaml and source-coverage.yaml in the tree, and the first follow-up commit was built on main's result-requests.yaml (reverting #1001's changes). Caught by git status; files restored, follow-ups reapplied on commit 2's file, commit amended before any push. Rerun without interruption: all four papers byte-identical across three renders.

Commits (16 November UTC): 02b091536 packet + test; cf6b7ed38 corrections; 2ef66f7a6 #914/#927 follow-ups; 90a62fbc1 no-public-change record; fe39ec54d release: re-pin DATA_REVISION to cf6b7ed3 (stamp_landed --apply: nothing to stamp). Pushed claude/bold-ritchie-xo28us-l188; draft PR https://github.com/jlevy/squares/pull/1003.
Final local validation on fe39ec54d: --edit 71/71, --records 55/55, 16 touched modules 1,276 passed 1 skipped, check_release_impact all dispositioned, release_pin --check ok, both packets PACKET_MATCHES_ITS_CONTRACT.

Hosted CI on fe39ec54d: Packing validation 43855599070 failed only in suite-c, test_house_adoption::test_the_receipt_of_the_custody_run_names_every_input_and_house: devtools/house-custody-2026-10-11.json pins joegun-upper-bounds-2026-11-16/acquisition/sources.json, which cf6b7ed38 edited (claim sentence). Certificate page 43855599187 and Branch mergeability 43855430264 passed. Fix 1b4595192 (11:28Z): declaration.json and sources.json back to main's bytes (the record states what the source said at its pin, still true); the README, evidence, register prose, bibliography and requests entry carry the correction. test_house_adoption + test_acquire_source + lane module 151 passed locally; release_pin --check ok (pin cf6b7ed38, no data change after). Not a D-509 flake.

Hosted CI on head 1b45951924cde6680be5eb669206f63986e13dc9: Packing validation 43858038476 success (12 jobs succeeded, 12 skipped), Certificate page 43858038516 success, Branch mergeability 43858027308 success. PR #1003 (draft) body updated with both CI rounds. Handoff: nothing registered; the stage 7 reply on #1001 stays with think-0y9m; this bead can close once #1003 merges.
