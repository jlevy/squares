                                               Differentiable Physics Simulations with Contacts: Do They Have Correct
                                                            Gradients w.r.t. Position, Velocity and Control?


                                                                      Yaofeng Desmond Zhong 1 Jiequn Han 2 Georgia Olympia Brikis 1


                                                                  Abstract                                 potential of differentiable simulations in solving control and
                                               In recent years, an increasing amount of work               design problems that are hard to solve by traditional tools.
                                                                                                           Compared to black-box neural networks counterparts, dif-
arXiv:2207.05060v1 [cs.LG] 8 Jul 2022




                                               has focused on differentiable physics simulation
                                               and has produced a set of open source projects              ferentiable simulations utilize physical models to provide
                                               such as Tiny Differentiable Simulator, Nimble               more reliable gradient information and better interpretabil-
                                               Physics, diffTaichi, Brax, Warp, Dojo and Dif-              ity, which is beneficial to various learning tasks involving
                                               fCoSim. By making physics simulations end-                  physics simulations.
                                               to-end differentiable, we can perform gradient-             A crucial challenge of making physics simulation differ-
                                               based optimization and learning tasks. A ma-                entiable is the non-smoothness of contact events. In the
                                               jority of differentiable simulators consider colli-         literature, different techniques have been proposed to com-
                                               sions and contacts between objects, but they use            pute gradients in dynamics involving contact events. A
                                               different contact models for differentiability. In          detailed comparison of these techniques is necessary for
                                               this paper, we overview four kinds of differen-             researchers to understand their pros and cons.
                                               tiable contact formulations - linear complemen-
                                               tarity problems (LCP), convex optimization mod-             In this paper, we first overview four kinds of differentiable
                                               els, compliant models and position-based dynam-             contact formulations - linear complementarity problems
                                               ics (PBD). We analyze and compare the gradi-                (LCP), convex optimization models, compliant models and
                                               ents calculated by these models and show that               position-based dynamics (PBD). Even though differentiable
                                               the gradients are not always correct. We also               simulation and contact models has been studied for de-
                                               demonstrate their ability to learn an optimal con-          formable objects (Rojas et al., 2021; Qiao et al., 2021a;
                                               trol strategy by comparing the learned strategies           Du et al., 2021a) and cloth (Liang et al., 2019; Li et al.,
                                               with the optimal strategy in an analytical form.            2021), we focus on collisions between rigid bodies in our
                                               The codebase to reproduce the experiment re-                benchmark experiments. We seek to answer a simple yet
                                               sults is available at https://github.com/                   important question - do these differentiable contact formula-
                                               DesmondZhong/diff_sim_grads.                                tions compute the correct gradients w.r.t. position, velocity
                                                                                                           and control? We implement different types of differentiable
                                                                                                           simulations on two examples where the analytical gradients
                                        1. Introduction                                                    can be derived in a closed form. By comparing the gradi-
                                                                                                           ents computed by simulations with analytical gradients, we
                                        With rapid advances and development of machine learning            observe that not all the computed gradients are correct and
                                        and automatic differentiation tools, a family of techniques        the gradients computed by different open source implemen-
                                        emerge to make physics simulation end-to-end differen-             tations do not agree. Our results reveal the limitation of
                                        tiable (Liang & Lin, 2020). These differentiable physics           current differentiable simulators and open up new research
                                        simulators make it easy to use gradient-based methods for          opportunities to develop more reliable physics simulators.
                                        learning and control tasks, such as system identification
                                        (Zhong et al., 2021; Le Lidec et al., 2021; Song & Boularias,
                                                                                                           2. Differentiable Physics Simulation with
                                        2020a), learning to slide unknown objects (Song & Boular-
                                        ias, 2020b) and shape optimization (Strecke & Stueckler,              Contacts
                                        2021; Xu et al., 2021). These applications demonstrate the         In this section, we overview different kinds of differentiable
                                           1                      2
                                            Siemens Technology Flatiron Institute. Correspondence to:      contact models and discuss how the gradients through the
                                        Y. D. Zhong <yaofeng.zhong@siemens.com>.                           contact events are derived and calculated. We start with
                                                                                                           linear complementarity problems and convex optimization
                                        2nd AI4Science Workshop at the 39 th International Conference on   models, both of which treat contact events as instantaneous
                                        Machine Learning (ICML), 2022. Copyright 2022 by the author(s).
                                       Differentiable Physics Simulations with Contacts

velocity changes during simulation. The goal of these two        (Todorov, 2011; Todorov et al., 2012; Todorov, 2014). The
families of methods is to solve velocity impulses.               idea is based on maximum dissipation principle - the kinetic
                                                                 energy would be maximally dissipated after an inelastic col-
2.1. Linear Complementarity Problems                             lision. Then the contact impulses are solved by minimizing
                                                                 the post-collision kinetic energy. This is a different family
Solving velocity impulses in a frictional contact event can be   of models since the complementarity condition can be vio-
formulated as a nonlinear complementarity problem (NCP),         lated in this formulation, i.e., the force and velocity along
where the friction cone constraint is nonlinear. A recent        the contact normal direction can be simultaneously positive.
differentiable simulator Dojo (Howell et al., 2022) designs      In other words, LCP treats contact surfaces as hard surfaces,
a customized solver to solve the NCP problem, and lever-         while convex optimization formulation treats them as soft
ages the implicit-function theorem to derive the gradients.      surfaces.
Most of existing works, however, approximate the NCP by
a linear complementarity problem (LCP), where the friction       With the recent progress of differentiable optimizations such
cone is approximated by a polyhedral cone (Anitescu &            as CvxpyLayer (Agrawal et al., 2019), we can easily com-
Potra, 1997). The purpose of the approximation is to guar-       pute the gradients of the solution of the convex optimization
antee a solution with any number of contacts and contact         problem w.r.t input parameters. Zhong et al. (2021) imple-
configuration. Different methods have been proposed to           ment this idea and demonstrate its application in end-to-end
compute the gradients of the solution of a LCP w.r.t. input      simultaneous learning of system properties, e.g., mass and
parameters.                                                      potential energy, and contact properties, e.g., coefficient of
                                                                 friction and restitution.
de Avila Belbute-Peres et al. (2018) derive these gradients
using implicit differentiation in a similar way as in Opt-
                                                                 2.3. Compliant Models
Net (Amos & Kolter, 2017). They show that the derived
gradients enable end-to-end learning of unknown physics          Compliant models assume contact surfaces can deform,
parameters such as the mass of objects.                          which will produce elastic forces to push collided objects
                                                                 away from each other. Since the contact constraints are not
