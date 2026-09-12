---
type: is
id: is-01m2aykekvqjdn3bn8p85g551v
title: Reap the BC329 worker group when its supervisor receives POSIX termination
kind: bug
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
  - type: blocks
    target: is-01m2b1h8cawhz8q1y1tg2d3c5d
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T13:58:37.945Z
updated_at: 2026-09-12T15:11:12.843Z
closed_at: 2026-09-12T15:11:12.843Z
close_reason: "Repair commit 1a5a8565 passed source-distinct reproduction at each stated boundary: literal Git pathspec and tracked-output overlap are fail closed; the post-Popen deadline uses recomputed remaining time and kills a late process group; real SIGTERM and launch-window SIGHUP kill and reap workers before signal redelivery. The 98-test focused suite, Ruff, BasedPyright, edit tier, and diff check passed. Adjacent findings remain separately blocked; no BC329 target ran."
resolution: null
duplicate_of: null
---
Independent target-free review of c516a592 ran supervise_worker around a pause-only child, sent SIGTERM to the supervisor, and observed supervisor exit -15 while the start_new_session worker remained alive and result.json stayed preflight-pending/pending. Install and restore appropriate SIGTERM/SIGHUP handling around the supervised lifetime, cover the launch window, terminate and reap the owned worker process group, and retain preflight-failed/supervisor-interrupted with exact exit/signal provenance. Add a real subprocess control in addition to the mocked KeyboardInterrupt test, and verify no orphan remains. Re-run focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.

## Notes

Repair committed as 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe. Temporary SIGTERM/SIGHUP handlers span handler installation, launch, wait, receipt closure, and cleanup; the launch-window path retains the new process handle before raising, terminates/reaps its session, records supervisor signal and worker exit status, restores prior handlers and mask, then re-delivers the signal. Real subprocess controls cover SIGTERM while waiting and SIGHUP between Popen return and supervisor assignment, and verify no worker remains. Validation: 98 fixed-core tests passed in 11.40 s; repository Ruff and BasedPyright reported zero findings; packing-validate --edit passed in 55.66 s. Keep open pending source-distinct review. BC329 was not registered or run.
