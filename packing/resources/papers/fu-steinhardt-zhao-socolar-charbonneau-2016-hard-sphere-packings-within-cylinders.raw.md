                                                                                   Hard sphere packings within cylinders

                                                           Lin Fu,a William Steinhardt,b Hao Zhao,a Joshua E. S. Socolar,b and Patrick Charbonneau∗ab
                                                                                  a
                                                                                    Duke University, Department of Chemistry, Durham,
                                                                                 NC 27708, USA. E-mail: patrick.charbonneau@duke.edu,
                                                                           b
                                                                             Duke University, Department of Physics, Durham, NC 27708, USA.
                                                                                               (Dated: September 8, 2017)
                                                                 The packing of hard spheres (HS) of diameter σ in a cylinder has been used to model experimental
                                                              systems, such as fullerenes in nanotubes and colloidal wire assembly. Finding the densest packings of
                                                              HS under this type of confinement, however, grows increasingly complex with the cylinder diameter,
                                                              D. Little is thus known about the densest achievable packings for D > 2.873σ. In this work, we
                                                              extend the identification of the packings up to D = 4.00σ by adapting Torquato-Jiao’s adaptive-
arXiv:1511.08472v1 [cond-mat.soft] 26 Nov 2015




                                                              shrinking-cell formulation and sequential-linear-programming (SLP) technique. We identify 17 new
                                                              structures, almost all of them chiral. Beyond D ≈ 2.85σ, most of the structures consist of an outer
                                                              shell and an inner core that compete for being close packed. In some cases, the shell adopts its own
                                                              maximum density configuration, and the stacking of core spheres within it is quasiperiodic. In other
                                                              cases, an interplay between the two components is observed, which may result in simple periodic
                                                              structures. In yet other cases, the very distinction between core and shell vanishes, resulting in
                                                              more exotic packing geometries, including some that are three-dimensional extensions of structures
                                                              obtained from packing hard disks in a circle.


                                                                 I.   INTRODUCTION                                thickness is increased from a monolayer to a bulk system.
                                                                                                                     The intermediate case of quasi-one-dimensional con-
                                                    Packing problems, i.e., identifying optimal configura-        finement models a number of experiments, including
                                                 tions of a set of hard geometric objects in space without        packing fullerenes in nanotubes [24, 25], colloidal wire
                                                 overlap, are NP-hard optimization problems [1]. Of these         formation [26] and nanoparticle self-assembly in cylindri-
                                                 problems, packings of hard spheres (HS) have been the            cal domains [27, 28], yet has received substantially less
                                                 most extensively investigated because of their dual phys-        attention than other confinement types. Existing stud-
                                                 ical generality and mathematical elegance. For instance,         ies nonetheless suggest that these systems can display a
                                                 in condensed matter hard sphere packings help explain            variety of remarkable structural features. The first ef-
                                                 both the ordering of binary alloys [2–4] and the persis-         forts by Pickett et al. to systematically identify maxi-
                                                 tence of disorder in metallic glass formers [5]. Mathemat-       mally dense packings of HS of diameter σ in cylinders
                                                 ical demonstrations of the optimality of these packings          of diameters D revealed the emergence of spontaneous
                                                 are also prestigious challenges to surmount. In two di-          helical chirality [29]; and Mughal et al.’s systematic ex-
                                                 mensions, the triangular lattice has long been known to          tension of this work from D = 2.155σ to D = 2.873σ
                                                 be the densest packing of disks [6], but the proof of the        showed how plane disclinations allow helical structures
                                                 Kepler conjecture for hard spheres in three dimensions           to continuously transform into one another [30].
                                                 was only recently obtained [7] (with much fanfare [6]),             Because the largest cylinders studied remain quite far
                                                 and in higher dimensions demonstrations are an absolute          from the bulk limit, a rich set of structural features is
                                                 scarcity [8, 9].                                                 to be expected in wider cylinders as well. Many of the
                                                    Although packing objects in infinite spaces can be a          existing tools for finding optimal packings are, however,
                                                 reasonable model for describing the structure of bulk ma-        insufficient in this regime. Earlier analyses relied on sim-
                                                 terials, in confined systems boundaries play a substantial       ulated annealing [29, 30], whose computational efficiency
                                                 role. The consideration of packings in bounded spaces is         is too limited for finding packings with a separate in-
                                                 also motivated by the wide variety of situations in which        ner core and outer shell. Algorithms based on sequential
                                                 objects are stored in containers of different shapes [10–        deposition are much more expedient [31], but the final
                                                 12]. Many variants of this problem have thus been con-           structure they generate depends too sensitively on the
                                                 sidered by mathematicians and physicists, including disks        choice of underlying template for them to be of broad
                                                 in a circle [13–15], a rectangle or a strip [16, 17] in two      applicability. Although genetic algorithm schemes (akin
                                                 dimensions, and spheres in a sphere, a cube [18, 19] or          to that used in Ref. [3]) can search configuration space
                                                 a parallelepiped [20] in three dimensions. Irrespective of       more broadly, the growing structural complexity of the
                                                 the dimensionality of the packed objects, however, the           packings with D necessitates unit cells that are too large
                                                 above packing problems are all quasi-zero-dimensional,           for the approach to remain computationally tractable.
                                                 because extrapolating to the small system limit gives               In this work, we improve the computational capabil-
                                                 a simple point. Packing objects between planes, i.e.,            ity of finding dense HS packings cylinders with D >
                                                 in quasi-two-dimensional confinement, has also been in-          2.873σ by instead using an adaptive-shrinking cell and
                                                 tensely studied [21–23], notably in order to understand          a sequential-linear-programming (SLP) technique [32].
                                                 the transition from two-step to first-order melting as the       This approach confirms earlier results for D ≤ 2.86σ and
                                                                                                                              2