Heiden et al. (2021b); Degrave et al. (2019); Qiao et al.
                                                                 strictly satisfied due to the soft surface assumption, com-
(2021b) also solve collision responses based on LCP, but
                                                                 pliant models are also referred to as penalty-based models
the LCP is solved using a projected Gauss-Seidel (PGS)
                                                                 from an optimization perspective. Compliant models use
method. Here the constraints of LCP are not guaranteed to
                                                                 spring-damper systems to resolve interpenetration between
hold at the end of PGS iterations, so the gradients derived
                                                                 surfaces. The interpenetration is usually resolved in mul-
by implicit differentiation might not be valid. Heiden et al.
                                                                 tiple consecutive time steps and the number of time steps
(2021b); Degrave et al. (2019) leverage existing automatic
                                                                 depends on the stiffness of the spring. In addition to normal
differentiation frameworks to get gradients through the PGS
                                                                 forces, lateral friction forces are computed using either a
solver. However, significant overhead is introduced in trac-
                                                                 nonlinear or a relaxed friction model for frictional contacts.
ing the computation graph. To improve efficiency, Qiao et al.
                                                                 In order to have a stable simulation of contact and collisions,
(2021b) propose a reverse version of the PGS solver using
                                                                 one needs to carefully tune the parameters such as spring
the adjoint method.
                                                                 stiffness, and these parameters could be hard to tune in a
Different from these approaches, Nimble (Werling et al.,         contact-rich scenario.
2021) efficiently computes analytical gradients through the
                                                                 Since the forces from the spring-damper system are con-
LCP by exploiting the sparsity of the LCP solution. Nimble
                                                                 tinuously differentiable functions of position and velocity,
also shows that analytically correct gradients might prevent
                                                                 the trajectories of position and velocity are also continuous
an optimizer from finding a good solution and proposes an
                                                                 and differentiable. This makes compliant models easy to
exploratory heuristic called “complementarity-aware gradi-
                                                                 implement using existing automatic differentiation tools. A
ent” to help optimization escape saddle points.
                                                                 number of works have explored differentiable simulation
DiffPD (Du et al., 2021b) supports a limited LCP model           with compliant models, including (Giftthaler et al., 2017),
which can handle only static friction. The gradients are         (Carpentier & Mansard, 2018), (Xu et al., 2022), Neural-
derived analytically and sparsity is leveraged for efficiency.   Sim (Heiden et al., 2021b), gradSim (Murthy et al., 2021),
DiffCloth (Li et al., 2021) extends DiffPD by deriving ana-      ADD (Geilinger et al., 2020), IPC (Li et al., 2020), DiSECt
lytical gradients of LCP with an implicit integration scheme.    (Heiden et al., 2021a), DiffPD (Du et al., 2021b), Warp
                                                                 (Macklin, 2022) and the legacy implementation of Brax
2.2. Convex Optimization Models                                  (Geilinger et al., 2020).
Mujoco simulator formulates the problem of solving fric-
tional contact impulses as a convex optimization problem
                                       Differentiable Physics Simulations with Contacts

2.4. Position-based Dynamics                                     3. Implementation Choices for Experiments
To resolve contacts, compliant models manipulate forces,         In principle, different concepts of differentiable simulation
LCP as well as convex optimization models manipulate ve-         mentioned above are not restricted to any single software
locities, and position-based dynamics (PBD) (Müller et al.,     tool. For example, we can implement them in general-
2007) directly manipulate positions. PBD is originally pro-      purpose machine learning tools such as Tensorflow, Pytorch
posed to tackle contact-rich physics-based animation in          and Jax, or tools that are tailored for physics simulations
computer graphics and games. In PBD, interpenetration            such as DiffTaichi (Hu et al., 2020) and Warp (Macklin,
in a contact event is resolved by directly projecting points     2022). In this work, we implement different differentiable
to valid locations in such a way that takes into account the     contact formulations on three systems by leveraging existing
conservation of linear and angular momentum. Velocities          open source tools to avoid reinventing the wheel. Our im-
are then updated based on the updated positions and the          plementation choice for each formulation is detailed below.
positions in the previous time step. Extended PBD (XPBD)
                                                                 For LCPs, we implement our systems in Nimble (Werling
(Macklin et al., 2016) extends the original PBD to address
                                                                 et al., 2021). Nimble is a fork of the DART physics engine
the problems of iteration-dependent contact stiffness by in-
                                                                 (Lee et al., 2018), with analytical gradients of LCP and
troducing elastic potentials.
                                                                 PyTorch binding. DiffTaichi (Hu et al., 2020) has pointed
The forward pass of calculating position-based impulses          out that directly adding velocity impulse can lead to incor-
only involves differentiable operations so the gradients can     rect gradients and proposed using continuous-time detection
be computed by automatic differentiation. Open source            or time-of-impact (TOI) for computing correct gradients.
libraries such as Warp (Macklin, 2022) and Brax (Freeman         Since LCP uses velocity impulse in simulation, it would
et al., 2021) implement differentiable PDB in this way.          suffer from this problem if the correction is not considered.
                                                                 Nimble has implemented continuous-time detection and
Liang et al. (2019) study differentiable cloth simulation and
                                                                 therefore does not suffer from this particular problem, as we
formulate the updates of positions as a quadratic program-
                                                                 can see in the experiment sections. In this work we focus
ming (QP) problem. They introduce a QR decomposition
                                                                 on frictionless contact, where the NCP and LCP formula-
step after the implicit differentiation to compute the gradi-
                                                                 tions become equivalent. We leave the investigation of NCP
ent through the QP more efficiently in the context of cloth
                                                                 formulations (Howell et al., 2022) as a future work.
simulation. Qiao et al. (2020) adopt a similar approach but
use generalized coordinates instead of Cartesian coordinates     For convex optimization models, we implement our sys-
and additionally deal with the mapping between the two           tems with a simplified version of DiffCoSim (Zhong et al.,
coordinates when deriving gradients. A relevant work in          2021). As convex optimization models also calculate veloc-
learning contact constraints (Yang et al., 2020) also use        ity impulses and the original DiffCoSim does not implement
position-based techniques to handle inelastic contacts.          TOI, we add the TOI implementation for comparison.
                                                                 For compliant models and PBD, we implement our sys-
