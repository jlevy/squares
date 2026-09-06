# BC-254: The Next Exact Discriminator After exp-113

Recommendation: fund one bounded **overweight-pair separator for the retained
candidate**, with a separate strict-interior witness checker.
Do not couple that first test to another LP or a complete arrangement build.
A checked witness would refute the specific $56/5$ candidate; a completed screen without
one would remain inconclusive about its almost-everywhere feasibility and about H-099.

This is a design-only W6 research-loop commission under an Insight focus, `think-eilk`,
in Session 089 phase 8. The commissioned window is
`2026-09-06T21:01:13Z`–`2026-09-06T21:21:13Z`. No target geometry, new row,
optimization, or timing experiment was run for this assessment.
The coordinator owns funding, instrument readiness, any new experiment identity, and the
prospective freeze.

## Why This Test Comes First

[exp-113’s checked packet](../exp-113-h-099-trump-support-screen/packet.json) has orbit
sizes $(4,8,8,8,8,8,8,8)$ and per-member weights

$$
a=(1,0,2/5,1/10,0,1/10,3/10,0).
$$

Thus four placements have weight one, 32 others have positive weight at most $2/5$, and
24 have weight zero.
Two placements outside the weight-one orbit have combined weight at most $4/5$. Only

$$
\binom42+4\cdot32=134
$$

unordered pairs can have combined weight strictly above one.
These counts follow from the retained weights and orbit sizes; they are not new
geometric measurements.
No claim is made here that any eligible pair actually overlaps.

If distinct placements $P_i,P_j$ have intersecting interiors and $w_i+w_j>1$, their
common interior is open and nonempty, hence has positive area.
On that set the full candidate depth is at least $w_i+w_j>1$, because all other weights
are nonnegative. One such pair therefore suffices.
It avoids the completeness problem that makes a full feasibility certificate more
expensive.

## Concrete Algorithm and Witness

Freeze the exact parent packet by Git revision and repository-relative path, its eight
weights, `trump11-v1`, and source/orbit ordering.
Reconstruct the same 60 distinct placements with the reviewed source binding.
Do not round coordinates or count a labelled preimage as another placement.

1. Enumerate unordered distinct-placement pairs in exact key order and retain only those
   with rational weight sum strictly greater than one.
   Refuse unexpected source, orbit, weight, or pair-count metadata.
2. Call [`sqpack.verify.separated`](../../../../../src/sqpack/verify.py) with
   `exact_sign`, without floating buckets.
   Test the result with `is None`: `None` means intersecting interiors, while `0` is
   exact contact and must not count as a violation.
   Stop at the first strict overlap.
3. Construct an exact common-interior point.
   Collect the corners of either square lying in the other closed square and all
   intersections of their edge segments, deduplicate by exact coordinates, and average
   the collected points.
   Use exact segment parameters and handle parallel edges explicitly.
   This includes every vertex of the convex intersection.
   For a full-dimensional intersection its vertex average is strict in every defining
   half-plane; check all eight strict forms directly and refuse if the construction
   fails that check.
4. Obtain positive rational lower bounds on those forms and the container margins by the
   existing exact sign/enclosure procedure.
   If their minimum is $\gamma>0$, retain $\varepsilon=\gamma/4$. Unit normals bound
   each affine change under an $L^\infty$ displacement of $\varepsilon$ by
   $2\varepsilon$, so the whole positive-area box remains inside both squares and the
   container.
5. Retain the two exact placement keys, parent-candidate binding, point, rational
   radius, and excess $w_i+w_j-1>0$. A separate checker reconstructs the source and
   weights, requires distinct keys, and checks strict orientation-corrected edge
   determinants for both squares and the container margins.
   It needs no SAT search, intersection enumeration, or optimizer.

The point may lie on a third square’s supporting line.
That does not invalidate this pair witness: its depth lower bound uses only the two
selected positive weights and does not require the other incidences to stay constant.
It does mean that the point must not automatically be appended as an exp-113-style
necessary row. Producing such a row would require the full support’s off-line and
positive-neighborhood guards under a separately frozen next procedure.

