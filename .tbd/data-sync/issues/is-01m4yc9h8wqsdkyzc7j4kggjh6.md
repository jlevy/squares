---
type: is
id: is-01m4yc9h8wqsdkyzc7j4kggjh6
title: Keep module fixtures together in reachable xdist runs
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:34:50.895Z
updated_at: 2026-10-14T23:40:45.121Z
started_at: 2026-10-14T23:40:45.121Z
---
Current broad prepush exposes a pre-existing main9b behavior: reachable_tests.py pytest_command uses -n10 with default load scheduling, while canonical quick shards use loadfile. Case-level distribution can repeat large module-scoped publication/atlas fixtures across workers. Inspect actual fixture construction counts and preserve every selected identity, normal/pool complement, native crash/requeue and deadlines. Prefer supported native loadfile distribution rather than a custom scheduler or shared transport; prove colocation with real workers and exact fixture-count/identity controls before any speed claim. Main9b and reviewed08d already contain this shape, so it is not introduced by PR599 and should follow current stabilization. Final prepush logs at7b802 record broad normal phase over400s; no attribution of that entire interval to this mechanism without measurement.
