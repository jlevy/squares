                                                               The contact dynamics method for granular
arXiv:cond-mat/0211696v1 [cond-mat.soft] 29 Nov 2002




                                                                                media
                                                                                    Tamás Unger∗ and János Kertész∗
                                                          ∗
                                                              Department of Theoretical Physics, Budapest University of Technology and Economics, H-1111
                                                                                                  Budapest, Hungary

                                                         Abstract. In this paper we review the simulation method of the non-smooth contact dynamics. This
                                                         technique was designed to solve the unilateral and frictional contact problem for a large number of
                                                         rigid bodies and has proved to be especially valuable in research of dense granular materials during
                                                         the last decade. We present here the basic principles compared to other methods and the detailed
                                                         description of a 3D algorithm. We point out an artifact manifesting itself in spurious sound waves
                                                         and discuss the applicability of the method.



                                                                                             INTRODUCTION
                                                       Granular materials, due to their rich phenomenology and wide variety of applications
                                                       in technological processes, have captured much recent interest and are subject of active
                                                       research. Their study is often based on computer simulations, where, with growing im-
                                                       portance, discrete element methods play a fundamental role. Such numerical techniques,
                                                       e.g. the well known soft particle molecular dynamics [1, 2], the event driven method
                                                       [3, 2] or the here presented non-smooth contact dynamics [4, 5, 2, 6], have the common
                                                       property that the trajectory of each single particle is calculated by virtue of interaction
                                                       with other particles and with the environment. The characteristics of these algorithms
                                                       originate mainly from different treatments of interparticle interactions, which leads to
                                                       somewhat different applicabilities. E.g. the event driven method operates with instant
                                                       binary collisions and works very well in gas-like situations, however, if a dense state is
                                                       approached, where clusters of contacting grains would appear, then the simulation gets
                                                       critically slow, a phenomenon known as inelastic collapse[3].
                                                          The simulation of dense granular systems is always a computational challenge, in a
                                                       typical situation dry friction and many long lasting contacts between hard particles have
                                                       to be taken into account. Using molecular dynamics (MD) the velocities are modeled
                                                       as smooth functions of time (even for collisions), therefore the treatment of hard bodies
                                                       becomes problematic: here small time steps of the integration must be used resulting
                                                       in slow simulation. As we will see later, this problem of numerous hard particles is
                                                       difficult to solve even with other conceptions. In MD further difficulties are encountered
                                                       by dry friction, where it is not obvious how to distinguish between sliding and nonsliding
                                                       contacts.
                                                          The contact dynamics method (CD), developed by M. Jean and J. J. Moreau [4, 5, 6],
                                                       has a clear conception to overcome the above mentioned difficulties. The way is to
                                                       consider the particles as perfectly rigid and to handle the interaction by means of
the perfect volume exclusion, i.e. the contacting bodies may not deform each other.
For that an implicit algorithm is used, which has the significant advantage that the
implementation of dry friction is rather simple; the infinitely steep graph of Coulomb
friction can be adopted, thus no regularization is needed. The resulting method provides
realistic dynamics for various granular systems and is especially efficient for simulating
frictional multi-contact situations of hard bodies (for comparison with experiments and
with other methods see [7, 8, 9]).
   Although in recent years CD has been the simulation tool of many studies [10, 11,
12, 13] that provided understanding for several questions of granular media, it is rather
difficult to implement this algorithm relying merely on the literature. The reason, it
seems to us, is the lack of a practical description with hints how to adopt CD. One of the
goals of this paper is to help solving this problem: in the following section the basic ideas
and the structure of our 3D CD algorithm is presented. The description here is confined
mostly to cohesionless, rigid and spherical particles with perfectly inelastic collisions
(i.e. with zero Newton restitution), but it has to be emphasized that CD contains no
restriction on shape or on other of these conditions. We refer to simulations, where
cohesive disks and polygons were implemented [13, 14], or particles with finite Newton
restitution [8], even deformable bodies can be adopted in CD with a minor change of
variable [6].
   Finally we will discuss some consequences of the iterative solver used for the cal-
culation of the interparticle forces (see later) with respect to the computational time
and we will review a potential elastic behavior that may arise from inaccurate force-
determination.


                                 THE CD METHOD

                                 The basic principles
   As a discrete element method CD provides the dynamics by integrating the equations
of motion for each particle, where besides external fields (e.g. gravity) the interaction
between the particles are also taken into account. The particles are considered as per-
fectly rigid and interact with each other via point-contacts. The question is, how the
force at such a contact is calculated with CD. Because of the rigidity it cannot be given
as a function of the extent or rate of the contact-deformation, like in the case of the soft
particle MD. In fact, the principles of the two methods are basically different. In CD the
contact forces are calculated by virtue of their effect, namely the generated motion has
to fulfill certain constraints. Typically such a constraint is the volume exclusion of the
particles, or the absence of sliding due to static friction.
   Using constraint forces for the interaction has a serious consequence: a contact force
depends also on other forces that press the two contacting bodies together, e.g. on
adjacent contact forces. Thus for a compressed cluster of rigid particles the problem
cannot be solved locally for each contact. In the algorithm, in order to calculate a global
consistent system of constraint forces at every time step, an iterative scheme is needed
(called the iterative solver).
                                          Rn


                PSfrag repla ements

                                      0                    g

                                FIGURE 1.   The Signorini graph



   This iteration process of course demands computational effort, but in exchange it
makes possible to apply an implicit stepping algorithm with large time steps. The
resulting dynamics is non-smooth and includes velocity jumps due to shocks when
collisions occur. In contrast, the MD method considers the motion smooth even for
collision, therefore the harder the particles are, the finer resolution in time is needed,
consequently small time steps are used.



                               The constraint conditions
   The main feature of unilateral contacts we want to attain is impenetrability, further-
more only repulsive forces are allowed corresponding to dry granular materials. This is
expressed by the Signorini graph (Fig. 1), which relates the gap g between two particles
and the normal force Rn between them. Rn can be non-negative and arbitrarily large
if g = 0, but becomes zero if the two particles are not in contact (g > 0). In the algo-
rithm the normal force is determined according to this multi-mapping graph and to the
additional principle, that the smallest value of Rn is applied at a contact, which is just
needed to avoid interpenetration.
   Regarding the tangential force Rt it is due to the Coulomb friction (Fig. 2), which
