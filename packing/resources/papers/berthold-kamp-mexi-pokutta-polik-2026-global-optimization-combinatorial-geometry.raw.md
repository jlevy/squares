                                                             Global Optimization for
                                                         Combinatorial Geometry Problems
                                                           Revisited in the Era of LLMs

                                              Timo Berthold1,2 , Dominik Kamp3 , Gioni Mexi3 , Sebastian Pokutta2,3 , and
                                                                            Imre Pólik4
arXiv:2601.05943v1 [math.OC] 9 Jan 2026




                                                    1
                                                        Fair Isaac Deutschland GmbH, Germany, timoberthold@fico.com
                                                    2
                                                        Technische Universität Berlin, Institut für Mathematik, Germany
                                                                        3
                                                                          Zuse Institute Berlin, Germany
                                                                4
                                                                  Fair Isaac Corporation, USA, imre@polik.net



                                                  Abstract. Recent progress in LLM-driven algorithm discovery, exem-
                                                  plified by DeepMind’s AlphaEvolve, has produced new best-known so-
                                                  lutions for a range of hard geometric and combinatorial problems. This
                                                  raises a natural question: to what extent can modern off-the-shelf global
                                                  optimization solvers match such results when the problems are formu-
                                                  lated directly as nonlinear optimization problems (NLPs)?
                                                  We revisit a subset of problems from the AlphaEvolve benchmark suite
                                                  and evaluate straightforward NLP formulations with two state-of-the-art
                                                  solvers, the commercial FICO Xpress and the open-source SCIP. With-
                                                  out any solver modifications, both solvers reproduce, and in several cases
                                                  improve upon, the best solutions previously reported in the literature,
                                                  including the recent LLM-driven discoveries. Our results not only high-
                                                  light the maturity of generic NLP technology and its ability to tackle
                                                  nonlinear mathematical problems that were out of reach for general-
                                                  purpose solvers only a decade ago, but also position global NLP solvers
                                                  as powerful tools that may be exploited within LLM-driven algorithm
                                                  discovery.

                                                  Keywords: nonlinear optimization · circle packing · hexagon packing ·
                                                  distance ratio


                                          1     Introduction
                                          The rapid progress in global optimization technology over the past decade has
                                          substantially expanded the range of nonlinear, nonconvex problems that can
                                          be solved to proven global optimality, or at least to very high-quality solutions
                                          with reliable dual bounds. State-of-the-art academic solvers like SCIP [20] and
                                          commercial solvers like FICO® Xpress [3] combine spatial branch-and-bound,
                                          automatic linearization and convexification, sophisticated presolving, and in-
                                          creasingly powerful primal heuristics [4,5,6], enabling them to solve instances
                                          that would have been considered computationally prohibitive only a few years
                                          ago.
2      T. Berthold et al.

    At the same time, recent developments in algorithm design based on Large
Language Models (LLMs) have drawn renewed attention to long-standing ge-
ometric and combinatorial problems that can be formulated as nonlinear op-
timization models. Specifically, DeepMind presented the AlphaEvolve frame-
work [19,25], which uses LLM-generated code in an evolutionary search to pro-
duce high-quality solutions for an extensive set of mathematical problems, in-
cluding variants of circle packing, hexagon packing, and minimum-distance con-
figurations of points. These breakthrough results raise a natural question: to
what extent can state-of-the-art global optimization solvers match, or even sur-
pass, such automatically discovered algorithms on challenging nonlinear prob-
lems?
    More broadly, the last few years have seen rapid progress in LLM-driven dis-
covery workflows that couple generative models with structured search and auto-
mated evaluation or verification. FunSearch combines an LLM with evolutionary
program search and task-specific evaluators, enabling improvements for several
discrete mathematical and algorithmic problems [28]. Complementary advances
include AlphaDev, which used learning-based search to rediscover and improve
low-level algorithms such as sorting routines [24], and AlphaGeometry, which
combines neural generation with symbolic reasoning to solve olympiad-level ge-
ometry problems without human demonstrations [33]. Related LLM+evolution
approaches have also been used to design effective heuristics for combinatorial
optimization [23]. Taken together, these advances motivate revisiting classical
mathematical optimization as a competitive and reliable baseline on the same
challenging benchmarks.
    In this work we revisit three problems from the AlphaEvolve benchmark
suite and study them through the lens of Nonlinear Programming (NLP). An
NLP is an optimization problem minimizing a nonlinear objective function over
a feasible set defined by nonlinear constraints on continuous variables:

                   min{f (x) | gk (x) ≤ 0, ∀k ∈ K, ℓ ≤ x ≤ u},                 (1)

