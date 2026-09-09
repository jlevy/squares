                                                    Quasistatic rheology, force transmission and
                                                     fabric properties of a packing of irregular
                                                                polyhedral particles
arXiv:0805.0178v1 [physics.class-ph] 2 May 2008




                                                                  E. Azéma a,b , F. Radjai a, G. Saussine c
                                                  a Laboratoire de Mécanique et Génie Civil, Université Montpellier 2, Place Eugène

                                                                         Bataillon, 34095 Montpellier cedex 05
                                                      b Present address : Laboratoire Central des Ponts et Chaussées, Démarches

                                                          Durables en Génie Civil, 44341 Bouguenais cedex (Site de Nantes)
                                                  c Innovation and Research Departement of SNCF, 45 rue de Londres, 75379 Paris

                                                                                        Cedex 08



                                                  Abstract

                                                  By means of contact dynamics simulations, we investigate a dense packing composed
                                                  of polyhedral particles under quasistatic shearing. The effect of particle shape is an-
                                                  alyzed by comparing the polyhedra packing with a packing of similar characteristics
                                                  except for the spherical shape of the particles. The polyhedra packing shows higher
                                                  shear stress and dilatancy but similar stress-dilatancy relation compared to the
                                                  sphere packing. A harmonic approximation of granular fabric is presented in terms
                                                  of branch vectors (connecting particle centers) and contact force components along
                                                  and perpendicular to the branch vectors. It is found that the origin of enhanced
                                                  shear strength of the polyhedra packing lies in its higher force anisotropy with
                                                  respect to the sphere packing which has a higher fabric anisotropy. Various con-
                                                  tact types (face-vertex, face-face, etc) contribute differently to force transmission
                                                  and fabric anisotropy. In particular, most face-face contacts belong to strong force
                                                  chains along the major principal stress direction whereas vertex-face contacts are
                                                  correlated with weak forces and oriented on average along the minor principal stress
                                                  direction in steady shearing.

                                                  Key words: granular materials, polyhedral particles, contact dynamics method,
                                                  shear strength, granular fabric, force chain
                                                  PACS: 61.43.Bn, 81.05.Rm, 83.80.Fg, 45.70.Cc




                                                    Email addresses: emilien.azema@lcpc.fr (E. Azéma ),
                                                  radjai@lmgc.univ-montp2.fr (F. Radjai), gilles.saussine@sncf.fr (G.
                                                  Saussine).


                                                  Preprint submitted to Mechanics of Material                          25 October 2018
1   Introduction


Many recent numerical studies of granular media deal with model systems
composed of spherical particles. The use of simplified particle shapes and
contact interactions is needed in order to focus on the collective behavior
of particles which is at the origin of many specific properties of granular
materials. On the other hand, the numerical treatment of complex particle
shapes by discrete element methods was until very recently out of reach due
to demanding computational resources. There is presently, however, consider-
able scope for the numerical investigation of complex granular packings. This
is not only due to available computer power and memory but also because
during more than two decades of intense research in this field, many funda-
mental aspects of granular media have already been established for simpli-
fied particle shapes. In particular, various microscopic features such as fabric
anisotropy (Kruyt and Rothenburg [1996], Bathurst and Rothenburg [1988],
Rothenburg and Bathurst [1989], Radjai et al. [1998], Kruyt and Rothenburg
[2004]), force transmission (Liu et al. [1995], Radjai et al. [1996], Coppersmith et al.
[1996], Mueth et al. [1998], Lovol et al. [1999], Bardenhagen et al. [2000], Antony
[2001], Silbert et al. [2002], Metzger [2004], Majmudar and Behringer [2005])
and friction mobilization (Radjai et al. [1998], Staron and Radjai [2005]) have
been analyzed for circular particles (in 2D) and spheres (in 3D). Hence, a recur-
rent issue today is how robust these findings are with respect to particle shape
(Ouadfel and Rothenburg [2001], Antony and Kuhn [2004], Cambou et al. [2004],
Nouguier-Lehon et al. [2003], Alonso-Marroquin and Herrmann [2002], Pena et al.
[2005, 2006a,b], Azéma et al. [2007]).

The issue of shape effect opens actually the door to a vast and substan-
tial scientific domain given a multitude of potential particle morphologies.
Several well-known examples are elongated and platy shapes (occurring in
biomaterials and pharmaceutical applications), angular and facetted shapes
(occurring in geomaterials) and nonconvex shapes (occurring in sintered pow-
ders). The macroscopic shear behavior is considerably influenced by parti-
cle shape. Rounded particles enhance flowability whereas angular shape is
susceptible to improve shear strength, a factor of vital importance to civil-
engineering applications (Nouguier-Lehon et al. [2003]). In many engineering
applications the particle shapes need to be optimized in order to increase
performance (Markland [1981], Wu and Thompson [2000], Lim and MacDowel
[2005], Saussine et al. [2006], Lobo-Guerrero and Vallejo [2006], Lu and McDowel
[2007]).

In this paper, we employ the contact dynamics method to investigate the
slow shear behavior of granular media composed of polyhedral particles. The
facetted shapes give rise to a rich microstructure where the particles touch
at their faces, edges and vertices. Face-face contacts are expected to play a


                                        2
major role in force transmission and statics of polyhedra by accommodating
long force chains that are basically unstable in a packing composed of spheres.
In order to isolate the effects arising from particle shape, the data from the
polyhedra packing will be compared with a packing of spherical particles that,
apart from the particle shape, is identical in all respects (preparation, friction
coefficients, particle size distribution) to the polyhedra packing. Both packings
are subjected to monotonous triaxial compression.

The numerical procedures will be presented with a brief technical introduction
to the detection and treatment of contacts between polyhedra in the frame-
work of the contact dynamics method. We will consider the stress-strain and
volume-change behavior. The harmonic approximation of the fabric and addi-
tive decomposition of the stress tensor into fabric and force anisotropies will
be presented in detail. This will allow us to assess in clear terms the origins of
shear strength in the polyhedra packing from fabric and force anisotropies in
comparison to the sphere packing. The probability density functions of normal
forces will be studied and compared between the two assemblies. Finally, we
will focus on the contact networks of polyhedral particles and the role played
by different contact categories with respect to force transmission.



2   Numerical method


In this section we briefly introduce the contact dynamics (CD) method with
polyhedral particles and the numerical procedures used for sample prepara-
tion.


2.1 Contact dynamics method with polyhedra


