---
type: is
id: is-01m2asa131hqk3kagma2t2t3ab
title: Name exact interval and dilation directions in partial BC329 receipts
kind: task
status: in_progress
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol high isolated implementation; root integration
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m260z2959dmcmn61pn2z7jsk
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
  - type: blocks
    target: is-01m26c1jahzgfckegz7fp9wcq7
  - type: blocks
    target: is-01m2b1h805emc13mx1cykp5s5x
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T12:26:06.304Z
updated_at: 2026-09-12T15:39:31.995Z
---
Partial interval and dilation receipts currently retain a count and last row while the filesystem may contain an unpublished sparse tail. They publish no partial scientific summary and cannot produce acceptance, so this is auditability and recovery hardening. Before the BC329 scientific target, record canonical completed-direction labels for each published checkpoint and make readback distinguish the receipt-bound set from valid unpublished tail rows, mirroring raw and exact handling.

## Notes

Implementation commit ecce6dba0084d80e08d9eece2a37b19c1fe5e9ed publishes exact
canonical completed-direction strings for partial interval and dilation receipts and
strictly distinguishes published subsets from sparse unpublished tails. A source-distinct
Sol xhigh audit found no behavioral blocker: 97 isolated tests plus 6 adversarial
controls passed, Ruff/BasedPyright/diff were clean, and a temporary merge with c516 ran
101 tests plus the 6 controls clean. The integration cherry-pick is 8d21f58a.

A later exact-head preflight review reconfirmed the partial-direction behavior but found
that the integrated files are not Ruff-format clean: formatting would change
fixed_core_packet.py and test_fixed_core_packet.py, so packing-validate --edit is red.
Repair the formatting, rerun the combined focused and edit gates, then integrate and push
before closing this bead. Residual scope remains unchanged: partial non-last rows are not
digest-bound until complete state, last chronology is not derivable from files, and
Linux process-pool behavior was simulated on macOS. No BC329 run.
