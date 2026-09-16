                                        Geometric Batch Optimization for the Packing Equal Circles in a
                                        Circle Problem on Large Scale
                                        Jianrong Zhoua , Kun He∗a , Jiongzhi Zhenga and Chu-Min Lib
                                        a School of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan, 80039, China
                                        b MIS, University of Picardie Jules Verne, Amiens, 430074, France
arXiv:2303.02650v1 [cs.CG] 5 Mar 2023




                                        ARTICLE INFO                                      Abstract
                                        Keywords:                                         The problem of packing equal circles in a circle is a classic and famous packing problem,
                                        Global optimization                               which is well-studied in academia and has a variety of applications in industry. This problem
                                        Heuristics                                        is computationally challenging, and researchers mainly focus on small-scale instances with the
                                        Equal Circle Packing                              number of circular items 𝑛 less than 320 in the literature. In this work, we aim to solve this
                                        Geometric batch optimization                      problem on large scale. Specifically, we propose a novel geometric batch optimization method
                                        Solution-space exploring & descent                that not only can significantly speed up the convergence process of continuous optimization but
                                                                                          also reduce the memory requirement during the program’s runtime. Then we propose a heuristic
                                                                                          search method, called solution-space exploring and descent, that can discover a feasible solution
                                                                                          efficiently on large scale. Besides, we propose an adaptive neighbor object maintenance method
                                                                                          to maintain the neighbor structure applied in the continuous optimization process. In this way,
                                                                                          we can find high-quality solutions on large scale instances within reasonable computational
                                                                                          times. Extensive experiments on the benchmark instances sampled from 𝑛 = 300 to 1,000 show
                                                                                          that our proposed algorithm outperforms the state-of-the-art algorithms and performs excellently
                                                                                          on large scale instances. In particular, our algorithm found 10 improved solutions out of the
                                                                                          21 well-studied moderate scale instances and 95 improved solutions out of the 101 sampled
                                                                                          large scale instances. Furthermore, our geometric batch optimization, heuristic search, and
                                                                                          adaptive maintenance methods are general and can be adapted to other packing and continuous
                                                                                          optimization problems.




                                        1. Introduction
                                            The packing problems are a typical class of optimization problems that aim to pack a set of geometric objects
                                        into one or multiple containers, and the goal is to either find a configuration that is as dense as possible or find a
                                        solution with as few containers (bins) as possible. The packing problems have a rich research history, with numerous
                                        variants being proposed, and a number of studies and methods being published for solving these problems, such
                                        as circle packing (Huang and Ye, 2011; He, Ye, Wang and Liu, 2018; Lai, Hao, Yue, Lü and Fu, 2022), sphere
                                        packing (Hartman, Mazáč and Rastelli, 2019; Hifi and Yousef, 2019), square packing (Leung, Tam, Wong, Young and
                                        Chin, 1990; Fekete and Hoffmann, 2017), cube packing (Miyazawa and Wakabayashi, 2003; Epstein and van Stee,
                                        2005), irregular packing (Leao, Toledo, Oliveira, Carravilla and Alvarez-Valdés, 2020; Zhao, Jiang and Teo, 2020;
                                        Rao, Wang and Luo, 2021) and bin packing (Baldi, Manerba, Perboli and Tadei, 2019; Zhao, She, Zhu, Yang and Xu,
                                        2021; He, Tole, Ni, Yuan and Liao, 2021), etc.
                                            As one of the most popular packing problems, the Circle Packing Problem (CPP) has been widely studied in
                                        mathematics and computer science fields. Given 𝑛 circular items with fixed radii, the CPP aims to pack all the 𝑛 items
                                        into a container so that all the items are totally contained in the container without overlapping with each other, and
                                        the container size is minimized. Specifically, if the container is square, then the goal is to minimize the side length of
                                        the square container; and if the container is circular, then the goal is to minimize the radius of the circular container.
                                        There are also other CPP variants (López and Beasley, 2011) based on different geometric containers.
                                            CPP has a lot of industrial applications, such as facility layout, cylinder packing, circular cutting, container
                                        loading, dashboard layout (Castillo, Kampas and Pintér, 2008), structure design (Yanchevskyi, Lachmayer, Mozgova,
                                        Lippert, Yaskov, Romanova and Litvinchev, 2020) and satellite packaging (Wang, Wang, Sun, Huang and Zhang,
                                        2019). Furthermore, the solution of CPP can be applied to data visualization and data analysis (Wang, Wang, Dai and
                                        Wang, 2006; Murakami, Higo and Kusumoto, 2015; Görtler, Schulz, Weiskopf and Deussen, 2017). On the other hand,
                                            ∗ Corresponding author. Email: brooklet60@hust.edu.cn

                                             ORCID (s):



                                        Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                                   Page 1 of 26
                        Geometric Batch Optimization for the PECC Problem on Large Scale

CPP is proved to be NP-hard (Demaine, Fekete and Lang, 2010), therefore solving this problem is computationally
challenging. In particular, there is a special variant of CPP, called Packing Equal Circles in a Circle (PECC), which
aims to pack 𝑛 unit circles into a circular container with the smallest possible radius. Since PECC is representative
and simple in form, it has become the most famous and well-studied problem in the CPP family, to which numerous
efforts have been devoted.
    Since the CPP is NP-hard, the computational resource and difficulty for obtaining a high-quality configuration
grow exponentially with the number of circular items to be packed, and solving the large scale instances of CPP
is extremely difficult. Therefore, most works for CPP focus on solving instances on small or moderate scale, and
only a few efforts are devoted to solving large scale instances. In this work, we address the PECC variant of CPP.
Based on the classic elastic model (Huang and Xu, 1999; He et al., 2018) (also known as Quasi-Physical Quasi-
Human model, QPQH), we propose a Geometric Batch Optimization (GBO) method that can construct a feasible
solution or an infeasible solution with the overlaps being as few as possible on large scale instances. Different from
existing methods, GBO divides the packing circles into several geometric batches. Then, in the non-convex continuous
optimization process, GBO alternately updates each batch of packing circles instead of updating all the circles. In this
way, GBO reduce the time and space complexity, which can not only significantly speed up the convergence process
of the non-convex continuous optimization but also reduce the resident memory requirement during the program’s
runtime.
    In addition, we propose an Adaptive Neighbor object Maintenance (ANM) method to maintain the neighbor
structure (He et al., 2018) for the continuous optimization process. ANM uses two variables “𝑐𝑜𝑢𝑛𝑡𝑒𝑟” and
“𝑑𝑒𝑓 𝑒𝑟𝑟𝑖𝑛𝑔 𝑙𝑒𝑛𝑔𝑡ℎ” to accomplish the adaptive feature. When the layout is changing significantly, ANM maintains
the neighbors in each iteration, otherwise, ANM defers the maintaining process. Our ANM method can handle some
issues and disadvantages of the existing methods (He et al., 2018; Lai et al., 2022) and it can adopt to solve dynamic
packing problems or online packing problems.
    Finally, we propose an advanced local search heuristic, called Solution-space Exploring and Descent (SED), based
on the GBO module to solve the PECC problem. SED perturbs the current solution to obtain several perturbed
candidate solutions. Then, SED employs the GBO module to minimize the overlap of each candidate solution and
takes a solution with minimal overlap among the candidate solutions to replace the current solution. The algorithm
could efficiently find a high-quality solution by iteratively executing the SED heuristic procedure.
    The experimental results show that our GBO method dramatically accelerates the convergence speed of the non-
convex continuous process and reduces memory consumption. Specifically, GBO reduces the convergence time by
32.74% to 54.11% and the runtime resident memory by 36.00% to 39.04% compared with the typical non-batch
method on large scale instances for 𝑛 = 500 to 1,000. By combining the GBO module into SED to solve 101
large scale instances, including 51 regular numbers and 50 irregular numbers selected from 500 ≤ 𝑛 ≤ 1,000, our
method improves the best-known solution for 95 instances reported in Packomania website (Specht, 2022). Besides,
our method is also efficient on moderate scale instances, because it improves the best-known solution for 10 instances
among the 21 well-studied moderate scale instances, 300 ≤ 𝑛 ≤ 320, which were solved by the state-of-the-art
algorithm called IDTS (Lai et al., 2022). Through these experiments, GBO shows clear advantages over existing
methods for solving large scale packing instances and SED is an efficient heuristic.
    The main contributions of this work are summarized as follows:
    • We propose a novel method called Geometric Batch Optimization (GBO), which divides the circles into several
      geometric batches and speeds up the computation significantly.
    • We propose an Adaptive Neighbor object Maintenance (ANM) method of the neighbor structure for solving the
      PECC problem.
    • We propose an efficient Solution-space Exploring and Descent (SED) heuristic with the GBO as a sub-module
      for solving the PECC problem.
    • Extensive experiments on large scale instances sampled from 𝑛 = 500 to 1,000, as well as moderate instances
      for 𝑛 = 300 to 320, demonstrate the excellent performance and efficiency of our proposed algorithm, gaining
      new best solutions on many instances.
    The rest of this paper is organized as follows. Section 2 presents the related works of the CPP and PECC problem,
including the landmark models, the landmark heuristics, and the recent works for solving the CPP and PECC problems.

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                           Page 2 of 26
                         Geometric Batch Optimization for the PECC Problem on Large Scale

Section 3 introduces the mathematical formula of the PECC problem and the famous and powerful elastic model
(QPQH) that is adopted in this work. Section 4 presents the continuous optimization methods, including our proposed
GBO method, the container adjusting method, and our ANM method, which are the essential modules adopted in our
final heuristic. Section 5 presents the discrete optimization method (i.e., SED heuristic), which is our final algorithm
for solving the PECC problem. Section 6 presents the experimental results of our proposed algorithm compared with
the best-known results and the state-of-the-art algorithm and parameter study. The conclusion is drawn in the end.


2. Related Work
    In this section, We briefly review the works on CPP, including some typical works, landmark models, and landmark
heuristics, then we review the recent works on the PECC problem.
    Early works for solving CPP focus on solving the PECC variant using mathematical analysis with the goal of
finding and proving an optimal solution for small scale instances. Starting from 1967, Kravitz (1967) first provided
the solutions for 2 ≤ 𝑛 ≤ 19. Subsequently, Graham and Peck (1968) proved the optimality for 2 ≤ 𝑛 ≤ 7. In 1969,
Pirl (1969) further proved the optimality of the solutions for 2 ≤ 𝑛 ≤ 10 and also provided solutions for 11 ≤ 𝑛 ≤ 19.
In 1971, Goldberg (1971) improved the solutions for 𝑛 = 14, 16, 17 and further provided the solution for 𝑛 = 20. In
1975, Reis (1975) provided the solutions for 21 ≤ 𝑛 ≤ 25. Melissen (1994) proved the optimality for 𝑛 = 11 and
Fodor (1999, 2000, 2003) proved the optimality for 𝑛 = 12, 13, 19. To summarize, the optimality for 2 ≤ 𝑛 ≤ 13 and
𝑛 = 19 has been proven. For larger instances, it is hard to find and prove the optimality of a solution by exploiting
mathematical analysis. Thereafter, most efforts are devoted to designing efficient heuristic algorithms.
    The discrete optimization model is one of the popular techniques for solving CPP, of which the idea is to pack each
circle one by one into the container. If there exists a placement order by which all the circles can be packed into the
container, then the solution is found. A circle placement heuristic is essential to this model, because it directly impacts
the placement strategies and the performance. Huang, Li, Jurkowiak, Li and Xu (2003) and Huang, Li, Li and Xu
(2006) propose a classic circle placement heuristic, called Corner-Occupying Placement (COP), and a metric function
for placement action, named Maximal Hole Degree (MHD), on the unequal circle packing problem. COP requests
each current packing circle contact with two packed circles or the boundary of the container and does not overlap with
other circles, and the MHD function can measure the quality of the candidate action of the circle placement. There
are several follow-up works based on COP heuristic and MHD function to either solve other variants or improve the
algorithm efficiency: Huang, Li, Akeb and Li (2005) adopt this heuristic for packing circles in a rectangular container;
Lü and Huang (2008) apply a Pruned–Enriched-Rosenbluth Method (PERM) to improve the performance on the
unequal circle packing problem; Akeb, Hifi and M’Hallah (2009); Akeb, Hifi and M’Hallah (2010) further employ the
beam search and adaptive beam search algorithms to improve the performance on unequal circle packing problems,
and Chen, Tang, Song, Zeng, Peng and Liu (2018) present a greedy heuristic algorithm for solving the PECC problem.
There also exist other circle placement heuristics for solving the packing problems, such as Bottom-Left-Fill (Martello,
Monaci and Vigo, 2003; Burke, Hellier, Kendall and Whitwell, 2006) and Best Local Position (Hifi and M’Hallah,
2004; Hifi and M’Hallah, 2007).
    However, due to the characteristic of the discrete optimization model, it takes massive computational time to
obtain a dense solution on moderate or large scale instances. Therefore, most researchers prefer to adopt the non-
convex continuous optimization model to solve moderate scale CPP. Inspired by the physical model, some quasi-
physical models have been proposed for solving CPP. Graham, Lubachevsky, Nurmela and Östergård (1998) design a
molecular repulsion model and a Billiards model for solving the PECC problem, and these models are also applied to
solve other packing variants (Nurmela and Östergård, 1997). Some efforts are devoted to designing an efficient local
search heuristic based on the elastic model, termed Quasi-Physical Quasi-Human (QPQH), proposed by Huang and
Xu (1999) for solving CPP and its variants: Huang and Ye (2011) propose a basin hopping heuristic of attractive force
model to solve the PECC problem; He et al. (2018) propose a shrinking basin-hopping heuristic to solve the PECC
problem; Lai et al. (2022) adopt the iterated dynamic thresholding search to solve the PECC problem; He, Mo, Ye and
Huang (2013) employ the elastic model to solve circle packing problem with equilibrium constraints and Liu, Zhang,
Yao, Xue and Guan (2016) employ the elastic model to solve the weighted circle packing problem.
    There also exist other methods and heuristics for solving CPP, such as monotonic basin hopping and population
