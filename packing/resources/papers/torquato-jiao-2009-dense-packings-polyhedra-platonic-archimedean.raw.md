                                         Dense Packings of Polyhedra: Platonic and Archimedean Solids

                                                                               S. Torquato1,2,3,4,5,6 and Y. Jiao6
                                                                  1
                                                                      Department of Chemistry, Princeton University,
                                                                              Princeton New Jersey 08544, USA
                                                                        2
                                                                            Princeton Center for Theoretical Science,
arXiv:0909.0940v3 [math-ph] 9 Sep 2009




                                                           Princeton University, Princeton New Jersey 08544, USA
                                                     3
                                                         Princeton Institute for the Science and Technology of Materials,
                                                           Princeton University, Princeton New Jersey 08544, USA
                                                             4
                                                                 Program in Applied and Computational Mathematics,
                                                           Princeton University, Princeton New Jersey 08544, USA
                                          5
                                              School of Natural Sciences, Institute for Advanced Study, Princeton NJ 08540 and
                                                            6
                                                                Department of Mechanical and Aerospace Engineering,
                                                           Princeton University, Princeton New Jersey 08544, USA




                                                                                              1
                                                 Abstract
  Understanding the nature of dense particle packings is a subject of intense research in the
physical, mathematical and biological sciences. The preponderance of previous work has focused
on spherical particles, and very little is known about dense polyhedral packings. We formulate the
problem of generating dense packings of nonoverlapping, non-tiling polyhedra within an adaptive
fundamental cell subject to periodic boundary conditions as an optimization problem, which we call
the Adaptive Shrinking Cell (ASC) scheme. This novel optimization problem is solved here (using
a variety of multi-particle initial configurations) to find the dense packings of each of the Platonic
solids in three-dimensional Euclidean space R3 , except for the cube, which is the only Platonic solid
that tiles space. We find the densest known packings of tetrahedra, icosahedra, dodecahedra, and
octahedra with densities 0.823 . . ., 0.836 . . ., 0.904 . . ., and 0.947 . . ., respectively. It is noteworthy
that the densest tetrahedral packing possesses no long-range order. Unlike the densest tetrahedral
packing, which must not be a Bravais lattice packing, the densest packings of the other non-tiling
Platonic solids that we obtain are their previously known optimal (Bravais) lattice packings. We
also derive a simple upper bound on the maximal density of packings of congruent nonspherical
particles, and apply it to Platonic solids, Archimedean solids, superballs and ellipsoids. Provided
that what we term the “asphericity” (ratio of the circumradius to inradius) is sufficiently small,
the upper bounds are relatively tight and thus close to the corresponding densities of the optimal
lattice packings of the centrally symmetric Platonic and Archimedean solids. Our simulation
results, rigorous upper bounds, and other theoretical arguments lead us to the conjecture that
the densest packings of Platonic and Archimedean solids with central symmetry are given by
their corresponding densest lattice packings. This can be regarded to be the analog of Kepler’s
sphere conjecture for these solids. The truncated tetrahedron is the only non-centrally symmetric
Archimedean solid, the densest known packing of which is a non-lattice packing with density at least
as high as 23/24 = 0.958333 . . .. We discuss the validity of our conjecture to packings of superballs,
prisms and anti-prisms as well as to high-dimensional analogs of the Platonic solids. In addition, we
conjecture that the optimal packing of any convex, congruent polyhedron without central symmetry
generally is not a lattice packing. Finally, we discuss the possible applications and generalizations
of the ASC scheme in the predicting the crystal structures of polyhedral nanoparticles and the
study of random packings of hard polyhedra.



                                                     2
PACS numbers: 05.20.Jj, 45.70.-n, 61.50.Ah




                                             3
I.    INTRODUCTION


     Particle packing problems are ancient, dating back to the dawn of civilization. Bernal
has remarked that “heaps” (particle packings) were the first things that were ever measured
in the form of basketfuls of grain for the purpose of trading or of collection of taxes [1].
Dense packings of hard particles have served as useful models to understand the structure
of liquid, glassy and crystal states of matter [2, 3, 4], granular media [5], and heterogeneous
materials [3, 6]. Understanding the symmetries and other mathematical properties of the
densest packings in arbitrary dimensions is a problem of long-standing interest in discrete
geometry and number theory [7].
     A large collection of nonoverlapping solid objects (particles) in d-dimensional Euclidean
space Rd is called a packing. The packing density φ is defined as the fraction of space
Rd covered by the particles. A problem that has been a source of fascination to mathe-
maticians and scientists for centuries is the determination of the densest arrangement(s)
of particles that do not tile space and the associated maximal density φmax [7]. Finding
the maximal-density packing arrangements is directly relevant to understanding the struc-
ture and properties of crystalline equilibrium phases of particle systems as well as their
(zero-temperature) ground-state structures in low dimensions in which the interactions are
characterized by steep repulsions and short-ranged attractions.
     The preponderance of previous investigations have focused on dense packings of spheres
in various dimensions [3, 7, 8, 9]. For congruent particles in three dimensions, the sphere
is the only non-tiling particle for which the densest packing arrangements can be proved
[10]. It is only very recently that attention has turned to finding the maximal-density
packing arrangements of nonspherical particles in R3 , including ellipsoids [11, 12], tetrahedra
[13, 14, 15], and superballs [16, 17]. Very little is known about the densest packings of
polyhedral particles [18].
     The Platonic solids (mentioned in Plato’s Timaeus) are convex polyhedra with faces
composed of congruent convex regular polygons. There are exactly five such solids: the
tetrahedron (P1), icosahedron (P2), dodecahedron (P3), octahedron (P4), and cube (P5)
(see Fig. 1) [19]. One major concern in this paper is the determination of the densest
packings of each of the Platonic solids in three-dimensional Euclidean space R3 , except for
the cube, which is the only Platonic solid that tiles space.


                                              4
FIG. 1: (color online). The five Platonic solids: tetrahedron (P1), icosahedron (P2), dodecahedron
(P3), octahedron (P4), and cube (P5).


   It is useful to highlight some basic geometrical properties of the Platonic solids that we
will employ in subsequent sections of the paper. The dihedral angle θ is the interior angle
between any two face planes and is given by

                                              θ   cos(π/q)
                                        sin     =          ,                                  (1)
                                              2   sin(π/p)

where p is the number of sides of each face and q is the number of faces meeting at each
                              √               √               √                  p
vertex. Thus, θ is 2 sin−1 (1/ 3), 2 sin−1 (Φ/ 3), 2 sin−1 (Φ/ Φ2 + 1), 2 sin−1 ( 2/3), and
π/2, for the tetrahedron, icosahedron, dodecahedron, octahedron, and cube, respectively,
                √
where Φ = (1 + 5)/2 is the golden ratio. Thus, since the dihedral angle for the cube is the
only one that is a submultiple of 2π, the cube is the only Platonic solid that tiles space. We
note in passing that in addition to the regular tessellation of space by cubes in the simple
cubic lattice arrangement, there are an infinite number of other irregular tessellations of
space by cubes [20]. Figure 2 shows a portion of a realization of a two-dimensional analog
of such an irregular tessellation.
   Every polyhedron has a dual polyhedron with faces and vertices interchanged. The dual
of each Platonic solid is another Platonic solid, and therefore they can be arranged into dual
pairs: the tetrahedron is self-dual (i.e., its dual is another tetrahedron), the icosahedron and
dodecahedron form a dual pair, and the octahedron and cube form a dual pair.
   An Archimedean solid is a highly symmetric, semi-regular convex polyhedron composed
of two or more types of regular polygons meeting in identical vertices. There are thirteen
Archimedean solids: truncated tetrahedron (A1), truncated icosahedron (A2), snub cube
(A3), snub dodecahedron (A4), rhombicosidodecahdron (A5), truncated icosidodecahdron
(A6), truncated cuboctahedron (A7), icosidodecahedron (A8), rhombicuboctahedron (A9),

                                                 5
 FIG. 2: (color online). A portion of a realization of an irregular tiling of the plane by squares.




FIG. 3: The 13 Archimedean solids: truncated tetrahedron (A1), truncated icosahedron (A2),
snub cube (A3), snub dodecahedron (A4), rhombicosidodecahdron (A5), truncated icosidodecah-
dron (A6), truncated cuboctahedron (A7), icosidodecahedron (A8), rhombicuboctahedron (A9),
truncated dodecahedron (A10), cuboctahedron (A11), truncated cube (A12), and truncated octa-
hedron (A13).


                                                6
truncated dodecahedron (A10), cuboctahedron (A11), truncated cube (A12) and truncated
octahedron (A13) (see Fig. 3). Note that the truncated octahedron is the only Archimedean
solid that tiles space.
   Another important observation is that the tetrahedron (P1) and the truncated tetrahe-
dron (A1) are the only Platonic and Archimedean solids, respectively, that are not centrally
symmetric. A particle is centrally symmetric if it has a center C that bisects every chord
through C connecting any two boundary points of the particle, i.e., the center is a point of
inversion symmetry. We will see that the central symmetry of the majority of the Platonic
and Archimedean solids (P2 – P5, A2 – A13) distinguish their dense packing arrangements
from those of the non-centrally symmetric ones (P1 and A1) in a fundamental way.
   Some basic definitions concerning packings are given here. A saturated packing is one
in which there is no space available to add another particle to the packing. A lattice Λ in
Rd is a subgroup consisting of the integer linear combinations of vectors that constitute a
basis for Rd [21]. A lattice packing PL is one in which the centroids of the nonoverlapping
particles are located at the points of Λ, each oriented in the same direction. The set of
lattice packings is a subset of all possible packings in Rd . In a lattice packing, the space Rd
can be geometrically divided into identical regions F called fundamental cells, each of which
contains just the centroid of one particle. Thus, the density of a lattice packing is given by
                                                vp
                                         φ=           ,                                      (2)
                                              Vol(F )
where vp is the volume of a d-dimensional particle and Vol(F ) is the volume of a fundamental
cell.
   A more general notion than a lattice packing is a periodic packing. A periodic packing of
congruent particles is obtained by placing a fixed nonoverlapping configuration of N particles
(where N ≥ 1) with arbitrary orientations in each fundamental cell of a lattice Λ. Thus, the
packing is still periodic under translations by Λ, but the N particles can occur anywhere in
the chosen fundamental cell subject to the nonoverlap condition. The packing density of a
periodic packing is given by
                                            Nvp
                                      φ=           = ρvp ,                                   (3)
                                           Vol(F )
where ρ = N/Vol(F ) is the number density, i.e., the number of particles per unit volume.
   The determination of the maximal-density arrangements of non-tiling polyhedral parti-
cles is a notoriously difficult problem, especially since such extremal structures will generally

                                              7
be non-Bravais-lattice packings. Computer simulations that seek the maximal-density pack-
ings can be an indispensable tool, especially if they can incorporate collective motions of the
particles in order to obtain, in principle, the highest possible densities. However, the chal-
lenge presented by polyhedral particles in R3 is the non-smooth (i.e., nonanalytic) nature
of the particle shape. In the case of smoothly-shaped particles, such as spheres, ellipsoids
and superballs, one can construct analytic “overlap potential functions” for the particles [24]
and hence one can employ efficient collision-driven molecular dynamics (MD) growth pack-
ing algorithms that inherently involve collective particle motions [12, 16, 17, 25, 26]. The
fact that analytic overlap potential functions cannot be constructed for polyhedral particles
prevents us from using event-driven MD growth methods to study such systems.
   In this paper, we devise a novel optimization scheme, called the Adaptive Shrinking Cell
(ASC), that can be applied to generate dense packings of polyhedra in R3 . We employ it
specifically to obtain the densest known packings of tetrahedra, icosahedra, dodecahedra,
and octahedra with densities 0.823 . . . , 0.836 . . ., 0.904 . . ., and 0.947 . . ., respectively. The
result for tetrahedra improves upon the density reported in our recent investigation [27, 28].
Unlike the densest tetrahedral packing, which must not be a Bravais lattice packing [13], the
densest packings of the other non-tiling Platonic solids that we obtain are their corresponding
densest lattice packings [22, 23].
   We also derive a simple upper bound on the maximal density of packings of congruent
nonspherical particles, and apply it to Platonic solids, Archimedean solids, superballs and
ellipsoids. We introduce the “asphericity” parameter γ (ratio of the circumradius to inradius)
to show that when γ is sufficiently small, the upper bounds are relatively tight and thus close
to the corresponding densities of the optimal lattice packings of octahedra, dodecahedra and
icosahedra as well as of the majority of the Archimedean solids with central symmetry.
   Our simulation results as well as theoretical arguments lead us to conjecture that the
densest packings of Platonic and Archimedean solids with central symmetry are given by
their corresponding densest lattice packings. This can be regarded to be the analog of
Kepler’s sphere conjecture for these solids. The truncated tetrahedron is the only non-
centrally symmetric Archimedean solid, the densest known packing of which is a non-lattice
packing with density as high as 23/24 = 0.958333 . . .. Our work also suggests that the
optimal packings of superballs are their corresponding densest lattice packings.
   In a recent letter [27], we briefly reported the densest known packings of the non-tiling

                                                 8
