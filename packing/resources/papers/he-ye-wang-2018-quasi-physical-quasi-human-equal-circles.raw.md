                                          An Efficient Quasi-physical Quasi-human Algorithm for Packing
                                                        Equal Circles in a Circular Container

                                                                     Kun He, Hui Ye1 , Zhengli Wang2a , Jingfa Liub
                                                 a School of Computer Science, Huazhong University of Science and Technology, Wuhan 430074, China
                                          b School of Computer & Software, Nanjing University of Information Science & Technology, Nanjing 210044, China
arXiv:1611.02323v2 [cs.CG] 13 Apr 2017




                                         Abstract
                                         This paper addresses the equal circle packing problem, and proposes an efficient Quasi-physical
                                         Quasi-human (QPQH) algorithm. QPQH is based on a modified Broyden-Fletcher-Goldfarb-
                                         Shanno (BFGS) algorithm which we call the local BFGS and a new basin hopping strategy based
                                         on a Chinese idiom: alternate tension with relaxation. Starting from a random initial layout, we
                                         apply the local BFGS algorithm to reach a local minimum layout. The local BFGS algorithm
                                         fully utilizes the neighborhood information of each circle to considerably speed up the running
                                         time of the gradient descent process, and the efficiency is very apparent for large scale instances.
                                         When yielding a local minimum layout, the new basin-hopping strategy is to shrink the container
                                         size to different extent to generate several new layouts. Experimental results indicate that the new
                                         basin-hopping strategy is very efficient, especially for a type of layout with comparatively dense
                                         packing in the center and comparatively sparse packing around the boundary of the container.
                                         We test QPQH on the instances of n = 1, 2, · · · , 320, and obtain 66 new layouts which have
                                         smaller container sizes than the current best-known results reported in literature.
                                         Keywords: Circle packing, neighborhood structure, container shrinking strategy,
                                         quasi-physical, quasi-human


                                         1. Introduction
                                              The circle packing problem (CPP) is concerned with arranging n circles in a container with
                                         no overlap, which is of great interest to the industry and academia. CPP is encountered in a
                                         variety of real world applications, including apparel, naval, automobile, aerospace and facility
                                         layout (Castillo et al., 2008). CPP has been proven to be NP-hard (Demaine et al., 2010), and
                                         it is difficult to find an exact solution in polynomial time even for some specific instances. Re-
                                         searchers resort to heuristic methods that fall into two categories: the construction method and
                                         the optimization method.
                                              The construction method can be described as packing circles one by one using some spe-
                                         cific rules. There is one type of rules that fixes the container radius and only concerns where to
                                         feasibly place the circles in the container. Algorithms include Max Hole Degree (MHD) algo-
                                         rithm (Huang et al., 2003), self look-ahead search strategy (Huang et al., 2005, 2006), Pruned-
                                         Enriched-Rosenbluth Method (PERM) (Lü and Huang, 2008), and beam search algorithm (Akeb

                                            1 Corresponding author. Email:yehui20080414@gmail.com
                                            2 Corresponding author. Email:498195342@qq.com

                                         Preprint submitted to Computers and Operations Research                                          August 22, 2018
et al., 2009). The other type of rules adjusts the container radius along with the construction
procedure. Algorithms include the Best Local Position (BLP) series (Hifi and M’Hallah, 2004;
Hifi and MHallah, 2006, 2007; Akeb and Hifi, 2010), and hybrid beam search looking-ahead
algorithm (Akeb and Hifi, 2010).
     Different to the construction method, the optimization method doesn’t directly obtain a good
solution, but iteratively improve the solution based on an ordinary initial solution. The great
variety of optimization method can be further classified into quasi-physical, quasi-human algo-
rithm (Wang et al., 2002; Liu et al., 2016), Tabu search and simulated annealing hybrid approach
(Zhang and Deng, 2005), population basin hopping algorithm (Addis et al., 2008b), simulated
annealing algorithm (Mller et al., 2009), formulation space search algorithm (Lopez and Beasley,
2013), iterated local search algorithm (Fu et al., 2013; Ye et al., 2013; Liu et al., 2009, 2015), etc.
In 2015, there are two new algorithms published that yield excellent results: iterated Tabu search
and variable neighborhood descent algorithm (Zeng et al., 2015) and evolutionary computation-
based method (Flores et al., 2015).
     We address the classic CPP, the Equal Circle Packing Problem (ECPP). In this section, we
first recall mathematical methods for ECPP, which are the basis of researching ECPP. Then we
concentrate on heuristics for ECPP, which are more effective for large scale ECPP. We summarize
our work finally.

1.1. Mathematical methods for ECPP
     As a classical type of CPP, ECPP is still difficult in the field of mathematics. In the early
stage of the study, the value of n is relatively small, and researchers used mathematical analysis
to not only find the optimal layout but also provide proofs on the optimality. Kravitz (1967), the
first scholar working on ECPP, gave the layout for n = 2, 3, · · · , 19 with the container radius, but
he provided no proof of optimality. Graham (1968) proved the optimality for n = 2, 3, 4, 5, 6, 7.
Pirl (1969) proved the optimality for n = 2, 3, 4, 5, 6, 7, 8, 9, 10, and provided the layout for
n = 11, 12, · · · , 19 at the same time. Goldberg (1971) improved the layout for n = 14, 16, 17
that Pirl provided, and Goldberg also provided the layout for n = 20 for the first time. Reis
(1975) improved the layout for n = 17 based on Pirl’s research, and he first gave the layout for
n = 21, 22, 23, 24, 25. Melissen (1994) proved the layout configuration optimality for n = 11,
and Fodor (1999, 2000, 2003) proved the optimality for n = 12, 13, 19. To summed up, only the
optimality for n = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 19 has been proved so far.

1.2. Heuristics for ECPP
    Heuristics demonstrate their high effectiveness on ECPP. In this subsection, we introduce
landmark heuristics for ECPP, and two key issues for solving ECPP.

