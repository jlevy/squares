3rd Workshop in Virtual Reality Interactions and Physical Simulation "VRIPHYS" (2006)
C. Mendoza, I. Navazo (Editors)




                                               Position Based Dynamics

                                       Matthias Müller Bruno Heidelberger Marcus Hennix John Ratcliff

                                                                   AGEIA




        Abstract

        The most popular approaches for the simulation of dynamic systems in computer graphics are force based. Internal
        and external forces are accumulated from which accelerations are computed based on Newton’s second law of
        motion. A time integration method is then used to update the velocities and finally the positions of the object.
        A few simulation methods (most rigid body simulators) use impulse based dynamics and directly manipulate
        velocities. In this paper we present an approach which omits the velocity layer as well and immediately works
        on the positions. The main advantage of a position based approach is its controllability. Overshooting problems
        of explicit integration schemes in force based systems can be avoided. In addition, collision constraints can be
        handled easily and penetrations can be resolved completely by projecting points to valid locations. We have used
        the approach to build a real time cloth simulator which is part of a physics software library for games. This
        application demonstrates the strengths and benefits of the method.
        Categories and Subject Descriptors (according to ACM CCS): I.3.5 [Computer Graphics]: Computational Geometry
        and Object ModelingPhysically Based Modeling; I.3.7 [Computer Graphics]: Three-Dimensional Graphics and
        RealismAnimation and Virtual Reality




1. Introduction                                                         ing the density or lumped masses of vertices, the forces are
                                                                        transformed into accelerations. Any time integration scheme
Research in the field of physically based animation in com-
                                                                        can then be used to first compute the velocities from the ac-
puter graphics is concerned with finding new methods for
                                                                        celerations and then the positions from the velocities. Some
the simulation of physical phenomena such as the dynamics
                                                                        approaches use impulses instead of forces to control the an-
of rigid bodies, deformable objects or fluid flow. In contrast
                                                                        imation. Because impulses directly change velocities, one
to computational sciences where the main focus is on accu-
                                                                        level of integration can be skipped.
racy, the main issues here are stability, robustness and speed
while the results should remain visually plausible. There-                  In computer graphics and especially in computer games
fore, existing methods from computational sciences can not              it is often desirable to have direct control over positions of
be adopted one to one. In fact, the main justification for              objects or vertices of a mesh. The user might want to attach
doing research on physically based simulation in computer               a vertex to a kinematic object or make sure the vertex always
graphics is to come up with specialized methods, tailored to            stays outside a colliding object. The method we propose here
the particular needs in the field. The method we present falls          works directly on positions which makes such manipula-
into this category.                                                     tions easy. In addition, with the position based approach it is
   The traditional approach to simulating dynamic objects               possible to control the integration directly thereby avoiding
has been to work with forces. At the beginning of each time             overshooting and energy gain problems in connection with
step, internal and external forces are accumulated. Examples            explicit integration. So the main features and advantages of
of internal forces are elastic forces in deformable objects or          position based dynamics are
viscosity and pressure forces in fluids. Gravity and collision
forces are examples of external forces. Newton’s second law             • Position based simulation gives control over explicit inte-
of motion relates forces to accelerations via the mass. So us-            gration and removes the typical instability problems.

c The Eurographics Association 2006.
°
                                              M. Müller et al. / Position Based Dynamics




              Figure 1: A known deformation benchmark test, applied here to a cloth character under pressure.



• Positions of vertices and parts of objects can directly be          cloth simulation [BFA02] and combine it with a geomet-
  manipulated during the simulation.                                  ric collision resolving algorithm based on positions to make
• The formulation we propose allows the handling of gen-              sure that the collision resolving impulses are kept within sta-
  eral constraints in the position based setting.                     ble bounds. The same holds for the kinematical collision cor-
• The explicit position based solver is easy to understand            rection step proposed by Volino et al. [VCMT95].
  and implement.                                                         A position based approach has been used by Clavet et
                                                                      al. [CBP05] to simulate viscoelastic fluids. Their approach
                                                                      is not fully position based because the time step appears in
2. Related Work
                                                                      various places of their position projections. Thus, the inte-
The recent state of the art report [NMK∗ 05] gives a good             gration is only conditionally stable as regular explicit inte-
overview of the methods used in computer graphics to simu-            gration.
late deformable objects, e.g. mass-spring systems, the finite            Müller et al. [MHTG05] simulate deformable objects
element method or finite difference approaches. Apart from            by moving points towards certain goal positions which are
the citation of [MHTG05], position based dynamics does not            found by matching the rest state to the current state of the
appear in this survey. However, parts of the position based           object. Their integration method is the closest to the one we
approach have appeared in various papers without naming it            propose here. They only treat one specialized global con-
explicitly and without defining a complete framework.                 straint and, therefore, do not need a position solver.
   Jakobsen [Jak01] built his Fysix engine on a position                 Fedor [Fed05] uses Jakobsen’s approach to simulate char-