captures the characteristics of dry frictional contacts that sliding cannot be induced
below a certain threshold. This threshold is proportional to the normal force with the
factor µ , the friction coefficient. (Here we neglect the difference between static and
sliding friction coefficients for simplicity, but this distinction can be made in CD without
difficulty.)
   In a non-sliding situation the value of Rt is not determined by the graph, the static
friction force can be arbitrary below the threshold. Here a similar constraint principle is
applied as for Rn , namely that the proper friction force is chosen, which is needed to
keep the contact from sliding. If this condition cannot be satisfied below the threshold,
then the contact will slide with a friction force µ Rn against the motion, i.e. pointing
opposite to the relative tangential velocity.
   The graph shown in Figure 2 concerns rather a two-dimensional case. In three-
dimension one can speak about the Coulomb cone: for a given Rn the friction force
                                                Rt
                                                Rn



           PSfrag repla ements                                   Vt
                                        Rn

                                 FIGURE 2.   The Coulomb graph



must lie in a two-dimensional plane within a circle, the radius of which is defined by the
threshold above, thus the radius depends linearly on the normal force.
   We would like to emphasize that both graphs presented here are infinitely steep and
can be implemented in the CD method without any change.


                         The discrete dynamical equations
   According to the Signorini condition, collisions of particles give rise to shocks,
therefore discontinuous velocities are expected during the time-evolution. In such a
case of non-smooth mechanics [15] the use of second or higher order schemes for the
integration of motion is not beneficial and could even be problematic. Therefore first
order schemes are applied, e.g. an implicit Euler integration in our CD code:

                          ~ri (t + ∆t) = ~ri (t) +~vi (t + ∆t) ∆t                        (1)
                                                    1
                          ~vi (t + ∆t) = ~vi (t) + ~Fi (t + ∆t) ∆t .                     (2)
                                                   mi
   The two equations describe the change in velocity and position of the center of mass
during one time step for the ith particle. The vector ~Fi denotes the sum of the forces
acting on this particle and is calculated to be consistent with the new velocities and
positions.
   The time-stepping is also similar for the rotation around the center of mass: the
orientation of a particle is updated with the new angular velocity ω  ~ i (t + ∆t), while for
the update of ω
              ~ i we use the torque ~Ti (t + ∆t) resulting from the new contact forces.


                                       One contact
  Let us first consider the simple case of only one candidate for contact, i.e. two convex
particles already in contact or with a small gap between them. They are numbered 0
                         0                                                   1
                               F~0ext                    F~1ext
   PSfrag repla ements
                                        ~l0
                                                         ~l1


                                                                  R~
                   FIGURE 3.     Two rigid particles before a possible contact state.



and 1 and may be subjected to constant external forces ~F0ext , ~F1ext acting on the centers
of mass (Fig. 3). The volume exclusion and the Coulomb friction law may require a
                 ~ at this contact-candidate (contact force for short), where we use the
constraint force R
convention that R~ acts on particle 1, while its reaction force −R ~ acts on the other one.
In this section we will show how R ~ is calculated with contact dynamics.
   An important quantity of a contact-candidate is its relative velocity:
                                                             
                           V~ =~v1 + ω
                                     ~ 1 ×~l1 − ~v0 + ω
                                                      ~ 0 ×~l0 ,                         (3)

where the vectors ~l0 and ~l1 point from the centers of mass to possible contact points.
  It is useful to introduce a generalized velocity vector:

                                                   ~v0
                                                   
                                                  ~ω0 
                                              V =  .                                     (4)
                                                   ~v1
                                                    ω
                                                    ~1

With the bold notation we indicate that V is not a three-dimensional vector but actually
has 12 real components. The form (3) shows a linear dependence of the contact velocity
V~ on V.
   In a similar way generalized forces can be defined:

                                     ~R             ~F
                                                 ext 
                                        0              0
                                   ~T  ext  ~0 
                              R=       0
                                   ~R  F = ~F ext  ,                             (5)
                                                        
                                        1              1
                                      ~T              ~0
                                        1

                                                                        ~
where R contains torques and central forces equivalent to the effect of R:

                    ~
              ~R = −R,              ~
                               ~R = R,                      ~
                                                 ~T = −~l × R,                     ~
                                                                         ~T = ~l × R,      (6)
                0                1                 0     0                 1    1

while Fext collects the external forces (the external torques are zero).
  Now the relation between the corresponding contact and central quantities can be
expressed with the following linear forms:

                                            ~
                                       R = HR                                            (7)
                                      V~ = HT V ,                                        (8)

where HT is the transpose of the matrix H. These two matrices depend only on the
geometry, their structures follow from Eq. (3) and Eq. (6):
                                                 
                                             −1
                                             
                                        ~
                                        − l0 × 
                                                  
                                   H=            ,                         (9)
                                       
                                          1   
                                            ~l ×
                                               1

                               h           i
                           HT = −1 ~l0 × 1 − ~l1 × .                                    (10)
                                                                 
The elements here are 3 × 3 matrices: 1 is the unit matrix and ~li × gives simply the
crossproduct of ~li and the vector it is acting on. The matrix H allows us to transform
contact quantities into particle quantities and vice versa.
  For the particles Newton’s equation of motion reads:
                                dV
                                   = M−1 R + M−1 Fext ,                                 (11)
                                dt
where M−1 is the inverse of the generalized mass matrix, which is built up from the
masses and moments of inertia matrices of the particles:

                                  m0 1       0  0       0
                                                          
                                  0         I0 0       0
                               M=                           .                          (12)
                                   0         0 m1 1     0
                                   0         0  0       I1

  If one transforms the Equation (11) multiplying it with HT from the left, the equation
of motion can be obtained regarding this candidate for contact (note that the term
dHT /dt V describing the geometrical change is neglected here, which is typically a good
approximation) :
                                  d V~       −1 ~    d V~ free
                                       =M R+                   ,                         (13)
                                   dt                   dt
where M is the effective mass matrix of the contact and it describes the contact-
acceleration due to the contact force. This is an important relation because, as we will
see, it gives the possibility to utilize our constraint conditions and therefore to calculate
                        ~
