                                                      Rethinking Optimization with Differentiable
                                                         Simulation from a Global Perspective
                                               Rika Antonova∗ 1 , Jingyun Yang∗1 , Krishna Murthy Jatavallabhula2 , Jeannette Bohg1

                                                              1                          2
                                                                  Stanford University,       Massachusetts Institute of Technology


                                                      Abstract: Differentiable simulation is a promising toolkit for fast gradient-based
arXiv:2207.00167v1 [stat.ML] 28 Jun 2022




                                                      policy optimization and system identification. However, existing approaches to
                                                      differentiable simulation have largely tackled scenarios where obtaining smooth
                                                      gradients has been relatively easy, such as systems with mostly smooth dynam-
                                                      ics. In this work, we study the challenges that differentiable simulation presents
                                                      when it is not feasible to expect that a single descent reaches a global optimum,
                                                      which is often a problem in contact-rich scenarios. We analyze the optimization
                                                      landscapes of diverse scenarios that contain both rigid bodies and deformable ob-
                                                      jects. In dynamic environments with highly deformable objects and fluids, differ-
                                                      entiable simulators produce rugged landscapes with nonetheless useful gradients
                                                      in some parts of the space. We propose a method that combines Bayesian op-
                                                      timization with semi-local ‘leaps’ to obtain a global search method that can use
                                                      gradients effectively, while also maintaining robust performance in regions with
                                                      noisy gradients. We show that our approach outperforms several gradient-based
                                                      and gradient-free baselines on an extensive set of experiments in simulation, and
                                                      also validate the method using experiments with a real robot and deformables.
                                                      Videos and supplementary materials are available at https://tinyurl.com/globdiff.

                                                      Keywords: Differentiable simulation, Global optimization, Deformable objects



                                           1       Introduction

                                           Physics simulation is indispensable for robot learning: it has been widely used to generate synthetic
                                           training data, explore learning of complex sensorimotor policies, and also help anticipate the per-
                                           formance of various learning methods before deploying on real robots. An increasing volume of
                                           recent work attempts to invert physics engines: given simulation outputs (e.g. trajectories), infer the
                                           input parameters (e.g. physical properties of the scene, robot controls) that best explain the outputs
                                           [1, 2, 3, 4, 5]. Differentiable physics engines aim to offer a direct and efficient way to invert sim-
                                           ulation, and could enable fast gradient-based policy optimization and system identification. Works
                                           that we survey in the background section show a number of recent successes. However, to highlight
                                           the most promising prospects of differentiable simulation, works in this space focus primarily on
                                           scenarios where obtaining smooth gradients is relatively easy.
                                           With more research efforts gearing to develop (and use) differentiable physics engines, it is now
                                           crucial that we analyze the limits of these systems thoroughly. Surprisingly, efforts to investigate the
                                           differentiability of these simulators are far and few. One prior work [6] has highlighted a few funda-
                                           mental limitations of differentiable simulation in the presence of rigid contacts, in low-dimensional
                                           systems. In this work, we first investigate the quality of gradients by visualizing loss landscapes
                                           through differentiable simulators for several robotic manipulation tasks of interest. For this analysis
                                           we create several new challenging environments, and also use environments from prior work.
                                               ∗
                                               Rika and Jingyun contributed equally. Contacts: {rika.antonova, jingyuny}@stanford.edu.
                                           This project was supported in part by a research award from Meta. Rika was supported by the National Science
                                           Foundation grant No.2030859 to the Computing Research Association for the CIFellows Project.
Our main focus is to understand whether the limitations of rigid contacts are also prevalent across
deformable object simulation. We show that in many cases obtaining well-behaved gradients is fea-
sible, but challenge the assumption that differentiable simulators provide easy landscapes in suffi-
ciently interesting scenarios. We analyze scenarios with flexible deformable objects (cloth), plastics
(clay), and fluids. Our visualizations of optimization landscapes uncover numerous local optima and
plateaus, showing the need for extending gradient-based methods with global search. We propose
a method that combines global search using Bayesian optimization with a semi-local search. Our
semi-local strategy allows to make progress on parts of the landscape that are intractable for gradi-
ent descent alone. In our experiments we show visual, quantitative and qualitative analysis of the
optimization problems arising from simulations with deformables in a variety of scenarios. We also
validate our proposed approach on a real robot interacting with cloth, where our aim is to identify
the properties of the cloth that make the motion of the simulated cloth match the real one.

2   Background
Differentiable Simulation: The earliest differentiable simulators [7, 8] focused solely on rigid-body
dynamics, often operating only over a small number of predefined object primitives. A number of
approaches subsequently focused on arbitrary rigid body shapes [9, 10], articulations [11, 12, 13],
accurate contacts [14, 15, 16], scalability [17], speed [18, 19], and multiphysics [1]. Differentiable
simulation has also been explored in the context of deformable objects [20], cloth [21], fluids [22],
robotic cutting [23] and other scientific and engineering phenomena [24, 25, 26]. While several
approaches sought to achieve physically accurate forward simulations and their gradients, they did
not rigorously study the impact of their loss landscapes on inference. Most modern simulators are
plagued by two fundamental issues. First, they rely on gradient descent as an inference mechanism,
which makes the optimization dependent on a good initial guess. Second, the loss landscape for
contact-rich scenarios is laden with discontinuities and spurious local optima. This is evident even
in the most basic case of a single bouncing ball as shown in [19]. In this work, we also verify that
the issue is present in the more recent frameworks, such as Nimble [14] and Warp [27].
Global Search Methods: Global optimization tackles the problem of finding the global optimum
in a given search space. In our case, this could constitute finding the optimal parameters for a
controller (e.g. target position, velocity, force, torque) or physical parameters of a simulator to
make the behavior of simulated objects match reality. Global optimization includes several broad
families of methods: 1) space covering methods that systematically visit all parts of the space; 2)
clustering methods that use cluster analysis to decide which areas of the space could be promising;
3) evolutionary methods that start from a broad set of candidates and evolve them towards exploring
the promising regions; 4) Bayesian optimization (BO) that uses non-parametric approaches to keep
track of a global model of the cost function and its uncertainty on the whole search space. The
survey in [28] gives further details. Random search is also considered a global search method, and
is one of the few methods that guarantees eventually finding a global optimum. While data efficiency
can be a challenge, it is often a surprisingly robust baseline. Space covering and clustering methods
face significant challenges when trying to scale to high dimensions. The recent focus in global
optimization has been on evolutionary methods and BO, which can be successful on search spaces
with thousands of dimensions. Hence, in this work we compare methods based on random search,
evolutionary approaches and BO.
CMA-ES: One of the most versatile evolutionary methods is Covariance Matrix Adaptation - Evo-
lution Strategies (CMA-ES) [29]. It samples a randomized ‘generation’ of points at each iteration
from a multivariate Gaussian distribution. To evolve this distribution, it computes the new mean
from a subset of points with the lowest cost from the previous generation. It also uses these best-
performing points to update the covariance matrix. The next generation of points is then sampled
from the distribution with the updated mean and covariance. CMA-ES succeeds in a wide variety of
applications [30], and has competitive performance on global optimization benchmarks [31]. This
method does not make any restrictive assumptions about the search space and can be used ‘as-is’
i.e. without tuning. However, this method is technically not fully global — while it can overcome
shallow local optima, it can get stuck in deeper local optima.


                                                  2
Bayesian optimization (BO): BO views the problem of global search as seeking a point x ∗ to
minimize a given cost function f (x ): f (x ∗ ) = minx f (x ). At each trial, BO optimizes an auxiliary
acquisition function to select the next promising x to evaluate. f is frequently modeled with a
Gaussian process (GP): f (x ) ∼ GP(m(x ), k(x i , x j )). Modeling f with a GP allows to compute the
posterior mean f¯(x ) and uncertainty (variance) V ar[f (x )] for each candidate point x . Hence, the
acquisition function can select points to balance a high mean (exploitation) with high uncertainty
(exploration). The kernel function k(·, ·) encodes similarity between inputs. If k(x i , x j ) is large for
inputs x i , x j , then f (x i ) strongly influences f (x j ). One of the most widely used kernel  functions
                                                          xj |) = σk2 exp − 21 r T diag(``)−2r , where σk2 , `
                                                                                              
is the Squared Exponential (SE): kSE (rr ≡ |x       xi −x
are signal variance and a vector of length scales respectively. σk2 , ` are hyperparameters and are
optimized automatically by maximizing the marginal data likelihood. See [32] for further details.


