---
type: is
id: is-01m2b1h8cawhz8q1y1tg2d3c5d
title: Reap calibration workers on SIGTERM, SIGHUP, and launch-window interruption
kind: bug
status: in_progress
priority: 1
version: 7
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
updated_at: 2026-09-12T15:49:31.170Z
---
CAL-4 from the Astra Max source-distinct review. A real pause-only control showed SIGTERM exits the calibration supervisor with its worker alive and receipt partial with process_group_reaped false. Port the independently admitted signal, launch-window, restoration, cancellation, and process-group cleanup contract into the separate calibration supervisor, and retain real signal controls. The reviewer killed the owned test group; no BC329 target ran.

## Notes

Source-distinct review at `d924a4bf` accepted TERM/HUP launch handling and SIGINT during ordinary polling, then reproduced a remaining SIGINT launch-window orphan: interruption after Popen creates the worker but before `active_process` assignment exits the supervisor, leaves the worker alive, and incorrectly records it reaped. The reviewer killed the owned group. The next repair must protect SIGINT across launch, retain signal provenance, restore prior state, and keep a real-process regression. Review: `/private/tmp/bc329-calibration-integrated-correction-review.md`. No scientific target ran.