basin hopping heuristics (Addis, Locatelli and Schoen, 2008; Grosso, Jamali, Locatelli and Schoen, 2010), simulated
annealing approach (Hifi, Paschos and Zissimopoulos, 2004), genetic algorithm-based approach (Hifi and M’Hallah,


Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                             Page 3 of 26
                         Geometric Batch Optimization for the PECC Problem on Large Scale

2004), tabu search approach (Carrabs, Cerrone and Cerulli, 2014), non-linear programming based approach (Mlade-
nović, Plastria and Urošević, 2005; Birgin and Sobral, 2008; Stoyan and Yaskov, 2014), mixed-strategy (Stoyan,
Yaskov, Romanova, Litvinchev, Yakovlev and Cantú, 2020), etc.
    The well-known Packomania website (Specht, 2022) maintained by Specht presents many circle packing problems
and records their best-known solutions. According to the number of solutions, the scale of solutions, and the recently
updated history, we observe that the PECC problem and the problem of circle packing in a rectangle are popular
and well-studied, and the recent algorithms for solving the two problems are similar to the methods mentioned
above, suggesting that these methods and algorithms have good universality and generality on different circle packing
problems and their variants.
    From the recently updated history on PECC with 𝑛 ≥ 100 at Packomania, we observe the current best-known
records as follows: Huang and Ye (2011) hold several best-known solutions for 100 ≤ 𝑛 ≤ 200; Cantrell holds several
best-known solutions for 110 ≤ 𝑛 ≤ 1039 with unpublished methods; Donovan holds three best-known solutions
for 𝑛 = 85, 109 and 121 with unpublished methods; Lai et al. (2022) hold a number of best-known solutions for
126 ≤ 𝑛 ≤ 319, Stoyan et al. (2020) hold 16 best-known solutions for 1077 ≤ 𝑛 ≤ 5000, and the remaining
best-known solutions are held by Specht with unpublished methods. In summary, the elastic model (QPQH) based
methods (Huang and Ye, 2011; Lai et al., 2022) and mixed-strategy method (Stoyan et al., 2020) can be regarded as
the state-of-the-art algorithms for solving the PECC problem.

3. Preliminaries
3.1. Problem Formulation
    The PECC problem aims to pack 𝑛 unit circles {𝑐1 , 𝑐2 , ..., 𝑐𝑛 } into a circular container with the smallest possible
radius while subjected to two constraints: (I) Any two circles do not overlap; (II) Any circle does not exceed the
container. The problem can be formulated in the Cartesian coordinate system as a non-linear constrained optimization
problem:
      Minimize      𝑅
                    √
             s.t.     (𝑥𝑖 − 𝑥𝑗 )2 + (𝑦𝑖 − 𝑦𝑗 )2 ≥ 2, 1 ≤ 𝑖, 𝑗 ≤ 𝑛, 𝑖 ≠ 𝑗,                                                (1)
                    √
                      𝑥2𝑖 + 𝑦2𝑖 + 1 ≤ 𝑅, 1 ≤ 𝑖 ≤ 𝑛,                                                                      (2)

where 𝑅 is the radius of the circular container centered at the origin (0, 0), and the center of unit circle 𝑐𝑖 is located at
(𝑥𝑖 , 𝑦𝑖 ). Eqs. (1) and (2) correspond to the two constraints (I) and (II).

3.2. The Elastic Model (QPQH) for PECC
     The elastic model (Huang and Xu, 1999; He et al., 2018; Lai et al., 2022) could be regarded as a relaxation of the
PECC problem, considering that each circle is elastic. An algorithm following this model first forces all circles to be
packed into the container with possible circle-circle and circle-container overlapping, and quantifies the overlapping
degree using a metric function. The main work of the algorithm is then to minimize the value of the metric function
(i.e., minimize the overlapping area). In this way, the elastic model converts the PECC problem to an unconstrained
non-convex continuous optimization problem.
Definition 3.1 (Overlapping distance). The overlapping distance of two unit circles 𝑐𝑖 and 𝑐𝑗 , denoted as 𝑑𝑖𝑗 , is defined
as follows:
                 (       √                       )
       𝑑𝑖𝑗 = max 0, 2 − (𝑥𝑖 − 𝑥𝑗 )2 + (𝑦𝑖 − 𝑦𝑗 )2 ,                                                                      (3)

And the overlapping distance of circle 𝑐𝑖 to the container, denoted as 𝑑𝑖0 , is defined as follows:
                ( √                      )
                        2    2
     𝑑𝑖0 = max 0, 𝑥𝑖 + 𝑦𝑖 + 1 − 𝑅 .

    Figure 1 shows a conflicting example with the two types of overlaps. According to the theory of elasticity, the
elastic potential energy between two elastic objects is proportional to the square of the embedded distance, giving the
following elastic energy definition.

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                               Page 4 of 26
                          Geometric Batch Optimization for the PECC Problem on Large Scale




Fig. 1: Illustration of a conflicting example with two types of overlaps, where 𝑑𝑖𝑗 indicates the circle-circle overlapping
distance and 𝑑𝑖0 indicates the circle-container overlapping distance.



Definition 3.2 (Elastic energy). The total elastic energy 𝐸 of the PECC system is defined as follows:

                 ∑
                 𝑛 ∑
                   𝑛                  ∑
                                      𝑛
      𝐸𝑅 (𝒙) =               𝑑𝑖𝑗2 +          2
                                            𝑑𝑖0 ,                                                                          (4)
                 𝑖=1 𝑗=𝑖+1            𝑖=1

where 𝒙 = [𝑥1 , 𝑦1 , 𝑥2 , 𝑦2 , ..., 𝑥𝑛 , 𝑦𝑛 ]T is a vector, 𝒙 ∈ ℝ2𝑛 , representing a candidate solution, and 𝑅 is the container
radius.
   Note that, in the elastic model of the PECC problem, the energy quantifies the overlapping degree. When the
energy 𝐸, i.e., Eq. (4), is equal to zero, Eqs. (1) and (2) are satisfied and the solution is feasible for the PECC problem.
Since the radius 𝑅 of the container is fixed in the rest of the paper, we omit the subscript 𝑅 in 𝐸𝑅 (𝒙) and denote it
simply as 𝐸(𝒙) in the rest of the paper for readability reason.


4. Continuous Optimization
    Since we employ the elastic model for solving the PECC problem, our target switches to minimizing the energy
𝐸 so as to discover a feasible solution that can be solved using continuous optimization algorithms. In this section,
we present 1) our proposed Geometric Batch Optimization (GBO) method for minimizing the energy of a conflicting
solution with a fixed container radius, which can be regarded as a batch non-convex continuous optimization algorithm,
2) the optimization method for adjusting container radius to obtain a feasible solution with a minimal radius 𝑅, 3)
our proposed Adaptive Neighbor object Maintenance (ANM) method that can adaptively and efficiently maintain
the neighbor structure in the continuous optimization process, and finally, 4) we give a complexity analysis of our
proposed GBO method.

4.1. The GBO Method for Solving PECC
   Let 𝑘 be a hyperparameter. Given an infeasible solution in which 𝑛 elastic unit circles are already forced to be
packed in the container, GBO first evenly partitions these circles into 𝑘 disjoint sets: 𝐵1 , 𝐵2 , ..., 𝐵𝑘 , with the following

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                 Page 5 of 26
                              Geometric Batch Optimization for the PECC Problem on Large Scale

  Algorithm 1: GBO (𝒙, 𝑅)
 1   Input: A candidate solution 𝒙; and the fixed container radius 𝑅
 2   Output: A local minimum solution 𝒙∗
      1: (𝒙1 , 𝒙2 , … , 𝒙𝑘 ) ← partition(𝒙)
      2: (𝑯 1 , 𝑯 2 , … , 𝑯 𝑘 ) ← (𝑰, 𝑰, … , 𝑰)
      3: 𝑐𝑛𝑡 ← 0, 𝑙𝑒𝑛 ← 1
      4: construct the current neighbor Γ
      5: for 𝑡 for 1 to 𝑀𝑎𝑥𝐼𝑡𝑒𝑟 do
      6:   for 𝑝 from 1 to 𝑘 do
      7:       calculate 𝑔(𝒙𝑝 )
      8:       calculate 𝛼𝑝 by using Eq. (7)
      9:       𝒙𝑝 ← 𝒙𝑝 − 𝛼𝑝 𝑯 𝑝 𝑔(𝒙𝑝 )
     10:       update 𝑯 𝑝 by using Eqs. (8) and (9)
     11:   end for
     12:   (𝑐𝑛𝑡, 𝑙𝑒𝑛, Γ) ← ANM(𝑐𝑛𝑡, 𝑙𝑒𝑛, Γ)
               ∑
     13:   if 𝑘𝑝=1 ‖𝑔(𝒙𝑝 )‖2 ≤ 10−12 then
     14:       break
     15:   end if
     16: end for
     17: 𝒙∗ ← merge(𝒙1 , 𝒙2 , … , 𝒙𝑘 )
     18: return 𝒙∗



properties:
       𝐵𝑝 ∩ 𝐵𝑞 = ∅,        1 ≤ 𝑝, 𝑞 ≤ 𝑘, 𝑝 ≠ 𝑞
       ⋃
       𝑘
             𝐵𝑝 = {𝑐1 , 𝑐2 , … , 𝑐𝑛 }.
       𝑝=1

Each subset of circles is regarded as a batch. The circles in batch 𝐵𝑝 can be represented as a vector 𝒙𝑝 , and the energy
𝐸(𝒙𝑝 ) of the circles in batch 𝐵𝑝 can be reformulated as follows:

                    ∑∑
                     𝑛                                  ∑
       𝐸(𝒙𝑝 ) =               𝑑𝑖𝑗2 [𝑗 ∉ 𝐵𝑝 ∨ 𝑗 < 𝑖] +           2
                                                               𝑑𝑖0 ,                                                       (5)
                   𝑖∈𝐵𝑝 𝑗=1                             𝑖∈𝐵𝑝

where [] is the Iverson bracket that [𝑃 ] = 1 if statement 𝑃 is true, and otherwise [𝑃 ] = 0. The statement
“𝑗 ∉ 𝐵𝑝 ∨ 𝑗 < 𝐼” guarantees the circle-circle overlaps in batch 𝐵𝑝 only be calculated once. We employ the
Broyden–Fletcher–Goldfarb–Shanno (BFGS) algorithm (Ren-Pu and Powell, 1983) as our basic optimization method
to minimize the batch energy, by iteratively reducing the energy 𝐸(𝒙𝑝 ) as follows:

       𝒙(𝑡+1)
        𝑝     ← 𝒙(𝑡)  (𝑡) (𝑡)  (𝑡)
                 𝑝 − 𝛼𝑝 𝑯 𝑝 𝑔(𝒙𝑝 ),                                                                                        (6)
                                                                                                            [             ]−1
where superscript 𝑡 indicates the algorithm at the 𝑡-th iteration, 𝑯 (𝑡) is an approximation Hessian matrix   ∇ 2 𝐸(𝒙(𝑡) )    ,
                                                                     𝑝                                               𝑝
𝛼 is the step length obtained by the line search method, and the function 𝑔(𝒙) is the gradient of the energy, i.e., ∇𝐸(𝒙).
The update of 𝑯 (𝑡+1)
                   𝑝   and the calculation of 𝛼𝑝(𝑡) are performed as follows:
                         (                        )
       𝛼𝑝(𝑡) = arg min 𝐸 𝒙(𝑡)
                            𝑝 − 𝛼𝑯   (𝑡)
                                     𝑝   𝑔(𝒙(𝑡)
                                            𝑝   )   ,                                                                      (7)
                𝛼∈ℝ+
       𝒖𝑝 = 𝒙(𝑡+1)
        (𝑡)
                𝑝    − 𝒙(𝑡)
                        𝑝 ,    𝒗(𝑡)
                                 𝑝 = 𝑔(𝒙𝑝
                                         (𝑡+1)
                                               ) − 𝑔(𝒙(𝑡)
                                                       𝑝 ),     𝛽 = (𝒗(𝑡) T (𝑡)
                                                                      𝑝 ) 𝒖𝑝 ,                                             (8)
                  (                  )      (                   )
          (𝑡+1)
                        𝒖(𝑡)   (𝑡) T
                          𝑝 (𝒗𝑝 )       (𝑡)
                                                   𝒗(𝑡)   (𝑡) T
                                                     𝑝 (𝒖𝑝 )         𝒖(𝑡)   (𝑡) T
                                                                      𝑝 (𝒖𝑝 )
       𝑯𝑝       = 𝑰−                   𝑯𝑝 𝑰 −                     +               .                                        (9)
                             𝛽                          𝛽                 𝛽

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                 Page 6 of 26
                         Geometric Batch Optimization for the PECC Problem on Large Scale




                           (a) Sector                                                (b) Annulus




                           (c) Fence                                                 (d) Random

Fig. 2: Illustration of the four partitions of the GBO method. The illustrative example has 300 circles (𝑛 = 300), which is
evenly partitioned into three batches (𝑘 = 3) colored by three different colors where each batch having 100 circles.



    In this way, the PECC problem is converted to an unconstrained non-convex continuous optimization problem
with a fixed container radius. The pseudocode of our proposed GBO algorithm is presented in Algorithm 1. Given a
candidate solution 𝒙, a fixed container radius 𝑅, algorithm GBO(𝒙, 𝑅) returns a solution 𝒙∗ such that energy 𝐸(𝒙∗ )
reaches a local minimum. For this purpose, GBO first partitions the 𝑛 unit circles into 𝑘 batches (line 1), then GBO
applies the BFGS method to minimize the energy on each batch iteratively (lines 6-11), the iteration process terminates
when the maximum iteration step is reached (line 5) or the sum of the 𝐿2 -norm of 𝑘-batch gradients is tiny enough
(lines 13-15). Finally, GBO returns a local minimum solution 𝒙∗ obtained by merging the 𝑘-batch circles (line 17).
Though it is hard to provide a mathematical analysis on the convergence of the proposed GBO algorithm, we observe
that it always meets the convergence condition (line 13) when the maximum iteration step is set large enough.


Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                             Page 7 of 26
                             Geometric Batch Optimization for the PECC Problem on Large Scale

    To minimize the total computational complexity of the GBO method, each batch groups nearly the same number
