# BC-278: Independent Audit of the Boundary-Band Results

**Accepted as exact model obstructions; the full-square determination remains
unresolved.** The [author](bc-278-boundary-band-author.md) supplies an admitted rational
four-pose configuration with seven valid residual disks.
This disproves the proposed uniform bounds of six in both the disk and octagon models.
The same seven centers cannot support seven contained full unit squares.
The author’s perturbation also establishes a nontrivial open family of independently
oriented selected poses admitting the seven disks.

The [adversary](bc-278-boundary-band-adversary.md) independently supplies another
admitted configuration with seven centers strictly outside all closed guard octagons.
Its stated disk-overlap refusal is correct.
That construction is an octagon witness only; it is not a disk or full-square witness.

Neither result excludes or populates the full eleven-square child $D_0$. Neither
determines an exact capacity.
No H118 comparison with a matching coupled LP follows.
The adversary’s suggestion that a uniform disk bound of six might be the next route is
superseded by the author’s stronger obstruction.

## Frozen Domain and Uniform Localization

I read the unchanged [protocol](bc-278-boundary-band-protocol.md), the
[admitted domain](bc-277-boundary-band-domain-design.md), and both terminal reports.
The question remains the whole closed eight-guard domain at $q=96/25$, with $b=1/2$,
$d=167/50$, all actual independent angles modulo quarter turns, all eleven containment
conditions and all 55 complete weak SAT disjunctions.
The split remains six selected-pair, 28 cross-pair and 21 residual-pair conditions.
The examples choose legal values of independent selected angles; they impose no
common-angle restriction on the domain.

The author’s localization lemma is accepted uniformly.
The first two guards give $0\le\Delta\le A-k$. Both row means are at least $b$, and
attachment gives $u-A\le b$. Thus $[b,\ell+A]$ lies in the common row interval
$[u-A,\ell+A]$. On that interval each row section has radius at least $k$, and the sum
of alternating radii is at least $2k+\Delta$: it is concave in height and has endpoint
values $k+(k+\Delta)$. The three gap guards connect consecutive sections.
The two endpoint guards extend their union to both $b$ and $d$. Consequently

$$
[b,d]\times[b,\ell+A]\subseteq\bigcup_iK_i.
$$

The accepted strict incircle inclusion puts even the closed $K_i$ inside the actual
disk-forbidden region.
Every legal disk or actual-square center therefore has $Y>\ell+A$, including at legal
touching configurations.
This strict conclusion is not asserted for the octagon relaxation, which permits guard
boundary points.

For $\ell+A<Y\le u+A$, only the two high-row guards remain.
Their radius is at least $k$, so the rightmost reaches $d$ by $x_3-d+k\ge0$. A center
avoiding the closed guards must be left of the first high-row interval or between the
two. These are potential passages of the guard geometry, not a proof of actual disk or
square paths through the corresponding larger obstacles.
The high-row radii decrease toward $k$ on this height range, and the guards end at
$u+A$. The already admitted bound $u+A<779/300<d$ leaves the upper region beyond this
barrier. No capacity-six conclusion is licensed by this localization.

## Author: Exact Four-Pose Membership

Write $G_A$ for the author’s configuration, distinguishing it from the adversary’s
different configuration.
The displayed $e=(4/5,3/5)$ and $f=(-3/5,4/5)$ form an orthonormal basis at an actual
angle strictly inside the admitted chart.
Their coordinate support is $7/10$ and their core radius is $5/8$.

In common denominator 850 the selected centers are

$$
C_0=(595,595)/850,\quad C_1=(1269,1113)/850,\quad
C_2=(1995,595)/850,\quad C_3=(2669,1113)/850.
$$

This reproduces the author’s coordinates, ordered gaps $337/425,363/425,337/425$, and
row difference $259/425$. The extreme horizontal wall distances and low row heights
equal $7/10$ exactly, so their containment contacts are legal.
Every other wall inequality holds.
The high-row lower-band margin is $217/150-1113/850=7/51>0$.

The six chosen directed projections, in pair order $01,12,23,02,13,03$, are

$$
1,\quad1,\quad1,\quad112/85,\quad112/85,\quad197/85.
$$

For the adjacent pairs the relevant numerators are $4(337)+3(259)=2125$ and
$3(363)+4(259)=2125$, over denominator 2125. For pair 03 the numerator is
$4(1037)+3(259)=4925$, giving $197/85$. The directed normals are the actual
$e,-f,e,e,e,e$, whose parallel-square support sums are one.
One satisfied alternative proves each complete pair disjunction; no unused alternative
is removed. The three equalities are valid square contacts.

Direct substitution gives $\varepsilon=0$, $A=41/40$, $R=331/250$, and the eight guard
values

