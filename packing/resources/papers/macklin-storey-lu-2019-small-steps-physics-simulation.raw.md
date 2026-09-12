                                              Small Steps in Physics Simulation
                     Miles Macklin                                                     Kier Storey                                  Michelle Lu
                      NVIDIA                                                           NVIDIA                                          NVIDIA
             University of Copenhagen                                            kstorey@nvidia.com                             michellel@nvidia.com
              mmacklin@nvidia.com

                  Pierre Terdiman                                           Nuttapong Chentanez                                   Stefan Jeschke
                      NVIDIA                                                         NVIDIA                                            NVIDIA
               pterdiman@nvidia.com                                           nchentanez@nvidia.com                             sjeschke@nvidia.com

                                                                                  Matthias Müller
                                                                                     NVIDIA
                                                                              matthiasm@nvidia.com
ABSTRACT
In this paper we re-examine the idea that implicit integrators with
large time steps offer the best stability/performance trade-off for
stiff systems. We make the surprising observation that performing
a single large time step with n constraint solver iterations is less
effective than computing n smaller time steps, each with a single
constraint solver iteration. Based on this observation, our approach
is to split every visual time step into n substeps of length ∆t/n and
to perform a single iteration of extended position-based dynamics
(XPBD) in each such substep. When compared to a traditional
implicit integrator with large time steps we find constraint error and
damping are significantly reduced. When compared to an explicit
integrator we find that our method is more stable and robust for a
wider range of stiffness parameters. This result holds even when
compared against more sophisticated implicit solvers based on
Krylov methods. Our method is straightforward to implement, and                                 Figure 1: High resolution cloth consisting of 150k particles,
is not sensitive to matrix conditioning nor is it to overconstrained                            and 896k spring constraints draped over a Stanford bunny.
problems.                                                                                       With 1 substep and 30 XPBD iterations the simulation takes
                                                                                                12.4ms/frame but shows visible stretching (left). With 30
CCS CONCEPTS                                                                                    substeps, each performing only 1 XPBD iteration the simula-
• Computing methodologies → Simulation by animation; In-                                        tion takes 13.5ms/frame but shows significantly less stretch-
teractive simulation.                                                                           ing and higher material stiffness (right). In both cases we
                                                                                                have performed collision detection once per-frame.
KEYWORDS
Physics-based animation, real-time simulation
ACM Reference Format:
                                                                                                1    INTRODUCTION
Miles Macklin, Kier Storey, Michelle Lu, Pierre Terdiman, Nuttapong Chen-                       The simulation of physical systems is a challenging problem in
tanez, Stefan Jeschke, and Matthias Müller. 2019. Small Steps in Physics Sim-                   interactive computer graphics. Ideal algorithms should not only
ulation. In SCA ’19:The ACM SIGGRAPH / Eurographics Symposium on Com-                           reproduce the underlying physical model, they should be robust
puter Animation (SCA ’19), July 26–28, 2019, Los Angeles, CA, USA. ACM, New                     and efficient enough for real-time applications and user interaction.
York, NY, USA, Article 39, 7 pages. https://doi.org/10.1145/3309486.3340247                     Many methods exist to evolve a physical system forward in time,
                                                                                                however they can broadly be split into two categories: explicit and
Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed           implicit methods.
for profit or commercial advantage and that copies bear this notice and the full citation          Explicit time-integration is rarely used in physical simulations
on the first page. Copyrights for components of this work owned by others than the              because it is only conditionally stable. This means that the simula-
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
republish, to post on servers or to redistribute to lists, requires prior specific permission   tion can diverge any time if certain conditions are not met. For this
and/or a fee. Request permissions from permissions@acm.org.                                     reason, implicit integrators are often preferred due to their stability.
SCA ’19, July 26–28, 2019, Los Angeles, CA, USA                                                 However, in contrast to explicit integration, where the state of the
© 2019 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM ISBN 978-1-4503-6677-9/19/07. . . $15.00                                                    next time step can be computed directly from the current state, for
https://doi.org/10.1145/3309486.3340247                                                         implicit integration a system of non-linear equations must be solved
SCA ’19, July 26–28, 2019, Los Angeles, CA, USA           M. Macklin, K. Storey, M. Lu, P. Terdiman, N. Chentanez, S. Jeschke, and M. Müller


at every time step. Typically this is done using a Newton method           Table 1: Summary of the relative strengths and weaknesses
that repeatedly linearizes the non-linear system. Each linear sys-         of each method.
tem is then solved by a global solver such as Conjugate Gradients
(CG) or direct methods, and the solution is used to get closer to the        Method                Stability   Efficiency   Simplicity   Energy
non-linear one. First order implicit methods introduce numerical             Semi-Implicit Euler                    ✓          ✓           ✓
damping, and are often more computationally expensive than ex-               Implicit Euler           ✓
                                                                             XPBD                     ✓            ✓            ✓
plicit methods. In addition, they may not guarantee a time-bound
                                                                             Small Steps              ✓           ✓✓            ✓          ✓