of circles. Concretely, the size of each batch is either ⌊ 𝑘𝑛 ⌋ or ⌈ 𝑘𝑛 ⌉. We provide several geometric 𝑘-batch partition
strategies for solving the PECC problem, described as follows:
                                                                                                              𝑦
    • 1) Sector (default): Sort all circles in the container in ascending order of the angle 𝜃𝑖 = arctan 𝑥𝑖 , then partition
                                                                                                          𝑖
      them into 𝑘 subsets successively.
                                                                                  √
    • 2) Annulus: Sort all circles in ascending order of the distance 𝑑𝑖𝑠𝑖 = 𝑥𝑖 2 + 𝑦𝑖 2 , then partition them into 𝑘
      subsets successively.
    • 3) Fence: Sort all circles in ascending order of the coordinate 𝑥𝑖 , then partition them into 𝑘 subsets successively.
    • 4) Random: Partition all circles into 𝑘 sets randomly.

Our experiments show that the sector partition outperforms other partitions, so the default partition is set as sector in
this work. Figure 2 illustrates the above four partitions of the GBO method.

4.2. Optimization Method for Adjusting the Container
    Starting from a random layout (all the circles are randomly placed in the container and overlapping is allowed),
a local minimum solution is obtained by applying the GBO method, possibly containing overlaps and thus being
infeasible. One strategy for obtaining a feasible solution is to expand the container radius and adjust the layout until the
overlaps are eliminated. The most intuitive and common way to achieve this goal is to adopt the binary search (Huang
and Ye, 2011; He et al., 2018). Recently, a smart and significantly faster method is proposed in (Lai et al., 2022) to
find a feasible solution with a local minimum container radius 𝑅, which we present as follows.
    Let vector 𝒛 = [𝑥1 , 𝑦1 , 𝑥2 , 𝑦2 , ..., 𝑥𝑛 , 𝑦𝑛 , 𝑅]T , 𝒛 ∈ ℝ2𝑛+1 , be a candidate solution with the container radius 𝑅 as a
variable. A new elastic energy 𝑈 can be reformulated as follows:

                    ∑
                    𝑛 ∑
                      𝑛                   ∑
                                          𝑛
      𝑈 (𝒛, 𝜆) =                 𝑑𝑖𝑗2 +          2
                                                𝑑𝑖0 + 𝜆𝑅2 ,                                                                 (10)
                     𝑖=1 𝑗=𝑖+1            𝑖=1

where 𝜆𝑅2 is a penalty term, and 𝜆 is a penalty coefficient. By employing the optimization method to minimize the
energy 𝑈 , the container radius prefers to shrink when 𝜆 increases, and it prefers to expand when 𝜆 is decreasing.
Therefore, the model converts the current goal to an unconstrained continuous optimization problem. By adjusting 𝜆,
it could allow to obtain a feasible solution when minimizing the energy 𝑈 with a local minimum container radius.
     We adopt the main idea of adjusting container radius of (Lai et al., 2022) and control 𝜆𝑅2 to minimize the container
size. The pseudocode of our container radius adjusting method is depicted in Algorithm 2. Given a candidate solution
(𝒙, 𝑅), Algorithm 2 initializes the coefficient 𝜆 to an empirically fixed value 10−4 and combines (𝒙, 𝑅) to obtain a new
candidate solution 𝒛; then the algorithm performs several iterations to obtain a feasible solution. At each iteration, the
algorithm employs the BFGS method to minimize the energy 𝑈 (𝒛, 𝜆) and updates the candidate solution 𝒛. Then, the
algorithm halves 𝜆 and continually adjusts the candidate solution 𝒛 at the next iteration. After several iterations, the
energy 𝑈 (𝒛, 𝜆) converges to 0, so that the overlaps are tiny enough and the candidate solution 𝒛 can be regarded as a
feasible solution with a local minimum container radius. Finally, the method returns the solution (𝒙∗ , 𝑅∗ ) as the result.
     Note that the term 𝜆𝑅2 is tiny enough with sufficient iteration steps. The algorithm forces to converge the energy
𝐸(𝒙) = 0 (𝑈 degenerates to 𝐸 without penalty term 𝜆𝑅2 ) with non-fixed container radius.

4.3. The Neighbor Structure of Circles for Optimization
   He et al. (2018) first propose an efficient neighbor structure, which can efficiently calculate the energies 𝐸 and
𝑈 and its gradient functions of a candidate solution, and the state-of-the-art algorithm IDTS (Lai et al., 2022) also
adopts this method. In this subsection, we first introduce the neighbor structure. Then, we present our proposed ANM
method and discuss the advantage of our method over the existing methods.
   Let 𝑙𝑖𝑗 denote the distance between the centers of two unit circles 𝑐𝑖 and 𝑐𝑗 :
              √
      𝑙𝑖𝑗 =       (𝑥𝑖 − 𝑥𝑗 )2 + (𝑦𝑖 − 𝑦𝑗 )2 ,


Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                   Page 8 of 26
                            Geometric Batch Optimization for the PECC Problem on Large Scale

    Recall that 𝑑𝑖𝑗 denotes the energy between two unit circles 𝑐𝑖 and 𝑐𝑗 and is defined by Eq. (3). It is clear that
𝑑𝑖𝑗 > 0 when 𝑙𝑖𝑗 < 2, and 𝑑𝑖𝑗 = 0 otherwise. We define the neighbor Γ(𝑖) of circle 𝑐𝑖 to be a subset of 𝑛 unit circles as
follows, using a distance controlling hyperparameter 𝑙𝑐𝑢𝑡 :
             {                                     }
      Γ(𝑖) = 𝑐𝑗 ∣ ∀𝑗 ∶ 1 ≤ 𝑗 ≤ 𝑛, 𝑖 ≠ 𝑗, 𝑙𝑖𝑗 < 𝑙𝑐𝑢𝑡 ,

When 𝑙𝑐𝑢𝑡 = 2, all the circles {𝑐𝑗 } overlapping with circle 𝑐𝑖 are contained in Γ(𝑖). Therefore the energies concerning
circle 𝑐𝑖 can be calculated by enumerating the circles 𝑐𝑗 in Γ(𝑖) instead of enumerating all the packing circles. So, the
batch energy 𝐸 (Eq. (5)) and the energy 𝑈 (Eq. (10)) can be reformulated as follows:
                 ∑ ∑                               ∑
       𝐸(𝒙𝑝 ) =            𝑑𝑖𝑗2 [𝑗 ∉ 𝐵𝑝 ∨ 𝑗 < 𝑖] +    2
                                                     𝑑𝑖0 ,
                𝑖∈𝐵𝑝 𝑗∈Γ(𝑖)                                  𝑖=1

                    ∑
                    𝑛    ∑                        ∑
                                                  𝑛
       𝑈 (𝒛, 𝜆) =                𝑑𝑖𝑗2 [𝑗 < 𝑖] +          2
                                                        𝑑𝑖0 + 𝜆𝑅2 ,
                    𝑖=1 𝑗∈Γ(𝑖)                    𝑖=1

    Note that the statements “𝑗 ∉ 𝐵𝑝 ∨ 𝑗 < 𝑖” and “𝑗 < 𝑖” guarantee the circle-circle overlaps be calculated only once.
    However, when 𝑙𝑐𝑢𝑡 = 2, the neighbor structure needs to be maintained even if the circles have minor shifts in
the layout, otherwise, the correctness of the energy and gradient computation can not be guaranteed. Therefore, if
we properly increase the value of 𝑙𝑐𝑢𝑡 , more adjacent circles are contained in the neighbor, so that the correctness is
guaranteed without maintaining the neighbor structure when the circles have minor shifts in the layout. But if 𝑙𝑐𝑢𝑡
is set too large, the neighbor contains many unnecessary circles, increasing the time cost of the energy and gradient
computation. Therefore, we empirically set 𝑙𝑐𝑢𝑡 = 4 as a trade-off setting. Figure 3 gives an example to show the
neighbors of a circle and the different settings of 𝑙𝑐𝑢𝑡 . Note that calculating the energies 𝐸 and 𝑈 and their gradients
by enumerating the pairwise circles is of 𝑂(𝑛2 ) complexity. By adopting the neighbor structure, the complexity can
be reduced to 𝑂(𝑛) (He et al., 2018).
    Our proposed ANM method is depicted in Algorithm 3. ANM maintains three parameters, i.e., the counter 𝑐𝑛𝑡,
deferring length 𝑙𝑒𝑛, and historical neighbor Γ. Initially, the counter is set to 0, the length is set to 1, and the algorithm
calculates an initial neighbor Γ (refer to Algorithm 1 lines 3-4). In the continuous optimization process, the ANM is
called after each iteration (see in Algorithm 1 line 12), and the counter will increase by 1 when ANM is called. If the
counter 𝑐𝑛𝑡 equals the deferring length 𝑙𝑒𝑛, ANM reconstructs a new neighbor Γ′ and compares it with the historical
neighbor Γ. If two neighbors Γ′ and Γ are the same, the counter is set to 0 and the deferring length 𝑙𝑒𝑛 is multiplied
by 2, otherwise, the counter is set to 0, the deferring length is set to 1 and the neighbor Γ is updated by Γ′ .
    The basic idea of ANM to defer maintaining the neighbor structure is based on the operation of the counter 𝑐𝑛𝑡 and
the deferring length 𝑙𝑒𝑛. If the layout is unstable and the neighbor is changed, ANM reconstructs the neighbor in every
iteration. If the layout is stable, the deferring length 𝑙𝑒𝑛 grows exponentially, which makes ANM defers maintaining
the neighbor. It is worth noting that the Voronoi diagram approach can also be used to construct the√neighbor, which
can gain an excellent time complexity 𝑂(𝑛 log 𝑛). In this work, we adopt the scan line approach (𝑂(𝑛 𝑛)) to construct
the neighbor, which is efficient enough and easy to implement.
    He et al. (2018) use a simple strategy to maintain the neighbor, consisting in reconstructing the neighbor every
10 iterations. However, reconstructing the neighbor is unnecessary when the layout is stable, and it will waste


  Algorithm 2: adjust_container(𝒙, 𝑅)
 1   Input: A candidate solution 𝒙 and the container radius 𝑅
 2   Output: A feasible solution with local minimum container radius (𝒙∗ , 𝑅∗ )
      1: 𝒛∗ ← combine(𝒙, 𝑅), 𝜆 ← 10−4
      2: for 𝑡 from 1 to 35 do
      3:   employ BFGS to minimize the energy 𝑈 (𝒛∗ , 𝜆)
      4:   𝜆 ← 0.5 × 𝜆
      5: end for
      6: (𝒙∗ , 𝑅∗ ) ← divide(𝒛∗ )
      7: return (𝒙∗ , 𝑅∗ )



Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                Page 9 of 26
                           Geometric Batch Optimization for the PECC Problem on Large Scale




Fig. 3: Illustration of the neighbors of a circle with different 𝑙𝑐𝑢𝑡 settings. This illustrative example gives three settings for
𝑙𝑐𝑢𝑡 = 2, 4 or 6 on a conflicting layout. We empirically set 𝑙𝑐𝑢𝑡 = 4 as a trade-off setting in this work.


  Algorithm 3: ANM (𝑐𝑛𝑡, 𝑙𝑒𝑛, Γ)
 1   Input: A deferring counter 𝑐𝑛𝑡; A deferring length 𝑙𝑒𝑛; A neighbor Γ
 2   Output: An updated counter 𝑐𝑛𝑡; A updated length 𝑙𝑒𝑛; A updated neighbor Γ
      1: 𝑐𝑛𝑡 ← 𝑐𝑛𝑡 + 1
      2: if 𝑐𝑛𝑡 ≥ 𝑙𝑒𝑛 then
      3:    construct the current neighbor Γ′
      4:    if Γ ≠ Γ′ then
      5:       𝑐𝑛𝑡 ← 0, 𝑙𝑒𝑛 ← 1, Γ ← Γ′
      6:    else
      7:       𝑐𝑛𝑡 ← 0, 𝑙𝑒𝑛 ← 2 × 𝑙𝑒𝑛
      8:    end if
      9: end if
     10: return (𝑐𝑛𝑡, 𝑙𝑒𝑛, Γ)



computational resources in this case. Lai et al. (2022) propose a two-phase strategy. In the first phase, they calculate the
energy and gradient by enumerating all the pairwise circles without using the neighbor structure. When the condition
‖𝑔(𝒙)‖∞ < 10−2 is met, they change to the second phase. In the second phase, they construct the neighbor structure
only at the beginning of the phase; then they use the neighbor structure to obtain the energy and gradient until the
algorithm finds a local minimum solution. This two-phase strategy has three disadvantages: 1) The enumeration
method in the first phase is computationally expensive, especially on large scale instances. 2) The threshold of the

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                  Page 10 of 26
                         Geometric Batch Optimization for the PECC Problem on Large Scale

condition needs to be fine-tuned on the different scales of instances. 3) The neighbor structure is not updated in the
second phase, so that if the solution falls into a saddle point, the correctness of this strategy can not be guaranteed.
Our ANM method can well handle these issues.
   It is worth mentioning that our ANM is an adaptive method, ANM can handle dynamic problems where the number
and the radius of the packing items can be changed, such as the online packing problems (Hokama, Miyazawa and
Schouery, 2016; Fekete and Hoffmann, 2017; Fekete, von Höveling and Scheffer, 2019; Lintzmayer, Miyazawa and
Xavier, 2019).

4.4. The Complexity Analysis of GBO
    We now provide the time and space complexity analysis of our GBO based on the BFGS optimization method.
    Time complexity. We analyze the time complexity of each iteration. From Algorithm 1 lines 6 to 15, it is
