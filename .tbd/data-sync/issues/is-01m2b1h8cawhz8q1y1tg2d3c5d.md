---
type: is
id: is-01m2b1h8cawhz8q1y1tg2d3c5d
title: Reap calibration workers on SIGTERM, SIGHUP, and launch-window interruption
kind: bug
status: in_progress
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation or source-distinct review; root integration
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
  - type: blocks
    target: is-01m2b4yfx3th5wcdaw9apr0vn5
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:51.753Z
updated_at: 2026-09-12T16:09:01.559Z
---
CAL-4 from the Astra Max source-distinct review. A real pause-only control showed SIGTERM exits the calibration supervisor with its worker alive and receipt partial with process_group_reaped false. Port the independently admitted signal, launch-window, restoration, cancellation, and process-group cleanup contract into the separate calibration supervisor, and retain real signal controls. The reviewer killed the owned test group; no BC329 target ran.

## Notes

Implementation correction is retained at 229b3fc2d3e5056c67b7dbe0224a399e524537c3. SIGINT now shares the launch-window deferral used by TERM and HUP. The real subprocess control delivers SIGINT after child creation but before Popen returns, verifies worker disappearance, records signal provenance and truthful reaping, and proves the prior handler was restored and invoked on redelivery. Author validation: combined suites 177 passed in 17.79s; repository-wide Ruff and BasedPyright clean; edit tier passed in 61.84s. No full profile or BC329 target ran. Leave open for source-distinct re-review.
