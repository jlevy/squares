                                                   DiffXPBD : Differentiable Position-Based Simulation of
                                                              Compliant Constraint Dynamics
                                                                     Tuur Stuyck                                                     Hsiao-yu Chen
                                                             Meta Reality Labs Research                                         Meta Reality Labs Research
                                                                        USA                                                                USA
arXiv:2301.01396v3 [cs.GR] 28 Jun 2023




                                         Figure 1: We present a fully analytically differentiable solver that allows to obtain gradients with respect to a desired parameter
                                         in order to minimize a goal function. In this example, we show how coefficients for the shape of a statistical body model can
                                         efficiently be computed in order to minimize the distance of the draped clothing to an observed reference. Our differentiable
                                         solver can differentiate through collisions of the cloth with the underlying body shape which allows the gradient information
                                         to propagate. Left shows the target drape. Next, we show the original body shape with the draped cloth. The middle figure
                                         shows the final optimized body shape that produces a drape close to the goal shape. The goal drape and ground truth body
                                         shape are shown second to the right. The rightmost figure visualizes the distance of the estimated garment drape to the ground
                                         truth drape. Note how they closely coincide where the garment touches the body, indicating a successful optimization result.
                                         ABSTRACT                                                               CCS CONCEPTS
                                         We present DiffXPBD, a novel and efficient analytical formulation      • Computing methodologies → Physical simulation.
                                         for the differentiable position-based simulation of compliant con-
                                         strained dynamics (XPBD). Our proposed method allows compu-            KEYWORDS
                                         tation of gradients of numerous parameters with respect to a goal
                                                                                                                differentiable simulation, parameter estimation
                                         function simultaneously leveraging a performant simulation model.
                                         The method is efficient, thus enabling differentiable simulations of
                                         high resolution geometries and degrees of freedom (DoFs). Colli-
                                         sions are naturally included in the framework. Our differentiable      1   INTRODUCTION
                                         model allows a user to easily add additional optimization variables.   Differentiable simulation enables integration of physics-based mod-
                                         Every control variable gradient requires the computation of only a     els with data-driven methods in a seamless and efficient way. By
                                         few partial derivatives which can be computed using automatic dif-     making the simulation model differentiable, we can compute gradi-
                                         ferentiation code. We demonstrate the efficacy of the method with      ents of the output variables with respect to the model parameters,
                                         examples such as elastic cloth and volumetric material parameter       which can be optimized through gradient-based methods. This
                                         estimation, initial value optimization, optimizing for underlying      opens up a range of possibilities for tasks such as model identifi-
                                         body shape and pose by only observing the clothing, and optimizing     cation, material estimation, inverse design, where we want to fit
                                         a time-varying external force sequence to match sparse keyframe        the simulation model to data or optimize certain parameters to
                                         shapes at specific times. Our approach demonstrates excellent ef-      achieve specific goals. Differentiable simulation can also enable us
                                         ficiency and we demonstrate this on high resolution meshes with        to create more realistic and accurate simulations by incorporating
                                         optimizations involving over 26 million degrees of freedom. Making     real-world data into the simulation process. Recent advances in cap-
                                         an existing solver differentiable requires only a few modifications    ture systems [Chen et al. 2021; Halimi et al. 2022; Wang et al. 2023,
                                         and the model is compatible with both modern CPU and GPU               2022; White et al. 2007] provide high quality data that can be used
                                         multi-core hardware.                                                   to learn the simulation parameters and fine-tune the simulation
                                                                                                                                     Stuyck and Chen


model to better match real-world behavior. Physics-based simula-            in contact heavy scenarios [Zhong et al. 2022]. Liang et al. [2019]
tion methods have shown widespread success and many different               introduced a differentiable approach for handling cloth collisions
techniques have been proposed. The seminal work of Baraff and               using a linear complementary problem. Du et al. [2021] introduced
Witkin [1998] introduced an implicit integration scheme enabling            a differentiable approach to Projective Dynamics using the adjoint
simulations which remain stable for large time steps, resulting in          method, enabling fast differentiable simulations. Follow up work
efficient simulations. This method is still commonly used in top-           extends this research to enable cloth simulations with dry frictional
tier animation studios [Kim and Eberle 2022]. Since then, many              contact [Li et al. 2022]. Others focus on the optimization of static
novel approaches have been proposed to tackle different shortcom-           cloth simulations [Bartle et al. 2016; Umetani et al. 2011]. Coros et al.
ings. The introduction of Position-Based Dynamics (PBD) [Müller             [2021] provide an overview of differentiable simulation methods.
et al. 2007] enabled a unified high performance solver that maps               Differentiable soft body simulation models [Geilinger et al. 2020;
efficiently to modern parallel hardware such as multi-core CPUs             Hahn et al. 2019] and estimating material properties from scanned
and GPUs. Follow up work introduced eXtended Position-Based                 volumetric objects using differentiable simulation as an inverse de-
Dynamics (XPBD) [Macklin et al. 2016] which resolves the iter-              sign problem has been active domain of research [Weiss et al. 2020].
ation and time step dependent stiffness issue of PBD. Projective            Chen et al. [2022] introduced differentiable point-based simulation
Dynamics (PD) [Bouaziz et al. 2014] introduced a fast local-global          for material estimation of soft deformable bodies coupled with neu-
solver for implicit time integration of FEM simulations with elastic        ral radiance field representations [Mildenhall et al. 2021]. Similarly,
energies in a quadratic form. Stuyck [2018] provides an overview            parameter estimation for cloth simulations has been a focus of at-
of several simulation techniques.                                           tention [Larionov et al. 2022; Miguel et al. 2012; Wang et al. 2011].
   Several of these methods have been extended to be differentiable         Guo et al. [2021] showed that is possible to estimate body shape and
for dynamic simulations and we are the first to present an analytical       pose given a point cloud by differentiating through clothing simula-
differentiable formulation for the XPBD simulation framework. The           tions. A full end-to-end system is presented by Jatavallabhula et al.
differentiable solver can easily be extended to novel constraints by        [2021] where they propose a system identification technique by
adding a few partial derivatives per constraint. We empirically show        combining differentiable simulation with differentiable rendering
that our method scales to high simulation resolutions and DoFs              which allows them to backpropagate gradient information from pix-
with respect to prior work. Our contributions are the following :           els in a video sequence. This pipeline enables them to optimize for
     • We present a differentiable formulation for position-based           control variables to reproduce image observations directly. Other
       simulation of compliant constraint dynamics. The method              simulation models like the Material Point Method have successfully
       is efficient, scales to large number of DoFs, and maintains          been made differentiable [Hu et al. 2019] and have been used for a
       all advantages of the forward simulation model enabling              variety of control tasks [Hu et al. 2020].
       parallel cpu and gpu implementations.                                   In addition to analytical formulations of these differentiable sim-
     • Our method naturally differentiates through the constraints          ulation models, specialized differentiable programming frameworks
       formulation which seamlessly enables differentiable simula-          focusing on physics-based simulation applications are becoming
       tion of different potentially coupled phenomena, including           more commonplace [Hu 2022; Macklin 2022]. The research field has
       self-collisions and collisions with the environment.                 made great progress enabling dynamic differentiable simulation
     • The approach requires only a small addition to the forward           for numerous applications. However, several issues still remain.
       simulation model and as such, it can be easily added to ex-          Performance and memory usage is a primary concern for any dif-
       isting solvers. The backward solve involves sparse matrices          ferentiable method. With our efficient and highly parallelizable
       and can be implemented using off-the-shelf libraries.                formulation, we demonstrate optimizations involving high resolu-
                                                                            tion geometries and DoFs.