obvious that each iteration has 6 components, including the batch gradient 𝑔(𝒙𝑝 ) calculation, the batch step length
𝛼𝑝 calculation, the batch vector 𝒙𝑝 update, the batch Hessian matrix 𝑯 𝑝 update, the maintenance module ANM, and
the sum of the 𝑘-batch gradient norm. Since we adopt the efficient neighbor structure (He et al., 2018) (discussed in
Section 4.3), the energy and gradient functions can be executed in time complexity 𝑂(𝑛). So, the time complexity of
the batch gradient calculation, the step length calculation and the sum of 𝑘-batch gradient norm is 𝑂( 𝑘𝑛 ), 𝑂(𝛽 𝑘𝑛 ) and
𝑂(𝑛), respectively, where the constant 𝛽 approximates the recursion depth of line search approach. Each batch has
𝑛
𝑘
  packing items, so the size of the batch Hessian matrix is 𝑂(( 𝑘𝑛 )2 ). The batch vector update (Eq. (6)) and the batch
Hessian matrix update (Eqs. (8) and (9)) involve matrix and vector multiplication, so both of their time complexity
are 𝑂(( 𝑘𝑛 )2 ). We employ the scan line approach to construct the neighbor structure in the ANM module (discussed in
                                           √
Section 4.3), its time complexity is 𝑂(𝑛 𝑛) (using Voronoi diagram approach can gain a better time complexity of
                                                                                                 √
𝑂(𝑛 log 𝑛)). Finally, the time complexity of each iteration is 𝑂(𝑘( 𝑘𝑛 + 𝛽 𝑘𝑛 + ( 𝑘𝑛 )2 ) + 𝑛 + 𝑛 𝑛), which can be simplified
                √     2                           2
as 𝑂(𝛽𝑛 + 𝑛 𝑛 + 𝑛𝑘 ), and it becomes 𝑂(𝛽𝑛 + 𝑛𝑘 ) if the ANM module defers the maintaining process.
    Space complexity. The memory requirement of the GBO method is mainly used to store the 𝑘 batch Hessian
                                                                                                                   2
matrices. Therefore, the space complexity of the GBO method is 𝑂(𝑘( 𝑘𝑛 )2 ), which can be simplified as 𝑂( 𝑛𝑘 ).
                                                                                                    2           2
    As discussed above, our GBO method has lower time and space complexity (𝑂(𝛽𝑛 + 𝑛𝑘 ) and 𝑂( 𝑛𝑘 )) than the
classic BFGS method (𝑂(𝑛2 ) and 𝑂(𝑛2 )). It degenerates to the BFGS method when 𝑘 = 1.


5. Search Heuristic
     The algorithms for solving the PECC problem based on the elastic model can be divided into two phases. In the
first phase, the container radius is fixed, and the goal is to find a feasible solution or an infeasible solution with as
few overlaps as possible (i.e., the energy 𝐸 being as minimal as possible). In the second phase, the algorithms expand


  Algorithm 4: The framework for solving PECC
 1   Input: A number of unit circles 𝑛; A best-known container radius 𝑅𝑏 ; The cut-off time 𝑇𝑐𝑢𝑡
 2   Output: A feasible solution with the minimal container radius (𝒙∗ , 𝑅∗ )
      1: 𝒙∗ ← random_solution(𝑛, 𝑅𝑏 )
      2: 𝒙∗ ← GBO(𝒙∗ , 𝑅𝑏 )
      3: (𝒙∗ , 𝑅∗ ) ← adjust_container(𝒙∗ , 𝑅𝑏 )
      4: while time() ≤ 𝑇𝑐𝑢𝑡 do
      5:   𝑅 ← min(𝑅𝑏 , 𝑅∗ )
      6:   𝒙 ← SED(𝑛, 𝑅)
      7:   (𝒙, 𝑅) ← adjust_container(𝒙, 𝑅)
      8:   if 𝑅 < 𝑅∗ then
      9:       𝒙∗ ← 𝒙, 𝑅∗ ← 𝑅
     10:   end if
     11: end while
     12: return (𝒙∗ , 𝑅∗ )




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                              Page 11 of 26
                           Geometric Batch Optimization for the PECC Problem on Large Scale

or shrink the container radius to obtain a feasible solution with the container radius being as minimum as possible.
Starting from a random candidate solution, although we can obtain a feasible solution by employing the GBO method
(Section 4.1) to accomplish the first phase and employing the container adjustment method (Section 4.2) to accomplish
the second phase. However, the quality of the solution obtained in this way is still unsatisfactory.
    Through sufficient experiments, we observe that the quality of the final solution is directly impacted by the
solution obtained in the first phase. If the energy 𝐸(𝒙), corresponding to the overlapping area, of the obtained
solution in the first phase is large, the expanded difference of the radius adjustment in the second phase is also large.
On the other hand, if a feasible solution is found in the first phase, the radius can be shrunk in the second phase.
Therefore, a minimum energy solution discovered in the first phase is important to obtain a final high-quality feasible
solution. However, the elastic model converts the PECC problem to a non-convex optimization problem as discussed
in Section 3.2, and it is extremely difficult to find a global minimum solution. Therefore, we propose an efficient
Solution-space Exploring and Descent (SED) heuristic for the first phase to discover a solution with as minimum
energy as possible.

5.1. The Framework for Solving PECC
    We first introduce our algorithm framework, of which the pseudocode is depicted in Algorithm 4.
    Initially, the algorithm adopts the best-known radius (Specht, 2022) 𝑅𝑏 as the initial fixed container radius and
generates a random layout as the initial solution (line 1). The center (𝑥𝑖 , 𝑦𝑖 ) of each circle satisfies 𝑥𝑖 , 𝑦𝑖 ∈  (−𝑅𝑏 , 𝑅𝑏 )
( is denoted as the continuous uniform distribution). Then, the algorithm employs our GBO method (Section 4.1)
to minimize the energy 𝐸(𝒙∗ ) (line 2) to obtain an initial feasible solution 𝒙∗ (line 3) by employing the container
adjusting method (Section 4.2). Next, the algorithm performs an iterative process to improve the best recorded solution
until the cutoff time 𝑇𝑐𝑢𝑡 is reached (lines 4-11).
    At each iteration, the algorithm sets the target radius 𝑅 as min(𝑅𝑏 , 𝑅∗ ) (line 5), where 𝑅𝑏 is the best-known
radius 𝑅𝑏 and 𝑅∗ is the best feasible radius 𝑅∗ found so far. Then, it adopts our proposed SED heuristic (Section 5.2)
to discover a candidate solution 𝒙 with as low energy as possible (line 6). Subsequently, the algorithm computes a
new feasible solution by applying the container radius adjusting method to the candidate solution (line 7). If the new
feasible radius is smaller than the best recorded radius, indicating a better feasible solution is found, then the best
record solution is updated (lines 8-10). Finally, the algorithm returns the best recorded solution as the result.
    Note that our goal is to solve large scale instances, which is an incredibly big computational challenge. Using
the best-known radius instead of an approximate radius or a radius obtained by an initial method as the baseline can
reduce the computational difficulty, quickly discover a high-quality solution and improve the algorithm performance.
Therefore, it is an efficient quick-start method.

5.2. The Solution-Space Exploring and Descent Heuristic
    Our proposed SED heuristic aims to solve a problem described as follows. Given a fixed container radius, the
problem determines whether there is a feasible solution, and it is essentially a decision PECC problem. If SED
discovers a feasible solution, it returns the solution immediately; otherwise, it returns an infeasible solution with
the smallest energy during the search process. First, we define a new metric function 𝐽 , formulated as follows:

      𝐽 (𝒙) = ⌈− log10 𝐸(𝒙)⌉,

where function 𝐽 is the ceiling of the negative logarithm of the function 𝐸. It maps the energy 𝐸 to an integer. And
the value of function 𝐽 is applied to control the exploring number in the heuristic process.
    Now, we introduce our proposed SED heuristic depicted in Algorithm 5. Starting from a fixed container radius
𝑅, SED first generates a random configuration as the initial solution and minimizes the energy of the initial solution
𝒙 by adopting our GBO method (lines 1-2). Then, SED performs an iterative process to discover a feasible solution
(lines 4-18). At each iteration, SED obtains a value 𝑚 by function 𝐽 as the perturbing number (line 8), a candidate
solution set 𝑈 , |𝑈 | = 𝑚, is created where the candidate solution 𝒙′ in 𝑈 is obtained by perturbing the current operated
solution 𝒙 and minimizing energy 𝐸(𝒙′ ) by adopting GBO (lines 9-13). Then SED adopts a 𝑠𝑒𝑙𝑒𝑐𝑡 operator to choose
a candidate solution from set 𝑈 to replace the solution 𝒙. If the energy of new solution 𝒙 is smaller than the energy
of the best record solution 𝒙∗ , then 𝒙∗ is updated (lines 15-17). If the energy of 𝒙∗ is tiny enough, indicating a
feasible solution is discovered, SED returns the feasible solution 𝒙∗ immediately (lines 5-7), otherwise, SED returns
an infeasible solution with the smallest energy during the iteration process when reaching the maximum number of
iteration steps 𝑆𝑖𝑡𝑒𝑟 .

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                  Page 12 of 26
                         Geometric Batch Optimization for the PECC Problem on Large Scale

 Algorithm 5: SED(𝑛, 𝑅)
 1   Input: A number of unit circles 𝑛; A container radius 𝑅
 2   Output: A smallest energy solution found so far 𝒙∗
      1: 𝒙 ← random_solution(𝑛, 𝑅)
      2: 𝒙 ← GBO(𝒙, 𝑅)
      3: 𝒙∗ ← 𝒙
      4: for 𝑖 from 1 to 𝑆𝑖𝑡𝑒𝑟 do
      5:   if 𝐸(𝒙∗ ) ≤ 10−25 then
      6:       break
      7:   end if
      8:   𝑚 ← max(1, 𝐽 (𝒙)), 𝑈 ← ∅
      9:   for 𝑗 from 1 to 𝑚 do
     10:       𝒙′ ← perturbing(𝒙)
     11:       𝒙′ ← GBO(𝒙′ )
     12:       𝑈 ← 𝑈 ∪ {𝒙′ }
     13:   end for
     14:   𝒙 ← select(𝑈 )
     15:   if 𝐸(𝒙) < 𝐸(𝒙∗ ) then
     16:       𝒙∗ ← 𝒙
     17:   end if
     18: end for
     19: return 𝒙∗



   To obtain a perturbed solution 𝒙′ , we randomly shift the coordinate of the circles in the operated solution 𝒙 which
can be described as follows, 𝑥′𝑖 ← 𝑥𝑖 + 𝑟 and 𝑦′𝑖 ← 𝑦𝑖 + 𝑟 (1 ≤ 𝑖 ≤ 𝑛), where 𝑟 is a random number, 𝑟 ∈  (−0.8, 0.8).
   The strategy of the 𝑠𝑒𝑙𝑒𝑐𝑡 operator is described as follows:

                    ⎧
                    ⎪arg min 𝐸(𝒚),                    if min 𝐸(𝒚) < 𝐸(𝒙)
                                                         𝒚∈𝑈
       select(𝑈 ) = ⎨ 𝒚∈𝑈
                       (                           )
                    ⎪𝑃 𝑋 = 𝒚 ∣ 𝑝𝒚 = 𝑠𝑜𝑓 𝑡𝑚𝑎𝑥(𝐽 (𝒚)) , otherwise
                    ⎩


                                 exp(𝐽 (𝒚))
       𝑠𝑜𝑓 𝑡𝑚𝑎𝑥(𝐽 (𝒚)) = ∑                  ′
                                                .
                             𝒚 ′ ∈𝑈 exp(𝐽 (𝒚 ))

This operator first compares the candidate solution with the smallest energy in set 𝑈 to the current operated solution 𝒙.
If the energy of the candidate solution is smaller than the operated solution, the operator replaces the operated solution
as the candidate solution; otherwise, the operator selects a candidate solution from set 𝑈 according to the probability
of the softmax function.

6. Experiments
    For experiments, we first evaluate the performance of our proposed GBO method on the different number of
batches and different geometric partition methods, then we present the comparisons between the results and also give
the parameter studies.

6.1. Experimental Setup
    Our algorithm was implemented in C++ and compiled using g++ 5.4.0. Experiments were performed on a server
with Intel® Xeon® E5-2650 v3 CPU and 256 GBytes RAM, running the Linux OS. Due to the randomness, we run our
algorithm multiple times independently with different random seeds (CPU timestamps). To evaluate the performance
of our algorithm thoroughly, we select three instance scales as our benchmarks, described as follows:


Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                           Page 13 of 26
                         Geometric Batch Optimization for the PECC Problem on Large Scale

    • Moderate scale: 300 ≤ 𝑛 ≤ 320, for comparing with the state-of-the-art algorithm IDTS (Lai et al., 2022). We
      set 𝑘 = 3 for the batch number of GBO, 12 hours for cut-off time 𝑇𝑐𝑢𝑡 of our overall search. The algorithm
      performs 20 times independently, where the settings of cut-off time and performing time are the same as in the
      IDTS work.
    • Large scale I: 500 ≤ 𝑛 < 800, for comparing with the best-known results (Specht, 2022). We set 𝑘 = 5 for the
      batch number, 24 hours for cut-off time 𝑇𝑐𝑢𝑡 . The algorithm performs 10 times independently.
    • Large scale II: 800 ≤ 𝑛 ≤ 1000, for comparing with the best-known results (Specht, 2022). We set 𝑘 = 5 for
      the batch number, 48 hours for cut-off time 𝑇𝑐𝑢𝑡 . The algorithm performs 10 times independently.

    The rest of the parameters are consistently set as follows. The geometrical partition method is sector (Section 4.1),
the maximum iteration steps of GBO 𝑀𝑎𝑥𝐼𝑡𝑒𝑟 = 5000 (Section 4.1), and the maximum iteration steps of SED
𝑆𝑖𝑡𝑒𝑟 = 500 (Section 5.2). The parameters tuning and analysis are presented in Section 6.5.

