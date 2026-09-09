# What the Owner-Conditioned Cover Sprint Has Established

The sprint has excluded a genuine four-owner case at $q=96/25=3.84$: five rational dots
meet every allowable remaining core in that case.
Exp144 verified the complete 361-direction net exactly; the reviewed owner-footprint and
strict-core arguments transfer that result to physical squares at arbitrary angles.
An independent check of the residual-domain union is deferred to the next slice.
This is a conditional branch theorem, not an exclusion of eleven squares from the
container in general.
The case comes from a premise proved for every hypothetical eleven-square packing: four
distinct squares own specified corner marks.
Turning that premise into occupied area has now produced a substantial numerical gain.

## The Problem and the Covering Method

We replace each physical unit square by a slightly smaller, concentric core of side
$B=9977/10000$, with a nearby orientation from the retained rational net.
The shrink leaves the selected core strictly inside its parent.
This lets us use exact rational geometry while retaining a rigorous route back to
arbitrary physical angles.

A weighted-dot cover puts nonnegative mass at chosen points and requires every allowable
core to contain at least one unit of mass.
Eleven disjoint cores would then require at least eleven units altogether.
A globally valid cover of mass below eleven would therefore exclude the packing.

Conditioning changes which cores the cover must meet.
If four distinct cores are already identified, and we know regions that those cores
occupy, the other seven cores must avoid those regions.
A cover of all these remaining possibilities with available mass below seven would
exclude that conditional case.
To prove the general result, the cases must cover every possible packing, and every case
must be excluded.

The proved corner-pair premise supplies four distinct owners, each containing at least
one of two marks near its corner.
It does not place four unit squares flush against the container.
See the
[BC303 corner-pair replay](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md).

## Why Owning a Point Is Not Enough

A useful new sanity check explains why the owner premise needs geometry.
Suppose a residual cover meets every core avoiding an owned mark $m$. Adding a
unit-weight dot at $m$ makes it a global cover: any core either contains the mark or was
already covered. Consequently the true matched optima satisfy

$$
\tau_{\mathrm{global}}\leq\tau_{\mathrm{point}}+1.
$$

For four owned marks, the added cost is at most four.
Point conditioning alone therefore cannot improve the exclusion margin beyond the
reduction in the number of cores we have to cover.
We need the owner’s occupied area, its allowed position and angle, or another geometric
restriction to obtain additional power.
This is an exact construction; comparing two unfinished numerical objectives is not a
test of the optimum inequality.
See the
[point-extension lemma](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/point-extension-lemma.md).

We now have guaranteed occupied footprints.
From a mark inside a core, choose the two perpendicular directions toward its centre.
At least half a core side is available along each direction, so an anchored quarter of
the core is occupied.
Splitting these directions into eight sectors gives a rational triangle common to every
pose in each sector.
Intersecting the two endpoint quarter-squares enlarges that triangle to a common
quadrilateral. These regions lie inside the selected owner core itself.

Two possible marks and eight sectors give sixteen exhaustive classes per corner, or
$16^4=65{,}536$ raw four-owner combinations.
Closed sector boundaries can belong to both adjacent classes.
A footprint’s area does not guarantee that it contains one unit of cover mass: four
distinct owners justify the remaining count of seven, but small footprints do not
automatically save four units of weight.
See the
[triangle proof](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md)
and
[enlarged-footprint contract](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/owner-footprint-contract.md).

## What the Experiments Say

**Exp136 found a numerical gain in the fixed-corner example.** On matched finite support
and directions, the unrestricted objective was about $11.981481$ and the residual
objective about $7.804878$. The reduction exceeded the four-owner count by about
$0.176603$. This is evidence that occupied-region conditioning can improve the numerical
comparison. The residual mass still exceeds seven, and the difference between two primal
solutions is not an exact optimum-gap proof.
This special case does not establish the general owner premise.
[Exp136 record](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-136-repaired-fixed-corner-pilot.md)

**Exp137 and exp138 failed to recover an obstruction from the existing fractional
family.** A fractional family is a weighted collection of possible cores with total
weight through any point at most one.
Its total weight gives a lower bound on the mass any cover needs; it is not a physical
packing. The shared exact producer filtered an existing family against every declared
owner-footprint class.
None of the sixteen one-owner endpoint classes retained weight at least ten, and none of
the $65{,}536$ four-owner classes retained weight at least seven.
The records retain independent receipt-audit obligations, so these are scoped producer
results pending that audit.
[Exp137](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-137-corner-dual-salvage.md),
[exp138](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-138-four-owner-dual-salvage.md)

The point controls already retained only about $9.417433$ for one owner and $6.517094$
for four. Any larger obstacle containing the same marks deletes at least those same
poses. With the weights unchanged, its surviving mass can only fall.
Subject to the pending receipt audit, this closes further deletion-only refinements of
this family as a route to the ten- or seven-unit obstruction.
It does not show that a useful cover exists, or that a newly optimized fractional family
could not obstruct one.

**Exp139 supplied an exact conditional cover, with an honest normalization cost.** The
unchanged rationalized exp136 residual weights have mass $7.804903$. Their exact minimum
coverage over the full folded net is $760979/800000$, below one, so the raw cover failed
verification. Dividing all weights by that positive minimum produces a feasible
normalized cover of exact mass

$$
\frac{31219612}{3804895}\approx8.205118.
$$

