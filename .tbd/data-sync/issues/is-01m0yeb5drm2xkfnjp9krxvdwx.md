---
type: is
id: is-01m0yeb5drm2xkfnjp9krxvdwx
title: Serve deterministic free-quench runs through a loopback API
kind: task
status: closed
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
labels:
  - packing
  - motion-lab
dependencies:
  - type: blocks
    target: is-01m0yebd9ks8n9kjn3adq8npdv
parent_id: is-01m0yd38q3mxynbc38k3gyxt7f
created_at: 2026-08-26T07:07:54.154Z
updated_at: 2026-08-26T08:15:39.497Z
closed_at: 2026-08-26T08:15:39.496Z
close_reason: Loopback-only service, strict Phase 1 payload validation, deterministic trace save/replay, and free-quench scenario adapter implemented and validated.
resolution: null
duplicate_of: null
---
Add the loopback-only numerical service and free-quench scenario adapter. Accept versioned side/x/y/theta requests, enforce declared n and time budgets, reject editor-group or contact-lock fields, return typed trace failures, expose no remote network capability, and support deterministic request/trace save and replay.