Platonic solids obtained using the ASC algorithm and proposed the aforementioned conjec-
ture concerning the optimal packings of the Platonic and Archimedean solids. In this paper,
we expand on theoretical and computational details and report additional new results. In
particular, we provide comprehensive details about the ASC scheme and the simulation re-
sults (Sec. II), including a discussion about the various initial configurations we used for the
ASC algorithm (Sec. III). Moreover, we have improved on the highest tetrahedral packing
density reported in Ref. [27] (i.e., from 0.782 . . . to 0.823 . . .), by exploring a broad range of
dynamical parameters for the algorithm and initial configurations. Certain pair statistics of
the densest known packing of tetrahedra (e.g., the contact number, the centroidal correla-
tion function and the face-normal correlation function) are given (Sec. III). It is noteworthy
that the densest tetrahedral packing is a non-Bravais structure with a complex periodic cell
and possesses no long-range order.
   The initial configurations for the icosahedral, dodecahedral and octahedral packings are
described and the numerical challenges in producing dense packings of such polyhedral
particles are discussed (Sec. III). In addition, a detailed derivation of the upper bound and
tables containing the geometrical characteristics of the Platonic and Archimedean solids as
well as their upper bound values are given (Sec. IV). The upper bound is also applied
to superballs and ellipsoids (which was not done in Ref. [27]). Moreover, we provide the
major elements of a possible proof of our conjecture (Sec. V). We also discuss how our
conjecture could be generalized to other centrally symmetric polyhedral particles such as
prisms and anti-prisms as well as high-dimensional analogs of the Platonic solids. Our
work also naturally leads to another conjecture reported here for the first time, namely, the
optimal packing of any convex, congruent polyhedron without central symmetry is generally
not a (Bravais) lattice packing (Sec. V).
   Furthermore, we discuss the possible applications and generalizations of the ASC scheme
to predict the crystal structures of polyhedral nanoparticles and to the study of random
packings of hard polyhedra. Finally, we collect in appendices basic packing characteristics
of various optimal lattice and non-lattice packings of polyhedra (including lattice vectors)
that have been scattered throughout the literature and provide lattice vectors and other
characteristics of the densest known packings of tetrahedra (obtained here) and truncated
tetrahedra.



                                                9
II.     ADAPTIVE SHRINKING CELL (ASC) OPTIMIZATION SCHEME


      We formulate the problem of generating dense packings of nonoverlapping, non-tiling
polyhedra within a fundamental cell in R3 subject to periodic boundary conditions as an
optimization problem. In particular, the objective function is taken to be the negative of the
packing density φ. Starting from an initial unsaturated packing configuration of particles of
fixed size in the fundamental cell, the positions and orientations of the polyhedra are design
variables for the optimization. Importantly, we also allow the boundary of the fundamental
cell to deform macroscopically as well as compress or expand (while keeping the particles
fixed in size) such that there is a net compression (increase of the density of the packing) in
the final state [29]. Thus, the deformation and compression/expansion of the cell boundary,
which we call the adaptive fundamental cell, are also design variables. We are not aware of
any packing algorithm that employs both a sequential search of the configurational space
of the particles and the space of lattices via an adaptive fundamental cell that shrinks
on average to obtain dense packings. We will call this optimization scheme the Adaptive
Shrinking Cell (ASC).
      We will see that the ASC optimization scheme allows for some desired collective motions
of the particles to find the optimal lattice for the periodic cell. This is to be contrasted with
previous treatments that use a fixed shape for the fundamental cell, which may or may not
be the optimal shape. Figure 4 illustrates a simple sequence of configuration changes for a
four-particle system (which is explained in more detail in Sec. II.A). By efficiently exploring
the design-variable space (DVS), which consists of the particle configurational space as well
as the space of lattices via an adaptive fundamental cell, the ASC scheme enables one to
find a point in the DVS in the neighborhood of the starting point that has a higher packing
density than the initial density. The process is continued until the deepest minimum of the
objective function (a maximum of packing density) is obtained, which could be either a local
or global optimum, depending on the particle shapes.
      The ASC optimization problem could be solved using various techniques, depending on
the shapes of the particles. For example, for spheres, one can linearize the objective function
and the constraints, and we have found that linear programming techniques can efficiently
produce optimal solutions for such ASC problems [30]. However, for hard polyhedra the
non-overlapping conditions given by the separation axis theorem (discussed in detail below)


                                              10
               (a)                             (b)                              (c)


FIG. 4: (color online). Sequential changes of the packing configuration due to the design vari-
ables in the ASC algorithm. (a) An initial configuration of four particles. (b) A trial move of a
randomly selected particle that is rejected because it overlaps another particle. (c) A trial move
that is accepted, which results in a deformation and compression (small in magnitude) changing
the fundamental cell shape and size as well as the relative distances between the particles. The
large fundamental cell is divided into smaller sub-cells in order to implement the “cell method”
discussed in Sec. II.D.

involve at least quartic inequalities, which makes it inefficient to solve even using nonlinear
programming methods.
   Here, for polyhedral particles, we solve the ASC optimization problem using a stochastic
procedure, i.e., Monte Carlo (MC) method with a Metropolis acceptance rule for trial moves
to search the DVS efficiently. However, it is important to distinguish our procedure that
incorporates deformation and compression/expansion of the fundamental cell (i.e., the space
of lattices) as design variables from previous MC hard-particle packing algorithms [31]. In
standard MC simulations, arbitrarily selected individual particle is given random displace-
ment or rotation. This sequential movement method is not able to account for any collective
motions of the particles, which is crucial to increasing the packing density, as pointed out in
Sec. I. In our procedure, the deformation/compression/expansion of the boundary at least
in part allows for collective particle motions in a direction leading to higher packing den-
sity. Moreover, it is the overall compression of the fundamental cell that causes the packing
density to increase, not the growth of the particles as in most MD and MC hard-particle


                                              11
packing algorithms [25, 26, 31].
   At first glance, one might surmise that an algorithm that employs particle growth with
an adaptive non-shrinking fundamental cell is equivalent to our choice of fixing the particle
size while allowing the cell to shrink on average. The former is computationally less efficient
than the latter for polyhedral particles. Specifically, growth of polyhedral particles requires
manipulating the coordinates of the vertices of each particle, and thus involves at least dNnv
numerical operations, where d is the spatial dimension, N is the total number of particles in
the system and nv is the number of vertices per particle. It is much more computationally
expensive to use growing/shrinking particles as trial moves for the optimization scheme,
especially when the number of particles is large, compared to our adaptive fundamental cell
approach, which only requires manipulating d(d + 1)/2 strain components.
   In the ASC scheme, the macroscopic deformation and compression/expansion of the fun-
damental cell of the lattice is completely specified by a strain tensor. Since we only consider
small deformations, linear strain analysis can be applied here. Starting from an initial con-
figuration, a trial configuration can be generated by moving (translating and rotating) a ran-
domly chosen particle or by a random macroscopic deformation and compression/expansion
of the fundamental cell. If any two particles overlap, the trial configuration is rejected;
otherwise, if the fundamental cell shrinks in size (which makes the density φ higher), the
trial configuration is accepted. On the other hand, if the cell expands in size, the trial
configuration is accepted with a specified probability pacc , which decreases as φ increases
and approaches zero when the jamming limit [32] (i.e., locally maximal dense packing) is
reached. In particular, we find pacc , with an initial value pacc ∼ 0.35, decreasing as a power
law with exponent equal to -1 works well for most systems that we studied. The particle
motion is equally likely to be a translation or a rotation. The ratio of the number of particle
motions to the number of boundary trial moves should be greater than unity (especially
towards the end of the simulation), since compressing a dense packing could result in many
overlaps between the particles. Depending on the initial density, the magnitudes of the
particle motions and strain components (e.g., the dynamical parameters) need to be chosen
carefully to avoid the system getting stuck in some shallow local minimum. The parame-
ters should also be adjusted accordingly as the packing density increases, especially towards
the jamming point. The number of total Monte-Carlo moves per particle is of the order of
5 × 106 .

                                             12
   In the ensuing subsections, we describe in detail how we implement particle motions as
well as the deformation and compression/expansion of the fundamental cell, and precise
check for interparticle overlaps using the separation axis theorem [33]. We also discuss the
cell method and nearest-neighbor lists that are employed to speed up the simulations.


   A.    Particle Motions


   The fact that a polyhedron is the convex hull of its vertices makes the set of vertices a
useful geometrical representation of a such particle. It is convenient to choose the origin
of the local coordinate system for the vertices to be the centroid of the polyhedron. Other
important geometrical properties of the polyhedron, such as its faces and edges, can be
represented as certain subsets of the vertices.
   Let the Euclidean position of the centroid of the jth particle be xE
                                                                      j (j = 1, .., N). A

translational motion of the particle centroid can be obtained by generating a randomly
                                                  −4
oriented displacement ∆xE
                        j with small magnitude (10   − 10−6 of the characteristic length
of the particle), i.e.,
                                       x̄E    E     E
                                         j = xj + ∆xj .                                     (4)

A rotational motion can be generated by rotating the particle (all of its vertices) along a
randomly chosen axis (passing through its centroid) by a random small angle θ. Let the
vector vi originating at the centroid denote the vertex i. We have

                                                        k
                                      v̄i = R · vi⊥ + vi ,                                  (5)

                  k
where vi⊥ and vi are the components of vi perpendicular and parallel to the rotation axis,
respectively, and R is the rotation matrix, i.e.,
                                                       
                                        cos θ − sin θ 0
                                                       
                                  R =  sin θ cos θ 0  .                                   (6)
                                                       
                                                       
                                          0       0   1

If this motion does not result in the overlap with another particle, the trial move is accepted;
otherwise it is rejected.




                                             13
   B.    Adaptive Fundamental Cell


   For a lattice-based periodic packing, the fundamental cell is specified by the lattice vectors
ai (i = 1, 2, 3). Recall that the Euclidean coordinates of the particle centroids are xE
                                                                                       j

(j = 1, .., N). The relative coordinates of the centroids with respect to the lattice vectors
are given by
                                         xE        L
                                          j = Γ · xj ,                                       (7)

where Γ = [a1 , a2 , a3 ].
   The adaptive fundamental cell allows for a small strain of the fundamental cell, including
both volume and shape changes, which is represented by a symmetric strain tensor ε, i.e.,

                                          ∆Γ = ε · Γ,                                        (8)

where                                                   
                                          ǫ   ǫ   ǫ
                                         11 12 13 
                                    ε =  ǫ21 ǫ22 ǫ23  ,                                    (9)
                                                     
                                                     
                                          ǫ31 ǫ32 ǫ33
and the new fundamental cell (lattice vectors) are given by

                                         Γ̄ = Γ + ∆Γ.                                       (10)

Substituting the above equation into Eq. (4), we have

                                 x̄E         L    E         L
                                   j = Γ̄ · xj = xj + ∆Γ · xj .                             (11)

   Thus, the strain of the fundamental cell corresponds to non-trivial collective motions of
the particle centroids (see Fig. 4). In general, the translational motions of the particles con-
tain the contributions from a random independent part (given by Eq. (4)) and the collective
motion imposed by the adaptive fundamental cell. It is this collective motion that enables
the algorithm to explore the configuration space more efficiently and to produce highly dense
packings.


   C.    Checking Overlaps and the Separation Axis Theorem


   Hard polyhedron particles, unlike spheres, ellipsoids and superballs, do not possess simple
overlap potential functions. Thus, the check of overlapping for such particles requires other

                                              14
techniques. Two convex objects are separated in space if and only if there exist an axis, on
which the line segments defined by projections of the two objects do not overlap (see Fig. 5).
This statement is usually referred to as the separation axis theorem (SAT) [33].




     FIG. 5: (color online). Two nonoverlapping particles and one of their separation axes.


   For convex polyhedra, the above theorem has a simpler version. Since a polyhedron
is completely defined by its vertices, the line segment on the axis is defined by the most
separated two projections of the vertices. Moreover, the axis is either perpendicular to one
of the faces or perpendicular to a pair of edges, one from each polyhedron. This reduces the
number of axes that need to be checked from infinity to [E(E − 1)/2 + 2F ], where E and F
is the number of edges and faces of the polyhedron, respectively. Here we employ the SAT
to check for interparticle overlaps numerically up to the highest machine precision.
   For polyhedra whose circumscribed and inscribed spheres are well defined, two particles
are guaranteed to overlap if the centroidal separation is smaller than the inscribed diameter
and guaranteed not to overlap if the centroidal separation is larger than the circumscribed
diameter. This pre-check dramatically speeds up the simulations starting from configurations
with low densities.


   D.   Cell Method and Near-Neighbor List


   The well-developed cell method [25, 26] for particle-system simulation is used here to
speed up the process. However, the simulation box (fundamental cell) will not remain a

                                             15
FIG. 6: (color online). The particles (black) in the central fundamental cell (with red bound-
ary) and their images (gray). The distances between the particles in the central cell and all the
corresponding images need to be checked.