6.2. Comparison on the Well-Studied Moderate Scale Instances
    We perform our proposed SED (3-batch GBO) algorithm and its variant SED (1-batch GBO) on the moderate
scale instances (300 ≤ 𝑛 ≤ 320). The comparisonal results of two algorithms with best-known results (Specht, 2022)
and IDTS (Lai et al., 2022) are shown in Table 1. Note that SED (1-batch GBO) only changes the number of batches
from 𝑘 = 3 to 𝑘 = 1 for SED (3-batch GBO), and the 1-batch GBO degenerates to the classic BFGS method.
    In Table 1, 𝑛 corresponds to the number of items in the instance, 𝑅∗ is for the best-known results from the
Packomania website (Specht, 2022) (download data 2022/10/1), followed by the best results of IDTS (Lai et al.,
2022). SED (1-batch GBO) and SED (3-batch GBO) correspond to the results of our methods: 𝑅𝑏𝑒𝑠𝑡 shows the best
result of 20 independent runs, 𝑅𝑎𝑣𝑔 shows the average result of 20 independent runs, 𝑅𝑏𝑒𝑠𝑡 − 𝑅∗ is the difference
between 𝑅𝑏𝑒𝑠𝑡 and 𝑅∗ (a negative value indicates an improved best result), 𝑅𝑅 is the ratio of better than or equal
to the best-known result 𝑅∗ , 𝐻𝑅 is the ratio of hitting the best value 𝑅𝑏𝑒𝑠𝑡 , and 𝑡𝑖𝑚𝑒 (𝑠) shows the average time of
obtaining a best solution in seconds. At the bottom of the table, “#Improve”, “#Equal” and “#Worse” indicates that for
our two algorithms SED (1-batch GBO) and SED (3-batch GBO), the number of instances that our algorithm obtained
better, equal, or worse result than the best of 𝑅∗ and IDTS.
    From Table 1, we can draw several conclusions as follows:
  (1) Our proposed heuristic SED with 1-batch GBO (i.e., classic BFGS) has 10 improved best results, 7 equal
      best results and 4 worse best results to IDTS on the 21 moderate scale instances. It demonstrates that SED
      outperforms IDTS. Note that the best-known results are same as IDTS, excluding 𝑛 = 320, and IDTS adopts
      L-BFGS as the optimization method, which is also a Quasi-Newton method.
  (2) SED (3-batch GBO) has 6 improved best results, 8 equal best results and 7 worse best results on the 21 moderate
      scale instances. The results show that the 3-batch GBO does not outperform the 1-batch GBO (classic BFGS
      method). It implies the multi-batch GBO does not work well on moderate scale instances.
  (3) From the ratio of hitting the best result 𝑅𝑏𝑒𝑠𝑡 (𝐻𝑅), there are few ratios of 𝐻𝑅 high than 10/20, the most of the
      ratios of HR are equal to 1/20. From the IDTS work, we also observe that all the ratios of 𝐻𝑅 in the IDTS work
      for 300 ≤ 𝑛 ≤ 320 are less than 6/20, and there are 14 ratios of 𝐻𝑅 equal to 1/20. These results demonstrate
      the moderate scale instances are well-studied and obtaining an improved best result is very difficult.

6.3. Comparison on Large Scale Instances
    For large scale instances, we select 𝑛 = 500, 510, 520, ..., 990, 1000 as our 51 large scale instances of the regular
number, then we randomly sample 30 irregular numbers from 500 ≤ 𝑛 < 800 and 20 irregular numbers from
800 ≤ 𝑛 ≤ 1000 as our 50 large scale instances of the irregular number. We perform SED (5-batch GBO) on
these instances, and the experimental results of the regular and irregular numbers are shown in Table 2 and Table 3,
respectively.
    In Tables 2 and 3, We provide 𝑛 for the number of items in the instances, 𝑅∗ for the best-known results from the
Packomania website (Specht, 2022) (download data 2022/10/1), 𝑅𝑏𝑒𝑠𝑡 for the best result of 10 independent runs, 𝑅𝑎𝑣𝑔
for the average result of 10 independent runs. 𝑅𝑏𝑒𝑠𝑡 − 𝑅∗ shows the difference between 𝑅𝑏𝑒𝑠𝑡 and 𝑅∗ (a negative value
indicates an improved best result). 𝑅𝑅 shows the ratio of equal or better than the best-known result 𝑅∗ , and 𝐻𝑅

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                          Page 14 of 26
                                                                                   Table 1: Comparison between the best-known results, IDTS and our proposed algorithms SED (1-batch GBO) and (5-batch GBO) on the 21 well-studied
                                                                                   moderate scale instances. The improved best results 𝑅𝑏𝑒𝑠𝑡 found by our proposed algorithms appear in bold.

                                                                                                                             SED (1-batch GBO)                                                       SED (3-batch GBO)
                                                                                    𝑛          𝑅∗             IDST
                                                                                                                             𝑅𝑏𝑒𝑠𝑡            𝑅𝑎𝑣𝑔           𝑅𝑏𝑒𝑠𝑡 − 𝑅∗   𝑅𝑅      𝐻𝑅      𝑡𝑖𝑚𝑒 (𝑠)   𝑅𝑏𝑒𝑠𝑡            𝑅𝑎𝑣𝑔           𝑅𝑏𝑒𝑠𝑡 − 𝑅∗   𝑅𝑅      𝐻𝑅      𝑡𝑖𝑚𝑒 (𝑠)
                                                                                    300        18.813153706   18.813153706   18.813157576     18.813191071   3.87E-06     0/20    1/20    26216      18.813189941     18.813198345   3.62E-05     0/20    12/20   33237
                                                                                    301        18.843463507   18.843463507   18.843463507     18.844498079   0.00E+00     2/20    2/20    26222      18.843463507     18.843551084   0.00E+00     1/20    1/20    38618
                                                                                    302        18.891782255   18.891782255   18.891781604     18.892064228   -6.51E-07    2/20    1/20    20792      18.891782255     18.892033313   0.00E+00     2/20    2/20    23987
                                                                                    303        18.929749153   18.929749153   18.929749153     18.930326363   0.00E+00     1/20    1/20    23549      18.929750618     18.930328723   1.47E-06     0/20    1/20    23652
                                                                                    304        18.964441751   18.964441751   18.964297557     18.964819754   -1.44E-04    3/20    1/20    24562      18.963620323     18.964664008   -8.21E-04    5/20    1/20    18852
                                                                                    305        19.001754565   19.001754565   19.001744832     19.002856526   -9.73E-06    1/20    1/20    24542      19.001726813     19.002734687   -2.78E-05    2/20    1/20    21922
                                                                                    306        19.030389407   19.030389407   19.031079983     19.031763629   6.91E-04     0/20    1/20    21131      19.030651242     19.031391719   2.62E-04     0/20    2/20    25226
                                                                                    307        19.060160922   19.060160922   19.061100857     19.062150163   9.40E-04     0/20    1/20    23579      19.060841920     19.061955433   6.81E-04     0/20    1/20    26981
                                                                                    308        19.104991437   19.104991437   19.109083748     19.110722905   4.09E-03     0/20    1/20    26804      19.107239953     19.109820607   2.25E-03     0/20    1/20    23291
                                                                                    309        19.142573165   19.142573165   19.141335827     19.143371324   -1.24E-03    5/20    1/20    25662      19.142625039     19.143620434   5.19E-05     0/20    1/20    24278
                                                                                    310        19.178928265   19.178928265   19.178560517     19.179857308   -3.68E-04    2/20    1/20    18906      19.178419320     19.179442843   -5.09E-04    6/20    1/20    24718
                                                                                    311        19.212365036   19.212365036   19.210669807     19.213148503   -7.17E-04    5/20    1/20    22109      19.210564074     19.212561780   -8.22E-04    4/20    2/20    21153
                                                                                    312        19.233585653   19.233585653   19.233585653     19.234863780   0.00E+00     1/20    1/20    23934      19.233585653     19.234529499   0.00E+00     4/20    4/20    30386
                                                                                    313        19.257103014   19.257103014   19.256994660     19.258015876   -1.08E-04    1/20    1/20    21251      19.257103014     19.258284406   0.00E+00     1/20    1/20    25457
                                                                                    314        19.286195141   19.286195141   19.286190236     19.286514591   -4.91E-06    4/20    4/20    25125      19.286190236     19.286476954   -4.91E-06    1/20    1/20    26386
                                                                                    315        19.302288067   19.302288067   19.302273991     19.302586043   -1.41E-05    17/20   11/20   25517      19.302273991     19.302286175   -1.41E-05    18/20   3/20    24488
                                                                                    316        19.334041754   19.334041754   19.334041754     19.334805176   0.00E+00     9/20    9/20    25370      19.334041754     19.334584281   0.00E+00     7/20    7/20    22840
                                                                                    317        19.367595672   19.367595672   19.367595672     19.367930543   0.00E+00     10/20   10/20   23713      19.367595672     19.367871121   0.00E+00     9/20    9/20    23129
                                                                                    318        19.391566091   19.391566091   19.391566091     19.391909306   0.00E+00     15/20   15/20   22836      19.391566091     19.391631572   0.00E+00     17/20   17/20   27084




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier
                                                                                    319        19.424277830   19.424277830   19.424277830     19.424920970   0.00E+00     15/20   15/20   18382      19.424277830     19.425310867   0.00E+00     12/20   12/20   24782
                                                                                    320        19.456230764   19.451649630   19.451583741     19.453206681   -4.65E-03    20/20   1/20    27713      19.451734176     19.454455527   -4.50E-03    19/20   3/20    30039
                                                                                    #Improve                                 10                                                                      6
                                                                                    #Equal                                   7                                                                       8
                                                                                    #Worse                                   4                                                                       7
                                                                                                                                                                                                                                                                             Geometric Batch Optimization for the PECC Problem on Large Scale




Page 15 of 26
                                                                                   Table 2: Comparison between the best-known results and SED (5-batch GBO) on the 51 large scale instances of the regular number. The improved best results
                                                                                   of 𝑅𝑏𝑒𝑠𝑡 and 𝑅𝑎𝑣𝑔 appear in bold.

                                                                                                               SED (5-batch GBO)                                                                               SED (5-batch GBO)
                                                                                    𝑛          𝑅∗                                                                                       𝑛      𝑅∗
                                                                                                               𝑅𝑏𝑒𝑠𝑡             𝑅𝑎𝑣𝑔            𝑅𝑏𝑒𝑠𝑡 − 𝑅∗   𝑅𝑅      𝐻𝑅     𝑡𝑖𝑚𝑒 (𝑠)                          𝑅𝑏𝑒𝑠𝑡             𝑅𝑎𝑣𝑔            𝑅𝑏𝑒𝑠𝑡 − 𝑅∗   𝑅𝑅      𝐻𝑅     𝑡𝑖𝑚𝑒 (𝑠)
                                                                                    500        24.1329376240   24.1312529426     24.1313788210   -1.68E-03    10/10   1/10   39561      800    30.4212133790   30.4198645288     30.4250741893   -1.35E-03    2/10    1/10   132389
                                                                                    510        24.4365629292   24.4210537570     24.4249135890   -1.55E-02    10/10   1/10   60259      810    30.6017659657   30.5956736421     30.6002028281   -6.09E-03    6/10    1/10   92738
                                                                                    520        24.6609522831   24.6258073657     24.6314124118   -3.51E-02    10/10   1/10   69426      820    30.7666908826   30.7489836784     30.7533477503   -1.77E-02    10/10   1/10   125921
                                                                                    530        24.8482376878   24.8455280225     24.8472603022   -2.71E-03    7/10    1/10   44648      830    30.9418117602   30.9297617239     30.9337956547   -1.21E-02    10/10   1/10   116582
                                                                                    540        25.0884399378   25.0855911217     25.0877127273   -2.85E-03    8/10    1/10   45255      840    31.1208576445   31.1194578886     31.1224527712   -1.40E-03    2/10    1/10   88791
                                                                                    550        25.3384484709   25.3342535707     25.3357628704   -4.19E-03    10/10   1/10   43783      850    31.3552353388   31.3432578820     31.3503256930   -1.20E-02    9/10    1/10   117055
                                                                                    560        25.5167889934   25.5122424885     25.5146796829   -4.55E-03    9/10    1/10   59827      860    31.5114350783   31.5070879233     31.5135835953   -4.35E-03    5/10    1/10   114252
                                                                                    570        25.7224085766   25.7134847249     25.7138542411   -8.92E-03    10/10   1/10   63852      870    31.6807723726   31.6747965238     31.6790476977   -5.98E-03    8/10    1/10   125813
                                                                                    580        25.9623218516   25.9511074848     25.9527379554   -1.12E-02    10/10   1/10   69140      880    31.8536138755   31.8463147084     31.8512855368   -7.30E-03    8/10    1/10   107682
                                                                                    590        26.2105443770   26.2025041590     26.2069156613   -8.04E-03    9/10    1/10   62246      890    32.0482429714   32.0438440391     32.0485774225   -4.40E-03    6/10    1/10   88801
                                                                                    600        26.4274162694   26.4176880113     26.4216830234   -9.73E-03    10/10   1/10   58273      900    32.2330843545   32.2199533426     32.2301042219   -1.31E-02    8/10    1/10   92746
                                                                                    610        26.6310600018   26.6227736610     26.6256150993   -8.29E-03    10/10   1/10   55976      910    32.3661258161   32.3658580937     32.3778653220   -2.68E-04    1/10    1/10   79106
                                                                                    620        26.8618811252   26.8431235737     26.8457652476   -1.88E-02    10/10   1/10   65063      920    32.5489524357   32.5347534619     32.5391088907   -1.42E-02    10/10   1/10   121667
                                                                                    630        27.0340036487   27.0525778864     27.0618588183   1.86E-02     0/10    1/10   44900      930    32.7013004786   32.6957714244     32.7024754370   -5.53E-03    7/10    1/10   119341
                                                                                    640        27.2419589706   27.2387282736     27.2421894917   -3.23E-03    6/10    1/10   59358      940    32.9143189848   32.9009771761     32.9052353405   -1.33E-02    10/10   1/10   109627
                                                                                    650        27.4458279070   27.4382286041     27.4422058882   -7.60E-03    10/10   1/10   71570      950    33.1232153862   33.1032839823     33.1093226461   -1.99E-02    10/10   1/10   136179
                                                                                    660        27.6680891671   27.6589093888     27.6622225342   -9.18E-03    10/10   1/10   69611      960    33.2729042511   33.2554924317     33.2639325269   -1.74E-02    10/10   1/10   111880
                                                                                    670        27.9068676439   27.9008215002     27.9030904780   -6.05E-03    10/10   1/10   65422      970    33.4357278371   33.4225668260     33.4271703375   -1.32E-02    10/10   1/10   114131
                                                                                    680        28.0951980575   28.0877536042     28.0903964995   -7.44E-03    10/10   1/10   63392      980    33.6049866471   33.5827959909     33.5885379042   -2.22E-02    10/10   1/10   154687
                                                                                    690        28.2458655422   28.2447186303     28.2638787279   -1.15E-03    5/10    1/10   55853      990    33.7831428326   33.7627857460     33.7698434841   -2.04E-02    10/10   1/10   132277
                                                                                    700        28.4958443164   28.4839888638     28.4877680865   -1.19E-02    10/10   1/10   59161      1000   33.9571409147   33.9457725483     33.9500559701   -1.14E-02    10/10   1/10   115406
                                                                                    710        28.7110433153   28.6956216568     28.7030160501   -1.54E-02    10/10   1/10   51258
                                                                                    720        28.8599089374   28.8547583326     28.8594487318   -5.15E-03    6/10    1/10   49792
                                                                                    730        29.0380889370   29.0368792578     29.0438783072   -1.21E-03    1/10    1/10   39872




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier
                                                                                    740        29.2501613747   29.2418887324     29.2440743866   -8.27E-03    10/10   1/10   61698
                                                                                    750        29.4806882503   29.4704602348     29.4725052490   -1.02E-02    10/10   1/10   51594
                                                                                    760        29.6611069657   29.6529205123     29.6626249312   -8.19E-03    5/10    1/10   45894
                                                                                    770        29.8480812041   29.8415580215     29.8451997650   -6.52E-03    9/10    1/10   47679
                                                                                    780        30.0188056551   30.0138757407     30.0164282850   -4.93E-03    9/10    1/10   59540
                                                                                    790        30.2195970061   30.2169949810     30.2208074501   -2.60E-03    4/10    1/10   44975
                                                                                    #Improve                   29                24                                                                            21                15
                                                                                                                                                                                                                                                                                        Geometric Batch Optimization for the PECC Problem on Large Scale




                                                                                    #Equal                     0                 0                                                                             0                 0
                                                                                    #Worse                     1                 6                                                                             0                 6




