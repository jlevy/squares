# BC-270: Independent Review of the Parent Compatibility Fence

The [parent-fence construction](bc-270-parent-compatibility-design.md) is accepted.
Its finite guards imply that at most four further unit squares can coexist with the
selected four squares, at arbitrary residual orientations.
Thus its guarded eleven-square child $D$ is empty.
The exact central four-square fixture satisfies the four-pose guards with strict
margins, as does a relative open family of nearby actual poses.
No decisive geometric premise failed this audit.

This accepts a restricted parent-compatibility result.
It does not establish
[H118](../../../../hypotheses/H-118-capacity-versus-coupled-lp.md): the strongest
declared coupled outer LP on the identical guarded domain, including a sound
representation of the nonlinear guards, and an exact surviving point are still missing.
The [original capacity-comparison design](bc-270-capacity-comparison-design.md) remains
correct about feasibility of the unguarded four-square and anchored five-square
subsystems.

This is session092’s independent BC270 review under the recorded 09:05:57–09:20:57 UTC
lease. I read the two designs and H118, and reconstructed the geometric inclusions,
section cover, diameters and fixture comparisons by hand.
No concurrent negative-slide report was read or used.

## Actual-Angle Cores and Strict Forbidden Guards

For an actual orthonormal square basis, put

$$
m_i=\frac1{2\max(|e_{i,x}|,|e_{i,y}|,|f_{i,x}|,|f_{i,y}|)}.
$$

The denominator is positive.
Each vertex $(\pm m_i,0),(0,\pm m_i)$ has both square basis projections of magnitude at
most $1/2$. Convexity therefore proves $\mathcal D(m_i)\subseteq Q_i$, with
$1/2\le m_i\le1/\sqrt2$. This uses each square’s actual orientation and is invariant
under its quarter-turn lifts.
The complete closed angle chart and both seam representations are retained.

The eight vertices of $E$ are the sign and coordinate permutations of $(2/5,299/1000)$.
Their squared norm is

$$
(2/5)^2+(299/1000)^2=249401/1000000<1/4.
$$

The norm on their convex hull is no greater than the maximum vertex norm.
Thus the entire closed octagon lies strictly inside every residual square’s radius-$1/2$
incircle. If a residual center is $C_i+d+e$ with $d\in\mathcal D(m_i)$ and $e\in E$, the
point $C_i+d$ lies in $Q_i+C_i$ and in the residual square’s interior.
Even if it is on the first square’s boundary, a sufficiently small move toward that
square’s interior stays inside the residual interior.
The two interiors therefore overlap.
This proves the asserted strict forbidden-center implication on the guard boundary as
well as in its interior.

The Minkowski-sum octagon is exactly

$$
\mathcal D(m_i)+E
=\{(x,y):|x|,|y|\le m_i+2/5,
\quad |x|+|y|\le m_i+699/1000\}.
$$

The forward inclusion follows from the triangle inequalities.
Conversely its vertices are the sign and coordinate permutations of
$(m_i+2/5,299/1000)$, obtained by adding $(m_i,0)$ and $(2/5,299/1000)$. Their convex
hull proves the reverse inclusion.

For the virtual-row construction, $|v_i-y_i|\le\varepsilon$ by the definitions of the
two averages and the measured maximum scatter.
With $m=\min_i m_i$ and $A=m+2/5-\varepsilon$, $R=m+699/1000-\varepsilon$, every point
of $K_i$ satisfies

$$
|X-x_i|\le A\le m_i+2/5,\quad
|Y-y_i|\le A+\varepsilon\le m_i+2/5,
$$

$$
|X-x_i|+|Y-y_i|\le R+\varepsilon\le m_i+699/1000.
$$

Hence $K_i\subseteq C_i+\mathcal D(m_i)+E$. The shrink spends the scatter once in the
diagonal inequality; it does not assume that the actual row heights coincide.
Every residual center avoids every closed $K_i$.

## Exhaustive Horizontal-Section Cover

Write $k=299/1000$. The first fence inequalities give $A\ge k>0$ and
$0\le\Delta\le A-k$. On the overlap $u-A\le Y\le\ell+A$, both row sections are active.
Each radius

$$
r_v(Y)=\min(A,R-|Y-v|)
$$

is concave on its active interval.
At an overlap endpoint the two radii are $k$ and $k+\Delta$: the latter is at most $A$.
Their sum is consequently at least $2k+\Delta$ throughout the overlap.
Because the slots are weakly ordered by $x$ and alternate rows, the consecutive
intervals meet by (F). Their first left endpoint is at most $b$, and last right endpoint
at least $d$, using $r_v\ge k$, $x_0\le b+k$ and $x_3\ge d-k$. This covers the entire
horizontal center interval, including equality between consecutive guard intervals.

Below the overlap, $b\le Y\le u-A\le\ell$, the low row is active because $\ell-A\le b$.
Its radius is exactly $R-\ell+Y$: at the highest such ordinate it is $k+\Delta\le A$.
The slot-0 interval reaches the left boundary.
A center outside both low-row guards is therefore between them or to the right of slot
2\. The weak between-interval enlargement has sides