cube during the simulation and several conventional techniques developed for cubic box
need modifications. In particular, to obtain the minimum image distances, all surrounding
boxes need to be checked explicitly (see Fig. 6). With the help of the relative-coordinate
representation of the particle centroids, the separation vector of a pair of particles is given
by
                                    dS = Γ · (xLi − xLj + L),                               (12)

where L is a vector with the values of components to be 1, 0 or -1. Note L can also be
considered as the index of the box that the image particle is in.
     The cells are taken to be the same shapes as the simulation box. Partitions of the particle
centroids into the cells are also convenient for relative coordinate representations, i.e., the
index of the cell (represented by a vector) C for particle i is given by

                                           C = [NC xLi ],                                   (13)

where [X] gives the smallest integer part of X and NC is the number of cells. Note that
the boundary deformations and rotations of particles do not affect the cells in which the
particles are situated; only translations may cause transitions between the different cells.

                                               16
   For dense packings, we make use of a near-neighbor list (NNL) to further improve the
efficiency of the algorithm [25, 26]. In particular, when the packing density is high, each
particle is “trapped” in a “cage” formed by its near neighbors. These near-neighbor config-
urations are practically stationary, i.e., the particles undergo very small “jiggling” motions.
Thus, to check for overlapping between the particles, one only needs to consider a particles
nearest neighbors. If a large magnitude translation is made, the NNL needs to be set up
again.


III.     APPLICATION OF THE ASC SCHEME TO THE PLATONIC SOLIDS AND
RESULTS


   Here we apply the ASC scheme to obtain the densest known packings of the non-tiling
Platonic solids. Due to its lack of central symmetry, the tetrahedron presents the greatest
challenge for the numerical solution procedure of the ASC scheme because of its tendency
to get stuck in local (density) minima, which is a consequence of the associated “rugged”
energy or, more precisely, “density” landscape (e.g., the packing density as function of the
centroidal positions and orientations of all of the particles in the fundamental cell). Hence,
the choice of initial configurations becomes crucial in getting dense tetrahedral packings. By
contrast, the central symmetry of the octahedron, dodecahedron and icosahedron results in
density landscapes for the numerical procedure that are appreciably less rugged than that
for tetrahedral packings.


   A.     Tetrahedra


   The determination of the densest packings of regular tetrahedra is part of the 18th prob-
lem of Hilbert’s famous set of problems. It is of interest to note that the densest (Bravais)
lattice packing of tetrahedra (which requires all of the tetrahedra to have the same orienta-
tions) has the relatively low density φLmax = 18/49 = 0.367 . . . and each tetrahedron touches
14 others [34]. Recently, Conway and Torquato showed that the densest packings of regular
tetrahedra must not be a Bravais lattice packings, and found packings with density as large
as φ ≈ 0.72 [13]. One such packing is based upon the filling of “imaginary” icosahedra with
the densest arrangement of 20 tetrahedra and then employing the densest lattice packing


                                             17
of icosahedra. A slightly higher density was achieved by a perturbation of the so-called
“Welsh” packings with density φ = 17/24 ≈ 0.708 [13]. Using “tetrahedral” dice, Chaikin
et al. [14] experimentally generated jammed disordered packings of such dice with φ ≈ 0.75.
Even though the dice are not perfect tetrahedra (because the vertices and edges are slightly
rounded), these experimental results suggested that the densest packings of tetrahedra could
exceed the highest densities reported by Conway and Torquato. Indeed, Chen [15] has re-
cently discovered a periodic packing of tetrahedra with φ = 0.7786 . . . [35]. We will call
this the “wagon-wheels” packing because the basic subunits consist of two orthogonally in-
tersecting “wagon” wheels. A “wagon wheel” consists of five contacting tetrahedra packed
around a common edge (see Fig. 1a of Ref. 13).

TABLE I: Some packing characteristics of certain known tetrahedral packings. Here φ is the
packing density, N is the number of particles in the fundamental cell, and Z̄ is the average contact
number per particle.

                     Name                   φ            Locally Jammed     N      Z̄

             Optimal Lattice [34]   18/49 ≈ 0.367346           Yes           1    14
                 Uniform [13]        2/3 ≈ 0.666666            Yes           2    10
                  Welsh [13]        17/24 ≈ 0.708333            No          34   25.9
                Icosahedral [13]         0.716559               No          20   20.6
              Wagon Wheels [15]          0.778615              Yes          18    7.1




   1.   Initial Conditions


   Because we will use all of the aforementioned tetrahedral packing arrangements as ini-
tial conditions in our numerical solution procedure for the ASC optimization problem, we
describe them now in a bit more detail. Table I summarizes some of their packing charac-
teristics, including the packing density φ, the number of particles N in the fundamental cell,
the average number of contacting particles per particle Z̄, and whether the packing is locally
jammed. A packing is locally jammed if each particle is locally trapped by its neighbors,
i.e., it cannot be translated or rotated while fixing the positions and orientations of all the
other particles [32, 36].


                                                18
   In the optimal lattice packing, each tetrahedron touches 14 others via edges and vertices.
In the uniform packing, the tetrahedra are “locked” in a planer layer, and each particle
has eight in-plane partial face-to-face contacts and two edge-to-edge contacts (contributed
by the two layers above and below), and therefore each particle contacts 10 others. In the
icosahedral packing, the tetrahedra have a greater degree of freedom to move, and indeed it
is not locally jammed. The 20 tetrahedra inside the imaginary icosahedron are required to
meet at its centroid, and so each tetrahedron has 20 vertex-to-vertex contacts. Placing the
imaginary icosahedra on the sites of its optimal lattice results in a tetrahedral packing with 12
partial face-to-face contacts. Thus, there are 8 tetrahedra that have 20 contacts per particle
and 12 tetrahedra with 21 contacts per particle, and therefore Z̄ = (8 × 20 + 12 × 21)/20 =
20.6.
   The Welsh packing is based on the “primitive Welsh” tessellation of R3 into truncated
large tetrahedra and small regular tetrahedra [13]. Interestingly, the “primitive Welsh” con-
figuration is closely related to the uniform packing, i.e., it can be constructed by replicating
a periodic packing with two truncated large tetrahedra and two small regular tetrahedra
in the fundamental cell. Each truncated large tetrahedron can be divided into 12 “Welsh
lows”, and 4 “Welsh medials,” following the notation in Ref. 13. The Welsh medials and
Welsh lows are tetrahedra with lower symmetry than regular tetrahedra, which are referred
to as the “Welsh highs.” To construct the Welsh packing, we insert Welsh highs (regular
tetrahedra) into the Welsh low and medial regions. We will refer to the regular tetrahedra
that are placed in the Welsh low, medial and high regions as lows, medials and highs, re-
spectively. In the Welsh packing, each high makes 4 face-to-face contacts with 4 medials.
Each medial contacts 24 lows and 3 other medials at the centroid of the large truncated
tetrahedron; moreover, each medial makes a face-to-face contact with one high. Thus, each
medial has 28 contacts. Each low contacts 23 other lows and 4 medials at the centroid of
the large truncated tetrahedron. Thus, in total each low has 27 contacts. Each truncated
large tetrahedron has 12 lows and 4 medials. Thus, the number of basis particles in the
fundamental cell N = 34 and Z̄ = (12 × 27 + 4 × 28 + 1 × 4)/17 = 440/17 = 25.882352 . . ..
   In the fundamental cell of the wagon-wheels packing, there are N = 18 particles, forming
two clusters, each of which includes two ”wheels” entangled orthogonally to each other.
Each cluster has a central connection particle, an “upper” wheel and a “lower” wheel.
The central particle contacts the other 8 tetrahedra through two of its edges. Each of

                                              19
the other 8 tetrahedra has 4 edge contacts with particles in its own cluster and 3 partial
face-to-face contacts with particles from other clusters. Thus the average contact number
Z̄ = (1 × 8 + 8 × 7)/9 = 64/9 = 7.111111 . . .. The coordinates of all of the 18 tetrahedra in
the fundamental cell can be found on the authors’ website [37].


   2.   Dense Packings


   We employ our algorithm to obtain dense packings of tetrahedra using initial configu-
rations that are based upon the known packings given in Table I as well as certain dilute
packings with carefully chosen fundamental cells and the number of particles. Note that
these dilute packings were not used as initial configurations to obtain the results reported
in Ref. [27]. A range of initial densities is used to yield the largest possible densities in the
final states, as summarized in Table II.
   For initial conditions using the known packings in Table I, the fundamental cell is isotropi-
cally expanded with the relative coordinates of the tetrahedra fixed so that the initial packing
is locally unjammed with a lower density φint . The highest density of 0.782 obtained from
this subset of initial conditions started from the “wagon-wheels” packing, which was the
value reported in Ref. [27].
   For the aforementioned dilute packings, a variety of fundamental cell shapes spanning
from that for the simple cubic lattice to that of the hexagonal close packing as well as a
wide range of particle numbers spanning from 70 to 350 are explored to generate the dense
packings. Specifically, the densest known tetrahedral packing is obtained from a dilute initial
packing with a rhombical fundamental cell similar to that of the hexagonal close packing
and 314 particles (see Table II). The particles are originally placed in the fundamental cell
randomly and then the system is sufficiently equilibrated with the fundamental cell fixed.
The final packing configuration has a density of about 0.823 and is shown in Fig. 7 from
two different viewpoints. The optimized lattice vectors for the densest packing and other
characteristics are given in Appendix B. We see that the packing lacks long-range order
and is composed of “’clusters” of distorted wagon wheels and individual tetrahedra. Thus,
we call this dense arrangement the “disordered wagon wheels” packing. We will comment
further about the significance of achieving this remarkably high density with a disordered
packing in the Discussion and Conclusions (Sec. V).


                                              20
TABLE II: Dense tetrahedral packings generated from our algorithm using initial configurations
based upon the packings given Table I and the dilute packing as described in the text. Here φint
is the initial packing density, φ is the final packing density, N is the number of tetrahedra in the
fundamental cell [38], and Z̄ is the average contact number per particle.

             Initial Packing             φint           φ       Locally Jammed     N     Z̄

            Optimal Lattice           0.25 − 0.3     0.695407         Yes          27    6.6
                 Uniform             0.45 − 0.55     0.665384         Yes          54    9.8
                  Welsh               0.45 − 0.6     0.752092         Yes          34    7.4
                Icosahedral           0.45 − 0.6     0.744532         Yes          20    7.1
             Wagon Wheels            0.55 − 0.65     0.782021         Yes          72    7.6
        Disordered Wagon Wheels      0.005 − 0.01    0.822637         Yes         314    7.4




                               (a)                                  (b)


FIG. 7: The densest known packing of tetrahedra with 314 particles in the fundamental cell. We
call this the ”disordered wagon-wheels” packing. (a) Viewed from the side. (b) Viewed from the
top. It is apparent that the packing lacks long-range order and consists of “clusters” of distorted
wagon wheels.


   3.   Statistics of the Densest Tetrahedral Packing


   Contact Numbers: The contact numbers of the densest tetrahedral packing as well as
those obtained using the other five initial configurations (Table I) are given in Table II. To
determine contacting neighbors, it is crucial to find the interparticle gaps first. In particular,


                                                21
each of the equilateral triangular faces of the tetrahedra is discretized into M equal-sized
smaller triangles and the distances between the vertices of the small triangles of the neigh-
boring tetrahedra are computed, the minimum of which is used as the gap value between
the two corresponding tetrahedra. For our packings, when M > 200, the values of interpar-
ticle gaps obtained by this approximation scheme become stable and converge to the true
gap values. Like any packing generated via computer simulations, the particles never form
perfect contacts and hence contacting neighbors must be determined by setting a tolerance
T for the interparticle gaps. Here we choose T to be equal to the mean value of the gaps
(of order 10−2 to 10−3 of the edge length) such that any gap less than T is associated with
a contact. This procedure yields the contact numbers given in Table II. In particular, we
find that in the disordered wagon wheels packing, there are approximately 6.3 face-to-face
or partial face-to-face contacts and 1.1 edge-to-edge contacts.
   Face-Normal Correlation Function: An important statistical descriptor for packings of
non-spherical particles is the particle orientation correlation function, which measures the
extent to which a particle’s orientation affects the orientation of another particle at a different
position. For highly symmetric particle shapes, it is reasonable to focus on those pair
configurations in which the particles are in the same orientation, since particle alignment
is associated with dense configurations and phase transitions that may occur. However,
because tetrahedra lack central symmetry, we found that face-to-face contacts are favored
by the dense packings, instead of face-to-vertex contacts, which are necessarily associated
with aligning tetrahedral configurations, such as in the case of the optimal lattice packing.
                                          1

                                        0.8

                                        0.6
                               CFN(r)




                                        0.4

                                        0.2

                                          0

                                        -0.2
                                           0   1           2       3   4
                                                        r/(2rin)




FIG. 8: The face-normal correlation function CF N (r) of the densest known packing of tetrahedra
obtained here, where rin is the radius of the insphere of a tetrahedron.


                                                   22
   Thus, because our interest is in dense tetrahedral packings, we determine the “face-