The existing
[support geometry](../../../../../src/sqpack/full_size_density/support_ceiling.py) and
[packet checker](../../../../../devtools/check_full_size_density_support_ceiling.py)
already supply field arithmetic, source binding, canonical rational validation, and the
determinant margin pattern.
Reuse those contracts.
The generic clipping routine in the
[Stromquist control](../../../../../cases/stromquist/restricted_orientation.py) is
another construction option, but importing a case-specific module into the library or
changing the frozen Stromquist control is unnecessary for this two-square test.

Keep the reusable operation in `sqpack.full_size_density`, with explicit
candidate-search and witness-replay command modes and focused tests.
No new scheduler, registry, arrangement framework, checksum manifest, or dependency is
needed. Preserve exp-113’s packet format and accepted result.
Reuse its canonical-number guard rather than introducing a permissive `Fraction(text)`
parser for the new witness.

## Controls and Independent-Check Limits

The build must retain these controls before its target command is frozen:

| Control | Required result |
| --- | --- |
| Two distinct overlapping axis-aligned unit squares with weights $1$ and $1/2$ | Return a strict-interior witness; separate determinant replay proves depth at least $3/2$ on its box |
| The same weights with an exact shared edge, shared corner, or positive gap | No pair obstruction; `0` from SAT is not interpreted as overlap |
| Positive-area overlap with weights $1/2,1/2$ | No violation from a weight sum equal to one |
| Three distinct nearby unit squares, each of weight $2/5$, with a common interior | Pair screen reports no pair obstruction, never full feasibility; triple depth can exceed one |
| Reversed corner traversal, a quarter turn, duplicate raw preimages, or repeated placement key | Representation changes preserve the answer; duplicate geometric keys cannot be counted twice |
| Degree-eight non-target square centers using the existing field $K$, inside a side-two container | Exact witness construction and replay succeed without float conversion or constructing a target candidate |
| Boundary point, nonpositive or excessive radius, wrong source/key/weight, float, Boolean, or exponent-form rational | Refuse at the source, type, strict-margin, or weight guard |
| Original exact Trump packing with unit weights, and the retained D4 uniform average | No overweight-pair obstruction; both are known feasible source controls, not evidence about the new candidate |

The negative witness checker is independent of pair selection and witness construction,
but shares exact field arithmetic and the retained source constructor.
It proves the specific candidate invalid, not H-099 false.
A no-hit receipt proves at most completion of the eligible-pair sweep.
It must not contain a general `feasible` verdict or a claimed maximum depth.
The triple control makes that limitation executable.

## Alternatives and Their Completeness Obligations

A complete checker for this fixed candidate can discard zero-weight boundaries when
partitioning depth, while retaining their source identities.
Its 36 positive placements have at most 144 supporting lines, or 148 including the
walls. No target line deduplication or face count was computed here.

One concrete complete algorithm is to clip every distinct supporting line to the
container, split it at all pairwise intersections, and probe both sides of every
nondegenerate open segment with a certified small exact displacement.
Include the container walls and ignore outward probes.
Distinct parallel lines, coincident lines, multiple intersections, zero-length contacts,
and all exact equalities require explicit handling.
Every positive-area arrangement face has an open boundary segment, so this visits every
face; the omitted line union is Lebesgue null.
A checker must establish that completeness, not merely replay the supplied sample list.

For $M$ lines this construction has $O(M^2)$ intersections and edge probes, although
naively checking all other lines and square incidences at every probe costs $O(M^3)$
exact work. An independent exhaustive replay can share field arithmetic but must not
trust an author-curated face list.
Its target runtime is unmeasured.

The existing rational
[`fractional.ceiling.maximum_depth`](../../../../../src/sqpack/fractional/ceiling.py)
checks closed-set depth at arrangement vertices.
Its upper-semicontinuity argument is correct for that stronger pointwise problem.
It cannot be relabelled as an a.e. checker: touching squares can have excessive vertex
depth and valid a.e. depth, and an open-face excess must be witnessed away from the
boundary. Its rational placement model also does not directly accept the algebraic Trump
geometry.

