---
type: is
id: is-01m5ph9rqe5bpdf29txxgz7bce
title: "Hold #763's 13 L-border recipes at 325-1024 (365 444 487 632 733 734 737 788 789 845 910 966 970) until the D2 maintained construction checker"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-import-gn29-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T08:44:07.790Z
updated_at: 2026-10-25T01:10:42.217Z
started_at: 2026-10-24T20:35:19.037Z
---
The #763 import (think-ptkk, PR A) walks Couzo's 964ee2b claims to 1024 in report order (campaign/issue-intake/upper-bounds-issue763-20261024). Thirteen of the claims the walk records are tiling and L-border recipes certified_bounds.json states with no certificate file at their own count: 365 444 487 632 733 734 737 788 789 845 910 966 970 (909, the fourteenth, restates PR C's row and is not recorded). beyond_horizon_replay still holds the recipe class (RECIPE), so the walk holds them from rows (Walk upper-bounds-issue763-20261024, Held RECIPE) until a maintained construction checker decides a recipe exactly (D2, think-f2io; the W7 slice). Then: decide each recipe from its retained source certificate (the packet couzo-issue763-2026-10-23 retains every source certificate), write their rows, and drop the hold. Done when the 13 have rows or a recorded disposition.

blocked_on: think-f2io

## Notes

2026-10-24 coord-intake-1024, from #795 review A (https://github.com/jlevy/squares/pull/795#issuecomment-6386978876, 'outside this PR'): #763's held recipes also have best/ certificate files new in the 23:38:42Z push at 14 counts; at 632 the file is Lavrentev's fa6237e certificate, which couzo_678_replay.decide accepts, 2.08e-2 below main's row. Revisit: those counts may be certificate rows now, not recipes waiting on the D2 checker. Scratch: rev-795/recipe_files.py, decide_files.py.

2026-10-25 c-import-gn29-1024 (in think-gn29's PR https://github.com/jlevy/squares/pull/800): DONE on the branch. devtools.construction_checker decides all 13 of #763's recipes (365 444 487 632 733 734 737 788 789 845 910 966 970) exactly from recipe + replayed parent, 117 controls refused (couzo-issue763 packet receipts/recipe-decisions.json); parents 328 and 850 (restate f1ceee4, not rows) replayed on both routes with 6 controls each. Dated by the first index stating each (recipe_first_commits): efef7d1 at 365/970, 964ee2b at the rest. Frozen #763 walk: only WALKS holds changed (_HELD_763 keeps 683); ledger.json unchanged; sources.yaml/ledger.yaml/README re-rendered for the hold sentence; release declares 197 rows. 13 rows of couzo-issue763-2026-10-23 in the register; at 444 487 632 733 737 788 845 43f666c's recipe supersedes them. Review A's push files at these counts: walked commit by commit in the 43f666c walk after the issue; each above or equal to #763's recipe (or restating f1ceee4), none recorded; at 683 they rest on the held deletion. Note: each recipe also has a full n-square expansion in certificates/parents/ at exactly its side (as #795 A2 found for the notebook recipes); decided by the checker per the brief, flagged for the coordinator. Can close when PR #800 merges.