1.2.1. Landmark heuristics
    When n is relatively large, it is very difficult to find the optimal layout and prove the opti-
mality. Heuristic algorithms for ECPP can be very efficient to find optimal or suboptimal lay-
outs. Although heuristics may not guarantee the theoretical optimality, they can find some layout
where the container radius is very close to the theoretical minimum.
    Graham et al. (1998) did some early work and proposed two heuristic methods. The first
method is to simulate the repulsion m    forces. It transforms ECPP to a problem of finding the
                              λ
                                                S 1 , S 2 , · · · , S n correspond to the coordinates for the
             P
minimum on 1≤i≤ j≤n                     , where
                        kS i −S j k2
                                                     2
set of circle centers in the container, S i − S j ≥ 2, λ the zoom factor, and m a large positive
integer. For such objective function, we can use some existing methods such as gradient descent
to find a layout with the local minimum value. The second method is the billiards simulation.
This is a quasi-physical method that regards the circle items as billiards. This algorithm starts
with a small billiard radius and randomly assigns an initial movement direction for each billiard.
Then a series of collision motion occurs in the circular container. During the process movement,
the authors slowly increase the sizes of the billiards. By repeatedly running the algorithm, it is
possible to find the global optimal solution. By the comprehensive use of repulsion forces and
billiards simulation, Graham found the near-optimal layout for n = 25, 26, · · · , 65.
     There are many followup work based on heuristics. Here we highlight several landmark
works. Akiyama et al. (2003) used a greedy method to find local optimal solution. Their algo-
rithm continuously improves the current layout by randomly moving one circle until the moving
reaches an iteration limit (e.g. 300000). By repeatedly running the greedy method, Akiyama
found much denser layouts for n = 70, 73, 75, 77, 78, 79, 80. Grosso et al. (2010) assumed that
ECPP has the characteristic of “funneling landscape”, and used a monotone hopping strategy to
look for the “funnel bottom”. In order to solve the funnel problem, they used the population
hopping strategy to enhance the diversity of the layout. They found a number of denser layout
schemes for 66 ≤ n ≤ 100. Huang and Ye (2011) proposed a global optimization algorithm using
a quasi physical model. They proposed two new quasi physical strategies and found 63 denser
layouts among the 200 instances for n = 1, 2, · · · , 199, 200.

1.2.2. Two key issues
    There are two key issues to solve the ECPP. First, how can we optimize a random or given
layout so that it is more likely to reach the local optimum layout. Second, when we reach a
local optimal layout which is not feasible, that is, there exists overlapping among some circles,
we need to use some strategy to jump out of the local minimum layout and reach a new layout
that inherits the advantages of the previous local optimum. Then we could continue the local
optimization to reach another local minimum, and we aim to eventually obtain an optimal or
near-optimal layout.
    For the local optimization method, the repulsion forces and billiards simulation of Graham
et al. (1998), the monotone hopping strategy of Grosso et al. (2010), and the elastic force move-
ment of Huang and Ye (2011) described above all fall into this category. There are also other good
methods, like TAMSASS-PECS method (Szabó et al., 2005), nonlinear optimization method
(Birgin et al., 2005) and reformulation descent algorithm (Mladenović et al., 2005). Each of
these algorithms has its own advantages, depending on the number of circles and the container
shapes (square, circle, rectangle, or polygon).
    There are diverse methods for the Basin-hopping strategy. For example, the small random
perturbation method (Addis et al., 2008a) formed a new layout by moving several circles in the
local optimal layout to some random places. However, due to purely randomness, this method
may destroy the holistic heredity. Huang and Ye (2011) considered three kinds of forces, elastic
force, attractive force and repulsive force, to promote the entire layout to a new form. They used
three parameters c1 , c2 and steps to control the strength of the attractive force, the strength of
the repulsive force and the duration time of the abrupt movement. Zeng et al. (2015) proposed
another strategy for moving random circles to vacant places in the container. By dividing the
entire container into square grids, Zeng et al. regarded the vacant point with large vacant degree
as candidate insertion place for the center of the “jumping circle”, which can improve the current
layout to a certain extent.
                                                  3
1.3. Our work
    We propose an efficient Quasi-physical Quasi-human (QPQH) algorithm for solving ECPP.
We adopted the physical model (Huang and Ye, 2011) popularly used for solving CPP. And
through the establishment of the physical model, we look for a minimum of the objective func-
tion using the classical Quasi-Newton method, the Broyden-Fletcher-Goldfarb-Shanno (BFGS)
algorithm (Liu and Nocedal, 1989). To speed up the computation without losing much accuracy,
we fully utilize the neighborhood structure of the circles, and propose a local BFGS algorithm.
We also propose a new Basin-hopping strategy by shrinking the radius of the container. In the
proposed QPQH, we iteratively apply the local BFGS algorithm to achieve a new layout after
a certain number of continuous optimization iterations, and apply the Basin-hopping strategy
to jump out of the local minimum. Experiments on 320 (n = 1, 2, · · · , 320) ECPP instances
demonstrate the effectiveness of the proposed method.


2. Problem Formulation

    The Equal Circle Packing Problem (ECPP) can be described as packing n unit circle items
into a circular container. We need to ensure no overlap between any two circles and the radius
of the container, R, is minimized. By setting a Cartesian coordinate system with its origin (0,0)
located at the container center, as shown in Figure 1, and denoting the coordinate for the center of
circle i (i = 1, 2, · · · , n) as (xi , yi ), we want to find a layout configuration X = (x1 , y1 , · · · , xn , yn )
such that the container’s radius is minimized.

                            minimize         R
                                                       q
                                   s.t.      (1)           xi2 + y2i ≤ R − 1
                                                       q
                                             (2)           (xi − x j )2 + (yi − y j )2 ≥ 2

where i, j = 1, 2, · · · , n and i , j.


3. Algorithm Description

     Finding the minimum radius R of the container is an optimization problem. As R is unknown,
