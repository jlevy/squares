---
type: is
id: is-01m2aj2dszhq8h9e6sftwqjp0g
title: Make BC329 deadlines and process-group reaping end-to-end
kind: bug
status: in_progress
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
created_at: 2026-09-12T10:19:37.150Z
updated_at: 2026-09-12T11:59:36.722Z
---
The WIP scientific clock begins after parent process launch and interpreter/module startup, partial receipts can retain stale scientific_seconds, and the supervisor's mocked TERM/KILL tests do not establish that descendants are gone. Start the scientific clock at the declared parent invocation boundary, propagate an absolute deadline, update every terminal and partial clock consistently, reject NaN and infinity for every duration, and add a real subprocess-tree control that proves the process group is reaped after grace. Preserve invalid scientific classifications when the outer supervisor records process outcomes.

## Notes

Parent-origin clocks, inherited deadlines, prelaunch refusal, exit attestation and timeout/interruption process-group termination are implemented. Independent pre-commit audit reproduced a blocking leak: a leader can exit nonzero while a SIGTERM-ignoring grandchild remains in its PGID because supervise_worker only cleans the group on timeout/interruption. Follow-up must clean and verify the owned group after every nonzero exit and should fail closed if a nominal zero exit leaves descendants. A real synchronized adversarial test is required before closure.
