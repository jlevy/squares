# Review: Incorporating Stromquist’s Memos and Helper Arguments

Stromquist’s 1984 Memo III already states the unrestricted eleven-square lower bound
`2 + 4/sqrt(5)` that the paper’s introduction dates to 2003. Memo II also contains the
ten-square proof that the explainer says he settled in 2003. These chronology
corrections are the strongest candidates for his suggested “tiny revision.”
Only Stromquist can identify his intended hint.
His suggestion to automate preliminary geometric arguments also identifies a difference
from the project’s new fractional certificates, although the repository already verifies
one complete Stromquist-style helper chain.

This independent W2 factual review checked the reader documents and proof record at
repository baseline `07e82d1e` against the three archived 1984 memos and Stromquist’s
2003 paper. Line references below refer to that baseline.
Source conclusions use the archived page images where specified; OCR is a search aid.
This review does not reproduce every geometric lemma in the memos or establish a new
packing bound. The companion source survey is
[Stromquist’s memos and helper arguments](../research/research-2026-09-07-stromquist-memos-and-helper-arguments.md).

## The Likely “Tiny Revision”

| Rank | Candidate | Source evidence | Consequence and confidence |
| --- | --- | --- | --- |
| 1 | Date the preceding lower-bound statement to 1984 | [Memo III](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.pdf), p. 10, explicitly states the unrestricted impossibility for `s < 2 + (4/5)sqrt(5)` | **High confidence as a needed clarification; strongest inference about the hint.** Say “stated in 1984, published in 2003.” The interval since the first statement is about 42 years, while 23 years measures time since journal publication. |
| 2 | Date the ten-square proof to 1984 | [Memo II](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares.pdf), dated October 15, 1984, p. 1 states `s(10)=3+(1/2)sqrt(2)` and pp. 10–15 give the main proof | **High confidence as a correction and strong candidate for the hint.** The explainer says Stromquist settled the case in 2003; say the proof appeared in his 1984 memo and was published in the journal in 2003. |
| 3 | Acknowledge Gustafsson and Thulin’s independent construction | Memo III, pp. 2–4, credits Mats Gustafsson and Magnus Thulin with the `3.877…` construction and cites Gardner’s November 1980 column | **Medium confidence as the intended hint.** Add the rediscovery when discussing history. This source does not displace Trump’s earlier priority claim. |
| 4 | Attribute the six-square helper proof and its segment-length argument to the 1984 memo | [Memo I](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.pdf), pp. 13–18, gives a length-budget incompatibility lemma followed by forced point consumption | **High confidence about the source; lower confidence about the hint.** It is a direct antecedent of systematic compatibility and resource arguments. The email discusses it separately, which makes it less likely to be the concealed item. |

Memo III’s p. 10 aside is a statement of the unrestricted bound, with no supplied
unrestricted point coordinates or detailed proof.
Its actual theorem on pp.
7–10 is restricted to `0°` and `45°` orientations, at `2 + (4/3)sqrt(2)`. The
distinction is already explicit in the
[archive reading aid](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-iii-cases-through-65-and-gardner-conjecture.md),
lines 43–63. Thus “proved in the 1984 memo” would overstate the unrestricted evidence.
The original date and later published derivation can both be credited.

The chronology correction belongs in the maintained [README](../../../README.md), lines
6–7 and 61–64; the
[explainer template](../../../packing/devtools/templates/explainer-article.md), lines
55–58 and its source notes; and any generated introduction using those fields.
The existing “first improvement in 23 years” wording is defensible when explicitly
anchored to journal publication, but leaves out the earlier statement.
Historical experiment records retain the source descriptions used at their original
checkpoints.