Here the fixed obstacles and verified weighted measure have the required square
symmetries. Together with the strict-core shrink inequality, the complete net check
transfers to all physical angles in the literal four-flush-corner case.
The effective mass remains above seven, so this yields no eleven-square exclusion and no
exact optimum-gap claim.
It does show that the numerical candidate can be turned into a rigorously interpretable
conditional cover without solving another LP.
[Exp139 record](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-139-fixed-corner-full-net-replay.md)

**Exp140 left the generic area comparison unresolved.** Its unrestricted arm converged
numerically, but the point arm reached the sixty-round limit with minimum coverage about
$0.955338$. Neither the triangle nor the enlarged-footprint arm ran.
The clean process exit is not a completed experiment, and the unfinished point objective
is not a feasible-cover result.
The limitation was the iteration allowance, reached in seconds, rather than exhausted
wall time.
[Exp140 record](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-140-h139-owner-footprint-matched-gain.md)

## The Completed Area Comparisons

**Exp142 isolated a clear one-owner area gain.** All four arms converged numerically:
unrestricted $11.884615$, point $11.574515$, triangle $10.555556$, and enlarged
footprint $10.388889$. The enlarged footprint improves on the bare point by about
$1.185626$. This measures the extra value of occupied area.
It still misses the ten-unit threshold for excluding a one-owner case.
The comparison uses the same available support and nine residual directions; the owner
footprints themselves come from the full manifest.
[Exp142 protocol](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-142-one-owner-completion.md)

**Exp143 produced the strongest candidate: five dots for four guaranteed owners.** For
four reflected copies of the prescribed $m_1$, sector-zero class, all four arms
converged: unrestricted $11.884615$, point $9$, triangle $6$, and enlarged footprint
$5$. The area arms passed below the seven-unit residual threshold on the nine-direction
screen. The point-extension and nested-domain numerical sanity checks passed.

The enlarged-footprint candidate is especially simple.
It has five rational sites, each with the same rounded weight $\beta=1000001/1000000$.
Its exact saved mass is $5\beta$, not exactly five.
But every core collects an integer multiple of $\beta$. If a complete exact replay over
all 361 residual orientations proves a positive minimum, that minimum is at least
$\beta$. Dividing by $\beta$ then gives five unit dots meeting every relevant core.
At most five pairwise disjoint residual cores could fit, whereas an eleven-square
packing in this branch requires seven.
No LP optimality proof is needed for that counting contradiction.

Exp143 supplied the numerical candidate; exp144 supplied its exact replay.
The full net is essential because the five-dot measure and the obstacle union do not
share the symmetries needed to justify the folded shortcut.
[Exp143 raw receipt](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json)

**Exp144 passed the exact full-net check.** The source-bound reader completed all 361
orientations in about 12.76 seconds.
Every direction has exact minimum coverage $1000001/1000000=\beta$, and the normalized
total mass is exactly five.
Independent receipt scrutiny confirmed all indices and labels once each, positive
reachable-cell counts, and the source blob against both the saved exp143 file and its
recorded Git commit.
The reader evaluated 589,549 dense event cells in total.
[Exp144 receipt](/Users/levy/.codex/worktrees/88e2/squares/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-144-four-owner-endpoint-full-net-replay.json)

The computation proves coverage of the finite net.
The separate mathematical argument supplies the physical implication: each unit parent
contains a selected net core strictly; each owner footprint lies in its selected owner
core; and the remaining selected cores avoid those footprints with positive clearance.
Thus every remaining core contains one of the five dots.
Pairwise disjoint cores cannot share a dot, so at most five remain.
An eleven-square packing in this four-owner branch would require seven and is therefore
impossible. The general packing bracket does not change: other owner combinations have
not all been excluded.
An independent domain-union instrument and confirmation are deferred to the next slice;
no exp145 target was registered or launched.

## What Deserves the Next Effort

The immediate assurance priority is the independent domain-union confirmation.
The next research priority is extending the certificate before a broad LP campaign.
Transform the dots and owner regions together under valid container symmetries.
Reuse a certified pattern for any class whose guaranteed occupied union contains the
certified obstacle union.
Prune classes only with an exact impossibility argument, such as incompatible required
owner footprints or an empty legal-owner pose domain.
Shared marks or overlapping class labels do not create additional owners.

Build a small portfolio of dot patterns, starting with the certified five dots and their
symmetry images. Six unit dots also suffice for a seven-core contradiction.
Test unresolved classes against these patterns, retain exact uncovered-core witnesses,
and optimize only the cases still uncovered.
Reuse direction geometry and event partitions where their contracts agree.
This can exploit shared geometry and avoid blindly solving all $65{,}536$ combinations.

If small guaranteed footprints lose too much information, the next mathematical
refinement is to partition owner position and angle more tightly.
A smaller pose class gives a larger common occupied intersection, or allows a stronger
condition that a remaining core must coexist with at least one legal owner pose.
These are ways to strengthen the conditional covering problem.
More deletion of the same weighted fractional family cannot supply the missing
obstruction; changing that direction would require new poses or newly optimized weights
with a valid depth bound.

The remaining proof obligations are substantive: cover every possible owner case, check
successful candidates over the complete required orientation family, retain strict-core
transfer, and get the effective mass below the correct remaining-core count.
The sprint has clarified and instrumented those obligations.
The completed comparisons and exact replay justify pursuing conditional geometry: the
program now has a concrete branch exclusion to extend.

The untested independent-audit draft and proposed controls are retained as text in
[unrun-independent-audit](unrun-independent-audit/check_five_dot_cover.py.txt).
They are next-slice engineering material, not additional evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
