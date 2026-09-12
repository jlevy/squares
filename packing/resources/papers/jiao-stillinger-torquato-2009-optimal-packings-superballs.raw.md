                                                                           Optimal Packings of Superballs

                                                                     Y. Jiao1 , F. H. Stillinger2 and S. Torquato2,3,4,5
                                                               1
                                                                   Department of Mechanical and Aerospace Engineering,
                                                              Princeton University, Princeton New Jersey 08544, USA
                                                                     2
                                                                         Department of Chemistry, Princeton University,
arXiv:0902.1504v1 [cond-mat.soft] 9 Feb 2009




                                                                                 Princeton New Jersey 08544, USA
                                                               3
                                                                   Program in Applied and Computational Mathematics,
                                                              Princeton University, Princeton New Jersey 08544, USA
                                               4
                                                   School of Natural Sciences, Institute for Advanced Study, Princeton NJ 08540 and
                                                                           5
                                                                               Princeton Center for Theoretical Science,
                                                              Princeton University, Princeton New Jersey 08544, USA
                                                                                       (Dated: October 24, 2018)




                                                                                                 1
                                              Abstract
  Dense hard-particle packings are intimately related to the structure of low-temperature phases of
matter and are useful models of heterogeneous materials and granular media. Most studies of the
densest packings in three dimensions have considered spherical shapes, and it is only more recently
that nonspherical shapes (e.g., ellipsoids) have been investigated. Superballs (whose shapes are
defined by |x1 |2p + |x2 |2p + |x3 |2p ≤ 1) provide a versatile family of convex particles (p ≥ 0.5) with
both cubic- and octahedral-like shapes as well as concave particles (0 < p < 0.5) with octahedral-
like shapes. In this paper, we provide analytical constructions for the densest known superball
packings for all convex and concave cases. The candidate maximally dense packings are certain
families of Bravais lattice packings (in which each particle has 12 contacting neighbors) possessing
the global symmetries that are consistent with certain rotational symmetries of a superball. We
also provide strong evidence that our packings for convex superballs (p ≥ 0.5) are most likely the
optimal ones. The maximal packing density as a function of p is nonanalytic at the sphere-point
(p = 1) and increases dramatically as p moves away from unity. Two more nontrivial nonanalytic
behaviors occur at p∗c = 1.1509 . . . and p∗o = ln 3/ ln 4 = 0.7924 . . . for “cubic” and “octahedral”
superballs, respectively, where different Bravais lattice packings possess the same densities. The
packing characteristics determined by the broken rotational symmetry of superballs are similar
to but richer than their two-dimensional “superdisk” counterparts [Y. Jiao, F. H. Stillinger and
S. Torquato, Phys. Rev. Lett., 100, 245504 (2008)], and are distinctly different from that of
ellipsoid packings. Our candidate optimal superball packings provide a starting point to quantify
the equilibrium phase behavior of superball systems, which should deepen our understanding of
the statistical thermodynamics of nonspherical-particle systems.

PACS numbers: 61.50.Ah, 05.20.Jj




                                                  2
I.    INTRODUCTION


     Packing problems, such as how densely given solid objects can fill d-dimensional Euclidean
space ℜd , have been a source of fascination to mathematicians and scientists for centuries,
and continue to intrigue them today. Dense packings of hard particles have served as useful
models to understand the structures of low-temperature phases of matter, such as liquids,
glasses and crystals [1, 2, 4], heterogeneous materials [3, 4, 5], granular media [6, 7], and even
protein folding [8]. Packing problems arise in many different branches of pure mathematics
[9, 10] and in information theory [11].
     In general, a collection of given solid objects (particles) in d-dimensional Euclidean space
Rd is called a packing if no two of the objects have an interior point in common. The
packing density φ is defined as the fraction of space Rd covered by the particles. A problem
of great interest is the determination of the densest arrangement(s) of such particles and the
associated maximal density φmax . Besides the aforementioned applications, finding maximal
density packings is of importance to understanding the structure and properties of crystalline
equilibrium phases of particle systems as well as their ground-state (T = 0) structures in low
dimensions in which the interactions are characterized by steep repulsions and short-ranged
attractions.
     The optimal solution to this packing problem for congruent particles that do not tile
space is already very challenging, even in low-dimensional Euclidean spaces Rd (d = 2, 3).
In two dimensions, the optimal packing of circular disks is the well-known triangular-lattice
                                 √
packing with density φmax = π/(2 3). For ellipses, the densest packing can be obtained by
an affine transformation of the triangular-lattice packing of circular disks, which possesses
                              √
the same density φmax = π/(2 3). These packings can also be constructed by enclosing each
particle with a hexagon with minimum area that tessellates R2 [12, 13]. It is only recently
that the famous Kepler conjecture, which postulates that the densest packing of spheres in
                             √
R3 has a density φmax = π/(3 2), as realized by the stacking variants of the face-centered
cubic (FCC) lattice packing, has been proved [14]. Although dense sphere packings for d ≥ 4
have received considerable recent attention [15, 16, 17, 18, 19], optimal solutions are not
rigorously known. Packing problems in high Euclidean dimensions are intimately related to
the best way of transmitting digital signals over a noisy channel [10, 11].
     Understanding the organizing principles that lead to the densest packings of nonspherical


                                               3
particles that do not tile space is of great practical and fundamental interest. Clearly, the
effect of asphericity is an important feature to include on the way to characterizing more
fully real dense granular media. Another important application relates to supramolecular
chemistry [20] of organic compounds whose molecular constituents can possess many different
types of group symmetries [21].
   On the theoretical side, no results exist that rigorously prove the densest packings of
other congruent non-space-tiling particles in three dimensions. For congruent ellipsoids, the
densest known packings with density φmax = 0.7707 . . . are achieved by a family of crystal
packings (for a wide range of aspect ratios) in which each ellipsoid has contact with 14 others
[22]. Recently, Conway and Torquato found dense periodic packings of regular tetrahedra
with φ ≈ 0.72 by filling imaginary icosahedra with the densest arrangement of 20 tetrahedra
and arranging the icosahedra in their optimal Bravais lattice arrangement [23]. Chaikin
et al. experimentally produced jammed disordered packings of nearly tetrahedral dice with
density φ ≈ 0.75 [24]. Chen has discovered the densest known periodic packing of tetrahedra
with φ = 0.7786 . . . [25, 26].
   This paper is concerned with superball packings in low dimensions, although primarily in
three dimensions. A d-dimensional superball is a centrally symmetric body in Rd occupying
the region [27]
                                  |x1 |2p + |x2 |2p + · · · + |xd |2p ≤ 1,                 (1)