2.5. Other Related Works
                                                                 tems with both Brax (Freeman et al., 2021) and Warp (Mack-
We further review some other relevant differentiable physics     lin, 2022). The authors of Brax have experimented with
simulators. Macklin et al. (2020) propose a primal/dual de-      compliant models but encountered stability issues. Never-
scent method for simulation, where the primal formulation        theless, they include this implementation in the project (the
is related to projective dynamics (Bouaziz et al., 2014) and     legacy spring dynamics mode). Their latest collision
the dual formulation is related to XPBD. They demonstrate        model is position-based (the pbd dynamics mode), which
the differentiability of the primal formulation using an ex-     also supports frictional and elastic contacts. Warp is a re-
ample of trajectory optimization. Le Lidec et al. (2021)         cently released open source project for high-performance
formulate the frictional contact problem into a sequence of      physics simulation. They provide example implementations
QCQPs. The analytical gradients are derived by implicit          of compliant models and PBD along with the release, but
differentiation. They demonstrate the framework on system        their current PBD implementation is preliminary and does
identification from videos of dynamical scenes. Chen et al.      not support frictional and elastic contact yet. We add fric-
(2021) propose neural event functions to model instanta-         tional and elastic support tailored to our systems.
neous velocity change during a collision. They show that for     For frictionless collisions, we can easily compute the veloc-
frictionless contacts, both the neural event functions and the   ity impulse without using the LCP or convex optimization
instantaneous updates can be learned. Sutanto et al. (2020)      models. In fact, the billiards example in diffTaichi
demonstrate the learning of physics parameters by encoding       (Hu et al., 2020) is implemented in this way. In our sys-
physical constraints in differentiable simulation. However,      tems with frictionless collisions, we also implement direct
simulation with contacts has not been investigated.              computation of velocity impulses using diffTaichi.
                                          Differentiable Physics Simulations with Contacts


                        Table 1. Task 1: gradients of the final heights w.r.t. initial position, velocity and control

                 Implementations                             ∂py,N /∂py,0                   ∂py,N /∂vy,0                    ∂py,N /∂uy,0
              Analytical gradients                             −1.0000                        −1.0000                         −0.0021
                 LCP (with TOI)                                −1.0000                        −1.0000                         −0.0021
                                      with TOI                 −1.0000                        −1.0000                         −0.0021
 Convex Optimization Model
                                     without TOI                1.0000                        −0.0958                         −0.0002
                                      with TOI                 −1.0000                        −1.0000                         −0.0021
    Direct Velocity Impulse
                                     without TOI                1.0000                        −0.1000                         −0.0002
                                         Warp                  −1.5680                        −1.2248                         −0.0026
       Compliant Model
                                         Brax                   1.0000                        −0.0958                         −0.0004
                                         Warp                   0.0000                        −0.5479                         −0.0011
               PBD
                                         Brax                  −0.0020                        −0.5467                         −0.0023


4. Experiments                                                           at t = 0 as ∆t → 0.1
In this section, we investigate and compare the performance
                                                                         4.1. Task 1: Gradients with a Simple Collision
of differentiable contact models on three tasks. The physics
system in all three tasks are two-dimensional. We mainly                 In this section, we revisit the task of simple collision studied
work with a discrete-time formulation, where the simulation              in DiffTaichi. As shown in Figure 1, this is a 2D system
duration T is discretized into N time steps with ∆t =                    without gravity. The initial position and velocity of the ball
T /N . In all three tasks, we choose ∆t = 1/480s. We                     are p0 = [−1, 1] and v0 = [2, −2]. We add constant zero
use pn = [px,n , py,n ] to denote the position of an object              controls un = [0, 0], n = 0, ..., N − 1 to the ball in order
at the nth time step. Task 3 involves two objects and the                to compute the gradients w.r.t. controls. The simulation
configuration of the system at the nth time step is denoted              duration is T = 1s. During the simulation, the ball has a
as pn = [p1,n , p2,n ] = [px1 ,n , py1 ,n , px2 ,n , py2 ,n ]. When      perfectly elastic frictionless collision with the ground. We
working in a continuous-time perspective, we use p(t) to                 are interested in the gradients of the final height w.r.t. the
denote the system configuration at time t. The velocity                  initial position, velocity and control.
variables are denoted by v and defined similarly.
                                                                         In this example, we can write down the analytical expression
Gradients with control. From a continuous-time view-                                                                RT
point, the concept of gradients w.r.t. the position or velocity
                                                                             1
                                                                              We take the functional l(u) = 0 u(t)2 dt as an example.
at certain time (this paper mainly examines the quantity at              The Fréchet derivative of l(u) in L2 is δu  δl
                                                                                                                         (t) = 2u(t). If we take
the initial time) is well-defined while the gradients w.r.t. the         the discrete approximation of the integral as ˜    l(u0 , · · · , uN −1 ) =
                                                                         PN −1 2
control is more subtle. The reason is that when the control is              i=0  u i ∆t,  where  u i are values at i∆t,  the function ˜  l has gradi-
                                                                               ˜
                                                                         ent ∇l(u0 , · · · , uN −1 ) = 2∆t(u0 , · · · , uN −1 ).
viewed as a function of time, we need to extend the classical
concept of gradients to some functional derivatives, such
as Gateaux derivative or Fréchet derivative (Gelfand et al.,
2000). To avoid the complication of diving into deeper math-
ematical concepts, here we examine the gradients w.r.t. the
control in a special setting. Given ∆t > 0 and continuous-
time control profile ũ(t) defined on [0, T ], we apply constant
u0 on [0, ∆t] and then ũ on [∆t, T ] to get the total loss l.
Then ∂l/∂u0 can be defined in the classical sense and we
treat that as the analytical gradient for comparison. We
remark that, in the finite-dimensional case, the functional
derivative is consistent with the classical derivative up to a
time discretization factor. Specifically, when u0 = ũ(0), the
gradient we consider converges to the functional derivative

                                                                                          Figure 1. Simple collision in task 1.
                                         Differentiable Physics Simulations with Contacts


                   Table 2. Task 2: gradients of loss w.r.t. initial velocity; optimized velocity; and trajectory mode.

                                                        ∂l/∂vx,0 , ∂l/∂vy,0                vx,0 , vy,0
                Implementations                                                                                     trajectory mode
                                                           at iteration 0              at iteration 999
                LCP (with TOI)                          −3.2016, −0.3059             10.2297, −4.1396                 Trajectory 1
                                     with TOI           −3.1652, −0.3059             10.2575, −4.2041                 Trajectory 1
 Convex Optimization Model
                                    without TOI          1.5898, −0.1391             −2.4934, −4.3371                 Trajectory 2
                                     with TOI           −3.1662, −0.3111             10.1841, −4.1606                 Trajectory 1
    Direct Velocity Impulse
                                    without TOI          1.5550, −0.1552             −2.4933, −4.2984                 Trajectory 2
                                        Warp            −4.9727, −0.3984             10.6386, −4.2821                 Trajectory 1
       Compliant Model
                                        Brax             1.6971, −0.0366             −2.4935, −4.7927                 Trajectory 2
                                        Warp           −16.7149, −2.0866              9.7299, −4.0706                 Trajectory 1
              PBD
                                        Brax           −0.8311, −0.0663              10.4865, −4.7518                 Trajectory 1


