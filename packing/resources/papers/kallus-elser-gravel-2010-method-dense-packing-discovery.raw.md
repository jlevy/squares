                                                                                                                                                           arXiv preprint

                                                                              A method for dense packing discovery
                                                                                         Yoav Kallus∗ and Veit Elser
                                                          Laboratory of Atomic and Solid-State Physics, Cornell University, Ithaca, New York, 14853

                                                                                                    Simon Gravel
                                                      Department of Genetics, Stanford University School of Medicine, Stanford, California 94305-5120
                                                                                        (Dated: August 28, 2018)
                                                          The problem of packing a system of particles as densely as possible is foundational in the field
                                                       of discrete geometry and is a powerful model in the material and biological sciences. As packing
                                                       problems retreat from the reach of solution by analytic constructions, the importance of an efficient
arXiv:1003.3301v2 [math.MG] 4 Aug 2010




                                                       numerical method for conducting de novo (from-scratch) searches for dense packings becomes crucial.
                                                       In this paper, we use the divide and concur framework to develop a general search method for
                                                       the solution of periodic constraint problems, and we apply it to the discovery of dense periodic
                                                       packings. An important feature of the method is the integration of the unit cell parameters with
                                                       the other packing variables in the definition of the configuration space. The method we present led
                                                       to improvements in the densest-known tetrahedron packing which are reported in Ref. [1]. Here, we
                                                       use the method to reproduce the densest known lattice sphere packings and the best known lattice
                                                       kissing arrangements in up to 14 and 11 dimensions respectively (the first such numerical evidence
                                                       for their optimality in some of these dimensions). For non-spherical particles, we report a new dense
                                                       packing of regular four-dimensional simplices with density φ = 128/219 ≈ 0.5845 and with a similar
                                                       structure to the densest known tetrahedron packing.

                                                       PACS numbers: 61.50.Ah, 45.70.-n, 02.70.-c


                                                           I.   INTRODUCTION                               the resolution of the Kepler conjecture about the dens-
                                                                                                           est packing of spheres in three dimensions [3], and has
                                            The dense packing behavior of a general solid body             therefore been considered resolved since the latter was
                                         (particle) in a Euclidean space is a problem of interest          proved by Hales [4]. However, Hilbert’s statement of
                                         in mathematics, physics, and many other fields. A pack-           the problem does not single out the sphere, and actu-
                                         ing is a collection of particles in the Euclidean space Rd ,      ally mentions the regular tetrahedron as another parti-
                                         wherein no two particles overlap (i.e., the intersection of       cle of interest. Recent work diverging from the focus on
                                         any two particles has an empty interior) and the pack-            spherical particles has spotlighted ellipsoids [5], regular
                                         ing fraction or density φ is then the volume fraction of          and semi-regular polyhedra [6, 7] (and the regular tetra-
                                         space covered by the particles. Of particular interest are        hedron in particular [1, 8–11]), and superballs [12]. Few
                                         packings of a given particle (wherein all particles are con-      bounds are known for the maximum packing fraction of
                                         gruent), and the problem of interest is to determine the          general convex particles. Kuperberg and Kuperberg have
                                         maximum possible density φmax among all packings of               shown that
                                                                                                                    √ for any convex particle in two dimensions,
                                         a given particle. A packing that realizes this maximum            φmax ≥ 3/2 ≈ 0.86602 [13]. Torquato et al. used the
                                         can be thought of as the equilibrium state of the system          known maximal packing density of spheres to derive an
                                         of classical hard particles in the limit of infinite pressure     upper bound on the packing density of any solid, but
                                         or zero temperature.                                              this bound is trivial (i.e., φmax ≤ φU , where φU > 1) for
                                            The general problem of packing congruent particles             many solids [6]. Ulam has conjectured that in three di-
                                         was posed as a part of the eighteenth of David Hilbert’s          mensions, the sphere achieves
                                                                                                                                    √      the lowest maximum pack-
                                         famous Mathematische Probleme:                                    ing fraction, φmax = π/ 18 ≈ 0.74048, among all convex
                                                                                                           particles [14].
                                               How can one arrange most densely in space
                                               an infinite number of equal solids of a given                  In the quest for dense packings of various particles,
                                               form, e.g., spheres with given radii or regular             analytic and numerical investigations have both played
                                               tetrahedra with given edges (or in prescribed               important roles. The former have been very successful
                                               position), that is, how can one so fit them                 in the study of the dense packing of spheres, where an-
                                               together that the ratio of the filled to the un-            alytic constructions based on groups, codes, and lami-
                                               filled space may be as large as possible? [2]               nated lattices have produced the densest-known sphere
                                                                                                           packings and lattice sphere packings in many dimensions
                                         This part of the problem has been taken over the years as         [15]. However, the analytic approach to the construction
                                                                                                           of dense packings relies on the imagination of the con-
                                                                                                           structor, and for a variety of other problems the densest
                                                                                                           packings have evaded the creativity of analytic investiga-
                                         ∗ Electronic address: yk328@cornell.edu                           tors and were only uncovered in computational investiga-
                                                                                                                           2

tions. While complete (i.e., exhaustive) algorithms exist      growth in the number of local optima in the configura-
for some problems (such as the algorithm in Ref. [16],         tion space, which the search will still have to traverse, will
which gave new best known results for the lattice cover-       nevertheless lead to suboptimal results when many inde-
ing and covering-packing problems in some dimensions),         pendent particles are included in the search. Therefore,
they do not exist or have runtimes that are too long for       as discussed below, it is crucial for the unit cell variables
other problems. In those cases, incomplete search algo-        to be aggressively optimized so that the number of par-
rithms become necessary.                                       ticles to be simulated can be reduced. The incorporation
   One example of a dense packing that has only been           of the unit cell variables directly into the basic dynamics
uncovered by a de novo numerical search is the cur-            of the search achieves this goal.
rently densest-known packing of tetrahedra, whose struc-          Numerical searches are restricted to finite-dimensional
ture was first hinted at by a numerical search using the       configuration spaces, and therefore have been largely lim-
method described in this paper [1]. The structure was          ited to investigating periodic packings, packings which
later optimized by Torquato and Jiao [10] and by Chen          are preserved under translations by a lattice Λ. In a gen-
et al. [11]. Results of subsequent Monte Carlo simu-           eral periodic packing, the particles are partitioned into
lations have reproduced this structure and suggest it is       p orbits of the lattice Λ, and when p = 1 the packing is
the densest packing of regular tetrahedra at least with a      called a lattice packing. In physics, any periodic arrange-
small number (≤ 16) of tetrahedra in the unit cell [10, 11].   ment is usually referred to as a lattice and the special
Another de novo search with Monte Carlo dynamics has           case of p = 1 is known as a Bravais lattice. In general,
uncovered a packing based on a quasicrystal approximant        the maximum density need not be realizable by a periodic
reminiscent of the Frank-Kasper σ-phase with a slightly        packing, but arbitrarily close densities are realizable with
lower density [9]. As these two structures were overlooked     periodic packings of arbitrarily large p. Similarly, arbi-
by previous analytical investigations [8, 17], it is quite     trarily accurate approximations of any packing can be
likely that without the results of de novo searches, they      obtained using a sufficiently large cubic or orthorhombic
would have remained unimagined and undiscovered.               unit cell. However, due to the rapid increase in compu-
   In the best case, such searches would produce the op-       tational complexity and the proliferation of local optima
timal packing possible subject to the built-in restrictions    as the number of independent particles rises, it is of-
(such as number of particles in the unit cell or unit cell     ten preferable to include fewer particles but allow for a
shape). However, in problems exhibiting a large degree         variable unit cell shape. We focus then on searching for
of frustration, the presence of many local optima that are     packings with a small number of particles in the unit cell.
separated from each other by high barriers complicates            To our knowledge, variable unit cells have only been
the task of finding the optimal packing. The tendency          introduced recently to searches for dense packings, for
of simulations to get stuck in the local optima of such a      instance with the adaptive shrinking cell scheme in Refs.
rugged optimization landscape, especially when these lo-       [5, 7] and with the use of Parrinello-Rahman dynamics in
cal optima proliferate as more particles are simulated, has    the space of lattices in Ref. [21]. The increased particle
been held responsible for suboptimal results in searches       population associated with restricting unit cell variabil-
[6, 7]. One technique which has been observed to re-           ity can sometimes be tolerated in two and three dimen-
lieve dynamical stagnation in Monte Carlo simulations          sions, but in high dimensions the number of particles that
at high pressures has been to allow slightly unphysical        must be simulated grows exponentially due to the curse
moves, such as allowing particles to temporarily overlap       of dimensionality and this approach becomes impracti-
[9].                                                           cal. The constraint-satisfaction formulation of the peri-
   We propose a novel search method as an alternative to       odic packing problem used in PDC features a variable
