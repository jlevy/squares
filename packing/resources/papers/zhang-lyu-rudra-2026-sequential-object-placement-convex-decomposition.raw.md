                                          Sequential Object Placement Optimization with Convex Decomposition
                                                    Yuezhe Zhang1 , Xiangyu Lyu1 , Sohan Rudra1 , Davide Tateo1,2,3 and Georgia Chalvatzaki1,4,5
arXiv:2608.25162v1 [cs.RO] 25 Aug 2026




                                                    Fig. 1: A sequence of screenshots of placing the Tangram puzzle using an Allegro Hand and an Xarm.

                                            Abstract— Robotic object packing has been a core challenge           sample-inefficient, and the exploration-exploitation dilemma
                                         for robotic deployment in logistics, industry, etc., due to             makes it difficult to generalize to non-convex shapes.
                                         the curse of dimensionality in combinatorial search and the
                                         difficulty of dealing with dynamic and contact constraints for             In this paper, we introduce SOPO-CD, a sequential op-
                                         irregularly shaped objects. Current heuristic and learning-             timization framework that frames object placement as a
                                         based methods assume a limited spatial discretization resolution        differentiable nonlinear optimization problem in a decom-
                                         of space, and computation becomes extremely inefficient as dis-         posed free space. We first divide the free space into a set
                                         cretization accuracy increases. In this work, we eliminate these        of convex hulls in 2D or 3D using greedy algorithms. We
                                         assumptions by introducing SOPO-CD, a sequential optimiza-
                                         tion framework that frames object placement as a differentiable         prove that placing a convex object inside a convex hull is
                                         nonlinear optimization problem in a decomposed free space.              essentially constraining the vertices of the object inside the
                                         We prove that placing a convex object inside a convex hull              convex hull. The constraints are more efficient than checking
                                         is essentially constraining the vertices of the object inside the       collisions among convex object pairs. We provide first- and
                                         convex hull. The constraints and their derivatives can be written       second-order analytic derivatives of the constraints and the
                                         in closed form and calculated within 200ns. We implement a
                                         custom solver that achieves optimal placement within tightly            Lagrangian function, resulting in 2 − 20 times faster than
                                         constrained space in milliseconds; a 100× speedup compared              an AutoDiff method. By selecting a set of convex hulls in
                                         to a classical grid search method. We generalize our framework          free space using heuristics and assigning the convex hull
                                         to 2D Tangram, 2D Tetris, and 3D Bin Packing, and have                  to each convex body of the object, we frame the object
                                         demonstrated strong computational performance and packing               placement as a differentiable nonlinear optimization problem.
                                         utility. We also demonstrate solving a real-world Tangram
                                         puzzle online using an Allegro Hand and an Xarm.                        We implement a custom Sequential Quadratic Programming
                                                                                                                 (SQP) solver based on [8] to solve the optimization problem
                                                                I. I NTRODUCTION                                 and achieve optimal placement within a tightly constrained
                                            Finding efficient placements of as many objects as possible          space in milliseconds.
                                         within a designated space has gained multidisciplinary inter-              We evaluate SOPO-CD on 2D Tangram, 2D Tetris, and
                                         ests from combinatorial optimization, computational geome-              3D Bin Packing. For Tangram, we test on a given sequence
                                         try, and machine learning. While existing algorithms [1], [2],          of objects and outperform SQP with a state-of-the-art dif-
                                         [3], [4], [5] have made strides in recent years, they often as-         ferentiable collision checker, achieving a 10× speedup and
                                         sume a predefined discretized action space for both position            much higher success rates. For Tetris, we test on a random
                                         and orientation, and the action space grows explosively with            sequence of objects and achieve a packing utility of 77% with
                                         the accuracy of the discretization. Packing Configuration               a computation time of 20ms per object in a batch of 8, a 50×
                                         Trees [6], [7] is the first learning-based method that solves           speedup over a grid search method. For 3D Bin Packing, we
                                         online 3D bin packing in a continuous space. However, it is             test on a random sequence of objects and achieve a packing
                                                                                                                 utility of 80% with a computation time of 15ms per object
                                           1 Interactive Robot Perception & Learning, Technical Univsersity of
                                                                                                                 in a batch of 8, a 100× speedup over a grid search method.
                                         Darmstadt, Germany; 2 Intelligent Autonomous Systems, Technical Uni-
                                         vsersity of Darmstadt, Germany; 3 Robotics and Semantic Systems, Lund   We also demonstrate a real-world Tangram puzzle task using
                                         University, Sweden; 4 Hessian.AI; 5 Robotics Institute Germany.         a high-degree-of-freedom system.
                    II. R ELATED W ORKS
   Early interest in the 3D bin packing problem focused                              minimize f (t, q)
                                                                                       t,q∈R3                                     (1)
primarily on the offline setting, where all items are known                                 s.t.     g(O, t, q) ∈ Cf ree
a priori and can be placed in arbitrary order. [9] solved this
problem with an exact branch-and-bound approach. How-                where g applies the transformations {t, q} on the object
ever, the problem is strongly NP-Hard, the exact algorithms          set O. Note that the object set O and collision-free space
do not guarantee optimal results within a reasonable amount          Cf ree are not necessarily convex, which makes the problem
of time. Therefore, heuristic methods and metaheuristic              challenging to solve.
approaches have been developed to obtain approximate
                                                                     B. Convex Hull Definition
solutions quickly, such as the Bottom-Left (BL) heuristic
[10] and the Best-Fit-Decreasing heuristic [11]. However,               The convex hull of a set of points S ∈ Rd is the
in many real-world application scenarios, e.g., logistics or         intersection of all convex sets containing S. We define the
warehousing, the upcoming items cannot be fully observed.            vertices of the convex hull as X = {x1 , x2 , . . . , xm }. There
Many online bin packing problems are solved using either             are two ways of representing the convex hull conv(X).
heuristics or learning-based methods. Deepest-Bottom-Left-              V-representation writes the convex hull as a convex com-
Fill (DBLF) [12] was proposed and combined with a genetic            bination of points in Rd . Mathematically, this reads
algorithm to place items in the deepest, bottom-most, left-                                      Xm          m
                                                                                                              X                    
                                                                                            d
