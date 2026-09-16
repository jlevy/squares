                                                                Divide and concur: A general approach to constraint satisfaction

                                                                                                Simon Gravel and Veit Elser
                                                               Laboratory of Atomic and Solid-State Physics, Cornell University, Ithaca, NY, 14850-2501 USA
                                                                                                 (Dated: October 24, 2018)
                                                                 Many difficult computational problems involve the simultaneous satisfaction of multiple con-
                                                              straints which are individually easy to satisfy. Such problems occur in diffractive imaging, protein
                                                              folding, constrained optimization (e.g., spin glasses), and satisfiability testing. We present a simple
                                                              geometric framework to express and solve such problems and apply it to two benchmarks. In the first
                                                              application (3SAT, a boolean satisfaction problem), the resulting method exhibits similar perfor-
                                                              mance scaling as a leading context-specific algorithm (walksat). In the second application (sphere
arXiv:0801.0222v1 [physics.comp-ph] 31 Dec 2007




                                                              packing), the method allowed us to find improved solutions to some old and well-studied optimiza-
                                                              tion problems. Based upon its simplicity and observed efficiency, we argue that this framework
                                                              provides a competitive alternative to stochastic methods such as simulated annealing.


                                                     Difficult problems can often be broken down into a col-          The D&C approach can be applied to a wide range of
                                                  lection of smaller, more tractable, subproblems. This is         problems, both discrete and continuous. We first show
                                                  the basis of the divide and conquer approach, which ap-          how D&C is applied to the boolean satisfiability problem
                                                  plies when the initial problem and the subproblems have          (SAT), a standard benchmark in computer science. In
                                                  a similar structure, and the global solution can be re-          this problem, the D&C approach exhibits similar scaling
                                                  trieved from the solutions to the subproblems. Divide            behavior to walksat, a leading SAT solver which out-
                                                  and conquer as a rule leads to very efficient algorithms.        performs general-purpose algorithms such as simulated
                                                  However, many difficult problems do not fit such an effi-        annealing [1]. As a second example we study continu-
                                                  cient framework.                                                 ous sphere packing problems, which are formally simi-
                                                     For example, consider the problem of determining the          lar to the molecular geometry example mentioned above.
                                                  three-dimensional structure of a complex molecule given          The D&C approach matched or improved upon the best
                                                  clues about the distances between particular pairs of            known packings in some well-studied, two-dimensional
                                                  atoms (from knowledge of chemical bonds, NMR mea-                problems. In 10 dimensions it also discovered an inter-
                                                  surement, etc.). As subproblems we might consider the            esting new sphere arrangement related to quasicrystals.
                                                  substructures formed by small groups of atoms, since             The D&C approach therefore combines the advantages of
                                                  finding substructures satisfying local constraints is usu-       general purpose algorithms (versatility, simplicity) with
                                                  ally not challenging. However, the location and orienta-         the performance of special purpose algorithms (such as
                                                  tion in space of the substructures depends intricately and       walksat).
                                                  sensitively on their collective arrangement. Because the            In D&C the individual constraints are first expressed
                                                  division into subproblems in this case does not lead to          as subsets of a Euclidean space K, thereby transforming
                                                  a practical algorithm, molecular geometry problems are           the constraint satisfaction problem into the geometrical
                                                  usually transformed into optimization problems through           problem of finding a point in the intersection of multiple
                                                  the definition of a global cost function, and are then           sets. The Euclidean space provides the setting to define
                                                  solved through stochastic optimization methods such as           distance-minimizing projections to each of the N con-
                                                  simulated annealing.                                             straint sets. The projection operators {Pi }i=1...N will be
                                                     In this Letter we introduce a general method for solv-        the building blocks of the algorithm. Starting from an
                                                  ing constraint problems that takes advantage of the di-          initial guess, one uses the projections to probe the con-
                                                  vision into subproblems. In broad terms the method dif-          straint sets and update the guess. This idea has been
                                                  fers from stochastic searches in that the configurations         studied extensively in the context of convex constraint
                                                  explored are generated iteratively and deterministically.        sets [2].
                                                  Each iterative step is defined by two fundamental opera-           Given N primary constraints expressed as subsets of
                                                  tions. In the first operation, the problem is divided into       K, we first define the product space K N , consisting of
                                                  its constituent constraints, which are then solved inde-         N copies (or replicas) of K [15] . We then define, in
                                                  pendently, ignoring possible conflicts between different         the product space, the ‘divide’ constraint D (enforcing
                                                  constraints. In the second operation, conflicts between          one primary constraint on each replica) and the ‘concur’
                                                  constraints are resolved regardless of the satisfaction of       constraint C (enforcing replica concurrence) [2, 3]. The
                                                  the constraints. By a judicious application of these two         associated projections, acting on y = x(1) ⊗ x(2) ⊗ · · · ⊗
                                                  operations, we obtain a search strategy which, at each           x(N ) , are
                                                  step, solves all the subproblems separately and at the
                                                  same time seeks to resolve conflicts between their solu-
                                                  tions. We call this method divide and concur (D&C).                  PD (y) = P1 (x(1) ) ⊗ P2 (x(2) ) ⊗ · · · ⊗ PN (x(N ) ),   (1)
                                                                                                                              2

