                                                     Dense Packings of the Platonic and Archimedean Solids

                                                     S. Torquato1,2,3,4,5 & Y. Jiao5
arXiv:0908.4107v1 [cond-mat.stat-mech] 27 Aug 2009




                                                     1
                                                         Department of Chemistry, Princeton University, Princeton New Jersey 08544, USA

                                                     2
                                                         Princeton Center for Theoretical Science, Princeton University, Princeton New Jersey 08544,

                                                     USA

                                                     3
                                                         Princeton Institute for the Science and Technology of Materials, Princeton University, Princeton

                                                     New Jersey 08544, USA

                                                     4
                                                         School of Natural Sciences, Institute for Advanced Study, Princeton New Jersey 08540, USA

                                                     5
                                                         Department of Mechanical and Aerospace Engineering, Princeton University, Princeton New Jer-

                                                     sey 08544, USA


                                                     Dense packings have served as useful models of the structure of liquid, glassy and crystal

                                                     states of matter 1–4 , granular media 3, 5 , heterogeneous materials 3 , and biological systems

                                                     6–8
                                                           . Probing the symmetries and other mathematical properties of the densest packings is a

                                                     problem of long-standing interest in discrete geometry and number theory 9–11 . The prepon-

                                                     derance of previous work has focused on spherical particles, and very little is known about

                                                     dense polyhedral packings. We formulate the problem of generating dense packings of poly-

                                                     hedra within an adaptive fundamental cell subject to periodic boundary conditions as an

                                                     optimization problem, which we call the Adaptive Shrinking Cell (ASC) scheme. This novel

                                                     optimization problem is solved here (using a variety of multi-particle initial configurations)

                                                     to find dense packings of each of the Platonic solids in three-dimensional Euclidean space. We


                                                                                                       1
find the densest known packings of tetrahedra, octahedra, dodecahedra and icosahedra with

densities 0.782 . . ., 0.947 . . ., 0.904 . . ., and 0.836 . . ., respectively. Unlike the densest tetra-

hedral packing, which must be a non-Bravais lattice packing, the densest packings of the

other non-tiling Platonic solids that we obtain are their previously known optimal (Bravais)

lattice packings. Our simulations results, rigorous upper bounds that we derive, and theoret-

ical arguments lead us to the strong conjecture that the densest packings of the Platonic and

Archimedean solids with central symmetry are given by their corresponding densest lattice

packings. This is the analog of Kepler’s sphere conjecture for these solids.


      A large collection of nonoverlapping solid objects (particles) in d-dimensional Euclidean

space Rd is called a packing. The packing density φ is defined as the fraction of space Rd covered

by the particles. A problem that has been a source of fascination to mathematicians and scientists

for centuries is the determination of the densest arrangement(s) of particles that do not tile space

and the associated maximal density φmax 9 . The preponderance of previous work has focused on

spherical particles but, even for this simple shape, the problem is notoriously difficult. Indeed,

Kepler’s conjecture concerning the densest sphere packing arrangement was only proved by Hales

in 2005 10 .


      Attention has very recently turned to finding the maximal-density packings of nonspherical

particles in R3 , including ellipsoids 12 , tetrahedra 13, 14 , and superballs 15 . Very little is known

about the densest packings of polyhedral particles that do not tile space, including the majority of

the Platonic and Archimedean solids studied by the ancient Greeks. The difficulty in obtaining



                                                   2
dense packings of polyhedra is related to their complex rotational degrees of freedom and to the

non-smooth nature of their shapes.




Figure 1 The five Platonic solids: tetrahedron (P1), icosahedron (P2), dodecahedron

(P3), octahedron (P4) and cube (P5). The 13 Archimedean solids: truncated tetra-

hedron (A1), truncated icosahedron (A2), snub cube (A3), snub dodecahedron (A4),

rhombicosidodecahdron (A5), truncated icosidodecahdron (A6), truncated cuboctahe-

dron (A7), icosidodecahedron (A8), rhombicuboctahedron (A9), truncated dodecahedron

(A10), cuboctahedron (A11), truncated cube (A12), and truncated octahedron (A13). Note

that the cube (P5) and truncated octahedron (A13) are the only Platonic and Archimedean

solids, respectively, that tile space.


                                               3
      The Platonic solids (mentioned in Plato’s Timaeus) are convex polyhedra with faces com-

