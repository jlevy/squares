# Agenda 034, lane X3: containment atoms on the plateau families, two negatives

Retained measurement-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by the
coordinator on 2026-09-09, read-only on the repository at
`claude/n-11-stronger-result-d730ds`. The report is reproduced as delivered, with its
own findings table and status labels.
Its file references were rewritten to say where each file now is, and the correction
below governs the historical body.
X-024 carries the coordinator’s reading.

> **Correction, added 2026-09-10.** The stacking rule used by
> [`lane-x3-box-sweep.py.txt`](lane-x3-box-sweep.py.txt),
> `min(a,b) < 2B => capacity <= floor(max(a,b)/B)`, is false for rotated squares.
> For a strict counterexample, set `B = 1`, `w = 199/100`, `epsilon = 1/1000`,
> `a = sqrt(2)/2`, and `d = 2 sqrt(2) - w + epsilon`. Four 45-degree squares centred at
> `(a,a)`, `(w-a,a+d)`, `(a,a+2d)`, and `(w-a,a+3d)` are strictly disjoint: adjacent
> centres have L1 separation `sqrt(2) + epsilon`, centres two steps apart have
> separation `2d > sqrt(2)`, and the remaining pair is farther apart.
> They fit in a rectangle of width `199/100` and height `7 sqrt(2) - 5967/1000 < 79/20`,
> although the helper returns capacity three for `(199/100, 79/20, 1)`.

> The area bound `floor(ab/B^2)` remains valid.
> The recorded grid weights stay below that valid bound, so the finite no-exceedance
> observations survive at their measured scope: the specified eight-step boxes, strip
> widths, and two retained families.
> They do not decide arbitrary off-grid boxes, other convex regions, or other placement
> families. Claims that the strip capacity is exactly three, that the tested families
> saturate a general stacking theorem, or that containment atoms are closed as a route
> are withdrawn.

> The retained `.py.txt` helper preserves the original measurement record.
> Its stacking branch is invalid and the file is unfit for reuse or promotion.

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
So a violated containment atom would be a cut outside
[lane T2](lane-t2-cap-and-next-cuts.md)’s `3.868983` bracket, which is why it was worth
testing first.

## What was measured

> **Current scope.** In the historical description below, only the area capacity is a
> proved general bound.
> The stacking capacity and conclusions that depend on its tightness are superseded by
> the correction above.

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

> **Current interpretation.** The screen is a finite negative result on the stated grid
> and families. It does not close containment cuts as a class.

**Closed: containment atoms on wall strips and axis-aligned boxes are not the missing
cut. Do not build them.**

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
`10` once the floor atoms are imposed — so the ceiling support does not reach eleven
under the atom inequalities and **caps neither side**. The barrier is not this family,
and it is not containment atoms either.

## Files

Retained beside this report:

- [`lane-x3-strip-profile.py.txt`](lane-x3-strip-profile.py.txt) — wall-strip weight as
  an exact function of strip width, for both families.
- [`lane-x3-box-sweep.py.txt`](lane-x3-box-sweep.py.txt) — the retained historical
  eight-step box sweep.
  Its stacking branch is invalid and must not be reused; the area-bound comparisons
  remain interpretable.

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
