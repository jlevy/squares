---
type: is
id: is-01m7fh3qx5tv2n6v88me8sk1fz
title: "Import #996/#997: Joost de Winter's s(90) <= 9.994038766610 (fa53fb0, replacing #996's 64d5ee7 certificate; T-303's arrangement improved); adopt in a 2026-11-16 pass"
kind: task
status: in_progress
priority: 1
version: 8
delegate: bold-ritchie-l181
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-15T11:57:32.962Z
updated_at: 2026-11-15T13:52:31.564Z
started_at: 2026-11-15T11:57:34.424Z
---

## Notes

L181 (bold-ritchie-l181), 2026-11-15: controls plan stated before any run of the certificate, in scratch l181-notes: controls-plan-n90.md SHA-256 b441e936eee35ef5aa377e478265c0344ffb22969397ddd8406582ce706c7ea3, hashed 12:03:58Z; 3 gross and 11 sharp controls, with the one branch (a square touching its wall exactly) stated in advance. Source: JoostdeWinter/square-packing; the issue names 64d5ee762a1159248d375973fb33825d51da637d (11:27:26Z); head 9cafa33d43f60423e51058f51dbdf042077c7cc2 (clone 12:01Z) adds n90/REGISTRATION.md and n90/SHA256SUMS (0c9bcd2) and renames the local-search model from 'OpenAI Codex (GPT-6 Astra)' to 'GPT-6.1 Sol Max' (9cafa33); n90_exact.json (blob 620a72b7) and n90_witness.yaml (blob 52ccc234) are the same blobs at both.

Intake commit 35e33e184 (12:17:43Z): packet de-winter-s90-upper-bound-2026-11-15 pinned at 64d5ee7; replay on both routes (24,030 pair decisions), 3 gross and 11 sharp controls all as stated (the touching-square branch taken: square 10 grown by 0); left/bottom wall contacts exact, far wall 5.07e-21, least pair gap 1.0641e-12 (2, 40); T-303 contraction margin 1.0988e-11 (79, 81), own 9.533e-12 (2, 40); identity vs T-303: not 1:1 by nearest centres, identity assignment 6 beyond 0.1 (largest 0.646), all 40 tilted paired same sign -> T-303's arrangement improved; twin = JSON (witness-corners now accepts the schema URL and square-k ids); L step carries nowhere; ledger upper-bounds-996-20261115. Registered T-304 (V3/C3 on the replay, S3 draft) in b1e8f98ab (12:38:45Z). Nothing of L180 read before these commits.

Read L180's frozen findings (4622bdfb8) at 12:39Z; merged (249a0dd08), mapped (d1e0283f7): accepted, 26/26 controls, F1-F7 notes, no disagreement. Read final head (95ad4bc8a) at 12:43Z; merged (8f15a2305), mapped (8cd27803b): F8-F13 notes, S3, six questions for the author; agrees with packet measurements. Adoption (pass of 2026-11-16, LATER_PASSES {90}), regularization, stamps and re-pin wait for 16 November UTC.

Change of input (coordinator, 12:55Z): de Winter's #997 (12:08:33Z) replaces #996's certificate with fa53fb0d734fbf438bcfb73c1434a15894bb2bc5 (side 99940387666098521323/10000000000000000000 = 9.994038766610 at 12 places, 9e-8 below), asking to pin it and disregard 64d5ee7. Head 6c0ad56 (12:07:15Z) changes only n90/REGISTRATION.md (the commit named) and n90/SHA256SUMS (the new digests). New controls plan stated before any run of the fa53fb0 certificate: scratch l181-notes/controls-plan-n90-fa53fb0.md SHA-256 88b26ff1b8fb96a7ee5bf9909193b237f85fc0808cc494bb0ec0e36364ef8cf2, hashed 12:56:59Z; 3 gross and 11 sharp controls, the touching-square branch stated in advance.

fa53fb0 intake 48bf8278b (13:08:49Z): packet de-winter-s90-upper-bound-2026-11-15 now pins fa53fb0 (head 6c0ad56 differs only in REGISTRATION.md, SHA256SUMS); 64d5ee7 moved to retention-only packet de-winter-s90-64d5ee7-2026-11-15 (superseded by author). Replay: 24,030 pair decisions, 3 gross + 11 sharp all as stated (plan 88b26ff1, 12:56:59Z); edge contacts at left/bottom, far wall 2.51e-22, least gap 2.0264e-12 (2,40). Identity: vs T-303 6 beyond 0.1 (0.645), all 40 tilted same sign -> T-303 improved (found_by jazivxt, improved_by de Winter at adoption); vs #996 one-to-one, largest 0.0142. Margins: T-303 1.0988e-11 (gain 3.86e8x), #996 9.533e-12 (step 9539x), own 1.8187e-11. New reader witness-corners-opposite holds the twin as same packing. Ledger renamed upper-bounds-996-997-20261115 (#997 recorded, #996 other item: replaced by author). Records 20c8c89e4 (13:21:03Z): T-304 = fa53fb0, evidence E-de-winter-997-*, #996 entry not_registered, #997 entry T-304. Addendum (L182, 83ac8ceec) read 13:21Z after those commits; merged 86ce0aa8d; mapped 09a290837: accepted, 26/26, F14 F15, S3; no disagreement. Re-pin 2f0da862a. Adoption, regularization, stamps on 16 Nov.

Pushed claude/bold-ritchie-xo28us-l181 at 2f0da862a; draft PR https://github.com/jlevy/squares/pull/998 (13:32Z). Hosted run 43719521961: every job passed but suite-c, whose 19 failures are all test_house_adoption, from the pending adoption at 90 (T-304 is the smallest validated side and 90 cannot move again on 15 November); they resolve with the adoption in the pass of 16 November. Certificate page 43719522039 success, mergeability 43719460473 success. Waiting for 00:00Z on 16 November to adopt, regularize, stamp and re-pin.
