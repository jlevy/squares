---
type: is
id: is-01m2b1h8ra857ksmj3dd8peqy8
title: Publish calibration success only after bounded terminal readback
kind: bug
status: in_progress
priority: 1
version: 10
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
updated_at: 2026-09-12T16:21:52.237Z
---
CAL-5 from the Astra Max source-distinct review. The supervisor publishes calibration-passed before its final readback and deadline check; KeyboardInterrupt at that boundary leaves a false terminal success, and unbounded observer/readback calls sit outside the measured lifetime. Keep the receipt nonterminal through bounded readback and observation, make final success the last transaction, retain complete admission duration, and test interruption and expiry at the boundary. This blocks calibration admission.

## Notes

Implementation correction 0533ebae fixed late validation, normal serialization, and atomic-promotion deadline handling, but Astra Max rereview found one remaining cancellation window. A real SIGINT delivered immediately after tempfile.mkstemp creates the staging file, before _stage_result receives the returned path, leaves an open descriptor and .result-admission-* file. The supervisor publishes partial and redelivers SIGINT, but the retained-artifact reader rejects the unexpected file. Both staging passes reproduce this. Admission remains closed; no profile or BC329 target ran.
