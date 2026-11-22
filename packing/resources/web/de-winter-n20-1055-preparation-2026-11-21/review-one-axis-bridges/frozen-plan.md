# Frozen Plan: Independent One-Axis Bridge Exclusions

This slice tests all 3,488 excluded local bridge profiles in the one-axis theorem of
issue #1055 for `0 < tan(theta/2) <= 1/24`. A profile is a five-tile chain whose four
forward separating-axis relations hold, crossing five consecutive ranks with exactly one
transverse step of plus or minus one.
It is a local implication, not a proof that every packing has a particular chain.

The previously
[accepted 576-certificate bank](../n20-one-axis-bank-independent-20261122/README.md) is
a separate later obligation.
This bridge check does not need that bank as a premise.
It must not be presented as completing the theorem: global sign, vacancy/symmetry and
separation-graph coverage remain open.

The reviewer has already read the producer’s proof statements and implementations of the
path bound and polynomial verifier.
This is an independent implementation with disclosed exposure, not a blind review.
No contributor program will run.

## Exact Roster and Source Binding

The immutable [specification](bridge-spec.json) binds the original source archive,
statement and path-formula texts by their retained hashes.
Its source pin is `dad9c3fd3443bcb9f8950bc302445bdf1e3fbbcc`. The checker will enumerate
rank tuples independently from all `range(5)^5` tuples, selecting exactly one nonzero
consecutive difference of magnitude one.
There are 32 selected rank profiles.
It will independently enumerate `(-1,0,1)^5` and retain at most one zero, giving 112
sign profiles.

The 3,584 distinct combinations are classified by the integer cost: absolute endpoint
signs, plus absolute sign differences on straight steps, minus `h(a+b)` on the diagonal
step. Exactly 96 have zero cost; these are not claimed feasible, and this slice does not
exclude them. Exactly 3,488 have positive cost: 992 with no zero on the chain and 2,496
with one zero. A zero-free chain can occur in the one-axis theorem when the aligned tile
lies elsewhere.

The checker also compares zero cost with the geometric arm condition: signs point toward
the diagonal and their magnitudes are nondecreasing along each arm from its board wall.
This binds the independently enumerated exclusion roster to the statement’s exact
intended scope.

A canonical digest of all 3,584 profiles, all excluded profiles with their full
normal-choice roster, and all 96 untested zero-cost profiles will be retained.
The output cannot pass from counts alone: every required normal choice of every
positive-cost profile must receive a continuum proof.
The half-tangent parameter and all roster dimensions are fixed by the immutable input.

## Exact Bound

Put `c = cos(theta)`, `s = sin(theta)`, `u = c+s`, `d = u(u-1)`, and `H = (1+u)/2`. An
aligned tile has board-axis width one; a tilted tile has width `u`. The two endpoint
walls contribute half the sum of their widths.
For a step with transverse displacement `y`, the forward displacement obeys
`x >= A - lambda tan(theta) y`, with these exhaustive choices under the
forward-separation premise:

| Signs and transverse step h | A | lambda |
| --- | --- | --- |
| Equal nonzero signs a | `1/c` | `a` |
| Opposite nonzero signs, diagonal | `u` | `h` |
| Opposite nonzero signs, straight | `u` | Either `-1` or `1` |
| Mixed aligned/tilted, favorable diagonal | `H/c` | The nonzero sign |
| Mixed aligned/tilted, unfavorable diagonal | `H` | `0` |
| Mixed aligned/tilted, straight | Either `H` or `H/c` | Respectively `0` or the nonzero sign |

The favorable mixed reduction also requires `1-5d > Ht`, where `t = tan(theta/2)`. The
checker independently certifies this prerequisite on the whole interval `[0,1/24]`,
using the polynomial obtained after multiplication by `2(1+t²)²`. The analytic rank and
forward-axis premises are those already read in the restricted-statement review; this
slice does not regenerate those global premises.
The vertical case is covered by expressing signs in the chain’s forward/transverse
frame; all sign tuples are present, including their simultaneous negations.

For transverse rank `r[j]`, write the coordinate error as `d * eta[j]`, where
`-r[j] <= eta[j] <= 4-r[j]`. For each normal choice, compute `J = sum(lambda[i] h[i])`.
Instead of using the producer’s coefficient shortcut, enumerate all 32 endpoint vertices
of this five-variable box to compute the exact integer maximum
`K = max sum(lambda[i](eta[i+1]-eta[i]))`. The physical span is bounded below by

`endpoint_widths/2 + sum(A) - (s/c)(J + dK)`.

Require this to be at least five for every normal choice.
There are at most eight normal choices per single-jump profile.
Multiplying the difference from five by `2(1-t²)(1+t²)²`, positive throughout the stated
interval, yields a polynomial of degree at most six.

The checker obtains that polynomial by exact rational interpolation at seven points
`0,1/8,...,6/8` from the physical formula, and checks it at the eighth point `7/8`.
These points are algebraic probes; no geometric assertion outside the target interval is
used.
The known degree bound follows by substituting the rational half-angle formulas and
clearing the displayed denominator.
Normalized rational Bernstein coefficients certify nonnegativity on `[0,1/24]`. The
prerequisite uses strict positivity, including both endpoints.
This reuses the independently implemented arithmetic method of the accepted bank
checker, with no producer arithmetic or source-module imports.

## Twelve Predeclared Controls

Six expected acceptances:

1. Exact interpolation reconstructs `2-3t+5t²-7t³+11t⁶`.
2. The zero polynomial is an admissible nonnegative path bound.
3. The all-negative normal tuple on ranks `(0,0,0,0,1)` has box maximum `K=5`.
4. Normal tuple `(1,-1,1,-1)` on those ranks has `K=17`.
5. The all-negative sign profile on those ranks is excluded by its physical span bound.
6. The original favorable mixed-diagonal prerequisite is strictly positive.

Six expected refusals:

1. A negative constant path bound.
2. `1-48t`, whose right endpoint is negative.
3. `t-24t²` as a strict prerequisite, because its endpoints vanish.
4. Raising the board threshold in the accepted baseline from five to six.
5. Adding one to the interpolated baseline’s constant coefficient while keeping its
   physical formula.
6. Negating the favorable mixed-diagonal prerequisite.

A control mismatch, failed local profile, incomplete branch count, wrong input digest or
unexpected exception fails the run.
The output is published only after all controls and every required profile pass.
The receipt includes exact bound polynomials and Bernstein evidence, with shared
polynomial records referenced by each branch.

## Execution Boundary

Preparation only. No checker execution, import, compile or syntax check before the
coordinator offers the memory-guard serial slot.

Proposed run: one project Python 3.14.7 worker with `-I -B`, standard library only,
external scratch/cache directories, no network, project/source imports or geometry
beyond these local formulas.
Target under 20 wall seconds and 0.10 GiB peak RSS; hard stop at 60 wall seconds, 0.25
GiB sampled process-tree footprint or pressure level 2. Retain the guard journal and
worker result independently.

No checkout, branch, tracker or GitHub writes are in scope.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