it is difficult to directly find the minimum R. We can transform the problem into a decision
problem, that is, for a fixed R, whether we can find a layout to meet the above conditions (1) and
(2). If the response is “yes”, then we will continue reduce the value of R, until we can not find
any feasible layout on a smaller R.
     This section describes in detail the algorithm we proposed. We first introduce a popular
physical model for solving this problem, and give a brief introduction to the local search algo-
rithm, the classic BFGS algorithm. Then, we propose the local BFGS algorithm, for each circle
we form an adjacency list to record the current overlapping circles as well as possible overlap-
ping circles in the near future. Next, we propose a new basin-hopping strategy, and the global
search algorithm combining the local BFGS algorithm and the basin-hopping strategy. And we
introduce a post-processing procedure, the container adjustment procedure, to yield a container
radius as small as possible while maintaining feasibility. Finally, we add an overall pseudo-code
integrating all sub-algorithms in QPQH.

                                                         4
                                                               (xj,yj)
                                                            (xj,yj)
                                         (xi,yi)
                                          (xi,yi)




                                      Figure 1: The coordinate system.


3.1. Physical model
    Similar to previous quasi-physical methods (Ye et al., 2013; Huang and Zhan, 1982; He
et al., 2013, 2015), we regard the circle items as elastic items and imagine the container as a rigid
circular container. If an elastic object embeds itself in another object, it will be deformed and the
deformation will cause some elastic potential energy. Based on the Cartesian coordinate system,
we have the following definitions.
Definition 1 (Overlapping Depth). There are two kinds of overlaps, item-item overlap and item-
container overlap. The overlapping depth between item i and the container is doi .
                                              q
                                   doi = max( xi2 + y2i + 1 − R, 0)                               (1)
    And the overlapping depth between item i and item j (i , j) is di j .
                                         q
                          di j = max(2 − (xi − x j )2 + (yi − y j )2 , 0)                         (2)
Definition 2 (Elastic Energy). According to the elastic mechanics, the elastic potential energy
between two smoothy elastic objects is proportional to the square of the embedded depth. The
elastic energy between item i and j ( j , i) is defined as following, where item 0 indicates the
hollow object of the container.
                                                    Ui j = di2j                                   (3)
And the elastic energy Ui of item i is defined as:
                                                        n
                                                        X
                                             Ui =                 Ui j                            (4)
                                                       j=0, j,i

The total elastic energy U(X) for the whole system X = {x1 , y1 , ..., xn , yn } is defined as:
                                                        n
                                                        X
                                                U=              Ui                                (5)
                                                         i=1
                                                        5
3.2. The BFGS continuous optimization algorithm
    With the physical model established, the potential energy function U(X) is defined and it has
the following properties:
    (1) For all X ∈ (−∞, +∞)n , U(X) ≥ 0;
    (2) X is a feasible packing layout if and only if U(X) = 0.
    Thus, the packing problem is transformed into the optimization problem of finding the mini-
mum value on function U(X). We use the classical Quasi-Newton method, the BFGS algorithm,
for the continuous optimization of finding local minimums.
    The basic idea of the BFGS algorithm is as follows. From a layout configuration Xk , we
construct an approximate Hessian matrix Hk using information of the objective function U and
the gradient gk . Thus we can get a search direction dk and a search length λk , and generate a new
layout configuration Xk+1 . We continue the process iteratively until reaching a minimum layout
configuration.
    The gradient gk is defined by Eq. (6), and the search step length λk is defined by Eq. (7). λk
is a positive real number in order to reach the minimum value of the elastic energy U at step k.
Xk corresponds to a 2n − coordinate vector, and dk , defined by Eq. (9), is the search direction at
step k
                                                                  !
                                       dUk dUk           dUk dUk
                                 gk =       ,     ,··· ,    ,                                    (6)
                                        dx1 dy1          dxn dyn
                                 λk = arg min+ U(xk + λdk )                                        (7)
                                          λ∈R

    Hessian matrix is a symmetric matrix composed of the second derivatives of U(Xk ), and H
is an approximate Hessian matrix of size 2n by 2n. It is updated by Eq. (8), where I is the unit
matrix, sk is the change quantity of Xk , and yk is the change quantity of gk . The pseudo code of
the BFGS algorithm is described in Algorithm 1.

                                           sk yTk   yk sTk  sk sTk
                                                                
                            Hk+1 = I − T  Hk I − T  + T
                                    
                                                                                               (8)
                                          yk sk           yk sk      yk sk


                                           dk = −Hk ∗ gk                                           (9)


3.3. The local BFGS algorithm
     In the BFGS algorithm, when we use Eq. (5) and Eq. (6) to calculate U and gk , for each
circle i, we need to calculate its distance to each of the other n − 1 circles in order to judge
whether there exist some overlaps. In the actual procedure, however, a circle usually intersects
with approximately six other circles when there exist only slight overlaps. Ideally, if three equal
circles are tangent to each other, the three lines connecting the pairwise circle centers construct
an equilateral triangle. The angle between two lines is 60 degrees. As the maximum degree of
the central angle in a circle is 360 degree. So there are at most six other circles tangent to a circle
if there exists no overlap.
     As illustrated in Figure 2, there will be tiny changes for the adjacency relationship of the
circles after certain iterations of the BFGS algorithm. So during the calculation procedure, for
each circle in the system, we record its overlapping circles at present and possible overlapping
                                                  6
Algorithm 1 The BFGS algorithm(X, R)
INPUT:
    An initial layout (X, R)
OUTPUT:
    A locally optimal packing layout (X ∗ )
 1: H0 ← I; //H0 is the initial approximate Hessian matrix, and I is the unit matrix
 2: k ← 0; //k is the iteration step
 3: while k ≤ MaxIterations do
 4:    calculate the gradient gk by Eq. (6);
 5:    calculate the search direction dk ← −Hk ∗ gk ;
 6:    calculate the search step length λk by Eq. (7);
 7:    sk ← λk ∗ dk , Xk+1 ← Xk + sk ;
 8:    if U < 10−20 or kgk k < 10−10 then
 9:       return the current layout (X ∗ );