on convergence, which makes them less attractive for interactive
applications.
    For real-time applications, local iterative relaxation methods
such as Position-based Dynamics (PBD) [Müller et al. 2007] are             performing a single iteration in each step. Based on this observation
popular. Unlike global solvers which treat the system of equations         we split a time step of size ∆t into n substeps of size ∆t/n and
as a whole, local solvers such as the Projected Gauss-Seidel (PGS)         perform one iteration of Extended Position Based Dynamics (XPBD)
iteration used in PBD handle each equation individually, one after         in each substep. The effect of replacing iterations by substeps is so
the other. These methods are known to be very robust on typical            substantial that one-step XPBD is competitive with sophisticated
problems. This is due in part to the fact that during a global solve the   global matrix solvers in terms of convergence. Intuitively, a single
system matrix is frozen, meaning all constraint gradients are held         pass over the constraints seems hardly enough to yield meaningful
fixed. This can cause the solution to move far from the constraint         information about forces and torques, but our results show that
manifold. In contrast, non-linear PGS methods work on the system           this is actually not the case. Indeed, as was shown by Macklin et
of non-linear equations directly. Each constraint projection uses          al [2016], the first iteration of XPBD is equivalent to the first step
the current gradients, which minimizes overshooting. In addition,          of a Newton solver operating on the backward Euler equations.
relaxation methods are robust for overconstrained systems that pose        Thus, while our single iteration method has a close computational
a challenge for global linear solvers, which may fail to converge at       resemblance to explicit integration, it comes with all the stability
all in such scenarios. Furthermore, solving each equation separately       properties of an implicit method.
allows PGS to trivially handle unilateral (inequality) constraints.           It is common in computer graphics literature to compare ex-
Here, only constraints which violate the inequality conditions (the        plicit integration with small time steps against implicit integration
active set) are projected. This set can change in every iteration and      with large time steps. But we are not aware of works that explore
even after each constraint projection, which prevents sticking. To         the middle-ground: approximate implicit integration with small
simulate the two-way coupling of different features like liquids and       time steps. The contributions of this work are a new approach to
rigid bodies, their list of constraints are simply concatenated or         simulation, but more importantly, a study on the effectiveness of de-
interleaved, allowing fine-grained coupling [Macklin et al. 2014;          creasing the time step size and the investigation of single iteration
Stam 2009].                                                                implicit integration.
    Despite their advantages, due to their local nature, relaxation           In Table 1 we broadly summarize these trade-offs. Explicit meth-
methods propagate error corrections more slowly than if the equa-          ods are simple, and can be efficient for moderately stiff problems.
tions are solved simultaneously, making them less suitable for stiff       Traditional implicit methods such as backwards Euler are stable, but
problems. They also suffer from numerical dissipation like tradi-          have poor energy conservation, and are generally more expensive.
tional implicit methods. The aim of this project was to increase the       Iterative implicit methods like XPBD are stable, and efficient for
convergence rate and energy preservation of local solvers while            moderate stiffness, however they struggle to achieve high stiffness,
keeping all their advantages. We derived our solution from a rather        and also suffer from numerical damping. Our proposed method im-
surprising observation. There are two ways to increase the accuracy        proves the convergence and energy preservation of XPBD through
of a simulation: either decrease the time step size, or increase the       a simple modification of the underlying algorithm.
number of solver iterations. Both increase the amount of computa-
tional work that has to be done. Consequently, if we want to keep          2    RELATED WORK
the work constant we have to change both. If we decide to increase         The use of implicit integration for forward dynamics in computer
the number of solver iterations or the complexity of the solver,           graphics dates back to a seminal work by Terzopoulos et al. [1988;
we have to increase the time step size to stay within the computa-         1987]. They utilize the alternating-direction implicit (ADI) method
tional budget. On the other hand, if we decide to take smaller time        [Peaceman and Rachford 1955] to solve some of the forces implic-
steps, then we have to decrease the number of solver iterations.           itly. Since that time, the use of explicit integration became popular
The question we asked was which direction is more effective. Is it         until Baraff and Witkin [1998] proposed a implicit backward Euler
more effective to (a) solve one difficult problem accurately, or (b)       scheme for handling all the forces implicitly, including damping
many simpler problems approximately. Since the work of Baraff              in cloth simulation. This provides a method that is stable even for
et al. [1998], the commonly accepted knowledge in the computer             large time step sizes. Desbrun et al. [1999] sped up the computation
graphics community has been to prefer large steps and implicit             by using a predictor-corrector approach to compute an approxi-
methods for stiff problems.                                                mate solution to implicit integration. These approaches, however,
    However, in our studies we found that (b) is significantly more        suffer from artificial numerical damping. A second-order backward
effective than (a). In fact, for PGS the optimum lies at the far end of    difference formula (BDF) was used for cloth simulation in [Choi and
(b), i.e. taking as many small steps as the time budget allows while       Ko 2002] to reduce this numerical damping. Bridson et al. [2003]
Small Steps in Physics Simulation                                                             SCA ’19, July 26–28, 2019, Los Angeles, CA, USA