$$
X\ge x_0+R-\ell+Y,\qquad X\le x_2-R+\ell-Y.
$$

They meet at the displayed apex of $P_B$, and their section at $Y=b$ is its displayed
base. Every nonempty such section lies in $P_B$. The right-hand enlargement is
$X\ge x_R+(Y-b)$, $b\le Y\le y_R$, $X\le d$; its vertices are exactly those of $P_R$.
The guard $0\le h_R\le w_R$ makes the stated trapezoid valid, including its degenerate
limits.

Above the overlap, $\ell+A\le Y\le d$, the high row is active by $u+A\ge d$. Its radius
is exactly $R+u-Y$, since $\ell+A\ge u$ and its radius at the lower endpoint is
$k+\Delta\le A$. The last interval reaches the right boundary.
The left-hand enlargement has

$$
b\le X\le x_1-R-u+Y,\qquad Y\le d,
$$

which is the displayed triangle $P_L$. The between-interval enlargement has sides
$X\ge x_1+R+u-Y$, $X\le x_3-R-u+Y$, meeting at the displayed apex of $P_T$. This proves
the claimed exhaustive inclusion

$$
[b,d]^2\setminus\bigcup_i K_i
\subseteq P_B\cup P_R\cup P_L\cup P_T.
$$

If a portion of one of these height ranges is empty, its inclusion is vacuous; no
additional sign assumption is needed.
The overlap itself is covered by the closed guards.
The four remaining regions are weak enlargements, so no potentially legal touching point
is removed by taking their boundaries.

## Four Diameters and Residual Capacity

The guards require all vertices inside the center box and nonnegative region sizes.
The middle triangles have height half their base length.
Their largest vertex distance is the base, respectively $w_B$ and $w_T$. The left
triangle has diameter $\sqrt2v_L$. After translation, the right trapezoid has vertices

$$
(0,0),\quad(w_R,0),\quad(w_R,h_R),\quad(h_R,h_R).
$$

When $0\le h_R\le w_R$, every pairwise squared vertex distance is at most $w_R^2+h_R^2$,
attained between $(0,0)$ and $(w_R,h_R)$. A convex hull’s diameter is bounded by its
largest vertex distance: represent each of two points as convex combinations and apply
the triangle inequality to their difference.
Thus (C) proves that every region has diameter at most $\beta=999/1000<1$.

Two centers in one region would be less than one apart.
Their open radius-$1/2$ incircles would overlap, and hence so would their unit-square
interiors, independently of orientation.
Assigning each center to its lowest-index containing region handles region intersections
without double counting.
At most four residual centers are possible.
This is a uniform complement-capacity bound $\kappa(G)\le4$ for additional full unit
squares, not a bound on isolated centers without their square geometry.
The seven residual labels of an eleven-square parent contradict it.

## Exact Fixture and Continuous-Family Check

For $h=1/\sqrt2$, the exact enclosure $7071/10000<h<7072/10000$ follows by squaring
positive endpoints. At the stated four diamonds it gives $m=h$, $\varepsilon=0$,
$\ell=8/5$, $u=23/10$, $A=h+2/5$, $R=h+699/1000$ and $\Delta=7/10$.

I checked all fence inequalities, including the smaller clearance $\ell-A=6/5-h<1/2$,
the top reach $u+A=27/10+h>d$, and $\Delta<A-k=h+101/1000$. The two end-slot and all
consecutive-gap guards have the strict margins stated in the design.
The region substitutions are

$$
w_B=1201/500-2h<9878/10000<\beta,\qquad
w_T=1141/500-2h<8678/10000<\beta,
$$

$$
v_L=1361/1000-h<2/3,\quad
w_R=1421/1000-h<143/200,\quad
h_R=7/5-h<139/200.
$$

All are positive, and $w_R-h_R=21/1000>0$. The remaining diameter checks are

$$
2v_L^2<8/9<\beta^2,\qquad
w_R^2+h_R^2<3977/4000<\beta^2.
$$

Substitution in the four vertex lists reproduces the design’s fixture vertices exactly.
The same $h$ enclosure puts every nonconstant coordinate strictly between $b$ and $d$;
the remaining coordinates lie identically on their specified box edges.

The original fixture’s containment and all six pair checks also pass: minimum wall
clearance is $18/25>h$, adjacent diamond centers have $L^1$ distance $3/2>\sqrt2$,
two-step centers have distance $8/5>\sqrt2$, and the endpoints have distance
$31/10>\sqrt2$. Its band membership and horizontal ordering are strict.
Every nontrivial success guard has strict margin.
Minimum, maximum and absolute-value operations are continuous even at their ties, so
nonzero scatter and inward angular perturbations preserve the guards in a sufficiently
small relative open family.
The finite inequalities, rather than an unspecified neighborhood, define the closed
guarded four-pose set.

The membership control here consists of four poses satisfying those guards.
It is not a point of the full eleven-square child $D$, which this proof excludes.
The original bottom anchor is one residual square and consumes one of the at most four
available places; the anchored five-square fixture therefore cannot admit six more
squares. The lower-band fixture fails $u+A\ge d$, and its upper-band reflection is
outside the central child.
Neither sibling is excluded by this result.

