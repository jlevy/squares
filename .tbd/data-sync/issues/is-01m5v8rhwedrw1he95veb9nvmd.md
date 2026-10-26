---
type: is
id: is-01m5v8rhwedrw1he95veb9nvmd
title: "Intake close rule P1/P2, #540/#541, blocked-label taxonomy, record #544/#684 closes"
kind: task
status: in_progress
priority: 2
version: 3
delegate: w-close-rule-1026
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-26T04:51:07.278Z
updated_at: 2026-10-26T06:03:26.324Z
started_at: 2026-10-26T04:51:19.110Z
---
Owner direction 26 Oct: close issues once answered (P1), asks belong to the author (P2), blocked:* label taxonomy, #540 and #541 replies_due/--github fixes, record #544 and #684 closes. Do not implement P3. Branch claude/friendly-einstein-gf9z0h-close-rule.

## Notes

2026-10-26 w-close-rule-1026 (branch claude/friendly-einstein-gf9z0h-close-rule, draft PR https://github.com/jlevy/squares/pull/828, labels intake and S2; commits 0e25a5998 and f547d716e):
- P1: check_requests.closeable closes an issue once answered; a result below V3/C3 is disposed of by `validation` beads; review tracks (#772 to #786, review_track: true) still wait for V3/C3; --draft names the owning beads and says the close confirms nothing still open; --report needs ids on main; check_bead_tree holds validation beads open on closed issues too. close_when recorded as descriptive (the rule governs).
- P2: asks are the author's; 10 asks moved (#428 1, #446 4, #413 2, #565 1, #719 2 to awaiting_author); every queued ask on an open issue names its source (36); the gate refuses a queued ask under a validation bead.
- #540 (positions and comments read after the last reply) and #541 (reply ids in the posted text, ranges and worded report entries) done; their asks marked done.
- 37 blocked fields: owner-decision 18, owner-reply 2, standing-hold 9, author 1, compute 7. Labels not applied (coordinator's).
- #544 and #684 closes recorded.
- Closeable on the branch: #420, #428, #446, #594, #600, #607, #610, #640, #810, plus #540 and #541 after merge, and #819 (already on main). Drafts in the PR body.
- Follow-ups: the 11 replies --github's #541 check flags; follow-ups now due on #238, #256, #366, #522; stale validation owners think-juuq, think-nv5o, think-ndvg, think-f40c, think-nqnl (P5).