3    BO-Leap: A Method for Global Search on Rugged Landscapes

We propose an approach for global search that can benefit from gradient-based descents and em-
ploys a semi-local strategy to make progress on rough optimization landscapes. To explore the loss
landscape globally, we use Bayesian optimization (BO). BO models uncertainty over the loss and re-
duces uncertainty globally by exploring unseen regions. It also ensures to return to low-loss regions
to further improve within the promising areas of the search space. BO uses an acquisition function
to compute the most promising candidate to evaluate next. We treat each candidate as a starting
point for a semi-local search. As we show in our experiments, the straightforward strategy of using
gradient descent from each of these starting points does not ensure strong performance in scenar-
ios with noisy gradients. Hence, we propose a hybrid descent strategy that combines gradient-free
search with gradient-based descents. For this, we collect a small population of local samples and
compute a sampling distribution based on CMA-ES. Instead of directly using the resulting mean and
covariance to sample the next population (as CMA-ES would), we use gradient descent to evolve
the distribution mean, then use this updated mean when sampling the next population.
We outline our method, BO with semi-local
leaps (BO-Leap), in Algorithm 1. We also vi-                                                    Global
                                                                       or                       Search
sualize the algorithm in Figure 1. We start by
initializing a global model for the loss with a                                                    Semi-local
                                                                                                   Leaps
Gaussian process (GP) prior. Using the BO ac-
quisition function, we sample a vector x 1 of
simulation or control parameters to evaluate.                            Local Minimum             Gradient
                                                                                                   Descent
We then run a semi-local search from this start-
                                                                                         Structure of our method
ing point. For this, we initialize the popula- Loss
tion distribution N µ 1 = x 1 , σ12C 1 and sam-
ple K local candidates. Next, we update the             Parameter
distribution in a gradient-free way similar to the
CMA-ES strategy. We then start a gradient de-
scent from the updated mean s 1 . The gradient         Figure 1: A conceptual illustration of BO-Leap.
descent runs for at most J steps and is halted if the loss stagnates or increases for more than three
steps. The gradient is clipped to avoid leaving the search space boundaries. When the semi-local
search reaches a given number of steps (e.g. 100 in our experiments), we update the BO posterior
and let BO pick a new starting point x2 globally. We add all the points that the semi-local search
encounters to the set S n that is used to compute the posterior for each BO trial.
Obtaining a noticeable improvement by incorporating gradients into a strategy based on CMA-ES
is not trivial. One hybrid approach that seems conceptually sound proposes to shift the mean of
each CMA-ES population by taking a step in the direction of the gradient [33]. In our preliminary
experiments, taking a single gradient step was insufficient to significantly improve the performance
of CMA-ES: the method from [33] performed worse than gradient-free CMA-ES. In contrast,
our semi-local search strategy allows gradient-based descents to take large leaps on the parts of the
landscape where gradients are relatively smooth. To prevent being mislead by unstable gradients


                                                       3
Algorithm 1: BO-Leap : Bayesian Optimization with Semi-local Leaps
 1 Initialize : S 0 ← {}                                        . Set of points seen so far (initially empty)
                L ← GP m(x ) =0 , k(x , x0 ) |S 0
                                                      
 2                                                               . Gaussian process as a global loss model
 3              BO acquisition function ← LCB                                    . Lower Confidence Bound
 4 for n = 1..max steps do
                                        
 5      GP S n = GP m(·), k(·, ·)|S n              . Compute GP posterior using Eq. 2.25-26 from [34]
 6     x n ← arg minx LCB x | GP S n                   . Get next simulation (or control) parameter vector
 7     µ 1 ← x n ; σ1 ← 1.0; C 1 ← I (identity); K=10              . Initialize local population distribution
 8      for i = 1..local stepsdo
 9          x k ∼ N µ i , σi2C i , k = 1..K                              . Sample K population candidates
10          lk ← Sim(x k ), k = 1..K             . Compute losses lk with x k as sim/control parameters
11          Kbest ← sort(lk )                                         . Get candidates with the lowest loss
                      1
                          P
12          s 1 = |Kbest | k∈Kbest  x k       . Compute    descent start point (CMA-ES population mean)
13          for j = 1..J do
14              lk , ∇Sim |s j ← Sim(s j )                   . Compute sim. loss lj and gradients ∇Sim |s j
15              s j ← s j−1 − α∇Sim |s j                                               . Take a gradient step
16              Break if lj stagnates for more than 3 steps
17          µ i+1 ← s J ; σi+1 , C i+1 ← Eq.14-17 from [29] . Update local population distribution
18          S n+1 = S n ∪ {(s j , lj )}Jj=1 ∪ {(x k , lk )}K
                                                           k=1               . Update data for GP posterior


and avoid wasting computation when stuck on a plateau, our method monitors the quality of the
gradient-based evolution of the mean and terminates unpromising descents early. BO-Leap oper-
ates on three levels: global, semi-local and local (gradient descent), which allows it to tackle loss
landscapes that are challenging due to various aspects: local optima, non-smooth losses, and noisy
gradients. In the next section, we show that BO-Leap has strong empirical performance in contact-
rich scenarios with highly deformable objects, plastic materials and liquid.


4   A Suite of Differentiable Simulation Scenarios

       Framework         Simulation Type     Supported Models                  Environments
                                                                         Cartpole, 3-Link Cartpole*,
       Nimble [14]         Mesh-based               Rigid
                                                                                   Pinball*
        Warp [27]           Multiple       Rigid, deformable, fluid               Bounce*
     DiffTaichi [19]        Multiple       Rigid, deformable, fluid         Fluid*, Swing*, Flip*
                                                                      Assembly, Pinch, RollingPin, Rope,
     PlasticineLab [2]    Particle-based     Rigid, deformable
                                                                       Table, Torus, TripleMove, Writer
Table 1: Summary of differentiable simulation frameworks and environments we use in this work. We used
several existing environments and created new ones (marked with asterisks *). See supplement for more details.

In this work, we implement scenarios using several differentiable simulation frameworks. Table 1
summarizes their properties. Our main goal is to study scenarios with deformables, because prior
works already explored a number of tasks limited to rigid-body motion (see previous section). That
said, very few works considered contact-rich tasks, and one prior work highlighted the potential
fundamental limitations of gradients for rigid contacts [6]. Hence, there is a need to further study
the fundamentals of how loss landscapes and gradient fields are affected by rigid contacts. For that,
we created several scenarios using Nimble [14] and Warp [27] frameworks (described below).

               3-Link Cartpole: an extension of the classic Cartpole to get more challenging dynam-
               ics. Here, a 3-link pole needs to reach the blue target with its tip. Cart velocity and
               joint torques are optimized for each of the 100 steps of the episode, yielding a 400-
               dimensional optimization problem.


                                                      4
                Pinball and Bounce: a ball launches and bounces off colliders as in a pinball game.
                We optimize orientations of n colliders to route the ball from the top to the blue target
                at the bottom. Pinball helps analyze effects of increasing the number of contacts,
                implemented in Nimble [14]. We also created a simplified Bounce scenario to study
effects of a single collision in Warp [27], which produced well-behaved gradients in prior work [23].

To go beyond rigid objects, mesh-based simulations can model highly deformable objects, such as
cloth. Particle-based simulators can model interactions with granular matter and liquids, plastic
deformation with objects permanently elongating, buckling, bending, or twisting under stress. We
created several mesh-based and particle-based environments that involve deformables using Diff-
Taichi [19] and compared the quality of the loss landscapes and gradient fields they yield. We also
included environments from the PlasticineLab [2] that focus on plastic deformation.
              Fluid: a particle-based fluid simulation that also involves two rigid objects (a spoon
              and a sugar cube) interacting in fluid. The objective is to scoop the sugar cube out of
              the liquid. We optimize forward-back and up-down velocity of the spoon, and let it
              change fives times per episode, yielding a 10-dimensional optimization problem.
              Assembly, Pinch, RollingPin, Rope, Table, Torus, TripleMove, Writer: scenarios based
              on PlasticineLab [2] with particle-based simulations of plastic deformation. We opti-
              mize 3D velocities of anchors or pins, allowing them to change five times per episode.
              This yields a 90D problem for TripleMove, 30D for Assembly, 15D for the rest.
              Swing: a basic cloth swinging scenario to study dynamic tasks with deformables. We
              give options to optimize the speed of the anchor that swings the cloth, the cloth width
              & length, and stiffness of cloth that is partitioned into n×m patches. Varying n, m lets
              us experiment with effects of increasing dimensionality of the optimization problem.
              Flip: a scenario with highly dynamic motion and rigid-deformable object collisions.
              The goal is to flip a pancake by moving the pan. We optimize pan motion: n waypoints
              for left-right, up-down position and pan tilt. The pancake is modeled using a mass-
              spring model with small stiffness to avoid large forces from dynamic movement.
