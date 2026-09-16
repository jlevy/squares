                                                      Newtonian Event-Chain Monte Carlo and Collision Prediction with
                                                      Polyhedral Particles
                                                               Marco Klement,1 Sangmin Lee,2, 3 Joshua A. Anderson,2 and Michael Engel1, a)
                                                               1)
                                                                  Institute for Multiscale Simulation, IZNF, Friedrich-Alexander University Erlangen-Nürnberg, 91058 Erlangen,
                                                               Germany
                                                               2)
                                                                  Department of Chemical Engineering, University of Michigan, Ann Arbor, MI 48109,
                                                               USA
                                                               3)
                                                                  Department of Biochemistry, University of Washington, Seattle, WA 98195,
                                                               USA
arXiv:2104.06829v1 [cond-mat.stat-mech] 14 Apr 2021




                                                               (Dated: 15 April 2021)
                                                               Polyhedral nanocrystals are building blocks for nanostructured materials that find applications in catalysis and
                                                               plasmonics. Synthesis efforts and self-assembly experiments have been assisted by computer simulations that
                                                               predict phase equilibra. Most current simulations employ Monte Carlo methods, which generate stochastic
                                                               dynamics. Collective and correlated configuration updates are alternatives that promise higher computational
                                                               efficiency and generate trajectories with realistic dynamics. One such alternative involves event-chain updates
                                                               and has recently been proposed for spherical particles. In this contribution, we develop and apply event-
                                                               chain Monte Carlo for hard convex polyhedra. Our simulation makes use of an improved computational
                                                               geometry algorithm XenoSweep, which predicts sweep collision in a particularly simple way. We implement
                                                               Newtonian event chains in the open source general-purpose particle simulation toolkit HOOMD-blue for serial
                                                               and parallel simulation. The speed-up over state-of-the-art Monte Carlo is between a factor of 10 for nearly
                                                               spherical polyhedra and a factor of 2 for highly aspherical polyhedra. Finally, we validate the Newtonian
                                                               event-chain algorithm by applying it to a current research problem, the multi-step nucleation of two classes
                                                               of hard polyhedra.


                                                                                                                      such case are hard particles, in which shape alone is the
                                                                                                                      dominating factor. Hard particle phase diagrams9–12 and
                                                                                                                      equations of states13–15 help to understand experiments
                                                                                                                      and to select promising polyhedral shapes and target
                                                                                                                      structures. Other studies utilize simulations outcomes
                                                                                                                      to predict photonic properties.16
                                                                                                                         Simulations of anisotropic particles are often per-
                                                                                                                      formed stochastically with Monte Carlo methods. Molec-
                                                                                                                      ular dynamics would in principle be favored because it
                                                                                                                      equilibrates configurations more efficiently17 . The rea-
                                                                                                                      son is that density fluctuations relax with the speed of
                                                                                                                      sound in molecular dynamics, whereas such fluctuations
                                                      I.   INTRODUCTION                                               equilibrate by diffusion in Monte Carlo. Furthermore,
                                                                                                                      molecular dynamics creates realistic trajectories, which
                                                                                                                      are an advantage when comparing details of trajecto-
                                                         Nanocrystals can be synthesized in a variety of poly-
                                                                                                                      ries with experiment. However, integrating the equations
                                                      hedral Wulff shapes. They self-assemble by destabi-
                                                                                                                      of motion for anisotropic particles is not easily possible.
                                                      lization in solution or in evaporation and sedimentation
                                                                                                                      This is in particular the case for hard anisotropic par-
                                                      experiments1–4 . The resulting superlattices have applica-
                                                                                                                      ticles, which interact via discontinuous forces. Event-
                                                      tions as functional materials.5 Some particles have sev-
                                                                                                                      driven molecular dynamics is a well-established method
                                                      eral competing superlattice candidates. Octahedra, for
                                                                                                                      for hard spheres to obtain Newtonian trajectories18 . But
                                                      example, can form four different superlattice structures.
                                                                                                                      event-driven molecular dynamics for anisotropic particles
                                                      Three of these are extremal in packing density or contact
                                                                                                                      requires solving collision equations that involve rotations
                                                      area between particles.1,6 While the structures predicted
                                                                                                                      and thus trigonometric functions. The solution of these
                                                      can be reproduced in experiment reliably, the ordering
                                                                                                                      non-linear equations is only possible numerically by it-
                                                      phenomena and pathways to the superlattices are often
                                                                                                                      eration with approximations19 and is necessarily slow.
                                                      not well understood. Varying the types and amounts
                                                                                                                      In Monte Carlo, the problematic collision checks are re-
                                                      of ligand molecules affects the structures found.7,8 Only
                                                                                                                      placed by overlap checks. Importantly, overlaps can be
                                                      for special cases, predictive rules have been found. One
                                                                                                                      solved analytically in a finite number of steps for many
                                                                                                                      shapes, including for polyhedra.20–22 It is thus desirable
                                                                                                                      to combine the advantages of molecular dynamics (fast
                                                      a) Electronic mail: michael.engel@fau.de                        equilibration and realistic dynamics) with the advantages
                                                                                                                              2

of Monte Carlo (simple algorithm and no approximation).         A.   Local Updates
   Here, we develop a simulation method that combines
the advantages of Monte Carlo and molecular dynam-                 Local-update Monte Carlo (LMC) applies a sequence
ics in an algorithm that avoids approximations and it-          of trial moves to update the configuration. A randomly
erations to the extend possible. Our starting point is          selected particle is either translated by a random vec-
event-chain Monte Carlo23,24 , which offers efficient equi-     tor of length up to dtrans or rotated by addition of a
libration and prediction of structures, especially in the re-   random quaternion29 of norm up to drot and subsequent
cently proposed variant of Newtonian event chains.17 We         re-normalization.
generalize Newtonian event-chain Monte Carlo to hard               We denote the probability to execute a translation
convex polyhedra. The algorithmic bottleneck for event-         move as
chain Monte Carlo is the prediction of collisions between
non-rotating polyhedra. The detail that the polyhedra                                     ] translation trials
                                                                     ptrans =                                            ,   (1)
are non-rotating is crucial. It means the underlying equa-                      ] translation trials + ] rotation trials
tions do not contain trigonometric functions and can be
solved analytically.                                            where the character ‘]’ means ‘number of’. The new
   Fast collision detection is a classic problem in com-        configuration is accepted with a Boltzmann factor. The
puter graphics25–27 . Solutions started with the evalua-        Boltzmann factor collapses to an overlap check when sim-
tion of all vertex–face and edge–edge feature combina-          ulating hard particles.
tions of the two polyhedra in question.20 Because the
number of such combinations increases rapidly with the
                                                                B.   Newtonian Event Chains