based approach. His central idea was to use a Verlet inte-            acters in games. His method is tuned to the particular prob-
grator and manipulate positions directly. Because velocities          lem of simulating human characters. He uses several skeletal
are implicitly stored by current and the previous positions,          representations and keeps them in sync via projections.
the velocities are implicitly updated by the position manip-             Faure [Fau98] uses a Verlet integration scheme by modi-
ulation. While he focused mainly on distance constraints,             fying the positions rather than the velocities. New positions
he only gave vague hints on how more general constraints              are computed by linearizing the constraints while we work
could be handled. In this paper we present a fully general            with the non linear constraint functions directly.
approach which handles general constraints. We also focus
on the important issue of conservation of linear and angu-               We define general constraints via a constraint function
lar momenta by position projection. We work with explicit             as [BW98] and [THMG04]. Instead of computing forces as
velocities instead of storing previous positions which makes          the derivative of a constraint function energy, we directly
damping and friction simulation much easier.                          solve for the equilibrium configuration and project positions.
                                                                      With our method we derive a bending term for cloth which
   Desbrun [DSB99] and Provot [Pro95] use constraint pro-             is similar to the one proposed in [GHDS03] and [BMF03]
jection in mass spring systems to prevent springs from over-          but adopted to the point based approach.
stretching. In contrast to a full position based approach, pro-
                                                                         In Section 4 we use the position based dynamics approach
jection is only used as a polishing process for those springs
                                                                      for the simulation of cloth. Cloth simulation has been an ac-
that are stretched too much and not as the basic simulation
                                                                      tive research field in computer graphics in recent years. In-
method.
                                                                      stead of citing the key papers of the field individually we
  Bridson et al. use a traditional force based approach for           refer the reader to [NMK∗ 05] for a comprehensive survey.

                                                                                                        c The Eurographics Association 2006.
                                                                                                        °
                                                            M. Müller et al. / Position Based Dynamics

3. Position Based Simulation                                                        in exact correspondence with a Verlet integration step and
                                                                                    a modification of the current position [Jak01], because the
In this section we will formulate the general position based
                                                                                    Verlet method stores the velocity implicitly as the difference
approach. With cloth simulation, we will give a particular
                                                                                    between the current and the last position. However, working
application of the method in the subsequent and in the results
                                                                                    with velocities allows for a more intuitive way of manipulat-
section. We consider a three dimensional world. However,
                                                                                    ing them.
the approach works equally well in two dimensions.
                                                                                        The velocities are manipulated in line (5), (6) and (16).
3.1. Algorithm Overview                                                             Line (5) allows to hook up external forces to the system if
                                                                                    some of the forces cannot be converted to positional con-
We represent a dynamic object by a set of N vertices and M                          straints. We only use it to add gravity to the system in which
constraints. A vertex i ∈ [1, . . . , N] has a mass mi , a position                 case the line becomes vi ← vi + ∆tg, where g is the gravita-
xi and a velocity vi .                                                              tional acceleration. In line (6), the velocities can be damped
   A constraint j ∈ [1, . . . , M] consists of                                      if this is necessary. In Section 3.5 we show how to add global
                                                                                    damping without influencing the rigid body modes of the
• a cardinality n j ,
                                                                                    object. Finally, in line (16), the velocities of colliding ver-
• a function C j : R3n j → R,
                                                                                    tices are modified according to friction and restitution coef-
• a set of indices {i1 , . . . in j }, ik ∈ [1, . . . N],
                                                                                    ficients.
• a stiffness parameter k j ∈ [0 . . . 1] and
• a type of either equality or inequality.                                             The given constraints C1 , . . . ,CM are fixed throughout the
                                                                                    simulation. In addition to these constraints, line (8) generates
    Constraint j with type equality is satisfied if
                                                                                    the Mcoll collision constraints which change from time step
C j (xi1 , . . . , xin j ) = 0. If its type is inequality then it is
                                                                                    to time step. The projection step in line (10) considers both,
satisfied if C j (xi1 , . . . , xin j ) ≥ 0. The stiffness parameter k j            the fixed and the collision constraints.
defines the strength of the constraint in a range from zero to
one.                                                                                   The scheme is unconditionally stable. This is because the
                                                                                    integration steps (13) and (14) do not extrapolate blindly
   Based on this data and a time step ∆t, the dynamic object                        into the future as traditional explicit schemes do but move
is simulated as follows:                                                            the vertices to a physically valid configuration pi computed
(1) forall vertices i                                                               by the constraint solver. The only possible source for insta-
(2)    initialize xi = x0i , vi = v0i , wi = 1/mi                                   bilities is the solver itself which uses the Newton-Raphson
(3) endfor                                                                          method to solve for valid positions (see Section 3.3). How-
(4) loop                                                                            ever, its stability does not depend on the time step size but
(5)    forall vertices i do vi ← vi + ∆twi fext (xi )                               on the shape of the constraint functions.
(6)    dampVelocities(v1 , . . . , vN )                                  The integration does not fall clearly into the category
(7)    forall vertices i do pi ← xi + ∆tvi                            of implicit or explicit schemes. If only one solver iteration
(8)    forall vertices i do generateCollisionConstraints(xi → pi ) is performed per time step, it looks more like an explicit
(9)    loop solverIterations times                                    scheme. By increasing the number of iterations, however, a
(10)      projectConstraints(C1 , . . . ,CM+Mcoll , p1 , . . . , pN ) constrained system can be made arbitrarily stiff and the al-
(11) endloop                                                          gorithm behaves more like an implicit scheme. Increasing
(12) forall vertices i                                                the number of iterations shifts the bottleneck from collision
(13)      vi ← (pi − xi )/∆t                                          detection to the solver.
(14)      xi ← pi
(15) endfor
(16) velocityUpdate(v1 , . . . , vN )                                 3.2. The Solver
(17) endloop                                                          The input to the solver are the M + M         constraints and
                                                                                                                                coll
                                                                                    the estimates p1 , . . . , pN for the new locations of the points.
   Lines (1)-(3) just initialize the state variables. The core                      The solver tries to modify the estimates such that they sat-