extends our knowledge of packings up to D = 4.00σ.                  for boundary particles. In order to find the maximum
Interestingly, many of the new structures appear to be              packing density we must solve the following problem:
quasiperiodic and another of the packings presents fairly
exotic geometries. In Section II, we describe the SLP                                            minimize vu
computational method, in Section III we present the SLP
results for different ranges of cylinder diameters, and             subject to
in Section IV we specifically analyze the quasiperiodic                             n
                                                                                   rmn  ≥ D̄mn , ∀ mn neighbor pairs,       (7)
structures observed in the range 2.988σ ≤ D ≤ 3.42σ
                                                                         rir + ∆rr + Ri ≤ D/2, ∀ i = (1, 2, ..., N ),       (8)
using a sinking algorithm developed for this problem.
                                                                    where D̄mn = (Dm + Dn )/2 and Ri is the radius of parti-
                                                                    cle i. The first condition corresponds to the hard-sphere
  II.     SEQUENTIAL LINEAR PROGRAMMING                             constraint and the second to the hard-wall constraint.
                    METHOD                                          Because during the optimization D is fixed, minimizing
                                                                    vu is equivalent to minimizing λz . The packing prob-
   In order to identify HS packings in cylinders, we adapt          lem then becomes a standard constrained optimization
the SLP method of Torquato and Jiao [32] to this ge-                problem, and the constraints can be linearized (by Tay-
ometry. For convenience, we describe configurations us-             lor expansion), allowing the use of linear-programming
ing cylindrical coordinates with z, r, and θ representing           solvers [32, 33]. The optimization problem at each step
the axial, radial and angular components, respectively.             then becomes
For our search procedure, we consider a fixed number
of spheres in a finite cylinder with periodic boundary                                          minimize : z ,
conditions that match the top of the cylinder to the bot-
tom with a twist. In other words, the entire volume of              subject to
the cylinder is initially taken as a unit cell with a one-                            n
                                                                                     rmn ≥ D̄mn , ∀ mn neighbor pairs       (9)
dimensional periodicity. The infinite structure consists
of spheres centered at                                                               D/2 ≥ rir + ∆rr + Ri , ∀ i            (10)
                                                                              ∆rlower ≤ |∆ri | ≤ ∆rupper , ∀ i             (11)
                          ij = ri + nj λ ,                   (1)                     lower               upper
                                                                                            ≤ || ≤            ,         (12)
where ri (i = 1, 2, ...) are the particle positions within a
                                                                    where the superscripts refer to the upper and lower
unit cell, nj ∈ Z, and λ = (λr , λθ , λz ) is the lattice vector.
                                                                    bounds for particle displacements and volume changes.
For our system, λz is the height of the unit cell, λθ is the
                                                                    Although the solution of this problem can be obtained by
twist angle, and λr = 0. The volume of a unit cell is thus
                                                                    linear programming, displacements and unit cell adjust-
                        vu = π(D/2)2 λz ,                    (2)    ments at each optimization step must remain relatively
                                                                    small because of the linearization. The overall packing
and the lattice packing fraction can be expressed as                optimization must thus be done sequentially, meaning
                                                                    that the optimal solution for a given step is used as in-
                                 N vs                               put for the subsequent one, until convergence is achieved.
                            η=        ,                      (3)    Operationally, we accept a solution as having converged
                                 vu
                                                                    when the difference between two iterations |∆vu | < vtol ,
where N is the number of particles in a unit cell and vs            where vtol = 10−6 . Note that because this criterion is in-
is the volume of a sphere of diameter σ.                            dependent of the unit cell size, the final unit cell volume
   A each optimization step, we allow the N particles in            is determined less precisely for larger unit cells, but this
the unit cell to move as well as changes to the unit cell           effect is negligible on the scale of the figures and other
height, λz , and twist angle, λθ . Denoting the particle            numerical results reported here.
displacements ∆r, the matrix specifying changes to the
unit cell , the new particle positions rn , and the new
lattice vector λn , we have                                                              III.     SLP RESULTS

     λn = (I + )λ                                           (4)       Using the SLP method, we identified candidate struc-
                  
            0 0 0                                                   tures for HS packings from D = 2.16σ to D = 4.00σ.
       = 0 θ 0                                           (5)    For D ≤ 2.862, we reproduced previously reported re-
            0 0 z                                                  sults [30] (Fig. 1), but we obtained denser structures than
        rn = ( rr + ∆rr , rθ + ∆rθ , (1 + z )(rz + ∆rz ) ) . (6)   Mughal et al. for 2.862σ < D < 2.873σ (Fig. 3 inset).
                                                                    This discrepancy is likely due to the difference in system
Note that the twist angle is not continuously shearing              sizes between the two studies. The packings obtained
the particles within the unit cell, but is only a property          for this regime in Ref. [30] had unit cells with either
of the boundary conditions. It thus only appears in rn              N = 7 or 15 particles, while our search extended up to
                                                                                                                              3

                                                                lix can be defined in three different ways (Fig. 2), each
                                                                maximal density structure presents up to six correspond-
                                                                ing line-slip possibilities (two directions for each type of
                                                                slip), although symmetry can reduce this number.
                                                                   In the following subsections we present an overview of
                                                                different D regimes over which the packings we obtain
                                                                share a number of structural features.


                                                                TABLE I. Structural parameters and properties of close-
                                                                packed outer shells for different cylinder diameters. Quan-
                                                                tities are rounded to the last digit
                                                                Notation D/σ      ∆θ ∆z/σ Chirality Number of helices
                                                                 (6,5,1) 2.8652 1.1167 0.1538 chiral      1
                                                                 (6,6,0) 3.0000 1.0472 0.0000 achiral     /
                                                                 (7,4,3) 3.0038 0.9365 0.4268 chiral      3
                                                                 (7,5,2) 3.0623 0.9697 0.2759 chiral      2
