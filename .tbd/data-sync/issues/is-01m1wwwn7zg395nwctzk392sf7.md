---
type: is
id: is-01m1wwwn7zg395nwctzk392sf7
title: Reconstruct Burns's near-record n = 17 topology from the rounded coordinates and decide its atlas status
kind: task
status: open
priority: 2
version: 2
labels:
  - n17
  - atlas
dependencies: []
parent_id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
created_at: 2026-09-07T02:59:20.447Z
updated_at: 2026-09-07T03:00:03.389Z
---
Burns's second post describes an n = 17 arrangement at side W = 4.677648294965133 (0.002118 above Bidwell's 4.675530093604551) with 11 axis-aligned squares and 6 at a common tilt theta = 39.63188122755316 deg, a different contact topology from Bidwell's 10 + 7 at two angles, reached by four distinct searches. He gives W = 4 + 2/q - 1/q^2 with q = sin(theta) the root of 5q^5 + 5q^4 + 3q^3 - 3q^2 - 3q + 1 in (0, 1), W the real root of W^5 - 11W^4 + 41W^3 - 37W^2 - 81W + 19, and two wall-to-wall contact certificates A(theta), B(theta) that balance at that angle. The archive README and X-011 both say this repository has not reconstructed the contact graph. Using the rounded coordinates JSON (see the archive sub-bead), reconstruct the contact graph, confirm the exact side algebraically, and decide whether it enters the atlas as a non-record alternative basin for n = 17 and serves the H-020 / exp-011 search-calibration lane (the annealer returned the 5 x 5 grid at n = 17). Nothing here changes a bound.

## Notes

Receipt 2026-09-07 (scratch check on the fetched JSON, SHA-256 40622c8b...): 17 squares, 11 at angle 0 and 6 at 0.69170681618 rad = 39.6318812275 deg; all corners lie in [0, W]^2 with max coordinate exactly W = 4.677648294965133 and min exactly 0; separating-axis test gives max pairwise penetration 8.9e-16 (rounding noise), 25 pair contacts and 26 corner-wall contacts within 1e-6. Burns's algebra checks: the q quintic 5q^5+5q^4+3q^3-3q^2-3q+1 has real roots 0.63785262957341249 and 0.28894240127545662 in (0,1); the first gives theta = 39.6318812275532 deg, W = 4 + 2/q - 1/q^2 = 4.677648294965135, A(theta) = B(theta) = 4.677648294965133, and the W quintic residual 5.7e-14; the second root is spurious (W negative). The JSON's W and theta agree with the algebraic values to 2e-15 and 2e-14. Gap above Bidwell: 0.0021182013605818.
