---
type: is
id: is-01m45ncp7p0yab6vmn2x4358d2
title: "n17 kernel producer: hull-vertex compression pull 2^-12 caps reachable radius (lane R9 finding)"
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: guzhou-codex-graph-gate
labels: []
dependencies: []
parent_id: is-01m3z64p1mx8yrv14xk2e77xz2
hold: null
hold_until: null
created_at: 2026-10-05T09:12:50.678Z
updated_at: 2026-10-07T06:14:09.077Z
started_at: 2026-10-07T06:14:09.076Z
---
Lane R9 review (session-182, review-2026-10-05-n17-capture-r9.md): producer.kernel_points/compress pull every owned-hull vertex 2^-12 of its distance to the vertex mean (~1.22e-4 at unit scale), at producer.py lines 191-228 and 681-715 at 451154f60. Three one-link wall-side bounds converged to -1.2623e-4 (x2) and -1.4866e-4, identical at 128 and 256 rows: 13% of the box per hull link, 61% of H-261's radius 1/5000, so the kernel as built cannot reach that radius through hull links at any row count. It does not explain pilot 2's stall (3 links lose 3.7e-4 of 9.8e-4). Proposed repair: 2^-12 -> 2^-18, predicted residual < 1e-5 with contraction still not starting. Candidate defect record; also part of R9 measurement stage 1. Soundness: the pull is inward compression used by the producer; confirm the checker/verifier are unaffected before any record.
