---
type: is
id: is-01m4qhcw0287k3633q1rhz4jwn
title: "Workbench trajectory cost check: compare the best of three timings with the 400 ms ceiling (flaked on #512)"
kind: bug
status: in_progress
priority: 3
version: 4
delegate: claude-workbench-cost-fix-20261019
labels:
  - testing
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T07:49:22.050Z
updated_at: 2026-10-19T17:01:19.072Z
started_at: 2026-10-19T17:01:19.072Z
---
packages/workbench/tools/workbench_tools/animate_view_contract.py (about lines 1036-1043, run by workbench_tools.check_frontend as the "workbench browser behavior in Chromium" step) times six trajectory builds (n = 11, 100, 324; styles physics and bodies) once each and requires each under 400 ms and 4 MB. On PR #512, run 38182457550 attempt 1 (frontend job 114597711232, head 604699ee1) failed with "a trajectory costs over 400 ms or 4 MB: [(324, 'physics', 454, 1807280)]"; attempt 3 at the same commit passed. Proposed fix (not implemented): time each build three times and compare the fastest with 400 ms; keep the 4 MB limit on one measurement and both ceilings unchanged. Done when the check uses the best of three, the ceilings are unchanged, and check_frontend passes.

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/538 (label bug). Tracker https://github.com/jlevy/squares/issues/544.

2026-10-12, a second Animate view message (PR #546, review A, finding A5): both local runs of the Animate view check at 8a5e72e65, the `--fast` tier and its rerun, on a host at load 13 to 18 over 4 CPUs, failed with "play did not carry on from step to step: the stage showed n = [5, 6]" beside the trajectory cost message. `plays_across_steps` (packages/workbench/tools/workbench_tools/check_animate_view.py, about lines 230-246) plays for 3.5 s of real time, so load is a plausible cause; but n and n + 1 and nothing more is also the signature of the 2026-09-21 regression that stopped playback after the first step, which the check exists to catch. The hosted frontend job passed the check at 8a5e72e65 (Packing validation run 38229096917), and PR #546 changes no workbench code. Added to #538's scope, so that a third occurrence can be attributed: to load, or to a real regression.
