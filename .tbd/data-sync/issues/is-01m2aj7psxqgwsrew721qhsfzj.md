---
type: is
id: is-01m2aj7psxqgwsrew721qhsfzj
title: Preserve BC329 partial evidence on unexpected worker failures
kind: bug
status: open
priority: 1
version: 5
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
created_at: 2026-09-12T10:22:30.204Z
updated_at: 2026-09-12T11:27:55.777Z
---
Handle BrokenProcessPool, MemoryError, signals, parent interruption, and other unexpected worker or supervisor failures without leaving a stale phase/error or erasing completed direction files. Classify each failure consistently as invalid invocation or incomplete/unresolved under the declared outcome table, record exit status or signal and external lifetime, and guarantee process-group cleanup in a finally path. Add real and synthetic controls for pool death, signal exit, parent interruption, and failure after partial progress.

## Notes

Implemented worker preservation for unexpected Exception subclasses including MemoryError/BrokenProcessPool-class failures, supervisor preservation for signals/nonstandard exits, and BaseException cleanup for parent interruption. Completed direction files survive and scientific status stays unresolved. Focused synthetic plus real process-group controls pass; keep open until committed/integrated.
