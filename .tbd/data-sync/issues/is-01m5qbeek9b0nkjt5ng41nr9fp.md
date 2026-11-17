---
type: is
id: is-01m5qbeek9b0nkjt5ng41nr9fp
title: "PR #795 (merge): senior review of the 99 Kaggle-credited sides at 964ee2b (87 rows, 12 recipes held)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-795-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T16:21:04.233Z
updated_at: 2026-10-24T16:58:17.362Z
started_at: 2026-10-24T16:21:11.518Z
closed_at: 2026-10-24T16:58:17.362Z
close_reason: "Review A posted https://github.com/jlevy/squares/pull/795#issuecomment-6386978876: changes requested (A1 High: walk the whole push per commit; A2 High: the 12 recipes have certificates; A3 Low); coordinator decided A1 by precedent; addressed by c-import-lyf9-1024; correctness review to follow."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-795-1024 (senior reviewer, claude-opus-5-5 at xhigh; coordinator coord-intake-1024). Review A (kind=senior, round 1) of #795 published as a PR comment at head cbf4998f2, base 2ec489d1e: https://github.com/jlevy/squares/pull/795#issuecomment-6386978876
Verdict: request changes. A1 High (the walk reads only 964ee2b's index; efef7d1 and fa6237e, in the same 23:38:42Z push, state 86 more sides below main's start at 60 of the 99 counts, 72 Couzo's and 14 Tymchishin's or Lavrentev's; at 364, 378, 405 and 450 the row is 1.35e-9 to 3.11e-8 below another notebook's fa6237e certificate, which 964ee2b's manifest names as previous_source: refinement and credit candidates). A2 High (each of the 12 held recipes has an n-square certificate in 964ee2b's certificates/parents/ at exactly its side, from its own commit, plus a dilated best/nN.cert; parents 445 and 859 and best/n445 decide on couzo_678_replay.decide; holding them for D2 and think-ww95's premise are unnecessary). A3 Low (169/70 should be 149/50). No Blocker; the 87 rows, 77 supersessions, margins, Göbel, first commits, credit, licence and the handle profiles verified.
Outside the diff: #763's held recipes (think-g2qy) also have best/ files new in the push at 444 487 632 683 733 734 737 788 789 845 909 910 966 970; at 632 it is Lavrentev's fa6237e certificate (2.08e-2 below main's row). Recommended: a correctness review of the walk path after A1/A2.
Scratch: /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/rev-795/ (verify_795.py, verify.json, push-intermediate.json, recipe_files.py, orphan_headers.py, decide_files.py, count169.py, review-A.md). About 0.29 CPU-h. Not synced.
