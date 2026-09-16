                                                              Packing Hyperspheres in High-Dimensional Euclidean Spaces

                                                            Monica Skoge,1 Aleksandar Donev,2, 3 Frank H. Stillinger,4 and Salvatore Torquato2, 3, 4, 5, ∗
arXiv:cond-mat/0608362v1 [cond-mat.stat-mech] 16 Aug 2006




                                                                         1
                                                                             Department of Physics, Princeton University, Princeton, NJ 08544
                                                                                  2
                                                                                      Program in Applied and Computational Mathematics,
                                                                                             Princeton University, Princeton NJ 08544
                                                                                      3
                                                                                          PRISM, Princeton University, Princeton NJ 08544
                                                                     4
                                                                         Department of Chemistry, Princeton University, Princeton NJ 08544
                                                                                             5
                                                                                                 Princeton Center for Theoretical Physics,
                                                                                             Princeton University, Princeton NJ 08544




                                                                                                                   1
                                                 Abstract
     We present the first study of disordered jammed hard-sphere packings in four-, five- and six-
dimensional Euclidean spaces. Using a collision-driven packing generation algorithm, we obtain
the first estimates for the packing fractions of the maximally random jammed (MRJ) states for
space dimensions d = 4, 5 and 6 to be φM RJ ≃ 0.46, 0.31 and 0.20, respectively. To a good
approximation, the MRJ density obeys the scaling form φM RJ = c1 /2d +(c2 d)/2d , where c1 = −2.72
and c2 = 2.56, which appears to be consistent with high-dimensional asymptotic limit, albeit with
different coefficients. Calculations of the pair correlation function g2 (r) and structure factor S(k)
for these states show that short-range ordering appreciably decreases with increasing dimension,
consistent with a recently proposed “decorrelation principle,” which, among othe things, states
that unconstrained correlations diminish as the dimension increases and vanish entirely in the
limit d → ∞. As in three dimensions (where φM RJ ≃ 0.64), the packings show no signs of
crystallization, are isostatic, and have a power-law divergence in g2 (r) at contact with power-law
exponent ≃ 0.4. Across dimensions, the cumulative number of neighbors equals the kissing number
of the conjectured densest packing close to where g2 (r) has its first minimum. Additionally, we
obtain estimates for the freezing and melting packing fractions for the equilibrium hard-sphere
fluid-solid transition, φF ≃ 0.32 and φM ≃ 0.39, respectively, for d = 4, and φF ≃ 0.19 and
φM ≃ 0.24, respectively, for d = 5. Although our results indicate the stable phase at high density
is a crystalline solid, nucleation appears to be strongly suppressed with increasing dimension.




∗
    Electronic address: torquato@electron.princeton.edu

                                                     2
I.    INTRODUCTION


     Hard-sphere systems are model systems for understanding the equilibrium and dynamical
properties of a variety of materials, including simple fluids, colloids, glasses, and granular
media. The hard-sphere potential is purely repulsive; it is infinite when two spheres overlap,
but otherwise zero. Despite the simplicity of the potential, hard-sphere systems exhibit rich
behavior: they undergo a fluid-solid phase transition and can exhibit glassy behavior. Of
particular recent interest are (nonequilibrium) disordered jammed packings of hard spheres
and their statistical and mechanical properties, such as the maximally random jammed
(MRJ) state [1, 2], pair correlations [3], isostaticity [3], and density fluctuations [4]. Such
packings have been intensely studied computationally in two and three dimensions [1, 2,
3, 4, 5, 6, 7, 8, 9, 10, 11] and in this paper we extend these studies to four, five and six
dimensions.
     A hard-sphere packing in d-dimensional Euclidean space Rd is an arrangement of congru-
ent spheres, no two of which overlap. As in a variety of interacting many-body systems [12],
we expect studies of hard-sphere packings in high dimensions to yield great insight into the
corresponding phenomena in lower dimensions. Analytical investigations of hard-spheres can
be readily extended into arbitrary spatial dimension [13, 14, 15, 16, 17, 20, 21, 22, 23, 24,
25, 26, 27, 28, 29] and high dimensions can therefore be used as a stringent testing ground
for such theories. Along these lines and of particular interest to this paper, predictions have
been made about long-wavelength density fluctuations [25] and decorrelation [27, 28] in dis-
ordered hard-sphere packings in high dimensions. Additionally, the optimal packing of hard
spheres in high dimensions is also of interest in error-correcting codes in communications
theory [30].
     Our focus in this paper will be the study of hard-sphere packings in four, five and six
dimensions. Specifically, we consider both equilibrium packings for d = 4 and d = 5 and
nonequilibrium packings representative of the maximally random jammed state for d = 4,
d = 5 and d = 6.
     Equilibrium thermodynamic properties of hard-sphere packings for d = 4 and d = 5
have been studied both computationally and with approximate theories [15, 22, 31]. For
the low-density fluid, lower-order virial coefficients, B2 , B3 , and B4 , are known exactly for
arbitrary dimensionality [13, 14, 17]. Higher-order virial coefficients have been calculated


                                              3
by Monte Carlo simulation, B5 , B6 and B7 for both d = 4 and d = 5 [16] and B8 for
d = 4 [16], and analytically [18, 19]. The pair correlation function for equilibrium fluids has
been studied and a decrease in ordering with increasing dimension was readily apparent [32].
Hard-sphere systems have been shown to undergo a (first-order) fluid-solid phase transition
by numerical simulations for 3 ≤ d ≤ 5 [33] and with approximate theories for d as high as
50 [22]. The freezing points for d = 4 and d = 5 were estimated numerically to occur at
packing fractions φF ≈ 0.5φmax = 0.31 and φF ≈ 0.4φmax = 0.19, respectively, and it was
conjectured that freezing occurs at lower packing fractions relative to close packing as the
dimension increases [33]. The packing fraction φ is the fraction of space Rd covered by the
spheres, i.e.,
                                         φ = ρv1 (R),                                      (1)

where ρ is the number density,
                                                 π d/2
                                   v1 (R) =              Rd                                (2)
                                              Γ(1 + d/2)
is the volume of a d-dimensional sphere of radius R, and Γ(x) is the gamma function [23].
   At sufficiently large densities, the packing of spheres with the highest jamming density
has the greatest entropy because the free-volume entropy dominates over the degeneracy
entropy. Therefore, the high-density equilibrium phase corresponds to the optimal packing,
i.e., maximal density. The densest packing for d = 3 was recently proven by Hales [34] to be
                                                             √
attained by the FCC lattice with packing fraction φmax = π/ 18 = 0.7404 . . .. The kissing
number Z, the number of spheres in contact with any given sphere, for the FCC lattice
corresponds to the maximal kissing number Zmax = 12 for d = 3. One of the generalizations
of the FCC lattice to higher dimensions is the Dd checkerboard lattice, defined by taking a
cubic lattice and placing spheres on every site at which the sum of the lattice indices is even
(i.e., every other site). The densest packing for d = 4 is conjectured to be the D4 lattice,
with packing fraction φmax = π 2 /16 = 0.6168 . . . and kissing number Z = Zmax = 24 [30],
which is also the maximal kissing number in d = 4 [35]. For d = 5, the densest packing is
                                                                        √
