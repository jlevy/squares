# BC-282: Independent Skeleton-Design Admission

**Accept the exact domain, envelope and translation/fiber reduction. NO-GO for the
conditional 30/25/20-minute target.** The
[frozen design](bc-282-residual-skeleton-design.md) preserves all 40 containment rows and
45 pair clauses through its reduction. Its proposed six-source fence is sufficient for
exclusion but remains unproved and is not equivalent to general interval coverage.
There is no bounded set of uniform templates or accounted sequence of active-facet
transitions from which to price the target. This verdict follows the reconstruction
below, independently of the author's recommendation.

This is the separately dispatched admission in
[session096](../../../../agent-sessions/session-096-residual-skeleton.md), phase 2,
under BC282 and `think-s6e7`. The earlier
[domain inventory](bc-282-residual-domain-inventory.md) was written without reading the
new design or proposing its new implication. The other frozen
[inherited-premise inventory](bc-282-inherited-premise-inventory.md) was read during
this admission. Both are consistent with the
[BC281 audit](bc-281-full-angle-independent-review.md), whose accepted results are not
reopened here.

## Domain and Envelope Reconstruction

The design keeps the seven parameters $(L,z,p_x,p_y,a,b,t)$, the original side and
center bounds, and all ten indexed centers from
[BC280](bc-280-full-angle-release-domain.md). It retains both closed slide signs over
$[1/24,1/3]\cup[1/2,23/25]$, including zero slides, all angle endpoints and all contact
equalities. Deleting square 10 removes precisely four containment rows and its ten pair
clauses; $15+24+6=45$ retained pairs remain. The original eleven-square projection is
included in this necessary skeleton; equality or universal extendability is not asserted.

Write $q_0=(L,z,a,b,t)$ for the structural tuple and keep the design's
$U=ae-f$, $V=e+bf$, with offsets $0,U,V,U+V$. In either coordinate, minimization over
these four offsets is exactly the sum of the two separate minima over $\{0,U_d\}$ and
$\{0,V_d\}$; maximization works identically. Thus the displayed $m_x,M_x,m_y,M_y$ are
exact even when an increment vanishes.

All four block squares have axis support $h=(c+s)/2$. In each coordinate, taking the
strongest of their four lower and four upper bounds gives precisely

$$
T=[h-m_x,L-h-M_x]\times[h-m_y,L-h-M_y].
$$

The prescribed axis squares are contained for the declared $L,z$ bounds. Their 15 pair
clauses are still imposed. The six block clauses also remain, including both diagonals.
Containment of square 6 implies $p\in[1/2,167/50]^2$, so omitting a separate
intersection with the looser original $p$ box changes nothing. This accounts for all 40
wall rows without changing $L$ or moving any fixed wall square.

The ten chamber rows check as follows. On the low interval,
$c\ge4/5$ and $s\le3/5$, so $U_y\le-13/20<0$ and $V_x\ge13/20>0$ for both slide
signs. Nonnegative slides also give $U_x,V_y>0$. Nonpositive slides leave exactly the
four weak choices of $U_x$ and $V_y$. On the high interval,
$s\ge4/5$ and $c\le3/5$ give $U_x,V_y\ge13/20>0$. Nonpositive slides fix
$V_x>0,U_y<0$; nonnegative slides leave exactly the four weak choices of $V_x,U_y$.

| Chamber group | Independent extremal-owner check, in left/right/bottom/top order |
| --- | --- |
| Low, nonnegative | $6,9,7,8$ |
| Low, nonpositive, $U_x\ge0,V_y\ge0$ | $6,9,7,8$ |
| Low, nonpositive, $U_x\le0,V_y\ge0$ | $7,8,7,8$ |
| Low, nonpositive, $U_x\ge0,V_y\le0$ | $6,9,9,6$ |
| Low, nonpositive, $U_x\le0,V_y\le0$ | $7,8,9,6$ |
| High, nonpositive | $6,9,7,8$ |
| High, nonnegative, $V_x\ge0,U_y\le0$ | $6,9,7,8$ |
| High, nonnegative, $V_x\le0,U_y\le0$ | $8,7,7,8$ |
| High, nonnegative, $V_x\ge0,U_y\ge0$ | $6,9,6,9$ |
| High, nonnegative, $V_x\le0,U_y\ge0$ | $8,7,6,9$ |

