# Stromquist’s `n = 26` Packing: Directions and a Restricted-Family Obstruction

Memo III’s twelve-square oblique group has been reconstructed and verified as a
historical construction in the
[completed review](../research/research-2026-09-07-stromquist-n26-verification.md).
Its side `5.650629191439388…` exceeds the current exact verified upper bound
`U = (7 + 3√2)/2 = 5.62132034355964…`. The current configuration also admits a short
restricted-family argument: rotating and translating its rigid central block, while
preserving the separating faces specified below, cannot reduce the side below `U`.

This independent review concerns mathematical directions and their prerequisites.
The completed review retains the source reconstruction and current-bound replay.
No new unrestricted packing bound is established here.

## The Two Construction Families

[Memo III](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.pdf),
p. 5, Figure 4(b), shows three apparent four-square columns with common oblique
orientation, surrounded by fourteen aligned squares.
The [exact reconstruction](../../../packing/cases/stromquist/memo3_n26.py) resolves each
column into two independently offset `1 × 2` dominoes: six dominoes in all.
Their small relative slides matter; treating a column as a rigid `1 × 4` bar would
change the construction.
The caption gives `s ≈ 5.650629` and `θ ≈ 27.583°`. Figure 3(b), on the same page, has
eight oblique squares and gives `(7 + √7)/2`, the same side as the current `n = 18`
upper bound. The page was inspected as a rendered scan; the separate
[exact record](../../../packing/cases/stromquist/memo3-n26.json) verifies the `n = 26`
coordinates against every wall and all 325 pairs.

