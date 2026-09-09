# Research: Physics and Simulation Mechanisms for Square Packing

**Date:** 2026-09-09

**Author:** Joshua Levy, with Claude Opus 5 assistance

**Status:** Complete for the question asked.

## Overview

[The annealing survey](research-2026-09-08-annealing-for-square-packing.md) covered
stochastic search over an objective.
This one covers the other family: mechanisms that move bodies under a simulated physical
or geometric rule. Inflation among collisions, containers that deform, overlap resolved
by projection, rigid-body solvers with exact non-penetration, smoothed penalties with an
annealed smoothing parameter, and differentiable simulation used as an optimiser.

The short answer has three parts.

**The mechanism most people would reach for first is the one that cannot work here.**
Lubachevsky-Stillinger inflation grows particles among elastic collisions until jamming,
and it shares a name with the billiard entry this repository’s own catalogue credits
with two square records.
The two are not the same algorithm, and the catalogue now says so: Graham and
Lubachevsky’s disk billiard is this mechanism run inside hard walls, while Gensane and
Ryckelynck’s square billiard is an adaptive-step random walk that deliberately never
computes a collision direction.
It does not port to squares, for three independent reasons, any one of which is
sufficient: the collision time under rotation is transcendental rather than quadratic,
and the people who built the fast collision predictors say so in as many words; the only
published non-spherical generalisation restricts itself to shapes with continuously
differentiable overlap potentials, and the family that approaches a square was abandoned
by its own authors before reaching it, for numerical reasons; and in two dimensions the
protocol crystallises, which for congruent squares means it converges to the trivial
grid this repository already cannot escape.
The distinction that saves the idea is that **Gensane and Ryckelynck’s inflation factor
for two rotated squares is closed form while the collision time is not**, and those are
different objects. The route to squares runs through the first.

**The mechanism with the best evidence is the one nobody in this field talks about.**
Divide and concur, searched with relaxed-reflect-reflect, is a constraint-projection
method that needs no potential, no derivative and no smoothness.
It was run cold on the sibling problem across 197 values of `n`, up to 400 random starts
each, with no information used beyond the target densities.
It reached the best-known diameter within `1e-9` on 143 of them and **beat the best
known on 38**. Separately, and in a different paper, the same framework produced new
densest packings of non-spherical bodies with the container’s own parameters optimised
alongside the particles.
The two halves have never been joined, and squares in a square sits exactly between
them.

**And there is one head-to-head between the two families.** A shrinking-cell method
solved by linear programming was compared against Lubachevsky-Stillinger at matched
density, and beat it from 1.5 hours to 10 minutes in three dimensions and from 193.5
hours to 8.3 hours in six, while reaching the densest known in dimensions two through
six where the inflation runs reached it only in two and three.

Underneath all of this sit five properties of this problem, four of them measured here.
The objective is a maximum attained by two to four squares, so at the grid no
single-square move lowers it at all.
The container has no slack at any record, at most `3.7e-33` over 318 of them.
A contact at a record is exactly zero while the nearest non-contact is `1.2e-2` away, so
the tolerance question has a 97-decade answer.
And **the packings a cold search is being asked to find are mostly not jammed**: of the
36 non-grid best-knowns at `n <= 100`, 34 are screened and 30 of those have at least one
square that can be translated.
A mechanism whose termination rule is “stop when nothing can move” is not describing its
own targets, and every recommendation below has to say what it does about that.

## Questions to Answer

1. What does each physics-style mechanism actually do, and has any of them been run on
   squares rather than on disks and spheres?
2. Which of them could plausibly recover a best-known packing for a non-grid `n < 100`
   from a cold start, and what would each need to be set up correctly?
3. What are the settings, in numbers: inflation rate, restart policy, damping, the
   smoothing schedule, the tolerance at which a jam is declared?
4. Which are dead ends here, and what makes them dead ends rather than merely untried?
5. What does this repository’s own geometry say about the mechanisms before any of them
   is run?

## Scope

Included: mechanisms that move bodies under a simulated physical or geometric rule
rather than sampling an objective, applied to packing congruent squares under free
rotation in a minimal square container.
Growth and collision, container deformation, constraint projection, non-smooth contact
solvers, smoothed penalties with continuation, and differentiable simulation.

Excluded: the stochastic-search family, which
[the annealing survey](research-2026-09-08-annealing-for-square-packing.md) covers, and
which this document does not repeat.
Simulated annealing, basin hopping, threshold accepting, replica exchange over a
pressure ladder, iterated tabu search and perturbation-based thresholding search are all
there, with their sources retained.
Also excluded: lower bounds and optimality proofs, and exact algebraic promotion of a
numerical packing.

Claims below are separated three ways, as in the survey this one extends.
**Published** means a source with a URL and a date states it.
**Measured here** means this repository ran it and recorded it.
**Inference** means it is the author’s reasoning over the other two, and is marked.

## 1. Five Properties of This Problem That Decide Every Mechanism Below

Each mechanism in sections 2 to 8 is judged against these five.
They are stated first because four of them are measurements this repository already
holds, and because every dead end in section 11 is a mechanism colliding with one of
them.

### 1.1 The objective is a maximum attained by two to four squares

`required_side(c) = max(hix - lox, hiy - loy)` (`packing/sqsearch/src/geom.rs`), so only
the squares attaining the extremes of the binding span can reduce it.
**Measured here**, exp-134: at the trivial grid, over 8,000 proposals per kind per cell
at scales `0.01`, `0.05` and `0.2` alike, **no single-square proposal lowers the
objective at all** for any tested cell except `n = 5`, while a quarter to a third of
proposals change it and every one of those raises it.
Off the grid the picture inverts: on the engine’s own emitted `n = 18` states at side
`4.84`, `3.5` per cent of single-square proposals lower the side.

The sparsity is a property of the *starting configuration*, not of the objective.
That is the single most useful thing to carry into a discussion of physics mechanisms,
because a physical rule that only ever moves one body at a time inherits the same
plateau, and a physical rule whose container is a degree of freedom does not.

### 1.2 The best-known packings are, with four exceptions, not jammed

Every inflation, compression and event-driven method in the physics literature stops at
a *jam*: it grows the particles until nothing can move.
Whether that rule can emit a best-known square packing is a question about the targets.

**Measured here, 2026-09-09**, by `packing/devtools/screen_jamming_targets.py`, which
joins
[`translation-escape-screen.json`](../../../packing/atlas/known-best/translation-escape-screen.json)
against the 100 frontier case files:

| Of the 36 non-grid best-known packings at `n <= 100` | count |
| --- | ---: |
| Screened (`n = 68, 69` excluded by the shape-residual limit) | 34 |
| With at least one square the screen can translate | 30 |
| Movable squares in those, out of 1,723 screened | 232 |
| Of those, squares that can be pushed clear of everything they touch | 76 |
| With no movable square at all | 4 (`n = 5, 11, 28, 40`) |

Read the two square counts as bounds rather than as one number.
The screen’s own note is that every square in every retained record touches something,
so a movable square usually slides tangentially with a contact staying closed rather
than floating in a hole; the 76 that separate are the ones that genuinely float.

**Inference.** A termination rule of the form “stop when no particle can move” does not
describe 30 of these 34 targets.
That is not fatal, because the loose squares carry no objective: the container side is
set by the jammed backbone, and a rattler can sit anywhere inside its cage without
changing the answer.
It is a specification requirement, and a precise one.
A jam test has to be run on the backbone with the free squares removed, and the free set
has to be recomputed as the configuration changes, because the count is not small: 27 of
the 66 squares at `n = 66`, 17 of 87 at `n = 87`, 13 of 39 and 13 of 51. An
implementation that declares a jam only when every square is immobile will run forever
on most of the cases it is being asked to find.

The physics literature has both the vocabulary and the practice for this, which is worth
saying because it means the requirement is normal rather than exotic.
Torquato and Jiao’s comparison table reports the “fraction of rattlers, i.e., movable
particles caged by their jamming neighbors” beside every density, at `0.028` in three
dimensions falling to `0.005` in six; and Maher, Stillinger and Torquato’s
contact-generation criterion is stated on “the interparticle distances (excluding
rattlers)”. The comparable figure here is the 76 squares that can be pushed clear, `4.4`
per cent of the 1,723 screened, which sits in the same range as those rattler fractions.
The looser 232, at `13.5` per cent, counts squares that slide along a contact and would
not be called rattlers in that literature at all.

### 1.3 The container has no slack anywhere in the corpus

**Measured here**, over the 318 screened records and 52,064 squares of the same screen:
the largest absolute container slack anywhere is `3.7485e-33`, at `n = 11`. No retained
packing has room to spare inside its own reported side.
Two consequences follow and both matter below.
A settle that grows the container side has overlapped something, so the side is a
one-sided check on any physical relaxation.
And there is no margin to relax into: the objective and the feasibility boundary are the
same surface, which is why every method that treats overlap as a soft penalty is
optimising a problem whose optimum sits exactly on the constraint.

### 1.4 A square has three degrees of freedom and no analytic overlap potential

The separating-axis distance between two squares is piecewise smooth, with a kink
wherever the active axis changes, and the objective inherits it.
**Measured here**, exp-006 and H-019: walking the shared `n = 11` tilt off its optimum
gives a response that is linear on both sides with slopes `0.175` and `0.384`, so the
objective has a corner at the optimum where the active contact set changes; finite-
difference descent stalls five orders short there, and Powell and Nelder-Mead both did
worse than plain descent.

**Inference.** Two mechanism families are ruled on by this alone.
Anything that requires a smooth or twice-differentiable overlap function is modelling
something this problem does not have, at exactly the configurations that matter.
And anything that requires a closed-form collision time is asking for the root of a
transcendental system rather than of a quadratic, because a growing square’s contact
condition involves its rotation angle.

### 1.5 The tolerance at which a contact is declared is measurable, and it is wide

Every mechanism below has to decide, numerically, when two squares are touching.
The repository holds the two records whose contact structure has been extracted exactly
(`packing/atlas/known-best/contact-structures.json`), and they answer the question
directly.

| record | pair contacts | wall incidences | total incidences | unknowns (`3n + 1`) |
| --- | ---: | ---: | ---: | ---: |
| `n = 11`, Trump | 14 | 20 | 34 | 34 |
| `n = 29`, Schadt and Ellsworth | 52 | 37 | 89 | 88 |

The `n = 29` entry also records the separation of scales: **the worst contact margin is
`3.65694e-100` and the smallest strict separation is `0.0116001`, which the artifact
notes are 97.5 decades apart.**

**Inference, and it is the most directly usable number in this section.** At a record, a
contact is exactly zero and the nearest thing that is not a contact is `1.2e-2` away.
Any tolerance in the enormous band between them classifies every incidence correctly, so
the contact tolerance is not a tuning problem at a converged configuration; it becomes
one only away from a record, where the margins are not exactly zero and the two
populations are not separated.
The incidence counts say the second half of the same thing: a record’s contact network
sits at or one above the isostatic count, so a jam test that compares contacts against
degrees of freedom has a sharp target, provided the free squares of section 1.2 are
taken out of both sides of the comparison first.

## 2. Growth and Collision: Lubachevsky-Stillinger Inflation

### 2.1 What the algorithm is

