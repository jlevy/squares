---
title: H-124 — full distinguished-square compatibility
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-124
  kind: hypothesis
  claim: >-
    At q=1939/500, every contained closed unit square Q in the actual near45
    angle band, with center in [1,q/2] times [0,1] and avoiding all ten original
    Stromquist P10 marks, intersects every contained closed unit square S in
    either actual near-axis or near45 band that avoids the nine unchanged B–J marks.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: complete full-square compatibility in both actual closed angle bands
    direction: >-
      Accept only a complete independently checked implication over every
      admissible Q and S, including all seams. Reject only one independently
      checked closed-disjoint pair meeting every stated condition. Finite
      no-witness output, failed sufficient guards, errors and timeouts are unresolved.
    threshold: every admissible pair intersects
  instrument: >-
    Source-free-controlled exact event-cell discriminator for one fixed S and
    one Q frame, with an independently implemented corner/SAT witness reader.
    Independently source-bound closed-polygon cover certificates are also available;
    exp125 certifies the whole diagonal S band, while its axis sufficient cover is unresolved.
  instrument_ready: true
  regime: Fixed q, unchanged P10 and B–J coordinates, canonical Q center and both full closed angle bands; closed tangency counts as intersection.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: Two twenty-minute source-free authors in parallel, independent reviews, then a separately capped prospective discriminator if ready.
  prereqs: [independent instrument controls and review, committed prospective target protocol, actual-angle and all-mark witness validation]
  replication: false
  registered: '2026-09-07'
---
# H-124 — Keep the Full Distinguished Square

This is the changed BC255 obligation selected under `think-7e72` after H110 and H123
were accepted and H122 was refuted.
The sole
[exp124](../series/series-000-smoke-and-calibration/experiments/exp-124-full-square-compatibility-screen.md)
fixed-S, exact45-Q screen returned no witness in 0.84 seconds.
Its witness-only reader was not invoked.
H124 remains unresolved; neither continuous compatibility nor the finite search’s
coverage has an independent certificate from that run.
The producer and independent reader passed 27 source-free controls and independent
reviews by 08:09:33 UTC, before the prospective protocol and sole scientific invocation.
No retry or second frame is allocated.

The separately registered complete-cover experiment
[exp125](../series/series-000-smoke-and-calibration/experiments/exp-125-h124-complete-residual-cover.md)
subsequently certified the sufficient cover for every S in the whole near45 band: the
independent source reader checked13 polygons,12 closed slabs and72 endpoint-pair
conditions. Its axis-band producer returned `no_chain` and did not authorize a reader.
Thus the remaining compatibility obligation is the near-axis S band; H124 as a whole and
restricted H036 are still unresolved.
This partial lemma does not change the unrestricted packing bound.

Write q=1939/500. The actual angle bands, modulo square quarter turns, are
[-pi/720,pi/720] and [pi/4-pi/720,pi/4+pi/720]. Both closed unit squares must lie in
[0,q]^2. Q uses the second band and the canonical center region [1,q/2] x [0,1].
Avoiding a mark means the mark is outside the closed square, not on its boundary.
Q avoids all ten P10 marks; S avoids all nine unchanged B–J marks.

