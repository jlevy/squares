EUROGRAPHICS 2017/ A. Bousseau and D. Gutierrez                                                                                        Tutorial




                                  A Survey on Position Based Dynamics, 2017

                                                                Jan Bender1 , Matthias Müller2 and Miles Macklin2

                                                                             1 RWTH Aachen University
                                                                             2 NVIDIA PhysX Research




                                   Figure 1: A selection of scenes simulated inside the position-based dynamics framework.

         Abstract
         The physically-based simulation of mechanical effects has been an important research topic in computer graphics for more than
         two decades. Classical methods in this field discretize Newton’s second law and determine different forces to simulate various
         effects like stretching, shearing, and bending of deformable bodies or pressure and viscosity of fluids, to mention just a few.
         Given these forces, velocities and finally positions are determined by a numerical integration of the resulting accelerations.
         In the last years position-based simulation methods have become popular in the graphics community. In contrast to classical
         simulation approaches these methods compute the position changes in each simulation step directly, based on the solution of
         a quasi-static problem. Therefore, position-based approaches are fast, stable and controllable which make them well-suited
         for use in interactive environments. However, these methods are generally not as accurate as force-based methods but provide
         visual plausibility. Hence, the main application areas of position-based simulation are virtual reality, computer games and
         special effects in movies and commercials.
         In this tutorial we first introduce the basic concept of position-based dynamics. Then we present different solvers and compare
         them with the variational formulation of the implicit Euler method in connection with compliant constraints. We discuss ap-
         proaches to improve the convergence of these solvers. Moreover, we show how position-based methods are applied to simulate
         elastic rods, cloth, volumetric deformable bodies, rigid body systems and fluids. We also demonstrate how complex effects like
         anisotropy or plasticity can be simulated and introduce approaches to improve the performance. Finally, we give an outlook
         and discuss open problems.
         Keywords: physically-based animation, position-based dynamics, deformable solids, rigid bodies, fluids
         Categories and Subject Descriptors (according to ACM CCS): Computer Graphics [I.3.7]: Three-Dimensional Graphics and
         Realism—Animation




©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                  J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Contents

1   Tutorial Details                                                                                                                                            3
1.1 Presenters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                      3
1.2 Length . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                      3
1.3 Necessary Background . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                          3
1.4 Potential Target Audience . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                       3

2     Introduction                                                                                                                                              4

3     Background                                                                                                                                                4
3.1   Equations of Motion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                     4
3.2   Time Integration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                    5
3.3   Constraints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                   5

4     The Core Of Position Based Dynamics                                                                                                                       5
4.1   The Algorithm . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                     5
4.2   Solver . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                    6

5    Specific Constraints                                                                                                                                      9
5.1 Stretching . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                     9
5.2 Bending . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                      9
5.3 Isometric Bending . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                      9
5.4 Collisions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                    10
5.5 Volume Conservation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                       11
5.6 Long Range Attachments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                        13
5.7 Strands . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                   13
5.8 Continuous Materials . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                      13
5.9 Rigid Body Dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                       17
5.10 Fluids . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                   18
5.11 Shape Matching . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                     19

6   Implementation                                                                                                                                            25
6.1 Parallelization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                   25
6.2 Unified Solver . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                    27

7     Applications                                                                                                                                            27
7.1   Strain Limiting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                 27
7.2   Wrinkle Meshes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                    27
7.3   Further Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                  28

8     Conclusion                                                                                                                                              29

References                                                                                                                                                    29




                                                                                                                                            ©
                                                                                                                                               2017 The Author(s)
                                                                                                     Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

1. Tutorial Details                                                                     1.2. Length
1.1. Presenters                                                                         This is a half day tutorial (180 minutes).
Jan Bender Jan Bender received his doctoral degree in the begin-
ning of 2007 from the University of Karlsruhe. The topic of his                         1.3. Necessary Background
thesis was the interactive dynamic simulation of multibody sys-                         In our tutorial we will make a short introduction in the basics of
tems. In the following years he continued his research in the area of                   physically-based animation. However, general knowledge in this
physically-based simulation as post-doc at the Karlsruhe Institute                      area is recommended.
of Technology (2007-2010) and as assistant professor at the Grad-
uate School of Computational Engineering, TU Darmstadt (2010-
2016). Since 2016 he is professor at the Visual Computing Institute                     1.4. Potential Target Audience
at RWTH Aachen University and leads the Computer Animation                              This tutorial is intended for researchers and developers in the area
Group. His current research areas include: rigid body dynamics, de-                     of computer animation who are interested in interactive physically-
formable solids, fluids, position-based methods, collision detection                    based simulation methods. This will be an intermediate level tuto-
and resolution, cutting, fracturing and real-time visualization. He                     rial.
has served on program committees of major graphics conferences
and is associate editor for IEEE Computer Graphics and Applica-
tions.
• email address: bender@cs.rwth-aachen.de
• URL:           www.interactive-graphics.de

Matthias Müller Matthias Müller received his PhD in atomistic
simulation of dense polymer systems in 1999 from ETH Zürich.
During his post-doc with the MIT Computer Graphics Group
(1999-2001), he changed fields to macroscopic physically based
simulations. He has published papers on particle-based water simu-
lation and visualization, finite element-based soft bodies, cloth sim-
ulation, and fracture simulation. The main focus of his research are
unconditionally stable, fast and controllable simulation techniques
for the use in computer games. Most relevant to this tutorial, he is
one of the founders of the field of position based simulation meth-
ods.
   In 2002, he co-founded the game middleware company
NovodeX (acquired in 2004 by AGEIA), where he was head
of research and responsible for extension of the physics simulation
library PhysX by innovative new features. He has been head of
the PhysX research team of NVIDIA since that company acquired
AGEIA Technologies, Inc. in early 2008.
• email address: matthiasm@nvidia.com
• URL:           www.matthias-mueller-fischer.ch

Miles Macklin Miles Macklin is a researcher on the PhysX re-
search team at NVIDIA. Since 2013, he has been working on a
unified physics library called NVIDIA Flex, built using Position-
Based Dynamics. The technology in Flex has been the subject of
two papers at SIGGRAPH and has now been released to several
games and visual effects studios. Prior to joining NVIDIA, Miles
worked in the games industry as a visual effects engineer at Sony
Computer Entertainment on early Playstation3 development, Rock-
steady Studios in London on the Batman Arkham series, and Lu-
casArts in San Francisco on the Star Wars franchise. His current
research is focused on real-time methods for simulation and ren-
dering using GPUs.
• email address: mmacklin@nvidia.com
• URL:           www.mmacklin.com

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                   J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

2. Introduction                                                              the velocity layer as well and immediately work on the positions.
                                                                             The main advantage of a position-based approach is its controllabil-
The simulation of solid objects such as rigid bodies, soft bodies
                                                                             ity. Overshooting problems of explicit integration schemes in force
or cloth has been an important and active research topic in com-
                                                                             based systems can be avoided. In addition, collision constraints can
puter graphics for more than 30 years. The field was introduced
                                                                             be handled easily and penetrations can be resolved completely by
to graphics by Terzopoulos and his colleagues in the late eighties
                                                                             projecting points to valid locations.
[TPBF87a]. Since then, a large body of work has been published
and the list is growing rapidly. There exists a variety of survey pa-           Among the force based approaches, one of the simplest methods
pers [GM97,MTV05,NMK∗ 06,MSJT08,BET14] which document                        is to represent and simulate solids with mass-spring networks. A
this development.                                                            mass spring system consists of a set of point masses that are con-
                                                                             nected by springs. The physics of such a system is straightforward
   In this tutorial we focus on a special class of simulation meth-
                                                                             and a simulator is easy to implement. However, there are some sig-
ods, namely position-based approaches [BMO∗ 14]. These methods
                                                                             nificant drawbacks of the simple method.
were originally developed for the simulation of solids. However,
some recent works demonstrated that the position-based concepts              • The behavior of the object depends on the way the spring net-
can even be used to simulate fluids and articulated rigid bodies.              work is set up.
Classical dynamics simulation methods formulate the change of                • It can be difficult to tune the spring constants to get the desired
momentum of a system as a function of applied forces, and evolve               behavior.
positions through numerical integration of accelerations and ve-             • Mass spring networks cannot capture volumetric effects directly
locities. Position-based approaches, instead, compute positions di-            such as volume conservation or prevention of volume inversions.
rectly, based on the solution to a quasi-static problem.
                                                                                The Finite Element Method solves all of the above problems be-
   Physical simulation is a well studied problem in the computa-             cause it considers the entire volume of a solid instead of replacing it
tional sciences and therefore, many of the well established meth-            with a finite number of point masses. Here, the object is discretized
ods have been adopted in graphics such as the Finite Element                 by splitting the volume into a number of elements with finite size.
Method (FEM) [OH99], the Finite Differences Method [TPBF87b],                This discretization yields a mesh as in the mass spring approach in
the Finite Volume Method [TBHF03], the boundary element                      which the vertices play the role of the mass points and the elements,
method [JP99] or particle-based approaches [DSB99, THMG04].                  typically tetrahedra, can be viewed as generalized springs acting on
The main goal of computer simulations in computational physics               multiple points at the same time. In both cases, forces at the mass
and chemistry is to replace real-world experiments and thus, to be           points or mesh vertices are computed due to their velocities and the
as accurate as possible. In contrast, the main applications of phys-         actual deformation of the mesh.
ically based simulation methods in computer graphics are special
effects in movies and commercials and more recently, computer                   In this tutorial we focus on position-based simulation methods
games and other interactive systems. Here, speed and controllabil-           which omit the velocity and acceleration layer and directly mod-
ity are the most important factors and all that is required in terms of      ify the positions. In the following we first introduce the basics of
accuracy is visual plausibility. This is especially true for real-time       physically-based simulation, before we present the position-based
applications.                                                                concept in the next section.

   Position-based methods are tailored particularly for use in inter-
active environments. They provide a high level of control and are            3.1. Equations of Motion
stable even when simple and fast explicit time integration schemes
                                                                             Each particle i has three attributes, namely its mass mi , its position
are used. Due to their simplicity, robustness and speed these ap-
                                                                             xi and its velocity vi . The equation of motion of a particle is derived
proaches have recently become very popular in computer graphics
                                                                             from Newton’s second law:
and in the game industry.
                                                                                                                     1
   Collision detection is an important part of any simulation system.                                        v̇i =      fi ,                                  (1)
                                                                                                                     mi
However, an adequate discussion of this topic is beyond the scope
                                                                             where fi is the sum of all forces acting on particle i. The relationship
of this tutorial. Therefore, we refer the reader to the surveys of Lin
                                                                             between ẋ and v is described by the velocity kinematic relationship:
and Gottschalk [LG98] and the one of Teschner et al. [TKH∗ 05].

                                                                                                               ẋi = vi .                                     (2)
3. Background
The most popular approaches for the simulation of dynamic sys-                  While particles have only three translational degrees of freedom,
tems in computer graphics are force based. Internal and exter-               rigid bodies have also three rotational ones. Therefore, a rigid body
nal forces are accumulated from which accelerations are com-                 requires additional attributes, namely its inertia tensor Ii ∈ R3×3 ,
puted based on Newton’s second law of motion. A time integration             its orientation, which is typically represented by a unit quaternion
method is then used to update the velocities and finally the positions       qi ∈ H, and its angular velocity ωi ∈ R3 . For a rigid body generally
of the object. A few simulation methods (most rigid body simula-             a local coordinate system is chosen so that its origin is at the cen-
tors) use impulse based dynamics and directly manipulate veloc-              ter of mass and its axes are oriented such that the inertia tensor is
ities [BFS05, Ben07]. In contrast, geometry-based methods omit               diagonal in local coordinates.

                                                                                                                                             ©
                                                                                                                                                2017 The Author(s)
                                                                                                      Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

   Newton’s second law actually applies only to particles. By view-                     methods only consider constraints that depend on positions and in
ing rigid bodies as collections of infinite numbers of particles, Euler                 the case of rigid bodies on orientations. Hence, a bilateral constraint
extended this law to the case of rigid bodies. Therefore, the equa-                     is defined by a function
tions of motion for rigid bodies are also known as the Newton-Euler
                                                                                                               C(xi1 , qi1 , . . . , xin j , qin j ) = 0
equations. The equation of motion for the rotational part of a rigid
body is:                                                                                and a unilateral constraint by
                         ω̇i = I−1
                                i (τi − (ωi × (Ii ωi ))) ,                   (3)                              C(xi1 , qi1 , . . . , xin j , qin j ) ≥ 0,
where τi is the sum of all moments. A moment can be a pure mo-                          where {i1 , . . . in j } is a set of body indices and n j is the cardinality of
ment or a byproduct of a force τ = (p − x) × f if the force f acts                      the constraint. Typically, the constraints used in PBD only depend
at a point p and x is the center of mass of the body. The velocity                      on positions and time but not on velocities. Such constraints are
kinematic relationship for the rotational part is defined by                            called holonomic.
                                          1                                                Since constraints are kinematic restrictions, they also affect the
                                     q̇i = ω̃i qi ,                          (4)
                                          2                                             dynamics. Classical methods determine forces to simulate a dy-
                                                 y
where ω̃i is the quaternion [0, ωxi , ωi , ωzi ].                                       namic system with constraints. This is done, e.g. by defining a po-
                                                                                        tential energy E = 2k C2 and deriving the forces as f = −∇E (soft
                                                                                        constraints) or via Lagrange multipliers derived from constrained
3.2. Time Integration                                                                   dynamics (hard constraints) [Wit97]. In contrast to that position-
A simulation step for an unconstrained particle or rigid body is per-                   based approaches modify the positions and orientations of the bod-
formed by numerical integration of Equations (1)-(2) or Equations                       ies directly in order to fulfill all constraints.
(1)-(4), respectively. The most popular integration method in the
field of position-based dynamics is the symplectic Euler method
                                                                                        4. The Core Of Position Based Dynamics
which is introduced in the following.
                                                                                        In this section we present Position-Based Dynamics (PBD), an ap-
   In contrast to the well-known explicit Euler, the symplectic Euler                   proach which omits the velocity and acceleration layer and imme-
uses the velocity at time t0 + ∆t instead of time t0 for the integration                diately works on the positions [MHHR07]. We will first describe
of the position vector. The time integration for a particle is then                     the basic idea and the simulation algorithm of PBD. Then we will
performed by the following equations:                                                   focus specifically on how to solve the system of constraints that
                                                  1                                     describe the object to be simulated.
                    vi (t0 + ∆t) = vi (t0 ) + ∆t      fi (t0 )
                                                 mi
                                                                                           In the following the position-based approach is introduced first
                    xi (t0 + ∆t) = xi (t0 ) + ∆t vi (t0 + ∆t).                          for particle systems. An extension to handle rigid bodies is pre-
                                                                                        sented in Section 5.9.
   In the case of a rigid body also Equations (3) and (4) must be
integrated. Using the symplectic Euler method this yields:
                                                                                        4.1. The Algorithm
           ωi (t0 + ∆t) = ωi (t0 ) + ∆t I−1
                                         i (t0 ) ·
                                                                                        The objects to be simulated are represented by a set of N particles
                         (τi (t0 ) − (ωi (t0 ) × (Ii (t0 )ωi (t0 ))))
                                                                                        and a set of M constraints. For each constraint we introduce a stiff-
                                      1
            q(t0 + ∆t) = q(t0 ) + ∆t ω̃i (t0 + ∆t)qi (t0 ).                             ness parameter k which defines the strength of the constraint in a
                                      2                                                 range from zero to one. This gives a user more control over the
Note that due to numerical errors the condition kqk = 1, which                          elasticity of a body.
must be satisfied by a quaternion that represents a rotations, can
be violated after the integration. Therefore, the quaternion must be                    4.1.1. Time Integration
normalized after each time integration step.
                                                                                        Given this data and a time step ∆t, the simulation proceeds as de-
   Symplectic Euler is a first-order integrator, and is used only for                   scribed by Algorithm 1. Since the algorithm simulates a system
the prediction step of the algorithm. In Position Based Dynamics                        which is second order in time, both the positions and the velocities
(PBD), constraint forces are integrated implicitly as described in                      of the particles need to be specified in (1)-(3) before the simula-
Section 4.2.4.                                                                          tion loop starts. Lines (5)-(6) perform a simple symplectic Euler
                                                                                        integration step on the velocities and the positions. The new loca-
                                                                                        tions pi are not assigned to the positions directly but are only used
3.3. Constraints
                                                                                        as predictions. Non-permanent external constraints such as colli-
Constraints are kinematic restrictions in the form of equations and                     sion constraints are generated at the beginning of each time step
inequalities that constrain the relative motion of bodies. Equality                     from scratch in line (7). Here the original and the predicted posi-
and inequality constraints are referred to as bilateral and unilateral                  tions are used in order to perform continuous collision detection.
constraints, respectively. Generally, constraints are functions of po-                  The solver (8)-(10) then iteratively corrects the predicted positions
sition and orientation variables, linear and angular velocities, and                    such that they satisfy the Mcoll external as well as the M internal
their derivatives to any order. However, position-based simulation                      constraints. Finally, the corrected positions pi are used to update

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                        J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

Algorithm 1 Position-based dynamics                                               These forces can also be applied to position-based methods. How-
 1: for all vertices i do                                                         ever, as the approaches of Baraff and Witkin and Nealen et al. rely
 2:     initialize xi = x0i , vi = v0i , wi = 1/mi                                on topological information of the object geometry, they cannot be
 3: end for                                                                       applied to meshless techniques such as shape matching.
 4: loop                                                                             Point and spring damping can be used to reduce current veloci-
 5:     for all vertices i do vi ← vi + ∆twi fext (xi )                           ties or relative velocities. However, it is generally more appropriate
 6:     for all vertices i do pi ← xi + ∆tvi                                      to consider predicted velocities or relative velocities for the next
 7:     for all vertices i do genCollConstraints(xi → pi )                        time step.
 8:     loop solverIteration times
 9:          projectConstraints(C1 , . . . ,CM+MColl , p1 , . . . , pN )             An interesting damping alternative has been presented
