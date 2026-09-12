---
type: is
id: is-01m2b2esnxm9p4tmaxh5zvyrvm
title: Classify calibration-runner process-launch failures without losing evidence
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh repair; source-distinct rereview; root integration
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T15:05:59.729Z
updated_at: 2026-09-12T15:06:03.120Z
---
The source-distinct repair review reproduced that a non-OSError host failure from Popen is reported as supervisor-interrupted, drops the original message, and re-raises instead of producing a coherent operational terminal record. Define the allowed launch failure classes, preserve the concrete error, publish a schema-valid non-scientific disposition, reap any partially created process group, and retain adversarial controls for OSError and non-OSError launch failures. No BC329 target may run until this closes.
