---
type: is
id: is-01m4y1hjs107rt9h7hbztpmbh6
title: "Records PR after #602 merges: credit Ryan Xu by name on main; T-174 and T-180 text; Fang direct evidence and rows 421-814 to replayed; #605's News entry"
kind: task
status: closed
priority: 1
version: 4
delegate: serene-hopper-records
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T20:27:00.250Z
updated_at: 2026-10-14T23:42:02.986Z
started_at: 2026-10-14T22:04:00.417Z
closed_at: 2026-10-14T23:42:02.986Z
close_reason: "Landed with #608 (merge 0dd9003e0): Ryan Xu credited by name across bibliography, register and case records; T-174's 17 decided comparisons; T-180's calibration basis with E-wand125-closed-form-replay4d-sample; Fang direct evidence for all 14 counts, rows 421-814 verified; #602's 21 follow-ups and the verdict comments in result-requests; News entries for #602 and #605, #597 omission; site v0.7.2."
resolution: null
duplicate_of: null
---
The follow-on edits the coordinator handed over, all on files #602 owns until it merges. Open the PR after #602 lands, on claude/serene-hopper-xxh80m restarted from main.

1. Ryan Xu by name (owner, 2026-10-14). In packing/resources/bibliography.yaml, change [ry-xu square packing 2026]'s authors to Ryan Xu and credited_names ry-xu: ry-xu to Ryan Xu: Xu. Fix register prose credits in T-125, T-136, T-146 and T-159 and the 'Credit to ry-xu' notes. Keep keys, paths and URLs.
2. T-174 (PR #574): 17 undecided comparisons decided exactly, by devtools.decide_undecided_comparisons. It is above at 14 counts and equal at 54, 107 and 178; 29, 55, 71 and 83 stay gated. The receipt is packing/campaign/issue-intake/upper-bounds-20261014/undecided-resolved.json, on main via #605.
3. T-180 (wand125 closed form): the calibration basis. replay4d replays here at 1.22x the source's CPU, so the full replay is about 5,250 CPU-h, held over the owner's 40 CPU-h cap. See packing/resources/web/wand125-closed-form-2026-10-14/calibration-plan.md.
4. Fang direct: extend E-fang-direct-exact-feasibility from [380, 381, 382] to all 14 counts, and move the rows at 421-814 from assurance: reported to replayed. The receipts are per count, receipts/exact-certification-nNNN.json.xz, on main via #605.
5. Write #605's site-changelog.yaml entry (or an omission) and this PR's own, per development.md 'Maintaining the project changelog'. Cut the site edition if release impact requires it.
Merge with a merge commit.

## Notes

2026-10-14 ~23:30Z, serene-hopper-records (records lane), worktree lane/records-3aum off origin/main 9b32da04d. Not pushed.

Commits (oldest first): 41d96c0f7 Ryan Xu credit; b01bccfa2 T-174's 17 decided comparisons; 24b8d2ea8 T-180 calibration basis and replay4d 0.1.1 hashes (+ E-wand125-closed-form-replay4d-sample, deferred case citation); 58c303ebc Fang direct certificates verified at all 14 counts; dea12db40 check_requests holds a recorded PR (#574); 38775ff40 #602's post-merge follow-ups and the 14 October verdict comments recorded; 2c6aa0327 News entries for #602 and #605; ba21cfa03 DATA_REVISION re-pin; 5bfb4a041 site v0.7.2 cut (papers keep editions by measured no-change records).

No rung moved. Gates: packing-validate --records and --edit green; check_release_impact: every candidate disposed; render_changelog --check green; targeted tests green. Snapshot 226,339,965 bytes, 152,451 under the cap.

Follow-ups: #600 owes a reply naming E-wand125-closed-form-replay4d-sample (the calibration; its 22:19Z follow-up said no record had been replayed here). PUBLICATION_REVISION ba21cfa0 is a branch commit: merge with a merge commit. Posters still list ry-xu until the next infographics redraw; the methods survey's algebraic-witness figure credit still reads "ry-xu, square_packing" (needs a survey edition). #597 and #604 have no changelog entry or omission.