Every listed owner follows directly from the sums of signed increments. At zero, both
weak chambers overlap and the extrema agree; tied owners do not change $T$. Since
$c,s>0$ throughout the closed remainder, actual block corners 3, 1, 0 and 2 supply the
left, right, bottom and top support offsets respectively. The design assumes neither a
global top-center label nor a reflection between the intervals.

## Exact Open Collision Intervals

Fix $q_0$ satisfying the retained axis and internal clauses. For one axis/block pair set

$$
d_x=X+o_{j,x}-C_{i,x},\qquad d_y=Y+o_{j,y}-C_{i,y},\qquad
D=(1+c+s)/2.
$$

Both actual-square supports sum to $D$ on each of $x,y,e,f$. The complement of the
complete nonoverlap clause is therefore exactly

$$
|d_x|<D,\quad |d_y|<D,\quad |cd_x+sd_y|<D,\quad |-sd_x+cd_y|<D.
\tag{C}
$$

It describes interior overlap. A weak equality in any separating direction remains
legal nonoverlap. If $|d_y|\ge D$, (C) is impossible and the forbidden interval is
empty, including at equality. Otherwise the three constraints on $d_x$ are the open
intervals

$$
(-D,D),\qquad
\left(\frac{-D-sd_y}{c},\frac{D-sd_y}{c}\right),\qquad
\left(\frac{cd_y-D}{s},\frac{cd_y+D}{s}\right).
$$

Their intersection, translated by $C_{i,x}-o_{j,x}$, gives exactly the design's maximum
of three lower endpoints and minimum of three upper endpoints. Division is by positive
$c,s$ only. If the resulting lower endpoint is at least the upper endpoint, the open
interval is empty; a singleton collision interval is not invented.

Consequently, for every retained structural tuple,

$$
(X,Y)\text{ completes the skeleton}
\iff (X,Y)\in T\ \text{and}\quad
X\notin\bigcup_{i=0}^{5}\bigcup_{j=6}^{9} I_{ij}(Y).
$$

All 24 cross clauses occur once in this union; none is screened or replaced by a chosen
SAT branch. Together with the retained 15 axis and six internal clauses this is the
claimed exact 40/45-to-fiber equivalence. It proves no particular fiber covered.

The 12 row/block slice types also check: four offsets against the three axis heights
$1/2,L-1/2,L-3/2$. Horizontal differences within a row are known translations, not
permission to discard the individual source labels or their different positions.

## Strict Coverage and Every Degenerate Fiber

For a nonempty closed horizontal fiber $[l,r]$, the proposed fence begins with an open
interval containing $l$ strictly. Each subsequent interval has its lower endpoint
strictly below the preceding right endpoint and a right endpoint no smaller than that
preceding endpoint. The two intervals therefore overlap on an open set. Inductively
their union covers from $l$ to, but not including, the final right endpoint. Requiring
$r$ strictly below that endpoint covers the entire closed fiber.

Thus the six-source condition is a valid sufficient implication. It requires pairwise
distinct axis owners and at most six intervals; those restrictions do not follow from
the full interval-union description.

For an arbitrary cover by the full 24 open intervals, begin with one containing $l$.
If its right endpoint has not passed $r$, the cover must contain that endpoint in
another interval, whose lower endpoint is strictly smaller and upper endpoint strictly
larger. Repeating increases the right endpoint and never reuses an interval. At most
24 intervals suffice. Axis-source labels may repeat. For $l=r$, one interval containing
that point already suffices. This establishes the unrestricted chain representation,
not the proposed six-source bound or coverage of a target fiber.

| Containment or collision case | Required treatment |
| --- | --- |
| Inverted horizontal or vertical containment interval | $T$ is empty; this structural tuple has no translation. |
| Positive width and height | Check every height in the closed vertical interval, including both ends, and both horizontal endpoints. |
| Zero horizontal width | The singleton $X=l=r$ is excluded only if some forbidden open interval contains it strictly. |
| Zero vertical height | Check that one height; do not remove it as an empty range. |
| Both widths zero | Check the single translation point against all 24 open intervals. |
| $|d_y|=D$ or $\lambda=\rho$ | The individual forbidden interval is empty; another interval would have to cover the point. |
| Active lower/upper ties or zero envelope increments | Keep the weak parameter seam; max/min formulas remain exact there. |
| Neighboring interval endpoints merely equal | Their common point is uncovered by those two open intervals. |