where the objective f (x) and all constraint functions gk : Rn → R are factorable
and all variable bounds ℓ, u ∈ R̄ := R ∪ {±∞}. The set K := {1, . . . , m} indexes
the constraints. The circle packing problem, the minimum-distance ratio prob-
lem and the hexagon packing problem admit compact NLP models. This makes
them good showcases for the power of modern global optimization tools: these
combinatorial problems can be very intuitively modelled and effectively solved
in their most natural form, as nonlinear optimization instances. We show that
combined with off-the-shelf global optimization technology, these straightforward
NLP formulations not only reproduce the best solutions reported in [19,25], but
in several cases produce significantly better solutions. Our goal in doing so is to
illustrate the power of modern general-purpose nonlinear optimization solvers
rather than to perform a head-to-head comparison of solvers.
    Next to presenting simple formulations that work and identifying some key
modeling decisions that drive performance, our main contributions are:
                 Global Optimization for Combinatorial Geometry Problems            3

Stronger solutions with unmodified solvers. With off-the-shelf Xpress and SCIP
we obtain solutions that match, and in multiple cases improve, previously re-
ported best-known results. Some problems were solved with only one solver,
some used both. In this paper we do not make a distinction of which solver
found which solution. All the solutions that our solvers produced were verified
using the validation code in the AlphaEvolve repository.

Lessons learned. We reflect on the respective strengths and limitations of LLM-
based approaches and nonlinear optimization, discuss modeling insights, and
how global optimization software has become a complementary, industry-ready
tool for challenging combinatorial problems.
    These insights are discussed in Section 5, while Sections 2–4 present one
model each, together with the accompanying computational results. Due to lack
of space we will not comment on the dual bounds and how they could be im-
proved (such as stronger formulations or symmetry breaking), even though it is
a key differentiator between ad-hoc heuristics and general optimization solvers.


2     Minimizing the Ratio of Maximum to Minimum
      Distance

The problem of minimizing the ratio between the maximum and minimum pair-
wise distances in a finite point set, called the min-max ratio problem, has its
origins in classical extremal geometry. Bateman and Erdős [2] formulated the
question in terms of determining, for a given number of points, the configura-
tion of points in the plane with mutual distances at least one that minimizes
the diameter of the set. This is equivalent to minimizing the ratio of largest
to smallest distance when the minimum is normalized to one. Bateman and
Erdős provided optimal solutions for n ≤ 7 in two dimensions. David Cantrell,
see, e.g., [16], has contributed many best-known solutions in both 2D and 3D,
while Audet et al. formulated the problem explicitly as a nonlinear optimization
model and found some improving configurations for n ≤ 30, using derivative-free
optimization techniques [1].


2.1   Optimization model

In a slightly more general form, for given positive integers n and d, the goal
of the min-max ratio problem is to find n distinct points in d-dimensional Eu-
clidean space Rd such that the ratio between the maximum and the minimum
pairwise distance is minimized. This problem seeks a configuration of points that
is as evenly spaced as possible, minimizing clustering and maximizing spatial ef-
ficiency. Let N = {1, 2, . . . , n} denote the set of points and D = {1, 2, . . . , d}
denote the set of dimensions. We define the following decision variables:

xi,k ∈ R: coordinate of point i ∈ N in dimension k ∈ D
tmin ∈ R+ : minimum squared distance between any two points
4        T. Berthold et al.

tmax ∈ R+ : maximum squared distance between any two points
r ∈ R+ : squared ratio variable, defined as r = ttmax
                                                  min

The first observation is that it is more convenient and efficient to work with the
ratio of the squared distances and avoid the square roots. For any pair of points
i, j ∈ N , the squared Euclidean distance is given by:
                                     X
                              d2ij =    (xi,k − xj,k )2
                                         k∈D

A key insight is that this problem exhibits scale-invariance: the optimal objec-
tive value remains unchanged if all lengths are multiplied by the same constant
factor. We can therefore normalize the problem by fixing either tmin or tmax
without loss of generality. This simplifies the formulation by reducing the num-
ber of nonlinear terms, thereby benefiting the solution process. We present two
equivalent formulations:

Circle Packing Formulation By fixing tmin = 1, the problem becomes a variant
of the uniform circle packing problem where points maintain a pairwise distance
of at least 1, with the maximum distance to be minimized. The optimization
problem can be formulated as:

                                min tmax                                            (2)
                      X
               s.t.         (xi,k − xj,k )2 ≥ 1,       for all i, j ∈ N , i < j     (3)
                      k∈D
                      X
                            (xi,k − xj,k )2 ≤ tmax ,   for all i, j ∈ N , i < j     (4)
                      k∈D
                                     tmax ≥ 1                                       (5)

Constraints (3) ensure that all pairwise squared distances are at least5 1, while
constraints (4) bound them by tmax . Minimizing tmax is then equivalent to min-
imizing the ratio r = tmax
                        1 = tmax .