We built this suite of environments to be representative of a wide range of possible robot manipu-
lation scenarios, regardless of whether differentiable simulators produce sensible gradients in them.
We found that some of these environments yield high-quality gradients, while others do not. In
Section 5.1, we show that Cartpole, Fluid, and the eight PlasticineLab environments produce well-
behaved gradients and that our method can outperform competing baselines in these scenarios. Then,
in Section 5.3, we show that differentiable simulators can produce incorrect gradients in highly dy-
namic and contact-rich environments like Pinball, Swing, and Flip, which makes gradient-based
methods (including our method) less effective in these environments.


5     Experiments and Analysis of Optimization Landscapes

In this section, we present visual analysis of optimization landscapes and gradients, as well as com-
parison experiments, in various environments. We use Rand (random search) and CMA-ES as our
gradient-free baselines; we use RandDescents, an algorithm that runs multiple gradient descents
with randomly sampled initial parameter value, and BO as our gradient-based baselines.


5.1   Simulation Experiments and Analysis

We first analyze using gradients with rigid objects. The left side of Figure 2 shows experiments on
the 1-Link Cartpole, where gradient-free CMA-ES performs similar to gradient-based algorithms
(RandDescents, BO), while BO-Leap obtains a significantly lower loss. The right side shows results
for 3-Link Cartpole which has much more complex dynamics. Here, all gradient-based algorithms


                                                   5
show a large improvement over gradient-free ones. CMA-ES does better than a completely random
search (Rand), but fails to lift the pole tip to the target.
On the top-right corner of Figure 2, we show
qualitative results from a CMA-ES run (top)
and from a BO-Leap run (bottom), where BO-
Leap brings the tip close to the target.
Next, we study a variety of scenarios that use
particle-based simulation. Particle simulators
have much larger computational and memory
requirements than mesh-based options. Gradi-
ent computations further increase resource re-
quirements. For the differentiability to be war-
ranted, benefits of gradients have to be signif- Figure 2: Left: results for 1-Link Cartpole. Right: re-
icant. We show that gradient-based methods sults for 3-Link Cartpole. For all bar charts in this pa-
                                                    per, the vertical axis shows the mean and 95% confi-
can indeed have large benefits. Figure 3 visual- dence interval of best loss value after 1,000 optimiza-
izes the Fluid scenario: the left side shows a 2D tion steps. Each optimization step runs one simulation
slice of the loss landscape. It has many valleys episode, computes the loss, and propagates the gradient
with shallow local optima and appears more wrt. optimization parameters if the algorithm needs it.
difficult than many test landscapes designed to
challenge global optimization methods. The middle of Figure 3 shows directions of gradients pro-
duced by the differentiable simulator. The right side shows results for gradient-based and gradient
free methods. CMA-ES gets stuck in a local optimum: the spoon fails to lift the sugar cube in most
runs as shown in the next-to-last column. In contrast, BO-Leap successfully lifts the sugar cube in
most runs, outperforming all baselines. BO is designed to balance allocating trials to global explo-
ration while still reserving enough trials to return to the well-explored regions that look promising.
In this scenario such global optimization strategy proves to be beneficial. Furthermore, BO-Leap
also handles the rough parts of the landscape more effectively than the baseline BO.
In the next set of experiments, we analyze eight environments from PlasticineLab [2]. Figure 4
shows a Rope scenario, where the objective is to wrap it around a rigid cylindrical pole. The loss
landscape is smooth in most dimensions (the left plot shows an example 2D slice). However, higher
dimensionality makes the overall problem challenging. The middle plot confirms that gradients
are correct in most parts, but also shows a large plateau where even the gradient-based approaches
are likely to get stuck. The right side shows evaluation results: CMA-ES and BO fail to wrap the
rope fully around the pole, while BO-Leap succeeds in pulling the ends on the back side of the
pole correctly. This environment also shows that simply using gradients with random restarts is not
sufficient even on smooth landscapes: RandDescents has poor performance that does not improve
significantly over gradient-free random search.




Figure 3: A scenario with scooping up a sugar cube from fluid. The left side shows a 2D slice of the 10D
optimization landscape and the corresponding gradients. To make gradient directions visible, we normalize
the magnitude of gradients in all gradient plots in this paper; the arrows point towards the direction of negated
gradients (i.e. the direction gradient descent updates take). The right plot shows quantitative evaluation of
optimization methods. We visualize qualitative results for CMA-ES and BO-Leap on the right side.




                                                       6
Figure 4: Results for the Rope environment. BO-Leap outperforms all other methods and successfully com-
pletes the task of wrapping the rope fully around the pole (light blue region shows the target shape). Gradient-
free CMA-ES cannot reliably get the optimal behavior. While BO-Leap uses gradients effectively, this scenario
shows that simply using gradients with random restarts is not sufficient: RandDescents has poor performance.




Figure 5: Top row: analysis and results for RollingPin task. Bottom rows: results for the other six PlasticineLab
tasks. Plots show mean performance over 10 runs of each method per task (see supplemental for further details).
Environment illustrations below the six bar charts at the bottom of this figure are borrowed from [2].

Figure 5 shows experiments with the other seven PlasticineLab tasks. The top shows the RollingPin
task, where the objective is to spread the dark-blue dough using a thin rigid cylindrical white pin
(the light-blue region shows the target shape). The loss landscape is smoother than that of the Rope
task, but has even larger plateaus and flat gradients in most regions, making the problem challenging
despite a smooth loss. BO-Leap outperforms CMA-ES and gradient-based methods on this task as
well. Example frames on the right show that CMA-ES thins out the dough too much (large gaps
appear in the middle, revealing the light-blue target shape underneath). BO and BO-Leap keep the
central portion of the dough more uniformly spread. The bottom plots show results for the additional
six PlasticineLab tasks. BO-Leap outperforms gradient-based methods in all tasks, and achieves
significantly lower loss than CMA-ES in Assembly, Torus, and TripleMove tasks (see supplementary
materials for further details).

5.2 Validation in Real Robot Setup

To validate the proposed method using real data, we consider the task of identifying the properties
of a simulated deformable object to make its motion match the real motion. In this scenario, a
Gen3 (7DoF) Kinova robot manipulates a small deformable object by lifting it up from the table
surface. The object is tracked by two RealSense D435 depth cameras, one placed overhead, the
other on the side. The objective is to optimize the size (width & length), mass, and friction of the
deformable object, as well as stiffness of each of the 8×8 = 64 patches of the object, which yields
a 68D optimization problem. The loss penalizes the distance of the simulated corner vertices to the
position of the corners marked on the real object. Figure 6 shows results of experiments with two


                                                       7
Figure 6: Results for optimizing a simulated object to match the motion of a real paper (left) and cloth (right),
which are lifted by a real robot. We visualize the midway alignment showing that our method finds the size,
mass, friction and stiffness (for each of the 64 patches) to bring simulated object behavior close to the real one.

objects: a stiff but flexible paper (left) and a highly flexible cloth (right). In both cases, BO-Leap is
able to find physical simulation parameters that produce the best alignment of the simulated and real
object. This offers a validation of the method on real data, and shows that it can tackle ‘real2sim’
problems to automatically bring the behavior of simulated objects closer to reality. This is valuable
for highly deformable objects, since manual tuning is intractable for high dimensions.

5.3   Limitations

Modeling global loss posterior with BO can be computationally expensive. We use BoTorch [35]
for BO on GPU, which can scale to high dimensions. We focused on results within a budget of 1K
optimization steps. If a much larger budget is allowed, then more tests would be needed to validate
that BoTorch (or other frameworks) can scale well in terms of compute and memory resources.