FIG. 1. Packings for 2.16σ ≤ D ≤ 2.86σ. Configurations           (7,6,1) 3.1664 0.9507 0.1309 chiral      1
are depicted at the density maxima. Yellow particles are part    (8,4,4) 3.2630 0.7854 0.5000 achiral     4
of a same helix. In this regime, the results are in complete     (8,5,3) 3.2888 0.8357 0.3706 chiral      3
agreement with those of Ref. [34]. Figure 3 presents results     (7,7,0) 3.3048 0.8976 0.0000 achiral     /
for D ≥ 2.86σ.
                                                                 (8,6,2) 3.3615 0.8475 0.2391 chiral      2
                                                                 (8,7,1) 3.4720 0.8272 0.1139 chiral      1
                                                                 (9,5,4) 3.5377 0.7220 0.4434 chiral      4
N = 150, and the densest structures had 50 ≤ N ≤ 85.
                                                                 (9,6,3) 3.5818 0.7496 0.3267 chiral      3
The origin of this strong system size dependence likely
lies in the aperiodicity or the complex periodicity of the       (8,8,0) 3.6131 0.7854 0.0000 achiral     /
packings. (We come back to this point in Section III.2.)         (9,7,2) 3.6648 0.7512 0.2109 chiral      2
For D ≥ 2.873σ, no systematic studies had previously             (9,8,1) 3.7805 0.7318 0.1008 chiral      1
been undertaken, and only a few structures had been             (10,5,5) 3.8025 0.6283 0.5000 achiral     5
proposed [35]. SLP identifies 17 distinct structures and        (10,6,4) 3.8223 0.6624 0.3971 chiral      4
their deformations over 2.873σ ≤ D ≤ 4.00σ (Fig. 3).            (10,7,3) 3.8800 0.6771 0.2917 chiral      3
The packings depicted in Figure 3 are local maxima in            (9,9,0) 3.9238 0.6981 0.0000 achiral     /
η(D).
                                                                (10,8,2) 3.9711 0.6738 0.1883 chiral      2
   Most of the structures in this regime have two well-
defined layers: an inner core and an outer shell. Because
many of the outer shells are optimal packings of disks on
the inner surface of the cylinder, they can be described
using the phyllotactic notation for helices, (l, m, n), with
l = m+n, where l, m and n are the number of helices, us-
ing the three possible helix definitions (Fig. 2) [34]. The
parameters defining some of these helical outer shells are
listed in Table III. For simplicity, we denote below struc-
tures with the helix whose height difference, ∆z, between
two successive particles within that helix is minimal, and
∆θ is thus the angular coordinate difference between two
successive particles within that helix (Fig. 2a). Based
on these definitions, we note that λz = (Ns /l)∆z, λθ =
mod 2π ((Ns /l)∆θ), where Ns is the number of shell par-
ticles in the unit cell.
   Intermediate structures can be obtained by contin-
uously transforming the local density maxima. Some
                                                                FIG. 2. There exists three different ways to define a helix,
are uniform radial expansions (or compressions) of these
                                                                and thus six possible line-slip structures. Yellow particles are
structures, accompanied with a compression (or expan-           part of a same helix. In the text, we select the convention
sion) in z, while other structures undergo a line-slip,         depicted in (a).
which is a slip between two helices, keeping the relative
position of the other helices constant [30]. Because a he-
                                                                                                                           4

            III.1.   Structures for D < 2.86σ                   3.000σ is a line-slip structure of (7,4,3), for which no six
                                                                outer particles are ever in the same plane. They can thus
   In this regime, all the structures are periodic and have     wrap an inner core without difficulty. Optimal packings
a simple mathematical description. Most of them are             from that point on and up to D = 3.42σ are found to
simple helices. The last two structures, however, are non-      almost always form the densest possible shell packing,
helical and contain an inner core (Fig. 1). The densest         independently of the core particles. The local density
structure for 2.71486σ ≤ D ≤ 2.74804σ has D5 symmetry           maxima in Figure 3 for this regime indeed all correspond
with a close-packed inner core, and can be constructed as       to the diameters of close-packed outer shells (Table III).
a packing of spindles of nearly regular tetrahedra. The            Out of the sequence, the structure with a (8,4,4) outer
optimal structure for 2.74804σ ≤ D ≤ 2.8481σ has in-            shell is particularly noteworthy. As for all outer shells
stead a unit cell of 11 particles – an inner particle sand-     with m = n = 21 l, this helical structure is achiral – two
wiched between two staggered five-particle rings – that         of the three possible helical directions are equivalent, and
is reminiscent of a stacking of ferrocene molecules. Note,      ∆z = σ/2. As a result, the outer shell consists of straight
however, that neither the inner core nor the outer shell        columns when viewed from the top of the cylinder. The
of this last structure are close-packed.                        top view of (8,4,4) outer shell and its core is thus very
                                                                similar to the packing of disks in a circle (Fig. 4a). Two
                                                                other structures are found to have this property (Fig. 4b
       III.2.   Structures for 2.86σ ≤ D < 2.988σ               and c), but the structure with the (8,4,4) outer shell is
                                                                the only one that is close-packed. Note that a similar
   For D ≥ 2.86σ, packings do not have simple ana-              phenomenon would likely be observed for a structure with
lytical descriptions. The competition between the in-           a (10,5,5) outer shell were it to be a density maximum
ner core and the outer shell becomes more complex,              (which it is not).
because the two layers have different packing require-             The case D = 3.00σ is also remarkable. The outer
ments, and neither of them systematically wins. For             shell is then a close-packed structure with staggered six-
2.86σ ≤ D ≤ 2.988σ, the inner core dominates. To see            particle rings,
                                                                            p√i.e., (6,6,0). The spacing between two rings
                                                                                       .
