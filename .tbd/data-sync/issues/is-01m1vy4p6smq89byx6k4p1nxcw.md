---
type: is
id: is-01m1vy4p6smq89byx6k4p1nxcw
title: Withdraw unsupported n12 covering-value slope and ladder endpoint inference
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1vyfpzegaxyp52t4bfx85md
created_at: 2026-09-06T18:01:57.720Z
updated_at: 2026-09-06T18:50:56.991Z
closed_at: 2026-09-06T18:50:56.991Z
close_reason: "Implemented in PR #100 on codex/adversarial-review-fixes. Final commit 237d9386 passed hosted CI and pre-push validation; counterexample regressions and the 20000-case independent oracle replay passed. The separate missing-witness follow-up think-aenh remains open under epic think-hmtc."
resolution: null
duplicate_of: null
---
At edccf294, covering-values.yaml654-661 and CERTIFICATE-REACH64 infer slope>=24.9 and endpoint3.96004 from two feasible upper masses11.998960@3.96 and12.248227@3.97. Subtracting upper bounds does not lower-bound growth; a constant11.9 meets all quoted bounds, including lower10.845594 at3.97. A secant also gives no local derivative bound. Withdraw endpoint or explicitly qualify heuristic and assumptions. Source record and independent counter-review confirm error; actual s12>=3.96 and s11>=3.81 certificates unaffected. Full review /tmp/squares-core-review-2026-09-06/review.md.