A cutting route needs that complete separation oracle first.
With all 60 support members available as weights change, at most 240 supporting lines
give at most $1+240\cdot241/2=28{,}921$ plane faces before restriction to the container.
This is a generic combinatorial bound, not a measured target count.
Each truly violated cut is new because the current exact LP point satisfies the existing
rows. Finite exhaustion can therefore be proved, but a useful wall-time bound cannot be
inferred from it. An exact solver also needs its own termination argument or an explicit
pivot refusal; the present 64-pivot guard does not promise every enlarged LP will finish
optimally. Neither the pair screen nor a few new cuts supplies a complete feasibility
oracle.

## Proposed Cost and Stop Conditions

The recommendation is one author slice capped at 30 active minutes for the reusable pair
test, source/toy controls, refusal behavior and receipt, followed by a separately
allocated ten-minute independent review.
These are prospective effort estimates, not funding or measured implementation costs.
If that slice cannot establish its guards, retain the missing condition and stop before
target access.

After successful controls and coordinator freeze, propose one candidate process capped
at 30 seconds and one separate witness replay capped at 30 seconds.
These are proposed limits, not runtime predictions.
The available cost anchors are exp-113’s 19.69-second producer and 9.10-second file
replay, and the earlier 0.573108-second source-only worker; none measured these 134 pair
checks or the new witness reader.
Price the new controls before accepting those target caps.
Do not repeat the already accepted parent LP or its full replay merely to obtain another
timing number.

The complete open-face route would need at least two bounded author slices for
enumeration, completeness controls and replay, plus separate mathematical review; that
effort estimate and its target runtime remain unvalidated.
A cutting route adds LP/oracle integration and repeated-solve accounting on top.
Neither is the cheapest next funded build while the overweight-pair discriminator is
untried.

Stop at the first independently checkable pair witness, after all 134 eligible pairs
without a witness, or at a declared guard/time failure.
Preserve those outcomes separately.
A pair witness retires only this candidate; no hit selects the complete
positive-area-face obligation for later pricing.
Do not silently continue to triples, finer points, another weighting, a larger support,
or another solve. All new target work requires a new prospective commission; exp-113
remains unchanged.

## Next Step: Complete Face Verification, 2026-09-06

This dated section supersedes the earlier pair-build recommendation for future
allocation; it does not rewrite that prospective design.
The coordinator reports that exp-115 completed all 134 eligible pairs with separately
checked separating axes and no witness.
H-105 is rejected only at its exact pair-obstruction scope.
H-099 and the unchanged exp-113 candidate’s a.e. feasibility remain unresolved.

This is source-only assessment `think-pg9k`, opened at `2026-09-06T22:09:48Z`; the
coordinator shortened its finalization boundary to `2026-09-06T22:19:32Z`. No new target
construction, binding, line or face enumeration, row, LP, test, or timing run occurred.
The recommendation is a complete face verifier, with independently reconstructed
coverage, not a higher-order overlap filter.

### Domain and Boundary Semantics

Freeze the same exact side, 60 distinct placements, source/orbit ordering, and eight
weights as exp-113. Keep all geometry and arithmetic in its certified real number field.
Validate containment, unit geometry, nonnegative rational weights, and source identity
before calculating depth.

For this fixed candidate only, omit zero-weight squares from the arrangement but retain
them in source metadata.
Its 36 positive placements contribute at most 144 supporting lines; adding the four
container walls gives at most 148 before exact deduplication.
These are combinatorial bounds from retained weights, not measured target line counts.

The finite union of these lines has Lebesgue area zero.
On each component of its complement inside the open container, every positive square’s
membership is constant, so weighted depth is constant.
Closed-square and interior-square indicators agree off their boundaries.
The required maximum is over these positive-area faces, not over closed arrangement
vertices. Excess confined to an edge or vertex is not an a.e. violation.
No global configuration-space capture is involved.

