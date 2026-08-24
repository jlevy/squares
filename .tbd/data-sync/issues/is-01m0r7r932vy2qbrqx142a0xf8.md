---
type: is
id: is-01m0r7r932vy2qbrqx142a0xf8
title: Baseline and profile the end-to-end research loop
kind: task
status: in_progress
priority: 0
version: 11
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
updated_at: 2026-08-24T18:28:11.658Z
---
Unify the existing gate timing history on think-l3ds with reproducible end-to-end measurements of the normal gate, strict/deep gate, candidate generation, quench, overlap testing, canonicalization, certification, visualization preparation, ledger reconciliation, and agent idle time. Pre-register representative cold and warm workloads and repeat counts before tuning.

Acceptance: a versioned benchmark artifact records hardware, revision, commands, workload identities, raw samples, medians and dispersion; imports rather than duplicates think-l3ds evidence; attributes cost by stage; identifies the top throughput constraints; and establishes control-preserving speed targets without changing scientific acceptance criteria.

## Notes

2026-08-24 deep-review measurement finding D-101: exp-007 records 3.4 wall seconds although its sequential JSONL has two ~30s candidate quenches plus other calls; exp-008 aggregate is also below retained per-call sums. Treat historical round-level wall_seconds as untrusted for map pricing until reconstructed or remeasured with current receipts.\n\n2026-08-24 exp-029 n=8 bounded stage baseline at engine 69c6008: four retained quench events total 38.004s. Five four-event batches give median independent verification 0.000684s and canonical-key computation 0.004956s; in-process semantic replay is 0.007029s, while the frozen CLI costs 0.713s including startup. Canonicalization is only about 0.013% of retained quench wall at n=8. BC-007 preregisters a single n=9 event and stops for profile if the full cell exceeds 30s.
