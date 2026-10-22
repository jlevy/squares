---
type: is
id: is-01m5h5w4d59h67ckp28qgzbere
title: Couzo's 13 unclaimed 5a299b4 certificates below main (372, 409, 450, 453, 649, 743, 810, 812, 933, 934, 990, 991, 997)
kind: task
status: in_progress
priority: 2
version: 3
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m4yr8jtj1znqhx7fva8g60bw
hold: null
hold_until: null
created_at: 2026-10-22T06:48:14.501Z
updated_at: 2026-10-22T09:58:59.261Z
started_at: 2026-10-22T06:48:16.556Z
---
Found by the #719 triage: 13 certificates in franciscouzo/square-packing 5a299b4 that no issue claims and no packet retains, each below main by 1.1e-12 to 6.2e-10; they are the nearest earlier report at those counts for #719's ledger. This is the sweep's open 'needs an owner' item for franciscouzo. Retain, replay and record them as a watched-repository publication dated by their first commit (before #719's rows at those counts).
blocked_on: none

## Notes

2026-10-22 c-lane-719-import (#719's import, think-xyhn): #719's ledger (packing/campaign/issue-intake/upper-bounds-issue719-20261022, starts frozen at main 0281e7763) walks Couzo's 5a299b4 commit as a publication dated by its push (2026-10-21T22:56:37Z, after #715's issue), from the #719 packet's receipts/earlier-publications.json (devtools.beyond_horizon_replay earlier). It records 5a299b4 at 13 counts: the 12 of this bead's list at which it is the report just before #719 (372, 409, 450, 453, 649, 810, 812, 933, 934, 990, 991, 997) and 366, where 5a299b4's certified_bounds.json states an L-border bound (from best/n294.cert) slightly below the 4e4c8ce certificate. At 743 5a299b4's certificate states the 4e4c8ce certificate's side exactly, a restatement, so 743 is think-yfoo's. At 366 and 372 5a299b4's side is 1.97e-23 and 1.98e-23 below 4e4c8ce's, the same 12-place print: a sub-print re-certification, think-fwa9's question again. Also yours by the same reading: franciscouzo/square-packing@23aff0c at 447, certificates/best/n447.cert and upper_bounds.json's verified bound 25/2 + 13/2*sqrt(2) rounded up (21.692388155426), Göbel's off-centre construction, below 487b058's row and below 4e4c8ce's 447; #670 does not claim 447. #719's beyond_horizon_replay.WALKS names this bead as Awaiting for both commits: when this import lands, map each to its source in the walk's declaration and repoint the start rows (487b058's or #686's at these counts) to the new rows, each superseded by #719's mishapolk-issue719-2026-10-22 row; chain_problems then holds the chain.