The CD method is based on implicit time integration and nonsmooth formula-
tion of mutual exclusion and dry friction between particles (Jean and Moreau
[1992], Moreau [1994], Radjai and Roux [1999], Dubois and Jean [2003]). The
equations of motion are formulated as differential inclusions in which velocity
jumps replace accelerations (Moreau [1994]). The unilateral contact interac-
tions and Coulomb friction law are represented as set-valued force laws. The
implementation of the time-stepping scheme requires the geometrical descrip-
tion of each potential contact in terms of contact position and its normal unit
vector.

At each time step, all kinematic constraints implied by enduring contacts are
simultaneously taken into account together with the equations of motion in
order to determine all velocities and contact forces in the system. This problem


                                       3
is solved by an iterative process pertaining to the non-linear Gauss-Seidel
method that consists of solving a single contact problem, with other contact
forces being treated as known, and iteratively updating the forces until a given
convergence criterion is achieved. The method is thus able to deal properly
with the nonlocal character of the momentum transfers resulting from the
impenetrability of the particles and friction law.


The CD method is unconditionally stable due to its inherent implicit time
integration method. The uniqueness of the solution at each time step is not
guaranteed for perfectly rigid particles. However, by initializing each step with
the forces calculated in the preceding step, the variability of admissible so-
lutions shrinks to the numerical resolution. In the discrete element methods
based on molecular dynamics, this “force history” is, by construction, included
in the particle positions.


The treatment of a contact interaction between two particles requires the
identification of the contact zone and a “common plane”. For rigid parti-
cles it is possible to define this contact zone by a finite set of points. Before
applying the contact detection algorithm between a pair of particles of irreg-
ular shapes, a “bounding box” method is used to compute a list of particle
pairs potentially in contact. Then, for each pair, the first step is to determine
if an overlap exists through a 3D extension of the “shadow overlap method”
(Saussine [2004], Dubois and Jean [2003]). Several algorithms exist for overlap
determination between convex polyhedra (Cundall and Strack [1979], Cundall
[1988], Nezami et al. [2004, 2006], Dubois and Jean [2003], Saussine [2004],
Saussine et al. [2006], Pérales [2007]). When an overlap occurs, the contact
plane is determined by computing the intersection between the two particles.


The contacts between polyhedral particles belong to different categories, namely
face-face, edge-face, vertex-face, edge-edge, vertex-vertex, vertex-edge; see Fig.
1. The vertex-vertex and vertex-edge contacts are practically absent. In all
cases, we determine one, two or three contact points which provide a good
description of the contact zone. In this paper, the vertex-edge and edge-edge
contacts are referred to as “simple” contacts whereas the edge-face and face-
face contacts are treated as “double” and “triple” contacts since their repre-
sentation involves 2 and 3 distinct points on the common plane, respectively.


For our simulations, we used the LMGC90 which is a multipurpose software
developed in Montpellier, capable of modeling a collection of deformable or
undeformable particles of various shapes by different resolution algorithms
(Dubois and Jean [2003]).


                                       4
            Fig. 1. Different types of contacts between two polyhedra.

2.2 Sample preparation


We generate two numerical samples. The first sample (S1) is composed of
36933 polyhedra. The particle shape are taken from a library of 1000 digitalised
ballast grains provided by the French Railway Company SNCF. Each particle
has at most 70 faces and 37 vertices and at least 12 faces and 8 vertices. Fig.
2 shows several examples of the polyhedral particles used in the simulations.
The size of a particle is defined as two times the largest distance between the
barycenter and the vertices of the particle, to which we will refer as “diameter”
below. We used the following size distribution: 50% of diameter dmin = 2.5
cm, 34% of diameter 3.75 cm, 16% of diameter dmax = 5 cm. This distribution
represents an approximation of that of railway ballast grains. The sample
contains 7.1 105 vertices and more than 106 faces, the average numbers being
20 and 35, respectively. The second sample (S2) is composed of 19998 spheres
with exactly the same size distribution as in S1. Fig. 3 shows a snapshot of the
two samples in equilibrium state after deposition and isotropic compression
under a constant stress of σ0 = 104 Pa in a rectangular box at zero gravity.

The coefficient of friction is 0.5 between the particles in both samples and
0 with the walls. The normal and tangential coefficients of restitution are
0. The zero restitution simplifies the deposition and compaction process by


                                       5
             Fig. 2. Examples of polyhedra used in the simulations.




Fig. 3. Snapshots of the two packings S1 (polyhedra) and S2 (spheres). The walls
are not shown
enhancing dissipation during dynamics rearrangements. The initial value of
the solid fraction is ρ ≃ 0.6 in both samples. Both samples have a nearly
square bottom of side such that L ≈ l and an aspect ratio H/L ≃ 2, where H
is the height. The initial configuration is defined by H0 ≃ 30DM for S1 and
for S2 with DM the mean diameter.

The isotropic samples are subjected to vertical compression by imposing a
constant downward velocity of 10 cm/s on the upper wall and a constant
confining stress σ2 = σ3 = σ0 on the lateral walls. Each simulation is stopped
for a vertical deformation of 30%. The time step was 2.10−4 s. The CPU
time was 2 10−3 s for S1 and 1 10−3 s for S2, per particle and per time
step on an Apple G5 computer. The deformation process can be considered
to be quasistatic in view of the weak kinetic energy injected into the samples


                                       6
compared to the static pressure. This can be expressed more generally through
the inertial number defined as (GDR-MiDi [2004]):
             s
                 m
    I = ε̇          ,                                                       (1)
                 dp


where ε̇ = Ḣ/H is the vertical strain rate, m is the total mass, p is the mean
pressure and d is the mean particle diameter. In our simulations, we have
I ≃ 10−3 , corresponding to the quasistatic limit.



3   Stress-strain behavior


In this section, we compare the stress-strain and volume-change behavior be-
tween the packings of polyhedra (packing S1) and spheres (packing S2). The
stress and strain variables are defined from numerical data. For the estima-
tion of the stress tensor, we use the ”tensorial moment” M i of each particle i
defined by (Moreau [1997], Staron and Radjai [2005]):
     i
                       fαc rβc ,
                 X
    Mαβ =                                                                   (2)
                 c∈i



where fαc is the α component of the force exerted on particle i at the contact
c, rβc is the β component of the position vector of the same contact c, and
the summation runs over all contact neighbors of particle i (noted briefly by
c ∈ i).

It can be shown that the tensorial moment of a collection of rigid particles is
the sum of the tensorial moments of individual particles (Moreau [1997]). The
stress tensor σ for a packing of volume V is simply given by (Moreau [1997],
Staron and Radjai [2005]):

         1 X i     1 X c c
    σ=         M =      f ℓ ,                                               (3)
         V i∈V     V c∈V α β


where ℓc is the branch vector joining the centers of the two touching particles
at the contact c. Remark that the first summation runs over all particles
whereas the second summation involves the contacts, each contact appearing
only once.

