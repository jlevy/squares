                                                                                                                                                                                               1




                                         Dojo: A Differentiable Physics Engine for Robotics
                                                         Taylor A. Howell1∗ , Simon Le Cleac’h1∗ , Jan Brüdigam2 , Qianzhong Chen1 , Jiankai Sun1 ,
                                                                      J. Zico Kolter3 , Mac Schwager1 , and Zachary Manchester4



                                            Abstract—We present Dojo, a differentiable physics engine
                                         for robotics that prioritizes stable simulation, accurate contact
                                         physics, and differentiability with respect to states, actions, and
                                         system parameters. Dojo models hard contact and friction with
                                         a nonlinear complementarity problem with second-order cone
                                         constraints. We introduce a custom primal-dual interior-point
arXiv:2203.00806v5 [cs.RO] 26 Aug 2025




                                         method to solve the second order cone program for stable
                                         forward simulation over a broad range of sample rates. We
                                         obtain smooth gradient approximations with this solver through
                                         the implicit function theorem, giving gradients that are useful
                                         for downstream trajectory optimization, policy optimization,
                                         and system identification applications. Specifically, we propose
                                         to use the central path parameter threshold in the interior
                                         point solver as a user-tunable design parameter. A high value
                                         gives a smooth approximation to contact dynamics with smooth
                                         gradients for optimization and learning, while a low value gives                 Fig. 1: Atlas drop simulation. Dojo simulates this system with 403
                                         precise simulation rollouts with hard contact. We demonstrate                    maximal-coordinates states, 30 joint constraints, 36 inputs, and 8
                                         Dojo’s differentiability in trajectory optimization, policy learning,            contact points in real-time at 65 Hz. Dojo respects floor-feet pen-
                                         and system identification examples. We also benchmark Dojo                       etration constraints to machine precision. Other simulators struggle
                                         against MuJoCo, PyBullet, Drake, and Brax on a variety of                        to maintain the floor contact constraint, especially at low simulation
                                         robot models, and study the stability and simulation quality                     rates.
                                         over a range of sample frequencies and accuracy tolerances.
                                         Finally, we evaluate the sim-to-real gap in hardware experiments
                                         with a Ufactory xArm 6 robot. Dojo is an open source project
                                                                                                                          learning, system identification, and dataset generation for do-
                                         implemented in Julia with Python bindings, with code available
                                         at https://github.com/dojo-sim/Dojo.jl.                                          mains ranging from locomotion to manipulation. To overcome
                                                                                                                          the sim-to-real gap [6] and to be of practical value in real-
                                           Index Terms—Contact Dynamics, Differentiable Optimization,
                                         Simulation, Robotics
                                                                                                                          world applications, an engine should provide stable simula-
                                                                                                                          tion, accurately reproduce a robot’s dynamics, and ideally,
                                                                                                                          be differentiable to enable the use of efficient gradient-based
                                                                   I. I NTRODUCTION                                       optimization methods.
                                            The last decade has seen immense advances in learning-                           In recent years, a number of physics engines [7, 8, 9, 10,
                                         based methods for policy optimization and trajectory opti-                       11, 12, 13, 14] have been developed and utilized for robotics.
                                         mization in robotics, e.g., for dexterous manipulation [1, 2],                   These works have advanced the state of the art in robot simula-
                                         quadrupedal locomotion [3, 4], and pixels-to-torques control                     tion, particularly offering differentiability [8, 11, 9, 10], multi-
                                         [5]. These advances have largely hinged on innovations in                        physics simulation [13, 14, 11, 15], and the incorporation of
                                         learning architectures, large scale optimization algorithms, and                 learnable dynamics residuals [12]. Recent work is also moving
                                         large datasets. In contrast, there has been comparatively little                 towards a convergence of fully learning based world models
                                         work on the lowest level of the robotics reinforcement learning                  and traditional physics-based simulators [16, 17], representing
                                         stack: the physics engine. We argue that core improvements in                    an exciting new frontier in robot simulation.
                                         physics engines can enable future advancements in robotics,                         In this work, we propose to further advance the state of
                                         and we present Dojo as a physics engine that embodies several                    the art by focusing on the underlying numerics of the physics
                                         such advances.                                                                   engine, introducing features that can be adopted throughout
                                            Physics engines that simulate rigid-body dynamics with                        the existing simulation ecosystem to improve performance in
                                         contact are utilized for trajectory optimization, reinforcement                  a variety of ways. We package these numerical improvements
                                            1 Stanford University, Stanford, CA 94305, USA. {thowell,                     in a new simulation engine, Dojo, to highlight their favorable
                                         simonlc, qchen23, jksun, schwager}@stanford.edu                                  properties over exiting numerical techniques commonly used
                                            2 School of Computation, Information and Technology, Technical Univer-
                                                                                                                          in physics simulators.
                                         sity of Munich, Munich, 80333, Germany. jan.bruedigam@tum.de
                                            3 Department of Computer Science, Carnegie Mellon University, Pittsburgh,        Specifically, we introduce two new contributions specific
                                         PA 15213, USA. zkolter@cs.cmu.edu                                                to Dojo: (i) We propose a custom primal-dual interior point
                                            4 The Robotics Institute, Carnegie Mellon University, Pittsburgh, PA 15213,
                                                                                                                          solver for stably solving the complementary problem for
                                         USA. zacm@cmu.edu
                                            (Corresponding author: S. Le Cleac’h)                                         forward simulation. This solver allows for low sample rates
                                            ∗ These authors contributed equally to this work.                             while maintaining stable and accurate contact simulation,
                                                                                                                                   2



thereby alleviating the vanishing/exploding gradient problem             with a user-defined smoothness approximation set by the
that appears when differentiating through high sample rate               central path parameter,
rollouts common in other differentiable simulators. (ii) We        (iii) incorporation of variational integration and a nonlinear
obtain tunable gradient information through implicit differ-             complementarity problem (NCP) model for accurate con-
entiation of the interior point solver, obtaining user-defined           tact dynamics (previously introduced in literature, but not
smoothness of the gradients through contact events by tuning             yet integrated in a simulator).
the central path parameter. This gives informative gradients          In the remainder of this paper, we first provide an overview
through contact events for policy and trajectory optimization      of related state-of-the-art physics engines in Section II. We
(with a high central path parameter), while also enabling sharp,   then summarize important technical background in Section III.
physically accurate simulation rollouts (with a low central        Next, we present Dojo, and its key features in Section IV.
path parameter). This is in contrast to existing methods that      Simulation, planning, policy optimization, and system identi-
either deliver non-smooth gradients that are not informative       fication examples, and hardware sim-to-real gap evaluation are
for trajectory or policy optimization, or expensive sampling-      presented in Section V. Finally, we conclude with a discussion
based gradient approximations that require a large number of       of limitations and future work in Section VI.
calls to the engine, leading to slow computation.
   Additionally, we also incorporate the following features that                        II. R ELATED W ORK
have been presented in previous works, but are not typically         In this section, we provide an overview of several popular
implemented in existing physics engines: (a) We use a vari-        physics engines, focusing on their physical fidelity, underlying
ational integration scheme for strong energy and momentum          optimization algorithms, and capability to compute gradients.
conservation in non-contact regimes. (b) We use full nonlinear
complementarity constraints with nonlinear friction cones to
avoid numerical artifacts like interpenetration of rigid bodies    A. Mainstream Physics Engines
(e.g., a robot foot sinking through the floor) and creep (e.g.,       1) MuJoCo: In the learning community, MuJoCo [19] has
objects that should be at rest incorrectly sliding) commonly       become a standard for benchmarking reinforcement learn-
seen in robotics simulators [18]. (c) We use maximal coor-         ing algorithms using the OpenAI Gym environments [20].
dinates, explicitly representing the 6 degree of freedom pose      MuJoCo utilizes minimal-coordinates representations, and
of each rigid link, and the internal constraint forces that bind   employs both semi-implicit Euler and explicit fourth-order
them together.                                                     Runge-Kutta integrators to simulate multi-body systems.
   The Dojo physics engine is designed around these core           These integrators often require small time steps, particularly
numerical innovations with the goal of advancing robot simu-       for systems experiencing contact, and typically sample rates
lation for trajectory optimization and motion planning, control,   of hundreds to thousands of Hertz are required for stable
reinforcement learning, system identification, and for generat-    simulation, which a mature and efficient implementation is
ing high-quality datasets for learning and validation.             able to achieve at much faster than real-time rates. However,
   To demonstrate the advantages of this combination of nu-        these high rates can prove a challenge for control tasks, such as
merical features, we benchmark Dojo against MuJoCo [19],           reinforcement learning settings where vanishing or exploding
Drake [7], and Brax [8] for computational speed in simulations     gradients are exacerbated over long horizons with many time
with four different robot platforms, showing Dojo delivers a       steps [21, 22, 23].
comparable performance as other differentiable simulators. We         Impact and friction are modeled using a smooth, convex
demonstrate Dojo’s numerical stability and accuracy over sam-      contact model [24]. While this approach reliably computes
ple rates down to 20Hz, allowing for lower sample rates than       contact forces, it introduces unphysical artifacts, and contact
other simulators, leading to fewer rollout steps, and therefore    forces at a distance (i.e., while not in contact) [25], and the
less severe vanishing/exploding gradients. We also compare         default friction model introduces creep and velocity drift dur-
Dojo’s primal-dual solver versus a more common primal only         ing sliding. Additionally, achieving good simulation behavior
interior point solver, showing improved convergence speed and      often requires system-specific tuning of multiple solver param-
constraint satisfaction. We demonstrate Dojo’s differentiability   eters. Further, the “soft” contact model is computed using a
in trajectory optimization, policy optimization, and system        primal optimization method, meaning that as parameters are
identification examples in comparison with sampling-based          set to produce “hard” or more realistic contact, the underlying
gradient approximations. Finally, we show Dojo’s low sim-          optimization problem becomes increasingly ill-conditioned
to-real gap in hardware experiments with a UFactory xArm           and difficult to solve. For RL methods, where obtaining a large
6.                                                                 volume of rollouts quickly is more important than preserving
                                                                   physical fidelity of each rollout, these compromises have been
   In summary, the key contributions of this paper as integrated
                                                                   effective. However, for control and planning with real robot
into the Dojo simulator include:
                                                                   hardware they can be problematic. For example, it is often not
 (i) a custom primal-dual interior-point method for giving         possible to eliminate unphysical artifacts from the simulation
     stable, accurate simulation over sample rates as low as       to produce realistic results. The lack of smooth gradients is
     20Hz,                                                         also a major challenge in deep learning [18], where contact
(ii) analytic gradients through contact efficiently computed       dynamics must often be smoothened unrealistically in order to
     via implicit differentiation of the interior-point solver     make learning progress. Analytical gradients are not provided
                                                                                                                                         3



TABLE I: Comparison of physics engines used for robotics. Several simulators like MuJoCo and Drake have a selection of integrators that
users can choose. We demonstrate their default/most-widely-used integrators.

            Engine    Application    Integrator       State    Contact Softness    Contact Model/Solver        Gradients
           MuJoCo      robotics         RK4          minimal          soft               Newton              finite difference
            Drake      robotics     implicit Euler   minimal       soft/hard        penalty-based/SAP     randomized smoothing
            Bullet     graphics     implicit Euler   minimal       soft/hard             iterative           finite difference
           DART        robotics     implicit Euler   minimal         hard                  LCP                  subgradient
           PhysX       graphics        explicit      minimal          soft               iterative           finite difference
            Brax       graphics        explicit      maximal          soft               iterative               analytical
            Dojo       robotics      variational     maximal         hard                  NCP              implicit gradient



by the engine, and instead require finite-difference schemes           policies.
[26] that are computationally expensive. This approach re-
quires multiple calls to the engine, which can be expensive
if not performed in parallel.
   2) Drake: Drake [7], designed for robotics applications,            B. Differentiable Physics Engines
