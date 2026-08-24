---
type: is
id: is-01m0sy35vs5bh8b3692qvp0v6j
title: H-041 checker must prove all tiling vertices lie in the container
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-041-repaired-stromquist-point-set.md
labels: []
dependencies: []
parent_id: is-01m0srspsyjecv6bdatrx8r5bx
created_at: 2026-08-24T13:06:57.514Z
updated_at: 2026-08-24T13:18:00.172Z
closed_at: 2026-08-24T13:18:00.171Z
close_reason: The H-041 verifier exact-checks all Figure 13 and Figure 14 tiling vertices inside [0,s]^2 and its outside-container mutation is rejected. Exact generate/replay and lint/type checks pass; D-156 records the correction.
resolution: null
duplicate_of: null
---
Verifier soundness gap found before the scientific run. The first exact-cover draft checked face incidence, noncrossing, Euler characteristic, boundary-line membership and total area, but never explicitly proved that every used vertex lies in [0,s]^2. Acceptance: exact Q(sqrt(5)) containment for the complete Figure 13 and Figure 14 vertex inventories, a mutation outside the container that the checker rejects, defect-log entry, and focused lint/type/generate/replay evidence.