posed of congruent convex regular polygons. There are exactly five such solids: the tetrahedron,

icosahedron, dodecahedron, octahedron and cube (see Fig. 1). An Archimedean solid is a highly

symmetric, semi-regular convex polyhedron composed of two or more types of regular polygons

meeting in identical vertices. There are thirteen Archimedean solids (see Fig. 1). Note that the

tetrahedron (P1) and truncated tetrahedron (A1) are the only Platonic and Archimedean solids, re-

spectively, that are not centrally symmetric. A particle is centrally symmetric if it has a center C

that bisects every chord through C connecting any two boundary points of the particle. We will see

that this type of symmetry plays a fundamental role in determining the nature of the dense packing

arrangements.


      Some definitions are in order here. A lattice Λ in R3 is an infinite set of points generated by a

set of discrete translation operations (defined by integer linear combinations of a basis of R3 ) 4 . A

(Bravais) lattice packing is one in which the centroids of the nonoverlapping particles are located

at the points of Λ, each oriented in the same direction. The space R3 can then be geometrically

divided into identical regions F called fundamental cells, each of which contains just the centroid

of one particle. Thus, the density of a lattice packing is given by

                                                 vparticle
                                            φ=             ,                                       (1)
                                                 Vol(F )

where vparticle is the volume of a particle and Vol(F ) is the volume of a fundamental cell. A

periodic packing of particles is obtained by placing a fixed nonoverlapping configuration of N

particles (where N ≥ 1) with arbitrary orientations in each fundamental cell of a lattice Λ. Thus,

the packing is still periodic under translations by Λ, but the N particles can occur anywhere in the

                                                  4
chosen cell subject to the nonoverlap condition. The density of a periodic packing is given by

                                              Nvparticle
                                         φ=              .                                       (2)
                                               Vol(F )



     We formulate the problem of generating dense packings of nonoverlapping polyhedra within

an adaptive fundamental cell subject to periodic boundary conditions as an optimization problem

(see Methods Summary). We call this optimization scheme the Adaptive Shrinking Cell (ASC).

Figure 2 illustrates a simple sequence of configuration changes for a four-particle packing.




               (a)                              (b)                              (c)




Figure 2     By efficiently exploring the design-variable space (DVS), which consists of the

particle configurational space and the space of lattices (due to our use of an adaptive

fundamental cell), the Adapative Shrinking cell (ASC) scheme enables one to find a point

in the DVS in the neighborhood of the starting point that has a higher packing density than

the initial density. The process is continued until the deepest minimum of the objective

function (a maximum of packing density) is obtained, which could be either a local or

                                                 5
global optimum. Here we show a series of sequential changes of a four-particle packing

configuration due to the design variables in the ASC algorithm. (a) An initial configuration

of four particles. (b) A trial move of a randomly selected particle (colored red in this

frame) that is rejected because it overlaps another particle. This is determined precisely

using the separation axis theorem 16 . (c) A trial move that is accepted, which results in a

deformation and compression (small in magnitude) changing the fundamental cell shape

and size as well as the relative distances between the particles.


       Finding the densest packings of regular tetrahedra is part of the 18th problem in Hilbert’s

famous set of problems. The densest (Bravais) lattice packing of tetrahedra (which requires all

of the tetrahedra to have the same orientations) has the relatively low density φlattice
                                                                                 max = 18/49 =


0.367 . . . and each tetrahedron touches 14 others 17 . Recently, Conway and Torquato showed that

the densest packings of tetrahedra must be non-Bravais lattice packings, and found packings with

density as large as φ ≈ 0.72 13 . Chaikin, Wang and Jaoshvili experimentally generated jammed

disordered packings of nearly “tetrahedral” dice with φ ≈ 0.75. Chen 14 has recently discovered

a periodic packing of tetrahedra with φ = 0.7786 . . .. We call this the “wagon-wheels” packing

because the basic subunits consist of two orthogonally intersecting “wagon” wheels. A “wagon

wheel” consists of five contacting tetrahedra packed around a common edge (see Fig. 1a of Ref.

13).


       We begin by solving the ASC scheme to obtain dense packings of tetrahedra using initial

configurations based upon low-density versions of the aforementioned packings. Initial conditions



                                                6
based on periodic copies of the wagon-wheels packing with 72 particles per cell lead to the densest