most position. [1] performed grid search on a heightmap and            conv(X) = x ∈ R x =            ωi xi ,   ωi = 1, ωi ≥ 0
proposed a Heightmap-Minimization method to minimize the                                                  i=1       i=1
volume increase of the packed items. Many RL works [2],                                                                           (2)
[5] directly learn their policy on a grid by discretizing the full   where ωi , i = 1, . . . , m are the convex coefficients.
coordinate space, where the action space grows explosively              Alternatively, H-representation defines the convex hull as
with the discretization accuracy. Packing Configuration Trees        a finite number of inequalities. Mathematically, this yields
[6], [7] is the first learning-based method that solves online                                                      
3D bin packing in a continuous space. However, the size of                          conv(X) = x ∈ Rd Ax ≤ b                     (3)
the packing action space scales with the number of candidate
placements, which is still huge in continuous domains, and           where A and b can be computed from X and they determine
the sampling costs for training RL agents are thus expensive,        the halfspaces of the convex hull.
making it difficult to generalize to non-convex shapes.
   Therefore, we frame the object placement as an optimiza-          C. Differentiable Collision via LP
tion problem that handles the continuous space naturally. It            One state-of-the-art differentiable collision checker is pro-
is crucial to consider constraints in a differentiable manner.       posed by [14] as solving a Linear Cone Program between a
Differentiable collision checking between two convex shapes          set of convex primitives. It solves for the minimum uniform
can be formulated as a convex optimization problem [13],             scaling α that must be applied to the convex primitives S1 (α)
[14] and solved in microseconds. However, the computation            and S2 (α) for an intersection to occur. When primitives are
time may grow as the number of collision pairs grows. In             not in contact, the minimum scaling α > 1, and when the
the packing problem, this is important because the objects           objects are in contact, the minimum scaling α ≤ 1. The
to be placed need to check for collisions with all previously        problem is formulated as:
placed objects. In addition, it is challenging to do narrow-                             minimize α
space planning with the non-convex obstacles. We thus take                               α∈R,x∈R3
a different view by considering the object placement in the                                        s.t.    x ∈ S1 (α),            (4)
decomposed free space, inspired by [15], [16], [17], [18].                                                 x ∈ S2 (α),
Some recent works also frame stacking [19], [20], [21] as
an optimization problem, but they are soft constrained and                                                 α ≥ 0,
cannot generalize to placing a large number of objects in a             When the convex primitives are polytopes, the constraints
tightly constrained space.                                           are halfspace constraints of the convex hull.
                                                                                         IV. M ETHODOLOGY
                     III. P RELIMINARIES
                                                                     A. Convex Decomposition
A. Problem formulation
                                                                        We decompose the collision-free space into a set of convex
   We study the problem of optimal object placement within           sets Cf ree = C1 ∪ C2 ∪ · · · ∪ CL while keeping L as small
a constrained space. Given an object set O and the collision-        as possible. For 2D problems, we use constrained Delaunay
free space Cf ree , we aim to find the optimal translation           Triangulation [22] to split the non-convex free space into a
t ∈ R3 and rotation parameters q ∈ R3 that optimizes the             number of triangles. It will output a list of valid triangles,
objective function f (t, q), such as the depth of the object,        and adjacent triangle pairs. We implement a greedy algorithm
and makes the object collision free.                                 to merge adjacent triangles into larger convex polygons. We
Fig. 2: Visualization of the Tangram puzzle with the given object sequence and cost functions. The first two rows show the
free-space decomposition using Delaunay Triangulation [22] and merged convex polygons. At each iteration, we select the
largest convex hull, and SQP will calculate the best placement in this convex hull, as shown in the third row.

will only merge the triangles/polygons when they share the           We consider each convex free space as a convex hull,
same edge, and the potential merged polygon is convex,            which can be represented using A ∈ Rk×3 and b ∈ Rk
and the area of the merged polygon is large enough. The           in a world frame W via H-representation. The number of
algorithm runs in a loop and will terminate when there are        halfspace constraints is k. Each object is defined with an
no adjacent polygons that can be merged. The complexity of        attached body reference frame B with an origin r ∈ R3
the merging algorithm is O(N 2 ), where N is the number of        expressed in a world frame W. The vertices of the object
triangle pieces.                                                  can be expressed as Vi ∈ R3 , 1 ≤ i ≤ l in frame B, where l
   For 3D Packing, the 3D free space is represented as a 2D       is the number of vertices. The translation of the object can be
heightmap of size M ×M . We implement a greedy algorithm          defined as t ∈ R3 . The orientation of an object is defined by
to partition the free space into a set of axis-aligned Maximal    a rotation matrix W QB ∈ R3×3 in the world frame, denoted
Empty Cuboids [23]. The algorithm sequentially scans the          as Q for shorthand.
heightmap to locate uncovered cells. Upon finding a seed             Therefore, the vertices of the object can be expressed in
cell at height z, it executes a two-stage expansion along the     W as r + t + QVi . And we can express the constraint that
X and Y axes to compute a maximal flat bounding region.           each vertex lies inside the free space as:
This region is then extruded vertically to the maximum
container height, forming a candidate 3D convex hull. To                           A(r + t + QVi ) ≤ b, 1 ≤ i ≤ l.            (5)
optimize execution, regions that fail minimum volume or
width constraints are logged into a rejection buffer alongside
                                                                    Then the problem of convex object placement can be
valid hulls. This design ensures that each coordinate is
                                                                  written as:
evaluated as a candidate origin at most once, yielding an
overall algorithmic complexity of O(M 2 ).                           minimize f (t, q)
                                                                       t,q∈R3                                                 (6)