number of polyhedron vertices, a brute-force calculation
of all combinations is too time consumption. The algo-
rithm by Gilbert, Johnson, and Kerthi21 (GJK) was a               Event-chain Monte Carlo (ECMC)23 applies a se-
major breakthrough. It was not only faster, but sup-            quence of collective moves in the form of chains to up-
ported all sorts of convex objects – as long as there is        date the configuration. Each chain consists of a random
a support function that returns the furthest vector of          start followed by a series of deterministic collision events.
an object for any given direction. Due to its conceptual        A randomly selected particle is translated in a random
complexity, the GJK algorithm remains cumbersome to             chain direction up to its first collision. The collision part-
implement. Snethen22 created with Xenocollide a de-             ner then takes over and continues the translation in the
rived algorithm that can easily be visualized at any step.      chain direction up to its first collision. At this point the
Xenocollide is the starting point of the collision predic-      third particle takes over and so on. ECMC terminates
tion algorithm presented in this paper. Similar to the          the chain after a predefined chain length.
directional contact range28 calculation, we determine the         ECMC only translates particles and has been applied
directional contact distance of convex polyhedra. This          only to disks and spheres23 , and point particles with in-
is the distance by which a polyhedron can be translated         teraction potentials. To treat anisotropic particles, we
without rotation up to collision, a process called ‘sweep-      mix event-chain translations with LMC rotation trial
ing’. The algorithm we present here, called XenoSweep,          moves as illustrated in Fig. 1. The probability to exe-
predicts sweep collisions and is particularly simple.           cute an event chain is
   The central goal of the present manuscript is method                                      ] event chains
development. We first implement Newtonian event-chain                   pchain =                                       .     (2)
Monte Carlo of polyhedral particles utilizing XenoSweep                             ] event chains + ] rotation trials
in an open source software package and test it exten-              We recently introduced Newtonian event-chain Monte
sively. We then confirm that the algorithm indeed has           Carlo (NEC) as a variant of ECMC that is more efficient
the expected efficiency advantages. An advantage of             but still follows the correct statistics, which is guaran-
Newtonian event-chain Monte Carlo is that the partially         teed by the fact that it obeys the balance condition.17
stochastic trajectories generated resemble Newtonian dy-        NEC associates each particle with a velocity vector. A
namics significantly better than the fully stochastic tra-      randomly selected particle is translated in the direction
jectories of Monte Carlo with local moves only.                 of its velocity vector up to the first collision. During this
                                                                translation, time advances by ∆ti = ∆xi /vi , where ∆xi
                                                                is the translation distance and vi the velocity of the trans-
II.   MONTE CARLO SIMULATION
                                                                lated particle. The velocities of both particles involved
                                                                in the collision are updated at the collision according to
   We consider a system of anisotropic particles. The sys-      the rules of elastic collisions. The chain then continues
tem is fully specified by the position vectors {xi }i and       with the collision partner as in ECMC. NEC terminates
orientation quaternions {qi }i of all particles and their
                                                                                                                    P
                                                                the chain after a predefined chain time tchain = i ∆ti .
shape. The most commonly employed strategy to simu-
late anisotropic particles is Monte Carlo with local up-
dates of the positions and orientations.
                                                                                                                           3

                                                                 It has the expression
                                                                                     ] translation moves
                                                                   µ=
                                                                          ] translation moves + ] rotation moves
                                                                          
                                                                          ptrans                               for LMC,
                                                                        =           pchain (Nchain + 1)                  (5)
                                                                                                                for NEC.
                                                                            pchain (Nchain + 1) + (1 − pchain )
                                                                          


                                                                 D.     Parallel Event Chains

                                                                    ECMC can be parallelized with a cell decomposition
                                                                 scheme.24 As cells have a large inactive volume, we use
                                                                 domain decomposition30 to parallelize NEC. Collisions
FIG. 1. Flowchart of Monte Carlo simulation for anisotropic
particles. The algorithm combines event chains for translation   with the domain wall and with particles outside of the cell
moves and random trial rotation moves as in local Monte          are treated as elastic collisions with partners of infinite
Carlo. The type of move is chosen randomly. pchain is the        mass. Such collisions fulfill the detailed balance condition
probability to execute an event chain.                           and lead to ergodic dynamics if the domain walls are
                                                                 shifted every now and then.24
                                                                    We argued that NEC is efficient because the tra-
C.   Parameters                                                  jectories it generates follow Newtonian dynamics more
                                                                 closely.17 However, while collision between particles con-
   LMC and NEC both have three dimensionless param-              serve momentum, collisions with domain walls or outside
eters, which must be tuned for maximal efficiency of the         particles break momentum conservation and break New-
simulation algorithms:                                           tonian dynamics near the walls. The result is a decrease
   (1) The NEC chain time is naturally expressed in units        of the advantage of NEC over LMC. This decrease can
of the mean free time tmf = h∆ti iNEC . The average is           be critical especially for small domains.
conveniently computed in NEC after equilibration. In                Anisotropic particles have an additional issue. The
LMC, the translation trial move distance is naturally            number of chains per cell between two domain wall shifts
expressed in units of the mean free path dmf . We ap-            is not fixed but Bernoulli-distributed with mean pro-
proximate the mean free path using the mean free time            portional to pchain Ndomain and variance proportional to
and the root                                                     pchain (1 − pchain )Ndomain . Here, Ndomain is the average
          p mean square velocity measured in NEC,
dmf ≈ tmf hv 2 i. We call the joint parameter the trans-         number of particles in the domain. Whenever domain
lation parameter. It is given by                                 walls are to be shifted, the simulations for all domains
                                                                 must wait for the slowest domain (with most chains).
                       d                                         The variance can be reduced by using shorter chains, in-
                    
                     trans for LMC,
                    
                                                                 creasing pchain , or generally simulating longer between
                τ = t dmf                             (3)
                     chain for NEC.
                                                                shifting domain walls. Too short chains destroy the ad-
                         tmf                                     vantage of event chains and are not efficient.17

The translation parameter τ behaves differently in LMC
and NEC and will be treated separately below.                    III.    SWEEP COLLISIONS OF CONVEX POLYHEDRA
  (2) The rotation trial move distance drot is identical
in LMC and NEC. We call this parameter the rotation                 Event chains require the prediction of sweep collisions.
parameter,                                                       A sweep collision is the collision of two particles when one
                     (                                           of them is translated along a given direction, the other
                       drot for LMC,                             is not translated, and neither of them is rotated. While
                 ρ=                                  (4)
                       drot for NEC.                             predicting sweep collisions of spheres is trivial, no simple
                                                                 expression exists for anisotropic particles.
   (3) The probability to execute a translation move ptrans         We develop an iterative algorithm for sweep collision
in LMC can be mapped to an equivalent NEC parameter              prediction of convex polyhedra. For this purpose, we
using pchain by observing that the number of translation         simplify and extend Snethen’s XenoCollide algorithm22 .
moves is given by pchain (Nchain + 1), where Nchain is the       XenoCollide utilizes Minkowski portal refinement. Por-
average number of collision events per chain. We call the        tals are triangles that hit the origin when translated (or
fraction of translation moves the move ratio parameter.          swept) along a normalized ray direction r. This means
                                                                                                                  R
                                                                 the portal ray, which is the line {λr | λ ∈ }, inter-
                                                                 sects the triangle. Our modified XenoSweep algorithm
                                                                 not only returns the sweep distance ` at collision but
                                                                                                                                 4

also the normal vector to the collision plane n. The nor-                           Algorithm: XenoSweep
mal vector is not calculated by XenoCollide, but we need              Inputs:    SC      support vector function of C
it to perform elastic collisions in ECMC or NEC.                                 r       ray direction
   Let A and B be two convex particles. Minkowski portal                         vAB     point within C
refinement utilizes the Minkowski difference C = {a − b |             Outputs: `         sweep distance
a ∈ A, b ∈ B}. C contains the origin, if and only if the                         n       normal to collision plane
intersection of A and B is non-empty. Sweep collision                 Variables: vi      vertices of the portal
prediction is equivalent to checking whether C is a portal.                                                 — Initialization —
A further simplification is that we need to know only             1 v1 ← vAB
the support vector SC (v) = x, which is defined as the            2 v2 ← SC (r(r · v1 ) − v1 (r · r))
vector x ∈ C that maximizes x · v. The support vector             3 if v1 · (v2 × r) > 0:

