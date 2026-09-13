---
type: is
id: is-01m2e60sxv8kxk26am7ydbpceg
title: "PR157-INTEGRATION-01: bind calibration launch instructions to the reviewed combined source"
kind: bug
status: in_progress
priority: 2
version: 3
assignee: root
delegate: proof_review
labels: []
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-13T20:05:58.841Z
updated_at: 2026-09-13T21:14:05.123Z
---
Independent integration review compares PR157 876c5945 with the accepted PR156 run sheet committed at 9c56e901 (sheet blob 29517a3f). The sheet intentionally requires its PR156 branch/live-head equality. PR157 changes five of the 23 source-closure paths, so PR156 receipts cannot certify the combined leaf. After the owner publishes PR156 and it is integrated, retain dated PR156 reviews and add a narrowly reviewed current launch procedure binding clean HEAD to the actual local branch and live remote PR/ref. Keep reader revision equal to execution revision, sole-parent evidence commit, and staged/postcommit source-closure checks. Preserve MATH05 preflights alongside task_observer plumbing. No profiles or BC329 target are required or authorized by this handoff review.

## Notes

2026-09-13 21:12 UTC: PR156 base has now been pushed to exact 9c56e901, but its required hosted suite failed and draft remains unready (think-bpy8). PR157 remote head 876c5945 was green only against old 52e4ab65. When PR157 coordinator integrates the new base, preserve both PR156 task_observer changes and PR157 MATH05 preflight changes in the five overlapping source-closure paths; then derive a fresh combined-head launch sheet and source-distinct review. Do not treat prior PR156 receipts or old-base PR157 green checks as admission for combined leaf. No profiles or target ran.
