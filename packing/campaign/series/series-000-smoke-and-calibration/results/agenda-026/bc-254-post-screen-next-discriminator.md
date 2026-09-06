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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
