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
| Release a specified source contact pattern | The [first released-contact family](#first-released-contact-family) splits the current central block into nine squares at one common angle, with half-turn symmetry, and releases four specified pair branches. `think-z0fi` owns the affine LP adapter and controls. Driver readiness is false; no target LP or packing search has run. |

### First Released-Contact Family

The mathematical specification for `think-z0fi` is complete enough to implement the
adapter and controls below.
Driver readiness is false: no target LP or packing search has run.
Its finite angle sample covers only the stated choices.

#### Family and Parameters

Start from `cases.gobel_offcentre.packing.build(2, 3)`. Keep its twelve aligned corner
triplet squares and five side-column squares at their existing positions as affine
functions of container side `L`. Thus the inner rectangle has width `W = L - 1` and
height `H = L`; the added column has centers `(L - 1/2, k + 1/2)`, `k = 0,...,4`.

Replace the rigid central `3 × 3` block by nine independently translated unit squares at
one common angle. Impose half-turn symmetry on these nine squares about
`C(L) = ((L - 1)/2, L/2)`. Label them `P_ij`, `i,j = 0,1,2`, by their source centers

```
C(L) + (i - 1) u + (j - 1) v,
u = (cos(theta), sin(theta)), v = (-sin(theta), cos(theta)).
```

Use four independent center offsets `d_00`, `d_01`, `d_02`, `d_10`; set
`d_(2-i,2-j) = -d_ij` and `d_11 = 0`. Bound each offset component to `[-1/2, 1/2]` and
`L` to `[28/5, 45/8]`. There are eight free translation coordinates and `L`: nine linear
variables at each fixed angle.
These bounds define the proposed local family; they do not bound all possible
improvements.

The sole nonlinear parameter is `t = tan(delta/2)`, where `theta = pi/4 + delta` and `t`
lies in `[-1/20, 1/20]`. Put `a = (1 - t²)/(1 + t²)`, `b = 2t/(1 + t²)`, and
`u = ((a - b)/sqrt(2), (a + b)/sqrt(2))`. Rational `t` keeps all coefficients in
`Q(sqrt(2))` and preserves the unit-edge identity exactly.

The first prospective angle sample is exactly `t = -1/20, -1/40, 0, 1/40, 1/20`. This
finite sample tests only those angles.
The interval declaration preserves the intended later family; it is not certified by
sampling it.

#### Exactly Which Separations Are Released

The proof’s whole-triplet versus solid-block inequalities are not imposed.
The solid block equalities are also removed.
Retain all unit-square pair nonoverlap constraints.

Let `A` be the aligned square with lower-left corner `(1,0)` and `B` the square with
lower-left corner `(0,1)`. Their inner corners `(2,1)` and `(1,2)` meet `P_00` and
`P_01`, respectively.
Release the signed separating-axis choices for these two pairs and their half-turn
partners in the northeast triplet.
For each southwest pair choose one of `+x`, `-x`, `+y`, `-y`, `+u`, `-u`, `+v`, `-v`;
use the opposite signed normal on its half-turn partner.
This gives `8 × 8 = 64` branch patterns per angle.

In the exact builder’s zero-based output order, the expected four released pairs are
`(4,18)`, `(1,15)`, `(11,14)`, and `(9,17)`. These are builder indices, not retained
witness IDs. The implementation must derive the semantic labels from exact centers and
assert this mapping before building an LP. The tilted-square order follows
`P_ij = output[12 + 3*(2-j) + i]`; the aligned output indices are `A=4`, `B=1`,
`A_NE=11`, and `B_NE=9`.

For the other `325 - 4 = 321` pairs, freeze a deterministic signed axis from the exact
Friedman pose at `t=0`, retaining axis identity when `u,v` rotate.
Use exact signs to resolve choices and record the resulting full map.
Freezing these other branches is a restriction of the experiment, not a claim that
alternative branches are impossible.

This family can violate the rigid-block assumptions and permits alternative separating
axes at the four contacts underlying the obstruction.
Feasibility or an improvement after those releases remains unproved.

#### LP, Controls, and Acceptance

For a selected signed normal `n` pointing from square `i` to `j`, impose

```
n · (center_j - center_i) >= h_i(n) + h_j(n),
h_i(n) = (abs(n · u_i) + abs(n · v_i))/2.
```

All centers are affine in the nine variables and all support values are exact constants
at fixed `t`. Add every wall inequality, the offset bounds, and the side bounds.
This constructs one convex LP with all 325 pair constraints, including the four
replacements. Solve `min L`, retain the complete coefficients and branch map, then
reconstruct every corner from the returned exact point.

Use the [exact LP implementation](../../../packing/src/sqpack/exact_lp.py): `ExactLP`,
`LinearRow`, `solve_from_scratch`, and `certify_vertex`; a numerical solve may supply a
basis hint. Existing `fixed_cell_lp` and the
[quench’s `solve_cell`](../../../packing/src/sqpack/research/quench.py) do not directly
represent this reduced family: their independent square translations and pose-derived
branch selection require a new adapter with explicit affine substitution.
Using either unchanged would test a different domain.

Required controls before the target sample:

- Reproduce the exact Friedman geometry at `t=0` and zero offsets.
  Restore rigid-block equalities and the two whole-triplet separating-face inequalities,
  then require the exact optimum to be `U = (7 + 3sqrt(2))/2`. Any strict improvement
  with those restrictions imposed is an instrument failure.
- Force `P_00` and `P_01` to coincide and require infeasibility or exact rejection.
- Replay the memo’s six-domino construction through the geometry-verification pipeline.
  This is an independent pipeline control: the memo is outside this 17-aligned,
  9-common-angle family and has side greater than `U`.

Accept an upper-bound improvement if the exact candidate side satisfies `L-U < 0` in
`Q(sqrt(2))`, all 26 squares have exact unit edges, and independent pair/wall replay
accepts all 325 pairs and every wall.
Retain the exact feasible coordinates; an LP dual is required only for a claimed
fixed-cell optimum or infeasibility, not for the upper-bound improvement.
Keep the typed solver status separate from geometric acceptance: a capped or refused
solve alone supplies no certificate, but does not disqualify a separately recovered and
independently verified feasible packing.
A float improvement alone is insufficient.
An exact LP optimum or infeasibility certificate applies only to its fixed angle and
branch; unsuccessful sampling does not exhaust the angle interval or all branch changes.

#### Next Implementation Slice

Implement the semantic-index check, nine-variable affine adapter, explicit branch-map
serialization, and controls first.
Measure one exact control LP before registering a target time limit.
Then register the five angles and 64 branch patterns each, with fixed LP pivot limits, a
total solve limit, and a rule to retain typed refusals.
Publish every attempt’s side, certificate status, branch, and cost.
Any undecided cell remains undecided.
Broader angle refinement or additional released contacts require a subsequent declared
slice.

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

The
[MacIver source review](review-2026-09-07-maciver-square-packing.md#defect-charging-and-a-co-hit-graph)
adds a possible conditional route under `think-0x08`: if a reconstructed scaffold admits
avoiding squares, certify which point losses those squares force and combine the losses
through the co-hit matching bound.
That n17 method supplies neither the missing n26 points nor their geometric
classification. A transferred proof must establish both for its own n26 domain.
The source and formal replay dependency `think-sske` also remains open; no MacIver
theorem is adopted here.

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