where xi (i = 1, . . . , d) are Cartesian coordinates and p ≥ 0 is the deformation parameter,
which indicates to what extent the particle shape has deformed from that of a d-dimensional
sphere (p = 1). A particle is centrally symmetric if it has a center P that bisects every chord
through P connecting any two boundary points of the particle. We note that a particle is
convex if the entire line segment connecting two points of the particle also belongs to the
particle; otherwise it is concave. The terms superdisk and superball will be our designations
for the two-dimensional (d = 2) and three-dimensional (d = 3) cases, respectively. In
general, a superdisk possesses square symmetry, as p moves away from unity, two families
of superdisks with square symmetry can be obtained, with the symmetry axes rotated 45
degrees with respect to each other; when p < 0.5, the superdisk is concave (see Fig. 1).
   In three dimensions, a superball is a perfect sphere at p = 1, but can possess two types
of shape anisotropy: cubic-like shapes (three-dimensional analog of the square symmetry
of the superdisk) and octahedral-like shapes, depending on the value of the deformation

                                                   4
         (a) p = 0.45          (b) p = 0.75           (c) p = 1.0           (d) p = 2.0


            FIG. 1: Superdisks with different values of the deformation parameter p.




         (a) p = 0.45            (b) p = 0.75            (c) p = 1.0           (d) p = 2.0


     FIG. 2: (color online). Superballs with different values of the deformation parameter p.


parameter p (see Fig. 2). As p continuously increases from 1 to ∞, we have a family of
convex superballs with cubic-like shapes; at the limit p = ∞, the superball is a perfect cube.
As p decreases from 1 to 0.5, a family of convex superballs with octahedral-like shapes are
obtained; at p = 0.5, the superball becomes a regular octahedron. When p < 0.5, the
superball still possesses an octahedral-like shape but is now concave, becoming a three-
dimensional “cross” in the limit p → 0 [28]. Note that the cube and regular octahedron
(two of the five Platonic polyhedra) have the same group symmetry (i.e., they have the same
48 space group elements) because they are dual to each other [29].
   Recently, we constructed the densest known packings of superdisks in R2 , which provides
a wide class of packings of both convex and concave particles with square symmetry [30]. In
particular, the optimal packing is achieved by one of two families of Bravais lattice packings,
which we called the Λ0 - and Λ1 -lattice packings. (Note that in a Bravais lattice packing there
is only one particle in the fundamental cell in contrast to periodic packings that have multi-
particle fundamental cells.) In the following, we will usually use the term “lattice” to mean
a “Bravais lattice.” As the particle shape moves away from the circular disk point, the
                                                √
packing density increases dramatically from π/(2 3) and shows a non-analytic behavior at


                                                5
the circular point. Here we stress that in light of a theorem due to Fejes Tóth [12, 13],
which states that the optimal packing of any centrally symmetric convex body in R2 can be
always achieved by circumscribing the body with the smallest hexagon that tiles the plane,
our packings can be verified to be optimal for every specific value of p > 0.5. This procedure
is outlined in the Appendix of this paper.
   In this paper, we construct the densest known packings of convex superballs, which are
suggested by simulations and based on the requirements that certain group symmetries of
the packings are preserved as the superballs deform from the sphere and octahedron points.
Moreover, we show that as p changes from unity, i.e., moves away from the sphere point,
maximal packing density φmax rises steeply. The broken rotational symmetry of superballs
results in a cusp in φmax at p = 1. Thus, the initial increase of φmax is linear in |p − 1| and
φmax is a nonanalytic function of p at p = 1. Two more nontrivial nonanalytic behaviors
occur at p∗c = 1.1509 . . . and p∗o = ln 3/ ln 4 = 0.7924 . . . for “cubic” and “octahedral”
superballs, respectively,
   For superballs in the cubic regime (p > 1), the candidate optimal packings are achieved
by two families of Bravais lattice packings possessing two-fold (see Sec. III.A) and three-
fold rotational symmetry (see Sec. III.B), respectively, which can both be considered to
be continuous deformations of the FCC lattice. For superballs in the octahedral regime
(0.5 < p < 1), there are also two families of Bravais lattices obtainable from continuous
deformations of the FCC lattice keeping its four-fold rotational symmetry (see Sec. III.B),
and from the densest lattice packing for regular octahedra [32, 33], keeping the translational
symmetry of the projected lattice on the coordinate planes, which are apparently optimal in
the vicinity of the sphere point and the octahedron point, respectively (see Secs. IV.A and
IV.B). The fact that the two families of lattice packings for superballs with octahedral shapes
constructed separately from the provable optimal packing of spheres and the densest known
packing of octahedra (which we conjecture to be optimal [34]) meet at a single point (the
same packing density with the same p value) strongly suggests that our candidate packings
are most likely optimal. The packing characteristics determined by the broken rotational
symmetry of superballs are similar to but richer than their two-dimensional “superdisk”
counterparts [30] and are distinctly different from that of ellipsoid packings [22].
   For concave superballs (p < 0.5), the lack of simulation techniques to generate such dense
packings prevent us from drawing definitive conclusions about the optimality of concave

                                             6
superball packings. Here we construct a family of dense packings of concave superballs that
are close to optimal around the octahedron point (p = 0.5), based on the densest Bravais
lattice packing and will discuss an interesting aligning effect in the limit p → 0 (see Sec.
IV.C).
      The rest of the paper is organized as follows: In Sec. II, we briefly describe the simulation
techniques used to generate dense packings of superballs, which guide our analytical packing
constructions. In Sec. III and Sec. IV, we construct the densest known packings of superballs
in the cubic and octahedral regimes, respectively. The structural characteristics of the
packings and the affect of the broken symmetry of the superballs are discussed in detail. In
Sec. V, we present concluding remarks. In the Appendix, we briefly outline the procedure to
show that for every specific value of p the constructed packings of two-dimensional superdisks
in Ref. [30] are indeed optimal.


II.     DENSE PACKINGS OF SUPERBALLS VIA COMPUTER SIMULATIONS


      A.   Event-Driven Molecular Dynamics Algorithm for Superballs in the Cubic
Regime


      Recently, Donev, Torquato and Stillinger developed a highly efficient event-driven molec-
