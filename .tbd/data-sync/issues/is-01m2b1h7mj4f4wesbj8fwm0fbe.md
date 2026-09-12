---
type: is
id: is-01m2b1h7mj4f4wesbj8fwm0fbe
title: Close and exactly validate the calibration dilation record
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
created_at: 2026-09-12T14:49:50.993Z
updated_at: 2026-09-12T15:25:32.844Z
---
CAL-2 from the Astra Max source-distinct review. The calibration dilation checker accepts exact surd strings with arbitrary suffixes and incomplete nested records, and does not bind the outer summary to the nested artifact. Require canonical exact values or exact positive-surd parsing, validate the complete generic record and source fields, bind the outer summary, and retain coherent rehash, omission, polynomial, and source-geometry mutations. This blocks calibration admission; it proves no defect in the independently derived fixture constants.

## Notes

Repair implemented in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014. Dilation readback now compares the full generic record against the exact n=2 oracle, including canonical surd strings, source geometry, accepted conditions, defining polynomials, proof fields, and endpoint semantics; the outer summary must reproduce the nested record. Maintained source, expression, polynomial, omission, square, and boolean mutations are refused. Leave open for source-distinct closure review.