normal” correlation function CF N (r), which we define as the average of the largest negative
value of the inner product of two face normals of a pair of tetrahedra separated by a distance
r. This quantity is plotted in Fig. 8. The strong positive peak values, ranging from r =
           √
2rin = d0 / 6 (where rin is the radius of the insphere of the tetrahedron and d0 is the
edge length of the particle) to r slightly greater than 2rin , indicate a large number of face-
to-face contacts between neighboring particles, implying strong short-range orientational
correlations. The fact that CF N (r) plateaus to its maximum or near maximum value, for
the distance interval r/(2rin ) ∈ (1, 2.2), indicates that there are partial face-to-face contacts
in which particles slide relative to one another such that the distance between the centroids
can increase while the face-normal inner product remains the same. The “valleys” of CF N (r)
with relatively small magnitudes are manifestations of weak particle alignments (alignment
in the same direction), which are local configurations that are necessary “costs” to achieve
the largest face-to-face contact numbers on average.
   Centroidal Radial Distribution Function: Another statistical descriptor of the structure
is the centroidal radial distribution function g2 (r). In particular, g2 (r)r 2 dr is proportional
to the conditional probability that a particle centroid is found in a spherical shell with
thickness dr at a radial distance r from another particle centroid at the origin. It is well
established that when there is no long-range order in the system, g2 decays to unity very fast.
Figure 9 shows the centroidal radial distribution of the densest known tetrahedral packing.
We see that g2 (r) decays to unity after a few oscillations, indicating that the packing lacks
long-range order.


   B.   Octahedra


   To obtain dense packings of octahedra, we use a wide range of initial configurations. This
includes unsaturated packings in which the particles are randomly oriented and positioned
with densities spanning the range from 0.2 to 0.35 as well as unsaturated simple cubic (SC)
and face-centered cubic (FCC) lattice packings with densities from 0.1 to 0.125, and the
optimal lattice packings with densities from 0.3 to 0.55 are used. We found that, using small
compression rates for the random initial configurations and moderate compression rates for
the various lattice configurations along with a sufficient number of particle displacements


                                              23
                                        6

                                        5

                                        4




                                g2(r)
                                        3

                                        2

                                        1

                                        0
                                         0   1        2      3      4
                                                  r/(2rin)




FIG. 9: The centroidal radial distribution function g2 (r) of the densest known packing of tetrahedra,
where rin is the radius of the insphere of a tetrahedron.


and rotations, resulted in final configurations with densities larger than 0.93 that are very
close in structure and density to the optimal lattice packing. More specifically, starting
from the unsaturated SC lattice (with density 0.1) and optimal lattice (with density 0.55)
packings, final packings with densities very slightly larger than the value 0.947003 . . . can be
obtained, which are extremely close in structure and density to the optimal lattice packing
(φLmax = 0.947368 . . .) [22]. A previous study involving an event-driven molecular dynamics
growth algorithm for the case of octahedral-like superballs led to the same the densest lattice
packing, which lends further credence to the fact that this lattice is indeed optimal among all
packings [17]. Each octahedron in the optimal lattice packing, depicted in Fig. 10, contacts
14 others and its lattice vectors are given in Appendix A.




                 FIG. 10: A portion of the optimal lattice packing of octahedra.



                                                 24
   C.   Icosahedra


   As in the case of octahedra, we use a variety of initial conditions to get dense packings
of icosahedra. This includes unsaturated packings in which the icosahedra are randomly
oriented and positioned with densities spanning the range from 0.2 to 0.3 as well as various
unsaturated lattice packings, such as the BCC, FCC and the densest lattice packing, with
densities spanning the range from 0.3 to 0.65. We found that by starting from a low-density
configuration, with a small enough compression rate and sufficient number of particle moves,
one can always obtain a final configuration that is very close to the optimal lattice packing
with a density φ ≈ 0.83. An initial configuration of an unsaturated optimal lattice packing
configuration with a density 0.65 gives a final packing with density 0.836315 . . ., which is
extremely close in structure and density to the optimal lattice packing (φLmax = 0.836357 . . .)
[23]. Each icosahedron of the optimal lattice packing, depicted in Fig. 11, contacts 12 others
and its lattice vectors are given in Appendix A.




                FIG. 11: A portion of the optimal lattice packing of icosahedra.




   D.   Dodecahedra


   Unsaturated random packings with densities ranging from 0.15 to 0.3 as well as unsatu-
rated simple cubic and the optimal lattice packings with densities spanning the range from
0.3 to 0.6 are employed as initial configurations to generate dense packings of dodecahedra.
We found that it is algorithmically more difficult to avoid local density maxima for dodecahe-
dra than octahedron and icosahedron packings discussed above. For example, starting from


                                             25
random configurations, even with sufficiently small compression rate and a large number of
particle moves, we can only achieve apparently jammed final packings with densities in the
range from 0.83 to 0.85. When we use an unsaturated optimal lattice packing with density
0.72 as an initial condition, we can generate a final packing with φ = 0.904002 . . ., which is
relatively close in structure and density to the optimal lattice packing (φLmax = 0.904508 . . .)
[23]. Each dodecahedron of the optimal lattice packing, depicted in Fig. 12, contacts 12
others and its lattice vectors are given in Appendix A.




               FIG. 12: A portion of the optimal lattice packing of dodecahedra.


   We note that the tendency for dodecahedral packings to get stuck in local-density maxima
in our algorithm is due to the fact that in some sense the dodecahedron is a shape that is
intermediate between the octahedron and icosahedron. Specifically, for octahedral packings,
the octahedral symmetry of the particles facilitates the formation of nematic phases at
relatively high densities, which can then be easily compressed into a dense crystalline phase
with adaptive fundamental cells. An icosahedron is highly isotropic and possesses a large
number of faces. Thus, at low densities, the icosahderal packing behaves like a hard-sphere
fluid, and it is only near the jamming point that the asphericity of the icosahedron begins
to play an important role. Again, by allowing the fundamental cell to adapt in the case of
icosahedra, the optimal lattice that best accommodates the packing can be easily identified.
However, for our algorithm, the dodecahedral packing behaves differently from either the
octahedral or icosahedral packings. In particular, while dodecahedra are more isotropic
than octahedra, which strongly suppresses the formation of nematic phases, they have fewer
but larger faces than icosahedra, which favors the formation of face-to-face contacts that

                                              26
ends up jamming the dodecahedral packing at lower densities than either the octahedral or
icosahedral packings.


IV.   UPPER BOUND ON THE MAXIMAL DENSITY OF PACKINGS OF NON-
SPHERICAL PARTICLES


   Here we derive a simple upper bound on the maximal density φmax of a packing of
congruent nonspherical particles of volume vp in any Euclidean space dimension d. We will
see that this bound will aid in our analysis of the optimality of not only the Platonic and
Archimedean solids but also superballs. Let φSmax be the maximal density of a d-dimensional
packing of congruent spheres and let vs represent the volume of the largest sphere than can
be inscribed in the nonspherical particle.
Lemma: The maximal density of a packing of congruent nonspherical particles is bounded
from above according to the following bound [39]:
                                                    
                                              vp S
                                 φmax ≤ min     φ ,1 ,                                     (14)
                                              vs max
where min[x, y] denotes the minimum of x and y.
   The proof is straightforward. The maximal packing density φmax can be expressed in
terms of the maximal number density ρmax via the relation

                                          φmax = ρmax vp .                                 (15)

If we inscribe within each nonspherical particle of the packing the largest possible sphere, it
is clear that
                                          ρmax vs ≤ φSmax ,                                (16)

and therefore combination of the last two equations yields the upper bound of the Lemma.
Remark: The upper bound (14) will yield a reasonably tight bound for packings of non-
spherical particles provided that the asphericity γ of the particle is not large. Here we define
the asphericity as the following ratio:
                                                    rout
                                             γ=                                            (17)
                                                    rin
where rout and rin are the circumradius and inradius of the circumsphere and insphere of the
nonspherical particle. The circumsphere is the smallest sphere containing the particle. The

                                               27
insphere is the largest sphere than can be inscribed in the particle. For a sphere, clearly the
asphericity γ = 1. Since upper bound (14) cannot be sharp (i.e., exact) for a nonspherical
particle, any packing construction for a nonspherical particle whose density is close to the
upper bound (14) is nearly optimal, if not optimal.
   In the three-dimensional case, the upper bound (14) becomes
                                                          
                                      U           vp π
                             φmax ≤ φmax = min      √ ,1 .                                (18)
                                                  vs 18

We now apply this upper bound to packings of the Platonic and Archimedean solids and
compare the bounds to the densities of the corresponding densest lattice packings. Moreover,
we apply the upper bounds to superball and ellipsoid packings.


   A.   Platonic Solids


   Table III compares the density of the densest lattice packings of the Platonic solids to the
corresponding upper bounds on the maximal density for such packings. The large asphericity
and lack of central symmetry of the tetrahedron is consistent with the large gap between the
upper bound density and densest lattice packing density, and the fact that there are non-
lattice packings with density appreciably greater than φLmax . On the other hand, the central
symmetry of the octahedron, dodecahedron and icosahedron and their associated relatively
small asphericities explain the corresponding small differences between φLmax and φUmax and
is consistent with our simulation findings that indicate that their optimal arrangements are
their respective densest lattice packings.


   B.   Archimedean Solids


   We also compute the upper bound (18) for each of the 13 Archimedean solids and compare
them to the densities of the corresponding densest lattice packings [23, 34]. (In Appendix
A we provide the lattice vectors for the optimal lattice packings of the Archimedean solids).
Table IV summarizes the upper bounds on the maximal density for such packings. Not
surprisingly, the truncated tetrahedron (the only Archimedean solid that is not centrally
symmetric) has a large asphericity, implying that there are denser non-lattice packings, as
we explicitly identify in Section V. The central symmetry of the majority of the Platonic


                                             28
TABLE III: Comparison of the densities of the densest lattice packings for the Platonic solids
[22, 23, 34] to the corresponding upper-bound densities as obtained from (18). Here vp is volume
of the polyhedron with unit edge length, rin and rout are the radii of the insphere and circumsphere
of the polyhedron with unit edge length, respectively, γ = rout /rin is the asphericity, φL
                                                                                          max is the

density of the optimal lattice packing and φU
                                            max is the upper bound (18). The numerical values are

reported up to the sixth decimal place. The naming code used here is the same one used in Fig. 1.

              Name              vp         rin            rout         γ     φL
                                                                              max      φU
                                                                                        max
                                √           √             √
                                  2          6              6
        Tetrahedron (P1)        12         12              4           3    0.367346    1
                                  √      √ √          √     √
                             5(3+ 5)    3 3+ 15        10+2 5
         Icosahedron (P2)       12                               1.258410 0.836357 0.893417
                                   √   √ 12 √         √ √
                                                         4
                             15+7 5     250+110 5      3+ 15
        Dodecahedron (P3)        4         20            4       1.258410 0.904508 0.981162
                                √          √            √
                                  2          6            2
         Octahedron (P4)         3         6             2       1.732050 0.947368      1
                                                        √
                                            1             3
            Cube (P5)           1           2            2       1.732050      1        1


and Archimedean solids and their associated relatively small asphericities explain the cor-
responding small differences between φLmax and φUmax and is consistent with our simulation
findings that strongly indicate that their optimal arrangements are their respective densest
lattice packings.


   C.   Superballs


   The upper bound (18) in the case of superballs [17] can be expressed analytically for
all values of the deformation parameter p. A three-dimensional superball is a centrally
symmetric body in R3 occupying the region

                                    |x1 |2p + |x2 |2p + |x3 |2p ≤ 1,                           (19)

where xi (i = 1, 2, 3) are Cartesian coordinates and p ≥ 0 is the deformation parameter,
which indicates to what extent the particle shape has deformed from that of a sphere (p = 1).
A superball can possess two types of shape anisotropy: cubic-like shapes for 1 ≤ p ≤ ∞, with
p = ∞ corresponding to the perfect cube, and octahedral-like shapes for 0 ≤ p ≤ 1, with
p = 1/2 corresponding to the perfect regular octahedron. In Ref. 17, event-driven molecular
dynamics growth algorithms as well as theoretical arguments led to the conjecture that


                                                 29
