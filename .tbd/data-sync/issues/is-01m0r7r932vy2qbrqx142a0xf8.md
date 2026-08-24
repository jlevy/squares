---
type: is
id: is-01m0r7r932vy2qbrqx142a0xf8
title: Baseline and profile the end-to-end research loop
kind: task
status: in_progress
priority: 0
version: 9
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
updated_at: 2026-08-24T00:16:10.624Z
---
Unify the existing gate timing history on think-l3ds with reproducible end-to-end measurements of the normal gate, strict/deep gate, candidate generation, quench, overlap testing, canonicalization, certification, visualization preparation, ledger reconciliation, and agent idle time. Pre-register representative cold and warm workloads and repeat counts before tuning.

Acceptance: a versioned benchmark artifact records hardware, revision, commands, workload identities, raw samples, medians and dispersion; imports rather than duplicates think-l3ds evidence; attributes cost by stage; identifies the top throughput constraints; and establishes control-preserving speed targets without changing scientific acceptance criteria.

## Notes

2026-08-23 inventory now includes pushed revision 5fee7f0: one normal-gate run at 126s with soundness perimeter 34s, negative controls 31s, historical regressions 22s, LP 8s, lint 7s, atlas 5s, bead tree 4s and canonical identity 4s. Prior pushed point: 108s without a retained split; older normal 152s; older strict/deep 291-298s. These are single runs, not a benchmark. Next acceptance step remains a versioned three-run warm/cold artifact before tuning.
