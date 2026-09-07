# BC-279: Maximal Wall-Core Protocol

**Status: prospective; the scientific target is unattempted.** BC279, under existing
H118 and bead `think-cwve`, asks whether the maximal wall-conditioned common cores admit
at most six residual bodies throughout the entire unchanged four-pose domain $\Gamma_0$.
This document fixes one model and its acceptance rules.
Independent admissions, passing record checks, a committed protocol and separately
recorded actual leases are required before target dispatch.

The model is the exact convex hull/intersection selected in the native
[midpoint allocation](midpoint-allocation.md).
Its definition and generic proof are self-contained below.
It retains the complete domain from [BC277](bc-277-boundary-band-domain-design.md) and
its [accepted admission](bc-277-boundary-band-domain-review.md).
The [BC278 independent audit](bc-278-boundary-band-independent-review.md) accepted exact
obstructions to the weaker disk and octagon bounds of six; neither excluded nor
populated the full-square child $D_0$. No retry of those weaker questions is admitted.

## Complete Parent and Selected Domain

Fix

$$
q=96/25,\qquad b=1/2,\qquad d=167/50,
$$

$$
B_0=[1/2,217/150],\quad B_1=[217/150,359/150],\quad
B_2=[359/150,167/50].
$$

A contained unit square has center in $[b,d]^2$. For counting, assign a band seam to its
lower-index band. Eleven assigned centers force four in one band.
Retain every four-label subset $I$ and every weak horizontal ordering $\pi$ of its four
slots. The closed parent $P_{j,I,\pi}$ consists of eleven contained, interior-disjoint
actual unit squares, with the chosen centers in $B_j$ in that order.
Counting ownership does not delete points from the overlapping closed parents.

For an actual square use its complete independent angle chart $\theta\in[-\pi/4,\pi/4]$
modulo quarter turns, including both endpoint lifts, and write

$$
e_i=(c_i,s_i),\quad f_i=(-s_i,c_i),\quad
c_i^2+s_i^2=1,\quad c_i\ge0,\quad -c_i\le s_i\le c_i,
$$

$$
Q_i=\{\alpha e_i+\beta f_i:|\alpha|,|\beta|\le1/2\},\quad
H_i(n)=\tfrac12(|n\cdot e_i|+|n\cdot f_i|),\quad
h_i=(c_i+|s_i|)/2.
$$

Containment is $h_i\le C_{i,x},C_{i,y}\le q-h_i$. For every pair of actual squares, the
complete weak SAT condition is

$$
\bigvee_{n\in\{e_i,f_i,e_j,f_j\},\ \sigma\in\{-1,1\}}
\sigma(C_j-C_i)\cdot n\ge H_i(n)+H_j(n).
\tag{1}
$$

The full parent retains all 55 such clauses.
No contact graph, anchor, common angle, chosen separating direction or stationarity
condition is imposed.

For the selected four slots $i=0,1,2,3$, define $\Gamma_0$ by their actual containment,
all six clauses (1), $y_i\in B_0$, $x_0\le x_1\le x_2\le x_3$, and the following exact
pose-derived quantities and eight guards:

$$
m_i=\frac1{2c_i},\quad m=\min_i m_i,\quad
\ell=(y_0+y_2)/2,\quad u=(y_1+y_3)/2,
$$

$$
\varepsilon=\tfrac12\max(|y_0-y_2|,|y_1-y_3|),\quad
k=299/1000,\quad A=m+2/5-\varepsilon,\quad\Delta=u-\ell,
$$

$$
\Delta\ge0,\quad A-k-\Delta\ge0,\quad b-u+A\ge0,\quad
b+k-x_0\ge0,\quad x_3-d+k\ge0,
$$

$$
2k+\Delta-x_{i+1}+x_i\ge0\qquad(i=0,1,2).
\tag{2}
$$

The chart has $c_i\ge|s_i|$, so this $m_i$ is exactly BC277’s reciprocal twice-maximum
coordinate core radius.
Neither it, its minimum nor the scatter is a free favorable bound.
The eight conditions are the original geometric guards, with no new capacity, area,
diameter or pose-box premise.