idea of position based dynamics is shown in lines (7), (9)-                         isfy all the constraints. The resulting system of equations
(11) and (13)-(14). In line (7), estimates pi for new locations                     is non-linear. Even a simple distance constraint C(p1 , p2 ) =
of the vertices are computed using an explicit Euler inte-                          |p1 − p2 | − d yields a non-linear equation. In addition, the
gration step. The iterative solver (9)-(11) manipulates these                       constraints of type inequality yield inequalities. To solve
position estimates such that they satisfy the constraints. It                       such a general set of equations and inequalities, we use a
does this by repeatedly project each constraint in a Gauss-                         Gauss-Seidel-type iteration. The original Gauss-Seidel al-
Seidel type fashion (see Section 3.2). In steps (13) and (14),                      gorithm (GS) can only handle linear system. The part we
the positions of the vertices are moved to the optimized es-                        borrow from GS is the idea of solving each constraint inde-
timates and the velocities are updated accordingly. This is                         pendently one after the other. However, in contrast to GS,

c The Eurographics Association 2006.
°
                                                   M. Müller et al. / Position Based Dynamics

solving a constraint is a non linear operation. We repeat-                                                                     ∆p2
edly iterate through all the constraints and project the par-                                                      d                  m2
                                                                                                ∆p1                                  p2
ticles to valid locations with respect to the given constraint
alone. In contrast to a Jacobi-type iteration, modifications to                         m1
point locations immediately get visible to the process. This                              p1
speeds up convergence significantly because pressure waves
                                                                           Figure 2: Projection of the constraint C(p1 , p2 ) = |p1 −
can propagate through the material in a single solver step, an
                                                                           p2 | − d. The corrections ∆pi are weighted according to the
effect which is dependent on the order in which constraints
                                                                           inverse masses wi = 1/mi .
are solved. In over-constrained situations, the process can
lead to oscillations if the order is not kept constant.

3.3. Constraint Projection                                                    Substituting Eq. (4) into Eq. (3), solving for λ and substi-
                                                                           tuting it back into Eq. (4) yields the final formula for ∆p
Projecting a set of points according to a constraint means
moving the points such that they satisfy the constraint. The
most important issue in connection with moving points di-                                                    C(p)
rectly inside a simulation loop is the conservation of linear                                   ∆p = −               ∇pC(p)                            (5)
                                                                                                           |∇pC(p)|2
and angular momentum. Let ∆pi be the displacement of ver-
tex i by the projection. Linear momentum is conserved if                   which is a regular Newton-Raphson step for the iterative so-
                                                                           lution of the non-linear equation given by a single constraint.
                             ∑ mi ∆pi = 0,                       (1)       For the correction of an individual point pi we have
                             i
which amounts to conserving the center of mass. Angular                                     ∆pi = −s ∇pi C(p1 , . . . , pn ),                          (6)
momentum is conserved if                                                   where the scaling factor
                       ∑ ri × mi ∆pi = 0,                        (2)
                                                                                                s=
                                                                                                         C(p1 , . . . , pn )
                                                                                                                                                       (7)
                         i
                                                                                                     ∑ j p j C(p1 , . . . , pn )|2
                                                                                                        |∇
where the ri are the distances of the pi to an arbitrary com-
                                                                           is the same for all points. If the points have individual
mon rotation center. If a projection violates one of these con-
                                                                           masses, we weight the corrections ∆pi by the inverse masses
straints, it introduces so called ghost forces which act like ex-
                                                                           wi = 1/mi . In this case a point with infinite mass, i.e. wi = 0,
ternal forces dragging and rotation the object. However, only
                                                                           does not move for example as expected. Now Eq. (4) is re-
internal constraints need to conserve the momenta. Collision
                                                                           placed by
or attachment constraints are allowed to have global effects
on the object.                                                                ∆pi = λ wi ∇pi C(p) yielding
   The method we propose for constraint projection con-
serves both momenta for internal constraints. Again, the                                                    C(p1 , . . . , pn )
point based approach is more direct in that we can directly                                s=                                                          (8)
                                                                                                    ∑ j w j |∇p j C(p1 , . . . , pn )|2
use the constraint function while force based methods derive
forces via an energy term (see [BW98, THMG04]). Let us
                                                                              for the scaling factor and for the final correction
