# BC-278: An Exact Obstruction to the Octagon Capacity Method

**The declared octagon relaxation admits seven centers at an exact member of
$\Gamma_0$.** All seven centers lie strictly outside every closed guard octagon, and all
21 pair distances are at least one.
Thus a uniform octagon-capacity upper bound of six on the unchanged family is false.
Removing the relaxation’s allowance for octagon boundary points does not repair that
proposed bound.

This is a surrogate obstruction, **not an eleven-square packing**. One of the seven
radius-$1/2$ disks strictly overlaps a selected actual square.
The configuration therefore supplies neither a disk-model witness nor a full-square
witness. The complete question $D_0=\varnothing$ remains unresolved by this adversary,
subject to the fresh independent audit of both terminal arguments.

The target and interpretation are those of the
[frozen BC278 protocol](bc-278-boundary-band-protocol.md),
[BC277 domain](bc-277-boundary-band-domain-design.md), and
[accepted admission review](bc-277-boundary-band-domain-review.md).
No guard, angle range, label convention or full-square condition is changed.
Choosing one exact $G\in\Gamma_0$ is sufficient to refute the universal surrogate bound;
it does not replace the whole full-square target by a smaller domain.

## Exact Selected Four Squares

Let $r=\sqrt3$, and give all four selected squares the actual orientation
$\theta=\pi/6$, strictly inside the admitted chart.
Their common orthonormal basis, coordinate half-width and core radius are

$$
e=(r/2,1/2),\qquad f=(-1/2,r/2),\qquad
h=(r+1)/4,\qquad m_i=1/r=r/3.
$$

Take the centers, in the frozen horizontal slot order,

$$
C_0=(7/10,7/10),\quad
C_1=(37/25,41/30),\quad
C_2=(233/100,7/10),\quad
C_3=(311/100,41/30).
\tag{1}
$$

All quantities are exact elements of $\mathbb Q(\sqrt3)$. The rational enclosure

$$
\frac{69}{40}<r<\frac{87}{50},\qquad
\frac{23}{40}<m=\frac r3<\frac{29}{50}
\tag{2}
$$

follows from

$$
3-\left(\frac{69}{40}\right)^2=\frac{39}{1600}>0,
\qquad
\left(\frac{87}{50}\right)^2-3=\frac{69}{2500}>0.
$$

The smallest distance of a selected center coordinate from a corresponding container
wall is $7/10$. Since $h<137/200<7/10$, every selected square is strictly contained in
$[0,96/25]^2$. Both ordinates lie strictly in $B_0$: $7/10>1/2$ and $41/30<217/150$,
with upper clearance $2/25$. The horizontal gaps are $39/50,17/20,39/50$, all positive.

For two parallel unit squares, separation along either of their actual unit axes needs a
directed center projection of at least one.
The following six directed SAT choices verify the entire selected-pair inventory:

| Pair | Directed normal | Projection of $C_j-C_i$ |
| --- | --- | --- |
| $(0,1)$ | $e$ | $39r/100+1/3$ |
| $(1,2)$ | $-f$ | $17/40+r/3$ |
| $(2,3)$ | $e$ | $39r/100+1/3$ |
| $(0,2)$ | $e$ | $163r/200$ |
| $(1,3)$ | $e$ | $163r/200$ |
| $(0,3)$ | $e$ | $241r/200+1/3$ |

They all exceed one.
From (2), the first expression is greater than $12073/12000$, the second is greater than
$17/40+23/40=1$, and the fourth is greater than $11247/8000$. The last is the sum of the
first and the fifth expressions.
Equal angles are allowed, and these are actual square normals, not coordinate-axis
proxies. The chosen valid alternatives establish each complete SAT disjunction; no
alternative is deleted from the domain.

## All Eight Guards at the Actual Poses

The poses determine

$$
\ell=7/10,\qquad u=41/30,\qquad
\varepsilon=0,\qquad \Delta=2/3,\qquad
m=r/3,\qquad A=m+2/5,\qquad R=A+299/1000.
\tag{3}
$$