Under triaxial conditions with vertical compression, we have σ1 ≥ σ2 = σ3 ,
where the σα are the stress principal values. Using the Cambridge representa-


                                      7
tion, we define the mean stress p and stress deviator q by (Airey and Wood
[1988]) :


       1
    p = (σ1 + σ2 + σ3 ),                                                     (4)
       3
       1
    q = (σ1 − σ3 ).                                                          (5)
       3

For our system of perfectly rigid particles, the stress state is characterized by
the mean stress p and the normalized shear stress q/p.

The cumulative strain components εα are defined by


           ZH
                 dH ′          ∆H
                                    
    ε1 =            ′
                      = ln 1 +    ,                                          (6)
                  H            H0
         H0
           ZL
                 dL′          ∆L
                                  
    ε2 =             = ln 1 +    ,                                           (7)
                 L′           L0
         L0
           Zl
                 dl′
                               !
                              ∆l
    ε3 =             = ln 1 +    ,                                           (8)
                 l′           l0
           l0


where H0 , l0 and L0 are the initial height, width and length of the simulation
box, respectively and ∆H = H0 − H, ∆l = l0 − l and ∆L = L0 − L are the
corresponding cumulative displacements. The volumetric strain is given by

            ZV
                 dV ′          ∆V
                                    
    εp =            ′
                      = ln 1 +           ,                                   (9)
                  V            V0
           V0




where V0 is the initial volume and ∆V = V − V0 is the total volume change.
The cumulative shear strain is defined by

    εq ≡ ε1 − ε2 .                                                          (10)


Figure 4 displays the evolution of q/p for the packings S1 and S2 as a func-
tion of εq . For both packings, we observe a classical behavior characterized by
a hardening behavior followed by (slight) softening and a stress plateau cor-
responding to the critical state of soil mechanics (Mitchell and Soga [2005]).
The critical-state strength in the case of polyhedra (≃ 0.46) is twice as high
as that of spheres (≃ 0.23). This implies that the polyhedra packing has a


                                             8
                            0.5


                            0.4
                                                          S1
                                                          S2




                      q/p
                            0.3


                            0.2


                            0.1
                               0       0.1        0.2   0.3     0.4
                                                  εq

Fig. 4. The strength parameter q/p as a function of shear strain εq for the polyhedra
packing S1 and sphere packing S2.

                            0.04


                            0.03
                                       S1
                                       S2
                            0.02
                  εp




                            0.01


                                  0
                                   0    0.1       0.2   0.3     0.4
                                                  εq

Fig. 5. The volume change εp as a function of shear strain εq for the packings S1 et
S2.

higher angle of internal friction ϕ defined by

                 3q
     sin ϕ =          .                                                         (11)
               2p + q


At the critical state, we have ϕ = ϕ0 = 34◦ for S1 and ϕ0 = 18◦ for S2.

Figure 5 shows the volumetric strain εp as a function of shear strain εq in S1
and S2. In both packings, we observe an early compaction slightly larger in S2
than in S1. The subsequent dilation is lower in S2 and the critical state with
isochoric deformation is reached at εq = 0.3. Dilation in S1 continues with a
decreasing rate of volume change but the isochoric plateau is not fully reached.
The dilatancy can be expressed in terms of the dilation angle ψ defined by

               εp
     sin ψ =      .                                                             (12)
               εq


We have ψ ≃ 5◦ for S1 and ψ ≃ 2.5◦ for S2 at the stress peak state.


                                              9
                    0.2
                             S1
                     0.1     S2

                      0                            ϕ
                                              ψ=




                ψ
                    -0.1

                    -0.2

                    -0.3
                       0.2        0.3   0.4            0.5   0.6   0.7
                                                   ϕ

Fig. 6. The stress-dilatancy diagram representing the relation between the internal
angle of friction and the dilation angle for polyhedra and spheres.
The variation of ψ versus ϕ, a sort of stress-dilatancy diagram (Wood [1990]),
is displayed in Fig. 6 for polyhedra and spheres. For both packings, we have

    ϕ ≃ kψ + ϕ0 ,                                                             (13)


where k is a constant slightly smaller than 1 in both packings. This corre-
lation between dilatancy and shear stress during stress-strain transients is a
consequence of energy balance. The mechanical work performed on the sys-
tem is partially dissipated in contact interactions and partially used in vol-
ume change (Radjai and Roux [2004]). Several stress-dilatancy relations have
been proposed as flow rules for plastic deformations of granular media (Wood
[1990]). The relation (13) associates the peak state to the largest positive value
of dilatancy and the critical state to zero dilatancy. It shows the “non asso-
ciated” character of the flow rule in granular media (an associated flow rule
implying ϕ = ψ).



4   Harmonic representation of the fabric


The expression of stress tensor in Eq. (3) is an arithmetic mean involving
the branch vectors and contact forces. Hence, in order to analyze the shear
strength properties of the polyhedra packing compared to the sphere packing,
we need a statistical description of the granular microstructure (texture or
fabric) and force transmission.

In the presence of steric exclusions, the granular microstructure is highly dis-
ordered at the particle scale (Troadec [2002], Troadec et al. [2002]). Since me-
chanical interactions are governed by contact and friction, the relevant de-
scriptors of the microstructure are related to the contact network. At the
lowest order, the contact network is characterized by the coordination num-
ber z which describes the compactness of a packing. This is a crude scalar


                                          10
                   6



                    5                                     S1
                                                          S2




                 z
                   4



                    3
                     0        0.1           0.2         0.3        0.4
                                            εq

Fig. 7. Evolution of the coordination number z as a function of the cumulative shear
strain εq for polyhedra (S1) and spheres (S2)
                        0.4


                        0.3
                                                              S2
                                                              S1
                 P(c)




                        0.2


                        0.1


                         0
                          0    2       4            6         8    10
                                                c
Fig. 8. The connectivity P (c) of the contact network for the packings S1 and S2.

information in view of the complex arrangement of the particles, but it is
well-known that the compactness, generally expressed in terms of the solid
fraction, controls the stress-strain behavior under monotonous shearing. Let
us remark here that double and triple contact types (see section 2) are counted
as single contacts for the coordination number although they are represented
by two and three contact points, respectively, in the numerical treatment of
interactions between polyhedra.

The evolution of z for polyhedra and spheres is shown in Fig. 7 as a function
of εq . It is remarkable that z is nearly constant in spite of the overall dilation
in both packings. We have z ≃ 5.5 for polyhedra and z ≃ 4 for spheres. The
connectivity of the contact network can be characterized in more detail by the
fraction P (c) of particles with exactly c contact neighbors. The coordination
number is the mean value of c : z = c cP (c). Fig. 8 shows P (c) for S1 and S2
                                       P