$$
259/425,\quad991/8500,\quad733/3400,\quad99/1000,\quad99/1000,
\quad3523/8500,\quad3003/8500,\quad3523/8500.
$$

All are positive. In particular $A-k=363/500$, and the common gap allowance is
$2k+\Delta=10263/8500$, which verifies the stated gap margins.
Thus $G_A\in\Gamma_0$. Its barrier and high-row top are $69/40$ and $7937/3400$. The
four-pose membership does not assert an eleven-square completion.

## Author: All Seven Disks and 49 Separation Checks

The seven disk coordinates are exactly those in the author table.
Each coordinate lies in $[b,d]$. The lowest height is $617/340$, whose excess above the
barrier is $617/340-69/40=61/680>0$; the other low center has excess $9/40$. Thus the
localization and all closed disk-containment conditions are respected.

### All 21 disk pairs

I checked the four pairs requiring both coordinates:

| Pair | Squared distance | Excess over one |
| --- | --- | --- |
| $03$ | $11765/10000$ | $1765/10000$ |
| $13$ | $10088/10000$ | $88/10000$ |
| $24$ | $10081/10000$ | $81/10000$ |
| $35$ | $2894450/2890000$ | $4450/2890000$ |

For pair 35 the exact differences are $1207/1700$ and $1199/1700$;
$1207^2+1199^2=1456849+1437601=2894450$. The other 17 pairs have the following
single-coordinate certificates, each at least one:

| Pairs | Certified absolute coordinate differences, in the same order |
| --- | --- |
| $01,02,04,05,06$ | $129/100,229/100,71/25,2593/1700,91/50$ |
| $12,14,15,16$ | $1,31/20,129/100,139/100$ |
| $23,25,26$ | $79/50,229/100,139/100$ |
| $34,36,45,46,56$ | $213/100,111/100,71/25,51/50,91/50$ |

The certificates for 05, 16 and 26 use the vertical coordinate; the remaining ones use
the horizontal coordinate.
This partitions all 21 pairs without duplication.
Only pair 12 is tight.
Its distance-one contact is legal.

### All 28 disk-to-square pairs

In the selected orthonormal basis, the distance from a point with relative coordinates
$(a,c)$ to the closed square is

$$
\sqrt{(|a|-1/2)_+^2+(|c|-1/2)_+^2}.
$$

A distance of at least $1/2$ is exactly the needed disk avoidance condition.
A unit normal projection of at least one is sufficient because the square and disk
supports on that normal are both $1/2$. This threshold is not substituted for a full
residual square’s actual support.

The author’s grouping is exhaustive, with the following independently checked values:

| Disk-square group | Count | Certificate |
| --- | --- | --- |
| $P_0,P_1,P_2$ against all four squares | 12 | Disk bottoms exceed the maximum selected top $854/425$ by $353/425$ |
| $P_3$ against all four squares | 4 | Vertical gap $101/50-854/425=9/850$ |
| $P_4$ against $C_0,C_2$ | 2 | Vertical gap $3/5$ |
| $P_4$ against $C_1$ | 1 | Horizontal gap $11/17$ |
| $P_4$ against $C_3$ | 1 | Exact corner-distance check below |
| $P_5$ against $C_2,C_3$ | 2 | Horizontal gaps $11/17,36/25$ |
| $P_5$ against $C_0$ | 1 | $f$ projection $86/85>1$ |
| $P_5$ against $C_1$ | 1 | $(a,c)=(-167/340,1)$; exact legal distance $1/2$ |
| $P_6$ against $C_0$ | 1 | Vertical gap $1/20$ |
| $P_6$ against $C_1,C_2,C_3$ | 3 | Normal projections $8891/8500,4319/4250,4269/4250$, all greater than one |

For the corner pair, $P_4-C_3=(1/5,506/425)$ gives normal coordinates
$1858/2125,1769/2125$. Subtracting $1/2$ gives $1591/4250,1413/4250$. Their squared
distance is

$$
\frac{1591^2+1413^2}{4250^2}
=\frac{2531281+1996569}{18062500}
=\frac14+\frac{12225}{18062500}>\frac14.
$$

For the tight $P_5,C_1$ pair, $|-167/340|<1/2$ verifies that the stated distance is
exactly $1/2$, not merely a projection bound.
It is the sole tight cross condition.
These 28 checks, the 21 disk-pair checks and containment establish

$$
\kappa_{\rm disk}(G_A)\ge7,
\qquad \kappa_{\rm oct}(G_A)\ge7.
$$

The second implication uses the admitted inclusion into the weaker octagon model.
The first already uses the actual selected squares and exact disk geometry.
Both are lower bounds, not exact capacity evaluations.