Monte Carlo simulations, with a number of features that        unit cell and naturally treats the positions of particles
directly address these observations. The method is based       in the unit cell and the unit cell parameters on the same
on the dynamics of the difference map, a constraint-           footing. This new approach allows us to successfully look
satisfaction iterative search algorithm, and on the di-        for dense sphere packings in dimensions as high as 14,
vide and concur constraint framework (we abbreviate            further than probed by any previously reported unbiased
this combination D − C, where the minus sign stands            numerical exploration of periodic packings.
for the difference map) [18–20]. It adapts the D − C              Besides the density of a packing, another attribute of
approach to the case of periodic problems and we shall         interest is the coordination number, that is, the num-
call it periodic divide and concur (PDC). The difference       ber of nearest neighbors of particles in the packing. In
map is designed to avoid being trapped in local optima         the case of spherical particles, this amounts to the num-
and has been demonstrated in multiple applications to          ber of spheres in contact with a given sphere, known as
find solutions of highly non-convex problems, including        the kissing number [15]. Searching for high-coordination
finite packing problems with large numbers of particles,       number arrangements around a single sphere has been
from random starting configurations [18–20]. The search        accomplished previously with the D − C method [19].
proceeds through a non-physical configuration space, cut-      Here we apply PDC to search for space-filling periodic
ting through the conventional physical optimization land-      arrangements of high coordination number, and particu-
scape. Still, it is to be expected that the exponential        larly lattice arrangements.
                                                                                                                               3

   An efficient de novo numerical search method can pro-        The exclusion constraint is then