conjectured to be the D5 lattice, with packing fraction φmax = 2π 2 /(30 2) = 0.4652 . . . and
kissing number Z = 40 [30]. For d = 6, the densest packing is conjectured to be the “root”
                                           √
lattice E6 , with density φmax = 3π 3 /(144 3) = 0.3729 . . . and kissing number Z = 72 [30].
The maximal kissing numbers Zmax for d = 5 and d = 6 are not known, but have the
following bounds: 40 ≤ Zmax ≤ 46 for d = 5 and 72 ≤ Zmax ≤ 82 for d = 6 [30]. In very

                                              4
high dimensions, it has been suggested that random packings of spheres might have a higher
density than ordered packings, enabling the intriguing possibility of disordered ground states
and hence thermodynamic glass transitions [27]; see also Ref. [28].
   Equilibrium hard-sphere systems for d = 2 and d = 3 crystallize into ordered packings
upon densification. However, for d = 3, it has been found both experimentally [36] and
computationally [1, 3, 5] that if the system is densified sufficiently rapidly, the system can be
kept out-of-equilibrium and can jam in a disordered state. A jammed packing is one in which
the particle positions are fixed by the impenetrability constraints and boundary conditions,
despite thermal or mechanical agitation of the particles or imposed boundary deformations or
loads. Depending on the boundary conditions, different jamming categories can be precisely
defined, including local, collective and strict jamming [37, 38, 39]. The density of disordered
collectively jammed hard-sphere packings for d = 3 is around φ ≃ 0.64 for a variety of
packing-generation protocols and has traditionally been called random close packing (RCP)
[23]. However, Ref. [1] showed that RCP is ill-defined because “random” and “close packed”
are at odds with one another and the precise proportion of each of these competing effects
is arbitrary. Therefore, Ref. [1] introduced the concept of the maximally random jammed
(MRJ) state to be the most disordered jammed packing in the given jamming category. This
definition presupposes an order metric ψ can be defined such that ψ = 1 corresponds to the
most ordered (i.e., crystal) packing and ψ = 0 corresponds to the most disordered packing,
in which there are no spatial correlations. Figure 1 from Ref. [1] shows where MRJ lies on
a schematic diagram of the space of jammed packings in the density-disorder φ-ψ plane.
   In this paper, we numerically study MRJ packings of hard spheres for d = 4, 5 and 6
that are at least collectively jammed and report the first estimates of the packing fractions
of the MRJ states [1] in these dimensions to be φM RJ ≃ 0.46, 0.31 and 0.20, respectively.
We find that short-range ordering exhibited by g2 (r) and S(k) appreciably diminishes with
increasing dimension, consistent with a recently proposed “decorrelation principle” stating
that unconstrained spatial correlations vanish asymptotically in high dimensions and that
the n-particle correlation function gn for any n ≥ 3 can be inferred entirely from a knowledge
of the number density ρ and the pair correlation function g2 (r) [27, 40]. We also explore
equilibrium properties, in particular the fluid-solid phase transition, for d = 4 and d = 5,
and find a decreased tendency to crystallize with increasing dimension.
   This paper is organized as follows: Section II explains the simulation procedure, Section

                                              5
                     1.0
                                                                          B
                                                           A



                  ψ 0.5            Jammed                       MRJ
                                  Structures




                     0.0
                        0.0           0.2           0.4           0.6
                                                   φ


FIG. 1: A highly schematic plot of the subspace in the density-disorder φ − ψ plane, where strictly
jammed three-dimensional packings exist, as adapted from Ref. [1]. Point A corresponds to the
lowest-density jammed packing, and it is intuitive to expect that a certain ordering will be needed
to produce low-density jammed packings. Point B corresponds to the most dense jammed packing,
which is also expected to be the most ordered. Point MRJ represents the maximally random
jammed state. The jamming region in the φ-ψ plane will of course depend on the jamming category.
The gray region is devoid of hard-sphere configurations.



III gives equilibrium results for d = 4 and d = 5, Section IV gives results for disordered
jammed packings for d = 4, 5 and 6, and Section V summarizes and discusses our results.


II.     SIMULATION PROCEDURE


      We use event-driven molecular dynamics and a modified Lubachevsky-Stillinger (LS) al-
gorithm [41], as in Ref. [42], to produce collectively-jammed hard-sphere packings. As in
Ref. [42], our algorithm uses periodic boundary conditions applied to a hypercubic cell,
in which a fundamental cell containing N spheres is periodically replicated to fill all of
Euclidean space. We also use the cell method, in which the computational domain is di-

                                               6
vided into cubic cells and only neighboring cells are checked when predicting collisions for
a given sphere. Since the number of neighboring cells, as well as the number of spheres
per cell, increases considerably with increasing dimension, working in high dimensions is
computationally intensive. Additionally, eliminating excessive boundary effects requires on
the order of ten sphere diameters per simulation box length, i.e., on the order of N = 10d
spheres. Due to the increasing computational load with increasing dimension, we cannot
yet study d > 6. Implementing the near-neighbor list (NNL) techniques from Ref. [42],
as well as parallelization, are necessary in order to study higher dimensions. Dimension-
independent C++ codes used to generate the data in this paper can be downloaded at
http://cherrypit.princeton.edu/Packing/C++/.
   Starting from a Poisson distribution of points, the points grow into nonoverlapping
spheres of diameter D at an expansion rate γ = dD/dt, while the positions of the spheres
evolve in time according to Newtonian mechanics, augmented with energy non-conserving
collisions. Spheres receive an extra energy boost after the collision due to the positive expan-
sion rate. In practice, the starting configurations for our packing algorithm are low density
random-sequential-addition packings of spheres [23]. As the density increases, statistics,
such as pressure, are collected. In the limit γ → 0, the system is in equilibrium; for small
but nonzero γ, the system is in quasi-equilibrium; and for large γ, the system is out of equi-
librium. Eventually, a jammed state with diverging collision rate is reached. For studies of
amorphous jammed packings, the expansion must be initially fast to suppress crystallization
and maximize disorder, but at sufficiently high pressure, the expansion rate must be slow
enough to allow local particle rearrangements necessary to achieve jamming [3].


III.   EQUILIBRIUM AND METASTABLE PROPERTIES


   The temperature in equilibrium systems of hard spheres is a trivial variable; i.e., it does
not affect equilibrium configurational correlations, leaving only one independent thermody-
namic state variable, which can be taken to be either the reduced pressure p = P V /NkB T or
the density φ, related through the equation of state (EOS). Hard-sphere systems undergo a
(first-order) fluid-solid phase transition, characterized by a melting point, i.e., the density at
which the crystal thermodynamically begins to melt, and a freezing point, i.e., the density
at which the fluid thermodynamically begins to freeze. Equilibrium properties, such as the


                                               7
melting and freezing points, are studied here using small expansion rates (γ = 10−5 − 10−9)
and periodic rescaling of the average sphere velocity to one, such that the total change
in kinetic energy of the system, due to the collisions between growing spheres, was kept
small. Strictly speaking, a positive growth rate yields nonequilibrium packings but equilib-
rium packings result as the growth rate tends to zero. The packings were “equilibrated”
by verifying that orders of magnitude of change in the expansion rate did not change the
resulting equation of state. In this section we only consider four and five dimensions due to
(presently) prohibitive computational costs for higher dimensions.
   Figure 2 shows the reduced pressure p as a function of density φ for (a) simulations of