prioritizes physical accuracy and flexibility in simulation. Its          In contrast to traditional physics engines, differentiable
contact modeling primarily employs a penalty method, where             physics engines present promising opportunities for robotics
contact forces are approximated using stiff springs, based on          by incorporating physical models into auto-differentiation
the Hunt-Crossley model [27]. This approach provides a com-            frameworks [36]. Prior research has explored differentiation
pliant contact model but requires small time steps to ensure           across various domains, such as contact and friction mod-
stability, as the stiffness can lead to numerical challenges such      els [37, 38, 39, 40, 41, 42], latent state models [43, 44, 45, 46],
as instability and gradient explosion [21]. Recently, Drake has        volumetric soft bodies [47, 48, 11], and particle dynamics [44,
introduced the soft articulated-body dynamics with compliant           49]. Additionally, system identification using parameterized
contact (SAP) method [28], which formulates contact as a               physics models [50, 51, 52, 53, 54, 55, 56, 57, 58, 59] and
time-stepping optimization problem. SAP introduces compli-             inverse simulation techniques [60] have also been explored.
ance to relax the contact model, making it robust for simu-            Furthermore, there has been considerable research on smooth
lating articulated systems, similar in spirit to methods used          gradient computation [61], which aids in reducing noise in
in MuJoCo [19]. Drake offers flexibility in integrator choices,        gradient-based model explanations and ensures stable gradient
including advanced error-controlled methods, ensuring stable           calculations. Examples of such systems include Warp [62] and
and accurate simulation for various dynamics. Gradients in             Brax [8], both of which utilize the XPBD [63] model for
Drake are currently computed using Eigen’s autodiff frame-             contact simulation. The GradSim framework [64] combines a
work through the penalty method, but this approach is less             physics simulator with a differentiable rendering pipeline. Key
ideal for stiff systems. While SAP could theoretically utilize         components of these simulators include gradient calculation,
the implicit function theorem for gradient computation, this           dynamics models, contact models, and integrators. These sim-
feature has not been implemented yet. Additionally, methods            ulators are capable of leveraging gradient-based optimization
like randomized smoothing for returning gradients [29] pro-            techniques to enhance real-to-sim transfer capabilities.
vide alternative strategies for handling contact-rich dynamics            Gradients of rigid body dynamics can be useful in robotics
outside of Drake’s native capabilities.                                for various purposes. Applications include system identifica-
   3) Other Engines: The popular robotics simulator Gazebo             tion [65], controller design [66], controller tuning [67], trajec-
[30] can utilize several different physics engines to simulate         tory optimization [68], and policy optimization [69]. However,
multi-body contact dynamics, Bullet [31] and DART [32] are             gradients are typically computed through autodifferentiating
common choices. These engines model hard contact dynamics              through a simulation rollout by expressing the rollout as a
with an LCP formulation. Automatic differentiation tools have          computation graph, making use of mature auto-diff capa-
been utilized to compute gradients [12], [33], [34]. However,          bilities, e.g. in PyTorch. Unfortunately, this approach often
because of the discontinuous nature of contact dynamics, this          leads to numerical instability as a long chain of differentiation
approach will return discontinuous gradients at contact events,        tends toward infinity or zero as determined by the eigenvalues
which are less useful for gradient based trajectory or policy          of the Jacobians in the computation graph: the so called
optimization. Heuristics have been proposed to enumerate               vanishing/exploding gradients problem.
contact modes in order to select informative gradients [9].               Dojo uses an optimization solver to propagate a trajectory
However, this approach scales poorly with the number of                in time, making it impossible to apply back propagation to
contact mode switches.                                                 compute gradients. Instead, we use implicit differentiation,
   Engines designed for hardware accelerators (e.g., GPUs),            which has been explored recently to obtain gradients of the
including Brax [8] and PhysX [35], typically utilize simplified        solution to optimization problems with respect to problem
contact dynamics. Additionally, these engines usually require          parameters [38, 70]. Implicit gradients are computed using
system-specific tuning and their simulation results typically          the implicit function theorem, rather than directly auto-diffing
prioritize speed over physical fidelity, so a large number             through through a simulation rollout, in hopes of producing
of rollouts can be obtained quickly to train learning based            more stable gradient computations.
                                                                                                                                                    4



   The properties and characteristics of several of these exist-
ing engines are summarized in Table I. We find that none of the
existing engines prioritize two of the most important attributes
of robotics: physical accuracy and useful differentiability. This
motivates our development of Dojo as a physics engine for
robotics applications.
   Building on prior work [71], Dojo utilizes the                                   Fig. 2: Friction-cone comparison. Linearized double-parameterized
                                                                                    (left) and nonlinear second-order (right) cones.
open-source       maximal-coordinates       dynamics      library
ConstrainedDynamics.jl and efficient graph-based
linear-system solver GraphBasedSystems.jl. However,
unlike this previous work, Dojo has an improved contact                             where v ∈ R2 is the tangential velocity at the contact point,
model, specifically with regard to friction; and utilizes a more                    b ∈ R2 is the friction force, and cf ∈ R+ is the coefficient of
efficient, reliable, and versatile interior-point solver for the                    friction between the two objects [72].
NCP.                                                                                   This problem is naturally a convex second-order cone
                                                                                    program, and can be efficiently and reliably solved [73].
                           III. BACKGROUND                                          Classically, other works solve an approximate version of (4),
  Here we review existing methods of complementarity-based                                                               T
                                                                                                                              −v T β
                                                                                                                                  
contact models, implicit differentiation, maximal coordinates,                                        minimize           v
                                                                                                           β
and variational integrators that are used in Dojo.                                                    subject to β T 1 ≤ cf γ,                   (5)
                                                                                                                 β ≥ 0,
A. Complementarity-Based Contact Models
   Impacts and friction can be modeled through constraints on                       which satisfies the LCP formulation. Here, the friction cone
the system’s configuration and the applied contact impulses.                        is linearized (Fig. 2) and the friction vector, β ∈ R4 , is
   Impact: For a system with P contact points, we define                            correspondingly overparameterized and subject to additional
a signed-distance function, ϕ : Z → RP , subject to the                             positivity constraints [74].
following element-wise constraint                                                      The optimality conditions of (5) and constraints used in the
                                                                                    LCP are
                                   ϕ(z) ≥ 0.                                 (1)
                                                                                                      T           T
Where z represents the system configuration (i.e., the pose                                           v    −v T         + ψ1 − η = 0,            (6)
of robot and other objects in the simulation environment).                                                     T
                                                                                                    cf γ − β 1 ≥ 0,                              (7)
Impact forces with magnitude γ ∈ RP are applied to the                                                             T
bodies’ contact points in the direction of their surface normals                                    ψ · (cf γ − β 1) = 0,                        (8)
in order to enforce (1) and prevent interpenetration. Collision                                     β ◦ η = 0,                                   (9)
points1 are checked for constraint satisfaction at each iteration                                   β, ψ, η ≥ 0,                                (10)
of our primal-dual interior-point solver that will be introduced
in IV-B. A non-negative constraint                                                  where ψ ∈ R and η ∈ R4 are the dual variables associated
                                     γ ≥ 0,                                  (2)    with the friction cone and positivity constraints, respectively.
                                                                                    In practice, ψ acts as a flag to judge if the object has relative
enforces physical behavior that impulses are repulsive (e.g.,                       movement to the ground, while η is used to enforce the
the floor does not attract bodies), and the complementarity                         constraint that friction forces align with the vertices of the
condition                                                                           linearized friction cone approximation, and 1 is a vector of
                                  γ ◦ ϕ(z) = 0,                              (3)    ones.
                                                                                       The primary drawback of this formulation is that the opti-
where ◦ is an element-wise product operator, enforces zero
                                                                                    mized friction force will naturally align with the vertices of
force if the body is not in contact and allows non-zero force
                                                                                    the cone approximation, which may not align with the velocity
during contact.
                                                                                    vector of the contact point. Thus, the friction force does not
   Friction: Coulomb friction instantaneously maximizes the
                                                                                    perfectly oppose the movement of the system at the contact
dissipation of kinetic energy between two objects in contact.
                                                                                    point. Unless the pyramidal approximation is improved with
For a single contact point, this physical phenomenon can be
                                                                                    a finer discretization, incurring increased computational cost,
modeled by the following optimization problem:
                                                                                    unphysical velocity drift will occur. Additionally, the LCP
                        minimize        vT b                                        contact model requires a linearized form of the dynamics (12)
                              b                                              (4)    and a linear approximation of the signed-distance functions
                        subject to ∥b∥2 ≤ cf γ,
                                                                                    (1-3), both of which negatively impact physical accuracy. To
   1 Collision geometries are currently limited to simple shape primitives (e.g.,   avoid these problems, in Dojo we solve the full NCP with
four points on the foot of a humanoid instead of using a full mesh). While this     nonlinear friction cone, and develop a new primal-dual interior
is a limitation of the current implementation, it is common in other simulators
to manually edit contact geometries for critical parts of the robot, such as the    point method to reliably solve this more difficult optimization
feet of a humanoid or quadruped.                                                    problem.
                                                                                                                                                      5



B. Implicit Differentiation
                                                                        body                          body             joint   body         contact
   An implicit function, r : Rnw × Rnθ → Rnw , is defined as             a                             c                cd      d              3
r(w∗ ; θ) = 0 for solution w∗ ∈ Rnw and problem data θ ∈
Rnθ . At a solution point, the sensitivities of the solution with
                                                                               joint          joint          contact                  contact
respect to the problem data, i.e., ∂w∗ /∂θ, can be computed                     ab             bc               1                        2
using the implicit function theorem [75]
                    ∂w∗         ∂r −1 ∂r
                          =−                 .               (11)                      body
                     ∂θ         ∂w        ∂θ                                            b

Newton’s method is typically employed to find solutions
                                                                      Fig. 3: Graph structure for maximal-coordinates system with 4
w∗ . When the method succeeds, the sensitivity (11) can
                                                                      bodies, 3 joints, and 3 points of contact.
be computed and the factorization of ∂r/∂w used to find
the solution is reused to efficiently compute sensitivities at
very low computational cost, using only back-substitution.            where K : X × X → Rl×6 is a mapping from the joint to
Additionally, each element of the sensitivity can be computed         the maximal-coordinates space and is related to the Jacobian
in parallel. Dojo uses implicit method to obtain gradients for        of the joint constraint.
simulation rollouts with respect to control inputs, dynamics             We can generalize (14) to include additional bodies and
parameters, or initial conditions.                                    joints. For a multi-body system with N bodies and M
                                                                      joints we define a maximal-coordinates configuration z =
C. Maximal-Coordinates State Representation                           (x(1) , . . . , x(N ) ) ∈ Z and joint impulse j = (j (1) , . . . , j (M ) ) ∈
   Most multi-body physics engines utilize minimal- or joint-         J. We define the implicit discrete-time dynamics of the
coordinate representations for dynamics because of the small          maximal-coordinates system as
number of states and convenience of implementation. This                                         F (z− , z, z+ , j) = 0,                        (15)
results in small, but dense, systems of equations. In contrast,
maximal-coordinates explicitly represent the position, orien-         where F : Z × Z × Z × J → R6N . In order to simulate the
tation, and velocities of each body in a multi-body system.           system we find z+ and j that satisfy (15) for a provided z−
This produces large, sparse systems of equations that can             and z using Newton’s method.
be efficiently solved, including in the contact setting. We              By exploiting the mechanism’s structure, we can efficiently
provide an overview, largely based on prior work [76], of this        perform root finding on (15) (see [76] for additional details).
representation.                                                       This structure is manifested as a graph of the mechanism,
   A single rigid body is defined by its mass and inertia, and        where each body and joint is considered a node, and joints
