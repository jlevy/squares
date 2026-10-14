---
type: is
id: is-01m4wyep8wzf5r5ah673af8xcb
title: "render_announcement: Review A of PR 598, findings A1, A2, A5, A10, A11, A14, A15 (layer 5's tool, #563)"
kind: bug
status: open
priority: 2
version: 5
delegate: null
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-14T10:13:45.372Z
updated_at: 2026-10-14T10:30:08.624Z
started_at: 2026-10-14T10:29:34.480Z
---
Review A on https://github.com/jlevy/squares/pull/598#pullrequestreview-5516346807 found, in packing/devtools/render_announcement.py (layer 5, #563): A1 counts() treats the case lane's regularization of the entry's own packing as a rival (T-136 drops six counts, T-138 two); A2 a SUPERSEDED standing drops T-009 for its own regularization T-155; A5 shown() prints up to 40 decimals where the bound cannot beat previous (--all); A11 the header date defaults to UTC; A14 MONTHS repeats adopt_houses.words; A15 serial gh api users calls. A10: bibliography credited_names has no Rio Calle entry, so --all credits T-159 to Calle. Fix on #563 or after it merges.

## Notes

2026-10-14, from #563 (layer 5) round 2, review C (https://github.com/jlevy/squares/pull/563#issuecomment-6166235040):

C5 (side effect of #563's B2 fix, --all only, not changed on #563): `statement` elides a count's number wherever a regularization of the same packing has the smaller side (Count.regularized_by). On a single-count line that leaves a statement with no number: `--ids T-009 --all` prints "s(29) ≤ … (verified), since superseded by T-155". No line of the default output does this today. Options: print the regularization's bound, or the entry's own, when the line has one count.

Status on #563 of this bead's items, as of head 455f3c604: A1 (the case lane's regularization of the entry's own packing counted as a rival) is fixed by #563's B2 (2d6170911); --ids T-136 gives 11 counts, and T-138 at 103 and 258 is no longer bettered by T-146. A5 (up to 40 decimals under --all) is fixed by #563's A5 (f2fdd9d7c). A2 is in part: T-009 at 29 is no longer bettered by T-155, its own regularization, but it is still bettered by the catalogue's 14-decimal print in the reported lane, and its standing stays SUPERSEDED, so it is left out without --all. A10, A11, A14 and A15 are untouched by #563.