### Producer: Probe Every Open Boundary Segment

Use the following complete finite procedure, without floating screens:

1. Form every positive square’s infinite supporting lines and the four walls.
   For exact identity, divide each nonzero line triple by its first nonzero normal
   coefficient. Retain its incident square/edge labels; coincident lines are one
   geometric line, not extra weighted placements.
2. Clip each line to the closed container using exact line/wall intersections.
   Retain point contacts as a classified boundary case, but generate probes only from
   positive-length clipped segments.
   Split those segments at every intersection with a distinct nonparallel supporting
   line inside the segment.
   Include both container endpoints, deduplicate concurrent intersections exactly, and
   sort along an injective coordinate using algebraic order, not coefficient-tuple
   order.
3. For each pair of successive distinct cut points, take its midpoint $m$. It is on
   exactly its own geometric line: an equality with another line is a failed
   completeness guard. Choose a nonzero normal $n$ to its own line.
   For every other affine line form $g(x,y)=ax+by-c$, put $D_g(n)=an_x+bn_y$. Choose a
   positive rational displacement $\delta$ satisfying $|\delta D_g(n)|<|g(m)|/2$
   whenever $D_g(n)\ne0$. Exact sign and rational enclosure provide such a value; forms
   constant along the displacement need no bound.
4. Check $m+\delta n$ and $m-\delta n$. Keep each strictly interior container point; a
   wall segment has only one inward probe.
   Verify that retained probes lie on no positive supporting line.
   At each, compute depth by exact oriented edge tests and rational weight summation.
   Retain a positive rational neighborhood margin when depth exceeds one; otherwise
   continue through every segment and side.

Completeness follows from the bounded line arrangement: every positive-area face has a
nondegenerate open boundary segment in its closure.
Splitting at all intersections visits such a segment, and the bounded normal
displacement reaches its adjacent face without crossing any other line.
Thus every face is represented.
Repeated probes of the same face are harmless and need no face-identity machinery.
Container corners, coincident edges, parallel lines, and concurrent crossings do not
justify skipping their adjacent positive-area regions.

### Independent Replay: A Different Complete Enumeration

A positive packet must not be accepted by checking only its supplied probes or counts.
Recommend an independently written vertical-slab sweep for the reader, reconstructing
the source through the existing direct D4 maps and rebuilding its own supporting lines.
It must not call the producer’s clipping, cut-list, or probe generator.

Collect $0$, the container side, all vertical-line coordinates, and the x-coordinates of
every nonparallel supporting-line intersection within the horizontal container range.
Including intersections whose y-coordinate is outside the container merely
overpartitions; it avoids an unnecessary event-filtering premise.
Include the horizontal walls in that construction.
Sort and deduplicate exactly.

For each open interval between successive x-events, choose its midpoint.
Intersect each positive square’s interior with that vertical line, obtaining an empty
set or one open y-interval.
Clip to the container, sort all interval endpoints, and sweep their rational weights,
grouping equal endpoints before evaluating each nonempty open y-band.
Endpoints themselves are not scored.
Independent determinant checks at band interior points supply negative witnesses when
needed.

All active endpoint formulas and their ordering are fixed between x-events: changes
require a vertical supporting line or an intersection already in the event set.
Consequently every positive-area face appears in at least one inspected slab/band.
An exceptional x-line has area zero and cannot be the sole location of an a.e.
violation. This supplies a second completeness argument, not just a second call to the
producer’s enumeration.

Both routes still share the exact field kernel and retained original source.
Original packing validation also uses its accepted geometric validator.
These shared foundations must remain explicit.
Complete independent regeneration can validate a compact result receipt; counts alone
are not a standalone portable proof.
If only a negative witness is returned, its exact positive-area box can be checked
directly without finishing either exhaustive route.

### Reuse and Control Matrix