has a configuration, x = (p, q) ∈ X = R3 × H, comprising a            have edges connecting bodies (Fig. 3). Because the mecha-
position p and unit quaternion q, where H is the space of four-       nism structure is known a priori, a permutation matrix can
dimensional unit quaternions. We define the implicit discrete-        be precomputed and used to perform efficient sparse linear
time dynamics F : X × X × X → R6 as                                   algebra during simulation. For instance, in the case where the
                                                                      joint constraints form a system without loops, the resulting
                       F (x− , x, x+ ) = 0,                   (12)    sparse system can be solved in linear time with respect to the
where we indicate the previous and next time steps with minus         number of links.
(−) and plus (+) subscripts, respectively, and the current time
step without decoration. We employ a variational integrator           D. Variational Integrator
that has desirable energy and momentum conservation proper-              We use a specialized implicit integrator that natively handles
ties [77]. Linear and angular velocities are handled implicitly       quaternions and alleviates spurious artifacts that commonly
via finite-difference approximations.                                 arise from contact interactions. The dynamics are derived by
   For a two-body system with bodies a and b connected                approximating Hamilton’s Principle of Least-Action using a
via a joint—common types include revolute, prismatic, and             simple midpoint scheme [77, 78]. This approach produces
spherical—we introduce a constraint, k : X × X → Rl , that            variational integrators.
couples the two bodies                                                   Each body has a linear
                       k ab (xa+ , xb+ ) = 0.                 (13)            p+ − 2p + p−
                                                                            m              − hmg − A(p)T j − hf = 0, (16)
                                                                                     h
An impulse, j ∈ Rl , where l is equal to the six degrees-of-
freedom of an unconstrained body minus the joint’s number                and rotational
of degrees-of-freedom, acts on both bodies to satisfy the                q
                                                                                 T ψ Jψ + ψ × Jψ
constraint. The implicit integrator for the two-body system                1 − ψ+    +  +   +     +

has the form
                                                                            p                                   τ
                                                                          − 1 − ψ T ψJψ + ψ × Jψ − B(q)T j − h2 = 0, (17)
          a a a a                                                                                              2
           F (x− , x , x+ ) + K a (xa , xb )T j ab
                                                        
          F b (xb− , xb , xb+ ) + K b (xa , xb )T j ab  = 0, (14)   dynamics specified by mass m ∈ R++ , inertia J ∈ S3++ ,
                          k ab (xa+ , xb+ )                           gravity g ∈ R3 , and time step h ∈ R++ . Equations (16, 17)
                                                                                                                                          6



Algorithm 1 Analytical Line Search For Cones                          relaxed optimality conditions for (19) in interior-point form
 1: procedure S EARCH (w, ∆, τ ort , τ soc )                          are
       αyort ← α(y (1) , τ ort ∆y )
                                 (1)
 2:                                                           ▷ 41                                        v − η(2:3) = 0,              (20)
       αzort ← α(z (1) , τ ort ∆z )
                                 (1)
 3:                                                           ▷ 41                                       ξ (1) − cf γ = 0,             (21)
       αsoc ← min α(y (i) , τ soc ∆y )
                                          (i)
 4:       y                                                   ▷ 46
                  i∈{2,...,n}                                                                                   ξ ◦ η = κe,            (22)
        αzsoc ←                 α(z (i) , τ soc ∆z )
                                                     (i)
 5:                  min                                      ▷ 46                   ∥ξ (2:3) ∥2 ≤ ξ (1) , ∥η(2:3) ∥2 ≤ η(1) ,         (23)
                  i∈{2,...,n}
 6:     Return min(αort , αort , αsoc , αsoc )
                          y       z      y       z                    with dual variable η ∈ R3 associated with the second-order-
                                                                      cone constraints, and central-path parameter, κ ∈ R+ . The
                                                                      second-order-cone product is
are essentially second-order centered-finite-difference approx-                     ξ ◦ η = (ξ T η, ξ (1) η(2:3) + η(1) ξ (2:3 ),      (24)
imations of Newton’s second law and Euler’s equation for the
rotational dynamics, respectively, where                              and
                            "q              #                                                  e = (1, 0, . . . , 0),                  (25)
                               1 − ψ+Tψ
                                         +
                   q+ = q ·                                (18)       is its corresponding identity element [80]. Friction is recovered
                                  ψ+
                                                                      from the solution: b = ξ ∗(2:3) . The benefits of this model are
is recovered from a three-parameter representation ψ ∈ R3             increased physical fidelity and fewer optimization variables,
[79]. We refer to Appendix A for quaternion conventions               without substantial increase in computational cost.
and algebra. Joint impulses j ∈ J have linear A : R3 →                   Nonlinear complementarity problem: Systems comprising
                                                                      N bodies and a single contact point are simulated using a
Rdim(J)×3 and rotational B : H → Rdim(J)×3 mappings into
                                                                      time-stepping scheme that solves the feasibility problem
the dynamics. The configuration of a body x(i) = (p(i) , q (i) ) ∈
R3 × H comprises a position and orientation represented as                           find z+ , j, γ, ξ, η                              (26)
a quaternion. Forces and torques f, τ ∈ R3 can be applied to
                                                                              subject to F (z− , z, z+ , j, γ, ξ, u) = 0,
the bodies.
                                                                                             γ ◦ ϕ(z+ ) = κ1,
                                                                                             ξ ◦ η = κe,
                              IV. M ETHOD
                                                                                             v(z, z+ ) − η(2:3) = 0,
  We now introduce Dojo’s contact model and custom primal-                                   ξ(1) − cf γ = 0,
dual interior-point solver, as well as the implicit differentiation
                                                                                             γ, ϕ(z+ ) ≥ 0,
method for obtaining gradients through the solver.
                                                                                             ∥ξ(2:3) ∥2 ≤ ξ(1) , ∥η(2:3) ∥2 ≤ η(1) .
                                                                      The system’s smooth dynamics F : Z × Z × Z × J ×
A. Contact Dynamics Model
                                                                      R+ × R2 × U → R6N comprise linear and rotational
   Impact and friction behaviors are modeled, along with              dynamics (16-17) for each body which are subject to inputs
the system’s dynamics, as an NCP. This model simulates                u = (f (1) , τ (1) , . . . , f (N ) , τ (N ) ) ∈ U. The contact-point
hard contact without requiring system-specific solver tuning.         tangential velocity v : Z×Z → R2 is a function of the current
Additionally, contacts between a system and the environment           and next configurations (i.e., a finite-difference velocity). The
are treated as a single graph node connected to a rigid body          central-path parameter κ ∈ R+ and target e [80] are utilized
(Fig 3). As a result, the engine retains efficient linear-time        by the interior-point solver in the following section. This
complexity for open-chain mechanical systems.                         formulation extends to multiple contacts.
   Dojo uses the rigid impact model (1-3) and in the following           Solving the NCP finds a maximal-coordinates state rep-
section we present its Coulomb friction model that utilizes an        resentation. In many applications it is desirable to utilize
exact nonlinear friction cone.                                        a minimial-coordinates representation (e.g., direct trajectory
   Nonlinear friction cone: In contrast to the LCP approach,          optimization where algorithm complexity scales with the state
we utilize the optimality conditions of (4) in a form amenable        dimension). Dojo includes functionality to analytically convert
to a primal-dual interior-point solver. The associated cone           between representations, as well as formulate and apply the
program is                                                            appropriate chain rule in order to differentiate through a
                                                                      representation transformation.
                  minimize         v T ξ (2:3)                           To simulate a system forward in time one step, given a
                      ξ
                  subject to ξ (1) = cf γ,                    (19)    control input and state comprising the previous and current
                             ∥ξ (2:3) ∥2 ≤ ξ (1) ,                    configurations, solutions to a sequence of barrier problems
                                                                      (26) are found with κ → 0. The central-path parameter has
where ξ is an auxiliary vector under the nonlinear friction           a physical interpretation as being the softness of the contact
cone model, with elements 2 and 3 representing the friction           model. A value κ = 0 corresponds to exact “hard” or inelastic
force components, and subscripts indicate vector indices. The         contact, whereas a relaxed value produces soft contact where
                                                                                                                                                7



Algorithm 2 Primal-Dual Interior-Point Solver                                              Dojo      randomized smoothing        dynamics
 1: procedure O PTIMIZE(a0 , b0 , c0 , θ, K)                                              κ                 Σ                     κ
                      soc = 0.99, τ
       Parameters: τmax
                                                                                              10−4               10−1                 10−4
 2:                                   min = 0.95                                              10−5               10−2                 10−5
 3:    rtol = 10 , κtol = 10−5 , β = 0.5
                  −5                                                                          10−6
                                                                                              10−7
                                                                                                                 10−3
                                                                                                                  0th
                                                                                                                                      10−6
                                                                                                                                      10−7
 4:    Initialize: a = a0 , b = b0 ∈ K, c = c0 ∈ K                                            10−8                1st                 10−8

 5:    rvio , κvio ← V IOLATION(w)                 ▷ (49, 50)
 6:     Until rvio < rtol and κvio < κtol do




                                                                                 ∂y/∂fy
          ∆aff ← −R̄−1 (w; θ)r(w; θ, 0)




                                                                                                                        ∆y
 7:
          αaff ← C ONE S EARCH(w, ∆aff , 1, 1)




                                                                       normal
 8:
 9:       µ, σ ← C ENTER(b, c, αaff , ∆aff )         ▷ (51-54)
10:       κ ← max(σµ, κtol /5)
11:       ∆ ← −R̄−1 (w; θ)r(w; θ, κ)                                                          fy                 fy                   fy
12:       τ ort ← max(τmin , 1 − max(rvio , κvio )2 )
13:       τ soc ← min(τmax soc , τ ort )




                                                                                 ∂x/∂fx
          α ← C ONE S EARCH(w, ∆, τ ort , τ soc )




                                                                      friction




                                                                                                                            ∆x
14:
15:       c∗vio , κ∗vio ← rvio , κvio
16:       ŵ ← U PDATE(w, ∆, α)                     ▷ (47, 48)
17:       rvio , κvio ← V IOLATION(ŵ)              ▷ (49, 50)
18:       Until rvio ≤ c∗vio or κvio ≤ κ∗vio do                                               fx                 fx                   fx
19:           α ← βα                                                Fig. 4: Gradient and dynamics comparison between point-wise gradi-
20:           ŵ ← U PDATE(w, ∆, α)                 ▷ (47, 48)      ents (black), randomized-smoothing gradients [29] (orange, blue) and
21:           rvio , κvio ← V IOLATION(ŵ)          ▷ (49, 50)      Dojo’s analytic gradients (magenta). The dynamics for a box in the
22:       end                                                       XY plane that is resting on a flat surface and displaced an amount
23:       w ← ŵ                                                    ∆ by a force f (top left). Randomized smoothing gradients (right
                                                                    column) are computed using 500 samples with varying covariances Σ.
24:     end                                                         Dojo’s gradients (middle column) are computed for different values
25:     ∂w∗ /∂θ ← −R̄−1 (w∗ ; θ)D̄(w∗ ; θ)              ▷ (11)      of central-path parameter κ. Compared to Dojo, the randomized
26:     Return w, ∂w∗ /∂θ                                           smoothing method produces noisy derivatives that are many times
                                                                    more expensive to compute. Simulated dynamics comparisons were
                                                                    conducted using Dojo’s results under varying values of the central-
                                                                    path parameter, κ. The dynamics involve a box of 1 kg mass resting
contact forces can occur at a distance. The primal-dual interior-   on a flat surface in the XY plane, displaced by a force ∆ (top
point solver described in the next section adaptively decreases     left). The applied force was gradually increased from 0 N to 20
this parameter in order to efficiently and reliably converge        N. Throughout the simulation process, considering two separate
to hard contact solutions. In practice, the engine is set to        cases—one involving impact and the other involving friction—the
converge to small values (i.e. κ → 0) for simulation in order to    maximum ∆x and ∆y differences between κ = 1 × 10−4 and
                                                                    κ = 1 × 10−8 were 1.52 × 10−3 m and 2.56 × 10−3 m, respectively.
simulate accurate physics. Intermediate solutions (i.e., κ > 0)
are cached and later utilized to compute smooth gradients in
order to provide useful information through contact events.
                                                                    between the affine (predictor) and corrector steps ensures
B. Primal-Dual Interior-Point Solver                                steady progress towards eliminating both constraint and com-
                                                                    plementarity violations. The analytical line search offers a
   To efficiently and reliably satisfy (26), we developed a         principled means of selecting step sizes that keep the iterates
custom primal-dual interior-point solver for NCPs with support      strictly within the cone, while the specialized handling of non-
for cone constraints and quaternions. The algorithm is largely      Euclidean variables ensures stable and accurate updates. By
based upon Mehrotra’s predictor-corrector algorithm [81, 82],       continuously monitoring violations and adjusting parameters
while implementing non-Euclidean optimization techniques to         accordingly, the approach reliably converges to a solution
handle quaternions [83] and borrowing features from CVX-            that meets predefined tolerances. As a result, this solver
OPT [80] to handle cones.                                           is capable of addressing a broad range of problems—from
   The primary advantages of this algorithm are the correc-         those with simple linear conditions to complex, nonlinear
tion to the classic Newton step, which can greatly reduce           scenarios—while providing accurate solutions and informative
the iterations required by the solver (often halving the total      gradients.
number of iterations), and feedback on the problem’s central-
path parameter that helps avoid premature ill-conditioning and         1) Problem formulation: The solver aims to satisfy instan-
adaptively drives the complementarity violation to zero in          tiations of the following problem
order to reliably simulate hard contact.
   The solver functions as a systematic procedure that itera-                             find         a, b, c