in the critical state. The distribution is broader in S1 than in S2. This shows
the wider range of potential equilibrium states in the polyhedra packing. For
both packings, we observe a peak centered on c = 4 with a higher probability
for S2.

Since the shear stress corresponds to the deviation of stress components from
the mean stress p along different space directions, the coordination number


                                           11
              Fig. 9. Geometry of a contact between two polyhedra.
z as a scalar quantity cannot account for the shear stress and its evolution
with strain. Indeed, the expression of the stress tensor suggests that the useful
information for the analysis of shear stress is the density and average force as
a function of contact orientation. Such functions can be expanded in spherical
harmonics in 3D (Ouadfel and Rothenburg [2001]).

Let n be the unit vector along the branch vector ℓ ; Fig. 9. We set

    ℓ = ℓn,                                                                 (14)


where ℓ is the length of the branch vector. We remark that the unit vector n
does not coincide with the contact normal except in the case of spheres. We
consider the components of the contact force in a local frame defined by n
and an orthoradial unit vector t:

    f = fn n + ft t,                                                        (15)


where fn and ft are the radial and orthoradial components of the contact
force, respectively. The writing of Eq. (15) assumes that t is oriented along
the orthoradial force.

We now define the angular averages associated with the branch vectors ℓ and
contact force vectors f . Let A(Ω) be the set of branch vectors pointing in the
direction Ω ≡ (θ, φ) up to a solid angle dΩ and Nc (Ω) its cardinal. The angles
θ and φ are shown in Fig. 10. The angular averages are defined as follows:


                 Nc (Ω)
      PΩ (Ω) =          ,                                                   (16)
                  Nc


                                      12
                                                    n
                                       θ

                                      φ         t


                            Fig. 10. Spherical coordinates.

                    1      X c
      hℓi(Ω) =                  ℓ,                                           (17)
                  Nc (Ω) c∈A(Ω)
                    1
                               f c,
                           X
    hfn i(Ω) =                                                               (18)
                  Nc (Ω) c∈A(Ω) n
                    1
                               f c,
                           X
     hft i(Ω) =                                                              (19)
                  Nc (Ω) c∈A(Ω) t

where Nc = Nc (Ω)dΩ is the total number of contacts, and ℓc , fnc , and ftc are
             R

the actual values of branch vector length, radial force and orthoradial force
for contact c, respectively.

Under the axisymmetric conditions of our simulations, the four functions de-
fined in Eq. (19) are independent of φ. Fig. 11 displays a polar representation of
these functions in the θ-plane for polyhedra (S1) and spheres (S2) at εq = 0.3.
We observe an anisotropic behavior in all cases except in hℓi(θ) for S2. A weak
anisotropy can be seen for S1 in the latter case. The peak values occur along
the compression axis except for hft i(θ) in which the peaks are inclined at π/4
with respect to the vertical. The magnitude of anisotropy is larger for poly-
hedra compared to spheres except for PΩ (θ) which is weakly anisotropic for
polyhedra.

The simple shapes of the above functions suggest that harmonic approximation
based on spherical harmonics at leading terms captures their anisotropies.
There are 9 second-order basis functions Yml (θ, φ). But only the functions
compatible with the symmetries of the problem, namely independent with
respect to φ and π-periodic as a function of θ, are admissible. For PΩ (θ)
as a scalar, and hℓi(θ) and hfn i(θ) as radial components of the vectors, the


                                           13
                                                        z
                       z                                                S1
                                    S1                                  S2
                                    S2




                       <l>!!"
                                                       P!!""



                           z                                z
                                         !                             
                                                                     




                                                         <f'>!!"
                        <fn>!!"



Fig. 11. Polar representation of density probability function PΩ (θ), hfn i(θ), hft i(θ)
and hℓi(θ) for S1 et S2 in residual state.
only admissible functions are Y00 = 1 and Y20 = 3 cos2 θ − 1. For hft i(θ) as
orthoradial component of a vector, the only function independent of φ and
perpendicular to Y00 = 1 and Y20 = 3 cos2 θ − 1 is sin 2θ. Hence, within the
harmonic model of fabric and force, we have


                 1
      PΩ (θ) =      { 1 + a [3 cos2 θ − 1] },                                      (20)
                4π
      hℓi(θ) = ℓ0 { 1 + al [3 cos2 θ − 1] }                                        (21)
     hfn i(θ) = f0 { 1 + an [3 cos2 θ − 1] },                                      (22)
     hft i(θ) = f0 at sin 2[θ],                                                    (23)

where a, al , an and at are the anisotropy parameters, ℓ0 is the mean branch
vector length, and fR0 the mean force. The probability density function PΩ (θ)
is normalized to 1 ( S PΩ (Ω)dΩ = 1, where S is a sphere of unit radius). The
values of the anisotropies a, al , an and at can be calculated from generalized


                                              14
         0.3                                            0.15



         0.2                      S1                    0.10
                                  S2




                                                   al
                                                                              S1
    a

                                                                              S2
         0.1                                            0.05



          0                                             0.00
           0    0.1    0.2     0.3           0.4            0   0.1   0.2   0.3          0.4
                       εq                                             εq
         0.6                                            0.6

         0.5                                            0.5                   S1   (b)
                                                                              S2
         0.4                      S1   (a)              0.4
                                  S2
    an




                                                   at
         0.3                                            0.3

         0.2                                            0.2

         0.1                                            0.1

          0                                              0
           0    0.1    0.2     0.3           0.4          0     0.1   0.2   0.3          0.4
                       εq                                             εq

Fig. 12. Evolution of anisotropies a, al , an and at with εq for packings S1 and S2.

fabric tensors introduced in Appendix A.

The evolution of the anisotropies with εq are displayed in Fig. 12 for our
packings S1 and S2. The fabric orientation anisotropy a increases with εq
and relaxes to a plateau after passing by a pronounced peak. Its value is
systematically larger for spheres than for polyhedra (by a factor 3 in the
critical state). The branch vector anisotropy al is quite low compared to other
anisotropies and its value all along shearing is negligible for spheres. It is
remarkable that al for polyhedra declines (as εp , see Fig 5) at the beginning
of shearing. The radial force anisotropy an increases as the fabric anisotropy
and tends to a plateau. But, in contrast to fabric anisotropy, its value is
higher for polyhedra than for spheres. In other words, the aptitude of the
polyhedra packing to develop large force anisotropy is correlated with particle
shape rather than with fabric anisotropy (see section 7). The orthoradial force
anisotropy at has a similar behavior except that it takes considerably higher
values in the case of polyhedra compared to spheres. In the following section,
we study the relationship between the fabric and force anisotropies.