We show efficient computation of derivatives of high DoFs and high
geometric resolutions for a variety of tasks.
                                                                            3 BACKGROUND
2    RELATED WORK                                                           3.1 XPBD: Position-Based Simulation of
Differentiable simulation has been applied in recent research [Liang            Compliant Constrained Dynamics
et al. 2019; Qiao et al. 2020] to system identification and for inferring   XPBD is an efficient unified simulation model, capable of produc-
material parameters from observations [Hu et al. 2019; Strecke and          ing real-time simulations. The constraint-based formulation can be
Stückler 2021]. It has applications in computer graphics, vision,           parallelized [Fratarcangeli et al. 2016] and implemented on modern
robotics and many others. Several of these techniques rely on the           GPU and multi-core CPU hardware. As a result, the model show-
adjoint method for gradient computation. Over the last decades,             cases much better performance compared to expensive non-linear
the adjoint method has been successfully applied to differentiate           solvers. The method solves Newton’s equations of motion given
various dynamic simulation models. This includes fluid simulation           by M¥x = −∇𝑈 ⊤ (x), where x are the 𝑉 vertex positions and M is
[McNamara et al. 2004] and implicit simulation of cloth dynamics            the mass matrix. The energy potential 𝑈 (x) is formulated in terms
[Wojtan et al. 2006]. The adjoint method continues to be successfully       of a vector of constraint functions C = [𝐶 1 (x), · · ·, 𝐶𝑚 (x)] ⊤ and
applied with a focus on time-dependent deformation problems                 inverse compliance matrix 𝜶 −1 as
with contact [Gjoka et al. 2022]. Notoriously, cloth simulations
frequently undergo numerous contacts. Because of this, work has                                             1
focused specifically on the handling of differentiable simulation                                 𝑈 (x) =     C(x) ⊤ 𝜶 −1 C(x)                   (1)
                                                                                                            2
DiffXPBD : Differentiable Position-Based Simulation of Compliant Constraint Dynamics


Implicit Euler time integration results in the constraint multiplier                                                Forward                              Goal
                                                                                                                                                        Function
updates Δ𝝀 at iteration 𝑖 being computed as                                                                       Differentiable
                                                                                                                   Simulation
           (∇C(x𝑖 ) ⊤ M −1 ∇C(x𝑖 ) + 𝜶˜ )Δ𝝀 = −C(xi ) − 𝜶˜ 𝝀𝑖               (2)
                                                                                                                     Storage
where 𝜶˜ = 𝜶 /Δ𝑡 2 . Given Δ𝝀, the position update is computed as
                           Δx = M −1 ∇C(x𝑖 )Δ𝝀                              (3)
                                                                                                                                    Backward
With external forces fext acting on the system. The state q𝑛 =                                                                     Adjoint State
                                                                                                     Gradient
(x𝑛 , v𝑛 ) at time step 𝑛 consisting of positions x ∈ R3𝑉 and velocities                            Computation                    Computation
v ∈ R3𝑉 is updated as
                                                           
             x𝑛+1 = x𝑛 + Δx (x𝑛+1 ) + Δ𝑡 v𝑛 + Δ𝑡M −1 fext
                                                                                       Figure 2: Overview of the different components of the gradient
                      1                                              (4)
                                                                                       computation process. The forward simulation computes and
             v𝑛+1 =      (x𝑛+1 − x𝑛 )
                      Δ𝑡                                                               stores the quantities required in the backward pass. After
                                                                                       which, the goal function gets evaluated which in turn starts
3.2     The Adjoint Method                                                             the backward adjoint state computation pass. The total gra-
The gradients 𝑑𝜙/𝑑u required to minimize a goal function 𝜙 with                        dient 𝑑𝜙/𝑑u is obtained using Eq. 7.
respect to control variables u are typically intractable to compute
directly for dynamic simulations. The adjoint method provides
an efficient solution to compute these derivatives in a single pass                    defined over all steps 𝑁 or a subset thereof. Any goal function or
through the computation graph, regardless of the number of param-                      combination of goal functions can be used as long as the required
eters. The gradients of the control variables with respect to some                     derivatives 𝜕𝜙/𝜕q and 𝜕𝜙/𝜕u can be computed. Section 6.3 shows
goal function can be computed as                                                       the use of a point-cloud-based goal function.
                        𝑑𝜙    𝜕𝜙 𝑑Q 𝜕𝜙
                           =          +                        (5)                     4.2     Adjoint State Computation
                        𝑑u 𝜕Q 𝑑u 𝜕u
                                                                                       The adjoint evolution for the XPBD integration scheme is found by
where Q represents the full set of states q𝑛 across all times 𝑁 .                      combining Eq. 4 and Eq. 6, see the supplemental material for the
The adjoint method turns this intractable computation into a more                      full derivation. We find
efficient formulation by replacing the vector-matrix product con-
                                                                                                                         𝜕fext ⊤         v̂𝑛 v̂𝑛+1 𝜕𝜙 ⊤
                                                                                                                              
                                                                                                        𝜕Δx
taining 𝑑Q/𝑑u with an equivalent computation involving the ad-                          x̂𝑛 = x̂𝑛+1 +        + Δ𝑡 2 M −1          x̂𝑛 +      −      +
joint  of Q, denoted by                                                                                  𝜕x               𝜕x             Δ𝑡      Δ𝑡   𝜕x
                     Q̂ which contains all adjoint states q̂𝑛 =                                                     ⊤                      ⊤
                                                                                                                                                         (9)
 x̂𝑛 ∈ R3𝑉 , v̂𝑛 ∈ R3𝑉 over all times 𝑁 . We refer to the supple-                       v̂𝑛 =
                                                                                                 𝜕Δx
                                                                                                     + Δ𝑡 2 M −1
                                                                                                                 𝜕fext
                                                                                                                          x̂𝑛 + Δ𝑡 x̂𝑛+1 +
                                                                                                                                            𝜕𝜙
mental material and Wojtan et al. [2006] for an in-depth overview.                                𝜕v              𝜕v                        𝜕v
The simulation moves the states forward in time using q𝑛+1 =                             After re-arranging and by substituting v̂𝑛 we find
F𝑛 (q𝑛+1, q𝑛 , u), see Eq. 4. The adjoint states Q̂ are computed in a
                                                                                                                                          𝜕fext ⊤
                                                                                                                                              
