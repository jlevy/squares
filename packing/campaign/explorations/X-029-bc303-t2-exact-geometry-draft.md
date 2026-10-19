---
title: "X-029 — BC303 T2 Exact Geometry and Open Threshold Tests"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-029
  title: BC303 T2 Exact Geometry and Open Threshold Tests
  date: '2026-09-13'
  author: Codex (mathematical analysis with independent review under think-8057)
  campaign: packing.squares
  brief: >-
    Retain the reviewed exact co-owner reduction, split-owner feasibility
    control, and next threshold tests for BC303 T2 without computing charges,
    deciding T2, resolving global routing, or changing the n11 bound.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-293-measure-free-96-25.json
  - packing/cases/n11_five_dot_cover/wall-containment-contract.md
  - packing/devtools/owner_footprints.py
  - packing/src/sqpack/fractional/adaptive.py
  - docs/project/research/research-2026-09-12-n11-selection-routing-first-principles.md
  - docs/project/reviews/review-2026-09-13-bc303-t2-geometry.md
  proposes: []
---
# BC303 T2: Exact Geometry and the Next Determinations

Date: 2026-09-13. This X-029 draft retains the bounded W3 mathematical analysis and the
independent W2 review.
The source analysis was read-only; this artifact adds only the reviewed geometry and
replay controls. The coordinator owns `think-cexv`, `think-5zkv`, and `think-d6ls`.

**T2 remains undecided.** This analysis derives a smaller complete co-owner geometry
test and supplies a rational split-owner feasibility control.
It evaluates no BC303 charge, runs no surplus minimization, and makes no packing-bound
or routing claim. An
[independent mathematical review](../../../docs/project/reviews/review-2026-09-13-bc303-t2-geometry.md)
accepted the C and S geometry after correcting the C rational-witness statement below.
The proposed readers are not implemented or admitted here.

The working plan is the
[daytime strategy plan](../../../docs/project/specs/archive/plan-2026-09-10-n11-daytime-strategy-and-explainer.md),
with agenda 035. That plan explicitly leaves the owner-requested V3 source unresolved
under `think-i1fr`; this analysis does not claim V3 alignment.
That missing planning source does not prevent the following deductions from the frozen
BC303 contract.

## Inputs and Evidence Status

The mathematical inputs are the frozen source revision
`39714308ce2081abbd76624387d134fee4be6deb` identified in the reviewed preregistration
under `think-8v6c`. The source-distinct review under that bead accepts the literal T1
arithmetic, complete labels, opposite-parent separation, combined T2 equivalence, and
single-parent projection.
The underlying
[BC303 report](../series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md)
and its
[377-site measure](../series/series-000-smoke-and-calibration/results/agenda-030/bc-293-measure-free-96-25.json)
are retained in the campaign.

The read-only T1 reader review under `think-3jsz` accepts the disclosed nineteen-atom
calculation but refuses instrument admission at its reviewed commit because retained
atom rows are not authenticated against source atoms and the executing reader revision
is misidentified in cross-checkout execution.
Those tool defects do not alter the accepted arithmetic.
Repair and independent readmission remain coordinator work.

This note imports BC303’s complete coverage floor rather than rerunning that coverage.
The
[maintained exact control](../../cases/n11_five_dot_cover/bc303_t2_geometry_control.py)
checks rational geometry, constants, source-chart combinatorics, and the split fixture.
Its [focused test](../../tests/test_bc303_t2_geometry_control.py) replays these checks.
Neither reads the atom file or evaluates charge; they are geometry controls, not a
source-bound instrument or campaign determination.

## Exact T2 Obligations

Use the closed, D4-invariant equipment domain from the reviewed proposal.
Write

$$
q=\frac{96}{25},\quad h=\frac{9977}{20000},\quad
a=\frac{3152}{3175},\quad b=\frac{2336}{3175},\quad
\delta=a-b=\frac{816}{3175}.
$$

The BL marks are $m_1=(a,b)$ and $m_2=(b,a)$. The other corners use the specified maps
$I,H,V,HV$. Every unit parent and its selected core have one common centre:

$$
Q_i=z_i+[-1/2,1/2]u_i+[-1/2,1/2]Ju_i,
\qquad C_i=z_i+[-h,h]r_i+[-h,h]Jr_i.
$$

The physical angle of $u_i$ ranges over the entire admitted source cell of $r_i$. All
displayed parents must have one simultaneous realization inside the container with
disjoint interiors; parent boundary contact is allowed.
The strict snapping inequality puts each closed core in its parent’s interior, so
different displayed cores are disjoint, including their boundaries.
Ownership and atomic charge use closed core membership.

Let $A_c$ be the union of the complete signed-frame label sets supplied by the actual
local owners.
Forced 0 means $A_c\cap\lbrace0,15\rbrace=\lbrace0\rbrace$; forced 15 means
that intersection is $\lbrace15\rbrace$. Other labels remain allowed.
At a forced-0 corner the roles are C, S, O1; at a forced-15 corner they are C, S, O2. C
has one core owning both marks, S has distinct owners of the two marks, and O1/O2 has
one owner and one locally missing mark.
A co-owner is charged once.

For every ordered adjacent or opposite corner pair, T2 asks for the following universal
inequalities over its jointly realizable domain:

| Ordered roles | Distinct owners $k$ | Missing marks $u$ | Required surplus |
| --- | ---: | ---: | --- |
| C,C | 2 | 0 | $S>\varepsilon$ |
| C,S or S,C | 3 | 0 | $S>\varepsilon$ |
| S,S | 4 | 0 | $S>\varepsilon$ |
| O1,C or C,O2 | 2 | 1 | $S>\varepsilon-w$ |
| O1,S or S,O2 | 3 | 1 | $S>\varepsilon-w$ |

Here

$$
S=\sum_{i=1}^{k}(\mu(C_i)-1),\quad
\varepsilon=\frac{524199}{2000000},\quad
w=\frac{106251}{800000},\quad g=\frac3{800000}.
$$

The two-missing pair O1,O2 is excluded by the seven-of-eight ownership premise.
Cross-corner mark distances preclude sharing a core between different corners.
For a hypothetical packing the common resource identity is

$$
U_\mu+\sum_{i=1}^{11}(\mu(C_i)-1)=\varepsilon,
\qquad U_\mu\ge u_{\rm total}w,
\qquad\mu(C_i)-1\ge g>0.
$$

Thus each displayed strict inequality contradicts such a packing’s resource account.
An O role is applied using the packing’s actual global incidence; the local test itself
does not assert that its missing mark remains unowned after adding arbitrary parents.

Conversely, a local violating configuration need not extend to eleven parents.
Indeed, a packing extension would have to satisfy the stronger necessary inequality
$S\le\varepsilon-uw-(11-k)g$. That extra resource fact does not change the original T2
test or its verdict threshold.

For opposite corners put $s=a+b$ and $f(x,y)=x+y$. Every unit square has full $f$-width

$$
|c+d|+|c-d|=2\max(|c|,|d|)\le2.
$$

A BL-mark parent lies below $f=s+2$; a TR-mark parent lies above $f=2q-s-2$. Their gap
is

$$
2q-2s-4=\frac{708}{3175}>0.
$$

Consequently each opposite-corner role pair is exactly the product of its two local
domains. The aggregate is the union of the eight admitted products, with O1,O2 omitted.
Adjacent parents have no such automatic separation; their cross-corner compatibility
must be retained in an adjacent-only test.

Let

$$
A=\min\lbrace S(X):X\in\mathcal D^0_{{\rm BL},C}\cup
\mathcal D^0_{{\rm BL},S}\rbrace.
$$

The domain is nonempty, and finite atomic charges give an attained minimum even on a
nonclosed centre domain.
Whole-configuration diagonal reflection exchanges forced 0 and forced 15 and preserves
mass, C/S incidence, and the closed equipment domain.
If $A>\varepsilon/2$, full/full pairs exceed $\varepsilon$, while one-missing pairs
exceed $\varepsilon-w$ because $2w>\varepsilon$. If $A\le\varepsilon/2$, its attaining
configuration and the opposite-corner transport of its diagonal reflection coexist and
have total surplus $2A\le\varepsilon$. Therefore