of the final height (see Appendix A for a derivation),                 4.2. Task 2: Optimize the Initial Velocity of a Bouncing
                                                                            Ball to Hit a Target
                                     1
 py,N = −py,0 − vy,0 T − uy,0 (T ∆t − (∆t)2 ) + 2r, (1)                In this section, we revisit a task studied in Warp (Macklin,
                                     2                                 2022) and (Macklin et al., 2020). As shown in Figure 2(a),
                                                                       we have a ball of radius r = 0.1 with initial position p0 =
where r is the radius of the ball. In Table 1, we compare the          [−0.5, 1.0] and initial velocity v0 = [5, −5]. The simulation
analytical gradients with gradients computed by different im-          duration is T = 0.6s.
plementations. We find that the three implementations that
can compute accurate gradients in this example are the ones            The initial trajectory is shown in Figure 2(a). We assume
that implement TOI. This is consistent with DiffTaichi’s               collisions are frictionless and the elastic coefficient is e =
observation. It should be emphasized that discarding TOI               0.92. These contact properties will produce trajectories
in velocity-impulse-based contact models will result in a              close to the original Warp implementation.2
completely wrong gradient w.r.t. the position, and making              The task is to optimize the initial velocity such that the
∆t smaller cannot solve the issue. We refer the interested             ball hits a target at ptarget = [−2.0, 1.5] at the end of the
reader to DiffTaichi (Hu et al., 2020) for more details.               simulation. With differentiable simulations, we can set up a
For compliant models, there exists no concept of TOI since             loss function l = ||pN − ptarget ||22 , get the gradient w.r.t the
interpenetration is resolved in multiple time steps. The gradi-        initial velocity ∂l/∂vx,0 , ∂l/∂vy,0 and use gradient descent
ents w.r.t. position of the Warp and Brax implementations do           to update the initial velocity to minimize the loss. In this
not match. In fact, they are even in the opposite directions.          task, we use a learning rate of 0.01 for 1000 gradient steps.
This phenomenon might be due to different implementation               The learning curves in Figure 2(d) (left) indicate that all the
details, e.g. spring stiffness.                                        implementations can successfully minimize the loss to zero
The two PBD implementations agree well, but they do not                and accomplish the task. Table 2 shows the gradients of
match the analytical gradients. In particular, the gradients           loss w.r.t. initial velocity before optimization (Figure 2(a))
w.r.t. position are close to zero. This is because when a              and the optimized initial velocity after 1000 gradient steps.
collision (interpenetration) is detected, the position of the          We observe that this task has at least two solutions, with
ball is updated to resolve the interpenetration. An infinitesi-        the trajectories shown in Figure 2(b) and 2(c). Different
mal change in py,0 will not change the value of py,n after             implementations learn different trajectories, as summarized
the collision, since the ball is always updated to touch the           in the last column in Table 2.
ground (py = r) right after the collision.                                 2
                                                                            The original Warp implementation is frictionless and use the
                                                                       compliant model with nonzero damping coefficient. In this non-
We also remark that across all implementations, the gra-               perfectly elastic collision case, there’s no one-to-one mapping
dients w.r.t. velocity and control are all negative. In other          between compliant model parameters and the elastic coefficient
words, even if they might be wrong in value, they are correct          in other models. We examine the horizontal velocity of the ball
in direction. If we are optimizing over velocity or control            before (5.0) and after (−4.6) the bouncing with the wall in the
in an optimization task, it is possible that it ends up with a         original trajectory and choose to use an elastic coefficient e =
                                                                       | − 4.6/5.0| = 0.92 to produce similar trajectories.
reasonable solution with these “inaccurate” gradients.
                                            Differentiable Physics Simulations with Contacts




                      (a)                                            (b)                                              (c)




                                                                      (d)


Figure 2. Trajectories and learning curves of task 2. (a) initial trajectory; (b) optimized trajectory 1; (c) optimized trajectory 2; (d) Left:
learning curves - loss over iterations; Right: learning curves - initial horizontal velocity over iterations.


We also find that which solution an implementation end
up with can be inferred from the sign of ∂l/∂vx,0 at it-
eration 0. For example, the LCP implementation results
in ∂l/∂vx,0 < 0. To minimize the loss, the algorithm in-
creases the value of vx,0 and ends up with trajectory 1. For
those implementations with ∂l/∂vx,0 > 0, the algorithm
decreases the value of vx,0 and ends up with trajectory 2.
This reasoning can be verified in Figure 2(d) (right).
If we compare implementations with and without TOI, we
notice that TOI affects the sign of ∂l/∂vx,0 , which in turn
affects the optimized trajectory. The two compliant model
implementations again produce gradients in the opposite
directions.
The takeaway from this task is that even in a simple set-                   Figure 3. The initial configuration and target position of task 3.
ting with two frictionless collisions, the gradients computed
by different implementations do not agree. These differ-
ences have a huge impact on optimization and can lead to
totally different outcomes. We also experiment with fric-                   proach, i.e., hybrid minimum principle (HMP). As Hu et al.
tional contacts in this task and have similar observations                  (2022) has derived the analytical solution of this specific
(see Appendix B.)                                                           task, we are able to use that to measure the performance of
                                                                            different implementations.
4.3. Task 3: Learning Optimal Control with a Two-ball                       The system is shown in Figure 3. We have two balls, of
     Collision                                                              the same size (radius r = 0.2) on a plane with no gravity.
                                                                            The initial positions of the balls are p1,0 = [−2, −2] and
In this section, we investigate the learning of optimal control
                                                                            p2,0 = [−1, −1] and the initial velocities are v1,0 = v2,0 =
sequences using differentiable simulation. The specific task
                                                                            [0, 0]. The simulation duration is T = 1s. We are able to
