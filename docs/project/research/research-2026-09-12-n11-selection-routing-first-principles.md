# N11: The Missing Owner-Selection Theorem

Date: 2026-09-12. Analysis bead: think-979p. Review and retention bead: think-gldo.
Primary source revision: `9be2bf274e4c9f6dbca03c05cd6e21bb852af521`.

For the two owner tuples currently certified by T-023 and its admitted transports, the
remaining selection theorem has two exact parts: every corner must offer at least one of
the two certified local labels, and corners that force opposite choices must not coexist
in one hypothetical eleven-square packing.
The reviewed ownership and contact arguments prove neither part.
Exact four-parent configurations below satisfy eight-mark ownership and joint owner
compatibility while defeating either part.

The finite remainder consists of sixteen maximal products of available labels.
They have three symmetry types on the unrestricted physical domain.
If the proof uses S1 with its named left and bottom walls, the wall chart must also be
retained: only a two-element stabilizer remains, giving ten types rather than three.
No geometric branch is excluded by these counts.

The mathematical reductions, exact configurations, two new contact-path lemmas, and
surplus acceptance implications passed
[source-distinct review](../reviews/review-2026-09-12-n11-selection-routing-first-principles.md).
The correction readback accepts the narrower rejection scope and closes review finding
SEL-1. The imported facts retain their reviewed status.
No scientific target ran in producing or reviewing this analysis, and the argument uses
no BC329 outcome. The separation between a result and its derivation follows
[epistemics.md:75–89](../../../epistemics.md).

## The Exact Theorem and Its Physical Transfer

Fix \(q=96/25\), \(B=9977/10000\), the admitted direction net and snapping rule, the
eight BC303 marks, and the closed-core boundary convention.
An equipped physical packing \(P\) consists of eleven contained unit parents with
pairwise disjoint interiors and one coherent admitted choice of strict concentric core
inside each parent. The core selection is made once for the packing.
The admission argument establishes strict containment for every parent angle; it does
not restrict physical parents to the net angles.
See [TUTORIAL.md:208–248](../../../TUTORIAL.md) and the
[structural-helper definitions:28–67](research-2026-09-10-x027-structural-helpers.md).

Use corner order BL, BR, TL, TR. At each corner \(c\), let
\(\Lambda_c=\{0,\ldots,15\}\), with \(m_1:j0,\ldots,m_1:j7\) numbered 0 through 7 and
\(m_2:j0,\ldots,m_2:j7\) numbered 8 through 15. Let \(A_c(P)\) contain every label
actually realized by an owned mark of an actual selected core of \(P\), including every
allowed signed-axis and closed-bin endpoint choice.
Owning a mark on a core boundary counts.
Owning it only in the unit parent does not.
The
[sector proof:26–71](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md)
defines this overlapping label cover.

Every \(A_c(P)\) is nonempty.
Owners of different corners are distinct.
Consequently

$$
\Gamma(P)=\prod_{c\in\{\mathrm{BL},\mathrm{BR},\mathrm{TL},\mathrm{TR}\}}A_c(P)
$$

is the valid four-owner selection set for this one packing.
Its Cartesian-product form is sound because all its choices select parents already
present together in \(P\). It is not a product of independently feasible owner-pose
domains. The [helper report:422–465](research-2026-09-10-x027-structural-helpers.md) and
[X-027:625–649](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md)
make this distinction.

For an admitted family \(G\) of completely excluded conditional selections, the required
direct theorem is

$$
\boxed{\quad
\forall P\in\mathfrak P_{11}(q),\qquad
\Gamma(P)\cap G\ne\varnothing.
\quad} \tag{R}
$$

Here each conditional exclusion must apply to every physical realization of its label,
over the full declared residual domain, with its admitted snapping and counting
transfer. An escape test on a relaxation, an isolated owner witness, or an unchecked
tuple does not put a label in \(G\). This is the precise quantifier in
[X-028:244–287](../../../packing/campaign/explorations/X-028-n11-strategy-portfolio-draft.md)
and the [evidence account:241–272](research-2026-09-09-n11-evidence-and-inference.md).