B. Differentiable Collision Checking in Free Space                          s.t.   A(r + t + Q(q)Vi ) − b ≤ 0, 1 ≤ i ≤ l.
Theorem 1. A convex hull A is inside another convex hull
B if and only if the vertices of A are inside B.                    We denote gi (t, q) = A(r + t + Q(q)Vi ) − b ∈ Rk . If we
Proof. Sufficiency: Given that A ⊆ B and the vertices of A        want to minimize the height of all the vertices in W, we can
are a subset of A, it is obvious that the vertices of A are a     choose
subset of B.                                                                                     l
   Necessity: Given that the vertices of A are a subset of
                                                                                                 X
                                                                                    f (t, q) =     (t + Q(q)Vi )z ,           (7)
B, we want to prove that any point in A also belongs to                                          i=1
B. Since the vertices of A are a convex combination of the
vertices of B, and any point in A is a convex combination         where the subscript z means to retrieve the third element of
of the vertices of A. It is not difficult to calculate that any   the position. Similarly, we can minimize a linear combination
point in A can be expressed as a convex combination of the        of the x, y, z positions of the sum of all vertices. The problem
vertices of B.                                                    is nonlinear, as the mapping from the representation q to the
                                                                  rotation matrix Q is nonlinear.
C. Convex Hull Selection and Assignment
   Now we can divide the free space into a set of convex
hulls, and we can represent the constraint of placing each
convex object inside each specific convex hull. However, the
assignment between the convex hull and the convex object
can result in different solutions. For example, if the volume
of the convex hull is smaller than that of the convex object,
there is no solution to place it inside. Iterating over all the
convex hulls and solve the placement inside each convex
hull is exhaustive but time-consuming. We rely on a set of         Fig. 3: Illustration of hull assignment for placing an L-shape
heuristics to improve the solution quality and computational       object. The free-space convex hulls can be grouped into 5
performance.                                                       pairs of adjacent hulls. We sort the pairs by height and
   For the Tangram puzzle, we select the largest convex hull       select the top k = 2 hull pairs. Each convex body of the
to place at each step. For 3D Bin Packing, at each step we         object is assigned to each hull, resulting in 4 combinations
sort the free-space convex hulls by height and volume. We          of constraint pairs, and we will solve these 4 problems
first select the lowest and largest convex hull, then proceed      separately.
to the next one. We iterate until we solve the placement
optimization for each hull from the top k convex hulls. If         where ∂Q is a third-order tensor and can be explicitly written
                                                                      ∂q 
there is no solution, we consider it a failure; otherwise, we          ∂Q         ∂Q
                                                                   as ∂q       = ∂qkij . 1
select the best solution based on the objective function.                    ijk

   For non-convex object placement, it is more difficult to           Since gi ∈ Rk , the second-order derivative of gi with
solve, as the different convex bodies of the object can belong     respect to x is a third-order tensor. To express it efficiently,
to different convex hulls. A conservative estimate that treats     we denote gij = Aj (r + t + Q(q)Vi ) − bj ∈ R, 1 ≤ j ≤ k,
the non-convex object as a single convex hull may work in          where Aj ∈ R1×3 and bj ∈ R represent each halfspace
simple scenarios, but it is not applicable to placement in         constraint. Then we can calculate the Hessian as:
narrow spaces, such as in the Tetris problem. As shown in                      " ∂2g     ∂ 2 gij
                                                                                                 # "                 #
                                                                     ∂ 2 gij      ∂t2
                                                                                     ij
                                                                                                    0        0
Fig. 3, the free space is split into a set of convex hulls. We                           ∂t∂q
                                                                             = ∂ 2 gij ∂ 2 gij =            ∂2Q        ∈ R6×6 (10)
associate adjacent hulls and sort the resulting pairs by height.      ∂x2                     2
                                                                                                    0   A j ∂q 2 V i
                                                                                    ∂q∂t   ∂q
We solve for the top k lowest pairs separately. For each pair,                  2                  2
we denote the convex hulls as B1 , B2 , and their halfspace        where Aj ∂∂qQ
                                                                               2 Vi ∈ R
                                                                                          3×3 ∂ Q
                                                                                             , ∂q2 is a fourth-order tensor and
                                                                                                              ∂2Q
                                                                                                 2 
constraints as Ā1 ∈ Rk×3 , b̄1 ∈ R3 and Ā2 ∈ Rk×3 , b̄2 ∈ R3 .   can be explicitly written as ∂∂qQ2      = ∂qk ∂qijl .
For the non-convex tetrominoes, we can split them into two                                                  ijkl
                                                                      We choose the Euler angle as the representation q =
convex bodies as A1 , A2 , and we can denote their vertices
                                                                   [α, β, γ] and follow the ZYX convention. We have Q =
as Vi , 1 ≤ i ≤ k1 and Vi , k1 < i ≤ k2 . Given these two
                                                                   Rz (γ)Ry (β)Rx (α), where the rotation matrices can be writ-
pairs, we can have two assignments A1 ⊆ B1 , A2 ⊆ B2 or
                                                                   ten as:
A1 ⊆ B2 , A2 ⊆ B1 . We write the problem for the assignment
A1 ⊆ B1 , A2 ⊆ B2 as:
                                                                                                                      
                                                                                  cγ −sγ 0                  cβ 0 sβ
  minimize f (t, q)                                                   Rz (γ) = sγ cγ 0 , Ry (β) =  0            1 0 ,
    t,q∈R3                                                                         0   0     1             −sβ 0 cβ
         s.t.   Ā1 (r + t + Q(q)Vi ) − b̄1 ≤ 0, 1 ≤ i ≤ k1                     
                                                                                 1 0       0
                                                                                               
              Ā2 (r + t + Q(q)Vi ) − b̄2 ≤ 0, k1 < i ≤ k2 .          Rx (α) = 0 cα −sα  ,
                                                           (8)                   0 sα cα
  Here, we can adopt similar objective functions as in 7. If                                                              (11)
we choose the top k lowest adjacent hulls, we need to solve
                                                                   where c and s represent cos and sin functions. Rotation
