---
type: is
id: is-01m2as8hsq3d7dxy1z185zxeah
title: Bound the BC329 parent-side source and runtime preflight
kind: task
status: in_progress
priority: 2
version: 15
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
  - is-01m2b1njv7ygehsqbcfbrg161b
created_at: 2026-09-12T12:25:17.878Z
updated_at: 2026-09-12T14:52:13.542Z
---
The external deadline currently begins at worker launch; parent-side Git, runtime, and source-manifest preflight runs before supervision, and _git has no timeout. The receipt states that scope accurately, but a command can still hang before the worker starts. Before the BC329 scientific target, either bring parent preflight under an end-to-end deadline or add bounded subprocess timeouts with explicit prelaunch failure records, and keep documentation precise about the measured boundary.

## Notes

Repair commit 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe addresses the four independent c516a592 blockers: think-rvhu literal pathspec plus tracked-output overlap; think-fmju invalid-versus-operational taxonomy; think-42zc post-Popen deadline recomputation with an explicit unbounded OS-launch interval; and think-5fdx real SIGTERM/SIGHUP process-group cleanup including the launch window. The active plan and preflight review record the contracts and exact bead IDs. Validation on the repaired target-free tree: 98 fixed-core tests passed in 11.40 s, Ruff and BasedPyright reported zero findings, and packing-validate --edit passed in 55.66 s. All four child beads and this parent remain open for source-distinct re-review. No BC329 target was registered or run.
