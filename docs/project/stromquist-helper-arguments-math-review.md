# Stromquist’s Helper Arguments and Conditional Dots Certificates

Stromquist’s three 1984 memoranda contain working examples of the extension suggested in
his email: geometric constraints force several dots into the same square, then a
counting argument excludes the packing.
Memo I gives a useful six-square control.
The repository already verifies this form of argument for the repaired unrestricted
eleven-square certificate; further work should reuse that result and the recorded
failures of stronger conditional covers.

This review checks the mathematical structure and implements the finite allocation step
in Memo I. It does not independently verify every geometric lemma in the memo, prove the
claimed impossibility of a pure dots proof for six squares, or improve a packing bound.

## What the Sources Contribute

| Source | Preliminary argument | Final dots argument |
| --- | --- | --- |
| [Memo I](../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.pdf), pp. 11–19 | Adjacent isolated marks cannot occur in separate blocks; incidence counting leaves one allocation; its center block contains four specified marks | Eight unavoidable marks, four in one block, allow at most five blocks |
| [Memo II](../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares.pdf), pp. 10–15 | Replace marks in unavoidable sets to force additional incidences; convexity then excludes whole segments from other blocks | Marks already occupied by eight blocks leave only one available mark for two remaining blocks |
| [Memo III](../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.pdf), pp. 6–10 | A box avoiding ten marks is localized and forced to contain three new marks, with orientations restricted to 0° or 45° | Twelve unavoidable marks with three in one box allow at most ten boxes |
| [2003 paper](../../packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.pdf), Theorems 1–3 | Develops the ten-square forcing chain and the eleven-square localization/triple argument | The unrestricted eleven-square printed cover requires the separately verified one-coordinate repair |

The existing [reading aids](../../packing/resources/README.md) distinguish the scanned
memoranda from mathematical transcriptions.
In Memo I, the comparison in Lemma 8 is with **one half**, not the value 2 produced by
OCR. The point grid and the final allocation were checked against the rendered pages 13,
18, and 19.

The unrestricted eleven-square repair is already retained as
[H-041](../../packing/campaign/hypotheses/H-041-repaired-stromquist-point-set.md), with
the complete checker in
[repaired_cover.py](../../packing/cases/stromquist/repaired_cover.py).
It verifies the first cover’s exceptional regions, the forced triple, the repaired
second cover, and the capacity contradiction.
Moving the printed mark `G=(.8,1.85)` to `(.79,1.85)` is a source-distinct repair, not a
recovered coordinate from the memoranda.

## The Counting Lemma

Let the finite marked set carry nonnegative weights of total mass $M$. Here a block is
an open square, and a mark is charged only when it lies inside that open square.
Suppose every block in a hypothetical packing contains marked mass at least $c>0$.
Suppose also that $r$ distinct blocks contain specified groups of marks of masses
$m_1,\ldots,m_r$. The groups belong to different blocks and therefore cannot share a
mark. Then

$$
(n-r)c+\sum_{i=1}^{r}\max(c,m_i)\le M,
\qquad
n\le r+\frac{M-\sum_{i=1}^{r}\max(c,m_i)}{c}.
$$

The proof sums the mass consumed by the blocks.
The open blocks are disjoint, so each mark contributes at most once.
The distinguished blocks pay their forced mass, or the baseline $c$ if that is larger;
every other block pays $c$. The statement is conditional on coverage and forcing, both
of which require geometric proofs.

For unit-weight dots and one distinguished block containing $k$ of $m$ marks, this is
`n <= 1 + m - k`. Memo I uses `(m,k)=(8,4)`; the unrestricted eleven-square proof uses
`(12,3)`. The new [occupancy_bound function](../../packing/src/sqpack/incidence.py)
checks this arithmetic with exact rational weights and rejects overlapping forced
groups. Its return value does not certify the geometric premises.

The gain comes from a relation between squares.
A universal weighted cover assigns a minimum mass to every possible placement
independently. Here a helper argument forces a larger mass in a distinguished placement
because it is part of the hypothesized packing.
This distinction matters when a fractional-piercing ceiling excludes every unconditional
measure in the current certificate family.

## Six Squares: A Checked Finite Control

Write the nine marks in the square `[0,3]^2` as

```text
G=(1,2)       H=(3/2,2)       I=(2,2)
D=(1,3/2)     E=(3/2,3/2)     F=(2,3/2)
A=(1,1)       B=(3/2,1)       C=(2,1)
```

