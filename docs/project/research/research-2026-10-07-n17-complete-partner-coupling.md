---
title: Complete Partner-Pose Coupling for the n17 Parent
date: 2026-10-07
status: prospective-proof-contract
---
# Complete Partner-Pose Coupling for the n17 Parent

The first test asks whether complete partner pose covers exclude the exact single-square
witness accepted by exp288. If they do, a fixed sequence of closed position-and-angle
boxes tests whether that information excludes a region of positive width.
The accepted parent remains feasible at the known endpoint.
This contract therefore checks endpoint retention and keeps its excluded boxes disjoint
from the endpoint family.

The [W3 decision](research-2026-10-07-n17-w3-capacity-and-route-selection.md) selects
this test. The
[preceding proof interfaces](research-2026-10-07-n17-proof-interfaces-and-lp-contract.md)
record the accepted cap, parent and ownership premises.
The new implications below are the sole Astra agent’s hand derivations.
They have not received an independent mathematical review or an end-to-end machine
proof. Source controls and fresh finite reconstruction will check the declared
arithmetic; they do not upgrade that assurance automatically.
The initial contract is preserved below; the dated resource outcome and amendment are
recorded at the end.

## Accepted Inputs and Coordinates

Use the original accepted numeric-cap parent of exp276, the full input and endpoint
receipt of exp277, and the independent centered standing receipt of exp280. The final
parent has 1,056 closed rows: 64 for each of the sixteen contracting owners, and 32 for
the coarse owner of label 6. Owner 0 is label 1. Removing its 64 rows leaves **992
foreign rows** for sixteen partners.

All geometry uses the original frame with

$$
U=\frac{1169}{250},\qquad
V=\frac{935106018721}{200000000000},\qquad
o=\frac{U-V}{2}=\frac{93981279}{400000000000},\qquad B=1.
$$

The centered container is $[o,U-o]^2$. Angles use the original rational half-angle chart
$\tau\in[0,1]$, with

$$
c(\tau)=\frac{1-\tau^2}{1+\tau^2},\qquad
s(\tau)=\frac{2\tau}{1+\tau^2},\qquad
u=(c,s),\quad v=(-s,c).
$$

This is not a root-relative angular perturbation coordinate.

The fixed control is the accepted
[exp288 witness](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-288-pooled-feasible-center/certificate.json):

$$
\tau_* = \frac{53}{128},\qquad
x_* = \left(
\frac{5430403782687847}{7677200000000000},
\frac{66243855429262412554911630273}{66485768927696869600000000000}
\right).
$$

It lies in owner-0 row 26, piece 0, satisfies exact centered containment and all
retained conditional ownership predicates, and avoids every foreign owned pool.
It is one square consistent with those reduced constraints, not a seventeen-square
packing. Its square touches the left wall.
All later domains remain closed.

The input descriptor freezes five path-and-byte-identity roles: the exp282 parent
descriptor, the exp280 centered receipt, and the exp288 descriptor, certificate and
fresh receipt. The exp288 descriptor binds its accepted exp286 and exp287 inputs
recursively.
Require identical accepted canonical seed/node identities, compressed-object
identities, owner/label map, original 24-cell frame, cap, parent step order and complete
final-state headers across the joins.

Reuse `finite.extract` for bounded canonical EOF and the accepted exp277 parent premise.
Its existing owner-0-only numeric validation is insufficient for this test: the new
instrument must validate every foreign row and piece as used geometry.
Reuse exp288’s finite checker once per construction or fresh check; that small
reconstruction reads no original bulk proof.
Join exp280’s full centered `PASS_STALL`, sixteen steps and 48-point computational hull
allowance to the same objects.
Claim neither a fresh parent replay nor a new root check.
Exp284’s unaccepted child and all its geometry remain excluded.

## Complete Partner Domains

For every owner, validate the full row list, exact typed references and the closed
partition from 0 to 1. Adjacent rows share their boundary.
Missing rows, reordered or mismatched references, gaps and omitted singleton
intersections refuse the input.

For a row $[l,h]$, set

$$
r_{l,h}=\frac12\min\{c(l)+s(l),c(h)+s(h)\},\qquad
W_{l,h}=[o+r_{l,h},U-o-r_{l,h}]^2.
$$

This is a necessary centre box for every square in that row: $c+s$ is concave as a
function of angle on this quadrant, so its minimum occurs at an endpoint.
Intersect **each original residual polygon separately** with this box, retaining points
and segments. Let $P_k$ be the convex hull of all surviving vertices for row $k$. Linear
support minima over this hull equal those over the union of the pieces.
This loses correlations but retains every represented physical centre.