TABLE IV: Comparison of the densities of the densest lattice packings for the Archimedean solids
to the corresponding upper-bound densities as obtained from (18). Except for the cubeoctahedron
[34], the densities of the densest lattice packings were obtained by Betke and Henk [23]. Here vp
is volume of the polyhedron with unit edge length, rin and rout are the radii of the insphere and
circumsphere of the polyhedron with unit edge length, respectively, γ = rout /rin is the asphericity,
φL                                                       U
 max is the density of the optimal lattice packing, φmax is the upper bound (18) and t = [1 +
       √ 1             √ 1
(19 − 3 33) 3 + (19 + 3 33) 3 ]/3 ≈ 1.83929 . . . is the Tribonacci constant. The numerical values
are reported up to the sixth decimal place. The naming code used here is the same one used in
Fig. 3.

                 Name                         vp               rin           rout         γ        φL
                                                                                                    max     φU
                                                                                                             max
                                               √               √             √
                                             23 2                6               22
   Truncated Tetrahedron (A1)                 12                4                4     1.914854 0.680921      1
                                                 √        √        √     √        √
                                          125+43 5            21+9   5       58+18 5
   Truncated Icosahedron (A2)                  4
                                                                √
                                                               2 2             4     1.092945     0.784987 0.838563
                                         √       √        q              q
                                        3 t−1+4    t+1          t−1            3−t
            Snub Cube (A3)                   √
                                            3 2−t              4(2−t)         4(2−t)   1.175999 0.787699 0.934921

     Snub Dodecahedron (A4)              37.616654
                                            1.980915 2.155837 1.088303 0.788640 0.855474
                                                √      √      √
                                                         31+12 5
 Rhombicicosidodecahedron (A5)           95 + 50 5
                                            3.523154             1.079258 0.804708 0.835964
                                        √              √ 2 √
                                  60+29 5                11+4 5
Truncated Icosidodecahedron (A6)      3     2.016403             1.107392 0.827213 0.897316
                                        √        √     √ 2√
                                  12+10 2     1+ 2        5+2 2
 Truncated Cuboctahedron (A7)         3         2          2     1.158941 0.849373 0.875805
                                        √   q      √        √
                                  45+17 5      5+2 5     1+ 5
     Icosidodecahedron (A8)           6           5              1.175570 0.864720 0.938002
                                         √       √     √ 2 √
                                              1+2 2      13+6 2
   Rhombicuboctahedron (A9)      22 + 14 2                       1.210737 0.875805     1
                                        √   √ 2 √ √ 2 √
                                 5(99+47 5)   25+11  5   74+30 5
 Truncated Dodecahedron (A10)        12
                                                √
                                               2 2         4     1.192598 0.897787 0.973871
                                              √                √
                                             5 2               2
          Cuboctahedron (A11)                 3               2                1       1.414213 0.918367      1
                                                √             √          √       √
                                           21+14 2          1+ 2             7+4 2
      Truncated Cube (A12)                    3               2               2        1.473625 0.973747      1
                                             √               √
                                                               6
                                                                             √
                                                                               10
   Truncated Octahedron (A13)               8 2               2               2        1.290994      1        1


the densest packings of superballs for all convex shapes (1/2 ≤ p ≤ ∞) are certain lattice
packings, depending on the value of the deformation parameter p.
   For convex superballs in the octahedral regime (0.5 < p < 1), the upper bound (18) is
explicitly given by
                                   √                                                 
                                     6        1          1 2p + 1                 1 p+1
                        φUmax =        2
                                         × 3 2p B         ,              B         ,      ,                  (20)
                                  108p                  2p 2p                    2p p



                                                     30
similarly, for superballs in the cubic regime (p > 1), the upper bound (18) is given by
                                  √                             
                           U        2     1 2p + 1         1 p+1
                          φmax = 2 B        ,         B      ,      ,                   (21)
                                  4p      2p 2p           2p p

where B(x, y) = Γ(x)Γ(y)/Γ(x + y) and Γ(x) is the Euler Gamma function. Here and in the
subsequent paragraphs concerning ellipsoids, we only state the nontrivial part of the upper
bound (18). For p near the sphere point (p = 1), the densest lattice packings [17] have
densities that lie relatively close to the corresponding upper-bound values. For example,
for p = 0.99, 0.98 and 0.97, φUmax = 0.745327 . . . , 0.750274 . . ., and 0.755325 . . ., respectively,
which is to be compared to φLmax = 0.740835 . . . , 0.741318 . . ., and 0.741940 . . ., respectively.
For p = 1.01, 1.02 and 1.03, φUmax = 0.747834 . . . , 0.755084 . . ., and 0.762233 . . ., respectively,
which is to be compared to φLmax = 0.741720 . . . , 0.742966 . . ., and 0.744218 . . ., respectively.
   The fact that the constructed densest lattice packings of superballs have density φLmax
relatively close to the upper bound value φUmax strengthens the arguments made in Ref. 17
that suggested that the optimal packings are in fact given by these arrangements. If the
optimal packings around p = 1 are indeed the lattice packings, it would be surprising that
for other values of p a continuous deformation of the superballs would result in a transition
from lattice packings to denser non-lattice packings.


   D.   Ellipsoids


   In the case of ellipsoids in which the the ratio of the three semiaxes are given by 1 : α : β
(α, β ≥ 1), the upper bound (18) becomes

                                                      π
                                          φUmax = αβ √ .                                          (22)
                                                      18
For prolate spheroids β = 1, and the bound becomes

                                                      π
                                           φUmax = α √ .                                          (23)
                                                      18
For oblate spheroids with α = β > 1, the bound is given by

                                                      π
                                          φUmax = α2 √ .                                          (24)
                                                      18
The upper bounds for ellipsoids generally do not work as well as those for the centrally
symmetric Platonic and Archimedean solids, and superballs. This is due to the fact that the

                                                31
three principle directions (axes) are not equivalent for an ellipsoid, i.e., it generally possesses
different semiaxes. Note that the three equivalent principle (orthogonal) axes (directions)
of a centrally symmetric particle are those directions that are two-fold rotational symmetry
axes such that the distances from the particle centroids to the particle surfaces are equal.
In addition, the asphericity of an ellipsoid increases linearly as the largest aspect ratio α
increases without limit. By contrast, the three principle directions are equivalent for the
centrally-symmetric Platonic and Archimedean solids as well as for superballs, for which the
asphericity is always bounded and close to unity (see Tables III and IV). Thus, we see that
an asphericity value close to unity is a necessary condition to have a centrally symmetric
particle in which the three principle directions are equivalent.


V.    DISCUSSION AND CONCLUSIONS


     We have formulated the problem of generating dense packings of nonoverlapping poly-
hedra within an adaptive fundamental cell subject to periodic boundary conditions as an
optimization problem, which we call the Adaptive Shrinking Cell (ASC) scheme. The pro-
cedure allows both a sequential search of the configurational space of the particles and the
space of lattices via an adaptive fundamental cell that shrinks on average to obtain dense
packings. We have applied the ASC to generate the densest known packings of the Platonic
solids.
     For tetrahedra, we find a packing with density φ ≈ 0.823, which is a periodic (non-
Bravais lattice) packing with a complex basis. Unlike the other Platonic solids, finding
dense packings of tetrahedra with our algorithm requires having good initial configurations.
The densest packing was found using 314 particles in a rhombical fundamental cell that
is similar to that of the hexagonal close packing. As we stressed in our earlier work [27]
and continue to confirm in this paper, it is possible that denser packings of tetrahedra will
involve increasingly larger numbers of particles in the fundamental cell. In fact, the higher
density found here is realized by a larger periodic packing (314 particles per cell) than
the one reported in Ref. [27] (72 particles per cell) with density 0.782. It is apparent the
obtained densest known tetrahedral packing is disordered in the sense that it possesses no
long-range order, at least on the scale of the simulation box. This packing can be considered
to be a disordered “mixture” of distorted wagon wheels and individual tetrahedra and it


                                               32
is distinct from the one reported in Ref. [27] in both the arrangement of the wagon wheels
and the extent of the distortion of the wagon wheels. Although we cannot rule out the
possibility of the existence of denser packings involving a more ordered arrangement of
the wagon wheels and individual tetrahedra, it is reasonable to expect that wagon wheels
will be key building blocks in denser packings and should at least be slightly distorted to fill
the interparticle gaps in wagon-wheel clusters more efficiently, which necessarily introduces a
certain degree of disorder to the packing. If denser packings of tetrahedra must involve larger
number of particles without long-range order, than it raises the amazing prospect that the
densest packings of tetrahedra might be truly disordered, due to the geometrical frustration
associated with the lack of central symmetry of a tetrahedron and that tetrahedra cannot
tile space. This would be the first example of a maximally dense packing of congruent convex
three-dimensional particles without long-range order. However, we cannot offer definitive
conclusions about this possibility at this stage. It is clear that in future work in the search
for denser packings, increasingly larger number of tetrahedra must be considered, which can
only be studied using greater computational resources.
   Our simulation results and rigorous upper bounds strongly suggest that the optimal
lattice packings of the centrally symmetric Platonic solids (octahedra, dodecahedra and
icosahedra) are indeed the densest packings of these particles, especially since these arise
from a variety of initial “dilute” multi-particle configurations within the fundamental cell
[40]. It is noteworthy that a different simulation procedure (an event-driven molecular
dynamics growth algorithm with an adaptive fundamental cell) has recently been used to
demonstrate that the densest packings of octahedral-like superballs (which contains the
perfect octahedron) are likely to be the optimal lattice packings [17]. Moreover, the fact that
the optimal lattice packing densities of certain centrally symmetric nonspherical particles,
such as the Archimedean solids with central symmetry and convex superballs, are relatively
close to their upper bounds as well as other theoretical arguments given below suggest that
the densest packings of these particles may also be given by their optimal lattice packings.
   It is crucial to stress that the nonspherical particles in this family do not deviate appre-
ciably from a sphere, i.e., their corresponding asphericity γ is always bounded and relatively
close to unity, and, moreover, their three principle axes (directions) are equivalent. This is
in contrast to the ellipsoid, which, although centrally symmetric, generally possesses three
principle axes (directions) that are inequivalent and its asphericity can increase without limit

                                             33
as the largest aspect ratio grows. These characteristics suggest that the densest ellipsoid
arrangements are non-lattice packings, which indeed has been verified [12].
   Our simulation results and the ensuing theoretical arguments lead to the following con-
jecture:
Conjecture 1: The densest packings of the centrally symmetric Platonic solids are given by
their corresponding optimal lattice packings.
   We now sketch what could be the major elements of a proof of this conjecture. In the case
of each of the Platonic solids, face-to-face contacts are favored over vertex-to-face contacts to
achieve higher packing densities, since the former allows the particle centroids to get closer
to one another. Such contacting neighbor configurations around each particle reduce the
volume of the corresponding convex hull joining the centroids of the contacting particles,
and the fraction of space covered by the particles within this convex hull should be increased;
see Fig. 13 for a two-dimensional illustration.
   To achieve the densest packing, the fraction of space covered by the particles within the
convex hull should ideally be maximized and so should the number of face-to-face contacts
per particle. Of course, this is only a local criterion that may not be consistent with the
densest global packing. However, it will be seen that the equivalence of the three princi-
ple directions of a centrally symmetric Platonic solid is crucial for this local optimization
criterion to be consistent with the globally densest packing.
   It is noteworthy that orienting each of the particles in the packings of centrally symmetric
Platonic solids enable a larger number of face-to-face contacts and thus allows the maximal
fraction of space covered by the particles within the convex hull. For example, a particle
with F faces, possesses F/2 families of axes that go through the centroid of the particle and
intersect the centrally-symmetric face pairs such that the particles (in the same orientation)
with their centroids arranged on these axes form face-to-face contacts.
   The requirement that the particles have the same orientation is globally consistent with a
lattice packing. Indeed, in the optimal lattice packings of the centrally symmetric Platonic
solids, each particle has the maximum number of face-to-face contacts that could be obtained
without violating the impenetrability condition. It is highly unlikely that such particles
possessing three equivalent principle directions and aligned in the same direction could form
a more complicated non-lattice periodic packings with densities that are larger than the
optimal lattice packings. Such non-lattice packings would arise to take advantage of the

                                              34
             (a)                 (b)                   (c)                       (d)

FIG. 13: (color online). Illustration of our conjecture concerning the optimal packings of centrally-
symmetric particles using two-dimensional octagonal packings. It is shown how different particle
orientations and arrangements affect the number of face-to-face contacts and the area of the convex
hulls joining the centers of the neighboring particles around a central one. (a) The octagons do
not have the same orientation and the number of face-to-face contacts is small. (b) The octagons
are aligned with 4 contacts per particle to form a lattice packing, but the area of the convex
hull associated with the central particle is not minimized. (c) The octagons are aligned with 6
contacts per particle to form a lattice packing, but although the area of the convex hull associated
with the central particle is smaller than in (b), it is not minimized. (d) The octagons are aligned
with 6 contacts per particle to form a lattice packing, and the area of the convex hull associated
with the central particle is minimized. This minimization corresponds to finding the the minimal
circumscribing hexagon and therefore corresponds to the optimal lattice packing [41].



rotational degrees of freedom. By requiring particle alignments, only translational degrees
of freedom remain and hence optimization over these degrees of freedom would lead to the
globally optimal packings, which should be lattice packings. Constraining rotational degrees
of freedom in this way in a non-lattice packing would at best lead to a local optimum in
density. This conclusion is clearly supported by our simulations, which use multiple-particle
configurations in the fundamental cell and only produce the optimal lattice packings.
   In the aforementioned arguments, a key step that is difficult to prove is the observation
that alignment of each of the particles maximizes the number of face-to-face contacts and
thus the fraction of space covered by the particles within the convex hull joining the centroids
of the contacting neighbors around a central polyhedron. A rigorous verification of this step
would lead to the consistency of the aforementioned local and global optimization criteria.


                                               35
   It is noteworthy that in two dimensions, our local criterion to achieve the optimal packings
