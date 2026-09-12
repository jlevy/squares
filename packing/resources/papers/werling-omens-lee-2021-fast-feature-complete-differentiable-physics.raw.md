                                            Fast and Feature-Complete Differentiable Physics
                                                for Articulated Rigid Bodies with Contact
                                                       Keenon Werling1 , Dalton Omens1 , Jeongseok Lee2 , Ioannis Exarchos1 and C. Karen Liu1
                                                            1
                                                                Stanford University: {keenon, domens, exarchos, ckliu38}@stanford.edu
                                                                                   2
                                                                                     Robotics AI, Amazon: jeoslee@amazon.com


                                            Abstract—We present a fast and feature-complete differen-
                                         tiable physics engine, Nimble (nimblephysics.org), that supports
                                         Lagrangian dynamics and hard contact constraints for articu-
arXiv:2103.16021v3 [cs.RO] 22 Jun 2021




                                         lated rigid body simulation. Our differentiable physics engine
                                         offers a complete set of features that are typically only available in
                                         non-differentiable physics simulators commonly used by robotics
                                         applications. We solve contact constraints precisely using linear
                                         complementarity problems (LCPs). We present efficient and novel
                                         analytical gradients through the LCP formulation of inelastic
                                         contact that exploit the sparsity of the LCP solution. We
                                         support complex contact geometry, and gradients approximating
                                         continuous-time elastic collision. We also introduce a novel             Fig. 1. Boston Dynamics’ Atlas Robot learning to do yoga, being simulated
                                         method to compute complementarity-aware gradients that help              by our engine. This robot has 34 mesh colliders and 32 degrees of freedom.
                                                                                                                  This freeze frame contains 24 contact points, 12 per foot. Even with all that
                                         downstream optimization tasks avoid stalling in saddle points.
                                                                                                                  complexity, we are able to compute the Jacobians of dynamics on this robot
                                         We show that an implementation of this combination in a                  87x faster on a single CPU core using the analytical methods introduced in this
                                         fork of an existing physics engine (DART) is capable of a                paper than by finite differencing (only 8.5ms vs 749ms for finite differencing).
                                         87x single-core speedup over finite-differencing in computing
                                         analytical Jacobians for a single timestep, while preserving all
                                         the expressiveness of original DART.
                                                                                                              A fully-featured physics engine like DART is complex
                                                                                                           and has many components that must be differentiated. Some
                                                                I. I NTRODUCTION                           components (such as collision detection and contact force
                                                                                                           computation) are not naively differentiable, but we show that
                                            Many modern robotics problems are optimization problems.
                                                                                                           under very reasonable assumptions we can compute useful
                                         Finding optimal trajectories, guessing the physical parameters
                                                                                                           Jacobians regardless. In order to differentiate through contacts
                                         of a world that best fits our observed data, or designing a
                                                                                                           and collision forces, we introduce an efficient method for
                                         control policy to optimally respond to a dynamic environment
                                                                                                           differentiating the contact Linear Complementarity Problem
                                         are all types of optimization problems. Optimization methods
                                                                                                           (LCP) that exploits sparsity, as well as novel contact geometry
                                         can be sorted into two buckets: gradient-based, and gradient-
                                                                                                           algorithms and an efficient continuous-time approximation for
                                         free. Despite the well-known drawbacks of gradient-free
                                                                                                           elastic collisions. As a result, our engine is able to compute
                                         methods (high sample complexity and noisy solutions), they
                                                                                                           gradients with hard contact constraints up to 87 times faster
                                         remain popular in robotics because physics engines with the
                                                                                                           than finite differencing methods, depending on the size of the
                                         necessary features to model complex robots are generally
                                                                                                           dynamic system. Our relative speedup over finite differencing
                                         non-differentiable. When gradients are required, we typically
                                                                                                           grows as the system complexity grows. In deriving our novel
                                         approximate them using finite differencing [41].
                                                                                                           method to differentiate through the LCP, we also gain an
                                            Recent years have seen many differentiable physics engines understanding of the nature of contact dynamics Jacobians
                                         published [11, 19, 15, 42, 38, 10, 34, 29, 12], but none has yet that allows us to propose heuristic “complementarity-aware
                                         gained traction as a replacement for popular non-differentiable gradients” that may be good search directions to try, if a
                                         engines [9, 41, 26]. We hypothesize that an ideal differentiable downstream optimizer is getting stuck in a saddle point.
                                         physics engine needs to implement an equivalent feature set to
                                                                                                              We provide an open-source implementation of all of these
                                         existing popular non-differentiable engines, as well as provide
                                                                                                           ideas, as well as derivations from previous work [25, 7], in a
                                         excellent computational efficiency, in order to gain adoption. In
                                                                                                           fully differentiable fork of the DART physics engine, which
                                         this paper, we extend the existing physics engine DART [26],
                                                                                                           we call Nimble. Code and documentation are available at
                                         which is commonly used in robotics and graphics communities,
                                                                                                           nimblephysics.org.
                                         and make it differentiable. Our resulting engine supports all
                                         features available to the forward simulation process, meaning        To summarize, our contributions are as follows:
                                         existing code and applications will remain compatible while          • A novel and fast method for local differentiability of LCPs
                                         also enjoying new capabilities enabled by efficient analytical         that exploits the sparsity of the LCP solution, which
                                         differentiability.                                                     gives us efficient gradients through static and sliding
                                                                    tends to introduce round-off errors and performs poorly for a
 Engine          Contact      Dynamic      Collision    Gradients   large number of input variables.
                  Force        State       Geometry      Method        Automatic differentiation (auto-diff) is a method for
 MuJoCo        customized    generalized   complete       finite    computing gradients of a sequence of elementary arithmetic
 Degrave         impulse      cartesian    primitives      auto     operations or functions automatically. However, the constraint
 DiffTaichi      impulse       caresian    primitives      auto     satisfaction problems required by many existing, feature-
 Heiden         iter LCP     generalized   primitives      auto
                                                                    complete robotic physics engines are not supported by auto-diff
 de A. B.-P.   direct LCP     cartesian    primitives   symbolic
 Geilinger     customized    generalized   primitives   symbolic    libraries. To avoid this issue, many recent differentiable physics
                                                                    engines instead implement impulse-based contact handling,
 Ours          direct LCP    generalized   complete     symbolic
                                                                    which could lead to numerical instability and constraint
                                                                    violation if the contact parameters are not tuned properly
                            TABLE I
  D IFFERENTIABLE ENGINES SUPPORTING ARTICULATED RIGID BODIES       for the specific dynamic system and the simulation task.
                                                                    Degrave et al. [11] implemented a rigid body simulator in
                                                                    the Theano framework [1], while DiffTaichi [18] implemented
    contacts and friction without changing traditional forward-     a number of differentiable physics engines, including rigid
    simulation formulations. Section IV                             bodies, extending the Taichi programming language [19], both
  • A novel method that manipulates gradient computation            representing dynamic equations in Cartesian coordinates and
    to help downstream optimization problems escape saddle          handling contact with impulse-based methods. In contrast, Tiny
    points due to discrete contact states. Section IV-D             Differentiable Simulator [15] models contacts as an LCP, but
  • Fast geometric analytical gradients through collision           they solve the LCP iteratively via Projected Gauss Siedel (PGS)
    detection algorithms which support various types of 3D          method [24], instead of directly solving a constraint satisfaction
    geometry and meshes. Section V                                  problem, making it possible to compute gradient using auto-diff
  • A novel analytical approximation of continuous-time             libraries.
    gradients through elastic contact, which otherwise can             Symbolic differentiation is another way to compute gra-
    lead to errors in discrete-time systems. Section VI             dients by directly differentiate mathematical expressions. For
  • An open-source implementation of all of our proposed            complex programs like Lagrangian dynamics with constraints
    methods (along with analytical gradients through Feather-       formulated as a Differential Algebraic Equations, symbolic
    stone first described in GEAR [25]) in a fork of the DART       differentiation can be exceedingly difficult. Earlier work
    physics engine which we call Nimble. We have created            computed symbolic gradients for smooth dynamic systems
    Python bindings and a PyPI package, pip install                 [25], and [7] simplified the computation of the derivative of
    nimblephysics, for ease of use.                                 the forward dynamics exploiting the derivative of the inverse
                                                                    dynamics. Symbolic differentiation becomes manageable when
                     II. R ELATED W ORK                             the gradients are only required within smooth contact modes
   Differentiable physics simulation has been investigated          [42] or a specific contact mode is assumed [38]. Recently, Amos
previously in many different fields, including mechanical           and Kolter proposed a method, Opt-Net, that back-propagates
engineering [16], robotics [14], physics [23, 21] and computer      through the solution of an optimization problem to its input
graphics [32, 28]. Enabled by recent advances in automatic          parameters [2]. Building on Opt-Net, de Avila Belbute-Peres et
differentiation methods and libraries [31, 1, 18], a number of      al. [10] derived analytical gradients through LCP formulated as
differentiable physics engines have been proposed to solve          a QP. Their method enables differentiability for rigid body
control and parameter estimation problems for rigid bodies          simulation with hard constraints, but their implementation
[25, 11, 18, 15, 10, 12, 34] and non-rigid bodies [37, 27, 13,      represents 2D rigid bodies in Cartesian coordinates and only
20, 34, 17, 12]. While they share a similar high-level goal         supports collisions with a plane, insufficient for simulating
of solving “inverse problems”, the features and functionality       complex articulated rigid body systems. More importantly,
provided by these engines vary widely, including the variations     computing gradients via QP requires solving a number of
in contact handling, state space parameterization and collision     linear systems which does not take advantage of the sparsity of
geometry support. Table II highlights the differences in a few      the LCP structure. Qiao et al. [34] built on [2] and improved
differentiable physics engines that have demonstrated the ability   the performance of contact handling by breaking a large scene
to simulate articulated rigid bodies with contact. Based on the     into smaller impact zones. A QP is solved for each impact
functionalities each engine intends to support, the approaches to   zone to ensure that the geometry is not interpenetrating, but
computing gradients can be organized in following categories.       contact dynamics and conservation laws are not considered.
   Finite-differencing is a straightforward way to approxi-         Solving contacts for localized zones has been previously