Page 16 of 26
                                                                                   Table 3: Comparison between the best-known results and SED (5-batch GBO) on the 50 large scale instances of the irregular number. The improved best results
                                                                                   of 𝑅𝑏𝑒𝑠𝑡 and 𝑅𝑎𝑣𝑔 appear in bold.

                                                                                                               SED (5-batch GBO)                                                                              SED (5-batch GBO)
                                                                                    𝑛          𝑅∗                                                                                       𝑛     𝑅∗
                                                                                                               𝑅𝑏𝑒𝑠𝑡             𝑅𝑎𝑣𝑔            𝑅𝑏𝑒𝑠𝑡 − 𝑅∗   𝑅𝑅      𝐻𝑅     𝑡𝑖𝑚𝑒 (𝑠)                         𝑅𝑏𝑒𝑠𝑡             𝑅𝑎𝑣𝑔            𝑅𝑏𝑒𝑠𝑡 − 𝑅∗   𝑅𝑅      𝐻𝑅     𝑡𝑖𝑚𝑒 (𝑠)
                                                                                    505        24.2933415273   24.2888919603     24.2901907584   -4.45E-03    10/10   1/10   41754      818   30.7297559207   30.7181308589     30.7214168182   -1.16E-02    10/10   1/10   96312
                                                                                    507        24.3570322874   24.3483441023     24.3499568679   -8.69E-03    10/10   1/10   56666      823   30.7951925938   30.7907479760     30.7953689952   -4.44E-03    7/10    1/10   102853
                                                                                    511        24.4539029279   24.4418315424     24.4443899780   -1.21E-02    10/10   1/10   65166      828   30.9026164659   30.8916045494     30.8945942840   -1.10E-02    10/10   1/10   129179
                                                                                    513        24.4944643498   24.4803487672     24.4836476996   -1.41E-02    10/10   1/10   53628      846   31.2210952935   31.2169756294     31.2320033828   -4.12E-03    7/10    1/10   77582
                                                                                    515        24.5352933431   24.5160216754     24.5234661213   -1.93E-02    10/10   1/10   64179      856   31.4404613224   31.4415597563     31.4451742962   1.10E-03     0/10    1/10   93393
                                                                                    517        24.5806822590   24.5688597754     24.5708937360   -1.18E-02    10/10   1/10   64080      861   31.5340220772   31.5286770943     31.5304575449   -5.34E-03    10/10   1/10   121885
                                                                                    539        25.0666591245   25.0644157476     25.0649834706   -2.24E-03    10/10   1/10   61702      872   31.7129332496   31.7028455621     31.7105946951   -1.01E-02    9/10    1/10   93714
                                                                                    547        25.2486649453   25.2630537774     25.2647995297   1.44E-02     0/10    1/10   39954      873   31.7297370844   31.7220224328     31.7251146977   -7.71E-03    9/10    1/10   95472
                                                                                    568        25.6768452576   25.6742746832     25.6747142118   -2.57E-03    9/10    2/10   63844      877   31.8055541388   31.7939196678     31.7991773790   -1.16E-02    10/10   1/10   123868
                                                                                    578        25.9195920293   25.9105502154     25.9141526168   -9.04E-03    10/10   1/10   57305      879   31.8366948955   31.8265208472     31.8312690574   -1.02E-02    10/10   1/10   110296
                                                                                    591        26.2324777614   26.2247762629     26.2300329942   -7.70E-03    8/10    1/10   63852      888   32.0091101899   31.9999805643     32.0056588693   -9.13E-03    10/10   1/10   93530
                                                                                    597        26.3542748538   26.3529416759     26.3549863877   -1.33E-03    5/10    1/10   48364      892   32.0884743996   32.0850195925     32.0888263967   -3.45E-03    5/10    1/10   118031
                                                                                    605        26.5365274699   26.5233023305     26.5261325786   -1.32E-02    10/10   1/10   72521      899   32.2281486010   32.2157001450     32.2200915147   -1.24E-02    10/10   1/10   130749
                                                                                    608        26.6012529572   26.5828030363     26.5852665616   -1.84E-02    10/10   1/10   73642      906   32.3065651824   32.3093777750     32.3220781255   2.81E-03     0/10    1/10   131780
                                                                                    613        26.6970192350   26.6806757801     26.6857073661   -1.63E-02    10/10   1/10   77051      911   32.3720611668   32.3751529633     32.3910623981   3.09E-03     0/10    1/10   90007
                                                                                    666        27.8222921562   27.8095070987     27.8149840911   -1.28E-02    10/10   1/10   62523      923   32.6092522621   32.5891329001     32.5927036033   -2.01E-02    10/10   1/10   117298
                                                                                    669        27.8866609962   27.8807032094     27.8832913945   -5.96E-03    10/10   1/10   50575      924   32.6279909132   32.6035557397     32.6110620319   -2.44E-02    10/10   1/10   131299
                                                                                    677        28.0279735048   28.0223920966     28.0294202784   -5.58E-03    3/10    1/10   50970      945   33.0363462137   33.0028997187     33.0183695018   -3.34E-02    10/10   1/10   138869
                                                                                    678        28.0545929509   28.0452214253     28.0486293696   -9.37E-03    10/10   1/10   70367      964   33.3393817195   33.3204312890     33.3287459497   -1.90E-02    10/10   1/10   115451
                                                                                    737        29.1885579873   29.1805602263     29.1837249288   -8.00E-03    10/10   1/10   59552      977   33.5337256998   33.5256191705     33.5286656634   -8.11E-03    10/10   1/10   117418
                                                                                    741        29.2673369351   29.2630224724     29.2656945026   -4.31E-03    8/10    1/10   52375
                                                                                    743        29.2989651471   29.2950962890     29.3006429415   -3.87E-03    7/10    1/10   51812
                                                                                    755        29.5864164492   29.5781420320     29.5813137994   -8.27E-03    10/10   1/10   66710
                                                                                    763        29.7207712331   29.7156118909     29.7208072730   -5.16E-03    6/10    1/10   47539




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier
                                                                                    764        29.7349505495   29.7321782541     29.7356589694   -2.77E-03    7/10    1/10   42529
                                                                                    774        29.9175478793   29.9123498351     29.9157783799   -5.20E-03    9/10    1/10   44943
                                                                                    778        29.9893439763   29.9830573225     29.9844978472   -6.29E-03    10/10   1/10   55350
                                                                                    781        30.0278742024   30.0301280216     30.0358959038   2.25E-03     0/10    1/10   65116
                                                                                    796        30.3480735601   30.3399225581     30.3447190305   -8.15E-03    10/10   1/10   49815
                                                                                    797        30.3755692236   30.3676919043     30.3715277628   -7.88E-03    9/10    1/10   46237
                                                                                    #Improve                   28                23                                                                           17                14
                                                                                                                                                                                                                                                                                       Geometric Batch Optimization for the PECC Problem on Large Scale




                                                                                    #Equal                     0                 0                                                                            0                 0
                                                                                    #Worse                     2                 7                                                                            3                 6




Page 17 of 26
                             Geometric Batch Optimization for the PECC Problem on Large Scale




               (a) 𝑛 = 302                              (b) 𝑛 = 304                              (c) 𝑛 = 305




               (d) 𝑛 = 309                              (e) 𝑛 = 310                              (f) 𝑛 = 311




               (g) 𝑛 = 313                              (h) 𝑛 = 314                               (i) 𝑛 = 315

Fig. 4: New improved solutions found by our proposed algorithm on the moderate scale instances (300 ≤ 𝑛 ≤ 320).
The circles are colored by various colors according to the number of contact circles, where two circles 𝑐𝑖 and 𝑐𝑗 are
considered to contact each other if the distance 𝑑(𝑐𝑖 , 𝑐𝑗 ) between two circle centers satisfies 𝑑(𝑐𝑖 , 𝑐𝑗 ) ≤ 2 + 10−10 .



shows the ratio of hitting the best value 𝑅𝑏𝑒𝑠𝑡 . The last column of 𝑡𝑖𝑚𝑒 (𝑠) shows the average time of obtaining a best
solution. At the bottom of the tables, “#Improve”, “#Equal” and “#Worse” show the number of instances for which
SED (5-batch GBO) obtained an improved, equal and worse result compared to the best-known results.
    From the results, we can draw conclusions as follows:



Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                Page 18 of 26
                            Geometric Batch Optimization for the PECC Problem on Large Scale

Table 4
Comparison between 1-batch GBO and 5-batch GBO on the 20 selected large scale instances. The best results of 𝑅′𝑏𝑒𝑠𝑡
and 𝑅𝑏𝑒𝑠𝑡 and the best results of 𝑅′𝑎𝑣𝑔 and 𝑅𝑎𝑣𝑔 appear in bold.
            SED (1-batch GBO)                             SED (5-batch GBO)
     𝑛
            𝑅′𝑏𝑒𝑠𝑡            𝑅′𝑎𝑣𝑔            𝑡𝑖𝑚𝑒 (𝑠)   𝑅𝑏𝑒𝑠𝑡             𝑅𝑎𝑣𝑔            𝑡𝑖𝑚𝑒 (𝑠)   𝑅𝑏𝑒𝑠𝑡 − 𝑅′𝑏𝑒𝑠𝑡   𝑅𝑎𝑣𝑔 − 𝑅′𝑎𝑣𝑔
     510    24.4854461416      24.5081091304   48297      24.4210537570     24.4249135890   60259      -6.44E-02        -8.32E-02
     610    26.6992073479      26.7150332110   58763      26.6227736610     26.6256150993   55976      -7.64E-02        -8.94E-02
     700    28.5679045373      28.5899851016   52511      28.4839888638     28.4877680865   59161      -8.39E-02        -1.02E-01
     740    29.2443717879      29.2477209407   56338      29.2418887324     29.2440743866   61698      -2.48E-03        -3.65E-03
     760    29.7452134712      29.7964289470   37391      29.6529205123     29.6626249312   45894      -9.23E-02        -1.34E-01
     780    30.1284909797      30.1454731784   36161      30.0138757407     30.0164282850   59540      -1.15E-01        -1.29E-01
     820    30.8413365443      30.8831339363   87278      30.7489836784     30.7533477503   125921     -9.24E-02        -1.30E-01
     890    32.1297407398      32.1758794016   80371      32.0438440391     32.0485774225   88801      -8.59E-02        -1.27E-01
     930    32.8196370611      32.8494260033   104544     32.6957714244     32.7024754370   119341     -1.24E-01        -1.47E-01
     960    33.3779501763      33.4204902518   100149     33.2554924317     33.2639325269   111880     -1.22E-01        -1.57E-01
     513    24.4833011422      24.4880257346   69720      24.4803487672     24.4836476996   53628      -2.95E-03        -4.38E-03
     568    25.6742746832      25.6750224839   58749      25.6742746832     25.6747142118   63844      0.00E+00         -3.08E-04
     608    26.5872589451      26.5914219805   63320      26.5828030363     26.5852665616   73642      -4.46E-03        -6.16E-03
     678    28.0507101923      28.0533386356   49399      28.0452214253     28.0486293696   70367      -5.49E-03        -4.71E-03
     737    29.2746711273      29.3098829156   46403      29.1805602263     29.1837249288   59552      -9.41E-02        -1.26E-01
     774    29.9122799819      29.9166270797   46759      29.9123498351     29.9157783799   44943      6.99E-05         -8.49E-04
     846    31.2194588931      31.2658324893   96767      31.2169756294     31.2320033828   77582      -2.48E-03        -3.38E-02
     877    31.7991261202      31.8019948228   105985     31.7939196678     31.7991773790   123868     -5.21E-03        -2.82E-03
     923    32.5978399965      32.6013970912   128923     32.5891329001     32.5927036033   117298     -8.71E-03        -8.69E-03
     964    33.3301336049      33.3336095372   110927     33.3204312890     33.3287459497   115451     -9.70E-03        -4.86E-03




  (1) SED (5-batch GBO) has 50 improved, 0 equal and 1 worse best results of the 51 large scale instances with
      regular number, and it has 45 improved, 0 equal and 5 worse best results of the 50 large scale instances
      with irregular number. The results demonstrate that our proposed SED (5-batch GBO) algorithm has excellent
      performance on large scale instances.

  (2) Most ratios of 𝑅𝑅 are greater than 5/10, and many of them are equal to 10/10. SED (5-batch GBO) had 39
      improved, 0 equal and 12 worse average results of the 51 large scale instances of the regular number, and it has
      37 improved, 0 equal and 13 worse average results of the 50 large scale instances of the irregular number. These
      results imply many runs of SED (5-batch GBO) are better than the best-known results. It also demonstrates that
      the algorithm has excellent performance on large scale instances.

  (3) All the ratios of HR are equal to 1/10 except 𝑛 = 568. It shows that obtaining the best results is extremely
      difficult, and the large scale PECC problem is computationally challenging.