corresponds to the point in C that is extended furthest           4    swap(v1 ,v2 )
along v.                                                                                                 — Portal Discovery —
   The XenoSweep algorithm (Fig. 2) consists of three             5 while True:
stages, an initialization stage and two iterative stages.         6   n ← (v2 − v1 ) × r
Both iteration stages terminate for polyhedra after a fi-         7   v3 ← SC (n)
                                                                  8   if n · v3 < 0:
nite number of iterations bounded from above by the
                                                                  9       return NoCollision
number of vertices. In principle, the algorithm can be
made to scale significantly faster than linearly with the        10     if v1 · (v3 × r) < 0:
number of polyhedron vertices by implementing a tree-            11         v2 ← v3
like data structure for the calculation of the support vec-      12     elif v2 · (v3 × r) > 0:
                                                                 13         v1 ← v3
tor function. However, we do not implement such a data
                                                                 14     else:
structure here to keep the algorithm simple. The first           15         break
iterative stage searches for the existence of a portal only
in the plane perpendicular to the ray direction r. The                                                  — Portal Refinement —
second iterative stage gradually improves the portal to-         16 while True:
wards the collision plane. Differences to XenoCollide are        17   n ← (v3 − v1 ) × (v2 − v1 )
a modified initialization and improved exit conditions.          18   if v1 · n ≥ 0:
                                                                 19       return Overlapping
                                                                 20     v4 ← SC (n)
A.   Initialization                                              21     if (v4 − v1 ) · n ≈ 0:
                                                                 22         ` ← −(v1 · n)/(r · n)
  We initialize the algorithm with two vectors v1 , v2 ∈         23         return `, n
C. These vectors can be chosen arbitrarily, which is what        24     x ← v4 × r
we do for v1 (line 1). We find it efficient to set v2 as the     25     if v1 · x > 0:
support vector in direction r × (r × v1 ) = r(r · v1 ) −         26         if v2 · x ≤ 0:
v1 (r · r) on the opposite side of the particle as seen along    27             v3 ← v4
r towards the origin (line 2). The normal vector n =             28         else:
r × (v2 − v1 ) is the search direction in the next step. We      29             v1 ← v4
guarantee that n points towards the origin, by swapping          30     else:
the initial vectors if that is not yet the case by testing       31        if v3 · x > 0:
the condition v1 · n < 0 (lines 3-4).                            32            v2 ← v4
                                                                 33        else:
                                                                 34            v1 ← v4
B.   Portal Discovery

  The portal discovery stage searches for the existence         FIG. 2. Python-like pseudocode of XenoSweep that extends
of a portal. A portal candidate (v1 , v2 , v3 ) is created      XenoCollide22 . The algorithm consists of the three stages:
by including as v3 the support vector in a direction per-       Initialization, Portal Discovery, and Portal Refinement.
pendicular to r and towards the origin (lines 6-7). By
construction, we can exclude that the origin is behind
the portal in negative normal direction (‘forbidden’ re-        replacing the vector furthest away (regions ‘replace v1
gion in Fig. 3). If n · v3 < 0, we found a separating           and ‘replace v2 ’ in Fig. 3), or breaks and continues with
axis perpendicular to the ray direction r and can return        the next stage if the portal candidate is found to be a
‘NoCollision’ (lines 8-9).                                      portal (lines 10-15).
  Otherwise, we test the intersection of the portal ray
with the portal candidate. Depending on the relative
location of the portal ray, portal discovery continues by
                                                                                                                                 5




                                                                    FIG. 4. Sketch of the portal refinement stage. The portal
                                                                    (v1 , v2 , v3 ) is projected along r. We illustrate an example,
                                                                    where the origin O is located such that v4 replaces v1 .
FIG. 3. Sketch of the portal discovery stage. The portal can-
didate (v1 , v2 , v3 ) is shown in projection along r. The portal
ray is a point in this projection. By construction, we know
                                                                    the same sign. Because the origin ray intersects the por-
this point is located above the line through v1 and v2 and falls
within the portal candidate if and only if the portal candidate
                                                                    tal, the set of scalar products vi · x, i = 1, 2, 3 contain
is a portal. Portal discovery is iterated in the algorithm un-      at least one positive and one negative result, and one
til either a portal is found or it is determined that no portal     replacement criterion is fulfilled implicitly.
exists.

                                                                    D.   Test and validation
C.   Portal Refinement
                                                                       To validate XenoSweep, we set up a well-defined test
   At this point in the algorithm, we successfully discov-          configuration. Two octahedra with edge length 1 are dis-
ered the existence of a portal (v1 , v2 , v3 ). But other           placed by 1.8 in horizontal direction and 5 in vertical
portals might be closer to the origin. The distance of the          direction (Fig. 5(a)). The sweep distance is calculated
portal from the origin along r is ` = −(n · v1 )/(n · r) with       in vertical direction as the second octahedron is rotated.
the portal normal vector n = (v3 − v1 ) × (v2 − v1 ). Here,         For some rotation angles around π/4, the sweep distance
we utilized that r is a normalized vector. The portal re-           is infinite because the octahedra do not collide. An ad-
finement stage searches for the portal with the smallest            vantage of this setup is that the sweep collision can be
`. By construction n · r ≥ 0, and we know ` ≤ 0 if                  calculated analytically.
n · v1 ≥ 0, which means the origin is on the back-side                 Fig. 5(b) compares the accuracy and performance of
of the portal. At this point we cannot distinguish be-              XenoSweep with LinearConvexCastDemo in the Bullet
tween particles moving apart and intersecting particles.            library31 , which includes collision detection by employ-
Because we are not interested in negative sweeps, we re-            ing GJK Ray Casting32 . The Bullet library is a physics
turn ‘Overlapping’ (lines 17-19). If n · v1 ≥ 0 first occurs        engine and is used in many video games and for visual
in a later iteration, then the origin is located between            effects in movies. Our calculations show that the evalu-
the previous and the current portal. Because all portals            ated sweep distance is accurate in both algorithms and
intersect C, the origin is then also inside C and we know           agrees with the analytic solution. We also evaluate the
the particles are intersecting.                                     time for 104 collision. In this test, XenoSweep is signif-
   Next, we compute a new support vector v4 in direc-               icantly faster with a performance that only weakly de-
tion of the normal vector (line 20). We skip the check              pends on the specific geometry. We find an improvement
for a separating axis, n · v4 < 0, that would allow an              of about a factor of 4 in cases with collision, and an
early return in case the goal was only an overlap check             improvement of about a factor of 2 if there is no colli-
instead of calculating the sweep distance. If v4 is copla-          sion. While this single test cannot replace a systematic
nar to the other vectors (up to numerical precision), the           benchmark, it already demonstrates that XenoSweep is
portal is not moving towards the origin anymore, and we             not only simple but also sufficiently fast for our purposes,
return ` as the sweep distance (lines 21-23). Finally, the          and that it compares well with established collision detec-
portal is updated by replacing one of its vertices by v4            tion libraries. A further, more thorough validation will
such that the new triangle remains a portal. We can re-             be presented below where we utilize NEC for the repro-
place vi , i ∈ {1, 2, 3} by v4 when v(i+1) mod 3 · x > 0 and        duction of multi-step nucleation in two thermodynamic
v(i+2) mod 3 · x ≤ 0, where x = v4 × r (lines 24-34). One           systems of hard polyhedra.
example is illustrated in Fig. 4. Based on the result of
a first scalar product, we can choose the second scalar
product either such that one of the replacement criterion
is fulfilled directly or such that both scalar products have
                                                                                                                                     6


