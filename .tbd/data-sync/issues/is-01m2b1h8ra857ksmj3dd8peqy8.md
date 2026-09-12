---
type: is
id: is-01m2b1h8ra857ksmj3dd8peqy8
title: Publish calibration success only after bounded terminal readback
kind: bug
status: in_progress
priority: 1
version: 12
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
updated_at: 2026-09-12T16:42:58.430Z
---
CAL-5 from the Astra Max source-distinct review. The supervisor publishes calibration-passed before its final readback and deadline check; KeyboardInterrupt at that boundary leaves a false terminal success, and unbounded observer/readback calls sit outside the measured lifetime. Keep the receipt nonterminal through bounded readback and observation, make final success the last transaction, retain complete admission duration, and test interruption and expiry at the boundary. This blocks calibration admission.

## Notes

Repair commit 967f7cd46e94a9fddbad653295b146de5740110c closes the remaining staging-acquisition ownership window. The supervisor blocks SIGTERM, SIGHUP, and SIGINT across each _stage_result call until its descriptor is closed and the returned path is assigned to the supervisor's final cleanup owner, then delivers pending cancellation through the existing provenance and redelivery path. A maintained real subprocess regression synchronizes SIGINT in the first and second real mkstemp acquisitions and verifies status 130, signal 2, prior-handler restoration and one delivery, closed descriptor, absent staging file, and strict retained-partial readback. Ordinary success and all late validation/serialization/publication cases remain covered. Author checks: 180 focused tests passed in 23.31s; exact Ruff floor clean with 1,786 files formatted; BasedPyright 0 findings in 37.06s. packing-validate --edit reached the full surface in 46.83s but failed only an unrelated concurrently introduced bead-tree inconsistency under the closed BC303 routing parent; all other selected steps passed. No profile or BC329 target ran. Leave CAL-5 open for source-distinct readback.