ular dynamics packing algorithm [35], which generalizes the Lubachevsky-Stillinger (LS)
sphere-packing algorithm [36] to the case of other centrally symmetric convex bodies (e.g.,
ellipsoids and superballs). Henceforth, we refer to the algorithm as the Donev-Torquato-
Stillinger (DTS) algorithm for convenience. The DTS algorithm works as follows: Initially,
small particles (in our case the superballs) are randomly distributed and randomly oriented
in the simulation box (fundamental cell) with periodic boundary conditions and without any
overlap. The particles are then given translational and rotational velocities randomly and
their motion followed as they collide elastically and also expand uniformly, while the funda-
mental cell deforms to better accommodate the configuration. After some time, a jammed
state with a diverging collision rate γ is reached and the density reaches a local maximum
value.
      In order to generate the densest packing (or a packing close to the densest one) of su-
perballs in the cubic regime (p > 1), a sufficiently slow growth rate is necessary, as verified


                                                 7
                         (a)                                           (b)

FIG. 3: (color online). Dense packings of superdisks (a) and superballs (b) with p = 1.5 gener-
ated via the Donev-Torquato-Stillinger algorithm with the growth rate γ = 10−5 . The packing
densities are φa = 0.9123 . . . and φb = 0.7072 . . ., respectively. One can see that the superdisk
packing is nearly completely crystallized, while the superball packing shows no significant signs of
crystallization. The white “chord” in each superdisk indicates one of its symmetry axis.




              (a)                              (b)                               (c)


FIG. 4: (color online). Illustrations of certain rotational symmetries of the cube and regular
octahedron. (a) Two-fold rotational symmetry of a cube (axis shown coincides with a face diagonal).
(b) Three-fold rotational symmetry of a cube (axis shown coincides with a body diagonal). (c)
Four-fold rotational symmetry of a regular octahedron.




                                                8
by the extensive studies on spheres and circular disks, ellipsoids and ellipses as well as su-
perdisks [22, 30, 37, 38]. In two dimensions, the densest local packing of many centrally
symmetric convex particles (among which circular disks, ellipses and superdisks are of par-
ticular interest) can tessellate the space. The consistency of local and global optima results
in nearly complete crystallization in large packings of these particles [e.g., see Fig. 3(a)].
By contrast, in three dimensions the geometrical frustration of superballs (i.e., the densest
local packing is not consistent with the optimal global packing) makes it very difficult for
the system to follow the equilibrium branch of the phase diagram (without becoming stuck
in any local minima) all the way to the densest packing state, even when small growth rates
are used [e.g., see Fig. 3(b)].
   To resolve this difficulty, one could specify initial configurations that are not random. A
good initial configuration would be unsaturated [39] lattice packings that are hypothesized
to be similar to the optimal lattice packing, which can be obtained by a reasonable guess.
Here we choose to arrange the superballs on the Bravais lattices that provide dense packings
of spheres, such as the face-centered cubic lattice and its stacking variants as well as the
body-centered cubic lattice, with a four-fold rotational symmetry axis of a superball that is
parallel to a coordinate axis.
   Two kinds of highly dense lattice packings of superballs emerge from the simulations [see
Fig. 6(a) and (b)] starting from the unsaturated face-centered cubic packing as the initial
configuration. Subsequent analytical calculations suggested by these simulation results lead
us to the exact construction of two families of Bravias lattice packings, which we call the
C0 - and C1 -lattice packings (so named because they both involve particles with cubic-like
shapes), whose global symmetries are consistent with the two-fold [see Fig 4(a)] and three-
fold rotational symmetry [see Fig. 4(b)] of a superball of the packing, respectively. The
structural and packing characteristics of the C0 - and C1 -lattice packings will be discussed in
detail in Sec. III. We emphasize here that we do not exclude the possibility of the existence of
denser periodic packings with a complex particle basis, although we did not find any of these
packings by running the simulations with a small number of particles in the fundamental
cell which facilitates occurrence of denser periodic packings if they existed [22].




                                              9
   B.   Stochastic Optimization Algorithm for Superballs in Octahedral Regime


   For convex superballs in the octahedral regime (0.5 < p < 1), the prediction of the
collision sequence of particles, an essential step in the DTS algorithm, is numerically unstable
when the particle shape deviates too much from a sphere [see Fig. 2(b)] [40]. Here we
use a novel stochastic optimization packing algorithm [41] to generate dense packings of
convex superballs with octahedral-like shapes. Starting with a given initial configuration,
the positions and orientations of the particles as well as the lattice vectors are considered
as “design variables”, on which the packing density is dependent. Various optimization
techniques could be used to search the design-variable space for a point associated with a
(local) maximum of packing density close to the initial value, subject to the nonoverlapping
conditions. This process is repeated and the packing density is gradually increased until a
global maximum is reached. For superballs, a stochastic optimization technique is employed
whereby random small trial moves in the design-variable space are generated such any move
is accepted if it leads to an increase of the packing density without causing any overlaps,
and is rejected otherwise.
   The final density of the packing generated via the optimization algorithm is sensitively
dependent on the initial configuration. Thus, appropriate choices of initial configurations
are crucial to the determination of the optimal packings. Based on the results of packings
of superdisks and superballs in the cubic regime, it is reasonable to assume that the optimal
packing lattice deforms continuously as the shape of the superball changes, while the group
symmetry of the lattice consistent with the four-fold rotational symmetry of superballs
is preserved. Near the sphere point, we take advantage of the cubic two-fold rotational
symmetry of the FCC lattice by orienting the superballs with their four-fold rotational
symmetry axis parallel to those of the lattice (see Fig. 12). Near the octahedron point,
we use Minkowski’s densest lattice packing for regular octahedra [32] (with the density
φM = 18/19 = 0.9473 . . .) and insert a shrunken superball into each octahedron in the
packing. Note that Minkowski’s lattice packing is the densest known packing of regular
octahedra, which we conjecture to be optimal among all packings of regular octahedra, as
explained in [34]. The unsaturated packings so constructed are used as initial configurations
for the optimization algorithm.
   Two types of highly dense lattice packings emerge from the simulations [see Fig. 6(c)


                                             10
                            1
                                   0.76




                                 0.7595
                           0.9                1.15         1.1525


                       φ                                                          O1-Lattice Packing
                                                                                  O0-Lattice Packing
                                                                                  C0 Lattice-Packing
                           0.8
                                                                                  C1-Lattice Packing



                           0.7
                             0.5          1          1.5      2     2.5       3      3.5    4    4.5   5
                                                                          p

FIG. 5: (color online). Density versus deformation parameter p for the packings of convex super-
balls. Insert: Around p∗c = 1.1509 . . ., the two curves are almost locally parallel to each other.




            (a)                                       (b)                                  (c)             (d)


FIG. 6: (color online). Candidate optimal packings of superballs: (a) The C0 -lattice packing of
superballs with p = 1.8. (b) The C1 -lattice packing of superballs with p = 2.0. (c) The O0 -lattice
packing of superballs with p = 0.8. (d) The O1 -lattice packing of superballs with p = 0.55.


and (d)], which we call the O0 - and O1 -lattice packings, respectively (so named because the
particles have octahedral-like shapes). The packings and their structural characteristics will
be discussed in detail in Sec. IV.




                                                                    11
                           (a)                                       (b)