(a)




(b)              6
                                                                            FIG. 6. The three polyhedra used for optimizing the parame-
                               Bullet GJK Convex Cast
                5.5            XenoSweep                                    ters of LMC and NEC. The colors and symbols represent the
evaluated




                               analytic solution
 distance
  sweep




                                                                            key for Fig. 7, 8 and 9.
                 5

                4.5                                                                                                         p
                                                                            locity hvi = 0 and root mean square velocity hv2 i = 1.
                  4
                15                                                          We quantify the efficiency of the algorithms by measuring
               12.5
calculations
time for 104




                                                                            the diffusion coefficient in units of CPU time (seconds),
                10
   in ms




                                                                            DCPU . Simulations are performed in single-core mode on
                7.5
                  5
                                                                            Intel Skylake compute nodes. Unless specified otherwise
                2.5                                                         in each of the following sections, we use: τLMC = 2 in
                  0                                                         LMC, τNEC = 30 in NEC, µ = 0.5, ρ = 0.15 for icosa-
                      0   10    20    30    40   50     60   70   80   90   hedron and octahedron; ρ = 0.07 for tetrahedron. The
                                      rotation in degree                    unit of length x in Fig. 7, 8 and 9 is the length of a cube
                                                                            with the same volume for each shape.
FIG. 5. Comparison of collision prediction with XenoSweep
and with the Bullet library.31 (a) Geometry for collision pre-
diction tests. Two octahedra are placed with vertical and                   A.   Translation parameter
horizontal (not to scale) offset. (b) The sweep distance of the
octahedra is predicted accurately with both algorithms (top).                  We discuss the translation parameter τ separately for
Time for the calculation of 104 collisions on an Intel Core                 LMC and NEC because it affects the efficienty of both
i5-2400 CPU (bottom). In this test, XenoSweep is notice-                    algorithms differently. In LMC, highest diffusion is ob-
ably faster. The definition of the rotation angle θ (x-axis) is             tained for a translation move distance of about double
indicated in (a).
                                                                            the mean free path, i.e. τ = 2 (Fig. 7(a)). The accep-
                                                                            tance probability of translation moves is about 20% for
                                                                            this choice. Diffusion eventually decreases with increas-
IV.    IMPLEMENTATION AND PARAMETERIZATION
                                                                            ing τ because random translations over large distances
                                                                            generate many overlaps.
   We implemented NECs in the open source general-                             In NEC, chains should be sufficiently long (τ ≥ 10)
purpose particle simulation toolkit HOOMD-blue.30,33                        but increasing their length further has no significantly
HOOME-blue has a well-tested and highly-efficient hard                      detrimental effect (Fig. 7(b)). This behavior agrees with
particle Monte Carlo (HPMC) package, which we ex-                           NEC of hard spheres17 . In both cases, particles that are
tend. From the existing HOOMD-blue codebase, we use                         more spherical (icosahedron; yellow color) diffuse faster
axis-aligned bounding boxes (AABBs), AABB-trees, the                        than particles that are less spherical (tetrahedron; pur-
general management structure for memory, communica-                         ple) with the octahedron (green) located in the middle.
tion via MPI, and file input/output. As a result of this                    We also observe a clear performance advantage (higher
work, NEC for spheres17 and convex polyhedron will be                       diffusion) of NEC over LMC that is greater for the icosa-
included in HOOMD-blue in version 3.0.0.34                                  hedron than the tetrahedron.
   It remains to tune the translation parameter, the ro-
tation parameter, and the move ratio parameter in both
LMC and NEC for maximal efficiency. Three polyhe-                           B.   Rotation parameter
dra are tested, the tetrahedron with four vertices, the
octahedron with six vertices, and the icosahedron with                         The rotation parameter ρ has similar behavior in LMC
twelve vertices (Fig. 6). Every polyhedron is scaled to                     and NEC (Fig. 8). At density 45%, particles still have
have volume V0 = 1. The reference systems contains                          ample space to rotate, which means optimal performance
8000 particles at 45% volume fraction. At this density                      is obtained for rather large orientation changes. Just
all convex polyhedron remain in the fluid phase. Particle                   like for the translation parameter in LMC, optimal per-
velocities in NEC are initialized randomly with mean ve-                    formance generally occurs near values of the acceptance
                                                                                                                                                                         7




                                                                                                   diﬀusion coeﬃcient
     (a)




                                                                                                       Dcpu [x2s-1]
           Dcpu [x2s-1]
                                                                                                                        10-2
           coeﬃcient
            diﬀusion              10-3

                                  10-4                                                                                  10-3


                                  0.7                                                                                   0.7




                                                                                                 acceptance
           acceptance




                                  0.6                                                                                   0.6




                                                                                                  probability
           translation
            probability




                                                                                                   rotation
                                  0.5                                                                                   0.5
                                  0.4                                                                                   0.4
                                  0.3                                                                                   0.3
                                  0.2                                                                                   0.2
                                  0.1
                                         0     1      2     3    4      5       6     7                                    0.01                   0.1               1
                                             translation parameter τ = dtrans / dmf                                                     rotation parameter r

                                  10-1
     (b)
                                                                                          FIG. 8. Effect of the rotation parameter ρ on the diffusion co-
                                                                                          efficient DCPU . Highest diffusion occurs for acceptance proba-
                                                                                          bilities near 20%. We expect diffusion to decrease faster along
             diﬀusion coeﬃcient




                                  10-2                                                    the ρ-axis in more dense systems.
                 Dcpu [x2s-1]




                                                                                                                        10-1

                                  10-3
                                                                                                                        10-2
                                                                                                   diﬀusion coeﬃcient
                                                                                                       Dcpu [x2s-1]
                                  10-4
                                                 1        10    100     1000 10000                                      10-3
                                             translation parameter τ = tchain / tmft


                                                                                                                        10-4