demonstrated the use of mixed implicit/explicit integration (IMEX)        position x̃ is obtained by an explicit integration of external forces:
for cloth simulation. They used explicit integration for treating the                       x̃ ⇐ xn + ∆tvn + ∆t 2 M−1 fex t (xn ).            (3)
elastic force and implicit integration for damping forces, yielding
a central Newmark scheme [Newmark 1959]. Along with the use                  Examining equation (3), we make the observation that the effect
of strain limiting, the method is stable for moderate time step size      of external forces on positions is proportional to ∆t 2 . This is due
and does not suffer much from numerical damping. An IMEX type             to the discretization of a second order differential equation, and it
method was also used for a particle system simulation in [Eber-           has a strong influence on the error committed in a single step. For
hardt et al. 2000]. Fierz et al. [2011] combined the use of explicit      example, halving the time step will result in a quarter of the position
and implicit integrators using element-wise criteria. In all these        error, and so on. This simple fact is what motivates our method,
works, the use of an implicit integrator that requires a global linear    and makes smaller time steps so effective at reducing positional
solver is commonplace.                                                    error, as we show in Section 6.
   Variational approaches can also be used to derive integrators
                                                                          Algorithm 1 Substep XPBD simulation loop
[Kane et al. 2000; Kharevych et al. 2006; Marsden and West 2001]
with excellent energy preservation and controlled damping. De-                1: perform collision detection using xn , vn
                                                                                          ∆t f
pending on the quadrature rule used for converting the continuous             2: ∆ts ⇐ n
                                                                                         s t eps
Langrangian to a discrete version, one can arrive at explicit or im-          3: while n < nst eps do
plicit integration of varying orders of accuracy. While energy is             4:   predict position x̃ ⇐ xn + ∆ts vn + ∆ts2 M−1 fex t (xn )
stable, the resulting animation can still oscillate and produce un-           5:   for all constraints do
natural high frequency vibration. The trade-offs between explicit             6:  compute ∆λ using Eq (7)
and implicit integration still apply. Another interesting alternative         7:  compute ∆x using Eq (4)
is an exponential integrator [Michels et al. 2014] that combines an        8:     update λn+1 ⇐ ∆λ (optional)
analytic solution of the linear part of the ODE with a numerical           9:     update xn+1 ⇐ ∆x + x̃
method for the nonlinear parts. However, as with all integrators          10:   end for
stability is only guaranteed in the linear regime.                        11:   update velocities vn+1 ⇐ ∆t1s xn+1 − xn
                                                                                                                        
   Projective Dynamics [Bouaziz et al. 2014] produces impressive          12:   n ⇐n+1
real time simulation results by combining local and global solves.        13: end while
Recently Dinev et al. [2018] proposed an energy control strategy          14:
for Projective Dynamics by mixing implicit midpoint with either
forward Euler or Backward Euler. Nonetheless, the global solve step
needs to pre-factorize the system matrix to be fast, which prevents
                                                                          4        CONSTRAINT SOLVE
simulated meshes from changing topology at runtime, for example.
   Asynchronous integrators [Lew et al. 2003; Thomaszewski et al.         To enforce the constraints on the system coordinates we use XPBD
2008] and contact handling [Harmon et al. 2009; Zhao et al. 2016] al-     [Macklin et al. 2016] which performs a position projection for a
low for varying the time step over the simulation domain. However,        constraint with index i as follows,
the required computation can fluctuate greatly over time, which is
not desirable in real-time simulations.                                                          ∆x = M−1 ∇Ci (x)T ∆λi .                   (4)
   The usefulness of a single Newton solver step over explicit in-             Where the associated Lagrange multiplier increment is given by,
tegration was also reported in [Gast et al. 2015], but they did not
                                                                                                        −Ci (x) − α̃ i λi
explore utilizing this observation further. The idea of using the                                ∆λi =                    .                (5)
predicted state in the next time step for force computation similar                                   ∇Ci M−1 ∇CiT + α̃ i
to an implicit integrator is also used in the context of PD controller       Position-based dynamics would typically repeat this update mul-
in [Tan et al. 2011], resulting in a more stable simulation.              tiple times per-constraint in a Gauss-Seidel or Jacobi fashion. Our
                                                                          idea is to instead divide the whole frame’s time step ∆t f into n
3   TIME INTEGRATION                                                      substeps,
                                                                                                             ∆t f
We write our equations of motion using an implicit position-level                                    ∆ts =         ,                       (6)
time discretization as follows:                                                                            nst eps
                                                                             and then perform a single constraint iteration for that substep.
               M(xn+1 − x̃) − ∇C(xn+1 )T λn+1 = 0                  (1)    This can be thought of as an approximate, or inexact implicit solve
                              C(xn+1 ) + α̃ λn+1 = 0.              (2)    for each substep. However, by dividing the time-step we benefit
                                                                          from the dependence of position error on ∆t 2 in the discrete equa-
   Here M is the system mass matrix and xn+1 is the system state          tions of motion.