A row with no accepted residual pieces is already empty.
A row whose pieces all become empty after the new wall clipping may be skipped only with
that exact piece-by-piece witness.
If all rows of any partner become empty, refuse the endpoint calibration: these partner
domains are unconditioned original-parent domains, and the known endpoint guarantees
that each owner has a pose.
Do not convert this contradictory control outcome into regional success.

Before target acceptance, use the accepted full-root endpoint roster to check that each
of the seventeen endpoint centre boxes lies in an aggregate clipped row domain whose
closed interval contains one of its chart alternatives.
All four centre-box corners suffice for convex containment.
This is a new exact control on inherited endpoint enclosures, not a new root enclosure
calculation.

## Strict Partner Cores and Closed Owner Cores

For a partner row $[l,h]$, enclose the axis coefficients by

$$
c\in[c(h),c(l)],\qquad s\in[s(l),s(h)].
$$

Starting from $[-1,1]^2$, clip all sixteen inequalities

$$
\sigma(cx+sy)\le\frac12-\epsilon,\qquad
\sigma(-sx+cy)\le\frac12-\epsilon,
\qquad \epsilon=2^{-20},
$$

for $\sigma\in\{-1,1\}$ and the four corners of the coefficient rectangle.
Call the resulting polygon $D_k$. Require positive area, and independently run the
standing checker’s exact closed-arc `core_strict` test.
Thus $D_k$ lies in the interior of the zero-centred square for every angle in the entire
row. The construction is valid on all of $[0,1]$; the earlier union-cover helper, which
restricts its input to the selected guard, is not a foreign-row adapter.

For a closed owner-0 angle interval $K$, use the same sixteen inequalities with
right-hand side $1/2$, obtaining a positive-area common **closed** core $C_K$.
Independently check its vertices against both signed body axes over the whole arc.
Multiply by $1+\tau^2>0$ and check each quadratic is nonnegative at both endpoints and,
when its leading coefficient is positive, at its interior stationary point.
Equality is allowed.
At the singleton $\tau_*$ use the exact full closed unit square $S_{\tau_*}$ with
vertices $(\pm u\pm v)/2$.

Only the partner core needs strict containment.
If a point belongs to the closed owner-0 square and the interior of the partner, an open
ball around it lies in the partner.
A closed square is the closure of its interior, so that ball meets the owner-0 interior.
The physical interiors overlap even if the common point lies on the owner-0 boundary.
Both cores merely closed would be insufficient: two feasible squares may touch along
their boundaries.

## The Coupling Implication

For each facet $n\cdot z\le b$ of $D_k-C_K$, impose

$$
n\cdot x\le b+\min_{y\in P_k}n\cdot y.
$$

Then for every $y\in P_k$, the displacement $x-y$ belongs to $D_k-C_K$. There are
$d\in D_k$ and $a\in C_K$ with $x-y=d-a$, so $x+a=y+d$ is common to the owner-0 square
and the partner’s interior.
The preceding argument proves overlap for every represented partner centre and angle in
that row.

Intersect these facet inequalities across **every live row of one partner** to obtain
its guaranteed-collision region $R_j(K)$. Take the union only across different partners.
A cover by $\bigcup_j R_j(K)$ excludes the covered owner-0 centres.
Unioning row alternatives of one partner would be unsound: the actual partner could
occupy a different row.

Reuse the standalone checker’s `difference_facets`, exact support minima,
`covered_by_sweep` and `degenerate_covered`. The support shift is a **minimum**, not a
maximum or a sampled centre.
Degenerate nonempty $P_k$ domains are valid.
All facets and all input row alternatives are accounted for even when a region becomes
empty early. Empty-intersection shortcuts may skip vacuous later clipping, but must
record the reason and retain the full validated row roster.

This implication already occurs in full standing verification.
The experiment compares a complete finite reconstruction against the specific
retained-point relaxation and accepted residual over-cover; it claims neither a new
capability absent from the standing checker nor dominance over that checker.

## Frozen Discriminator and Region Ladder

First evaluate $x_*$ against the complete $R_j(\{\tau_*\})$ for all sixteen partners,
using the full closed $S_{\tau_*}$. Retain exact facet violations or containment
evidence for each partner.
Evaluate the shifted facets directly; constructing an unrelated global polygon is
unnecessary for point membership.
Validate membership of $x_*$ in an actual individually clipped owner-0 piece, not merely
the convex hull of the row’s pieces.

