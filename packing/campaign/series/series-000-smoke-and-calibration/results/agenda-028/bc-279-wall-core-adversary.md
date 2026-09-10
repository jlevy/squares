# BC-279 Adversary: Six Exact Wall Cores; the Seven-Core Question Remains Open

**Partial result: the admitted four-pose control supports six maximal wall cores.** The
certificate below supplies their exact clearance graphs, all 15 mutual separators and
all 24 selected-square cross separators.
It proves $\kappa_{\rm wall}(G_A)\ge6$. No seventh core or uniform upper bound is
established. The whole frozen question $\mathcal M_7=\varnothing$ remains unresolved.

This independent attempt follows the [BC279 protocol](bc-279-wall-core-protocol.md), its
[predicate admission](bc-279-wall-core-control-review.md), and the
[accepted BC278 source control](bc-278-boundary-band-independent-review.md).
The coordinator reports protocol checkpoint `52b1b43e` and runnable-record correction
`d11b866f`, with all 31 record steps passing before dispatch.
This report changes no model condition.
It uses the exact maximal hull, one normal per pair shared by all support components,
actual selected angles, legal touching and all original guards.

## Exact Selected Four-Pose Membership

Use the BC278 author configuration $G_A$ with the actual common basis

$$
e=(4/5,3/5),\qquad f=(-3/5,4/5),
$$

and selected centers

$$
C_0=(595,595)/850,\quad C_1=(1269,1113)/850,\quad
C_2=(1995,595)/850,\quad C_3=(2669,1113)/850.
\tag{1}
$$

This is one legal choice of the four independent angle variables, not a restriction on
$\Gamma_0$. The normals are orthonormal, with $4/5\ge3/5\ge0$, so the actual angle is
inside the admitted chart.
Coordinate support is $h=7/10$ and the selected diamond core radius is $m=5/8$. The
extreme abscissae are $7/10$ and $157/50=q-7/10$; every ordinate and remaining abscissa
is between these bounds.
The selected squares are contained, including their legal wall contacts.
Their heights $7/10$ and $1113/850$ belong to the lower band.

The ordered gaps are $337/425,363/425,337/425$. For selected pairs $01,12,23,02,13,03$,
choose directed normals $e,-f,e,e,e,e$, respectively.
Their projections are

$$
1,\quad1,\quad1,\quad112/85,\quad112/85,\quad197/85.
$$

Both actual square supports on each selected normal are $1/2$. Thus one complete-SAT
alternative holds for each of the six pairs; the three equalities are legal contacts.
No other alternative is discarded from the domain.

Direct substitution gives $\varepsilon=0$, $\ell=7/10$, $u=1113/850$, $\Delta=259/425$,
and $A=41/40$. The eight guards, in protocol order, are

$$
259/425,\quad991/8500,\quad733/3400,\quad99/1000,\quad99/1000,
\quad3523/8500,\quad3003/8500,\quad3523/8500.
$$

They are all positive.
These values and the six actual pair certificates re-establish $G_A\in\Gamma_0$. They
assert no eleven-square completion.

## Six Centers and Their Exact Cores

Write $R_0,\ldots,R_5$ for the six residual centers, distinguishing them from the old
BC278 disk labels. Keep $q=96/25$ and the exact graph $r_j=\min(X_j,Y_j,q-X_j,q-Y_j)$.

| Core | Center $R_j$ | $r_j$ | $a_j$ | Active clearance |
| --- | --- | --- | --- | --- |
| 0 | $(3/5,2)$ | $3/5$ | $5/12$ | Left wall |
| 1 | $(3/2,51/20)$ | $129/100$ | $\sqrt2/4$ | Top wall, saturated core |
| 2 | $(3/5,81/25)$ | $3/5$ | $5/12$ | Left and top tie |
| 3 | $(117/50,81/25)$ | $3/5$ | $5/12$ | Top wall |
| 4 | $(167/50,81/25)$ | $1/2$ | $1/2$ | Right wall |
| 5 | $(27/10,113/50)$ | $57/50$ | $\sqrt2/4$ | Right wall, saturated core |

All coordinates belong to $[1/2,167/50]$. For cores 0, 2 and 3, $4(5/12)(3/5)=1$ and
$r^2=9/25<1/2$. For core 4, $4(1/2)(1/2)=1$. For cores 1 and 5, $r>1>1/\sqrt2$ and the
positive value $a=\sqrt2/4$ satisfies $8a^2=1$. Here $\sqrt2$ denotes the unique
positive root of $z^2=2$. The saturated cores 1 and 5 are exactly disks; core 4 is the
full axis unit square.
The other three are the full disk/box hulls, not either component separately.