2k different optimization problems.
                                                                   matrices have some good properties that we can use,
D. Compute Analytic Derivative                                                                 
   We have framed the convex object placement in eq. 6 and                         0   0      0
                                                                      ∂Rx (α) 
Tetris placement in eq. 8. Given that the constraints and cost                 = 0 −sα −cα  = Rx (α + π/2) − E11 ,
                                                                          ∂α
functions are written explicitly with respect to variables t, q,                   0 cα −sα
                                                                                               
we can calculate the gradient of the cost function, the Jaco-                      0   0      0
                                                                     ∂ 2 Rx (α) 
bian of the constraints, and the Hessian of the Lagrangian                     = 0 −cα sα  = −Rx (α) + E11 ,
                                                                         ∂α2
function directly in closed form. We denote x = [t, q] ∈ R6                        0 −sα −cα
and consider the constraint gi = A(r + t + Q(q)Vi ) − b.                                                               (12)
We can write the Jacobians as:
         ∂gi    h          i h               i                       1 q means the k-th value of vector q and does not mean the covariant
             = ∂g ∂t
                    i  ∂gi
                        ∂q  = A A ∂Q    ∂q Vi ∈ R
                                                   k×6      (9)         k
                                                                   component.
         ∂x
where Eij is the standard basis matrix that has value 1 at               The Lagrangian function for this problem is
index i, j and 0 elsewhere. Similarly, we can have
                                                                             L(x, λ) = f (x) + λT c(x),             (18)
∂Ry (β)                        ∂ 2 Ry (β)
        = Ry (β + π/2) − E22 ,            = −Ry (β) + E22 , where λ ∈ R is the lagrangian multiplier. We can compute
                                                                         kl
  ∂β                               ∂β 2
                                                            the Hessian of the Lagrangian function as:
∂Rz (γ)                        ∂ 2 Rz (γ)
        = Rz (γ + π/2) − E33 ,            = −Rz (γ) + E33 ,                           l X k
                                                                                                 ∂ 2 gij
                                                                                                                    
  ∂γ                              ∂γ 2                         2              2
                                                                                     X                      0   0
                                                     (13)     ∇xx L(x, λ) = ∇xx f +          λij         =             ,
                                                                                                  ∂x2       0 ∇2qq L
                                                                                                  i=1 j=1
  Using the chain rule, we can compute                                                            l X
                                                                                                    k
                                                                                                  X               ∂ 2 gij
   ∂Q                 ∂Rx (α)                                           ∇2qq L(x, λ) = ∇2qq f +             λij           ∈ R3×3
      = Rz (γ)Ry (β)                                                                                               ∂q 2
   ∂α                     ∂α                                                                      i=1 j=1
      = Rz (γ)Ry (β)(Rx (α + π/2) − E11 )                                                                                          (19)
  ∂2Q                 ∂ 2 Rx (α)                                                           2
                                                                                          ∂ g
                                                                       where ∇2xx f and ∂x2ij can be calculated using eq. 16 and
      = Rz (γ)R y (β)
  ∂α2                     ∂α2                                          eq. 10. To make the calculations more efficient, we use
      = Rz (γ)Ry (β)(−Rx (α) + E11 )                                   the Kronecker product and vectorization to eliminate for
 ∂2Q           ∂Ry (β) ∂Rx (α)                                         loops when computing the analytic derivatives. The memory
      = Rz (γ)
∂α∂β             ∂β        ∂α                                          is entirely stack-allocated and one-shot during initialization
      = Rz (γ)(Ry (β + π/2) − E22 )(Rx (α + π/2) − E11 )               without tedious forward or backward calculations in auto-
                                                                       matic differentiation.
 ∂2Q    ∂Rz (γ)          ∂Rx (α)
      =         Ry (β)                                                 E. Object Placement Optimization via SQP
∂α∂γ      ∂γ               ∂α
      = (Rz (γ + π/2) − E33 )Ry (β)(Rx (α + π/2) − E11 )                  We solve the nonlinear optimization problem 6 and 8
                                                   (14)                via Sequential Quadratic Programming [24]. The idea is
                                              2     2      2           to model the optimization problem at the current iterate
   Similarly, we can compute ∂Q         ∂Q ∂ Q ∂ Q ∂ Q
                                   ∂β , ∂γ , ∂β 2 , ∂γ 2 , ∂β∂γ . At   (xn , λn ) as a quadratic programming subproblem, then use
every iteration when we have the values of α, β, γ,                    its solution to obtain a new iterate (xn+1 , λn+1 ). Suppose at
we first compute the rotation matrices Rx (α), Rx (α +                 iterate (xn , λn ), the quadratic problem is modeled as:
π/2), Ry (β), Ry (β +π/2), Rz (γ), Rz (γ +π/2), then we can
                   ∂2Q
                                                                                                               1
calculate ∂Q
           ∂q and ∂q 2 by composing these rotation matrices
                                                                                   minimize fn + ∇fnT p + pT ∇2xx Ln p
                                                                                      p∈R 6                    2                 (20)
following eq. 14.
   If we choose the cost function f as in eq. 7, we can                                    s.t. Jn p + cn ≤ 0
calculate the gradient of the cost function as                         where Jn and cn are the Jacobian matrix and constraints at
                 
                   ∇t f
                                                                      xn defined in eq. 17.
           ∇f =             ∈ R6 ,                                        We use Clarabel [8] to solve the QP problem. Note that
                   ∇q f
                                                                   in eq. 19, ∇2xx Ln is zero everywhere except the bottom
                     0        0                                        right block ∇2qq Ln , and ∇2qq Ln is possibly indefinite. We
          ∇t f = l 0 = 0 ,                                         add a scaled identity matrix to ∇2xx Ln to improve numerical
                     1         l                                (15)   stability. We perform a backtracking line search to calculate
                 h                        iX  l                        how far we should move along the direction p and enforce a
          ∇q f = ∂Q ∂q
                       31    ∂Q32
                              ∂q
                                    ∂Q33
                                      ∂q         Vi                    sufficient decrease in the merit function following the Armijo
                                             i=1                       rule. We choose the merit function ϕ(x, µ) = f (x)+µT c(x),
                      ∂Q31        ∂Q32         ∂Q33                    where µ ∈ Rkl is the penalty parameter. The penalty param-
                 = ā       + b̄         + c̄         ∈ R3 ,
                       ∂q           ∂q           ∂q                    eter is zero when the corresponding constraint is smaller than
                      Pl                                               the threshold tol; otherwise, it is set to a positive constant.