tively refines the solution while maintaining feasibility within                          subject to E(a, b, c; θ) = 0,                      (27)
the prescribed cone constraints. The primal-dual framework                                           b ◦ c = κe,
provides a structured pathway to the solution, and the interplay                                     b, c ∈ K,
                                                                                                                                                 8



TABLE II: Contact violation for Atlas drop (Fig. 1). Comparison
                                                                            Euclidean variables have corresponding identity blocks. This
between Dojo and MuJoCo for foot contact penetration (millimeters)
with the floor for different time steps (seconds). Dojo strictly enforces   modification accounts for the implicit unit-norm constraint
no penetration. When Atlas lands, its feet remains above the ground         on each quaternion variable and improves the convergence
by an infinitesimal amount. In contrast, MuJoCo exhibits significant        behaviour of the solver.
penetration through the floor (i.e., negative values).                         3) Cones: The generalized inequality, cone-product opera-
                Time Step       0.1      0.01    0.001
                                                                            tor, and target for the n-dimensional positive orthant are
                  MuJoCo      failure    −28      −46                                 Rn++ = {a ∈ Rn | a(i) > 0, i = 1, . . . , n},          (33)
                   Dojo       +1e-12    +1e-7    +8e-6
                                                                                       a ◦ b = (a(1) b(1) , . . . , a(n) b(n) ),             (34)
                                                                                           e = 1.                                            (35)
with decision variables a ∈ Rna and b, c ∈ RnK , equality-                  For the second-order cone they are
constraint set E : Rna × RnK × RnK × Rnθ → Rna +nK ,
problem data θ ∈ Rnθ ; and where K is the Cartesian product                     Qn = {(a(1) , a(2:n) ) ∈ R × Rn−1 | ∥a(2:n) ∥2 ≤ a(1) },
of positive-orthant and second-order cones [84].                                                                                       (36)
   Interior-point methods aim to satisfy a sequence of relaxed                 a ◦ b = (aT b, a(1) b(2:n) + a(1) b(2:n) ),                   (37)
problems with κ > 0 and κ → 0 in order to reliably converge
                                                                                   e = (1, 0, . . . , 0).                                    (38)
to a solution of the original problem (i.e., κ = 0). This con-
tinuation approach, though it makes our interior point solver               The solver utilizes the Cartesian product
hard to warm-start, helps avoid premature ill-conditioning and                                                                     l
is the basis for numerous convex and nonconvex interior-point                                  K = Rn+ × Ql11 × · · · × Qjj ,                (39)
solvers [82].                                                               of the n-dimensional positive orthant and j second-order
   The LCP formulation is a special-case instantiation of (27)              cones, each of dimension li .
where the constraint set is affine in the decision variables and              4) Analytical line search for cones: To ensure the cone
the cone is the positive orthant. Most general-purpose solvers              variables strictly satisfy their constraints, a cone line search is
for LCP problems rely on active-set methods that strictly                   performed for a candidate search direction. For the update
enforce κ = 0 at each iteration. Consequently, these solvers
generate non-informative gradient information (see Section                                                  y ← y + α∆,                      (40)
IV-C). In contrast our interior point solver can give informative           with step size α and search direction ∆, the solver finds the
gradients with a smoothing effect related to the size of κ.                 largest α ∈ [0, 1] such that y + α∆ ∈ K. The step-size is
   2) Residual and Jacobians: The interior-point solver aims                computed analytically for the positive orthant
to find a fixed point for the residual                                                                                    
                                                                                                               n    y(k) o
                            
                                    E(w; θ)
                                                                                        α = min 1, max          −           ,       (41)
                                                                                                      k|∆(k) <0    ∆(k)
                             b(1) ◦ c(1) − κ1 
              r(w; θ, κ) =                       ,         (28)           and second-order cone
                                                 
                                        ..
                                        .        
                                                                                        2      T
                              b(nK ) ◦ c(nK ) − κe                                 ν = y(1) − y(2:k) y(2:k) ,                                (42)
                                                                                                    T
while respecting the cone constraints. The Jacobian of this                        ζ = y(1) ∆(1) − y(2:k) ∆(2:k) ,                           (43)
residual with respect to the decision variables                                       ζ
                                                                                ρ(1) =  ,                                              (44)
                               ∂r(w; θ, ·)                                            ν
                      R(w; θ) =            ,              (29)                                   ζ
                                                                                                √ + ∆(1)
                                  ∂w                                                  ∆(2:k)      ν
                                                                              ρ(2:k) = √ −          √          y(2:k) ,                (45)
is used to compute a search direction. For convenience, we                                ν    y(1) ν + ν
denote w = (a, b, c). After a solution w∗ (θ, κ) is found, the
                                                                                      (                        
                                                                                        min 1, ∥ρ(2:k) ∥12 −ρ(1) , ∥ρ(2:k) ∥2 > ρ(1) ,
Jacobian of the residual with respect to the problem data                         α=
                                                                                        1, otherwise.
                               ∂r(w; θ, ·)                                                                                             (46)
                      D(w; θ) =            ,             (30)
                                  ∂θ
                                                                            The line search over all individual cones is summarized in
is used to compute the sensitivity of the solution. These
                                                                            Algorithm 1.
Jacobians are not explicitly dependent on the central-path
                                                                               5) Candidate update: The variables are partitioned: a =
parameter.
                                                                            (a(1) , . . . , a(p) ), where i = 1 are Euclidean variables and
   The non-Euclidean properties of quaternion variables are
                                                                            i = 2, . . . , p are each quaternion variables; and b =
handled with modifications to these Jacobians (29) and (30)
                                                                            (b(1) , . . . , b(n) ), c = (c(1) , . . . , c(n) ), where j = 1 is the
by right multiplying each with a matrix H containing attitude
                                                                            positive-orthant and the remaining j = 2, . . . , n are second-
Jacobians [83] corresponding to the quaternions in x and θ,
                                                                            order cones. For a given search direction, updates for Eu-
respectively
                                                                            clidean and quaternion variables are performed. The Euclidean
                    R̄(w; θ) = R(w; θ)HR (w),                       (31)    variables in a use a standard update
                    D̄(w; θ) = D(w; θ)HD (θ).                       (32)                            a(1) ← a(1) + α∆(1) .                    (47)
                                                                                                                                           9



                                                                           and affine complementarity violations,
                                                                                               nK
                                                                                          1
                                                                              µaff =
                                                                                              X              (i)            (i)

                               top view                                                           (b(i) + α∆b )T (c(i) + α∆c ),        (53)
                                                                                       deg(K) i=1

                                                                           as well as their ratio,
                                                                                                                      !!3
                                                                                                            µaff
                                                                                          σ = min 1, max 0,                 .          (54)
                                                                                                             µ

                                                                           As the algorithm makes progress, it aims to reduce these
                              side view                                    violations.
                                                                              8) Algorithm: The interior-point algorithm used to solve
                                                                           (27) is summarized in Algorithm 2. Additional tolerances τ ∈
                                                                           [0.9, 1] are used to improve numerical reliability of the solver.
                                                                           The algorithm parameters include τmaxsoc to prevent the iterates
Fig. 5: Velocity drift resulting from friction-cone approximation.         from reaching the boundaries of the cones too rapidly during
Comparison between a box sliding with approximate cones having             the solve, τmin to ensure we are aiming at sufficiently large
four vertices implemented in MuJoCo (magenta) and Dojo (orange)
versus MuJoCo’s (black) and Dojo’s (blue) and PyBullet’s (green)
                                                                           steps, and β is the decay rate of the step size α during the
nonlinear friction cones. Dojo’s nonlinear friction cone gives the         line search. In practice, rtol and κtol are the only parameters
physically correct straight line motion, while linear friction-cone        the user might want to tune.
approximations lead to lateral drift. MuJoCo’s nonlinear friction cone        Finally, the algorithm outputs a solution w∗ (θ, κ) that
exhibits a minor rotational drift. PyBullet’s nonlinear friction cone      satisfies the solver tolerance levels and, optionally, the im-
delivers correct straight line motion, but exerts greater friction force
on the box leading to a shorter trajectory than Dojo and MuJoCo.
                                                                           plicit gradients of the solution with respect to the problem
                                                                           parameters θ.
                                                                              For an instance of problem (27), the algorithm is provided
For each quaternion variable, the search direction exists in               problem data and an initial point, which is projected to
the space tangent to the unit-quaternion hypersphere and is                ensure that the cone variables are initially feasible with some
3-dimensional. The corresponding update for i = 2, . . . , p is            margin. Next, an affine search direction (i.e., predictor) is
                                                                           computed that aims for zero complementarity violation. Using
                       a(i) ← L(a(i) )φ(α∆(i) ),                   (48)    this direction, a cone line search is performed followed by
                                                                           a centering step that computes a target relaxation for the
where L : H → R4×4 is a matrix representing a left-
                                                                           computation of the corrector search direction. A second cone
quaternion matrix multiplication, and φ : R3 → H is a
                                                                           line search is then performed for this new search direction. A
mapping to a unit quaternion. The standard update (47) is
                                                                           subsequent line search is performed until either the constraint
used for the remaining decision variables b and c.
                                                                           or complementarity violation is reduced. The current point is
  6) Violation metrics: Two metrics are used to measure                    then updated, a new affine search direction is computed, and
progress: (i) the constraint violation                                     the procedure repeats until the violations satisfy the solver
                         rvio = ∥r(w; θ)∥∞ ,                       (49)    tolerances.

and (ii) complementarity violation
                                                                           C. Gradients
                                       (i)     (i)
                   κvio = max{∥b             ◦ c ∥∞ }.             (50)       Dojo simulates a user-tuneable smoothed approximation of
                           i
                                                                           hard contact dynamics. This approach allows us to compute
The problem (27) is considered solved when rvio < rtol and                 gradients that are more informative in the presence of contacts
κvio < κtol .                                                              by enabling a force-from-a-distance mechanism, as discussed
  7) Centering: The solver adaptively relaxes (27) by com-                 in references [85] and [29]. As previously discussed, interior-
