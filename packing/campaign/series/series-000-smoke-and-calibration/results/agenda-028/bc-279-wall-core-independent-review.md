# BC-279: Independent Audit of the Two Six-Core Results

**Both six-core certificates and the author’s fixed-insertion obstruction are accepted.
The seven-core model remains unresolved.** Each report supplies a different exact
arrangement of six maximal wall-conditioned cores at the same admitted four-square
configuration. Neither supplies seven cores or an upper capacity bound, even at that
fixed four-square configuration.

This is the reserved independent mathematical audit under session-092 phase 17, with
prospective lease 2026-09-07 12:14–12:34 UTC. The actual first clock was 12:14:12 UTC. I
read both frozen reports only after their terminalization:
[author](bc-279-wall-core-author.md) and [adversary](bc-279-wall-core-adversary.md).
Their calculations were independently reconstructed by hand against the complete
[native protocol](bc-279-wall-core-protocol.md), its
[mathematical admission](bc-279-wall-core-mathematical-review.md), and
[predicate admission](bc-279-wall-core-control-review.md).
No target reasoning was exchanged with either writer.

## Model, Source Domain, and Exact Claim Inventory

The model is unchanged: $q=96/25$, $b=1/2$, $d=167/50$, the entire four-pose $\Gamma_0$,
four independent actual angle variables, the original six complete selected-square SAT
clauses, all eight source guards, and seven independently variable residual centers.
Every residual center determines its own exact values

$$
r=\min(X,Y,q-X,q-Y),\qquad
a=\frac1{4\min(r,1/\sqrt2)},\qquad
K(r)=\operatorname{conv}(B_{1/2}\cup[-a,a]^2).
$$

The admitted identity with the intersection of all wall-compatible actual squares
remains the model’s justification.
At $r=1/2$, the body is the axis unit square; at and above $1/\sqrt2$, it is the disk.
The minimum graph retains every wall tie, and the two closed saturation branches agree
at their seam. The reports do not replace these exact graphs by favorable auxiliary
values.

For a unit normal $n$, put $L_n=|n_x|+|n_y|$. I used

$$
h_{K_j}(n)=\max(1/2,a_jL_n)
$$

to recompute each full threshold.
For a residual pair, the sum of these two maxima is the maximum of the four protocol
thresholds. For a selected square/core pair, $H_i(n)+h_{K_j}(n)$ is the maximum of the
two cross thresholds.
Therefore one displayed unit normal with projection at least the full support sum
verifies every required inequality for that pair on the **same** normal.
Both reports meet this quantifier requirement; neither checks hull components with
different normals.

Six residual cores require $\binom62=15$ mutual and $4\cdot6=24$ cross normals: 39
normals and $15\cdot4+24\cdot2=108$ support inequalities.
Each report supplies that complete inventory, in addition to the six selected-square SAT
certificates. Seven cores require 49 normals and 140 inequalities.
A seventh fixed insertion would add ten normals and 32 inequalities; the missing ten
cannot be inferred from the existing certificate.

The source guards are still those in the
[BC-277 domain](bc-277-boundary-band-domain-design.md).
No capacity, diameter, area, fitted pose box, contact graph, stationarity, or
common-angle condition has been added to $\Gamma_0$. Choosing equal angles at a single
control is legal and does not change the independent-angle domain.
All eleven actual squares and all 55 actual SAT clauses remain in the separate
full-square child $D_0$. The selected chart has $c_i\ge|s_i|$ and $c_i\ge1/\sqrt2>0$, so
$m_i=1/(2c_i)$ is precisely the original maximum-coordinate formula.
Both diagonal endpoint lifts, exact minimum and scatter ties, all eight closed failure
children, every label subset, and every weak order remain quantified.
The generic inclusion gives $\kappa_\square\le\kappa_{\rm wall}\le\kappa_{\rm disk}$; no
reverse implication is used.

## The Shared Four-Pose Control

Both reports use exactly the same centers, here in one denominator:

$$
C_0=(595,595)/850,\quad C_1=(1269,1113)/850,\quad
C_2=(1995,595)/850,\quad C_3=(2669,1113)/850,
$$

with $e=(4/5,3/5)$ and $f=(-3/5,4/5)$. Their actual angle lies strictly inside the
admitted chart. The coordinate support is $7/10$, and the extreme abscissae are $7/10$
and $157/50=q-7/10$. All other coordinates satisfy the same actual containment bounds.
The two heights are $7/10$ and $1113/850$; the latter is below the lower-band ceiling
$217/150$ by exactly $7/51$.