To use S1, let \(\mathcal N_{LB}\) be the family satisfying S1’s proved left/bottom
contact and genuine-contact-basis conclusions.
S1 implies that every feasible fixed-angle translation component has a representative in
this family. It therefore suffices to prove

$$
\forall P^*\in\mathcal N_{LB},\qquad
\Gamma(P^*)\cap G\ne\varnothing. \tag{R-N}
$$

Select cores and owners after normalization.
The motion need not preserve \(A_c(P)\), the initial contact graph, or a preselected
separating-axis cell.
The valid implication is
\(\mathfrak P_{11}(q)\ne\varnothing\Rightarrow\mathcal N_{LB}\ne\varnothing\); it is not
the assertion that normalized labels were available in the initial packing.
See [S1:121–207](../reviews/review-2026-09-10-n11-structural-normal-forms.md), its
[independent review:58–143](../reviews/review-2026-09-10-n11-structural-normal-forms-independent.md),
and [helper report:621–645](research-2026-09-10-x027-structural-helpers.md).

For T-023, a selected valid tuple supplies four distinct owners and seven remaining
cores. The admitted five-dot cover meets every such residual core, and disjoint closed
cores cannot share a dot.
Thus \(7\le5\), a contradiction.
This is the complete conditional-to-global proof once (R) or (R-N) is supplied.
See [TUTORIAL.md:396–451](../../../TUTORIAL.md).

## What the Proved Incidence and Contact Facts Actually Enumerate

The BC303 measure has

$$
M=\frac{22524199}{2000000},\qquad
\varepsilon=M-11=\frac{524199}{2000000},\qquad
w=\frac{106251}{800000}.
$$

Each selected core collects at least one.
Two unowned marks would cost \(2w>\varepsilon\), so zero or one mark is unowned.
Different corners cannot share an owner.
For a fully owned corner pair, either one core co-owns both marks or two cores split
them. If \(\sigma\) pairs are split, the total number of mark owners is \(k=4+\sigma\).
The [reviewed proof:245–313](research-2026-09-10-x027-structural-helpers.md) gives this
exhaustive incidence list:

| Unowned marks \(u\) | Split pairs \(\sigma\) | Number of incidence patterns | Distinct mark owners \(k\) | Other parents \(11-k\) |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 4 | 7 |
| 0 | 1 | 4 | 5 | 6 |
| 0 | 2 | 6 | 6 | 5 |
| 0 | 3 | 4 | 7 | 4 |
| 0 | 4 | 1 | 8 | 3 |
| 1 | 0 | 8 | 4 | 7 |
| 1 | 1 | 24 | 5 | 6 |
| 1 | 2 | 24 | 6 | 5 |
| 1 | 3 | 8 | 7 | 4 |

The count is \(16+64=80\). For \(u=1\), choose the missing mark in eight ways and assign
co-owned/split status to the three full corners.
These patterns specify neither sectors nor parent poses.

The four-owner T-023 selection still leaves seven residuals even in a split pattern: the
additional mark owners are among those seven.
Using all \(k\) owners in a new certificate instead leaves \(7-\sigma\) residuals and
requires a correspondingly valid domain and budget.
Removing more owners does not itself produce a strict resource saving.
The
[sector banking proof:73–101](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md)
explains why a small guaranteed footprint does not bank one full unit.

For the same fixed measure, write

$$
U_\mu=M-\sum_{i=1}^{11}\mu(C_i),\qquad
\xi_i=\mu(C_i)-1\ge0.
$$

The exact resource identity is

$$
U_\mu+\sum_{i=1}^{11}\xi_i=\varepsilon.
$$

If a local or joint argument forces surplus \(\gamma_c\) from the distinct owners at
corner \(c\), every realization must satisfy

$$
uw+\sum_c\gamma_c\le\varepsilon. \tag{S}
$$