puting the centering parameters µ and σ. These values provide              point methods optimize a sequence of smooth barrier sub-
an estimate of the cone-constraint violation and determine the             problems, where the degree of smoothing is parameterized by
value of the central-path parameter that a correction step will            the central-path parameter κ. Differentiating at a large value
aim to satisfy. These values rely on the degree of the cone                of κ gives more contact smoothing, with more informative
[80],                                                                      gradients but less accurate solutions, while differentiating at
                 nK
                 X                                                         small κ values gives less smoothing, less informative gradients,
    deg(K) =           deg(K(i) ) = dim(K(1) ) + nK − 1,           (51)    but better physical fidelity. The chosen intermediate solution,
                 i=1                                                       w∗ (θ, κ > 0), is differentiated using the implicit function the-
the complementarity violations,                                            orem (11) to compute smooth implicit gradients. In practice,
                                   n
                                                                           we find that these gradients greatly improve the performance
                                   K
                             1   X                                         of gradient-based optimization methods, consistent with the
                   µ=                (b(i) )T c(i) ,               (52)
                          deg(K) i=1                                       long history of interior-point methods. Dojo’s gradients are
                                                                                                                                       10



                                                                    TABLE III: Planning results. Comparison of final cost value, goal
                                                                    constraint violation, and total number of iterations for a collection
                                                                    of systems optimized with iterative LQR [86] using Dojo (D) with
                                                                    implicit gradients or MuJoCo (M) with finite-difference gradients.

                                                                                  System        Cost     Violation   Iterations
                                                                              box right (D)     14.5       3e-3         30
                                                                              box right (M)     13.5       3e-3         95
                                                                               box up (D)       14.5       3e-3         106
                                                                               box up (M)      failure      1.0          -
                                                                               hopper (D)        8.9       1e-3         96
                                                                               hopper (M)       26.7       2e-3         66
                                                                              quadruped (D)     2e-2       3e-4         20




                                                                       Impact constraints comparison: The Atlas humanoid is
                                                                    simulated dropping onto a flat surface (Fig. 1). The system
                                                                    comprises 31 bodies, resulting in 403 maximal-coordinates
                                                                    states, and has 36 actuated degrees-of-freedom. Each foot has
                                                                    four contact points. A comparison with MuJoCo is performed
                                                                    measuring penetration violations with the floor for different
                                                                    simulation rates (Table II). The current implementation of
                                                                    Dojo simulates this system in real time at 65 Hz.
                                                                       Friction-cone comparison: The effect of friction-cone ap-
Fig. 6: Locomotion plan for quadruped generated using trajectory    proximation is demonstrated by simulating a box that is initial-
optimization. Time progresses top to bottom.                        ized with lateral velocity before impacting and sliding along
                                                                    a flat surface. The complementarity problem with P contact
                                                                    points requires 2P (1+2d) decision variables for contact and a
compared with point-wise gradients and randomized smooth-
                                                                    corresponding number of constraints, where d is the degree of
ing in Fig. 4. Since κ represents a tradeoff between simulation
                                                                    parameterization (e.g., double parameterization: d = 2). For a
accuracy and gradient smoothness, we evaluate the effect of
                                                                    pyramidal approximation, in the probable scenario where its
κ on simulation accuracy. We compare the simulation results
                                                                    vertices are not aligned with the direction of motion, velocity
of different κ values in Fig. 4.
                                                                    drift occurs for a linearized cone implemented in Dojo and
   The problem data for each simulation step includes: the pre-
                                                                    MuJoCo. Meanwhile, though MuJoCo and PyBullet also can
vious and current configurations, control input, and additional
                                                                    use nonlinear friction cones, compared to Dojo, MuJoCo’s
terms like the time step, friction coefficients, and parameters
                                                                    nonlinear friction cone exhibits a minor rotational drift and
of each body.
                                                                    PyBullet’s nonlinear friction cone exerts greater friction force
                                                                    on box that leads to a shorter trajectory (Fig. 5). While it is
D. Implementation                                                   possible to reduce such artifacts by increasing the number of
   An open-source implementation, Dojo.jl, written in Ju-           vertices in the approximation of the second-order cone, this
lia, is available and a Python interface, dojopy, is also           increases the computational complexity. Such approximation
included. These tools, and the experiments, are available at,       is unnecessary in Dojo as we handle the exact nonlinear cone
                                                                    constraint efficiently and reliably with optimization tools from
          https://www.github.com/dojo-sim/Dojo.jl.
                                                                    cone programming; the result is accurate sliding.
                         V. R ESULTS                                   Simulation Stability at Low Frequencies To validate the
                                                                    stability of the primal-dual interior point solver under different
   Dojo’s capabilites are highlighted through a collection of ex-   simulation frequencies, we conduct Atlas drop (Fig. 1) and
amples, including: simulating physical phenomena, gradient-         similar quadrupedal drop experiments under different simu-
based planning with trajectory optimization, policy optimiza-       lation frequencies. During the simulations, we recorded the
tion, system identification, and sim-to-real gap evaluation with    robots’ torso heights over time. The simulation results can be
robot hardware. The current implementation supports point,          found in Fig. 7. Under a large span of simulation frequency
sphere, and capsule collisions with flat surfaces with a pre-       from 20-500 Hz, both Atlas drop and quadrupedal drop deliver
existing collision detection module (which is outside the scope     similar simulation results with small reasonable deviations.
of this work). All of the experiments were performed on a           The test results demonstrate that Dojo preserves simulation
computer with an Intel Core i9-10885H processor and 32GB            fidelity at low frequency, even through contact events.
of memory.
                                                                       Computation time: One of the primary challenges with
                                                                    differentiable simulators is their computation speed. Table
A. Simulation                                                       V presents a benchmark comparing the computation time
   The simulation accuracy of Dojo and MuJoCo is compared           for forward simulation and gradient calculation across four
in a number of illustrative scenarios.                              simulators on four different robot types. Each test involved
                                                                                                                                            11




                 1.4                         Sim. Freq.
                 1.2                              20 Hz
                 1.0                              50 Hz
      Height/m

                 0.8                              100 Hz
                 0.6                              200 Hz
                 0.4                              500 Hz
                 0.2
                 0.0
                   0.0   0.5   1.0     1.5 2.0   2.5       3.0
                                     Time/s
                                                                      Fig. 8: Simulation and real robot comparison under physical contacts
                 0.24                      Sim. Freq.                 and frictions. Robot arm pushing box experiment scenarios.
                 0.22                           20 Hz                 TABLE IV: Robot arm pushing box experiment results for Sim-to-
                 0.20                           50 Hz                 Real gap evaluation. Box was placed at different locations on the table
      Height/m




                 0.18                           100 Hz                with different initial x-direction distances to robot arm’s base. Both
                                                                      simulation and real robot are controlled by the same PD controller
                                                200 Hz
                 0.16                           500 Hz
                                                                      to track the same joint space at 100 Hz.
                 0.14                                                         Initial Distance (cm)        30     35     40      45    50
                 0.12                                                  Real
                                                                                         Box Flip         Yes    Yes    Yes     Yes    No
                                                                                   Final Distance (cm)    46.9   52.7   55.1    61.2   50
                 0.10
                    0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4                                      Box Flip         Yes    Yes    Yes     Yes    No
                                   Time/s                               Sim
                                                                                   Final Distance (cm)    45.7   52.3   55.2    62     50
                                                                       Sim-to-Real Distance Gap (cm)      1.2     0.4    0.1    0.8     0
Fig. 7: Torso height over time under different simulation frequency
for Atlas (top) drop and A1 (bottom) drop experiments.

                                                                      accuracy, we also examined the flipping behavior of the box,
                                                                      which is sensitive to the precise point of contact and influenced
simulating 1000 steps with a time step of 0.01s, using ran-           by complex frictional and contact forces. Dojo’s predictions
domly generated actions. MuJoCo’s gradients are calculated            of flipping outcomes closely matched those observed in the
with built-in finite differentiation function, Drake utilizes its     physical experiments, indicating that the simulator can capture
randomized smoothing gradients calculation function, while            the subtle and intricate dynamics involved in frictional contact
Brax calculates gradients through auto-differentiation.               scenarios. Taken together, these results give evidence of Dojo’s
   Among all four simulators, MuJoCo exhibited a clear advan-         ability to reproduce physical phenomena, thereby supporting
tage in computation speed. However, Dojo significantly out-           robust sim-to-real transfer in robotic manipulation tasks.
performs another differentiable simulator, Brax, and delivers a          Convergence study: Dojo’s solver reduces the constraint
comparable performance as Drake. This advantage stems from            violation rvio and complementarity violation κvio until both
(i) the maximal-coordinate dynamics model, which is highly            residual values are smaller than prescribed tolerances. As the
effective in handling complex systems with multiple links and         problem is nonconvex, it is important to analyze Dojo’s con-
joints, as discussed in Section III-C, and (ii) Dojo’s implicit       vergence performance across different robots under different
differentiation method, which avoids the O(n2 ) complexity            conditions. We simulate three robots in Dojo and record their
of finite difference techniques in the action and observation         κvio and rvio as well as the solver’s condition numbers over
spaces.                                                               iterations under different tolerance settings. Meanwhile, to
   Sim-to-Real gap evaluation: To assess the sim-to-real trans-       further substantiate Dojo’s ability to avoid ill-conditioning, we
fer capabilities and fidelity of Dojo, we conducted a series of       also compare Dojo with a primal-only interior point solver [28]
box pushing experiments using a 6-axis xArm manipulator and           on condition numbers over iterations under different tolerance
a 0.5 kg rectangular box (11 cm by 13 cm by 21 cm) positioned         settings. The convergence study results are shown in Fig. 9
at initial x-axis distances of 30, 35, 40, 45, and 50 cm from         and 10.
the manipulator’s base, the simulation and real experimental             When testing with different κtol , we fix rtol at 1 × 10−8 ,
scenario can be seen in Fig. 8. In both the simulated and             while as κvio is the main bottleneck of the solver, we relax
real-world trials, identical proportional-derivative (PD) gains       κtol to 0.1 when testing with different rtol . We do the same
and joint-space commands were applied. We record the box’s            for both residual values and condition number experiments.
final location and flipping status of each experiment (real           The experiment results demonstrate that Dojo’s primal-dual
world) or simulation (Dojo), the results can be found in              interior-point solver can converge within 15 iterations for
Table IV. After the pushing action, the positional discrepancy        all three robots. The residual decreases reliably for different
in the box’s final location between simulation and reality            tolerance settings, showing that Dojo’s solver has strong
averaged approximately 0.5 cm (1.25%). Apart from positional          numerical stability. For condition number experiments, the
                                                                                                                                                                                      12



 TABLE V: Computation time benchmark results. Comparison of computation time of forward simulation plus gradient calculation for
 different simulators on different types of robots. Simulation time step is 0.01 s, each test was simulated for 1000 steps, with randomly
 generated actions. MuJoCo’s gradients are calculated with built-in finite differentiation function, Drake utilizes its randomized smoothing
 gradients calculation function, while Brax calculates gradients through auto-differentiation.
                                                                          Simulation Time of Different Robots [s]
                                      Simulator
                                                            Humanoid           Unitree A1      Franka Panda       Skydio X2
                                          MuJoCo           1.512 ± 0.045         1.114 ± 0.007                     0.335 ± 0.001        0.047 ± 0.002
                                           Drake           5.463 ± 0.078         3.870 ± 0.024                     2.352 ± 0.055        0.571 ± 0.011
                                           Brax            6.975 ± 0.485        11.064 ± 0.521                     10.954 ± 0.395       7.953 ± 0.484
                                           Dojo            1.750 ± 0.135         5.235 ± 0.071                     1.159 ± 0.077        0.807 ± 0.003



                                           Tolerance                                                                             Primal-Dual Optimization Solver
                      tol = 1e-4              tol = 1e-6           tol = 1e-8                                              tol = 1e-4          tol = 1e-6          tol = 1e-8
       1e1      Push Box           1e2 Franka Panda             1e1      Unitree A1                                              Primal-Only Optimization Solver
                                                                                                                           tol = 1e-4          tol = 1e-6          tol = 1e-8
   5e-3                            2e-2                         5e-3                                                  Push Box
                                                                                                            1e10                        1e7 Franka Panda      1e13       Unitree A1
 vio




                                                                                          Cond. Num. Tol.
   2e-6                            5e-6                         2e-6
                                                                                                             1e7                        5e5                    2e9
   1e-9                            1e-9                         1e-9
             0 1 2 3 4 5 6 7              0 2 4 6 8 10 12              0123456789                            1e4                        2e4                    5e5
       1e1                         1e1                          1e2
                                                                                                             1e1 0 1 2 3 4 5 6 7 1e3 0 2 4 6 8 10 12 1e2 0 1 2 3 4 5 6 7 8 9
   5e-3                            2e-3                         2e-2
                                                                                                             1e4                 1e6                 1e9