backward pass using                                                                                𝜕Δx             𝜕fext   1 𝜕Δx
                                                                                              𝐼−       − Δ𝑡 2 M −1       −       − Δ𝑡M −1         x̂𝑛
                   
                     𝜕F𝑛−1 ⊤
                                      
                                         𝜕F𝑛 ⊤
                                                    
                                                       𝜕𝜙 ⊤
                                                                                                   𝜕x              𝜕x     Δ𝑡 𝜕v           𝜕v
         q̂𝑛−1 =               q̂𝑛−1 +         q̂𝑛 +              (6)                                                                                (10)
                      𝜕q𝑛                𝜕q𝑛           𝜕q𝑛                                            v̂𝑛+1 𝜕𝜙 ⊤ 1 𝜕𝜙 ⊤
                                                                                          = 2x̂𝑛+1 −       +       +
                                     𝑑𝜙                                                                 Δ𝑡    𝜕x     Δ𝑡 𝜕v
after which the full derivative 𝑑u is obtained using                                   Assuming that the external forces are generally independent of the
                            𝑑𝜙       𝜕F 𝜕𝜙                                             positions and velocities, and since 𝜕Δx/𝜕v evaluates to 0, we left
                               = Q̂⊤   +                                    (7)        multiply with the mass matrix M. We solve this sparse symmetric
                            𝑑u       𝜕u 𝜕u
                                                                                       linear system using Conjugate Gradients (CG) to obtain x̂𝑛 . We
4 METHOD                                                                               then find v̂𝑛 using Eq. 28.
4.1 Goal Function                                                                      4.2.1 Linear System Filtering. Vertices can be fully constrained in
An overview of the method is illustrated in Figure 2. We minimize a                    the simulation due to Dirichlet boundary conditions. These pinned
goal function 𝜙 by modifying the control variables u. This function                    vertices are modeled using an infinite mass. To handle this robustly,
can be easily provided by the user and adapted based on the problem                    we rely on modified Conjugate Gradient with pre-filtering [Baraff
at hand. The most straight-forward metric is to compare simulation                     and Witkin 1998] as presented by Tamstorf et al. [2015].
state Q directly with a given reference Q∗ using
                            𝑁                                                          4.3     Position Update Derivative Computation
                        1 ∑︁                                     
           𝜙 (u, Q) =          ||W𝑛 (q𝑛 − q𝑛∗ )|| 2 + 𝛽 ||u𝑛 || 2           (8)        For every constraint in the system, Eq. 10 requires us to differenti-
                        2 𝑛=0
                                                                                       ate through the position update in order to obtain 𝜕Δx/𝜕x. These
where an optional regularization term with weight 𝛽 based on the                       derivatives can be computed analytically or using automatic or
control variable u has been added. The weight matrix W𝑛 can be                         symbolic differentiation techniques. The derivatives can be accu-
used to introduce relative importance. The goal function can be                        mulated in parallel in the same iterative fashion as the position
                                                                                                                                              Stuyck and Chen


updates, which allows the method to remain highly parallelizable.            5     EXAMPLE APPLICATIONS
Analytically, these derivatives are computed as                              Our method provides a way to efficiently compute gradients ana-
                𝜕Δx
                                                                           lytically with respect to any control variable. To illustrate this, we
                         −1 𝜕∇C            𝜕Δ𝝀
                     =M            Δ𝝀 + ∇C                   (11)            present several example applications leveraging our optimization
                 𝜕x            𝜕x           𝜕x
                                                                             pipeline. Our method is not limited to these specific examples.
Where we can omit the M −1 term since this vanishes when multi-
plied by the mass matrix in Eq. 10. To keep the notation compact,            5.1    Cloth Material Parameter Estimation
we define ∇C(x𝑖 ) ⊤ M −1 ∇C(x𝑖 ) + 𝜶˜ = J, and we group the terms in         We use an orthotropic Saint Venant-Kirchhoff membrane energy
Eq. 2 as JΔ𝝀 = b. We can then compute the required quantities as             model combined with a discrete bending [Bender et al. 2017] term
    𝜕Δ𝝀            𝜕J             𝜕b
                                               
                                                 𝜕J      𝜕b
                                                                            to model the fabric properties. Different material models are equally
           = −J −1 J −1 b + J −1       = −J −1      Δ𝝀 −        (12)         applicable and our proposed differentiation method is not limited to
     𝜕x            𝜕x             𝜕x             𝜕x      𝜕x
                                                                             these. Per triangle with area 𝐴, the membrane model has an inverse
      𝜕b and 𝜕J Δ𝝀 are computed as
where 𝜕x                                                                     compliance matrix of the form
             𝜕x
        𝜕b         𝜕C 𝜕 𝜶˜        𝜕𝝀                   ∑︁ 𝜕Δ𝝀                                              𝐶 00           𝐶 01         
              =−      −    𝝀 − 𝜶˜         = −∇C − 𝜶˜                 (13)                           −1
                                                                                                                                       
        𝜕x         𝜕x   𝜕x        𝜕x                         𝜕x                                   𝜶 △ = 𝐴 𝐶 01           𝐶 11         ,
                                                                                                                                        
                                                                                                                 
                                                                                                                                 𝐶 22 
           𝜕J      𝜕∇C𝑇 −1                   𝜕∇C
              Δ𝝀 =      M ∇CΔ𝝀 + ∇C𝑇 M −1        Δ𝝀
           𝜕x       𝜕x                        𝜕x                             where 𝐶𝑖 𝑗 are the compliance coefficients. The constraint func-
                                                                     (14)
                   𝜕∇C𝑇               𝜕∇C                                    tion for each triangle is then defined to be the Green strain 𝜖 in
                 =      Δx + ∇C𝑇 M −1     Δ𝝀                                 Voigt notation C △ (x) = (𝜖𝑢𝑢 , 𝜖 𝑣𝑣 , 2𝜖𝑢𝑣 ) ⊤, where subscripts 𝑢 and 𝑣
                    𝜕x                 𝜕x
                                                                             indicate warp and weft directions, respectively. For bending, the
4.3.1 Derivative Verification. According to the XPBD formulation,            inverse compliance matrix is given by the scalar bending stiffness:
we have the relation M 𝜕Δx         𝜕f                      ⊤
                            𝜕x = 𝜕x , where f = −∇𝑥 𝑈 (x𝑛+1 ), and             −1 = 𝑏. We optimize directly over the compliance coefficients
                                                                             𝜶 bend
 𝜕f is the Hessian of an elastic potential 𝑈 . To validate the derivative,
𝜕x                                                                           and bending parameter by choosing the parameter set to be
one can rely on the symmetry property of the Hessian and verify
the symmetry of M 𝜕Δx 𝜕x . In addition, the internal forces inside each
                                                                                               𝜸 := (𝐶 00, 𝐶 11, 𝐶 01, 𝐶 11, 𝑏), 𝜸 ∈ 𝚪                   (15)