has been studied by Hu et al. (2022) using a different ap-
                                                                            add control inputs as forces acted on the first ball. The goal
                                           Differentiable Physics Simulations with Contacts


                        Table 3. Task 3: gradients of loss w.r.t. initial position, velocity and control at iteration 0

                                                         ∂l/∂px1 ,0 , ∂l/∂px2 ,0       ∂l/∂vx1 ,0 , ∂l/∂vx2 ,0              ∂l/∂ux1 ,0
                 Implementations
                                                             at iteration 0                at iteration 0                  at iteration 0
              Analytical gradients                       −0.3987, −0.3213              −0.4978, −0.2221                      −0.0009
                 LCP (with TOI)                           −0.5476, −0.1825              −0.6031, −0.1270                      0.0000
                                       with TOI            −0.7325, 0.0000              −0.7310, −0.0015                     −0.0003
 Convex Optimization Model
                                      without TOI          0.0000, −0.7291              −0.2233, −0.5058                     0.0008
                                       with TOI            −0.7191, 0.0000               −0.7191, 0.0000                     −0.0002
    Direct Velocity Impulse
                                      without TOI          0.0000, −0.7156              −0.2221, −0.4935                     0.0008
                                          Warp             0.9509, −1.6969               0.4348, −1.1808                      0.0022
        Compliant Model
                                          Brax             0.0000, −0.7252              −0.2220, −0.5031                      0.0016
                                          Warp            −0.3610, −0.3610              −0.4723, −0.2497                      0.0003
               PBD
                                          Brax            −0.3613, −0.3606              −0.4725, −0.2494                      0.0005




Figure 4. Results of task 3. Left: learning curves; Right: learned control profiles along with analytical optimal control profile.


in this task is to push ball 1 to strike ball 2 so that ball 2 will       φ(s(T )) = ||p2 (T )||22 to capture our goal and running cost
be close to the origin at the end of the simulation.                      to be L(s, u) = ||u||22 with  = 0.1 to penalize large con-
                                                                          trol inputs. See the appendix of Hu et al. (2022) for the
The problem can be formulated as an optimal control prob-
                                                                          optimal solution of this problem in an analytic form.
lem in continuous-time with state jumps:
                        Z T                                               To solve the above problem approximately, we discrete the
 minimize φ(s(T )) +        L(s(t), u(t))dt,          (2)                 problem into
    u(·)                      0                                                                                  N −1
               ṡ(t) = f (s(t), u(t)), t ∈ [0, γ) or t ∈ (γ, T ],
                                                                                                                 X
subject to                                                                           minimize        φ(sN ) +           L(si , ui )∆t,      (6)
                                                              (3)                    u0 ,...,uN −1
                                                                                                                 i=0
               ψ(s(γ − )) = 0,                                   (4)                 subject to      si+1 = step(si , ui , ∆t).             (7)
                   +              −
               s(γ ) = g(s(γ )).                                 (5)
                                                                          The step function takes the current state and control as
                                                                          inputs and calculates the next time step state based on dy-
Here we use s = [p, v] to denote the positions and veloc-
                                                                          namics and collisions. With differentiable simulations, we
ities of two balls as the state variable. f denotes the state
                                                                          can differentiate through the step function and solve for
dynamics under external forces u; γ denotes the time of
                                                                          the optimal control sequence directly using gradient descent.
collision between two balls, characterized by the distance
function ψ between two balls; and g denotes the effect                    We initiate our control sequence as a constant force un =
of collision on the state. We choose terminal cost to be                  [3, 3], n = 0, ..., N −1. With this constant control sequence,
                                       Differentiable Physics Simulations with Contacts

we can compute the gradients of the loss w.r.t. initial posi-
tions and velocities of the two balls as well as the control
at the first time step. As this task is symmetric in x and
y coordinates, we only present the x-components in Ta-
ble 3. The y-components are the same as the corresponding
x-components. The analytical gradients in the table are com-
puted by deriving the analytical expression of the loss as
done in Section 4.1. We provide code scripts of computing
these gradients in Appendix C.
Surprisingly, from Table 3, we observe that none of the
gradients from differentiable simulators match the analytical    Figure 5. Task 3: learning curves of compliant models imple-
gradients; only the two implementations based on PBD give        mented in Warp with different spring stiffness kn . Spring stiffness
results that are close to the analytical gradients.              determines the normal contact force based on interpenetration d,
                                                                 i.e., fn = −kn · d.
In this task, we use a learning rate of 10 for 1000 gradient
steps. Figure 4 (left) shows the learning curves of differ-
ent implementations along with the analytical optimal loss
(1.3965). We observe that two implementations without TOI
and two compliant model implementations fail to converge
to the analytical optimal loss. The rest of the implemen-        The takeaway from this task is that the gradients computed
tations converge to values that are close to the analytical      by differentiable physics simulators might not reflect the true
optimal loss.                                                    gradients in the physics process. Nevertheless, they might
                                                                 still be helpful in gradient-based learning tasks. The reasons
Figure 4 (right) compares the control profile optimized          behind the successful optimizations with wrong gradients
by different simulators with the analytical optimal control,     need further investigation. In more complex contact-rich
based on the analytical expression presented in (Hu et al.,      scenarios, it is likely that none of the current differentiable
2022). We observe that for two implementations without           simulators can accomplish particular optimization tasks.
TOI and the Brax implementation of the compliant model,
the learned control sequences are close to zero all the time.
Under a zero control sequence, the two balls would not           5. Conclusion
move at all resulting in a running loss of 0 and a terminal      In this paper, we investigated gradient computation using
loss of 2. From Figure 4 (left) we can confirm that these        existing differentiable physics simulation tools. We apply
three implementations end up with a loss close to 2. For         multiple differentiable simulators on three tasks. All the
all the other implementations, the shapes of the learned op-     three tasks only involve simple frictionless collision and do
timal control profiles resemble the analytical one, where,       not involve ill-cases such as grazing contacts (Corner, 2017),
they linearly decrease before the collision and drop to zero     which are likely not differentiable. We find that in a specific
after the collision. Three implementations with TOI per-         system (Task 3), the gradients w.r.t. position, velocity and
form the best in learning the optimal control sequence. We       control computed from all differentiable simulators studied
remark that, as reported in (Hu et al., 2022), the deep rein-    in this paper do not match the analytical result well.
forcement learning algorithm PPO (Schulman et al., 2017)
usually finds a solution with a running loss of 0 and a ter-     This finding raises two questions: 1) how can the optimiza-
minal loss of 2, if there is no reward shaping. Compared to      tion task be successfully achieved with wrong gradients?
such model-free reinforcement learning methods, optimiz-         and more importantly 2) how to improve differentiable sim-
ing with differentiable physics simulations demonstrates its     ulations to compute correct gradients? If these questions
strength in solving control tasks.                               are properly addressed, differentiable physics simulation
                                                                 can serve as a powerful interpretable tool in end-to-end op-