The design's component control reconstructs directly: two axis unit squares at equal
height collide when the second center has $X\in(-1/2,3/2)$ relative to the first center
at $X=1/2$. At $X=3/2$ they touch legally. Likewise $(0,1)\cup(1,2)$ omits 1. These
are strictness controls, not target witnesses. No closed-polygon tangency rule can be
substituted for them.

## Readiness and Evidence Dispositions

No error was found in the exact reduction, chamber table, interval formulas or stated
strict-chain implication. The inherited cap and separating lemmas remain restricted
to their audited domains; the new reduction does not promote their $c,s\ge1/4$
conclusions into the outer residual portions. The two negative scalar threshold
controls still specify no feasible centers.

**The target is not admitted.** A finite inventory of 24 intervals and ten envelope
chambers leaves five structural variables and a height variable, with three competing
lower and three competing upper facets per slice, interval births/deaths, endpoint
orders and weak seams. The design supplies neither uniform strict-cover templates nor
a bounded accounting of these transitions. The general at-most-24 chain argument does
not fill this gap, and the six-source condition remains an unproved strengthening.
No bounded alternative witness discriminator is supplied either. These are independent
reasons not to spend the conditional 75 worker-minutes and 50-minute critical path.

The existing [closed polygon cover tool](../../../../../devtools/closed_polygon_cover.py)
was inspected read-only. Its contract counts closed tangencies, accepts fixed data in
one supplied number field, and requires a nondegenerate rectangle. It does not verify
these open forbidden intervals over variable structural parameters or their degenerate
containment fibers. Existing tooling therefore supplies no missing admission evidence.
No adapter or replay is authorized by this review.

An exact ten-square witness must satisfy the complete parameter, feature, 40-row and
45-clause contract, equivalently all retained structural clauses plus one point of $T$
outside all 24 open collision intervals. Failure of a six-source chain alone is not
such a witness. An exact skeleton refutes skeleton emptiness but supplies no square-10
extension. An actual eleven-square witness needs its independent $w,v$, four further
containment rows and ten further pair clauses. Complete skeleton exclusion would finish
only the original restricted source family with its inherited complementary coverage;
no unrestricted bound or representative theorem follows.

The next action is to record the accepted reduction and the target NO-GO, then reprice
from the explicit missing uniform coverage argument. Any later allocation must supply
bounded templates and transitions, or a different complete discriminator with a credible
price, before a separately committed target protocol. No target, partial interval or
unchanged BC281 retry begins at this checkpoint.

## Work Receipt

The prospective admission lease was **17:39:15–17:49:15 UTC on September 7, 2026**.
The actual first clock was **17:40:17 UTC**; initialization did not move the hard stop.
The author was terminal at 17:38:53 UTC before this reader opened the design.
This reviewer authored only the earlier domain inventory and BC281 audit, neither of
which coauthored the new translation-fence implication. The complete frozen design was
read, and its new algebra, chamber coverage, quantifiers and strictness were reconstructed
independently here. Author agreement was not an acceptance premise.

No target proof, chain inequality search, numerical run, optimizer, adapter, scientific
code, source replay, Git operation, shared-record edit or new identifier occurred.
Only this assigned admission document was written. Skeleton feasibility, complete
coverage, the six-source strengthening and target tractability remain unresolved.

Mathematical reconstruction and content readback froze at **17:45:17 UTC**, 300 seconds
after the first clock. At **17:45:18 UTC**, all seven native links resolved, the
required footer occurred once, the trailing-whitespace scan had no matches and the
installed Flowmark no-cache check passed on this assigned file.
The common-document and prose passes were applied.
No mathematical continuation follows the freeze.

Final recorded end clock: **17:46:50 UTC**, 393 seconds after the first clock.
The final receipt also passed the same scoped format/check before terminal delivery.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
