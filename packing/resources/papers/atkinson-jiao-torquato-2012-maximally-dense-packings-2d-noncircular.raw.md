                                                         Maximally dense packings of two-dimensional convex and concave noncircular
                                                                                          particles
                                                                                                         Steven Atkinson
                                                                                    Department of Mechanical and Aerospace Engineering,
                                                                                   Princeton University, Princeton, New Jersey 08544, USA

                                                                                                            Yang Jiao
arXiv:1405.0245v1 [cond-mat.stat-mech] 1 May 2014




                                                                                Princeton Institute for the Science and Technology of Materials,
                                                                                   Princeton University, Princeton, New Jersey 08544, USA

                                                                                                       Salvatore Torquato
                                                                   Department of Chemistry, Department of Physics, Princeton Center for Theoretical Science,
                                                                                    Program of Applied and Computational Mathematics,
                                                                               Princeton Institute for the Science and Technology of Materials,
                                                                                  Princeton University, Princeton New Jersey 08544, USA
                                                                                                  (Dated: November 13, 2021)
                                                                   Dense packings of hard particles have important applications in many fields, including con-
                                                                densed matter physics, discrete geometry and cell biology. In this paper, we employ a stochastic
                                                                search implementation of the Torquato-Jiao Adaptive-Shrinking-Cell (ASC) optimization scheme
                                                                [Nature (London) 460, 876 (2009)] to find maximally dense particle packings in d-dimensional Eu-
                                                                clidean space Rd . While the original implementation was designed to study spheres and convex
                                                                polyhedra in d ≥ 3, our implementation focuses on d = 2 and extends the algorithm to include both
                                                                concave polygons and certain complex convex or concave non-polygonal particle shapes. We verify
                                                                the robustness of this packing protocol by successfully reproducing the known putative optimal
                                                                packings of congruent copies of regular pentagons and octagons, then employ it to suggest dense
                                                                packing arrangements of congruent copies of certain families of concave crosses, convex and concave
                                                                curved triangles (incorporating shapes resembling the Mercedes-Benz logo), and “moon-like” shapes.
                                                                Analytical constructions are determined subsequently to obtain the densest known packings of these
                                                                particle shapes. For the examples considered, we find that the densest packings of both convex and
                                                                concave particles with central symmetry are achieved by their corresponding optimal Bravais lattice
                                                                packings; for particles lacking central symmetry, the densest packings obtained are non-lattice pe-
                                                                riodic packings, which are consistent with recently-proposed general organizing principles for hard
                                                                particles. Moreover, we find that the densest known packings of certain curved triangles are periodic
                                                                with a four-particle basis, and we find that the densest known periodic packings of certain moon-like
                                                                shapes possess no inherent symmetries. Our work adds to the growing evidence that particle shape
                                                                can be used as a tuning parameter to achieve a diversity of packing structures.

                                                                PACS numbers: 61.50.Ah, 05.20.Jj


                                                                    I.   INTRODUCTION                               lapping particles), especially of congruent copies of con-
                                                                                                                    vex particles [16–21]. Perhaps the simplest characteristic
                                                                                                                    of a packing is its packing density, φ, which is, intuitively
                                                       The problem of packing nonoverlapping particles in d-
                                                                                                                    speaking, the fraction of the plane covered by the parti-
                                                    dimensional Euclidean space Rd has been of interest in
                                                                                                                    cles. It is well known that the triangular lattice is the
                                                    discrete mathematics and geometry for centuries. One
                                                                                                                    densest packing
                                                                                                                                  √ of congruent circles, and its packing den-
                                                    overarching aim is to ascertain organizing principles that
                                                                                                                    sity is φ = π/ 12 = 0.906899 . . . [22]. Other simple two-
                                                    govern the nature of dense packings of various shapes [1]
                                                                                                                    dimensional shapes that have been studied include the
                                                    in order to better understand many natural phenomena,
                                                                                                                    class of regular polygons and related variations. For ex-
                                                    including liquid, glassy and crystalline states of matter
                                                                                                                    ample, it is known that the densest packing of congruent
                                                    [2–5]; heterogeneous materials [4]; crystalline polymers
                                                                                                                    regular octagons   √is the
                                                                                                                                             optimal Bravais lattice packing
                                                    [6, 7]; and biological systems [8–10]; to name a few. In                   
                                                                                                                    with φ = 4(3 − 2) /7 = 0.906163 . . . . When the cor-
                                                    two dimensions, the packing of hard particles has im-
                                                                                                                    ners of the octagon are all appropriately “smoothed” into
                                                    plications for understanding the behavior and structures
                                                                                                                    hyperbolic curves, the resulting “smoothed octagon” is
                                                    found in thin films [11], adsorption of molecules on sub-
                                                                                                                    conjectured to possess the lowest optimal packing density
                                                    strates [12, 13], and the organization of epithelial cells
                                                                                                                    among all convex,√ centrally-symmetric
                                                                                                                                                  √            particle shapes,
                                                    [14, 15].
                                                                                                                    with φ = (8 − 4 2 − ln 2)/(2 2 − 1) = 0.902414 . . . [23].
                                                       In the two-dimensional Euclidean plane R2 , consider-        Another simple yet interesting case is the regular pen-
                                                    able effort has been devoted to study and characterize          tagon, which has a putative maximum packing density
                                                    packings (roughly speaking, large collections of nonover-
                                                                                                                        2
              √
of φ = (5 − 5)/3 = 0.921311 . . . , given by its densest      and other particle shapes. We then offer conclusions and
(non-Bravais) double-lattice packing [24–27].                 plans for future work. In addition, an appendix includes
   Generally, it has been shown independently by both         some additional numerical results, and the Supplemental
Fejes Tóth [18] and Rogers [17] that the densest pack-       Material contains mathematical details for many of the
ing of congruent copies of any convex, two-dimensional        packing structures presented in this work[33].
shape possessing central symmetry is achieved by a lat-
tice structure. Fejes Tóth [28] and Mahler [29] also
proved that such a construction must                                            II.   DEFINITIONS
                                     √ be able to achieve
a packing density of at least φ = 3/2 = 0.866025 . . .
for any convex shape. Moreover, Kuperberg and Kuper-             In order to make precise the problem that will be
berg showed that, for any convex shape (with or with-         addressed, we introduce some mathematical definitions.
out central symmetry), a double-lattice
                              √           packing may be      First, we define a particle, S, to be a closed, simply-
constructed, also with φ ≥ 3/2, and conjectured that          connected set in R2 that may be either concave or con-
the densest double-lattice packing realizes the maximum       vex. The boundary of the set is denoted as Γ. A special
packing density for shapes such as regular pentagons and      case of convexity is strict convexity, denoting a convex
heptagons while asking if this might extend to all regular    boundary that contains no line segments. The area of S
polygons with an odd number of sides [25].                    is denoted by a1 , and we will henceforth assume that this
   In the present work, we use a two-dimensional stochas-     quantity is bounded.
tic search implementation of the Torquato-Jiao Adaptive          Given two linearly independent (column) vectors λ1
Shrinking Cell (ASC) packing method, originally imple-        and λ2 , the lattice generated by λ1 and λ2 is defined
mented in three and higher dimensions in Refs. [30–32],       as the set {iλ1 + jλ2 ∀i, j ∈ Z}. A packing, P is de-
to generate the densest known packings of a variety of        fined as a collection of particles {Si } whose interiors are
nontrivial convex and concave noncircular particles. The      mutually disjoint. If all members of P are translates of
ASC scheme generates dense packings by rearranging a          each other where the vectors of translation form a lat-
nonoverlapping configuration of particles within a peri-      tice, P is known as a Bravais lattice (or, simply, lattice)
odic Fundamental Cell (FC) whilst decreasing its volume       packing. Furthermore, if P can be decomposed into the
to increase the packing density. Our current implemen-        union of two distinct lattice packings P0 and P1 , such
tation of the ASC scheme expands upon the previous one        that an inversion about some point in the plane inter-
by detecting overlaps between any concave polygons and        changes P0 and P1 , then P is called a double-lattice pack-
certain smoothly shaped convex and concave nonspheri-         ing. Generally, if one can decompose P into the union of
cal particles. This allows us to readily investigate dense    N ≥ 1 distinct lattice packings, each sharing the same
packings of a wide spectrum of nontrivial nonspherical        lattice vectors, then P is said to be a periodic packing
particles in the plane that exhibit unique packing behav-     with an N -particle basis. Also, for all periodic packings,
iors.                                                         there exists a fundamental cell (FC) of the packing, par-
   In this paper, we study the dense packing behavior of      allelogrammatic in shape, described by a lattice matrix
several families of noncircular particle shapes including     Λ = {λ1 , λ2 }, inside which all N centroids lie. Exam-
so-called “fat crosses”, convex and concave “curved tri-      ples of lattice and periodic packings are given in Figure
angles” (incorporating shapes resembling the Mercedes-        1. Note that, in a lattice packing, all particles must have
Benz logo), and “moon-like” shapes. We then use the           the same orientation, whereas, in a general periodic pack-
results of the ASC algorithm to inform analytical con-        ing, the N particles in the FC are free to have their own
structions of the densest known packings of those parti-      orientations.
cle shapes considered, recovering several well-known re-         The packing density, φ, defined for a given P is, in-
sults, then moving onward to study other particle shapes.     tuitively speaking, the fraction of the plane covered by
Specifically, we find that the densest packings of certain    the copies of S. When it is assumed that P is a periodic
curved triangles are periodic with a four-particle basis.     packing with an N -particle basis,
Also, we find that the densest periodic packings of certain                                 N a1
moon-like shapes possess no inherent symmetries. Our                                  φ=                              (1)
                                                                                           Area(F )
work adds to the growing evidence that particle shape
can be used as a tuning parameter to achieve a diversity      , where a1 denotes the area of a single particle, and
of packing structures.                                        Area(F ) denotes the area of the FC. If φ = 1, then P
   The rest of this paper is organized as follows: in Sec.    is said to be a tiling.
II, we will introduce the mathematical definitions that
are necessary for a rigorous treatment of the packing
problem; in Sec. III, we review the ASC scheme and            III.   TORQUATO-JIAO ADAPTIVE SHRINKING
discuss our contributions to the method; in Sec. IV, we              CELL (ASC) OPTIMIZATION SCHEME
introduce the particle shapes whose packing behavior we
have studied; and in Sec. V, we discuss a number of             The Torquato-Jiao Adaptive Shrinking Cell (ASC) op-
results in packing congruent copies of both well-known        timization scheme seeks to generate dense packings of a
                                                                                                                                            3

                                                                                     During the “random movements” step, every particle
                                                                                  in the basis is either translated or rotated within some
                                                                                  prescribed limits on the magnitude of the movement. If
                                                                                  the new position of the particle does not cause it to over-
                                                                                  lap with any other particles in the FC (or their periodic
                                                                                  images), the move is kept; otherwise, the move is rejected
                                                                                  and the particle remains where it began. Note that only
                                                                                  one particle is moved at a time; collections of particles
                                                                                  never move simultaneously during this step. The process
                                                                                  is repeated a specified number of times for each particle
                                                                                  to explore the configurational space of the packing; the
                  (a)                                         (b)                 precise number is determined empirically based on the
                                                                                  criterion that the particles are allowed to equilibrate be-
FIG. 1: (Color online) Examples of a lattice packing (a)                          fore attempting to strain the FC. In the present work, at
 and periodic packing with four-particle basis (b). The                           least 500 trial movements are attempted for each particle
lattice parallelogram is shown by the black grid behind                           at each occurrence of this step, and this number remains
                      the particles.                                              constant for the duration of the simulation.
                                                                                     During the “random strains” step, the simulation box
                                                                                  is simultaneously deformed and compressed or dilated
collection of shapes within a periodic FC through a pro-                          in a way that attempts to decrease its area on average
cess of rearranging the positions of the shapes within an                         while preserving the nonoverlap constraints. Since the
FC while decreasing the FC’s volume in order to increase                          locations of the particles are expressed in terms of the
the packing density. Formally stated, the ASC optimiza-                           lattice vectors, straining the simulation box also effects
tion scheme is                                                                    a collective motion of the particles. The straining pro-
                                                                                  cess is attempted up to a prescribed maximum number
 minimize −φ(r λ1 , rλ2 , rλ3 , . . . , r λN ; θ1 , θ2 , θ3 , . . . , θN ; Λ),    of attempts. The first successful strain is kept, and the
 such that (Si ∩ Sj ) ⊆ (Γi ∪ Γj ) ∀i, j = 1, 2, 3, . . . , N,                    algorithm returns to the first step (random movements).
     i 6= j,                                                                (2)   After each unsuccessful strain attempt, the maximum al-
                                                                                  lowed strain is decreased by a constant ratio in order
where N is the number of particles in the FC, and r λi                            to steadily increase the chances of finding a valid strain.
and θi specify the position and orientation of particle i,                        Therefore, more attempts are required as the packing in-
respectively (see below). The optimization scheme can                             creases in density. In addition, uphill moves that allow
be solved using a variety of techniques including stochas-                        the FC to expand are allowed with a given probability.
tic search methods with simulated annealing [30, 31] and                             The maximum magnitude of the trial movements is
linear programming [32]; the present work uses an adap-                           steadily decreased throughout the execution of the algo-
tation of the former. For the sake of completeness, the                           rithm, reducing the maximum magnitude by a constant
technique will be described here.                                                 ratio when the acceptance rate of trial moves falls signif-
    In R2 , the ASC scheme utilizes a parallelogrammatic                          icantly below 50%. Moreover, while the maximum strain
fundamental unit cell (FC) with periodic boundary con-                            magnitude is decreased after each unsuccessful attempt,
ditions. The positions of the N particles are given                               the maximum magnitude is restored to its original value
by the lattice coordinates (i.e., the relative coordinates                        the next time the “random strains” step occurs, since,
with respect to the lattice vectors) of their centroids,                          for example, particle movements within the FC may re-
r λ1 , r λ2 , rλ3 , . . . rλN ∈ [0, 1)2 ; and (global) orientations,              sult in two particles being next to each other at the end
θ1 , θ2 , θ3 , . . . , θN ∈ [0, 2π). From the initial configura-                  of one “random movements” step (necessitating a small
tion, the stochastic search method uses an iterative pro-                         strain), and may result in the particles being more uni-
cess to increase the packing density. Its main steps are                          formly spaced at the end of the next step (allowing for a
the following:                                                                    larger strain even though the FC may be smaller).
    • Random rotations or translations are applied to the                            The sequence of random movements and random
      shapes, accepting moves that satisfy the required                           strains is repeated a prescribed number of times, cho-
      nonoverlap constraints between the shapes (“ran-                            sen such that the algorithm has “enough time” to find
      dom movements”), then                                                       and settle in a minimum of the objective function (which
                                                                                  is determined by monitoring the convergence of the pack-
    • Random strains, composed of a combination of a                              ing density); in the present work, the maximum number
      deformation and either a dilation or a compression,                         of iterations is always at least 500. In order to refine the
      are applied to the FC that seek to either increase or                       results, a “fine tuning” procedure may be used in which
      decrease its area with a specified probability, corre-                      the ASC algorithm is executed a second time, starting
      sponding to uphill and downhill moves, respectively                         with the previous final dense configuration by expanding
      (“random strains”).                                                         the FC by some small amount and greatly reducing the
                                                                                                                       4

magnitude of the movements and strains in order to more       [0, 1]; the w = 0 case corresponds to a pair of lines of
accurately approach the density maximum that has been         length l bisecting each other at a right angle, and the
identified. However, this process is only used in cases       w = 1 case corresponds to a square of side length l.
where the particles are convex, since this is necessary
to ensure that a general expansion of the FC does not
introduce overlaps.                                                            B.    Curved Triangle
   In the past, the ASC scheme has been applied to deter-
mining packings of convex polyhedra in three and higher         Another particle shape that we investigate is the so-
dimensions, detecting overlaps between particles through      called “curved triangle,” that, in the convex case, is
use of the separation axis theorem [30, 31]; in this work,    a two-dimensional analog of the “tetrahedral puff” de-
the algorithm has been modified to detect overlaps be-        scribed in [34]. This particle shape is derived by replac-
tween concave particles in two dimensions through a com-      ing the sides of an equilateral triangle with circular arc
binatoric check of the particle’s edges, which may be         segments; this is illustrated in Figure 3. The particle
some combination of line segments and circular arc seg-       shape may then described by a parameter
ments.
                                                                                               r0
   This solution of the ASC scheme is a particularly                                     k=±      ,                  (4)
strong investigative tool since it is capable of identify-                                     r
ing dense packing configurations quickly and with ap-         where r is the radius of the arc segments, and r0 is the
preciable consistency. Analytical methods may then be         radius of a circle passing through the triangle’s vertices.
used, benefitting from the information derived from the       k is taken by convention to be positive when the curved
algorithm’s results to determine the exact structures of      triangle is convex as in Figure 3a, and negative when
the packings. In addition, the freedom to choose any          the curved triangle is concave as in Figure 3b. When
initial condition may be used to enhance the quality of       k = 0, then the particle √ shape becomes an equilateral
solutions found if an interesting structure is more often     triangle; when k = 1/ 3 = 0.577350 . . . , the particle
realized through specific initial conditions [32]. In the     shape becomes the well-known Reuleaux triangle [35];
present work, we find that, by choosing initial lattice       and when k = √    1, the particle shape becomes a circle.
vectors that more closely resemble the final lattice vec-     When k = −1/ 3, the vertices of the particle become
tors of dense structures, denser results are achieved, and    cusps, and in order to decrease k beyond this point, a line
with increased frequency.                                     segment connects the cusp and the vertex, as is shown in
                                                              Figure 3c; the curved triangle is said to be “spiked” in
                                                              this regime, and begins to resemble the Mercedes-Benz
    IV.   NONCIRCULAR PARTICLE SHAPES                         logo. In the limit k → −∞, the particle shape becomes
                                                              the union of three line segments of length r0 , each at an
   A variety of noncircular particle shapes were stud-        angle of 2π/3 from the others.
ied in the present work; this section aims to make pre-
cise the geometries that were studied. In order to es-
tablish benchmarks for the program’s performance, the                          C.   Moon-Like Shape
well-known cases of regular pentagons and octagons were
considered. In addition, we consider three families of           The third nontrivial particle shape that we investigate
nontrivial particle shapes: “fat crosses”, “curved trian-     is the a “moon-like” shape, which is constructed by a pair
gles”, and “moon-like shapes”. The packing characteris-       of circular arc segments with radii r0 and r, where the
tics of these noncircular particle shapes have heretofore     former arc is a half-circle. The particle shape is parame-
not been studied. We show that they lead to unique            terized by the same parameter k used to characterize the
packing arrangements.                                         curved triangle [cf. Eq. (4)], where k is, by convention,
                                                              taken to be negative when the particle shape is a concave,
                                                              “crescent” shape, as in Figure 4a and positive when the
                     A.   Fat Cross                           moon is a convex, “gibbous” shape, as in Figure 4b.

   The first nontrivial particle shape that we investigate
is a so-called “fat cross.” Several examples of this par-                           V.   RESULTS
ticle shape are given in Figure 2. The particle shape is
described by a width parameter w according to the defi-          The stochastic search solution of the ASC scheme
nition                                                        described in Sec. III is used to generate dense peri-
                               δ                              odic packings of congruent copies of the particle shapes
                          w=     ,                     (3)    described above, and the resulting computer-generated
                               l
                                                              packings are used to inform analytical predictions for the
where δ is the width of the cross’s legs, and l is the end-   structures of the densest packings; the following details
to-end length of the cross. Therefore, it follows that w ∈    the results of the numerical simulations and discusses
                                                                                                                               5


                                                               δ


                                                               l


PSfrag replacements         PSfrag replacements         PSfrag replacements
                  l                                                       l
                  δ                                                       δ
                                (a)                         (b)                                (c)

             FIG. 2: Three instances of the general “fat cross” with w = 1/10 (a), 1/3 (b), and 9/10 (c).


the structures that we find. We also provide visual rep-                                  C.    Fat Crosses
resentations of some noteworthy cases. A summary of
the densest packing behavior of the noncircular particle              Periodic packings of congruent copies of fat crosses
shapes the we obtain is given in Table I.                          were generated using the ASC algorithm with four-
                                                                   particle bases for various values of w. From these sim-
                                                                   ulations, four different packing behaviors were observed.
                                                                   Figure 7 compares the packing density of a number of
                      A.   Octagons                                computer-generated cases against the analytical puta-
                                                                   tive maximum packing density. The curve contains four
                                                                   piecewise-smooth regimes, corresponding to four differ-
  Periodic packings of congruent copies of regular oc-             ent structures, identified as L1 , L2 , L3 , and L4 , in order
tagons were generated using the ASC algorithm with                 of increasing w. Figure 8 shows a few selected packings
one-, two-, three-, and four-particle bases. Some note-            to show these different configurations. Notice that at
worthy computer-generated packings are shown in Fig-               w = 1/3, 1/2, and 1, the packing becomes a tiling. It
ure 5. The ASC algorithm finds periodic packings of oc-            is interesting to note that, though this shape is concave,
tagons in accordance with Fejes Tóth’s well-known the-            all of the densest packings found are lattice packings.
orem that the densest packing of a centrally-symmetric             Another interesting property of these packings is that,
convex particle shape is realized by a lattice packing [18].       in the limit case w = 0, the fat cross is equivalent (up
Moreover, the packing densities found via numerical sim-           to a scaling constant) to the limit case of a superdisk,
ulation are remarkably close to the theoretical optimum:           lim {(x, y) ∈ R2 : |x|2p + |y|2p ≤ 1}, and the analyt-
δφ1 = 2.0 × 10−5 , δφ2 = 1.35 × 10−4 , δφ3 = 2.35 × 10−4 ,         p→0

and δφ4 = 2.61 × 10−4 , where δφN denotes the differ-              ical packing structure matches this superdisk’s already-
ence in packing density between the analytical optimal             known densest packing [36]. The fat crosses’ putative
construction and the best numerical result using an N -            maximum packing density is tabulated for several repre-
particle basis.                                                    sentative values in Table II; see the Supplemental Mate-
                                                                   rial for mathematical details about the various packing
                                                                   structures.


                      B.   Pentagons                                                 D.    Curved Triangles

   Periodic packings of congruent copies of regular pen-              Periodic packings of congruent copies of convex curved
tagons were generated using the ASC algorithm with two-            triangles were generated using the ASC algorithm with
and four-particle bases. Figure 6 shows some noteworthy            two- and four-particle bases for various values of k. Using
numerical findings. These results closely resemble the             a method of Kuperberg and Kuperberg [25], the densest
best-known √  packing of pentagons, whose packing density          double-lattice packing of convex curved triangles was de-
is φ = (5 − 5)/3 = 0.921311 . . . ; the packings shown in          rived as a function of the curvature parameter k. This
Figures 6a and 6b differed from this by 2.09 × 10−4 and            function is plotted as a solid curve in Figure 9, and
1.0 × 10−5 , respectively. These packings show the struc-          computer-generated packings with a two-particle basis
ture conjectured to be the densest packing of pentagons            are plotted as triangular marks; it was observed that the
[24–27]. Indeed, it is conjectured that, for a wide class          results predicted by the Monte Carlo method using a two-
of bodies lacking central symmetry, the densest packing            particle basis closely matched the optimal double-lattice
is realized in a double-lattice configuration. The regular         packing for all of the chosen values of k.
pentagon is one of these shapes.                                      Figures 10 and 11 show a few of the packings that
                                                                                                                                     6




                                                                                                              r
                                             r
                                                                                              r0

                                                 r0




PSfrag replacements                                   PSfrag replacements

                                       (a)                                                         (b)




                                                                           r0




                                                      r
                         PSfrag replacements


                                                                    (c)

      FIG. 3: (Color online) Three examples of the basic form of a curved triangle: convex ((a), k = 0.71), concave ((b),
                                        k = −0.39), and “spiked” ((c), k = −1.55).

        TABLE I: Symmetries of the putative densest packings of the aforementioned particle shapes. The properties of
      well-known shapes (pentagons and octagons) are compared to the results we obtain for our nontrivial particle shapes
                                    (fat crosses, curved triangles, and moon-like shapes).

      Shape Name             Convex              Centrally-Symmetric Particle       Centrally-Symmetric Basis          N
      Pentagon                 Yes                           No                                Yes                     2
      Octagon                  Yes                           Yes                               Yes                     1
      Fat Cross                No                            Yes                               Yes                     1
      Curved Triangle      depends on k                      No                                Yes            2,4 (depending on k)
      Moon-like shape      depends on k                      No                           depends on k                 2




      were generated by the ASC algorithm with two- and four-             triangles do not line up such that their vertices touch. In-
      particle bases, respectively. Notice that the densest pack-         stead, the two adjacent triangles are rotated slightly so
      ings with a two-particle basis are double-lattice packings,         that the vertex of one contacts the arc of the other. In-
      implying a centrally-symmetric√ basis. However, in all of           deed, when determining the optimal double-lattice struc-
      the cases where 0 < k < 1/ 3, it was observed that the              ture by a method of Kuperberg and Kuperberg [25], it
                                                                                                                                       7

                                                                                          1


                                                                                         0.8


                                                                                         0.6
g replacements                 PSfrag replacements




                                                                                     φ
            rr0                                 rr0                                      0.4
                            (a)                             (b)
                                                                                         0.2
                   FIG. 4: (Color online) Examples of a “crescent” ((a),
                  k > 0) and a “gibbous” ((b), k < 0) moon-likePSfrag
                                                                shape,replacements
                                                                         .
                                                                                          0
                                                                                           0         0.2   0.4       0.6   0.8     1
                                                                                                                 w

                                                                                 FIG. 7: Analytically-derived (solid curve) and
                                                                             computer-generated (data points) packing densities for
                                                                             packings of fat crosses as a function of width parameter
                                                                             w. The structures are labeled as follows: filled circle =
                                                                                   L1 , square = L2 , triangle = L3 , cross = L4 .



                            (a)                             (b)




                                                                                               (a)                               (b)
                            (c)                             (d)

                    FIG. 5: (Color online) Computer-generated dense
                  periodic packings of octagons using one- (a), two- (b),
                   three- (c), and four-particle (d) bases. The packing
                   densities are φ = 0.906144, 0.906029, 0.905929, and
                                  0.905903, respectively




                                                                                               (d)                               (e)

                                                                                 FIG. 8: (Color online) Computer-generated dense
                                                                              periodic packings of fat crosses for various values of w
                                                                             showing the four structures observed. The L1 structure
                                                                             is shown for w = 1/10 (a), 1/3 (b), and 2/5 (c); the L2
                                                                              structure is shown for w = 19/40 (d); the L3 structure
                            (a)                             (b)                 is shown for w = 11/20 (e); and the L4 structure is
                                                                                              shown for w = 7/10 (f).
                    FIG. 6: (Color online) Computer-generated dense
                    periodic packings of pentagons using two- (a) and                                               √
                    four-particle (b) bases. The packing densities are       the packing density when 0 < k < 1/ 3, meaning that
                         φ = 0.921102 and 0.921301, respectively.            this characteristic of the numerical results is not due to
                                                                             numerical inaccuracies, but, on the contrary, showcases
                                                                             the sensitivity of the stochastic search in finding dense
              was found that this small perturbation actually increases      packings.
                                                                                                                                            8

               TABLE II: Putative maximum packing densities of
             congruent copies of fat crosses for selected values of w.

             w                                                  φ(w)
             0.1                                         76/125 = 0.608
             0.2                                           9/10
             0.3                                        204/205 = 0.995121 . . .
             0.4                                          64/65 = 0.984615 . . .
             0.48                                       912/925 = 0.985945 . . .              (a)                              (b)
             0.55                                         29/31 = 0.935483 . . .
             0.6                                          21/23 = 0.913043 . . .     FIG. 11: (Color online) Computer-generated dense
             0.7                                        182/191 = 0.952879 . . .         periodic packings of curved triangles with a
             0.8                                          48/49 = 0.979591 . . .      four-particle basis for k = 3/10 (a) and 7/10 (b);
                                                                                          φ = 0.921528 and 0.921460, respectively.
             0.9                                        198/199 = 0.994974 . . .


                                                                                      Numerical results using a four-particle basis showed
                           1                                                       that, for sufficiently large k, a packing structure exists
                                                                                   whose density is significantly higher than the best double-
                         0.98                                                      lattice packing; below this point, the four-particle basis’
                                                                                   optimal configuration is a degenerate case of the two-
                         0.96                                                      particle basis, as shown in Figure 11a; an example of the
                                                                                   non-degenerate four-particle basis structure is given in
                     φ




                         0.94                                                      Figure 11b. Numerical results using an eight-particle ba-
                                                                                   sis, an example of which is shown in Figure 12, provide
                         0.92
                                                                                   additional evidence that the four-particle basis is in fact
                                                                                   the densest configuration. These results were verified by
Sfrag replacements                                                                 determining the analytical structure of the four-particle
                          0.9
                             0        0.2   0.4       0.6    0.8         1         basis that is currently the best-known packing structure
                                                  k
                                                                                   for this shape. The densities of computer-generated pack-
              FIG. 9: Analytically-derived and computer-generated                  ings of curved triangles using a four-particle basis are
              packing densities of curved triangles for various values             plotted as filled circles, and the corresponding analyti-
             of k. The solid curve denotes the density of the optimal              cal packing density is displayed as a dashed line in Fig-
             double lattice packing, and the dashed curve shows the                ure 9. Though periodic tilings of convex particles have
                  density of the optimal periodic packing with a                   been shown that exhibit more than a two-particle basis
             four-particle basis; triangle and filled circle data points           [37–39], we do not know of any other convex, non-tiling
                 denote densities obtained by computer-generated                   shapes that have been observed to exhibit this behavior
             packings with two- and four-particle bases, respectively.             [40].
                                                                                      In order to create this four-particle packing structure,
                                                                                   the particles in the FC, denoted A0 , B0 , C0 , and D0 ,
                                                                                   are placed facing straight-up and straight-down, where
                                                                                   particles A0 and D0 are both in contact with all of the
                                                                                   other particles in the basis, as shown in Figure 13. The
                                                                                   lattice vectors λ1 and λ2 are found by finding the posi-
                                                                                   tions of shapes A1 and A2 (both of which are periodic
                                                                                   images of A0 ) relative to A0 . All of the bodies in the
                                                                                   basis are rotated by the same angle θ: A and D are ro-
                                                                                   tated anti-clockwise, and B and C are rotated clockwise.
                                                                                   Doing this causes B1 and C2 (and their periodic images)
                                (a)                                (b)             to come into contact. Once this contact is established,
                                                                                   the packing achieves its maximum density; this result is
              FIG. 10: (Color online) Computer-generated dense                     shown in Figure 14. The curved triangles’ putative maxi-
            periodic packings of curved triangles with a two-particle              mum packing density is tabulated for some representative
              basis for k = 2/5 (a) and 4/5 (b); φ = 0.922437 and                  values of k in Table III; see the Supplemental Material for
                             0.924589, respectively.                               details of the analytical construction of this packing. In
                                                                                   addition, computer-generated packings of concave curved
                                                                                   triangles are provided in the Appendix without analytical
                                                                                                                                    9

                                                                           TABLE III: Putative maximum packing densities of
                                                                         congruent copies of convex curved triangles for selected
                                                                                               values of k.

                                                                         k                                                 φ(k)
                                                                         0.1                                           0.967582 . . .
                                                                         0.2                                           0.944761 . . .
                                                                         0.3                                           0.930217 . . .
                                                                         0.4                                           0.922458 . . .
                                                                         0.5                                           0.922458 . . .
                                                                         0.6                                           0.927362 . . .
                                                                         0.7                                           0.928415 . . .
                                                                         0.8                                           0.925249 . . .
                                                                         0.9                                           0.918262 . . .




                                                                         densest computer generated packings are plotted as data
             FIG. 12: (Color online) A computer-generated densest        points along solid curves denoting three different ana-
             packing of curved triangles with an eight-particle basis    lytical constructions in Figure 15. The first structure
              (k = 0.62), showing a structure that is a degenerate       observed was a double-lattice packing shown in Figures
                   case of the best-known four-particle basis.           16a and 16d. This structure is indicated in Figure 15
                                                                         by triangular data points and will be referred to as the
                                                                         D1 structure. The second structure observed was a non-
             constructions; all of these packings appear to be double-   double-lattice periodic packing with a two-particle basis,
             lattice packings.                                           shown in Figure 16b; it is indicated in Figure 15 by square
                                                                         data points and will be referred to as the B-structure.
                                                                         The third structure observed was a second double-lattice
                                                                         packing, shown in Figure 16c. This structure is indicated
                                                                         in Figure 15 by filled circle data points and is denoted
                                                                         as the D2 -structure. The putative densest packings of
Sfrag replacements                                                       moon-like shapes are tabulated as a function of k in Ta-
                                   A0        B0
                                                                         ble IV.
                                                                           The B-structure is a unique structure in that its funda-
                              C0        D0                               mental basis possesses no inherent symmetries. Further-
                                                  A2        B2           more, its discovery underscores the utility of the ASC
                                                                         algorithm in determining the densest packings that are
                         A1        B1                                    not obvious by inspection.
               C1                            C2        D2

                                                                           TABLE IV: Putative maximum packing densities of
                              D1                                         congruent copies of moon-like shapes for selected values
                                                                                                 of k.

               FIG. 13: (Color online) A portion of the analytical       k                φ(k)              k              φ(k)
             packing without any applied rotation (k = 0.65). Notice     −0.9         0.928125 . . .       0.1         0.936131 . . .
             that a gap exists between B1 and C2 (and their periodic     −0.8         0.916116 . . .       0.2         0.935451 . . .
                images). Applying the rotation closes this gap and       −0.7         0.910371 . . .       0.3         0.933966 . . .
                         maximizes the packing density.                  −0.6         0.907259 . . .       0.4         0.931709 . . .
                                                                         −0.5         0.911837 . . .       0.5         0.928675 . . .
                                                                         −0.4         0.921385 . . .       0.6         0.924819 . . .
                                                                         −0.3         0.928392 . . .       0.7         0.920053 . . .
                              E.   Moon-like Shapes
                                                                         −0.2         0.932303 . . .       0.8         0.915055 . . .
                                                                         −0.1         0.933906 . . .       0.9         0.914783 . . .
               Periodic packings of congruent copies of moon-like
                                                                         0            0.935931 . . .       0.95        0.913563 . . .
             shapes were generated using the ASC algorithm with
             two- and four-particle bases for various values of k. The
                                                                                                                               10




                                                        PSfrag replacements
                                             A0    B0                   A0                      A0              B0
                                                                        B0
Sfrag replacements                                                      C0
                                            C0   D0 A2 B2               D0
                                                                        A1
                                         A1    B1 C2 D2                 B1
                                                                        C1                 C0              D0
                                                                        D1
                                       C1 D1                            A2
                                                                        B2
                                                                        C2
                                                                        D2



                                             (a)                                                     (b)

               FIG. 14: (Color online) The analytically-derived packing of curved triangles (k = 0.65) with the applied rotation
              (a); a zoomed-in view is provided in (b). Triangles A0 and D0 are rotated anti-clockwise by θ, and triangles B and
                                     C are rotated clockwise by θ, where θ = 0.057 rad. φ = 0.928473 . . . .



                          1


                        0.98


                        0.96
                    φ




                        0.94

                                                                                    (a)                              (b)
                        0.92

frag replacements
                         0.9
                           −1   −0.5         0          0.5   1
                                             k

                  FIG. 15: Putative maximum packing densities for
              congruent copies of moon-like shapes as a function of k.
                The three different structures are denoted as follows:
               triangle = D1 , square = B, dot = D2 ); the solid curve
                           shows the analytical densities.
                                                                                    (c)                              (d)

                                                                            FIG. 16: (Color online) Computer-generated dense
                 VI.       CONCLUSIONS AND FUTURE WORK                   periodic packings of moon-like shapes for various values
                                                                          of k, displaying the three different packing structures
                In this paper, we implemented a two-dimensional im-          observed. (a): k = −0.8 (D1 -structure, crescent
             plementation of the Torquato-Jiao Adaptive Shrinking          instance). (b): k = −0.2 (B-structure). (c): k = 0.6
             Cell scheme using a stochastic search with simulated an-      (D2 -structure). (d): k = 0.9 (D1 -structure, gibbous
             nealing to study the dense packing behavior of a variety                            instance).
             of well-known and nontrivial particle shapes. We con-
             firmed the utility of the algorithm by reproducing the
             well-known densest packings of regular pentagons and        correctly and accurately predicted subtle perturbations
             octagons. Next, we applied the algorithm to several non-    in the two-particle packings of curved triangles that are
             trivial particle shapes to find their densest packing be-   not immediately intuitively apparent.
             havior. It is especially worth noting that the ASC scheme     The packing characteristics of the curved triangle
                                                                                                                      11




                       (a)                                 (b)                                (c)

 FIG. 17: (Color online) Computer-generated dense periodic packings of concave curved triangles for k ′ = 1/20 (a),
