# C1092: a direct exclusion of the entire last auxiliary assignment

All decimal constants denote exact rationals. This chapter joins the
completed direct sign arguments. It states the actual starting assignment,
its owner map, the full sign cover, and the precise simplification obtained.
No incoming angle or center history is a premise.

## 1. The original physical configuration

Suppose twelve distinct open squares Q0,...,Q11 have common side

    1<a≤1001/1000,

pairwise disjoint interiors, and closures in [0,4]². Retain the original
C1092 marker groups and auxiliary-label convention from the supplied
handoff. The exact last auxiliary assignment is

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

A label specifies its owner's exact owned subset of the twenty original
auxiliaries, with label=f+1024g for the two ordered ten-point coverings.
Thus both its owned points and its exclusions retain their original
meaning. The four original paired-corner squares have their compulsory
strict inner points. Retain the closed MPPM wall-center conditions

    center(Q8)_y≥2,  center(Q9)_x≤2,
    center(Q10)_y≤2, center(Q11)_x≥2.                 (1)

**Theorem.** No such configuration exists.

## 2. One common chart with four actual applications

Let R(x,y)=(4−y,x). For i=0,1,2,3, transport the entire physical
configuration by R^(−i) to the ith sector chart. The following are
actual owners, not independently chosen local squares.

| Sector i | Central C_i | Paired corner K_i | Bottom boundary B_i |
|---:|---|---|---|
| 0 | Q4 | Q0 | Q9 |
| 1 | Q5 | Q1 | Q10 |
| 2 | Q6 | Q2 | Q11 |
| 3 | Q7 | Q3 | Q8 |

In each corresponding chart the original strict data become

    C_i: (1.65,1.65), (1,1.74), (1,1.6), (1.74,2);
    B_i: (2,.914), (1.6,1), (1.74,1);
    K_i: (1,.914), (.914,1), (1,1).

Every boundary has its genuine bottom wall y≥0, every paired corner
has its genuine two corner walls, and (1) becomes

    center(B_i)_x≤2.                                  (2)

All foreign markers and auxiliary exclusions are transported by the same
map. In particular the preceding and following central and boundary
owners in a local argument are the actual adjacent owners in this table.
The eight local squares used in the cycle are not eight independently
relaxed support regions.

Choose a canonical angle in [−π/4,π/4] for each central square in its
own chart. The repeated endpoint representation of a diagonal square
causes no omission: the direct negative/mixed arguments include their
closed canonical endpoints, while the positive entrance itself forces
any positive canonical angle into a much smaller open interval.

## 3. Exhaustive sign cover

There are three exhaustive alternatives.

**All four central angles are nonpositive.**
The direct negative-cycle theorem in
[C1092-DIRECT-NEGATIVE-CYCLE.md](C1092-DIRECT-NEGATIVE-CYCLE.md)
starts with exactly the actual data in Section 2. The strict point
propagation and actual corner-to-wall transfers establish its required
boundary points. Its face and actual-segment estimates place the four
central centers in an open disk too small to contain four pairwise
disjoint side-greater-than-one squares. The theorem includes zero and
both relevant canonical endpoint choices; it assumes no angle cutoff.
This excludes the first alternative.

**There are positive and nonpositive central angles.**
Choose the first positive angle following a nonpositive angle around
the actual four-sector cycle. The direct mixed-cycle theorem in
[C1092-DIRECT-MIXED-CYCLE.md](C1092-DIRECT-MIXED-CYCLE.md)
handles this actual transition. It identifies the corner-transfer and
boundary-point owners needed at that transition and derives the
positive successor's angle bound from its actual neighbors. The same
support profile then forbids the successor. No premise that all four
boundary points are already owned is used. This excludes every mixed
or zero/positive alternative.

**All four central angles are strictly positive.**
The complete direct proof in
[C1092-DIRECT-POSITIVE-CYCLE.md](C1092-DIRECT-POSITIVE-CYCLE.md)
starts from Section 2 and proves its own entrance. In every chart it
forces the strict central points H=(1,1.5), X=(1.5,2) and the strict
boundary point P=(2,1), and derives

    0<x_i:=tan(p_i/2)<1/5,
    −1/8<tan(β_i/2)<1/3,
    center(C_i)_x<3/2<center(C_i)_y.                 (3)

The proof treats each actual separating-normal source and every
relative central-angle order. It defines, in the ith square's own
sector chart,

    L_i=v_(p_i)·((2,2)−center(C_i)),
    f(x_i)=(1−cos p_i)(2cos p_i−1)/cos p_i>0,

and establishes on every actual edge

    L_(i+1)−L_i>f(x_i)−(x_(i+1)−x_i).               (4)

The positive-boundary proof covers all four actual normal-source
combinations. A separate proved nonpositive-boundary calculation gives
the identical inequality for the remaining boundary signs. Summing
(4) over the four sectors, with indices modulo four, yields

    0>sum_i f(x_i)>0,

a contradiction. All center and half-angle differences cancel exactly;
the actual angles need not be equal or extremal. This excludes the final
alternative and proves the theorem. ∎

## 4. Proof dependencies for the positive alternative

The continuous entrance is supplied by
[C1092-POSITIVE-D-TRANSFER.md](C1092-POSITIVE-D-TRANSFER.md),
[C1092-POSITIVE-QUADRANT-BOOTSTRAP.md](C1092-POSITIVE-QUADRANT-BOOTSTRAP.md),
and [C1092-POSITIVE-WALL-POINTS.md](C1092-POSITIVE-WALL-POINTS.md).
They derive their foreign points from actual neighboring owners.

The negative-boundary edge uses
[C1092-POSITIVE-BOUNDARY-ORDER.md](C1092-POSITIVE-BOUNDARY-ORDER.md)
and
[C1092-NONPOSITIVE-BOUNDARY-POTENTIAL.md](C1092-NONPOSITIVE-BOUNDARY-POTENTIAL.md).

The positive-boundary edge uses the exact scalar estimates in
[C1092-POSITIVE-ENDPOINT-SCALARS.md](C1092-POSITIVE-ENDPOINT-SCALARS.md),
[C1092-CB-ENDPOINT-SCALARS.md](C1092-CB-ENDPOINT-SCALARS.md),
[C1092-POSITIVE-BB-REDUCTION.md](C1092-POSITIVE-BB-REDUCTION.md),
and [C1092-BC-CURVATURE-SCALAR.md](C1092-BC-CURVATURE-SCALAR.md).
Their endpoint identities, coefficient bounds, and curvature estimates
are proofs on full closed parameter domains. Their use in the geometric
cycle follows the explicit, acyclic source reductions in the direct
positive-cycle chapter. Numerical angle samples supply no proof step.

## 5. Exact effect on the simplification program

For this identified last assignment, the theorem supplies a complete
continuous ending directly from original physical ownership and MPPM
wall-center data. It requires none of the old terminal angle ranges,
center boxes, or incoming maximal-angle histories as extra assumptions.
The eight independently completed terminal replacements remain valid
and are preserved in the package, but the theorem now reaches their
common last-assignment contradiction directly.

The theorem does not identify every earlier ownership vector with this
one. The earlier MPPM ownership reduction and the separate whole MMMM
and MMMP wall classes are distinct obligations. Their simplification
requires proofs from their own original owner families. This chapter
completes the last assignment and states exactly that scope.
