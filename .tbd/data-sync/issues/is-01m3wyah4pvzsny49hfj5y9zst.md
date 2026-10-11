---
type: is
id: is-01m3wyah4pvzsny49hfj5y9zst
title: "Import wand125: mixed rectangle-measure certificates at n = 37, 65, 66, 90, 92 (#282)"
kind: task
status: closed
priority: 2
version: 10
spec_path: docs/project/specs/active/plan-2026-10-01-result-import-first-application.md
labels:
  - packing
  - result-import
dependencies:
  - type: blocks
    target: is-01m3yrzkz80qd1wv5sjr0kkkv0
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-01T23:55:47.217Z
updated_at: 2026-10-03T22:47:14.588Z
closed_at: 2026-10-03T22:47:14.588Z
close_reason: T-069 V3/C3 on main.
resolution: null
duplicate_of: null
---
Result import process from stage 1. New lower-bound entry for five counts; T-048 keeps its claim. Tarballs (125 MB) pinned by digest and not retained, as for n = 50. audit_wand125_point_and_mixed is hard-coded to n = 50 and needs a certificate parameter. Complete replay 45 to 90 CPU-h. T-048 own replay sits unmerged on claude/replay-wand125-n50-l740-local (think-nnlg). A rolling request: n = 82 to 85 are announced.

## To finish (validation backlog, 2026-10-02)

T-069 (mixed rectangle measures at n = 37, 65, 66, 90, 92, V0/C1). From packing/, per certificate: `.venv/bin/python3 -m devtools.audit_wand125_point_and_mixed mixed-replay nNN --range A-B --work W --workers 4` over all 201 angles, `mixed-merge nNN`, and `mixed-control nNN --work W`. Packet resources/web/wand125-point-and-mixed-2026-10-01/. Expected CPU by `mixed-price`: n37 3.1, n65 13.2, n66 10.3, n90 8.2, n92 9.0, 43.8 CPU-hours in all (wall up to twice that). Refutes: an angle refused, or a replay not matching the shipped record. Moves the rung: the five merged receipts recorded as replayed-here entries derive V3/C3. mixed_n92_L975 (think-r7yt) raises n = 92's reported value; T-069 stays true as stated. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

2026-10-01: stages 2 and 3 are in draft PR jlevy/squares#292 (branch claude/import-2026-10-01-requests, commit 2b7191461), stacked on #290. Stage 4 not started. The T-id is provisional until #292 is on main; quote it to no author before then.

2026-10-02 (PR #298): audit_wand125_point_and_mixed generalised (mixed-audit/fetch/replay/merge/price), all seven certificates' premises pass; replays of n37,n65,n66,n90,n92 and G's n84,n85 running on cloud runners m1-m3 (branches claude/replay-wand125-mixed-m1..m3), ~66 CPU-h estimated. Review docs/project/reviews/review-2026-10-02-wand125-mixed-rectangle-bounds.md: no blocking defect.