The displayed ties and all wall contacts are retained.
Core containment follows from the admitted generic inclusion, using these exact
clearances rather than midpoint or free halfside values.

## All 15 Mutual Pairs on Shared Unit Normals

For each $j<k$, the table gives one normal $n$ directed from $R_j$ toward $R_k$, the
exact projection $n\cdot(R_k-R_j)$, and the full support sum $T=h_{K_j}(n)+h_{K_k}(n)$.
A single projection at least $T$ proves all four protocol support inequalities on that
same normal.

| Pair | Unit normal $n$ | Projection | Full threshold $T$ |
| --- | --- | --- | --- |
| 01 | $(24/25,7/25)$ | $509/500$ | $61/60$ |
| 02 | $(0,1)$ | $31/25$ | $1$ |
| 03 | $(1,0)$ | $87/50$ | $1$ |
| 04 | $(1,0)$ | $137/50$ | $1$ |
| 05 | $(1,0)$ | $21/10$ | $1$ |
| 12 | $(-4/5,3/5)$ | $567/500$ | $13/12$ |
| 13 | $(4/5,3/5)$ | $543/500$ | $13/12$ |
| 14 | $(1,0)$ | $46/25$ | $1$ |
| 15 | $(1,0)$ | $6/5$ | $1$ |
| 23 | $(1,0)$ | $87/50$ | $1$ |
| 24 | $(1,0)$ | $137/50$ | $1$ |
| 25 | $(1,0)$ | $21/10$ | $1$ |
| 34 | $(1,0)$ | $1$ | $1$ |
| 35 | $(7/25,-24/25)$ | $651/625$ | $61/60$ |
| 45 | $(-7/25,-24/25)$ | $28/25$ | $28/25$ |

Every normal is unit: the non-axis integer triples are $(3,4,5)$ and $(7,24,25)$. On an
axis every core has support $1/2$. For normals with absolute component sum $31/25$, a
core with $a=5/12$ has support $31/60>1/2$, while a disk has support $1/2$; this gives
$61/60$. With absolute component sum $7/5$, that same hull has support $7/12$, giving
$13/12$ against a disk.
For pair 45, the axis-square support is $31/50$ and the disk support is $1/2$, giving
$28/25$.

The small positive margins are exact: pair 01 has margin $1/750$, pair 13 has margin
$1/375$, and pair 35 has margin $187/7500$. Pairs 34 and 45 touch legally.
The table covers all 15 unordered pairs and proves all 60 component inequalities with
shared normals. No component-wise choice of different normals is used.

## All 24 Cross Pairs Against the Actual Selected Squares

Each normal below is directed from $C_i$ toward $R_j$. The selected support on an axis
is $7/10$ and every core’s axis support is $1/2$, so an axis separator has threshold
$6/5$. The grouped minimum projections apply to every member of their displayed group.

| Cross group | Count | Shared unit normal | Projection or group minimum | Full threshold |
| --- | --- | --- | --- | --- |
| $R_1$ against all four selected squares | 4 | $(0,1)$ | $2109/1700$ | $6/5$ |
| $R_2,R_3,R_4$ against all four | 12 | $(0,1)$ | $1641/850$ | $6/5$ |
| $R_0$ against $C_0,C_2$ | 2 | $(0,1)$ | $13/10$ | $6/5$ |
| $R_0$ against $C_1$ | 1 | $f=(-3/5,4/5)$ | $37/34$ | $13/12$ |
| $R_0$ against $C_3$ | 1 | $(-1,0)$ | $127/50$ | $6/5$ |
| $R_5$ against $C_0,C_2$ | 2 | $(0,1)$ | $39/25$ | $6/5$ |
| $R_5$ against $C_1$ | 1 | $e=(4/5,3/5)$ | $3264/2125$ | $1$ |
| $R_5$ against $C_3$ | 1 | $f=(-3/5,4/5)$ | $2177/2125$ | $1$ |

The counts total 24. For the close cross pair $R_0,C_1$, its coordinates in denominator
850 are $(-759,587)$, giving

$$
f\cdot(R_0-C_1)=\frac{3(759)+4(587)}{4250}=37/34.
$$