look at a constraint with cardinality n on the points p1 , . . . , pn
with constraint function C and stiffness k. We let p be the                                ∆pi = −s wi ∇pi C(p1 , . . . , pn ).                        (9)
concatenation [pT1 , . . . , pTn ]T . For internal constraints, C is
independent of rigid body modes, i.e. translation and rota-                  To give an example, let us consider the distance constraint
tion. This means that rotating or translating the points does              function C(p1 , p2 ) = |p1 − p2 | − d. The derivative with re-
not change the value of the constraint function. Therefore,                spect to the points are ∇p1 C(p1 , p2 ) = n and ∇p2 C(p1 , p2 ) =
the gradient ∇pC is perpendicular to rigid body modes be-                  −n with n = |pp1 −p−p2
                                                                                                  | . The scaling factor s is, thus, s =
                                                                                                1    2
cause it is the direction of maximal change. If the correction             |p1 −p2 |−d
∆p is chosen to be along ∇Cp both momenta are automati-                      w1 +w2 and the final corrections
cally conserved if all masses are equal (we handle different                                  w1                      p1 − p2
                                                                                    ∆p1 = −         (|p1 − p2 | − d)                                 (10)
masses later). Given p we want to find a correction ∆p such                                 w1 + w2                  |p1 − p2 |
that C(p + ∆p) = 0. This equation can be approximated by                                      w2                      p1 − p2
                                                                                    ∆p2 = +         (|p1 − p2 | − d)                                 (11)
            C(p + ∆p) ≈ C(p) + ∇pC(p) · ∆p = 0.                  (3)                        w1 + w2                  |p1 − p2 |
                                                                           which are the formulas proposed in [Jak01] for the projec-
  Restricting ∆p to be in the direction of ∇pC means choos-                tion of distance constraints (see Figure 2). They pop up as a
ing a scalar λ such that                                                   special case of the general constraint projection method.
                         ∆p = λ ∇pC(p).                          (4)

                                                                                                                       c The Eurographics Association 2006.
                                                                                                                       °
                                               M. Müller et al. / Position Based Dynamics

   We have not considered the type and the stiffness k of              namic colliding objects can be achieved by simulating both
the constraint so far. Type handling is straight forward. If           objects with our simulator, i.e. the N vertices and M con-
the type is equality we always perform a projection. If                straints which are the input to our algorithm simply represent
the type is inequality, the projection is only performed if            two or more independent objects. Then, if a point q of one
C(p1 , . . . , pn ) < 0. There are several ways of incorporating       objects moves through a triangle p1 , p2 , p3 of another object,
the stiffness parameter. The simplest variant is to multiply           we insert an inequality constraint with constraint function
the corrections ∆p by k ∈ [0 . . . 1]. However, for multiple           C(q, p1 , p2 , p3 ) = ±(q − p1 ) · [(p2 − p1 ) × (p3 − p1 )] which
iteration loops of the solver, the effect of k is non-linear.          keeps the point q on the correct side of the triangle. Since
The remaining error for a single distance constraint after             this constraint function is independent of rigid body modes,
ns solver iterations is ∆p(1 − k)ns . To get a linear relation-        it will correctly conserve linear and angular momentum.
ship we multiply the corrections not by k directly but by              Collision detection gets slightly more involved because the
k0 = 1 − (1 − k)1/ns . With this transformation the error be-          four vertices are represented by rays xi → pi . Therefore the
comes ∆p(1 − k0 )ns = ∆p(1 − k) and, thus, becomes linearly            collision of a moving point against a moving triangle needs
dependent on k and independent of ns as desired. However,              to be detected (see section about cloth self collision).
the resulting material stiffness is still dependent on the time
step of the simulation. Real time environments typically use
fixed time steps in which case this dependency is not prob-
                                                                       3.5. Damping
lematic.
                                                                       In line (6) of the simulation algorithm the velocities are
3.4. Collision Detection and Response                                  dampened before they are used for the prediction of the
                                                                       new positions. Any form of damping can be used and many
One advantage of the position based approach is how simply             methods for damping have been proposed in the literature
collision response can be realized. In line (8) of the simula-         (see [NMK∗ 05]). Here we propose a new method with some
tion algorithm the Mcoll collision constraints are generated.          interesting properties:
While the first M constraints given by the object representa-
tion are fixed throughout the simulation, the additional Mcoll         (1)   xcm = (∑i xi mi )/(∑i mi )
constraints are generated from scratch at each time step. The          (2)   vcm = (∑i vi mi )/(∑i mi )
number of collision constraints Mcoll varies and depends on            (3)   L = ∑i ri × (mi vi )
the number of colliding vertices. Both, continuous and static          (4)   I = ∑i r̃i r̃Ti mi
collisions can be handled. For continuous collision handling,          (5)   ω = I−1 L
we test for each vertex i the ray xi → pi . If this ray enters an      (6)   forall vertices i
object, we compute the entry point qc and the surface normal           (7)      ∆vi = vcm + ω × ri − vi
nc at this position. An inequality constraint with constraint          (8)      vi ← vi + kdamping ∆vi
function C(p) = (p − qc ) · nc and stiffness k = 1 is added            (9)   endfor
to the list of constraints. If the ray xi → pi lies completely
inside an object, continuous collision detection has failed at
some point. In this case we fall back to static collision han-         Here ri = xi − xcm , r̃i is the 3 by 3 matrix with the property
dling. We compute the surface point qs which is closest to             r̃i v = ri × v, and kdamping ∈ [0 . . . 1] is the damping coeffi-
pi and the surface normal ns at this position. An inequality           cient. In lines (1)-(5) we compute the global linear velocity
constraint with constraint function C(p) = (p − qs ) · ns and          xcm and angular velocity ω of the system. Lines (6)-(9) then
stiffness k = 1 is added to the list of constraints. Collision         only damp the individual deviations ∆vi of the velocities vi
constraint generation is done outside of the solver loop. This         from the global motion vcm + ω × ri . Thus, in the extreme
makes the simulation much faster. There are certain scenar-            case kdamping = 1, only the global motion survives and the
ios, however, where collisions can be missed if the solver             set of vertices behaves like a rigid body. For arbitrary values
works with a fixed collision constraint set. Fortunately, ac-          of kdamping , the velocities are globally dampened but without
cording to our experience, the artifacts are negligible.               influencing the global motion of the vertices.

   Friction and restitution can be handled by manipulating
