---
type: is
id: is-01m5h5w4d59h67ckp28qgzbere
title: "Couzo's watched publications no issue claims: 5a299b4 (20 certificates below main) and 23aff0c (21 superseded the same day), plus the held re-certifications"
kind: task
status: in_progress
priority: 2
version: 5
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m4yr8jtj1znqhx7fva8g60bw
hold: null
hold_until: null
created_at: 2026-10-22T06:48:14.501Z
updated_at: 2026-10-22T13:13:37.450Z
started_at: 2026-10-22T06:48:16.556Z
---
Found by the #719 triage: 13 certificates in franciscouzo/square-packing 5a299b4 that no issue claims and no packet retains, each below main by 1.1e-12 to 6.2e-10; they are the nearest earlier report at those counts for #719's ledger. This is the sweep's open 'needs an owner' item for franciscouzo. Retain, replay and record them as a watched-repository publication dated by their first commit (before #719's rows at those counts).
blocked_on: none

## Notes

2026-10-22 c-lane-719-import (#719's import, think-xyhn): #719's ledger (packing/campaign/issue-intake/upper-bounds-issue719-20261022, starts frozen at main 0281e7763) walks Couzo's 5a299b4 commit as a publication dated by its push (2026-10-21T22:56:37Z, after #715's issue), from the #719 packet's receipts/earlier-publications.json (devtools.beyond_horizon_replay earlier). It records 5a299b4 at 13 counts: the 12 of this bead's list at which it is the report just before #719 (372, 409, 450, 453, 649, 810, 812, 933, 934, 990, 991, 997) and 366, where 5a299b4's certified_bounds.json states an L-border bound (from best/n294.cert) slightly below the 4e4c8ce certificate. At 743 5a299b4's certificate states the 4e4c8ce certificate's side exactly, a restatement, so 743 is think-yfoo's. At 366 and 372 5a299b4's side is 1.97e-23 and 1.98e-23 below 4e4c8ce's, the same 12-place print: a sub-print re-certification, think-fwa9's question again. Also yours by the same reading: franciscouzo/square-packing@23aff0c at 447, certificates/best/n447.cert and upper_bounds.json's verified bound 25/2 + 13/2*sqrt(2) rounded up (21.692388155426), Göbel's off-centre construction, below 487b058's row and below 4e4c8ce's 447; #670 does not claim 447. #719's beyond_horizon_replay.WALKS names this bead as Awaiting for both commits: when this import lands, map each to its source in the walk's declaration and repoint the start rows (487b058's or #686's at these counts) to the new rows, each superseded by #719's mishapolk-issue719-2026-10-22 row; chain_problems then holds the chain.

2026-10-22 c-triage-1022b (read-only re-plan against main 76496462b and #719's head
f9cee4736; coordinator scratchpad triage-1022b/: couzo-residue-plan.md, residue-rows.tsv,
residue-held.tsv).

**The list of 13 came from #719's counts only.** A walk of every count from 325 to 1024
finds:

- **`5a299b4`: 20 certificate rows** (root `certificates/nN.cert`, dated by the push at
  2026-10-21T22:56:37Z).
  - **9 current**, at 487, 532, 579, 628, 679, 732, 787, 844 and 903. They are not on the
    list. Each is 2.6e-11 below `4e4c8ce`'s certificate, with a different 12-place print,
    and 3e-11 to 2.1e-9 below `487b058`'s row.
  - **11 history**, superseded by #719, at 409, 450, 453, 649, 810, 812, 933, 934, 990,
    991 and 997.
  - At 372 `5a299b4` is a sub-print re-certification of `4e4c8ce` (held, below). 743 is
    `think-yfoo`'s. Both agree with #719's ledger.
- **`23aff0c` (#670's pin, 17 October 18:00:09Z): 21 certificates #670 did not claim.**
  All are history, superseded within hours by #672 (16) or #675 (5): 547, 554, 602, 652,
  653, 704, 705, 759, 814, 815, 816, 872, 873, 874, 932, 933, 934, 994, 995, 996 and 997.
- **447.** `23aff0c` states the deletion bound 21.692388155426 (held, below) beside a file
  at 21.692388155457, which is above that bound. If the owner rules that index bounds are
  not reports, the file becomes a history row under #719.

**Held:**

- 41 sub-prints for `think-fwa9`: `5a299b4`'s 31 (11 files and 20 index L-borders) and
  `23aff0c`'s 10. #715's 30 are separate, and #715 reported them first.
- 15 `23aff0c` index deletion bounds (D6, proposed on `think-f2io`).
- 46 `23aff0c` L-border and tiling recipes (D2, `think-f2io`).
- 331, above Göbel (`think-8krd`).

**Not new.** `d09edd7`'s paths hold nothing to import (its n183.cert is T-220's bytes,
SHA-256 279e70d1…). Above 1024, `5a299b4`'s index states 5,078 non-grid bounds, all D1.

**Packets.**

- New: `couzo-reconcile-2026-10-20` at `5a299b4`, retaining the 20 files (2.54 MB).
- `23aff0c`'s 21 files (6.37 MB) join `couzo-issue670-2026-10-17`, the same revision,
  with a claims record of their own.
- The filtered replay is about 11 CPU-min with controls (Σn = 31,620).

**The read.** Until the PR, a read through `6b7391d` with `bead: think-tmwt` owns the
sweep's franciscouzo item (draft in intake-watch-drafts.yaml). After the PR the read stays
without its bead (`think-bspk`). The one Couzo history records PR closes this bead.

blocked_on: think-xyhn