FIG. 7: (color online). (a) The stretched square-lattice layer of spheres. (b) The stretched lattice
layer of superballs.


III.    OPTIMAL PACKING OF SUPERBALLS IN THE CUBIC REGIME


   A.    The C0 -Lattice Packing


   As suggested by the simulation results, our analysis shows that the densest packings
of superballs with 1 < p < p∗c are given by the C0 lattices, where p∗c = 1.1509 . . . with
φ∗c = 0.7596 . . .. Although the C0 -lattice packings are only apparently optimal for p ∈ (1, p∗c ),
they exist for all p ≥ 1, contrary to the O0 - and O1 -lattice packings of superballs with
octahedral-like shapes, which only exist for certain range of p as discussed below. The
C0 -lattice is obtainable from continuous deformation of the face-centered cubic lattice. In
particular, the FCC lattice packing can be considered as a laminate of square-lattice planar
layers [see Fig. 7(a)]. The planar square-lattice must be stretched along one of its orthogonal
directions so that the superballs in the cubic regime can be arranged on the (stretched)
lattice site with one of its two-fold rotational symmetry axis along the stretched direction
and the other one perpendicular to the plane of the square lattice, as shown in Fig. 7(b).
The magnitude of stretching is determined by the shape of the superballs, thus by the p
value. The stretched layers are then stacked so that the superballs in the top layers can sit
exactly in the “pockets” formed by every four neighboring superballs in the bottom layer.
Thus, each superball has 4 contacting neighbors in its own layers, 4 in the layer above and 4
in the layer below. The layer lamination is continued ad infinitum to construct the packing.


                                               12
FIG. 8: (color online). The C0 lattice for superballs in the cubic regime viewed from the [110]
direction. The structure remains invariant when it is rotated 180◦ about an axis in the [110]
direction, showing its two-fold rotational symmetry.


   The above construction uniquely defines the C0 -lattice packings which possess two-fold
rotational symmetry [see Fig. 8] consistent with that of the superballs [see Fig. 4(a)]. The
lattice vectors for any p value are given by

                        1          1                                                   1
              e1 = 21− 2p i + 21− 2p j,     e2 = 2k,    e3 = −2si + 2(s + 2− 2p )j + k,    (2)

where i, j and k are the unit vectors along the coordinate axis and s is the smallest positive
root of the following equation:

                                        1
                                           2p
                                 s + 2− 2p     + s2p + 2−2p − 1 = 0.                       (3)

   The packing density φmax is given by

                                       Vsb (p)               V (p)
                              φ=                   =          sb         ,               (4)
                                   |e1 × e2 · e3 |   2
                                                           1
                                                       3− 2p
                                                              2s + 2
                                                                        1
                                                                     − 2p


where Vsb (p) is the volume of superballs given by

                                                                            
                                      2         1 2p + 1               1 p+1
                            Vsb (p) = 2 B         ,            B         ,         ,       (5)
                                     p          2p 2p                  2p p
and B(x, y) = Γ(x)Γ(y)/Γ(x + y) and Γ(x) is the Euler Gamma function.



                                                   13
   The packing density φmax as a function of deformation parameter p is plotted in Fig. 5.
The “right” slope of φmax at p = 1 is given by

                                                        
                   π                    1          3          5
        a+ = − √ 24 + ln 8 + 4Ψ             + 2Ψ      − 6Ψ          = 0.3555 . . . ,    (6)
                12 2                    2          2          2
where Ψ(z) = d[ln Γ(z)]/dz is the digamma function. The positive value of a+ indicates that
the initial increase of the packing density is linear in (p − 1). As mentioned before, the C0 -
lattice packings are only optimal for p ∈ (1, p∗c ), beyond p∗c the C1 -lattice packings become
the densest. For p > 1 φmax increases dramatically until it reaches unity as the particle
shapes becomes more like a cube, which is more efficient at filling space than a sphere.
These characteristics stand in contrast to those of the densest known ellipsoid packings,
achieved by certain crystal arrangements of congruent spheroids with a two-particle basis,
whose packing density as a function of aspect ratios has zero initial slope and is bounded
from above by a value of 0.7707 . . . [22]. As we will see in Sec. IV, as p decreases from unity,
the initial increase of φmax is linear in (1 − p). Thus, φmax is a nonanalytic function of p
at p = 1, which is consistent with our conclusions about superdisk packings. However it is
distinctly different from the optimal spheroid packings, for which φmax increases smoothly
as the aspect ratios of the semi-axes vary from unity and hence has no cusp at the sphere
point [22]. The density of congruent ellipsoid packings (not φmax ) has a cusp-like behavior
at the sphere point only when the packings are randomly jammed [42]. The distinction
between the two systems results from different broken rotational symmetries. For spheroids,
the continuous rotational symmetry is only partially broken, i.e., spheroids still possess one
rotationally symmetric axis; and the three coordinate directions are not equivalent which
facilitates dense non-Bravais packings. For superballs, the continuous rotational symmetry
of a sphere is completely broken and the three coordinate directions are equivalently four-
fold rotationally symmetric directions of the particle. Thus, a superball is less symmetric
but more isotropic than an ellipsoid which apparently prefers dense Bravais lattice packings.
The broken symmetry of superballs makes their shapes more efficient in tiling space and
thus results in a larger and faster increase in the packing density.
   At p = p∗c = 1.1509 . . ., the two lattice packings have the same density φ∗c = 0.7596 . . .
and superballs with p∗c possess a two-fold degenerate crystalline maximal density state. The
C0 and C1 lattices have distinct group symmetries, thus the optimal packing “jumps” from
one structure to another leading to another nonanalytic point in φmax . This behavior is

                                              14
similar with that of optimal superdisk packings.


   B.    The C1 -Lattice Packing


   For superballs with p ≥ p∗c the densest packings are given by the C1 lattices with three-
