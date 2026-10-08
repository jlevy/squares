{{FRONT_MATTER}}

*Evidence cutoff: 8 October 2026. The survey includes retained releases through 7
October 2026.*

A record square packing can begin as a geometric sketch, a random configuration, or
pieces borrowed from an earlier record.
The final coordinates may then pass through several optimizers before a verifier
establishes that the squares fit.
Understanding that chain explains both how a new arrangement is found and why an
improvement in its last decimal places can be a different contribution.

## Contents

1. [The Problem and the Kind of Result](#the-problem-and-the-kind-of-result)
2. [From a Seed to a Certified Bound](#from-a-seed-to-a-certified-bound)
3. [The Geometry a Search Has to Navigate](#the-geometry-a-search-has-to-navigate)
4. [Constructing and Reusing Seeds](#constructing-and-reusing-seeds)
5. [Moving Between Arrangements](#moving-between-arrangements)
6. [Refining a Promising Arrangement](#refining-a-promising-arrangement)
7. [Turning Coordinates Into a Bound](#turning-coordinates-into-a-bound)
8. [Reading the Record](#reading-the-record)
9. [Vocabulary and Further Reading](#vocabulary-and-further-reading)

## The Problem and the Kind of Result

Let $s(n)$ be the smallest side of a square that can contain $n$ **unit squares**, each
free to translate and rotate.
The small squares must have disjoint interiors; edges and corners may touch.
A construction that fits in a container of side $S$ establishes the **upper bound**
$s(n)\le S$.

Two elementary bounds put the search in context.
The pieces have total area $n$, so $s(n)\ge\sqrt n$. An axis-aligned grid supplies
$s(n)\le\lceil\sqrt n\rceil$. At a perfect square these meet: $s(m^2)=m$. At $n=11$ they
leave the interval $\sqrt{11}\le s(11)\le4$. Tilting some pieces permits a smaller
container than that grid.
Walter Trump’s 1979 construction uses six axis-aligned squares and five at one common
angle near $40.18^\circ$, in side approximately $3.87708359$. Its geometry provides an
upper bound; proving that no other arrangement improves it is a separate problem
([historical survey](../../resources/web/friedman-ds7-survey-2009-html.md);
[tutorial](../../../TUTORIAL.md#1-the-problem)).

A square’s **pose** consists of its centre $(x_i,y_i)$ and orientation $\theta_i$. A
quarter turn gives the same square, so angles can be represented modulo $\pi/2$.
Together with the side $S$, a configuration has $3n+1$ continuous variables.
To recover its corners, write $c_i=\cos\theta_i$ and $d_i=\sin\theta_i$. The four
corners are

$$
(x_i,y_i)+\frac12\bigl(u(c_i,d_i)+v(-d_i,c_i)\bigr),
\qquad u,v\in\{-1,1\}.
$$

Place the container at $[0,S]^2$. A candidate packing must satisfy two kinds of
condition: every corner stays in the container, and every pair of squares has disjoint
interiors. Reducing $S$ leaves less room to satisfy these conditions together.
A picture can suggest that the conditions hold, but tiny overlaps or an inward-rounded
side can be invisible.
The search produces candidate poses; certification checks the geometric conditions at
the side actually claimed.

## From a Seed to a Certified Bound

The workflow has four jobs.
They can be separate programs, or loops inside one program.

| Job | Input and operation | Output |
| --- | --- | --- |
| Construct a seed | design a pattern, choose a random state, or transform an existing packing | a starting configuration, possibly infeasible |
| Explore | move far enough to reach different arrangements or local basins | promising candidates |
| Refine | reduce the side near a candidate, adjusting centres, angles, or contact equations | a numerical packing or stationary candidate |
| Certify | check unit shape, containment, and all pairwise non-overlap rigorously | a feasible witness and an upper bound |

A **seed** need not already be a packing.
Adding a square to a crowded arrangement, for example, can create overlaps that the
following search must resolve.
A successful seed supplies useful structure: orientations, rows, a tilted block, or
empty space where rearrangement can begin.

Fix a deterministic local refiner, including its settings.
The starting configurations it returns to one endpoint form a **basin** for that
refiner. Exploration tries to reach another basin; refinement tries to improve the
configuration it has reached.
If stronger refinement closes a gap to a record, it has exposed removable slack in the
candidate.
Repeated returns to an inferior endpoint justify trying other starts with that
refiner. They do not establish that all local improvement is exhausted: the refiner may
have held angles fixed, constrained squares to share an angle, or stopped at a tolerance
or budget limit.

One record can therefore have several contributors.
A finder discovers the arrangement; another optimizer reduces its side; a high-precision
solver removes numerical slack; and an independent checker establishes the upper bound.
David Ellsworth’s Kingbird site is a catalogue and refinement site, continuing Erich
Friedman’s earlier catalogue.
It is not the name of a single search algorithm.

## The Geometry a Search Has to Navigate

### Choosing a separating branch

Two convex squares have disjoint interiors exactly when a line weakly separates them.
The **separating-axis theorem** says that for convex polygons, it suffices to test axes
perpendicular to their edges.
Each square has two distinct edge normals, giving up to four axes for a pair; along each
axis there are two possible orders.

For a unit direction $\nu$, one order requires

$$
\max_{p\in Q_i}\langle\nu,p\rangle
\;\le\;
\min_{q\in Q_j}\langle\nu,q\rangle,
$$

where $Q_i$ and $Q_j$ are the two squares.
Only their corners need be tested.
Equality permits contact.
The pair is non-overlapping if *at least one* axis and order works.
That logical choice is a **disjunction**; one selected alternative is a **separating
branch**.

For an exact small example, take two axis-aligned squares.
The branch placing square 1 to the left of square 2 is

$$
x_1+\tfrac12\le x_2-\tfrac12,
\qquad\text{or equivalently}\qquad x_2-x_1\ge1.
$$

The centres $(1/2,1/2)$ and $(3/2,1/2)$ satisfy this with equality in a side-2
container. Placing one square above the other uses a different branch, $y_2-y_1\ge1$.
Both are valid constructions.
Restricting the search to horizontal separation excludes that stacked construction.

A **cell** selects one separating branch for every pair.
Cells can overlap: two squares far apart diagonally may satisfy both a horizontal and a
vertical branch. A cell describes separation choices for all pairs, including pairs that
never touch. A **contact graph** records only touching pairs, and so does not specify a
cell ([tutorial’s cell decomposition](../../../TUTORIAL.md#the-cell-decomposition)).

### Why fixing angles helps

With all angles fixed, every corner is its centre plus a constant offset.
Containment then consists of linear inequalities in $x_i,y_i,S$. Fix a separating branch
for each pair as well, and its axis is constant: the projection inequalities are linear
too. Minimizing $S$ under those restrictions is a **linear program**, or LP.

This isolates a tractable subproblem inside the larger search.
An LP can optimize centres and side for one choice of angles and branches.
The full problem still has to choose branches and move angles.
A change in which separation condition binds can also create a kink in the optimized
side as a function of angle.
Smooth optimization methods have to account for those changes.

Cells and basins refer to different objects.
A cell is a geometric restriction; a basin is defined by what a particular refiner does.
The refiner can change angles and separating branches along its route.
Its settings and tie-breaking rules affect the basins.
If endpoints are grouped by pattern or by a continuous family of poses instead of
identical coordinates, that grouping must be specified too.
Three squares in a side-2 container, for example, admit an exact sliding family: two
occupy the bottom row, and the centre of the top square moves from $(1/2,3/2)$ to
$(3/2,3/2)$. Different returned coordinates can belong to that same family
([tutorial’s basin discussion](../../../TUTORIAL.md#3-cells-basins-and-two-traps)).

## Constructing and Reusing Seeds

### Designing a parametric family

A hand construction chooses an arrangement before optimizing its dimensions.
Frits Göbel placed a diagonal strip of $45^\circ$ squares across an axis-aligned
background. Wider strips, rational-slope tilts, and an L-shaped border supplied related
counts. Trump’s eleven-square packing and Hämäläinen and Gustafson’s eighteen-square
constructions likewise reduce the search to a small geometric family.
The design specifies how pieces meet; algebra or one-dimensional optimization determines
a remaining angle
([historical survey](../../resources/web/friedman-ds7-survey-2009-html.md)).

Composition reuses a good packing as a block inside a larger one, or wraps an L-shaped
layer around it. Such constructions can produce exact, reproducible sides.
They rely on anticipating a useful pattern.
The $n=29$ arrangement found by Gensane and Ryckelynck uses six orientation classes,
illustrating the complexity that an unrestricted computer search can find beyond a
simple hand-designed family.

### Changing the count or replacing a component

**Packing surgery** transforms an existing arrangement into a seed, often changing which
pieces can touch.
The retained SQUISH publications distinguish operations by how the seed
is assembled, even though their later search and polishing are incompletely disclosed.

**Deletion and addition** connect neighboring counts.
Deleting pieces preserves feasibility at the old side and creates room for
rearrangement; adding pieces supplies a harder starting state.
SQUISH’s original release says nine of its ten original packings began from its own
neighboring certified packings this way, while $n=126$ began with nearby search from the
published record. A supplement added $n=153$. Later reports give explicit deletion
chains: $110\to108$ and $182\to180$ remove two squares, while $155\to154$ and
$239\to238$ remove one, followed by nearby search and polishing
([original release](../../resources/web/squish-401-2026-10-07/README.md);
[first update](../../resources/web/squish-401-update-2026-10-07/README.md);
[second update](../../resources/web/squish-422-second-update-2026-10-07/README.md)).

**Grafting** installs a useful subpacking in a target-count arrangement.
Reported lineages include Couzo $102\to123$, Couzo $105\to126$, and Kingbird $41\to88$.
For the last, the author says he replaced a component of the older $n=88$ record with
the $n=41$ packing improved in January 2026. The arrow names the seed component and the
resulting total count; it does not mean that 41 squares alone became 88. **Repeated
reuse** then carried SQUISH’s reported $n=88$ packing into $n=207$, $236$, and $302$
([source explanation](https://github.com/jlevy/squares/issues/422);
[retained second update](../../resources/web/squish-422-second-update-2026-10-07/README.md)).

**Carving** starts farther away in count.
The reported $297\to263$ construction carved down Couzo’s large packing, then used
nearby search and a final squeeze.
The squeeze tried roughly 120 random perturbations, at amplitudes $10^{-5}$ to $10^{-3}$
times the side, each followed by polishing.
It improved $n=263$ by about $4\times10^{-10}$; at the other eight counts, it found no
improvement above $10^{-11}$
([reported protocol](https://github.com/jlevy/squares/issues/422)).

These are author-reported lineages.
The packets do not disclose which squares were removed, graft interfaces, carving
decisions, or the optimizer behind nearby search and squeeze.
Francisco Couzo supplied many of the seeds: his September release contains 49 improved
packings, and his October 3 update improves seven of them.
He credited Claude assistance for the first $n=102$ and $103$ results, but the retained
publications specify no discovery algorithm.
Published coordinates and subsequent reuse establish available seeds; they do not reveal
how those seeds were found
([September packet](../../resources/web/franciscouzo-square-packing-2026-09-27/README.md);
[October update](../../resources/web/franciscouzo-square-packing-2026-10-03/README.md)).

## Moving Between Arrangements

Exploration needs a rule for proposing moves and deciding which to keep.
Methods called physical, billiard, or annealing can use quite different rules.

### Hard-particle motion and greedy billiards

In physical billiards, bodies travel between collision events.
A simulation predicts the next collision and updates velocities when it occurs.
Lubachevsky–Stillinger dynamics also grows the particles, making collisions
progressively more frequent as the packing densifies.
This has been effective for disks.
Rotating polygons make collision prediction much harder, because the equations involve
changing orientations as well as centre motion.
Two-dimensional compression can also favor ordered arrangements; for congruent squares
the axis-aligned grid is an obvious ordered state.
No freely rotating square record in this catalogue is attributed to
Lubachevsky–Stillinger dynamics
([retained simulation survey and primary references](../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md#2-growth-and-collision-lubachevsky-stillinger-inflation)).

Gensane and Ryckelynck’s 2005 square **billiard** instead tests proposed endpoints.
It grows congruent squares inside a fixed box.
If the common square side is $a$ in a unit box, rescaling gives unit squares in side
$1/a$; maximizing $a$ minimizes the final container side.

At fixed size, the algorithm chooses one square and proposes a random translation and
rotation of amplitude $\varepsilon$. It accepts the new pose only if it overlaps neither
another square’s interior nor the outside of the box.
It does not simulate the path between the old and new poses.
If this walk permits growth, it inflates the squares and doubles $\varepsilon$;
otherwise it halves $\varepsilon$. A second phase perturbs *every* square, recomputes an
admissible common size, and runs the billiard again.
It keeps the refined result only if it improves the previous one.

Thousands of random starts used $\varepsilon=0.1$ initially and $10^{-8}$ as the first
pass’s stopping threshold.
Collective perturbations then used a stopping threshold of $10^{-12}$. This is a greedy
stochastic walk with adaptive step size and collective shakes.
It produced the 2004 packings reported at $5.934342$ for $n=29$ and $6.603236$ for
$n=37$
([published pseudocode](../../resources/papers/gensane-ryckelynck-2005-improved-dense-packings.raw.md)).
The $n=29$ arrangement remained best known until Schadt’s December 2025 search
([catalogue history](../../resources/web/kingbird-squares-in-squares-compared-2026-08-22.md)).

### Forces from an optimization penalty

A physically inspired optimizer can instead allow temporary overlap, assign a cost to
it, and move squares in a direction that reduces that cost.
For a *schematic* example, let $\delta_{ij}$ be a chosen nonnegative overlap measure and
$w_i$ a wall-violation measure.
With positive penalty weights $\lambda$ and $\mu$, an objective could take the form

$$
E=S+\lambda\sum_{i<j}\delta_{ij}^2+\mu\sum_i w_i^2.
$$

The first term favors compression; the other terms oppose invalid poses.
Where the chosen functions are differentiable, their negative gradients with respect to
centres and angles determine translations and torques for a descent step.
A program might add damping, noise, or a schedule for the penalty weights.
Those are choices in an optimizer; calling its derivatives forces does not imply that it
simulates elastic collisions.
The formula here explains the mechanism and is not an attribution to any record
producer.

The surrogate objective needs care.
A finite penalty can trade overlap against a smaller side, so reducing $E$ does not by
itself produce a packing.
The gradient of a squared penalty also tends to zero as a smooth violation closes.
For rotating squares, changing the best separating branch introduces further nonsmooth
behavior. Exact geometric checking must follow any such search
([simulation survey](../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)).

### Annealing and basin hopping

**Simulated annealing** evaluates a proposal using an objective or energy.
It accepts favorable moves and sometimes accepts unfavorable ones.
A common schematic rule accepts a worsening $\Delta E>0$ with probability
$\exp(-\Delta E/T)$, where $T$ is the **temperature**. Cooling reduces that probability.
Temperature controls acceptance of worse objective values; the procedure need not
integrate physical trajectories.
The objective, proposal distribution, and cooling schedule all affect which arrangements
it reaches.

Thomas Schadt’s program found a new $n=29$ arrangement from randomness in December 2025
and later found the $n=51$ and $n=55$ structures.
His public $n=29$ packet says discovery used C++ `float`, followed by Boost
high-precision relaxation.
It does not publish the energy, proposal distribution, or cooling schedule, so the
schematic acceptance rule above should not be read as a reconstruction of that program
([Schadt packet](../../resources/web/schadt-s29-2025/README.md)).

Ellsworth modified Schadt’s annealer, ran parallel GPU searches, and then performed
analytic minimization.
The $n=51$ record was refound from randomness.
The $n=55$ breakthrough began from a cherry-picked state produced by Schadt’s
reimplementation of the Gensane–Ryckelynck search; Ellsworth later refound its basin
from randomness. These histories separate the seed’s contribution from the annealer and
refiner
([Kingbird comparison](../../resources/web/kingbird-squares-in-squares-compared-2026-08-22.md)).

Griffin Casson’s September 2026 pipeline ran 8,192 single-precision GPU chains for
twelve minutes on an RTX 3070, seeded from published records, with twelve CPU polishers.
Annealing supplied candidates; sequential linear programming refined them.
It found new arrangements at $n=106$ and $123$. Direct local refinement of published
records supplied another 37 reported numerical improvements
([first-party README](../../resources/web/casson-square-packing-2026-09-23/griffcass-square-packing/README.md)).

**Basin hopping** inserts local refinement into the exploration loop: perturb a locally
optimized pose, refine the perturbed pose, and apply an acceptance rule to the refined
outcome. Thus even a large raw perturbation can count as no escape if refinement returns
to the same endpoint.
Casson’s README names a CPU basin-hopping component, but its detailed document and
parameters are not retained.
SQUISH, short for “SQuare-packing Using Iterative Shrink-Hopping,” explicitly reports
basin hopping after seed transformations, followed by polishing.
Its published evidence does not disclose the objective, local optimizer,
square-selection rule, or hop schedule
([Casson README](../../resources/web/casson-square-packing-2026-09-23/griffcass-square-packing/README.md);
[original SQUISH submission](https://github.com/jlevy/squares/issues/401)).

Joost de Winter describes the 16 September 2026 $n=211$ result as full-packing adaptive
search, grouped-angle local refinement, and interval-verified decimal export.
This identifies the stages but not their detailed mechanics.
Sharing an angle among selected squares can reduce the nonlinear degrees of freedom; the
source does not specify how its groups were selected or constrained.
No code, adaptive schedule, or interval boxes were published
([retained packet](../../resources/web/de-winter-square-packing-211-2026-09-16/README.md)).

## Refining a Promising Arrangement

### Fixed-angle LP and angle refinement

A **fixed-angle LP** holds all angles and one separating branch per pair fixed, then
minimizes $S$ over centres and side.
The formulation is exactly linear.
A floating-point solver still has tolerances: its returned coordinates can slightly
violate an inequality.
Even an exact optimum solves only that chosen subproblem; other branches or other angles
may admit smaller sides.

This project’s **quench**, its local refiner, alternates two loops.
The inner loop reads separating branches from the pose, solves their fixed-angle LP,
then reads branches again from the result.
It repeats until the selected cell stabilizes, or reports that it stopped unsettled.
The outer loop brackets and minimizes angles shared by selected groups of squares.
An optional pass moves individual angles as well.
Angle refinement can improve a pose whose fixed-angle LP no longer improves
([quench description](../../../TUTORIAL.md#the-quench-map)).

**Sequential linear programming (SLP)** can instead let angles move inside each local
LP. Near the current pose, it replaces nonlinear angle-dependent constraints with their
first-order approximations.
It solves that linear subproblem, updates the pose, and builds another approximation.
Casson’s implementation uses HiGHS and moves each square’s centre and angle.
It polished both annealer outputs and slightly perturbed copies of catalogue records.
Even an exactly solved linearized subproblem can produce a pose that violates the
original nonlinear constraints, so the resulting geometry needs a feasibility check
([implementation description](../../resources/web/casson-square-packing-2026-09-23/griffcass-square-packing/README.md)).

The distinction is the variables in the LP. Fixed-angle LP has exact linear separation
constraints and moves centres and side.
Rotational SLP also moves angles, using a linear approximation to their nonlinear
effect. Both are local ingredients; neither searches all branch choices.

### Contact equations and analytic reconstruction

Near a settled arrangement, likely **contacts** identify equalities: a particular corner
touches a particular edge, or an edge or corner meets a wall.
Knowing only that two squares touch does not specify the equation.
A contact graph therefore needs geometric feature information before a solver can use
it.

Ellsworth writes contact equations, eliminates coordinates where possible, and adds
stationarity equations if the contacts leave freedom to change the side.
For example, suppose a reduced contact equation is $F(S,a)=0$, where $a$ is one angle
and $F_S=\partial F/\partial S\ne0$. Locally it defines $S$ as a function of $a$, with

$$
\frac{dS}{da}=-\frac{F_a}{F_S}.
$$

A stationary side along this smooth family therefore satisfies $F_a=0$. The contact
equation and derivative equation can be solved together.
With more variables, a **Jacobian** collects first derivatives; appending the side’s
gradient to the contact gradients gives rank conditions that Ellsworth expresses through
determinants
([analytic minimization notes](../../resources/web/kingbird-squares-in-squares-analytic-minimization.md)).

On a regular smooth contact family, **stationarity** means the side’s derivative
vanishes in every tangent direction.
A zero determinant alone can also arise from redundant or singular equations.
Stationary solutions can be maxima or saddles, and motions that open contacts or change
separating branches require separate analysis.
High-precision root finding supplies numerical candidates.
Integer-relation methods then seek small integer coefficients for a polynomial nearly
zero at the numerical side.
A rigorous algebraic reconstruction must identify the intended root and verify the
equations and every packing inequality
([tutorial’s reconstruction](../../../TUTORIAL.md#from-a-numeric-solution-to-an-exact-one)).

Evan Daniel’s October 2026 solver uses **Karush–Kuhn–Tucker (KKT) equations**. For a
smooth branch, write the pair and wall clearances as $g_k(q)\ge0$, where $q$ collects
the side, centres, and angles.
At a feasible pose the KKT conditions require multipliers $\lambda_k$ satisfying

$$
\nabla S=\sum_k\lambda_k\nabla g_k,\qquad
\lambda_k\ge0,\qquad \lambda_k g_k(q)=0.
$$

Here $\nabla$ is the vector of first derivatives with respect to $q$. The last equation
allows a nonzero multiplier only at a closed contact; a closed contact may still have
zero multiplier. The first equation balances the pressure to reduce $S$ against contact
forces and torques. Under suitable regularity conditions, KKT is necessary for a branch
minimum. Singular branches can require more general first-order conditions, and
satisfying KKT alone does not prove a minimum
([tutorial’s stationarity conditions](../../../TUTORIAL.md#contact-graphs-stationary-branches-and-rattlers)).

Daniel’s equilibrium LP identifies contacts that can carry force.
His solver projects the pose onto contact equations and takes high-precision Newton
steps in the KKT system: each step uses a linear approximation to correct the current
solution. Squares outside the force-bearing set are moved to gain clearance where
possible.

Corner-to-corner touches require additional care: the squares can separate along
different branches. Daniel sets these alternatives apart from the smooth contact
equations and tests first-order motions with a **mixed-integer model**, combining
continuous motions with discrete separating-branch choices.
His numerical checks also examine contact multipliers and second-order behavior.
Of 321 configurations with certificates, 315 passed the producer’s numerical
local-minimum checks.
These are numerical tests, not interval proofs of a KKT root or of local optimality.
Even a rigorous result for one smooth contact branch would leave other corner-contact
branches and better arrangements elsewhere to be addressed
([producer method and limitations](../../resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/README.md)).

## Turning Coordinates Into a Bound

A **witness** supplies the container side and every square’s pose.
A certificate adds the data and interpretation needed for a rigorous checker.
Discovery and high-precision refinement help make that witness, but feasibility can be
established without proving that its coordinates are the exact numerical optimum.

SQUISH stores a rational container side, rational centres, and a rational half-angle
parameter $t=\tan(\theta/2)$ for each square.
Define

$$
c=\frac{1-t^2}{1+t^2},\qquad d=\frac{2t}{1+t^2}.
$$

The identity $c^2+d^2=1$ holds exactly.
Thus $(c,d)$ and $(-d,c)$ are perpendicular unit directions, and the corner formula
gives an exact unit square.
A verifier can check every corner’s containment and every pair’s separation with
rational arithmetic, allowing boundary contact
([certificate explanation](../../resources/web/squish-401-2026-10-07/README.md)).

For a small exact example of the representation, take $t=1/3$, so $c=4/5$ and $d=3/5$.
Centre the square at $(7/10,7/10)$. Its corners, in cyclic order, are $(4/5,7/5)$,
$(7/5,3/5)$, $(3/5,0)$, and $(0,4/5)$. They lie in the side-$7/5$ box, and consecutive
corner differences have length one.
All of these statements are rational checks.
This illustrates certification of a pose; a single axis-aligned square already fits in
side 1.

For a full packing, the verifier checks the square count and unit shape, every wall
inequality, and non-overlap for every pair, whether by explicit separating-axis tests or
another rigorous geometric route.
Rigorous interval methods can instead enclose uncertain quantities and prove the
required inequalities over the enclosures.
A gap interval that straddles zero leaves that separation test undecided; a tighter
enclosure, another separating axis, or an exact contact identity may resolve it.
Every pair still needs a rigorous non-overlap decision.

Daniel first expands centres and container slightly while keeping the pieces unit size,
then rounds centres and half-angle parameters to rationals.
The added clearance permits exact verification without identifying the original optimum
as an algebraic number.
The upper bound is the side of the resulting certified packing, including enlargement
and rounding. A shorter decimal claimed as an upper bound must round the certified side
upward
([producer certificate construction](../../resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/README.md)).

This matters even when the source publishes many digits.
SQUISH’s second $n=263$ update prints $16.7404196795387747$, below its exact certificate
side. The safe sixteen-place ceiling is $16.7404196795387766$. The exact certificate
remains valid; the inward-rounded display does not itself follow as an upper bound
([retained exact side and displays](../../resources/web/squish-422-second-update-2026-10-07/README.md#exact-sides-and-displays)).

Three conclusions require different evidence:

| Conclusion | What must be established |
| --- | --- |
| Feasibility, hence an upper bound | the listed unit squares fit in the claimed side |
| Local optimality | no smaller-side packing exists in a specified neighborhood, including applicable contact branches |
| Global optimality | no smaller-side packing exists anywhere, usually by a matching lower bound |

A valid witness establishes the first.
A long decimal, equilibrium equations, or unsuccessful perturbation tests do not supply
the other two.

## Reading the Record

### Discovery gains and numerical gains

The releases below combine the four jobs in different ways.
Counts describe the release’s scope at publication, rather than the number of current
records.

| Publication | Producer and disclosed method | Scope and representative result |
| --- | --- | --- |
| 16 September 2026 | [Joost de Winter](../../resources/web/de-winter-square-packing-211-2026-09-16/README.md): author-reported adaptive full-packing search and grouped-angle refinement | a certified $n=211$ packing at side $14.99796070496771500150<15$ |
| 23 September 2026 | [Griffin Casson](../../resources/web/casson-square-packing-2026-09-23/griffcass-square-packing/README.md): GPU annealing and SLP, plus direct SLP on records | 39 reported improvements: two new arrangements, at $n=106,123$, and 37 local refinements |
| 23–27 September and 3 October 2026 | [Francisco Couzo](../../resources/web/franciscouzo-square-packing-2026-10-03/README.md): published configurations and revisions; discovery algorithm unspecified | 49 counts, then seven updated; October $n=208$ lowers the verified ceiling from $14.937018796984568$ to $14.926534459703512$ |
| 5 October 2026 | [Evan Daniel](../../resources/web/evand-square-packing-2026-10-05/README.md): contact/KKT refinement and rational certification; some inputs received an unpublished SLP squeeze first | 48 certified improvements of about $3.5\times10^{-13}$ to $5.0\times10^{-11}$, principally numerical slack removed from existing arrangements |
| 7 October 2026 UTC | [Nate Chaoweeraprasit, SQUISH](../../resources/web/squish-422-second-update-2026-10-07/README.md): author-reported neighbor-count seeds, basin hopping, grafting, carving, and polishing; exact certificates | 23 distinct counts across the original release, supplement, and two updates; second-update $n=108$ has verified ceiling $10.9099400734448775$ |

Casson’s 37 direct-refinement improvements have all since been superseded in this
repository’s frontier ([source coverage](../../frontier/source-coverage.yaml)). That
does not change their role as evidence that local optimization can expose slack in a
published arrangement.

SQUISH’s original $n=108$ ceiling was $10.9206589394033085$. Its second-update gain of
about $0.01072$ followed deletion of two squares from its $n=110$ packing and nearby
search. This exceeds the $10^{-10}$-scale final squeeze reported for $n=263$ by many
orders of magnitude.
Both $n=108$ configurations have confirmed feasibility; the producer supplies the
account of how the new seed reached the improved result
([original certificate](../../resources/web/squish-401-2026-10-07/README.md);
[second update](../../resources/web/squish-422-second-update-2026-10-07/README.md)).

### Rare hits and scoped failures

A basin can be rare under a particular search.
Ellsworth’s retained $n=51$ statistics classify 3,004 annealer outcomes: only four
refined to the record pattern.
The source estimates 4.917 GPU hours per hit on its tuned RTX 3080 Ti setup.
This measures that implementation’s sampling and refinement, rather than the geometric
volume of a basin or a portable cost for another search
([run statistics](../../resources/web/kingbird-run-statistics-2026/README.md)).

Negative experiments help distinguish missing exploration from weak refinement.
This repository’s fixed-side shrink-and-re-anneal attempts, using single-square moves,
failed to escape the grid.
Simultaneous all-square perturbations substantially improved $n=10$, $11$, $17$, and
$26$, but returned the grid unchanged at $n=29$, $37$, $50$, and $52$. An isotropic
spread penalty favored a round cloud rather than the square container and regressed
proved controls. Basin hopping over the LP quench improved ordinary test cells but
reached no record; it also exposed the need to repair floating-point LP outputs
monotonically before calling them packings
([retained experiments and discussion](../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md#9-what-this-repository-has-already-tried-in-this-direction)).

At the $n=11$ contact kink, the tested Powell and Nelder–Mead angle searches performed
worse than finite-difference descent.
That is a result about those tested angle optimizers, not an experiment on
differentiable simulation
([exp-006](../../campaign/series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)).
A failed search at declared settings and budget constrains a method claim; it does not
prove that a family of methods cannot work or that the incumbent packing is locally
optimal.

## Vocabulary and Further Reading

| Term | Meaning here |
| --- | --- |
| Pose | a square’s centre and orientation |
| Seed | the starting configuration supplied to a search |
| Separating branch | one axis and order that can establish a pair’s non-overlap |
| Cell | one separating branch selected for every pair |
| Contact graph | which pairs touch; feature-level equations require more information |
| Basin | starting configurations grouped by their endpoint under a specified refiner |
| Quench or polish | local refinement toward an endpoint |
| Surgery | a seed transformation such as deletion, addition, grafting, or carving |
| Witness | a container side and complete square poses |
| Certified upper bound | a side at which feasibility has been rigorously established |

A useful record names the finder, seed and parent count, exploration method, local
refiner, verifier, certified side, publication date, and source revision.
Missing fields remain unknown.
This preserves the distinction between a producer’s account of the search and
independently checked feasibility of its output.

The [tutorial](../../../TUTORIAL.md) develops the mathematical model, cell and basin
distinctions, exact reconstruction, and optimality proofs.
The [strategy catalogue](../../frontier/search-strategies.yaml) indexes search families
and their record histories; the [frontier register](../../frontier/README.md) records
bounds, evidence, and attribution by count.
The retained
[annealing survey](../../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md)
and
[simulation survey](../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
provide deeper mechanism comparisons and their source limitations.
For the other half of the problem,
[the lower-bound explainer]({{PAPER:n11-lower-bounds-explainer}}) shows how a
certificate can exclude every packing below a specified side.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
