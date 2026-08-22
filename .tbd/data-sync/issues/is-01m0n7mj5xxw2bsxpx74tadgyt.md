---
type: is
id: is-01m0n7mj5xxw2bsxpx74tadgyt
title: Establish how a proposed packing is verified exactly
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0n7mkg9c5ay1x8mza9z88wx
parent_id: is-01m0n7ka0xjff91yctt25c4m1y
created_at: 2026-08-22T17:17:32.221Z
updated_at: 2026-08-22T17:53:26.724Z
closed_at: 2026-08-22T17:53:26.724Z
close_reason: "Established that validity is a closed condition and record packings touch exactly, so no floating-point or interval check can certify one at any precision. Built a reusable exact verifier in explorations/packing/ (number field arithmetic with exact zero and sign decisions, separating-axis check generic over the scalar type, grid bucketing). Verified Trump's 11-square packing exactly: 55 pairs, 14 with zero gap, 20 boundary contacts, P(s)=0 for the published degree-8 polynomial, 43 digits recovered matching the 33 published, 0.35 s. Negative controls confirm it rejects overlaps down to 1e-100 while float64 with tolerance 1e-9 silently accepts 1e-12."
---
Separating-axis theorem over a real algebraic number field; why floating point and interval arithmetic alone cannot certify a packing whose squares touch; reference implementation plus negative controls; cost comparison against float64.