## Author: Perturbation and Fixed-Center Lifting Refusal

The positive-$\eta$ argument is accepted as stated.
The three formerly tight selected projections change by $2\eta/5,8\eta/5,2\eta/5$.
Moving the extreme selected abscissae inward and raising the low centers makes all
formerly tight selected wall conditions strict.
The simultaneous change of $C_1$ by $(0,3\eta)$ and $P_5$ by $(0,4\eta)$ raises their
tight $f$ projection to $1+4\eta/5$.

Every other selected-pair, wall, band, ordering, guard and cross condition starts strict
and is continuous. Every disk pair affected by moving $P_5$ starts strict as well,
including the close pair 35. Disk containment continues for sufficiently small positive
$\eta$. Pair 12 is unchanged and remains legally tight.
A finite collection of these strict conditions persists on some positive interval; an
explicit numerical neighborhood is not needed for this existence conclusion.

Fix one such positive $\eta$. All selected-pose and cross conditions are then strict,
and the seven disk centers may be held fixed.
Continuity permits independent changes of all four selected actual angles and centers,
including nonzero row scatter.
For a selected pair, retain the chosen edge axis of one owning square and evaluate the
actual support sum of both squares.
These quantities vary continuously with the two angles; the parallel-square support sum
one is not kept as a premise after they change.
Minima and maxima in the guards are continuous, so their ties do not obstruct the
argument. This proves an open family of selected poses admitting those disks.
It does not claim an open family of all disk coordinates, since the unchanged disk pair
still touches.

The fixed-center full-square refusal is also accepted.
A contained unit square centered on $Y=d$ must satisfy

$$
\frac{|\cos\theta|+|\sin\theta|}{2}\le q-d=1/2.
$$

The opposite inequality always holds.
Equality forces $|\cos\theta\sin\theta|=0$, hence axis alignment modulo quarter turns.
The same argument applies at $X=d$. Therefore full squares centered at $P_2$ and $P_4$
must both be axis aligned.
Their absolute displacement coordinates are $11/20$ and $21/25$, both less than one.
Every directed axis alternative is then less than the support sum one; all eight SAT
alternatives fail. Their interiors overlap despite their legal disk squared distance
$10081/10000$.

The perturbation leaves $P_2$ and $P_4$ unchanged, so this refusal also applies to the
displayed perturbed disk-center family.
It does not exclude other residual center choices at $G_A$ or anywhere else in
$\Gamma_0$.

The author’s common-core observation is correct with its stated limitation.
The intersection of all centered unit-square orientations is the closed radius-$1/2$
disk: that disk lies in each orientation, and any point of larger norm is excluded by an
orientation having an edge normal in its radial direction.
Thus enlarging a fixed inner core beyond the incircle cannot be valid for every residual
angle. Refining an individual-obstacle approximation up to the exact
selected-square-plus-disk obstacle cannot reject this seven-disk configuration.
This does not rule out joint or orientation-dependent full-square arguments, or other
methods using stronger premises.

## Adversary: Exact Octagon Obstruction and Disk Refusal

Write $G_O$ for the adversary’s distinct selected configuration and $r=\sqrt3$. The
basis at $\pi/6$ has support $h=(r+1)/4$ and actual core radius $m=r/3$. The endpoint
square comparisons give exactly

$$
3-(69/40)^2=39/1600>0,\qquad (87/50)^2-3=69/2500>0.
$$

Hence $69/40<r<87/50$, $23/40<m<29/50$, and $h<137/200<7/10$. These bounds verify strict
containment of all four displayed selected squares.
Their band clearance is $2/25$, with ordered gaps $39/50,17/20,39/50$.

The six stated actual-axis SAT projections are correct.
The first and third exceed $12073/12000>1$; the middle adjacent projection exceeds
$17/40+23/40=1$. The two same-row projections exceed $11247/8000>1$, and the last equals
the sum of the first and a same-row projection.
All selected pairs are strictly separated.
Their chosen valid alternatives establish the complete disjunctions.

The eight guard values are exactly

$$
2/3,\quad m-1697/3000,\quad m-7/15,\quad99/1000,\quad69/1000,
\quad727/1500,\quad311/750,\quad727/1500.
$$

The two variable values exceed $7/750$ and $13/120$, respectively.
Thus $G_O\in\Gamma_0$ with strict selected-pose and guard margins.

All seven listed centers are in $[b,d]^2$. For the six centers in the upper two rows,
their minimum height exceeds the high guard top by $7/12-m>1/300$. This checks 24
octagon avoidances. The remaining center $P_0$ is above both low guards by $3/5-m>1/50$,
and its horizontal distance from the first high guard is $49/50>A$; the last high guard
is farther right. This checks its other four avoidances.
Every one of the 28 avoidances is strict with respect to the closed $K_i$, so permitting
guard boundaries is not responsible for the witness.

