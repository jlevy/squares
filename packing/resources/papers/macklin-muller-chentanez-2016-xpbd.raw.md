          XPBD: Position-Based Simulation of Compliant Constrained Dynamics
                                          Miles Macklin              Matthias Müller      Nuttapong Chentanez

                                                                           NVIDIA




Figure 1: In this example, we see the effect of changing the relative stiffness of volume conservation and stretch and shear constraints on a
deformable body. Unlike traditional PBD, our method allows users to control the stiffness of deformable bodies in a time step and iteration
count independent manner, greatly simplifying asset creation.


Abstract                                                                         simulation [Bender et al. 2014b]. Specifically, constraints become
                                                                                 arbitrarily stiff as the iteration count increases, or as the time step
We address the long-standing problem of iteration count and                      decreases. This coupling of parameters is particularly problematic
time step dependent constraint stiffness in position-based dynamics              when creating scenes with a variety of material types, e.g.: soft
(PBD). We introduce a simple extension to PBD that allows it to                  bodies interacting with nearly rigid bodies. In this scenario, raising
accurately and efficiently simulate arbitrary elastic and dissipative            iteration counts to obtain stiffness on one object may inadvertently
energy potentials in an implicit manner. In addition, our method                 change the behavior of all other objects in the simulation. This often
provides constraint force estimates, making it applicable to a wider             requires stiffness coefficients to be re-tuned globally, making the
range of applications, such as those requiring haptic user-feedback.             creation of reusable simulation assets extremely difficult. Iteration
We compare our algorithm to more expensive non-linear solvers                    count dependence is also a problem even in the case of a single asset,
and find it produces visually similar results while maintaining the              for example, setting the relative stiffness of stretch and bending
simplicity and robustness of the PBD method.                                     constraints in a cloth model. To make matters worse, the effects of
                                                                                 iteration count are non-linear, making it difficult to intuitively adjust
Keywords: physics simulation, constrained dynamics, position                     parameters, or to simply rescale stiffness values as a simple function
based dynamics                                                                   of iteration count.

Concepts: •Computing methodologies → Real-time simulation;                       The recent resurgence in virtual-reality has given rise to the need for
Interactive simulation;                                                          higher fidelity and more physically representative real-time simu-
                                                                                 lations. At the same time, the wide-spread use of haptic feedback
                                                                                 devices require methods than can provide accurate force estimates.
1    Introduction                                                                PBD does not have a well defined concept of constraint force, and
                                                                                 as such it has mostly been limited to applications where accuracy
Position-Based Dynamics [Müller et al. 2007] is a popular method                is less important than speed, and where simulations are secondary
for the real-time simulation of deformable bodies in games and                   effects.
interactive applications. The method is particularly attractive for its
simplicity and robustness, and has recently found popularity outside             In this paper we present our extended position-based dynamics
of games, in film and medical simulation applications.                           (XPBD) algorithm. Our method addresses the problems of iteration
                                                                                 and time step dependent stiffness by introducing a new constraint
As its popularity has increased, the limitations of PBD have be-                 formulation that corresponds to a well-defined concept of elastic
come more problematic. One well known limitation is that PBD’s                   potential energy. We derive our method from an implicit time dis-
behavior is dependent on the time step and iteration count of the                cretization that introduces the concept of a total Lagrange multiplier
                                                                                 to PBD. This provides constraint force estimates that can be used to
Permission to make digital or hard copies of all or part of this work for        drive force dependent effects and devices.
personal or classroom use is granted without fee provided that copies are not
made or distributed for profit or commercial advantage and that copies bear      To summarize, our main contributions are:
this notice and the full citation on the first page. Copyrights for components      • Extending PBD constraints to have a direct correspondence to
of this work owned by others than the author(s) must be honored. Abstracting
                                                                                      well-defined elastic and dissipation energy potentials.