FIG. 7. Effect of the translation parameter τ on the diffusion
coefficient DCPU for (a) LMC and (b) NEC. Highest diffusion
occurs near τ = 2 with a corresponding LMC acceptance
                                                                                                                        10-5
probability of about 20%. As τ increases, diffusion decreases                                                                  0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
for LMC but plateaus for NEC.                                                                                                          move ratio parameter µ


                                                                                          FIG. 9. Effect of the move ratio parameter µ on the diffusion
probability of around 20%. An overall vertical shift of
                                                                                          coefficient DCPU . As expected, a mix of rotation and trans-
the curves can be explained by the role of translation up-                                lation gives highest diffusion. The optimal mix changes with
dates, which dominate diffusion. As before, more spher-                                   the polyhedron shape.
ical particles diffuse faster, and NEC is generally more
efficient than LMC.
                                                                                          ical polyhedra to rotate easily and highly anisotropic
                                                                                          polyhedra to preferentially align face-to-face.
C.    Move ratio parameter                                                                   Generally, the location of the diffusion maximum shifts
                                                                                          towards lower µ in NEC compared to LMC. This confirms
   The move ratio µ is the ratio of translation moves                                     once more that translation moves are more efficient in
among all moves in the simulation and ranges from zero                                    NEC. We do not see a clear choice for µ that would allow
(only rotation) to one (only translation). Simulations                                    us to select a particular optimal parameter value. For
with parameters in either end of the parameter range                                      this reason, we set µ = 0.5 in line with common practice.
are inefficient because particles get easily stuck in their
neighbor shell (Fig. 9)). Shape plays an important role
for the optimal choice of µ. Icosahedra prefer more trans-                                V.   PERFORMANCE
lations (µ >∼ 0), which is explained by the presence of a
rotator phase prior to crystallization.35 Tetrahedra prefer                                 After extending the NEC algorithm to convex poly-
more rotations (µ <∼ 1) due to their strong preference for                                hedra and implementing it in HOOMD-blue, we now
face-to-face contact.36 In general, we expect nearly spher-                               quantify the speed-up of NEC over LMC. For this pur-
                                                                                                                                                  8

     18     12            20        12      60            32         120           Sph   results in higher speed-up (Fig. 10). This makes sense
                                                                                         because, as we have seen in Fig. 9, translations are less
                                                                                         critical for equilibrating polyhedra with low sphericity.
      6
                                                                                         After all, translations benefit directly from NEC whereas
                          10                                                             rotations are not or only indirectly affected by the effi-
                                                                12     32
      8                                                               60
                                                                                         ciency boost. The relationship between sphericity and
                                                           20                Sph
                                                          12                             speed-up is nearly linear.
                           8
                                                                                            The number of vertices also plays a role, but a minor
                    LMC




                                                                           120
             cpu / Dcpu




     12                                                                                  one. For example the pentakis dodecahedron (spheric-
                                                     18
                           6                                                             ity 0.939, 32 vertices) is sped up by a factor of 10 and
            DNEC




                                                 6
                                         12 8                                            the truncated pentakis dodecahedron (sphericity 0.958,
      6                                                                                  120 vertices) is sped up by a factor of 8. The speed-
                           4
                                    6                                                    up is smaller for the truncated pentakis dodecahedron,
                                                                                         which has similar sphericity but more vertices than the
      4                    2    4
                                                                                         pentakis dodecahedron. This behavior can be explained
                               0.3 0.4 0.5 0.6 0.7 0.8 0.9                  1            by details of the XenoSweep algorithm. While an overlap
                                         sphericity Q                                    check with XenoCollide (implemented in LMC) only finds
                                                                                         a separating axis or a shared point, the distance mea-
FIG. 10.     Speed-up of NEC over LMC as quantified by                                   surement with XenoSweep searches for the colliding sur-
the ratio of diffusion coefficients. Twelve convex polyhedra                             face elements. The letter task costs more compute time
and the sphere (labelled ‘Sph’) are tested. The polyhedra                                and, in comparison, slows down faster with the number
are, from bottom left (number of vertices): tetrahedron (4),                             of polyhedron vertices. Interestingly, the NEC speed-up
triangular prism (6), truncated tetrahedron (12), cube (8),                              for the sphere17 falls right on top of the polyhedron data
octahedron (6), elongated dodecahedron (18), cuboctahe-                                  despite the use of conceptually different algorithms for
dron (12), dodecahedron (20), icosahedron (12), truncated                                overlap and collision checks in both cases.
icosahedron (60), pentakis dodecahedron; all vertices of same
distance from the origin (32), and truncated pentakis dodec-
ahedron (120).
                                                                                         B.   Parallel Performance


pose, we analyze the ratio of the diffusion coefficients,                                   To test parallel performance of NEC, we simulate oc-
  NEC
DCPU      LMC
       /DCPU  . The simulation parameters of the algo-                                   tahedra varying the system size and the number of CPU
rithms are chosen as τLMC = 2, τNEC = 30, µ = 0.5.                                       cores. Parallel performance is analyzed by the particle
The rotation parameter is chosen depending on particle                                   update frequency (i.e., how fast the algorithm generates
shape to account for variations in the importance of ro-                                 and executed translations and rotations) and the diffu-
tations as ρ = 0.07 for the tetrahedron, ρ = 0.10 for the                                sion coefficient (i.e., the efficiency of the algorithm to
triangular prism, ρ = 0.15 for the truncated tetrahedron,                                propagate through configuration space). We normalized
the cube, and the octahedron, ρ = 0.3 for the elongated                                  the measurements to the values for a single-core simula-
dodecahedron, and ρ = 1.0 for all others polyhedra in-                                   tion and divide them by the number of cores.
vestigated.                                                                                 Results are shown in Fig. 11. NEC slows down as the
   We put a particular focus on the role of particle shape,                              number of cores increases, and scales better in the parti-
which we describe by the sphericity (or isoperimetric quo-                               cle update frequency than the diffusion coefficient. This
tient) of the polyhedron. Sphericity is defined for a con-                               means domain decomposition has a negative influence on
vex particle as Q = 36πV 2 A−3 with surface area A and                                   the parallel performance of chains, an effect that we find
volume V . Besides single-core performance, we also in-                                  to be particularly strong for small systems. Our obser-
vestigate the scaling behavior for parallel LMC and par-                                 vation is in line with previous research.24 NEC requires
allel NEC.                                                                               correlated translations in chains over significantly larger
                                                                                         distances than translation trial moves in LMC. This can
                                                                                         become problematic. For good parallel efficiency of NEC
A.   Single-Core Performance                                                             beyond a small number of cores, the system should be
                                                                                         rather large, likely contain millions of particles. Mas-
                                                                                         sively parallel simulations on GPUs as performed with
   We analyze the speed-up of NEC over LMC for differ-
                                                                                         LMC37 are not advisable with NEC, though chains with
ent polyhedra in serial (single-core) mode of HOOMD-
                                                                                         local times38 may be an alternative.
