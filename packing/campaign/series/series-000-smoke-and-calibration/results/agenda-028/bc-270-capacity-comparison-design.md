# BC-270 — Capacity Comparison Design and Exact Domain Obstruction

**Disposition: no target determination is admitted by this design.** A natural
four-square subsystem from a complete split of the eleven-square problem has an exact
feasible packing. The same obstruction survives addition of a bottom-wall anchor.
A sound resource cannot exclude either domain, and a sound geometric outer relaxation
must retain its exact packing witness.
The missing premise is a necessary restriction on the selected squares imposed by the
remaining squares.

This is mathematical design and an analytical obstruction under
[H-118](../../../../hypotheses/H-118-capacity-versus-coupled-lp.md),
[X-018](../../../../explorations/X-018-hybrid-strength-and-angular-release.md), and
[Agenda 028](../../../../agendas/agenda-028-hybrid-strength-and-angular-release.md).
It allocates no experiment, changes no hypothesis, and launches no target search.
The
[source review](../../../../../../docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md)
owns the resource and uniform-LP implications used here.

## A Natural Closed Parent Split

Fix the container $[0,q]^2$, where $q=96/25$. Every contained unit square has center
coordinates in $[1/2,q-1/2]=[1/2,167/50]$: its support half-width in either coordinate
is at least $1/2$, at every orientation.

Divide the vertical center interval into three equal closed bands:

$$
B_0=[1/2,217/150],\qquad
B_1=[217/150,359/150],\qquad
B_2=[359/150,167/50].
$$

Each has width $71/75$. Assign seam centers to the lower-index band for the counting
argument. Eleven assigned centers force at least four in one band.
For every band and every four-label subset, retain the closed branch that puts those
four centers in that band.
The branches overlap on seams and when a band contains more than four centers; this is
harmless for an exclusion cover.
Every packing has at least one represented assignment.
No sibling is discarded because another branch was selected.

The prospective local domain $D_1$ consists of four unit squares, each contained in
$[0,q]^2$, with centers in

$$
[1/2,167/50]\times B_1,
$$

and arbitrary individual actual orientations modulo $\pi/2$. Use the closed chart
$[-\pi/4,\pi/4]$, retaining its seam.
Include all six pair nonoverlap disjunctions; touching is legal.
The original eleven-square branch additionally contains the other seven squares, with
their containment and every pair separation, and places no new restrictions on them.
Passing to $D_1$ forgets those seven squares, so an exclusion of $D_1$ would exclude its
parent branch, but feasibility of $D_1$ does not prove that the parent branch extends to
eleven squares.

Keep the corresponding lower-band domain $D_0$ as the sibling; vertical reflection
transfers it to $D_2$. All label choices remain represented by relabeling the identical
four-slot domains.
This is a necessary occupancy split using the full center range, not a
pose box fitted around a desired contradiction.

## Exact Four-Square Packing

Let $h=1/\sqrt2$. A unit square at angle $\pi/4$ is the diamond

$$
Q(c)=\{(x,y): |x-c_x|+|y-c_y|\le h\}.
$$

For $k=0,1,2,3$, take

$$
c_{k,x}=\frac{18}{25}+\frac{4k}{5},\qquad
c_{k,y}=\begin{cases}8/5&k\text{ even},\\23/10&k\text{ odd},\end{cases}
\qquad \theta_k=\pi/4.
$$

All four centers lie in $D_1$'s band because

$$
\frac85-\frac{217}{150}=\frac{23}{150}>0,
\qquad
\frac{359}{150}-\frac{23}{10}=\frac7{75}>0.
$$

The first and last horizontal centers have clearance $18/25$ from the corresponding
container wall. The vertical center clearances are larger.
Containment is strict since

$$
\left(\frac{18}{25}\right)^2-h^2=\frac{23}{1250}>0.
$$

Two such diamonds have disjoint interiors whenever their centers’ $L^1$ distance is at
least $2h=\sqrt2$. Adjacent centers have distance $3/2$; centers two steps apart have
distance $8/5$; the endpoints have distance $31/10$. The two smallest satisfy

$$
(3/2)^2-2=1/4>0,\qquad (8/5)^2-2=14/25>0.
$$

Thus all six pairs are strictly separated.
These comparisons are an exact algebraic packing certificate, not a numerical solver
output.

The lower-band sibling has the same obstruction: keep the four horizontal coordinates
and alternate vertical coordinates $18/25$ and $71/50$. They belong to $B_0$, with

$$
\frac{18}{25}-\frac12=\frac{11}{50}>0,
\qquad
\frac{217}{150}-\frac{71}{50}=\frac2{75}>0.
$$

