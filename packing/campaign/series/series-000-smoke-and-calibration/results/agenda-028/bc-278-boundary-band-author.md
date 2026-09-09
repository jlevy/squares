# BC-278: Boundary-Band Author Result

**Partial result; the full-square target remains unresolved.** The unchanged admitted
four-pose domain contains an exact configuration admitting seven radius-$1/2$ disks with
disjoint interiors. Consequently neither $\kappa_{\rm disk}\le6$ nor
$\kappa_{\rm oct}\le6$ holds uniformly on that domain.
These are negative controls for the two relaxations.
They do not refute $\kappa_\square\le6$, and the particular seven disk centers below
cannot be lifted to seven full squares.

The construction, its complete model checks, and that non-liftability argument are
proved analytically below, subject to the separately scheduled independent audit.
No whole-domain full-square exclusion or eleven-square witness is claimed.

## Frozen Scope and the Remaining Cavity

This attempt follows the unchanged [BC278 protocol](bc-278-boundary-band-protocol.md),
the [BC277 domain](bc-277-boundary-band-domain-design.md), and its
[accepted admission](bc-277-boundary-band-domain-review.md).
Put $q=96/25$, $b=1/2$, $d=167/50$ and $k=299/1000$. The selected four actual unit
squares have centers in the closed lower band $[b,217/150]$, weakly ordered
horizontally, and independent actual angles in the complete chart $[-\pi/4,\pi/4]$
modulo quarter turns.

The pose-dependent quantities $m,\ell,u,\varepsilon,A,R,\Delta$ have exactly their
admitted meanings: $A=m+2/5-\varepsilon$, $R=A+k$, and $\Delta=u-\ell$. All eight guards
are retained:

$$
\Delta,\quad A-k-\Delta,\quad b-u+A,\quad
b+k-x_0,\quad x_3-d+k,\quad
2k+\Delta-x_{i+1}+x_i\quad(i=0,1,2)
\quad\ge0.
$$

The full child $D_0$ continues to include eleven actual squares, their actual
containment, all six selected-pair, 28 selected-to-residual and 21 residual-pair
complete SAT clauses.
Each pair retains all four edge axes and both signs, with weak inequalities.
No guard, angle, alternative, contact, seam, label choice or failure sibling is removed
in this report. Choosing a particular legal member for a counterexample to a universal
relaxation bound does not restrict the target domain.

There is a useful uniform localization, but it is insufficient for capacity six.
The admitted octagons $K_i$ have horizontal section radius

$$
r_v(Y)=\min(A,R-|Y-v|),\qquad |Y-v|\le A,
$$

where $v$ is $\ell$ or $u$ according to the selected slot.
The first two guards imply $0\le\Delta\le A-k$. On the common interval $[u-A,\ell+A]$,
the alternating section radii sum to at least $2k+\Delta$: their sum is concave, and at
either endpoint the two radii are $k$ and $k+\Delta$. The gap guards therefore join all
four horizontal sections, and the endpoint guards reach $b$ and $d$. The attachment
guard puts $b$ in that common interval.
Thus

$$
[b,d]\times[b,\ell+A]\ \subseteq\ \bigcup_{i=0}^3K_i.
$$

The admission proved that even the closed $K_i$ is strictly forbidden to a legal disk
center. Every actual residual square or legal residual disk therefore has center height
strictly greater than $\ell+A$. This strict conclusion concerns the actual square and
disk models; the octagon relaxation deliberately permits octagon boundary points.

Above $\ell+A$ and through $u+A$, any surviving center lies left of the first high-row
obstacle or between the two high-row obstacles.
These potential passages open into the top region above $u+A$. The lower-band domain
always has $u+A<779/300<d$, so they cannot be capped by the central-band argument.
The exact disk construction below occupies both lower passages and the upper region.

## A Legal Four-Square Member

Let all four selected squares have the actual orientation

$$
e=(4/5,3/5),\qquad f=(-3/5,4/5),\qquad
\theta=\arctan(3/4)\in(0,\pi/4).
$$

Their centers are

| Slot | $x_i$ | $y_i$ |
| --- | --- | --- |
| $0$ | $7/10$ | $7/10$ |
| $1$ | $1269/850$ | $1113/850$ |
| $2$ | $399/170$ | $7/10$ |
| $3$ | $157/50$ | $1113/850$ |