An **incidence mask** is the complete subset of these marks contained in one block.
The finite control admits every nonempty mask satisfying the following necessary
conditions, with no upper bound imposed on its size:

1. It contains a perimeter mark.
   This is Memo I’s Lemma 6; the center `E` alone is insufficient.
2. It contains every marked point in the closed convex hull of its own marks.
   This follows from convexity, including marks on hull edges.
3. If it has exactly two marks, their distance is `1/2`, as stated on p. 18.
4. Two adjacent perimeter marks cannot both be singleton masks in different blocks.
   This is Lemma 8 and its global square symmetries.
   The control does not extend that lemma to pairs involving the center.

Different blocks have disjoint masks.
Some initial marks may be unused; requiring all nine to be occupied would assume part of
the conclusion.
Exhaustive enumeration gives four allocations forming one orbit under the
eight global square symmetries.
One is

```text
{A,D}, {B}, {C,F}, {E,H}, {G}, {I}.
```

All nine marks are used in every survivor.
This is derived by the enumeration.
The [retained JSON](../../packing/cases/stromquist/memo1-incidence.json) includes the
complete allowed-mask inventory, all four allocations, the source premises, and the
controls. The [independent test oracle](../../packing/tests/test_stromquist_memo1.py)
reconstructs convex membership through segments and triangles and enumerates assignments
to numbered blocks with a separate unused bucket.
The production code instead builds convex hulls and branches on the least undecided
site.

The usual counting proof explains why this finite calculation is small.
Six nonempty masks among nine sites require at least three singleton masks.
The perimeter cycle allows at most four mutually nonadjacent singleton marks.
If its four corners are singletons, one proposed remaining triple contains the center in
its convex hull, forcing a forbidden shared incidence.
If its four midpoints are singletons, the remaining sites cannot supply two allowed
nonsingleton masks. Thus exactly three singleton masks remain, and the other three masks
are adjacent pairs. The center’s partner can be placed at `H` by symmetry, after which
the perimeter matching has the displayed form.

Memo I’s next geometric step forces the `EH` block to contain `J=(1,17/10)` and
`K=(2,17/10)`. Lemma 7 supplies the unavoidable eight-mark set

```text
{E,G,H,I,J,K,L,M},    L=(1,9/10), M=(2,9/10).
```

Four marks lie in the center block, giving `1 + (8 - 4) = 5` blocks at most.
The new tool checks that implication, while retaining the forced `J,K` statement and the
eight-mark coverage as explicit unverified geometric premises of this replay.

Each premise has a control that exposes its contribution:

| Omitted condition | Surviving six-block allocations |
| --- | ---: |
| None | 4 |
| Every block hits the perimeter | 28 |
| Convex-hull closure | 8 |
| Two-mark blocks use adjacent marks | 118 |
| Adjacent perimeter singletons are incompatible | 680 |

Weakening the final forced group from four marks to three raises the capacity from five
to six, so that weakened argument does not exclude the target packing.
These controls verify the finite instrument, not geometric realizability of the
additional allocations.

Reproduce from `packing/`:

```bash
uv run --frozen python -m cases.stromquist.memo1 \
  --output cases/stromquist/memo1-incidence.json
uv run --frozen --all-extras --group dev pytest -q \
  tests/test_incidence.py tests/test_stromquist_memo1.py
```

## Eleven Squares: Keep the Full Distinguished Square

The existing conditional-dots target is
[H-036](../../packing/campaign/hypotheses/H-036-robust-restricted-orientation.md):
eleven squares whose orientations are all within `0.25°` of either `0°` or `45°` require
containing side at least `3.878`. This is an orientation-restricted statement.
Its threshold is above Trump’s unrestricted packing side and cannot be promoted to an
unrestricted lower bound.

Three useful preliminary clauses are already accepted:

- [H-106](../../packing/campaign/hypotheses/H-106-continuous-near-axis-ten-point-cover.md)
  proves the ten-mark cover throughout the near-axis band.
- [H-123](../../packing/campaign/hypotheses/H-123-near45-coordinate-localization.md)
  localizes a near-45° square avoiding those ten marks to the stated boundary region.
- [H-109](../../packing/campaign/hypotheses/H-109-near45-canonical-a1-a2-forcing.md)
  forces two specified marks into that localized square.