at the end of the nth time step. C is a vector of constraint functions,      Since we perform a single iteration per-substep and the initial
∇C it’s gradient with respect to system coordinates, and λn+1 the         Lagrange multiplier is always zero, the numerator in (5), can be
associated Lagrange multipliers. Constraints are regularized with         simplified as follows:
a compliance matrix α̃ that results from factorizing a quadratic                              ∆λi =
                                                                                                          −Ci (x)
                                                                                                                         .                (7)
energy potential [Macklin et al. 2016]. The predicted or inertial                                    ∇Ci M−1 ∇CiT + α̃ i
SCA ’19, July 26–28, 2019, Los Angeles, CA, USA             M. Macklin, K. Storey, M. Lu, P. Terdiman, N. Chentanez, S. Jeschke, and M. Müller

                                                                                   0                                                                             0



                                                                                                                                                               -50
                                                                               -0.05


                                                                                                                                                              -100
                                                                                -0.1

                                                                                                                                                              -150

                                                                               -0.15

                                                                                                                                                              -200

                                                                                -0.2
                                                                                                                                                              -250


                                                                               -0.25
                                                                                                                                                              -300
                                                                                                                                      10 iters                                                                     100 iters
                                                                                                                                      10 substeps                                                                  100 substeps
                                                                                -0.3                                                                          -350
                                                                                       0   100   200   300   400   500   600   700   800     900    1000             0   100   200   300   400   500   600   700   800   900      1000




                                                                             Figure 3: Left: The stretch in a 1D chain of particles con-
                                                                             nected by distance constraints hanging under gravity. Sub-
                                                                             steps (red) are significantly more effective at reducing
                                                                             stretch than the equivalent number of iterations (blue).
                                                                             Right: The same test with a large mass (105 kg) attached to
                                                                             the bottom of the chain, emphasizing the effect.

Figure 2: A position-based fluid simulation consisting of                      10 1                                                                           240


936k particles. Using 10 iterations the fluid shows signifi-                   10 0
                                                                                                                                                              220



cant compression and highly damped motion. In contrast,                                                                                                       200

                                                                               10 -1
substepping with 10 iterations results in a visibly stiffer                                                                                                   180



fluid with more dynamic motion.                                                10 -2
                                                                                                                                                              160


                                                                               10 -3
                                                                                                                                                              140


                                                                               10 -4
                                                                                                                                           Iterations         120                                                  100 Iterations
                                                                                                                                           Substeps                                                                100 Substeps
                                                                               10 -5
                                                                                       0   20    40    60    80    100   120   140   160      180       200         0    10    20    30    40    50    60    70    80     90        100
When using a single iteration per-step it is not required to store the
Lagrange multipliers, however they can be useful to provide force
estimates back to the user. In the results section we demonstrate that       Figure 4: Left: We plot the residual error at frame 1000 for
these force estimates remain accurate even when using only a single          varying iteration and substep counts. We see approximately
iteration per substep (Figure 4). An overview of our simulation loop         two orders of magnitude lower error for the equivalent num-
is given in Algorithm 1.                                                     ber of substeps. Right: We plot the force estimate (Lagrange
                                                                             multiplier) for the constraint at the top of the chain over
4.1    Damping                                                               time. The true value is 190N. Surprisingly, even performing
                                                                             a single iteration per-substep provides accurate force esti-
Reducing the time step reduces the amount of numerical dissipation
                                                                             mates.
in the integrator. For this reason it becomes important to explicitly
include damping in our constraint model. We do this using the
XPBD formulation:                                                               Performing one collision detection phase per-frame could result
                                                                             in missed collisions due to changing trajectories. Missed collisions
                         −Ci (x) − γi ∇Ci (x − xn )                          would then be processed the next frame, however to minimize this
                 ∆λi =                                  .           (8)
                         (1 + γi )∇Ci M−1 ∇CiT + α̃ i                        effect we generate contacts between features that come within some
                                                                             user-controlled margin distance. This could be further addressed by
   Given β˜i = ∆ts2 βi , a time step scaled damping parameter for
                                                                             updating the contact set in a manner similar to constraint manifold
                                       α̃ β˜
constraint i, we then define γi = ∆t  i i
                                        s
                                          . We refer the reader to           refinement (CMR) [Otaduy et al. 2009].
publications by Macklin et al. [2016], and Servin et al. [2006] for
the derivation.                                                              4.3                Contact
                                                                             We treat contacts as inelastic and prevent interpenetration between
4.2    Collision Detection                                                   bodies through inequality constraints of the form
Decreasing time step size typically improves the accuracy of colli-
                                                                                                                     Cn (x) = nT [a(x) − b(x)] ≥ 0.                                                                            (9)
