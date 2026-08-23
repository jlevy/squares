---
type: is
id: is-01m0r7r9k8dcz960yqpx69vwnm
title: Parallelize isolated mutation controls and prove serial equivalence
kind: bug
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T21:17:17.799Z
updated_at: 2026-08-23T21:32:06.502Z
---
think-97pp owns removal of D-035: mutation controls must stop changing tracked files in place. This bead begins after that safety boundary exists. It runs independent isolated controls concurrently, removes redundant interpreter and dependency startup where measured, and preserves exact mutation-to-failure matching.

Acceptance: think-97pp is complete; serial and parallel modes run identical control ids and expected-failure assertions; per-worker state and output cannot cross-contaminate; interruption leaves no tracked or shared residue; three representative runs show the speedup and variance; and any non-equivalence fails closed.
