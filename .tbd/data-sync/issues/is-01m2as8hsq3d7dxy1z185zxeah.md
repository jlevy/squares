---
type: is
id: is-01m2as8hsq3d7dxy1z185zxeah
title: Bound the BC329 parent-side source and runtime preflight
kind: task
status: in_progress
priority: 2
version: 13
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
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
child_order_hints:
  - is-01m2ayepsewj93c5b3h1ww1vq3
  - is-01m2ayf0drt7y45xm38m8qt4q0
  - is-01m2ayh5000tkvsjyk2tt3tvxv
  - is-01m2aykekvqjdn3bn8p85g551v
created_at: 2026-09-12T12:25:17.878Z
updated_at: 2026-09-12T14:13:23.936Z
---
The external deadline currently begins at worker launch; parent-side Git, runtime, and source-manifest preflight runs before supervision, and _git has no timeout. The receipt states that scope accurately, but a command can still hang before the worker starts. Before the BC329 scientific target, either bring parent preflight under an end-to-end deadline or add bounded subprocess timeouts with explicit prelaunch failure records, and keep documentation precise about the measured boundary.

## Notes

Implementation commit c516a592 moves Git/runtime/source preflight inside the supervised process group and passes 86 target-free tests plus Ruff and BasedPyright. Independent audit found four blockers: think-rvhu for literal Git pathspecs and tracked-path overlap; think-fmju for operational-versus-invalid failure taxonomy; think-42zc for stale post-Popen timeout accounting and the OS-launch boundary; think-5fdx for real SIGTERM/SIGHUP cancellation reaping and receipt closure. Complete all four, run focused and required gates, and obtain fresh source-distinct review. No BC329 run.