With one missing mark, the allowance is \(\varepsilon-w=517143/4000000\). One cannot
count the missing-mark charge twice, count one co-owner twice, or sum independently
chosen measures. See
[helper report:345–387](research-2026-09-10-x027-structural-helpers.md).
No useful positive \(\gamma_c\) is supplied merely by the incidence count.

After S1, each physical contact component touches left and bottom.
At most three parents touch each wall, hence there are one, two, or three components;
some component has at least four parents.
Four different corner roles therefore put two corner owners in a common component.
The endpoint pair can be any of the six unordered corner pairs.
The component containing those owners need not be the component with at least four
parents. See [helper report:577–663](research-2026-09-10-x027-structural-helpers.md).

Two additional elementary deductions narrow the contact bookkeeping without solving a
sector case:

1. **An owner-to-owner path count.** Choose a shortest path over all pairs of mark
   owners belonging to different corners.
   No interior vertex can be a mark owner: its corner differs from at least one
   endpoint, giving a shorter eligible path.
   There are only \(11-k\) unmarked parents, so some such path uses at most
   \(13-k=9-\sigma\) parents.
   This is an existential count for some pair of corner roles, not a two-parent or
   three-parent theorem, a prescribed endpoint theorem, or a bound for the wall-to-wall
   path.
2. **Right and top owners require at least three parents to the distant normalized
   wall.** Write \(a=3152/3175\). Every right-corner mark has
   \(x\ge q-a=1808/635>2\sqrt2\). A left-wall square and one square contacting it have
   their union within \(x\le2\sqrt2\), since each has horizontal width at most
   \(\sqrt2\). Thus a right-corner owner neither touches the left wall nor contacts a
   left-wall parent directly.
   Its path to that wall has at least three parents.
   The top/bottom statement follows by swapping coordinates.
   The exact positive square comparison is \((1808/635)^2-8=43064/403225>0\). These
   statements use mark containment in the parent and actual contact, not projection
   equality.

The first deduction uses only the reviewed component and owner counts.
The second uses the
[mark coordinates:98–130](research-2026-09-10-x027-structural-helpers.md) and
[square width formula:582–588](research-2026-09-10-x027-structural-helpers.md).
The source-distinct review checked both new deductions analytically.

## The Sixteen Products Left by T-023

The two transported occupied tuples in the declared local coordinates are

$$
g_0=(0,0,0,0),\qquad g_{15}=(15,15,15,15).
$$

There are four patch-and-dot certificate pairs but only two occupied tuple geometries.
The two dot patterns do not produce mixed tuples.
These are the family \(G_0=\{g_0,g_{15}\}\) used below; any later certified enlargement
would require recomputing the remainder.
See
[wall-containment-contract.md:55–113](../../../packing/cases/n11_five_dot_cover/wall-containment-contract.md).

For this family,

$$
\Gamma(P)\cap G_0\ne\varnothing
\quad\Longleftrightarrow\quad
\bigl[\forall c,\ 0\in A_c(P)\bigr]\ \lor\
\bigl[\forall c,\ 15\in A_c(P)\bigr].
$$

Consequently failure is exactly

$$
\exists c,d,\qquad 0\notin A_c(P),\quad 15\notin A_d(P). \tag{B}
$$

For each ordered pair \((c,d)\), define \(E^{c,d}_e\) to be the full local label set,
except delete 0 when \(e=c\) and delete 15 when \(e=d\). The sixteen products
\(\prod_e E^{c,d}_e\) are precisely the maximal nonempty products avoiding \(G_0\).

**Proof.** A product avoids \(g_0\) only if one factor lacks 0, and avoids \(g_{15}\)
only if one factor lacks 15. It is therefore contained in the product associated with
those two factors.
Restoring either deleted label admits the corresponding uniform tuple;
deleting any further label would not be maximal.
When \(c=d\), both labels are deleted from the same factor.
This proves completeness and maximality.

