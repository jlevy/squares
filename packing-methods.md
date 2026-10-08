# How Record Square Packings Are Found

*Evidence cutoff: 8 October 2026. The survey includes retained releases through 7
October 2026.*

Let $s(n)$ be the smallest side of a square that can contain $n$ unit squares, each free
to translate and rotate.
Their interiors must not overlap; edges and corners may touch.
A construction that fits in side $S$ proves the **upper bound** $s(n)\le S$. Finding a
smaller $S$ can involve several kinds of search before anyone has a packing whose
feasibility is established.

The useful division is into four jobs:

```text
transform or invent a seed
           ↓
explore configurations and local basins
           ↓
refine one promising pattern locally
           ↓
verify the resulting packing rigorously
```

One program can do several jobs, and several people can contribute to one record.
The finder may discover the arrangement, another optimizer may reduce its side, a third
program may convert it to high precision, and an independent checker may establish the
upper bound. Each contribution answers a different question about the record.

## Why the Search Is Hard

A pose for square $i$ consists of its centre $(x_i,y_i)$ and angle $\theta_i$; the
container contributes its side $S$. A search over $n$ squares thus has $3n+1$ continuous
variables. The awkward part is non-overlap.
Two squares have disjoint interiors exactly when a line weakly separates them.
It is enough to test directions perpendicular to an edge of either square: up to four
distinct axes, with two possible orders along each axis.
Along a chosen axis, every projected corner of one square must lie at or before every
projected corner of the other.
Equality allows contact.
Non-overlap is therefore a **disjunction**, a choice among alternatives: at least one of
these separating branches must hold for every pair.

