---
type: is
id: is-01m2nf99em5gccxeaeynqzapm5
title: Require successful packing-required before reusing a PR-verified tree
kind: bug
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:02:35.091Z
updated_at: 2026-09-17T02:06:21.848Z
---
PR #185 review: packing/devtools/verified_merge_tree.py accepts workflow-level conclusion=success, but GitHub workflows can succeed with required jobs skipped. Before a post-merge run omits fast checks, query the candidate run's jobs and require an explicit completed successful packing-required aggregator; refuse missing, skipped, cancelled, failed, or API-unreadable states. Add negative controls for each refusal.

## Notes

2026-09-16 evidence audit at da2259fb: SATISFIED (verified_merge_tree.py:105-118, 154-162; tests at test_verified_merge_tree.py:109,121; commit 4b2f1904). A cancelled packing-required case was untested; it is being added on #188. Close after green exact-head hosted CI.