mate gradients of a function. For a feature-complete physics        implemented in many existing physics engines [41, 9, 26].
engine, where analytical gradients are complex to obtain,           Adapting the collision handling routine in DART, our method
finite-differencing provides a simpler method. For example, a       by default utilizes the localized contact zones to speed up
widely used physics engine, MuJoCo [41], supports gradient          the performance. Adjoint sensitivity analysis [35] has also
computation via finite differencing. However, finite-differencing   been used for computing gradients of dynamics. Millard et
al. [29] combined auto-diff with adjoint sensitivity analysis to    The velocity of a contact point at the next time step, vt+1 ,
achieve faster gradient computation for higher-dof systems, but can be expressed as a linear function in f
their method did not handle contact and collision. Geilinger
                                                                     vt+1 = J q̇t+1 = J M −1 M q̇t − ∆t(c − τ ) + J T f
                                                                                                                           
et al. [12] analytically computed derivatives through adjoint
sensitivity analysis and proposed a differentiable physics engine         = Af + b,                                          (4)
with implicit forward integration and a customized frictional where A = J M −1 J T and b = J (q̇ + ∆tM −1 (τ − c)). The
                                                                                                          t
contact model that is natively differentiable.                    LCP procedure can then be expressed as a function that maps
   Approximating physics with neural networks is a differ- (A, b) to the contact impulse f :
ent approach towards differentiable physics engine. Instead of                                                     
forward simulating a dynamic system from the first principles                 fLCP A(qt , µ), b(q t , q̇ t , τ , µ) = f      (5)
of Newtonian mechanics, a neural network is learned from            As such, the process of forward stepping is to find f and
training data. Examples of this approach include Battaglia et. resulting q̇
                                                                            t+1 that satisfy Equation 2 and Equation 5.
al [4], Chang et. al. [8], and Mrowca et. al [30].
   Our engine employs symbolic differentiation to compute
gradients through every part of the engine using hand-tuned
C++ code. We introduce a novel method to differentiate the
LCP analytically that takes advantage of the sparsity of the
solution and is compatible with using direct methods to solve
the LCP. In addition, our engine supports a richer set of
geometry for collision and contact handling than has been
previously available, including mesh-mesh and mesh-primitive
collisions, in order to achieve a fully functional differentiable
version of the DART physics engine for robotic applications.
                                                                         Fig. 2. Data flow during a forward simulation, visualizing equations 2 and
                           III. OVERVIEW                                 5. The inputs are q t and q̇ t , the current position and velocity in generalized
                                                                         coordinates, µ, the inertial properties, and τ , the external (control) torques on
                                                                         the joints. The outputs are the generalized position and velocity at the next
   A physics engine can be thought of as a simple function               timestep, q t+1 and q̇ t+1 . Every forward arrow represents a dependency in
that takes the current position q t , velocity q̇ t , control forces τ   data flow, which must be differentiated during backpropagation. Challenging
and inertial properties µ, and returns the position and velocity         dependencies, and the relevant sections where we introduce analytical Jacobians,
                                                                         are labeled with colored arrows and text in the diagram.
at the next timestep, q t+1 and q̇ t+1 :

                 P (q t , q̇ t , τ , µ) = [q t+1 , q̇ t+1 ].      (1)       The main task in developing a differentiable physics engine
                                                                         is to solve for the gradient of next velocity q̇ t+1 with respect
   In an engine with simple explicit time integration, our next          to the input to the current time step, namely q t , q̇ t , τt , and µ.
position q t+1 is a trivial function of current position and             The data flow is shown in Figure 2. For brevity we refer to the
velocity, q t+1 = q t + ∆tq̇ t , where ∆t is the descritized             ouput of a function for a given timestep by the same name as
time interval.                                                           the function with a subscript t (e.g. Jt = J (q t )). The velocity
   The computational work of the physics engine comes from               at the next step can be simplified to
solving for our next velocity, q̇ t+1 . We are representing our
articulated rigid body system in generalized coordinates using                                     q̇t+1 = q̇t + Mt−1 zt ,                            (6)
the following Lagrangian dynamic equation:                               where z t ≡ −∆t(ct − τt ) + JtT ft . The gradients we need to
                                                                         compute at each time step are written as:
  M (qt , µ)q̇t+1 = M (qt , µ)q̇t − ∆t(c(qt , q̇t , µ) − τ )
                                                                  (2)      ∂ q̇t+1   ∂Mt−1 z t
                                                                                                           
                                                                                                                    ∂ct        ∂JtT
                    + J T (qt )f ,                                                 =             + Mt −1
                                                                                                               −∆t        +         ft
                                                                            ∂qt          ∂q t                      ∂q t        ∂q t
where M is the mass matrix, c is the Coriolis and gravitational                          ∂f t
                                                                                              
force, and f is the contact impulse transformed into the                           +J Tt                                                  (7)
                                                                                         ∂q t
generalized coordinates by the contact Jacobian matrix J . Note                                                              
                                                                           ∂ q̇t+1                       ∂ct           ∂f t
that multiple contact points and/or other constraint impulses                      = I + M −1 t    −∆t          + J Tt                    (8)
can be trivially added to Equation 2.                                       ∂ q̇t                        ∂ q̇ t        ∂ q̇ t
                                                                                                                
                                                                           ∂ q̇t+1                         ∂f t
   Every term in Equation 2 can be evaluated given q t , q̇ t and                  = M −1t     ∆tI + J Tt                                 (9)
τ except for the contact impulse f , which requires the engine              ∂τt                            ∂τ t
                                                                                     ∂M −1
                                                                                                                                      
to form and solve an LCP:                                                  ∂ q̇t+1         t zt                    ∂ct            ∂f t
                                                                                   =             + M −1
                                                                                                      t        −∆t        + J Tt         (10)
                                                                             ∂µ          ∂µ                          ∂µ           ∂µ
         find f , vt+1
                                                                           We tackle the tricky intermediate Jacobians in sections
         such that f ≥ 0, vt+1 ≥ 0, f T vt+1 = 0.                 (3)    that follow. In Section IV we will introduce a novel sparse
analytical method to compute the gradients of contact force f t           Since we know the classification of each contact that forms the
with respect to q t , q̇ t , τt , µ. Section V will discuss ∂J∂q t —how
                                                                 t
                                                                          valid solution f ∗ , we rewrite the LCP constraints as follows:
collision geometry changes with respect to changes in position.                            ∗      ∗
                                     ∂q           ∂q                       find          f
                                                                                          C , f S , vC , v S
In Section VI we will tackle ∂qt+1 and ∂ q̇t+1 , which is not as
                                                                                                                ACS f ∗C
                                                                                                                      
                                         t            t                                   vC            ACC                   b
simple as it may at first appear, because naively taking gradients         such that               =                      + C (12)
                                                                                          vS            ASC     ASS f ∗S      bS
through a discrete time physics engine yields problematic
                                                                                         f ∗C > 0, f ∗S = 0, v C = 0, v S > 0.
results when elastic collisions take place. Additionally, the
appendix gives a way to apply the derivations from [25] and                   From here we can see how the valid solution f ∗ changes
                              ∂M −1 z      ∂ct
[7] to analytically find ∂qt t , ∂q            , and ∂∂cq̇t .             under infinitesimal perturbations  to A and b. Since f ∗S = 0
                                t       t          t

                IV. D IFFERENTIATING THE LCP                              and v C = 0, the LCP can be reduced to three conditions on
                                                                          f ∗C :
   This section introduces a method to analytically compute
 ∂f         ∂f
 ∂A and ∂b . It turns out that it is possible to efficiently                               0 = ACC f ∗C + bC                      (13)
get unambiguous gradients through an LCP in the vast                                         ∗
                                                                                           fC > 0                                 (14)
majority of practical scenarios, without recasting it as a QP                                      ∗
(which throws away sparsity information by replacing the                                   ASC f C + bS > 0.                      (15)
complementarity constraint with an objective function). To see
                                                                     We will show that these conditions will always be possible to
this, let us consider a hypothetical LCP problem parameterized
                                  ∗                               satisfy under small enough perturbations  in the neighborhood
by A, b with a solution f found during the forward pass:
                                                                  of a valid solution. Let us first consider tiny perturbations
fLCP (A, b) = f ∗ .
                                                                  to bS and ASC . If the perturbations are small enough, then
   For brevity, we only include the discussion on normal
                                                                  Equation 15 will still be satisfied with our original f ∗C , because
contact impulses in this section and leave the extension to
                                                                  we know Equation 15 already holds strictly such that there is
friction impulses in Appendix A. Therefore, each element in
  ∗                                                               some non-zero room to decrease any element of ASC f ∗C + bS
f ≥ 0 indicates the normal impulse of a point contact. By
                                                                  without violating Equation 15. Therefore,
complementarity, we know that if some element fi∗ > 0, then
             ∗
vi = (Af + b)i = 0. Intuitively, the relative velocity at                            ∂f ∗C              ∂f ∗C
contact point i must be 0 if there is any non-zero impulse                                  = 0 and           = 0.                (16)
                                                                                     ∂bS               ∂ASC
being exerted at contact point i. We call such contact points
“Clamping” because the impulse fi > 0 is adjusted to keep Next let us consider an infinitesimal perturbation ∗ to bC and
the relative velocity vi = 0. Let the set C to be all indices the necessary change on the clamping force ∆f C to satisfy
that are clamping. Symmetrically, if fj = 0, then the relative Equation 13:
velocity vj = (Af ∗ + b)j ≥ 0 is free to vary without the
                                                                                  0 = ACC (f ∗C + ∆f ∗C ) + bC + .               (17)
LCP needing to adjust fj to compensate. We call such contact
points “Separating” and define the set S to be all indices that      Setting ACC f ∗C + bC = 0 and assuming ACC is invertible,
are separating. Let us call indices j where fj = 0 and vj = 0 the change of the clamping force is given as ∆f ∗ = −A−1 .
                                                                                                                       C          CC
“Tied.” Define the set T to be all indices that are tied.         Since f ∗C is strictly greater than 0, it is always possible to
   If no contact points are tied (T = ∅), the LCP is strictly choose an  small enough to make f ∗ − A−1  > 0 and
                                                                                                              C      CC