sion detection. However, performing collision detection every time
step adds a significant computational overhead. A key idea that                  Here a and b are points on a rigid or deformable body and n ∈ R3
makes our substepping approach feasible is to amortize this cost             is the contact plane normal. The contact normal may be fixed in
by performing collision detection once per-frame and re-using the            world space, or may itself be a function of the system coordinates.
contact set over multiple substeps. To do this, we first predict the             One artifact of reducing the time step is that any initial pene-
state of the system using the current velocity and the whole frame’s         tration error between bodies will be converted to large separating
time step, ∆t f . We use this trajectory to detect potential collisions      velocities by our implicit solve. A solution to this problem is the pre-
and generate contact constraints accordingly.                                stabilization pass proposed by Macklin et al. [2014], which removes
Small Steps in Physics Simulation                                                                 SCA ’19, July 26–28, 2019, Los Angeles, CA, USA


initial overlap by projecting out bodies in a kinematic fashion. Here
we propose a simpler method specifically for contacts.
   Given a contact with an initial overlap d 0 at the start of the time
step, an implicit solver aims to find a velocity that will completely
remove this penetration over the course of one substep. This leads to
                                  d0
a separating velocity of vsep = ∆t  s
                                      . As the time step is reduced, sep-
arating velocities are increased, leading to artificial elastic popping
artifacts. To avoid such excessive velocities we limit the maximum
depenetration speed in any given substep by modifying the contact
constraint as follows:

      Cn (x) = nT [a(x) − b(x)] + max(d 0 − vmax ∆ts , 0) ≥ 0.      (10)
                                                                            Figure 5: Simple hanging sheets of cloth with stiffness of
   Here vmax is the maximum separating speed that we wish to                k = 107 N/m. Left: XPBD 1 substep, 40 iterations, Middle:
allow in one substep. When vmax is large we allow the bodies to             XPBD 40 substeps, 1 iteration, Right: Semi-Implicit Euler 40
separate explosively. Conversely, if vmax is small, then penetrating        substeps. Unlike explicit methods our approach remains sta-
bodies will be gently separated. This is similar to the clamped             ble even for high stiffness coefficients.
normal impulses used by Bridson et al. [2003]. However we note
that when there is no initial penetration, i.e.: d 0 = 0, our formulation
automatically treats contacts as hard inequality constraints.                               104
                                                                                    4
                                                                                                                               40 Iterations
4.4      Friction                                                                   3                                          40 Substeps
We formulate frictional attachment constraints as follows:
                    C f (x) = DT [a(x) − b(x)] = 0                  (11)            2

where D is a 1-2 dimensional frictional basis matrix. To satisfy
                                                                                    1
Coulomb’s law that the frictional force should be limited by the
normal force we clamp the frictional Lagrange multiplier updates
                                                                                    0
as follows:                                                                             0                500            1000               1500

                       ∆λ f ← min(µ∆λn , ∆λ f )                     (12)
   where λn , λ f are the normal and frictional Lagrange multipli-          Figure 6: A plot of the system energy (gravitational + ki-
ers, and µ the friction coefficient. This projection implicitly cap-        netic) for the hanging cloth example. Reducing the time-
tures stick/slip transitions and ensures the frictional force is always     step significantly reduces damping due to the implicit time-
bounded by the scaled normal force.                                         discretization, resulting in more dynamic motion.

5     COMPARISON TO EXPLICIT METHODS
Computationally, our method bears a lot of resemblance to an ex-            with mass m = 1kg, connected by inextensible distance constraints
plicit time-integration scheme. However, because we derive our              with rest length of l = 0.01m hanging under gravity. We use the
method from an implicit time-discretization we obtain the benefit           position of the bottom particle as a measure of error and plot its
of stability even with large stiffness values. This robustness is cru-      value in Figure 3. A modification of this experiment is to attach
cial for real-time or interactive applications, and makes authoring         a large mass to the bottom of the chain, which is a stress test for
simulation assets considerably easier. Even with infinite stiffness         most iterative methods. We attach a particle such that the total
(zero compliance) our method is stable, and will behave as stiff as         mass ratio is 1 : 100000. In this case, the maximum error with 100
possible given the total number of substeps.                                iterations is e = 322.1m, the equivalent error with 100 substeps is
                                                                            e = 3.2m. This two orders of magnitude reduction in error is in
6     RESULTS                                                               line with our prediction of quadratic error reduction with respect
For our 3D examples we have implemented our method in CUDA                  to time step size.
and run it on an NVIDIA RTX 2080 Ti GPU. We use a parallel Jacobi
iteration over constraints. Since our focus is on real-time simulation      6.2    Cloth
we have used a fixed iteration count for most examples. This is             We test our method on the common scenario of a piece of cloth hang-
common in interactive settings where computational budgets are              ing under gravity. Iterative solvers typically struggle to maintain
fixed and should not vary from frame to frame.                              stiffness and reduce stretching. Many methods have been proposed
                                                                            to address this specific problem [Goldenthal et al. 2007; Kim et al.
6.1      Hanging Chain                                                      2012; Müller 2008; Müller et al. 2012], often with non-physical ar-
We use a 1D example to analyze the effect of time step size on              tifacts. In Figure 5 we see the effect of substeps compared with
constraint error. Specifically we look at a chain of 20 particles each      iterations on the hanging cloth. Despite being computationally
SCA ’19, July 26–28, 2019, Los Angeles, CA, USA            M. Macklin, K. Storey, M. Lu, P. Terdiman, N. Chentanez, S. Jeschke, and M. Müller