Dual Formulation. Alternatively, fixing tmax = 1 yields a dual perspective where
we maximize the minimum distance subject to a unit bound on the maximum
distance:

                                max tmin                                            (6)
                      X
               s.t.         (xi,k − xj,k )2 ≥ tmin ,   for all i, j ∈ N , i < j     (7)
                      k∈D
                      X
                            (xi,k − xj,k )2 ≤ 1,       for all i, j ∈ N , i < j     (8)
                      k∈D
                                 0 ≤ tmin ≤ 1                                       (9)
5
    For any (locally) optimal solution some of the inequalities in (3) will be satisfied
    with equality, otherwise the solution could be trivially improved by scaling.
                 Global Optimization for Combinatorial Geometry Problems          5

                                                                        1
Maximizing tmin is then also equivalent to minimizing the ratio r = tmin   . Again,
this simple flip renders a nonlinear rational objective into a linear objective,
which is preferable for the solution process.
    Both formulations yield nonconvex quadratically constrained optimization
problems (QCPs) that can be solved efficiently by modern global optimization
solvers. In our experiments the first model performed slightly better, but the
difference was not very significant.
    The power of the mathematical modeling approach is that we can handle
point configurations in any dimension with the same model. Crucially, and this
may be one of the reasons why optimization solvers perform great on this prob-
lem, the model is essentially unconstrained (at least in its original form): any
finite set of points has a largest and smallest pairwise distance, so their ratio is
well-defined. There is no extra constraint that the point set has to satisfy (such
as inclusion in a bounding region). The constraints get introduced only through
the auxiliary variable for the objective.


2.2   Computational Results

We implemented the above model in the Mosel modeling language [14]. The re-
sulting instances range in size from 7 variables and 10 constraints (three points
in two dimensions) to 91 variables and 876 constraints (30 points in three dimen-
sions). The improving solutions (rounded up to five decimal places) reported in
Table 1 were obtained with this approach, and the corresponding configurations
for the 2d case are illustrated in Figure 1. For many additional instances, the
method reproduced the currently best-known solutions.


           d     n    Squared distance ratio    Previous best    Source
           2    16                 12.88924          12.88927    [19,25]
           2    21                 17.77499            17.776       [16]
           2    22                 19.05398            19.055       [16]
           2    29                 25.92460            25.929        [1]
           3    14                   4.16578          4.16585    [19,25]

Table 1. Improving solutions for the min-max distance ratio problem in 2D and 3D




3     Packing Circles inside a Square or a Rectangle

The study of packing circles in polygonal regions dates back almost 200 years [9].
One of the most studied variants concerns packing a fixed number of unit circles
into the smallest possible square; a good survey is given by Peikert [26]. For most
instances of up to twenty circles, exact optimal packings are known and can be
6                      T. Berthold et al.
                                             √                                                     √                                                            √                                                              √
       16 points, distance ratio ∼               12.88924           21 points, distance ratio ∼        17.77499           22 points, distance ratio ∼               19.05398             29 points, distance ratio ∼               25.92460
 2.5
                                                             2.5                                                   2.0                                                            3.0
 2.0                                                                                                                                                                              2.5
                                                                                                                   1.5
                                                             2.0
 1.5                                                                                                                                                                              2.0
                                                                                                                   1.0
                                                             1.5
                                                                                                                                                                                  1.5
 1.0                                                                                                               0.5
                                                             1.0                                                                                                                  1.0
                                                                                                                   0.0
 0.5                                                         0.5                                                                                                                  0.5
                                                                                                                   -0.5
                                                             0.0                                                                                                                  0.0
 0.0
                                                                                                                   -1.0                                                           -0.5
                                                             -0.5
-0.5                                                                                                               -1.5                                                           -1.0
                                                             -1.0
                                                                                                                   -2.0                                                           -1.5
-1.0
                                                             -1.5                                                                                                                 -2.0
                                                                                                                   -2.5
        -2.5   -2.0   -1.5   -1.0   -0.5   0.0   0.5   1.0           -4.0 -3.5 -3.0 -2.5 -2.0 -1.5 -1.0 -0.5 0.0          -2.0 -1.5 -1.0 -0.5 0.0   0.5   1.0   1.5   2.0   2.5          -5.0 -4.5 -4.0 -3.5 -3.0 -2.5 -2.0 -1.5 -1.0 -0.5 0.0




Fig. 1. Graphical representation of the solutions for the distance ratio problem in 2D.
Red lines indicate maximum distance pairs, blue lines indicate minimum distance pairs.



derived using algebraic geometry techniques based on polynomial systems and
Gröbner basis computations, see, e.g., [11].
    In this work, we investigate a variant for which it is harder to prove optimality
since both the positions and radii of the circles are decision variables. Specifically,
we consider packing circles of variable radii into a unit square, or, in a mild
relaxation, into a rectangle of perimeter four, while maximizing the sum of their
radii. Best-known solutions are mostly due to Cantrell [17], but optimality proofs
are only known for some trivial cases.



