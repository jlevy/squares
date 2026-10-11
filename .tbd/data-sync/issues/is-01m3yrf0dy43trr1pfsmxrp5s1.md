---
type: is
id: is-01m3yrf0dy43trr1pfsmxrp5s1
title: "Stacked PR on #298: verifier provenance and the independent verifier"
kind: task
status: closed
priority: 1
version: 7
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:51.358Z
updated_at: 2026-10-03T22:39:33.323Z
closed_at: 2026-10-03T22:39:33.323Z
close_reason: "#311 merged into main at 4043d863e; remaining verifier slices tracked under think-gpe0 (think-3ok2, think-th8p, think-j1pd)."
resolution: null
duplicate_of: null
---
Branch stacked on claude/zealous-gauss-jem7l9; carries the verifier-provenance epic and the independent-verifier slices. Draft until its lanes land; green and mergeable after #298. Merge order #290 -> #292 -> #298 -> this.

## Notes

Branches to stack (all pushed): claude/lane-x-verifier-provenance, claude/lane-w1-verifier-spec, claude/lane-w2-fast-verifier-wip. Base: claude/zealous-gauss-jem7l9 after the records lane's pushes. After merging, re-run packing/devtools/backfill_verifier_relation.py (lane X) on the merged evidence.yaml rather than hand-resolving conflicts; render views; open as draft PR with base claude/zealous-gauss-jem7l9. Full state: think-20pp notes.
2026-10-03 06:00 #311 CI red on fdae100df (run 37098372802): checks tier 168s over the 140s ceiling (sqverify-fast step 84s); Status cell qualifier breaks test_results_md_labels_every_result_by_its_kind; verifier registry undeclared verified_upper_bound consumer; DATA_REVISION and n-012 inherited from #298. Cloud lane SP2 (session_013RU7RpqfBqeDcpo29X5RJ8) owns driving #311 green; W2 keeps the crate source. #298 also has a real conflict with main (#310's site tables, ea0a3b19a): the records lane is merging main first.
2026-10-03 16:25 SP2 on #311: merged #298 through ee4102e59, W2 4ddf37d9c and both review branches (RA ca6ea4cd7, RB 299ce0681). b928e0362: measure_verifier is its own pull-request tier and job (90 s ceiling, pending under think-th8p; read 32.07 s and 19.83 s hosted), so checks read 119.5-120.5 s. 0d65f68c2: the full check_sqverify_fast is a deferred step in deferred-controls-finer (49.58 s; post-merge surface green on dispatch 37134371034). Typecheck missed 111 s by 0.46 s on PR run 37134368166 (runner drift, think-t7k5). Records decisions for the T-079 merge: native-parent-core entry gets independence_record verify_evand_angle_net_native.py; the s12 audit entry is a premise check (not-applicable, not a deciding replay), fixed on #298 by the records lane and via the backfill FIX table on #311 meanwhile. E-n061 FF replay corrected to same-implementation on both branches.
2026-10-03 17:40 Owner merged #290 into main at 16:45 (1c21ee6be); GitHub rebased #292 onto main (f40260d50; five patches identical by range-diff to 2b7191461..91bd92b78). Restack plan (no history rewrite): #292 lane fixes its pin and the intro example; the records lane merges main into #298, then 'git merge -s ours f40260d50', then #292's fix commits normally; SP2 then merges #298 into #311. A stray merge of main (b9a4bf908) was pushed to the merged #290 branch at 17:04; harmless, left. #311's description now summarizes the whole stack (published 17:40; 38 KB; check_pr_description passes), with the results table from the new devtools.render_stack_results (local branch stack-results-tool 9319ca8a2, to be merged into #298). Refresh after the restack.