differentiable and the gradients can be analytically computed. A (f ∗ + ∆f ∗ ) + b > 0 remain true. Therefore,
                                                                     SC   C        C       S
When some contact points are tied (T 6= ∅), the LCP has valid
subgradients and it is possible to follow any in an optimization.                            ∂f ∗C
                                                                                                    = −A−1
                                                                                                         CC .                     (18)
The tied case is analogous to the non-differentiable points                                  ∂bC
in a QP where an inequality constraint is active while the
                                                                     Note that ACC is not always invertible because A is positive
corresponding dual variable is also zero. In such a case,
                                                                  semidefinite. We will discuss the case when ACC is not full
computing gradients via taking differentials of the KKT
                                                                  rank in Section IV-C along with a method to stabilize the LCP
conditions will result in a low-rank linear system and thus
                                                                  when there exists multiple LCP solutions in Appendix B.
non-unique gradients [2].
                                                                     Lastly, we compute gradients with respect to ACC . In prac-
A. Strictly differentiable cases                                  tice, changes to ACC only happen because we are differentiating
   Consider the case where T = ∅. We shuffle the indices of with respect to parameters q or µ, which also changes bC . As
f ∗ , v, A and b to group together members of C and S. The such, we introduce a new scalar variable, x, which could
LCP becomes:                                                      represent any arbitrary scalar quantity that effects both A and
                    ∗     ∗                                       b. Equation 13 can be rewritten as:
  find            f   , f   ,
                   C  S C Sv , v
                                       ACS f ∗C
                                              
                   vC           ACC                   bC
  such that                =                       +                                  f ∗C = −ACC (x)−1 bC (x).                   (19)
                   vS           ASC    ASS f ∗S       bS (11)
                    ∗           ∗
                  f C ≥ 0, f S ≥ 0, v C ≥ 0, v S ≥ 0                 Because ACC (x) and bC (x) are continuous, and the original
                  f ∗T              ∗T
                    C v C = 0, f S v S = 0.                       solution is valid, any sufficiently small perturbation to x will
not reduce f ∗C below 0 or violate Equation 15. The Jacobian      where A+ CC is the pseudo inverse matrix of the low-rank A.
with respect to x can be expressed as:                            For numerical stability, we can solve a series of linear systems
                                                                  instead of explicitly evaluating ACC (x)+ .
        ∂f ∗C             ∂ACC (x)
              = ACC (x)−1          ACC (x)−1 bC (x)
         ∂x                 ∂x                                    D. Complementarity-aware gradients via contact constraints
                                          ∂bC (x)                   Sometimes analytically correct Jacobians through the LCP
                             +ACC (x)−1           .       (20)
                                            ∂x                   can actually prevent an optimizer from finding a good solution.
Using A = J M −1 J T and b = J (q̇t +∆tM −1 (τ −c)), along When a contact i is clamping (i ∈ C), we effectively impose
with the derivations of Featherstone presented in Appendix F, a constraint that the relative velocity at that contact point is
it is possible to compute ∂A           ∂bC
                              ∂x and ∂x for any specific x.
                                CC                               zero no matter how we push or pull on the contact. This
   Remark: Previous methods [10, 27, 34] cast an LCP to a prevents the gradients from pointing towards any motions that
QP and solved for a linear system of size n + m derived from require breaking contact, because our constraints will zero out
taking differentials of the KKT conditions of the QP, where n gradients that lead to v i > 0.
is the dimension of the state variable and m is the number of       This behavior is caused by the complementarity constraint
contact constraints. Our method also solves for linear systems requiring that at most one of vi or fi can be non-zero. This
to obtain A−1CC , but the size of ACC is often much less than m
                                                                 phenomenon grows out of the short-sightedness of the gradient
due to the sparsity of the solution (f ∗ , v ∗ ).                (it only considers an infinitely small neighborhood  around
                                                                 the current state). While it is true that small attempts to push
B. Subdifferentiable case                                        vi > 0 will result in no change to v as f compensates to keep
   Now let us consider when T =      6 ∅. Replacing the LCP vi = 0, eventually we will reach a discontinuity where f can no
constraints with linear constraints will no longer work because longer prevent the contact from separating. However, a gradient-
any perturbation will immediately change the state of the based optimizer may never take steps in that direction because
contact and the change also depends on the direction of gradients in that direction are 0. In this section we propose a
perturbation. Including the class of “tied” contact points to heuristic to opportunistically explore “projecting forward” to
Equation 11, we need to satisfy an additional linear system,     the discontinuity where the complementarity constraint flips
                                                                 during backpropagation, depending on the gradient of loss
           vT = AT T fT∗ + AT C fC∗ + AT S fS∗ + bT              function with respect to v and ∂v ∂`
                                                                                                      .
                          ∗
               = AT T fT + b̃T ,                            (21)    To make it more concrete, let us consider a simple example
                                                                 of a 2D circle attached to a linear actuator that can produce
where b̃T = AT C fC∗ + bT and vT and fT∗ are both zero force along the vertical axis (Figure 3). Our goal is to lift the
at the solution. Let i ∈ T be the index of a tied contact circle up to a target height above the ground by generating
point. Consider perturbing the i’th element of b̃T by . If an upward velocity using the linear actuator. When the circle
 > 0, AT T fT∗ cannot become negative to balance Equation is resting on the ground under gravity, the contact point with
21 because AT T is positive semidefinite and fT∗ must be the ground is classified as “clamping”. This means that any
nonnegative. Therefore, vT i must become positive, resulting tiny perturbation in the control force of linear actuator will be
contact point i being separated and fT∗ i remaining zero. If met with an exactly offsetting contact force to ensure that the
 < 0, then i is immediately bumped into the “clamping” relative velocity between the circle and the ground remains
set C because vT i cannot be negative. Therefore, fT∗ i must zero. As such, no matter what gradient of loss function with
become positive to balance Equation 21. The gradients for respect to the control force we try to backpropagate through
the clamping and separating cases are both valid subgraidents the contact, we will always get ∂l = 0.
                                                                                                    ∂τ
for a tied contact point. In an optimization, we can choose
either of the two subgradients at random without impacting
the convergence [6]. In practice, encountering elements in T
is quite rare for practical numerical reasons.
C. When ACC is not full rank
   When ACC is not full rank, the solution to fLCP (A, b) = f ∗
is no longer unique. Nevertheless, once a solution is computed
                                                                  Fig. 3. Increasing force from the linear actuator (τ ) is met by an equal
using any algorithm and the clamping set C is found, we can       and opposite decrease in ground reaction force f , resulting in no change in
use the stabilization method proposed in Appendix B to find       velocity and thus no gain in height. Gradients of loss function will be zeroed
the least-squares minimal f ∗ that solves the LCP. The gradient   out by ∂τ∂v
                                                                               = 0 when backpropgating through the contact. In contrast, if
                                                                  the contact is classified as “separating”, the gradient will increase the linear
of clamping forces can then be written as:                        actuator, resulting in an upward force v.
           ∂f ∗C       ∂ACC −1             ∂bC
                 = A−1
                    CC        ACC bC + A−1
                                        CC
            ∂x           ∂x                ∂x                        Consider another example where the same 2D circle is
                                  T 
                               ∂A CC                              uncontrolled and resting on a linearly actuated platform (Figure
             +(I − A+ CC ACC )        A+T   +
                                       CC ACC ,           (22)
                                ∂x                                4). To lift the circle up, we need to utilize the contact force
from the platform. If the initialization of the problem results in                        and put them into “clamping” to impose the constraint
the contact point being classified as “separating”, no constraint                         that vi = 0.
force will be applied on the contact point, as if the contact did                                                                         || ∂` ||2
                                                                                       The contact strategy with the larger || ∂∂`       2
                                                                                                                                  q̇ t ||2 +
                                                                                                                                             ∂τt 2
                                                                                                                                              ∆t   is
not exist. Therefore, the gradient of contact force with respect                    used during backpropagation for learning. We call the gradient
to the platform control force is zero, which may cause the                          produced by this exploratory procedure a “Complementarity-
optimization to be trapped in a saddle point.                                       aware Gradient,” and find empirically that it can help avoid
                                                                                    saddle points during trajectory optimization. We show an
                                                                                    example of this in Section VII.
                                                                                       The complementarity-aware gradients do not guarantee to
                                                                                    improve global convergence because the gradient is chosen for
                                                                                    each contact point independently, which might not result in
                                                                                                             ∂`
                                                                                    an aggregated gradient ∂τ   that moves in a globally optimal
                                                                                    direction. However, if an optimization problem currently gets
Fig. 4. If the initial contact state is “separating”, the platform cannot apply     stuck in a saddle point, complementarity-aware gradients
contact force to the circle, resulting in zero gradient of the contact force with   provide another tool for practitioners to try.
                                               ∂f
respect to the control force of the platform, ∂τ   = 0. However, if the contact
is classified as “clamping”, we can utilize the contact force from the platform          V. G RADIENTS THROUGH COLLISION GEOMETRY
to push the circle upwards by increasing the control force of the platform.                                                               ∂J T f
                                                                                       This section addresses efficient computation of ∂qt , the
                                                                                                                                               t
                                                                                    relationship between position and joint impulse. In theory, we
   In both examples, the issues can be resolved by classifying                      could utilize auto-diff libraries for the derivative computation.
the contact point differently. If we know that to solve this                        However, using auto-diff and passing every gradient through
problem we need to actuate the circle and the platform                              a long kinematic chain of transformations is inefficient for
separately, we would set the contact point to be “separating.”                      complex articulated rigid body systems. In contrast, computing
This gives the optimizer a chance to explore a solution with                        the gradients symbolically shortcuts much computation by
contact breaking. On the other hand, if we know that we need                        operating directly in the world coordinate frame.
to exploit the contact force between the circle and the platform,                      Let Ai ∈ se(3) be the screw axis for the i’th DOF, expressed
we would relabel a separating contact point to be “clamping”.                       in the world frame. Let the k’th contact point give an impulse
This lets the optimizer search for the most effective contact                       Fk ∈ dse(3), also expressed in the world frame. Let ψi,k ∈
force that reduces the loss function.                                               {−1, 0, 1} be the relationship between contact k and joint i.
   Is there a way to know which strategy to use in advance?                         ψi,k = 1 or ψi,k = −1 means contact k is on a child body of