Figure 7: Visual insights into the challenges of obtaining well-behaved gradients for cases with rigid contacts
in Pinball, and for deformables in the presence of contacts and highly dynamic tasks, such as Swing & Flip.
The biggest challenges of optimization with differentiable simulators arise due to quality of the
gradients, which can be insufficient to be beneficial for gradient-based algorithms, including our
method. In Figure 7, we show three environments where gradients produced by differentiable simu-
lators are of poor quality. In the Pinball environment, gradients with respect to collider orientations
are computable only if a collision (with the pinball) has occurred to begin with. In addition to
collision-induced discontinuities, the absence of gradients results in plateaus, affecting gradient-
based optimizers. Even in a state-of-the-art simulator Warp [27] with relaxed contact models, a
simple Bounce task induces gradient discontinuities (see supplement for details). In Swing and Flip
tasks, while the dynamics appear realistic, differentiable simulators yield gradients with incorrect
(often opposite) directions. This is a common pitfall for practitioners who use differentiable simu-
lators without assessing loss landscapes first.

Conclusion Our analysis shows that differentiable simulation of contact-rich manipulation sce-
narios results in loss landscapes that are difficult for simple gradient-based optimizers. To overcome
this, we proposed a hybrid approach that combines local (gradient-based) optimization with global
search, and demonstrated success on rugged loss landscapes, focusing on cases with deformables.
We believe our analyses and tools provide critical feedback to differentiable simulator designers and
users alike, to take differentiable simulators a step closer to real-world robot learning applications.


                                                        8
Appendix
A     Additional Environment Descriptions and Details

In this section, we list details of environments we covered in the paper. We describe the simula-
tion framework, physics model, contact type, parameter information, loss configuration, as well as
landscape and gradient characteristics for each environment.

A.1     Rigid Body Environments

A.1.1    3-link Cartpole




                        Figure A.1: Illustration of the 3-link Cartpole environment.
A cart carries a triple inverted pendulum where each link has length 1m. Links farther away from
the cart are lighter than the link attached to the cart (for easier control). The goal is to move the cart
and actuate the joints so that the tip of the pendulum is as close as possible to a preset goal location.

 • Simulation Framework or Physics Model: Nimble [14]
 • Types of Contacts: none (there is no self-contact between different parts of the cartpole)
 • Parameter Dimensionality: 400
 • Parameter Description: at each of the 200 timesteps, the parameters specify cart velocity with
   1 dimension and torques of 3 joints.
 • Loss: L2 distance from final tip position to target position.
 • Landscape and Gradient Characteristics: landscape is very smooth. Gradient quality is good.


A.1.2    Pinball




                   Figure A.2: Illustration of the Pinball environment with 16 colliders.


On a vertical platform of 8m wide and 10m tall, a ball is dropped on to a grid of nh × nw spinning
colliders that have one revolute joint each attached to the platform. The goal is to guide the ball to a
goal position at the end of the episode by adjusting the orientation of each collider.

 • Simulation Framework or Physics Model: Nimble [14]
 • Types of Contacts: rigid (pinball collides with colliders and walls)
 • Parameter Dimensionality: nh × nw (in this work, we consider two setups with nh = 1, nw =
   2 and nh = 4, nw = 4)
 • Parameter Description: rotation angle of each spinning collider in the nh × nw grid.


                                                     9
 • Loss: L2 distance from final pinball position to target pinball position near the bottom-right of
   the platform.

 • Landscape and Gradient Characteristics: landscape has large flat regions as well as disconti-
   nuities. Gradients are zero in flat regions and not useful at locations of discontinuities.


A.2     Deformable Object Environments

A.2.1    Fluid




Figure A.3: Illustration of the Fluid environment. The upper and lower rows are renderings of the same episode
in the same environment. The upper row uses the built-in realtime rendering engine in DiffTaichi; while the
lower row uses Blender, which is slower but higher quality.

A ladle with 2 DOF is manipulated to scoop a sugar cube from a tank of transparent syrup with
width 0.4m, depth 0.4m, and height 0.2m. The goal is to scoop the cube to as high of a position as
possible while being close to the ladle and the center vertical axis of the tank. This environment is
made with DiffTaichi. The dynamics of syrup and the sugar cube in this environment are modeled
with MLS-MPM [36], a state-of-the-art particle-based fluid simulation method.

 • Simulation Framework or Physics Model: DiffTaichi [19] with MLS-MPM [36] as physics
   model for fluid and the sugar cube

 • Types of Contacts: collision between rigid objects and fluid (such as fluid particles bouncing
   back off container walls)

 • Parameter Dimensionality: 10

 • Parameter Description: an episode splits into 5 equal-length segments. In each segment, 2
   parameter values control the horizontal (forward-backward) and vertical (up-down) speed of the
   ladle. Note that although the ladle might not directly make contact with the cube, the ladle can
   push the liquid particles, which can then push the cube away from the ladle.
                              p                              p
 • Loss: max(0, y −yw )+3· (x − xs )2 + (z − zs )2 + (x − xc )2 + (z − zc )2 , where (x, y, z)
   denotes the final sugar cube position, (xs , ys , zs ) denotes final ladle body center position, and
   yw = 0.2 denotes height of the container. In this and all following DiffTaichi environments, the
   x-axis points rightward, y-axis points upward, z-axis points to the front.

 • Landscape and Gradient Characteristics: landscape is rugged and has many local minima.
   Gradient quality is good.


                                                     10
A.2.2   PlasticineLab Environments




Figure A.4: Illustration of environments derived from PlasticineLab. From top to bottom, we show Assembly,
Pinch, RollingPin, Rope, Table, Torus, TripleMove, and Writer.
We consider 8 different environments derived from PlasticineLab [2] — Assembly, Pinch, Rolling-
Pin, Rope, Table, Torus, TripleMove, and Writer. These environments involve 1-3 anchors or a pin
manipulating one or several pieces of deformable objects. The goal of all environments are to make
the final deformable object configuration close to a target shape. When we adapt the environments
for our purpose, we only modify the format of optimizable parameters and leave other aspects of
the environments such as dynamics, episode length, and loss formulation unchanged. As we already
described the high-level objectives of several PlasticineLab environments we analyzed in detail in
the main paper, we direct readers to the original paper [2] for additional details of each environment.


                                                   11
 • Simulation Framework or Physics Model: PlasticineLab is based on DiffTaichi [19]; its envi-
   ronments use MLS-MPM [36] to model interactions between rigid and deformable objects; rigid
   bodies are modeled using signed distance fields (SDF)
 • Types of Contacts: collision between rigid and deformable objects
 • Parameter Dimensionality: 90 (TripleMove), 30 (Assembly, Rope), 15 (Pinch, RollingPin,
   Table, Writer)
 • Parameter Description: an episode splits into 5 equal-length segments. In each segment, the
   3D velocities of each anchor or pin are controlled by optimizable parameters. In TripleMove,
   there are six anchors to be controlled, so the optimizable parameter has a total of [5 segments
   × 6 anchors × 3 velocity values = 90] dimensions. In Assembly and Rope, there are two
   anchors to be controlled, so the parameter has [5 segments × 2 anchors × 3 velocity values = 30]
   dimensions. In Pinch, Table, and Writer, there is one anchor, so the parameter has [5 segments ×
   1 anchor × 3 velocity values = 15] dimensions. In RollingPin, instead of controlling 3D velocity
   of the pin in each segment, the environment uses 3 values to control the left-right, up-down, and
   top-down tilting angle of the pin, leading to [5 segments × 1 anchor × 3 control parameters =
   15] dimensions.
 • Loss: PlasticineLab uses a 3-part loss that encourages the anchors or pins to be closer to the
   deformable objects while penalizing the distance between the final deformable object shape and
   the target shape. The only modification we made to the original loss function is increasing the
   weight of the loss component that encourages the manipulators to get close to the target shape.
   For more details of the original loss function, please refer to Section 3.1 of the original paper [2]).
 • Landscape and Gradient Characteristics: the landscape is smooth with local minima, while
   the high dimensionality makes the problem challenging; gradient quality is good.


A.2.3   Swing