vide critical utility in the field of packing. In addition to
the ability of a de novo search to provide confidence in a            Kexcl = {(x1 , x2 ) ∈ Ψ : ||x1 − x2 || ≥ 2} ⊆ Ψ.        (2)
putative, but not proven, optimal result, a de novo search
has often been responsible for surprising new results: two      This constraint adheres to the simplicity criterion of hav-
recent examples in which unexpected (as it turns out,           ing an efficient method to compute a projection to it.
quasiperiodic) packings were found as the results of de         Specifically, the projection is given by
novo searches are in the problem of tetrahedron packing                                  (
[9] and in the ten-dimensional kissing number problem                                      (x′1 , x′2 ) if ||x1 − x2 || < 2
                                                                   πKexcl [(x1 , x2 )] =                                    (3)
[22]. It is with these motivations that we introduce the                                   (x1 , x2 ) otherwise,
PDC method in this paper. In Section II we introduce
the D − C scheme by presenting a simple example which           where,
serves to motivate the constructions in the subsequent
sections. In Section III we formulate the problems tack-                               2 − ||x1 − x2 ||
                                                                             x′1 =x1 +                  (x1 − x2 )            (4)
led in this paper — sphere packing, the lattice kissing                                  2||x1 − x2 ||
number, and polytope packing — in terms of constraint                                  2 − ||x1 − x2 ||
satisfaction. In Section IV we describe in detail aspects                    x′2 =x2 −                  (x1 − x2 )            (5)
                                                                                         2||x1 − x2 ||
of our implementation of the PDC search, including ef-
ficient computation of projections to the constraints of        as illustrated in Figure 1.
Section III. In Section V we present some results of PDC           A more complicated case arises when three or more
for the problems discussed, including a newly discovered        disks are considered. In this case, the exclusion con-
packing of regular four-dimensional simplices. In Section       straint,
VI we present concluding remarks.
                                                                         Kexcl = {(x1 , . . . xn ) ∈ Ψ :
                                                                              ||xi − xj || ≥ 2 for all 1 ≤ i < j ≤ n},
                   II.    MOTIVATION
                                                                is not a simple constraint according to the criterion
                                                                above. Alternatively, we could replace Kexcl by many
                 A.      The D − C scheme                       pairwise exclusion constraints
                                                                          i,j
   The key step in applying the D − C approach to pack-                  Kexcl = {(x1 , . . . xn ) ∈ Ψ : ||xi − xj || ≥ 2}.   (6)
ing problems is to recast the problem as a problem of
constraint satisfaction. Particularly, we must express it       The pairwise constraints are all individually simple.
as the problem of finding a configuration in a Euclidean        However, as noted above, we are limited to problems de-
configuration space (Ω), which satisfies two constraints.       scribed by only two simple constraints.
We identify a constraint C with the subset C ⊆ Ω of               Divide and concur provides a general procedure for re-
configurations satisfying the constraint. A projection of       ducing the number of simple constraints to two, at the
a configuration x to a constraint C is the operation of         expense of enlarging the configuration space. This re-
finding a configuration x′ ∈ C that minimizes the dis-          duction is achieved by parameterizing the configuration
tance ||x − x′ ||. Each of the two constraints (C, D ⊆ Ω),      space with more variables than are necessary to fully
must be simple enough that the operation of projecting          specify a configuration. In the example at hand, the new
an arbitrary configuration to it can be computed effi-          configuration space is
ciently. The iterative map used in exploring the config-
uration space takes advantage of the formulation of the            Ω = {(x1,2 , . . . xn,n−1 ) : xi,j ∈ R2 for all i 6= j},   (7)
problem in terms of two simple constraints, as outlined
                                                                where we call all the variables xi,j for a particular index
in section II B. In this section we present the application
                                                                i the replicas of the original variable xi . Every configura-
of the D − C scheme to finite sphere packing problems,
                                                                tion (x1 , . . . xn ) ∈ Ψ can be identified with a configura-
which has been developed and implemented in Ref. [19],
                                                                tion (x1,2 , . . . xn,n−1 ) ∈ Ω, wherein xi,j = xi for all i, j,
as an introduction to the main ideas of the scheme.
                                                                through a simple linear map A. Enough redundant vari-
   The defining constraint of packing problems is the con-      ables have been introduced to the configuration space so
straint that no particles in the packing overlap, which we      that each pairwise exclusion constraint can now be writ-
call the exclusion constraint. As a simple illustration of      ten in terms of a private set of variables, disjoint from
this constraint, consider the exclusion of a pair of unit-      the private variables of other constraints:
radius disks in R2 . In this case, the configuration space
Ψ is parameterized by the positions of the centers of the         Di,j = {(x1,2 , . . . xn,n−1 ) ∈ Ω : ||xi,j − xj,i || ≥ 2}. (8)
two disks:
                                                                The intersection, D ⊆ Ω, of all of the pairwise exclusion
               Ψ = {(x1 , x2 ) : x1 , x2 ∈ R2 }.         (1)    constraints, which we will call the “divide” constraint, is
                                                                                                                                  4

                                                                     now also simple, since the projection can be performed
                                                                     independently on each set of private variables (Figure 1).
                                                                        The map A : Ψ → Ω from the original configuration
                                                                     space (the physical configuration space) to the new one
                                                                     (the formal configuration space) is not surjective, and so
                                                                     a general point in the formal configuration space does not
                                                                     correspond to a valid physical configuration. The “con-
                                                                     cur” constraint C = A(Ψ) is given by the range of A, the
                                                                     subset of Ω that does correspond to valid configurations.
                                                                     That is, the constraint requires redundant specifications
                                                                     of an original variable to concur in regard to its value.
                                                                     Since A is linear, C is also a simple constraint.
                                                                        Another constraint that must usually be addressed in
                                                                     packing problems with a finite number of particles is the
                                                                     confinement constraint. In most cases the particles, or
                                                                     their centers, are confined to lie in some subset M of
                                                                     space, where M can be either some region of finite vol-
                                                                     ume, or a compact manifold (as in the case of spherical
                                                                     codes). As a subset of the original configuration space,
                                                                     the confinement constraint is written as
                                                                       Kconf = {(x1 , . . . xn ) ∈ Ψ : xi ∈ M for all i} ⊆ Ψ. (9)
                                                                     We can incorporate this constraint into the “concur” con-
                                                                     straint, C, by modifying it to be the image A(Kconf ) in-
                                                                     stead of the entire range of A. In our example, this would
                                                                     give the constraint
                                                                      C = {(x1,2 , . . . xn,n−1 ) ∈ Ω : xi,j = xi ∈ M for all i, j}.
                                                                                                                                (10)
                                                                     Since A is linear, the projection to C = A(Kconf ) can
                                                                     be decomposed into a projection to A(Ψ) followed by
                                                                     a projection to A(Kconf ). The first step is performed by
                                                                     taking the average position of all the replicas of each disk.
                                                                     The second step is performed by projecting this average
                                                                     position to M (see Figure 1). In general, this two-step
                                                                     projection method is valid for handling the constraints
                                                                     in the physical configuration space that are simple at
                                                                     the outset and do not require the introduction of new
                                                                     variables.
                                                                        The result of the above construction is that a configu-
FIG. 1: An illustration of the D − C scheme in the case
                                                                     ration in Ω satisfies the “divide” and “concur” constraints
of packing three disks into a square box. In the case of two
overlapping disks (a), the exclusion constraint is simple in the
                                                                     simultaneously if and only if it corresponds to a config-
sense that a projection to the constraint can be performed ef-       uration in Ψ which satisfies all the exclusion constraints
ficiently. The projection is given by (3) and yields the config-     and the confinement constraint; that is, it corresponds to
uration (b). In the case of three disks (c), there is no similarly   a solution of the packing problem under consideration.
efficient projection method to the constraint that no overlaps          In the following sections we modify the above simple
occur. In the D − C scheme, each disk is represented by two          construction so as to generalize the method in two major
replicas (d), which together make three independent replica          ways. The first generalization is to packings of infinite
pairs (e). The exclusion constraint, now also called the “di-        regions, instead of only finite ones. Specifically, we allow
vide” constraint, is modified so that only replica pairs are         for periodic packings with an arbitrary unit cell. This
prohibited from overlapping, and any other overlaps are al-          is achieved by generalizing the idea of replicas of parti-
lowed. Thus, the projection to the exclusion constraint can be
                                                                     cles to include also their periodic images. When the unit
performed independently on each replica pair as in the case of
two disks (f). A second constraint, the “concur” constraint,         cell vectors are included in the original set of parameters,
requires all replicas representing a single disk to coincide and     the map from the original parameter space to the space of
requires the disk to lie within the confinement box. The re-         replica configurations is still linear, though a little more
sult of projecting the configuration (d) to this constraint is the   elaborate. Additionally, the confinement constraint of
configuration (g). In order to search for a configuration sat-       finite packings is replaced in the case of periodic pack-
isfying both constraints, we do not alternately project from         ings by a constraint on the unit cell volume, ensuring a
one constraint to the other, but instead use the difference          specified density.
map (12) to evolve the configuration. The result of a success-
ful search is a configuration (h) satisfying both constraints,
which by construction corresponds to a solution of the prob-
lem.
                                                                                                                             5

   The second generalization is to packings of non-              D-estimates of the solution at the ith iteration. The dis-
spherical particles, specifically convex polytopes. This         tance between the two estimates is the error ǫ and the
is achieved by representing each particle not only by the        search terminates when the error converges to zero.
position of its centroid, but by the positions of all its ver-      To summarize, a simple difference map solver for con-
tices. A new constraint, the rigidity constraint, is added       tinuous constraints would consist of the following simple
to ensure that the particle is not deformed in the solution.     steps:
Despite the mathematical complications that arise from
these two generalizations, the conceptual framework is              1. Initialize the iterate x to a random configuration.
identical to the above example, and the constructions in            2. Compute the two estimates of the solution xC ←
the following sections will draw attention to the analogy              πC (fD (x)) and xD ← πD (fC (x)).
with the construction presented above.
                                                                    3. Compute the error ǫ ← ||xC − xD ||. If it is be-
                                                                       low a predefined convergence threshold, the search
                B.    The difference map                               terminates, and the solution is given by xC ≈ xD .
                                                                    4. Advance the iterate x ← x + β(xD − xC ). Start
   Given a problem formulated as the task of finding a                 the next iteration at Step 2.
configuration x ∈ C ∩ D, simultaneously satisfying the
constraints C, D ⊆ Ω, we wish to use the availability of
efficient methods for computing the projections πC and                            III.   CONSTRAINTS
πD to the constraints in order to set up an iterated map
to search through the configuration space for a solution.               A.   Periodic sphere packing and kissing
Naive schemes, such as the alternating projections map
x 7→ πD (πC (x)), suffer from the problem of stagnation at
near solutions (local minima of the distance between the            A periodic packing of equal-sized spheres (radius r) in
two constraints). The difference map, a slightly more so-        d dimensions can be generated by the action of a lattice
phisticated scheme, is designed to provide efficient search      Λ on a set of p primitive spheres. Let P be the set of
dynamics while avoiding the traps of local minima [18].          centers of the primitive spheres. We define a generating
   The difference map (DM) can be written in terms of            matrix of the packing as a (d + p) × d matrix M whose
                                                                 first d rows are a set of generators of Λ and whose re-
the projections πC and πD and one parameter β:
                                                                 maining p rows are the vectors in the set P . Combining
                        DM : Ω → Ω                       (11)    these quite different sets of configuration variables into
                                                                 a single matrix serves to remind us that at the highest
                                                                 level of our search algorithm both sets are treated in a
          x 7→ x + β [πD (fC (x)) − πC (fD (x))] ,       (12)    uniform manner by the projection operators. The de-
                                                                 tailed constraints, of course, distinguish among the two
where                                                            parts of M, which we denote M0 (lattice generators) and
                                                               M1 (primitive sphere centers). The set of all the centers
                          1           1                          of spheres in the packing is then the Minkowski sum
             fD (x) = 1 −     πD (x) + x,
                          β           β
                                                                          Λ + P = {b0 M0 + y : b0 ∈ Zd , y ∈ P }          (14)
                                                                                                  d
                                                                                = {bM : b ∈ Z ⊕ Ep },
                            1           1
             fC (x) =    1+     πC (x) − x.
                            β           β                        where Ep is the set of coordinate-permutations of the p-
                                                                 dimensional vector (1, 0, 0, . . . , 0). The space R(d+p)×d of
In this paper we use only β = 1. A difference map                generating matrices takes the role of the physical config-
search proceeds by starting from a random initial config-        uration space Ψ.
uration x0 and iteratively applying the difference map:            A matrix M generates a valid packing if the centers
xi = DM(xi−1 ) [18]. When the map reaches a fixed point          of any two sphere of the packing, b1 M and b2 M, are
xf p , a solution is obtained by                                 separated at least by a distance of 2r when b1 6= b2 .
                                                                 Each choice of b1 and b2 generates a constraint on the
          xsol = πC (fD (xf p )) = πD (fC (xf p )) .     (13)    matrix M
Notice that the ability to obtain a solution from any fixed                         ||b1 M − b2 M|| ≥ 2r,                 (15)
point of the map, due to the cancelation of the two brack-
eted terms in (12), relies on the definition of the problem      which we call an exclusion constraint. Note that there are
in terms of only two simple constraints. For a given it-         infinitely many independent exclusion constraints (con-
erate xi , the terms πC (fD (xi )) and πD (fC (xi )) provide     straints with b1 − b2 = b′1 − b′2 are not independent).
two estimates of the solution, each satisfying one of the        However, for any non-degenerate matrix M only finitely
two constraints. We call these respectively the C- and           many independent exclusion constraints are violated or
                                                                                                                           6

are even remotely close to being violated. In practice,         because it requires different periodic images of a primitive
only those constraints need be tested in our computa-           particle to lie on the points of a lattice, and requires that
tions. We call those constraints the relevant exclusion         lattice to be the same for all primitive particles (up to
constraints (let there be n of them), and we define a           translation). Again, as in Section II A, we combine the
2n × (d + p) matrix A whose rows a2i−1 and a2i are              lattice constraint with the density constraint to form the
the vectors b1 and b2 related to the ith relevant ex-           “concur” constraint:
clusion constraint. We discuss below how the relevant
constraints are identified.                                              C =A(Kdensity )                                (20)
   The linear map A : M 7→ X = AM is a map from the                        ={X = AM ∈ Ω : | det M0 | ≤ Vtarget }.
physical configuration space Ψ to a larger-dimensional
space, Ω = R2n×d , which we use as the formal configura-           With these definitions of the constraint sets, X =
tion space. As before, since the map A is not surjective,       AM ∈ C ∩D if and only if M generates a periodic packing
only a subset (a linear subspace, in fact) of formal config-    of density φ ≥ φtarget . The action of the projections πD
urations have a corresponding generating matrix in the          and πC to the two constraints is illustrated in Figure 2
physical configuration space. The choice of constraints         and Sections IV A and IV B discuss how the projections
below will guarantee that solutions belong to this subset.      are computed efficiently.
The size of the configuration space grows as the number            The basic operations of the search — projections —
of relevant independent exclusion constraints, which is         depend directly on the metric defined on the formal con-
the number of independent near neighbor pairs for which         figuration space. Therefore, the choice of metric affects
overlap needs to be actively avoided. Notice that each          both the complexity of implementing the projection and
relevant exclusion constraint can now be written in terms       the search dynamics. The simplest choice for the metric
of a private set of variables. Specifically, each row of the    is the distance induced from the Frobenius (Euclidean)
matrix X corresponds to the position of one particle, and       norm
the ith relevant exclusion constraint is given by
                                                                    ||X1 − X2 ||2F = trace (X1 − X2 )(X1 − X2 )T . (21)
                                                                                                                
           Di = {X ∈ Ω : ||x2i−1 − x2i || ≥ 2r}.        (16)
                                                                This choice of metric amounts to giving all replicas of a
The intersection of all the relevant exclusion constraints      particle equal weight in influencing its consensus position
forms our “divide” constraint,                                  in the “concur” projection. We can use a slightly different
                                                                Euclidean metric, given by
 D = {X ∈ Ω : ||x2i−1 − x2i || ≥ 2r for i = 1, . . . n}. (17)
                                                                  ||X1 − X2 ||2W = trace W(X1 − X2 )(X1 − X2 )T , (22)
                                                                                                                   
Each set of private variables associated with one exclu-
sion constraint is composed of the coordinates of replicas      where W is a diagonal matrix whose diagonal elements
of two particles, and we call these two replicas a replica      wi are the metric weights of different replicas. Per-
pair.                                                           formance is greatly enhanced by adjusting the metric
   As mentioned in Section II A, the confinement con-           weights throughout the search to afford greater weight
straint of finite packing problems is replaced in the case      to replica pairs that continually violate their constraints
of periodic packings with a constraint on the density of        and smaller weight to replica pairs that are in low risk
the packing. The density of a packing generated by a            of violating their constraints [19]. Note that removing a
matrix M is given by the density of the unit cell, whose        constraint from the list of relevant constraints (i.e., re-
volume is | det M0 | and which contains p particles of vol-     moving the corresponding pair of rows from A and X) is
ume V1 :                                                        equivalent to setting the metric weight of its replicas to
                              pV1                               zero. Therefore, in the course of the search we not only
                      φ=              .                 (18)    adjust the weights wi of replica pairs, but also add and
                           | det M0 |                           remove replica pairs. The details of how these changes
Therefore, if we wish to find a packing of density φ ≥          are applied systematically are given in Section IV C.
φtarget , the density constraint on the generating matrix          This constraint formulation of the periodic sphere
will be                                                         packing problem (finding a periodic packing with density
                                                                φtarget ) can be straightforwardly modified to describe in-
        Kdensity = {M ∈ Ψ : | det M0 | ≤ Vtarget },     (19)    stead the periodic kissing number problem (finding a pe-
                                                                riodic packing with average coordination number τtarget ).
where Vtarget = pV1 /φtarget .                                  First, the “divide” constraint is modified so that each
   As in the example of Section II A, since the map A           replica pair must still be separated by a distance of at
is not surjective, a general element X ∈ Ω of the formal        least 2r, but at least pτtarget replica pairs must be sep-
configuration space does not correspond to a well-defined       arated by a distance of exactly 2r. Second, the condi-
physical configuration. We therefore impose a constraint        tion on the volume of the unit cell is dropped from the
that requires X to lie in the range of A. In the context of     “concur” constraint. Projections to these modified con-
the PDC construction we call this the lattice constraint        straints are also given in Section IV.
                                                                                                                                         7

                                                                               v vertices is represented by a v × d vertex matrix and
 HaL                                             HbL                           is given by the convex hull of these vertices. Although
                                     B                     C       B
               C
                                                                               the configuration of a single particle is no longer rep-
                                                                               resented by a single vector but by a matrix composed
       B
                           A
                           AA
                            A
                                 A
                                                       B
                                                               A               of v vectors, it is convenient to treat these matrices as
                                         C                                 C
                       A
                                                                               vectors, which we typeset as bold-face upper-case Latin
                                                                               letters (e.g., X for the vertex matrix of the polytope
                   C
                                                           C
                                                                               K = conv X = conv{xi : i = 1, . . . v}), and to construct
                                                                   B
                                     B
                                                                               matrices whose rows are such vectors. A translation by
                                                                               t of a polytope conv X is given by conv(X + cT t), where
                                                                               cT is a column vector of unit elements and cT t is the
                                                                               translation matrix corresponding to the translation vec-
                                                                               tor t. Similarly, a rotation is given by conv(XR), where
 HcL       C                         B            HdL                          R is a d × d orthogonal matrix.
                                                                       B          A periodic packing is again generated by the action of
                                                                               a lattice Λ on a set of p primitive polytopes whose vertex
       B               A
                           AA
                            AA                                                 matrices form the set P . The set of all vertex matrices
                       A                     C
                                                                               of polytopes in the packing is the Minkowski sum

                   C
                                                                                    cT Λ + P = {b0 M0 + Y : b0 ∈ Zd , Y ∈ P }         (23)
                                     B                     A                                                 d
                                                                                              = {bM : b ∈ Z ⊕ Ep },

                                                                               where M is a generating matrix of the packing, whose first
                                                                               d rows (comprising M0 ) are translation matrices generat-
                                                                               ing Λ, and whose remaining p rows (comprising M1 ) are
FIG. 2: An illustration of the “divide” and “concur” pro-                      the vertex matrices of the set P . The space of generating
jections in the two-dimensional sphere packing problem with                    matrices Ψ = R(d+p)×(v×d) is the physical configuration
p = 3. (a) A hypothetical configuration of six replica pairs in-               space.
volving the primitive disk A. Disks with the same letter mark-
                                                                                  Each exclusion constraint between two particles of
ing their centers are replicas of the same primitive disk (as for
disk A) or of its lattice translates (as for disks B and C). One               the packing requires the convex hulls conv(b1 M) and
replica pair, violating its exclusion constraint, is emphasized.               conv(b2 M) not to overlap for any b1 6= b2 . To con-
(b) The output of the “concur” projection: the closest config-                 struct the formal configuration space we again form one
uration to (a) such that all replicas of a particular primitive                replica pair for the particles involved in each relevant ex-
disk lie on top of each other, or a lattice translation apart (ar-             clusion constraint, which gives Ω = R2n×(v×d) . The map
rows), and such that those lattice translations define a lattice               A from physical configurations to formal configurations
with a sufficiently small unit cell volume. This projection is                 is given by the matrix A whose rows a2i−1 and a2i are
a modification of the “concur” projection depicted in Figure                   the vectors b1 and b2 related to the ith relevant exclu-
1d,g. (c) The output of the “divide” projection: the clos-                     sion constraint. The “divide” constraint is given by the
est configuration to (a) such that no replica pair violates its
                                                                               intersection of all the relevant exclusion constraints, each
exclusion constraint. This is identical to the “divide” projec-
tion depicted in 1d-f. Detail: (d) the emphasized replica pair
                                                                               expressed in terms of its private replica pair:
before the “divide” projection (thin-outline disks) and after
(thick-outline disks) isolated for clarity.                                       D = {X ∈ Ω : int(conv X2i−1 ∩ conv X2i ) = ∅       (24)
                                                                                                             for i = 1, 2, . . . n}.

                                                                                  In addition to the lattice constraint and the density
                       B.            Convex polytope packing                   constraints, which combine in Section III A to form the
                                                                               “concur” constraint, in the case at hand we must include
   The symmetry of the spherical particle allows its con-                      a third constraint, the rigidity constraint. The primitive
figuration to be described solely by the position of its cen-                  particles of a packing generated by a general matrix M
ter. In the case of a general convex particle, the variables                   are only constrained in their number of vertices, not in
of the configuration space need to include information                         the arrangement of those vertices. However, we are inter-
also about the orientation of the particle. One possible                       ested only in packing where all the particles are congruent
description of the particle assigns variables separately to                    with a given shape, and so we impose the constraint on
the position of its centroid and to the description of the                     M that the vertices of its primitive particles are obtained
rotation about the centroid (e.g., a rotation matrix or a                      from the vertices of the given particle by a rigid motion:
quaternion). In this paper, however, we find it more con-
                                                                                      Krigidity = {M ∈ Ψ : Y = Y(0) Ri + cT ti        (25)
venient to describe convex polytopes by reference to the
positions of their vertices. Therefore, a polytope with                                                for all p rows Y of M1 },
                                                                                                                               8

            “divide” constraint       “concur” constraint                                        HbL
   sphere   ||x2i−1 − x2i || ≥ 2r for X = AM                     HaL
   packing  all n replica pairs       M ∈ Kdensity
   kissing  ||x2i−1 − x2i || ≥ 2r for X = AM
   number   all n replica pairs and
            = 2r for pτtarget pairs
   polytope convex hulls of X2i−1 X = AM
   packing and X2i+1 non-overlap- M ∈ Kdensity                     HcL                          HdL
            ping for all n replica    and M ∈ Krigidity
            pairs

TABLE I: A summary of the D − C constraints for peri-
odic sphere packing, the average kissing number problem, and
polytope packing. The “divide” constraint encompasses the          HeL
relevant exclusion constraints, while the “concur” constraint
                                                                                                 HfL
encompasses, where applicable, the density, rigidity, and lat-
tice constraints.


where Y(0) is the vertex matrix of the given particle. The
“concur” constraint C = A(Kdensity ∩ Krigidity ) is given                         HgL
by combining the density and rigidity constraints on the
generating matrix with the lattice constraint. The result
of constructing the “divide” and “concur” constraints is
that a formal configuration satisfies both of them if and
only if it corresponds to a generating matrix in the physi-
cal configuration space which yields a packing of the given      FIG. 3: An illustration of the polytope exclusion and rigidity
particle with the desired density. Table I summarizes the        constraint projections for the case of regular pentagons. (a)
D − C constraints for the three problems discussed and           The pentagons are non-overlapping, as demonstrated by the
Section IV describes in detail the projections to these          existence of a separating axis that passes through one vertex
constraints.                                                     of each pentagon (red dots). (b) A hypothetical situation
                                                                 of overlapping pentagons. No axis, and particularly no axis
                                                                 passing through one vertex of each pentagon, separates the
                                                                 two sets of vertices. (c) For the input pentagons in (b), the
              IV.     IMPLEMENTATION                             subset S = T (red dots) that minimizes δ(S)2 , the sum of
                                                                 squared-distances to the least-squares axis (red line) while
                                                                 satisfying that the latter separates the remaining vertices. (d)
                A.    “Divide” projections
                                                                 Another choice of S that yields a valid separating axis, but a
                                                                 larger sum of squared-distances. (e) A choice of S that yields
               1.    Sphere packing and kissing                  an axis that fails to separate the remaining vertices. (f) Using
                                                                 T found in (c), the output of the projection to the exclusion
   In order to implement an iterated difference map              constraint is determined by moving the points of T onto their
                                                                 least-squares axis. (g) The output (solid line) of the rigidity
search, whose iterations are given by (12), we must im-
                                                                 projection for the input pentagons (dashed) in (b).
plement efficient projections to the “divide” and “con-
cur” constraints. These implementations are the subject
of Sections IV A and IV B. In the course of the search,
                                                                 the replica pair is one of the pτtarget closest replica pairs.
considerations of efficiency require certain changes to the
formal configuration space – specifically adding and re-
moving replica pairs, changing metric weights, and lat-
tice reduction. In section IV C we discuss when and how                           2.    Convex polytope packing
these changes are applied.
   In the case of sphere packing, the “divide” constraint          Although identifying and resolving overlaps between
simply requires that the centers of the two spheres com-         two spheres is straightforward, the same task is more
prising each replica pair be a certain distance apart. This      challenging in the case of other convex objects, where
is obtained by applying equation (3) to each replica pair.       more degrees of freedom come into play. The literature
Note that the “divide” projection acts independently on          on the topic of detecting overlaps (collisions) between
each replica pair, and since the metric weight of all vari-      polyhedral solids is extensive (driven in part by appli-
ables specifying one replica pair are equal, the metric          cations in computer graphics), and many efficient tech-
weights have no influence on this projection. The action         niques exist for checking whether two convex polyhedra,
of this projection is illustrated in Figure 2. For the kiss-     conv X1 and conv X2 , overlap (see e.g., [23, 24]). In our
ing number problem, the first case of (3) is also used if        case, as we are interested in computing the projection
                                                                                                                               9

to the exclusion constraint, we also need to determine           a least-squares plane separating the remaining vertices
the distance-minimizing resolution of the overlap. That          X1 \ S from X2 \ S, find the one with the minimal sum of
is, we must find the smallest displacement of the vertices       squared distances (28). This is the set T (Figure 3c–f).
such that the new polyhedra do not overlap. As far as we           The least-squares plane Vls of a set S is determined
have been able to determine, there is not an established,        by minimizing the sum of squared distances (28). Note
efficient computational method developed for this specific       that for a fixed normal direction n̂, the value
                                                                                                               P of h that
problem. The method we provide here is efficient enough          minimizes the sum is h = n̂ · r, where r = r∈S r/|S| is
for the purpose of packing polyhedra with a small num-           the centroid of S. Therefore, we wish to minimize
ber of vertices, but the computation time required grows                                     "                  #
exponentially with the number of vertices. A more effi-              X                        X
cient resolution method for particles with more vertices                [n̂ · (r − r)]2 = n̂    (r − r)T (r − r) n̂T , (29)
and for smooth particles is currently in development.               r∈S                      r∈S

   The method relies on the separating plane theorem:            the minimum of which is P equal to the smallest eigenvalue
the convex hulls of two sets of vertices in Rd do not over-      of the symmetric matrix r∈S (r − r)T (r − r). The mini-
lap if and only if there is a (d − 1)-dimensional plane          mum is realized when n̂ is the corresponding eigenvector.
that separates the two sets, so that each is contained in        Degenerate cases with equal lowest eigenvalues occur, but
a different half-space. The theorem can be made even             they do not pose a problem: whenever an optimal sepa-
stronger by specifying that the separating plane can al-         rating plane occurs as a degenerate least-squares plane of
ways be chosen to contain d vertices from the given sets,        some set S, its degeneracy implies that there is a least-
including at least one from each. Therefore, one can             squares plane of S which also includes an extra vertex;
check whether two polytopes overlap by checking whether          this plane will be equally optimal and will occur as a
they are separated by any of the planes defined by any           less degenerate least-squares plane of a superset S ′ ⊇ S.
such subset of vertices (Figure 3a–b). If the polytopes          Therefore, the optimal least-squares plane always occurs
are non-overlapping, the resolution leaves the vertices un-      as a non-degenerate least-squares plane of a set S.
changed.                                                            To summarize, the overlap detection and resolution al-
   If the polytopes overlap, we must find the smallest dis-      gorithm consists of three steps (illustrated in Figure 3a–
placement of their vertices that resolves the overlap. In        f):
the resolved configuration there is a separating plane,
Vsp = {r ∈ Rd : n̂sp ·r = hsp }, that separates the two sets       1. Consider all subsets S ⊆ X1 ∪ X2 of size |S| = d
of vertices. As a consequence of distance minimization,               with at least one point from each polytope. Let
the only vertices moved in the course of the resolution are           V = {r ∈ Rd : n̂ · r = h} be a plane that includes
the vertices which lie on Vsp in the resolved configuration.          S. For each S let
Let T and T ′ be the pre- and post-resolution positions,                      X                   X
respectively, of those vertices that are displaced during          ∆2+ (S) =      (n̂ · x − h)2 +    (n̂ · x − h)2 , (30)
the resolution. Therefore, T ′ is the set of points in Vsp                     x∈X1                    x∈X2
                                                                               n̂·x>h                 n̂·x≤h
closest to the points of T :                                                    X                      X
                                                                   ∆2− (S) =        (n̂ · x − h)2 +        (n̂ · x − h)2 ,   (31)
      ′
     T = {r + (hsp − r · n̂sp )n̂sp : r ∈ T } ⊆ Vsp .    (26)                  x∈X1                    x∈X2
                                                                               n̂·x≤h                 n̂·x>h
The squared norm of the resolution displacement is                        ∆2 (S) = min(∆2+ (S), ∆2− (S)),                    (32)
                 X
                     (hsp − r · n̂sp )2 .          (27)               and let
                    r∈T
                                                                                        ∆2 = min∆2 (S).                      (33)
  For any set of points S there is at least one plane V =                                     S
{r ∈ Rd : n̂ · r = h} that minimizes the sum of squared
distances                                                             ∆2 provides a measure for the interpenetration of
                      X                                               the two polytopes. If ∆2 = 0, then a separating
                         (n̂ · r − h)2 .              (28)            plane exists, the input polytopes do not overlap,
                       r∈S                                            and the algorithm ends here by returning the orig-
                                                                      inal vertex positions X1 and X2 . If ∆2 > 0, the
We call such a plane a least-squares plane of S. The                  polytopes overlap and the algorithm continues to
separating plane of the resolved configuration is always              Step 2.
a least-squares plane of T . If this were not the case, a
small tilting of the separating plane towards such a least-         2. Consider all subsets S ⊆ X1 ∪ X2 of size |S| > d
squares plane (with a corresponding movement of the                    with at least one point from each polytope. Let
points in T ′ ) would result in a resolution by a smaller dis-         V = {r ∈ Rd : n̂ · r = h} be a least-squares plane
placement. In order to resolve an overlap between poly-                of S. If the plane separates the vertex sets with
topes conv X1 and conv X2 , we therefore have to solve a               the points of S removed — X1 \ S and X2 \ S —
discrete problem: among all subsets S of X1 ∪ X2 with                  let δ 2 (S) be the sum of squared-distances from S
                                                                                                                        10

     to the plane. Otherwise, let δ 2 (S) = ∞. Among           This projection strategy parallels the two-step strat-
     the subsets S considered, let T be the subset that      egy used in Section II A. First, the formal configuration
     minimizes δ 2 (S) and VT = {r ∈ Rd : n̂T ·r = hT } be   X is projected to the range A(Ψ) of the physical config-
     its associated least-squares plane. As δ 2 (S) < ∞      uration space, giving AM. Then, the projection of M to
     if S contains all vertices, the minimum is always       the additional constraint K is performed in the physical
     finite. Continue to Step 3.                             configuration space using the metric induced on its im-
                                                             age in the formal configuration space. Below, we solve
   3. The sets of vertices returned are given by X1′ and     the second step of this projection problem for various
      X2′ , wherein x′ ∈ X1′ ∪ X2′ is given by               constraints K.
               (
            ′    x                       if x 6∈ T
          x =                                        (34)
                 x + (hT − x · n̂T )n̂T if x ∈ T ,                              2.     Density constraint

     where x ∈ X1 ∪ X2 is the corresponding original            In the “concur” constraint for the sphere packing prob-
     vertex position.                                        lem, the only constraint on the generating matrix is the
   The projection πD (X) to the “divide” constraint (24),    density constraint. The set of generating matrices M sat-
of an input matrix X comprised of pairs of vertex matrices   isfying the density constraint is
X2i−1 and X2i , is then achieved by applying the above
algorithm independently to all i = 1, . . . n pairs.                    Kdensity = {M : | det M0 | ≤ Vtarget },       (41)

                                                             where M0 is the generating matrix of the lattice and is
              B.     “Concur” projections                    given by the first d rows of M. If | det M0 | ≤ Vtarget , then
                                                             the projection to the constraint (the choice of M that
                                                             minimizes the cost function (40)) is trivially M = M.
                    1.   Lattice constraint
                                                             Otherwise, since M1 is unconstrained, we can minimize
                                                             (40) with respect to M1 for a given M0 . This yields M1 =
  All the “concur” constraint sets described in this paper             −1
                                                             M1 − W′ 11 W10 ′
                                                                               (M0 − M0 ), where WIJ  ′
                                                                                                           are the block-
are of the form                                                              ′
                                                             elements of W acting on MI to the left and on MJ to
         C = A(K) = {X = AM ∈ Ω : M ∈ K}             (35)    the right. Thus, the cost function for M0 is simply

                                                                 f (M0 ) = trace W′′ (M0 − M0 )(M0 − M0 )T ,
                                                                                                               
where A is constant, and M is variable, but must satisfy                                                               (42)
a constraint M ∈ K. The projection then is given by                                           −1
                                                             where W′′ = W00 ′
                                                                               − W01′
                                                                                      W′ 11 W10
                                                                                              ′
                                                                                                .
                                 ′
                    πC : X 7→ X = AM,                (36)      The projection becomes easier to analyze in terms of
                                                             the matrix L = (W′′ )1/2 M0 . The cost function then takes
where M realizes the minimum over K of the distance          the form of the simple Frobenius distance
  ||X − X ′ ||2 = trace W(X − AM)(X − AM)T . (37)
                                            
                                                                         f (L) = trace (L − L)(L − L)T ,
                                                                                                         
                                                                                                                   (43)
  Absent any constraints on M (as for example in the
“concur” constraint for the kissing number problem,          and the density constraint is still in the form
where K = Ψ), the solution would be given by                                                      ′
                                                                                     | det L| ≤ Vtarget ,             (44)
                          T      −1    T
                M = (A WA)            A WX.          (38)              ′
                                                             where Vtarget  = Vtarget /| det W ′′ |1/2 . Since the absolute
This can easily be seen by writing M = M + δM, which         value of the determinant of L is given by the product
gives                                                        of its singular values, the solution to this minimization
                                                             problem is given by a matrix L = UΣV with the same
      ||X − X ′ ||2 = trace W(X − AM)(X − AM)T
                                               
                                                             (right and left) singular vectors as the matrix L = UΣV,
                   = c + trace(WA δM δMT AT )                but different singular values. The cost function expressed
                                                             in terms of the singular values σi and σi of, respectively,
                   = c + trace(W′ δM δMT ),          (39)    L and L takes the form
where W′ = AT WA and the constant term c does not de-                                      d
                                                                                           X
pend on δM. The second term is non-negative, and when                           f (Σ) =          (σi − σi )2 .        (45)
M is unconstrained, (39) is minimized by letting M = M.                                    i=1
Additionally, we have just reduced the constrained case
to the problem of finding M ∈ K that minimizes the cost      We numerically minimize this quadratic function subject
function                                                     to the density constraint (44). Through back substitu-
                                                             tion we then have the matrix M that minimizes (37) and
         f (M) = trace W′ (M − M)(M − M)T .                  πC (X) = X′ = AM.
                                              
                                                    (40)
                                                                                                                          11

                   3.   Rigidity constraint                          C.   Formal configuration space maintenance


   In the “concur” constraint for the polytope packing              In our discussion of the choice of metric in Section III,
problem, an additional constraint on the generating ma-          we discussed the ideas of dynamically readjusting the
trix M is that the primitive polytopes that make up M1           metric (through the weights wi of the various replicas)
are congruent with a given polytope. The generating              and of removing and adding replicas (removing replicas is
matrix is then constrained to the set                            formally equivalent to setting their weight to zero). The
                                                                 latter is necessary for implementation reasons: there are
                                                                 infinitely many independent exclusion constraints (and
                  K = Kdensity ∩ Krigidity               (46)    therefore replicas), but we can only represent a finite
                                                                 number of replicas in our implementation. As the set of
where                                                            relevant constraints changes over the course of the search,
                                                                 we must remove and add replicas. Our criterion for which
                                                                 replicas to represent is based on the difference map’s cur-
          Kdensity = {M : | det M0 | ≤ Vtarget },                rent “concur” estimate: we include a replica pair for each
          Krigidity = {M : Y = Y(0) Ri + cT ti                   pair of particles whose centroids in the “concur” estimate
                       for all p rows Y of M1 }.                 are closer than some cut-off distance. Using the gener-
                                                                 ating matrix obtained in the “concur” projection we can
                                                                 easily find all such pairs using the method of Agrell et al.
To calculate the projection πC (X), the cost function (40)       [27]. The cut-off distance is chosen so that at least all
must be minimized over K. However, since the off-                replicas that might be in risk of overlap are represented.
                     ′
diagonal block W01      couples the lattice parameters M0           The problem of implementation is not the only reason
to the primitive particle parameters M1 , this minimiza-         we wish to limit the number of replicas we represent. A
tion is complicated. Instead of exact minimization, we           proliferation of unnecessary replicas has the adverse effect
employ a two-step heuristic method, which results in an          of attenuating the information obtained from the “con-
approximate projection.                                          cur” projection by diluting the influence of more critical
   In the first step, we calculate the matrix M′ ∈ Kdensity      replicas. We observe that such replica proliferation could
that minimizes the cost function, as in Section IV B 2.          result not only in a slower search, but also in an increased
Then, in the second step, we calculate the matrix M ∈ K          tendency to become trapped in local optima. Limiting
by applying to each row Y of M′1 the smallest change so          the number of replicas is one way to avoid this effect,
that it becomes a vertex matrix of a polytope congruent          but we find it useful to further amplify the information
with the reference polytope. The second step is achieved         from critical constraints by giving them greater weights
by finding the rigid motion applied to the reference poly-       [19]. We perform the weight adjustments adiabatically,
tope which brings its vertices as close as possible to the       that is, slowly over the course of many iterations, by up-
vertices of Y as measured by the sum of squared distances        dating the weights of each replica pair according to the
(Figure 3g). The problem of finding the rigid motion that        rule
brings one given list of points closest to another given list,                             τ wi + wi′ (Xc )
sometimes known as the problem of absolute orientation,                             wi →                    ,           (47)
                                                                                                τ +1
occurs frequently in a variety of fields (e.g., in calculat-
ing RMSD between two conformations of a biomolecule)             where wi′ (Xc ) is a function that assigns replicas weights
and several efficient methods for its solution have been         based on their configuration in the “concur” estimate,
developed (see [25, 26]).                                        and τ is a relaxation time for the replica weights in units
   The output of the approximate projection is then given        of iterations.
by X′ = π̃C (X) = AM ≈ πC (X). As X′ ∈ C, the approx-               In the sphere packing problem (in d dimensions, with
imate projection gives a configuration in the constraint         unit spheres), we choose the weight function to be
set, but might not give the closest one to the input config-                     (             2

uration. We justify the use of the approximate projection               ′          eα(4−||xi || )       if ||xi || ≤ 2
                                                                      wi (Xc ) =                                        (48)
by noting that it is an exact projection if the off-diagonal                       (||xi ||2 − 3)−2−d/2 if ||xi || > 2,
         ′
block W01    is zero. A non-zero off-diagonal block is the
result of correlations in the relevant exclusion constraint      with α ≈ 20. The dimensional dependence is chosen so
vectors b between the coefficients of lattice translations       that under the assumption of uniform density, the to-
and the coefficients of primitive particle vertex positions.     tal weight from replicas over a certain distance follows a
We expect these coefficients to give uncorrelated contri-        dimension-independent power law. In the polytope pack-
butions and to add up to small off-diagonal elements due         ing problem, we similarly use
to random cancellations. Indeed, we find that the off-                       (     2

diagonal block is small in comparison with the diagonal            ′           eα∆i               if the polytopes overlap
                                                                  wi (Xc ) =
blocks, and we expect our heuristic to yield a good ap-                        (1 + ri2 − 4rin
                                                                                            2 −2
                                                                                               )  if not,
proximate projection.                                                                                                  (49)
                                                                                                                          12

                                                                             (L)
with α ≈ 10, where rin is the inradius of the polytope,        d Λdensest φdensest hNiter i hni    titer success rate
ri is the centroid-centroid distance of the polytopes, and     2 A2       0.90690 42        11     0.1ms 100/100
∆2i is the measure of the overlap between the polytopes        3 D3       0.74047 230       38     0.2ms 100/100
defined in (33).                                               4 D4       0.61685 191       127    0.4ms 100/100
                                                               5 D5       0.46526 308       323    1ms 100/100
   In addition to the maintenance of replicas, which is
                                                               6 E6       0.37295 173       977    2ms 100/100
performed after every iteration of the difference map,         7 E7       0.29530 217       2740   5ms 96/100
we also periodically perform a lattice reduction using         8 E8       0.25367 99        8528   20ms 96/100
the LLL algorithm [28]. The lattice generated by M0 is         9 Λ9       0.14577 161       16314 30ms 85/100
re-represented using the LLL-reduced generating matrix         10 Λ10     0.092021 394      31433 70ms 47/100
M′0 = G0 M0 , where G0 is a unimodular integer matrix.         11 K11     0.060432 421      68722 0.3s 54/100
Additionally, all primitive particles
                                   P whose centroids are       12 K12     0.049454 397      204321 0.9s 55/100
outside of the unit cell given by { i λi ai : − 1/2 ≤ λi <     13 K13     0.029208 577      430796 2s    25/100
1/2} are re-represented by their lattice-translate in that     14 Λ14     0.021624 1652 1007250 6s       4/10
cell. In summary, the new packing generating matrix M′
                                                             TABLE II: Results of PDC searches for dense lattice packing
is given by
                                                             in dimensions d = 2, . . . 14. For each dimension, 100 runs from
                                                           random initial conditions were performed with the density
                                G0 0
                 M′ = GM =               M,           (50)                        (L)
                                                             target φtarget = φdensest , the density of the densest known
                                G1 1                         lattice Λdensest [15]. The runs were limited to 5000 iterations,
                                                             and the number of converged runs is quoted in the right-
where G1 gives the lattice translations to be applied to     most column. For dimensions 10 and above, each run was
the primitive particles. Since the actual positions of the   first allowed to converge at a density target of 0.8φdensest and
particles, as represented in the matrix X = AM, should       then continued with the final target. The mean number of
be unchanged, the lattice reduction must also be applied     difference map iterations in converged runs was hNiter i, and
to the nominally constant matrix A (A → A′ = AG−1 ).         the mean number of relevant exclusion constraint used was
                                                             hni. Each iteration took an average runtime of titer on a
                                                             single 3 GHz CPU. In d = 14 only 10 runs were performed
                                                             with three intermediate targets.
                       V.   RESULTS

                  A.    Sphere packing
                                                             the searches reproduced the lattice packing, suggesting
                                                             that the lattice packing in these dimensions is the opti-
   Using the PDC scheme described in the previous sec-       mal packing with a small number of spheres in the unit
tions we perform a de novo search for the densest lattice    cell.
(p = 1) sphere packings in dimensions 2—14. The PDC
search, starting from random initial configurations, was
able to reproduce the densest packing lattices known for                           B.   Kissing number
all cases, and the results of the search are summarized in
Table II. For dimensions 2—8 the lattices are known to
be optimal, and for dimensions 9—14 these results are,          For the kissing number problem, PDC searches were
to our knowledge, the first numerical evidence from a de     able to reproduce the best known lattice kissing arrange-
novo search that the known lattices are optimal.             ments in dimensions 2—11. In dimensions 2—9, the re-
   Note that the number of replicas is determined by the     sult is known to be optimal, and for dimensions 10 and
number of near neighbors of each sphere, which rises         11, we are not aware of previous numerical evidence for
rapidly with the number of dimensions. This rise causes      their optimality. Table III summarizes the performance
an increased computational storage cost per physical de-     of our method.
gree of freedom in a PDC search, compared to a con-
stant storage cost per physical degree of freedom in a
method involving a local search in the physical configura-                     C.       Polytope packing
tion space. However, this rise need not affect the scaling
of CPU costs, since both search methods need necessarily        By inspection of a packing of regular tetrahedra yielded
check a comparable number of particle pairs for possible     by our numerical search during early phases of its devel-
overlaps.                                                    opment, we were able to construct a new transitive, peri-
   In dimensions d = 10, 11, 13 there are known non-         odic (p = 4) packing of tetrahedra with a higher density
lattice packings with p = 40, 72, 144 respectively that      (φ ≈ 0.8547) than previously reported [1]. This packing
are denser than the densest known lattices [15]. In up to    takes the form of a double lattice of bipyramidal dimers
11 dimensions, we searched for non-lattice packings with     (the union of two face-sharing tetrahedra). The packing
as many as p = 12 primitive spheres, but the searches        has since been slightly improved to a closely related, but
did not produce packings denser than the lattice pack-       less symmetric packing with density φ ≈ 0.8563 [10, 11].
ings. For a density target matching the lattice density,     In its current form, our search method is able to repro-
                                                                                                                                       13

                        (L)
        d Λhighest τhighest hNiter i hni   success rate                  primitive pentatopes K1 = conv{r1 , r2 , r3 , r4 , r5 }
        2 A2       6        27       12    100/100                                            K2 = conv{r2 , r3 , r4 , r5 r6 }
        3 D3       12       54       40    100/100                                            K3 = t − K1
        4 D4       24       132      118 98/100                                               K4 =√t − K2
        5 D5       40       163      331 94/100                                        where r1 = 5(1, 1, 1, 1)
        6 E6       72       225      928 64/100                                               r2 = (3, −1, −1, −1)
        7 E7       126      597      2729 66/100                                              r3 = (−1, 3, −1, −1)
        8 E8       240      511      6988 55/100                                              r4 = (−1, −1, 3, −1)
        9 Λ9       272      350      15604 63/100                                             r5 = (−1,
                                                                                                      √ −1, −1, 3)
        10 Λ10     336      438      32203 28/100                                             r6 = − 5(1, 1, 1, 1) √
        11 Λ11     438      549      73766 10/100                                             t = 41 (−7, 1, 3, 3) − 45 (1, 1, 1, 1)
                                                                         lattice              Λ = Z4 M 0
TABLE III: Results of PDC searches for lattice packing with
                                                                                                                                 
                                                                                                          −6 10 −6 2
high kissing number in dimensions d = 2, . . . 11. For each                                             −8 −4 4 8 
dimension, 100 runs from random initial conditions were per-                           where M0 = 14   −7 5 9 −7 
                                                                                                                                 
                                              (L)
formed with a target coordination τtarget = τhighest , the high-
                                                                                                        1 −7        9 −3
est coordination number known for a lattice of that dimen-                                                2 2 2 2
sion, Λhighest [15]. The runs were limited to 5000 iterations,                                     √ 
                                                                                                          2 2 2 2
and the number of converged runs is quoted in the right-most                                    + 45  1 1 1 1
                                                                                                                     
column. The mean number of difference map iteration in                                                    3 3 3 3
converged runs was hNiter i, and the mean number of relevant
exclusion constraints used was hni.                                   TABLE IV: Coordinates of the densest pentatope packing
                                                                      discovered by the PDC search (φ = 4 vol(K1 )/ det(M0 ) =
    2                                                                 128/219 ≈ 0.5845).
                                                iteration
    0
               10 000         20 000                30 000   40 000
                                                                      takes the form of a double lattice of dimers (a dimer here
   -2
                                                                      is the union of two cell-sharing pentatopes). This struc-
                                                                      ture, composed of a repeating unit of two oppositely ori-
   -4
                                                                      ented dimers, repeatedly came up as the densest in de
                                                                      novo PDC searches with p = 4 and p = 8 pentatopes in
   -6                                          1+log10 Ε2
                                                                      the unit cell, whereas searches with intermediate values
                                                                      of p yielded sparser packings. We subsequently refined
   -8
                                       log10 SDi2                     the packing with a restricted search where the dimer was
  -10
                                                                      taken as the basic particle.
                                                                         Note that the density reported is slightly lower than
FIG. 4: The course of a sample run searching for dense peri-          that of the densest known packing of four-dimensional
odic packings                                                         spheres (φ = π 2 /16 ≈ 0.6169). It remains to be deter-
          P 2(p = 4) of unit edge-length regular tetrahedra,
showing     ∆i , a measure of the total interpenetration be-          mined whether this is the case because the optimal pack-
tween tetrahedra in the “concur” estimate (blue, defined in           ing density of pentatopes is smaller than that of spheres
(33)), and ǫ2 , the squared distance between the “divide” and         or because the dimer double lattice is suboptimal. The
“concur” estimates (purple, shifted up for clarity), both on a        vertex coordinates of the four primitive pentatopes and
logarithmic scale. The density target for the search is started       the generating matrix of the lattice are given in Table
at φtarget = 0.75 and adjusted when the search is converged           IV.
on a solution (vertical red lines) to φtarget = 0.82 (at itera-
tion 15751) and then to φtarget = 0.8563 (at iteration 15898).
Each iteration took 14 millisecond on average on a single 3
                                                                                         VI.    CONCLUSION
GHz CPU.

                                                                         In this article we report on the development of PDC,
duce this densest known packing reliably (fifteen out of a            a novel, constraint-based method for discovering dense
hundred runs converged within the iteration limit), and               periodic packings through de novo numerical searches.
Figure 4 shows the results of a sample run converging to              We lay out the principles of the method and demon-
this packing.                                                         strate its application for selected problems. In addition
  For the problem of packing regular four-dimensional                 to the dense packing of regular tetrahedra reported in
simplices (pentatopes) in four-dimensional Euclidean                  Ref. [1], we also discover a new dense packing of regu-
space, we report a new packing discovered by our search               lar pentatopes using the PDC method. We also use the
method (Figure 5). This packing, with density φ =                     method to numerically recover the lattice sphere pack-
128/219 ≈ 0.5845, is, to our knowledge, denser than any               ings of highest known density and highest known kissing
previously reported packing of regular pentatopes. Like               number in a range of dimensions, providing empirical ev-
the densest known tetrahedron packing, this packing also              idence of their optimality.
                                                                                                                         14

                                                                 ear combinations of the original parameters, such that
                                                                 these new parameters over-determine the configuration.
                                                                 Therefore, by contrast with the traditional construction,
                                                                 where new parameters are, specifically, redundant copies
                                                                 of original parameters and concurrence is described by
                                                                 the equality of all copies of a given original parameter,
                                                                 here we allow concurrence to be described by a general
                                                                 linear relation. With this generalization, we can treat
                                                                 the periodic images of a particle as “replicas” of the par-
                                                                 ticle, even as they are related by a lattice vector instead
                                                                 of being identical. Thus, the variables describing the pe-
                                                                 riodic repetition of the configuration, namely the lattice
                                                                 vectors, are not imposed as constants or adjusted in ded-
                                                                 icated steps. Instead, due to the projection formulation
                                                                 of the dynamics, the unit cell variables that minimize the
                                                                 change to the configuration are determined at each iter-
                                                                 ation. These variables are treated on the same footing as
                                                                 particle positions and orientations and are optimized as
                                                                 aggressively.
                                                                    Additionally, we develop a displacement-minimizing
                                                                 overlap resolution algorithm for the convex hulls of two
                                                                 sets of points in Rd . We use this algorithm to implement
                                                                 the projection to the exclusion constraint in the case of
                                                                 polytopal particles.
                                                                    Unlike Monte Carlo simulations, which explore the
                                                                 physical optimization landscape using stochastic moves,
                                                                 a PDC search uses a deterministic map in an expanded,
                                                                 non-physical configuration space. As such, it is useful
                                                                 when interest lies more in discovering optimal configu-
                                                                 rations and less in discovering the physical pathways to
                                                                 such configurations. However, introducing non-physical
                                                                 dynamics has been observed to be important in over-
                                                                 coming dynamical stagnation [9]. The projection-based
                                                                 dynamics make PDC particularly well-suited in problems
                                                                 with hard constraints, such as hard particle packing, or
                                                                 with step potentials, which prohibit the use of gradient
FIG. 5: The top figure shows a two-dimensional cut through       information.
the densest known packing of tetrahedra. The plane of the           While no direct comparison has been made between
cut is parallel to the bases of the bipyramidal dimers. Trian-   the performance of PDC and Monte Carlo searches in
gular sections from dimers of one orientation (red) and from     the case of periodic packing problems, difference map and
dimers of inverted orientation (blue) are visible. The bot-
tom figure shows a three-dimensional cut through the densest
                                                                 D − C methods in the case of other problems have been
known packing of pentatopes. The cut is taken parallel to the    shown to perform better than or on a par with specialized
bases of the pentatope dimers, and tetrahedral sections from     and general-purpose methods [18–20, 29]. The generality
the two dimer orientations (red and blue, again) are visible.    of the PDC scheme and its demonstrated ability to dis-
                                                                 cover dense packings in a variety of settings indicate its
                                                                 utility as a general method for conducting de novo nu-
   In developing the PDC scheme, we adapt the D − C              merical searches and as a possibly attractive alternative
framework to periodic systems. PDC retains the mind-             to conventional methods [30].
set of the traditional D − C approach of Ref. [19], but             Y. K. acknowledges N. Duane Loh for valuable dis-
generalizes its formalism in a few ways. We introduce            cussions. This work was supported by grant NSF-DMR-
an expanded configuration space parameterized by lin-            0426568.




 [1] Y. Kallus, V. Elser, and S. Gravel, Discrete Compu.          [3] D. Rowe and J. Jeremy, The Hilbert Challenge (Oxford
     Geom. 44, 245 (2010).                                            University Press, 2001).
 [2] D. Hilbert, Bull. Am. Math. Soc. 8, 437 (1902).              [4] T. C. Hales, Ann. Math. 162, 1065 (2005).
                                                                                                                          15

 [5] A. Donev, F. H. Stillinger, P. M. Chaikin, and             [19] S. Gravel and V. Elser, Phys. Rev. E 78, 036706 (2008).
     S. Torquato, Phys. Rev. Lett. 92, 255506 (2004).           [20] S. Gravel, Ph.D. thesis, Cornell University, Ithaca, New
 [6] S. Torquato and Y. Jiao, Nature 460, 876 (2009).                York (2009).
 [7] S. Torquato and Y. Jiao, Phys. Rev. E 80, 041104 (2009).   [21] H. Cohn, A. Kumar, and A. Schürmann, Phys. Rev. E
 [8] E. R. Chen, Discrete Comput. Geom. 5, 214 (2008).               (2010), accepted for publication.
 [9] M. E. A. Haji-Akbari et al., Nature 462, 773 (2009).       [22] V. Elser and S. Gravel, Discrete Comput. Geom. 43, 363
[10] S. Torquato and Y. Jiao, Phys. Rev. E 81, 041310 (2010).        (2010).
[11] E. R. Chen, M. Engel, and S. C. Glotzer, Discrete          [23] G. van den Bergen, Proximity queries and penetration
     Compu. Geom. 44, 253 (2010).                                    depth computation on 3d game objects (2001), game De-
[12] Y. Jiao, F. H. Stillinger, and S. Torquato, Phys. Rev. E        velopers Conference.
     79, 041309 (2009).                                         [24] S. Cameron, in Proceedings of International Conference
[13] G. Kuperberg and W. Kuperberg, Discrete Compu.                  on Robotics and Automation (1997), p. 3112.
     Geom. 5, 389 (1990).                                       [25] B. K. P. Horn, J. Opt. Soc. Am. A 4, 629 (1987).
[14] M. Gardner, The Colossal Book of Mathematics: Classic      [26] B. K. P. Horn, H. M. Hilden, and S. Negahdaripour, J.
     Puzzles, Paradoxes, and Problems (Norton, New York,             Opt. Soc. Am. A 5, 1127 (1988).
     2001).                                                     [27] E. Agrell et al., IEEE Trans. Inform. Theory 48, 2201
[15] J. H. Conway and N. J. A. Sloane, Sphere Packings, Lat-         (2002).
     tices and Groups (Springer-Verlag, New York, 1998), 3rd    [28] A. K. Lenstra, H. W. Lenstra, and L. Lovász, Math. Ann.
     ed.                                                             261, 515 (1982).
[16] A. Schürmann and F. Vallentin, Discrete Comput. Geom.     [29] V. Elser and I. Rankenburg, Phys. Rev. E 73, 026702
     35, 73 (2006).                                                  (2006).
[17] J. H. Conway and S. Torquato, Proc. Natl. Acad. Sci.       [30] An implementation of our algorithm is available upon
     USA 103, 10612 (2006).                                          request from the corresponding author.
[18] V. Elser, I. Rankenburg, and P. Thibault, Proc. Natl.
     Acad. Sci. USA 104, 418 (2007).