6.4. Comparison of GBO (Multi-Batch) and Non-Batch
    We further do a comparison to evaluate the performance of our proposed GBO module on the large scale instances.
We randomly select 10 regular numbers and 10 irregular numbers for the large scale instances, then we perform SED
(5-batch GBO) and its variant SED (1-batch GBO), which only changes the batch number from 𝑘 = 5 to 𝑘 = 1 for
SED (5-batch GBO), on the 20 selected instances. Both algorithms run 10 times on each instance independently. The
results are shown in Table 4. Note that the 1-batch (non-batch) GBO degenerates to the classic BFGS optimization
method.
    In the table, we show 𝑛 for the number of instances, 𝑅′𝑏𝑒𝑠𝑡 and 𝑅′𝑎𝑣𝑔 for the best results and average results of 10
runs of SED (1-batch GBO) respectively, 𝑅𝑏𝑒𝑠𝑡 and 𝑅𝑎𝑣𝑔 for the best results and average results of 10 runs of SED
(5-batch GBO) respectively, 𝑡𝑖𝑚𝑒 (𝑠) for the average time of obtaining a best solution. 𝑅𝑏𝑒𝑠𝑡 − 𝑅′𝑏𝑒𝑠𝑡 and 𝑅𝑎𝑣𝑔 − 𝑅′𝑎𝑣𝑔
show the difference between two types of results represented where a negative value indicates SED (5-batch GBO)
yields better results than SED (1-batch GBO).
    From the results, we can observe that SED (5-batch GBO) has 18 best results better than SED (1-batch GBO), 1
best result equal to the latter and 1 best result worse. All the average results of SED (5-batch GBO) are better than
SED (1-batch GBO). It clearly demonstrates that the multi-batch method outperforms the non-batch method on large
scale instances, and our proposed GBO method has excellent performance on large scale instances.
    We also do a comparison of the runtime memory requirement of 5-batch GBO compared and non-batch (i.e.,
1-batch). We perform SED (5-batch GBO) and SED (1-batch GBO) for the instances 𝑛 = 500, 550, 600, ..., 1000, and


Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                        Page 19 of 26
                            Geometric Batch Optimization for the PECC Problem on Large Scale

we record the resident memory requirement during the two programs’ runtime. The comparisonal results are presented
in Figure 7.
    From the Figure 7, we observe that SED (5-batch GBO) requires lower resident runtime memory than SED (1-
batch GBO). In particular, 5-batch GBO only needs 60.96% to 64.00% runtime memory of 1-batch GBO (i.e., the
classic BFGS) for the instances 𝑛 = 500, 550, 600, ..., 1000. The memory ratio of 5-batch GBO to 1-batch GBO




              (a) 𝑛 = 505                              (b) 𝑛 = 610                             (c) 𝑛 = 650




              (d) 𝑛 = 710                              (e) 𝑛 = 774                             (f) 𝑛 = 828




              (g) 𝑛 = 890                              (h) 𝑛 = 940                             (i) 𝑛 = 990

Fig. 5: New improved solutions found by our algorithm for some representative instances on the large scale instances,
which have the closest packing in the central zone.




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                             Page 20 of 26
                            Geometric Batch Optimization for the PECC Problem on Large Scale




              (a) 𝑛 = 500                              (b) 𝑛 = 513                             (c) 𝑛 = 669




              (d) 𝑛 = 743                              (e) 𝑛 = 800                             (f) 𝑛 = 840




              (g) 𝑛 = 900                              (h) 𝑛 = 930                             (i) 𝑛 = 970

Fig. 6: New improved solutions found by our algorithm for some representative instances on the large scale instances,
which do not have the closest packing in the central zone.



decreases as 𝑛 increases. It demonstrates multi-batch GBO has advantage of the runtime memory requirement on
large scale instances.




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                             Page 21 of 26
                         Geometric Batch Optimization for the PECC Problem on Large Scale




Fig. 7: Comparison of the runtime resident memory requirement of SED (5-batch GBO) and SED (1-batch GBO) for
the instances 𝑛 = 500, 550, 600, ..., 1000, where the memory requirement is presented in MiB (i.e., MebiByte).




                              (a)                                                      (b)

             Fig. 8: Comparison between the four partitions of the GBO method on large scale instances.



6.5. Parameter Study
    Three parameters need to be tuned in our proposed algorithm, i.e., the batch strategy of the GBO partition
(Section 4.1), the batch number 𝑘 of GBO (Section 4.1) and the iteration step 𝑆𝑖𝑡𝑒𝑟 of SED heuristic (Section 5.2). In
this subsection, we give the experimental design and comparisonal results to determine a suitable parameter setting.
    On batch partition strategy. Since GBO is a continuous optimization method, it is not sensitive to a specific
instance, but it is sensitive to the instance scale. Therefore, we performed the four batch partition strategies (sector,
annulus, fence and random) on the 𝑛 = 1000 scale for the batch number from 𝑘 = 1 to 15, for investigating the
performance of the partition strategies on large scale instances. We run each of the settings independently for 1,000
times where each of the runs starts from a random initial layout and terminates at the energy be converged or the
maximal iteration step be reached (see in Algorithm 1), and the experimental results of the average time cost and the
average converged energy are shown in Figure 8. Note that the GBO method degenerates to the classic BFGS method
when the batch number 𝑘 = 1 (i.e., the non-batch method).
    Figure 8a illustrates the comparison of the average time cost of the four partitions where the X-axis indicates the
batch number 𝑘 and the Y-axis indicates the average time cost of 1,000 runs. From the figure we can observe that:




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                          Page 22 of 26
                        Geometric Batch Optimization for the PECC Problem on Large Scale




                              (a)                                                      (b)

Fig. 9: Comparison between the different settings on the batch number of the GBO method on different scale instances.


Table 5
The optimal batch number settings of GBO for 𝑛 = 100, 200, ..., 1000 compared with the non-batch setting.
  𝑛        𝑇𝑛𝑜𝑛. (𝑠)   𝑜𝑝𝑡.         𝑇𝑜𝑝𝑡. (𝑠)   Ratio(%)         𝑛         𝑇𝑛𝑜𝑛. (𝑠)   𝑜𝑝𝑡.      𝑇𝑜𝑝𝑡. (𝑠)      Ratio(%)
  100      0.09        𝑘=1          0.09        100.00%          600       7.17        𝑘=7       4.74           66.16%
  200      0.49        𝑘=1          0.49        100.00%          700       9.90        𝑘=5       5.48           55.32%
  300      1.23        𝑘=3          1.09        88.91%           800       13.35       𝑘=6       7.19           53.81%
  400      2.43        𝑘=3          1.89        77.78%           900       17.35       𝑘=5       8.73           50.33%
  500      4.04        𝑘=5          2.72        67.26%           1000      24.97       𝑘=6       11.46          45.89%



  (1) The time cost of random partition is significantly higher than non-batch (i.e., 𝑘 = 1), which implies applying
      the random partition on GBO makes the performance worse. Still, the average time cost of the random partition
      can be decreased as the batch number increases.
  (2) The three geometric batch partition strategies show a similar trend that the average time cost of the three
      strategies first decreases and then increases with the increasing batch number. The time cost of the annulus
      partition is slightly lower than non-batch when 𝑘 = 2 and 3, and it is higher than non-batch when 𝑘 ≥ 4, the
      time cost of the sector and fence partitions are all lower than non-batch when 𝑘 ≥ 2, and the sector partition has
      the best performance on the large scale.
  (3) By comparing the random partition with the sector, annulus and fence partitions, we see that a reasonable
      geometric partition strategy is necessary for solving the PECC problem instead of using the random partition,
      and the partition strategy directly impacts the performance of the GBO method.
    Figure 8b gives the comparison of the average converged energy of the four partitions where the X-axis indicates
the batch number 𝑘 and the Y-axis indicates the average converged energy 𝐸(𝒙) of 1,000 runs. From the figure we
can observe that the four average converged energies of most of the batch partition settings are slightly higher than
non-batch. However, most of these average converged energies locate between 0.62 and 0.66, and we consider the
difference as the experimental error because the difference between these average converged energies compared with
non-batch does not exceed 7%.
    According to the above discussion, the sector partition of the GBO method can obviously boost the convergence
speed, and there is no essential difference between sector partition and non-batch in the convergence result. Therefore,
we select the sector partition as the optimal setting of the batch strategy.
    On the batch number for various instance scales. To evaluate the performance of GBO on instances of different
scales, we perform the GBO method with sector partition on the scale 𝑛 = 100, 200, ..., 1000 for the batch number
from 𝑘 = 1 to 𝑘 = 15. We run each of the settings independently 1,000 times where each of the runs starts from

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                             Page 23 of 26
                          Geometric Batch Optimization for the PECC Problem on Large Scale

Table 6
Computational results and comparison of the parameter 𝑆𝑖𝑡𝑒𝑟 on the average result (𝑅𝑎𝑣𝑔 ) for 12 selected instances
where the best results obtained among the tested parameter values are presented in bold.
               𝑅𝑎𝑣𝑔
   𝑛 / 𝑆𝑖𝑡𝑒𝑟   100                200                300               400                500               600
   305         19.0029499894      19.0022928525      19.0023365854     19.0022767126      19.0027346869     19.0026950563
   316         19.3350583426      19.3348928193      19.3352210818     19.3347673471      19.3345842813     19.3346305894
   513         24.4871818937      24.4850574870      24.4858380045     24.4843239209      24.4836476996     24.4850158014
   568         25.6753984748      25.6746996472      25.6746268914     25.6749397842      25.6747142118     25.6746092173
   608         26.5878240724      26.5866285288      26.5860789992     26.5865544926      26.5852665616     26.5867207111
   678         28.0509853708      28.0507532028      28.0503173118     28.0509759006      28.0486293696     28.0498132121
   740         29.2459673340      29.2469306141      29.2451838453     29.2451220192      29.2440743866     29.2458209932
   774         29.9177876254      29.9143968413      29.9117005742     29.9143441746      29.9157783799     29.9153122016
   846         31.2425443239      31.2333675583      31.2304459481     31.2320033828      31.2275469287     31.2261977327
   877         31.8025272145      31.7999463301      31.8016759748     31.7975804456      31.7991773790     31.7998976078
   923         32.5975528505      32.5942894739      32.5935176512     32.5949283036      32.5927036033     32.5947280012
   964         33.3335745251      33.3300879802      33.3314171856     33.3271953322      33.3287459497     33.3265773865
   Average     27.6066126681      27.6044452780      27.6040300044     27.6037509847      27.6031336198     27.6035015425



a random initial layout and terminates at the energy being converged or the maximal iteration step is reached. The
experimental results of the average time cost are shown in Figure 9. Note that the GBO method degenerates to the
classic BFGS method when the batch number 𝑘 is set to 1.
    Figures 9a and 9b give the average time cost of the scale 𝑛 = 100, 200, ..., 500 and the scale 𝑛 = 600, 700, ..., 1000,
respectively. The X-axis indicates the batch number 𝑘 and the Y-axis indicates the average time cost of 1,000 runs.
Table 5 shows the comparison of the average time cost of the non-batch and optimal batch setting where the first
column of the table gives 𝑛 of the instances, 𝑇𝑛𝑜𝑛. and 𝑇𝑜𝑝𝑡. for the average time costs of the non-batch (i.e., 𝑘 = 1) and
                                                                                                   𝑇
the optimal batch setting, 𝑜𝑝𝑡. for the optimal setting of the batch number 𝑘 and Ratio (%) = 𝑇 𝑜𝑝𝑡. for the average time
                                                                                               𝑛𝑜𝑛.
cost ratio of the optimal batch to non-batch.
    From the two Figures 9a and 9b, and Table 5, we have the following observations:
  (1) The curves of the scale for 𝑛 = 100 and 𝑛 = 200 show that GBO does not work well on very small instances,
      applying the batch method will increase the convergence time, and GBO needs more time to obtain a converged
      solution as the batch number increases.
  (2) The curve of the scale for 𝑛 = 300 shows that GBO has a small advantage over the non-batch method on
      moderate scale instances. The average time costs of 𝑘 = 2, 3, 4 and 5 are slightly lower than non-batch (i.e.,
      𝑘 = 1). The curves of the scale 400 ≤ 𝑛 ≤ 1000 show that GBO can reduce the convergence time and boosts the
      convergence process significantly with a proper batch number setting. And the column of Ratio (%) of the table
      shows that the ratio will be reduced with the increasing scale, which indicates that GBO has more advantage of
      accelerating effect as the instance scale increases. The experimental results demonstrate that GBO has excellent
      performance on large scale instances.

  (3) The curves for the large scale instances, 500 ≤ 𝑛 ≤ 1000, show that the average time cost is increasing for batch
      number 𝑘 ≥ 8. It indicates that the batch number is not always better for larger values. And the optimal batch
      number 𝑘 of the large scale instances is located in interval [5, 7].
    According to the above discussion, we use the batch number 𝑘 = 3 as the optimal setting for the moderate
