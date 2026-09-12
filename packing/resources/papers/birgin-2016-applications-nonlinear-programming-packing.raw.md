Applications of nonlinear programming to
packing problems

Ernesto G. Birgin




Abstract The problem of packing items within bounded regions in the Euclidean
space has multiple applications in a variety of areas, such as, Physics, Chemistry,
and Engineering. Problems of this type exhibit various levels of complexity. Nonlin-
ear programming formulations and methods had been successfully applied to a wide
range of packing problems. In this review paper, a brief description of the state-of-
the-art and an illustrated overview of packing nonlinear programming techniques
and applications will be presented.



1 Introduction

The problem of packing items within bounded areas has been widely studied over
the last decades. Due to the amount of publications dedicated to packing and cutting
problems, making a comprehensive review of the recent literature may be impos-
sible. A simple search by the words “circle packing” in the Google Images search
engine displays a myriad of amazing pictures describing theoretical results and ap-
plications. In this work we focus on models and techniques based on nonlinear pro-
gramming.
   Among the packing problems that can be addressed by nonlinear models and
methods, the problem of packing identical or non-identical circular and spherical
items presents several applications, such as origami design [17], analysis of con-
crete properties [23], study of the properties of forest soils and its influence in the
development of roots [22], Gamma Knife radiosurgery [24], molecular dynamics
simulations [19, 20], and industrial problems like facility location [13] and container
loading [14], among others. More recently, the packing of three-dimensional poly-
gons, such as thetrahedra, has also gained attention due to its applications to model

Ernesto G. Birgin
Institute of Mathematics and Statistics, University of São Paulo, Rua do Matão, 1010, Cidade
Universitária, 05508-090, São Paulo, SP, Brazil, e-mail: egbirgin@ime.usp.br


                                                                                            1
2                                                                               Ernesto G. Birgin

low-temperature states of matter, including liquids, crystals, glasses, and powders
(see, [12] and the references therein). In [8, 21] the concept of sentinels has been
introduced as a tool to model the overlapping between polygons through the sat-
isfaction of a finite set of continuous and differentiable constraints, that is one of
the key ingredients to model packing problems as tractable nonlinear programming
problems.
   Nonlinear programming models include, in the objective function or the con-
straints, functions that “measure” the overlapping between every pair of items. As
described in [26], these functions were named Φ-functions in [25]. Given a pair of
items i and j, a function Φi j (·) is said a Φ-function if its value is negative whenever
items i and j overlap, null if they are tangent, and positive if they do not overlap. Ev-
ery mathematical model related to a packing problem needs to deal with the items’
overlapping and, in some way or another, makes use of and objective function or a
set of constraints that can be seen as Φ-functions.



2 Packing of circles and spheres

The problem of packing a given set of items within an object with fixed dimensions
may be modeled as a nonlinear (continuous and differentiable) feasibility problem.
As an example, the problem of packing N circular items with radii r1 , r2 , . . . , rN
within a circular object with radius R (with R ≥ ri for all i) can be modeled as
finding (xi , yi )T ∈ R2 (for i = 1, . . . , N) such that

                  (xi − x j )2 + (yi − y j )2 ≥ (ri + r j )2 , for all j > i,
                                                                                             (1)
                                    xi2 + y2i ≤ (R − ri )2 , for all i.

In the problem described above, without loss of generality, it is assumed that the
circular object is centered at the origin of the Cartesian coordinate system. The first
set of equations says that the circular items must not overlap; while the second
set of equations says that the items must be placed within the object. Both sets of
equations are based on computing distances; and distances are squared to avoid the
nondifferentiability of the square root at x = 0. Analogous models can be considered
for different kinds of items and objects.
    When the items to be packed are all identical, the considered goal may be max-