$$
(\text{all adjacent and all opposite T2 inequalities})
\quad\Longleftrightarrow\quad A>\varepsilon/2.
$$

With $W=4000000$, the two remaining queries are exactly

$$
\begin{array}{ll}
\mathrm C:& W\mu(C)\le4524199,\cr
\mathrm S:& W(\mu(C_1)+\mu(C_2))\le8524199.
\end{array}
$$

A witness to either rejects opposite T2 and hence the combined helper.
Acceptance requires both complete domains to have integer surplus at least $524200$, or
to be empty. Equality at $524199$ rejects the strict inequality.
An opposite rejection alone does not decide adjacent-only T2.

## A Smaller Exact Co-Owner Domain

This reduction specializes the reviewed generic event-stratum proposal to role C.

Each selected square has four possible first rays of a proper signed frame.
To supply label 0, at least one ray must lie in the closed angular bin $[0,\pi/4]$.
There is exactly one such ray whenever one exists in this source family.
Call it $r=(c,s)$ and use it as the ordered core frame, regardless of the raw source’s
quarter-turn representative.

No rational source ray is exactly diagonal.
The source parameters satisfy

$$
t_{179}^2+2t_{179}-1<0,
\qquad t_{180}^2+2t_{180}-1=\frac{309449}{250000000000}>0.
$$

Thus the bin-0 source manifest consists of both axis aliases, unreflected indices 1
through 179, and reflected index 180: **182 source charts and 181 distinct selected
orientations**. The other 180 charts cannot supply label 0 and have empty forced-0 C
domains. The maintained control reconstructs this list using all four signed rays and
closed bin tests.

For every non-axis eligible ray, $0<s<c$. Its four rays fall strictly in bins 0, 2, 4,
and 6, so none lies in bin 7. Consequently this core cannot supply label 15, for any
centre or mark placement.
The absence predicate is automatic for these C charts.
This argument uses the actual selected rays; replacing the last source by a diagonal
would invalidate it.

Write the centre in mark-relative core coordinates:

$$
z=m_1+xr+yJr.
$$

Label 0 is equivalent to $0\le x,y\le h$. The displacement $m_2-m_1=(-\delta,\delta)$
has core coordinates $(-\delta(c-s),\delta(c+s))$. The exact inequalities

$$
h^2-2\delta^2=\frac{753193512241}{6451600000000}>0,
\qquad h-\delta=\frac{614279}{2540000}>0
$$

give $0<\delta(c+s)<h$ and $h-\delta(c-s)>0$. The second mark’s perpendicular-coordinate
containment then holds throughout $0\le y\le h$; its other coordinate requires
$x+\delta(c-s)\le h$. Hence the exact non-axis C centre rectangle before parent
containment is

$$
\boxed{0\le x\le X_r:=h-\delta(c-s),\qquad0\le y\le h.}
$$

All its points own both marks, supply 0, and fail to supply 15. Every non-axis forced-0
co-owner lies in this rectangle.

The axis ray is the necessary exception.
East lies in both closed bins 0 and 7, so the second mark supplies label 15 exactly when
$y\ge\delta$ inside the co-owner rectangle.
Both axis source aliases therefore have the exact half-open domain

$$
\boxed{0\le x\le h-\delta,\qquad0\le y<\delta.}
$$

In physical BL coordinates this is $a\le z_x\le b+h$ and $b\le z_y<a$. The excluded edge
$y=\delta$ must stay excluded, including its vertices.

### Only the near left wall remains

For a source chart whose folded lower whole-angle tangent is $L_j$, the minimum unit
parent coordinate half-extent is

$$
e_j=\frac{1+L_j}{2\sqrt{1+L_j^2}}\le\frac1{\sqrt2}.
$$

For closed source cells it is attained at that lower endpoint.
In either C rectangle, $z_y=b+sx+cy\ge b$, and

$$
2b^2-1=\frac{833167}{10080625}>0.
$$

