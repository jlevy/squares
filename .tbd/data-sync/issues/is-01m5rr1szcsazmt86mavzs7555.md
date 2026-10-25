---
type: is
id: is-01m5rr1szcsazmt86mavzs7555
title: "Import #806: Evan Daniel's s(182) <= 13.970916436215 (evand d99925d), 3.17e-3 below the register"
kind: task
status: in_progress
priority: 1
version: 6
delegate: c-import-806-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5rs5zgh67xp4p355jr8s3ak
hold: null
hold_until: null
created_at: 2026-10-25T05:20:35.819Z
updated_at: 2026-10-25T05:40:26.481Z
started_at: 2026-10-25T05:20:59.792Z
---
New 2026-10-25 issue https://github.com/jlevy/squares/issues/806 (evand, 04:16:24Z): s(182) <= 13.970916436215, the exact side of search/packer/candidates/s182-1024.cert at evand/square-packing d99925d1 (with .exact.txt KKT point, .input.txt, .json, _regularized.cert), 3.17e-3 below the register's 13.974090713122 (Couzo). In the case corpus (n <= 324): a register entry, stage 4 review and adoption under the house rule. Side-only Kaggle entries (Subramanya N, 2026-10-24 18:41 UTC, matching to 1.6e-11) are not reports. Also owns the read of evand/square-packing's 28 commits past the last read (head d99925d12982). Stage 1 triage read-only first.

## Notes

2026-10-25 stage 1 triage (c-triage-2lzo-1025, read-only, main bb756e193):
- Pin: evand/square-packing d99925d1298262c4ddb81c95abbb6f45adca8d3d (committed 04:11:15Z, pushed 04:16:05Z in 3c335fe..d99925d; #806 opened 04:16:24Z). s182-1024.cert 30648 B sha256 9e12e0a4...fe97 and _regularized.cert 30526 B f1ec415a...fabf match the issue's table; .exact.txt 3ed2a8a8..., .input.txt e79897cb..., .json e5491852... (issue gives no digests for these).
- Quick check: side = header = 13970916436214678735385725854133/10^30, rounds up to 13.970916436215; 3.174277e-3 below T-174 (house, both lanes); side - S_exact = 1.40e-19. One positive job on both maintained routes (kernel.run_case + validate_job): both accept, 16471 pairs, wall clearance 5e-21, pair gap ~1e-20; 4.03 CPU-s (exact_verify 2.39, independent 1.64), 4.11 s wall.
- Identity (devtools.measure_identity): vs T-174/house witness/T-098: no symmetry one to one; assignment 44 > 0.1, 79 > 1e-2, largest 0.813; 74 turned; 16 tilts reversed; no tilt angle shared. vs source input: one to one, largest 2.55e-7. vs source regularized view: same side, moves exactly its 43 flat + 6 rattler squares, 5 > 0.1 (largest 0.381).
- Report order at 182: T-056, T-098 (#375), #476, T-174 (PR #574, house), #593 (not recorded) all >= 13.97409071312...; Kaggle side-only Chavan 13.9727613470647 and Subramanya N 13.9709164362306 are no reports (no packing; the latter 1.59e-11 above). Couzo 1c17153 (head) holds T-174's side. Ledger draft upper-bounds-issue806-20261025 (scratch): #806 recorded, new packing continuing T-188; check OK.
- 28 commits: only d99925d holds a certificate; the rest are packer code, docs, deletions and private-store experiment notes (store bests only above 324, values private). Nothing else to import.
- Next free T: T-243 (unless #804 registers first in report order). Draft S3.
- Drafts: scratchpad/triage-806/drafts/ (result-requests-806.yaml validated by check_requests --record; intake-watch-read.yaml validated against schema; import-plan-806.yaml; ack-806.md; upper-bounds-issue806-20261025/).
