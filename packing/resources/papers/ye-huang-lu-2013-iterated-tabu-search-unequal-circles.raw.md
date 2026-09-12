                                            Iterated Tabu Search Algorithm for Packing Unequal
                                                             Circles in a Circle

                                                             Tao Yea,b , Wenqi Huanga , Zhipeng Lüa,∗
arXiv:1306.0694v1 [math.OC] 4 Jun 2013




                                            a
                                             School of Computer Science and Technology, Huazhong University of Science and
                                                                  Technology, Wuhan, 430074, China
                                         b
                                           Department of Mathematics, Simon Fraser University Surrey, Central City, 250-13450
                                                        102nd AV, Surrey, British Columbia, V3T 0A3, Canada




                                         Abstract

                                         This paper presents an Iterated Tabu Search algorithm (denoted by ITS-
                                         PUCC) for solving the problem of Packing Unequal Circles in a Circle. The
                                         algorithm exploits the continuous and combinatorial nature of the unequal
                                         circles packing problem. It uses a continuous local optimization method
                                         to generate locally optimal packings. Meanwhile, it builds a neighborhood
                                         structure on the set of local minimum via two appropriate perturbation
                                         moves and integrates two combinatorial optimization methods, Tabu Search
                                         and Iterated Local Search, to systematically search for good local minima.
                                         Computational experiments on two sets of widely-used test instances prove
                                         its effectiveness and efficiency. For the first set of 46 instances coming from
                                         the famous circle packing contest and the second set of 24 instances widely
                                         used in the literature, the algorithm is able to discover respectively 14 and
                                         16 better solutions than the previous best-known records.
                                         Key words: Packing, Circle packing, Global optimization, Tabu search,
                                         Iterated local search


                                            ∗
                                             Corresponding Author. Tel: 86-27-87543885. Email address: yeetao@gmail.com (T.
                                         Ye), wqhuang@hust.edu.cn(W. Huang), zhipeng.lui@gmail.com (Z. Lü)


                                         Preprint submitted to Elsevier                                    November 27, 2024
1. Introduction

   Given n circles and a container of predetermined shape, the circle packing
problem is concerned with a dense packing solution, which can pack all the
circles into the smallest container without overlap. The circle packing prob-
lem is a well-known challenge in discrete and computational geometry, and it
arises in various real-world applications in the field of packing, cutting, con-
tainer loading, communication networks and facility layout (Castillo et al.,
2008). In the field of global optimization, the circle packing problem is a
natural and challenging test bed for evaluating various global optimization
methods.
   This paper focuses on solving a classic circle packing problem, the Pack-
ing Unequal Circles in a Circle (PUCC) problem. As indicated in previous
papers (Addis et al., 2008b; Grosso et al., 2010; Hifi and M’Hallah, 2009),
the PUCC problem has an interesting and important characteristic that it
has a both continuous and combinatorial nature. It has continuous nature
because the position of each circle is chosen in R2 . The combinatorial nature
is due to the following two facts: (1) A packing pattern is composed of n
circles, and shifting a circle to a different place would produce a new packing
pattern; (2) The circles have different radiuses, and swapping the positions
of two different circles may result in a new packing pattern.
   In this paper, we pay special attention to the continuous and combi-
natorial characteristic of the PUCC problem. We propose an algorithm
which integrates two kinds of optimization techniques: A continuous local
optimization procedure which minimizes overlaps between circles and pro-
duces locally optimal packing patterns, and an Iterated Tabu Search (ITS)
procedure which exploits the combinatorial nature of the problem and in-


                                       2
telligently uses two appropriate perturbation moves to search for globally
optimal packing patterns.
   The proposed algorithm is assessed on two sets of widely used test in-
stances, showing its effectiveness and efficiency. For the first set of 46 in-
stances coming from the famous circle packing contest, the algorithm is able
to discover 14 better solutions than the previous best-known records. For
the second set of 24 instances widely used in the literature, the algorithm
can improve 16 best-known solutions in a reasonable time.
   The rest of this paper is organized as follows. Section 2 briefly reviews the
most related literature. Section 3 formulates the PUCC problem. Section
4 describes the details of the proposed algorithm. Section 5 assesses the
performance of the algorithm through extensive computational experiments.
Section 6 analyzes some key ingredients of the algorithm to understand
the source of its performance. Finally, Section 7 concludes this paper and
proposes some suggestions for future work.


2. Related Literature

   Over the last few decades, the circle packing problem has received con-
siderable attention in the literature. The simplest and most widely studied
cases are the packing of equal circles in a square or in a circle. Though
researchers have spent significant effort on the two problems, only a few
packings (up to tens of circles) have been proved to be optimal by purely an-
alytical methods and computer-aided proving methods (Szabó et al., 2007;
Graham et al., 1998). A second category of research aims at finding the
best possible packings without optimality proofs. Following this spirit, var-
ious heuristic approaches have been proposed, including: Billiard simulation


                                      3
(Graham et al., 1998), minimization of energy function (Nurmela and Östergård,
1997), nonlinear programming approaches (Birgin et al., 2005, 2010), Popu-
lation Basin Hopping method (Addis et al., 2008a; Grosso et al., 2010), for-
mulation space search heuristic algorithm (López and Beasley, 2011), quasi-
physical global optimization method (Huang and Ye, 2011), greedy vacancy
search method (Huang and Ye, 2010) and so on. With these approaches,
best-known packings for up to thousands of circles have been found, which
are reported and continuously updated on the Packomania website (Specht,
2013).
   There are also a number of papers devoted to the unequal circle pack-