3.1               Optimization model


Given a positive integer n, we consider the problem of packing n circles inside
a rectangle such that the sum of their radii is maximized. We examine two
variants: packing circles into any rectangle of perimeter 4, and the special case
of packing circles into a unit square (which has perimeter 4). A key advantage
of mathematical optimization approaches is that the optimization model can be
changed easily. This facilitates exploring related problems by simply adding or
modifying constraints, such as for the two problem variants shown below.
    Let N = {1, 2, . . . , n} denote the set of circles. We define the following deci-
sion variables:

(xi , yi ) ∈ R2 : coordinates of the center of circle i ∈ N
ri ∈ R+ : radius of circle i ∈ N
α ∈ R+ : width of the rectangle

We consider the problem of packing circles in a rectangle with fixed perimeter
P = 4 and variable side lengths. We introduce a decision variable α representing
the width and set the height to H = P2 − α = 2 − α. We can assume without loss
of generality that α ≤ 1 (i.e., α is the shorter side). The optimization problem
                 Global Optimization for Combinatorial Geometry Problems              7

can be formulated as:
                               X
                        max          ri                                             (10)
                               i∈N

                       s.t.   ri ≤ xi ≤ α − ri ,         for all i ∈ N              (11)
                              ri ≤ yi ≤ (2 − α) − ri ,   for all i ∈ N              (12)
                   2                 2             2
         (xi − xj ) + (yi − yj ) ≥ (ri + rj ) ,          for all i, j ∈ N , i < j   (13)
                              0 ≤ ri ≤ α2 ,              for all i ∈ N              (14)
                               0<α≤1                                                (15)

The objective (10) is to maximize the sum of all radii. Note that this is fun-
damentally P different from maximizing the total area covered by circles, which
would be π i∈N ri2 , whereas the linear objective tends to favor more balanced
distributions of circle sizes. Constraints (11) and (12) ensure that each circle
remains entirely within the rectangle: the center coordinates must maintain a
distance of at least ri from all rectangle boundaries. Constraints (13) ensure that
no two circles overlap by requiring that the Euclidean distance6 between any pair
of circle centers is at least the sum of their radii. Constraints (14) provide an
upper bound on each radius: no circle can have a diameter exceeding the width
of the rectangle α (which is the shorter side by assumption). Finally, constraint
(15) bounds the width variable.
    The aspect ratio determined by α is a decision variable that can be modified
to maximize the sum of radii for a given number of circles. We can trivially change
this formulation to packing into a unit square by fixing α = 1. This is a crucial
property of mathematical optimization modeling: the user needs to change only
the model and does not have to worry about whether this changes the algorithm:
the solvers will take care of that. This contrasts with many heuristic approaches,
including LLM-generated ones, in which a new set of heuristics often needs to
be developed once the model formulation changes.
    Again, we have only linear and nonconvex quadratic constraints.


3.2   Computational Results

First, let us focus on the restricted problem, packing circles into a square. The
following improving solution (floored to five decimal digits) has been found7 with
both solvers (see Table 2). The solution is visualized in Figure 2.
    Now we can turn to the slightly relaxed version, where instead of a square
we are trying to pack into a rectangle of perimeter 4. Obviously, all the previous
solutions are still feasible for this relaxed problem, but we can do slightly better.
6
  Similar to the distance ratio problem, it is again advantageous to work with squared
  distances.
7
  We have found possibly even more improving solutions, but the original source [17]
  for the best-known packings lists only three digits after the decimal. In almost all
  cases, we managed to match the best-known solutions from literature.
8             T. Berthold et al.


                      Variant             n             Sum of radii             Previous best          Source
                      square              32                     2.93957              2.93794           [19,25]
                     rectangle            26                 2.63930                     2.638                [16]
                     rectangle            27                 2.69015                     2.687                [16]

                     Table 2. Improving solutions for the circle packing problem



We found the following improving solutions, again floored to five decimal digits
(see Table 2). The solutions are visualized in Figure 2. Not surprisingly, the
solutions all tend to use a rectangle that is almost square.


              32 circles in unit square         26 circles in rectangle, perimeter 4.0 27 circles in rectangle, perimeter 4.0
     1.0                                          1.0                                    1.0



     0.8                                          0.8                                    0.8



     0.6                                          0.6                                    0.6



     0.4                                          0.4                                    0.4



     0.2                                          0.2                                    0.2



     0.0                                          0.0                                    0.0
        0.0    0.2    0.4   0.6    0.8    1.0        0.0   0.2     0.4   0.6   0.8          0.0   0.2   0.4    0.6   0.8




Fig. 2. Graphical representation of the solutions for the circle packing problem. Left:
square variant (n=32). Middle and right: rectangle variant (n=26, n=27).




4    Packing Unit Regular Hexagons inside a Regular
     Hexagon