The current `n = 26` construction has a solid `3 × 3` oblique block at `45°`, twelve
aligned squares in four corner triplets, and five more aligned squares in a side column.
[Friedman’s survey, Section 3](https://erich-friedman.github.io/papers/squares/squares.html)
gives the rectangle-and-column rule; the repository’s
[exact builder](../../../packing/cases/gobel_offcentre/packing.py) specializes it at
`(a, b) = (2, 3)`. The memo and current construction have different square groupings and
contact patterns.

The
[older-packing catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html)
already lists Stromquist’s `n = 26` side as `5.65062919143938…` with polynomial
`s³ − 14s² + 67s − 112 = 0`. Its recognition by a catalogue supports the historical
identification; the exact reconstruction establishes that the figure fits at the
polynomial’s real root.

## A Closed Direction: Rigid Central-Block Rotation

**Claim and scope.** Fix the southwest and northeast aligned corner triplets of the
current construction in a rectangle of width `W = L − 1` and height `H = L`. Put a solid
square block of side `3` in that rectangle, allowing its center and orientation to vary.
Require the southwest triplet to remain entirely beyond one block face, and the
northeast triplet entirely beyond its opposite face, with the assignments given below.
Every such configuration has

$$
L \ge U = \frac{7+3\sqrt 2}{2}.
$$

The existing exact construction attains equality.
This proves the minimum in this declared family.
It does not establish optimality among all `26`-square packings, among all possible
arrangements of a `3 × 3` block and aligned squares, or among all ways to separate the
block from those corner triplets.

**Coordinates and separation assignments.** The southwest triplet consists of the three
closed unit squares with lower-left corners `(0, 0)`, `(1, 0)`, and `(0, 1)`. Reflect it
through the rectangle center to obtain the northeast triplet.
Let

$$
u=(c,s)=(\cos\theta,\sin\theta),\qquad
0\le\theta\le\frac\pi2,
$$

and let `C` be the center of the oblique block.
A block whose edge directions are `u` and `(-s, c)` has projection interval
`[C·u − 3/2, C·u + 3/2]` along `u`.

The maximum `u` projection of the southwest triplet is

$$
M=\max(2c+s,c+2s)=c+s+\max(c,s).
$$

The minimum projection of the northeast triplet is `Wc + Hs − M`. The two required
separating-face assignments are therefore exactly

$$
M\le C\cdot u-\frac32,
\qquad
C\cdot u+\frac32\le Wc+Hs-M.
$$

These inequalities are part of the family’s definition.
Requiring a whole triplet to lie beyond one block face is stronger than requiring its
three unit squares to avoid the block separately.
In particular, the triplet’s missing fourth square creates a corner gap that other
separating-axis assignments may use.

**Eliminate the center.** The inequalities imply

$$
3\le Wc+Hs-2M
  =L(c+s)-c-2(c+s)-2\max(c,s).
$$

Since `c + s > 0`,

$$
L\ge F(\theta)
 :=2+\frac{3+c+2\max(c,s)}{c+s}.
$$

Two elementary inequalities finish the argument:

$$
c+2\max(c,s)\ge\frac32(c+s),
\qquad c+s\le\sqrt2.
$$

The first follows separately from `c ≥ s` and `s ≥ c`; in the two cases the difference
is `3(c − s)/2` and `(s − c)/2`, respectively.
The second follows from `c² + s² = 1` and `(c − s)² ≥ 0`. Therefore

$$
L\ge F(\theta)\ge\frac72+\frac{3}{c+s}
                  \ge\frac72+\frac{3}{\sqrt2}=U.
$$

Equality requires `c = s = 1/√2`, hence `θ = π/4`.

At the existing construction, `C = ((U − 1)/2, U/2)` and both projection inequalities
are equalities. Its other pair and wall constraints are the ones checked by
[the exact replay](../../../packing/cases/gobel_offcentre/verify_exact.py).

This also explains why the retained witness’s movable side-column squares do not supply
a descent direction in this family.
The obstruction uses only the central block and two corner triplets.
Moving a square outside those groups cannot change the two inequalities.
The [record’s translation result](../../../packing/frontier/n-026.md) concerns feasible
motion at a fixed side and has its own finite-precision scope; it does not imply a
smaller enclosing square.

## What to Pursue

| Direction | Concrete test and disposition |
| --- | --- |
| Recover Memo III’s geometry | Completed: six independently shifted `1 × 2` dominoes reproduce Figure 4(b), with exact unit-square identities, all 325 pair checks, and every wall check at the cubic side. The [exact record](../../../packing/cases/stromquist/memo3-n26.json) retains the coordinates and comparison. The related `n = 18` current record also passes its separate exact replay. |
| Rotate or translate the current solid block within the stated separation family | The proof above closes this proposed direction analytically. A numerical sweep would add no evidence to that claim. The restriction on separating faces must remain attached to any reuse of the result. |
| Release a specified source contact pattern | Use the two verified constructions as controls. Preserve the memo’s six independent domino offsets; declare any additional freedom in their angles or frame positions. For the current construction, declare which internal block contacts or corner-triplet constraints are released. Test changed pair-separation assignments and compare against both the memo side and `U`. First verify that the chosen release can violate the obstruction’s assumptions; sliding unrelated side-column squares cannot do so. This is the next packing-search experiment, conditional on a reusable driver that preserves and replays the controls. |

For the third test, freeze the allowed motions, separating-axis branches, parameter
intervals, and stopping rule before searching.
A fixed-angle translation LP can evaluate one branch, but its feasibility is only
branch-specific and its numerical optimum needs independent verification.
An apparent improvement must become explicit coordinates and pass every pair and wall
check at a side strictly below `U`. An unsuccessful finite sample establishes only the
outcome of that sample.
An exhaustive interval or exact argument would be required to close the whole released
family.

The central block’s rigid rotation is an inexpensive exact negative control for such a
driver.
It must reproduce `U` and refuse any claimed strict improvement while the proof’s
assumptions remain imposed.
A control failure would identify a geometry or constraint error before a candidate is
treated as a new packing.

## Recovering Green’s Reported Lower-Bound Argument

[Friedman’s Theorem 9 and Table 2](https://erich-friedman.github.io/papers/squares/squares.html)
report a lower bound attributed to Green:

$$
s(26)\ge G=2\sqrt2+\frac{27+2\sqrt{10}}{13}
\approx5.3918.
$$

The theorem specializes at parameter `5`; Table 2 explicitly lists `26–27`. The citation
is to Green’s private communication in 2000. The survey supplies no `n = 26` point
coordinates or proof, and its Figure 34 illustrates only `17` and `19`. Thus source
recovery or a new independent construction is needed before this argument can be
reproduced in the repository.

This is a separate lower-bound direction with a concrete target: recover a proof of `G`,
or construct and certify a point set at a specified threshold below `G`. The
[existing Green `n = 17` case](../../../packing/cases/green17/) supplies a related
control, but its sixteen points do not establish a twenty-five-point cover by scaling or
adding a row without a new coverage argument.
Freeze any such generalization as a hypothesis, exercise an escaping-square falsifier,
and require the exact or interval cover verifier to accept the complete pose domain.
A refusal should retain the escaping pose and the invalidated geometric assumption.
Until then, Green’s value remains source-reported, distinct from the independently
verified lower bound in the case record.

## The Earlier `5.52` Computation Is a Separate Lower-Bound Question

[BC-202](../../../packing/campaign/agendas/agenda-021-three-numbers-and-a-wall.md)
attempted a fractional unavoidable-set certificate at `138/25 = 5.52`. Its
[retained result](../../../packing/campaign/series/series-000-smoke-and-calibration/results/bc-202-n26-138-25.json)
reports 22 column rounds and 137 LP rounds in `7,982.760…` seconds, finishing at
covering objective `26.4643165243211`, with no frozen certificate.
The final row loop had converged on its site set; the column loop still found negative
reduced-cost candidates and had not converged.

A numerically converged restricted covering objective above `26` leaves no candidate to
certify from this run.
The JSON contains no exact dual certificate proving a lower bound on that covering
optimum. Adding sites can lower the restricted optimum, so the run does not exclude a
certificate at `5.52` or establish the reach of the method.
It also says nothing about whether Memo III’s upper-bound construction is valid or
better than the current packing.

The recorded checkpoint names a temporary path on an earlier host.
[BC-209](../../../packing/campaign/agendas/agenda-022-the-conditional-route.md) inherits
the covering question and is recorded as blocked on a priced target and prior lane
disposition. Resuming that work requires locating the actual checkpoint and its matching
state or declaring a fresh run.
The summary JSON alone is not a continuation checkpoint.
The present source review supplies no mathematical reason to duplicate BC-202’s
unresolved computation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
