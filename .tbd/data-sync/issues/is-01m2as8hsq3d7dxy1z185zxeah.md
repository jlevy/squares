---
type: is
id: is-01m2as8hsq3d7dxy1z185zxeah
title: Bound the BC329 parent-side source and runtime preflight
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh isolated implementation; root integration
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m260z2959dmcmn61pn2z7jsk
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T12:25:17.878Z
updated_at: 2026-09-12T13:36:48.236Z
---
The external deadline currently begins at worker launch; parent-side Git, runtime, and source-manifest preflight runs before supervision, and _git has no timeout. The receipt states that scope accurately, but a command can still hang before the worker starts. Before the BC329 scientific target, either bring parent preflight under an end-to-end deadline or add bounded subprocess timeouts with explicit prelaunch failure records, and keep documentation precise about the measured boundary.

## Notes

A source-distinct Sol xhigh agent is implementing an end-to-end bounded parent preflight in an isolated worktree from 5095241d. It will add stalled-subprocess and cleanup controls and will not run BC329.