packing of tetrahedra reported to date with φ = 0.7820021 . . . (see Fig. 3). Its lattice vectors

and other characteristics are given in the Supplementary Information. The preference for face-to-

face (not vertex-to-face) contacts and the lack of central symmetry ensure that dense tetrahedral

packings must be non-lattice structures.




          (a)                     (b)                       (c)                      (d)




Figure 3 Portions of the densest packing of tetrahedra that we obtain from our simu-

lations and the optimal lattice packings of the icosahedra, dodecahedra, and octahedra

that our simulations converge to. All of these packings are at least locally jammed, i.e.,

each particle cannot be translated or rotated while fixing the positions and orientations of

all the other particles 18, 19 . We emphasize that even though the latter three cases begin

with complex multi-particle initial configurations in the large fundamental (repeating) cell,

they all converge to packings in which a smaller repeat unit contains only one centroid,

                                                7
i.e., they all converge to lattice (i.e., Bravais lattice) packings and, in fact, the correspond-

ing densest lattice packings. (a) Tetrahedral packing. We depict the 72 particles in the

fundamental cell of this non-lattice packing. Within the cell, the particles are character-

ized by short-range translational order and a preference for face-to-face contacts (see

Supplementary information). (b) Optimal lattice packing of icosahedra. (c) Optimal lattice

packing of dodecahedra. (d) Optimal lattice packing of octahedra.


        To obtain dense packings of icosahedra, dodecahedra and octahedra, we use a wide range of

initial configurations. These include multi-particle configurations (with N ranging from 20 to 343)

of random “dilute” packings and a variety of lattice packings with a wide range of densities. In

the case of icosahedra, dodecahedra and octahedra, we obtain final packings with densities at least

as large as 0.836315 . . ., 0.904002 . . . and 0.947003 . . ., respectively, which are extremely close in

structure and density to their corresponding optimal lattice packings with φlattice
                                                                            max     = 0.836357 . . .
                     √
20
     , φlattice
        max = (5 +       5)/8 = 0.904508 . . . 20 , and φlattice                     21
                                                         max = 18/19 = 0.947368 . . . , respectively.


Figure 3 shows the optimal lattice packings of icosahedra, dodecahedra and octahedra in which

each particle contacts 12, 12 and 14 others, respectively. Our simulation results strongly suggest

that the optimal lattice packings of the centrally symmetric Platonic solids are indeed the densest

packings of these particles, especially since these arise from a variety of initial “dilute” multi-

particle configurations within an adaptive fundamental cell.


        We can show that the maximal density φmax of a packing of congruent nonspherical particles




                                                    8
of volume vp is bounded from above according to

                                                                      
                                                          vparticle π
                          φmax ≤ φupper
                                  max
                                        bound
                                              = min                √ ,1 ,                         (3)
                                                          vsphere   18

where vsphere is the volume of the largest sphere that can be inscribed in the nonspherical particle
      √
and π/ 18 is the maximal sphere-packing density. The proof is given in the Supplementary Infor-

mation. The upper bound (3) will be relatively tight for packings of nonspherical particles provided

that the asphericity γ (equal to the ratio of the circumradius to the inradius) of the particle is not

large. Since bound (3) cannot generally be sharp (i.e., exact) for a nontiling, nonspherical particle,

any packing whose density is close to the upper bound (3) is nearly optimal, if not optimal.




Figure 4 Comparison of the densest known lattice packings (blue circles) of the Pla-

tonic and Archimedean solids 17, 20, 21 to the corresponding upper bounds (red squares)

                                                  9
obtained from (3). The large asphericity and lack of central symmetry of the tetrahe-

dron (P1) and truncated tetrahedron (A1) are consistent with the large gaps between

their upper-bound densities and densest-lattice-packing densities, and the fact that there

are non-lattice packings with densities appreciably greater than φlattice
                                                                  max (depicted as green


triangles in the figure). The truncated tetrahedron is the only non-centrally symmetric

Archimedean solid, the densest known packing, which is a non-lattice packing with two

particles per fundamental cell and a density at least as high as 23/24 = 0.958333 . . . 13 .


      Figure 4 compares the density of the densest lattice packings of the Platonic and Archimedean

solids to the corresponding upper bounds on the maximal density for such packings. The central

symmetry of the majority of the Platonic and Archimedean solids and their associated relatively