We also experiment with the spring stiffness parameter in the    timization tasks, such as system identification, learning of
compliant models, as shown in Figure 5. We observe that a        dynamics systems, learning of optimal control, geometry
small stiffness (100) makes the surface too soft to represent    optimization and reinforcement learning. We hope this work
the actual collision phenomenon. The initial loss is 2.39        can motivate future research into differentiable physics sim-
in this case while the analytical loss before optimization is    ulations. A recent study (Suh et al., 2022) compares the
around 2.06. The initial losses of larger stiffness are indeed   gradients of a differentiable simulator and policy gradients
around 2.06, but a large stiffness such as 105 makes learning    in a stochastic setting. It will also be of interest to extend the
unstable and fails to learn a reasonable control strategy.       comparison with the differentiable simulator with improved
                                                                 gradients.
                                       Differentiable Physics Simulations with Contacts

References                                                       Geilinger, M., Hahn, D., Zehnder, J., Bächer, M.,
                                                                   Thomaszewski, B., and Coros, S. Add: Analytically
Agrawal, A., Amos, B., Barratt, S., Boyd, S., Diamond, S.,
                                                                   differentiable dynamics for multi-body systems with fric-
  and Kolter, J. Z. Differentiable convex optimization lay-
                                                                   tional contact. ACM Transactions on Graphics (TOG),
  ers. Advances in neural information processing systems,
                                                                   39(6):1–15, 2020.
  32, 2019.
                                                                 Gelfand, I. M., Silverman, R. A., et al. Calculus of varia-
Amos, B. and Kolter, J. Z. Optnet: Differentiable opti-
                                                                   tions. Courier Corporation, 2000.
 mization as a layer in neural networks. In International
 Conference on Machine Learning, pp. 136–145. PMLR,              Giftthaler, M., Neunert, M., Stäuble, M., Frigerio, M., Sem-
 2017.                                                             ini, C., and Buchli, J. Automatic differentiation of rigid
Anitescu, M. and Potra, F. A. Formulating dynamic multi-           body dynamics for optimal control and estimation. Ad-
  rigid-body contact problems with friction as solvable            vanced Robotics, 31(22):1225–1237, 2017.
  linear complementarity problems. Nonlinear Dynamics,           Heiden, E., Macklin, M., Narang, Y., Fox, D., Garg, A.,
 14(3):231–247, 1997.                                              and Ramos, F. Disect: A differentiable simulation en-
Bouaziz, S., Martin, S., Liu, T., Kavan, L., and Pauly, M.         gine for autonomous robotic cutting. arXiv preprint
  Projective dynamics: Fusing constraint projections for           arXiv:2105.12244, 2021a.
  fast simulation. ACM transactions on graphics (TOG),           Heiden, E., Millard, D., Coumans, E., Sheng, Y., and
  33(4):1–11, 2014.                                                Sukhatme, G. S. Neuralsim: Augmenting differentiable
Carpentier, J. and Mansard, N. Analytical derivatives of           simulators with neural networks. In 2021 IEEE Interna-
  rigid body dynamics algorithms. In Robotics: Science             tional Conference on Robotics and Automation (ICRA),
  and systems (RSS 2018), 2018.                                    pp. 9474–9481. IEEE, 2021b.

Chen, R. T. Q., Amos, B., and Nickel, M. Learning neural         Howell, T. A., Cleac’h, S. L., Kolter, J. Z., Schwager, M.,
  event functions for ordinary differential equations. In          and Manchester, Z. Dojo: A differentiable simulator for
  International Conference on Learning Representations,            robotics. arXiv preprint arXiv:2203.00806, 2022.
  2021.                                                          Hu, W., Long, J., Zang, Y., E, W., and Han, J. Solving
Corner, S. M. Modeling, sensitivity analysis, and optimiza-        optimal control of rigid-body dynamics with collisions
  tion of hybrid, constrained mechanical systems. PhD              using the hybrid minimum principle. arXiv preprint
  thesis, Virginia Polytechnic Institute and State University,     arXiv:2205.08622, 2022.
  2017.
                                                                 Hu, Y., Anderson, L., Li, T.-M., Sun, Q., Carr, N., Ragan-
de Avila Belbute-Peres, F., Smith, K., Allen, K., Tenenbaum,       Kelley, J., and Durand, F. Difftaichi: Differentiable pro-
  J., and Kolter, J. Z. End-to-end differentiable physics for      gramming for physical simulation. In International Con-
  learning and control. Advances in neural information             ference on Learning Representations, 2020.
  processing systems, 31, 2018.
                                                                 Le Lidec, Q., Kalevatykh, I., Laptev, I., Schmid, C., and Car-
Degrave, J., Hermans, M., Dambre, J., et al. A differentiable      pentier, J. Differentiable simulation for physical system
  physics engine for deep learning in robotics. Frontiers in       identification. IEEE Robotics and Automation Letters, 6
  neurorobotics, pp. 6, 2019.                                      (2):3413–3420, 2021.

Du, T., Hughes, J., Wah, S., Matusik, W., and Rus, D. Under-     Lee, J., Grey, M. X., Ha, S., Kunz, T., Jain, S., Ye, Y., Srini-
  water soft robot modeling and control with differentiable        vasa, S. S., Stilman, M., and Liu, C. K. Dart: Dynamic
  simulation. IEEE Robotics and Automation Letters, 6(3):          animation and robotics toolkit. Journal of Open Source
  4994–5001, 2021a.                                                Software, 3(22):500, 2018.

Du, T., Wu, K., Ma, P., Wah, S., Spielberg, A., Rus, D., and     Li, M., Ferguson, Z., Schneider, T., Langlois, T., Zorin, D.,
  Matusik, W. Diffpd: Differentiable projective dynam-             Panozzo, D., Jiang, C., and Kaufman, D. M. Incremental
  ics. ACM Transactions on Graphics (TOG), 41(2):1–21,             potential contact: Intersection-and inversion-free, large-
  2021b.                                                           deformation dynamics. ACM transactions on graphics,
                                                                   2020.
