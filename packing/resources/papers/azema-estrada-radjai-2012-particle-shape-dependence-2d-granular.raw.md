                                      epl draft




                                      Particle shape dependence in 2D granular media

                                      CEGEO(a) , B. Saint-Cyr1,4 , K. Szarf2 , C. Voivret5 , E. Azéma1 , V. Richefeu2 , J.-Y. Delenne6 , G.
                                      Combe2 , C. Nouguier-Lehon3 , P. Villard2 , P. Sornay4 , M. Chaze3 and F. Radjai1
                                      1
                                        University Montpellier 2, CNRS, LMGC UMR 5508, Place Eugène Bataillon, F-34095 Montpellier Cedex, France.
                                      2
                                        UJF-Grenoble 1, Grenoble-INP, CNRS UMR 5521, 3SR Lab., B.P. 53, F-38041 Grenoble Cedex 09, France.
arXiv:1208.0499v1 [cond-mat.soft] 2 Aug 2012




                                      3
                                        University of Lyon, Ecole Centrale de Lyon, LTDS UMR CNRS 5513, 36 avenue Guy de Colongue, F- 69134 Ecully
                                      cedex, France.
                                      4
                                        CEA, DEN, SPUA, LCU, F-13108 Saint Paul Lez Durance, France.
                                      5
                                        SNCF Innovation and Research Immeuble Lumière, 40 Avenue des Terroirs de France, F-75611 Paris cedex 12,
                                      France.
                                      6
                                        IATE, UMR 1208 INRA-CIRAD-Montpellier Supagro-UM2, 2 place Pierre Viala, F-34060 Montpellier cedex 01,
                                      France.



                                               PACS 45.70.-n – First pacs description
                                               PACS 81.05.Rm – Second pacs description
                                               PACS 61.43.Hv – Third pacs description

                                               Abstract – Particle shape is a key to the space-filling and strength properties of granular matter.
                                               We consider a shape parameter η describing the degree of distortion from a perfectly spherical
                                               shape. Encompassing most specific shape characteristics such as elongation, angularity and non-
                                               convexity, η is a low-order but generic parameter that we used in a numerical benchmark test for a
                                               systematic investigation of shape-dependence in sheared granular packings composed of particles
                                               of different shapes. We find that the shear strength is an increasing function of η with nearly the
                                               same trend for all shapes, the differences appearing thus to be of second order compared to η. We
                                               also observe a nontrivial behavior of packing fraction which, for all our simulated shapes, increases
                                               with η from the random close packing fraction for disks, reaches a peak considerably higher than
                                               that for disks, and subsequently declines as η is further increased. These findings suggest that
                                               a low-order description of particle shape accounts for the principal trends of packing fraction
                                               and shear strength. Hence, the effect of second-order shape parameters may be investigated by
                                               considering different shapes at the same level of η.




                                         The hard-sphere packing is at the heart of various mod-       elongation, angularity, slenderness and nonconvexity are
                                      els for the rheology and (thermo)dynamical properties of         described by distinct groups of parameters, and the effect
                                      amorphous states of matter including liquids, glasses and        of each parameter is not easy to isolate experimentally.
                                      granular materials [1, 2]. Such models reflect both the             In order to evaluate the shape-dependence of gen-
                                      purely geometrical properties of sphere packings, e.g. the       eral granular properties such as packing fraction, shear
                                      order-disorder transition with finite volume change [3],         strength and internal structure for particles of different
                                      and emergent properties arising from collective particle in-     shapes, we designed a numerical benchmark test that was
                                      teractions, e.g. force chains and arching in static piles [4].   simulated and analyzed by the members of a collabora-
                                      As to non-spherical particle packings, rather recent results     tive group (CEGEO). The idea of this test is that various
                                      suggest that such packings exhibit higher shear strength         non-spherical or non-circular shapes can be characterized
                                      than sphere packings [5–15], and may approach unusually          by their degree of distortion from a perfectly spherical or
                                      high packing fractions [2, 16–18]. However, a systematic         circular shape. Let us consider an arbitrary 2D shape as
                                      and quantitative investigation of shape-dependence is still      sketched in Fig. 1. The border of the particle is fully
                                      largely elusive since particle shape characteristics such as     enclosed between two concentric circles: a circumscribing
                                       (a) Collaborative group “Changement d’Echelle dans les GEO-     circle of radius R and an inscribed circle of radius R−∆R.
                                      matériaux” (scale change in geomaterials)                       We define the η-set as the set of all shapes with borders

                                                                                                    p-1
