# X027: Seven Corner Marks, Contact Components, and Relational Helpers

Date: 2026-09-10. Author: GPT-6 Astra, max reasoning.
Entry: W3 insight iteration, structural-helper lane of X027; coordinator bead
`think-jx95`. Status: analytical derivations with independent cross-review.
The fractional-duality and certificate-mechanisms lanes independently checked Lemmas A
and B, the 80 abstract incidence patterns, the distinct-owner count and the
normalized-component consequence; both dispositions were PASS. The fractional reviewer
also re-read BC303’s exact source and checked the surplus identity and the
corner-to-corner contact-path consequence.
The coordinator separately checked the elementary arithmetic.
These are reviewed deductions from admitted inputs, not frontier claim registrations.
The proposed discriminators are unrun.
No bound, campaign verdict, or new target measurement is claimed.

The admitted corner measure forces **at least seven of the eight corner marks to be
owned**. The existing account extracts only one owned mark per corner from the same
inequality. Three corners therefore have both marks owned, either by one core or by two
distinct cores. This gives stronger occupied geometry in the first case and an extra
selected owner in the second.
Separately, an incircle argument bounds the number of squares touching one wall by three
at `q=96/25`; the admitted adjacent-wall normal form therefore has at most three
physical contact components.

These deductions suggest using allocation constraints and relations between full owners
before multiplying the number of footprint classes.
BC329 remains the next direct global-bound target, and BC337 remains the prepared
single-owner domain continuation.
The proposals here are mathematical departures to evaluate alongside that work, not
authorization to rerun either target.

## 1. Fixed Premises and the Current Negatives