Freeman, C. D., Frey, E., Raichuk, A., Girgin, S., Mordatch,
  I., and Bachem, O. Brax - a differentiable physics engine      Li, Y., Du, T., Wu, K., Xu, J., and Matusik, W. Diffcloth:
  for large scale rigid body simulation, 2021. URL http:           Differentiable cloth simulation with dry frictional contact.
  //github.com/google/brax.                                        arXiv preprint arXiv:2106.05306, 2021.
                                       Differentiable Physics Simulations with Contacts

Liang, J. and Lin, M. C. Differentiable Physics Simulation.      Song, C. and Boularias, A. Identifying mechanical models
  In ICLR 2020 Workshop on Integration of Deep Neural              of unknown objects with differentiable physics simula-
  Models and Differential Equations, 2020.                         tions. In Proceedings of the 2nd Conference on Learning
                                                                   for Dynamics and Control, volume 120 of Proceedings of
Liang, J., Lin, M., and Koltun, V. Differentiable cloth            Machine Learning Research, pp. 749–760. PMLR, 2020a.
  simulation for inverse problems. Advances in Neural
  Information Processing Systems, 32, 2019.                      Song, C. and Boularias, A. Learning to slide unknown ob-
                                                                   jects with differentiable physics simulations. In Robotics
Macklin, M. Warp: A high-performance python framework              science and systems, 2020b.
 for gpu simulation and graphics. https://github.
 com/nvidia/warp, March 2022. NVIDIA GPU                         Strecke, M. and Stueckler, J. Diffsdfsim: Differentiable
 Technology Conference (GTC).                                      rigid-body dynamics with implicit shapes. In 2021 In-
                                                                   ternational Conference on 3D Vision (3DV), pp. 96–105.
Macklin, M., Müller, M., and Chentanez, N. Xpbd: position-        IEEE, 2021.
 based simulation of compliant constrained dynamics. In
 Proceedings of the 9th International Conference on Mo-          Suh, H., Simchowitz, M., Zhang, K., and Tedrake, R. Do dif-
 tion in Games, pp. 49–54, 2016.                                   ferentiable simulators give better policy gradients? arXiv
                                                                   preprint arXiv:2202.00817, 2022.
Macklin, M., Erleben, K., Müller, M., Chentanez, N.,
 Jeschke, S., and Kim, T. Primal/dual descent methods for        Sutanto, G., Wang, A., Lin, Y., Mukadam, M., Sukhatme,
 dynamics. In Proceedings of the ACM SIGGRAPH/Euro-                G., Rai, A., and Meier, F. Encoding physical constraints
 graphics Symposium on Computer Animation, pp. 1–12,               in differentiable newton-euler algorithm. In Learning for
 2020.                                                             Dynamics and Control, pp. 804–813. PMLR, 2020.

Müller, M., Heidelberger, B., Hennix, M., and Ratcliff, J.      Todorov, E. A convex, smooth and invertible contact model
 Position based dynamics. Journal of Visual Communica-             for trajectory optimization. In 2011 IEEE International
 tion and Image Representation, 18(2):109–118, 2007.               Conference on Robotics and Automation, pp. 1071–1076,
                                                                   2011.
Murthy, J. K., Macklin, M., Golemo, F., Voleti, V., Petrini,
 L., Weiss, M., Considine, B., Parent-Lévesque, J., Xie,        Todorov, E. Convex and analytically-invertible dynamics
 K., Erleben, K., Paull, L., Shkurti, F., Nowrouzezahrai,          with contacts and constraints: Theory and implementation
 D., and Fidler, S. gradsim: Differentiable simulation for         in MuJoCo. In 2014 IEEE International Conference on
 system identification and visuomotor control. In Interna-         Robotics and Automation (ICRA), pp. 6054–6061, 2014.
 tional Conference on Learning Representations, 2021.
                                                                 Todorov, E., Erez, T., and Tassa, Y. Mujoco: A physics
Qiao, Y., Liang, J., Koltun, V., and Lin, M. Differentiable        engine for model-based control. In 2012 IEEE/RSJ Inter-
  simulation of soft multi-body systems. Advances in Neu-          national Conference on Intelligent Robots and Systems,
  ral Information Processing Systems, 34, 2021a.                   pp. 5026–5033. IEEE, 2012.

Qiao, Y.-L., Liang, J., Koltun, V., and Lin, M. Scalable         Werling, K., Omens, D., Lee, J., Exarchos, I., and Liu,
  differentiable physics for learning and control. In Interna-    C. K. Fast and feature-complete differentiable physics
  tional Conference on Machine Learning, pp. 7847–7856.           for articulated rigid bodies with contact. arXiv preprint
  PMLR, 2020.                                                     arXiv:2103.16021, 2021.

Qiao, Y.-L., Liang, J., Koltun, V., and Lin, M. C. Efficient     Xu, J., Chen, T., Zlokapa, L., Foshey, M., Matusik, W.,
  differentiable simulation of articulated bodies. In Interna-     Sueda, S., and Agrawal, P. An End-to-End Differentiable
  tional Conference on Machine Learning, pp. 8661–8671.            Framework for Contact-Aware Robot Design. In Pro-
  PMLR, 2021b.                                                     ceedings of Robotics: Science and Systems, Virtual, July
                                                                   2021.
Rojas, J., Sifakis, E., and Kavan, L. Differentiable implicit
  soft-body physics. arXiv preprint arXiv:2102.05791,            Xu, J., Macklin, M., Makoviychuk, V., Narang, Y., Garg,
  2021.                                                           A., Ramos, F., and Matusik, W. Accelerated policy
                                                                   learning with parallel differentiable simulation. In In-
Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and           ternational Conference on Learning Representations,
  Klimov, O. Proximal policy optimization algorithms.              2022. URL https://openreview.net/forum?
  arXiv preprint arXiv:1707.06347, 2017.                           id=ZSKRQMvttc.
                                     Differentiable Physics Simulations with Contacts

Yang, S., He, X., and Zhu, B. Learning physical constraints
  with neural projections. Advances in Neural Information
  Processing Systems, 33:5178–5189, 2020.
Zhong, Y. D., Dey, B., and Chakraborty, A. Extending
  lagrangian and hamiltonian neural networks with differ-
  entiable contact models. Advances in Neural Information
  Processing Systems, 34, 2021.
                                         Differentiable Physics Simulations with Contacts


Appendices
A. Derivation of Equation 1
For this system, the dynamics along x and y axes are decoupled. Here we are interested in the dynamics along y axis.
We assume the initial control component uy,0 is applied to the ball from time 0 to time ∆t, and the control remain zero
afterwards. Then the velocity and position components at time ∆t are
                                               vy,1 = vy,0 + uy,0 ∆t                                                                   (8)
                                                                    1
                                             py,1 = py,0 + vy,0 ∆t + uy,0 (∆t)2                                                        (9)
                                                                    2