CEGEO et al.


                 R                                                           0.55
                                                                                           A
                                                                                           A’
                                                                             0.50          B
                                                                                           C
                                                                                           D
                                          ∆R                                 0.45




                                                                    *
                                                                     sin ϕ
                                                                             0.40

                                                                             0.35

                                                                             0.30

Fig. 1: An arbitrary particle shape represented by a concentric              0.25
pair of circumscribing and inscribed circles.                                    0   0.1        0.2       0.3   0.4      0.5
                                                                                                      η

enclosed between a pair of concentric circles (spheres in         Fig. 4: Shear strength sin ϕ∗ of packings composed of various
                                                                  particle shapes (see Fig. 2) as a function of η.
3D), touching both circles and having the same ratio

                               ∆R
                          η=      .                        (1)
                                R                              which shape-dependence may be analyzed among parti-
                                                               cles of very different shapes. Within an η-set, each spe-
   Four different particle shapes belonging to the same η- cific shape may further be characterized by higher-order
set are shown in Fig. 2. A non-zero value of η corresponds parameters. The issue that we address in this Letter is to
to non-convexity for A-shape, elongation for B-shape, an- what extent the packing fraction and shear strength are
gularity for C-shape, and a combination of angularity and controlled by η and in which respects the behavior depends
elongation for D-shape.                                        on higher-order shape parameters .
                                                                  The benchmark test is based on the four shapes of Fig.
                                                               2. The A-shape (trimer) is composed of three overlapping
       A              B               C            D           disks touching the circumscribing circle and with their in-
                                                               tersection points lying on the inscribed circle; the B-shape
                                                               (rounded-cap rectangle) is a rectangle touching the in-
                                                               scribed circle and juxtaposed with two half-disks touching
Fig. 2: Four different shapes belonging to the same η-set with the circumscribing circle; the C-shape (truncated trian-
η = 0.4: trimer (A), rounded-cap rectangle (B), truncated tri- gle) is a hexagon with three sides constrained to touch the
angle (C), and elongated hexagon (D).                          inscribed circle and all corners on the circumscribing cir-
                                                               cle; and the D-shape (elongated hexagon) is an irregular
                                                               hexagon with two sides constrained to touch the inscribed
                                                               circle and two corners lie on the circumscribing circle. The
                                                               range of geometrically defined values of η for a given shape
                                                               (defined by a construction method) has in general a lower
                                                               bound η0 . For A and B, the particle shape changes con-
                                                               tinuously√from a disk, so that η0 = 0 whereas we have
                                                               η0 = 1 − 3/2 ≃ 0.13 for C and D.
                                                                  Two different discrete element methods (DEM) were
        A                         B                            used for the simulations: contact dynamics (CD) and
                                                               molecular dynamics (MD). In the CD method, the par-
                                                               ticles are treated as perfectly rigid [20] whereas a linear
                                                               spring-dashpot model was used in MD simulations with
                                                               stiff particles (kn /p0 > 103 , where kn is the normal stiff-
                                                               ness and p0 refers to the confining pressure) [21]. The
                                                               trimers were simulated by both methods for all values of
                                                               η. We refer below as A (for CD) and A’ (for MD) to these
        C                        D                             simulations. The packing C was simulated by MD whereas
                                                               the packings B and D were simulated by CD. In CD sim-
Fig. 3: Snapshots of the simulated packings in the densest ulations, the coefficient of restitution was set to zero. In
isotropic state for η = 0.4.                                   MD simulations, the damping parameter was taken very
                                                               close to the critical damping coefficient so that the resti-
   The parameter η is obviously a rough low-order shape tution coefficient was also negligibly small [22]. Note that