fold rotational symmetry consistent with that of the superballs, see Fig. 6(b) and Fig. 10.
Note though the C1 -lattice packings are only apparently optimal when p ≥ p∗c , they also
exist for all p ≥ 1. In the packing, each superball has 12 contacting neighbors, among which
6 contacting points are the edge centers and the other 6 are along the surface diagonals, as
schematically shown in Fig. 9. At p = 1, this local packing (the central particle and its 12
neighbors) possessing three-fold rotational symmetry is just the building block of the face-
centered cubic lattice packing of spheres. As p increases from unity, the continuous rotational
symmetry of a sphere is broken while the three-fold rotational symmetry of the local packing
could still be maintained since “cubic” superballs still possess three-fold rotational symmetry
[see Fig. 4(b)]. Although the edge contacting points will remain at the centers of the edges,
the surface contacting points will continuously follow a path along the surface diagonals as
p changes from unity to infinity. As p approaches infinity, the surface contacting points will
approach the surface centers; when the superballs becomes a perfect cube at p = ∞, the
contacting points are degenerate, i.e., the entire edges and surfaces of neighboring particles
contact each other, respectively.
   The three-fold rotational symmetry of the local packing together with the requirement
that each particle has 12 contacting neighbors uniquely determine the global packing lattice.
And the packing lattice for a specific p value can be obtained by continuously deforming the
face-centered cubic lattice. In particular, the lattice vectors of the C1 are given by


                  1          1                1         1                      1
        e1 = 21− 2p i + 21− 2p j,   e2 = 21− 2p i + 21− 2p k,   e3 = 2(s + 2− 2p )i − 2sj − 2sk,   (7)

where s is the smallest positive root of the following equation:

                                             1
                                                2p
                                      s + 2− 2p     + 2s2p − 1 = 0.                                (8)

The packing density is readily computed from



                                                   15
                              (a)                                   (b)


FIG. 9: (color online). Contacting points of the a sphere (a) and a schematic superball (shown
as a cube) (b). The view is along the [111] direction. The surface contacting points (blue) will
continuously move along the surface diagonals as the p value changes from unity to infinity. Every
contacting point has a symmetric image about the center of the superball and their distributions
have three-fold rotational symmetry.



                                        Vsb (p)              V (p)
                          φmax =                    =        sb       ,                     (9)
                                    |e1 × e2 · e3 |       1          1
                                                      23− p 3s + 2− 2p

where Vsb (p) is the volume of a superball with deformation parameter p as given by Eq. (5).
The packing density φmax is shown in Fig. 5.
   As shown in Fig. 11(a), a sequence of superballs contacting each other through the centers
of edges can be considered as a chain which serves as the basic building block of the packing
structure. In contrast to the FCC packing of spheres in which the dense layers constructed
by stacking the chains of spheres are parallel to one coordinate plane; for superballs with
p 6= 1, the chains are shifted relative to each other and the normal direction of the layer
containing the centers of superballs does not coincide with the coordinate directions. In this
way, a lattice of “pockets” is formed in which the particles in the layer above can be exactly
fitted to construct the C1 -lattice packing, as illustrated in Fig. 11 (b) and (c).




                                               16
FIG. 10: (color online). The C1 lattice for superballs in the cubic regime viewed from the [111]
direction. The thin dark lines show the three orthogonal directions, which clearly exhibits the
3-fold rotational symmetry of the structure.




                (a)                             (b)                              (c)


FIG. 11: (color online). The C1 -lattice packing of superballs obtained by stacking superball chains:
(a) The chain as depicted in the text. (b) The layer constructed by stacking the chains. (c) The
packing obtained by stacking the layers.


IV.     OPTIMAL PACKINGS OF SUPERBALLS IN THE OCTAHEDRAL REGIME


   A.    The O0 -Lattice Packing


   As p decreases from unity, the continuous rotational symmetry of a sphere is broken and
a superball has an octahedral-like shape [see Fig. 2(b)]. The O0 lattice [see Fig. 6(c)] also
can be considered as a continuous deformation of the face-centered cubic lattice. As before,


                                               17
                           (a)                                       (b)


FIG. 12: (color online). (a) Face-centered cubic packing of spheres, viewed as a laminate of face-
centered square layers from the [001] direction. (b) Similar laminate of face-centered square planar
layers of superballs in the octahedral regime, viewed from the [001] direction.


we start from the FCC packing , viewed as a laminate of square-lattice planar layers of
spheres, as illustrated in Fig. 12(a). We similarly construct layers of superballs by orienting
one of the four-fold rotationally symmetric axis along the normal of the layer [see Fig. 4(c)],
and aligning the other two of each superball so that the square symmetry of cross-sections
of superballs in the layer is consistent with that of the layer, as shown in Fig. 12(b). The
layers are stacked so that the superballs in the top layers can exactly sit in the holes formed
in the bottom layer. The layer lamination is then continued ad infinitum to generate the
packing.
   In the O0 -lattice packing, each superball has 4 contacting neighbors in its own layer, 4
in the layer above and 4 in the layer below. The lattice vectors for any specific p can be
uniquely determined by the symmetry and contacting requirements. i.e.,

                                                                       1
                   e1 = 2i,      e2 = 2j,      e3 = i + j + 2 1 − 21−2p 2p k.                  (10)

As the shape of a superball deviates more from a sphere, the holes in the layer become
larger and the distance between successive layers becomes smaller. In the limit that the
superballs become octahedra (p = 0.5), the planes of two successive layers coincide with
each other. However, the distance between every other layer cannot be smaller than 2,
which is the nearest distance between centers of two superballs aligned along one of the


                                               18
coordinate directions. As p decreases from unity, there exists a point p∗o where the particles
of every other layer contact each other, forming “cages” for the particles of the layer in
between. The value of p∗o can be obtained from the relation.

                                                 1
                                      2 1 − 21−2p 2p − 1 = 0,                                     (11)

and we have p∗o = ln 3/ ln 4 = 0.7924 . . . with the corresponding packing density φ∗o =
0.7959 . . .. If p decreases further (i.e., p < p∗o ), the “cages” will be too large for the superballs
to maintain 12 contacts and the packing density would decrease.
   Thus, the O0 lattice only gives the densest known packings of superballs in the vicinity
left of the sphere point, i.e., p∗o < p < 1. The packing density is given by

                                          Vsb(p)             Vsb (p)
                             φmax =                   =                 1 ,                       (12)
                                      |e1 × e2 · e3 |   8 (1 − 21−2p ) 2p
where Vsb (p) is the volume of a superball given by Eq. (5). Packing density φmax as a function
of p is plotted in Fig. 5 (the branch with p∗o < p < 1). The “left” slope of φmax at p = 1 is
given by


                                             
             π                  1        3        5
     a− = − √ ln (64) + 8 + 4Ψ     + 2Ψ     − 6Ψ      = −0.02941 . . . .                          (13)
           12 2                 2        2        2

