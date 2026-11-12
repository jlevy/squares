---
type: is
id: is-01m769qmqxk8mkymbfh6f7jkv2
title: "Import #960: Doğa Özden's s(237) <= 15.893805580573 (kenaznia-doga/s237-upper-bound @ 13c4b231), 8.798e-3 below T-190 (the issue names T-189)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: bold-ritchie-l129
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T21:55:26.589Z
updated_at: 2026-11-12T05:52:58.956Z
started_at: 2026-11-11T22:28:48.841Z
---

## Notes

## Lane L110 (bold-ritchie-l110), 11 November 2026

Branch `claude/bold-ritchie-xo28us-l110`, cut from `origin/main` `b5b12c206`. Draft PR #963 (head 402455e82).

**Stage 2, retained.** `ozden-s237-upper-bound-2026-11-11`, pinned at kenaznia-doga/s237-upper-bound 13c4b23 (21:37:37Z, 13 s before the issue); both stated digests hold (candidate 80687bdc...3833, JSON 98f55b8e...3ca7); acquire_source --check PACKET_MATCHES_ITS_CONTRACT. Pinned-only: the diff PNG by digest; verifier/README.md, sqcheck.py, Evan Daniel's MIT notice identical_to the s299, s232 and evand-issue845 copies. CC BY 4.0 data / MIT code. The issue names T-189 but quotes T-190's side; house is T-190. T-253 (Polkovskyi, pending, T-190's padding) declared as the pending report at 237.

**Stage 4 replay (blind to L109).** Controls plan before any run (scratch l110/notes/controls-plan.md, SHA-256 66243fb8...0f0c, 22:31:31Z). certify 3 jobs, 167,796 pair decisions, 68.10 route CPU-s; check --replay passed; sharp-controls 11, all as expected (square 67 already touches its wall). Walls touched exactly; least pair gap 2.04e-13 (squares 19, 20). Intake commit cb2851d0b, before the review branch was read.

**Measurements.** Gain 8.798e-3 below T-190 (exact). T-190 margin 1.59e-19 (1-lambda* 1.0e-20, pair 54-55), T-189 2.39e-11 (pair 74-103), within_margin false: RV-3 not reached. Own margin 2.985e-12 (pair 36-140). Identity vs T-190: not one to one; 72 beyond 0.1, 111 beyond 0.01, all beyond 1e-3, largest 0.925; 73 turned >1 degree (centred); 42 tilted >1 degree (+1 at 0.83) vs T-190's 49. T-189, house witness, view same. L-step scan identical to main's.

**Review mapped (L109, eaef45205, merge ff282a7fb).** Accepted, F5 minor (author), rest notes, S3. Reconciliation: least pair gap, T-190/T-189 contraction receipts and measure_identity receipts equal exactly. V-ozden-960-review-check, E-ozden-960-review-exact-feasibility, external_review, document map, T-295 reviews. F6 (id; issue named T-189), F8, F9 (40 not 42; copy B not where stated), F10 (think-71uq, not think-mdxq), F12 (dating), eight questions in packet README, entry, requests notes.

**Adopted and regularized.** 237 from T-190 to T-295; T-190 no house source (custody); PRINT_CREDIT_HELD gains 237; prior-state archive gains 237 only. Evan Daniel's same-side view drawn (33,68,68,75,19 -> 0,0,0,2,2; 331/721 -> 788/788), half-turn flip; KKT solve 3.44e-12 below the side held at row 3 (RV-3). SETTLED 237 removed. Rigidity 206 translate (21 before); gate totals n=1..324 2,695/6,587. Custody 73 houses, 240 inputs, 76 mutations refused. Not stamped (still 11 November).

**Held / for the coordinator.** check_results contiguity red until T-292/T-293 (#961) and T-294 (issue 959, L107) merge; bead tree red on main's #954 entry naming think-f65n (closed). Atlas rebuild ran on 4 cores by default before PACK_JOBS=2 was set.

2026-11-11 ~23:58Z, coordinator, after senior review L115 of #963 (head 402455e82). Owed before merge; to be applied in the rebase pass after #961 and #959 merge:
B1: run stamp_landed --apply (landings.yaml n=237 still names T-190; test_stamp_landed and test_home_recent fail), then release_pin --update.
B2: tests/test_render_colors.py:44 "n=1..324": (103, 237), and its docstring at :447-454 (103 at Özden's n = 237, T-295, since 11 Nov; 85 at Couzo's 267 before that).
S1: adopt_houses.py ~2866-2868 credit phrase "Doğa Özden’s packing from two copies of a band of the tilted squares of Ryan Xu’s n = 70 packing as Evan Daniel and PingYou Ltd improved it, below Nate Chaoweeraprasit’s SQUISH packing as Francisco Couzo and Mykhailo Polkovskyi refined it", then adopt_houses --refresh --n 237.
S2: append to T-253 next_rung (results.yaml ~36439): "At 237 T-295, adopted on 11 November 2026, lies 8.80e-03 below this certificate, so if the entry stays recorded it is adopted at the other eight counts only." Fix the stale note at ~36393.
N1: evidence.yaml ~60707, 60777, 60870 → "F6, F8, F9 and F11 for both, and F10 for the records". PR body → "F5, F7 and F12 are for the author; F6, F8, F9 and F11 for both".
Contiguity clears once T-292..T-294 are on main.
## Lane L129 (bold-ritchie-l129), 12 November 2026

Worktree on `claude/bold-ritchie-xo28us-l110` (402455e82), merged origin/main 942256917 (#955, #957, #961, #964, #965, #968) and applied the senior review; pushed 402455e82..5fb3bdce2 to #963 (draft).

**Merge 9dece3ec7.** Both sides kept in the hand-written records; generated views taken from main and derived again. Adoption moved to the pass of 12 November: LATER_PASSES["2026-11-12"] = {179, 237}; 237's prior-state row (byte-equal to main's n-237.md) added to house-adoption-prior-state-2026-11-12.json.xz with adopt_houses.retain_history; 11 November archive is main's. Layer index from main's + axis view at 237 + Evan Daniel's view layered from L110's original scratch run (retained copy lacks regularize.json; report/receipt byte-identical, view byte-identical to L110's). Gate totals n=1..324 2,683/6,574. Custody 74 houses, 248 inputs, 80 mutations refused. Synopsis 295 registered, 263 by others.

**Review 897318c3e.** B1 stamp_landed --apply: T-295 and landings n=237 on 2026-11-12. B2 palette pin (103, 237), re-measured after the merge (next: 85 at 267). S1 credit phrase + adopt_houses --refresh --n 237. S2 T-253 next_rung sentence (12 November) and its 237 report-order note. N1 evidence F6, F8, F9 and F11 for both, F10 for the records; PR body likewise. Also source_reviewed 2026-11-12 at 237 (refresh does not write it; writer test needs it).

**Re-pin 5fb3bdce2.** release_pin --update to 897318c3.

**Validation.** records tier 55/55 (twice); check_results 295 contiguous; check_requests; adopt_houses/select_houses/upper_bound_houses checks; apply_closed_form; check-state moves 1 house (237); flips, composite, citations, release impact, release_pin --check. pytest -n 2: brief's list 378 passed; 14 more touched modules 1,070 passed, 1 skipped (only failure the pin, fixed after); test_release 20 passed after re-pin. Ruff/format/BasedPyright clean; flowmark check clean. PR body updated (check_pr_description --label intake ok).
