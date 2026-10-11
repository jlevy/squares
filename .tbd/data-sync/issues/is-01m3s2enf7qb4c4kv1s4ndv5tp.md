---
type: is
id: is-01m3s2enf7qb4c4kv1s4ndv5tp
title: Index exact cover events by closed x-overlap for costly center rows
kind: task
status: closed
priority: 0
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rp1yjrw96h7yy6azcahx2w
created_at: 2026-09-30T11:50:59.302Z
updated_at: 2026-10-06T08:35:11.165Z
closed_at: 2026-10-06T08:35:11.164Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): devtools/n11_indexed_exact_cover.py is the 'indexed' cover backend of check_n11_generic_sequential.py on origin/main, pinned at INDEXED_COVER_SHA 68580e32...; check_n11_center_partition uses it; receipts/nonfield-manifest/indexed-cover-benchmark.json retained
resolution: null
duplicate_of: null
---
Build an opt-in exact cover helper that enumerates only segment pairs with overlapping closed x-projections, preserving all vertex and line-crossing events including equal-endpoint tangency. Differential-check event sets and cover verdicts against the frozen all-pairs backend on analytic adversarial shapes and representative pinned 1383 source geometry. Measure matched row cost before connecting the backend to accepted replay; no source proof credit from a primitive benchmark.

## Notes

Astra approved indexed exact-cover source SHA 68580e324e56c555ea0587b6f396b208fb66563d1e10bd449b446c97b7667ccd. Six focused controls pass; Ruff/format/BasedPyright clean. Retained source-bound benchmark receipts/nonfield-manifest/indexed-cover-benchmark.json: accepted 2095 rows 0/22/31 exact full-cover and receipt parity; representative 1383 node0 step1 row2 full source-proposal event set 613/1738 edges matches all-pairs, 1.682 vs 8.085 CPU seconds (4.81x event construction), 26.24s bounded benchmark wall. This is diagnostic, not case credit or whole replay speed. Four retained spawn receipts show whole-node128.3MB pickle vs current-step23.8MB; 3-worker startup1.864s vs0.551s. Parent integrating opt-in backend and current-step worker payload; full 1383 replay remains unverified.