the interparticle force R.
  The second term of the right hand side in Eq. (13) has the meaning of the acceleration
without any interaction between the particles, i.e. only due to the external forces:

                                  d V~ free
                                            = HT M−1 Fext                              (14)
                                     dt



                 The properties of the effective mass matrix M
  The value of M −1 easily follows from the transformations (7) and (8):
                                   M −1 = HT M−1 H .                                   (15)
It can be shown that M −1 gets a really simple form for contacting spheres, because on
one hand the spherical moments of inertia simplify M −1 (i.e. I0 and I1 are numbers):
                                             !
                        1    1     ~l 2 ~l 2      1 ~ ~  1 ~ ~ 
             M −1 =       +     + 0 + 1 1−           l ◦l −         l ◦l           (16)
                       m0 m1 I0           I1      I0 0 0        I1 1 1

 (where ◦ is the dyadic product), on the other hand one can take into account the fact that
~l and ~l are on the same line, which is perpendicular to the contact surface. The result
  0      1
 is that M −1 can be characterized by two parameters mn and mt :

                                                1 −1
                                                 
                                          1
                             mn =           +                                         (17)
                                         m0 m1
                                                        !−1
                                          1 ~l02 ~l12
                             mt =           + +              ,                        (18)
                                         mn I0       I1

which could be called normal and tangential mass respectively, as they are the inertia of
this candidate in normal and tangential direction. More clearly if R ~ is given by the sum
of the normal and tangential component: Rn~n + R  ~ t (~n is a normal unit vector, while the
tangential component is a vector in the two-dimensional tangent plane), then M −1 acts
in the following way:
                              M −1 R~ = 1 Rn~n + 1 R      ~ .                           (19)
                                         mn          mt t
Thus the normal and tangential components are not coupled for spheres, which is not
true in general.


                                   The time stepping
  Turning back to the dynamics, our aim is to find a proper interaction force in accor-
dance with the discrete equations. Based on the implicit Euler scheme, the following
discrete form of the dynamical equations is obtained for the two-particle system:

                        Vnew − V = M−1 Rnew + M−1 Fext ∆t .
                                                           
                                                                                      (20)

The superscript “new” indicates the yet unknown values of parameters, i.e. the values
after the time step ∆t. Because the external forces are kept constant here, their change is
not involved in the equation. This implies the following approximate change in contact
velocity during one time step:
                                                              
                      V~ new  ~         −1 ~ new
                             −V = M R +H M F         T −1 ext
                                                                 ∆t ,                 (21)

where the unknown values are V~ new and R ~ new . The part of this velocity change due to
the external forces is known and can be subtracted from Eq. (21):

                                                 ~ new ∆t ,
                              V~ new − U~ = M −1 R                                    (22)

where
                                U~ = HT M−1 Fext ∆t + V~                              (23)
would be the new velocity without interaction.
   Similarly, positions are updated by means of new velocities (Eq. 1), which implies the
following predictive formula for the gap g (the distance between the two particles):

                                  gnew − g = Vnnew ∆t ,                               (24)

where Vnnew = ~nV~ new is the normal component of the contact velocity. The normal
vector ~n points from particle 0 towards particle 1, thus for approaching particles the
normal velocity is negative. Note, that negative g has the meaning of an overlap.
  Considering the Equations (22) and (24) the constraint conditions can be easily
imposed on the “new” situation, which is done in three steps in the algorithm:
  1. First we check what happens to the gap without interaction after ∆t and if it remains
     positive:
                                      g + Un ∆t > 0 ,                                 (25)
     then R~ new is set to zero. This means if the contact state is not reached no contact
     force is needed. If the left hand side of the inequality (25) is zero or negative, the
     algorithm jumps to the second point.
  2. As the two objects are considered perfectly rigid, a contact force is needed to
     hinder the interpenetration. This step is an attempt to have a sticking contact, i.e.
     we require on one hand that the gap closes:

                                          gnew = 0 ,                                  (26)

     on the other hand no slip occurs:

                                          V~t new = 0 ,                               (27)
     thus the unknown values can be determined. From Eq. (24) the new velocity is
     obtained V~ new = −(g/∆t)~n, then Eq. (22) reads:
                             1  h g     
                                               ~
                                                 i
                                                    ~ new ,
                            − M      + Un ~n + Ut = R                                    (28)
                             ∆t   ∆t
     which provides the contact force. However, this contact force can only be accepted
     if it satisfies the Coulomb condition:
                                           ~ t ≤ µ Rn .
                                           R                                             (29)

     If this inequality does not hold, the friction is not strong enough to ensure sticking.
     In this case the contact will be a slipping one and a new calculation is needed for
     R~ new , which is done in the third point.
  3. For a slipping contact the condition (26) remains valid, but (27) does not. Then the
     following equation must be solved:
                           1  h g     
                                             ~    ~
                                                    i
                                                       ~ new ,
                          − M      + Un ~n + Ut − Vt = R                                 (30)
                           ∆t   ∆t
     together with two further conditions corresponding to the sliding friction. Firstly

                   V~t and R
                           ~ t must be parallel and have opposite direction,             (31)

     secondly
                                           ~ t = µ Rn .
                                           R                                             (32)

   These three points form a shock law that in general provides the contact force at every
time step. It can be applied for colliding particles, but also for an old-established contact,
in that sense no distinction has to be made. If the treatment is restricted to spherical
particles, the shock law can be written in a more simple form, but before the summary
of this case is given, we would like to make two remarks.
   Firstly, this shock law corresponds to a completely inelastic collision, i.e. to zero value
of the normal restitution coefficient. To accomplish such a collision, two time steps are
needed: at the first time step the relative normal velocity is only reduced but it is not
set to zero, in order to let the gap close and at the following time step then the relative
velocity vanishes completely for the already established contact.
   Secondly, for practical applications a slight change is proposed in the shock law [6],
which is the use of
                                      gpos = max (g, 0)                                   (33)