Let $D_0=P_{0,I,\pi}\cap\{G\in\Gamma_0\}$, still with all eleven actual squares and all
55 clauses (1). It is a distinct full-square question.
BC279 introduces a necessary relaxation of its 28 cross and 21 residual clauses; it does
not redefine $D_0$ as a core configuration.

## The Maximal Wall-Conditioned Common Core

For any possible residual center $P=(X,Y)\in[b,d]^2$, put

$$
r(P)=\min(X,Y,q-X,q-Y),\quad
t(P)=\min(r(P),1/\sqrt2),\quad a(P)=\frac1{4t(P)}.
$$

Let $B$ be the closed radius-$1/2$ disk centered at zero.
Define

$$
K(r)=\operatorname{conv}\bigl(B\cup[-a,a]^2\bigr).
\tag{3}
$$

This is exactly the intersection of the centered actual unit squares admissible at that
center:

$$
K(r)=\bigcap_{h(\theta)\le r}Q_\theta.
\tag{4}
$$

Here is a generic proof, not a capacity argument.
Containment gives $1/2\le h(\theta)\le t$. The axis square of halfside $a$ has support
$a(|\cos\theta|+|\sin\theta|)=2ah(\theta)\le1/2$ on either actual square normal, so it
and the incircle lie in every admissible square.
Convexity proves one inclusion in (4). Also $a\le r$, so these translated common cores
are contained in the container at every allowed center.

Choose $\alpha\in[0,\pi/4]$ with $\cos\alpha+\sin\alpha=2t$, and write $c=\cos\alpha$,
$s=\sin\alpha$. The admissible normals are four closed arcs of half-width $\alpha$
around the coordinate axes.
In a first-quadrant gap their two endpoint normals are $n_1=(c,s)$ and $n_2=(s,c)$.
Their supporting lines at height $1/2$ meet at $(a,a)$, since $a(c+s)=1/2$.

For a unit normal in an admissible arc, the support of the hull (3) is $1/2$, so its
inequality is among those defining the intersection.
In the gap, write $n=\lambda n_1+\mu n_2$ with $\lambda,\mu\ge0$. The two endpoint
inequalities imply $n\cdot z\le(\lambda+\mu)/2=a(n_x+n_y)$, which is exactly the hull
support there. Reflection and quarter-turn symmetry cover all directions.
The intersection thus satisfies every hull support inequality, proving the converse
inclusion.
At $\alpha=0$, the body is the axis square; at $\alpha=\pi/4$, it is the disk,
so no degenerate normal decomposition is needed at the endpoints.

The support function for every $n$ is consequently

$$
h_K(n)=\max\bigl(\|n\|/2,\ a(|n_x|+|n_y|)\bigr).
\tag{5}
$$

At $r=1/2$ the core equals the full axis unit square.
At $r\ge1/\sqrt2$ it equals the incircle.
In that regime the additional axis-core support threshold is redundant; the disk pair
conditions and every selected-square/disk cross condition still remain.
This is the strongest individual common core using only a center and container
containment. It does not retain a common actual residual orientation across different
pairs, nor use other squares to restrict such orientations.

## Exact Seven-Core Model

Range over the entire $G\in\Gamma_0$ and seven independent variable residual centers
$P_j\in[b,d]^2$, $j=0,\ldots,6$. The indices $j$ here label residual bodies and are
separate from the four selected slots.
Compute each exact $r_j,a_j$ and let $K_j=K(r_j)$. These residual common cores are
distinct from BC277’s selected-pose guard octagons, which only supply the unchanged
source guards (2). Impose exactly the following separation predicates in addition to the
source domain. All normal variables are independent between pairs.

For each of the 21 pairs $j<k$, there exists a **single** unit normal
$n_{jk}\in\mathbb R^2$. Put $L_{jk}=|n_{jk,x}|+|n_{jk,y}|$ and require, on that same
normal, all four inequalities

$$
\begin{aligned}
n_{jk}\cdot(P_k-P_j)&\ge1,\\
n_{jk}\cdot(P_k-P_j)&\ge1/2+a_jL_{jk},\\
n_{jk}\cdot(P_k-P_j)&\ge1/2+a_kL_{jk},\\
n_{jk}\cdot(P_k-P_j)&\ge(a_j+a_k)L_{jk},
\end{aligned}
\qquad \|n_{jk}\|^2=1.
\tag{6}
$$