The ordered gaps are $337/425,363/425,337/425$. On pairs $01,12,23,02,13,03$, the
normals $e,-f,e,e,e,e$ give the projections

$$
1,\quad1,\quad1,\quad112/85,\quad112/85,\quad197/85.
$$

The support sums are one.
Thus all six selected pairs pass an actual SAT alternative, including the three legal
equalities. For example, pair 01 has displacement $(674,518)/850$, and its projection is
$(4\cdot674+3\cdot518)/4250=1$. Pair 12 similarly gives $(3\cdot726+4\cdot518)/4250=1$
on $-f$.

Direct substitution gives

$$
m_i=m=5/8,\quad\varepsilon=0,\quad\ell=7/10,\quad u=1113/850,
\quad\Delta=259/425,\quad A=41/40.
$$

The eight guards, in protocol order, are exactly

$$
259/425,\quad991/8500,\quad733/3400,\quad99/1000,\quad99/1000,
\quad3523/8500,\quad3003/8500,\quad3523/8500.
$$

All are positive. These independently checked values establish $G_A\in\Gamma_0$,
consistent with the
[accepted BC-278 control](bc-278-boundary-band-independent-review.md).
They establish no eleven-square completion.

## Exact Core Graphs in Both Reports

The source tables name the author’s centers $W_0,\ldots,W_5$ and the adversary’s centers
$R_0,\ldots,R_5$. I checked each against all four wall distances, not only the claimed
active distance. Every coordinate belongs to $[b,d]$.

| Index | Author $r$ and active wall | Author $a$ | Adversary $r$ and active wall | Adversary $a$ |
| --- | --- | --- | --- | --- |
| 0 | $5/8$, left/top tie | $2/5$ | $3/5$, left | $5/12$ |
| 1 | $49/40$, top | $\sqrt2/4$ | $129/100$, top | $\sqrt2/4$ |
| 2 | $5/8$, top | $2/5$ | $3/5$, left/top tie | $5/12$ |
| 3 | $5/8$, right | $2/5$ | $3/5$, top | $5/12$ |
| 4 | $5/8$, left | $2/5$ | $1/2$, right | $1/2$ |
| 5 | $38/25$, right | $\sqrt2/4$ | $57/50$, right | $\sqrt2/4$ |

For instance, the author’s $W_1$ has wall distances $893/600,523/200,1411/600,49/40$;
the last is the minimum.
Its $W_5$ has minimum $q-58/25=38/25$, smaller than its vertical distances.
The adversary’s $R_4$ has right distance $1/2$ and top distance $3/5$, giving a full
axis-square core.

Below saturation, $4ar=1$ holds with $r^2<1/2$ in every displayed case.
Above saturation, each reported $r$ exceeds one, and the specified positive radical
$a=\sqrt2/4$ satisfies $8a^2=1$. Thus there are no ambiguous algebraic root choices.
The two exact wall-minimum ties and the $r=1/2$ endpoint are retained.
All translated cores are contained by the admitted inclusion; saturation removes only
redundant box thresholds, not disk or selected-square separation conditions.

## All Mutual Certificates

The following are my recomputed projection-minus-full-support margins on each report’s
stated normal. This table covers all 15 unordered pairs in each report.
Write

$$
\mu=\frac{79\sqrt7-205}{2400}>0.
$$

| Pair | Author margin | Adversary margin |
| --- | --- | --- |
| 01 | $\mu$ | $1/750$ |
| 02 | $109/150$ | $6/25$ |
| 03 | $159/100$ | $37/50$ |
| 04 | $43/200$ | $87/50$ |
| 05 | $139/200$ | $11/10$ |
| 12 | $\mu$ | $19/375$ |
| 13 | $109/150$ | $1/375$ |
| 14 | $27/2600$ | $21/25$ |
| 15 | $193/3000$ | $1/5$ |
| 23 | $\mu$ | $37/50$ |
| 24 | $109/150$ | $87/50$ |
| 25 | $53/200$ | $11/10$ |
| 34 | $159/100$ | $0$ |
| 35 | $11/200$ | $187/7500$ |
| 45 | $139/200$ | $0$ |

