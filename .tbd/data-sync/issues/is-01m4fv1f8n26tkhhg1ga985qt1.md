---
type: is
id: is-01m4fv1f8n26tkhhg1ga985qt1
title: Investigate the empty slow-lane validation control failure
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T08:03:58.867Z
updated_at: 2026-10-09T08:27:05.344Z
started_at: 2026-10-09T08:05:02.568Z
---
The complete frozen bbd7c301 pre-push run records tests/test_validation_cli.py::test_slow_lane_distinguishes_worker_collection_failure_from_empty_selection[empty] failing in worker gw4; the full run is still active and its final traceback is not yet available. Preserve source while the suite completes. A strong agent reads existing test/runtime/child evidence and may prepare an external patch only. Diagnose the actual refusal, collection and deadline path before changing a test or runtime; do not extend production deadlines or weaken the serial empty-selection-versus-worker-failure distinction. Root owns application after gate drain, independent review, focused checks, final rebinding and a complete gate.

## Notes

Completed bbd7 full gate confirms the first real nested pytest -n2 command timed out at unchanged30s with only bringing-up-nodes output; serial proof was never entered. Both controls passed at be0. Root and senior accepted the narrow existing exclusive allocation classification based on actual internal workers, preserving both cases, all assertions/deadlines and exact-once quick/slow coverage. Web owns CLI marker plus truthful conftest/development wording; native singleton short-deadline subprocess controls are described explicitly. Source application/focused checks/full rerun pending; this does not prove contention caused the earlier failure.
