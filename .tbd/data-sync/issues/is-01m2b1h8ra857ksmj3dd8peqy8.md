---
type: is
id: is-01m2b1h8ra857ksmj3dd8peqy8
title: Publish calibration success only after bounded terminal readback
kind: bug
status: in_progress
priority: 1
version: 8
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
updated_at: 2026-09-12T16:09:01.935Z
---
CAL-5 from the Astra Max source-distinct review. The supervisor publishes calibration-passed before its final readback and deadline check; KeyboardInterrupt at that boundary leaves a false terminal success, and unbounded observer/readback calls sit outside the measured lifetime. Keep the receipt nonterminal through bounded readback and observation, make final success the last transaction, retain complete admission duration, and test interruption and expiry at the boundary. This blocks calibration admission.

## Notes

Implementation correction is retained at 229b3fc2d3e5056c67b7dbe0224a399e524537c3. Terminal validation and serialization now prepare staged bytes while the durable receipt remains partial. Fresh cancellation and deadline checks precede the one atomic promotion, and a post-promotion deadline check revokes late success. The receipt records narrowly scoped terminal-admission time. Late CPU validation, serialization, OS promotion, and serialization-interrupt controls retain a partial receipt. Author validation: combined suites 177 passed in 17.79s; repository-wide Ruff and BasedPyright clean; edit tier passed in 61.84s. No full profile or BC329 target ran. Leave open for source-distinct re-review.
