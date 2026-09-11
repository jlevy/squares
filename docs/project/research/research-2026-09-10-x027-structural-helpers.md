# X027: Seven Corner Marks, Contact Components, and Relational Helpers

Date: 2026-09-10. Author: GPT-6 Astra, max reasoning.
Entry: mathematical idea development, workflow W3; coordinator bead `think-jx95`.
Status: analytical deductions with independent review, followed by unrun proposals.
No packing bound or experimental verdict changes.

Consider eleven squares of side one inside a larger square, allowing rotation and
boundary contact. At container side $q=96/25=3.84$, the retained weighted-point argument
forces at least seven of eight specified points near the corners into the selected
smaller squares used by the proof.
At least three corner pairs are therefore fully occupied: either one smaller square
contains both points, or two different squares contain them.
A separate geometric argument bounds the number of unit squares touching a wall by
three. Combined with an earlier theorem that chooses a convenient arrangement, this also
constrains which squares can be connected by physical contacts.

This report proves those deductions and states the extra work needed to use them in a
packing exclusion.
[X-027](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md)
is the downstream reading entry and strategic synthesis that consumes these results.
Its recommendations are not premises of the proofs here.

## 1. Fixed Premises and the Current Negatives

### Squares, cores, and contact

Write $K_q=[0,q]^2$ for the square container.
A **pose** specifies a centre $z$ and an orientation angle $\theta$. If $R_\theta$
denotes rotation through $\theta$, its closed unit square is

$$
Q(z,\theta)=z+R_\theta[-1/2,1/2]^2.
$$

Angles differing by a quarter turn describe the same square.
In the companion reports’ notation, this is $S_p$ at pose $p=(z,\theta)$. A **physical
packing** $\mathcal P=(Q_1,\ldots,Q_{11})$ means that every $Q_i$ lies in $K_q$ and the
square interiors are pairwise disjoint.
Here $\operatorname{int}Q_i$ means the interior, with its boundary removed.
Physical squares may share edges or vertices.

The certificate method selects a smaller closed square $C_i$ inside each physical square
$Q_i$, called its **core**. The original unit square is its **parent**. Each core has
side $0<B<1$, the same centre as its parent, and an orientation from a finite list
called the **direction net**. An admitted geometric selection rule places it strictly
inside the parent:

$$
C_i\subset\operatorname{int}Q_i.
$$

The constant $D$ bounds the tangent of the absolute angular difference between a parent
and its selected core.
Its exact value and the strict-containment argument are part of the source premises
below. Cores of different squares are disjoint even as **closed sets**, so they cannot
share boundary points.
This stronger disjointness permits point mass on a core boundary to count safely.

A **physical contact** occurs when two closed parents meet.
The **physical contact graph** has one vertex for each parent and an edge for every such
contact. A **contact component** is a maximal group joined by chains of these edges; a
**contact path** is a sequence of distinct parents in which consecutive parents meet.
Contact need not have positive length, and physical contact between parents does not
make their strict cores touch.
A wall contact means that a parent meets that container wall, possibly at only one
vertex.

### Weighted points and ownership

A nonnegative **point measure** here is a finite collection of sites $x_\ell$ with
weights $a_\ell\ge0$. For any region $E$, its captured mass is

$$
\mu(E)=\sum_{\ell:x_\ell\in E}a_\ell.
$$

Its total mass is $M=\mu(K_q)$. A **core domain** is a declared set of permitted core
placements. A point **cover** of that domain gives $\mu(C)\ge1$ to every core $C$ in it.
If the domain contains every selected core of a hypothetical packing, closed-core
disjointness gives

$$
11\le\sum_{i=1}^{11}\mu(C_i)\le M.
$$

Thus $M<11$ would exclude the packing.
The auxiliary measure used here has $M>11$; its role is to restrict the mass left
outside the cores, not to prove that exclusion directly.

A **mark** is one of the eight specified sites near the four corners.
A mark is **owned** when it belongs to a selected closed core, and that core is its
**owner**. Membership on the core boundary counts.
Containment in a parent alone is insufficient for this definition.
The four corners are denoted
$\mathcal C=\{\mathrm{BL},\mathrm{BR},\mathrm{TL},\mathrm{TR}\}$: bottom-left,
bottom-right, top-left and top-right.
The bottom-left pair is

