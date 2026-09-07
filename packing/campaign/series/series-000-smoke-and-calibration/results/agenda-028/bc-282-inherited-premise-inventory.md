# BC-282: Inherited Premise Inventory

**The inherited lemmas leave a complete residual skeleton question open.** Both counts
and the individual top-cap bound apply throughout that remainder.
The stronger cap ordering and forced separating row apply only where $c,s\ge1/4$. The
low-$s$ and low-$c$ portions remain mandatory.
This inventory admits no new implication, scientific target, solver or case-elimination
method.

The sources are the [full-angle domain](bc-280-full-angle-release-domain.md), the
[accepted BC281 audit](bc-281-full-angle-independent-review.md), and the accepted
[positive](bc-273-analytic-independent-review.md) and
[negative](bc-276-negative-slide-independent-review.md) middle-angle audits.
The BC281 audit supplies the inherited verdicts; this report does not reopen them.
The new BC282 design was not read or coauthored.

## Necessary Skeleton and Closed Cover

Delete square 10, its center and angle, its four containment rows and its ten incident
pair clauses from the admitted family.
The remaining seven parameters are

$$
(L,z,p_x,p_y,a,b,t),\qquad
381/100\le L\le96/25,\quad 2\le z\le L-1,\quad
p\in[1/2,7/2]^2,\quad a,b\in[-1/4,1/4].
$$

Retain exactly the admitted centers and corner conventions for labels 0–9, all nine
flush incidences and all six retained positive segments, including their contact sides.
There are **40 actual containment rows and 45 complete pair disjunctions**:

| Pair group | Count |
| --- | --- |
| Within axis squares 0–5 | 15 |
| Between 0–5 and common-angle squares 6–9 | 24 |
| Within 6–9, including both diagonals | 6 |

For every pair, the disjunction still ranges over both signs of all four actual owning
edge axes. Weak equality permits touching.
A proved necessary row may be adjoined; it does not replace an unexamined pair clause.

Every original residual eleven-square point maps into this necessary skeleton.
This statement is inclusion into a relaxation, not an assertion that every skeleton
extends to square 10. Removing its conditions is not computing the exact image of the
original feasible set.

The admitted block diagonals imply $ab\ge0$. Both closed children $a,b\ge0$ and
$a,b\le0$ remain, meeting at $a=b=0$. If one slide vanishes, the sign of the other
determines its child.
Both diagonal clauses remain in the inventory.

The accepted exclusions leave the prescribed closed angle remainder

$$
t\in[1/24,1/3]\ \cup\ [1/2,23/25].
\tag{1}
$$

Each endpoint overlaps an accepted excluded region.
The four endpoint fibers are already excluded by proofs using only labels 0–9, but
remain in the closed cover.
Their exclusion does not justify calling the open set obtained by removing them a closed
remainder.

To express the applicability of $c,s\ge1/4$ exactly, put

$$
\rho=4-\sqrt{15},\qquad \sigma=\sqrt{3/5}.
$$

These are the threshold values already specified by the inherited lemma’s inequalities:
$s(t)=1/4$ is $t^2-8t+1=0$ on the chart, and $c(t)=1/4$ is $5t^2-3=0$. The relevant
roots satisfy

$$
1/24<\rho<1/3,\qquad 1/2<\sigma<23/25.
$$

This translates an existing premise into the admitted half-angle coordinate; it adds no
new exclusion. Cross every row below with both closed sign children:

| Closed angle regime | Applicability of $c,s\ge1/4$ | Mandatory scope qualification |
| --- | --- | --- |
| $[1/24,\rho]$ | At $\rho$ only | Its interior has $s<1/4$; do not use the stronger cap ordering or forced $A$ row there. |
| $[\rho,1/3]$ | Entire row | Both stronger necessary conclusions apply, including $\rho$. |
| $[1/2,\sigma]$ | Entire row | Both stronger necessary conclusions apply, including $\sigma$. |
| $[\sigma,23/25]$ | At $\sigma$ only | Its interior has $c<1/4$; do not use the stronger conclusions there. |