For each of the 28 pairs of selected slot $i$ and residual center $j$, there exists a
**single** unit normal $v_{ij}\in\mathbb R^2$. Put $M_{ij}=|v_{ij,x}|+|v_{ij,y}|$ and
require both

$$
\begin{aligned}
v_{ij}\cdot(P_j-C_i)&\ge H_i(v_{ij})+1/2,\\
v_{ij}\cdot(P_j-C_i)&\ge H_i(v_{ij})+a_jM_{ij},
\end{aligned}
\qquad \|v_{ij}\|^2=1.
\tag{7}
$$

Equations (6) and (7) are exactly support-sum separation using (5). Compact convex
bodies with disjoint interiors admit a nonzero separating normal, which can be
normalized to length one; conversely these support inequalities separate their
interiors. They therefore describe the actual nonoverlap of the declared core bodies,
including legal touching.
The normals range over the entire unit circle, including both signs.
Restricting them to coordinate or selected-square axes would omit valid separations
along curved boundaries.
Assigning different normals to the inequalities of one pair would weaken the hull model
to separate component checks and is forbidden.

The exact inventory is 49 two-coordinate normal variables, 49 unit-circle equalities and
140 support inequalities, alongside the seven center/core graphs and the selected
domain. These are core-model predicates, not 49 actual residual full-square SAT clauses.
Separate disk/core component checks may be explanatory controls, but no union-only,
disk-only or octagon-only target is substituted for this model.

Let $\mathcal M_7$ denote this seven-core feasible set, and let $\kappa_{\rm wall}(G)$
be the maximum number of such residual cores at fixed $G$. Every full-square extension
induces a model configuration by (4), and every model configuration induces the
corresponding disk configuration.
Thus

$$
\kappa_\square(G)\le\kappa_{\rm wall}(G)
\le\kappa_{\rm disk}(G)\le\kappa_{\rm oct}(G).
\tag{8}
$$

BC279’s target is precisely $\mathcal M_7=\varnothing$, equivalently
$\kappa_{\rm wall}(G)\le6$ for every $G\in\Gamma_0$. No value of $\kappa_{\rm wall}$ is
established by this protocol.

## Exact Graphs, Closed Seams and Reflection

Every derived value in this protocol is its stated function, not an unconstrained
auxiliary. An exact rational-polynomial description uses

$$
r\ge1/2,\quad r\le X,Y,q-X,q-Y,
$$

$$
r=X\quad\lor\quad r=Y\quad\lor\quad r=q-X\quad\lor\quad r=q-Y,
\tag{9}
$$

and $a\ge0$ together with

$$
(r^2\le1/2\ \wedge\ 4ar=1)
\quad\lor\quad
(r^2\ge1/2\ \wedge\ 8a^2=1).
\tag{10}
$$

Both saturation branches agree at equality.
Every wall-minimum tie belongs to every applicable branch.
The values are uniquely determined and positive.
The square-root constant in (3) has therefore introduced no approximate threshold.

For exact absolute values, $w=|z|$ means $w\ge0,w^2=z^2$. For a finite minimum, require
the value to be no greater than every entry and equal to at least one; use the reversed
inequalities for a maximum.
These graphs define $m$ and the row scatter exactly, while $2c_i m_i=1$ defines each
$m_i$. All signs and min/max ties are retained.
Equations (1), (2), (6)–(10) with these graph conventions constitute a finite closed
semialgebraic description with rational polynomial predicates.
Normal circles and bounded center domains make its auxiliary graphs compact too.

Midpoint-only core values are not the declared model.
If a separately authorized outer approximation later uses a constant core on a cell, it
must be no larger than the true core throughout that cell; using a midpoint value
without such a bound can be unsound.
No cell approximation or engine is authorized by this document.