ing problem. Most previous papers on the unequal circle packing problem
can be classified into two categories: Constructive approaches and global
optimization approaches. The constructive approaches build a packing by
successively placing a circle into the container. These approaches usually in-
clude two important components: A placement heuristic, which determines
several candidate positions for a new circle in the container, and a tree
search strategy, which controls the tree search process and avoids exhaus-
tive enumeration of the solution space. The widely used placement heuris-
tics include the principle of Best Local Position (BLP) (Hifi and M’Hallah,
2004, 2007, 2008; Akeb and Hifi, 2010) and the Maximum Hole Degree
(MHD) rule (Huang et al., 2005, 2006; Lü and Huang, 2008; Akeb et al.,
2009). The tree search strategies include the self look-ahead search strategy
(Huang et al., 2005, 2006), Pruned-Enriched-Rosenbluth Method (PERM)
(Lü and Huang, 2008), beam search algorithm (Akeb et al., 2009) and the
hybrid beam search looking-ahead algorithm (Akeb and Hifi, 2010).
   The global optimization approaches formulate the unequal circle packing
problem as a mathematical programming problem, then the task becomes to

                                      4
find the global minimum of a mathematical model. These kind of approaches
include the quasi-physical quasi-human algorithm by Wang et al. (2002), the
Tabu Search and Simulated Annealing hybrid approach (Zhang and Deng,
2005), the Population Basin Hopping algorithm (Addis et al., 2008b; Grosso et al.,
2007, 2010), the GP-TS algorithm by Huang et al. (2012a), the Iterated
Local Search algorithm by Huang et al. (2012b), the Formulation Search
Space algorithm by López and Beasley (2012) and the Iterated Tabu Search
algorithm by Fu et al. (2013) for the circular open dimension problem.
    For the circle packing problem, there also exist many important literature
not mentioned here. Interested readers are referred to the review articles by
Castillo et al. (2008) and Hifi and M’Hallah (2009), the book by Szabó et al.
(2007) and the Packomania website (Specht, 2013).


3. Problem Formulation

    Given n disks, each having radius ri (i = 1, 2, · · · , n), the PUCC problem
consists in finding a dense packing solution, which can pack all n disks into
the smallest circular container of radius R without overlap. We designate
the container center as the origin of the cartesian coordinate system and
locate disk i (i = 1, 2, . . . , n) by the coordinate position of its center (xi , yi ).
The PUCC problem can be formulated as:

                                   minimize R, s.t. :
                                      q
                                        x2i + yi2 + ri ≤ R                          (1)
                     q
                         (xi − xj )2 + (yi − yj )2 ≥ ri + rj                        (2)

where i, j = 1, 2, · · · , n; i 6= j. Eq.(1) ensures that each disk is completely in
the container and Eq.(2) guarantees that no overlap exists between any two


                                           5
disks. Note that, this problem can also be formulated in other ways, see for
example Birgin et al. (2005) and Grosso et al. (2010).
     A packing solution is described by two variables: The radius of the
container R and the packing pattern denoted by the positions of all n
disks X = (x1 , y1 , x2 , y2 , · · · , xn , yn ). The infeasibility of a packing can be
caused by two kinds of overlaps: Overlaps between two disks and overlaps
between a disk and the exterior of the container. We define the overlapping
depth between disks i and j (i, j = 1, 2, · · · , n; i 6= j) as:
                                          q
              oij = max {0, ri + rj −          (xi − xj )2 + (yi − yj )2 }.        (3)

and the overlapping depth between disk i (i = 1, 2, · · · , n) and the exterior
of the container as:
                                       q
                       o0i = max {0,       x2i + yi2 + ri − R}.                    (4)

     Adding all squares of overlapping depth together, we get a penalty func-
tion measuring overlaps of a packing
                                           n−1
                                           X      n
                                                  X
                             E(X, R) =                 o2ij .                      (5)
                                           i=0 j=i+1

Thus, a packing (X, R) is feasible (non-overlapping) if and only if E(X, R) =
0.
     Sometimes, we fix the radius of the container at a constant value R and
the penalty function becomes

                                ER (X) = E(X, R).                                  (6)

Note that, finding a packing pattern X with ER (X) = 0 corresponds to
solving the following circle-packing decision problem (Birgin et al., 2005):


                                           6
Given a circular container with fixed radius R, find out a feasible pattern
X which can pack all the circles into the container without overlap.
   Our original PUCC problem aims to find the smallest container of radius
R∗ and a corresponding non-overlapping packing pattern X. In practice, the
PUCC problem can be solved as a serial of circle-packing decision problems
with descending R (Huang and Ye, 2010). The main steps are as follows:

(1) Let R be an upper bound of R∗ . Initialize R with a relatively large
    number such that all circles can be easily packed into the container of
    radius R without overlap.
(2) Set R ← R and launch an algorithm to find a feasible X with ER (X) =
    0 (i.e., to solve the corresponding circle-packing decision problem).
(3) Tighten the packing (X, R), i.e, to minimize R while keeping X basically
    unchanged. This step can be achieved using various approaches, like the
    simple bisection method described in Huang and Ye (2011), the simple
    penalty method described in Huang and Ye (2010), the standard local
    optimization solver SNOPT adopted by Addis et al. (2008b) and the
    more sophisticated augmented Lagrangian method (Andreani et al. ,
    2007; Birgin and Sobral , 2008; Birgin and Martı́nez , 2009). After this
    step, we can usually obtain a better (at least not worse) packing (X ′ , R′ ).
(4) Set R ← R′ and go to step 2. The loop of steps 2-4 is ended until a
    certain termination criterion (like time limit) is satisfied.

   In the rest of this paper, we will first introduce an Iterated Tabu Search
algorithm to solve the circle-packing decision problem, and then use it to
search for dense packing solutions for the PUCC problem in the computa-
tional experiments section.



                                       7
4. Iterated Tabu Search Algorithm

   This section describes the Iterated Tabu Search (ITS) procedure for solv-
ing the circle-packing decision problem. As indicated in Section 3, this prob-
lem can be transformed to an unconstraint global optimization problem:

                             minimize     ER (X).                          (7)

This subproblem is very difficult because there exist enormous local minima
in the solution space. Grosso et al. (2010) have shown that, even for the
equal circle packing problem, the number of local minima tends to increase
very quickly with the number of circles. For the more complex unequal circle
packing problem, it is very possible that the number of local minima will be
significantly larger.
   The main rationale behind the ITS procedure is as follows: (1) Each
