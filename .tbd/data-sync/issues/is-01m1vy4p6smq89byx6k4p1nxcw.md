---
type: is
id: is-01m1vy4p6smq89byx6k4p1nxcw
title: Withdraw unsupported n12 covering-value slope and ladder endpoint inference
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T18:01:57.720Z
updated_at: 2026-09-06T18:01:57.720Z
---
At edccf294, covering-values.yaml654-661 and CERTIFICATE-REACH64 infer slope>=24.9 and endpoint3.96004 from two feasible upper masses11.998960@3.96 and12.248227@3.97. Subtracting upper bounds does not lower-bound growth; a constant11.9 meets all quoted bounds, including lower10.845594 at3.97. A secant also gives no local derivative bound. Withdraw endpoint or explicitly qualify heuristic and assumptions. Source record and independent counter-review confirm error; actual s12>=3.96 and s11>=3.81 certificates unaffected. Full review /tmp/squares-core-review-2026-09-06/review.md.