| Blocker relation | Ordered pairs | Physical-domain representative |
| --- | --- | --- |
| Same corner | 4 | BL lacks both 0 and 15 |
| Adjacent corners | 8 | BL lacks 0 and BR lacks 15 |
| Opposite corners | 4 | BL lacks 0 and TR lacks 15 |

The seven-mark rule restricts which marks appear inside an availability set, but it does
not specify their sectors.
At the level of those incidence premises, every one of the eighty patterns can assign
its owned marks labels other than 0 and 15. This is an abstract consistency statement,
not a realizability claim.
Intersecting the eighty incidence conditions with these sixteen blocker conditions is a
complete, overlapping cover of the remaining physical possibilities.

### A symmetry condition that cannot be dropped

On the full physical domain, global \(D_4\) transport gives the three types in the
table. Under diagonal reflection \(S(x,y)=(y,x)\), local labels obey
\(\tau(m_a:j)=m_{3-a}:(7-j)\), so 0 and 15 exchange.
See
[wall-containment-contract.md:101–113](../../../packing/cases/n11_five_dot_cover/wall-containment-contract.md).

The fixed family \(\mathcal N_{LB}\) is not invariant under every \(D_4\) map:
reflecting left to right changes the two named walls.
Within that chart, use only the identity and \(S\). Their action on blocker corners is

$$
(c,d)\longmapsto(Sd,Sc).
$$

Four pairs are fixed, namely those with \(d=Sc\); the remaining twelve form six pairs.
There are therefore ten orbits in the fixed left/bottom chart.
Keeping all sixteen ordered pairs is an equally sound and simpler bookkeeping choice.
Using three types while also imposing fixed left/bottom contacts would omit the
transformed wall charts.
Renormalizing after transport cannot repair that omission without a proof that the
required owner availability survives the second motion.

## The Two Missing Lemmas

For a packing \(P\), retain only the two relevant available types:

$$
V_c(P)=A_c(P)\cap\{0,15\}.
$$

The following two propositions are together equivalent to routing into \(G_0\) on the
declared physical or normalized domain:

1. **Local availability.** No corner has \(V_c(P)=\varnothing\).
2. **Consistency of forced types.** Among packings satisfying the first proposition, no
   two corners have \(V_c(P)=\{0\}\) and \(V_d(P)=\{15\}\), respectively.

If every \(V_c\) is nonempty and opposing singleton types are absent, either all corners
offer 0 or all offer 15. If some corner is a singleton, take its type; otherwise every
corner offers both. Conversely a common offered type implies both propositions.

These are the smallest useful separate obligations for this admitted tuple family: a
single-corner missing-choice condition and an incompatible forced-choice condition, with
adjacent/opposite geometry distinguished where needed.
They are not proved here.
In the normalized route, each retains the wall-chart qualification above.

The earlier proposed endpoint condition with \(E=\{0,7,8,15\}\) on one diagonal is
weaker than the availability needed for \(G_0\). Even proving that earlier condition
would not route directly to the two certified tuples.
See
[after-exp149-strategy.md:134–159](../../../packing/cases/n11_five_dot_cover/after-exp149-strategy.md).

Each missing lemma still quantifies over complete continuous realizations:

- Core orientations use the admitted finite net, but centres vary continuously and
  parent orientations range over their full snapping cells.
  The selected core must have a contained unit parent at the same centre.
  Parent orientation cannot be equated with the signed owner sector.
- The incidence pattern must use actual core identities.
  Co-ownership imposes containment of both marks and hence their segment; split
  ownership imposes two jointly disjoint parents.
  Every other owned or unowned mark condition must be retained.
- Absence of a label is absence from every valid mark, owner and signed-frame choice at
  that corner. Choosing a bad label from an owner that also offers a good one does not
  establish (B).
- Every owner variable is shared across all residual, contact and mark constraints.
  Full parent interiors must be pairwise disjoint; boundary contact is permitted.
  Strict cores are disjoint as closed sets.