element should sum to zero, which implies that 𝑖 𝜕f
                                                       Í i
                                                           𝜕x = 0, for all   where the parameters are constrained to be in the feasible set 𝚪.
vertices 𝑖 inside the element. This suggests that the rows of M 𝜕Δx   𝜕x     In order to optimize for these parameters, we compute and store
sum to zero, and by symmetry the column should sum to zero as
                                                                             𝜕Δx/𝜕𝜸 during the constraint solve at every step.
well. A more detailed discussion can be found in the documents
by Kim and Eberle [2022].
                                                                             5.2    Volumetric Material Parameter Estimation
4.3.2 Positive Definite Projection. Although a direct solver can be          To model inhomogeneous elastic objects, we utilize the stable Neo-
used to solve Eq. 10, iterative solvers like Preconditioned Conjugate        Hookean energy [Smith et al. 2018], following the XPBD formula-
Gradients (PCG) are preferred due to its efficiency. PCG requires            tion by Macklin and Müller [2021], with the hydrostatic constraint
the matrix to be semi-positive-definite. Therefore, we project all                 det(F) − 1 to preserve volume, and the deviatoric constraint
                                                                             C𝐻 = √︁
derivative blocks to positive definiteness [Nocedal and Wright 2006].        C𝐷 = tr(F𝑇 F) to penalize stretching, where F is the deformation
The projection can be computed in parallel over all derivatives and          gradient. We assume that the object can be composed of different
happens only once at the end of every step.                                  materials, characterized by sets of first and second Lamé parameters,
                                                                             denoted as (𝝁, 𝝀). Our optimization process aims to identify the set
4.4    Control Variable Derivative Computation                               of parameters (a, b) such that a2 = 𝝁 and b2 = 𝝀. By optimizing
For every control variable u we wish to obtain a gradient for, we            over a and b, we ensure that the optimized values are within the
need to evaluate Eq. 7 which requires 𝜕F/𝜕u. For control variables           physical range, as the Lamé parameters are strictly positive.
influencing the position updates, we need to compute and store
𝜕Δx/𝜕u. These derivatives can be computed using a similar deriva-            5.3    Body Shape Optimization
tion as explained in Section 4.3. For those influencing the external
                                                                             Given a statistical body model such as SMPL [Loper et al. 2015] but
forces, additional 𝜕fext /𝜕u terms are needed.
                                                                             not limited to this specific model, we can estimate the PCA shape
                                                                             coefficients 𝜶 that would minimize a given goal function defined
4.5    Collision Handling                                                    on the simulated cloth mesh. The connection between the cloth
In order to include collision handling in our differentiable frame-          and the body is established through the collisions and gradients
work, we model collisions as stiff springs using compliant con-              can flow through freely. We accumulate gradients with respect to
straints to maintain a closest separation distance of at least a user-       the coefficients using the chain rule
set thickness between the garment layers as well as the body surface.
The approach is compatible with any collision detection strategy                   𝜕Δxcloth-body collision           𝜕Δxcloth-body collision 𝜕xbody
                                                                                                             =                                           (16)
such as continuous time collision detection.                                                𝜕𝜶                              𝜕xbody           𝜕𝜶
DiffXPBD : Differentiable Position-Based Simulation of Compliant Constraint Dynamics


5.4     Skeleton Pose Optimization
Similarly as for the body shape optimization, by applying the chain
rule and differentiating through the linear blend skinning directly,
we obtain the gradient with respect to the skeleton joint angles 𝜏
using
      𝜕Δxcloth-body collision       𝜕Δxcloth-body collision 𝜕xbody
                                =                                          (17)
                 𝜕𝝉                        𝜕xbody              𝜕𝝉

5.5     Initial Value Optimization
Following Eq. 7, the gradient with respect to the initial position and
velocities can be directly obtained from the adjoint states without
the need for computing additional control variable derivatives of
the position updates.                                                                                (a) Initial                      (b) Optimized


5.6     Keyframe Simulation                                                            Figure 3: Bend Stiffness Optimization. Material parameter
The method can also be used for motion in-betweening or stitching                      estimation is effective even when the clothing is interacting
distinct simulations together. Provided with a few keyframes, the                      with an underlying body. The optimized fabric coincides
method can automatically optimize for an external time-varying                         closely with the target shape shown in the blue wireframe.
force sequence that pushes the clothing through the keyframes
at the desired times. We optimize directly for all external forces
per particle per step resulting in a high dimensional optimization
problem. The external force gradients can be directly obtained from
the adjoint velocities as they do not influence the position updates                   6.3    Body Shape Optimization
directly.                                                                              We show optimization of the coefficients of a statistical body model
                                                                                       so that a draped garment matches a given cloth observation as
6     RESULTS                                                                          closely as possible. This is demonstrated in Figure 1. We optimize
We demonstrate the efficacy of our method with respect to sev-                         for all 2781 body PCA coefficients simultaneously. Fig. 6 shows body
eral applications. All differentiable simulations are dynamic and                      shape optimization using a scan of a real person captured wearing
accompanying videos can be found in the supplemental material.                         a t-shirt. Since the scan has a different topology than the simulated
The resolutions of the simulated objects are reported in Table 1. All                  garment, we use a goal function based on the closest distance of the
optimizations are minimized using gradient descent with fixed step                     simulated vertices to the scan where closest points computations are
size.                                                                                  recomputed every iteration and the t-shirt geometry is segmented
                                                                                       out of the scan. The segmented t-shirt scan contains 144,556 vertices
6.1     Cloth Material Parameter Estimation                                            and 288,034 faces and the optimized body shape contains 7,324
Our method is capable of optimizing the material parameter while                       vertices and 14,644 faces.
the clothing is draped on a body for which the collisions are taken
into account. We demonstrate before and after estimation of the                        6.4    Skeleton Pose Optimization
bending stiffness for a dress draped on a static body in Fig. 3 where
                                                                                       We can optimize for the skeleton pose that through a linear blend
the keyframe is shown in blue. Similarly, we estimate in-plane elas-
                                                                                       skinning operation defines the body surface positions. We show
tic material properties. Figure 4 demonstrates the optimization of
                                                                                       that we can optimize this pose to produce a draped garment that
the Young’s moduli in both warp and weft direction such that a tar-
                                                                                       matches the reference closely. Different iteration results of this
get shape gets matched at a specific frame in a dynamic simulation.
                                                                                       experiment are shown in Fig. 8.
In this example, all triangles in the swatch share the same material.

                                                                                       6.5    Initial Value Optimization