blue. As Fig. 10 shows, NEC is significantly more ef-
ficient than LMC for all tested convex polyhedra. The
speed-up is always at least a factor of 2 and can be up
to a factor of 10, with the minimum taken for tetrahedra
and the maximum for icosahedra.
   We observe the trend that higher sphericity generally
                                                                                                                                                                 9

                           particle update frequency / Ncore     diffusion coefficient / Ncore        to start.39 This means our observation is a first indication
                 1.0                                                                                  that it is possible to convert the speed-up derived from
                                                                                                      brief trajectories and diffusion measurements into an ef-
                 0.8
                                                                                                      ficient equilibration of highly complex particle systems
normalized ...




                 0.6                                                                                  with a noticeable (factor 2.0) speed advantage of NEC
                                                                                                      over LMC for TTs a slight (factor 1.2) speed advantage
                 0.4                                                                                  for the highly aspherical TBPs. Still, given the difference
                                                                                                      in system sizes, these numbers are difficult to compare.
                 0.2               Nparticle=8000*13
                                   Nparticle=8000*23                                                  Furthermore, because crystallization is a stochastic pro-
                                   Nparticle=8000*43                                                  cess that becomes more probable with larger system size,
                 0.0
                       1               Ncore              10 1            Ncore                  10   these speed advantages might in fact be underestima-
                                                                                                      tions. Clearly, more simulation work is necessary for a
                                                                                                      rigorous comparison.
FIG. 11. Scaling behavior for parallel NEC for systems of                                                As an added benefit, our simulations directly address
different numbers of particles Nparticle . The algorithm ran on                                       a concern related to the way how Monte Carlo trajec-
the same CPUs but utilized different numbers of cores Ncore ∈                                         tories approach equilibrium. By design, Monte Carlo
{1, 2, 4, 8}. At all times, all CPU cores were completely filled
                                                                                                      and molecular dynamics methods must always reach the
with identical compute jobs to achieve comparable load. The
particle update frequency (left) and the diffusion coefficient
                                                                                                      same equilibrium given sufficient equilibration time. This
(right) are normalized to their single-core values and divided                                        equivalence of algorithms is, however, not necessarily the
by the number of cores. A flat line corresponds to perfect                                            case for trajectories: Monte Carlo trajectories are dis-
scaling.                                                                                              tinct from trajectories produced by molecular dynamics
                                                                                                      at the microscopic level. Molecular dynamics trajecto-
                                                                                                      ries are preferred, in principle, because they resemble
VI.               PATHWAYS OF MULTI-STEP NUCLEATION                                                   the dynamics of experiments more closely. But molec-
                                                                                                      ular dynamics is not easily achievable for polyhedra, be-
   It remains to apply the polyhedron NEC code to                                                     cause the equations that need to be solved are highly
a current research problem. We focus on systems of                                                    non-linear. Event-driven hard particle simulations work
truncated tetrahedra (TTs) and triangular bipyramids                                                  only for spheres or with numerical approximations19 that
(TBPs). Both of these systems show interesting phase                                                  might again affect the trajectories. In contrast, Monte
behavior and unusual phase transformation pathways.39                                                 Carlo is much simpler and therefore currently preferen-
TTs forms a high-density fluid consisting of shared dodec-                                            tially applied to anisotropic particles. A priori there is no
ahedron motifs that nucleate a cF432 crystal. TBPs form                                               guarantee that LMC reaches equilibrium in the same way
a high-density fluid in form of an amorphous network and                                              as integrating Newton’s equations of motions. Is the use
crystallize into a Clathrate I crystal. Importantly, when                                             of Monte Carlo as a replacement for molecular dynamics
simulated at intermediate volume fraction, both systems                                               problematic when analyzing details of phase transforma-
exhibit two-step crystallization. This finding was unex-                                              tions trajectories?
pected and the systems are currently the only known                                                      NEC does not fully reproduce Newtonian dynamics
examples of multi-step phase transitions in a hard par-                                               but resembles it significantly better than Monte Carlo17 .
ticle system. Our aim here is to test whether NEC can                                                 In fact, NEC can reasonably be considered intermediate
reproduce the findings previously made with the LMC                                                   to Monte Carlo and molecular dynamics. Our results
implementation in the HPMC package of HOOMD-blue.                                                     in Fig. 12 and 13 demonstrate that the phenomenon of
This is a good test, because such phase behavior is highly                                            two-step crystallization remain present in NEC. This in-
sensitive to mistakes in the collision prediction (i.e. prob-                                         dicates that the choice of simulation algorithm is, after
lems in the XenoSweep algorithm) and to violations of                                                 all, less crucial. We note that these results are only a pre-
the balance condition (i.e. incorrect statistics in the NEC                                           liminary evaluation of the phenomenon. More in-depth
implementation). Our analysis utilizes the same order                                                 analysis will be required in future to settle the issue more
parameters as in previous work.39                                                                     conclusively.
   Indeed, TTs (Fig. 12) and TBPs (Fig. 13) both repro-
duce all details of the reported two-step crystallization
                                                                                                      VII.   CONCLUSION
pathways. This finding demonstrates that our NEC al-
gorithm follows the correct thermodynamics. Further-
more, NEC simulations of 4000 particles reach initial                                                    We developed, implemented, and tested NEC for con-
crystal formation after 430 core-hours (0.11 h/particle)                                              vex hard polyhedra. The new simulation method is an
for TTs and 292 core-hours (0.07 h/particle) for TBPs.                                                improvement over existing polyhedron simulation codes.
In contrast, previous LMC simulations required 1725                                                   It is multiple times more efficient, cutting simulation
core-hours (TT) for a system of 8000 TT particles                                                     time and resulting in a lower cost and smaller CO2 foot-
(0.22 h/particle) and 1800 core-hours for a system of                                                 print. As an added benefits, NEC returns particle tra-
20,000 TBP particles (0.09 h/particle) for crystallization                                            jectories that are closer to molecular dynamics than con-
                                                                                                                              10

                         a            Frame 100         Frame 300             Frame 523         Frame 797




                         b




                         c




FIG. 12. Analysis of a long NEC trajectory for tetrahedra with truncated tips and edges (TTs) at volume fraction 61%.
The system is known to crystallize in two steps via a prenucleation motif with clusters.39 Views along the (111) direction
depicting (a) the polyhedra and (b) spheres at the centers of the polyhedra. Particles are colored for better visibility of the
crystal, with fluid particles translucent. A high-density fluid phase (orange, left) features a dodecahedron motif with particles
shared across dodecahedron (SD). The crystal phase (red, right) features dodecahedron that do not share particles (NSD).
(c) Characterization of the trajectory with order parameters. See Ref. 39 for a detailed description of the phases and order
parameters.

                         a            Frame 25          Frame 100             Frame 194         Frame 349




                         b




                         c                                                                              0.04
                               0.4
                                                                                                               Clathrate OP




                                                                                                        0.03
                      Density OP




                               0.3

                               0.2                                                                      0.02

                               0.1                                                                      0.01

                               0.0                                                                      0.00
                                  0          50   100         150       200         250   300         350
                                                                    Frame