Packing various shapes into other shapes in an optimal way has a vast literature,
from classical geometry problems and puzzles [8,15], to packing problems solved
for designing packaging and packing boxes into shipping containers [10,35]. In
general, the more complicated the shape to be packed is, the harder the problems
become both to analyze theoretically and to solve practically. Problems with unit
circles are well-studied (compare Section 3), but more complex shapes are often
only handled with ad-hoc heuristics.
    In this section we consider the problem of packing n regular hexagons with
unit side length into a regular hexagon of minimum side length R. Each in-
ner hexagon can be positioned and rotated freely. This problem is significantly
more involved than circle packing due to the possible rotation of the non-circular
geometry of hexagons. However, it is a special case of the polygon packing prob-
lem, where two-dimensional geometrical objects bounded by an arbitrary closed
                   Global Optimization for Combinatorial Geometry Problems                  9

sequence of non-intersecting line segments must be packed into a container in
some efficient way. An optimization model for the polygon packing problem with
a fixed size container was developed by [22], which was later generalized to convex
objects by [32] and afterwards even further to also allow nonconvex objects by
[27]. These approaches construct so-called quasi-phi-functions for certain object
geometries to formulate pairwise non-overlapping conditions among them. The
following hexagon packing formulation adopts this approach in a simplified way
by defining Farkas multipliers (see, e.g., [7]) on pairwise hexagon intersections
in order to exclude interior overlaps, respectively.


4.1     Optimization model

Let N = {1, 2, . . . , n} denote the set of inner hexagons and S = {0, 1, 2, 3, 4, 5}
denote the six sides of any hexagon. We use the following geometric constants:
      √
ρ = 23 : inradius (distance from center to edge, also called apothem)
ϕ = π3 : angular separation between adjacent vertices

We define the following decision variables:

R ∈ R+ : side length of the outer hexagon (to be minimized)
(xi , yi ) ∈ R2 : coordinates of the center of inner hexagon i ∈ N
θi ∈ [0, ϕ]: rotation angle of inner hexagon i ∈ N

To facilitate the formulation of the geometric constraints we introduce:

ai,j , bi,j ∈ R: normal vector components for side j ∈ S of hexagon i ∈ N
ci,j ∈ R: offset term for side j ∈ S of hexagon i ∈ N
λi,j,k ∈ R+ : Farkas multipliers for separation of hexagons i, j ∈ N with i < j,
      where k ∈ {1, . . . , 12}

The optimization problem can be formulated as:

                                             min R                                        (16)
                                                   
      s.t.   Rρ + sin(kϕ) xi + sin(θi + (j + 0.5)ϕ)
                                                   
                + cos(kϕ) yi + cos(θi + (j + 0.5)ϕ) ≥ 0, ∀i ∈ N , j, k ∈ S                (17)
                                    ai,j = sin(θi + jϕ),              ∀i ∈ N , j ∈ S      (18)
                                    bi,j = cos(θi + jϕ),              ∀i ∈ N , j ∈ S      (19)
                              ci,j = ai,j xi + bi,j yi − ρ,           ∀i ∈ N , j ∈ S      (20)
                                                    12
                                                    X
                                                          λi,j,k = 1, ∀i, j ∈ N , i < j   (21)
                                                    k=1
                    5
                    X                       5
                                            X
                          λi,j,k+1 ai,k +         λi,j,k+7 aj,k = 0, ∀i, j ∈ N , i < j    (22)
                    k=0                     k=0
10     T. Berthold et al.

                 5
                 X                       5
                                         X
                       λi,j,k+1 bi,k +         λi,j,k+7 bj,k = 0, ∀i, j ∈ N , i < j   (23)
                 k=0                     k=0
                 5
                 X                       5
                                         X
                       λi,j,k+1 ci,k +         λi,j,k+7 cj,k ≥ 0, ∀i, j ∈ N , i < j   (24)
                 k=0                     k=0

                                                    0 ≤ θi ≤ ϕ, ∀i ∈ N                (25)
                                                     λi,j,k ≥ 0, ∀i, j, k             (26)
                                                              √
                                                         R≥ n                         (27)

    Constraints (17) ensure that all vertices of each inner hexagon lie within the
outer hexagon. For a regular hexagon centered at (xi , yi ) with rotation angle θi ,
the vertices are located at positions (xi + sin(θi + (j + 0.5)ϕ), yi + cos(θi + (j +
0.5)ϕ)) for j ∈ S. Each vertex must satisfy all six half-space constraints defining
the outer hexagon.
    Constraints (18)–(20) define the half-space representation of the inner hexagons.
Each side j ∈ S of hexagon i ∈ N is characterized by a normal vector (ai,j , bi,j )
and an offset ci,j , representing the inequality ai,j x + bi,j y ≥ ci,j .
    Constraints (21)–(24) represent Farkas-based separation conditions to ensure
