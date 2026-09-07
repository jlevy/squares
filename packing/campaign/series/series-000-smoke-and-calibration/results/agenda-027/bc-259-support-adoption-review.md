# BC259: Independent Support-ceiling Adoption Review

The contributed seven-row argument has a sound upper-bound contract, and its source
formulas match the current Trump construction symbolically.
Fund a bounded, history-free independent checker if the two source assessments agree.
Do not yet adopt the ceiling: this review did not reconstruct the current support or
verify the seven boxes on it.

This is the independent `think-am7h` assessment for Session095, dispatched at 2026-09-07
11:52:47 UTC with an original deadline of 12:22:47 UTC. The first observed task clock
was 11:53:51 UTC. The parallel author’s assessment was not inspected.
Only this note was written; no scientific constructor, geometry calculation, test,
optimizer, target, or archived executable was invoked.

## Source Identity and Its Remaining Check

The
[archived checker](../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/original_review/certificate/check_support_ceiling.py),
lines 47–89, uses the same polynomial and isolating bracket as
[the current source](../../../../../cases/trump11/packing.py), lines 25–28 and 45–94.
Their parameter is the half-angle variable $u$, not the container side:

$$
P(u)=5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1,
\qquad 36/100<u<37/100.
$$

The container side is $L=(6u+4)/(1+2u-u^2)$. It is not the fixed $1939/500$ side of the
separate H124 work. On this bracket, $u>0$, $1-u^2>0$, and all denominators in the
following formulas are nonzero.
Both sources define $c=(1-u^2)/(1+u^2)$ and $s=2u/(1+u^2)$; the identity $c^2+s^2=1$ is
algebraic.

| Archive name | Current name | Formula |
| --- | --- | --- |
| `L` | `side` | $(6u+4)/(1+2u-u^2)$ |
| `r` | `r1` | $1-(L-3)c$ |
| `a` | `u1` | $((1+r)c-1)/s$ |
| `v` | `v1` | $c-s$ |
| `b` | `v2` | $(L-1)/s-r-(3+a)c/s$ |
| `x` | `x0` | $1+2/c-(L-2)s/c$ |

The six axis-aligned squares and five tilted squares occur in the same original label
order.
Both tilted constructors apply $(X,Y)\mapsto(1+cX-s(Y-r),1+sX+c(Y-r))$ to the same
four local unit-square corners.
A read-only Git comparison found no change to `cases/trump11/packing.py` from the
archive’s cited source revision `4d305597` to the reviewed checkout.

The archive’s derivative coefficients are the derivative of $P$. Its interval arithmetic
encloses addition, subtraction, multiplication and division away from zero; successful
strict signs therefore imply the corresponding exact signs.
Its 100-interval derivative cover and 80 bisections are a contributed root certificate,
not an independently replayed result in this review.
A new reader can instead use the accepted `NumberField` root on the same bracket.
That shares the field and seed; it must not be described as independently deriving
Trump’s construction.

Let $\mathcal R(x,y)=(L-y,x)$ and $F(x,y)=(L-x,y)$. As closed geometric squares, with
corner ordering ignored,

$$
Q_1=\mathcal R Q_0,\qquad Q_3=\mathcal R^3Q_0,\qquad Q_5=\mathcal RFQ_4.
$$

These identities follow directly from their axis-aligned coordinates.
Consequently the archive’s representatives $(0,2,4,7,10,8,6,9)$ cover the D4 closure of
all eleven current seeds.
For $Q_0$, the skipped reflected images are already rotations because
$FQ_0=\mathcal RQ_0$. Thus the archive’s list and the current 88-image construction have
the same geometric set before any numerical comparison is needed.

Set equality alone does not establish that the archive’s 60 listed entries are distinct,
or identify their order in the current coefficient-key quotient.
The archive checks distinct centers; the current code deduplicates complete corner sets.
The latter also handles different squares with the same center.