where the constant i=1 Vi is denoted as [ā, b̄, c̄]T . Then we
can calculate the Hessian of the cost function as                      The SQP terminates when the norm of the current step ∥p∥
             
               0       0
                                                                      and the constraint violation max(cn ) are smaller than the
   ∇2xx f =                   ∈ R6×6 ,                                 tolerance threshold tol. We set tol = 1 × 10−4 and the
               0 ∇2qq f
                                                               (16)    maximum SQP iteration number to 50.
                ∂ 2 Q31       ∂ 2 Q32       ∂ 2 Q33                       Like many other optimization methods, SQP is also a
    ∇2qq f = ā          + b̄          + c̄          ∈ R3×3
                                                             .
                  ∂q 2          ∂q 2          ∂q 2                     local-optimal solver, making it difficult to find global op-
  We use c(x) and J(x) to denote the whole constraints and             timal solutions in one shot. In our placement setting, global
Jacobian matrix of the constraints,                                    optimality is essential: a local optimal solution may have
           
            g1 (x)
                                            ∂g1                     zero constraint violation, yet its failure to achieve the best
                                                ∂x
           g2 (x)                          ∂g2                     placement leaves no room for the following objects to be
                                                ∂x 
  c(x) =  .  ∈ Rkl , J(x) =  .  ∈ Rkl×6 , (17)                     placed. We thus parallelize the SQP solver using randomized
                                          
            . .                            ..                      initial states and select the best placement based on the merit
             gl (x)                         ∂gl
                                            ∂x
                                                                       function.
TABLE I: Computation time for calculating gradient, Jaco-                                     TABLE III: Performance for full sequence Tangram.
bian, and Hessian.
                                                                                                        n threads   total time (ms)   successful placements   memory estimate (MiB)
                                                                                                            2            9.02                 4.35                     2.53
                   scenario     gradient (ns)        Jacobian (ns)        Hessian (ns)                      4            9.31                 5.62                     4.66
                                                                                            SOPO-CD
                      2D               16.29             24.96               41.45                          8           10.02                 6.63                     9.44
  Analytic                                                                                                 16           12.98                 6.96                    17.67
                      3D               90.79             188.70             368.59
                                                                                                            2            27.48                2.63                     3.26
                      2D                21.16            45.70               311.65         DCOL
                                                                                                            4            46.34                3.54                     6.76
  ForwardDiff                                                                                               8            91.79                4.53                    18.26
                      3D               167.82            345.27             7652.00
                                                                                                           16           123.58                4.95                    61.95




                               V. R ESULTS                                                 to place the last two objects, since the SQP iterations hit the
   We implement our algorithms in Julia and leverage Bench-                                maximum limit of 50.
markTools [25] to efficiently run all our modules multiple                                    We also report the median total time, average number of
times to evaluate computational performance. We run ex-                                    successful placements, and memory estimates for placing the
periments on a computer with an AMD Ryzen 9 7950x3D                                        full sequence of objects in Table III. SOPO-CD consistently
16-core CPU.                                                                               performs better than SQP with DCOL. When setting the
                                                                                           number of threads to 8, our method can place almost all
A. Analytic Derivatives vs. AutoDiff                                                       7 objects successfully with a total computation time around
   We first compare the computational performance between                                  10ms.
analytic derivatives and ForwardDiff [26]. During each run,
                                                                                           C. Solve 2D Tetris Puzzle
we randomize the object’s state in 2D and 3D scenarios and
compute the gradient of the cost function, the Jacobian of the                                We evaluate our method on the 5-Tetris and 8-Tetris
constraints, and the Hessian of the Lagrangian. We report the                              benchmarks introduced by cuTAMP [20] and SPaSM [21].
median computation time in Table I. At every run, we check                                 The goal is to determine feasible object poses for the 5 and
that the values of the analytic derivatives are identical to                               8 objects so that they fit within a constrained bounding box.
the values of ForwardDiff. The computation time of analytic                                We compare with SPaSM without trajectory optimization.
derivatives is consistently better than ForwardDiff in 2D                                  The results of our method are shown in Table IV. The total
and 3D scenarios, especially for the most time-consuming                                   time reports the total average time for convex decomposition,
Hessian calculation; the analytic solution is almost 10 − 20                               constraint extraction, and batch SQP calculations. The total
times faster.                                                                              time for 5-Tetris is around 3 − 5ms. The total time for 8-
                                                                                           Tetris is around 7 − 11ms. The success rate and number of
B. Solve Tangram Puzzle                                                                    successful placements increase with the number of threads,
   We evaluate our method on a Tangram puzzle as shown                                     and it is almost always successful when setting the number
