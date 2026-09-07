# BC265: What the Seven-Box Calibration Unlocks

Do not automatically expand the density support after closing H099. The seven boxes give
an explicit mass-eleven area density calibrated on the old sixty placements.
Finding another placement that this density undercovers would reject that particular
density, not establish a stronger dual or a packing bound.

For the next research allocation, prefer **BC264/H114’s small interaction-kernel
discriminator**, subject to its missing feature and verification contract.
Keep an **H101 common-support obstruction under BC265** as the independent fallback, but
only if a concrete pose and a finite exact exclusion certificate become available.
Neither recommendation authorizes a target or a general verifier build.

This is Session095’s source-free `think-bmuz` design, allocated from 2026-09-07 13:02:00
to 13:26:00 UTC; the first observed clock was 13:02:34 UTC. The coordinator reports that
[exp128](../../experiments/exp-128-h099-seven-row-support-ceiling.md) completed with
exit zero, all seven rows and 41 inclusions, full 88/60/8 source identity, upper bound
eleven and baseline mass eleven, in 1.12 seconds wall.
Its output audit and registry disposition are separate.
The derivation below states the premises explicitly and does not perform that audit.
No scientific constructor, field, placement, geometry, target, or test was evaluated
here. The parallel assessment was not inspected.

## Calibration from Positive Inclusions

Let $C=[0,U]^2$ be the exact Trump container, $G=D_4$, and $\mathcal F$ the sixty
distinct squares in the full $G$-closure of the accepted eleven-square packing.
Write its eight orbits as $O_j$, with sizes $d_j$. Let $B_r\subset C$, $r=1,\ldots,7$,
be the verified positive-area boxes.
The prescribed integer $R_{rj}$ counts distinct selected members of $O_j$ whose
interiors contain the entire closed box $B_r$. Unselected members need not have been
classified.

The retained certificate supplies nonnegative multipliers satisfying

$$
\sum_r\lambda_r=11,
\qquad \sum_r\lambda_rR_{rj}=d_j.
$$

Define the unsymmetrized density and its container-symmetry average by

$$
\rho_0(x)=\sum_r\frac{\lambda_r}{|B_r|}\mathbf1_{B_r}(x),
\qquad
\bar\rho(x)=\frac18\sum_{g\in G}\rho_0(g^{-1}x).
$$

Both are nonnegative integrable area densities of mass eleven.
Overlapping or duplicate boxes retain their additive weights; no disjointness of the
boxes is assumed. Every container symmetry preserves area and maps the container to
itself. These densities charge no square boundary.

For $S\in O_j$, each member of $O_j$ appears $8/d_j$ times among $g^{-1}S$. Therefore

$$
\begin{aligned}
\int_S\bar\rho
&=\frac1{d_j}\sum_{T\in O_j}\int_T\rho_0\\
&=\frac1{d_j}\sum_r\frac{\lambda_r}{|B_r|}
                 \sum_{T\in O_j}|T\cap B_r|\\
&\ge\frac1{d_j}\sum_r\lambda_rR_{rj}=1.
\end{aligned}
$$

Only the verified positive inclusions were used in this inequality.
To obtain equality, sum it on the original eleven-square packing.
Its interiors are disjoint and its boundaries have zero area, so the sum of those eleven
integrals is at most the total mass eleven.
Each integral is at least one; hence each equals one.
$G$-invariance then gives

$$
\int_S\bar\rho=1\qquad\text{for every }S\in\mathcal F.
$$