which acts separately on each of the replicas, and                 boolean variables that satisfies a list of Nc boolean con-
                                                                   straints, or clauses. Each clause is an OR statement in-
                PC (y) = x̄ ⊗ x̄ ⊗ · · · ⊗ x̄,               (2)   volving three literals, `1 ∨ `2 ∨ `3 , where each literal `i
                                                                   represents either one of the Nv boolean variables or its
which replaces the value of each replica by the average            negation.
value x̄ of all the replicas. In defining the concurrence             A D&C formulation of 3SAT is obtained by associating
projection, different weights
                           P λi may bePassigned to differ-         a real-valued search variable to each 3SAT literal, where
ent constraints, i.e., x̄ = i (λi x(i) )/ i λi [16]. Chang-        the values {1, −1} are taken to mean {True, False}. The
ing the weights is equivalent to changing the metric of            constraint D requires that each clause is satisfied; that is,
the product space; this possibility will prove beneficial          each literal must have value ±1, with at least one literal
even in problems where all the constraints are formally            per clause having value 1. In other words, to each clause
equivalent. Note that both projections, PC and PD , act            corresponds a variable triplet, which is projected by PD
in a highly parallel sense: either by treating indepen-            to the nearest of the seven satisfying assignments for this
dently each replica (PD ), or by treating independently            clause. Geometrically, these correspond to seven vertices
each variable across the replicas (PC ).                           of a cube. In this application PC ensures that all literals
   Through the product space construction the original             associated with the same boolean variable concur (with
constraint problem has been expressed as the problem of            due regard to negations). Since each constraint (clause)
finding a point in the intersection of two sets, both of           involves only three variables, the reduced search space[15]
which have easily implemented projection operators. To             has dimension 3Nc . For simplicity, we give equal weight
proceed, we need a search strategy that can use a pair of          to each constraint (λi = 1).
projection operators (Pa and Pb ) to seek the intersection            We compared the performance of the D&C algorithm
of two sets. The simplest approach is the alternating pro-         with walksat [1] on a collection of 3SAT problem in-
jections scheme, where yn+1 = Pa (Pb (yn )) [2, 4]. Despite        stances ranging from Nv = 50 to Nv = 25600, with fixed
its success with convex constraints and some nonconvex             ratio α ≡ Nc /Nv = 4.2, a value for which randomly gen-
problems, the alternating projections scheme is prone to           erated instances are expected to be difficult [10]. Random
getting stuck at fixed points which do not correspond to           instances were generated using the program makewff
solutions.                                                         (distributed with walksat), and instances that were not
   The difference map (DM) is an improvement upon al-              solved by either walksat or the D&C algorithm were
ternating projections which emerged in response to the             discarded. Each algorithm was applied 10 times to each
nonconvex constraints arising in diffractive imaging (the          instance, starting from different random initial condi-
phase problem)[5, 6]. It is defined by a slightly more             tions. The median number of variable updates required
elaborate set of rules, namely                                     to find the solution is plotted in Figure 1. The number
                                                                   of variable updates in walksat equals the total number
        yn+1 =yn + β (Pa ◦ fb (yn ) − Pb ◦ fa (yn ))               of flips of the boolean variables. In the D&C algorithm
                                                             (3)
      fi (yn ) =(1 + γi )Pi (yn ) − γi yn        i = a, b,         it is the total number of nonzero updates of any of the
                                                                   real-valued search variables (literals).