that no two inner hexagons overlap. These constraints are based on the Farkas
lemma for certifying infeasibility of sets of linear constraints. For each pair of
hexagons (i, j) with i < j, we introduce 12 Farkas multipliers λi,j,k (one for each
side of the two hexagons). The constraints ensure that the mutual system of
inequalities defining the intersection of both hexagons is degenerate, i.e., no point
can simultaneously lie in the interior of both hexagons, thereby guaranteeing
non-overlapping configurations.
    Constraint (25) restricts the rotation angle to [0, ϕ] due to the six-fold rota-
tional symmetry of regular hexagons because rotations beyond ϕ are equivalent
to rotations within this range. Finally, the lower bound on R (27) is implied by
elementary geometry. The area of the outer hexagon must be at least the total
area of the n contained unit hexagons.
    Due to the trigonometric functions, these problems are general nonconvex
nonlinear. Even worse, there are nonlinear equality constraints in the formulation
we presented. This can pose a challenge to any solution approach, as equations
are naturally harder to satisfy. Global solvers handle this challenge in various
ways (both Xpress and SCIP use an outer approximation method). At the same
time, the stronger constrainedness makes this problem also more challenging to
create ad-hoc heuristics for. This is the area where we can report the largest
improvements over the previous best solutions, indicating that modern global
solvers are well positioned for this strongly constrained problem – a situation
that we are used to from mixed-integer linear optimization for years.
    The solution approach can easily be adapted to pack other regular polygons
(triangles, squares, pentagons, etc.) by just changing n, recomputing ρ, ϕ, and
rerunning the solver. Actually, any convex polyhedral objects can be handled
in a structurally similar way even in higher dimensional domains as long as the
                            Global Optimization for Combinatorial Geometry Problems                                                                    11

linear outer formulations are known because the non-overlapping constraints
solely rely on the definition of feasible Farkas multipliers for the intersections.
This is one example that demonstrates the generalizable nature of mathematical
optimization.


4.2   Computational Results

The following solutions were produced (often within minutes) with a run using
only default settings. The solvers managed to match the best-known solutions
for up to 10 hexagons. After that, we found solutions that were better than
the best-known solutions, except for 13 hexagons, where the known trivial (and
most likely, optimal) solution with side length 4 was reproduced. In particular,
the following improving solutions have been found, ceiled to five decimal digits
(see Table 3 and Figure 3).


                  n         Side of containing hexagon                                                Previous best                    Source
                  11                                                       3.92485                               3.93010               [19,25]
                  12                                                       3.94165                               3.94192               [19,25]
                  14                                                       4.26900                               4.27240                  [18]
                  15                                                       4.44769                               4.45406                  [18]
                  16                                                       4.52788                               4.53633                  [18]

             Table 3. Improving solutions for the hexagon packing problem




                      11 Hexagon Packing                                   12 Hexagon Packing                                 14 Hexagon Packing
                                                                                                                     4


         2                                                    2                                                      2


         0                                                    0                                                      0


        −2                                                −2                                                     −2


                                                                                                                 −4
             −4        −2     0            2          4           −4        −2       0            2          4           −4     −2    0     2      4
                                               15 Hexagon Packing                                     16 Hexagon Packing
                                  4                                                      4


                                  2                                                      2


                                  0                                                      0


                              −2                                                     −2


                              −4                                                     −4
                                      −4         −2       0            2         4           −4         −2       0        2      4




 Fig. 3. Graphical representation of the solutions for the hexagon packing problem
12      T. Berthold et al.

5    Conclusion

Code-generating LLMs provide an effective entry point into new problem do-
mains and ideally facilitate a technology-agnostic exploration of solution ap-
proaches. In the context of the present work, they also helped to draw attention
to classical problems where further improvements are still possible and that had
not been revisited by mathematical optimization approaches for some time. Our
results show that off-the-shelf global optimization software can solve straightfor-
ward formulations of hard combinatorial geometry problems within seconds or
minutes. This highlights the substantial progress achieved in recent years and
suggests that nonlinear optimization is approaching the role that (mixed-integer)
linear optimization has played for at least two decades: a robust, performant,
readily available black-box technology.
    At the same time, mathematical optimization can meet several expectations
often associated with LLM-based approaches. Combinatorial and other math-
ematical problems can be formulated in a very natural way, and changes in
the problem definition typically require only minor modifications to the model
and are thereby quickly realized. Solutions can then be obtained quickly, pre-
sumably considerably faster than generating, refining, and testing solver-specific
code through dozens of LLM-driven code-generation iterations.
    Nevertheless, the two technologies should not be viewed as competing, but