Reuse the reviewed source binding, exact square validation, canonical rational parser,
bounded file reader, and process/refusal interfaces from the support and pair tools.
Reuse `NumberField.sign` and `enclose` for exact signs and rational margins.
The
[Stromquist clipping implementation](../../../../../cases/stromquist/restricted_orientation.py)
is a reference for equality handling, not a reason to import a case module into the
reusable library or alter its frozen source control.

Two existing routines are not drop-in complete a.e. checkers:

- `fractional.ceiling.maximum_depth` solves a closed-pointwise problem in a rational
  placement model. Its vertex maximum must not be relabelled as an a.e. maximum.
- `full_size_density.support_ceiling.necessary_row` checks all support boundaries,
  including zero-weight ones.
  Positive-only face probes can legitimately hit those omitted lines.
  Keep that accepted row guard unchanged; use a separate fixed-weight depth helper.
  A returned face point is not automatically a full-support LP row.

| Control | Required behavior |
| --- | --- |
| One square and a disjoint unit-weight packing | Exact a.e. maximum one, including boundary-touching placements |
| Edge/corner contacts whose closed depth exceeds one | Accept a.e. feasibility; do not score the contact itself |
| Overlapping pairs, equality at depth one, and the existing common-interior $2/5$ triple | Distinguish strict excess, equality, and a genuine violation invisible to pair filtering |
| Coincident supporting lines, parallel families, concurrent crossings, wall-coincident edges, and repeated event coordinates | Preserve every adjacent open region without zero-division or duplicated geometric weights |
| A rational sliver and non-target degree-eight rotated squares | Preserve narrow positive-area regions with exact order and signs |
| A zero-weight boundary passing through a probe | Same candidate depth and verdict after adding or removing that zero-weight placement |
| Original exact Trump packing and its D4 uniform average, when separately commissioned as source controls | Known a.e. depth at most one; do not presume an unmeasured exact maximum for the uniform average |
| Missing event, omitted segment side or slab, reordered/equal endpoint events, altered source/weight, invalid radius, and malformed packet | Refuse a false complete receipt or independently detect its omitted excess |

Tests must include handcrafted expected answers, a producer-independent negative
witness, and cases where only a small interior face violates depth.
Agreement between two programs without these known answers does not establish
completeness.

### Cost, First Slice, and Disposition

Let $P$ be the number of positive placements and $M$ the distinct line count including
walls. The facet route has $O(M^2)$ cut segments/probes and a straightforward
$O(M^2(M+P))$ bound on exact field operations for clearance and membership checks.
The slab reader has $O(M^2)$ x-slabs; direct square-interval construction and endpoint
sweeps cost $O(M^2P\log P)$ exact operations.
These are operation-count estimates, not bit-complexity or wall-time bounds.
Algebraic division, coefficient growth, near-coincident events, and root-interval
refinement can dominate.

Implementation effort and target producer/replay costs remain unknown.
Exp-115’s reported 1.05-second producer and 0.75-second reader do not price an
arrangement. Do not inherit its 30-second caps or promise this verifier will fit them.
Set new finite process, event-count, memory, and serialized-output limits after control
costs are measured; hitting a limit remains unresolved, never complete feasibility.

The smallest useful funding request is **one 30-active-minute author slice followed by a
separately commissioned 15-minute independent review**, both control-only.
Build the complete facet procedure for small exact unit-square families, its strict
depth witness, and the degeneracy controls above.
Retain actual wall/CPU, operation counts, first obstruction, and remaining
implementation work.
Do not add target bindings or run the target during that slice.
The reviewer audits the completeness argument and controls; it does not accept global
readiness without the independent complete reader.
Price that reader and bounded packet integration from the first slice’s evidence rather
than assigning a fabricated total completion estimate here.

After both routes pass review and a new prospective target is frozen, complete checked
depth at most one for these weights would supply mass $56/5>11$ under H-099’s existing
BC-243 soundness requirements.
An independently checked excess would invalidate only these weights, leaving H-099
unresolved and permitting a separately priced exact-cut proposal.
A partial positive sweep, timeout, or disagreement proves neither outcome.
No reweighting, support extension, new row, LP, or new research allocation is authorized
by this assessment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