rvio




                                                                                           Cond. Num. r Tol.
   2e-6                            5e-7                         5e-6                                         2e3                        1e5                    5e6
   1e-9 0 1 2 3 4 5 6 1e-10 0 1 2 3 4 5 6 1e-9 0 1 2 3 4 5 6 7                                               5e2
                                                                                                                                        1e4                    2e4
                                              Iterations
                                                                                                             1e2
 Fig. 9: Plots of residual values κvio and rvio versus iteration under                                             0 1 2 3 4 5 6 1e3 0 1 2 3 4 5 6 1e2 0 1 2 3 4 5 6 7
                                                                                                                                               Iterations
 different tolerance for three different robots.
                                                                                            Fig. 10: Plots of condition numbers versus iteration under different
                                                                                            κ and r tolerance for three different robots.
 general trend is that condition number increases with the
 iteration for both methods, as expected. Specifically, for Dojo,
 under relaxed κtol (0.1), the condition number stays low                                   Dojo uses a time step h = 0.1, whereas MuJoCo uses h =
 (smaller than 1 × 10−4 ) with iterations for all three robots.                             0.01 to prevent significant contact violations with the floor.
 Meanwhile, under rigorous κtol (1 × 10−8 ), the condition                                  MuJoCo fails in the scenario with the goal in the air, while
 number was higher than that under relaxed κtol , but still lies                            Dojo succeeds at both tasks.
 at a reasonable level for a nonconvex optimization problem                                    Hopper: The hopping robot [88] with m = 3 controls and
 (smaller than 1 × 109 ). Moreover, the primal-only solver’s                                n = 14 degrees-of-freedom is tasked with moving to a target
 condition number is much higher than the proposed method.                                  pose over 1 second. Similar, although not identical, models
 Under different tolerance settings, at the last iteration of each                          and costs are used. Dojo uses a time step h = 0.05 whereas
 experiment, the primal method’s condition number is 2 to                                   MuJoCo uses h = 0.01. The hopper is initialized with controls
 1×104 times of Dojo’s condition number, showing that Dojo’s                                that maintain its standing configuration. Quadratic costs are
 primal-dual interior-point solver has an advantage in avoiding                             used to penalize control effort and perform cost shaping on an
 numerical ill-conditioning.                                                                intermediate state in the air and the goal pose. The optimizer
                                                                                            typically finds a single-hop motion.
                                                                                               Quadruped: The Unitree A1 with m = 12 controls and
 B. Planning                                                                                n = 36 degrees-of-freedom is tasked with moving to a goal
    We utilize iterative LQR by providing implicit gradients                                location over a planning horizon T = 41 with time step h =
 from Dojo [87] to perform trajectory optimization on three                                 0.05. Controls are initialized to compensate for gravity and
 systems: planar box, hopper, and quadruped. A comparison                                   there are costs on tracking a target kinematic gait and control
 is performed with MuJoCo and finite-difference gradients.                                  inputs. The optimizer finds a dynamically feasible motion that
 The results are visualized for the quadruped in Fig. 6 and                                 closely tracks the kinematic plan (Fig. 6).
 summarized for all of the systems in Table III.                                               Overall, we find that final results from both engines are
    Box: Inputs are optimized to move a stationary rigid body                               similar. However, importantly, MuJoCo is enforcing soft con-
 that is resting on a flat surface (Fig. 4) to a goal location that                         tact whereas Dojo simulates hard contact. Dojo’s gradients
 is either to the right or up in the air 1 meter. The planning                              are computed with κ = 3e−4. Further, for systems with
 horizon is 1 second and the controls are initialized with zeros.                           contact, MuJoCo requires a time step h = 0.01 for successful
                                                                                                                                               13



                                                                          TABLE VI: Policy optimization results. Comparison of total reward,
                                                                          number of simulation-step and gradient evaluations for a collection
                                                                          of policies trained with Augmented Random Search (ARS) [90] and
                                                                          Augmented Gradient Search (AGS). For AGS, we test with both
                                                                          implicit gradients and randomized gradients. The results are averaged
                                                                          over the best 3 out of 5 runs with different random seeds. Optimizing
                                                                          with implicit gradients from Dojo reaches similar performance levels
                                                                          while being 5 to 10 times more sample efficient, while optimizing
                                                                          with randomized finite difference gradients is 3 to 5 times more
                                                                          sample efficient.
                                                                              Environment        Method         Reward    Simulation Evals
                                                                                                  ARS           46 ± 24        3e+4
                                                                              Half-Cheetah      AGS (Dojo)      44 ± 24        5e+3
                                                                                               AGS (random)     39 ± 27        8e+3
Fig. 11: Learned policy rollouts for half-cheetah (top) and ant                                   ARS           64 ± 15        2e+5
(bottom). Time progresses left to right.                                           Ant          AGS (Dojo)      54 ± 28        2e+4
                                                                                               AGS (random)     59 ± 24        4e+4

optimization, whereas Dojo succeeds with h = 0.05.
                                                                          Dojo performs one-step simulation to predict the next state,
C. Policy Optimization                                                    ẑ+ . Implicit gradients are utilized by a Gauss-Newton method
                                                                          to perform gradient-based learning of the system parameters.
   Gym-like environments [20, 89]: ant and half-cheetah are
                                                                             The parameters are learned by minimizing the following
implemented in Dojo and we train static linear policies for
                                                                          loss:
locomotion. As a baseline, we employ Augmented Random
                                                                                                          X 1
Search (ARS) [90], a gradient-free approach coupling random
                                                                                         X
                                                                            L(D, θ) =        L(Z, θ) =           ||Dojo(z− , z; θ) − z+ ||2W ,
search with a number of simple heuristics. For comparison, we                                                  2
                                                                                         Z∈D              Z∈D
train the same policies using augmented gradient search (AGS)                                                                                (55)
which replaces the stochastic-gradient estimation of ARS with
Dojo’s implicit gradients. Policy rollouts are visualized in Fig.         where || · ||W is a weighted norm, which aims to minimize the
11 and results are summarized in Table VI.                                difference between the ground-truth trajectories and physics-
   Half-cheetah: This planar system with m = 6 controls and               engine predictions. We use gradients
n = 18 degrees-of-freedom is rewarded for forward velocity                         ∂L     ∂Dojo T
and penalized for control effort over a horizon T = 80 with                            =          W (Dojo(z− , z; θ) − z+ ) ,                (56)
                                                                                   ∂θ      ∂θ
time step h = 0.05.
                                                                          and approximate Hessians
   Ant: The system has m = 8 controls and n = 28 degrees-of-
freedom and is rewarded for forward motion and maintaining                                   ∂2L      ∂Dojo T ∂Dojo
a certain altitude and is penalized for control effort and contact                               2
                                                                                                   ≈          W         .           (57)
                                                                                              ∂θ       ∂θ          ∂θ
over a horizon T = 150 with time step h = 0.05.                           Gradients are computed with κ = 3e−4.
   First, we are able to successfully train policies using this              After training, the learned parameters are within 5% of the
simple learning algorithm in Dojo’s hard contact environ-                 true geometry and friction coefficient for the box from the
ments. Second, MuJoCo requires smaller h = 0.01 time steps                dataset. We complete the real-to-sim transfer and simulate
for stable simulation, whereas Dojo is stable with h = 0.05.              the learned system in Dojo, comparing it to the ground-truth
Third, our initial results indicate that it is possible to train          dataset trajectories. Results are visualized in Fig. 12.
comparable polices in Dojo with 5 to 10 times less samples
by utilizing implicit gradients compared to the gradient-free
                                                                                                  VI. C ONCLUSION
method.
                                                                            Dojo is designed from physics- and optimization-first princi-
                                                                          ples to enable better gradient-based optimization for planning,
D. System Identification
                                                                          control, policy optimization, and system identification.
   System identification is performed on an existing real-
world dataset of trajectories collected by throwing a box on
a table with different initial conditions [91]. We learn a set            A. Contributions
of parameters θ = (cf , p(1) , . . . , p(8) ) that include the friction      The engine makes several advancements over previous state-
coefficient cf , and 3-dimensional vectors p(i) that represent            of-the-art engines for robotics: First, the variational integra-
the position of vertex i of the box with respect to its center            tor enables stable simulation at low sample rates. Second,
of mass.                                                                  the contact model includes an improved friction model that
   Each trajectory is decomposed into T − 2 triplets of consec-           eliminates artifacts like creep, particularly for sliding, and
utive configurations: Z = (z− , z, z+ ), where T is the number            hard contact for impact is achieved to machine precision. This
of time steps in the trajectory. Using the initial conditions z− , z      enables sim-to-real transfer for implementation on real robot
from a tuple, and an estimate of the system’s parameters θ,               hardware. The underlying primal-dual interior point solver,
                                                                                                                                    14



developed specifically for solving NCPs, is numerically robust             Iteration:       (1)        (5)       (50)     truth
and minimizes user hyperparameter tuning, while offering
good performance across numerous systems, and handling
cone and quaternion variables. Third, the engine efficiently
returns implicit gradients whose smoothness through contact
are tuned by the user to trade off gradient smoothness with
simulation accuracy, providing useful information through
contact events. Fourth, in addition to building and providing
Dojo as an open-source tool, the physics and optimization
algorithms presented can be ported into existing simulation
engines.

B. Limitations
   In terms of features, reliability, and wall-clock time,
MuJoCo–the product of a decade of excellent software              Fig. 12: System identification. Top right: Learning box geometry and
engineering–is impressive. As development of Dojo contin-         friction cone to less than 5% error. Bottom: Simulated trajectory of
ues, we expect to make significant progress in all of these       the box using the learned properties (blue) compared to ground truth
areas. However, fundamentally, Dojo’s approach of solving an      (orange).
NCP with a primal-dual interior point method requires more
computation per time step compared to existing simulators         translate into better transfer of simulation results to successes
that use a soft-contact model (e.g. MuJoCo and Drake), but        on real-world robotic hardware. In this thrust, future work
allows for accurate simulation with a lower sample rate,          will explore the transfer of control policies trained in Dojo to
making wall-clock comparisons between the two simulators          hardware and deployment of the engine in model predictive
difficult. This is the fundamental trade-off Dojo makes for       control frameworks.
robotics applications: greater computational cost per time step      In conclusion, we have presented a new physics engine,
for accurate physics and smooth gradients over fewer total        Dojo, specifically designed for robotics. This tool is the
time steps.                                                       culmination of a number of improvements to the contact
   Additionally, it should be acknowledged that Dojo’s interior   dynamics model and underlying optimization routines, aiming