in Fig. 2. Here, the object sequence and corresponding                                     of threads to 8.
cost functions are given, and we aim to find the optimal                                      We run SPaSM on 5-Tetris and 8-Tetris on an NVIDIA
placement at each time step while minimizing or maximizing                                 GeForce RTX 4090 GPU. The results of SPaSM are shown in
the objects’ height or width. We compare SOPO-CD to                                        Table V. We keep the remaining hyperparameters unchanged
the same SQP with Differentiable Collision (DCOL) [14],                                    and test only on different termination cost thresholds. The
where DCOL uses ForwardDiff to calculate the constraint                                    default cost thresholds for 5-Tetris and 8-Tetris are 0.42 and
Jacobians and Hessian of the Lagrangian by default. We                                     0.66, respectively. In these settings, the algorithms converge
report the median computation time and average converged                                   within 1 and 10ms, with an average penetration of the wall
SQP iterations for placing each object in Table II. For                                    and sphere between 2 × 10−4 and 3 × 10−3 . We also observe
each object, the convex decomposition preprocessing takes                                  that lowering the cost threshold can improve the penetration
25−75µs. With convex decomposition, SQP shows consistent                                   distance, but SPaSM will not converge when the threshold
performance, takes less time (0.2 − 0.8ms per object), and                                 is much lower. In contrast, our method can handle hard
requires fewer iterations to converge. Compared to us, for                                 constraints with a tolerance of 1 × 10−4 .
SQP with DCOL, the computation time increases as the                                          We generalize our method to a full Tetris problem, where
number of objects grows, because the number of collision                                   we include all 7 different tetrominoes, as shown in Fig.
pairs between the current object and the placed objects                                    4. The objective function for each placement is f (t, q) =
increases. As a consequence, it is very challenging for DCOL
                                                                                           TABLE IV: Performance for mini Tetris using SOPO-CD.
    TABLE II: Computation time per step for Tangram.                                                   n threads    total time (ms)     successful placements     success rate (%)
                               obj 1     obj 2   obj 3   obj 4    obj 5    obj 6   obj 7                   2              3.14                   4.75                   74.95
                                                                                            5-Tetris       4              3.46                   4.94                   93.71
             Preprocess (µs)   35.34     60.35   25.05   75.44    49.64    39.94   31.78
 SOPO-CD     SQP Time (ms)      0.84      0.18    0.19    0.26     0.36     0.25    0.26                   8              4.62                   4.99                   99.84
             SQP Iters         12.53     3.86    4.21    4.71     11.00    4.00    6.23                    2             10.45                   7.28                   35.13
             SQP Time (ms)      0.87      1.02   0.97     3.43    15.67    17.63   20.76    8-Tetris       4              6.90                   7.80                   81.05
 DCOL                                                                                                      8              8.22                   7.99                   98.71
             SQP Iters         12.68     13.49   6.94    27.31    33.96    49.91   50.00
TABLE V: Performance for mini Tetris using SPaSM [21].
                 cost thresh        total time (ms)      wall penetration         sphere penetration        success rate (%)
                    0.42                 0.22                 3.10e-3                  3.00e-4                     100
                    0.38                 3.52                 3.08e-3                  2.86e-4                     100
 5-Tetris
                    0.37                95.11                 2.83e-3                  3.18e-4                     100
                   ≤0.36                   -                     -                        -                         0
                    0.66                 6.84                 2.93e-3                  2.34e-4                     100
 8-Tetris           0.64                14.15                 2.89e-3                  2.08e-4                     100
                    0.63                55.78                 2.97e-3                  1.86e-4                     100
                   ≤0.62                   -                     -                        -                         0




                                                                                                                                  Fig. 5: An intermediate screenshot of convex hull generation
                                                                                                                                  and placed objects for 3D Bin Packing.

                                                                                                                                  represent the occupied objects. The heightmap is character-
                                                                                                                                  ized by a predefined grid size M × M . For every object
                                                                                                                                  placement, we use the same objective function as the grid
                                                                                                                                  search algorithm, f (t, q) = tx +ty +5tz , where t = [tx , ty , tz ]
                                                                                                                                  is the center of the cuboid. This is the same heuristic as
                                                                                                                                  in DBLF [12]. The time complexity for the grid search
Fig. 4: An intermediate screenshot of convex hull generation                                                                      algorithm is O(M 2 ).
and placed objects for 2D Tetris.                                                                                                    We test SOPO-CD against the grid search algorithm on
Pl                      Pl                                                                                                        a number of random sequences of objects. The convex hull
   i=1 (t+Q(q)Vi )x +5     i=1 (t+Q(q)Vi )y , which optimizes                                                                     generation and placed objects at an intermediate step are
the object to be at the bottom-left area. We test our method                                                                      visualized in Fig. 5. The quantitative results are shown
against a grid search algorithm on a number of random                                                                             in Table VIII. We compare the average preprocessing and
sequences. We show the results of grid search on different                                                                        computation times for each object, the number of successful
grid sizes in Table VI. We show the results of SOPO-CD on                                                                         placements across the whole sequence, and the occupancy
different top k convex pairs in Table VII. At each iteration,                                                                     rate for all placements. The preprocessing includes convex
the preprocessing takes around 6µs and solving 2k placement                                                                       hull generation and constraint extraction. It is shown that
optimization problems for each object takes 10 − 20ms. As                                                                         the search time grows drastically as the grid size increases.
the solver batch size and top-k increase, the number of                                                                           The preprocessing time for our method also increases with
successful placements and the occupancy rate rise, reaching                                                                       grid size, but remains within 1ms. Our method generates
77% when setting the number of threads to 8 and k = 1. The                                                                        a set of axis-aligned convex hulls, and we select the 3
computation time of SOPO-CD is consistently performant,                                                                           lowest convex hulls and run the batched SQP solver on
and it is 50 times faster than grid search at the largest grid                                                                    each hull. The computation time of our method shows
size.                                                                                                                             consistent performance across varying grid sizes and grows
D. Solve 3D Bin Packing                                                                                                           only linearly with the solver batch size and the number of
                                                                                                                                  selected convex hulls. At the largest grid size, our method is
   We evaluate our method on the 3D Bin Packing prob-
                                                                                                                                  more than 200 times faster than the grid search algorithm.
lem and compare it with the standard grid search algo-
                                                                                                                                  The number of successful placements and the occupancy rate
rithm on the heightmap. The container size is [5, 5, 5], and
                                                                                                                                  also increase significantly as the solver batch size increases,
the packed objects are 3D rectangular shapes with sizes
                                                                                                                                  and the performance is competitive with that of the grid