Figure A.5: Illustration of the Swing environment. The upper and lower rows are renderings of the same episode
in the same environment. The upper row uses the built-in realtime rendering engine in DiffTaichi; while the
lower row uses Blender, which is slower but has higher quality.
Two anchors grasp the two corners of a 20 × 20cm piece of cloth and swing it onto the floor. The
goal is to make the final cloth configuration as close as possible to a goal configuration.
 • Simulation Framework or Physics Model: DiffTaichi with mass-spring model as cloth sim-
   ulation technique; to handle contact, we update the velocities of cloth vertices when contacts
   occur so that the updated speed is perpendicular to the normal of the contact surface
 • Types of Contacts: collision between rigid (floor) and deformable objects (cloth)
 • Parameter Dimensionality: 16 if stiffness is optimized; 3 if initial speed is optimized
 • Parameter Description: we have two different parameter setups in this task. In the first setup,
   we split the cloth into 4 × 4 = 16 cloth patches and fix the swinging motion. The stiffness values
   of the 16 cloth patches are optimized. In the second setup, we fix the stiffness of the cloth and
   optimize the initial 3D velocity of the cloth.


                                                     12
 • Loss: we have three different loss formulations for this task — loss formulation ‘single’ opti-
   mizes the distance between the center of mass of the cloth at the final frame to a goal position.
   Loss formulation ‘corner’ optimizes the average distance between the four corners of the cloth
   to their corresponding goal positions. Loss formulation ‘mesh’ optimizes the average distance
   between final vertex positions of the cloth to a target cloth mesh.

 • Landscape and Gradient Characteristics: landscape is rugged. Gradients are noisy in large
   areas of the parameter space.


A.2.4   Flip




Figure A.6: Illustration of the Flip environment. The upper and lower rows are renderings of the same episode
in the same environment. The upper row uses the built-in realtime rendering engine in DiffTaichi; while the
lower row uses Blender, which is slower but has higher quality.

A pancake is placed in a pan with 20cm radius and smooth edges that move and tilt with 3 DOF. The
goal is to manipulate the pan so that the pancake is flipped at the end of the episode.

 • Simulation Framework or Physics Model: DiffTaichi with mass-spring model for simulating
   the pancake; compared to the Swing task, the stiffness value in this task is smaller to make
   sure collision forces are not too large during the dynamic movement of the pancake; to handle
   contact, we update the velocities of pancake vertices when contacts occur so that the updated
   speed is perpendicular to the normal of the contact surface

 • Types of Contacts: collision between rigid (floor) and deformable objects (pancake)

 • Parameter Dimensionality: 15

 • Parameter Description: an episode is split into 5 equal-length segments. The parameters set
   the x (left-right) and y (up-down) positions as well as the tilt of the pan at the end of each
   segment. This leads to [5 segments × 3 control parameters = 15] dimensions; position and
   angular velocity of the pan is linearly interpolated within each segment.

 • Loss: average L2 distance between final position of the four pancake corners (the four pancake
   vertices with highest and lowest x and y values at the start of the episode) and four corresponding
   target positions.

 • Landscape and Gradient Characteristics: landscape is extremely rugged. Gradients are noisy
   in large areas of the parameter space.



                                                     13
B     Additional Analysis

B.1   Analysis of Challenges with Gradients for Rigid Contacts

In this section, we analyze the quality of gradients through a differentiable physics engine; observing
the nature of discontinuities induced by contact. We define the Bounce task, where the goal is to steer
a bouncing (red) ball with known friction and elasticity parameters to a target position (green). We
seek a policy that imparts an initial 3D velocity vinit to a ball such that, at the end of the simulation
time tmax , the center of mass of the ball achieves a pre-specified target position. Importantly, the
policy must shoot the ball onto the ground plane, and upon a bounce, reach the target location (this
is achieved by restricting the cone of velocities to contain a vertically downward component). This
enforces at least one discontinuity in the forward simulation.
We use the relaxed contact model from Warp [27], and compute the gradients for a wide range of
initial velocities (−10 to 10 m/s along both X and Y directions). Notice that, in the X-direction
(horizontal speeds), the gradients are smoother, as changes to X components of the velocity only
push the ball further (closer) to the goal, and have little impact on the discontinuities (bounces).
However, the Y -axis components of velocities (vertical speeds) tend to have a significant impact on
the location and nature of the discontinuities, and therefore induce a larger number of local optima.




Figure B.1: A simple rigid body Bounce task implemented using Warp [27]. The goal is to impart an initial
velocity to the red ball so that it reaches the target location (green) at the end of 2 seconds. The ball moves in
3D: X left-right, Y down-up, Z in-out of the image plane. We restrict out attention the Y direction and observe
that discontinuities caused by the rigid contacts remain, even in Warp – a recent framework with semi-implicit
Euler integration and advanced relaxed-contact and stiffness models.


While prior work (e.g., DiffTaichi [19]) has extensively analyzed gradients through similar contact
scenarios, they leverage the conceptually simple (but numerically unstable) Euler integrator and
perfectly elastic collisions. Warp [27], on the other hand, uses both a symplectic time integrator
and a contact model that includes both friction and elasticity parameters. Our Bounce experiments
confirm the fact that significant challenges with computing gradients through rigid contacts remain,
even in these more recent and advanced differentiable simulation frameworks.

B.2   Landscape Gallery

In this section, we present more landscape and gradient plots to provide more insight into the differ-
entiable simulation environments we presented in the paper. Apart from this section, we also present
animated landscape plots in the supplementary video.
Pinball Below, we show two landscape and gradient plots, one plotting the landscape of the Pin-
ball 2D environment with two colliders, and the other plotting a 2D slice for the Pinball 16D envi-
ronment with a grid of 4-by-4 colliders. In the right plot, the x and y axes correspond to the rotation
of the center two colliders at the bottom of the collider grid. From the plots, we see that the rugged
landscapes occur in different variations of the Pinball task.


                                                       14
                                                                                                              1.00                                                                                                                                      1.00
                                                                                                                                                                                                           8.5                                                                                                                                       6.80
                                                                                                              0.75                                                                                                                                      0.75
                                                                                                                                                                                                           7.6                                                                                                                                       6.08

                                                                                                              0.50                                                                                         6.7                                          0.50                                                                                         5.36




                                                                                                                                                                                                                    Rotation of collider #14 (dim 14)
                                                                            Rotation of collider #1 (dim 1)




                                                                                                              0.25                                                                                         5.8                                          0.25                                                                                         4.64

                                                                                                                                                                                                           4.9                                                                                                                                       3.92
                                                                                                              0.00                                                                                                                                      0.00




                                                                                                                                                                                                             Loss




                                                                                                                                                                                                                                                                                                                                                        Loss
                                                                                                                                                                                                           4.0                                                                                                                                       3.20
                                                                                                              0.25                                                                                                                                      0.25
                                                                                                                                                                                                           3.1                                                                                                                                       2.48
                                                                                                              0.50                                                                                                                                      0.50
                                                                                                                                                                                                           2.2                                                                                                                                       1.76

                                                                                                              0.75                                                                                         1.3                                          0.75                                                                                         1.04

                                                                                                              1.00                                                                                         0.4                                          1.00                                                                                         0.32
                                                                                                                     1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                                              1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00
                                                                                                                               Rotation of collider #0 (dim 0)                                                                                                           Rotation of collider #13 (dim 13)


Figure B.2: Landscape (top) and gradient (bottom) plots for Pinball environment. Left column – Pinball 2D
dimensions 0 and 1. Right column – Pinball 16D dimensions 13 and 14.