These eight closed angle/sign cells cover (1). The overlaps at $\rho,\sigma$ preserve
the lemma equality cases.
The first residual interval has $c>s$ and the second has $c<s$. The $c=s$ seam and both
axis lifts belong to the already excluded chart regions, rather than being removed by a
symmetry assumption.

## Accepted Lemmas and Their Dependencies

Use the audit’s notation

$$
c=\frac{1-t^2}{1+t^2},\quad s=\frac{2t}{1+t^2},\quad
u=c+s,\quad h=u/2,\quad D=(1+u)/2,\quad
A=e\cdot p,\quad B=f\cdot p.
$$

All statements below are necessary conditions of the actual skeleton, with the original
variable side and retained features.

| Accepted statement | Inherited domain | Conditions that remain relevant |
| --- | --- | --- |
| The support sum is $D$ on each of $x,y,e,f$ for an axis/block pair. | Entire chart, hence all eight residual cells | Actual unit squares and the declared common block basis. This identifies thresholds, not a selected separating direction. |
| $Lu\ge4$ | Entire chart | Six axis squares and four common-angle squares, all contained and interior-disjoint, provide equal axis-aligned inner cores. Equality is retained. |
| $L\ge2+2/u$ | Entire chart with the original $L,z$ ranges | Six axis squares at the prescribed centers and four contained, interior-disjoint common-angle unit squares. The proof can drop the block contact equations, sides and slides; the skeleton definition does not drop them. |
| $y_i\le L-1-h+(L-3)cs$ for $i=6,7,8,9$ | Entire chart | Actual containment and nonoverlap with the three prescribed top squares. The audit treats axis endpoints separately. |
| Only square 8 may have a positive top cap: $y_6+h,y_7+h,y_9+h\le L-1$ | $c,s\ge1/4$ | The retained block neighbor equations, short-slide bounds and actual top-row obstacles. Both signs and all zero slides are included. |
| $A\ge u+1/2$ | $c,s\ge1/4$ | The stronger cap lemma, containment, and complete clauses for 0–6, 1–7 and 5–6. This conclusion does not exclude the broader region. |

The stronger count is accepted for a larger class with four independent common-angle
centers. That reuse preserves the prescribed six axis centers, the same side and top-gap
parameter ranges, and actual containment and interior nonoverlap of all ten.
It gives no result for arbitrary placements of six axis squares, independent angles on
the other four, or another wall pattern.

For an interior angle, define

$$
\delta_i=y_i+h-(L-1),\qquad X_i=x_i+(c-s)/2.
$$

When $\delta_i>0$, the accepted individual cap argument additionally gives
$0<\delta_i<\min(c,s)$ and a weak limiting base interval

$$
\left[X_i-\frac c s\delta_i,\ X_i+\frac s c\delta_i\right]
$$

inside the closure of **one** of the top gaps $(2,z)$ or $(z+1,L)$. It gives
$\delta_i\le(L-3)cs$ throughout both residual intervals.
The skeleton’s residual angles have $c,s>0$, so those denominators are nonzero; small
positive $c$ or $s$ still does not imply the stronger $1/4$ bounds.

The individual lemma does not place every positive cap in the central gap.
The stronger ordering lemma does not assert $\delta_8>0$. At $\delta_i=0$, the weak
height bound applies; strict positive-cap conclusions need their stated positive-depth
premise.
An argument using $B+b\le M$ or the central-gap upper row for $A$ must establish
central localization and positive depth on its own exact branch.

## Exclusions and Screenings That Do Not Extend by Citation

The BC273/276 exclusions cover $[1/3,2/5]$ for the two signs.
BC281 adds $[2/5,1/2]$, $[0,1/24]$ and $[23/25,1]$. Their contradictions use only the
ten retained squares, so the corresponding skeleton fibers inherit exclusion.
Within (1), their direct exclusion coverage consists of the four boundary fibers.

The original middle-angle coarse ranges, forced alternatives and terminal side
contradiction do not become full-residual premises.
In particular:

- The BC281 screening table on $[2/5,1/2]$ has angle bounds absent from both residual
  interiors. Its discarded alternatives remain in all 45 skeleton clauses unless another
  accepted implication applies.
