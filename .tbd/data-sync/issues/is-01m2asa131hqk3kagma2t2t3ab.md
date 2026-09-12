---
type: is
id: is-01m2asa131hqk3kagma2t2t3ab
title: Name exact interval and dilation directions in partial BC329 receipts
kind: task
status: in_progress
priority: 2
version: 6
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
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T12:26:06.304Z
updated_at: 2026-09-12T14:13:25.101Z
---
Partial interval and dilation receipts currently retain a count and last row while the filesystem may contain an unpublished sparse tail. They publish no partial scientific summary and cannot produce acceptance, so this is auditability and recovery hardening. Before the BC329 scientific target, record canonical completed-direction labels for each published checkpoint and make readback distinguish the receipt-bound set from valid unpublished tail rows, mirroring raw and exact handling.

## Notes

Implementation commit ecce6dba0084d80e08d9eece2a37b19c1fe5e9ed publishes exact canonical completed-direction strings for partial interval and dilation receipts and strictly distinguishes published subsets from sparse unpublished tails. Source-distinct Sol xhigh audit found no blocker: 97 isolated tests plus 6 adversarial controls passed, Ruff/BasedPyright/diff clean; a temporary conflict-free merge with c516 ran 101 tests plus the 6 adversarial controls clean. Residual limits are scoped: partial non-last rows are not digest-bound until complete state, last chronology is not derivable from files, and Linux process-pool behavior was simulated but not executed on macOS. Keep in progress until cherry-picked onto the publication stack, revalidated on the combined exact head, pushed, and hosted CI is green. No BC329 run.