with credit is permitted. To copy otherwise, or republish, to post on servers
or to redistribute to lists, requires prior specific permission and/or a fee.       • Introducing the concept of a total Lagrange multiplier to PBD
Request permissions from permissions@acm.org. © 2016 Copyright held by                allowing us to solve constraints in a time step and iteration
the owner/author(s). Publication rights licensed to ACM.                              count independent manner.
MiG ’16,, October 10 - 12, 2016, Burlingame, CA, USA
ISBN: 978-1-4503-4592-7/16/10                                                       • Validation of our algorithm against a reference implicit time
DOI: http://dx.doi.org/10.1145/2994258.2994272                                        stepping scheme based on a non-linear Newton solver.
2    Related Work                                                         3    Background
                                                                          We briefly describe the core of the position-based dynamics algo-
There is a large body of work in computer graphics that attempts to       rithm and refer to the survey paper by Bender et al. [2014b] for
solve constrained dynamics simulations [Nealen et al. 2005]. Our          further detail. PBD can be thought of as a semi-implicit integration
method builds on the position-based dynamics (PBD) algorithm              step using the Stömer-Verlet method, followed by a number of con-
presented by Müller et al. [2007], which solves constraints at the       straint projection steps. The projection step is performed using local
position-level in an iterative Gauss-Seidel fashion. Stam [2009]          linearizations of each constraint function with mass weighted cor-
proposed a similar Gauss-Seidel constraint solver that operates on        rections. The main step in PBD’s constraint solver is the calculation
velocities. These approaches operate on constraints locally and are       of the per-constraint position delta, given by:
popular due to their efficiency and ease of implementation, however
both methods suffer from iteration count stiffness dependence.
                                                                                                ∆x = kj sj M−1 ∇Cj (xi ).                        (1)
Many authors have applied PBD to deformable object simulation.
Recently, Bender et al. [2014a] proposed a continuum-based for-           Here the subscript i denotes the iteration index, j is the constraint
mulation that treats strain-energy as a constraint function directly.     index, and k ∈ [0, 1] is the constraint stiffness applied simply as
Concurrently, Müller et al. [2014] proposed constraining the entries     a multiplier on each constraint correction. The scaling factor, s, is
of the Green-St Venant strain tensor to allow controlling strain in di-   given by the following equation, derived from a single Newton step
rections independent from the model discretization. Shape matching        of the constraint function:
[Müller et al. 2005] introduces a geometric constraint for the simu-
lation of deformable objects amenable to PBD, but again, all these                                         −Cj (xi )
methods suffer from a strong dependency of stiffness on iteration                                 sj =                .                          (2)
                                                                                                         ∇Cj M−1 ∇CjT
count. In contrast, our compliant constraint formulation has a direct
correspondence to tradtional constitutive models, and converges to a
well-defined solution.                                                    An undesirable side-effect of simply scaling the position change by
                                                                          k is that the effective constraint stiffness is now dependent on both
                                                                          the time step and the number of constraint projections performed.
Servin et al. [2006] proposed a compliant constraint formulation of       Müller et al. [2007] attempted to address this by exponential scaling
continuum models and a semi-implicit, velocity level integrator to        of the stiffness coefficient. However this does not take into account
handle a large range of stiffness in a time step independent manner.      the time step, and does not converge to a well-defined solution in
Our work adapts their compliant constraint formulation to PBD,            the presence of multiple constraints.
allowing us to solve constraints at the position level, and without
additional stabilization terms.                                           In the following section we develop a scheme using regularized
                                                                          constraints that have a direct correspondence to well-defined energy
A number of works use a global approach in solving constraints.           potentials, and show how to solve these in a time step and iteration
Goldenthal et al. [2007] proposes a projection method for enforcing       count independent manner.
inextensible constraints similar to PBD, but where the constrained
system is globally linearized and solved with a direct method at each     Algorithm 1 XPBD simulation loop
iteration. Our method may be seen as a compliant version of their
                                                                           1: predict position x̃ ⇐ xn + ∆tvn + ∆t2 M−1 fext (xn )
Fast Projection algorithm, combined with an iterative Gauss-Seidel
                                                                           2:
solver. Tournier et al. [2015] extend a compliant constraint formula-
                                                                           3: initialize solve x0 ⇐ x̃
tion with second order derivative information to avoid instabilities
                                                                           4: initialize multipliers λ0 ⇐ 0
due to linearization. In contrast to their work, our method uses
                                                                           5: while i < solverIterations do