Figure 7: A cantilever beam consisting of 12800 tetrahedral
FEM elements with Young’s modulus of 107 Pa and Pois-
son’s ratio of 0.45. Left: XPBD 1 substep, 100 iterations, Mid-
dle: XPBD 100 substeps, 1 iteration, Right: Backwards Euler
(PCG): 1 substep, 100 iterations. Timings for each method
are 4ms, 6ms, and 12ms per-frame respectively. Substepping
provides a stiffness comparable to more complex methods
                                                                            Figure 8: A chain of rigid bodies with a suspended weight
with less damping, and lower computational cost.
                                                                            creating a mass ratio of 1:1000. Left: 1 substep and 100 iter-
                                                                            ations takes 4ms/frame and shows visible joint separation.
                                                                            Middle: 1 substep and 500 iterations takes 17ms/frame and
similar, using smaller time steps shows significantly less stretch-         still shows visible stretching. Right: 100 substeps and 1 iter-
ing, and better energy preservation compared to higher iteration            ation takes 6ms/frame and the chain is stiff and stable.
counts (Figure 6). In addition, we compare this scenario to a simple
semi-implicit integration scheme which evaluates spring forces
explicitly. We find our approximate implicit scheme to be robust
for large stiffness values, even in the limit of infinite stiffness (zero
compliance), while semi-implicit Euler quickly diverges.
   From a performance perspective, the amount of work done per-
iteration in all approaches is quite similar. There is a small overhead
to performing time-integration per-substep, but this is relatively
small compared to the work done during constraint solving. For
the cloth example per-frame simulation time is 1.8ms for XPBD
with 40 iterations, 2.4ms for XPBD with 40 substeps, and 2.5ms for
semi-implicit Euler.
                                                                            Figure 9: A heavy box resting on a stack of capsules. With 1
6.3    FEM                                                                  substep and 100 iterations the stack quickly collapses (left).
To test the effect of time step size on deformable bodies we simulate       With 100 substeps and 1 iteration the stack remains stable
a cantilever beam hanging under gravity. The beam consists of               (right). In both examples we have performed collision detec-
12800 tetrahedral FEM elements and a linear constitutive model              tion only once per frame.
with Young’s modulus of Y = 107 Pa, Poisson’s ratio of µ = 0.45, and
a density of ρ = 1000kg/m3 . As illustrated in Figure 7, when using
large time steps and many iterations we see significant deformation         we restrict the particles to not move farther than 0.3 times their
causing the beam to collapse to the ground. In contrast, with the           radius per time step (CFL condition). With sub-stepping, the time
equivalent number of substeps the beam supports itself. We also             steps are so small that no visual damping is introduced. There are
compare this example to a linearly implicit Newton method with a            no particle crossings and the fluid comes to complete rest. With
Krylov PCG solver (using a diagonal Jacobi preconditioner) applied          large time steps, a large amount of damping and instabilities are
directly to equations (1)-(2). Our substep method achieves similar          introduced. Relaxing the CFL condition yields disturbing particle
stiffness with significantly less numerical damping. The per-frame          crossings. In Figure 2 we create a 3D column of fluid with rest
simulation time is 4ms for 100 XPBD iterations, 6ms for 100 XPBD            density ρ = 1000kg/m3 consisting of 936k particles, and simulate
substeps, and 12ms for 100 PCG iterations.                                  its collapse under gravity inside a container. Using 10 iterations of
                                                                            the PBF density constraint solver fails to enforce incompressibility,
6.4    Fluids                                                               resulting in significant volume loss. Using 10 substeps, each with a
We test our approach on a particle-based fluid simulation using             single PBF iteration yields a stiffer response, and allows us to use a
Position-based Fluids (PBF) [Macklin and Müller 2013]. In the ac-           larger CFL condition, resulting in more dynamic motion.
companying video we demonstrate the effectiveness of sub-stepping
in a 2D fluid scene. The scene is a stress case for any particle based      6.5    Rigid Bodies
fluid solver because of the water depth (over a hundred particle            In Figure 8 we examine the effect of substeps on a heavy weight
layers) and the velocity of the incoming particles. To make it stable       being suspended by jointed rigid bodies. We observe a similar effect
Small Steps in Physics Simulation                                                                               SCA ’19, July 26–28, 2019, Los Angeles, CA, USA


