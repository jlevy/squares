# Agenda 034, lane X3: containment atoms on the plateau families, two negatives

Retained measurement-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by the
coordinator on 2026-09-09, read-only on the repository at
`claude/n-11-stronger-result-d730ds`. The report is reproduced as delivered, with its
own findings table and status labels; only its file references were rewritten to say
where each file now is.
X-024 carries the coordinator’s reading.

Prompted by [lane A3](lane-a3-threshold-loop-at-383-100.md)’s site-separation addendum
(S2/S4): the plateau excess retreats into a `0.0006`-wide sliver of interleaved
near-axis wall squares, so vertex-by-vertex site separation cannot close it.
The question asked here is whether a *containment* atom closes it instead.

Retained beside this report: the two sweep scripts, listed under [Files](#files).
Not retained (scratch only): the per-width strip profiles and the box sweep’s full grid
output, both rebuildable in seconds by the retained scripts.

Labels: **EXACT** = a rational decision by repository primitives; **Reading** = an
interpretation of the exact numbers, not itself decided.

## The atom class tested

A **containment atom** `(R, c, w)` charges `w` to every core contained in the region `R`
and contributes `c * w` to the budget, where `c` is a proved upper bound on the number
of pairwise-disjoint cores that fit inside `R`. On the dual side it is the valid packing
inequality `y({P : P subset R}) <= c`. It is **not** in the rank-one threshold language:
a threshold atom charges a core for *containing* points of a finite set, and “contained
in `R`” is not expressible that way.
It was tested first on the belief that a violated containment atom would be a cut
outside [lane T2](lane-t2-cap-and-next-cuts.md)’s `3.868983` bracket.
**That belief is withdrawn, 2026-09-10 (PR 139 finding R5).** The bracket is witnessed
by an actual packing of eleven pairwise-disjoint integral `B`-cores, and **every valid
packing-capacity inequality holds on such a packing** — a containment atom included,
since its whole content is a capacity `c` on a region `R`. Being outside the rank-one
*syntax* buys nothing against an obstruction that is a witness rather than a language
restriction. The class was still worth testing, on the ordinary ground that it is cheap
and expresses something the point atoms do not; it was never a way past the bracket.

## What was measured

Two families at `L = 153/40 = 3.825`, both of total weight exactly 11:

- the `191/50` point-method ceiling family
  ([`ceiling-family-191-50.json`](ceiling-family-191-50.json)) under the homothety,
  **verified depth-one** (lane A3 addendum S3), so a genuine fractional packing.
- the `1/25`-integral plateau dual after one round of site separation
  ([`lane-a3-family-153-40-sites-round1-exact25.json`](lane-a3-family-153-40-sites-round1-exact25.json)),
  280 placements, exact maximum depth `28/25` (lane A3 addendum S2).

Scripts: [`lane-x3-strip-profile.py.txt`](lane-x3-strip-profile.py.txt) (wall-strip
weight as an exact function of strip width) and
[`lane-x3-box-sweep.py.txt`](lane-x3-box-sweep.py.txt) (every axis-aligned box on an
8-step grid, against two valid capacity bounds: the area bound `floor(a*b/B^2)` and,
when `min(a,b) < 2B`, the stacking bound `floor(max(a,b)/B)`). All arithmetic in
`Fraction`.

## Findings

| # | Finding | Status |
| --- | --- | --- |
| C1 | **Wall strips are tight, not violated.** For every strip width from about `1.1` (ceiling family) or `1.5` (plateau family) up to just below `2B = 1.99540`, both families carry **exactly 3** in each wall strip, against a capacity of exactly 3. The weight first exceeds 3 at width `1.997393` (ceiling) and `1.997119` (plateau) — both immediately above `2B`, where a second column of cores becomes geometrically possible and the capacity rises. The families saturate the bound and never break it. | EXACT |
| C2 | **No axis-aligned box violates its capacity.** Over every box with corners on the 8-step grid of `[0, 153/40]^2`, for both families, no box carries more weight than the capacity bound allows. | EXACT on that grid |
| C3 | Reading: the plateau families are geometrically sane in the containment sense. Their infeasibility is purely **local depth excess in slivers**, which containment atoms on convex axis-aligned regions cannot see. A containment atom would have to be violated to cut, and none is. | Reading |
| C4 | The saturation in C1 is itself structural: both families are “three per wall column” objects, and the jump at exactly `2B` says the LP is finding extreme points that respect the side-by-side geometry to the digit. That is evidence the value 11 at `3.825` reflects the geometry rather than a sampling artefact, though it is not a proof: the ceiling family is a valid depth-one witness at `3.825` and at `383/100` (lane A3 S3) but its two-of-three maximum is `5/4`, so it caps the point method at both sides and caps nothing for the threshold method. | Reading |

## What this closes and what it leaves open

**Negative, at the scope tested: containment atoms on wall strips and on axis-aligned
boxes over an eight-step grid are not the missing cut on these two families.
Do not build them.**

**Scope note, 2026-09-10 (PR 139 finding R5).** What was tested, stated beside the
verdict rather than left to be inferred: two families at `L = 153/40` — the `191/50`
point-method ceiling family under the homothety and the `1/25`-integral plateau dual
after one round of site separation — against two region families, wall strips swept in
width and axis-aligned boxes with corners on an eight-step grid of `[0, 153/40]^2`,
under two capacity bounds.
Other regions, other grids, other families and other capacity bounds are unmeasured.
A finite negative on that surface is not a closure of the containment class, and C3
should be read as an expectation about where the next cut is *not* rather than as a
theorem.

**One of the two capacity bounds is also false**, and its correction is attached as
[`lane-x3-box-sweep-capacity-correction.md`](lane-x3-box-sweep-capacity-correction.md):
the stacking bound `min(a, b) < 2B => capacity <= floor(max(a, b)/B)` fails for rotated
squares, with an exact four-square counterexample at `B = 1` in a `199/100` by `79/20`
box. C1 and C2 survive it, because an understated capacity makes a violation easier to
find rather than harder, so finding none under it means none under the true capacity;
the negative stands on the area bound alone.

Open, and unchanged by this: whether a depth-one family of weight 11 at `3.825` exists
whose two-of-three maximum is at most 1. That family, if it exists, caps the threshold
method at `3.825`; if none exists, the method has room and the barrier is only the cost
of column generation.
Neither the restricted dual (value 11, but depth `28/25`, so not a valid witness) nor
the scaled ceiling family (valid, but two-of-three maximum `5/4`, so cut) settles it.

That open question was then measured from the other side and the answer is the second
one. [Lane A5](lane-a5-the-fixed-support-maximum-under-the-atom-classes.md) reads the
fixed-support maximum on the ceiling support under depth-one plus the complete
budget-one class as exactly `32/3` at both `153/40` and `383/100`, falling to exactly
`10` once the floor atoms are imposed — so **that support** does not reach eleven under
the atom inequalities.
Read at its own scope (2026-09-10, R5): an optimum below eleven on **one fixed support**
does not settle whether some other support reaches eleven, which is what a cap would
need, and A5’s own F4 and F6 say so.
The barrier is not this family, and it is not containment atoms either.

## Files

Retained beside this report:

- [`lane-x3-strip-profile.py.txt`](lane-x3-strip-profile.py.txt) — wall-strip weight as
  an exact function of strip width, for both families.
- [`lane-x3-box-sweep.py.txt`](lane-x3-box-sweep.py.txt) — every axis-aligned box on the
  8-step grid against the two capacity bounds.
- [`lane-x3-box-sweep-capacity-correction.md`](lane-x3-box-sweep-capacity-correction.md)
  — the dated correction to the second of those two bounds, with the exact
  counterexample. The script’s bytes are as delivered; the correction is attached beside
  it rather than edited into it.

Both scripts are retained with a `.py.txt` extension, as
`agenda-032/unrun-independent-audit/` already does: they are scratch measurement
scripts, not importable project modules, and the repository’s Python surface is held at
zero Ruff and BasedPyright findings over every tracked `.py` file.
Their bytes are as delivered; nothing was reformatted.

Not retained (scratch only): the per-width strip profile tables and the box sweep’s full
grid output. Both rebuild in seconds from the two families already in this directory.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