only first order constraint derivatives, and avoids stability problems
                                                                           6:    for all constraints do
related to global linearization through repeated local linearizations
                                                                           7:        compute ∆λ using Eq (18)
per-time step.
                                                                           8:        compute ∆x using Eq (17)
                                                                           9:        update λi+1 ⇐ λi + ∆λ
Liu et al. [2013] propose a local–global solver for mass-spring sys-      10:        update xi+1 ⇐ xi + ∆x
tems, where a local solve is used to handle non-linear terms relating     11:    end for
to direction, while the global solve, which can be pre-factored, is       12:    i⇐i+1
used for handling stretching. The stiffness is largely independent        13: end while
of the iteration count and the solution approaches that of Newton’s       14:
method as the number of iterations increases. The idea is generalized     15: update positions xn+1 ⇐ xi
to other constraints in Projective Dynamics by Boaziz et al. [2014].      16: update velocities vn+1 ⇐ ∆t 1
                                                                                                            xn+1 − xn
                                                                                                                      
Wang [2015] proposes a Chebyshev type approach that combines
results from previous iterations to obtain better convergence. Narain
et al. [2016] applies the alternating direction method of multipliers
(ADMM) for implicit time integration. Their method allows han-            4    Our Method
dling nonlinear constitutive models, hard constraints, and they show
that projective dynamics is a special case of the ADMM.                   We derive our extended position-based dynamics algorithm (XPBD)
                                                                          by starting with Newton’s equations of motion subject to forces
                                                                          derived from an energy potential U (x):
These global approaches typically rely on the fact the global solve
can be done efficiently, which often means pre-factoring the global                                 Mẍ = −∇U T (x).                             (3)
matrix. However, if the constraint topology changes during run-time
such as due to tearing or fracturing, the global matrix needs to be
re-factored, which can be computationally intensive. They also tend       Here x = [x1 , x2 , · · · , xn ]T is the system state. In PBD this is often
to be much more involved to implement compared to PBD.                    simply particle positions, however it may represent any generalized
                                                                                        ∂g
coordinate model, e.g.: rigid body transforms. Note that we use the       where K = ∂x     . This system may be solved for ∆x and ∆λ and
convention that the gradient operator ∇ is a row vector of partial        the positions and multipliers updated accordingly:
derivatives.
                                                                                                   λi+1 = λi + ∆λ                           (13)
We perform an implicit position-level time discretization of our                                   xi+1 = xi + ∆x.                          (14)
equations of motion (3), where the superscript n denotes the time
step index:
                                                                          This is a fixed-point iteration that satisfies our implicit equations
                                                                          of motion (8, 9) for any sequence such that |xi+1 − xi | → 0 and
                 xn+1 − 2xn + xn−1
                                  
                                                                          |λi+1 − λi | → 0. Generally this method works well, however
         M                           = −∇U T (xn+1 ).              (4)
                        ∆t2                                               it may require a line search strategy to be robust, and computing
                                                                          the system matrix can be expensive. In particular, we would like
The energy potential U (x) may be further specified in terms of a         to avoid computing K, which requires the evaluation of constraint
                                                                          Hessians.
vector of constraint functions C = [C1 (x), C2 (x), · · · , Cm (x)]T
as                                                                        We now introduce two approximations that simplify the implementa-
                                                                          tion of our method and allow us to make a connection back to PBD.
                              1                                           First, we use the approximation that K ≈ M. This omits the geo-
                    U (x) =     C(x)T α−1 C(x),                    (5)    metric stiffness and constraint Hessian terms, and introduces a local
                              2
                                                                          error on the order of O(∆t2 ). We note that this approximation may
where α is a block diagonal compliance matrix corresponding to            change the rate of convergence, but it does not change the global
inverse stiffness. The force from an elastic potential is then given by   error or solution to the fixed-point iteration. Specifically, it can be
the negative gradient of U with respect to x,                             seen as a quasi-Newton method.
                                                                          Next, we assume that g(xi , λi ) = 0. This assumption is justified
               felastic = −∇x U   T
                                      = −∇C α T   −1
                                                       C.          (6)    by noting that it is trivially true for the first Newton iteration when
                                                                          initialized with x0 = x̃ and λ0 = 0. In addition, if the constraint
                                                                          gradients change slowly then it will remain small, and will go to zero
