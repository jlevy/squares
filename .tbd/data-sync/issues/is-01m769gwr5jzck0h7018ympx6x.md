---
type: is
id: is-01m769gwr5jzck0h7018ympx6x
title: "Import #959: Doğa Özden's s(179) <= 13.880960371559 (supersedes his #954/T-291 by 4.07e-4; 2.2e-12 above Nevska's unpublished Kaggle side)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l107
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T21:51:45.413Z
updated_at: 2026-11-12T00:32:58.044Z
started_at: 2026-11-11T22:20:33.166Z
---

## Notes

## Lane L107 (bold-ritchie-l107), 11 November 2026

Branch `claude/bold-ritchie-xo28us-l107`, cut from `origin/main` `b5b12c206` (#956's merge).

**Stage 2, retained.** `ozden-s179-issue959-2026-11-11`, pinned at kenaznia-doga/s179-upper-bound-13880960371 6ab3cfe (21:18:12Z, 12 s before the issue); both stated digests hold (candidate 77ee3dd2...e1fc, JSON 4b2509fe...ae1a); acquire_source --check PACKET_MATCHES_ITS_CONTRACT. Pinned-only: the diff PNG by digest; verifier/README.md, sqcheck.py, Evan Daniel's MIT notice identical_to the s299, s232 and evand-issue845 copies. CC BY 4.0 data / MIT code. Key [Özden s179 issue 959 2026-11-11].

**Stage 4 replay.** Controls plan before any run (scratch l107/notes/controls-plan.md, SHA-256 28ab9fb2...935b, 22:23:56Z). certify 3 jobs, 95,586 pair decisions, 39.82 route CPU-s; check --replay passed; sharp-controls 11, all as expected (square 67 already at its wall). Walls touched exactly; least pair gap 1.99e-13 (squares 104, 105).

**Measurements.** Gain 4.068e-4 below T-291, 2.835e-3 below T-174 (exact). T-291 contraction margin 2.616e-12 (pair 14-15), gain/margin 1.56e8: RV-3 does not reach it. Own margin 2.566e-12 (1 - lambda* 1.992e-13, pair 104-105); contracted side s(70)+5+7.9e-14. Identity: one to one with T-291 by nearest centres under the identity, 3 beyond 0.1 (largest 0.218), 5 turned > 1 degree centred: a further arrangement of T-291; vs T-174 not one to one, 46 beyond 0.1. L-step scan: carries nowhere.

**s(70)+5.** New tool devtools.measure_core (tests/test_measure_core.py). Side - s(70) - 5 = 2.645427e-12 (1.906e-13 relative). Not a core with a border: five L steps round the 70 hold 175 at s(70)+5; best corner placement keeps 48 of 70 within 1e-9 (upper right, identity), 34 lower left. Band: 70 laid at diagonal shifts 0..5 under identity lies within 1e-9 of 15 of the 35 tilted squares (7 at (0,0), 8 at (5,5)), 29 within 0.05; no other symmetry within 0.01. Credit: a band re-laid from the 70's (as T-291's), not 70 + border; Özden finder, Xu/Daniel/PingYou as the seed's source.

**Ledger** upper-bounds-959-20261111: recorded at 179 (start T-291 at b5b12c206). Nevska's side-only 13.880960371556 (= s(70)+5 at 12 places, 2.2e-12 below): context only.

**Stage 3.** T-294 (T-292/T-293 are PR #961's, merged first; this branch merged main 75cce00b6). Requests entry for 959 (answer bead think-89i7); main's closed 954 entry gains a note of the adoption.

**Review mapped (L108, 440acdb99, merged).** Accepted, 13 findings all notes, S3. V-ozden-959-review-check registered clean-room; E-ozden-959-review-exact-feasibility; T-294's adversarial accepted review; external_review on report and replay; review in the document map; deferral removed. F5-F13 folded in; F10's contracted side (13.88096037155566185) noted, NOT registered (RV-3, think-ruu2); F11's think-mdxq -> think-71uq. Eight questions in packet README, entry and requests notes.

**Adopted** 179 from T-291 to T-294 as the pass of 12 November (LATER_PASSES "2026-11-12"; the 11 November pass had already moved 179 and a day's archive holds one prior state a count, as at 260 and 268); adopt_houses Prose and Credit, ADOPTED, packet_source (T-291 no source now); landing stamped 2026-11-12. Regularization in packing/cases/regularized_drawings/think-89i7-2026-11-12/: Evan Daniel's same-side view admitted (6,11,5,17,17 -> 0,0,0,4,4; 497/530 -> 552/552); his KKT solve 2.645e-12 below the side, at s(70)+5+1.4e-19, held at row 3 (RV-3) and NOT registered. Rigidity 64 translate (74 before); gate totals 724/2,315 and 2,481/6,389 after merging main. Custody 74 houses. Refused: a pkill of my own stopped edit-tier processes (classifier); not retried.
