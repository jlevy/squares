                                                          Kinetic Frustration Effects on Dense
                                                      Two-Dimensional Packings of Convex Particles
                                                          and Their Structural Characteristics
                                                      Charles Emmett Maher,† Frank H. Stillinger,† and Salvatore Torquato∗,†,‡,¶,§
arXiv:2103.06290v1 [cond-mat.soft] 10 Mar 2021




                                                      †Department of Chemistry, Princeton University, Princeton, New Jersey 08544, United
                                                                                              States
                                                    ‡Department of Physics, Princeton University, Princeton, New Jersey 08544, United States
                                                     ¶Princeton Institute for the Science and Technology of Materials, Princeton University,
                                                                           Princeton, New Jersey 08544, United States
                                                     §Program in Applied and Computational Mathematics, Princeton University, Princeton,
                                                                                 New Jersey 08544, United States

                                                                                   E-mail: torquato@princeton.edu


                                                 Abstract                                              and “ice cream cone” (a semicircle grafted onto
                                                                                                       an isosceles triangle) shaped particles, with a
                                                 The study of hard-particle packings is of fun-        wide range of packing fractions and degrees of
                                                 damental importance in physics, chemistry, cell       order. To quantify these kinetic effects, we in-
                                                 biology, and discrete geometry. Much of the           troduce the kinetic frustration index K, which
                                                 previous work on hard-particle packings con-          measures the deviation of a packing from its
                                                 cerns their densest possible arrangements. By         maximum possible packing fraction. To inves-
                                                 contrast, we examine kinetic effects inevitably       tigate how kinetics affect short- and long-range
                                                 present in both numerical and experimental            ordering in these packings, we compute their
                                                 packing protocols. Specifically, we determine         spectral densities χ̃V (k) and characterize their
                                                 how changing the compression/shear rate of a          contact networks. We find that kinetic effects
                                                 two-dimensional packing of noncircular parti-         are most significant when the particles have
                                                 cles causes it to deviate from its densest pos-       greater asphericity, less curvature, and less ro-
                                                 sible configuration, which is always periodic.        tational symmetry. This work may be relevant
                                                 The adaptive shrinking cell (ASC) optimiza-           to the design of laboratory packing protocols.
                                                 tion scheme maximizes the packing fraction of
                                                 a hard-particle packing by first applying ran-
                                                 dom translations and rotations to the parti-          1     Introduction
                                                 cles and then isotropically compressing and
                                                 shearing the simulation box repeatedly until          Dense hard-particle packings have been em-
                                                 a possibly jammed state is reached. We use            ployed to model the behavior of simple liquids,
                                                 a stochastic implementation of the ASC op-            glasses, and crystalline states of matter, 1–4 het-
                                                 timization scheme to mimic different effective        erogeneous materials, 3 granular media, 5 biolog-
                                                 time scales by varying the number of parti-           ical systems, 6–8 and many other physical phe-
                                                 cle moves between compressions/shears. We             nomena; see also refs 9 and 10. A hard-particle
                                                 generate dense, effectively jammed, monodis-          packing is a collection of nonoverlapping ob-
                                                 perse, two-dimensional packings of obtuse sca-        jects in d-dimensional Euclidean space Rd . The
                                                 lene triangle, rhombus, curved triangle, lens,        packing fraction φ is the fraction of space these

                                                                                                   1
particles occupy. A considerable amount of                such packings can aid in the design of experi-
work on such packings in both two 9–14 and three          ments involving packings at interfaces for exam-
dimensions 9–11,15–19 concerns ordered packings.          ple, using Langmuir-Blodgett troughs to syn-
  Sufficiently slow compression protocols tend            thesize monolayers 39,40 or to verify the results
to produce the densest packings, which are                of experimental two-dimensional packings. 41
periodic in low space dimensions. 9–11 Increas-             It is important to obtain a more complete
ing the compression rate can result in defec-             understanding of kinetic effects due to their
tive crystalline, polycrystalline, and even glassy        ubiquity in numerical and experimental hard-
states, 9 including maximally random jammed               particle packing protocols. Specifically, we ex-
(MRJ) states. 20 Qualitatively, MRJ packings              amine the extent to which kinetic effects cause
are maximally disordered and mechanically                 deviations, in packing fraction and order, with
rigid systems that can be used to emulate                 respect to the corresponding densest possible
structural glasses. 9,20 Such packings are known          configuration of a two-dimensional monodis-
to be hyperuniform, meaning their infinite-               perse hard-particle packing as a function of the
wavelength density fluctuations are anoma-                particle shape.
lously suppressed compared to those in typical              In this work, we use a stochastic search imple-
disordered systems. 21–23                                 mentation of the adaptive shrinking cell (ASC)
  Disorder can occur in dense, jammed                     optimization scheme 14,16,42,43 to generate dense
monodisperse sphere packings in R3 as a re-               packings of convex, noncircular objects. In this
sult of geometrical frustration. A packing is             algorithm, the packing fraction is maximized by
geometrically frustrated if the local densest             sequentially applying random translations and
packing arrangement is incompatible with the              rotations to hard particles in a periodic funda-
global densest packing arrangement. These                 mental cell, which is subsequently isotropically
sphere packings are geometrically frustrated              compressed (or dilated) and sheared. These
because the densest local arrangement, which is           steps are repeated until the increase in pack-
tetrahedral, cannot optimally fill the space, 3,24        ing fraction is less than a small numerical toler-
and thus is inconsistent with the global densest          ance, at which point the packing is considered
arrangements, the FCC lattice and its stack-              effectively jammed (within some tolerance). We
ing variants. 25 Monodisperse packings of many            mimic different effective time scales to exam-
other particle shapes in R3 are known to have             ine kinetic effects using this implementation by
MRJ states including ellipsoids, 26 superballs, 27        modulating the number of particle moves be-
the Platonic solids, 28 and truncated tetrahe-            tween compression/shear steps. We determine
dra. 29                                                   how the degree of rotational symmetry of a par-
  Monodisperse circular disks in R2 lack geo-             ticular shape, curvature, and asphericity im-
metrical frustration because their densest local          pact packing kinetics by studying packings of
packing is consistent with the densest global             rhombi, obtuse scalene triangles, lenses, curved
packing, which is the triangular lattice. 3 As a          triangles, 14 and so-called “ice cream cones”.
result, use of garden-variety compression algo-             To contrast with geometrical frustration, we
rithms produces dense packings that are poly-             introduce the idea of kinetic frustration, which
crystalline with a probability of nearly unity. 30        is the deviation of a packing from its densest
Bidisperse disks and superdisks in R2 , however,          possible configuration caused by the compres-
are known to form disordered, jammed pack-                sion rate. We characterize the degree of kinetic
ings. 31–33                                               frustration using the kinetic frustration index
  Packings of particles in two dimensions are             K (defined in section 2.2), which measures the
of particular interest because of their ability           deviation of a packing from its maximum pos-
to model thin films, 34 single-layer molecular            sible packing fraction. We determine the effect
adsorption onto flat substrates, 35,36 and two-           of asphericity, curvature, and rotational sym-
dimensional biological systems like epithelial            metry on K. To quantify the degree of short-
cells. 37,38 Characterization of kinetic effects in       and long-range translational and orientational

                                                      2
order in these packings, we compute their spec-            vais lattice (or, simply, lattice) packing. More
tral densities χ̃V (k) (defined in section 2.4).           generally, if P can be decomposed into a set of
The spectral density is the Fourier transform of           N ≥ 1 distinct lattice packings all with the same
the autocovariance of the phase indicator func-            lattice vectors, P is said to be a periodic pack-
tion and can be obtained from scattering ex-               ing with an N-particle basis. A periodic pack-
periments. 3,44 We also determine the type and             ing with a two-particle basis of particular im-
number of contacts in each packing to within a             portance is the double lattice packing, examples
small numerical tolerance (see section 2.5) and            of which are given in section 2.6.2. A packing
determine the resulting contact network. We                P is a double lattice packing if P can be de-
use the contact networks to determine how the              composed into two lattice packings, P0 and P1 ,
average number of constraints on each particle             such that an inversion around some point in
ZC (see section 2.3) and the fraction of particles         the space interchanges P0 and P1 . For each of
that can freely move within cages of the jammed            these periodic packings, there is an associated
backbone, or rattlers, vary as a function of com-          fundamental cell F , parallelotopic in shape, de-
pression rate and particle shape. We expect the            fined by the lattice matrix Λ = {p1 , p2 , ..., pd }
examination of such kinetic effects on this large          containing all N particle centroids. The pack-
collection of shapes to be relevant to the design          ing fraction, φ, is the fraction of space that the
of experimental packing protocols.                         particles cover. For a monodisperse periodic
  The rest of the paper is organized as follows.           packing with an N -particle basis φ is given by