10:    end if
11:    yk ← gk+1 − gk ;  
                     s yT          y sT     s sT
                                       
12:    Hk+1 ← I − ykT sk Hk I − ykT sk + ykT sk ;
                      k k           k k      k k
13:   k ← k + 1;
14: end while



circles in the near future in an adjacency list. Specifically, for a circle i located at (xi , yi ), the
container is regarded as an adjacency object if Eq. (10) holds; for a circle j located at (x j , y j ) is
regarded as an adjacency object if Eq. (11) holds. We set d1 = 1, d2 = 1, which means an object
(circle or container) is considered as adjacent if the distance from its boundary to the boundary
of the current circle is no greater than 1, as illustrated in Figure 3.
                                  q
                                     xi2 + y2i + 1 − R ≤ d1                                         (10)
                                  q
                                     (xi − x j )2 + (yi − y j )2 − 2 ≤ d2                           (11)

     We only check the overlapping status for circles in the adjacency list in the local BFGS
algorithm. And we will update the adjacency list for each circle after running the local BFGS for
l iterations. If l is too large, then there could be some big error for the overlapping approximation.
If l is too small, then we need to frequently recalculate the distance for all other circles for each
circle and could not really speed up the BFGS optimization. We set l = 10 as a tradeoff selection.
     We experimentally test the effectiveness of the local BFGS algorithm on 20 instances, n =
10, 20, · · · , 200. We set the radius of the container as the current known minimum radius, and
record the time starting from a random initial layout to a local minimum layout. We calculate
each instance for 1000 times, record the average running time T of reaching the local minimum,
and compare with the original BFGS algorithm. The comparison result is shown in Figure 4.
With the increasement on the scale n, the average time T of the two methods both increases.
However, the running time of the BFGS algorithm increases much faster. In the case of n = 200,
the value T of the BFGS algorithm is about 4 times as compared with the value T of the local
BFGS algorithm.
     When using Eq. (5) to compute U and Eq. (6) to compute gk , we only consider the adjacency
circles, the time complexity reduces from O(N 2 ) to O(N). But the total complexity is still O(N 2 ),
as we need to update the approximate Hessian matrix which is in n by n scale. Nevertherless,
                                                      7
                                Figure 2: The local minimum layout when n = 31.




                                                (xi,yi)             (xj,yj)




                                         d1
                                                              d2
         Figure 3: Distance d1 between circle i and the container, and distance d2 between circles i and j.


the computational efficiency shows great improvement for the local optimization, especially for
relatively large instances (such as n ≥ 200), as shown in Figure 4.

3.4. Basin-hopping procedure
    When reaching a local minimum by the local BFGS, we shrink the container radius as the
Basin-hopping strategy. We fix the original coordinate of each circle and reduce the container
radius by a factor of β (0 < β < 1): R0 = βR0 . β is defined as β = 0.3 + 0.035m and m varies
from 0, 1, 2, to 19 such that β varies from 0.30 to 0.965 to generate diverse layouts. 0.3 is just
an empirical setting and 0.035 = 0.7 20 . Other alternative setting also works. For instance, if you
choose the shrinking ratio to start from 0.4 and want to generate 20 new layouts, then you should
set β = 0.4 + 0.03m as 0.03 = 0.6
                                20 , and R shrinks from 0.4R to 0.97R.
    We then run the local BFGS algorithm for h iterations (h is a random number ranging from
50 to 100) to reach a new layout. Figure 5 represents the layout before and after the Basin-
                                                          8
                                                                                                                    modified
                                                                                                                    Local BFGSBFGS method
                                                                     12                                             BFGS
                                                                                                                     BFGS method




                                                              T(s)
                                                                     11

                                                                     10




                                              cal miniminina,
                                                      na T(s)
                                                                     9

                                                                     8

                                                                     7
                                          f lolocal                  6

                                                                     5
                                     tim oof


                                                                     4
                             Averagetime




                                                                     3
                           Average



                                                                     2

                                                                     1

                                                                     0

                                                                     -1
                                                                          0   20   40   60     80       100   120   140   160   180   200

                                                                                             Number  ofdisks
                                                                                              Number of circles
                Figure 4: Improvement on the average minimum time of the local BFGS method.


hopping procedure. The pseudo-code of the Basin-hopping procedure is shown in Algorithm 2.
We reduce the container radius R0 to βR0 , and run the local BFGS for h iterations regarding the
current minimum layout as an initial layout. In this way, we have 20 new layouts as the basin
hopping results.




                Figure 5: The layout before and after the Basin-hopping procedure for n = 130.

     We experimentally test the effectiveness of the Basin-hopping procedure. We test the in-
stances for n = 50, 51, · · · , 70 to compare the Basin-hopping procedure with random initial-
ization method. The radius of the container is set as the current known minimum radius. We
compare the number of iterative steps needed to find a feasible layout using the local BFGS
algorithm.
     The calculation results are shown in Figure 6. It shows that, the Basin-hopping procedure is
apparently better in the cases of n = 53, 54, 55, 66, 67, 68, 69; In the case of n = 70, the random
initial method is better. In other cases, the effectiveness of two methods are almost the same. On
the average, the shrinking strategy exhibits better performance.
     In the shrinking Basin-hopping procedure, the container’s radius decreases dramatically. Af-
ter several iterations using the local BFGS algorithm, all circles contract to the container center.
Then we recover the container radius and there exists a large vacant space in the outer layer of
                                                                                                    9
Algorithm 2 Basin-hopping procedure(X, R)
INPUT:
    A local minimum layout (X, R)