d = 4 systems of spheres placed in a D4 lattice with negative expansion rate γ = −10−6 and
(b) simulations of d = 5 systems of spheres placed in a D5 lattice with negative expansion
rate γ = −10−5 . The pressure initially follows the (lower) crystal branch, until the system
becomes mechanically unstable and jumps onto the (higher) fluid branch. Also plotted
is the theoretical prediction of Luban and Michels (LM) for the equation of state [15],
which agrees well with our numerical results for the fluid branch for d = 4, but less so
for d = 5. It is a computational observation that crystals become mechanically unstable,
giving rise to a sudden jump in pressure, at a density close to the freezing point [43, 44].
Such “superheating” (undercompression) is most likely due to the difficulty of achieving
coexistence in finite systems, although we are not aware of a theoretical analysis. From the
results in Fig. 2, we estimate the freezing points for d = 4 and d = 5 to be φF ≃ 0.31 − 0.32
and φF ≃ 0.19 − 0.20, respectively.
   The melting points for d = 4 and d = 5 can also be estimated from the data in Fig. 2.
Since throughout the coexistence region the fluid and solid have the same absolute pressure
P , the melting density can be estimated as the density on the crystal branch with the same
absolute pressure P as that at the freezing point. The coexistence region is plotted in Fig. 2
and the melting packing fractions for d = 4 and d = 5 are estimated to be φM ≃ 0.38 − 0.40
and φM ≃ 0.24−0.26, respectively. We also observe that the reduced pressure at the freezing
point is pF ≃ 12 in both d = 4 and d = 5, which agrees with the reduced pressure at the
freezing point for d = 3, pF ≃ 12.3, obtained from free energy calculations [45].
   The melting point was also estimated for d = 4 (higher dimensions are presently too
computationally demanding) by slowly densifying a system of spheres, initially a fluid, and
looking for the onset of partial crystallization, again by monitoring the reduced pressure p as

                                             8
                   13

                          (a)                                                           2048
                                                                                        5000
                                                                                        10,368
                   12
                                                                                        19,208
                          liquid                                                        32,768
                                                                                        LM EOS
                   11                                                                   coexistence
              p


                   10



                    9
                                                                                     crystal


                    8

                           0.3            0.32           0.34          0.36           0.38             0.4
                                                                φ
                   13

                          (b)                                                        16,384
                                                                                     50,000
                   12
                                                                                     124,416
                                                                                     LM EOS
                             liquid                                                  Coexistence
                   11
               p




                   10



                    9
                                                                                      crystal

                    8

                   0.16    0.17    0.18     0.19   0.2       0.21   0.22      0.23   0.24    0.25     0.26
                                                                φ

FIG. 2: (Color online) Reduced pressure p as a function of density φ, for a range of system sizes
(see legend), for (a) d = 4 systems of spheres, initially in a D4 lattice, and negative expansion rate
γ = −10−6 and (b) d = 5 systems of spheres, initially in a D5 lattice, and negative expansion rate
γ = −10−5 . N was chosen to make a perfect Dd lattice with periodic boundary conditions, i.e.,
N = (2n)d /2 for n ǫ Z. Also plotted is the theoretical prediction of Luban and Michels (LM) for
the equation of state [15]. Curves for larger system sizes lie farther to the right.




                                                         9
a function of density φ. Due to the difficulty of observing coexistence in finite systems and
the relatively high activation barrier, simulated hard-sphere systems become “supercooled”
(overcompressed) and nucleation does not occur until the melting density is surpassed. Con-
sequently, the density at which partial crystallization appears for sufficiently slow expansion
provides a reasonable estimate for the melting density. Near jamming the reduced pressure
is asymptotically given by the free-volume equation of state [46],

                                      PV    1      d
                                p=         = =          ,                                   (3)
                                     NkB T  δ  1 − φ/φJ

which can be inverted to give an estimate φ̃J of the jamming density,

                                                   φ
                                        φ̃J =           .                                   (4)
                                                1 − d/p

Since the pressure increases very rapidly near jamming, it is more convenient to plot the
estimated jamming density φ̃J (φ) instead of the pressure p(φ), as shown in Fig. 3 for a system
of 648 spheres in d = 4. In such a plot, the onset of partial crystallization causes a dramatic
jump in φ̃J (φ), as the jamming density of the crystal is much higher than the jamming
density of a disordered packing. The intersection of the curves with the line φ̃J (φ) = φ gives
the final jamming density. Sufficiently fast expansion suppresses crystallization and leads
to packing fractions around 0.45 − 0.47. Slower expansion allows for partial crystallization,
typically around φM ≃ 0.38 − 0.39, which is our rough estimate of the melting point, in
agreement with our estimate from the results in Fig. 2. More accurate estimates can only
be obtained using free-energy calculations. Since crystallization is a nucleated process, it is
not surprising that the same expansion rates γ can crystallize at different packing fractions
and onto different crystal branches, e.g. γ = 10−8 (a) and (b) in Fig. 3.




                                             10
                0.65                                                       150
                                                                                         D4
                                                                                           -8
                                                                                         10 (b)
                                                                                           -9
                                                                                         10

                 0.6

                                                                           100
 Estimated φJ




                                                                          Z(r)
                0.55                                           -5
                                                             10
                                                               -6
                                                             10
                                                               -7
                                                             10
                                                               -8
                                                             10 (a)          50
                                                               -8
                                                             10 (b)
                 0.5                                           -9
                                                             10
                                                             φJ = φ
                                                             LM EOS
                                                             φJ = φD4

                0.45                                                             0
                   0.35   0.4   0.45       0.5        0.55          0.6              1        1.5   2
                                       φ                                                 r/D

FIG. 3: (Color online) Left panel: The estimated jamming packing fraction φ̃J as a function of
density φ for systems of 648 spheres for d = 4 with various expansion rates (see legend and note
that there are two samples labeled (a) and (b) for γ = 10−8 ). For the curves showing no partial
crystallization (i.e., γ = 10−5 , 10−6 , and 10−7 ), curves with smaller expansion rates have larger
peak heights. For the curves that show partial crystallization (i.e. γ = 10−8 (a and b) and
10−9 ), curves with smaller expansion rate lie farther to the left. Right panel: The cumulative
coordination Z(r) (i.e., the number of contacts) for the perfect D4 lattice and for the partially
crystallized packings at p > 1012 obtained for expansion rates γ = 10−8 and γ = 10−9 . The
jamming packing fraction for the γ = 10−8 packing is φ = 0.511, and the jamming packing fraction
for the γ = 10−9 packing agreed up to 12 significant figures with the density of the D4 lattice,
φ = π 2 /16 ≃ 0.617.



    To determine whether the crystallized packings were forming a D4 lattice, the conjectured
densest packing in four dimensions, we computed the average cumulative coordination num-
ber Z(r), which is the average number of sphere centers within a distance r from a given


                                                 11
                           -3
                        10
                           -4
                        10
        0.48               -5
                        10
                           -6
                        10
                           -7
                        10
                        mix
                        φ = φJ
 φJ




        0.47




        0.46
           0.32 0.33 0.34 0.35 0.36 0.37 0.38 0.39 0.4 0.41 0.42 0.43 0.44 0.45 0.46
                                                    φ