rather as complementary. The solution-method-agnostic prototyping capabili-
ties of an LLM-based code generation are a powerful tool for exploring new
problems and formulating new solution approaches. Curiously, in a study with
OpenEvolve [31] on a problem of packing 26 circles specifically, the LLM con-
verged to using an optimization approach [30], namely a Sequential Least Squares
Programming formulation with a local solver implemented in SciPy [29,34]. Fur-
thermore, the concept of using LLMs as a support tool for the authoring of
optimization models, as, e.g., in [12,13,21] is a very promising one.
    It is noteworthy that in our experiments the smallest improvements were
observed for the relatively unconstrained min-max ratio problem, whereas the
largest gains were achieved for the highly constrained hexagon packing problem.
Although based on a limited set of examples, this suggests that optimization-
based approaches become increasingly competitive the more constrained the
problems are. Since real-world industrial problems are typically characterized
by large and diverse constraint sets, these observations further support the view
that global optimization has matured into an industry-ready technology.

Acknowledgments. We are grateful for the contributions of Liding Xu (ZIB) and
the FICO Xpress team, in particular Bruno Vieira and Susanne Heipcke, for their
contributions during an early phase of this project.
    Research reported in this paper was partially supported through the Research Cam-
pus Modal funded by the German Federal Ministry of Education and Research (fund
numbers 05M14ZAM,05M20ZBM) and the Deutsche Forschungsgemeinschaft (DFG)
through the DFG Cluster of Excellence MATH+.
                  Global Optimization for Combinatorial Geometry Problems            13

References

 1. Audet, C., Fournier, X., Hansen, P., Messine, F.: A note on diameters of point sets.
    Optimization Letters 4(4), 585–595 (2010)
 2. Bateman, P., Erdős, P.: Geometrical extrema suggested by a lemma of Besicovitch.
    The American Mathematical Monthly 58(5), 306–314 (1951)
 3. Belotti, P., Berthold, T., Gally, T., Gottwald, L., Pólik, I.: Solving MINLPs to
    global optimality with FICO Xpress Global. Optimization pp. 1–19 (2025). https:
    //doi.org/10.1080/02331934.2025.2595437
 4. Berthold, T.: Heuristic algorithms in global MINLP solvers. Ph.D. thesis, Technis-
    che Universität Berlin (2014)
 5. Berthold, T.: A computational study of primal heuristics inside an MI(NL)P solver.
    Journal of Global Optimization 70(1), 189–206 (2018). https://doi.org/10.1007/
    s10898-017-0600-3
 6. Berthold, T., Lodi, A., Salvagnin, D.: Primal Heuristics in Integer Programming.
    Cambridge University Press (2025)
 7. Bertsimas, D., Tsitsiklis, J.N.: Introduction to linear optimization, vol. 6. Athena
    scientific Belmont, MA (1997)
 8. Bezdek, K.: Classical topics in discrete geometry. Springer Science & Business
    Media (2010)
 9. Bolyai, W.: Tentamen Juventutem Studiosam in Elementa Matheseos Purae, El-
    ementaris Ac Sublimioris. Typis Collegii Reformatorum, Marosvásárhely (1832),
    two volumes
10. Bortfeldt, A., Wäscher, G.: Constraints in container loading–a state-of-the-art re-
    view. European Journal of Operational Research 229(1), 1–20 (2013)
11. Buchberger, B.: A theoretical basis for the reduction of polynomials to canonical
    forms. ACM SIGSAM Bulletin 10(3), 19–29 (1976)
12. Chen, H., Constante-Flores, G.E., Mantri, K.S.I., Kompalli, S.M., Ahluwalia, A.S.,
    Li, C.: Optichat: Bridging optimization models and practitioners with large lan-
    guage models. INFORMS Journal on Data Science (2025)
13. Chen, Z., Zhang, X., Zope, H., Barbalho, H., Mellou, K., Molinaro, M., Kulkarni, J.,
    Menache, I., Li, S.: OptiMind: Teaching LLMs to think like optimization experts.
    arXiv preprint arXiv:2509.22979 (2025)
14. Colombani, Y., Heipcke, S.: Mosel: an extensible environment for modeling and
    programming solutions. In: Proceedings of CP-AI-OR. vol. 2, pp. 277–290 (2002)
15. Conway, J.H., Sloane, N.J.A.: Sphere packings, lattices and groups, vol. 290.
    Springer Science & Business Media (2013)
16. Friedman, E.: Packing center — circle packings and related problems. https://
    erich-friedman.github.io/packing/, online Resource
17. Friedman, E.: Circles in squares (2012), https://erich-friedman.github.io/packing/
    cirRsqu/
18. Friedman, E.: Hexagons in hexagons (2015), https://erich-friedman.github.io/
    packing/hexinhex/
19. Georgiev, B., Gómez-Serrano, J., Tao, T., Wagner, A.Z.: Mathematical exploration
    and discovery at scale. arXiv preprint arXiv:2511.02864 (2025)