Thus, the initial increase of the packing density as p decreases from unity is linear in (1 −
p). As pointed out in the previous section, the linear dependence on |p − 1| indicates the
nonanalyticity of φmax at p = 1, resulting from the broken symmetry of superballs which
is distinctly different from other known hard particle systems such as ellipsoids in three
dimensions. Note that the magnitude of a− is smaller than a+ , implying that superballs in
the cubic regime are more efficient at filling space than superballs in the octahedral regime,
as can be also seen in the limiting cases: cubes can tile space while the densest known
packing of regular octahedra covers about 94.74% of the space. The fact that the density
of the O0 lattice packing begins to decrease when p < p∗o suggests the existence of packings
with different symmetry that would be optimal near the octahedron point.




                                                19
                (a)                            (b)                             (c)


FIG. 13: (color online). Projections of a O1 -lattice sub-packing on three orthogonal coordinate
planes: (a) Projection on the (001) plane. (b) Projection on the (010) plane. (c) Projection on the
(100) plane.


   B.   The O1 -Lattice Packing


   In particular, the densest known packing of regular octahedra, defined by |x1 | + |x2 | +
|x3 | ≤ 1, is achieved by a Bravais lattice packing with the lattice vectors [33]

                   2   2   2                1   4   1              1   1   4
               e1 = i + j − k,        e2 = − i + j − k,        e3 = i − j − k.                (14)
                   3   3   3                3   3   3              3   3   3
This packing, with density φM = 18/19 = 0.9473 . . ., was discovered by Minkowski [32]. By
perturbing the Minkowski lattice packing using the method depicted in Sec. II.B, we are able
to identify a family of highly dense packings of superballs near the octahedron point, i.e.,
the O1 -lattice packing [see Fig. 6(d)]. As shown in Fig. 13, the projections of the O1 -lattice
packing on the three orthogonal coordinate planes possess certain translational symmetry in
two dimensions. The translational vectors are along (i + j) direction for (001) plane, along
(i + k) and (k − i) directions for (010) plane and along (k − j) direction for (100) plane. The
magnitude of the translational vectors are functions of p, which can be determined with the
additional condition that each particle has 12 contacting neighbors. Thus, we obtain the
lattice vectors for the O1 , i.e.,


            e1 = 2li + 2lj − 2lk,    e2 = −2qi + 2sj − 2qk,     e3 = 2qi − 2qj − 2sk,         (15)



                                               20
where l, s and q are given by the following equations

                                       1
                               l = 3− 2p ,     2q 2p + s2p − 1 = 0,
                                                                                             (16)
                           (l + q)2p + (s − l)2p + (l − q)2p − 1 = 0.
At the limit p = 0.5, Eq. (15) reduces to Eq. (14).
   As p increases from 0.5, the superballs deviate more and more from regular octahedra
and it becomes more difficult to maintain 12 contacts for each particle and simultaneously
to keep the translational symmetry of the projected packings. Interestingly, as p exceeds
p∗o = ln 3/ ln 4, Eq. (16) will have no real roots, indicating that the symmetry and contacting
conditions could not be satisfied at the same time beyond p∗o . Thus, the O1 lattice gives
the densest known packings of superballs near the octahedron point, i.e., 0.5 < p < p∗o .
At p∗o , the O0 - and O1 -lattice packings have exactly the same density, i.e., φ∗o = 0.7959 . . .
and superballs with p = p∗o possess a two-fold degenerate crystalline maximal density state.
Note that the O0 and O1 lattices possess distinct symmetries, as p passes p∗o the apparently
optimal packing “jumps” from one lattice to the other, which results in one more nontrivial
nonanalytic point in φmax . This additional nonanalytical point does not exist for superdisk
packings. Nor does similar behavior exist for any other known hard-particle systems.
   We emphasize that the O1 - and O0 -lattice packings are separately constructed from the
FCC packing of spheres which has been proved to be optimal, and from the Minkowski
packing – the densest known packing of regular octahedra, respectively. The amazing fact
that the two families of packings both terminate at p∗o with the same density suggests
that these packings are very likely optimal, although we could not completely exclude the
possibility that a periodic packing with a complex particle basis might have a higher density
over an interval including p∗o . In other words, the existence of the continuous “path” of
superball packings that we found connecting the FCC lattice packing of spheres and the
Minkowski lattice packing of regular octahedra given the optimal packings of two limiting
particle shapes strongly suggests that the packings along the path are also optimal.
   The packing density φmax is given by

                                          Vsb (p)          Vsb (p)
                             φmax =                   =                ,                     (17)
                                      |e1 × e2 · e3 |   8l(3q 2 + s2 )
where Vsb (p) is the volume of a superball given by Eq. (5). The plot of φmax as a function
of p is shown in Fig. 5 (the branch with 0.5 < p < p∗o ). The packing structure could also be

                                               21
                (a)                             (b)                              (c)


FIG. 14: (color online). The O1 -lattice packing of superballs obtained by stacking superball chains:
(a) The superball chain. (b) The layer constructed by stacking the chains. (c) The packing obtained
by stacking the layers.




FIG. 15: (color online). Density versus deformation parameter p for the packings of concave
superballs. Insert: a concave superball with p = 0.1, which will becomes a three-dimensional cross
at the limit p → 0.


considered as the stacking of superball chains, as illustrated in Fig. 14.


   C.   Generalization to Concave Superballs


   As p decreases from 0.5, the superballs become concave particles, but they still possess
octahedral-like shapes [see Fig. 2(a)]. The lack of simulation techniques to generate concave
superball packings make it very difficult to find the optimal packings for the entire range

                                               22
of concave shapes (0 < p < 0.5). However, based on our conclusions for convex superball
packings, we conjecture that near the octahedron point, the optimal packings possess similar
translational symmetry in two dimensions to that of the O1 -lattice packing. By inserting
into each octahedron in the Minkowski packing a concave superball, we are able to obtain
a family of packings that are dense near p = 0.5 but not optimal, the density of which is
shown in Fig. 15. The packings could be densified a little by carefully adjusting the particles
to minimize the exclusion volume effects. However, the adjustments are difficult to quantify.
     It is interesting to point out that at the limit p → 0, one can construct zero-length
“chains” of a infinite number of “crosses” along the [111] (or any equivalent) direction. In
other words, the centers of “crosses” packed along the chain are infinitely close to each
other. This aligning effect, which appears in three dimensions but not in two dimensions,
suggests that near the “cross” point, the similarly constructed chains of superballs might be
a reasonable building block to produce dense packings.


