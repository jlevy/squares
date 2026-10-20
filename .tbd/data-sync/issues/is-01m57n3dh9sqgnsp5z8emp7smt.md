---
type: is
id: is-01m57n3dh9sqgnsp5z8emp7smt
title: Make resident-Rust shutdown timeout control independent of startup timing
kind: bug
status: in_progress
priority: 2
version: 3
delegate: codex@spud10.local
labels:
  - validation
dependencies: []
parent_id: is-01m578snhcmb9xf25bnb3atvy8
hold: null
hold_until: null
created_at: 2026-10-18T14:01:57.544Z
updated_at: 2026-10-18T14:13:43.345Z
started_at: 2026-10-18T14:02:06.675Z
---
At clean #676 head611b45437, the full push gate passed66/67 selected steps but test_rust_rectangle_geometry::test_shutdown_timeout_cannot_promote_completed_angles received zero completed angles instead of one. Its0.5second budget includes fake-process startup, so it can exercise startup timeout rather than the intended shutdown timeout. The unchanged isolated test passes. Preserve the fail-closed INCONCLUSIVE/backend_timeout behavior and the completed VERIFIED-angle assertions; make startup and angle progress independent of the shutdown deadline, then force a bounded real shutdown wait. Scope only the test and its helper, disclose the repair in #676, and require focused controls plus a green final-head push before publication. No production verifier change or scientific replay.

## Notes

Reviewed repair committed 3fc464c0ece40a42f5ba76d813e5508e9c0b3340; the two report phase-inference sentences are calibrated by ddebf00520532d1cd5f9fe45cbeb328732ba5fd1. Scope is one existing test and append-only disclosure in the two dated reviews. A test-only subclass advances a controlled clock only on entering the real shutdown method, leaving 0.05s for its real select wait; startup/angle accounting is held fixed with individually bounded protocol waits. Existing INCONCLUSIVE/backend_timeout/one VERIFIED-angle assertions remain, and actual worker termination is asserted. No production verifier/deadline change. All seven focused resident-Rust boundary tests pass in 2.63s; Ruff, formatting and BasedPyright pass, documentation covers2065 files, normal hooks pass3.02s and1.55s. Predecessor611b45437's push failed1/67 selected steps in1219.13s; zero completed angles are consistent with pre-angle expiry but no exact timeout phase was traced. The unchanged isolated test passed0.59s. Durable evidence: push-611b45437-failure-evidence.json, reachable-611b45437.log and shutdown-control-repair-focused2.log in /Volumes/spud-ext1/agent-source/squares-intake-20261018-evidence/. Root reviewed the test repair without blocker. Current clean ddebf0052 still requires records then push qualification after665's broad CPU slot, followed by remote draft update and terminal hosted checks. Keep open until qualified publication; remote676 remains5fb743b3e.