In particular the common value $m$ is the actual minimum of the four core radii; it is
not chosen as a relaxation variable.
The exact eight guard values, in the protocol’s order, are

$$
\frac23,\quad m-\frac{1697}{3000},\quad m-\frac7{15},\quad
\frac{99}{1000},\quad\frac{69}{1000},\quad
\frac{727}{1500},\quad\frac{311}{750},\quad\frac{727}{1500}.
\tag{4}
$$

All are strictly positive.
For the two involving $m$, (2) gives

$$
m-\frac{1697}{3000}>\frac7{750}>0,
\qquad
m-\frac7{15}>\frac{13}{120}>0.
$$

Thus (1) is a member of the unchanged four-pose domain $\Gamma_0$, with strict wall,
band, ordering, pair and guard margins.
This membership check is independent of the seven-center construction.
It asserts no full eleven-square completion.

## Seven Centers Strictly Outside the Closed Octagons

Use these seven exact rational centers for the declared octagon relaxation:

$$
P_0=(1/2,17/10),
\tag{5}
$$

$$
P_1=(13/10,47/20),\qquad
P_2=(23/10,47/20),\qquad
P_3=(33/10,47/20),
\tag{6}
$$

$$
P_4=(1/2,167/50),\qquad
P_5=(9/5,167/50),\qquad
P_6=(31/10,167/50).
\tag{7}
$$

Every coordinate lies in the required closed center box $[1/2,167/50]^2$. The boundary
coordinates in (5) and (7) are retained legally in that model.

The top of either high-row octagon is

$$
u+A=\frac{53}{30}+m.
$$

Every center in (6) and (7) has ordinate at least $47/20$, and

$$
\frac{47}{20}-(u+A)=\frac7{12}-m>\frac1{300}>0
\tag{8}
$$

by (2). They therefore lie strictly above all four closed $K_i$.

For $P_0$, the two low-row octagons have top $\ell+A=11/10+m$, and

$$
\frac{17}{10}-(\ell+A)=\frac35-m>\frac1{50}>0.
\tag{9}
$$

It lies above both of those guards.
Its horizontal distance to the first high-row guard center is

$$
x_1-\frac12=\frac{49}{50}>m+\frac25=A,
\tag{10}
$$

because $m<29/50$. The other high-row guard is farther right.
Thus $P_0$ is strictly left of both high-row guards.
Equations (8)–(10) verify strict avoidance of every closed $K_i$ for every center, using
an axis inequality of that same octagon.
No open-versus-closed convention is used to gain any of these seven places.

## All 21 Mutual Distance Conditions

The 21 unordered pairs split exhaustively into five groups:

- The three pairs within (6) have horizontal separations one, one and two, so their
  distances are at least one.
  The two adjacent pairs touch in the disk-distance model.
- The three pairs within (7) have horizontal separations $13/10,13/10,13/5$.
- The nine pairs between (6) and (7) have vertical separation $99/100$. The smallest
  absolute horizontal separation between their listed abscissae is $1/5$, attained by
  $P_3,P_6$. Every such squared distance is therefore at least $10201/10000>1$.
- The three pairs from $P_0$ to (6) have vertical separation $13/20$ and horizontal
  separation at least $4/5$. Their squared distances are at least $17/16>1$.
- The three pairs from $P_0$ to (7) have vertical separation $41/25>1$.

These groups contain $3+3+9+3+3=21$ pairs.
Together with (8)–(10), they prove

$$
\kappa_{\rm oct}(G_*)\ge7
\tag{11}
$$

for the exact four-pose member $G_*$ in (1). No numerical separation tolerance, sampled
angle, unverified mutual pair or unstated rounding decision is present.

## Why This Is Not a Disk or Full-Square Witness

The failure is strict, not a touching ambiguity.
Consider $P_1$ and the selected square at $C_1$. Their displacement is

$$
P_1-C_1=(-9/50,59/60)=\alpha e+\beta f,
$$

where

$$
\alpha=\frac{59}{120}-\frac{9r}{100},\qquad
\beta=\frac9{100}+\frac{59r}{120}.
\tag{12}
$$

