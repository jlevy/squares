---
type: is
id: is-01m2aj2e56r62h83avk7kexvhb
title: Promote any BC329 exact-route disagreement before timeout classification
kind: bug
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:19:37.509Z
updated_at: 2026-09-12T11:02:31.204Z
---
The WIP records per-direction dense/slab disagreements but checks the aggregate only after the complete exact route. If a later direction times out, an already observed method disagreement can be published merely as incomplete. Make the first verified reader disagreement an invalid invocation with scientific status unresolved, retain its exact direction and both witnesses/values, and ensure later timeout or supervisor handling cannot downgrade or erase that classification. Add a disagreement-before-timeout regression and independent readback mutation.

## Notes

Implemented immediate ExactReaderDisagreementError after the disagreeing row is retained and before the deadline check. The result records direction, both exact values and both witnesses as invalid/reader-disagreement; readback reconstructs the first disagreement; later external-timeout bookkeeping preserves it. Focused controls pass. Keep in progress until committed.