small asphericities explain the corresponding small differences between φlattice  upper bound
                                                                         max and φmax         and

is consistent with our simulation findings that strongly indicate that their optimal arrangements are

their respective densest lattice packings.


      Why should the densest packings of the centrally symmetric solids be their corresponding

optimal lattice packings? First, note that face-to-face contacts allow such polyhedral packings to

achieve higher densities because they enable the contacting centroids around each particle to come

closer together. Second, face-to-face contacts are maximized when each particle has the same

orientation because of the central symmetry and the equivalence of the three principle axes (asso-

ciated with the small asphericity) of the solid. This is consistent with a lattice packing, the densest

of which is the optimal one. These arguments in conjunction with our simulation results and rig-



                                                  10
orous bounds lead us to the following conjecture: The densest packings of the centrally symmetric

Platonic and Archimedean solids are given by their corresponding optimal lattice packings. This

is the analog of Kepler’s sphere conjecture for these solids.


      There is no reason to believe that denser packings of tetrahedra cannot be achieved by em-

ploying even better initial conditions than those based on the wagon-wheels packing and a larger

number of particles. Observe that the densest packings of all of the Platonic and Archimedean

solids reported here as well as the densest known packings of superballs 15 and ellipsoids 12 have
                                                                     √
densities that exceed the optimal sphere packing density φsphere
                                                          max    = π/ 18 = 0.7408 . . .. These re-

sults are consistent with a conjecture of Ulam 22 . Ulam’s conjecture may be violated if the convex

particle has little or no symmetry, but a counterexample has yet to be given.


      How does our conjecture extend to other polyhedral packings? It’s natural to group the

infinite families of prisms and antiprisms 23 with the Archimedean solids. A prism is a polyhedron

having bases that are parallel, congruent polygons and sides that are parallelograms. An antiprism

is a polyhedron having bases that are parallel, congruent polygons and sides that are alternating

bands of triangles. Prisms with an even number of sides and antiprisms are centrally symmetric and

so it may be that Bravais lattices of such solids are optimal. However, prisms with an odd number

of sides are not centrally symmetric and thus their optimal packings may not be Bravais lattices.

In future work, we will determine whether our conjecture extends to prisms and antiprisms.


METHODS SUMMARY



                                                 11
      The objective function in our ASC optimization scheme is taken to be the negative of the

packing density φ. Starting from an initial packing configuration in the fundamental cell, the

positions and orientations of the polyhedra are design variables for the optimization. Importantly,

we also allow the boundary of the fundamental cell to deform as well as shrink or expand such

that there is a net shrinkage (increase of the density) in the final state. Thus, the deformation

and compression/expansion of the cell boundary are also design variables. We are not aware of

any packing algorithm that employs both a sequential search of the configurational space of the

particles and the space of lattices via an adaptive fundamental cell that shrinks on average to obtain

dense packings. The ASC has a number of novel features that distinguish it from previous packing

algorithms that have been devised for spheres 24–26 , ellipsoids 27, 28 and superballs 15 (see Methods

for details).



 1. Bernal, J. D. in Liquids: Structure, Properties, Solid Interactions (eds Hughel, T. J.) 25-50

    (Elsevier, 1965).


 2. Zallen, R. The Physics of Amorphous Solids (Wiley, 1983).


 3. Torquato, S. Random Heterogeneous Materials: Microstructure and Macroscopic Properties

    (Springer-Verlag, 2002).


 4. Chaikin, P. M.& Lubensky, T. C. Principles of Condensed Matter Physics (Cambridge Uni-

    versity Press, 2000).


 5. Edwards, S. F. in Granular Matter (eds Mehta, A.) 121-140 (Springer-Verlag, 1994).



                                                 12
 6. Liang, J. & Dill, K. A. Are proteins well-packed? Biophys J. 81, 751-7666 (2001).


 7. Purohit, P. K., Kondev, J. & Phillips, R. Mechanics of DNA packaging in viruses. Proc. Nat.

    Acad. Sci. 100, 3173-3178 (2003).


 8. Gevertz, J. L. & Torquato, S. A Novel Three-Phase Model of Brain Tissue Microstructure.

    PLoS Comput. Biol. 4, e1000152 (2008).


 9. Conway, J. H. & Sloane, N. J. A. Sphere Packings, Lattices and Groups (Springer-Verlag,

    1998).


