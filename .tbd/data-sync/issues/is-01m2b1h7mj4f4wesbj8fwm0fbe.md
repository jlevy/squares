---
type: is
id: is-01m2b1h7mj4f4wesbj8fwm0fbe
title: Close and exactly validate the calibration dilation record
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
created_at: 2026-09-12T14:49:50.993Z
updated_at: 2026-09-12T16:14:12.982Z
---
CAL-2 from the Astra Max source-distinct review. The calibration dilation checker accepts exact surd strings with arbitrary suffixes and incomplete nested records, and does not bind the outer summary to the nested artifact. Require canonical exact values or exact positive-surd parsing, validate the complete generic record and source fields, bind the outer summary, and retain coherent rehash, omission, polynomial, and source-geometry mutations. This blocks calibration admission; it proves no defect in the independently derived fixture constants.

## Notes

Implementation correction is retained at 0533ebaeb90cf42acf20e0029535356282a5624c. The exact oracle now includes Condition 5 prime, and a maintained positive control runs the real generic builder on the complete three-direction n=2 net before exact oracle comparison. Canonical surd, source, polynomial, proof, and omission negatives remain. Author validation: combined calibration and fixed-core suites 177 passed in 18.07s; repository-wide Ruff and BasedPyright clean; edit tier passed in 50.83s. No full profile or BC329 target ran. Leave open for source-distinct re-review.