scale instances, 300 ≤ 𝑛 ≤ 320, and the batch number 𝑘 = 5 as the trade-off setting for the large scale instances,
500 ≤ 𝑛 ≤ 1000.
    On iteration step of SED. The rest of the parameters to be analyzed is the iteration step of SED. We perform
SED (5-batch GBO) with the several iteration steps 𝑆𝑖𝑡𝑒𝑟 = 100, 200, ..., 600 on the 12 instances, including 2, 6 and
4 randomly selected instances from the moderate scale, the large scale I and II respectively. The comparison of the
iteration steps is shown in Table 6. 𝑛 is the number of items in the instances, and columns 2 to 7 show the average
results, 𝑅𝑎𝑣𝑔 , of 10 or 20 runs (20 for the moderate scale and 10 for the large scale) for each tested iteration step 𝑆𝑖𝑡𝑒𝑟 ,
and the row of “Average” in the bottom shows the average value of the 12 instance results for each column.


Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                               Page 24 of 26
                               Geometric Batch Optimization for the PECC Problem on Large Scale

    Table 6 shows that the algorithm with 𝑆𝑖𝑡𝑒𝑟 = 500 obtains the best performance in terms of 𝑅𝑎𝑣𝑔 for 6 out of the
tested 12 instances, a much higher number than the other 5 tested iteration steps. It has also obtained the best average
value of the 12 instance results among the 6 tested iteration steps. As a result, we set the default value of 𝑆𝑖𝑡𝑒𝑟 to 500.


7. Conclusions
    In this paper, we aim to address the most representative packing problem, the packing equal circles in a circle
problem, on large scale. We propose a novel geometric batch optimization method that not only can significantly
speed up the continuous optimization process but also can reduce the memory requirement for finding a local minimum
packing configuration. We also propose a solution-space exploring and descent search heuristic accordingly for the
search to find a global minimum for the optimization of the overall packing. Besides, we propose an adaptive neighbor
object maintenance method, which handles some issues of the existing methods for maintaining the neighbor structure,
and it is suitable for dynamic packing problems and online packing problems. Extensive experiments on 21 moderate
instances (𝑛 = 300 to 320) and 101 sampled large-scale instances (𝑛 = 500 to 1000) demonstrate the effectiveness and
efficiency of our proposed methods. Our algorithm could often find new and better packing results than the current
best records. In addition, our geometric batch optimization, heuristic search and adaptive maintenance methods are
generic and can be used for other optimization problems. In future work, we will extend our methods for solving other
packing problems.


References
Addis, B., Locatelli, M., Schoen, F., 2008. Disk packing in a square: a new global optimization approach. INFORMS Journal on Computing 20,
   516–524.
Akeb, H., Hifi, M., M’Hallah, R., 2010. Adaptive beam search lookahead algorithms for the circular packing problem. International Transactions
   in Operational Research 17, 553–575.
Akeb, H., Hifi, M., M’Hallah, R., 2009. A beam search algorithm for the circular packing problem. Computers & Operations Research 36,
   1513–1528.
Baldi, M.M., Manerba, D., Perboli, G., Tadei, R., 2019. A generalized bin packing problem for parcel delivery in last-mile logistics. European
   Journal of Operational Research 274, 990–999.
Birgin, E.G., Sobral, F., 2008. Minimizing the object dimensions in circle and sphere packing problems. Computers & Operations Research 35,
   2357–2375.
Burke, E., Hellier, R., Kendall, G., Whitwell, G., 2006. A new bottom-left-fill heuristic algorithm for the two-dimensional irregular packing
   problem. Operations Research 54, 587–601.
Carrabs, F., Cerrone, C., Cerulli, R., 2014. A tabu search approach for the circle packing problem, in: 17th International Conference on Network-
   Based Information Systems, IEEE. pp. 165–171.
Castillo, I., Kampas, F.J., Pintér, J.D., 2008. Solving circle packing problems by global optimization: numerical results and industrial applications.
   European Journal of Operational Research 191, 786–802.
Chen, M., Tang, X., Song, T., Zeng, Z., Peng, X., Liu, S., 2018. Greedy heuristic algorithm for packing equal circles into a circular container.
   Computers & Industrial Engineering 119, 114–120.
Demaine, E.D., Fekete, S.P., Lang, R.J., 2010. Circle packing for origami design is hard. arXiv preprint arXiv:1008.1224 .
Epstein, L., van Stee, R., 2005. Online square and cube packing. Acta Informatica 41, 595–606.
Fekete, S.P., Hoffmann, H.F., 2017. Online square-into-square packing. Algorithmica 77, 867–901.
Fekete, S.P., von Höveling, S., Scheffer, C., 2019. Online circle packing, in: Algorithms and Data Structures: 16th International Symposium, WADS
   2019, Edmonton, AB, Canada, August 5–7, 2019, Proceedings 16, Springer. pp. 366–379.
Fodor, F., 1999. The densest packing of 19 congruent circles in a circle. Geometriae Dedicata 74, 139–145.
Fodor, F., 2000. The densest packing of 12 congruent circles in a circle. Beiträge Algebra Geom 41, 401–409.
Fodor, F., 2003. The densest packing of 13 congruent circles in a circle. Beiträge zur Algebra und Geometrie 44, 431–440.
Goldberg, M., 1971. Packing of 14, 16, 17 and 20 circles in a circle. Mathematics Magazine 44, 134–139.
Görtler, J., Schulz, C., Weiskopf, D., Deussen, O., 2017. Bubble treemaps for uncertainty visualization. IEEE Transactions on Visualization and
   Computer Graphics 24, 719–728.
Graham, R., Peck, C., 1968. Sets of points with given maximum separation (problem e1921). The American Mathematical Monthly 75, 80–81.
Graham, R.L., Lubachevsky, B.D., Nurmela, K.J., Östergård, P.R., 1998. Dense packings of congruent circles in a circle. Discrete Mathematics
   181, 139–154.
Grosso, A., Jamali, A., Locatelli, M., Schoen, F., 2010. Solving the problem of packing equal and unequal circles in a circular container. Journal
   of Global Optimization 47, 63–81.
Hartman, T., Mazáč, D., Rastelli, L., 2019. Sphere packing and quantum gravity. Journal of High Energy Physics 2019, 1–68.
He, K., Mo, D., Ye, T., Huang, W., 2013. A coarse-to-fine quasi-physical optimization method for solving the circle packing problem with
   equilibrium constraints. Computers & Industrial Engineering 66, 1049–1060.
He, K., Tole, K., Ni, F., Yuan, Y., Liao, L., 2021. Adaptive large neighborhood search for solving the circle bin packing problem. Computers &
   Operations Research 127, 105140.

Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                                    Page 25 of 26
                               Geometric Batch Optimization for the PECC Problem on Large Scale

He, K., Ye, H., Wang, Z., Liu, J., 2018. An efficient quasi-physical quasi-human algorithm for packing equal circles in a circular container.
   Computers & Operations Research 92, 26–36.
Hifi, M., M’Hallah, R., 2004. Approximate algorithms for constrained circular cutting problems. Computers & Operations Research 31, 675–694.
Hifi, M., M’Hallah, R., 2007. A dynamic adaptive local search algorithm for the circular packing problem. European Journal of Operational
   Research 183, 1280–1294.
Hifi, M., Paschos, V.T., Zissimopoulos, V., 2004. A simulated annealing approach for the circular cutting problem. European Journal of Operational
   Research 159, 430–448.
Hifi, M., Yousef, L., 2019. A local search-based method for sphere packing problems. European Journal of Operational Research 274, 482–500.
Hokama, P., Miyazawa, F.K., Schouery, R.C., 2016. A bounded space algorithm for online circle packing. Information Processing Letters 116,
   337–342.
Huang, W., Li, Y., Akeb, H., Li, C., 2005. Greedy algorithms for packing unequal circles into a rectangular container. Journal of the Operational
   Research Society 56, 539–548.
Huang, W., Xu, R., 1999. Two personification strategies for solving circles packing problem. Science in China Series E: Technological Sciences
   42, 595–602.
Huang, W., Ye, T., 2011. Global optimization method for finding dense packings of equal circles in a circle. European Journal of Operational
   Research 210, 474–481.
Huang, W.Q., Li, Y., Jurkowiak, B., Li, C.M., Xu, R.C., 2003. A two-level search strategy for packing unequal circles into a circle container, in:
   International Conference on Principles and Practice of Constraint Programming, Springer. pp. 868–872.
Huang, W.Q., Li, Y., Li, C.M., Xu, R.C., 2006. New heuristics for packing unequal circles into a circular container. Computers & Operations
   Research 33, 2125–2142.
Kravitz, S., 1967. Packing cylinders into cylindrical containers. Mathematics Magazine 40, 65–71.
Lai, X., Hao, J.K., Yue, D., Lü, Z., Fu, Z.H., 2022. Iterated dynamic thresholding search for packing equal circles into a circular container. European
   Journal of Operational Research 299, 137–153.
Leao, A.A., Toledo, F.M., Oliveira, J.F., Carravilla, M.A., Alvarez-Valdés, R., 2020. Irregular packing problems: A review of mathematical models.
   European Journal of Operational Research 282, 803–822.
Leung, J.Y., Tam, T.W., Wong, C.S., Young, G.H., Chin, F.Y., 1990. Packing squares into a square. Journal of Parallel and Distributed Computing
   10, 271–275.
Lintzmayer, C.N., Miyazawa, F.K., Xavier, E.C., 2019. Online circle and sphere packing. Theoretical Computer Science 776, 75–94.
Liu, J., Zhang, K., Yao, Y., Xue, Y., Guan, T., 2016. A heuristic quasi-physical algorithm with coarse and fine adjustment for multi-objective
   weighted circles packing problem. Computers & Industrial Engineering 101, 416–426.
López, C.O., Beasley, J.E., 2011. A heuristic for the circle packing problem with a variety of containers. European Journal of Operational Research
   214, 512–525.
Lü, Z., Huang, W., 2008. Perm for solving circle packing problem. Computers & Operations Research 35, 1742–1755.
Martello, S., Monaci, M., Vigo, D., 2003. An exact approach to the strip-packing problem. INFORMS Journal on Computing 15, 310–319.
Melissen, H., 1994. Densest packings of eleven congruent circles in a circle. Geometriae Dedicata 50, 15–25.
Miyazawa, F.K., Wakabayashi, Y., 2003. Cube packing. Theoretical Computer Science 297, 355–366.
Mladenović, N., Plastria, F., Urošević, D., 2005. Reformulation descent applied to circle packing problems. Computers & Operations Research 32,
   2419–2434.
Murakami, H., Higo, Y., Kusumoto, S., 2015. Clonepacker: A tool for clone set visualization, in: IEEE 22nd International Conference on Software
   Analysis, Evolution, and Reengineering (SANER), IEEE. pp. 474–478.
Nurmela, K.J., Östergård, P.R., 1997. Packing up to 50 equal circles in a square. Discrete & Computational Geometry 18, 111–120.
Pirl, U., 1969. Der mindestabstand von n in der einheitskreisscheibe gelegenen punkten. Mathematische Nachrichten 40, 111–124.
Rao, Y., Wang, P., Luo, Q., 2021. Hybridizing beam search with tabu search for the irregular packing problem. Mathematical Problems in
   Engineering 2021.
Reis, G.E., 1975. Dense packing of equal circles within a circle. Mathematics Magazine 48, 33–37.
Ren-Pu, G., Powell, M.J., 1983. The convergence of variable metric matrices in unconstrained optimization. Mathematical Programming 27,
   123–143.
Specht, E., 2022. Packomania website: http://www.packomania.com .
Stoyan, Y., Yaskov, G., 2014. Packing unequal circles into a strip of minimal length with a jump algorithm. Optimization Letters 8, 949–970.
Stoyan, Y., Yaskov, G., Romanova, T., Litvinchev, I., Yakovlev, S., Cantú, J.M.V., 2020. Optimized packing multidimensional hyperspheres: a
   unified approach. Mathematical Biosciences and Engineering 17, 6601–6630.
Wang, W., Wang, H., Dai, G., Wang, H., 2006. Visualization of large hierarchical data by circle packing, in: Proceedings of the SIGCHI Conference
   on Human Factors in Computing Systems, pp. 517–520.
Wang, Y., Wang, Y., Sun, J., Huang, C., Zhang, X., 2019. A stimulus–response-based allocation method for the circle packing problem with
   equilibrium constraints. Physica A: Statistical Mechanics and its Applications 522, 232–247.
Yanchevskyi, I., Lachmayer, R., Mozgova, I., Lippert, R.B., Yaskov, G., Romanova, T., Litvinchev, I., 2020. Circular packing for support-free
   structures. EAI Endorsed Transactions on Energy Web 7, e3–e3.
Zhao, C., Jiang, L., Teo, K.L., 2020. A hybrid chaos firefly algorithm for three-dimensional irregular packing problem. Journal of Industrial &
   Management Optimization 16, 409.
Zhao, H., She, Q., Zhu, C., Yang, Y., Xu, K., 2021. Online 3d bin packing with constrained deep reinforcement learning, in: Proceedings of the
   AAAI Conference on Artificial Intelligence, pp. 741–749.




Jianrong Zhou, Kun He, Joingzi Zheng, Chu-Min Li: Preprint submitted to Elsevier                                                     Page 26 of 26