6.2     Volumetric Material Parameter Estimation                                       We demonstrate optimizing over initial condition parameters. We
We demonstrate estimation of the material parameters of an inho-                       intend to find the initial velocity per vertex so that at the end
mogeneous volumetric elastic object. The target object is composed                     of the simulation, the clothing is at a specified position and pose
of two materials with different stiffnesses, and we create a target                    provided by the keyframe. Fig. 9 visualizes different iteration results.
shape by fixing one end and allowing the rest to deform under                          In the first iteration, the shirt simply falls down due to gravity. In
gravity. We try to match this boundary shape by optimizing for 100                     the following iterations, the model iteratively updates the initial
materials randomly distributed over all tetrahedrons, resulting in                     velocity prediction such that the shirt coincide closely with the
200 DoFs. Fig. 5 demonstrates the effectiveness of our method in                       goal shape at the requested frame. This example highlights the
finding a set of material parameters that generates similar behavior                   scalability of our method by easily estimating all 197,904 velocity
to the target, even when the initial guess is vastly different.                        values directly.
                                                                                                                                   Stuyck and Chen




Figure 4: Young’s Moduli Optimization. We show different iterations of a cloth swatch draping under gravity with its corners
pinned. The simulated cloth is textured and the goal shape is shown in blue. We optimize for the elastic material properties such
that the simulated cloth reaches the desired pose at the requested frame. Initially, the material is too stiff and sags insufficiently
under gravity to reach the target state. The optimization converges quickly to a looser material that matches the target at the
specified frame.




Figure 5: Volumetric Material Optimization. Our method es-
timates the material of an inhomogenous elastic body (red)
to fit a target (blue), starting from an initial guess (left) to an
optimized result (right).




                                                                       Figure 7: External Force Sequence Optimization. We find
                                                                       the time-varying force sequence that pushes the garment
                                                                       through the keyframes (green). Over 21 million DoFs are
                                                                       being optimized for.

                                                                                   Simulation    Differentiable Simulation       Resolution
                                                                                                         Matrix
                                                                                    Forward     Forward Assembly   CG Solve   Vertices   Elements

                                                                        Shirt        0.145       2.459    0.490      2.046    65,968     131,421
                                                                        T-Shirt      0.079       0.496    0.087      0.476    14,639      29,032
                                                                        Dress        0.056       0.354    0.064      0.282    10,422      20,685
                                                                        Pants        0.053       0.192    0.050      0.254     8002       16,170
Figure 6: Body Shape Optimization From Scan. We show suc-               Swatch       0.005       0.011    0.003      0.005      441         800
cessful body shape optimization given a high resolution scan.           Dino         0.039       2.425    0.006      0.007     1365        4802
                                                                       Table 1: Timings in seconds. Normal and differentiable sim-
                                                                       ulation timings per step are. Timings are computed as the
6.6    Keyframe Simulation                                             average per step. Mesh resolutions used in the examples are
Given a few sparse keyframes of the cloth geometry, we want to         shown on the right.
optimize the time-varying sequence of forces so that the cloth ge-
ometry passes through the provided keyframes at the desired time.
We initialize the sequence with forces equal to zero. Initially, the
garment falls down under gravity but then converges to a solution      6.7        Performance
where the garment flows through the desired keyframes at the re-       The algorithm is implemented in C++ on CPU and we report the
quested time, see Fig. 7. This example highlights the capability of    timings in Table 1. All experiments are run using an AMD Ryzen
our method to optimize for high number of DoFs in an efficient and     Threadripper PRO 3975WX 32-Cores using 20 constraint iterations
scalable way. We optimize for 900 simulation steps which results       with a time step of 0.0016 ms. The timings reported include collision
in 21,605,400 control variables being optimized for simultaneously.    detection and resolving, the constraint solve, and the computation
To the best of our knowledge, this far exceeds prior work.             the derivative terms, including definiteness fix. We also report the
DiffXPBD : Differentiable Position-Based Simulation of Compliant Constraint Dynamics




Figure 8: Skeleton Pose Optimization. We show how the skeleton pose can be recovered simply by looking at the drape of the
garment. From left to right, we visualize different optimization iterations and the target drape is shown on the far right. We
optimize over the 3 rotational DoFs of all 114 joints simultaneously.




Figure 9: Initial condition optimization. We show optimization of the initial velocity per vertex in order to reach a specific pose
and location at a specified frame. The pink shirt indicates the starting position and the green is the goal position. Different
iterations are visualized. The inset images provide an non-occluded view of the final optimized shape per iteration. Our method
effortlessly handles the high DoFs of 197,904 velocity values.


timing of the non-differentiable version of the solver. Although                       7   DISCUSSION, LIMITATIONS, AND FUTURE
enabling differentiability adds some expected overhead, the method                         WORK
remains performant. The backward pass consists of matrix assembly
                                                                                       We present an efficient extension to the position-based simula-
from the individual derivative blocks and the linear system solve
                                                                                       tion model of compliant constraint dynamics to obtain gradients
using Conjugate Gradients.
                                                                                       with respect to any parameter through a dynamic simulation. We
                                                                                       illustrate the effectiveness of the method with several example
                                                                                       applications and show that our method is capable of efficiently
6.8     Comparisons To Related Work                                                    computing gradients for high resolutions and high DoFs. A limita-
                                                                                       tion of the adjoint method is the need to store intermediate particle
Guo et al. [2021] demonstrates body pose and shape optimization                        states and gradients at every time step. The resulting memory usage
from cloth scans. They assume that variations in the time-varying                      scales linearly with the length of the simulation. In practice, this
body states only affect the current state of the cloth geometry.                       limitation is manageable as our approach allows us to store data
This simplification is justified since this would require propagating                  for individual steps and retrieve them when needed. Since our con-
gradients across the entire simulation resulting in intractable com-                   tribution does not modify the properties of the forward simulation
putations. Wojtan et al. [2006] presented a differentiable implicit                    algorithm, we inherit the same performance advantages but also
simulator for resolutions up to 2500 vertices. Liang et al. [2019]                     the limitations such as slow convergence for very stiff constraints.
demonstrate differentiable cloth simulation on geometries with up                      As future work, we would like to use more complex optimization
to 4096 vertices. Hu et al. [2019] show optimizations for up to 3000                   algorithms. Additionally, we are keen to explore end-to-end opti-
DoFs. Du et al. [2021] report gradient computation for resolutions                     mizations from image data by combining differentiable rendering
up to nearly 30,000 DoFs. Our examples show that our method is                         with differentiable simulation.
capable of computing gradients and perform optimizations with
several orders of magnitude increase in DoFs and increased mesh
resolutions. We show up to 65,968 vertices and 21 million DoFs.
                                                                                                                                                              Stuyck and Chen


REFERENCES                                                                                 Miles Macklin. 2022. Warp: A High-performance Python Framework for GPU Simu-
David Baraff and Andrew Witkin. 1998. Large steps in cloth simulation. In Proceedings         lation and Graphics. https://github.com/nvidia/warp. NVIDIA GPU Technology
   of the 25th annual conference on Computer graphics and interactive techniques. 43–54.      Conference (GTC).
