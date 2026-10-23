---
type: is
id: is-01m4rg52wxyzg43rkd2hcg89rf
title: "Independent checks of #557's computations"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T16:46:52.829Z
updated_at: 2026-10-23T06:12:31.069Z
started_at: 2026-10-12T16:46:57.081Z
closed_at: 2026-10-23T06:12:31.069Z
close_reason: "Tracker audit 2026-10-23 (c-audit-b-1023, think-ioqe), checked by coord-intake-1023: STALE-CLAIM + DONE. K3 receipts 3a6d0468b are on main via #577 (5584b2283, 2026-10-13). Evidence E-n017-overbeck-*-sample/-independent are on main (check_requests #557 rows). The complete replays belong to think-fgmr and think-0at1."
resolution: null
duplicate_of: null
---
Lane K3 on https://github.com/jlevy/squares/issues/557 (Kleddamag, candidate proof s(17) = L, pin 653b9589d). Independent exact checks: upper-bound packing via sqpack exact routes and independent root isolation; sampled recompute of capture slices; tree certificates through both exact checkers; rigidity stage price. Receipts only (no upstream bytes): packing/resources/web/kleddamag-n17-candidate-2026-10-12/receipts-here/.

## Notes

Issue: https://github.com/jlevy/squares/issues/557. K3 done on branch k17-checks, commit 3a6d0468b (not pushed): receipts under packing/resources/web/kleddamag-n17-candidate-2026-10-12/receipts-here/ (copies in scratch k17/receipts/). Upper bound: rational packing at R valid by sqpack + independent checker; K3 Krawczyk proves unique root, L in 20-place interval, L root of n-017 deg-18 polynomial; statement F,G,box = exp-237. Capture: 28 recompute_slice calls (34 rows, 20 statements, all 11 roots) EQUAL; K3 independent row checker 34 rows / 6 statements, all per-level minima equal stored Python+Node; full recompute 2,347 CPU-h. Trees: JQ, JPG17m_v5, JPG15p_v5 ACCEPTED, reports equal stored; 13-tree replay 7.4 CPU-h build machine, ~22 h here. Rigidity checks PASS in K1's check.py (~60 s). Leave open until the branch is merged.