We convert this to a compliant constraint formulation by following        when they are constant. Furthermore, the modified linear system
Servin et al. [2006] and decomposing the force into its direction and     now corresponds to the optimality conditions for a mass-weighted
scalar components by introducing the Lagrange multiplier,                 minimization to the constraint manifold starting from the current
                                                                          iterate xi . This variational point of view was discussed in detail by
                      λelastic = −α̃−1 C(x).                       (7)    Goldenthal et al. [2007], and our method can be seen as a compliant
                                                                          version of their Fast Projection algorithm.

Here λelastic = [λ1 , λ2 , · · · λm ]T is a vector of constraint multi-   Including these approximations, our updated linear subproblem is
pliers. Henceforth we will drop the subscript unless necessary for        given by
clarity. Note that we have included the time step from the left-hand
side of Equation (4) by folding it into our compliance matrix and                                                                
defining α̃ = ∆tα
                  2.                                                                 M        −∇CT (xi )        ∆x           0
                                                                                                                     =−                 ,   (15)
                                                                                    ∇C(xi )     α̃              ∆λ        h(xi , λi )
Substituting in our expression for λ we have the discrete constrained
equations of motion:
                                                                          we may then take the Schur complement with respect to M to obtain
                                                                          the following reduced system in terms of the unknown ∆λ:

            M(xn+1 − x̃) − ∇C(xn+1 )T λn+1 = 0                     (8)
                                                                             h                        i
                              C(xn+1 ) + α̃λn+1 = 0,               (9)        ∇C(xi )M−1 ∇C(xi )T + α̃ ∆λ = −C(xi ) − α̃λi .                (16)

where x̃ = 2xn − xn−1 = xn + ∆tvn is called the predicted, or             The position update is then given directly by evaluating
inertial, position. To solve this non-linear system we design a fixed
point iteration based on Newton’s method. In the following, we
omit the time step superscript (n + 1) to emphasize the per-iteration                          ∆x = M−1 ∇C(xi )T ∆λ.                        (17)
unknown, indicated by the subscript (i + 1).
                                                                          Although the solution returned by our method can no longer be said
We label equations (8, 9) as g and h respectively. Our goal is to find    to solve the implicit equations of motion exactly, in practice the
an x and λ that satisfies:                                                error is small. We investigate the accuracy of our method further in
                                                                          Section 6.
                            g(x, λ) = 0                           (10)
                            h(x, λ) = 0.                          (11)    4.1   A Gauss-Seidel Update

                                                                          We now make a connection back to PBD by considering a Gauss-
Linearizing equations (10, 11) we obtain the following linear Newton      Seidel solution for our linear system of equations (16). If we take a
subproblem:                                                               single constraint equation with index j, we can directly compute its
                                                                          Lagrange multiplier change by evaluating
                                                
        K          −∇CT (xi ) ∆x         g(xi , λi )                                                   −Cj (xi ) − α̃j λij
                                    =−                            (12)                        ∆λj =                        .
       ∇C(xi )       α̃         ∆λ      h(xi , λi )                                                                                         (18)
                                                                                                      ∇Cj M−1 ∇CjT + α̃j
This equation forms the core of our method. During constraint             Substituting in our discrete approximation of velocity v =
solving, we first calculate ∆λj for a single constraint, then we           1
                                                                          ∆t
                                                                              (xn+1 − xn ), and linearizing with respect to λ, we have the
update the system positions and multipliers using Equations (13, 14).     following updated Newton step:
Algorithm 1 summarizes our method. It is identical to the original
PBD algorithm with the addition of lines 4, 7, and 9.
                                                                                                                            
If we examine the equation for ∆λj more closely, we can see that                                  α̃β̃          −1      T
                                                                                             (I +      )∇C(xi )M ∇C(xi ) + α̃ ∆λ = −h(xi , λi ).