5       Origins of shear stress


In this section, we analyze the stresses in the framework of the harmonic
approximation of granular microstructure introduced in the last section. Since
this representation involves continuous functions of contact orientations, we
need to express the stress tensor in integral form. The stress tensor as defined


                                              15
in Eq. (3) is an average:

    σαβ = nc hℓkα fβk ik ,                                                   (24)


where nc = Nc /V is the number density of contacts, ℓkα is the α component of
the branch vector at contact k and ℓkβ is the β component of the force vector
at contact k. The average is taken over all contacts k in the control volume V .
To express this mean as an integral, we introduce the joint probability density
PΩf ℓ (n, f , ℓ) of the force and branch vectors (Bathurst and Rothenburg [1988],
Rothenburg and Bathurst [1989], Ouadfel and Rothenburg [2001]). Then, from
Eq. (24), we have
                Z
    σαβ = nc        PΩf ℓ (n, f , ℓ) ℓ(n) fβ (n, ℓ) nα dΩ df dℓ,             (25)


where dΩ = sin θdθdφ.

Equation (25) can be simplified by integrating out the contribution of ℓ. As-
suming that f is independent of ℓ (an assumption which is verified with a
good approximation), we get
                Z
    σαβ = nc        PΩf (n, f ) hℓi(n) fβ (n) nα dΩ df ,                     (26)


where hℓi PΩf = PΩf ℓ dℓ.
                     R


Finally, integration of (26) over force vector yields the following expression for
the stress tensor:
                Z
    σαβ = nc        PΩ (n) hℓi(n) nα hfβ i(n) dΩ,                            (27)


where hf iPΩ = PΩf df . By introducing the average force components hfn i
                    R

and hft i in this equation, we get
                Z
    σαβ = nc        PΩ (n) hℓi(n) { hfn i(n) nβ + hft i(n) tβ }dΩ.           (28)


This writing of the stress tensor involves the functions previously introduced
with the harmonic representation of the fabric (Eqs. (21), (22), (23) and (23)).
Inserting these functions in the integral expression (Eq. 28) and given the
definitions of mean stress p and stress deviator q in Eq. (5), one gets


     p ≃ nc ℓ0 f0 ,                                                          (29)
     q 2
       ≃ (a + al + an + at ),                                                (30)
     p 5


                                           16
                 0.5

                 0.4                              q/p, S1
                                                  0.4 (a+an+at+al)
                 0.3                              q/p, S2
                                                  0.4 (a+an+at)

                 0.2

                 0.1

                  0
                   0         0.1        0.2       0.3                0.4
                                        εq

Fig. 13. The normalized shear stress q/p as a function of shear strain εq for the
packings S1 and S2 both from direct simulation data and theoretical prediction of
Eq. (30).
where the cross products (aal , aan and aat ) among the anisotropies have
been neglected. Our simulation data are in quantitative agreement with this
“stress-force-fabric” relation (a term coined by Rothenburg and Bathurst in
(Bathurst and Rothenburg [1988], Rothenburg and Bathurst [1989]) ) both for
spheres and polyhedra, as shown in Fig. 13, all along the shear. We note that
the theoretical fit would have been less satisfactory for polyhedra if the branch
vector length anisotropy al were omitted from the description.

Equation (30) is interesting as it exhibits the two origins of shear stress in
a granular system: 1) the fabric anisotropies a and al , related to the branch
vector and 2) the force anisotropies an and at , related to the contact force.
Figure 12 shows that the values of these anisotropy parameters underlying
the shear stress depend on the particle shape. In particular, the total force
anisotropy an + at compared to the total fabric anisotropy a + al is much
higher in the case of polyhedra. In the critical state, we have an + at ≃ 0.88
and a+al ≃ 0.2 for polyhedra, an +at ≃ 0.26 and a+al ≃ 0.24 for spheres. The
high value of the force anisotropy in the case of polyhedra comes from both
radial and orthoradial components whereas in the sphere packing at ≃ 0.05
is much less important than an ≃ 0.21. This suggests that friction is more
directly involved in force transmission in the polyhedral packing than in the
sphere packing. The strong contribution of force anisotropy to the polyhedra
packing is a particle shape effect related to the face-face contacts which carry
most strong forces. This point will be analyzed in more detail below.



6   Force distributions


In this section, we study the probability density functions (pdf’s) P (fn ) for
sphere and polyhedra packings. Fig. 14 shows typical maps of normal forces
in a portion of both packings in the critical state. The 3D force chains can


                                      17
Fig. 14. Force maps in a portion of the packings S1 (right) and S2 (left). The
segments are branch vectors with thickness proportional to the normal force, and
gray level proportional to the depth of field.
                            -1
                       10


                            -2                                         S1   (a)
                       10
                                                                       S2
                 pdf




                            -3
                       10


                            -4
                       10 0           1              2             3               4
                                                     fn
                            -1
                       10


                            -2                                     S1       (b)
                       10
                                                                   S2
                 pdf




                            -3
                       10


                            -4
                       10        -2        -1                  0                   1
                            10            10              10                      10
                                                     fn

Fig. 15. Probability density functions of normal forces in the packings of spheres
and polyhedra.
be observed in both packings, but they seem more tortuous in the case of
polyhedra.

The normal force pdf’s are shown in Fig. 15 on log-linear and log-log scales at
εq = 0, 3. In both pdf’s, the strong forces, i.e. forces above the mean normal
force hfn i, fall off exponentially: P (fn ) ∝ e−βfn /hfn i , with β ≃ 0.9 for S1
and β ≃ 1.1 for S2. In contrast, the shapes of the pdf’s in the range of


                                                18
weak forces (fn < hfn i) are radically different. In the sphere packing, the pdf
slightly bends down as fn → 0 but does not tend to zero. We observe also
a small peak close to the mean force. This is consistent with several other
numerical and experimental observations for isotropic packings (Lovol et al.
[1999], Bardenhagen et al. [2000], Antony [2001], Silbert et al. [2002], Metzger
[2004], Majmudar and Behringer [2005]). In the case of polyhedra, the number
of weak forces bends up as the force tends to zero. For both packings, the range
of weak forces is well approximated by a power-law distribution :

     P (fn ) ∝ [ hffnn i ]α ,                                               (31)


with α = −0.24 for S1 and α = 0.05 for S2. The divergence of the number of
weak forces in S1 should be attributed to the polyhedral shape of the particles
favoring the arching effect an hence a higher fraction of weak forces. The
coefficient of friction has a similar effect though to a lesser extent. We find,
however, that in both systems the fraction of weak forces (fn < hfn i) is about
60%.


7   Contact networks of polyhedral particles