$$
m_1=\left(\frac{3152}{3175},\frac{2336}{3175}\right),\qquad
m_2=\left(\frac{2336}{3175},\frac{3152}{3175}\right).
$$

The other pairs are obtained by symmetries of the container.
Its group $D_4$ consists of the eight rotations and reflections preserving the square;
an **orbit** is the set of distinct images under those transformations.
These marks are the full $D_4$ orbit of $m_1$.

The corner argument uses exactly the
[BC303 ownership measure](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md#3-replay-of-the-corner-pair-theorem-lane-c):

| Item | Fixed value or convention |
| --- | --- |
| Container | $q=96/25$ |
| Selected core side | $B=9977/10000$ |
| Angular mismatch bound | $D=207107/90000000$, with the admitted 181-direction representation and its reflected directions |
| Measure | 377 sites; total $M=22524199/2000000$ |
| Core charge | $\mu(C)\ge1$ for every admitted core, independently replayed |
| Uncovered allowance | $\varepsilon=M-11=524199/2000000$ |
| Eight corner marks | The complete $D_4$ orbit of $m_1$ |
| Weight of each mark | $w=106251/800000$ |
| Ownership | Membership in a selected **closed** core; boundary membership counts |

No core contains marks from different corners.
The source verifies that the least squared distance between such marks exceeds the
squared core diameter:

$$
\frac{34668544}{10080625}>2B^2=\frac{99540529}{50000000}.
$$

### Conditional domains and fractional obstructions

An **owner class** groups cores by an owned mark and a closed angular **sector**, an
interval of permitted directions for axes chosen toward the core’s centre from that
mark. The
[sector construction](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md)
retains every allowed sign and endpoint choice.
Two marks and eight sectors give sixteen labels per corner; a core may carry several
labels.
An **angle cell** is a specified interval of angles whose entire continuous range
must be considered.

A **common footprint** is a region contained in every owner core of a class.
Selecting owners leaves **residual squares**, the remaining physical squares.
Their core domain can be restricted by requiring avoidance of the occupied footprints.
Such a domain is usually a **relaxation**: it contains every physically possible
residual core and may also contain cores that cannot coexist with full owners or other
residuals. An **escape** is a core in this domain that misses a proposed cover.
It refutes that cover on that domain; it need not extend to a physical packing.

A finite **fractional family** assigns nonnegative weights $b_j$ to core placements
$C^{(j)}$, allowing them to overlap.
Its **depth** at a point $x$ is

$$
d(x)=\sum_j b_j\mathbf 1_{C^{(j)}}(x),
$$

where the indicator $\mathbf 1_E(x)$ is one when $x\in E$ and zero otherwise.
If $d(x)\le1$ everywhere, any point cover of all these cores has mass at least
$\sum_j b_j$, by summing the coverage requirements.
A retained family of sufficiently large weight is therefore an **obstruction** to a
proposed point-cover budget, not an integral physical packing.
**Survivors** are its cores remaining after a restriction; their surviving weight has
the same interpretation if they satisfy the new domain.
Here a **neutral** owner class means that the retained patch restriction deletes only as
much fractional weight as the number of selected owners, leaving no strict budget
advantage from that particular family and restriction.

A **threshold charge** uses a finite site set $A$ and a positive integer $t$: it charges
one to a core containing at least $t$ sites of $A$. Disjoint closed cores collect at
most $\lfloor |A|/t\rfloor$ such charges, where $|A|$ counts the sites and the floor
rounds down to an integer.
These additional capacities need not hold for every depth-one fractional family.
Thus a point obstruction does not automatically obstruct a certificate using threshold
charges.

### What is imported and what is new

**Admitted** means accepted by the project’s documented source, proof or computational
replay checks.
A **normal form** here means a representative packing obtained by changing
positions while keeping the container side and each labelled orientation fixed.
S1 is the name of the earlier theorem providing such a representative with the contacts
stated in the table.

| Input or result | Evidentiary role | Where it is used |
| --- | --- | --- |
| BC303’s measure, core selection and mark distances | Admitted baseline source facts | Lemma A, the owner count and the surplus inequality in Section 2 |
| Containment and disjoint radius-$1/2$ disks inside unit squares | Elementary geometric premises, used in the calculation below | Lemma B in Section 5 |
| [Fixed-side normal form S1](../reviews/review-2026-09-10-n11-structural-normal-forms.md) | Independently reviewed baseline theorem: any feasible packing has a representative at the same side and with the same labelled orientations whose physical contact components each touch both left and bottom walls | Combined with Lemma B for the component cap; combined with distinct corner owners for the contact-path consequence |
| Lemmas A and B and their displayed consequences | New analytical deductions in this report, independently checked | Structural inputs consumed by the downstream X-027 synthesis and the prospective helpers below |
| Sibling reports’ cross-reviews | Assurance: independent checks of these proofs and source readings | Review confidence only; no sibling theorem is a premise of Lemma A or Lemma B |

S1 proves that a representative with the stated contacts exists; it does not assert
those contacts in every starting packing.

The fractional-duality and certificate-mechanisms reviewers both passed the elementary
lemmas, the eighty abstract ownership patterns, the distinct-owner count and the
component consequence.
The fractional reviewer also re-read BC303 and checked the surplus identity and the path
joining owners from different corners.
The coordinator checked the arithmetic separately.
These checks are not new frontier theorem registrations.
Their direction is from source facts to the proofs here, then to X-027’s synthesis;
navigational links and reciprocal reviews introduce no circular proof dependence.

### Limits established by earlier work

The [evidence report](research-2026-09-09-n11-evidence-and-inference.md) and
[X026](../../../packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md)
keep the relevant failures separate:

- T023 excludes one specified four-owner branch at $q$, with its admitted symmetry
  transports. It supplies neither all raw class closure nor routing of every physical
  packing to an excluded selection.
- Exp150 supplied separate side-$B$ core owners compatible with exp149’s escape.
  Exp151 concerns a different escape;
  [exp156](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-156-unit-parent-saved-residual.md)
  completely excludes that escape against its top-right owner already in the model
  requiring only side-$B$ core geometry.
  Repeating that parent comparison cannot measure parent gain.
  The other three corners were not evaluated by exp156.
- Exp152’s two retained escapes intersect.
  Exp153 excludes every sixth site added to the fixed five-site pattern on its named
  relaxation. Neither result is a disjoint two-core obstruction to arbitrary added mass.
- The translated depth-one family has
  [explicit individual unit parents](../reviews/review-2026-09-10-n11-parent-domain-translation.md)
  from side $3.82345$. Individual parent realizability means that each core separately
  has a possible contained unit parent; it does not require those parents to coexist.
  Tightening that condition cannot remove this point obstruction at $3.827$ with the
  retained $B$ and directions.
  Full-owner compatibility, ownership, joint realizability and changed charge languages
  remain additional conditions.
- Neutral classes in the retained patch model, including cores 59 and 60, obstruct point
  closure of those domains.
  They do not establish that a physical packing admits only neutral selections.

The last two statements are proved at their own regimes.
They are not identities between the unrestricted problem at side $3.827$ and the owner
problem at side $3.84$.

## 2. Seven of Eight Marks Are Owned

**Lemma A, independently reviewed.** Every hypothetical eleven-unit-square packing in
$K_q=[0,96/25]^2$, with the admitted core selection above, owns at least seven of the
eight corner marks.

**Proof.** Write the disjoint selected cores as $C_1,\ldots,C_{11}$. Their total
captured measure is at least eleven, so

$$
\mu\!\left(K_q\setminus\bigcup_{i=1}^{11}C_i\right)
=M-\sum_{i=1}^{11}\mu(C_i)\le\varepsilon.
$$

Any two unowned corner marks would contribute $2w$ to this uncovered measure.
But

$$
2w-\varepsilon
=\frac{106251}{400000}-\frac{524199}{2000000}
=\frac{441}{125000}>0.
$$

Thus at most one of the eight marks is unowned.
This uses the same global uncovered allowance once, rather than applying it
independently to each corner.
∎

This is a consequence of the admitted measure, not a new certificate or a new lower
bound.
It also applies to an eleven-square packing in a smaller container embedded in the
same $K_q$ frame; moving the marks to that smaller container’s own corners would be a
different statement.

### Co-ownership or an additional owner

At least three corner pairs are fully owned.
Each fully owned pair has precisely one of two incidence types:

- **Co-owned:** one selected core contains both marks.
- **Split:** two distinct selected cores contain the two marks separately.

Closed-core disjointness makes the owner of an owned mark unique.
A core cannot serve two different corners by the cross-corner distance inequality.
Let $k$ be the number of distinct cores owning any of the eight marks, and let $\sigma$
be the number of split, fully owned corner pairs.
Then

$$
k=4+\sigma.
$$

If all eight marks are owned, $0\le\sigma\le4$; if exactly seven are owned,
$0\le\sigma\le3$. Selecting these distinct owners leaves $11-k=7-\sigma$ physical
residual squares.

At the incidence level there are only

$$
2^4+8\,2^3=80
$$

patterns: sixteen with no missing mark and sixty-four obtained by choosing the unique
missing mark and the co-owned/split type at each of the other three corners.
These are **abstract ownership patterns**, before sectors, positions, angles or
geometric feasibility.
They are not eighty feasible packings and do not replace continuous owner domains.
The actual pattern of a packing belongs to this list without making an arbitrary
four-owner selection first.

A co-owned pair supplies the whole segment between its marks by convexity.
To express the centre restriction, let $r$ be a unit vector along a retained core
direction and let $Jr$ be its quarter-turn rotation.
Write

$$
C_r^0=[-B/2,B/2]r+[-B/2,B/2]Jr
$$

for the side-$B$ core shape centred at the origin.
Here sums of scaled intervals mean all vector sums, so a translated core is $z+C_r^0$.
Containing both marks requires

$$
z\in(m_1-C_r^0)\cap(m_2-C_r^0).
$$

Here $m-C_r^0=\{m-y:y\in C_r^0\}$ is exactly the set of centres whose translated core
contains $m$. Container, parent and sector restrictions must also be imposed.
A split pair instead supplies two owners with joint disjointness and two distinct roles.
Keeping only one owned mark discards one of these two kinds of information.

There are immediate controls against overclaiming.
The retained neutral cores 59 and 60 themselves contain both bottom-left marks, so
co-ownership alone does not eliminate their fixed-family point obstruction.
The
[X022 counterexamples](../../../packing/campaign/explorations/X-022-segment-ownership-continuation.md)
include two adjacent split corner pairs carried by four diamond squares.
Adjacent split pairs cannot be declared incompatible merely from their labels.

### A common surplus budget

The same measure gives a resource inequality for these patterns.
Let $U_\mu$ be its uncovered mass and let $\xi_i$ be the surplus above one captured by
core $C_i$:

$$
U_\mu=\mu\!\left(K_q\setminus\bigcup_{i=1}^{11}C_i\right),
\qquad \xi_i=\mu(C_i)-1\ge0.
$$

Then the exact identity is

$$
U_\mu+\sum_{i=1}^{11}\xi_i=\varepsilon.
$$

Let $u\in\{0,1\}$ count the unowned marks in the pattern.
Then $U_\mu\ge uw$. For corner $c\in\mathcal C$, let $I_c$ be the set of indices of its
distinct owner cores.
Suppose a local proof, valid throughout that corner’s declared role, establishes
$\sum_{i\in I_c}\xi_i\ge\gamma_c$ for some $\gamma_c\ge0$. The sets $I_c$ are disjoint
across corners. Thus every physical realization must satisfy

$$
uw+\sum_{c\in\mathcal C}\gamma_c\le\varepsilon. \tag{1}
$$

With one missing mark the remaining surplus allowance is exactly

$$
\varepsilon-w=\frac{517143}{4000000}.
$$

Equation (1) is a way to use one common measure across co-owner and split-owner helpers.
A strict reverse inequality excludes that pattern.
The missing-mark charge cannot be counted again as owner surplus, and the same owner
cannot contribute to two corner minima.
Arbitrary independently chosen measures do not give this sum.

This is a modest extension of the weighted ownership-transfer mechanism in
[X021](../../../packing/campaign/explorations/X-021-what-can-be-proved-about-eleven-squares.md).
Its benefit is unmeasured: all useful $\gamma_c$ might be zero on the required domains.

### First discriminator and stopping rule

Lemma A and the 80-pattern incidence calculation use the already reviewed eight weights
and total mass; their independent mathematical cross-review has passed.
No new geometric target is necessary for that deduction.
A maintained finite allocation reader, if commissioned, should derive the owner count
from mark-to-core identities and reject double-counted owners; its controls should
include zero, one and two missing marks and the retained adjacent split-pair
construction.

The first geometric target should use fixed retained inputs before commissioning eighty
separate optimization problems.
One option is to freeze the four symmetry-related, explicit neutral co-owner poses
derived from core 59 at $q$, first verify their full unit parents and mutual
compatibility, then screen the same retained 88-core family against those **full
parents**. Compare its surviving weight with the seven-unit requirement and the matched
core-only obstacles.
This asks whether parent geometry coupled to actual co-owners removes the known
obstruction. No such screen was run here.

Strictly lower survivor weight would remove this particular obstruction and justify one
follow-up on an **owner cell**, a specified range of centres and angles with at least
one continuous parameter interval of positive length.
It would not establish a residual cover.
Surviving weight at least seven would stop this fixed-source point-only direction.
Either outcome leaves other incidence patterns, threshold charges and routing open.
A fixed-pose success cannot be silently treated as a whole co-owner class.

An alternative discriminator is one complete local surplus minimum for a fixed co-owner
or split-owner cell under the 377-atom measure, compared with the allowance in (1).
Choose between these after checking which existing exact instrument needs less new
surface; do not fund both by default.

## 3. Owner Choice Is a Routing Problem

**Routing** means proving that every hypothetical physical packing has at least one
valid choice of owners belonging to a case already excluded.
To state the quantifiers, let $\Lambda_c$ be the finite set of all owner-class labels at
corner $c$. For a physical packing $\mathcal P$, fix its admitted selected cores and let
$A_c(\mathcal P)\subseteq\Lambda_c$ be its nonempty set of valid labels, retaining every
admitted sign and boundary choice.
Since cores from different corners are distinct, independent local choices combine into
the product

$$
\Gamma(\mathcal P)=\prod_{c\in\mathcal C}A_c(\mathcal P).
$$

This Cartesian product is the set of tuples choosing one available label at each corner.
Let $G\subseteq\prod_{c\in\mathcal C}\Lambda_c$ be the set of tuple labels whose
associated cases have been excluded.
Sufficient routing is

$$
\forall\mathcal P\text{ feasible in }K_q,\qquad
\Gamma(\mathcal P)\cap G\ne\varnothing. \tag{2}
$$

Labels record too little to imply geometric feasibility.
In particular, a raw neutral tuple is not a counterexample to (2).

An elementary finite toy shows the difference.
Give two corners labels $a_0,a_1$ and $b_0,b_1$, and exclude $(a_0,b_0)$ and
$(a_1,b_1)$. Every packing with both choices available at either corner routes to an
excluded tuple, since the other availability set is nonempty.
Only the two opposite singleton availability pairs remain bad.
Excluding those **forced-choice situations** suffices; one need not separately exclude
every configuration that admits an off-diagonal label.

For the real finite label set, every availability product missing $G$ lies inside a
maximal product $\prod_{c\in\mathcal C}E_c$ that also misses $G$, with each
$E_c\subseteq\Lambda_c$ nonempty.
Here **maximal** means that enlarging any factor introduces a tuple from $G$. Finiteness
guarantees such a containing product.
These products give a finite list of candidate situations in which routing might fail.
Lemma A imposes additional mark-availability restrictions on that list, while
co-ownership records whether two labels refer to the same core.

The first routing discriminator should construct this abstract remainder from the
actually certified T023 transports and the seven-mark rule, then identify one geometric
implication that excludes a remainder.
A shorter abstract list alone is not a theorem about physical packings.
Stop if the reduction leaves essentially the same geometric obligations or if a proposed
implication fails a retained local counterexample.
Reopen when another certified tuple or an independently proved incidence implication
changes the remainder.

## 4. Relations Retain Information That Footprints Lose

Fix one class at corner $c$. Let $\mathcal O_c$ be the set of all its allowed owner core
placements, and let $R$ be a residual core.
Define the compatible-owner set

$$
\mathcal F_c(R)=\{C\in\mathcal O_c:C\cap R=\varnothing\}.
$$

This is the closed-disjointness rule for strict selected cores.
If the owner is a full parent $Q$ and the residual is a strict core $R$, the necessary
condition is still $Q\cap R=\varnothing$. If both variables are physical parents $Q$ and
$Q'$, their rule is instead $\operatorname{int}Q\cap\operatorname{int}Q'=\varnothing$,
permitting boundary contact.
A comparison must specify which objects it uses.

The single-owner test asks whether $\mathcal F_c(R)$ is empty.
For a collection of $t$ residual cores $R_1,\ldots,R_t$, the necessary shared-owner
condition is

$$
\bigcap_{i=1}^t\mathcal F_c(R_i)\ne\varnothing. \tag{3}
$$

The same owner must coexist with all residuals.
Separate nonempty sets do not establish (3). A finite toy uses two allowed owner poses,
$C^{(0)},C^{(1)}$: residual $R_0$ is compatible only with $C^{(0)}$, and $R_1$ only with
$C^{(1)}$. Each residual passes the isolated test, but their pair cannot coexist with
any permitted owner.
This is a logical counterexample, not a constructed square-packing configuration.

There is a second consistency condition between different owners: choosing one pose from
each $\mathcal F_c(R)$ must also give mutually compatible owners.
Even nonempty relations for every pair of owner classes need not give a common tuple.
Three two-valued roles with pairwise “different value” constraints are the smallest toy:
each pair is satisfiable, but the triple is not.

These distinctions identify two forms of a bounded comparison worth testing:

1. Retain one owner variable shared by two residuals; exclude the pair when (3) fails.
2. Retain two or more owner variables and their mutual compatibility, instead of
   selecting a separate witness for every constraint.

The current BC337 construction tests a single residual at a time.
To compare its geometry with a common footprint, write a residual as $z+C^0$, where
$C^0$ is its fixed core shape centred at the origin.
For sets $E$ and $F$, their **Minkowski sum** is $E+F=\{e+f:e\in E,\ f\in F\}$, and
$-C^0=\{-y:y\in C^0\}$. The translated residual intersects an owner core $C$ exactly
when $z\in C+(-C^0)$. Thus the set of residual centres incompatible with **every** owner
is

$$
\mathcal K_c=\bigcap_{C\in\mathcal O_c}(C+(-C^0)).
$$

Assume $\mathcal O_c$ is nonempty; otherwise that owner class is already impossible.
Its common-footprint obstacle obeys only the inclusion

$$
\left(\bigcap_{C\in\mathcal O_c}C\right)+(-C^0)\subseteq\mathcal K_c.
$$

Minkowski addition need not commute with intersection.
BC337 already targets this difference for the top-right class, so treating it as a new
pairwise idea would duplicate active work.
The new proposal retains the **same** owner across multiple residuals or across an
incidence pattern.

The prepared
[two-attainer construction](../../../packing/cases/n11_five_dot_cover/two-attainer-source-admission.md)
starts from placements maximizing or minimizing specified coordinate projections, called
**attainers**, then attempts to move them to strict escapes with positive clearance from
the forbidden closed obstacles and the container boundary.
If its target passes, it would supply two disjoint cores missing the fixed five-site set
$\mathcal D$ in the patch relaxation.
The symbol $\mathcal D$ denotes those sites, whereas $D$ remains the angular mismatch
bound. Before using such a pair as an obstruction on a stronger conditional domain,
recheck the relevant shared-owner constraints.
If the pair fails (3), its obstruction does not transfer there.
If it passes, that establishes only the tested owner consistency, not eleven-square
feasibility. Exp149 and exp151 are an unsuitable substitute: their cores intersect, and
exp151 already fails the complete single-residual test at the top-right owner.

**Discriminator:** first obtain a fixed pair for which each residual separately has an
exact compatible-owner witness in the selected class.
These are the **unary controls**; they test one residual at a time.
Then freeze that pair and ask whether the complete owner domain contains a single owner
compatible with both.
A complete pair exclusion absent from the unary controls earns a small instrument for
jointly restricting residuals or bounding how many of them can occur together.
A compatible common owner stops that particular pair.
Exhausting an arbitrary pose sample proves neither outcome for the continuum.

Pair incompatibility can produce new capacity inequalities only after the charged events
are defined and universally checked.
A graph whose vertices are the finitely many cores of a retained fractional family and
whose edges record pair incompatibility may expose a missing inequality; it does not
automatically implement that inequality in the existing point or threshold certificate
language.

## 5. A Wall Has at Most Three Touching Squares

**Lemma B, independently reviewed.** In a packing of unit squares at $q=96/25$, at most
three squares touch any one container wall, including vertex contact.

**Proof.** Consider the left wall.
Choose an orientation representative $\theta$ modulo quarter turns.
The square’s horizontal and vertical spans have the same half-width

$$
h(\theta)=\frac{|\cos\theta|+|\sin\theta|}{2}
\in[1/2,\sqrt{2}/2].
$$

A left-wall contact puts the centre’s horizontal coordinate at $h(\theta)$. Let
$\Delta x$ and $\Delta y$ be the differences between the coordinates of two such
centres. Then $|\Delta x|\le(\sqrt{2}-1)/2$. Each unit square contains the open disk of
radius $1/2$ about its centre, its **incircle**. Disjoint square interiors imply
disjoint incircle interiors, so the centre distance is at least one.
Define the resulting lower bound on vertical separation by

$$
|\Delta y|\ge\eta
=\sqrt{1-\left(\frac{\sqrt{2}-1}{2}\right)^2}
=\frac{\sqrt{1+2\sqrt{2}}}{2}.
$$

All vertical centre coordinates lie in $[1/2,q-1/2]$, an interval of length $q-1=71/25$.
Four centres ordered vertically would require a span at least $3\eta$. But
$\sqrt{2}>7/5$ gives

$$
9\eta^2=\frac{9(1+2\sqrt{2})}{4}
>\frac{171}{20}>\left(\frac{71}{25}\right)^2.
$$

This is impossible. The other walls follow by symmetry.
∎

The proof works whenever $q<1+3\eta$. Equality at this sufficient threshold is outside
the stated exclusion.
Three touching squares occur already in an axis-aligned column, so this cap for
arbitrary packings cannot be reduced to two at $q$ by the same premises.

### At most three normalized contact components

Apply the independently reviewed
[fixed-side normal form S1](../reviews/review-2026-09-10-n11-structural-normal-forms.md)
to a hypothetical packing at $q$. It gives a representative with unchanged labelled
orientations in which every physical contact component touches both left and bottom
walls. Distinct components use distinct left-wall squares.
Lemma B therefore gives **at most three contact components**, and some component
contains at least four of the eleven squares.

This conclusion is existential for the normalized representative.
It does not hold for every untranslated configuration.
Select corner-mark owners **after** normalization, since the motion can change their
labels. Lemma A still applies to the normalized packing because its side and admitted
core premises are unchanged.

There is also a joint owner/contact consequence.
Select one core owner at each corner after normalization.
Their four distinct parents occupy at most three physical contact components, so some
component contains owners from **two different corners**. A genuine parent-contact path
therefore connects those corner roles.
This supplies six possible unordered corner pairs as endpoint types, with arbitrary
allowed intermediate squares.
The component containing that path need not be the one containing at least four squares.
Strict cores need not touch along a parent-contact path.

A component of four or more squares need not contain a long simple path; a star is a
combinatorial counterexample to that inference.
Physical contacts need not have positive length, the component need not be rigid, and
its squares need not share angles.
The existing adjacent-wall alternative remains valid: either one square touches both
left and bottom walls, a **snug square**, or a physical contact path of two through
eleven squares connects them.
A tilted snug square need not contain the actual container corner.

The new finite reduction is by one, two or three **physical components**, with at most
three parents touching each wall.
It suggests charging several connected squares together, or imposing their common wall
constraints on a residual **pilot**, a small comparison confined to a stated case.
It does not justify a broad enumeration of contact graphs yet.
The first useful target should remove a declared fractional obstruction with a complete
small component cell: a range of parent poses with the specified wall and pair contacts
imposed throughout. A count of possible graph labels by itself supplies no exclusion.

## 6. Continuous Segment and Angle Profiles

Stromquist’s reusable contribution is the resource shared by several squares under an
incidence pattern. The
[independent Memo I helper](../reviews/review-2026-09-07-stromquist-segment-helper.md)
compares one owner’s required segment length with the portion accessible from its owned
mark after another owner is placed.
Its $1/2$ constants concern the source’s six-square geometry and cannot be imported at
$q=96/25$.

For a candidate eleven-square helper, choose finitely many line segments $I_j$ and
nonnegative coefficients $\lambda_j$. The **trace** of a core $C$ on a segment is
$C\cap I_j$, an interval or the empty set by convexity.
Let $L_j(C)=\operatorname{length}(C\cap I_j)$ be its ordinary segment length.
Strict cores have disjoint traces, giving the shared resource inequality

$$
\sum_{i=1}^{11}\sum_j\lambda_j L_j(C_i)
\le\sum_j\lambda_j\operatorname{length}(I_j).
$$

An owner-specific lower bound can depend on its parent’s continuous angle.
For a relation between two owners, let the segments start at a mark $m_*$ owned by core
$C_A$. If another core $C_B$ is disjoint from $C_A$, convexity implies that the trace of
$C_A$ lies in the component of $I_j\setminus C_B$ containing $m_*$. This is the
**accessible component**: the part reachable along the segment from $m_*$ without
crossing $C_B$. Summing the whole free complement would lose that restriction.
A uniform lower bound on the length required by $C_A$ greater than an upper bound on the
accessible length left by $C_B$ excludes their specified incidence and angle case.

Lemma A supplies a reason to investigate such cells: it limits missing marks and
identifies co-owned segments or split-owner pairs.
The complete incidence pattern also specifies the other marks that each selected core
avoids. These are the kind of containments and exclusions the Memo I argument needs.
A core’s merely passing near a segment gives no positive length lower bound; the
[X022 segment capacities](../../../packing/campaign/explorations/X-022-segment-ownership-continuation.md)
are separate facts with their own ownership and tolerance conventions.

The first discriminator should fix one surviving incidence pattern and one pair of angle
intervals of positive length, derive exact clipping formulas and the accessible
components, then ask whether a strict demand-capacity gap holds throughout that cell.
On an interval avoiding odd multiples of $\pi$, write $t=\tan(\theta/2)$ for a
**half-angle coordinate**. The identities

$$
\cos\theta=\frac{1-t^2}{1+t^2},\qquad
\sin\theta=\frac{2t}{1+t^2}
$$

make the formulas rational once the square edges determining each clipped endpoint have
been specified. Keep the admitted parent-to-core selection rule when connecting this
helper to Lemma A; changing that rule requires re-establishing the ownership premise.
A midpoint sweep is only proposal work.
Axis endpoints, changes in the determining edges and equality cases belong to the proof.

Let $\theta_A$ and $\theta_B$ be the parent angles, let $d(\theta_A)$ be a proved lower
bound on the first core’s weighted trace length, and let $b(\theta_B)$ be a proved upper
bound on the weighted accessible length left by the second.
Both bounds must be uniform over the other allowed pose parameters.
If separate worst-case bounds lose the desired strict inequality, a **joint angle
profile** can retain the function

$$
d(\theta_A)-b(\theta_B)
$$

on a proved relation $\Omega$ of allowed angle pairs.
To exclude the case, this difference must be positive for every
$(\theta_A,\theta_B)\in\Omega$, and $\Omega$ must contain every physically possible pair
in that case. Replacing continuous profiles by two exact angles has no justification.
A complete global result must retain the other angle cells or establish a routing
theorem into the excluded ones.
Stop a pilot when a verified admissible pair defeats its proposed uniform gap; reopen
only with a new incidence restriction, segment resource or angle relation.

## 7. Choice of the Next Structural Slice

These proposals depend on the proofs above; none has been run.
Before a pilot becomes an experiment, its **admission** must check the input sources,
the geometric objects being compared, the complete domain and boundary conventions, and
an independent reader of the result.
The coordinator must then declare its criterion, work limit and stopping rule before
examining target output.
BC329 remains the next direct global-bound target; BC337 is the secondary single-owner
domain continuation.

| Direction | New information sought | First decision-changing result | Main limitation |
| --- | --- | --- | --- |
| Seven-mark allocation and common surplus | More owned marks, extra distinct owners, or paired containment | Reviewed lemma; then one geometry or surplus comparison using fixed retained inputs | The eighty patterns still contain continuous geometry |
| Shared-owner relations | One owner must serve several constraints simultaneously | Separate compatible-owner witnesses but a complete exclusion for the fixed residual pair | A packing proof must apply the pair relation to its whole declared domain |
| Contact-component resource | At most three normalized components, one containing at least four squares | One whole component cell removes a retained obstruction | Neither a short path nor shared angles follows |
| Segment/angle helper | Geometric incidence changes accessible length or required charge | A strict exact gap on a positive-width cell | Full cell coverage and remaining branches are substantial |

The first two deductions have passed independent mathematical cross-review; their proofs
need no target computation.
For the next implemented structural block, prefer one seven-mark/co-owner comparison
using fixed retained inputs or one shared-owner pair discriminator; choose according to
which can produce a consequential exact result with the admitted geometry.
The segment helper is the more ambitious follow-up once a surviving incidence pattern
has been identified.

The two-attainer target is worthwhile only if its result changes that choice.
The individual-parent negative at TR is settled, the isolated-parent global obstruction
has explicit realizations, and neutral patch refinement alone has named counterexamples.
BC329 can proceed as the direct bound lane while these structural propositions are
narrowed into a separate finite contract.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
