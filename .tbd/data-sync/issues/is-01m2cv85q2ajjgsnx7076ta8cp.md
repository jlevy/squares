---
type: is
id: is-01m2cv85q2ajjgsnx7076ta8cp
title: Teach the profile coordinator the observed-topology receipt contract
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - integration
dependencies: []
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
created_at: 2026-09-13T07:38:31.521Z
updated_at: 2026-09-13T07:53:01.138Z
---
At integrated PR156 head faa4085d, the coordinator's inventory reader requires the old four-field supervision object and omits raw-worker-topology.json and normalized-exact-worker-topology.json. A successful topology-complete calibration receipt is therefore refused before any three-profile summary can complete. Update the independent inventory/readback contract, exact top-level artifact set, bindings, reconstructed metrics, and mutation controls; preserve source distinction and CAL-5 behavior; obtain exact-head rereview. Do not run a positive profile or BC329.

## Notes

Coordinator repair implemented in the PR156 worktree and root-verified before commit. The inventory reader now requires six-field supervision, binds coordinator PID/PGID, includes both topology sidecars in the exact artifact set, and independently reconstructs route task/child identities, lifetimes, configured versus observed workers, concurrency, serial mode, summaries, digests, counts, and bytes. Integrated target-free suite: 242 passed in 24.59s; focused Ruff and Ruff format clean; BasedPyright zero. Exact-head source-distinct rereview remains required. No profile or BC329 ran.