For the author’s three upper adjacent pairs, $c_*=(5+\sqrt7)/8$ and $s_*=(5-\sqrt7)/8$
are positive, $c_*^2+s_*^2=1$, and $c_*+s_*=5/4$. The displacement has horizontal
magnitude $259/300$ and vertical magnitude $3/5$. Hence its stated normal gives

$$
c_*\frac{259}{300}+s_*\frac35
=\frac{2195+79\sqrt7}{2400}=1+\mu.
$$

The hull support is exactly $1/2$ on these normals since $(2/5)(5/4)=1/2$. The strict
radical comparison is exact: $7\cdot79^2-205^2=1662>0$, with both compared quantities
positive. The other non-axis normals use the integer triples $(5,12,13)$, $(3,4,5)$, and
$(7,24,25)$, so their unit lengths are exact as well.

The nontrivial support sums also check.
The author’s pair 14 has $1/2+(2/5)(17/13)=133/130$, and pair 35 has
$1/2+(2/5)(7/5)=53/50$. The adversary’s $a=5/12$ hull gives sums $61/60$ against a disk
on a normal of absolute-coordinate sum $31/25$, and $13/12$ when that sum is $7/5$. Its
pair 45 instead uses the full axis-square support $31/50$ plus disk support $1/2$,
giving $28/25$, exactly its projection.

All remaining coordinate-normal sums are one.
Thus every entry certifies all four inequalities of its pair on the displayed common
normal. The author’s 15 mutual pairs are strict; the adversary’s pairs 34 and 45 touch
legally. Neither equality is a failure or a missing branch.

## All Cross Certificates

Every cross calculation uses the actual selected-square support.
On a coordinate axis it is $7/10$; on $\pm e,\pm f$ it is $1/2$. Every core has
coordinate-axis support $1/2$. The grouped entries below give the smallest margin in
their group, so they check each pair represented there.

| Author cross group $(i,j)$ | Count | Recomputed full-support margin |
| --- | --- | --- |
| Every selected $i$, $j=0,1,2,3$ | 16 | $359/3400$ |
| $(0,4)$ | 1 | $1/10$ |
| $(1,4)$ | 1 | $9/680$ |
| $(2,4)$ | 1 | $71/136$ |
| $(3,4)$ | 1 | $263/200$ |
| $(0,5)$ | 1 | $1/20$ |
| $(1,5)$ | 1 | $391/8500$ |
| $(2,5)$ | 1 | $69/4250$ |
| $(3,5)$ | 1 | $19/4250$ |

For example, the first group has smallest projection $523/200-1113/850=4439/3400$ and
threshold $6/5$. The close $(1,4)$ row gives $3649/3400$ on $f$ and uses the full sum
$1/2+14/25=53/50$, not the disk-only threshold one.
The final three rows use saturated core 5, so their threshold on the actual selected
normal is exactly one.

| Adversary cross group | Count | Recomputed full-support margin |
| --- | --- | --- |
| $R_1$ against all selected squares | 4 | $69/1700$ |
| $R_2,R_3,R_4$ against all selected squares | 12 | $621/850$ |
| $R_0$ against $C_0,C_2$ | 2 | $1/10$ |
| $R_0$ against $C_1$ | 1 | $1/204$ |
| $R_0$ against $C_3$ | 1 | $67/50$ |
| $R_5$ against $C_0,C_2$ | 2 | $9/25$ |
| $R_5$ against $C_1$ | 1 | $1139/2125$ |
| $R_5$ against $C_3$ | 1 | $52/2125$ |

The close $R_0,C_1$ row has displacement $(-759,587)/850$ and projection
$(3\cdot759+4\cdot587)/4250=37/34$ on $f$. Its full support sum is $1/2+7/12=13/12$,
leaving $1/204$. The last two rows use an actual selected normal and a saturated disk;
their projections $3264/2125$ and $2177/2125$ both exceed one.

Each table totals 24 cross pairs, with no overlap or omission in the groups.
Every listed margin is positive and verifies both cross inequalities on the same normal.
Together with the mutual tables, this accepts all 39 normals and 108 support
inequalities in each report.
The resulting conclusion is $\kappa_{\rm wall}(G_A)\ge6$ from two independently
constructed controls.
No actual orientation has been supplied for the six residual full squares.

## Source Localization and the Author’s Strict Insertion Cover