27/100 (b), and 9/20 (c). The packing densities are φ = 0.019141, 0.446702, and 0.896363, respectively. All of these
                                    packing suggest double-lattice structures.


shape class are unlike anything studied before because its      adapted to generate both packings of hard particles in
optimal packing density is not achieved using a double-         closed containers. By altering the shrinking behavior of
lattice packing for sufficiently high curvature. In addi-       the domain, it may be possible to study both densest
tion, the B-structure that achieves the densest packings        packings and disordered jammed packings. Furthermore,
of certain moon-like shapes is a counterintuitive finding       the algorithm may be readily adapted to study packings
for its lack of symmetry in its fundamental basis. These        of particles with a polydispersity in size and shape. Fi-
discoveries underscore the utility of the stochastic search     nally, the stochastic search solution to the ASC scheme
implementation of the ASC scheme because of its abil-           may readily be adapted to investigate the dense packing
ity to accurately predict these structures up to the small      behavior of concave solids in higher dimensions.
details inherent in them.
   The packing structures discussed in this work of-
fer insights towards the organizing principles for three-                       1

dimensional particles in Ref. [1]. For example, the dens-
est packings of regular polygons, as two-dimensional                          0.8

analogs of convex polyhedra, show similar behavior in                         0.6
that the densest packings of regular polygons possess-
                                                                          φ