OUTPUT:
    20 new layouts.
 1: R0 ← R;
 2: for m ← 0 to 19 do
 3:    β ← 0.3 + 0.035m;
 4:    R ← βR0 ;
 5:    h ←a random integer in [50, 100];
 6:    run the local BFGS (X, R) for h iterations to reach a new layout Xm ;
 7: end for
 8: return the 20 new layouts (Xm )(m = 0, 1, · · · , 19).


                                                                                                                               Muti-start method
                                                                                                                               Basin-hopping method
                                                                              30000
                         Average local minima per hit of best-known packing




                                                                              20000




                                                                              10000




                                                                                  0




                                                                                      48   50   52   54   56    58   60   62     64   66   68   70   72
                                                                                                               Number of disks
       Figure 6: Comparison of the shrinking Basin-hopping procedure with random the initialization method.


the container. In the iterative process of the local BFGS, all circles move outwards as a whole.
While the outer space is large and the inner space is small, the result of the final movement is
that inner circles are dense and outer circles are sparse. Therefore, the Basin-hopping procedure
has better influence for instances with dense inner packing and sparse outer packing, which are
the most cases for the near-optimal or dense packing. We show two typical examples with the
above characteristics in Figure 7.




                                                                                                               10
                        Figure 7: The resulting minimum layouts for n = 53 and n = 68.


    Combining the local BFGS algorithm with the Basin-hopping procedure, we present the
global search algorithm in Algorithm 3. We first run the local BFGS with a random initial layout
X. When reaching a local minimum layout, we run the Basin-hopping procedure with the local
minimum layout to generate 20 new layouts. Then we run the local BFGS on the 20 new layouts
respectively. The algorithm will terminate once it finds a feasible layout. If none of the 20
new layouts becomes feasible, we will randomly generate an initial layout again and repeat the
calculation until a time limit t0 is reached.

Algorithm 3 The global search algorithm
INPUT:
    A container radius R
OUTPUT:
    A feasible or stuck layout (X, R)
 1: while U > 10−20 and the timeout limit t0 is not reached do
 2:    randomly generate an initial layout X;
 3:    run the local BFGS algorithm(X, R);
 4:    if U < 10−20 then
 5:       break;
 6:    end if
 7:    run Basin-hopping (X, R) to generate 20 new layouts and store them in array C;
 8:    for i = 1 to 20 do
 9:       run the local BFGS algorithm(C[i], R);
10:       if U < 10−20 then
11:          break;
12:       end if
13:    end for
14: end while
15: return the current layout(X, R).




3.5. The container adjustment procedure
    In the global search algorithm, for the new layout after the Basin-hopping, the radius and lo-
cation of the container are constant, and circles are centralized around the center of the container.
We then continue the optimization with the local BFGS algorithm and hopefully to reach a feasi-
ble layout. During this procedure, viewing from the layout picture, most circles are moving from
the container’s center to the border. If the termination condition U < 10−20 is satisfied while the
                                                     11
circles haven’t been tangent to the border of the container, it is obviously that the radius of the
container can be reduced until the circles are tangent to the border of the container. So as a post
processing, we use the container adjustment strategy to decrease the radius of the container.
    If the global search algorithm returns a feasible layout, we hope to maintain the relative
locations of the circles and further decrease the radius of the container to get a more compact
layout. Here we use the dichotomy method to find the minimal radius Rmin of the container from
the current layout. We update Rbestknown to Rmin , and use the global search algorithm for a new
round of search.

Algorithm 4 Container adjustment algorithm
INPUT:
    Current best minimum layout (X, R)
OUTPUT:
    New feasible layout (X, Rmin )
 1: R0 ← R;
 2: i ← −1;
 3: repeat
 4:    Rupperbound ← R0 ;
 5:    i ← i + 1;
 6:    R0 ← Rupperbound − 10−10 × 10i ;
 7:    run the local BFGS algorithm(X, R0 );
 8: until (X0 , R) is not feasible;
 9: Rlowerbound ← R0 ;
10: repeat
11:    Rmin ← (Rupperbound + Rlowerbound )/2;
12:    run the local BFGS algorithm(X,Rmin );
13:    if (X, Rmin ) is feasible then
14:        Rupperbound ← Rmin ;
15:    else
16:        Rlowerbound ← Rmin ;
17:    end if
18: until |Rupperbound − Rlowerbound | <= 10−10 ;
19: return the current feasible layout (X, Rmin ).


    For the instance of n = 130, Rbestknown = 12.6023189367. The global search algorithm finds
the global minimum layout, as shown at the left of Figure 8. After the container adjustment
procedure, the container radius is changed to Rmin = 12.6017746136, which is reduced by about
6 × 10−4 , as shown at the right of Figure 8.

3.6. The Efficient Quasi-physical Quasi-human (QPQH) Algorithm
    We add a general pseudo-code integrating all algorithms for QPQH. For the initialization,
we set R the current known minimum radius. Then we do the following iterations until reaching
a time limit t1 or R is not improved at the last iteration. At each iteration, we first call the
Global Search Algorithm GSA(R); if GSA returns a feasible layout X, then we call the Container
Adjustment Algorithm CAA(X, R) and wish it output a smaller R with a new feasible layout X.
The pseudo-code of QPQH is shown in Algorithm 5.


                                                     12
              Figure 8: The layout before and after the container adjustment procedure for n = 130.

Algorithm 5 The efficient Quasi-physical Quasi-human algorithm
INPUT:
    the current known minimum container radius Rbestknown
OUTPUT:
    The feasible minimum layout (X, R) or NULL.
 1: R ← Rbestknown ;
 2: Rbest ← 0;
 3: while the time limit t1 is not reached do
 4:    X ← GS A(R);
 5:    if X is feasible then
 6:       R0 ← R;
 7:       (X, R) ← CAA(X, R);
 8:       if R = R0 then
 9:           return the current layout (X, R);
10:       end if
11:       if R < R0 then
12:           Xbest ← X;
13:           Rbest ← R;
14:       end if
15:    end if
16: end while
17: if Rbest > 0 then
18:    return the best layout (Xbest , Rbest );
19: end if
20: return NULL.