In the general case, the answer seems to be no, but we can do                       joint i. Otherwise, ψi,k = 0. The total joint impulse caused by
better than naive gradients which stick with whatever contact                       contact impulses for the i’th joint is given by:
classification they were initialized into and do not explore to                                            X                    X
break out of resulting saddle points. We propose a heuristic to                               (J Tt f )i =    ψi,k ATi Fk = ATi      ψi,k Fk .   (23)
explore more broadly at a constant additional cost.                                                      k                      k
   We propose that always picking the contact strategy that                           Taking the derivative of Equation 23 gives
                                              ∂`   2
                                       || ∂τ ||2
results in the largest || ∂∂`      2
                            q̇ t ||2 +      is a good heuristic
                                            t
                                           ∆t                                          ∂(J Tt f )i   ∂Ai T X               X      ∂Fk
during learning for avoiding saddle points. While we could try                                     =         ψi,k Fk + ATi   ψi,k      .           (24)
                                                                                         ∂q t        ∂q t                         ∂q t
backprop through all O(2n ) possible strategies and pick the                                                 k                 k
best one, that gets expensive as the number of contacts becomes                       Evaluating ∂A                                             ∂Fk
                                                                                                    ∂q t is straightforward, but computing ∂qt
                                                                                                       i

larger than a small handful. Instead of exhaustively searching                                                                                3
                                                                                    requires understanding how the contact normal nk ∈ R and
for all possible combinations of contact states with exponential
                                                                                    contact position pk ∈ R3 change with changes in q t .
complexity, we propose to only check two classifications:
                                                                                      Let Fk be a concatenation of torque and force in dse(3).
   1) First, check the “correct” contact classification solved by                   The derivative with respect to the current joint position q t is:
      the LCP.                                                                                             "                       #
                             ∂`                                                                              ∂nk               ∂pk
                                                                                                             ∂q t × pk + nk × ∂q t
   2) Second, we compute ∂v     (the gradient of loss with respect                                 ∂Fk
      to relative contact velocity), and use the elements of                                             =            ∂nk                       (25)
                                                                                                   ∂q t                ∂q
       ∂`                                                                                                                t
      ∂v to compute the “clamping” and “separating” sets as
      follows. Take any indices i that are trying to increase the                     It turns out that computing ∂n
                                                                                                                  ∂qt
                                                                                                                     k
                                                                                                                       for curved primitives shape
                                         ∂`
      relative velocity at that contact ∂v i
                                             < 0, which implies                     colliders (spheres and capsules) requires different treatment
      the optimizer is feebly trying to separate the objects,                       from meshes or polygonal primitives. To understand why,
      and put those indices into “separating” to remove the                         consider using a high polycount mesh to approximate a true
                                                          ∂`
      constraint that vi = 0. Take any indices i where ∂v   i
                                                              > 0,                  sphere as shown in Figure 5.
      which implies the optimizer is trying to move the objects                        On a mesh approximation of a sphere, infinitesimally moving
      closer together (which would violate contact constraints),                    the contact point pk by  (by perturbing q of the triangle) will
Fig. 5. ∂n
         ∂q
           k
             can be set to zero for mesh or polygonal geometry, but has to   Fig. 6. Discrete-time Jacobians do not adequately describe the dynamics of
be computed analytically for curved geometry.                                an elastic collision. In the system pictured here, letting q be a scalar giving
                                                                             the distance from the ground, discrete-time would lead us to falsely believe
                                                                                  ∂q t+1                                                       ∂q t+1
                                                                             that ∂q       = 1. In continuous time, we would instead expect ∂q        = −σ,
                                                                             where σ is the coefficient of restitution. Modeling this requires understanding
                                                                             how the time of collision changes with initial conditions, and how that affects
not cause the normal of the contact face nk to change at all,                the final state after the step.
because we remain on the same face of the mesh. So ∂n     ∂q is
                                                            k


always zero for a mesh or polygonal shape. However, on a                                                  TABLE II
true sphere, an infinitesimal perturbation of the contact point                            B ENCHMARKS AGAINST F INITE D IFFERENCING
with the sphere (no matter how small) will cause the contact
normal with the sphere nk to change. The way the contact
                                                                               E NVIRONMENT           A NALYTICAL          C ENTRAL           S PEEDUP
normal nk changes with position (e.g. ∂n   ∂q ) is often crucial
                                              k
                                                                                                                         D IFFERENCES
information for the optimizer to have in order to solve complex
problems, and mesh approximations to curved surfaces falsely                   ATLAS                     16.1 MS             737 MS            45.8 X
                                                                               H ALF C HEETAH           0.870 MS             7.52 MS           8.64 X
set ∂n
     ∂q = 0.
       k
                                                                               J UMP -W ORM             0.484 MS             3.08 MS           6.36 X
   We refer the interested reader to Appendix C for a discussion               C ATAPULT                0.576 MS             3.69 MS           6.40 X
                                 ∂pk
of how we compute ∂n   ∂q t and ∂q t for different combinations
                          k


of collider types.
                                                                             (∆t − ci )σv t,i . From there we have:
       VI. G RADIENTS THROUGH ELASTIC CONTACTS                                              ∂pi,t+1                 ∂pi,t+1
                                                                                                    = −σi ,                 = −σi ∆t.(26)
   DiffTaichi [18] pointed out an interesting problem that arises                            ∂pi,t                   ∂v i,t
from discretization of time in simulating elastic bouncing              After finding the above gradients for each collision indepen-
phenomenon between two objects. The problems arise from dently, we need to find a pair of Jacobians, ∂qt+1 and ∂qt+1 ,
                                                                                                                       ∂q t         ∂ q̇ t
the discrete time integration of position: q t+1 = q t + ∆tq̇ t . that approximate our desired behavior at each of            the contact
                  ∂q t+1            ∂q t+1
The Jacobians ∂q = I and ∂ q̇ = ∆tI are correct for points as closely as possible.
                      t                 t
most scenarios. However, when an elastic collision occurs,
the discrete time integration scheme creates problems for                   ∂pi,t+1     ∂pi,t+1 ∂q t+1 ∂q t
differentiation. In a discrete time world, the closer the object                     =
                                                                              ∂pi,t      ∂q t+1 ∂q t ∂pi,t
is to the collision site at the beginning of the time step when
                                                                                                ∂q
collision happens, the closer to the collision site it ends up                       = J i,t+1 t+1 J −1    , for i = 1 · · · m       (27)
at the end of that time step. In continuous time, however, the                                    ∂q t i,t
closer the object begins to its collision site, the further away where J i,t+1 is the Jacobian matrix of contact i, J −1 is the
                                                                                                                                i,t
it ends up, because the object changes velocity sooner (Figure pseudo inverse Jacobian, and m is the total number of contact
6).                                                                                                             ∂q
                                                                      points. Our goal is to find a Jacobian ∂qt+1 that satisfies the
   DiffTaichi [18] proposed using continuous-time collision above equations (Equation 27) as closely tas possible (details
detection and resolution during training, but noted that switch- in Appendix E). Once we find a satisfactory approximation for
ing to discrete-time at test time did not harm performance. ∂qt+1 , we can get
                                                                       ∂q t
Since introducing full continuous-time collision detection is
computationally costly for complex dynamic systems and                                      ∂q t+1       ∂q
                                           ∂q           ∂q                                          = ∆t t+1 .                       (28)
scenes, we instead opt to find a ∂qt+1 and ∂ q̇t+1 that                                      ∂ q̇ t        ∂q t
                                              t             t
approximates the behavior of continuous-time Jacobians when
elastic collisions occur.                                                                   VII. E VALUATION
   Let pt,i be the relative distance at contact i at time t and v t,i   First, we evaluate our methods by testing the performance of
be the relative velocity. We further define σi as the coefficient gradient computation. In addition, we compare gradient-based
of restitution at contact i and t + ci as the time of collision trajectory optimization enabled by our method to gradient-
of contact i, where ci ∈ R. Assuming the relative velocity is free stochastic optimization, and discuss implications. We also
constant in this time step, we get ci = −pi /v i and pt+1,i = demonstrate the effectiveness of the complementarity-aware
gradients in a trajectory optimization problem. Finally, we show                 C. Complementarity-aware gradients
that our physics engine can solve optimal control problems for      To highlight the complementarity-aware gradients, we solve
complex dynamic systems with contact and collision, including    a trajectory optimization problem of a drone taking-off from
an Atlas humanoid jumping in the air.                            the ground and reaching a fixed height in 500 timesteps.
A. Performance                                                      Because the drone is initialized resting on the ground, it
                                                                 has a contact with the ground that is classified as “clamping.”
   Controlled comparison to existing methods can be chal-
                                                                 When we attempt to optimize the control on the drone using
lenging because they use different formulations for forward
                                                                 correct gradients, we get zero gradients and make no progress.
simulation, essentially simulating different physical phenomena.
                                                                 By contrast, when we use our complementarity aware gradient,
We therefore benchmark the performance of our method at the
                                                                 while we still see no change in loss for the first few iterations
atomic level–measuring the computation time of a Jacobian for
                                                                 of SGD, we’re able to get non-zero gradients and escape the
a single time step using a single-core CPU and comparing
                                                                 saddle point (Figure 7). See the supplementary video for the
it to finite differencing methods, using the same forward
                                                                 resulting drone trajectories.
simulation process provided by an existing non-differentiable
physics engine (DART). This comparison removes factors due
to differences in forward simulation, implementation techniques,
and computation resources, and focuses on the speed gain solely
contributed by our gradient computation method.
   Table II contains abbreviated benchmark performance of our
Jacobians against central differencing. We evaluate our results
in four environments: the Atlas robot on the ground (33 DOFs,
12 contact points), Half Cheetah on the ground (9 DOFs, 2
contact points), Jump-Worm (5 DOFs, 2 contact points), and
Catapult (5 DOFs, 2 contact points). For each environment, we
compare the speed of evaluating all five primary Jacobians. For
a complete table, including the speed of individual Jacobian
evaluations, see Appendix D.
                                                                                 Fig. 8. Training a drone to lift off the ground and fly to a target height after