local minimum of ER (X) corresponds to a packing pattern of n disks in
the container. (2) If we perturb the current local minimizer X by swapping
the positions of two different disks (or shifting the position of one disk) and
then call the LBFGS procedure to minimize ER (X), we can obtain a new
local minimizer. (3) By systematically using the two perturbation moves,
swap and shift, we can obtain a set of neighboring local minima from the
current local minima. Furthermore, we can build a neighborhood structure
on the set of local minima of ER (X). (4) Since there is a neighborhood
structure, some Stochastic Local Search methods (Hoos and Stützle, 2005),
such as Tabu Search (Glover and Laguna, 1998) and Iterated Local Search
(Lourenço et al., 2003), can be employed to search for good local minima.
   The outline of the ITS procedure is given in Algorithm 1. The proce-
dure performs searches on the set of local minima of ER (X) and follows an


                                      8
Iterated Local Search schema. In Algorithm 1, we run the ITS procedure
in a multi-start fashion. At each run, the algorithm starts from a randomly
generated local minimum (steps 2-3). It goes through the SwapT abuSearch
procedure (step 4) and reaches a swap-optimal local minimum (which will
be defined in the next section). Then the search explores the solution space
by repeatedly escaping from local optima traps (step 6) and moving to an-
other local optimum (step 7). This process is repeated until the best-found
solution has not been improved during the last P erturbDepth iterations.

     Input: Radiuses of n disks, radius of the container R
     Output: A feasible packing pattern X of n disks in the container
 1 while not time out do

 2      X ← Randomly scatter n disks into the container ;
 3      X ← Minimize ER (X) using LBFGS ;
 4      X ← SwapTabuSearch(X) ;                      /* local search */
 5      repeat
 6         Y ← ShiftPerturb (X) ;                            /* perturb */
 7         Y ← SwapTabuSearch(Y ) ;                  /* local search */
 8         if ER (Y ) ≤ ER (X) then
 9             X ←Y;
10         end
11      until the best-found solution has not been improved in the last
        PerturbDepth iterations;
12 end

                  Algorithm 1: The ITS procedure




                                      9
4.1. The SwapTabuSearch Procedure
   In the SwapT abuSearch procedure, we build a neighborhood structure
on the set of local minima of ER (X). A swap move performed on a packing
pattern X is defined as swapping the positions of two disks with different ra-
diuses and then locally minimizing ER (X). For two local minima of ER (X),
X and X ′ , we say X ′ is a neighbor of X if and only if X ′ can be reached by
performing a swap move on X. The neighborhood of X is a set containing
all the neighbors of X. We use ER (X) as the evaluation function, and a
local minimum X of ER (X) is called a swap-optimal local minimum if it
has better solution quality than all its neighbors (or it cannot be improved
via any swap move).
   Totally, there are n ∗ (n − 1) possible swap moves for a packing pattern
with n disks. However, for efficiency purposes, a restricted neighborhood is
used in this paper. We first sort the disks in a nondecreasing order w.r.t.
their radius values, such that for disks i and j, ri ≤ rj if i < j. A swap
move can only be performed on a pair of disks with neighboring radius
values. That is to say, disk i can only exchange positions with disks i − 1
and i + 1. Then, there are in total n − 1 swap moves and a local minimum
X has at most n − 1 different neighbors.
   The SwapT abuSearch procedure follows a Tabu Search strategy. At
the beginning of the search, the tabu list is empty and all swap moves are
admissible. At each step, the algorithm chooses a best admissible move
which leads to the best nontabu solution. The aspiration criterion is used
such that a tabu move can be selected if it generates a solution that is better
than the best-found solution. Once a move is selected, it is declared tabu for
the next T abuT enure steps. The procedure is repeated until the best-found
solution has not been improved with the last T abuDepth steps. The sketch

                                      10
of the SwapT abuSearch procedure is presented in Algorithm 2.

     Input: An initial local minimum of ER (X)
     Output: A swap-optimal minimum of ER (X)
 1 repeat

 2      choose a best candidate swap move mv;
 3      perform move mv ;
 4      declare move mv tabu for T abuT enure iterations;
 5 until The best-found solution has not been improved in the last

     T abuDepth iterations;
 6 return the best-found solution X ∗ ;

            Algorithm 2: The SwapTabuSearch procedure



4.2. The ShiftPerturb Procedure

     In the Shif tP erturb procedure, the algorithm escapes a local optimum
by a series of shift moves. A shift move performed on a packing pattern X is
defined as shifting the position of a randomly chosen disk to a random place
in the container and then locally minimizing ER (X). The number of times
the shift move is performed is controlled by a parameter P erturbStrength.
As pointed out in previous research (Lourenço et al., 2003), the perturbation
strength is very important for Iterated Local Search. If it is too weak, the
local search may undo the perturbation and the search will be confined in a
small area of the solution space. On the contrary, if the perturbation is too
strong, the Iterated Local Search will behave like random restart, leading
to poor performance. After preliminary computational tests, we choose the
value of P erturbStrength to be a random integer from [1, n/8].



                                     11
                                 Table 1: Parameter settings
    Parameter          Section     Description                         Value
    T abuT enure       4.1         Tabu tenure of Tabu Search          n/5 + rand(0,10)
    T abuDepth         4.1         Improvement cutoff of Tabu Search   10*n
    P erturbStrength   4.2         Perturbation strength of ITS        rand(1,n/8)
    P erturbDepth      4           Improvement cutoff of ITS           10*n




5. Performance Assessment

   In this section, we assess the performance of the proposed algorithm
through computational experiments on two sets of widely-used test instances.
We also compare the results of our algorithm with some state-of-the-art al-
gorithms in the literature.

5.1. Experimental Protocol

   The algorithm is programmed in C++ and complied using GNU G++.
All computational experiments are carried out on a personal computer with
4Gb memory and a 2.8GHz AMD Phenom II X6 1055T CPU. Table 1 gives
the settings of the four important parameters of the algorithm. Note that
all the computational results are obtained without special tuning of the
parameters, i.e., all the parameters used in the algorithm are fixed for all
the tested instances.