parameter; see also [19]. But, encompassing most spe- in quasi-static flow, the relaxation time of the particles is
cific shape parameters, it provides a general framework in short enough (compared to the inverse shear rate) to al-

                                                              p-2
                                                                                                                    Particle shape

        0.6                                                                  0.92
                         A                                                             A
        0.5              A’                                                  0.91      A’
                         B                                                             B
                         C                                                             C
        0.4              D                                                   0.90      D
        0.3                                                                  0.89
   Mη




                                                                       iso
                                                                       ρ
        0.2                                                                  0.88

        0.1                                                                  0.87

        0.0                                                                  0.86

        -0.1                                                                 0.85
            0      0.1        0.2         0.3    0.4       0.5                   0     0.1      0.2       0.3       0.4       0.5
                                      η                                                               η

Fig. 5: Friction mobilization in the steady state as a function     Fig. 6: Packing fraction in the isotropic state as a function of
of η for different particle shapes.                                 η for different particle shapes.


low for efficient dissipation of kinetic energy in each time        between C and D shapes, on the other hand. This sug-
step. For this reason, in contrast to granular gases, the           gests that nonconvex trimers and rounded-cap rectangles,
exact values of the damping parameters or restitution co-           in spite of their very different shapes, belong to the same
efficients have practically no influence on the numerical           family (rounded shapes). In the same way, the truncated
data analyzed below [23].                                           triangles and elongated hexagons seem to belong to the
   For each shape, several packings of 5000 particles were          family of angular particles and exhibit a shear strength
prepared with η varying from 0 to 0.5. To avoid long-               slightly above that of rounded shapes. Note also that the
range ordering, a size polydispersity was introduced by             results are robust with respect to the numerical approach
taking R in the range [Rmin , Rmax ] with Rmax = 3Rmin              as the packings A and A’ were simulated by two different
and a uniform distribution of particle volumes. A dense             methods.
packing composed of disks (η = 0) was first constructed by             The increase of shear strength with η may be attributed
means of random deposition in a box [24]. For other values          to the increasing frustration of particle rotations as the
of η, the same packing was used with each disk serving              shape deviates from a disk [11, 25]. Since the particles
as the circumscribing circle. The particle was inscribed            may interact at two or three contact points (A-shape) or
with the desired value of η and random orientation inside           through side-to-side contacts (shapes B, C and D), the
the disk. This geometrical step was followed by isotropic           kinematic constraints increase with η and frustrate the
compaction of the packings inside a rectangular frame.              particle displacements by rolling. The restriction of rolling
The gravity g and friction coefficients between particles           leads to enhanced role of friction in the mechanical equilib-
and with the walls were set to 0 during compaction in order         rium and relative sliding of particles during deformation.
to avoid force gradients. Fig. 3 displays snapshots of the          A related static quantity is the mean friction mobilization
packings for η = 0.4 at the end of isotropic compaction1 .          defined by M = hft /(µfn )i, where ft is the magnitude of
   The isotropic samples were sheared by applying a slow            the friction force, fn is the normal force, and the average
downward velocity on the top wall with a constant con-              is taken over all force-bearing contacts in the system.
fining stress acting on the lateral walls. During shear, the           To evaluate the effect of particle shape, we consider the
friction coefficient µ between particles was set to 0.5 and         parameter
to 0 with the walls. The shear strength is characterized                                          M (η)
                                                                                        Mη =               −1                 (3)
by the internal angle of friction ϕ defined by                                                  M (η = 0)
                                    σ1 − σ2                         as a function of η for different shapes, where M (η = 0)
                         sin ϕ =            ,                (2)
                                    σ1 + σ2                         is the friction mobilization for circular particles. Fig. 5
                                                                    shows that Mη is a globally increasing function of η for all
where the subscripts 1 and 2 refer to the principal stresses.       shapes. The parameter η appears also in this respect to
sin ϕ increases rapidly from zero to a peak value before            account for the global trend of friction mobilization, and
relaxing to a constant material-dependent value sin ϕ∗ ,            the differences observed in Fig. 5 among different shapes
which defines the shear strength at large strain at a steady        are rather of second order.
stress state.                                                          We also observe that the proportions of double and
   Figure 4 shows the dependence of sin ϕ∗ with respect             triple contacts for A-shape packings and the proportion of
