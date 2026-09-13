---
type: is
id: is-01m2dzxy2qg4x28a66x0gw3r0t
title: "Run sheet: verify full source closure before evidence commit"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - run-sheet
dependencies: []
parent_id: is-01m2b884n0ms50xp93q6aaps1g
child_order_hints:
  - is-01m2e1t9kewbw1bv9zt6ak6fx7
created_at: 2026-09-13T18:19:33.334Z
updated_at: 2026-09-13T18:52:31.209Z
---
Independent operational review R4: compare all source/runtime paths and blob IDs from each accepted receipt to execution revision and intended evidence commit, including fixture, package initializers, helpers, lockfile and declarations; refuse additions/deletions/changes.

## Notes

Proposed R4 full source-closure contract retained at docs/project/specs/active/plan-2026-09-13-n11-bc329-runset-verifier.md; Sol max implementing target-free maintained command and synthetic controls. No admission until exact-head review.
