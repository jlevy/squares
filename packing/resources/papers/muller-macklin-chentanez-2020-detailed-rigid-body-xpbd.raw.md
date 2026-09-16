ACM SIGGRAPH / Eurographics Symposium on Computer Animation 2020                                                                       Volume 39 (2020), Number 8
J. Bender and T. Popa
(Guest Editors)




                                          Detailed Rigid Body Simulation
                                      with Extended Position Based Dynamics

                        Matthias Müller1            Miles Macklin1,2              Nuttapong Chentanez1      Stefan Jeschke1    Tae-Yong Kim1

                                                                       1 NVIDIA       2 University of Copenhagen




Figure 1: Our method allows the stable simulation of a rolling ball sculpture with fast moving marbles and collisions against curved geometry
as well as a remote controlled car racing over obstacles with deformable tires.

        Abstract
        We present a rigid body simulation method that can resolve small temporal and spatial details by using a quasi explicit integra-
        tion scheme that is unconditionally stable. Traditional rigid body simulators linearize constraints because they operate on the
        velocity level or solve the equations of motion implicitly thereby freezing the constraint directions for multiple iterations. Our
        method always works with the most recent constraint directions. This allows us to trace high speed motion of objects colliding
        against curved geometry, to reduce the number of constraints, to increase the robustness of the simulation, and to simplify the
        formulation of the solver. In this paper we provide all the details to implement a fully fledged rigid body solver that handles
        contacts, a variety of joint types and the interaction with soft objects.
        CCS Concepts
        • Computing methodologies → Simulation by animation; Interactive simulation;
        Keywords: Rigid body simulation, soft body simulation, position based dynamics



1. Introduction                                                                               methods are rarely used in games and films because large forces
                                                                                              and small time steps are needed to make colliding bodies look rigid.
Rigid body simulation lays at the heart of every game engine and                              Recently, penalty methods have gained popularity in connection
plays a major role in computer generated special effects in movies.                           with differentiable simulations because they generate smooth tra-
The central aspects of a rigid body simulation are contact and                                jectories.
joint handling. Two popular approaches exist for collision handling,
namely penalty methods and impulse based methods. Penalty meth-                                  The most popular approach is to use impulses, however. Mir-
ods use forces caused by penetrating bodies for separation. These                             tich and Canny [MC95] laid the foundation for impulse based

 c 2020 The Author(s)
Computer Graphics Forum c 2020 The Eurographics Association and John
Wiley & Sons Ltd. Published by John Wiley & Sons Ltd.
                               M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics


                              𝛻𝐶1      𝐩3                                       PBD has mostly been used for the simulation of constrained par-
                                            𝛻𝐶2                              ticle systems to simulate cloth and soft bodies until Macklin et
                                                                             al. [MM13] devised a way to handle fluids as well. This allowed the
                                                                             development of a particle based unified solver in the position based
                    𝑙1                            𝑙2                         framework [MMCK14] by the same group. They used the idea of
                                                                             shape matching [MHTG05] to simulate rigid bodies as a collection
           𝐩1                                          𝐩2                    of rigidly connected particles. However, the cost of shape matching
                                                                             grows with the number of particles, impulse propagation is slow
                                                                             and handling joints difficult. A more effective way is to extend
                                       𝐩3                                    PBD beyond particles and simulate rigid bodies as single entities
                                                                             by introducing rotational states. Deul et al. [DCB14] formulated
                                                                             this type of rigid body dynamics in the positional framework of
                    𝑙1                            𝑙2                         PBD.
                                                                                Working with velocities or linearizing the positional problem for
           𝐩1                                          𝐩2                    an iteration of a global solver both have one aspect in common:
                                                                             they freeze the constraint directions for the time of the linear solve,
                                                                             i.e. over several iterations [MEM∗ 19, ST96, KSJP08]. In this case,
Figure 2: Non-linear Gauss-Seidel: Points 𝑝 1 and 𝑝 2 are fixed to           contacts have to be treated as local planes and coulomb friction
the ground. The distances from the top point 𝑝 3 to 𝑝 1 and 𝑝 2 are          cones as polyhedra. Also, constraints in three dimensions such as
constrained to be 𝑙1 and 𝑙2 respectively. Finding a position for 𝑝 3         an attachment yield three constraint equations. In contrast, algo-
which satisfies both constraints is a non-linear positional problem.         rithms based on solving local contact problems with methods such
By working with velocities or by solving it globally the constraint          as Gauss-Seidel allow contact geometry to change at each itera-
gradients get fixed. In these cases the red point above the true so-         tion. This approach has been used to model smooth isotropic fric-
lution is found no matter how many iterations are applied. To find           tion [Erl17, DBDB11]. We extend this approach to also allow con-
the true solution, multiple linear solves have to be performed. A            tact normal geometry to change each iteration.
non-linear Gauss-Seidel solver works on the non-linear positional
                                                                                The original PBD approach uses the non-linear projected Gauss-
problem directly. It updates the gradients after each individual con-
                                                                             Seidel (NPGS) method to solve the non-linear positional equations.
straint projection and converges to the true solution without the
                                                                             NPGS is fundamentally different from applying the regular or pro-
danger of overshooting.
                                                                             jected Gauss-Seidel (PGS) method to the linearized equations. Fig-
                                                                             ure 2 visualizes this difference. The key is that after each individual
                                                                             constraint solve, the positions are immediately updated. In this way,
rigid bodies simulation in graphics and games in the mid nineties.           PBD works on the non-linear problem directly, increasing both ro-
Hecker [Hec97] introduced the concepts to game developers and                bustness and accuracy. Round friction cones or collisions against
Baraff [Bar97] to the computer graphics community. Here, the ve-             curved objects are easy to handle. Instead of storing contacts as ref-
locities are changed immediately at impacts by applying impulses             erences to a pair of objects together with a static normal which re-
instead of applying accelerations caused by forces. Conceptually,            sults to a contact plane, we only store the references and recompute
these methods work on the velocities directly omitting the acceler-          the normal before every individual solve of the specific contact. A
ation layer.                                                                 less expensive way would be to store the local contact geometry as
                                                                             in the traditional approach but using a higher-order approximation.
   Simulating objects with dynamically changing positions and ori-
entations is a non-linear problem. However, freezing a spatial con-             Due to these advantages, our goal was to extend PBD in a way
figuration and solving for velocities results in a linear system of          that allows the implementation of a fully fledged rigid body engine
equations. Contacts yield inequality constraints so in general, a lin-       but without sacrificing its simplicity. We will provide all the algo-
ear complementarity problem (LCP) has to be solved which is –                rithms on a level that allows an immediate implementation.
as the name indicates – still linear. The space of velocities can be           However, PBD has had the reputation of being non-physical and
viewed as the tangent space to the non-linear space of spatial states        too much of a simplification based on the following concerns:
at the current configuration. Working within the linear space of ve-
locities is therefore more convenient than working with positions            • It does not use physical quantities and units
and orientations directly. However, one of the main drawbacks of             • The stiffness is iteration and time step dependent
this approach is the problem of drift because a velocity solver does         • The integration is not physically accurate
not see positional errors. Existing engines solve this problems with         • It is dependent on the order of constraint handling
a variety of methods such as introducing additional forces or con-           • It depends on mesh tessellation
straints.                                                                    • It converges slowly
                                                                                Fortunately, all these concerns have been addressed recently with
   Position based dynamics (PBD) [MHR06, Sta09] solves this
                                                                             the result that our proposed solver is a serious competitor to other