[3, 2, 1], [2, 2, 2], [1, 2, 2], [1, 1, 2]. We use the heightmap to
                                                                                                                                  search.

 TABLE VI: Performance for full Tetris using grid search.                                                                                    TABLE VIII: Performance for 3D Bin Packing.
                                                                                                                                                   grid size   preprocess per obj (µs)   compute time per obj (ms)   successful placements   occupancy rate (%)
                        grid size     compute time per obj (ms)          successful placements          occupancy rate (%)                          10×10                 -                        0.01                     21.80                  85.32
                                                                                                                                                    50×50                 -                        0.41                     21.93                  85.47
                          8×8                     0.03                              14.10                       84.86              Grid Search     100×100                -                        6.28                     22.04                  86.63
 Grid-Search             80×80                    1.69                              13.97                       83.92                              250×250                -                       222.60                    21.70                  85.47
                        800×800                  1455.24                            13.67                       82.29                              500×500                -                      3940.55                    22.20                  85.97
                                                                                                                                                    10×10               1.46                       7.32                     16.17                  62.02
                                                                                                                                                    50×50               9.36                       7.49                     17.02                  64.42
                                                                                                                                   SOPO-CD
                                                                                                                                                   100×100              31.83                      7.22                     16.02                  62.84
                                                                                                                                   (n threads=2)
                   TABLE VII: Performance for full Tetris.                                                                                         250×250
                                                                                                                                                   500×500
                                                                                                                                                                       189.92
                                                                                                                                                                       666.90
                                                                                                                                                                                                   7.67
                                                                                                                                                                                                   8.02
                                                                                                                                                                                                                            16.20
                                                                                                                                                                                                                            16.42
                                                                                                                                                                                                                                                   64.20
                                                                                                                                                                                                                                                   64.53
                                                                                                                                                    10×10               1.57                      10.74                     19.77                  76.92
                  top k     preprocess per obj (µs)   compute time per obj (ms)     successful placements    occupancy rate (%)                     50×50               9.66                      10.78                     19.60                  77.25
                                                                                                                                   SOPO-CD
                    1                5.40                       9.05                         9.95                  59.46                           100×100              33.32                     10.64                     18.53                  74.73
 SOPO-CD                                                                                                                           (n threads=4)
                    2                5.59                      13.52                        10.88                  65.13                           250×250             180.40                     10.08                     19.94                  76.38
 (n threads=2)                                                                                                                                     500×500             694.34                     10.93                     19.94                  77.86
                    3                5.83                      18.70                        11.06                  66.23
                                                                                                                                                    10×10               1.69                      19.90                     20.57                  81.00
                    1                5.73                      12.39                        12.06                  72.28
 SOPO-CD                                                                                                                                            50×50               9.52                      14.31                     20.45                  81.31
                    2                6.09                      19.06                        12.28                  73.62           SOPO-CD
 (n threads=4)                                                                                                                                     100×100              31.21                     14.04                     21.33                  81.72
                    3                5.84                      26.05                        12.32                  73.94           (n threads=8)
                                                                                                                                                   250×250             176.49                     13.92                     22.18                  83.30
                    1                5.58                      16.19                        12.75                  76.56                           500×500             692.78                     14.68                     20.30                  80.26
 SOPO-CD
                    2                6.27                      24.02                        12.61                  75.66
 (n threads=8)
                    3                6.39                      34.31                        12.79                  76.79
E. Real-world Experiment                                                      [7] H. Zhao, J. Xu, K. Yu, R. Hu, C. Zhu, B. Du, and K. Xu, “Deliberate
                                                                                  planning of 3d bin packing on packing configuration trees,” The
   For the real-world experiment, we deploy our algorithm                         International Journal of Robotics Research, 2025.
to solve the Tangram puzzle using an Allegro hand and an                      [8] P. J. Goulart and Y. Chen, “Clarabel: An interior-point solver for conic
                                                                                  programs with quadratic objectives,” arXiv preprint arXiv:2405.12762,
Xarm, as shown in Fig. 1. The system runs in an open loop;                        2024.
once the object’s goal location is calculated, it is fed into                 [9] S. Martello, D. Pisinger, and D. Vigo, “The three-dimensional bin
the motion planner to perform pick-and-place. We predefine                        packing problem,” Operations research, vol. 48, no. 2, pp. 256–267,
                                                                                  2000.
the contact points for each object and the finger, and run an                [10] B. S. Baker, E. G. Coffman, Jr, and R. L. Rivest, “Orthogonal packings
online optimization to compute the force closure. We plan                         in two dimensions,” SIAM Journal on computing, vol. 9, no. 4, pp.
and control the arm using an off-the-shelf sampling-based                         846–855, 1980.
                                                                             [11] D. S. Johnson, A. Demers, J. D. Ullman, M. R. Garey, and R. L.
motion planner [27].                                                              Graham, “Worst-case performance bounds for simple one-dimensional
                                                                                  packing algorithms,” SIAM Journal on computing, vol. 3, no. 4, pp.
                         VI. C ONCLUSION                                          299–325, 1974.
                                                                             [12] K. Karabulut and M. M. İnceoğlu, “A hybrid genetic algorithm for
   We introduced SOPO-CD, a sequential optimization                               packing in 3d with deepest bottom left with fill method,” in Inter-
framework that solves the object placement problem with                           national Conference on Advances in Information Systems. Springer,
differentiable collision constraints in free space. We divided                    2004, pp. 441–450.
                                                                             [13] L. Montaut, Q. Le Lidec, A. Bambade, V. Petrik, J. Sivic, and J. Car-
the collision-free space into various convex hulls and as-                        pentier, “Differentiable collision detection: a randomized smoothing
signed the convex hull to each convex body. We implemented                        approach,” in IEEE International Conference on Robotics and Au-
a custom SQP solver and solved the optimal placement in                           tomation, 2023, pp. 3240–3246.
                                                                             [14] K. Tracy, T. A. Howell, and Z. Manchester, “Differentiable collision
