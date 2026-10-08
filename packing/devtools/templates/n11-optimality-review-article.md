{{FRONT_MATTER}}

This paper explains the computer-assisted optimality proof published by
[Queuingtheorydotcom in 11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal).
The original
[mathematical argument](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md),
[verification driver](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/VERIFY.py),
[certificate data](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/data),
and
[reproduction instructions](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/REPRODUCING.md)
are pinned to the source revision reviewed here.
[Queuingtheorydotcom’s announcement](https://x.com/MathCompSciFTW/status/2104772485816168618)
credits Astra’s work building on the Squares Project and Kleddamag.

The components have distinct provenance:

- **Attaining construction:** Walter Trump’s packing, with
  [David Ellsworth’s reconstruction and exact formulas](https://kingbird.myphotos.cc/packing/square-11.svg),
  retained in the
  [construction source record](../../resources/papers/kingbird-square-11-provenance.svg).
- **Mathematical antecedents:** the Squares Project’s
  [threshold-certificate method](../../cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md),
  which [Part I of this series]({{PAPER:n11-lower-bounds-explainer}}) explains, and its
  [local-isolation theorem](../../cases/trump11/isolation-theorem.md), together with
  [Kleddamag’s earlier proof](https://github.com/Kleddamag/11-squares-certified-bound)
  of a lower bound of 31/8
  ([retained source](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/README.md)),
  which [Part II]({{PAPER:n11-threshold-bound-review}}) explains.
  The original proof’s
  [third-party notices](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/THIRD_PARTY_NOTICES.md)
  identify its incorporated Squares Project revision.
- **Verification and exposition here:** the Squares Project’s
  [T-060 result record](../../frontier/RESULTS.md),
  [retained proof and verification packet](../../resources/web/n11-optimality-2026-09-29/README.md),
  and
  [mathematical acceptance review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance)
  document the confirmation explained in this paper.[^credit]

For a technical review, start with the
[T-060 validation guide](../../resources/web/n11-optimality-2026-09-29/VALIDATION.md).
It links the published proof, certificate inputs, independent checks, and accepted
evidence for each obligation.
The guide distinguishes checking retained evidence from a fresh geometric replay and
states the remaining work needed for a standalone executable package.

## The Result

Place eleven unit squares inside a larger square.
Each small square may rotate independently.
Their edges may touch, but their interiors may not overlap.
How small can the container be?
Write $s(11)$ for the smallest such side and $L_0$ for the side of a container under
test, as [Part I]({{PAPER:n11-lower-bounds-explainer#the-square-packing-problem}}) does;
the theorem below shows that a smallest side exists.

The answer is the side length of Trump’s construction in Figure 1:

$$
s(11)=T=3.8770835900228141773078970601\ldots.
$$

$T$ is an algebraic number of degree eight.
Let $u$ be the unique positive real root of

$$
p(u)=5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0;
$$

it lies in $(9/25,37/100)$, and the proof’s exact arithmetic uses that interval to tell
it apart from the polynomial’s other roots.
Then

$$
T=\frac{6u+4}{1+2u-u^2}.
$$

The polynomial is a contact condition between two of the eleven squares; the
construction section says which.

**Theorem.** Eleven unit squares with arbitrary independent rotations and pairwise
disjoint interiors fit in a square of side $T$, and do not fit in any square of side
$L_0<T$. The smallest side is therefore attained, and $s(11)=T$.[^proof]

The evidence behind the lower bound is a set of component computations, each observed
and reviewed separately.
Each accepted execution is retained as a **receipt**: its verdict, a hash of every input
object and of the checker’s own bytes, the command and commit that produced it, and a
replay script. A program called the composer reads a fixed set of receipts by hash and
checks the joins between them without rerunning the geometry; no single fresh run of the
whole proof has yet been made.
The closing section states that scope exactly.

<figure>
<div class="stage trump"><a href="../../atlas/rendering/trump11-overview.svg" aria-label="The rendering in the repository">{{WITNESS_SVG}}</a></div>
<figcaption><strong>Figure 1.</strong> The attaining construction: six squares are
axis-aligned and five share a tilted orientation. The drawing is rounded for display;
the <a href="../../cases/trump11/verify_exact.py">exact witness check</a> uses algebraic coordinates.
Touching edges and corners are legal.
The construction reaches both opposite walls in each coordinate direction.</figcaption>
</figure>

An upper bound needs one example: the packing drawn above.
A lower bound must exclude every arrangement in a smaller container, including
unfamiliar contact patterns and eleven independently chosen angles.
Numerical search can suggest a good packing, but failing to find a better one does not
exhaust those possibilities.

Suppose a packing fits in a smaller square, of side $L_0<T$. The proof must handle that
packing without knowing any of its positions or angles.
It first classifies the centers and uses exact certificates to eliminate impossible
classes. Every survivor, after a symmetry of the container, enters a capture argument
that encloses its positions and angles near the known construction.

The last step connects this global restriction to a local theorem.
The same smaller packing can be placed inside the exact side-$T$ container, within a
checked neighborhood where only the construction is feasible.
But the construction spans $T$, so it cannot fit inside the smaller container.
Figure 2 shows both halves of the proof.

<figure>
{{ROADMAP_SVG}}
<figcaption><strong>Figure 2.</strong> Two routes to the exact optimum. The construction
supplies an upper bound. The lower-bound route follows an arbitrary hypothetical
smaller packing through restrictions that preserve every feasible possibility, ending
in a contradiction. The counts of center patterns classify continuous families of
positions and angles; they do not count individual packings. The
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/final-composition.json">accepted composition</a>
checks the joins between these obligations.</figcaption>
</figure>

The geometric steps are
[center classification](#sixteen-regions-cover-all-possible-centers),
[safe exclusions](#one-geometric-invariant-supports-the-certificates),
[symmetry](#symmetry-reduces-the-four-survivors-to-one), and
[capture](#capture-forces-case-438-near-the-construction).
The [local estimate](#the-local-argument-excludes-every-nonzero-motion) and
[exact frame change](#closing-the-gap-between-the-rational-cap-and-the-exact-optimum)
complete the contradiction.

## From Weighted Points to a Global Proof

[Part I][earlier] of this series develops the lower-bound method from weighted points.
Select a small **core** strictly inside each packed square; the **charge** a core
receives is the weight it collects.
If every possible core must receive a charge of at least one, eleven disjoint cores must
receive at least eleven units.
A certificate with less than eleven units available proves a contradiction.
Exact coverage checks turn that idea into a theorem about every position and
orientation. Part I explains the point certificate T-018, the threshold certificate
T-025, whose $k$-of-$m$ charges pay a core holding at least $k$ of its $m$ charge sites,
and T-026’s dilation bound $s(11)\ge3.8264474\ldots$.
[Part II]({{PAPER:n11-threshold-bound-review}}) explains Kleddamag’s T-037,
$s(11)>31/8=3.875$, and what it changes in T-026’s certificate.[^lineage] Figure 3
places these bounds in order.

<figure>
{{LADDER_SVG}}
<figcaption><strong>Figure 3.</strong> The series bound ladder: the verified lower
bounds for eleven squares, from Stromquist’s T-010 to T-060’s exact optimum $T$, with
values from the result register. Rungs are evenly spaced, not to scale; T-061 reweights
T-037’s certificate and stands $3.9\times10^{-9}$ above it.</figcaption>
</figure>

The bound gap between $3.875$ and $T$ is small, but closeness of two numbers supplies no
geometric information about a hypothetical packing in between.
The optimality proof adds two kinds of information.
It conditions geometric and charge arguments on occupied center regions, so they can
eliminate individual patterns.
For the pattern that survives, it proves where every square must be, then applies a
quantitative local theorem at the exact endpoint.
The earlier bounds are antecedents of the method, not premises of the proof: the proof
does not infer equality from a sequence of improving lower bounds, and the separate
tools that check related certificates, wand125’s row-minimum check of T-037
([T-059, in Part II]({{PAPER:n11-threshold-bound-review#what-was-verified-and-what-the-verification-means}}))
and Tokoharu’s rectangle-density verifier, do not verify this argument.[^tools]

## The Construction Gives One Half of the Answer

The algebraic parameter $u$ determines a rotation:

$$
c=\frac{1-u^2}{1+u^2},\qquad s=\frac{2u}{1+u^2},\qquad c^2+s^2=1.
$$

Here $c$ and $s$ are the cosine and sine of the common tilt $a$ of the five tilted
squares in Figure 1, and $u=\tan(a/2)$, with $a=2\arctan u\approx40.18^\circ$. The same
half-angle parameter later describes the orientation of an arbitrary square.
Appendix A gives the placement formulas; number the squares 0 to 10 in the order listed
there. Because a rotation preserves length and right angles, those formulas produce
eleven unit squares.

Feasibility has two finite checks.
Each of the 44 vertices must lie in $[0,T]^2$. Each of the 55 pairs of squares must have
disjoint interiors. For two convex polygons, project both onto a direction and call the
distance between the two projection intervals the **gap** in that direction, negative
when the intervals overlap.
The polygons have disjoint interiors exactly when some edge normal of one of them has a
nonnegative gap, a **weak separating axis**; a zero gap is allowed.
The polygons touch exactly when the largest gap over the edge normals of both polygons
is zero.[^guzhou] Fourteen pairs touch in the construction, and the other 41 are
separated by a positive gap.

The calculations take place in the **number field** $\mathbb Q(u)$, the polynomial
expressions in $u$ with rational coefficients.
Expressions are reduced using the equation defining $u$, and because $p$ is irreducible,
division is exact there too; the selected root is isolated by rational bounds.
Exact identities establish zero, while rational interval refinement determines the signs
of nonzero expressions.
A small floating-point error is never substituted for an equality.[^construction]

These checks prove $s(11)\le T$. Twenty vertex coordinates are exactly $0$ or $T$, with
vertices on all four walls, so the construction’s horizontal and vertical spans are both
exactly $T$; the last step of the proof uses this fact.

The defining polynomial of $u$ is itself one of the fourteen contacts.
If $u$ is varied near its selected root in Appendix A, every wall contact (a square
touching a side of the container) and thirteen of the square contacts hold identically.
The remaining one, between square 2, $A(x_0,T-1)$, and square 10, the image of
$A(\eta+2,-\zeta)$, has gap $p(u)/\bigl(2u(1-u^4)(1+2u-u^2)\bigr)$, which vanishes
exactly at the root; for $u$ just below the root the two squares overlap.[^guzhou] On
the interval $[9/25,37/100]$ the derivative $p'$ exceeds $4$, so the root there is
unique.[^gpt6]

## Sixteen Regions Cover All Possible Centers

Most of the global calculations use the rational number

$$
U=\frac{387708359002281417731}{10^{20}}>T.
$$

This **cap** is slightly larger than the proposed optimum.
If a packing existed in a square of side $L_0<T$, we could translate its container
concentrically into $[0,U]^2$. Its unit squares would keep their sizes, angles and
relative positions. Thus excluding possibilities in the cap also excludes them for every
smaller container. One storage convention needs a name.
The certificate files record a center $p$ as the scaled **file coordinates**
$p_f=(191/50)\,p/U$, so that the container has side $191/50$ in the files; this paper
states every quantity in physical units, and the checkers undo the scale wherever they
read the files.

A unit square contains an open disk of radius $1/2$ about its center.
Two packed squares therefore have centers at least one unit apart: otherwise those
disks, and hence the square interiors, would overlap.
Also, each center $p$ lies in $[1/2,U-1/2]^2$. Normalize this center domain by writing

$$
z=\frac{p-(1/2,1/2)}{U-1}\in[0,1]^2.
$$

Choose sixteen rational cover sites.
Assign each point of $[0,1]^2$ to any nearest cover site, keeping ties.
The resulting **closed Voronoi cells** cover the whole square.
They are the polygons in Figure 4, rather than the squares of a uniform grid: a grid
cell would have physical diameter $1.017$, too large for the lemma below, while the
largest of these cells has physical diameter $0.975$. The exact checker reconstructs
them from nearest-site halfplanes and proves

$$
(U-1)^2\operatorname{diam}(C_j)^2<1
\qquad\text{for every cell }C_j.
$$

**Center-cover lemma.** A physical cell contains at most one packed-square center.
Indeed, two centers in it would be less than one unit apart, contradicting the disk
argument. A center’s label is the index of a cell containing it; at a cell boundary
either containing label may be chosen, and the same argument still prevents two centers
from receiving one label.
A packing on a boundary therefore admits more than one labeling, and each labeling it
admits is excluded on its own below.[^cover]

<figure>
<div class="figure-pair">
{{COVER_SVG}}
{{MASK_SVG}}
</div>
<figcaption><strong>Figure 4.</strong> Left: the sixteen closed Voronoi cells, drawn
from rational vertices bound by the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json">retained cover receipt</a>.
Right: the eleven cells that the
quarter-turned construction occupies. A highlighted cell specifies where a center may
be; it is not a small square. Shared cell boundaries remain in the proof.</figcaption>
</figure>

<figure>
{{CAPACITY_SVG}}
<figcaption><strong>Figure 5.</strong> Why a center cell holds at most one center. Two
hypothetical centers in the same cell would be less than one unit apart, so their open
radius-1/2 disks would overlap. Each disk lies inside its unit square, independent of
the square’s angle, so the squares’ interiors would overlap too. The selected cell,
cell {{CAPACITY_CELL}}, comes from the exact cover; the centers illustrate
the lemma and are not a candidate packing. The
<a href="../../devtools/check_n11_optimality_d4.py">cell checker</a>
proves the strict diameter bound for all sixteen closed cells.</figcaption>
</figure>

An eleven-square packing therefore chooses eleven different labels among sixteen.
There are

$$
\binom{16}{11}=4368
$$

possible subsets, called **masks**. The cover sites are symmetric under the half-turn
$(x,y)\mapsto(1-x,1-y)$ of the center square, which maps cell $j$ to cell $15-j$; they
have no other symmetry, which matters later.
No eleven-element mask is fixed by this pairing, since a fixed mask would have even
size.
Choosing one representative from each half-turn pair leaves 2,184 **cases**, each a
representative mask together with everything the proof derives for it.
These representatives are sorted and numbered starting at zero.

The center-cover reduction permits every orientation.
A square’s orientation is defined only up to a quarter-turn, so take its angle $\theta$
in $[0,\pi/2]$, where both endpoints describe the same square.
For each square separately, write $t=\tan(\theta/2)$. Then

$$
0\le t\le1,\qquad
\cos\theta=\frac{1-t^2}{1+t^2},\qquad
\sin\theta=\frac{2t}{1+t^2}.
$$

This rational parameterization makes interval calculations exact; the tilted squares of
the construction have $t=u$. Both endpoints are retained, even though they describe the
same square orientation.
A certificate never samples angles: it works in **rows**, each a closed interval of $t$
for one square together with the centers allowed over that interval.

The frames and units used below, for reference:

| Symbol | Meaning and units |
| --- | --- |
| $p$ | a center in the cap $[0,U]^2$, in units of the small squares’ side |
| $z=(p-(1/2,1/2))/(U-1)$ | the same center, normalized to the cell cover’s square $[0,1]^2$ |
| $p_f=(191/50)\,p/U$ | the center in the file coordinates the certificate files store |
| $y_i$ | the centered physical height $p_y-U/2$ of the square assigned to cell $i$, where a closed split restricts it |
| $t_i$ | the half-angle parameter $\tan(\theta_i/2)$ of that square, a real number in $[0,1]$ |
| $h_{3k},h_{3k+1},h_{3k+2}$ | the local displacement of construction square $k$: center in physical units, angle in radians |
| $p_T$ | a center after the rigid alignment into the fixed container $[0,T]^2$ |

## One Geometric Invariant Supports the Certificates

Fix a case. A **pose** is a square’s center and angle.
An **owner** is the square assigned to an occupied cell.
Although the packing is unknown, two kinds of rigorous information can be maintained
about each owner:

- An **outer pose cover** contains every pose still possible for that square: a set of
  rows, closed angle intervals with their center polygons.
  It may also retain artificial poses that no valid packing realizes.
- An **owned hull** is a convex polygon that lies strictly inside the square in every
  valid packing under the current assumptions, even while the square’s position is
  uncertain.

The first is an overestimate of possibilities; the second is a guaranteed interior.
Together they are the **invariant**, stated row by row: in every valid packing under the
current assumptions, for every row of an owner whose angle interval contains the owner’s
actual angle, the owner’s actual center lies in that row’s center polygon; and the rows’
angle intervals together cover the whole allowed angular range.
This is stronger than saying the pose lies in the union of the rows, and the difference
matters at a seam: two rows that share an endpoint angle both enclose a pose at that
angle, so a **branch**, an argument that assumes one side of a closed split, may
restrict the angle to one side and drop the other row’s single shared angle, because the
retained row already carries the guarantee there.
A branch may never drop a point or a segment of a center polygon on that ground; those
have their own exact treatment.
Initial owned points need their own proofs, using open inscribed disks or wall
inequalities, or come from a **seed**, a set of points whose ownership has its own
checked proof. Ownership is quantified the same way, over valid packings: an owned hull
need not lie inside the artificial poses that a deliberately loose outer cover retains,
and one retained row of the capture proof contains such a pose, in which a seed point
falls outside an artificial square that the walls already forbid.[^gpt6] An **update**
(the proof data say *step*) takes one owner’s rows, removes centers that an argument
below forbids, and records what remains as the **residual** of each row; a row with a
nonempty residual is **live**. Search programs **propose** rows, residuals and **cuts**
(closed half-plane conditions on a center); the checker proves or refuses them.
The same invariant supports case exclusion and, later, capture near the construction.

### Removing poses that force overlap

Suppose another square must contain a small inner region.
A proposed position of our square is impossible if it forces their interiors to overlap.
We can reject a whole region of centers at once, provided the collision is guaranteed
for every angle in the row.
All other positions remain available until a further argument excludes them.

For an angle interval, choose a convex core $Q$ around the origin that lies strictly
inside the centered unit square at every angle in the interval.
After substituting the half-angle formulas, the needed inequalities reduce to signs of
rational quadratic polynomials.
Checking endpoints and any interior minimum establishes the inequality over the entire
interval, as the independent control beside
[Part II’s Strict-core lemma]({{PAPER:n11-threshold-bound-review#parents-cores-and-the-angle-catalogue}})
does for square cores.

Let $K$ be an owned hull of another square.
A proposed center $x$ is forbidden if

$$
x\in K-Q=K+(-Q)=\{k-q:k\in K,\ q\in Q\}.
$$

For such a center, $k=x+q$ belongs to both squares’ interiors.
This proves overlap.
The strict interior guarantees justify rejecting even the boundary of this closed
forbidden region.
If the cores merely touched the squares’ boundaries, the same rejection
could incorrectly remove a legal touching configuration.

<figure>
{{POSE_SVG}}
<figcaption><strong>Figure 6.</strong> A schematic of one safe exclusion. A possible-center
region records uncertainty; a guaranteed inner region records what a valid packing must
contain. A translated strict core meeting the other square’s owned hull forces overlap:
if $x \in K - Q$, a core point meets the owned hull $K$. $Q$ stays strictly inside the
square throughout the angle row, $K$ is owned in every valid packing under the current
assumptions, and a shared interior forbids even a boundary center $x$.
The forbidden centers can be discarded, while the retained region remains an
overestimate. The drawing illustrates the
<a href="../../devtools/check_n11_generic_fresh.py">geometric checker’s</a>
invariant; it is not a certificate for the displayed schematic.</figcaption>
</figure>

A second collision check compares a region of proposed centers, over one angle row,
against every row of another square’s pose cover, its **partner rows**. It may exclude
the region only when collision is forced for every partner row, including the endpoints
of its angle intervals.

### Keeping everything else

Removing a list of forbidden polygons is insufficient unless the remainder is accounted
for. The checker first computes the domain it must cover: the row’s domain in the
accepted **predecessor** state, the state the update starts from, cut down by two
necessary conditions, that the square lies inside the container and that it contains its
own owned hull, which bounds where its center can be.
It then checks that this required domain is covered by the verified forbidden regions
together with the proposed residual regions.
A proposal may describe a larger domain; only the required domain must be covered.
Exact arrangement checks include segments, singleton points and zero-area intersections.
An area sum alone cannot detect a missing segment where a touching packing might live.
One historical helper deserves a named caveat: the one-dimensional interval test inside
the frozen checkers of charge certificates and of capture accepts a singleton target
$[a,a]$ when a supplied interval lies entirely below $a$, so it is not a general
closed-interval checker.
Its use there is sound for a different reason: the target is a convex polygon of
positive area, the sweep examines every interior slice, which has positive length and
cannot trigger the defect, and a finite union of closed covering regions contains the
limits of those slices and hence the boundary.
Zero-area domains never reach that helper: the charge-certificate checkers refuse them,
and the capture and generic checkers send them to an exact point and segment check.
New callers use a corrected kernel that treats $[a,a]$ as covered exactly when some
supplied closed interval contains $a$; the faster cover kernel that the center partition
uses was already correct.[^gpt6]

After the complete surviving angle cover has been checked, the points that lie strictly
inside the square for every surviving pose, the **common core**, can be added to the
owned hull; their convex hull is also strictly inside.
The hull may then be **compressed** to fewer vertices by exact convex combinations,
which only shrinks it.
These points constrain the other squares.

**Pose-preservation lemma.** Starting from a valid outer cover and valid ownership, each
accepted update preserves every actual packing under its stated assumptions.
If an occupied square’s complete pose cover becomes empty, the case is impossible.
If two independently established owned hulls intersect, the two square interiors overlap
and the case is again impossible.[^geometry]

The order of updates matters.
A point cannot be used as owned before the check establishing its ownership.
Each update names the state it starts from, which must be the state its predecessor
produced; when several owners are updated in parallel, all of them start from the same
declared **common prior**, and their results are joined only after every one succeeds.
The certificate consumers check these dependencies as well as the local inequalities.

<figure>
{{ROW_SVG}}
<figcaption><strong>Figure 7.</strong> One accepted row: case 2095, its second update
(step 1 in the zero-based proof data), owner 10, row 17, over the complete interval
$17/32 \le t \le 9/16$. The panels use retained exact
geometry, rounded only for display, and distinguish the file coordinates of centers
from square-relative core offsets. This row is one of {{ROW_UPDATE_ROWS}} in its update and
contributes one triangular residual to it. A complete
ownership update must also check every other row, closed angular coverage, common-core
inclusion and compression. The
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/full-result.json">accepted case result</a>
and <a href="../../devtools/check_n11_generic_fresh.py">independent checker</a>
supply the evidence: {{ROW_CASE_UPDATES}} complete updates exclude case 2095.
This is an excluded noncandidate case, not the case-438 capture.</figcaption>
</figure>

## Charge Budgets Exclude Many Patterns at Once

The weighted-point idea becomes more selective when the occupied cells are known.
A **field certificate** assigns a charge to every strict inner core; the charges it
assigns, as a function of the core, form its **charge field**. It proves that a square
centered in cell $i$ must receive charge at least $\Gamma_i$, unless it would collide
with an already proved owned hull.
In a legal packing the collision alternative is unavailable, so the charge lower bound
must hold.

One useful charge is defined by five charge sites.
For each projection direction, consider the median of the five projected sites.
A core receives charge one when its projection interval contains that median in every
direction.
Equivalently, every closed half-plane that contains the core contains at least
three of the five sites; the two supporting half-planes of each direction give the
equivalence. A third form is the one to picture: the core meets the convex hull of every
three of the five sites (a three-site hull that misses the core is strictly separated
from it by a line, and the half-plane of that line containing the core then holds at
most two sites). None of the three forms says that the core contains three sites.
With sites at $(\pm1/2,0)$, $(0,\pm1/2)$ and $(1/2,1/2)$, the square core
$[-3/10,3/10]^2$ contains none of them, yet every three of them include two of the four
axial sites, whose midpoint lies in the core, so the core receives the charge.[^gpt6]
The certificate reduces the condition to finitely many direction inequalities.
For the square cores used by these field certificates, directions parallel to the core’s
axes and normals to site-pair lines divide the directions into sectors.
Within each sector the median site and the signs in the core’s support function stay
fixed, so the inequalities are linear in the direction normal; because both axes are
among the dividing directions, no sector exceeds a quarter-turn, and the two bounding
directions suffice.

Two disjoint strict cores cannot both receive that charge.
A strictly separating direction gives them disjoint projection intervals, which cannot
both contain the same median; in the half-plane form, the two closed half-planes on
either side of a separating line would each contain three of the five sites, which is
impossible. The charge therefore has **capacity** one: over any family of disjoint cores
it sums to at most one.
A checked example forces the squares in two occupied cells each to receive charge one,
giving $2>1$. Owned-point collision regions help prove that each cell must be charged,
but those collision regions pay no charge.[^field] Other certificates use three or seven
charge sites, add weighted charges at single points, or combine several such charges;
each charge contributes its weight to at most one core, and the **budget** $b$ is the
sum of the weights. A k-of-m charge of
[Part II]({{PAPER:n11-threshold-bound-review#from-points-to-k-of-m-charges}}) can pay as
many as $\lfloor m/k\rfloor$ disjoint cores; when $2k>m$, a core holding $k$ of its
sites also receives the median-type charge on them, which has capacity one.

The accepted certificate for mask 0, which Figure 8 draws, is the smallest example.
It requires owners in cells 0, 1, 2, 3 and 6, whose 55 owned points have their own
proofs, and requires a charge of one in each of cells 1 and 2 against a budget of one.
Cell 1 is covered by 67 rows and cell 2 by 69. In the first row of cell 1, over the
half-angle interval $[0,1/64]$, every center in the cell’s legal domain either activates
the five-site charge or places the core over a point owned by square 0 or square 2,
which no valid packing allows; the accepted proposal covers the row with the charge’s
region and four such points, and two already suffice.
So each of the two cells receives charge one, the total is $2>1$, and the certificate
excludes every case whose mask or half-turn contains its five owner cells: 459 of
them.[^field]

A certificate requires certain owner cells $O$ to be present, because their owned hulls
supply its collision regions, and assigns lower bounds $\Gamma_i$ to the cells in a set
$P$. It excludes a mask $J$ when

$$
O\subseteq J,
\qquad
\sum_{i\in P\cap J}\Gamma_i>b,
$$

and likewise when the half-turn image of $J$ satisfies the same two conditions, since
that image is the same case.
This explains why one checked certificate can exclude many masks: its antecedent is only
that the cells of $O$ are occupied, so it applies to every mask containing them.
Equality with the budget excludes nothing.
In every accepted certificate the charged cells lie in $O$ and their bounds already
exceed the budget, so in practice the rule reads: a certificate excludes every case
whose mask, or its half-turn, contains its owner set.[^adversarial]

<figure>
{{CHARGE_SVG}}
<figcaption><strong>Figure 8.</strong> Median-projection charge as a capacity argument.
In a separating direction, two disjoint strict cores have disjoint projection
intervals, so both cannot contain the same median. Receiving charge one requires the
median condition in every direction; a single projection illustrates the capacity
argument, not that full test. Required owners and a strict excess over the budget are
necessary for the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json">accepted field certificate</a>
to transfer to another mask. The exact checker certifies every required direction; the
drawing does not show three sites inside a core.</figcaption>
</figure>

The accepted exclusion inventory combines 1,904 cases excluded by field certificates and
276 cases excluded one at a time by the pose-cover updates above, which the proof data
call generic certificates.
Its conclusion is the exact set equality

$$
E=\{0,\ldots,2183\}\setminus\{438,999,1462,1659\}.
$$

The check compares case identities and dependencies, not only the number 2,180. The
publisher groups the same excluded set by provenance as $1931+76+173$: its original
baseline, 76 **prior-family** cases that extend it, and 173 cases **returned** later.
The two groupings divide the same obligation; they are not different totals or
additional exclusions.[^exclusions]

Some exclusions have extra assumptions that must be discharged.
Cases 2175 and 2176 use cuts on center positions that are justified by symmetry, and
that justification assumes the 1,931 exclusions of the publisher’s original baseline:
the cuts are checked only against the 253 cases the baseline leaves.
Cases 2175 and 2176 are two of the publisher’s 76 prior-family cases, and the only two
whose accepted certificates carry this premise; it is a premise of those
certificates.[^premises] wand125 reports a Lean proof of all 76 prior-family cases that
does not use it.[^lean] The four-survivor reduction below assumes these two exclusions
in turn, so their cuts may not use it; the dependency runs one way.
Case 1383 requires both sides of a closed center split at $y_{13}=4/3$. Here
$y_{13}=p_y-U/2$ is the centered physical height of the square assigned to cell 13. Both
sides of the split and the state they split remain part of the accepted proof, even
though the common geometric invariant lets us describe them briefly.

## Symmetry Reduces the Four Survivors to One

Rotating or reflecting the entire container preserves feasibility.
The construction’s center patterns under the eight symmetries of the square belong to
the four surviving cases: the identity and the half-turn give case 1462, the two
reflections in the axes give case 999, the two reflections in the diagonals give case
1659, and the two quarter-turns give case 438 (no center of the construction lies within
$0.0079$ of a cell boundary in normalized units, so these labels are
unambiguous).[^adversarial] It is tempting to rotate the cell labels and declare the
four cases equivalent, but the irregular Voronoi cover does not permit that shortcut.
The half-turn is the cover’s only symmetry; a quarter-turn or reflection need not send a
whole cell to another cell.

Instead, consider four views of each normalized center:

$$
(x,y),\quad(1-x,y),\quad(1-y,x),\quad(y,x).
$$

Together with half-turns these represent the eight symmetries of a square, usually
called $\mathbf{D}_4$
([Part I]({{PAPER:n11-lower-bounds-explainer#the-five-conditions-for-a-point-certificate}})).
Intersect the inverse images of the cells in the four views.
The result is a finite overlay of 220 nonempty closed regions: 212 polygons and eight
singleton points. A center in one overlay region has a specified allowable label in each
view.

For two overlay regions, exact vertex calculations sometimes prove that every pair of
points, one in each region, is less than one unit apart in physical coordinates.
Such a pair cannot contain two centers.
The check retains 1,572 strict distance bans; a distance equal to one is not banned.

<figure>
{{SYMMETRY_SVG}}
<figcaption><strong>Figure 9.</strong> Four views of a center against the fixed cell
cover. The point changes position under square symmetries; the irregular cell polygons
are not permuted by those transformations. An overlay region records the allowed
cell labels in every view. One strict distance ban, for illustration: the maximum
squared physical center distance of overlay regions {{D4_BAN_REGIONS}} is below 1.
The two regions that close the shorter proof in the text, with labels 1, 1, 11, 4 and
2, 5, 6, 9 in the four views, lie at the bottom center and in the lower middle of the
first view, within the rational boxes the text gives.
This illustration explains the construction used by the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json">accepted symmetry check</a>.
The composed proof rests on that check’s exhaustive assignment search,
including boundary ties, over {{D4_REGIONS}} closed regions and {{D4_BANS}} bans; the
shorter proof, which needs one ban, is checked beside it and is not a premise.</figcaption>
</figure>

**Symmetry lemma.** Once the 2,180 exclusions hold, every remaining packing has a
symmetry image that admits case 438, the pattern of the quarter-turned construction.
To prove this, suppose every view avoids 438 and its half-turn.
Each view must then have a mask from the other three candidates and their half-turns.
Exhaustive finite enumeration tries the compatible overlay assignments, requiring
distinct occupied labels in each view and respecting all distance bans.
None exists.[^symmetry]

Every genuine packing would supply such an assignment by choosing containing closed
cells in each view. Their nonexistence proves the lemma, including all boundary ties.
The enumeration may allow geometric arrangements that no real packing realizes; that
only makes its impossibility conclusion stronger.

The same conclusion has a shorter proof that needs only one distance ban.
A retained checker carries it beside the accepted one, but the composed proof rests on
the exhaustive search above, and the shorter proof is not one of its premises.
Fix the mask of the identity view and consider the 216 ways to assign one of the six
non-438 masks to each of the other three views.
Propagating the cell labels through the overlay, each owner keeps only the regions whose
labels in every view agree with that view’s mask, and an owner left with no region, or a
mask label that no owner carries, ends the triple at once.
That leaves 48, 18 and 20 triples for the identity cases 999, 1462 and 1659. Two rules
then propagate the labels: an owner confined to one region reserves that region’s
labels, deleting conflicting regions from the other owners; and if only one owner can
supply a required label in a view, that owner keeps only regions carrying that label.
Repeating both rules, and rejecting an empty owner domain or an unsupported view label,
leaves one, one and none.[^guzhou] In the survivor for 999, the owners of cells 1 and 2
are each confined to one overlay region, inside $[23/50,27/50]\times[0,11/100]$ and
$[11/25,14/25]\times[23/100,7/25]$ in normalized coordinates, so their centers differ by
at most $1/10$ horizontally and $7/25$ vertically and lie less than one unit apart,
since $(U-1)^2\bigl((1/10)^2+(7/25)^2\bigr)<1989/2500<1$. The survivor for 1462 is the
reflection of that one through the first view, and the same pair of regions closes
it.[^gpt6]

## Capture Forces Case 438 Near the Construction

Case 438 specifies the occupied cells

$$
\{0,1,2,3,4,8,9,10,11,13,15\}.
$$

The pose-preservation invariant now serves a different purpose.
Rather than emptying every pose domain, the checks progressively enclose surviving poses
near the quarter-turned construction.
The proof is a tree of **nodes**. Each node is a checked state, the pose covers and
owned hulls of all eleven owners, together with the branch assumptions it inherits; each
**leaf** ends either in a contradiction, a **far** leaf, or in an enclosure, the
**near** leaf. The **root** carries no assumption.
Before the tree, fourteen **root rounds**, each a parallel update of all eleven owners
from a common prior, establish the root’s ownership; the root node then completes
thirteen further updates of its own.
A fourteenth step covers only part of its angle range; it is checked but changes no
ownership. All of this is replayed here, in the capture receipts cited below, before the
local theorem is invoked.

Three closed splits produce four branches.
Here square subscripts denote owner-cell labels; $y_{15}$ is a centered physical height
and $t_i$ is the half-angle parameter of the square assigned to cell $i$.

| Branch assumptions | Checked conclusion |
| --- | --- |
| $y_{15}\le5/4$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\le147/512$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\le183/512$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\ge183/512$ | Enclosure in the local neighborhood |

Equality belongs to both sides of every split.
The overlap is harmless and prevents a missing boundary branch.

<figure>
{{CAPTURE_SVG}}
<figcaption><strong>Figure 10.</strong> The accepted ten-node capture ancestry.
Intermediate nodes propagate a checked state; three far leaves end in contradiction
and the near leaf encloses every surviving pose. Edges denote proof dependencies,
not trajectories of moving squares. Here $y_{15} = p_y - U/2$ is a physical centered height
and $t_i = \tan(\theta_i/2)$ is an owner’s half-angle parameter.
Edge labels give each new closed split condition;
the branch table collects the inherited conditions. Both sides retain equality.
The near leaf is an enclosure; the fixed-T local theorem is still needed.
The fourteen root rounds precede the root node itself; the nine parent edges drawn here
are bound by the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json">accepted source graph</a>,
the receipt that records each node’s parent.</figcaption>
</figure>

The final near state contains 136 live rows and 1,542 center vertices.
The pose-inclusion check proves that all their center polygons and all their angle
intervals lie inside the same local rectangle, which the next section describes.
Convexity extends center bounds from vertices to whole polygons.
Exact bounds for $2\arctan(t)$ convert interval endpoints to angular displacements in
radians. For an axis-aligned square, an interval near $t=1$ describes the same
orientations as one near $t=0$, and the chart change $t\mapsto(t-1)/(t+1)$, which equals
$\tan((\theta-\pi/2)/2)$, measures its displacement from that side.
A half-angle parameter is never substituted for a radian angle.
The root rounds, the accepted ten nodes and their nine parent edges together bind this
enclosure to the original unconditional case, rather than to an assumed favorable
starting pose.[^capture]

## The Local Argument Excludes Every Nonzero Motion

Fix the container as $[0,T]^2$ and label the eleven squares as in the exact
construction. A perturbation has 33 coordinates:

$$
h=(\Delta x_0,\Delta y_0,\Delta\theta_0,\ldots,
\Delta x_{10},\Delta y_{10},\Delta\theta_{10}).
$$

The checked local neighborhood is a rectangle $|h_j|\le r_j$, with positive coordinate
radii $r_j$. Different coordinates have different radii, allowing the rectangle to fit
the captured domains: the largest radius is $0.0068$ and the smallest $0.00065$, and
each was chosen to fit its captured domain with almost no slack.
All radii lie within the **working box** $|h_j|\le1/64$, the region over which the
curvature constants of Appendix B were bounded.

The local theorem excludes any nonzero displacement in this rectangle that remains
feasible in the fixed-$T$ container.
Its mechanism is quantitative: the linear gap constraints obstruct motion, and an exact
bound on their curvature proves that the nonlinear terms cannot overcome that
obstruction anywhere in the rectangle.

Write $\tau$ for the largest displacement as a fraction of its allowed coordinate
radius. A nonzero displacement has $0<\tau\le1$. The certificate for a coordinate
attaining that maximum forces $\tau\le c_j\tau^2$, with $c_j<1$. This is impossible:
throughout that interval, $c_j\tau^2<\tau$.

<figure>
{{LOCAL_SVG}}
<figcaption><strong>Figure 11.</strong> The local contradiction. The upper line is
$\tau$ and the lower curve is $c\tau^2$, with a coefficient $c$ below one, on
$0 < \tau \le 1$. A feasible nonzero displacement would require the line to lie at or
below the curve, so there is none. This is an
algebraic illustration of the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json">accepted exact inequalities</a>,
{{LOCAL_MARGINS}} exact margins over {{LOCAL_BRANCHES}} linear systems,
not a projection of the 33-dimensional feasible set. The theorem applies in the checked
rectangle inside the fixed side-$T$ container, which capture and inclusion reach first.</figcaption>
</figure>

### Covering all possible local contact patterns

Nearby squares can change which edges separate them, so the proof must consider more
than one contact pattern.
The construction has fourteen contacting pairs.
A **separation feature** of a pair chooses which square supplies the axis, one of its
two edge-normal directions, and which square lies on the positive side; the pair is
separated by the feature when all four corners of the other square satisfy the
corresponding projection inequality.
Written out, with $g_{f,k}$ the gap of corner $k$ under feature $f$, the pair has
disjoint interiors exactly when

$$
\bigvee_{f=1}^{8}\ \bigwedge_{k=1}^{4}\ g_{f,k}(h)\ge0,
$$

a disjunction over features of a conjunction over corners.
Each pair has eight features, 112 altogether.
A feature is **available** when its conjunction holds at the construction; exact signs
show 24 available and 88 unavailable, each of the 88 having a corner with a strictly
negative gap, which disables the whole feature.[^gpt6] Taylor bounds prove that those 88
remain unavailable throughout the full rectangle.

A feasible perturbation separates each contacting pair by one of its available features,
so the check enumerates the 512 combinations of available features.
Coincident corners in the two pairs of axis-aligned squares that meet along a full edge
give identical inequalities, which leaves 128 distinct linear systems, the **contact
branches**. A contact branch keeps only the inequalities that are **tied** at the
construction, those whose gap is exactly zero there: 22 corner inequalities from the
chosen features and 20 wall inequalities, 42 in all.
Omitting the constraints of pairs that do not touch at the construction, and the
inequalities with positive gap, weakens this necessary system; it cannot discard a
feasible packing. No new contact can form inside the rectangle in any case: the 41
non-contacting pairs keep a clearance of at least $0.015$ throughout it.[^adversarial]
Conversely, every feasible perturbation must select one of the checked contact
branches.[^local]

### From a linear obstruction to a finite neighborhood

Let $g_i(h)$ be a gap that must be nonnegative in a chosen contact branch, with
$g_i(0)=0$. Write its linear part as $A_i h$. A linear calculation alone would describe
only infinitesimal motion.
To control an actual displacement, the proof bounds the quadratic remainder.

Normalize the size of a hypothetical nonzero displacement by

$$
\tau=\max_j\frac{|h_j|}{r_j},\qquad 0<\tau\le1,
\qquad R=\max_j r_j.
$$

The checked curvature bounds $K_i$ give the necessary inequalities

$$
A_i h\ge-\frac{\tau^2K_i}{2}.
$$

Choose a coordinate $j$ attaining $|h_j|=\tau r_j$, and choose the sign $\sigma$
opposite to $h_j$. A certificate supplies nonnegative rational weights $\lambda_i$, and
the weighted combination of the gap rows nearly isolates that coordinate: write

$$
e=\lambda^{\top}A-\sigma e_j^{\top},\qquad
\eta=\sum_k r_k|e_k|,\qquad M_j=\sum_i\lambda_iK_i,
$$

where $e_j$ selects coordinate $j$. Multiplying the gap inequalities by the weights and
using $|h_k|\le\tau r_k$ gives

$$
\tau r_j=-\sigma h_j\le e\cdot h+\frac{\tau^2M_j}{2}
\le\tau\eta+\frac{\tau^2M_j}{2}.
$$

A certificate with

$$
\eta+\frac{M_j}{2}<r_j
$$

therefore leaves no $\tau$ in $(0,1]$: dividing by $\tau$ and using $\tau\le1$ would
give $r_j\le\eta+M_j/2$. The checker bounds the residual more coarsely, by
$\|e\|_1\le\epsilon_j$ with $R=\max_k r_k$, so that $\eta\le\epsilon_jR$, and verifies
for every one of the $128\times33\times2=8,448$ certificates the strict margin

$$
M_j<2(r_j-\epsilon_jR),
$$

which is the same conclusion in the form $\tau\le c_j\tau^2$ with
$c_j=M_j/(2(r_j-\epsilon_jR))<1$, the form Figure 11 draws.
The largest certified $c_j$ is approximately $0.676505208$; the proof uses exact strict
comparisons, not this rounded display value, and the two ratios $(\eta+M_j/2)/r_j$ and
$c_j$ are different numbers.[^gpt6]

**Local-isolation lemma.** The zero perturbation is the only feasible packing in the
declared labeled rectangle inside the fixed container $[0,T]^2$. The quadratic bounds
make this a theorem about a finite neighborhood, including its boundary.
Appendix B describes the curvature and negative-feature checks.

## Closing the Gap Between the Rational Cap and the Exact Optimum

The global geometry was computed at $U>T$, while isolation holds at the exact side $T$.
The conclusion needs a precise connection between the two frames.

Start from a hypothetical packing $P$ in a square of side $L_0<T$, centered in the cap.
The symmetry lemma supplies a symmetry $g$ of the square for which $g(P)$ admits case
438; because $g$ fixes the cap’s center, $g(P)$ still lies in the concentric side-$L_0$
container, and its squares are unchanged.
Case 438 is the pattern of the quarter-turned construction, so let
$\operatorname{rot}(x,y)=(-y,x)$ be that quarter-turn and undo it.
In physical coordinates, the local center corresponding to a captured center $p$ is

$$
p_T=\operatorname{rot}^{-1}\!\left(p-(U/2,U/2)\right)+(T/2,T/2);
$$

the certificate files store $p_f=(191/50)\,p/U$, so the checker first multiplies by
$U/(191/50)$. This is a rigid rotation and translation, and a quarter-turn leaves every
orientation unchanged modulo $\pi/2$, so the captured angle rows carry over unchanged.
The side-$L_0$ container centered inside $U$ becomes

$$
[(T-L_0)/2,(T+L_0)/2]^2\subset[0,T]^2
\qquad(L_0<T).
$$

Its small squares are still unit squares.
The complete capture and inclusion checks place their labeled poses in the local
rectangle, and they are feasible in the fixed-$T$ container.
The local-isolation lemma forces them to be the exact construction.
But that construction spans $T$, so it cannot lie in a square of side $L_0<T$. This
contradiction excludes every smaller side directly.
Together with the exact witness, it proves $s(11)=T$.[^endpoint]

<figure>
{{ENDPOINT_SVG}}
<figcaption><strong>Figure 12.</strong> Why the rational cap settles the exact endpoint.
The same hypothetical side-$L_0$ container, with $L_0 < T$, fits concentrically inside the
cap and then inside the fixed side-$T$ container after the checked rigid alignment. Its
unit squares keep their size. Capture and
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json">pose inclusion</a>
put the packing in the local rectangle; isolation forces the construction, whose span
$T$ contradicts its containment in side $L_0$. Gaps are exaggerated for visibility;
the drawing does not depict a feasible smaller packing.</figcaption>
</figure>

This deduction does not rule out perturbations in the larger cap $U$. It needs only the
impossibility of a smaller packing.
The same premises apply when $L_0=T$: a packing of side exactly $T$ also enters the cap,
the symmetry lemma, capture and inclusion, and the local theorem then makes its aligned
image the construction.
So, on the same complete exclusion and capture ensemble, every optimal packing is the
construction up to the eight symmetries of the container and relabeling of the
squares.[^gpt6] The Squares Project registers this corollary separately as T-112. It
rests on T-060’s evidence and adds no computation; its one new step, that each premise
is stated for a side at most $T$, is prose.
Trump called his packing rigid, meaning that no square can move; that is a local
property, and no earlier source found states that the optimum is unique.
Uniqueness is not automatic at a solved count: Stromquist gives three different optimal
packings of ten squares.[^prior-unique]

## What Was Verified, and What the Verification Means

The public proof source is
[Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c),
linked at the revision that was confirmed.
The Squares Project’s confirmation uses independently written consumers of its proposed
certificate data and a mathematical review of the implications above.
The accepted computation covers the required proof ensemble, including all 2,180
exclusions and all ten capture nodes.[^review]

| Mathematical obligation | Accepted evidence |
| --- | --- |
| Exact endpoint and matching upper bound | Algebraic root, unit-square construction, 44 vertex containment checks, 55 pair checks, $T<U$, opposite-wall span |
| Exhaustive global classification | Sixteen closed cells, 4,368 masks, 2,184 half-turn representatives |
| Noncandidate impossibility | Exact 2,180-case exclusion set with discharged conditional premises |
| Reduction to case 438 | Closed symmetry overlay and exhaustive assignment check |
| Capture | Complete root induction, ten nodes, nine parent joins, three far contradictions and the near enclosure, all under closed branch conditions |
| Local isolation and inclusion | Complete feature census, 8,448 dual checks, nonlinear bounds and enclosure of the accepted near state |
| Final theorem | Composition of those premises with the rigid smaller-container embedding |

Search programs may choose promising cuts, cores or dual weights.
They need not be trusted to find correct ones: a certificate checker recomputes the
finite conditions that make each proposal sound.
The review must still establish why those conditions imply the continuous geometric
claim. Reexecution tests reproducibility; it does not, by itself, prove that a checker
implements a sound mathematical rule.

The independence has limits.
The consumers share this project’s exact clipping, closed-cover and collision routines,
which the published source also bundles; the local checks also share construction,
derivative and exact-arithmetic primitives.
The confirmation follows the same mathematical argument, rather than supplying a
distinct proof method.
The Squares Project therefore records the result as T-060, S5/V3/C3, rungs on the
significance, verification and confirmation axes of its
[epistemics guide](../../../epistemics.md): significance 5, movement on a central open
case, with a machine certificate replayed here and its review record pending on both the
verification and the confirmation axes.
Under the ladder of 2026-09-30, rung 4 on either axis also needs a second adversarial
review by a distinct reviewer and a retained human oversight record; the reviews linked
from this paper that record V4/C5 were written under the ladder in force before that
date.
This confirmation claims neither a distinct proof method nor a full proof-assistant
replay. The trust base includes the reviewed mathematical reductions, checker source,
arithmetic libraries, runtime and executing system.

Two Lean 4 formalization projects are
[wand125/n11-optimality-lean](https://github.com/wand125/n11-optimality-lean) and
[Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized).
wand125 reports that the 76 prior-family cases and the 173 returned cases are already
kernel-checked using only Lean’s standard axioms; an independent replay of the 173
against the 11SquaresFormalized assembly is recorded in
[an open pull request to that repository](https://github.com/Queuingtheorydotcom/11SquaresFormalized/pull/7),
not merged as of October 4.[^lean] On October 6 Queuingtheorydotcom reported the
formalization in 11SquaresFormalized complete: 7,920 Lean modules with no admitted goal,
its numerical certificates checked by `native_decide`, so that it trusts Lean’s compiler
as well as its kernel.[^lean-done] The Squares Project’s statement audit of October 6
reads its theorem, `ElevenSquare.optimality`, as exactly $s(11)=T$; the full run is
private, so T-060 records it as the source’s report, and no rung rests on either
formalization.

The final composition receipt reconciles the completed geometric executions and their
reviewed dependencies.
It does *not* rerun those calculations.
Four stale final-state digest bindings in the publisher’s packet prevented accepting its
unchanged full runner as a successful replay; the independent confirmation uses freshly
observed component executions and checked state joins instead.
A fresh one-command rerun of the entire independent ensemble still needs a reviewed way
to rebind newly generated parent receipts, whose timing fields change their bytes.
That automation issue is tracked separately from the completed mathematical
obligations.[^reproduce]

The composer reads its receipts by hash, and each receipt names its inputs by hash, so a
reader can verify at three depths: that every retained object still decodes to its hash;
that the composition’s joins agree over the retained executions, which takes seconds; or
that a component’s geometry recomputes afresh from the retained inputs, for which the
validation guide gives one portable command per checker.
The packet also keeps the ancestry each accepted receipt cites as its input, the
controls that measure what a partial or refused run reports, and the superseded attempts
beside their replacements, so the record says why each accepted run exists; the
[receipts register](../../resources/web/n11-optimality-2026-09-29/receipts/README.md)
states the purpose of every one and who reads it.

The two adversarial reviews of October 3 added four checked components that stand beside
the accepted ones rather than in their place: a corrected closed-interval kernel for new
callers; the incidence propagation that shortens the symmetry lemma; the two-radius
local box; and the selection of 44 of the 46 accepted field certificates whose union
already excludes every case the field certificates exclude, a reading aid and a replay
shortcut rather than a deletion.
Each has its own receipt or manifest and its own tests.
None is a premise of the composed proof, and none changes a frozen checker or an
accepted receipt.

The [T-060 validation guide][reproduction] separates fast checks of retained evidence
from fresh geometric replay, and links each checker, source binding and recorded
execution. It is the place to reproduce a component; merely rerunning the final composer
is not an independent end-to-end proof run.

## Appendix A: Exact Placement Formulas

For a direct construction, let $A(a,b)=[a,a+1]\times[b,b+1]$, and define

$$
\begin{aligned}
\rho&=1-(T-3)c, &
\eta&=\frac{(1+\rho)c-1}{s},\\
v&=c-s, &
\zeta&=\frac{T-1}{s}-\rho-(3+\eta)\frac{c}{s},\\
x_0&=1+\frac{2}{c}-(T-2)\frac{s}{c}.
\end{aligned}
$$

The six axis-aligned squares are

$$
\begin{gathered}
A(0,0),\quad A(T-1,0),\quad A(x_0,T-1),\\
A(0,T-1),\quad A(1,T-1),\quad A(0,T-2).
\end{gathered}
$$

Define the rigid map

$$
F(x,y)=(1,1)+
\begin{pmatrix}c&-s\\s&c\end{pmatrix}(x,y-\rho).
$$

The remaining five squares are the images under $F$ of

$$
\begin{gathered}
A(0,0),\quad A(\eta,-1),\quad A(1,v),\\
A(\eta+1,v-1),\quad A(\eta+2,-\zeta).
\end{gathered}
$$

All quantities are elements of $\mathbb Q(u)$. These formulas, together with the
isolated root, specify the construction without relying on coordinates read from a
drawing.[^construction]

The squares, numbered as above, correspond to the cells that case 438 assigns their
quarter-turned images; the inclusion check and the local theorem use this
correspondence.

{{ROLE_MAP_TABLE}}

## Appendix B: The Nonlinear Estimates

For a pair gap, let square $o$ supply the separating axis and square $p$ supply the
tested corner. Put $w_i=r_{3i+2}$ for square $i$’s angular radius.
A bound on the second derivative along any direction in the coordinate rectangle is

$$
\begin{aligned}
K={}&D_{op}w_o^2\\
&+2\sqrt{(r_{3o}+r_{3p})^2+(r_{3o+1}+r_{3p+1})^2}\,w_o\\
&+\frac{(w_o+w_p)^2}{\sqrt2}.
\end{aligned}
$$

Here $D_{op}$ bounds center separation throughout the working box.
The terms bound the rotation of the center projection, the mixed translation–rotation
derivative and the relative rotation of the corner.
A wall gap has $K=w_i^2/\sqrt2$. Checked rational upper bounds replace the square roots.
When several elementary gap functions share one gradient, the checker uses the largest
applicable curvature bound.

An unavailable separation feature has a corner gap $g$ with $g(0)<0$. The checker
establishes

$$
g(0)+\sum_j|\partial_jg(0)|r_j+K/2<0.
$$

Taylor’s theorem then keeps that corner gap negative throughout the closed rectangle.
The feature cannot become available there.
These 88 exclusions, the exhaustive remaining feature choices, and the
curvature-weighted dual inequalities supply the nonlinear premises of local
isolation.[^local]

## Appendix C: Retained Data of the Local Rectangle and the Cover

The 33 radii of the local rectangle, as the accepted inclusion and isolation receipts
bind them, by construction square: $r_x$ and $r_y$ in units of the small square’s side
and $r_\theta$ in radians.

{{LOCAL_RADII_TABLE}}

The sixteen sites of the center cover, in normalized coordinates: each pair of integers
is divided by $2{,}000{,}000$, and site $15-i$ is $(1,1)$ minus site $i$.

{{COVER_SITES_TABLE}}

A box with two radii isolates the construction as well, and more simply: $1/256$ for
every coordinate except the angles of squares 9 and 10, which get $1/128$. Every
accepted radius is at most its replacement, the tightest being square 6’s angle at
$0.904$ of $1/256$, so the accepted pose inclusion places the captured poses in this box
too. Over it the quadratic remainders of the gap functions have six curvature bounds of
the form $K/r^2$: $21/2$, $57/4$, $99/4$ and $30$ for a contacting pair, by the two
squares’ multiplicities, and $3/4$ and $3$ for a wall contact.
Run with the repository’s finer curvature bounds, the accepted dual weights and the same
128 contact branches, the isolation checker accepts this box with worst ratio $0.8667$
over its 8,448 signed-coordinate margins, against $0.6765$ for the fitted radii; the
review’s six constants alone give $0.9515$. The result is retained as a checked
component beside the accepted one; the proof’s rectangle remains the fitted one.[^gpt6]

## Sources and Verification Record

The [simplification review][simplification] freezes the dependency map used in this
exposition. It consolidates repeated geometric rules and the endpoint argument without
claiming fewer necessary cases, rounds or branches.
The figures are explanatory renderings of retained data; their rounded screen
coordinates are not inputs to certificate acceptance.
Two adversarial reviews of October 3, 2026, the
[project’s own](../../../docs/project/reviews/review-2026-10-03-n11-optimality-paper-adversarial.md)
and
[GPT-6 Pro’s](../../../docs/project/reviews/review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md),
recomputed the paper’s numbers independently and found no mathematical error; the
[integration record](../../../docs/project/reviews/review-2026-10-03-n11-gpt6-pro-review-integration.md)
dispositions every finding of the second, and the retained components it added stand
beside the accepted ones rather than in their place.
The [October 7 review][guzhou] checks the revised exposition and selected proof
components, including the contact criterion, local contact deformation and shorter
symmetry census. It records seven corrections and distinguishes its fresh component
checks from retained-receipt composition and a full proof replay.

## Version History

{{VERSION_HISTORY}}

[^credit]: [T-060 attribution and evidence](../../frontier/results.yaml);
    [upstream source and third-party credits](../../resources/web/n11-optimality-2026-09-29/README.md).
    Trump’s construction is credited to Walter Trump; the bundled exact reconstruction
    credits David Ellsworth’s diagram.
    This paper explains the imported proof and the repository’s confirmation, rather
    than claiming a new global argument.

[^proof]: [Original proof, §1: exact statement](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#1-statement-and-exact-endpoint)
    and
    [§10: final deduction](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#10-deduction-of-the-optimum);
    [whole-proof acceptance review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance).

[^review]: [T-060](../../frontier/results.yaml);
    [current review disposition](../../../docs/project/reviews/review-2026-09-29-n11-optimality.md);
    [whole-proof acceptance](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance);
    [verification and confirmation levels](../../../epistemics.md).

[^lineage]: [Part I, the T-018/T-025/T-026 explainer]({{PAPER:n11-lower-bounds-explainer}});
    [Part II, the review of T-037]({{PAPER:n11-threshold-bound-review}});
    [n = 11 result history](../../frontier/n-011.md);
    [result register](../../frontier/results.yaml).

[^tools]: [Tooling overview and scope of independent verification](../../../docs/project/verification-tooling.md).
    T-059 concerns reported row-minimum equality, while T-060 concerns global
    optimality. A rectangle-density or row-minimum check cannot substitute for the
    latter’s complete case and capture argument.

[^construction]: [Exact construction source](../../cases/trump11/packing.py);
    [exact feasibility checker](../../cases/trump11/verify_exact.py);
    [original proof, §2: construction and upper bound](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#2-exact-construction-and-upper-bound).

[^cover]: [Original proof, §4: closed center cover and masks](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#4-closed-center-cover-and-the-2184-cases);
    [exact cover consumer](../check_n11_optimality_d4.py);
    [independent cover receipt](../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json);
    [case census](../../resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json).

[^geometry]: [Original proof, §5: case-exclusion implications](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves);
    [independent row geometry checker](../check_n11_capture_transition_pilot.py) and
    [first-row receipt](../../resources/web/n11-optimality-2026-09-29/receipts/capture-transition-row0/result.json);
    [complete ownership update](../../resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json).
    The
    [mathematical transition review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#first-complete-capture-owner-update)
    separates a checked row from a promoted complete step.

[^field]: [Original proof, §12: the field certificates and their transfer](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#12-how-the-23-verification-stages-support-the-theorem),
    which names the 59 certificates and the transfer rule but states no charge lemma;
    the lemma above and its review are the Squares Project’s;
    [exact field consumer](../check_n11_optimality_field_mask0.py);
    [accepted mask-0 field receipt](../../resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json);
    [mathematical review of the five-site charge](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#first-independent-field-exclusion-mask-0).

[^exclusions]: [Complete exclusion inventory](../../resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json);
    [case census, which counts the field certificates](../../resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json);
    [original proof, §9: accepted global obligations](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#9-accepted-global-verification-obligations);
    [independent exclusion and conditional-premise review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#complete-exclusion-execution-census).

[^premises]: [Non-field case manifest](../../resources/web/n11-optimality-2026-09-29/receipts/nonfield-manifest/manifest.json.gz),
    which records the 1,931-case premise for cases 2175 and 2176 alone among the 76
    prior-family cases; the cut reports for
    [case 2175](../../resources/web/n11-optimality-2026-09-29/receipts/generic-case2175-complete/replay-d4-cuts.json)
    and
    [case 2176](../../resources/web/n11-optimality-2026-09-29/receipts/generic-case2176-complete/replay-d4-cuts.json);
    [the special adapters and their premises](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#the-three-special-adapters).

[^symmetry]: [Closed-overlay checker](../check_n11_optimality_d4.py),
    [accepted symmetry receipt](../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json)
    and
    [original proof, §6: the D4 implication](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#6-the-exact-d4-reduction-to-case438).

[^capture]: [Capture ancestry](../../resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json);
    [fourteen-round root chain](../../resources/web/n11-optimality-2026-09-29/receipts/capture-root-chain/result.json);
    the root node’s
    [first update](../../resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json)
    and
    [twelve further complete updates with the partial fourteenth step](../../resources/web/n11-optimality-2026-09-29/receipts/capture-root-node-full-integer/result.json);
    [accepted near node](../../resources/web/n11-optimality-2026-09-29/receipts/capture-child-near/result.json)
    and
    [pose-inclusion receipt](../../resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json);
    [original proof, §8: capture and frame bridge](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#8-complete-case438-capture-and-the-exact-u-to-t-bridge).

[^local]: [Exact local-isolation checker](../check_n11_optimality_local_isolation.py)
    and
    [accepted local-isolation receipt](../../resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json);
    [original proof, §7: contact branches and finite rectangle](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#7-local-contact-analysis-and-the-focused-isolation-rectangle).
    The focused rectangle is distinct from the earlier uniform-radius local theorem.

[^endpoint]: [Original proof, §10: deduction of the optimum](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#10-deduction-of-the-optimum);
    [endpoint and final-composition review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance);
    [accepted final composition](../../resources/web/n11-optimality-2026-09-29/receipts/final-composition.json).

[^adversarial]: [Adversarial review of this paper](../../../docs/project/reviews/review-2026-10-03-n11-optimality-paper-adversarial.md):
    the contact that defines $u$, the symmetry images of the construction, the shape of
    the accepted charge certificates and the clearance of the non-contacting pairs were
    computed there, outside the accepted certificate ensemble.

[^guzhou]: [October 7 exposition and component review](../../../docs/project/reviews/review-2026-10-07-n11-optimality-paper-guzhou.md),
    findings F1–F4; its verification table states the scope of each fresh check.

[^gpt6]: [GPT-6 Pro’s unified adversarial review](../../../docs/project/reviews/review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md),
    received 3 October 2026: its findings C1, C5, C6, C7 and C9 and simplifications S1,
    S5, S6 and S7 are applied in this revision, and the
    [integration record](../../../docs/project/reviews/review-2026-10-03-n11-gpt6-pro-review-integration.md)
    dispositions every finding.

[^lean]: [wand125’s comment of 4 October 2026 on jlevy/squares#317](https://github.com/jlevy/squares/issues/317#issuecomment-5975093980),
    the source for the formalization status this paper reports, and the
    [prior-family theorem](https://github.com/wand125/n11-optimality-lean/blob/112f91a0a0a30539472718b88e06e71f64d61694/lean/Sqpack/S11Opt/Split/U2Prior.lean)
    on the `split` branch of wand125/n11-optimality-lean, as committed on October 1,
    2026, which states the exclusion of all 76 cases with no baseline hypothesis.
    The Squares Project has audited the statement of the 11SquaresFormalized theorem and
    built its statement closure and upper half, and has replayed neither proof in full.

[^prior-unique]: [Trump 2023](https://www.researchgate.net/publication/368988287), p. 2:
    “The geometrical object is absolutely rigid, no unit square can be rotated or
    translated”;
    [Stromquist 1984, memorandum II](https://www.walterstromquist.com/papers/squares2.pdf),
    p. 1: “Three different packings of ten unit squares in a square of side
    $s = 3 + \sqrt{2}/2$”, which [Stromquist 2003](https://doi.org/10.37236/1701) proves
    optimal (its Figure 1). The upstream proof states uniqueness only for the near
    branch of its case 438, in
    [§8](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#8-complete-case438-capture-and-the-exact-u-to-t-bridge),
    and concludes $s_{11}=T$ in its §10.

[^lean-done]: [The verification report of 6 October 2026](https://github.com/Queuingtheorydotcom/11SquaresFormalized/blob/cdc746ed907d258057c283aeb6d077cb2c27e349/docs/VERIFICATION_20261006.md)
    in Queuingtheorydotcom/11SquaresFormalized, status
    `OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES`, which states that
    `ElevenSquare.optimality` depends on `propext`, `Classical.choice`, `Quot.sound` and
    13,308 axioms from approved `native_decide` certificate checks; and this project’s
    [statement audit](../../../docs/project/reviews/review-2026-10-06-n11-lean-formalization-statement-audit.md)
    of the theorem it states.

[^reproduce]: [Reproduction guide and disclosed limits](../../resources/web/n11-optimality-2026-09-29/README.md#reproducing-the-independent-checks);
    [tooling overview](../../../docs/project/verification-tooling.md).
    The final composition has `geometry_rerun: false`; it binds the observed executions
    rather than replacing them.

[earlier]: {{PAPER:n11-lower-bounds-explainer}}
[reproduction]: ../../resources/web/n11-optimality-2026-09-29/VALIDATION.md
[simplification]: ../../../docs/project/reviews/review-2026-09-30-n11-expository-simplification.md
[guzhou]: ../../../docs/project/reviews/review-2026-10-07-n11-optimality-paper-guzhou.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
