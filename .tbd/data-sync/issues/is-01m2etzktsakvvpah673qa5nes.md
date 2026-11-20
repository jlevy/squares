---
type: is
id: is-01m2etzktsakvvpah673qa5nes
title: Diagnose slow-lane collection self-test timeout under concurrent validation
kind: bug
status: open
priority: 2
version: 5
spec_path: docs/project/specs/archive/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - validation
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-09-14T02:12:19.926Z
updated_at: 2026-11-18T07:21:45.439Z
---
On clean X032 head 646bb66a, unsandboxed pre-push with --jobs 1 --inner-jobs 1 selected 47 test files and ran pytest -n 10 while H162 exhaustive exact gate was active. One existing tests/test_validation_cli.py::test_slow_lane_distinguishes_worker_collection_failure_from_empty_selection[empty] timed out its nested slow-lane subprocess after 30 s; 1,368 other reachable tests passed. Earlier sandboxed pre-push had four OS-permission failures, separate from this timing failure. Re-run after host contention clears or with a calibrated smaller test-worker shape, then determine whether a test/gate change is needed. No X032 research claim is implicated; do not call the required pre-push gate green until resolved.

## Notes

2026-11-18 coord-intake-1117r: main's post-merge slow-lane run for #1016 (2980557a2) timed out: run 44216081708, reported by #1026's Review A. Not caused by #1026. Recorded here as a fresh occurrence; it has not been diagnosed.

2026-11-18 coord-intake-1117r: another occurrence. Main's post-merge slow-lane timed out after 1800 s at 86284ec20 (#1023), as reported by lane r1021b. Before it, 44216081708 at #1016. Not diagnosed.