**Published.** Boris Lubachevsky, *How to Simulate Billiards and Similar Systems*,
Journal of Computational Physics 94:255-283, 1991
([arXiv:cond-mat/0503627](https://arxiv.org/abs/cond-mat/0503627), retained at
`packing/resources/papers/lubachevsky-1991-how-to-simulate-billiards.pdf`), section 9.
Place `N` points in a periodic box with random velocities.
Let the diameters grow as `D(t) = a t` and run the billiard exactly, event by event.
Two things change relative to a fixed-diameter billiard.
The collision time solves `|p + v t|^2 = (a t)^2` rather than `|p + v t|^2 = D^2`, which
is still a quadratic in `t`; and the post-collision normal velocity components must be
*increased*, by an additive velocity larger than `a / 2`, so that growing disks neither
overlap nor stick. Energy is therefore not conserved, the system heats, and the
implementation periodically projects all positions to a common time and rebalances the
velocities to zero total momentum.
Cost is `O(log N)` per event, and the paper reports 150 to 450 collisions per second on
the hardware of its day, independent of `N`, using a 40 by 40 sector grid to cut the
neighbour candidates for 2,000 disks from about 16,000 to about 10.

The **inflation rate is the algorithm’s one important parameter**, and the literature is
specific about it. Skoge, Donev, Stillinger and Torquato, *Packing Hyperspheres in
High-Dimensional Euclidean Spaces*
([arXiv:cond-mat/0608362](https://arxiv.org/abs/cond-mat/0608362), 2006, retained)
define `gamma = dD/dt` and publish a staged schedule keyed to the reduced pressure
`p = PV / (N k_B T)`: `gamma = 1e-2` until `p = 10`, then `1e-3` until `p = 1e4`, then
`1e-4` until `p = 1e6`, then `1e-5` until `p = 1e12`. **Jamming is declared at
`p > 1e12`.** Equilibrium studies use `gamma` from `1e-5` to `1e-9`, and the sensitivity
is real: in four dimensions `gamma = 1e-8` gives a jamming fraction of `0.511`, while
`gamma = 1e-9` reproduces the `D4` lattice to twelve significant figures.
The public `packing-generation` implementation states the same recipe operationally: run
until the non-equilibrium reduced pressure is high enough, “e.g., a conventional value
of `1e12`”, then halve the compression rate and repeat until the rate falls below
`1e-4`.

The rate-to-density relation is the reason anyone tunes it.
Torquato and Stillinger’s review (*Jammed Hard-Particle Packings: From Kepler to Bernal
and Beyond*, [arXiv:1008.2982](https://arxiv.org/abs/1008.2982), 2010, retained) records
that the fastest growth gives about `0.64`, the maximally random jammed value, and that
slowing the growth raises the fraction continuously toward `0.74048`, with order rising
monotonically as it does.

### 2.2 In two dimensions it crystallises, which is this problem’s failure mode

**Published, and it is the single most relevant sentence Lane A found.** The same review
states that the protocol which yields a disordered jammed state in three dimensions
“typically yields a highly crystalline collectively jammed packing in two dimensions”,
and its figure 8 shows 1,000 disks driven at a *fast* expansion rate reaching about
`0.88` in a crystalline arrangement.

**Inference.** In two dimensions, inflation among elastic collisions has an ordered
attractor, and it reaches it even when driven hard.
For congruent squares in a square container the ordered attractor is the axis-aligned
grid. That is the same basin `sqsearch` cannot leave (section 1.1), reached by a
completely different mechanism, and it is a reason to expect an inflation method to
*confirm* the grid rather than to escape it.
It is also independent corroboration of the first-hand statement in section 2.4 below.

### 2.3 The non-spherical extension exists, and it stops before a square

**Published.** Donev, Torquato and Stillinger, *Neighbor List Collision-Driven Molecular
Dynamics Simulation for Nonspherical Hard Particles*
([arXiv:physics/0405089](https://arxiv.org/abs/physics/0405089), 2005, retained) is the
generalisation, and it states its own scope twice.
It is tailored “for smooth particles for which it is possible to introduce and easily
evaluate continuously differentiable overlap potentials”, and its conclusion offers “any
shape for which a smooth overlap potential can be constructed and easily
differentiated”. It also assumes a spherically symmetric moment of inertia so that
angular velocities are constant between collisions.
Its working tolerances: a collision-search tolerance typically `1e-4` to `1e-3`, with
contacts reproduced to `1e-12`. Two limitations it states are worth carrying.
The rigorous Lipschitz-bound argument that works for needles could not be generalised to
ellipsoids, so even there the interval search is heuristic; and the method is
“inherently non-parallelizable due to its sequential processing of the events”.

The closest anyone has come to a square along this line is the superdisk family
`|x|^{2p} + |y|^{2p} <= 1`, which is a circle at `p = 1` and a square as `p` grows.
Jiao, Stillinger and Torquato ([arXiv:1001.0423](https://arxiv.org/abs/1001.0423), 2010,
retained) ran the collision-driven algorithm on it with expansion rates in `(0.1, 0.5)`,
described as the largest initially feasible, noting that larger rates cause numerical
instability and that `gamma` around `0.05` suffices for ellipsoids.
Their jamming criterion is a diverging collision rate with the density at a local
maximum, verified by an infinitesimal shrinkage.
And their stated range is `p` from `0.85` to `3.0`, “since extreme values of `p`
associated with polyhedron-like shapes present numerical difficulties”, with an explicit
statement that they could not study the limits `p -> 0.5` and `p -> ∞`.

**The direct verdict on squares.** Klement, Lee, Anderson and Engel
([arXiv:2104.06829](https://arxiv.org/abs/2104.06829), 2021, retained) say it without
hedging: event-driven molecular dynamics for anisotropic particles “requires solving
collision equations that involve rotations and thus trigonometric functions”, whose
solution “is only possible numerically by iteration with approximations and is
necessarily slow”. Their own fast collision predictor works precisely because the
polyhedra do not rotate: “the detail that the polyhedra are non-rotating is crucial.
It means the underlying equations do not contain trigonometric functions and can be
solved analytically.”
Rotation is handled by separate Monte Carlo trial moves.
The one square case that *is* solved and shipped is the non-rotating one: Hoover, Hoover
and Bannerman ([arXiv:0905.0293](https://arxiv.org/abs/0905.0293), 2009, retained) do
event-driven molecular dynamics of hard parallel squares and cubes, and DynamO
implements it in `src/dynamo/dynamo/interactions/parallelcubes.cpp` with no orientation
state at all.

### 2.4 The distinction that decides this: the inflation factor is analytic, the collision time is not

**Published.** Gensane and Ryckelynck’s 2005 square paper, already retained here, gives
the homothety factor at which two rotated squares first touch **in closed form** (its
Proposition 1, a maximum of two expressions built from a per-corner minimum), along with
a closed-form confinement factor against the container walls.

**Inference, and it is the sharpest point in this section.** The primitive an inflation
*search* needs for squares is analytic and cheap: given a configuration, how far can
everything grow before something touches.
The primitive an event-driven *dynamics* needs is a collision time under rotation, and
that one does not exist in closed form.
These are different objects and the literature’s habit of calling both “inflation”
conflates them. The route to squares runs through the first and not the second.

The 2024 state of the art on non-spherical two-dimensional packings agrees.
Hoy ([arXiv:2409.19196](https://arxiv.org/abs/2409.19196), retained) generates the
densest known disordered jammed ellipse packings with what the abstract calls a
“Lubachevsky-Stillinger-like growth algorithm”, and it is **not** event driven.
Each cycle is: a random translation and rotation of every particle at magnitudes
`0.05 f` and `16 f / alpha` degrees; a growth of every particle by the single factor
that brings one pair into tangential contact; a biased swap; and a capped per-particle
growth step.
`N = 1000`, `f` starts at 1 and is multiplied by `3/4` after 100 consecutive
cycles whose growth factor is below `1e-10`, terminating jammed at `f < 2e-8`, which the
paper gives as the double-precision floor.
It lands within `0.5` per cent of the ellipse crystal for aspect ratios between about
`1.25` and `1.4`.

**Inference.** Steps one and two of that cycle are Gensane’s random walking plus his
inflation factor, under a different name.
The record-setting two-dimensional non-spherical protocol of 2024 is discrete
grow-to-first-contact, not continuous-time dynamics.

### 2.5 Billiard algorithms, and the only published cost per improved configuration

**Published.** Graham and Lubachevsky’s disk-record work describes the billiard exactly
as inflation with hard walls: the disks “move chaotically in the square without overlaps
while their diameter increases at a common rate until no further growth is possible”
(*Repeated Patterns of Dense Packings of Equal Disks in a Square*,
[arXiv:math/0406394](https://arxiv.org/abs/math/0406394), 1996, retained).

Boll, Donovan, Graham and Lubachevsky, *Improving Dense Packings of Equal Disks in a
Square* ([arXiv:math/0405310](https://arxiv.org/abs/math/0405310), 2000, retained), give
the number this document was asked for.
**The billiard alone needed more than 1,000 attempts to find the record 32-disk packing
and more than 5,000 for 37 disks.** Their two-phase replacement, a perturbation phase
followed by a billiard finaliser, needed under 30 attempts for 32 disks and under 100
for 37, which they describe as taking the work from months of computing to a few hours.
**Their phase one is fully specified and is the part that ports to squares unchanged**,
because it schedules a *step size* rather than a potential.
Scatter the disks at random in an oversized square, each with an initial direction
toward the origin; compute the smallest axis-parallel bounding square centred at the
origin; set the move step to `s_0 = 0.25`; and loop while `s > 1e-10`, sweeping the
disks in a random order and attempting a move of distance `s` each time.
A move attempt tries the current direction, and on collision resets the direction to the
**sum of repelling vectors over the obstacles reachable within a straight motion of
length `s`**, then tries once more.
An impatience counter increments whenever the bounding square fails to shrink; when it
passes `1000`, or when a whole sweep fails, the step shrinks by `q = 0.43` and the
counter resets. The records this set are `n = 32, 37, 48, 50` disks in a square.
Their rigidity probe is worth stealing too: rotate the phase-one configuration by 90
degrees before phase two and confirm the answer comes back as the corresponding rotation
with identical bonds.

Their precision economics are also published: the billiard delivers more than 13 digits
in double precision while phase one stalls at about 10, and “each next digit of
precision takes roughly several times more computing time than the previous digit”,
which is why the billiard is retained purely as a finisher.
Their bond identification after phase two has a six-order gap: bonds below `1e-11` of
the diameter and every other distance above `1e-5`, which is the disk analogue of the
`1e-100` against `1.2e-2` separation this repository measured at `n = 29` (section 1.5).

**And here is Gensane and Ryckelynck’s own account of the failure mode on squares**,
read from the retained PDF. Their production run is `BilliardOfSquares` with initial
step `0.1`, floor `1e-8` and 1,000 attempts, run some thousand times from random starts
to harvest candidates, then `WithPerturbations` from each candidate with initial step
`0.1`, floor `1e-12`, factor `1.5` and 1,000 attempts.
They state that the procedure is attracted to configurations with all angles zero,
“which are rarely good”, and that when the optimal packing contains more than two
angles, as at `n = 17`, “the chance of finding a good approximation by
`BilliardOfSquares` becomes weak”.

**Inference.** That is the same diagnosis three times over from three independent
directions: the two-dimensional inflation attractor is the ordered, axis-aligned
configuration (section 2.2); the authors of the first working square algorithm say their
billiard is attracted to the all-zero-angle configurations (here); and this repository
measures that no single-square move leaves the grid at all (section 1.1). An inflation
mechanism does not by itself fix the problem this repository has.
What fixes it, in Gensane’s own pipeline and in Hoy’s 2024 one, is the simultaneous
perturbation wrapped around it.

### 2.6 Implementations

| Name | URL | Language | Licence | Shapes | Growth |
| --- | --- | --- | --- | --- | --- |
| `packing-generation` | [github.com/VasiliBaranov/packing-generation](https://github.com/VasiliBaranov/packing-generation) | C++ | MIT | hard spheres only | Lubachevsky-Stillinger, Jodrey-Tory, force-biased |
| DynamO | [github.com/dynamomd/DynamO](https://github.com/dynamomd/DynamO) | C++ | GPL3 | spheres, needles, dumbbells, parallel axis-aligned cubes | isotropic-compression Liouvillean |
| PackLSD | [math.nyu.edu/inmemoriam/donev//Packing/PackLSD/](https://math.nyu.edu/inmemoriam/donev//Packing/PackLSD/) | Fortran 90 | not stated | spheres, ellipses and ellipsoids, superellipses and superellipsoids | the reference implementation of the 2005 algorithm |
| HOOMD-blue | [github.com/glotzerlab/hoomd-blue](https://github.com/glotzerlab/hoomd-blue) | C++, CUDA, Python | BSD-3 | convex polygons including squares, polyhedra | none; Monte Carlo with box compression |

**Inference.** Nothing on that list packs a rotating square by growth.
The one code that represents squares natively, HOOMD-blue, does so with Monte Carlo and
box compression, which is section 3’s mechanism rather than this one.

## 3. Deforming the Container: The Adaptive Shrinking Cell

### 3.1 What it does, in enough detail to reimplement

**Published**, and read first-hand for this document from the retained PDF: Torquato and
Jiao, *Dense Packings of Polyhedra: Platonic and Archimedean Solids*
([arXiv:0909.0940](https://arxiv.org/abs/0909.0940), Physical Review E 80:041104, 2009,
retained at
`packing/resources/papers/torquato-jiao-2009-dense-packings-polyhedra-platonic-archimedean.pdf`),
section II.

The state is the particle configuration *and* the container.
A trial configuration is generated either by moving one randomly chosen particle, or by
a random macroscopic deformation and compression or expansion of the fundamental cell,
whose change is written as a symmetric strain tensor applied to the lattice vectors.
The acceptance rule, in the paper’s own terms:

- If any two particles overlap, the trial configuration is **rejected**. Overlap is
  forbidden, tested by the separating axis theorem, and there is no potential anywhere
  in the method.
- If the cell shrinks, the trial configuration is **accepted**.
- If the cell expands, it is accepted with probability `p_acc`, and the paper is
  specific: “we find `p_acc`, with an initial value `p_acc ~ 0.35`, decreasing as a
  power law with exponent equal to `-1` works well for most systems that we studied”,
  approaching zero at the jamming limit.
- The particle motion is **equally likely to be a translation or a rotation**.
- **The ratio of particle motions to boundary trial moves should be greater than
  unity**, especially towards the end of the simulation, since compressing a dense
  packing produces many overlaps.
- The total number of Monte Carlo moves per particle is **of order `5e6`**.
- The magnitudes of the particle motions and strain components must be adjusted as the
  density rises, especially near the jamming point.

**The paper’s own explanation of why the cell move matters is the point of this whole
section**, and it is worth quoting: the strain of the fundamental cell “corresponds to
non-trivial collective motions of the particle centroids … It is this collective motion
that enables the algorithm to explore the configuration space more efficiently and to
produce highly dense packings.”

**Inference.** That is section 1.1, stated by Torquato and Jiao in 2009 about a
different problem, before this repository measured it.
The mechanism they identify as load-bearing is exactly the one `sqsearch` does not have,
and the mechanism exp-135 added by hand and measured.
Their own justification for shrinking the cell rather than growing the particles is an
operation count: growing polyhedra costs `d N n_v` per move while straining the cell
costs `d(d + 1) / 2`, independent of `N`.

Two further numbers from the same paper: translation magnitudes of `1e-4` to `1e-6` of
the characteristic particle length, and a contact-gap tolerance of `1e-2` to `1e-3` of
the edge length. The starting density matters more than any of them.
Their tetrahedron table runs from `0.695407` at `N = 27` from an optimal-lattice start
to **`0.822637` at `N = 314` from a dilute start at initial density `0.005` to `0.01`**.

### 3.2 The two-dimensional protocol, which is the one to copy

**Published.** The two-dimensional implementations state a tighter protocol than the
three-dimensional one, and it answers most of this document’s parameter questions.

Atkinson, Jiao and Torquato: at least **500 trial movements per particle** in each
random-movement step, held constant through the run; the maximum move magnitude cut by a
constant ratio whenever the acceptance rate falls significantly below **50 per cent**;
the strain step keeping the **first** feasible strain it finds, with the maximum strain
shrinking by a constant ratio after each failure and **resetting** at the next strain
step; at least **500 outer iterations**; and an optional second pass from the final
configuration with the cell slightly expanded and much smaller magnitudes.

Maher, Stillinger and Torquato ([arXiv:2103.06290](https://arxiv.org/abs/2103.06290),
retained) is the most explicit: `N = 504` from a random-sequential-adsorption start at a
density orders of magnitude below the maximum; the same 50 per cent acceptance target;
**compression schedules of 1000, 100 and 10 trial moves per particle between strain
steps**, described as slow, medium and fast; **strictly downhill strain, with no
area-increasing move accepted at all**; **termination when the density increases by less
than `1e-10` over 100 consecutive strain steps**; and a contact-generation pass run
until the interparticle distances, **excluding rattlers**, fall below **`1e-10` of the
characteristic length for shapes made of arcs and `6e-10` for shapes containing flat
edges**, the coarser figure chosen because flat facets add rotational constraints near
jamming. Three independent runs per shape and schedule, averaged.

**Inference.** That flat-edge figure is the closest published answer to this document’s
tolerance question for a shape with facets, and it sits comfortably inside the band
section 1.5 measured at `n = 29`. The strictly-downhill strain rule is also worth noting
against the three-dimensional paper’s `p_acc = 0.35` uphill allowance: in two dimensions
the same group turned the uphill move off.

### 3.3 The linear-programming variant, and the one head-to-head against inflation

**Published.** Torquato and Jiao, *Robust algorithm to generate a diverse class of dense
disordered and ordered sphere packings via linear programming*
([arXiv:1008.2747](https://arxiv.org/abs/1008.2747), Physical Review E 82:061302, 2010,
retained), replaces the Monte Carlo search with a sequence of linear programs over the
particle displacements and the cell strain, with the non-overlap conditions linearised
inside an influence sphere of radius `gamma = alpha D`.

The published settings are a dial from disordered to optimal:

| `gamma` | strain bound | displacement bound | outcome |
| --- | --- | --- | --- |
| `1.5 D` | `0.1` | `0.5 D` | maximally random jammed |
| `3.5 D` | `0.01` | `0.05 D` | densest known |
| `> 4 D` |  |  | generally reaches maximal density |

Termination is a density increase below `1e-8`; if impenetrability is violated at a
solution, the bound widths are halved and the program re-solved.
`N` may be as small as 1, in which case the method reduces to lattice optimisation.

**And here is the only direct head-to-head in this document between a
deforming-container method and inflation.** Their table compares the linear-programming
scheme against Lubachevsky-Stillinger at matched density: **10 minutes against 1.5 hours
in three dimensions, 46 minutes against 4.8 hours in four, 3.2 hours against 14 hours in
five, and 8.3 hours against 193.5 hours in six.** For the densest packings rather than
the random ones, the linear-programming scheme reproduced the densest known in
dimensions two through six while their Lubachevsky-Stillinger runs did so only in two
and three. Lubachevsky-Stillinger is reported to need `1e5` to `1e7` collisions per
particle.

**Inference.** A deforming container solved by linear programming beat event-driven
inflation on the same problem, on both cost and reach, in the one place anyone measured
them together. That is the strongest single argument in this document for preferring
section 3’s mechanism to section 2’s, and it points at a hybrid this repository is
unusually well placed to build, because exp-006 already validated a fixed-angle linear
program over all centres and the side to `4.4e-16`.

### 3.4 What it has been run on, and the one thing it has deliberately never been run on

Platonic and Archimedean solids, superballs, spheres in dimensions two to six, and in
two dimensions pentagons, octagons, concave crosses, curved triangles, moon shapes,
rhombi, obtuse scalene triangles, lenses and ice-cream cones.
Atkinson, Jiao and Torquato, *Maximally dense packings of two-dimensional convex and
concave noncircular particles* ([arXiv:1405.0245](https://arxiv.org/abs/1405.0245),
retained), reproduces the known putative optimal packings of regular pentagons to
`2.09e-4` and `1.0e-5` in density.

**So the mechanism has been run in two dimensions, on polygons, with exact
separating-axis overlap tests, and it reproduces known optima.** That is the closest
published precedent to this problem of anything in this document.

**It has never been run on congruent squares, and the exclusions are deliberate and
stated.** Torquato and Jiao’s 2009 study covers each Platonic solid “except for the
cube, which is the only Platonic solid that tiles space”.
Maher, Stillinger and Torquato parameterise rhombi by an angle and identify the square
as the limiting case, then simulate only the six intermediate angles, recording a
maximal density of exactly 1 for the whole rhombus family.

**That is the periodic-cell degeneracy, confirmed from the sources rather than
asserted.** Congruent squares tile the plane, so a periodic adaptive-shrinking-cell run
on them has optimum 1, attained by the square lattice, and the `s(n)` problem never
arises. The already-retained torus annealer of Blair, Santangelo and Machta makes the
same point concretely for squares: density-one packings whenever `n` is a sum of two
squares, and a family at density `n / (n + 1)` otherwise.

The literature is also small enough to say so: an arXiv full-text search for the exact
phrase returns seven records and OpenAlex returns 27.

### 3.5 The one bounded-container adaptation that exists

**Published.** Fu, Steinhardt, Zhao, Socolar and Charbonneau, *Hard sphere packings
within cylinders* ([arXiv:1511.08472](https://arxiv.org/abs/1511.08472), Soft Matter
12:2505, 2016, retained), adapt the linear-programming variant to a **bounded**
direction by adding the hard wall as one more linear inequality alongside the pair
conditions, and collapsing the cell variables to the axial height and a twist.
Convergence is declared at a velocity change below `1e-6`. They searched to `N = 150`,
found their densest structures between `N = 50` and `85` where earlier work had used 7
or 15, and report 17 new structures.
Their own stated limitation is the honest one: the densest structures may be
quasiperiodic and so cannot be obtained with a finite periodic unit cell, which is what
the algorithm relies on.

**Inference.** This is the existence proof that the mechanism survives a hard wall.
A wall is just another linear inequality, and the cell variables shrink to whatever the
container has. For a square container the cell collapses to a single scalar, the side,
and the “strain” is a uniform rescale.
Nothing else about the method changes.

**Inference, and it is the recommendation this document ends on.** The periodic cell is
not the mechanism.
The mechanism is *the container being a degree of freedom that a trial
move can shrink*, with overlap forbidden and the shrink rejected when it collides.
In a bounded square container that reduces to a single scalar: propose
`s -> s(1 - eps)`, rescale every centre by the same factor about the container’s centre,
and reject the whole move if any pair or any wall test fails.
Nothing about that requires periodicity.
It is the same object as Squarl’s “contract, act, re-expand”, arrived at from the
physics side rather than from the search side, and the two arriving independently is the
same kind of evidence the 2026-09-08 survey drew from Squarl and exp-006 converging on
the fixed-angle LP.

## 4. Constraint Projection: Moving Bodies Apart Instead of Pushing Them

Two literatures answer to this description and they are not the same thing.
One is real-time graphics, where the object is plausible motion at a fixed frame budget.
The other is optimisation, where the object is a point in the intersection of constraint
sets. Only the second has been pointed at packing, and it is the one that matters here.

### 4.1 Position-based dynamics: what it is, and what it actually guarantees

**Published**, read first-hand from the retained PDF: Mueller, Heidelberger, Hennix and
Ratcliff, *Position Based Dynamics*, Journal of Visual Communication and Image
Representation 18(2):109-118, 2007, retained at
`packing/resources/papers/muller-heidelberger-hennix-2007-position-based-dynamics.pdf`.

The loop predicts positions by explicit integration, generates collision constraints for
the predicted positions, then runs `solverIterations` passes that project each
constraint in turn, Gauss-Seidel style, moving the participating points along the
constraint gradient weighted by inverse mass.
Velocities are recovered from the position change afterwards.
An inequality constraint is projected only when it is violated, which is exactly the
“resolve overlap by moving bodies apart” rule.

**Its convergence property, in the paper’s own words, is the reason to be careful.** The
stiffness parameter `k` enters by multiplying the corrections, and the remaining error
for a single distance constraint after `n_s` solver iterations is
`delta_p (1 - k)^{n_s}`. The paper introduces `k' = 1 - (1 - k)^{1/n_s}` to make the
error linear in `k` and independent of the iteration count, and then states plainly that
“the resulting material stiffness is still dependent on the time step of the
simulation”. So a single constraint is satisfied geometrically at rate `1 - k` per pass,
the coupled system is Gauss-Seidel with no global guarantee, and the effective stiffness
is a function of solver settings rather than of the material.
XPBD exists precisely to break that dependence.

**What the successors fix, and what they do not.** XPBD (Macklin, Mueller and Chentanez,
2016, retained) replaces the stiffness `k` with a compliance `alpha` scaled by
`1 / dt^2` and carries a per-constraint Lagrange multiplier, which makes the stiffness
independent of iteration count and time step.
The survey by Bender, Mueller and Macklin (2017, retained) is explicit that this is a
consistency fix and not a speed one: “XPBD does not make PBD converge faster, the same
number of iterations would be required to reach a stiff solution … if the solver is
terminated before convergence then this will manifest as artificial compliance.”
The same survey notes that Gauss-Seidel “typically converges significantly slower than
global solvers” and is “called a smoother because it evens out the high frequency errors
much faster than low frequency errors”, and that the Jacobi variant “may not converge at
all, for example if the system matrix is not positive definite”.
The 2020 rigid-body paper lists PBD’s defects in its own words: the stiffness is
iteration and time step dependent, it converges slowly, and it depends on the order of
constraint handling.
Its practical answer is substepping rather than iterating: with `dt = 1/60` and
typically one position iteration per substep, 20 substeps for most scenes.
On a chain with a 1:100000 mass ratio, 100 iterations left a maximum error of `322.1`
against `3.2` for 100 substeps.
Constraint-force accuracy on a 20-particle chain reaches a maximum relative error of 6
per cent at 50 iterations, 2 per cent at 100 and 0.5 per cent at 1,000.

**Inference.** As a *dynamics* this is a modelling choice with known artifacts.
As a *feasibility projection* at a fixed container side it is a reasonable, cheap
operator: for each overlapping pair, separate the two squares along the minimum
translation direction of the separating-axis test, share the correction between them,
and iterate. That is a useful primitive here for a specific measured reason.
exp-137 records that the LP quench returns separations non-negative only to solver
tolerance, so an emitted pose needs a monotone repair before it is a packing, and the
repair currently in use scales the centres apart, which can only raise the reported
side. A projection repair moves only what is overlapping.

What the graphics literature does **not** supply is any evidence that iterated
projection finds *dense* packings.
Its objective is a feasible configuration, not an extremal one, and the negative search
result is clean: on arXiv, `all:"position based dynamics" AND all:packing` returns
**zero** results, the hyphenated variant returns zero, and `all:"XPBD"` returns eleven
papers of which none is about packing.
An OpenAlex search for position-based dynamics with packing optimisation returns terrain
modelling, surgical simulation and pavement-crack sealing.
**Position-based dynamics has never been used as a packing optimiser.**

### 4.2 Divide and concur, and relaxed-reflect-reflect, which are the packing versions

**Published.** Elser and collaborators built a general constraint-satisfaction method on
projections and pointed it at packing.
The retained sources are Gravel and Elser’s *Divide and Concur*, Kallus, Elser and
Gravel’s *A Method for Dense Packing Discovery*
([arXiv:1003.3301](https://arxiv.org/abs/1003.3301), 2010) and their tetrahedron paper,
and Elser’s *How densely can spheres be packed with moderate effort in high dimensions?*
([arXiv:2305.13492](https://arxiv.org/abs/2305.13492), 2023), all in
`packing/resources/papers/`.

Divide and concur splits the problem into two sets whose projections are easy.
The **divide** set gives each object as many copies as it has constraints, and each copy
is projected to satisfy its own constraint independently; the **concur** set forces all
copies of the same object to agree, by averaging.
A packing is a point in the intersection.
The 2010 method paper’s stated design feature is the one this document keeps returning
to: “the integration of the unit cell parameters with the other packing variables in the
definition of the configuration space”.
**The container is a variable, not a boundary condition**, which is the adaptive
shrinking cell’s idea reached from the projection side.

The iteration is relaxed-reflect-reflect, and Elser 2023 states it and its settings,
read first-hand:

- The map is `x -> x + beta (P_B(R_A(x)) - P_A(x))` with `R_A(x) = 2 P_A(x) - x`.
- **`beta`**: “fixed-point convergence is fastest when `beta = 1` is used for the RRR
  time step, smaller values are more productive when the search is faced with nonconvex
  constraints. We used `beta = 0.5` in all the experiments.”
- A metric update rate `gamma` was `1e-3` in all experiments except one hard search,
  where it was `1e-2`.
- Progress is monitored by the normalised error `eps = ||x' - x|| / sqrt(N)`, which is
  the root-mean-square distance moved by the copies.
- **Restart policy is explicit and quantified.** A run is abandoned when a monotonicity
  criterion is violated; an instance has “`m`-monotone difficulty” when a run with
  monotonicity parameter `m` succeeds with probability one half over random initial
  points. That is a published way of measuring how hard an instance is for the method,
  and it is exactly the shape of statistic
  [H-012](../../../packing/campaign/hypotheses/H-012-record-basins-are-rare.md) asks
  for.
- Reported performance: three of four runs found Best’s packing of 40 spheres in ten
  dimensions in under `1e5` iterations.
  Success is declared at `eps < 1e-4`. Cost per configuration in fourteen dimensions
  rises with the monotonicity parameter: 59 iterations at `m = 1`, 163 at `m = 10`,
  1,190 at `m = 100`, 3,980 at `m = 1000`. Its author’s comparison note is worth
  carrying: “Unlike Lubachevsky-Stillinger, RRR is not prone to jamming.”

**What is actually proved about it.** In the convex case Douglas-Rachford and
alternating projections converge, and that is classical.
In the nonconvex case the results are local only.
Lal, *The Flow Limit of Reflect-Reflect-Relax*
([arXiv:2512.23843](https://arxiv.org/abs/2512.23843), December 2025, retained) proves
that inside a tubular neighbourhood of a smooth transversally intersecting feasible
manifold the transverse dynamics form a hyperbolic sink with exponential decay at rates
set by the principal angles, and that a quadratic energy is a strict Lyapunov function
there, which excludes recurrence and chaos in that basin.
Small-`beta` RRR is shown to be a forward-Euler discretisation of a flow with `O(eps)`
trajectory error, which is why the small-`beta` guidance is not folklore.
The paper states its own limit: all of its rigorous results are local, the global
wandering phase before entry dominates the runtime at every `beta`, and the degradation
as `beta` approaches 1 is a conjecture built on a percolation model rather than a
theorem. Clean scaling is measured only for `beta <= 0.3`.

**Cost per configuration on non-spherical bodies**, from the periodic divide-and-concur
work: in two dimensions, 42 iterations, 11 replicas, `0.1` milliseconds per iteration,
100 successes in 100 runs.
On tetrahedra it reproduces the densest known packing in **15 of 100 runs**, at 14
milliseconds per iteration, with the sample run raising its density target at iteration
15,751 and again at 15,898 and continuing past 40,000 iterations.

### 4.3 The one cold, at-scale result on the sibling problem

**Published**, and read first-hand from
`packing/resources/papers/gravel-elser-2008-divide-and-concur.raw.md`: Gravel and Elser,
*Divide and concur: A general approach to constraint satisfaction*
([arXiv:0801.0222](https://arxiv.org/abs/0801.0222), 2008), applied the method to **`n`
equal disks in a unit square for every `n` from 2 to 200**, generating up to 400 random
initial guesses per `n`. Their protocol is a container schedule: choose a small
diameter, seek a packing, increase the diameter on success, repeat until the algorithm
fails or the best known diameter is reached, then push past it.
Their own statement of the starting information is the important one: **“No information
about the known packings was used, apart from their densities.”**

The result:

| Outcome over the 197 values of `n` | count |
| --- | ---: |
| Reached within `1e-9` of the best known diameter | 143 |
| **Improved on the best known** | **38** |
| Improved by more than `1e-6` | 28 |

The smallest improved case is `n = 91`, and the largest improvement is at `n = 182`, at
`4.6e-5` above the previous best.
Their metric update is published too:
`lambda_ab -> sigma lambda_ab + (1 - sigma) exp(-alpha d_ab)` with `sigma = 0.99`,
chosen so the metric update is quasi-adiabatic, and `alpha` about `30`. Their closing
argument is a direct claim against the family this repository has been pursuing: on
simplicity and observed efficiency, the framework is “a competitive alternative to
stochastic methods such as simulated annealing”.

**Inference, and it changes the ranking in section 10.** This is the only cold,
at-scale, whole-benchmark result found anywhere in either survey for a non-annealing
mechanism on the sibling problem, and it is the shape of result the owner’s question
asks for: point the method at a whole range of `n`, from randomness, and see how many
best-knowns come back.
It is also, unlike replica exchange over a pressure ladder, fully retrievable and fully
specified.

**Applied to non-spherical bodies: yes.** The 2010 method paper reports a new dense
packing of regular four-dimensional simplices at density `128/219`, and the same
framework produced the improvements to the densest known tetrahedron packing.
So projection with the cell as a variable has set records on non-spherical particles.

**Applied to squares in a square: no.** The searches are clean negatives.
On arXiv, `"Douglas-Rachford" AND "packing"` returns **zero**, `"difference map" AND
"packing"` returns **zero**, and `"projection" AND "square packing"` returns **zero**.
The Douglas-Rachford hits that do exist are convergence theory rather than packing runs.
The thirteen works that cite the 2010 method paper are sphere, ellipsoid, polyhedron and
discrete-element work, with no two-dimensional polygon-in-a-bounded-container follow-up.

### 4.4 The polygon projection this problem needs already exists

**Published.** Kallus’s 2011 Cornell thesis, *Solving Geometric Puzzles with Divide and
Concur* (retained at
`packing/resources/papers/kallus-2011-solving-geometric-puzzles-with-divide-and-concur.pdf`),
specifies the non-overlap projection for **convex polytopes**: the smallest vertex
displacement that separates two overlapping convex hulls.
It searches the subsets of the combined vertex set for the separating plane that costs
least, taking exact planes through `d`-point subsets first and least-squares planes
through larger subsets second, then moves only the vertices in the winning subset onto
that plane. A rigidity projection afterwards finds the rigid motion of the reference
polytope closest to the displaced vertices, which is what makes the concur projection
approximate rather than exact.
The cost is exponential in the vertex count, which the thesis acknowledges and bounds to
“polyhedra with a small number of vertices”.

**Inference.** For a square in the plane that is `d = 2` and eight vertices across the
pair, so the first stage enumerates sixteen cross pairs.
It is trivially cheap here, and its by-product `Delta^2` is an interpenetration measure
usable as the adaptive weight the same framework already wants.
**So the two halves of the machinery exist and have never been joined**: disks in a
*bounded unit square* on one side (section 4.3), convex polytopes in a *periodic cell
with no boundary* on the other.
Squares in a square sits exactly between them.

**Inference, on the ranking.** This is the mechanism in this document with the best
combination of four properties.
It needs no potential and no smoothness, only projections, which suits section 1.4. It
makes the container a variable, which suits section 1.1. It has an escape mechanism
inside the iteration rather than bolted on, since the reflections are what keep it from
stalling at a consistent-but-infeasible point, and its authors say so: alternating
projections is explicitly rejected in the 2008 paper as “prone to getting stuck at fixed
points which do not correspond to solutions”.
And it is the only mechanism here with a published cold, whole-benchmark result on the
sibling problem. The simplest projection of all is already computed by `sqsearch`: the
minimum translation along the best separating axis is `geom::pair_depth`.

## 5. Contact Dynamics and Exact Non-penetration

### 5.1 What it is

**Published.** Bodies are perfectly rigid, with no stiffness and no penalty.
The contact law is the Signorini graph, complementarity between the gap and the normal
reaction, together with the Coulomb friction cone, both set-valued rather than
functions. Time stepping is implicit and backward-Euler, and the unknowns are the
relative velocity at the *end* of the step and the *impulse over* the step rather than
instantaneous forces, which is what allows a large step.
The solver is a non-linear Gauss-Seidel sweep over the contact list: one contact at a
time, its neighbours’ current reactions treated as external, the one-contact problem
solved by intersecting a hyperplane with the Signorini-Coulomb graphs, and the result
written back in place.
Sources retained here: Unger and Kertesz’s review
([arXiv:cond-mat/0211696](https://arxiv.org/abs/cond-mat/0211696), 2003), Dubois, Acary
and Jean’s history (Comptes Rendus Mecanique 346:247, 2018, retained from the
open-access mirror), and the parallel and ultrascale papers below.

The update order should be a random *sweep*, re-randomised each pass, and a fully
parallel Jacobi update is unstable: Shojaaee and colleagues
([arXiv:1104.3516](https://arxiv.org/abs/1104.3516), retained) report divergence of the
parallel update above a critical fraction of about `0.65` in dense systems.

Working settings from the retained papers, since the question was asked in numbers:
Shaebani, Unger and Kertesz ([arXiv:0803.3566](https://arxiv.org/abs/0803.3566),
retained) run 100 disks with 100 solver iterations per step at `dt = 0.01`, stopping
when both the mean velocity and the mean acceleration fall below `1e-10`; Shojaaee and
colleagues use a convergence threshold of `1e-6` required at 90 per cent of contacts, or
a cap of 200 iterations; Preclik and Ruede
([arXiv:1501.05810](https://arxiv.org/abs/1501.05810), retained) use `dt = 100`
microseconds, under-relaxation `0.75` and a fixed 10 iterations per step at up to `1e9`
particles; Chrono matching a granular experiment uses `dt = 1e-4` seconds with 500
solver iterations.

### 5.2 Non-penetration is exact in the law and approximate in the gap

**Published**, and this matters because “exact non-penetration” is the reason the
mechanism was on the list.
Dubois, Acary and Jean state that Moreau’s velocity-level formulation “ensures that the
gap remains positive in a continuous time evolution”, but that in a time-stepping scheme
“this formulation provides approximate gaps and may generate interpenetrations,
sometimes self-restoring”.
They name three remedies: a viscoelastic regularisation between contacting bodies,
enforcing the position and velocity constraints across two steps, or adding a
position-level constraint.
Shaebani and colleagues treat the mean overlap as a tunable accuracy axis, sweeping it
from `1e-8` to `1e-1` against a CPU cost from `1e-2` to `1e4` seconds.

**Inference.** Against section 1.3 that is disqualifying for the objective.
The container has no slack at any record, so a method whose overlap is a tunable
accuracy parameter is reporting a side that depends on how long it was run.

### 5.3 The indeterminacy bites squares specifically

**Published.** Rigid contact-dynamics packings are hyperstatic and the reaction field is
not unique. Dubois, Acary and Jean name the polygon case exactly: “When two polygonal
objects meet, a side of a polygon set onto a side of the other, the situation is handled
choosing two contact loci where nodal reactions are exerted.
This localization process generates indeterminacy.”
Olsen and Kamrin ([arXiv:1805.07437](https://arxiv.org/abs/1805.07437), 2018, retained)
propose an elastic compatibility condition to pick a unique element of the kernel and
state they are not aware of any previously proposed methodology to resolve it.

**Inference.** Edge-to-edge contact between two squares is that case, and it is not an
edge case here: at the trivial grid every interior contact is edge to edge, and the
`n = 11` record has 14 pair contacts of which the retained contact structure classifies
several as corner-to-edge.
A solver whose force field is ambiguous on exactly the configurations this problem lives
in is a poor foundation for a search that reads structure off the forces.

### 5.4 It has never been used as an optimiser, and the near miss says why

**Published.** An OpenAlex search combining contact dynamics with densest packing and
optimisation returns seven records, none of which is a packing-optimisation paper.
Every application in the 2018 review is process simulation: rheology, tribology,
industrial process, masonry, rock masses, earthquakes, landslides, robotics.

The nearest thing to an exception is instructive.
Shaebani, Unger and Kertesz couple the periodic cell to a constant external pressure so
that it shrinks until the internal pressure matches, which is structurally the
contact-dynamics analogue of an adaptive cell.
Their declared goal is to generate *homogeneous random* packings, and their own finding
is that the final volume fraction is **insensitive** to the external pressure, the
iteration count, the time step and the inertia parameter across the ranges they swept.

**Inference.** That is a random-close-packing sampler, not a density maximiser, and the
insensitivity is the diagnosis: the mechanism converges to the packing the *process*
makes, and turning its dials does not move the density.
A search needs a dial that moves the answer.

### 5.5 Where it does earn a place here

Contact dynamics handles a bounded container trivially, because a wall is simply another
contact candidate, and it runs routinely on two-dimensional polygons at thousands of
particles (Azema, Estrada and Radjai,
[arXiv:1208.0499](https://arxiv.org/abs/1208.0499), retained, run 5,000 particles across
five shape families prepared by isotropic compaction inside a rectangular frame).
The asymmetry with section 3 is sharp and worth stating plainly: **contact dynamics
handles the bounded container and has no density objective; the adaptive shrinking cell
has the density objective and is intrinsically periodic.**

**Inference.** The one job in this repository for which a rigid contact solver is the
right tool is the necessary-condition test X-025 already frames as C0d: load a retained
best-known packing, run the law with no target and no snap, and check that it does not
drift. Section 1.2 supplies the answer key and makes the test two-sided: on the four
fully immobile non-grid records at `n = 5, 11, 28, 40` nothing may move, and on the
other 30 exactly the squares the escape screen lists may move, with the container side
never growing. That is a use for a simulator, not a search.

### 5.6 Implementations, and the licence problem

| Package | Licence | 2D convex polygons first class | Non-penetration |
| --- | --- | --- | --- |
| LMGC90 | **none declared** in the public repository | **yes**, disk, polygon, sphere, polyhedron are native | true non-smooth contact dynamics |
| Solfec-1.0 | none declared | no, three-dimensional only | true non-smooth contact dynamics |
| Siconos | Apache-2.0 | partly; a non-smooth framework with its own solver library | true non-smooth, Moreau-Jean stepping |
| Project Chrono | BSD-3-Clause | three-dimensional first | complementarity mode is exact by constraint; it also ships a penalty mode |
| Box2D | MIT | **yes**, the core primitive | **soft**, with contact stiffness, damping and an explicit slop |
| Bullet | zlib | a thin wrapper over three dimensions | approximate, sequential impulse with error reduction and a contact-breaking threshold |

**Inference.** The one combination this problem would want, a rigid complementarity
solver with two-dimensional convex polygons as a first-class primitive, exists only in
LMGC90, whose public repository declares no licence.
Under this repository’s supply-chain rules that is a blocker to vendoring rather than a
detail. Box2D is the only permissively licensed two-dimensional polygon solver on the
list and it is explicitly soft, which section 5.2 already rules out for the objective.

## 6. Smoothing and Continuation on the Overlap Penalty

**Published**, and read first-hand from the retained PDF: Nurmela and Ostergard,
*Packing up to 50 Equal Circles in a Square*, Discrete and Computational Geometry
18:111-120, 1997, retained at
`packing/resources/papers/nurmela-ostergard-1997-packing-up-to-50-equal-circles-in-a-square.pdf`.
This is the cleanest published instance of annealing a smoothing parameter on a packing
problem, and every part of it is stated.

The objective is a soft minimum over pairwise distances:

`E = sum over pairs of (lambda / d_ij^2)^m`

with `d_ij` the centre distance, `lambda` a scaling factor to prevent numerical
overflow, and `m` a positive integer.
As `m` grows, only the smallest distances affect the energy, so `E` interpolates between
a smooth all-pairs repulsion and the true minimum-distance objective.
The recipe around it:

- The container constraint is removed rather than penalised, by the coordinate
  transformation `x_i = sin(x~_i)`, `y_i = sin(y~_i)`, which makes the problem
  unconstrained while keeping every centre inside the square by construction.
- The energy is twice continuously differentiable except where two points coincide, so a
  second-order method applies.
  They use steepest descent with a Goldstein-Armijo backtracking line search early and a
  modified Newton method at the end, for each value of `m`.
- **The schedule: start with `m` in the range 10 to 100, find a local optimum, then
  double `m` and re-optimise.** Final values as large as `1e50` were used in some cases,
  “although optimization can usually be ended when `m` reaches `1e6`”.
- `lambda` is recalculated after each optimisation step, set to the square of the
  current shortest distance, because otherwise the cost becomes impractically small at
  large `m`.
- **Restart policy: at least 50 optimisation runs per `n` from random initial
  solutions.**
- The result is then promoted exactly: sort all distances, find the location where the
  distance shows a sudden increase, assume everything below it is a contact, assume
  points very close to the boundary are on it, form the resulting nonlinear system and
  solve it by a modified Newton-Raphson.
  Two threshold values drive that automatically.

**Inference.** Three parts of that transfer to squares directly and one does not.
The soft-minimum-by-large-exponent trick transfers, with the pairwise distance replaced
by the separating-axis gap, since the gap is also a maximum over four axis tests and can
be softened the same way.
The doubling schedule transfers.
The contact-promotion step transfers, and section 1.5 says the “sudden increase” they
look for is 97 decades wide at this repository’s `n = 29` record, so the threshold is
not a delicate choice at a converged configuration.
What does not transfer is the coordinate transformation: a square’s containment
constraint depends on its angle through the half-extent `(|cos t| + |sin t|) / 2`, so a
fixed `sin` reparameterisation does not enforce it.
That is a real cost, because the container constraint then has to come back as a penalty
or a projection.

## 7. Differentiable Simulation as an Optimiser

### 7.1 The failure mode is measured, not merely suspected

**Published.** Suh, Simchowitz, Zhang, Tedrake and Zhang, *Do Differentiable Simulators
Give Better Policy Gradients?* ([arXiv:2202.00817](https://arxiv.org/abs/2202.00817),
ICML 2022, retained), is the definitive statement and it is a set of theorems, not an
anecdote. The zeroth-order estimator is unbiased even under discontinuous dynamics and
cost; the first-order estimator, the one differentiable simulation supplies, is unbiased
only under locally Lipschitz dynamics and a continuously differentiable cost.
Their Heaviside example is the one to remember: the first-order estimator has **zero
empirical variance and is biased in expectation**, because the gradient of a step
function is zero almost everywhere.
So choosing an estimator by its measured variance selects the wrong one.
Their Coulomb-friction example shows the bias and variance scaling inversely with the
slip tolerance, meaning more physical friction gives worse gradients; and their
geometric-discontinuity example, **balls colliding with a rectangular wall**, shows that
rounding the corner makes the estimator asymptotically unbiased while leaving high
empirical bias because the relaxation is stiff.
That is the geometry of congruent squares in contact.

Metz, Freeman, Schoenholz and Kachman
([arXiv:2111.05803](https://arxiv.org/abs/2111.05803), 2021, retained) measured gradient
variance growing **exponentially with unroll length** in double precision, and name
rigid body physics with contacts as a chaotic case; averaging buys only `1/sqrt(N)`
against that.

### 7.2 The measurement that rules out combining sections 4 and 7

**Published.** Zhong, Han and Brikis
([arXiv:2207.05060](https://arxiv.org/abs/2207.05060), 2022, retained) compare gradients
from several differentiable engines against a closed-form ground truth on a bouncing
ball at `dt = 1/480`. The analytical derivative of the final height with respect to the
initial height is `-1.0000`. A linear-complementarity engine with a continuous time of
impact reproduces it exactly.
**Both position-based-dynamics implementations return `0.0000` and `-0.0020`.**

Their explanation is structural rather than an implementation defect: when
interpenetration is detected the position is projected to resolve it, so an
infinitesimal change in the initial position does not change the outcome, because the
body is always moved to touch.
**The projection annihilates the derivative.** They also record that discarding the
continuous time of impact in velocity-impulse contact models gives a completely wrong
position gradient and that shrinking the time step does not fix it, and that two
compliant implementations disagree in *sign*.

**Inference.** The obvious hybrid, “use a position-based solver and differentiate
through it”, is ruled out by measurement.
The projection that makes section 4 attractive is exactly what destroys the gradient in
section 7. These two mechanisms are alternatives, not layers.

### 7.3 Differentiable packing exists, and its overlap proxy cannot represent this problem

**Published.** Gupta and Raman, *Differentiable Packing of Irregular 3D Objects with
Adaptive Container Estimation* ([arXiv:2606.16333](https://arxiv.org/abs/2606.16333),
2026, retained), jointly optimises `6N` pose parameters and three container side lengths
in one automatic-differentiation loop, with no physics engine.
Its settings are fully published: six weighted penalty terms, an overlap weight of
`80 ln(N + 1)` with threshold `1e-6`, two Adam optimisers at learning rate `0.005` for
translations and `0.002` for rotations, plateau scheduling with patience 100 and factor
`0.7`, gradients clipped to L2 norm `0.5`, at most `min(5000, 1000 + 5N)` epochs with
early stopping, and an adaptive container squeeze fired typically 5 to 10 times inside a
declared epoch window.
It reports packing efficiency between `42.3` and `70.9` per cent, and runtimes from 24
seconds at `N = 10` to 223 seconds at `N = 100` on one consumer GPU in `float32`.

**And its overlap term is computed on axis-aligned bounding boxes rather than on the
bodies.**

**Inference, and it is a sharper reason to set this aside than “wrong problem”.** Two
axis-aligned unit squares in edge contact have touching bounding boxes, so the surrogate
is exact there.
Two unit squares tilted 45 degrees have bounding boxes of side `sqrt(2)`,
so the surrogate would hold them about 41 per cent further apart than the geometry
requires. Every known-best square packing above the small cases uses tilted squares, and
`n = 17` needs three distinct angles.
The proxy cannot represent the configurations this problem is about, independently of
any question about gradients.
The paper’s own data confirm the proxy is loose rather than tight: it reports
bounding-box overlaps with zero mesh intersection.
An efficiency band of `42` to `71` per cent is also nowhere near the regime here, where
the interesting margin at `n = 89` is `0.0503` on a side of `9.95`.

Two further differentiable-packing papers were retained and screened out for stated
reasons: an image-space collage method whose overlap is a pixel count through a
differentiable renderer, and therefore resolution-limited by construction so that exact
contact is unavailable; and two placement pipelines that are not congruent-shape optimal
packing at all.

## 8. What the Circle Literature Adds That the Annealing Survey Did Not Work Through

The 2026-09-08 survey covered the stochastic-search side of this literature.
Four mechanisms beside it are physics- or continuation-flavoured, all four have
published recovery rates against a whole record table, and none was in that survey.

### 8.1 A container-shrink ladder, which is the closest circle analogue to inflation

**Published.** He, Ye and Wang, *An efficient quasi-physical quasi-human algorithm for
packing equal circles in a circular container*
([arXiv:1611.02323](https://arxiv.org/abs/1611.02323), retained), is the sharpest
recovery result found in either survey, and its escape mechanism is a container schedule
rather than a temperature.

The potential is a squared hinge, so it is continuously differentiable: overlap depths
use a maximum against zero but the energy squares them, giving `U >= 0` everywhere and
`U = 0` exactly on feasible layouts, which turns packing at a fixed container radius
into root finding. The local solver is BFGS with an exact line search, terminating at
`U < 1e-20` or a gradient norm below `1e-10`, with each circle keeping only its `l`
nearest neighbours in the gradient sum; `l = 10` was chosen by fixing the radius to the
best known at `n = 100, 150, 200` and running the local solver 1,000 times.

**The escape step is the part to carry over.** Instead of a temperature, they shrink the
container and relax: `R' = beta R` with `beta = 0.3 + 0.035 m` for `m = 0` to `19`, so
twenty levels from `0.30` to `0.965`, generating twenty shrunk layouts per iteration and
relaxing each. The container radius itself is then bisected to `1e-10`.

**Recovery, stated exactly.** Over `n = 1` to `100`, “except `n = 82, 100`, QPQH finds
98 current best-known layouts”, and “for `n <= 49`, the algorithm can always stably find
the current best-known layout”.
Their per-instance hit counts out of ten runs above `n = 50` are the honest picture: ten
of ten at `n = 91`, three of ten at `n = 78`, one of ten at `n = 97`, zero of ten at
`n = 82`. Over `n = 1` to `320` they report 66 new best layouts, with improvements from
`1e-7` to `1e-2` and most at `1e-3` or `1e-4`.

**Inference.** This is what a positive answer to the owner’s question looks like on the
sibling problem, and its mechanism is a shrink ladder with a smooth local solver, not an
annealer. What would have to change for squares: the squared-hinge potential would be
built on the separating-axis gap rather than on a centre distance, which reintroduces
the maximum that section 1.4 warns about; and the neighbour truncation at `l = 10` rests
on a disk touching at most six others, a bound a square does not have.

### 8.2 Smooth nonlinear programming with a squared hinge, and its measured recovery

**Published.** Birgin and Sobral
(`packing/resources/papers/birgin-sobral-2008-minimizing-object-dimensions-circle-sphere-packing.pdf`)
write non-overlap as a squared hinge on squared distances, which removes two
non-differentiabilities at once: squaring the distance avoids the square root’s kink at
zero, and squaring the hinge makes it continuously differentiable.
The result is a smooth equality constraint that an augmented-Lagrangian code can take,
and they solve it with ALGENCAN over a multistart that scatters items into an
overestimated container and runs to a CPU budget.

**Recovery, and it is the strongest smooth-method result in the circle literature.**
Birgin and Gentil (retained) report that over `n = 1` to `50`, “in 48 of the cases of
packing in a circle and in 44 of those of packing in a square, the results matched to
all decimal places, i.e. up to the machine precision”, with the remaining eight at about
`1e-6`. Their refinement is the same two-stage shape this repository already uses: solve
to `1e-4`, then remove the loose items, detect contacts, build the nonlinear contact
system and take at most 1,000 Newton steps.
**A public implementation exists**, Fortran 77 with all solutions, on the author’s page.

The cost data are worth carrying because they are the cleanest statement of how
multistart behaves on this landscape: in a square container their trials-to-best run
from 987 at `n = 100` to 18,817 at `n = 75`, a spread of three to four orders of
magnitude between adjacent `n`.

**Squares verdict: this line does not do free rotation.** Birgin, Martinez and
Nishihara’s rectangle paper is orthogonal packing with axes parallel to the coordinate
axes, extended only to 90-degree rotations.

### 8.3 The formulation trick that removes the maximum, and the one that removes it exactly

Three retained sources attack the same obstacle, which is section 1.4’s.

Lopez and Beasley (retained) replace the non-overlap maximum by a convex combination
with one new continuous variable per pair in `[0, 1]`, so the disjunction becomes a
continuous interpolation.
Their formulation-space search moves a relaxation parameter from `0.05` down by a factor
`0.5` per level, terminating at `1e-5` or after three non-improving iterations, with
five replications and a per-solve limit.
**Their own verdict is decisive for this repository: “Rotation through an arbitrary
angle cannot be dealt with by our approach.”**

Romanova, Bennell and Stoyan (retained) name the problem outright: phi-functions for
polyhedra “can be highly complicated analytically, since they involve many radicals and
maximum operators, and are therefore difficult for NLP-solvers to handle”.
Their quasi-phi-functions are radical-free and maximum-free at the cost of auxiliary
variables per pair, and they *do* handle free rotation, through a rotation matrix in the
placement parameters.
**And they publish the scaling wall**: feeding the full model to a nonlinear-programming
solver directly is “an unrealistic task for the available state of the art NLP-solvers …
for `N > 15` starting from a random point and for `N > 30` starting from a feasible
point.”

**Inference.** That wall is at the same place as the one the 2026-09-08 survey found for
general-purpose global optimisation, which matched the square records to `n = 16` and
failed from `n = 17`. Two different formulations, two different solver families, the
same boundary. A smooth global model of this problem stops in the teens.

**The third source removes the maximum exactly rather than by relaxation, and it is the
one worth building on.** Peralta, Andretta and Oliveira (retained) allow free rotation
of the polygons *and of the separating lines*: non-overlap is enforced by an explicit
separating line per pair whose angle is itself a continuous variable, which is exact for
convex pieces and needs no maximum at all.

**Inference, and it is a genuinely new option for this repository.** This is the
continuous version of what Squarl and exp-006 do discretely.
Squarl infers one directed separating-axis branch per pair and beams over the ambiguous
ones; exp-006 fixes the angles and solves the centres by linear programming.
Making the separating-line angle a variable removes the branch choice, and with it the
kink that exp-006 measured at the `n = 11` optimum, at a cost of one variable per pair.
For `n = 17` that is 136 extra variables; for `n = 50`, 1,225. It is the only mechanism
found in either survey that makes this problem genuinely smooth without approximating
the geometry.

### 8.4 Continuation measured against multistart, on a problem that is not packing

**Published.** More and Wu, *Global Continuation for Distance Geometry Problems* (1995
Argonne preprint, retained; its scanned pages carry no text layer, so an OCR aid is
retained beside it and the numbers below are read from the page images).
Their Gaussian transform of the distance-geometry objective is closed form: the
smoothing adds a single quadratic term of stiffness `10 lambda^2`, so there is no
quadrature. They give a convexity threshold, `lambda >= sqrt(2/5) delta`, about
`0.63 delta`, above which the transform is convex.

**Their schedule is linear, not geometric**: `lambda_k = (1 - k/p) lambda_0` for `k = 0`
to `p`, ending at exactly zero so the last iterate minimises the original function.
They used `lambda_0 = 0.5, p = 10`, and when that failed on the 64-atom problem they
diagnosed the initial smoothing as too small and reran at `lambda_0 = 1, p = 20`, after
which the method “found the global minimizer for all ten starting points”.

**The comparison is the point.** Against multistart with the same local solver,
continuation succeeded on every problem in their table while multistart failed at 64 and
216 atoms, and at 216 atoms continuation used roughly a sixth of the function
evaluations. Their own summary at that size is that finding a global minimiser cost less
than 30 per cent more than finding a local one.

**Inference.** This is not a packing problem and nothing in that paper packs anything.
It is included because it is the cleanest measured statement that annealing the
smoothing parameter beats restarting, and because its schedule shape, linear in the
smoothing parameter rather than geometric in an exponent, is a second published option
beside section 6’s doubling rule.

### 8.5 Which ladders port to a rotating square, and which do not

This is the synthesis the section is for, and it divides cleanly.

**The ladders that do not port** are the ones that schedule a smoothing parameter of the
*potential*. Every method above that reaches record quality on disks builds its
potential from **one scalar per pair, the centre distance**: `(lambda / d^2)^m` in
section 6, `max(2 - d, 0)^2` in section 8.1, `max{0, (r_i + r_j)^2 - d^2}^2` in section
8.2. A freely rotating square has no such scalar and no analytic overlap potential
(section 1.4), so the exponent doubling and the Gaussian stiffness ramp are ladders over
an object this problem does not have.
They can be rebuilt on the separating-axis gap, but that is a transfer with an untested
step in it, not a port.

**The ladders that do port unchanged** are the ones that schedule the *container* or the
*step*, and there are two, both fully specified.
He, Ye and Wang’s container-shrink ladder, twenty levels of shrink factor from `0.30` to
`0.965` (section 8.1), touches no overlap model at all.
Boll, Donovan, Graham and Lubachevsky’s move-step ladder, `s_0 = 0.25` with shrink
`0.43` down to a floor of `1e-10` under an impatience counter of 1,000 (section 2.5),
touches no overlap model either.
Both are indifferent to what the bodies are.

**The formulation changes that make free rotation exact** are section 8.3’s: a
separating line per pair with a variable angle, or quasi-phi-functions with auxiliary
variables per pair. Both handle continuous rotation, and both are published with their
solver and their tolerance.

**The blunt data point on rotation.** The nonlinear-programming and formulation-space
literatures *have* packed squares, and never freely rotating ones.
Lopez and Beasley say arbitrary-angle rotation cannot be dealt with by their approach;
Birgin’s whole rectangle line is orthogonal with at most 90-degree rotation.
Free rotation is where this problem leaves the well-trodden part of the circle
literature, and it is why the mechanisms ranked first in section 10 are the ones that
never needed a potential in the first place.

**One mechanism named here and deliberately not ranked.** Energy landscape paving
(Hansmann and Wille, [arXiv:physics/0201054](https://arxiv.org/abs/physics/0201054),
retained) reweights by a histogram of visited states, so that the crossable barrier
height *grows* with simulation time, the opposite of a cooling schedule.
On a peptide it reached the global minimum in 20 runs of 20 against 8 of 20 for
annealing at equal statistics, and in roughly a third of the sweeps.
It was later carried to circle packing by Liu and collaborators in three papers, **all
closed, none retrieved, and none read**, so there is no packing evidence in hand for it
and it is recorded here as a lead rather than as an option.

<!-- MECHANISM-SECTIONS -->

## 9. What This Repository Has Already Tried in This Direction

Four of these are refutations, and every one of them constrains a recommendation above.
All are recorded in `packing/campaign/`.

- **The fixed-side shrink-and-re-anneal outer loop was built twice and abandoned**
  (`packing/campaign/ideas.md`). The first version crawled, returning `2.875` at `n = 5`
  where the answer is `2.707`; the second never left the grid basin at all, because the
  trivial grid is exactly jammed and no local move escapes it.
  **This is the direct precedent for every inflation and compression scheme below**, and
  it says the loop is not the missing piece.
  What was missing in both attempts is a collective move, which section 1.1 measures and
  exp-135 confirms.
- **A simultaneous all-square perturbation move was then built and measured** (exp-135,
  H-135, 2026-09-08). It takes `n = 17` from exactly `5.0` on every control seed to a
  best of `4.682227`, a gap of `+6.70e-03` from Bidwell against the control’s
  `+3.2447e-01`; `n = 11` from `3.922761` to `3.886755`; `n = 26` from exactly `6.0` to
  `5.746574`; and `n = 10` from `+7.08e-04` to `+3.14e-07`, inside the `1e-4` basin
  proxy on five seeds of five.
  It was nonetheless *rejected* against its declared criterion, because at
  `n = 29, 37, 50, 52` every seed of both arms returned the grid bit for bit.
  The failure is not gradual: above `n = 26` the arm either leaves the grid or it does
  not, and it does not.
- **The cheap aggregate substitute for an inflation objective was measured and refuted**
  (exp-136, H-136). Adding an isotropic `spread` term to the energy improved one cell of
  eleven and regressed three, including both proved controls, returning exactly `2√2` at
  `n = 5` where the control reaches the proved optimum on every seed.
  The verdict names the design error: `required_side` is minimised by a tight square and
  an aggregate spread term is minimised by a disc, so the term optimises a disc.
  **Any pressure-like term below has to carry the container’s shape**, which means a
  per-wall directional force rather than an aggregate.
- **Basin hopping over the LP quench was built and accepted as a proposer** (exp-137,
  H-137), improving four of five cells by `0.06` to `0.13` in median with disjoint seed
  ranges at `n = 10` and `n = 19`, and settling nothing about record finding since no
  run came within `1e-2` of any record.
  Its recorded failure mode is the one section 4 is about: *the LP quench returns
  separations non-negative only to solver tolerance, so an emitted pose needs a monotone
  repair before it is a packing, and the repair scales centres apart and can only raise
  the reported side.*
- **A squared overlap penalty was replaced by a linear one** (`ideas.md`), because the
  squared gradient vanishes as the overlap closes so it never quite reaches zero, while
  the linear penalty has an exact finite-`lambda` constrained optimum.
  That is the same objection section 6 raises against a smooth penalty, already measured
  here.
- **[H-013](../../../packing/campaign/hypotheses/H-013-delta-continuation.md), delta
  continuation, is registered and unbuilt.** Its instrument is described as “a
  fixed-side feasibility/projection operator with a declared delta schedule,
  predictor/corrector residuals, event-level branch identities, common terminal
  classifier and verifier”, and it notes that the existing side-minimising quench is not
  that operator because it erases delta.
  That is a constraint projection under a container schedule, which is section 4’s
  mechanism, so this hypothesis is the registered home for it rather than a new lane.
- **A physics settle was built for the atlas video and answered a question nobody
  asked**
  ([X-025](../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md)).
  Aimed at a known answer with the final snap disabled, the settle still rests one to
  `1.7` units away per square and `0.1` to `1.1` per cent wide; run blind, every
  genuinely packed case loses, by up to `6.8` per cent.
  Raising its annealing dial from level 0 to level 10 more than halves the worst angle
  error twice over while the container side stays flat to within a few tenths of a per
  cent. The exploration’s own caveat is the right one and is repeated here: nothing
  checks that blind run against a real compaction, so those numbers describe that
  simulator with those constants and are not a measurement of the problem.
  What they do show is the section 1.1 signature, in a second instrument: shaking harder
  fixes orientations and does nothing to the side.

## 10. Ranked: What Could Recover a Record Cold, and What Each Needs

The ranking criterion is the question asked: could this mechanism, from a cold start,
return a best-known packing for a non-grid `n < 100`. Four things decide it, and they
are sections 1.1 to 1.4. Does it give every square a way to affect the objective?
Does it need a potential or a derivative the geometry does not have?
Does it terminate at a state the targets actually are?
And has anyone ever run it cold, at scale, on the sibling problem?

### Rank 1. Divide and concur with relaxed-reflect-reflect, over a bounded square container

**Why first.** It is the only mechanism in this document with a published cold,
whole-benchmark result on the sibling problem: 197 values of `n`, up to 400 random
starts each, no information used beyond the target densities, reaching the best known
within `1e-9` on 143 and beating it on 38 (section 4.3). It needs only projections, so
section 1.4 costs it nothing.
It makes the container a variable, so section 1.1 costs it nothing.
Its two halves both exist in the literature and have never been joined: the bounded unit
square on the disk side, the convex-polytope projection on the shape side (section 4.4).

**What it needs to be set up correctly.**

- *Constraint sets.* `A` is the concur set, forcing all replicas of a square’s pose to
  agree; `B` is the divide set, each replica satisfying one constraint independently.
  Constraints per square: `n - 1` pair non-overlaps plus four wall conditions.
  Search space is `O(n^2)` replicas, which the sphere work names as its own scaling
  limit and which at `n <= 100` is at most about `1e4` replicas.
- *The pair projection.* Kallus’s convex-polytope projection, at `d = 2` with eight
  vertices across the pair: enumerate the sixteen cross pairs for the cheapest exact
  separating line, then the larger subsets for least-squares lines, move only the
  winning vertices, then project back to a rigid square.
  A cheaper first cut is available and already implemented here: the minimum translation
  along the best separating axis, `geom::pair_depth` in `sqsearch`. Start with the cheap
  one, because it is the same object whenever the contact is corner-to-edge, and only
  the flat-on-flat case needs the full enumeration.
- *`beta`.* `0.5`, following Elser’s sphere-packing choice and his stated reason that
  smaller values are more productive against nonconvex constraints.
  The theory paper measures clean behaviour only for `beta <= 0.3`, so treat `0.3` and
  `0.5` as the two settings worth an arm and do not use `1.0`, which is the
  Douglas-Rachford limit the same paper models as degenerating.
- *Metric weights.* `lambda_ab -> 0.99 lambda_ab + 0.01 exp(-alpha d_ab)`, with `alpha`
  near 30 for the disk case and near 10 for the polytope case; the polytope work uses
  the interpenetration measure the projection already computes.
- *Container schedule.* The published protocol is a ratchet, not a continuous shrink:
  fix a side, seek a packing, tighten the side on success, repeat until the search
  fails. Start well above the target and stop at the trivial grid’s side as a floor, so a
  run that never beats the grid is recorded as a failure rather than as a grid packing.
- *Restart policy, and this is the part worth copying exactly.* `m`-monotonicity:
  abandon a run as soon as the error fails to improve within `m` iterations, and
  characterise an instance by the `m` at which the success probability is one half.
  That is a published, well-defined way to measure how hard a case is for a method, and
  it is the shape of statistic
  [H-012](../../../packing/campaign/hypotheses/H-012-record-basins-are-rare.md) has been
  waiting for.
- *Success tolerance.* `eps = ||x' - x|| / sqrt(N) < 1e-4` for the projection loop, with
  the resulting pose then handed to the existing `sqpack.verify` at `1e-9` and to the
  fixed-angle LP for the last digits.
  Do not ask the projection loop for the final precision; section 4.3’s own results are
  quoted at `1e-9` after refinement.
- *Budget.* Denominate in refined local optima as the 2026-09-08 survey concluded, not
  in iterations. The disk benchmark used up to 400 starts per `n`; the tetrahedron work
  reached the densest known in 15 runs of 100.

**Honest expectation.** Nobody has run this on squares in a bounded container.
The claim is that it is the best-supported thing to try, not that it will work.

### Rank 2. An adaptive shrinking cell rewritten for a bounded container

**Why second.** It is the mechanism whose authors independently identified this
repository’s measured defect, and named the collective cell move as the fix (section
3.1). It has been run in two dimensions on polygons with exact separating-axis tests and
it reproduces known optima there (section 3.4). Its bounded-container adaptation exists,
in one dimension of one paper, and consists of adding the wall as another linear
inequality (section 3.5). And in the one head-to-head anyone ran, its linear-programming
form beat Lubachevsky-Stillinger on cost and on reach (section 3.3). It ranks second
only because its published results are all periodic, so the transfer is larger than Rank
1’s.

**What it needs to be set up correctly.**

- *Cell variable.* One scalar, the side `s`. The strain move is `s -> s(1 - eps)` with
  every centre rescaled about the container centre by the same factor, which is what
  makes it collective.
  Angles are untouched by the rescale.
- *Move mix.* Particle moves and cell moves, with the ratio of particle moves to cell
  moves above one and rising toward the end of the run, per the published guidance.
  Particle moves equally likely translation and rotation.
- *Acceptance.* Overlap rejects, tested by separating axis, no potential.
  A shrink that survives the overlap test is accepted.
  For the uphill move, prefer the two-dimensional papers’ rule over the
  three-dimensional one: **strictly downhill, no side-increasing move accepted**, with
  the escape coming from the perturbation rather than from uphill acceptance.
  If an uphill arm is wanted, the published alternative is an initial acceptance
  probability of `0.35` decaying as a power law of exponent `-1` toward jamming.
- *Magnitudes.* Tune the particle-move magnitude to a **50 per cent acceptance ratio**,
  cutting it by a constant ratio when acceptance falls significantly below that.
  Tune the strain magnitude separately: take the first feasible strain, shrink the
  maximum strain by a constant ratio after each failure, and reset it at the next strain
  step.
- *Compression schedule.* The published three are 1000, 100 and 10 trial moves per
  particle between strain steps.
  Run at least the slow and fast ones, because the rate-to-outcome dependence is the
  point of the mechanism.
- *Starting density.* Dilute.
  The tetrahedron table moves from `0.695` to `0.823` on this factor alone, and it is
  also the only way to avoid starting at the grid, which sections 1.1 and 9 both say is
  fatal.
- *Termination.* The side decreasing by less than `1e-10` over 100 consecutive strain
  steps, and a contact-generation pass to `6e-10` of the characteristic length, that
  being the published figure for shapes with flat edges, computed **excluding the free
  squares** of section 1.2.
- *Runs.* At least three per case and schedule, as the two-dimensional protocol does,
  and more if the case is being scored.
- *An alternative outer ladder, if the strain move alone stalls.* The circle
  literature’s best cold-recovery result uses a container-shrink ladder instead: shrink
  hard, relax, and keep the diversity, with twenty levels of shrink factor from `0.30`
  to `0.965` in steps of `0.035` and twenty shrunk layouts relaxed per iteration
  (section 8.1). That is a much more violent schedule than a strain move, and it is the
  one that recovered 98 of 100 best-known circle packings.

**The LP variant is the version to build second**, because exp-006 already validated the
fixed-angle linear program over all centres and the side to `4.4e-16` here.
Its published dial is an influence radius: `1.5 D` with strain bound `0.1` gives random
jammed states, `3.5 D` with strain bound `0.01` gives the densest known, and above `4 D`
it generally reaches maximal density.
Termination at a density increase below `1e-8`, halving the bound widths and re-solving
whenever a solution violates impenetrability.

### Rank 3. Continuation on a smoothed separating-axis penalty

**Why third.** It is the cheapest of the three to build here and it has a fully
specified published precedent that recovered known circle optima (section 6). It ranks
below the first two because it does not fix section 1.1 by itself: smoothing the overlap
does nothing about the container objective being a maximum over two to four squares.
It needs the container term to be handled the same way, and that is the untested part.

**What it needs to be set up correctly.**

- *Objective.* Replace the separating-axis maximum over four axis tests by a softmax at
  temperature `tau`, and the enclosing side’s maximum over spans by the same
  construction. Both are maxima; both soften the same way; and softening the *side* is
  the part with no precedent, so it is the part to ablate.
- *Schedule.* Nurmela and Ostergard’s rule: optimise to a local minimum, then double the
  sharpness, and repeat.
  Their exponent runs from a start between 10 and 100 to a stopping point around `1e6`,
  with `1e50` used in a few cases.
- *Rescaling.* Their `lambda` is reset after every step to the square of the current
  shortest distance, to stop the cost underflowing at large sharpness.
  The analogue here is rescaling by the current minimum gap.
- *Optimiser.* Steepest descent with a backtracking line search early, a second-order
  method late, exactly as published.
- *The terminal step is not smooth and must not be treated as smooth.* At small `tau`
  the objective regains the kink exp-006 measured, where Powell and Nelder-Mead both
  lost to plain descent.
  Hand over to the fixed-angle LP with a bracketing search on the angle classes rather
  than continuing with a smooth local model.
- *Restarts.* At least 50 per case from random starts, which is the published figure.
- *Promotion.* Sort the gaps, find the sudden increase, freeze everything below it as a
  contact, and solve the resulting system.
  Section 1.5 says that gap is 97 decades wide at a record here.

### Rank 4. Separating-line angles as continuous variables

**Why here.** Section 8.3’s third source is the only formulation found in either survey
that makes this problem smooth without approximating the geometry, and it does so by
promoting the thing Squarl and exp-006 both treat as a discrete branch, the separating
axis, into a continuous variable.
It is ranked below the first three because it is a formulation rather than a search: it
supplies a better local solver, and something still has to propose.

**What it needs to be set up correctly.**

- *Variables.* The `3n` pose coordinates, the side `s`, and one separating-line angle
  per pair. At `n = 17` that is 52 pose-and-side variables plus 136 angles; at `n = 50`,
  151 plus 1,225.
- *Constraints.* For each pair, both squares on opposite sides of their line, which is
  four vertex inequalities per square per pair and is exact for convex pieces.
  Wall conditions stay as they are.
- *Solver.* An interior-point code, since the published instance uses one at accuracy
  `1e-8`.
- *Seeding.* The published practice is to start from a few predefined orientations and
  release the continuous rotation afterwards, which is exactly the angle-class
  tie-and-release exp-006 measured at 70 LP solves against 1,024 for free descent.
- *The check this needs before it is believed.* Section 1.4 says the objective has a
  corner at the optimum where the active contact set changes.
  Promoting the separating axis to a variable should remove that corner.
  Whether it does is measurable directly at `n = 11`, where exp-006 already has the
  two-sided slopes `0.175` and `0.384` on the shared tilt.
  Re-walk the same slice under the new formulation and see whether the response becomes
  differentiable. That is a cheap, decisive test and it needs no search at all.

### Rank 5. The move-step ladder, which is the cheapest thing on this list

Section 2.5’s phase one is a complete, published, shape-agnostic algorithm that
schedules a step size rather than a potential, and it set four disk records.
Porting it needs no new geometry at all: `sqsearch` already has the poses, the
separating-axis test and the bounding computation.
Settings as published: initial step `0.25`, shrink factor `0.43`, floor `1e-10`,
impatience counter `1000`, disks swept in a random order reset whenever the step
changes, and on collision a direction reset to the sum of repelling vectors over the
obstacles reachable within the current step.
Its natural companion is Boll and colleagues’ rigidity probe: rotate the result by 90
degrees, rerun the finisher, and confirm the same contact set comes back.

It is ranked last among the things worth running because it is a *perturbation*
schedule, and section 1.1 says a perturbation that moves one body at a time inherits the
plateau. Its repelling-vector direction reset is what makes it more than that, and
whether that is enough on squares is exactly the kind of thing an arm settles.

### Rank 6. Constraint projection as a component, not as a search

Independently of Rank 1, the projection operator is worth building on its own, because
exp-137 recorded a specific defect it fixes: the LP quench emits poses whose separations
are non-negative only to solver tolerance, and the current repair scales all centres
apart, which can only raise the reported side.
A projection repair moves only the overlapping pair.
This is a small, testable component with a measured motivation, and it is also the
operator [H-013](../../../packing/campaign/hypotheses/H-013-delta-continuation.md) has
been registered and unbuilt for since the beginning.

## 11. Dead Ends, and Why They Are Dead

Each of these is dead for a stated reason, not for lack of enthusiasm.
Where the reason is a repository measurement rather than a published one, it says so.

- **Lubachevsky-Stillinger event-driven molecular dynamics on rotating squares.** Three
  independent obstructions, any one of which is sufficient.
  The collision time under rotation is transcendental, which the 2021 event-chain paper
  states in as many words, and the only non-spherical generalisation restricts itself to
  shapes with continuously differentiable overlap potentials, which a square does not
  have. The superdisk family, which approaches a square in the limit, was explicitly
  abandoned by its own authors before reaching it for numerical reasons.
  And in two dimensions the protocol crystallises, which for congruent squares means it
  converges to the grid this repository already cannot leave.
  The parallel-square case that does work is the axis-aligned one, which is the trivial
  packing.
- **Contact dynamics as a search.** It has never been used as one, and the near miss
  explains why: the one variant coupled to an external pressure produces random close
  packings whose density is *insensitive* to every dial it exposes.
  Its non-penetration is exact in the contact law and approximate in the discrete gap,
  which section 1.3 disqualifies, since no record has any container slack.
  And its force field is indeterminate exactly at edge-to-edge polygon contact, which is
  every interior contact at the grid.
  It keeps one job here, as the simulator for the “hold a known optimum still” test.
- **Differentiable simulation through contact.** The first-order estimator is biased
  wherever the dynamics are discontinuous, and it is biased with *low* empirical
  variance, so the usual diagnostic does not detect it.
  The measured case closest to this geometry is a ball against a rectangular wall.
  This repository has its own version of the same finding: exp-006 measured a kink at
  the `n = 11` optimum and found two smooth local optimisers worse than plain descent
  there.
- **Differentiating through a position-based solver.** Ruled out by a direct measurement
  rather than an argument: two independent implementations return a position gradient of
  `0.0000` and `-0.0020` where the analytic answer is `-1.0000`, because the projection
  that resolves interpenetration destroys the dependence on the initial condition.
- **Bounding-box overlap surrogates.** The 2026 differentiable-packing work uses one,
  and for congruent squares it is not an approximation but a different problem: two unit
  squares tilted 45 degrees have bounding boxes of side `sqrt(2)`, so the surrogate
  holds them about 41 per cent too far apart, and every interesting record here uses
  tilted squares.
- **Any periodic-cell formulation.** Congruent squares tile the plane, so the periodic
  optimum is density 1 and the `s(n)` question does not arise.
  This is not a guess about the method: the adaptive-shrinking-cell papers exclude the
  cube and the square from their own studies for exactly this reason, and the retained
  torus annealer reports density-one packings for squares whenever `n` is a sum of two
  squares.
- **An aggregate compaction surrogate.** Measured and refuted here, exp-136: an
  isotropic spread term optimises a disc, improved one cell of eleven and regressed
  three including both proved controls.
  A pressure-like term has to carry the container’s shape, which means per-wall and
  directional.
- **A fixed-side shrink-and-re-anneal loop with only single-square moves.** Built twice
  here and abandoned, and section 1.1 says why: at the grid, no single-square proposal
  lowers the side at all.
  Every mechanism in this document that has a container schedule inherits this failure
  unless it also has a collective move.
  That is the whole reason Ranks 1 and 2 are ranked where they are.
- **Handing the whole smooth model to a general nonlinear-programming solver.** The
  quasi-phi-function line publishes the wall: direct solution is “an unrealistic task”
  for more than 15 bodies from a random start and more than 30 from a feasible one.
  That is the same boundary the 2026-09-08 survey found for general-purpose global
  optimisation, which matched the square records to `n = 16` and failed from `n = 17`. A
  smooth global model is a local solver here, not a search.
- **Formulation space search over Cartesian and polar coordinates.** The one retained
  description of it is second-hand, and the paper that applies the idea to squares says
  in its own words that rotation through an arbitrary angle cannot be dealt with by its
  approach. Its squares are axis-aligned.
- **Soft or sequential-impulse two-dimensional rigid-body engines**, meaning the ones a
  game would use. They carry an explicit penetration slop and an error-reduction
  parameter, so the side they report is a function of solver settings.
  Section 1.3 rules them out at `3.7e-33`.

## Key Insights

- **The targets are not jammed, and that is a new measurement.** Of the 36 non-grid
  best-known packings at `n <= 100`, 34 are screened and **30 have at least one square
  the escape screen can translate**, 232 squares in all, of which 76 can be pushed
  clear. Only `n = 5, 11, 28, 40` are fully immobile.
  Every growth-and-jamming mechanism has to declare its jam on the backbone with the
  free squares excluded, and the published protocols already do exactly that.
- **The two-dimensional inflation attractor is the ordered configuration**, said three
  ways by three unrelated sources: the review that says the protocol “typically yields a
  highly crystalline collectively jammed packing in two dimensions”; Gensane and
  Ryckelynck, who say their billiard is “attracted” to configurations with angle zero
  “which are rarely good”; and this repository’s own measurement that no single-square
  proposal lowers the side at the grid.
- **The inflation factor for squares is analytic and the collision time is not.**
  Gensane and Ryckelynck’s Proposition 1 gives the homothety factor at which two rotated
  squares first touch in closed form.
  Event-driven dynamics needs a different object that does not exist in closed form.
  Conflating the two is what makes Lubachevsky-Stillinger look available here.
- **Divide and concur reached 143 of 197 best-known disk packings cold and beat 38 of
  them**, using no information beyond the target densities.
  That is the only cold, whole-benchmark, non-annealing result found in either survey,
  and the projection it needs for squares is already implemented here as
  `geom::pair_depth`.
- **A deforming container beat inflation in the one place both were measured**, on cost
  by a factor of 9 to 23 and on reach by two dimensions.
- **Torquato and Jiao named this repository’s defect in 2009.** The cell strain
  “corresponds to non-trivial collective motions of the particle centroids … It is this
  collective motion that enables the algorithm to explore the configuration space more
  efficiently”, which is section 1.1 written about polyhedra seventeen years before
  exp-134 measured it on squares.
- **Position-based dynamics has never been used as a packing optimiser**, and
  differentiating through it is measurably impossible: two independent implementations
  return a position gradient of `0.0000` and `-0.0020` where the analytic answer is
  `-1.0000`, because the projection that resolves interpenetration destroys the
  dependence on the initial condition.
- **Contact dynamics is a simulator, not a searcher.** The one variant coupled to an
  external pressure produces random close packings whose density is insensitive to every
  dial it exposes, its non-penetration is approximate in the discrete gap, and its force
  field is indeterminate at exactly the edge-to-edge polygon contact this problem is
  full of.
- **Smooth global models of this problem stop in the teens, twice, independently.** The
  quasi-phi-function line publishes a wall at 15 bodies from a random start and 30 from
  a feasible one; general-purpose global optimisation matched the square records to
  `n = 16` and failed from `n = 17`.
- **The one formulation that removes the nonsmoothness exactly** promotes the separating
  line’s angle to a continuous variable, one per pair.
  It is the continuous version of what Squarl and exp-006 both do discretely, and
  whether it removes the kink is testable at `n = 11` against slopes this repository
  already measured.
- **The contact tolerance is not a delicate choice at a converged configuration.** At
  the `n = 29` record the worst contact margin is `3.65694e-100` and the smallest strict
  separation is `0.0116001`, 97.5 decades apart.
  The published two-dimensional protocol for shapes with flat edges uses `6e-10` of the
  characteristic length, well inside that band.
- **Every published continuation schedule found is either geometric in a sharpness
  exponent or linear in a smoothing radius**, and both are specified: double the
  exponent from a start between 10 and 100 until about `1e6`, or ramp the smoothing
  linearly to zero over 10 to 20 levels.
- **The ladders split cleanly by what they schedule.** A ladder on a smoothing parameter
  of the pair potential does not port, because every record-quality disk potential is a
  function of one scalar per pair and a rotating square has no such scalar.
  A ladder on the container or on the move step ports unchanged, and both are published
  in full: twenty shrink levels from `0.30` to `0.965`, and a step from `0.25` shrinking
  by `0.43` to a floor of `1e-10` under an impatience counter of 1,000.

## Limits

- **No mechanism in this document has been run on congruent squares in a square
  container.** Every recovery rate quoted is on disks, spheres, ellipses, polyhedra or a
  distance-geometry problem.
  The transfer arguments are stated where they are made and they are inferences.
- **The adaptive shrinking cell has never been run on a bounded container in two
  dimensions.** The one bounded adaptation found is a cylinder, in one direction, for
  spheres, still periodic axially.
  The claim that the mechanism survives a hard wall rests on that single case.
- **Divide and concur has never been run on a bounded container with polygons.** The
  disk work is bounded and round; the polytope work is periodic and unbounded.
  Joining them is the untested step, and the concur projection for polytopes is
  approximate rather than exact, by its author’s own statement.
- **Four foundational contact-dynamics papers could not be retrieved and were not
  read.** HAL, which hosts the open copies of Moreau 1994, Jean 1999 and Radjai and
  Richefeu 2009, served a bot-check page to every request from this host, and the
  Anitescu-Potra and Stewart-Trinkle complementarity papers are closed with no open
  copy. Everything stated about them here is second-hand from the 2018 review and the
  Chrono paper, both of which were read in full.
- **The two Mladenovic formulation-space-search papers are closed and were not read.**
  What section 8.3 says about them is quoted from a retained secondary source.
- **The three papers that carried energy landscape paving to circle packing are closed
  and were not read**, so section 8.5’s note on it rests on a peptide result and nothing
  else. Two further phi-function sources were nominally open access and returned HTTP 403
  or a truncated capture, so the phi-function definition used here comes from the 2018
  paper rather than from the 2010 one that introduces it.
- **One dynamics-simulation packing paper was not retrieved** and everything said about
  it in the retained 2026 differentiable-packing paper is that paper’s characterisation,
  not this document’s reading.
- **Graduated non-convexity is named in the brief and no source for it was retained.**
  The arXiv sweep returned 40 records, none of them a packing application, and the
  classical statement is a book that could not be obtained here.
  No numeric claim about a graduated-non-convexity schedule appears above.
- **Nothing here was replayed.** Every number is read from a retained source or from
  this repository’s own registers.
  No mechanism was implemented, no run was made, and the ranking in section 10 is an
  argument rather than a measurement.
- **The section 1.2 measurement inherits the escape screen’s own one-sidedness.** A hit
  certifies that one square can be translated; a miss proves only that that square
  cannot be translated at that tolerance.
  Rotation and coordinated multi-square motion are outside the test, so nothing there
  may be restated as rigidity, and `n = 68, 69` are excluded because their witness
  geometry is too coarse.
- **The cost figures are not comparable to each other.** They come from different
  decades, different hardware and different problems, and this document quotes them only
  as the sources state them.
  Two things compared at different budgets have not been compared.

## References

- [Boris D. Lubachevsky, *How to Simulate Billiards and Similar Systems*, J. Comput. Phys. 94:255-283, 1991](https://arxiv.org/abs/cond-mat/0503627)
  (retained at
  `packing/resources/papers/lubachevsky-1991-how-to-simulate-billiards.pdf`)
- [Aleksandar Donev, Salvatore Torquato and Frank H. Stillinger, *Neighbor List Collision-Driven Molecular Dynamics Simulation for Nonspherical Hard Particles*, 2005](https://arxiv.org/abs/physics/0405089)
  (retained)
- [Monica Skoge, Aleksandar Donev, Frank H. Stillinger and Salvatore Torquato, *Packing Hyperspheres in High-Dimensional Euclidean Spaces*, 2006](https://arxiv.org/abs/cond-mat/0608362)
  (retained)
- [Salvatore Torquato and Frank H. Stillinger, *Jammed Hard-Particle Packings: From Kepler to Bernal and Beyond*, Rev. Mod. Phys. 82:2633, 2010](https://arxiv.org/abs/1008.2982)
  (retained)
- [Yang Jiao, Frank H. Stillinger and Salvatore Torquato, *Distinctive features arising in maximally random jammed packings of superballs*, 2010](https://arxiv.org/abs/1001.0423)
  (retained)
- [Marco Klement, Sangmin Lee, Joshua A. Anderson and Michael Engel, *Newtonian Event-Chain Monte Carlo and Collision Prediction with Polyhedral Particles*, 2021](https://arxiv.org/abs/2104.06829)
  (retained)
- [Wm. G. Hoover, Carol G. Hoover and Marcus N. Bannerman, *Single-Speed Molecular Dynamics of Hard Parallel Squares and Cubes*, 2009](https://arxiv.org/abs/0905.0293)
  (retained)
- [David W. Boll, Jerry Donovan, Ronald L. Graham and Boris D. Lubachevsky, *Improving Dense Packings of Equal Disks in a Square*, 2000](https://arxiv.org/abs/math/0405310)
  (retained)
- [Ronald L. Graham and Boris D. Lubachevsky, *Repeated Patterns of Dense Packings of Equal Disks in a Square*, 1996](https://arxiv.org/abs/math/0406394)
  (retained)
- [Robert S. Hoy, *Ultradense jammed packings of ellipses via biased SWAP*, 2024](https://arxiv.org/abs/2409.19196)
  (retained)
- Thierry Gensane and Philippe Ryckelynck, *Improved Dense Packings of Congruent Squares
  in a Square*, Discrete Comput.
  Geom. 34:97-109, 2005
  ([doi:10.1007/s00454-004-1129-z](https://doi.org/10.1007/s00454-004-1129-z); already
  retained, read here for its Proposition 1 and its production procedure calls)
- [Salvatore Torquato and Yang Jiao, *Dense Packings of Polyhedra: Platonic and Archimedean Solids*, Phys. Rev. E 80:041104, 2009](https://arxiv.org/abs/0909.0940)
  (retained)
- [Salvatore Torquato and Yang Jiao, *Robust algorithm to generate a diverse class of dense disordered and ordered sphere packings via linear programming*, Phys. Rev. E 82:061302, 2010](https://arxiv.org/abs/1008.2747)
  (retained)
- [Steven Atkinson, Yang Jiao and Salvatore Torquato, *Maximally dense packings of two-dimensional convex and concave noncircular particles*, Phys. Rev. E 86:031302, 2012](https://arxiv.org/abs/1405.0245)
  (retained)
- [Charles E. Maher, Frank H. Stillinger and Salvatore Torquato, *Kinetic frustration effects on dense two-dimensional packings of convex particles*, 2021](https://arxiv.org/abs/2103.06290)
  (retained)
- [Lin Fu, Paul Steinhardt, Hao Zhao, Joshua E. S. Socolar and Patrick Charbonneau, *Hard sphere packings within cylinders*, Soft Matter 12:2505, 2016](https://arxiv.org/abs/1511.08472)
  (retained)
- [Matthias Mueller, Bruno Heidelberger, Marcus Hennix and John Ratcliff, *Position Based Dynamics*, 2007](https://matthias-research.github.io/pages/publications/posBasedDyn.pdf)
  (retained; the served PDF is the 2006 workshop version of the same work)
- [Miles Macklin, Matthias Mueller and Nuttapong Chentanez, *XPBD: Position-Based Simulation of Compliant Constrained Dynamics*, 2016](https://mmacklin.com/xpbd.pdf)
  (retained)
- [Jan Bender, Matthias Mueller and Miles Macklin, *A Survey on Position Based Dynamics*, Eurographics 2017 course notes](https://animation.rwth-aachen.de/media/papers/2017-EG-CourseNotes.pdf)
  (retained)
- [Simon Gravel and Veit Elser, *Divide and concur: A general approach to constraint satisfaction*, Phys. Rev. E 78:036706, 2008](https://arxiv.org/abs/0801.0222)
  (retained)
- [Yoav Kallus, Veit Elser and Simon Gravel, *A method for dense packing discovery*, 2010](https://arxiv.org/abs/1003.3301)
  (retained)
- Yoav Kallus, *Solving Geometric Puzzles with Divide and Concur*, Cornell thesis, 2011
  (retained at
  `packing/resources/papers/kallus-2011-solving-geometric-puzzles-with-divide-and-concur.pdf`)
- [Veit Elser, *How densely can spheres be packed with moderate effort in high dimensions?*, 2023](https://arxiv.org/abs/2305.13492)
  (retained)
- [Devansh Lal, *The Flow Limit of Reflect-Reflect-Relax*, 2025](https://arxiv.org/abs/2512.23843)
  (retained)
- [Ferenc Unger and Janos Kertesz, *The contact dynamics method for granular media*, 2003](https://arxiv.org/abs/cond-mat/0211696)
  (retained)
- Frederic Dubois, Vincent Acary and Michel Jean, *The Contact Dynamics method: A
  nonsmooth story*, Comptes Rendus Mecanique 346:247-262, 2018 (retained from the
  open-access mirror at
  `packing/resources/papers/dubois-acary-jean-2018-contact-dynamics-method-nonsmooth-story.pdf`)
- [M. Reza Shaebani, Tamas Unger and Janos Kertesz, *Generation of homogeneous granular packings: contact dynamics simulations at constant pressure using fully periodic boundaries*, 2008](https://arxiv.org/abs/0803.3566)
  (retained)
- [Zahra Shojaaee, M. Reza Shaebani, Lothar Brendel, Janos Torok and Dietrich E. Wolf, *An adaptive hierarchical domain decomposition method for parallel contact dynamics simulations of granular materials*, 2012](https://arxiv.org/abs/1104.3516)
  (retained)
- [Tobias Preclik and Ulrich Ruede, *Ultrascale simulations of non-smooth granular dynamics*, 2015](https://arxiv.org/abs/1501.05810)
  (retained)
- [Emily Olsen and Ken Kamrin, *Resolving force indeterminacy in contact dynamics using compatibility conditions*, 2018](https://arxiv.org/abs/1805.07437)
  (retained)
- [Emilien Azema, Nicolas Estrada and Farhang Radjai, *Particle shape dependence in 2D granular media*, 2012](https://arxiv.org/abs/1208.0499)
  (retained)
- Kari J. Nurmela and Patric R. J. Ostergard, *Packing up to 50 Equal Circles in a
  Square*, Discrete Comput.
  Geom. 18:111-120, 1997 (retained at
  `packing/resources/papers/nurmela-ostergard-1997-packing-up-to-50-equal-circles-in-a-square.pdf`)
- Jorge J. More and Zhijun Wu, *Global Continuation for Distance Geometry Problems*,
  Argonne preprint MCS-P505-0395, 1995 (retained; the scan carries no text layer, so an
  OCR aid is retained beside the empty faithful extraction)
- [Kun He, Menglong Ye and Zhengli Wang, *An efficient quasi-physical quasi-human algorithm for packing equal circles in a circular container*, 2018](https://arxiv.org/abs/1611.02323)
  (retained)
- Ernesto G. Birgin and Fabio N. C. Sobral, *Minimizing the object dimensions in circle
  and sphere packing problems*, Comput.
  Oper. Res. 35:2357-2375, 2008 (retained)
- Ernesto G. Birgin and Jan M. Gentil, *New and improved results for packing identical
  unitary radius circles within triangles, rectangles and strips*, 2010 (retained)
- Tetyana Romanova, Julia Bennell, Yurij Stoyan and Alexander Pankratov, *Packing of
  concave polyhedra with continuous rotations using nonlinear optimisation*, Eur.
  J. Oper. Res., 2018 (retained)
- Jeinny Peralta, Marina Andretta and Jose Fernando Oliveira, *Solving irregular strip
  packing problems with free rotations using separation lines*, 2018 (retained)
- Jose Luis Lopez and John E. Beasley, *Packing unequal rectangles and squares in a
  fixed size circular container using formulation space search*, 2018 (retained)
- [The simulation methods source audit, 2026-09-09](../../../packing/resources/web/simulation-methods-audit-2026-09-09/README.md):
  the query receipts, the acquisition manifest with hashes, the readings checked against
  the retained bytes, the screened-out material and every attempted and failed retrieval
- [Annealing for square packing, and how far it actually reaches](research-2026-09-08-annealing-for-square-packing.md),
  which this document extends
- [Algorithms and tooling for square packing](research-2026-08-22-square-packing-algorithms-and-tooling.md)
- Campaign artifacts: exp-006, exp-011, exp-012, exp-134, exp-135, exp-136, exp-137,
  exp-138; hypotheses H-002, H-004, H-012, H-013, H-019, H-135, H-136, H-137;
  exploration
  [X-025](../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md)
- Repository artifacts read directly:
  `packing/atlas/known-best/translation-escape-screen.json`,
  `packing/atlas/known-best/contact-structures.json`, and
  `packing/devtools/screen_jamming_targets.py`, which produced the section 1.2 table

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