imizing the number of packed items within an object with fixed dimensions. In this
case, the feasibility problem (1) may be used to solve the problem if an increasing
number of items N is considered. More specifically, we may try to solve the feasibil-
ity problem (1) with N = 1. If we manage to find a solution, then we try with N + 1
until finding that for, let say, N = N,
                                     b problem (1) is infeasible. In this case, the maxi-
mum number of identical items that can be packed is N   b −1. In practice, guaranteeing
that a nonlinear feasibility problem is infeasible is a very hard task. Therefore, we
may fix some maximum effort we are able to do and, if within this limited amount of
effort we are unable to find a solution, we may heuristically say that the problem is
Applications of nonlinear programming to packing problems                                 3

infeasible. At this point, many readers may think that it would be better to try some
kind of bisection scheme instead of increasing N one by one. Assume that the max-
imum number of items that can be packed is N ∗ . Feasibility problems with N < N ∗
are feasible and use to be simple (can be solved with a small computational effort).
On the other hand, feasibility problems with N > N ∗ are infeasible and detecting
infeasibility may be very hard. For that reason, it is easier (cheaper) to approach
N ∗ from below increasing N slowly. Of course, there is no need to start with N = 1
if it is known that the feasibility problem is feasible for some value N = NLB . The
described strategy was considered in [10] to pack identical circles within circles,
in [3] to pack identical circles within ellipses, and in [9, 8, 5] to pack identical rect-
angles (with different types of constraints related to the rectangular items’ angle of
rotation) within arbitrary convex regions.
    If the items to be packed are different and each item has an associated value (that
may be proportional to the item’s area), the goal may be maximizing the value of the
packed items [18]. In this case, packing an increasing number of items as described
in the paragraph above does not provide an optimal strategy. Selecting the subsets of
items for which a feasibility nonlinear (sub)problem may be modeled and solved is a
combinatorial problem for which heuristic strategies may be considered in practice.
On the other hand, independently of the items being identical or not, if the object
dimensions are not fixed, the goal may be finding the smallest object of a certain
type (circle, square, equilateral triangle, rectangle with smallest perimeter or area,
etc) within which a given set of items can be packed. In this case the problem can
be modeled as an optimization problem. As an example, consider again the problem
of packing a fixed number N circular items with radii r1 , r2 , . . . , rN within a circular
object with variable radius R and assume that the problem is to minimize R. This
problem can be easily formulated as

             Minimize R
             subject to (xi − x j )2 + (yi − y j )2 ≥ (ri + r j )2 , for all j > i,
                                                                                        (2)
                         xi2 + y2i ≤ (R − ri )2 ,                   for all i,
                         R ≥ r̄,

where r̄ = max1≤i≤N {ri }. Figure 1a shows the solution to the problem of finding
the smallest circle within which N = 6 identical unitary-radius circular items can be
packed. The solution corresponds to R∗ = 3 [16, 15]. It is interesting to note that,
within the circular object with R = 3, N = 7 identical unitary-radius circular items
can also be packed (see Figure 1b). This means that there is no equivalence between
the problem of minimizing the object dimensions and the problem of packing as
many items as possible. Variations of the model (2) were considered in [4, 11] for
packing identical circular items within circles, squares, equilateral triangles, and
strips, among others. Models and methodology presented in [11] also deal with 3D
problems. See Figure 2.
    In [7, p.171], sphere packing problems with up to 1,000,000 spheres are consid-
ered as an illustration of the capabilities of a nonlinear programming solver named
4                                                                                 Ernesto G. Birgin




                            (a)                                      (b)


Fig. 1 Graphical representation of (a) the smallest circle (that has R∗ = 3) within which 6 unitary-
radius circles can be packed and (b) the maximum number of unitary-radius circles that can be
packed within a circle with radius R = 3.




                 (a)                            (b)                              (c)


Fig. 2 Graphical representation of (a) smallest cube, (b) cylinder of minimal surface, and (c) small-
est regular tetrahedron within which 100 unitary-radius spheres can be packed. See [11] for details.