B. Gradient-based vs gradient-free trajectory optimization                       500 timesteps. Loss is the squared distance of the drone from the target at
                                                                                 t = 500. The drone is initialized resting on the ground, which means the
   To demonstrate the benefit of analytical Jacobians of dynam-                  drone-ground contacts are classified as “clamping.” That means Jacobians will
ics, we compare trajectory optimization on our catapult trajec-                         ∂ q̇
                                                                                 show ∂τt+1 = 0. While both standard and complementarity-aware training
                                                                                             t
tory problem between Multiple Shooting and Stochastic Search                     runs start in a saddle point, the complementarity-aware gradients are able to
(SS) [5], as well as cartpole and the double-pendulum using                      guide SGD to escape after several iterations of learning.
both Differential Dynamic Programming (DDP) [39, 22, 40]
and Stochastic Search [5]. The gradient-based methods (DDP
and Multiple Shooting) are able to converge much more quickly,                   D. Optimal control with contact
because the additional convergence gained from analytical                           We present several trajectory optimization problems that
Jacobians more than offsets the time to compute them. See                        involve complex contact dynamics, optimized using multiple
Figure VII-B.                                                                    shooting. We demonstrate “Catapult”, which is a 3-dof robot
                                                                                 that is tasked with batting a free ball towards a target, in such
                                                                                 a way that it exactly hits the target at the desired timestep
                                                                                 (pictured in Figure 7). We also demonstrate “Jump-Worm”,
                                                                                 which is a 5-dof worm-shaped robot that is attempting to jump
                                                                                 as high as possible at the end of the trajectory. Both of these
                                                                                 problems involve complex contact switching throughout the
                                                                                 course of the trajectory. We also optimize a trajectory where
                                                                                 the “Atlas” robot learns to jump. See the supplementary video
                                                                                 for the resulting trajectories.

                                                                                                          VIII. C ONCLUSIONS
                                                                                    We present a fast and feature-complete differentiable physics
                                                                                 engine for articulated rigid body simulation. We introduce
Fig. 7. Comparing wall clock time to find a single-pendulum cartpole (CP),       a method to compute analytical gradients through the LCP
double-pendulum cartpole (DCP), and catapult (CTPLT) trajectory, using DDP       formulation of inelastic contact by exploiting the sparsity of the
(D), SS (S), and Multiple Shooting (M). The results are unsurprising: gradient
information speeds convergence tremendously.
                                                                                 LCP solution. Our engine supports complex contact geometry
                                                                                 and approximating continuous-time elastic collision. We also
                                                                                [4] Peter Battaglia, Razvan Pascanu, Matthew Lai,
                                                                                    Danilo Jimenez Rezende, et al. Interaction networks
                                                                                    for learning about objects, relations and physics. In
                                                                                    Advances in neural information processing systems,
                                                                                    pages 4502–4510, 2016.
                                                                                [5] George I Boutselis, Ziyi Wang, and Evangelos A
                                                                                    Theodorou. Constrained sampling-based trajectory opti-
                                                                                    mization using stochastic approximation. In 2020 IEEE
                                                                                    International Conference on Robotics and Automation
                                                                                    (ICRA), pages 2522–2528. IEEE, 2020.
Fig. 9. A few snapshots of the trajectory that an Atlas robot learns when it    [6] Stephen Boyd, Lin Xiao, and Almir Mutapcic. Subgradi-
is asked to jump up towards the green markers, starting from a crouch.              ent methods. lecture notes of EE392o, Stanford University,
                                                                                    Autumn Quarter, 2004:2004–2005, 2003.
                                                                                [7] Justin Carpentier and Nicolas Mansard. Analytical deriva-
introduce a novel method to compute complementarity-aware                           tives of rigid body dynamics algorithms. In Robotics:
gradients that help optimizers to avoid stalling in saddle points.                  Science and Systems (RSS 2018), 2018.
   There a few limitations of our current method. Currently,                    [8] Michael B Chang, Tomer Ullman, Antonio Torralba, and
computing ∂J    tf
              ∂q t , the way the joint torques produced by the
                                                                                    Joshua B Tenenbaum. A compositional object-based
contact forces change as we vary joint positions (which in turn                     approach to learning physical dynamics. arXiv preprint
varies contact positions and normals) takes a large portion of                      arXiv:1612.00341, 2016.
the total time to compute all Jacobians of dynamics for a given                 [9] Erwin Coumans. Bullet physics engine. Open Source
timestep. Perhaps a more efficient formulation can be found.                        Software: http://bulletphysics. org, 1(3):84, 2010.
   Our engine also doesn’t yet differentiate through the ge-                   [10] Filipe de Avila Belbute-Peres, Kevin Smith, Kelsey
ometric properties (like link length) of a robot, or friction                       Allen, Josh Tenenbaum, and J Zico Kolter. End-to-
coefficients. Extending to these parameters is an important step                    end differentiable physics for learning and control. In
to enable parameter estimation applications.                                        Advances in Neural Information Processing Systems,
   We are excited about future work that integrates gradients                       pages 7178–7189, 2018.
and stochastic methods to solve hard optimization problems in                  [11] Jonas Degrave, Michiel Hermans, Joni Dambre, and
robotics. In running the experiments for this paper, we found                       Francis Wyffels. A differentiable physics engine for deep
that stochastic trajectory optimization methods could often                         learning in robotics. Frontiers in neurorobotics, 13:6,
find better solutions to complex problems than gradient-based                       2019.
methods, because they were able to escape from local optima.                   [12] Moritz Geilinger, David Hahn, Jonas Zehnder, Moritz
However, stochastic methods are notoriously sample inefficient,                     Bächer, Bernhard Thomaszewski, and Stelian Coros.
and have trouble fine-tuning results as they begin to approach a                    Add: analytically differentiable dynamics for multi-body
local optima. The authors speculate that there are many useful                      systems with frictional contact. ACM Transactions on
undiscovered techniques waiting to be invented that lie at the                      Graphics (TOG), 39(6):1–15, 2020.
intersection of stochastic gradient-free methods and iterative                 [13] David Hahn, Pol Banzet, James M. Bern, and Stelian
gradient-based methods. It is our hope that an engine like the                      Coros. Real2sim: Visco-elastic parameter estimation from
one presented in this paper will enable such research.                              dynamic motion. ACM Trans. Graph., 38(6), November
                                                                                    2019.
                        ACKNOWLEDGMENTS
                                                                               [14] Eric Heiden, David Millard, Hejia Zhang, and Gaurav S
                           R EFERENCES                                              Sukhatme. Interactive differentiable simulation. arXiv
 [1] Rami Al-Rfou, Guillaume Alain, Amjad Almahairi,                                preprint arXiv:1905.10706, 2019.
     Christof Angermueller, Dzmitry Bahdanau, Nicolas Ballas,                  [15] Eric Heiden, David Millard, Erwin Coumans, and Gau-
     Frédéric Bastien, Justin Bayer, Anatoly Belikov, Alexan-                     rav S Sukhatme. Augmenting differentiable simulators
     der Belopolsky, et al. Theano: A python framework for                          with neural networks. arXiv preprint arXiv:2007.06045,
     fast computation of mathematical expressions. arXiv e-                         2020.
     prints, pages arXiv–1605, 2016.                                           [16] Michiel Hermans, Benjamin Schrauwen, Peter Bienstman,
 [2] Brandon Amos and J Zico Kolter. Optnet: Differentiable                         and Joni Dambre. Automated design of complex dynamic
     optimization as a layer in neural networks. In Proceed-                        systems. PLOS ONE, 9(1):1–11, 01 2014.
     ings of the 34th International Conference on Machine                      [17] Philipp Holl, Nils Thuerey, and Vladlen Koltun. Learning
     Learning-Volume 70, pages 136–145. JMLR. org, 2017.                            to control pdes with differentiable physics. In Interna-
 [3] David Baraff. Fast contact force computation for non-                          tional Conference on Learning Representations, 2020.
     penetrating rigid bodies. In Proceedings of the 21st                      [18] Yuanming Hu, Luke Anderson, Tzu-Mao Li, Qi Sun,
     annual conference on Computer graphics and interactive                         Nathan Carr, Jonathan Ragan-Kelley, and Frédo Durand.
     techniques, pages 23–34, 1994.                                                 Difftaichi: Differentiable programming for physical simu-
     lation. arXiv preprint arXiv:1910.00935, 2019.                  differentiation in pytorch. 2017.
[19] Yuanming Hu, Tzu-Mao Li, Luke Anderson, Jonathan           [32] Jovan Popović, Steven M. Seitz, Michael Erdmann, Zoran
     Ragan-Kelley, and Frédo Durand. Taichi: a language for         Popović, and Andrew Witkin. Interactive manipulation
     high-performance computation on spatially sparse data           of rigid body simulations. In Proceedings of the 27th
     structures. ACM Transactions on Graphics (TOG), 38(6):          Annual Conference on Computer Graphics and Interac-
     1–16, 2019.                                                     tive Techniques, SIGGRAPH ’00, page 209–217. ACM
[20] Yuanming Hu, Jiancheng Liu, Andrew Spielberg,                   Press/Addison-Wesley Publishing Co., 2000.
     Joshua B Tenenbaum, William T Freeman, Jiajun Wu,          [33] William H. Press, Saul A. Teukolsky, William T. Vet-
     Daniela Rus, and Wojciech Matusik. Chainqueen:                  terling, and Brian P. Flannery. Numerical Recipes 3rd
     A real-time differentiable physical simulator for soft          Edition: The Art of Scientific Computing. Cambridge
     robotics. Proceedings of IEEE International Conference          University Press, USA, 3 edition, 2007.
     on Robotics and Automation (ICRA), 2019.                   [34] Yi-Ling Qiao, Junbang Liang, Vladlen Koltun, and
[21] A. Iollo, M. Ferlauto, and L. Zannetti. An aerodynamic          Ming C. Lin. Scalable differentiable physics for learning
     optimization method based on the inverse problem adjoint        and control. In ICML, 2020.
     equations. Journal of Computational Physics, 173(1):87–    [35] Christopher Rackauckas, Yingbo Ma, Vaibhav Dixit,
     115, 2001.                                                      Xingjian Guo, Mike Innes, Jarrett Revels, Joakim Nyberg,
