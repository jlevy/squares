---
type: is
id: is-01m2b1h8ra857ksmj3dd8peqy8
title: Publish calibration success only after bounded terminal readback
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
created_at: 2026-09-12T14:49:52.138Z
updated_at: 2026-09-12T15:25:33.976Z
---
CAL-5 from the Astra Max source-distinct review. The supervisor publishes calibration-passed before its final readback and deadline check; KeyboardInterrupt at that boundary leaves a false terminal success, and unbounded observer/readback calls sit outside the measured lifetime. Keep the receipt nonterminal through bounded readback and observation, make final success the last transaction, retain complete admission duration, and test interruption and expiry at the boundary. This blocks calibration admission.

## Notes

Repair implemented in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014. The calibration receipt stays nonterminal through a separate deadline-bounded parent readback process; ps observations use the remaining external allowance; success is the final atomic write after readback, deadline, metrics, and invocation checks. Maintained timeout and KeyboardInterrupt transaction controls leave partial receipts and reap the active group. Leave open for source-distinct closure review.