This proves an explicit absolutely continuous calibration for the finite support.
It does not assume strong duality, primal attainment for the full placement space, or
the archive’s stronger exclusion-margin checks.
It refines the calibration argument in the
[contributed review](../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/original_review/n11_research_review.md#equality-density-has-a-much-smaller-necessary-support)
to the positive-only row semantics.
The relevant weak-duality and boundary conventions are in
[BC242](../agenda-026/bc-242-full-size-density-proof-contract.md).

## What One Undercovered Pose Would Decide

For a proposed exact contained unit square $P$, the calibration coverage is

$$
F(P)=\int_P\bar\rho
=\frac18\sum_{g\in G}\sum_r
  \lambda_r\frac{|P\cap gB_r|}{|B_r|}.
$$

There are at most 56 weighted rectangle-intersection terms for one fixed pose.
This is a finite operation inventory, not a measured runtime.
Tangencies contribute zero area; repeated transformed boxes must retain their total
weight. The source binding, real embedding, containment and exact intersection-area
reader would still need review before a scientific use.

An independently verified $F(P)<1$ would establish that:

- $\bar\rho$ is not a feasible covering density for all contained unit squares;
- $P$ is outside the old support, since every old member has coverage exactly one;
- the calibration is a useful proposer of a changed support or density constraint.

It would **not** establish that every mass-eleven density fails, that the expanded
finite-support optimum exceeds eleven, or that the old support ceiling was wrong.
A different old-optimal density or upper witness may cover the new pose while retaining
mass eleven. Failure of one optimal certificate is not failure of every optimal
certificate. A new pose with smaller calibration integral is therefore not, by itself, a
sufficient reason to commission a complete expanded-depth verifier.

For a simple symbolic counterexample, let two unit squares $A,B$ have both $|A\cap B|>0$
and $|A\setminus B|>0$. A mass-one density supported on $A\setminus B$ covers the old
support $\{A\}$ and gives coverage zero on $B$. Nevertheless, any feasible weights on
$\{A,B\}$ have sum at most one, by the necessary depth inequality on their positive-area
intersection. The expanded optimum is still one.
No particular source placement is evaluated in this example.

Neither a deficient pose nor a subsequently verified $D>11$ at $U$ improves the global
packing lower bound.
The latter would rule out the endpoint mass-eleven density route by weak duality.
It does not exclude a packing at a smaller side, and wall-touching placements have no
automatic below-$U$ transport.
[H116](../../../../hypotheses/H-116-expanded-full-size-dual-support.md) owns expanded
supports; H099 remains the old support only.
H116 is an open question, not an executable substitute for a narrower frozen support
claim and protocol.

## A Stronger, Independent Equality-Support Test

Let $A_g$ be the union of the eleven squares in symmetry image $g$ of the accepted
packing, and put

$$
\Omega=\bigcap_{g\in G}A_g.
$$

Any nonnegative area density of mass eleven covering every unit-square placement must
vanish almost everywhere outside each $A_g$: its eleven disjoint-interior squares
already require all eleven units of mass.
It therefore vanishes almost everywhere outside $\Omega$. The same conclusion holds for
the calibration, since it covers all old members.
Thus the union of positive-weight transformed boxes $gB_r$ is contained in $\Omega$ up
to area zero. Their union is not assumed to equal $\Omega$.

An exact contained unit square $P$ with $|P\cap\Omega|=0$ would thus refute the
existence part of H101, not merely the current calibration.
No such square or zero-area intersection is asserted here.

There is also a direct finite-dual consequence of that stronger premise.
Let $w_0$ be the average of the eight original packings, of mass eleven.
Away from their finitely many boundaries its depth is the number of covering packing
unions divided by eight.
On $P\setminus\Omega$, that number is at most seven.
Consequently

$$
w_0+\frac18\delta_P
$$

would have depth at most one almost everywhere and mass $89/8>11$. This conditional
construction needs no optimizer or strong-duality theorem.
It remains an endpoint density obstruction, not a new packing bound.
It also shows why the missing premise is the full $\Omega$ intersection, not an empty
intersection with the seven calibration boxes.

A possible finite certificate would cover $P$ by convex polygons, each assigned to one
source packing and proved interior-disjoint from all eleven squares of that packing.
Outside the finite polygon and square boundaries, every covered point is absent from at
least one $A_g$. This would certify the required area-zero intersection without
constructing every cell of the full Boolean arrangement.
Every source packing, polygon and cover seam must be accounted for; a point sample or an
incomplete cover would not suffice.

This is only a certificate design.
No pose, void polygon inventory, source construction or runtime has been supplied.
The existing
[closed-cover reader](../../../../../devtools/check_closed_polygon_cover.py) admits
fields only through degree four, while the exact Trump source uses degree eight.
Its current readiness cannot be inherited by this fallback.
The generic graph route also caps families at 64 squares: adjoining a generic
eight-member D4 orbit to the old sixty would exceed that ceiling.
One unsymmetrized new placement would instead give 61, but still needs a new source
binder and a complete depth argument; a graph overweight clique remains inconclusive.
No cap change or adapter is commissioned by this note.

## Comparative Disposition

| Existing entry | Result that would justify further work | Concrete input now available | Missing premise and disposition |
| --- | --- | --- | --- |
| BC265 / H101 | An exact $\Omega$-avoiding pose, or an actual globally covering equality density | Accepted source packing, its symmetries, and the finite calibration | No avoiding pose, void cover or continuum density certificate; retain the stronger obstruction as a conditional fallback |
| BC265 / H116 | A complete depth-one expanded weighting of mass above eleven, or a useful ceiling for one genuinely changed support | Old support, baseline and exact calibration | No added pose or complete expanded-depth certificate; do not promote a calibration violation into a dual result |
| BC265 / H115 | A specified curved resource with useful capture and complete boundary-null coverage | The nondegenerate quadratic-arc boundary lemma | No candidate or uniform integral verifier; line-nullity alone is not headroom, so park |
| BC257 / H100 | Mass below eleven covering every full-size pose at a declared below-$U$ side | Weak-duality semantics and exact field/geometry foundations | No density mechanism with demonstrated prospective headroom, fixed family or continuum reader; old-support closure supplies none of these |
| BC264 / H114 | A small feature-family obstruction, or a kernel candidate with a credible complete verification cost | The finite-feature kernel formulation and existing exact geometry | Kernel-specific review, fixed features, exact PSD evidence and full diagonal/pair verification remain missing; select a bounded feasibility gate, not a hierarchy build |

The H114 mechanism can directly exclude eleven squares at its declared side $96/25$: it
requires $K-1$ positive semidefinite, diagonal at most $b<11$, and $K(p,q)\le0$ on every
distinct compatible pair, including touching pairs.
This uses explicit compatible-pair constraints.
Universal verification can be expensive: the pair domain has six continuous pose
coordinates, and its two absolute orientations permit only valid joint symmetry
reductions.

[PR110’s BC260 review](https://github.com/jlevy/squares/blob/86dbff43683739acc5e936dc299e293d13d59b8d/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-028/bc-260-direct-hybrid-contracts.md#individual-verdicts)
explicitly leaves kernels unresolved while accepting its direct case/Farkas consumers.
Do not reopen those accepted consumers or duplicate external BC261 and BC273–280. The
selected kernel subset needs its own limited review.

## One Next Discriminator, One Conditional Fallback

**Preferred: take BC264’s existing 30-minute feature and separator pricing slice in a
later allocation.** Its deliverable must be one small fixed feature family, the exact
finite necessary constraints used to test it, a solver-independent PSD/dual certificate
format, and a price for the unresolved continuum diagonal and compatible-pair domains.
Reserve an independent review within the slice.
No feature family is selected or evaluated by this note.

The first subsequent scientific discriminator, if admitted under a narrower hypothesis,
should decide whether those finite necessary constraints already force $b\ge11$. For a
fixed exact feature map $\phi$, the standard form is $K(p,q)=1+\phi(p)^TQ\phi(q)$ with
$Q\succeq0$. Fixed diagonal and compatible-pair evaluations give linear constraints on
$Q$ and $b$; a nonnegative combination of those constraints and an exact
positive-semidefinite matrix certificate can establish a finite obstruction.
The feature map must respect square reparameterization, or retain a proved complete
chart and seam convention.
An exact obstruction rejects only that feature family.
A finite $b<11$ candidate does not prove the packing bound; it earns at most a
separately priced continuum check.
An unresolved finite problem earns neither conclusion.
The required controls include exact PSD/refusal checks, legal touching pairs, joint
symmetry, and the original Trump-side no-false-$b<11$ control.
Their future scientific invocation needs its own authorization.

This recommendation is a priority judgment, not an assertion that a low-degree kernel
exists. If the 30-minute slice cannot fix the feature family and an independent exact
acceptance path, stop and retain that gap.
Do not increase degree, build a general six-dimensional separator, or fund successive
sample fits merely to continue the allocation.
No target runtime estimate is justified yet.

**Independent fallback: BC265/H101’s $\Omega$-avoiding-pose test.** Reopen it only when
one exact candidate and a bounded source-bound void-cover plan are supplied.
Allow at most a separately allocated 30-minute admission/design review before deciding
whether any implementation and target cost are worthwhile.
Require the whole closed pose, all eight source packings and every cover seam; regard a
failed sufficient cover as unresolved, not proof that every pose meets $\Omega$. Do not
substitute the weaker $F(P)<1$ test or extend the existing cover reader’s degree guard
without separately reviewed controls.

Neither H115 nor H100 supplies an independent fallback candidate at this checkpoint.
Reopen H100 for a named below-side density mechanism with a credible mass and coverage
margin, not because an endpoint obstruction failed to materialize.
If neither selected entry reaches its admission condition, defer further scientific
work. That is preferable to treating the old H099 support as an invitation to another
unpriced representation build.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