[22] David H Jacobson and David Q Mayne. Differential                and Vijay Ivaturi. A comparison of automatic differentia-
     dynamic programming. 1970.                                      tion and continuous sensitivity analysis for derivatives of
[23] Y. Jarny, M.N. Ozisik, and J.P. Bardon. A general               differential equation solutions, 2018.
     optimization method using adjoint equation for solving     [36] C.J.F. Ridders. Accurate computation of f’(x) and f’(x)
     multidimensional inverse heat conduction. International         f”(x). Advances in Engineering Software (1978), 4(2):
     Journal of Heat and Mass Transfer, 34(11):2911–2919,            75–76, 1982.
     1991.                                                      [37] Connor Schenck and Dieter Fox. Spnets: Differentiable
[24] Franck Jourdan, Pierre Alart, and Michel Jean. A                fluid dynamics for deep neural networks. In Proceedings
     gauss-seidel like algorithm to solve frictional contact         of The 2nd Conference on Robot Learning, volume 87
     problems. Computer Methods in Applied Mechanics and             of Proceedings of Machine Learning Research, pages
     Engineering, 155(1):31–47, 1998.                                317–335. PMLR, 29–31 Oct 2018.
[25] Junggon Kim. Lie group formulation of articulated          [38] Changkyu Song and Abdeslam Boularias. Learning
     rigid body dynamics. Technical report, Technical Report.        to slide unknown objects with differentiable physics
     Carnegie Mellon University, 2012.                               simulations. In Robotics: Science and Systems, Oregon
[26] Jeongseok Lee, Michael X Grey, Sehoon Ha, Tobias Kunz,          State University at Corvallis, Oregon, USA, 14–16 July
     Sumit Jain, Yuting Ye, Siddhartha S Srinivasa, Mike             2020.
     Stilman, and C Karen Liu. Dart: Dynamic animation          [39] Yuval Tassa, Tom Erez, and Emanuel Todorov. Synthesis
     and robotics toolkit. Journal of Open Source Software, 3        and stabilization of complex behaviors through online
     (22):500, 2018.                                                 trajectory optimization. In 2012 IEEE/RSJ International
[27] Junbang Liang, Ming Lin, and Vladlen Koltun. Dif-               Conference on Intelligent Robots and Systems, pages 4906–
     ferentiable cloth simulation for inverse problems. In           4913. IEEE, 2012.
     H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alché-    [40] Emanuel Todorov and Weiwei Li. A generalized iterative
     Buc, E. Fox, and R. Garnett, editors, Advances in Neural        lqg method for locally-optimal feedback control of
     Information Processing Systems, volume 32. Curran               constrained nonlinear stochastic systems. In Proceedings
     Associates, Inc., 2019.                                         of the 2005, American Control Conference, 2005., pages
[28] Antoine McNamara, Adrien Treuille, Zoran Popović, and          300–306. IEEE, 2005.
     Jos Stam. Fluid control using the adjoint method. ACM      [41] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco:
     Trans. Graph., 23(3):449–456, August 2004.                      A physics engine for model-based control. In 2012
[29] David Millard, Eric Heiden, Shubham Agrawal, and                IEEE/RSJ International Conference on Intelligent Robots
     Gaurav S. Sukhatme. Automatic differentiation and               and Systems, pages 5026–5033. IEEE, 2012.
     continuous sensitivity analysis of rigid body dynamics,    [42] Marc Toussaint, Kelsey R. Allen, K. Smith, and J. Tenen-
     2020.                                                           baum. Differentiable physics and stable modes for tool-
[30] Damian Mrowca, Chengxu Zhuang, Elias Wang, Nick                 use and manipulation planning. In Robotics: Science and
     Haber, Li F Fei-Fei, Josh Tenenbaum, and Daniel L               Systems, 2018.
     Yamins. Flexible neural representation for physics
     prediction. In Advances in neural information processing
     systems, pages 8799–8810, 2018.
[31] Adam Paszke, Sam Gross, Soumith Chintala, Gregory
     Chanan, Edward Yang, Zachary DeVito, Zeming Lin, Al-
     ban Desmaison, Luca Antiga, and Adam Lerer. Automatic
                           A PPENDIX                                  B. LCP stabilization
A. Frictional impulse                                                    When ACC is not full rank, the solution to fLCP (A, b) = f ∗
                                                                      is no longer unique. To grasp this intuitively, consider a 2D
   In DART, friction impulses are solved by the boxed LCP             case where a box of unit mass that cannot rotate is resting
method, using the same implementation of the boxed variant of         on a plane. The box has two contact points, with identical
the Dantzig algorithm found in the Open Dynamics Engine, and          contact normals, and because the box is not allowed to rotate,
originally proposed in [3]. Boxed LCPs are not theoretically          the effect of an impulse at each contact point is exactly the
guaranteed to be solvable, but are quite common in practice           same (it causes the box’s upward velocity to increase). This
because of their speed and high-quality results. We therefore         means that both columns of A (one per contact) are identical.
extend our formulation in Section IV to compute the gradient          That means that ACC ∈ R2×2 is actually only rank one. Let’s
of frictional impulse magnitudes found in a boxed LCP solver          assume we need a total upward impulse of −mg to prevent
with respect to A and b. Similar to normal impulses, each             the box from interpenetrating the floor. Because ACC is a low
frictional impulse is classified into one of the two states:          rank, we’re left with one equation and two unknowns:
      a) Clamping (C): If the relative velocity along the fric-
tional impulse direction is zero, and friction impulse magnitude                       
                                                                                        1     1
                                                                                                   ∗   ∗
                                                                                                    fC1    fC1 + fC∗2
                                                                                                                       
                                                                                                                         −mg
                                                                                                                             
is below its bound, then any attempt to push this contact will            ACC f ∗C =                     = ∗           =
                                                                                        1     1     fC∗2   fC1 + fC∗2    −mg
be met with an increase in frictional impulse holding the point
in place. This means the contact point is clamping, which                It is easy to see that this is just fC∗1 + fC∗2 = −mg. And that
behaves will be treated in the same way as clamped normal             means that we have an infinite number of valid solutions to
forces.                                                               the LCP.
      b) Bounded (B): If the frictional impulse magnitude is at          In order to have valid gradients, our LCP needs to have
its bound (either positive or negative) then the contact point is     predictable behavior when faced with multiple valid solutions.
sliding or about to slide along this friction direction. Bounded      Thankfully, our analysis in the previous sections suggests a
frictional impulse B is quite like “Separating” S in normal           quite simple and efficient (and to the authors’ knowledge novel)
impulse. The difference is that frictional impulses in B are          LCP stabilization method. Once an initial solution is computed
not zero but at a non-zero bound based on the corresponding           using any algorithm, and the clamping set C is found, we
normal impulses.                                                      can produce a least-squares-minimal (and numerically exact)
   Bounded frictional impulse can be expressed by f ∗B = Ef ∗C ,      solution to the LCP by setting:
where each row of E ∈ R|B|×|C| contains a single non-zero
value with the friction coefficient, µs , for the corresponding                         f ∗C = A−1
                                                                                                CC bC ,       f ∗S = 0
normal impulse index in C.                                                This is possible with a single matrix inversion because the
   We define J C to be the matrix with just the columns of            hard part of the LCP problem (determining which indices
J corresponding to the indices in C. Likewise, we define J B          belong in which classes) was already solved for us by the main
containing just the columns of J that are bounded. If we              solver. Once we know which indices belong in which classes,
multiply J TC f C we get the joint torques due to the clamping        solving the LCP exactly reduces to simple linear algebra.
constraint forces. Similarly, if we multiply J TB f B we get the          As an interesting aside, this “LCP stabilization” method
joint torques due to bounded friction impulses. Since f B =           doubles as an extremely efficient LCP solver for iterative LCP
Ef C , we can modify ACC to take bounded frictional impulses          problems. In practical physics engines, most contact points
into account:                                                         do not change from clamping (C) to separating (S) or back
                                                                      again on most time steps. With that intuition in mind, we can
                 ACC = J C M −1 (J TC + J TB E)                       opportunistically attempt to solve a new fLCP (At+1 , bt+1 ) =
                                                                      f ∗t+1 at a new timestep by simply guessing that the contacts
   With this one small change, all the formulation in Section IV
                                                                      will sort into C and S in exactly the same way they did on the
works with frictional forces. An interesting observation is that
                                                                      last time step. Then we can solve our stabilization equations
the bounded frictional cases are analogous to the separating
                                                                      for f ∗t+1 as follows:
cases for the normal forces, in that the force value is constrained
at µs fi (or −µs fi ), where fi is the corresponding normal force
                                                                                f t+1 ∗C = At+1 −1
                                                                                                CC bt+1 C ,      f t+1 ∗S = 0
for the same contact. The only way the bounded force values
will change is through the change of corresponding clamping              If we guessed correctly, which we can verify in negligible
normal force, which needs to be accounted for when computing          time, then f ∗t+1 is a valid, stable, and perfectly numerically
the gradients.                                                        exact solution to the LCP. When that happens, and in our
   Just like the overall boxed LCP problem is not solvable, ACC       experiments this heuristic is right > 95% of the time, we can