In the case of the polyhedra packing, it is interesting to investigate the orga-
nization of the contact network in terms of simple, double and triple contacts.
The respective fractions of these contact types and their contributions to the
structural anisotropy and force transmission are the key quantities for un-
derstanding the effect of particle shape on the shear strength properties of
granular media. In fact, one expects that the triple (face-to-face) contacts
play an essential role in force transmission. This feature was observed in the
case of polygon packings for side-to-side contacts (Azéma et al. [2007]).

Considering the discrete expression of the stress tensor in Eq. (3) and re-
stricting the summation to each contact type allows us to perform an additive
decomposition:

    σ = σs + σd + σt ,                                                      (32)


where the subscripts s, d and t design the respective contributions of simple,
double and triple contacts. The corresponding stress deviators qs , qd and qt
are then calculated and normalized by the mean stress p. Fig. 16 shows the
evolution of partial shear stresses qs /p, qd /p and qt /p as a function of shear
strain εq . The contribution of simple contacts is larger for double and triple
contacts. However, the double and triple contacts support together the largest
portion of the overall shear stress, i.e. qd + qt > qs .


                                      19
                         0.5

                                                                         s+d+t
                         0.4

                         0.3




                   q/p
                                s
                         0.2
                                               d
                                                              t
                         0.1

                          0
                           0               0.1          0.2        0.3                0.4
                                                        εq

Fig. 16. Evolution of partial shear stresses as a function of shear strain for simple
(s), double (d) and triple (t) contacts, as well as the total shear stress (s+d+t).
                   0.8
                          ks
                   0.6

                                                                                 fs
                   0.4
                                                                                 ft
                   0.2                                                                fd
                                    kd
                           kt
                     0
                      0                  0.1       0.2            0.3             0.4
                                                   εq

Fig. 17. Proportions ks , kd and kt of simple, double and triple contacts (dashed
lines), and the relative average forces fs , fd and ft (full lines) supported by each
contact type as a function of shear strain εq .

The partial shear stress supported by each contact type depends on both the
number of its contacts and their mean force. Fig. 17 shows the proportions ks ,
kd and kt of simple, double and triple contacts as a function of shear strain.
ks declines during shear from 0.75 to 0.71 whereas kd and kt increase from
0.14 to 0.15 and from 0.11 to 0.14, respectively. Hence, the critical state is
characterized by ks ≃ 0.7 et kt ≃ kd ≃ 0.15. Fig. 17 also shows the relative
mean forces fs , fd and ft defined by


     fs = ks hfn is /hfn i,                                                                 (33)
     fd = kd hfn id /hfn i,                                                                 (34)
     ft = kt hfn it /hfn i,                                                                 (35)

where hfn is , hfn id and hfn it correspond to the mean normal forces of simple,
double and triple contacts. We see that fs declines slightly with strain but
is nearly two times larger than ft and 2.3 times larger than fd in the critical
state. We have fs ≃ fd + ft . Hence, the lower contribution of triple contacts
with respect to shear stress can be attributed to both the low level of the mean
force (ft < 0.3) sustained by this class and to their weak number (< 15%).


                                                   20
                        0.06

                        0.04

                        0.02

                        0.00




                   a’
                        -0.02     s
                                  d
                        -0.04     t

                        -0.06
                             0    0.1        0.2      0.3       0.4
                                             εq

Fig. 18. Evolution of the signed anisotropies a′ of simple (s), double (d) and triple
(t) contacts as a function of shear strain εq .

Following the same procedure as for the stress tensor, we now perform a similar
decomposition of the fabric tensor F , defined by Eq. (A.4), into three terms:


     F = Fs + Fd + Ft ,                                                         (36)
                                                                                (37)

where Fs , Fd and Ft are the contributions of simple, double and triple contacts.
The corresponding anisotropies as , ad and at can be extracted, but since the
principal directions of these partial fabric tensors are not necessarily identical
to those of the overall fabric tensor, we define the “signed” anisotropies by
multiplying each partial anisotropy ai by a phase factor cos 2(θF − θFi ):


     a′i = ai cos 2(θF − θFi ).                                                 (38)


Figure 18 shows the evolution of signed anisotropies of the three contact
classes. We see that a′d and a′t increase with shear strain and tend to the
limit value ≃ 0.04. As to a′s , we observe an initial increase followed by rapid
decrease and change of sign at εq ≃ 0.2. This evolution means that during
shear the branch vectors of simple contacts tend to become increasingly per-
pendicular to the major principal direction (the direction of compression). A
map of contact forces projected along the branch vectors is displayed in Fig.
19 in different colors according to the type of contact. The triple contacts,
despite their lower proportion, appear clearly to be correlated in the form of
long chains across the packing. These are mostly parallel to the direction of
compression. We also observe a large number of weak forces mainly at simple
contacts.

The pdf’s of normal forces are shown in Fig. 20 separately for simple, double
and triple contacts. The three contact types are involved in strong and weak
networks. The strong forces have in all cases an exponential behavior but a
major difference is observed in the range of weak forces where the proportion


                                        21
Fig. 19. Map of contact forces projected along branch vectors at εq = 0.4. Line
thickness is proportional to the force. The simple, double and triple contacts are in
red (dark gray), in green (light gray) and in blue (black).

                             -1
                        10
                                                                        s
                                                                        d (a)
                                                                        t
                             -2
                        10
                  pdf




                             -3
                        10


                             -4
                        10             1              2             3            4
                                                      fn
                             -1
                        10
                                                                        s
                                                                        d (b)
                                                                        t
                             -2
                        10
                  pdf




                             -3
                        10


                             -4
                        10        -2        -1                  0                1
                             10            10              10                   10
                                                      fn

Fig. 20. Probability distribution functions of radial forces at simple (s), double (d)
and triple (t) contacts on log-linear (a) and log-log (b) scales.

of simple contacts prevails. This correlation between simple and weak contacts
is interesting as it clearly reveals the contrast between simple contacts, on one
hand, and double and triple contacts, on the other hand, in the organization
of the force network.


                                                 22
                  0.6
                              W
                  0.5    ks

                  0.4                        W        S
                                        kt       kt        W
                                                          kd =kd
                                                                   S

                  0.3
                              S
                         ks
                  0.2

                  0.1

                    0
                     0            0.1             0.2     0.3          0.4
                                                  εq

