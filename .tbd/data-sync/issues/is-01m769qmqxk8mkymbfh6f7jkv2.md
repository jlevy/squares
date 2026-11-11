---
type: is
id: is-01m769qmqxk8mkymbfh6f7jkv2
title: "Import #960: Doğa Özden's s(237) <= 15.893805580573 (kenaznia-doga/s237-upper-bound @ 13c4b231), 8.798e-3 below T-190 (the issue names T-189)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l110
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T21:55:26.589Z
updated_at: 2026-11-11T23:44:16.995Z
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
