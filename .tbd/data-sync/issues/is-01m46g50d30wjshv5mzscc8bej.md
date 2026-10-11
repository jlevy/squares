---
type: is
id: is-01m46g50d30wjshv5mzscc8bej
title: Verify the wand125 mixed backlog (T-090, T-091, T-094; n != 17) with sqverify_fast on the 201-angle net, and move verified lanes the policy allows
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T17:00:30.498Z
updated_at: 2026-10-06T02:41:31.919Z
started_at: 2026-10-05T17:06:26.474Z
closed_at: 2026-10-06T02:41:31.918Z
close_reason: Done in jlevy/squares#369 (merged 34e87a86b); verdict replies posted 2026-10-06
resolution: null
duplicate_of: null
---

## Notes

## Policy (step 1), 2026-10-05 17:20 UTC

What a full sqverify_fast pass at all 201 directions counts for:
- With admission passing (exact premises: mass < n, B(1+D/(1-D^2/4)) < 1, net pinned at step 83/40000 to index 200, per-bin domain for format M), every direction `verified`, summary `VERIFIED`, exit 0, at the declared threshold 1, it proves s(n) >= L by SOUNDNESS.md's theorem. sqverify_fast src/ at 04a0a2217 is byte-identical to 4ddf37d9c, the build RA (soundness) and RB (testing, independence) accepted on 3 October; only Cargo.toml's gate-test profile was added since.
- In the register it is one evidence entry per certificate: assurance verified, method interval-certified, performed_by repository, origin replayed-here, relationship_to_generator independent-implementation, verifiers [V-sqverify-fast] (not yet in verifiers.yaml: added by this lane, first-party, decides, independence_record packing/sqverify_fast/independence-record.yaml), certificate = the retained candidate whose decompressed SHA-256 the packet pins, replay command, replay_status passed. Structurally that is V3 and C3 (epistemics.md, Verification and Confirmation), given a control path. It is a complete replay here and an independent decision of coverage, which the source-checker replays of T-069..T-075 were not.
- It is not a second method (same net-and-shrink, interval-certified), so it never raises a result already at C3 (T-069, T-071, T-072, T-075: an attribute beside the rung, think-gpe0/think-3ok2). Not V4/C4: two adversarial reviews by distinct reviewers plus a human oversight record are needed.
- result-import.md stage 4 says the replay "runs the source's own verification"; the same section admits independent-implementation replays in relationship_to_generator. The register next_rung texts of T-082/T-090/T-091/T-094 plan source-checker replays (146+131+26.5+162 CPU-h). Recorded as a tension for the coordinator, not resolved by this lane.

What a verified-lane move needs (frontier/README.md, epistemics.md "Integrated", think-mt6e which no checker enforces yet):
- a complete replay here (above), passing, on the pinned bytes;
- a mapped review of the mathematics under docs/project/reviews/, cited as proof.audit_record on the replay entry and in the register entry's reviews;
- controls: at least one control path on a C3 entry; result-import stage 4 asks two mutated certificates refused and a test holding them. Here: per-certificate --control receipts (99/100 scaling; near-threshold scaling to 1 - 1e-6 at the least-bound leaf centre) and a test that re-checks them;
- every derived consumer of a moved verified bound follows (case records, carries by mass to higher counts, views, citations, atlas, tests, overview, SYNOPSIS, piercing survey).

Is a review required:
- T-090, T-091: the 5 October review (separately prompted, accepted) is the review of their mathematics. T-082: the 3 October review. T-094: none, so required (think-flv5's review lane).
- Neither review saw a sqverify_fast replay (both were written for source-checker replays). One separately prompted adversarial review covering T-094's mathematics and the sqverify_fast replays of the whole batch is run by this lane.

## Progress

- 2026-10-05 18:36 e38b78165: T-094's two certificates VERIFIED by sqverify-fast at all 201 directions (n67 1,388 CPU-s / 2,122 s wall; n84 1,878 / 2,765, two threads, load 3-17); controls refused; census tool learns the 3-5 October packets, --control, --evidence; V-sqverify-fast registered; tests/test_sqverify_fast_census.py.
- 2026-10-05 18:51 review-2026-10-05-wand125-october-5-and-independent-replays.md (separate claude -p tbd-strong, claude-opus-5-5, detached worktree, removed): accepted, IR-1..IR-5 notes; route carries to T-082/T-090/T-091 per certificate (checklist in its "Carrying the Route").
- 2026-10-05 19:35 e020eb1e2 records (T-094 V3/C3; n67 -> 212/25, n84 -> 9411/1000; IR-2 amends result-import.md), eb3404c31 re-pin.
- Queue: T-091 (evening 10-04 packet) running since 18:35; n53 VERIFIED 1,352 CPU-s / 2,176 s wall.
- 2026-10-06 01:45 T-091 done: 41468f546 (12 census rows VERIFIED, 21,613 CPU-s = 6.0 CPU-h, 6.8 wall-h at two threads, load 4-15; 12 controls refused), ce4423003 (records: T-091 V3/C3; verified bound moves at 17 counts n = 53..95; route review listed on T-091, covers [T-091, T-094]), d25992c91 re-pin. test_result_status +1 (T-072 superseded at n = 76): 35 -> 36 on this branch.
- Stopped at the T-091 boundary at the owner's request (coordinator 2026-10-06 00:5x). Not started: T-090 (16 certs; priced 7.1 CPU-h, about 8.4 wall-h at two threads, by T-091's 17.6 us of CPU per source node), T-082/think-wpuu (22 certs; 8.7 CPU-h, about 10.3 wall-h). Format T leftovers (think-r7yt's T-077 rect n20/n42/n70 and think-j8f1's T-046 n51/57/58/72/73/91) are already VERIFIED in census/ since #332 (182-371 CPU-s each); they need a format-T --control mode and records only. think-3tgc's rect_n93_L973 has no packet; nothing moves at n = 93 from it (verified now 781/80). T-097 (s(66)) dropped from this lane: the coordinator does its exit on the coordinator branch with --control/--evidence.
- 2026-10-06 02:00 7c490df1b test fix (T-007 audit, n = 73 now T-091). Reachable tests on d25992c91+fix: 4985 passed, 9 failed (8 not lane C: 5 browser-floor eslint for missing typescript-eslint, 2 fixed_core known, 1 site_glyphs n11 review 12 vs 11 also at 04a0a2217; 1 mine, test_t007 n73, fixed in 7c490df1b). --records: only the known think-d135. Rust target removed.