- The proof of the broad $A$ row includes subsidiary cases such as $R:p_x\ge1+h$ and
  $c\le5/8$, or $V:p_y\ge1+h$. A conditional alternative list in that proof cannot be
  installed as a global list without its case premises.
- The terminal inequality $L\ge2+4u/(1+u^2)$ was reached after the applicable cap and
  SAT reductions. Its formula alone is not an accepted universal inequality on the
  residual skeleton.
- The scalar support identity under $t\mapsto(1-t)/(1+t)$ does not reflect the physical
  configuration. The admitted quarter-turn conversion changes basis, slots and corner
  labels together; it does not erase either residual interval.

## What the Scalar Negative Controls Refute

The audit accepts the exact threshold definitions

$$
J=3/2+u-sL,\qquad
M=cL-c-2s-1/2,\qquad
K_5=cL-2c-s-1/2.
$$

At $L=96/25$, its two controls are:

| Half-angle | Exact $(c,s)$ | Accepted negative difference | Location in (1) |
| --- | --- | --- | --- |
| $1/5$ | $(12/13,5/13)$ | $J-M=-7/325$ | $[\rho,1/3]$ |
| $2/3$ | $(5/13,12/13)$ | $J-K_5=-7/325$ | $[1/2,\sigma]$ |

Both controls satisfy $c,s\ge1/4$. Therefore that angle condition and the side range
alone cannot imply $J>M$ or $J>K_5$ uniformly, respectively.
The differences are independent of the slides; selecting one sign child does not repair
an angle-and-side-only estimate.

Neither control supplies $z,p,a,b$ or a feasible ten-square configuration.
They do not refute an implication using further containment, contact or SAT premises; do
not show that a discarded geometric branch survives; and do not provide a packing
counterexample. The broad cap and $A$ lemmas remain accepted.
No eleven-square feasibility, whole-family refutation or changed packing bound follows.

## Admission Boundary and Next Action

The inventory preserves all 45 pair clauses, 40 containment rows, closed signs, side and
$z$ endpoints, slide endpoints, zero slides, weak contacts and all remaining recontacts.
Square 10’s pose and incident clauses are absent only in the necessary skeleton.
Any claim about an actual eleven-square witness must restore its independent center and
angle, all four containment rows and all ten pair clauses.

A complete contradiction for the residual skeleton, together with the accepted
complementary exclusions, would exclude the admitted original source-feature family.
An exact feasible skeleton would show that the ten-square exclusion strategy cannot
dispose of that pose; it would not supply an eleven-square upper bound.
Neither result has been established by this inventory.

The next action is independent review of a completed design’s full alternative
inventory, using the domains above, and an explicit admission decision about its
additional geometric implication.
Until that decision and a separately frozen protocol, the new target remains unadmitted.
No favorable interval, missing outer cell or unchanged retry is licensed here.

## Work Receipt

This is session098 preparation within the coordinator’s documented September 7, 2026,
17:20–19:20 UTC block.
The assigned inventory stop is 17:30:00 UTC, including writing and checks.
The first actual clock was 17:21:21 UTC; initialization does not extend the stop.

I previously authored the BC281 adversarial report.
This inventory uses its subsequent independent acceptance and keeps the new BC282 design
unread, preserving separation from the current design author.
It performs source-scope comparison and exact coordinate translation of inherited
thresholds, not a search for a new implication.
No numerical target, solver, target sample, new scientific code, source replay, shared
record, Git operation, identifier or dependency change occurred.
Only this assigned report was written.

The scope comparison, full report readback and initial document checks completed at
17:26:36 UTC, 315 seconds after the first clock, before the fixed stop.
The common-document and de-slop passes were applied.
All four native link targets exist, the required footer occurs once and the whitespace
scan found no trailing blanks.
Installed Flowmark formatted only this assigned file with caching disabled; its scoped
auto-format check passed.
The interval table, premise qualifications and unresolved outcome survived readback.
A final scoped formatting check follows this receipt before terminal delivery.
No background command or mathematical continuation remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