Since the contact is perfectly elastic, we have
                                           (py,N − r) + (py,1 − r) = −vy,1 (T − ∆t)                                                   (10)
Thus we get Equation 1
                                                                         1
                                     py,N = −py,0 − vy,0 T − uy,0 (T ∆t − (∆t)2 ) + 2r.                                               (11)
                                                                         2
The analytical gradients are
                              ∂py,N                 ∂py,N                   ∂py,N          1
                                    = −1,                 = −T,                   = −T ∆t + (∆t)2                                     (12)
                              ∂py,0                 ∂vy,0                   ∂uy,0          2

B. Task 2 with Friction
We change the frictionless contacts in Task 2 to be frictional with coefficient µ = 0.1. In this case, it would be challenging
to directly compute the velocity impulse. Thus, we implement the all the other contact model formulations and present the
result in Table 4. Here Trajectory 1 and 2 refers to trajectories similar to those in Figure 2(b) (colliding with both the ground
and the wall) and Figure 2(c) (colliding with only the ground), respectively.

            Table 4. Task 2 with friction: gradients of loss w.r.t. initial velocity; optimized velocity; and trajectory mode.

                                                        ∂l/∂vx,0 , ∂l/∂vy,0                vx,0 , vy,0
                Implementations                                                                                     trajectory mode
                                                           at iteration 0              at iteration 999
                LCP (with TOI)                          −3.2016, −0.3190             11.3389, −6.1378                 Trajectory 1
                                     with TOI           −4.2416, −1.4351             10.3454, −3.9920                Trajectory 1
 Convex Optimization Model
                                    without TOI          3.2069, 0.1918               0.6268, −4.7243                N/A (Failed)
            Direct Velocity Impulse                                                          N/A
                                        Warp            −4.5909, −1.4180             11.8168, −6.4319                 Trajectory 1
       Compliant Model
                                        Brax             1.7889, −0.0147             −2.5777, −4.7980                 Trajectory 2
                                        Warp           −12.9160, 126.9161            10.3663, −3.9202                 Trajectory 1
              PBD
                                        Brax           −0.8622, −0.3825              10.1879, −3.9497                 Trajectory 1



C. Code Snippets for Computing Analytical Gradients in Task 3
The gradients in this case can be derived in an analytical form. They can also be computed by automatic differentiation. As
the analytical expressions are lengthy, here we provide two code snippets to compute the these gradients in JAX. We have
verified that the gradients computed by analytical expressions and by the code snippets match with each other as expected.
Since this problem is symmetric, the gradients in the direction [1, −1] are zero. In the code snippets, we simplify the problem
into a 1D problem by computing the gradients along the direction [1, 1]. We then convert them back to the 2D coordinate
frame.
                                            Differentiable Physics Simulations with Contacts

     The first code snippet only computes the gradient w.r.t. initial position, it has a simple form and should be easy to understand
 1 import jax
 2 import jax.numpy as jnp
 3 import numpy as np
 4 def loss_fn(x, u_c=3*jnp.sqrt(2), r=0.2, T=1.):
 5     x1_0 = x[0]
 6     x2_0 = x[1]
 7     # time of collision
 8     s = jnp.sqrt(2 * (x2_0 - x1_0 - 2 * r) / u_c)
 9     # velocity at time of collision
10     v1_s = u_c * s
11     x2_T = x2_0 + v1_s * (T - s)
12     l = x2_T ** 2
13     return l, (s, v1_s, x2_T)
14
15 grad_loss_fn = jax.grad(loss_fn, has_aux=True)
16 x0 = jnp.array([-2 * jnp.sqrt(2), -1 * jnp.sqrt(2)])
17 dl_dx, aux_data = grad_loss_fn(x0)
18 print((dl_dx)/ jnp.sqrt(2))
19
20   # output
21   # [-0.39866853 -0.3212531 ]

                                        Listing 1. computing gradients w.r.t. initial position in Task 3

     The second code snippet computes the gradient w.r.t. initial position, velocity and control.
 1 import jax
 2 import jax.numpy as jnp
 3 import numpy as np
 4 def loss_fn(x0, v0, u0, u_c=3*jnp.sqrt(2), dt=1./480, r=0.2, T=1., epsilon=0.1):
 5     x1_0 = x0[0] ; x2_0 = x0[1]
 6     v1_0 = v0[0] ; v2_0 = v0[1]
 7     # integrate first time analytically
 8     v1_dt = v1_0 + u0 * dt ; v2_dt = v2_0
 9     x1_dt = x1_0 + v1_0 * dt + u0 * dt**2/2
10     x2_dt = x2_0 + v2_0 * dt
11     # solve time of collision
12     # \int_{dt}ˆ{s} (v1_dt + u_c*(t-dt) - v2_dt) = x2_dt - x1_dt - 2 * r
13     dist_dt = x2_dt - x1_dt - 2 * r
14     # a (s-dt)ˆ2 + b (s-dt) + c = 0
15     a = u_c / 2
16     b = v1_dt - v2_dt
17     c = -dist_dt
18     s = (-b + jnp.sqrt(b*b - 4*a*c)) / (2*a) + dt
19     # velocity at time of collision
20     v1_s = v1_dt + u_c * (s - dt)
21     x2_s = x2_dt + v2_dt * (s - dt)
22     x2_T = x2_s + v1_s * (T - s)
23     l = x2_T ** 2 + epsilon * u0 * dt # running loss for future us does not matter
24     return l, (s, v1_s, x2_T)
25
26 grad_loss_fn = jax.grad(loss_fn, [0, 1, 2], has_aux=True)
27 x0 = jnp.array([-2 * jnp.sqrt(2), -1 * jnp.sqrt(2)])
28 v0 = jnp.array([0., 0.])
29 u0 = 3 * jnp.sqrt(2)
30 dl, aux_data = grad_loss_fn(x0, v0, u0)
31 dl_dx0, dl_dv0, dl_du0 = dl
32 print(dl_dx0 / jnp.sqrt(2))
33 print(dl_dv0 / jnp.sqrt(2))
34 print(dl_du0 / jnp.sqrt(2))
35 # output
36 # [-0.39866856 -0.32125315]
37 # [-0.49779078 -0.22213092]
                                      Differentiable Physics Simulations with Contacts

38   # -0.0008888851

                       Listing 2. computing gradients w.r.t. initial position velocity and control in Task 3