why, note that a core particle can only fit into a shell        is ∆⊥ = σ       3 − 1 = 0.8556σ. Although core particles
formed by a horizontal layer of 6 spheres when D ≥ 3σ.          placed between the planes of the rings can shift off the
For D < 3σ, a core sphere can only fit if these 6 spheres       cylinder axis, they cannot shift enough to allow a peri-
form a helix around it. Every core particle must thus be        odic packing of the core with no gaps between successive
at the center of a six-particle helix, which limits its free-   core spheres. This phenomenon illustrates the difficulty
dom to move within the inner core. For instance, for the        of searching for close-packed structures in this regime.
close-packed (6,5,1) outer shell, for which D = 2.8652σ,        Optimal structures may be quasiperiodic and thus not
the spacing between two turns of the six-particle helix         correspond to any finite λz . Our numerical approach
that forms the outer shell is 6∆z = 0.9228σ < σ. If             then at best provides a periodic approximant of the opti-
the outer shell were close-packed, then three six-particle      mal structure. In order to consider this issue more care-
helices would only accommodate a single inner particle,         fully, we present an alternate algorithm for studying this
leaving large gaps between inner particles. A denser            regime in Section IV.
packing is instead obtained by deforming the outer shell
in order to accommodate a close-packed inner core.
   As D approaches 3σ, core particles become increas-                       III.4.   Structures for D > 3.42σ
ingly free to move. For 2.97σ < D < 3.00σ, the
densest possible outer shell is a line-slip structure of           For D > 3.42σ, many of the close-packed outer shells
(7,4,3). The perfect (7,4,3) outer shell at D = 3.0038σ         are not observed. Instead of remaining disordered or
has an inner core spacing of 73 ∆z = 0.9959(1)σ, which          quasiperiodic, the inner core then forms nearly ordered
is barely smaller than a particle diameter. Hence, for          structure, which imposes many defects on the outer shell.
2.97σ < D < 2.988σ, although the overall structure re-          For some of the packings, the defects are so large that
mains dominated by the inner core, the outer shell is           they enable the two shells to interpenetrate. The packing
barely different from a close-packed line-slip structure of     structures in this regime are thus not clearly dominated
(7,4,3).                                                        by any one of the two layers, hence neither of the two
                                                                shells is typically close-packed. For instance, of l-particle
                                                                staggered ring structures, (l, l, 0), only l = 6, 7 and 9 are
       III.3.   Structures for 2.988σ ≤ D ≤ 3.42σ               observed. For l = 6 and 7, the inner core is so small that
                                                                only a lightly zig-zagging chain of particles fits within it;
   For 2.988σ ≤ D, the inner core is sufficiently large to      for l = 9, the inner core is large enough that a staggered
allow core particles to move freely within an outer shell,      three-particle ring structure fits. For l = 8, however, the
thus greatly reducing their constraint on the outer shell.      zig-zagging structure is not very dense, and a two-particle
Note that the lower end of this range is smaller than           flat pair does not fit. The packing structure thus ends
3σ because the densest outer shell for 2.988σ ≤ D <             up having a completely different organization: a dense
                                                                                                                                5




FIG. 3. Packings for D = 2.85 − 4.00σ. Configurations are depicted at the density maxima. Yellow particles are part of a same
helix or its line-slip structure, as described by the phyllotactic notation, and red particles are hoppers (see text for details).
Note that some configurations do not have a well-defined helical structure. The inset shows the difference between Mughal
et al.’s (red triangles) and the current (blue circles) results for 2.86σ < D < 2.875σ.


triple helix inner core and an tortuous outer helical shell           As discussed in Sec. III.2, for 3.00σ ≤ D ≤ 3.42σ, the
of eight particles.                                                incommensurability of the two shells may result in struc-
   The competition between the two shells does not only            tures that are not periodic. The densest structures thus
result in defective compromises, but also yields two novel         cannot be obtained using a finite periodic unit cell, which
types of structures. First, some structures are analogous          makes the numerical search for packings by SLP ex-
to three-dimensional extensions of packing of hard disks           tremely challenging (if not impossible) for some regions,
in a circle (Fig. 4b and c). Although the roughly straight         e.g. 3.00σ ≤ D ≤ 3.05σ. By contrast, for D > 3.42σ
columns formed by these structures gives their top view a          the strong interaction between the two shells forces the
two-dimensional feel, they are not simple stacks of these          two to share a same periodicity in some ranges of D (see
packings. As can be seen in Figure 4, projections of par-          Supplementary information). The packings in those re-
ticles onto the cylinder base reveals overlaps. The outer          gions are thus periodic, which reduces the computational
shell is an (imperfect) triangular lattice rather than a           difficulty of identifying these structures. The vastness of
square lattice, and the outer rings are not flat but form          the configurational space to sample at this point, how-
zig-zags. As a result the same three-dimensional ver-              ever, reduces the confidence with which truly optimal
sion fits in a cylinder of a smaller diameter than that            packings are then identified.
of the two-dimensional circle. Second, some structures
cannot be neatly divided into shells. For instance, for
3.55σ ≤ D ≤ 3.61σ, although both layers are dense the                       IV.    SINKING ALGORITHM FOR
gap between them is sufficiently large to allow outer par-                            2.988σ ≤ D ≤ 3.42σ
ticles to hop back and forth between the two shells, keep-
ing η unchanged (Fig. 4c and Fig. 3).                                 SLP results suggest that for 2.988σ ≤ D ≤ 3.42σ pack-
  Table III indicates that four ten-fold (l = 10) outer            ings may be quasiperiodic. Despite their relatively sim-
shells could potentially be observed for D ≤ 4.00σ. Yet            ple geometrical description, the true densest structures
only one appears in the phase sequence, as the last struc-         are then beyond the reach of our numerical algorithm
ture. The other three structures are missing, because for          because the algorithm relies on periodic boundary con-
3.62σ ≤ D ≤ 3.94σ, the inner core is just large enough to          ditions. We thus consider an approach that can analyze
accommodate a triple helix, and thus a nine-fold helical           the infinite-system size limit of these packings. This ap-
outer shell provides a better periodicity than a ten-fold          proach, however, rests on assumptions about the overall
one to accommodate this inner shell.                               structure of packings that are not rigorously justified,
                                                                                                                                 6