Algencan [1, 2]. Those problems are an oversimplification of the problem of pack-
ing molecules considered in [19, 20]. One of the characteristics of this problem
that makes it tractable is that the density (proportion of occupied volume of the ob-
ject) is relatively low. The first step in a molecular dynamics simulation consists
of obtaining initial coordinates for all the atoms of the system. Since molecular
dynamics force-fields contain repulsive terms that increase abruptly for short atom-
to-atom distances, the distances between atoms from different molecules must be
large enough so that repulsive potentials do not disrupt the simulations. Finding ad-
equate initial configurations was modeled as a packing problem in [19] and [20],
giving rise to the software Packmol1 .
   Let us call nmol the total number of molecules that we want to place in a re-
gion R of the three-dimensional space. For each i = 1, . . . , nmol, let natom(i) be the
number of atoms of the i-th molecule. Each molecule is represented by the orthog-

1 http://www.ime.unicamp.br/∼martinez/packmol/
Applications of nonlinear programming to packing problems                                    5

onal coordinates of its atoms. To facilitate the visualization, assume that the origin
is the barycenter of all the molecules. For all i = 1, . . . , nmol, j = 1, . . . , natom(i),
let A(i, j) = (ai1j , ai2j , ai3j ) be the coordinates of the j-th atom in the i-th molecule.
Suppose that one rotates the i-th molecule sequentially around the axes x1 , x2 , and
x3 , being γ i = (γ1i , γ2i , γ3i ) the angles that define such rotations. Moreover, suppose
that, after these rotations, the whole molecule is displaced so that its barycenter,
instead of the origin, becomes t i = (t1i ,t2i ,t3i ). These movements transform the atom
of coordinates A(i, j) in a displaced atom of coordinates P(i, j) = (pi1j , pi2j , pi3j ). Ob-
serve that P(i, j), j = 1, . . . , natom(i), is a function of (t i , γ i ), the relation being
P(i, j) = t i + R(γ i )A(i, j), j = 1, . . . , natom(i), where
                                  i i i
                                      c1 c2 c3 − si1 si3 si1 ci2 ci3 + ci1 si3 −si2 ci3
                                                                                        

                  R(γ i ) =  −ci1 ci2 si3 − si1 ci3 −si1 ci2 si3 + ci1 ci3 −si2 si3  ,    (3)
                                            ci1 si2              si1 si2        ci2

in which sik ≡ sin γki and cik ≡ cos γki , for k = 1, 2, 3.
   In [19, 20], the objective is to find angles γi and displacements ti , i = 1, . . . , nmol,
in such a way that, whenever i 6= i0 ,

                                kP(i, j) − P(i0 , j0 )k22 ≥ d 2 ,                          (4)

for all j = 1, . . . , natom(i), j0 = 1, . . . , natom(i0 ), where d > 0 is the required mini-
mum distance, and
                                           P(i, j) ∈ R,                                    (5)
for all i = 1, . . . , nmol, j = 1, . . . , natom(i). In other words, the rotated and displaced
molecules must remain in the specified region and the distance between any pair
of atoms must not be less than d. Problem (4,5) is a nonlinear feasibility problem
similar to (1). With some reformulations related to specific characteristics of the
problem, using heuristics to construct initial guesses, and using a nonlinear pro-
gramming solver [6], Packmol is able to solve practical problems like the ones il-
lustrated in Figure 3.



3 Packing of polygons

The packing of rectangular items within rectangular objects is a particular case of
the packing of polygons within polygons that has many practical applications in
Logistics and Engineering. A large variety of problems exists, depending on the
imposition of “cutting patterns”, the possibility of allowing rotations of the items or
not, the fact of the items being identical or not, etc. In many cases, the problem can
be modeled as a mixed-integer linear programing problem and solved by dedicated
exact or heuristic methods. On the other hand, when the rectangular items can be
freely rotated or the the items are other kind of polygons and the object within which
6                                                                                Ernesto G. Birgin