The user identified the [public explainer](https://jlevy.github.io/squares/) as the page
Stromquist likely read.
At the audit baseline its source template, lines 90–91, says that Stromquist settled
`s(10)=3+1/sqrt(2)` in `{{PRIOR_YEAR}}`, whose value is 2003. Memo II’s visually checked
opening page dates the note to October 15, 1984 and states the exact optimum.
This corrects a second sentence on the same page, even if the introduction continues to
measure elapsed time from journal publication.

For the construction attribution, the [tutorial](../../../TUTORIAL.md), lines 53 and 92,
uses Trump alone, while the
[long research report](../research/research-2026-08-22-packing-11-unit-squares.md),
lines 366–369, already includes the independent 1980 rediscovery.
Trump’s retained
[2023 author note](../../../packing/resources/papers/trump-2023-packing-11-unit-squares.pdf),
pp. 1–2, identifies his drawing and calculation sent to Gardner in 1979. Neither the
original 1979 correspondence nor the Swedish *Ronden* article is independently supplied
by Memo III. The source therefore warrants additional credit, without adjudicating
priority anew.

The three memos supply no correction to the 2003 Figure 14 coordinates.
Memo I’s Figure 14 concerns six squares; Memo II’s concerns ten; Memo III has no Figure
14\. The independently checked replacement `G'=(.79,1.85)` remains the repository’s
repair, with its attribution and scope preserved.

## What “Pure Dots” Describes Here

The project’s new weighted certificates require **every individual admissible square**
to cover a fixed minimum mass from a common measure.
They then sum those inequalities over disjoint inner squares.
Their only use of the other squares is that disjointness prevents double counting.
These are unconditional weighted dots proofs, consistent with Stromquist’s description.

The weights extend unweighted point counting.
At `s=3.81`, the certificate has 1,121 rational sites with positive rational weights,
total mass `434547/40000`, and exact covering inequalities for the prescribed smaller
squares. The [tutorial](../../../TUTORIAL.md), lines 138–176, and
[certificate implementation](../../../packing/src/sqpack/fractional/certificate.py),
lines 3–31, state this construction and its `D4` symmetry requirement.
The claim is not that ten unweighted dots suffice at `3.81`.

The repository’s complete proof inventory also includes a helper proof.
The repaired Stromquist result T-010 uses ten initial marks to force an avoiding square,
localizes that square, forces three second-stage marks into it, proves a twelve-point
second-stage cover, and finishes with ten remaining squares sharing only nine available
marks. The exact five-node implementation is in
[repaired_cover.py](../../../packing/cases/stromquist/repaired_cover.py), lines
1427–1468;
[H-041](../../../packing/campaign/hypotheses/H-041-repaired-stromquist-point-set.md)
records the accepted scope.
Its second-stage arrangement is chosen after locating the distinguished square.
This is already the preliminary-argument mechanism described in the email.

No archived source examined here proves the email’s stronger historical assertion that
no pure dots proof exists for `n=6`. Memo I supplies the successful helper proof, but
not an impossibility theorem for all five-point hitting sets.
The email is first-person evidence of Stromquist’s investigation with an intern; its
quantifiers, boundary convention, and applicability to weighted measures remain
unspecified. The new five-point derivation reviewed below supplies a precise unweighted
statement independently; a finite failure to find five dots would not establish it.

## Why Removing Symmetry Alone Is Insufficient

For the unrestricted weighted covering problem, averaging over the container’s
symmetries loses no mathematical strength.
This is a direct derivation, rather than a claim imported from the memos.

Let `K=[0,L]^2`, let `G=D4`, and let `mu` be any finite nonnegative measure satisfying
`mu(Q)>=1` for every admissible square `Q` in `K`. Define

$$
\bar\mu(A)=\frac1{|G|}\sum_{g\in G}\mu(g^{-1}A).
$$

The group preserves `K` and the admissible family.
Hence

$$
\bar\mu(K)=\mu(K),\qquad
\bar\mu(Q)=\frac1{|G|}\sum_{g\in G}\mu(g^{-1}Q)\ge1.
$$

Reindexing the finite sum proves `G`-invariance.
If `mu` consists of finitely many rational atoms with rational weights and `L` is
rational, the averaged measure does too; it uses the union of their symmetry orbits.
The same reasoning applies to open or closed squares if the admissible family uses that
convention consistently.

This statement concerns the full covering problem.
A fixed support, an orbit catalogue that omits needed sites, a bound on the number of
atoms, or an angle family not closed under `D4` can prevent that averaging within the
chosen representation.
Averaging also does not turn an unweighted five-point set into another five-point set.
Computational restrictions and the unweighted problem therefore require separate
analysis.

Helper arguments add information the unconditional measure does not express: for
example, that a particular region is occupied, that two incidence patterns cannot
coexist, or that one square consumes several marks.
A branch-conditioned cover may legitimately be asymmetric because the branch has already
chosen a distinguished square’s location.

## The Helper Work Already Attempted

The current record contains continuous-angle helper work beyond the accepted T-010
repair. The following dispositions are fixed in
[H-124](../../../packing/campaign/hypotheses/H-124-full-distinguished-square-compatibility.md)
and [SYNOPSIS](../../../SYNOPSIS.md), lines 623–671.

| Mechanism | Retained evidence | Remaining limit |
| --- | --- | --- |
| Source `0°`/`45°` auxiliaries | H-104 confirms all seven fixed-formula clauses at `q=1939/500` | Exact source orientations alone do not cover neighborhoods of those orientations |
| Continuous near-axis ten-point coverage | H-106 and exp-117 | One-square auxiliary, not a packing theorem |
| Near-45 localization and forced marks | H-108, H-109 and H-123 | Supplies the distinguished-square premises |
| Unchanged unconditional twelve-point cover | H-110 and exp-121 give an exact escaping square | That cover is refuted; H-036 remains unresolved |
| Cover conditional on a common diamond | H-122 and exp-122 give a square avoiding both diamond and nine marks | Refutes the chosen sufficient obstacle; does not decide compatibility with a full square |
| Full distinguished-square compatibility | Exp-125 certifies the entire near-45 branch; exp-124 supplies only a finite no-witness screen | The near-axis branch remains unresolved |
| Collision-augmented near-axis sufficient cover | Exp-127 returns `no_chain`, with no independent reader invoked | No geometric counterexample or completed cover follows; that fixed representation has no allocated retry |

These experiments concern the restricted H-036 theorem, not a new unrestricted bound.
The selected handoff at this review’s baseline assigns BC-264 to assessing an H-114
pair-kernel feature family and its verification cost.
Any further H-124 attempt needs to be considered against that allocation.

## A Bounded Memo I Calibration

Memo I, p. 13, introduces the nine half-grid marks A through I in `[1,2]^2`. Every open
block of side greater than one contains a peripheral mark.
The center mark E cannot be the only mark in its block.
Lemma 8 rules out adjacent isolated marks by comparing the total lengths occupied on two
segments against `1/2`; the scanned page is essential because OCR misreads the fraction
as `2`. On p. 18, Stromquist states that a block containing exactly two marks contains
an adjacent pair, and that the remaining six-block allocation is unique up to symmetry.
It has isolated B, G and I and pairs AD, CF and EH.

The same page then forces J and K into the EH block.
Its final set has eight marks `{G,H,I,J,K,E,L,M}`, with four `{E,H,J,K}` in that block.
A capacity-one count leaves at most four other blocks.
This supplies a control for a reusable incidence engine: enumerate disjoint nonempty hit
masks under declared implications, retain all allowed allocations, reduce them by actual
`D4` actions, and replay the final forced-consumption count.

The frozen calibration criterion is exactly one surviving `D4` orbit under the declared
source premises, followed by the `4 of 8` consumption bound of five blocks.
An independent partition oracle and premise-removal controls must check the finite
enumeration. Allow initially unused marks; do not assume a partition of all nine marks
unless the premises imply it.
Convexity forbids a mask containing two marks while omitting another mark on their
connecting segment. Every geometric premise remains explicitly sourced or proved
separately.

Passing this calibration establishes the finite consequence of the supplied premises.
It does not reverify the continuous-angle geometric lemmas, certify that any surviving
allocation is realizable, prove the absence of a five-dot proof, or improve `s(6)` or
`s(11)`. The second consumer is the existing twelve-mark, forced-triple `n=11` count;
that makes the shared finite resource operation useful beyond this one source example.

## Independent Implementation Review

The finite control is accepted at its declared conditional scope.
Independent review covered [incidence.py](../../../packing/src/sqpack/incidence.py),
[memo1.py](../../../packing/cases/stromquist/memo1.py), and the
[generic](../../../packing/tests/test_incidence.py) and
[source-specific](../../../packing/tests/test_stromquist_memo1.py) tests.
The eight focused tests passed under the project’s Python 3.14.7 in 1.21 seconds.
The attempted `uv run --frozen` command could not access its cache in this sandbox, so
the review used the expressly supported project interpreter.
From `packing/`, the equivalent local command is:

```shell
.venv/bin/python3 -m pytest -q \
  tests/test_incidence.py tests/test_stromquist_memo1.py
```

The production enumerator’s alternatives are exhaustive: the least undecided site is
unused, or it belongs to one chosen allowed mask.
Disjointness removes every point in that mask, and its pair exclusions are checked
against all previously chosen masks.
Every allocation therefore has a unique search path.
The implementation imposes no mask size cap or full-occupation assumption.

The independent source oracle reconstructs convex membership through all segments and
triangles, rather than using the producer’s monotone hull construction.
The planar convex-hull criterion is complete because every point in a finite planar
convex hull belongs to the hull of at most three of its points.
A separate assignment recursion includes an unused bucket and reconstructs the same
complete six-block allocation set.
Both procedures retain precisely four allocations; those form one `D4` orbit and use all
nine marks. The unused-mark outcome is consequently a result, not an input.

The source-local symmetry function enumerates the four rotations and their reflected
images. Tests check preservation of every allowed mask and singleton conflict, then
closure of each reported allocation orbit.
Lemma 8’s exclusions apply only to adjacent perimeter marks, including in the control
that removes the perimeter-hit premise.
Convex closure includes sites on hull edges: finite convex combinations of points inside
an open convex block are inside that block.
Thus these boundary marks cannot be discarded as if the mask described an open convex
hull.

Each of the four premise-removal controls enlarges the allocation set.
The final forced-group control changes the capacity from five to six when one of the
four forced marks is removed.
The generic mass lemma also gives ten for twelve unit-weight marks with three forced
together, checks a fractional example and multiple distinguished blocks, and rejects
overlapping forced groups.
These results validate the finite arithmetic without certifying any continuous geometric
premise.

The retained JSON explicitly sets `full_geometric_proof_verified` and
`new_packing_bound` to false.
There is no implementation soundness finding at this scope.
Review of the accompanying mathematical prose requested two corrections: place the
open-block or pairwise-disjoint-core convention beside the counting lemma, and replace
the proposed H-122-escape test with the current H-124 disposition, since that fixed test
was already executed as exp-124. The author made both corrections, and the revised
passages passed review.

## An Independently Checked Symmetric Five-Dot Obstruction

The source review derived a limited obstruction that can be proved without assuming
Stromquist’s general historical claim.
Every `D4`-invariant set of at most five points in `[0,3]^2` is avoidable by an open
square of side greater than one.
This statement concerns an unweighted set with at most five distinct sites.

Translate the center of the container to the origin.
A noncentral point cannot be fixed by a nonidentity rotation.
Its stabilizer therefore contains either only the identity or one reflection: two
distinct reflections would produce such a rotation.
Its orbit has size eight or four, respectively; only the center has orbit size one.
A set of at most five points can thus contain at most one four-point orbit and the
optional center. The four-point orbit lies either on the two diagonals or on the two
coordinate midlines, since these are the two families of reflection axes under `D4`.

For the diagonal family, take the open diamond with vertices

$$
(3/2,0),\quad(9/4,3/4),\quad(3/2,3/2),\quad(3/4,3/4).
$$

Its side squared is `9/8>1`, and its interior lies in the container with `x-y>0` and
`x+y<3`. It therefore avoids both diagonals, including the optional center, which is its
top boundary vertex.
For the midline family, the open square `(0,3/2)^2` has side squared `9/4>1` and avoids
both `x=3/2` and `y=3/2`. The case containing only the center is covered by either
construction.

The independent mathematical review accepts this orbit classification and both exact
escape geometries. Open boundaries are essential: replacing either escape by its closed
square would invalidate the claimed avoidance.
This proof rules out a symmetric five-dot solution at side three.
The general five-point result below has a different proof; weighted covers with
unrestricted support remain outside both statements.

## Review of the General Five-Point Obstruction

The separately written
[five-dot obstruction](review-2026-09-07-n6-pure-dots-obstruction.md) proves a stronger
statement: every set of at most five points in `[0,3]^2` misses some **closed** square
of side greater than one.
Independent review accepts the complete mathematical argument, including its compactness
extension to point sets that vary with the desired enlargement.
This is a newly reconstructed proof of a precise version of the statement in
Stromquist’s email; it does not establish priority or constitute an adopted campaign
theorem.

The proof separates the case in which a closed axis-aligned unit square already misses
the points. Its positive clearance permits a slightly larger closed square inside the
container. Wall contact causes no problem.
If the unit square has lower coordinates `a,b`, replace its side by `1+delta` and its
lower coordinates by `min(a,2-delta), min(b,2-delta)`. For sufficiently small `delta>0`,
this larger square contains the original, stays in the container and lies within
Euclidean distance `sqrt(2)*delta` of it.
Choosing that quantity below the clearance preserves avoidance.

Otherwise each of the four pairwise-disjoint closed corner unit squares contains a
point. There is at most one remaining point.
Along each boundary strip, translates of a closed unit interval force the relevant
corner points to the inner strip endpoints.
The source derivation’s central, edge-middle and corner cases are exhaustive: corner
regions include their boundaries, edge-middle regions use a strict middle coordinate,
and the central region is `(1,2)^2`. No line at coordinate one or two is omitted.
In the edge and corner cases the opposite two corner points are forced to the inner
corners and all other points are in the opposite outer strip.
An open diamond of side squared `9/8` avoids them.
In the central case, all four corner points are forced onto the two diagonals; of the
four diamond interiors, at most one contains the remaining point.
Shrinking any avoiding diamond by `19/20` makes it closed, preserves avoidance, and
leaves side squared `3249/3200>1`.

For this qualitative proof, compactness supplies the stronger conclusion about a family
of dots depending on the enlargement.
If five-point covers existed for sides `1+epsilon_k` with `epsilon_k` tending to zero,
order and pad the point sets and take a convergent subsequence in the compact space
`[0,3]^{10}`. A closed avoiding square for the limit has positive clearance from every
limit point. It therefore avoids every sufficiently late point set, and contains an open
square of side `1+epsilon_k`, a contradiction.
Thus a whole positive interval of sufficiently small enlargements has no five-point
cover. This compactness argument alone gives no numerical endpoint; the strengthening
below supplies an explicit one by direct geometry.

The theorem excludes arbitrary, possibly asymmetric sets of at most five unweighted
sites in the one-dot-per-square model.
It does not exclude fractional measures with unrestricted support or conditional
resource arguments. The exact rational constructor reviewed below implements the uniform
strengthening; its controls support the geometric calculations, while the universal
quantifiers rest on the reviewed argument.

## Review of the Quantitative Strengthenings

Independent review also accepts the uniform rational version: for every five-point set
in `[0,3]^2`, a closed square of side at least `a=101/100` avoids it.
If a closed axis-aligned square of that side is empty, it is the witness.
Otherwise the same translated-strip argument places the relevant corner sites in
coordinate intervals `[3-2a,a]=[49/50,101/100]` and `[3-a,2a]=[199/100,101/50]`. The
central region is now `(a,3-a)^2`; the corresponding closed corner and edge regions
still account for every boundary.

Use four closed diamonds centered at `(3/2,3/4)`, `(3/4,3/2)`, `(3/2,9/4)` and
`(9/4,3/2)`, with `L1` radius `143/200`. Their distance from an adjacent inner corner
box is at least `18/25`, greater than the radius by `1/200`. Other corner boxes are
farther away. The top diamond has minimum height `307/200>a`, and distinct centers have
`L1` distance at least `3/2>2*(143/200)`. These strict gaps give the same avoidance
argument as before. Their side squared is `20449/20000`, exceeding `a^2` by `47/20000`.
This proves the uniform size claim and, by scaling, excludes a five-point unit-square
cover for every container side at least `300/101`.

A sharper **open-square** conclusion follows from the same inequalities without a
numerical search. Put

$$
L_0=\frac{12+2\sqrt2}{5},\qquad r=\frac{1}{\sqrt2}.
$$

At container side `L0`, use closed axis-aligned unit squares for the first test.
If all are hit, the relevant corner coordinates lie in `[L0-2,1]` and `[L0-1,2]`. Four
open unit diamonds have centers `(L0/2,L0/4)` and its quarter-turn images, with `L1`
radius `r`. Their minimum distance from an adjacent inner corner box is `5L0/4-3=r`; for
a nonadjacent box it is at least `r+1`. Equality is safe because the diamonds are open.
The exact wall clearance is

$$
L_0/4-r=\frac{3-2\sqrt2}{5}>0.
$$

The center distances are at least `L0/2>2r`, so even their closed versions are pairwise
disjoint. The diamond opposite an extra point’s outer strip has its nearest height
`3L0/4-r=(9-sqrt(2))/5>1`. Thus the corner, edge and central cases exclude every
five-point cover of open unit squares at `L0`. Embedding this container in any larger
one extends the conclusion there; points outside the embedded container cannot hit its
squares.

This sharper threshold is accepted as an analytic obstruction for the five-dot method.
It is not asserted optimal.
The equality claim uses open unit squares and must not be reported as a
closed-unit-square witness with positive clearance at `L0`. The rational `a=101/100`
constructor has strict margins and is a separate exact control.
Neither threshold is a new lower bound on packing six or eleven squares, and neither
excludes fractional measures with unrestricted support.

## Final Exact-Constructor Review

The final
[five-point constructor](../../../packing/cases/stromquist/five_point_obstruction.py)
implements the rational `a=101/100` result.
Its axis search partitions each translation coordinate at every site-entry and site-exit
event, including both endpoint faces and one representative of every open interval.
Closed-square membership is constant on each product stratum, so this finite search
exhausts the axis-aligned alternatives for the supplied rational sites.
If none avoids them, the constructor checks all four fixed diamonds of radius `143/200`.

Each witness undergoes a separate exact verification of equal sides, orthogonal adjacent
edges, counterclockwise order, containment, and side squared at least `(101/100)^2`.
Every supplied site must have a strictly separating edge.
This strict inequality correctly rejects a site on the boundary of the closed witness.
The public entry points reject malformed points and non-`Fraction` coordinates before
geometric work. Decimal command-line coordinates are parsed exactly, and floating-point
arithmetic is confined to the optional SVG presentation.

The [test oracle](../../../packing/tests/test_stromquist_five_point_obstruction.py)
checks avoidance using orthogonal projections rather than the production edge
determinants. Controls cover all 126 five-point subsets of a nine-site grid, asymmetric
sites, diamonds, all four container corners, closed-boundary hits, malformed inputs,
corrupted squares, and a square that exceeds side one but fails the claimed `101/100`
minimum. A drift check rebuilds the retained JSON exactly; an SVG check verifies the
serialized presentation structure.

The independent final run used the project’s Python 3.14.7:

```bash
.venv/bin/python3 -m pytest -q \
  tests/test_incidence.py tests/test_stromquist_memo1.py \
  tests/test_stromquist_five_point_obstruction.py
```

All 19 tests passed in 0.56 seconds.
Static and behavioral review found no remaining soundness issue within the stated scope.
The incidence replay remains conditional on the memo’s continuous geometric premises.
The arbitrary-real-five-point proposition and sharper open-square endpoint rest on the
analytic derivations, not on the finite test cases.
Neither retained control claims a new packing bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
