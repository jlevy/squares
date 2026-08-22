---
type: is
id: is-01m0n7mjghkb7qhbf6972zsfcw
title: Document symbolic/analytic optimisation of packings
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0n7mkg9c5ay1x8mza9z88wx
parent_id: is-01m0n7ka0xjff91yctt25c4m1y
created_at: 2026-08-22T17:17:32.560Z
updated_at: 2026-08-22T17:53:11.113Z
closed_at: 2026-08-22T17:53:11.113Z
close_reason: "Recorded in docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md. Key results: the record engine is a closed-source GPU simulated annealer (Schadt/Ellsworth, RTX 3080 Ti, 65536 threads) with published basin statistics; no open-source tool targets this problem, and the nesting ecosystem (jagua-rs, sparrow, packingsolver) has the wrong objective and tolerance regime; SCIP 10 / FICO Xpress with a Farkas-lemma non-overlap model match the records only to about n=16; symbolic refinement runs on contact equations plus a Jacobian-determinant constraint and RootApproximant recovery, giving minimal polynomials up to degree 62; and no square-in-square bound has ever been proved with computer assistance, the only rigorous computer-assisted result for rotatable unit squares being three squares in a circle (Montanher et al. 2018)."
---
Contact equations, the Jacobian-determinant constraint for underdetermined systems, RootApproximant/PSLQ numeric-to-symbolic recovery, Groebner/resultant elimination, and the resulting minimal polynomials for s(n).