ing central symmetry are given by their corresponding                         0.4

densest lattice packings; and the densest packings of
                                                                              0.2
those lacking central symmetry are nonetheless given   PSfrag replacements
by packings that possess a point of inversion symme-                            0
                                                                                 0   0.1  0.2
try. Furthermore, the densest packings of fat crosses                                         k′ 0.3 0.4   0.5


are given by their corresponding densest lattice pack-
ings, in much the same way that the densest packings            FIG. 18: (Color online) Densities of computer generated
of three-dimensional, centrally-symmetric polyhedra are          packings of concave curved triangles for various values
conjectured to be given by their corresponding densest                                     of k ′ .
lattice packings. One final interesting remark is that the
B structure of moon-like shapes possesses no points of in-
version. This is in contrast to the proposition in three di-
mensions that the densest packings of concave polyhedral
particles are composed of centrally symmetric compound
units. It seems intuitively true that, by approximating
the appropriate moon-like shape as a polygon with suffi-                       ACKNOWLEDGEMENTS
ciently many edges, some structure similar to B structure
will achieve the densest packing (which has no points of
inversion).                                                        This work was supported by the Materials Research
   It will be desirable in future work to determine the an-     Science and Engineering Center (MRSEC) Program of
alytical packing behavior of the concave instance of the        the National Science Foundation under Grant No. DMR-
curved triangle (for which computer-generated results are       0820341 and by the Division of Mathematical Sciences at
provided in the Appendix) for the sake of completeness.         the National Science Foundation under Award Number
More generally, the algorithm used in this work may be          DMS-1211087.
                                                                                                                                12

 APPENDIX: MAXIMALLY DENSE PACKINGS                                was observed for all particle shapes that we tried. The
   OF TWO-DIMENSIONAL CONVEX AND                                   packing densities of the computer-generated cases are
   CONCAVE NONCIRCULAR PARTICLES                                   plotted in Figure 18 as a function of an alternative pa-
                                                                   rameter k ′ , defined as the ratio of the inradius of the
                                                                   particle to its circumradius. According to this alternative
  Figure 17 shows a collection of computer-generated               parameter, the k ′ = 0 limit is equivalent to the k = −∞
