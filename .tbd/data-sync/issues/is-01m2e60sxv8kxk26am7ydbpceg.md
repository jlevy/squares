---
type: is
id: is-01m2e60sxv8kxk26am7ydbpceg
title: "PR157-INTEGRATION-01: bind calibration launch instructions to the reviewed combined source"
kind: bug
status: in_progress
priority: 2
version: 5
assignee: root
delegate: proof_review
labels: []
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-13T20:05:58.841Z
updated_at: 2026-09-13T21:51:30.442Z
---
Independent integration review compares PR157 876c5945 with the accepted PR156 run sheet committed at 9c56e901 (sheet blob 29517a3f). The sheet intentionally requires its PR156 branch/live-head equality. PR157 changes five of the 23 source-closure paths, so PR156 receipts cannot certify the combined leaf. After the owner publishes PR156 and it is integrated, retain dated PR156 reviews and add a narrowly reviewed current launch procedure binding clean HEAD to the actual local branch and live remote PR/ref. Keep reader revision equal to execution revision, sole-parent evidence commit, and staged/postcommit source-closure checks. Preserve MATH05 preflights alongside task_observer plumbing. No profiles or BC329 target are required or authorized by this handoff review.

## Notes

2026-09-13 21:12 UTC: PR156 base has now been pushed to exact 9c56e901, but its required hosted suite failed and draft remains unready (think-bpy8). PR157 remote head 876c5945 was green only against old 52e4ab65. When PR157 coordinator integrates the new base, preserve both PR156 task_observer changes and PR157 MATH05 preflight changes in the five overlapping source-closure paths; then derive a fresh combined-head launch sheet and source-distinct review. Do not treat prior PR156 receipts or old-base PR157 green checks as admission for combined leaf. No profiles or target ran.

2026-09-13 21:50 UTC live reconciliation: PR157 head d819d564e72d2a030dcf64d45e9d73b5b8800c4e remains non-draft and its required suite and packing-required checks fail. Exact hosted job 103795888086 in run 34783944929 reports only elapsed-time budget failure: fast behavioral tests 305.8s against 275s ceiling and recorded 183.44s reference (1.67x versus 1.5x limit). The same two calibration-reader nodes are over the 12s individual limit (26.53s and 18.08s). This is consistent with PR156 think-bpy8, but the combined d819 head still needs a fresh exact-head gate after the base fix; no assertion failure reported in this step. Other current checks pass. PR157 still bases on old 52e4ab65 and cannot inherit PR156 9c run-sheet admission.