- Contact equations must describe actual meeting parents, with all feature and
  separating-axis alternatives.
  A complete contact-basis reduction retains every remaining inequality and all singular
  or alternative-basis cases.
  Its angles remain real.
- Any surplus or segment contradiction must use a single valid resource inequality and
  count each physical owner once.
  The seven remaining parents cannot be replaced by seven independently feasible core
  poses.

The centre restriction for co-ownership is explicit in
[helper report:315–335](research-2026-09-10-x027-structural-helpers.md).
Shared-owner quantifiers and boundary rules appear at
[476–568](research-2026-09-10-x027-structural-helpers.md).
The continuous basis and segment obligations appear in
[normal-form review:351–423](../reviews/review-2026-09-10-n11-structural-normal-forms.md)
and [helper report:675–736](research-2026-09-10-x027-structural-helpers.md).

## Exact Controls Against Stronger Inferences

### Eight marks and joint owners do not force either missing lemma

Write \(a=3152/3175\), \(b=2336/3175\), and use an axis-aligned unit parent with an
axis-aligned concentric side-\(B\) core.
The following three local centres all co-own the two bottom-left marks \((a,b),(b,a)\):

| Centre | All available local labels | Relevant type |
| --- | --- | --- |
| \(z^N=(17/20,17/20)\) | \(\{1,2,13,14\}\) | Neither 0 nor 15 |
| \(z^+=(6/5,9/10)\) | \(\{0,7,13,14\}\) | Forced 0 |
| \(z^-=(9/10,6/5)\) | \(\{1,2,8,15\}\) | Forced 15 |

**Containment.** The largest coordinate difference from either mark is
\(6/5-b=1474/3175<B/2=9977/20000\), so both marks lie strictly in each listed core.
Each unit parent lies strictly within the container.

**Label calculation.** From \(z^N\), the rays toward the centre from \(m_1\) are north
and west, whose first counterclockwise-ordered ray has angle \(\pi/2\), hence bins
\(j1,j2\). From \(m_2\) the first ray is south, hence bins \(j5,j6\). For \(z^+\),
\(m_1\)'s first ray is east, hence bins \(j7,j0\), while \(m_2\)'s first ray is south.
Swapping coordinates gives \(z^-\). All signs are strict; only the deliberately closed
angular-bin boundaries supply the two labels per mark.

**Joint realization.** At each corner choose any of the three centres and transport the
whole parent and core by \((I,H,V,HV)\), where \(H(x,y)=(q-x,y)\), \(V(x,y)=(x,q-y)\).
Two different corners have a horizontal or vertical centre separation of at least
\(q-2(6/5)=36/25>1\). Thus all four unit parents are jointly disjoint, and all eight
marks are co-owned. Four \(z^N\) choices realize the missing-choice condition.
Mixtures of \(z^+\) and \(z^-\) realize adjacent or opposite forced-type conditions
while every corner offers one of 0 and 15. Containment and parent separation have
positive margins, so sufficiently small parent-angle perturbations within the admitted
axis snapping cell preserve these owner examples.

These are exact four-parent counterexamples to deductions from ownership and joint owner
compatibility alone.
They do not provide eleven parents, satisfy the eleven-core surplus identity as a full
configuration, or establish a normalized eleven-square packing.
They refute neither (R) nor (R-N). Whether those four-parent configurations extend to
eleven parents remains open.

A further control is the literal bottom-left parent \([0,1]^2\): its selected core
\([23/20000,19977/20000]^2\) co-owns both marks and offers \(\{3,4,11,12\}\), hence
neither certified type.
It satisfies S1’s singleton-component contact conditions locally.
Thus a hypothetical normalized packing with that singleton would fall in the
missing-choice branch, not automatically in a certified tuple.

The sources for these new calculations are the
[mark and core constants:110–130](research-2026-09-10-x027-structural-helpers.md) and
[signed-axis definition:28–63](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md).
They are not outputs from a scientific target.
The maintained
[selection-routing checker](../../../packing/devtools/check_n11_selection_routing.py)
replays them with exact rational arithmetic and finite enumeration.

