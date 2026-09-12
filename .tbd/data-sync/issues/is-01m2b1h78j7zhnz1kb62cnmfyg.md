---
type: is
id: is-01m2b1h78j7zhnz1kb62cnmfyg
title: Require complete known-answer routes in calibration terminal readback
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation or source-distinct review; root integration
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:50.609Z
updated_at: 2026-09-12T14:52:23.404Z
---
CAL-1 from the Astra Max source-distinct review. The default calibration load_result accepts status complete and calibration-passed with zero completed raw directions, null raw minimum and normalization, null routes, and only matching file counts. Make every successful terminal record require complete raw coverage, the exact normalized candidate, complete exact, interval, and dilation routes, and independent known-answer reconstruction. Reject phase-inconsistent artifacts and retain the fabricated-terminal negative control. This blocks calibration admission and every profile; it does not concern BC329 scientific coverage.
