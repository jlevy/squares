---
type: is
id: is-01m50ye7bh333b791fv1cks4gk
title: "PR #616 A5 (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252): continuous_pose_followup premises pipeline has no end-to-end test; a malformed log raises StopIteration"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: ecstatic-edison-address-627
labels: []
dependencies: []
parent_id: is-01m50yc0efcxyyh72mesjv7t15
hold: null
hold_until: null
created_at: 2026-10-15T23:30:27.824Z
updated_at: 2026-10-15T23:30:52.356Z
started_at: 2026-10-15T23:30:52.356Z
---
Nit. #616 review A (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252), carried by PR #627 B1. packing/devtools/continuous_pose_followup.py crate_log_checks bare next(); main catches only AuditError, KeyError, ValueError. Fix: require() lookups; a synthetic-asset premises test.
