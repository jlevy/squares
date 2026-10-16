---
type: is
id: is-01m4yrp92rttnxj4sfeh8b3h2g
title: "Register cases 76 and 95 in the mixed-cover tools, then record the zmx2 + zm_mixed reproductions of T-184 and #610 as evidence"
kind: task
status: in_progress
priority: 2
version: 11
delegate: user-eb-records-76-95
labels: []
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-15T03:11:31.416Z
updated_at: 2026-10-16T11:38:46.555Z
started_at: 2026-10-16T05:25:32.902Z
---
The C3 route for T-184 (#594, s(76)=9) and #610 (s(95)=10) needs the full reproductions (zmx2 D4 sweep over 10,000 roots plus all zm_mixed.py sub-roots, already run and retained in packets bengreff-s76-certificate-* and bengreff-s95-certificate-2026-10-15 on intake-610 @ 7c65c191b) recorded as evidence entries. That first needs cases 76 and 95 registered in the two mixed-cover tools (zmx2, zm_mixed). Then a stage 4 review with no blocking defect raises the rungs. Optional: zmx2 --full (think-eucc, ~6 CPU-h), as T-066's s(59) replay ran. Found by the #610 lane on 2026-10-15.

## Notes

2026-10-16T05:40Z user-eb-records-76-95 (lane E): started on branch claude/intake-2026-10-16-records-76-95 from origin/main e2e018f32. Plan: (1) register 76/95 in replay_evand_zmx2 and audit_evand_mixed_covers with a zmx2+zm_mixed split-composite judge and tests; (2) targeted zm_mixed.py controls on mutated covers (packets lack them); (3) evidence entries, verifiers rows, coverage entries, uncited until lane F's review; (4) draft PR. No rung change before lane F's verdict.

2026-10-16T06:12Z lane E checkpoint: tool slice committed and pushed at 5575ad2bf (claude/intake-2026-10-16-records-76-95): replay_evand_zmx2 cases 76/95 (+ source --uncert-cap for run) and their retained controls; audit_evand_mixed_covers split cases, composite judge, compare-sub-roots, check covers both packets (clean: 8096+64 sub-roots for 76, 9981+304 for 95; replay equals source root for root). Tests in test_audit_evand_mixed_covers, test_replay_controls (+ zm_mixed.py pose receipts held), test_replay_tools. Priced zm_mixed.py cert refusals of the two retained mutations: not affordable (depth 24 > 5 CPU-min and depth 12 > 10 CPU-min on one cell, both stopped); ~15 CPU-min spent. Next: evidence entries, verifiers rows, coverage entries (uncited until lane F).

2026-10-16T06:58Z lane E checkpoint: evidence commit fcfcb0443 (E-bengreff-594-cover-replay, E-bengreff-610-cover-replay; verifiers rows; coverage rows; T-184/T-191 cite them with V0/C0 held by composition until lane F's review, activity + unfinished item link think-l8wi; case adoption deferred in certificate-citation-deferrals.yaml under think-ccjt, blocked on think-l8wi; papers no-public-change record, renders byte-identical), re-pin cf408163a, URL amendments 0f2c667c1. Head pushed. Next: draft PR; site edition cut (v0.7.15, collides with #644 and review-185-190 branch) as the last commit after lane F's verdict or at 12:00Z.

2026-10-16T06:52Z lane E: draft PR #649 (https://github.com/jlevy/squares/pull/649) opened at 0f2c667c1, labels intake + S2. Waiting on lane F's verdict for the final commit; site cut last.

2026-10-16T07:10Z lane E: hosted CI at 0f2c667c1 is green except 'synopsis agrees with the artifacts' (site release impact: the edition is not cut). The v0.7.15 site cut (devtools.cut_release, dry run clean) was refused by this session's permission classifier as a production deploy; it needs the owner's permission or the owner's cut. v0.7.15 is also taken by #644 and the review-185-190 branch. Holding for lane F's verdict.

2026-10-16T08:20Z lane E: merged #652 (lane F's review, 7ae52624, with its v0.7.15 site cut) at 52f4e8410; mapped the review (external_review on both report entries, reviews on T-184/T-191, audit_record on the replays); check_results derives V3/C3 and the register declares it (T-184 and T-191 V0/C0 -> V3/C3, S3 confirmed); F8's owed zm_mixed.py controls (1 more for s(76), 2 for s(95); the review's depth-12 pair now held by a test) are in next_rung, limitations and the case-adoption deferrals, since unfinished_confirmations refuse an item at or below C3; case adoption deferred on the owner's answer to F8. Records tier passes (322 s). Head bc92041ea pushed; PR #649 description updated, label S2 -> S3.

2026-10-16T11:20Z lane E: #649 Review A addressed at d296e9f11 (merged #652 a4d48feb7; A1 header-hash and settings binding with fault controls; A2 rungs held at V3/C1 with the owed zm_mixed.py controls as unfinished C3 items and owner question 16 of think-l3oo; A3-A8 fixed). Disposition reply posted (review 5546888955). Records tier passes; label S2. Waiting on hosted CI.

2026-10-16T11:15Z lane E: hosted CI green at d296e9f11 (31 success, 40 skipped, 0 failed). #649 ready for the coordinator; rungs held at V3/C1 pending zm_mixed.py controls (owner question 16, think-l3oo).

2026-10-16 ~11:50Z coordinator user-eb: PR #649 MERGE-READY at 33fde412f pending hosted CI on that head (tests-only change after the green d296e9f11): senior+correctness Review A (0/2/2/4) and follow-up Review B (0/0/0/2) addressed; B2 is owner question 25 in think-l3oo. T-184 and T-191 at V3/C1, C3 held for zm_mixed.py controls (question 16). Carries #652 (merge-ready) and its site v0.7.15 cut.