of centrally symmetric regular polygons (the two-dimensional counterparts of the centrally
symmetric Platonic solids) amounts to the identification of optimal neighbor configurations
with the maximal edge-to-edge contacts per particle such that the convex hull joining the
centroids of the contacting neighbors is minimal. This statement is rigorously true in two
dimensions because it is tantamount to a theorem due to Fejes Tóth [41], which states that
the densest packing of a centrally symmetric particle in two dimensions can be obtained by
circumscribing the particle with the minimal centrally symmetric hexagon, which of course
tiles R2 . Finding the minimal circumscribing centrally symmetric hexagon is equivalent to
finding the minimal area convex hull joining the centroids of the six contacting particles
(the maximal number can be obtained in two dimensions for centrally symmetric particles).
The fact that local optimality is consistent with the global optimality in two dimensions
(e.g., a centrally symmetric hexagon can always tessellate the space) does not hold in three
dimensions. Although we have presented a three-dimensional generalization of the Fejes
Tóth theorem, by replacing the minimal hexagon with the minimal convex-hull volume, as
pointed out before, it is extremely difficult to provide a rigorous proof for it.
   Although Conjecture 1 applies to the centrally symmetric Platonic solids, all of our argu-
ments apply as well to each of the centrally symmetric Archimedean solids. It cannot be true
for the truncated tetrahedron, which is the only non-centrally symmetric Archimedean solid.
Specifically, it immediately follows from the results of Ref. 13 that a non-lattice packing of
truncated tetrahedra can be constructed based on the “primitive Welsh” tessellation (i.e., by
removing the small regular tetrahedra) that possesses the density φ = 23/24 = 0.958333 . . .,
which is appreciably larger than the optimal-lattice-packing density of φLmax = 0.680921 . . .,
and contains two particle centroids per fundamental cell. In fact, given that the truncated
tetrahedra cannot tile space, the density of the “primitive Welsh” packing of truncated tetra-
hedra is so large that it may be the optimal packing of such particles. The lattice vectors
of this periodic packing are given in Appendix C.
   Since the arguments used to justify Conjecture 1 apply equally well to the 12 centrally
symmetric Archimedean solids, we are led to the following more general conjecture:
Conjecture 2: The densest packings of the centrally symmetric Platonic and Archimedean
solids are given by their corresponding optimal lattice packings.
   The aforementioned arguments can also be extended to the case of superballs, but here

                                             36
the local principle curvatures at the contacting points should be sufficiently small so as to
maximize the fraction of space covered by the particles within the convex hull joining the
centroids of the neighbors. The central symmetry and equivalence of the three principle
directions of superballs means that dense packings of such objects are favored when the
particles are aligned, which again leads to consistency between local and global optimal-
ity. The fact that the optimal lattice packing densities of superballs is relatively close to
the upper-bound values, at least around the sphere point, as well as results from previous
molecular dynamics simulations [17] also strongly suggest that the densest packings of these
particles are given by their corresponding optimal lattice packings.
   It is noteworthy that under the assumption that Conjecture 2 is valid, one has upper
bounds that are the complete analog of (14), i.e.,
                                                      
                                              vp C
                               φmax ≤ min          φ ,1 ,                                   (25)
                                              vc max

where vc is the volume of an appropriately chosen centrally symmetric Platonic or
Archimedean solid and φC
                       max is the corresponding optimal density for such a solid, which ac-

cording to Conjecture 2 is the optimal lattice packing. This bound will generally be sharper
than bound (14) because the reference optimal packing is less symmetric than the sphere.
For example, the conjectured bound (25) will be sharp for slightly deformed Platonic and
Archimedean solids or nonspherical particles derived by smoothing the vertices, edges and
faces of polyhedra.
   Our work also naturally leads to another conjecture:
Conjecture 3: The optimal packing of any convex, congruent polyhedron without central
symmetry generally is not a (Bravais) lattice packing.
In other words, the set of such polyhedra whose optimal packing is not a lattice is overwhelm-
ingly larger than the set whose optimal packing is a lattice. We have seen that because the
regular tetrahedron and truncated tetrahedron lack central symmetry, dense packings of
such objects favor face-to-face contacts. Such orientations immediately eliminate the possi-
bility that lattice packings (in which particles must have the same orientations) are optimal.
Similarly, it is very plausible that dense packings of most convex, congruent polyhedra with-
out central symmetry are facilitated by face-to-face contacts and hence the optimal packings
cannot be lattices. For example, consider a square with one missing corner, i.e., an isosceles
triangle with a right angle (see Fig. 14). At first glance, one might surmise that if the missing

                                              37
                             (a)                                  (b)

FIG. 14: (color online). Portions of two packing configurations of pentagons obtained by cutting
off a corner (isosceles triangle with a right angle) of a square. (a) The optimal lattice packing and
(b) a two-particle basis periodic packing that tiles the plane. Let side length of the square be 1
and the lengths of the equal sides of the isosceles triangle be β ∈ (0, 1). The lattice vectors of the
                                     β              β
optimal lattice packing are eL             L
                             1 = i − 2 j, e2 = (1 − 2 )i + (1 − β)j and the lattice vectors of the

periodic packing are eP1 = i + βj, eP2 = (1 − β)i + (2 − β)j with one particle at origin and the other
at b1 = (1 − β)i + (1 − β)j, where i, j are the unit vectors along the two orthogonal coordinate
directions, coinciding with two orthogonal sides of the square. The density (covering fraction) of
                                           β  2     β  2
the optimal lattice packing is φL
                                max = (1 − 2 )/(1 − 4 ) and the density of the periodic packing is

φPmax = 1. It can be seen that for all 0 < β < 1, φL                           P
                                                   max is always smaller than φmax .




piece is sufficiently small, the original lattice packing should still be optimal or nearly opti-
mal (see Fig. 14a), since lattice packings are optimal for squares. However, no matter how
small the missing piece may be, a periodic packing in which the fundamental cell contains
two pentagons can be constructed that tile the plane (see Fig. 14b). This is done by taking
advantage of the asymmetry of the particle. Thus, we see from this counterintuitive example
that if the particle does not possess central symmetry, it is possible to exploit its rotational
degrees of freedom to yield a periodic packing with a complex basis that are generally denser
than the optimal lattice packing. On the other hand, there are special cases where the lat-
tice will be optimal, such as for the rhombic dodecahedron that has one corner clipped [43].
However, these special cases are overwhelmed in number by those whose optimal packings
are not lattices. If Conjecture 3 is valid, it also applies to nonspherical particles derived by


                                                  38
smoothing the vertices, edges and faces of polyhedra provided that the particle curvature at
face-to-face contacts is sufficiently small.
   It should not go unnoticed that the densest packings of all of the Platonic and
Archimedean solids reported here as well as the densest known packings of superballs
[17] and ellipsoids [12] have densities that exceed the optimal sphere packing density
          √
φSmax = π/ 18 = 0.7408 . . .. These results are consistent with a conjecture of Ulam who
proposed, without any justification, that the optimal density for packing congruent spheres
is smaller than that for any other convex body [42]. The sphere is perfectly isotropic with
an asphericity γ of unity, and therefore, as noted earlier, its rotational degrees of freedom
are irrelevant in affecting its packing characteristics. On the other hand, each of the afore-
mentioned convex non-spherical particles break the continuous rotational symmetry of the
sphere and thus its broken symmetry can be exploited to yield the densest possible packings.
However, broken rotational symmetry in and of itself may not be sufficient to satisfy Ulam’s
conjecture if the convex particle has a little or no symmetry.
   It will also be interesting to determine whether our conjecture can be extended to other
polyhedral packings. The infinite families of prisms and antiprisms [44] provide such a class
of packings. A prism is a polyhedron having bases that are parallel, congruent polygons and
sides that are parallelograms. An antiprism is a polyhedron having bases that are parallel,
congruent polygons and sides that are alternating bands of triangles. Prisms with an even
number of sides and antiprisms are centrally symmetric. Although prisms and antiprisms
are naturally grouped with the Archimedean solids (i.e., they are polyhedra in which the
same regular polygons appear at each vertex), they are generally much less symmetric than
either the Platonic or Archimedean solids. Moreover, even the centrally symmetric prisms
and antiprisms generally do not possess three equivalent directions. Thus, it is less obvious
whether Bravais lattices would still provide the optimal packings for these solids, except for
prisms that tile space (e.g., hexagonal prism or rhombical prisms). In future work, it would
be desirable to test whether our conjecture extends to prisms and antiprisms that possess
central symmetry and three equivalent directions using the ASC scheme.
   It is worth noting that in four dimensions, the analogs of the tetrahedron, cube, octahe-
dron, dodecahedron and icosahedron are the four-dimensional regular simplex, hypercube,
cross polytope, 120-cell and 600-cell, respectively. All of these four-dimensional polytopes
possess central symmetry, except for the simplex [45]. While the hypercube and cross poly-

                                               39
tope tile R4 , the optimal packings of simplices are still likely to be non-lattices. Since our
conjecture for the three-dimensional Platonic solids should still apply in four dimensions,
the densest packings of the 120-cell and 600-cell could be their corresponding optimal lattice
packings. The cross polytopes for d ≥ 5 no longer tile space, and their optimal packings
may still be their densest lattice packings provided that d is sufficiently small. However, in
sufficiently high dimensions, the densest lattice packings of the centrally symmetric poly-
topes are probably no longer optimal, since lattice packings in high dimensions are known
to possess huge “holes” into which additional particles can be inserted, yielding higher pack-
ing densities with possibly non-lattice arrangements. Indeed, it has recently been argued
that disordered sphere packings in very high dimensions could be denser than any ordered
packing [46].
   Recent progress in particle synthesis methods have enabled the production of a wide
spectrum of nanoparticle shapes such as tetrahedra [47], cubes [48], icosahedra [49] and
prisms [50]. In such applications, it would be of great interest to predict the corresponding
crystal structures, which might possess unusual symmetries and properties. The idea of
incorporating collective particle motions due to the adaptive fundamental cell should still
make it efficient to search the desired crystal structures formed by those polyhedral nano-
building blocks. Finally, it is worth noting that the ASC algorithm is also suitable to generate
random packings of polyhedral particles. Crucial dynamical parameters of the system, such
as the strain rate can be properly controlled to produce packings with varying degrees of
disorder, including the maximally random jammed ones [51]. We will explore disordered
packings in future work.


   ACKNOWLEDGMENTS


   We are grateful to Henry Cohn, John Conway and Alex Jaoshvili for helpful comments
on our manuscript. S. T. thanks the Institute for Advanced Study for its hospitality during
his stay there. This work was supported by the Division of Mathematical Sciences at the
National Science Foundation under Award Number DMS-0804431 and by the MRSEC Pro-
gram of the National Science Foundation under Award Number DMR-0820341. The figures
showing the polyhedra were generated using the AntiPrism package developed by Adrian
Rossiter.


                                             40
   APPENDIX A: OPTIMAL LATTICE PACKINGS OF THE PLATONIC AND
ARCHIMEDEAN SOLIDS


   Here we collect fundamental packing characteristics (i.e., the lattice vectors, densities and
contact numbers) of the optimal lattice packings of the Platonic and Archimedean solids,
most of which are obtained from Refs. 22, 34 and 23. The Platonic solids are explicitly
defined as the regions (sets of points) bounded by a set of linear equations of the coordinates.
The Archimedean solids are either defined as intersections of different Platonic solids or
delineated based on their symmetry. A point set S representing the polyhedron multiplied
by a number α means an isotropic expansion of the polyhedron S with linear ratio α. S1 ∩S2
represents the intersection region of two polyhedra S1 and S2 . The lattice vectors are given
by column vectors (i.e., the basis vectors are the unit vectors along the coordinate axis).
The naming code used below for the Platonic and Archimedean solids is the same one used
in Figs. 1 and 3.
   A tetrahedron (P1) has 4 vertices, 6 edges and 4 triangular faces. It is defined as the
region

P 1 = x ∈ R3 : x1 + x2 + x3 ≤ 1, −x1 − x2 + x3 ≤ 1, −x1 + x2 − x3 ≤ 1, x1 − x2 − x3 ≤ 1 .
     

                                                                                               (A1)
The optimal lattice vectors are given by

      a1 = (2, −1/3, −1/3)T ,      a2 = (−1/3, 2, −1/3)T ,     a3 = (−1/3, −1/3, 2)T ,         (A2)

where the superscript “T” denotes transpose of a column vector. Each tetrahedron of the
packing contacts 14 others. The packing density is φLmax = 18/49 = 0.367346 . . ..
   An icosahedron (P2) has 12 vertices, 30 edges and 20 triangular faces. It is defined as
the region

P 2 = x ∈ R3 : |x1 | + |x2 | + |x3 | ≤ 1, |Φx1 | + |x3 /Φ| ≤ 1, |Φx2 | + |x1 /Φ| ≤ 1, |Φx3 | + |x2 /Φ| ≤ 1 ,
     

                                                                                               (A3)




                                               41
                   √
