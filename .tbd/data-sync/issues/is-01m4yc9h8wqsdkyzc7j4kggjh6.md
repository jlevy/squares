---
type: is
id: is-01m4yc9h8wqsdkyzc7j4kggjh6
title: Keep module fixtures together in reachable xdist runs
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:34:50.895Z
updated_at: 2026-10-15T10:41:11.054Z
started_at: 2026-10-14T23:40:45.121Z
---
Current broad prepush exposes a pre-existing main9b behavior: reachable_tests.py pytest_command uses -n10 with default load scheduling, while canonical quick shards use loadfile. Case-level distribution can repeat large module-scoped publication/atlas fixtures across workers. Inspect actual fixture construction counts and preserve every selected identity, normal/pool complement, native crash/requeue and deadlines. Prefer supported native loadfile distribution rather than a custom scheduler or shared transport; prove colocation with real workers and exact fixture-count/identity controls before any speed claim. Main9b and reviewed08d already contain this shape, so it is not introduced by PR599 and should follow current stabilization. Final prepush logs at7b802 record broad normal phase over400s; no attribution of that entire interval to this mechanism without measurement.

## Notes

Committed in the independently reviewed quick-push slice at 934c68019. Supported native --dist=loadfile preserves eight exact test identities and case writes while the retained real two-worker experiment builds the module fixture once instead of twice. Explicit child basetemps preserve parent fixtures and native scheduler failure/requeue behavior. Full runner/progress module has 164 passes; selected CLI has 44 passes. No unmeasured total-runtime speedup claim. Persistent logs/JUnit are in primary .codex/regularization-closeout-evidence-2026-10-13/quick-push-validation/. Merge/deployment remain pending with gg64; do not close on local implementation alone.