The insertion argument uses a necessary center region derived from the unchanged source
guards. It does not add a fitted restriction to the target.
I rechecked the localization from the
[BC-278 audit](bc-278-boundary-band-independent-review.md).

The selected guard octagons are distinct from the residual cores.
Their section radius at virtual row height $v$ is $\min(A,A+k-|Y-v|)$ on $|Y-v|\le A$.
The guards imply $0\le\Delta\le A-k$ and $u-A\le b\le\ell$. On the common row interval
$[u-A,\ell+A]$, both section radii are at least $k$. Their sum is concave in height,
with value $2k+\Delta$ at both endpoints, so it is at least that value throughout.
The three gap guards join consecutive intervals; the endpoint guards extend their union
to $b$ and $d$. Thus

$$
[b,d]\times[b,\ell+A]\subseteq\bigcup_i\mathcal O_i.
$$

The closed auxiliary octagon $E$ has vertex squared norm $249401/1000000<1/4$. Since
each selected diamond lies in its actual square, the accepted inclusion of each
$\mathcal O_i$ into that diamond plus $E$ puts even its boundary inside the strict
forbidden region for a residual incircle.
This is why legal square/disk touching does not leave an exception on a guard boundary.
Any additional core contains its incircle, so at $G_A$ its center has $Y>\ell+A=69/40$.
The author’s closed rectangle $\mathcal R=[b,d]\times[69/40,d]$ safely contains every
remaining possible center.

I checked every vertical bound, squared-radius sum, interval overlap, and extreme
endpoint in the three-strip cover:

| Closed strip | Centers used | Squared-distance upper bounds | Consecutive horizontal overlaps |
| --- | --- | --- | --- |
| $[69/40,49/20]$ | $W_4,W_5,W_3$ | $9946/10000, 2474/2500, 9946/10000$ | $11/200, 83/200$ |
| $[49/20,543/200]$ | $W_0,W_1,W_2,W_3$ | $37809/40000, 39505/40000, 37809/40000, 39505/40000$ | Each $43/60$ |
| $[543/200,167/50]$ | $W_0,W_2,W_3$ | $39929/40000, 39929/40000, 39521/40000$ | $1/300, 409/600$ |

The halfwidths and vertical bounds are exactly those displayed in the author report.
In particular, the highest strip uses halfwidth $173/200$ about $W_0,W_2$; its squared
bound is $(173/200)^2+(1/2)^2=39929/40000$. Their center gap is $259/150$, so the
overlap is $173/100-259/150=1/300>0$.

The extreme horizontal interval endpoints in the three strips are respectively

$$
(-53/200, 733/200),\qquad
(1/40, 839/200),\qquad
(-6/25, 779/200).
$$

Each pair extends beyond both $b$ and $d$. Consequently every point of the **closed**
rectangle lies strictly inside an open unit-radius disk about some $W_j$. The smallest
certified squared-distance margin is $71/40000>0$. All strip endpoints and both shared
seams are covered; no strict endpoint selector is used.

A new residual core there would have its incircle at distance less than one from an
existing incircle.
Their interiors overlap, and the unit-normal Cauchy bound prevents the
necessary projection threshold one.
Therefore a seventh core cannot be appended to this fixed six-core arrangement.
This implication is accepted on the whole possible insertion-center domain.

It is **insertion maximality**, not a maximum-cardinality result.
It fixes all six existing centers.
The unit-radius disks are forbidden neighborhoods of those centers, not a partition into
six regions of capacity one.
Rearranging the existing cores changes the neighborhoods.
No upper bound on $\kappa_{\rm wall}(G_A)$ or on the whole $\Gamma_0$ follows.

## Adversary’s Additional Necessary Statements

The specified failed insertion is accepted.
For the old disk center $(58/25,39/20)$ and $R_5=(27/10,113/50)$, the squared distance
is

$$
(19/50)^2+(31/100)^2=481/2000<1.
$$

The incircles overlap, so no pair normal can repair this insertion.
This tests one center against one fixed arrangement; it is not the author’s complete
insertion cover and does not exclude other insertions into the adversary’s arrangement.

The generic wall-edge condition is also sound.
For $1/2\le r\le1/\sqrt2$, $r+a-1=(2r-1)^2/(4r)\ge0$. Above saturation,
$r+a\ge3/(2\sqrt2)>1$, since $9>8$. A top-wall-minimum core therefore has lower box edge
$Y-a=q-(r+a)\le q-1$; a right-wall-minimum core has left box edge $X-a\le q-1$.