10. Hales, T. C. A proof of the Kepler conjecture. Ann. Math. 162, 1065-1185 (2005).


11. Cohn, H. & Elkies, N. New upper bounds on sphere packings I. Ann. Math. 157, 689-714

    (2003).


12. Donev, A., Stillinger, F. H., Chaikin, P. M. & Torquato, S. Unusually dense crystal ellipsoid

    packings. Phys. Rev. Lett. 92, 255506 1-4 (2004).


13. Conway, J. H. & Torquato, S. Packing, tiling and covering with tetrahedra. Proc. Nat. Acad.

    Sci. 103, 10612-10617 (2006).


14. Chen, E. R. A dense packing of regular tetrahedra. Discrete Comput. Geom. 40, 214-240

    (2008).


15. Jiao, Y., Stillinger, F. H. & Torquato, S. Optimal packings of superballs. Phys. Rev. E 79,

    041309 1-12 (2009).



                                               13
16. Golshtein, E. G. & Tretyakov, N. V. Modified Lagrangians and Monotone Maps in Optimiza-

    tion (Wiley, 1996).


17. Hoylman, D. J. The densest lattice packing of tetrahedra. Bull. Am. Math. Soc. 76, 135-137

    (1970).


18. Torquato, S. & Stillinger, F. H. Multiplicity of generation, selection, and classification proce-

    dures for jammed hard-particle packings. J. Phys. Chem. B 105, 11849-11853 (2001).


19. Donev, A., Connelly, R., Stillinger, F. H. & Torquato, S. Underconstrained jammed packings

    of nonspherical hard particles: ellipses and ellipsoids. Phys. Rev. E 75, 051304 1-32 (2007).


20. Betke, U. & Henk, M. Densest lattice packings of 3-polytopes. Comput. Geom. 16, 157-186

    (2000).


21. Minkowski, H. Dichteste gitterförmige Lagerung kongruenter Körper. Nachr. K. Ges. Wiss.

    Göttingen, Math.-Phys. KL 311-355 (1904).


22. Gardner, M. The Colossal Book of Mathematics: Classic Puzzles, Paradoxes, and Problems

    (Norton, 2001).


23. Cromwell, P. R. Polyhedra (Cambridge University Press, 1997).


24. Jodrey, W. S. & Tory, E. M. Computer simulation of close random packing of equal spheres.

    Phys. Lett. A 32, 2347-2351 (1985).


25. Rintoul, M. D. & S. Torquato, S. Hard-sphere statistics along the metastable amorphous

    branch. Phys. Rev. E 58, 532-537 (1998).

                                                 14
26. Uche, O. U., Stillinger, F. H. & Torquato, S. Concerning maximal packing arrangements of

    binary disk mixtures. Physica A 342, 428-446 (2004).


27. Donev, A., Torquato, S. & Stillinger, F. H. Neighbor list collision-driven molecular dynamics

    for nonspherical hard particles: I. algorithmic details. J. Comput. Phys. 202, 737-764 (2005).


28. Donev, A., Torquato, S. & Stillinger, F. H. Neighbor list collision-driven molecular dynamics

    for nonspherical hard particles: II. applications to ellipses and ellipsoids. J. Comput. Phys.

    202, 765-793 (2005).



Acknowledgements We are grateful to Henry Cohn and John Conway for helpful comments on our

manuscript. S. T. thanks the Institute for Advanced Study for its hospitality during his stay there. This

work was supported by the National Science Foundation under Award Numbers DMS-0804431 and DMR-

0820341. The figures showing the polyhedra were generated using the AntiPrism package developed by

Adrian Rossiter.


Competing Interests    The authors declare that they have no competing financial interests.


Correspondence     Correspondence and requests for materials should be addressed to S.T (email:

torquato@electron.princeton.edu).




METHODS


      The ASC optimization problem could be solved using various techniques, depending on the

shapes of the particles. For example, for spheres, linear programming (LP) techniques can effi-

                                                   15
ciently produce optimal solutions (Torquato, S. & Jiao, Y.). However, for polyhedra, the complex

nonoverlap conditions make the ASC scheme inefficient to solve using LP methods. For polyhedral

particles, we solve the ASC optimization problem using a standard Monte Carlo (MC) procedure

