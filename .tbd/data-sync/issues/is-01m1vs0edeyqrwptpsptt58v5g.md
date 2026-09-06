---
type: is
id: is-01m1vs0edeyqrwptpsptt58v5g
title: "W5: measure and optimize the exhaustive checkpoint with bounded workers"
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T16:32:15.789Z
updated_at: 2026-09-06T18:11:41.343Z
---

## Notes

Full per-test profile retained at packing/benchmarks/validation-efficiency/checkpoints/2026-09-06-pre-main-integration.tar.gz with digest manifest; oldbase dirty-source limits explicit. Exhaustive55 passed1414.32s command wall; full65steps passed1generated drift failed1687.79s. Largest individual costs include witness207.83s, n40182.71s, n12interval105.11s, n20interval92.94s. PACK_JOBS cap corrected; no exhaustive-scheduling or overall-CI speedup claimed. Next experiment must preregister bounded outer/inner scheduling and total-work guard; n40 duplicate removal remains separate topology/coverage decision under think-xejq. Final hosted checkpoint34050662740 on fb1a987d is running.