Aric Bartle, Alla Sheffer, Vladimir G Kim, Danny M Kaufman, Nicholas Vining, and           Miles Macklin and Matthias Müller. 2021. A Constraint-Based Formulation of Stable
   Floraine Berthouzoz. 2016. Physics-driven pattern adjustment for direct 3D garment         Neo-Hookean Materials. In Proceedings of the 14th ACM SIGGRAPH Conference on
   editing. ACM Trans. Graph. 35, 4 (2016), 50–1.                                             Motion, Interaction and Games (Virtual Event, Switzerland) (MIG ’21). Association
Jan Bender, Matthias Müller, and Miles Macklin. 2017. A Survey on Position Based              for Computing Machinery, New York, NY, USA, Article 12, 7 pages. https://doi.
   Dynamics, 2017. In EUROGRAPHICS 2017 Tutorials. Eurographics Association.                  org/10.1145/3487983.3488289
Michael Betancourt, Charles C. Margossian, and Vianey Leos-Barajas. 2020. The              Miles Macklin, Matthias Müller, and Nuttapong Chentanez. 2016. XPBD: position-
   Discrete Adjoint Method: Efficient Derivatives for Functions of Discrete Sequences.        based simulation of compliant constrained dynamics. In Proceedings of the 9th
   arXiv:2002.00326 [stat.CO]                                                                 International Conference on Motion in Games. 49–54.
Sofien Bouaziz, Sebastian Martin, Tiantian Liu, Ladislav Kavan, and Mark Pauly. 2014.      Antoine McNamara, Adrien Treuille, Zoran Popović, and Jos Stam. 2004. Fluid control
   Projective dynamics: Fusing constraint projections for fast simulation. ACM trans-         using the adjoint method. ACM Transactions On Graphics (TOG) 23, 3 (2004),
   actions on graphics (TOG) 33, 4 (2014), 1–11.                                              449–456.
Andrew M Bradley. 2019. PDE-constrained optimization and the adjoint method.               Eder Miguel, Derek Bradley, Bernhard Thomaszewski, Bernd Bickel, Woj-
   https://cs.stanford.edu/~ambrad/adjoint_tutorial.pdf                                       ciech Matusik, Miguel A. Otaduy, and Steve Marschner. 2012.                   Data-
He Chen, Hyojoon Park, Kutay Macit, and Ladislav Kavan. 2021. Capturing detailed              Driven Estimation of Cloth Simulation Models. Computer Graphics Forum
   deformations of moving human bodies. ACM Transactions on Graphics (TOG) 40, 4              31, 2pt2 (2012), 519–528.          https://doi.org/10.1111/j.1467-8659.2012.03031.x
   (2021), 1–18.                                                                              arXiv:https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1467-8659.2012.03031.x
Hsiao-yu Chen, Edith Tretschk, Tuur Stuyck, Petr Kadlecek, Ladislav Kavan, Etienne         Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ra-
   Vouga, and Christoph Lassner. 2022. Virtual Elastic Objects. IEEE Conference on            mamoorthi, and Ren Ng. 2021. Nerf: Representing scenes as neural radiance fields
   Computer Vision and Pattern Recognition(CVPR) 2022 (2022).                                 for view synthesis. Commun. ACM 65, 1 (2021), 99–106.
Stelian Coros, Miles Macklin, Bernhard Thomaszewski, and Nils Thürey. 2021. Dif-           Matthias Müller, Bruno Heidelberger, Marcus Hennix, and John Ratcliff. 2007. Position
   ferentiable Simulation. In SIGGRAPH Asia 2021 Courses (Tokyo, Japan) (SA ’21).             based dynamics. Journal of Visual Communication and Image Representation 18, 2
   Association for Computing Machinery, New York, NY, USA, Article 3, 142 pages.              (2007), 109–118.
   https://doi.org/10.1145/3476117.3483433                                                 Jorge Nocedal and Stephen J. Wright. 2006. Numerical Optimization (2e ed.). Springer,
Tao Du, Kui Wu, Pingchuan Ma, Sebastien Wah, Andrew Spielberg, Daniela Rus, and               New York, NY, USA.
   Wojciech Matusik. 2021. DiffPD: Differentiable Projective Dynamics. ACM Trans.          Yi-Ling Qiao, Junbang Liang, Vladlen Koltun, and Ming C. Lin. 2020. Scalable Differ-
   Graph. 41, 2, Article 13 (nov 2021), 21 pages. https://doi.org/10.1145/3490168             entiable Physics for Learning and Control. In ICML.
Marco Fratarcangeli, Valentina Tibaldo, and Fabio Pellacini. 2016. Vivace: A practical     Breannan Smith, Fernando De Goes, and Theodore Kim. 2018. Stable Neo-Hookean
   gauss-seidel method for stable soft body dynamics. ACM Transactions on Graphics            Flesh Simulation. ACM Trans. Graph. 37, 2, Article 12 (mar 2018), 15 pages. https:
   (TOG) 35, 6 (2016), 1–9.                                                                   //doi.org/10.1145/3180491
Moritz Geilinger, David Hahn, Jonas Zehnder, Moritz Bächer, Bernhard Thomaszewski,         Michael Strecke and Jörg Stückler. 2021. DiffSDFSim: Differentiable Rigid-Body Dy-
   and Stelian Coros. 2020. Add: Analytically differentiable dynamics for multi-body          namics With Implicit Shapes. In International Conference on 3D Vision (3DV).
   systems with frictional contact. ACM Transactions on Graphics (TOG) 39, 6 (2020),       Tuur Stuyck. 2018. Cloth simulation for computer graphics. Synthesis Lectures on
   1–15.                                                                                      Visual Computing: Computer Graphics, Animation, Computational Photography, and
Arvi Gjoka, Zizhou Huang, Davi Colli Tozoni, Zachary Ferguson, Teseo Schneider,               Imaging 10, 3 (2018), 1–121.
   Daniele Panozzo, and Denis Zorin. 2022. Differentiable solver for time-dependent        Rasmus Tamstorf, Toby Jones, and Stephen F McCormick. 2015. Smoothed aggregation
   deformation problems with contact. arXiv preprint arXiv:2205.13643 (2022).                 multigrid for cloth simulation. ACM Transactions on Graphics (TOG) 34, 6 (2015),
Jingfan Guo, Jie Li, Rahul Narain, and Hyun Soo Park. 2021. Inverse Simulation:               1–13.
   Reconstructing Dynamic Geometry of Clothed Humans via Optimal Control. In               Nobuyuki Umetani, Danny M Kaufman, Takeo Igarashi, and Eitan Grinspun. 2011.
   IEEE Conference on Computer Vision and Pattern Recognition (CVPR).                         Sensitive couture for interactive garment modeling and editing. ACM Trans. Graph.
David Hahn, Pol Banzet, James M Bern, and Stelian Coros. 2019. Real2Sim: Visco-elastic        30, 4 (2011), 90.
   parameter estimation from dynamic motion. ACM Transactions on Graphics (TOG)            Huamin Wang, James F O’Brien, and Ravi Ramamoorthi. 2011. Data-driven elastic
   38, 6 (2019), 1–13.                                                                        models for cloth: modeling and measurement. ACM transactions on graphics (TOG)