problem by working with positions directly. Velocities are derived
                                                                             methods as we will show in the results section.
after the solve as the difference between the configuration at the
end and the beginning of the time step.                                         The first three concerns have been addressed in [MMC16]. Ex-

                                                                                                                                                 c 2020 The Author(s)
                                                                                Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                       M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

tended PBD (XPBD) adds a small extension to the original ap-                             of Baraff [Bar93]. We have already mentioned most of the specific
proach which makes stiffness independent of the iteration count                          work that is closely related to our method in the introduction. Here
and time step size with physical units and allows measuring forces                       we add a few more approaches to that list.
and torques. The authors also show that XPBD is a close approxi-
                                                                                            Our method focuses on the handling of varying contact normals.
mation of implicit Euler integration. An important feature of XPBD
                                                                                         To handle time-varying contact areas, Xu et al. [XZB14] proposed
is that compliance is used which is the inverse of stiffness. This
                                                                                         a simulation method based on semi-implicit integration. They use
means we can easily handle infinitely stiff constraints in a robust
                                                                                         analytic contact gradients in connection with a penalty formulation.
way by setting the compliance to zero. In this case XPBD falls
                                                                                         The stability is increased by using symbolic Gaussian elimination.
back to PBD.
                                                                                         To increase the fidelity of contact handling, Wang et al. [WSPJ17]
   The solution returned from Gauss-Seidel methods is in general                         precompute spatially and directionally varying restitution coeffi-
dependent on the ordering of the constraint solve. There are sit-                        cients by treating a body as a stiff deformable object and solve
uations in which this order dependence is valuable, for instance                         a proxy contact problem. Using this data results in more realistic
to control error propagation. However, the dependence can be re-                         bouncing behavior during simulation.
moved by using Jacobi, or symmetric successive over relaxation
                                                                                            Implicit position-based time discretizations and constraints have
(SSOR) iterations. PBD can also handle constraints that are based
                                                                                         been used in the computer-aided design (CAD) and multibody dy-
on continuum mechanics with common finite element (FEM) con-
                                                                                         namics software, such as ADAMS and MBDyn [OCC77, Rya90,
stitutive models [MMC16]. This alleviates the problem of mesh de-
                                                                                         MMM14]. They most often use penalty models of contact that re-
pendent stiffness present in more ad-hoc energy models.
                                                                                         quire carefully tuned parameters, and do not allow for perfectly
   Finally, the concern regarding slow convergence was addressed                         hard contact response. Offline multibody dynamics software may
most recently in [MSL∗ 19]. By replacing solver iterations with                          also use higher-order integration schemes such as second order
substeps, Gauss-Seidel and Jacobi methods become competitors of                          implicit Euler (BDF2) that increase the accuracy of the simula-
global solvers in terms of convergence. Substepping in combina-                          tion of objects in free flight. However, for non-smooth trajectories,
tion with one NPGS iteration per substep yields a method that looks                      typical situation in rigid body simulations with contact, we found
computationally almost identical to an explicit integration step, but                    higher-order integration may yield spurious and unpredictable col-
with the advantage of being unconditionally stable due to the usage                      lision response. This motivates our use of small time-steps and
of compliance. We call it a quasi-explicit method.                                       complementarity-based contact models.
   The findings described in [MSL∗ 19] about substepping are sur-                           One of the advantages of our method is the natural handling
prising and somewhat unintuitive. Substepping is not just the reduc-                     of coupled simulations with rigid and soft bodies. Galvez et
tion of the time step size. The important concept is the simulation                      al. [GCC∗ ] simulate the non-smooth dynamics of systems with
time budget per frame which is typically constant in real-time appli-                    rigid and deformable bodies by linking them with kinematic joints.
cations and given by the number of sub-steps times the number of                         The resulting contact problem is formulated using a mixed aug-
solver iterations per substep. One extreme choice is to only use one                     mented Lagrangian method. The equations of motion are integrated
substep and spend all the time budget with solving the equations                         with a non-smooth generalized-𝛼 time integration scheme.
to high accuracy. The other extreme is to use as many substeps as
possible and only use a single iteration to solve the equations ap-                         To handle rigid bodies, we augment the particles with orienta-
proximately. The surprising fact which we will demonstrate in this                       tion information. Müller et al. [MC11] used this idea to stabilize
paper as well is that the best choice in terms of accuracy of the                        the simulation of soft objects via shape matching. Later Umetani
simulation is to choose the maximum number of substeps with one                          et at. [USS15] leveraged the same idea to simulate position based
iteration each. Substepping is not only optimal for accuracy, it also                    elastic rods.
reveals high frequency temporal detail that is missed when using                            The most closely related method to our approach is the work of
large time steps. Substepping also improves energy conservation                          Deul et al. [DCB14]. They developed a formulation of rigid body
significantly and reduces the chances of missing collisions via tun-                     dynamics in the positional framework of PBD. Their ideas are for-
neling.                                                                                  mulated somewhat vaguely, however. An example is the short para-
   Since using one iteration is the best choice in terms of accuracy,                    graph about joints which only discusses one joint type and does not
the number of substeps can be derived from the time budget and                           address joint limits – a central feature of rigid body engines. In the
since we use XPBD which allows the use of true physical quanti-                          results section we will present various examples which rely on the
ties, there is no need to tune any parameters. Due to the uncondi-                       handling of hard and soft joint limits. We also describe collision
tional stability of XPBD, there is no need to tune the time step sizes                   against rounded objects. A central difference is the use of XPBD
for stability reasons either.                                                            instead of PBD which not only allows the use of physical param-
                                                                                         eters but also allows the derivation of forces and torques at joints
                                                                                         and contacts.
2. Related Work
Rigid body simulation has a long history in computer graphics. For
                                                                                         3. Position Based Rigid Body Simulation
a comprehensive overview of the field we refer the reader to the
recent survey by Bender et al. [BET14]. It covers most of the im-                        We first recap the original position based simulation algorithm for
portant work in this field published since the state of the art report                   constrained particle systems.

 c 2020 The Author(s)
Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                  M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

                                               ∆𝐱                                                    ∆𝐱1                 ∆𝐱 2

                                         𝑚1                       𝑚2                                    𝑚1             𝑚2


                                                    ∆𝐱
                                       𝐫1
                                                                                        ∆𝐪1                                          ∆𝐪2
                                                                  𝐫2
                                                                                                 ∆𝐱1                        ∆𝐱 2

                                    𝑚1 , I1                  𝑚2 , I2                          𝑚1 , I1                      𝑚2 , I2


                                                     ∆𝐪

                                                                                        ∆𝐪1                                          ∆𝐪2

                                                             I2                                                               I2
                                                                                                I1
                                         I1

Figure 3: The basic correction operations. Top: traditional particle based PBD. A positional correction vector Δx is applied to a pair of
particles. This correction is distributed among both particles proportional to their inverse mass to conserve linear and angular momentum.
Middle: applying a positional correction to points r1 and r2 on a pair of rigid bodies results in a pair of positional corrections Δx1 and Δx2
applied to the centers of mass as well as a pair of rotational corrections Δq1 and Δq2 proportional to a combination of their inverse masses
and inverse moments of inertia. Bottom: a rotational correction Δq is applied to two bodies – in this case to align their orientations. The
rotational correction is distributed among the two bodies proportional to their inverse moments of inertia while the centers of mass are not
affected.