Call this four-pose configuration $G_*$. Equal choices at this one point are legal
values of four independent angle variables.
This is a new exact member of the unchanged domain, not a replacement for the original
four-diamond membership fixture.

Every selected square has horizontal and vertical support $h=7/10$. The two extreme
horizontal centers equal $h$ and $q-h$; the low centers equal $h$ vertically.
These wall contacts are legal.
All other wall inequalities hold, and the high centers are strictly below the lower-band
ceiling, with

$$
217/150-1113/850=7/51>0.
$$

The horizontal gaps are $337/425$, $363/425$, $337/425$, and the alternating height
difference is $259/425$. Since the selected squares share $e,f$, their support sums on
either axis are one.
The following six weak SAT certificates prove all their pair conditions:

| Pair | Separating normal | Projected center displacement |
| --- | --- | --- |
| $(0,1)$ | $e$ | $1$ |
| $(1,2)$ | $-f$ | $1$ |
| $(2,3)$ | $e$ | $1$ |
| $(0,2)$ | $e$ | $112/85$ |
| $(1,3)$ | $e$ | $112/85$ |
| $(0,3)$ | $e$ | $197/85$ |

For example, the first numerator is $4(337)+3(259)=2125$, and the middle adjacent
numerator is $3(363)+4(259)=2125$, both over denominator $2125$. The three adjacent
touches must not be discarded by replacing weak SAT with strict separation.

At $G_*$ the guard quantities are

$$
m=5/8,\quad \varepsilon=0,\quad \ell=7/10,\quad
u=1113/850,\quad \Delta=259/425,\quad
A=41/40,\quad R=331/250.
$$

In the frozen order, the eight guard values are

$$
\frac{259}{425},\quad \frac{991}{8500},\quad
\frac{733}{3400},\quad \frac{99}{1000},\quad
\frac{99}{1000},\quad \frac{3523}{8500},\quad
\frac{3003}{8500},\quad \frac{3523}{8500}.
$$

Every value is strictly positive.
Thus $G_*\in\Gamma_0$. Its bottom barrier is $\ell+A=69/40$ and its high-row octagon top
is $u+A=7937/3400$. Membership in $\Gamma_0$ asserts four guarded poses, not a point of
the as-yet unresolved eleven-square child $D_0$.

## Seven Exact Disk Centers

Place closed radius-$1/2$ disks at the following centers:

| Disk | $X$ | $Y$ |
| --- | --- | --- |
| $P_0$ | $1/2$ | $167/50$ |
| $P_1$ | $179/100$ | $167/50$ |
| $P_2$ | $279/100$ | $167/50$ |
| $P_3$ | $121/100$ | $63/25$ |
| $P_4$ | $167/50$ | $5/2$ |
| $P_5$ | $1/2$ | $617/340$ |
| $P_6$ | $58/25$ | $39/20$ |

All coordinates lie in $[b,d]$, so every disk is contained in the square container.
The top and side contacts are legal in this model.
All centers are above $69/40$, as required by the guard barrier.

### All 21 Mutual Disk Conditions

Only four pairs need both coordinates to certify distance at least one:

| Pair | Squared distance |
| --- | --- |
| $(P_0,P_3)$ | $11765/10000$ |
| $(P_1,P_3)$ | $10088/10000$ |
| $(P_2,P_4)$ | $10081/10000$ |
| $(P_3,P_5)$ | $2894450/2890000$ |

Every displayed fraction is greater than one.
For the last pair the coordinate differences are $1207/1700$ and $1199/1700$, whose
squared numerators sum to $2894450>1700^2=2890000$.

Each of the other 17 pairs has a coordinate difference at least one.
Their inventory is

$$
\begin{gathered}
01,\ 02,\ 04,\ 05,\ 06,\ 12,\ 14,\ 15,\ 16,\\
23,\ 25,\ 26,\ 34,\ 36,\ 45,\ 46,\ 56.
\end{gathered}
$$

Here $ij$ means $(P_i,P_j)$. Pair $12$ has horizontal distance exactly one; all other
pairs in this list have a coordinate distance strictly greater than one.
This accounts for all 21 unordered pairs and preserves the legal disk touch.

### All 28 Disk-to-Selected-Square Conditions

In the orthonormal $e,f$ coordinates, the selected unit square is $[-1/2,1/2]^2$. If
$a=e\cdot(P-C_i)$ and $c=f\cdot(P-C_i)$, its squared distance from $P$ is