is no longer guaranteed to be exactly invertible. In order to         skip the expensive call to our LCP solver entirely. As an added
support this, we need to use the pseudoinverse of ACC during          bonus, because C is usually not all indices, inverting At+1 CC
the forward pass, and the gradient of the pseudoinverse when          can be considerably cheaper than inverting all of At+1 , which
computing Jacobians.                                                  can be necessary in an algorithm to solve the full LCP.
                                                             TABLE III
                                           F ULL B ENCHMARKS AGAINST F INITE D IFFERENCING


           E NVIRONMENT        JACOBIAN     A NALYTICAL     C ENTRAL D IFFERENCES      S PEEDUP    R IDDERS    S PEEDUP
                                                T IME               T IME                            T IME
           ATLAS                  A LL         8.53 MS               749 MS              87.84 X   2229 MS      261 X
                                 ∂qt+1
                                   ∂qt
                                             0.0204 MS               160 MS              7850 X     581 MS     28480 X
                                 ∂ q̇t+1
                                   ∂qt
                                               6.75 MS               161 MS               23.8 X    581 MS      86 X
                                 ∂qt+1
                                   ∂ q̇t
                                              0.016 MS              107.2 MS            6570.9 X    304 MS     19000 X
                                 ∂ q̇t+1
                                   ∂ q̇t
                                              0.778 MS               160 MS              205.7 X    487 MS      626 X
                                 ∂ q̇t+1
                                   ∂τt
                                              0.981 MS               161 MS              163.9 X    524 MS      471 X
           H ALF C HEETAH         A LL        0.395 MS              8.64 MS             21.86 X      24 MS        60 X
                                 ∂qt+1
                                   ∂qt
                                             0.0059 MS              1.69 MS              284 X      3.17 MS      537 X
                                 ∂ q̇t+1
                                   ∂qt
                                              0.254 MS              1.874 MS             7.35 X     7.92 MS      31.1 X
                                 ∂qt+1
                                   ∂ q̇t
                                             0.00358 MS             1.228 MS             342 X      2.42 MS     675.9 X
                                 ∂ q̇t+1
                                   ∂ q̇t
                                              0.053 MS              1.98 MS              37.1 X     5.63 MS     106.2 X
                                 ∂ q̇t+1
                                   ∂τt
                                              0.077 MS              1.87 MS              24.1 X     5.75 MS      74.6 X
           J UMP -W ORM           A LL        0.256 MS              3.82 MS             14.89 X    9.727 MS      37.9 X
                                 ∂qt+1
                                   ∂qt
                                             0.00433 MS             0.732 MS            168.8 X     1.58 MS     364.8 X
                                 ∂ q̇t+1
                                   ∂qt
                                              0.174 MS              0.836 MS             4.78 X     2.84 MS     16.32 X
                                 ∂qt+1
                                   ∂ q̇t
                                             0.00307 MS             0.532 MS            173.1 X     0.81 MS     263.8 X
                                 ∂ q̇t+1
                                   ∂ q̇t
                                             0.0343 MS              0.872 MS             25.4 X     2.17 MS      63.2 X
                                 ∂ q̇t+1
                                   ∂τt
                                              0.040 MS              0.851 MS             21.2 X     2.31 MS     57.75 X
           C ATAPULT              A LL        0.265 MS              4.36 MS             16.45 X    12.0 MS       45.2 X
                                 ∂qt+1
                                   ∂qt
                                             0.0050 MS              0.845 MS            167.8 X    1.79 MS       358 X
                                 ∂ q̇t+1
                                   ∂qt
                                              0.181 MS              0.972 MS             5.36 X    3.71 MS      20.49 X
                                 ∂qt+1
                                   ∂ q̇t
                                             0.0036 MS              0.574 MS            156.7 X    0.958 MS      266 X
                                 ∂ q̇t+1
                                   ∂ q̇t
                                              0.035 MS              1.01 MS             28.42 X    2.72 MS       77.7 X
                                 ∂ q̇t+1
                                   ∂τt
                                              0.039 MS              0.960 MS             24.3 X    2.85 MS       73.1 X



   When our heuristic does not result in a valid f ∗t+1 , we can       1) Mesh-mesh collisions: Mesh-mesh collisions only have
simply return to our ordinary LCP solver to get a valid set C       two types of contacts: vertex-face and edge-edge collisions.
and S, and then re-run our stabilization.                           The other cases (vertex-edge, vertex-vertex, edge-face, face-
   As long as results from our LCP are stabilized, the gradients    face) are degenerate and easily mapped into vertex-face and
through the LCP presented in this section are valid even when       edge-edge collisions.
A is not full rank.                                                    Mesh-mesh collision detection algorithms like Gilbert-
                                                                    Johnson-Keerthi or Minkowski Portal Refinement are iterative,
C. Contact point and normal stabilization and gradients             and so produce imprecise collision points and normals that
                                                                    can vary depending on initialization. Both algorithms produce
   To compute gradients through each contact point and normal       a separating “witness plane” as part of their output, which
with respect to q t , we need to provide specialized routines for   is a 3D plane that approximately separates the two meshes
each type of collision geometry, including collisions between       (as much as possible, if they’re intersecting). Going from an
spheres, capsules, boxes, and arbitrary convex meshes. Deriving     approximate separating witness plane to precisely specified
the routines is a matter of straightforward algebra. However in     vertex-face and edge-edge collisions in the general case is
order for well-defined gradients to exist at all, each collision    complex. Take all the points on object A that lie within some
must have precisely specified contact points and normals, so        tiny  of the witness plane, and map them into 2D coordinates
that we can compute well-behaved gradients.                         within the witness plane. Do likewise with the points on object
   We describe in this appendix how we produce well-defined         B. Now we have two convex 2D shapes, because any linear
contact points and normals, since this is a design choice. The      slice of a convex shape is itself convex. Throw out any vertices
gradients of these methods are left as an exercise to the reader,   that are not on the 2D convex hull of the point cloud for A and
who is invited to check their work against our open-source          B respectively. Call the resulting convex shapes “witness hulls”
implementation.                                                     of A and B. Now any vertices on the witness hull of A that lie
within the witness hull of B are vertex-face collisions from A              vertex, and point the normal towards the nearest point on the
to B. Analogously, any vertices on the witness hull of B that               centerline of the pipe.
lie within the witness hull of A are face-vertex collisions from               For edge-pipe contacts, we treat them as pipe-pipe contacts
A to B. Finally, any edges of the witness hulls A and B that                where the radius of the first pipe is 0.
intersect are edge-edge collisions.                                            7) Gradients: Once all the contact behavior is firmly
   For all vertex-face collisions, during the forward simulation,           established, it’s just a matter of rote calculus to compute
the collision detector places a collision at the point of the               derivatives. We refer the reader to our open source code for the
vertex, with a normal dictated by the face under collision. The             implementation of those derivatives. Once a stable collision
body providing the vertex can only influence the collision                  detection system and its derivatives are implemented that, it’s
location p, and the body providing the face can only influence                                                ∂J T f
                                                                            possible to efficiently compute ∂qt t .
the collision normal n.
   For all edge-edge collisions, the collision detector first finds         D. Jacobian Benchmark Evaluation
the nearest point on edge A to edge B (call that a), and the                   In addition to speed, we are interested in the accuracy of our
nearest point on edge B to edge A (call that b). Then the                   Jacobians, as gradients computed via finite differencing become
contact point is set to the average of a and b, which is a+b          2 .   more inaccurate as the system becomes more complex, which
The normal is given by the cross product of the two edges.                  can lead to instability in optimization. As another baseline, we
That means changing q of Object A can affect the contact                    apply Ridders’ method [36] to efficiently calculate Jacobians
normal and the contact location along the other edge from                   to a higher-order error than central differencing, using the
Object B. For this reason, we need to construct our Jacobians               stopping criterion given in [33].
globally.                                                                      Table III contains the full benchmark performance of
   2) Sphere-sphere collisions: These are straightforward. We               our analytical Jacobians against central differencing and the
have sphere A, with center ca and radius ra , and sphere B, with            accurate Ridders’ extrapolated finite differences. For each
center cb and radius rb . The contact normal is the normalized              environment, we compare the speed of evaluation of each
vector pointing from cb to ca . The contact point is a weighted             individual component Jacobian as well as the total time.
combination of the two sphere centers, rb ∗craa+r    a ∗cb
                                                   +rb     .
   3) Mesh-sphere collisions: These can be divided into three               E. Calculating the Bounce Approximation Jacobian
categories: sphere-face collisions, sphere-edge collisions, and                Recall the matrix J T that transforms contact forces to joint
sphere-vertex collisions. Starting from the simplest, a sphere-             forces. By conservation of momentum J q̇ t = v t , leading to:
vertex collision places the contact point at the vertex and the
normal points from the vertex to the sphere center.                                                ∂pt+1    ∂q
                                                                                                         ≈ J t+1 J −1                    (29)
   A sphere-edge collision places the contact point on the                                          ∂pt      ∂q t
closest point to the sphere center along the edge. The contact
                                                                               Our matrix notation is somewhat misleading here, because
normal points from the collision point to the sphere center.
                                                                            we do not want our approximation to capture off-diagonals
   A sphere-face collision gets the contact normal from the                     ∂p                                                 ∂p
                                                                            of ∂pt+1 . Because we construct our approximate ∂pt+1 by
normal of the colliding face. Call the contact normal n, and                        t                                                  t
                                                                            assuming each bounce is independent, we end up with 0s on
define the sphere center as c and radius as r. For the simplicity
                                                                            the off-diagonals, but we know that assumption to be false. We
of downstream gradient computation, we then place the contact                                    ∂q
point at the point on the sphere, projected along with the                  just want to find a ∂qt+1 where the above equation matches
                                                                                                     t

contact normal towards the contact: c + r ∗ n.                              the diagonals as closely as possible, ignoring other elements.
   4) Pipe-pipe collisions: In a capsule-capsule collision, when            The following derives this relation in closed form.
both capsule cylinders are colliding, we call that a pipe-pipe                 Since we are only interested in enforcing the diagonal entries,
collision. Mechanically, this is very similar to an edge-edge               so we can write out a series of linear constraints we would
collision, only with added radius variables ra and rb . Let ca be           like to attempt to satisfy. Let J (i) denote the i’th column of
                                                                                            ∂p
the nearest point on the centerline of pipe A to the centerline             J . Recall that ∂pi,t+1 = −σi .
                                                                                               i,t
of pipe B. Let cb be the nearest point on the centerline of pipe
                                                                                                           ∂q t+1 −1
B to the centerline of pipe A. Then we say the contact point                                       J (i)         J ≈ −σi                 (30)
is rb ∗craa+r a ∗cb
                    . The contact normal points from cb to ca .                                             ∂q t (i)
           +rb
   5) Pipe-sphere collisions: These look a lot like pipe-pipe                                                                      ∂q
                                                                               We would like to find some approximate matrix ∂qt+1 that
collisions, except that cb is now fixed to the center of the                                                                        t
                                                                            satisfies all n of the above constraints as closely as possible.
sphere. Let ca be the nearest point on the centerline of the
                                                                            Stated directly as a least-squares optimization object:
pipe to cb . Then we say the contact point is rb ∗craa+r +rb
                                                             a ∗cb
                                                                   . The