the velocities of colliding vertices in step (16) of the algo-
rithm. The velocity of each vertex for which a collision con-          3.6. Attachments
straint has been generated is dampened perpendicular to the
                                                                       With the position based approach, attaching vertices to static
collision normal and reflected in the direction of the collision
                                                                       or kinematic objects is quite simple. The position of the ver-
normal.
                                                                       tex is simply set to the static target position or updated at ev-
   The collision handling discussed above is only correct for          ery time step to coincide with the position of the kinematic
collisions with static objects because no impulse is trans-            object. To make sure other constraints containing this vertex
ferred to the collision partners. Correct response for two dy-         do not move it, its inverse mass wi is set to zero.

c The Eurographics Association 2006.
°
                                                            M. Müller et al. / Position Based Dynamics

             p2                                n1                                                  p2                                               n
                                                                                          n
  n1
                                                         p1,2                                                                               q
                                                     ϕ
                                     p4                                                       q
       p3               p1                                                                                                                  h
                                                                                              p3                 p1                                          p1
                                                                                                                                                        p2
                                          p3        n2                  p4
                                                                                                                                   p3
                       n2

Figure 4: For bending resistance, the constraint function                             Figure 5: Constraint function C(q, p1 , p2 , p3 ) = (q − p1 ) ·
C(p1 , p2 , p3 , p4 ) = arccos(n1 · n2 ) − ϕ0 is used. The actual                     n − h makes sure that q stays above the triangle p1 , p2 , p3
dihedral angle ϕ is measure as the angle between the nor-                             by the the cloth thickness h.
mals of the two triangles.

                                                                                      4.2. Collision with Rigid Bodies
4. Cloth Simulation                                                                   For collision handling with rigid bodies we proceed as de-
We have used the point based dynamics framework to im-                                scribed in Section 3.4. To get two-way interactions, we apply
plement a real time cloth simulator for games. In this section                        an impulse mi ∆pi /∆t to the rigid body at the contact point,
we will discuss cloth specific issues thereby giving concrete                         each time vertex i is projected due to collision with that
examples of the general concepts introduced in the previous                           body. Testing only cloth vertices for collisions is not enough
section.                                                                              because small rigid bodies can fall through large cloth tri-
                                                                                      angles. Therefore, collisions of the convex corners of rigid
                                                                                      bodies against the cloth triangles are also tested.
4.1. Representation of Cloth
Our cloth simulator accepts as input arbitrary triangle                               4.3. Self Collision
meshes. The only restriction we impose on the input mesh
                                                                                      Assuming that the triangles all have about the same size,
is that it represents a manifold, i.e. each edge is shared by at
                                                                                      we use spatial hashing to find vertex triangle collisions
most two triangles. Each node of the mesh becomes a simu-
                                                                                      [THM∗ 03]. If a vertex q moves through a triangle p1 , p2 ,
lated vertex. The user provides a density ρ given in mass per
                                                                                      p3 , we use the constraint function
area [kg/m2 ]. The mass of a vertex is set to the sum of one
third of the mass of each adjacent triangle. For each edge,                                                          (p2 − p1 ) × (p3 − p1 )
                                                                                       C(q, p1 , p2 , p3 ) = (q − p1 ) ·                      − h,
we generate a stretching constraint with constraint function                                                        |(p2 − p1 ) × (p3 − p1 )|
                                                                                                                                               (12)
                  Cstretch (p1 , p2 ) = |p1 − p2 | − l0 ,                             where h is the cloth thickness (see Figure 5). If the vertex
stiffness kstretch and type equality. The scalar ł0 is the initial                    enters from below with respect to the triangle normal, the
length of the edge and kstretch is a global parameter provided                        constraint function has to be
by the user. It defines the stretching stiffness of the cloth. For                                                      (p3 − p1 ) × (p2 − p1 )
each pair of adjacent triangles (p1 , p3 , p2 ) and (p1 , p2 , p4 )                     C(q, p1 , p2 , p3 ) = (q − p1 ) ·                        −h
                                                                                                                       |(p3 − p1 ) × (p2 − p1 )|