Oshri Halimi, Tuur Stuyck, Donglai Xiang, Timur Bagautdinov, He Wen, Ron Kimmel,              30, 4 (2011), 1–12.
   Takaaki Shiratori, Chenglei Wu, Yaser Sheikh, and Fabian Prada. 2022. Pattern-          Ziyan Wang, Giljoo Nam, Tuur Stuyck, Stephen Lombardi, Chen Cao, Jason Saragih,
   Based Cloth Registration and Sparse-View Animation. ACM Trans. Graph. 41, 6,               Michael Zollhöfer, Jessica Hodgins, and Christoph Lassner. 2023. NeuWigs: A
   Article 196 (nov 2022), 17 pages. https://doi.org/10.1145/3550454.3555448                  Neural Dynamic Model for Volumetric Hair Capture and Animation. In Proceedings
Yuanming Hu. 2022. High-performance parallel programming in Python. https:                    of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
   //www.taichi-lang.org/.                                                                    8641–8651.
Yuanming Hu, Luke Anderson, Tzu-Mao Li, Qi Sun, Nathan Carr, Jonathan Ragan-               Ziyan Wang, Giljoo Nam, Tuur Stuyck, Stephen Lombardi, Michael Zollhöfer, Jessica
   Kelley, and Frédo Durand. 2020. DiffTaichi: Differentiable Programming for Physical        Hodgins, and Christoph Lassner. 2022. HVH: Learning a Hybrid Neural Volumet-
   Simulation. ICLR (2020).                                                                   ric Representation for Dynamic Hair Performance Capture. In Proceedings of the
Yuanming Hu, Jiancheng Liu, Andrew Spielberg, Joshua B Tenenbaum, William T                   IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 6143–
   Freeman, Jiajun Wu, Daniela Rus, and Wojciech Matusik. 2019. Chainqueen: A                 6154.
   real-time differentiable physical simulator for soft robotics. In 2019 International    Sebastian Weiss, Robert Maier, Daniel Cremers, Rudiger Westermann, and Nils Thuerey.
   conference on robotics and automation (ICRA). IEEE, 6265–6271.                             2020. Correspondence-free material reconstruction using sparse surface constraints.
Krishna Murthy Jatavallabhula, Miles Macklin, Florian Golemo, Vikram Voleti, Linda            In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recogni-
   Petrini, Martin Weiss, Breandan Considine, Jerome Parent-Levesque, Kevin Xie,              tion. 4686–4695.
   Kenny Erleben, Liam Paull, Florian Shkurti, Derek Nowrouzezahrai, and Sanja             Ryan White, Keenan Crane, and D. A. Forsyth. 2007. Capturing and animating occluded
   Fidler. 2021. gradSim: Differentiable simulation for system identification and             cloth. ACM Trans. Graph. 26 (July 2007). Issue 3.
   visuomotor control. International Conference on Learning Representations (ICLR)         Chris Wojtan, Peter J Mucha, and Greg Turk. 2006. Keyframe control of complex
   (2021). https://openreview.net/forum?id=c_E8kFWfhp0                                        particle systems using the adjoint method. In Proceedings of the 2006 ACM SIG-
Theodore Kim and David Eberle. 2022. Dynamic deformables: implementation and                  GRAPH/Eurographics symposium on Computer animation. 15–23.
   production practicalities (now with code!). In ACM SIGGRAPH 2022 Courses. 1–259.        Yaofeng Desmond Zhong, Jiequn Han, and Georgia Olympia Brikis. 2022. Differentiable
Egor Larionov, Marie-Lena Eckert, Katja Wolff, and Tuur Stuyck. 2022. Estimating Cloth        Physics Simulations with Contacts: Do They Have Correct Gradients wrt Position,
   Elasticity Parameters Using Position-Based Simulation of Compliant Constrained             Velocity and Control? arXiv preprint arXiv:2207.05060 (2022).
   Dynamics. arXiv preprint arXiv:2212.08790 (2022).
Yifei Li, Tao Du, Kui Wu, Jie Xu, and Wojciech Matusik. 2022. DiffCloth: Differentiable
   Cloth Simulation with Dry Frictional Contact. ACM Trans. Graph. 42, 1, Article 2
   (oct 2022), 20 pages. https://doi.org/10.1145/3527660
Junbang Liang, Ming Lin, and Vladlen Koltun. 2019. Differentiable cloth simulation
   for inverse problems. Advances in Neural Information Processing Systems 32 (2019).
Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J.
   Black. 2015. SMPL: A Skinned Multi-Person Linear Model. ACM Trans. Graphics
   (Proc. SIGGRAPH Asia) 34, 6 (Oct. 2015), 248:1–248:16.
DiffXPBD : Differentiable Position-Based Simulation of Compliant Constraint Dynamics


8     SUPPLEMENTAL MATERIAL                                                                    We can exploit the freedom of the Lagrange multipliers and set
We review the Adjoint method in Section 8.1 and demonstrate how                                                             𝜕F0 𝜕𝜓 0
                                                                                                                  𝝁 ⊤ + q̂⊤
                                                                                                                          0 𝜕q + 𝜕q = 0                      (22)
this applies to the simulation of compliant constraint dynamics in                                                             0       0
section 8.2.                                                                                and define the adjoint states in the backward difference manner
                                                                                                             ⊤       ⊤ 𝜕F𝑛−1            𝜕F𝑛 𝜕𝜙𝑛
8.1     The Adjoint Method                                                                                 q̂𝑛−1 = q̂𝑛−1         + q̂𝑛⊤      +       .       (23)
                                                                                                                           𝜕q𝑛          𝜕q𝑛 𝜕q𝑛
Consider the following time dependent optimization problem
                                                                                               The gradient of the Lagrangian can be simplified to the following
                                            min Φ(Q, u)                                     form
                                             u                                                                               𝑁 −1                   
                                                                                                         𝑑L           𝑑w ∑︁ 𝜕𝜙𝑛                  𝜕F𝑛
                      s.t. ∀𝑛             F𝑛 (q𝑛+1, q𝑛 , u) − q𝑛+1 = 0                                         = −𝝁 ⊤      +              + q̂𝑛⊤       .     (24)
                                                                                                         𝑑u           𝑑u 𝑛=0 𝜕u                   𝜕u
                                                                                     (18)
                                          q0 (u) = w,                                          A detailed discussion of the continuous adjoint method can be
where q𝑛 = [x𝑛 , v𝑛 ] ⊤ , Q = [q0, q1, ..., q𝑁 ] ⊤ is the concatenation of                  found in the tutorial by Bradley [2019], and the discrete adjoint
all the discrete state of positions and velocities given some initial                       method for forward Euler method by Betancourt et al. [2020].
some boundary condition w, and F is the time integration scheme.
Here we choose the commonly used first order implicit time inte-                            8.2      The Adjoint Method Applied to XPBD
gration scheme, but the derivation can be trivially modified to apply                       Given the XPBD implicit update rule, Q = F (Q, u) takes the form
to higher order and explicit methods. We can write the Lagrangian                                   
                                                                                                      x𝑛+1
                                                                                                            
                                                                                                               x + Δx (x𝑛+1 ) + Δ𝑡 v𝑛 + Δ𝑡M −1 fext
                                                                                                                                                    