10:     end loop                                                                  in [SGT09]. Here, the idea of symmetric, momentum-conserving
11:     for all vertices i do                                                     forces is extended to meshless representations. Global symmetric
12:          vi ← (pi − xi )/∆t                                                   damping forces are computed with respect to the center of mass
13:          xi ← pi                                                              of an object. While such forces conserve the linear momentum,
14:     end for                                                                   the preservation of the angular momentum is guaranteed by force
15:     velocityUpdate(v1 , . . . , vN )                                          projection onto relative positions or by torque elimination using
16: end loop
                                                                                  Linear Programming. The approach presented in [SGT09] itera-
                                                                                  tively computes damping forces. The paper, however, also shows
                                                                                  the convergence of the iterative process and how the solution can
                                                                                  be computed directly without performing iterations. Therefore,
the positions and the velocities. It is essential here to update the ve-          the approach is an efficient alternative to compute damping forces
locities along with the positions. If this is not done, the simulation            for arbitrary position-based deformation models with or with-
does not produce the correct behavior of a second order system.                   out connectivity information. The approach can be used to damp
As you can see, the integration scheme used here is very similar to               oscillations globally or locally for user-defined clusters.
the Verlet method. It is also closely related to Jos Stam’s Nucleus
solver [Sta09] which also uses a set of contraints to describe the
                                                                                  4.2. Solver
objects to be simulated. The main difference is that Nucleus solves
the constraints for velocities, not positions.                                    4.2.1. The System to be Solved
                                                                                  The goal of the solver step (8)-(10) in Algorithm 1 is to correct the
4.1.2. Damping                                                                    predicted positions of the particles such that they satisfy all con-
The quality of dynamic simulations can generally be improved by                   straints. In what follows and in contrast to Algorithm 1, we will
the incorporation of an appropriate damping scheme. As a positive                 use the symbol x for the positions of the particles the solver works
effect, damping can improve the stability by reducing temporal os-                on which is a more common symbol for positions. In Algorithm 1
cillations of the point positions of an object. This enables the use              we have a larger context and used the symbol p to distinguish the
of larger time steps which increases the performance of a dynamic                 predicted positions from the positions of the previous time step.
simulation. On the other hand, damping changes the dynamic mo-                       The problem that needs to be solved comprises of a set of M
tion of the simulated objects. The resulting effects can be either                equations for the 3N unknown position components, where M is
desired, e.g. reduced oscillations of a deformable solid, or disturb-             now the total number of constraints. This system does not need to
ing, e.g. changes of the linear or angular momentum of the entire                 be symmetric. If M > 3N (M < 3N), the system is over-determined
object.                                                                           (under-determined). In addition to the asymmetry, the equations
   Generally, a damping term CẊ can be incorporated into the mo-                 are in general non-linear. The function of a simple distance con-
tion equation of an object where Ẋ denotes the vector of all first               straint C(x1 , x2 ) = |x1 − x2 |2 − d 2 yields a non-linear equation.
time derivatives of positions. If the user-defined matrix C is diago-             What complicates things even further is the fact that collisions pro-
nal, absolute velocities of the points are damped, which sometimes                duce inequalities rather than equalities. Solving a non-symmetric,
is referred to as point damping. If appropriately computed, such                  non-linear system with equalities and inequalities is a tough prob-
point damping forces result in an improved numerical stability by                 lem.
reducing the acceleration of a point. Such characteristics are de-                  Let x be the concatenation [xT1 , . . . , xTN ]T and let all the constraint
sired in some settings, e.g. in the context of friction. In the general           functions C j take the concatenated vector x as input while only
case, however, the overall slow-down of an object, caused by point                using the subset of coordinates they are defined for. We can now
damping forces, is not desired. Point damping forces are, e.g., used              write the system to be solved as
in [TF88] or in [PB88], where point damping is used for dynamic
                                                                                                                 C1 (x)  0
simulations with geometric constraints such as point-to-nail.
                                                                                                                     ...
   In order to preserve linear and angular momentum of deformable
                                                                                                                CM (x)  0,
objects, symmetric damping forces, usually referred to as spring
damping forces, can be used. Such forces can be represented by                    where the symbol  denotes either = or ≥. Newton-Raphson itera-
non-diagonal entries in the matrix C. Damping forces are, e.g., de-               tion is a method to solve non-linear symmetric systems with equal-
scribed by Baraff and Witkin [BW98] or Nealen et al. [NMK∗ 06].                   ities only. The process starts with a first guess of a solution. Each

                                                                                                                                                   ©
                                                                                                                                                      2017 The Author(s)
                                                                                                            Eurographics Proceedings © 2017 The Eurographics Association.
                                               J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

constraint function is then linearized in the neighborhood of the                         and wi = 1/mi . Formulated for the concatenated vector x of all po-
current solution using                                                                    sitions we get

            C(x + ∆x) = C(x) + ∇C(x) · ∆x + O(|∆x|2 ) = 0.                                                     λ=
                                                                                                                         C(x)
                                                                                                                                    .                        (9)
                                                                                                                    ∇C(x)M−1 ∇C(x)T
This yields a linear system for the global correction vector ∆x
                                                                                             As mentioned above, the solver linearizes the constraint func-
                            ∇C1 (x) · ∆x = −C1 (x)                                        tions. However, in contrast to the Newton-Raphson method, the
                                         ...                                              linearization happens individually per constraint. It is important
                           ∇CM (x) · ∆x = −CM (x),                                        to note that linearization does not affect the projection of an indi-
                                                                                          vidual distance constraint. This is because despite being non-linear
where ∇C j (x) is the 1 × N dimensional vector containing the                             globally, a distance constraint is linear along the constraint gradi-
derivatives of the function C j w.r.t. all its parameters, i.e. the N                     ent which happens to be the search direction. This is true for other
components of x. It is also the j-th row of the linear system. Both,                      constraints as well like the tetrahedral volume constraint we will
the rows ∇C j (x) and the right hand side scalars −C j (x) are con-                       discuss in Section 5.5.1. Constraints of this type can be solved in a
stant because they are evaluated at the location x before the system                      single step. Because the positions are immediately updated after a
is solved. When M = 3N and only equalities are present, the system                        constraint is processed, these updates will influence the lineariza-
can be solved by any linear solver, e.g. a preconditioned conjugate                       tion of the next constraint because the linearization depends on
gradient method. Once it is solved for ∆x the current solution is up-                     the actual positions. Asymmetry does not pose a problem because
dated as x ← x + ∆x. A new linear system is generated by evaluat-                         each constraint produces one scalar equation for one unknown La-
ing ∇C j (x) and −C j (x) at the new location after which the process                     grange multiplier λ. Inequalities are handled trivially by first check-
repeats.                                                                                  ing whether C(x) ≥ 0. If this is the case, the constraint is simply
                                                                                          skipped.
   If M 6= 3N the resulting matrix of the linear system is non-
symmetric and not invertible. Goldenthal et al. [GHF∗ 07] solve this                        The fact that each constraint is linearized individually before its
problem by using the pseudo-inverse of the system matrix which                            projection makes the solver more stable than a global approach in
yields the best solution in the least-squares sense. Still, handling                      which the linearizations are kept fixed for the entire global solve of
inequalities is not possible directly.                                                    a Newton iteration.
                                                                                             We have not considered the stiffness k of the constraint so far.
                                                                                          There are several ways to incorporate it. The simplest variant is
4.2.2. The Non-Linear Gauss-Seidel Solver
                                                                                          to multiply the corrections ∆x by k ∈ [0 . . . 1]. However, for multi-
In the PBD approach, non-linear Gauss-Seidel is used. It solves                           ple iteration loops of the solver, the effect of k is non-linear. The
each constraint equation separately. Each constraint yields a single                      remaining error for a single distance constraint after ns solver iter-
scalar equation C(x)  0 for all the particle positions associated                        ations is ∆x(1 − k)ns . To get a linear relationship we multiply the
with it. The subsystem is therefore highly under-determined. PBD                          corrections not by k directly but by k0 = 1 − (1 − k)1/ns . With this
solves this problem as follows. Again, given x we want to find a                          transformation the error becomes ∆x(1 − k0 )ns = ∆x(1 − k) and,
correction ∆x such that C(x + ∆x)  0. It is important to notice                          thus, becomes linearly dependent on k and independent of ns as de-
that PBD also linearizes the constraint function but individually for                     sired. However, the resulting material stiffness is still dependent on
each constraint. The constraint equation is approximated by                               the time step of the simulation. Real time environments typically
                                                                                          use fixed time steps in which case this dependency is not problem-
                    C(x + ∆x) ≈ C(x) + ∇C(x) · ∆x  0.                         (5)        atic.

The problem of the system being under-determined is solved by
                                                                                          4.2.3. Hierarchical Solver
restricting ∆x to be in the direction of ∇C which is also a require-
ment for linear and angular momentum conservation. This means                             The Gauss-Seidel method is stable and easy to implement but it
that only one scalar λ - a Lagrange multiplier - has to be found such                     typically converges significantly slower than global solvers. The
that the correction                                                                       main reason is that error corrections are propagated only locally
                                                                                          from constraint to constraint. Therefore, the Gauss-Seidel method
                               ∆x = λM−1 ∇C(x)T                                (6)        is called a smoother because it evens out the high frequency errors
                                                                                          much faster than low frequency errors.
solves Equation (5), where M = diag(m1 , m2 , . . . , mN ). This yields
the following formula for the correction vector of a single particle                         A popular method to increase the convergence rate of the Gauss-
i                                                                                         Seidel method is to create a hierarchy of meshes in which the coarse
                                                                                          meshes make sure that error corrections propagate fast across the
                              ∆xi = −λ wi ∇xi C(x)T ,                          (7)        domain. A smoother works on all meshes of the hierarchy one by
                                                                                          one while the error corrections are carried over across meshes of
where
                                                                                          different resolutions typically in multiple cycles from fine to coarse
                                             C(x)                                         levels and back. This technique is called the multi-grid method
                              λ=                                               (8)
                                     ∑ j w j |∇x j C(x)|2                                 [GW06]. Transferring corrections from coarse to fine meshes and

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                    J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

                                                                              Equation (12) can be seen as the first order optimality condition for
                                                                              the following minimization:
                                                                                                 1 n+1
                                                                                         min       (x   − x̃)T M(xn+1 − x̃) − ∆t 2 kCn+1                      (13)
                                                                                           x     2
                                                                              where x̃ is the predicted position, given by:
                                                                                                 x̃ = 2xn − xn−1 + ∆t 2 M−1 Fext                              (14)
                                                                                                       n          n       2    −1
                                                                                                   = x + ∆tv + ∆t M                 Fext .                    (15)
                                                                              Taking the limit as k → ∞ we obtain the following constrained
                                                                              minimization:
Figure 2: The construction of a mesh hierarchy: A fine level l is
                                                                                                    1 n+1
composed of all the particles shown and the dashed constraints.                              min      (x     − x̃)T M(xn+1 − x̃)
                                                                                               x    2                                  (16)
The next coarser level l + 1 contains the proper subset of black
particles and the solid constraints. Each fine white particle needs                          s.t.   Ci (xn+1 ) = 0, i = 1, . . . , n.
to be connected to at least k (=2) black particles – its parents –            We can interpret this minimization problem as finding the clos-
shown by the arrows.                                                          est point on the constraint manifold to the predicted position (in
                                                                              a mass-weighted measure). PBD approximately solves this mini-
                                                                              mization using a variant of the fast projection algorithm of Gold-
                                                                              enthal et al. [GHF∗ 07], which first takes a prediction step and then
from fine to coarse meshes is called prolongation and restriction,            iteratively projects particles onto the constraint manifold. PBD fol-
respectively. Multi-grid methods differ in the way the hierarchy is           lows this approach, but differs in the method used to solve the
created, in how the restriction and prolongation operators are de-            projection step. In contrast to [GHF∗ 07] PBD does not necessar-
fined and in what order the meshes are processed.                             ily linearize and solve the system as a whole in each Newton step.
   In [Mül08], Müller et al. used this technique and introduced Hi-           Instead, it linearizes one constraint at a time in a Gauss-Seidel fash-
erarchical Position Based Dynamics (HPBD). They define the orig-              ion as discussed in Section 4.2.1. This helps to make PBD robust
inal simulation mesh to be the finest mesh of the hierarchy and               in the presence of large constraint non-linearities.
create coarser meshes by only keeping a subset of the particles of               Projective Dynamics [BML∗ 14] presents a modification to PBD
the previous mesh. The hierarchy is traversed only once from the              that allows treating constraints in an implicit manner that does
coarsest to the finest level. Therefore, they only need to define a           not depend on the constraints being infinitely stiff. This is accom-
prolongation operator. By making sure that each particle of a given           plished by adding additional constraints that act to pull the solution
level is connected to at least two particles in the next coarser level        back towards the predicted (inertial) position.
(see Figure 2), prolongation amounts to interpolating the informa-
tion from adjacent particles of the coarser level. They also propose          4.2.5. Second Order Methods
a method to create distance constraints on the coarse meshes based
on the constraints of the original mesh. It is important to note that         Now we have established the connection to backward Euler, we
these coarse constraints must be unilateral, i.e. only act if the cur-        can apply higher order integration schemes to PBD. Following the
rent distance is larger than the rest distance otherwise they would           derivation in [EB08] we will adapt BDF2, a second order accurate
prevent bending and folding.                                                  multistep method. First, we write the second order accurate BDF2
                                                                              update equations:
   In Section 5.6 we describe a much simpler and effective way to
                                                                                          4       1           2
speed up error propagation for the specific but quite common case                 xn+1 = xn − xn−1 + ∆tvn+1                                                   (17)
of cloth that is attached to a kinematic or static object.                                3       3           3
                                                                                          4 n 1 n−1 2                         
                                                                                  vn+1
                                                                                       = v − v            + ∆tM−1 Fext + k∇Cn+1 .                             (18)
                                                                                          3       3           3
4.2.4. Connection to Implicit Methods
                                                                              Eliminating velocity and re-arranging gives
As Liu et al. [LBOK13] pointed out, PBD is closely related to im-                                               4
                                                                                                M xn+1 − x̃ = ∆t 2 k∇Cn+1 ,
                                                                                                  
plicit backward Euler integration schemes. We can see this by con-                                                                                            (19)
                                                                                                                    9
sidering backward Euler as a constrained minimization over posi-
tions. Starting with the traditional implicit Euler time discretization       where the inertial position x̃ is given by
of the equations of motion:                                                          4     1          8       2           4
                                                                                x̃ = xn − xn−1 + ∆tvn − ∆tvn−1 + ∆t 2 M−1 Fext . (20)
                n+1      n        n+1                                                3     3          9       9           9
              x       = x + ∆tv                                    (10)
                                                                            Equation (19) can again be considered as the optimality condition
                n+1      n        −1
              v       = v + ∆tM          Fext + k∇Cn+1             (11)       for a minimization of the same form as (16). Once the constraints
                                                                              have been solved, the updated velocity is obtained according to
where C is the vector of constraint potentials, and k is the stiffness,       (17),
we can eliminate velocity to give:
                                                                                                     1 3 n+1            1
                                                                                                                              
                                                                                            vn+1 =             − 2xn + xn−1 .              (21)
    M(xn+1 − 2xn + xn−1 − ∆t 2 M−1 Fext ) = ∆t 2 k∇Cn+1 .
                                                                                                          x
                                                                   (12)                              ∆t 2               2

                                                                                                                                              ©
                                                                                                                                                 2017 The Author(s)
                                                                                                       Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

To evaluate this more accurate scheme we need only store the previ-                     5. Specific Constraints
ous position and velocity, and perform some additional basic arith-
                                                                                        In the following we will introduce different constraints that can be
metic during the prediction and velocity update steps, while the
                                                                                        used to simulate a variety of materials such as articulated rigid bod-
rest of the PBD algorithm is unchanged. The benefits of this simple
                                                                                        ies, soft bodies, cloth or even fluids with PBD. For better readability
modification are an order of magnitude less numerical damping,
                                                                                        we define xi, j = xi − x j .
and faster convergence for the constraint projection. This can be
understood by considering the algorithm as using previous time-
step information in order to generate predicted positions that stay                     5.1. Stretching
closer to the constraint manifold, making projection faster.
                                                                                       To give an example, let us consider the distance constraint function
                                                                                       C(x1 , x2 ) = |x1,2 | − d. The derivatives with respect to the points
4.2.6. XPBD                                                                                                                                        x
                                                                                       are ∇x1 C(x1 , x2 ) = n and ∇x2 C(x1 , x2 ) = −n with n = |x1,2 | . The
                                                                                                                                                          1,2
One limitation of PBD described so far is that the stiffness of con-                    scaling factor λ is, thus, λ =
                                                                                                                         |x1,2 |−d
                                                                                                                           1+1 and the final corrections
straints is dependent on the time-step size and iteration count used
                                                                                                                     w1
for the constraint solver. In the limit of infinite constraint iterations,                                 ∆x1 = −         (|x1,2 | − d) n
the constraints will become infinitely stiff. Surprisingly this con-                                               w1 + w2
                                                                                                                     w2
vergence to an infinitely stiff solution occurs regardless of how the                                      ∆x2 = +         (|x1,2 | − d) n,
constraint stiffness coefficients are set.                                                                         w1 + w2
                                                                                        which are the formulas proposed in [Jak01] for the projection of
   The problem of time-step and iteration count dependent stiffness                     distance constraints (see Figure 3). They can be derived as a special
