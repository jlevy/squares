---
type: is
id: is-01m2b4yfx3th5wcdaw9apr0vn5
title: Source-distinct rereview and admission of the second calibration correction
kind: task
status: closed
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Astra Max source-distinct review; root integration
labels:
  - n11
  - calibration
  - review
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T15:49:31.170Z
updated_at: 2026-09-13T07:21:28.688Z
closed_at: 2026-09-13T07:21:28.688Z
close_reason: CAL-5 is independently accepted at exact implementation head fcb538c29b846fb5e7c33bd962772ada9c21aedd. Source-distinct Astra Max review replayed 54 signal/staging/adoption/deadline controls, 10 fixture/source/readback controls, four real launch controls, and all prior CAL-1 through CAL-7 evidence; 192 tests passed with zero Ruff or BasedPyright findings. Acceptance is retained at calibration commit cd02a0cd. No positive profile or BC329 target ran.
resolution: null
duplicate_of: null
---
After the five remaining CAL-2 through CAL-6 defects and Ruff formatting drift are repaired, independently replay the complete dilation-builder comparison, partial dilation readback, SIGINT launch-window lifecycle control, final-publication deadline controls, and positive RSS evidence contract on the exact combined revision. Recheck the n=2 fixture and all prior admitted preflight behaviors, run focused Python 3.14 gates and the edit tier, retain an accept/refuse report, and do not run a positive full-shape profile or BC329 target. Acceptance is required before calibration profiles.

## Notes

Exact review target is calibration branch fcb538c2 (code repair 85d3f529). The prior 967f7cd review remains REFUSE and is retained at /private/tmp/bc329-calibration-967f7cd-final-review.md. New author controls: 192 combined tests in 25.44s; Ruff and BasedPyright zero; edit tier 45/74 passed. Independently replay cross-thread TERM/HUP/INT at both stages, fdopen adoption failures, prior CAL1-7 evidence, and exact fixture without running a profile or BC329.