Fig. 21. Proportions ksS , kdS and ktS of simple (s), double (d) and triple (t) contacts
in the strong network (S) and the corresponding proportions ksW , kdW and ktW in
the weak network (W) as a function of shear strain.
In order to situate the simple, double and triple contacts with respect to the
force network, we have plotted in Fig. 21 the proportions ksS , kdS et ktS of the
three contact sets in the strong network and the corresponding proportions
ksW , kdW et ktW in the weak network as a function of shear strain εq . It is
interesting to note that the proportion of weak simple contacts is quite high
(≃ 0.55). The proportions kdW et kdS of weak and strong double contacts are
identical (≃ 0.07). Finally, we see that most double contacts belong to the
strong network (ktS ≃ 2ktW ).



8   Conclusion


In this paper, granular materials composed of irregular polyhedral particles
were numerically investigated. Macroscopic and microstructural properties
were analyzed by (1) direct comparison with a similar packing composed
of spherical particles and (2) characterization of contact networks and force
transmission. A novel finding of this work is that the origin of enhanced shear
strength in a polyhedra packing compared to a sphere packing lies in force
anisotropy induced by particle shape. The fabric anisotropy associated with
the network of branch vectors is lower in the polyhedra packing. This find-
ing extends the results of a previous study of pentagonal particles in two
dimensions to three dimensions Azéma et al. [2007]. In other words, the force
anisotropy, partially underlying shear strength, is mainly controlled by the
fabric anisotropy in a sphere packing. This mechanism breaks down to some
extent in a packing of polyhedra where force anisotropy results mainly from
the “facetted” particle shape.

The face-face contacts were shown to belong mostly to the strong force net-
work. The local equilibrium structures involving face-face and edge-face con-
tacts accommodate force lines that are basically unstable with spherical par-


                                                 23
ticles. Hence, the term “arching” seems to be more adapted to the description
of force patterns in an assembly of polyhedra than in an assembly of spheres.
This effect is crucial for the probability density function of normal forces in
the range of weak forces that is well approximated by a decreasing power-law
in the case of polyhedra.

In this investigation the polyhedra were irregular with a given number of
faces, edges and vertices. These shape parameters can now be changed and
the resulting packings can be analyzed along the same lines as in the present
investigation. Since the face-face contacts seem to play a key role, it would be
interesting to consider irregular polyhedra with less faces in number but with
larger areas. From a mechanical point of view, there should be little difference
between a small face and a vertex. The best shape from the shear strength
viewpoint can be obtained with a large number of faces of large area, but
these two conditions can not be realized at the same time. It seems thus that
an optimal polyhedral shape should exist with a number of faces of not two
low areas. The work is under way to elucidate this point and other aspects of
the problem concerned with packing structure by systematically changing the
particle shape parameters.

We acknowledge assistance by F. Dubois with the LMGC90 platform em-
ployed for the simulations, as well as the precious help of V. Richefeu with 3D
visualization of forces. This work was funded by the French Railway Society,
the SNCF, and the Région Languedoc-Roussillon of France.




A   Fabric tensors


The anisotropies a, an , at and al can be calculated from the tensors F , H (n) ,
H (t) and H (l) defined by (Bathurst and Rothenburg [1988], Rothenburg and Bathurst
[1989], Ouadfel and Rothenburg [2001]) :


             Z
     Fαβ =       PΩ (θ) nα nβ dΩ,                                         (A.1)
             S
             Z
     (n)
    Hαβ =        hfn i(θ) nα nβ dΩ,                                       (A.2)
             S
             Z
      (t)
     Hαβ =       hft i(θ) nα tβ dΩ,                                       (A.3)
             S
             Z
      (l)
     Hαβ =       hℓi(θ) nα nβ dΩ.                                         (A.4)
             S



                                      24
Using the equations (21), (22), (23) and (23), it is then easy to show that the
corresponding anisotropies are :


         5 F3 − F1
     a=            ,                                                       (A.5)
         2 trF
             (n)      (n)
         5 H3 − H1
    an =                   ,                                               (A.6)
         2    trH (n)
             (t)     (t)
         5 H3 − H1
    at =                 ,                                                 (A.7)
         2 trH (n)
             (l)     (l)
         5 H3 − H1
    al =                 ,                                                 (A.8)
         2 trH (l)

where trH (n) = hf i, trF = 1 et trH (l) = ℓ0 .



References

D.W. Airey and D.M. Wood. ”The Cambridge true triaxial apparatus”, Ad-
   vanced Triaxial Testing of Soil and Rock. Rebert T. Donaghe, Ronald C.
   Chaney & Marshall L. Silver, 1988.
F. Alonso-Marroquin and H. J. Herrmann. Calculation of the incremental
   stress-strain relation of a polygonal packing. Phys. Rev. E, 66(2):021301–,
   August 2002.
S. J. Antony. Evolution of force distribution in three-dimensional granular
   media. Phys Rev E, 63:011302, 2001.
S.J Antony and M.R. Kuhn. Influence of particle shape on granular contact
   signatures and shear strength: new insights from simulations. International
   Journal of Solids and Structures, 41(21):5863–5870, October 2004.
E. Azéma, F. Radjai, R. Peyroux, and G. Saussine. Force transmission in a
   packing of pentagonal particles. Phys. Rev. E, 76:011301, 2007.
S. G. Bardenhagen, J. U. Brackbill, and D. Sulsky. Numerical study of stress
   distribution in sheared granular material in two dimensions. Phys. Rev. E,
   62:3882–3890, 2000.
R. J. Bathurst and L. Rothenburg. Micromechanical aspects of isotropic gran-
   ular assemblies with linear contact interactions. J. Appl. Mech., 55:17, 1988.
B. Cambou, Ph. Dubujet, and C. Nouguier-Lehon. Anisotropy in granular
   materials at different scales. Mechanics of Materials, 36(12):1185–1194,
   December 2004.
S. N. Coppersmith, C.-h. Liu, S. Majumdar, O. Narayan, and T. A. Witten.
   Model for force fluctuations in bead packs. Phys. Rev. E, 53(5):4673–4685,
   1996.
P. A. Cundall and O.D.L. Strack. Discrete numerical model for granular
   assemblies. geotechnique, 29(1):47–65, 1979.


                                      25
P.A. Cundall. Formulation of a three-dimensionnal distinct element model-
   part i: a scheme to detect and represent contacts in a system composed of
   many polyhedral blocks. Int. J. Rock Mech. Min Sci & Geomech. Abstr.,
   1988.
F. Dubois and M. Jean. Lmgc90 une plateforme de développement dédiée à
   la modélisation des problèmes d’intéraction. In Actes du sixième colloque
   national en calcul des structures - CSMA-AFM-LMS -, volume 1, pages
   111–118, 2003.
GDR-MiDi. On dense granular flows. Eur. Phys. J. E, 14:341–365, 2004.
M. Jean and J. J. Moreau. Unilaterality and dry friction in the dynamics of
   rigid body collections. In Proceedings of Contact Mechanics International
   Symposium, pages 31–48, Lausanne, Switzerland, 1992. Presses Polytech-
   niques et Universitaires Romandes.