For every fixed lower parent retain its guarded child and all eight closed failure
children $P_{0,I,\pi}\cap\{g\le0\}$, where $g$ ranges over (2). If success fails, a
guard is strictly negative, so these children cover the remainder.
A success point with $g=0$ belongs to both corresponding children.
An equality point with another negative guard need not be in success.
All subsets and weak orders remain present.
The central cover and its accepted
[24-guard correction](bc-270-parent-compatibility-design.md#closed-siblings-comparison-status-and-next-obligation)
are unchanged.

Let $\mathcal R(X,Y)=(X,q-Y)$ and let $T(X,Y)=(X,-Y)$ be its linear part.
Apply the affine map $\mathcal R$ to every selected and residual center.
Apply $T$ to every displacement, separating normal and square basis vector; replace
selected angles by their negatives, with the resulting basis sign absorbed by the
square’s corner signs.
This is a joint reflection of every pose and separation predicate.
Then $r,a$ are invariant, $K(r)$ is reflection invariant, all support inequalities are
preserved and $B_0$ maps to $B_2$. The upper guards are (2) evaluated in depths $q-y_i$.
This defines the complete reflected success and failure children.
Band seams retain their closed representatives even where reflection changes their
canonical counting owner.
A reflection of only the four selected poses is not a domain transfer.
No full-square child is pruned before independent acceptance of a whole-domain
implication.

## Explicit Admission Controls

These controls check the model and its interpretation.
They are not target attempts.

| Control | Exact expected result |
| --- | --- |
| Original lower fixture $x_i=18/25+4i/5$, even $y_i=18/25$, odd $y_i=71/50$, all $\theta_i=\pi/4$ | Accept four-pose membership only. Its eight guard values are $7/10,h-599/1000,h-13/25,79/1000,79/1000,249/500,249/500,249/500$, with $h=1/\sqrt2$. All are positive; containment and selected SAT have the accepted strict margins. No seven-body capacity follows. |
| Joint reflection of that fixture | Preserve all guard values, with even heights $78/25$, odd heights $121/50$, and angles $-\pi/4$. Preserve both band and angle seam lifts. |
| Actual unit squares centered at $(1/2,1/2)$ and $(3/2,1/2)$ | Here $r=a=1/2$. Accept the legal core/full-square touch using normal $(1,0)$; all four pair support thresholds equal one. |
| $r=3/5$, $a=5/12$, $c=(6+\sqrt{14})/10$, $s=(6-\sqrt{14})/10$ | Verify $c^2+s^2=1$, $h=3/5$ and a core vertex on an actual square edge. An inflated halfside must fail common-core inclusion. |
| $r\ge1/\sqrt2$ and the equality seam | Recover exactly the disk and retain both equal saturation branches. No extra interior-region strength may be claimed from the axis core. |
| Accepted BC278 author disk centers $P_2=(279/100,167/50)$ and $P_4=(167/50,5/2)$ | Both give $r=a=1/2$. Their coordinate gaps $11/20,21/25$ are both below one, so their axis-square cores overlap and no unit normal can satisfy (6). Reject this accepted disk witness in the new model; do not infer capacity six. |
| Accepted BC278 adversary octagon witness | Its audited disk-to-selected-square overlap remains forbidden because every $K$ contains its incircle. An octagon witness cannot bypass (7). |
| Arbitrarily changed $r,a,m$ or understated scatter | Refuse the claimed exact model graph or source-domain identity. |
| Separate normals within one pair, a zero normal, selected-axis-only normals, omitted support inequality, dropped guard/failure child or midpoint substitution | Refuse a claim to this complete model or a whole-parent conclusion. A sound weakening, if separately declared, has a different comparison contract. |

The last two BC278 controls reuse the
[audited exact configurations](bc-278-boundary-band-independent-review.md).
Their rejection is established by generic inclusion and the displayed pair calculation;
no new seven-core packing search is part of admission.
The hull identity itself requires independent review, including its endpoint cases and
the same-normal predicates.

## Prospective Acceptance and Stopping Rules

The target author and adversary must work on this whole unchanged model independently
until both terminalize.
Permitted scientific work is bounded hand analysis and exact construction.
No numerical target, solver, one-off target script, engine build, resource sweep, added
guard, fitted center box or serial weaker-model retry is admitted.
A need for such work is a recorded limitation, not automatic authorization.

Accept a model exclusion only with an independently audited argument covering every
$G\in\Gamma_0$, all seven center variables, all 49 complete normal predicates, every
wall-minimum and saturation branch, actual selected angle endpoints, weak contacts and
all source-domain seams.
A proof for one fixture, a strict subdomain or a partial branch inventory is
insufficient. By (8), a uniform bound of six would exclude the corresponding full-square
child and its joint reflection, while preserving the unresolved siblings.

Accept a negative model result only with an exact seven-core witness: four actual
selected poses and seven centers, the uniquely derived graph values, and explicit 49
unit normals or exact constructions generating them.
The reader must verify selected containment, all six complete selected SAT clauses, the
eight source guards, all center bounds and graph equations, and every inequality in (6)
and (7). Exact algebraic coordinates require their defining equations and unambiguous
real-root choices; approximate coordinates or residuals are not certificates.

Such a witness refutes only the uniform wall-core bound.
Because (4) is the maximal common core, the same witness also obstructs packing-only
models using smaller individual cores justified by exactly the same wall information.
It does not obstruct additional joint angle premises.
It is not an eleven-square packing: that would require actual residual orientations,
their actual containment and all 55 clauses (1). No lower bound on full-square capacity
follows from a core witness.

A failed construction, unresolved case, incomplete cover or expired lease leaves the
model target unresolved.
No continuation, engine switch or changed guard family follows automatically.
Full-square $D_0$ remains separately unresolved unless an accepted implication or actual
eleven-square witness determines it.

Strict H118 comparison is also separate.
It requires a frozen strongest matching coupled outer LP on the same domain, including
its ordering, projection, SAT and nonlinear-graph relaxation policies, together with an
exact feasible point surviving that comparator.
This protocol supplies neither.
Rejecting a disk witness is not an LP comparison.
At fully fixed actual angles and complete chosen SAT branches, the geometry is an exact
LP, and a sound capacity statement cannot exclude a genuinely feasible point of that
exact geometry. A wall-core exclusion without the required comparator witness is
parent-cover evidence, not strict H118 separation.

## Price, Admission Gate and Receipt

The phase-15 design/admission window is 11:12:25–11:37:25 UTC on 2026-09-07; this
writer’s absolute design deadline is 11:27:25. Reviewers may inspect the frozen W5
formula concurrently, but must reconcile their admissions against this final native
protocol after it freezes.
The coordinator owns record changes, protocol publication and commit.
Passing record checks and independent admissions against the final model, followed by a
committed prospective protocol, must precede any target dispatch.

Price one future analytical author for **30 minutes** and an independent adversary for
**25 minutes**, concurrently, followed by a fresh **20-minute independent audit** after
both reports freeze.
This is at most 75 worker-minutes and 50 minutes of mathematical critical path,
excluding admission and integration.
Actual leases will be recorded later; these are prospective caps, not launched work.

All scientific target and audit work must stop by **12:40 UTC**. Honoring all priced
caps requires dispatch no later than 11:50 UTC. If the gate completes later, the
coordinator must prospectively shorten the leases or decline dispatch; there is no
deadline extension. A generic core identity and controls do not admit a scientific
capacity result by themselves.

The actual first clock read for this packaging task was **11:15:32 UTC**. I read the
complete current BC277 domain and used the frozen assessment and accepted BC278 results.
Only this assigned native protocol was written.
No scientific target, numerical run, solver, engine build, new identifier, shared-record
edit, dependency change or Git mutation occurred.
The target remains unattempted.
The native model and protocol froze at **11:23:05 UTC**, 7 minutes 33 seconds after the
actual first clock read.
The final wording distinguishes affine center reflection from linear normal reflection,
retains all disk conditions in the saturated regime, and distinguishes common cores from
the old guard octagons.
All scientific source links are native repository documents.
Installed Flowmark 0.4.0 formatting and its no-cache check passed; linked files exist,
the required footer appears once, and the trailing-whitespace scan found no matches.
A final scoped formatting check follows this receipt before notifying the coordinator
and both admission reviewers, within the 11:27:25 design deadline.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
