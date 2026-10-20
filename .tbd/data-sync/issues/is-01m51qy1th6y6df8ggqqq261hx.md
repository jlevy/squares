---
type: is
id: is-01m51qy1th6y6df8ggqqq261hx
title: "Records: T-185 to T-190 to V3/C3 after the 16 October review, adopt 15 houses and regularize them on the new witnesses"
kind: task
status: closed
priority: 1
version: 16
delegate: user-eb-records-185-190
labels:
  - result-import
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T06:56:00.849Z
updated_at: 2026-10-17T01:42:47.758Z
started_at: 2026-10-16T06:56:10.518Z
closed_at: 2026-10-17T01:42:47.758Z
close_reason: "Landed in the regularization stack, merged into main on 16-17 Oct (#644 b35a6289f, #653 3301a1cf6, #654 5012a97d6, #656 76cb5cbdb, #657 c593e2bfd); PENDING_ALLOWED is empty on main."
resolution: null
duplicate_of: null
---
Stage 4 exit (records lane) for T-185 to T-190, after the review of 16 October (think-tdna; PR #648; docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md): all six accepted for finite feasibility, each supports V3/C3 with its confirming evidence entry (E-couzo-506-n175-exact-feasibility, E-mishapolk-70a033f-exact-feasibility, E-evand-606-n146-exact-feasibility, E-couzo-487b058-exact-feasibility, E-couzo-607-exact-feasibility, E-couzo-4e4c8ce-n237-exact-feasibility); findings RT-1 to RT-13, none blocking or major. Write the confirming evidence, map the review, derive the rungs, set the reviewed significance (T-185 S1->S2, T-188 S1->S2, T-189 S2->S3, T-190 S1->S2), fix RT-1 to RT-4, and adopt the houses the review's Adoption per Count names: T-186 at 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304; T-187 at 146; T-188 at 211; T-190 at 237 (15 counts). By the intake step of #641, every re-housed count is regularized in the same PR (both strong generators on the new witnesses, select, admit) or allowlisted with an open bead. Stacked on the top of the regularization stack (#644 -> 3b -> 3c -> leftovers).

## Notes

2026-10-16 07:10Z user-eb-records-185-190: started. Worktree .claude/worktrees/records-185-190, branch claude/intake-2026-10-16-records-185-190 from #648 head 9bd813b2b. Part 1 (evidence, rungs, reviews, scores, RT-1..RT-4) first; stack top at 07:05Z is only #644 (3a, 780d81b82): 3b/3c/leftovers not pushed yet.

2026-10-16 07:25Z user-eb-records-185-190: part 1 pushed (c83680311: six confirming entries, V3/C3, reviews, scores, RT-1..RT-7/RT-10/RT-11; RT-4's T-161 question left to the owner; RT-8 not retained). Merged #644 3a (5f613b85e, one v0.7.15 for both). Next: adoption code (upper_bound_houses + adopt_houses) and adopt_houses write.

2026-10-16 07:47Z user-eb-records-185-190: adoption written in the worktree (adopt_houses: 15 houses; witnesses/renderings via build_known_best_atlas --update --n, 9m wall; axis tool --update-atlas on the 15, 290 s wall at 2 workers, 5 strong views lapsed: 129 146 156 176 271; default_drawings --update: 18 pending, 204/303 SETTLED stale). Generators started 07:46Z in scratchpad laneJ/runs (evand z7wn-adopt-1016 --workers 1; grid-slack z7wn-adopt-deg05/deg1/deg5-1016 serial), 2 processes niced. Not yet committed: adoption data + code (uncommitted in worktree).

2026-10-16 08:30Z user-eb-records-185-190: pushed 8e02327fa: adoption (8de04c413), views+URL amendments+T-181 302 report atom split (c2eed83c2), merged #648 at 2ea1d00bb (13eae8385), A2/A7/A9/RT-8 alignment. Generators restarted 07:57Z in two batches (A=129..211, B=232..304; evand z7wn-{a,b}-1016 --workers 1, grid z7wn-{a,b}-deg{05,1,5}-1016), first attempt 07:46-07:56Z aborted (set aside in laneJ/aborted). Next: selection/admission per batch; if B cannot finish by ~11:45Z, defer B to PENDING_ALLOWED with a new bead under think-sfas.

2026-10-16 11:59Z user-eb-records-185-190: all 8 z7wn runs finished 09:43Z (evand z7wn-a/b-1016: 1,554 + 3,263 CPU-s; grid-slack z7wn-a/b-deg05/1/5-1016: 3,487 CPU-s). Selection killed by the 10:40Z restart; rerun as batches: A (129..211) done 11:52Z: 6 regularized (129 146 175 204 evand same-side; 154 grid 5 deg; 156 grid 0.5 deg), 176 and 211 decided no better (211 all views row 7 review). B (232 237 264 271 302 303 304) not selected: allowlisted under new bead think-r3cl (child of think-sfas, claimed). Merged #653 3b locally (48c1054ec), axis rerun done; next: merge leftovers/3c heads, admit A, renders, retain run evidence, re-pin, edition, push, draft PR by 13:15Z.

2026-10-16 12:41Z user-eb-records-185-190: DONE. Draft PR #657 (https://github.com/jlevy/squares/pull/657, base claude/intake-2026-10-16-regularize-leftovers at 7e44e4bdb, labels intake + S3), head b64187bdf. Includes #648 (2ea1d00bb) and the stack (3a, 3b 4da7ae92d, 3c 97d513032, leftovers). V3/C3 for T-185..T-190; 15 houses; regularized 129 146 154 156 175 204; settled 176 211; 232 237 264 271 302 303 304 in PENDING_ALLOWED under think-r3cl (runs done, selection owed). Site: folded into the stack's v0.7.15 (v0.7.16 cut reverted, since the impact check reads origin/main). records tier 0 failures; focused tests 624 pass after 2 updates. Replies drafted in think-o644, think-rvv7, think-qik6 (incl. #506). Can close at merge: think-z7wn; think-r3cl stays open.

2026-10-16 13:12Z user-eb-records-185-190: CI fix + review B round pushed: 4dcac3d03 (B1 sparse checkout +4 packets; B2 bound-citations, family census, translation screen, 574 algebraic claims, closed form 302; B3 211 -> PENDING_ALLOWED think-r3cl; B5 176 text), re-pin daee851d4. 330 focused tests pass locally. Poster composites not redrawn. PENDING_ALLOWED now 8 (211, 232, 237, 264, 271, 302, 303, 304).

2026-10-16 13:17Z user-eb-records-185-190: head 733794e33 pushed (merged leftovers' new head 6ecb4c810; papers' no-change record covers bound-citations.json). Local records tier at 733794e33: 0 failures (124 s). Hosted CI running.

2026-10-16 13:43Z user-eb-records-185-190: STOPPED at head 7b91fb238 (pushed, clean). Review B: B1 FIXED (sweeps sparse checkout + 4 house packets, 4dcac3d03); B2 FIXED for bound-citations (+211 test pin), X049 family census, contact-shade census (ee644ee38), translation-escape screen (+SCREEN_FINDINGS tripwires in validate.py, +176 in the test's unstable list), PR 574 algebraic claim record, closed form at 302, rigidity blocks at 10 records (7b91fb238); B2 NOT FIXED: poster composites (not redrawn; suite-a's test_known_best_atlas poster tests fail on them: 211 caption 14.99356 vs 14.99355, credits 26 vs 28; needs the infographics successor, a merge-time step); B3 FIXED (211 to PENDING_ALLOWED under think-r3cl); B5 FIXED (176 text); B4 the coordinator's. CI at ee644ee38: suite-d (rigidity tests, now fixed locally: 23 pass), suite-a (poster tests), validate (rigidity + release impact, both fixed in 7b91fb238) failed; at 7b91fb238 CI just started, not yet observed. Local: records tier 0 failures at 733794e33; 330 focused tests pass.

2026-10-16 13:57Z user-eb-records-185-190: head 5d5eb2dec pushed (fast-forward over 7b91fb238). bda885404: build_composite_figure_data --update (10 rigidity scope sentences copied from the rewritten case blocks; no value, rung, house or drawing), for hosted sweeps' composite-figure check and suite D's test_current_prospective_figure_is_identical_to_the_retained_record; re-pin 5d5eb2dec. Local: 59 focused tests pass (test_rigidity_status, test_composite_figure_displays, test_frontier_rigidity_assessment); records tier 0 failures (124 s). Left red by instruction: suite-a's poster caption and credit tests (infographics cut, think-nv87). Hosted CI at 5d5eb2dec not yet observed.

2026-10-16 19:57Z user-eb-stack: handover. The owner handed the regularization stack (#644 -> #653 -> #654 -> #656 -> #657) to lane S (user-eb-stack); claim skipped (held by its earlier lane), carrying on per the brief.

2026-10-16 21:08Z user-eb-stack: #657 at 1f343b743 (stack merged in 26c6817a5; think-r3cl's selection admitted; B2 poster pins 6d3ea4a3e; B dispositions review 5553667876). think-z7wn can close at #657's merge.

2026-10-17 01:42Z user-eb-stack: #657 at f8071ce60 ready to merge (packing-required, pages-required, deep-gate-required green). Close at #657's merge.