V.     CONCLUSIONS


     In this paper, we have constructed the densest known packings of convex superballs based
on symmetry and contacting requirements. For superballs in the cubic regime (p > 1), the
candidate optimal packings are achieved by the C0 - and C1 -lattice packings possessing two-
fold and three-fold rotational symmetry, respectively, which can both be considered as a
continuous deformation of the FCC lattice. For convex superballs in the octahedral regime
(0.5 < p < 1), the O1 - and O0 -lattice, obtainable from continuous deformation of the FCC
lattice keeping its four-fold rotational symmetry, and from the Minkowski lattice for regular
octahedra [32] keeping the translational symmetry of the projected lattice on the coordinate
planes, are apparently optimal in the vicinity of the sphere- and the octahedron-point,
respectively. The packings jump between distinct lattices as p passes p∗c and p∗o , leading to
two nontrivial nonanalytic points in φmax .
     The existence of the continuous “path” of superball packings that we found connecting
the FCC lattice packing of spheres and the Minkowski lattice packing of regular octahedra
provides strong evidence that our candidate packings are very likely optimal. For concave
superballs, we constructed a family of dense packings based on the Minkowski lattice and dis-
cussed an interesting aligning effect. Moreover, we have shown that as p changes from unity,


                                              23
there is a significant increase of the maximal packing density φmax , which is initially linear in
|p − 1| resulting in the nonanalytic behavior of φmax at the sphere point. Interestingly, this
three-dimensional behavior is consistent with the fact that there is an exponential improve-
ment on the lower bound on φmax of superballs relative to that for spheres in arbitrarily
high dimensions as found by Elkies, Odlyzko and Rush [27]. The packing characteristics of
superball packings are much richer than those of superdisks, and the nontrivial influences of
the broken symmetry are distinctly different from the other known aspherical packings, such
as ellipsoid packings. Although the anisotropic shape of the particle allows for the possibility
of local arrangements with larger coordination numbers, in the candidate optimal packings
each superball maintains twelve contacting neighbors for all values of p, in contrast to the
densest known ellipsoid packings in which each particle has fourteen contacting neighbors.
   The optimal Bravais lattice packings of convex superballs for a particular value of p are
also the corresponding dense crystal phase states of superballs in equilibrium. Therefore,
our findings provide a starting point to quantify the entire equilibrium phase behavior of
superball systems, which should deepen our understanding of the statistical thermodynam-
ics of non-spherical particle systems [44, 45, 46]. Ideally, one would expect a first-order
disorder-order phase transition of superball systems for every value of p. However, the ki-
netic difficulty of such a transition increases with the geometrical frustrations introduced
by the particles. In practice, the disordered metastable states could frequently occur, as
illustrated in Fig. 3(b). Some preliminary investigations that we have carried out show
that disordered superball packings are hypoconstrained, i.e., the average contact number is
smaller than twice of the number of degrees of freedom of the particles [47]. A rotational
transition is also possible, i.e., the rotational degrees of freedom of the particles are suddenly
frozen when the packing density exceeds a certain threshold value. A unique feature of su-
perball systems is that symmetry transitions occur at p∗c and p∗o . Thus for particles with a
deformation parameter close to p∗c or p∗o , multi-morphological maximal density states might
be found.
   Moreover, the optimal packings of convex superballs are significantly denser than optimal
sphere packings when p deviates considerably from unity; even the disordered packings could
have a densities close to φmax of spheres. This suggests that one could use particles with
shapes similar to that of superballs in situations where dense packings are favored, such as
in certain powder sintering processes. We also note that superballs can be mass produced

                                              24
FIG. 16: (color online). A superdisk circumscribed by a hexagon formed from three pairs of parallel
lines.

using modern lithography techniques, which would enable one to prepare and study superball
packings experimentally.
   In the future, we will generalize the current work to the study of disordered packings of
superdisks and superballs and further explore the effect of broken rotational symmetry. It
will be also interesting to understand the “jamming” characteristics [43, 47] of both random
and crystalline packings of these particles.


   APPENDIX A: OPTIMALITY OF THE SUPERDISK PACKINGS FOUND IN
REF. [30]


   In this section, we briefly outline the procedure used to verify that for every specific value
of p > 0.5 the constructed packings of superdisks in two dimensions in Ref. [30] are indeed
optimal, by virtue of Fejes Toth’s theorem [12, 13] described in Sec. I. In particular, Fejes
Toth’s theorem states that the densest packing of any centrally symmetric convex body in
two dimensions is always given by the smallest hexagon that circumscribes the body. Since
the body is centrally symmetric, the hexagon is as well and therefore it tiles R2 . Fejes Toth’s
theorem also implies that the optimal packing for any two-dimensional centrally symmetric
body is a Bravais lattice packing. Thus, the problem of finding the optimal packing reduces
to finding the circumscribing hexagon of a superdisk with minimum area.
   Let a superdisk be circumscribed by three pairs of parallel lines forming a hexagon, as
                                                                                          (i)   (i)
shown in Fig. 16. Denote the common tangent points by Mi with the coordinates (m1 , m2 )


                                               25
(i = 1, ..., 6). Since the particle is centrally symmetric, Mi and Mi+3 (i = 1, 2, 3) are also
                                     (i)         (i+3)
symmetric about the center, i.e., mj = −mj               (j = 1, 2).
   From the common tangent conditions, one can write down the equations of the parallel
                                       (i)
lines in terms of the coordinates mj (i = 1, ..., 6, j = 1, 2), from which the vertices of
the hexagon as intersections of different pairs of lines can be obtained. Thus, the area of
                                                               (i)         (1)   (6)
the hexagon is readily expressed as a function of mj , i.e., S(m1 , ..., m2 ). By solving the
following optimization problem

                                                         (1)         (6)
                                Minimize :        S(m1 , ..., m2 ),
                                           (i)        (i)
                                                                                             (A1)
                     Subject to :    |m1 |2p + |m2 |2p = 1, (i = 1, ..., 6);
one can find the smallest hexagon circumscribing the particle and thus verify for every
specific p > 0.5, the packings given in Ref. [30] are indeed optimal.


   ACKNOWLEDGMENTS


   The authors would like to thank Aleksandar Donev, Martin Henk and Greg Kuperberg