4. Experimental Results

    In this section, we introduce the experimental environment, the key parameter tuning, the
experimental instances and results. The experimental results are divided into two parts. One is
for the first 100 cases, whether QPQH can always stably find the current best-known layouts. The
other is for n ≤ 320 we compare the best finding of QPQH to the current best-known layouts.


                                                      13
4.1. Experimental setup and parameter tuning
    We implement QPQH in the C++ programming language, and the IDE is Visual C++ 6.0.
We run QPQH on the Ali cloud platform (http://www.aliyun.com). The platform has an 8 core
processor and an 8GB memory. The OS is Windows Server 2012, and the experiment is com-
pleted without any parallelism technique.
    For the key parameters in the algorithm, we pick several candidate sets of values, and did a
small trial of experiments to determine the suitable setting. For example for l in the local BFGS
algorithm, we set n = 100, 150 or 200, fix the radius to the current-best-known, and run the local
BFGS algorithm for 1000 times to reach a local minima. The average potential energy and the
convergence time are as shown in Figure 9. We could see that the proposed algorithm is not very
sensitive to the parameter l as the fluctuation is very small. We choose l = 10 as it has a slightly
shorter convergence time and slightly better average potential energy.




Figure 9: Comparation of the average performance and the convergence time on different values of parameter l for
n = 100, 150, 200.



4.2. Computational efficiency and robustness
     The first set of experiments is to test whether the algorithm can robustly find the current best-
known layout. For the first 100 instances (n = 1, 2, · · · , 100), the radius of the container is set to
the current known minimum (downloaded from the official website http://www.packomania.com,
20 June 2016). We randomly locate n circles in the container and then call the local BFGS
algorithm. Then we get 20 new layouts for the next iteration. Once the program finds a feasible
layout or the running time is more than 4 hours, the calculation will terminate. In order to verify
the robustness of the proposed algorithm, each instance is calculated for 10 times.
     The results show that for the 100 instances (n = 1, 2, · · · , 100), except n = 82, 100, QPQH
finds 98 current best-known layouts. For n ≤ 49, the algorithm can always stably find the current
best-known layout. In these 49 instances, the average computation time is at most 720s.
     The corresponding statistics for n = 50, 51, · · · , 100 are as shown in Table 1. The first column
is the number of circles. The second column corresponds to the current known minimum radius
of the container. The third column is the hit count among the 10 times of calculation, i.e., the
number of feasible layouts found by the Global Search Algorithm (GSA) within 4 hours. And
the forth column is the average computation time in seconds.




                                                      14
               n      Rbestknown     Hit Count   Time (s)     n        Rbestknown     Hit Count   Time (s)
              50    7.9475152747      10/10           34     76      9.7295968021      10/10          464
              51    8.0275069524      10/10           21     77      9.7989119245      10/10          147
              52    8.0847171906      10/10             6    78      9.8577098998       3/10         4276
              53    8.1795828268      10/10         1043     79      9.9050634676      10/10         5464
              54    8.2039823834      10/10           33     80      9.9681518131       5/10         5145
              55    8.2111025509      10/10           27     81     10.0108642412       7/10         5446
              56    8.3835299225      10/10           21     82     10.0508242234       0/10             -
              57    8.4471846534      10/10             7    83     10.1168578751       7/10         4821
              58    8.5245537701      10/10           71     84     10.1495308672       8/10         5364
              59    8.5924999593      10/10           67     85     10.1631114658      10/10          377
              60    8.6462198454      10/10           13     86     10.2987010531       2/10         5867
              61    8.6612975755      10/10             4    87     10.3632085050      10/10         1148
              62    8.8297654089      10/10          861     88     10.4323376927      10/10         4866
              63    8.8923515375      10/10           92     89     10.5004918145       5/10         7751
              64    8.9619711084      10/10         2872     90     10.5460691779      10/10          588
              65    9.0173973232      10/10           34     91     10.5667722335      10/10           40
              66    9.0962794269      10/10         2404     92     10.6846458479       4/10         4992
              67    9.1689718817      10/10         7492     93     10.7333526002       3/10         6092
              68    9.2297737467      10/10         3252     94     10.7780321602       8/10         5552
              69    9.2697612666      10/10          713     95     10.8402050215       5/10         6056
              70    9.3456531940      10/10         1752     96     10.8832027597       4/10         5824
              71    9.4157968968      10/10          916     97     10.9385901100       1/10        11540
              72    9.4738908567      10/10          113     98     10.9793831282       9/10         2593
              73    9.5403461521       2/10         5571     99     11.0331411514       9/10         3445
              74    9.5892327643       6/10         5343     100    11.0821497243       0/10             -
              75    9.6720296319       8/10         6671

  Table 1: The bestknown container radius, hit count and average running time for 10 rounds on n = 50, 51, · · · , 100.


    The second set of experiments is to test whether QPQH can find a better layout than the
current best. For the first 320 instances (n = 1, 2, · · · , 320), the radius of the container is set
to the current known minimum (downloaded from official website http://www.packomania.com,
20 June 2016). We randomly locate n circles in the container and run GSA (the time limit t0 is
4 hours). Once we find the minimum layout, we apply the container adjustment procedure to
decrease the radius of the container, and run QPQH again, until we can not reduce the container
size within the time limit t1 which is generally set to 3 days.
    The results show that for 66 of the 320 instances, QPQH finds better layouts than the current
best. Table 2 shows the specific improvements. In Table 2, R0 is the current known minimum
container radius, R∗ is the container radius obtained by QPQH, and R0 − R∗ is the improvement
degree. The improvements are in the range of 10−7 to 10−2 , and most improvements are 10−3 or
10−4 .
    Figure 9 further illustrates some new and better layouts obtained by QPQH.




                                                            15
(a) n = 126                                              (b) n = 128




(c) n = 130                                              (d) n = 137




(e) n = 138                                              (f) n = 140
Figure 10: New and better layouts abtained by QPQH on some instances.


                                 16
            n           R0              R∗         R0 − R∗         n         R0              R∗       R0 − R∗
           126    12.417463955    12.417144417      10−4          230   16.596430072   16.596246697    10−4
           128     12.50231007    12.502222199      10−4          231   16.640078326   16.631031907    10−2
           130    12.602318936    12.601774612      10−3          242   16.962132986   16.961287246    10−3
           137    12.914725416    12.914711247      10−5          243   17.004065249   17.001947599    10−3
           138    12.962702608    12.961304417      10−3          244   17.039719463   17.039559451    10−4
           140    13.061097215    13.060696617      10−4          245   17.079365817   17.078003394    10−3
           156    13.719600039    13.718404613      10−3          246   17.113998222   17.113112319    10−3
           160    13.920538614    13.920451761      10−4          247   17.141082423   17.132526683    10−2
           163    14.069620216    14.067635971      10−3          248   17.184447103   17.182444113    10−3
           177    14.617194154    14.614803186      10−3          251   17.305245615   17.297607156    10−2
           178    14.658814223    14.655927628      10−3          252   17.331245569   17.326883903    10−2
           179    14.702293364    14.699982808      10−3          254   17.400734608   17.400641308    10−4
           180    14.742878035    14.739035484      10−3          255   17.454200693   17.454058463    10−4
           183    14.869399059    14.865788757      10−3          256   17.494310641    17.49310149    10−3
           188    15.028782734    15.028750763      10−5          258   17.547880529   17.547085193    10−3
           194    15.249753585    15.241428667      10−2          261   17.634862232   17.634766878    10−4
           197    15.368975294     15.36851843      10−4          277   18.142486517   18.139629995    10−3
           198    15.391207855    15.390410683      10−3          278   18.189804499   18.187675017    10−3
           204    15.652649998    15.644738394      10−2          279   18.224068629   18.221572693    10−3
           205    15.709043665    15.695538521      10−2          281   18.284504843   18.281539686    10−3
           207    15.770271663    15.770190573      10−4          282   18.315754345   18.309334921    10−2
           213    15.970256294    15.969855988      10−4          286   18.434315259   18.434157792    10−4
           214     16.01876322    16.018386421      10−4          296   18.704963368   18.703338597    10−3
           216    16.087407652    16.087017095      10−4          301   18.843979273   18.843675327    10−4
           217    16.119370348    16.118237367      10−3          302   18.895682961    18.89237664    10−3
           221    16.261873984    16.261873763      10−7          303   18.936286113   18.935589502    10−3
           222    16.299696226    16.299162417      10−3          304   18.973327182   18.972060389    10−3
           224     16.37189924    16.369591221      10−3          305   19.010908936   19.008914111    10−3
           225    16.409054279    16.408410528      10−3          308   19.121680199   19.120984457    10−3
           226    16.450019501    16.449824611      10−4          318   19.407004242   19.396538989    10−2
           227    16.494400009    16.489753739      10−2          319   19.432992566   19.432246442    10−3
           228     16.52734087    16.527071189      10−4          320   19.456230764   19.451309906    10−2
           229    16.566377981    16.564350195      10−3

                             Table 2: Improvements in the case of n = 126, 127, · · · , 320.


5. Conclusion

    We propose an efficient Quasi-physical Quasi-human (QPQH) algorithm for solving the clas-
sical Equal Circle Packing Problem (ECPP). Our contributions include: (1) We modified the
classic Quasi-Newton method BFGS by only considering the neighbor structure of each circle
during the iteration process. In this way, we considerably speed up the calculation, especially for
large scale instances. (2) We propose a new basin-hopping strategy of shrinking the container
size and the container adjustment procedure, which is simple but very effective. Experiments
on 320 ECPP instances (n = 1, 2, · · · , 320) demonstrate the success of the proposed algorithm.
For the first 100 instances (n = 1, 2, · · · , 100), we found 98 current best-known layouts except
n = 82, 100, and we found 66 better layouts for all the 320 instances. In the future, we will adapt
the idea of solving ECPP for unequal circles packing problem.


References
Addis, B., Locatelli, M., Schoen, F., 2008a. Disk packing in a square: a new global optimization approach. INFORMS
  Journal on Computing 20 (4), 516–524.
Addis, B., Locatelli, M., Schoen, F., 2008b. Efficiently packing unequal disks in a circle. Operations Research Letters
  36 (1), 37–42.
Akeb, H., Hifi, M., 2010. A hybrid beam search looking-ahead algorithm for the circular packing problem. Journal of
  combinatorial optimization 20 (2), 101–130.

                                                             17
Akeb, H., Hifi, M., MHallah, R., 2009. A beam search algorithm for the circular packing problem. Computers & Opera-
    tions Research 36 (5), 1513–1528.
Akiyama, J., Mochizuki, R., Mutoh, N., Nakamura, G., 2003. Maximin distance for n points in a unit square or a unit
    circle. In: Discrete and Computational Geometry. Springer, pp. 9–13.
Birgin, E. G., Martınez, J., Ronconi, D. P., 2005. Optimizing the packing of cylinders into a rectangular container: a
    nonlinear approach. European Journal of Operational Research 160 (1), 19–33.
Castillo, I., Kampas, F. J., Pintér, J. D., 2008. Solving circle packing problems by global optimization: numerical results
    and industrial applications. European Journal of Operational Research 191 (3), 786–802.
Demaine, E. D., Fekete, S. P., Lang, R. J., 2010. Circle packing for origami design is hard. CoRR abs/1008.1224.
Flores, J. J., Martı́nez, J., Calderón, F., 2015. Evolutionary computation solutions to the circle packing problem. Soft
    Computing, 1–15.
Fodor, F., 1999. The densest packing of 19 congruent circles in a circle. Geometriae Dedicata 74 (2), 139–145.
Fodor, F., 2000. The densest packing of 12 congruent circles in a circle. Beiträge Algebra Geom 41, 401–409.
Fodor, F., 2003. The densest packing of 13 congruent circles in a circle. Contributions to Algebra and Geometry 44 (2),
    431–440.
Fu, Z., Huang, W., Lü, Z., 2013. Iterated tabu search for the circular open dimension problem. European Journal of
    Operational Research 225 (2), 236–243.
Goldberg, M., 1971. Packing of 14, 16, 17 and 20 circles in a circle. Mathematics Magazine, 134–139.
Graham, R., 1968. Sets of points with given minimum separation (solution to problem e1921). Amer. Math. Monthly 75,
    192–193.
Graham, R. L., Lubachevsky, B. D., Nurmela, K. J., Östergård, P. R., 1998. Dense packings of congruent circles in a
    circle. Discrete Mathematics 181 (1), 139–154.
Grosso, A., Jamali, A., Locatelli, M., Schoen, F., 2010. Solving the problem of packing equal and unequal circles in a
    circular container. Journal of Global Optimization 47 (1), 63–81.
He, K., Huang, M., Yang, C., 2015. An action-space-based global optimization algorithm for packing circles into a square
    container. Computers & Operations Research 58 (C), 67–74.
He, K., Mo, D., Ye, T., Huang, W., 2013. A coarse-to-fine quasi-physical optimization method for solving the circle
    packing problem with equilibrium constraints. Computers & Industrial Engineering 66 (66), 1049–1060.
Hifi, M., M’Hallah, R., 2004. Approximate algorithms for constrained circular cutting problems. Computers & Opera-
    tions Research 31 (5), 675–694.
Hifi, M., MHallah, R., 2006. Strip generation algorithms for constrained two-dimensional two-staged cutting problems.
    European Journal of Operational Research 172 (2), 515–527.
Hifi, M., MHallah, R., 2007. A dynamic adaptive local search algorithm for the circular packing problem. European
    Journal of Operational Research 183 (3), 1280–1294.
Huang, W., Li, Y., Akeb, H., Li, C., 2005. Greedy algorithms for packing unequal circles into a rectangular container.
    Journal of the Operational Research Society 56 (5), 539–548.
Huang, W., Ye, T., 2011. Global optimization method for finding dense packings of equal circles in a circle. European
    Journal of Operational Research 210 (3), 474–481.
Huang, W. Q., Li, Y., Jurkowiak, B., Li, C. M., Xu, R. C., 2003. A two-level search strategy for packing unequal circles
    into a circle container. In: Principles and Practice of Constraint Programming–CP 2003. Springer, pp. 868–872.
Huang, W. Q., Li, Y., Li, C. M., Xu, R. C., 2006. New heuristics for packing unequal circles into a circular container.
    Computers & Operations Research 33 (8), 2125–2142.
Huang, W. Q., Zhan, S. H., 1982. A quasi- physical method of solving packing problems. pp. 176–180.
Kravitz, S., 1967. Packing cylinders into cylindrical containers. Mathematics magazine, 65–71.
Liu, D. C., Nocedal, J., 1989. On the limited memory bfgs method for large scale optimization. Mathematical Program-
    ming 45 (1), 503–528.
Liu, J., Jiang, Y., Li, G., Xue, Y., Liu, Z., Zhang, Z., 2015. Heuristic-based energy landscape paving for the circular
    packing problem with performance constraints of equilibrium. Physica A Statistical Mechanics & Its Applications
    431, 166–174.
Liu, J., Xue, S., Liu, Z., Xu, D., 2009. An improved energy landscape paving algorithm for the problem of packing
    circles into a larger containing circle. Computers & Industrial Engineering 57 (3), 1144–1149.
Liu, J., Zhang, K., Yao, Y., Xue, Y., Guan, T., 2016. A heuristic quasi-physical algorithm with coarse and fine adjustment
    for multi-objective weighted circles packing problem. Computers & Industrial Engineering 101, 416–426.
Lopez, C., Beasley, J., 2013. Packing unequal circles using formulation space search. Computers & Operations Research
    40 (5), 1276–1288.
Lü, Z., Huang, W., 2008. Perm for solving circle packing problem. Computers & Operations Research 35 (5), 1742–1755.
Melissen, H., 1994. Densest packings of eleven congruent circles in a circle. Geometriae Dedicata 50 (1), 15–25.
Mladenović, N., Plastria, F., Urošević, D., 2005. Reformulation descent applied to circle packing problems. Computers
    & Operations Research 32 (9), 2419–2434.
                                                            18
Mller, A., Schneider, J. J., Schmer, E., 2009. Packing a multidisperse system of hard disks in a circular environment.
   Physical Review E 79 (2 Pt 1), 319–354.
Pirl, U., 1969. Der mindestabstand von n in der einheitskreisscheibe gelegenen punkten. Mathematische Nachrichten
   40 (1-3), 111–124.
Reis, G. E., 1975. Dense packing of equal circles within a circle. Mathematics Magazine, 33–37.
Szabó, P. G., Markót, M. C., Csendes, T., 2005. Global optimization in geometrycircle packing into the square. In: Essays
   and Surveys in Global Optimization. Springer, pp. 233–265.
Wang, H., Huang, W., Zhang, Q., Xu, D., 2002. An improved algorithm for the packing of unequal circles within a larger
   containing circle. European Journal of Operational Research 141 (2), 440–453.
Ye, T., Huang, W., Lü, Z., 2013. Iterated tabu search algorithm for packing unequal circles in a circle. CoRR
   abs/1306.0694.
Zeng, Z., Yu, X., He, K., Huang, W., Fu, Z., 2015. Iterated tabu search and variable neighborhood descent for packing
   unequal circles into a circular container. European Journal of Operational Research 250 (2), 615–627.
Zhang, D.-f., Deng, A.-s., 2005. An effective hybrid algorithm for the problem of packing circles into a larger containing
   circle. Computers & Operations Research 32 (8), 1941–1951.




                                                           19
