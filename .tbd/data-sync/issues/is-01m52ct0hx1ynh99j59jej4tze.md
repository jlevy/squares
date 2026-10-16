---
type: is
id: is-01m52ct0hx1ynh99j59jej4tze
title: "default_drawings --compare misses strong-view losses whose replacement is the axis tool's view (7 of 7 at #657's adoption)"
kind: bug
status: closed
priority: 1
version: 8
delegate: user-eb-addr-641
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdvvpwz9asfq2gvaxfz5w
hold: null
hold_until: null
created_at: 2026-10-16T13:00:48.573Z
updated_at: 2026-10-16T20:34:45.526Z
started_at: 2026-10-16T17:51:29.706Z
closed_at: 2026-10-16T20:34:45.526Z
close_reason: "Fixed in #641 (strong_view_losses under the improvement rule; marks only counts still pending), merged at 68cdbc614 on 16 Oct."
resolution: null
duplicate_of: null
---
From PR #657 review B4 (https://github.com/jlevy/squares/pull/657#pullrequestreview-5548086952): #641's `default_drawings --compare` predicate (`falls_to_irregular_house` at 7aa4775ea) flags a strong view lost by a deferral or adoption only when the new drawing is the house drawing. After #657's adoption every new drawing at a lost strong view is the axis tool's view, so the predicate flags 0 of the 7 losses (176, 211, 232, 237, 264, 271, 302); the worst is 302: 0/0/0/14/14/978/978 -> 6/26/11/40/19/882/952. Fix in #641 (or a follow-up before the next adoption): flag any strong view whose replacement is worse on some goal of the improvement rule, whatever drew the replacement, with a test at a real-shaped count; then rerun --compare on #657 and list the losses for the owner.

## Notes

2026-10-16T17:59Z user-eb-addr-641: #641 review D addressed in badaf21f0 (pushed from 7aa4775ea after a fetch confirmed it unmoved). D1: falls_to_irregular_house -> strong_view_losses: marks a drawn strong view whose replacement, whatever drew it, is worse on a goal of the improvement rule (7 measures, larger side, exactness for a house not shown exact), naming the goals; one wording STRONG_VIEW_LOST in summary, printout, runbook, guide. D2: docs and --help use origin/$BASE. Replay on #657 (base 6ecb4c810 -> head 5d5eb2dec): 15 changed, 9 marked: 146, 156, 176, 211, 232, 237, 264, 271, 302. Focused pytest 85 passed. Next: records tier, CI, PR body, dispositions; then #650.

2026-10-16T18:06Z user-eb-addr-641: D dispositions posted on #641 at badaf21f0: https://github.com/jlevy/squares/pull/641#pullrequestreview-5551825905 (D1 fixed option b, D2 fixed; no deferrals). PR body updated. Records tier 51/52: the one red step is site_urls history vs origin/main (t-193/t-194 registered on main after the base); passes vs e2e018f32. Next: #641 hosted CI to final; #650 merge ae6adcac3 + B1 fix.

2026-10-16T18:36Z user-eb-addr-641 DONE: #641 head badaf21f0, CI green (43 ok/16 skipped; Packing validation 38943929105, Deferred checkpoint 38943928911); D reply https://github.com/jlevy/squares/pull/641#pullrequestreview-5551825905. #650 head 18a21ac8b (merge ae6adcac3 of badaf21f0, B1 fix 18a21ac8b); B reply https://github.com/jlevy/squares/pull/650#pullrequestreview-5551850063; CI red only in validate/packing-required: site_urls history vs origin/main (t-193/t-194 registered on main by #642/#651; #650's merge ref is with #641's branch) -- clears at retarget (think-bb70). think-cmj7 can close when #641 merges.

2026-10-16T19:06Z user-eb-addr-641: review E on #641. Pushed c5d7e08ba (merge main 7b34cd5bb, clean; site_urls history 0 failures, release_pin ok 0afbc796e52c) and 453128d1c (E1: DEFERRAL_WAITS/UNDEFERRED in #660's words, line 624 owner hold removed; E2: mark only later-pending counts). #657 replay: 9 listed, 6 marked (211 232 237 264 271 302). Focused tests 90 passed. Next: records tier, CI, PR body (E3), E dispositions.

2026-10-16T19:42Z user-eb-addr-641 DONE review E: #641 head 453128d1c, CI green (43 ok/16 skipped; Packing validation 38952444584, Deferred checkpoint 38952444505), mergeable clean. E reply https://github.com/jlevy/squares/pull/641#pullrequestreview-5552523129 (E1/E2/E3 fixed). #650 and #660 should merge 453128d1c; #660 meets small conflicts (step 3 lines, stage 5 opening, mark lines): take #660's house-rule links on top.