instead of g in Equations (28) and (30). This, in principle, makes no difference because
g should be non-negative. However, due to inaccurate calculations some small overlaps
can be created between neighboring particles. These overlaps would be immediately
eliminated by the first version of the inelastic shock law by applying larger repulsive
force in order to satisfy the Equation (26). This self-correcting property, nonetheless, has
the non-negligible drawback that it pumps kinetic energy into the system, while pushing
the overlapping particles apart, which mechanism can destroy stable equilibrium states.
With the application of gpos one gets rid of the overlap correcting impulses in such a
way that the already existing overlaps are not eliminated, only the further growths are
inhibited. In that sense the resulting shock law is “more inelastic” than the original one.
  The inelastic shock law of the second type is given by the following very simple
scheme for spherical particles, which allows different masses and sizes for the contacting
spheres:

  if   Un ∆t + gpos > 0 
                           Rnnew := 0
                   then     ~ new                                  (no contact)
                          Rt := 0            pos       
                              new      1        g
                          Rn := − mn
                                                   + Un
                    else               ∆t        ∆t                (sticking contact)
                          R
                           ~ new := − 1 mt U~t                                         (34)
                              t
                                       ∆t
  if   ~
       Rtnew > µ Rn  new
                         
                                             ~ new
                           ~ new := µ R new Rt
                         
                   then   R                                        (sliding contact)
                          t           n
                                            R~ new
                                                  t

   Note, that in the third sliding case the recalculation of Rn is not necessary, because the
mass matrix M is diagonal, even the direction of the non-sliding friction force obtained
before can be accepted for the sliding contact, relying on the the Eq. (22).
   When situations in real experiments are numerically studied, it is a natural require-
ment that certain confining objects are involved in the simulation (e.g. container, fixed
wall, moving piston, rotating drum). Therefore the algorithm has to be able to handle
not only sphere-sphere contacts, but also sphere-plane and sphere-cylinder contacts. One
can easily verify that if planes and cylinders with infinite moments of inertia are used
(I1 = ∞), the same simple contact law can be applied as the one derived here for spheres.
(Only in the expression of mt (Eq. 18) the term ~l12 /I1 is set to zero.)


                                    Many contacts
   As we have pointed out, the unilateral frictional problems of contacts cannot be solved
independently in a dense granular system. The unknowns of one contact R    ~ new and V~ new
depend on adjacent “new” contact forces that are also unknown. In this way a contact
force is coupled to every other contact if they are connected through the contact network.
This is a natural consequence of the perfect rigidity, e.g. a collision can immediately
affect the forces even in a very far part of the system.
   In order to solve this global multi-contact problem, i.e. to satisfy the constraint
conditions for all contacts, an iterative method is applied in CD. This iterative solver
is executed at every time step before the implicit Euler integration can proceed one step
further with the newly provided forces.
   This method works as follows. At each iteration step we update every contact, inde-
pendently in the sense that for one contact-candidate a “new” contact force is calculated
based on a one-contact shock law, pretending that the current forces of the neighboring
contacts are constant. After that the resulting force is stored immediately as the current
force of the given contact and a new candidate is chosen for the next update. In that way
all the contact forces are updated one by one sequentially, which of course does not yet
provide a global solution, but approaches it to some extent. Then this iteration step is
repeated many times letting the forces relax according to their neighborhood towards a
globally consistent state. After satisfactory convergence is reached the iteration loop is
stopped. With convergence we mean that further update of the contact forces gives only
negligible changes, thus the constraint conditions are practically fulfilled for the whole
system.
   If the inelastic shock law is applied for the one-contact update, one must not forget
that the forces from the adjacent particles (acting now as external forces) exert also
torques ~T0ext and ~T1ext , that have to be involved by the generalized vector Fext in Eq. (5),
where the two torques originally were set to zero.
   In contrast to this sequential process a simple parallel update would be unstable.
Regarding the order of the update sequence within the list of the candidates, it is
preferably random and the random pattern is generated repeatedly for each sweep. In
this way we want to avoid any bias in the information spreading, what may be caused
e.g. by geometrical sweeps. (If the update order is from top to the bottom, the news
of a collision or other events pass faster through the contact network downwards than
upwards, at least in the early stage of the iteration process.) It has to be mentioned that
the random sweep described here differs from the well known random sequential update
because while in this latter the choice of a contact is independent from the previous
choices (the same contact could be selected even three times successively), the random
sweep selects each contact exactly once within one iteration step.
   In applications the iteration process of the contact dynamics has a nice behavior and
converges under reasonable assumptions. About the conditions of convergence more can
be found in [6] and references therein.


                                  Convergence criteria
   Convergence criteria [16] are applied in the iteration loop to decide, whether the force-
system has reached a satisfactory consistent state or further iterations are needed. That
is, a convergence criterion is a rule according to which one choses the the final number of
the iterations within one time step. Various criteria are used by different research groups,
but the structure or efficiency of these criteria is not much discussed in the literature.
   In the following a few possible choices are presented, where the first two examples
make conditions on the relative change of the forces. The notations used here are the
following: R ~ α is the force of the contact-candidate α in the current state of the iteration
process, ∆R ~ α is its change during the last iteration step and the brackets hi mean average
over all candidates.
  The first local criterion is:
                                     ~α ≤ ε R
                                    ∆R      ~α ,                                      (35)
which inequality is required for every α . Once it is satisfied everywhere, the iteration
loop stops. With the parameter ε the required accuracy can be given. With smaller ε
the calculation is more accurate, but the loop of the iteration is forced to run longer.
However, if this criterion is applied, an additional cutoff for small forces is needed
because small numerical fluctuations present in the simulation can be relatively large
for tiny contact forces (there are always such forces in large granular packings), and
therefore condition (35) cannot be fulfilled. One way to solve this is to add a certain
small force δ to the right hand side.
  The second example is of global type:
                                  D     E     D       E
                                ∆ Rα ≤ ε Rα .
                                      ~          ~                                   (36)

Here the change in the average force is tested, thus it means only one condition globally
for the whole system. The role of ε is the same as in the local case, but of course the
same value of ε provides different accuracies for the calculation of the force-system.
   We performed test runs [17] in order to compare the efficiency of the two criteria.