With eleven disjoint squares and only ten preliminary marks, at least one square avoids
all ten marks. The accepted clauses constrain that distinguished square.
The remaining covering obligation must use its full constraints.

[H-122](../../packing/campaign/hypotheses/H-122-diamond-conditional-nine-point-cover.md)
tested whether nine unchanged marks cover every unit square disjoint from a fixed
diamond known to lie in the distinguished square.
A checked counterexample refutes that sufficient cover.
It does not establish whether the escaping square can coexist with any full
distinguished square satisfying the preliminary clauses.

[H-124](../../packing/campaign/hypotheses/H-124-full-distinguished-square-compatibility.md)
already formulates the full-square compatibility implication.
Its outcomes determine what remains:

- [Exp-124](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-124-full-square-compatibility-screen.md)
  screened that retained escape against distinguished squares at the exact 45° frame.
  It returned no witness, which cannot establish the continuous implication.
- [Exp-125](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-125-h124-complete-residual-cover.md)
  independently certified the complete near-45° remaining-square branch.
  Its sufficient near-axis cover returned `no_chain`.
- [Exp-127](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-127-h124-collision-augmented-axis-cover.md)
  added a fixed collision region to the near-axis representation and also returned
  `no_chain`, without an independent reader.

Only the near-axis remaining-square branch of H-124 is still open.
The failed representations have no allocated retry or parameter sweep.
Their failures neither refute H-124 nor supply a disjoint square pair.
Repeating the fixed escape test would duplicate completed work.

For fixed orientations, containment, forced-point membership, and the separating-axis
conditions for a pair of squares are linear in their centers.
Avoiding a mark is a finite disjunction of square-side inequalities.
This gives finite linear subproblems for exploratory falsification.
Acceptance over a continuous angle band needs exact interval or polynomial sign
certificates as in the existing angle instruments.
Finite angle samples can refute the universal claim with an independently checked
witness; absence of a sampled witness cannot accept it.

The selected next slice in
[Session 095](../../packing/campaign/agent-sessions/session-095-collision-cover-and-support-ceiling.md)
is BC-264’s feature and verification-cost assessment for
[H-114](../../packing/campaign/hypotheses/H-114-two-pose-kernel-exclusion.md).
That target concerns the unrestricted pose domain at side `96/25 = 3.84` and represents
pair compatibility directly.
It seeks a kernel $K$ such that $K-1$ is positive semidefinite, $K(Q,Q)\le b<11$, and
$K(Q,R)\le0$ for every distinct compatible pair.
For a hypothetical packing of $n$ squares, these conditions imply

$$
n^2\le\sum_{i,j}K(Q_i,Q_j)\le nb,
$$

and hence $n\le b$. This is a systematic way to use relations between squares in a
lower-bound certificate.
It does not promise that a small feature family can meet the conditions.
The existing handoff requires a fixed feature family, a reviewed kernel argument, exact
positive-semidefinite evidence, and a credible complete pair-domain verification cost
before a target experiment.
The Memo I control complements that work by providing a small independently reproducible
incidence argument.

## Boundary Conditions and Proof Scope

Stromquist works with open squares of side strictly greater than one.
To exclude unit squares in a container of side smaller than $L$, rescale a hypothetical
packing to side $L$; the small squares then have side greater than one.
Their open interiors are pairwise disjoint, so a marked point is charged at most once.
The strict enlargement also supplies the slack used by the nonavoidance lemmas.

The repository’s closed-core certificates implement a related but distinct convention:
the chosen closed cores must be pairwise disjoint inside the original open square
interiors. One must carry the core-containment and orientation-net guarantees through a
new conditional certificate.
Closed unit squares with merely disjoint interiors can share boundary marks, so the
open-box point-counting conclusion cannot be copied to that setting without the
strict-sublevel reduction.

The implementation separates three obligations: justify the geometric premises,
enumerate their finite incidence consequences, and apply the resource count.
The new Memo I replay completes the latter two as a conditional control.
The subsequent
[segment-helper derivation](reviews/review-2026-09-07-stromquist-segment-helper.md)
independently proves Lemma 8, including localization and all orientations.
An executable helper still needs exact clipping and universal inequality certificates;
the remaining full-proof premises include Lemmas 6–7, the two-mark adjacency assertion,
and the `EH -> J,K` forcing step.
The eleven-square handoff selects the separate H-114 assessment while retaining H-124’s
unresolved near-axis branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
