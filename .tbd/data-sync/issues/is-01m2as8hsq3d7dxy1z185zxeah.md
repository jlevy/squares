---
type: is
id: is-01m2as8hsq3d7dxy1z185zxeah
title: Bound the BC329 parent-side source and runtime preflight
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m260z2959dmcmn61pn2z7jsk
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T12:25:17.878Z
updated_at: 2026-09-12T12:26:17.341Z
---
The external deadline currently begins at worker launch; parent-side Git, runtime, and source-manifest preflight runs before supervision, and _git has no timeout. The receipt states that scope accurately, but a command can still hang before the worker starts. Before the BC329 scientific target, either bring parent preflight under an end-to-end deadline or add bounded subprocess timeouts with explicit prelaunch failure records, and keep documentation precise about the measured boundary.
