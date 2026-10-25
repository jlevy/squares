# All eight long C1092 terminal covers now have continuous replacements

## Result and retained scope

The eight maximal-angle terminal ranges numbered 1,2,3,4,5,6,50,51
in the supplied C1092 continuation are excluded by the continuous
theorems in this revision. Their terminal adaptive covers are no longer
needed. The new proof uses the actual common side, actual square
supports, and exact geometric entrance data.

This is a replacement of all eight long endings. The earlier deductions
that establish their entrances remain retained. In particular this result
does not delete the 431 common-parent coordinate cuts, the unrestricted
MPPM ownership reduction, or the incoming maximal-angle histories.

## 1. The negative ranges

C1092-CYCLES.md proves the negative scalar inequality throughout
0≤h≤1/8. C1092-NEGATIVE-GEOMETRY.md supplies its full geometric proof
with the weaker center bound Cₓ≥27/20 and joins it to both actual
negative endpoints. Their maximal half-angles are

| Range | Exact maximal half-angle interval |
|---|---|
| 50 | [13/115,7/57] |
| 51 | [3/29,13/115] |

Both lie within [0,1/8]. All the other negative endpoints 52–63 already
satisfy the stronger old entrance and are covered by the same theorem.

The exact endpoint bounds and strict-point certificates for the newly
covered ranges are in NEGATIVE-50-51-ENTRANCE-DATA.txt. A point on
the boundary of a convex hull of strict owned points is still strict
inside the square. All foreign exclusions are supplied by actual other
owners, and the actual outer wall supplies the boundary wall constraint.

## 2. The positive theorem and its physical inputs

C1092-POSITIVE-CYCLE.md proves a continuous theorem for four actual
central angles with 0≤tan(pᵢ/2)≤7/64 and boundary half-angles of
absolute value at most 1/8. It uses each central square's own angle.
Its scalar companion, C1092-POSITIVE-EDGE-INEQUALITIES.md, proves
just two inequalities, according to the order of consecutive angles.
The positive wall remainders are proved in C1092-WALL-REMAINDERS.md.

Use the last MPPM auxiliary assignment

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

The central owners are Cᵢ=Q₄₊ᵢ. The corresponding boundary owners
Bᵢ are Q9,Q10,Q11,Q8. Every statement uses chart R^(−i), with
R(x,y)=(4−y,x); no symmetry of the actual packing is assumed.

The exact original auxiliary ownership itself supplies the following
central points in every chart:

    U=(1,87/50), T=(87/50,2), and (1,8/5).

Only U,T are needed as hypotheses of the new positive theorem: its
forced-face bounds imply strict ownership of (1,8/5) as well. The
actual corner owners supply exclusion of A=(1,1).

The preserved incoming states for ranges 1–6 strictly give P=(2,1)
to Bᵢ in every chart. Consequently the preceding boundary Bᵢ₋₁
owns D=(1,2) in sector i, proving its exclusion from Cᵢ directly.
This cyclic implication removes D as an independent entrance premise.

The remaining consumed geometric bounds are

    Cₓ≤3/2≤Cᵧ,
    −1/4≤Cₓ−Bₓ≤0,   0≤Cᵧ−Bᵧ≤3/2,
    0≤Jₓ−Bₓ≤1,      3/4≤Jᵧ−Bᵧ≤1.                  (1)

Here J is the next actual central center in the same chart. The boundary
square lies above y=0 by the real container. No near-axis coordinate
rectangle from the old positive theorem is added.

## 3. Exact audit of the six actual entrances

The endpoints are the six preserved states

    maxangle-mppm23-k{k}-1-segments-seed,  k=1,…,6.

POSITIVE-1-6-ENTRANCE-DATA.txt records their exact per-sector center
intervals, angle cells, and all 24 rational convex-combination certificates
for strict boundary ownership of P. It identifies which facts are retained
endpoint consequences and which already follow from the original table.

Every center bound below encloses every vertex of every retained pose
polygon, in each of the four sector charts. Interval subtraction is
outward: it never assumes that different square centers attain their
extrema simultaneously. For all six ranges,

    Cₓ≤3/2, Cᵧ≥3/2, Bₓ≥3/2,
    Jₓ−Bₓ≤1, Jᵧ−Bᵧ≤1,
    Cᵧ−Bᵧ>9/10, Cᵧ−Bᵧ<11/10.

