# Frozen Plan: Independent General Five-Tile Path Catalogue

This slice reconstructs the additional local exclusions used by the one-axis source’s
`--Q 24 --exact-paths` graph pruning.
It covers all five-tile forward chains with zero to four transverse rank jumps.
It will classify every local profile and retain exact evidence for every normal choice.
It will not enumerate global separation graphs or connect those graphs to the polynomial
bank.

The checker has not been executed, imported, compiled or syntax-checked.
Execution requires the coordinator’s serial memory-guard slot.

## Source, Exposure and Reuse

The [immutable specification](general-path-spec.json), SHA-256
`73e09d72fa3094ee6e5eecb743428b3a3edb7ae20b3e1af598466fc662910a12`, binds the stronger
issue #1055 attachment and the exact source members read.
The source pin is `dad9c3fd3443bcb9f8950bc302445bdf1e3fbbcc`, with archive SHA-256
`475d7ef50e21ce4a83cfb4c8415c9e9852d619beeade5c4c8745c2c963d6c867`.

The reviewer has read the producer’s proof, path generator, path bounds and positivity
implementation. This is not a blind review.
The arithmetic, physical-span and local step-option functions are copied as source text
from the earlier first-party independent bridge checker, SHA-256
`05be38c984078df7fc17c0444a4981c756d166b3f83743035a1ac88d6979eb16`. They are
independently implemented relative to the producer, but this slice is not a second
implementation independent of that bridge arithmetic.
No producer module will be imported or executed.

## Exact Geometric Premises

Let `0 < t = tan(theta/2) <= 1/24`, `c = cos(theta)`, `s = sin(theta)`, `u = c+s`,
`d = u(u-1)`, and `H = (1+u)/2`. The target is a strict board `S < 5`, with nineteen
independently signed tilts of magnitude theta and one aligned tile.

A local chain contains one tile at each consecutive forward rank 0 through 4. Its
transverse ranks `r[0],...,r[4]` lie in 0 through 4, with adjacent differences in
`{-1,0,1}`. Its five tilt signs lie in `{-1,0,1}`, with at most one zero.
The aligned tile may instead lie outside the chain.

Each of the four pairs must have a separating normal in the chain’s forward direction.
The reviewed near-grid reduction supplies transverse errors `d*eta[j]`, with
`-r[j] <= eta[j] <= 4-r[j]`. A vertical chain is expressed in the rotated frame with
forward coordinate y and transverse rank `4-x`; tilt signs are unchanged by that
quarter-turn.

For each pair the forward displacement is at least `A - lambda*(s/c)*dy`:

| Pair and transverse step h | A | lambda |
| --- | --- | --- |
| Equal nonzero sign a | `1/c` | `a` |
| Opposite nonzero signs, diagonal | `u` | `h` |
| Opposite nonzero signs, straight | `u` | Each of `-1,+1` |
| Aligned/tilted, favorable diagonal | `H/c` | Nonzero tilt sign |
| Aligned/tilted, unfavorable diagonal | `H` | `0` |
| Aligned/tilted, straight | `H` or `H/c` | Respectively `0` or nonzero tilt sign |

The favorable mixed step needs `1-5d > Ht`. The checker re-establishes it on the whole
closed interval `[0,1/24]`, from its degree-four polynomial after multiplication by
`2(1+t²)²`, with strictly positive endpoint Bernstein coefficients and no negative
coefficient.

No additional geometric theorem is needed when the number of transverse jumps changes:
each pair obeys the same local alternatives and the four displacements telescope.
The global assertion that every relevant graph supplies these forward chains remains
outside this local calculation.

## Finite Coverage

Enumerate all `range(5)^5` tuples and retain adjacent differences of absolute value at
most one. Independently generate the same tuples by extending walks one rank at a time;
require identical sets.

| Transverse jumps | Rank profiles | Rank/sign profiles |
| ---: | ---: | ---: |
| 0 | 5 | 560 |
| 1 | 32 | 3,584 |
| 2 | 84 | 9,408 |
| 3 | 96 | 10,752 |
| 4 | 42 | 4,704 |
| Total | 259 | 29,008 |

The sign roster has 32 zero-free vectors and 80 vectors with exactly one zero.
Construct it both by filtering `(-1,0,1)^5` and by inserting a zero into all four-sign
vectors; require agreement and a total of 112.

This is a complete local superset.
Some profiles cannot occur for a particular vacancy permutation; keeping them is
harmless.
Applying the catalogue to particular occupied-cell paths is a later obligation.

For each profile, enumerate the entire Cartesian product of its four pair-option lists,
with no early return on a failed bound.
At most four straight pairs can have two options, hence at most sixteen choices per
profile and 464,128 choices as a conservative total ceiling.
The specification fixes their traversal order.
The receipt retains one physical-bound record identifier per choice, as well as every
failed choice index.

As a regression against the accepted bridge slice, all 3,488 positive-cost single-jump
profiles must be excluded through exactly 15,696 normal choices.
The other exclusion counts are not prescribed.
They must be derived and reported, rather than guessed from the producer’s global graph
totals.