One has $0<\alpha<1/2$ and $1/2<\beta<1$. For example, $1<r<9/5$, which follows from
(2), gives $\alpha>59/120-81/500>0$, $\alpha<59/120<1/2$, $\beta>9/100+59/120>1/2$, and
$\beta<39/40<1$.

In the selected square’s orthonormal coordinates, the nearest point to $P_1$ is
therefore on the face with $f$ coordinate $1/2$, at distance $\beta-1/2<1/2$. Moving
that point a sufficiently small distance into the square keeps it inside the open
radius-$1/2$ disk centered at $P_1$. The two interiors intersect.
The declared disk model consequently rejects this configuration.

Every full unit square centered at $P_1$, whatever its actual orientation, contains that
incircle. Hence no choice of an actual orientation for this center repairs the overlap
with the selected square.
There is no eleven-square certificate here: one of the 28 selected-to-residual
full-square conditions already fails, and no claim is made that the 21 residual
full-square SAT clauses follow from the distance checks.

The obstruction occurs with zero row scatter, common actual selected angles, strict
source guards and strict avoidance of all $K_i$ boundaries.
It cannot be repaired merely by deleting the octagon boundary allowance or by requiring
those same common-angle and zero-scatter properties.
The retained octagon approximation loses geometric information needed to reject these
centers; this report does not identify a replacement relaxation as uniformly sufficient.

## Scope, Remaining Gap and Work Receipt

The proposed sufficient statement $\kappa_{\rm oct}(G)\le6$ for every $G\in\Gamma_0$ is
refuted by the exact data above, subject to independent arithmetic and geometry review.
Its reflected version is obstructed by the admitted joint reflection of the selected
poses and all seven centers.
No new upper-band theorem is asserted.

The sound chain $\kappa_\square\le\kappa_{\rm disk}\le\kappa_{\rm oct}$ gives no lower
bound for either stronger model from (11). This adversary proves neither
$\kappa_{\rm disk}(G_*)\ge7$ nor $\kappa_\square(G_*)\ge7$, and supplies no uniform
upper bound in those models.
The whole $D_0$ and reflected $D_2$ determination remains open in this report.
Every original failure sibling, actual-angle seam, legal touching case and full-square
condition is retained.

The smallest remaining mathematical implication is a uniform bound in the admitted disk
model, or an argument using the actual orientation-dependent square cavities and their
21 mutual SAT clauses, throughout the unchanged $\Gamma_0$. Such a proof must use
information that rejects the present octagon configuration.
Establishing it only at $G_*$ would still not be uniform.
The declared octagon argument ends at this obstruction; no replacement target, new
engine, narrowed guard family or automatic retry is attempted.
The independent author may have a different whole-domain argument, which this adversary
has neither read nor discussed with that author.

The prospective session092 lease was `2026-09-07T10:12:58Z` through
`2026-09-07T10:32:58Z`. The actual first clock read after dispatch was
`2026-09-07T10:14:17Z`. Work used the three frozen sources linked above, exact hand
construction and symbolic comparisons.
No author report or evolving argument was read; no reasoning was exchanged with that
author. Only the coordinator received the scoped interim finding.

Only this assigned report was written.
No numerical target, solver, one-off target script, resource search or implementation
ran. No Git state, shared record, identifier, dependency or other scientific file was
changed. The common-document and prose-editing passes were applied.

The mathematical draft was complete at `2026-09-07T10:20:59Z`. The complete formatted
readback and source/whitespace/footer checks ended at `2026-09-07T10:22:36Z`, 8 minutes
19 seconds (499 seconds) after actual startup.
Installed Flowmark 0.4.0 passed its full auto-format check with caching disabled.
All three linked source files existed, the whitespace scan found no trailing blanks, and
the required footer appeared once.
The six SAT rows, eight guard values, 21-distance partition, strict octagon avoidance
and disk-overlap calculation were reread by hand.
No machine verification of the target arithmetic is claimed.
A final no-cache format/check follows this receipt before delivery.
Independent acceptance belongs to the reserved fresh reader, and no background command
remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
