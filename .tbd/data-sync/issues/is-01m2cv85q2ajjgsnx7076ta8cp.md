---
type: is
id: is-01m2cv85q2ajjgsnx7076ta8cp
title: Teach the profile coordinator the observed-topology receipt contract
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - integration
dependencies: []
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
created_at: 2026-09-13T07:38:31.521Z
updated_at: 2026-09-13T07:38:38.413Z
---
At integrated PR156 head faa4085d, the coordinator's inventory reader requires the old four-field supervision object and omits raw-worker-topology.json and normalized-exact-worker-topology.json. A successful topology-complete calibration receipt is therefore refused before any three-profile summary can complete. Update the independent inventory/readback contract, exact top-level artifact set, bindings, reconstructed metrics, and mutation controls; preserve source distinction and CAL-5 behavior; obtain exact-head rereview. Do not run a positive profile or BC329.

## Notes

Source-distinct exact-head review at faa4085d reproduced two integration refusals: _validate_inventory_receipt expects old supervision fields, and inventory_profile excludes the two worker-topology sidecars. Isolated topology tests 8 pass, calibration file 84 passes, coordinator file 14 passes only against old fake receipts; Ruff/BasedPyright clean. Repair is now active; no profile or BC329 ran.
