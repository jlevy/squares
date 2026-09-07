# BC-265: Calibration Scope and the Next Discriminator

The accepted seven-row certificate gives an explicit D4-symmetric area density of mass
eleven that covers every placement in the old sixty-placement support.
Coverage of the full pose space remains unproved.
The cheapest useful next test is a counterexample to this particular calibration, with a
strict limit on the cost of finding it.
A general expanded-support engine is not justified by exp128.

This is the independent source-free review under `think-ju6v` in
[Session095](../../../../agent-sessions/session-095-collision-cover-and-support-ceiling.md).
Dispatch was 2026-09-07 at 13:04:15 UTC; observed start was 13:04:45 UTC. The original
hard deadline is 13:26:00 UTC. The parallel design report was not read or imported
before this report froze.
No scientific field, placement, geometry, factory, sample or target was evaluated.
The reviewer owns only this note; the coordinator owns registration and funding.

## An Explicit Calibration on the Old Support

Let $C=[0,U]^2$ be the exact Trump container, $G=D_4$, and
$\mathcal F=\bigsqcup_{j=1}^8 O_j$ the accepted deduplicated support.
Write $d_j=|O_j|$. The accepted
[exp128 output](../exp-128-h099-seven-row-support-ceiling/verification.json) supplies
seven closed boxes $B_i$, each of positive area $A_i$, nonnegative multipliers
$\lambda_i$, and distinct selected members meeting the inclusion quotas $R_{ij}$. Its
exact identities are

\[
\lambda^T R=d^T,\qquad \sum_i\lambda_i=11.
\]

Define the unsymmetrized density and its D4 average by

\[
\rho_0(x)=\sum_{i=1}^7\frac{\lambda_i}{A_i}\mathbf1_{B_i}(x),
\qquad
\rho(x)=\frac18\sum_{g\in G}\rho_0(g^{-1}x).
\]

Both are nonnegative and integrable, with mass eleven; $\rho$ is D4 invariant.
There are at most 56 distinct image boxes, represented by exactly 56 labelled terms.
Overlapping boxes add their densities.
Coincident images must retain their summed weight; geometric deduplication without
multiplicities changes the measure.
The common radius remains $r=1/100000$, so $A_i=4r^2$. No atom or square-boundary charge
occurs.

For $S\in O_j$, orbit-stabilizer counting gives

\[
\int_S\rho
=\frac1{d_j}\sum_{Q\in O_j}\int_Q\rho_0
\geq\frac1{d_j}\sum_i\lambda_iR_{ij}=1.
\]

Each selected member contains the entire corresponding box, so its $B_i$-term in the
middle sum contributes exactly $\lambda_i$. Unselected members contribute nonnegative
amounts. The proof needs the accepted positive inclusions, not an unperformed exclusion
or constant-incidence check.
The unsymmetrized $\rho_0$ alone need not cover each old placement; the group average is
essential.

In fact, every old placement captures exactly one.
Let $c_j$ be the number of original packing seeds in $O_j$. The accepted D4 average of
that packing has strictly positive weights $w_Q=c_j/d_j$ on every member of $O_j$, mass
eleven and depth $D_w\leq1$ almost everywhere.
Consequently

\[
11=\sum_{Q\in\mathcal F}w_Q
\leq\sum_{Q\in\mathcal F}w_Q\int_Q\rho
=\int_C\rho D_w\leq\int_C\rho=11.
\]

Since all $w_Q>0$, equality forces $\int_Q\rho=1$ for every old member.
It also forces $\rho(1-D_w)=0$ almost everywhere.
This is a consequence of two explicit certificates, not an assumption of strong duality
or attainment for the continuum problem.

The baseline weights in archive order are $(3/4,1/8,1/4,1/8,1/8,1/8,1/8,1/8)$. The
source correspondence, all 88 labelled images, their sixty-placement quotient, the
eight-orbit permutation and the seven positive rows are accepted exp128 premises; they
are not reconstructed or remeasured here.

## What a New Pose Would Establish

Let $P$ be a contained full unit square, and write

