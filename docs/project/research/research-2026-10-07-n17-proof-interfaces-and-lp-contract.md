---
title: n17 Proof Interfaces and Finite-Angle LP Contract
date: 2026-10-07
status: research-contract
---
# n17 Proof Interfaces and Finite-Angle LP Contract

The fixed-container local theorem composes with a centred global search without moving
the packing after capture.
The finite-angle reconnaissance below uses 19 pairs, 27 allowed owner options and 256
feature branches. Its sampled values concern a specified relaxation; they do not
establish a widened terminal theorem.

This is the mathematical contract for BC-431 and BC-433 under the
[ten-hour plan](../specs/active/plan-2026-10-06-n17-ten-hour-session.md), derived from
the initial source at `f3a13e3a2` and extended by the derivations and linked receipts
below. The coordinator owns hypothesis and experiment registration.
Outcome summaries refer to those registered experiments and preserve their stated scope.
The centred-container join and the finite-geometry arguments below are hand derivations
by the session’s sole Astra agent; they have not received independent mathematical
review or been machine-checked.
Existing receipts keep their existing assurance and scope.

## Proof Interfaces

Write $S^*$ for the accepted exact endpoint side, $U=1169/250$, $m=(U/2,U/2)$, and
$C(V)=[(U-V)/2,(U+V)/2]^2$. Every cell remains in the original $[0,U]^2$ cover frame.
A smaller cap changes the container walls, not the cells.
The endpoint family in that frame is $F(w)=x^*(w)+(\sigma,\sigma)$, with
$\sigma=(U-S^*)/2$ and $w=(a,b,z)$.

The [W3 consolidation](../reviews/review-2026-10-06-n17-w3-consolidation.md) records the
accepted local parts, the admitted residue and the capture failure.
The following obligations state how those parts can be used in one proof.

| Interface | Required input and implication | Evidence and check | Remaining obligation |
| --- | --- | --- | --- |
| Container normalization | A putative packing in side $s\le S^*$ is translated into $C(s)\subset C(S^*)\subset C(U)$. Preserve this placement thereafter. | The centred-container lemma below; inclusion is exact for ordered side lengths. | Independent review of this hand join; consumers must use the same walls and cell coordinates. |
| Closed-cell assignment | Every centre is in the closed cover. Choose one containing cell per square. Capacity one makes the chosen cells distinct, giving a 17-cell mask. Boundary membership may allow several masks. | exp-247 and `check_n17_capacity_one_cover`; the census must retain all geometrically allowed assignment masks. | A deterministic choice is safe only with a proof that its transported assignments remain represented. Discarding seam cases because they are non-generic is invalid. |
| D4 and labels | Apply a symmetry about $m$ to the packing, its chosen cell assignment and its angle axes together. Transfer the mask to its representative. In the endpoint mask, label each assigned square by the corresponding family cell. | Exact cover cell permutations and admitted consumer semantics; $gC(V)=C(V)$ for every $g\in D_4$. The exp-259 endpoint orbit has size 8, so its mask stabilizer is trivial. | Retain the symmetry/label witness, including its action on reflected angle axes. |
| Global exclusions | Each admitted exclusion rules out its declared cell subpattern at a declared cap $V\ge S^*$, with matching frame, cells and full closed-branch coverage. | Full certificate verification and admission ledger; a subpattern exclusion removes every containing assignment mask and its valid symmetry images. | Close or capture every remaining orbit. After Tail B's ordinary admission, the exp-274 [admission summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-274-current-tail-b-replication/admission-summary.json) joins the independent census and partition: 36,768 states / 4,683 orbits under 60 entries, with the endpoint surviving. These are unresolved assignments, not a cover of terminal neighbourhoods. Held closures require their ruling. |
| Cap monotonicity | The normalized packing stays inside $C(S^*)\subseteq C(V)$ whenever a certificate uses $V\ge S^*$. | Exact inequalities for the certificate cap and the certified root enclosure. | Tightening a cap below $S^*$ is invalid; changing from centred to origin-anchored walls without transporting cells changes the claim. |
| Capture cap | Use a rational $U'$ proved to satisfy $S^*\le U'\le U$; the current design requests $0<U'-S^*\le10^{-12}$. Capture runs in $C(U')$ with the original cells. | H-288/exp-275 and its fresh replay establish the fixed cap inequalities over the full accepted root and retained consumer enclosure. | Bind each actual producer input and saved seed to that numeric frame, then derive its coordinate bounds. A small cap excess does not itself bound a coordinate error. |
| Outer capture | Every target packing represented by an unresolved cell state reaches a declared terminal region, or is excluded. Every split retains a closed cover of its parent. | A complete capture/exclusion certificate from the actual cells; terminal leaves may also use the original containment in $C(S^*)$. | Open. Success from a small pose box, contraction of a pilot box, or a widened terminal theorem alone does not cover the outer cells. |
| Coordinate frame and root | Capture returns bounds on the exact-root family in the same cover frame, with H254 angle lifts modulo $\pi/2$. | Layout identities, exp-237/238 root enclosures, and the explicit allowance below. | Certify all frame, centre, basis and angle conversion errors. Charge them to the delivered enclosure before comparison with the terminal radius. |
| Square 6 | In the endpoint assignment, the square labelled 6 has its centre in the complete closed `side-S2` cell, at any orientation. | exp-247 assignment and exp-248 slider coverage; `check_n17_slider_coverage.SIX_CELL`. | Keep the cell premise through symmetry and capture. No closeness premise on square 6 is licensed. Dropping it from the local/LP subsystem is a relaxation, not permission to drop it from slide coverage. |
| Slider domain | Once the 45 coordinates meet $r=1/5000$ and square 6 meets its cell premise, exp-248 places $(a,b,z)$ in $B_W'$ below. | The accepted slider composition and the local ratio receipt on $B_W'$. | A widened neighbourhood needs new slider coverage, or explicit capture bounds on the sliders. The old implication cannot be used at a larger radius. |
| Terminal radius | All 45 exact non-slider coordinates satisfy their componentwise closed bound $\le1/5000$. | exp-244/248 local theorem, with its reviewed hand lemmas and recorded ratio test. | Capture must establish every component, not only three widest owners or a scalar extent statistic. Use the correct 29 position functionals and 16 angles. |
| Terminal conclusion | Inside $C(S^*)$, the local theorem forces the sixteen retained squares onto $F(w)$; that family spans $S^*$ in both coordinates. | C10 and the fixed-container theorem in the [recipe](../reviews/review-2026-10-02-n17-local-theorem-recipe.md). | Combine the conclusion with the original containment in $C(s)$. This proves $s\ge S^*$ only after the exclusion/capture coverage obligations are discharged. |
| Evidence custody | The admitted ledger identifies complete retained objects, their checker, parameters and interpretation. | Hosted manifest, transfer integrity, full replay receipts and recorded admission. | Recover absent objects; representative replays do not replace required full verification. Missing custody blocks reproducibility even when the abstract implication is clear. |

Tail A and Tail B are two admitted full seventeen-owner closures under the same
producer recipe. Each removed eight states in one orbit. Their outcomes establish
neither a closure rate for the selected stratum nor capture of its remaining states.

### The centred-container lemma

Let $P$ be a packing in a square of side $s\le S^*$. Translate the centre of that
containing square to $m$; then

