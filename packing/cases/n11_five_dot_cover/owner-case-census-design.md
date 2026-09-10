# Prospective Exact Census of Coarse Owner Classes

**Status:** analytical continuation reviewed by GPT-6 Astra at extra high and by the
coordinator on 2026-09-09, adopted in
[Session114](../../campaign/agent-sessions/session-114-independent-owner-audit.md).
No new owner tuple, target cover, or geometry benchmark was evaluated.
The proper-containment obstruction below changes the next research priority; the
proposed census remains unrun and changes no registered bound.

The shared-arrangement census is sound for the strict footprint relaxation and avoids
one covering program per tuple.
Proper occupied-union containment cannot expand the coarse endpoint family: its patches
are congruent and every four-patch union has the same area.
Whole-container symmetry transport and refined larger footprints remain useful.

## Exact Congruence and Containment

Let $J$ be a counterclockwise quarter-turn, $S(x,y)=(y,x)$, and $G$ the full signed
owner-ray set. The direction construction makes $G$ invariant under $J$ and $S$, and
hence under $T=SJ$, the reflection $(x,y)\mapsto(x,-y)$.

At an anchor translated to the origin, write

$$Q_r=[0,h]r+[0,h]Jr,\qquad P_j=Q_{a_j}\cap Q_{b_j},$$

where $a_j,b_j$ are the exact first and last rays in closed sector $j$. Then

$$JQ_r=Q_{Jr},\qquad SQ_r=Q_{SJr}.$$

For the second identity, $J(SJr)=Sr$, so the two reflected edge vectors occur in
counterclockwise order.
The first map sends sector $j$ to $j+2$ modulo eight.
The ray map $SJ$ reverses angular order and sends sector $j$ to $7-j$, mapping its exact
endpoints to the reversed exact endpoints there.
Thus

$$JP_j=P_{j+2},\qquad SP_j=P_{7-j}.$$

These sector permutations act transitively on all eight sectors.
All endpoint shapes are congruent; changing marks translates them, and moving corners
reflects and translates them.
Every coarse endpoint patch has the same positive area $p$. This argument preserves the
rational endpoints on their actual sides of the nominal 45-degree boundary.

Each patch is contained in an anchored $h$-square and hence in a radius-$h\sqrt2$ disk
about its mark. The retained corner-pair premise gives every cross-corner mark distance
greater than $B\sqrt2=2h\sqrt2$. Patches at different corners are therefore separated
for every coarse class choice.
Every four-patch union has area $4p$.

If two such unions satisfy $A\subseteq A'$, they must be equal.
Otherwise a point of $A'\setminus A$ has an open neighbourhood disjoint from the closed
set $A$; that neighbourhood meets a full-dimensional polygon of $A'$ in positive area.
This contradicts equal areas.
This rules out proper **union containment**, beyond the equal-area obstruction for
same-index component containment.

Equality also has a short geometric discriminator.
The reviewed retained width has $0<\delta<\pi/4$. The endpoint quadrilateral has angles
$\pi/2-\delta,\pi/2,\pi/2+\delta,\pi/2$, so its unique acute vertex is the owned mark.
Equal patches must have the same mark, and their tangent cones at that mark determine
the retained endpoint wedge and sector.
Separated corner components cannot substitute for another physical corner.
Therefore coarse-union equality identifies the same geometric tuple, subject to the
implementation’s exact class-to-polygon transport.
Canonical polygon equality is still a useful control.

Refinement changes this conclusion: taking the convex hull of a refined rectangle with
the old footprint can create a proper enlargement.
Also, collision polygons can have useful containment *after clipping to one residual
centre domain*, even when the occupied patches do not.
That is an orientation-dependent cover test.

### Incorporate the Container Before Splitting More Classes