FIG. 4: The estimated jamming packing fraction φ̃J as a function of density φ for a system of
10, 000 spheres for d = 4 with various expansion rates. Curves with smaller expansion rates have
larger peak heights. The curve labeled “mix” corresponds to the following sequence of expansion
rates: γ = 10−2 until p = 10, γ = 10−3 until p = 104 , γ = 10−4 until p = 106 , and γ = 10−5 until
p = 1012 .



sphere center. The inset to Fig. 3 shows Z(r) for a perfect D4 lattice and for the crystallized
packings with γ = 10−8 and γ = 10−9 (corresponding colors represent the same packing).
The sharp plateaus for the D4 lattice correspond to the coordination shells and the number of
spheres in the first shell is the kissing number Zmax = 24. The packing shown with γ = 10−9
formed a perfect D4 lattice. The packing shown with γ = 10−8 partially crystallized with a
final density of φ ≃ 0.511.
   Figure 4 shows the estimated jamming packing fraction φ̃J , as in Fig. 3, but for a sys-
tem of 10, 000 spheres, instead of 648 spheres, in four dimensions. In contrast to the 648
sphere system, there is no sign of partial crystallization for the 10, 000-sphere system. In
fact, molecular dynamics was performed at packing fractions of φ ≃ 0.38 − 0.42 for 10 mil-

                                              12
lion collisions per sphere and there was no significant drop in pressure indicative of partial
crystallization. The curves in Figs. 3 and 4 exhibit a bump around φG ≃ 0.41, suggesting a
kinetic transition from the fluid branch to a glassy branch.


                0.74
                                                                               crystal

                0.72
                                        ce
 Estimated φJ




                                      isten
                                                                                       Equilibrium
                 0.7                                                                   10
                                                                                         -6
                                     coex


                                                                                                 -6
                                                                                       4*10
                                                                                                  -6
                                                                                       16*10
                                                                                                  -6
                                                                                       32*10
                0.68                                                                              -6
                                                                                       64*10
                                                                                                      -6
                                                                                       128*10
                                                                                       φ = φJ
                       fluid                                                           PY EOS
                0.66                                                                        -4
                                                                                       -10
                                                                                            -5
                                                                                       -10
                                                                                            -6
                                                                                       -10
                0.64
                               0.5            0.55        0.6     0.65           0.7                       0.75
                                                            φ

FIG. 5: (Color online) The estimated jamming packing fraction φ̃J as a function of packing fraction
φ for d = 3. Shown are systems of 4096 spheres with various expansion rates and systems of 10, 976
spheres placed in an FCC lattice with negative expansion rates γ = −10−4 , −10−5 , and −10−6
(last three curves). Also plotted are approximations to the equilibrium EOS for the fluid phase,
the coexistence region, and the crystal phase [47], as well as the Percus-Yevick (PY) EOS for the
fluid phase. Compare this figure to the curves shown in Figs. 3 and 4. For the curves showing
no partial crystallization (i.e., γ = 32 × 10−6 , 64 × 10−6 , and 128 × 10−6 ), curves with smaller
expansion rates have larger peak heights. For the curves that show partial crystallization (i.e.,
γ = 10−6 , 4 × 10−6 , and 16 × 10−6 ), curves with smaller expanion rates lie farther to the left. For
the melting curves (i.e., γ = −10−4 , −10−5 , and −10−6 ), curves with smaller compression rates lie
farther to the right.



    Figure 5 shows the estimated jamming packing fraction φ̃J for systems of spheres for

                                                     13
d = 3 with various positive and negative expansion rates, for comparison with the results
for d = 4 and d = 5 in Figs. 2, 3 and 4. The locations of the freezing and melting points
in d = 3 have been determined from free-energy calculations [45] and good approximations
to the EOS for both the fluid and crystal phases are known [47]. Our estimates of the
freezing and melting points as the densities at the onset of melting of a diluted crystal or of
partial crystallization of a densified fluid, respectively, compare favorably to the true values
computed from free-energy calculations in d = 3. The bump around φG ≃ 0.59, analogous
to the bump in Fig. 4 around φG ≃ 0.41, is often cited as the approximate location of the
“kinetic” glass transition [48]. Comparing Figs. 4 and 5 reveals that the melting point and
suggested kinetic glass transition are closer for d = 4 than for d = 3, which is a possible
reason why there is a lower tendency to crystallize for d = 4 than for d = 3. Similar results
have been observed for binary hard disks, a model glass former [6].


IV.   DISORDERED JAMMED PACKINGS


   Packings representative of the maximally random jammed (MRJ) state are produced by a
combination of expansion rates. The expansion rate must be initially high (compared to the
average thermal velocity) to suppress crystallization and produce disordered configurations
that are trapped in the neighborhood of a jammed packing. Near the jamming point, the
expansion rate must be sufficiently slow to allow for particle readjustments necessary for
collective jamming. Figure 4 shows the final jamming packing fractions of packings created
using a variety of expansion rates, as the packing fraction at which the curves intersect the
line φ̃J = φ. We see that by increasing the expansion rate, we attain packings with lower
jamming packing fractions.
   By comparing Fig. 4 and to the analogous plot for a d = 3 system (Fig. 5), where it is
widely accepted that φM RJ ≃ 0.64 − 0.65 [1, 2], we estimate the MRJ density for d = 4
to be φM RJ ≃ 0.460 ± 0.005. A more accurate calculation of φM RJ demands a better
theoretical understanding of order metrics and how the expansion rate in the algorithm
affects the ordering in the produced packings; statistical errors are smaller than the effect of
the packing-generation protocol. Systematic investigation of different protocol parameters,
as done for d = 4 in Fig. 4, is currently too computationally intensive in higher dimensions.
Reasonable estimates of φM RJ for both d = 5 and d = 6 are obtained using the following


                                             14
less computationally intensive procedure. First, the system of spheres is expanded, starting
from zero initial kinetic energy (T = 0), until it reached a high pressure (say, p = 100 −
1000). Then the system is slowly expanded (γ = 10−5 − 10−3 ) and periodically cooled to
kB T = 1 until a very high pressure (say, p = 1012 ) is attained. The resulting packings are
approximately collectively jammed, as demonstrated by very large relaxation times for the
pressure during long molecular dynamics runs [3]. Using this method we estimate the MRJ
density for d = 5 to be φM RJ ≃ 0.310 ± 0.005 and for d = 6 to be φM RJ ≃ 0.200 ± 0.01.
   The MRJ packing fractions as well as important equilibrium packing fractions are summa-
rized in Table I. It is useful to compare the MRJ packings fractions for 3 ≤ d ≤ 6 to recent
estimates of the saturation packing fraction φs for the random sequential addition (RSA)
packing of hard spheres obtained by Torquato, Uche and Stillinger [29] in corresponding
dimensions, which were shown to be nearly hyperuniform [25]. These authors found that
φs = 0.38278 ± 0.000046, 0.25454 ± 0.000091, 0.16102 ± 0.000036 and 0.09394 ± 0.000048 for
d = 3, 4, 5 and 6, respectively. The nonequilibrium RSA packing is produced by randomly,
irreversibly, and sequentially placing nonoverlapping spheres into a volume. As the process
continues, it becomes more difficult to find available regions into which the spheres can be
added. Eventually, in the saturation (infinite-time) limit, no further additions are possible,
and the maximal achievable packing fraction is the saturation value φs [see Ref. [23] and
references therein]. As expected, the RSA saturation packing fraction in dimension d is
substantially smaller than the corresponding MRJ value because, unlike the latter packing,
the particles cannot rearrange.
   Our estimates for the MRJ packing fraction are compared to a theoretical formula pro-