$$
P\subset C(s)\subset C(S^*)\subset C(U')\subset C(U).
$$

For any $g\in D_4$ about $m$, these containments also hold for $gP$. Suppose a
transported closed-cell assignment gives $gP$ the endpoint labels, square 6 is in
`side-S2`, and all 45 non-slider coordinates relative to $F$ are at most $r=1/5000$.
Translate $gP$ by $-(\sigma,\sigma)$. It is a packing in the fixed container
$[0,S^*]^2$, so apply slide coverage with the declared containing side $S=S^*$, then the
local theorem on $B_W'$. Its sixteen retained squares equal $x^*(w)$. These squares
touch both opposite walls in each coordinate at every permitted $w$; their coordinate
spans are therefore $S^*$. But $gP\subset C(s)$ has each span at most $s$. Thus
$s\ge S^*$; if $s<S^*$ there is a contradiction.

The theorem’s quantifier is containment in $[0,S^*]^2$. It does not require the declared
container to be the smallest one containing the configuration: the
[recipe’s theorem and corollary](../reviews/review-2026-10-02-n17-local-theorem-recipe.md#the-theorem-and-its-lemmas)
state this directly.
Consequently the equality choice $S=S^*$ is legitimate even when the original packing
fit inside a smaller square.
This use also satisfies slide coverage’s right-wall bound $x_5^*+1/2=S^*$.

No translation by $(S^*-s)/2$ is made after capture.
The argument therefore avoids the radius loss discussed for a change of embeddings in
the
[local-half composition](../reviews/review-2026-10-02-n17-local-half-composition.md#the-composition).
It supplies the abstract normalization and D4 join; an implementation that uses
different walls, labels or cell coordinates still needs a separate correction and
verification.

### Checks on the lemma’s scope

- Choosing the declared side $S^*$ does not prove that $s=S^*$ in advance.
  The family conclusion supplies the span bound only after all local premises hold.
- The local theorem covers the sixteen-square subsystem.
  The preceding slide-coverage step uses the full 17-square packing and square 6’s
  actual cell, with no assumed pose.
- A D4 transformation preserves centred boxes.
  A reflection also changes angle axes; relabelling cells alone does not transport the
  H254 angle chart.
- A mask in the endpoint orbit supplies labels, but supplies no metric closeness.
  That is still the capture obligation.
- The argument uses the restricted capture-target theorem.
  It does not close H-261 as worded, whose unrestricted slider domain includes the
  square-5/6 exchange.
- The argument remains valid at $s=S^*$, where its conclusion describes the retained
  family. It claims neither uniqueness of square 6’s pose nor global uniqueness before
  the other states are handled.

The retained
[exp-259 orbit roster](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue/partition.json)
gives the endpoint representative mask 1900015 and orbit size 8. Since $|D_4|=8$, the
orbit-stabilizer identity gives a trivial endpoint-mask stabilizer.
Thus a chosen endpoint-orbit assignment has a unique group element taking it to the
fixed endpoint representative; no additional stabilizer images of the family need
separate capture for this cover.
This observation does not make a centre’s closed-cell assignment unique on a seam.

### Exact-root allowance and coordinate inventory

Let $I=\{1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17\}$ and $J=I\setminus\{5,11,13\}$. The
45 quantities are the 16 lifted angle differences and these 29 position quantities, in a
single translated frame:

$$
y_5-y_5^*,\qquad
u^*\!\cdot(r_{11}-r_{11}^*),\qquad
u^*\!\cdot(r_{13}-r_{13}^*),\qquad
(x_i-x_i^*,y_i-y_i^*)\quad(i\in J).
$$

The projections kill the slides of 11 and 13 because $u^*\cdot v^*=0$. The omitted
position quantity of square 5 is its slide.
Every angle except square 6’s remains a non-slider quantity.

For each centre, enclose the exact cover-frame value $r_i^*$ around the value
$\widehat r_i$ used by capture with $\|r_i^*-\widehat r_i\|_\infty\le E_i$. This
enclosure includes any rounding of $\sigma$. Enclose $\|u^*-\widehat u\|_1\le E_u$ and
bound $\|r_i-\widehat r_i\|_\infty\le M_i$ on the entire captured set, including the
possible slider displacement.
Then

$$
\left|u^*\cdot(r_i-r_i^*)-
\widehat u\cdot(r_i-\widehat r_i)\right|
\le E_uM_i+\|u^*\|_1E_i.
$$

Ordinary coordinate errors need only the corresponding component allowance $E_i$. For an
angle, certify the H254 lift and add an outward bound on the nominal angle error to the
delivered angle radius.
If $R_j$ is the reported radius and $E_j$ its complete conversion allowance, the
terminal check is $R_j+E_j\le1/5000$ for every component.
Do not replace $r$ by a larger radius because the root enclosure is small.
The accepted root box has tiny parameter widths, but this consumer check still needs an
explicit bound and the actual representation used.

## Finite-Angle LP

### Variables, endpoint and position domain

The primal variables are $X=((x_i,y_i)_{i\in I},S)\in\mathbb R^{33}$. They are
unrestricted solver variables; containment and domain restrictions are explicit rows.
In particular there is no solver default $x_i\ge0$ standing in for a missing row, and no
imposed upper bound $S\le S^*$. The objective is $\min S$.

Use the accepted exp-237/238 root data and the centroid layout implemented by
[`_layout`](../../../packing/devtools/check_n17_endpoint_feasibility.py).
Its nominal axes are $(e_x,e_y)$ for $1$–$5$, $7$, $8$, $15$, $17$; $(u^*,v^*)$ for
$9$–$14$; and $(p^*,q^*)$ for $16$, whose nominal angle is $-\beta$. All centre and
domain formulas below use the same chosen endpoint representation.

For a **numerical reconnaissance**, the exact rational midpoint of the accepted root box
is an allowed nominal point.
It is not the exact root.
Record the root source, the midpoint parameters, the resulting nominal side $S_0$ and
the accepted exact-side enclosure separately.
Even exact rational arithmetic at that midpoint does not certify a claim at the
algebraic endpoint.

Define the slider projections by

$$
a=x_5^*-x_5,\qquad
b=-v^*\!\cdot(r_{11}-r_{11}^*),\qquad
z=v^*\!\cdot(r_{13}-r_{13}^*).
$$

The `bounded_tube` profile has six rows placing these projections in

$$
B_W'=[0,1/4]\times[-1/2500,1/12]\times[-1/8,1/16],
$$

and 58 rows bounding each of the 29 position quantities above by $\rho_p$ in absolute
value. The registration supplies the exact rational $\rho_p$. This is the affine family
with independent non-slider position errors; it does not pin the slider coordinates to
the centroid.

The comparison profiles are nested relaxations:

| Profile | Slider rows | Position-tube rows | Purpose |
| --- | ---: | ---: | --- |
| `bounded_tube` | 6 | 58 | Declared candidate terminal region |
| `drop_sliders` | 0 | 58 | Determine dependence on slider bounds |
| `free_positions` | 6 | 0 | Determine dependence on non-slider position bounds |
| `fully_relaxed` | 0 | 0 | Bare chain and containment relaxation |

Removing rows cannot increase an optimum, branch by branch or after the outer minimum.
The two middle profiles need not be ordered relative to each other.
The historical scratch V0/V2/V3 domains are not reconstructed by assigning those names
to different rows. At a widened radius, $B_W'$ is an explicit premise: exp-248 does not
prove that every packing in the widened tube has those sliders.

### Exact finite-angle rows

A point is a vector of 16 signed rational half-angle turns $q_i=\tan(\delta_i/2)$, in
the ordered label set $I$. Define

$$
c(q)=\frac{1-q^2}{1+q^2},\qquad d(q)=\frac{2q}{1+q^2},
$$

$$
u_i=c(q_i)u_i^*+d(q_i)v_i^*,\qquad
v_i=-d(q_i)u_i^*+c(q_i)v_i^*.
$$

The actual turn is $\delta_i=2\arctan q_i$. The half-angle parameter is not an angle in
radians. For any vector $n$, the support of square $i$ is exactly

$$
h_i(n)=\frac{|n\cdot u_i|+|n\cdot v_i|}{2}.
$$

Every point has 64 containment rows:

$$
x_i\ge h_i(e_x),\quad S-x_i\ge h_i(e_x),\quad
y_i\ge h_i(e_y),\quad S-y_i\ge h_i(e_y)\qquad(i\in I).
$$

For a selected option on an ordered pair $i<j$, let its signed owner normal be $n$. Its
one complete support row is

$$
n\cdot(r_j-r_i)\ge h_i(n)+h_j(n).
$$

At fixed angles this is linear in $X$, and is the full separating-axis inequality for
that owner normal. It uses neither a tangent row nor an assumed common perturbed angle.
The support’s absolute values are evaluated at that point; a later interval certificate
must enclose them or prove their sign branches separately.
With rational nominal axes and rational $q_i$, all row coefficients and right-hand sides
can be evaluated exactly as rationals before any conversion to a numerical solver.

### Pair and feature branches

Use `CONTACTS` from
[`check_n17_contact_chart`](../../../packing/devtools/check_n17_contact_chart.py), omit
$(9,11)$, and do not add the extra $(2,3)$ pair.
Filter [`option_manifest`](../../../packing/devtools/check_n17_endpoint_features.py) to
those 19 pairs and its `identity` options.
The resulting complete roster is below; an entry $+u_k$ means the current axis of owner
$k$, not a common global $u$.

| Ordered pair | Allowed signed owner normals |
| --- | --- |
| $(1,2)$ | $+u_1$ or $+u_2$ |
| $(1,3)$ | $+v_1$ or $+v_3$ |
| $(2,13)$ | $+u_{13}$ |
| $(3,9)$ | $+v_3$ |
| $(3,11)$ | $+u_{11}$ |
| $(4,10)$ | $-v_{10}$ |
| $(5,7)$ | $+v_5$ or $+v_7$ |
| $(7,14)$ | $+v_{14}$ |
| $(8,16)$ | $-v_{16}$ |
| $(9,10)$ | $+u_9$ or $+u_{10}$ |
| $(10,12)$ | $-v_{10}$ or $-v_{12}$ |
| $(10,15)$ | $+u_{10}$ |
| $(11,12)$ | $+u_{11}$ or $+u_{12}$ |
| $(12,14)$ | $-v_{12}$ or $-v_{14}$ |
| $(12,16)$ | $+u_{12}$ |
| $(13,14)$ | $+u_{13}$ or $+u_{14}$ |
| $(14,17)$ | $+u_{14}$ |
| $(15,16)$ | $+u_{16}$ |
| $(16,17)$ | $+u_{16}$ |

There are 11 singleton and 8 binary choices, hence 27 options and $2^8=256$ raw
branches. The 21-pair inventory has 33 identities; dropping $(2,3)$ removes four and
dropping $(9,11)$ removes two.
The nine parallel pairs in the full inventory include the dropped $(9,11)$. This
explains the branch-count correction to the
[historical scope](../reviews/review-2026-10-02-n17-widened-projection-scope.md).

For manifest axes, `ex/u/p` select the owner’s $u_i$, and `ey/v/q` its $v_i$; retain the
manifest’s pair-order sign.
Sort binary pairs lexicographically and select their lower/higher owner by bit 0/1,
respectively, for reproducible branch IDs 0 through 255. One branch chooses one of the
two normals on each binary pair.
Requiring both would replace a union by an intersection and could exclude valid
packings.

The `bounded_tube` branch has 147 inequalities: 64 containment, 19 pair, 6 slider and 58
tube rows. Square 6 and all unlisted pairs are absent.
An implementation may merge exactly equal branch row systems at a particular point, but
it must retain all raw branch IDs represented by each merged solve.
Approximate equality is insufficient for a certified merge.

This branch union is necessary for a real packing only after feature forcing is proved.
The 19 pairs have 152 raw owner-axis options; the 125 omitted options must have strictly
negative separation gap throughout the declared region, or another valid argument must
cover their alternatives.
The existing local proof supplies this at its certified radius and slider domain.
A wider tube requires a new proof.
The LP may investigate the conditional selected-feature system before that proof; its
report must say that feature coverage is unproved.

### Objective, dual and coverage signs

Normalize a branch as $AX\ge b$, with $c=e_S$. Its primal and dual are

$$
L_k=\inf\{c^{\mathsf T}X:AX\ge b\},\qquad
D_k=\sup\{b^{\mathsf T}\lambda:A^{\mathsf T}\lambda=c,
\ \lambda\ge0\}.
$$

Any feasible dual gives a lower bound for its branch.
A lower-valued dual sheet does not refute a stronger bound: other feasible duals can
raise the supremum. With the solver convention $A_{\rm ub}X\le b_{\rm ub}$, use
$A_{\rm ub}=-A$, $b_{\rm ub}=-b$; nonnegative multipliers satisfy
$c+A_{\rm ub}^{\mathsf T}\lambda=0$ and give $-b_{\rm ub}^{\mathsf T}\lambda$.

The union’s value is $L=\min_{0\le k<256}L_k$. Thus a pointwise lower bound needs a
valid bound or an infeasibility certificate for every branch.
A dual sheet from one branch says nothing about the other 255. For an exactly infeasible
branch, set $L_k=+\infty$ only after checking a Farkas certificate, for example
$\lambda\ge0$, $A^{\mathsf T}\lambda=0$, $b^{\mathsf T}\lambda>0$. Every feasible branch
is bounded below: containment implies $S\ge1$. A numerical `unbounded` outcome is
therefore a model/solver diagnostic requiring investigation.

Record execution coverage separately from mathematical coverage.
All 256 branches can have terminal numerical statuses while exact bound coverage is
still absent. A numerical infeasibility report may enter a labelled heuristic
aggregation; it does not supply certified $+\infty$. If any branch is omitted, times
out, errors or has unknown solver status, retain the solved branch results and mark the
point incomplete.
A minimum over only solved branches is an observed candidate value, not
a lower bound for the full union.

A feasible primal candidate with $S<S^*$ is a possible counterexample to the proposed
relaxation bound after exact-root and row verification.
It is not a 17-square packing counterexample: square 6 and many pairs were omitted.
Failure of one numerical dual is neither kind of counterexample.

### The exact zero-turn LP

At the exact algebraic endpoint and $q=0$, every domain profile above has LP value
$S^*$. Moreover, an equality configuration belongs to the affine three-slider family,
subject to whichever domain and containment rows the profile keeps.
This is a hand consequence of the accepted stress, rather than a new numerical result.

To see it, write $h=(r-r^*,0,S-S^*)$ in the stress’s centre, angle and side columns;
square 6’s coordinates may be set to zero because its rows have zero weight.
At zero turns, each of the 52 positively weighted stress inequalities is the linear
centre/side part of one of this LP’s finite pair or active-wall inequalities, or a
nonnegative combination of such inequalities.
All eight parallel-owner alternatives coincide at these angles.
The retained constraints are tight at the endpoint, so LP feasibility implies
$A_Ph\ge0$. The
[accepted stress identity](../reviews/review-2026-10-01-n17-core-stress.md) is
$A_P^{\mathsf T}\lambda=e_S$ at the exact root, with every retained weight positive.
Consequently $S-S^*=\lambda^{\mathsf T}A_Ph\ge0$. The accepted centroid is feasible in
every profile at $S=S^*$, giving equality of the optimal value.

If $S=S^*$, positivity forces every retained inequality tight.
The retained wall contacts and the $1/2$, $1/3$, $5/7$ pairs pin squares 1, 2, 3, 4, 7
and 8 and the height of 5. The wall of 9 and the $3/9$ pair pin 9. The $9/10$ and $4/10$
pairs determine 10; $3/11$ fixes 11’s $u^*$ coordinate; $11/12$ and $10/12$ determine
12; $2/13$ fixes 13’s $u^*$ coordinate; $13/14$ and $12/14$ determine 14. The top wall
and $10/15$ determine 15; the right wall and $14/17$ determine 17; $15/16$ and $8/16$
determine 16. Only $x_5$ and the $v^*$ coordinates of 11 and 13 remain free, precisely
$(a,b,z)$. The remaining retained contacts are consistent by the endpoint identities.

This argument has the same single-author hand-review status as the centred-container
join. The numerical tool evaluates a rational root midpoint, where the closing rows can
have small residuals; it must still report those residuals rather than declaring exact
zero-turn equality from floating agreement.

## Reconnaissance and Controls

For H-277’s explicitly numerical criterion, a point can contribute positive numerical
evidence when all 256 branch statuses are `numerically_optimal` or
`numerically_infeasible`, at least one branch has a finite optimum, and the registered
primal and dual-candidate margins pass.
Record the numerical-infeasible counts and keep `bound_coverage_certified=false`. An
all-numerical-infeasible point is inconclusive.
An omitted, timed-out, erroneous, residual-failing, unknown or numerically unbounded
branch prevents positive numerical evidence.
Numerical infeasibility remains unresolved for any later proved lower bound until a
valid infeasibility certificate is checked.

### Deterministic point semantics

The registration freezes the root representation, ordered labels, branch roster,
profiles, exact rational $\rho_p$, rational half-angle radii $\tau$, direction roster,
solver settings, tolerances and wall/worker ceilings before target execution.
It may instead freeze a fully specified direction generator and seed, provided the
generated roster is retained before the target solves begin.

A direction is an explicit integer vector $d\in\mathbb Z^{16}\setminus\{0\}$. At radius
$\tau>0$, construct

$$
q_i=\tau\,d_i/\|d\|_\infty.
$$

This has actual angular infinity radius $r_a=2\arctan\tau$. Store each rational $q_i$,
not merely a rounded displayed angle.
Coordinate directions are all $\pm e_i$ for the 16 labels.
Mixed directions have at least two nonzero entries; retain separate strata for
directions supported on the seven backbone labels $\{9,10,11,12,13,14,16\}$ and
directions using the full 16-angle system.
Include signed mixtures rather than only common-angle turns.
Exact duplicate points may share one evaluation with all sample aliases retained.

Seven-angle sampling supplies no reduction of the nine other angles.
That reduction would require a separate domination argument over their complete domains.
Similarly, a finite mixed-direction roster supplies no coverage of the direction sphere.
An adaptive adversarial follow-up is a separate recorded stage with its selection rule
and consumed budget, not an undisclosed change to the frozen sample.

Report the raw nominal gap $S_{\rm LP}-S_0$ and, for nonzero turns, its ratio to $r_a$.
A comparison to the accepted side enclosure is separate.
If a quadratic ratio is useful, label $(S_{\rm LP}-S_0)/r_a^2$ explicitly; the linear
slope and quadratic ratio are different measurements.
Use complete point evaluations, with their branch counts and deduplication, when
calibrating cost. A direction/radius point is not one LP solve.

### Readiness controls

| Control | Required observation or refusal |
| --- | --- |
| Finite support | Compare selected row supports with direct extrema of all four rotated vertices, including mixed and opposite-sign turns. Pair-order reversal with $n\mapsto-n$ must preserve the inequality. |
| Synthetic objective/dual | A small retained LP with known optimum verifies the solver’s inequality convention, unrestricted variables, multiplier sign, stationarity, complementary slackness and primal/dual gap reporting. Mutating a multiplier sign or omitting its identity must be refused. |
| Roster and coverage | Assert 19 pairs, 27 allowed options, 8 binary pairs, 256 raw branch IDs, 33 variables and profile row counts. Removing one branch alias must make the point incomplete. |
| Endpoint | At $q=0$, compare the objective and the nominal centroid’s row residuals with the accepted endpoint enclosure and a declared root-rounding/solver tolerance. Record the actual residual; do not replace it by zero. Parallel-owner rows coincide here, so merged solves must still account for all 256 branches. |
| Signed turns | Construct both signs of every coordinate turn. In particular positive turn of label 16 decreases its positive parameter $\beta$; label 16’s turn is not a positive $\beta$ increment. |
| Relaxed sliders | On matched complete points, `drop_sliders` cannot have a larger optimum than `bounded_tube` beyond the declared numerical tolerance. Also compare `fully_relaxed` to each restricted profile. No particular historical negative slope is required to reproduce. |
| Slider meaning | Construct the affine family at the centroid and declared box vertices and verify that the three projections recover $(a,b,z)$ and the 29 position quantities are zero. A vertex with $b<0$ need not be a physical packing. |
| Failure preservation | Exercise timeout/unknown/error and numerical-infeasible statuses. Preserve partial branch work and refuse a complete-union lower-bound claim. |

Run endpoint and relaxed-slider controls with the same source, rows and settings used by
the target. Tolerances are registration inputs; loosening one after a failure is a new
controlled run. A failed geometric or dual-sign control suspends dependent target
interpretation.

### Degeneracy, stop rules and later proof work

Record numerical primal residuals, dual residuals, objective gaps, solver status and
active-row information per solved branch.
A solver may return different valid bases at a degenerate optimum.
Row signatures and observed basis counts describe the sample; they do not count all
possible bases or unobserved direction patches.
If a proposed unseen-basis estimator is undefined or rests on nondegeneracy that was not
checked, its forecast is `unknown`. Do not turn zero observed novelty into zero
remaining proof cost.

The ten-hour plan mentions competing 100,000- and 1,000,000-patch routing figures.
Neither is an accept/kill threshold in this contract: a sampled basis census has not
been shown to estimate certified patches.
The first retained reconnaissance reports measured complete-point cost and observed
signatures.
Any later cost hypothesis must define its estimator, degeneracy treatment and
threshold before the applicable target.

Stop a point at its registered ceiling and retain partial work.
Stop interpretation on failed controls, missing branch coverage or a provenance/domain
mismatch. Positive sampled margins can justify scoping an interval-dual instrument; they
cannot accept a widened theorem.
A verified relaxation counterexample rejects that exact row/domain bound, while leaving
open a stronger subsystem or a smaller declared region.
Any changed region, omitted option rule or sample criterion is a new contract.

A widened terminal proof would still need complete angle-region and feature coverage,
verified dual or infeasibility certificates for every allowed branch, treatment of the
apex and equality set, exact-root arithmetic, and slider-domain coverage at the widened
radius. It would then replace the terminal-region obligation in the proof table.
Outer capture from the actual closed cells would remain separate.

## Uniform Forcing of the Retained Features

This section gives sufficient exact checks for removing the 125 omitted owner-axis
options throughout the wider region.
The conclusion is conditional on the position, angle and slider bounds; it does not
establish those bounds for an arbitrary packing in the endpoint cells.

Use the complete certified `inclusion_bounds` from the accepted exp-237 root
certificate, denoted $R$, with outward rounding if needed.
Recheck the root certificate before using this enclosure.
Keep its original contraction-search box separately identified: the midpoint alone and
the search-box radius are different objects from the certified inclusion enclosure.

Set $\rho_p=1/100$, $|q_i|\le1/200$, and $w\in B_W'$. Thus
$|\delta_i|=|2\arctan q_i|\le1/100$. For each retained pair require the nominal
centre-distance bound

$$
\|x_j^*(w)-x_i^*(w)\|_2\le D=4/3.
$$

For each of its omitted owner-axis options require the nominal separation gap to be at
most $g_0=-11/200$. The
[retained checker](../../../packing/devtools/check_n17_widened_features.py) checks these
sufficient bounds over all eight closed vertices of $B_W'$ and the entire root enclosure
$R$.

### Why the finite checks cover the slider box

For fixed root parameters, the centre displacement is affine in $w$, so its squared
Euclidean norm is convex.
Bounding it by $16/9$ at the eight vertices bounds it throughout the slider box.

For an omitted option, orient the displacement from the owner to the other square.
When the owner is the right endpoint of the stored ordered pair, negate the stored axis
sign as well. If $n$ is this signed owner normal, the support gap equals

$$
\min_{c\text{ a corner of the other square}}
\bigl(n\cdot(x_{\rm other}^*(w)+c-x_{\rm owner}^*(w))-1/2\bigr).
$$

Choose one corner at the nominal midpoint and keep that same corner for all slider
vertices and the whole root enclosure.
Its expression is affine in $w$. If its upper interval endpoint is at most $-11/200$ at
every vertex, it bounds the full support gap throughout the box.
The chosen corner need not remain the minimizing corner.
This is an upper bound because the full gap is the minimum of all four expressions.

The check accounts for every omitted option of the 19 retained pairs: 125 options, eight
slider vertices each, and 19 distance checks at eight vertices.
Completeness of these rosters is part of the certificate.
A certificate for a smaller position, angle or slider domain does not discharge this
fixed contract.

### The finite-angle loss

Write an actual centre as $r_i=x_i^*(w)+e_i$. The 29 position bounds give
$\|e_i\|_2\le\sqrt2\rho_p$; for labels 5, 11 and 13 the sharper bound is $\rho_p$. For
an owner-axis option the owner’s support is always $1/2$. The other square’s support in
that axis is

$$
h(\phi)=\tfrac12(|\cos\phi|+|\sin\phi|).
$$

This function is globally $1/2$-Lipschitz: its derivative has absolute value at most
$1/2$ on each open quadrant, and it is continuous at the quadrant boundaries.
The relative-angle change is at most $2/100$, so the other support changes by at most
$1/100$. Rotation of the owner normal changes its projection of the nominal displacement
by at most $D/100$; position errors add at most $2\sqrt2/100$. Consequently every
omitted gap is at most

$$
-\frac{11}{200}+\frac{2\sqrt2}{100}+\frac{D+1}{100}
< -\frac{11}{200}+\frac{2(99/70)}{100}+\frac{4/3+1}{100}
=-\frac{71}{21000}<0.
$$

The rational square-root allowance is valid because $(99/70)^2>2$. No angle grid is used
in this implication.
Once the finite nominal checks pass, every nonoverlapping pair in the specified wider
region must use one of its retained options.
Hence any physical packing there lies in one of the 256 selected-feature branches.
This proves neither a side bound for those branches nor capture into the wider region.

## An Apex Bound from the Retained Position Duals

A finite collection of positive-angle patches cannot cover all angles approaching zero.
The following bound supplies a candidate inner cube without solving a new LP. Its exact
arithmetic checks are implemented by the
[apex checker](../../../packing/devtools/check_n17_widened_apex.py); the finite-geometry
implication in this section remains a hand proof.

Work in the declared fixed container $[0,S^*]^2$. This is legitimate for a smaller
packing by the centred-container lemma.
The argument has side increment zero; it is not a bound for an LP whose side variable
remains unrestricted.

Let $p\in\mathbb R^{29}$ be the non-slider position coordinates, let $M=\|p\|_\infty$,
and let $\alpha=\max_i|\delta_i|$. Suppose the wider-region hypotheses above hold,
including $w\in B_W'$. Let $T$ be the 52 positive local rows restricted to the 29
position lifts: remove all angle columns and the side-increment column.

### Tightness and independence from the sliders

All 52 positive rows are tight at every $x^*(w)$ in $B_W'$. For the 27 retained owner
options, `slide_invariance_audit` in the
[local checker](../../../packing/devtools/check_n17_local_minimum.py) proves the nominal
support gap is independent of the sliders as a rational identity.
H-257 supplies its zero value at the exact root.
C10 supplies the active-wall identities.
An interval enclosing zero at a rational midpoint is not a substitute for these
identities.

The position coefficients of a wall row are signed coordinate vectors, and those of a
pair row are its nominal normal on the two centres.
All slider-dependent moments in `generic_face_rows` occur in angle columns.
Thus $T$ is independent of $w$, even though the full local matrix is not.
The three slide directions are annihilated: label 5 moves along its bottom wall and its
vertical 5/7 contact; labels 11 and 13 move along $v$, perpendicular to the $u$ normals
of their retained contacts.
No unchanged full centroid stress is assumed.

For a parallel pair, either retained owner option has the same nominal position row.
Thus one finite separating option implies the estimate below for both local rows of that
pair. This is why their different angle columns cause no difficulty after projection to
$T$.

### The finite-geometry inequality

Containment and retained-feature separation imply

$$
T_i p\ge-L_i\alpha,
\qquad
L_i=\begin{cases}1/2,&i\text{ a wall row},\\12/5,&i\text{ a pair row}.
\end{cases}
$$

For a wall, the support change is at most $\alpha/2$. For a pair, compare its actual
separating normal with the nominal normal at the actual centres.
Their distance is at most $D+2\sqrt2\rho_p$, and the other-square support changes by at
most $\alpha$. The total loss is at most

$$
(D+2\sqrt2\rho_p+1)\alpha<\frac{12}{5}\alpha.
$$

Root tightness and slide invariance identify the remaining nominal gap with $T_i p$.
These inequalities use the selected finite separation, not tangent feasibility assumed
for a finite perturbation.

### Exact dual residuals and the resulting inner cube

Use the 58 signed position-direction certificates from exp-248 `run-002`. For each
direction $(s,j)$, select the lexicographically first closed slider cell containing
$w_0=(0,0,0)$ and evaluate its affine multiplier exactly there:

$$
\lambda_i=\operatorname{lam}_i-
\sum_{k=1}^3\operatorname{centre}_k\operatorname{mu}_{ki}.
$$

The retained numerators have denominator $2^{44}$. Check all 52 resulting multipliers
are nonnegative. Only these constant weights are reused; independence of $T$ from $w$
makes them applicable throughout $B_W'$. Over the full root enclosure compute

$$
r_{s,j}=\lambda_{s,j}^{T}T+s e_j^T,
\qquad
\epsilon_{s,j}=\sum_{k=1}^{29}\sup_R|r_{s,j,k}|,
\qquad
C_{s,j}=\sum_{i=1}^{52}\lambda_{s,j,i}L_i.
$$

Set $\epsilon=\max_{s,j}\epsilon_{s,j}$ and $C=\max_{s,j}C_{s,j}$. Require $\epsilon<1$
and $C>0$. Multiplication of the finite-geometry inequalities by $\lambda_{s,j}$ gives

$$
-s p_j+r_{s,j}p\ge-C_{s,j}\alpha,
\qquad
s p_j\le C\alpha+\epsilon M.
$$

The row $\ell^1$ residual is essential: it bounds $|r_{s,j}p|$ by $\epsilon M$.
Maximizing over both signs of all 29 coordinates yields

$$
M\le\frac{C\alpha}{1-\epsilon}.
$$

Freeze the sufficient radii

$$
\alpha_0=\min\left\{\frac1{5000},
\frac{1-\epsilon}{10000C}\right\},
\qquad q_0=\alpha_0/2.
$$

If $\|q\|_\infty\le q_0$, then $\alpha\le\alpha_0$, the position coordinates are at most
$1/10000$, and every one of the 45 non-slider coordinates is at most $1/5000$. The
accepted local theorem therefore forces the retained squares onto the endpoint family.
The wider slider-domain premise has been retained explicitly; the old slider-coverage
theorem has not been applied at radius $1/100$.

The certificate checks the complete 58-direction, 52-row, 29-column roster, nonnegative
multipliers, root-domain identity, residuals and radius formulas.
Root tightness, slide invariance, the finite-geometry inequality and the accepted local
theorem remain named premises.
Its immediate conclusion concerns physical packings satisfying those premises.
Extending the conclusion to every point in the selected LP union requires an explicit
reuse of the local recipe’s proof, rather than a broader reading of its stated packing
theorem.

## Exact Certificates on the Remaining Angle Region

After an accepted apex certificate, a widened terminal proof still needs to cover the
compact annulus

$$
q_0\le\|q\|_\infty\le1/200
$$

in all 16 half-angle variables, including closed patch boundaries.
The interval method below permits both finite LP duals and infeasibility multipliers.
A sampled point or a certified patch is only its declared subset of this annulus.

Fix a rational closed angle box $Q$ and a selected-feature branch.
Substitute the exact fixed side $S^*$ into its finite inequalities and write

$$
A(q,R)r\ge b(q,R).
$$

The centre domain is $r=x^*(w)+Pp$, with $w\in B_W'$ and $p\in[-\rho_p,\rho_p]^{29}$.
Here $P$ is the exact-root matrix of position lifts.
Take a retained, nonnegative rational multiplier vector $\lambda$ and set
$a=\lambda^TA$, $d=\lambda^Tb$. A sufficient contradiction certificate is

$$
\eta=
\min_{v\in\operatorname{Vert}(B_W')}
\inf_{(q,R)\in Q\times R}\bigl(d-a\,x^*(v)\bigr)
-\rho_p\sum_{j=1}^{29}
\sup_{(q,R)\in Q\times R}|aP_j|>0.
$$

Indeed, feasibility would give $ar\ge d$, whereas the affine slider box and the position
box give $ar<d$. This charges a nonzero stationarity residual to an explicit bounded
centre domain. It requires neither exact cancellation of $a$ nor an interval matrix
inverse. Evaluate the expressions with outward exact interval arithmetic, including all
absolute-value supports and the accepted root enclosure.
Keep the root parameter and angle-box meanings separate.

A positive sampled side dual can propose $\lambda$ after the fixed-side substitution.
An all-numerical-infeasible sample instead needs a retained Farkas candidate; its solver
status supplies no multiplier or exact contradiction.
Rationalizing a candidate and failing the strict interval check is an unresolved patch,
not evidence of a feasible packing.

The same certificate can cover several feature branches.
Give every pair row a stable pair index and enclose both allowed owner rows wherever
that pair has two options.
If the strict check succeeds using these row enclosures, it holds for all their
combinations. Otherwise split the owner choices or retain separate multipliers.
This interval enclosure is a conservative proof device, not a claim that differing owner
rows are algebraically equal.

An eventual annulus receipt must identify every covered closed box and every covered
owner branch, with a mechanically checked cover of the declared annulus.
Unknown branches, nonpositive margins, uncovered seams and exhausted budgets remain
unresolved. The apex and annulus together would give a conditional widened terminal
result on the fixed position and slider domain.
Outer capture must still map each remaining closed-cell packing into that domain, with
exact frame and root allowances, or exclude it.
A successful terminal certificate does not remove any global residue state by itself.

## Widened Slider Bounds and Capture Leaves

The new terminal contracts use $B_W'$ as an explicit premise.
The existing
[slider-coverage checker](../../../packing/devtools/check_n17_slider_coverage.py) proves
this premise at the original radius $1/5000$; increasing the position and angle radii to
$1/100$ changes its inequalities.
Two faces illustrate what can and cannot be reused directly.

The lower face $a\ge0$ is independent of the radius.
In the fixed container, $x_5=S^*-1/2-a$ and the square’s horizontal reach is
$h(\delta_5)\ge1/2$. Therefore containment gives

$$
a\ge h(\delta_5)-1/2\ge0.
$$

For the lower face of $b$, separate the position and angle bounds.
Write $|\delta_{9}|,|\delta_{11}|\le\alpha$, $|\xi_9|\le\rho_{9x}$,
$|\eta_9|\le\rho_{9y}$ and $|u^*\cdot(r_{11}-x_{11}^*)|\le\rho_{11}$. In the notation of
`b_floor`, $D_0=1$ and $\tau_0=c(s-1)<0$, where $(c,s)=u^*$. Once the separating-axis
lemma’s three hypotheses have been checked over a previously justified coarse slider
domain, it gives

$$
\begin{aligned}
b\ge {}&\sec\alpha-D_0+\tau_0\tan\alpha-\rho_{11}\tan\alpha\\
&-\rho_{9x}|\tan\alpha\,u_x^*-v_x^*|
-\rho_{9y}|\tan\alpha\,u_y^*-v_y^*|.
\end{aligned}
$$

For a rational half-angle bound $0\le\bar q<1$, take $\alpha=2\arctan\bar q$. Then
$\sin\alpha=2\bar q/(1+\bar q^2)$, $\tan\alpha=2\bar q/(1-\bar q^2)$ and
$\sec\alpha=(1+\bar q^2)/(1-\bar q^2)$ are rational; the root-dependent terms can be
enclosed over $R$.

This sufficient estimate cannot supply $b\ge-1/2500$ for the uniform wider position
bounds.
Indeed, with $\rho_{9x}=\rho_{9y}=1/100$ and $\bar q=1/200$, orthonormality gives
$\|\tan\alpha\,u^*-v^*\|_1\ge\sec\alpha$. The displayed lower-bound expression is
therefore at most

$$
\frac{99}{100}\frac{40001}{39999}-1
=-\frac{39801}{3999900}<-\frac1{2500}.
$$

This is a limitation of that estimate, not a packing counterexample.
A successful widened join must obtain the missing slider faces by direct capture bounds,
a new slider certificate, or additional bounds on selected position and angle
coordinates. For example, narrower bounds on squares 9 and 11 can be inserted into the
displayed formula while other coordinates retain their wider bounds.
The direction-exclusion hypotheses and any coarse upper bound on $b$ must be proved
before applying it.
Using the desired slider conclusion to justify those hypotheses would
be circular.

### A conditional terminal leaf

Let $\mathcal P$ be the original counterexample domain: labelled packings in $C(S^*)$
with the chosen closed-cell assignment and the retained square-6 premise.
A producer may use the larger rational container $C(U')$, whose feasible set contains
$\mathcal P$. For each retained closed leaf $L$, require either a verified exclusion of
$L$, or a verified implication

$$
\mathcal P\cap L\ \subseteq\ \mathcal T,
$$

where $\mathcal T$ is the exact terminal theorem’s complete domain.
This allows the terminal implication to use the original $C(S^*)$ containment as well as
the producer’s leaf bounds.
In particular $a\ge0$ follows for the target packing, although it need not hold for
every extra configuration allowed by $C(U')$. The consumer must record this conditional
premise explicitly.

The retained leaf evidence must identify its original cell state, transported labels and
D4 action, root and angle frame, square-6 cell, all 29 position functionals, all 16
angle bounds, and the six slider-face inequalities or their separate geometric
implications. A scalar extent statistic does not supply these items.
Every root/frame allowance must be charged before the final closed-bound comparison.
The tree must cover the original cells through all closed splits; an open frontier
remains unresolved even if every completed leaf has a valid terminal implication.

For states other than the endpoint representative, a terminal invocation also needs an
explicit relabelling and the square-6 premise it uses.
The endpoint’s unique occupancy result concerns its declared family domain; it does not
assign nearby arbitrary packings to that state.
Excluding other residue states and capturing the endpoint state remain separate
obligations unless a certificate supplies the full geometric and assignment join.

### Half-angle transport without rounded inverse trigonometry

After applying the declared D4 symmetry, choose a quarter-turn-equivalent oriented unit
axis $e_i$ for each retained square.
With its exact-root nominal axis $u_i^*$, set

$$
c_i=u_i^*\cdot e_i,\qquad s_i=\det(u_i^*,e_i),\qquad
q_i=\frac{s_i}{1+c_i}.
$$

Certify $1+c_i>0$ on the leaf.
This is the half-angle parameter of the principal relative turn, so enclosing $c_i,s_i$
and the quotient gives an exact interface to the terminal $q$ bounds without a rounded
`atan` calculation. The leaf must retain its quarter-turn choice or cover all applicable
choices through closed branches.
A source angle-chart identifier alone does not identify the H-254 lift.

For a reflection $g$, taking $e_i=g(u_i)$ requires the positively oriented second axis
$J e_i=-g(v_i)$, where $J$ is counterclockwise rotation by $\pi/2$. Keeping the
reflected ordered basis unchanged would reverse the angle convention.
Changing this second-axis sign leaves the square itself unchanged and makes the
half-angle formulas consistent with the terminal rows.

### A bounded leaf-consumer contract

A leaf consumer can check the preceding interfaces before an expensive capture campaign
exists.
Its input is a closed leaf domain tied to a separately verified producer receipt,
with exact centre polygons, complete orientation-chart unions, cover cells, a label
bijection and a fixed D4 transformation.
Convert producer field coordinates to physical unit-square coordinates using the
declared scale before applying the cover-frame symmetry and root-dependent translation.
All position and slider thresholds use these physical units.

For each position or slider functional, bound every centre-polygon vertex over the
entire root enclosure.
For each orientation-chart piece, retain its quarter-turn choice and certify the whole
relative half-angle interval.
If a chart is split, its retained closed subpieces must cover it.
Missing pieces cannot be replaced by sampling or by a favourable endpoint.
Square 6 keeps its complete angle domain.

The consumer distinguishes the following predicates; it does not infer a global state
closure from any one leaf.

| Predicate | Required bounds and theorem join | Meaning |
| --- | --- | --- |
| Local terminal | All 29 position bounds are at most $1/5000$ and all 16 half-angle bounds at most $1/10000$; original $C(S^*)$ containment and square 6’s cell premise hold. | The exact angle is at most twice the half-angle magnitude, so all 45 coordinates meet the accepted radius and the local composition applies. |
| Wide domain only | Position bounds are at most $1/100$, half-angle bounds at most $1/200$, and every face of $B_W'$ has an independent justification. | The wider-domain premise has been checked; no terminal theorem follows from these bounds alone. |
| Apex terminal | The wide-domain predicate holds, an accepted apex receipt is joined, and every half-angle bound is at most its $q_0$. | Invoke the conditional apex argument and the accepted local theorem. |
| Patch exclusion | The wide-domain predicate holds, an accepted exact patch receipt is joined, and the entire leaf angle product lies in that receipt’s closed box. | The fixed-container branch subsystem is infeasible throughout the leaf’s target-packing intersection. |

Direct slider projection bounds can establish all six faces of $B_W'$. Alternatively the
lower $a$ face can use the original-container lemma above.
The other faces require their own bounds or accepted geometric certificates; a widened
position radius does not invoke the old slide-coverage result.
The local-terminal route uses square 6’s cell to obtain slide coverage.
The apex and patch proofs, once the slider box is supplied independently, concern the
sixteen retained squares.
A first consumer may conservatively retain the square-6 cell premise for every terminal
route without enlarging any existing claim.

Valid bounds outside the accepted terminal or exclusion domains remain unresolved.
An open input or split frontier is incomplete.
A missing root, frame, label, producer-coverage or theorem-premise binding is refused.
Reproducing a leaf descriptor is not verification that every original cell-state packing
reaches it. The consumer’s contribution is the exact conversion and conditional theorem
join; outer capture remains a separate certificate obligation.

## A Homogeneous Cone from the Soft-Direction Dual

The sixteen nonzero rows of exp-260’s finite dual for the negative turn of square 16
suggest a telescoping identity.
H-283's exp-267 subsequently accepted the exact finite checks in both its
[certificate](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-267-continuous-soft-direction-cone/certificate.json)
and [fresh replay](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-267-continuous-soft-direction-cone/replay.json).
The analytic perturbation argument below remains a sole-Astra hand derivation, without
independent mathematical review or formal verification. Its declared domain is one
cone times six free angle coordinates, not a cover of all directions.

Write $(c,s)=u^*$ and $(d,-e)=p^*$, with $c,s,d,e>0$. Let $x=x_{15}^*$ and $y=y_{17}^*$
be the endpoint coordinates appearing in the contact chart, and set

$$
A=S^*-x-3/2,\qquad B=S^*-y-3/2,\qquad K=-eA+dB.
$$

The accepted exact contact identity F2 is $dA+eB=1$. This exact identity is essential
below.
An interval enclosing a small nonzero residual cannot replace it: a constant error
would dominate a bound proportional to an arbitrarily small turn.

### Two contact chains

First fix every angle other than square 16’s at its nominal value.
The walls and contacts $1/2$, $2/13$, $13/14$, $14/17$ give

$$
c x_{17}+s y_{17}\ge 2+\tfrac52c+\tfrac32s.
$$

Using $x_{17}\le S^*-1/2$ yields $y_{17}\ge y$. Independently, the left wall of 9 and
the chain $1/3$, $3/9$, $9/10$, $10/15$ give

$$
c x_{15}+s y_{15}\ge2+cs+\tfrac12c+\tfrac52s.
$$

Using $y_{15}\le S^*-1/2$ yields $x_{15}\ge x$. These inequalities follow from the
selected finite rows and require no slider or position-tube restrictions.
Each binary owner choice in these chains has the same nominal normal when both owner
angles are zero.

Let $q_{16}=-r$, where $0<r\le1/200$, and put $\alpha=2\arctan r$. Square 16’s axis is
$(d_r,-e_r)$, where

$$
d_r=\frac{d(1-r^2)-2er}{1+r^2},\qquad
e_r=\frac{e(1-r^2)+2dr}{1+r^2}.
$$

If $d_r,e_r>0$, the two owner-16 rows $15/16$ and $16/17$ imply

$$
d_r(x_{17}-x_{15})-e_r(y_{17}-y_{15})\ge1+d_r+e_r.
$$

The preceding chain bounds and the top/right walls therefore require $d_r A+e_r B\ge1$.
But F2 gives the exact identity

$$
d_r A+e_r B-1
=\cos\alpha+K\sin\alpha-1
=\frac{2r(K-r)}{1+r^2}.
$$

Thus $K<0$ would exclude this entire punctured axis in the selected-feature subsystem,
uniformly over all centre positions.
Feature forcing is still needed to infer the selected rows from a physical packing.

### Explicit nonnegative weights

The argument is a positive combination of the following sixteen finite gaps
$g_i=A_i r-b_i$. Every omitted row receives weight zero.
A pair’s alternative retained owners use the same weight.

| Row | Weight |
| --- | --- |
| Left wall of 1 | $e_r c/s$ |
| Bottom wall of 1 | $d_r s/c$ |
| Bottom wall of 2 | $e_r$ |
| Left wall of 9 | $d_r$ |
| Top wall of 15 | $e_r+d_r s/c$ |
| Right wall of 17 | $d_r+e_r c/s$ |
| Pair $1/2$ | $e_r c/s$ |
| Pair $1/3$ | $d_r s/c$ |
| Pair $2/13$ | $e_r/s$ |
| Pair $3/9$ | $d_r s/c$ |
| Pair $9/10$ | $d_r/c$ |
| Pair $10/15$ | $d_r/c$ |
| Pair $13/14$ | $e_r/s$ |
| Pair $14/17$ | $e_r/s$ |
| Pairs $15/16$ and $16/17$ | $1$ each |

At the baseline angles, the centre coefficients cancel exactly and
$\sum_i\lambda_i g_i=d_r A+e_r B-1$. Dividing these weights by $(c+s)(d_r/c+e_r/s)$
normalizes the side coefficient to one, explaining their relation to the retained LP
dual. The proof uses the exact weights above, not a numerical equality with that dual.

### Thickening the axis to a cone

Now retain the wider position and slider premises and allow

$$
q_{16}=-r,\quad 0<r\le1/200,\quad
|q_j|\le\varepsilon r\quad
(j\in\{1,2,3,9,10,13,14,15,17\}),\qquad \varepsilon=1/2048.
$$

The six remaining labels $\{4,5,7,8,11,12\}$ occur in none of the weighted rows.
Their half angles may range independently over the entire interval $[-1/200,1/200]$. The
feature-forcing premise still uses the outer angle bound for all sixteen labels.
A checker should reconstruct the weighted-row label roster to verify this independence.
Thus the proposed domain is a cone in ten angle coordinates times a full cube in six
coordinates; requiring all fifteen non-16 angles to be small would give a valid but
unnecessarily restrictive subset.

Relative to the baseline at the same $r$, the other angle changes in weighted rows are
at most $2\varepsilon r$. Each of the six weighted wall gaps increases by at most
$\varepsilon r$. For the eight weighted pairs not involving 16, either allowed owner
choice gives a gap increase at most

$$
2(D+2\sqrt2\rho_p+1)\varepsilon r
<\frac{24}{5}\varepsilon r.
$$

This uses the verified nominal pair-distance bound and the same support Lipschitz
argument as the apex proof.
In the two pairs owned by 16, the owner normal is unchanged from the baseline; only the
other square turns. Each gap therefore increases by at most $\varepsilon r$.

Define the total wall weight and the eight-pair weight by

$$
W=2(c+s)(d_r/c+e_r/s),\qquad
P=e_r c/s+2d_r s/c+3e_r/s+2d_r/c,
$$

and set $M=W+(24/5)P+2$. The proposed exact finite checks are

$$
K\le-1/50,\qquad M\le50
$$

over the complete accepted root enclosure and $r\in[0,1/200]$, together with strict
positivity of $c,s,d_r,e_r$ and the exact chain identities.
If they pass, every allowed branch in this cone satisfies

$$
\sum_i\lambda_i g_i
\le-\left(\frac{1600}{40001}-\frac{25}{1024}\right)r
=-\frac{638375}{40961024}\,r<0.
$$

Feasibility would make every selected gap nonnegative, so this is a contradiction.
The estimate covers all 256 owner combinations and all positive radial scales in the
cone. The apex $r=0$ is retained; the accepted zero-angle or apex argument treats it.
No claim excludes the endpoint itself.

A retained checker should reconstruct the sixteen weights, verify their centre and side
coefficient identities, join F2 to its accepted exact-root proof, and enclose $K,M$ and
the positive denominators by outward rational arithmetic.
Freeze the constants and complete root/radial domains before checking them.
Failure of a sign, mass or premise check leaves this proposed cone uncertified; it is
not evidence of a packing in the cone.
Passing would add one continuous cone to the coverage record, while the remaining
angular directions and outer capture stay open.

## A Separate Positive-Turn Cone Contract

The retained exp-260 point `target:outer:coordinate:16:1` has a different dual support.
Its seventeen positive rows led to the following further hand derivation.
H-284's exp-269 accepted the exact finite checks in its
[certificate](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-269-positive-continuous-cone/certificate.json)
and [fresh replay](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-269-positive-continuous-cone/replay.json).
The analytic implication remains a sole-Astra hand derivation, without independent
mathematical review or formal verification.
This certificate is separate from the negative-turn cone: D4 transport does not establish
the positive-turn claim in the same labelled endpoint frame.

Put $q_{16}=r$, with $0<r\le1/200$, and define

$$
d_r=\frac{d(1-r^2)+2er}{1+r^2},\qquad
e_r=\frac{e(1-r^2)-2dr}{1+r^2},\qquad
\alpha_r=cd_r-se_r,\qquad \gamma_r=ce_r+sd_r.
$$

All four quantities must be strictly positive on the checked root and radial domains.
Write $Y=y_{17}^*$ and set

$$
C_r=d_r(S^*-1)-e_r(Y+1/2)-1/2,\qquad
B_r=(d_r+e_r)(S^*-1)-1/2.
$$

At the baseline where every other angle is nominal, the right contact chain from the
preceding section gives $y_{17}\ge Y$. The two upper walls of square 8, the right wall
of 17, and the contacts $8/16$ and $16/17$ therefore give

$$
(e_r,d_r)\cdot x_{16}\le B_r,\qquad
(d_r,-e_r)\cdot x_{16}\le C_r.
$$

The bottom wall of 1, the left wall of 3, and contacts $1/3$, $3/11$, $11/12$ and
$12/16$ give

$$
u^*\cdot x_{16}\ge c+2s+2+(\alpha_r+\gamma_r)/2.
$$

Since $u^*=\alpha_r(d_r,-e_r)+\gamma_r(e_r,d_r)$, feasibility requires

$$
G(r):=\alpha_r(C_r-1/2)+\gamma_r(B_r-1/2)-(c+2s+2)\ge0.
$$

### Seventeen weights and the exact root join

The positive combination has the following weights.
All other rows have weight zero; alternative retained owners receive the same pair
weight.

| Row | Weight |
| --- | --- |
| Left wall of 1 | $ce_r\alpha_r/s$ |
| Bottom wall of 1 | $s$ |
| Bottom wall of 2 | $e_r\alpha_r$ |
| Left wall of 3 | $c$ |
| Right wall of 8 | $e_r\gamma_r$ |
| Top wall of 8 | $d_r\gamma_r$ |
| Right wall of 17 | $\alpha_r\gamma_r/s$ |
| Pair $1/2$ | $ce_r\alpha_r/s$ |
| Pair $1/3$ | $s$ |
| Pair $2/13$ | $e_r\alpha_r/s$ |
| Pairs $3/11$, $11/12$ and $12/16$ | $1$ each |
| Pair $8/16$ | $\gamma_r$ |
| Pairs $13/14$ and $14/17$ | $e_r\alpha_r/s$ each |
| Pair $16/17$ | $\alpha_r$ |

The centre coefficients cancel, the side coefficient is $\gamma_r(d_r+e_r+\alpha_r/s)$,
and the fixed-container weighted gap is $G(r)$. These are symbolic identities to check
against reconstructed finite support rows.
In particular, the $12/16$ row is owned by square 12; it is not an owner-16 row.

At zero turn, $C_0=A_{\rm chart}+F2$, where $A_{\rm chart}$ is the coordinate named `A`
in the endpoint layout, and $B_0=B_{\rm chart}$. Consequently

$$
G(0)=F3+\alpha_0 F2=0
$$

at the accepted exact root.
Both polynomial normalizations must be joined to that root: F2 to Pi2 and F3 to Pi3.
Interval residual smallness again cannot replace exact zero.
Symbolically form the polynomial

$$
H(r)=\frac{(1+r^2)^2\,[G(r)-G(0)]}{r}.
$$

Its numerator has an exact factor $r$, leaving a polynomial of degree at most three.
A checker must cancel that factor symbolically and interval-evaluate the resulting
polynomial on the closed interval $[0,1/200]$. It must not divide an interval by $r$ at
zero. The registered and accepted finite criterion is $H\le-1/2$ throughout that domain.

An explicit coefficient form avoids division by $r$. Put $T=S^*-1$, $Z=Y+1/2$ and

$$
A_2=(c+s)T,\quad B_2=c(T-Z),\quad C_2=sZ+cT,
$$

$$
Q_0=A_2d^2+B_2de+C_2e^2,\quad
Q_{90}=A_2e^2-B_2de+C_2d^2,\quad
Q_\times=2de(A_2-C_2)+B_2(e^2-d^2),
$$

$$
L_0=(c+s)d+(c-s)e,\qquad L_\times=(c+s)e-(c-s)d.
$$

Then the coefficient list, from constant to cubic, is

$$
\bigl(2(Q_\times-L_\times),\;
4(Q_{90}-Q_0)+2L_0,\;
-2(Q_\times+L_\times),\;
2L_0\bigr).
$$

A symbolic check should bind this list to the preceding definition of $H$ before outward
interval evaluation of its coefficients and radial powers.

### Checked mixed-angle domain

The weighted rows involve labels $\{1,2,3,8,11,12,13,14,16,17\}$. The cone
constrains the nine non-16 labels in that set by $|q_j|\le r/128$, while
$\{4,5,7,9,10,15\}$ retain the full outer half-angle interval.
The wider position, slider and feature-forcing premises remain explicit.

Let $W$ be the sum of the seven wall weights and let

$$
P=ce_r\alpha_r/s+s+3e_r\alpha_r/s+2
$$

be the sum of the seven pair weights not involving 16. Those pair gaps each change by at
most $(24/5)(r/128)$. For $12/16$, only the owner turns relative to the baseline; its
gap changes by at most $(19/5)(r/128)$, using $2(D+2\sqrt2\rho_p)+1<19/5$. The owner-16
rows $8/16$ and $16/17$ each change by at most $r/128$. The accepted finite mass bound is

$$
M_+=W+(24/5)P+19/5+\gamma_r+\alpha_r\le50.
$$

The accepted sign checks, exact root joins, $H\le-1/2$ and this mass bound give

$$
\sum_i\lambda_i g_i
\le-\left[\frac{1}{2(1+1/40000)^2}-\frac{50}{128}\right]r
=-\frac{11197999975}{102405120064}\,r<0.
$$

With the stated hand implication, this excludes the second punctured cone times six
free angle coordinates. Its apex and all remaining directions remain subject to the
existing terminal and coverage obligations. In particular, the two cones do not cover
the hyperplane $q_{16}=0$ outside the apex region, or arbitrary mixed-angle directions.

## A Noncircular Lower Slider Bound for Capture Leaves

The wider position tube alone did not establish the lower $b$ face of $B_W'$.
The following new hand derivation supplies a sufficient capture-leaf predicate using
one additional position projection and one-sided angle bounds.
H-285's exp-270 accepted the finite root guard and rational inequalities in its
[certificate](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-270-coarse-slider-floor/certificate.json)
and [fresh replay](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-270-coarse-slider-floor/replay.json),
with a combined measured wall cost of 1.08 seconds.
The geometric implication remains a sole-Astra hand derivation, without independent
mathematical review or formal verification; no actual leaf's premises have been checked.
It uses physical non-overlap of squares 9 and 11 before invoking the widened feature
certificate and does not assume membership in $B_W'$.

Let $u=(c,s)$ and $v=(-s,c)$ be the nominal root axes. The endpoint layout satisfies the
symbolic identity

$$
x_9^*-x_{11}^*=\tau_0u+v,\qquad \tau_0=c(s-1).
$$

Write $e_9=x_9-x_9^*$ and
$x_{11}-x_{11}^*=\eta_{11}u-bv$, where $b$ and $\eta_{11}$ are the usual exact root
projections. Consider the following sufficient premises:

| Quantity | Required bound |
| --- | --- |
| Root guard | $-1/3\le\tau_0\le-1/8$ |
| Existing wide position bounds | $|(e_9)_x|,|(e_9)_y|\le1/100$ and $|\eta_{11}|\le1/100$ |
| Additional direct projection | $|v\cdot e_9|\le1/5000$ |
| Coarse slider bound | $-1/2\le b\le1/12$ |
| One-sided half-angle bounds | $-1/200\le q_9,q_{11}\le1/5000$ |
| Physical premise | Squares 9 and 11 have disjoint interiors. |

All other position and angle coordinates may retain their wider bounds. The two angle
intervals need not be symmetric about zero. The additional position bound should be
computed directly on each residual polygon in the root $v$ direction; forming an
axis-aligned bounding box first can discard the thin direction that makes it useful.

### Independent forcing for the 9/11 pair

For $\Delta=x_9-x_{11}$, put $U=u\cdot\Delta$ and $V=v\cdot\Delta$. Then

$$
U=\tau_0+u\cdot e_9-\eta_{11},\qquad
V=1+b+v\cdot e_9.
$$

Using $\sqrt2<99/70$, the premises give

$$
-9/25<U<0,\qquad
V_{\min}:=1/2-1/5000\le V\le13/12+1/5000=:V_{\max}.
$$

For example, $1/3+99/7000+1/100<9/25$, while
$-1/8+99/7000+1/100<0$. These inequalities do not use the desired lower face of $B_W'$.

Let $Q_0=1/200$,
$C_0=(1-Q_0^2)/(1+Q_0^2)$ and $S_0=2Q_0/(1+Q_0^2)$. Either square's actual axis is
obtained by a turn $\delta_i=2\arctan q_i$, so $\cos\delta_i\ge C_0>0$ and
$|\sin\delta_i|\le S_0$. The four signed $u$-axis separation possibilities have
projection at most

$$
9/25+S_0V_{\max}<1.
$$

The two negative $v$-axis possibilities have projection at most

$$
S_0(9/25)-C_0V_{\min}<1.
$$

The sum of the two unit-square supports along any owner axis is at least one.
Those six directions therefore cannot separate the pair. The separating-axis criterion
for disjoint square interiors leaves at least one of the two positive $v$ directions:

$$
\cos\delta_i\,V-\sin\delta_i\,U\ge1
\quad\text{for some }i\in\{9,11\}.
$$

This forcing argument has its own coarse domain. Reusing H-278 here would be circular,
because H-278 assumes the very slider box whose lower face is being established.

### The lower face and its exact margin

Dividing the preceding inequality by its positive cosine gives

$$
b\ge\sec\delta_i-1+\tan\delta_i\,U-v\cdot e_9.
$$

If $\delta_i\le0$, then $\tan\delta_i\,U\ge0$ because $U<0$. If $\delta_i\ge0$,
the one-sided upper half-angle bound gives

$$
\tan\delta_i\le\frac{2/5000}{1-1/5000^2}
=\frac{10000}{24999999}.
$$

In both cases, using $\sec\delta_i-1\ge0$ yields

$$
b\ge-\frac1{5000}-\frac{3600}{24999999}
=-\frac1{2500}+\frac{6999999}{124999995000}
>-\frac1{2500}.
$$

The positive margin is exact. The retained checker binds the displacement identity to
the endpoint chart, verifies the root guard over the complete accepted root enclosure,
and recomputes all eight direction cases, the six exclusions, the two survivors and the
lower-face inequalities. Its accepted strict headroom is $2333333/41666665000$.

### Consumer scope

For a freshly replayed capture leaf, retain the raw $b$ interval and all direct projection
and chart bounds. If every premise above holds, the target-packing intersection may use
an effective $b$ lower endpoint equal to the maximum of the raw lower endpoint and the
proved geometric floor. Its upper endpoint remains the raw one. The remaining slider
faces still need their own direct bounds or accepted implications; in particular this
argument does not clip $z$ or establish the upper $a$ face.

This implication applies to physical packings, using the previously dropped 9/11
non-overlap condition. It is not a consequence of the nineteen-pair LP relaxation alone.
It can therefore support a conditional capture-leaf-to-terminal join without silently
strengthening an LP result. Missing premises or failed direct bounds leave the leaf
unresolved. An empty effective interval would require an explicitly supported geometric
exclusion route rather than an implicit new admission.

The predicate gives a concrete geometric target for capture: a thin $v$ projection of
square 9, coarse confinement of $b$, and controlled positive turns of 9 and 11. Whether
an actual leaf meets it is a separate registered evaluation. It does not establish that
the producer will reach that domain or that a complete capture tree is covered.

### A prospective direct-separation premise

The preceding argument needs the three individual position bounds and the numeric
$\tau_0$ guard only to establish the interval for $U=u\cdot(x_9-x_{11})$.
A future consumer could instead certify directly that

$$
-9/25\le U\le0.
$$

Retain the complete root unit-axis and nominal displacement identities, the bounds
$|v\cdot e_9|\le1/5000$ and $-1/2\le b\le1/12$, the same one-sided intervals for
$q_9,q_{11}$, and physical non-overlap of the pair. Then
$V=1+b+v\cdot e_9$ has the same positive closed interval. The six forbidden-axis
upper bounds still hold at the closed endpoints $U=-9/25$ and $U=0$, since they use
only $|U|\le9/25$. For a surviving positive $v$ axis, the same rearrangement gives

$$
b\ge\sec\delta_i-1+\tan\delta_i\,U-v\cdot e_9.
$$

When $\delta_i\le0$, the product $\tan\delta_i\,U$ is nonnegative even at $U=0$.
For positive $\delta_i$, the same tangent upper bound and $U\ge-9/25$ apply.
Consequently the exact lower floor and strict headroom are unchanged. This proves a
weaker sufficient premise for the same geometric conclusion; it does not modify the
domain accepted by H-285's existing checker.

The direct bound can be computed in time linear in the number of live polygon
vertices. Let $G$ be the leaf's declared D4 matrix, $B$ its field scale, and let $p$
denote an original field-coordinate vertex. Over the full accepted root enclosure,
form the interval covector

$$
w=G^{\mathsf T}u/B.
$$

Enclose $w\cdot p$ over every original live polygon vertex of owner 9, and separately
over every such vertex of owner 11. Subtract these two complete scalar hull intervals.
This encloses $U$: both the D4 centre and the root-dependent translation cancel in
$x_9-x_{11}$. It requires neither a vertex-pair enumeration nor an axis-aligned
rectangle before projection. Shared-root dependence may still widen the result;
soundness does not imply that this bound will be sharper on a particular leaf.

This would be a supplemental projection, not a thirtieth position coordinate. Keep
the raw $b$ interval and require a separately registered consumer predicate before
using an effective lower floor. H-290 retains its stated 49 quantities and does not
compute or apply this proposed predicate. No actual direct-$U$ bound has been
evaluated. The reformulation and projection rule are sole-Astra hand derivations,
without independent mathematical review or a new machine-checked implication.

## Conservative Dependencies of an Accepted Closure

Tail A's ordinary admission makes its retained certificate a possible source of a
smaller reusable obstruction. A dependency inventory can identify a candidate owner set;
it cannot establish that a projected certificate passes the smaller-arity checker.
Exp-273 under H-282 reads the already accepted full standing
receipt and its exact seed/node objects without producing or rewriting a certificate.

The standing verifier's [row-cover rule](../../../packing/devtools/verify_n17_kernel_certificate.py)
uses every nonempty foreign owned hull implicitly, as well as explicitly recorded
collision regions. An owner absent from the collision-partner list may still be
essential. Conversely, the producer supplies complete pose covers for every other live
owner, including partners never used in a collision region. The inventory retains two
dependency channels so these supplied witnesses do not force an all-owner result by
construction.

| Fact | Geometric dependencies | Additional validation dependencies |
| --- | --- | --- |
| Seed row or owned hull | Its owner's presence and the fixed cell, wall and frame premises. | The complete accepted seed and content identity. |
| Updated row | Its owner, accepted predecessor, every nonempty foreign prior owned hull, and every current row of each collision-cited partner. | Every current row of every supplied partner cover, including unused covers. |
| Updated owned hull | Its old owned hull and all new row facts that justify the common-kernel planes, including compression in replacement mode. | The corresponding accepted compression and state metadata. |
| Empty-pose closure | Every final row of the declared owner. | The full standing closure and final-state custody. |
| Owned-hull intersection | Both named final hull facts, after joining the named pair to the exact intersection predicate. | The standing closure metadata. Unsupported or unjoined pair identity is refused. |

An updated row does not use its owner's old hull: the supported row grammar forbids
self-hull cuts and the implicit forbidden-region rule excludes that owner. The old
hull remains necessary for compression, even in replacement mode, because replacement
points can be convex combinations of old-hull vertices. Empty foreign hulls contribute
no forbidden-region edge. These rules deliberately keep geometrically redundant
nonempty foreign hulls; pruning such edges would need a separate exact coverage test.

Each complete partner pose cover may be represented by one DAG fact depending on all
of that partner's current rows. This factors repeated edges without weakening the
universal partner-pose quantifier. References, closed row partitions and chronological
state updates must be joined exactly; missing, future, foreign or duplicate references
are refused. The streamed node must reach its canonical content identity at EOF.

A complete all-owner geometric closure set is a valid no-reduction result. A strict
subset is only a projection proposal. A later attempt must reconstruct the typed seed
and node, state keysets, skipped-step indices, row references, initial and final states,
compression and closure references, and content identities. The world-cell enumeration
and physical frame stay fixed. Deleting tuples from an existing certificate is not a
projection proof. Only a separately registered full standing replay on the smaller
owner set can support ordinary subpattern admission and its symmetry/containment count.

The prospective workload is one primary inventory and one fresh deterministic
reproduction, each with a 90-second ceiling and a combined 180-second scientific and
termination ceiling, followed by at most 10 seconds of termination cleanup. Proposed
representation ceilings are 10 MiB compressed and decoded for the seed, 512 MiB
compressed and 2 GiB decoded for the streamed node, 25,000 facts, 500,000 total channel
edges and 64 MiB decoded report output. The node's decoded ceiling is separate from its
compressed ceiling. A sampled 4 GiB current-RSS guard is not an allocation-time limit.
Bulky DAG output belongs outside Git under the normal retained-object manifest.

These are prospective scheduling ceilings, not measured costs. Both runs must agree on
their complete deterministic inventory and proposal, with the same accepted full
standing receipt, seed/node identities, named cells, frame and closure. No expensive
standing replay is repeated merely to inventory its already accepted result. A ceiling,
unsupported grammar or identity failure leaves the inventory incomplete or refused;
it does not establish that a smaller core is impossible. No inventory outcome directly
changes the exclusion census.

The [exp-273 summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-273-tail-a-dependency-inventory/summary.json)
records the inventory and its fresh independent reproduction, both completed in
10.49 seconds combined. The complete DAGs remain available through the
[retained-object manifest](../../../packing/campaign/retained/session-184-tail-a-dependencies/README.md).
The two inventories
agree on 3,338 facts, 101,931 edges and the deterministic inventory identity. Both the
geometric and validation owner sets contain all seventeen owners, so
`strict_subset_proposal=false`. This establishes no reduction under the declared
conservative rules. It does not establish that every owner is necessary or that the
certificate is minimal. No smaller-arity certificate or additional exclusion follows.

## First Saved-Prefix Capture Adapter Contract

The accepted endpoint prefix from exp-266 supplies a concrete first input for the
capture consumer. Its saved seed and node are gzip objects, and its independent replay
uses `PASS_SAVED_STALL`. The original consumer accepts plain JSON with a different
receipt shape. Bridging these formats must preserve the exact pose-cover and frame
contracts; changing a receipt's status string is not that bridge.

The H-286/exp-272 adapter keeps the first workload narrow: the endpoint's
seventeen named owners, one complete accepted update, identity D4 action, and
$U=L=1169/250$, $B=1$. The descriptor binds the seed and node content identities,
label-to-owner bijection, cells, frame, accepted root and expected step count. The
original `capture_cap=None` remains in custody. Its normalized inner cap is $U$ because

$$
\operatorname{offset}=(U-U)/2=0,\qquad
\operatorname{field\_centre\_bounds}(h)=(Bh,B(U-h)).
$$

This is the same affine formula as a frame with numeric capture cap $U$, for every
half-extent $h$. Binding its coefficients and comparing all seed-row wall planes
establish the concrete normalization. The cells, scale and D4 action do not change.
A nonunit-$B$ synthetic control checks the general equality, although this first saved
workload uses $B=1$.

The adapter must read bounded gzip inputs and consume the saved node completely through
its streamed end before using its final rows. Proposed representation ceilings are
10 MiB decoded for the seed and 64 MiB decoded for the streamed node. Content identities
come from canonical decoded content, not filenames or gzip bytes. A fresh subprocess
must perform the full saved verification without importing the producer and return
`PASS_SAVED_STALL`, no closure, the same seed/node/frame/cell/state identities, and one
checked step. Changed objects, incomplete streams, unsupported guards or ancestry, and
incomplete verification are refused or incomplete. A parent process may use existing
geometry helpers; that does not weaken the separate clean-process verification rule.

From those verified final rows, compute every existing root-frame coordinate and chart
bound, and additionally compute $v\cdot(x_9-x_9^*)$ directly on each original polygon
vertex across the full root enclosure. This supplemental projection does not become a
thirtieth coordinate in the existing position norm. It does not clip $b$ or apply the
proposed coarse-slider lemma without an explicit accepted-certificate and premise join.

The readiness criterion is complete replay custody, exact bounds covering all live row
pieces, retention of all seventeen exact endpoint pose enclosures, and inclusion of the
endpoint's zero displacement, slider and relative-angle coordinates. Geometric status
may remain unresolved. It is not a requirement that a first-update prefix already lies
inside a local, apex or exclusion region. The registration used a 180-second parent
ceiling with a fresh child limited to 60 seconds inside that clock.

The original centred $C(S^*)$ premise remains inherited. The prefix does not establish
it. This first adapter admits no capture tree, exclusion, global coverage or census
change. It records which actual bounds prevent the conditional terminal join.

### The first actual leaf result

The [exp-272 receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-272-saved-prefix-capture-adapter/receipt.json)
passed readiness in 11.23 seconds. Its fresh producer-free replay returned
`PASS_SAVED_STALL` for the same one-step seed/node pair. All seventeen complete root-pose
enclosures were retained, square 6 met its closed S2 premise, and all 49 derived
intervals contained zero: 29 position coordinates, 16 half angles, three sliders and
the supplemental $v_9$ projection. The consumer checked 1,088 seed wall rows and retained
1,024 live angle pieces. Only square 1's endpoint witness used an updated row; the other
sixteen still used seed rows.

The resulting bounds are far outside the terminal domains. None of the 29 position
enclosures lies inside either the local or wide coordinate interval, and none of the
16 half-angle enclosures lies inside either corresponding angle interval. The largest
position magnitude is approximately $0.92976505$; the largest half-angle magnitude is
$0.421875$. The following decimals summarize exact rational bounds in the receipt;
they are not inputs to any proof check.

| Quantity | Retained interval, approximately | Missing sufficient premise |
| --- | --- | --- |
| Effective $a$ | $[0,0.78976505]$ | Upper face $a\le1/4$. The lower face uses the original-container premise. |
| Raw $b$ | $[-0.51520218,0.36795567]$ | Both $B_W'$ faces and the coarser interval $[-1/2,1/12]$. |
| Raw $z$ | $[-0.93490794,0.21827829]$ | Both $B_W'$ faces. |
| Direct $v_9$ | $[-0.47058586,0.65447155]$ | The coarse-slider lemma's interval $[-1/5000,1/5000]$. |
| $q_9$ and $q_{11}$ | $[-0.41925316,0.41004508]$ | The coarse-slider lemma's one-sided interval $[-1/200,1/5000]$. |
| $q_{16}$ | $[-0.40927285,0.42145778]$ | The common wide angle bound and either cone's sign/domain premises. |

The coarse-slider lemma's three position bounds on $\xi_9,\eta_9,u_{11}$ also fail.
Thus its accepted root guard does not authorize clipping this leaf's $b$ interval.
No optional feature, apex or patch certificates were requested in this first control;
the common wide-domain premise already fails. `unresolved` is the correct geometric
result. A failed enclosure inclusion does not show that a physical packing violates the
desired bound, and one owner update supplies no contraction-rate or fixed-point verdict.

## Full-Root Join for the Capture Cap

The first adapter used the larger $C(U)$ walls. A successor at a near-optimal numeric
cap needs a separate exact join; the `None`-to-numeric-$U$ equivalence above cannot be
reused for a smaller cap. H-288/exp-275 fixes the historically retained
$U'=935106018721/200000000000$, recorded in the
[R9 review](../reviews/review-2026-10-05-n17-capture-r9.md), and freshly checks it against
the full accepted root enclosure.

The exact chart formula is

$$
F(t)=\frac{6+4t}{1+2t-t^2},\qquad
F'(t)=\frac{4(t^2+3t-2)}{(1+2t-t^2)^2}.
$$

For the accepted $t\in[t_-,t_+]$, verify $0<t_-\le t_+<1$, positivity of the
denominator, and $t_+^2+3t_+-2<0$. The derivative is then negative throughout the
interval, giving the exact enclosure $S_-=F(t_+)$, $S_+=F(t_-)$. Bind this formula
symbolically to the endpoint layout's side and retain the same accepted root identity.
The independent cap conditions are

$$
S_-\le S_+<U'\le U,\qquad
0<U'-S_+\le U'-S_-\le10^{-12}.
$$

Apply the same upper-excess condition to the consumer's outward side enclosure.
Interval overlap alone does not establish the common-root formula or the full-domain
excess. The historical `pilot_n17_capture.load_endpoint` check bounded
$U'-\mathrm{side.hi}$ above by $10^{-12}$; the claimed uniform upper excess requires
$U'-\mathrm{side.lo}\le10^{-12}$ instead. This identifies an insufficient check, not
evidence that the retained numerical cap is wrong. The fixed candidate must be refused
or left uncertified if its exact inequalities fail; it must not be silently replaced.

For this numeric cap, the physical centre walls are

$$
[(U-U')/2+h,\;(U+U')/2-h],
$$

and field coordinates multiply both endpoints by $B$. Keep the original cells, $U,L,B$,
D4 centre $U/2$ and induced permutations. A saved numeric-cap seed and node must be
freshly admitted against these walls; old $U$-wall objects cannot be relabelled.
The fresh verifier must retain the explicit checked numeric frame, since the frame name
alone does not distinguish its capture cap. The original $C(S^*)$ premise and exact
root shift $\sigma=(U-S^*)/2$ remain unchanged.

The [exp-275 certificate](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-275-capture-cap-root-join/certificate.json)
and [fresh replay](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-275-capture-cap-root-join/replay.json)
passed the finite criterion in 1.21 seconds combined. Their scientific payloads agree.
The exact stored rationals satisfy the derivative and denominator guards, whole-box
containment and both cap inequalities. The monotone enclosure gives excesses of
approximately $[4.49048365876565,4.49048365900895]\times10^{-13}$; the preserved
consumer enclosure gives
$[4.49048365785146,4.49048365992313]\times10^{-13}$. These decimals summarize the
exact receipt. The result certifies the cap/root join only; endpoint-cell containment,
capture, object relabelling, exclusion and global coverage remain unproved by it.

### A future smaller-cap exclusion interface

The same centred containment permits a future exclusion certificate at $U'$ to rule
out a cell state for a putative packing of side at most $S^*$. It must use the original
$U$-frame cells and the offset walls above. The current
[standing verifier](../../../packing/devtools/verify_n17_kernel_certificate.py)
constructs walls from one cap as $[h,U-h]$. Substituting $U'$ for that cap would change
the origin of the inner container relative to the cells. A future extension therefore
needs both outer and inner caps, independent centred-wall checks, exact cap/root
custody and its own controls. H-290's numeric-frame replay supplies no standing
admission for such an exclusion.

The census must also declare the cap at which a state is ruled out. If its target is
$T$, an exclusion proved in $C(V)$ transfers whenever $T\le V$. Existing $U$-cap
exclusions transfer to $T=U'$; a new $U'$-cap exclusion does not prove impossibility in
the larger $C(U)$. A future optimality census could instead state its exact $S^*$
target and retain the proof that every certificate cap is at least $S^*$. Its cell
cover may remain the original $U$ cover in either case. These are prospective
admission obligations; the current sixty-entry census and its interpretation remain
unchanged. Whether smaller-cap work closes any remaining state is unmeasured.

An optimality cover must distinguish exclusions from terminals. An exclusion in
$C(V)$ denies the declared assignment there and transfers to every $C(T)$ with
$T\le V$. A local terminal under the inherited $C(S^*)$ premise instead proves
that a represented packing has containing side $s\ge S^*$. The endpoint assignment
is feasible at $S^*$, so such a terminal is not an excluded census state. A final
argument for optimality would combine the exclusions with terminal implications
for every remaining assignment, obtaining a contradiction under $s<S^*$. Neither
type of certificate can substitute for the other's coverage obligation.

## Numeric-Cap Checkpoint and Consumer Contracts

The registered H-289/exp-276 preparation run starts from the actual seventeen endpoint
cells at the H-288 certified numeric cap. It uses no position box and resumes no old
checkpoint. One complete round updates each of the sixteen contracting owners once;
square 6 retains its complete seed cover. The production control checks all seventeen
endpoint poses after seed admission and after each update. A separate process then
resumes the complete round-001 checkpoint with the same one-round limit, admits the
seed, and replays all sixteen steps without producing a new step. Its endpoint check
is a final-state check; it does not independently repeat the production phase's
seventeen endpoint checkpoints.

The [exp-276 record](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-276-h289-numeric-cap-first-round.md)
now retains one complete round: sixteen updates and seventeen production endpoint
checks in 175.86083 seconds. Its separate fresh replay passed all sixteen saved
steps, 1,024 rows and 143,498 checker events in 66.47918 seconds. The saved seed and
node identities, update lists and round records agree between phases, and replay
reports final-state agreement. The inherited `checked_after: 17` field in the fresh
receipt is production history; the independent fresh endpoint check is one check
of all seventeen final poses. This is checkpoint readiness, with no terminal or
capture conclusion from the pilot's floating extent summaries.

The pilot and cap checker use different outward root enclosures. The pilot reads the
accepted endpoint receipt's midpoint and inclusion radii, rounded outward to
$10^{-40}$; the cap checker freshly verifies the root and uses a dyadic enclosure.
The input join must bind the endpoint receipt's exact midpoint and radii to that same
checked root, prove that both pilot parameter intervals contain the cap checker's
inclusion intervals, and require the pilot's computed cap to equal the fixed certified
$U'$. The corrected upper-excess check also applies to the pilot's own side enclosure.
Matching certificate names or overlapping side intervals alone is insufficient.

The H-290/exp-277 consumer takes that complete checkpoint's saved seed and
node. Its descriptor binds the H-288 cap/root certificate, both H-289 phase receipts,
the exact label-to-owner assignment, actual sixteen-step order, cells, scale, D4 action
and canonical object identities. It accepts only the stated full seventeen-owner,
$B=1$, identity-action workload, with no position box, guard or ancestry. The named
frame retains its original cells and outer cap $U$, and explicitly sets
`capture_cap=U'`.

For every half-extent $h$, verify the numeric frame's affine wall formula

$$
\operatorname{field\_centre\_bounds}(h)=
\left(B\left(\frac{U-U'}2+h\right),
B\left(\frac{U+U'}2-h\right)\right).
$$

Equality at $h=0,1$ binds the affine coefficients; exact comparison of every declared
seed-row wall binds the saved input. A fresh producer-free process must admit the seed
and replay every saved step to the complete stream end under this explicit numeric
frame. Require `PASS_SAVED_STALL`, no closure, sixteen steps, the same named owners and
canonical seed/node identities. The frame name alone cannot distinguish the inner cap.
The existing `None`-wall prefix receipt supplies no numeric-cap replay premise.

The fresh child's proof may be conditional on its supplied exact frame. In that
design, the parent freshly establishes that this same frame equals the accepted
root/cap/cell context, and compares the child's complete frame identity before using
its result. The child must record its actual inner cap, scale, cells, names, actions
and other frame conventions; it must not claim to have independently checked the
root or cap if that check belongs to the parent. The synthetic seventeen-cell replay
fixture tests this composition and the sixteen-step custody path. It is not evidence
that its synthetic poses form a physical seventeen-square packing.

The parent consumer obtains final rows by exact replay and applies the retained
root-coordinate and complete closed-chart calculations. It must retain all 49 bounds:
29 position coordinates, sixteen relative half angles, three raw sliders and the direct
$v_9$ projection. Every interval must contain the endpoint's zero value, all seventeen
full-root endpoint pose boxes must remain present, and square 6 must satisfy its S2
premise. The original centred $C(S^*)$ and local composition theorem remain explicit
inherited premises. Readiness does not require a terminal predicate to pass. No cone,
coarse-slider or patch certificate is silently added to this workload.

Prospective representation ceilings are 10 MiB compressed and decoded for the seed,
512 MiB compressed and 2 GiB decoded for the streamed node, and 64 MiB for the retained
consumer output. Check byte bounds before replay, retain object identity across reads,
and never load the entire node as one decoded JSON value. The proposed parent ceiling
is 600 seconds, with a fresh child limited to 300 seconds inside that same clock,
termination at 600 seconds and forced cleanup ten seconds later. Preserve the existing
200,000-event checker ceiling and a sampled 4 GiB RSS ceiling. These limits are
prospective scheduling limits; the registration must confirm them after the H-289
checkpoint's measured readiness. A ceiling, incomplete stream or incomplete replay
leaves the consumer incomplete. A root, frame, identity, pose-retention or exact-check
disagreement refuses it. Neither outcome is evidence against optimality.

### The actual numeric checkpoint remains broad

The [exp-277 summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-277-numeric-checkpoint-capture/summary.json)
records accepted readiness in 163.293 seconds inside 164.506 seconds of supervision.
Its fresh producer-free replay took 63.157 seconds. All 49 intervals contain zero,
all seventeen full-root endpoint poses survive, and square 6 satisfies S2. All four
terminal predicates are false.

Every one of the 29 position enclosures fails both the local $1/5000$ and widened
$1/100$ bounds. Every one of the sixteen half-angle enclosures fails both the local
$1/10000$ and widened $1/200$ bounds. The largest position magnitude is approximately
$0.929765046802$; the largest half-angle magnitude is exactly $27/64$. The effective
$a$ interval reaches approximately $0.789765046802$, exceeding $1/4$;
$b\in[-0.515202180574,0.367955673984]$ and
$z\in[-0.934727446175,0.218278290614]$ both exceed their direct domains. These
displayed decimals summarize the exact stored intervals. The direct $v_9$ enclosure,
approximately $[-0.470585863452,0.505033753350]$, also fails the coarse-floor premise.
The coarse floor therefore cannot be applied to clip $b$.

Each active label has exactly 64 live chart rows, with intervals
$[k/64,(k+1)/64]$ for $k=0,\ldots,63$. Hence each owner's represented orientation
projection remains the entire closed chart $[0,1]$. All 1,024 angle pieces are live;
narrow individual rows have not removed any orientation from this relaxation.
These facts concern the retained row products, not the simultaneous feasible packing
set. Comparing them with the earlier one-update, larger-cap exp-272 does not isolate
the effect of changing the cap or the number of updates.

### A necessary angular span bound

A live row $[l,h]\subseteq[0,1]$ represents the product of its retained centre
polygons with that full chart interval. Its physical orientation span is

$$
2\arctan\frac{h-l}{1+lh}.
$$

If this entire product lies inside a relative half-angle bound $|q|\le Q$, where
$Q\in\{1/10000,1/200\}$, its connected orientation interval must fit within one
quarter-turn lift of the allowed arc. Different lifts are separated by a nonempty
gap. The allowed arc has width $4\arctan Q$, so a necessary condition is

$$
\frac{h-l}{1+lh}\le\frac{2Q}{1-Q^2}.
$$

For the actual uniform rows, the left side is
$64/(4096+k(k+1))$. Its minimum is $1/127$, which exceeds the local threshold
$20000/99999999$. All 1,024 live rows therefore fail this necessary local span test.
For the widened threshold $400/39999$, precisely $k=0,\ldots,47$ fail: 48 rows per
active owner, or 768 rows in total. Passing the necessary span test on the other
rows does not establish a widened angle bound. A direct example is label 1's first
row, whose recorded $q$ interval is $[0,1/64]$.

These are exact hand deductions from the accepted row roster. They have not received
independent mathematical review or a machine-checked span certificate. They establish
noncontainment of the row-product relaxation in the terminal region. The physical
feasible subset could be much smaller: an additional checked use of containment or
non-overlap could remove the offending pose pairs without refining the rows. The
deductions prove neither a packing counterexample nor the cause of a producer stall.

The same distinction applies to positions. If two retained vertices in one live row
have a required coordinate difference greater than $2\rho$, that row product cannot
fit in a radius-$\rho$ coordinate tube. The common root and container translation
cancel in this difference. Cartesian differences are rational; rotated covectors
require an accepted-root bound. No position-span target has been evaluated here.

## Why the Signed Cones Do Not Cover an Endpoint Product Domain

An endpoint-preserving leaf's coordinate enclosures contain zero. In particular, its
angle product contains $q_{16}=0$. The negative and positive cones require opposite
strict signs of $q_{16}$ and bound a shared constrained angle such as $q_1$ by a
multiple of $|q_{16}|$. Their closures therefore require $q_1=0$ on the section
$q_{16}=0$. The accepted annulus patch is separated from that section.

Consider a product domain containing

$$
q_{16}=0,\qquad q_1=\delta,\qquad q_j=0\quad(j\ne1,16),
$$

where $1/10000<|\delta|\le1/200$. This angle vector lies outside both ratio cones,
the accepted off-zero patch, the apex radius and the local angle bound. Zero position
and slider coordinates do not change that conclusion. Thus any declared relaxation
containing this vector is not covered by the currently accepted sufficient regions.
The angle intervals retained in exp-272 are broad enough for this obstruction.

This is a witness to a gap in coverage of a relaxation, not a feasible packing or a
counterexample to optimality. Containment or non-overlap constraints could exclude the
vector; a checked use of those constraints is additional proof work. Merely splitting the sign of
$q_{16}$ also leaves arbitrarily small nonzero $|q_{16}|$ paired with an independent
nonzero $q_1$, outside the ratio cones. A complete use of those cones needs further
validated angular restrictions or a closed case cover whose remaining cases have
their own certificates.

For the current unconditional endpoint leaf, the direct objective remains the local
terminal bounds on all positions and angles. A later guarded capture tree could use
the signed cones and patch on branches away from the endpoint, but its complete
coverage, guard propagation and leaf custody would need a new checked interface.
The present consumer accepts no such tree. This coverage argument is a hand derivation
by the sole Astra agent; it has not received independent mathematical review or a
machine-checked coverage proof.

## Centered Replay and Finite-Gate Intake

H-291/exp-280 completed the independent centered-container readiness control. Its
[receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-280-centered-endpoint-hull-capacity/receipt.json)
binds the original H-290 seed and node to the unchanged 24-cell world, $B=1$,
$U=1169/250$, and $V=T=935106018721/200000000000$. The exact offset is
$93981279/400000000000=(U-V)/2$. Parent and child contexts, original canonical and
compressed identities, accepted root and cap inputs, and the inherited H-290
full-seventeen endpoint premise agree.

The producer-free standing child reports full `PASS_STALL`: sixteen updates,
1,024 updated rows, 544 seed rows and 25,134,984 collision-facet checks, with the
explicit 48-vertex computational hull limit. The child took 104.68 seconds; total
supervised time was 106.494 seconds with cleanup confirmed. Its rational-container
proof keeps the root join in the parent context checker. No new leaf bounds or
endpoint evaluation are claimed. All exclusion, admission and global-proof flags
remain false. The earlier exp-278 and exp-279 operational refusals remain in the
record; neither indicated loss of the endpoint.

The first H-292/exp-281 finite-gate invocation stopped after 1.1124 seconds with
[`incomplete`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-281-conditional-owned-hull-gate/certificate.json),
before evaluating gain. It encountered an accepted label-16 endpoint ordinate whose
rational string exceeded the declared parser ceiling and 4,096-bit arithmetic limit.
That coordinate is not an operand of the label-1 ownership construction. The accepted
parent's identity and endpoint validity were not refuted.

The prescribed repair changes the computational input scope in a separately
registered replication. Full canonical EOF, compressed and canonical object
identities, accepted-receipt bytes, world, owner roster, step order and endpoint
witness joins remain required. Other owners' geometry and unused endpoint/root
coordinates are explicit opaque premises from that accepted parent. New numerical
geometry concerns only owner 0's residual vertices, owned group and closed row
intervals, label 1's endpoint box and chart, the fixed container constants, and the
derived finite construction. Those operands retain the 4,096-bit limit; no coordinate
is rounded and no gain threshold changes.

The repaired report must reference unused parent geometry through the accepted
receipt identity instead of copying and reparsing it as new arithmetic. Any oversized
operand actually used by the construction still makes the result incomplete. This is
a computational and custody-scope repair, not a gain result or merely a serialization
change. The exact-arc alternative below remains prospective until this gate has a
mathematical disposition.

That disposition arrived in exp-282. Its
[certificate](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-282-conditional-owned-hull-scoped-input/certificate.json)
and [fresh reconstruction](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-282-conditional-owned-hull-scoped-input/replay.json)
both report `conditional_gain_candidate`, with matching certificate identity and a
nonempty, strictly valid endpoint control. All four all-angle support differences
are negative. All four target differences exceed the exact $1/1024$ threshold;
their approximate values, in E, N, W, S order, are $0.1200241$, $0.1200241$,
$0.2381591$, and $0.2390397$. These decimals summarize the retained rational
comparisons and are not acceptance inputs.

The target construction includes row 26 and the singleton boundary pieces from
rows 25 and 27, all with nonempty clipped centre polygons. Its 96 finite halfplanes
give a five-vertex polygon, and all five vertices are selected. The all-angle and
endpoint selections each have four points. Construction and fresh reconstruction
completed in 8.38847 supervised seconds with cleanup confirmed. The original
exp-281 remains incomplete before gain evaluation.

This result supplies five points owned by square 1 under the closed guard $I$.
It supplies no conditional contradiction or unconditional exclusion. The accepted
parent and its sixteen other endpoint coordinates remain explicit premises, not
newly replayed geometry. All propagation, exclusion, admission and global-proof
flags remain false. The result selects the guarded continuation below; it does not
justify spending on the exact-arc fallback now.

## A Conditional Owned-Hull Gate

The next proposed stronger implication conditions the corner-SW square, analytic
label 1 and owner 0, on one closed angular slice

$$
I=[13/32,27/64].
$$

This is the accepted checkpoint's row 26, near a physical angle of $45$ degrees.
Points proved to lie strictly inside that square for every remaining pose in $I$
become obstacles for all other squares under the same condition. A later complete
conditional contradiction could therefore remove the entire slice. A narrower row
by itself supplies no such contradiction. H-292/exp-281 is reserved for the finite
gate below; production is a separate prospective step requiring registration.

### The accepted parent premise

Use the accepted H-290 receipt and its exact canonical seed and node identities.
Its sequential replay invokes `admit_final_state`, which compares every final group,
row reference, interval, outer domain and residual polygon with the checked
induction. It also binds the final world, mask, scale, source and unguarded context.
Thus the saved final state under that same canonical node identity is a valid input
domain for a new finite implication.

Construction and fresh checking must independently stream the saved node through
canonical EOF, verify the seed identity and source reference, and bind the accepted
receipt bytes and full numeric context. They may extract the final state without
replaying the parent's geometry. State this assurance explicitly:
`parent_geometry_replayed=false`. The finite checker must import neither the producer
nor the hull kernel. The accepted parent is a proof premise, not a newly verified
parent in this experiment.

### A finite strict-ownership polygon

Use three closed angle domains: the target $I$, the all-angle control $A=[0,1]$, and
the endpoint control $Z=[0,1/64]$. Fix $\epsilon=2^{-20}$ and write
$c(t)=(1-t^2)/(1+t^2)$, $s(t)=2t/(1+t^2)$. For each accepted owner-0
row $J$ intersecting the chosen domain, write the closed intersection as $[l,h]$.
Include singleton intersections at boundaries. Begin with the convex hull of all
that row's retained residual vertices. Clip it by the exact necessary centred-wall
box for the restricted interval:

$$
[o+h_{\min},U-o-h_{\min}]^2,\qquad
o=(U-U')/2,\qquad
h_{\min}=\tfrac12\min\{c(l)+s(l),c(h)+s(h)\}.
$$

Call the resulting polygon $P$. This additional intersection follows from the
existing containment premise. It removes centre alternatives from boundary rows
that were legal only at angles outside the guard. Apply this intersection to the
all-angle control too: the accepted coverage statement permits over-cover and does
not by itself require every published residual vertex to satisfy the row's walls.
Any gain from this unconditional tightening belongs to the all-angle control.
Empty clipped polygons impose no constraint.

For each vertex $x=(x_x,x_y)$ of $P$, every corner $(c,s)$ of
$[c(h),c(l)]\times[s(l),s(h)]$, and each $\eta\in\{-1,1\}$, impose

$$
\begin{aligned}
\eta c p_x+\eta s p_y
&\le 1/2-\epsilon+\eta(c x_x+s x_y),\\
-\eta s p_x+\eta c p_y
&\le 1/2-\epsilon+\eta(c x_y-s x_x).
\end{aligned}
$$

Intersect these rational closed halfplanes with $[0,U]^2$ to obtain $K_D$, for
$D\in\{A,I,Z\}$. A singleton chart intersection uses its exact sine and cosine.
The interval rectangle contains every axis vector on the chart intersection;
affinity in the centre and in each trigonometric coefficient makes the finite
corner checks sufficient. Hence every point of $K_D$ lies strictly inside square 1
for every represented parent pose satisfying that guard. Taking the convex hull of
old owned points and any points of $K_D$ preserves this conditional ownership.
No contact choice or pair-separation feature is assumed.

For each nonempty polygon, select a maximizing vertex in the fixed directions
E, NE, N, NW, W, SW, S, SE, with lexicographically smallest $(x,y)$ breaking ties.
Deduplicate in that order, retaining at most eight points. Let $S_D$ be their convex
hull and let $H_0$ be the parent's owner-0 owned hull.

For a nonempty baseline $H$, a selected hull $K$ has a declared gain when

$$
\max_{n\in\{(1,0),(0,1),(-1,0),(0,-1)\}}
\bigl(h_K(n)-h_H(n)\bigr)\ge1/1024.
$$

If the baseline is empty, require $\operatorname{area}(K)\ge2^{-20}$ instead.
An empty candidate has no gain. Compare $S_A$ with $H_0$ to detect unconditional
owned-hull information lost by the current extraction. Compare $S_I$ with
$\operatorname{conv}(H_0\cup S_A)$ to identify information added by conditioning.
These are declared prioritization thresholds, not necessary conditions for a useful
geometric implication.

The endpoint control requires nonempty $S_Z$. Every selected point must be strictly
inside the full-root endpoint square-1 centre box, using chart zero and exact
coordinate inequalities. The accepted H-290 input roster supplies this endpoint
box; its equivalent chart-one representation is not a second pose to discard.
An empty endpoint-control hull is inconclusive, and a failed strict containment
check refuses the gate.

After that control passes, an unconditional gain takes priority and yields an
`unconditional_refresh_candidate`; it does not launch guarded production. Otherwise,
a guard-specific gain yields a `conditional_gain_candidate`. If neither reaches the
declared threshold, record `no_gain_under_frozen_recipe`. Fresh checking reconstructs
all three polygons and all support comparisons. Verifying only proposed points would
not establish the control comparison or a no-gain result.

Here “unconditional” means across the accepted parent domain, without an additional
angle guard. Those owned points still depend on the parent's contracted row cover.
They cannot be inserted into a fresh wall seed as though the implication held for
every placement in the original cells. Any continuation retains the accepted parent
certificate and the finite owned-point join.

Construction and independent finite replay each have a proposed 60-second ceiling,
including their own bounded extraction, for 120 seconds combined. The accepted
receipt and seed are limited to 10 MiB; the node to 512 MiB compressed and 2 GiB
decoded; the extracted final state to 64 MiB. Require complete canonical EOF without
loading the entire node as one JSON object. Each intermediate or final $K_D$ has at
most 128 vertices, and every admitted or computed rational numerator and denominator
has at most 4,096 bits. A resource stop is incomplete, with no gain verdict. Preserve
a sampled 4 GiB memory ceiling and original-object identity across reads.

### What a later conditional continuation would prove

The positive exp-282 gate selects preparation of H-293/exp-283, one separately
registered conditional continuation. Its scientific target has not run. Freshly
establish the accepted parent, the closed guard, and the extra
owned-point implication before producing any child step. Keep all original rows
initially. A proposed first round updates the other fifteen contracting owners in
their existing order and owner 0 last; square 6 remains coarse. This lets the other
owners use the new points before owner-0 compression. It does not enlarge the
64-live-row or 48-point hull policies.

For this actual input, the old hull has twenty vertices and the target contributes
five points. Their augmented hull therefore has at most twenty-five vertices.
Retain them all; no inner-selection fallback or loss of old points is needed in this
trial. Production disables refinement explicitly and must report zero splits.

The prospective parent-aware checker binds the accepted H-290 final state and the
same-object full centered replay from exp-280, the finite gate and its fresh check,
the fixed root/container context, and one explicit closed guard. Every unchanged
initial row and group must equal its parent record; owner 0's selected hull is the
sole declared exception. Each child step retains its predecessor references, and
the final state retains the same ancestry and guard. Generic final-state checks
that assume empty ancestry cannot substitute for those joins.

Adding eight points to a 48-vertex hull need not preserve the latter limit. The
initializer must check the augmented hull's size, or use a separately declared exact
inner selection. For example, retaining the old hull's eight fixed-direction support
vertices and all eight new points gives at most sixteen points, each already proved
owned. Dropping other old vertices weakens the recorded obstacles but does not
invalidate the accepted parent row cover. Record that loss explicitly. The new
rational points also carry no grid-membership promise; any later grid compression
must establish its usual exact convex-combination witnesses.

The inductive invariant concerns every physical parent packing satisfying the guard:
each square's pose remains in its retained row cover, and each retained owned point
lies strictly inside that square. The accepted parent and the finite ownership lemma
establish this invariant after augmenting owner 0's hull. Existing exact step cover
and ownership implications preserve it. Rows covering angles outside $I$ are harmless
over-cover; a first continuation can retain their complete $[0,1]$ partitions rather
than introduce a new angular partition algorithm. Its conditional initialization must
still be checked explicitly. Current generic-root admission rejects ancestry and guards,
so the augmented state cannot be presented as a new generic wall seed.

The useful acceptance boundary is a completely checked contradiction for every
parent configuration satisfying $\tau_1\in I$. Such a result removes a whole closed
chart interval of width $1/64$. A valid nonclosed result remains unresolved even if
some polygons shrink. A complete nonclosed sixteen-owner round misses H-293's
frozen one-round exclusion criterion; it leaves physical feasibility under $I$
unresolved. A resource stop is incomplete. The parent-plus-guard receipt needs an explicit conditional
schema; it must never enter an unconditional exclusion ledger or claim that the
remaining angles are covered. Full conditional replay costs and limits must be
registered separately after the finite gate and centered-control measurements.

The chosen initial test scans all unordered owner pairs in lexicographic order for
an exact nonempty intersection of their closed owned hulls. The first such pair is
an initial conditional contradiction at step $-1$, before any update. A shared point
or segment is enough: every owned-hull point lies strictly inside its physical
square, so a common point would lie in both square interiors. Empty hulls do not
intersect. The fresh checker must reconstruct the actual intersection, including
point and segment degeneracies; bounding-box overlap is insufficient. No initial
intersection has been evaluated during preparation.

Absent an initial contradiction, stop at the first independently checkable post-step
contradiction, or after the one complete sixteen-owner round. Freeze 600 seconds for
production and 300 for independent full checking, including their input and finite
ownership joins, with a sampled 4 GiB memory ceiling. The fresh receipt must bind
the actual closure kind, owner pair and step. Source controls and mathematical review
precede registration and launch; a producer's declaration alone cannot meet the
criterion.

The final owner-0 update also has a guard-specific terminal test. Reconstruct every
row whose closed interval meets $I$, using
$\max(l,13/32)\le\min(h,27/64)$. In the unchanged partition these are rows 25, 26
and 27, with intersections respectively the left endpoint, all of $I$, and the right
endpoint. If all three residuals are empty, the parent-plus-guard cover has no pose
for square 1, even when rows outside $I$ remain live. This is a checked conditional
contradiction, not a contraction diagnostic. Row 26 alone is insufficient for this
union-cover test. Record the actual row roster, closed intersections, owner and step
under a distinct `guarded_owner_cover_empty` discriminator; the fresh checker
reconstructs them after the final complete update. Ordinary post-step contradictions
take priority. This additional terminal was selected before any conditional child
row was evaluated.

The target guard $I$ excludes the endpoint's chart-zero and chart-one representations.
Consequently, an $I$-conditional child must not be required to retain that
outside-guard endpoint after its updates. The separate $Z$ finite control calibrates
the ownership construction. An all-angle parent refresh, by contrast, must retain
the full-root endpoint after each complete update and in its fresh final-state check.
For that unguarded route, a prospective progress boundary is a loss of at least
$1/64$ in the exact union length of one owner's live chart intervals. Emptying one
row need not exclude its shared boundary angles, which adjacent closed rows may
still represent. Neither smaller polygon extents nor a finer partition counts as
orientation removal under this criterion.

An apparent full closure of the all-angle known-endpoint parent would be a refused
control, not an alternative success. The closed-$I$ trial has no such requirement
because the known endpoint lies outside its guard.

If a future checked conditional contradiction excludes $I$, it can strengthen the
original unguarded parent through a separate pruning certificate. Start from the
original parent's groups and rows and transfer only the proved impossibility of
$\tau_1\in I$. The full row partition may remain, with row 26 marked empty and
shared boundary angles retained as harmless over-cover in adjacent rows. Do not
transfer child-only grown hulls or contracted other-owner rows: those depended on
$I$ and need not hold outside it. Such a pruning interface requires its own checked
parent/guard-closure join; the finite gain alone supplies none of it.

This pruning would remain a statement about the centered $C(V)$ parent. Its live
angle union would lose the open interval $(13/32,27/64)$, of exact length $1/64$,
even though the closed neighboring rows still represent the two boundary angles.
The conditional impossibility itself includes those boundaries. Containment gives
the same implication for $C(S_*)$ because $S_*<V$; it does not extend the
impossibility to every packing in the larger $C(U)$ container or change that
container's existing census.

Before that gate supplies evidence, do not spend on blanket row doubling, further
cones, a full annulus tiling, broad LP sweeps or long unchanged iteration. If the
all-angle control already yields a substantial gain, prefer the unconditional
extraction correction because its implication applies across the entire parent
domain. If all three kernels are empty or too small, this particular construction
has not supplied the proposed improvement; it has not refuted conditional branching
or optimality. The hand implications in this section remain the sole Astra agent's
derivations, pending independent mathematical review and the stated finite checks.

### Two bounded alternatives after a no-gain result

The rectangle used above is a sufficient enclosure of an angular arc. Its corners
need not be unit vectors, so it can reject a point that every actual square contains.
Consequently, an empty $K_I$ would not prove that the exact common-owned set is empty.
A later finite checker can remove this particular conservatism for supplied rational
points without trigonometric approximation or a numerical optimization verdict.

For a proposed point $p$, a vertex $x$ of the same clipped centre polygon, and
$\Delta=p-x$, put $a=1/2-\epsilon$. For each $\eta\in\{-1,1\}$ the two exact
ownership inequalities, after multiplication by the positive denominator $1+t^2$,
are

$$
\begin{aligned}
(-\eta\Delta_x-a)t^2+2\eta\Delta_y t+(\eta\Delta_x-a)&\le0,\\
(-\eta\Delta_y-a)t^2-2\eta\Delta_x t+(\eta\Delta_y-a)&\le0.
\end{aligned}
$$

For a rational quadratic $f(t)=At^2+Bt+C$ on the closed rational interval $[l,h]$,
check both endpoints. If $A<0$ and $t_*=-B/(2A)$ lies inside that interval, check
$f(t_*)$ too. These finitely many exact rational comparisons are equivalent to
$f\le0$ throughout the interval. Affinity in $x$ then extends the result from all
centre vertices to their convex hull. The fixed positive $\epsilon$ supplies strict
interior ownership for the actual unit axes.

One possible proposal source is an outer polygon obtained from the true rational
axes at the endpoints and midpoint of each row intersection. Its proposed vertices
would still need every quadratic check above. A failed proposed point proves nothing
about other points, and failure of a bounded proposal search is not an emptiness
certificate. No such proposal or exact-arc target has been evaluated; this is a
prospective successor only if the registered rectangle gate does not supply useful
information.

A different source of weakness is taking a common-owned intersection over a broad
centre domain. It can be addressed by a complete position case cover while keeping
the same angular guard. Freeze two rational cuts $\alpha,\beta$ before a future
target, and define four closed cases

$$
D_{\sigma,\tau}=\{x:\sigma(x_x-\alpha)\ge0,\;
\tau(x_y-\beta)\ge0\},\qquad (\sigma,\tau)\in\{-1,1\}^2.
$$

Their union is the whole centre plane. In each row use
$P\cap D_{\sigma,\tau}$ in the owned-point proof. Every physical parent pose with
angle in $I$ belongs to at least one of these four cases, including poses on a cut.
Thus complete checked contradictions for all four cases would exclude the original
closed angle slice. A contradiction or a useful owned hull in only one case says
nothing about the unresolved cases. Shared boundaries must occur in every relevant
child; they cannot be discarded by assigning a numerical sample to one side.

This alternative requires a checked parent-plus-angle-plus-position guard interface
and four complete child obligations. It changes neither H-292's frozen experiment
nor the current unconditional ledger. The first gate's measured result should decide
whether tighter angular arithmetic or position conditioning is worth a separately
registered implementation. Both implications above are sole-agent hand derivations,
without independent mathematical review or target measurements.

### Selected successor: four closed centre cases

If the registered H-293 recipe completes all sixteen updates and its fresh full
checker accepts a nonclosed result, the selected different approach is a finite
four-case centre partition. It is prospective: no conditional child geometry,
partition signs or gains have been evaluated for this successor. Exp-283's
parent-custody schema refusal occurred before any child or update and therefore
is not a mathematical negative. The finite proof also has a separately declared
initial-state fallback if no complete conditional child is accepted. These input
routes are distinct; registration selects one before the finite target runs.

The angle interval is already narrow. The remaining common-owned construction
quantifies over broad centre domains. Partitioning the two diagonal centre
coordinates addresses that quantifier directly. The experiment attempts an exact
contradiction in every case, without another producer round or a new numerical
separation LP.

**Accepted parent and scope.** Let $D$ be the original centered $C(V)$ occupied-cell
domain with the inherited closed guard $\tau_1\in I$. The preferred
`accepted_complete_conditional_child` base requires a fresh, full
`PASS_CONDITIONAL_STALL` receipt for exactly sixteen complete updates, together with
the immutable conditional child, its canonical and compressed identities, its
initial-state identity, and the original parent, finite-point and centered-container
premise references. A refused, partial or closed child cannot supply this base.
The accepted final row cover and owned hulls describe every physical packing
in $D$; the experiment does not assert that every represented tuple is physical.

The fallback `accepted_conditional_initialization` base instead freshly reconstructs
the same conditional initialization from H-290, its same-object full centered replay
in exp-280, and the freshly checked exp-282 finite certificate. It takes the original
parent rows and other owned hulls, and augments owner 0 by all twenty old points and
the five checked new points. Their hull has at most twenty-five vertices. The
parent-cover and finite-ownership implications already establish the invariant for
$D$; no conditional child is required. This route inherits no point, row or update
from an incomplete or refused trial. It records fresh initialization reconstruction
and accepted original-parent geometry explicitly, without claiming a child replay.
The four-case geometry, decision rule and arithmetic limits below are the same for
both bases. Exp-284's producer completed sixteen updates, but its fresh conditional
replay reached the wall ceiling. That child has not been accepted and supplies no
geometry or owned points to this successor. The proposed H-294/exp-285 target
therefore selects the initial fallback. The complete-child route remains a distinct
future option, not an implicit source of facts for this run.

For the complete-child base, intake must stream the complete child through canonical EOF and bind its exact
header, ancestry, guard, world, owner keys, final row counts and predecessor
references to that accepted receipt. Use the same exact role-to-path normalization
for compressed identities as the corrected conditional intake. Parent geometry is
an explicitly accepted premise, not geometry replayed by this finite instrument.
The fresh finite checker imports neither the producer, kernel nor algebraic-root
machinery. It independently repeats intake and every finite construction below.
For the initial base it independently repeats the original-parent intake and finite
point reconstruction instead. Each descriptor and receipt must identify the actual
base kind and its different premise identities.

Arithmetic uses the owner-0 residual polygons in rows meeting $I$, their closed
intervals, and all seventeen accepted owned hulls. Unused row geometry and large
root or endpoint scalars remain structurally checked, identity-bound parent data.
Do not repeat the unrelated-scalar parsing failure from exp-281. The original frame
has $B=1$, outer cap $U$, inner cap $V$ and offset $o=(U-V)/2$; its analytic label 1
is owner 0. Neither coordinates nor stored artifacts are relabelled.

**Retain proved parent points.** The selected initial-base recipe also reconstructs
proof-only owned hulls from the original native H-290/H-289 parent, whose same-object
full centered replay passed in exp-280. While streaming that accepted node, collect
each owner's `initial.groups` points and every accepted step's
`common_owned_kernel` points, assigned by `step.owner`. Use no point from exp-284.
The source order is initial point index, then increasing step index and kernel-point
index. Bind all sixteen steps, their owners and complete status to the accepted
parent receipt; retain the canonical object and JSON-path origins of these points.

For each owner $j$, form the exact pool

$$
Q_j=\operatorname{conv}\left(
 H_j^{\mathrm{initial}}\cup\bigcup_{r:\,\operatorname{owner}(r)=j}K_r
\right),
$$

where $K_r$ here denotes the recorded accepted `common_owned_kernel` point list,
not a newly computed finite polygon. Every such point was checked against all its
strict-core ownership planes. It remains strictly inside square $j$ for every
physical packing of the original, unconditional $C(V)$ parent. Replacing a stored
hull by grid-compressed convex combinations can forget a point computationally;
it cannot invalidate the already proved ownership fact. Convexity therefore makes
every point of $Q_j$ strictly owned throughout that parent domain.

Freshly check that each vertex of the parent's final compressed hull $H_j$ lies in
$Q_j$. Do not add final vertices to the source pool before this test: containment
is the control that the extraction retained all facts needed by the accepted
compression chain. Check every unordered pair of these **unconditional** parent
pools for disjointness. A nonempty intersection would contradict the accepted
endpoint in $C(V)$ and is a refused calibration inconsistency, not a new global
exclusion. This control would not apply to pools extracted from a future child
whose ownership already depends on $I$.

Now augment only $Q_0$ by the five freshly checked exp-282 points. Those additional
points are owned under $I$, so a shared point after this augmentation is a valid
conditional contradiction. Compare the ordinary final parent hulls with the five
points added to owner 0 against these augmented pools. A direct unpooled
intersection has priority. A pooled intersection absent from that matched unpooled
test demonstrates recoverable information lost from the represented compressed
hulls. In either case the exact common point proves the whole $I$ slice impossible;
no centre cases are needed. Do not attribute later combined improvements to
compression alone without their own matched comparison.

If neither direct test closes the slice, use the augmented pools in place of the
parent hulls in the unsplit and four-case constructions below. This reuses accepted
proof facts; it launches no producer update and imposes no 48-vertex producer cap.
Deduplicate exact coordinates while retaining their first source origin. Require
at most 512 raw pool points per owner before deduplication and 8,192 in total,
within the overall 16,384 arithmetic-input-vertex limit. Each pooled convex hull
has at most 128 vertices, both before and after owner 0's five-point augmentation.
The finite case hull may have at most 256 vertices, and
its closed intersection with a foreign pool may have at most 384. The latter
replaces the earlier 256-vertex intersection ceiling; the centre-polygon and
128-vertex finite-kernel limits do not change. All rational bit limits still apply.

**Necessary centre domains.** For every owner-0 row, intersect its closed interval
with $I$. Keep each nonempty intersection $J=[l,h]$, including the two singleton
seams. Define

$$
m_J=\frac12\min\{c(l)+s(l),c(h)+s(h)\},\qquad
W_J=[o+m_J,U-o-m_J]^2.
$$

Intersect each original residual polygon separately with $W_J$. Preserve singleton
and segment intersections. Do not convexify distinct residual pieces before this
clipping: clipping their convex hull could introduce centres between disconnected
pieces. If no piece survives in any relevant row, the necessary centre cover for
$D$ is empty, which already proves the closed-angle exclusion.

Otherwise evaluate $d=x+y$ and $e=y-x$ at all surviving vertices in all relevant
rows. Their exact global extrema define

$$
\alpha=\frac{d_{\min}+d_{\max}}2,\qquad
\beta=\frac{e_{\min}+e_{\max}}2.
$$

This is a frozen midrange rule, not a parameter chosen after a sign test. A zero
range is valid and creates duplicate closed cases; it causes no division by the
range and removes no case obligation. The four raw cases, in lexicographic order
with $-1$ before $+1$, are

$$
D_{\sigma,\tau}
=D\cap\{\sigma(x_1+y_1-\alpha)\ge0,
         \ \tau(y_1-x_1-\beta)\ge0\},
\qquad \sigma,\tau\in\{-1,1\}.
$$

Their union is $D$. A pose on a cut belongs to both relevant cases, and a pose on
both cuts belongs to all four. Each case halves the global width of both projected
centre coordinates, though this alone does not guarantee a useful owned hull.

In the clipping convention $a x+b y\le c$, the additional rows are
$(-\sigma,-\sigma)\mathbin{\cdot}x\le-\sigma\alpha$ and
$(\tau,-\tau)\mathbin{\cdot}x\le-\tau\beta$.
Apply them to each surviving residual piece before taking any hull. Within a fixed
row, the convex hull of the surviving pieces may then be used for ownership tests:
those tests are affine in the centre, so this last convexification changes no
extremal inequality. An empty case is proved only when every relevant row piece is
empty. It is not inferred from an empty common-owned polygon.

**Finite ownership and contradiction.** First run the same construction without
the two centre cuts as a matched unsplit control. For it and each nonempty case,
construct $K\subseteq[0,U]^2$ using the H-292 ownership rows, with the unchanged
$\epsilon=2^{-20}$. For every relevant row, every surviving centre vertex $x$,
every corner $(c,s)$ of $[c(h),c(l)]\times[s(l),s(h)]$, and each
$\eta\in\{-1,1\}$, require

$$
\begin{aligned}
\eta c p_x+\eta s p_y
&\le 1/2-\epsilon+\eta(c x_x+s x_y),\\
-\eta s p_x+\eta c p_y
&\le 1/2-\epsilon+\eta(-s x_x+c x_y).
\end{aligned}
$$

These two signed pairs test both square axes. The rectangular coefficient enclosure
contains the whole closed angular arc; the positive margin makes every admitted
point strictly interior to square 1 for every physical packing of that case.

Let $H_0$ be the accepted parent's owner-0 hull and put
$H=\operatorname{conv}(H_0\cup K)$. Use **all** vertices of $K$ for this finite
proof object. There is no eight-point proposal selection and no 48-point producer
hull ceiling here. The old $H_0$ points are owned by the accepted parent; they need
not satisfy the new sufficient rows defining $K$ over its centre over-cover.

For every other owner $j$, in increasing owner order, test the exact closed
intersection $H\cap H_j$. Any shared point, including a point or segment of
intersection, proves the case impossible: it would lie strictly inside both
physical squares. Empty hulls contribute no intersection. Retain the first such
owner and a canonical common point, with exact hull-membership evidence. A small
witness may express that point as a convex combination of at most three vertices
from $H_0\cup K$ and at most three vertices of $H_j$, with nonnegative rational
weights summing to one. The fresh checker may instead reconstruct both hulls and
their exact closed intersection.

This is a rational linear feasibility problem for a common owned point. Its
feasibility certificate proves a contradiction for the packing case. Failure to
find such a point, even if certified for the entire constructed polygon, proves
only that this direct ownership recipe did not close the case. It does not prove
that a packing exists. No floating-point LP status is accepted as either outcome.

**Frozen decision rule.** Apply the parent-pool calibration and direct matched
unpooled/pooled intersection tests first. Then the unsplit control has priority: an empty necessary
centre cover or a shared owned point closes all of $D$ directly. Otherwise process
all four raw cases. Primary success requires an exact empty-centre or shared-point
contradiction for **every** case, followed by fresh reconstruction of the complete
cover and its four conclusions. There is no gain threshold substituting for this
exclusion. A complete run with any unresolved case misses the recipe's criterion;
retain any proved subcases as partial coverage. In particular, three closed cases
do not cover the fourth. A resource stop is incomplete, without a four-case verdict.
The result concerns the inherited centered parent and $I$ only; it supplies no
whole-mask, old-$U$-census or global-optimality admission.

Freeze one worker, 60 seconds for construction and 60 for fresh reconstruction,
120 seconds combined, with a sampled 4 GiB memory ceiling. Each phase includes its
own complete child extraction. Limit descriptors and accepted receipts to 10 MiB,
the conditional child to 64 MiB compressed and 512 MiB decoded, its extracted final
state and finite output to 64 MiB each. Admit at most 16,384 arithmetic input
vertices across the relevant residual pieces and all owned hulls; each used or
computed rational numerator and denominator has at most 4,096 bits. Limit each
intermediate centre polygon and constructed owned hull to 256 vertices, each
closed owned-hull intersection to 384 vertices, and each
intermediate or final $K$ to 128. These are resource limits, not geometric claims;
exceeding one is incomplete. Keep all four raw case identities even if their
geometry coincides.
The initial fallback retains its original-parent input limits instead: seed 10 MiB,
node 512 MiB compressed and 2 GiB decoded, and extracted final state 64 MiB. These
different input limits do not enlarge any finite arithmetic or output limit.

Target-free controls must cover all clipping signs, a centre on one or both cuts,
zero projected ranges, empty overall and individual cases, both chart-boundary
singletons, disconnected pieces clipped before convexification, both square axes
and all coefficient corners, strict versus boundary-only ownership, and point or
segment hull intersections. A four-case positive fixture, a three-of-four refusal,
an unsplit-priority fixture and a complete unresolved fixture check the decision
rule. Custody controls change each parent identity, guard, owner role and structural
join independently; byte, time, rational and polygon caps stop without a scientific
verdict. A fresh producer-free process must reconstruct a synthetic full receipt.
Pool controls must include a compression witness that drops an older proved point,
exact final-hull containment in the recovered pool, a pooled-only conditional
intersection absent from the matched final-hull test, duplicate source points,
changed kernel-owner or point-origin references, and an unexpected unconditional
parent-pool intersection that refuses the calibration.

The actual endpoint lies outside $I$, so retaining it in these four conditional
cases is not an applicable control. Its earlier full-root retention and the H-292
$Z$ calibration remain inherited premise references, not tests rerun here. Add a
target-free feasible-pose negative control instead: an owner-0 square with rational
half-angle $53/128$ and centre $(1,1)$, a disjoint axis-aligned square with centre
$(3,3)$, and owned hulls strictly inside those respective squares. Other synthetic
owners may have empty owned hulls; this tests the finite two-square implication,
not existence of a new seventeen-square packing. The centre case containing the
known pose must remain nonempty, its owned construction must contain a checked
strict-interior point, and it must not acquire a shared-owned-point contradiction.
The zero-range version places that centre in all four cases and checks that none
is silently dropped. A separate pure chart-zero fixture checks the same signs at an
endpoint without reading actual algebraic-root data.

For the initial fallback, all five previously selected points must satisfy the new
ownership inequalities of every nonempty case. Its clipped centre domains are
subsets of the original H-292 domains, with the same angular intersections and
margin, so this is a matched inclusion control. Do not impose that sufficient-row
test on points merely inherited from a complete child: an outer-envelope update
can over-cover older residuals even though their previously proved ownership
remains valid for every physical packing in $D$.

This contract is the sole Astra agent's prospective mathematical derivation. It
does not assert that the actual conditional round is nonclosed, that any partition
case is empty, or that the proposed resource ceilings will suffice. Registration
and source review must precede the first target construction.

## A Future Label-Bijection Extension

The current consumer requires all seventeen transported owners to equal the endpoint's
label-to-cell assignment. That is a conservative adapter restriction. The geometric
recipe arguments label otherwise identical unit squares by their coordinates and
roles; they do not require every core square to occupy its endpoint cell.

Let a freshly replayed leaf have seventeen occupied owners, and fix one bijection
$\sigma$ from the analytic labels to those owners. Apply one declared D4 action to the
entire leaf, and label each represented packing's square in owner $\sigma(i)$ by $i$.
This preserves containment and every physical non-overlap relation. If exact bounds
computed over all row pieces establish the relevant root-coordinate, angle and slider
premises for these labels, the same geometric implication applies. The local composition
route still requires the transported square-6 region to lie in the declared closed S2
cell. The direct sixteen-square arguments retain their own stated premises.

This observation does not prove that a suitable bijection exists for any particular
leaf. A future consumer may accept one supplied bijection after checking it and all
uniform bounds. It must not choose different labels for sampled poses and then treat
the samples as a cover of the leaf. A search over candidate bijections may produce a
witness, but failure to find one leaves the leaf unresolved. Any partition into several
labelling cases needs its own complete closed-coverage certificate.

This is a proposed future contract, not an expansion of H-286's first endpoint-labelled
adapter. It identifies a route by which other cell states could reach the existing
geometric proof without changing that proof's position or angle thresholds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
