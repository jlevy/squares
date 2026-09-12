---
type: is
id: is-01m2b1h7mj4f4wesbj8fwm0fbe
title: Close and exactly validate the calibration dilation record
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
created_at: 2026-09-12T14:49:50.993Z
updated_at: 2026-09-12T14:50:20.225Z
---
CAL-2 from the Astra Max source-distinct review. The calibration dilation checker accepts exact surd strings with arbitrary suffixes and incomplete nested records, and does not bind the outer summary to the nested artifact. Require canonical exact values or exact positive-surd parsing, validate the complete generic record and source fields, bind the outer summary, and retain coherent rehash, omission, polynomial, and source-geometry mutations. This blocks calibration admission; it proves no defect in the independently derived fixture constants.