we generate a bending constraint with constraint function                                                                                          (13)
                                                                                      to keep the vertex on the original side. Projecting these con-
                       Cbend (p1 , p2 , p3 , p4 ) =
       µ                                                                ¶             straints conserves linear and angular momentum which is es-
            (p2 − p1 ) × (p3 − p1 ) (p2 − p1 ) × (p4 − p1 )                           sential for cloth self collision since it is an internal process.
acos                                ·                                        − ϕ0 ,
           |(p2 − p1 ) × (p3 − p1 )| |(p2 − p1 ) × (p4 − p1 )|                        Figure 6 shows a rest state of a piece of cloth with self col-
stiffness kbend and type equality. The scalar ϕ0 is the ini-                          lisions. Testing continuous collisions is insufficient if cloth
tial dihedral angle between the two triangles and kbend is a                          gets into a tangled state, so methods like the ones proposed
global user parameter defining the bending stiffness of the                           by [BWK03] have to be applied.
cloth (see Figure 4). The advantage of this bending term
over adding a distance constraint between points p3 and p4                            4.4. Cloth Balloons
or over the bending term proposed by [GHDS03] is that it is
independent of stretching. This is because the term is inde-                          For closed triangle meshes, overpressure inside the mesh can
pendent of edge lengths. This way, the user can specify cloth                         easily be modeled (see Figure 7). We add an equality con-
with low stretching stiffness but high bending resistance for                         straint concerning all N vertices of the mesh with constraint
instance (see Figure 3).                                                              function
                                                                                                          Ãn                     !
                                                                                                                  triangles
  Eqns. (10) and (11) define the projection for the stretch-
ing constraints. In the appendix A we derive the formulas to
                                                                                         C(p1 , . . . , pN ) =        ∑ (pt × pt ) · pt
                                                                                                                              i
                                                                                                                              1
                                                                                                                                        i
                                                                                                                                        2
                                                                                                                                                i
                                                                                                                                                3
                                                                                                                                                    − kpressureV0
                                                                                                                      i=1
project the bending constraints.                                                                                                                                  (14)

                                                                                                                                  c The Eurographics Association 2006.
                                                                                                                                  °
                                                      M. Müller et al. / Position Based Dynamics




Figure 3: With the bending term we propose, bending and stretching are independent parameters. The top row shows
(kstretching , kbending ) = (1, 1), ( 21 , 1) and ( 100
                                                     1
                                                        , 1). The bottom row shows (kstretching , kbending ) = (1, 0), ( 21 , 0) and ( 100
                                                                                                                                        1
                                                                                                                                           , 0).




                                                                                Figure 7: Simulation of overpressure inside a character.


Figure 6: This folded configuration demonstrates stable self
collision and response.                                                       ments have been carried out to analyze the characteristics
                                                                              and the performance of the proposed method. All test sce-
                                                                              narios presented in this section have been performed on a
                                                                              PC Pentium 4, 3 GHz.
and stiffness k = 1 to the set of constraints. Here t1i ,t2i and t3i
are the three indices of the vertices belonging to triangle i.                  Independent Bending and Stretching. Our bending term
The sum computes the actual volume of the closed mesh. It                     only depends on the dihedral angle of adjacent triangles, not
is compared against the original volume V0 times the over-                    on edge lengths, so bending and stretching resistances can
pressure factor kpressure . This constraint function yields the               be chosen independently. Figure 3 shows a cloth bag with
gradients                                                                     various stretching stiffnesses, first with bending resistance
                                                                              enabled and then disabled. As the top row shows, bending
∇pi C = ∑ (pt j × pt j ) + ∑ (pt j × pt j ) + ∑ (pt j × pt j )
                      2      3                3   1              1   2        does not influence stretching resistance.
           j:t1j =i                j:t2j =i           j:t3j =i
                                                         (15)                    Attachments with Two Way Interaction. We can sim-
These gradients have to be scaled by the scaling factor given                 ulate both, one way and two way coupled attachment con-
in Eq. (7) and weighted by the masses according to Eq. (9)                    straints. The cloth stripes in Figure 8 are attached via one
to get the final projection offsets ∆pi .                                     way constraints to the static rigid bodies at the top. In addi-
                                                                              tion, two way interaction is enabled between the stripes and
                                                                              the bottom rigid bodies. This configuration results in realis-
5. Results
                                                                              tically looking swing and twist motions of the stripes. The
We have integrated our method into Rocket [Rat04], a game-                    scene features 6 rigid bodies and 3 pieces of cloth which are
like environment for physics simulation. Various experi-                      simulated and rendered with more than 380 fps.

c The Eurographics Association 2006.
°
                                              M. Müller et al. / Position Based Dynamics

                                                                      7. Future Work
                                                                      A topic we have not treated in this paper is rigid body simu-
                                                                      lation. However, the approach we presented could quite eas-
                                                                      ily be extended to handle rigid objects as well. Instead of
                                                                      computing a set of linear and angular impulses for the res-
                                                                      olution of collisions as regular rigid body solvers typically
                                                                      do, movements and rotations would be applied to the bod-