Fig. 3 Graphical representation of a double layered spherical vesicle with water inside and outside.
The depicted configuration, obtained by solving a packing problem, can be used as initial point for
molecular dynamics simulations. (This figure was extracted from the Packmol web site, where
additional information can be found.) In practice, the region R in (5) is replaced for potentially
different regions Ri j for each atom i of each molecule j.



the items must be placed is an arbitrary convex region, the problem may be modeled
as a nonlinear programming problem.
   In [8, 21] the concept of sentinels was introduced. Let I1 and I2 be nonempty,
open, bounded, and convex sets of Rn . Define J1 = I¯1 the closure of I1 and J2 = I¯2
the closure of I2 (J1 and J2 place the role of the items to be packed). Let D1 , D2 :
Rn → Rn be two displacement operators. So, D1 and D2 transform items in items
preserving distances, angles, and orientation. If D1 (I1 ) ∩ D2 (I2 ) 6= 0/ then we say that
D1 (J1 ) and D2 (J2 ) (or D1 (I1 ) and D2 (I2 )) are superposed. Let S1 and S2 be finite
subsets of J1 and J2 , respectively. We say that S1 and S2 are sentinels sets relatively
to J1 and J2 if the following property holds: for all displacements D1 and D2 , if
D1 (J1 ) and D2 (J2 ) are superposed then D1 (S1 )∩D2 (I2 ) 6= 0/ or D2 (S2 )∩D1 (I1 ) 6= 0.
                                                                                          /
Roughly speaking, if, after the displacements, the items J1 and J2 are superposed
then at least one sentinel of J1 becomes interior to J2 or one sentinel of J2 becomes
interior to J1 . The concept of sentinels can be easily extended to any family of
(potentially non-identical) m ≥ 2 “items”, the key point being to define the (finite)
sentinels sets for a given family of polygons (or to determine that they do not exist).
In [21], minimal sets of sentinels for rectangles are exhibited (see Figure 4), as well
as sentinels sets for other types of polygons; while it is also shown that no finite sets
of sentinels do not exist for triangles.
   We now describe how the sentinels concept can be used to formulate a polygons
packing problem as a nonlinear programming problem. This description follows [8]
very closely. Let I1 , . . . , Im ⊂ Rn be nonempty, open, bounded, and convex sets, Ω ⊂
Rn , and assume that we want to pack the items I1 , . . . , Im (or, equivalently, they
closures J1 , . . . , Jm ) into the region Ω . This means that we want to find displacements
D1 , . . . , Dm such that
                                     Di (Ji ) ⊂ Ω for i = 1, . . . , m                   (6)
and
                    Di (Ji ) and D j (J j ) are not superposed for all i 6= j.                  (7)
Applications of nonlinear programming to packing problems                                          7

     Let S1 ⊂ J1 , . . . , Sm ⊂ Jm be such that S1 , . . . , Sm are sentinels sets relatively to
J1 , . . . , Jm . Given i, j ∈ {1, . . . , m}, i 6= j, define

                  κ(Di , D j ) = #{[Di (Si ) ∩ D j (I j )] ∪ [D j (S j ) ∩ Di (Ii )]}.            (8)

This means that condition (7) can be formulated as

                                    κ(Di , D j ) = 0 for all i 6= j                               (9)

and, thus, the packing problem defined by (6,7) can be formulated as the optimiza-
tion problem

            Minimize ∑ κ(Di , D j ) subject to Di (Ji ) ⊂ Ω for i = 1, . . . , m.                (10)
                         i6= j

The objective function of (10) represents the total number of sentinels of one item
that, after the displacements, fall in the interior of some other item. If a global so-
lution of (10) is found such that the objective function vanishes then the packing
problem (6,7) is solved.
    The optimization problem (10) defines the Method of Sentinels. However, this