### Other quantifier and geometry controls

| Proposed strengthening | Counterexample or precise obstruction | Scope |
| --- | --- | --- |
| A parent touching two adjacent walls occupies their literal corner | With axes \((4/5,3/5),(-3/5,4/5)\) and centre \((7/10,7/10)\), the parent touches both axes but has minimum \(x+y=3/5\) | Exact single-parent counterexample; [normal-form review:261–273](../reviews/review-2026-09-10-n11-structural-normal-forms.md) |
| Every optimum occupies corners | Two side-by-side axis squares centred vertically in a side-two container are optimal and occupy no corner | Refutes the universal statement; does not refute existence of another corner-occupying optimum, or an n11-specific theorem; [275–287](../reviews/review-2026-09-10-n11-structural-normal-forms.md) |
| S1 reduces physical angles to a prescribed finite set | S1 preserves every labelled angle. The retained six-square optimum has a rotational rattler at every angle | Refutes a general finite-angle inference; does not decide an existential n11-specific angle theorem; [independent review:392–398](../reviews/review-2026-09-10-n11-structural-normal-forms-independent.md) |
| Every normalized component has a snug square or a very short required path | The tilted pair at \(74/35\) is a singleton fixed-angle feasible component with no square on both named walls. Connectedness alone admits arbitrarily subdivided paths; component size alone also admits a star | The exact pair defeats the snug-only same-component reduction. The graph examples are combinatorial controls, not geometric n11 packings. Only the explicit \(9-\sigma\) owner-path count above is newly derived; [independent review:268–348](../reviews/review-2026-09-10-n11-structural-normal-forms-independent.md), [helper report:637–654](research-2026-09-10-x027-structural-helpers.md) |
| Independently chosen owners establish one shared owner | Compatibility sets \(\mathcal F(R_0)=\{Q_0\}\), \(\mathcal F(R_1)=\{Q_1\}\) are separately nonempty but have empty intersection | Exact logical countermodel, not a square fixture; [helper report:493–512](research-2026-09-10-x027-structural-helpers.md) |
| A surviving raw label refutes routing, or routing needs every raw label excluded | Let BL offer \(\{0,1\}\) and every other corner offer \(\{0\}\). The product contains both the excluded \(g_0\) and the unexcluded \((1,0,0,0)\) | Availability-level countermodel only; no eleven-packing assertion. It preserves the existential selection distinction in [X-028:246–259](../../../packing/campaign/explorations/X-028-n11-strategy-portfolio-draft.md) |

A geometric version of the shared-owner control uses the continuous unit-parent domain
\(Q_t=[t,t+1]\times[0,1]\), \(3/5\le t\le11/10\), and the two disjoint unit residuals
\(R_0=[17/10,27/10]\times[0,1]\), \(R_1=[0,1]\times[0,1]\). All fit in \(K_q\), and
every \(Q_t\)'s concentric axis core contains the same artificial mark \((27/20,1/2)\).
Parent compatibility with \(R_0\) requires \(t\le7/10\), while compatibility with
\(R_1\) requires \(t\ge1\). Both unary domains are nonempty and their intersection is
empty. This is an exact continuous square-geometry counterexample to exchanging the
quantifiers.
Its mark and restricted owner domain are controls, not the BC303 marks or an
admitted n11 owner class.

The retained neutral cores 59 and 60 already co-own the bottom-left marks and have
individually contained unit parents, yet obstruct their stated point-only patch domains.
They do not show that every selection of one physical packing is neutral.
See [helper report:337–343](research-2026-09-10-x027-structural-helpers.md) and
[evidence account:923–948](research-2026-09-09-n11-evidence-and-inference.md).
The retained four-diamond construction also prevents discarding adjacent split pairs
from the eighty patterns:
[X-022:64–80](../../../packing/campaign/explorations/X-022-segment-ownership-continuation.md).