Fluid In the main paper, we presented Fluid as an environment where the landscape is rugged
and showed one 2D slice of the loss landscape of the 10D environment. Here, we show two more
slices of the landscape (the middle and right plots below). In the plots, we see that the optimization
landscape is similarly rugged in these dimensions.




                                      2.0                                                                                                                                        2.0                                                                                          0.72                                         2.0                                                        0.72

                                                                                                                                    0.72                                                                                                                                      0.64                                                                                                    0.64
                                      1.5                                                                                                                                        1.5                                                                                                                                       1.5
                                                                                                                                    0.64
                                                                                                                                                                                                                                                                              0.56                                                                                                    0.56
                                      1.0                                                                                                                                        1.0                                                                                                                                       1.0
                                                                                                                                    0.56
                                                                                                                                              Speed X for 40 <= t < 50 (dim 8)




                                                                                                                                                                                                                                                                                        Speed Y for 40 <= t < 50 (dim 9)
    Speed Y for 0 <= t < 10 (dim 1)




                                                                                                                                                                                                                                                                              0.48                                                                                                    0.48
                                      0.5                                                                                           0.48                                         0.5                                                                                                                                       0.5
                                                                                                                                                                                                                                                                              0.40                                                                                                    0.40
                                      0.0                                                                                           0.40                                         0.0                                                                                                                                       0.0
                                                                                                                                       Loss




                                                                                                                                                                                                                                                                                 Loss




                                                                                                                                                                                                                                                                                                                                                                                         Loss




                                                                                                                                                                                                                                                                              0.32                                                                                                    0.32
                                                                                                                                    0.32
                                      0.5                                                                                                                                        0.5                                                                                                                                       0.5
                                                                                                                                                                                                                                                                              0.24                                                                                                    0.24
                                                                                                                                    0.24
                                      1.0                                                                                                                                        1.0                                                                                                                                       1.0
                                                                                                                                    0.16                                                                                                                                      0.16                                                                                                    0.16

                                      1.5                                                                                                                                        1.5                                                                                          0.08                                         1.5                                                        0.08
                                                                                                                                    0.08

                                      2.0                                                                                           0.00                                         2.0                                                                                          0.00                                         2.0                                                        0.00
                                            2.0   1.5    1.0 0.5 0.0 0.5 1.0                                            1.5   2.0                                                      2.0   1.5    1.0 0.5 0.0 0.5 1.0 1.5                                            2.0                                                       2.0   1.5    1.0 0.5 0.0 0.5 1.0 1.5           2.0
                                                        Speed X for 0 <= t < 10 (dim 0)                                                                                                            Speed X for 30 <= t < 40 (dim 6)                                                                                                          Speed X for 40 <= t < 50 (dim 8)


Figure B.3: Landscape (top) and gradient (bottom) plots for Fluid environment with 10D parameters. Left
column – dimensions 0 and 1. Middle column – dimensions 6 and 8. Right column – dimensions 8 and 9.


Assembly Assembly is an environment in PlasticineLab where two anchors need to pick up a
soft purple ball on the left side of the scene and place it on a yellow stand on the right side. The


                                                                                                                                                                                                                 15
landscape and gradients plotted below show that these environments have smooth landscapes with
local minima and good quality gradients.




                                                  1.00                                                                                                               1.00                                                                                                                1.00

                                                                                                            43.50                                                                                                              43.75                                                                                                                41.4
                                                  0.75                                                                                                               0.75                                                                                                                0.75
                                                                                                            41.25                                                                                                              41.50                                                                                                                39.4




                                                                                                                                                                                                                                          Right anchor speed Z for 0 <= t < 10 (dim 5)
                                                                                                                       Left anchor speed Z for 0 <= t < 10 (dim 2)
    Left anchor speed Y for 0 <= t < 10 (dim 1)




                                                  0.50                                                                                                               0.50                                                                                                                0.50
                                                                                                            39.00                                                                                                              39.25                                                                                                                37.4

                                                  0.25                                                      36.75                                                    0.25                                                      37.00                                                     0.25                                                       35.4

                                                  0.00                                                      34.50                                                    0.00                                                      34.75                                                     0.00                                                       33.4
                                                                                                                Loss




                                                                                                                                                                                                                                   Loss




                                                                                                                                                                                                                                                                                                                                                        Loss
                                                                                                            32.25                                                                                                              32.50                                                                                                                31.4
                                                  0.25                                                                                                               0.25                                                                                                                0.25
                                                                                                            30.00                                                                                                              30.25                                                                                                                29.4
                                                  0.50                                                                                                               0.50                                                                                                                0.50
                                                                                                            27.75                                                                                                              28.00                                                                                                                27.4
                                                  0.75                                                                                                               0.75                                                                                                                0.75
                                                                                                            25.50                                                                                                              25.75                                                                                                                25.4

                                                  1.00                                                      23.25                                                    1.00                                                      23.50                                                     1.00                                                       23.4
                                                         1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                       1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                        1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00
                                                              Left anchor speed X for 0 <= t < 10 (dim 0)                                                                        Left anchor speed Y for 0 <= t < 10 (dim 1)                                                                         Right anchor speed Y for 0 <= t < 10 (dim 4)


Figure B.4: Landscape (top) and gradient (bottom) plots for Assembly environment with 30D parameters. Left
column – dimensions 0 and 1. Middle column – dimensions 1 and 2. Right column – dimensions 4 and 5.



Table In the Table environment, an anchor pushes one leg of a table so it points outward. The
visualizations below reveal that small changes in the action can result in very different loss values.




                                                  1.00                                                      55.0                                                     1.00                                                                                                                1.00                                                       20.28
                                                                                                                                                                                                                               86.4
                                                  0.75                                                      50.5                                                     0.75                                                                                                                0.75                                                       19.62
                                                                                                                                                                                                                               78.4
                                                                                                            46.0                                                                                                                                                                                                                                    18.96
                                                                                                                                                                                                                                          Anchor speed Z for 40 <= t < 50 (dim 14)




                                                  0.50                                                                                                               0.50                                                                                                                0.50
                                                                                                                       Anchor speed Z for 10 <= t < 20 (dim 5)
    Anchor speed Z for 0 <= t < 10 (dim 2)




                                                                                                                                                                                                                               70.4
                                                                                                            41.5                                                                                                                                                                                                                                    18.30
                                                  0.25                                                                                                               0.25                                                      62.4                                                      0.25
                                                                                                            37.0                                                                                                                                                                                                                                    17.64
                                                  0.00                                                                                                               0.00                                                      54.4                                                      0.00
                                                                                                                Loss




                                                                                                                                                                                                                                   Loss




                                                                                                                                                                                                                                                                                                                                                        Loss




                                                                                                            32.5                                                                                                                                                                                                                                    16.98
                                                                                                                                                                                                                               46.4
                                                  0.25                                                                                                               0.25                                                                                                                0.25
                                                                                                            28.0                                                                                                                                                                                                                                    16.32
                                                                                                                                                                                                                               38.4
                                                  0.50                                                                                                               0.50                                                                                                                0.50
                                                                                                            23.5                                                                                                               30.4                                                                                                                 15.66

                                                  0.75                                                      19.0                                                     0.75                                                                                                                0.75                                                       15.00
                                                                                                                                                                                                                               22.4

                                                  1.00                                                      14.5                                                     1.00                                                      14.4                                                      1.00                                                       14.34
                                                         1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                       1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                        1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00
                                                                Anchor speed X for 0 <= t < 10 (dim 0)                                                                             Anchor speed Z for 0 <= t < 10 (dim 2)                                                                             Anchor speed X for 40 <= t < 50 (dim 12)


Figure B.5: Landscape (top) and gradient (bottom) plots for Table environment with 30D parameters. Left
column – dimensions 0 and 2. Middle column – dimensions 2 and 5. Right column – dimensions 12 and 13.


                                                                                                                                                                                                   16
TripleMove In the TripleMove environment, six anchors manipulate three blocks to move them to
three corresponding goal positions. It can be seen in the plots below that the landscape generated by
this environment is pretty rugged.




                                               1.00                                                   85.2                                                 1.00                                                   76.2                                                     1.00
                                                                                                                                                                                                                                                                                                                                  71.75
                                               0.75                                                   81.2                                                 0.75                                                   73.2                                                     0.75
                                                                                                                                                                                                                                                                                                                                  69.25
                                                                                                      77.2                                                                                                        70.2
                                               0.50                                                                                                        0.50                                                                                                            0.50
                                                                                                                Anchor 0 speed Z for 0 <= t < 10 (dim 2)




                                                                                                                                                                                                                                Anchor 1 speed Z for 0 <= t < 10 (dim 5)
    Anchor 0 speed Y for 0 <= t < 10 (dim 1)




                                                                                                                                                                                                                                                                                                                                  66.75
                                                                                                      73.2                                                                                                        67.2
                                               0.25                                                                                                        0.25                                                                                                            0.25                                                   64.25
                                                                                                      69.2                                                                                                        64.2
                                               0.00                                                                                                        0.00                                                                                                            0.00                                                   61.75
                                                                                                         Loss




                                                                                                                                                                                                                         Loss




                                                                                                                                                                                                                                                                                                                                      Loss
                                                                                                      65.2                                                                                                        61.2
                                                                                                                                                                                                                                                                                                                                  59.25
                                               0.25                                                                                                        0.25                                                                                                            0.25
                                                                                                      61.2                                                                                                        58.2
                                                                                                                                                                                                                                                                                                                                  56.75
                                               0.50                                                                                                        0.50                                                                                                            0.50
                                                                                                      57.2                                                                                                        55.2                                                                                                            54.25
                                               0.75                                                   53.2                                                 0.75                                                   52.2                                                     0.75
                                                                                                                                                                                                                                                                                                                                  51.75

                                               1.00                                                   49.2                                                 1.00                                                   49.2                                                     1.00                                                   49.25
                                                      1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                    1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00
                                                            Anchor 0 speed X for <= t < 10 (dim 0)                                                                      Anchor 0 speed Y for <= t < 10 (dim 1)                                                                          Anchor 1 speed X for <= t < 10 (dim 3)


