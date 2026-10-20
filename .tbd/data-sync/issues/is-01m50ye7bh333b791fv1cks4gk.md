---
type: is
id: is-01m50ye7bh333b791fv1cks4gk
title: "PR #616 A5 (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252): continuous_pose_followup premises pipeline has no end-to-end test; a malformed log raises StopIteration"
kind: bug
status: open
priority: 2
version: 3
delegate: ecstatic-edison-address-627
labels: []
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
hold: null
hold_until: null
created_at: 2026-10-15T23:30:27.824Z
updated_at: 2026-10-15T23:58:23.995Z
started_at: 2026-10-15T23:30:52.356Z
---
Nit. #616 review A (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252), carried by PR #627 B1. packing/devtools/continuous_pose_followup.py crate_log_checks bare next(); main catches only AuditError, KeyError, ValueError. Fix: require() lookups; a synthetic-asset premises test.

## Notes

Deferred in part from #616's review A (A5), carried by PR #627 B1. The StopIteration half is fixed in 879690b4c on PR #627 (log_row raises AuditError; test_crate_log_checks_refuse_a_log_missing_a_row fails before, passes after). Still open: an end-to-end test of continuous_pose_followup premises() and main(['premises', ...]) on a synthetic asset, one that holds and one refusal such as an unscaled control, as test_fine_net_followup.py:198 does for the sibling tool. Waits on a synthetic-asset builder for the n28 bundle layout (candidate, control, check1 logs and crate archive with its build.rs source digest, check2 manifests and receipts).
