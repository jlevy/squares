---
type: is
id: is-01m3vqg7xv2wwb5rh3d24fg278
title: Benchmark bounded exact intervals and compact n17 endpoint receipts
kind: task
status: open
priority: 2
version: 7
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
child_order_hints:
  - is-01m4as6c7fr14famqr6qm8r2ah
hold: paused
created_at: 2026-10-01T12:37:19.929Z
updated_at: 2026-10-13T00:55:29.642Z
---
Deferred after exp238 cost review: repeated support caching preserves exact arithmetic; fixed256bit outward dyadic rounding could bound denominator/receipt growth but needs new frozen arithmetic contract and independent controls. Baseline43.45s,4.717MB with25.80s symbolic and16.42s interval+formatting. Do not rerun accepted targets or displace n17 capture work without a separately selected bounded benchmark.

## Notes

Deferred optimization is a sibling of completed profilingthink-4krl under the active research epic. Reparented to preserve openwork without leaving an open child under a closed task. No targetrerun or changedarithmeticcontract.

2026-10-13 owner decision: suspended pending Overbeck's proof that s(17) = L (#557; registered as T-153 by #560, credited by #571), which likely subsumes new s(17) research. Resumes only if the owner lifts the suspension, for example if T-153's replays and reviews find a gap or the candidate is withdrawn. Benchmark of exact intervals and compact n17 endpoint receipts: an instrument built for the n = 17 proof.
