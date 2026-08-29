---
type: is
id: is-01m168m0rb4qqsb392amrgsjek
title: Eliminate the five-unknown system for the n=29 minimal polynomial
kind: task
status: open
priority: 0
version: 4
labels: []
dependencies: []
created_at: 2026-08-29T08:01:48.299Z
updated_at: 2026-08-29T08:12:35.593Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
BC-060's exit named two routes — elimination via SymPy, and integer relation via mpmath pslq — and only the second was built. It refused: no relation through degree 20 below 1e22 at 1000 digits. A symbolic build of the Kingbird system, rationalised by the half-angle substitution u = tan(theta/2), gives per-equation total degrees [11, 20, 23, 22, 19, 6] in {s, u_a, u_b, u_c, u_d, u_i} and a Bezout bound of 12,690,480 on the solution variety — so degree 20 was a corner of the space, not a survey of it. Build the symbolic system as a retained artifact, tighten the bound with a BKK/mixed-volume computation, and attempt resultant or Groebner elimination of the five angle unknowns to get the eliminant in s exactly. A refusal is a result: it would say the exact-algebraic route is out of reach at n=29 and the interval route is what carries the bound.

## Notes

DONE in session-043 — the degree bound. Under u = tan(theta/2) the published system
rationalises over Q into six polynomials with total degrees [11, 15, 10, 15, 7, 6],
giving a Bezout bound of 1,039,500 on the solution variety. So the integer-relation
refusal through degree twenty surveyed a corner of the space, not the space. Every
equation is degree 1 in s, and solving the smallest for s gives it as a rational
function of u_b and u_c alone. Tool: devtools/probe_system_degree.py --eliminate-side.

REMAINING — the elimination itself. Five equations in five unknowns
(u_a, u_b, u_c, u_d, u_i) with total degrees [16, 20, 15, 20, 12]. Attempt a resultant
chain or Groebner basis to get the eliminant in s exactly. This is where the
exact-algebraic route either succeeds or is shown out of reach at n = 29, and a refusal
is a result: it would confirm that the interval route is what carries the n = 29 bound.
Needs its own budget — a five-variable resultant chain at these degrees can blow up, so
the block should declare a wall-clock cap and report what it reached.