FIG. 4. Comparison between disks in a circle and the top
view of spheres in a cylinder at (a) D = 3.613σ [36] (circle)      FIG. 5. The cylinder surface area occupancy for bent
and D = 3.25σ (cylinder), (b) D = 3.813σ [36] (circle) and         hexagons with different orientations for D = 3σ. The area
3.43σ (cylinder), and (c) D = 3.924σ [37] (circle) and 3.58σ       coverage is minimized for θ = π/6 and is maximal for θ = 0,
(cylinder). Red particles are hoppers. The cylinder outer          even though it is the latter structure that gives rise to the
shells consist of straight columns and only the top layer of       (6,6,0) outer shell.
particles is visible, so the resulting packings look similar to
those of disks in a circle. Note that because the height of
neighboring columns is shifted by 0.5σ, the cylinder diameter
is smaller than that of the circle and projecting particles onto
the cylinder base reveals overlaps.



and is found to be suboptimal in a few instances.
   We first assume that packings in this regime have an
outer shell that is as dense as possible along the cylin-
der wall. For certain special values of D, these shells are        FIG. 6. Close-packed outer shells: (a) stacked layers of 6
close-packed, meaning that every sphere in that shell is           spheres each (6,6,0), (b) a 7-particle triple helix (7,4,3), and
in direct contact with six other particles within the shell        (c) a 7-particle double helix (7,5,2).
(see Fig. 6). For D = 3σ, for instance, the densest outer
shell is the (6,6,0) structure. Note, however, that even
this seemingly straightforward case would be mathemati-            density of the inner core is then computed as follows.
cally nontrivial to demonstrate. The structure cannot be           We first choose a random height for the first particle and
argued to be optimal based on the local packing density,           maximize its radial coordinate. Given the position of a
because a closed hexagon (or triangle) of spheres on the           sphere in the core, we assume the best way to pack the
cylinder surface minimizes the covered area when one di-           next higher sphere is to place it at the lowest possible po-
ameter of the hexagon is vertical rather than horizontal           sition without moving any sphere in the shell or already
as in the (6,6,0) structure (Fig. 5). Proving that (6,6,0)         placed in the core. Each core sphere thus touches the
shell is the densest possible for D = 3σ thus remains an           core sphere below it and two spheres of the outer shell.
open problem. We nonetheless persist in this direction             The procedure is iterated until the density of the core
and next assume that each successive core particle then            can be determined to within the desired accuracy.
falls to its lowest possible position without perturbing              In the special case of D = 3σ, the procedure
                                                                                                               p√       can be
the outer shell. These assumptions are broadly consis-             described by a map. Recall that ∆⊥ = σ          3 − 1 is the
tent with the SLP results, and should allow for slightly           spacing between successive layers of the shell. Consider a
denser structures to be obtained by side-stepping the pe-          core sphere at a generic specified height z1 that is moved
riodicity constraint.                                              as far as possible off of the cylinder axis and is therefore
   For convenience in the following, we define the shell           touching two shell spheres. Let x1 be the position of this
density, ρs , as the number of shell spheres per unit length       sphere and x2 be the position of the core sphere that
along the cylinder axis. As the cylinder diameter D ex-            sits just above it. Let ai = {zi /∆⊥ }, where {·} denotes
pands from a close-packed shell, the shell could expand            the fractional part, indicate the relative height of the ith
radially and compress axially, but it is always preferable         sphere with respect to the shell layers just below and
for a line slip to emerge instead [38]. It is an exercise in       just above it. We construct the map M (a) that relates
geometry to analytically generate these structures. The            a2 to a1 . This map can then be iterated to determine the
                                                                                                                              7

locations of all of the spheres in the core:
             zi+1 = zi + (1 + {a2 − a1 })∆⊥ .            (13)
If the map converges to a fixed point or a limit cycle, the
core is periodic. We will see, however, that this map is
either quasiperiodic or has an extremely long period.
   Figure 7 shows the possible locations x1 for a sphere
within one layer. The cyan circular arc shows the possible
locations for a sphere that touches two adjacent shell
spheres in a same layer. The magenta arc shows the
possible locations for a sphere that touches two adjacent
spheres in different layers. The purple arc shows the
same locations as the cyan arc, but shifted up one layer
and rotated accordingly by π/6 about the cylinder axis.
The portions of these arcs shown with thick blue and red
curves (along with the positions related by the hexagonal
rotations and reflections) are the possible locations of a
core sphere within the depicted layer.




                                                                 FIG. 8. Placement of a core sphere. A point P on the blue or
                                                                 red curve indicates a possible placement of a sphere center.
                                                                 The sphere above it lies on the point on the green or orange
                                                                 curve that is a distance σ from P . See text for details.



                                                                 the map yields ω = 0.163887 and the function f (a) shown
                                                                 in Fig. 9. Note the scale on the vertical axis; deviations
                                                                 from a line with unit slope are quite small. The slope of
                                                                 M (a) lies within the range (0.8689, 1.1533) everywhere,
FIG. 7. Possible locations of a core sphere within a layer.      hence the map is monotonic and thus invertible, which
The large disks are cross sections of the confining cylinder,    means that it cannot be chaotic [39].
and are separated by ∆⊥ . The core sphere must be centered
on a point on one of the thick blue curves or the short, thick
red curve. See text for details.

   The placement, x2 , of the sphere that rests on top
of the sphere at x1 must lie on a piecewise arc of the
type shown in Fig. 7, displaced one or two layers upward,
and rotated so as to be as close to diametrically opposite
x1 as possible. Inspection of the possible rotations and
reflections reveals that the choice leading to the densest
structure is a reflection through the plane containing the
cyan arc in Fig. 7, followed by a rotation by 7π/6 about
the cylinder axis and a translation upward by ∆⊥ , as
shown in Fig. 8.
   The map M (a) is determined by finding the value of
