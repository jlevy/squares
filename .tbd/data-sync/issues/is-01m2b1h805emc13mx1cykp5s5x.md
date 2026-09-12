---
type: is
id: is-01m2b1h805emc13mx1cykp5s5x
title: Verify exact partial interval and dilation sets in calibration readback
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation or source-distinct review; root integration
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:51.364Z
updated_at: 2026-09-12T15:25:33.228Z
---
CAL-3 from the Astra Max source-distinct review. The calibration schema records completed_directions for partial interval and dilation routes but its delegated base readers accept same-count substitutions that do not match retained row files. Integrate the exact-set repair owned by think-yiay, require the last row to belong to the published set, distinguish later unpublished tails, and retain substitution and deletion controls through the calibration reader. This blocks calibration admission and does not imply a scientific result.

## Notes

Repair integrated from ecce6dba0084d80e08d9eece2a37b19c1fe5e9ed as 8d21f58a and exercised on combined head d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014. Partial interval and dilation reconstruction now requires the exact named published file set, requires the last row to belong to it, and permits only an explicitly ignored valid unpublished tail. Maintained same-count substitution, deletion, label, and tail controls pass in the 170-test target-free suite. Leave open for source-distinct closure review.
