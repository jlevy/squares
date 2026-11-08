---
type: is
id: is-01m6ykfj03kfqvmdxfgrx6fz2q
title: "Checker gap: verified_lane_review_problems accepts any mapped review named by a deciding evidence entry's proof.audit_record"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-11-08T22:11:51.939Z
updated_at: 2026-11-08T22:11:51.939Z
---
Found by L57 during #924 intake (PR #925). verified_lane_review_problems accepts any mapped review that a deciding evidence entry names in proof.audit_record. The native parent-core evidence entry names the 2026-09-22 review of the native route itself, so a verified lane could move with no review of the specific certificate. It passed for T-274 only because the real stage-4 review exists. Fix: require the review to be of the result (certificate) being promoted, not of the method.