\[
F(P)=\int_P\rho
=\frac18\sum_{g\in G}\sum_i
\frac{\lambda_i}{A_i}\,|P\cap gB_i|.
\]

An independently verified $F(P)<1$ disproves universal coverage by this fixed
calibration. It also shows $P\notin\mathcal F$, since all old members capture one.
Its entire D4 orbit has the same capture, without requiring another measurement.

It does not prove
[H-116](../../../../hypotheses/H-116-expanded-full-size-dual-support.md).
A different mass-eleven calibration could cover the enlarged finite support.
Even a violated constraint for one optimal finite dual certificate need not improve the
reoptimized primal objective when other optimal dual certificates exist.
An H116 accept still requires explicit nonnegative placement weights of total mass above
eleven and an independent, complete almost-everywhere depth certificate.
Pairwise screening, an overweight graph clique or a finite necessary-row LP does not
supply that certificate.

Nor does the pose refute the existence question in
[H-101](../../../../hypotheses/H-101-trump-equality-density.md), reject another density
family, or improve a packing lower bound.
Conversely, proving $F(P)\geq1$ for every admissible pose would settle H101’s
density-existence part for this candidate, but would leave the complete compatible
eleven-placement equality set unclassified.
Mass eleven alone does not exclude eleven squares.

Even an accepted H116 mass above eleven would only obstruct the endpoint one-body
density route at $U$. It would not exclude a packing or resolve
[H-100](../../../../hypotheses/H-100-below-trump-area-density.md) at a smaller side.
These are different scientific payoffs, not alternative labels for the same result.

## Selected Small Test: An Axis-Aligned Calibration Falsifier

The fixed object is $\rho$ above.
Select only an axis-aligned contained unit square as the first possible counterexample.
This avoids a new rotating-polygon area instrument.
It is a proposed discriminator, not a registered hypothesis or permission to evaluate
its grid.

For an image box $B=[a,b]\times[c,d]$ and center $(x,y)$, its intersection area is

\[
|B\cap P_{x,y}|=\ell_{a,b}(x)\ell_{c,d}(y),
\qquad
\ell_{a,b}(x)=\max\{0,\min(b,x+1/2)-\max(a,x-1/2)\}.
\]

The center domain is $[1/2,U-1/2]^2$. An overlap length is continuous and piecewise
affine, with breakpoints $a\pm1/2,b\pm1/2$. Include the domain endpoints and all
breakpoints lying inside the domain for every labelled image box, then sort and
deduplicate exactly.
On each closed Cartesian grid cell, $F$ is bilinear; its minimum is attained at a
vertex. Therefore the complete grid suffices for the axis-aligned minimum.
Closed walls and zero-area tangencies are included, not discarded as open-cell
exceptions.

There are at most 226 events per coordinate and 51,076 grid vertices before exact
deduplication. Those are combinatorial upper bounds from 56 boxes, not measurements of
the scientific source.
The naive calculation has at most 2,860,256 box terms.
A cached one-dimensional overlap table can reduce repeated work, but this estimate does
not promise completion within a proposed runtime cap.

Freeze the exact source, 56 labelled terms, event rule, traversal order, finite caps and
a narrower claim before any target run.
A producer may stop at its first exact under-covered pose.
The independent reader need check only that one pose, the exact calibration identity and
all 56 area terms. It need not reproduce the discovery grid.
The accept predicate is a strictly positive exact deficit $1-F(P)$, with the pose
contained in the exact container and both processes actually exiting zero.

A search that finds no witness, reaches its cap or refuses arithmetic gives no universal
verdict. Even a producer’s completed nonnegative axis minimum is not an independently
certified full-pose cover.
An optional complete axis reader would need to reconstruct the entire event grid and
every necessary minimum; it is outside this first negative-witness pilot.

The independent reader must bind the accepted exp128 row data and source embedding,
reconstruct all D4 image boxes with multiplicity, verify unit size and closed
containment of the proposed axis-aligned square, and recompute the weighted areas.
It must not trust a supplied capture, omitted box, symmetry count or Boolean verdict.
Shared exact arithmetic is acceptable if disclosed.
The existing atomic `sqpack.fractional.sweep` is not a drop-in area verifier: its
coverage is piecewise constant, whereas this coverage is piecewise bilinear.