to η for our different shapes. Remarkably, sin ϕ∗ increases         side-to-side contacts for other shapes increase with η. For
with η at the same rate for all shapes. The data nearly co-         noncircular particles, one should distinguish the coordina-
incide between the A and B shapes, on the one hand, and             tion number Z, defined as the mean number of contact-
   1 Animation videos of the simulations can be found at www.cgp-   ing neighbors per particle, from the “contact coordination
gateway.org/ref012.                                                 number” Zc defined as the mean number of contacts per

                                                                 p-3
CEGEO et al.

                                                                                  0.08
                                                                                                        A
                                                                                                        A’
                                                                                                        B
                                                                                  0.06                  C
                                                                                                        D




                                                                    ρ /ρ(0) - 1
                                                                                  0.04




                                                                    iso
                                                                                  0.02

                           (a)                      (b)
                                                                                  0.00
                                                                                         0     0.1           0.2        0.3      0.4   0.5   0.6
Fig. 7: Pore volume reduction by (a) overlap between self-                                                             η−η0
porosities; (b) steric pores.
                                                                     Fig. 8: Normalized packing fractions fitted by Eq. (6).

particle. Obviously, for the calculation of both Z and Zc
only the force-bearing contacts and non-floating particles         A plausible second-order parameter is
are taken into account [26]. We have Z = Zc ≃ 4 for
                                                                                                                       Vp
the disks in the initial state prepared with µ = 0. This                                                     ν=           ,                    (4)
value corresponds to an isostatic state in which one ex-                                                              πR2
pects Z = 2Nf , where Nf is the number of degrees of             where Vp is the particle volume in 2D. Its complement
freedom of a particle [27]. For frictionless disks, we have      1 − ν is the “self-porosity” of a particle, i.e. the unfilled
Nf = 2 (two translational degrees of freedom), leading to        volume fraction inside the circumscribing circle. Keeping
Z = 4. For noncircular shapes, we have Nf = 3 since the          the radius R of the circumscribing circle constant, ρiso =
rotational degrees of freedom take part in the mechanical        Vp /V varies with η as a result of the relative changes of
equilibrium of the particles. Hence, if isostaticity holds       Vp and the mean volume V per particle. The free (pore)
also for noncircular frictionless particles, we expect Z = 6.    volume per particle is Vf = V − Vp .
We observe instead Z < 5 for all our packings. However,             At η = 0, the free volume Vf is only composed of steric
we find Zc ≃ 6 for η 6= 0 if each side-to-side contact is        voids, i.e. voids between three or more particles, and the
counted twice, representing two independent constraints.         packing fraction is given by ρ(0) = πR2 /V (0). For η > 0,
This result is consistent with the isostatic nature of a pack-   the void patterns are more complex but can be described
ing of frictionless noncircular particles and shows that the     by considering the generic shape of particles belonging to
packings of noncircular shape are not under-constrained as       a given η-set. The borders of a particle involve “hills”,
previously suggested [28]. For µ = 0.5, the packings are         which are the parts touching the circumscribing circle, and
no more isostatic and Z and Zc vary only slightly with η         “valleys” touching the inscribed circle. The volume V per
with values in the range 3 to 4 for Z and in the range 4         particle varies with η by two mechanisms. First, the hills
to 5 for Zc in the course of shearing.                           of a particle may partially fill the valleys of a neighboring
   We now focus on the packing fraction which crucially          particle; Fig. 7(a). Secondly, the steric voids between the
depends on particle shape. Fig. 6 shows the packing frac-        hills shrink as η increases due to the increasing local curva-
tion ρiso in the initial isotropic state as a function of η.     ture of the touching particles; Fig. 7(b). To represent this
We observe a nontrivial behavior for all particle shapes:        excess or loss of pore volume due to the specific jamming
the packing fraction increases with η, passes by a peak de-      configurations induced by particle shapes, we introduce
pending on each specific shape and subsequently declines.        the function h(η) by setting
For the B-shape a sharp decrease of ρiso occurs beyond
                                                                                               V (η) = V (η0 ) − πR2 h(η),                     (5)