of this system using the discrete Lagrange multipliers 𝝁 and q̂ as                                          = 𝑛           1                               (25)
                                                                                                      v𝑛+1               Δ𝑡 (x𝑛+1 − x𝑛 )
                                   𝑁
                                   ∑︁−1                                                     We find the implicit update rule for the adjoint states using Eq. 23.
    L = 𝝁 ⊤ (q0 − w) +                    𝜙𝑛 (q𝑛 , u) + q̂𝑛⊤ (F𝑛 (q𝑛+1, q𝑛 , u) − q𝑛+1 )    For a simulation of 𝑉 particles we find the adjoint states q̂𝑛 consist-
                                   𝑛=0
                                                                                            ing of adjoint positions x̂𝑛 ∈ R3𝑉 and adjoint velocities v̂𝑛 ∈ R3𝑉
                                                                                            as
      𝑑L        𝑑q0 𝑑w
                           𝑁
                           ∑︁−1
                                𝜕𝜙𝑛 𝑑q𝑛 𝜕𝜙𝑛        𝜕F𝑛                                                            𝜕F𝑛−1 ⊤         𝜕F𝑛 ⊤       𝜕𝜙𝑛 ⊤
         = 𝝁⊤ (    −    )+             +    + q̂𝑛⊤                                                       q̂𝑛−1 =          q̂𝑛−1 +       q̂𝑛 +                 (26)
      𝑑u        𝑑u   𝑑u         𝜕q𝑛 𝑑u   𝜕u         𝜕u                                                             𝜕q𝑛            𝜕q𝑛         𝜕q𝑛
                           𝑛=0
                                                                                     (19)                                                                       " 𝜕𝜙 # ⊤
              𝑁 −1                                                                                     " 𝜕Fx,𝑛−1   𝜕Fx,𝑛−1 ⊤                    𝜕Fx,𝑛 ⊤  
                                                                                                                           #          " 𝜕Fx,𝑛         #
                               𝜕F𝑛 𝑑q𝑛+1 𝜕F𝑛 𝑑q𝑛 𝜕q𝑛+1                                          x̂𝑛−1                           x̂𝑛−1                      x̂𝑛
              ∑︁
          +          q̂𝑛⊤ (             +        −     )                                               = 𝜕F𝜕x 𝑛      𝜕v𝑛               + 𝜕F𝜕x𝑛     𝜕v𝑛         + 𝜕x 𝑛

              𝑛=0
                              𝜕q𝑛+1 𝑑u    𝜕q𝑛 𝑑u   𝜕u                                           v̂𝑛−1       v,𝑛−1   𝜕Fv,𝑛−1     v̂𝑛−1       v,𝑛   𝜕Fv,𝑛    v̂𝑛    𝜕𝜙
                                                                                                            𝜕x𝑛      𝜕v𝑛                   𝜕x𝑛     𝜕v𝑛           𝜕v𝑛
    We can rearrange the last term into                                                                                                                         (27)
                                                                                            Computing and substituting the partial derivative terms relating to
         𝑁 −1                                                                               F, we find
         ∑︁               𝜕F𝑛 𝑑q𝑛+1 𝜕F𝑛 𝑑q𝑛 𝜕q𝑛+1
                q̂𝑛⊤ (             +        −     )
                                                                                                                                𝜕fext ⊤         v̂𝑛 v̂𝑛+1 𝜕𝜙 ⊤
                                                                                                                                     
                         𝜕q𝑛+1 𝑑u    𝜕q𝑛 𝑑u   𝜕u                                                               𝜕Δx
         𝑛=0                                                                                   x̂𝑛 = x̂𝑛+1 +        + Δ𝑡 2 M −1          x̂𝑛 +      −      +
                     𝜕F0 𝑑q0             𝜕F𝑁 −1 𝑑q𝑁           𝑑F                                                𝜕x               𝜕x             Δ𝑡      Δ𝑡   𝜕x
                 = q̂⊤
                     0          + q̂⊤
                                    𝑁 −1 𝜕q           − q̂𝑁 −1 𝑁                     (20)                                    ⊤                      ⊤
                     𝜕q0 𝑑u                      𝑑u            𝑑u                                      𝜕Δx              𝜕fext                      𝜕𝜙
                                             𝑁
                                                                                               v̂𝑛 =        + Δ𝑡 2 M −1          x̂𝑛 + Δ𝑡 x̂𝑛+1 +
                  𝑁 −1                                                                                  𝜕v               𝜕v                        𝜕v
                  ∑︁
                           ⊤ 𝜕F𝑛−1          𝜕F𝑛           𝑑q𝑛
                +      ( q̂𝑛−1        + q̂𝑛     − q̂𝑛−1 )                                                                                                       (28)
                  𝑛=1
                               𝜕q 𝑛         𝜕q𝑛           𝑑u

    Setting q̂𝑁 −1 = 0 and rearrange the terms
    𝑑L        𝑑q0 𝑑w            𝜕F0 𝑑q0
       =𝝁 ⊤ (     −     ) + q̂⊤
                              0 𝜕q 𝑑u
    𝑑u        𝑑u     𝑑u           0
           𝑁  −1
           ∑︁    𝜕𝜙𝑛 𝑑q𝑛 𝜕𝜙𝑛             𝜕F𝑛
        +                 +       + q̂𝑛⊤
           𝑛=0
                 𝜕q𝑛 𝑑u       𝜕u          𝜕u
               𝑁 −1
               ∑︁
                             ⊤     𝜕F𝑛−1       𝜕F𝑛           𝑑q𝑛
           +             ( q̂𝑛−1         + q̂𝑛     − q̂𝑛−1 )
                𝑛=1
                                    𝜕q𝑛        𝜕q𝑛           𝑑u
                                                                                     (21)
                      𝜕F0 𝜕𝜙 0 𝑑q0        ⊤ 𝑑w
         =(𝝁 + q̂⊤
               ⊤
                   0 𝜕q + 𝜕q ) 𝑑u − 𝝁 𝑑u
                        0     0
            𝑁 −1
            ∑︁
                     ⊤     𝜕F𝑛−1        𝜕F𝑛           𝜕𝜙𝑛 𝑑q𝑛
          +      ( q̂𝑛−1 −       + q̂𝑛⊤         ⊤
                                            − q̂𝑛−1 +    )
            𝑛=1
                            𝜕q𝑛         𝜕q𝑛           𝜕q𝑛 𝑑u
               𝑁 −1
               ∑︁   𝜕𝜙𝑛        𝜕q𝑛
           +            + q̂𝑛⊤
                𝑛=0
                     𝜕u         𝜕u
