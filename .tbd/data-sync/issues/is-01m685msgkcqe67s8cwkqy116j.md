---
type: is
id: is-01m685msgkcqe67s8cwkqy116j
title: "Import Francisco Couzo: s(130) <= 11.902430645985 (#843)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l2
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m687befj0g6hrrfg6jxz126x
hold: null
hold_until: null
created_at: 2026-10-31T05:06:45.907Z
updated_at: 2026-10-31T05:49:47.841Z
started_at: 2026-10-31T05:07:20.327Z
---
Issue jlevy/squares#843 (franciscouzo, 2026-10-27T19:49:57Z): certificates/n130.cert at franciscouzo/square-packing 3a4d95c (committed 2026-10-27T19:42:09Z, 7 min before the issue), SHA-256 a2618e1a...7fcd, exact side 466915711841738962256077475351530705109199164124122993/39228601764570445403995003040207131754000000000000000 = 11.9024306459843486..., 2.05e-3 below the house (PingYou Ltd's PR #574 certificate of Chaoweeraprasit's packing, improved by Gupta). The issue calls it a new packing found from #574's (largest matched move 0.704, 11 squares > 0.1) by the web app's fq, basin hopping and native SLP on the author's computers. Stage 1-3 and the stage 4 replay in the 2026-10-31 intake pass, lane L2 (think-3guf); review and adoption follow. Kaggle side-only 11.902430646006 (Cats and boxes) is no report.

## Notes

2026-10-31 bold-ritchie-l2: stages 1-3 and the stage 4 replay on branch claude/bold-ritchie-xo28us-upper: packet couzo-issue843-2026-10-28 at 712c6a6 (n130.cert first committed at 3a4d95c), both digests the issue prints match, both maintained exact routes accept it and refuse the gross and sharp controls, identity vs T-174 (no symmetry one to one; 11 squares beyond 0.1), ledger upper-bounds-843-846-20261031 records it (new packing), registered T-253 at V0/C0 (id may be renumbered at merge). Review and adoption: think-oy8d; at 130 the house rule adopts Polkovskyi's #846 refinement of this packing (2.08e-12 lower) if both reviews accept. DRAFT import reply for #843, to render from main with check_requests --draft 843 after the merge: thanks; received certificates/n130.cert at 3a4d95c, retained at 712c6a6 with n130.json and n130.txt (digests match); its exact side rounds up to 11.902430645985, 2.05e-3 below T-174; both maintained exact routes accept it, with gross and sharp controls refused as expected; registered as T-253 (reported, V0/C0), credited to Couzo after the PR #574 packing's credits; the ledger also records Polkovskyi's #846 certificate at 130, a 2e-14 dilation of this packing 2.08e-12 below it, as a refinement credited to this packing; the stage 4 review and the adoption at 130 with both regularizations are queued (think-oy8d).