to that seen in the cloth example, with reduced stretching, and more                     Mathieu Desbrun, Peter Schröder, and Alan Barr. 1999. Interactive Animation of
robust handling of angular degrees of freedom.                                               Structured Deformable Objects. In Proceedings of the 1999 Conference on Graphics
                                                                                             Interface ’99. Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 1–8.
   In Figure 9 we test a rigid body contact example with a large                         Dimitar Dinev, Tiantian Liu, and Ladislav Kavan. 2018. Stabilizing Integrators for
mass being held up by a stack of rigid body capsules. This is a                              Real-Time Physics. ACM Transactions on Graphics (TOG) 37, 1 (2018), 9.
                                                                                         B. Eberhardt, O. Etzmuß, and M. Hauth. 2000. Implicit-Explicit Schemes for Fast
stress test for iterative methods. With substeps we see the stack is                         Animation with Particle Systems. In In Eurographics Computer Animation and
stiff and remains stable with little interpenetration. On the other                          Simulation Workshop. Springer-Verlag, 137–151.
hand, using one substep and multiple iterations results in significant                   Basil Fierz, Jonas Spillmann, and Matthias Harders. 2011. Element-wise mixed implicit-
                                                                                             explicit integration for stable dynamic simulation of deformable objects. In Proceed-
interpenetration, quickly leading to the stack collapsing.                                   ings of the 2011 ACM SIGGRAPH/Eurographics Symposium on Computer Animation.
                                                                                             ACM, 257–266.
                                                                                         T. F. Gast, C. Schroeder, A. Stomakhin, C. Jiang, and J. M. Teran. 2015. Optimization
7    LIMITATIONS AND FUTURE WORK                                                             Integrator for Large Time Steps. IEEE Transactions on Visualization and Computer
We have demonstrated that time step size reduction is an effective                           Graphics 21, 10 (Oct 2015), 1103–1115.
                                                                                         Rony Goldenthal, David Harmon, Raanan Fattal, Michel Bercovier, and Eitan Grinspun.
method for reducing positional error in dynamics. However, the                               2007. Efficient simulation of inextensible cloth. In ACM Transactions on Graphics
same is not true for velocity dependent terms, e.g.: damping forces.                         (TOG), Vol. 26. ACM, 49.
                                                                                         David Harmon, Etienne Vouga, Breannan Smith, Rasmus Tamstorf, and Eitan Grinspun.
This is explained by the fact that velocity error is proportional                            2009. Asynchronous contact mechanics. SIGGRAPH ’09 (ACM Transactions on
only to ∆t in our equations of motion. For many scenarios error on                           Graphics).
velocity is more acceptable, however for situations where this is                        C. Kane, J. E. Marsden, M. Ortiz, and M. West. 2000. Variational integrators and the
                                                                                             Newmark algorithm for conservative and dissipative mechanical systems. Internat.
not true, e.g.: highly viscous materials, it may be advisable to use                         J. Numer. Methods Engrg. 49, 10 (2000), 1295–1325.
an accurate implicit solve on the velocity terms as a post-process                       Liliya Kharevych, Weiwei Yang, Yiying Tong, Eva Kanso, Jerrold E Marsden, Peter
after positional constraints are solved.                                                     Schröder, and Matthieu Desbrun. 2006. Geometric, variational integrators for
                                                                                             computer animation. In Proceedings of the 2006 ACM SIGGRAPH/Eurographics sym-
   Our method also works with Gauss-Seidel iteration, however, as                            posium on Computer animation. Eurographics Association, 43–51.
with most Gauss-Seidel methods the residual has some dependence                          Tae-Yong Kim, Nuttapong Chentanez, and Matthias Müller-Fischer. 2012. Long range
                                                                                             attachments-a method to simulate inextensible clothing in computer games. In
on the iteration order. In practice we have not found this to be a                           Proceedings of the ACM SIGGRAPH/Eurographics Symposium on Computer Animation.
significant issue, however a symmetric successive over-relaxation                            Eurographics Association, 305–310.
scheme (SSOR) could also be applied to mitigate this effect.                             A. Lew, J. E. Marsden, M. Ortiz, and M. West. 2003. Asynchronous Variational Integra-
                                                                                             tors. Archive for Rational Mechanics and Analysis 167, 2 (01 Apr 2003), 85–146.
   Another issue we have observed is that due to the ∆t 2 term we                        Miles Macklin and Matthias Müller. 2013. Position Based Fluids. ACM Trans. Graph.
can run into the limits of single precision floating point after some                        32, 4, Article 104 (July 2013), 12 pages.
number of substeps. This depends on the magnitude of the system                          Miles Macklin, Matthias Müller, and Nuttapong Chentanez. 2016. XPBD: position-
                                                                                             based simulation of compliant constrained dynamics. In Proceedings of the 9th
coordinates, e.g.: adding a small position delta to a large coordinate                       International Conference on Motion in Games. ACM, 49–54.
may result in no change in a finite representation. All our examples                     Miles Macklin, Matthias Müller, Nuttapong Chentanez, and Tae-Yong Kim. 2014. Uni-
                                                                                             fied particle physics for real-time applications. ACM Transactions on Graphics (TOG)