The retained
[source review](../agenda-026/bc-254-target-readiness-independent-review.md#mathematical-checks)
establishes 88 labelled images, 60 distinct placements and eight orbits for the current
source. Combined with the symbolic set equality, that accepted cardinality implies that
the archive’s 60 listed placements are distinct.
Its eight representative classes cover eight orbits, so they cannot duplicate a class
either. This inference uses the retained current-source verification; it is not a fresh
replay of the archive’s center test.
The expected correspondence is:

| Archive column | Representative | Original labels in the orbit | Size | Average weight per distinct member |
| ---: | ---: | --- | ---: | --- |
| 0 | 0 | 0, 1, 3 | 4 | $3/4$ |
| 1 | 2 | 2 | 8 | $1/8$ |
| 2 | 4 | 4, 5 | 8 | $1/4$ |
| 3 | 7 | 7 | 8 | $1/8$ |
| 4 | 10 | 10 | 8 | $1/8$ |
| 5 | 8 | 8 | 8 | $1/8$ |
| 6 | 6 | 6 | 8 | $1/8$ |
| 7 | 9 | 9 | 8 | $1/8$ |

Adoption must determine a permutation $\pi$ by comparing each representative’s full D4
corner-key set with a current orbit.
The source packet names the displayed order, but sizes and original counts alone cannot
identify the six singleton seed orbits.
Do not assume $\pi$ is the identity.
Apply the same permutation to row columns, orbit sizes and baseline weights, retaining
all 88 labels `(seed, reflection, turn)`. This review did not perform that
current-coordinate comparison.

## What the Seven Rows Would Prove

Write $a_j\ge0$ for the weight of each distinct member of orbit $j$, and
$d=(4,8,8,8,8,8,8,8)$. A source-bound row records the number of distinct members of each
orbit containing a whole positive-area box in their interiors.
Constant incidence on that box makes $R_i a\le1$ necessary for almost-everywhere depth
at most one: the box cannot be contained in the exceptional null set.

The archive fixes seven centers, radius $1/100000$, the matrix $R$, and
$\lambda=(1,3,1,1,5/2,1,3/2)$ in lines 91–131. Hand substitution into the printed
integer rows gives the eight columns of $\lambda^T R$ as

$$
(1+3,\ 1+6+1,\ 1+2+5,\ 2+5+1,\ 1+1+1+5,
 2+6,\ 2+3+3,\ 2+1+2+3)=(4,8,8,8,8,8,8,8).
$$

The nonnegative multipliers sum to eleven.
Therefore, once the geometric rows are verified, $d\cdot a=\lambda^TRa\le11$. This needs
no optimizer, matching finite-row primal, arrangement enumeration, or assumption of
strong duality.

For an arbitrary feasible weighting on the complete support, average its eight D4
transforms. The group preserves the container and permutes the support, so total mass is
unchanged. The union of the eight transformed exceptional sets is null; the average is
still almost-everywhere feasible and is constant on each orbit.
The ceiling therefore bounds nonsymmetric weightings as well.

The matching lower bound uses the accepted original eleven-square packing.
Averaging its eight images assigns each distinct placement its preimage count divided by
eight. The expected multiplicities are six on four placements, two on eight, and one on
48: $4(6)+8(2)+48=88$. This gives the displayed baseline and mass eleven.
Packing boundary contacts cause no problem: the finite union of square boundaries has
area zero. Replaying the seven finite rows alone would not establish this baseline’s
global feasibility; the original packing verification does.

Thus verified rows and source binding, together with that lower-bound premise, would
establish attained fixed-support optimum eleven and reject
[H099](../../../../hypotheses/H-099-trump-d4-finite-support-dual.md) under its existing
criterion. They would not prove a mass-eleven area density, a ceiling for placements
outside this support, continuum attainment, or any global packing bound.

The archive’s eighth box and claimed candidate depth $7/5$ are separate evidence.
They are unnecessary for the support ceiling and should not enter the smallest adoption
call. A later accepted ceiling would not turn exp115’s pair result or exp126’s graph
clique into a verified common-interior witness.
Preserve those historical records and exp113’s finite-row value $56/5$.

## Why the Existing Packet Reader Is Not the Adoption Interface

[The existing independent reader](../../../../../devtools/check_full_size_density_support_ceiling.py)
has useful public source reconstruction at lines 161–212: explicit D4 maps, complete
preimages, exact geometry and containment checks, original-packing verification, and the
averaged baseline. The corresponding producer functions are
[`bind_source` and `support_metadata`](../../../../../src/sqpack/full_size_density/support_screen.py),
lines 61–95 and 253–271.

Its `replay_packet`, lines 246–338, additionally requires exp113’s primal, solve-count
receipt, center-first row dispositions and dyadic extension history.
The seven contributed boxes are a different frozen row protocol.
Neither invented history nor a call to private `_replay_upper` is an acceptable adapter;
the public `replay_upper` intentionally refuses targets outside its side-two controls.

There is also a geometric admission difference.
The legacy row replay requires distance from every infinite supporting line, even for an
already excluded square.
The archive needs either four strictly inward edge forms throughout the box or one
strictly outward form throughout it.
An exterior square’s other supporting lines may cross the box without changing
membership. The legacy requirement is sufficient but stronger, so its refusal would not
invalidate the archive’s box semantics.

## Smallest Independently Bound Adoption Contract

One new public, history-free reader is sufficient to test the contributed evidence.
The archive already supplies the proposed rows and retained same-code receipts; there is
no need to rebuild its exploratory LP or a new search producer.
The new entry point must be reviewed and controlled before a scientific invocation.
The full-incidence contract below is the direct adoption route; the cheaper variant that
follows can replace its third step if selected prospectively.

1. Bind the immutable current source identifier, the half-angle polynomial and real
   embedding, and all eleven original seeds.
   Use public `reconstruct_source` for the separately structured D4 enumeration;
   disclose the shared seed, field arithmetic and packing verifier.
   Reconstruct the complete support metadata, verify the 88/60/8 counts and all labelled
   preimages, and establish $\pi$ by complete orbit-key equality.
   Input metadata, if supplied, must match in full.
2. Admit exactly the seven archived centers, the fixed positive radius, their
   representative-labelled rows, and the seven nonnegative rational multipliers.
   Use a closed, bounded data format; ignore no extra row or unknown field.
   A bounded JSON loader must reject duplicate keys, floats and expansion syntax before
   rational conversion.
   Never construct an arbitrary field from the packet.
3. Independently check each closed box inside the container and classify all 60 squares.
   For a cyclic square, orient each edge form inward.
   Its extrema on an axis-aligned box occur at box corners.
   Inclusion requires every edge minimum to be strictly positive; exclusion requires at
   least one edge maximum to be strictly negative.
   Otherwise refuse. Recompute the orbit counts and compare every mapped row; a
   `margin_positive` Boolean from the archive is not evidence.
4. Verify $\lambda\ge0$, $\lambda^TR=d^T$ and $\sum\lambda=11$ directly.
   Verify the independently reconstructed original packing and averaged mass eleven.
   The frozen certificate needs no finite-row candidate primal or solver receipt.
5. Return the source identity, full support/preimage metadata, permutation, seven
   geometric row results, exact multiplier identity and scoped ceiling.
   Only a completed positive result with literal verified predicates may support
   adoption. Parse refusal, source mismatch, changed constants, geometric ambiguity,
   timeout or partial output leaves adoption unresolved, with no automatic retry.

The full-classification corner method requires at most $7\cdot60\cdot4\cdot4=6720$
edge-form sign checks, plus source validation and eight orbit bindings.
It can require fewer by reusing exact affine extrema; every square’s classification must
still be accounted for.
This is an operation inventory, not a target runtime measurement.

### Cheaper ceiling-only row predicate

For the ceiling, an alternative needs only the positive inclusions.
In row $i$, select $R_{ij}$ distinct members of each orbit $j$ and prove that each
selected square contains the entire fixed box strictly.
For every nonnegative weighting and every point in that box, these selected
contributions give a lower bound $R_i a$ on the full depth.
Consequently $R_i a\le1$ is necessary even if unselected squares have not been
classified. The same multiplier proof gives the ceiling unchanged.

The seven printed rows request $3+3+7+6+6+8+8=41$ selected incidences.
With supplied member identities, their inclusion checks require at most
$41\cdot4\cdot4=656$ edge-form signs.
A history-free checker could instead find the first required number of strictly
containing members in each independently reconstructed orbit; discovery could still scan
all 60 placements. It must refuse if any quota is unmet, count no member twice within a
row, and retain the selected identities.
Full 88-image source binding is unchanged; the omitted work is only exclusion
classification.

This alternative is a necessary-lower-incidence certificate, not a direct replay of all
exact incidence signs.
H099’s current prose describes constant-incidence rows, and exp113 freezes a particular
row-generation history.
Name the new history-free predicate prospectively before invocation; its sufficient
proof does not alter the support claim or its ceiling criterion.
Here the printed rows also satisfy $R_i a^{\rm avg}=1$ for every $i$, and every
component of the accepted baseline $a^{\rm avg}$ is positive.
Thus any additional interior intersection with a box would create a positive-area depth
violation for that baseline, contradicting its known feasibility.
This gives exact interior incidence as a deduction if needed; it does not supply the
archive’s strict exclusion margins.
The ceiling itself needs no such extra deduction.

I recommend this positive-inclusion predicate if the coordinator selects a ceiling-only
instrument. The full-classification version remains a valid, more demanding adoption
check. Neither version has been run here.

Source-free controls must forbid the Trump factory and the legacy algebraic toy that
uses the Trump field.
Use unrelated rational and quadratic sources.
Cover duplicate geometric images and their labels, nontrivial orbit permutations, equal
centers with different squares, reflected corner order, full-box inclusion and
exclusion, an exterior supporting-line crossing, a box crossing an actual square
boundary, container escape, zero radius, malformed coefficients, changed incidence or
multiplier, missing rows, wrong embedding, and resource interruption.
For the positive-only variant, also reject repeated selected member identities within a
row and unmet inclusion quotas; verify that an unclassified member cannot contribute to
a quota. At least one valid upper certificate must be accepted; a reject-everything
reader is not ready.

## Funding and Stop Condition

The next useful allocation is a focused source-free reader/API slice, not another
candidate or arrangement run.
A prospective estimate is 15–20 author minutes plus 5–10 minutes for independent
code/control review and integration.
The second 30-minute BC259 allocation is justified only if the coordinator can name the
history-free entry point, its frozen data, its independent geometry check, and who owns
each review. It is not enough to have a wrapper around `replay_packet`.

The
[exp113 independent review](../exp-113-h-099-trump-support-screen/independent-review.md#output-review)
retains a 9.10-second file replay with 20 rows and additional history checks.
That is useful scale evidence, not a forecast for the new reader’s exact-corner method.
After source-free controls, review, immutable validation and a committed prospective
protocol, a separately declared once-only whole-child cap can test the seven rows.
No scientific cap or invocation is allocated by this assessment.

If authoring or independent controls do not finish within the second allocation, retain
the exact gap and reprice; do not consume its remainder on an unreviewed scientific
call. On a source-bound ceiling of eleven, close the unchanged support question and
reconsider only changed supports under separate authority.
On refusal, retain the smallest failed binding or sign obligation without claiming the
contributed mathematics false.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
