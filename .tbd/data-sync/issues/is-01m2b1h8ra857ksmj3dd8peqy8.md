---
type: is
id: is-01m2b1h8ra857ksmj3dd8peqy8
title: Publish calibration success only after bounded terminal readback
kind: bug
status: in_progress
priority: 1
version: 14
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
updated_at: 2026-09-13T05:47:38.908Z
---
CAL-5 from the Astra Max source-distinct review. The supervisor publishes calibration-passed before its final readback and deadline check; KeyboardInterrupt at that boundary leaves a false terminal success, and unbounded observer/readback calls sit outside the measured lifetime. Keep the receipt nonterminal through bounded readback and observation, make final success the last transaction, retain complete admission duration, and test interruption and expiry at the boundary. This blocks calibration admission.

## Notes

Second repair is committed at 85d3f529c29114cf6b202fb1b09445c0dc002bc1. It adds handler-level staging-depth deferral with signal-first provenance and explicit raw-fd ownership until os.fdopen adopts it. Maintained controls cover SIGINT/SIGTERM/SIGHUP at both staging passes from the main thread and an already eligible background thread, plus fdopen failure at both passes. The combined target-free suites pass 192 tests in 25.44s; Ruff, BasedPyright, and packing-validate --edit pass. Author evidence only; CAL-5 remains open pending think-1arg source-distinct exact-head review. No profile or BC329 run.