The existing
[pose-refinement contract](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/owner-pose-refinement-contract.md#exact-pruning-and-further-refinement)
already intersects possible owner centres with the container constraints.
The same step can be applied to an unsplit coarse class.
This offers a prospective way around the equal-area obstruction without first changing
16 classes per corner to 256.

For a retained signed owner frame $r,Jr$ in the class, let $K_r$ be its contained-centre
rectangle and put

$$Z_r=K_r\cap\bigl(m+[0,h]r+[0,h]Jr\bigr).$$

If $Z_r$ is empty, that frame cannot be an owner in the class.
For a nonempty $Z_r$, define a rectangle $R_r$ by the four projection bounds

$$
\max_{z\in Z_r} r\cdot z-h\le r\cdot x
\le\min_{z\in Z_r}r\cdot z+h,
$$

and the identical pair with $r$ replaced by $Jr$. All extrema occur at rational vertices
of $Z_r$. These inequalities say exactly that $x$ lies in every square $z+S_r$ with
$z\in Z_r$: they are the intersection of each square’s four support bounds over all
allowed centres.

The polygon $A_{\mathrm{wall}}=\bigcap_{r:Z_r\ne\varnothing}R_r$ is therefore a
guaranteed footprint for the coarse class.
It contains the old endpoint footprint, because the container restriction only removes
candidate owner poses.
If every $Z_r$ is empty, the class is impossible rather than a footprint with an
unbounded intersection.
Keeping nonempty degenerate $Z_r$ is conservative; dropping them needs the separate
strict-containment argument in the refinement contract.

This support identity is analytic.
No area gain, class elimination or stronger cover has been measured for these polygons.
The cheap prospective discriminator is to construct all sixteen bottom-left footprints,
verify nesting, and record where the inclusion is strict before choosing another
covering experiment.
Unlike the original congruent patches, these footprints use each frame’s relation to the
walls and need not all have equal area.

Sources: [owner geometry](../../devtools/owner_footprints.py),
[corner-owner sectors](../../campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md),
[endpoint containment](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/endpoint-footprint-review.md),
and
[pose refinement](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/owner-pose-refinement-contract.md).

## Shared Arrangement and Tuple Masks

At one retained angle let $S_\theta$ be the centred closed side-$B$ core and $K_\theta$
its closed legal centre rectangle.
In world coordinates, dot-hit and owner-collision polygons are

$$H_d=d-S_\theta=d+S_\theta,\qquad F_{c,j}=A_{c,j}+S_\theta.$$

Overlay the boundaries of $K_\theta$, five $H_d$, and all 64 $F_{c,j}$. For each
two-dimensional open cell inside $K_\theta$ and avoiding all five $H_d$, choose a
rational interior point $x$. Its four avoidance masks are

$$M_c(x)=\{j:x\notin F_{c,j}\}.$$

Membership is constant on the open cell.
The Cartesian product of its masks is exactly a set of tuples for which this core misses
all dots and all four chosen patches.
An empty mask contributes no tuple.
Owner polygons are optional obstacles: **subtracting all 64 would be unsound for the
census**, because it would miss cores that avoid the chosen four but hit an unchosen
patch.

Union these products across cells and angles.
An exact escape permanently refutes this fixed pattern on those relaxed tuples.
The complement is only a prefix survivor set until every required orientation has been
checked. A completed survivor inherits the existing strict-core transfer and
five-versus-seven count.
A failed tuple does not imply feasible owners, seven mutually compatible residual cores,
or an eleven-square packing.
Overlapping class labels do not add owners.

All geometry must use one frame.
In world coordinates $K_\theta$ is an axis-aligned rectangle; in core coordinates the
five $H_d$ are axis-aligned squares and $K_\theta$ is generally oblique.

## Boundary Obligations and Independent Audits

For one selected tuple its escape set is

$$\operatorname{int}(K_\theta)\setminus
\left(\bigcup_dH_d\cup\bigcup_cF_{c,j_c}\right).$$

It is open, because the excluded polygons are closed.
Every escape has a rational point off all arrangement boundaries.
Open two-dimensional cells therefore suffice.
A dot on a closed core boundary counts as a hit; owner contact is forbidden by the
strict-core contract.
A centre on an unselected class boundary can be perturbed inside the selected tuple’s
open escape set. No boundary-only escape is lost.

For vertical decomposition, retain all vertex abscissae and isolated segment
intersection abscissae.
Collinear overlap endpoints are already vertex events.
Use exact equality and ordering for vertical/coincident edges, triple crossings,
nesting, tangencies, repeated vertices, and degenerate clips.
Only open strips supply witnesses.
Independently replay every retained witness against the open container, closed dot
polygons, and all selected closed collision polygons.

The existing vertical-decomposition routine supplies relevant conventions, but its union
output loses the membership labels needed for the census.

The independent audit’s inclusion-exclusion proof is sound.
For the fixed five dot polygons and four owner collision polygons, 511 nonempty subsets
suffice. Exact zero uncovered area forces coverage of the container interior: an omitted
interior point would have an open disk disjoint from the finite closed union and hence
positive uncovered area.
Closedness extends this to all of the closed container.
This covers boundaries and requires no claim about an event-boundary mass minimum or LP
optimality.
Zero-area intersections and every descendant intersection may be pruned since
further constraints cannot increase area.
Negative uncovered area is an invalid computation.
Positive area detects failure; an additional extraction step supplies an exact witness.

Recursive convex subtraction is also sound if each selected closed obstacle is removed
by its exterior half-planes and every positive-area surviving piece is retained.
A first-violated-edge convention makes interiors disjoint; retaining all exterior pieces
duplicates work but covers the complement.
Pieces represent closures, so an interior sample must be replayed with strict
predicates. Dropping zero-area pieces is safe for the open escape set.
For the shared census, subtract only the five common dot obstacles and then split and
label owner boundaries.
Changing the outer algorithm does not independently check a shared faulty clipper.

The [independent union contract](union-contract.md) gives this argument for the retained
five-dot audit. Its mathematical review found no coverage or boundary gap.

## Shared Work and Symmetries

Eight endpoint shapes at the origin generate the 64 owner polygons by translation to the
eight corner marks. Minkowski addition commutes with translation, so only eight shape
sums per residual angle are needed.
The five dot polygons are translations of one square.
The source-derived initial edge bound is $64\cdot8+5\cdot4+4=536$; no arrangement size
or runtime has been measured.
Deduplicate identical geometry while retaining all labels.
Processing dot-free cells first avoids labeling regions that cannot supply an escape.

Store one exact witness per distinct mask quadruple and a 65,536-bit failure table.
Coordinatewise-contained mask products are redundant.
Stream angles, updating failures monotonically, and record cuts, open cells, distinct
masks, rational bit lengths, wall time, and peak memory.
Exact intersection arithmetic can dominate even when the tuple bitset is small.

Whole-container D4 maps must transport dots, patches, direction indices, corner labels,
and witnesses together.
The frozen dot pattern has diagonal and central symmetry and lacks horizontal/vertical
symmetry, as recorded in the transfer review.
Its stabilizer has four elements, so its D4 orbit has two patterns.
One completed census supplies the other pattern’s table by exact global permutation.

For the particular retained patch union $A$ and dot set $P$, the
[transfer review](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/five-dot-transfer-review.md)
records the exact symmetry distinction.
With $H,V$ the horizontal and vertical reflections, $D,D'$ the diagonal reflections, and
$R$ the half-turn,

$$\operatorname{Stab}(A)=\{1,H,V,R\},\qquad
\operatorname{Stab}(P)=\{1,D,D',R\}.$$

The square’s eight-element symmetry group therefore produces two distinct patch unions
and four patch-and-dot pairs.
In the common reflected bottom-left labels, diagonal reflection changes the all-`m1:j0`
tuple to the all-`m2:j7` tuple: it swaps the marks and sends sector $j$ to $7-j$, while
conjugating $H$ to $V$. The equality discriminator above means symmetry plus
coarse-union containment reaches only these two geometric tuples.
This is an analytic orbit argument, not a measured fraction of physically possible
packings; class labels may overlap.

Diagonal reflection preserves the dots while permuting tuples and paired orientations.
This can reduce a *whole-table census* to 181 representative orientations even though it
cannot fold the selected asymmetric T-023 union alone.
Require exact class/direction permutations; first check all 361 directly and use the
identities as controls before adopting the fold.

## First Prospective Bounded Experiment

After independent T-023 replay, freeze q, B, the full owner manifest, endpoint
construction, dots, class order, and the already-certified tuple set including
simultaneous symmetry transports.
Ask: **Does this unchanged pattern cover any coarse tuple beyond those transports?**

Validate on synthetic rational arrangements with known covers and escapes, including
thin strips, coincident edges, tangencies, empty masks, and mutations invalidating each
witness predicate. Compare all toy mask products against direct tuple-by-tuple
nine-obstacle checks.
Reproduce the frozen T-023 answer before any new scientific verdict.

The proposed target scope is all 65,536 coarse tuples, the unchanged five dots, and the
complete 361-direction manifest, with no adaptive dots or footprints.
An existence screen can stop before a complete census: one independently verified
additional tuple proves expansion, while checked escapes for every additional tuple
refute it even if they were all found in a short direction prefix.
The unclassified part of any partial table must remain explicit.
Proposed bounds are 30 minutes of target-process wall time and 2 GiB of memory; these
are experiment limits to freeze before execution, not runtime predictions.
Save progress and checked partial escape witnesses after each direction.

| Verdict | Condition |
| --- | --- |
| Accept expansion | An independent complete361-direction nine-obstacle check verifies a tuple beyond the frozen transported set, selected by the prospectively frozen order; all source, class and coverage guards pass. A partial census remains partial. |
| Refute expansion by this pattern | Every tuple beyond the transported set has a directly checked rational escape. This may be decided before all orientations are processed; a failed pattern needs only one escaping orientation per tuple. |
| Incomplete | A declared limit is reached before either condition, required checks are missing, or geometry remains unresolved. Validated partial escapes remain useful. |
| Invalid | Any control, provenance, strict-witness, permutation, or known-answer check fails. No scientific accept/refute may be recorded. |

An independent check of one survivor confirms existence of an expansion, not the whole
survivor table. To certify every newly listed tuple, verify the full arrangement
certificate or independently replay each distinct certificate class.
The result guides another dot pattern or selective pose refinement.
A global n=11 bound still requires covering every admissible owner case, with all
physical transfer premises retained.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