$$
(|a|-1/2)_+^2+(|c|-1/2)_+^2.
$$

Distance at least $1/2$ proves that a radius-$1/2$ disk avoids the square interior.
In particular, a positive normal coordinate at least one is a sufficient separating
projection for this square and disk.
It is not the corresponding support threshold for an arbitrary full residual square.

The 28 checks reduce as follows, without omitting any pair:

- The three top disks $P_0,P_1,P_2$ and disk $P_3$ lie vertically above all four
  selected squares. The maximum selected top height is $854/425$. The bottom of each top
  disk is $71/25$, leaving gap $353/425$; the bottom of $P_3$ is $101/50$, leaving gap
  $9/850$. This checks 16 pairs.
- Disk $P_4$ clears squares $0,2$ vertically by $3/5$, and square $1$ horizontally by
  $11/17$. Its remaining pair with square $3$ is checked exactly below.
- Disk $P_5$ clears squares $2,3$ horizontally, with gaps $11/17$ and $36/25$. Relative
  to square $0$, its $f$ coordinate is $86/85>1$. Relative to square $1$, its
  coordinates are $a=-167/340$ and $c=1$. Since $|a|<1/2$, its distance from that square
  is exactly $1/2$: this is a legal disk touch, not a strict-clearance claim.
- Disk $P_6$ clears square $0$ vertically by $1/20$. Its separating normal coordinates
  for squares $1,2,3$ are respectively $e\cdot(P_6-C_1)=8891/8500$,
  $f\cdot(P_6-C_2)=4319/4250$, and $f\cdot(P_6-C_3)=4269/4250$. All three are strictly
  greater than one.

For the remaining pair $(P_4,C_3)$, the displacement is $(1/5,506/425)$. Its normal
coordinates are $1858/2125$ and $1769/2125$, both greater than $1/2$. Therefore the
exact squared distance is

$$
\frac{1591^2+1413^2}{4250^2}
=\frac{4527850}{18062500}
=\frac14+\frac{12225}{18062500}
>\frac14.
$$

This completes all 28 cross checks.
Together with disk containment and the 21 mutual checks, it proves

$$
\kappa_{\rm disk}(G_*)\ge7,
\qquad
\kappa_{\rm oct}(G_*)\ge7.
$$

The second statement follows from the accepted relaxation inclusion; the first is
already a check against the actual four selected squares, not merely the virtual
octagons. Neither inequality is an upper bound or a determination of the exact capacity
in its model.

### The Obstruction Persists Beyond One Pose Point

The selected wall and pair contacts do not make this merely an isolated example of the
four-pose domain. For a sufficiently small positive real $\eta$, change the selected
centers to

$$
\begin{aligned}
C_0(\eta)&=(7/10+\eta,7/10+\eta),\\
C_1(\eta)&=(1269/850,1113/850+3\eta),\\
C_2(\eta)&=(399/170,7/10+\eta),\\
C_3(\eta)&=(157/50-\eta,1113/850+3\eta).
\end{aligned}
$$

Keep the four angles initially unchanged, and replace $P_5$ by $(1/2,617/340+4\eta)$,
leaving the other six disk centers fixed.
The three formerly tight selected-pair projections become $1+2\eta/5$, $1+8\eta/5$,
$1+2\eta/5$. The formerly tight selected wall inequalities become strict.
The sole tight cross condition, the $f$ projection from square $1$ to $P_5$, becomes
$1+4\eta/5$.

All other relevant selected, cross and guard inequalities were strict and are
continuous, so they persist for some positive interval of $\eta$. The changed mutual
disk distances were also strict; the unchanged touch $P_1P_2$ remains legal.
After fixing one sufficiently small positive $\eta$, every selected containment,
selected separation, band, ordering, guard and cross-clearance condition is strict.
Continuity then permits a nontrivial open family of selected poses, including
independent angle changes, with these same seven disk centers.
No numerical neighborhood size or fitted pose box is required for this existence
argument.

This strengthens the model obstruction; it adds no premise to $\Gamma_0$ and says
nothing about a seven-full-square extension.

## Why This Does Not Solve the Full-Square Target

There is an exact obstruction to lifting these particular disk centers.
Any contained unit square centered at height $d=q-1/2$ must have coordinate support
$1/2$, hence must be axis aligned modulo quarter turns.
The same holds for a square centered at horizontal coordinate $d$. Consequently a square
at $P_2$, which lies on the top center boundary, and one at $P_4$, which lies on the
right center boundary, are both forced to be axis aligned.
Their coordinate differences are

