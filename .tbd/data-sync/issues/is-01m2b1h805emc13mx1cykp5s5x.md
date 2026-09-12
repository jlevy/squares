---
type: is
id: is-01m2b1h805emc13mx1cykp5s5x
title: Verify exact partial interval and dilation sets in calibration readback
kind: bug
status: in_progress
priority: 1
version: 9
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
created_at: 2026-09-12T14:49:51.364Z
updated_at: 2026-09-12T16:14:13.334Z
---
CAL-3 from the Astra Max source-distinct review. The calibration schema records completed_directions for partial interval and dilation routes but its delegated base readers accept same-count substitutions that do not match retained row files. Integrate the exact-set repair owned by think-yiay, require the last row to belong to the published set, distinguish later unpublished tails, and retain substitution and deletion controls through the calibration reader. This blocks calibration admission and does not imply a scientific result.

## Notes

Implementation correction is retained at 0533ebaeb90cf42acf20e0029535356282a5624c. Calibration dilation receipts now use string direction labels through progress publication, closed schema, complete comparison, and the common reader. A real positive partial readback and substitution, deletion, last-row, and malformed unpublished-tail negatives are maintained. Author validation: combined suites 177 passed in 18.07s; repository-wide Ruff and BasedPyright clean; edit tier passed in 50.83s. No full profile or BC329 target ran. Leave open for source-distinct re-review.