Their vertical differences remain $7/10$, so all pair certificates remain unchanged.
The smallest wall clearance remains $18/25>h$. Reflection gives the upper-band packing.
Consequently none of the three isolated four-square band domains can be excluded.

The coordinator supplied the central witness during design; this report independently
checks its six pair and containment conditions and derives the lower-band extension.
The chart seam is substantive: deleting the $\pi/4$ endpoint would erase the displayed
witness without justifying a parent cover.
Strict physical clearance also permits small perturbations into the chart interior, so
seam deletion would not repair the exclusion.

## A Bottom Anchor Alone Does Not Supply the Missing Restriction

A common downward translation of a packing gives a bottom-wall contact.
This permits a bottom anchor with arbitrary orientation and horizontal position; it does
not imply a flush, axis-aligned square.
The four central-band squares cannot themselves be a bottom anchor, since their centers
are above $217/150>h$.

The central four-square witness coexists with an axis-aligned unit square centered at
$(38/25,1/2)$. Its horizontal interval is $[51/50,101/50]$, and its upper edge is at
$y=1$. The two low diamonds have horizontal center distance $3/10$ from this interval;
their lowest ordinate over the interval is therefore at least

$$
\frac85-h+\frac3{10}=\frac{19}{10}-h>1.
$$

The two high diamonds lie wholly above $23/10-h>1$. The anchor is contained, touches the
bottom wall legally, and is disjoint from all four diamonds.
Its center is left of the container midpoint $48/25$, so a horizontal-reflection
normalization does not remove it.

Hence merely adding a freely positioned, freely oriented bottom anchor still leaves a
feasible five-square subsystem.
Excluding the eleven-square parent requires some additional consequence of its six other
squares. The fixture makes no claim that those six can be inserted.

## Finite Resources and the Exact Obstruction

For a prospective atomic comparison on $D_1$, freeze the 99-atom basis

$$
A=\left\{\left(\frac{8i}{25},\frac{8j}{25}\right):
1\le i\le11,\ 2\le j\le10\right\},\qquad
\mu_w=\sum_{a\in A}w_a\delta_a,\quad w_a\ge0.
$$

This is a finite generating family; the nonnegative weights are optimization variables,
not a claim that the cone contains finitely many measures.
Its budget is $M=\sum_a w_a$, used once for the four slots.
No additional atoms, angle-dependent measure changes, negative weights, or independent
copies of the budget belong to this family.
Use $W(Q)=\operatorname{int}Q$ or explicitly certified strict interior cores.
Atomic mass on a square boundary does not count as captured mass.

A normalized resource exclusion would require a uniform capture of at least one on every
allowed single-square pose and total mass $M<4$. More generally, four guaranteed
captures $\alpha_i$ require $\sum_i\alpha_i>M$. Both formulations are impossible here:
the four displayed squares have disjoint interiors and lie in the four slot domains, so

$$
\sum_{i=0}^3\alpha_i
\le\sum_{i=0}^3\mu_w(W(Q_i))\le M.
$$

The four exact poses, each with dual weight one, are also a finite-family obstruction:
every atom is counted in at most one strict interior, while the dual objective is four.
No atom-incidence enumeration or optimization is needed to establish that upper bound on
the resource’s possible exclusion strength.
The argument holds for every nonnegative measure with the stated disjoint-witness
semantics, not just these 99 generators.
Likewise, a sound subset capacity for this domain must be at least four.
The five-square anchored fixture gives the corresponding bound of at least five on that
enlarged domain.

## Strong Geometric Comparator and Acceptance Boundary

The matching geometric arm uses precisely the same closed domain, labels, actual angle
variables, walls, and common parameters.
Order the four centers horizontally by label, which is valid because the slots have
identical domains. Keep the complete weak-order seams.
For each of the six pairs retain all eight directed SAT alternatives until an
alternative is selected, and include all sixteen corner-pair inequalities of each
selected alternative.
Include every physical wall inequality and every center bound.
Projection and ordering contractions may strengthen the system only with sound
whole-domain implications.
Any certified core or incircle deduction applies to both arms.
No asymmetric angle, center, or SAT subdivision is allowed.

At the exact witness angle $\pi/4$, choose a separating axis for each pair from the sign
of its displacement.
If $i<j$, their horizontal displacement is positive.
Choose the normal $(1,1)/\sqrt2$ when $c_{j,y}-c_{i,y}\ge0$, and $(1,-1)/\sqrt2$
otherwise. In both cases the directed projection gap is their $L^1$ distance divided by
$\sqrt2$, strictly larger than the required unit support sum.
These are actual edge normals of the squares.
Thus the displayed centers, already horizontally ordered, give a feasible point of the
complete exact fixed-angle translation LP over $\mathbb Q(\sqrt2)$.

