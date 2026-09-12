---
type: is
id: is-01m2b4yfx3th5wcdaw9apr0vn5
title: Source-distinct rereview and admission of the second calibration correction
kind: task
status: in_progress
priority: 1
version: 4
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
updated_at: 2026-09-12T16:21:52.555Z
---
After the five remaining CAL-2 through CAL-6 defects and Ruff formatting drift are repaired, independently replay the complete dilation-builder comparison, partial dilation readback, SIGINT launch-window lifecycle control, final-publication deadline controls, and positive RSS evidence contract on the exact combined revision. Recheck the n=2 fixture and all prior admitted preflight behaviors, run focused Python 3.14 gates and the edit tier, retain an accept/refuse report, and do not run a positive full-shape profile or BC329 target. Acceptance is required before calibration profiles.

## Notes

Source-distinct rereview at b6260970 passes CAL-2, CAL-3, CAL-4, and CAL-6 and reproduces their regression sensitivity. It refuses final admission on a remaining CAL-5 SIGINT window inside tempfile.mkstemp that can leave an open descriptor and unexpected staging file, making the partial directory unreadable. The exact report is being finalized. No positive full-shape profile or BC329 target ran.