20. Hojny, C., Besançon, M., Bestuzheva, K., Borst, S., Chmiela, A., Dionísio, J.,
    Eifler, L., Ghannam, M., Gleixner, A., Göß, A., Hoen, A., van der Hulst, R.,
    Kamp, D., Koch, T., Kofler, K., Lentz, J., Maher, S.J., Mexi, G., Mühmer, E.,
    Pfetsch, M.E., Pokutta, S., Serrano, F., Shinano, Y., Turner, M., Vigerske, S.,
14      T. Berthold et al.

    Walter, M., Weninger, D., Xu, L.: The SCIP Optimization Suite 10.0. Techni-
    cal report, Optimization Online (2025), https://optimization-online.org/2025/11/
    the-scip-optimization-suite-10-0/
21. Huang, C., Tang, Z., Hu, S., Jiang, R., Zheng, X., Ge, D., Wang, B., Wang, Z.:
    Orlm: A customizable framework in training large models for automated optimiza-
    tion modeling. Operations Research (2025)
22. Kallrath, J.: Cutting circles and polygons from area-minimizing rectangles. Journal
    of Global Optimization 43(2), 299–328 (2009)
23. Liu, F., Tong, X., Yuan, M., Lin, X., Luo, F., Wang, Z., Lu, Z., Zhang, Q.: Evolution
    of heuristics: Towards efficient automatic algorithm design using large language
    model. arXiv preprint arXiv:2401.02051 (2024), https://arxiv.org/abs/2401.02051
24. Mankowitz, D.J., Michi, A., Zhernov, A., Gelmi, M., Selvi, M., Paduraru, C.,
    Leurent, E., Iqbal, S., Lespiau, J.B., Ahern, A., Köppe, T., Millikin, K., Gaffney,
    S., Elster, S., Broshear, J., Gamble, C., Milan, K., Tung, R., Hwang, M., Cemgil,
    T., Barekatain, M., Li, Y., Mandhane, A., Hubert, T., Schrittwieser, J., Hassabis,
    D., Kohli, P., Riedmiller, M., Vinyals, O., Silver, D.: Faster sorting algorithms
    discovered using deep reinforcement learning. Nature 618(7964), 257–263 (2023).
    https://doi.org/10.1038/s41586-023-06004-9
25. Novikov, A., Vũ, N., Eisenberger, M., Dupont, E., Huang, P.S., Wagner, A.Z., Shi-
    robokov, S., Kozlovskii, B., Ruiz, F.J., Mehrabian, A., et al.: Alphaevolve: A cod-
    ing agent for scientific and algorithmic discovery. arXiv preprint arXiv:2506.13131
    (2025)
26. Peikert, R., Würtz, D., Monagan, M., de Groot, C.: Packing circles in a square:
    a review and new results. In: System Modelling and Optimization: Proceedings of
    the 15th IFIP Conference Zurich, Switzerland, September 2–6, 1991. pp. 45–54.
    Springer (2007)
27. Romanova, T., Bennell, J., Stoyan, Y., Pankratov, A.: Packing of concave polyhe-
    dra with continuous rotations using nonlinear optimisation. European Journal of
    Operational Research 268(1), 37–53 (2018)
28. Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M.P.,
    Dupont, E., Ruiz, F.J.R., Ellenberg, J.S., Wang, P., Fawzi, O., Kohli, P., Fawzi, A.:
    Mathematical discoveries from program search with large language models. Nature
    625(7995), 468–475 (2024). https://doi.org/10.1038/s41586-023-06924-6
29. SciPy API: Optimization and root finding (2025), https://docs.scipy.org/doc/
    scipy/reference/optimize.minimize-slsqp.html
30. Sharma, A.: Advanced circle packing for n=26 circles in a unit square
    (2025), https://github.com/algorithmicsuperintelligence/openevolve/blob/main/
    examples/circle_packing/best_program.py
31. Sharma, A.: Openevolve: an open-source evolutionary coding agent (2025), https:
    //github.com/algorithmicsuperintelligence/openevolve
32. Stoyan, Y., Pankratov, A., Romanova, T.: Quasi-phi-functions and optimal packing
    of ellipses. Journal of Global Optimization 65(2), 283–307 (2016)
33. Trinh, T.H., Wu, Y., Le, Q.V., He, H., Luong, T.: Solving olympiad geometry
    without human demonstrations. Nature 625(7995), 476–482 (2024). https://doi.
    org/10.1038/s41586-023-06747-5
34. Virtanen, P., Gommers, R., Oliphant, T.E., Haberland, M., Reddy, T., Courna-
    peau, D., Burovski, E., Peterson, P., Weckesser, W., Bright, J., et al.: SciPy 1.0:
    fundamental algorithms for scientific computing in python. Nature methods 17(3),
    261–272 (2020)
                Global Optimization for Combinatorial Geometry Problems      15

35. Wäscher, G., Haußner, H., Schumann, H.: An improved typology of cutting and
    packing problems. European journal of operational research 183(3), 1109–1130
    (2007)