Here the extent of the errors and the average iteration over many time steps needed
by the simulation were measured, this latter representing the computational effort. In
most cases the exact solution to the forces was not available, so one cannot describe
the errors as differences between exact and approximate solutions. Here the level of
accuracy was simply characterized by the average overlap, what should be zero in an
ideal case. This non-extensive investigation provided the results that both criteria are
working well, but in many cases significant differences in the efficiency were found.
However, which criterion is more efficient depends on the specific situation and also on
the required level of accuracy.
   Finally we mention the example that a criterion can simply prescribe a fixed number
of iterations:
                                      NI = const,                                    (37)
i.e. at every time step the iteration loop stops after NI steps. The accuracy can be
improved here by applying larger NI number. This choice of the criterion behaves also
nicely in simulations and one of its advantages is simplicity, which makes the operations
of the program more transparent giving the possibility of a better understanding of the
method.


                                   Sources of errors
   When numerical simulations are performed, numerous simplifications and approxi-
mations are needed, which lead to dynamics somewhat different from that in a real sys-
tem. These can be e.g. the assumption of point-contacts or constraint conditions when
setting up a theoretical model of a real system, or other type of approximations due to the
numerical implementation of this theoretical model, e.g. a discrete integration scheme.
   Knowing about the trivial sources of deviations, one can formulate a reduced expec-
tation from the algorithm (as we did in this section): “We want to have a dynamics
based on the implicit Euler integration, where the contact forces satisfy the Signorini
and Coulomb conditions.”
   Is this requirement met by the here presented algorithm? In fact, the computation of
contact forces can lead to further errors. The first and main reason of this is that the
convergence of the iterative process is not perfect, the loop is necessarily broken after
finitely many steps. More about the consequences of this non-accurate force calculation
can be found in the next section. Additional errors can emerge even if the one-contact
shock law is satisfied everywhere in the system. This is because in the shock law some
geometrical changes are neglected when predicting the “new” configuration. E.g., for
approaching particles the contact normal can slightly turn or the vectors ~l0 , ~l1 can suffer
small changes, which would alter the matrix H. However, if the relative displacement
of the particles during one time step is small compared to the particle size and to the
curvature of the contacting surfaces, these geometrical changes are kept also small and
their effect can be typically neglected.


                       SPURIOUS ELASTIC BEHAVIOR
This section is devoted to the behavior of contact dynamics arising from the iterative
force computation and to its consequences. The study of the algorithm is carried out in a
manner commonly applied in physics: starting with the given microscopic laws (e.g. the
one-contact shock law here) properties of global behavior are examined. For a simple
test system a coarse grained description is given based on the discrete dynamics, where
physical phenomena such as diffusion or sound propagation will turn out to be relevant.


                         Relaxation of the contact forces
   In order to learn more about CD, one can analyze and test the algorithm using the
following very simple system [18]. The system consists of an array of identical rigid
disks or spheres aligned in a straight line (Fig. 4) and is considered one-dimensional, as
only the motion along the line is taken into account (spinning or transversal motion is
not allowed). The long chain of particles is compressed by external forces acting at the
ends, the inner part of the chain is free from external forces. The neighboring particles
are permanently in contact, i.e. gpos
                                   i
                                       = 0, where the ith contact is between the particles
i and i + 1. In this one-dimensional case the tangential forces are zero and the normal
contact forces are denoted by Ri . First we show how the iterative solver works for this
simple case.
   For the update of the contact forces the shock law (34) is applied. Provided the
particles remain in contact and no friction is considered, the update of the ith contact
attains the following form:
                                   m            R + Ri+1
                          Ri :=       vi − vi+1 + i−1     .                              (38)
                                  2∆t                 2
            PSfrag repla ements



                                  10
                                  010
                                    1 i     10
                                             1 i 00
                                             1 00
                                             0
                                                 11i + 1 0
                                                 11
                                                         1
                                                         1i + 2
                                                         0            0
                                                                      10
                                                                       10
                                                                        1
                                             R 1 R R +1
                                               i       i         i


FIGURE 4. A multi-contact situation in an 1D array. External forces act only on particles far away from
those shown. Each particle is subjected only to the contact forces of the adjacent ones.



Based on the current values of the adjacent velocities and forces, a new value of Ri is
given by this assignment which is applied several times on the contacts in the way we
described before for the multi-contact states. Here, the effective mass (the normal inertia
of the contacts) is half of the particle mass m.
   As we are searching for a continuum description, the shock formula (38) can be
regarded as the discretized form of a partial differential equation (PDE). In order to
make this transformation, on one hand, we consider the particle index i as space variable
x and replace the differences of consecutive quantities by spacial derivatives in the usual
way:
                                       vi+1 − vi
                                                 → ∂x v                                (39)
                                           d
and
                                Ri+1 + Ri−1 − 2Ri
                                                    → ∂x2 R ,                          (40)
                                         d2
where d is the particle diameter. On the other hand we introduce a fictitious time t ∗ for
the iteration process, to be able to describe the force evolution. (Note that the physical
time does not elapse while the iterations develop the forces.) Then the force change ∆R
during one iteration step ∆t ∗ can be replaced by a time derivative:
                                              ∆R
                                                   → ∂t ∗ R .                                     (41)
                                              ∆t ∗
   Thus, by applying these transformations straightforward to the assignment (38) one
arrives to the following PDE:

                                          ∂t ∗ R = D∂x2 R − β ∂x v                                (42)


                                                           d2
                                            with D = q          ,                                 (43)
                                                           ∆t ∗
                                                      md
                                              β =q          ,                                     (44)
                                                     ∆t∆t ∗
                                                           1
                                              and    q=      .                                    (45)
                                                           2
This analytic form clearly reveals the nature of the iteration loop: The contact forces
relax towards the solution in a diffusive way. (The term ∂x v being constant during the
iteration depends only on x but not on t ∗.)
   The introduction of the constant q reflects a subtlety regarding the sequential character
of the update which was not taken into account in the derivation of Eqs.(42,43,44,45). In
fact, q = 1/2 corresponds to a parallel update, but the right hand side of Eq.(38) always
employs the freshly updated values Ri , not those from the beginning of the iteration
sweep. However, it can be shown that a calculation based on the random sweep update
instead of a parallel one results in the same form of the PDE, only the value of q is
renormalized:                              √
                                         4 e−5
                                   q=             ≈ 0.797                               (46)
                                             2