a2 along the upper curve (green/orange in Fig. 8) that
is exactly σ away from a1 on the lower curve (blue/red).
M (a) has the form of a circle map:
                 M (a) = {a + ω + f (a)} ,               (14)    FIG. 9. Plot of the nonlinear term in the map from the height
                                                                 of one core sphere to the next one up, f (a). Note that for the
where ω is a constant and f (a) is a periodic function with      purposes of this figure we have not taken the fractional part
unit period and zero mean. Numerical computation of              of an+1 . Note also the scale on the vertical axis.
                                                                                                                           8

   For a circle map with a small amplitude nonlinearity,       sinking algorithm identifies the densest structures to have
the generic behavior is quasiperiodic [39]. In the present     a (7,4,3) outer shell, while the SLP algorithm produces
case, we confirm the quasiperiodicity to a high degree of      a (6,6,0) outer shell. The packing fraction difference be-
accuracy, i.e., we detect no exponential convergence to a      tween these two structures is small, but well above our
limit cycle, and we determine the asymptotic density ρ∞        numerical precision. The discrepancy may thus result
by fitting the values of ρn = n/zn to the form ρ∞ + c/n,       from the former structure not being as easily accessible
where c is a constant. More precisely, we compute zn ,         in the SLP search than the latter for our choice of algo-
the height of the nth sphere in the core, taking z = 0 to      rithmic parameters and initial conditions.
be a point at the center of a layer of the outer shell and        At the level of precision considered for the SLP study
beginning with z1 = 0. We then extract the sequence of         (∆D = 0.01σ), the sinking algorithm is found not to win
zn values for which the nth sphere sets a new record for       outright at three points: D = 3.04σ, D = 3.27σ, and
coming closest to lying exactly in the plane of a layer, but   D = 3.40σ (see Table II). We find two distinct mecha-
is just below that plane, i.e, points for which an comes       nisms are at play here, which can be seen through con-
ever closer to unity. Note that if the sequence were con-      sideration of the linear density ratio between the SLP
verging to a periodic limit cycle, this procedure would        and the sinking algorithms separately for the shell, ρs ,
either yield a finite sequence or one that exponentially       and for the core, ρ∞ (Fig. 11 inset). Interestingly, we
approaches a value different from unity. Figure 10 shows       find that ρSLP
                                                                           s   /ρsink
                                                                                 s    ≤ 1 at 3.04σ and 3.40σ. This in-
ρn − ρ∞ as a function of n for the sequence of best ap-        dicates that a denser core is obtained at the expense of
proximants, where ρ∞ has been adjusted to get a straight       having a slightly perturbed (and less dense) outer shell.
line on the log-log plot. We find the best fit to be ob-       At 3.27σ, some shell spheres instead do not touch the
tained for ρ∞ ≈ 1.0043324(1)/σ, which is slightly denser       cylinder wall (taking over some of the empty core space),
than for a simple stack of spheres on the cylinder axis,       which increases both the shell and the core densities. (For
1/σ. The total number of spheres per unit of cylinder          D = 3.09 − 3.10σ, the SLP also identifies a denser outer
length is thus ρs + ρ∞ = 8.0169578(1)/σ, corresponding         shell than the one used in the sinking algorithm, but in
to η = 0.593849(1), which is denser than η = 0.593661(1)       these cases the denser core obtained by the sinking algo-
obtained from the SLP algorithm as expected.                   rithm more than compensates for this difference.) The
                                                               effect of the coupling between the outer shell and the
                                                               inner core may be due to the proximity of a change to
                                                               the shell symmetry (D ≈ 3.04σ), or to the end of this
                                                               regime (D ≈ 3.40σ), but finer resolution studies would
                                                               be needed to make more definitive statements. It is also
                                                               unclear whether this coupling is strong enough to make
                                                               the densest structures periodic. SLP identifies unit cells
                                                               that contain at least 55 ≤ N ≤ 80 spheres, but more
                                                               would be certainly possible.


                                                               TABLE II. Density differences between SLP and sinking
                                                               structures for points where the former is denser than the lat-
                                                               ter.
                                                                    D/σ (ρSLP
                                                                            s    − ρsink
                                                                                    s    )σ (ρSLP    sink
                                                                                              ∞ − ρ∞ )σ η
                                                                                                            SLP
                                                                                                                − η sink
                                                                                       −6               −3
                                                                     3.04 −6.4 × 10          1.259 × 10    9.0 × 10−5
FIG. 10. Infinite-system size extrapolation of the packing                            −6                −4
                                                                     3.27    2.9 × 10        4.510 × 10    2.8 × 10−5
density to ρ∞ for D = 3σ from the sinking algorithm.                                   −3               −3
                                                                     3.40 −7.9 × 10          9.254 × 10    7.2 × 10−5
   For D 6= 3σ, the lack of reflection symmetry in the he-
lical shells and the presence of line slips complicate the
construction of a map from one core sphere height to the
next. We instead perform brute force numerical compu-                             V.   CONCLUSION
tations of the core packing algorithm for n spheres and
take the core density to be ρ = n/zn . The joint core and        In this study, we have extended the range of known
shell packing fraction, η(D), is obtained with a resolution    HS packings in cylinders of diameters D = 2.862σ to
of ∆D = 0.001σ (see Fig. 11). For most values of D, the        D = 4.00σ by adapting the SLP method of Ref. [32] to
sinking algorithm gives structures with a higher packing       this geometry and by developing a sinking algorithm. We
fraction than the SLP algorithm, but differences that are      have identified 17 new structures, most of them chiral,
typically less than 0.1%, which suggests that the SLP          along with their continuous deformation. We also distin-
algorithm performs remarkably well in this regime. The         guish ranges of cylinder diameters over which different
most significant structural difference between the two al-     types of packings are observed. Most notably, around
gorithms is observed for 3.003σ ≤ D ≤ 3.017σ, where the        D = 3σ the outer shell is both fairly independent of the
                                                                                                                                      9

                                                                               Although our study ended at D = 4.00σ, we expect the
    0.62
                                                                            competition between different shells to persist even once
    0.61
                                          1.01                              three and four of them develop. For D  4σ, however,




                             ρSLP/ρsink
                                            1
                                                                            the bulk FCC limit should eventually be recovered. The
     0.6                                                                    shell area should thus eventually form but a thin wrap-
                                          0.99                              ping of a FCC core. Based on the analogy with packing
    0.59
                                          0.98                              of disks within a circle [15], however, we don’t expect
    0.58
                                                                            this phenomenon to develop before D & 20σ, which is
                                             3    3.1    3.2    3.3   3.4
                                                                            far beyond the regime that can be reliably studied with
    0.57                                                                    existing numerical methods.
                                                                               In closing, it is important to recall the difference be-
    0.56
                                                                            tween packings and their assembly from local algorithms.
    0.55
                                                                            Although optimal, some of the packings may be dy-
            3   3.05   3.1   3.15           3.2   3.25   3.3   3.35   3.4   namically hard to access (or even inaccessible) via self-
                                                                            assembly, which can be important in simulations and col-
                                                                            loidal experiments. This aspect will be the object of a