posed by Philipse [24] for the “random jamming density” φd ,

                                         0.046d2 + 1.22d + 0.73
                                  φd ≃                          ,                          (5)
                                                   2d

which predicts φ3 ≃ 0.601, φ4 ≃ 0.397, φ5 ≃ 0.249, and φ6 ≃ 0.152. It is seen that Eq. (5)
underestimates MRJ density φM RJ in d = 3 and becomes worse with increasing dimension.
Following Ref. [29], we obtain a better scaling form by noting that the product 2d φM RJ for
3 ≤ d ≤ 6 is well approximated by a function linear, rather than quadratic, in d (see Fig.
6), i.e., the scaling form for φM RJ is given by

                                                   c1 c2 d
                                         φM RJ =      + d,                                 (6)
                                                   2d   2

                                               15
              Packing
              fraction             d=3             d=4              d=5               d=6

                 φF         0.494 [23, 45]     0.32 ± 0.01∗     0.19 ± 0.01∗               -
                φM          0.545 [23, 45]     0.39 ± 0.01∗     0.24 ± 0.01∗               -
               φM RJ 0.645 ± 0.005 [2] 0.46 ± 0.005∗ 0.31 ± 0.005∗                0.20 ± 0.01∗
                φmax       0.7405 . . . [34] 0.6169 . . . [30] 0.4652 . . . [30] 0.3729 . . . [30]

TABLE I: Important packing fractions for d = 3, 4, 5 and 6. These include the equilibrium values
for the freezing, φF , melting, φM , and densest states, φmax , as well as the nonequilibrium MRJ
values. The freezing and melting points for d = 6 were not calculated here. ∗ Values computed in
this work.


                                  15
                         2 φMRJ




                                  10
                       d




                                   5
                                    3             4                  5                 6
                                                           d

FIG. 6: (Color online) Fit of the data for the product 2d φM RJ to the linear form (6) for 3 ≤ d ≤ 6
with c1 = −2.72 and c2 = 2.56.



where c1 = −2.72 and c2 = 2.56. Although the scaling form (6) applies only in low di-
mensions such that d ≥ 3, theoretical arguments given by Torquato, Uche and Stillinger
[29] suggest that the general scaling form (6) persists in the high-dimensional asymptotic
limit, albeit with different coefficients c1 and c2 . In Ref. [29], the density lower bound
φM RJ ≥ (d + 2)/2d is derived for MRJ packings in any dimension. This MRJ density lower
bound yields 0.3125, 0.1875, 0.109375, 0.0625 for d = 3, 4, 5 and 6, respectively. We note
that Parisi and Zamponi [26] suggest the MRJ density scaling φM RJ ∼ (d log d)/2d .


                                                      16
   A.   Pair Correlations


   Our main interest is pair correlations in the jamming limit in four, five and six dimensions.
We characterize jammed packings statistically using the pair correlation function g2 (r) and
structure factor S(k). The pair correlation function measures the probability of finding
a sphere center at a given distance from the center of another sphere, normalized by the
average number density ρ to go asymptotically to unity at large r; i.e.

                                                       hP (r)i
                                         g2 (r) =              ,                             (7)
                                                       ρs1 (r)

where P (r) is the probability density for finding a sphere center a distance r from an arbitrary
sphere center, hi denotes an ensemble average, and s1 (r) is the surface area of a single
hypersphere of radius r [23]: s1 (r) = 2π 2 r 3 in d = 4, s1 (r) = 8π 2 r 4 /3 in d = 5 and
s1 (r) = π 3 r 5 in d = 6. The structure factor

                                        S(k) = 1 + ρĥ(k)                                    (8)

is related to the Fourier transform of the total correlation function h(r) = g2 (r) − 1. It mea-
sures spatial correlations at wavenumber k and in particular, large-scale density fluctuations
at k = 0 [25]. The structure factor can be observed directly via scattering experiments [12].
   In the jamming limit, the pair correlation function g2 (r) consists of a δ-function due to
sphere contacts and a background part g2b (r) due to spheres not in contact:

                                             Z̄δ(r − D)
                                  g2 (r) =              + g2b (r),                           (9)
                                               ρs1 (D)

where Z̄ is the average kissing number. Figure 7 compares the pair correlation function for
jammed packings of 105 spheres in d = 3, 4, 5 and 6. Due to periodic boundary conditions,
g2 (r) can only be calculated up to half the length of the simulation box, which limits the
calculation to r/D ≃ 3 for d = 6. The well-known split second peak present in d = 3
is strongly diminished as the dimension increases, i.e., the amplitude of the split second
peak decreases and the sharp cusps become rounded with increasing dimension. The split
third peak present in d = 3 with considerable structure and two shoulders vanishes almost
completely in the higher dimensions. The oscillations are strongly damped with increasing
dimension and the period of oscillations might also decrease slightly with increasing dimen-
sion; this latter possibility is revealed more vividly in the structure factor through the shift

                                                  17
           3
                    d=3                                   1
                    d=4
          2.5       d=5                               0.1
                    d=6




                                          |h(r)|
                                                     0.01

           2
                                                    0.001
  g2(r)




                                                   0.0001
                                                              3       3.5          4        4.5     5
          1.5
                                                                                  r/D

           1



          0.5

                1   1.5         2          2.5                    3         3.5         4         4.5   5
                                                          r/D
FIG. 7: The pair correlation function g2 (r) for MRJ packings of 104 hard spheres for d = 3, 4, 5
and 6 at the respective densities reported in Table I. Pair separation is plotted in units of the
sphere diameter D. [For d = 6, g2 (r) was only calculated up to r/D = 3 due to the system size and
periodic boundary conditions]. The delta-function contribution [cf. Eq. 9] at contact, of course, is
not shown. The inset shows |h(r)| = |g2 (r) − 1| on a logarithmic scale for d = 3, 4 and 5. Each
curve for g2 (r) is obtained from a single packing realization (not time-averaged). Curves for higher
dimensions are increasingly diminished.



in the location of the maximum, as we will describe below. The inset to Fig. 7 shows the
magnitude of the decaying oscillations in h(r) on a semi-log scale. Though at the values
of r/D shown, up to about half the length of the simulation box, there is still structure in
addition to the oscillations, especially apparent for d = 3, it appears that the decay rate of
the oscillations in h(r) does not change significantly with dimension, whereas the amplitude
of oscillations does. However, further studies with larger r and therefore larger systems are
needed to obtain more quantitative results.


                                                     18
   We calculate the structure factor S(k), defined in Eq. 8, for d = 4 and d = 5 by
                                            Z ∞
                                                         J1 (Kx)
                          S(K) = 1 + 128φ        x3 h(x)         dx                      (10)
                                             0             Kx
and
                                             x4 h(x) sin(Kx)
                                       Z ∞                           
                   S(K) = 1 + 480φ                           − cos(Kx) dx,               (11)
                                        0    (Kx)2      Kx
