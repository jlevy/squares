---
type: is
id: is-01m5279qrmrrbgygjevvr1ppcq
title: Regularize the counts the 16 October adoption left pending (selection and admission owed)
kind: task
status: in_progress
priority: 1
version: 5
delegate: user-eb-records-185-190
labels:
  - validation
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-16T11:24:32.404Z
updated_at: 2026-10-16T17:17:04.344Z
started_at: 2026-10-16T11:24:43.640Z
---
Select and admit the strong-generator views of the counts the 16 October adoption (think-z7wn, branch claude/intake-2026-10-16-records-185-190) re-housed and could not decide by its stop time: the runs are done, the selection and admission are owed. Each count is in default_drawings.PENDING_ALLOWED under this bead.

## Validation
- Claim: the regularized drawing of each listed count on its new house witness (T-186 at 232, 264, 271, 302, 303, 304; T-190 at 237), decided by both strong generators under the improvement rule.
- Run: the generator runs are finished and their receipts and per-count reports are retained in packing/atlas/known-best/regularized/runs/ (evand-regularize-z7wn-b-1016, grid-slack-z7wn-b-deg05-1016, grid-slack-z7wn-b-deg1-1016, grid-slack-z7wn-b-deg5-1016); their full directories were in the lane-J session scratch (laneJ/runs/), which may be gone, in which case run both generators again on the counts (regularization-process.md, "When a Witness Changes") under new directory basenames. Then `python -m devtools.regularize_select --evand-run RUNS/z7wn-b-1016 --grid-run RUNS/z7wn-b-deg05-1016 RUNS/z7wn-b-deg1-1016 RUNS/z7wn-b-deg5-1016 --workers 2`, the `layer` commands it prints, step 5's renders, SETTLED for no-better counts, and each count off PENDING_ALLOWED.
- Cost: generators done (evand 3,263 CPU-s, grid-slack 1,995 CPU-s at the three thresholds); the selection about 1 to 2 CPU-hours by the 16 October receipts on a loaded host; admission and renders minutes.
- Budget status: runnable, within the pass's cap.
- Possible subset under the cap: none needed.
- Depends on: the records PR of think-z7wn (the new witnesses) merging, or working on its branch.
- Done when: each listed count is regularized or settled on its current witness and off PENDING_ALLOWED, in a merged PR.
- Machine note: the selection decides every view on both exact routes; give it 2 workers, niced.

## Notes

2026-10-16 12:41Z user-eb-records-185-190: created by the think-z7wn records lane; PR #657 names 232, 237, 264, 271, 302, 303, 304 in PENDING_ALLOWED under this bead. Runs retained in packing/cases/regularized_drawings/think-z7wn-2026-10-16/ (z7wn-b-1016, z7wn-b-deg05/deg1/deg5-1016: receipts and per-count reports; the full run dirs with views are in /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneJ/runs/ on this host, not retained). Next: regularize_select over the four b runs (--workers 2), the layer commands it prints, renders, SETTLED, take the counts off the list.

2026-10-16 13:12Z: 211 added to this bead's PENDING_ALLOWED entries (review B3 of #657): its runs were selected and every strong view is at row 7, for the owner's review; Daniel's same-side view betters the axis view on all seven measures.

Owner's policy, 16 Oct afternoon: always adopt the smallest packing and regularize it. The 8 counts #657 allowlisted (211, 232, 237, 264, 271, 302, 303, 304) are selected and admitted in #657 before it merges (coordinator's plan); 176 is adopted as settled on the owner's word.