The bottom wall therefore imposes no further condition.
Both centre coordinates are less than $1+h\sqrt2<2$, whereas $q-e_j\ge q-1/\sqrt2>2$.
The far right and top walls impose no condition either.
The complete non-axis parent-existence predicate is consequently

$$
\boxed{a+cx-sy\ge e_j.}
$$

Necessity is parent containment.
For sufficiency choose the lower-endpoint parent at the same centre and transport its
source reflection and quarter turn correctly; its selected core is strictly inside it by
the snapping theorem.
The axis rectangles already satisfy all parent walls with $e_0=1/2$.

This is a single-parent result.
It makes no assertion that two independently chosen endpoint parents coexist.

### Exact event-stratum feasibility without an LP

For each source chart, use the Cartesian products of rational event points and open
intervals inside its C rectangle.
For each atom $p$, its membership boundaries are $(p-m_1)\cdot r\pm h$ and
$(p-m_1)\cdot Jr\pm h$. Include rectangle bounds and mark sign boundaries as well.
For non-axis C, the additional interior sign level $y=\delta(c+s)$ makes the complete
label set constant, including the second mark’s zero-coordinate case.
Axis C retains its strict upper boundary.

Atomic charge and complete labels are constant on every such product stratum
$\sigma=I_x\times I_y$. Parent feasibility need not be constant there: the admissible
portion is its intersection with the left-wall half-plane.
Only that intersection’s nonemptiness is needed to decide whether its charge is
attainable.

For a non-axis chart let

$$
\alpha=\sup I_x,\quad\beta=\inf I_y,\quad
M_\sigma=a+c\alpha-s\beta.
$$

The coefficients $c,s$ are strictly positive, so this is the maximum distance from the
near left wall on the stratum’s closure.
Every such value is positive because $M_\sigma\ge a-hs>a-h>0$. Its exact relation to
$e_j$ is the sign of the rational quantity

$$
\boxed{4M_\sigma^2(1+L_j^2)-(1+L_j)^2.}
$$

For a closed source cell:

- A positive sign gives a feasible centre in the stratum, by approaching the maximizing
  corner from within it.
- A negative sign proves its parent intersection empty.
- At zero, feasibility requires both $\alpha\in I_x$ and $\beta\in I_y$. Since the
  strata use singletons and open intervals, only the maximizing vertex can pass this
  equality case.

The result is complete for these two-dimensional event strata, their edges, and their
vertices. No open-cell perturbation is used to discard a conditioned boundary.
If an endpoint is excluded by a separately frozen source policy, parent feasibility is
strict at $e_j$ when the minimum extent is unattained; then only a positive comparison
passes. If only the upper endpoint is excluded, an admitted lower endpoint still gives
the weak comparison.
Empty or absent source charts must be handled as such.

An admitted reader could enumerate the entire rational product arrangement and apply
this comparison only to strata whose integer mass is at most $4524199$. A complete
absence proof then determines C above its threshold.
A feasible stratum supplies an exact centre and a matching parent for witness replay.
Every feasible C stratum admits a rational centre and a rational parent ray.
Positive clearance permits rational approximations inside the stratum and source cell.
At equality, $M_\sigma=e_j$ is rational, and the endpoint parent ray has rational
components $2M_\sigma/(1+L_j)$ and $2M_\sigma L_j/(1+L_j)$. The exact quadratic
comparison still decides whether a stratum is empty; finding rational witnesses alone
cannot prove absence.

This is a proposed maintained reader, not an evaluated runtime claim.
The source manifest, full atom scan, stratum coverage, endpoint decisions, and executing
implementation identity still need the authenticated receipt contracts and independent
controls required by the T1 review.
There is no general LP or real-algebraic decomposition dependency for this C geometry
oracle.

### Symmetry and policy scope

The derivation is in the declared BL chart.
Global D4 maps transport whole parents, cores, source aliases, marks, and proper signed
frames. Under a reflection the proper frame uses $e'=L(Je)$ and $Je'=L(e)$. Diagonal
reflection exchanges labels $m_a:j$ and $m_{3-a}:(7-j)\bmod8$, sending this forced-0 C
domain to its forced-15 counterpart.
Corner charts must be pulled back before applying the displayed rectangle formulas.