Figure B.6: Landscape (top) and gradient (bottom) plots for TripleMove environment with 90D parameters.
Left column – dimensions 0 and 1. Middle column – dimensions 1 and 2. Right column – dimensions 3 and 5.


Writer Below we show landscape and gradient plots of the Writer environment. We observe that
in this environment, the landscape is smoother than that of the previous environments, but there are
still a number of local minima at different areas of the landscape (see the left plot and the right plot).




                                               1.00                                                                                                        1.00                                                                                                            1.00                                                   7.44
                                                                                                      7.36                                                                                                        14.55
                                               0.75                                                                                                        0.75                                                                                                            0.75                                                   7.04
                                                                                                      6.96
                                                                                                                                                                                                                  13.20                                                                                                           6.64
                                               0.50                                                                                                        0.50                                                                                                            0.50
    Anchor speed X for 10 <= t < 20 (dim 3)




                                                                                                                                                                                                                                Anchor speed Z for 10 <= t < 20 (dim 5)
                                                                                                                Anchor speed Y for 10 <= t < 20 (dim 4)




                                                                                                      6.56
                                                                                                                                                                                                                  11.85                                                                                                           6.24
                                               0.25                                                   6.16                                                 0.25                                                                                                            0.25
                                                                                                                                                                                                                  10.50                                                                                                           5.84
                                               0.00                                                   5.76                                                 0.00                                                                                                            0.00
                                                                                                         Loss




                                                                                                                                                                                                                         Loss




                                                                                                                                                                                                                                                                                                                                      Loss




                                                                                                                                                                                                                  9.15                                                                                                            5.44
                                                                                                      5.36
                                               0.25                                                                                                        0.25                                                                                                            0.25
                                                                                                                                                                                                                  7.80                                                                                                            5.04
                                                                                                      4.96
                                               0.50                                                                                                        0.50                                                                                                            0.50
                                                                                                      4.56                                                                                                        6.45                                                                                                            4.64

                                               0.75                                                                                                        0.75                                                   5.10                                                     0.75                                                   4.24
                                                                                                      4.16

                                               1.00                                                   3.76                                                 1.00                                                   3.75                                                     1.00                                                   3.84
                                                      1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00                                                                    1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00
                                                             Anchor speed X for 0 <= t < 10 (dim 0)                                                                      Anchor speed Y for 0 <= t < 10 (dim 1)                                                                          Anchor speed Z for 0 <= t < 10 (dim 2)


Figure B.7: Landscape (top) and gradient (bottom) plots for Writer environment with 15D parameters. Left
column – dimensions 0 and 3. Middle column – dimensions 1 and 4. Right column – dimensions 2 and 5.


                                                                                                                                                                                       17
Flip In the paper, we showed that the Flip environment has rugged landscapes with suboptimal
gradient quality. Below we show additional landscape and gradient plots of the Flip environment to
confirm this. As seen in the plots, the landscape is very rugged, and gradients are pointing to rather
random directions.




                                     0.150                                                                                                                                     0.624                                                                                                       0.558
                                                                                    0.558
                                     0.125                                                                                       0.6                                           0.558                                        0.6                                                            0.498
                                                                                    0.498
                                     0.100                                                                                       0.4                                           0.492                                        0.4                                                            0.438
                                                                                    0.438
                                     0.075                                                                                                                                     0.426
    Initial speed Y of pan (dim 1)




                                                                                                                                                                                          Initial Tilt of the pan (dim 2)
                                                                                               Initial Tilt of the pan (dim 2)




                                                                                    0.378                                                                                                                                                                                                  0.378
                                                                                                                                 0.2                                                                                        0.2
                                     0.050                                          0.318                                                                                      0.360                                                                                                       0.318
                                                                                                                                 0.0                                                                                        0.0




                                                                                                                                                                                                                                                                                               Loss
                                                                                                                                                                                   Loss
                                                                                        Loss




                                     0.025                                          0.258                                                                                      0.294                                                                                                       0.258
                                                                                                                                 0.2                                                                                        0.2
                                     0.000                                          0.198                                                                                      0.228                                                                                                       0.198
                                                                                                                                 0.4                                                                                        0.4
                                     0.025                                          0.138                                                                                      0.162                                                                                                       0.138

                                     0.050                                          0.078                                        0.6                                           0.096                                        0.6                                                            0.078

                                     0.075                                          0.018                                                                                      0.030                                                                                                       0.018
                                             0.06 0.04 0.02 0.00 0.02 0.04 0.06                                                        0.06 0.04 0.02 0.00 0.02 0.04 0.06                                                     0.075 0.050 0.0250.000 0.025 0.050 0.075 0.100 0.125 0.150
                                                   Initial speed X of pan (dim 0)                                                             Initial speed X of pan (dim 0)                                                                 Initial speed Y of pan (dim 1)


Figure B.8: Landscape (top) and gradient (bottom) plots for Flip environment. Left column – dimensions 0 and
1. Middle column – dimensions 0 and 2. Right column – dimensions 1 and 2.



C                Details for Method Implementation and Compute Resources

For implementing CMA-ES, we used a fast and lightweight library provided by [37].
For implementing Bayesian optimization (BO), we used the BOTorch library [35], which supports
various versions of Gaussian processes (exact & approximate) and various BO acquisition func-
tions. For all experiments described in the main paper, we used the Lower Confidence Bound (LCB)
acquisition function, with default parameters (i.e. exploration coefficient α = 1.0). In our previous
experience, LCB had a similar performance as other commonly used functions (such as the Expected
Improvement acquisition function), and LCB has the advantage of being very easy to implement and
interpret. See Section IV in [32] for more information. BOTorch implements automatic hyperpa-
rameter optimization based on maximizing the marginal likelihood (see [32], Section V-A). We used
this for all our BO-based experiments.
We experimented with various versions of Gaussian process (GP) models, including exact GP
and sparse variational GP versions that are provided in BOTorch. BOTorch uses the lower-level
GPyTorch library [38] for GP implementations. We found that exact GPs performed best, and used
these for all BO experiments reported in the main paper. In future work, it would be interesting to
experiment with other GP implementations that could support posteriors with a much larger number
of points.
We used NVIDIA Tesla T4 GPUs and 32 cores of an Intel Xeon 2.3GHz CPU for our experiments.
The computational requirements of each simulation environment differ widely. For example, our
environments based on Warp, Nimble and mesh-based DiffTaichi were fastest, requiring only a few
minutes for 1,000 episodes (including gradient computations). Particle-based DiffTaichi environ-
ments (Fluid and the PlasticineLab environments) required significantly more time (e.g. Fluid took
≈ 2 hours for 1,000 episodes including gradient computations).


                                                                                                                                                         18
