---
type: is
id: is-01m4y1hjs107rt9h7hbztpmbh6
title: "Records PR after #602 merges: credit Ryan Xu by name on main; T-174 and T-180 text; Fang direct evidence and rows 421-814 to replayed; #605's News entry"
kind: task
status: in_progress
priority: 1
version: 2
delegate: serene-hopper-records
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T20:27:00.250Z
updated_at: 2026-10-14T22:04:00.422Z
started_at: 2026-10-14T22:04:00.417Z
---
The follow-on edits the coordinator handed over, all on files #602 owns until it merges. Open the PR after #602 lands, on claude/serene-hopper-xxh80m restarted from main.

1. Ryan Xu by name (owner, 2026-10-14). In packing/resources/bibliography.yaml, change [ry-xu square packing 2026]'s authors to Ryan Xu and credited_names ry-xu: ry-xu to Ryan Xu: Xu. Fix register prose credits in T-125, T-136, T-146 and T-159 and the 'Credit to ry-xu' notes. Keep keys, paths and URLs.
2. T-174 (PR #574): 17 undecided comparisons decided exactly, by devtools.decide_undecided_comparisons. It is above at 14 counts and equal at 54, 107 and 178; 29, 55, 71 and 83 stay gated. The receipt is packing/campaign/issue-intake/upper-bounds-20261014/undecided-resolved.json, on main via #605.
3. T-180 (wand125 closed form): the calibration basis. replay4d replays here at 1.22x the source's CPU, so the full replay is about 5,250 CPU-h, held over the owner's 40 CPU-h cap. See packing/resources/web/wand125-closed-form-2026-10-14/calibration-plan.md.
4. Fang direct: extend E-fang-direct-exact-feasibility from [380, 381, 382] to all 14 counts, and move the rows at 421-814 from assurance: reported to replayed. The receipts are per count, receipts/exact-certification-nNNN.json.xz, on main via #605.
5. Write #605's site-changelog.yaml entry (or an omission) and this PR's own, per development.md 'Maintaining the project changelog'. Cut the site edition if release impact requires it.
Merge with a merge commit.