Section 2 contains the background pertaining to
and the mathematical definitions of the meth-                                       N v1
                                                                              φ=                           (1)
ods used to produce and characterize the dense                                     Vol(F )
particle packings. Section 2.5 describes the
                                                           where v1 is the volume of a single d-dimensional
ASC scheme and its adaptation used here to
                                                           particle and Vol(F ) is the d-dimensional volume
generate particle packings with different com-
                                                           of the fundamental cell.
pression rates. Section 2.6 defines the noncir-
cular particle shapes considered in this work as
well as information about the densest packings             2.2    Kinetic Frustration
for shapes that do not tile the plane. In section          The focus of this work is the characterization of
3, we present results for the kinetic frustration          dense hard-particle packings generated by us-
and degree of order/disorder in the final pack-            ing packing protocols with different compres-
ings. We then offer conclusions and plans for              sion rates. Kinetic frustration is the deviation
future research in section 4.                              of a packing from its densest possible configura-
                                                           tion caused by the compression rate. To quan-
2     Computational Details                                tify this, we define the kinetic frustration index
                                                           K:
                                                                                        φ
2.1    Packings                                                              K =1−                        (2)
                                                                                       φmax
Here, we give the pertinent definitions follow-            where φmax is the maximum possible pack-
ing closely refs 9 and 14. A lattice Λ in Rd               ing fraction associated with a given packing.
is a subgroup comprising integer linear combi-             Larger values of K indicate larger deviations
nations of a set of d vectors, {p1 , p2 , ..., pd },       from the maximum possible packing fraction.
which are a basis for Rd . This, in the physical           Knowledge of K as a function of particle shape
sciences and engineering, is termed a Bravais              and compression rate may be relevant to the de-
lattice. A packing, P , is a collection of nonover-        sign of laboratory packing protocols. Addition-
lapping particles in Rd . If all members of P are          ally, we compute the spectral density (defined
translates of each other, where the vectors of             below) of each packing to quantify the degree
translation form a lattice, P is known as a Bra-           of short- and long-range ordering and determine


                                                       3
how ordering is correlated to K.                          In the infinite-particle-number limit, the aver-
                                                          age number of constraints per particle ZC in
2.3    Jamming Categories and Iso-                        an isostatic packing is equal to twice the num-
                                                          ber of degrees of freedom per particle f (i.e.,
       staticity                                          ZC = 2f ). 9,28 Packings with more constraints
Jammed hard-particle packings are those in                than isostatic ones are hyperstatic, and those
which mechanical stability of a specific type is          having fewer constraints are hypostatic. While
conferred to the packing via interparticle con-           MRJ sphere packings in three dimensions 50–53
tacts. 9 Three broad and mathematically pre-              and MRJ disk packings in two dimensions 30 are
cise jamming categories can be distinguished              isostatic, this is not generally true of all MRJ
based on the nature of the mechanical stability           packings. In particular, certain aspherical par-
conferred, which in order of increasing stability         ticles with smooth boundaries, like ellipsoids, 26
are as follows: 9,45 (1) Local jamming: no indi-          superellipsoids, 54 and superballs, 27 have hypo-
vidual particle can be moved while holding all            static MRJ packings. In the two-dimensional
other particles fixed. (2) Collective jamming:            packings considered herein, edge-to-edge con-
the packing is locally jammed, and no collec-             tacts impose two constraints on each particle,
tive motion of a finite subset of particles is pos-       and all other contact types (e.g., vertex-to-
sible. (3) Strict jamming: the packing is col-            edge) impose one constraint on each particle.
lectively jammed and all volume-nonincreasing               In practice, jammed hard-particle packings
deformations are disallowed by the impenetra-             produced via simulations or experiments con-
bility constraint. A special jammed state is              tain a small concentration of rattlers, which
the maximally random jammed (MRJ) state,                  are not jammed but are locally imprisoned
which is defined as the most disordered con-              by neighboring jammed particles. 9,20 None of
figuration (as measured by a set of scalar order          the three jamming definitions above permit the
metrics) subject to a particular jamming cate-            presence of rattlers. Nevertheless, it is the sig-
gory. 20 Such packings are known to possess hy-           nificant majority of hard particles that con-
peruniform density fluctuations. 22,46–48                 fers rigidity to the packing, and in any case,
  Jammed packings are also characterized by               the rattlers could be removed (in computer
the number of constraints imposed by interpar-            simulations) without disrupting the remaining
ticle contacts relative to the number of degrees          jammed particles. 9 The rattler fraction, φR , is
of freedom (DOF) in the packing. In hard disk             greatest in sphere packings in any dimension
or ellipse packings, for example, each interpar-          and is significantly decreased when rotational
ticle contact occurs at a single point and corre-         degrees of freedom are introduced 27 or the spa-
sponds to a single constraint. Faceted particles          tial dimension is decreased. 30 Atkinson et al. 55
can have contacts at more than a single point,            have shown that removal of rattlers from MRJ
e.g., edge-to-edge contacts or face-to-face con-          packings results in a nonhyperuniform packing,
tacts, which impose additional constraints by             meaning that the subset of jammed particles
blocking rotations and must be weighted ac-               alone is far from hyperuniform. In this work we
cordingly when counting the number of con-                consider packings that do not have their rattlers
straints. 49 MRJ sphere packings in R3 , for ex-          removed.
ample, are known to be isostatic, 50–53 meaning
that total number of constraints is equal to the          2.4    Spectral Density
number of DOF in the system. The number of
constraints required for isostaticity will depend         A hard-particle packing can be modeled as a
on the particle shape, jamming category, and              two-phase heterogeneous medium, where the
boundary conditions. For example, an isostatic            matrix phase V1 is the void space between the
strictly jammed disk packing in R2 under peri-            particles and the particle phase V2 is the space
odic boundary conditions must have 2N +1 con-             occupied by the particles, such that V1 ∪ V2 =
straints, where N is the number of particles. 52          V ⊂ Rd . 56 The (micro)structure of the pack-

                                                      4
ing can be fully characterized by a countably                 shape and size distributions possess vanishing
                                                    (i)
infinite set of n-point probability functions Sn ,            infinite-wavelength local-volume-fraction fluc-
defined by 3                                                  tuations and signature quasi-long-range (QLR)
                                  * n            +            pair correlations. These QLR correlations are
                                   Y                          manifested by a linear scaling in the small-
       Sn(i) (x1 , . . . , xn ) =     I (i) (xn ) , (3)
                                                              wavenumber region of χ̃V (k), i.e. χ̃V (k) ∼ k
                               j=1
                                                              as k → 0.