where Φ = (1 +      5)/2 is the golden ratio. The lattice vectors are given by
                                  √       2
                                                          √                  √ 
                      (−33/8 − 39 5/8)x̄ + (39/4 + 33 5/4)x̄ − 11/4 − 3 5/2
                2
                                              √              √                
    a1 (x̄) = (1+Φ)                 (−1/4 − 5/4)x̄ + 1 + 5/2                  ,
                                                                              
                                  √                      √                √   
                        (33/8 + 39 5/8)x̄2 + (−19/2 − 8 5)x̄ + 13/4 + 3 5/2

                                 √           2
                                                               √                  √        
                   (−39/8 − 33 5/40)x̄ + √
                                          (35/4 + 41 5/20)x̄ − 5/2 − 23 5/20 
                                                       √
              2
  a2 (x̄) = (1+Φ)                  (5/4 + 5/4)x̄ − 1 − 5/2                    , (A4)
                                                                            
                  
                               √       2
                                                    √                 √      
                     (−39/8 − 33 5/40)x̄ + (15/2 + 9 5/5)x̄ + 13/4 − 3 5/20

                                                     √               √ 
                                             (3/2 +       5/2)x̄ − 2 − 5
                                                                        
                       a3 (¯(x)) = (1+Φ)
                                     2
                                                            x̄           ,
                                                                        
                                         
                                                                        
                                                            0

where x̄ ∈ (1, 2) is the unique root of the polynomial
                                     √          √                   √
                 1086x3 − (1063 + 113 5)x2 + (15 5 + 43)x + 102 + 44 5 = 0.                    (A5)

It is found that x̄ = 1.59160301 . . . and therefore the lattice vectors, up to nine significant
figures, are given by

                         a1 = (0.711782425, 0.830400102, 1.07585146)T ,
                        a2 = (−0.871627249, 0.761202911, 0.985203828)T ,                       (A6)
                               a3 = (−0.06919791, 1.59160301, 0)T .

Each icosahedron of the packing contacts 12 others.                The packing density is φLmax =
0.836357 . . .
   A dodecahedron (P3) has 20 vertices, 30 edges and 12 pentagonal faces. It is defined as
the region

             P 3 = x ∈ R3 : |Φx1 | + |x2 | ≤ 1, |Φx2 | + |x3 | ≤ 1, |Φx3 | + |x1 | ≤ 1 .
                  
                                                                                               (A7)

The optimal lattice vectors are given by

                                 a1 = (2/(1 + Φ), 2/(1 + Φ), 0)T ,
                                 a2 = (2/(1 + Φ), 0, 2/(1 + Φ))T ,                             (A8)
                                 a3 = (0, 2/(1 + Φ), 2/(1 + Φ))T .

                                                  42
Each dodecahedron of the packing contacts 12 others. The packing density is φLmax =
(2 + Φ)/4 = 0.904508 . . ..
   An octahedron (P4) has 6 vertices, 12 edges and 8 triangular faces. It is defined as the
region
                              P 4 = x ∈ R3 : |x1 | + |x2 | + |x3 | ≤ 1 .
                                   
                                                                                          (A9)

The optimal lattice vectors are given by

         a1 = (2/3, 1, 1/3)T ,   a2 = (−1/3, −2/3, 1)T ,       a3 = (−1, 1/3, −2/3)T .    (A10)

Each octahedron of the packing contacts 14 others. The packing density is φLmax = 18/19 =
0.947368 . . ..
   A cube (P5) has 8 vertices, 12 edges and 6 square faces. It is defined as the region

                                    P 5 = x ∈ R3 : |xi | ≤ 1 .
                                         
                                                                                          (A11)

The optimal lattice vectors are given by

                       a1 = (2, 0, 0)T ,   a2 = (0, 2, 0)T ,   a3 = (0, 0, 2)T .          (A12)

Each cube of the packing contacts 26 others (which includes vertex-to-vertex contacts). The
packing density is φLmax = 1.
   A truncated tetrahedron (A1) has 12 vertices, 18 edges and 8 face: 4 hexagons and 4
triangles. It is defined as the region

                              A1 = x ∈ R3 : x ∈ 5 · P 1 ∩ −3 · P 1 .
                                  
                                                                                          (A13)

The optimal lattice vectors are given by

         a1 = (4/3, 4, 8/3)T ,   a2 = (4, −8/3, −4/3)T ,       a3 = (−8/3, 4/3, −4)T .    (A14)

Each truncated tetrahedron of the packing contacts 14 others. The packing density is
φLmax = 207/304 = 0.680921 . . ..
   A truncated icosahedron (A2) has 60 vertices, 90 edges and 32 faces: 20 hexagons and 12
pentagons. It is defined as the region

                      A2 = x ∈ R3 : x ∈ (1 + Φ) · P 2 ∩ (4/3 + Φ) · P 3 .
                          
                                                                                          (A15)


                                                43
The optimal lattice vectors are given by

                   a1 = (1 + Φ)aP1 2 ,       a2 = (1 + Φ)aP2 2 ,    a3 = (1 + Φ)aP3 2 ,   (A16)

where aPi 2 (i = 1, 2, 3) are the lattice vectors of the optimal lattice packing of icosahedra.
Each truncated icosahedron of the packing contacts 12 others. The packing density is
φLmax = 0.784987 . . .
   A snub cube (A3) has 24 vertices, 60 edges and 38 faces: 6 squares and 32 triangles. Let
the snub cube orientated in a way such that its 6 square faces lie in the hyperplanes

                                     x ∈ R3 : |xi | = 1(i = 1, 2, 3) .
                                    
                                                                                          (A17)

The optimal lattice vectors are given by

                  a1 = (2, 0, 0)T ,    a2 = (0, 0, 2)T ,    a3 = (1, 2/y ∗ − 2, −1)T .    (A18)

where y ∗ is the unique real solution of y 3 + y 2 + y = 1. Each snub cube of the packing
contacts 12 others. The packing density is φLmax = 0.787699 . . .
   A snub dodecahedron (A4) has 60 vertices, 150 edges and 92 faces: 12 pentagons and 80
triangles. Let the snub dodecahedron orientated in a way such that its 12 pentagonal faces
lie in the hyperplanes of the faces of the dodecahedron (1 + Φ) · P 3. The optimal lattice
vectors are given by

                         a1 = (2, 2, 0)T ,    a2 = (2, 0, 2)T ,    a3 = (0, 2, 2)T .      (A19)

Each snub dodecahedron of the packing contacts 12 others. The packing density is φLmax =
0.788640 . . .
   A rhombicosidodecahdron (A5) (also known as small rhombicosidodecahedron) has 60
vertices, 120 edges and 62 face: 12 pentagons, 30 squares and 20 triangles. It is defined as
the region:
          n                                 √                                        o
    A5 = x ∈ R3 : x ∈ (3Φ + 2) · [P 5 ∩ (1 + 2)P 4] ∩ (4Φ + 1) · P 2 ∩ (3 + 3Φ) · P 3 .
                                                                                          (A20)
The optimal lattice vectors are given by

                          a1 = ((Φ − 1)/(2Φ + 1), 7, (9Φ + 4)/(2Φ + 1))T ,
                          a2 = ((9Φ + 4)/(2Φ + 1), (Φ − 1)/(2Φ + 1), 7)T ,                (A21)
                          a3 = (7, (9Φ + 4)/(2Φ + 1), (Φ − 1)/(2Φ + 1))T .

                                                   44
Each rhombicosidodecahedron of the packing contacts 12 others. The packing density is
φLmax = (8Φ + 46)/(36Φ + 15) = 0.804708 . . ..
   A truncated icosidodecahdron (A6) (also known as great rhombicosidodecahedron) has
120 vertices, 180 edges and 62 faces: 12 decagons, 20 hexagons and 30 squares. It is defined
as the region
          n
              3
                                           √                                        o
    A6 = x ∈ R : x ∈ (5Φ + 4) · [P 5 ∩ (1 + 2)P 4] ∩ (6Φ + 3) · P 2 ∩ (5 + 5Φ) · P 3 .
                                                                                      (A22)
The optimal lattice vectors are given by

                  a1 = (10, 10, 0)T ,    a2 = (10, 0, 10)T ,   a3 = (0, 10, 10)T .    (A23)

Each truncated icosidodecahedron of the packing contacts 12 others. The packing density
is φLmax = (2Φ/5 + 9/50) = 0.827213 . . ..
   A truncated cubeoctahedron (A7) (also known as great rhombicubeoctahedron) has 48
vertices, 72 edges and 26 faces: 6 octagons, 8 hexagons and 12 squares. It is defined as the
region
                                                   √                          √
              A7 = {x ∈ R3 : |x1 | + |x2 | ≤ (2 + 3 2), |x2 | + |x3 | ≤ (2 + 3 2),
                                      √          √                    √               (A24)
                |x2 | + |x3 | ≤ (2 + 3 2), x ∈ (2 2 + 1) · P 5 ∩ (3 2 + 3) · P 4}.
The optimal lattice vectors are given by
                             √          √          √           T
                     a1 = 4 2 + 2, −4 2 − 1 + 2α, 4 2 + 1 − 2α ,
                        √                  √                √     T
                  a2 =    2/2 − 3/2 + α, −3 2/2 + 1/2 + α, 4 2 + 2 ,      (A25)
                                 √                √              T
                   a3 = 7/2 + 7 2/2 − α, 1 + 2α, 5 2/2 + 3/2 − α ,
           √ √
where α = 33( 2 + 1)/6. Each truncated cubeoctahedron of the packing contacts 12
others. The packing density is φLmax = 0.8493732 . . ..
   An icosidodecahedron (A8) has 30 vertices, 60 edges and 32 faces: 12 pentagons and 20
triangles. It is defined as the region

                                A8 = x ∈ R3 : x ∈ P 2 ∩ P 3 .
                                    
                                                                                      (A26)

The optimal lattice vectors are given by

                               a1 = (2/(1 + Φ), 2/(1 + Φ), 0)T ,
                               a2 = (2/(1 + Φ), 0, 2/(1 + Φ))T ,                      (A27)
                               a3 = (0, 2/(1 + Φ), 2/(1 + Φ))T .

                                               45
Each icosidodecahedron of the packing contacts 12 others. The packing density is φLmax =
(14 + 17Φ)/48 = 0.864720 . . ..
   A rhombicuboctahedron (A9) (also known as small rhombicubeoctahedron) has 24 vertices,
48 edges and 26 faces: 18 squares and 8 triangles. It is defined as the region

                          A9 = {x ∈ R3 : |x1 | + |x2 | ≤ 2, |x2 | + |x3 | ≤ 2,
                                                  √                 √                    (A28)
                            |x1 | + |x3 | ≤ 2, x ∈ 2 · P 5 ∩ (4 − 2) · P 4}.

The optimal lattice vectors are given by

                      a1 = (2, 2, 0)T ,   a2 = (2, 0, 2)T ,   a3 = (0, 2, 2)T .          (A29)

Each truncated cubeoctahedron of the packing contacts 12 others. The packing density is
           √
φLmax = (16 2 − 20)/3 = 0.875805 . . ..
   A truncated dodecahedron (A10) has 60 vertices, 90 edges and 32 faces: 12 decagons and
20 triangles. It is defined as the region

                   A10 = {x ∈ (1 + Φ) · P 3 ∩ [(7 + 12Φ)/(3 + 4Φ)] · P 2} .              (A30)

The optimal lattice vectors are given by

                      a1 = (2, 2, 0)T ,   a2 = (2, 0, 2)T ,   a3 = (0, 2, 2)T .          (A31)

Each truncated dodecahedron of the packing contacts 12 others. The packing density is
φLmax = (5Φ + 16)/(24Φ − 12) = 0.897787 . . ..
   A cuboctahedron (A11) has 12 vertices, 24 edges and 14 faces: 6 squares and 8 triangles.
It is defined as the region
                                    A11 = {x ∈ P 5 ∩ 2 · P 4} .                          (A32)

The optimal lattice vectors are given by

     a1 = (2, −1/3, −1/3)T ,       a2 = (−1/3, 2, −1/3)T ,     a3 = (−1/3, −1/3, 2)T .   (A33)

Each cuboctahedron of the packing contacts 14 others. The packing density is φLmax =
45/49 = 0.918367 . . ..
   A truncated cube (A12) has 24 vertices, 36 edges and 14 faces: 6 octagons and 8 triangles.
It is defined as the region
                                                   √
                                A12 = x ∈ P 5 ∩ (1 + 2) · P 4 .                          (A34)

                                                46
The optimal lattice vectors are given by

                 a1 = (2, −2α, 0)T ,     a2 = (0, 2, −2α)T ,     a3 = (−2α, 0, 2)T ,   (A35)
                 √
where α = (2 − 2)/3. Each truncated cube of the packing contacts 14 others. The packing
                           √
density is φLmax = 9/(5 + 3 2) = 0.973747 . . ..
     A truncated octahedron (A13) has 24 vertices, 36 edges and 14 faces: 8 hexagons and 6
