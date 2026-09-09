                                         Computational Particle Mechanics manuscript No.
                                         (will be inserted by the editor)




                                         Ultrascale Simulations of Non-smooth Granular Dynamics
                                         Tobias Preclik · Ulrich Rüde
arXiv:1501.05810v1 [cs.CE] 23 Jan 2015




                                         Received: 31.12.2014 / Accepted:


                                         Abstract This article presents new algorithms for mas-      1 Introduction
                                         sively parallel granular dynamics simulations on dis-
                                         tributed memory architectures using a domain parti-
                                                                                                     Granular matter exhibits intriguing behaviours akin to
                                         tioning approach. Collisions are modelled with hard
                                                                                                     solids, liquids or gases. However, in contrast to those
                                         contacts in order to hide their micro-dynamics and thus
                                                                                                     fundamental states of matter, granular matter still can-
                                         to extend the time and length scales that can be simu-
                                                                                                     not be described by a unified model equation homoge-
                                         lated. The multi-contact problem is solved using a non-
                                                                                                     nizing the dynamics of the individual particles [26]. To
                                         linear block Gauss-Seidel method that is conforming to
                                                                                                     date, the rich set of phenomena observed in granular
                                         the subdomain structure. The parallel algorithms em-
                                                                                                     matter, can only be reproduced with simulations that
                                         ploy a sophisticated protocol between processors that
                                                                                                     resolve every individual particle. In this paper, we will
                                         delegate algorithmic tasks such as contact treatment
                                                                                                     consider methods where also the spatial extent and ge-
                                         and position integration uniquely and robustly to the
                                                                                                     ometric shape of the particles can be modelled. Thus
                                         processors. Communication overhead is minimized through
                                                                                                     in addition to position and translational velocity the
                                         aggressive message aggregation, leading to excellent strong
                                                                                                     orientation and angular velocity of each particle consti-
                                         and weak scaling. The robustness and scalability is as-
                                                                                                     tute the state variables of the dynamical system. The
                                         sessed on three clusters including two peta-scale super-
                                                                                                     shapes of the particles can be described for example
                                         computers with up to 458 752 processor cores. The sim-
                                                                                                     by geometric primitives, such as spheres or cylinders,
                                         ulations can reach unprecedented resolution of up to ten
                                                    10                                               with a low-dimensional parameterization. Composite
                                         billion (10 ) non-spherical particles and contacts.
                                                                                                     objects can be introduced as a set of primitives that
                                                                                                     are rigidly glued together.Eventually, even meshes with
                                         Keywords Granular Dynamics · High Performance
                                                                                                     a higher-dimensional parameterization can be used. In
                                         Computing · Non-smooth Contact · Parallel Com-
                                                                                                     this article the shape of the particles does not change
                                         puting · Message Passing Interface
                                                                                                     in time, i.e. no agglomeration, fracture or deformation
                                                                                                     takes place. The rates of change of the state variables
                                         Mathematics Subject Classification (2000) 65Y05 · are described by the Newton-Euler equations, and the
                                         70F35 · 70F40 · 70E55                                       particle interactions are determined by contact models.

                                         T. Preclik                                                        Two fundamentally different model types must be
                                         Lehrstuhl für Informatik 10 (Systemsimulation), Friedrich-   distinguished: Soft and hard contacts. Soft contacts al-
                                         Alexander-Universität Erlangen-Nürnberg, Cauerstr. 11,      low a local compliance in the contact region, whereas
                                         91052 Erlangen, Germany
                                         E-mail: tobias.preclik@fau.de
                                                                                                       hard contacts forbid penetrations. In the former class
                                                                                                       the contact forces can be discontinuous in time, lead-
                                         U. Rüde
                                         Lehrstuhl für Informatik 10 (Systemsimulation), Friedrich-
                                                                                                       ing to non-differentiable but continuous velocities after
                                         Alexander-Universität Erlangen-Nürnberg, Cauerstr. 11,      integration. The differential system can be cast e.g. as
                                         91052 Erlangen, Germany                                       an ordinary differential equation with a discontinuous
                                         E-mail: ulrich.ruede@fau.de                                   right-hand side or as differential inclusions. However,
2                                                                                             Tobias Preclik, Ulrich Rüde


the resulting differential system is typically extremely        computational power to integrate such systems for a
stiff if realistic material parameters are employed.            relevant simulation time. Consequently a massive par-
     In the latter class, discontinuous forces are not suffi-   allelization of the numerical method for architectures
cient to accomplish non-penetration of the particles. In-       with distributed memory is absolutely essential.
stead, impulses are necessary to instantaneously change
velocities on collisions or in self-locking configurations
if Coulomb friction is present [33]. Stronger mathemat-              In the last half decade several approaches were pub-
ical concepts are required to describe the dynamics. For        lished suggesting parallelizations of the methods inte-
that purpose, Moreau introduced the measure differen-           grating the equations of motion of rigid particles in hard
tial inclusions in [27].                                        contact [38, 39, 20, 34, 15, 16, 28]. The approach put for-
     Hard contacts are an idealization of reality. The          ward in this article builds conceptually on these previ-
rigidity of contacts has the advantage that the dynam-          ous approaches but exceeds them substantially by con-
ics of the micro-collisions does not have to be resolved        sistently parallelizing all parts of the code, consistently
in time. However, this also introduces ambiguities: The         distributing all simulation data (including the descrip-
rigidity has the effect that the force chains along which       tion of the domain partitioning), systematically mini-
a particle is supported are no longer unique [29]. If en-       mizing the volume of communication and the number
ergy is dissipated, this also effects the dynamics. To          of exchanged messages, and relying exclusively on ef-
integrate measure differential inclusions numerically in        ficient nearest-neighbor communication. The approach
time, two options exist: In the first approach the inte-        described here additionally spares the expensive assem-
gration is performed in subintervals from one impulsive         bly of system matrices by employing matrix-free com-
event to the next [25, 11]. At each event an instan-            putations. All this is accomplished without sacrificing
taneous impact problem must be solved whose solu-               accuracy. The matrix-freeness allows the direct and straight
tion serves as initial condition of the subsequent inte-        forward evaluation of wrenches in parallel and thus re-
gration subinterval. Impact problems can range from             duces the amount of communicated data. Furthermore,
simple binary collisions, to self-locking configurations,       an exceptionally robust synchronization protocol is de-
to complicated instantaneous frictional multi-contact           fined, which is not susceptible to numerical errors. The
problems with simultaneous impacts. The dynamics be-            excellent parallel scaling behaviour is then demonstrated
tween events are described by differential inclusions,          for dilute and dense test problems in strong- and weak-
differential algebraic equations or ordinary differential       scaling experiments on three clusters with fundamen-
equations. Predicting the times of the upcoming events          tally different interconnect networks. Among the test
correctly is non-trivial in general and handling them in        machines are the peta-scale supercomputers SuperMUC
order in parallel is impeding the scalability [25]. In the      and Juqueen. The results show that given a sufficient
second approach no efforts are made to detect events,           computational intensity of the granular setup and an
but the contact conditions are only required to be sat-         adequate interconnect, few hundred particles per pro-
isfied at discrete points in time. This approach is com-        cess are enough to obtain satisfactory scaling even on
monly referred to as a time-stepping method.                    millions of processes.
     This article focuses on the treatment of hard con-
tacts in order to avoid the temporal resolution of micro-
collisions and thus the dependence of the time-step length          In Sect. 2 of this paper the underlying differential
on the stiffness of the contacts. In order to avoid the res-    equations and the time-continuous formulation of the
olution of events a time-stepping method is employed.           hard contact models are formulated. Sect. 3 proposes
This considerably pushes the time scales accessible to          a discretization scheme and discrete constraints for the
granular flow simulations for stiff contacts.                   hard contact model. The problem of reducing the num-
     To estimate the order of a typical real-life problem       ber of contacts in the system for efficiency reasons is
size of a granular system, consider an excavator bucket         addressed in Sect. 4. Subsequently, an improved nu-
with a capacity of 1 m3 . Assuming sand grains with             merical method for solving multi-contact problems in
a diameter of 0.15 mm, and assuming that they are               parallel is introduced in Sect. 5 before turning to the
packed with a solid volume fraction of 0.6, the exca-           design of the parallelization in Sect. 6. The scalability
vator bucket contains in the order of 1010 particles. In        of the parallelization is then demonstrated in Sect. 7 by
such a dense packing the number of contacts is in the           means of dilute and dense setups on three different clus-
same order as the number of particles. Only large scale         ters. Finally, the algorithms and results are compared
parallel systems with distributed memory can provide            to previous work by other authors in Sect. 8 before sum-
enough memory to store the data and provide sufficient          marizing in Sect. 9.
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                                              3


2 Continuous Dynamical System                                  and time t. The wrench contributions from contact re-
                                                               actions are summed up with external forces fext and
The Newton-Euler equations for a system with νb par-           torques τext such as fictitious forces from non-inertial
ticles are [22]                                                reference frames.
                                                               Let λj (t) ∈ R3 be the contact reaction of a con-
             ẋ(t)        v(t)
                    =                 ,                        tact j ∈ C, where C = {1 . . νc } is the set of poten-
             ϕ̇(t)    Q(ϕ(t))ω(t)
                                                           tial contact indices. Let (j1 , j2 ) ∈ B2 be the index pair
             v̇(t)                f(s(t), t)                   of both particles involved in the contact j, where B =
M(ϕ(t))             =                                  ,
             ω̇(t)    τ(s(t), t) − ω(t) × I(ϕ(t))ω(t)          {1 . . νb } is the set of body indices. Let x̂j (x(t), ϕ(t)) ∈
where the positions x(t) ∈ R3νb , the rotations ϕ(t) ∈         R3 be the location of contact j, then the wrench on
R4νb , translational velocities v(t) ∈ R3νb , and angular      body i is
velocities ω(t) ∈ R3νb are the state variables at time t.      
                                                                fi (s(t), t)
                                                                               
                                                                                  fi,ext (s(t), t)
                                                                                                    X
                                                                                                                     1
                                                                                                                                   
                                                                               =                    +                                λ (t)
    Different parameterizations exist for the rotations,         τi (s(t), t)     τi,ext (s(t), t)     (x̂j (x(t), ϕ(t)) − xi (t))× j
                                                                                                    j∈C
                                                                                                    j1 =i
but quaternions having four real components are the                                                 X                    1
                                                                                                                                        
                                                                                                                                                   (1)
                                                                                                −                                         λ (t),
parameterization of choice here. Independent of the pa-                                             j∈C
                                                                                                            (x̂j (x(t), ϕ(t)) − xi (t))× j
                                                                                                    j2 =i
rameterization, the derivatives of the rotation compo-                                          |                       {z                    }
                                                                                                                wrench contributions
nents can be expressed in terms of a matrix-vector prod-
uct between a block-diagonal matrix and the angular                           ×
                                                               where ( · ) is a matrix, which when multiplied to a
velocities [10]. If the rotation of particle i is described    vector corresponds to the cross product between its
by the quaternion qw + qx i + qy j + qz k ∈ H then, ac-        operand ( · ) and the vector.
cording to [10], the i-th diagonal block of Q(ϕ(t)) is              In contrast to soft contact models, the contact re-
                 
                   −qx −qy −qz
                                                              actions in hard contact models cannot be explicitly ex-
               1  qw qz −qy                                  pressed as a function of the state variables but are de-
Qii (ϕi (t)) =                  .                            fined implicitly, e.g. by implicit non-linear functions [21],
               2  −qz qw qx 
                     qy −qx qw                                 complementarity constraints [1, 3], or inclusions [36].
                                                               In any case, the constraints distinguish between reac-
    Each particle has an associated body frame whose           tions in the directions normal to the contact surfaces
origin coincides with the body’s center of mass and            and reactions in the tangential planes of the contact
whose axes are initially aligned with the axes of the ob-      surfaces. The former are used to formulate the non-
servational frame. The body frame is rigidly attached          penetration constraints, and the latter are used to for-
to the body and translates and rotates with it. All of         mulate the friction constraints. For that reason, each
the state variables and other quantities are expressed         contact j is associated with a contact frame, where
in the observational frame unless noted otherwise. Fur-        the axis nj (x(t), ϕ(t)) ∈ R3 points along the direc-
thermore, the matrix                                           tion normal to the contact surface, and the other two
            
               diag mi 1
                                                              axes tj (x(t), ϕ(t)) ∈ R3 and oj (x(t), ϕ(t)) ∈ R3 span
                                                               the tangential plane of the contact.
M(ϕ(t)) = i=1..νb                         
                          diag Iii (ϕi (t))                         Let Si be the set of points in the observational frame
                          i=1..νb
                                                               defining the shape of particle i, and let fi (xi (t), ϕi (t), y) ∈
is the block-diagonal mass matrix, where 1 denotes the         R be the associated signed distance function for a point
3 × 3 identity matrix. The mass matrix contains the            y in the observational frame. The signed distance func-
constant particle masses mi and the particles’ inertia         tion shall be negative in the interior of Si . Assum-
matrices Iii (ϕi (t)) about the particles’ centers of mass.    ing that all particles are (strictly) convex with suffi-
The latter can be calculated by similarity transforma-         ciently smooth boundaries, then for a pair of particles
tions from the constant body frame inertia matrices I0ii .     (j1 , j2 ) involved in a contact j, the contact location
If the body frames are attached such that they coincide        x̂j (x(t), ϕ(t)) is defined by the optimization problem
with the principal axes of their particles, then the body
frame inertia matrices are diagonal, and floating-point
operations as well as memory can be saved. The lower-          x̂j (t) := x̂j (x(t), ϕ(t))
                                                                       =            arg min                 fj1 (xj1 (t), ϕj1 (t), y),             (2)
right block of the mass matrix corresponds to the ma-
                                                                           fj2 (xj2 (t),ϕj2 (t),y)≤0
trix I(ϕ(t)). f(s(t), t) and τ(s(t), t) are the total forces
and torques (together they are referred to as wrenches)        with associated contact normal
acting at the particles’ centers of mass. Both may de-
pend on any of the state variables s(t) of the system          nj (t) := nj (x(t), ϕ(t)) = ∇y fj2 (xj2 (t), ϕj2 (t), x̂j (t)),
4                                                                                                   Tobias Preclik, Ulrich Rüde