The actual selected support is $1/2$ and the full hull support is $7/12$, not the disk
value $1/2$. The exact margin above their sum $13/12$ is $1/204$. For the two final
cross pairs, $R_5$ is a saturated disk, so the actual selected normal and residual
support sum is exactly one.
Their projections are computed from the actual selected bases in (1), not from an
octagon guard.

Every row proves both cross thresholds on its one displayed normal.
Thus all 48 cross support inequalities hold.
The 15 mutual and 24 cross pairs together supply 39 exact unit normals and 108 support
inequalities for these six bodies.

This six-core result is consistent with a future uniform bound of six, if one is proved.
It would make that bound attained at $G_A$. It is not evidence that the bound holds
uniformly, and it does not provide six actual residual square orientations.

## Failed Seventh Insertion and a Wall-Edge Limitation

The old BC278 valley disk center $P_6=(58/25,39/20)$ cannot be appended to the six
cores. Its displacement from $R_5$ has absolute coordinates $19/50$ and $31/100$, hence

$$
\|P_6-R_5\|^2=\frac{38^2+31^2}{10000}=\frac{481}{2000}<1.
$$

The incircles alone overlap.
By the unit-normal Cauchy bound, no normal can satisfy this new pair’s threshold one.
This is a refused fixed insertion, not exclusion of all possible seventh centers or all
possible rearrangements of the six.

A generic necessary condition also limits repairs that only move a roof or side center
inward. For every $r\ge1/2$ with its exact $a(r)$,

$$
r+a(r)\ge1.
$$

On the unsaturated branch the difference from one is $(2r-1)^2/(4r)\ge0$. On the
saturated branch it is at least $3/(2\sqrt2)-1>0$. Consequently a core for which the top
wall attains the clearance minimum has lower box edge

$$
Y-a=q-(r+a)\le q-1,
$$

and a right-wall-minimum core has left box edge $X-a\le q-1$. Suppose the former center
is weakly above and left of the latter.
Their contained axis boxes can have disjoint interiors only if

$$
X_{\rm top}+a_{\rm top}\le q-1
\quad\text{or}\quad
Y_{\rm right}+a_{\rm right}\le q-1.
$$

This follows from the two axis-box separation alternatives and the two preceding edge
bounds. All inequalities are weak, and wall-minimum ties cause no loss of coverage.
The condition explains why shrinking a halfside through inward motion is not by itself a
complete repair of the rejected BC278 roof/right pair.
It is only a necessary condition; it supplies no residual count.

## Exact Remaining Obligation and Terminal Scope

The frozen target still has seven independently variable residual centers and the whole
unchanged $\Gamma_0$. A seventh center added to the displayed six would need its exact
clearance graph, four selected cross pairs and six mutual pairs: ten additional shared
unit normals and 32 support inequalities.
No such addition has been certified.
A seven-core witness could instead require changing any of the selected poses or all six
existing centers; none is fixed in the actual target.

No argument here rules out those changes or supplies a uniform count of six.
In particular, the wall-edge limitation and the single failed insertion do not form a
complete cover.
The model could still admit seven cores elsewhere, and a seven-core model
witness would still not be an eleven-square packing.
The full-square child and H118’s matching coupled-LP comparison remain undetermined by
this attempt.

The terminal disposition is an exact six-core lower control plus a failed seventh
insertion, subject to the fresh independent audit.
No target narrowing, weaker union model, discretized normal catalogue, engine switch or
retry is proposed by this result.

## Work Receipt

The prospective phase-16 start was `2026-09-07T11:36:33Z`, with this adversary’s hard
stop at `2026-09-07T12:01:33Z`. The actual first clock read was `2026-09-07T11:39:06Z`.
The attempt read the frozen protocol, its completed predicate admission and the
previously accepted BC278 source control.
It did not read the active BC279 author report or exchange reasoning with the author or
reserved auditor.

All construction and verification arithmetic above was performed by hand.
No numerical target run, solver, target script, resource search, implementation,
dependency, new identifier, shared-record or Git change was made.
Only this assigned native report was written.
The mathematical report and complete certificate readback froze at
`2026-09-07T11:57:40Z`, 1,114 seconds after the actual first clock read.
The common-document and prose passes were applied.
Installed Flowmark 0.4.0 formatted only this assigned file with caching disabled.
The three native source links, the single required footer, and the final no-cache format
and trailing-whitespace checks are verified before handoff, within the absolute cap.
No target reasoning continues after this freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
