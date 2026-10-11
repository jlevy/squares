---
type: is
id: is-01m3xgkna3m3w1w50ky6gqyxyk
title: "Families of the n = 1..324 known-best packings: patterns, contact shading, exact regularization and asymptotics"
kind: epic
status: in_progress
priority: 2
version: 21
labels:
  - research
dependencies: []
child_order_hints:
  - is-01m3xgm640hgn44hzng6f4bpxb
  - is-01m3xgm6msf13b4yj4b9vx8y0a
  - is-01m3xgm762qkfx1wfna887cdsz
  - is-01m3xgm7qkkkcdckn74h9rq6c1
  - is-01m3xgm88psy65032zcy4re45j
  - is-01m3xgm8td0cpy923bjvqb7c31
  - is-01m3xgm9ccqv1h8p3j5x9ezjy0
  - is-01m3xhkkyewysj9dz2wb8tk6w8
  - is-01m3xhkvaxx58sv3pd8bdc7y9n
  - is-01m3xhxhccxa8qwx75rsgqrqmc
  - is-01m3xjxbdp7kkn4zemtj04cbwz
  - is-01m3xk451q4e319z9rrrj0ewb2
  - is-01m3xqajnsprcyjjcprafbvmee
  - is-01m3xqak9dr1e1r1z9ydv5gdf7
  - is-01m3yqvdgvgy8pbdg53j9xb7pj
  - is-01m3z2p86sfyxcc595rne126t7
  - is-01m41cx3q2pckpmsmmwq1rsngz
  - is-01m41gv134xbbtnamrd9nn94x9
created_at: 2026-10-02T05:15:20.771Z
updated_at: 2026-10-03T18:36:19.940Z
---
Owner question, 2026-10-02, after the atlas triangle view (think-kbo4) put all 324 known-best packings side by side.

Workflow entry (OR-5): W3 insight-iteration. Its literature lanes are W1-shaped and its census lanes are W2-shaped measurements; all are bounded delegated work inside this phase. Durable result: exploration X-049 plus two measurement tools under packing/devtools/ with tests.

Questions:
1. Families. The triangle shows structure by position relative to k^2: n = k^2-1 and k^2-2 are clean grids, n = k^2+1 looks 45-degree and symmetric, k^2+2 and pairs like 232-233 and 264-265 share patterns, and 268-269 and 301-302 are diagonal. Has anyone studied these families, experimentally or theoretically? Is it in our literature archive, and what does a new search find?
2. Shading. Many axis-aligned squares render lighter than the dark green that means four full-face contacts (102, 103, 106, 206, 268, 269 and others). Are these inexact-arithmetic errors? Confirm or refute by measurement.
3. Exact corrections. Where an axis-aligned component is a true grid but does not render dark, can an exact-arithmetic regularization fix it without changing the side or the evidence tier?
4. Asymptotics. How do these families behave as n grows? Is the set of patterns in the limit finite or infinitely varied? Which theory studies large-n structure, and is it on our research frontier (H-035, H-037, asymptotic-waste-bounds.yaml)?

Claim boundary: atlas witnesses are feasible constructions, not optimality evidence. A regularized drawing is a derived view and never replaces a source witness or promotes a tier.

## Notes

2026-10-03 close: every child bead is closed but think-wqfw, the owner's restoring commit for the sixteen rollups' withheld model labels. Session-168 is completed and certified at dd636b4cc; PR jlevy/squares#305 merged main (jlevy/squares#312) at 4a0d79ee9 and is green on every check at c73d0cc25. The epic closes when think-wqfw does.