milliseconds. We validated our method on a set of tasks,                          detection for a set of convex primitives,” in IEEE International
including the 2D Tangram puzzle, 2D Tetris puzzle, and 3D                         Conference on Robotics and Automation, 2023, pp. 3663–3670.
Bin Packing, and demonstrated strong computational perfor-                   [15] R. Deits and R. Tedrake, “Computing large convex regions of obstacle-
                                                                                  free space through semidefinite programming,” in International Work-
mance and packing utility. We also demonstrated solving a                         shop on the Algorithmic Foundations of Robotics. Springer, 2015,
real-world Tangram puzzle using an Allegro Hand and an                            pp. 109–124.
Xarm.                                                                        [16] S. Liu, M. Watterson, K. Mohta, K. Sun, S. Bhattacharya, C. J.
                                                                                  Taylor, and V. Kumar, “Planning dynamically feasible trajectories for
   Despite these strengths, some limitations remain to be                         quadrotors using safe flight corridors in 3-d complex environments,”
addressed in the future. The convex hull selection is not                         IEEE Robotics and Automation Letters, vol. 2, no. 3, pp. 1688–1695,
exhaustive, and our 3D convex decomposition module gener-                         2017.
                                                                             [17] J. Tordesillas, B. T. Lopez, M. Everett, and J. P. How, “Faster: Fast
ates axis-aligned cuboids; a more general method is needed                        and safe trajectory planner for navigation in unknown environments,”
to handle more complex scenarios. Our algorithm is greedy                         IEEE Transactions on Robotics, vol. 38, no. 2, pp. 922–938, 2021.
in choosing the current placement without looking ahead to                   [18] T. Marcucci, M. Petersen, D. von Wrangel, and R. Tedrake, “Motion
                                                                                  planning around obstacles with convex optimization,” Science robotics,
the future. The objective functions/heuristics for each object                    vol. 8, no. 84, p. eadf7843, 2023.
are predefined, and it is interesting to combine tree search                 [19] Z. Yang, J. Mao, Y. Du, J. Wu, J. B. Tenenbaum, T. Lozano-Pérez,
and backtracking over different combinations of heuristics as                     and L. P. Kaelbling, “Compositional Diffusion-Based Continuous
                                                                                  Constraint Solvers,” in Conference on Robot Learning, 2023.
in [28], [29].                                                               [20] W. Shen, C. Garrett, N. Kumar, A. Goyal, T. Hermans, L. P. Kaelbling,
                                                                                  T. Lozano-Pérez, and F. Ramos, “Differentiable gpu-parallelized task
                    ACKNOWLEDGMENT                                                and motion planning,” in Robotics: Science and Systems, 2025.
                                                                             [21] L. Chen, S. R. Iyer, and Z. Kingston, “Differentiable parti-
  This project has received funding from the European                             cle optimization for fast sequential manipulation,” arXiv preprint
Union’s Horizon Europe programme under Grant Agreement                            arXiv:2510.07674, 2025.
                                                                             [22] D. J. VandenHeuvel, “DelaunayTriangulation.jl: A Julia package for
No. 101120823, project MANiBOT.                                                   Delaunay triangulations and Voronoi tessellations in the plane,” Jour-
                                                                                  nal of Open Source Software, vol. 9, no. 101, p. 7174, Sep. 2024.
                            R EFERENCES                                      [23] S. C. Nandy and B. B. Bhattacharya, “Maximal empty cuboids among
                                                                                  points and blocks,” Computers & Mathematics with Applications,
 [1] F. Wang and K. Hauser, “Stable bin packing of non-convex 3d                  vol. 36, no. 3, pp. 11–20, 1998.
     objects with a robot manipulator,” in IEEE International Conference     [24] J. Nocedal and S. J. Wright, Numerical optimization. Springer, 2006.
     on Robotics and Automation, 2019, pp. 8698–8704.                        [25] J. Chen and J. Revels, “Robust benchmarking in noisy environments,”
 [2] H. Zhao, Q. She, C. Zhu, Y. Yang, and K. Xu, “Online 3d bin packing          arXiv preprint arXiv:1608.04295, 2016.
     with constrained deep reinforcement learning,” in Proceedings of the    [26] J. Revels, M. Lubin, and T. Papamarkou, “Forward-mode automatic
     AAAI Conference on Artificial Intelligence, vol. 35, no. 1, 2021, pp.        differentiation in Julia,” arXiv:1607.07892 [cs.MS], 2016.
     741–749.                                                                [27] I. A. Sucan, M. Moll, and L. E. Kavraki, “The open motion planning
 [3] N. Funk, G. Chalvatzaki, B. Belousov, and J. Peters, “Learn2assemble         library,” IEEE Robotics & Automation Magazine, vol. 19, no. 4, pp.
     with structured representations and search for robotic architectural         72–82, 2012.
     construction,” in Conference on Robot Learning, 2022.                   [28] M. Toussaint and M. Lopes, “Multi-bound tree search for logic-
 [4] H. Zhao, Z. Pan, Y. Yu, and K. Xu, “Learning physically realizable           geometric programming in cooperative manipulation domains,” in
     skills for online packing of general 3d shapes,” ACM Transactions on         IEEE International Conference on Robotics and Automation, 2017,
     Graphics, vol. 42, no. 5, pp. 1–21, 2023.                                    pp. 4044–4051.
 [5] S. Yang, S. Song, S. Chu, R. Song, J. Cheng, Y. Li, and W. Zhang,       [29] D. Silver, T. Hubert, J. Schrittwieser, I. Antonoglou, M. Lai, A. Guez,
     “Heuristics integrated deep reinforcement learning for online 3d bin         M. Lanctot, L. Sifre, D. Kumaran, T. Graepel et al., “A general
     packing,” IEEE Transactions on Automation Science and Engineering,           reinforcement learning algorithm that masters chess, shogi, and go
     vol. 21, no. 1, pp. 939–950, 2023.                                           through self-play,” Science, vol. 362, no. 6419, pp. 1140–1144, 2018.
 [6] H. Zhao, Y. Yu, and K. Xu, “Learning efficient online 3d bin
     packing on packing configuration trees,” in International conference
     on learning representations, 2021.