Every sound same-domain uniform outer LP must retain this point in a represented angle
and SAT branch. Adding further sound projection or coupled geometric deductions cannot
change that fact. A fully enumerated SAT comparator also retains at least this branch.
This is stronger than showing survival in one deliberately weak envelope: the actual
packing obstructs the exclusion under any sound comparator.
No numerical outer-row matrix or target experiment is frozen after this obstruction, and
BC-261 instrument readiness is not inferred from the algebraic argument.

For any later, differently constrained target, H-118’s acceptance still requires both:

1. An independently checked uniform resource exclusion on its entire frozen closed
   domain, with exact strict margin, all boundary strata, and every common budget.
2. An exact feasible point of the strongest declared coupled outer LP on the identical
   domain and branch policy, checked against its complete reconstructed row list.
   Solver status, failure to find a Farkas certificate, or feasibility of a weaker arm
   does not meet this requirement.

If the complete geometric comparator also excludes that future domain, classify any
resource benefit as a proof-cost result.
At fixed exact angles with all alternatives selected, the LP is exact and strength
separation is impossible.
A verified packing refutes the domain exclusion; a finite-family dual rejects only that
family unless its argument applies more broadly, as it does here.
Timeout or failed certificate search leaves a claim unresolved.

## Controls and Next Proof Obligation

| Control | Exact expected behavior |
| --- | --- |
| The four-diamond central and outer-band fixtures | All sound exclusion arms retain them; capacity below four is refused |
| The central diamonds with the bottom anchor | All five-square exclusion arms retain them |
| Three axis squares at $(1/2,48/25),(48/25,48/25),(167/50,48/25)$ | Feasible contained three-square control in $D_1$ |
| The source four-slot band at side $3.9$ with its three atoms | Resource contradiction is valid; ordering also excludes it, so no strength verdict |
| Count an atom on a boundary as strictly captured, reuse the same budget twice, or delete a chart seam | Independent resource/domain reader refuses the certificate |
| Omit a wall, a selected corner row, or a SAT sibling | Independent geometry/cover reader refuses completeness, even when a supplied dual still cancels |
| Widen a certified pose domain without rechecking capture or coefficient errors | Reader refuses reuse |

**Selected next proof:** in one further 30-minute BC-270 design slice, derive one closed
compatibility restriction on a four-square band group that is necessary in its
*eleven-square* parent and excludes the explicit four- and five-square fixtures for a
proved reason. The restriction must come from retained residual squares or accepted
forcing, with every count, anchor-feature, and localization sibling preserved.
A fitted angle cap or chosen anchor box does not meet this obligation by itself.

Price that slice as 10 minutes to bind one existing accepted forcing/anchor premise, 15
minutes to derive its exact closed residual and test the fixtures analytically, and 5
minutes for a proof-obligation handoff.
Separately reserve a 15-minute independent mathematical replay before accepting the
restriction. These are prospective attention allocations, not measured solver runtimes.
The current result justifies no capacity search or large enumeration.
If no such premise is available, return the missing localization obligation to BC-262’s
parent-cover owner and keep BC-271 blocked.

BC-261 should receive a concrete descriptor only after this dependency is met.
Its needed interface remains arbitrary closed pose domains, shared actual-angle
parameters, complete selected SAT corner rows, exact outer-LP feasibility witnesses, and
a separate whole-domain resource reader.
This report creates no duplicate exporter.

## Timing and Checks

Design started at 06:39:29 UTC on 2026-09-07, with a delivery deadline of 06:51:12 UTC.
The work comprised source review, the necessary band split, independent symbolic
verification of the supplied feasible witness, and the anchored/sibling extensions.
No target search, benchmark, dependency change, registry mutation, or Git mutation ran.

Design and document checks completed at 06:50:18 UTC, 10 minutes 49 seconds after the
recorded start. Installed Flowmark 0.4.0 formatted this report and its check passed; all
four relative links resolve, the single terminal native footer check passed, and
`git diff --check` reported no whitespace error.
The initial formatter invocation could not persist its outside-workspace incremental
cache; rerunning with `--no-cache` completed without changing cache permissions.
The common-document and prose-editing guidelines were applied to this report.
The only assigned durable write is this report.
Parent integration owns campaign validation and independent mathematical acceptance.
The four-square subsystem feasibility and its measure obstruction are established by the
explicit derivation above; a useful restricted eleven-square target and the geometric
premise needed to obtain it remain open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
