---
type: is
id: is-01m0r7r932vy2qbrqx142a0xf8
title: Baseline and profile the end-to-end research loop
kind: task
status: in_progress
priority: 0
version: 12
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-efficiency
  - performance
dependencies:
  - type: blocks
    target: is-01m0r7r9k8dcz960yqpx69vwnm
  - type: blocks
    target: is-01m0r7rab2j8krgraey9a810x9
  - type: blocks
    target: is-01m0r7rb2hs1vdeebqb33471w3
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T21:17:17.281Z
updated_at: 2026-08-24T18:36:24.041Z
---
Unify the existing gate timing history on think-l3ds with reproducible end-to-end measurements of the normal gate, strict/deep gate, candidate generation, quench, overlap testing, canonicalization, certification, visualization preparation, ledger reconciliation, and agent idle time. Pre-register representative cold and warm workloads and repeat counts before tuning.

Acceptance: a versioned benchmark artifact records hardware, revision, commands, workload identities, raw samples, medians and dispersion; imports rather than duplicates think-l3ds evidence; attributes cost by stage; identifies the top throughput constraints; and establishes control-preserving speed targets without changing scientific acceptance criteria.

## Notes

2026-08-24 deep-review measurement finding D-101: exp-007 records 3.4 wall seconds although its sequential JSONL has two ~30s candidate quenches plus other calls; exp-008 aggregate is also below retained per-call sums. Treat historical round-level wall_seconds as untrusted for map pricing until reconstructed or remeasured with current receipts.\n\n2026-08-24 exp-029 n=8 baseline: four quenches total 38.004s; median four-event verification 0.000684s, keys 0.004956s, replay 0.007029s. Keys are ~0.013% of quench wall.\n\n2026-08-24 exp-030 n=9 performance cell: complete command 21.36s under the 30s profile trigger; retained quench 20.062s; median one-event verification 0.000174s, keys 0.001074s, replay 0.001622s. Keys are ~0.0054% of quench wall. No profile or additional sample was triggered. Broader benchmark acceptance remains open.