FIG. 13. Analysis of a long NEC trajectory for triangular bipyramids (TBPs) at volume fraction 50%. The system is known
to crystallize in two steps via a prenucleation motif with a dense network.39 Views along the (100) direction depicting (a) the
polyhedra and (b) spheres at the centers of the polyhedra tetramers. Particles are colored for better visibility of the crystal,
with fluid particles translucent. A high-density fluid phase (blue) features tetrahedral coordination. The crystal phase (red) is
of type clathrate I. (c) Characterization of the trajectory with two order parameters. See Ref. 39 for a detailed description of
the phases and order parameters.
                                                                                                                                11

ventional Monte Carlo simulation. Another advantage is         the Interdisciplinary Center for Functional Particle Sys-
that the virial expression for pressure, often a helpful ob-   tems (FPS), and computational resources and support
servable to identify phase transformations, drops out as       provided by the Erlangen Regional Computing Center
a side product of using event chains without additional        (RRZE) are gratefully acknowledged. Algorithm imple-
effort17,40–42 . In LMC, pressure must be computed sepa-       mentation and optimization in HOOMD-blue supported
rately and requires additional steps. Our method is a first    by the National Science Foundation, Division of Mate-
step towards more general and more versatile simulation        rials Research Award # DMR 1808342. Work imple-
algorithms for anisotropic particles.                          menting the test cases and model verification was sup-
   At the core of NEC lies the sweep collision prediction      ported as part of the Center for Bio-Inspired Energy Sci-
algorithm XenoSweep. This algorithm heavily builds on          ence, an Energy Frontier Research Center funded by the
prior work in the computer graphics community.22 Our           U.S. Department of Energy, Office of Science, Basic En-
new implementation is an important improvement both            ergy Sciences under Award # DE-SC0000989. This work
in terms of speed and in terms of simplicity of the al-        used the Extreme Science and Engineering Discovery En-
gorithm. XenoSweep solves the classic problem of poly-         vironment (XSEDE)45 , which is supported by National
hedron collision prediction and overlap detection43,44 in      Science Foundation grant number ACI-1548562; XSEDE
only 34 lines of pseudocode. Such efficient and simple col-    award DMR 140129.
lision prediction is of interest to researchers working on a
broad range of problems in computer graphics, robotics,
and granular dynamics.                                         BIBLIOGRAPHY
   Future extensions should advance our work in two di-
rections: improved handling of rotations and generaliza-        1 C.-C.   Chang, H.-L. Wu, C.-H. Kuo, and M. H. Huang,
tion to anisotropic particles with extended interaction,          “Hydrothermal Synthesis of Monodispersed Octahedral Gold
i.e. particles that are not purely hard. Concerning the           Nanocrystals with Five Different Size Ranges and Their Self-
first point: While we sped up the effect of translation           assembled Structures,” Chemistry of Materials 20, 7570–7574
moves by about one order of magnitude, rotations re-              (2008).
                                                                2 M. Eguchi, D. Mitsui, H.-L. Wu, R. Sato, and T. Teranishi,
main a bottleneck. This is apparent from Fig. 10. Effi-           “Simple Reductant Concentration-dependent Shape Control of
ciency reduces as the importance of rotations increases,          Polyhedral Gold Nanoparticles and Their Plasmonic Properties,”
which is the case towards more aspherical particles. Fu-          Langmuir 28, 9021–9026 (2012).
                                                                3 J. Henzie, M. Grünwald, A. Widmer-Cooper, P. L. Geissler, and
ture work could develop collective rotations moves that
resemble conceptually the idea of event chains for trans-         P. Yang, “Self-assembly of Uniform Polyhedral Silver Nanocrys-
                                                                  tals into Densest Packings and Exotic Superlattices,” Nature Ma-
lations. Such an improved algorithm has the potential to          terials 11, 131 (2012).
reach a speed-up of up to one order of magnitude across         4 C. Avci, I. Imaz, A. Carné-Sánchez, J. A. Pariente, N. Tasios,
all convex polyhedra. Second, the hard particle condition         J. Pérez-Carvajal, M. I. Alonso, A. Blanco, M. Dijkstra,
employed exclusively in this work is a simplification and         C. López, and D. Maspoch, “Self-assembly of Polyhedral Metal-
limits comparison to experiments. Whereas nanoparticle            organic Framework Particles into Three-dimensional Ordered Su-
                                                                  perstructures,” Nature Chemistry 10, 78–84 (2017).
shape is often of central importance, interactions such as      5 M. A. Boles, M. Engel, and D. V. Talapin, “Self-assembly of
van der Waals forces, electrostatic forces, or the effect of      Colloidal Nanocrystals: From Intricate Structures to Functional
ligands can typically not be entirely ignored. Develop-           Materials,” Chemical Reviews 116, 11220–11289 (2016).
                                                                6 J. Gong, R. S. Newman, M. Engel, M. Zhao, F. Bian, S. C.
ing a general simulation method for anisotropic convex
                                                                  Glotzer, and Z. Tang, “Shape-dependent Ordering of Gold
or concave polyhedra with arbitrary interactions remains
                                                                  Nanocrystals into Large-scale Superlattices,” Nature Communi-
a challenging open problem.                                       cations 8, 14038 (2017).
                                                                7 S.-S. Wang, Z.-H. Xing, G.-Y. Chen, H. Cölfen, and A.-W. Xu,

                                                                  “Cuboctahedral Sb2O3 mesocrystals organized from octahedral
NOTES                                                             building blocks: more than self-similarity,” Crystal Growth &
                                                                  Design 16, 3613–3617 (2016).
                                                                8 F. Lu, T. Vo, Y. Zhang, A. Frenkel, K. G. Yager, S. Kumar, and
   The authors declare no competing financial interest.           O. Gang, “Unusual packing of soft-shelled nanocubes,” Science
An implementation of the XenoSweep algorithm and                  Advances 5, eaaw2399 (2019).
                                                                9 R. Ni, A. P. Gantapara, J. d. Graaf, R. v. Roij, and M. Dijkstra,
NEC for convex polyhedra is included open-source as
                                                                  “Phase Diagram of Colloidal Hard Superballs: From Cubes Via
part of the HPMC package of the general-purpose parti-
                                                                  Spheres to Octahedra,” Soft Matter 8, 8826 (2012).
cle simulation toolkit HOOMD-blue in version 3.0.0.30,33       10 P. F. Damasceno, M. Engel, and S. C. Glotzer, “Crystalline As-

                                                                  semblies and Densest Packings of a Family of Truncated Tetra-
                                                                  hedra and the Role of Directional Entropic Forces,” ACS Nano
ACKNOWLEDGMENTS                                                   6, 609–614 (2012).
                                                               11 P. F. Damasceno, M. Engel, and S. C. Glotzer, “Predictive Self-

                                                                  assembly of Polyhedra into Complex Structures,” Science 337,
  This work has been funded by SFB1411 and the Clus-              453–457 (2012).
                                                               12 A. P. Gantapara, J. d. Graaf, R. v. Roij, and M. Dijkstra,
ter of Excellence Engineering of Advanced Materials of
the German Research Foundation (DFG). Support by                  “Phase Diagram and Structural Diversity of a Family of Trun-
the Central Institute for Scientific Computing (ZISC),
                                                                                                                                             12

   cated Cubes: Degenerate Close-packed Structures and Vacancy-          29 D. Frenkel and B. Smit, Understanding molecular simulation:

   rich States,” Physical Review Letters 111, 015501 (2013).                from algorithms to applications, Vol. 1 (Elsevier, 2001).
