---
type: is
id: is-01m5kjb1djc8q6yy990cmn3fys
title: "Apply the owner's sub-print answer: rerun the history, #719 and #732 walks with SUB_PRINT holds as restatements (think-fwa9, 2026-10-23)"
kind: task
status: closed
priority: 1
version: 5
delegate: c-answers-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T05:04:34.738Z
updated_at: 2026-10-23T15:52:33.471Z
started_at: 2026-10-23T07:54:15.406Z
closed_at: 2026-10-23T15:52:33.470Z
close_reason: "Applied in PR #754 (https://github.com/jlevy/squares/pull/754), head 41c43051c, CI green (runs 39979866593, 39979866417, 39979860680): the restatement ruling in the history, #719 and #732 walks; every SUB_PRINT hold settled, no row changed; #719's 631 left to think-oqjd; follow-ups for #715, #719 and #732 drafted in the notes, not posted."
resolution: null
duplicate_of: null
---
Owner decision of 23 October (think-fwa9 note): sub-print re-certifications are restatements. Remove the SUB_PRINT holds from beyond_horizon_replay's walks (HISTORY_RESTING, the #719 walk's resting, #732's 499), rerun the walks, confirm no current row changes, and answer #715, #719 and #732 where their replies named the question. After #742 merges; may ride the #719 records PR (claude/intake-2026-10-23) if small, else its own.

## Notes

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754, branch claude/intake-2026-10-23-owner-answers).

**Done.** devtools.intake_ledger gains the owner's rulings as an input of a walk (`rulings`
in sources.yaml and ledger.yaml, `RULINGS`, `Rulings`): `restatement` (think-fwa9) and
`classical-constructions` (think-8krd), applied through 1024 in the history, #719 and #732
walks (`beyond_horizon_replay.WALK_RULINGS`); the backlog walk and every earlier ledger
apply none and render byte-identically. A claim below every member but within 1e-12 of
the member it is closest below, a report and not a construction, at the same 12-place
print, is `not recorded`, reason `restates`. The SUB_PRINT and GOEBEL_ABOVE hold classes are
gone; the walks were rerun (sources, gather --snapshot, render).

**Rerun result.** Every SUB_PRINT hold became a restatement: Couzo's 74 (5a299b4 31,
23aff0c 10, 4e4c8ce 3 in the history walk; and the 30 of #715), #732's 499, and in the
#719 walk #715's 19 and 5a299b4's 366, 372. The verdicts that rested on them (5a299b4 at
325, 333, 362, 401, 442, 485, 530, 577 and the 19 in the #719 walk; #719's 366) are now
decided against the reports they restate: each is a restatement or stays not recorded.
No current row changes, and no row at all changes from this ruling (coverage_problems and
chain_problems: none; the register's only row edits are the Göbel ones, think-8krd).

**Found, not decided (think-oqjd).** The ruling's words also reach #719's 631, another
holder's re-certification (2.73e-13 below Couzo's 4e4c8ce certificate, same 12-place print)
that #722 recorded. It is listed under the ruling's `awaiting_owner` in the history and
#719 walks, walked as before (recorded, superseded on main by #732's row). Applying the
ruling to it would remove that superseded row; no current row would change.

**Follow-ups drafted (not posted).**

- #715: "Follow-up on the 30 re-certifications. On 23 October the maintainer decided the
  question the earlier replies left open: a side below an earlier report at its count by
  less than the 12-place print, with both rounding up to the same 12-place print, restates
  that report, and the earlier report stays the row. Your 30 certificates first committed
  at 5a299b4 are 2.37e-23 to 3.18e-23 below your 4e4c8ce certificates and round up to the
  same print, so they restate them: the 4e4c8ce certificates stay the rows there, and no
  row changes. The same rule covers 44 more of your publications in 5a299b4, 23aff0c and
  4e4c8ce. Your 743 and 985 equal the bounds your 4e4c8ce index states there by deleting a
  square from the next count's certificate; such a bound is an earlier report, so they are
  not recorded either. The runbook states both rules (Several Reports at One Count) since
  https://github.com/jlevy/squares/pull/754. Still open here: the exact check at 335, and
  the rows above 1024, which the record will now track (that work is under way)."
- #719: "Follow-up on two questions the earlier replies left open, decided on 23 October.
  Re-certifications below the 12-place print restate the report they beat: in this issue's
  walk #715's at 19 counts and Couzo's 5a299b4 files at 21 restate his 4e4c8ce
  certificates, and none of your rows changes. Your 631 is 2.73e-13 below his 4e4c8ce
  certificate and both round up to 25.656854249519; it stays recorded while that case is
  with the maintainer, and your #732 row supersedes it either way. Of the ten files your
  edit withdrew, the nine where #732 claims a lower file (411, 451, 494, 495, 540, 583,
  587, 632, 683) are not reports, so your #732 rows there stand; 539 is #732's own row. The
  34 in-corpus files you left to us stay pinned by digest."
- #732: "Follow-up on what the acknowledgement left open, decided on 23 October. 499 is
  8.66e-13 below your #719 row and both round up to 22.881306218113: it restates that row,
  which stays the count's row. The nine 1851c2c files #719's edit withdrew are not reports,
  so your 77 rows stand. Göbel's classical constructions now count as earlier reports
  beyond 324: your 331, 369 and 376 (18.707106781187, 19.707106781187, 19.899494936612)
  are rational enclosures just above Göbel's exact sides there (18 + sqrt(2)/2, 19 +
  sqrt(2)/2, 10 + 7 sqrt(2)), so they are not recorded. 985 equals the bound Couzo's
  4e4c8ce index states there by deleting a square from his 986 certificate; such a bound is
  an earlier report, so 985 is not recorded. No row changes."

**Validation.** See the PR's Validation section. Closed by c-answers-1023 at CI green with
the head commit, or by the coordinator after merge. Addendum (D6, 23 October): the
owner also answered D6 (think-f2io); the #715 and #732 drafts above carry it.
