# Correction: the stacking capacity bound in lane X3’s box sweep is false

Dated correction, 2026-09-10, attached to the retained artifact
[`lane-x3-box-sweep.py.txt`](lane-x3-box-sweep.py.txt) and to
[lane X3](lane-x3-containment-atoms-do-not-cut.md).
The artifact’s bytes are as delivered and were not edited; this document is the
correction. Raised as finding R4 of the PR 139 review and re-derived here.

## The false claim

The module docstring (lines 4-9) and `capacity` (line 35) use two upper bounds on the
number of pairwise-disjoint closed `B`-squares that fit inside an `a x b` box:

- the **area** bound `floor(a*b / B^2)`, which is valid;
- a **stacking** bound, `if min(a, b) < 2B then floor(max(a, b) / B)`, with the stated
  reason that “no two contained cores sit side by side across the short side, so they
  stack along the long side and each has extent `>= B` there”.

**The stacking bound is false for rotated squares.** Its reason silently assumes each
core’s extent along the long side is at least `B` *and* that cores cannot interleave
across the short side.
A square rotated by 45 degrees has extent `B*sqrt(2)` across both axes, so two of them
can sit at different heights, overlap in their projections onto the long side, and still
be disjoint.

## The counterexample, re-derived exactly

Take `B = 1` and the box `a = 199/100` by `b = 79/20`, so `min(a, b) = 1.99 < 2B = 2`
and the stacking bound fires.
Place four unit squares at 45 degrees with centres

```
(a0, a0), (w - a0, a0 + d), (a0, a0 + 2d), (w - a0, a0 + 3d)
    where  w = 199/100,  a0 = sqrt(2)/2,  d = 2*sqrt(2) - w + 1/1000
```

Two squares at 45 degrees and side `B` are disjoint exactly when the `L1` distance
between their centres is at least `B*sqrt(2)`. Computed at 60 significant digits:

| reading | value |
| --- | --- |
| minimum `L1` centre separation over all six pairs | `1.415213562373095048801688724209698078569671875376948073176680` |
| required `B*sqrt(2)` | `1.414213562373095048801688724209698078569671875376948073176680` |
| slack | exactly `0.001` |
| width used | exactly `1.99` |
| height used | `3.932494936611665341611821069467886549987703127638636512236760` |

All four are strictly disjoint, the width used is exactly `a`, and the height used is
below `b = 3.95`. So four fit.

`capacity(199/100, 79/20, 1)` returns `min(7, 3) = 3`.

## What still stands, and why

**Both recorded observations, C1 and C2, still stand**, and the reason matters rather
than being a formality: an **understated** capacity makes a violation *easier* to find,
not harder.
The sweep looked for a box whose family weight exceeds its capacity bound and
found none. Under the false, too-small stacking bound it found no exceedance; under the
true capacity, which is at least as large everywhere the stacking bound fired, there is
no exceedance either.
The negative result is therefore valid under the weaker **area** bound alone, which is
the bound that survives.

`T-024`, `T-025` and `T-026` do not use this formula, and neither does any other
retained instrument: the function is local to
[`lane-x3-box-sweep.py.txt`](lane-x3-box-sweep.py.txt).

## What must not be inferred from it

A capacity bound that is wrong in the *lenient* direction cannot be used to claim a
containment atom is *valid*. If anyone rebuilds the sweep to propose containment atoms
rather than to look for violations, the stacking branch has to go, or be replaced by a
bound proved for rotated cores.
Delete the branch and the sweep is sound as an exceedance search on the area bound
alone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
