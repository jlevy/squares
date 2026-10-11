---
type: is
id: is-01m3zq1e2jrzc7w09gkzt9qx4c
title: "Adaptive (non-uniform) kernel rows: producer split rule (K2) and verifier partition/predecessor check (P2, reviewed by R6)"
kind: task
status: closed
priority: 0
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-03T01:46:12.434Z
updated_at: 2026-10-05T05:35:42.773Z
started_at: 2026-10-05T05:34:33.077Z
closed_at: 2026-10-05T05:35:42.773Z
close_reason: "Landed (155abe8a2, on #347) and its verifier is listed (kernel-adaptive-rows at 575795e02, verifier-rewrites review section 5); SW9 closed with it."
resolution: null
duplicate_of: null
---
K2's closure rule: a class closes only when per-row losses (wall legal-box loss ~dtheta/2 near axis angles, core loss) are below ~1-1.5x its float margin. Residue margins are 4e-3 to 1e-2, so uniform rows would need 128-256 bins (4-8x cost). Adaptive rows bisect only live wall rows near axis angles: effective 256-512 bins there at ~1.5-2x the 64-bin cost. The checker already accepts refinement (complete_refinement); producer split rule opt-in (K2); verifier must check partition and predecessor containment (P2); R6 reviews before the new digest is listed. First target: the 539-orbit south-wall class, which stalls at 64 bins (e1ee78eb9).

## Notes

K2 split rule committed 9d3cb521b; W7 at 64 bins with splitting still closes (f3c2ccced, +15% rows, splits on side-N0). P2's verifier extension (digest 64474e45) green: uniform W7 and N1 identical; two refined certificates pass; 10 doctored refinements refused; 12/13 mutants caught (1 equivalent). R6 reviewing the delta before the digest is listed. K2 now running flag 2 (a9, 122 orbits, pen 9.3e-3) at 64 bins uniform; flag 3 next; split reruns for stalls; then the south-wall class adaptive.