where I (i) is the indicator function for phase i:              In the present work, we consider packings of
                          (                                   N hard particles within a fundamental cell un-
                           1, x ∈ Vi                          der periodic boundary conditions. Under these
              I (i) (x) =                     (4)             conditions, we can express the spectral density
                           0, else.
                                                              χ̃V (k) of a finite hard-particle packing as 47
                 (i)
The function Sn gives the probability of finding                            PN                              2
n points at positions x1 , . . . , xn in phase i. In                         j=1 exp(−ik · rj )m̃(k; Rj )
                                                                χ̃V (k) =                                       (8)
what follows, we drop the superscript i, and                                             V
restrict our discussion to V2 .                                          (k 6= 0),
  For statistically homogeneous media,
Sn (x1 , . . . , xn ) is translationally invariant and,       where {rj } denotes the set of particle centroids,
in particular, the one-point correlation func-                Rj denotes all of the geometrical parameters of
tion is independent of position and equal to the              the particle shape, V is the volume of the sim-
packing fraction                                              ulation box (fundamental cell), and m̃(k; Ri ) is
                                                              the Fourier transform of the particle indicator
                       S1 (x) = φ,                 (5)        function defined as
                                                                                 (
while the two-point correlation function S2 (r)                                    1, r is in particle i
                                                                     m(r; Ri ) =                             (9)
depends on the displacement vector r ≡ x2 −                                        0, otherwise.
x1 . The corresponding two-point autocovari-
ance function χV (r) 3,57,58 is obtained by sub-              The shape of the fundamental cell, defined by
tracting the long-range behavior from S2 (r):                 the lattice vectors {pi }, restricts the wavevec-
                                                              tors such that k · pi = 2πn ∀ i, where n ∈ Z.
                χV (r) = S2 (r) − φ2               (6)        Visualization of the spectral densities allows
                                                              us to examine the degree of short- and long-
The nonnegative spectral density, χ̃V (k), is de-
                                                              range translational and orientational order in
fined as the Fourier transform of χV (r), 3 i.e.,
                                                              the packings. Instead of computing m̃(k; Ri )
                     Z                                        for each particle shape, we take the Fourier
           χ̃V (k) =    χV (r)e−ik·r dk.       (7)            transform of a square pixelization of the pack-
                         Rd
                                                              ing, requiring only m̃(k; Ri ) for a square (see,
A hyperuniform packing is one in which                        e.g., Ref. 60). The angular-averaged spectral
χ̃V (k) → 0 as k → 0. 59                                      densities in this work are ensemble averaged
  Because of the rigidity of MRJ packings and                 over 50 configurations. Accompanying two-
the presence of a well-defined contact network,               dimensional spectral densities are for a sin-
Torquato and Stillinger conjectured that any                  gle, representative configuration in order to ac-
strictly jammed and saturated packing is hy-                  count for important orientational information
peruniform. 21 A saturated packing is one in                  in anisotropic packings, which may be lost upon
which there is no space available to add an-                  angular averaging.
other particle of the same kind to the pack-
ing. Subsequently, Zachary et al. 46–48 have
shown that MRJ packings of hard particles with


                                                          5
2.5    Adaptive Shrinking                       Cell
       (ASC) Optimization
       Scheme
The Torquato-Jiao ASC scheme generates
dense hard-particle packings in a periodic fun-
damental cell by translating and rotating the                        (a)             (b)              (c)
particles while simultaneously shrinking and
                                                              Figure 1: Schematic of a single step of the ASC
deforming the boundary of the fundamental
                                                              optimization scheme. (a) The initial configura-
cell. This process can be formally stated as
                                                              tion of the 4 particles. (b)Two trial moves: a re-
follows: 14
                                                              jected rotation due to violation of the nonover-
 minimize : −φ(rp1 , rp2 , rp3 , . . . , rpN ;                lapping constraints, and an accepted transla-
                  θ1 , θ2 , θ3 , . . . , θN ; Λ),             tion. (c) The result of an accepted trial defor-
                                                   (10)       mation and compression of the packing.
 such that : (Si ∩ Sj ) ⊆ (Γi ∪ Γj )
               ∀ i, j = 1, 2, 3, . . . , N, i 6= j
                                                              translation or rotation with a prescribed max-
where N is the number of particles, rpi and θi                imum magnitude is applied to each of the N
denote the position and orientation of particle               particles a set number of times. A trial move is
i, respectively, Si is the closed set in R2 asso-             accepted if the new particle position does not
ciated with particle i, and Γi is the boundary                overlap any of the other particles or their pe-
of the set Si . This optimization scheme can be               riodic images. Otherwise, the particle is re-
solved by using either stochastic 14,16,42 or lin-            turned to its previous position or orientation.
ear programming 43 techniques. This work uses                 The maximum magnitude of these trial move-
the Monte Carlo implementation described in                   ments is steadily decreased throughout the ex-
ref 14.                                                       ecution of the algorithm by reducing this max-
   The stochastic implementation of this scheme               imum by some constant ratio when the number
in R2 uses a periodic parallelogrammatic fun-                 of moves accepted per “random move” step falls
damental cell. All N particle centroids are                   significantly below 50%.
given in lattice coordinates, which are relative                 During the “random strains” step, the sim-
coordinates with respect to the lattice vectors,              ulation box is both deformed and compressed
i.e., rpi ∈ [0, 1)2 . The particle orientations are           or dilated simultaneously such that the area of
specified by a rotation of a given angle, i.e.,               the box decreases on average, while ensuring the
θi ∈ [0, 2π). Given an initial configuration,                 nonoverlap constraint remains satisfied. These
the stochastic search method uses an iterative                strains effect collective motions on the particles
process to increase the packing fraction by us-               because the centroid positions of the particles
ing the following steps, shown schematically in               are defined in terms of the lattice vectors. The
Figure 1: (1) “Random moves” - Random ro-                     maximum magnitude of a trial strain and the
tations or translations are applied to the par-               maximum number of trials are prescribed. The
ticles. These moves are only accepted if the                  first trial that does not violate the nonoverlap
resulting configuration satisfies the nonoverlap              constraints is accepted. After each unsuccessful
constraints. (2) “Random strains” - A random                  trial, the maximum magnitude of the strain is
strain comprising a deformation and dilation or               decreased until either a trial is accepted or the
compression is applied to the simulation box.                 maximum number of trials has been attempted.
This strain will either increase or decrease the              When either of these conditions is met, we re-
area of the fundamental cell with some specified              turn to the first step of the scheme and the
probability, corresponding to uphill or downhill              maximum magnitude of the strain is reset to
moves, respectively.                                          the value from the beginning of the step.
   During the “random moves” step, a trial                       The linear programming solution to the ASC

                                                          6
scheme was designed to produce the inher-                ing is considered effectively jammed. We use a
ent structure associated with an initial, un-            coarser tolerance for faceted particles due to the
jammed, sphere packing. 43 An inherent struc-            increased computational cost associated with
ture is a minimum in the energy landscape. 61,62         the additional rotational constraints imposed
For packings, this corresponds to a mechani-             by flat edges as jamming is approached. Ki-
cally rigid and locally maximally dense config-          netic frustration and contact network results
uration. 43,63 These inherent structures vary in         for each combination of particle shape (see sec-
their packing fraction and degree of order, and          tion 2.6) and compression schedule are averaged
the number of possible inherent structures in-           over three configurations.
creases with N . The linear programming solu-
tion given by Torquato and Jiao in ref 43 guar-          2.6     Particle Shapes
antees with a high probability the generation
of a jammed sphere packing across dimensions             Here, we mathematically define the particle
for d ≥ 2, with a wide variety of packing frac-          shapes studied in this work. Additionally, we
tions and degrees of order. An inherent struc-           state the maximum packing fractions φmax of
ture is highly dependent on its initial configura-       these shapes, which are required to compute the
tion, and thus unusual initial configurations in         kinetic frustration index K (cf. eq 2), as well
principle allow one to obtain unusual inherent           as relevant geometrical properties. One such
structures.                                              property is the asphericity γ defined as 16,42
  In the present work we apply the ASC scheme                             rsmallest bounding circle
to monodisperse packings of 504 particles. To                        γ=                                 (11)
                                                                          rlargest inscribable circle
minimize the effect of the initial conditions, we
use a random sequential addition process 3 to            We examine obtuse scalene triangles, rhombi,
place particles in a square box with random              and curved triangles. Each of these shapes has
orientations such that the initial φ is several          a known φmax . We also study lenses and “ice
orders of magnitude smaller than φmax . Sim-             cream cones.” To our knowledge the φmax of
ulations are terminated when φ increases less            these shapes is unknown.
than 10−10 over the course of 100 “random
strain” steps, at which point it is assumed φ            2.6.1   Shape Definitions
has reached a local maximum. To impose dif-
ferent effective time scales (compression rates),        Rhombi. A rhombus is a quadrilateral with
we use “slow”, “medium”, and “fast” compres-             four equal sides, an example of which is given
sion schedules, in which there are 1000, 100,            in Figure 2a. The angle θRh ∈ (0◦ , 90◦ ], gen-
and 10 trial moves per particle in the “random           erating rhombi that interpolate between a thin
moves” step, respectively. The three schedules           line and a square. Rhombi have D2 symmetry,
have identical movement and strain magnitudes            except for in the square limit, where they have
and move strictly downhill (i.e., no “random             D4 symmetry. We generate packings of rhombi
strain” step increases the area of the simulation        with θRh = {30, 40, 50, 60, 70, 80}, which have
box). To generate the contact network, we take           γ = {3.86, 2.92, 2.37, 2.00, 1.74, 1.56}, respec-
the dense output from the procedure above and            tively. φmax = 1 for all rhombi.
use a fourth “contact generation” schedule with
much smaller movement and compression/shear              Obtuse Scalene Triangles. An obtuse sca-
magnitudes. This fourth schedule is termi-               lene triangle (OST) has three unequal sides and
nated when the interparticle distances (exclud-          one angle greater than 90◦ , an example of which
ing rattlers) are smaller than 10−10 D0 for par-         is given in Figure 2b. We base our OSTs on
ticle shapes composed of arcs and 6 × 10−10 D0           the first candidate from ref 64, which has an-
for particle shapes containing flat edges, where         gles of 18.6◦ , 45◦ , and 116.4◦ . Here, we chose
D0 is the largest distance from the particle cen-        that the ratio of the lengths of sides C1 and
troid to its boundary, at which point the pack-

                                                     7
                                                                                  r
                                                                                            r0
                                             OST

                                     c1                     c2
            θRh
                                                     c3
                  (a)                               (b)                                    (c)




                                                   θICC



                    b                                                                               h
                                                        r                                  win

                        a

                                                                                        wout
                  (d)                               (e)                                    (f)

Figure 2: Geometrical properties of the (a) rhombi, (b) obtuse scalene triangles, (c) curved triangles,
(d) lenses, (e) ice cream cones, and (f) bowties examined in this work. Shapes (a) - (e) are the
convex bodies examined in the main body of this work, and object (f) is a concave body discussed
briefly in section 4. Objects (a), (b), and (f) tile the plane, while (c) - (e) do not. Only (b) is chiral,
and racemic mixtures of this object are discussed briefly in section 4.


C2 is 2.216, as they are in the obtuse first can-           ure 2c. CTs are characterized by a curvature
didate and vary θOST ∈ (90◦ , 180◦ ). All OST               parameter, κ, given by
have C1 symmetry. All simulations containing                                          r0
OSTs are enantiopure, except for those in sec-                                   κ=                      (12)
                                                                                      r
tion 4. We generate packings of OSTs with
θOST = {100, 110, 120, 130, 140} which have                 where r0 is the circumradius of the CT and r
γ = {3.44, 3.89, 4.51, 5.37, 6.73}, respectively.           is the radius of the overlapping circles. Thus,
φmax = 1 for all OSTs.                                      CTs interpolate between a circle at κ = 1
                                                            and an√ equilateral triangle at κ = 0. At
Curved Triangles. A curved triangle (CT)                    κ = 1/ 3 the particle shape is the same as the
is the convex intersection of three congruent               well-known Reuleaux triangle. 65 CTs have D3
circles placed at the vertices of an equilateral            symmetry. We generate√packings of CTs with
triangle, 14 an example of which is given in Fig-           κ = {1/5, 7/20, 1/2, 1/ 3, 13/20, 4/5} which
                                                            have γ = {1.74, 1.58, 1.43, 1.37, 1.30, 1.18}, re-

                                                    8
spectively. CTs do not tile the plane, and their
φmax is given in in ref 14.

Lenses. A lens is the intersection of two con-
gruent circles, an example of which is given in
Figure 2d. Lenses are characterized by an as-
pect ratio, α, given by
                           a
                      α=                      (13)
                           b
where a is the minor axis and b is the major              Figure 3: Fundamental basis of the putative
axis. Lenses have D2 symmetry, except in the              densest α = 0.5 lens packing.
case of the α = 1 limit, where the circle has
O(2) symmetry. We generate packings of lenses
with α = {4/5, 2/3, 1/2, 1/3, 1/5} which have
γ = {1.25, 1.5, 2, 3, 5}, respectively. The φmax
of lenses is, to our knowledge, undetermined.
We give the putative φmax and corresponding
structure in section 2.6.2.

Ice Cream Cones. An “ice cream cone”
(ICC) is an isosceles triangle with a semi-
circle grafted onto its base, an example of
which is given in Figure 2e. The diame-
ter of this semicircle is equal to the length
                                                          Figure 4: Putative maximum packing fraction
of the base of this isosceles triangle, and the
                                                          φmax as a function of α for the dense packings
union of the two regions is convex. The angle
                                                          of lenses.
θICC ∈ (0◦ , 180◦ ], generating ICCs that inter-
polate between an infinitely tall isosceles tri-
angle in the θICC → 0◦ limit and a semicir-               parameter β, given by
cle when θICC = 180◦ . ICCs have D1 sym-                                          win
metry. We generate packings of ICCs with                                     β=        .             (14)
                                                                                  wout
θICC = {30◦ , 60◦ , 90◦ , 120◦ , 150◦ , 180◦ } with
γ = {2.43, 1.5, 1.21, 1.37, 1.60, 2}, respectively.       In principle, the aspect ratio of the bowtie
The φmax of ICC is, to our knowledge, undeter-            can be arbitrary,   but here we choose it such
                                                                     √
mined. We give the putative φmax and corre-               that h = 3wout . Thus, the bowties interpo-
sponding structures in section 2.6.2.                     late between a rectangle when β = 1 and two
                                                          equilateral triangles attached at a vertex when
Bowties. “Bowties” are rectangles with con-               β = 0. All bowties herein have D2 symmetry,
gruent isosceles triangles taken out of both long         and φmax = 1.
sides such that the resulting shape is an irreg-
ular hexagon; this is illustrated in Figure 2f.           2.6.2   Putative Densest Packings
Bowties are not discussed in the main body of
this work due to our focus on convex shapes but           Here, we follow the procedure given in ref 14
have their kinetics discussed briefly in section          to generate dense periodic packings of lenses
4. We characterize bowties with a thickness               and ICC to inform analytical predictions for
                                                          the φmax of these shapes and the corresponding
                                                          structures. We present the smallest periodic re-
                                                          peat units, or fundamental bases, of these dense

                                                      9
                                                          Figure 6: Putative maximum packing fraction
          (a)                         (b)
                                                          φmax as a function of θICC for both types of
Figure 5: Fundamental bases for (a) a type 1              dense ice cream cone packings.
(θICC = 120◦ ) ice cream cone packing and (b)
a type 2 (θICC = 60◦ ) ice cream cone packing.
                                                          densest for ICCs with small θICC . The funda-
                                                          mental bases of both packing types are shown
packings, as well as the analytically determined          in Figure 5. Figure 6 shows φmax for all val-
φmax as a function of the relevant geometrical            ues of θICC . In type 1 packings, φmax does not
parameter (α for lenses, θICC for ICC).                   vary monotonically, and in the semicircle limit
                                                          (θICC → 180◦ ), φ = 0.935931, a value that is
Lenses The putative densest arrangement of                consistent with the exact result given in ref 67,
lenses is consistent with Fejes Tóth’s theorem           namely
that the densest packing of a centrally symmet-                         π
ric convex particle is a lattice packing. 13 Fig-             φ= √            π
                                                                                 = 0.9359311 . . .    (15)
                                                                     3 + 5tan 10
ure 3 shows the fundamental basis for lenses
with α = 0.5. The analytically derived φmax               This level of agreement with the theoretical
for lenses is given
                  √ in Figure 4. The φmax has             prediciton is a testament to the efficacy of the
a maximum of 2 3 2 in the α → 0 limit and de-             ASC scheme to produce the densest jammed
creases monotonically as a function of α. We              packing. Moreover, in type 2 packings φmax
find that this packing is consistent with the tri-        decreases monotonically with θICC and reaches
angular lattice√ in the limit of α = 1 (circles)          unity in the limit of θICC → 0.
with φmax = π 6 3 .

Ice Cream Cones The putative densest                      3    Results and Discussion
packings of ICCs are consistent with the conjec-
                                                          Here, we use the stochastic solution to the
ture that noncentrally symmetric objects have
                                                          ASC scheme and the three compression sched-
their maximum densities realized in a two-
                                                          ules described in section 2.5 to generate dense
particle basis double lattice packing (defined
                                                          monodisperse packings of the shapes described
in section 2.1). 66 We have found two distinct
                                                          in section 2.6. We then characterize the kinetic
packing behaviors, which we name “type 1” and
                                                          frustration, degree of short- and long-range or-
“type 2” packings, both of which are consistent
                                                          der via the spectral density, and contact net-
with the theorem due to Kuperberg and Kuper-
                                                          works in these packings as a function of particle
berg 66 stating that each two-dimensional con-
                                                          shape and compression rate.
vex body
      √ admits a double lattice packing with
φ > 3/2. Type 1 packings are densest for
ICCs with large θICC , and type 2 packings are


                                                     10
                   0.2                                        0.2
                                           Fast
                  0.15                     Medium            0.15
                                           Slow


              K




                                                         K
                   0.1                                        0.1

                  0.05                                       0.05
                                                                     Fast    Medium    Slow
                    0                                          0
                    30   40   50 60         70      80         100     110    120     130   140
                                θRh                                           θOST
                              (a)                                            (b)




                              (c)                                            (d)

                                    0.09

                                    0.06
                                K




                                    0.03
                                             Fast    Medium         Slow
                                      0
                                      30      60     90 120 150 180
                                                       θICC
                                                     (e)

Figure 7: Kinetic frustration index K for (a) rhombi as a function of θRh , (b) OST as a function of
θOST , (c) CT as a function of κ, (d) lenses as a function of α, and (e) ICC as a function of θICC .


3.1    Kinetic Frustration                                 3.1.1     Symmetry
The kinetic frustration index K as a function of           The packings of OST, which are the least sym-
the particle shape and compression rate is given           metric particles studied here, tend to have a
in Figure 7, which shows that K increases as the           larger K than other packings (see Figure 7b).
compression rate increases, regardless of parti-           This can be directly contrasted with the results
cle shape. Three shape properties that have a              for the packings of rhombi, which have 2-fold
demonstrable effect on K are rotational sym-               rotational symmetry (see Figure 7a), and tend
metry, curvature, and asphericity γ.                       to have much lower values of K. Comparison of
                                                           CT and lens results (see Figures 7c and 7d, re-
                                                           spectively) indicates curved shapes with similar


                                                     11
                                                    (a)




                                                    (b)

Figure 8: Example representative configurations (left), corresponding two-dimensional (center),
and angular averaged spectral densities (right) χ̃V (k) /D2 vs dimensionless wavenumber kD from
OST packings: (a) θOST = 100◦ OST compressed using the fast schedule and (b) θOST = 140◦ OST
compressed using the slow schedule, where D is the circumradius of the particle.


γ have similar K, despite having different de-            it does as θICC deviates from 90◦ toward 180◦
grees of rotational symmetry. Thus, increased             (see Figure 7e). This behavior is attributed
rotational symmetry reduces the kinetic frus-             to the fraction of the shape perimeter that is
tration of polygonal particle shapes but does             curved going to zero as θICC goes to 0◦ .
not significantly affect curved particle shapes.
                                                          3.1.3   Asphericity
3.1.2   Curvature
                                                          Rhombus and lens packings show an increase
Directly comparing packings of curved (e.g.,              in K as γ increases, indicating that greater as-
Figure 7d) and faceted shapes (e.g., Figure 7a)           phericity results in greater kinetic frustration.
shows that for shapes with similar γ K is lower           This trend can also be observed in Figure 7e
in packings of curved shapes. This is also ev-            where both γ and K increase as θICC deviates
ident in CT packings (see Figure 7c) where                from 90◦ . Rapidly compressed OST packings
smaller κ (particle curvature) tends to result in         also exhibit this behavior (see Figure. 7b), but
larger K. This is not observed in slowly com-             more slowly compressed OST packings do not
pressed CT packings in the κ → 0 limit due                due to the emergence of 2-fold orientational or-
to the emergence of 6-fold orientational order            der (see section 3.2).
(see section 3.2). In ICC packings, K increases
faster as θICC deviates from 90◦ toward 0◦ than

                                                    12
                                                   (a)




                                                   (b)




                                                   (c)

Figure 9: Example representative configurations (left), corresponding two-dimensional (center), and
angular averaged spectral densities (right) spectral densities χ̃V (k) /D2 vs dimensionless wavenum-
ber kD from rhombus packings: (a) θRh = 30◦ rhombi compressed using the fast schedule, (b)
θRh = 80◦ rhombi compressed using the fast schedule, and (c) θRh = 80◦ rhombi compressed using
the slow schedule, where D is the circumradius of the particle.


3.2    Spectral Density                                  tion of compression rate and particle shape.
                                                         Here, we examine both two-dimensional and an-
Through visualization of the spectral density we
                                                         gular averaged χ̃V (k).
characterize the short- and long-range transla-
                                                           There does not appear to be significant short-
tional and orientational order in the packings
                                                         range translational order in any of the OST
produced through the ASC scheme as a func-
                                                         packings, shown by the lack of distinct peaks in


                                                   13
                                                  (a)




                                                  (b)




                                                  (c)

Figure 10: Example representative configurations (left), corresponding two-dimensional (center),
and angular averaged spectral densities (right) densities χ̃V (k) /D2 vs dimensionless wavenumber
kD from CT packings: (a) κ = 0.35 CT compressed using the slow compression schedule, √(b)
κ = 0.5 CT compressed using the fast compression schedule, and (c) Reuleaux triangles (κ = 1/ 3)
compressed using the slow compression schedule, where D is the circumradius of the particle.


the angular-averaged spectral densities in Fig-         nematic (2-fold) orientational order in OST
ure 8. Broad peaks close to the origin indi-            packings increases as θOST increases and as
cate that there are large-scale density fluctu-         the compression rate decreases. This behav-
ations in these OST packings, which dimin-              ior is exemplified by the non-radially symmetric
ish in intensity as kD increases. Short-range           two-dimensional spectral density in Figure 8b,


                                                  14
                                                   (a)




                                                   (b)




                                                   (c)

Figure 11: Example representative configurations (left), corresponding two-dimensional (center),
and angular averaged spectral densities (right) spectral densities χ̃V (k) /D2 vs dimensionless
wavenumber kD from ICC packings: (a) θICC = 180◦ ICC compressed using the fast compres-
sion schedule, (b) θICC = 90◦ ICC compressed using the medium compression schedule, and (c)
θICC = 30◦ ICC compressed using the fast compression schedule, where D is the circumradius of
the particle.


which is lost upon angular averaging.                    sity in the center panel of Figure 9c indicates
  In rhombus packings, the degree of short-              short- and long-ranged translational and ne-
range translational order increases with the             matic orientational order. However, the large
value of θRh . The two-dimensional spectral den-         fluctuations in the distances between defects re-

                                                   15
                                                   (a)




                                                   (b)




                                                   (c)

Figure 12: Example representative configurations (left), corresponding two-dimensional (center),
and angular averaged spectral densities (right) spectral densities χ̃V (k) /D2 vs dimensionless
wavenumber kD from lens packings: (a) α = 0.8 lenses compressed using the slow compression
schedule, (b) α = 0.666... lenses compressed using the medium compression schedule, and (c)
α = 0.2 lenses compressed using the slow compression schedule, where D is the circumradius of the
particle.


sults in an angular-averaged spectral density            peaks. The high scattering intensity near the
that appears to lack translational order (see            origin in the right panels of Figure 9 indicates
right panel of Figure 9c). Otherwise, as θRh in-         large-scale density fluctuations that decrease in
creases, the spectral densities begin to exhibit         intensity as kD increases. In the right panel of


                                                   16
Figure 9b there is a peak at kD ∼ 6, which cor-
responds to density fluctuations on the order of
the size of a single rhombus. Slowly compressed
packings of rhombi exhibit short-range nematic
orientational order (see center panels of Figures
9a and 9c), which is lost up angular averaging.
As the compression rate increases, the packings
become more isotropic (see center panel of Fig-
ure 9b). We also observe that these packings are
polycrystalline, and slowly compressed rhombi
with small γ tend to exhibit point-like defects,
while lager compression rates and γ result in
grain boundary-like defects.
   All CT packings exhibit a significant degree
of short-range translational order, shown by the
peaks in the right panels of Figure 10. The
first peak in the right panels of Figure 10 cor-
responds to a length scale associated with the
distance between neighboring voids between the
particles. In right panel of (c) of Figure 10 the
split second peak corresponds to length scales
associated with the height of the CT and the
side length of the CT. Short-range 6-fold orien-
tational order that is lost upon angular averag-
ing emerges when the packings are compressed
more slowly (see center panels of Figures 10a
and ??c), while fast compressions can result in
isotropic packings (see center panel of Figure
10b). As κ increases, the six-fold orientational
order increases in range, shown by the sharp-
ening of the Bragg peaks in the center panel of
Fig. 10c.
   Packings of ICC with θICC = 90◦ have short-
range translational and 6-fold orientational or-
der that is lost upon angular averaging at all
compression rates (see Figure 11b). The first
peak in the corresponding angular-averaged
spectral density corresponds to distance asso-
ciated with neighboring voids. As θICC devi-
ates from 90◦ , the spectral densities become
isotropic and exhibit less short-range transla-          Figure 13: A representative configuration (top),
tional order, which is shown by the disappear-           the corresponding two-dimensional (middle),
ance of the peaks in the right panels of Figures         and the angular averaged (bottom) spectral
11a and 11c. The broad peaks in these figures            density χ̃V (k) /D2 vs dimensionless wavenum-
are associated with the greater asphericity of           ber kD for a rapidly compressed packing of
the particle shape, resulting in more widely dis-        α = 0.5 lenses, where D is the circumradius
tributed distances between neighboring voids.            of the particle.
The the sharpness of the peak in the right
panel of Figure 11a, compared to that of the

                                                    17
right-hand panel of Figure 11c indicates greater
translational order in the θICC → 180◦ limit
than the θICC → 0◦ limit. Inspection of the
left panel of Figure 11a shows that at large φ,
semicircles do not form circular dimers which
could then pack in a triangular lattice, as one
may first surmise, suggesting these objects may
posses a rich equilibrium phase behavior.
  Lens packings with α > 0.5 exhibit an in-
crease in short-range 6-fold orientational order,
which increases in range as the compression rate                                 (a)
decreases, shown by the well-defined peaks in
the angular-averaged spectral density in right
panel of Figure 12a. As α decreases, the de-
gree of short-range 6-fold orientational order de-
creases, shown by the broadening of the peaks
in Figure 12b. In these two figures, the first
peaks correspond to nearest-neighbor void dis-
tances. For α close to zero, the packings exhibit
short-range nematic orientational order (see the
center panel of Figure 12c). The 6-fold (in Fig-
ure 12a,b) and nematic (in Figure 12c) orien-
tational order in these packings is lost upon
                                                                                 (b)
angular averaging. The corresponding angular-
averaged spectral density shows large-scale den-          Figure 14: Average number of constraints per
sity fluctuations, which do not decrease in in-           particle ZC in the packings of lenses and CT
tensity until a length scale associated with the          (ignoring rattlers) as a function of (a) α and
the minor axis of the lens.                               (b) κ.
  It is worth noting that rapidly compressed
packings of lenses with α = 0.5 have isotropic
spectral densities that exhibit little short-range        ref 69 can thus potentially be used to predict
translational order (see Figure 13). The peak             the translational and orientational order in a
in the angular-averaged spectral density is asso-         jammed lens packing by determining if a given
ciated with the nearest-neighbor void distances           α should result in a plastic-to-solid, isotropic-
and is broadened due to the orientational dis-            to-solid, or nematic-to-solid phase transition.
order in the packing and the anisotropy of the            In addition, studying the structural changes of
particle shape. In addition, χ̃V (k) becomes              these dense packings upon decompression can
nearly zero (≈ 0.001), i.e., nearly hyperuni-             allow one to qualitatively characterize the equi-
form, 55 as k approaches 0, implying a suppres-           librium melting properties of such particles. 70
sion of long-wavelength density fluctuations.               Thus, we find that slower compression rates
This indicates lenses with α = 0.5 are a reason-          tend to result in longer-range translational and
able candidate for a particle shape that readily          orientational order. Moreover, we find that
forms monodisperse disordered jammed pack-                packings with large K (see section 3.1) tend to
ings, an area of current interest. 30 In three di-        exhibit less short-range translational and orien-
mensions, the phase diagrams of oblate ellip-             tational order.
soids and lenses are known to closely resem-
ble each other but begin to differ in the hard-
sphere limit and for φ in the crystalline solid
range. 68 The phase diagram for hard ellipses in

                                                     18
                      (a)
                                                                             (a)




                      (b)
                                                                             (b)
Figure 15: Rattler fraction φR in the packings
of lenses and CT as a function of (a) α and (b)        Figure 16: (a) Average number of constraints
κ.                                                     per particle ZC (ignoring rattlers) and (b) rat-
                                                       tler fraction φR in the OST packings as a func-
                                                       tion of θICC .
3.3    Contact Statistics
In each of the packings produced by using the
                                                       while all other OST packings are hypostatic.
ASC scheme, we count the number of each type
                                                       OST packings have greater ZC than packings
of contact to determine the contact networks
                                                       of curved objects, which is attributed to the
and rattler fraction φR . We then examine how
                                                       edge-to-edge contacts only present in packings
the average number of constraints per particle
                                                       of faceted particles. Additionally, we see that
ZC and rattler fraction φR change as a function
                                                       φR increases as the packings are compressed
of the particle shape and compression rate.
                                                       more rapidly and as γ decreases.
  Figure 14 shows that lens and CT packings
                                                         Thus, we find that ZC tends to increase as
are hypostatic, and ZC decreases as the com-
                                                       the compression rate decreases and γ increases.
pression rate increases. We also observe that
                                                       Moreover, φR tends to increase as the compres-
ZC decreases in rapidly compressed packings of
                                                       sion rate increases and as γ decreases.
lenses with small α and CT with small κ be-
cause of their larger asphericities γ (see Fig-
ure 14). Figure 15 demonstrates that φR in             4    Conclusions
these packings tends to increase as the packing
is compressed more rapidly and as γ decreases.         Kinetic effects are ubiquitous in both numerical
  Figure 16 shows the trends in ZC and φR              and experimental hard-particle packing proto-
as a function of θOST . We find that slowly            cols. We have studied these effects by varying
compressed OST packings are nearly isostatic,          the compression rate used to produce monodis-

                                                  19
perse packings of convex, noncircular hard-
particles in two dimensions. In particular, we
used the ASC scheme to generate dense, ef-
fectively jammed packings of rhombus, obtuse
scalene triangle, lens, curved triangle, and ice
cream cone shaped particles with a wide range
of packing fractions and degrees of order. To
characterize the kinetic effects on these pack-
ings, we defined the kinetic frustration index
K which quantifies the deviation of a packing
from its maximum possible packing fraction. In
addition, we characterized the degree of short-            Figure 17: The kinetic frustration index K as a
and long-range order in the packings using the             function of thickness β for the bowtie shapes.
spectral density. We also determined the type
and number of contacts in the packings to ex-
amine the trends in ZC and φR .                            polydispersity. Additionally, it is of interest
  Regardless of particle shape, K increases as             to determine the equilibrium phase behavior
the compression rate increases. We found that              of these families of particle shapes away from
a higher order of rotational symmetry, smaller             the jamming point. Furthermore, because such
γ, and more curvature all reduce K. Pack-                  hard particle packings can be viewed as two-
ings with large K tend to have reduced short-              phase materials, the physical properties (e.g.,
range translational order and are more likely to           conductivity and elastic moduli) of these pack-
be isotropic. Additionally, slower compression             ings should also be studied. Additional inter-
rates tend to result in packings with a greater            particle forces can also be applied to this set
degree of short-range translational and orienta-           of noncircular convex hard particle shapes, e.g.,
tional order. We also found that ZC increases as           dipolar forces, to design a broader class of pack-
the γ increases and as the compression rate de-            ing arrangements (see, e.g. refs 71 and 72.
creases. Moreover, φR increases as γ decreases               Obvious nontrivial extensions of the present
and as the compression rate increases.                     work include a closer examination of concave
  Rapidly compressed lens-shaped particles                 two-dimensional shapes and chiral mixtures of
with α = 0.5 have spectral densities that indi-            particles. To preliminarily examine the extent
cate short-range translational order, isotropy,            to which kinetic frustration is affected by parti-
and suppressed long-wavelength density fluctu-             cle concavity, we have measured K for packings
ations. As such, these lenses are a promising              of concave bowtie-shaped particles (see Fig-
candidate for a two-dimensional shape that                 ure 2f) produced using the three compression
readily forms monodisperse disordered jammed               schedules given in section 2.5. Figure 17 shows
packings, a current area of interest. 30 Closer in-        the behavior of K as a function of thickness β
spection of lenses with α ∼ 0.5 is warranted in            for these packings. We find that a greater differ-
future work to determine if this particle shape            ence between the particle volume and the vol-
can readily generate MRJ-like packings.                    ume of its convex hull results in greater K. It is
  Our findings on the relationship between K               also noteworthy that bowties with small β have
and compression rate may aid in the design                 the highest values of K observed herein. This
of laboratory packing protocols. It is desir-              indicates concave particle shapes tend to more
able, however, to extend these results to three-           easily generate packings with large K. Thus,
dimensional particle shapes so that they are ap-           such particle shapes may allow for the genera-
plicable to a wider variety of physical systems.           tion of effectively jammed packings with small
Future work in this area should also include the           packing fractions, which warrants further ex-
study of kinetic effects in packings in closed con-        amination.
tainers as well as packings with size and shape              Moreover, becuase of the wide range of

                                                      20
Table 1: K Values for OSTs with θOST =                         of Condensed Matter Physics; Cambridge
100 for All Three Compression Schedules                        University Press: New York, 2000.
                                 K                         (5) Edwards, S. F. In Granular Matter an In-
  compression rate    racemic    enantiopure                   terdisciplinary Approach; Mehta, A., Ed.;
       fast           0.140612     0.127592                    Springer-Verlag: New York, 1994.
     medium           0.110041     0.096288
                                                           (6) Liang, J.; Dill, K. A. Are proteins well-
       slow           0.096090     0.084675
                                                               packed? Biophys. J. 2001, 81, 751 – 766.
                                                           (7) Purohit, P. K.; Kondev, J.; Phillips, R.
enantioselectivities in the synthesis of chiral
                                                               Mechanics of DNA packaging in viruses.
molecules, 73 it is of interest to determine the
                                                               Proc. Natl. Acad. Sci. U. S. A. 2003, 100,
effect of enantioenrichment on packing kinetics.
                                                               3173–3178.
Here, we preliminarily consider dense packings
of enantiopure (a system containing only one               (8) Gevertz, J. L.; Torquato, S. A novel three-
type of mirror image) and racemic (a system                    phase model of brain tissue Microstruc-
containing an equal amount of both mirror im-                  ture. PLoS Comput. Biol. 2008, 4, 1–9.
ages) packings of OST with θOST = 100◦ . Table
1 compares the values of the kinetic frustration           (9) Torquato, S.; Stillinger, F. H. Jammed
index K for these two types of packings. We                    hard-particle packings: from Kepler to
find that packings of racemic mixtures of OSTs                 Bernal and beyond. Rev. Mod. Phys.
have a higher K than the analogous enantiopure                 2010, 82, 2633–2672.
packings. Further studies of the effects of chi-          (10) Torquato, S. Perspective: basic under-
rality on kinetic frustration include the study of             standing of condensed phases of matter
K as a function of enantioenrichment as well as                via packing models. J. Chem. Phys. 2018,
the examination of other chiral particle shapes.               149, 020901.
  Acknowledgement The authors are grate-
                                                          (11) Conway, J. H.; Sloane, N. J. A. Sphere
ful to Duyu Chen, Murray Skolnick, and Steven
                                                               Packings, Lattices and Groups; Springer:
Atkinson for assistance in implementing the
                                                               New York, 2011.
ASC code and to Michael A. Klatt and Amy
Secunda for fruitful discussions. This work was           (12) Rogers, C. Packing and Covering; Cam-
supported by the by the National Science Foun-                 bridge University Press: Cambridge, UK,
dation (NSF) under Grant DMR-1714722. The                      1964.
authors declare no competing financial interest.
                                                          (13) Fejes Tóth, L. Some packing and covering
                                                               theorems. Acta Sci. Math. Szeged 1950,
References                                                     12, 62–67.

 (1) Bernal, J. Liquids: Structure, Proper-               (14) Atkinson, S.; Jiao, Y.; Torquato, S. Max-
     ties, Solid Interactions; Elsevier Pub. Co.:              imally dense packings of two-dimensional
     Amsterdam, 1965.                                          convex and concave noncircular particles.
                                                               Phys. Rev. E 2012, 86, 031302.
 (2) Zallen, R. The Physics of Amorphous
     Solids; Wiley-VCH: New York, 2007.                   (15) Donev,     A.;     Stillinger,  F.     H.;
                                                               Chaikin, P. M.; Torquato, S. Unusu-
 (3) Torquato, S. Random Heterogeneous Ma-                     ally dense crystal packings of ellipsoids.
     terials: Microstructure and Macroscopic                   Phys. Rev. Lett. 2004, 92, 255506.
     Properties; Springer: New York, 2002.
                                                          (16) Torquato, S.; Jiao, Y. Dense packings of
 (4) Chaikin, P. M.; Lubensky, T. C. Principles                the Platonic and Archimedean solids. Na-
                                                               ture 2009, 460, 876–879.

                                                     21
(17) Torquato, S.; Jiao, Y. Exact construc-              (28) Jiao, Y.; Torquato, S. Maximally random
     tions of a family of dense periodic pack-                jammed packings of Platonic solids: hype-
     ings of tetrahedra. Phys. Rev. E 2010, 81,               runiform long-range correlations and iso-
     041310.                                                  staticity. Phys. Rev. E 2011, 84, 041309.

(18) de Graaf, J.; van Roij, R.; Dijkstra, M.            (29) Chen, D.; Jiao, Y.; Torquato, S. Equilib-
     Dense regular packings of irregular non-                 rium phase behavior and maximally ran-
     convex particles. Phys. Rev. Lett. 2011,                 dom jammed state of truncated tetrahe-
     107, 155501.                                             dra. J. Phys. Chem. B 2014, 118, 7981–
                                                              7992.
(19) Torquato, S.; Jiao, Y. Organizing prin-
     ciples for dense packings of nonspherical           (30) Atkinson, S.;       Stillinger, F. H.;
     hard particles: not all shapes are created               Torquato, S. Existence of isostatic,
     equal. Phys. Rev. E 2012, 86, 011102.                    maximally random jammed monodisperse
                                                              hard-disk packings. Proc. Natl. Acad. Sci.
(20) Torquato, S.;       Truskett, T. M.;                     U. S. A. 2014, 111, 18436–18441.
     Debenedetti, P. G. Is random close
     packing of spheres well defined? Phys.              (31) Tian, J.; Xu, Y.; Jiao, Y.; Torquato, S. A
     Rev. Lett. 2000, 84, 2064–2067.                          geometric-structure theory for maximally
                                                              random jammed packings. Sci. Rep. 2015,
(21) Torquato, S.; Stillinger, F. H. Local den-               5, 16722.
     sity fluctuations, hyperuniformity, and or-
     der metrics. Phys. Rev. E 2003, 68,                 (32) Speedy, R. J. Glass transition in hard
     041113.                                                  disc mixtures. J. Chem. Phys. 1999, 110,
                                                              4559–4565.
(22) Donev, A.; Stillinger, F. H.; Torquato, S.
     Unexpected density fluctuations in                  (33) Donev, A.; Stillinger, F. H.; Torquato, S.
     jammed disordered sphere packings.                       Do binary hard disks exhibit an ideal glass
     Phys. Rev. Lett. 2005, 95, 090604.                       transition? Phys. Rev. Lett. 2006, 96,
                                                              225502.
(23) Torquato, S. Hyperuniform states of mat-
     ter. Phys. Rep. 2018, 745, 1 – 95.                  (34) Ohring, M. Materials Science of Thin
                                                              Films: Deposition and Structure; Aca-
(24) Jullien, R.; Sadoc, J.; Mosseri, R. Pack-                demic Press: New York, 2001.
     ing at random in curved space and frustra-
     tion: a numerical study. J. Phys. I 1997,           (35) Azzam, W.; Cyganik, P.; Witte, G.;
     7, 1677–1692.                                            Buck, M.; Wöll, C. Pronounced odd even
                                                              changes in the molecular arrangement and
(25) Hales, T. A proof of the Kepler conjecture.              packing density of biphenyl-based thiol
     Ann. Math. 2005, 162, 1065–1185.                         SAMs: a combined STM and LEED study.
(26) Donev, A.; Cisse, I.; Sachs, D.; Vari-                   Langmuir 2003, 19, 8262–8270.
     ano, E. A.; Stillinger, F. H.; Connelly, R.;        (36) Cyganik, P.; Buck, M.; Azzam, W.;
     Torquato, S.; Chaikin, P. M. Improving                   Wöll, C. Self-assembled monolayers of
     the density of jammed disordered packings                omega-biphenylalkanethiols on Au(111):
     using ellipsoids. Science 2004, 303, 990–                influence of spacer chain on molecular
     993.                                                     packing. J. Phys. Chem. B 2004, 108,
(27) Jiao, Y.; Stillinger, F. H.; Torquato, S.                4989–4996.
     Distinctive features arising in maximally           (37) Farhadifar, R.; Röper, J.; Aigouy, B.;
     random jammed packings of superballs.                    Eaton, S.; Jülicher, F. The influence of
     Phys. Rev. E 2010, 81, 041304.                           cell mechanics, cell-cell interactions, and

                                                    22
     proliferation on epithelial packing. Curr.                a signature of disordered jammed hard-
     Biol. 2007, 17, 2095 – 2104.                              particle packings. Phys. Rev. Lett. 2011,
                                                               106, 178001.
(38) Classen, A.; Anderson, K. I.; Marois, E.;
     Eaton, S. Hexagonal packing of drosophila            (47) Zachary, C. E.; Jiao, Y.; Torquato, S. Hy-
     wing epithelial cells by the planar cell po-              peruniformity, quasi-long-range correla-
     larity pathway. Dev. Cell 2005, 9, 805 –                  tions, and void-space constraints in maxi-
     817.                                                      mally random jammed particle packings.
                                                               I. Polydisperse spheres. Phys. Rev. E
(39) Dabbousi, B. O.; Murray, C. B.; Rub-                      2011, 83, 051308.
     ner, M. F.; Bawendi, M. G. Langmuir-
     Blodgett manipulation of size-selected               (48) Zachary, C. E.; Jiao, Y.; Torquato, S. Hy-
     CdSe nanocrystallites. Chem. Mater.                       peruniformity, quasi-long-range correla-
     1994, 6, 216–219.                                         tions, and void-space constraints in maxi-
                                                               mally random jammed particle packings.
(40) Basavaraj, M. G.; Fuller, G. G.;                          II. Anisotropy in particle shape. Phys.
     Fransaer, J.; Vermant, J. Packing,                        Rev. E 2011, 83, 051309.
     flipping, and buckling transitions in com-
     pressed monolayers of ellipsoidal latex              (49) Jaoshvili, A.; Esakia, A.; Porrati, M.;
     particles. Langmuir 2006, 22, 6605–6612.                  Chaikin, P. M. Experiments on the ran-
                                                               dom packing of tetrahedral dice. Phys.
(41) Zhao, Y.; Barés, J.; Zheng, H.;                          Rev. Lett. 2010, 104, 185501.
     Bester, C. S.; Xu, Y.; Socolar, J. E. S.;
     Behringer, R. P. Jamming transition in               (50) Alexander, S. Amorphous solids: their
     non-spherical particle systems: pentagons                 structure, lattice dynamics and elasticity.
     versus disks. Granular Matter 2019, 21,                   Phys. Rep. 1998, 296, 65 – 236.
     90.
                                                          (51) Edwards, S. F.; Grinev, D. V. Statistical
(42) Torquato, S.; Jiao, Y. Dense packings                     mechanics of stress transmission in dis-
     of polyhedra: Platonic and Archimedean                    ordered granular arrays. Phys. Rev. Lett.
     solids. Phys. Rev. E 2009, 80, 041104.                    1999, 82, 5397–5400.

(43) Torquato, S.; Jiao, Y. Robust algorithm              (52) Donev, A.; Torquato, S.; Stillinger, F. H.
     to generate a diverse class of dense dis-                 Pair correlation function characteristics
     ordered and ordered sphere packings via                   of nearly jammed disordered and ordered
     linear programming. Phys. Rev. E 2010,                    hard-sphere packings. Phys. Rev. E 2005,
     82, 061302.                                               71, 011105.

(44) Debye, P.; Anderson, H. R.; Brum-                    (53) O’Hern, C. S.; Silbert, L. E.; Liu, A. J.;
     berger, H. Scattering by an inhomoge-                     Nagel, S. R. Jamming at zero temperature
     neous solid. II. The correlation func-                    and zero applied stress: the epitome of dis-
     tion and its spplication. J. Appl. Phys.                  order. Phys. Rev. E 2003, 68, 011306.
     (Melville, NY, U. S.) 1957, 28, 679–683.
                                                          (54) Delaney, G. W.; Cleary, P. W. The
(45) Torquato, S.; Stillinger, F. H. Multiplic-                packing properties of superellipsoids. EPL
     ity of generation, selection, and classifica-             2010, 89, 34002.
     tion procedures for jammed hard-particle
     packings. J. Phys. Chem. B 2001, 105,                (55) Atkinson, S.; Zhang, G.; Hopkins, A. B.;
     11849–11853.                                              Torquato, S. Critical slowing down and
                                                               hyperuniformity on approach to jamming.
(46) Zachary, C. E.; Jiao, Y.; Torquato, S.                    Phys. Rev. E 2016, 94, 012902.
     Hyperuniform long-range correlations are

                                                     23
(56) Cinacchi, G.; Torquato, S. Hard convex             (67) Groemer, H.; Heppes, A. Packing and cov-
     lens-shaped particles: characterization of              ering properties of split disks. Studia Sci.
     dense disordered packings. Phys. Rev. E                 Math. Hungar. 1975, 10 .
     2019, 100, 062902.
                                                        (68) Cinacchi, G.; Torquato, S. Hard con-
(57) Stoyan, D.; Kendall, W.; Mecke, J.                      vex lens-shaped particles: densest-known
     Stochastic Geometry and Its Applications;               packings and phase behavior. J. Chem.
     Wiley, New York, 1995.                                  Phys. 2015, 143, 224506.

(58) Quintanilla, J. A. Necessary and sufficient        (69) Bautista-Carbajal, G.; Odriozola, G.
     conditions for the two-point phase prob-                Phase diagram of two-dimensional hard el-
     ability function of two-phase random me-                lipses. J. Chem. Phys. 2014, 140, 204502.
     dia. Proc. R. Soc. London, Ser. A 2008,
     464, 1761–1779.                                    (70) Jiao, Y.; Torquato, S. Communication:
                                                             a packing of truncated tetrahedra that
(59) Zachary, C. E.; Torquato, S. Hyperunifor-               nearly fills all of space and its melting
     mity in point patterns and two-phase ran-               properties. J. Chem. Phys. 2011, 135,
     dom heterogeneous media. J. Stat. Mech.:                151101.
     Theory Exp. 2009, 2009, P12015.
                                                        (71) Maloney, R. C.; Hall, C. K. Phase di-
(60) Chen, D.; Torquato, S. Designing dis-                   agrams of mixtures of dipolar rods and
     ordered hyperuniform two-phase materi-                  discs. Soft Matter 2018, 14, 7894–7905.
     als with novel physical properties. Acta
     Mater. 2018, 142, 152 – 161.                       (72) Liao, G.-J.; Hall, C. K.; Klapp, S. H. L.
                                                             Dynamical self-assembly of dipolar active
(61) Stillinger, F. H.; Weber, T. A. Hidden                  Brownian particles in two dimensions. Soft
     structure in liquids. Phys. Rev. A 1982,                Matter 2020, 16, 2208–2223.
     25, 978–989.
                                                        (73) Ojima, I. Catalytic Asymmetric Synthesis;
(62) Stillinger, F. H.; Weber, T. A. Inherent                Wiley: Hoboken, NJ, 2010.
     structure theory of liquids in the hard-
     sphere limit. J. Chem. Phys. 1985, 83,
     4767–4775.

(63) Stillinger, F. H.; DiMarzio, E. A.; Korne-
     gay, R. L. Systematic approach to expla-
     nation of the rigid disk phase transition.
     J. Chem. Phys. 1964, 40, 1564–1576.

(64) Robin, A. C. 93.39 The Most Scalene Tri-
     angle. Math. Gaz. 2009, 93, 331–338.

(65) Reuleaux, F. In The Kinematics of Ma-
     chinery: Outlines of a Theory of Ma-
     chines; Kennedy, A., Ed.; Macmillan:
     London, 1875.

(66) Kuperberg, G.; Kuperberg, W. Double-
     lattice packings of convex bodies in the
     plane. Discrete Comput. Geom. 1990, 5,
     389–397.



                                                   24
Graphical TOC Entry




                                   ky
                                            kx
                  Compression +         Scattering
                      Shear              Pattern




                              25