FIG. 11. Packing results for the SLP (blue circles) and
                                                                            future publication.
the sinking (solid line) algorithms are in fairly close agree-
ment, but the quasiperiodic phases identified by the lat-
ter are typically denser. The biggest differences are in the
choice of optimal shell morphology around D = 3.01σ and
D = 3.35σ. The phase sequence for the sinking algorithm                                    ACKNOWLEDGMENTS
is (7,4,3), (6,6,0), (7,4,3), (6,6,0), (7,5,2), (7,6,1), (8,4,4),
(8,5,3), (7,7,0) and (8,6,2), from left to right (separated by
dashed lines). The inset shows the shell ρSLP    /ρsink (red tri-              This work was supported by the National Science
                                             s      s
                    SLP   sink
angles) and core ρ∞ /ρ∞ (blue circles) linear density ratio                 Foundation’s Research Triangle Materials Research Sci-
as a function of D. See text for details.                                   ence and Engineering Center (MRSEC) under Grant No.
                                                                            (DMR-1121107), and NSF grant from the Nanomanufac-
                                                                            turing Program (CMMI-1363483). We thank Ce Bian,
inner core and closely packed, and both algorithms pro-                     Daniela Cruz, Gabriel Lopez, Rémy Mosseri, Crystal
vide strong numerical evidence that many of the packings                    Owens, Wyatt Shields and Benjamin Wiley for stimu-
are quasiperiodic.                                                          lating discussions.




 [1] M. Hifi and R. M’hallah, Adv. Oper. Res. 2009, 150624                  [13] R. L. Graham, B. D. Lubachevsky, K. J. Nurmela, and
     (2009).                                                                     P. R. Östergaard, Discrete Math. 181, 139 (1998).
 [2] A. B. Hopkins, Y. Jiao, F. H. Stillinger, and S. Torquato,             [14] F. Fodor, Beitrage Algebra Geom. 44, 431 (2003).
     Phys. Rev. Lett. 107, 125501 (2011).                                   [15] A. B. Hopkins, F. H. Stillinger, and S. Torquato, Phys.
 [3] L. Filion and M. Dijkstra, Phys. Rev. E 79, 046714                          Rev. E 81, 041305 (2010).
     (2009).                                                                [16] H. Akeb and M. Hifi, Comput. Oper. Res. 40, 1243
 [4] J. K. Kummerfeld, T. S. Hudson, and P. Harrowell, J.                        (2013).
     Phys. Chem. B 112, 10773 (2008).                                       [17] Y. G. Stoyan and G. Yas’ kov, Eur. J. Oper. Res. 156,
 [5] K. Zhang, W. W. Smith, M. Wang, Y. Liu, J. Schroers,                        590 (2004).
     M. D. Shattuck, and C. S. O’Hern, Phys. Rev. E 90,                     [18] M. Goldberg, Math. Mag. , 199 (1971).
     032311 (2014).                                                         [19] T. Gensane, Electron. J. Combin. 11, R33 (2004).
 [6] T. Aste and D. Weaire, The Pursuit of Perfect Packing,                 [20] Y. Y. Stoyan, G. Yaskow, and G. Scheithauer, Central
     2nd ed. (Taylor and Francis, New York, 2008).                               Eur. J. Oper. Res. 11, 389 (2003).
 [7] T. C. Hales, Ann. Math. , 1065 (2005).                                 [21] P. Pieranski, L. Strzelecki, and B. Pansu, Phys. Rev.
 [8] J. H. Conway and N. J. A. Sloane, Sphere Packings,                          Lett. 50, 900 (1983).
     Lattices and Groups, 3rd ed., A Series of Comprehen-                   [22] M. Schmidt and H. Löwen, Phys. Rev. Lett. 76, 4552
     sive Mathematics, Vol. 290 (Springer-Verlag, New York,                      (1996).
     1999) p. 663.                                                          [23] A. Fortini and M. Dijkstra, J. Phys.: Condens. Matter
 [9] H. Cohn and N. Elkies, Ann. Math. 157, 689 (2003).                          18, L371 (2006).
[10] Y. G. Stoyan, Advances in CAD/CAM: Proceedings of                      [24] W. Mickelson, S. Aloni, W.-Q. Han, J. Cumings, and
     PROLAMAT82, Leningrad, USSR , 67 (1982).                                    A. Zettl, Science 300, 467 (2003).
[11] H. J. Fraser and J. A. George, Eur. J. Oper. Res. 77, 466              [25] A. N. Khlobystov, D. A. Britz, A. Ardavan, and G. A. D.
     (1994).                                                                     Briggs, Phys. Rev. Lett. 92, 245507 (2004).
