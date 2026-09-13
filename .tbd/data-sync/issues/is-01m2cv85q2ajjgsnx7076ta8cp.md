---
type: is
id: is-01m2cv85q2ajjgsnx7076ta8cp
title: Teach the profile coordinator the observed-topology receipt contract
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - integration
dependencies: []
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
created_at: 2026-09-13T07:38:31.521Z
updated_at: 2026-09-13T17:51:08.186Z
---
At integrated PR156 head faa4085d, the coordinator's inventory reader requires the old four-field supervision object and omits raw-worker-topology.json and normalized-exact-worker-topology.json. A successful topology-complete calibration receipt is therefore refused before any three-profile summary can complete. Update the independent inventory/readback contract, exact top-level artifact set, bindings, reconstructed metrics, and mutation controls; preserve source distinction and CAL-5 behavior; obtain exact-head rereview. Do not run a positive profile or BC329.

## Notes

The original coordinator-topology consumer mismatch was repaired at 0cc0311a and integrated at 212e0dfc; 250 target-free tests and static gates pass. Independent exact-head review retained /private/tmp/bc329-topology-coordinator-exact-head-review.md with REFUSE on three follow-up defects: valid Linux effective-worker shape rejected; coherent topology task/child times not bounded by worker elapsed; result.json read before regular-file preflight. Sol repair is active on the four producer/coordinator code+test files. No profile or BC329 ran.
