---
type: is
id: is-01m0r7r932vy2qbrqx142a0xf8
title: Baseline and profile the end-to-end research loop
kind: task
status: in_progress
priority: 0
version: 8
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
updated_at: 2026-08-23T23:23:43.036Z
---
Unify the existing gate timing history on think-l3ds with reproducible end-to-end measurements of the normal gate, strict/deep gate, candidate generation, quench, overlap testing, canonicalization, certification, visualization preparation, ledger reconciliation, and agent idle time. Pre-register representative cold and warm workloads and repeat counts before tuning.

Acceptance: a versioned benchmark artifact records hardware, revision, commands, workload identities, raw samples, medians and dispersion; imports rather than duplicates think-l3ds evidence; attributes cost by stage; identifies the top throughput constraints; and establishes control-preserving speed targets without changing scientific acceptance criteria.

## Notes

2026-08-23 inventory: stable normal-gate checkpoint 108s (single run, no retained stage split); older measured normal gate 152s with perimeter 59s, controls 42s, LP 11s, atlas 11s, lint 10s, basin identity 7s; older strict/deep 291-298s. The 129s/27-control result belongs to the stashed prototype and is not a baseline. Next acceptance step is one versioned three-run warm/cold benchmark artifact for the normal gate, then separate candidate-generation, quench, canonicalization, and atlas workloads.
