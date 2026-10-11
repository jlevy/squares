{{FRONT_MATTER}}

This paper explains the computer-assisted proof of a lower bound of 31/8 for eleven unit
squares, published by
[Kleddamag in 11-squares-certified-bound](https://github.com/Kleddamag/11-squares-certified-bound):
the
[proof](https://github.com/Kleddamag/11-squares-certified-bound/blob/6a733f339395c3514f2ab63d8c4aa64cf63c0b5a/PROOF.md),
[certificate](https://github.com/Kleddamag/11-squares-certified-bound/blob/6a733f339395c3514f2ab63d8c4aa64cf63c0b5a/global-certificate.json)
and
[reproduction](https://github.com/Kleddamag/11-squares-certified-bound/blob/6a733f339395c3514f2ab63d8c4aa64cf63c0b5a/README.md)
at the reviewed release, v1.0.2, retained in this project’s
[archive](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/README.md).
The source’s `AUTHORS.md` says OpenAI Codex developed the mathematics and computation
under Kleddamag’s direction; the certificate develops this project’s T-026 certificate,
the subject of [Part I]({{PAPER:n11-lower-bounds-explainer}}), and the result is
registered here as T-037.[^authors]

## The Result

A **unit square** is a square of side one, placed anywhere in the plane at any angle.
A **packing** of unit squares in a **container**, a larger square with sides parallel to
the axes, is a placement in which every unit square lies inside the container and no two
unit squares have a common interior point; their boundaries may touch.
Write $s(11)$ for the smallest container side that admits a packing of eleven unit
squares, and $L_0$ for the side of a container under test, both as
[Part I]({{PAPER:n11-lower-bounds-explainer#the-square-packing-problem}}) does; the
[Attainment lemma](#the-contradiction-and-the-strict-bound) shows that a smallest side
exists. A square is unchanged by a quarter-turn, so its angle is only defined modulo
$\pi/2$, and this paper takes every angle in $[0,\pi/2)$.

**Theorem.** $s(11)>31/8=3.875$: no packing of eleven unit squares fits in a container
of side $31/8$, and so none fits in any smaller container.[^statement]

The method is Part I’s: weighted positions in the container, arranged so that a small
square placed anywhere must enclose at least a fixed amount of weight while the total
available is less than eleven times that amount, so eleven squares with disjoint
interiors cannot all be paid.
The source changes three things:

1. **five-site k-of-m charges**: charges of the kinds 2-of-5 and 3-of-5 beside
   [Part I’s]({{PAPER:n11-lower-bounds-explainer#proof-of-the-new-lower-bound}}) 2-of-3,
   each paying a core that holds at least $k$ of its $m$ sites (defined in
   [From Points to k-of-m Charges](#from-points-to-k-of-m-charges));
2. **k-of-m charges on shrunken parents with strict cores**: the squares are shrunk to
   side $A=764/775$ in a container of side $191/50$, each with a core strictly inside
   it, defined in [Parents and the One Inequality](#parents-and-the-one-inequality);
3. **a reoptimized certificate over 12,028 adaptive angle rows**, each with its own
   core, replacing T-026’s net, Part I’s finite list of core directions (defined in
   [Parents, Cores and the Angle Catalogue](#parents-cores-and-the-angle-catalogue)).

<figure>
{{CHANGES_SVG}}
<figcaption><strong>Figure 1.</strong> What changed from T-026 to T-037. Left: the charge
families and the share of the budget carried by single points, {{CHANGES_T026_POINT_SHARE}}
of T-026’s budget over {{CHANGES_T026_POINTS}} point charges and
{{CHANGES_T026_TRIPLES}} charges of kind 2-of-3, against {{CHANGES_T037_POINT_SHARE}} of
T-037’s over four families. Middle: T-026’s core, a square of side $B = {{CHANGES_T026_B}}$
at one of its net directions, inside a unit square, against T-037’s parent of side
$A = {{CERT_A}}$ with a row’s core inside it. Right: T-026’s {{CHANGES_T026_NET}}-step net
of directions against T-037’s {{CERT_ROWS}} angle rows, each a closed interval. Both
certificates are read from their retained files, the
<a href="../../cases/n11_threshold_certificate/certificate-191-50-net1440.json">T-026 certificate</a>
and the
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json">T-037 certificate</a>.</figcaption>
</figure>

The proof gives no better packing and does not find the exact minimum.
Write $T=3.8770835900\ldots$ for the side of Walter Trump’s packing of 1979, the best
packing known; the **bound gap**, the distance between the best upper and lower bounds,
was ${{LADDER_GAP}}$ after this proof.[^register] The result was superseded within a
week: on 2026-09-29 Ke Wang and Can Li reweighted and scaled this same certificate to
$s(11)>3875000000/999999999$, a step of about $3.9\times10^{-9}$ (T-061), and Ahmed
proved $s(11)=T$ by different machinery (T-060), which
[Part III]({{PAPER:n11-optimality-review}}) reviews.
With T-061’s reweighting of it, it is the furthest the charge method reached, and Part
III’s field certificates, which also charge cores, are easiest to follow against it.

<figure>
{{LADDER_SVG}}
<figcaption><strong>Figure 2.</strong> The series bound ladder: the rungs of
the lower bound for eleven squares, from Stromquist’s $2+4/\sqrt5$ (T-010)
through Part I’s T-018, T-025 and T-026, then T-033, the bound in force when this
paper’s T-037 appeared, T-037 with T-061 beside it, and T-060 at Trump’s $T$. The rungs
are evenly spaced and labeled with the values the
<a href="../../frontier/results.yaml">register</a> holds; on a linear axis T-037 and
T-061 would coincide.</figcaption>
</figure>

<figure>
{{ROADMAP_SVG}}
<figcaption><strong>Figure 3.</strong> The proof’s route, section by section. Eleven unit
squares in a container of side ${{CERT_BOUND}}$ become eleven parents of side $A$ in a
container of side $L_0={{CERT_L0}}$; each parent is assigned a core by one of {{CERT_ROWS}}
angle rows; every legal center of every row collects charge at least $\Gamma$ from
{{CERT_SITES}} sites; and $11\Gamma={{CERT_ELEVEN_GAMMA}}$ exceeds the budget $M={{CERT_M}}$.
Each symbol is defined in the section named on its card.</figcaption>
</figure>

## From Points to k-of-m Charges

A **site** is a position in the container, and a **point charge**, which Part I calls an
atom, is a site with a nonnegative **weight**.[^paper-one] A **core** is a closed square
strictly inside a packed square, and a core **captures** a site when the site lies in
the core. The total weight of the point charges a core $Q$ captures is what Part I calls
its **mass** $\mu(Q)$. Part I’s
[Conditions 1 to 5]({{PAPER:n11-lower-bounds-explainer#the-five-conditions-for-a-point-certificate}})
say that the point charges are symmetric under the container’s symmetries, that their
total is below eleven, that a finite net of directions reaches $\pi/4$, that the core is
small enough to fit at every angle between net directions, and that every core at every
net direction captures mass at least one.

A **k-of-m charge** $(S,k,w)$ is Part I’s
[threshold atom]({{PAPER:n11-lower-bounds-explainer#proof-of-the-new-lower-bound}})
under the series’ name: a set $S$ of $m=|S|$ distinct sites, an integer **threshold**
$1\le k\le m$, and a nonnegative weight $w$; it pays $w$ to a core that captures at
least $k$ sites of $S$, and nothing otherwise.
Part I defines it for any $k$ and $m$, and its certificates use only 2-of-3. A point
charge is the case $m=k=1$. The **charge** $C(Q)$ of a core $Q$ is the sum over all
point and $k$-of-$m$ charges of what each pays it; for point charges alone it is the
mass.[^charges] The charge at index {{CHARGE_ORBIT}} of the source’s list, the heaviest
in the certificate, is a 3-of-5 charge of weight {{CHARGE_WEIGHT}} on the five sites
{{CHARGE_SITES}}, rounded here from their exact coordinates: a core that captures any
three of them is paid the whole weight, and one that captures two is paid nothing.

**Budget lemma.** Let $r$ pairwise disjoint cores each capture at least $k$ sites of a
$k$-of-$m$ charge.
The captured subsets are disjoint, so together they hold at least $rk$
distinct sites of $S$, and $rk\le m$. The charge therefore pays at most
$\lfloor m/k\rfloor$ of any family of pairwise disjoint cores, and at most
$w\lfloor m/k\rfloor$ in total, its **budget**.[^charges]

Part I leaves two consequences of the lemma implicit.
First, the inequalities add when charges share sites: each one is valid on its own, so
the total paid to any family of disjoint cores is at most the sum of the budgets, with
no requirement that the charges have disjoint supports.
Second, the 2-of-5 charge has $\lfloor 5/2\rfloor=2$: it is the first family in the
series’ certificates that can pay two disjoint cores, and its budget is $2w$. The 2-of-3
and 3-of-5 charges have budget $w$.

**Why k-of-m charges pay.** Suppose one wants every core that captures $k$ of the $m$
sites to be guaranteed $w$. Point weights of $w/k$ at the $m$ sites do it, at a budget
of $mw/k$; the $k$-of-$m$ charge does it at a budget of $\lfloor m/k\rfloor w$. The
ratio of the two prices is $3/2$ for 2-of-3, $5/3$ for 3-of-5 and $5/4$ for 2-of-5. When
$k$ divides $m$ there is no saving: a 2-of-4 charge costs $2w$ either way, which is why
this project’s threshold code notes that only the families with $k$ not dividing $m$ add
anything.[^threshold-code] The price of the saving is that a core capturing fewer than
$k$ sites is paid nothing, where the point weights would have paid it something.

<figure>
{{CHARGE_SVG}}
<figcaption><strong>Figure 4.</strong> One $k$-of-$m$ charge: the 3-of-5 charge at index
{{CHARGE_ORBIT}} of the source’s list, of weight $w={{CHARGE_WEIGHT}}$, the largest in the
certificate. The core on the left holds three of its five sites and is paid; the disjoint
core on the right holds two and is not. Inset: point weights of $w/3$ on each of the five
sites guarantee the same $w$ to a core holding three of them but can pay out $5w/3$
across disjoint cores, against the one charge’s $w$. The core placements were checked
exactly against the
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json">retained certificate</a>.</figcaption>
</figure>

Single points carry 79% of T-026’s budget and 20% of T-037’s. There is also a reason the
points could not have done it alone: T-025’s exact ceiling family shows that no point
measure of mass below eleven with the container’s full symmetry exists at the side
$191/50$ on T-025’s core domain, so no point certificate of Part I’s form on that domain
reaches even $3.82$.[^register]

## What Is New, and What It Inherits

Three labels sort the proof’s ingredients.
An ingredient is **inherited** when a registered or cited antecedent has the idea; it is
**new data** when it is the source’s instance of an inherited idea, chosen afresh; and
it is **new** when no antecedent is registered.
The source’s own attribution claims no invention of the weighted-covering or
threshold-counting methods.[^credit]

The inventory:

- The general $k$-of-$m$ charge and its budget $w\lfloor m/k\rfloor$ are inherited from
  Part I, where T-025 states them as the general threshold atom and uses the case
  2-of-3; T-025’s proof sums the budgets over all atoms, shared sites included, without
  remarking on it, and the source states the rule.[^credit]
- The [signed inclusion–exclusion](#every-legal-center-collects-enough-charge) of a
  $k$-of-$m$ indicator into rectangle terms, and the
  [integer difference sweep](#every-legal-center-collects-enough-charge) that evaluates
  it, are T-025’s; the source’s coefficients are the same.[^credit]
- 2-of-3 charges beside point charges over contiguous intervals of
  [parent](#parents-and-the-one-inequality) angles are inherited from Kleddamag’s own
  proof for seventeen squares (T-038); point charges over such intervals are older (next
  item), and T-037 is the first certificate of that form at eleven squares.[^register]
- The shrunken parent of side $A<1$, the bound $L_0/A$, one closed core per angle
  interval, and coverage required only over the centers a parent may legally occupy are
  inherited through the Levy/Guzhou0806/Mira line of parent certificates; the first
  registered certificate of that form is Guzhou0806’s R012 (T-032,
  2026-09-20).[^lineage]
- New: 2-of-5 and 3-of-5 charges in a retained certificate.
  The families are named in this project’s threshold code, and a study of 2026-09-10
  weighed five-site charges, but no earlier registered certificate uses them: T-025,
  T-026 and T-038 are 2-of-3 only, and the next, R052’s 3-of-5 at seventeen squares
  (T-039), is dated 2026-09-25.[^credit]
- New data: the certificate reoptimized from T-026’s, with sites rounded and added,
  families added, weights reoptimized, and the
  [catalogue](#parents-cores-and-the-angle-catalogue) replaced.[^credit]
- New: the bound $31/8$ itself, strict by attainment.[^statement]
- Not claimed: external review, priority, or how the certificate was found.[^statement]

The audit notes that the certificate changes several ingredients at once, with no
ablation that attributes the gain to any one of them.[^audit]

## Parents and the One Inequality

A **parent** is a square of side $A=764/775$ inside the container $[0,L_0]^2$, whose
side is $L_0=191/50$. Parents may rotate independently and touch; their interiors must
be disjoint.[^parents]

**Scaling lemma.** Eleven parents fit in a container of side $L_0$ exactly when eleven
unit squares fit in a container of side $L_0/A$, and

$$
\frac{L_0}{A}=\frac{191/50}{764/775}=\frac{191\cdot775}{50\cdot764}=\frac{31}{8},
$$

because $764=4\cdot191$ and $775=31\cdot25$. Scaling a packing by $1/A$ about the
container’s corner sends parents to unit squares and preserves containment and disjoint
interiors, and scaling by $A$ sends them back.[^parents]

This is Part I’s
[rational dilation]({{PAPER:n11-lower-bounds-explainer#t-026-finer-directions-and-the-new-lower-bound}})
read the other way: Part I scales the certificate up by $q$ and leaves the squares at
side one; here the squares are scaled down to side $A$ and the certificate stays at
$191/50$.

Every parent is given an **assigned core**, a closed square strictly inside it whose
side and angle depend only on the parent’s angle; how is the subject of
[Parents, Cores and the Angle Catalogue](#parents-cores-and-the-angle-catalogue).
$\Gamma$ is the least charge of any assigned core of any parent anywhere in the
container, and $M$ is the sum of the budgets of all the charges.
Eleven parents with disjoint interiors hold eleven pairwise disjoint assigned cores,
each of charge at least $\Gamma$, so the cores collect at least $11\Gamma$; by the
Budget lemma, summed over all charges, they collect at most $M$. If $11\Gamma>M$, there
is no packing of eleven parents, and by the Scaling lemma no packing of eleven unit
squares in side $31/8$.[^conclusion]

The certificate has $\Gamma={{CERT_GAMMA}}$ and $M={{CERT_M}}$, so
$11\Gamma={{CERT_ELEVEN_GAMMA}}>M$, a surplus of {{CERT_SURPLUS_UNITS}} units of
$10^{-9}$. Neither number is normalized: $\Gamma$ is a little below one and $M$ a little
below eleven, their ratio $M/\Gamma$ about {{BUDGET_RATIO}}, and the inequality, not
either value alone, is what is checked.

<figure>
{{BUDGET_SVG}}
<figcaption><strong>Figure 5.</strong> The budget against the requirement. The four
families’ budgets, {{BUDGET_POINTS}} for points, {{BUDGET_TWO_OF_THREE}} for 2-of-3,
{{BUDGET_TWO_OF_FIVE}} for 2-of-5 and {{BUDGET_THREE_OF_FIVE}} for 3-of-5, stack to $M={{BUDGET_M}}$;
eleven cores need $11\Gamma$. The inset magnifies the surplus of {{BUDGET_SURPLUS}} units
of $10^{-9}$, which is about one part in $10^5$ of $M$. The values are read from the
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/VERIFIED.json">source’s verified summary</a>
and recomputed from the certificate.</figcaption>
</figure>

## The Certificate’s Charges

The container has eight symmetries, the four rotations and four reflections of the
square, which form the group $\mathbf{D}_4$ of Part I’s
[Condition 1]({{PAPER:n11-lower-bounds-explainer#the-five-conditions-for-a-point-certificate}}).
The **orbit** of a site is the set of its images under the eight symmetries, of size
one, four or eight, and the orbit of a $k$-of-$m$ charge is the set of its images under
the eight symmetries, eight or fewer.
A certificate is **$\mathbf{D}_4$-invariant** when every point charge and every
$k$-of-$m$ charge appears with its whole orbit at equal weights.
The source file lists one site per site orbit and, for each charge orbit, every image
set under one weight; both checkers rebuild each orbit from its first member and confirm
that the listed images are exactly those.[^census]

The certificate’s {{CERT_ORBITS}} site orbits expand to {{CERT_SITES}} distinct sites.
Point weight is positive on {{FAMILIES_POINT_ORBITS}} orbits, {{CERT_POINT_SITES}}
sites;
{{FAMILIES_SHARED}} of those also belong to $k$-of-$m$ charges, and the other
{{FAMILIES_CHARGE_ONLY}} sites belong to $k$-of-$m$ charges only, so
{{FAMILIES_IN_CHARGE}}
sites are in some $k$-of-$m$ charge and none is unused.[^census]

Point weight concentrates where a parent’s inner edge can lie.
An axis-aligned parent touching a wall has its inner edge on one of the four lines
$x=A$, $x=L_0-A$, $y=A$ or $y=L_0-A$. Of the {{FAMILIES_POINT_ORBITS}} point orbits,
{{FAMILIES_NEAR_ORBITS}} lie within $0.005$ of one of those lines and carry
{{FAMILIES_NEAR_SHARE}} of the point weight; {{FAMILIES_WIDE_SHARE}} of it lies within
$0.05$. The largest point weight, {{FAMILIES_POINT_MAX}}, sits at
{{FAMILIES_POINT_MAX_SITE}}, within $10^{-5}$ of the line $y=A$ and $0.026$ short of the
corner $(A,A)$ where two of the lines cross.[^census]

The families, as the source tabulates them and the audit recomputed them; each image of
a charge orbit, which the source calls a physical feature, counts as one
charge:[^census]

{{FAMILIES_TABLE}}

<figure>
{{FAMILIES_SVG}}
<figcaption><strong>Figure 6.</strong> The site system. Left: the {{CERT_SITES}} sites
by role: {{FAMILIES_POINT_ONLY}} carry point weight only, {{FAMILIES_SHARED}} point
weight and a $k$-of-$m$ charge, and {{FAMILIES_CHARGE_ONLY}} are in $k$-of-$m$ charges
only; a dot’s area is proportional to its point weight. Middle: the largest 2-of-3
charge, orbit {{FAMILIES_TRIPLE_ORBIT}} of weight {{FAMILIES_TRIPLE_WEIGHT}}, one site of
which lies {{FAMILIES_TRIPLE_CENTRE}} from the container’s center. Right: the largest
2-of-5 charge, orbit {{FAMILIES_PAIR_ORBIT}} of weight {{FAMILIES_PAIR_WEIGHT}}, with two
disjoint cores each holding two of its sites, both paid. The {{CERT_CHARGE_ORBITS}} charge
orbits expand to {{CERT_FEATURES}} $k$-of-$m$ charges in all. Sites and weights are read
from the
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json">retained certificate</a>.</figcaption>
</figure>

## Parents, Cores and the Angle Catalogue

Angles are kept in half-angle coordinates.
For an angle $\theta$, write $t=\tan(\theta/2)$; then

$$
\cos\theta=\frac{1-t^2}{1+t^2},\qquad \sin\theta=\frac{2t}{1+t^2},
$$

so a rational $t$ gives a rational cosine and sine, and every comparison the checkers
make is between rational numbers.
A parent’s angle is written $\varphi$, as Part I writes a packed square’s, and its
half-tangent $\tan(\varphi/2)$ ranges over $[0,1)$ as $\varphi$ ranges over
$[0,\pi/2)$.[^catalogue]

**Folding lemma.** Every parent may be assumed to have angle in $[0,\pi/4]$, one parent
at a time, without assuming anything about the packing.
Part I’s
[contradiction argument]({{PAPER:n11-lower-bounds-explainer#the-contradiction-argument}})
proves this for unit squares: a square whose angle lies past $\pi/4$ is reflected across
the container’s diagonal, which is one of the eight symmetries; the image is a square in
the container with angle in $[0,\pi/4]$; its core is chosen there and reflected back;
and because the certificate is $\mathbf{D}_4$-invariant the reflected core captures a
site exactly when the original captures the site’s image, so its charge is unchanged.
Here the same reflection is applied to a parent, and the core it brings back is a closed
square strictly inside the original parent, because reflection preserves containment.
Two parents may be folded by different symmetries.
The source states this in one sentence.[^folding]

A **row** $(a,b,t,B)$ is a closed interval $[a,b]$ of parent half-tangents together with
a core half-tangent $t\in[0,1)$ and a core side $0<B<A$: every parent with
$\tan(\varphi/2)\in[a,b]$ is assigned the concentric closed core of side $B$ at angle
$2\arctan t$. The **catalogue** is the certificate’s list of {{CATALOGUE_ROWS}} rows,
contiguous from $0$ to ${{CATALOGUE_END}}$. The last endpoint $b$ satisfies
$b^2+2b-1=309449/(2.5\times10^{11})>0$, so it lies past $\tan(\pi/8)=\sqrt2-1$ and the
rows cover every folded angle.
Row widths run from $3.6\times10^{-9}$ to $4.8\times10^{-4}$, and $B$ from
{{CATALOGUE_B_MIN}}
to {{CATALOGUE_B_MAX}}; the two cores of Figure 4 are row {{CHARGE_ROW}}’s.[^catalogue]

The **mismatch** $d$ between a parent and its core is the angle $\varphi-2\arctan t$. A
concentric square of side $B$ at angle $d$ to a square of side $A$ lies strictly inside
it exactly when

$$
B\,(\cos d+|\sin d|)<A,
$$

since $B(\cos d+|\sin d|)$ is the width of the tilted square’s projection on the
parent’s axes. Part I meets the same expression as $B(\cos d+\sin d)<1$ under its
[Condition 4]({{PAPER:n11-lower-bounds-explainer#the-five-conditions-for-a-point-certificate}}).

**Strict-core lemma.** For every row and every parent angle $\varphi$ with
$\tan(\varphi/2)\in[a,b]$, $B(\cos d+|\sin d|)<A$: every assigned core lies strictly
inside its parent. The checker evaluates $\cos d$ and $|\sin d|$ at the two endpoint
angles $2\arctan a$ and $2\arctan b$ as rational dot and cross products of the parent’s
and the core’s direction vectors, and checks three things: that $\cos d>0$ and
$\cos d\ge|\sin d|$ at both endpoints, which puts $d$ in $[-\pi/4,\pi/4]$ there; and
that the inequality holds at both.
The endpoint checks suffice for the whole row.
Since $2\arctan$ is increasing, $d$ is a monotone function of the parent’s half-tangent
and so stays between its endpoint values, in $[-\pi/4,\pi/4]$; and on that range
$\cos d+|\sin d|=\sqrt2\cos(|d|-\pi/4)$ increases with $|d|$, so its maximum over the
row is at an endpoint.
The **margin** $A-B(\cos d+|\sin d|)$ is at least $10^{-12}$ over the whole catalogue.
Independently, the source’s controls and this project’s audit check 48,112 rational
quadratic inequalities, four per row, one for each vertex of the core projected on a
parent axis, minimized over the whole interval including any interior critical point,
and all are strictly positive.[^strict]

The lemma is what lets parents touch.
Two parents with disjoint interiors may share an edge, but their closed cores lie in the
two disjoint interiors, so the cores are disjoint, and the Budget lemma applies to them.

<figure>
{{CORE_SVG}}
<figcaption><strong>Figure 7.</strong> A parent and its assigned core. The parent of side
$A = {{CERT_A}}$ at the row’s upper end angle, the concentric core of side $B$ at the
row’s core angle, and the mismatch $d$ between them, for row 0 and row
{{CATALOGUE_TIGHT_ROW}}, where $\Gamma$ is attained. The mismatch is drawn
{{CORE_EXAGGERATION}} times its true size and the core shrunk to fit: at true scale core
and parent differ by less than a pixel, and the margin is at least $10^{-12}$. The
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/independent_controls.py">source’s controls</a>
and this project’s
<a href="../../src/sqpack/fractional/parent_core.py">parent-core premise check</a>
prove the strict containment over every row.</figcaption>
</figure>

<figure>
{{CATALOGUE_SVG}}
<figcaption><strong>Figure 8.</strong> The catalogue strip: the density of the
{{CATALOGUE_ROWS}} rows over parent angles from 0° to 45°, with widths from
$3.6\times10^{-9}$ to $4.8\times10^{-4}$ in the half-tangent. The three rows whose least
charge is below one are marked: row {{CATALOGUE_TIGHT_ROW}}, at {{CATALOGUE_TIGHT_ANGLES}},
where the least charge is {{CATALOGUE_TIGHT_MIN}}, which is $\Gamma$, and rows
{{CATALOGUE_PAIR_ROWS}}, at {{CATALOGUE_PAIR_ANGLES}}, with least charge
{{CATALOGUE_PAIR_MIN}}. Rows and minima are read from the certificate’s
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json">entries</a>
and the
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/evidence/portable/python.json">Python scan’s per-row record</a>.</figcaption>
</figure>

## Every Legal Center Collects Enough Charge

Fix a row. Its core has a fixed side and angle, so the charge of an assigned core is a
function of its center alone, and the question is where the center can be.

A parent at angle $\varphi$ fits in the container exactly when its center lies in the
**legal center domain**

$$
\bigl[\tfrac{A}{2}(\cos\varphi+\sin\varphi),\;L_0-\tfrac{A}{2}(\cos\varphi+\sin\varphi)\bigr]^2,
$$

because $A(\cos\varphi+\sin\varphi)$ is the width of the parent’s projection on either
axis.[^envelope]

**Envelope lemma.** The union of the legal center domains over a row, the row’s
**envelope**, is the square $[\rho,L_0-\rho]^2$ with **inset**
$\rho=\tfrac{A}{2}\min(\cos\varphi+\sin\varphi)$ taken over the two endpoint angles of
the row. On $[0,\pi/2)$, $\cos\varphi+\sin\varphi=\sqrt2\cos(\varphi-\pi/4)$ has one
stationary point, a maximum at $\varphi=\pi/4$, so it has no interior minimum on any
interval, and its minimum over a row is at one of the two endpoint angles; in the
half-tangent the same derivative has the sign of $1-2\tan(\varphi/2)-\tan^2(\varphi/2)$,
which is how the checkers see it.
The domains are nested squares about the container’s center, so their union is the
largest of them, which is the one with the least inset.
The source scans the whole envelope for the row’s fixed core, so a center that is legal
for some parent angle of the row is checked whether or not it is legal for the others.
The lemma holds past $\tan(\pi/8)$ as well, which the last row needs.[^envelope]

Work in the **core frame**, the coordinates with axes parallel to the core’s edges.
A core of side $B$ captures a site $p$ exactly when its center lies in the closed
axis-aligned square of side $B$ about $p$; call this the site’s **capture rectangle**. A
core captures every site of a set exactly when its center lies in the intersection of
their capture rectangles, which is again a closed axis-aligned rectangle, possibly
degenerate or empty.
So the set of centers at which a $k$-of-$m$ charge pays is a finite union of rectangles,
one for each $k$-subset of its sites, and the charge of a core is a nonnegative sum of
indicators of closed sets.[^signed]

A union is awkward to scan; a signed sum of rectangles is easy.
The source uses an identity that T-025 introduced for the same purpose.

**Signed-expansion lemma.** Let $x_1,\ldots,x_m$ be the capture indicators of the $m$
sites, each $0$ or $1$. Then

$$
\mathbf 1\Bigl[{\textstyle\sum_i x_i}\ge k\Bigr]
=\sum_{j=k}^{m}(-1)^{j-k}\binom{j-1}{k-1}\sum_{|J|=j}\;\prod_{i\in J}x_i,
$$

the inner sum over the $j$-element subsets $J$ of the sites.
Each product is the indicator of the intersection of $j$ capture rectangles, so the
right side is a signed sum of rectangle indicators, and the $k$-of-$m$ charge is $w$
times it.[^signed]

Proof. Let $h$ be the number of captured sites.
A product over $J$ is $1$ exactly when $J$ is a subset of the captured sites, so the
inner sum is the number of $j$-subsets of an $h$-set, and the right side is

$$
S(h)=\sum_{j=k}^{h}(-1)^{j-k}\binom{j-1}{k-1}\binom{h}{j},
$$

which is $0$ for $h<k$, as the left side is.
For $h\ge k$ take the first difference $S(h)-S(h-1)$. Pascal’s identity
$\binom hj-\binom{h-1}j=\binom{h-1}{j-1}$ gives

$$
S(h)-S(h-1)=\sum_{j=k}^{h}(-1)^{j-k}\binom{j-1}{k-1}\binom{h-1}{j-1}.
$$

The two binomial coefficients combine.
Writing both as factorials,

$$
\binom{j-1}{k-1}\binom{h-1}{j-1}
=\frac{(h-1)!}{(k-1)!\,(j-k)!\,(h-j)!}
=\binom{h-1}{k-1}\binom{h-k}{j-k},
$$

which is the step the source’s proof leaves out.
Substituting and setting $i=j-k$,

$$
S(h)-S(h-1)=\binom{h-1}{k-1}\sum_{i=0}^{h-k}(-1)^i\binom{h-k}{i},
$$

and the alternating sum is $(1-1)^{h-k}$: it is $1$ when $h=k$ and $0$ when $h>k$. So
$S(k)=S(k-1)+1=1$ and $S(h)=S(h-1)=1$ for every $h>k$, which is the left side.

Appendix B tabulates the coefficients of the three families.
This project’s threshold code proves the same identity for its own checker.[^signed]

<figure>
{{SIGNED_SVG}}
<figcaption><strong>Figure 9.</strong> The signed expansion of one real 2-of-3 charge,
orbit {{SIGNED_ORBIT}}, in the core frame of row {{CATALOGUE_TIGHT_ROW}}, where $\Gamma$
is attained: the three capture rectangles of its sites, the three pairwise intersections
with coefficient $+1$ each, and the triple intersection with coefficient $-2$. Wherever
no rectangle edge is crossed, the signed sum is $0$ or $1$. The rectangles were rebuilt
exactly as the
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py">source’s geometry</a>
builds them.</figcaption>
</figure>

The **exact sweep**. Clear denominators so that every rectangle edge and every vertex of
the envelope, which is a square turned by the core’s angle in the core frame, has
integer coordinates, and drop the rectangles of zero area, the degenerate intersections.
The vertical lines through the remaining coordinates are the **event lines**; they cut
the frame into vertical **slabs**, and the horizontal lines cut each slab into
**y-cells**, which are Part I’s event cells.
On an open y-cell no retained rectangle edge is crossed, so the sweep’s signed sum is
constant there; a center in an open y-cell that lies on no dropped rectangle is a
**generic center**, and at a generic center the signed sum is the charge.
The sweep walks the slabs from left to right.
Entering a slab, it adds each rectangle that begins there and removes each that ends, as
a range addition of its signed weight over its range of y-cells; a lazy segment tree
holds the running sum per y-cell and answers the least value over any range of y-cells.
Within a slab the envelope’s boundary is linear, so its vertical extent is known from
the two edge values at the slab’s ends, and the sweep queries the least charge over
exactly the open y-cells that meet the envelope, and takes the least over all slabs and
rows. All weights are integers in units of $10^{-9}$, and the sum of the absolute
expanded weights over the whole certificate is {{SIGNED_EXPANSION_WEIGHT}}, below
$2^{50}$, so no partial sum can leave the range of a signed 64-bit integer in Python or
of an exactly represented integer in JavaScript.
The Python scan has 86,299,918 slabs and certifies 511,649,694,680 open y-cells; the
y-cells are counted by the range queries, never enumerated one by one.[^sweep]

The range query is exact, though the source says so only in code.
The envelope’s vertical extent at a slab’s end is a rational number, the ratio of two
integers from the edge equation, while the y-cell boundaries are integers.
The query asks for the open y-cells whose lower edge is below the extent’s upper end and
whose upper edge is above its lower end.
Comparing an integer with a rational is the same as comparing it with the rational’s
floor or ceiling, so the first y-cell is found by a binary search for the floor of the
lower end and the last by one for the ceiling of the upper end, and the range is exactly
the open y-cells that meet the envelope on that slab.
This project’s audit rebuilt the envelope as a polygon and clipped it on all 34,909
slabs of five rows, including row 11962, where $\Gamma$ is attained, and found the same
ranges and the same minimum.[^floor]

The sweep sees only generic centers, and the signed sum is only a formula for the charge
there. Two things remain: centers on event lines or on dropped zero-area rectangles,
where rectangles touch, and centers on the envelope’s boundary.

**Boundary lemma.** If the charge is at least $\Gamma$ at every generic center of the
envelope, it is at least $\Gamma$ at every center of the closed envelope.
The unexpanded charge is a nonnegative sum of indicators of closed sets, the capture
rectangles and their finite intersections and unions, and such a sum is **upper
semicontinuous**: at a limit of centers it is at least the limit of the values, because
a closed set contains the limit of any sequence of its points.
Every center of the closed envelope is a limit of generic centers, since the envelope
has positive area and the event lines and dropped rectangles are finitely many.
So the charge at any center is at least the limit superior of the charges at generic
centers approaching it, which is at least $\Gamma$. Dropping zero-area rectangles from
the sweep is harmless for the same reason: they change the signed sum only on
themselves, sets of zero area, so generic centers stay dense and the lemma, not the sum,
gives the bound there.[^boundary]

The source backs this with controls: 5,586 exact centers on event lines and envelope
boundaries of 14 rows, charged by direct membership rather than by rectangles, all at
least $1.000047518$. None of the 14 is one of the three rows whose minimum is below one
(8844, 8845 and 11962).[^boundary]

<figure>
{{ENVELOPE_SVG}}
<figcaption><strong>Figure 10.</strong> The envelope of row {{CATALOGUE_TIGHT_ROW}}, where
$\Gamma$ is attained, in the core frame: the union of the row’s legal center domains is
the square of inset $\rho = {{ENVELOPE_RHO}}$ and half-side $L_0/2 - \rho = {{ENVELOPE_HALF}}$,
turned by the core’s angle. Inset: the charge along the core’s first axis through the
row’s minimizer; at each jump the closed core takes the larger of the two neighboring
values, which is upper semicontinuity. The envelope is read from the row’s
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json">entry</a>
by the
<a href="../../src/sqpack/fractional/parent_core.py">parent-core premise check</a>.</figcaption>
</figure>

<figure>
{{FIELD_SVG}}
<figcaption><strong>Figure 11.</strong> The charge field of row {{FIELD_ROW}}, where
$\Gamma$ is attained: the charge of the assigned core as a function of its center over
the envelope, evaluated directly from the certificate on a {{FIELD_GRID}}-by-{{FIELD_GRID}}
grid, and the exact minimizer at {{FIELD_WITNESS}} from T-059’s
<a href="../../resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full.jsonl.gz">replayed journal</a>,
where the charge is exactly $\Gamma={{FIELD_MIN}}$.</figcaption>
</figure>

## The Contradiction and the Strict Bound

Suppose eleven unit squares fit in a container of side $31/8$. By the Scaling lemma,
eleven parents of side $A$ fit in $[0,L_0]^2$. Fold each parent separately into
$[0,\pi/4]$ (Folding lemma); its half-tangent lies in exactly one row, or on the shared
endpoint of two, and either row’s assigned core is a closed square strictly inside the
parent (Strict-core lemma), with its center in the row’s envelope (Envelope lemma).
The sweep and the Boundary lemma give every such core a charge of at least $\Gamma$;
they are pairwise disjoint, and the Budget lemma caps their total charge at $M$. Then
$11\Gamma\le M$, against $11\Gamma>M$. So no eleven parents fit, and no eleven unit
squares fit in side $31/8$.[^conclusion]

That excludes side $31/8$ exactly; the strict bound needs attainment.

**Attainment lemma.** Among the containers that admit a packing of eleven unit squares
there is a smallest, so $s(11)$ is a minimum and not only an infimum.
Eleven of the sixteen cells of a 4-by-4 grid hold eleven unit squares in a container of
side $4$, so a packing exists at side $4$ and $s(11)\le4$. A packing in a container of
side at most $4$ is described by its side and the eleven centers and angles; each center
lies in $[0,4]^2$, each angle in $[0,\pi/2]$, where both endpoints describe the same
square, and the side in $[0,4]$, so the descriptions form a bounded closed set of
$\mathbb R^{34}$, which is compact.
Containment is a closed condition, since every vertex is a continuous function of the
description and lies in a closed square.
Disjoint interiors is also closed: two squares whose interiors meet have a common
interior point with a neighborhood inside both, which persists under every small enough
change of the description, so the set of descriptions with overlapping interiors is open
and its complement is closed.
The feasible descriptions therefore form a compact set, the side is continuous on it,
and it attains its minimum.[^conclusion]

A packing exists at side $s(11)$, and none exists at side $31/8$, so $s(11)\ne31/8$; and
since any packing at a side below $31/8$ would also fit in side $31/8$, $s(11)>31/8$.
Part I states its bounds with $\ge$ because that is what its verifier’s theorem states,
and remarks that compactness gives the strict form; here the source states the strict
form and the lemma above is its proof.[^statement]

## What Was Verified, and What the Verification Means

The source supplies two checkers, a Python scanner (`exact_mixed.py` with
`integer_sweep.py`) and a JavaScript scanner reconstructed from R038’s, with independent
controls in standard-library rational arithmetic; this project replayed both in full,
audited the premises with its own instrument, and decided the coverage a second time by
a different method.[^audit][^native]

| Mathematical obligation | Human argument | Source checkers | This project |
| --- | --- | --- | --- |
| $k$-of-$m$ budgets add to $M$; the identity of the signed expansion | Budget and Signed-expansion lemmas | Exhaustive identity and disjoint-assignment checks for three and five sites | Independent orbit, budget and headroom reconstruction |
| $\mathbf{D}_4$ invariance of every charge | Folding lemma | Every orbit expanded and compared in both scanners | Weighted $\mathbf{D}_4$ check of the native premise validator |
| The catalogue covers $[0,\pi/4]$ | Folding lemma | Contiguity and $b^2+2b>1$ at the end | The same, independently |
| Every assigned core is strictly inside its parent | Strict-core lemma | Endpoint checks in the scanners; 48,112 quadratic inequalities in the controls | 48,112 inequalities minimized over whole intervals, with interior critical points |
| The envelope is the union of the legal domains | Envelope lemma | Envelope inequality per row | The same, with positive area |
| Every generic center of every row has charge at least $\Gamma$ | — | Two complete exact sweeps, identical histograms | Interval branch and bound certifying a lower bound of at least $\Gamma$ on every row; segment tree against a direct array and polygon clipping on five rows |
| Boundaries | Boundary lemma | 5,586 direct boundary centers on 14 rows | — |
| $11\Gamma>M$ and the scaling to $31/8$ | Scaling lemma | Exact comparison in the launcher | Exact comparison in the native receipt |
| The bound is strict | Attainment lemma | — | Reviewed in both 2026-09-22 reviews |

$\Gamma$ is computational only: no human-readable argument explains why every assigned
core of every row collects at least $0.99996$, and the value is known because two
complete sweeps computed it and a third method bounded it from below.[^statement]

The register counts the two source checkers as one method, an exact event-cell sweep
with signed rectangle terms, in two code lineages, the Python generalizing Kleddamag’s
seventeen-square checker and the JavaScript adapting R038’s: the Python geometry uses
polygon edges and the JavaScript geometry clamped extrema, and the two partition the
frame differently, 86,299,918 slabs against 86,275,862, exactly two fewer per row, yet
return identical per-row minima.[^register] The method-distinct decision is this
project’s native verifier, an interval branch and bound over boxes of centers that
counts captured sites with directed rounding, never forms the signed expansion, and
refuses any box it cannot resolve; it certified all 12,028 rows with 136,081,500 boxes,
none stalled, and a least certified lower bound of exactly
$\Gamma={{MINIMA_NATIVE_MIN}}$.[^native] T-059 is a computation of another kind:
wand125’s checker reproduces all 12,028 exact row minima with replayed witnesses, which
audits the source’s row-scan claim and is not a new proof of the bound.[^t059]

The JavaScript source is not in the archive: no code license was identified for the
pinned R038 file, so `prepare_secondary.py` reconstructs the checker from hash-pinned
upstream bytes and published edits, and verifies both hashes.[^credit]

The register records the result as T-037, S5/V3/C3: significance 5, movement on a
central open case; verification 3, machine-checked here; confirmation 3, decided by two
methods, the source’s sweeps and the native branch and bound, with the review record
pending. It held V4/C4 under the [ladder](../../../epistemics.md) in force until
2026-09-30, whose fourth levels now also need two adversarial reviews by distinct
reviewers and a human oversight record.
Whether a same-project review of another author’s certificate counts toward confirmation
is not yet decided.[^register]

<figure>
{{MINIMA_SVG}}
<figcaption><strong>Figure 12.</strong> The least charge of every row against its parent
angle, from the Python scan, with $\Gamma$ marked; {{MINIMA_TOP_ROWS}} of the
{{CERT_ROWS}} rows share the value {{MINIMA_TOP}}, and the row minima take
{{MINIMA_VALUES}} distinct values. The band is the native verifier’s certified lower
bound per row, at least $\Gamma$ and at most the exact minimum;
{{MINIMA_NATIVE_BELOW_ONE}} of its bounds are below one and {{MINIMA_NATIVE_EQUAL}} equal
the Python minimum. Read from the
<a href="../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/evidence/portable/python.json">Python scan</a>
and the
<a href="../../campaign/agent-sessions/session-153-native-full.rows.jsonl">native row journal</a>.</figcaption>
</figure>

## How Part III’s Certificates Relate to This One

Four facts connect this certificate to those of
[Part III]({{PAPER:n11-optimality-review}}). First, when $2k>m$ a core that captures $k$
of $m$ sites holds more than half of them, so in every direction its projection contains
the median of the projected sites: it receives Part III’s
[median-type charge]({{PAPER:n11-optimality-review#charge-budgets-exclude-many-patterns-at-once}})
on the same sites, whose budget is also $w$, and that charge pays every core the
$k$-of-$m$ charge pays.
The 2-of-3 and 3-of-5 charges are such cases; the 2-of-5 charge, with budget $2w$, has
no counterpart there.
Second, this paper’s $\Gamma$ and $M$ play the roles of Part III’s per-cell floors
$\Gamma_i$ and budget $b$. Third, this paper folds every angle into $[0,\pi/4]$ because
its certificate has the whole $\mathbf{D}_4$ symmetry; Part III works on $[0,\pi/2]$
because its cover of the centers has only the half-turn symmetry.
Fourth, Part III’s rows are also closed intervals of the half-tangent, but each carries
a polygon of allowed centers rather than a core.

## Appendix A: Certificate Schema

The retained file `global-certificate.json`, whose digest the release’s manifest and the
register’s evidence entry record, has ten fields: `L` and `A`, the container and parent
sides as rational strings; `coordinate_denominator` ($10^{10}$) and `weight_denominator`
($10^9$); `point_orbits`, a list of 679 triples $(x,y,w)$ of integers, one site per
orbit with its point weight, 613 of them zero; `charge_orbits`, a list of 284 objects
each with a `threshold`, an integer `weight` and `sets`, the index lists of the whole
orbit of one $k$-of-$m$ charge, eight or fewer; `entries`, the 12,028 rows $(a,b,t,B)$
as rational strings; and `minimum_units`, `budget_units` and `bound`. This project reads
it with [`load_kleddamag_parent_core`](../../src/sqpack/fractional/parent_core.py),
which refuses duplicate keys, inexact numbers, a container other than $191/50$, and a
declared budget that the charges do not sum to.
The family census is the table in
[The Certificate’s Charges](#the-certificates-charges); in the file’s units every budget
there is an integer count of $10^{-9}$.[^census]

## Appendix B: Coefficient Tables

The coefficient of the $j$-subsets in the signed expansion of a $k$-of-$m$ charge is
$(-1)^{j-k}\binom{j-1}{k-1}$, and the absolute coefficient sum is
$\sum_j\binom mj\binom{j-1}{k-1}$, which is {{SIGNED_ABS_SUMS}} for the three families
the certificate uses:

| Family | Pairs | Triples | Quadruples | Quintuple | Budget |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2-of-3 | $+1$ (3) | $-2$ (1) |  |  | $w$ |
| 2-of-5 | $+1$ (10) | $-2$ (10) | $+3$ (5) | $-4$ (1) | $2w$ |
| 3-of-5 |  | $+1$ (10) | $-3$ (5) | $+6$ (1) | $w$ |

The count of subsets of each size is in parentheses.
The source checks the identity exhaustively on every pattern of captured sites for three
and five sites and every threshold; its record also lists the other thresholds, 1-of-3
(sum 7), 3-of-3 (1), 1-of-5 (31), 4-of-5 (9) and 5-of-5 (1), none of which the
certificate uses.[^signed]

## Appendix C: Reproduction

The source’s README gives the commands: with Python 3.12 and Node.js, check out tag
`v1.0.2`, install `requirements.txt`, run `check_integrity.py`, then
`verify.py --output-dir <fresh directory>`, and finally `verify_threshold_algebra.py`. A
complete run reports `PASS_FRESH_PORTABLE_FULL_VERIFICATION`, bound $31/8$, 12,028
intervals and a counting surplus of $107{,}864$ units.
The two scans took about 9.5 minutes (Python) and 7.6 minutes (JavaScript) on the
source’s machine, and 1,501 and 1,790 seconds in this project’s replay under concurrent
load; the native decision took 6,197 seconds with two workers.
The first run downloads one commit-pinned R038 source file and checks its hash; run with
assertions enabled, since the entry points refuse `-O`. `verify_threshold_algebra.py`
rewrites the committed `threshold-algebra.json` beside it, so run it in a copy, not in
the archive.[^audit]

Evidence files, all retained: the source’s `evidence/portable/` directory (the launcher
`RESULT.json`, the Python scan’s per-row `python.json`, the JavaScript ranges under
`secondary/`, and `controls.json`); this project’s
[full-replay receipt](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/full-replay/RESULT.json)
and
[independent audit](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/independent-audit.json);
the [native receipt](../../campaign/agent-sessions/session-153-native-full.json) with
its [row journal](../../campaign/agent-sessions/session-153-native-full.rows.jsonl) and
[reconciliation](../../campaign/agent-sessions/session-153-native-reconciliation.json);
and T-059’s
[row-minimum summary](../../resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full-summary.json).
The native verifier is `python -m devtools.verify_kleddamag_n11_native --all`, and the
receipt reconciliation is `python -m devtools.audit_kleddamag_n11_native`, both from
`packing/` in the project environment.[^native]

## Appendix D: Series Glossary

The terms the three papers share, with the paper that derives each in full.

| Term | Owner | Meaning |
| --- | --- | --- |
| $s(n)$ | I | The least side of a square holding $n$ unit squares with disjoint interiors |
| Container side $L_0$ | I | The side under test in a certificate |
| Core | I | A smaller closed square strictly inside a packed square, or here a parent |
| Site | II | A position in the container |
| Point charge (I: atom) | I | A site with a nonnegative weight, paid to any core containing it |
| $k$-of-$m$ charge (I: threshold atom) | I, II | Pays $w$ to a core capturing at least $k$ of its $m$ sites; budget $w\lfloor m/k\rfloor$ |
| Charge $C(Q)$ | II | The total a core receives from point and $k$-of-$m$ charges |
| Budget, $M$ | I, II | The most the charges can pay across pairwise disjoint cores; $M$ is its total |
| $\Gamma$ | II | The certified minimum charge of an assigned core |
| Mass $\mu$ | I | The point-only charge of a region |
| Event cell | I | A region of centers on which the captured set is constant |
| Net; half-tangent | I | Finitely many directions; the parameter $t=\tan(\theta/2)$ of an angle $\theta$ |
| Parent | II | A side-$A$ square in $[0,L_0]^2$; parents in $L_0$ stand for unit squares in $L_0/A$ |
| Row | II | A closed interval of parent half-tangents with its assigned core $(t,B)$ |
| Envelope | II | The union of legal center domains over a row |
| Signed expansion | II | The rectangle-sum form of a $k$-of-$m$ indicator |
| Upper semicontinuity | II | The property that extends $\Gamma$ from generic centers to boundaries |
| Cap $U$, cell, mask, case | III | A rational side above $T$; a Voronoi region of the center cover; an 11-subset of cells; a half-turn class of masks |
| Field certificate, capacity | III | A charge certificate on occupied cells; the most disjoint cores one charge pays |
| Receipt | III | A checked execution’s verdict, input hashes, command and replay script |

## Sources and Verification Record

The [mathematical audit][audit] of 2026-09-22 read the proof, both checkers, the
controls and the attribution files, and found no blocking defect; the
[native parent-core review][native] records the method-distinct decision and its
receipt.
The archived source tree is immutable upstream material; the receipts cited here
are repository-generated.
The figures are explanatory renderings of retained data, drawn from hash-pinned files,
and their rounded coordinates are not inputs to any check.
Every number in this paper is read from the archived source, the register or the
retained receipts, and the renderer refuses a caption value the figure modules do not
supply.

## Version History

{{VERSION_HISTORY}}

[^authors]: [`AUTHORS.md`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/AUTHORS.md#L3-L8),
    which says Kleddamag commissioned and directed the research and OpenAI Codex
    developed the mathematical and computational continuation; the
    [attribution’s lead](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/ATTRIBUTION.md#L3-L7),
    which names this project’s T-026 certificate at its revision.

[^statement]: [Original proof, statement and scope](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L3-L7),
    [conclusion](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L79-L85)
    and the
    [verified summary](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/VERIFIED.json);
    the [T-037 record](../../frontier/results.yaml) holds the claim as stated here.
    Part I’s remark on compactness is in its
    [contradiction argument]({{PAPER:n11-lower-bounds-explainer#the-contradiction-argument}}).

[^register]: [Result register](../../frontier/results.yaml): T-037’s claim, significance
    and notes, including the supersession by T-061 and T-060; T-038 and T-039 for the
    seventeen-square antecedents; T-025’s significance rationale for the ceiling family;
    T-059 for the row-minimum audit.
    The [case record](../../frontier/n-011.md) gives the bound history, and
    [`epistemics.md`](../../../epistemics.md) the rungs.

[^credit]: [`ATTRIBUTION.md`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/ATTRIBUTION.md#L13-L22):
    the certificate developed from T-026 (line 13), the Python checker generalized from
    the seventeen-square checker and the JavaScript checker adapted from R038 (lines
    14–15), and the statement that no independent invention of the weighted-covering or
    threshold-counting methods is claimed (lines 18–22); the
    [source identity section](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/ATTRIBUTION.md#L24-L38)
    on the reconstructed JavaScript.
    Part I’s
    [threshold atom]({{PAPER:n11-lower-bounds-explainer#proof-of-the-new-lower-bound}});
    the
    [T-025 proof](../../cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md)
    and its
    [theorem review](../../../docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md),
    whose finding F6 is the signed expansion and its integer difference array;
    [`threshold.py`](../../src/sqpack/fractional/threshold.py), which names 2-of-5 and
    3-of-5; the
    [five-site study of 2026-09-10](../../../docs/project/reviews/review-2026-09-10-n11-weighted-five-site-atoms.md),
    which produced no certificate.

[^lineage]: [`NOTICES/Mira-ATTRIBUTION.md`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/NOTICES/Mira-ATTRIBUTION.md#L29-L45):
    adaptive interval refinement, maximal safe rational cores and certified parent
    envelopes as Mira’s additions in the 4.614153 continuation, by Mira’s own
    attribution (lines 29–32); weighted covering, exact event-cell verification,
    strict-core transport and the parent-center restriction as prior work in this
    project, with the
    [unit-parent center note](../../cases/n11_five_dot_cover/unit-parent-centre-contract.md)
    as the analytic antecedent (lines 40–45);
    [`NOTICES/Guzhou-NOTICE.md`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/NOTICES/Guzhou-NOTICE.md#L9),
    where R038 states that it adds the smaller rational parent side and the
    strict-containment transfer; the [T-032 record](../../frontier/results.yaml) for
    R012, the first registered certificate with parents, a catalogue of parent-angle
    intervals, one core per interval and coverage over the legal parent-center square.

[^audit]: [Mathematical review of 2026-09-22](../../../docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md):
    Integration Finding 4 on the ingredients changed together and the absent ablation;
    the polygon-clipping control on five rows, row 11962 among them; the replay times;
    and the note that the archive must not acquire generated files.
    Its instrument is [`audit_kleddamag_n11.py`](../audit_kleddamag_n11.py) and its
    receipt the
    [independent audit](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/independent-audit.json).
    The controls’ scope is in the
    [portable controls record](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/evidence/portable/controls.json).

[^paper-one]: Part I’s
    [atoms, mass and budget]({{PAPER:n11-lower-bounds-explainer#atoms-mass-and-the-budget}})
    and [core]({{PAPER:n11-lower-bounds-explainer#proof-of-the-new-lower-bound}}), which
    this paragraph recaps; Part I derives them in full.

[^charges]: [Original proof, charges and their budgets](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L31-L39);
    the budget computation in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L26-L47)
    and the exhaustive disjoint-assignment check in
    [`verify_threshold_algebra.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/verify_threshold_algebra.py)
    with its
    [record](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/threshold-algebra.json);
    this project’s [`threshold.py`](../../src/sqpack/fractional/threshold.py) states the
    same budget.

[^threshold-code]: [`threshold.py`](../../src/sqpack/fractional/threshold.py), whose
    docstring notes that when $k$ divides the token count the threshold inequality is
    implied by the point inequalities, so the atoms that add anything are 2-of-3,
    3-of-4, 2-of-5, 3-of-5 and their kin.

[^parents]: [Original proof, parents](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L29)
    and
    [scaling](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L83);
    the sides are checked by the launcher and, separately, by
    [`parent_core.py`](../../src/sqpack/fractional/parent_core.py), which records
    $L_0=191/50$, $A=764/775$ and $L_0/A=31/8$ in the
    [native receipt](../../campaign/agent-sessions/session-153-native-full.json).

[^conclusion]: [Original proof, conclusion](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L79-L85):
    the counting at lines 81–83 and the compactness argument at line 83; the
    [full-replay receipt](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/full-replay/RESULT.json)
    records the exact $\Gamma$, $M$ and surplus; the
    [native review](../../../docs/project/reviews/review-2026-09-22-native-n11-parent-core.md)
    states the attainment argument in its proof contract.

[^census]: [Original proof, the certificate](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L7-L14),
    with the family table; the orbit expansion and invariance check in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L16-L41);
    the
    [independent audit](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/independent-audit.json),
    which reconstructs every orbit, feature count and family budget; the site roles,
    wall-line concentration and largest weights were computed from the
    [retained certificate](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json)
    through [`load_kleddamag_parent_core`](../../src/sqpack/fractional/parent_core.py),
    outside any accepted check.

[^catalogue]: [Original proof, transport](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L41-L43);
    the catalogue check in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L91-L102);
    the row count, the last endpoint and the angle surplus in the
    [independent audit](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/independent-audit.json)
    and the
    [native receipt](../../campaign/agent-sessions/session-153-native-full.json).
    Row widths and the range of $B$ were read from the certificate’s `entries`.

[^folding]: [Original proof, line 43](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L43),
    one sentence; the invariance it rests on is checked in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L16-L41)
    and in the native premise validator of
    [`parent_core.py`](../../src/sqpack/fractional/parent_core.py); Part I proves the
    point case in its
    [contradiction argument]({{PAPER:n11-lower-bounds-explainer#the-contradiction-argument}}).

[^strict]: [Original proof, the relative width and its endpoint maximum](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L45-L49);
    the endpoint dot and cross checks in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L96-L100);
    the 48,112 quadratic inequalities in the
    [source’s controls](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/independent_controls.py)
    with their
    [record](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/evidence/portable/controls.json),
    and in this project’s
    [independent audit](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/independent-audit.json)
    and [`parent_core.py`](../../src/sqpack/fractional/parent_core.py), which minimize
    each quadratic over the whole interval.

[^envelope]: [Original proof, line 51](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L51);
    the envelope check in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L99-L100);
    the derivative argument in the
    [native review](../../../docs/project/reviews/review-2026-09-22-native-n11-parent-core.md)
    and in [`parent_core.py`](../../src/sqpack/fractional/parent_core.py), whose
    docstring carries it, and the 12,028 envelope inequalities in the
    [independent audit](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/independent-audit.json).

[^signed]: [Original proof, the exact finite sweep](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L53-L65):
    the identity at line 57 and its proof at lines 59–63, which omit the binomial
    identity written out above; the exhaustive check
    [`verify_threshold_algebra.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/verify_threshold_algebra.py)
    and its
    [record](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/threshold-algebra.json),
    which holds the absolute coefficient sums; the coefficients in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L43-L47);
    the same identity in this project’s
    [`threshold.py`](../../src/sqpack/fractional/threshold.py) and the
    [theorem review’s](../../../docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md)
    finding F6.

[^sweep]: [Original proof, lines 67–71](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L67-L71);
    the segment tree in
    [`integer_sweep.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/integer_sweep.py#L8-L38)
    and the geometry in
    [`exact_mixed.py`](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L50-L89);
    the headroom check at
    [line 47](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L47)
    and the reconstructed absolute weight in the
    [independent audit](../../resources/web/external-square-certificates-2026-09-22/receipts/n11/independent-audit.json);
    the slab and cell totals in the
    [Python scan record](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/evidence/portable/python.json).

[^floor]: [`exact_mixed.py`, line 85](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py#L85),
    the two binary searches; the
    [mathematical review](../../../docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md)
    states the equivalence of the comparisons and records the polygon-clipping control
    on all 34,909 slabs of rows 0, 1, 6014, 11962 and 12027.

[^boundary]: [Original proof, boundaries](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/PROOF.md#L73-L77);
    the direct boundary and event centers in the
    [source’s controls](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/independent_controls.py)
    and their
    [record](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/evidence/portable/controls.json),
    14 rows and 5,586 centers with least charge $1.000047518$; the
    [mathematical review](../../../docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md)
    on why a positivity argument on the signed form would be invalid and the source does
    not make one.

[^native]: [Native parent-core review](../../../docs/project/reviews/review-2026-09-22-native-n11-parent-core.md);
    the verifier [`verify_kleddamag_n11_native.py`](../verify_kleddamag_n11_native.py),
    the [complete receipt](../../campaign/agent-sessions/session-153-native-full.json),
    the [row journal](../../campaign/agent-sessions/session-153-native-full.rows.jsonl)
    and the [reconciliation tool](../audit_kleddamag_n11_native.py) with its
    [record](../../campaign/agent-sessions/session-153-native-reconciliation.json).
    The band counts of Figure 12 were computed from the row journal against the Python
    scan record.

[^t059]: [T-059 record](../../frontier/results.yaml);
    [wand125’s tools](../../resources/web/wand125-tools-2026-09-29/README.md) and the
    [row-minimum summary](../../resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full-summary.json),
    whose verdict is `COMPLETE_ROW_EQUALITY` with 12,028 exact witness replays and whose
    scope is per-row minimum equality only; the
    [tools review](../../../docs/project/reviews/review-2026-09-29-wand125-tools-mathematics.md).

[audit]: ../../../docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md
[native]: ../../../docs/project/reviews/review-2026-09-22-native-n11-parent-core.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