13 M. Marechal and H. Löwen, “Density Functional Theory for Hard         30 J.  A. Anderson, M. E. Irrgang, and S. C. Glotzer, “Scalable
   Polyhedra,” Physical Review Letters 110, 137801 (2013).                  Metropolis Monte Carlo for Simulation of Hard Shapes,” Com-
14 M. E. Irrgang, M. Engel, A. J. Schultz, D. A. Kofke, and S. C.           puter Physics Communications 204, 21–30 (2016).
   Glotzer, “Virial Coefficients and Equations of State for Hard         31 Bullet Physics Library - Version 2.81; http://bulletphysics.org.

   Polyhedron Fluids,” Langmuir 33, 11788–11796 (2017).                  32 G. van den Bergen, “Ray Casting against General Convex Ob-
15 J. Tian, H. Jiang, and A. Mulero, “Equations of the state of hard        jects with Application to Continuous Collision Detection,”
   sphere fluids based on recent accurate virial coefficients B5?B12,”      (2004).
   Phys. Chem. Chem. Phys. 21, 13070–13077 (2019).                       33 J. A. Anderson, C. D. Lorenz, and A. Travesset, “General Pur-
16 R. K. Cersonsky, J. Dshemuchadse, J. Antonaglia, G. v. Anders,           pose Molecular Dynamics Simulations Fully Implemented on
   and S. C. Glotzer, “Pressure-tunable photonic band gaps in an            Graphics Processing Units,” Journal of Computational Physics
   entropic colloidal crystal,” Physical Review Materials 2, 125201         227, 5342–5359 (2008).
   (2018).                                                               34 HOOMD-blue; http://hoomd-blue.readthedocs.io/.
17 M. Klement and M. Engel, “Efficient equilibration of hard spheres     35 M. Mravlak and T. Schilling, “On the phase diagram of Mackay

   with Newtonian event chains,” The Journal of Chemical Physics            icosahedra,” The Journal of Chemical Physics 149, 134502
   150, 174108 (2019).                                                      (2018).
18 B. Alder and T. Wainwright, “Studies in Molecular Dynamics.           36 A. Haji-Akbari, M. Engel, A. S. Keys, X. Zheng, R. G. Petschek,

   Ii. Behavior of a Small Number of Elastic Spheres,” Journal of           P. Palffy-Muhoray, and S. C. Glotzer, “Disordered, quasicrys-
   Chemical Physics 33, 1439–1451 (1960).                                   talline and crystalline phases of densely packed tetrahedra,” Na-
19 A. Donev, S. Torquato, and F. H. Stillinger, “Neighbor list
                                                                            ture 462, 773–777 (2009).
   collision-driven molecular dynamics simulation for nonspherical       37 J. A. Anderson, E. Jankowski, T. L. Grubb, M. Engel, and S. C.
   hard particles. I. Algorithmic details,” Journal of Computational        Glotzer, “Massively parallel Monte Carlo for many-particle simu-
   Physics 202, 737–764 (2005).                                             lations on GPUs,” Journal of Computational Physics 254, 27–38
20 J. Canny, “Collision detection for moving polyhedra,” IEEE
                                                                            (2013).
   Transactions on Pattern Analysis and Machine Intelligence , 200–      38 B. Li, S. Todo, A. C. Maggs, and W. Krauth, “Multithreaded
   209 (1986).                                                              event-chain Monte Carlo with local times,” Computer Physics
21 E. G. Gilbert, D. W. Johnson, and S. S. Keerthi, “A fast pro-
                                                                            Communications 261, 107702 (2021).
   cedure for computing the distance between complex objects in          39 S. Lee, E. G. Teich, M. Engel, and S. C. Glotzer, “Entropic col-
   three-dimensional space,” IEEE Journal on Robotics and Au-               loidal crystallization pathways via fluid?fluid transitions and mul-
   tomation 4, 193–203 (1988).                                              tidimensional prenucleation motifs,” Proceedings of the National
22 G. Snethen, “XenoCollide: Complex Collision Made Simple,” in
                                                                            Academy of Sciences 116, 14843–14851 (2019).
   Game Programming Gems 7, edited by S. Jacobs (Charles River           40 M. Michel, S. C. Kapfer, and W. Krauth, “Generalized Event-
   Media, 2008) pp. 165–178.                                                chain Monte Carlo: Constructing Rejection-free Global-balance
23 E. P. Bernard, W. Krauth, and D. B. Wilson, “Event-chain Monte
                                                                            Algorithms from Infinitesimal Steps,” Journal of Chemical
   Carlo Algorithms for Hard-sphere Systems,” Physical Review E             Physics 140, 054116 (2014).
   80, 056704 (2009).                                                    41 M. Engel, J. A. Anderson, S. C. Glotzer, M. Isobe, E. P.
24 T. A. Kampmann, H.-H. Boltz, and J. Kierfeld, “Parallelized
                                                                            Bernard, and W. Krauth, “Hard-disk Equation of State: First-
   Event Chain Algorithm for Dense Hard Sphere and Polymer Sys-             order Liquid-hexatic Transition in Two Dimensions with Three
   tems,” Journal of Computational Physics 281, 864–875 (2015).             Simulation Methods,” Physical Review E 87, 042134 (2013).
25 P. Jiménez, F. Thomas, and C. Torras, “3d Collision Detection:        42 M. Isobe and W. Krauth, “Hard-sphere Melting and Crystalliza-
   A Survey,” Computers & Graphics 25, 269–285 (2001).                      tion with Event-chain Monte Carlo,” Journal of Chemical Physics
26 T. Brochu, E. Edwards, and R. Bridson, “Efficient geometri-
                                                                            143, 084509 (2015).
   cally exact continuous collision detection,” ACM Transactions         43 J. R. Williams and R. O’Connor, “Discrete element simulation
   on Graphics 31, 1–7 (2012).                                              and the contact problem,” Archives of Computational Methods
27 J. Huang, J. Chen, W. Xu, and H. Bao, “A survey on fast sim-
                                                                            in Engineering 6, 279–304 (1999).
   ulation of elastic objects,” Frontiers of Computer Science 13,        44 M. de Berg, O. Cheong, M. van Kreveld, and M. Overmars,
   443–459 (2019).                                                          Computational Geometry: Algorithms and Applications, 3rd ed.
28 Y.-K. Choi, X. Li, F. Rong, W. Wang, and S. Cameron, “Deter-
                                                                            (Springer, 2008).
   mining the directional contact range of two convex polyhedra,”        45 J. Towns, T. Cockerill, M. Dahan, I. Foster, K. Gaither,
   Computer-Aided Design 42, 27–35 (2010).                                  A. Grimshaw, V. Hazlewood, S. Lathrop, D. Lifka, G. D. Pe-
                                                                            terson, R. Roskies, J. R. Scott, and N. Wilkins-Diehr, “Xsede:
                                                                            Accelerating scientific discovery,” Computing in Science & Engi-
                                                                            neering 16, 62–74 (2014).