Both closed axis aliases, all source seams, and the two distinct near-diagonal selected
orientations are retained.
A deterministic tie selector can change endpoint admission or break the required domain
symmetry; the closed-domain T2 equivalence must not be silently transferred to that
policy. The single-parent formulas can be adapted using the attained/unattained endpoint
rule above after that policy has been specified.

## Split Owners: One Exact Strip and a Rational Feasibility Control

In S, owner 1 supplies label 0 because it alone owns $m_1$. It must therefore use one of
the same 182 bin-0 source charts.
The calculation above also gives its exact core-centre condition for owning $m_1$ but
not $m_2$:

$$
\boxed{h-\delta(c-s)<x\le h,\qquad0\le y\le h.}
$$

This includes the axis ray $c=1,s=0$. Exclusion of the second mark is strict.
Owner 1 cannot supply label 15 because it does not own $m_2$. Moreover

$$
z_x>a+(c-s)(h-\delta c)>a,
\qquad z_y\ge b>1/\sqrt2.
$$

Both coordinates are less than 2. Thus every unit-parent angle at this first centre is
individually contained in the container; the matching source-angle condition still
applies. This removes its wall-containment constraints, while the second owner’s wall
conditions and absence-of-15 predicate remain.
Its strict strip is a geometric reduction, not a split-surplus lower bound.

A fully rational S configuration shows that the split domain is nonempty.
Use

$$
z_1=(149/100,737/1000),\quad r_1=u_1=(1,0),
$$

$$
z_2=(71/100,5/3),\quad
r_2=\left(\frac{207106690551}{292893309449},
           \frac{207107000000}{292893309449}\right),\quad
u_2=\left(\frac{207151}{292849},\frac{207000}{292849}\right).
$$

Each displayed rational ray is a unit ray obtained from $((1-t^2)/(1+t^2),2t/(1+t^2))$.
The second selected ray is unreflected source index 180. Its parent has half-angle
tangent $207/500$ and whole-angle tangent $207000/207151$, strictly inside that source
cell:

$$
\frac{207000}{207151}-L_{180}
=\frac{24689427804703000}{7731309841725105979}>0,
\qquad1-\frac{207000}{207151}=\frac{151}{207151}>0.
$$

It consequently avoids both nearest-cell and fold-endpoint tie questions.
The following exact quantities verify the geometry; the exact control checks
polygon-edge incidence for both marks in both cores.

| Obligation | Exact verification |
| --- | --- |
| First core owns $m_1$ strictly | Core-coordinate slacks $4079/2540000$ and $1263899/2540000$ |
| First core excludes $m_2$ | One slack is $-648721/2540000$ |
| Second core owns $m_2$ strictly | Slacks $90455351216094613/2231847018001380000$ and $3062738070831071/743949006000460000$ |
| Second core excludes $m_1$ | One slack is $-267335959120861729/743949006000460000$ |
| First parent contained | Minimum wall clearance beyond half-extent is $237/1000$ |
| Second parent contained | Half-extent $414151/585698$; minimum wall slack $84729/29284900$ |
| First core strictly in parent | $1-2h=23/10000>0$ |
| Second core strictly in parent | $1-2h(u_2\cdot r_2+\lvert\det(u_2,r_2)\rvert)=1660196533717283623/857735127788302010000>0$ |
| Complete first-core labels | $\lbrace0,7\rbrace$ |
| Complete second-core labels | $\lbrace9\rbrace$ |

For $f(x,y)=y-x$, the first parent’s maximum is $247/1000$. The second parent’s centre
has $f=287/300$, and its half-width is $\max(u_{2x},u_{2y})=207151/292849$. The parents
therefore have strict separation

$$
\min f(Q_2)-\max f(Q_1)
=\frac{287}{300}-\frac{207151}{292849}-\frac{247}{1000}
=\frac{2022521}{878547000}>0.
$$

