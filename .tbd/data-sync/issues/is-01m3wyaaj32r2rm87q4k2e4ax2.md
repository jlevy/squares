---
type: is
id: is-01m3wyaaj32r2rm87q4k2e4ax2
title: "Import wand125: s(59) = 8 (#280)"
kind: task
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
created_at: 2026-10-01T23:55:40.479Z
updated_at: 2026-10-04T06:33:58.503Z
closed_at: 2026-10-04T06:33:58.503Z
close_reason: "Done on origin/main e5a48b310: T-066 s(59)=8 V3/C3 (E-n059-wand125-mixed-cover-zmx2-replay with d4/full receipts and mutation controls); T-062/T-063 name the T-066 monotone route; review-2026-10-02-wand125-s59-s77-mixed-covers.md. #280 replied and closed 2026-10-03T18:48Z."
resolution: null
duplicate_of: null
---
Result import process from stage 1. New optimality entry; T-062 and T-063 gain a sentence naming the monotone route. Source wand125/square-packing-bounds at 1a25a5e, checkers Daniel at b91d70b6 (already retained). Triage: verify.sh cannot pass as published (SHA256SUMS lists unpublished logs); the exact evidence is two runs, the main one NOT VERIFIED with 6 boxes, on the checker that predates the zero-width-bin guard. Cheapest complete replay zmx2 --d4 and --full, about 2,200 CPU-s.

## Notes

2026-10-01: stages 2 and 3 are in draft PR jlevy/squares#292 (branch claude/import-2026-10-01-requests, commit 2b7191461), stacked on #290. Stage 4 not started. The T-id is provisional until #292 is on main; quote it to no author before then.

2026-10-02 (stage 4, PR #298): zmx2 6b7f0f79 d4 and full replays of the s59 cover PASS (6,400 and 51,200 roots, 0 uncertified; box totals equal the source README's); receipts in wand125-point-and-mixed-2026-10-01/receipts/. Review docs/project/reviews/review-2026-10-02-wand125-s59-s77-mixed-covers.md: no blocking defect for the claim; the two-run zm_mixed composite is undecided from published manifests and is not recorded as evidence. Left: controls (lane K), evidence + T-066 rungs, reply after merge.