3.1. Particle Simulation Loop                                                   Seidel or Jacobi style) and moves the positions of the particles us-
                                                                                ing constraint projection. Discussing this part will be our main fo-
Algorithm 1 Position Based Particle Simulation                                  cus. In the third loop the new velocities are derived from the previ-
while simulating do                                                             ous and current positions. Macklin et al. [MSL∗ 19] showed that it
    CollectCollisionPairs();                                                    is significantly more effective to take substeps than solver iterations
    ℎ ← Δ𝑡/numSubsteps;                                                         so "numPosIters" is typically set to 1.
    for numSubsteps do
        for 𝑛 particles do                                                      3.2. Rigid Body Simulation Loop
            xprev ← x;
            v ← v + ℎ fext /𝑚;                                                  In contrast to a particle which is described by its position x, its
            x ← x + ℎ v;                                                        velocity v and its mass 𝑚 alone, the state of a rigid body of finite
        end                                                                     size also contains the corresponding angular quantities. These are
        for numPosIters do
            SolvePositions(x1 , . . . x𝑛 );                                     • its orientation which can be described by a unit quaternion q ∈
        end                                                                       R4 , |q| = 1,
        for 𝑛 particles do                                                      • its angular velocity 𝜔 ∈ R3 and
            v ← (x − xprev )/ℎ;                                                 • its inertia tensor I ∈ R3𝑥3 .
        end
                                                                                   The angular velocity vector can be split into the unit axis of ro-
    end
                                                                                tation and the scalar angular velocity as
end
                                                                                                                    𝝎 = 𝜔 · nrot .                                   (1)
   Algorithm 1 shows the simulation loop. Here we already in-                   The inertia tensor I is the quantity that corresponds to the mass in