for valuable discussions. S. T. thanks the Institute for Advanced Study for its hospitality
during his stay there. This work was supported by the Division of Mathematical Sciences at
the National Science Foundation under Award Number DMS-0804431 and by the MRSEC
Program of the National Science Foundation under Award Number DMR-0820341.




 [1] R. Zallen, The Physics of Amorphous Solids (Wiley, New York, 1983).
 [2] P. M. Chaikin and T. C. Lubensky, Principles of Condensed Matter Physics (Cambridge
    University Press, New York, 2000).
 [3] I. C. Kim and S. Torquato, J. Appl. Phys. 69, 2280 (1991); S. Torquato, J. Mech. Phys. Solids
    46, 1411 (1998); M. C. Rechtsman and S. Torquato, J. Appl. Phys. 103, 084901 (2008).
 [4] S. Torquato, Random Heterogeneous Materials: Microstructure and Macroscopic Properties
    (Springer-Verlag, New York, 2002).
 [5] T. Zohdi, Int. J. Numer. Meth. Eng. 76, 1250 (2008).
 [6] S. F. Edwards, Granular Matter (Ed. A. Mehta, Springer-Verlag, New York, 1994).



                                                 26
 [7] W. D. Callister, Materials Science and Engineering: An Introduction, 7th Edition (Wiley,
     New York, 2006).
 [8] J. Liang and K. A. Dill, Biophys J. 81, 751 (2001).
 [9] J. W. S. Cassels, An Introduction to the Geometry of Numbers (Springer-Verlag, Berlin, 1959).
[10] J. H. Conway and N. J. A. Sloane, Sphere Packings, Lattices and Groups (Springer, Berlin
     Heidelberg New York, 1987).
[11] C. E. Shannon, Bell System Tech. J. 27, 379 (1948); ibid., 623 (1948).
[12] L. Fejes Tóth, Regular Figures (Macmillan, New York, 1964).
[13] J. Pach and P. K. Agarwal, Combinatorial Geometry (Wiley-Interscience, New York, 1995).
[14] T. C. Hales, Ann. Math. 162, 1065 (2005).
[15] H. Cohn and N. Elkies, Ann. Math. 157, 689 (2003).
[16] G. Parisi and F. Zamponi, J. Stat. Mech.: Theory Exp. P03017 (2006).
[17] S. Torquato and F. H. Stillinger, Exp. Math. 15, 307 (2006).
[18] G. Parisi, J. Stat. Phys. 132, 207 (2008).
[19] A. Scardicchio, F. H. Stillinger, and S. Torquato, J. Math. Phys. 49, 043301 (2008).
[20] Supramolecular chemistry deals with the chemistry and collective behavior of molecular build-
     ing blocks that are organized on large length scales (relative to molecular sizes) with long-range
     order.
[21] A. I. Kitaigorodskii, Molecular Crystal and Molecules, (Academic Press, New York, 1973).
[22] A. Donev, F. H. Stillinger, P. M. Chaikin, and S. Torquato, Phys. Rev. Lett. 92, 255506
     (2004).
[23] J. H. Conway and S. Torquato, Proc. Nat. Acad. Sci. 103, 10612 (2006).
[24] P. Chaikin, S. Wang, and A. Jaoshvili, Abstract submitted to APS March Meeting (2007).
[25] E. R. Chen, Discrete Comput. Geom. 40, 214 (2008).
[26] It is highly likely that the largest density of tetrahedral packings reported in Ref. [25] can be
     improved.
[27] N. D. Elkies, A. M. Odlyzko, and J. A. Rush, Invent. math. 105, 613 (1991).
[28] There is a fundamental distinction between the shapes of superball surfaces in the octahedral-
     like regime (0 ≤ p < 1) and the cubic-like regime (1 < p ≤ +∞). The former display a set
     of linear loci along which a principal curvature diverges, representing a generalization of the
     edge set for the true octahedron at p = 1/2. No such loci of diverging curvature exist for the


                                                  27
    cubic-like regime, except in the limit p → +∞.
[29] Two polyhedra are dual to each other if the vertices of one correspond to the faces of the
    other.
[30] Y. Jiao, S. H. Stillinger, and S. Torquato, Phys. Rev. Lett. 100, 245504 (2008).
[31] J. A. Rush, Invent. Math. 98, 499 (1989).
[32] H. Minkowski, Nachr. K. Ges. Wiss. Göttingen, Math.-Phys. KL, 311 (1904).
[33] U. Betke and M. Henk, Comput. Geom. 16, 157 (2000). This paper reports the densest Bravais
    lattice packings of a number of different three-dimensional polyhedra.
[34] The regular octahedron is centrally symmetric. In the densest octahedral lattice packing found
    by Minkowski [32], the octahedra have the maximal number of face-to-face contacting neigh-
    bors, which significantly reduces the free volume. This observation together with the results
    of our optimization simulations described in the text strongly suggests that the Minkowski
    lattice packing of regular octahedra is optimal among all packings of octahedra, which we
    conjecture to be the case.
[35] A. Donev, S. Torquato, and F. H. Stillinger, J. Comput. Phys. 202, 737 (2005).
[36] B. D. Lubachevsky and F. H. Stillinger, J. Stat. Phys. 60, 561 (1990).
[37] S. Torquato, T. M. Truskett, and P. G. Debenedetti, Phys. Rev. Lett. 84, 2064 (2000).
[38] A. R. Kansal, S. Torquato, and F. H. Stillinger, Phys. Rev. E 86, 041109 (2002).
[39] In a saturated packing, there is no space available to add another particle to the packing.
[40] A. Donev, Jammed Packings of Hard Particles, Ph.D. Thesis, Princeton University, 2006.
[41] Y. Jiao and S. Torquato, in preparation.
[42] A. Donev, I. Cisse, D. Sachs, E. A. Variano, F. H. Stillinger, R. Connelly, S. Torquato, and
    P. M. Chaikin, Science 303, 990 (2004).
[43] S. Torquato and F. H. Stillinger, J. Phys. Chem. B 105, 11849 (2001).
[44] K. W. Wojciechowski and D. Frenkel, Comput. Methods Sci. Technol. 10, 235 (2004).
[45] A. Donev , J. Burton, F. H. Stillinger, and S. Torquato, Phys. Rev. B 73, 054109 (2006).
[46] G. Yatsenko and K. S. Schweizer, Langmuir 24, 7474 (2008).
[47] A. Donev, R. Connelly, F. H. Stillinger, and S. Torquato, Phys. Rev. E 75, 051304 (2007).




                                                28
     1




    0.9

φ                  C-Lattice Packi
                    *
                   C -Lattice Pack
    0.8




    0.7
       1   2   3           4
               p