have used 32-bit floating point, however for higher iteration counts                         33, 4 (2014), 153.
using a double precision representation may be necessary.                                J. E. Marsden and M. West. 2001. Discrete mechanics and variational integrators. Acta
                                                                                             Numerica 10 (2001), 357–514.
                                                                                         Dominik L. Michels, Gerrit A. Sobottka, and Andreas G. Weber. 2014. Exponential
8    CONCLUSIONS                                                                             Integrators for Stiff Elastodynamic Problems. ACM Trans. Graph. 33, 1, Article 7
                                                                                             (Feb. 2014), 20 pages.
In this work we found that using many constraint solver iterations                       Matthias Müller. 2008. Hierarchical position based dynamics. (2008).
over large time steps to be inferior when compared to our approx-                        Matthias Müller, Bruno Heidelberger, Marcus Hennix, and John Ratcliff. 2007. Position
imate implicit integration over small time steps. Our method has                             based dynamics. J. Vis. Comun. Image Represent. 18, 2 (April 2007), 109–118.
                                                                                         Matthias Müller, Tae-Yong Kim, and Nuttapong Chentanez. 2012. Fast Simulation of
a low computational overhead, but provides a dramatic improve-                               Inextensible Hair and Fur. VRIPHYS 12 (2012), 39–44.
ment in achievable stiffness. This is a direct result of the positional                  N.M. Newmark. 1959. A Method of Computation for Structural Dynamics. Vol. 85.
error from external forces being dependent on the squared time                               American Society of Civil Engineers. 67–94 pages.
                                                                                         Miguel A Otaduy, Rasmus Tamstorf, Denis Steinemann, and Markus Gross. 2009.
step ∆t 2 . This relationship means reducing time step size gives                            Implicit contact handling for deformable objects. In Computer Graphics Forum,
quadratic error reduction with low complexity, making it an attrac-                          Vol. 28. Wiley Online Library, 559–568.
                                                                                         D. Peaceman and H. Rachford, Jr. 1955. The Numerical Solution of Parabolic and
tive alternative to traditional implicit integrators. Our result holds                       Elliptic Differential Equations. J. Soc. Indust. Appl. Math. 3, 1 (1955), 28–41.
over a diverse range of multibody and deformable body scenarios,                         Martin Servin, Claude Lacoursiere, and Niklas Melin. 2006. Interactive simulation of
and given its simplicity we believe it will be a valuable tool for                           elastic deformable materials. In Proceedings of SIGRAD Conference. 22–32.
                                                                                         Jos Stam. 2009. Nucleus: Towards a unified dynamics solver for computer graphics. In
practitioners.                                                                               Computer-Aided Design and Computer Graphics, 2009. CAD/Graphics’ 09. 11th IEEE
                                                                                             International Conference on. IEEE, 1–11.
                                                                                         Jie Tan, Karen Liu, and Greg Turk. 2011. Stable Proportional-Derivative Controllers.
REFERENCES                                                                                   IEEE Comput. Graph. Appl. 31, 4 (2011), 34–44.
David Baraff and Andrew Witkin. 1998. Large steps in cloth simulation. In Proceedings    Demetri Terzopoulos and Kurt Fleischer. 1988. Deformable models. The Visual Com-
   of the 25th annual conference on Computer graphics and interactive techniques. ACM,       puter 4, 6 (01 Nov 1988), 306–331.
   43–54.                                                                                Demetri Terzopoulos, John Platt, Alan Barr, and Kurt Fleischer. 1987. Elastically
Sofien Bouaziz, Sebastian Martin, Tiantian Liu, Ladislav Kavan, and Mark Pauly. 2014.        Deformable Models. SIGGRAPH Comput. Graph. 21, 4 (Aug. 1987), 205–214.
   Projective Dynamics: Fusing Constraint Projections for Fast Simulation. ACM           Bernhard Thomaszewski, Simon Pabst, and Wolfgang Straßer. 2008. Asynchronous
   Trans. Graph. 33, 4, Article 154 (July 2014), 11 pages.                                   Cloth Simulation. Computer Graphics International 2 (2008).
R. Bridson, S. Marino, and R. Fedkiw. 2003. Simulation of Clothing with Folds and        Danyong Zhao, Yijing Li, and Jernej Barbic. 2016. Asynchronous Implicit Backward
   Wrinkles. In Proceedings of the 2003 ACM SIGGRAPH/Eurographics Symposium on               Euler Integration. In Proceedings of the ACM SIGGRAPH/Eurographics Symposium
   Computer Animation (SCA ’03). Eurographics Association, Aire-la-Ville, Switzerland,       on Computer Animation (SCA ’16). Eurographics Association, Goslar Germany,
   Switzerland, 28–36.                                                                       Germany, 1–9.
Kwang-Jin Choi and Hyeong-Seok Ko. 2002. Stable but Responsive Cloth. ACM Trans.
   Graph. 21, 3 (July 2002), 604–611.