minimization problem needs to be reformulated in order to be transformed into a
solvable nonlinear programming problem. Let us consider the case in which Ω is a
closed and convex set defined by a set of inequalities, i.e.

                          Ω = {x ∈ Rn | gk (x) ≤ 0, k = 1, . . . , p}.                           (11)

Moreover, assume that each item Ji is a bounded polytope, so it is the convex hull
of its vertices V1 (Ji ), . . . ,Vν(i) (Ji ). Then, the constraints of (10) take the form

           gk (Di [V` (Ji )]) ≤ 0 for i = 1, . . . , m, ` = 1, . . . , ν(i), k = 1, . . . , p.   (12)

The displacements Di can always be described by a finite set of parameters. For ex-
ample, displacements in R2 are given by three parameters, the first two representing
a translation and the third the angle of rotation. Therefore, the constraints (12) have
the usual form adopted in nonlinear programming problems.
    The objective function of (10) depends on the continuous variables that define the
displacements but it takes only discrete integer nonnegative values. For nonlinear
programming reformulations we need to replace it by a continuous function of the
displacement variables. As before, we restrict ourselves to the case in which the
sets Ji are bounded polytopes. In this case, each Ji is described by a set of linear
inequalities of the form

                                 hcik , xi ≤ bik for k = 1, . . . , µ(i).                        (13)

If s ∈ S j ⊂ J j is a sentinel of I j and D j (s) is in Di (Ii ) with i 6= j then D−1
                                                                                   i D j (s)
belongs to Ii and, therefore, it satisfies
8                                                                                     Ernesto G. Birgin

                       hcik , D−1
                               i D j (s)i < bik for k = 1, . . . , µ(i).                          (14)

Thus, the displaced sentinel s belongs to the displaced Ii if, and only if,
                         µ(i)
                         ∏ max{0, bik − hcik , D−1
                                                i D j (s)i} > 0.                                  (15)
                         k=1

   Therefore, a degree of the superposition of Ii and I j (or Ji and J j ) under the
displacements Di and D j is given by
                                         µ( j)
             Φ(Di , D j ) = ∑s∈Si ∏k=1 max{0, b jk − hc jk , D−1
                                                              j Di (s)i}
                                                                         2
                                                                                                  (16)
                            + ∑s∈S j ∏k=1 max{0, bik − hcik , D−1
                                          µ(i)                            2
                                                               i D j (s)i} .

The function Φ(Di , D j ) is nonnegative and continuously differentiable with respect
to the parameters that define the displacements Di and D j ; and it vanishes if, and
only if, Di (Ji ) and D j (J j ) are not superposed. Therefore, it can replace the func-
tion κ(Di , D j ) in the optimization problem (10).
   Summing up, in the case in which Ω is a convex set defined by inequalities and
the items are bounded polytopes, the packing problem can be formulated as the
continuous and differentiable nonlinear programming problem

                                   Minimize ∑ Φ(Di , D j )                                        (17)
                                                  i6= j

subject to (12). Moreover, since we are only interested in global solutions of (17)
where the objective function must vanish, the problem can be reformulated as the
feasibility problem given by

           ∑i6= j Φ(Di , D j ) = 0,
                                                                                                  (18)
            gk (Di [V` (Ji )]) ≤ 0, i = 1, . . . , m, ` = 1, . . . , ν(i), k = 1, . . . , p.

Finally, (18) is equivalent to the following unconstrained continuously differentiable
global optimization problem

                                                 m ν(i) p
           Minimize ∑ Φ(Di , D j ) + ∑ ∑ ∑ max{0, gk (Di [V` (Ji )])}2 .                          (19)
                        i6= j                i=1 `=1 k=1

   A few examples of the solutions that can be obtained by solving (17), (18), or (19)
can be seen in Figure 5. In general, the nonlinear programming problems are non-
convex with many spurious stationary points that are not solutions to the packing
problem they represent (only global solutions are of interest). Because of that, clever
heuristics need to be developed to determine promising starting points for the iter-
ative optimization process. One possibility explored in [8] for packing rectangular
items was to consider, for each rectangle, a partial covering with varied-sized cir-
cles (see Figure 6). In a first phase, a circle packing problem is solved (with models
Applications of nonlinear programming to packing problems                                            9

similar to the one described in the previous section) to place the circles within the
object and avoiding the overlapping of the circles that cover different items. In a
second phase the circles are dismissed and the placement of the rectangular items is
used as an initial guess to the rectangular items packing problem.




Fig. 4 Minimal set of sentinels for a family of m identical rectangular items with smallest side s and
largest side 7s. The distance between the sentinels in the smallest side is s/2 while the “horizontal
distance” between the sentinels in the largest side and in the central line is smaller that s. (Enjoy
yourself: make two copies of the rectangle in the figure and try to overlap them without having a
sentinel of one rectangle in the interior of the other. Free rotations are allowed.)




Fig. 5 Examples of solutions found in [8] to the problem of packing freely-rotated rectangular
items within arbitrary convex regions.




Fig. 6 Arbitrary partial covering of a rectangular item by circles. In a first phase, a packing problem
with the circular items is solved (avoiding overlapping between the circles that cover different
rectangles). The position of the rectangular items inherited by the solution of the problem of the
first phase is used as initial guess to the original packing problem with rectangular items.
10                                                                             Ernesto G. Birgin

4 Concluding remarks

There are packing problems that, by its nature, are combinatorial problems. Exam-
ples of those problems are one-dimensional bin packing problems, two-dimensional
bin packing or stock cutting problems involving rectangular items (that can not be
freely rotated) and rectangular objects, and some two- or three-dimensional puzzle
problems, among many others. There are other packing problems, like for exam-
ple finding the densest packing of circles or spheres in the infinite Euclidean space,
that can be solved using lattices. On the other hand, there are also packing prob-
lems that can be naturally addressed with nonlinear programming techniques. The
packing of circles or spheres within restricted domains or the packing of irregular
shape items or arbitrary varied polygons are some of the many possible examples.
In these cases, discretizing the problem domain may produce sub-optimal solutions
(by reducing the feasible region) and nonlinear programming models and solution
methods should be considered. In most of the cases, global solutions are sought and
problems are very challenging and provide a nice source for benchmarking.



References

 1. R. Andreani, E. G. Birgin, J. M. Martı́nez, and M. L. Schuverdt, On Augmented Lagrangian
    Methods with general lower-level constraints, SIAM Journal on Optimization 18, pp. 1286–
    1309, 2008.
 2. R. Andreani, E. G. Birgin, J. M. Martı́nez, and M. L. Schuverdt, Augmented Lagrangian meth-
    ods under the Constant Positive Linear Dependence constraint qualification, Mathematical
    Programming 111, pp. 5–32, 2008.
 3. E. G. Birgin, L. H. Bustamante, H. F. Callisaya, and J. M. Martı́nez, Packing circles within
    ellipses, International Transactions in Operational Research 20, pp. 365–389, 2013.
 4. E. G. Birgin and J. M. Gentil, New and improved results for packing identical unitary ra-
    dius circles within triangles, rectangles and strips, Computers & Operations Research 37, pp.
    1318–1327, 2010.
 5. E. G. Birgin and R. D. Lobato, Orthogonal packing of identical rectangles within isotropic
    convex regions, Computers & Industrial Engineering 59, pp. 595–602, 2010.
 6. E. G. Birgin and J. M. Martı́nez, Large-scale active-set box-constrained optimization method
    with spectral projected gradients, Computational Optimization and Applications 23, pp. 101–
    125, 2002.
 7. E. G. Birgin and J. M. Martı́nez, Practical Augmented Lagrangian Methods for Constrained
    Optimization, Society for Industrial and Applied Mathematics, Philadelphia, 2014.
 8. E. G. Birgin, J. M. Martı́nez, W. F. Mascarenhas, and D. P. Ronconi Method of Sentinels for
    Packing Items within Arbitrary Convex Regions, Journal of the Operational Research Society
    57, pp. 735–746, 2006.
 9. E. G. Birgin, J. M. Martı́nez, F. H. Nishihara, and D. P. Ronconi, Orthogonal packing of
    rectangular items within arbitrary convex regions by nonlinear optimization, Computers &
    Operations Research 33, pp. 3535–3548, 2006.
10. E. G. Birgin, J. M. Martı́nez, and D. P. Ronconi, Optimizing the Packing of Cylinders into
    a Rectangular Container: A Nonlinear Approach, European Journal of Operational Research
    160, pp. 19–33, 2005.
11. E. G. Birgin and F. N. C. Sobral, Minimizing the object dimensions in circle and sphere pack-
    ing problems, Computers & Operations Research 35, pp. 2357–2375, 2008.
Applications of nonlinear programming to packing problems                                        11

12. D. Chen, Y. Jiao, and S. Torquato, Equilibrium phase behavior and maximally random jammed
    state of truncated tetrahedra, The Journal of Physical Chemistry B 118, pp. 7981–7992, 2014.
13. Z. Drezner and E. Erkut, Solving the continuous p-dispersion problem using non-linear pro-
    gramming Journal of the Operational Research Society 46, pp. 516–520, 1995.
14. H. J. Fraser and J. A. George, Integrated container loading software for pulp and paper industry
    European Journal of Operational Research 77, pp. 466–474, 1994.
15. R. L. Graham, Sets of points with given minimum separation (Solution to Problem El921),
    The American Mathematical Monthly 75, pp. 192–193, 1968.
16. S. Kravitz, Packing cylinders into cylindrical containers, Mathematics Magazine 40, pp. 65–
    71, 1967.
17. R. J. Lang, A computational algorithm for origami design, in 12th ACM Symposium on Com-
    putational Geometry, pp. 98–105, 1996.
18. S. Martello and P. Toth, Knapsack problems: Algorithms and computer interpretations. John
    Wiley & Sons, Chichester, New York, Brisbane, Toronto, Singapore, 1990.
19. L. Martı́nez, R. Andrade, E. G. Birgin, and J. M. Martı́nez, Packmol: A package for building
    initial configurations for molecular dynamics simulations, Journal of Computational Chem-
    istry 30, pp. 2157–2164, 2009.
20. J. M. Martı́nez and L. Martı́nez, Packing optimization for automated generation of complex
    system’s initial configurations for molecular dynamics and docking, Journal of Computational
    Chemistry 24, pp. 819–825, 2003.
21. W. F. Mascarenhas and E. G. Birgin, Using sentinels to detect intersections of convex and
    nonconvex polygons, Computational and Applied Mathematics 29, pp. 247–267, 2010.
22. K. T. Osman, Foerst Soils – Properties and Management, Springer, Cham, Heidelberg, New
    York, Dordrecht, London, 2013.
23. H. C. Wong and A. K. H. Kwan, Packing density: a key concept for mix design of high
    performance concrete, in Proceedings of the Materials Science and Technology in Engineering
    Conference, HKIE Materials Division, Hong Kong, 2005, pp. 1–15.
24. Q. J. Wu and J. D. Bourland, Morphology-guided radiosurgery treatment planning and opti-
    mization for multiple isocenters, Medical Physics 26, pp. 2151–2160, 1999.
25. Y. G. Stoyan, On the generalization of the dense allocation function, Reports of the Ukrainian
    SSR Academy of Science Ser. A 8, pp. 70–74, 1980 (in Russian).
26. Y. G. Stoyan, M. V. Novozhilova, and A. V. Kartashov, Mathematical model and method
    of searching for a local extremum for the non-convex oriented polygons allocation problem,
    European Journal of Operational Research 92, pp. 193–210, 1996.
