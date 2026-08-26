---
type: is
id: is-01m0yeb5drm2xkfnjp9krxvdwx
title: Serve deterministic free-quench runs through a loopback API
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
labels:
  - packing
  - motion-lab
dependencies:
  - type: blocks
    target: is-01m0yebd9ks8n9kjn3adq8npdv
parent_id: is-01m0yd38q3mxynbc38k3gyxt7f
created_at: 2026-08-26T07:07:54.154Z
updated_at: 2026-08-26T07:08:02.214Z
---
Add the loopback-only numerical service and free-quench scenario adapter. Accept versioned side/x/y/theta requests, enforce declared n and time budgets, reject editor-group or contact-lock fields, return typed trace failures, expose no remote network capability, and support deterministic request/trace save and replay.