dense periodic packings of concave curved triangles with           limit (Mercedes-Benz limit), and k ′ = 1/2 describes an
two- and four-particle bases. A double-lattice structure           equilateral triangle (k = 0).




 [1] S. Torquato and Y. Jiao, Phys. Rev. E 86, 011102 (2012).      [21] J. H. Conway and K. M. Knowles, Journal of Physics A:
 [2] J. D. Bernal, “Liquids: Structure, properties, solid inter-        Mathematical and General 19, 3645 (1986).
     actions,” (Elsevier, Amsterdam, 1965) pp. 25–50.              [22] L. Fejes Tóth, Regular Figures (MacMillan, New York,
 [3] R. Zallen, The Physics of Amorphous Solids (Wiley, New             1964).
     York, 2005).                                                  [23] K. Reinhardt, Abh. Math. Sem. Hamburg 10, 216 (1934).
 [4] S. Torquato, Random Heterogeneous Materials: Mi-              [24] C. L. Henley, Phys. Rev. B 34, 797 (1986).
     crostructure and Macroscopic Properties (Springer-            [25] G. Kuperberg and W. Kuperberg, Discrete & Computa-
     Verlag, New York, 2002).                                           tional Geometry 5, 389 (1990), 10.1007/BF02187800.
 [5] P. Chaikin and T. Lubensky, Principles of Condensed           [26] Y. L. Duparcmeur, A. Gervois, and J. P. Troadec, Jour-
     Matter Physics (Cambridge University Press, 2000).                 nal of Physics: Condensed Matter 7, 3421 (1995).
 [6] P. Corradini, V. Petraccone, and B. Pirozzi, European         [27] T. Schilling, S. Pronk, B. Mulder, and D. Frenkel, Phys.
     Polymer Journal 19, 299 (1983).                                    Rev. E 71, 036138 (2005).
 [7] T. Yamaguchi, T. Asada, H. Hayashi, and N. Nakamura,          [28] L. Fejes Tóth, Proc. Kon. Ned. Aka. Wet. 51, 189 (1948).
     Macromolecules 22, 1141 (1989)..                              [29] K. Mahler, Duke Math J. 13, 611 (1946).
 [8] J. Liang and K. A. Dill, Biophysical Journal 81, 751          [30] S. Torquato and Y. Jiao, Nature 460, 876 (2009).
     (2001).                                                       [31] S. Torquato and Y. Jiao, Phys. Rev. E 80, 041104 (2009).
 [9] P. K. Purohit, J. Kondev, and R. Phillips, Proc. Natl.        [32] S. Torquato and Y. Jiao, Phys. Rev. E 82, 061302 (2010).
     Acad. Sci. USA 100, 3173 (2003).                              [33] See Supplemental Material at http://link.aps.org/