A **cell** selects one branch per pair.
Cells can overlap, and a pair can have more than one valid separating branch without
touching. A cell therefore describes more than a contact graph, which records only which
squares touch. The [tutorial’s cell decomposition](TUTORIAL.md#the-cell-decomposition)
develops this geometry from first principles.

Once all angles and one separating branch per pair are fixed, containment and separation
are linear in the centres and $S$. A linear program can then optimize that one cell
within that restriction.
The global search still has to choose among an enormous number of cells and move the
angles.

A **basin** groups starting configurations that a chosen local refiner takes to the same
endpoint. If outcomes are grouped by a pattern or a continuous family of equally good
poses, that grouping must also be specified.
Basins depend on the refiner, including its angle moves and tie-breaking rules.
They are different from cells: a refiner can change separating branches along the way.

A record basin can be rare under a particular search.
For $n=51$, David Ellsworth’s retained run statistics classify 3,004 annealer outcomes:
only four refined to the record pattern, an estimated 4.917 GPU hours per hit on that
particular tuned RTX 3080 Ti setup.
These frequencies describe that implementation’s sampling and refinement; they do not
measure a basin’s geometric volume
([run statistics](packing/resources/web/kingbird-run-statistics-2026/README.md)).

## Geometry by Hand

A geometric construction begins by designing a contact pattern.
Frits Göbel placed a diagonal strip of $45^\circ$ squares across an axis-aligned
background. Wider strips, rational-slope tilts and an L-shaped border then generated
related counts. Walter Trump’s 1979 packing of eleven squares uses six axis-aligned
squares and five at one common angle near $40.18^\circ$. Hämäläinen and Gustafson’s
$n=18$ constructions use an angle with an exact trigonometric description.
These are small parametric families: a geometric design specifies how the pieces are
arranged, and algebra or one-dimensional optimization determines a remaining angle
([Friedman’s historical survey](packing/resources/web/friedman-ds7-survey-2009-html.md)).

Composition extends the idea.
A good packing can become a block inside a larger one, or an L-shaped layer can be
wrapped around it. Such constructions are reproducible and often yield exact sides.
Their weakness is also clear: the designer must anticipate the right contact pattern.
The $n=29$ arrangement eventually found by computer uses six orientation classes and is
difficult to invent on paper.

## Greedy Billiards and Inflation

Thierry Gensane and Philippe Ryckelynck supplied the first detailed computer search for
freely rotating squares.
Their 2005 algorithm grows congruent squares inside a fixed box.
Rescaling the final pieces to unit size turns a larger common square size into a smaller
container side. At a fixed square size it repeatedly chooses one square, proposes a
random translation and rotation of amplitude $\varepsilon$, and accepts the new pose
only if it overlaps neither the other squares’ interiors nor the outside of the box.
It checks the proposed pose, rather than simulating a physical path between poses.
If the walk permits a larger common square size, it inflates the squares and doubles
$\varepsilon$; otherwise it halves $\varepsilon$. A second phase perturbs *every*
square, recomputes an admissible common size and runs the billiard again.
It keeps the refined configuration only if it improves on the one before the shake.
Thousands of random starts used a first pass with $\varepsilon$ from $0.1$ down to
$10^{-8}$, followed by collective perturbations down to $10^{-12}$
([published pseudocode](packing/resources/papers/gensane-ryckelynck-2005-improved-dense-packings.raw.md)).

This is sometimes grouped under physics, but it is not thermal molecular dynamics and
has no temperature or Metropolis acceptance rule.
It is a greedy stochastic walk with adaptive step size and a collective shake.
It produced the 2004 $n=29$ bound $5.934342$ and $n=37$ bound $6.603236$, as well as
alternative versions of smaller packings.
The $n=29$ result stood until Thomas Schadt’s December 2025 search.

Lubachevsky–Stillinger dynamics grows hard particles between collision events and has
been effective for disks.
Rotating polygons make collision times much harder, and in two dimensions congruent
squares tend to crystallize into the axis-aligned grid.
No freely rotating square record in this catalogue is attributed to that method.
The retained
[simulation-mechanism survey](docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
collects the published obstructions and square-specific experiments.

## Simulated Annealing and Basin Hopping

Simulated annealing accepts favorable perturbations and sometimes accepts unfavorable
ones, with the latter probability falling as the temperature cools.
That controlled acceptance of worse objective values helps a search escape local traps.
Annealing produced several record arrangements in 2025–26. Thomas Schadt’s program found
a new $n=29$ arrangement from randomness in December 2025 and later found the $n=51$ and
$n=55$ structures.
His public $n=29$ packet says the discovery used C++ `float`, followed
by Boost high-precision relaxation; it does not publish the energy, proposal
distribution or cooling schedule
([Schadt packet](packing/resources/web/schadt-s29-2025/README.md)).

David Ellsworth modified Schadt’s annealer, ran massively parallel GPU searches and then
performed analytic minimization.
The provenance matters.
The $n=51$ record was refound from randomness.
The $n=55$ breakthrough began from a cherry-picked state made by Schadt’s
reimplementation of the Gensane–Ryckelynck search; later Ellsworth refound its basin
from randomness. These histories show that the seed and neighborhood can matter as much
as the cooling schedule
([Kingbird comparison](packing/resources/web/kingbird-squares-in-squares-compared-2026-08-22.md)).

Griffin Casson’s September 2026 project exposes a more explicit hybrid.
On an RTX 3070, it ran 8,192 single-precision GPU chains for twelve minutes, seeded from
published records, and assigned twelve CPU polishers.
The annealer supplied candidates; sequential linear programming (SLP) refined them.
That pipeline found new arrangements at $n=106$ and $123$. Running SLP directly on
published packings yielded 37 more numerical improvements, all since superseded in this
repository’s frontier
([first-party README](packing/resources/web/casson-square-packing-2026-09-23/griffcass-square-packing/README.md),
[coverage status](packing/frontier/source-coverage.yaml)).

Basin hopping alternates perturbation with local refinement: perturb a locally optimized
pose, optimize again, and apply an acceptance rule to the refined result.
The comparison uses the outcomes of local refinement, so a large raw displacement that
refines back to the same endpoint has not escaped its basin.
Casson’s retained README names a CPU basin-hopping implementation but does not retain
its detailed document or parameters.
It is therefore evidence for the component’s existence, not for a specific acceptance
schedule. SQUISH, whose name expands to “SQuare-packing Using Iterative Shrink-Hopping,”
explicitly reports basin hopping after seed transformations, followed by polishing
([original submission](https://github.com/jlevy/squares/issues/401)). Its public
evidence does not disclose its objective, local optimizer, square-selection rule or hop
schedule.

Joost de Winter gives a different concise description for the 16 September 2026 $n=211$
packing of side $14.99796070496771500150$: “full-packing adaptive search,” then
“grouped-angle local refinement,” then interval-verified decimal export.
This describes a search over the full configuration followed by refinement that groups
angles. Constraining selected squares to share an angle is one way to reduce the
nonlinear degrees of freedom, but the brief source description does not specify how the
groups were chosen or constrained.
No code, adaptive schedule or interval boxes were published, so finer mechanics remain
unknown
([retained source packet](packing/resources/web/de-winter-square-packing-211-2026-09-16/README.md)).

## Local Refinement: LP, SLP and Contacts

Local methods answer a narrower question: given a promising arrangement, how small can
this arrangement become?

A **fixed-angle LP** chooses a separating branch for every pair, holds all angles fixed,
and minimizes $S$ over the centres and side.
This is an exact linear formulation of the chosen subproblem; a floating-point LP solver
still has numerical tolerances.
A solver that reaches its optimum has minimized the side for those branches and fixed
angles. Other separating branches at the same angles may admit a smaller side.

This project’s **quench**, its local refiner, alternates an inner fixed-angle loop with
angle refinement. The inner loop solves a cell, selects separating branches again from
the result, and repeats to a fixed point.
The outer loop brackets and minimizes over angles shared by selected groups of squares.
Changing the angles can improve a configuration even after the fixed-angle LP has
stopped improving ([quench description](TUTORIAL.md#the-quench-map)).

**Sequential linear programming (SLP)** can move the angles in the local LP too.
At each iteration it replaces the nonlinear, angle-dependent face-separation constraints
by their first-order approximations near the current pose, solves that linear
subproblem, and updates the approximation.
Casson’s implementation used HiGHS and polished both annealer outputs and slightly
perturbed copies of catalogue records.
SLP can expose slack left by an earlier optimizer, but it remains local and its
linearized constraints require a feasibility check afterward.

Once likely contacts stabilize, a solver can turn the contact hypothesis into equations.
Knowing that two squares touch is insufficient: it must specify which corner meets which
edge, or which edge meets a wall.
Ellsworth writes these equations, eliminates coordinates where possible, and adds
Jacobian-determinant stationarity conditions when the contact equations alone leave
freedom to change the side.
Stationarity means the side has no first-order change along the allowed smooth contact
motions; it is a candidate condition for an extremum.
High-precision root finding locates a numerical solution, and integer-relation methods
can suggest a polynomial satisfied by its side.
An algebraic reconstruction must then identify the intended root and check its equations
and all packing inequalities rigorously
([analytic minimization](packing/resources/web/kingbird-squares-in-squares-analytic-minimization.md);
[tutorial’s exact reconstruction](TUTORIAL.md#from-a-numeric-solution-to-an-exact-one)).

Evan Daniel’s October 2026 solver reimplements analytic minimization with
**Karush–Kuhn–Tucker (KKT) equations**. These combine contact equalities with
stationarity: nonnegative contact multipliers, interpretable as forces, balance the
pressure to reduce the container side.
His equilibrium LP identifies contacts that can carry force.
The solver projects the pose onto contact equations and applies high-precision Newton
steps to the KKT system.
Squares outside the force-bearing contact set are moved to gain clearance where
possible. The contact model needs extra care at a corner-to-corner touch, where
separation can continue along different branches.
Daniel therefore tests these alternatives with a separate mixed-integer model of
first-order motions.

The October 5 batch gives 48 certified improvements of about $3.5\times10^{-13}$ to
$5.0\times10^{-11}$, principally by removing numerical slack from the same arrangements
([batch and comparison](packing/resources/web/evand-square-packing-2026-10-05/README.md)).
Of 321 configurations with certificates, 315 passed the producer’s numerical
local-minimum checks, including multiplier and second-order tests.
These computations supply evidence about the local structure; they are not interval
proofs of a KKT root or local optimality.
Even rigorously proving equilibrium on one smooth contact branch would not settle the
other corner-contact branches or exclude a better packing elsewhere
([producer method and limitations](packing/resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/README.md)).

## Packing Surgery and Reuse

Several recent records start from a packing at another count.
**Surgery** modifies an arrangement to supply a new seed, often changing which pieces
can touch. The published lineages distinguish several operations:

- **Deletion or addition** removes or adds squares to make a seed at a neighboring
  count. The original SQUISH release says nine of its ten original packings began with
  its own neighboring certified packings this way; $n=126$ began with nearby search from
  the published record.
  A later supplement added $n=153$
  ([original release](packing/resources/web/squish-401-2026-10-07/README.md)). Later
  reports give concrete chains: $110\to108$ and $182\to180$ delete two squares, while
  $155\to154$ and $239\to238$ delete one, followed by nearby search and polishing.
- **Grafting** installs a useful subpacking inside a target-count arrangement.
  Reported examples include Couzo $102\to123$, Couzo $105\to126$, and Kingbird
  $41\to88$. In the last example, the author says he replaced a component of the older
  $n=88$ record with the $n=41$ packing improved in January 2026
  ([source explanation](https://github.com/jlevy/squares/issues/422)).
- **Repeated reuse** carries a successful construction into several larger ones.
  SQUISH’s reported $n=88$ packing was then grafted into $n=207$, $236$ and $302$.
- **Carving** starts much farther away in count.
  The reported $297\to263$ construction carved down Couzo’s large packing, then applied
  nearby search and a squeeze.
  The source’s final **squeeze** tries roughly 120 random perturbations at amplitudes
  $10^{-5}$ to $10^{-3}$ times the side, each followed by polishing.
  This improved $n=263$ by about $4\times10^{-10}$; at the other eight counts it found
  no improvement above $10^{-11}$
  ([reported squeeze protocol](https://github.com/jlevy/squares/issues/422)). The local
  optimizer itself is unpublished, and a failed perturbation test is not a proof of
  local optimality.

These lineages are author-reported in the
[first SQUISH update](packing/resources/web/squish-401-update-2026-10-07/README.md) and
[second update](packing/resources/web/squish-422-second-update-2026-10-07/README.md).
The packets do not reveal which squares were removed, the graft interface, the exact
carving decisions or the optimizer behind “nearby search” and “squeeze.”
Francisco Couzo’s packings supply many seeds in these chains.
His September release contains 49 improved packings, and his October 3 update improves
seven of them.
He credited Claude assistance for the first $n=102$ and $103$ results, but
the retained publications specify no search algorithm.
Neither the coordinates nor the later use of those coordinates as surgery seeds tells us
how he found them
([September packet](packing/resources/web/franciscouzo-square-packing-2026-09-27/README.md);
[October update](packing/resources/web/franciscouzo-square-packing-2026-10-03/README.md)).

## Recent Releases Compared

These dated releases illustrate different combinations of discovery, reuse and
refinement. Counts describe each release’s scope, not the number of current records.

| Publication | Producer | Method evidence | Scope and representative result |
| --- | --- | --- | --- |
| 16 September 2026 | [Joost de Winter](packing/resources/web/de-winter-square-packing-211-2026-09-16/README.md) | author-reported full-packing adaptive search and grouped-angle refinement; algorithm unpublished | a certified $n=211$ packing at side $14.99796070496771500150<15$ |
| 23 September 2026 | [Griffin Casson](packing/resources/web/casson-square-packing-2026-09-23/griffcass-square-packing/README.md) | GPU annealing followed by SLP, and SLP applied directly to existing records | 39 reported improvements: two new arrangements, at $n=106,123$, and 37 local refinements |
| 23–27 September and 3 October 2026 | [Francisco Couzo](packing/resources/web/franciscouzo-square-packing-2026-10-03/README.md) | configurations and revision history published; discovery algorithm unspecified | 49 counts, then seven updated; the October $n=208$ verified ceiling falls from $14.937018796984568$ to $14.926534459703512$ |
| 5 October 2026 | [Evan Daniel](packing/resources/web/evand-square-packing-2026-10-05/README.md) | published contact/KKT solver followed by exact rational certification; some inputs first received an unpublished SLP squeeze | 48 strictly smaller certified sides for existing arrangements, typically at the $10^{-13}$ to $10^{-11}$ scale |
| 7 October 2026 UTC | [Nate Chaoweeraprasit, SQUISH](packing/resources/web/squish-422-second-update-2026-10-07/README.md) | author-reported neighbor-count seeds, basin hopping, grafting, carving and polishing; exact certificates published | 23 distinct counts across the original release, supplement and two updates; second-update $n=108$ has verified ceiling $10.9099400734448775$ |

The original SQUISH $n=108$ ceiling was $10.9206589394033085$. Its second-update
improvement of about $0.01072$ follows deletion of two squares from the author’s $n=110$
packing and nearby search.
This is much larger than the final squeeze improvements reported above.
Both configurations have confirmed feasibility; the producer’s account supplies the
search lineage
([original certificate](packing/resources/web/squish-401-2026-10-07/README.md);
[second update](packing/resources/web/squish-422-second-update-2026-10-07/README.md)).

## What Each Method Establishes

| Stage | Typical mechanism | What it can establish |
| --- | --- | --- |
| Seed transformation | hand construction, deletion, addition, grafting, carving | a proposed arrangement or starting configuration |
| Exploration | greedy billiard, annealing, basin hopping, adaptive full-packing search | candidates that may reach different basins |
| Refinement | fixed-angle LP, SLP, angle bracketing, squeeze, contact/KKT solve | numerical improvement or stationarity evidence for a local structure |
| Certification | exact arithmetic or rigorous interval enclosures | feasibility, hence an upper bound, when every required geometric condition is checked |

Certification is logically separate from discovery.
A **witness** gives the container side and every square’s pose.
SQUISH stores rational $(x,y,t)$, with $t=\tan(\theta/2)$, and defines

$$
c=\frac{1-t^2}{1+t^2},\qquad d=\frac{2t}{1+t^2}.
$$

The identity $c^2+d^2=1$ holds exactly, so $(c,d)$ and $(-d,c)$ are perpendicular unit
directions. Together with the rational centre, they specify an exact unit square.
A verifier can check containment at every corner and separation for every pair using
rational arithmetic, allowing boundary contact
([certificate explanation](packing/resources/web/squish-401-2026-10-07/README.md)).

Daniel’s producer first expands the centres and container slightly while keeping the
pieces unit size, then rounds centres and half-angle parameters to rationals.
The resulting clearance makes exact verification possible without identifying the
numerical optimum as an algebraic number.
The side actually certified, including any enlargement and rounding, is the upper bound;
a decimal display must round that side upward.

These checks prove that the listed squares fit.
A **local-optimality** proof would additionally exclude smaller-side packings in a
specified neighborhood, including every applicable contact branch.
A **global-optimality** proof would exclude them everywhere, usually by establishing a
matching lower bound.
Neither conclusion follows from a valid witness, a long decimal, or the failure of
another search to improve it.

## Negative Experiments That Changed the Search

This repository’s experiments reinforce the published history.
Fixed-side shrink-and-re-anneal with only single-square moves could not escape the
jammed grid. Adding simultaneous all-square perturbations greatly improved $n=10$, $11$,
$17$ and $26$, but still returned the grid unchanged at $n=29$, $37$, $50$ and $52$. An
isotropic spread penalty optimized a round cloud rather than a square container and
regressed proved controls.
Basin hopping over the LP quench improved ordinary test cells but came nowhere near a
record; it also exposed the need to repair floating-point LP solutions monotonically
before calling them packings.
Differentiable simulation at the $n=11$ contact kink performed worse than plain descent.
These are scoped negative results, not impossibility theorems
([simulation-mechanism survey](docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)).

## Provenance and Further Reading

A useful record should name at least: the finder; the seed packing and any parent count;
the exploration method; the local refiner; the verifier; the certified side; the date;
and the source revision.
Missing fields should remain unknown.
Kingbird is David Ellsworth’s catalogue and refinement site, continuing Erich Friedman’s
earlier catalogue; it is not the name of one solver.

For the mathematical model and the distinction between upper bounds, stationarity and
optimality, continue with the [tutorial](TUTORIAL.md).
For an indexed list of search families and their record history, see the
[strategy catalogue](packing/frontier/search-strategies.yaml).
The [frontier register](packing/frontier/README.md) records the current bound, evidence
and attribution for each count.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