respectively, where φ = π 2 ρD 4 /32 for d = 4 and φ = π 2 ρD 5 /60 for d = 5, x = r/D and
K = kD are the dimensionless radius and wave number, and Jν (x) is the Bessel function of
order ν. We do not calculate the structure factor for d = 6 because at present we do not
have g2 (r) over a sufficiently large range of r.
   Following Ref. [4], rather than working directly with g2 (x) as in Eq. (8), we consider the
average cumulative coordination Z(x), defined to be the following volume integral of g2 (x):
                                       Z x
                              Z(x) = ρ      s1 (x′ )g2 (x′ )dx′ .                      (12)
                                                 1

The excess coordination ∆Z(x),
                                                          Z x
                              ∆Z(x) = 1 + 64φ                      (x′ )3 h(x′ )dx′      (13)
                                                           0
                                                           Z x
                              ∆Z(x) = 1 + 160φ                      (x′ )4 h(x′ )dx′ ,   (14)
                                                               0

for d = 4 and d = 5, respectively, is the average excess number of sphere centers inside a
spherical window of radius x centered at a sphere, compared to the ideal gas expectations,
16φx4 for d = 4 and 32φx5 in d = 5. We can rewrite Eq. (8) in terms of ∆Z(x) using
integration by parts to get
                                            Z ∞
                                                                     d J1 (Kx)
                              S(K) = −2              ∆Z(x)                     dx        (15)
                                             0                      dx Kx
and                              Z ∞                           
                                              d sin(Kx) cos(Kx)
                    S(K) = −3          ∆Z(x)           −          dx,                    (16)
                                  0          dx (Kx)3    (Kx)2
for d = 4 and d = 5, respectively. Note that accurate evaluations of the integrals of ∆Z(x)
require extrapolations of its large-x tail behavior, for which we have used an exponentially-
damped oscillating function [49].
   Figure 8 shows S(k) for jammed packings of 105 spheres in three, four and five dimensions.
Qualitatively, S(k) is somewhat similar for d = 3, 4, and 5. However, with increasing
dimension, the height of the first peak of S(k) decreases, the location of the first peak

                                                     19
         5
                                                3
                                                        d=4                  jammed
         4
                       d=3                                                   liquid
                       d=4                      2
                       d=5




                                         S(k)
         3                                      1
  S(k)




                                                0
         2                                          0         1      2        3         4
                                                                  kD / 2π

         1



         0
             0                1                         2                3                    4
                                                kD / 2π
FIG. 8: The structure factor S(k) for jammed packings of 105 spheres for d = 3, 4 and 5 at the
respective densities reported in Table I. Inset: A comparison for d = 4 of S(k) for a jammed
packing and for a fluid near the freezing point (φ ≈ 0.31). Each curve for S(k) is obtained from a
single packing realization (not time averaged).



moves to smaller wavelengths, and the oscillations become damped. The width of the first
peak also increases with increasing dimension, which could indicate that the correlation
length decreases with increasing dimension. The inset to Fig. 8 shows S(k) for a jammed
packing and a fluid near the freezing point in four dimensions. The relation between the
structure factor for the fluid and jammed packing is strikingly similar to what is found
for d = 3, except that the peaks of both curves for d = 4 appear scaled down relative to
d = 3. Overall, our results for both g2 (r) and S(k) are consistent with a recently proposed
“decorrelation” principle [27]. We note that similar pair decorrelations are observed for RSA
packings as the dimension increases up to d = 6 [29].
   It is of interest to determine whether infinite-wavelength density fluctuations S(k = 0)


                                                  20
vanish; systems with this property are called “hyperuniform” [25]. For equilibrium fluids
and crystals, S(k = 0) is proportional to the isothermal compressibility and therefore must
be positive. As for d = 3, S(k) for d = 4 appears to go to zero faster near the origin for the
jammed packing than for the fluid. However, we cannot reliably determine whether S(k)
vanishes at the origin because our calculation of S(k) for small k involved an extrapolation
of the large-x tail of ∆Z(x). Nevertheless, using larger system sizes of one million spheres,
saturated [50] MRJ packings for d = 3 have been shown to be hyperuniform to a high
accuracy [4] and the comparison of d = 4 and d = 5 to d = 3, shown in Fig. 8, suggests that
MRJ packings for d = 4 and d = 5 are also hyperuniform.


   B.   Isostaticity


   We study the near-contact contribution to g2 (r), i.e., interparticle distances r that are
very close to the sphere diameter D, using the cumulative coordination number Z(x), where
as before x = r/D is the dimensionless radius and x − 1 is the dimensionless interparticle
gap. Figure 9 shows Z(x) for jammed packings of 10, 000 spheres for d = 4 and d = 5
with rattlers removed [51]. The plateaus at Z = 8 in Fig. 9 (a) and Z = 10 in Fig. 9 (b)
show that both packings are isostatic. Isostatic packings are jammed packings which have
the minimal number of contacts necessary for collective jamming. For spheres, this occurs
when the number of degrees of freedom equals the number of contacts (or constraints);
each d-dimensional sphere has d degrees of freedom, and hence the mean number of contacts
experienced by a sphere necessary for jamming is 2d, since each contact involves two spheres.
   Packings produced by the LS algorithm almost always contain a nonzero fraction of
“rattlers”, which are spheres trapped in a cage of jammed neighbors, but free to move
within the cage. We find approximately ∼ 1% rattlers for d = 4 and ∼ 0.6% rattlers for
d = 5, as compared to ∼ 2 − 3% rattlers for d = 3 [3]. Rattlers can be identified as having
less than the required d + 1 contacts necessary for local jamming and are removed to study
the jammed backbone of the packing, which we focus on in this section.
   The insets to Fig. 9 (a) and (b) show Z(x)−2d, along with a power-law fit for intermediate
interparticle gap x − 1,
                                  Z(x) = Z̄ + Z0 (x − 1)α ,                              (17)

where Z̄ = 2d. Since the packings are generally slightly subisostatic, we apply a small

                                            21
correction (< 0.1%) to the isostatic prediction of 2d by using the midpoint of the apparent
plateau in Z(x). The best-fit exponent is α ≃ 0.6 in both d = 4 and d = 5, in agreement with
that found for d = 3 [3]. The coefficients of the power law, Z0 ≃ 11 in d = 3, Z0 ≃ 24 for
d = 4, and Z0 ≃ 40 for d = 5 are close to the corresponding kissing numbers of the densest
packings, Z = 12 for d = 3, Z = 24 for d = 4, 40 ≤ Z ≤ 46 for d = 5 and 72 ≤ Z ≤ 80
for d = 6. Motivated by this observation, we measured the value of the gap x − 1 at which
the cumulative coordination Z(x) equals the kissing number of the densest packing to be:
x−1 ≃ 0.35, 0.34, 0.31 −0.36 and 0.33 −0.36 in d = 3, 4, 5 and 6, respectively, which we can
define to be the cutoff for the near-neighbor shell. This definition produces results similar
to that of the more common definition of the cutoff for the near-neighbor shell as the value
of the gap x − 1 at the first minimum in g2 , which occurs at x − 1 ≃ 0.35, 0.32, 0.30 and
0.28 in d = 3, 4, 5 and 6, respectively. It is also interesting to observe that the power-law fit
to Z(x) is good over a rather wide range of gaps, almost up to the first minimum in g2 . We
should, however, emphasize that the minimum of g2 is not very precisely defined, especially
due to decorrelation in high dimensions, and the choice of the gap at the minimum of g2 ,
or at which Z(x) equals the kissing number of the densest packing, as a special point is
somewhat arbitrary and not theoretically justified at present.