η = 0.5 as was shown in [10].
  This unmonotonic behavior of packing fraction was              with h(η0 ) = 0. With these assumptions, the packing
observed by experiments and numerical simulations for            fraction is expressed as
spheroids as a function of their aspect ratio [2, 16, 17, 28–
30]. The decrease of the packing fraction is attributed to                                                           ν(η)ρ(η0 )
                                                                                                     ρ(η) =                       .            (6)
the excluded-volume effect that prevails at large aspect                                                           1 − h(η)ρ(η0 )
ratios and leads to increasingly larger pores which cannot
                                                                   The function ν(η) is known for each shape but h(η)
be filled by the particles [29]. The observation of this un-
                                                                 needs to be estimated. A second-order polynomial ap-
monotonic behavior as a function of η for different shapes
                                                                 proximation
indicates that it is a generic property depending only on
deviation from circular shape. This behavior may thus be                                     h(η) = α(η − η0 ) + β(η − η0 )2                   (7)
explained from general considerations involving the pa-
rameter η but with variations depending on second-order          together with Eq. 6 allows us to recover the correct trend
shape characteristics.                                           and to fit the data as shown in Fig. 8. The error bars

                                                             p-4
                                                                                                                Particle shape


represent the variability at η0 assumed to be the same for       [6] Mirghasemi A., Rothenburg L. and Maryas E.,
all other values of η. The parameter α ensures the increase          Geotechnique, 52 (2002) N 3, 209.
of packing fraction with η at low values of the latter and it    [7] Nouguier-Lehon C., Cambou B. and Vincens E., Int.
basically reflects the shrinkage of steric pores (Fig. 7(b))         J. Numer. Anal. Meth. Geomech., 27 (2003) 1207.
whereas β accounts for the overlap between circumscribing        [8] Azéma E., Radjai F., Peyroux R. and Saussine G.,
                                                                     Phys. Rev. E, 76 (2007) 011301.
circles (Fig. 7(a))) and is responsible for the subsequent
                                                                 [9] Azéma E., Radjai F. and Saussine G., Mechanics of
decrease of the packing fraction.                                    Materials, 41 (2009) 721.
   The fitting parameters in Fig. 8 are α ≃ 1.30, 1.29,         [10] Azéma E. and Radjai F., Phys. Rev. E, 81 (2010)
1.14, 1.17 and β ≃ 1.23, 1.20, 0.23, 0.20 for C, A, D and B          051304.
shapes, respectively with increasing peak value. Note that      [11] Estrada N., Azéma E., Radjai F. and Taboada A.,
the values of β are considerably smaller for B and D that            Phys. Rev. E, 84 (2011) 011306.
have an elongated aspect and for which the overlapping of       [12] Azéma E. and Radjai F., Phys. Rev. E, 85 (2012)
self-porosities prevails as compared to A and C for which            031303.
the shrinkage of the initial pores is more important.           [13] Nouguier-Lehon C., Comptes Rendus Mécanique, 338
   In summary, our benchmark simulations show that a                 (2010) 587.
                                                                [14] Saint-Cyr B., Delenne J.-Y., Voivret C., Radjai F.
low-order shape parameter η, describing deviation with
                                                                     and Sornay P., Phys. Rev. E, 84 (2011) 041302.
respect to circular shape, controls to a large extent both
                                                                [15] Szarf K., Combe G. and Villard P., Powder Technol-
