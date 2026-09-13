---
type: is
id: is-01m2as8hsq3d7dxy1z185zxeah
title: Bound the BC329 parent-side source and runtime preflight
kind: task
status: closed
priority: 2
version: 22
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
  - type: blocks
    target: is-01m26c1jahzgfckegz7fp9wcq7
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
child_order_hints:
  - is-01m2ayepsewj93c5b3h1ww1vq3
  - is-01m2ayf0drt7y45xm38m8qt4q0
  - is-01m2ayh5000tkvsjyk2tt3tvxv
  - is-01m2aykekvqjdn3bn8p85g551v
  - is-01m2b1njv7ygehsqbcfbrg161b
  - is-01m2b2esnxm9p4tmaxh5zvyrvm
  - is-01m2b2etdnh14vgy3h8x79y5dj
  - is-01m2b3mn50tv03ktcns071x9m9
created_at: 2026-09-12T12:25:17.878Z
updated_at: 2026-09-13T05:13:28.200Z
closed_at: 2026-09-13T05:13:28.200Z
close_reason: Reviewed corrections integrated and published in the stack. Fresh T025/T026 exact replays pass; PR149 delta gate passes46steps/1109tests; final PR156 gate passes46steps/1284tests. Runner source and independent mathematical reviews accept the repairs. Final hosted checkpoint and overall readiness remain open under think-0adb; BC329 calibration/execution remains blocked separately.
resolution: null
duplicate_of: null
---
The external deadline currently begins at worker launch; parent-side Git, runtime, and source-manifest preflight runs before supervision, and _git has no timeout. The receipt states that scope accurately, but a command can still hang before the worker starts. Before the BC329 scientific target, either bring parent preflight under an end-to-end deadline or add bounded subprocess timeouts with explicit prelaunch failure records, and keep documentation precise about the measured boundary.

## Notes

Integrated follow-up preflight repair on calibration head: original repair 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe is 2179b327; d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014 fixes the remaining uv.lock I/O taxonomy, rejects worktree/common Git administrative output paths, and records ordinary non-OSError Popen failures as launch-failed return 1 while preserving signal/KeyboardInterrupt paths. Real and adversarial controls are part of the 170-test combined target-free pass. think-fmju, think-g7vg, and think-pvmv remain open for source-distinct re-review; BC329 was not run.