V.     DISCUSSION


     We have presented the first numerical results characterizing random jammed hard-sphere
packings in four, five and six dimensions. We find disordered packings, representative of the
maximally random jammed state, to be isostatic and have packing fractions φM RJ ≃ 0.46,
φM RJ ≃ 0.31 and φM RJ ≃ 0.20 for d = 4, 5 and 6, respectively. For equilibrium sphere
packings, we estimate the freezing and melting packing fractions for the fluid-solid transition
in four dimensions to be φF ≃ 0.32 and φM ≃ 0.39, respectively, and in five dimensions to
be φF ≃ 0.19 and φM ≃ 0.24, respectively. Additionally, a signature characteristic of the
kinetic glass transition is observed around φG ≃ 0.41 for d = 4. We observe a significantly
lower tendency to crystallize for d = 4 than in d = 3, which is likely due to the closer
proximity of the melting and kinetic glass transition densities for d = 4 [6].
     We find that in high dimensions the split-second peak in the pair correlation function g2 ,
present for d = 3, gets dramatically diminished and oscillations in both g2 and the structure


                                              22
                           10

                            9   (a)
                            8
                                                  100
                            7
          Coordination Z
                                                                  Numerical data
                                                                               -8            0.6
                            6                                     Z(x-1) - Z(10 ) = 24 (x-1)
                                                   10

                            5



                                              Z
                                                       1
                            4
                                                   0.1
                            3

                            2                     0.01
                                                            -5          -4        -3      -2         -1
                                                           10         10      10        10          10
                            1                                                     x-1
                            0
                                 -14    -12         -10            -8           -6             -4         -2
                                10     10         10             10          10          10              10
                                                                 Gap x-1
                           12

                           11

                           10
                                (b)
                            9
                                                  100
          Coordination Z




                            8                                     Numerical data
                                                                               -8            0.6
                                                                  Z(x-1) - Z(10 ) = 40 (x-1)
                            7                      10

                            6
                                              Z




                                                       1
                            5

                            4                      0.1
                            3

                            2                     0.01
                                                            -5          -4        -3      -2         -1
                                                           10         10      10        10          10
                            1                                                     x-1
                            0
                                 -14    -12         -10            -8           -6             -4         -2
                                10     10         10             10          10          10              10
                                                                 Gap x-1

FIG. 9: The near-contact cumulative coordination Z(x) [c.f. Eq. 12] for 104 -sphere MRJ packings
for d = 4 (a) and for d = 5 (b), with rattlers removed. The inset shows Z(x) on a log-log scale
along with power-law fits for intermediate interparticle gap x − 1 beyond contact. 105 -sphere MRJ
packings in d = 5 with final expansion rates of γ = 10−4 give similar results; such packings with
final expansion rates of γ = 10−5 are (presently) too computationally expensive. Compare these
plots to the equivalent results for d = 3 in Ref.23
                                                  [3] [c.f. Fig. 8].
factor S(k) get significantly dampened. These findings are consistent with a recently pro-
posed “decorrelation principle” [27], stating that unconstrained spatial correlations vanish
asymptotically in the high-dimensional limit and that the n-particle correlation function
gn for any n ≥ 3 can be inferred entirely from a knowledge of the number density ρ and
the pair correlation function g2 (r). Accordingly, in this limit the pair correlation function
g2 (r) would be expected to retain the delta-function contribution from nearest-neighbor
contacts, but the extra structure representing unconstrained spatial correlations beyond a
single sphere diameter would vanish. Figures 7 and 8 show dramatically the decorrelation
principle already taking effect in four, five and six dimensions. We note that decorrelation
principle is also apparent in the same dimensions for RSA packings [29].
   One should not be misled to believe that the decorrelation principle is an expected “mean-
field” behavior. For example, it is well known that in some spin systems correlations vanish
in the limit d → ∞ and the system approaches the mean-field behavior. While this idea
has meaning for spin systems with attractive interactions, hard-core systems, whose total
potential energy is either zero or infinite, cannot be characterized by a mean field. Mean-
field theories are limited to equilibrium considerations, and thus do not distinguish between
“constrained” and “unconstrained” correlations because, unlike us, they are not concerned
with non-equilibrium packings of which there an infinite number of distinct ensembles. The
decorrelation principle is a statement about any disordered packing, equilibrium or not.
For example, contact delta functions are an important attribute of non-equilibrium jammed
disordered packings and have no analog in equilibrium lattice models of any dimension.
The decorrelation principle is also justified on the basis of a rigorous upper bound on the
maximal packing density in high dimensions [27], which has no counterpart in mean-field
theories.
   A particularly interesting property of jammed hard-sphere packings is hyperuniformity,
the complete suppression of infinite wavelength density fluctuations, i.e., the vanishing of
the structure factor S(k) as k → 0. It has been recently conjectured that all saturated
strictly-jammed packings are hyperuniform [25] and calculations of the structure factor near
k = 0 for d = 3 using one million particle systems have strongly suggested that MRJ
packings for d = 3 are indeed hyperuniform [4]. Though the system sizes used in this paper
were too small to probe such large-scale density fluctuations without relying on dubious
extrapolations, our numerical results for the structure factor for d = 4 and d = 5, as shown

                                            24
in Fig. 8, are consistent with hyperuniformity.
   As in three dimensions, disordered jammed sphere packings show no signs of crystalliza-
tion, are isostatic, and have a power-law divergence in g2 (r) at contact. Interestingly, all
three dimensions (3, 4 and 5) share the same power law exponent 1 − α ≃ 0.4 when rattlers
are removed, and show the first minimum of g2 (r) close to where the cumulative coordina-
tion Z(r) equals the kissing number of the densest lattice packing. Such a relation between
the kissing numbers of the densest packings and MRJ packings for d = 3, 4, 5 and 6, if not
coincidental, is very surprising and may be a consequence of the geometrical structure of
MRJ packings. It suggests that disordered packings might be deformed crystal packings, in
which the true contacts are deformed into near contacts, and only the minimal number of
contacts necessary for jamming is preserved. This interpretation is to be contrasted with
the usual interpretation of disordered packing in d = 3 in terms of tetrahedral or icosahe-
dral packings, without relation to the crystal (FCC) packing. The former interpretation is
similar to the one of the MRJ state for binary hard disks as a random partitioning of the
monodisperse triangular crystal into “small” and “large” disks, i.e., a deformed monodis-
perse triangular disk crystal in which a randomly chosen fraction of the particles have grown
in size, as proposed in Ref. [6].
   It is important to point out that hard-sphere packings behave rather differently in two
dimensions than in three and higher dimensions. For d = 2, jammed hard-sphere systems
are polycrystalline and there is a very weak, nearly continuous fluid-solid phase transition.
Hence, there is no glassy behavior for d = 2 and consequently no amorphous jammed pack-
ings. Glassy behavior, due to geometrical frustration arising from the inconsistency of local
optimal packing rules and global packing constraints, first appears in three dimensions [23].
It is likely that geometrical frustration generally increases with dimension, consistent with
our observation that nucleation is suppressed with increasing dimension.
   Computational costs rise dramatically with increasing dimension and theoretical under-
