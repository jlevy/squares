---
type: is
id: is-01m7ejw4j4y7qmjc6kh8w8djy2
title: "Import #989: jazivxt's s(90) <= 9.998277166926 (below the 10 x 10 side; crop of de Winter's 157 with shifted copies)"
kind: task
status: closed
priority: 1
version: 8
delegate: bold-ritchie-l170
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-15T03:09:06.500Z
updated_at: 2026-11-15T09:31:31.135Z
started_at: 2026-11-15T03:09:08.001Z
closed_at: 2026-11-15T09:31:31.133Z
close_reason: "#989 imported as T-303 (#991, 588ccb226), answered and closed; reply recorded in #993 (942c1271f)."
resolution: null
duplicate_of: null
---

## Notes

L170 (bold-ritchie-l170), 2026-11-15: controls plan stated before any run, in scratch l170-notes: controls-plan-n90.md SHA-256 d23ca310bd13f3881abc69d0d946e14aa31fb982c68b04b56e28124fd06fd2f6, hashed 03:16:30Z; 3 gross and 11 sharp controls. Source: dpre4ai/n90-square-packing; the issue names 179fcba7f0e91e2c3d3e92525e0738b6da0f8dd5; head f9b31b4ebddb278a128b6cb5c43836a305a24dca (ls-remote 03:15Z) adds only n90-construction.png; n90.cert the same blob 9a070723 at both, SHA-256 88c93b2f...d466 as the issue states.

Intake commit 77dfd138a (03:25:49Z): packet jazivxt-s90-upper-bound-2026-11-15 pinned at f9b31b4; replay on both routes (24,030 pair decisions), 3 gross and 11 sharp controls all as stated; least wall clearance 2.1000000001021e-15 (square 28), least pair gap 1.19448e-12 (79, 81); grid contraction margin 0, own 1.099e-11; identity: not one to one with the grid, 52 beyond 0.1, 44 tilted 22.6-31.6 deg one way; L step: grid's 90->111 extension lapses, carries nowhere; ledger upper-bounds-989-20261115. Registered T-303 (V3/C3 on the replay, S3 draft) in 59489132c (03:32:32Z). Nothing of L169 read before these commits.

Read L169's frozen findings (d20230eb6, frozen 03:28:11Z) at 03:33Z, after both commits above; merged (083c57b38), mapped (3d88e55b9, 03:40Z): accepted, 23/23 controls, F1-F7 notes; no disagreement with replay, controls, margins or identity. Adoption written at 03:42Z (pass of 2026-11-15, LATER_PASSES {90,147,228}). Read L169's final head (22949a12e, 03:57Z) at 03:58Z; merged (3e5c54168): 14 findings, all notes, S3; lineage reproduces (F11); c70defa n157 file = retained blob 079d4cb1 (measured here). Adoption, regularization (evand same-side view admitted row 10; KKT 1.108e-11 below, ~1.01x own margin, held row 3) and derived records committed ddc209f9d (04:18Z); merged origin/main a3e4ea0c5 (#990) in 3bf7dc347; branch pushed.

Records tier on 6bf1356d7: 55/55 after fixing the synopsis row, RESULTS/VERIFIERS views and the chunk census/profile/taxonomy (90 is the first count of n=1..100 off the grid; profile constants 36/64 -> 37/63; BC-024 taxonomy gains 90's tilted interior component). Stamp ac00f8485 (T-303 and house at 90 landed 2026-11-15, 04:35Z); re-pin 6316c38e5 (DATA_REVISION ac00f848). Draft PR https://github.com/jlevy/squares/pull/991 head 6316c38e5; merge must be on 2026-11-15 UTC or stamp/re-pin rerun. Reply on #989 owed after merge (think-i8y9), with the review's six questions.

Hosted on 6316c38e5: four pins failed (gate text 36->37 chunk cases; grid first counts 90->91 in test_known_best_grid_transitions and test_overview; test_catalogue_precision 151->152; workbench check_animation_editor 155->154 grid fills); fixed in 6fb38e8dd (no data; stamp_landed --apply unchanged, release_pin --check: pin still ac00f8485). Hosted on 6fb38e8dd: 31 passed, 28 skipped, 0 failed; mergeable clean (runs 43679018452, 43679018425, 43679015526). PR #991 draft, not merged. Owed after merge: reply on #989 with the review's six questions.
