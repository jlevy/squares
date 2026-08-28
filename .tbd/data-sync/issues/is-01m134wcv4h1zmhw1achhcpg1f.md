---
type: is
id: is-01m134wcv4h1zmhw1achhcpg1f
title: "PR #50 review R2: High: 'no route to step 5 avoiding steps 3-4' is false; closed n=29 system exists in-repo"
kind: bug
status: open
priority: 2
version: 1
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:58:45.220Z
updated_at: 2026-08-28T02:58:45.220Z
---
The SVG contains FindRoot[{f1==0..f6==0},{{s,..},{a,..},{b,..},{c,..},{d,..},{i,..}},WorkingPrecision->200] plus r1..rD centre-elimination offsets, and verify_svg already replays it at residual 2.6e-100. Independently confirmed. X-004 and both specs assert the opposite; the forced phase order is wrong for the n=29 target.