References
 [1] K. M. Jatavallabhula, M. Macklin, F. Golemo, V. Voleti, L. Petrini, M. Weiss, B. Considine,
     J. Parent-Levesque, K. Xie, K. Erleben, L. Paull, F. Shkurti, D. Nowrouzezahrail, and S. Fidler.
     gradsim: Differentiable simulation for system identification and visuomotor control. 2021.
 [2] Z. Huang, Y. Hu, T. Du, S. Zhou, H. Su, J. B. Tenenbaum, and C. Gan. PlasticineLab: A
     soft-body manipulation benchmark with differentiable physics. 2021.
 [3] X. Lin, Z. Huang, Y. Li, J. B. Tenenbaum, D. Held, and C. Gan. Diffskill: Skill abstraction
     from differentiable physics for deformable object manipulations with tools. arXiv preprint
     arXiv:2203.17275, 2022.
 [4] P. Sundaresan, R. Antonova, and J. Bohg. DiffCloud: Real-to-Sim from Point Clouds
     with Differentiable Simulation and Rendering of Deformable Objects. arXiv preprint
     arXiv:2204.03139, 2022.
 [5] P. Ma, T. Du, J. B. Tenenbaum, W. Matusik, and C. Gan. Risp: Rendering-invariant state
     predictor with differentiable simulation and rendering for cross-domain parameter estimation.
     arXiv preprint arXiv:2205.05678, 2022.
 [6] H. J. T. Suh, M. Simchowitz, K. Zhang, and R. Tedrake. Do differentiable simulators give
     better policy gradients? arXiv preprint arXiv:2202.00817, 2022.
 [7] J. Degrave, M. Hermans, J. Dambre, et al. A differentiable physics engine for deep learning in
     robotics. Frontiers in neurorobotics, page 6, 2019.
 [8] F. de Avila Belbute-Peres, K. Smith, K. Allen, J. Tenenbaum, and J. Z. Kolter. End-to-end dif-
     ferentiable physics for learning and control. In S. Bengio, H. Wallach, H. Larochelle, K. Grau-
     man, N. Cesa-Bianchi, and R. Garnett, editors, Advances in Neural Information Processing
     Systems (NeurIPS). Curran Associates, Inc., 2018.
 [9] C. Song and A. Boularias. Identifying mechanical models of unknown objects with differ-
     entiable physics simulations. In Proceedings of the 2nd Conference on Learning for Dynam-
     ics and Control, volume 120 of Proceedings of Machine Learning Research, pages 749–760.
     PMLR, 10–11 Jun 2020.
[10] C. Song and A. Boularias. Learning to slide unknown objects with differentiable physics
     simulations. arXiv preprint arXiv:2005.05456, 2020.
[11] Y.-L. Qiao, J. Liang, V. Koltun, and M. C. Lin. Efficient differentiable simulation of articulated
     bodies. In International Conference on Machine Learning, pages 8661–8671. PMLR, 2021.
[12] M. Lutter, J. Silberbauer, J. Watson, and J. Peters. Differentiable physics models for real-
     world offline model-based reinforcement learning. In 2021 IEEE International Conference on
     Robotics and Automation (ICRA), pages 4163–4170. IEEE, 2021.
[13] M. A. Z. Mora, M. P. Peychev, S. Ha, M. Vechev, and S. Coros. Pods: Policy optimization
     via differentiable simulation. In International Conference on Machine Learning, pages 7805–
     7817. PMLR, 2021.
[14] K. Werling, D. Omens, J. Lee, I. Exarchos, and C. K. Liu. Fast and feature-complete differen-
     tiable physics engine for articulated rigid bodies with contact constraints. In Robotics: Science
     and Systems, 2021.
[15] M. Geilinger, D. Hahn, J. Zehnder, M. Bächer, B. Thomaszewski, and S. Coros. Add: Analyt-
     ically differentiable dynamics for multi-body systems with frictional contact. ACM Transac-
     tions on Graphics (TOG), 39(6):1–15, 2020.
[16] A. H. Taylor, S. Le Cleac’h, Z. Kolter, M. Schwager, and Z. Manchester. Dojo: A differentiable
     simulator for robotics. arXiv preprint arXiv:2203.00806, 2022.


                                                  19
[17] Y.-L. Qiao, J. Liang, V. Koltun, and M. Lin. Scalable differentiable physics for learning and
     control. In International Conference on Machine Learning, pages 7847–7856. PMLR, 2020.
[18] C. D. Freeman, E. Frey, A. Raichuk, S. Girgin, I. Mordatch, and O. Bachem. Brax - a dif-
     ferentiable physics engine for large scale rigid body simulation. In Conference on Neural
     Information Processing Systems (NeurIPS) Datasets and Benchmarks Track, 2021.
[19] Y. Hu, L. Anderson, T.-M. Li, Q. Sun, N. Carr, J. Ragan-Kelley, and F. Durand. Difftaichi:
     Differentiable programming for physical simulation. 2020.
[20] Y. Hu, J. Liu, A. Spielberg, J. B. Tenenbaum, W. T. Freeman, J. Wu, D. Rus, and W. Ma-
     tusik. Chainqueen: A real-time differentiable physical simulator for soft robotics. In 2019
     International conference on robotics and automation (ICRA), pages 6265–6271. IEEE, 2019.
[21] J. Liang, M. Lin, and V. Koltun. Differentiable cloth simulation for inverse problems. Advances
     in Neural Information Processing Systems, 32, 2019.
[22] N. Thuerey. Differentiable fluid simulations for deep learning. In APS Division of Fluid
     Dynamics Meeting Abstracts, pages H17–006, 2019.
[23] E. Heiden, M. Macklin, Y. S. Narang, D. Fox, A. Garg, and F. Ramos. DiSECt: A Differ-
     entiable Simulation Engine for Autonomous Robotic Cutting. In Proceedings of Robotics:
     Science and Systems, Virtual, July 2021. doi:10.15607/RSS.2021.XVII.067.
[24] W. Wang, S. Axelrod, and R. Gómez-Bombarelli. Differentiable molecular simulations for
     control and learning. 2020.
[25] P. Ma, T. Du, J. Z. Zhang, K. Wu, A. Spielberg, R. K. Katzschmann, and W. Matusik. Diffaqua:
     A differentiable computational design pipeline for soft underwater swimmers with shape inter-
     polation. ACM Transactions on Graphics (TOG), 40(4):132, 2021.
[26] S. S. Schoenholz and E. D. Cubuk. Jax m.d. a framework for differentiable physics. In Ad-
     vances in Neural Information Processing Systems, volume 33. Curran Associates, Inc., 2020.
[27] M. Macklin. Warp: A high-performance python framework for gpu simulation and graphics.
     https://github.com/nvidia/warp, March 2022. NVIDIA GPU Technology Conference
     (GTC).
[28] M. Locatelli and F. Schoen. (global) optimization: Historical notes and recent developments.
     EURO Journal on Computational Optimization, 9:100012, 2021.
[29] N. Hansen and A. Ostermeier. Completely derandomized self-adaptation in evolution strate-
     gies. Evolutionary computation, 9(2):159–195, 2001.
[30] N. Hansen. The cma evolution strategy: a comparing review. Towards a new evolutionary
     computation, pages 75–102, 2006.
[31] N. Hansen, A. Auger, R. Ros, S. Finck, and P. Pošı́k. Comparing results of 31 algorithms
     from the black-box optimization benchmarking bbob-2009. In Proceedings of the 12th annual
     conference companion on Genetic and evolutionary computation, pages 1689–1696, 2010.
[32] B. Shahriari, K. Swersky, Z. Wang, R. P. Adams, and N. de Freitas. Taking the Human Out
     of the Loop: A Review of Bayesian Optimization. Proceedings of the IEEE, 104(1):148–175,
     2016.
[33] X. Chen, X. Liu, and Y. Jia. Combining evolution strategy and gradient descent method for
     discriminative learning of bayesian classifiers. In Proceedings of the 11th Annual conference
     on Genetic and evolutionary computation, pages 507–514, 2009.
[34] C. K. Williams and C. E. Rasmussen. Gaussian processes for machine learning, volume 2.
     MIT press Cambridge, MA, 2006.


                                                20
[35] M. Balandat, B. Karrer, D. R. Jiang, S. Daulton, B. Letham, A. G. Wilson, and E. Bakshy.
     BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization. In Advances in
     Neural Information Processing Systems 33, 2020.
[36] Y. Hu, Y. Fang, Z. Ge, Z. Qu, Y. Zhu, A. Pradhana, and C. Jiang. A moving least squares
     material point method with displacement discontinuity and two-way rigid body coupling. ACM
     Transactions on Graphics, 37(4):150, 2018.
[37] M. N. Masashi Shibata, Hideaki Imamura.                     A Lightweight      Covariance
     Matrix Adaptation Evolution Strategy (CMA-ES)               Implementation.         URL
     https://github.com/CyberAgentAILab/cmaes.
[38] J. Gardner, G. Pleiss, K. Q. Weinberger, D. Bindel, and A. G. Wilson. GPyTorch: Black-
     box Matrix-matrix Gaussian Process Inference with GPU Acceleration. Advances in neural
     information processing systems, 31, 2018.




                                              21