squares. It is defined as the region

                                 A13 = {x ∈ P 5 ∩ (3/2) · P 4} .                       (A36)

The optimal lattice vectors are given by

                     a1 = (2, 0, 0)T ,   a2 = (2, 2, 0)T ,     a3 = (1, 1, −1)T .      (A37)

Each truncated octahedron of the packing contacts 14 others. The packing density is φLmax =
1.


     APPENDIX B: LATTICE VECTORS AND OTHER CHARACTERISTICS OF
THE DENSEST KNOWN TETRAHEDRAL PACKING


     Here we report the lattice vectors of fundamental cell for the densest known tetrahedral
packing with 314 particles up to 12 significant figures, although our numerical precision
is not limited by that. The side length of the tetrahedron is d0 = 1.8 and its volume is
     √
vp = 2d30 /12 = 0.687307791313. The lattice vectors are given by

                a1 = (6.130348985438, − 1.714011427194, 0.022462185673)T ,
                  a2 = (1.622187720300, 6.106123418234, 0.123567805838)T ,              (B1)
                  a3 = (0.055014355972, 0.116436714923, 6.526427521512)T .

The volume of the fundamental cell is Vol(F ) = |a1 × a2 · a3 | = 262.344828467328. Thus,
the packing density is readily computed as

                        N · vp    314 × 0.687307791313
                   φ=           =                      = 0.822637319490.                (B2)
                        Vol(F )     262.344828467328

The coordinates of each of the 314 tetrahedra are given elsewhere [37].



                                                47
   APPENDIX C: LATTICE VECTORS OF THE DENSEST KNOWN PACKING
OF TRUNCATED TETRAHEDRA


   The “primitive Welsh” tessellation of space consists of truncated large regular tetrahe-
dra and small regular tetrahedra, as described in Ref. 13. When the small tetrahedra are
removed, the remaining truncated tetrahedra give the densest known periodic (non-lattice)
packing of such objects. Following Ref. 13, the centroids of the truncated tetrahedra sit
at the nodes 0 and 1 of the two adjacent cells of a body-centered cubic lattice shown in
                                                                                   √
Fig. 2(a) of Ref. 13. Let length of the edges of the truncated tetrahedron be dE = 2/2,
then the lattice vectors are given by

                       a1 = (1, 1, 0)T ,   a2 = (1, 0, 1)T ,   a3 = (0, 1, 1)T .                (C1)

The basis vectors for the centroids of 0-type and 1-type truncated tetrahedra are respectively
given by
                             b0 = (1/2, 1/2, 1/2)T ,     b1 = (0, 0, 0)T .                      (C2)




 [1] J. D. Bernal, in Liquids: Structure, Properties, Solid Interactions, (Ed. T. J. Hughel, Elsevier,
    New York, 1965).
 [2] R. Zallen, The Physics of Amorphous Solids (Wiley, New York, 1983).
 [3] S. Torquato, Random Heterogeneous Materials: Microstructure and Macroscopic Properties
    (Springer-Verlag, New York, 2002).
 [4] P. M. Chaikin and T. C. Lubensky, Principles of Condensed Matter Physics (Cambridge
    University Press, New York, 2000).
 [5] S. F. Edwards, Granular Matter (Ed. A. Mehta, Springer-Verlag, New York, 1994); E. R.
    Nowak, J. B. Knight, E. Ben-Naim, H. M. Jaeger, and S. R. Nagel, Phys. Rev. E 57, 1971
    (1998); R. P. Behringer, Nature 435, 1079 (2005); M. Schröter, D. I. Goldman, and H. L.
    Swinney, Phys. Rev. E 71, 030301 (2005).
 [6] I. C. Kim and S. Torquato, J. Appl. Phys. 69, 2280 (1991); D. Cule and S. Torquato, Phys.
    Rev. B 58, R11829 (1998); M. C. Rechtsman and S. Torquato, J. Appl. Phys. 103, 084901
    (2008); T. Zohdi, Int. J. Numer. Meth. Eng. 76, 1250 (2008).


                                                48
 [7] J. H. Conway and N. J. A. Sloane, Sphere Packings, Lattices and Groups (Springer-Verlag,
     New York, 1998).
 [8] H. Cohn and N. Elkies, Ann. Math. 157, 689 (2003); H. Cohn, Geom. Topol. 6, 329 (2002).
 [9] G. Parisi and F. Zamponi, J. Stat. Mech.: Theory Exp. 2006, P03017. S. Torquato and F.
     H. Stillinger, Phys. Rev. E 73, 031106 (2006); S. Torquato, O. U. Uche and F. H. Stillinger,
     Phys. Rev. E 74, 061308 (2006).
[10] T. C. Hales, Ann. Math. 162, 1065 (2005).
[11] A. Bezdek and W. Kuperberg, in DIMACS Series in Discrete Math, Theoret. Comput. Sci. 4
     (Eds. P. Gritzmann and B. Sturmfels, AMS, Providence, RI, 1991); J. M. Wills, Mathematika
     38, 318 (1991).
[12] A. Donev, F. H. Stillinger, P. M. Chaikin, and S. Torquato, Phys. Rev. Lett. 92, 255506
     (2004).
[13] J. H. Conway and S. Torquato, Proc. Nat. Acad. Sci. 103, 10612 (2006).
[14] P. Chaikin, S. Wang, and A. Jaoshvili, APS March Meeting Abstract (2007).
[15] E. R. Chen, Discrete Comput. Geom. 40, 214 (2008).
[16] Y. Jiao, S. H. Stillinger, and S. Torquato, Phys. Rev. Lett. 100, 245504 (2008).
[17] Y. Jiao, S. H. Stillinger, and S. Torquato, Phys. Rev. E 79, 041309 (2009).
[18] Dense polyhedral packings have relevance to molecular crystal structures of organic com-
     pounds. See, for example, A. I. Kitaigorodskii, Molecular Crystal and Molecules (Academic,
     New York, 1973).
[19] It is well known that viral capsids have icosahedral symmetry. See, for example; R. Zandi,
     D. Reguera, R. F. Bruinsma, W. M. Gelbart, and 5. J. Rudnick, Proc. Nat. Acad. Sci. 101,
     15556 (2004).
[20] A. R. Kansal, S. Torquato, and F. H. Stillinger, Phys. Rev. E 66, 041109 (2002). This tiling-
     degeneracy example vividly illustrates a fundamental point made in Ref. 20, namely, packing
     arrangements of nonoverlapping objects at some fixed density can exhibit a large variation in
     their degree of structural order.
[21] In the physical sciences and engineering, this is referred to as a Bravais lattice. Unless otherwise
     stated, the term “lattice” will refer to a Bravais lattice only, not the more general classification
     of a periodic lattice with a basis.
[22] H. Minkowski, Nachr. K. Ges. Wiss. Göttingen, Math.-Phys. KL, 311 (1904).


                                                 49
[23] U. Betke and M. Henk, Comput. Geom. 16, 157 (2000).
[24] The overlap potential function of a pair of strictly convex and smooth particles is an analytic
    function of the positions, orientations and shapes of the two particles, whose value indicates
    whether the two particles overlap or not, or whether they are tangent to one another; see also
    Ref. 25.
[25] A. Donev. S. Torquato and F. H. Stillinger, J. Comput. Phys. 202, 737 (2005).
[26] A. Donev. S. Torquato and F. H. Stillinger, J. Comput. Phys. 202, 765 (2005).
[27] S. Torquato and Y. Jiao, Nature, 460 876 (2009).
[28] Note that in Fig. 1 of Ref. [27], “P6” should be “A1.”
[29] In this paper, a deformation refers to a volume-preserving shape change of the fundamental
    cell (i.e., a shear), which is to be distinguished from a volume change of the cell, which can
    either be a compression or an expansion of the cell.
[30] S. Torquato and Y. Jiao, unpublished.
[31] W. S. Jodrey and E. M. Tory, Phys. Rev. A 32, 2347 (1985); M. D. Rintoul and S. Torquato,
    Phys. Rev. E 58, 532 (1998); O. U. Uche, F. H. Stillinger, and S. Torquato, Physica A 342,
    428 (2004); A. Donev, J. Burton, F. H. Stillinger and S. Torquato, Phys. Rev. B 73, 054109
    (2006).
[32] S. Torquato and F. H. Stillinger, J. Phys. Chem. B, 105, 11849 (2001); S. Torquato, A.
    Donev, and F. H. Stillinger, Int. J. Solids Struct. 40, 7143 (2003); A. Donev, S. Torquato, F.
    H. Stillinger and R. Connelly, J. Appl. Phys. 95, 989 (2004).
[33] E. G. Golshtein and N. V. Tretyakov, Modified Lagrangians and Monotone Maps in Optimiza-
    tion (Wiley, New York, 1996).
[34] D. J. Hoylman, Bull. Am. Math. Soc. 76, 135 (1970).
[35] In Ref. 13, the authors suggested (not conjectured) that the regular tetrahedron “may not be
    able to pack as densely as the sphere, which would contradict a conjecture of Ulam.” Indeed,
    the results of Ref. 15 verifies that the tetrahedron does not violate Ulam’s conjecture.
[36] A. Donev, R. Connelly, F. H. Stillinger and S. Torquato, Phys. Rev. E 75, 051304 (2007).
[37] The supplementary materials can be found at http://cherrypit.princeton.edu/pre-packings.html.
[38] The fundamental cells of the initial configurations for the optimization algorithm involve
    periodic copies of the packings listed in Table I. Specifically, if the lattice vectors of the
    packings listed in Table I are denoted by e1 , e2 and e3 , then the lattice vectors associated


                                               50
    with the initial configurations are given by eL            L              L
                                                  1 = n1 e1 , e2 = n2 e2 and e3 = n3 e3 , where

    n1 , n2 , n3 ≥ 1 are integers. Thus, the number of tetrahedra in the fundamental cells of the
    initial configurations is an integral multiple, i.e., n1 × n2 × n3 , of that for the corresponding
    packings given in Table I. For the optimal lattice packing, n1 = n2 = n3 = 3; for the uniform
    packing, n1 = n2 = n3 = 3; for the Welsh packing, n1 = n2 = n3 = 1; for the icosahedral
    packing, n1 = n2 = n3 = 1; and for the wagon-wheels packing, n1 = n2 = 2, n3 = 1.
[39] This bound was motivated by a question posed by Robert Connelly in May, 2005 at a Banff
    International Research Station Workshop entitled “Densest Packings of Spheres,” organized
    by K. Bezdek, H. Cohn and C. Radin. Specifically, he asked whether an upper bound on the
    maximal density of congruent ellipsoid packings in R3 that is less than unity for any aspect
    ratios of the ellipsoid could be formulated. One of us in attendance (S. T.) provided the version
    of upper bound (14) for the special case of ellipsoids. Of course, for ellipsoids, the bound (14)
    is less than unity provided that the eccentricity of the ellipsoid is sufficiently small. However,
    here we recognize that the same type of upper bound can yield a reasonably tight upper bound
    for other nonspherical shapes provided that the particle has a small asphericity γ.
[40] Although we cannot exclude the possibility that there exist other optimal packing particle
    arrangements that possess the same density as the optimal lattice packings, it is highly unlikely
    that those arrangements could be constructed in the same way way as the stacking variants of
    the optimal FCC lattice packings for spheres (the so-called Barlow packings). The polyhedral
    shape of the particles does not allow them to fit snugly into the “holes” formed in the particle
    layers above and below a particular layer, as in the case of spheres, and hence stackings of the
    layers cannot result in packings with densities that are higher than that of the optimal lattice
    packing. If degenerate optimal packings exist, they cannot be of the “Barlow” type.
[41] L. Fejes Tóth, Regular Figures (Macmillan, New York, 1964).
[42] M. Gardner, The Colossal Book of Mathematics: Classic Puzzles, Paradoxes, and Problems
    (Norton, New York, 2001), p. 13.
[43] A. Bezdek, Intuitive Geometry 63, 17 (1994); T. C. Hales, Discrete Comput. Geom. 36, 5
    (2006).
[44] P. R. Cromwell, Polyhedra (Cambridge University Press, 1997).
[45] H. S. M. Coxeter, Regular Polytopes (Dover, New York, 1973).
[46] S. Torquato and F. H. Stillinger, Exp. Math. 15, 307 (2006); A. Scardicchio, F. H. Stillinger


                                               51
    and S. Torquato, J. Math. Phys. 49, 043301 (2008).
[47] E. C. Creyson, J. E. Barton and T. W. Odom, Small 2, 368 (2006).
[48] Y. G. Sun and Y. N. Xia, Science 298, 2176 (2002)
[49] T. S. Ahmadi, Z. L. Wang, T. C. Green, A. Henglein and M. A. El-Sayed, Science 272, 1924
    (1996).
[50] R. Jin, Y. Cao, C. A. Mirkin, K. L. Kelly, G. C. Schatz and J. G. Zeng, Science 294, 1901
    (2001).
[51] S. Torquato, T. M. Truskett and P. G. Debenedetti, Phys. Rev. Lett. 84, 2064 (2000).




                                             52
