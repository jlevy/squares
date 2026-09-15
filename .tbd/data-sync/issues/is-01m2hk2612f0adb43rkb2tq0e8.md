---
type: is
id: is-01m2hk2612f0adb43rkb2tq0e8
title: "PR #171 review D70: H-211 and X-034 imply the level-9 default sits in a measured range"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:38.786Z
updated_at: 2026-09-15T04:16:20.876Z
closed_at: 2026-09-15T04:16:20.875Z
close_reason: "Fixed on PR #171 in 1ef0e4e8: H-211 and X-034 say the cells ran under the previous law (0.15/2500/0/0) and 0.8 s moving span at 88d452f1, that #171 ships level 9 under 0.35/950/80/0.15 and a 0.9 s span, and that nothing has been measured under the new defaults."
resolution: null
duplicate_of: null
---
Canonical defect D70 from the 2026-09-14 stack triage (Medium). Sources: #171 R6 (doc item); #155 R8 (reviewer note on #171's sentence).

H-211 and X-034 imply the new level-9 default sits in a measured range ("inside the range measured as working"), but levels 6-10 were measured under the previous pair law (rigidity 0.15, repulsion 2500, attraction 0, range 0) and beat (0.8 + 0.55 + 0.25 + 0.8), and no level has been measured under #171's defaults.

Files: `packing/campaign/hypotheses/H-211-the-shake-has-a-sweet-spot.md:51-54`, `packing/campaign/explorations/X-034-the-workbench-physics-as-a-search.md:59-60`, `:205-207` @bb3f7c99. The recording half of #171 R6 is D46, fixed on #160 at 89250df8. Feature beads: think-redh, think-doxp.