5.2. Test Instances

   Two sets of test problems are considered, in total constituting 70 in-
stances. The first set comes from the famous circle packing contest (see
http://www.recmath.org/contest/CirclePacking/index.php). This con-
test started on October 2005 and ended on January 2006. During this pe-
riod, the participants were invited to propose densest packing solutions to

                                             12
pack n(n = 5, 6, . . . , 50) circles, each having radius ri = i(i = 1, 2, . . . , n)
into the smallest containing circle without overlap. 155 groups from 32
countries took part in the contest and submitted a total of 27490 tentative
solutions. After the contest, these results were further improved respectively
by Müller et al. (2009), Eckard Specht (Specht, 2013), Zhanghua Fu et al.
(Specht, 2013). Currently, all the best-known records are published and
continuously updated on the Packomania website.
   The second set of instances consists of 24 problem instances first pre-
sented by Huang et al. (2005). These instances are frequently used in the
literature by many authors, see for example Huang et al. (2006); Akeb et al.
(2009); Akeb and Hifi (2010). The size of these instances ranges from n = 10
to 60. A detailed description of these instances can be found in Huang et al.
(2005).

5.3. Computational results on the circle packing contest instances

   For the circle packing contest instances, researchers usually pay more at-
tention on the solution quality. Especially during the contest, people mostly
focus on finding better solutions than the best-known records and rarely con-
sider the computational resource used. After researchers have solved these
instances using various approaches and large amount of computational re-
source, this set of instances now becomes a challenging benchmark to test
the discovery capability (Grosso et al., 2007) of a new algorithm. Therefore,
our first experiment concentrates on searching for high-quality solutions.
For each run of each instance, we usually set the time limit to 24 hours, run
the algorithm multiple times and record the best-found solutions.
   Table 2 gives the computational results. Column 1 lists the best-known
records on the Packomania website. Columns 2-4 respectively report the


                                        13
solution difference between some top reference results and the best-known
records. These include: the best results found by Addis et al. (2008b) (who
is the champion of the circle packing contest) using PBH algorithm, the
best records obtained by all the participants in the contest, the best results
found by Müller et al. (2009) using Simulated Annealing (SA) algorithm.
Column 5 gives the solution difference between our results and the best-
known records. The results indicated in bold are better than the best-known
ones. Table 2 omits the results for n = 5, 6, . . . , 20, because our results and
all the reference results are the same on these instances. Note that, our
program generates solutions with a maximum error on the distances of 10−9 .
We have sent all the improved results to Eckard Specht. Using his own local
optimization solver, he has processed our results to a high precision (10−28 )
and published them on the Packomania website.
   Table 3 summarizes the comparison of our results with the reference re-
sults. The rows better, equal and worse respectively denote the number of
instances for which the proposed algorithm gets solutions that are better,
equal and worse than each reference result. Table 3 shows that the proposed
algorithm is able to discover a number of better solutions than the previ-
ous best reference results, demonstrating its efficacy in finding high-quality
solutions. In fact, we also tested the proposed algorithm on the larger in-
stances of n = 51, 52, . . . , 100. Some preliminary experiments show that the
algorithm can improve almost all previous best-known results. Interested
readers can refer to the Packomania website.
   All the reference algorithms in Table 2 concentrate on finding high-
quality solutions and do not reveal their computational statistics. In order
to further evaluate the proposed algorithm in terms of search efficiency, we
conduct additional experiments to compare the proposed algorithm with two

                                       14
    Table 2: Comparison of solution quality on the circle packing contest instances
                                Solution difference (i.e., this result - best-known)
       n    Best-Known
                              PBH        Contest record           SA          ITS-PUCC
      21   62.55887709     0.00118149            0                 0               0
      22   66.76028624          0                0                 0               0
      23   71.19946160          0                0                 0               0
      24   75.74914258     0.00356154       0.00356154             0               0
      25   80.28586443          0                0                 0               0
      26   84.98993916     0.11634365       0.08646206             0        -0.01174810
      27   89.75096268     0.07861113       0.04121888             0               0
      28   94.52587710     0.17998508       0.02410937        0.0006594            0
      29   99.48311156     0.02920634       0.02920634             0               0
      30   104.54036376    0.20743552       0.03819132        0.0008052            0
      31   109.68204275    0.08990423       0.08990423        0.0004137     -0.05280209
      32   114.79981466    0.06562367       0.06562367        0.0411343            0
      33   120.06565963    0.15129751       0.15129751        0.0001869            0
      34   125.36693920    0.24548366       0.06656255             0          0.07661871
      35   130.84907874    0.31742394       0.30727589        0.0685492            0
      36   136.49212355    0.04277728       0.04277728        0.0001210     -0.18421273
      37   141.93243775    0.32389631       0.24254278        0.1189377     -0.14870433
      38   147.45211646    0.53945928       0.40557489        0.0047288       0.16654317
      39   153.30070280    0.30312533       0.25459839        0.0793799     -0.00009525
      40   159.17977260    0.39413040       0.30925227        0.0026352     -0.12653569
      41   164.88704217    0.40486751       0.40486751        0.1498584            0
      42   170.89531908    0.03044253       0.03044253        0.0000083     -0.11479840
      43   176.82574386    0.41388066       0.24859621        0.2256308     -0.02750344
      44   183.04328935    0.32678190       0.13277222        0.0559354     -0.11226929
      45   189.19513856    0.48403531       0.44030054        0.0077934     -0.02405842
      46   195.52636407    0.38439932       0.38439932        0.0000710     -0.17039157
      47   201.72792559    0.50009381       0.45768615             0        -0.05939136
      48   208.09015930    0.54578742       0.54578742             0        -0.04513139
      49   214.29205550    0.36989651       0.36989651        0.0033920     -0.00983298
      50   220.56540026    0.52435233       0.52435233        0.0350184       0.50085590




Table 3: Summary of comparison of solution quality on the 30 circle packing contest
instances with n = 21, 22, . . . , 50
                            PBH     Contest record     SA    Best-known
                  Better     27          25            20        14
                  Equal      3            4             7        13
                  Worse      0            1             3         3




                                            15
recently published algorithms in a time-equalized basis. For each instance
of n = 5, 6, . . . , 32, we set the maximum time limit to 10000 seconds. We
record the best-found solution and the elapsed time when it is first detected
by the algorithm. To reduce the impact of randomness, each instance is
independently solved for 10 times.
   Table 4 gives the computational results. Columns 2-3, 4-5 respectively
list the best-found solution and the needed computing time of TS/NP algo-
rithm and FSS algorithm. Columns 2 and 3 are extracted from Al-Mudahka et al.
(2010) where the algorithm ran on a computer with a Pentium IV, 2.66 Ghz
CPU and 512Mb RAM. Columns 4 and 5 are extracted from López and Beasley
(2012). Their experiments were done on a computer with a Intel(R) Core(TM)
i5-2500 3.30 GHz CPU and 4.00 GB RAM. Columns 6-8 give the compu-
tational statistics of our algorithm, including the best-found solution, the
number of hit times and the averaged computing time to detect the best-
found solution.
   Columns 6-8 show that, for all the 28 instances, the proposed algorithm
can reach (or improve) the previous best-known records listed in Table 2
within the given time limit. Especially for n ≤ 25, the algorithm can ro-
bustly detect the best-known records in a short time. When compared with
the two reference algorithms, one observes that the proposed algorithm can
usually find better solutions within the time limit. These results provide
evidence of the search efficiency of ITS-PUCC algorithm.

5.4. Computational results on the NR instances

   This section tests the proposed algorithm on the 24 NR instances. For
each instance, we set the time limit to 10000 seconds, and record the best-
found solution and the elapsed time when it is first detected by the algo-


                                     16
     Table 4: Comparison of search efficiency on the circle packing contest instances
               TS/NP                      FSS                        ITS-PUCC
n
        R            time(s)      R             time(s)     R             #hits    time(s)
5       9.001398     426          9.00139775    461         9.00139774    10/10    1
6       11.05704     686          11.0570404    667         11.05704039   10/10    1
7       13.46211     1511         13.46211068   721         13.46211067   10/10    1
8       16.22175     2551         16.22174668   1028        16.22174667   10/10    1
9       19.39734     4051         19.23319391   1404        19.2331939    10/10    1
10      22.34516     5760         22.00019301   1438        22.00019301   10/10    1
11      24.96063     2094         24.96063429   1820        24.96063428   10/10    1
12      28.67863     3548         28.37138944   2299        28.37138943   10/10    1
13      32.00719     4054         31.54586702   2905        31.54586701   10/10    1
14      35.41261     6146         35.09564714   2970        35.09564714   10/10    2
15      39.00243     6696         38.83799682   3904        38.8379955    10/10    1
16      42.92185     9684         42.45811644   4917        42.45811643   10/10    6
17      46.77237     10168        46.34518193   5264        46.29134211   10/10    24
18      50.65635     14312        50.20889346   6224        50.11976262   10/10    23
19      55.02744     14925        54.36009421   7349        54.24029359   10/10    39
20      59.04547     19825        58.48047359   7517        58.40056747   10/10    82
21      63.49768     5923         63.00078332   8924        62.55887709   10/10    190
22      68.10291     6636         66.96471591   10762       66.76028624   10/10    127
23      72.70501     7209         71.69822657   13018       71.1994616    10/10    268
24      76.49105     8552         76.1231197    13004       75.74914258   10/10    704
25      81.56595     11409        80.8168236    15569       80.28586443   10/10    633
26      86.43809     12062        85.487438     18320       84.97819106   9/10     3538
27      91.15366     13657        90.93173506   18544       89.75096268   7/10     5287
28      96.34813     14364        95.6406414    21931       94.5258771    10/10    1568
29      101.7251     15185        100.7200313   25455       99.48311156   7/10     2915
30      107.1161     20745        105.8881722   25658       104.5403638   5/10     4538
31      111.8996     21424        111.077126    29973       109.6292407   2/10     8551
32      117.6701     22781        116.6122668   34445       114.7998147   4/10     3885




                                           17
rithm. Each instance is solved for 10 times from different randomly gener-
ated starting points.
   The computational results are presented in Table 5. Column 1 gives
the instance name. Columns 2-3, 4-5, 6-7, 8-9, respectively present the
best-found solution and the needed computing time of A1.5 Algorithm in
Huang et al. (2006), Beam Search (BS) algorithm in Akeb et al. (2009), Al-
gorithm 2 in Akeb et al. (2010) and GP-TS algorithm in Huang et al.
(2012a). Columns 10-12 give the computational statistics of our algorithm,
including the best-found solution, the number of hit times and the averaged
computing time for detecting the best-found solution. In experiments, our
program generates solutions with a maximum error on the distance of 10−9 .
However, in order to keep consistent with previous papers, we report in
Table 5 the results with 4 significant digits after the decimal point.
   Table 5 demonstrates that, for all the tested 24 instances, the proposed
algorithm can find 16 better solutions than the best results found by the
references algorithms (as indicated in bold in the table). For the other
8 instances, it can reach the best-known solutions efficiently and robustly.
These results further provide evidence of the competitiveness of the proposed
algorithm.


6. Algorithm Analysis

   In this section, we turn our attention to analyzing the two most impor-
tant ingredients of the proposed algorithm: the SwapT abuSearch procedure
and the Shif tP erturb procedure.




                                     18
                         Table 5: Comparison of search efficiency on the 24 NR instances
                  A1.5                BS               Algorithm 2           GP-TS                  ITS-PUCC
     Instance
                R      time(s)   R          time(s)   R         time(s)   R        time(s)   R          #hits   time(s)
     NR10-1     99.89 1          99.8851    19        99.8851   1         99.8851  1         99.8851    10/10   1
     NR11-1     60.71 1          60.7100    28        60.7100   2         60.7100  2         60.7100    10/10   1
     NR12-1     65.30 6          65.4752    4         65.0338   2483      65.0245  1         65.0244    10/10   1
     NR14-1     113.84 2         114.2919   151       113.5588 17860      113.5588 252       113.5588 10/10     16
     NR15-1     38.97 25         38.9441    59        38.9170   46283     38.9158  88        38.9114 10/10      57
     NR15-2     38.85 6          38.8380    1179      38.8380   9832      38.8380  166       38.8380    10/10   1
     NR16-1     143.44 71        143.7176   139       143.4339 235240     143.3798 128       143.3798 10/10     126
     NR16-2     128.29 44        128.0539   28        127.9021 80890      127.7174 6         127.6978 10/10     2
     NR17-1     49.25 30         49.2069    234       49.1977   6080      49.1874  258       49.1873    10/10   359
     NR18-1     197.40 88        198.2791   8         197.1038 111970     197.0367 76        196.9826 10/10     58
19




     NR20-1     125.53 39        125.6316   764       125.1525 199945     125.1178 13        125.1178 10/10     229
     NR20-2     122.21 318       122.2192   351       122.0296 150495     121.9944 120       121.7887 10/10     780
     NR21-1     148.82 683       149.1351   638       148.3462 132080     148.3373 647       148.0968 10/10     488
     NR23-1     175.47 1229      175.4058   3072      174.9491 58430      174.8524 283       174.3425 8/10      3259
     NR24-1     138.38 2339      138.2778   510       138.0520 37140      138.0044 433       137.7591 10/10     3706
     NR25-1     190.47 4614      190.1855   1493      189.4715 37053      189.3736 533       188.8314 7/10      3091
     NR26-1     246.75 1019      247.5464   583       246.4179 18620      246.0853 40        244.5743 10/10     795
     NR26-2     303.38 5164      303.2102   11240     302.5896 190600     302.0687 4         300.2631 10/10     179
     NR27-1     222.58 4436      222.4896   3750      221.6389 177000     221.4882 2505      220.9393 5/10      6037
     NR30-1     178.66 1365      178.0102   5045      177.6473 160700     178.0093 10439     177.5125 3/10      8678
     NR30-2     173.70 1078      173.4359   9217      173.2215 155050     173.1641 502       172.9665 8/10      574
     NR40-1     357.00 12109     357.0695   22140     355.6587 158700     355.1307 112       352.4517 4/10      2253
     NR50-1     380.00 9717      378.5854   21400     378.0044 186000     377.9105 12462     377.9080 2/10      8945
     NR60-1     522.93 13256     521.2739   13975     519.8494 116270     519.4515 60        518.6792 1/10      9657
6.1. Analysis of The SwapTabuSearch Procedure
   The SwapT abuSearch procedure is a key component of the proposed
algorithm, which enables the algorithm to intelligently examines the neigh-
boring packing patterns through swap moves. In order to make sure the
Tabu Search strategy makes a meaningful contribution, we conduct exper-
iments to compare the Tabu Search strategy with a simple local search
strategy called Steepest Descent (Hoos and Stützle, 2005).
   For comparison, we use the same neighborhood structure as described
in Section 4.1 and implement the Steepest Descent strategy as follows. At
each iteration, the search examines each neighbor of the current solution
and find out the best neighbor with the least objective value ER . If the best
neighbor X ′ is better than the current solution X, i.e., ER (X ′ ) ≤ ER (X),
then the search moves to X ′ and proceeds to the next iteration; otherwise
the search stops and declares reaching a local minimum.
   A representative instance NR15-2 is chosen as our test bed. This in-
stance is nontrivial. Though many previous papers have tested it, only
few state-of-the-art algorithms, like Beam Search (Hifi and M’Hallah, 2008),
PBH(Addis et al., 2008b; Grosso et al., 2010), SA(Müller et al., 2009) can
obtain the optimal packing pattern. We set the radius of container R to the
best-known value, randomly generate initial X and call both algorithms to
minimize ER (X).
   We run both algorithms 1000 times from different randomly generated
starting points and record in Table 6 respectively the best-found solution
(Column 2), the average solution quality (Column 3), the average number
of search steps for each local search (Column 4) and the average elapsed
time for each local search (Column 5). From Table 6, we observe that, the
Tabu Search strategy shows clear advantage over Steepest Descent strategy.

                                     20
Table 6: Computational statistics of Tabu Search strategy and Steepest Descent strategy
from 1000 randomly generated initial packings

 Search Strategy    Best-found solution   Average solution quality   Search steps   Time (s)
   Tabu Search           0.000000                0.000000               1269           2
 Steepest Descent        0.092194                2.085742                 7            0




Each time, the Tabu Search strategy can find the global minimum from a
randomly generated starting point, while the Steepest Descent strategy fails
for all 1000 runs. In fact, we try to run the Steepest Descent strategy from
100000 randomly generated starting points, it still cannot find the global
minimum.
    The main reason for the difference is that, with the Steepest Descent
strategy, the search is easily trapped in poor local minimum. As shown
in Table 6, the average number of search step for each local search is only
7. However, with the Tabu Search strategy, the search can escape from
low-quality local minimum trap and proceed to explore the neighboring
area. Figure 1 shows a typical search trajectory of Tabu Search, compared
with the search trajectory of Multistart Steepest Descent. In Figure 1,
both algorithms start from the same initial solution, a packing pattern with
ER = 8.77845794. After 7 search steps, both of them encounter a local min-
imum with ER = 1.37297106. At this time, the Steepest Descent strategy is
trapped, the search has to proceed from a new randomly generated initial
solution. However, with the Tabu Search strategy, the search is able to es-
cape from the local minimum with ER = 1.3729106, proceed to examine the
neighboring area, and finally find the global minimum at the 362th search
step.



                                            21
         30                                              Multistart Steepest Descent
                                                                Tabu Search

         25


         20
ER (X)




         15


         10


         5


         0

               0     50    100   150       200         250      300        350
                                   Search steps



Figure 1: Comparison of search trajectories between Multistart Steepest Descent and
Tabu Search


         These experiments reveal that, the Tabu Search strategy helps to per-
form an intensified examination around the incumbent packing pattern and
makes possible discovering those hidden good solutions. The same exper-
iments have been performed on several other instances, leading to similar
observation.

6.2. Analysis of the ShiftPerturb Procedure

         In order to verify the effectiveness of the Shif tP erturb procedure, we
conduct experiments to compare the proposed ITS algorithm with a Multi-
start Tabu Search algorithm. In the Multistart Tabu Search algorithm, when
the SwapT abuSearch procedure finishes, the search proceeds from a new
randomly generated initial solution. The parameter setting of SwapT abuSearch
is the same as listed in Table 1. We test the Multistart Tabu Search algo-
rithm on the 28 circle packing instances with 5 ≤ n ≤ 32. Each instance is
solved for 10 times. The time limit for each run is also set to 10000 seconds.



                                                  22
    The computational results show clear advantage of ITS algorithm over
Multistart Tabu Search algorithm. For the instances of 5 ≤ n ≤ 24, the
Multistart Tabu Search algorithm can also detect the best-known records,
but with lower success rates and relatively longer time. Nevertheless, for
each instance of 25 ≤ n ≤ 32, the Multistart Tabu Search algorithm fails
to detect the best-known solution for all the 10 runs within the given time
limit.
    We conjecture the superior of ITS over Multistart Tabu Search may
be explained from the following two aspects.     First, the Iterated Local
Search framework helps the search to perform a more intensified exam-
ination around the incumbent solution, making it possible to repeatedly
discover better solutions. This is supported by our observations from com-
putational experiments that, with the ITS algorithm, the search can usually
generate a sequence of local minima with descending objective value. The
final solution obtained by one run of ITS is usually much better than that
found by the first run of SwapT abuSearch. Second, the shift move in the
Shif tP erturb procedure is complementary to the swap move, enabling the
search to reach some packing patterns which are hard to detect only through
swap moves.


7. Conclusion and Future Work

    In this paper, we have presented a heuristic global optimization algo-
rithm for solving the unequal circle packing problem. The proposed al-
gorithm uses a continuous local optimization method to generate locally
optimal packings and integrates two combinatorial optimization methods,
Tabu Search and Iterated Local Search, to systematically search for good


                                    23
local minima. The efficiency and effectiveness of the algorithm have been
demonstrated by computational experiments on two sets of widely used test
instances. For the 46 challenging circle packing contest instances and the 24
widely-used NR instances, the algorithm can respectively improve 14 and
16 previous best-known records in a reasonable time.
   There are two main directions for future research. On the one hand,
the presented algorithm can be further improved by incorporating other
advanced strategies. Possible improvements include the following: First, re-
duce the solution space by first ignoring several smaller disks and only look-
ing for optimal packing pattern of the remaining larger disks. The smaller
disks can be inserted into the holes after the larger disks have been placed
into the container. This strategy was proposed in Addis et al. (2008b) and
had proved to be very useful. Second, test other Stochastic Local Search
methods, such as Simulated Annealing used in Müller et al. (2009), Vari-
able Neighborhood Search (Hoos and Stützle, 2005) and so on. Third, the
proposed algorithm is a single-solution based method. It is possible to
strengthen the robustness of the algorithm by employing some population-
based methods, like the Population Basin Hopping method proposed in
Grosso et al. (2007).
   On the other hand, the ideas behind the proposed algorithm can also
be applied to other hard global optimization problems. Many real-world
global optimization problems, such as the cluster optimization problem in
computational chemistry (Ye et al., 2011) and the protein folding problem
in computational biology (Huang et al., 2006), have the same characteristics
as the unequal circle packing problem, i.e., they have both a continuous and
combinatorial nature. For these kinds of problems, it is possible to build a
neighborhood structure on the set of local minima via appropriate perturba-

                                     24
tion moves, and then to employ some advanced combinatorial optimization
methods to systematically search for good local minima.


Acknowledgement

   We thank the anonymous reviewers whose detailed and valuable sug-
gestions have significantly improved the manuscript.      We thank Eckard
Specht for processing our data and publishing it on the Packomania website.
This work was supported by National Natural Science Foundation of China
(Grant No. 61100144, 61262011).


References

Addis, B., Locatelli, M., & Schoen, F. (2008a). Disk packing in a square:
  a new global optimization approach. Informs Journal on Computing, 20,
  516-524.

Addis, B., Locatelli, M., & Schoen, F. (2008b). Efficiently packing unequal
  disks in a circle. Operations Research Letters, 36, 37-42.

Akeb, H., Hifi, M., & M’Hallah, R. (2009). A beam search algorithm for the
  circular packing problem. Computers & Operations Research, 36, 1513-
  1528.

Akeb, H., & Hifi, M. (2010). A hybrid beam search looking-ahead algorithm
  for the circular packing problem. Journal of Combinatorial Optimization,
  20, 101-130.

Akeb, H., Hifi, M., & M’Hallah, R. (2010). Adaptive beam search lookahead
  algorithms for the circular packing problem. International Transactions in
  Operational Research, 17, 553-575.

                                     25
Al-Mudahka, I., Hifi, M., & M’Hallah, R. (2010). Packing circles in the
  smallest circle: an adaptive hybrid algorithm. Journal of the Operational
  Research Society, 62, 1917-1930.

Andreani, R., Birgin, E. G., Martnez, J. M., & Schuverdt, M. L. (2007).
  On Augmented Lagrangian methods with general lower-level constraints.
  SIAM Journal on Optimization 18, 1286-1309.

Birgin, E. G., Martı́nez, J. M., & Ronconi, D. P. (2005). Optimizing the
  packing of cylinders into a rectangular container: A nonlinear approach.
  European Journal of Operational Research, 160, 19-33.

Birgin, E. G., & Sobral, F. N. C. (2008). Minimizing the object dimensions
  in circle and sphere packing problems. Computers & Operations Research,
  35, 2357-2375.

Birgin, E. G., & Martı́nez, J. M. (2009). Practical Augmented Lagrangian
  Methods. In C. A. Floudas & P. M. Pardalos (Eds), Encyclopedia of
  Optimization (2nd ed., pp. 3013-3023), US: Springer.

Birgin, E. G., & Gentil, J. M. (2010). New and improved results for pack-
  ing identical unitary radius circles within triangles, rectangles and strips.
  Computers & Operations Research, 37, 1318-1327.

Castillo, I., Kampas, F. J., & Pintér, J. D. (2008). Solving circle packing
  problems by global optimization: Numerical results and industrial appli-
  cations. European Journal of Operational Research, 191, 786-80.

Fu, Z., Huang, W., & Lü, Z. (2013). Iterated tabu search for the circular
  open dimension problem. European Journal of Operational Research, 225,
  236-243.

                                      26
Glover, F., & Laguna, M. (1997). Tabu search. Boston: Kluwer Academic
  Publishers.

Graham, R. L., Lubachevsky, B. D., Nurmela, K. J., & Östergård, P. R. J.
  (1998). Dense packings of congruent circles in a circle. Discrete Mathe-
  matics, 181, 139-154.

Grosso, A., Locatelli, M., & Schoen, F. (2007). A population-based approach
  for hard global optimization problems based on dissimilarity measures.
  Mathematical Programming, 110, 373-404.

Grosso, A., Jamali, A. R., Locatelli, M., & Schoen, F. (2010). Solving the
  problem of packing equal and unequal circles in a circular container. Jour-
  nal of Global Optimization, 47, 63-81.

Hifi, M., & M’Hallah, R. (2004). Approximate algorithms for constrained
  circular cutting problems. Computers & Operations Research, 31, 675-
  694.

Hifi, M., & M’Hallah, R. (2006). Strip generation algorithms for constrained
  two-dimensional two-staged cutting problems. European Journal of Op-
  erational Research, 172, 515-527.

Hifi, M., & M’Hallah, R. (2007). A dynamic adaptive local search algo-
  rithm for the circular packing problem. European Journal of Operational
  Research, 183, 1280-1294.

Hifi, M., & M’Hallah, R. (2008). Adaptive and restarting techniques-based
  algorithms for circular packing problems. Computational Optimization
  and Applications, 39, 17-35.



                                      27
Hifi,   M.,   & M’Hallah,    R. (2009). A literature review on circle
  and sphere packing problems: Models and methodologies. Advances
  in Operations Research Volume 2009 (2009), Article ID 150624,
  doi:10.1155/2009/150624.

Hoos, H. H., & Stützle, T. (2005). Stochastic local search: Foundations and
  applications. Morgan Kaufmann.

Huang, W., Li, Y., Akeb, H., & Li, C. (2005). Greedy algorithms for packing
  unequal circles into a rectangular container. Journal of the Operational
  Research Society, 539-548.

Huang, W., Li, Y., Li, C., & Xu, R. (2006). New heuristics for packing un-
  equal circles into a circular container. Computers & Operations Research,
  33, 2125-2142.

Huang, W., Chen, M., & Lü, Z. (2006). Energy optimization for off-lattice
  protein folding. Physical Review E, 74, 41907.

Huang, W., & Ye, T. (2010). Greedy vacancy search algorithm for packing
  equal circles in a square. Operations Research Letters, 38, 378-382.

Huang, W., & Ye, T. (2011). Global optimization method for finding dense
  packings of equal circles in a circle. European Journal of Operational
  Research, 210, 474-481.

Huang, W, Fu, Z, Xu, R. (in press). Tabu search algorithm com-
  bined with global perturbation for packing arbitrary sized circles
  into a circular container, Science China (Information Sciences), doi:
  http://dx.doi.org/10.1007/s11432-011-4424-3.



                                    28
Huang, W. Zeng, Z., Xu, R., Fu, Z. (2012). Using iterated local search for
  efficiently packing unequal disks in a larger circle. Advanced Materials
  Research, 1477, 430-432.

Lü, Z., & Huang, W. (2008). PERM for solving circle packing problem.
  Computers & Operations Research, 35, 1742-1755.

Liu, D. C., & Nocedal, J. (1989). On the limited memory BFGS method for
  large scale optimization. Mathematical Programming, 45, 503-528.

López, C. O., & Beasley, J. E. (2011). A heuristic for the circle packing
  problem with a variety of containers. European Journal of Operational
  Research, 214, 512-525.

López, C. O., & Beasley, J. E. (2012). Packing unequal circles using for-
  mulation space search. Computers & Operations Research. (accepted
  manuscript).

Lourenço, H., Martin, O.,& Stützle, T. (2003). Iterated local search. In F.
  Glover, & G. Kochenberger (Eds.), Handbook of metaheuristics (pp. 320-
  353). New York: Springer.

Müller, A., Schneider, J. J., & Schömer, E. (2009). Packing a multidisperse
  system of hard disks in a circular environment. Physical Review E, 79,
  21102.

Nurmela, K. J., & Östergård , P. R. J. (1997). Packing up to 50 equal circles
  in a square. Discrete & Computational Geometry, 18, 111-120.

Specht, E. (2013). Packomania website, www.packomania.com.




                                      29
Szabó, P. G., Markót, M. Cs., Csendes, T., Specht, E., Casado, L. G., &
  Garcı́a, I. (2007). New approaches to circle packing in a square. Springer.

Wang, H., Huang, W., Zhang, Q., & Xu, D. (2002). An improved algo-
  rithm for the packing of unequal circles within a larger containing circle.
  European Journal of Operational Research, 141, 440-453.

Ye, T., Xu, R., & Huang, W. (2011). Global optimization of binary lennard-
  jones clusters using three perturbation operators. Journal of Chemical
  Information and Modeling, 51, 572-577.

Zhang, D., & Deng, A. (2005). An effective hybrid algorithm for the problem
  of packing circles into a larger containing circle. Computers & Operations
  Research, 32, 1941-1951.




                                     30