Source-free controls should cover disjoint and nested rectangles, partial overlaps, line
and point tangencies with zero area, coincident D4 terms whose weights must add, wall
endpoints, a nontrivial bilinear cell, exact deficits of both signs and zero, foreign
embeddings, omitted terms and malformed coefficient widths.
Use unrelated rational and genuine degree-eight examples, not the Trump constructor.
Scientific constructors remain forbidden in controls; lexical, byte, event and process
limits are separate admission obligations.

## Price, Stop and the Alternative

My recommendation is a conditional GO for this falsifier as a short routing test, not as
the next two-hour main proof program.
The following are prospective estimates, not costs measured on a new source or target:

| Allocation | Proposed ceiling | Required output |
| --- | --- | --- |
| Source-free producer and separately implemented reader, with controls | 25 combined author-minutes | Frozen, narrow area calculation and bounded axis discovery; no general geometry engine |
| Independent code, mathematical and source-binding review | 20 reviewer-minutes | Rejected mutations and a GO or explicit remaining premise |
| Protocol admission and disposition | 15 coordinator-minutes | One frozen target contract, gates, retained result and stop |
| Scientific discovery, if separately authorized | One 60-second complete-child attempt | An exact candidate or unresolved output; no restart |
| Positive-candidate independent reader | One 30-second complete-child attempt | An independently accepted strict deficit or refusal |

The author, reviewer and coordinator estimates total sixty agent-minutes.
They are a willingness-to-spend limit for a modest conclusion, not a forecast of a
successful implementation or witness.
Runtime limits must be finalized before the scientific call, using source-free readiness
evidence. No existing scientific budget is reopened by this proposal.
If separate implementations cannot fit the combined author allocation, decline the pilot
at that boundary rather than count parallel wall time as total agent cost.

Stop if the narrow implementation does not fit that price, if the target produces no
accepted witness, or immediately after an accepted witness.
None of these outcomes funds density repair, an angle sweep, new arcs, added dual
weights or a complete-depth engine.
Reopening H116 requires an explicit promising expanded support and weights together with
a credible price for complete depth certification.
Reopening a universal H101 proof requires a density candidate with a complete
pose-and-wall coverage plan and a separately priced compatible-equality obligation.

The separable fallback is
[BC-264 / H-114](../../../../hypotheses/H-114-two-pose-kernel-exclusion.md): one
30-minute source-free choice of a small feature family at the already stated side
$96/25$, conditional on acceptance of BC260’s kernel contract.
Its discriminator should be an exact necessary-constraint obstruction to that fixed
family, or a $b<11$ candidate with a bounded plan for exact PSD, the full diagonal
domain and every compatible pair, including touching pairs.
A genuine complete certificate there would improve a global lower bound.
Feature selection alone would not.
No degree escalation or six-dimensional general separator is funded by this fallback.
It does not use or duplicate external Session092’s BC261/273 interface and successors.

BC257 / H100 has the direct mass-below-eleven payoff, but no specified lower-side
density family or continuum price emerged from this review.
Preserve it for its own candidate-selection slice rather than infer transport from the
endpoint calibration.
[H-115](../../../../hypotheses/H-115-boundary-null-curved-resources.md) supplies no
advantage for this immediate test: the boxes already have no boundary charge, and curved
resources still owe uniform pose integrals through tangencies and root collisions.
A genuine finite depth obstruction also constrains line-null curved resources; changing
the representation does not evade it.
For a finite square support, depth is constant off the finite union of edge lines on
each arrangement face.
Thus an a.e. depth certificate and zero measure on those lines are enough for this
extension; arbitrary singular measures do not inherit the same argument.

These distinctions follow the existing
[BC265 selection rule](../../../../agendas/agenda-027-compatibility-and-restricted-families.md#how-to-choose-between-the-alternatives):
fund one specified object’s next useful test, or defer.
Neither exp128 nor this source-free calibration proof licenses a larger verifier or
changes a global bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