in the case of αj = 0 it corresponds exactly to the scaling factor                                ∆t
sj in the original PBD algorithm (2). From our new definition, we                                                                           (25)
understand sj as being the incremental Lagrange multiplier change
for an infinitely stiff constraint. In the case of compliance, we
have αj ≥ 0, and an additional term in both the numerator and             In terms of a single constraint equation, our Gauss-Seidel update is
denominator appears. These terms act to regularize the constraint in      now given by
such a way that the constraint force is limited, and corresponds to
the elastic potential given by Equation (5).                                                                 −Cj (xi ) − α̃j λij − γj ∇Cj (xi − xn )
                                                                                                 ∆λj =                                               .          (26)
                                                                                                                (1 + γj )∇Cj M−1 ∇CjT + α̃j
The numerator in Equation (18) includes reference to λij . This is
the total Lagrange multiplier for constraint j at the current iteration
i. We must store and update this variable in addition to the system       A common case is that α̃ and β̃ are simple diagonal (as opposed to
positions. The additional storage of one scalar per-constraint is         block-diagonal), then we have γj = ∆t   j j               α̃ β̃
                                                                                                                      , i.e.: the time step scaled
a modest overhead, and provides useful information on the total           product of compliance and damping parameters for the constraint.
constraint force that can be used to drive force dependent effects        We stress that all the additional terms here are easily and efficiently
(e.g.: breakable joints), or haptic devices.                              computable.

5    Damping                                                              6                   Results
Our method is derived from an implicit time stepping scheme that          We test our method on a variety of deformable models and constraint
naturally includes some dissipation of mechanical energy. Neverthe-       types. For our 2D results we have used a CPU implementation with
less, it can be useful to model additional constraint damping. To do      Gauss-Seidel style iteration which we validate against a traditional
so, we define a Rayleigh dissipation potential                            non-linear Newton solver applied directly to the discrete equations
                                                                          of motion (8, 9). The Newton solver uses the robust Cholesky
                             1
                  D(x, v) =    Ċ(x)T β Ċ(x)                     (19)    decomposition from the Eigen math library [2010] as its linear
                             2                                            solver.
                             1
                            = vT ∇CT β∇Cv,                        (20)    Our 3D results were captured from a GPU based solver using a Ja-
                             2
                                                                          cobi style iteration on a NVIDIA GTX1070. Collisions are handled
                                                                          exactly as in the original PBD method. We assume zero compli-
where β is a block diagonal matrix corresponding to the constraint        ance in contact, meaning it is not necessary to store the Lagrange
damping coefficients. Note that β is not an inverse parameter like        multiplier for the contact constraint.
compliance, and should be set as a damping stiffness. According to
Lagrangian dynamics the force from a dissipation potential comes                   1.5
                                                                                                                                                                Exact
from the negative gradient of D with respect to velocity                           1.4
                                                                                                                                                                XPBD
                                                                                                                                                                PBD 1
                                                                                                                                                                PBD 5
                                                                                   1.3                                                                          PBD 10

                                 T           T
               fdamp = −∇v D = −∇C β∇Cv.                          (21)             1.2



                                                                                   1.1
                                                                          Offset




As in the elastic case, we separate the scalar component of this force              1




vector into a constraint multiplier                                                0.9



                                                                                   0.8



                 λdamp = −β̃ Ċ(x) = −β̃∇Cv,                      (22)             0.7



                                                                                   0.6



                                                                                   0.5
where we have included the time step in our damping parameter by                         0       10     20      30     40    50
                                                                                                                            Frame
                                                                                                                                            60   70   80   90            100




defining β̃ = ∆t2 β.
                                                                          Figure 2: A simple harmonic oscillator modeled as a distance
It is possible to solve for λdamp by itself, and in so doing obtain a     constraint with compliance α = 0.001. XPBD matches the analytic
constraint force multiplier for the damping and elastic components        solution closely, while PBD’s solution is heavily dependent on the
individually. However, in most cases we only care to know the total       number of iterations.
constraint force, and because the damping force must act along the
same direction as the elastic force, we can combine our multipliers
into a single equation                                                    6.1                  Spring

      λ = λelastic + λdamp = −α̃−1 C(x) − β̃∇Cv.                  (23)    We test our method on the case of a simple harmonic oscillator
                                                                          modeled as a distance constraint, with rest position of of x = 1,
                                                                          initial position x0 = 1.5, α = 0.001, and mass m = 1. As we
