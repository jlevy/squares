---
type: is
id: is-01m2aykekvqjdn3bn8p85g551v
title: Reap the BC329 worker group when its supervisor receives POSIX termination
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T13:58:37.945Z
updated_at: 2026-09-12T14:06:29.738Z
---
Independent target-free review of c516a592 ran supervise_worker around a pause-only child, sent SIGTERM to the supervisor, and observed supervisor exit -15 while the start_new_session worker remained alive and result.json stayed preflight-pending/pending. Install and restore appropriate SIGTERM/SIGHUP handling around the supervised lifetime, cover the launch window, terminate and reap the owned worker process group, and retain preflight-failed/supervisor-interrupted with exact exit/signal provenance. Add a real subprocess control in addition to the mocked KeyboardInterrupt test, and verify no orphan remains. Re-run focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.