If the top core’s center is weakly above and left of the right core’s center, their
positive-halfside axis boxes can avoid interior overlap only by separating in the
ordered horizontal direction or the ordered vertical direction.
Substitution of the two preceding edge bounds gives exactly

$$
X_{\rm top}+a_{\rm top}\le q-1
\quad\text{or}\quad
Y_{\rm right}+a_{\rm right}\le q-1.
$$

This remains necessary at equality and wall-minimum ties.
It also applies to the contained axis box of a saturated disk.
It is a conditional necessary statement, with no residual-count implication.

## Reflection, Accepted Scope, and Remaining Obligation

Joint reflection sends every selected and residual center by $(X,Y)\mapsto(X,q-Y)$, and
every normal and displacement by $(n_x,n_y)\mapsto(n_x,-n_y)$. It preserves $r,a$,
normal length, core supports, and all dot products.
The actual selected angles change sign.
The upper guards use inward depths, so their values agree.
The insertion rectangle and its strict disk cover reflect together.
All accepted conclusions therefore transfer to the jointly reflected configurations.

This map preserves closed band representatives, even when it changes their lower-index
counting owner.
Angle endpoint lifts, wall-minimum and saturation seams, every four-label
subset, weak order, eight guard-failure siblings, and the accepted central remainder
stay in the original parent cover.
Neither report prunes any of them.
A reflection of selected poses alone is insufficient.

| Implication | Independent disposition |
| --- | --- |
| Shared exact $G_A\in\Gamma_0$ | Accepted, with all actual containment, six selected SAT clauses, and eight guards |
| Author’s six exact maximal wall cores | Accepted: every graph and all 39 common-normal certificates |
| Adversary’s different six exact maximal wall cores | Accepted: every graph and all 39 common-normal certificates, including two legal mutual contacts |
| No seventh core appended to the fixed author arrangement | Accepted over every possible insertion center, by strict three-strip coverage |
| Adversary’s named insertion refusal and conditional wall-edge lemma | Accepted with their stated fixed or conditional scopes |
| Uniform capacity below six | Refuted by either six-core control |
| Capacity at most six at $G_A$ or throughout $\Gamma_0$ | Unresolved; fixed-insertion maximality does not imply it |
| Seven-core witness, or emptiness of $\mathcal M_7$ | Neither established |
| Eleven actual squares in $D_0$, or exclusion of that full-square child | Neither established |
| Strict H118 comparison or failure of the entire class of maximal/smaller wall-core models at the seven-body threshold | Not established by these six-core results |

No mathematical error was found in either report’s stated partial claims.
The stronger implications refused above are also explicitly disclaimed by the writers.
The exact unresolved question is whether there exists a $G\in\Gamma_0$ and seven centers
satisfying all 49 complete normal predicates with their exact graphs; an exclusion must
rule out every such choice.
No complete treatment or seven-core witness appears in the frozen reports.
The maximal common-core identity alone does not settle that question, and a matched
strongest coupled-LP survival witness with its nonlinear guard policy remains absent for
strict H118 comparison.

The next action is coordinator disposition of these accepted partial controls and the
unresolved target. This audit authorizes no continuation, narrower target, different
model, or solver allocation.

## Work Receipt

Actual first clock: **2026-09-07 12:14:12 UTC**. Mathematical verification and the
complete report readback froze at **12:24:04 UTC**, an elapsed **592 seconds**. The
final document freeze clock was **2026-09-07 12:25:43 UTC**, **691 seconds** after the
actual start, before the **12:34 UTC** hard stop.
The complete protocol and both reports were read; the original guard formulas, prior
localization, and admitted model predicates were checked against native sources.
Every claimed graph value and certificate inequality was reconstructed by hand.
No numerical target, script, solver, resource search, new target proof, author
coordination, source edit, Git mutation, shared-record edit, identifier, or dependency
change was performed.
Only this assigned report was written.
The common-document and prose passes were applied.
Installed Flowmark 0.4.0 formatted this file and passed its no-cache check.
All seven native source targets exist, the required footer occurs once, and the
trailing-whitespace and malformed-math-token scans found no matches.
The final receipt receives the same scoped formatting check before terminal delivery.
No mathematical work resumes after the stated freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