Re-arranging (23) into our constraint form we have                        can see from Figure 2, PBD cannot reproduce the correct period of
                                                                          oscillation. We plot the PBD simulation with 1,5, and 10 iterations
             h(x, λ) = C(x) + α̃λ + α̃β̃∇Cv = 0.                  (24)    to illustrate how PBD’s oscillation period and damping are heavily
            600                                                                          0.1
                                                    Newton                                                                                  Newton
                                                    XPBD 50                                                                                 XPBD (Gauss−Seidel)
                                                                                        0.09
                                                    XPBD 100                                                                                XPBD (Jacobi)
                                                    XPBD 1000
            550                                                                         0.08



                                                                                        0.07



            500                                                                         0.06




                                                                      |h ( x, λ ) | 2
Force (N)




                                                                                        0.05



            450                                                                         0.04



                                                                                        0.03



            400                                                                         0.02                                                                           Figure 5: A cantilever beam modeled with triangular FEM elements
                                                                                        0.01                                                                           and a linear, isotropic constitutive model, simulated for 50 frames.
            350
              75    80     85
                                 Frame
                                         90    95               100
                                                                                          0
                                                                                               0   5   10   15   20      25
                                                                                                                      Iteration
                                                                                                                                  30   35       40      45        50   Left: Reference Newton solver. Right: XPBD, using 20 iterations
                                                                                                                                                                       our method is visually indistinguishable from the reference.
                                (a)                                                                               (b)

Figure 3: (a) The constraint force magnitude at the fixed support
over a series of frames in the Chain example. (b) Residual error                                                                                                       The compliance matrix is then given by the inverse stiffness matrix,
in h(x, λ) for a single frame taken from the Beam example, both                                                                                                        which, in terms of the Lamé parameters is
Gauss-Seidel and Jacobi converge linearly as expected for an itera-
tive method.                                                                                                                                                                                                                  −1
                                                                                                                                                                                               λ + 2µ             λ          0
                                                                                                                                                                                 αtri = K−1 =  λ               λ + 2µ       0 .          (28)
                                                                                                                                                                                                  0                0        2µ
iteration count dependent. In this simple case XPBD closely repro-
duces the analytic result regardless of time step and iteration count.
We note that in this example the damping in the reference solution is                                                                                                  The advantage of this formulation over Strain-Based Dynamics
a side-effect of our implicit discretization of the equations of motion.                                                                                               [Müller et al. 2014] is that, not only does it correspond to traditional
                                                                                                                                                                       material parameters, it correctly couples the individual strains to
                                                                                                                                                                       model Poisson’s effect. This allows XPBD to accurately simulate
6.2                Chain
                                                                                                                                                                       models with material properties obtained from experimental data.
                                                                                                                                                                       We evaluate our algorithm’s accuracy by simulating a cantilever
                                                                                                                                                                       beam modeled using a St Venant-Kirchhoff triangular FEM dis-
                                                                                                                                                                       cretization (Figure 5). We use a linear, isotropic constitutive model
                                                                                                                                                                       with Young’s modulus of E = 105 , Poisson’s ratio µ = 0.3, and
                                                                                                                                                                       ∆t = 0.008. We run the simulation for 50 frames and find that 20
                                                                                                                                                                       iterations of XPBD are sufficient to be visually indistinguishable
                                                                                                                                                                       from our reference Newton solver. The residual error over iteration
                                                                                                                                                                       is plotted in Figure 3b.
Figure 4: A time-lapse view of a hanging chain of 20 particles
falling under gravity. Left: Reference Newton solver. Right: XPBD
with 50 iterations.                                                                                                                                                    6.4   Cloth