(for the derivation see [18]).
   The diffusion like relaxation of the forces has an important consequence concerning
the number of iterations NI which is also crucial for the efficiency of the algorithm,
as the computational time is mainly expended to the iterative force calculation. Due to
the diffusive behavior a long iteration process can be expected e.g. when an external
force changes or a collision occurs at one end of the array. One can estimate the number
of iterations required to reach an “equilibrium” state (convergence) for the forces in the
whole system, where the estimation is based on the relation of two characteristic lengths:
the diffusion length related to NI steps

                                     ldiff = 4 D ∆t ∗NI
                                             p
                                                                                        (47)

must be much larger than the system size L. This implies the following estimation (q is
being of order 1)
                                   NI > (L/d)2 ,                                  (48)
that is NI scales with the square of the linear system size.
   One can expect similar diffusive relaxation in dense two and three-dimensional sys-
tems, where the diffusion takes place in a complex
                                              p         contact network instead of a line,
still the diffusion length is proportional to NI in typical homogen situations. Let us
estimate the total number of the contact updates during the force calculation, which rep-
resents the computational effort of one timestep TCDstep , where the question is the scaling
with respect to the number of particles n. Within one sweep one update is performed for
each contact, which implies an update number proportional to n (assuming the average
coordination number does not change with n). Therefore the computational time of one
time step is given by nNI apart from a constant factor which results in the following
scaling with the particle number:

                                   TCDstep ∼ n2    in 2D                               (49)


                                  TCDstep ∼ n5/3   in 3D                               (50)
(as long as L2 ∼ n in 2D and L3 ∼ n in 3D). For comparison in soft particle MD the
computational time of one time step scales like n. Thus applying the CD method in that
                                                  F




FIGURE 5. Setup of a numerical experiment in two dimensions. A dense packing of 1000 disks is
prepared in a container via compressing the system by means of the mobile upper wall.



way, it is computationally more costly for large systems. This is the price for simulating
rigid particles without getting elasticity artifacts, which cannot be done with MD.
   It is possible to achieve linear scaling with CD reducing the accuracy of the force
computation, however, that involves finite stiffness of the particles. As an example let
us imagine a CD simulation of a two dimensional dense granular packing, like the one
shown in Fig. 5, compressed in a container with an external force acting upon the mobile
upper piston. Let us suppose that the system is in equilibrium when the piston force is
increased abruptly with ∆F. At the given time step the CD algorithm starts the iterative
solver to find the new force system. What happens if one stops the iteration loop before
the convergence and performs the time step with the inaccurate forces? The momentum
∆F∆t is transmitted from the piston through the contact forces but only into a depth
given by the diffusion length. If NI was chosen in a way that the corresponding diffusion
length is smaller than the system height, than this momentum doesn’t reach the fixed
base and consequently the upper part of the system is accelerated downwards even if
it violates the volume exclusion of the particles. We will show (based on [18]) that the
resulting artificial dynamics can be interpreted as the dynamics of soft particles.


                                      Sound waves
   Coming back to the one dimensional system, the discrete time-evolution of the ve-
locities can also be transformed into a PDE in a similar manner as it was done for the
iteration loop. The Euler scheme (2) gives the following update formula:

                                             Ri−1 (t + ∆t) − Ri (t + ∆t)
                   vi (t + ∆t) := vi (t) +                               ∆t ,           (51)
                                                         m
and changing the differences into derivatives the continuum version is:
                                              d
                                      ∂t v = − ∂x R .                                   (52)
                                              m
This equation describes the time-evolution of the velocities on large time and length
scales. To connect it to the force update we must relate the “iteration time” t ∗ to the
physical time t. Although, depending on the convergence criterion, there can be in
principle a varying number of iterations during one physical time step ∆t, we assume
for simplicity that the simple criterion (37) is applied, i.e. the number NI is fixed.
   Hence, with ∆t = NI ∆t ∗, we can express the above quantities in terms of physical
time:
                                  ∂t R = D∂x2 R − β ∂x v ,                             (53)

                                                       d2
                                    and D = qNI                                       (54)
                                                       ∆t
                                               md
                                      β = qNI       .                          (55)
                                               ∆t 2
With the equations (52) and (53) we obtained two coupled PDEs. We can combine them
to arrive at a wave equation with an additional damping term:

                             ∂t2 R = c2 ∂x2 R + ∂t D∂x2 R .
                                                         
                                                                               (56)

The sound velocity appearing is of finite value
                                           p         d
                                     c=        qNI      .                             (57)
                                                     ∆t
   The equation (56) indicates that the CD simulation of the particle chain can lead to
sound propagation like in an elastic medium, though the one-contact force update as-
sumes perfectly rigid and completely inelastic contacts. This deviation from the original
hard particle model, as it was mentioned before, originates from the incomplete relax-
ation of the forces. As a consequence, small NI yields systematic errors in the force
calculation and involves soft particles in the sense that the particles can overlap, fur-
thermore, the time evolutionpof these overlaps corresponds to elastic waves. The sound
velocity is proportional to NI , which goes to infinity in the limit of infinite NI , as it
should for rigid particles.
  Searching for the dispersion relation one can perform a Fourier transformation on
Eq. (56) and obtain the properties of the different wave modes. The oscillation frequency
ω of the wave number k is
                                            r
                                                    D2 k 2
                                 ω (k) = k c2 −            .                         (58)
                                                     4
That means, ω (k) becomes zero at a critical wave number
                                           2c   1
                                    kc =      ∼p ,                                    (59)
                                           D     NI

and waves with k larger than kc (short wave lengths) are over-damped. The damping
time τ (k) for the oscillating modes is given by:
                                                 2
                                      τ (k) =       .                                 (60)
                                                Dk2
                                                                                    ext
                                                                                F
                                                    11
                                                    000
                                                      10
                                                       1
                   d

FIGURE 6.    Initial configuration of a numerical experiment for testing properties of artificial sound
waves.


  We derived the dispersion relation (58) in the continuum limit which is a good