## Two Falsifiable Mathematical Tests

These are proposed tests with declared accept/reject scopes, not registered experiments
or claims about likely gains.
These tests decide whether the stated one-corner or two-corner BC303 surplus inequality
holds on its declared domain.
A rejection leaves stronger domain restrictions and different resources or arguments
open.

### Test 1: Can one missing-choice corner overspend the common allowance?

Freeze the BC303 measure, \(q,B\), the complete admitted snapping cells, and the
missing-choice condition \(0,15\notin A_{\mathrm{BL}}\). Use the complete local parent
domain for each of four roles: one co-owner of both marks, two split owners, only
\(m_1\) owned, or only \(m_2\) owned.
Retain every valid label choice when enforcing absence.
For split owners require their unit parents to coexist.
Do not replace parent geometry by independently selected core witnesses.

For each role define the exact least total owner surplus

$$
\gamma_{\rm role}
=\inf \sum_{i\in I_{\mathrm{BL}}}\bigl(\mu(C_i)-1\bigr).
$$

**Accept the complete local helper** if every full-pair role is empty or has
\(\gamma_{\rm role}>\varepsilon\), and every one-mark role is empty or has
\(\gamma_{\rm role}>\varepsilon-w\), with complete continuous-domain proof.
Then the missing-choice condition is impossible in an eleven-square packing: other
owners and residuals have nonnegative surplus, and a one-mark corner forces the single
missing-mark cost. Global symmetry supplies every corner.
This proves the local-availability lemma, independently of contact normalization.
It leaves consistency of forced types open.

**Reject this local helper** with one exact admissible role witness whose surplus is at
or below the corresponding allowance.
That witness must exhibit its contained unit parent or jointly compatible split parents,
the selected cores, all label absences, and exact BC303 charges.
It refutes this one-corner resource inequality; it does not refute the global
local-availability lemma, because it need not extend to eleven parents or obey their
other constraints. The exact owner configurations above are controls, not premeasured
charge witnesses. Partial domain analysis is unresolved.

This test covers one complete logical failure type without assuming a finite set of
physical angles.
A rejection does not decide whether another local resource or a stronger
domain would prove local availability.

### Test 2: Can a forced-0/forced-15 pair overspend the allowance?

Freeze one adjacent or opposite ordered corner pair and the same source measure and
geometric conventions.
At the first corner require \(V_c=\{0\}\); at the other require \(V_d=\{15\}\). Include
every local mark-incidence role compatible with at most one missing mark, use all
distinct owners, and retain simultaneous full-parent compatibility across both corners.
Let \(u_{\rm local}\in\{0,1\}\) count missing marks in those two corners.

**Accept a pair helper** only with a complete proof that every realization of every
admitted role combination in that geometric pair domain satisfies

$$
\sum_{i\in I_c\cup I_d}\bigl(\mu(C_i)-1\bigr)
>\varepsilon-u_{\rm local}w,
$$

or that the domain is empty.
A missing mark elsewhere can only lower the true available surplus further, so this
inequality is sufficient.
It excludes that pair geometry independently of the omitted corners and residuals.
Both geometric types, adjacent and opposite, are needed to prove the forced-type
consistency lemma on the full physical domain.
A contact-conditioned version must instead retain the full wall-chart subdivision.

**Reject this pair helper** with one exact simultaneous parent realization having the
specified forced types and surplus at or below the threshold.
The mixed \(z^+,z^-\) constructions above control joint geometric feasibility before
charges are considered.
Rejection decides the named two-corner surplus mechanism only; shared residuals, contact
paths, other resources, or a larger certified tuple family remain separate obligations.

Neither test is a proof that the other lemma holds, a certificate for all residual
cores, or an eleven-square construction.
A successful complete inequality would discharge the stated part of the routing theorem.
A failed one would refute only that surplus mechanism; it would not identify which
additional information a future proof needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
