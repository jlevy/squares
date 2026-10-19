---
type: is
id: is-01m5279qrmrrbgygjevvr1ppcq
title: Regularize the counts the 16 October adoption left pending (selection and admission owed)
kind: task
status: closed
priority: 1
version: 13
delegate: user-eb-records-185-190
labels:
  - validation
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-16T11:24:32.404Z
updated_at: 2026-10-17T01:42:48.354Z
started_at: 2026-10-16T11:24:43.640Z
closed_at: 2026-10-17T01:42:48.354Z
close_reason: "Landed in the regularization stack, merged into main on 16-17 Oct (#644 b35a6289f, #653 3301a1cf6, #654 5012a97d6, #656 76cb5cbdb, #657 c593e2bfd); PENDING_ALLOWED is empty on main."
resolution: null
duplicate_of: null
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

2026-10-16 19:57Z user-eb-stack: handover. The owner handed the regularization stack (#644 -> #653 -> #654 -> #656 -> #657) to lane S (user-eb-stack); claim skipped (held by its earlier lane), carrying on per the brief.

20:56Z user-eb-stack: selection over z7wn-b runs (+ z7wn-a at 211), --workers 2, 28 min wall: grid-slack views admitted at 232, 264, 271 (0.5 deg) and 302 (5 deg); 237, 303, 304 settled decided-no-better (SETTLED, runs _RUNZ7WN_B, selection-r3cl.json/.md retained); 211 stays in PENDING_ALLOWED: every strong view (Daniel same-side/solved, grid-slack at 0.5/1/5 deg) is at row 7 (decision: review, worse: none), which the selection never admits and which only the owner's review can draw (policy section 5's review record does not exist yet). #657 head 1f343b743 (data 796a1d032, re-pin bce5db428). Records tier and verify-atlas running.

2026-10-16 21:08Z user-eb-stack: phase 1 done. #657 head 1f343b743: 232/264/271/302 regularized (grid-slack), 237/303/304 settled, 211 left in PENDING_ALLOWED (all strong views at row 7, review; the owner decides). This bead must stay open until a PR takes 211 off. Records tier 50/52 (two origin/main comparisons, base moved), verify-atlas on the 8 counts passed, 333 focused tests passed; hosted shards all green, validate red only on the origin/main comparisons. Review B dispositions posted (review 5553667876).

Owner, 16 Oct ~20:45Z, in the coordinator's session (AskUserQuestion): 211, Evan Daniel's same-side row-7 view of T-188's witness (2/10/3/17/17, 545/555, better on all seven measures): 'Admit it (Recommended)'. Lane S writes the section 5 review record and admits the view in #657 with the stack review's findings.

2026-10-16 22:18Z user-eb-stack: what closes this bead (review H7 of #657). The owner answered the 211 question: 'Admit it.' #657's next pass (local commits 6eae2cfbc and ee900f469 on top of 1f343b743, pushed with the cascade after #644 merges) writes the layer's first review record, packing/atlas/known-best/regularized/reviews.yaml, with its gallery retained under packing/cases/regularized_drawings/think-z7wn-2026-10-16/review-211/. It admits Evan Daniel's same-side view at 211 through it and takes 211 off PENDING_ALLOWED, which is then empty; nothing else names this bead. Close it once #657 merges (bead-tree rule: not before).

2026-10-17 00:35Z user-eb-stack: #657 pushed at 5cc2b5a83 with the 211 admission (reviews.yaml, gallery in review-211/), review H fixes, main merged (#644, #653, #654, #656 all merged), site v0.7.23. PENDING_ALLOWED empty; this bead closes when #657 merges. Review H dispositions: review 5555092825.

2026-10-17 01:42Z user-eb-stack: #657 at f8071ce60 green with the deep gate (run 38990141142); review J fixed (dispositions 5555312225). 211 admitted by the owner's review (reviews.yaml); PENDING_ALLOWED empty. Close at #657's merge.