approximation for small wave numbers, but not close to the border of the Brillouin zone
(kBr = 2π /d), where the effect of the spatial discreteness cannot be neglected. However,
increasing the number of the iterations sufficiently, kc becomes small compared to kBr .
Actually, for NI ≥ 10 the formula (58) works well not only for small wave numbers but
for all oscillating modes, as can be verified numerically.
  Related to the sound velocity and the dispersion relation one can define the following
characteristic lengths:
                                       lsound = c ∆t                                (61)
is the distance the sound can travel during one time step and
                                                    2π
                                             λc =                                                (62)
                                                    kc
is the wave length of the largest overdamped mode. If lsound and λc are chosen much
larger than the system length L (with proper choice of NI ), the elasticity artifacts are
avoided. This is the same length-scale as defined by the diffusion length:
                                             √
                                      ldiff = 4 D ∆t ,                                  (63)
                                                                   p 
since all three lengths are of the same order of magnitude: O d qNI . If the system is
too large compared to NI in the sense that L > ldiff (NI ) the simulation involves artificial
elasticity.


                                Numerical confirmation

                                        1D simulation
   In order to confirm the results of the coarse grained description, we performed the
following numerical experiment: The starting configuration of the simulation consists
of an array of 50 disks and an immobile wall, the geometry can be seen in Fig. 6.
Initially the gap between the wall and the leftmost particle is one disk diameter (d),
the gap between the particles is zero and the array has zero velocity. Starting from t = 0
a constant external force (F ext ) is applied on the rightmost particle which accelerates the
array towards the wall (only horizontal motions are present). As simulation parameters
we chose NI = 40 and F ext = 0.05 dm∆t −2.
                                  49.38




                       x(t) / d
                                  49.37




                                  49.36

                                      300   350    400   450    500   550   600   650
                                                           t / ∆t
FIGURE 7. Damped oscillation in a Contact Dynamics simulation. The dots indicate the measured data:
the position of the rightmost particle versus time (for details see the text). The line is an exponentially
damped sine function, where the frequency and the damping time is provided by the continuum model.



   The collision with the wall induces a relative motion of the grains and generates sound
waves in the array. After a transient period the grains remain permanently in contact (the
whole array is pressed against the wall by F ext ). Since the different wave modes have
different relaxation time, after a while only the largest wave length mode survives. This
wave length is four times the system size because the wall represents a fixed boundary
while the right side is free. Since the wave length is given the oscillating frequency and
the damping time can be calculated from Eq. (58) and Eq. (60). For comparison with the
simulation we measured the motion of the rightmost particle. The expected motion is a
damped oscillation

                                    x(t) = x0 + A exp (−t/τ ) sin (ω t + φ ) ,                       (64)

where the parameters x0 , A and φ are the offset, the amplitude and the phase shift
respectively. The Figure 7 shows the measured data (dots) and the fitted curve (64)
using the calculated values of ω and τ . It shows that the simulation agrees with the
coarse grained description very well.


                                                  2D simulation
   After the analysis of the regular 1D system the important question arises whether
its behavior is relevant for higher dimensions and for less regular systems. In CD
simulations of two-dimensional random packings of disks the same “elastic” waves can
be observed (even transversal modes were found).
   The simulation presented here corresponds to the thought-experiment of the two-
dimensional random dense packing we discussed before Fig. 5. It consists of 1000 disks
with radii distributed uniformly between rmin and rmax = 2rmin , the mass of each disk
being proportional to its area. The base and the two side-walls are fixed while the upper
                                      2

                                      1




                    ∆y / rmin [10 ]
                    -6
                                      0

                                      -1

                                      -2

                                      -3

                                       200   300     400         500   600
                                                     t / ∆t
FIGURE 8. Oscillations in a 2D simulation are similar to the 1D case. Here the sound waves are
generated in a random dense packing of disks. The dots are the measured position of the upper wall
versus time (see Fig. 5), while the curve is a fitted exponentially damped sine function.



piston is mobile. Starting from a loose state, we compressed the system and waited until
the packing reached an equilibrium state (the compression force F applied on the piston
was kept constant). The simulation was carried out without gravity and with a Coulomb
friction coefficient of 0.05 for all the disk-disk and disk-wall contacts.
   After the packing was relaxed completely, we generated sound waves by increasing
the compression force abruptly to F + ∆F. After a transient period only one standing
wave mode survives (both the wavenumber vector and the collective motion are verti-
cal), where the piston, representing a free boundary, oscillates with a relatively large
amplitude. We measured the vertical position of the piston versus time and found that
the data can be fitted by an exponentially damped sine function (Fig. 8). Here, in con-
trast to the 1D case, also ω and τ are fit parameters, since, due to the different geometry,
the values (58) and (60) cannot be adopted. As the system has random structure, a more
complex treatment is required for a quantitative description. However, we checked the
most important relation, namely that the  pscaling properties of ω and τ remain valid also
for the 2D random system, that is ω ∼ NI and τ ∼ NI−1 , which means that the artificial
visco-elasticity of the particles depends on the number of iterations in the same manner
as we showed for the 1D chain.


                                             Global elasticity
  It is instructive to compare our test-system to its simplest MD counterpart where the
contact forces depend linearly on the local kinematic variables, i.e. the so called linear
spring/dashpot model
                         Ri = −κ xi+1 − xi − d − γ vi+1 − vi
                                                               
                                                                                      (65)
with the spring stiffness κ and the damping coefficient γ . Searching again for the large
scale behavior of the particle chain one arrives to the same PDE as in Eq. (53) with its
coefficients being inherited from Eq. (65):

                                          γ d2 2
                                 ∂t R =       ∂ R − κ d ∂x v                             (66)
                                           m x
This allows us to relate the physical MD model parameters to the “technical” CD
parameters (NI and ∆t):
                                                   NI
                                          κ = qm                                         (67)
                                                   ∆t 2
and
                                                   NI
                                          γ = qm                                         (68)
                                                   ∆t
This equivalence shows that on large scales the CD chain should behave identical to
its MD counterpart, e.g. it will indeed exhibit a global shrinkage proportional to an
external compressive load. Note that a real congruence can be expected only for the
collective behavior but not on the level of contacts. In the CD method, as explained
above, contact forces are not related to the overlaps. Overlaps are present merely due to
the incompleteness of the force-calculation and in fact are stochastic quantities because
of our random update procedure. Only on scales larger than the grain size, where the
fluctuations of these local “deformations” are averaged out, the behavior can be smooth
as in an elastic medium (shown e.g. in Fig. 7).
   Performing simulations within the scope of the spurious elasticity (i.e. ldiff < L) Equa-
