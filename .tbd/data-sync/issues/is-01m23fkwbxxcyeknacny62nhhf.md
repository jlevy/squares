---
type: is
id: is-01m23fkwbxxcyeknacny62nhhf
title: Certificate format cannot express K5 and K6 atoms the reader separates
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T16:22:02.365Z
updated_at: 2026-09-09T16:22:02.365Z
---
The plateau reader separates cut families that the certificate format cannot express, and
that is now the blocker on turning any separation work into a bound.

Measured 2026-09-09 in agenda-033 lane A4
(packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-a4-separating-the-plateau-dual-at-153-40.md,
finding P10), confirmed by lane A5's sharpening loop
(.../lane-a5-the-fixed-support-maximum-under-the-atom-classes.md, F6).

The freeze path writes `atoms` (point atoms) and `threshold_atoms`
(`ThresholdAtom.to_record()`), and `devtools.decide_threshold_certificate` parses exactly
those. A `ThresholdAtom` is `(S, k, w)`: it charges `w` to every core holding at least `k`
points of a finite set `S`, one unit per core.

Two of the three cut families the reader can separate do not fit in it:

- A K5 budget-one clique atom carries INTEGER MULTIPLICITIES. The one A4 returned is
  `a = (1, 2, 2, 1, 1)` at `t = 4`, `a(S) = 7`, budget `floor(7/4) = 1`, floor charge
  `3/2` against this dual -- violation `1/2`, the hardest small cut found, charging all 42
  members of the heaviest rank-one clique.
- A K6 Chvatal-Gomory floor atom charges `floor(a(P)/t)`, which EXCEEDS ONE on some cores.
  A4 returned five of them, at violations `1109/200` through `827/100`, each using
  multiplicity `t-1` on most of its points. A5 separated seventeen more in its sharpening
  loop, which is what takes the fixed-support optimum from `32/3` to exactly `10`.

So neither can be frozen into a certificate today even when it does cut. A4 states the
consequence plainly: had the LP value dropped on a K5 or K6 column, the freeze-and-gate
step its brief specified would have had nothing to write. Every future run of the loop
that finds its best cut outside two-of-three hits the same wall.

The validity argument is already written down and is one line: for disjoint cores,
`sum_P floor(a(P)/t) <= floor(a(S)/t)`, because the floor is superadditive and disjoint
cores have disjoint traces on `S`. A4's LP driver already prices such a column correctly
-- coefficient `sum_images floor(a(P)/t)`, cost `|orbit| * floor(a(S)/t)`, the orbit's
budget -- so the pricing question is settled and only the record format and the two gate
routes are missing.

What to build:

1. Generalise the frozen atom record from `(S, k, w)` to `(S, a, t, w)` with integer
   multiplicities and an explicit threshold, keeping `ThresholdAtom` as the special case
   `a = 1, t = k` so every frozen certificate in the tree still reads. The charge is
   `w * floor(a(P)/t)` and the budget contribution `w * floor(a(S)/t)`.
2. Teach both routes of the gate to decide it: the exact event-cell sweep and the interval
   branch and bound. They must still fail differently -- that is the point of having two.
3. A control that refuses a record whose declared budget disagrees with
   `floor(a(S)/t)` recomputed from its own `a` and `t`, since a wrong budget is the one
   error that would make an unsound certificate look accepted.
4. Re-decide the frozen T-025 and T-026 certificates through the generalised path and
   confirm byte-identical verdicts, as the migration control.

This is X-024 slice E1 in substance, but its motivation is now unconditional: the
conditional line it was originally scoped for is closed (lane X1, H-146's disposition).