If none contains $x_*$, return a completed `criterion_missed` for this recipe without
running the region ladder.
This shortcut has a proof: every $C_K$ for $K$ containing $\tau_*$ is a subset of
$S_{\tau_*}$, so $R_j(K)\subseteq R_j(\{\tau_*\})$. The witness belongs to every
proposed position box and to its necessary owner-0 piece at angle $\tau_*$. No ladder
box can therefore be fully covered by these stronger-core regions.
Record the ladder as unrun under this declared obstruction, not as independently tested.

If some partner excludes the fixed witness, try only

$$
h\in\left\{\frac1{128},\frac1{512},\frac1{2048},\frac1{8192}\right\}
$$

in that order, with

$$
J_h=[\tau_*-h,\tau_*+h],\qquad
B_h=x_*+[-h,h]^2.
$$

All $J_h$ lie in $I=[13/32,27/64]$. For every original owner-0 row, retain its closed
intersection $K$ with $J_h$. The largest box includes the row-25 and row-27 singleton
seams; smaller boxes still derive their row roster by exact intersection.
Clip each original residual piece by $B_h$ and $W_K$ separately.
Use $C_K$ and the full partner domains above to check union coverage of every remaining
piece. Points and segments require exact degenerate coverage.
Construct each $R_j(K)$ starting from $B_h$: only its intersection with this declared
target box is used, so this restriction is exact.

Require the known $x_*$ to remain in a target piece at $\tau_*$ as a calibration.
This and the accepted exp288 pose supply a matched point-only witness inside each
proposed box. A successfully covered box therefore removes poses left by that specific
reduced model. Stop at the first fully covered level.

The primary success is fresh exact exclusion of one declared closed position-and-angle
box of positive width, conditional on the accepted parent.
It is not exclusion of all of $I$, the parent, an ordinary-U census entry or a global
optimality proof. If the point is excluded but every box fails coverage, retain
`fixed_witness_only` as a secondary result and `criterion_missed` for the regional
claim. Resource stops are incomplete; failed custody, malformed coverage, endpoint loss
or failed geometric calibration are refusals.

## Endpoint-Family Safeguards

The frozen owner map assigns analytic label 1 to owner 0. The accepted endpoint roster
gives label 1 chart alternatives 0 and 1. The analytic slider family moves the centres
of labels 5, 11 and 13 and does not rotate label 1; its orientation remains axis
aligned.
Every selected $J_h\subset I$ is disjoint from both endpoint chart alternatives.
Retain this family-orientation statement as an explicit inherited hand premise, check
the roles and interval disjointness exactly, and keep the full seventeen-owner
endpoint-retention control above.

This argument is specific to this frame, labelling and guard.
A future region that intersects the feasible endpoint family needs terminal capture
instead of an exclusion claim.
A failure to exclude the fixed witness supplies no feasible seventeen-square packing and
no impossibility result for a different coupling construction.

## Resource and Verification Contract

Use one worker. Freeze 120 seconds for construction and 120 for fresh finite
reconstruction, with a 240-second combined ceiling and owned-group cleanup.
The sampled RSS guard is 4 GiB **per live process**, not aggregate memory or an
allocation-time limit.
The fresh process reconstructs all used finite geometry and compares the scientific
payload. It imports no producer or kernel and inherits the same accepted parent and root
premises.

| Resource | Initial exp289 ceiling |
| --- | --- |
| Each JSON input; seed | 10 MiB each |
| Native node | 512 MiB compressed; 2 GiB decoded; complete canonical EOF |
| Final-state slice; output | 64 MiB each |
| Normalized used geometric rationals | 4,096 bits for input, intermediates and output |
| Endpoint-control rationals | 16,384-bit inputs; 32,768-bit intermediates; retain source references and control witnesses rather than copied large scalars |
| Residual pieces per row | 64 |
| Input polygon; clipped polygon | 256; 384 vertices |
| Construction geometry vertices, including repeated owner-0 passes | 262,144 |
| Aggregate partner domain; core | 1,024; 32 vertices |
| Facets per row/context; total checked facet instances | 64; 500,000 |
| Partner collision polygon | 256 vertices |
| Owner-0 target pieces per context | 1,024 |
| Support vertex products | 16,000,000, with cache accounting explicit |
| Coverage sweep per piece | 4,096 edges; 8,400,000 prospective edge pairs |