One of the key benefits of our method is its ability to return constraint
force magnitudes. An important question then, is how accurate are
the returned constraint forces? To quantify the error introduced by
the PBD update we simulate a weakly extensible chain of particles as
illustrated in Figure 4. The chain consists of 20 particles, each with
m = 1.0, and connected by distance constraints with α = 10−8 .
We simulate the scenario over 100 frames and measure the resultant
constraint force magnitude at the fixed particle at the top of the chain.
Figure 3a compares the result of our reference Newton solver’s
solution to XPBD’s. The maximum relative error for our method
over the course of the simulation is 6%, 2%, and 0.5% for 50, 100,
and 1000 iterations respectively. We believe this is acceptable for
most graphics applications.
                                                                                                                                                                       Figure 6: Hanging cloth with 20, 40, 80, and 160 iterations re-
                                                                                                                                                                       spectively (left to right). Top row: PBD, Bottom row: XPBD. PBD
6.3                Cantilever Beam
                                                                                                                                                                       stiffness is dependent on iteration count in a non-linear way, while
                                                                                                                                                                       XPBD’s behavior is qualitatively unchanged.
Traditional finite element methods (FEM) can be reformulated in the
compliant constraint framework [Servin et al. 2006]. In the case of a
linear isotropic constitutive model, the entries of the strain tensor                                                                                                 We test the iteration count independent nature of our algorithm
for each element are treated as a vector of constraint functions, here                                                                                                 by simulating a hanging cloth subject to gravity. The cloth model
in Voigt notation for a triangular element:                                                                                                                            consists of a 64x64 grid of particles connected by a graph of 24k
                                                                                                                                                                       distance constraints. In Figure 6 we show the effect of fixing the
                                                                                                                                                                     constraint stiffness and varying the iteration count. Cloth simulated
                                                             x                                                                                                        with PBD becomes progressively stiffer and more heavily damped
                                         Ctri (x) = tri =  y  .                                                                                   (27)             as iteration count increases, while in XPBD behavior is consistent
                                                            xy                                                                                                        regardless of iteration count.
To clearly show how the PBD behavior changes with varying itera-          only trivial modifications to an existing PBD solver we expect it to
tion counts we have used an artificially low constraint stiffness of      be easily adopted by industry and practitioners.
k = 0.01. We note that XPBD does not converge faster than PBD,
simply that behavior remains consistent at different iteration counts.    References
Indeed, in the limit of zero compliance XPBD is equivalent to a
constraint stiffness of k = 1 in PBD.                                     B ENDER , J., KOSCHIER , D., C HARRIER , P., AND W EBER , D.
We measure the performance impact of XPBD on our cloth example               2014. Position-based simulation of continuous materials. Com-
and find that it adds a small per-iteration cost that is typically less      puters & Graphics 44, 1–10.
than 2% of the total simulation time. Please refer to Table 1 for more    B ENDER , J., M” ULLER , M., OTADUY, M. A., T ESCHNER , M.,
detail.                                                                      AND M ACKLIN , M. 2014. A survey on position-based simulation
                                                                             methods in computer graphics. Computer Graphics Forum, 1–25.
Table 1: Per-step simulation time (ms) for the hanging cloth example
at varying iteration counts.                                              B OUAZIZ , S., M ARTIN , S., L IU , T., K AVAN , L., AND PAULY, M.
                                                                             2014. Projective dynamics: fusing constraint projections for fast
      Iterations        20          40          80         160               simulation. ACM Transactions on Graphics (TOG) 33, 4, 154.

      PBD              0.95        1.75        3.25        5.61           G OLDENTHAL , R., H ARMON , D., FATTAL , R., B ERCOVIER , M.,
                                                                            AND G RINSPUN , E. 2007. Efficient simulation of inextensible
      XPBD             0.97        1.78        3.34        5.65
                                                                            cloth. In ACM Transactions on Graphics (TOG), vol. 26, ACM,
                                                                            49.

6.5   Inflatable Balloon                                                  G UENNEBAUD , G., JACOB , B., ET AL ., 2010.             Eigen v3.
                                                                            http://eigen.tuxfamily.org.
