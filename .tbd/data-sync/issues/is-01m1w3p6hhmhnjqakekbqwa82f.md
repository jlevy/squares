---
type: is
id: is-01m1w3p6hhmhnjqakekbqwa82f
title: Provide retained Git history to deferred review checks
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:38:54.384Z
updated_at: 2026-09-06T20:01:24.496Z
---
The new slow Trump review reads exact retained theorem and archive bytes with git show. Both commits and paths exist, but the deferred workflow still uses a shallow checkout. PR98 run 34054616340 fails on the missing historical object; main integration fetches full history and passes. Provide fetch-depth: 0 for the deferred job and test this prerequisite without changing retained source bindings.

## Notes

Fixed in fc72f05e and integrated in b3b7275f. A depth-one clone reproduced Git status 128; fetching history restored the exact historical bytes. The complete retained-review module passed six tests in 33.72s, including the 128-branch audit. The workflow contract and ordinary CI 34056428243 passed. Final full checkpoint 34056585319 is pending.
