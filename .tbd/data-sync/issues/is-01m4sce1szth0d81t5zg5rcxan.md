---
type: is
id: is-01m4sce1szth0d81t5zg5rcxan
title: Recompute all 98 capture statements of T-153 and compare row for row (C3 part; ~1,273-2,347 CPU-h; held)
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m4sce27vcg4m62byjn67a8t9
parent_id: is-01m4sce0tyvdb701rcxm7p6h4g
hold: paused
created_at: 2026-10-13T01:01:06.751Z
updated_at: 2026-10-13T01:01:09.924Z
---
All 1,152 selected slices, 1,728,000 rows per checker, with at least the producer's Python capture checker (recompute_slice.py), each row compared with the stored receipts, plus a mutated-certificate control refused. Price (receipts/recomputation-price.json): 1,273 CPU-h Python, 1,074 Node, 2,347 both; median 2.5 CPU-s per row; K3 measured the Python checker here at 1.08x the stored CPU per row. Options priced 13 October: (a) GitHub Actions matrix on jlevy/squares (public, free standard runners): ~60 four-core jobs each under the 6 h limit, about a day at 15 jobs in parallel, sharing concurrency with PR CI; push-triggered on a dedicated branch since workflow_dispatch needs the default branch; (b) a rented 96-192 core machine, ~7-14 h, roughly 50-150 USD, owner-provided; (c) this 4-core container, ~13 days. Only receipts are retained (no licence for reuse). Held by the owner on 13 October.
