---
type: is
id: is-01m2aj2e56r62h83avk7kexvhb
title: Promote any BC329 exact-route disagreement before timeout classification
kind: bug
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:19:37.509Z
updated_at: 2026-09-12T16:11:31.534Z
closed_at: 2026-09-12T16:11:31.534Z
close_reason: Implemented, integrated, independently reviewed, and published on the clean PR 156 stack by f1e397cd. Their remaining follow-up risks are separately tracked under calibration, parent preflight, partial-direction integration, and admission beads; no BC329 scientific target ran.
resolution: null
duplicate_of: null
---
The WIP records per-direction dense/slab disagreements but checks the aggregate only after the complete exact route. If a later direction times out, an already observed method disagreement can be published merely as incomplete. Make the first verified reader disagreement an invalid invocation with scientific status unresolved, retain its exact direction and both witnesses/values, and ensure later timeout or supervisor handling cannot downgrade or erase that classification. Add a disagreement-before-timeout regression and independent readback mutation.

## Notes

Immediate ExactReaderDisagreementError and protected invalid classification are implemented for disagreements reached by the iterator. Root review found a remaining admission gap: ordered ProcessPoolExecutor.map consumption can hide a later direction whose disagreement already completed behind a slower earlier direction until timeout. Child think-0ajj owns the bounded completion-order scheduler needed to satisfy this bead fully. Do not close until its slow-prefix/fast-disagreement control passes and the milestone is committed.
