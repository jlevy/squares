---
type: is
id: is-01m6ykfj03kfqvmdxfgrx6fz2q
title: "Checker gap: verified_lane_review_problems accepts any mapped review named by a deciding evidence entry's proof.audit_record"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-11-08T22:11:51.939Z
updated_at: 2026-11-08T22:23:51.722Z
---
Found by L57 during #924 intake (PR #925). verified_lane_review_problems accepts any mapped review that a deciding evidence entry names in proof.audit_record. The native parent-core evidence entry names the 2026-09-22 review of the native route itself, so a verified lane could move with no review of the specific certificate. It passed for T-274 only because the real stage-4 review exists. Fix: require the review to be of the result (certificate) being promoted, not of the method.

## Notes

Senior review of #925 (N1) confirmed: with the stage-4 review removed from T-274's reviews, the review-sweep audit_record and external_review, verified_lane_review_problems still passes on the native entry's audit_record alone (review-2026-09-22-native-n11-parent-core.md, evidence.yaml ~18495); removing that too makes it fail. Same hole covers T-049, T-078, T-079, T-095. Logic at devtools/check_results.py:1690-1712. Suggested fix: count an audit_record only if the review is not older than the source, or only if a register entry for that n lists the review.
