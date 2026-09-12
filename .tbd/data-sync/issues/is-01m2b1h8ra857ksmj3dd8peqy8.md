---
type: is
id: is-01m2b1h8ra857ksmj3dd8peqy8
title: Publish calibration success only after bounded terminal readback
kind: bug
status: in_progress
priority: 1
version: 13
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
updated_at: 2026-09-12T17:06:01.577Z
---
CAL-5 from the Astra Max source-distinct review. The supervisor publishes calibration-passed before its final readback and deadline check; KeyboardInterrupt at that boundary leaves a false terminal success, and unbounded observer/readback calls sit outside the measured lifetime. Keep the receipt nonterminal through bounded readback and observation, make final success the last transaction, retain complete admission duration, and test interruption and expiry at the boundary. This blocks calibration admission.

## Notes

Astra Max exact-head rereview of 967f7cd has reproduced a remaining CAL-5 failure. pthread_sigmask protects only the calling thread; with one eligible background thread, process-directed SIGINT/SIGTERM/SIGHUP can be received there and Python can run the handler on the main thread inside mkstemp, leaking the new fd and .result-admission-* path at both staging passes. Six synchronized cases reproduce strict artifact-set refusal. A separate os.fdopen-before-adoption failure leaks the fd even though the path is removed. Required repair: handler-level deferred raising across resource acquisition/ownership plus exception-safe descriptor adoption/cleanup, with signal-first provenance and real controls. Admission remains refused; no profile/BC329 run.
