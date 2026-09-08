---
type: is
id: is-01m1vy4nvz0f2m60aa95b15qvy
title: Ceiling verifier falsely accepts impossibility certificates outside its floating screen scale assumptions
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1vyfpzegaxyp52t4bfx85md
created_at: 2026-09-06T18:01:57.374Z
updated_at: 2026-09-06T18:50:56.978Z
closed_at: 2026-09-06T18:50:56.977Z
close_reason: "Implemented in PR #100 on codex/adversarial-review-fixes. Final commit 237d9386 passed hosted CI and pre-push validation; counterexample regressions and the 20000-case independent oracle replay passed. The separate missing-witness follow-up think-aenh remains open under epic think-hmtc."
resolution: null
duplicate_of: null
---
Adversarial review at edccf294 reproduced verify_ceiling proved=True and max_depth=0 for two coincident weight-10^21 unit squares near coordinates10^10 (true depth2*10^21). Constructor admits unrestricted positive L; SCREEN_MARGIN assumes coordinates<10. Set n=2*10^21, L10000000010, B9/10 and net(0,.1,.2,.3,.4,.42). A finite D4 half-integer grid has mass(2L+1)^2<n and covers every B-square, refuting the emitted impossibility theorem. Main s11 verifier is separate and unaffected. Require rigorous screening or enforce proven numerical envelope. Reproducer and review in /tmp/squares-core-review-2026-09-06/.