Check canonical rational grammar and character ceilings before constructing fractions.
The larger endpoint budget is prospective and separate from the unchanged geometric
budget; exp281 already established that a legitimate unused endpoint scalar can exceed
4,096 bits. Count actual generated work and retain every resource stop.
Internal homogeneous arithmetic and sweep event counts are not covered by the
normalized-rational or prospective-edge bounds.
Keep checks before and after trusted sweep calls and the external wall guard.

Target-free controls must distinguish minimum from maximum support, row intersection
from row union, strict from nonstrict partner cores, closed owner boundary contact,
missing seams, degenerate domains and coverage, and a complete fixed-point obstruction
from a resource stop.
Include endpoint retention and family disjointness, point-only versus regional success,
giant endpoint scalars within their declared budget, geometry exceeding its own budget,
canonical EOF, changed-byte refusal and fresh producer-free reconstruction.
Registration and source review precede all actual coupling signs, regions and target
predicates.

## October 7 Resource Outcome and Amendment

Exp289 stopped before the coupling predicate with `status=incomplete` and
`coupling per-row residual piece ceiling`. Construction took 3.175524 seconds; fresh
verification was unstarted.
No fixed-point or regional result was computed, and every exclusion, capture and census
flag remained false.
The original
[certificate](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-289-complete-partner-coupling/certificate.json)
and
[phase record](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-289-complete-partner-coupling/phase-execution.json)
retain this operational outcome.
It is not a mathematical miss.

The subsequent input-only structural audit completed in 6.252654 seconds.
Its retained report is
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-289-complete-partner-coupling/structural-intake.json`.
It counted all 1,056 rows, including the 992 foreign rows: 91,825 residual pieces,
348,140 raw vertices, no empty pieces, at most 570 pieces in one row, eight vertices in
one piece and 135 bits in a coordinate.
It evaluated no new coupling predicate.
The accepted exp288 pose reconstruction in its intake was explicitly an
inherited-premise check.

The coordinator selected **1,024 pieces per row** and **1,048,576 cumulative
construction vertices** for exp291, a separately registered resource-amended replication
of H298. All domains, arithmetic thresholds, proof criteria and other resource ceilings
remain unchanged, including the 120-second construction and 120-second fresh-check
allocations. SAT inherits these representation limits only under its own later
registration.

The structural counts also cover the repeated work in the frozen recipe.
Owner-0 rows 25, 26 and 27 respectively have 22, 13 and 37 vertices, and 7, 4 and 11
pieces. The worst case across fixed-point calibration and all four ladder levels parses

$$
348140+5\cdot13+22+37=348264
$$

construction vertices.
The full-square SAT construction needs $348140+13=348153$. The largest regional interval
visits 22 pieces, including its closed singleton seams, below the unchanged 1,024-piece
target ceiling. These are structural sums, not geometric signs or runtime forecasts.
The inherited custody extractor has separate work and is not included in the
construction counter.
Aggregate hull size, collision-region size and arithmetic work remain guarded at
runtime; the input audit does not prove those caps fit.

## Exp291: Complete Fixed-Point Miss

The resource-amended run completed with `criterion_missed`, and a fresh process
reconstructed the same exact result.
The
[retained summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-291-complete-partner-coupling-amended/summary.json)
records all 1,056 original rows, 992 foreign rows and 348,153 parsed construction
vertices. All seventeen endpoint controls and the family-angle disjointness control
passed.
Each of the sixteen partners has an exact failed fixed-point facet; none excludes
the accepted exp288 pose through this common-core construction.

The four regional ladder levels were unstarted, as the fixed-point containment argument
already prevents their acceptance under this recipe.
This is one completed fixed-point miss with a proved reason to skip the ladder, not four
measured regional misses.
Construction took 51.699171 seconds and fresh reconstruction 54.946135 seconds; the
supervisor recorded 106.929355 seconds overall and successful cleanup.
The work counters report 1,152 generated facets, 11,904 checked facet instances and
48,516 minimum-support vertex products.

This result leaves the physical packing question unresolved.
It establishes failure of the declared common-core implication on these complete product
domains, not feasibility of the parent or impossibility of a stronger coupling.
The next selected discriminator is the separately registered full-square SAT test on the
same domains. A positive result there would identify the common-core approximation as a
sufficient cause of the discrepancy; a second complete miss would instead justify
testing centre-angle correlation or guard-conditioned multi-owner constraints.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