pointing outwards with respect to Sj2 and associated               These non-penetration conditions can be comple-
signed contact distance                                        mented by a friction condition. The most prominent
                                                               model for dry frictional contact is the Coulomb model
ξj (t) := ξj (x(t), ϕ(t)) = fj1 (xj1 (t), ϕj1 (t), x̂j (t))    which restricts the relative contact velocity in the tan-
which is negative in the case of penetrations.                 gential plane of the contact. The relative contact veloc-
    For convex particles each pair of bodies results in        ity for a pair of particles (j1 , j2 ) involved in a contact j
a potential contact, and thus the total number of con-         is
tacts νc is limited by 12 νb (νb − 1). Non-convex objects      δvj+ (s(t)) =vj+1 (t) + ωj+1 (t) × (x̂j (x(t), ϕ(t)) − xj1 (t))
e.g. can be implemented as composite objects of con-
                                                                           −vj+2 (t) − ωj+2 (t) × (x̂j (x(t), ϕ(t)) − xj2 (t)).
vex particles. By convention a positive reaction in nor-
mal direction is repulsive, and thus the contact reaction      Let
λj (t) acts positively on particle j1 and negatively on j2 ,                                   
                                                                                                   tj (x(t), ϕ(t))T δvj+ (s(t))
                                                                                                                                  
                                                                 +             +
thus explaining the signs in (1). By applying the oppo-        δvj,to (t) := δvj,to (s(t)) =
                                                                                                   oj (x(t), ϕ(t))T δvj+ (s(t))
site reactions at the same point in the observational
frame, not only the linear momentum can be conserved           be the relative contact velocity in the tangential plane
but also the angular momentum of the system. Con-              after application of the contact impulses, then the Cou-
servation of energy can only hold if the contact model         lomb conditions for a non-impulsive point in time t are
does not include dissipative effects. Hard-contact mod-
                                                               kλj,to (t)k2 ≤ µj λj,n (t) and
els require the Signorini condition to hold. Written as           +                                    +
a complementarity condition for a contact j, it reads          kδvj,to (t)k2 λj,to (t) = −µj λj,n (t)δvj,to (t).
                                                                              +
ξj (t) ≥ 0 ⊥ λj,n (t) ≥ 0,                                     However, if kδvj,to (t)k2 = 0 these conditions must be
                                                               supplemented by the constraint
where λj,n (t) = nj (t)T λj (t). The signed contact dis-
                                                                 ˙ + (t)k2 λj,to (t) = −µj λj,n (t)δv
                                                               kδv                                  ˙ + (t)
tance is required to be non-negative, resulting in a non-          j,to                               j,to
penetration constraint. The contact reaction in direc-         on acceleration level in order to determine the friction
tion of the contact normal is also required to be non-         force. Likewise constraints for the friction impulse are
negative, resulting in non-adhesive contact reactions.         necessary. At this point we refrain from formulating the
Furthermore, both quantities must be complementary,            measure differential inclusion in detail since it would
meaning that either of them must be equal to zero. This        not contribute information essential to the remaining
effects that the contact reaction can only be non-zero         paper which only deals with the discrete-time system.
if the contact is closed.
    However, the Signorini condition does not determine
the contact reaction force if the contact is closed. In        3 Discrete Dynamical System
that case the non-penetration constraint on the velocity
level,                                                         In simulations of granular matter impulsive reactions
                                                               are abundant. Higher-order integrators for time-stepping
ξ˙j+ (t) ≥ 0 ⊥ λj,n (t) ≥ 0,                                   schemes are still subject to active research [31]. In par-
                                                               ticular, discontinuities pose problems for these integra-
must be added to the system, where ξ˙j+ is the right
                                                               tors. Hence, the continuous dynamical system is dis-
derivative of the signed contact distance with respect
                                                               cretized in the following with an integrator of order one,
to time. The constraint allows the contact to break
                                                               resembling the semi-implicit Euler method and similar
only if no reaction force is present and otherwise forces
                                                               to the one suggested in [2].
ξ˙j+ (t) = 0. In the latter case the reaction force is still
                                                                   Let s, x, ϕ, v and ω denote the given discrete-time
not fixed. The non-penetration constraint on the accel-
                                                               state variables at time t and λ the contact reactions at
eration level,
                                                               time t. Then the state variables at time t + δt are func-
ξ¨j+ (t) ≥ 0 ⊥ λj,n (t) ≥ 0,                                   tions depending on the contact reactions: s0 (λ), x0 (λ),
                                                               ϕ0 (λ), v 0 (λ) and ω 0 (λ). The discrete-time Newton-
then determines the force also if ξ¨j+ (t) = 0. When con-      Euler equations integrated by the proposed scheme are
sidering impacts, a non-penetration constraint for the
reaction impulse in the direction normal to the contact        
                                                                x0 (λ)
                                                                         
                                                                          x
                                                                                  
                                                                                      v 0 (λ)
                                                                                                 
surface must be formulated, and, if the contact is closed,       0      =    + δt           0      ,
                                                                ϕ (λ)     ϕ         Q(ϕ)ω (λ)
an additional constraint modelling an impact law such           0                                                      (3)
                                                                v (λ)     v                          f(s, λ, t)
as Newton’s impact must be added.                                0      =    + δtM(ϕ)−1                                .
                                                                ω (λ)     ω                   τ(s, λ, t) − ω × I(ϕ)ω
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                5


Positions and orientations at time t + δt appear exclu-           A detailed discussion of solution algorithms for one-
sively on the left-hand side of the position and orien-       contact problems is out of the scope of this article. How-
tation integration. Velocities at time t + δt appear on       ever, splitting methods, where non-penetration and fric-
the left-hand side of the velocity integration and addi-      tion constraints are solved separately, are prone to slow
tionally in the integration of positions and orientations.    convergence or cycling. In [7] Bonnefon et al. solve the
The numerical integration of the quaternion has the ef-       one-contact problem by finding the root of a quartic
fect that the quaternion gradually looses its unit length.    polynomial. Numerous other approaches exist for mod-
This deficiency can be compensated by renormalizing           ified friction laws, notably those where the friction cone
the quaternions after each integration.                       is approximated by a polyhedral cone and solution al-
    Instead of discretizing each of the five intermittently   gorithms for linear complementarity problems can be
active continuous-time complementarity constraints, the       used [1, 30]. In any case the algorithm of choice should
Signorini condition is only required to hold at the end       be extremely robust in order to successfully resolve νc
of each time step. This has the effect that impulsive re-     contacts per iteration and time step, where νc can be
actions are no longer necessary to satisfy the condition      in the order of 1010 in this article.
since the condition is no longer required to be fulfilled
instantaneously. Furthermore, the signed distance func-
tion gets linearized, resulting in                            4 Contact Detection

ξj (t + δt) = ξj (t) + δtξ˙j (t) + O(δt2 ),                   The contact problem F (λ) = 0 has O(νb2 ) non-linear
                                                              equations. Thus, already the setup of the contact prob-
where the time derivative of the signed contact distance      lem would not run in linear time, much less the so-
can be determined to be                                       lution algorithm even if it were optimal. The contact
                                                              constraints of a contact j can be removed from the sys-
ξ˙j (t) = nj (t)T δvj+ (s(t))
                                                              tem without altering the result if the contact is known
under the assumption that the contact point x̂j (t) trans-    to stay open (λj = 0) within the current time step. Let
lates and rotates in accordance with body j2 , such that
                                                              Si (t) = y ∈ R3 fi (xi (t), ϕi (t), y) ≤ 0
                                                                      

x̂˙ j (t) = vj2 (t) + ωj2 (t) × (x̂j (t) − xj2 (t)).          be the set of points in space corresponding to the ro-
Let the time-discrete relative contact velocity be            tated and translated shape of particle i at time t and
                                                              let
δvj0 (λ) =vj0 1 (λ) + ωj0 1 (λ) × (x̂j − xj1 )
                                                              Hi (t) = Si (t) + y ∈ R3 kyk2 ≤ hi (t)
                                                                               
         −vj0 2 (λ) − ωj0 2 (λ) × (x̂j − xj2 ),
                                                              be an intersection hull that spherically expands the par-
where the velocities are discretized implicitly. The dis-     ticle shape by the radius hi (t) > 0. If hi (t) is chosen
crete non-penetration constraint then is                      large enough then an algorithm finding intersections be-
ξj        0
                                                              tween the hulls can detect all contacts that can poten-
   + nT
      j δvj (λ) ≥ 0 ⊥ λj,n ≥ 0.                        (4)    tially become active in the current time step. A possible
δt
                                                              choice for the expansion radius is
             ξ
The term δtj acts as an error correction term if pen-
etrations are present (ξj < 0). In that case it can be        hi (t) = δt(kvi (t)k2 + kωi (t)k2 ri ) + τ,           (6)
scaled down to avoid introducing an excessive amount
                                                              where ri = maxy∈Si (0) kyk2 is the bounding radius of
of energy. If no numerical error is present, the contact
                                                              particle i, and τ is a safety margin. The safety mar-
is inelastic. The frictional constraints translate into
                                                              gin becomes necessary since an explicit Euler step is
kλj,to k2 ≤ µj λj,n and                                       underlying the derivation of (6). In practice, the us-
   0                             0
                                                       (5)    age of intersection hulls reduces the number of contacts
kδvj,to (λ)k2 λj,to = −µj λj,n δvj,to (λ).
                                                              considerably. E.g., monodisperse spherical particles can
    Let Fj (λ) = 0 denote a non-linear system of equa-        have at most 12 contacts per particle if the expansion
tions equivalent to the constraints from (4) and (5) of a     radii are small enough [32], resulting in O(νb ) potential
single contact j, and let F (λ) denote the collection of      contacts.
all Fj (λ). Neither F (λ) = 0 nor Fj (λ) = 0 for given            Broad-phase contact detection algorithms aim to
λj have unique solutions. Let Fj−1 (0, λj ) be a possible     find as few as possible candidate particle pairs for con-
solution of the one-contact problem of contact j, given       tacts by using e.g. spatial partitioning approaches or ex-
the contact reactions λj of all other contacts j.             ploiting temporal coherence of the particle positions [9].
6                                                                                              Tobias Preclik, Ulrich Rüde

