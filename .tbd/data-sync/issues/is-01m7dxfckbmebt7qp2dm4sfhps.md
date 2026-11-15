---
type: is
id: is-01m7dxfckbmebt7qp2dm4sfhps
title: "Import #984 (s(228) <= 15.596043120921, supersedes T-300) and #985 (s(147) <= 12.651043556588, below 7 + 4*sqrt(2)): Roberto Ono, first contribution"
kind: task
status: in_progress
priority: 1
version: 8
delegate: bold-ritchie-l164
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-14T20:55:08.650Z
updated_at: 2026-11-15T01:13:27.106Z
started_at: 2026-11-14T21:06:10.385Z
---

## Notes

L164 (bold-ritchie-l164), 2026-11-14: controls plans stated before any run, in scratch l164-notes: controls-plan-n228.md SHA-256 4eb6cc4e828c525e40994e5fd1e2e4dcca09ff55e7867119ecfe265737c121e3 and controls-plan-n147.md SHA-256 a2ed80d123eab30d33f701c2636dfa77220924242f4ffd9a6ebce8c8d5f89212, both hashed 21:12:34Z; 3 gross and 11 sharp controls per count. Source pinned: RobertoOno/squares-in-square fce076f2bf459a25be3645d899e8950b93ed977c (the revision both issues name; head b5636fd adds only FOLLOWUP.md and the posted issue texts).

Packets ono-issue984-2026-11-14 and ono-issue985-2026-11-14 pin main b5636fd6694d2cc7aa5811ae33f441268b81b714 (fce076f's descendant; certificates identical). Recorded #983's final reply in its own commit ef0f8bb1b (coordinator's request). Intake commit 3f0976140 (21:29:42Z): replay on both routes, 3 gross and 11 sharp controls per count, all as stated in the plans above; contraction margins (T-300 2.949e-12, gain 1.61e9 times it; T-174 0; T-155 view at 147 0; own 3.49e-9 and 2.93e-9), identity, L-step scans, ledger upper-bounds-984-985-20261114. Registered T-301 (228) and T-302 (147) in fcce6be56 (21:44:47Z). Read L163's frozen review (8504d8e04, frozen 21:17:04Z) at 21:45:20Z, after both commits: both accepted, 40 of 40 controls, F1-F8 notes (F5: three walls, not four). Adoption waits for 2026-11-15 UTC (228 already moved on 14 November).

Read L163's final head (6d1e3383e, 21:54Z) at 21:56Z; merged it (71ee1243e) and mapped it (385617986): V-ono-984-985-review-check, E-ono-984/985-review-exact-feasibility, external_review on the reports and replays, T-301/T-302 adversarial accepted reviews; S3 each, 14 notes F1-F14; no disagreement with the replay, controls, margins or identity. T-301/T-302 read pending adoption at V3/C3. Adoption prepared in the working tree for the pass of 2026-11-15 ({147, 228}), not run before 00:00Z.

Adopted T-301 at 228 and T-302 at 147 in the pass of 2026-11-15 (adopt_houses at 00:01Z), commit 7006d0924; runs in packing/cases/regularized_drawings/think-17ex-2026-11-15 (147 grid-slack 0.5-degree view drawn; 228 decided no better, axis view kept); KKT solves held at row 3 for RV-3 (147 certified 3.415e-9 below, 228 local minimum 4.289e-9 below, certificate invalid; both equal Nevska's leaderboard sides at 24 places). Stamped landed 2026-11-15 (9860e55f7), re-pinned (b75bd8205). Draft PR jlevy/squares#988. Merge must be on 2026-11-15 UTC. Replies owed on #984 and #985, and #983's promised follow-up, after merge.

CI on b75bd8205 (runs 43660226126, 43660226180): suite-b (PR 574 frozen algebraic claim record, 147 row) and suite-d (SCREEN_FINDINGS n=1..200) fixed in 6687cec27 (pushed 01:12Z 2026-11-15); stamp_landed --apply and release_pin --update re-run at 01:11Z: no change (pin already last data commit 9860e55f7). overview/pages-required fail on result/t-180.html 501,700 bytes vs 500,000 budget (499,424 on #986 head 4544c4c96): HELD for owner (think-v4me), ceiling not raised.