tions (67) and (68) provide the effective stiffness and viscous dissipation of contacts.
One can see that the stiffness depends on NI , but not on the total number of particles n.
Therefore the choice of a constant NI independently from n provides the same stiffness,
no matter how large the system is. Using the CD in that way, the superlinear scaling of
the computational time in Eq. (49) and Eq. (50) can be avoided. Thus

                                        TCDstep ∼ n ,                                    (69)

similarly to MD. In this case, of course, elasticity artifacts (sound waves, elastic defor-
mations) are involved by the dynamics.
   Interestingly, the reduction of NI and ∆t while NI /∆t is kept constant increases the
stiffness, but does not affect the value of the dissipation γ or the total number of updates
corresponding to a given physical time interval. Hence, it seems to be worth reducing NI
and ∆t in that way (at least to some degree) if the goal is to simulate harder particles.
   The results concerning the iteration process made it possible to characterize CD
simulations by means of the diffusion length. One can draw a distinction between two
different types of behavior: spurious soft region for small values of ldiff , and rigid region
for large values of ldiff , where the transition can be found around the linear system size.
We would like to emphasize, however, that only dense systems were considered so far,
such states where roughly the whole system is one large cluster of contacting particles.
In loose situations, where mainly free particles or small separate clusters are present, the
system size is not relevant. Here, in order to avoid the soft region, one has to compare
ldiff to the size of the largest cluster.
   The description of the test system was based on the assumption of a constant number
of iterations for every time step, and due to this premise the analytical treatment became
simple and directly comparable to the corresponding simulation. It is important, though,
that applications of other convergence criteria typically involve fluctuating NI (i.e. it can
vary from time step to time step), and therefore steps with different “stiffness” are mixed
during the integration of motion. Consequently, the behavior of the CD method can be
more complex in detail, but qualitatively the results of constant NI remain relevant also
here. For example, the mechanism resulting in soft particles is the same, or shock-waves
with finite velocity can also arise in the case of fluctuating NI in a similar way.


                                          SUMMARY
We presented a 3D contact dynamics algorithm in detail to simulate large systems of
rigid spherical particles and gave a review of the iterative force calculation, where the
perfect volume exclusion and the exact Coulomb’s law of dry friction are adopted. We
showed that the systematic errors can lead to a spurious collective elastic behavior and
reproduced the numerical results analytically for a simple test system.
   Besides elucidating the origin of elastic behavior, the coarse grained description re-
vealed important characteristics of the CD method. It was shown that using the iterative
solver the contact forces are approached in a diffusion like manner, which is a crucial in-
formation concerning the computational time, when simulating rigid particles properly.
   When lowering the accuracy of the force calculation, CD simulation involves soft
particles. In that way Coulombian friction can be combined with global elasticity easily
and considerable computational time can be saved: even better performance than MD
can be achieved.


                                ACKNOWLEDGMENTS
The authors thank G. Bartels, L. Brendel, D. Kadau and D. E. Wolf for valuable discus-
sions. Thanks are due to APS for kind permission of reproducing figures. This work was
supported by OTKA T029985, T035028.


                                       REFERENCES
1.   Cundall, P. A., and Strack, O. D. L., Géotechnique, 29, 47–65 (1979).
2.   Wolf, D. E., “Modeling and Computer Simulation of Granular Media,” in Computational Physics,
     edited by K. H. Hoffmann and M. Schreiber, Springer, Berlin, 1996.
3.   McNamara, S., and Young, W. R., Phys. Rev. E, 50, R28–R31 (1994).
4.   Jean, M., and Moreau, J. J., “Unilaterality and dry friction in the dynamics of rigid body collec-
     tions,” in Proceedings of Contact Mechanics International Symposium, Presses Polytechniques et
     Universitaires Romandes, Lausanne, Switzerland, 1992, pp. 31–48.
5.    Moreau, J. J., Eur. J. Mech. A-Solids, 13, 93–114 (1994).
6.    Jean, M., Comput. Methods Appl. Mech. Engrg., 177, 235–257 (1999).
7.    Daudon, D., Lanier, J., and Jean, M., “A micro mechanical comparison between experimental results
      and numerical simulation of a biaxial test on 2D granular material,” in Powders & Grains 97,
      Balkema, Rotterdam, 1997, p. 219.
8.    Radjai, F., Roux, S., and Moreau, J., Chaos, 9, 544–550 (1999).
9.    Nouguier-Lehon, C., Dubujet, P., and Cambou, B., Analysis of granular material behaviour from two
      kinds of numerical modelling (2002), 15ht ASCE Engineering Mechanics Conference.
10.   Radjai, F., Jean, M., Moreau, J., and Roux, S., Phys. Rev. Lett., 77, 274–277 (1996).
11.   Radjai, F., Wolf, D., Jean, M., and Moreau, J., Phys. Rev. Lett., 80, 61–64 (1998).
12.   Staron, L., Vilotte, J., and Radjai, F., Phys. Rev. Lett., 89, 204302–204305 (2002).
13.   Kadau, D., Bartels, G., Brendel, L., and Wolf, D., Pore stabilization in cohesive granular systems
      (2002), cond-mat/0206572, submitted to Phase Transitions.
14.   Kadau, D., Bartels, G., Brendel, L., and Wolf, D. E., Comp. Phys. Comm., 147, 190–193 (2002).
15.   Moreau, J., and Panagiotopoulos, P., Nonsmooth Mechanics and Applications, Springer, Vienna,
      1988.
16.   Bartels, G., Die Kontakt-Dynamik Methode, Master’s thesis, Gerhard Mercator University, Duisburg,
      Germany (2001).
17.   Bartels, G., Unger, T., and Wolf, D., Comperison of convergence criteria in contact dynamics
      simulations (2001), unpublished.
18.   Unger, T., Brendel, L., Wolf, D. E., and Kertész, J., Phys. Rev. E, 65, 061305 (2002).