with γa = −1/β and γb = 1/β. The parameter β can                      Fig. 1 shows that Walksat (with the ‘noise’ parame-
have either sign and is chosen to improve performance.             ter fixed at the value p = 0.57) and the D&C algorithm
If the iteration reaches a fixed point y∗ , an intersection        (with β = 0.9) have similar performance behavior. Not
of the constraint sets has been found. The solution ysol is        only do they both find the same problems easy and the
obtained from the fixed point using ysol = Pa ◦ fb (y∗ ) =         same problems hard (which is not unexpected), but the
Pb ◦ fa (y∗ ). Note that the fixed point itself is not neces-      scaling of the number of variable updates needed to reach
sarily a solution; in fact, there typically is a continuum         the solution, as a function of problem size, is also similar.
of fixed points associated with every solution.                    Such a similarity is surprising, considering the difference
   The DM was recently used to solve a variety of difficult        in search strategies.
computational problems, including protein folding [7, 8],             walksat uses pseudorandom processes (or ‘noise’) to
boolean satisfiability, Diophantine equations, graph col-          update the variables asynchronously. In D&C, on the
oring, and spin glasses [9]. Most of these applications            other hand, the update rule is completely deterministic
relied on a decoupling of constraints through the use of a         and is applied synchronously to many variables. Fig.
dual set of variables, as in linear programming. The di-           1 also shows that choosing suboptimal parameters for
vide and concur approach we introduce here, defined by             either algorithm results in rapid performance degrada-
the use of the difference map with Pa = PC and Pb = PD ,           tion for large problem sizes. Even though the scaling of
is significantly more versatile and systematic.                    the variable updates are similar for walksat and D&C,
   The boolean satisfiability problem 3SAT is one of the           our implementation of D&C required significantly more
most extensively studied problems in constraint satisfac-          CPU time (between 4 and 200 times, depending on the
tion. The challenge is to find an assignement for Nv               instance) than walksat. Work on an optimized im-
                                                                                                                                                                             3

                                                                                                      ì   ì   ì
                                                                                                              à
                          10
                     10                                                                               à
                                                                                                          à   æ
                                                                                                  ì   æ
                                                                               à                  à       æ
                                                                                   æ
                                                                                   æ                  à
                                                                               æ   à                      à
                                                                                                  æ
 number of updates



                           8                                                           æ
                                                                                       à                      æ
                     10                                                        ì
                                                                                   ì
                                                                                   à
                                                                                       æ
                                                                                                  à
                                                                                                      æ
                                                                                                          æ
                                                                                        ì   à
                                                                                            æ     æ
                                                                               à
                                                                                        æ
                                                                                            ì æ
                                                                       à                à
                                                                   à   æ
                                                                           æ                æ
                                                               à
                                                               æ   æ   æ   à                à
                           6
                     10                                æ
                                                       à               à
                                                           æ       æ
                                                                   ì   ì   æ
                                                                           ì
                                                                           à
                                                           à       à
                                              æ
                                              à
                                                       æ
                                                       ì
                                                               æ
                                                               à
                                                               ì                                0.92 D&C
                                                       à
                                                   æ
                                               æ
                                               ì
                                              æà
                                                   à
                                                           æ
                                                                                                0.90
                           4             æ
                                         à                 à
                                                           ì
                     10        æ
                                   æ
                                   à         æ
                                                   æ
                                                   à                                            0.50
                               à
                                                   ì                                            0.54 WS
                                                                                                0.57
                               æ
                               à
                               ì
                                   æì
                                    æ
                                    æ
                                    à
                                         ì
                                         à
                                         æ                                                                        FIG. 2: An example of an improved packing for 169 disks in
                                        100                        1000                         10 000            a square found by the D&C algorithm. The figure on the left
                                                                                                                  shows the previously best known packing [13], with density
                                                           number of variables
                                                                                                                  0.8393. The density of the improved packing shown on the
                                                                                                                  right is 0.8399. Contacts are shown with dotted lines; colors
FIG. 1: Median number of variable updates needed to find a                                                        indicate the number of contacts.
solution for walksat (WS) and divide and concur (D&C) on
the same set of random 3SAT instances with α = 4.2. Each
median was calculated by solving the same instance 10 times                                                       mance improvement. At the end of each DM step we
starting from different random initial guesses, for parameter                                                     used λab → σλab + (1 − σ) exp (−α dab ), where dab is
values β = 0.9 (D&C) and p = 0.57 (walksat). Variations
                                                                                                                  the current distance between the pair[17]. We used the