[12] L. H. W. Yeung and W. K. Tang, IEEE Trans. Ind. Elec-                  [26] M. Tymczenko, L. F. Marsal, T. Trifonov, I. Rodriguez,
     tron. 52, 617 (2005).                                                       F. Ramiro-Manzano, J. Pallares, A. Rodriguez, R. Alcu-
                                                                                 billa, and F. Meseguer, Adv. Mater. 20, 2315 (2008).
                                                                                                                       10

[27] S. Sanwaria, A. Horechyy, D. Wolf, C.-Y. Chu, H.-L.        [36] U. Pirl, Math. Nachr. 40, 111 (1969).
     Chen, P. Formanek, M. Stamm, R. Srivastava, and            [37] H. Melissen, Geod. Dedic. 50, 15 (1994).
     B. Nandan, Angew. Chem. Int. Ed. 53, 9090 (2014).          [38] A. Mughal and D. Weaire, Phys. Rev. E 89, 042307
[28] R. Liang, J. Xu, R. Deng, K. Wang, S. Liu, J. Li, and           (2014).
     J. Zhu, ACS Macro Lett. 3, 486 (2014).                     [39] E. Ott, Chaos in dynamical systems (Cambridge Univer-
[29] G. T. Pickett, M. Gross, and H. Okuyama, Phys. Rev.             sity Press, Cambridge, New York, 2002) section 6.2.
     Lett. 85, 3652 (2000).
[30] A. Mughal, H. Chan, D. Weaire, and S. Hutzler, Phys.
     Rev. E 85, 051305 (2012).                                         SUPPLEMENTARY INFORMATION
[31] H.-K. Chan, Phys. Rev. E 84, 050302 (2011).
[32] S. Torquato and Y. Jiao, Phys. Rev. E 82, 061302 (2010).
                                                                 Appendix A: Unit cell sizes for packings identified
[33] A. Makhorin, “Glpk (gnu linear programming kit),”
                                                                to be optimal by the sequential linear programming
     (2008).
                                                                                  (SLP) method
[34] A. Mughal, H. K. Chan, and D. Weaire, Phys. Rev. Lett.
     106, 115704 (2011).
[35] H. C. Huang, S. K. Kwak, and J. K. Singh, J. Chem.           SLP identifies the densest structures in the ranges
     Phys. 130, 164511 (2009).                                  2.86σ ≤ D ≤ 2.98σ and 3.43σ ≤ D ≤ 4.00σ as well
                                                                as for D = 3.04σ, 3.27σ and 3.40σ.
                                                                                                                               11


TABLE III. Structural parameters for different cylinder diameters. Quantities are rounded to the last digit. * denotes that
the identified structure has a small enough period to give confidence that it is the truly optimal packing. Other entries indicate
the densest structure for the N range we search. Recall that η = [ 43 π( σ2 )3 N ]/[π( D
                                                                                       2
                                                                                         )2 ]λz .
 D/σ         N         λz /σ        λθ         D/σ        N        λz /σ        λθ         D/σ        N        λz /σ        λθ
  2.86       63       9.0393      2.9033        3.52      77      7.4307      0.6253       3.77       58      4.5814      0.8325
  2.87       50       6.9948      2.8225        3.53      77      7.3873      5.6060       3.78       58      4.5496      0.8230
  2.88       65       8.9876      5.2646        3.54      72      6.8727      3.7098       3.79       58      4.5220      0.8134
  2.89      138      18.9765      0.1512        3.55      62      5.8876      2.8030       3.80       54      4.1833      1.3869
  2.90      117      15.9913      0.8482        3.56      62      5.8565      3.4986       3.81       54      4.1563      1.4064
  2.91       81      10.9944      2.6513        3.57      52      4.8802      3.2919       3.82       54      4.1322      1.4034
  2.92      141      18.9795      1.8146        3.58      66      6.0746      0.0044       3.83       54      4.1166      4.8716
  2.93       90      12.0053      0.3859        3.59      66      6.0000      0.0153       3.84       54      4.1063      1.3987
  2.94       83      10.9975      0.9297        3.60      55      4.9973      0.0563       3.85       79      5.9917      0.0480
  2.95       69       1.9603      0.1637        3.61      66      5.9896      0.1373       3.86       79      5.9805      0.0473
  2.96       69       9.0133      4.3213        3.62      72      6.5186      0.3233       3.87       71      5.3601      1.8866
  2.97       69       8.9801      1.7785        3.63      57      5.1245      3.0348       3.88       71      5.3448      1.9012
  2.98       55       7.0602      2.4692        3.64      83      7.4014      0.0912       3.89       71      5.3314      1.9129
  3.04       48       5.9376      3.6792        3.65      83      7.3474      6.2378       3.90*      12      0.8944      0.3191
  3.27       50       5.4996      5.5196       3.66*      12      1.0527      0.1915       3.91*      12      0.8836      0.7146
  3.40       78       8.0863      2.5233       3.67*      12      1.0396      0.1961       3.92*      12      0.8704      0.7083
 3.43*       10       1.0192      0.0000       3.68*      12      1.0263      0.2005       3.93*      12      0.8609      0.9076
 3.44*       10       1.0069      0.0000       3.69*      12      1.0127      0.2050       3.94*      12      0.8598      0.3492
 3.45*       10       1.0000      0.0097       3.70*      12      0.9989      0.2094       3.95*      14      1.0002      0.1737
  3.46       59       5.9567      3.3920       3.71*      12      0.9972      0.1993       3.96*      14      0.9927      0.1797
  3.47       65       6.4690      1.1549       3.72*      12      0.9963      0.1953       3.97*      14      0.9890      0.1822
  3.48       51       5.0314      2.1022       3.73*      12      0.9944      0.8389       3.98*      14      0.9859      1.3955
  3.49       51       4.9989      4.1921        3.74      74      6.0863      2.1105       3.99*      14      0.9842      0.1769
  3.50       51       4.9740      2.1083        3.75      50      4.0720      2.8097       4.00*      14      0.9826      0.8123
  3.51       72       6.9849      2.6963        3.76      63      5.0371      3.8694