The full corner availability is $\lbrace0,7,9\rbrace$, so the relevant set is exactly
$\lbrace0\rbrace$. Each core owns one mark and their actual parents coexist with strict
geometric clearance.
The first parent uses the admitted physical axis endpoint; the second parent angle lies
strictly inside its source cell.
**The two core masses have not been evaluated.** This is a positive feasibility control
and a disclosed candidate for a later authorized charge check, not a surplus
counterexample.

A complementary exact negative control is available: if both parents are axis aligned
and use their axis selected cores, ownership of either BL mark puts both centre
coordinates in $[1/2,a+h]$. Since $a+h-1/2<1$, two such unit parents necessarily overlap
in both coordinate projections.
They cannot realize S. This excludes only that physical-angle pair, not all pairs of
axis source charts with nonzero physical angles.

## Complete S Methods and the Remaining Gaps

The first-owner strip can reduce the S product arrangement, but a split decision still
requires two centres and two shared continuous parent angles.
The second owner’s exact label absence and mark exclusion use strict Boolean branches.
All boundary strata and zeros remain part of the domain.
Individual parent projections or separately feasible pair constraints do not establish
one joint realization.

The reviewed half-angle formulation gives an exact fallback: rational polynomial source
constraints, containment, and the complete separating-axis disjunction for the two unit
parents, after clearing only positive denominators.
The first owner’s wall constraints can now be removed by the proved strip bound.
Within-corner parent coexistence remains an obligation over the two angle parameters.

A complete necessary relaxation can decide S positively if it contains every actual
split pair and excludes every pair at or below $8524199$ total integer mass.
For example, enforce the exact mark/label strata and individual projections, then use
proved necessary separation conditions on the selected cores or parent incircles.
A surviving relaxed pair requires actual parent replay before it can reject T2. The
rational control above is useful precisely because it supplies simultaneous parents.

If these relaxations do not decide S, an independently replayable semialgebraic or
outward-rounded complete cover method is still needed.
Unexplained solver infeasibility, omitted determinant-zero cases, incomplete interval
boxes, and coverage by volume alone cannot discharge that obligation.
No such general S reader is admitted by this note.

## Proof and Test Priorities

1. **Maintained C reader and controls.** Authenticate the frozen measure and executing
   implementation, retain source aliases, construct all rational event strata, and prove
   each threshold-relevant parent intersection feasible or empty with the single
   quadratic comparison.
   Include edge, vertex, zero-sign, wrong-source, and excluded-endpoint controls before
   a registered scientific determination.
2. **Small disclosed witness checks after admission.** The existing forced-0 C control
   at $(6/5,9/10)$ and the rational S control above have exact geometry.
   A maintained source scan can determine their charges directly.
   Neither is a new target-blind candidate, and neither has an asserted probability of
   beating the threshold.
   A charge above threshold leaves the rest of its domain unresolved.
3. **Complete threshold determination.** C can be completed with the reduced event
   method; S may be decided by an exact witness or a complete necessary relaxation, or
   require the general joint-parent method.
   A valid witness in either role rejects opposite T2; accepting the combined helper
   needs both roles complete.
4. **Separate global obligations.** T2 success would exclude forced-type conflicts in a
   hypothetical packing, but T1 local availability remains unproved on actual
   eleven-parent packings and global owner routing still needs its stated selection
   theorem. T2 failure would refute only the specified local surplus helper.

The independent mathematical review accepts the C and S geometry after correcting the
rational-witness statement.
Its
[disposition and limits](../../../docs/project/reviews/review-2026-09-13-bc303-t2-geometry.md)
are retained separately.
Instrument admission and source authentication remain open.
The C reader proposal has a complete mathematical decision rule but no implementation or
measured cost here. The scientific outcomes for C, S, adjacent-only T2, and opposite T2
remain uncomputed. No evidence in this note supports choosing a surplus outcome in
advance or changing the current n11 bound.

Reproduce the maintained geometry control from `packing/`:

```bash
uv run --frozen --all-extras --group dev pytest -q tests/test_bc303_t2_geometry_control.py
```

A C charge reader still needs complete source atoms, their integer weights, the source
manifest, and an authenticated executing implementation before a target run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