standing based on observations in moderate dimensions is necessary. We believe that the
numerical results presented in this work provide tests and motivations for such theories.




                                            25
   Acknowledgments


   M. S. was supported by the National Science Foundation and A. D. and S. T. were
partially supported by the National Science Foundation under Grant No. DMS-0312067.




 [1] S. Torquato, T. M. Truskett, and P. G. Debenedetti, Phys. Rev. Lett. 84, 2064 (2000).
 [2] A. R. Kansal, S. Torquato, and F. H. Stillinger, Phys. Rev. E 66, 041109 (2002).
 [3] A. Donev, S. Torquato, and F. H. Stillinger, Phys. Rev. E 71, 011105 (2005).
 [4] A. Donev, F. H. Stillinger, and S. Torquato, Phys. Rev. Lett. 95, 090604 (2005).
 [5] M. D. Rintoul and S. Torquato, Phys. Rev. Lett. 77, 4198 (1996).
 [6] A. Donev, F. H. Stillinger, and S. Torquato, Phys. Rev. Lett. 96, 225502 (2006).
 [7] J. L. Finney, Proc. R. Soc. Lond. A 319, 479 (1970).
 [8] C. H. Bennett, J. Appl. Phys. 32, 2727 (1972).
 [9] J. Tobochnik and P. M. Chapin, J. Chem. Phys. 88, 5824 (1988).
[10] A. Z. Zinchenko, J. Comput. Phys. 114, 298 (1994).
[11] N. Xu, J. Blawzdziewicz, and C. O’Hern, Phys. Rev. E 71, 061306 (2005).
[12] P. M. Chaikin and T. C. Lubensky, Principles of condensed matter physics (Cambridge Uni-
    versity Press, Cambridge, United Kingdom, 1995).
[13] M. Luban and A. Baram, J. Chem. Phys. 76, 3233 (1982).
[14] C. J. Joslin, J. Chem. Phys. 77, 2701 (1982).
[15] M. Luban and J. P. J. Michels, Phys. Rev. A 41, 6796 (1990).
[16] M. Bishop, A. Masters, and J. H. R. Clarke, J. Chem. Phys. 110, 11449 (1999); M. Bishop,
    A. Masters, and A. Y. Vlasov, J. Chem. Phys. 121, 6884 (2004); M. Bishop, A. Masters and
    A. Yu. Vlasov, J. Chem. Phys. 122, 154502 (2005); M. Bishop and P.A. Whitlock, J. Chem.
    Phys. 123, 014507 (2005).
[17] N. Clisby and B. McCoy, J. Stat. Phys. 114, 1343 (2004); ibid., 1361 (2004); ibid., 122, 15
    (2006); N. Clisby and B.M. McCoy, J. Phys. 64, 775 (2005).
[18] I. Lyberg, J. Stat. Phys. 119, 747 (2005).
[19] N. Clisby and B. McCoy, J. Stat. Phys. 122, 15 (2006).
[20] H. L. Frisch and J. K. Percus, Phys. Rev. E 60, 2942 (1999).


                                                  26
[21] G. Parisi and F. Slanina, Phys. Rev. E 62, 6554 (2000).
[22] R. Finken, M. Schmidt, and H. Lowen, Phys. Rev. E 65, 016108 (2001).
[23] S. Torquato, Random Heterogeneous Materials: Microstructure and Macroscopic Properties
    (Springer-Verlag, New York, 2002).
[24] A. P. Philipse, Colloids and Surfaces A 213, 167 (2003).
[25] S. Torquato and F. H. Stillinger, Phys. Rev. E 68, 041113 (2003).
[26] G. Parisi and F. Zamponi, J. Stat. Mech. p. P03017 (2006).
[27] S. Torquato and F. H. Stillinger, Experimental Math. (in press).
[28] S. Torquato and F. H. Stillinger, Phys. Rev. E 73, 031106 (2006).
[29] S. Torquato, O. U. Uche and F. H. Stillinger, in preparation.
[30] J. H. Conway and N. J. A. Sloane, Sphere Packings, Lattices, and Groups (Springer-Verlag,
    New York, 1998).
[31] L. Lue, J. Chem. Phys. 122, 044513 (2005).
[32] M. Bishop, P. Whitlock, and D. Klein, J. Chem. Phys. 122, 074508 (2005).
[33] J. P. J. Michels and N. J. Trappaniers, Phys. Lett. A 104, 425 (1984).
[34] T. C. Hales, Ann. Math. 162, 1065 (2005), see also T. C. Hales, arXiv:math.MG/9811078
    (1998).
[35] O. Musin, technical Report, Moscow State University, 2004.
[36] G. D. Scott and D. M. Kilgour, Brit. J. Appl. Phys. 2 863 (1969).
[37] S. Torquato and F. H. Stillinger, J. Phys. Chem. B 105, 11849 (2001).
[38] S. Torquato, A. Donev, and F. H. Stillinger, Int. J. Solids Structures 40, 7143 (2003).
[39] A. Donev, S. Torquato, F. H. Stillinger, and R. Connelly, J. Comp. Phys. 197, 139 (2004).
[40] Ref. [28] presents the first exactly solvable disordered sphere-packing model (“ghost random
    sequential addition packing) in arbitrary space dimension. Specifically, it was shown that all of
    the n-particle correlation functions of this nonequilibrium model can be obtained analytically
    for all allowable densities and in any dimension. It provides an exact demonstration of the
    decorrelation principle; see also Ref. [27]
[41] B. D. Lubachevsky and F. H. Stillinger, J. Stat. Phys. 60, 561 (1990).
[42] A. Donev, S. Torquato, and F. H. Stillinger, J. Comp. Phys. 202, 737 (2005).
[43] M. Ross and B. J. Alder, Phys. Rev. Lett. 16, 1077 (1966).
[44] W. B. Streett, H. J. Raveche, and R. D. Mountain, J. Chem. Phys. 61, 1960 (1974).


                                                  27
[45] D. Frenkel and B. Smit, Understanding Molecular Simulation (Academic Press, 2002).
[46] Z. W. Salsburg and W. W. Wood, J. Chem. Phys. 37, 798 (1962).
[47] R. J. Speedy, J. Phys. Condens. Matter 10, 4387 (1998).
[48] P. M. Chaikin, Soft and Fragile Matter, Nonequilibrium Dynamics, Metastability and Flow
    (M. E. Cates and M. R. Evans, editors) (Institute of Physics Publishing, London, 2000),
    chap. Thermodynamics and Hydrodynamics of Hard Spheres; the role of gravity, pp. 315–348.
[49] The specific extrapolation function we use for both d = 4 and d = 5 is of the form

                                    ∆Z(x) = a1 xe−a2 x cos (a3 x + a4 ),

    where a1 , a2 , a3 , and a4 are fitting parameters.
[50] A saturated packing is one that contains no voids large enough to accommodate an additional
    particle; see Ref. 20, for example.
[51] Due to computational constraints, our packings for d = 6 were produced with a relatively
    high expansion rate (γ = 10−3 ) and were not grown to sufficiently high pressures, as necessary
    to properly distinguish between true contacts and near contacts; therefore, we do not show
    results for d = 6 in this section.




                                                 28
