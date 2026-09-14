---
type: is
id: is-01m2etzktsakvvpah673qa5nes
title: Diagnose slow-lane collection self-test timeout under concurrent validation
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - validation
dependencies: []
parent_id: is-01m2eddtqbpv11d9g5yk0s8cv0
created_at: 2026-09-14T02:12:19.926Z
updated_at: 2026-09-14T02:12:19.926Z
---
On clean X032 head 646bb66a, unsandboxed pre-push with --jobs 1 --inner-jobs 1 selected 47 test files and ran pytest -n 10 while H162 exhaustive exact gate was active. One existing tests/test_validation_cli.py::test_slow_lane_distinguishes_worker_collection_failure_from_empty_selection[empty] timed out its nested slow-lane subprocess after 30 s; 1,368 other reachable tests passed. Earlier sandboxed pre-push had four OS-permission failures, separate from this timing failure. Re-run after host contention clears or with a calibrated smaller test-worker shape, then determine whether a test/gate change is needed. No X032 research claim is implicated; do not call the required pre-push gate green until resolved.
