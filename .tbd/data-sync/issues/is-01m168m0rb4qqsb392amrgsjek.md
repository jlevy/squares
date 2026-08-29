---
type: is
id: is-01m168m0rb4qqsb392amrgsjek
title: Eliminate the five-unknown system for the n=29 minimal polynomial
kind: task
status: open
priority: 0
version: 5
labels: []
dependencies: []
created_at: 2026-08-29T08:01:48.299Z
updated_at: 2026-08-29T10:09:57.466Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
BC-060's exit named two routes — elimination via SymPy, and integer relation via mpmath pslq — and only the second was built. It refused: no relation through degree 20 below 1e22 at 1000 digits. A symbolic build of the Kingbird system, rationalised by the half-angle substitution u = tan(theta/2), gives per-equation total degrees [11, 20, 23, 22, 19, 6] in {s, u_a, u_b, u_c, u_d, u_i} and a Bezout bound of 12,690,480 on the solution variety — so degree 20 was a corner of the space, not a survey of it. Build the symbolic system as a retained artifact, tighten the bound with a BKK/mixed-volume computation, and attempt resultant or Groebner elimination of the five angle unknowns to get the eliminant in s exactly. A refusal is a result: it would say the exact-algebraic route is out of reach at n=29 and the interval route is what carries the bound.

## Notes

BC-066 closed in session-044: a measured wall, not an eliminant.

Three msolve runs on the six-equation system with s ordered last, each from a
guarded export that re-parses its own text:

1. char 0, ELIM(5): OOM-killed at degree 32 after 25m09s, 13.8 GB anon-RSS.
   Completed degree 31 on a 656126 x 1670545 matrix in 382.84s.
2. char 1073741827, ELIM(5): identical matrix dimensions degree for degree, at
   about 70% of the memory.
3. char 1073741827, grevlex: largest matrix 20611 x 49890, 2.7 GB, pair list
   grew monotonically to 21,661, no basis inside a 25-minute cap.

Neither predicted failure mode stopped it. Coefficient swell is impossible over
F_p and the cheapest order did not terminate either, so what the runs measure is
the size of the ideal rather than the arithmetic carried through it.

Scope: a measurement on 2 threads and 15 GB, not a proof of intractability.
Nothing here moves any bound.

Next on this bead: the degree of the projection to the s-axis by homotopy
continuation, which needs no basis at all and would turn BC-060's blind sweep
into a targeted search at a known degree.