resulting from changing β and p are indicated by the shaded
areas; both methods exhibit parameter sensitivity for prob-                                                       value σ = 0.99 to ensure that the metric update is quasi-
lems with more than 104 variables. A point at the top edge                                                        adiabatic (i.e., slow on the time scale of variable updates),
indicates that the median exceeded the cutoff on the number                                                       and α ≃ 30.
of updates, 3 × 1010 .                                                                                               We first consider packings of n equal disks of diameter
                                                                                                                  m in a unit square, and take as a starting point the best
                                                                                                                  known packing diameters m∗ from Ref. [13]. This prob-
plementation of the D&C algorithm is in progress and                                                              lem is quite challenging, due to the coexistence of many
should allow an easier exploration of the behavior of the                                                         different arrangements with similar density. We tested
method for larger problem sizes.                                                                                  the D&C algorithm for each value of n in the range 2-
   Another constraint problem which has been exten-                                                               200. For each n, we generated up to 400 random initial
sively studied is the packing of n spheres in a finite D-                                                         guesses. For each initial guess, a small value of the di-
dimensional volume (see, e.g., Refs. [11–13] and refer-                                                           ameter m was chosen, and a packing was sought. When
ences therein). The constraint formulation of this prob-                                                          a solution was found, m was increased, and the process
lem is more directly geometrical than boolean satisfiabil-                                                        was repeated until the algorithm failed to find a pack-
ity. Since each sphere must avoid n − 1 other spheres                                                             ing, or until the best known packing diameter m? was
and lie within a certain volume, there are altogether n                                                           reached. In the latter case the target was increased be-
constraints per sphere. The reduced search space[15]                                                              yond m? with the hope of finding a denser packing. No
requires one D-dimensional variable replica for every                                                             information about the known packings was used, apart
sphere participating in a constraint, for a net search space                                                      from their densities.
dimensionality of Dn2 .                                                                                              For 143 of the 197 values of n a packing with diameter
   Within the framework of D&C there is a formal simi-                                                            close to the optimal packing (m > m? −10−9 ) was found.
larity in the constraint structure of packing spheres and                                                         More surprisingly, improved packings were found in 38
3SAT. Just as every boolean variable is constrained by                                                            cases. The smallest n for which an improved packing was
each of the clauses where it occurs, every sphere in a                                                            found is 91. The largest improvement was for n = 182,
packing has a volume exclusion relationship with each of                                                          for which a packing was found with m = m? + 4.6×10−5 .
the other spheres in the packing: kxa − xb k > mab . This                                                         For 28 values of n a packing was found with m > m? +
similarity and the success of D&C with 3SAT is strong                                                             1 × 10−6 . An example of such an improved packing is
motivation to apply D&C to the sphere packing problem.                                                            shown in Figure 2.
   Near the solution of any n-sphere packing problem,                                                                When packing many disks the optimization challenge is
the number of relevant exclusion constraints (contact-                                                            easy to identify as a contest between close-packing in the
ing pairs) grows only as n (for fixed D) while the to-                                                            bulk and an efficient match to the boundary. In higher
tal number of constraints is O(n2 ). In the D&C ap-                                                               dimensions the structure of the solution is not so easily
proach it is possible to increase the weight of these rel-                                                        characterized, and we can look to the D&C method as
evant pairs by dynamically adjusting the corresponding                                                            an unbiased tool for exploration. A classic problem in
metric weight λab . This results in considerable perfor-                                                          geometry is to determine kissing numbers τD : the max-
                                                                                                                            4

imum number of unit spheres that can be packed in D-          the difference map, for finding solutions given a pair of
dimensions, so that each contacts a given unit sphere.        constraint projections, makes the D&C approach almost
Early investigations of this problem were stimulated by       as easy to implement as general-purpose sampling algo-
a debate between Newton and Gregory, who disputed the         rithms such as simulated annealing. Most of the problem-
value of τ3 . The only known kissing numbers are τ1 = 2,      specific development needed, in this framework, is the
τ2 = 6, τ3 = 12, τ4 = 24, τ8 = 240, and τ24 = 196560.         definition of the appropriate projection operators. We
In dimension 1-8, and also 16-24, the best known lower        believe the latter are able to exploit important elements
bounds on τD are given by the number of minimal vectors       of the problem structure not accessed by stochastic sam-
in the unique laminated lattice of the same dimension[11].    pling, and that this accounts for the superior performance
For dimension 9-15 the best bounds are obtained from          of D&C.
constructions based on error-correcting codes[11]. Dis-
coveries of novel packings in higher dimensions has for         We acknowledge useful discussions with Y. Kallus, D.
the most part been achieved through mathematical in-          Loh, I. Rankenburg, and P. Thibault. This work was
spiration. Unbiased searches, defined only by the basic       supported by grant NSF-DMR-0426568.
constraints, have to our knowledge not been attempted
beyond dimension 5[14]. This raises the possibility that
interesting packings in high dimensions may have escaped
detection only for lack of imagination.
                                                               [1] B. Selman, H. Kautz, and B. Cohen, DIMACS Series in
   With minimal adjustment to the above procedure for
                                                                   Discrete Mathematics and Theoretical Computer Science