[10] J. L. Gevertz and S. Torquato, PLoS Comput Biol 4,                 supplemental/10.1103/PhysRevE.86.031302 for math-
     e1000152 (2008).                                                   ematical details for the packing structures presented in
[11] M. Ohring, Materials Science of Thin Films (Academic               this paper.
     Press, 2001).                                                 [34] Y. Kallus and V. Elser, Phys. Rev. E 83, 036703 (2011).
[12] W. Azzam, P. Cyganik, G. Witte, M. Buck, and C. Wll,          [35] F. Reuleaux, Kinematics of Machinery; Outlines of a
     Langmuir 19, 8262 (2003)..                                         Theory of Machines, edited by A. Kennedy (MacMillan,
[13] P. Cyganik, M. Buck, W. Azzam, and C. Wll, The                     London, 1875).
     Journal of Physical Chemistry B 108, 4989 (2004)..            [36] Y. Jiao, F. H. Stillinger, and S. Torquato, Phys. Rev.
[14] R. Farhadifar, J.-C. Rper, B. Aigouy, S. Eaton, and                Lett. 100, 245504 (2008).
     F. Jlicher, Current Biology 17, 2095 (2007).                  [37] K. Reinhardt, Über die Zerlegung der Ebene in Poly-
[15] A.-K. Classen, K. I. Anderson, E. Marois, and S. Eaton,            gone, Ph.D. thesis, Königlichen Universität zu Frankfurt
     journal Developmental Cell 9, 805 (2005).                          (1918).
[16] C. A. Rogers, Packing and Covering (Cambridge Univer-         [38] R. B. Kershner, The American Mathematical Monthly
     sity Press, 1964).                                                 75, pp. 839 (1968).
[17] C. A. Rogers, Acta Math 86, 309 (1951).                       [39] H. Heesch, Reguläres Parkettierungsproblem (West-
[18] L. Fejes Tóth, Acta Sci. Math. 12A, 62 (1950).                    deutscher Verlag, 1968).
[19] B. Grünbaum and G. Shephard, Bull. Amer. Math Soc.           [40] We do not consider particle shapes derived from applying
     3, 951 (1980).                                                     trivial perturbations (that is, those that do not alter the
[20] J. H. Conway and J. Lagarias, Journal of Combinatorial             densest packing structure) to shapes that form tilings.
     Theory, Series A 53, 183 (1990).
