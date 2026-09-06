---
type: is
id: is-01m1vy4nvz0f2m60aa95b15qvy
title: Ceiling verifier falsely accepts impossibility certificates outside its floating screen scale assumptions
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1vyfpzegaxyp52t4bfx85md
created_at: 2026-09-06T18:01:57.374Z
updated_at: 2026-09-06T18:09:17.336Z
---
Adversarial review at edccf294 reproduced verify_ceiling proved=True and max_depth=0 for two coincident weight-10^21 unit squares near coordinates10^10 (true depth2*10^21). Constructor admits unrestricted positive L; SCREEN_MARGIN assumes coordinates<10. Set n=2*10^21, L10000000010, B9/10 and net(0,.1,.2,.3,.4,.42). A finite D4 half-integer grid has mass(2L+1)^2<n and covers every B-square, refuting the emitted impossibility theorem. Main s11 verifier is separate and unaffected. Require rigorous screening or enforce proven numerical envelope. Reproducer and review in /tmp/squares-core-review-2026-09-06/.