contact normal points from cb to ca .                                                          X              ∂q t+1 −1       2
   6) Pipe-mesh collisions: This breaks down into two types of                           min          J (i)         J − (−σi )           (31)
                                                                                               i
                                                                                                               ∂q t (i)
contact: vertex-pipe, and edge-pipe. Face-pipe contacts reduce
to two edge-pipe contacts.                                                     The solution to this optimization can be found without
   For vertex-pipe contacts, we put the contact point at the                iterative methods.
        ∂q                                       ∂q
   Let ∂qt+1 be the i’th column of ∂qt+1 , and J (j,i) be the           F. Analytical derivatives through Featherstone
          t (i)                         t
j’th row and the i’th column of J . Note that:
                    ∂q t+1 −1 X                    ∂q t+1
            J (i)         J (i) =   J (j,i) (J −T
                                               (i)           )   (32)
                     ∂q t         j
                                    | {z }          ∂q t (j)
                                       scalar                               We present the derivation of analytical derivatives com-
                                                                        putation through the Featherstone algorithm. Although the
                 ∂q t+1       X                 T ∂q t+1                intellectual computation should be credited entirely to [25] and
  J (j,i) (J −T
             (i)           )=   (J (j,i) J −T
                                           (i) )          ) (33)                                                       ∂M −1 z
                                                                        [7], we specialized the derivations to obtain ∂qt t , ∂q ∂ct
                                                                                                                                     , and
  | {z }          ∂q t (j)    j |     {z       } ∂q t (j)                                                                   t      t
                                                                         ∂ct
                                                                        ∂ q̇ t for our implementation, rather than the entire inverse and
   scalar                                  vector
                                                                        forward dynamics. The detailed derivation might be of interest
   It becomes clear that we could construct a long vector v,
                                        ∂q                              to some readers.
which will map to every column of ∂qt+1 placed end to end.
                                            t
We can also construct a matrix W where every column W (i)
                                                                          The partial derivative of the inverse of joint space inertia
is the vectors J (j,i) J −1
                         (i) placed end to end (iterating over j).      matrix can be computed from the partial derivative of the joint
Now if we take the values of σi as entries of a vector r ∈ Rn ,
                                                                        space inertia matrix through the relation [7]:
we can write our optimization problem as a linear equation:

        X       ∂q t+1 −1            2
  min         J (i)    J (i) − (−σi ) = min ||W T v + r||22
       i
                 ∂q t
                                                           (34)
  This is a standard least squares problem, and is solved when:                          ∂M −1 z        ∂M −1
                                                                                                 = M −1     M z.                       (39)
                                                                                           ∂q            ∂q
                               v = −W T † r                      (35)

   Once we have a value of v, we can reconstruct the original
        ∂q                                 ∂q
matrix ∂qt+1 by taking each column of ∂qt+1 the appropriate
            t                                 t
segment of v.
   This is almost always an under-determined system, and we             Algorithm 1 and 2 show the recursive algorithms to compute
                          ∂q                                            M −1 and ∂M    ∂q M
                                                                                             −1
                                                                                                z, respectively. In Algorithm 3, the
want to default to having ∂qt+1 as close to I as possible, rather
                              t                                         derivatives of the Coriolis force with respect to the joint position
than as close to 0 as possible. We can slightly reformulate our
                                                                        and the joint velocity are given.
optimization problem where the least square objective tries to
keep the diagonals at 1, rather than 0. If we define an arbitrary
c vector (for “center”), we can use the identity:

                        W T (v − c) = −r − W T c                 (36)   Algorithm 1 Recursive forward dynamics for M −1
                                                                         1: for j = 1 to n do
                                                                         2:     for i = n to 1 Pdo
                        v = c − W T † (r + W T c)                (37)    3:         Î i = I i + l∈µ(i) Ad∗T −1 Πl AdT −1
                                                                                                             i,l       i,l

                                                                                    B̂i = l∈µ(i) Ad∗T −1 β l
                                                                                           P
                                                ∂q                       4:
   If we set c to the mapping for ∂qt+1 = I, then we get                                                 i,l
                                                                                                       −1
                                         t                                                 
a solution that minimizes the distance to the identity while             5:         Ψi = S Ti Î i S i
satisfying the constraints, measured as the sum of the squares
                                                                         6:         Πi = Î i − Î i S i Ψi S Ti Î i
of all the terms.                                                                                                         (
                                                                                                                           1 if i = j
   Also, remember that to get our Jacobian with respect to               7:         αi = δi,j − S Ti B̂i , where δi,j =
velocity, we simply:                                                                                                       0, otherwise
                                                                         8:        β i = B̂i + Î i S i Ψi αi
                            dθt+1     ∂q                                 9:    end for
                                  = ∆t t+1                       (38)
                             dθ̇t      ∂q t                             10:    for i = 1 to
                                                                                           n do                                
                                                                        11:          M −1 i,j = Ψi αi − S Ti Î i AdT −1 V̇ λ(i)
  And that should approximately solve the “gradient bounce”                                                          λ(i),i
                                                                                   V̇ i = AdT −1 V̇ λ(i) + S i M −1 i,j
                                                                                                              
                                                                        12:
problem. On timesteps where there is only a single bouncing                                   λ(i),i

contact, this will provide an exact solution. With more than            13:    end for
                                                                        14: end for
one bounce in a single frame, this may be approximate.
Algorithm 2 Derivative of the recursive inverse dynamics for                 Algorithm 3 Derivative of the recursive inverse dynamics for
∂M     −1                                                                    ∂c      ∂c
 ∂q M     z                                                                  ∂q and ∂ q̇
 1: for i = 1 to n do                                                         1: for i = 1 to n do
        V̇ i = AdT −1 V̇ λ(i) + S i M −1 z i
                                         
 2:                                                                           2:     V i = AdT −1 V λ(i) + S i q̇ i
                       λ(i),i                                                                                   λ(i),i
 3:     for j = 1 to n do                                                     3:        V̇ i = AdT −1 V̇ λ(i) + adV i S i q̇ i + Ṡ i q̇ i
            ∂ V̇ i               ∂ V̇ λ(i)                                                         λ(i),i
 4:         ∂q j = AdT λ(i),i ∂q j − ad ∂h           i AdT −1      V̇ λ(i)              for j = 1 to n do
                           −1                                                 4:
                                                  ∂q j      λ(i),i
                                                                                             ∂V i            ∂V λ(i)
                     + ∂S
                                  −1
                                                                             5:                  = AdT −1           − ad ∂hi AdT −1 V λ(i) +
                        ∂q j M          z i
                            i
 5:                                                                                          ∂q      j         ∂q          λ(i),i        j            ∂q j     λ(i),i

 6:     end for                                                                    ∂S i
                                                                                   ∂q j q̇ i
 7: end for                                                                                    ∂V i               ∂V λ(i)     k
                                                                              6:               ∂ q̇ j = AdT λ(i),i ∂ q̇ j + S i
                                                                                                            −1
 8: for i = n to 1 do
        F i = I i V̇ i + l∈µ(i) Ad∗T −1 F l                                                                       ∂ V̇ λ(i)
                         P
                                                                                               ∂ V̇ i
                                                                                               ∂q j = AdT λ(i),i ∂q j − ad ∂h
 9:                                                                           7:                            −1                     i AdT −1     V̇ λ(i)
                                            i,l                                                                                 ∂q       λ(i),i        j
10:     for j = 1 to n do
            ∂F i        ∂ V̇ i    ∂F   g                                      8:                                    + ad ∂V i S i q̇ i + adV i ∂S        ∂ Ṡ i
                                                                                                                                               ∂q q̇ i + ∂q q̇ i
                                                                                                                                                  i
11:         ∂q j = I i ∂q j − ∂q j                                                                                        ∂q j                             j          j
                                                                                             ∂ V̇ i             ∂ V̇ λ(i)
                                         ∗                    ∗               9:               ∂ q̇ j = AdT λ(i),i ∂ q̇ j
                        P                         ∂F l                                                      −1
12:                   + l∈µ(i) AdT −1 ∂q − ad ∂hi F l
                                           i,l       j        ∂q j                                                                                                        k
            h
              ∂M      −1
                            i
                                     ∂S i T            T ∂F i                10:                                    + ad ∂V i S i q̇ i + adV i S ki + ∂∂Ṡ
                                                                                                                                                        q̇ q̇ i + Ṡ i
                                                                                                                                                           i

13:            ∂q  M     z       =   ∂q      F  i + S  i ∂q
                                                                                                                          ∂ q̇ j                               j
                                i,j       j                 j
                                                                             11:     end for
14:    end for                                                               12: end for
15: end for
                                                                             13: for i = n to 1 do
                                                                                        F i = I i V̇ i − ad∗V i I i V i − F gi + l∈µ(i) Ad∗T −1 F l
                                                                                                                                 P
                                                                             14:
                                                                                                                                             i,l
                                                                             15:        for j = 1 to n do
                                                                                            ∂F i        ∂ V̇ i      ∗               ∗   ∂V i     ∂F g
                                                                             16:            ∂q j = I i ∂qj − ad ∂V i IV i − adV i I i ∂q j − ∂q j
                                                                                                                     ∂qj
                                                                                                                                            
                                                                                                        P               ∗      ∂F l   ∗
                                                                             17:                      + l∈µ(i) AdT −1 ∂q − ad ∂hi F l
                                                                                                                                                i,l    j       ∂q j
                                                                                               ∂F i         ∂ V̇ i     ∗              ∗       ∂V i
                                                                             18:               ∂ q̇ j = I i ∂ q̇ j − ad ∂V i IV i − adV i I i ∂ q̇ j
                                                                                                                                       ∂ q̇ j
                                                                                                                         P       ∗     ∂F l
                                                                             19:                                     +  l∈µ(i) AdT −1  ∂q j
                                                                                               h          i                        i,l
                                                                                                   ∂c                 ∂S i T       T ∂F i
                                                                             20:                   ∂q               = ∂q F i + S i ∂q
                                                                                                                        j               j
                                                                                               h          ii,j
                                                                             21:                   ∂c
                                                                                                   ∂ q̇             = S Ti ∂F
                                                                                                                           ∂ q̇
                                                                                                                                i

                                                                                                              i,j                  j
                                                                             22:    end for
                                                                             23: end for
