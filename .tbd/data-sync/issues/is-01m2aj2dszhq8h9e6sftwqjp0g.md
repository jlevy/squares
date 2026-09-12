---
type: is
id: is-01m2aj2dszhq8h9e6sftwqjp0g
title: Make BC329 deadlines and process-group reaping end-to-end
kind: bug
status: in_progress
priority: 1
version: 6
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
created_at: 2026-09-12T10:19:37.150Z
updated_at: 2026-09-12T11:27:55.777Z
---
The WIP scientific clock begins after parent process launch and interpreter/module startup, partial receipts can retain stale scientific_seconds, and the supervisor's mocked TERM/KILL tests do not establish that descendants are gone. Start the scientific clock at the declared parent invocation boundary, propagate an absolute deadline, update every terminal and partial clock consistently, reject NaN and infinity for every duration, and add a real subprocess-tree control that proves the process group is reaped after grace. Preserve invalid scientific classifications when the outer supervisor records process outcomes.

## Notes

Implemented parent-origin absolute scientific/external deadlines, worker CLI inheritance checks, supervisor prelaunch deadline refusal, parent-observed exit attestation, public readback refusal of unsupervised worker receipts, and real process-group/grandchild termination control. Every phase publication now refreshes clocks. Focused tests pass; keep open until provenance integration, commit, and full target-free calibration.
