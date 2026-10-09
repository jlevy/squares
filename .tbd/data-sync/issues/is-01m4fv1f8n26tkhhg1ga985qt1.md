---
type: is
id: is-01m4fv1f8n26tkhhg1ga985qt1
title: Investigate the empty slow-lane validation control failure
kind: bug
status: in_progress
priority: 1
version: 6
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T08:03:58.867Z
updated_at: 2026-10-09T10:05:05.212Z
started_at: 2026-10-09T08:05:02.568Z
---
The complete frozen bbd7c301 pre-push run records tests/test_validation_cli.py::test_slow_lane_distinguishes_worker_collection_failure_from_empty_selection[empty] failing in worker gw4; the full run is still active and its final traceback is not yet available. Preserve source while the suite completes. A strong agent reads existing test/runtime/child evidence and may prepare an external patch only. Diagnose the actual refusal, collection and deadline path before changing a test or runtime; do not extend production deadlines or weaken the serial empty-selection-versus-worker-failure distinction. Root owns application after gate drain, independent review, focused checks, final rebinding and a complete gate.

## Notes

The test-only private nested-pytest basetemp correction is committed in 98ccc9ad29. Twelve focused cases and static floors pass; the actual patched empty selection and serial collection finish in 0.732 seconds without global numbered cleanup. The complete 98 gate passed both real CLI controls, including the originally failing empty-selection case. Its overall verdict was failed because a different native partial-response control did not finish initialization. Historical cleanup behavior is demonstrated, but the exact earlier host timeout cause remains unproved. Final 1a7e4744c1 full pre-push and hosted verification remain pending; all original CLI assertions, two real workers, plugins and 30-second limits remain.
