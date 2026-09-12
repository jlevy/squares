---
type: is
id: is-01m2b1h8ra857ksmj3dd8peqy8
title: Publish calibration success only after bounded terminal readback
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
created_at: 2026-09-12T14:49:52.138Z
updated_at: 2026-09-12T16:14:14.055Z
---
CAL-5 from the Astra Max source-distinct review. The supervisor publishes calibration-passed before its final readback and deadline check; KeyboardInterrupt at that boundary leaves a false terminal success, and unbounded observer/readback calls sit outside the measured lifetime. Keep the receipt nonterminal through bounded readback and observation, make final success the last transaction, retain complete admission duration, and test interruption and expiry at the boundary. This blocks calibration admission.

## Notes

Implementation correction is retained at 0533ebaeb90cf42acf20e0029535356282a5624c. Terminal validation and a first serialization stage now complete while the durable receipt remains partial; that measured admission duration is embedded by a second stage. Fresh cancellation and deadline checks precede the one atomic promotion, and a post-promotion deadline check revokes late success. Late CPU validation, serialization, OS promotion, and serialization-interrupt controls retain a partial receipt. Author validation: combined suites 177 passed in 18.07s; repository-wide Ruff and BasedPyright clean; edit tier passed in 50.83s. No full profile or BC329 target ran. Leave open for source-distinct re-review.