We apply our method to an inflatable balloon where the interior air       L IU , T., BARGTEIL , A. W., O’B RIEN , J. F., AND K AVAN , L. 2013.
pressure is modeled using a global volume constraint, and the outer          Fast simulation of mass-spring systems. ACM Transactions on
surface as a cloth mesh with stretch, shear, and bending constraints         Graphics (TOG) 32, 6, 214.
(see Figure 1). In terms of additional storage, the interior volume
constraint requires only a single auxiliary multiplier, plus one multi-   M ÜLLER , M., H EIDELBERGER , B., T ESCHNER , M., AND G ROSS ,
plier for each surface constraint. Our method makes it easy to adjust        M. 2005. Meshless deformations based on shape matching.
the relative stiffness of constraints, for example, if necessary we may      In ACM SIGGRAPH 2005 Papers, ACM, New York, NY, USA,
increase solver iterations to obtain stronger volume preservation            SIGGRAPH ’05, 471–478.
without affecting surface stiffness.                                      M ÜLLER , M., H EIDELBERGER , B., H ENNIX , M., AND R ATCLIFF ,
                                                                             J. 2007. Position based dynamics. J. Vis. Comun. Image Repre-
7     Limitations and Future Work                                            sent. 18, 2 (Apr.), 109–118.
                                                                          M ÜLLER , M., C HENTANEZ , N., K IM , T.-Y., AND M ACKLIN ,
In the limit of α = 0 our method is identical to PBD with k = 1,             M. 2014. Strain based dynamics. In Proceedings of the ACM
and as such, requires the same number of iterations to obtain a stiff       SIGGRAPH/Eurographics Symposium on Computer Animation,
result. Similar to PBD, low iteration counts that terminate before          Eurographics Association, Aire-la-Ville, Switzerland, Switzer-
convergence will result in artificial compliance. Convergence speed         land, SCA ’14, 149–157.
may be improved by replacing Gauss-Seidel or Jacobi iteration with
a more sophisticated linear solver at each iteration. Recent work         NARAIN , R., OVERBY, M., AND B ROWN , G. E. 2016. ADMM
that focused on accelerated iterative methods such as the Chebyshev         ⊇ projective dynamics: Fast simulation of general constitutive
method presented by Wang et al. [2015] could be applicable.                 models. In Proceedings of the ACM SIGGRAPH/Eurographics
                                                                           Symposium on Computer Animation. To appear.
One promising avenue that our method opens up is temporal coher-
ence, because we now have a record of the total constraint force it       N EALEN , A., M ÜLLER , M., K EISER , R., B OXERMAN , E., AND
should be possible to warm-start the constraint solve based on the           C ARLSON , M. 2005. Physically Based Deformable Models
previous frame’s Lagrange multipliers.                                       in Computer Graphics. In Eurographics 2005 - State of the
                                                                            Art Reports, The Eurographics Association, Y. Chrysanthou and
Unlike Projective Dynamics [Bouaziz et al. 2014] our method is               M. Magnor, Eds.
only an approximation of an implicit Euler integrator. For real-time
graphical applications we believe the error is acceptable, and in         S ERVIN , M., L ACOURSIERE , C., AND M ELIN , N. 2006. Interactive
many cases indistinguishable. However, traditional methods may be            simulation of elastic deformable materials. In Proceedings of
more suitable for applications requiring greater accuracy guarantees.        SIGRAD Conference, 22–32.
                                                                          S TAM , J. 2009. Nucleus: Towards a unified dynamics solver for
8     Conclusion                                                             computer graphics. In Computer-Aided Design and Computer
                                                                             Graphics, 2009. CAD/Graphics’ 09. 11th IEEE International
We have presented a simple extension to position-based dynamics              Conference on, IEEE, 1–11.
that addresses its most well known limitation, namely, time step and      T OURNIER , M., N ESME , M., G ILLES , B., AND FAURE , F. 2015.
iteration count stiffness dependence. Our method requires comput-            Stable constrained dynamics. ACM Transactions on Graphics
ing and storing only a single additional scalar per-constraint, but          (TOG) 34, 4, 132.
allows PBD to simulate arbitrary elastic and dissipative energy poten-
tials. In addition, it can provide accurate constraint force estimates    WANG , H. 2015. A chebyshev semi-iterative approach for acceler-
for force dependent effects. We believe this widens the scope of           ating projective and position-based dynamics. ACM Transactions
PBD to applications which require greater accuracy and correspon-          on Graphics (TOG) 34, 6, 246.
dence to traditional material models. Because our method requires