point solver is solving a nonconvex optimization problem          to advance state-of-the-art physics engines for robotics by
at each simulation time step, which may have a danger of          improving physical accuracy and differentiability.
reaching poor local minima or not converging within the
allotted time window. Although in practice, we do not find this                       ACKNOWLEDGEMENTS
to be a problem, but for time- or safety-critical applications      The authors would like to thank Suvansh Sanjeev for
this should be a consideration. Moreover, the same is true        assistance with the Python interface. Toyota Research Institute
in using Dojo’s gradients for trajectory optimization, policy     provided funds to support this work.
optimization, or system identification. These require solving
inherently nonconvex optimization problems, which may con-                                  R EFERENCES
verge to poor local solutions, or fail to converge, regardless
                                                                   [1] O. M. Andrychowicz, B. Baker, M. Chociej, R. Joze-
of the smoothness or quality of Dojo’s gradient information.
                                                                       fowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert,
Although smoother gradients may facilitate optimization for
                                                                       G. Powell, A. Ray, et al., “Learning dexterous in-hand
these problems, they do not fully resolve the complexities
                                                                       manipulation,” The International Journal of Robotics
introduced by nonconvex optimization landscapes.
                                                                       Research, vol. 39, no. 1, pp. 3–20, 2020.
                                                                   [2] I. Akkaya, M. Andrychowicz, M. Chociej, M. Litwin,
C. Future Work                                                         B. McGrew, A. Petron, A. Paino, M. Plappert, G. Powell,
   A number of future improvements to Dojo are planned.                R. Ribas, et al., “Solving Rubik’s cube with a robot
First, Dojo currently implements simple collision detection            hand,” arXiv:1910.07113, 2019.
(e.g., sphere-halfspace, sphere-sphere). Natural extensions in-    [3] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and
clude support for convex primitives and curved surfaces and            M. Hutter, “Learning quadrupedal locomotion over chal-
triangular meshes. Another improvement is adaptive time                lenging terrain,” Science Robotics, vol. 5, no. 47, 2020.
stepping. Similar to advanced numerical integrators for stiff      [4] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “RMA: Rapid
systems, Dojo should take large time steps when possible and           motor adaptation for legged robots,” arXiv:2107.04034,
adaptively modify the time step in cases of numerical diffi-           2021.
culties or physical inaccuracies. Finally, hardware-accelerator    [5] S. Levine, P. Pastor, A. Krizhevsky, J. Ibarz, and
support for Dojo would potentially enable faster simulation            D. Quillen, “Learning hand-eye coordination for robotic
and optimization.                                                      grasping with deep learning and large-scale data collec-
   Perhaps the most important remaining question is whether            tion,” The International Journal of Robotics Research,
the physics and optimization improvements from this work               vol. 37, no. 4-5, pp. 421–436, 2018.
                                                                                                                               15



 [6] W. Zhao, J. P. Queralta, and T. Westerlund, “Sim-to-real     [22] P. Parmas, C. E. Rasmussen, J. Peters, and K. Doya,
     transfer in deep reinforcement learning for robotics: a           “Pipps: Flexible model-based policy search robust to the
     survey,” in 2020 IEEE Symposium Series on Computa-                curse of chaos,” in International Conference on Machine
     tional Intelligence (SSCI), pp. 737–744, 2020.                    Learning, pp. 4065–4074, PMLR, 2018.
 [7] R. Tedrake and the Drake Development Team, “Drake:           [23] L. Metz, C. D. Freeman, S. S. Schoenholz, and T. Kach-
     Model-based design and verification for robotics,” 2019.          man, “Gradients are not all you need,” arXiv preprint
 [8] C. D. Freeman, E. Frey, A. Raichuk, S. Girgin,                    arXiv:2111.05803, 2021.
     I. Mordatch, and O. Bachem, “Brax–A differentiable           [24] E. Todorov, “Convex and analytically-invertible dynam-
     physics engine for large scale rigid body simulation,”            ics with contacts and constraints: Theory and implemen-
     arXiv:2106.13281, 2021.                                           tation in MuJoCo,” in IEEE International Conference on
 [9] K. Werling, D. Omens, J. Lee, I. Exarchos, and C. K.              Robotics and Automation, pp. 6054–6061, 2014.
     Liu, “Fast and feature-complete differentiable physics for   [25] Legged Robotics Group, “SimBenchmark: Benchmark-
     articulated rigid bodies with contact,” arXiv:2103.16021,         ing Simulation Performance for Legged Robots,” 2025.
     2021.                                                             Accessed: 2025-02-17.
[10] M. Geilinger, D. Hahn, J. Zehnder, M. Bächer,               [26] Y. Tassa, T. Erez, and E. Todorov, “Synthesis and stabi-
     B. Thomaszewski, and S. Coros, “ADD: Analytically                 lization of complex behaviors through online trajectory
     differentiable dynamics for multi-body systems with fric-         optimization,” in IEEE/RSJ International Conference on
     tional contact,” ACM Transactions on Graphics, vol. 39,           Intelligent Robots and Systems, pp. 4906–4913, 2012.
     no. 6, pp. 1–15, 2020.                                       [27] K. H. Hunt and F. R. E. Crossley, “Coefficient of resti-
[11] Y. Hu, L. Anderson, T.-M. Li, Q. Sun, N. Carr, J. Ragan-          tution interpreted as damping in vibroimpact,” 1975.
     Kelley, and F. Durand, “DiffTaichi: Differentiable pro-      [28] A. M. Castro, F. N. Permenter, and X. Han, “An uncon-
     gramming for physical simulation,” International Con-             strained convex formulation of compliant contact,” IEEE
     ference on Learning Representations, 2020.                        Transactions on Robotics, vol. 39, no. 2, pp. 1301–1320,
[12] E. Heiden, D. Millard, E. Coumans, Y. Sheng, and                  2022.
     G. S. Sukhatme, “NeuralSim: Augmenting differentiable        [29] H. J. T. Suh, T. Pang, and R. Tedrake, “Bundled gradi-
     simulators with neural networks,” IEEE International              ents through contact via randomized smoothing,” IEEE
     Conference on Robotics and Automation, pp. 9474–9481,             Robotics and Automation Letters, vol. 7, no. 2, pp. 4000–
     2021.                                                             4007, 2022.
[13] NVIDIA Corporation, “Isaac Sim: Simulation for               [30] N. Koenig and A. Howard, “Design and use paradigms
     Robotics,” 2025. Accessed: 2025-02-19.                            for Gazebo, an open-source multi-robot simulator,” in
[14] G. Authors, “Genesis: A universal and generative physics          IEEE/RSJ International Conference on Intelligent Robots
     engine for robotics and beyond,” December 2024.                   and Systems, vol. 3, pp. 2149–2154, 2004.
[15] M. Macklin, M. Müller, N. Chentanez, and T.-Y. Kim,         [31] E. Coumans and Y. Bai, “PyBullet, a Python module
     “Unified particle physics for real-time applications,”            for physics simulation for games, robotics and machine
     ACM Transactions on Graphics (TOG), vol. 33, no. 4,               learning,” 2016–2019.
     pp. 1–12, 2014.                                              [32] J. Lee, M. X. Grey, S. Ha, T. Kunz, S. Jain, Y. Ye, S. S.
[16] N. Agarwal, A. Ali, M. Bala, Y. Balaji, E. Barker, T. Cai,        Srinivasa, M. Stilman, and C. K. Liu, “DART: Dynamic
     P. Chattopadhyay, Y. Chen, Y. Cui, Y. Ding, et al.,               animation and robotics toolkit,” Journal of Open Source
     “Cosmos world foundation model platform for physical              Software, vol. 3, no. 22, p. 500, 2018.
     ai,” arXiv preprint arXiv:2501.03575, 2025.                  [33] J. K. Murthy, M. Macklin, F. Golemo, V. Voleti,
[17] G. Zhou, H. Pan, Y. LeCun, and L. Pinto, “Dino-wm:                L. Petrini, M. Weiss, B. Considine, J. Parent-Lévesque,
     World models on pre-trained visual features enable zero-          K. Xie, K. Erleben, et al., “gradsim: Differentiable simu-
     shot planning,” arXiv preprint arXiv:2411.04983, 2024.            lation for system identification and visuomotor control,”
[18] M. Parmar, M. Halm, and M. Posa, “Fundamental chal-               in International conference on learning representations,
     lenges in deep learning for stiff contact dynamics,” in           2020.
     2021 IEEE/RSJ International Conference on Intelligent        [34] E. Heiden, M. Macklin, Y. Narang, D. Fox, A. Garg,
     Robots and Systems (IROS), pp. 5181–5188, 2021.                   and F. Ramos, “Disect: A differentiable simulation en-
[19] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics             gine for autonomous robotic cutting,” arXiv preprint
     engine for model-based control,” in IEEE/RSJ Interna-             arXiv:2105.12244, 2021.
     tional Conference on Intelligent Robots and Systems,         [35] Nvidia, “PhysX physics engine,” 2022.
     pp. 5026–5033, 2012.                                         [36] R. Newbury, J. Collins, K. He, J. Pan, I. Posner,
[20] G. Brockman, V. Cheung, L. Pettersson, J. Schneider,              D. Howard, and A. Cosgun, “A review of differentiable
     J. Schulman, J. Tang, and W. Zaremba, “OpenAI Gym,”               simulators,” IEEE Access, 2024.
     arXiv:1606.01540, 2016.                                      [37] M. A. Toussaint, K. R. Allen, K. A. Smith, and J. B.
[21] H. J. Suh, M. Simchowitz, K. Zhang, and R. Tedrake,               Tenenbaum, “Differentiable physics and stable modes for
     “Do differentiable simulators give better policy gradi-           tool-use and manipulation planning,” 2018.
     ents?,” in International Conference on Machine Learn-        [38] F. de Avila Belbute-Peres, K. Smith, K. Allen, J. Tenen-
     ing, pp. 20668–20696, PMLR, 2022.                                 baum, and J. Z. Kolter, “End-to-end differentiable
                                                                                                                                16



     physics for learning and control,” Advances in neural              contact dynamics,” in 2009 IEEE 12th International
     information processing systems, vol. 31, 2018.                     Conference on Computer Vision, pp. 2389–2396, IEEE,
[39] C. Song and A. Boularias, “Learning to slide unknown               2009.
     objects with differentiable physics simulations,” arXiv       [55] K. S. Bhat, C. D. Twigg, J. K. Hodgins, P. Khosla,
     preprint arXiv:2005.05456, 2020.                                   Z. Popovic, and S. M. Seitz, “Estimating cloth simulation
[40] C. Song and A. Boularias, “Identifying mechanical mod-             parameters from video,” 2003.
     els through differentiable simulations,” arXiv preprint       [56] C. K. Liu, A. Hertzmann, and Z. Popović, “Learn-
     arXiv:2005.05410, 2020.                                            ing physics-based motion style with nonlinear inverse
[41] J. Degrave, M. Hermans, J. Dambre, and F. Wyffels,                 optimization,” ACM Transactions on Graphics (TOG),
     “A differentiable physics engine for deep learning in              vol. 24, no. 3, pp. 1071–1081, 2005.
     robotics,” Frontiers in neurorobotics, vol. 13, p. 6, 2019.   [57] R. Grzeszczuk, D. Terzopoulos, and G. Hinton, “Neu-
[42] J. Wu, E. Lu, P. Kohli, B. Freeman, and J. Tenenbaum,              roanimator: Fast neural network emulation and control
     “Learning to see physics via visual de-animation,” Ad-             of physics-based models,” in Proceedings of the 25th
     vances in neural information processing systems, vol. 30,          annual conference on Computer graphics and interactive
     2017.                                                              techniques, pp. 9–20, 1998.
[43] V. L. Guen and N. Thome, “Disentangling physical              [58] G. Sutanto, A. Wang, Y. Lin, M. Mukadam, G. Sukhatme,
     dynamics from unknown factors for unsupervised video               A. Rai, and F. Meier, “Encoding physical constraints in
     prediction,” in Proceedings of the IEEE/CVF Conference             differentiable newton-euler algorithm,” in Learning for
     on Computer Vision and Pattern Recognition, pp. 11474–             Dynamics and Control, pp. 804–813, PMLR, 2020.
     11484, 2020.                                                  [59] K. Wang, M. Aanjaneya, and K. Bekris, “A first princi-