finding disk packings, we were able to find kissing ar-            26, 521 (1996).
rangements as good as the best known in dimension 2-           [2] H. Bauschke, P. Combettes, and D. Luke, J. Approx.
4, 6, and 8. After introducing just the assumption of              Theory 127, 178 (2004).
inversion symmetry, optimal packings were obtained in          [3] G. Pierra, in Proceedings of the 7th IFIP Conference on
all dimensions up to 8. Our searches in higher dimen-              Optimization Techniques (Springer-Verlag, London, UK,
sions have so far revealed an interesting new packing in           1976), pp. 200–218.
                                                               [4] S. Kaczmarz, Bull. Int. Acad. Polon. Sci. A 35, 355
dimension 10. It is easy to understand why this pack-
                                                                   (1937).
ing was missed. Constructions based on integral lattices       [5] V. Elser, J. Opt. Soc. Am. 20, 40 (2003).
and error-correcting codes all have the property that the      [6] P. Thibault, Ph.D. thesis, Cornell University (2007).
cosine of the angle subtended by any two spheres is ratio-     [7] V. Elser and I. Rankenburg, Phys. Rev. E 73, 26702
nal. The packing of 378 spheres discovered by the D&C              (2006).
algorithm has all cosines in a√set that includes irrational    [8] I. Rankenburg and V. Elser, arXiv: 0706.1754 (2007).
numbers: {±1, ±1/2, (±3 ± 3)/12, 0}. An analysis of            [9] V. Elser, I. Rankenburg, and P. Thibault, PNAS 104,
                                                                   418 (2007).
the coordinates obtained by the algorithm has revealed
                                                              [10] P. Cheeseman, B. Kanefsky, and W. Taylor, Proceedings
that these 378 sphere positions are expressible as unique          of the 12th IJCAI pp. 331–337 (1991).
integer multiples of a basis of 12 vectors. The construc-     [11] J. Conway and N. Sloane, Sphere Packings, Lattices and
tion has a strong relationship to quasicrystals, where the         Groups (Springer, 1999).
excess dimension of the basis accounts for irrational rela-   [12] K. Stephenson, Introduction to Circle Packing (Cam-
tionships in the geometry. The algorithm, of course, had           bridge University Press, 2005).
no knowledge of quasicrystal geometry.                        [13] P. Szabó, M. Markót, T. Csendes, E. Specht, L. Casado,
                                                                   and I. Garcãa, New Approaches to Circle Packing in a
   This ‘irrational’ structure emerged as soon as the num-
                                                                   Square (Springer-Verlag, New York, 2007).
ber of spheres was increased above 372, the largest known     [14] K. Nurmela, Constructing Spherical Codes by Global Op-
kissing number for 10-dimensional lattices [11]. The               timization Methods (Helsinki University of Technology,
same irrational arrangement was also found for up to               1995).
384 spheres; the 6 additional spheres were accomodated        [15] In problems where each projection Pi acts nontrivially
in holes of the structure (and have continuously variable          only on a limited subset Ki of K, the product search
cosines). Finally, the algorithm has so far been unsuc-            space may be reduced to K1 ⊗ K2 ⊗ · · · ⊗ KN , with ob-
                                                                   vious performance gains. If a variable is involved in Ni
cessful in discovering the best known kissing arrangement
                                                                   constraints, there will be Ni copies, or variable replicas,
in 10 dimensions, with kissing number 500.                         of this variable in the reduced search space.
   The divide and concur approach provides a natural          [16] In the reduced search space, the average should be taken
framework in which to address various hard computa-                only on the variables in the reduced space. If Vk is the
tional problems. In two benchmark applications, 3SAT               index list of the constraints in which variable k appears,
                                                                         P           (i)  P
and sphere packing, the D&C approach compares with,                x̄k = i∈Vk (λi xk )/ i∈Vk λi .
and in some cases improves upon, state-of-the-art spe-        [17] To get a unique pair distance one uses coordinates given
cialized methods. The uniform mechanism provided by                by the concurrence term of the difference map, PC ◦ fD .