1: k ← 0                                                          The algorithm is of iterative nature and needs an
2: λ(k) ← 0
3: while convergence criterion not met do                     appropriate stopping criterion to terminate. In each it-
4:    for j ← 1 to νc do                                      eration k a sweep over all contacts is performed, where
5:       for l ∈ C do (                                       each contact j is relaxed, given an approximation of all
                          (k+1)
               (k,j)     λl      if l < j ∧ sc (l) = sc (j)   other contact reactions λ̃(k,j) . In the subdomain NBGS,
6:           λ̃l     ←    (k)
                         λl      else                         the approximation of contact reaction l is taken from
7:       end for
8:
                        (k,j)
         y ← Fj−1 (0, λ̃j     )
                                                              the current iteration if it was already relaxed (l < j)
           (k+1)                    (k)                       and if it is associated with the same subdomain as the
 9:      λj    ← ωy + (1 − ω)λj
10:    end for
                                                              contact j to be relaxed (sc (l) = sc (j)). In all other
11:    k ←k+1                                                 cases, the approximation is taken from the previous it-
                                                                                                 (k+1)
12: end while                                                 eration. The contact reaction λj          is then a weighted
                                                              mean between the previous approximation and the re-
Algorithm 1: The subdomain NBGS method with re-               laxation result. If all contacts are associated with the
laxation parameter ω.                                         same subdomain and ω = 1 then Alg. 1 corresponds to
                                                              a classic NBGS. If each contact is associated to a differ-
The candidate pairs are then checked in detail in the         ent subdomain then Alg. 1 corresponds to a non-linear
narrow-phase contact detection, where (2) is solved for       block Jacobi (NBJ) with relaxation parameter ω.
each pair, leading to the contact location x̂j , normal nj
and signed distance ξj for a contact j.
    To solve (2) for non-overlapping particles, the Gil-   6 Parallelization Design
bert-Johnson–Keerthi (GJK) algorithm can be used [13,
4]. For overlapping particle shapes the expanding poly-    Sect. 6.1 introduces the domain partitioning approach.
tope algorithm (EPA) computes approximate solutions [5]. Sect. 6.2 then discusses requirements that must be met
For simple geometric primitives like spheres, the opti-    in order to be able to treat all contacts exactly once in
mization problem can be solved analytically. The in-       parallel. Sect. 6.3 explains how accumulator and cor-
dices of all contacts found that way form the set of po-   rection variables can be used in order to reduce data
tential contacts C = {1 . . νc } at time t. Let F (λ) = 0  dependencies to other processes. In Sect. 6.4 conditions
from now on denote the contact problem where all con-      are discussed under which the set of communication
tact conditions and contact reactions whose indices are    partners can be reduced to the nearest neighbors. Time-
not part of C have been filtered out.                      integration and the subsequent necessity of synchro-
                                                           nization are addressed in Sect. 6.5 before summarizing
                                                           the time-stepping procedure in Sect. 6.6.
5 Numerical Solution Algorithms

To solve the multi-contact problem, when suitable so-         6.1 Domain Partitioning
lution algorithms for the one-contact problems Fj−1
are given, a non-linear block Gauss-Seidel (NBGS) can         Under the assumption that no contacts are present,
be used as propagated by the non-smooth contact dy-           there exists no coupling between the data of any two
namics (NSCD) method [18]. Unfortunately, the Gauss-          particles, and the problem becomes embarrassingly par-
Seidel algorithm cannot be efficiently executed in par-       allel: Each process integrates b ννpb c or d ννpb e particles.
allel for irregular data dependencies as they appear in       Let sb (i) ∈ P determine the process responsible for the
contact problems [20].                                        time-integration of particle i as of now referred to as the
    As an alternative, a more general variant is pro-         parent process. All data associated with this particle,
posed here, accommodating the subdomain structure             that is the state variables (position, orientation, veloc-
that will arise in the domain partitioning. Therefore,        ities) and constants (mass, body frame inertia matrix,
each contact j ∈ C is associated with a subdomain             shape parameters), are instantiated only at the parent
number sc (j) ∈ P, where P = {1 . . νp } is the set of        process in order to distribute the total memory load.
subdomain indices for νp subdomains. Alg. 1 presents          However, contacts or short-range potentials introduce
pseudo-code for the subdomain NBGS with the relax-            data dependencies to particles that in general are not
ation parameter ω > 0. The initial solution is chosen to      instantiated on the local process nor on a process close
be zero, however, any other initialization can be used,       to the local one, rendering a proper scaling impossible.
in particular contact reactions from the previous time        A domain partitioning approach alleviates this prob-
step.                                                         lem.
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                 7


    Let Ω denote the computational domain within which        These additional instantiations shall be termed shadow
all particles are located and Ωp ⊆ Ω, p ∈ P, a family         copies in the following. They must be kept in synchro-
of disjoint subdomains into which the domain shall be         nization with the original instantiation on the parent
partitioned. In this connection subdomain boundaries          process. In order to agree upon the detecting process
are associated to exactly one process. One process shall      responsible for treating the contact without commu-
be executed per subdomain. The number of processes            nication a rule is needed. Here, the statement that a
can e.g. correspond to the number of compute nodes in         process is responsible for treating a contact refers to
a hybrid parallelization or to the total number of cores      the responsibility of the process for executing the re-
or even threads in a homogeneous parallelization. In the      laxation of the respective contact in Alg. 1. The typical
domain partitioning approach the integration of a par-        choice for this rule requires that the process whose sub-
ticle whose center of mass xi is located in a subdomain       domain contains the point of contact is put in charge
Ωp at time t is calculated by process p. That way data        to treat the contact [34].
dependencies typically pertain the local or neighboring           However, this rule only works if the process whose
subdomains since they are considered to be of short           subdomain contains the point is able to detect the con-
range. Let sb (i) be adapted accordingly. Special care        tact. This is only guaranteed if the point of contact is
is required when associating a particle to a subdomain        located within the hull intersection. Also, if the point
whose center of mass is located on or near subdomain          of contact is located outside of the domain Ω, then no
interfaces. Especially, periodic boundary conditions can      process will treat it.
complicate the association process since the finite pre-          A more intricate drawback of this approach is that
cision of floating-point arithmetics does in general not      it can fail in case of periodic boundary conditions: If
allow a consistent parametric description of subdomains       the contact point is located near the periodic bound-
across periodic boundaries. Sect. 6.5 explains how the        ary, the periodic image of the contact point will be
synchronization protocol can be used to allow a reliable      detected at the other end of the simulation box. Due
association.                                                  to the shifted position of the contact point image and
    The domain partitioning should be chosen such that        the limited numerical precision, the subdomains can no
an equal number of particles is located initially in each     longer consistently decide the subdomain affinity.
subdomain and sustained over the course of the simula-            A more robust rule to determine the subdomain
tion in order to balance the computational load which         affinity can be established by fulfilling the following re-
is directly proportional to the number of particles. Par-     quirement:
ticles now migrate between processes if their positions       Requirement 2 All shadow copy holders of a parti-
change the subdomain. Migration can lead to severe            cle maintain a complete list of all other shadow copy
load imbalances that may need to be addressed by dy-          holders and the parent process of that particle.
namically repartitioning the domain. Such load-balancing
techniques are beyond the scope of this article.              Then each process detecting a contact can determine
                                                              the list of all processes detecting that very same con-
                                                              tact, which is the list of all processes with an instan-
                                                              tiation of both particles involved in the contact. This
6.2 Shadow Copies                                             list is exactly the same on all processes detecting the
                                                              contact and is not prone to numerical errors. The rule
A pure local instantiation of particles has the effect that   can then e.g. appoint the detecting process with small-
contacts cannot be detected between particles that are        est rank to treat the contact. In order to enhance the
not located on the same process. A process can detect a       locality of the contact treatment, the rule should fa-
contact if both particles involved in the contact are in-     vor the particle parents if they are among the contact
stantiated on that process. In order to guarantee that        witnesses. Any such rule defines a partitioning of the
at least one process can detect a contact, the condi-         contact set C. Let Cp be the set of all contacts treated
tion that a contact j must be detected by all processes       by process p ∈ P. Then process p instantiates all con-
whose subdomains intersect with the hull intersection         tacts j ∈ Cp .
Hj1 ∩ Hj2 is sufficient if the intersection of the hull in-
tersection and the domain is non-empty. This condition
can be fulfilled by the following requirement:                6.3 Accumulator and Correction Variables

Requirement 1 A particle i must be instantiated not           The contact relaxations in Alg. 1 exhibit sums with
only on the parent process but also on all processes          non-local data dependencies. In the following, the re-
whose subdomains intersect with the particle’s hull.          dundant evaluation of these sums is prevented by intro-
8                                                                                                                                                            Tobias Preclik, Ulrich Rüde


ducing accumulator variables and the non-local data de-                                                      parameter. Since the subdomain NBGS respects the
pendencies are reduced by introducing correction vari-                                                       subdomain affinity of the contacts, the remote wrench
ables.                                                                                                       contributions to particle i cancel out, and just the total
    The relaxation of a contact j depends on the data                                                        wrench on particle i from the last iteration is needed
of the state variables of both particles (j1 , j2 ) involved                                                 in addition to corrections stemming from contacts that
in the contact, their constants and shape parameters,                                                        were already relaxed by the same process.
as can be seen by inspecting (4), (5) and the definitions
                                                                                                              fi (λ̃(k,j) )       fi (λ(k) )
                                                                                                                                            X             
of the terms appearing therein. All of these quantities                                                                                                  1        (k+1)    (k)
                                                                                                                      (k,j)    =       (k)    +               × (λl     − λl )
                                                                                                               τi (λ̃       )     τi (λ )          (x̂l − xi )
are instantiated on the detecting process, either as a                                                                                               l∈Csc (j)
                                                                                                                                                        l<j
shadow copy or as an original instance. The contact                                                                                                    l1 =i

variables of contact j (location, signed distance and                                                                                                  X                    
                                                                                                                                                                       1        (k+1)    (k)
                                                                                                                                                 −                          × (λl     − λl )
the contact frame) are also required. They are avail-                                                                                                            (x̂l − xi )
                                                                                                                                                     l∈Csc (j)
able on the detecting process since they result from                                                                                                    l<j
                                                                                                                                                       l2 =i
the positions, orientations, and the shape parameters
of the particles (j1 , j2 ) in the contact detection. Fur-                                                       Our implementation instantiates variables on pro-
thermore, the force and torque terms from (1) acting                                                         cess p for the reaction approximations λ[p] ∈ R3|Cp | of
on these particles additionally depend on the locations                                                      all contacts treated by process p. Any updates to the
                                     (k,j)
x̂l and reaction approximations λ̃l        of all other con-                                                 reaction approximations occur in place. Furthermore,
tacts l involving one of the particles (j1 , j2 ). Neither the                                               an implementation can instantiate accumulator vari-
locations nor the reaction approximations of these con-                                                      ables f [p] , τ [p] ∈ R3|Bp | on process p for the wrenches
tacts are necessarily available on the process treating                                                      from the last iteration of all instantiated particles (shadow
contact j. To rectify this deficiency, one can introduce                                                     copies and original instances), where Bp contains the in-
contact shadow copies so that location and reaction ap-                                                      dices of all shadow copies and original instances instan-
proximation can be mirrored at every instantiation of                                                        tiated on process p. This set is partitioned into Bp,local
both particles involved in the contact. However, the or-                                                     and Bp,shadow , containing the indices of the original in-
ganisational overhead of contact shadow copies can be                                                        stances and the shadow copies respectively.
circumvented. It is not necessary that the process treat-                                                        Instead of evaluating the wrench contribution sums
ing the contact evaluates all the wrench contributions                                                       each time when calculating the total wrench on parti-
to the particles involved in the contact. Instead, parts                                                     cle i anew, the contributions can be accumulated as the
of the wrench contribution sum can be evaluated on the                                                       contacts are relaxed. For that purpose, implementations
processes actually treating the remote contacts and can                                                      can instantiate corrections variables δf [p] ∈ R3|Bp | and
subsequently be communicated:                                                                                δτ [p] ∈ R3|Bp | . Then, after line 9 of Alg. 1, these wrench

    fi (λ)
            
               fi,ext
                       X
                                1
                                           X      1
                                                                                                            corrections can be updated by assigning
            =          +             × λl −              × λl
    τi (λ)     τi,ext     (x̂l − xi )         (x̂l − xi )
                                     l∈C                              l∈C
                                                                                                                            !                    !
                                                                                                                  [s (j)]              [s (j)]                 
                                    l1 =i                            l2 =i                                     δfj1 c               δfj1 c              1           (k+1)    (k)
                                                                                                     
                                                                                                                 [s (j)]        ←     [s (j)]        +        × (λj       − λj ),
                                  X X                   X                                               δτj1 c               δτj1 c       (x̂j − xj1 )
                   fi,ext                       1                    1         
           =                    +                     × λl −              × λl 
                                                                              
                   τi,ext                 (x̂l − xi )          (x̂l − xi )
                                                                                                                            !                 ! 
                                                                                                                 [s (j)]             [s (j)]                   
                                    p∈P          l∈Cp                             l∈Cp                         δfj2 c               δfj2 c              1           (k+1)    (k)
                                                 l1 =i                            l2 =i                                         ←              −                  (λj     − λj ).
                                             |                               {z                        }         [s (j)]
                                                                                                               δτj2 c
                                                                                                                                      [s (j)]
                                                                                                                                    δτj c         (x̂j − xj2 )×
                                            wrench contribution (fi,p τi,p )T to particle i from process p                             2



    The total wrench on particle i can also be expressed                                                         The evaluation of the total wrench on particle i in
in terms of the total wrench on particle i at the begin-                                                     line 8 of Alg. 1 when relaxing contact j in iteration k
ning of iteration k:                                                                                         becomes
                                                                                                                                          !              !
                                                                                                                                   [s (j)]        [s (j)]
                                                                                                               fi (λ̃(k,j) )
                                                                                                                            

    fi (λ)
                  (k)
               fi (λ )
                           X X
                                      1
                                                                                                                                fi c          δfi c
                                                      (k)                                                                      =             +   [s (j)] ,
                             
            =              +                   (λl − λl )                                                                         [s (j)]
                                                                                                               τi (λ̃(k,j) )
                             
    τi (λ)     τi (λ(k) )      (x̂l − xi )×                                                                                     τi c          δτi c
                                                  p∈P        l∈Cp
                                                             l1 =i
                                                                                                      
                                                                                                             that is the sum of the accumulator and the correction
                                                              X           1
                                                                                          
                                                         −
                                                                                         (k) 
                                                                                  (λl − λl )                variables.
                                                                     (x̂l − xi )×            
                                                             l∈Cp                                                At the end of each iteration the wrench corrections
                                                             l2 =i
                                                                                                             for each body have to be reduced and added to the accu-
    When relaxing the contact j in iteration k of the                                                        mulated wrench from the last iteration. This can be per-
subdomain NBGS, the wrench on particle i ∈ {j1 , j2 }                                                        formed in two message exchanges. In the first message
is evaluated with the reaction approximation λ̃(k,j) as                                                      exchange each process sends the wrench correction of
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                                 9


each shadow copy to its parent process. Then each pro-                 be the set of process indices in direct neighborhood of
cess sums up for each original instance all wrench cor-                process p’s subdomain, and let
rections obtained from the shadow copy holders, its own
                                                                                                                                      
wrench correction, and the original instance’s accumu-                                                                [               
lated wrench. Subsequently, the updated accumulated                    ldd = min inf kyp − yq k2 yp ∈ Ωp , yq ∈                   Ωq       ,
                                                                             p∈P                                                      
wrench of each original instance is sent to the shadow                                                            q∈P\(Np ∪{p})

copy holders in a second message-exchange communi-
cation step. The wrench corrections are then reset ev-                 be the shortest distance from a point inside a subdo-
erywhere.                                                              main to a non-nearest neighbor. Then the condition
    The accumulated wrenches f [p] , τ [p] are initialized
on each process p before line 3 in Alg. 1 to                           ri + kvi (t)k2 δt + τ < ldd   ∀i ∈ B                        (7)
          !
    [p]                       
  fi                  fi,ext                                           ensures in the first approximation that no hull extends
   [p]        ←                    ∀i ∈ Bp
  τi                  τi,ext                                           past neighboring subdomains. This immediately defines
                                                                       a hard upper limit of ri < ldd − τ for the bounding ra-
unless the initial solution is chosen to be non-zero. The              dius and thus for the size of all objects. Furthermore,
wrench corrections are initially set to 0. If the external             given the particle shapes, velocities, and safety mar-
forces and torques are not known on each process or are                gins, the condition defines an upper limit for the time-
scattered among the processes having instantiated the                  step length. The introduction of condition (7) entails
particles, the initialization requires another two mes-                that on a process p   only the description of the subdo-
sage exchanges, as they are necessary at the end of each               mains within Ωp + y ∈ R3 kyk2 ≤ ldd needs to be
iteration.                                                             available, meaning that the description of non-nearest-
    An alternative to storing accumulated wrenches and                 neighbor subdomains can be dispensed with, and that
wrench corrections is to store accumulated velocities                  the description of nearest-neighbor subdomains do not
and velocity corrections. In that case, a process p in-                have to be correct outside of the ldd -surrounding of Ωp .
stantiates variables v [p] , ω [p] , δv [p] , δω [p] ∈ R3|Bp | . The   This leads to a localized description of the domain par-
accumulated velocities are set to vi0 (λ(k) ) and ωi0 (λ(k) )          titioning on each process, describing the surrounding
for all i ∈ Bp in each iteration. They are initialized                 subdomains only.
and updated accordingly. The velocity corrections are                       Typically, the size limit stemming from (7) is not a
initialized and updated analogously to the wrench cor-                 problem for the particles of the granular matter them-
rections. Hereby, the velocity variables can be updated                selves, but very well for boundaries or mechanical parts
in place. In the classic NBGS no wrench or velocity                    the granular matter interacts with. However, the num-
correction variables would be necessary, but the correc-               ber of such enlarged bodies is typically significantly
tions could be added to the velocity variables right away              smaller than and independent of the number of small-
which is similar to the approach suggested by Tasora et                sized particles, suggesting that they can be treated glob-
al. in [37].                                                           ally. Let Bglobal be the set of all body indices exceeding
                                                                       the size limit. These bodies will be referred to as being
                                                                       global in the following. All associated state variables
6.4 Nearest-Neighbor Communication                                     and constants shall be instantiated on all processes and
                                                                       initialized equally. The time-integration of these global
In the following we describe how the strict locality of                bodies then can be performed by all processes equally.
particle interactions can be used to optimize the paral-               If a global body i has infinite inertia (mi = ∞ and
lel communication and synchronization by exchanging                    I0ii = ∞1), such as a stationary wall or a non-stationary
messages only between nearest neighbors. So far the                    vibrating plate, the body velocities are constant, and no
shadow copies can be present on any process, and the                   wrenches need to be communicated. Global bodies hav-
corrections in the summation over wrench or velocity                   ing a finite inertia can be treated by executing an all-
corrections can originate from a long list of processes.               reduce communication primitive whenever reducing the
However, by requiring that the particle hulls do not                   wrench or velocity corrections of the small-sized bodies.
extend past any neighboring subdomains, all message                    Instead of only involving neighboring processes, the all-
exchanges can be reduced to nearest-neighbor commu-                    reduce operation sums up the corrections for each global
nications. Let                                                         body with finite inertia from all processes and broad-
                                                                       casts the result, not requiring any domain partitioning
Np = {q ∈ P \ {p} | inf {kyp − yq k2 | yp ∈ Ωp , yq ∈ Ωq } = 0}        information.
10                                                                                           Tobias Preclik, Ulrich Rüde


6.5 Time-Integration and Synchronization Protocol              1: procedure simulateTimeStep
                                                               2:    Cp,bp = broadPhaseCollisionDetection
                                                               3:    Cp,np = narrowPhaseCollisionDetection(Cp,bp )
Having solved the contact problem F (λ) = 0 by Alg. 1,         4:    Cp = filterContacts(Cp,np )
the time-integration defined in (3) needs to be per-           5:    initializeAccumulatorAndCorrectionVariables
                                                               6:    k←0
formed. If the NBGS implementation uses velocity ac-
                                                               7:    λ[p] ← 0
cumulators, the integrated velocities are at hand after        8:    while convergence criterion not met do
the final communication of the velocity corrections. If        9:        for j ← 1 to νc ∧ j ∈ Cp do
                                                                              [p]             [p]           [p]
instead the NBGS implementation uses wrench accu-             10:            λj ← ωFj−1 (0, λj ) + (1 − ω)λj
mulators, the wrenches are at hand, and the velocities        11:        end for
of all local bodies can be updated immediately.               12:        reduceCorrections
                                                              13:        k ←k+1
     Subsequently, the time-integration of the positions      14:    end while
can take place. Updating a body’s position or orienta-        15:    integrateStateVariables
tion effects that the list of shadow copy holders changes     16:    synchronize
                                                              17: end procedure
since the intersection hull possibly intersects with dif-
ferent subdomains. Also, the body’s center of mass can        Algorithm 2: A single time step of the simulation on
move out of the parent’s subdomain. In order to restore       process p.
the fulfillment of the requirements 1 and 2, a process
must determine the new list of shadow copy holders
and the new parent process for each local body after          proposed by Shojaaee et al. in [34] are canonical. Con-
the position update. Shadow copy holders must be in-          cerning the geometry of the subdomains at least the
formed when such shadow copies become obsolete and            subdomain closures can be used for intersection test-
must be removed. Analogously, processes must be no-           ing. In our implementation we chose to determine al-
tified when new shadow copies must be added to their          most minimal sets of shadow copy holders by testing
state. In this case copies of the corresponding state vari-   the intersections of the actual hull geometries of the
ables, constants, list of shadow copy holder indices, and     particles with the closures of the subdomains. This re-
index of the parent process must be transmitted.              duces the number of shadow copies and thus the overall
     All other shadow copy holders must obtain the new        communication volume in exchange for more expensive
state variables, list of shadow copy holder indices, and      intersection tests.
index of the parent process. Hereby, the condition from
(7) guarantees that all communication partners are neigh-
bors. All information can be propagated in a single ag-       6.6 Summary
gregated nearest-neighbor message-exchange. The in-
formation should be communicated explicitly and should        Alg. 2 summarizes the steps that need to be executed on
not be derived implicitly, in order to avoid inconsisten-     a process p when time-integrating the system for a sin-
cies. This is essential to guarantee a safe determination     gle time step δt in parallel. The algorithm requires that
of the contact treatment responsibilities as well as time-    all shadow copies are instantiated on all subdomains
integration responsibilities.                                 their hull intersects with. Furthermore, the shadow copies
     Our implementation of the synchronization proto-         must be in sync with the original instance, and the
col makes use of separate containers for storing shadow       global bodies must also be in sync to each other. The
copies and original instances in order to be able to enu-     positions of all local bodies must be located within the
merate these different types of bodies with good per-         local subdomain. The time step proceeds by executing
formance. Both containers support efficient insertion,        the broad-phase contact detection which uses the po-
deletion and lookup operations for handling the fluctu-       sitions, orientations, shapes, hull expansion radii, and
ations and updates of the particles efficiently. Further-     possibly information from previous time steps, in order
more, the determination of the new list of shadow copy        to determine a set of contact candidates (body pairs)
holders involves intersection tests between intersection      Cp,bp on process p in near-linear time.
hulls of local bodies and neighboring subdomains as re-           Then, in the narrow-phase contact detection, for
quirement 1 explains in Sect. 6.2. However, determining       all candidates the contact location, associated contact
the minimal set of shadow copy holders is not necessary.      frame, and signed contact distance is determined if the
Any type of bounding volumes can be used to ease in-          hulls actually intersect. Finally, this set of detected con-
tersection testing. In particular bounding spheres either     tacts Cp,np needs to be filtered according to one of the
with tightly fitting bounding radii ri + hi (t) or even       rules presented above, resulting in Cp , the set of contacts
with an overall bounding radius maxi∈B ri + hi (t) as         to be treated by process p. Before entering the itera-
Ultrascale Simulations of Non-smooth Granular Dynamics                                                              11


tion of the subdomain NBGS, the accumulator, correc-          7.1 Weak and Strong Scalability
tion, and contact reaction variables must be initialized.
The initialization of the accumulator variables requires      To demonstrate the scalability of the algorithms and
an additional reduction step if the external forces or        their implementation, we perform weak-scaling exper-
torques cannot be readily evaluated on all processes.         iments, where the problem size is chosen directly pro-
    Each iteration of the subdomain NBGS on process p         portional to the number of processes and such that the
involves a sweep over all contacts to be treated by the       load per process stays constant. Thus, if ideal scaling
process. The contacts are relaxed by a suitable one-          were achieved, the time to solution would stay constant.
contact solver. The j indexing indicates that such a          Let tp be the time to solution on p processes, then the
solver typically needs to evaluate the relative contact       parallel efficiency ep,ws in a weak-scaling experiment is
velocity under the assumption that no reaction acts at        defined to be
the contact j. This can be achieved by subtracting out                  t1
the corresponding part from the accumulator variables.        ep,ws =      .
                                                                        tp
The weighted relaxation result is then stored in place.
The update of the wrench or velocity correction vari-
                                                                  In strong-scaling experiments, in contrast, the prob-
ables is not explicitly listed. After the sweep the wrench
                                                              lem size is kept constant, effecting a decreasing work
or velocity corrections are sent to the respective parent
                                                              load per process when increasing the number of pro-
process and summed up per body including the accu-
                                                              cesses. Thus, ideally the time to solution on p processes
mulator variables. Then the accumulator variables are
                                                              should be reduced by p in comparison to the time to
redistributed to the respective shadow copy holders in
                                                              solution on a single process. The speedup sp on p pro-
a second message-exchange step.
                                                              cesses is defined to be
    After a fixed number of iterations or some prescribed
convergence criterion is met, the time step proceeds by              t1
                                                              sp =      .
executing the time-integration for each local body. The              tp
changes of the state variables must then be synchro-
nized in a final message-exchange step, after which the       The parallel efficiency ep,ss in a strong-scaling experi-
preconditions of the next time step are met. Any user         ment is then the fraction of the ideal speedup actually
intervention taking place between two time steps needs        achieved
to adhere to these requirements.
                                                                        sp    t1
                                                              ep,ss =      =     .
                                                                        p    ptp

                                                                  Sometimes speedup and parallel efficiency are also
7 Experimental Validation of Scalability                      stated with respect to a different baseline, that is, a
                                                              single central processing unit (CPU) or a single node
This section aims to assess the scalability of the paral-     rather than a single hardware thread or core – the
lelization design presented in Sect. 6 as we implemented      principle remains the same. The parallel efficiency in
it in the pe which is an open-source software frame-          a weak- and strong-scaling context is a simple perfor-
work for massively parallel simulations of rigid bod-         mance metric that will serve in the following to assess
ies [16, 17]. The implementation is based on velocity ac-     the quality of the parallelization.
cumulators and corrections, as introduced in Sect. 6.3.
The accumulator initialization performs an additional
initial correction reduction step in all experiments.         7.2 Test Problems
    In Sect. 7.1 the idea behind weak- and strong-scaling
experiments is explained before presenting the test prob-     The scalability of the parallelization algorithm as it is
lems for which those experiments are executed in Sect. 7.2.   implemented in the pe framework is validated based on
The scaling experiments are performed on three clus-          two fundamentally different families of test problems.
ters whose properties are summarized and compared             Sect. 7.2.1 describes a family of dilute granular gas se-
in Sect. 7.3. Sect. 7.4 points out the fundamental dif-       tups whereas Sect. 7.2.2 describes a family of hexagonal
ferences in the scalability requirements of the two test      close packings of spheres corresponding to structured
problems. Finally, in Sect. 7.5 the weak-scaling and in       and dense setups. We chose these setups because their
Sect. 7.6 the strong-scaling results are presented for        demands towards the implementation vary considerably
each test problem and cluster.                                which will be analyzed in detail in Sect. 7.4.
12                                                                                            Tobias Preclik, Ulrich Rüde


7.2.1 Granular Gas                                            the number of processes in x-, y-, and z-dimension that
                                                              is used in the experiment. With this arrangement the
Granular material attains a gaseous state when suffi-         initial load is perfectly balanced. Statistically, the load,
cient energy is brought into the system, for example by       that is the number of particles and contacts per sub-
vibration. Consequently, granular gases feature a low         domain, remains balanced if the subdomains are large
solid volume fraction and are dominated by binary col-        enough, and clustering effects have not yet progressed
lisions. When the energy supply ceases, the system cools      too far. The duration of the simulation was chosen such
down due to dissipation in the collisions. Granular gases     that the load remains well balanced throughout.
are not only observed in laboratory experiments, but
appear naturally for example in planetary rings [35] and      7.2.2 Hexagonal Close Packing of Spheres
in technical applications such as granular dampers [19].
These systems in general exhibit interesting effects like     This setup aims to assess the scalability of the par-
the inelastic collapse [24] or other clustering effects as    allelization for dense granular setups. To demonstrate
they e.g. can be observed in the Maxwell-demon exper-         the scalability, the initial setup should be easily and
iment [41].                                                   efficiently generateable for arbitrary problem sizes and
     As initial conditions, a rectangular domain with con-    should feature a good load balance over a longer pe-
fining walls is chosen. The domain contains a prescribed      riod of time. Hence, a hexagonal close packing of equal
number of non-spherical particles arranged in a Carte-        spheres was chosen, for which simple formulas for the
sian grid. Random initial                                     position of the spheres are available. The packing den-
                         √ velocities are assigned to the                             π
particles with up to 2103 m/s ≈ 0.35 m/s. The particles       sity is known to be 3√    2
                                                                                          ≈ 74.0%. According to the Ke-
are composed of two to four spheres of varying radius         pler conjecture, a hexagonal close packing is the densest
in the range [0.6 cm, 0.8 cm], arranged at the bound-         possible packing of spheres. To avoid load imbalances
ary of a bounding sphere with a diameter of 1 cm. The         at the boundaries, a domain is chosen that is periodic
distance between the centers of two granular particles        in the x- and y-dimension. In z-dimension the packing
along each spatial dimension is 1.1 cm, amounting to          is confined by walls that are in direct contact with the
a solid volume fraction of 23% on average. In [16] al-        spheres on both sides. Assuming an even number of
most the same family of setups served as a scalability        particles in y-direction, the number of contacts is per-
test problem. However, there the granular gases had a         manently nx ny (6nz − 1) for nx × ny × nz particles. The
solid volume fraction of 3.8% on average. In order to         domain is decomposed in x- and y-dimensions only. The
test a higher collision frequency, a more dense granular      objects are subject to gravity. However, the gravity is
gas was chosen here. The system is simulated for 10    1
                                                         s,   tilted in the x-z-plane such that the setup corresponds
and the time step is kept constant at 100 µs, resulting       to a ramp inclined by 30◦ including a lid. The mag-
in 1 000 time steps in total. Since the contacts are dis-     nitude of gravity is 9.81 m/s2 . The time step is 10 µs
sipative and no energy is added, the system is quickly        constantly. The radii of the particles are 1 mm, and
cooling down. The coefficient of friction is 0.1 for any      their density is 2.65 g/cm3 . All particles get an initial
contact.                                                      downhill velocity of 10 cm/s. The coefficient of friction
                                                              is 0.85 constantly for any contact. The high coefficient
     For this test problem, the subdomain NBGS solver
                                                              of friction causes a slip-stick transition shortly after the
requires a slight underrelaxation in order to prevent di-
                                                              simulation begins. As in the granular gas setups the
vergence. Using an underrelaxation parameter of 0.75
                                                              subdomain NBGS uses an underrelaxation of 0.75. The
produces good results. For binary collisions, a single it-
                                                              solver unconditionally performs 100 iterations in each
eration of the solver would suffice, but because particles
                                                              time step. This intentionally disregards that the iter-
cluster due to the inelastic contacts, more iterations are
                                                              ative solver converges faster for smaller problems. A
required. This could be determined by a dynamic stop-
                                                              multigrid solver could possibly remedy the dependence
ping criterion, but in the scenario presented here it was
                                                              on the problem size, but the successful construction of
found to be more efficient to perform a fixed number of
                                                              such a solver needs substantial further research.
10 iterations.
     For particle simulations, the work load strongly de-
pends on the number of particles and contacts. For the        7.3 Test Machines
weak-scaling experiments, each process is responsible
for a rectangular subdomain, initially containing a fixed     In the following all test machines are presented. Tab. 1
number of particles arranged in a Cartesian grid. For         summarizes the basic information. The Emmy cluster
the strong-scaling experiments, the total number of par-      is located at the Regional Computing Centre in Er-
ticles in x-, y-, and z-dimension should be divisible by      langen (RRZE) in Germany which is associated to the
Ultrascale Simulations of Non-smooth Granular Dynamics                                                             13


    cluster name                  Emmy                           SuperMUC                 Juqueen
                                  Regional Computing Centre in   Leibniz Supercomputing   Jülich Supercomputing
    computing centre
                                  Erlangen (RRZE), Germany       Centre (LRZ), Germany    Centre (JSC), Germany
    best TOP 500 ranking          -                              4th (June 2012)          5th (November 2012)
    peak performance in PFlop/s   0.23                           3.2                      5.9
    number of nodes               560                            9 216                    28 672
    number of sockets             2                              2                        1
    name of CPU                   Intel Xeon E5-2660 v2          Intel Xeon E5-2680       IBM PowerPC A2
    clock rate in GHz             2.2                            2.7                      1.6
    number of cores per CPU       10                             8                        16
    number of threads per core    2                              2                        4
    total RAM in TiB              35                             288                      448
                                                                 Infiniband QDR/
    interconnection fabric        Infiniband QDR                                          BlueGene/Q
                                                                 Infiniband FDR 10
                                                                 non-blocking tree/
    network topology              non-blocking tree                                       5D torus
                                                                 4:1 pruned tree

            Table 1: The test machines used for performing the weak- and strong-scaling experiments.


Friedrich-Alexander-Universität Erlangen-Nürnberg. The 126 links to 126 spine switches. This results in a block-
cluster comprises 560 compute nodes. Each node has a        ing switch-topology. Thus, if e.g. all nodes within an
dual-socket board equipped with two Xeon E5-2660 v2         island send to nodes located in another island, then
processors. Each processor has 10 cores clocked at 2.2 GHz. the 512 nodes have to share 126 links to the spine
The processors offer 2-way simultaneous multithread-        switches, effecting that the bandwidth is roughly one
ing (SMT). The peak performance of the cluster is           quarter of the bandwidth that would be available in an
0.23 PFlop/s. Each node is equipped with 64 GiB of ran-     overall non-blocking switch-topology. Each (thin) com-
dom access memory (RAM). The cluster features a fully       pute node has two sockets, each equipped with an In-
non-blocking Infiniband interconnect with quad data         tel Xeon E5-2680 processor having 8 cores clocked at
rate (QDR) and 4× link aggregation, resulting in a          2.7 GHz. The processors support 2-way SMT. In the
bandwidth of 40 Gbit/s per link and direction. In all ex-   following, as in the case of the Emmy cluster, each core
periments on the Emmy cluster, each core is associated      is associated with a single subdomain. The peak per-
with a subdomain since preliminary tests showed that        formance of the cluster is stated to be 3.2 PFlop/s. Each
we could not take advantage of the SMT features by          node offers 32 GiB of RAM, summing up to 288 TiB in
associating each hardware thread with a subdomain.          total. The SuperMUC supercomputer has an interest-
The Emmy cluster has the smallest peak performance          ing blocking tree network-topology and the processors
among the test machines and was never among the 500         with the highest clock rate among the processors in the
world’s largest commercially available supercomputers.      test machines.
However, it is the only machine with the largest non-           The third test machine is the Juqueen supercom-
blocking tree network topology and the largest amount       puter which is located at the Jülich Supercomputing
of RAM per core.                                            Centre (JSC) in Germany and was best ranked on the
    The second test machine is the SuperMUC super-          5th place of the TOP 500 list in November 2012. The
computer which is located at the Leibniz Supercomput-       cluster is a BlueGene/Q system with 28 672 compute
ing Centre (LRZ) in Germany and was best ranked on          nodes since 2013 [14, 40]. Each node features a single
the 4th place of the TOP 500 list in June 2012. The         IBM PowerPC A2 processor having 18 cores clocked at
cluster is subdivided into multiple islands. The major-     1.6 GHz, where only 16 cores are available for comput-
ity of the compute power is contributed by the 18 thin-     ing. The processors support 4-way SMT. The Juqueen
node islands. Each thin-node island consists of 512 com-    supercomputer is the only machine, where we decided
pute nodes (excluding four additional spare nodes) con-     to associate each hardware thread with a subdomain
nected to a fully non-blocking 648 port FDR10 Infini-       in the scaling experiments. The machine’s peak perfor-
band switch with 4× link aggregation, resulting in a        mance is 5.9 PFlop/s. Each node offers 16 GiB of RAM,
bandwidth of 40 Gbit/s per link and direction. Though       summing up to 448 TiB in total. The interconnect fabric
QDR and FDR10 use the same signaling rate, the ef-          is a 5D torus network featuring a bandwidth of 16 Gbit/s
fective data rate of FDR10 is more than 20% higher          per link and direction [8]. The Juqueen supercomputer
since it uses a more efficient encoding of the transmit-    is the machine with the highest peak performance, the
ted data. The islands’ switches are each connected via      largest number of cores and threads and the only ma-
14                                                                                             Tobias Preclik, Ulrich Rüde


chine among our test machines with a torus intercon-
nect.
    Tab. 2 presents a summary of the domain parti-
tionings used for the scaling experiments on the vari-                      12.6
                                                                                   %                             16.
                                                                                                                       5%
                                                                                                         %
ous clusters. The number of nodes are always a power                  %                                .7




                                                                                                  22
                                                                 .9
                                                               25
of two except when using the whole machine or when




                                                                                       18.1%




                                                                                                                            16.0%
performing intra-node scalings. The intra-node scaling




                                                                                                .3%
behaviour is analyzed by means of weak-scaling exper-




                                                                  %




                                                                                                    %8
                                                               9.5
iments choosing the granular gas as a test problem and




                                                                                                 5.9
                                                                  %
the Emmy cluster as a test machine. The influence of                  8.0   .8%
                                                                                  25
                                                                                                             30.6%
the number of dimensions in which the domain is par-
titioned is also only analyzed for this configuration.       (a) Time-step profile of the      (b) Time-step profile of the
All further scaling tests of the granular gas scenario       granular gas executed with        granular gas executed with
use three-dimensional domain partitionings. All inter-       5 × 2 × 2 = 20 processes on       8 × 8 × 5 = 320 processes on
node weak-scaling experiments start with a single node       a single node.                    16 nodes.
and extend to the full machine where possible. The ex-
                                                             Fig. 1: The time-step profiles for two weak-scaling exe-
periments on the SuperMUC supercomputer were ob-
                                                             cutions of the granular gas on the Emmy cluster with
tained at the Extreme Scaling Workshop in July 2013
                                                             253 particles per process.
at the LRZ, where at most 16 islands corresponding
to 8 192 nodes were available. All strong-scaling exper-
iments start on a single node except on the Juqueen
                                                             correction reduction message (light green section). The
supercomputer, where we chose to start at 32 nodes
                                                             time slices are depicted counterclockwise in the given
which is the minimum allocation unit in the batch sys-
                                                             order. The message-exchange communications have a
tem on Juqueen. The experiments extend to a number
                                                             dotted border to distinguish them from the rest. A
of nodes where a notable efficiency degradation is ob-
                                                             single message-exchange communication time measure-
served. Since the results on the SuperMUC were ob-
                                                             ment started, when sending the first message buffer to
tained well before the other experiments, no scaling
                                                             the neighbors, and ended, when having received the last
experiments with the hexagonal close packing scenario
                                                             message buffer from the neighbors. The dark red section
were performed.
                                                             corresponds to the time used by the time-integration
                                                             of the positions, and the final blue section indicates
7.4 Time-Step Profiles                                       the time used by the position synchronization. The lat-
                                                             ter is split up into assembling, exchanging, and pro-
In this section we clarify how much time is spent in         cessing of the message in the inner ring. The message-
the various phases of the time-step procedure and how        exchange communication is highlighted by the dashed
this time changes in a weak scaling depending on the         border again. The first pie chart in Fig. 1a corresponds
test problem. Fig. 1 breaks down the wall-clock times        to the time-step profile of an execution in the weak-
of various time step components in two-level pie charts      scaling experiment with the three-dimensional domain
for the granular gas scenario. The times are averaged        partitioning 5 × 2 × 2 on a single node of the Emmy
over all time steps and processes. The dark blue section     cluster. Fig. 1b shows the time-step profile of an exe-
corresponds to the fraction of the time in a time step       cution in the weak-scaling experiment with the three-
used for detecting and filtering contacts. The orange        dimensional domain partitioning 8 × 8 × 5 on 16 nodes.
section corresponds to the time used for initializing the    The two time slices involving communication need more
velocity accumulators and corrections. The time to re-       time in comparison to Fig. 1a, especially the framed
lax the contacts is indicated by the yellow time slice. It   slices on the second level which amount to the com-
includes the contact sweeps for all 10 iterations with-      munication. The wall-clock time for the components
out the correction reductions. The time used by all cor-     involving no communication was roughly the same in
rection reductions is shown in the green section which       both runs. The enlarged synchronization time-slices in
includes the reductions for each iteration and the re-       Fig. 1b then approximately amount to the increased
duction after the initialization. The time slice is split    time-step duration on 16 nodes. Overall, computations
up on the second level in the time used for assembling,      in the time step of this granular gas scenario prevail.
exchanging, and processing the first correction reduc-       But since the collision frequency is low, the 10 contact
tion message (dark green section) and the time used          sweeps, marked by the yellow and green sections, are
for assembling, exchanging, and processing the second        dominated by communication.
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                                                                      15

                        1         2            4       8            10        16
          nodes         20        20           20      20           20        20
                                                                                        1         2         4      8       16     32     64      128     256      512
    1D    px            1         2           4        8        10            16        20     40 80 160 320 640                         1 280   2 560   5 120    10 240
                                                                                             weak-scaling granular gas
                        4         8            10      16
          nodes         20        20           20      20
                                                                1             2         4         8         16     32      64     128    256     512
          px            2         4           5        4        5             8    10 16 20 32          40      64    80                         128
    2D    py            2         2           2        4        4             5    8     10 16 20       32      40    64                         80
                                                                              weak-scaling granular gas
                                                                                   weak-scaling hexagonal close packing
                                                                                  strong-scaling hexagonal close packing
                        8         16
          nodes         20        20
                                              1        2        4             8         16        32        64     128     256    512
          px            2         4           5        5      5    8     8    10 16 16                                     20     32
    3D    py            2         2           2        4      4    5     8    8     10 16                                  16     20
          pz            2         2           2        2      4    4     5    8     8    10                                16     16
                                                            weak-scaling granular gas
                                                                strong-scaling granular gas
                                                       (a) Domain partitionings used on the Emmy cluster.

         nodes      1        2        4           8        16       32        64        128           256        512     1 024   2 048   4 096   8 192   16 384    28 672
         px         8        16       16          32       32       64        64 128 128 256 256               512    512                        1 024   1 024     1 024
   2D    py         8        8        16          16       32       32        64 64       128 128 256          256    512                        512     1 024     1 792
                                                                                weak-scaling hexagonal close packing
                                                                               strong-scaling hexagonal close packing
         nodes      1        2        4           8        16       32        64        128           256        512     1 024   2 048   4 096   8 192   16 384    28 672
         px         4        8        8           8        16       16        16      3232   32   64      64                             64      128     128       128
   3D    py         4        4        8           8        8        16        16      3216   32   32      64                             64      64      128       128
         pz         4        4        4           8        8        8         16      1616   32   32      32                             64      64      64        112
                                                                                  weak-scaling granular gas
                                                                    strong-scaling granular gas
                                               (b) Domain partitionings used on the Juqueen supercomputer.

                        nodes             1       2    4        8        16        32        64        128       256     512     1 024   2 048   4 096   8 192
                        px                4       4    4        8        8         8
                                                                                  16 16      16    32     32                             32      64      64
               3D       py                2       4    4        4        8        88   16    16    16     32                             32      32      64
                        pz                2       2    4        4        4        88   8     16    16     16                             32      32      32
                                                                                  weak-scaling granular gas
                                                                     strong-scaling granular gas
                                              (c) Domain partitionings used on the SuperMUC supercomputer.

                             Table 2: Summary of the domain partitionings used on all test clusters.


    Fig. 2 presents time-step profiles for two weak-scaling                                                 mainly responsible for the larger time slice of the cor-
executions of the hexagonal close packing scenario. The                                                     rection reduction.
time-step profiles use the same color coding as in Fig. 1.
In contrast to the time-step profiles of the granular gas
scenario, the time step is dominated by the 100 contact
sweeps (yellow section) and the 100 correction reduc-                                                           The time-step profiles showed that for the dilute
tions (green section). Contact detection, position inte-                                                    granular gas scenario the time spent in the various time-
gration, and synchronization play a negligible role. In                                                     step components is well balanced and the time spent in
Fig. 2a the time-step profile of a weak-scaling execution                                                   the communication routines moderately increases as the
with again 20 processes on a single node of the Emmy                                                        problem size is increased. For the hexagonal close pack-
cluster is presented, whereas in Fig. 2b the time-step                                                      ings most of the time is spent in the contact sweeps and
profile of a weak-scaling execution with again 320 pro-                                                     the reduction of the velocity corrections. Components
cesses on 16 nodes is shown. The wall-clock time spent                                                      such as the position integration and the final synchro-
in the contact sweep was roughly the same in both ex-                                                       nization play a negligible role due to the higher number
ecutions, hence the increased communication costs are                                                       of iterations in comparison to the granular gas scenario.
16                                                                                                                                   Tobias Preclik, Ulrich Rüde


                                                   Granular Gas                                                     Hexagonal Close Packing
                                                   Emmy        Juqueen                            SuperMUC          Emmy           Juqueen
                                                     3           3                                      3                3
                 number of particles per process   25          10                                 10                10             103
                 number of time steps              1 000       1 000                              10 000            1 000          100
                 maximum number of particles       1.6 · 108   1.8 · 109                          1.3 · 108         1.0 · 107      1.8 · 109
                 initial number of contacts        0           0                                  0                 6.0 · 107      1.1 · 1010
                 solid volume fraction             23%         23%                                3.8%              74%            74%

                Table 3: Summary of the test problem parameters used for the weak-scaling experiments.


                                                                                                70000


                                                                                                60000




                                                                     memory bandwidth in GB/s
                                                                                                50000

            %        22                     %         30
                                                                                                40000
       .3




                                       .5
                      .9




                                                         .8
     75




                                     67
                        %




                                                           %




                                                                                                30000


                                                                                                20000


                                                                                                10000
                                                                                                                      measured bandwidth of triad (ﬁrst series)
                                                                                                                    measured bandwidth of triad (second series)
                                                                                                    0
                                                                                                            2   4    6       8     10     12       14   16        18   20
                                                                                                                             number of processes
(a) Time-step profile of the      (b) Time-step profile of the
hexagonal close packing sce-      hexagonal close packing sce-       Fig. 3: Measured bandwidth of the triad in the stream
nario executed with 5 × 2 ×       nario executed with 8 × 8 ×        benchmark computed with a varying number of cores
2 = 20 processes on a single      5 = 320 processes on 16
node.                             nodes.
                                                                     on a single node of the Emmy cluster.

Fig. 2: The time-step profiles for two weak-scaling exe-
cutions of the hexagonal close packing scenario on the               7.5.1 Granular Gas
Emmy cluster with 103 particles per process.
                                                                     First, we pay special attention to the intra-node weak-
                                                                     scaling before turning to the inter-node weak-scaling
                                                                     since the former is subject to the non-linear scaling
                                                                     behaviour of the memory bandwidth. As a test prob-
7.5 Weak-Scaling Results                                             lem we chose the granular gas scenario and as the test
                                                                     machine the Emmy cluster. A single node in the clus-
                                                                     ter is equipped with two processors each one having
In the following subsections the weak-scaling results                a single on-chip memory controller. The total memory
for both test problems on the clusters are presented.                bandwidth available to both sockets is exactly twice
Tab. 3 gives an overview of the employed parameters.                 the bandwidth of a single socket. However, for a single
The experiments differ in terms of the number of parti-              socket a simple stream benchmark [23] reveals that the
cles generated per process depending on the amount of                memory architecture is designed such that for x cores
memory available. In order to control the overall wall-              more than x1 of the socket’s total memory bandwidth is
clock time the number of time steps performed varies                 available. Fig. 3 plots the measured memory bandwidth
between 100 and 10 000. All wall-clock times presented               of computations of the triad as defined in the stream
in the following subsections correspond to the average               benchmark. The computations were performed by a
wall-clock time needed to perform a single time step                 varying number of cores in parallel. The first series of
per 1 000 particles facilitating the comparison of the               measurements minimized the number of sockets in use
charts. The wall-clock times exclude the time needed to              meaning that the processor affinities of the processes
setup the systems and generate the simulation output.                were adjusted such that all processes in measurements
The scaling experiments of the granular gas scenario on              with less or equal to 10 processes shared the same mem-
SuperMUC differs from the other granular gas experi-                 ory controller. In the second series of measurements the
ments in that the gas is considerably more dilute and a              processes were pinned to the sockets alternately such
longer period of time is simulated.                                  that 2x processes had twice the bandwidth at their dis-
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                                                                      17

                                                 0.0075                                                               main partitionings are indeed consistently slightly bet-
av. time per time step and 1000 particles in s




                                                              3D partitioning (ﬁrst series)
                                                  0.007       2D partitioning (ﬁrst series)
                                                              1D partitioning (ﬁrst series)
                                                                                                                      ter than the timings for two-dimensional domain par-
                                                 0.0065
                                                              3D partitioning (second series)
                                                              2D partitioning (second series)
                                                                                                                      titionings, which are in turn slightly better than the
                                                  0.006
                                                              1D partitioning (second series)                         timings for three-dimensional domain partitionings.
                                                 0.0055
                                                  0.005
                                                                                                                          Even though the intra-node weak-scaling results re-
                                                 0.0045
                                                  0.004
                                                                                                                      veal an underperforming parallel efficiency between 30.8%
                                                 0.0035
                                                                                                                      and 32.9% when computing on all cores of an Emmy
                                                  0.003                                                               node, the correlation with the measured memory band-
                                                 0.0025                                                               width of a triad suggests that a good intra-node scal-
                                                  0.002
                                                          1         2                4             8   10   16   20
                                                                                                                      ing can be expected as long as the available bandwidth
                                                                             number of processes                      scales. With corresponding pinning this is the case as
                                                                                                                      off the first full socket on the Emmy cluster.
Fig. 4: Intra-node weak-scaling graphs for a granular
gas on the Emmy cluster.                                                                                                  Fig. 5a extends the weak-scaling experiment to al-
                                                                                                                      most the full Emmy cluster for one-, two-, and three-
                                                                                                                      dimensional domain partitionings. The scaling experi-
posal as x processes in the first series. Indeed, the lower-                                                          ment for the one-dimensional domain partitionings per-
left part of the first series’ graph very well matches the                                                            forms best and achieves on 512 nodes a parallel effi-
second series’ graph with proper scaling. The measured                                                                ciency of 98.3% with respect to the single-node per-
bandwidth in the first series increases for an increasing                                                             formance. The time measurements for two-dimensional
number of processes until the available memory band-                                                                  domain partitionings are consistently slower, but the
width of the first memory controller is saturated. Mea-                                                               parallel efficiency does not drop below 89.7%. The time
surements with more than 10 processes start to make                                                                   measurements for three-dimensional domain partition-
use of the second memory controller and the measured                                                                  ings come in last, and the parallel efficiency goes down
bandwidth continues to increase linearly.                                                                             to 76.1% for 512 nodes. This behaviour can be explained
    An analogous behavior can be observed in the intra-                                                               by the differences in the communication volumes of
node weak-scaling graphs. Fig. 4 plots the average wall-                                                              one-, two-, and three-dimensional domain partitionings.
clock time needed for a single time step and 1 000 par-                                                               The results attest that the problem can be efficiently
ticles. In the first series of executions again the pin-                                                              scaled (almost) up to the full machine if the load per
ning strategy minimizing the number of sockets in use                                                                 process is sufficiently large.
was employed. The average wall-clock time needed per                                                                      Fig. 5b shows the results of the inter-node weak-
time step increases considerably for executions with                                                                  scaling experiments on the Juqueen supercomputer. The
up to 10 processes. However, beyond that point the                                                                    scaling experiments were only performed with the more
weak-scaling graph continues almost ideally. The sec-                                                                 demanding three-dimensional domain parititionings. In
ond series of executions used as before the pinning strat-                                                            the first series of measurements the average wall-clock
egy minimizing the maximum number of processes per                                                                    time per time step increases as expected up to 2 048 nodes.
socket meaning that executions with 2x processes in                                                                   But then the average time-step duration for setups with
the second series have twice the bandwidth at their                                                                   4 096 nodes and beyond is significantly shorter than the
disposal as the executions with x processes in the first                                                              average time-step duration with fewer nodes. The time
series. The graphs of the second series show that the                                                                 steps are even computed faster than on a single node,
wall-clock times needed per time step on 2x processes                                                                 where no inter-node communication takes place at all.
indeed closely match the wall-clock times on x processes                                                              Assuming that intra-node communication is faster than
in the first series. This indicates that our implementa-                                                              inter-node communication, this is a puzzling result. In
tion is limited by the available memory bandwidth.                                                                    fact, it turned out that the intra-node communication
    The figure also distinguishes between weak-scaling                                                                was responsible for the behaviour: The default mecha-
graphs with one-, two-, and three-dimensional domain                                                                  nism for intra-node communication is via shared mem-
partitionings since their communication volumes differ.                                                               ory on the Juqueen. In the second series of measure-
Higher-dimensional non-periodic domain partitionings                                                                  ments we disallowed the usage of shared memory for
have typically a higher communication volume in com-                                                                  intra-node communication. This resulted in the mea-
parison to lower dimensional non-periodic domain par-                                                                 surements that are consistently faster than the mea-
titionings with the same number of processes, due to                                                                  surements from the first series, and the parallel effi-
the larger area of the interfaces between the subdo-                                                                  ciency is more or less monotonically decreasing with an
mains. The plotted timings for the one-dimensional do-                                                                excellent parallel efficiency of at least 92.9%.
18                                                                                                                                                                                                                       Tobias Preclik, Ulrich Rüde

                                                                           0.009                                                                                 1.2                       fastest. The T coordinate is limited by the number of
av. time per time step and 1000 particles in s




                                                                                                   av. time per time step (3D partitioning)
                                                                                                   av. time per time step (2D partitioning)
                                                                                                   av. time per time step (1D partitioning)
                                                                                                                                                                                           processes per node, which was 64 for the above measure-
                                                                                                                                                                 1
                                                                          0.0085                   parallel eﬃciency (3D partitioning)                                                     ments. Upon creation of a three-dimensional communi-
                                                                                                                                                                                           cator, the three dimensions of the domain partition-




                                                                                                                                                                       parallel eﬃciency
                                                                                                                                                                 0.8
                                                                           0.008
                                                                                                                                                                                           ing are mapped also in row-major order. This effects, if
                                                                                                                                                                 0.6
                                                                                                                                                                                           the number of processes in z-dimension is less than the
                                                                          0.0075
                                                                                                                                                                 0.4                       number of processes per node, that a two-dimensional
                                                                           0.007
                                                                                                                                                                                           or even three-dimensional section of the domain parti-
                                                                                                                                                                 0.2
                                                                                                                                                                                           tioning is mapped to a single node. However, if the num-
                                                                          0.0065                                                                                 0
                                                                                                                                                                                           ber of processes in z-dimension is larger or equal to the
                                                                                   1       2           4        8         16     32     64     128      256   512
                                                                                                                                                                                           number of processes per node, only a one-dimensional
                                                                                                                    number of nodes
                                                                                                                                                                                           section of the domain partitioning is mapped to a single
                                                                              (a) Weak-scaling graph on the Emmy cluster.
                                                                                                                                                                                           node. A one-dimensional section of the domain parti-
                                                                           0.116                                                                                 1.2
                                                                                                                                                                                           tioning performs considerably less intra-node communi-
                         av. time per time step and 1000 particles in s




                                                                           0.114
                                                                                                                                                                                           cation than a two- or three-dimensional section of the
                                                                           0.112
                                                                                                                                                                 1                         domain partitioning. This matches exactly the situa-
                                                                            0.11                                                                                                           tion for 2 048 and 4 096 nodes. For 2 048 nodes, a two-
                                                                                                                                                                       parallel eﬃciency




                                                                                                                                                                 0.8
                                                                           0.108                                                                                                           dimensional section 1×2×32 of the domain partitioning
                                                                           0.106                                                                                 0.6                       64×64×32 is mapped to each node, and for 4 096 nodes
                                                                           0.104                                                                                                           a one-dimensional section 1 × 1 × 64 of the domain par-
                                                                                                                                                                 0.4
                                                                           0.102                                                                                                           titioning 64 × 64 × 64 is mapped to each node. To sub-
                                                                             0.1
                                                                                                              av. time per time step (ﬁrst series)               0.2                       stantiate this claim, we confirmed that the performance
                                                                           0.098                           av. time per time step (second series)                                          jump occurs when the last dimension of the domain par-
                                                                                                                parallel eﬃciency (second series)
                                                                           0.096                                                                                 0
                                                                                   1           4           16        64        256     1024     4096     16384
                                                                                                                                                                                           titioning reaches the number of processes per node, also
                                                                                                                    number of nodes                                                        when using 16 and 32 processes per node.
                                                                    (b) Weak-scaling graph on the Juqueen supercomputer.
                                                                                                                                                                                               Fig. 5c presents the weak-scaling results on the Su-
                                                                          0.0075                                                                                 1.2
                                                                                                                                                                                           perMUC supercomputer. The setup differs from the
av. time per time step and 1000 particles in s




                                                                                                                                                                                           granular gas scenario presented in Sect. 7.2.1 in that it
                                                                           0.007
                                                                                                                                                                 1                         is more dilute. The distance between the centers of two
                                                                          0.0065
                                                                                                                                                                                           granular particles along each spatial dimension is 2 cm,
                                                                                                                                                                       parallel eﬃciency




                                                                           0.006                                                                                 0.8
                                                                                                                                                                                           amounting to a solid volume fraction of 3.8% and conse-
                                                                          0.0055
                                                                                                                                                                 0.6                       quently to less collisions. As on the Juqueen supercom-
                                                                           0.005
                                                                                                                                                                                           puter only three-dimensional domain partitionings were
                                                                          0.0045                                                                                 0.4
                                                                                                                                                                                           used. All runs on up to 512 nodes were running within a
                                                                           0.004
                                                                                                                                                                 0.2                       single island. The run on 1 024 nodes also used the min-
                                                                          0.0035                                               av. time per time step
                                                                                                                                    parallel eﬃciency
                                                                                                                                                                                           imum number of 2 islands. The run on 4 096 nodes used
                                                                           0.003                                                                                 0
                                                                                   1   2               8            32         128       512      2048        8192
                                                                                                                                                                                           nodes from 9 islands, and the run on 8 192 nodes used
                                                                                                                    number of nodes                                                        nodes from 17 islands, that is both runs used one island
                           (c) Weak-scaling graph on the SuperMUC supercomputer.                                                                                                           more than required. The graph shows that most of the
                                                                                                                                                                                           performance is lost in runs on up to 512 nodes. In these
Fig. 5: Inter-node weak-scaling graphs for a granular                                                                                                                                      runs only the non-blocking intra-island communication
gas on all test machines.                                                                                                                                                                  is utilised. Thus this part of the setup is very similar
                                                                                                                                                                                           to the Emmy cluster since it also has dual-socket nodes
                                                                                                                                                                                           with Intel Xeon E5 processors and a non-blocking tree
    The reason why the measured times in the first                                                                                                                                         Infiniband network. Nevertheless, the intra-island scal-
series became shorter for 4 096 nodes and more is re-                                                                                                                                      ing results are distinctly worse. The reasons for these
vealed when considering how the processes get mapped                                                                                                                                       differences were not yet further investigated. However,
to the hardware. The default mapping on Juqueen is                                                                                                                                         the scaling behaviour beyond a single island is decent
ABCDET, where the letters A to E stand for the five                                                                                                                                        featuring a parallel efficiency of 73.8% with respect to
dimensions of the torus network, and T stands for the                                                                                                                                      a single island. A possible explanation of the under-
hardware thread within each node. The six-dimensional                                                                                                                                      performing intra-node scaling behaviour could be that
coordinates are then mapped to the MPI ranks in a                                                                                                                                          some of the Infiniband links were degraded to QDR,
row-major order, that is, the last dimension increases                                                                                                                                     which was a known problem at the time the extreme-
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                                                                                                                                    19

                                                                          0.135                                                                         1.2                       to a single node stayed above 91.4% for all measure-
av. time per time step and 1000 particles in s




                                                                                                                                                                                  ments. This result is almost as good as the 92.9% par-
                                                                           0.13                                                                         1
                                                                                                                                                                                  allel efficiency in the scaling experiments of the granu-
                                                                                                                                                                                  lar gas. The largest execution ran 1 024 × 1 792 × 1 =




                                                                                                                                                              parallel eﬃciency
                                                                          0.125                                                                         0.8

                                                                                                                                                                                  1 835 008 processes on all 28 672 nodes of the machine,
                                                                           0.12                                                                         0.6
                                                                                                                                                                                  where 10 240×17 920×10 = 1 835 008 000 particles were
                                                                          0.115                                                                         0.4                       spawned, in total leading to 10 826 547 200 ≈ 1.1 · 1010
                                                                                                                                                                                  contacts – again a possibly record-breaking number for
                                                                           0.11                                                                         0.2
                                                                                                                  average time per time step
                                                                                                                                                                                  non-smooth contact dynamics.
                                                                                                                           parallel eﬃciency
                                                                          0.105                                                                         0
                                                                                  1    2       4        8         16    32     64    128       256   512
                                                                                                            number of nodes
                                                                                                                                                                                  7.6 Strong-Scaling Results
                                                                                  (a) Weak-scaling graph on the Emmy cluster.

                                                                           1.38                                                                         1.2
                                                                                                                                                                                  In the following subsections the strong-scaling results
                         av. time per time step and 1000 particles in s




                                                                                                                                                                                  for both test problems on the clusters are presented.
                                                                           1.36
                                                                                                                                                        1                         Tab. 4 gives an overview of the employed parameters.
                                                                           1.34                                                                                                   The experiments differ in terms of the number of par-
                                                                                                                                                              parallel eﬃciency




                                                                                                                                                        0.8

                                                                           1.32
                                                                                                                                                                                  ticles generated in total and the number of time steps
                                                                                                                                                        0.6                       used for averaging. As in the weak-scaling experiments
                                                                            1.3
                                                                                                                                                                                  the granular gas scenario on SuperMUC is considerably
                                                                                                                                                        0.4
                                                                           1.28                                                                                                   more dilute than on the other machines.
                                                                                                                                                        0.2
                                                                           1.26
                                                                                                                  average time per time step
                                                                                                                           parallel eﬃciency                                      7.6.1 Granular Gas
                                                                           1.24                                                                         0
                                                                                  1        4       16        64        256    1024     4096     16384
                                                                                                            number of nodes
                                                                                                                                                                                  Fig. 7 presents the strong-scaling results of the granu-
                                                                          (b) Weak-scaling graph on the Juqueen supercomputer.
                                                                                                                                                                                  lar gas scenario on all clusters. The strong-scaling graph
Fig. 6: Inter-node weak-scaling graphs for hexagonal                                                                                                                              on the Emmy cluster is presented in Fig. 7a. A total of
close packings of spheres.                                                                                                                                                        320 × 160 × 160 = 8 192 000 particles was used, leading
                                                                                                                                                                                  to at most 64 × 80 × 80 = 409 600 particles per process
                                                                                                                                                                                  on a single node and at least 10 × 8 × 10 = 800 particles
scaling workshop took place. The communication rou-                                                                                                                               per process on 512 nodes. The speedup is ideal for up to
tines then need 54 ·· 64
                      66 ≈ 1.21 times longer to complete.
                                                                                                                                                                                  64 nodes and then gradually becomes more inefficient.
This could also explain the high variability of the runs’                                                                                                                         However, no turnover is observed. Some time measure-
wall-clock times.                                                                                                                                                                 ments exceed the optimal speedup, which can happen
    Subsequently, a second series of measurements was                                                                                                                             for example if the problem becomes small enough to fit
performed with 603 non-spherical particles per process.                                                                                                                           into one of the caches. In conclusion, the scaling experi-
The scaling behaviour is comparable to the scaling be-                                                                                                                            ments for this dilute setup on the Emmy cluster suggest
haviour observed in Fig. 5c. However, the largest weak-                                                                                                                           that one obtains a satisfactory parallel efficiency on the
scaling run simulated 28 311 552 000 ≈ 2.8 · 1010 non-                                                                                                                            whole cluster, as long as several thousand particles are
spherical particles – a possibly record-breaking number                                                                                                                           present per process.
for non-smooth contact dynamics.                                                                                                                                                       Fig. 7b presents the results of the strong-scaling ex-
                                                                                                                                                                                  periments on the Juqueen supercomputer for the gran-
7.5.2 Hexagonal Close Packings of Spheres                                                                                                                                         ular gas. The total number of particles was 32 768 000
                                                                                                                                                                                  particles. In the execution on 32 nodes each of the
Fig. 6a shows the average wall-clock time needed for a                                                                                                                            16×16×8 = 2 048 processes initially had 20×20×40 =
single time step in the hexagonal close packing test on                                                                                                                           16 000 non-spherical particles, and in the execution on
the Emmy cluster. The parallel efficiency with respect                                                                                                                            4 096 nodes each of the 64 × 64 × 64 = 262 144 pro-
to a single node remains above 79.9% for all execu-                                                                                                                               cesses spawned 5 × 5 × 5 = 125 particles. The parallel
tions. This is slightly better than the parallel efficiency                                                                                                                       efficiency is plotted with respect to 32 nodes and stays
of 76.1% for the granular gas.                                                                                                                                                    above 80.7% for up to 1 024 nodes and 500 particles
    The weak-scaling results of the hexagonal close pack-                                                                                                                         per process before rapidly decreasing. On 4 096 nodes
ing scenario on the Juqueen supercomputer are pre-                                                                                                                                the efficiency is at 55.4%. The weak- and strong-scaling
sented in Fig. 6b. The parallel efficiency with respect                                                                                                                           results are both better in comparison to the Emmy clus-
20                                                                                                                                                           Tobias Preclik, Ulrich Rüde


                                                         Granular Gas                                                                            Hexagonal Close Packing
                                                         Emmy                               Juqueen                            SuperMUC          Emmy               Juqueen
             number of particles                         320 × 160 × 160                    320 × 320 × 320                    128 × 128 × 128   1 280 × 640 × 10   2 048 × 2 048 × 10
             number of time steps                        1 000                              1 000                              100               50                 20
             solid volume fraction                       23%                                23%                                3.8%              74%                74%

                         Table 4: Summary of the test problem parameters used for the strong-scaling experiments.


              512                                                                                    1.2                       ter, owed to the torus network which performs excellent
              256                                                                                                              for the nearest-neighbor communication.
                                                                                                     1
              128                                                                                                                   The results of the strong-scaling experiments on the
                                                                                                                               SuperMUC supercomputer are shown in Fig. 7c. In to-


                                                                                                           parallel eﬃciency
               64                                                                                    0.8

                                                                                                                               tal 1283 non-spherical particles were simulated. Hence,
   speedup




               32
                                                                                                     0.6
               16                                                                                                              in the single-node run each process owned 32×64×64 =
                8                                                                                    0.4                       131 072 particles, and in the run on 1 024 nodes, each
                4                                                                                                              process owned 8 × 4 × 4 = 128 particles. The parallel
                                                                           ideal speedup             0.2
                2                                                                 speedup
                                                                                                                               efficiency is at 90.0% on 256 nodes. Beyond that point
                                                                        parallel eﬃciency                                      it decreases dramatically, indicating that the scaling is
                1                                                                                    0
                    1    2            4         8        16        32        64     128     256   512
                                                                                                                               fine as long as at least about 500 particles are present
                                                    number of nodes
                                                                                                                               per process.
                    (a) Strong-scaling graph on the Emmy cluster.
                                                                                                                               7.6.2 Hexagonal Close Packings of Spheres
              128                                                                                    1.2


               64
                                                                                                     1                         In the strong-scaling experiment on the Emmy cluster
               32
                                                                                                                               in total 1 280 × 640 × 10 = 8 192 000 particles were gen-
                                                                                                           parallel eﬃciency




                                                                                                     0.8
                                                                                                                               erated. The experiment was run for 1 to 512 nodes, such
               16
   speedup




                                                                                                     0.6
                                                                                                                               that the smallest setup with 5 × 4 × 1 = 20 processes on
                8                                                                                                              a single node generated 256 × 160 × 10 = 409 600 spher-
                                                                                                     0.4                       ical particles per process, and the largest setup with
                4

                                                                                                     0.2
                                                                                                                               128 × 80 × 1 = 10 240 processes on 512 nodes generated
                2                                                          ideal speedup
                                                                                  speedup                                      10 × 8 × 10 = 800 particles per process. Fig. 8a presents
                                                                        parallel eﬃciency
                1                                                                                    0                         the results. A super-linear speedup is observed for sev-
                    32       64           128        256           512        1024        2048    4096
                                                    number of nodes                                                            eral executions, which is likely due to caching effects,
          (b) Strong-scaling graph on the Juqueen supercomputer.                                                               since the working set size becomes very small. In the
                                                                                                                               strong-scaling experiment for 512 nodes of the granu-
             1024                                                                                    1.2                       lar gas scenario on Emmy also only 800 particles were
              512                                                                                                              generated per process. However, the computational in-
                                                                                                     1
              256                                                                                                              tensity here is much higher in comparison to that of the
              128                                                                                                              granular gas, because far more contacts have to be re-
                                                                                                           parallel eﬃciency




                                                                                                     0.8
               64                                                                                                              solved. This explains the high parallel efficiency of 113%
speedup




               32                                                                                    0.6
                                                                                                                               in comparison to the disappointing parallel efficiency of
               16
                                                                                                     0.4
                                                                                                                               37.7% from Fig. 7a. In conclusion, the scaling experi-
                8
                                                                                                                               ments suggest that a few hundred particles per process
                4
                                                                           ideal speedup             0.2                       are enough to achieve a very good parallel efficiency on
                2                                                                 speedup
                                                                        parallel eﬃciency                                      the Emmy cluster if the granular flow is dense.
                1                                                                                    0
                    1    2        4        8        16        32        64    128    256    512   1024                             For the strong-scaling experiment on the Juqueen
                                                    number of nodes
                                                                                                                               supercomputer a hexagonal close packing with 41 943 040 par-
  (c) Strong-scaling graph on the SuperMUC supercomputer.                                                                      ticles in total was created. The smallest execution ran
                                                                                                                               64 × 32 × 1 = 2 048 processes on 32 nodes, where 32 ×
Fig. 7: Strong-scaling graphs for a granular gas test
                                                                                                                               64 × 10 = 20 480 spherical particles were generated per
problem on all test machines.
                                                                                                                               process. The largest execution ran 512 × 512 × 1 =
                                                                                                                               262 144 processes on 4 096 nodes, where 4 × 4 × 10 =
                                                                                                                               160 particles were generated per process. Fig. 8b shows
Ultrascale Simulations of Non-smooth Granular Dynamics                                                                                                                     21


           512                                                                           1.2                       ing the same structure as a multi-contact problem that
           256                                                                                                     is solved sequentially. Particles with multiple contacts
                                                                                         1
           128                                                                                                     that are associated with different subdomains are du-
                                                                                                                   plicated, similar to shadow copies used in this article.




                                                                                               parallel eﬃciency
            64                                                                           0.8

                                                                                                                   However, the mass and inertia are split among all in-
speedup




            32
                                                                                         0.6
            16                                                                                                     stantiations. The coupling is recovered by adding linear
             8                                                                           0.4                       equations gluing the duplicates back together through
             4
                                                                                                                   additional Lagrange multipliers. In contrast to the con-
                                                               ideal speedup             0.2
             2                                                        speedup
                                                                                                                   tact constraints, the interface equations are linear, and
                                                            parallel eﬃciency                                      a block-diagonal system of linear equations must be
             1                                                                           0
                 1    2        4         8      16     32      64     128       256   512
                                                                                                                   solved after several sweeps over all contacts. In [39], the
                                             number of nodes
                                                                                                                   authors present simulations with up to 2 · 105 spher-
                  (a) Strong-scaling graph on the Emmy cluster.
                                                                                                                   ical particles and 2 · 106 contacts, time-integrated on
           128                                                                           1.2
                                                                                                                   up to 100 processes. The NSCDD allows non-nearest-
                                                                                                                   neighbor communication in order to allow enlarged rigid
            64
                                                                                         1                         bodies instead of introducing a concept analogous to
            32                                                                                                     global bodies.
                                                                                               parallel eﬃciency




                                                                                         0.8

            16
                                                                                                                        Prior to Visseq et al., Koziara et al. presented the
speedup




                                                                                         0.6                       parallelization implemented in the solfec code [20]. This
             8
                                                                                                                   approach dispenses with the separation into interface
                                                                                         0.4
             4                                                                                                     problems and local multi-contact problems. A classic
             2                                                 ideal speedup             0.2                       NBGS is parallelized with a non-negligible but inevitable
                                                                      speedup
                                                            parallel eﬃciency                                      amount of serialization. Bodies are instantiated redun-
             1                                                                           0
                 32       64       128        256      512       1024       2048      4096                         dantly on all processes, prohibiting scaling beyond the
                                             number of nodes                                                       memory limit. Instead of using accumulator and correc-
          (b) Strong-scaling graph on the Juqueen supercomputer.                                                   tion variables, as proposed in this paper, the authors
                                                                                                                   synchronize dummy particles (particles that are in con-
Fig. 8: Strong-scaling graphs for hexagonal close pack-                                                            tact with shadow copies or original instances) in ad-
ings of spheres.                                                                                                   dition to shadow copies in order to implement contact
                                                                                                                   shadow copies. As in the NSCDD, the system matrix
the speedup and the parallel efficiency on the second                                                              (Delassus operator) is set up explicitly instead of using
axis, both with respect to 32 nodes. A parallel effi-                                                              matrix-free computations as proposed here. Simulations
ciency of 75.0% on 4 096 nodes is achieved, where only                                                             are presented with up to 1 · 104 polyhedral particles or
160 particles were owned per process. This suggests that                                                           6 · 105 contacts time-integrated on up to 64 processes.
a reasonable good efficiency can be achieved for a dense                                                                At the same time, Shojaaee et al. presented another
setup on the Juqueen supercomputer, as long as several                                                             domain partitioning method in [34]. The presentation
hundred particles are created per process.                                                                         is restricted to two-dimensional problems. The solver
                                                                                                                   in the paper corresponds to a subdomain NBGS with
                                                                                                                   relaxation parameter ω = 1, where the authors argue
8 Related Work                                                                                                     that divergence does typically not occur. At least for
                                                                                                                   three-dimensional simulations this is in our experience
Other authors have proposed approaches for paralleliz-                                                             not sufficient. Shadow copies are created not only if the
ing non-smooth contact dynamics on architectures with                                                              hulls overlap the neighboring subdomain but also if the
distributed memory. All of them are based on domain                                                                particles approach the subdomain boundaries, simpli-
partitionings. A parallelization strategy termed non-                                                              fying the intersection testing but introducing excessive
smooth contact domain decomposition (NSCDD) im-                                                                    shadow copies. Shojaaee et al. also introduce contact
plemented in the renowned LMGC90 code was lately                                                                   shadow copies instead of using accumulator and cor-
presented in [38, 39] by Visseq et al. The approach                                                                rection variables as proposed here. Simulations are pre-
is inspired by the finite element tearing and intercon-                                                            sented with up to 1 · 106 circular particles in a dense
nect (FETI) method for solving partial differential equa-                                                          packing on up to 256 processes.
tions in computational mechanics. The authors sug-                                                                      The approach presented in this paper improves in
gest to decouple the multi-contact problem such that                                                               general the robustness and scalability of previously pub-
on each process a multi-contact problem is solved hav-                                                             lished parallel algorithms. The matrix-free approach fa-
22                                                                                           Tobias Preclik, Ulrich Rüde


cilitates the evaluation of the particle wrenches in par-      of accumulators and correction variables enables the
allel as suggested in Sect. 6.3 and thus reduces the           evaluation of the particle wrenches in parallel, reuses
amount of communicated data. The separation of bod-            partial results and reduces the number of particles that
ies into global and local bodies allows to restrict message-   need to be synchronized.
exchange communications to nearest neighbors as de-                The integration of the positions and orientations is
tailed in Sect. 6.4 and thus maps well to various in-          entailed by the execution of an exceptionally robust
terconnect networks. Furthermore, the synchronization          synchronization protocol. The key to obtain this ro-
protocol defined in Sect. 6.2 and Sect. 6.5 is not suscep-     bustness is to add the rank of the parent process and
tible to numerical errors in contrast to the conventional      the ranks of the shadow copy holders to the state of
rules which are based on contact locations. Last but not       each particle and to explicitly communicate the state
least the scaling experiments from Sect. 7 with up to          changes. Only then processes can reliably agree upon
2.8 · 1010 non-spherical particles or 1.1 · 1010 contacts on   responsibilities such as contact treatment and particle
up to 1.8 · 106 processes exceed all previously published      integration without being susceptible to numerical er-
numbers by a factor of 103 to 104 .                            rors.
                                                                   Beyond that, all messages are aggressively aggre-
9 Summary                                                      gated in order to reduce the communication overhead of
                                                               small messages and all messages are restricted to near-
This article presents models and algorithms for per-           est neighbors. The latter is achieved by splitting bodies
forming scalable direct numerical simulations of gran-         into local and global bodies and identifying appropriate
ular matter in hard contact as we implemented them             requirements. Both measures improve the scalability of
in the pe open-source software framework for massively         the implementation.
parallel simulations of rigid bodies. The pe framework
                                                               Finally, the scalability was demonstrated for dilute
already has been successfully used to simulate granu-
                                                           and dense setups on three clusters, two of them having
lar systems with and without surrounding fluid in the
                                                           been in the top 10 of the world’s largest publicly avail-
past [12, 6].
                                                           able supercomputers. The parallel efficiency on Juqueen
    The discretization of the equations of motion un-
                                                           is outstanding. T he inter-island scaling results on Su-
derlying the time-stepping scheme use an integrator
                                                           perMUC are satisfactory, however, the intra-island scal-
of order one. Contacts are modelled as inelastic and
                                                           ing results show room for improvement. That this is not
hard contacts with Coulomb friction. The hard con-
                                                           inherently caused by the parallelization approach can
tact model avoids the necessity to resolve the collision
                                                           be seen by inspecting the results of the Emmy cluster,
micro-dynamics and the time-stepping scheme avoids
                                                           whose architecture is close to a single island of Super-
the necessity to resolve impulsive events in time. The
                                                           MUC.
one-step integration can be split into the integration
of the velocities and the subsequent integration of the        The largest scaling experiments demonstrate that
positions and orientations.                                simulations  of unprecedented scale with up to 2.8 · 1010
    The velocity integration requires the solution of a    non-spherical particles and up to 1.1 · 1010 contacts are
non-linear system of equations per time step. In or-       possible using up to 1.8 · 106 processes. The systmatic
der to reduce the size of the system in the first place    evaluation also confirms that good parallel efficiency
conventional broad-phase contact detection algorithms      can be expected on millions of processes even if only
are applied to exclude contacts between intersection       a few hundred particles are allocated to each process
hulls. To solve the non-linear system of equations the     provided that the computation exhibits a sufficiently
subdomain non-linear block Gauss-Seidel is used. The       high computational intensity and the architecture has
numerical solution algorithm is a mixture between a        a good interconnect network .
non-linear block Gauss-Seidel (NBGS) and a non-linear          The favourable scalability results do not account for
block Jacobi with underrelaxation. In contrast to a pure   the fact that the NBGS solver does not scale (algorith-
non-linear block Jacobi it only requires a mild under-     mically) in terms of the number of iterations needed to
relaxation and in contrast to a non-linear block Gauss-    achieve a given error bound. Possible future develop-
Seidel it accommodates the subdomain structure of the      ments arise out of that: The convergence rate of multi-
domain partitioning and thus allows an efficient par-      grid methods is independent of the number of unknowns
allelization avoiding irregular data dependencies across   and is in that sense optimal. A successful construction
subdomains. The implementation of the subdomain NBGS of such a multigrid method for hard contact problems
in the pe is matrix-free and thus avoids the expensive as- would be invaluable for simulating every-increasing sys-
sembly of the Delassus operator. Furthermore, the use      tem sizes.
Ultrascale Simulations of Non-smooth Granular Dynamics                                                          23


References                                                 15. Iglberger K, Rüde U (2009) Massively parallel rigid
                                                               body dynamics simulations. Computer Science-
 1. Anitescu M, Potra F (1997) Formulating dynamic             Research and Development 23(3-4):159–167
    multi-rigid-body contact problems with friction as     16. Iglberger K, Rüde U (2010) Massively parallel
    solvable linear complementarity problems. Nonlin-          granular flow simulations with non-spherical parti-
    ear Dynamics 14(3):231–247                                 cles. Computer Science-Research and Development
 2. Anitescu M, Potra F (2002) A time-stepping                 25(1-2):105–113
    method for stiff multibody dynamics with contact       17. Iglberger K, Rüde U (2011) Large-scale rigid
    and friction. International Journal for Numerical          body simulations. Multibody System Dynamics
    Methods in Engineering 55(7):753–784                       25(1):81–95
 3. Anitescu M, Tasora A (2010) An iterative approach      18. Jean M (1999) The non-smooth contact dynamics
    for cone complementarity problems for nonsmooth            method. Computer Methods in Applied Mechanics
    dynamics. Computational Optimization and Appli-            and Engineering 177(3–4):235–257
    cations 47(2):207–235                                  19. Kollmer J, Sack A, Heckel M, Pöschel T (2013)
 4. van den Bergen G (1999) A fast and robust GJK              Relaxation of a spring with an attached granular
    implementation for collision detection of convex ob-       damper. New Journal of Physics 15(9):093,023
    jects. Journal of Graphics Tools 4(2):7–25             20. Koziara T, Bićanić N (2011) A distributed memory
 5. van den Bergen G (2001) Proximity queries and              parallel multibody contact dynamics code. Interna-
    penetration depth computation on 3D game ob-               tional Journal for Numerical Methods in Engineer-
    jects. In: Game Developers Conference, vol 170             ing 87(1–5):437–456
 6. Bogner S, Mohanty S, Rüde U (2015) Drag correla-      21. Leyffer S (2006) Complementarity constraints as
    tion for dilute and moderately dense fluid-particle        nonlinear equations: Theory and numerical experi-
    systems using the lattice boltzmann method. Inter-         ence. In: Optimization with Multivalued Mappings,
    national Journal of Multiphase Flow 68(0):71–79            Springer, pp 169–208
 7. Bonnefon O, Daviet G (2011) Quartic formulation        22. Liu C, Jain S (2012) A quick tutorial on multibody
    of Coulomb 3D frictional contact. Technical Report         dynamics. Tech. rep., Georgia Institute of Technol-
    RT-0400, INRIA                                             ogy
 8. Chen D, Eisley N, Heidelberger P, Senger R, Sug-       23. McCalpin J (1995) Memory bandwidth and ma-
    awara Y, Kumar S, Salapura V, Satterfield D,               chine balance in current high performance comput-
    Steinmacher-Burow B, Parker J (2012) The IBM               ers. IEEE Computer Society Technical Committee
    Blue Gene/Q interconnection fabric. IEEE Micro             on Computer Architecture (TCCA) Newsletter pp
    32(1):32–43                                                19–25
 9. Cohen J, Lin M, Manocha D, Ponamgi M (1995) I-         24. McNamara S, Young W (1994) Inelastic collapse in
    COLLIDE: An interactive and exact collision detec-         two dimensions. Physical Review E 50(1):R28–R31
    tion system for large-scale environments. In: Pro-     25. Miller S, Luding S (2004) Event-driven molecu-
    ceedings of the 1995 symposium on Interactive 3D           lar dynamics in parallel. Journal of Computational
    graphics, ACM, pp 189–ff                                   Physics 193(1):306–316
10. Diebel J (2006) Representing attitude: Euler an-       26. Mitarai N, Nakanishi H (2012) Granular flow: Dry
    gles, unit quaternions, and rotation vectors               and wet. The European Physical Journal Special
11. Esefeld B (2014) Numerische Integration von                Topics 204(1):5–17
    Mehrkörpersystemen mit mengenwertigen Kraftge-        27. Moreau J, Panagiotopoulos P (1988) Nonsmooth
    setzen. Herbert Utz Verlag                                 Mechanics and Applications, vol 302. Springer
12. Fischermeier E, Bartuschat D, Preclik T, Marechal      28. Negrut D, Tasora A, Mazhar H, Heyn T, Hahn P
    M, Mecke K (2014) Simulation of a hard-                    (2012) Leveraging parallel computing in multibody
    spherocylinder liquid crystal with the pe. Computer        dynamics. Multibody System Dynamics 27(1):95–
    Physics Communications 185(12):3156–3161                   117
13. Gilbert E, Johnson D, Keerthi S (1988) A fast pro-     29. Popa C, Preclik T, Rüde U (2014) Regularized so-
    cedure for computing the distance between complex          lution of LCP problems with application to rigid
    objects in three-dimensional space. IEEE Journal of        body dynamics. Numerical Algorithms pp 1–12
    Robotics and Automation 4(2):193–203                   30. Sauer J, Schömer E (1998) A constraint-based ap-
14. Gilge M, et al (2013) IBM System Blue Gene Solu-           proach to rigid body dynamics for virtual reality
    tion Blue Gene/Q Application Development. IBM              applications. In: Proceedings of the ACM Sympo-
    Redbooks                                                   sium on Virtual Reality Software and Technology,
24                                                          Tobias Preclik, Ulrich Rüde


    pp 153–162
31. Schindler T, Acary V (2014) Timestepping schemes
    for nonsmooth dynamics based on discontinuous
    Galerkin methods: Definition and outlook. Mathe-
    matics and Computers in Simulation 95(0):180–199
32. Schütte K, van der Waerden B (1952) Das Prob-
    lem der dreizehn Kugeln. Mathematische Annalen
    125(1):325–334
33. Shen Y, Stronge W (2011) Painlevé paradox during
    oblique impact with friction. European Journal of
    Mechanics - A/Solids 30(4):457–467
34. Shojaaee Z, Shaebani M, Brendel L, Török J, Wolf
    D (2012) An adaptive hierarchical domain decom-
    position method for parallel contact dynamics sim-
    ulations of granular materials. Journal of Compu-
    tational Physics 231(2):612–628
35. Spahn F, Petzschmann O, Schmidt J, Sremčević M,
    Hertzsch JM (2001) Granular viscosity, planetary
    rings and inelastic particle collisions. In: Granular
    Gases, Springer, pp 363–385
36. Studer C (2009) Numerics of Unilateral Contacts
    and Friction: Modeling and Numerical Time Inte-
    gration in Non-smooth Dynamics, Lecture Notes
    in Applied and Computational Mechanics, vol 47.
    Springer
37. Tasora A, Anitescu M (2011) A matrix-free
    cone complementarity approach for solving large-
    scale, nonsmooth, rigid body dynamics. Computer
    Methods in Applied Mechanics and Engineering
    200(5):439–453
38. Visseq V, Martin A, Dureisseix D, Dubois F,
    Alart P (2012) Distributed nonsmooth contact do-
    main decomposition (NSCDD): Algorithmic struc-
    ture and scalability. In: Proceedings of the Interna-
    tional Conference on Domain Decomposition Meth-
    ods
39. Visseq V, Alart P, Dureisseix D (2013) High per-
    formance computing of discrete nonsmooth con-
    tact dynamics with domain decomposition. Inter-
    national Journal for Numerical Methods in Engi-
    neering 96(9):584–598
40. Wautelet P, Boiarciuc M, Dupays J, Giuliani S,
    Guarrasi M, Muscianisi G, Cytowski M (2014) Best
    Practice Guide – Blue Gene/Q. v1.1.1 edn
41. van der Weele K, van der Meer D, Versluis M, Lohse
    D (2001) Hysteretic clustering in granular gas. Eu-
    rophysics Letters 53(3):328