Figure 8: Cloth stripes are attached via one way interaction          ies at the contact points and the linear and angular velocities
to static rigid bodies at the top and via two way constraints         would have to be adjusted accordingly after the solver has
to rigid bodies at the bottom.                                        completed.



   Real Time Self Collision. The piece of cloth shown in
Figure 6 is composed of 1364 vertices and 2562 triangles.
The simulation runs at 30 fps on average including self col-
lision detection, collision handling and rendering. The effect
of friction is shown in Figure 9 where the same piece of cloth
is tumbling in a rotating barrel.
   Tearing and stability. Figure 10 shows a piece of cloth
consisting of 4264 vertices and 8262 triangles that is torn
open by an attached cube and finally ripped apart by a
thrown ball. This scene is simulated and rendered with 47 fps
on average. Tearing is simulated by a simple process: When-
ever the stretching of an edge exceeds a specified threshold
value, we select one of the edge’s adjacent vertices. We then
put a split plane through that vertex perpendicular to the edge
direction and split the vertex. All triangles above the split
plane are assigned to the original vertex while all triangles
below are assigned to the duplicate. Our method remains sta-
ble even in extreme situations as shown in Figure 1, a scene
inspired by [ITF04]. An inflated character model is squeezed
through rotating gears resulting in multiple constraints, col-
lisions and self collisions acting on single cloth vertices.
   Complex Simulation Scenarios. The presented method
is especially suited for complex simulation environments
(see Figure 12). Despite the extensive interaction with an-
imated characters and geometrically complex game levels,
simulation and rendering of multiple pieces of cloth can still
be done at interactive speed.

6. Conclusions
We have presented a position based dynamics framework
that can handle general constraints formulated via constraint
functions. With the position based approach it is possible to
manipulate objects directly during the simulation. This sig-
nificantly simplifies the handling of collisions, attachment
constraints and explicit integration and it makes direct and
immediate control of the animated scene possible.
   We have implemented a robust cloth simulator on top of
this framework which provides features like two way inter-
action of cloth with rigid bodies, cloth self collision and re-
sponse and attachments of pieces of cloth to dynamic rigid
bodies.

                                                                                                        c The Eurographics Association 2006.
                                                                                                        °
                                                  M. Müller et al. / Position Based Dynamics




              Figure 9: Influenced by collision, self collision and friction, a piece of cloth tumbles in a rotating barrel.




                    Figure 10: A piece of cloth is torn open by an attached cube and ripped apart by a thrown ball.




                          Figure 11: Three inflated characters experience multiple collisions and self collisions.




Figure 12: Extensive interaction between pieces of cloth and an animated game character (left), a geometrically complex game
level (middle) and hundreds of simulated plant leaves (right).




c The Eurographics Association 2006.
°
                                                  M. Müller et al. / Position Based Dynamics

References                                                                Appendix A:
[BFA02] B RIDSON R., F EDKIW R., A NDERSON J.: Robust treat-              Gradient of the Normalized Cross Product
  ment of collisions, contact and friction for cloth animation. Pro-
  ceedings of ACM Siggraph (2002), 594–603.                               Constraint functions often contain normalized cross products. To de-
                                                                          rive the projection corrections, the gradient of the constraint func-
[BMF03] B RIDSON R., M ARINO S., F EDKIW R.: Simulation of                tion is needed. Therefore it is useful to know the gradient of a nor-
  clothing with folds and wrinkles. In ACM SIGGRAPH Sympo-                malized cross product with respect to both arguments. Given the
  sium on Computer Animation (2003), pp. 28–36.                           normalized cross product n = |pp1 ×p×p2
                                                                                                                   , the derivative with respect to
                                                                                                            1   2|
[BW98] BARAFF D., W ITKIN A.: Large steps in cloth simula-                the first vector is
  tion. Proceedings of ACM Siggraph (1998), 43–54.                                    ∂ nx    ∂ nx     ∂ nx 
                                                                                        ∂ p1x   ∂ p1y   ∂ p1z
[BWK03] BARAFF D., W ITKIN A., K ASS M.: Untangling cloth.                  ∂n          ∂ ny   ∂ ny    ∂ ny    
                                                                                =                                                                (16)
  In Proceedings of the ACM SIGGRAPH (2003), pp. 862–870.                   ∂ p1       ∂ p1x
                                                                                         ∂ nz
                                                                                                ∂ p1y
                                                                                                 ∂ nz
                                                                                                        ∂ p1z
                                                                                                        ∂ nz
                                                                                                                
[CBP05] C LAVET S., B EAUDOIN P., P OULIN P.: Particle-based                            ∂ p1x   ∂ p1y   ∂ p1z
                                                                                                                                          
  viscoelastic fluid simulation. Proceedings of the ACM SIG-                                       0             p2z    −p2y
                                                                                       1       −p2z                                     T
  GRAPH Symposium on Computer Animation (2005), 219–228.                         =                                0      p2x   + n(n × p2 )
                                                                                   |p1 × p2 |
[DSB99] D ESBRUN M., S CHRÖDER P., BARR A.: Interactive                                           p2y           −p2x      0
  animation of structured deformable objects. In Proceedings of                                                                             (17)
  Graphics Interface ’99 (1999), pp. 1–8.                                 Shorter and for both arguments we have
