---
type: is
id: is-01m2as8hsq3d7dxy1z185zxeah
title: Bound the BC329 parent-side source and runtime preflight
kind: task
status: in_progress
priority: 2
version: 18
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
  - is-01m2b2esnxm9p4tmaxh5zvyrvm
  - is-01m2b2etdnh14vgy3h8x79y5dj
created_at: 2026-09-12T12:25:17.878Z
updated_at: 2026-09-12T15:11:39.197Z
---
The external deadline currently begins at worker launch; parent-side Git, runtime, and source-manifest preflight runs before supervision, and _git has no timeout. The receipt states that scope accurately, but a command can still hang before the worker starts. Before the BC329 scientific target, either bring parent preflight under an end-to-end deadline or add bounded subprocess timeouts with explicit prelaunch failure records, and keep documentation precise about the measured boundary.

## Notes

The first repair commit 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe
addressed the original four c516a592 findings. A source-distinct Sol xhigh rereview at
/private/tmp/bc329-preflight-repair-rereview.md reproduced every original control and
accepted three repairs at their stated boundaries: think-rvhu literal Git pathspec and
tracked-output overlap, think-42zc recomputed post-Popen remaining time with late-group
cleanup, and think-5fdx SIGTERM/SIGHUP launch-window cleanup and signal redelivery. Those
three beads are closed. The reviewed tree passed 98 target-free tests in 9.93 seconds,
Ruff, BasedPyright, git diff check, and a 44-step edit tier in 49.49 seconds.

Admission remains blocked. think-fmju is incomplete because a uv.lock read OSError is
still wrapped as PacketError and published as exit 2 invalid/preflight-invalid. The same
review opened think-g7vg because output under .git/refs/heads can create a broken Git ref
that source_manifest accepts, and think-pvmv because a non-OSError Popen host failure is
mislabeled supervisor-interrupted, loses the original message, and re-raises instead of
returning a coherent operational result. Repair and source-distinctly recheck all three,
then revalidate on the combined publication head before closing this parent. No BC329
target was registered or run.
