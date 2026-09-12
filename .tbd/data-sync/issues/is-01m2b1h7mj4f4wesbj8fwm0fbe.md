---
type: is
id: is-01m2b1h7mj4f4wesbj8fwm0fbe
title: Close and exactly validate the calibration dilation record
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
created_at: 2026-09-12T14:49:50.993Z
updated_at: 2026-09-12T15:49:31.170Z
---
CAL-2 from the Astra Max source-distinct review. The calibration dilation checker accepts exact surd strings with arbitrary suffixes and incomplete nested records, and does not bind the outer summary to the nested artifact. Require canonical exact values or exact positive-surd parsing, validate the complete generic record and source fields, bind the outer summary, and retain coherent rehash, omission, polynomial, and source-geometry mutations. This blocks calibration admission; it proves no defect in the independently derived fixture constants.

## Notes

Source-distinct review at `d924a4bf` confirmed that the surd-prefix and incomplete-record bypasses are fixed, then found one remaining positive-input integration defect: the calibration oracle omits the generic builder's Condition 5′ coverage entry, so every genuine complete dilation record is rejected. The next repair must include the complete accepted-condition list and retain a positive comparison against the real generic builder on a small complete net. Review: `/private/tmp/bc329-calibration-integrated-correction-review.md`. No profile or target ran.