the shear strength and packing fraction of granular me-              ogy, 208 (2011) 279.
dia composed of noncircular particles in 2D. The shear          [16] Donev A., Stillinger F., Chaikin P. and Torquato
strength is roughly linear in η whereas the packing frac-            S., Phys. Rev. Lett., 92 (2004) 255506.
tion is unmonotonic. Our simple model for this unmono-          [17] Donev A., Cisse I., Sachs D., Variano E., Stillinger
tonic behavior is consistent with the numerical data for             F., Connelly R., Torquato S. and Chaikin P., Sci-
all shapes. It is governed by a first-order term in η for            ence, 303 (2004) 990.
the shrinkage of the initial steric pores and a second-order    [18] Jiao Y., Stillinger F. H. and Torquato S., Phys.
term in η for the creation of large pores by shape-induced           Rev. E, 041304 (2010) 1.
steric pores. The effect of higher-order shape parameters       [19] Pöschel T. and Buchholtz V., Phys. Rev. Lett., 71
                                                                     (1993) 3963.
may be analyzed also in this framework in terms of differ-
                                                                [20] Radjai F. and Richefeu V., Mechanics of Materials, 41
ences in packing fraction and shear strength among various
                                                                     (2009) 715.
shapes belonging to the same η-set. An interesting issue        [21] Combe G. and Roux J.-N., Discrete numerical simula-
to be addressed in future is whether a generic second-order          tion, quasistatic deformation and the origins of strain in
parameter accounting for such differences exists. Another            granular materials in proc. of Deformation Characteris-
aspect that merits further investigation is the joint ef-            tics of Geomaterials, edited by et al. D. B., 2003 pp.
fects of size polydispersity and particle shape. The shear           1071–1078.
strength is independent of particle size polydispersity as a    [22] Brilliantov N. V., Spahn F., Hertzsch J.-M. and
result of the capture of force chains by the class of larger         Pöschel T., Phys. Rev. E, 53 (1996) 5382.
particles [31]. But the packing fraction and force and con-     [23] Roux J.-N. and Chevoir F., Dimensional analysis and
tact anisotropy depend on both shape and polydispersity.             control parameter in book. of Discrete-element Modeling
                                                                     of Granular Materials (ISTE-Wiley), edited by F.Radjai
                                                                     and F.Dubois., 2011 Ch. 8 pp. 223–253.
                            ∗∗∗                                 [24] Voivret C., Radjai F., Delenne J.-Y. and Youssoufi
                                                                     M. S. E., Phys. Rev. E, 76 (2007) 021301.
  We thank B. Cambou and F. Nicot for stimulating dis-          [25] Estrada N., Taboada A. and Radjai F., Phys. Rev.
cussions. We also acknowledge financial support of the               E, 78 (2008) 021301.
French government through the program PPF CEGEO.                [26] Combe G. and Roux J.-N., Construction of granular as-
                                                                     semblies under static loading in book. of ,Discrete-element
                                                                     Modeling of Granular Materials (ISTE-Wiley), edited by
REFERENCES                                                           F.Radjai and F.Dubois., 2011 Ch. 6 pp. 153–180.
                                                                [27] Agnolin I. and Roux J.-N., Phys; Rev. E, 76 (2007)
 [1] Binder K. and Kob W., Glassy materials and disordered           061302.
     solids (World Scientific) 2005.                            [28] Donev A., Connelly R., Stillinger F. and
 [2] Man W., Donev A., Stillinger F., Sullivan M.,                   Torquato S., Phys. Rev. E, 75 (2007) 051304.
     Russel W., Heeger D., S.Inati, Torquato S. and             [29] Williams S. and Philipse A., Phys. Rev. E, 67 (2003)
     Chaikin P., Phys. Rev. Lett., 94 (2005) 198001.                 051301.
 [3] Torquato S., Truskett T. M. and Debenedetti                [30] Sacanna S., Rossi L., Wouterse A. and Philipse A.,
     P. G., Phys. Rev. Lett., 84 (2000) 2064.                        Journal of Physics, 19 (2007) 376108.
 [4] Radjai F., Wolf D. E., Jean M. and Moreau J., Phys.        [31] Voivret C., Radjai F., Delenne J.-Y. and El Yous-
     Rev. Letter, 80 (1998) 61.                                      soufi M. S., Phys. Rev. Lett., 102 (2009) 178001.
 [5] Ouadfel H. and Rothenburg L., Mechanics of Mate-
     rials, 33 (2001) 201.


                                                            p-5