cluded the idea of substepping for which Δ𝑡 is the time step size               rotational terms. For basic shapes like boxes and spheres it is given
and ℎ the substep size. During the first loop of each substep, the              by simple formulas. Blow and Binstock [BB04] devised an elegant
particle’s positions x𝑖 and velocities v𝑖 are explicitly integrated             and short algorithm for the general case of a body that is described
taking only the external forces fext such as gravity into account.              by a closed triangle mesh, which simultaneously computes the cen-
The second loop implements the core implicit solver. The proce-                 ter of mass. Algorithm 2 shows the extended version of Algorithm 1
dure "SolvePositions" iterates through all constraints (either Gauss-           which take these additional quantities into account.

                                                                                                                                                    c 2020 The Author(s)
                                                                                   Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                        M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

Algorithm 2 Position Based Rigid Body Simulation                                         linear momentum, the correction vector is applied to both parti-
while simulating do                                                                      cles proportional to their inverse masses 𝑤 𝑖 = 𝑚 𝑖−1 . The middle
   CollectCollisionPairs();                                                              row shows the first basic operation used for rigid bodies, namely
   ℎ ← Δ𝑡/numSubsteps;                                                                   applying a position correction Δx to solve a generalized distance
   for numSubsteps do                                                                    constraint between points on two bodies. The points are defined by
        for 𝑛 bodies and particles do                                                    the vectors r1 and r2 relative to the center of mass. To conserve lin-
            xprev ← x;                                                                   ear and angular momentum, the operation changes the positions as
            v ← v + ℎ fext /𝑚;                                                           well as the orientations of both bodies proportional to their general-
            x ← x + ℎ v;                                                                 ized inverse masses. The second operation is applying a rotational
                                                                                         correction to two bodies as shown in the bottom row. In this partic-
                 qprev ← q;                                                              ular case, the correction is applied to align the orientations of the
                 𝜔 ← 𝜔 + ℎ I−1 (𝜏ext − (𝜔 × (I𝜔)));                                      two bodies. To conserve angular momentum, it has to be distributed
                 q ← q + ℎ 21 [𝜔 𝑥 , 𝜔 𝑦 , 𝜔 𝑧 , 0] q;                                   among the two bodies proportional to their inverse moments of in-
                 q ← q/|q|;                                                              ertia. We derive the formulas for the updates from impulse based
            end                                                                          dynamics in the Appendix. Here we show the final versions to be
            for numPosIters do                                                           used in an implementation.
                SolvePositions(x1 , . . . x𝑛 , q1 , . . . q𝑛 );
            end
            for 𝑛 bodies and particles do                                                3.3.1. Positional Constraints
                v ← (x − xprev )/ℎ;
                          −1 ;
                Δq ← q qprev                                                             To apply a positional correction Δx at positions r1 and r2 , we first
                𝝎 ← 2[Δq 𝑥 , Δq 𝑦 , Δq 𝑧 ]/ℎ;                                            split it into its direction n and its magnitude 𝑐. The latter corre-
                𝝎 ← Δ𝑞 𝑤 ≥ 0 ? 𝝎 : −𝝎;                                                   sponds to the evaluation of the constraint function in PBD. We then
                                                                                         compute the two generalized inverse masses
            end
                                                                                                               1
            SolveVelocities(v1 , . . . v𝑛 , 𝜔1 , . . . 𝜔 𝑛 );                                             𝑤1 ←    + (r1 × n)𝑇 I−1
                                                                                                                               1 (r1 × n)                    (2)
      end                                                                                                      𝑚1
                                                                                                               1
end                                                                                                       𝑤2 ←    + (r2 × n)𝑇 I−1
                                                                                                                               2 (r2 × n).                   (3)
                                                                                                               𝑚2
                                                                                         Following XPBD, we compute the Lagrange multiplier updates
   The additional lines for integrating the rotational quantities and                                                     −𝑐 − 𝛼˜ 𝜆
deriving the velocities can easily be added to an existing PBD sim-                                               Δ𝜆 ←                                       (4)
                                                                                                                        𝑤 1 + 𝑤 2 + 𝛼˜
ulator. The term for integrating angular velocity including external
                                                                                                                    𝜆 ← 𝜆 + Δ𝜆                               (5)
torques and gyroscopic effects is derived from the Newton-Euler
equations. We refer the reader to Brian Mirtich’s excellent the-                         where 𝛼˜ = 𝛼/ℎ2 and 𝛼 the compliance of the constraint. One mul-
sis [Mir96] for a derivation. To update the quaternions based on the                     tiplier 𝜆 is stored for each compliant constraint. It is set to zero be-
angular velocity and to derive the angular velocity from the change                      fore the iterative solver starts. The compliance corresponds to the
of the quaternions we use linearized formulas. They are fast and                         inverse of the stiffness and has the unit meters / Newton. Working
robust and well suited for the small time steps used in substepping.                     with the compliance allows the simulation of infinitely stiff con-
In contrast to simple particles, the implicit solver also manipulates                    straints by setting 𝛼 = 0. Setting the positional impulse p = Δ𝜆n we
the orientations of the bodies.                                                          update the states of the bodies immediately after each constraint
   This position based solver allows the simultaneous and coupled                        solve via
simulation of both rigid and deformable objects. To achieve this we
                                                                                                           x1 ← x1 + p/𝑚 1                                   (6)
iterate through all bodies as well as all particles. For the particles
we simply omit the updates of the rotational quantities.                                                   x2 ← x2 − p/𝑚 2                                   (7)
                                                                                                                     1h               i
                                                                                                           q1 ← q1 + I−11  (r1 × p), 0 q1                    (8)
                                                                                                                     2
3.3. Core Projection Operations                                                                                      1h                i
                                                                                                           q2 ← q2 − I−1   (r2 × p), 0   q2 .                (9)
The modifications to the main loop are straightforward. The chal-                                                    2 2
lenging part is the extension of the solver to handle constraints be-
tween finite sized bodies in a positional framework. Fortunately                            Note the minus sign in the update of the second body. Imme-
we only need two basic operations. The tasks of solving arbitrary                        diately updating the bodies after handling each constraint prevents
joints, handling contacts or coupling rigid with soft bodies can all                     overshooting and is one of the causes of PBD’s robustness. This re-
be built on top of these operations alone. They are visualized in                        sults in a non-linear projected Gauss-Seidel solve. Alternatively a
Figure 3. The top row shows a distance constraint between two                            Jacobi solve can be used for parallel implementations or to remove
particles as a reference. Here a correction vector Δx is applied to                      the dependence on the order of constraint projection but at the cost
project the overstretched constraint to its rest length. To conserve                     of slower convergence. In this case, the updates are accumulated

 c 2020 The Author(s)
Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

and applied after each iteration through all constraints. After the           3.4.1. Rotational Degrees of Freedom
solve, the forces acting along the constraint can be derived as               For a joint that aligns the mutual orientations of two bodies we
                                                                              compute the angular correction as follows:
                                                                                                                  q = q1 q−1                                     (18)
                             f = 𝜆n/ℎ2 .                           (10)                                                   2
                                                                                                          Δqfixed = 2(𝑞 𝑥 , 𝑞 𝑦 , 𝑞 𝑧 ).                         (19)
   Connecting a rigid body and a soft body defined as a constrained              To setup more general joints, an attachment point r̄ as well as a
particle system is straightforward because each body can be re-               set of perpendicular unit axes [ā, b̄, c̄] have to be defined on both
placed with a single particle by setting 𝑤 ← 𝑚 −1 and omitting the            bodies in the shape. To handle the joint, these are first transformed
update of the orientation.                                                    into world space vectors r and [a, b and c].
                                                                                For a hinge joint, we want the axes a1 and a2 to be aligned. To
3.3.2. Angular Constraints                                                    achieve this we apply

For joints we need the ability to constrain the mutual orientation of                                         Δqhinge = a1 × a2 .                                (20)
two bodies. In this case the correction is a rotation vector Δq ∈ R3 .
We split it into its direction n which is the rotation axis and its             To drive a hinge joint towards a specified target angle 𝛼 we rotate
magnitude 𝜃 which is the rotation angle. The generalized inverse              b1 about a1 by then angle 𝛼 to get btarget and apply
masses are

                            𝑤 1 = n𝑇 I−1
                                      1 n                          (11)                                    Δqtarget = btarget × b2 .                             (21)

                            𝑤 2 = n𝑇 I−1
                                      2 n                          (12)       The corresponding compliance 𝛼 controls the stiffness of the con-
                                                                              straint. With a target angle constraint we can create a velocity
                                                                              driven motor by updating the target angle via 𝛼 ← 𝛼 + ℎ 𝑣 at ev-
  The XPBD updates are the same as before with the angle replac-
                                                                              ery substep, where 𝑣 is the target velocity of the motor and the
ing the distance
                                                                              corresponding compliance its strength.
                                 −𝜃 − 𝛼˜ 𝜆                                       Handling joint limits is an essential part of a rigid body engine.
                         Δ𝜆 ←                                      (13)
                               𝑤 1 + 𝑤 2 + 𝛼˜                                 For the rotational degrees of freedom this amounts to limiting joint
                           𝜆 ← 𝜆 + Δ𝜆.                             (14)       angles. To do this we use the generic procedure defined in Algo-
                                                                              rithm 3. It limits the angle between the axes n1 and n2 of two bodies
This time, the correction only affects the orientations as                    to be in the interval [𝛼, 𝛽] using the common rotation axis n.
                                1h          i
                     q1 ← q1 + I−1  1   p, 0 q1                    (15)       Algorithm 3 Handling joint angle limits.
                                2
                                1h          i                                 LimitAngle (n, n1 , n2 , 𝛼, 𝛽):
                     q2 ← q2 − I−1   2  p, 0 q2 .                  (16)          𝜙 ← arcsin((n1 × n2 ) · n);
                                2
                                                                                 if n1 · n2 < 0 then 𝜙 ← 𝜋 − 𝜙;
                                                                                 if 𝜙 > 𝜋 then 𝜙 ← 𝜙 − 2𝜋;
   It is important to note that the inertia tensor I depends on the ac-
                                                                                 if 𝜙 < −𝜋 then 𝜙 ← 𝜙 + 2𝜋;
tual orientation of the body. Therefore, it would have to be updated
                                                                                 if 𝜙 < 𝛼 or 𝜙 > 𝛽 then
after every constraint projection. Instead, we project the quantities
                                                                                      𝜙 ← clamp(𝜙, 𝛼, 𝛽);
n, r and p into the rest state of the bodies before evaluating the ex-
                                                                                      n1 ← rot(n, 𝜙) n1 ;
pressions above. For joints, the attachment points r are typically
                                                                                      Apply(Δqlimit = n1 × n2 );
defined in the rest state already. In addition, we rotate the bodies in
the rest state such that the inertia tensor becomes diagonal which                end
simplifies the expressions above and allows storing the tensor as a           return
vector. Analogous to Equation (10) we can derive the torque ex-
erted as
                                                                                For hinge joints with common axis a1 = a2 we use [n, n1 , n2 ] =
                                                                              [a1 , b1 , b2 ].
                                                                                 For spherical joints (also called ball-in-socket joints) we have to
                             𝜏 = 𝜆n/ℎ2 .                           (17)
                                                                              distinguish between swing and twist limits for the motion of axis a2
                                                                              w.r.t. axis a1 . To restrict swing we use [n, n1 , n2 ] = [a1 ×a2 , a1 , a2 ].
                                                                              Twist must be decoupled from swing. We achieve this with the fol-
3.4. Joints                                                                   lowing axes:
We now describe how to handle joints of various types using the                                      n ← (a1 + a2 )/(|a1 + a2 |)                                 (22)
two correction operations defined in the previous section. Joints
                                                                                                    n1 ← b1 − (n · b1 ) n; n1 ← |n1 |                            (23)
attach pairs of bodies and restrict relative positional and rotational
degrees of the bodies.                                                                              n2 ← b2 − (n · b2 ) n; n2 ← |n2 |                            (24)


                                                                                                                                                  c 2020 The Author(s)
                                                                                 Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                       M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

   All limits can be made soft by using 𝛼 > 0.                                            non-linear Gauss-Seidel solver lets us handle the complementarity
                                                                                          condition by simply checking it on a per constraint basis. If the
3.4.2. Positional Degrees of Freedom                                                      bodies are penetrating we apply Δx = 𝑑n using 𝛼 = 0 and 𝜆 𝑛 .
Handling the positional degrees of freedom is simpler. We first                             To handle static friction we compute the relative motion of the
compute the positional offset as Δr = r2 − r1 . Setting Δx = Δr at-                       contact points and its tangential component
taches the bodies without separation which is the typical case for                                              Δp = (p1 − p̄1 ) − (p2 − p̄2 )               (27)
joints. Using 𝛼 > 0 allows the simulation of a spring with zero rest
length. We can make this more flexible by defining an upper limit                                              Δp𝑡 = Δp − (Δp · n)n.                         (28)
𝑑max for the separation distance. In this case we only apply a cor-                       Static friction prevents tangential motion at the contact points
rection if |Δr| > 𝑑max and use the correction                                             which is the case if Δp𝑡 = 0. Therefore, to enforce static friction
                                    Δr                                                    we apply Δx = Δp𝑡 at the contact points with 𝛼 = 0 but only if
                           Δx =         (|Δr| − 𝑑max ).                            (25)   𝜆 𝑡 < 𝜇 𝑠 𝜆 𝑛 , where 𝜇 𝑠 is the static friction coefficient. If the two
                                   |Δr|
                                                                                          bodies have different coefficients, we use 𝜇 = (𝜇1 + 𝜇2 )/2. Another
   We can also relax the fixed attachment by allowing the bodies                          option would be to take the maximum or minimum value.
to move within boundaries along a subset of the axes. For this we
start with Δx = 0. For the first axis a1 we compute the projected                         3.6. Velocity Level
displacement 𝑎 = Δr · a1 . If 𝑎 < 𝑎 min we add a1 (𝑎 − 𝑎 min ) to the
                                                                                          PBD updates the velocities after the position solve and then im-
correction vector, if 𝑎 > 𝑎 max we add a1 (𝑎 − 𝑎 max ). We do this for
                                                                                          mediately goes to the next substep. However, to handle dynamic
all axes and all limits before we apply the final correction vector.
                                                                                          friction and restitution we append a velocity solve as shown in Al-
This way, all limits are treated with a single constraint projection.
                                                                                          gorithm 2. Here we iterate once through all the contacts and update
   Setting all limits except the ones for the first axis to zero simu-                    the new velocities.
lates a prismatic joint. For a robot we might want to drive the joint                       For each contact pair we compute the relative normal and tan-
to a particular offset. Replacing 𝑑max by 𝑑target in Eqn.(25) and                         gential velocities at the contact point as
applying the correction unconditionally achieves this. Choosing a
compliance of 𝛼 = 1/ 𝑓 (|Δr| − 𝑑target ) applies a force 𝑓 .
   Joint handling shows the advantage of working on the positional                                         v ← (v1 + 𝜔1 × r1 ) − (v2 + 𝜔2 × r2 )
layer with the non-linear Gauss-Seidel approach. Unilateral con-                                          𝑣𝑛 ← n · v                                         (29)
straints are simply handled by applying corrections only when cer-                                        v𝑡 ← v − n 𝑣 𝑛 .
tain conditions hold. Also, the corrections are always aligned with
the current offsets and errors. In addition, attachments are handled                         The friction force is integrated explicitly by computing the ve-
with a single constraint instead of three in linearized solvers.                          locity update
                                                                                                                      v𝑡
                                                                                                           Δv ← −          min(ℎ 𝜇 𝑑 | 𝑓𝑛 |, |v𝑡 |),     (30)
3.5. Handling Contacts and Friction                                                                                  |v𝑡 |

To save computational cost we collect potential collision pairs                           where 𝜇 𝑑 is the dynamic friction coefficient and 𝑓𝑛 = 𝜆 𝑛 /ℎ2 the
once per time step instead of once per sub-step using a tree of                           normal force. This update corresponds to the explicit application of
axis aligned bounding boxes. We expand the boxes by a distance                            the dynamic Coulomb friction force. The explicit form in connec-
𝑘 Δ𝑡 𝑣 body , where 𝑘 ≥ 1 is a safety multiplier accounting for poten-                    tion with a Gauss-Seidel update allows us to make this step uncon-
tial accelerations during the time step. We use 𝑘 = 2 in our exam-                        ditionally stable! The minimum guarantees that the magnitude of
ples.                                                                                     the velocity correction never exceeds the magnitude of the velocity
                                                                                          itself.
   At each substep we iterate through the pairs checking for actual
collisions. If a collision occurs we compute the current contact nor-                       We also use the velocity pass to apply joint damping via
mal and the local contact positions r1 and r2 with respect to body                                           Δv ← (v2 − v1 ) min(𝜇lin ℎ, 1)                  (31)
1 and 2. We also initialize two Lagrange multipliers for the normal                                         Δ𝜔 ← (𝜔2 − 𝜔1 ) min(𝜇ang ℎ, 1).                  (32)
and tangential forces 𝜆 𝑛 and 𝜆 𝑡 with zero. To handle a contact dur-
ing the position solve we compute the contact positions on the two                          According to the derivation in the Appendix applying a velocity
bodies at the current state and before the substep integration as                         update Δv at positions r1 and r2 is achieved by the following steps:
                          p1 = x1 + q1 r1
                          p2 = x2 + q2 r2                                                                              Δv
                                                                                                                  p=
                                                                                   (26)                              𝑤1 + 𝑤2
                          p̄1 = x1,prev + q1,prev r1 and
                                                                                                                 v1 ← v1 + p/𝑚 1
                          p̄2 = x2,prev + q2,prev r2 ,                                                                                                       (33)
                                                                                                                 v2 ← v2 − p/𝑚 2
where the product of a quaternion and a vector refers to rotating
the vector using the quaternion. The current penetration can be                                                  𝝎1 ← 𝝎1 + I−1
                                                                                                                            1 (r1 × p)
computed as 𝑑 = (p1 − p2 ) · n. If 𝑑 ≤ 0 we skip the contact. The                                                𝝎2 ← 𝝎2 − I−1
                                                                                                                            2 (r2 × p).

 c 2020 The Author(s)
Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                 M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

 Example           substeps     iters/substep     time (ms/frame)
 3 Boxes               20              1                0.34
 7 Boxes               20              1                0.44
 Pendula               40              1           0.07, 0.09, 0.2
 Bunnies               20              1                 2.3
 Rolling balls         10              1                 15
 Coin                  20              1                 0.3
 Car                   20              1                 18
 Robot                 20              1                 0.4
 Rope                  20              1                 3.5

Table 1: Computation times. We used a simulation time step of
1/60s per frame in all cases.
                                                                               Figure 4: Our test application allows the visualization of forces,
                                                                               torques and elongations dynamically. Compliance, forces and elon-
                                                                               gation are in the correct relation independent of the substep and
   To handle restitution we also need 𝑣¯ 𝑛 , the normal velocity before        iteration counts.
the PBD velocity update. We compute this quantity by applying
Eqn 29 to the pre-update velocities. Given the restitution coeffi-
cient 𝑒 we want the normal velocity at the contact to be −𝑒 𝑣¯ 𝑛 . By
applying
                   Δv ← n(−𝑣 𝑛 + min(−𝑒 𝑣˜ 𝑛 , 0)),                  (34)
we subtract the current velocity 𝑣 𝑛 and replace it with the reflected
velocity −𝑒 𝑣¯ 𝑛 making sure that the resulting velocity points in the
direction of the collision normal. To avoid jittering we set 𝑒 = 0 if
|𝑣 𝑛 | is small. We use a threshold of |𝑣 𝑛 | ≤ 2|g|ℎ, where g is gravity.
This value corresponds to two times the velocity the prediction step           Figure 5: The yellow line shows a spring with a fixed compliance
adds due to gravitational acceleration.                                        that is attached to the mouse. This bar is attached on the left via
   This step also alleviates an important problem of PBD. The ve-              a hinge joint that has a target angle of zero with zero compliance.
locities created by the regular velocity update step of PBD are only           The joint applies the correct torque to hold the bar straight.
meaningful if no collisions have occured during the last time step.
Otherwise they simply reflect the penetration depth which is de-
pendent on the time discretization of the trajectory. Also, if objects
are created in an overlapped state, PBD yields large separating ve-            with zero compliance. It exerts the correct torque to counteract the
locities. Eqn (34) eliminates the derived velocity at an impact and            force that is applied by the user a distance of 20𝑐𝑚 away from
replaces it with the one from the previous time step considering the           the rotation center. With XPBD it is straightforward to specify an
restitution coefficient. In the case of initially overlapping objects,         infinitely stiff joint by setting the compliance to zero which is not
this velocity is zero.                                                         the case for force or impulse based systems.
                                                                                  Figure 6 shows an experiment with large mass ratios. A small
4. Results                                                                     box of one gram is attached to the static ceiling via a distance
                                                                               joint. Below it hangs a heavy box of one kilogram attached via an-
For our demos we used a system with a Core-i7 CPU at 3.6 GHz                   other distance joint. The experiment is duplicated with compliances
and 32 GB of RAM. Table 1 shows the simulation times per frame                 0.01, 0.001 and 0𝑚/𝑁. Our method handles this situation stably. In
for the various examples.                                                      the case of non-zero compliance, the distances are proportional to
   The capabilities and performance of our method are best seen in             the forces. In the case of zero compliance the distance remains zero
the accompanying video. We will first discuss a few basic technical            independent of the force. With 20 substeps a small error at the top
scenarios that we performed with our test application. The appli-              joint remains.
cation allows the visualization of forces, torques and elongations
                                                                                  In Figure 7 we show prismatic, hinge and ball-in-socket joint
at the joints. Figure 4 shows a set of boxes which are attached to
                                                                               with various joint limits and target angles and target offsets. With
the static ceiling via distance joints. All springs have compliance
                                                                               simple hinge joints it is possible to reproduce the behavior of a dou-
0.01𝑚/𝑁. The larger and smaller boxes have masses 1 and 1/8kg,
                                                                               ble, a triple and a closed loop pendulum as shown in Figure 8. The
respectively and we set gravity to 10𝑚/𝑠2 . The simulation yields
                                                                               typical chaotic motion only emerges with small time steps and a
the correct elongations and forces independent of the number of
                                                                               small amount of damping. With 40 substeps and one iteration the
iterations and sub-steps.
                                                                               pendula keep on swinging for a long time. Using 1 substep but an
   The same holds for joint torques. Figure 5 shows a bar that is              arbitrary number of solver iterations - 100 in our example - the pen-
attached via a hinge joint which has a target angle of zero degrees            dula come to rest very quickly. Figure 9 shows the evolution of the

                                                                                                                                                   c 2020 The Author(s)
                                                                                  Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                       M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics


                                                                                                                                                                 20 x 1
                                                                                                                                                                 10 x 2
                                                                                                                                                                 5x4
                                                                                                                                                                 2 x 10




                                                                                                 Energy
                                                                                                                                                                 1 x 20




                                                                                                                  0    1    2    3    4    5     6    7     8    9    10
                                                                                                                                          Time (s)


                                                                                         Figure 9: Energy conservation during the simulation of the triple
                                                                                         pendulum dependent on the number of substeps and solver itera-
                                                                                         tions.
Figure 6: Handling large mass ratios: A small box of 1 gram is
attached to the ceiling via a distance constraint and holds a box
of 1 kilogram via a second joint. The compliances of the joints are
from left to right 0.01, 0.001 and 0 m/N.




                                                                                         Figure 10: The simulation of a chain of 100 bunnies hanging from
                                                                                         the ceiling demonstrates the effectiveness of substepping. Left: 1
                                                                                         substep, 20 iterations, right: 20 substeps, 1 iteration.
Figure 7: With our method we can create a variety of joint types
with target angles and soft and hard joint limits.

                                                                                         energy during the simulation of the triple pendulum dependent on
                                                                                         the number of substeps and solver iterations. As discussed before,
                                                                                         the best choice is to replace all solver iterations by substeps.
                                                                                            To verify that this is the case for constraint errors as well, we
                                                                                         created a chain of 100 bunnies hanging from the ceiling as shown
                                                                                         in Figure 10. We tested a variety of substep and iteration count
                                                                                         combinations for a fixed time budget. Figure 11 shows the relative




                                                                                                                      30%
                                                                                                 Elongation (%)




                                                                                                                      20%
Figure 8: Substepping yields the correct behavior of the double                                                       10%
and triple pendula. We can easily simulate a closed loop pendulum
as well.                                                                                                              0%
                                                                                                                            20 x 1   10 x 2 5 x 4       2 x 10   1 x 20
                                                                                                                                      Substeps x Iterations

                                                                                         Figure 11: Elongation of the bunny chains dependent on the num-
                                                                                         ber of substeps and solver iterations


 c 2020 The Author(s)
Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                               M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics




Figure 12: From top to bottom: Initial condition, after the hit of
the red marble using our velocity pass and a restitution of 1 and
the state resulting from the regular PBD velocity derivation.

                                                                             Figure 14: In certain elements of the sculpture the marbles perform
                                                                             large turns in a single time step which requires the use of current
                                                                             constraint directions for each projection.




Figure 13: The marbles are created penetrating the wires. Top:
Regular PBD creates large velocities causing the marbles to jump
                                                                             Figure 15: With the ability of handling curved geometry and sub-
off the track. Bottom: The marbles are pushed up gently and remain
                                                                             stepping we are able to reproduce the high frequency motion of a
on the track.
                                                                             coin shortly before it comes to rest.


elongation of the chain for each case. Again, replacing all solver              The simulation of the remote controlled car demonstrates how
iterations by substeps is by far the best choice. The accompanying           our method handles the coupling of the soft body tires with the rigid
video shows the impressive difference in behavior.                           rims. It also shows how well sub-stepping handles large mass ratios.
   The velocity pass we described in Section 3.6 yields proper im-           We simulate the entire steering mechanism from servo to wheels as
pulse propagation as shown in Figure 12. Here a single marble hits           shown in Figure 16. The mass ration between the servo arm and the
a group of three marbles from the right. The impulse is correctly            wheels is 1:760. The servo arm is 3cm long while the wheels have
transferred to the right most marble as shown in the middle. The             a diameter of 15cm. Nevertheless, the servo motor is strong enough
bottom image shows the situation after the hit when using the ve-            to turn the big wheels at high speed against the obstacles and the
locity derivation of PBD.                                                    terrain. Using actual constraint directions is important because a
                                                                             remote controlled car experiences much higher accelerations and
   In the scene shown in Figure 13 the marbles penetrate the wires           changes in direction than a regular car. Our method also resolves
in the initial state. The velocity derivation of PBD yields large ve-        the high frequency vibrations giving the feel for the high stiffness
locities causing the marbles jumping off the track (top image) while         of the springs. The most expensive part is the simulation of the
they stay on the track with our method (bottom image).                       wheels. We have found that using FEM on tetrahedra did not yield
   We created two larger scenes tailored to demonstrate the advan-           the stiffness needed within the time budget. Instead, we perform
tages of our method: a rolling ball sculpture and a remote controlled
car travelling over bumpy terrain and obstacles shown in Figure 1.
   The rolling ball demo is an attempt to reproduce the fascinat-
ing sculptures of David Morell [Mor] including the clever mecha-
nisms in a simulation. In certain elements such as the spring shown
in Figure 14 the marbles perform a quarter turn in a single time
step. Simulating such fast curved motions requires substepping and
the use of current constraint normals for each projection. Here, the
most expensive part is collision handling, in particular finding the
closest point on a Hermite spline segment. Our method also allows            Figure 16: We simulate the steering mechanism from the small arm
us to reproduce the high frequency motion of a coin before it comes          at the servo to the big wheels with a mass ratio of 1:760.
to rest as shown in Figure 15.

                                                                                                                                                 c 2020 The Author(s)
                                                                                Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                       M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

                                                                                         conservation. It also allows the handling of large mass ratios and
                                                                                         fast directional changes within a single time step. We have shown
                                                                                         that two basic projection operations are sufficient to build a fully
                                                                                         fledged rigid body engine in a straightforward way. For snippets of
                                                                                         source code we refer the reader to our challenges page [Mue20].
                                                                                            A drawback of substepping is that it does not damp out high
                                                                                         frequency vibrations due to reduced numerical damping. This can
                                                                                         yield visual jittering. However, numerical damping can easily be
                                                                                         reintroduced by adding true physical damping. Also, for small time
                                                                                         steps, double precision floating point numbers are required. While
                                                                                         doubles are as fast as floats on CPUs, they currently still reduce the
                                                                                         performance on GPUs. Updating constraint directions after each
                                                                                         projection might cause instabilities when simulating tall stacks or
                                                                                         piles of objects. Investigating this problem is one of our directions
                                                                                         of future work.


                                                                                         References
Figure 17: Our method can be used to solve inverse kinematics                            [Bar93] BARAFF D.: Non-penetrating rigid body simulation. State of the
problems for overconstrained systems with possibly redundant de-                           art reports (1993). 3
grees of freedom such as this robot arm.                                                 [Bar97] BARAFF D.: An introduction to physically based modeling:
                                                                                           Rigid body simulation. In SIGGRAPH ’97 Course Notes (1997). 2
                                                                                         [BB04] B LOW J., B INSTOCK A.: How to find the inertia tensor (or other
                                                                                           mass properties) of a 3d solid body represented by a triangle mesh. 4
                                                                                         [BET14] B ENDER J., E RLEBEN K., T RINKLE J.:        Interac-
                                                                                           tive simulation of rigid body dynamics in computer graph-
                                                                                           ics. Computer Graphics Forum 33, 1 (2014), 246–270. URL:
                                                                                           https://onlinelibrary.wiley.com/doi/abs/10.1111/
                                                                                           cgf.12272, arXiv:https://onlinelibrary.wiley.com/
                                                                                           doi/pdf/10.1111/cgf.12272, doi:10.1111/cgf.12272.
                                                                                           3
                                                                                         [DBDB11] DAVIET G., B ERTAILS -D ESCOUBES F., B OISSIEUX L.: A
                                                                                           hybrid iterative solver for robustly capturing coulomb friction in hair dy-
                                                                                           namics. In ACM Transactions on Graphics (TOG) (2011), vol. 30, ACM,
Figure 18: The separate handling of swing and twist limits allows                          p. 139. 2
the simulation of a twisted rope.                                                        [DCB14] D EUL C., C HARRIER P., B ENDER J.: Position-based rigid
                                                                                           body dynamics. Computer Animation and Virtual Worlds 27, 2 (2014),
                                                                                           103–112.   URL: http://dx.doi.org/10.1002/cav.1614,
                                                                                           doi:10.1002/cav.1614. 2, 3
per element shape matching [MHTG05] on the 1100 hexahedral                               [Erl17] E RLEBEN K.: Rigid body contact problems using proximal op-
elements of the tires.                                                                      erators. In Proceedings of the ACM Symposium on Computer Animation
                                                                                            (2017), p. 13. 2
   Finally we created two scenarios to show the importance and
usefulness of joint limit handling. Figure 17 shows that our method                      [GCC∗ ] G ALVEZ J., C AVALIERI F. J., C OSIMO A., B RÜLS
                                                                                           O., C ARDONA A.:       A nonsmooth frictional contact formu-
can be used to solve the inverse kinematic problem to make the                             lation for multibody system dynamics.     International Jour-
robot gripper following the gray box while respecting all joint lim-                       nal for Numerical Methods in Engineering n/a, n/a.      URL:
its. Unreachable positions yield overconstrained problems which                            https://onlinelibrary.wiley.com/doi/abs/10.1002/
our method handles gracefully by moving the gripper as close as                            nme.6371, arXiv:https://onlinelibrary.wiley.com/
                                                                                           doi/pdf/10.1002/nme.6371, doi:10.1002/nme.6371. 3
possible to the target pose. Our method allows the user to spec-
ify independent limits on swing and twist degrees of freedom with                        [Hec97] H ECKER C.: The third dimension. Game Developer Mag-
                                                                                           azine (June 1997). URL: chrishecker.com/Rigid_Body_
different compliances. This allows us to simulate the twisted rope                         Dynamics. 2
shown in Figure 18 with the correct behavior as a simple chain of
                                                                                         [KSJP08] K AUFMAN D. M., S UEDA S., JAMES D. L., PAI D. K.: Stag-
100 capsules connected by spherical joints.                                                gered projections for frictional contact in multibody systems. In ACM
                                                                                           Transactions on Graphics (TOG) (2008), vol. 27, ACM, p. 164. 2
5. Conclusion                                                                            [MC95] M IRTICH B., C ANNY J.: Impulse-based simulation of rigid bod-
                                                                                           ies. In Proceedings of the 1995 Symposium on Interactive 3D Graphics
We have presented a rigid body simulation method than can ac-                              (New York, NY, USA, 1995), I3D ’95, Association for Computing Ma-
curately resolve small temporal and spatial detail. Because it is                          chinery, p. 181–ff. URL: https://doi.org/10.1145/199404.
based on XPBD, it inherits XPBD’s simplicity and ability to handle                         199436, doi:10.1145/199404.199436. 1
infinitely stiff joints. Substepping increases accuracy and energy                       [MC11]     M ÜLLER M., C HENTANEZ N.: Solid simulation with oriented

 c 2020 The Author(s)
Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
                                M. Müller et al. / Detailed Rigid Body Simulation with Extended Position Based Dynamics

  particles. ACM Trans. Graph. 30, 4 (July 2011). URL: https://doi.           [WSPJ17] WANG J.-H., S ETALURI R., PAI D. K., JAMES D. L.:
  org/10.1145/2010324.1964987, doi:10.1145/2010324.                             Bounce maps: An improved restitution model for real-time rigid-body
  1964987. 3                                                                    impact. ACM Transactions on Graphics (Proceedings of SIGGRAPH
[MEM∗ 19] M ACKLIN M., E RLEBEN K., M ÜLLER M., C HENTANEZ                      2017) 36, 4 (July 2017). doi:https://doi.org/10.1145/
  N., J ESCHKE S., M AKOVIYCHUK V.: Non-smooth newton methods                   3072959.3073634. 3
  for deformable multi-body dynamics. ACM Trans. Graph. 38, 5 (Oct.           [XZB14] X U H., Z HAO Y., BARBI Č J.: Implicit multibody penalty-
  2019). URL: https://doi.org/10.1145/3338695, doi:10.                          baseddistributed contact. IEEE Transactions on Visualization and Com-
  1145/3338695. 2                                                               puter Graphics 20, 9 (2014), 1266–1279. 3
[MHR06] M ÜLLER M., H ENNIX B. H. M., R ATCLIFF J.: Position based
  dynamics. Proceedings of Virtual Reality Interactions and Physical Sim-
  ulations (2006), 71–80. 2                                                   Appendix A: Appendix
[MHTG05] M ÜLLER M., H EIDELBERGER B., T ESCHNER M., G ROSS                   Derivation of the Position Based Updates
  M.:    Meshless deformations based on shape matching.   ACM
  Trans. Graph. 24, 3 (July 2005), 471–478. URL: https://doi.                 In impulse based rigid body solvers, impulses are applied to bodies
  org/10.1145/1073204.1073216, doi:10.1145/1073204.                           to change velocities at contact points. Let r be the vector from the
  1073216. 2, 11                                                              center of mass to the contact point. Applying an impulse p at the
[Mir96] M IRTICH B. V.: Impulse-based Dynamic Simulation of Rigid             contact point has two effects. It changes the velocity vcm of the
  Body Systems. PhD thesis, 1996. AAI9723116. 5                               center of mass and the angular velocity 𝜔 of the body via
[MM13] M ACKLIN M., M ÜLLER M.: Position based fluids. ACM Trans.
  Graph. 32, 4 (July 2013). URL: https://doi.org/10.1145/                                                           p = 𝑚 Δvcm                                   (35)
  2461912.2461984, doi:10.1145/2461912.2461984. 2                                                              r × p = I Δ𝜔,                                     (36)
[MMC16] M ACKLIN M., M ÜLLER M., C HENTANEZ N.:                  Xpbd:
  Position-based simulation of compliant constrained dynamics. In Pro-        where 𝑚 and I are the mass and the moment of inertia of the body,
  ceedings of the 9th International Conference on Motion in Games (New        respectively. The velocity at the contact point is
  York, NY, USA, 2016), MIG ’16, Association for Computing Machin-
  ery, p. 49–54. URL: https://doi.org/10.1145/2994258.                                                         v = vcm + 𝜔 × r.                                  (37)
  2994272, doi:10.1145/2994258.2994272. 2, 3
                                                                              Given the contact normal n we can express both the impulse and
[MMCK14] M ACKLIN M., M ÜLLER M., C HENTANEZ N., K IM T.-Y.:
                                                                              the velocity change along the normal as scalars and derive a rela-
  Unified particle physics for real-time applications. ACM Trans. Graph.
  33, 4 (July 2014). URL: https://doi.org/10.1145/2601097.                    tionship between the two as follows:
  2601152, doi:10.1145/2601097.2601152. 2
                                                                                               Δ𝑣 = [Δvcm + Δ𝜔 × r] · n                                          (38)
[MMM14] M ASARATI P., M ORANDINI M., M ANTEGAZZA P.: An Ef-                                         h                    i
  ficient Formulation for General-Purpose Multibody/Multiphysics Anal-                            = p 𝑚 −1 + I−1 (r × p) × r · n                                 (39)
  ysis. Journal of Computational and Nonlinear Dynamics 9, 4 (07                                      h                    i
  2014). 041001. URL: https://doi.org/10.1115/1.4025628,                                          = 𝑝 n 𝑚 −1 + I−1 (r × n) × r · n                               (40)
  doi:10.1115/1.4025628. 3
                                                                                                      h                              i
[Mor] M ORRELL D.: Rolling ball sculptures. URL: https://www.                                     = 𝑝 n · n 𝑚 −1 + I−1 (r × n) × r · n                           (41)
  rollingballsculpture.com.au. 10                                                                     h                           i
[MSL∗ 19] M ACKLIN M., S TOREY K., L U M., T ERDIMAN P., C HEN -                                  = 𝑝 𝑚 −1 + (r × n)𝑇 I−1 (r × n)                                (42)
  TANEZ N., J ESCHKE S., M ÜLLER M.: Small steps in physics simula-
  tion. In Proceedings of the 18th Annual ACM SIGGRAPH/Eurographics                                 = 𝑝 𝑤,                                                       (43)
  Symposium on Computer Animation (New York, NY, USA, 2019), SCA
  ’19, Association for Computing Machinery. URL: https://doi.                 where 𝑤 can be interpreted as a generalized inverse mass. Apply-
  org/10.1145/3309486.3340247, doi:10.1145/3309486.                           ing an impulse 𝑝 at the contact point between two bodies yields
  3340247. 3, 4                                                               a total velocity change of Δ𝑣 = Δ𝑣 1 + Δ𝑣 2 = 𝑝(𝑤 1 + 𝑤 2 ). In other
[Mue20] M UELLER M.: Web page, 2020. URL: matthiasmueller.                    words, we can change the velocity at the contact point by applying
  info/challenges/challenges.html. 11                                         an impulse 𝑝 = Δ𝑣/(𝑤 1 + 𝑤 2 ). Once the impulse is known, we can
[OCC77] O RLANDEA N., C HACE M. A., C ALAHAN D. A.: A sparsity-               compute the change of vcm and 𝜔 as via
  oriented approach to the dynamic analysis and design of mechanical sys-
  tems—part 1. 3                                                                                             Δvcm = p 𝑚 −1                                       (44)
[Rya90] RYAN R.: Adams—multibody system analysis software. In                                                            −1
                                                                                                                Δ𝜔 = I        (r × p).                           (45)
  Multibody systems handbook. Springer, 1990, pp. 361–402. 3
[ST96] S TEWART D. E., T RINKLE J. C.: An implicit time-stepping              To go from the velocity to the positional level, we conceptually
  scheme for rigid body dynamics with inelastic collisions and coulomb        multiply these equations by time. This turns the velocity correction
  friction. International Journal for Numerical Methods in Engineering        Δv into a positional correction Δx and the impulse into a quan-
  39, 15 (1996), 2673–2691. 2                                                 tity of the unit mass times distance. The definition of the general-
[Sta09] S TAM J.: Nucleus: Towards a unified dynamics solver for              ized mass is unchanged. The update of the velocity of the center of
   computer graphics. In Computer-Aided Design and Computer Graph-            mass turns into an update of the position of the center of mass. The
   ics, 2009. CAD/Graphics’ 09. 11th IEEE International Conference on
   (2009), IEEE, pp. 1–11. 2                                                  update of the angular velocity turns into a rotation. To apply the ro-
                                                                              tation to the orientations we use the linearized quaternion updates
[USS15] U METANI N., S CHMIDT R., S TAM J.: Position-based elastic
  rods. In Proceedings of the ACM SIGGRAPH/Eurographics Symposium             from Algorithm 2.
  on Computer Animation (Goslar, DEU, 2015), SCA ’14, Eurographics
  Association, p. 21–30. 3


                                                                                                                                                  c 2020 The Author(s)
                                                                                 Computer Graphics Forum c 2020 The Eurographics Association and John Wiley & Sons Ltd.