The corner argument uses exactly the
[BC303 ownership measure](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md#3-replay-of-the-corner-pair-theorem-lane-c):

| Item | Fixed value or convention |
| --- | --- |
| Container | `q=96/25` |
| Selected core side | `B=9977/10000` |
| Net mismatch bound | `D=207107/90000000`, with the admitted 181-direction representation and symmetry transfer |
| Measure | 377 point atoms; total `M=22524199/2000000` |
| Core charge | At least one for every admitted core, independently replayed |
| Uncovered allowance | `epsilon=M−11=524199/2000000` |
| Eight corner marks | The complete D4 orbit of `(3152/3175,2336/3175)` |
| Weight of each mark | `w=106251/800000` |
| Ownership | Membership in a selected **closed** core; boundary membership counts |

The selected cores are strictly contained in their unit parents.
Consequently cores of different squares are disjoint as closed sets, even when parent
boundaries touch.
No core contains marks from different corners: the source verifies that
the least cross-corner squared distance is `34668544/10080625`, greater than
`2 B^2=99540529/50000000`.

The [evidence report](research-2026-09-09-n11-evidence-and-inference.md) and
[X026](../../../packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md)
keep the relevant failures separate:

- T023 excludes one specified four-owner branch at `q`, with its admitted symmetry
  transports. It supplies neither all raw class closure nor routing of every physical
  packing to an excluded selection.
- Exp150 supplied separate B-core owners compatible with exp149’s escape.
  Exp151 concerns a different escape;
  [exp156](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-156-unit-parent-saved-residual.md)
  completely excludes that escape against its TR owner already in the B-only model.
  Repeating the TR parent comparison cannot measure parent gain.
  BL, BR and TL were not evaluated by exp156.
- Exp152’s two retained escapes intersect.
  Exp153 excludes every sixth site added to the fixed five-site pattern on its named
  relaxation. Neither result is a disjoint two-core obstruction to arbitrary added mass.
- The translated depth-one family has
  [explicit individual unit parents](../reviews/review-2026-09-10-n11-parent-domain-translation.md)
  from `3.82345`. Tightening isolated parent realizability cannot remove that point-only
  obstruction at `3.827` with the retained B and directions.
  Full-owner compatibility, ownership, joint realizability and changed charge languages
  remain additional conditions.
- Neutral classes in the retained patch model, including cores 59 and 60, obstruct point
  closure of those domains.
  They do not establish that a physical packing admits only neutral selections.

The last two statements are proved at their own regimes.
They are not identities between the `3.827` global problem and the `3.84` owner problem.

## 2. Seven of Eight Marks Are Owned

**Lemma A, independently reviewed.** Every hypothetical eleven-unit-square packing in
`[0,96/25]^2`, with the admitted core selection above, owns at least seven of the eight
corner marks.

**Proof.** Write the disjoint selected cores as `C_1,...,C_11`. Their total captured
measure is at least eleven, so

$$
\mu\!\left([0,q]^2\setminus\bigcup_{i=1}^{11}C_i\right)
=M-\sum_{i=1}^{11}\mu(C_i)\le\epsilon.
$$

Any two unowned corner marks would contribute `2w` to this uncovered measure.
But

$$
2w-\epsilon
=\frac{106251}{400000}-\frac{524199}{2000000}
=\frac{441}{125000}>0.
$$

Thus at most one of the eight marks is unowned.
This uses the same global uncovered allowance once, rather than applying it
independently to each corner.
∎

This is a consequence of the admitted measure, not a new certificate or a new lower
bound. It also applies to a smaller packing embedded in the same `q` frame; moving the
marks to the smaller container’s own corners would be a different statement.

### Co-ownership or an additional owner

At least three corner pairs are fully owned.
Each fully owned pair has precisely one of two incidence types:

- **Co-owned:** one selected core contains both marks.
- **Split:** two distinct selected cores contain the two marks separately.

Closed-core disjointness makes the owner of an owned mark unique.
A core cannot serve two different corners by the cross-corner distance inequality.
Therefore the set of **all** cores owning any of the eight marks has cardinality

$$
k=4+s,
$$

where `s` is the number of split, fully owned corner pairs.
If all eight marks are owned, `0<=s<=4`; if exactly seven are owned, `0<=s<=3`.
Selecting these distinct owners leaves `11-k=7-s` physical residual squares.

At the incidence level there are only

$$
2^4+8\,2^3=80
$$

patterns: sixteen with no missing mark and sixty-four obtained by choosing the unique
missing mark and the co-owned/split type at each of the other three corners.
These are **abstract ownership patterns**, before sectors, positions, angles or
geometric feasibility.
They are not eighty feasible packings and do not replace continuous owner domains.
The actual pattern of a packing belongs to this list without making an arbitrary
four-owner selection first.

A co-owned pair supplies the whole segment between its marks by convexity.
At one retained core orientation `r`, its exact centre domain includes the condition

$$
z\in(m_1-S_r)\cap(m_2-S_r),
$$

where `S_r` is the centred side-B square; containment, parent restrictions and any
sector conditions must also be intersected.
A split pair instead supplies two owners with joint disjointness and two distinct roles.
Keeping only one owned mark discards one of these two kinds of information.

There are immediate controls against overclaiming.
The retained neutral cores 59 and 60 themselves contain both bottom-left marks, so
co-ownership alone does not eliminate their fixed-family point obstruction.
The
[X022 counterexamples](../../../packing/campaign/explorations/X-022-segment-ownership-continuation.md)
include two adjacent split corner pairs carried by four diamond squares.
Adjacent split pairs cannot be declared incompatible merely from their labels.

### A common surplus budget

The same measure gives a resource inequality for these patterns.
Put

$$
U=\mu\!\left([0,q]^2\setminus\bigcup_iC_i\right),
\qquad \sigma_i=\mu(C_i)-1\ge0.
$$

Then the exact identity is

$$
U+\sum_i\sigma_i=\epsilon.
$$

For an ownership pattern with `u` missing marks, `u` is zero or one and `U>=u w`.
Suppose each corner’s declared role has a certified lower bound `gamma_c>=0` on the
**combined surplus of its distinct owners**. Owners at different corners are distinct,
so every physical realization must satisfy

$$
u w+\sum_c\gamma_c\le\epsilon. \tag{1}
$$

With one missing mark the remaining surplus allowance is exactly

$$
\epsilon-w=\frac{517143}{4000000}.
$$

Equation (1) is a way to use one common measure across co-owner and split-owner helpers.
A strict reverse inequality excludes that pattern.
The missing-mark charge cannot be counted again as owner surplus, and the same owner
cannot contribute to two corner minima.
Arbitrary independently chosen measures do not give this sum.

This is a modest extension of the weighted ownership-transfer mechanism in
[X021](../../../packing/campaign/explorations/X-021-what-can-be-proved-about-eleven-squares.md).
Its benefit is unmeasured: all useful `gamma_c` might be zero on the required domains.

### First discriminator and stopping rule

Lemma A and the 80-pattern incidence calculation use the already reviewed eight weights
and total mass; their independent mathematical cross-review has passed.
No new geometric target is necessary for that deduction.
A maintained finite allocation reader, if commissioned, should derive the owner count
from mark-to-core identities and reject double-counted owners; its controls should
include zero, one and two missing marks and the retained adjacent split-pair
construction.

The first geometric target should use a fixed retained source, not eighty new LPs.
One option is to freeze the four symmetry-related, explicit neutral co-owner poses
derived from core 59 at `q`, first verify their full unit parents and mutual
compatibility, then screen the same retained 88-core family against those **full
parents**. Compare its surviving weight with the seven-unit requirement and the matched
core-only obstacles.
This asks whether parent geometry coupled to actual co-owners removes the known
obstruction. No such screen was run here.

Strictly lower survivor weight would remove this particular obstruction and justify one
positive-width owner-cell follow-up; it would not establish a residual cover.
Surviving weight at least seven would stop this fixed-source point-only direction.
Either outcome leaves other incidence patterns, threshold charges and routing open.
A fixed-pose success cannot be silently treated as a whole co-owner class.

An alternative discriminator is one complete local surplus minimum for a fixed co-owner
or split-owner cell under the 377-atom measure, compared with the allowance in (1).
Choose between these after checking which existing exact instrument needs less new
surface; do not fund both by default.

## 3. Owner Choice Is a Routing Problem

For each physical packing `P`, fix its admitted selected cores.
Let `A_c(P)` be the nonempty set of all valid mark/sector owner labels at corner `c`,
retaining every admitted sign and boundary choice.
Since cores from different corners are distinct, independent local choices combine into
the product

$$
\Gamma(P)=\prod_c A_c(P).
$$

If `G` is the set of excluded tuple labels, sufficient routing is

$$
\forall P\text{ feasible at }q,\qquad\Gamma(P)\cap G\ne\varnothing. \tag{2}
$$

Labels record too little to imply geometric feasibility.
In particular, a raw neutral tuple is not a counterexample to (2).

An elementary finite toy shows the difference.
Give two corners labels `a0,a1` and `b0,b1`, and exclude `(a0,b0)` and `(a1,b1)`. Every
packing with both choices available at either corner routes to an excluded tuple, since
the other availability set is nonempty.
Only the two opposite singleton availability pairs remain bad.
Excluding those **forced-choice situations** suffices; one need not separately exclude
every configuration that admits an off-diagonal label.

For the real finite label set, every unsuccessful availability product lies inside a
maximal product of nonempty label subsets disjoint from `G`. These maximal products give
a finite list of candidate no-routing situations.
Lemma A imposes additional mark-availability restrictions on that list, while
co-ownership records whether two labels refer to the same core.

The first routing discriminator should construct this abstract remainder from the
actually certified T023 transports and the seven-mark rule, then identify one geometric
implication that excludes a remainder.
A shorter abstract list alone is not a theorem about physical packings.
Stop if the reduction leaves essentially the same geometric obligations or if a proposed
implication fails a retained local counterexample.
Reopen when another certified tuple or an independently proved incidence implication
changes the remainder.

## 4. Relations Retain Information That Footprints Lose

Let `O_c` be the admissible poses of one owner class and let `R` be a residual core.
Define

$$
F_c(R)=\{Q\in O_c:Q\cap R=\varnothing\}.
$$

For physical parents use their physical non-overlap rule; the displayed closed-core
version is appropriate when both shapes are strict selected cores.

The single-owner test asks whether `F_c(R)` is empty.
For several residuals the necessary condition is stronger:

$$
\bigcap_{i=1}^tF_c(R_i)\ne\varnothing. \tag{3}
$$

The same owner must coexist with all residuals.
Separate nonempty sets do not establish (3). A finite toy uses two allowed owner poses,
`Q0,Q1`: residual `R0` is compatible only with `Q0`, and `R1` only with `Q1`. Each
residual passes the isolated test, but their pair cannot coexist with any permitted
owner. This is a logical counterexample, not a constructed square-packing configuration.

There is a second consistency condition between different owners: choosing one pose from
each `F_c(R)` must also give mutually compatible owners.
Even nonempty relations for every pair of owner classes need not give a common tuple.
Three two-valued roles with pairwise “different value” constraints are the smallest toy:
each pair is satisfiable, but the triple is not.

These distinctions identify two finite relaxation levels worth testing:

1. Retain one owner variable shared by two residuals; exclude the pair when (3) fails.
2. Retain two or more owner variables and their mutual compatibility, instead of
   selecting a separate witness for every constraint.

The current BC337 construction is the unary predecessor.
For residual shape `S`, its all-owner-incompatible centre region is

$$
K_c=\bigcap_{Q\in O_c}(Q+(-S)).
$$

The common-footprint obstacle is only

$$
\left(\bigcap_{Q\in O_c}Q\right)+(-S)\subseteq K_c.
$$

Minkowski addition need not commute with intersection.
BC337 already targets this difference for TR, so rebranding it as a new pairwise idea
would duplicate active work.
The new proposal retains the **same** owner across multiple residuals or across an
incidence pattern.

The prepared
[two-attainer construction](../../../packing/cases/n11_five_dot_cover/two-attainer-source-admission.md)
would, if its target passes, supply two disjoint D-missed cores in the patch relaxation.
Before using such a pair as an obstruction on a stronger conditional domain, recheck the
relevant shared-owner constraints.
If the pair fails (3), its obstruction does not transfer there.
If it passes, that establishes only the tested owner consistency, not eleven-square
feasibility. Exp149 and exp151 are an unsuitable substitute: their cores intersect, and
exp151 already fails the complete TR unary test.

**Discriminator:** after a source-bound pair with positive unary controls exists, freeze
one owner class and ask whether its complete pose domain admits one owner compatible
with both. A strict pair exclusion absent from the unary control earns a small
joint-domain or conditional-capacity instrument.
A compatible common owner stops that particular pair.
Exhausting an arbitrary pose sample proves neither outcome for the continuum.

Pair incompatibility can produce new capacity inequalities only after the charged events
are defined and universally checked.
A graph on a finite retained fractional support may expose a missing inequality; it does
not automatically implement that inequality in the existing point or threshold
certificate language.

## 5. A Wall Has at Most Three Touching Squares

**Lemma B, independently reviewed.** In a packing of unit squares at `q=96/25`, at most
three squares touch any one container wall, including vertex contact.

**Proof.** Consider the left wall.
For a square with folded orientation `theta`, its coordinate half-width is

$$
h(\theta)=\frac{|\cos\theta|+|\sin\theta|}{2}
\in[1/2,\sqrt2/2].
$$

A left-wall contact puts the centre’s x coordinate at `h(theta)`. For two such squares,
`|Delta x|<=(sqrt(2)−1)/2`. Each square contains its open radius-1/2 incircle, so their
centre distance is at least one.
Thus

$$
|\Delta y|\ge\eta
=\sqrt{1-\left(\frac{\sqrt2-1}{2}\right)^2}
=\frac{\sqrt{1+2\sqrt2}}{2}.
$$

All centre y coordinates lie in `[1/2,q−1/2]`, an interval of length `q−1=71/25`. Four
centres ordered by y would require a span at least `3 eta`. But
`9 eta^2=9(1+2 sqrt(2))/4>171/20>(71/25)^2`, using `sqrt(2)>7/5`. This is impossible.
The other walls follow by symmetry.
∎

The proof works whenever `q<1+3 eta`. Equality at this sufficient threshold is outside
the stated exclusion.
Three touching squares occur already in an axis-aligned column, so this cap for
arbitrary packings cannot be reduced to two at `q` by the same premises.

### At most three normalized contact components

Apply the independently reviewed
[fixed-side normal form S1](../reviews/review-2026-09-10-n11-structural-normal-forms.md)
to a hypothetical packing at `q`. It gives a representative with unchanged labelled
orientations in which every physical contact component touches both left and bottom
walls. Distinct components use distinct left-wall squares.
Lemma B therefore gives **at most three contact components**, and some component
contains at least four of the eleven squares.

This conclusion is existential for the normalized representative.
It does not hold for every untranslated configuration.
Select corner-mark owners **after** normalization, since the motion can change their
labels. Lemma A still applies to the normalized packing because its side and admitted
core premises are unchanged.

There is also a joint owner/contact consequence.
Select one core owner at each corner after normalization.
Their four distinct parents occupy at most three physical contact components, so some
component contains owners from **two different corners**. A genuine parent-contact path
therefore connects those corner roles.
This supplies six possible unordered corner pairs as endpoint types, with arbitrary
allowed intermediate squares.
The component containing that path need not be the one containing at least four squares.
Strict cores need not touch along a parent-contact path.

A component of four or more squares need not contain a long simple path; a star is a
combinatorial counterexample to that inference.
Physical contacts need not have positive length, the component need not be rigid, and
its squares need not share angles.
The existing snug-square versus paths of lengths two through eleven remains the valid
adjacent-wall alternative.

The new finite reduction is by one, two or three **physical components**, with at most
three wall-contact carriers per wall.
It suggests charging several connected squares together, or imposing their common wall
constraints on a residual pilot.
It does not justify a broad enumeration of contact graphs yet.
The first useful target should remove a declared fractional obstruction with a complete
small anchored component cell; a count of possible graph labels by itself supplies no
exclusion.

## 6. Continuous Segment and Angle Profiles

Stromquist’s reusable contribution is the resource shared by several squares under an
incidence pattern. The
[independent Memo I helper](../reviews/review-2026-09-07-stromquist-segment-helper.md)
compares one owner’s required segment length with the portion accessible from its owned
mark after another owner is placed.
Its `1/2` constants concern the source’s six-square geometry and cannot be imported at
`q=96/25`.

For a candidate n11 helper, choose finitely many segments `I_j` and nonnegative
coefficients `a_j`, and use strict cores so their traces are disjoint.
Then

$$
\sum_i\sum_j a_j\,\operatorname{length}(C_i\cap I_j)
\le\sum_j a_j\,\operatorname{length}(I_j).
$$

An owner-specific lower bound can depend continuously on its angle.
For a relational version, let the segments start at a mark `p` owned by core `A`. If
another core `B` is disjoint from `A`, convexity implies that `A`’s trace on each
segment lies in the component of `I_j\setminus B` accessible from `p`. Summing the whole
free complement would lose this restriction.
A uniform lower demand for `A` greater than the accessible capacity left by `B` excludes
their incidence/angle cell.

Lemma A supplies a reason to investigate such cells: it limits missing marks and
identifies co-owned segments or split-owner pairs.
The complete incidence pattern also specifies the other marks that each selected core
avoids. These are the kind of containments and exclusions the Memo I argument needs.
A core’s merely passing near a segment gives no positive length lower bound; the
[X022 segment capacities](../../../packing/campaign/explorations/X-022-segment-ownership-continuation.md)
are separate facts with their own ownership and tolerance conventions.

The first discriminator should fix one surviving incidence pattern and one pair of angle
intervals, derive exact clipping formulas and the accessible components, then ask
whether a strict demand-capacity gap holds throughout that cell.
Half-angle coordinates make the formulas rational on each facet case.
A midpoint sweep is only proposal work.
Axis endpoints, cap changes and equality cases belong to the proof.

If independent global angle minima remove every surplus, retaining the joint profile
`d(theta_A)−b(theta_B)` may still help on a proved compatibility relation.
Replacing continuous profiles by two exact angles has no justification.
A complete global result must retain the other angle cells or establish a routing
theorem into the excluded ones.
Stop a pilot when a verified admissible pair defeats its proposed uniform gap; reopen
only with a new incidence restriction, segment resource or angle relation.

## 7. Choice of the Next Structural Slice

| Direction | New information sought | First decision-changing result | Main limitation |
| --- | --- | --- | --- |
| Seven-mark allocation and common surplus | More owned marks, extra distinct owners, or paired containment | Independently admitted lemma; then one source-bound geometry or surplus comparison | The 80 patterns still contain continuous geometry |
| Shared-owner relations | One owner must serve several constraints simultaneously | Positive unary controls but a complete negative joint result on one frozen pair | A pair inequality needs an admitted conditional capacity or joint-cover consumer |
| Contact-component resource | At most three normalized components, one containing at least four squares | One whole component cell removes a retained obstruction | Neither a short path nor shared angles follows |
| Segment/angle helper | Geometric incidence changes accessible length or required charge | A strict exact gap on a positive-width cell | Full cell coverage and remaining branches are substantial |

The first two deductions have passed independent mathematical cross-review; their proofs
need no target computation.
For the next implemented structural block, prefer one source-bound seven-mark/co-owner
comparison or one shared-owner pair discriminator; choose according to which can produce
a consequential exact result with the admitted geometry.
The segment helper is the more ambitious follow-up once a surviving incidence pattern
has been identified.

The two-attainer target is worthwhile only if its result changes that choice.
The individual-parent negative at TR is settled, the isolated-parent global obstruction
has explicit realizations, and neutral patch refinement alone has named counterexamples.
BC329 can proceed as the direct bound lane while these structural propositions are
narrowed into a separate finite contract.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
