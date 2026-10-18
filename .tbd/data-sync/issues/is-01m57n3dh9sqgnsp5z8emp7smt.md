---
type: is
id: is-01m57n3dh9sqgnsp5z8emp7smt
title: Make resident-Rust shutdown timeout control independent of startup timing
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10.local
labels:
  - validation
dependencies: []
parent_id: is-01m578snhcmb9xf25bnb3atvy8
hold: null
hold_until: null
created_at: 2026-10-18T14:01:57.544Z
updated_at: 2026-10-18T14:02:06.676Z
started_at: 2026-10-18T14:02:06.675Z
---
At clean #676 head611b45437, the full push gate passed66/67 selected steps but test_rust_rectangle_geometry::test_shutdown_timeout_cannot_promote_completed_angles received zero completed angles instead of one. Its0.5second budget includes fake-process startup, so it can exercise startup timeout rather than the intended shutdown timeout. The unchanged isolated test passes. Preserve the fail-closed INCONCLUSIVE/backend_timeout behavior and the completed VERIFIED-angle assertions; make startup and angle progress independent of the shutdown deadline, then force a bounded real shutdown wait. Scope only the test and its helper, disclose the repair in #676, and require focused controls plus a green final-head push before publication. No production verifier change or scientific replay.
