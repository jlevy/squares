---
type: is
id: is-01m2e60sxv8kxk26am7ydbpceg
title: "PR157-INTEGRATION-01: bind calibration launch instructions to the reviewed combined source"
kind: bug
status: in_progress
priority: 2
version: 2
assignee: root
delegate: proof_review
labels: []
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-13T20:05:58.841Z
updated_at: 2026-09-13T20:08:29.884Z
---
Independent integration review compares PR157 876c5945 with the accepted PR156 run sheet committed at 9c56e901 (sheet blob 29517a3f). The sheet intentionally requires its PR156 branch/live-head equality. PR157 changes five of the 23 source-closure paths, so PR156 receipts cannot certify the combined leaf. After the owner publishes PR156 and it is integrated, retain dated PR156 reviews and add a narrowly reviewed current launch procedure binding clean HEAD to the actual local branch and live remote PR/ref. Keep reader revision equal to execution revision, sole-parent evidence commit, and staged/postcommit source-closure checks. Preserve MATH05 preflights alongside task_observer plumbing. No profiles or BC329 target are required or authorized by this handoff review.

## Notes

Published PR157-INTEGRATION-01 as issuecomment-5655786544 before delegated repair. Proof lane prepares a narrow ignored patch to the existing run sheet for the actual PR157 execution worktree/branch/live head; root applies only after the PR156 owner publishes and integration lands. A separate publication lane must rereview the merged literal procedure. Preserve PR156 dated acceptance and strict source closure. No calibration execution.
