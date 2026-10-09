---
type: is
id: is-01m4fv1f8n26tkhhg1ga985qt1
title: Investigate the empty slow-lane validation control failure
kind: bug
status: in_progress
priority: 1
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T08:03:58.867Z
updated_at: 2026-10-09T09:41:33.177Z
started_at: 2026-10-09T08:05:02.568Z
---
The complete frozen bbd7c301 pre-push run records tests/test_validation_cli.py::test_slow_lane_distinguishes_worker_collection_failure_from_empty_selection[empty] failing in worker gw4; the full run is still active and its final traceback is not yet available. Preserve source while the suite completes. A strong agent reads existing test/runtime/child evidence and may prepare an external patch only. Diagnose the actual refusal, collection and deadline path before changing a test or runtime; do not extend production deadlines or weaken the serial empty-selection-versus-worker-failure distinction. Root owns application after gate drain, independent review, focused checks, final rebinding and a complete gate.

## Notes

Committed98ccc9ad29 applies the narrowly reviewed test-only custody fix: each actual nested command receives its own public --basetemp under tmp_path/child-pytest/run-0 orrun-1. Original two-command/refusal/fallback assertions, plugins, two real workers and30s bounds are unchanged. Twelve focused cases pass11.28s with clean lint/format/types; actual patched empty control and separate serial collection pass in0.732s, zero global numbered cleanup and unchanged shared entries. Independent root AST fence/senior lifecycle review are clear. The inherited cleanup mechanism is demonstrated, but historical df timeout cause remains unproved. New98 full pre-push is active with normal retention/default allocation;64prechecks and full normal phase14089passes/55combinedskip-xfail rows are green, final serial/overall/hosted results pending. Exact df failed receipts/fixture/history remain preserved.
