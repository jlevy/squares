---
type: is
id: is-01m3s5hdztw1rs4m4yfn29p17z
title: Measure resident Rust rectangle transport against batch queries
kind: task
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rcka78kmcccpetknr2mswh
created_at: 2026-09-30T12:44:55.673Z
updated_at: 2026-09-30T12:51:59.764Z
closed_at: 2026-09-30T12:51:59.763Z
close_reason: Fixed-work Rust transport optimization hypothesis measured and rejected; reusable benchmark and source-bound receipt retained.
resolution: null
duplicate_of: null
---
Predeclared fixed-work diagnostic: use pinned Tokoharu n11 rectangle table and 128 exact angle-1 core polygons. Compare one resident child doing 128 singleton JSONL requests with a fresh child doing one 128-polygon request; require identical exact per-polygon answers and immutable source/binary pins. Criterion for pursuing batching: batch query-phase wall <= 0.75 times singleton query-phase wall in three paired trials, with both <=30s total. Record child CPU and full session wall separately. This is diagnostic only: complete analytic n3 verifier parity remains the existing control and bounded n11 is inconclusive; no verifier speed or proof claim follows from this measurement.

## Notes

Predeclared three paired trials completed in 4.70s outer, 128 distinct angle-1 Tokoharu n11 core polygons per resident session, exact outputs identical in every pair. Batch/singleton query-wall ratios 0.99586, 0.98541, 0.99243 (median 0.99243), failing the <=0.75 criterion. Rust child CPU ~0.543-0.548s per 128 queries in both modes; coordinator CPU ~0.006-0.009s; arithmetic dominates this fixed workload. The existing complete analytic n3 all-201 verifier parity remains the correctness control (Rust slower 3.800s vs Python 0.504s); Tokoharu n11 1000-node parity is INCONCLUSIVE and confers no proof/speed claim. Do not implement batching solely for this workload. Next bounded optimization hypothesis, if prioritized after T060: reduce exact per-polygon arithmetic/rectangle work (profile Rust clip/BigRational and consider exact spatial filtering) under matched complete controls. Tool packing/benchmarks/bench_rectangle_rust_transport.py SHA85dad5a9c0422e21bc5a6a6ce2ca159b35874ee3989cc17ca2d074b533328bd2; receipt packing/resources/web/wand125-tools-2026-09-29/receipts/rust-transport-fixed-2026-09-30.json SHA2817014ec199dbe3e77a7e29d764c2349f007eb942ee2375a0c6730adaf5612b. Ruff/format/BasedPyright clean.