## Polynomial and Exclusion Criterion

For a normal choice, set `J = sum(lambda[i]*h[i])`. Independently maximize
`sum(lambda[i]*(eta[i+1]-eta[i]))` over all 32 vertices of the five-variable rank-error
box to obtain the exact integer K. The lower bound on total span is

`(left_width+right_width)/2 + sum(A) - (s/c)*(J+d*K)`.

Multiply its difference from five by `2(1-t²)(1+t²)²`. This factor is positive on the
target interval because `1-t² >= 575/576 > 0`. Substituting the rational half-angle
formula produces a polynomial of degree at most six: secant terms become multiples of
`(1+t²)^3`; width/support terms have degree at most six; the projection/rank-error terms
have degree at most five.

Recover each distinct physical bound by exact rational interpolation at `0,1/8,...,6/8`,
and check its identity at those points plus `7/8`. The degree bound comes from the
displayed algebra, not from sampling.
The interpolation points outside the geometric interval are algebraic probes.

Compute normalized degree-d Bernstein coefficients on `[0,1/24]`:

`beta[k] = sum(p[i]*binomial(k,i)/(24^i*binomial(d,i)), i=0..k)`.

All coefficients nonnegative imply span at least five for that normal choice.
A profile is excluded only if every possible choice passes.
That weak span inequality strictly contradicts `S < 5`; a strictly positive polynomial
is unnecessary, and an identically zero bound is sufficient.
The scalar bounds include t=0; the global positive-angle reduction and the fully aligned
endpoint remain distinguished.

The producer’s trimmed-degree integer Bernstein coefficient equals
`24^d*binomial(d,k)*beta[k]`, a positive multiple.
Its local non-strict test therefore has the same mathematical predicate.
Trailing zero coefficients are removed by both representations; a zero polynomial passes
both. This equivalence is an algebraic reading of the source, not a run of its program.

If any choice has a negative Bernstein coefficient, the profile is recorded as
`not-certified-by-this-Bernstein-test`. This does not prove the polynomial negative
somewhere and does not assert a feasible geometric placement.
The full bound polynomials and their exact coefficients remain in the receipt.

## Twenty Predeclared Controls

The first twelve controls retain the accepted bridge check’s arithmetic and
falsification boundaries: degree-six interpolation, zero bound, negative constant,
negative right endpoint, vanishing endpoints of a purported strict prerequisite, two
independently known box maxima, the original excluded bridge, a raised board threshold,
a corrupted polynomial constant, the favorable mixed prerequisite and its negation.

Eight added controls are:

1. Exclude the all-negative, zero-jump rank walk `(0,0,0,0,0)`.
2. Exclude its two-jump version `(0,0,0,1,2)`.
3. Exclude its three-jump version `(0,0,1,2,3)`.
4. Exclude its four-jump version `(0,1,2,3,4)`.
5. Retain all sixteen normal choices for a straight chain with alternating signs.
6. Refuse to certify the favorable all-positive walk `(0,1,2,3,4)`.
7. Refuse a transverse rank jump of two as outside the domain.
8. Refuse two aligned tiles on the chain as outside the domain.

In all there are eleven expected acceptances and nine expected refusals.
A failed control, changed input, incomplete roster, bridge-regression discrepancy,
unexpected exception or cap fails the whole job.
No partial catalogue is accepted.

## Work and Resource Bounds

The finite enumeration is 29,008 profiles with at most 464,128 normal choices.
A rank-error maximum enumerates 32 box vertices; a bounded cache reuses those
calculations. Distinct physical bounds are also cached, with a hard ceiling of 8,192
retained records. Each requires degree-six interpolation and exact Bernstein arithmetic.
The output retains the complete local roster with compact bound references instead of
copying all polynomials into every branch.

Proposed run: one project Python 3.14.7 worker, standard library only, with `-I -B`.
Target under 30 wall seconds and 0.15 GiB peak RSS. Hard limits: 60 seconds, 0.25 GiB
sampled process-tree cost, stop at pressure level 2; internal work ceiling 55 seconds.
Exceeding any limit produces a failed/incomplete attempt, never a narrowed claim.

From this directory, with an external supervisor:

```bash
"$PYTHON" -I -B check_one_axis_general_paths.py \
  --spec general-path-spec.json --output "$OUT/general-path-catalogue.json"
```

The output must be a new file.
Use external scratch/cache directories.
Do not execute, import, compile or syntax-check before the coordinator offers the serial
guarded slot.

## Boundaries After a Successful Run

A complete local catalogue would supply sound local exclusions for all possible
five-tile rank/sign profiles.
It would not establish that graph generation includes every separation choice, that
masks and vertical signs apply these clauses correctly, or that geometric rules for
every surviving graph are contained in an accepted polynomial certificate.

The producer’s 273,584 surviving graphs and 566 used bank certificates therefore remain
unverified global counts.
The one-axis theorem does not clear Stage 4 from this slice alone.
No unrestricted or angular-diversity theorem is decided.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
