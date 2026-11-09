---
type: is
id: is-01m6zhjxnkb2vbrmszz3r3w6mg
title: "Stage 4 blind review of #927-#931 (Özden's five upper bounds)"
kind: task
status: in_progress
priority: 1
version: 9
delegate: bold-ritchie-l64-review
labels:
  - intake
  - review
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T06:57:59.474Z
updated_at: 2026-11-09T08:07:38.132Z
started_at: 2026-11-09T06:58:03.800Z
---
Blind stage-4 mathematical review with a clean-room exact checker, frozen findings and SHA-256 before reading the import lane's work; precedent review-2026-11-04-ozden-893-894-299-204.md and review-2026-11-05-evand-914-seven.md.

## Notes

L64 (bold-ritchie-l64-review), stage 4 blind review of #927-#931.

- 07:05Z: read both precedents (11-04 ozden, 11-05 evand-914), issues #927-#931, the
  Witness/v2 schema, epistemics (significance, review records) and result-import stage 4.
  Record on main 19b354a5c: T-256 (232, 307), T-270 (268), T-263 (299), T-272 (303).
- Cloned the five repositories into scratch (one commit each, pins match the issues).
  Same sqcheck.py blob aa4b27ca and LICENSE.md blob 9803370f in all five.
  Not read: sqcheck.py, verifier/README.md, any sqpack witness or verifier code.
- Certificates are Witness/v2 `representation: corners`, rational p/q strings with
  ~10^215 denominators, promoted by this repository's `packing-witness promote
  --strategy robust-rational`. Writing the clean-room checker now.
- 07:18:14Z: clean-room checker FROZEN before any producer code was read. Six files
  (l64_util, l64_reader, l64_sat, l64_clip, l64_check, l64_selftest); the frozen-digests
  file has SHA-256 59c3d0065049c552c24226a6f2e1564638fcd6dd312960ff463b2aa01ab3acd3.
  l64_check.py 5c4927b8..., l64_sat.py b4e61fcb..., l64_clip.py d238d556...,
  l64_reader.py 0e51d443... Self-test PASSED. Timing run: 232 ACCEPT, 26,796 pairs all
  apart, least margin 2.0358e-13, 22 CPU-s.
- 07:20Z: final checker runs, all five ACCEPT by both methods, every pair strictly apart:
  232 least margin 2.0358e-13, 268 2.0122e-13, 299 2.0262e-13, 303 2.0128e-13,
  307 2.0174e-13; three wall contacts per file (left, bottom, and top or right).
- Sides: each claim is the 12-place ceiling; gaps match the issues' 4-digit prints.
- 07:24:31Z: controls plan stated before any control ran: controls-plan.json, SHA-256
  d5e090ad8d436e22bdb982f2313f99e129b6235c692ce547a46b6301a2633927 (19 controls/file).
- 07:58Z: all controls decided. First plan: every verdict as stated at all five; details
  missed only at S1b (232) and S5 (all five, construction). Addendum: S4', S5' (2,641
  near pairs closed along centre lines) and the S5 diagnosis as stated at all five
  (axis lines miss 28/91/123/5/238 pairs). Houses ACCEPT by the frozen checker; gaps
  exceed every house's scale slack by >= 5.7e8. Lineage: all five one to one with the
  house under the identity by assignment (299: nearest one short, bottom row slides
  0.642); issues' counts match the house; their "tilted" is beyond 0.5 deg.
- 08:07:30Z: FINDINGS FROZEN before reading anything of L63 (branch, PR, notes, packets),
  sqcheck.py or this repository's sqpack verifier/promote code. Frozen document
  review-2026-11-09-ozden-927-931-five.frozen.md, 712 lines, 47,124 bytes, SHA-256
  222929e07ce91629f049581485823ace65c719773f036d21ccb367b975551a2b.
  Verdicts: accept at all five; F1-F12 all notes; significance S3 at all five.