in PBD was addressed with an extension called XPBD [MMC16].                             case of the general constraint projection method.
XPBD derives from a compliant constraint formulation [SLM06]
that associates an inverse stiffness, or compliance, α = 1k with each
constraint.
   The derivation of XPBD shows that we can think of the λ calcu-
lated for each constraint during a PBD iteration as an incremental
change to a total multiplier. This modifies equation (9) in regular
PBD as follows                                                                          Figure 3: Projection of the constraint C(x1 , x2 ) = |x1,2 | − d. The
                                                                                        corrections ∆xi are weighted according to the inverse masses wi =
                                                                                        1/mi .
                                     −C(x) − α̃λ
                        ∆λ =                          .                     (22)
                                 ∇C(x)M−1 ∇C(x)T + α̃

    Here α̃ = ∆tα2 is the time-step scaled compliance parameter.                        5.2. Bending

   Now, after each iteration we not only update the system posi-                        In cloth simulation it is important to simulate bending in addition to
tions, we also update each constraint’s total Lagrange multiplier as                    stretching resistance. To this end, for each pair of adjacent triangles
follows                                                                                 (x1 , x3 , x2 ) and (x1 , x2 , x4 ) a bilateral bending constraint is added
                                                                                        with constraint function
                                      λ = λ + ∆λ                            (23)
                                                                                                                Cbend (x1 , x2 , x3 , x4 ) =
                                      x = x + ∆x.                           (24)
                                                                                                            x2,1 × x3,1 x2,1 × x4,1
                                                                                                                                              
                                                                                                      acos               ·                         − ϕ0
                                                                                                           |x2,1 × x3,1 | |x2,1 × x4,1 |
   The additional terms in the denominator of (22) act to limit the
amount of force a constraint can apply, specifically as λ grows,                        and stiffness kbend . The scalar ϕ0 is the initial dihedral angle be-
the incremental constraint change becomes smaller. In the case of                       tween the two triangles and kbend is a global user parameter defin-
zero compliance (α = 0) we obtain exactly the same formulation as                       ing the bending stiffness of the cloth (see Figure 4). The advan-
regular PBD, corresponding to infinitely stiff constraints (9).                         tage of this bending term over adding a distance constraint between
                                                                                        points x3 and x4 is that it is independent of stretching. This is be-
   The total Lagrange multiplier λ has a useful interpretation. It is a                 cause the term is independent of edge lengths. In Figure 9 we show
measure of the total force applied by the constraint to the particles,                  how bending and stretching resistance can be tuned independently.
this is a physical quantity that can be used to drive haptic devices,
or force dependent effects.
                                                                                        5.3. Isometric Bending
    We note that XPBD does not make PBD converge faster, the
same number of iterations would be required to reach a stiff solu-                      A bending constraint for inextensible surfaces was introduced
tion. However, XPBD does return a consistent solution that corre-                       in [BKCW14]. The definition of this constraint is based on the dis-
sponds to a well-defined energy potential. As in PBD, if the solver                     crete isometric bending model of Bergou et al. [BWH∗ 06], which
is terminated before convergence then this will manifest as artificial                  can be applied if a surface deforms isometrically, i.e., if the edge
compliance of the constraints.                                                          lengths remain invariant. Since many textiles cannot be stretched

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                       J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 4: For bending resistance, the constraint function
C(x1 , x2 , x3 , x4 ) = arccos(n1 · n2 ) − ϕ0 is used. The actual dihe-
dral angle ϕ is measured as the angle between the normals of the
two triangles.




significantly, this method is an appropriate choice in garment sim-
ulation.
   For each interior edge ei a stencil s is defined which consists of
                                                                                  Figure 6: A heavy sphere is pushing down a piece of cloth that
the two triangles adjacent to ei . The vector xs = (x0 , x1 , x2 , x3 )T
                                                                                  is thrown over four statues. Realistic wrinkles evolve due to the
contains the four vertices of the stencil and the vector es =
                                                                                  isometric bending constraint.
[x0 x1 , x1 x2 , x2 x0 , x0 x3 , x3 x1 ] contains the five stencil edges start-
ing with the common edge (see Figure 5).

                                     x1
                           e1                   e4
                   x2                   e0               x3
                           e2                   e3                                Figure 7: Constraint function C(q, x1 , x2 , x3 ) = (q − x1 ) · n − h
                                     x0                                           makes sure that q stays above the triangle x1 , x2 , x3 by the cloth
                                                                                  thickness h.
Figure 5: The isometric bending constraint is defined using the the
stencil of an interior edge e0 .
                                                                                  5.4. Collisions
  Using the isometric bending model the local Hessian bending                     5.4.1. Triangle Collisions
energy of a stencil is determined by
                                                                                  Self collisions within cloth can be handled by additional unilateral
                                     3                                            constraints. For vertex q moving through a triangle x1 , x2 , x3 , the
                           Q=             KT K,
                                  A0 + A1                                         constraint function reads
where A0 and A1 are the areas of the adjacent triangles and K is the                                                             x2,1 × x3,1
                                                                                              C(q, x1 , x2 , x3 ) = (q − x1 ) ·                − h,
vector                                                                                                                          |x2,1 × x3,1 |

        K = (c01 + c04 , c02 + c03 , −c01 − c02 , −c03 − c04 ),                   where h is the cloth thickness (see Figure 7). If the vertex enters
                                                                                  from below with respect to the triangle normal, the constraint func-
where c jk = cot ∠e j , ek . The matrix Q ∈ R4×4 is constant and can              tion has to be
be precomputed with the initial configuration of the stencil. The                                                               x3,1 × x2,1
local Hessian bending energy can be used to define a bending con-                            C(q, x1 , x2 , x3 ) = (q − x1 ) ·                − h.
                                                                                                                               |x3,1 × x2,1 |
straint as
                                      1
                      Cbend (xs ) =          Qi, j xTi x j .                      5.4.2. Environment Collisions
                                      2∑i, j
                                                                                  Collisions between particles and kinematic shapes, represented as
Since the Hessian bending energy is constant, the gradients are de-               e.g.: triangle or convex meshes, can be handled by first detecting
termined by                                                                       a set of candidate contact planes for each particle, then for each
                                                                                  contact plane normal n, a non-penetration constraint is introduced
                           ∂Cbend
                                  = ∑ Qi, j x j .                                 into the system of the form
                            ∂xi     j
                                                                                                        C(x) = nT x − drest = 0,                                 (25)
  Figure 6 shows a cloth simulation with the introduced bending                   where drest is the distance the particle should maintain from the
constraint.                                                                       geometry at rest.

                                                                                                                                                 ©
                                                                                                                                                    2017 The Author(s)
                                                                                                          Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

                                                                                        Friction with kinematic shapes is handled using the same method,
                                                                                        with the shape treated as having infinite mass and the contact plane
                                                                                        defined by its geometry.


                                                                                        5.5. Volume Conservation
                                                                                        The conservation of volume plays an important role in the dynamic
                                                                                        simulation of deformable bodies [HJCW06, ISF07, DBB09]. Since
                                                                                        most soft biological tissues are incompressible, this is an essential
Figure 8: A sand castle before collapse (left). After 300 frames the                    extension in the field of medical simulation. However, it is also used
position-based friction model maintains a steep pile (middle), while                    in the field of shape modeling [vFTS06] since volume conserving
the velocity level friction model has almost completely collapsed                       deformations appear more realistic.
(right).
                                                                                        5.5.1. Tetrahedral Meshes

5.4.3. Particle Collisions                                                              For tetrahedral meshes it is useful to have a constraint that con-
                                                                                        serves the volume of single tetrahedron. Such a constraint has the
Collisions between particles can be handled in a similar manner                         form
to the environment by linearizing and introducing a contact plane,
                                                                                                                           1
however, it is often more robust to maintain the non-linear nature
                                                                                                                                        
                                                                                                   C(x1 , x2 , x3 , x4 ) =   x2,1 × x3,1 · x4,1 −V0 ,
of the constraint, in the form:                                                                                            6
                                                                                       where x1 , x2 , x3 and x4 are the four corners of the tetrahedron and
                       C(xi , x j ) = |xi j | − (ri + r j ) ≥ 0,            (26)
                                                                                       V0 is its rest volume. In a similar way, the area of a triangle can be
where ri and r j are the radii of the two particles. This constraint can               kept constant by introducing
be used to model granular-like materials as shown in [MMCK14].                                                                             1
                                                                                                          C(x1 , x2 , x3 ) =                 x2,1 × x3,1 − A0 .
5.4.4. Friction                                                                                                                            2

Müller et al. [MHHR07] handled friction by introducing damping
forces applied after the constraint solve. This approach is suitable                    5.5.2. Cloth Balloons
for weak frictional effects, but cannot model static friction, because                  For closed triangle meshes, overpressure inside the mesh as shown
the positional constraints can freely violate the frictional forces. To                 in Figure 10 can easily be modeled with an equality constraint con-
model situations where friction is strong relative to the constraints                   cerning all N vertices of the mesh:
(see Figure 8), Macklin et al. [MMCK14] include frictional effects                                                                   !
                                                                                                                  n
as part of the position level constraint solve.                                                                                triangles
                                                                                              C(x1 , . . . , xN ) =             ∑ (xt × xt ) · xt
                                                                                                                                             i       i       i   − kpressureV0 .
                                                                                                                                             1       2       3
   Once interpenetration between particles has been resolved, a                                                                i=1
frictional position delta is calculated based on the relative tangen-
tial displacement of the particles during this time-step. The relative                  Here t1i ,t2i and t3i are the three indices of the vertices belonging to
displacement is given by                                                                triangle i. The sum computes the actual volume of the closed mesh.
                                                                                        It is compared against the original volume V0 times the overpres-
                 ∆x⊥ = (x∗i − xi ) − (x∗j − x j ) ⊥ n,            (27)
                                                
                                                                                        sure factor kpressure . This constraint function yields the gradients
where x∗i and x∗j are the current candidate positions for the colliding                    ∇xi C = ∑ (xt j × xt j ) + ∑ (xt j × xt j ) + ∑ (xt j × xt j ).
particles, including any previously applied constraint deltas, xi and                                j:t1j =i
                                                                                                                    2      3
                                                                                                                                      j:t2j =i
                                                                                                                                                 3       1
                                                                                                                                                                 j:t3j =i
                                                                                                                                                                            1      2