[44] C. Schenck and D. Fox, “Spnets: Differentiable fluid               ples approach for data-efficient system identification of
     dynamics for deep neural networks,” in Conference on               spring-rod systems via differentiable physics engines,”
     Robot Learning, pp. 317–335, PMLR, 2018.                           in Learning for Dynamics and Control, pp. 651–665,
[45] M. Jaques, M. Burke, and T. Hospedales, “Physics-                  PMLR, 2020.
     as-inverse-graphics: Joint unsupervised learning of           [60] D. Murray-Smith, “The inverse simulation approach: a
     objects and physics from video,” arXiv preprint                    focused review of methods and applications,” Mathe-
     arXiv:1905.11169, 2019.                                            matics and computers in simulation, vol. 53, no. 4-6,
[46] E. Heiden, D. Millard, H. Zhang, and G. S. Sukhatme,               pp. 239–247, 2000.
     “Interactive differentiable simulation,” arXiv preprint       [61] G. Kim, D. Kang, J.-H. Kim, and H.-W. Park, “Contact-
     arXiv:1905.10706, 2019.                                            implicit differential dynamic programming for model
[47] Y. Hu, J. Liu, A. Spielberg, J. B. Tenenbaum, W. T.                predictive control with relaxed complementarity con-
     Freeman, J. Wu, D. Rus, and W. Matusik, “Chainqueen:               straints,” in 2022 IEEE/RSJ International Conference on
     A real-time differentiable physical simulator for soft             Intelligent Robots and Systems (IROS), pp. 11978–11985,
     robotics,” in 2019 International conference on robotics            2022.
     and automation (ICRA), pp. 6265–6271, IEEE, 2019.             [62] M. Macklin, “Warp: A high-performance python frame-
[48] J. Liang, M. Lin, and V. Koltun, “Differentiable cloth             work for gpu simulation and graphics,” in NVIDIA GPU
     simulation for inverse problems,” Advances in Neural               Technology Conference (GTC), 2022.
     Information Processing Systems, vol. 32, 2019.                [63] M. Macklin, M. Müller, and N. Chentanez, “Xpbd:
[49] Y. Li, J. Wu, R. Tedrake, J. B. Tenenbaum, and A. Tor-             position-based simulation of compliant constrained dy-
     ralba, “Learning particle dynamics for manipulating rigid          namics,” in Proceedings of the 9th International Confer-
     bodies, deformable objects, and fluids,” arXiv preprint            ence on Motion in Games, pp. 49–54, 2016.
     arXiv:1810.01566, 2018.                                       [64] K. M. Jatavallabhula, M. Macklin, F. Golemo, V. Voleti,
[50] M. Salzmann and R. Urtasun, “Physically-based motion               L. Petrini, M. Weiss, B. Considine, J. Parent-Lévesque,
     models for 3d tracking: A convex formulation,” in 2011             K. Xie, K. Erleben, et al., “gradsim: Differentiable simu-
     International Conference on Computer Vision, pp. 2064–             lation for system identification and visuomotor control,”
     2071, IEEE, 2011.                                                  arXiv preprint arXiv:2104.02646, 2021.
[51] M. A. Brubaker, D. J. Fleet, and A. Hertzmann,                [65] J. Carpentier and N. Mansard, “Analytical derivatives of
     “Physics-based person tracking using the anthropomor-              rigid body dynamics algorithms,” in Robotics: Science
     phic walker,” International journal of computer vision,            and systems (RSS 2018), 2018.
     vol. 87, no. 1, pp. 140–155, 2010.                            [66] M. Giftthaler, M. Neunert, M. Stäuble, M. Frigerio,
[52] K. R. Kozlowski, Modelling and identification in                   C. Semini, and J. Buchli, “Automatic differentiation of
     robotics. Springer Science & Business Media, 2012.                 rigid body dynamics for optimal control and estimation,”
[53] P. M. Wensing, S. Kim, and J.-J. E. Slotine, “Linear               Advanced Robotics, vol. 31, no. 22, pp. 1225–1237,
     matrix inequalities for physically consistent inertial pa-         2017.
     rameter identification: A statistical perspective on the      [67] S. Cheng, M. Kim, L. Song, C. Yang, Y. Jin, S. Wang,
     mass distribution,” IEEE Robotics and Automation Let-              and N. Hovakimyan, “Difftune: Auto-tuning through
     ters, vol. 3, no. 1, pp. 60–67, 2017.                              auto-differentiation,” IEEE Transactions on Robotics,
[54] M. A. Brubaker, L. Sigal, and D. J. Fleet, “Estimating             2024.
                                                                                                                                      17



[68] Q. Chen, S. Cheng, and N. Hovakimyan, “Simultaneous            [85] M. Posa, C. Cantu, and R. Tedrake, “A direct method for
     spatial and temporal assignment for fast uav trajectory             trajectory optimization of rigid bodies through contact,”
     optimization using bilevel optimization,” IEEE Robotics             The International Journal of Robotics Research, vol. 33,
     and Automation Letters, vol. 8, no. 6, pp. 3860–3867,               no. 1, pp. 69–81, 2014.
     2023.                                                          [86] W. Li and E. Todorov, “Iterative linear quadratic regula-
[69] M. A. Z. Mora, M. Peychev, S. Ha, M. Vechev, and                    tor design for nonlinear biological movement systems,”
     S. Coros, “Pods: Policy optimization via differentiable             in International Conference on Informatics in Control,
     simulation,” in International Conference on Machine                 Automation and Robotics, pp. 222–229, 2004.
     Learning, pp. 7805–7817, PMLR, 2021.                           [87] T. A. Howell, S. Le Cleac’h, S. Singh, P. Florence,
[70] Q. Le Lidec, I. Kalevatykh, I. Laptev, C. Schmid, and               Z. Manchester, and V. Sindhwani, “Trajectory optimiza-
     J. Carpentier, “Differentiable simulation for physical              tion with optimization-based dynamics,” IEEE Robotics
     system identification,” IEEE Robotics and Automation                and Automation Letters, vol. 7, no. 3, pp. 6750–6757,
     Letters, vol. 6, no. 2, pp. 3413–3420, 2021.                        2022.
[71] J. Brüdigam, J. Janeva, S. Sosnowski, and S. Hirche,          [88] M. H. Raibert, H. B. Brown Jr., M. Chepponis, J. Koech-
     “Linear-time contact and friction dynamics in                       ling, J. K. Hodgins, D. Dustman, W. K. Brennan, D. S.
     maximal coordinates using variational integrators,”                 Barrett, C. M. Thompson, J. D. Hebert, W. Lee, and
     arXiv:2109.07262, 2021.                                             B. Lance, “Dynamically stable legged locomotion,” tech.
[72] J. J. Moreau, “On unilateral constraints, friction and plas-        rep., Massachusetts Institute of Technology Cambridge
     ticity,” in New Variational Techniques in Mathematical              Artificial Intelligence Lab, 1989.
     Physics, pp. 171–322, Springer, 2011.                          [89] Y. Duan, X. Chen, R. Houthooft, J. Schulman, and
[73] M. S. Lobo, L. Vandenberghe, S. Boyd, and H. Le-                    P. Abbeel, “Benchmarking deep reinforcement learning
     bret, “Applications of second-order cone programming,”              for continuous control,” in International Conference on
     Linear Algebra and its Applications, vol. 284, no. 1-3,             Machine Learning, pp. 1329–1338, 2016.
     pp. 193–228, 1998.                                             [90] H. Mania, A. Guy, and B. Recht, “Simple random search
[74] D. E. Stewart and J. C. Trinkle, “An implicit time-                 of static linear policies is competitive for reinforcement
     stepping scheme for rigid body dynamics with inelastic              learning,” in Advances in Neural Information Processing
     collisions and Coulomb friction,” International Journal             Systems, pp. 1800–1809, 2018.
     for Numerical Methods in Engineering, vol. 39, no. 15,         [91] S. Pfrommer, M. Halm, and M. Posa, “ContactNets:
     pp. 2673–2691, 1996.                                                Learning discontinuous contact dynamics with smooth,
[75] U. Dini, Lezioni di analisi infinitesimale, vol. 1. Fratelli        implicit representations,” in Conference on Robot Learn-
     Nistri, 1907.                                                       ing, pp. 2279–2291, 2021.
[76] J. Brüdigam and Z. Manchester, “Linear-time variational
     integrators in maximal coordinates,” in International                                    A PPENDIX A
     Workshop on the Algorithmic Foundations of Robotics,                               Q UATERNION A LGEBRA
     pp. 194–209, 2020.                                                In this section we introduce a set of conventions for notating
[77] J. E. Marsden and M. West, “Discrete mechanics and             standard quaternion operations, adopted from [76, 83], and
     variational integrators,” Acta Numerica, vol. 10, pp. 357–     employed in the rotational part of our variational integrator
     514, 2001.                                                     (17).
[78] Z. Manchester and S. Kuindersma, “Variational contact-            Quaternions are written as four-dimensional vectors:
     implicit trajectory optimization,” in Robotics Research,
                                                                                    q = (s, v) = (s, v1 , v2 , v3 ) ∈ H,           (58)
     pp. 985–1000, Springer, 2020.
[79] Z. R. Manchester and M. A. Peck, “Quaternion varia-            where s and v are scalar and vector components, respectively.
     tional integrators for spacecraft dynamics,” Journal of        Dojo employs unit quaternions (i.e., q T q = 1) to represent
     Guidance, Control, and Dynamics, vol. 39, no. 1, pp. 69–       orientation, providing a mapping from the local body frame
     76, 2016.                                                      to a global inertial frame.
[80] L. Vandenberghe, “The CVXOPT linear and                           Quaternion multiplication is represented using linear algebra
     quadratic      cone      program      solvers,”     Online:    (i.e., matrix-vector and matrix-matrix products). Left and right
     http://cvxopt.org/documentation/coneprog.pdf, 2010.            quaternion multiplication:
[81] S. Mehrotra, “On the implementation of a primal-dual                             sa sb − (v a )T v b
                                                                                                          
     interior point method,” SIAM Journal on Optimization,            qa · qb = a b                          = L(q a )q b = R(q b )q a ,
                                                                                  s v + sb v a + v a × v b
     vol. 2, no. 4, pp. 575–601, 1992.                                                                                             (59)
[82] J. Nocedal and S. J. Wright, Numerical Optimization.           where × is the standard vector cross product, is represented
     Springer, second ed., 2006.                                    using the matrices:
[83] B. E. Jackson, K. Tracy, and Z. Manchester, “Planning
                                                                                                      −v T
                                                                                                              
                                                                                            s
     with attitude,” IEEE Robotics and Automation Letters,                       L(q) =                          ∈ R4×4 ,          (60)
                                                                                            v sI3 + skew(v)
     vol. 6, no. 3, pp. 5658–5664, 2021.
                                                                                                      −v T
                                                                                                              
[84] S. Boyd and L. Vandenberghe, Convex Optimization.                                      s
                                                                                 R(q) =                          ∈ R4×4 ,          (61)
     Cambridge University Press, 2004.                                                      v sI3 − skew(v)
                                                                 18



where:                                             
                         0              −x3     x2
             skew(x) =  x3              0      −x1  ,   (62)
                        −x2              x1      0
is defined such that:
                        skew(x)y = x × y,                 (63)
and I3 is a 3-dimensional identity matrix. The vector compo-
nent of a quaternion:
                          v = V q,                       (64)
is extracted using the matrix:
                    V = 0 I3 ∈ R3×4 ,
                              
                                                          (65)
and quaternion conjugate:
                                    
                                   s
                        q† =           = T q,             (66)
                                  −v
is computed using:
                                   0T
                                      
                       1
                   T =                   ∈ R4×4 .         (67)
                       0           −I3