$$
|P_{4,x}-P_{2,x}|=11/20<1,
\qquad
|P_{4,y}-P_{2,y}|=21/25<1.
$$

Their interiors therefore overlap.
All their actual SAT alternatives fail.
This is compatible with their disk squared distance $10081/10000>1$. It proves failure
of this center-wise lifting attempt, not impossibility of other seven-square poses in
the same cavity or elsewhere in $\Gamma_0$.

The disk counterexample also blocks a tempting repair of the weaker-model route.
Replacing $E$ by a tighter polygon inside the radius-$1/2$ disk, adding more such
orientation-independent forbidden-center resources, or using the exact selected
square-plus-disk obstacle still cannot establish a uniform disk capacity of six: the
seven disks pass the strongest of those individual-obstacle checks already.
Indeed the intersection of all centered unit-square orientations is exactly the
radius-$1/2$ disk. The disk is contained in every orientation; conversely, for any point
of norm greater than $1/2$, choose a square edge normal parallel to that point, which
excludes it. Thus a larger fixed inner core valid for every residual angle is
unavailable. This argument concerns common-core center models; it does not rule out
orientation-dependent or joint full-square arguments.

The precise remaining implication is therefore unchanged:

$$
\forall G\in\Gamma_0:\quad
\text{seven individually contained actual unit squares cannot simultaneously satisfy}
\text{ all 28 cross and 21 mutual full-square SAT clauses.}
$$

The bottom barrier is established, but it does not imply this statement.
The disk witness identifies the missing information concretely: actual wall support and
residual-square pair shape can contradict a disk-legal arrangement.
A proof must control that information across the entire admitted four-pose family,
rather than checking only this arrangement.
No uniform such argument was completed in this lease.

## Reflection, Controls and Disposition

Reflect all selected squares and all seven disk centers jointly by
$(X,Y)\mapsto(X,q-Y)$, and replace each selected angle by its negative.
Orthogonal reflection preserves containment, distances, the selected SAT certificates
and all cross checks.
It gives the same seven-disk obstruction in the reflected upper-band domain.
The selected low heights become $157/50$ and selected high heights become $2151/850$;
the guard values are unchanged when evaluated in inward depth.
The disk centers are reflected by the same displayed formula, including those on walls.
The full-square non-liftability pair is transferred too.

The closed upper and lower band endpoints, counting seam convention, all label and
weak-order parents and every guard-failure sibling remain as admitted.
The reflection transfers closed domains, not the seam counting assignment.
No full-square success child is pruned by this partial result.

The original four-diamond lower fixture and its upper reflection remain membership
controls only. Their capacities were not determined here.
The new $G_*$ checks the same eight-guard domain at a different legal actual angle, and
the seven-center construction falsifies only the disk and octagon bounds of six.
The exact wall-forced overlap is a negative control against relabeling that construction
as an eleven-square witness.
The preserved selected-square touches, disk touch and wall contacts also check the
weak-boundary convention.

This result supplies neither an H118 separation from a matching coupled LP nor an exact
feasible point of such an LP. The unchanged full-square question is unresolved.
The next authorized action is the independent reader audit of this negative control and
of the separate adversary report after both reports freeze.
Any later actual-angle capacity argument needs its own prospective scope; this report
does not admit a retry, new guard, engine change, numerical run or instrument.

## Work Receipt

The prospective author lease was 10:12:58–10:38:23 UTC on 2026-09-07. The actual first
clock read was 10:14:08 UTC. I read the frozen protocol, admitted design and accepted
admission review. I did not read the adversary’s evolving report or exchange target
reasoning with that agent.
All mathematical work above was hand derivation and exact arithmetic.
No solver, numerical target, resource search or one-off target script was run.
Only this assigned report was written; no shared record, identifier, dependency or Git
state was changed.

The mathematical argument and full exact readback froze at the final clock read of
10:32:11 UTC, an elapsed 18 minutes 3 seconds.
The common-document and prose-editing passes were applied.
Installed Flowmark 0.4.0 formatted this file and passed its scoped check with caching
disabled; the three linked source files exist, the trailing-space check found no
matches, and the required footer appears once.
Those checks first completed at 10:31:50 UTC. A final scoped formatting check follows
this receipt before handoff, within the original 10:38:23 UTC hard deadline.
No mathematical target work continues after this freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