x j are the positions of the particles at the start of the time-step, and
n = x∗i j /|x∗i j | is the contact normal. The frictional position delta for            These gradients have to be scaled by the scaling factor given in
particle i is then computed as                                                          Equation (8) and weighted by the masses according to Equation (7)
                           (                                                            to get the final projection offsets ∆xi .
                     wi      ∆x⊥ ,                   |∆x⊥ | < µs d
      ∆xi =                              µk d                          (28)
                wi + w j ∆x⊥ · min( |∆x | , 1), otherwise                               5.5.3. Surface Meshes
                                                 ⊥

where d is the penetration depth, and µk , µs are the coefficients of                   In the following we introduce the position-based approach for vol-
kinetic and static friction, respectively. The first case in Eq. (28)                   ume conservation of Diziol et al. [DBB11]. This method considers
models static friction by removing all tangential movement when                         only the surface of a simulated object and does not require interior
the particle’s relative velocity is below the traction threshold. The                   particles which reduces the computational effort. The volume V of
second case models kinetic Coulomb friction, limiting the frictional                    a volumetric 3D shape V can be determined by using the divergence
position delta based on the penetration depth of the particle. The                      theorem as proposed in [Mir96] and [HJCW06]:
position change on particle j is given by                                                                   ZZZ                             ZZ
                                      wj                                                                                ∇ · x dx =               xT n dx = 3V,                         (30)
                         ∆x j = −           ∆xi .                 (29)
                                   wi + w j                                                                     V                           ∂V

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                       J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 9: The image shows a mesh that is simulated using stretching and bending constraints. The top row shows (kstretching , kbending ) =
                         1
(1, 1), ( 12 , 1) and ( 100 , 1). The bottom row shows (kstretching , kbending ) = (1, 0), ( 12 , 0) and ( 100
                                                                                                            1
                                                                                                               , 0).



                                                                                 servation, respectively, and the user-defined value α ∈ [0, 1] is used
                                                                                 to blend between both. The vector ∆xi contains the total position
                                                                                 change of the i-th. Hence, strongly deformed particles participate
                                                                                 more in volume correction. The weight of a colliding particle is set
                                                                                 to zero in order to ensure that a collision constraint is not violated
                                                                                 during the position correction for the volume conservation. Finally,
                                                                                 the weights are smoothed by a Laplacian filter.
     Figure 10: Simulation of overpressure inside a character.
                                                                                     Diziol et al. also propose another definition for the local weights
                                                                                 wli . To propagate volume changes through the object, they first de-
                                                                                 termine pairs of opposing particles in a pre-processing step by in-
where ∂V is the boundary of the shape and n is the surface normal.               tersecting the geometry with multiple rays. For each particle i one
If the boundary is given as triangle mesh, the integral can be written           particle k on the opposite side of the volumetric body is stored.
as sum over all triangles i:                                                     Then they choose a local weight which does not only depend on the
                1                    1                                           position change ∆xi of a particle but also on the distance changes
                    ZZ
     V (X) :=            xT n dx =       Ai (xi1 + xi2 + xi3 )T ni ,   (31)
                3                    9∑i
                                                                                 ∆di of the corresponding particle pairs:
                    ∂V
where Ai is the area and i1 , i2 and i3 are the vertex indices of the i-th                                 βsi ∆di + (1 − β)k∆xi k
                                                                                                wli =                                  ,
triangle. Now we can define a volume constraint C := V (X) −V0 =                                        ∑ j βs j ∆d j + (1 − β)k∆x j k
0 and compute a corresponding position correction (see Section 4):
                                                                                 where si is a user-defined stiffness parameter and β ∈ [0, 1] is used
                                                                                 to define the influence of the distance changes.
                                 wiC(X)
                ∆xVi = −                       ∇xi C(X).               (32)
                            ∑ j j k∇x j C(X)k2
                               w                                                    Analogous to the positions correction we perform a velocity cor-
The weights wi are used to realize a local volume conservation (see              rection to fulfill the constraint ∂C/∂t = 0. This leads to a divergence
below). The gradient can be approximated by                                      free velocity field.

                                1                                                  In Figure 11 different configurations for the presented volume
                     ∇C(X) ≈ [nT1 , . . . , nTn ]T ,
                                3                                                conservation method are compared with each other.
where ni = ∑ A j n j is the sum of the area weighted normals of all
triangles which contain particle i.
                                                                                 5.5.4. Robust Collision Handling with Air Meshes
  The weights in Equation (32) are chosen as follows:
                               g               k∆xi k          g  1              As Müller et al. show in [MCKM15], per-element volume con-
      wi = (1 − α)wli + αwi ,         wli =               ,   wi = ,             straints can also be used to robustly handle collisions. To this end,
                                              ∑ j k∆x j k         n
                                                                                 they tessellate the air between objects. Collisions can then be pre-
                 g
where wli and wi are the weights for local and global volume con-                vented by making sure that the air elements do not invert with the

                                                                                                                                                  ©
                                                                                                                                                     2017 The Author(s)
                                                                                                           Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

                                                                                        5.6. Long Range Attachments
                                                                                        Recently, Kim et al. [KCM12] found a surprisingly simple and ro-
                                                                                        bust technique they call Long Range Attachments (LRA) to pre-
                                                                                        vent cloth from getting stretched globally with low iteration counts.
                                                                                        Their method exploits the fact that stretching artifacts almost al-
                                                                                        ways appear when cloth is attached. In this case, instead of only
                                                                                        applying attachment constraints to the subset of the vertices near
                                                                                        the region where the cloth is attached and relying on error prop-
                                                                                        agation of the solver for all other vertices, they apply unilateral
                                                                                        attachment constraints to all the vertices by attaching each vertex
                                                                                        to one or more attachment point directly. The rest lengths of these
                                                                                        long range attachments can either be set to the Euclidean distance
                                                                                        in the rest state or via measuring geodesic lengths along the cloth.
                                                                                        Figure 14 demonstrates the method on a single rope attached at one
                                                                                        end. The method allows the simulation of a piece of cloth with 90K
                                                                                        vertices at interactive rates as shown in Figure 15.


                                                                                        5.7. Strands
                                                                                        A similar approach was recently proposed by Müller et al.
                                                                                        [MKC12] to guarantee zero stretch in a single pass for the case of
Figure 11: Four spheres with different volume conservation                              attached ropes. This approach allows the simulation of thousands
squeezed by a plate. Left to right: global conservation, local con-                     of hair strands in real time (see Figure 16). Figure 17 visualizes
servation with distance constraints, local conservation without dis-                    the basic idea. Particle x1 is attached. To satisfy the first distance
tance constraints and no volume conservation. The maximum vol-                          constraint, particle x2 is moved towards x1 such that their mutual
ume loss was 0.6%, 0.7%, 0.7% and 40% respectively.                                     distance is l0 . Particle x3 is then moved towards the new position
                                                                                        of x2 and similarly along the chain until the last particle is reached.
                                                                                        After this single pass, all the distance constraints are satisfied.
                                                                                        This method is called Follow The Leader (FTL). While LRA
                                                                                        guarantees zero stretch of all the particles w.r.t. the attachment
                                                                                        points, the constraint between consecutive particles can still re-
unilateral constraints                                                                  main overstretched. On the other hand, in contrast to LRA which is
                                                                                        momentum conserving, FTL introduces unphysical behavior. Not
        Cair element (x1 , x2 , x3 , x4 ) = x2,1 × x3,1 · x4,1 ≥ 0 and                  projecting distance constraints symmetrically means that a system
                                                       

             Cair element (x1 , x2 , x3 ) = x2,1 × x3,1 ≥ 0                             is simulated for which each particle has infinitely more mass than
                                                                                        its successor. To compensate for this behavior, the authors replace
in 3D and 2D, respectively. When the volume of an air element is                        the PBD velocity update vi ← (pi − xi )/∆t in Algorithm 1 by
positive, the element is passive, does not disturb the simulation and                                            pi − xi            −di+1
causes no computational cost. The main advantage of air meshes                                            vi ←           + sdamping       ,
                                                                                                                    ∆t               ∆t
over existing collision handling methods is that air meshes have a                      where di+1 is the position correction applied to particle i + 1 and
memory. Even if a scene is completely flattened as shown in Figure                      sdamping ∈ [0, 1] a scaling factor do influence damping. While this
12, the objects pop up in the correct order when released. This is                      modification of DFTL (dynamic FTL) hides the unphysical behav-
particularly useful in the simulation on complex clothing as shown                      ior of FTL, it introduces a certain amount of damping which is
in Figure 13. Air meshes not only detect entangled states easily,                       acceptable for the simulation of hair and fur as the author’s results
they also allow the smooth recovery from arbitrary entangled states                     show.
which is a hard problem as the literature on this topic shows.

   Müller et al. note that when large relative translations and rota-
                                                                                        5.8. Continuous Materials
tions between objects occur, the air elements can lock and report
collisions in a collision free state. The authors solve this problem                    Recently, position-based methods based on a continuum-based for-
by running a mesh optimization step. They perform edge flips in                         mulation were presented. In the following we introduce three meth-
2D and generalized edge flips in 3D whenever they improve the                           ods which use this formulation. The first method defines a con-
mesh quality. This step prevents locking - not provably but in all                      straint for the strain energy of a deformable solid [BKCW14] while
practical examples. In 2D, the optimization step is fast and allows                     the second one directly constrains the strain tensor [MCKM14].
the simulation of arbitrary scenarios. In 3D, mesh optimization is                      The third method constrains the strain measures of one dimensional
significantly more expensive. Fortunately, in the case of complex                       elastic bodies, so called Cosserat rods, which can undergo bending
clothing, locking does not cause disturbing visual artifacts.                           and twisting deformations [KS16].

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                  J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 12: With air mesh based collision handling, both the characters themselves as well as their spacial order is recovered from a
completely flat state.




Figure 13: Smooth recovery from a severely entangled cloth state
using an air mesh for collision handling.




                                                                            Figure 15: Simulation of a piece of cloth with 90K vertices at 20fps
                                                                            on a GPU using LRA.



                                                                            which maps a point X in material space to its corresponding de-
                                                                            formed location x in world space using a continuous displacement
                                                                            field u. The Jacobian of this function F = ∂X , also known as de-
                                                                                                                        ∂φ(X)

                                                                            formation gradient, is used to determine the non-linear Green strain
Figure 14: The Long Range Attachments (LRA) method used to                  tensor
simulate an inextensible rope attached at one end. Each particle is                                       1 T        
                                                                                                     ε=      F F−I ,                        (33)
constrained or remain inside a sphere centered at the attachment                                          2
point (red) whose radius is the initial distance from the particle to       where I denotes the identity matrix. Hooke’s generalized law gives
the attachment. For each configuration, target positions are shown          us the relation between stress and strain
in green when particles need to be projected. Particles inside the
constraint spheres are allowed to move freely.                                                               S = Cε,
                                                                            where C is the elasticity tensor which defines the elastic behavior of
                                                                            the material. For isotropic materials this relationship is called Saint-
                                                                            Venant Kirchhoff model, where C is defined by two independent
5.8.1. Strain Energy Constraint                                             variables, often expressed by the engineering constants Young’s
                                                                            modulus k and Poisson ratio ν. The energy of a deformed solid
In continuum mechanics the deformation of a body is defined by
                                                                            is defined by integrating the scalar strain energy density field
the function
                                                                                                       1       1
                        φ(X) = X + u = x,                                                          Ψs = ε : S = tr(εT S)
                                                                                                       2       2

                                                                                                                                            ©
                                                                                                                                               2017 The Author(s)
                                                                                                     Eurographics Proceedings © 2017 The Eurographics Association.
                                               J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 16: Dynamic FTL allows the simulation of every hair strand in real time. From left to right: 47k hair strands simulated at 25 fps
including rendering and hair-hair repulsion. Long hair composed of 1.9m particles at 8 fps. Curly hair using visualization post-processing.



                       x1                                                                 where V is the undeformed volume of the element. Additionally,
                                                                                          the position-based solver requires the gradients of the constraint
                              l0
                                                                                          ∇Cxi = ∂Es /∂xi which are determined by
                                                                                                                                             3
                                   l0                                                            ∂Es ∂Es ∂Es
                                                                                                                 = V P(Ftet )D−T
                                                                                                                              m ,
                                                                                                                                     ∂Es
                                                                                                                                         =−∑
                                                                                                                                                  ∂Es
                                                                                                                                                      ,
                                                                                                 ∂x1 ∂x2 ∂x3                         ∂x4      i=1 ∂xi
                         x2
                                            l0                                            where P(F) = FCε is the first Piola-Kirchhoff stress tensor.
                                                                                             Note that common constitutive models are not designed to han-
                                         x3                                               dle degenerate or inverted tetrahedral elements. However, this prob-
                                                                                          lem can be solved by using the inversion handling of Irving et
                                                                x4
                                                                                          al. [ITF04].
Figure 17: Follow The Leader (FTL) projection. Starting from the                            The constraint of a triangular element is defined analogously
attachment down, each particle is moved directly towards its pre-
decessor such that their mutual distance constraint is satisfied.                                              C(x) = Es (x) = AΨ(Ftri ),
                                                                                          where A is the area of the undeformed triangle. The constraint gra-
                                                                                          dients of the three vertices are determined by
over the entire body Ω:
                                                                                                                                           2
                                                                                                                = AP(Ftri )D−T
                                                                                                     ∂Es ∂Es                        ∂Es         ∂Es
                                                                                                                              m ,        =−∑        .
                                           Z                                                         ∂x1 ∂x2                        ∂x3     i=1 ∂xi
                                   Es =           Ψs dX,                      (34)
                                              Ω
                                                                                             The proposed energy constraint formulation [BKCW14] has the
where tr(·) is the trace of a matrix.
                                                                                          advantage that it can handle complex physical effects like lateral
   In order to simulate deformable solids with the position-based                         contraction, anisotropy or elastoplasticity (see Figure 18, right).
approach an energy constraint C(x) = Es (x) = 0 is defined. A dis-                        Moreover, it is not limited to the introduced Saint-Venant Kirchhoff
cretization of the solid is required to compute the energy. We use                        model, also other material models like e.g. the Neo-Hookean model
tetrahedral meshes for volumetric bodies and triangle meshes for                          are supported. Finally, Bender et al. [BKCW14] demonstrated that
surface models in combination with linear Lagrangian shape func-                          this approach is very efficient and even faster than shape matching.
tions to discretize the body. For linear shape functions the deforma-                     Therefore, the method allows to simulate complex scenes with a
tion gradient of a tetrahedral element is determined by                                   high number of elements (see Figure 18, left).
                                    Ftet = Ds D−1
                                               m ,                                        5.8.2. Strain Based Dynamics
where Ds is the deformed shape matrix and Dm the constant refer-                          In [MCKM14] the authors propose another position-based method
ence shape matrix defined by the vertices of the tetrahedral element                      based on continuum mechanics which allows the control of stretch
             Ds = x1 − x4 x2 − x4 x3 − x4
                                                                                         and shear deformations independent of the tessellation of the mesh.
                                                                                         The basic idea is to force the components of Green’s strain tensor ε
             Dm = X1 − X4 X2 − X4 X3 − X4 .                                               defined in Equation (33) to zero by introducing one constraint per
The deformation gradient Ftri ∈ R2×2 for a triangular element is                          independent component
defined analogously in the two-dimensional space of the triangle                                             Cstretch (x) = Sii − 1                      (35)
plane.                                                                                                        Cshear (x) = Si j       i < j,             (36)
    The constraint of a tetrahedral element can now be defined as
                                                                                          where S = FT F and x defines the positions of the four particles
                           C(x) = Es (x) = V Ψs (Ftet ),                                  adjacent to a tetrahedral element or the three particles adjacent to

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 18: Position-based simulation using the strain energy constraint. Left: 100 Stanford Armadillos with 371700 tetrahedral elements
falling through a funnel. Right: Elastoplastic Stanford Dragon is deformed persistently due to the weight of a heavy sphere.



                                                                          a triangle. In the soft body case there are three stretch and three
                                                                          shear constraints where as there are two stretch and one shear con-
                                                                          straint in the cloth case. The paper above gives the explicit update
                                                                          formulas derived from these constraints.
                                                                             The stretch constraints formulated as in Equation (35) are
                                                                          quadratic along the gradient and can therefore not be solved in a
                                                                          single step. This problem can be fixed by defining the stretch con-
                                                                          straints as
                                                                                                              p
                                                                                                Cstretch (x) = Sii − 1,
                                                                          which is linear along the constraint gradient.
                                                                              The shear constraint function Si j can also be written as Si j =
                                                                          fi · f j , where fi and f j are the ith and jth column vectors of F. How-
                                                                          ever, this function not only penalizes the angle between the axes
                                                                          of the deformed coordinate system, i.e. the dot product of the col-
                                                                          umn vectors, but also the principal stretches, i.e. the magnitudes of
                                                                          the column vectors. The following modification of Equation (36)
                                                                          decouples strain from stretch
                                                                                                                      fi · f j
                                                                                                   Cshear (x) =                  .
                                                                                                                     |fi ||f j |

                                                                             Figure 19 shows Strain Based Dynamics on cloth in action. Even
                                                                          though the tessellation of the mesh is not aligned with the principal
Figure 19: Varying the cloth stiffness parameters of different            directions, stretch and shear w.r.t. to those directions can be con-
strain components. From top to bottom the resistance to x-stretch,        trolled. In Figure 20, the deformation of a torus is controlled by
y-stretch and shear are: (high,high,high), (hight,high,low) and           varying the stiffnesses of the volume, stretch and shear constraints.
(low,high,high). Our method allows the control of these modes in-
dependently on triangle meshes with highly non-regular tessella-
tions as the one used here.                                               5.8.3. Elastic Rods
                                                                          In continuum mechanics elastic rods are modeled as a smooth curve
                                                                          r(s) : [s0 , s1 ] → R3 with curve parameter s which is called cen-
                                                                          terline. To simulate bending and twisting motion, an orthonormal
                                                                          frame with basis vectors {d1 (s), d2 (s), d3 (s)} is attached to each
                                                                          point of the centerline. The vectors d1 and d2 span the plane of the
                                                                          rod’s cross section and d3 = d1 × d2 is the cross section normal.
                                                                          Given a world coordinate system with the basis {e1 , e2 , e3 } the vec-

                                                                                                                                          ©
                                                                                                                                             2017 The Author(s)
                                                                                                   Eurographics Proceedings © 2017 The Eurographics Association.
                                              J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 20: Varying soft body stiffness parameters. Figures (a) - (d) show the recovery of a torus from a heavily entangled state by increasing
the volume stiffness. For (e) we reduced all but the volume conservation stiffness values. As a result, the torus heavily deforms but its volume
is conserved. Figure (f) shows the result of only softening the volume stiffness and the stiffness along the main axis of the torus. The result of
high shear and low stretch resistance is shown in Figure (g) where angle distortion is small while the shape is stretched. Figure (h) shows
the opposite configuration. Here, stretching is small while the torus bends heavily.


                                     q    1
                                       i+ 2         Ω
                q                                               q      3                    To achieve simpler and faster computations, we replace the iner-
                     1               Ωx                             i+ 2
                  i− 2
                             xi                                                          tia tensor I of the frame with a scalar mass mq so that the inverse
                                                                           xi+2          tensor is just the inverse mass wq . This yields the displacements
                                  Ωy          Ωz
        xi−1                                        xi+1                                                     ∆p1 = + w +ww+4w
                                                                                                                          1l
                                                                                                                                C,
                                                                                                                              l2 s
                                                                                                                        1   2     q


               Figure 21: The geometry of the discrete rod.                                                  ∆p2 = − w +ww+4w
                                                                                                                          2l
                                                                                                                                C,
                                                                                                                              l2 s
                                                                                                                        1   2     q

                                                                                                                        w l2
                                                                                                              ∆q = − w +w q+4w l 2 C̃s qẽ3 .            (37)
                                                                                                                      1  2    q


tors dk can be represented as rotated basis vectors dk = qẽk q̄ with                      The bending and torsion constraint for two adjacent quaternions
the rotation quaternion q(s) and the conjugate quaternion q̄(s).                         q1 and q2 becomes
   The strain measure Γ(s) measures the deviation of tangent of the                              Cb (q1 , q2 ) = = q̄1 q2 − q̄01 q02 = Ω − αΩ0 = 0,
                                                                                                                                   
centerline and the cross section normal d3 , which is called shear
                                                                                                             +1 if |Ω − Ω0 |2 ≤ |Ω + Ω0 |2
                                                                                                          (
deformation:
                                                                                                    α=
                              ∂                                                                              −1 if |Ω − Ω0 |2 > |Ω + Ω0 |2 ,
                      Γ(s) = r(s) − d3 (s).
                              ∂s
                                                                                         where α is required to get a unique constraint function since q and
Further it measures stretch or compression of the rod because d3                         −q describe the same rotation which means that the rest pose Dar-
has unit length and we assume that in the rest pose r(s) is a unit                       boux vector is not unique. The displacements drive the rod towards
speed parametrization. A second strain measure for bending and                           the rest pose, which is nearer to the current configuration. They can
torsion deformations is defined using the Darboux vector Ω:                              be computed with the following formulas:
                                                  0
                                                    !
                                                                                                                            w
                                                                                                                           q1
                                     ∂q      0 ∂q                                                               ∆q1 = + wq +w   q2 C̃b ,
             ∆Ω = Ω − Ω0 = = 2q̄ − 2q̄                ,                                                                     1 q  2
                                     ∂s         ∂s                                                                          w
                                                                                                                           q2
                                                                                                                ∆q2 = − wq +w q
                                                                                                                                q1 C̃b .
                                                                                                                            1    2
where =(·) denotes the imaginary or vector part of a quaternion and
the superscript 0 denotes values in rest pose. The Darboux vector                           It is important to normalize the quaternions after the displace-
describes the rate of change of the basis vectors dk when the curve                      ments are applied, because only unit quaternions represent proper
parameter s is varied and it is the spatial analog of the angular ve-                    rotations.
locity.
                                                                                           An example of a complex rod simulation is shown in Figure 22.
   For position-based simulation the rod is discretized as line seg-
ments and the mass is lumped in particles at their endpoints (see
Figure 21). The frames are attached to the midpoints of the line                         5.9. Rigid Body Dynamics
segments, which is the commonly used staggered grid discretiza-                          The position-based simulation method is not limited to particle-
tion. The strain measures are discretized using finite differences.                      based models. It can also be used to simulate articulated rigid body
Thereby the Darboux vector at the particle positions has to be in-                       systems with joint and contact constraints [DCB14].
terpolated from the two adjacent quaternions, which is not unique.
The stretch and shear constraint for two adjacent particles with po-                        A particle has three translational degrees of freedom (DOF). In
sitions p1 and p2 and the quaternion q in between becomes                                addition a rigid body has three rotational ones. We parameterize
                                                                                         the rotation by a vector ϑ which represents a rotation of |ϑ| about
                 Cs (p1 , p2 , q) = 1l (p2 − p1 ) − d3 (q) = 0.                          the axis ϑ/ |ϑ| in order to define constraint functions C(x, ϑ) for

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                        J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 22: Slinky walking down a stairway. It has 50 curls and is modeled with 1000 discrete rod elements. It was simulated using 50 solver
iterations and took 7 ms per simulation step (without collision detection) on a single core of an Intel Core i5 CPU.



positions and orientations. The vector ϑ is also known as the ex-                    In the following we describe how the position and orientation
ponential map [Gra98]. Analogous to Equation (5) each constraint                  corrections are computed for rigid bodies. Analogous to Equa-
for rigid bodies is approximated by a linearization of the constraint             tions (5)-(8) first a Lagrange multiplier λ is determined by solving
equation:
                                                                                                         JM−1 JT λ = −C(x, ϑ).                                    (39)
                                                          T
       C(x + ∆x, ϑ + ∆ϑ) ≈ C(x, ϑ) + J(x, ϑ) ∆xT , ∆ϑT .
                                                                                  Then the Lagrange multiplier is used to compute the position and
   However, instead of formulating constraints with respect to x and              orientation change of the linked rigid bodies
ϑ it is easier and more intuitive to use the concept of connectors                                    h           i
which was introduced by Witkin et al. [WGW90]. A connector can                                          ∆xT , ∆ϑT = M−1 JT λ.                 (40)
be a point or vector in local coordinates of a rigid body which is
used to define a constraint. The definition of connectors allows to                  The position-based solver for rigid bodies works analogously
formulate generic constraints without knowledge about the body it-                to the one for particles. Each constraint is linearized individually
self. For example a ball joint which removes all translational DOFs               and position and orientation corrections are determined in a Gauss-
between two linked bodies is defined by the constraint                            Seidel fashion.

                    C(P1 , P2 ) = P1 − P2 = 0,                                       Collisions can be simulated by defining inequality constraints
                                                                                  for colliding rigid bodies (see Figure 23, right). These constraints
where P1 and P2 are connector points in the first and second body,                can be handled similar to unilateral particle constraints [DCB14].
respectively.                                                                     Moreover, servo motors can be simulated by combining hinge or
  The world space position of a connector point Pi of a body j with               slider joints with additional constraints that define the goal posi-
position x j and orientation ϑ j is defined by                                    tions and orientations for the linked bodies (see Figure 23, left).

                    Pi (x j , ϑ j ) = x j + R(ϑ j )ri ,                (38)          Finally, after computing position and orientation changes of the
                                                                                  rigid bodies we have to update the velocities and angular velocities
where ri denotes the position of the connector in the local coordi-               (cf. Algorithm 1, line 12). The velocity update is done as follows:
nate system of the body. The Jacobian of a constraint function C(P)
which depends on a set of connector points P is determined by                                                   1  n+1        
                                                                                                       vn+1 =       x     − xn
                                                                                                                ∆t
                         ∂C(P)  ∂P ∂P T                                                                       2              
                    J=           · ∂x ∂ϑ ,                                                             ω n+1
                                                                                                             = = qn+1 · q̄n .
                         | ∂P
                           {z } |      {z     }                                                                 ∆t
                         constraint        connector
                        specific part     specific part
                                                                                  5.10. Fluids
where the first term is constraint specific and can be computed with-
out knowledge of the body while the second term only depends on                   It is also possible to simulate fluids in the PBD framework even
the connector type.                                                               though it has been used almost exclusively for the simulation of
                                                                                  deformable objects. We mention fluids simply as an item in the list
   For our ball joint example the constraint specific part of the Ja-
                                                                                  of possible constraints because all that is needed to simulate liquids
cobian is determined by ∂C(P)/∂P1 = −∂C(P)/∂P2 = I, where I
                                                                                  and gases is a specialized constraint.
is the identity matrix. The connector specific part for a point con-
nector is obtained by deriving Equation (38) with respect to x and                  A straightforward approach would be to model the fluid as a sys-
ϑ. The first term is determined by ∂P/∂x = I while the second term                tem of particles constrained to maintain a minimum distance from
∂P/∂ϑ requires the computation of ∂R(ϑ)/∂ϑ which is explained                     each other, however this leads to granular-like behavior and will
in detail by Grassia [Gra98].                                                     typically fail to reach hydrostatic equilibrium when coming to rest.

                                                                                                                                                  ©
                                                                                                                                                     2017 The Author(s)
                                                                                                           Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 23: Left: Millipede with walking over several obstacles. The simulation model consists of 261 rigid bodies, 340 constraints and 240
motors. Right: 2000 rigid bodies collide with each other.



An alternative method is presented by Macklin and Müller [MM13]
where fluid incompressibility is enforced using density constraints.
Borrowing the concept of a density estimator from Smoothed Par-
ticle Hydrodynamics (SPH) [Mon94, Mon92], a density constraint
is constructed for each particle i in the system as follows
                                          ρ
                      Ci (x1 , ..., xn ) = i − 1,              (41)
                                          ρ0
where ρ0 is the fluid rest density and ρi is the density at a parti-
cle, defined as the sum of smooth kernels [MCG03] centered at the
particle’s neighbor positions
                             ρi = ∑ m jW (xi − x j , h).
                                     j

Note that here each particle’s mass is assumed to be one, and the
rest density adjusted accordingly. In order to solve these density
constraints using position-based dynamics, the derivative of the
constraint function (41) with respect to each particle’s position is
required. This can be calculated using the gradient of SPH kernels                      Figure 24: A wave pool scene consisting of 128k fluid particles
                                                                                        simulated in 10ms/frame on the GPU. Incompressibility is enforced
                        ∇xk W (xi − x j , h) if k = i
                       
                     1 ∑  j                                                             using density constraints solved using position-based dynamics.
           ∇xk Ci =
                    ρ0 
                         −∇xk W (xi − x j , h) if k = j.
Note that the kernel W and its gradient ∇xk W can be computed
very efficiently using lookup tables [BK16].                                            visually plausible elastic and plastic deformations (see Figure 25).
                                                                                        This approach is easy to implement, very efficient and uncondition-
   By taking advantage of symmetry in the SPH smoothing kernel                          ally stable.
W , the corrective change in position due to the particle’s own den-
sity constraint, and the density constraints of its neighbors is given                     Shape matching can be seen as a form of constraint projection
by                                                                                      which can directly be integrated in the position-based dynamics
                                                                                        algorithm. By performing shape matching in line (9) of Algorithm 1
                       1             
                                                                                        it can be easily combined with other position-based constraints.
               ∆xi =      ∑  λi + λ j ∇W (xi − x j , h),
                      ρ0 j
                                                                                           The basic idea of simulating elastic behavior with shape match-
where λ is the per-constraint scaling factor (see Equation (6)). Fig-                   ing is shown in Figure 26. For the simulation the initial configura-
ure 24 shows a real-time water simulation using this method.                            tion of the deformable object must be stored. Since no connectivity
                                                                                        information is needed, this configuration is defined by the initial
                                                                                        positions x̄i . In each time step the positions and velocities of the
5.11. Shape Matching
                                                                                        particles are updated without considering any internal constraints
The geometrically motivated concept of shape matching to simu-                          between the particles. Only external forces and collision response
late deformable objects was introduced by Müller et al. [MHTG05].                       are taken into account. Instead of using internal constraints, goal
Shape matching is a meshless approach which is able to simulate                         positions are determined by matching the initial shape with the de-

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                    J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 25: Robust and volume-conserving deformations using shape matching. Armadillos (32442 particles total), 20 ducks and 20 tori
(21280 particles total) and 20 balls (7640 particles total) were simulated in real-time on a GPU.



                                                   g0                             If we minimize the term ∑i (Ar̄i − ri )2 with ri = xi − c and r̄i =
x0                  x1                                                  x1    x̄i − c̄, we get the optimal linear transformation A of the initial and
                               R, c
                                              g2        x0             g1     the deformed shape. This transformation is determined by:
                                                             x3
x2                  x3                     x2                                                                !             !−1
                                                                  g3                      A=     ∑ mi ri r̄Ti       ∑ mi r̄i r̄Ti        = Ar As .             (43)
                                                                                                  i                  i

                                                                              In our case we are only interested in the rotational part of this trans-
Figure 26: The initial shape with the vertex positions x̄i is matched         formation. Since As is symmetric, it contains no rotation. There-
to the deformed configuration xi to obtain goal positions gi . The            fore, we only need to extract the rotational part of Ar to get the
deformed shape is pulled towards these goal positions to simulate             optimal rotation R for shape matching. This can be done by a polar
elastic behavior.                                                             decomposition Ar = RS of the transformation matrix where S is a
                                                                              symmetric matrix.
                                                                                Finally, the goal positions are determined by
formed configuration. Then, each particle is pulled towards its goal
                                                                                                                  
                                                                                                                  x̄
position.                                                                                                  gi = T i ,
                                                                                                                   1
   In the following we first describe how the goal positions are de-          where T = R (c − Rc̄) . These goal positions are used to com-
                                                                                                        
termined. Then we show how large deformations can be simulated                pute position corrections:
using region-based shape matching and introduce fast summation
techniques for this approach. In the end the concept of oriented par-                                 ∆xi = α (gi (t) − xi (t)) ,
ticles and different extensions of the shape matching method are              where α ∈ [0, 1] is a user-defined stiffness parameter which defines
presented.                                                                    how far the particles are pulled to their goal positions.

5.11.1. Goal Positions                                                        5.11.2. Region-Based Shape Matching

In order to obtain goal positions for the deformed shape the best             The shape matching algorithm described above allows only for
rigid transformation is determined which matches the set of initial           small deviations from the initial shape. For the simulation of large
positions x̄ and the set of deformed positions x. The corresponding           deformations the concept of region-based shape matching became
rotation matrix R and the translational vectors c and c̄ are deter-           popular, see e.g. [MHTG05, RJ07, DBB11]. The idea is to per-
mined by minimizing                                                           form shape matching on several overlapping regions of the origi-
                                                                              nal shape. In each region we can have a small deviation from the
                     ∑ wi (R (x̄i − c̄) + c − xi )2 ,                         corresponding part of the initial shape which results in a large de-
                      i
                                                                              formation over all regions.
where wi are the weights of the individual points. The optimal
                                                                                 Diziol et al. [DBB11] propose to define a region for each particle
translation vectors are given by the center of mass of the initial
                                                                              of the model where the i-th region contains all particles in the ω-
shape and the center of mass of the deformed shape:
                                                                              ring of the i-th particle in the original mesh of the model. Shape
                 1               1                                            matching is a meshless method but Diziol et al. require a mesh to
          c̄ =       mi x̄i , c = ∑ mi xi , M = ∑ mi .                 (42)
                 M∑i             M i            i                             define the shape matching regions. Rivers and James [RJ07] use a

                                                                                                                                               ©
                                                                                                                                                  2017 The Author(s)
                                                                                                        Eurographics Proceedings © 2017 The Eurographics Association.
                                              J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

                                                                                         putation of the optimal translation c and the transformation matrix
                                                                                         Ar becomes a bottleneck since large sums have to be computed
                                                                                         for each region. For a mesh with the dimension d and n regions,
                                                                                         O(ωd n) operations are required with the naive approach.

                                                                                         5.11.3.1. Regular Lattices Rivers and James demonstrated
                                                                                         in [RJ07] how the number of operations for computing the sums
                                                                                         can be reduced to O(n) for regular lattices (d = 3). Their op-
                                                                                         timization is closely related to the concept of summed-area ta-
                                                                                         bles [Cro84]. In their approach they compute the summation for
                                                                                         a set of particles just once and reuse it for all regions that contain
                                                                                         this set. This reduces redundant computations significantly for
Figure 27: The stiffness of the model depends on the region size.                        a system with large overlapping regions. The fast summation of
Smaller regions (top) allow larger deformations than larger regions                      Rivers and James is based on the usage of cubical regions. These
(bottom). The hexagons in the left images represent the overlapping                      cubical regions can be subdivided in two-dimensional plate regions
regions of the model. The right images show the goal positions after                     which can again be subdivided in one-dimensional bar regions. The
one particle is moved away.                                                              region summation is performed in three passes. In the first pass the
                                                                                         sum for each bar is determined. The results are used to compute the
                                                                                         sums for the plates which are again used to obtain the final region
regular lattice instead to define their regions. No matter which kind                    sum. Each pass requires O(ω) operations. However, the region sum
of regions are used, the stiffness of the model depends on the size                      can even be determined in constant time if we take into account
of the overlapping regions (see Figure 27). Enlarging the regions                        that the sum of two neighboring bars, plates or cubes only differs
results in a more global shape matching and therefore the stiffness                      by one element. Lattice shape matching can be performed in linear
of the simulated model is increased.                                                     time if the sums in Equations (44) and (45) are evaluated using the
                                                                                         fast summation technique described above.
   In region-based shape matching a particle is part of multiple re-
gions. In the following we denote the set of regions to which a                             The FastLSM method of Rivers and James has several limita-
particle i belongs by <i . Since particles can belong to more than                       tions. To handle regions where the lattice is not regular, e.g. on the
one region, Rivers and James [RJ07] proposed to use modified par-                        boundary, several sums are defined in a pre-processing step for the
ticle masses m̃i = mi /|<i | for shape matching. This ensures that a                     corresponding node. In the case of fracturing the definition of these
particle which is part of many regions has not more influence than                       sums must be performed at run-time which is expensive to com-
others. The optimal translation vectors for a region i are determined                    pute. Small features need a fine sampling to obtain realistic results.
by                                                                                       Since a regular lattice is used, a fine sampling yields an explosion
                                                                                         of the computational costs. FastLSM does not support a varying
                          1                              1
                 c̄i =        ∑ m̃ j x̄ j ,     ci =         ∑ m̃ j x j ,    (44)        region size to simulate inhomogeneous material.
                         M̃i j∈<i                       M̃i j∈<i

where M̃i = ∑ j∈<i m̃ j is the effective region mass which can be                        5.11.3.2. Adaptive Lattices Steinemann et al. [SOG08] intro-
precomputed. The optimal rotation matrix R is computed by ex-                            duce an adaptive shape matching method which is based on lattice
tracting the rotational part of the following matrix:                                    shape matching to overcome these limitations. A fast summation
                                                                                         is realized by an octree-based sampling and an interval-based def-
                         Ar,i = ∑ m̃ j x j x̄Tj − M̃i ci c̄Ti .              (45)        inition of the shape matching regions. The hierarchical simulation
                                   j∈<i
                                                                                         model is created by starting with a coarse cubic lattice and then
In this form the first term depends on the particles j of the region                     performing an octree subdivision. The subdivision process can be
while the second term depends on the region i. This isolation of                         controlled by a user-defined criterion. At the end of the process a
the dependencies is required for fast summation techniques (see                          simulation node is placed at the center of each leaf cell and a virtual
below).                                                                                  node at the center of each non-leaf cell. A virtual node stores the
   After performing shape matching for all regions, we get multiple                      sum of all its descendant simulation nodes.
goal positions for each particle. The final goal position for a particle                    The fast summation for the hierarchical model is performed by
is determined by blending the goal positions of the corresponding                        an interval-based method which requires O(1) operations per re-
regions:                                                                                 gion. For each simulation node ni a shape matching region is de-
                              1                                                          fined by a region width ωi . To perform a fast summation, all sum-
                                           
                                            x̄
                       gi =        ∑   Tj i .                                            mation nodes of the region i are determined in a pre-processing
                            |<i | j∈<        1
                                                 i
                                                                                         step. First, for each node n j of the octree the interval of minimum
                                                                                         and maximum distances of all descendant leaves of n j to ni are de-
5.11.3. Fast Summation Techniques
                                                                                         termined. Then, during a top-down traversal each node n j where
In the case of region-based shape matching the stiffness increases                       the maximum distance is smaller than the region width is added to
with growing region size ω. However, at the same time the com-                           region i. If the descendant leaf nodes are contained only partially

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                      J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

in region i, the current node must be refined. Only in this case the                P4
traversal continues.                                                                P3
   The top-down traversal assigns O(1) summation nodes to each                      P2
region. A fast summation can now be performed in two steps. In the                  P1
first step the sums of all nodes in the hierarchy are determined. This
                                                                                    P0
is done by first computing the sums for the simulation nodes which                                    x0      x1      x2      x3
are the leaf nodes of the hierarchy, and then updating the sums of                  Prefix sum P0 0    x0 x0 +x1 x0 +x1 +x2 x0 +x1 +x2 +x3
the virtual nodes in a bottom-up fashion. The second step sums up
the values of the summation nodes for each region. For a roughly
balanced octree the computation of the sums takes O(n) time where                          Path P0 sum        −                  −
                                                                                           in regions  x0 +x1 +x2            x1 +x2 +x3
n is the number of simulation nodes. Hence, the adaptive shape
matching method requires linear time when using the described fast
summation technique to evaluate Equations (44) and (45).
                                                                                Figure 28: Fast summation technique for arbitrary triangle
5.11.3.3. Triangle Meshes In contrast to Rivers and James,                      meshes [DBB11]. First the prefix sums for the disjoint paths are
Diziol et al. [DBB11] only use the surface mesh of a volumet-                   determined. Then the region sum is computed by adding the differ-
ric model to simulate its deformation. Therefore, no interior ele-              ence of the intersection interval for each path.
ments are required for the simulation which reduces the compu-
tational costs. Diziol et al. introduce a fast summation technique
for arbitrary triangle meshes (d = 2) to compute the large sums of
                                                                                becomes ill-conditioned and the polar decomposition needed to ob-
the region-based approach efficiently. This technique only requires
                                                                                tain the optimal rotation tends to be numerically unstable.
O(ωn) operations instead of O(ω2 n) and can be performed very
efficiently in parallel.                                                           To solve this problem, Müller et al. [MC11] proposed to use
                                                                                oriented particles. By adding orientation information to particles,
   The fast summation technique of Diziol et al. is based on a sub-
                                                                                the polar decomposition becomes stable even for single particles.
division of all particles of the mesh in disjoint paths. A path i is a
                                                                                The moment matrix of a single spherical particle with orientation
set of vertices xi1 , . . . , xin which are connected by edges. The paths
                                                                                R ∈ R3×3 and finite radius r at the origin is well defined and can
are determined in a precomputation step. The goal of the path con-
                                                                                be computed via an integral over its volume as
struction algorithm is that each region is intersected by a minimum
number of paths. To determine the optimal path layout is computa-
                                                                                                          Z                            Z
                                                                                             Asphere =         ρ(Rx)xT dV = ρR                xxT dV
tionally expensive. Therefore, a heuristic is used to find a good path                                    Vr                             Vr
layout. Starting with a single vertex, adjacent vertices are added to                                   4 5         4       m
                                                                                                      =   πr ρR = πr5 R
a path until the path length exceeds a maximum size or cannot be                                       15           15     Vr
extended any further. The heuristic tries to avoid gaps by choos-                                      1
ing vertices which have neighbors that are already part of a path.                                  = mr2 R,
                                                                                                       5
To obtain paths which are as parallel as possible we add the vertex
                                                                                where Vr is the volume of a sphere of radius r. Since R is an or-
which is closest to a plane passing through the starting vertex of the
                                                                                thonormal matrix, Ai always has full rank and an optimal condition
current path, e.g. the xy-plane.
                                                                                number of 1. For an ellipsoid with radii a, b and c we get
   The fast summation is split in two phases (see Figure 28). In                                               2
                                                                                                                        0     0
                                                                                                                                 
                                                                                                                 a
the first phase the prefix sum for each path i is computed with j ∈                                        1 
[1, ni ]:                                                                                     Aellipsoid = m      0 b2 0  R.
                                                                                                           5
                                                                                                                  0     0 c2
                        j                       j
                 p                      p
                ci j = ∑ m̃ik xik ,   Ai j = ∑ m̃ik xik x̄Tik .
                      k=1                     k=1
                                                                                   However, the moment matrices of the individual particles cannot
                                                                                simply be added because each one is computed relative to the ori-
Since the prefix sums for all paths are independent of each other,
                                                                                gin. We need the moment matrix of particle i relative to the position
they can be computed in parallel. The sums for a region r are com-
                                                                                xi − c.
puted by first setting cr := 0 and Ar := 0. Then for each path i
which intersects the region in the interval [ik , . . . , il ], the following      Fortunately, this problem can be fixed easily. As we saw above,
terms are added:                                                                the equation for computing the moment matrix
                        p     p                         p         p
          cr := cr + cil − cik−1 ,    Ar := Ar + Ail − Aik−1 .          (46)                           A = ∑ mi (xi − c)(x̄i − c̄)T                              (47)
                                                                                                               i
The final translational vector and the affine matrix are determined
by cr := (1/M̃r )cr and Ar := Ar − M̃r cr c̄Tr respectively.                    can be re-written as
                                                                                                        A = ∑ mi xi x̄Ti − Mcc̄T ,
5.11.4. Oriented Particles                                                                                         i

For a small number of particles or particles that are close to co-              where c̄ and c are the centers of mass of the initial and the deformed
linear or co-planar (as in Figure 29), the matrix Ar in Equation (43)           shape, respectively (see Equation (42)).

                                                                                                                                                 ©
                                                                                                                                                    2017 The Author(s)
                                                                                                          Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

   Therefore, shifting the evaluation from the origin to the position                      An additional advantage of having orientation information is that
xi − c yields                                                                           ellipsoids can be used as collision volumes for particles. This al-
                          global                                                        lows a more accurate approximation of the object geometry than
                        Ai         = Ai + mi xi x̄Ti − mi cc̄T .                        with the same number of spherical primitives (see Figure 30).
Equation (47) now generalizes to
                                   
               A = ∑ Ai + mi xi x̄Ti − Mcc̄T
                             i
                                                      
                        = ∑ Ai + mi (xi − c)(x̄i − c̄)T .
                             i

As you can see, the last form looks like Equation (47) but with all
the individual particle moment matrices added in the sum.
   In addition to position x and velocity v, oriented particles carry a
rotation which can be defined as an orthonormal matrix R as above
or a unit quaternion q. They also carry the angular velocity ω. In
the prediction step of position-based dynamics, these two quantities
have to be integrated as well:
                  x p ← x + v∆t
                                                       
                           ω       |ω|∆t         |ω|∆t
                  qp ←        sin(       ), cos(       ) q.
                          |ω|        2             2
For stability reasons, q p should directly be set to q if |ω| < ε.
   After the prediction step, the solver iterates multiple times
through all shape match constraints in a Gauss-Seidel type fash-
ion as before. To simulate objects represented by a mesh of linked
particles, Müller and Chentanez [MC11] define one shape match-
ing group per particle. A group contains the corresponding particle                     Figure 29: This underwater scene demonstrates the ability of the
and all the particles connected to it via a single edge. The positions                  oriented particle approach to handle sparse meshes such as the
of the particles in a group are updated as in regular shape matching                    one-dimensional branches of the plants or the fins of the lion fish.
by pulling them towards the goal positions while the orientation of
the center particle only is replaced by the optimal rotation of shape
matching.
  After the solver has modified the predicted state (x p , q p ), the
current state is updated using the integration scheme
                    v ← (x p − x)/∆t
                    x ← xp
                    ω ← axis(q p q−1 ) · angle(q p q−1 )/∆t                             Figure 30: The rotation information of oriented particles cannot
                    q ← qp,                                                             only be used to stabilize shape matching, it also allows the use of
                                                                                        ellipsoids as collision primitives. The figure shows how the same
where axis() returns the normalized direction of a quaternion and                       mesh is approximated much more accurately with ellipsoids (right)
angle() its angle. Again, for stability reasons, ω should be set                        than with the same number of spheres (left).
to zero directly if |angle(q p q−1 )| < ε. There are two rotations,
r = q p q−1 and −r transforming q into q p . It is important to al-
ways choose the shorter one, i.e. if rw < 0 use −r, where rw is                         5.11.5. Plastic Deformation
the real part of the quaternion. As in traditional PBD for transla-
                                                                                        Shape matching can be extended in order to simulate plastic defor-
tion, changing the rotational quantity q p in the solver also affects
                                                                                        mations [MHTG05]. If we perform a polar decomposition Ar = RS
its time derivate ω through the integration step creating the required
                                                                                        for the linear transformation matrix Ar (see Equation (43)), we
second order effect.
                                                                                        get a rotational part R and a symmetric part S = RT Ar . The ma-
   The orientation information of particles cannot only be used to                      trix S represents a deformation in the unrotated reference frame.
stabilize shape matching but also to move a visual mesh along with                      Hence, for each region we can store the plastic deformation state in
the physical mesh. With position and orientation, each particle de-                     a matrix S p which is initialized with the identity matrix I. As pro-
fines a full rigid transformation at every point in time. This allows                   posed by Goktekin et al. [GBO04], we use two parameters cyield
the use of traditional linear blend skinning with particles replacing                   and ccreep to control the plastic behavior of the material. If the con-
skeletal bones.                                                                         dition kS − Ik2 > cyield is fulfilled for the deformation matrix S of

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                    J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

the current time step, the plastic deformation state is updated as            al. uses regions with only three vertices, the stiffness of high res-
follows:                                                                      olution models is too low for realistic results. Therefore, they in-
                                                                              troduce so-called fiber clusters to increase the stretching stiffness.
                   S p ← [I + ∆tccreep (S − I)] S p .
                                                                              These one-dimensional regions are determined in a pre-processing
After this update, S p is divided by 3 det (S p ) in order to conserve        step by subdividing the mesh into multiple edge strips. During the
                                      p

the volume. The plastic state S p is integrated in the shape matching         simulation each strip is traversed in both directions to obtain ad-
process by deforming the reference shape in Equation (43). This is            ditional goal positions. The resulting displacements are translated
done by replacing the definition of r̄i (see Section 5.11.1) with             so that they sum up to 0 to preserve the momentum of the model.
                                                                              The final goal positions are blended with the goal positions of the
                          r̄i = S p (x̄i − c̄) .
                                                                              triangular regions.
Note that the plasticity can be bound by the condition kS p − Ik2 >
                                                                                 The usage of fiber clusters increases the stiffness of the cloth
cmax where cmax is the threshold for the maximum plastic defor-
                                                                              model. However, this effect is limited and for high-resolution mod-
mation. If this condition is fulfilled, we use S p ← I + cmax (S p −
                                                                              els the stiffness is still too low to achieve a realistic cloth behav-
I)/kS p − Ik2 .
                                                                              ior. Bender et al. [BWD13] solve this problem by the introduction
                                                                              of multi-resolution shape matching (see Figure 32) which is based
5.11.6. Large Elasto-Plastic Deformation
                                                                              on the idea of multi-grid solvers [Hac85]. A shape matching re-
The approach described in the previous section works well as long             gion is defined for each edge and each triangle in a cloth model.
as the plastic deformation remains relatively small. However, when            To increase the influence of these simple regions and therefore
large deformations or topological changes occur as in the dough               the stretching and shearing stiffness of the model, shape matching
example in Figure 31, the sampling of the volume by particles and             is performed on different resolution levels. Multi-resolution shape
their clustering has to be adapted during the simulation.                     matching enables the robust simulation of stiff cloth models in lin-
                                                                              ear time.
   Chentanez et al. [CMM16] proposed a shape matching method
that can handle large elasto-plastic deformations. For plasticity they          In the following we first describe 2D shape matching for trian-
use the model of [Cho14] which is slightly more sophisticated than            gular regions and then introduce multi-resolution shape matching.
the one described in the previous section. To define the region that
has to be sampled with particles, they move an explicit triangle                 For a cloth simulation with triangular regions, shape matching
mesh surface along with the particles using linear blend skinning.            is performed per triangle in the two-dimensional space of the tri-
Their particle re-sampling method then comprises five steps: re-              angle plane. First the optimal translation vectors of the regions are
moving invalid particles, seeding new particles in under-sampled              computed by evaluating Equation (44). Then, for each triangle with
regions, updating the current clusters, remove invalid clusters and           the vertices x1 , x2 and x3 and the normal n a projection matrix is
add new clusters.                                                             determined:
                                                                                                            T
                                                                                                             a
   More specifically, particles are removed if the distance to their                                   P = xT ∈ R2×3
closest neighbor falls below a threshold or if they leave the surface                                        ay
mesh. Particles are added using poisson disk sampling in clusters             with
for which the Frobenius norm of the plasticity matrix S exceeds a                                       x2 − x1           n × ax
threshold. Deleted particles are removed from all clusters that ref-                           ax =               , ay =           .
                                                                                                       kx2 − x1 k        kn × ax k
erence them and the new particles are added to close enough clus-
ters. Then, existing clusters are removed if their particle count falls       The matrix P is used to project the vectors r and r̄ in Equation (43)
below or rises above given thresholds, the Frobenius norm of the              to get a 2D version of the matrix Ar :
plasticity matrix gets too large or if all referenced particles belong                          r̄0i = P̄ (x̄i − c̄) , r0i = P (xi − c) ,
to more than a given number of other clusters. To add new clusters,
a list of particles that are not referenced by a minimum number               where r̄0i ∈ R2 can be precomputed. The optimal rotation for
of clusters is created. Then, a subset of particles is selected whose         shape matching is obtained by performing a 2D polar decompo-
mutual distances are above the cluster radius. For each particle in           sition [SD92] for the resulting matrix A0r ∈ R2×2 . This rotation
this subset, a new cluster is created. For more details and a descrip-        matrix is used to compute 2D goal positions g0i for the particles
tion of how the surface mesh is updated we refer the reader to the            and the corresponding 2D position changes ∆x0i :
original paper.                                                                                                               1
                                                                                               g0i = R0 r̄0i ,   ∆x0i = α         (g0 − x0i ).
                                                                                                                             |<i | i
5.11.7. Cloth Simulation
                                                                              Finally, the vectors ∆x0i are transformed to world space by ∆xi =
Stumpp et al. [SSBT08] present a region-based shape matching ap-
                                                                              PT ∆x0i and the particle positions are updated. This process is shown
proach for the simulation of cloth. In their work they define a region
                                                                              in Figure 33.
for each triangle in the model. But instead of using the triangles
directly as regions for shape matching, overlapping regions are de-              In a simulation with multi-resolution shape matching [BWD13]
fined. The region of a triangle is defined by the outer corners of            two intergrid transfer operators are required to couple the differ-
its adjacent triangles. These overlapping regions enable the bend-            ent meshes in the multi-resolution hierarchy. The restriction oper-
ing resistance of the cloth model. Since the model of Stumpp et               ator Ill+1 transfers values from level l + 1 to the next coarser level

                                                                                                                                                ©
                                                                                                                                                   2017 The Author(s)
                                                                                                         Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017




Figure 31: Simulation of a piece of dough undergoing large plastic deformations. In this case, shape matching groups and sampling have
to be dynamically adjusted.



                                                                                                Algorithm 2 Multi-resolution shape matching
                                                                                                 1: for l = lmax to 1 do
                                                                                                 2:     Store current positions: x̂l ← xl
                                                                                                 3:     Perform shape matching
                                                                                                 4:     xl−1 := xl−1 + Il−1l   (xl − x̂l )
                                                                                                 5: end for
                                                                                                 6: for l = 0 to lmax do
                                                                                                 7:     Store current positions: x̂l ← xl
                                                                                                 8:     Perform shape matching
                                                                                                 9:     if l 6= lmax then
                                                                                                10:           xl+1 := xl+1 + Ill+1 (xl − x̂l )
                                                                                                11:     end if
                                                                                                12: end for


Figure 32: A stiff cloth model with 32467 triangles is simulated
using multi-resolution shape matching with five hierarchy levels.
                                                                                                   In the restriction phase the hierarchy is traversed from the finest
                                                                                                to the coarsest mesh performing a shape matching step on each
                x̄3                                                        g3                 level and projecting the resulting position differences xl − x̂l to the
                                                                      x3                       next coarser level with the restriction operator. In the prolongation
                                                                                                phase the hierarchy is traversed in the opposite direction. On each
         āy                                                               ay                 level a shape matching step is performed and the position differ-
           0       āx                                 x1                 0 ax         x2   ences are interpolated and added to the next finer level. Since only
                                                                                    g2         position differences are propagated between the levels, fine details
x̄1                      x̄2                                  g1                             are conserved on finer levels. However, fine details could get lost
                                                                                                if the original shape matching method is used on the coarse levels
                                                                                                of the hierarchy. Wrinkles on a fine resolution cause a compres-
Figure 33: 2D shape matching. The initial configuration of a trian-                             sion of elements on a coarser level. Shape matching reduces this
gle in 2D (left) is matched to the deformed configuration (middle)                              compression and thus eliminates fine details. Therefore, Bender et
by projecting the deformed triangle into 2D and computing the op-                               al. [BWD13] propose a modified computation of the goal positions
timal translation and rotation to get goal positions (right).                                   on the coarse levels of the hierarchy so that shape matching only
                                                                                                prevents stretching on these levels but not a compression.


l and the prolongation operator Il+1
                                  l   transfers values in the oppo-
site direction. These operators can be defined by barycentric coor-                             6. Implementation
dinates [GW06]. In each simulation step first the positions of the                              6.1. Parallelization
finest mesh are updated by time integration. For non-nested mod-
els the positions of the coarser meshes are interpolated using the                              The parallelization of the position-based approach is an important
restriction operator. Then multi-resolution shape matching is per-                              topic since multi-core systems and massively parallel GPUs are
formed in a V-cycle as described by Algorithm 2.                                                ubiquitous today.

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                      J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

6.1.1. Graph-Coloring Methods                                                   This form of local relaxation is not guaranteed to conserve mo-
                                                                                mentum when neighboring particles have differing number of con-
In a single CPU implementation, the solver processes the con-
                                                                                straints, however, visual errors are typically not noticeable. Averag-
straints one by one in a Gauss-Seidel-type fashion. Thereby, after
                                                                                ing constraint forces as described above ensures convergence, but
each constraint projection, the positions of affected particles are im-
                                                                                in some cases this averaging is too aggressive and the number of
mediately updated. In a parallel implementation, the constraints are
                                                                                iterations required to reach a solution increases. To address this a
processed in parallel by multiple threads. If two constraints affect-
                                                                                global user-parameter ω can be introduced to control the rate of
ing the same particle are handled by two different threads simulta-
                                                                                successive over-relaxation (SOR),
neously, they are not allowed to immediately update the particle’s
position because writing to the same position simultaneously leads                                            ∆x̃i =
                                                                                                                       ω
                                                                                                                          ∆xi .                                 (49)
to race conditions making the process unpredictable. A solution to                                                     ni
circumvent this problem is to use atomic operations. Such opera-
                                                                                We recommend using 1 ≤ ω ≤ 2, although higher values may be
tions are guaranteed not to be interrupted. However, atomics can
                                                                                used depending on the scene being simulated. Additional under-
slow down parallel execution significantly.
                                                                                relaxation (ω < 1) is not typically required as the constraint aver-
   To avoid these issues, a parallel implementation of PBD needs                aging is sufficient to avoid divergence.
to split the constraints into groups or phases. In each phase, none
of the constraints are allowed to share a common particle. With
this restriction, the constraints in the first phase can be processed           6.1.3. Hybrid Methods
in parallel without conflicts. Then, after a global synchronization,            To take advantage of both Gauss-Seidel and Jacobi solvers, Fratar-
the next phase can be processed. This cycle is repeated until all               cangeli et al. [FP15] proposed a hybrid approach. They use graph
constraints are processed.                                                      coloring and modify the graph such that it produces a desired num-
   As an example, if N particles are connected in a serial chain, the           ber of k colors by splitting high valence particles, i.e. solving them
constraints 1 − 2, 3 − 4, 5 − 6, 7 − 8, .. can be processed in phase 1          Jacobi style. An even simpler hybrid approach is to solve the first
and the constraints 2 − 3, 4 − 5, 6 − 7, .. in phase 2. This specific ex-       k − 1 colors using k − 1 Gauss-Seidel passes and then solve the
ample corresponds to the Red-Black Gauss Seidel scheme, where                   remaining constraints with one Jacobi pass.
there are two sets (colors) of constraints. For more general types
of constraints such as the stretch, shear and bending constraints
                                                                                6.1.4. Shape Matching
of cloth, more phases are needed. In this general case, splitting
constraints into phases corresponds to the graph coloring problem,              In Section 5.11.3 we presented different fast summation techniques
where each constraint corresponds to a node of the graph and two                for shape matching. The one of Diziol et al. [DBB11] is best suited
constraints are connected by an edge if they affect one or more                 for a parallel implementation on the GPU. In the following the GPU
common particles. The minimum number of colors determines how                   implementation of this technique with CUDA is described in detail.
many phases are needed in the parallel execution of PBD. Keeping                For such an implementation memory access and memory layouts
the number of phases small is not the only optimization criterion.              play an important role as well as the number of kernel calls.
The sets also need to have similar sizes for good load balancing.
                                                                                   Since each kernel call introduces a computational overhead, the
6.1.2. Jacobi Methods                                                           particles of all objects in a simulation are packed into one single ar-
                                                                                ray. This array is ordered according to the path layout which is used
For some models with high valence, graph-coloring methods may                   for the fast summation (see Section 5.11.3). Since the array con-
generate poor work load distributions, where initial sets of con-               tains the paths one after another, a segmented prefix sum [SHZO07]
straints may be large, but tailing sets are very small. This imbal-             can be used to determine the prefix sums of all paths at once. To
ance leads to resource under-utilization and potentially high syn-              avoid numerical problems due to the 32 bit floating-point arith-
chronization costs when many colors are required. An alternative                metics on the GPU, the path length is limited to 512. The resulting
method for parallelizing PBD is to use a Jacobi-style constraint                prefix sums are stored in texture memory to benefit from the tex-
solver. In a Jacobi solve, each constraint may be processed in par-             ture cache when the translational vectors and the affine matrices are
allel, and the position delta for each particle obtained by summing             determined (see Equation (46)).
the delta from each constraint at the end of an iteration.
                                                                                   The multi-resolution approach described in Section 5.11.7 can
   Jacobi methods often converge significantly slower than Gauss-               be implemented on the GPU as follows. Shape matching on each
Seidel iteration, and may not converge at all, for example if the sys-          level of the hierarchy is performed by computing the goal positions
tem matrix is not positive definite. To address this problem, under-            per element in parallel in a first step. The results are stored for each
relaxation based on the concept of constraint averaging [BFA02],                element. In a second step shape matching is completed by summing
or mass-splitting [TBV12] can be applied. At the end of the iter-               up the contributions of all elements containing a vertex to get a final
ation, once all constraints are processed, the particle’s total con-            goal position for the vertex. The restriction and the prolongation of
straint delta is divided by ni , the number of constraints affecting            the results can be performed efficiently using the sparse matrix data
the particle, to obtain the averaged position update ∆x̃:                       structure of Weber et al. [WBS∗ 13]. This implementation allows to
                                      1                                         simulate the deformation of a cloth model with more than 200k
                             ∆x̃i =      ∆xi .                       (48)       triangles on the finest level in 22 ms/step on a GeForce GTX 470.
                                      ni

                                                                                                                                                ©
                                                                                                                                                   2017 The Author(s)
                                                                                                         Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

                                                                                           A strain limiting method makes sure that the overall stretch of
                                                                                        the cloth stays below a certain threshold. In force based simula-
                                                                                        tions, strain limiting is a separate pass which is executed before
                                                                                        or after the regular cloth solver. In most cases, this pass moves
                                                                                        the positions of vertices directly, even in force based simulations.
                                                                                        Therefore, most strain limiting methods fall under the category of
                                                                                        position-based methods.
                                                                                           A straightforward way of limiting strain is to iterate through all
Figure 34: Rigid body bunnies, attached to cloth by deformable                          edges of a cloth mesh and project the adjacent particles of over-
ropes parachute to the ground. A drag model on the clothing parti-                      stretched edges as shown in Figure 3 so that the stretch of the edge
cles slows the descent of the bunnies.                                                  does not exceed the stretch limit. Provot [Pro95] was among the
                                                                                        first to use this method in the context of cloth simulation. He per-
                                                                                        forms a single iteration through all cloth edges after a force based
6.2. Unified Solver                                                                     solver. Desbrun et al. [DSB99] and Bridson et al. [BMF03] later
                                                                                        used the same post solver strain limiter but with multiple iterations
Macklin et al. [MMCK14] present a method that brings together
                                                                                        through all edges. Due to its simplicity, this method is still one of
many of the PBD applications in a unified framework. The core
                                                                                        the most popular strain limiting methods used in cloth simulations.
idea is to represent everything in the system by particles, and lever-
age fast GPU particle-particle collision techniques [Gre08] to gen-                        The method is very similar to position-based cloth simulation.
erate complex interactions efficiently.                                                 The main difference is that the strain limiting pass described above
   In this framework, rigid bodies are represented by voxelizing                        does not influence the velocities. These are updated by the force-
closed triangle meshes, and adding particles in interior cells. A                       based solver. In contrast, position-based cloth simulation derives
shape-matching constraint is then added to the system to enforce                        the new velocities from the projections, making an additional
the rigid particle configuration. Interaction between objects is ac-                    solver pass obsolete. Therefore, every position-based strain limit-
complished by simply connecting particles by constraints, e.g.:                         ing method used in force based simulations can directly be used in
tethering a rigid object to the corners of a piece of cloth generates                   a PBD solver.
a basic parachute (see Figure 34).                                                         The result of projecting along edges depends on the structure of
  Particles are extended with an integer phase attribute, which is                      the mesh. To reduce this artifact, Wang et al. [WOR10] propose to
used to control the generation of constraints. One possible inter-                      limit the principal strains of the 2D deformation field within each
pretation of the phase attribute is that particles of the same phase                    triangle. The 2D deformation field can be determined by consider-
do not generate collision constraints. For example, when model-                         ing the 2D coordinates of the vertices of a triangle within the planes
ing rigid bodies, particles belonging to the same body are given the                    of the rest and current triangle configurations. Wang et al. compute
same phase to avoid generating internal collisions.                                     the principal strains of the 2D deformation gradient, clamp them
                                                                                        and construct a new 2D transformation using the clamped strains.
   Fluids are modeled using the density constraint of Section 5.10,                     With this new transformation they correct the current positions of
because the fluid is also modeled by particles, full two-way cou-                       the triangle vertices. As before, to limit strain globally, they iterate
pling with clothing, rigid bodies, and granular materials is possi-                     through all triangles multiple times in a Gauss-Seidel fashion.
ble. Constraints may also be combined to achieve new effects, e.g.:
a rigid body constraint combined with the fluid density constraint                         Due to the relatively slow convergence rate of a Gauss-Seidel
can be animated to model phase changes such as melting.                                 solver, high iteration counts are necessary to limit the strain glob-
                                                                                        ally which slows down the simulation. The two main methods to
                                                                                        improve the convergence rate are the use of a global Newton-
7. Applications                                                                         Raphson solver as proposed by Goldenthal et al. [GHF∗ 07] or to
In this section we introduce different application areas of position-                   perform Gauss-Seidel iterations on a hierarchy of meshes as pro-
based methods. These methods are mainly used in interactive ap-                         posed in [Mül08], [WOR10] and [SKBK13]. However, these meth-
plications where performance, controllability and stability are more                    ods complicate the implementation and even though their conver-
important than accuracy, like e.g. in [SGdA∗ 10, DB13]. But there                       gence rate is higher, a single iteration can be significantly more
exist also other works which use a position-based approach for sta-                     expensive than a simple Gauss-Seidel iteration.
bilization.
                                                                                        7.2. Wrinkle Meshes
7.1. Strain Limiting
                                                                                        In cloth simulations, reducing the mesh resolution not only reduces
Strain limiting is an important topic in the field of cloth simulation.                 the cost of a single solver iteration but also the number of itera-
The reason is that the low solver iteration counts used in real-time                    tions required to get visually pleasing results. In [MC10] the au-
applications yield stretchy cloth. Since most cloth types are per-                      thors proposed a way to reduce the resolution of the dynamic mesh
ceived by the human eye as completely inextensible, it is important                     without losing too much visual detail. The most significant detail
to make simulated cloth inextensible in order to avoid disturbing                       in cloth simulations are small wrinkles. The method is based on the
visual artifacts [GHF∗ 07, BB08].                                                       observation that global dynamic behavior of the cloth and wrinkle

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                    J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

formation can be separated. Therefore, expensive dynamic simula-                                     p                             n
tion including collision handling is performed on a low-resolution
mesh. The wrinkle formation is handled on a high resolution mesh
that is attached to the dynamic mesh (see Figures 35 and 36). Since                         a                                               a
wrinkles do not oscillate, it is sufficient to use a static solver with a
                                                                                                                                       p
low iteration count on the high-resolution mesh.

                                                                                                l0            p2

                                                                                                                              p1            p4        p2
                                                                                    p1
                                                                                                                                       p3

                                                                              Figure 37: Static constraints on a wrinkle mesh: Attachment con-
                                                                              straint (top left), one sided attachment constraint (top right), stretch
Figure 35: Basic idea of wrinkle meshes. The high resolution wrin-
                                                                              constraint (bottom left) and bending constraint (bottom right).
kle mesh (white vertices) follows the low-resolution dynamic mesh
(black vertices) by restricting the white vertices to remain within a
certain distance (gray discs) to the dynamic mesh.
                                                                              Kubiak et al. [KPGF07] present a simulation method for surgical
                                                                              threads which is based on the position-based dynamics approach
                                                                              of Müller et al. [MHHR07]. Their method simulates the stiffness,
                                                                              bending and torsion of a thread and also provides feedback for a
                                                                              haptic device. For the simulation Kubiak et al. define distance con-
                                                                              straints for stiffness and bending, torsion constraints, contact con-
                                                                              straints and friction constraints. The presented method allows for
                                                                              an interactive and robust simulation of knots.
                                                                                 The simulation of complex hairstyles using a shape matching ap-
                                                                              proach is presented by Rungjiratananon et al. [RKN10]. Their ap-
                                                                              proach is based on Lattice Shape Matching which was originally in-
                                                                              troduced by Rivers and James [RJ07]. For the simulation each hair
                                                                              strand is represented by a chain of particles which is subdivided
                                                                              in overlapping chain regions. After shape matching an additional
                                                                              position-based strain limiting is applied to each strand which moves
                                                                              the particles in the direction of their root. Different hair styles are
Figure 36: Visualization of the wrinkle mesh (solid) and the under-           realized by using appropriate initial configurations and by modify-
lying dynamic mesh (wireframe).                                               ing the region sizes of a chain.
                                                                                 Umetani et al. [USS14] use a position-based rod model which
   Figure 37 shows the constraints defined on the high-resolution             is derived from the Cosserat theory in order to simulate complex
mesh to make it form wrinkles and follow the dynamic mesh. The                bending and twisting of elastic rods. The authors define material
attachment constraints makes sure that the vertices of the wrinkle            frames on the centerline of each edge to represent the orienta-
mesh stay close to their attachment points on the dynamic mesh.               tions along the rod. These material frames are represented by ghost
If the dynamic mesh has outside/inside information, a one-sided               points which are coupled with the edges by position-based con-
constraint can be used which makes sure that the wrinkle vertices             straints.
stay on the outside of the dynamic mesh, thus avoiding penetra-
                                                                                 O’Brien et al. [ODC11] use position-based dynamics for the
tions with other objects. The stretching and bending constraints are
                                                                              physically plausible adaptation of motion-captured animations. In
responsible for wrinkle formation.
                                                                              their work they use a vertex-based character skeleton and different
                                                                              constraints to preserve the skeleton structure, to define joint lim-
7.3. Further Applications                                                     its and to implement a center of mass control. In addition to the
                                                                              kinematic constraints, they define a couple of dynamics constraints
Another application area for position-based methods is interactive
                                                                              which consider vertices in multiple frames. Dynamics constraints
surgical simulation. In this area Wang et al. [WXX∗ 06] introduce a
                                                                              are used to enforce smooth acceleration and dynamical correctness.
mass-spring model based on a surface mesh to simulate deformable
bodies in real-time. Since such a model can neither preserve its vol-            Fierz et al. [FSAH12] introduce a position-based approach to sta-
ume nor resume its rest shape in the absence of external forces,              bilize a finite element simulation. When using an explicit time inte-
the authors propose to couple the surface model with a rigid core             gration for a finite element simulation, the time step size is typically
by using spring forces. This rigid core is simulated using shape              limited by the stiffness of the model and its spatial discretization. In
matching [MHTG05] which results in a fast and stable simulation.              each simulation step Fierz et al. use the Courant-Friedrichs-Lewy

                                                                                                                                                ©
                                                                                                                                                   2017 The Author(s)
                                                                                                         Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

(CFL) condition to determine the maximum allowed time step size                         [BK16] B ENDER J., KOSCHIER D.: Divergence-free sph for incompress-
for each tetrahedral element in their volumetric simulation model.                        ible and viscous fluids. IEEE Transactions on Visualization and Com-
However, instead of using the time step size given by the CFL con-                        puter Graphics (2016). 19
dition to perform a stable simulation step with an explicit integra-                    [BKCW14] B ENDER J., KOSCHIER D., C HARRIER P., W EBER D.:
tion scheme, they use a fixed size and mark all elements where the                        Position-based simulation of continuous materials. Computers & Graph-
                                                                                          ics 44, 0 (2014), 1 – 10. 9, 13, 15
condition is not met. The marked elements are then simulated us-
ing a shape matching approach while for all other elements a linear                     [BMF03] B RIDSON R., M ARINO S., F EDKIW R.: Simulation of clothing
                                                                                          with folds and wrinkles,. In Proc. ACM/Eurographics Symposium on
finite element method is used for the simulation.
                                                                                          Computer Animation (2003), pp. 28–36. 27
                                                                                        [BML∗ 14] B OUAZIZ S., M ARTIN S., L IU T., K AVAN L., PAULY M.:
8. Conclusion                                                                             Projective dynamics: Fusing constraint projections for fast simulation.
                                                                                          ACM Trans. Graph. 33, 4 (July 2014), 154:1–154:11. 8
In this tutorial, we focused on position-based approaches. Such ge-
                                                                                        [BMO∗ 14] B ENDER J., M ÜLLER M., OTADUY M. A., T ESCHNER M.,
ometrically motivated techniques are not force-driven and are par-                        M ACKLIN M.: A survey on position-based simulation methods in com-
ticularly appropriate in interactive applications due to their versa-                     puter graphics. Computer Graphics Forum 33, 6 (2014), 228–251. 4
tility, robustness, controllability and efficiency. We explained gen-                   [BW98] BARAFF D., W ITKIN A.: Large steps in cloth simulation. In
eral ideas of position-based methods and introduced several spe-                          Proceedings of Computer graphics and interactive techniques (1998),
cific constraints. Various aspects and efficient solution strategies                      SIGGRAPH ’98, ACM, pp. 43–54. 6
were discussed with a particular focus on the benefits of position-                     [BWD13] B ENDER J., W EBER D., D IZIOL R.: Fast and stable cloth sim-
based approaches compared to force-driven techniques.                                     ulation based on multi-resolution shape matching. Computers & Graph-
                                                                                          ics (2013). 24, 25
   Position-based dynamics is fast, easy to implement and control-
lable. Furthermore, it avoids the overshooting problems of force-                       [BWH∗ 06] B ERGOU M., WARDETZKY M., H ARMON D., Z ORIN D.,
                                                                                          G RINSPUN E.: A quadratic bending model for inextensible surfaces. In
based simulation models when using an explicit time integration                           Proc. Symposium on Geometry processing (2006), Eurographics Associ-
scheme. The method can handle arbitrary bilateral and unilateral                          ation, pp. 227 – 230. 9
constraints as long as the gradient of the constraint function can be                   [Cho14] C HOI M. G.: Real-time simulation of ductile fracture with ori-
determined. Therefore, this method is very flexible and has already                       ented particles. Computer Animation and Virtual Worlds 25, 3-4 (2014),
been used to simulate cloth, deformable solids and fluids.                                455–463. 24

   However, position-based dynamics also has some disadvantages.                        [CMM16] C HENTANEZ N., M ÜLLER M., M ACKLIN M.: Real-time sim-
                                                                                          ulation of large elasto-plastic deformation with shape matching. In Pro-
The stiffness of the model does not only depend on the user-defined                       ceedings of the ACM SIGGRAPH/Eurographics Symposium on Com-
stiffness parameter but also on the time step size and the number of                      puter Animation (Aire-la-Ville, Switzerland, Switzerland, 2016), SCA
solver iterations. Although the dependency can be reduced as de-                          ’16, Eurographics Association, pp. 159–167. 24
scribed in Section 4.2.2, it cannot be completely removed. There-                       [Cro84] C ROW F. C.: Summed-area tables for texture mapping. SIG-
fore, it is difficult to adjust parameters independently. Decoupling                      GRAPH Comput. Graph. 18, 3 (Jan. 1984), 207–212. 21
these parameters as well as adaptive time stepping are open prob-                       [DB13] D EUL C., B ENDER J.: Physically-Based Character Skinning. In
lems and important topics for future work. Another drawback is                            VRIPHYS 13: 10th Workshop on Virtual Reality Interactions and Physi-
that position-based dynamics is not convergent, i.e. the simula-                          cal Simulations (Lille, France, 2013), Eurographics Association, pp. 25–
tion does not converge to a certain solution with mesh refinement.                        34. 27
Hence, the usage of adaptive meshes is another open problem.                            [DBB09] D IZIOL R., B ENDER J., BAYER D.: Volume conserving simu-
                                                                                          lation of deformable bodies. In Short Paper Proceedings of Eurographics
Acknowledgments We wish to thank Tassilo Kugelstadt for help-                             (Mar. 2009). 11
ing us with the elastic rods part.                                                      [DBB11] D IZIOL R., B ENDER J., BAYER D.: Robust real-time deforma-
                                                                                          tion of incompressible surface meshes. In Proceedings of the 2011 ACM
                                                                                          SIGGRAPH/Eurographics Symposium on Computer Animation (2011),
References                                                                                SCA ’11, Eurographics Association. 11, 20, 22, 26

[BB08] B ENDER J., BAYER D.: Parallel simulation of inextensible cloth.                 [DCB14] D EUL C., C HARRIER P., B ENDER J.: Position-based rigid
  In VRIPHYS 08: Fifth Workshop in Virtual Reality Interactions and Phys-                 body dynamics. Computer Animation and Virtual Worlds (2014). 17,
  ical Simulations (2008), pp. 47–56. 27                                                  18
[Ben07] B ENDER J.: Impulsbasierte Dynamiksimulation von Mehrkör-                       [DSB99] D ESBRUN M., S CHRÖDER P., BARR A.: Interactive animation
  persystemen in der virtuellen Realität. PhD thesis, University of Karl-                 of structured deformable objects. In Proc. of SIGGRAPH 99 (1999),
  sruhe, Germany, 2007. 4                                                                 ACM, pp. 1–8. 4, 27
[BET14] B ENDER J., E RLEBEN K., T RINKLE J.: Interactive simulation                    [EB08] E NGLISH E., B RIDSON R.: Animating developable surfaces us-
  of rigid body dynamics in computer graphics. Computer Graphics Forum                    ing nonconforming elements. ACM Trans. Graph. 27, 3 (2008), 66. 8
  33, 1 (2014), 246–270. 4                                                              [FP15] F RATARCANGELI M., P ELLACINI F.: Scalable partitioning for
[BFA02] B RIDSON R., F EDKIW R., A NDERSON J.: Robust treatment of                        parallel position based dynamics. EUROGRAPHICS 2015 34, 2 (2015).
  collisions, contact and friction for cloth animation. ACM Trans. Graph.                 26
  21, 3 (July 2002), 594–603. 26
                                                                                        [FSAH12] F IERZ B., S PILLMANN J., AGUINAGA I., H ARDERS M.:
[BFS05] B ENDER J., F INKENZELLER D., S CHMITT A.: An impulse-                            Maintaining large time steps in explicit finite element simulations using
  based dynamic simulation system for VR applications. In Proceedings                     shape matching. Visualization and Computer Graphics, IEEE Transac-
  of Virtual Concept (2005), Springer. 4                                                  tions on 18, 5 (may 2012), 717 –728. 28

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
                                    J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

[GBO04] G OKTEKIN T. G., BARGTEIL A. W., O’B RIEN J. F.: A                    [MCKM14] M ÜLLER M., C HENTANEZ N., K IM T.-Y., M ACKLIN
  method for animating viscoelastic fluids. ACM Trans. Graph. 23, 3 (Aug.       M.: Strain based dynamics. In Proceedings of the 2014 ACM SIG-
  2004), 463–468. 23                                                            GRAPH/Eurographics Symposium on Computer Animation (2014), Eu-
                                                                                rographics Association. 13, 15
[GHF∗ 07] G OLDENTHAL R., H ARMON D., FATTAL R., B ERCOVIER
  M., G RINSPUN E.: Efficient simulation of inextensible cloth. ACM           [MCKM15] M ÜLLER M., C HENTANEZ N., K IM T.-Y., M ACKLIN M.:
  Trans. Graph. 26, 3 (2007), 49. 7, 8, 27                                      Air meshes for robust collision handling. to appear in ACM Trans.
                                                                                Graph. (2015). 12
[GM97] G IBSON S. F., M IRTICH B.: A survey of deformable modeling in
  computer graphics. Tech. Rep. TR-97-19, Mitsubishi Electric Research        [MHHR07] M ÜLLER M., H EIDELBERGER B., H ENNIX M., R ATCLIFF
  Lab., 1997. 4                                                                 J.: Position based dynamics. Journal of Visual Communication and
                                                                                Image Representation 18, 2 (2007), 109–118. 5, 11, 28
[Gra98] G RASSIA F. S.: Practical parameterization of rotations using the
  exponential map. Journal of Graphics Tools 3 (1998), 29–48. 18              [MHTG05] M ÜLLER M., H EIDELBERGER B., T ESCHNER M., G ROSS
                                                                                M.: Meshless deformations based on shape matching. ACM Trans.
[Gre08]   G REEN S.: Cuda particles. nVidia Whitepaper 2, 3.2 (2008), 1.        Graph. 24, 3 (2005), 471–478. 19, 20, 23, 28
  27
                                                                              [Mir96] M IRTICH B.: Fast and accurate computation of polyhedral mass
[GW06] G EORGII J., W ESTERMANN R.: A multigrid framework for                   properties. J. Graph. Tools 1, 2 (Feb. 1996), 31–50. 11
  real-time simulation of deformable bodies. Computer & Graphics 30           [MKC12] M ÜLLER M., K IM T.-Y., C HENTANEZ N.: Fast Simulation
  (2006), 408–415. 7, 25                                                        of Inextensible Hair and Fur. In VRIPHYS 12: 9th Workshop on Vir-
[Hac85] H ACKBUSCH W.: Multi-Grid methods and applications, vol. 4              tual Reality Interactions and Physical Simulations (2012), Eurographics
  of Springer Series in Computational Mathematics. Springer, 1985. 24           Association. 13
[HJCW06] H ONG M., J UNG S., C HOI M., W ELCH S.: Fast volume                 [MM13] M ACKLIN M., M ÜLLER M.: Position based fluids. ACM Trans.
  preservation for a mass-spring system. IEEE Comput. Graph. Appl. 26           Graph. 32, 4 (July 2013), 104:1–104:12. 19
  (2006), 83–91. 11                                                           [MMC16] M ACKLIN M., M ÜLLER M., C HENTANEZ N.:                 Xpbd:
                                                                                position-based simulation of compliant constrained dynamics. In Pro-
[ISF07] I RVING G., S CHROEDER C., F EDKIW R.: Volume conserving
                                                                                ceedings of the 9th International Conference on Motion in Games
   finite element simulations of deformable models. ACM Trans. on Graph-
                                                                                (2016), ACM, pp. 49–54. 9
   ics 26, 3 (July 2007), 13:1–13:6. 11
                                                                              [MMCK14] M ACKLIN M., M ÜLLER M., C HENTANEZ N., K IM T.-Y.:
[ITF04] I RVING G., T ERAN J., F EDKIW R.: Invertible finite elements           Unified particle physics for real-time applications. ACM Trans. Graph.
   for robust simulation of large deformation. In Proc. of the 2004 ACM         33, 4 (July 2014), 153:1–153:12. 11, 27
   SIGGRAPH/Eurographics Symp. on Comput. Anim. (2004), Eurograph-
   ics Association, pp. 131–140. 15                                           [Mon92] M ONAGHAN J. J.: Smoothed particle hydrodynamics. Annual
                                                                                Review of Astronomy and Astrophysics 30, 1 (1992), 543–574. 19
[Jak01] JAKOBSEN T.: Advanced character physics. In Proceedings,
   Game Developer’s Conference 2001 (2001). 9                                 [Mon94] M ONAGHAN J. J.: Simulating free surface flows with sph. J.
                                                                                Comput. Phys. 110, 2 (Feb. 1994), 399–406. 19
[JP99] JAMES D. L., PAI D. K.: Artdefo: accurate real time deformable
                                                                              [MSJT08] M ÜLLER M., S TAM J., JAMES D., T HÜREY N.: Real time
   objects. In Proc. of SIGGRAPH 99 (1999), ACM, pp. 65–72. 4
                                                                                physics: class notes. In ACM SIGGRAPH 2008 classes (2008), SIG-
[KCM12] K IM T.-Y., C HENTANEZ N., M ÜLLER M.: Long Range At-                   GRAPH ’08, ACM, pp. 88:1–88:90. 4
  tachments - A Method to Simulate Inextensible Clothing in Computer          [MTV05] M AGNENAT-T HALMANN N., VOLINO P.: From early draping
  Games. In Eurographics/ ACM SIGGRAPH Symposium on Computer                    to haute couture models: 20 years of research. The Visual Computer 21
  Animation (2012), Lee J., Kry P., (Eds.), Eurographics Association,           (2005), 506–519. 4
  pp. 305–310. 13
                                                                              [Mül08] M ÜLLER M.: Hierarchical Position Based Dynamics. In VRI-
[KPGF07] K UBIAK B., P IETRONI N., G ANOVELLI F., F RATARCAN -                  PHYS 08: Fifth Workshop in Virtual Reality Interactions and Physical
  GELI M.: A robust method for real-time thread simulation. In Pro-             Simulations (2008), Faure F., Teschner M., (Eds.), Eurographics Associ-
  ceedings of the 2007 ACM symposium on Virtual reality software and            ation, pp. 1–10. 8, 27
  technology (2007), VRST ’07, ACM, pp. 85–88. 28
                                                                              [NMK∗ 06] N EALEN A., M ÜLLER M., K EISER R., B OXERMAN E.,
[KS16] K UGELSTADT T., S CHOEMER E.: Position and orientation based             C ARLSON M.: Physically based deformable models in computer graph-
  cosserat rods. In Proceedings of the 2016 ACM SIGGRAPH/Eurograph-             ics. Computer Graphics Forum 25, 4 (December 2006), 809–836. 4,
  ics Symposium on Computer Animation (2016), Eurographics Associa-             6
  tion. 13                                                                    [ODC11] O’B RIEN C., D INGLIANA J., C OLLINS S.: Spacetime vertex
[LBOK13] L IU T., BARGTEIL A. W., O’B RIEN J. F., K AVAN L.: Fast               constraints for dynamically-based adaptation of motion-captured anima-
  simulation of mass-spring systems. ACM Transactions on Graphics 32,           tion. In Proceedings of the 2011 ACM SIGGRAPH/Eurographics Sym-
  6 (Nov. 2013), 209:1–7. Proceedings of ACM SIGGRAPH Asia 2013,                posium on Computer Animation (2011), SCA ’11, ACM, pp. 277–286.
  Hong Kong. 8                                                                  28
[LG98] L IN M. C., G OTTSCHALK S.: Collision detection between geo-           [OH99] O’B RIEN J. F., H ODGINS J. K.: Graphical modeling and anima-
  metric models: A survey. In In Proc. of IMA Conference on Mathematics         tion of brittle fracture. In SIGGRAPH ’99: Proceedings of the 26th an-
  of Surfaces (1998), pp. 37–56. 4                                              nual conference on Computer graphics and interactive techniques (New
                                                                                York, NY, USA, 1999), ACM Press/Addison-Wesley Publishing Co.,
[MC10] M ÜLLER M., C HENTANEZ N.: Wrinkle meshes. In Proceedings                pp. 137–146. 4
  of the 2010 ACM SIGGRAPH/Eurographics Symposium on Computer
  Animation (2010), SCA ’10, Eurographics Association, pp. 85–92. 27          [PB88] P LATT J. C., BARR A. H.: Constraints methods for flexible ob-
                                                                                jects. In Proceedings of the 15th annual conference on Computer graph-
[MC11] M ÜLLER M., C HENTANEZ N.: Solid simulation with oriented                ics and interactive techniques (1988), SIGGRAPH ’88, ACM, pp. 279–
  particles. ACM Trans. Graph. 30, 4 (July 2011), 92:1–92:10. 22, 23            288. 6
[MCG03] M ÜLLER M., C HARYPAR D., G ROSS M.: Particle-based fluid             [Pro95] P ROVOT X.: Deformation constraints in a mass-spring model to
  simulation for interactive applications. In Proceedings of the 2003 ACM        describe rigid cloth behavior. In In Graphics Interface (1995), Davis
  SIGGRAPH/Eurographics symposium on Computer animation (2003),                  W. A., Prusinkiewicz P., (Eds.), Canadian Human-Computer Communi-
  SCA ’03, Eurographics Association, pp. 154–159. 19                             cations Society, pp. 147–154. 27


                                                                                                                                              ©
                                                                                                                                                 2017 The Author(s)
                                                                                                       Eurographics Proceedings © 2017 The Eurographics Association.
                                             J. Bender, M. Müller and M. Macklin / A Survey on Position Based Dynamics, 2017

[RJ07] R IVERS A. R., JAMES D. L.: FastLSM: fast lattice shape match-                   [TPBF87b] T ERZOPOULOS D., P LATT J., BARR A., F LEISCHER K.:
  ing for robust real-time deformation. In SIGGRAPH ’07: ACM SIG-                         Elastically deformable models. In Computer Graphics (Proceedings of
  GRAPH 2007 papers (2007), ACM, p. 82. 20, 21, 28                                        SIGGRAPH 87) (1987), vol. 21, ACM, pp. 205–214. 4
[RKN10] RUNGJIRATANANON W., K ANAMORI Y., N ISHITA T.: Chain                            [USS14] U METANI N., S CHMIDT R., S TAM J.: Position-based Elastic
  shape matching for simulating complex hairstyles. Computer Graphics                     Rods. In Eurographics/ ACM SIGGRAPH Symposium on Computer An-
  Forum 29, 8 (2010), 2438–2446. 28                                                       imation (2014), The Eurographics Association. 28
[SD92] S HOEMAKE K., D UFF T.: Matrix animation and polar decom-                        [vFTS06] VON F UNCK W., T HEISEL H., S EIDEL H.-P.: Vector field
  position. In Proceedings of the conference on Graphics interface ’92                     based shape deformations. ACM Trans. on Graphics 25, 3 (July 2006),
  (1992), Morgan Kaufmann Publishers Inc., pp. 258–264. 24                                 1118–1125. 11
[SGdA∗ 10] S TOLL C., G ALL J., DE AGUIAR E., T HRUN S.,                                [WBS∗ 13] W EBER D., B ENDER J., S CHNOES M., S TORK A., F ELL -
  T HEOBALT C.: Video-based reconstruction of animatable human char-                      NER D.: Efficient GPU data structures and methods to solve sparse lin-
  acters. ACM Trans. Graph. 29, 6 (Dec. 2010), 139:1–139:10. 27                           ear systems in dynamics applications. Computer Graphics Forum 32, 1
                                                                                          (2013), 16–26. 26
[SGT09] S CHMEDDING R., G ISSLER M., T ESCHNER M.: Optimized
  damping for dynamic simulations. In Spring Conference on Computer                     [WGW90] W ITKIN A., G LEICHER M., W ELCH W.: Interactive dynam-
  Graphics (2009), pp. 205–212. 6                                                         ics. In SI3D ’90: Proceedings of the 1990 symposium on Interactive 3D
                                                                                          graphics (New York, NY, USA, 1990), ACM Press, pp. 11–21. 18
[SHZO07] S ENGUPTA S., H ARRIS M., Z HANG Y., OWENS J. D.:
                                                                                        [Wit97] W ITKIN A.: An introduction to physically based modeling: Con-
  Scan primitives for GPU computing. In Proc. of the 22nd ACM SIG-
                                                                                          strained dynamics, 1997. 5
  GRAPH/Eurographics Symp. on Grap. Hardware (2007), Eurographics
  Association, pp. 97–106. 26                                                           [WOR10] WANG H., O’B RIEN J., R AMAMOORTHI R.: Multi-resolution
                                                                                          isotropic strain limiting. ACM Trans. Graph. 29, 6 (Dec. 2010), 156:1–
[SKBK13] S CHMITT N., K NUTH M., B ENDER J., K UIJPER A.: Multi-                          156:10. 27
  level Cloth Simulation using GPU Surface Sampling. In VRIPHYS 13:
  10th Workshop on Virtual Reality Interactions and Physical Simulations                [WXX∗ 06] WANG Y., X IONG Y., X U K., TAN K., G UO G.: A mass-
  (Lille, France, 2013), Eurographics Association, pp. 1–10. 27                           spring model for surface mesh deformation based on shape matching.
                                                                                          In Proceedings of the 4th international conference on Computer graph-
[SLM06] S ERVIN M., L ACOURSIERE C., M ELIN N.: Interactive sim-                          ics and interactive techniques in Australasia and Southeast Asia (2006),
  ulation of elastic deformable materials. In SIGRAD 2006. The An-                        GRAPHITE ’06, ACM, pp. 375–380. 28
  nual SIGRAD Conference; Special Theme: Computer Games (2006),
  Linköping University Electronic Press. 9
[SOG08] S TEINEMANN D., OTADUY M. A., G ROSS M.: Fast adaptive
  shape matching deformations. In Proceedings of the 2008 ACM SIG-
  GRAPH/Eurographics Symposium on Computer Animation (2008), SCA
  ’08, Eurographics Association, pp. 87–94. 21
[SSBT08] S TUMPP T., S PILLMANN J., B ECKER M., T ESCHNER M.: A
  Geometric Deformation Model for Stable Cloth Simulation. In VRIPHYS
  08: Fifth Workshop in Virtual Reality Interactions and Physical Simula-
  tions (2008), Faure F., Teschner M., (Eds.), Eurographics Association,
  pp. 39–46. 24
[Sta09] S TAM J.: Nucleus: Towards a unified dynamics solver for com-
   puter graphics. IEEE International Conference on Computer-Aided De-
   sign and Computer Graphics (2009), 1–11. 6
[TBHF03] T ERAN J., B LEMKER S., H ING V. N. T., F EDKIW R.: Finite
  volume methods for the simulation of skeletal muscle. In Proc. of the
  2003 ACM SIGGRAPH/Eurographics Symp. on Comput. Anim. (2003),
  Eurographics Association, pp. 68–74. 4
[TBV12] T ONGE R., B ENEVOLENSKI F., VOROSHILOV A.: Mass split-
  ting for jitter-free parallel rigid body simulation. ACM Trans. Graph. 31,
  4 (July 2012), 105:1–105:8. 26
[TF88] T ERZOPOULOS D., F LEISCHER K.: Deformable models. The
  Visual Computer 4 (1988), 306–331. 6
[THMG04] T ESCHNER M., H EIDELBERGER B., M ULLER M., G ROSS
  M.: A versatile and robust model for geometrically complex deformable
  solids. In Proceedings of the Computer Graphics International (Wash-
  ington, DC, USA, 2004), CGI ’04, IEEE Computer Society, pp. 312–319.
  4
[TKH∗ 05] T ESCHNER M., K IMMERLE S., H EIDELBERGER B., Z ACH -
  MANN G., R AGHUPATHI L., F UHRMANN A., C ANI M.-P., FAURE F.,
  M AGNENAT-T HALMANN N., S TRASSER W., VOLINO P.: Collision de-
  tection for deformable objects. Computer Graphics Forum 24, 1 (Mar.
  2005), 61–81. 4
[TPBF87a] T ERZOPOULOS D., P LATT J., BARR A., F LEISCHER K.:
  Elastically deformable models. In Proceedings of the 14th annual con-
  ference on Computer graphics and interactive techniques (1987), SIG-
  GRAPH ’87, ACM, pp. 205–214. 4

©
  2017 The Author(s)
Eurographics Proceedings © 2017 The Eurographics Association.
