---
type: is
id: is-01m2aj2dszhq8h9e6sftwqjp0g
title: Make BC329 deadlines and process-group reaping end-to-end
kind: bug
status: in_progress
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
created_at: 2026-09-12T10:19:37.150Z
updated_at: 2026-09-12T10:32:33.243Z
---
The WIP scientific clock begins after parent process launch and interpreter/module startup, partial receipts can retain stale scientific_seconds, and the supervisor's mocked TERM/KILL tests do not establish that descendants are gone. Start the scientific clock at the declared parent invocation boundary, propagate an absolute deadline, update every terminal and partial clock consistently, reject NaN and infinity for every duration, and add a real subprocess-tree control that proves the process group is reaped after grace. Preserve invalid scientific classifications when the outer supervisor records process outcomes.

## Notes

Root is implementing the end-to-end deadline/schema slice on the clean BC329 stack. Current uncommitted changes start elapsed time at the worker invocation clock, include source binding/replay under the scientific deadline, update partial/terminal clocks, reject nonfinite CLI and saved numeric settings, and parse strict JSON without NaN/Infinity extensions. Real process-tree reaping, parent launch attestation, and adversarial timeout coverage remain before closure.
