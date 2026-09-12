---
type: is
id: is-01m2b1h805emc13mx1cykp5s5x
title: Verify exact partial interval and dilation sets in calibration readback
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:51.364Z
updated_at: 2026-09-12T14:50:20.233Z
---
CAL-3 from the Astra Max source-distinct review. The calibration schema records completed_directions for partial interval and dilation routes but its delegated base readers accept same-count substitutions that do not match retained row files. Integrate the exact-set repair owned by think-yiay, require the last row to belong to the published set, distinguish later unpublished tails, and retain substitution and deletion controls through the calibration reader. This blocks calibration admission and does not imply a scientific result.
