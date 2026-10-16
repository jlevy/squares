---
type: is
id: is-01m51qy1th6y6df8ggqqq261hx
title: "Records: T-185 to T-190 to V3/C3 after the 16 October review, adopt 15 houses and regularize them on the new witnesses"
kind: task
status: in_progress
priority: 1
version: 8
delegate: user-eb-records-185-190
labels:
  - result-import
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T06:56:00.849Z
updated_at: 2026-10-16T12:40:02.659Z
started_at: 2026-10-16T06:56:10.518Z
---
Stage 4 exit (records lane) for T-185 to T-190, after the review of 16 October (think-tdna; PR #648; docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md): all six accepted for finite feasibility, each supports V3/C3 with its confirming evidence entry (E-couzo-506-n175-exact-feasibility, E-mishapolk-70a033f-exact-feasibility, E-evand-606-n146-exact-feasibility, E-couzo-487b058-exact-feasibility, E-couzo-607-exact-feasibility, E-couzo-4e4c8ce-n237-exact-feasibility); findings RT-1 to RT-13, none blocking or major. Write the confirming evidence, map the review, derive the rungs, set the reviewed significance (T-185 S1->S2, T-188 S1->S2, T-189 S2->S3, T-190 S1->S2), fix RT-1 to RT-4, and adopt the houses the review's Adoption per Count names: T-186 at 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304; T-187 at 146; T-188 at 211; T-190 at 237 (15 counts). By the intake step of #641, every re-housed count is regularized in the same PR (both strong generators on the new witnesses, select, admit) or allowlisted with an open bead. Stacked on the top of the regularization stack (#644 -> 3b -> 3c -> leftovers).

## Notes

2026-10-16 07:10Z user-eb-records-185-190: started. Worktree .claude/worktrees/records-185-190, branch claude/intake-2026-10-16-records-185-190 from #648 head 9bd813b2b. Part 1 (evidence, rungs, reviews, scores, RT-1..RT-4) first; stack top at 07:05Z is only #644 (3a, 780d81b82): 3b/3c/leftovers not pushed yet.

2026-10-16 07:25Z user-eb-records-185-190: part 1 pushed (c83680311: six confirming entries, V3/C3, reviews, scores, RT-1..RT-7/RT-10/RT-11; RT-4's T-161 question left to the owner; RT-8 not retained). Merged #644 3a (5f613b85e, one v0.7.15 for both). Next: adoption code (upper_bound_houses + adopt_houses) and adopt_houses write.

2026-10-16 07:47Z user-eb-records-185-190: adoption written in the worktree (adopt_houses: 15 houses; witnesses/renderings via build_known_best_atlas --update --n, 9m wall; axis tool --update-atlas on the 15, 290 s wall at 2 workers, 5 strong views lapsed: 129 146 156 176 271; default_drawings --update: 18 pending, 204/303 SETTLED stale). Generators started 07:46Z in scratchpad laneJ/runs (evand z7wn-adopt-1016 --workers 1; grid-slack z7wn-adopt-deg05/deg1/deg5-1016 serial), 2 processes niced. Not yet committed: adoption data + code (uncommitted in worktree).

2026-10-16 08:30Z user-eb-records-185-190: pushed 8e02327fa: adoption (8de04c413), views+URL amendments+T-181 302 report atom split (c2eed83c2), merged #648 at 2ea1d00bb (13eae8385), A2/A7/A9/RT-8 alignment. Generators restarted 07:57Z in two batches (A=129..211, B=232..304; evand z7wn-{a,b}-1016 --workers 1, grid z7wn-{a,b}-deg{05,1,5}-1016), first attempt 07:46-07:56Z aborted (set aside in laneJ/aborted). Next: selection/admission per batch; if B cannot finish by ~11:45Z, defer B to PENDING_ALLOWED with a new bead under think-sfas.

2026-10-16 11:59Z user-eb-records-185-190: all 8 z7wn runs finished 09:43Z (evand z7wn-a/b-1016: 1,554 + 3,263 CPU-s; grid-slack z7wn-a/b-deg05/1/5-1016: 3,487 CPU-s). Selection killed by the 10:40Z restart; rerun as batches: A (129..211) done 11:52Z: 6 regularized (129 146 175 204 evand same-side; 154 grid 5 deg; 156 grid 0.5 deg), 176 and 211 decided no better (211 all views row 7 review). B (232 237 264 271 302 303 304) not selected: allowlisted under new bead think-r3cl (child of think-sfas, claimed). Merged #653 3b locally (48c1054ec), axis rerun done; next: merge leftovers/3c heads, admit A, renders, retain run evidence, re-pin, edition, push, draft PR by 13:15Z.

2026-10-16 12:41Z user-eb-records-185-190: DONE. Draft PR #657 (https://github.com/jlevy/squares/pull/657, base claude/intake-2026-10-16-regularize-leftovers at 7e44e4bdb, labels intake + S3), head b64187bdf. Includes #648 (2ea1d00bb) and the stack (3a, 3b 4da7ae92d, 3c 97d513032, leftovers). V3/C3 for T-185..T-190; 15 houses; regularized 129 146 154 156 175 204; settled 176 211; 232 237 264 271 302 303 304 in PENDING_ALLOWED under think-r3cl (runs done, selection owed). Site: folded into the stack's v0.7.15 (v0.7.16 cut reverted, since the impact check reads origin/main). records tier 0 failures; focused tests 624 pass after 2 updates. Replies drafted in think-o644, think-rvv7, think-qik6 (incl. #506). Can close at merge: think-z7wn; think-r3cl stays open.