with a Metropolis acceptance rule for trial moves to search the design variable space (DVS) effi-

ciently, which contains both the configuration space of the particles and the space of lattices.


      In our implementation, a polyhedral particle is represented by the position of its centroids as

well as the coordinates of all its vertices relative to the centroid. Note that although this represen-

tation contains redundant information, it is a convenient way to deal with the rotational motions

of the polyhedra. To search the configuration space of the particles, small random trial moves of

arbitrarily selected particles are attempted sequentially for each particle. Each trial move is equally

likely to be a translation of the centroid of the particle or a rotation of the particle about a randomly

oriented axis through its centroid.


      The space of lattices is searched by deforming/compressing/expanding the fundamental cell,

which is completely characterized by a strain tensor in the linear regime (i.e., small strain limit).

The trace of the strain tensor determines the volume change of the fundamental cell and is involved

in the objective function. The off-diagonal components of the tensor determines the shape change

of the cell. The positions of the particles centroids are relative coordinates with respect to the

lattice vectors. When the strain tensor is applied to the lattice vectors, although the relative coordi-

nates of the centroids remain the same, the Euclidean distances between the particles will change.

Thus, the deformation/compression/expansion of the fundamental cell at least in part allows for



                                                   16
collective particle motions, which is more efficient in finding a direction in the DVS leading to a

higher packing density. Moreover, it is the overall compression of the fundamental cell that causes

the packing density to increase, not the growth of the particles as in most molecular dynamics and

MC hard-particle packing algorithms 15, 24–28 . It should be noted that for polyhedral particles, an

algorithm that employs particle growth with an adaptive non-shrinking fundamental cell is compu-

tationally less efficient than the ASC scheme that fixes the particle size while allowing the cell to

shrink on average.


      In the simulation, starting from an initial configuration of polyhedral particles, a trial config-

uration can be generated by moving (translating and rotating) a randomly chosen particle or by a

random deformation and compression/expansion of the fundamental cell. If this causes interpar-

ticle overlaps, the trial configuration is rejected; otherwise, if the fundamental cell shrinks in size

(which makes the density φ higher), the trial configuration is accepted. On the other hand, if the

cell expands in size, the trial configuration is accepted with a specified probability pacc , which is

made to decrease as φ increases and approaches zero at the jamming limit 18 (i.e., locally maxi-

mally dense packing) is reached. In particular, we find pacc , with an initial value pacc ∼ 0.35 and

decreasing as a power law, works well for most systems that we studied. The ratio of the number of

particle motions to the number of cell trial moves should be greater than unity (especially towards

the end of the simulation), since compressing a dense packing could cause many overlaps between

the particles. Depending on the initial configuration, the magnitudes of the particle motions and the

strain components need to be chosen carefully to avoid the system getting stuck in some shallow

local minimum.


                                                  17
      A crucial aspect of any packing algorithm is the need to check for interparticle overlaps under

attempted particle motions. Hard polyhedron particles, unlike spheres, ellipsoids and superballs,

do not possess simple “overlapping” functions. (The overlap function of a pair of strictly convex

and smooth particles is a function of the positions, orientations and shapes of the two particles,

whose value indicates whether the two particles overlap or not, or whether they are tangent to

one another.) The separation axis theorem 16 enables us to check for interparticle overlaps for

polyhedra up to the numerical precision of the machine. In particular, the theorem states that two

convex polyhedra are separated in space if and only if there exists an axis, on which the projections

of the vertices of the two polyhedra do not overlap. The separation axis is either perpendicular to

one of the faces of the polyhedra or perpendicular to a pair of edges from different polyhedra. Thus,

this reduces the number of axes that need to be checked from infinity to [E(E − 1)/2 + 2F ], where

E and F is the number of edges and faces of the polyhedra, respectively. A pre-check using the

circumradius and inradius of the polyhedra could dramatically speeds up the simulations, i.e., two

particles are guaranteed to overlap if the centroidal separation is smaller than twice the inradius

and guaranteed not to overlap if the centroidal separation is larger than twice the circumradius.

The circumsphere is the smallest sphere containing the particle. The insphere is the largest sphere

than can be inscribed in the particle.


      The cell method and near-neighbor list 27, 28 are also employed to improve the efficiency of

the simulation, but are appropriately modified to incorporate the adaptive fundamental cell.




                                                 18
