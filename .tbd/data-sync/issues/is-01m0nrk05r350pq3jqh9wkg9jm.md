---
type: is
id: is-01m0nrk05r350pq3jqh9wkg9jm
title: Machine-verify existing unavoidable point sets
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0nrjz7jn0q1ktm5n7bhxbwm
created_at: 2026-08-22T22:13:46.808Z
updated_at: 2026-10-06T08:32:30.584Z
closed_at: 2026-10-06T08:32:30.584Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Published unavoidable sets are machine-checked on origin/main: E-bentz46-theorem8-audit (session-060, BC-106) certifies Bentz's Theorem 8 set exactly as printed; devtools/check_green_ds7.py decides Friedman DS7 Figure 34's sets for k = 2..17
resolution: null
duplicate_of: null
---
'Does every unit square in [0,k]^2 contain a point of P?' is a decision problem in three parameters (x, y, theta) -- well inside interval branch-and-bound or an SMT solver with nonlinear arithmetic. Every published lower bound in this subject rests on such sets, checked only by referees with pencils. Nobody has ever machine-checked one. This is the cheapest entry into the proof lane, where nothing automated has ever run.