N. P. Kruyt and L. Rothenburg. Micromechanical definition of strain tensor
   for granular materials. ASME Journal of Applied Mechanics, 118:706–711,
   1996.
N. P. Kruyt and L. Rothenburg. Kinematic and static assumptions for homog-
   enization in micromechanics of granular materials. Mechanics of Materials,
   36(12):1157–1173, December 2004.
W.L. Lim and G.R. MacDowel. Discrete element modelling of railway ballast
   discrete element modelling of railway ballast. Granular Matter, 7:19–29,
   2005.
C.-h. Liu, S. R. Nagel, D. A. Schecter, S. N. Coppersmith, S. Majumdar,
   O. Narayan, and T. A. Witten. Force fluctuations in bead packs. Science,
   269:513, 1995.
S. Lobo-Guerrero and L. E. Vallejo. Discrete element method analysis of
   railtrack ballast degradation during cyclic loading. Granular Matter, 8:195–
   2004, 2006.
G. Lovol, K. Maloy, and E. Flekkoy. Force measurments on static granular
   materials. Phys. Rev. E, 60:5872–5878, 1999.
M. Lu and G.R. McDowel. The importance of modelling ballast particle shape
   in the discrete element method. Granular Matter, 9:69–80, 2007.
T. S. Majmudar and R. P. Behringer. Contact force measurements and stresse-
   induced anisotropy in granular materials. Nature, 435:1079–1082, 2005.
J.G.D Morgan E. Markland. The effect of vibration on ballast beds. Geotech-
   nique, 31(3):3,367–386, 1981.
Philip T. Metzger. Granular contact force density of states and entropy in a
   modified edwards ensemble. Phys. Rev. E, 70(5 Pt 1):051303, Nov 2004.
J.K. Mitchell and K. Soga. Fundamentals of Soil Behavior. Wiley, NY, 2005.
J. J. Moreau. Numerical investigation of shear zones in granular materials. In
   D. E. Wolf and P. Grassberger, editors, Friction, Arching, Contact Dynam-
   ics, pages 233–247, Singapore, 1997. World Scientific.
J.J. Moreau. Some numerical methods in multibody dynamics : application
   to granular. Eur. J. Mech. A/Solids, 13:93–114, 1994.
D. M. Mueth, H. M. Jaeger, and S. R. Nagel. Force distribution in a granular


                                      26
  medium. Phys. Rev. E., 57(3):3164–3169, 1998.
E.G. Nezami, Y.M.A Hashash, D. Zaho, and J. Ghaboussi. A fast contact
  detection for 3-d discrete element method. Computers and Geotechnics, 31:
  575–587, 2004.
E.G. Nezami, Y.M.A Hashash, D. Zaho, and J. Ghaboussi. Shortest link
  method for contact detection in discrete element method. Int. J. Numer.
  Anal. Meth. Geomech., 30:783–801, 2006.
C. Nouguier-Lehon, B. Cambou, and E. Vincens. Influence of particle shape
  and angularity on the behavior of granular materials: a numerical analysis.
  Int. J. Numer. Anal. Meth. Geomech, 27:1207–1226, 2003.
H. Ouadfel and L. Rothenburg. ‘stress-force-fabric’ relationship for assemblies
  of ellipsoids. Mechanics of Materials, 33(4):201–221, April 2001.
A.A Pena, H. J. Herrmann, A. Lizcano, and F. Alonso-Marroquin. Investiga-
  tion of the asymptotic states of granular materials using a discrete model
  of anisotropic particles. In Powders and Grains 2005, pages 697–700. A. A.
  Balkema, 2005.
A.A. Pena, R. Garcia-Rojo, and H.J. Herrmann. Influence of particle shape
  on sheared dense granular media. Granular Matter, In Press, 2006a.
A.A. Pena, A. Lizcano, F. Alonso-Marroquin, and H.J. Herrman. Fluctuations
  at the critical state of a polygonal packing. Int. J. For Numer. Anal. Meth.
  Geomech., 00:1–12, 2006b.
R. Pérales. Contribution à la modélisation des structures maconnées par ap-
  proche discrete. Intégration vers une application industrielle. PhD thesis,
  Université Montpellier II (en cours), 2007.
F. Radjai and S. Roux. Etats internes des milieux granulaires denses. In 14e
  Congres Francais de Mécanique. Toulouse, 1999.
F. Radjai and S. Roux. Contact dynamics study of 2d granular media : Critical
  states and relevant internal variables. In H. Hinrichsen and D. E. Wolf,
  editors, The Physics of Granular Media, pages 165–186, Weinheim, 2004.
  Wiley-VCH.
F. Radjai, M. Jean, J.J. Moreau, and S. Roux. Force distributions in dense
  two dimensional granular systems. Phys. Rev. Letter, 77:274–277, 1996.
F. Radjai, D. E. Wolf, M. Jean, and J.J. Moreau. Bimodal character of stress
  transmission in granular packings. Phys. Rev. Letter, 80:61–64, 1998.
L. Rothenburg and R. J. Bathurst. Analytical study of induced anisotropy in
  idealized granular materials. Geotechnique, 39:601–614, 1989.
G. Saussine. Contribution à la modélisation de granulats tridimensionnels :
  application au ballast. PhD thesis, Université Montpellier II, 2004.
G. Saussine, C. Cholet, P.E. Gautier, F. Dubois, C. Bohatier, and J.J. Moreau.
  Modelling ballast behaviour under dynamic loading. part1 : A 2d polygonal
  discrete element method approach. Comput. Methods Appl. Mech. Eng.,
  195:2841 – 2859, 2006.
L. E. Silbert, G. S. Grest, and J. W. Landry. Statistics of the contact network
  in frictional and frictionless granular packings. Phys. Rev. E, 66:1–9, 2002.
L. Staron and F. Radjai. Friction versus texture at the approach of a granular


                                     27
  avalanche. Phys. Rev. E, 72:1–5, 2005.
H. Troadec. Texture locale et plasticité des matériaux granulaires. PhD thesis,
  Université Montpellier II, 2002.
H. Troadec, F. Radjai, S. Roux, and J.-C. Charmet. Model for granular texture
  with steric exclusions. Phys. Rev. E, 66:041305, 2002.
D.M. Wood. Soil behaviour and critical state soil mechanics. Cambridge
  University Press, Cambridge, England, 1990.
Wu and Thompson. The vibration behavior of railway track at high frequencies
  under multiple preloads and wheel interactions. J Acoust Soc Am, 108(3 Pt
  1):1046–1053, Sep 2000.




                                      28