## Complete Parent Cover and Its Limits

The three closed bands cover the full possible center-height interval.
Assigning their seams to the lower-index band makes the pigeonhole count unambiguous:
eleven centers force four assigned to one of three bands.
Every four-label subset and every weak horizontal ordering is retained.
The closed parent cover consequently includes band seams, order ties and bands
containing more than four centers.
All eleven containment conditions and all 55 complete weak SAT disjunctions remain part
of each parent. The seven residual labels have no additional angle or location
restriction.

Every fence, vertex and diameter guard is continuous in the actual poses.
Their finite conjunction with the compact parent is closed.
Writing the guards as $g_r\ge0$, the success child together with all closed siblings
$g_r\le0$ covers its central parent: a point outside the conjunction has some $g_r<0$.
All lower and upper parents remain, as do every label and ordering.
The proof supplies the necessary failure of at least one success guard, not the
assertion that every four-square group satisfies the fence.

One representation detail limits claims about pruning: some displayed vertex bounds are
identically tight, such as the bottom ordinate $Y=b$. Its expression $g_r=Y-b$ is
identically zero, so its closed failure sibling is the entire central parent.
Including such siblings is sound but redundant.
The sibling formula alone therefore does not guarantee a proper reduction of every
parent. A materialized cover should distinguish tautological bounds from guards that can
fail; no capacity argument depends on removing them, and this review does not change the
proposed construction.

The restriction excludes the fixture’s guarded continuous family for a proved residual
reason.
It does not cover the other bands or central guard-failure siblings and yields no
unrestricted eleven-square lower bound.

## Comparator Obligation and Disposition

No same-domain coupled-LP survival witness is present.
A matching comparator must retain the same actual angle variables, selected labels,
orders, walls, all applicable projection/incircle deductions and the same SAT branching
policy.
It must also declare an exact or rigorously justified outer representation of the
pose-dependent minimum, maximum, absolute-value and quadratic guards.
Comparing the guarded capacity result with an unguarded or otherwise weakened arm would
not establish the stated H118 claim.

At fixed exact angles a fully selected physical SAT system is an exact translation LP;
the additional nonlinear guards do not become linear merely by calling that system the
comparator. Their representation and any remaining relaxation must be explicit.
The complete row/constraint inventory and an exact feasible relaxation point need
independent checking.
No failure to find a dual or numerical solver status supplies that witness.

The capacity implication is accepted; H118 and BC271 remain unresolved as a strength
comparison, and BC261 readiness is not inferred.
The next action is to return the accepted compatibility restriction and its complete
siblings to BC262’s parent-cover owner.
A later same-domain comparison needs its own prospective definition and price.
No resource search is needed to rediscover this proved exclusion.

## Work Receipt

The lease was recorded as `2026-09-07T09:05:57Z` through `2026-09-07T09:20:57Z`. The
first clock read after dispatch was `2026-09-07T09:10:35Z`. Work consisted of the three
requested source reads and exact hand reconstruction of the implications above.
No numerical target, solver, target script, resource search or source witness replay
ran.

Only this assigned review was written.
No concurrent negative-slide argument was read or used, and no shared record, Git state,
identifier or dependency was changed.
The document received the common-guidelines and de-slop passes and installed Flowmark
0.4.0 with caching disabled.

The mathematical review, full reread and initial document checks completed at
`2026-09-07T09:17:37Z`, 7 minutes 2 seconds after the first clock read and 3 minutes 20
seconds before the hard deadline.
Flowmark’s full auto-format check passed; all three linked sources existed; no trailing
whitespace was found; the footer appeared once; and the equations survived the formatted
readback. A final scoped formatting check follows this receipt before delivery.
No background command remains.

## Coordinator Review of the Remainder Correction

The coordinator independently checked the corrected 24-guard list after its author froze
it at 09:29:42 UTC. This review began at 09:30:03 UTC and completed at 2026-09-07
09:31:20 UTC. The nine fence expressions retain every non-parent-implied part of (F).
For each middle triangle, the base endpoints are exactly its midpoint plus or minus its
nonnegative height; their box bounds also imply the apex-height bound.
The left triangle requires exactly $0\le v_L\le d-b$, and the right trapezoid exactly
$0\le h_R\le w_R\le d-b$. Thus the eleven vertex expressions are equivalent to the
original vertex and size conditions.
The remaining four expressions are exactly (C).

Every listed expression is strictly positive at the exact four-pose fixture, including
$b-\ell+A=1/2-6/5+h>0$ and $w_R-h_R=21/1000>0$. Continuity therefore gives the stated
relative open four-pose family excluded from every closed failure child.
Outside the success conjunction some retained guard is strictly negative, so the failure
children still cover the necessary remainder.
All equality seams remain.
No eleven-square fixture membership or global pruning percentage is asserted.

The correction is accepted at that representation scope.
The historical finding above remains the assessment of the original redundant list; the
capacity theorem and its missing H118 comparator are unchanged.
No numerical target or new theorem was attempted.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