The five pair groups have sizes $3,3,9,3,3$, totaling 21. Within the middle row the
distances are $1,1,2$; within the top row they are $13/10,13/10,13/5$. Between those
rows the vertical difference is $99/100$ and the minimum horizontal difference is $1/5$,
giving squared distance at least $10201/10000$. From $P_0$ to the middle row the lower
squared-distance bound is $(4/5)^2+(13/20)^2=17/16$; from $P_0$ to the top row the
vertical difference is $41/25>1$. This exhaustively proves $\kappa_{\rm oct}(G_O)\ge7$.

The claimed disk refusal uses $P_1-C_1=(-9/50,59/60)$. Its actual normal coordinates are

$$
\alpha=59/120-9r/100,\qquad
\beta=9/100+59r/120.
$$

The source bounds imply $0<\alpha<1/2$ and $1/2<\beta<39/40<1$. Therefore the
point-to-square distance is $\beta-1/2<1/2$. Moving the nearest face point a
sufficiently small positive distance into the square keeps it inside the open disk.
This is strict interior overlap.
Every centered full unit square contains that open incircle in its interior, so no
residual orientation at that center repairs the cross-pair failure.

This proves failure of the displayed disk interpretation and fixed-center full-square
interpretation. It does not prove that $G_O$ admits no other seven disks or squares.
The author’s stronger result occurs at a different admitted $G_A$; the two reports are
consistent.

## Joint Reflection and Final Scope

Reflect each selected square and every displayed residual center by
$(X,Y)\mapsto(X,q-Y)$, and negate each selected actual angle.
This is the accepted joint isometry: it preserves containment, actual-square geometry,
disk distances, SAT certificates, guard values in inward depth, and both fixed-center
lifting refusals. For the author the selected reflected heights are indeed $157/50$ and
$2151/850$. The adversary’s configuration transfers by the same map.
Both model obstructions therefore also occur in the reflected upper family.

Reflection acts on closed parent branches, not the seam-counting assignment.
All original endpoint lifts, counting seams, label subsets, weak orders, eight failure
siblings and the central remainder are retained.
No full-square success child is pruned by these partial results.

The combined accepted and unresolved implications are:

| Implication | Independent disposition |
| --- | --- |
| Uniform actual-disk and actual-square center localization $Y>\ell+A$ | Accepted, including weak guard boundaries |
| Seven disks at $G_A$, and on a nontrivial family of independently oriented selected poses | Accepted |
| Uniform disk or octagon upper bound of six on unchanged $\Gamma_0$ | Refuted by the author’s exact control |
| Seven centers strictly outside closed octagons at $G_O$ | Accepted independently |
| Adversary centers as disks or full squares | Refused by the stated strict cross overlap |
| Author’s fixed disk centers as seven contained full squares | Refused by wall-forced axis-square overlap |
| Whole $D_0$ exclusion or an eleven-square witness in $D_0$ | Unresolved; neither report supplies it |
| Exact capacities, unrestricted n11 coverage, or strict H118 strength over a matching coupled LP | Not established |

The smallest remaining full-square obligation is unchanged: either exclude every
seven-square extension throughout the admitted $\Gamma_0$, with actual wall supports and
all cross and mutual SAT conditions, or give one exact eleven-square packing in that
domain. The accepted disk obstruction rules out a uniform disk capacity-six route under
the same model and domain.
Any subsequent attempt needs a prospective checkpoint decision; this audit does not
supply a new target, narrowed domain or retry.

## Work Receipt

The prospective session-092 phase-13 lease was 10:33:33–10:53:33 UTC on 2026-09-07. The
actual first clock read was 10:35:13 UTC, after both writers had terminalized.
I coauthored neither target argument and read neither while it was evolving.
This audit used the frozen protocol, admitted domain and both completed reports.
All target arithmetic and geometric checks were reconstructed by hand.
No numerical target, solver, one-off target script, resource search or unused scratch
control was run or consulted.
Only this assigned review was written; no source report, Git state, shared record,
identifier or dependency was changed.

The complete mathematical readback, including the independent-angle support
clarification, and document checks ended at 10:45:39 UTC, an elapsed 10 minutes 26
seconds from the actual first clock read.
The common-document and prose-editing passes were applied.
Installed Flowmark 0.4.0 formatted this file and passed its scoped check with caching
disabled. All four linked source files exist; the trailing-whitespace scan found no
matches, and the required footer appears once.
A final scoped formatting check follows this receipt before handoff, within the 10:53:33
UTC hard deadline. No target work continues after this audit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