The last lower bound may be weakened to 0; it is stated only to make
the actual upward order explicit. The other needed margins, combined
over the four sectors in each range, are:

| Range | max(Bₓ−Cₓ) | min(Jₓ−Bₓ) | min(Jᵧ−Bᵧ) |
|---|---:|---:|---:|
| 1 | .16065931 | .84383655 | .89061465 |
| 2 | .19501720 | .81058777 | .85988937 |
| 3 | .16466510 | .85283455 | .83169643 |
| 4 | .19094488 | .83513957 | .80329094 |
| 5 | .19063292 | .83630178 | .80280687 |
| 6 | .20656370 | .83573409 | .78245394 |

All decimals denote exact rationals. The first column is below 1/4,
the second is positive, and the third exceeds 3/4. This verifies (1)
without a further center subdivision.

The retained boundary canonical half-angles, combined over all six
ranges and all sectors, lie in [−1/63,7/64], a subset of [−1/8,1/8].
These endpoint bounds hold over the whole angular cells by the rational
half-angle formulas and their monotonicity.

The actual maximal-angle choice puts Q4's positive half-angle in
[k/64,(k+1)/64] and bounds every other central absolute angle by it.
Thus the positive maximum over ranges 1–6 is at most 7/64. This actual
maximality condition is retained explicitly; a coarse polygon's raw
angle cell need not itself be clipped at that upper bound.

## 4. Sign coverage

Ranges 1 and 2 may still contain a central angle of the opposite sign
in their individual raw cells. C1092-MIXED-SIGNS.md excludes every
mixed or zero sign configuration in both ranges, with the strict
inequality

    0≥4(a−1)+(12/125)α+(2/5)m.

Its aggregate gap hypotheses are established there from the exact same
incoming endpoint centers. Because the chosen maximal central angle
is positive, the remaining configuration has all four central angles
strictly positive. The new positive-cycle theorem now applies.

For ranges 3,4,5,6, all retained central canonical angle cells are
already nonnegative. Their upper half-angle limits are at most 7/64
after the actual maximality condition is used. The positive theorem
itself rules out an exactly zero angle from its forced faces and
Cₓ≤3/2. Thus it applies to the full remaining domains, including
every boundary and maximum-angle tie.

The positive cycle concludes

    0=Σ(Lᵢ₊₁−Lᵢ)
      ≥Σ[(1−cos pᵢ)(2cos pᵢ−1)/cos pᵢ]+(1/10)V>0,

where V is the common total of ascending and descending half-angle
increments around the closed cycle. Each pᵢ is strictly positive and
cos pᵢ>1/2. This supplies the actual contradiction for all six ranges.

## 5. Exactly which old material becomes unnecessary

The old Section 7 of wall_geometry_next/09_C1092_complete_composition.txt
uses finite covers for precisely the eight ranges above. Its 55 selected
tables contain 8,090 binary splits, 6,650 geometric certificate leaves,
and 1,730 dominance leaves, with the additional continuation histories
used only inside those terminal covers. These endings can all be
replaced by the continuous results just proved.

The smaller earlier negative ranges and the near-axis positive range
retain their already established entrance proofs. The new positive
theorem also subsumes the old all-positive near-axis theorem whenever
its displayed narrow boxes are used, since those boxes imply (1).

This result removes the eight large terminal trees as mathematical
dependencies. It does not replace the entrance histories that produced
their root states. The distinction is necessary: point P and the broad
center inequalities in (1) must still be proved from an original packing
before the new short ending may be invoked.

## 6. Verification of the new argument

The rational half-angle identities in both scalar theorems were checked
independently. For the positive theorem this includes reconstructing both
full polynomials directly from the displayed formulas, checking their
exact positive denominator factorizations, and verifying every rational
coefficient sum in their sign proofs. The twelve wall-remainder factor
identities were likewise checked exactly. These checks verify written
identities; the continuous sign arguments in the proofs, rather than
angle samples, establish validity on their complete domains.

The forced-face alternatives, actual square support directions, wall
transport signs, strictness at a>1, and endpoint owner mappings were
reviewed separately. No proof-assistant dependency or new interval
enumeration is introduced by these replacements.