The coordinates are the original `point_sets(q)` definitions in
[restricted_orientation.py](../../cases/stromquist/restricted_orientation.py), not the
different fixed-side `source_points(field)` calibration.
The B–J formulas also appear in
[H122](H-122-diamond-conditional-nine-point-cover.md#fixed-domain-and-data).

## What a Complete Proof Would Buy

The reviewed
[counting reduction](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md#the-counting-reduction)
scales any hypothetical strict-sublevel eleven-square packing to side q and takes
pairwise-disjoint closed unit cores.
One core avoids P10. H106 makes it near45; H123 and a global coordinate-midline
reflection put it in the canonical region.
Call that core Q. Each other core must then contain one of the nine B–J marks if H124
holds, contradicting ten disjoint cores and nine marks.

No forced-anchor or fixed-diamond lemma is required for this full-square implication.
Those lemmas remain valid optional pruning facts.
Replacing Q by a common obstacle forgets correlations between its shape and position;
H122’s negative result does not settle H124.

A verified disjoint Q/S pair would refute this sufficient compatibility statement only.
It is not an eleven-square packing and does not refute H036 or change the global bound.

## First Proposed Discriminator

Keep the exact S from the retained exp122 packet unchanged and use the single exact45
frame for Q. Enumerate Q’s exact event strata against all ten marks, intersect their
closures with the canonical region, and reconstruct a strict-stratum witness after
clipping.
For each signed edge-normal axis of either square, the separating gap is affine
in Q’s center. A positive closure-vertex gap can be retained while moving into the
required strict stratum.
Degenerate clipped strata and open boundaries need explicit source-free controls.

The independent reader reconstructs unit-square geometry and all mark-edge tests from
exact ordered corners, verifies actual angles and containment, binds unchanged S to the
retained source, and requires a strict separating-axis gap.
There are 76 point-edge determinants for the ten plus nine marks.
Across eight corners there are 16 coordinate containment checks, or 32 lower/upper
scalar wall inequalities.
Tangency is not a witness.

This finite slice can refute the hypothesis but cannot accept it.
Even exhaustive no-witness output for this S and frame leaves all other S and continuous
Q angles open. There is no automatic second frame, changed S, larger cap or
completed-target retry.
The exact invocation and budgets belong in a separate prospective experiment.

## A Stronger Continuous Common Obstacle

The analytical assessment used the full ten-mark avoidance condition to enlarge the old
diamond. Independent mathematical review accepted this derivation in Session093 at
08:50:29 UTC; it does not establish the remaining nine-mark cover or resolve H124. No
additional scientific evaluation produced it.

Put $m=q/2$, $W=m-1=939/1000$, $r=\sqrt2/2$, and $k=1+W/2$. Write $C=\cos\theta$,
$S=\sin\theta$ and $h=(C+S)/2$. Containment of Q implies its center $(x,y)$ has
$y\ge h$. In the canonical region, $a=x-1$ and $z=1-y$ therefore satisfy $0\le a\le W<1$
and $0\le z\le1-h<1/2$.

Two original P10 marks are $L=(1,1)$ and $M=(m,1)$. Their coordinates relative to Q’s
center in its orthonormal frame are

$$
L:\ (-Ca+Sz,\ Sa+Cz),\qquad
M:\ (C(W-a)+Sz,\ -S(W-a)+Cz).
$$

Joint avoidance of these two marks by the closed square Q forces

$$
Sa+Cz>1/2,\qquad C(W-a)+Sz>1/2.
$$

Indeed, the alternative escape $Ca-Sz>1/2$ for L implies $a>1/2$. M’s first coordinate
is then less than $CW-1/2<1/2$, while its second lies strictly between $-1/2$ and $1/2$,
forcing M inside Q. The symmetric alternative escape for M forces L inside Q. The other
escape directions are impossible since $Cz,Sz<1/2$. Strict inequalities matter: a mark
on Q’s boundary is contained, so avoidance is strict.

Use frame coordinates $U=Cx+Sy$ and $V=-Sx+Cy$ for the center.
The preceding inequalities and bottom containment place it inside the closed triangle

$$
K_\theta=\{U\le u_*,\ V\le v_*,\ SU+CV\ge h\},\qquad
u_*=Cm+S-1/2,\quad v_*=C-S-1/2.
$$

This is an outer approximation to the possible centers; enlarging the center set is safe
when taking a common intersection.
For a nonempty triangle let $\Delta=1-2h+CSW\ge0$. Its coordinate ranges have widths
$\Delta/S$ and $\Delta/C$. The intersection of all unit squares with centers in this
triangle is consequently a frame-aligned rectangle with half-sides

$$
\frac{1-\Delta/S}{2},\qquad\frac{1-\Delta/C}{2},
$$

and center, in the original coordinates,

$$
p_\theta=\left(k+\frac{(C-S)(2h-1)^2}{4CS},\ h\right).
$$

Put $d=|\theta-\pi/4|$. The full angle band satisfies $d<1/180$ because $\pi<4$. Using
$707/1000<r<708/1000$, $\sin d\le d$ and $\cos d\ge1-d^2/2$ gives

$$
703/1000<C,S<89/125,\qquad h>353/500.
$$

Since $CS\le1/2$, we have $\Delta\le23/400$. Each rectangle half-side is at least
$1291/2812>459/1000$. Also $|C-S|<1/125$, $(2h-1)^2<9/49$ and $4CS>49/25$ bound the
horizontal displacement of $p_\theta$ from $(k,r)$ by $1/1000$. The vertical
displacement is less than $1/90000$, so $\|p_\theta-(k,r)\|_1<1/800$.

It follows that the fixed diamond

$$
K_1=\{(X,Y):|X-k|+|Y-r|\le16/25\}
$$

lies in the interior of every admissible Q: either frame projection relative to
$p_\theta$ is at most

$$
\frac{89}{125}\left(\frac{16}{25}+\frac1{800}\right)
=\frac{45657}{100000}<\frac{459}{1000}.
$$

The old
[anchor diamond D](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md#a-larger-fixed-obstacle-from-two-anchors)
is also contained in Q. Thus $E=\operatorname{conv}(D\cup K_1)$, the convex hull of the
two diamonds, is a larger common obstacle.
This is a sufficient obstacle, not a maximal-intersection claim.
Its internal margin is not a uniform clearance between hypothetical packed cores.

### A Continuous Cover Contract, Not Two Angle Samples

Let T be the accepted outer tangent-half-angle endpoint $110880/50803079$ and set

$$
\alpha=\frac{1+T^2}{2(1+2T-T^2)},\qquad
B_\phi=R_\phi[-\alpha,\alpha]^2,\quad\phi\in\{0,\pi/4\}.
$$

Here $R_\phi$ rotates a point by $\phi$. For S’s orientation $\psi$, put
$\delta=|\psi-\phi|$. Each shrunken square $B_\phi$ lies in the centered unit-square
kernel for every actual orientation in that band: $t=\tan(\delta/2)\le T$, and
$(1+2t-t^2)/(1+t^2)=\cos\delta+\sin\delta$ is increasing over this short interval.
The largest required projection is therefore bounded by
$\alpha(\cos\delta+\sin\delta)\le1/2$. A complete cover of all possible S centers by

$$
(E+B_\phi)\ \cup\ \bigcup_{p\in\{B,\ldots,J\}}(p+B_\phi)
$$

would prove H124 for that whole band.
The plus sign between sets denotes their Minkowski sum: all sums of one point from each
set. Because $B_\phi$ is centrally symmetric, a center in $E+B_\phi$ gives an
intersection with E; a center in $p+B_\phi$ gives containment of p.

However, one enlarged center box can forget the correlation between wall containment and
angle. Uniform shrinking may then fail at wall-tight seams even when the actual cover
holds.
Marked corners admit an analytical patch: for $b_\theta=|\cos\theta|+|\sin\theta|$
and $h_\theta=b_\theta/2$, a mark one unit from both adjacent walls belongs to any
contained square whose center distances from those walls are both in $[h_\theta,1]$,
because

$$
b_\theta(1-h_\theta)=1/2-(b_\theta-1)^2/2\le1/2.
$$

Any residual-cover instrument must incorporate these actual-angle regions safely,
reconstruct every remaining event stratum and check all closed boundaries.
More precisely, put

$$
Z_0=[1/2,q-1/2]^2,\qquad
Z_{\pi/4}=[h_{\min},q-h_{\min}]^2,\qquad
h_{\min}=r\frac{1-T^2}{1+T^2}.
$$

For each of the three marked corners B, D and F, let $R_j$ be the portion of $Z_\phi$
within distance one of both adjacent walls.
Actual containment supplies the lower distances $h_\psi$ needed by the corner lemma.
The unmarked bottom-left corner has no such patch.
The exact sufficient obligation, for both central frames, is the closed union cover

$$
Z_\phi\subseteq(E+B_\phi)\ \cup\
\bigcup_{p\in P_9}(p+B_\phi)\ \cup R_B\cup R_D\cup R_F.
$$

Writing a closed union preserves seams rather than discarding them informally.
Failure of this sufficient representation would leave H124 unresolved.
Exp125 subsequently tested exactly this sufficient representation, with the scoped
outcomes recorded above.
No retry or continuous arrangement build is allocated here.

### Endpoint-chain Certificates

The independently assessed cover instrument partitions the rectangle’s full x-range into
contiguous closed slabs.
For each slab $[a,b]$, it supplies one ordered chain of convex polygons.
The reader checks that the first polygon contains both bottom slab corners, the last
contains both top corners, and each consecutive pair has overlapping closed vertical
sections at both $x=a$ and $x=b$.

Each consecutive pair’s intersection is convex.
Its two endpoint intersection points therefore yield an intersection at every
intermediate x. The resulting interval chain connects the rectangle’s bottom and top
throughout the slab, proving its full closed coverage.
Different chains at the two endpoints would not suffice.
The reader also binds the complete source and verifies convexity and the entire
contiguous slab partition; it need not trust or reconstruct discovery events.

A complete discovery method includes rectangle walls, polygon supporting lines, vertical
lines and every nonparallel supporting-line intersection whose x-coordinate lies in the
rectangle’s x-range.
Intersections outside its y-range are retained to keep the completeness argument simple.
Between consecutive x-events, section endpoint orders are fixed.
A covering interval chain found in one interior fiber persists through the open slab,
and closedness extends it to both endpoints.
Thus the representation is complete for finite closed convex-polygon covers absent
resource limits. Adjacent slabs with the same chain can be merged.

The bounded source-free producer and reader were authored independently under
`think-g29r` and `think-qt0k`; independent reviews passed by 09:21:09 UTC. Their 21 and
69 synthetic controls pass, including independently replayed closed-contact and
unresolved examples.
In [Session094](../agent-sessions/session-094-complete-cover-and-density-controls.md),
the source-constructor author `think-jxs9` froze at 10:02:36 UTC with 33 unrelated toy
controls passing.
The independently authored source reader `think-smve` froze at 10:06:51
UTC with 22 unrelated controls passing, before its original 10:14 UTC deadline.
The [capped caller](../../devtools/run_h124_cover.py) passed 13 source-free controls and
independent mechanical review under `think-m820`. Independent mathematical source
reviews passed at 10:10:26 and 10:14:46 UTC. The reviewed source has at most 60 polygon
vertices and at most 2,082 conservative x-events; these are static bounds, not runtime
measurements or an actual cover.
Exp125 supplied the committed prospective protocol and actual source evaluation after
those readiness checks.
Only its diagonal cover passed independent source reconstruction; the axis producer
returned `no_chain` and did not authorize a reader.
Timeout, omitted evidence or failure to construct a chain is unresolved; even a verified
gap in this sufficient cover would not refute H124.

### A Fixed Collision-region Strengthening

The next selected instrument keeps those thirteen regions and appends one fixed
S-center region, $C^*$, directly. It is not another obstacle to dilate by $B_0$.
The [author proof](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-center-correlated-collision.md)
and [independent derivation](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-center-correlated-review.md)
prove the uniform displacement guard $\varepsilon=1/500$ and the collision implication
throughout both actual closed angle bands. They define every constant and distinguish
world coordinates from the rotated Q-frame.

The producer constructs $C^*$ by closed half-plane clipping; the independently authored
reader reconstructs it by enumerating supporting-line intersections. Both source-free
reviews passed in Session094, with the fixed eight unnormalized normals and the
required $2\varepsilon$ penalty on diagonal normals. The reviewed source retains the
old thirteen regions unchanged and has at most fourteen regions and 68 vertices.
Empty or degenerate new regions are refused, not silently discarded.

This is instrument readiness only. Neither new scientific constructor has been invoked,
and actual source agreement, nondegeneracy and complete near-axis coverage remain
untested. A separate prospective experiment and its admission checks are required.
No radius sweep, two-angle solver or retry of exp125 is authorized by this construction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