[Fau98] FAURE F.: Interactive solid animation using linearized                           ∂n          1      ¡                    ¢
   displacement constraints. In Eurographics Workshop on Com-                                 =              −p˜2 + n(n × p2 )T                    (18)
                                                                                         ∂ p1    |p1 × p2 |
   puter Animation and Simulation (EGCAS) (1998), pp. 61–72.
                                                                                         ∂n          1      ¡                    ¢
[Fed05] F EDOR M.: Fast character animation using particle dy-                                =−              −p˜1 + n(n × p1 )T                   (19)
                                                                                         ∂ p2    |p1 × p2 |
   namics. Proceedings of International Conference on Graphics,
   Vision and Image Processing, GVIP05 (2005).                                                                                                     (20)

[GHDS03] G RINSPUN E., H IRANI A., D ESBRUN M.,                           where p̃ is the matrix with the property p̃x = p × x.
  S CHRODER P.:  Discrete shells. In Proceedings of the
  ACM SIGGRAPH Symposium on Computer Animation (2003).
                                                                          Bending Constraint Projection
[ITF04] I RVING G., T ERAN J., F EDKIW R.: Invertible finite el-
   ements for robust simulation of large deformation. In Proceed-         The constraint function for bending is C = arccos(d) − ϕ0 , where
   ings of the ACM SIGGRAPH Symposium on Computer Animation               d = n1 · n2 = nT1 n2 . Without loss of generality we set p1 = 0 and get
   (2004), pp. 131–140.                                                   for the normals n1 = |pp2 ×p
                                                                                                     ×p3
                                                                                                          and n2 = |pp2 ×p4 . With d arccos(x) =
                                                                                                                                   dx
                                                                                                   2   3|             2 ×p4 |
                                                                                1
[Jak01] JAKOBSEN T.: Advanced character physics Ű the fysix              −√        we get the following gradients:
                                                                              1−x2
   engine. www.gamasutra.com (2001).                                                                    µ      ¶
                                                                                                  1       ∂ n1 T
[MHTG05] M ÜLLER M., H EIDELBERGER B., T ESCHER M.,                                  ∇p3 C = − √       (          n2 )                             (21)
  G ROSS M.: Meshless deformations based on shape matching.                                     1 − d 2 ∂ p3
                                                                                                        µ      ¶
  Proceedings of ACM Siggraph (2005), 471–478.                                                    1       ∂ n2 T
                                                                                     ∇p4 C = − √       (          n1 )                             (22)
[NMK∗ 05] N EALEN A., M ÜLLER M., K EISER R., B OXERMAN                                         1 − d 2 ∂ p4
                                                                                                        µ      ¶T      µ      ¶
  E., C ARLSON M.: Physically based deformable models in com-                                     1       ∂ n1           ∂ n2 T
                                                                                     ∇p2 C = − √       (          n2 +          n1 )               (23)
  puter graphics. Eurographics 2005 state of the art report (2005).                             1 − d 2 ∂ p2             ∂ p2
[Pro95] P ROVOT X.: Deformation constraints in a mass-spring                         ∇p1 C = −∇p2 C − ∇p3 C − ∇p4 C                                (24)
   model to describe rigid cloth behavior. Proceedings of Graphics
                                                                          Using the gradients of normalized cross products, first compute
   Interface (1995), 147Ű–154.
                                                                                    p2 × n2 + (n1 × p2 )d
[Rat04] R ATCLIFF J.: Rocket - a viewer for real-time phyics sim-              q3 =                                                                (25)
  ulations. www.physicstools.org (2004).                                                  |p2 × p3 |
                                                                                    p2 × n1 + (n2 × p2 )d
[THM∗ 03] T ESCHNER M., H EIDELBERGER B., M ÜLLER M.,                          q4 =                                                                (26)
  P OMERANERTS D., G ROSS M.: Optimized spatial hashing for                               |p2 × p4 |
  collision detection of deformable objects. Proc. Vision, Model-                     p3 × n2 + (n1 × p3 )d p4 × n1 + (n2 × p4 )d
                                                                               q2 = −                      −                                       (27)
  ing, Visualization VMV 2003 (2003), 47–54.                                                |p2 × p3 |            |p2 × p4 |
[THMG04] T ESCHNER M., H EIDELBERGER B., M ÜLLER M.,                           q1 = −q2 − q3 − q4                                                  (28)
  G ROSS M.: A versatile and robust model for geometrically com-          Then the final correction is
  plex deformable solids. Proceedings of Computer Graphics In-                                      √
  ternational (CGI) (2004), 312–319.                                                              wi 1 − d 2 (arccos(d) − ϕ0 )
                                                                                        ∆pi = −                                qi                  (29)
                                                                                                         ∑ j w j |q j |2
[VCMT95] VOLINO P., C OURCHESNE M., M AGNENAT-
  T HALMANN N.:         Versatile and efficient techniques for
  simulating cloth and other deformable objects. Proceedings of
  ACM Siggraph (1995), 137–144.

                                                                                                                    c The Eurographics Association 2006.
                                                                                                                    °
