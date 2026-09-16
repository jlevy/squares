 New and improved results for packing identical unitary
  radius circles within triangles, rectangles and strips∗
                         Ernesto G. Birgin†                 Jan M. Gentil†
                                          June 3rd, 2009


                                               Abstract
            The focus of study in this paper is the class of packing problems. More speciﬁ-
        cally, it deals with the placement of a set of N circular items of unitary radius in-
        side an object with the aim of minimizing its dimensions. Diﬀerently shaped con-
        tainers are considered, namely circles, squares, rectangles, strips and triangles. By
        means of the resolution of nonlinear equations systems through the Newton-Raphson
        method, the herein presented algorithm succeeds in improving the accuracy of pre-
        vious results attained by continuous optimization approaches up to numerical ma-
        chine precision. The computer implementation and the data sets are available at
        http://www.ime.usp.br/~egbirgin/packing/.

        Keywords: packing, nonlinear equations system, Newton’s method, nonlinear pro-
        gramming.


1       Introduction
Packing problems commonly arise in practical life. Hence, strategies capable of efficiently
solving them are of great interest, not only from a purely mathematical but also from an
economical standpoint. Some of the techniques available in the published literature consist
of reasonably fast discrete heuristics [21, 22], but which are not guaranteed to converge to
global optima. Others employ nonlinear models [5–7, 12–15, 17–20], which can be solved
by nonlinear programming algorithms. Of special relevance to this paper, such iterative
methods generate linearly convergent sequences to whose set of accumulation points the
looked-for answer is expected to belong.
    ∗
     This research was partly supported by PRONEX-Optimization (PRONEX-CNPq / FAPERJ E-26 /
171.510/2006 - APQ1) and FAPESP (Grants 2006/53768-0 and 2006/57633-1).
   †
     Department of Computer Science, Institute of Mathematics and Statistics, University of São Paulo, Rua
do Matão 1010, Cidade Universitária - 05508-090 São Paulo, SP - Brazil ({egbirgin|jgmarcel}@ime.usp.br).



                                                    1
    In particular, in a recently published work [8], twice differentiable models for both two
and three-dimensional packing problems were introduced and further solved with the aid
of Algencan [1–4], a modern Augmented Lagrangian routine for optimization of smooth
minimization problems with general constraints. Although feasible answers were obtained
for all discussed cases, they were of poor precision in comparison to the known optimal
results [16]. Motivated by these achievements, this study aspired to develop a method of
quadratic convergence rate that would improve their accuracy and hopefully also provide
optimal solutions not yet reported in the literature.
    This paper is organized as follows. In Section 2 the problem is formally stated and
the proposed approach is fully described. Section 3 details the most significant challenges
faced in its implementation. In Section 4 the numerical experiments are delivered. Finally,
Section 5 concludes the paper.


2     Nonlinear model and suggested approach
The problem at hand is that of packing a set of N identical circles of radius r = 1 (here-
inafter called items) in a fixed-shaped figure (denominated object) while minimizing the
latter’s dimensions. Throughout this work, several geometric forms were treated, namely
circles, squares, rectangles, triangles and strips, defined as a rectangle that has got one of
its dimensions fixed.
    In order for a setup to be accepted as valid, all items must obviously not overlap or violate
the object’s boundaries. Being solely dependent upon items’ positions, the non-overlapping
condition can be expressed, irrespective of the object’s form, as:
                         q
                           (cxi − cxj )2 + (cyi − cyj )2 ≥ ri + rj for all i 6= j              (2.1)

where ci = (cxi , cyi ) and ri denote the i-th item’s centre and radius, respectively, for 1 ≤ i ≤ N.
    On the other hand, both the objective function and the non-boundaries-violation con-
straints vary according to the object and therefore must be individually studied.

Circular object Without loss of generality, assume the object’s centre C to be located at
the coordinate system’s origin and let R represent its radius. It may be readily seen that all
items will q
           be completely contained within the object’s boundaries if and only if the inequality
R ≥ ri + (cxi )2 + (cyi )2 holds for every i = 1, . . . , N. Thus, the following nonlinear model
can be written:

                           minimize R
                          subject to (cxi )2 + (cyi )2 ≤ (R − ri )2 for all i                  (2.2)
                                     non-overlapping constraints (2.1)




                                                    2
Squared object Under the assumption that the coordinate system’s origin coincides with
the lower left-hand vertex of the square, the nonlinear model results naturally:

                          minimize L
                         subject to ri ≤ cxi ≤ L − ri for all i                            (2.3)
                                    ri ≤ cyi ≤ L − ri for all i
                                    non-overlapping constraints (2.1)

Strip object Indicating by W the variable width of an strip with fixed height L and
asserting as true the same assumption concerning the system’s origin, one can derive the
model below:

                          minimize W
                         subject to ri ≤ cxi ≤ L − ri for all i                            (2.4)
                                    ri ≤ cyi ≤ W − ri for all i
                                    non-overlapping constraints (2.1)

Rectangular object Based on whether the objective function is intended to minimize
the rectangle’s perimeter or its area, two different and equally interesting models may be
formulated:

                          minimize L + W or L × W
                         subject to ri ≤ cxi ≤ L − ri for all i                            (2.5)
                                    ri ≤ cyi ≤ W − ri for all i
                                    non-overlapping constraints (2.1)

Triangular object For the (equilateral) triangle of side length L, the coordinate system’s
origin is taken as the base’s midpoint:

                         minimize L
                        subject to ri ≤ cyi for all i
                                    √                    √
                                   2 3cyi − 6cxi ≤ 3L − 4 3ri for all i                    (2.6)
                                    √                    √
                                   2 3cyi + 6cxi ≤ 3L − 4 3ri for all i
                                   non-overlapping constraints (2.1)

    The explicit resolution of problems (2.2) through (2.6) by utilizing an Augmented La-
grangian nonlinear solver was the technique attempted in [8]. Two main concerns were raised
by the paper authors: (i) the quadratic relation between the number of items and the number
of constraints, which makes their evaluation a costly task, and (ii) the difficulty of achieving
high precision results with the employed routine.

                                               3
    The central idea of this study stems from the observation that in an optimal configuration
(i.e. one that realizes the global minimum of the above stated optimization problems) a
number of items are placed in contact with each other and with the object’s boundaries
(see Figure 1), making active the matching constraints. Consequently, if those contacts were
known a priori, an overdetermined system of nonlinear equations could then be constructed,
to whose solution set an optimal arrangement must belong. Moreover, it will be shown that
the number of such equations is linear with respect to the number of items (in contrast to
the quadratic number of constraints in the nonlinear optimization models).




                        Figure 1: Optimal setup of 5 items in a circle


    More formally, let Φ and Ψ designate the supposedly known sets of contacts, in an optimal
solution, of items with the object and with other items, respectively.

                          i ∈ Φ ⇐⇒ item i makes contact with object,
                     (i, j) ∈ Ψ ⇐⇒ item i makes contact with item j.

Besides, allow G to be the undirected graph whose vertices are the items’ centres and such
that two vertices are adjacent if and only if the corresponding items are in contact. Note
that, since G is planar (i.e. it can be drawn on the plane in such a way that its edges intersect
only at their endpoints; see Figure 1), it holds true that |Ψ| = O(N) (see, for example, [9]).
(The same conclusion stems from the fact that each circular item cannot touch more than
six others, so that 6N serves as an upper bound on the number of such contacts.) Likewise,
|Φ| ≤ N.
    Now, consider a nonlinear system F : Rn → Rm where the number of equations m equals
the number of contacts — |Φ| + |Ψ|, already known to belong to O(N) — and the number
of variables n may assume one of the values below (coordinates (x, y) of each item’s centre
plus the number of variable dimensions of the containing object):
                       
                       2N + 1 for the circle, square, strip and triangle,
                  n=
                       2N + 2 for the rectangle.


                                               4
                                                                        q
   To each (i, j) ∈ Ψ corresponds an active constraint (cxi − cxj )2 + (cyi − cyj )2 = 2r or,
equivalently, (cxi − cxj )2 + (cyi − cyj )2 = (2r)2. This translates into the addition of the following
equation to the system F :
                               fijψ (·) = (cxi − cxj )2 + (cyi − cyj )2 − 4r 2 .                  (2.7)

    Clearly, the equation fiφ (·) that shall be included in F for each i ∈ Φ depends on the
form of the object. qIn the circular case, for instance, to each i ∈ Φ corresponds an active
constraint R = ri + (cxi )2 + (cyi )2 or, equivalently, (R − ri )2 = (cxi )2 + (cyi )2 . This translates
into the addition of the following equation to the system F :
                                 fiφ (·) = (R − ri )2 − (cxi )2 + (cyi )2 .                       (2.8)
The analogous procedure for differently shaped containers, being trivially deducible from the
appropriate nonlinear problem, will be omitted herein for the sake of brevity.
   It should be noted, however, that while overdetermined (as a rule, m ≫ n), the system
deduced above will be compatible as long as the contacts are assumed to be known in advance.
That is because many of the equations it comprises are redundant. This observation is


                                                            1
                                              6


                                                                    2
                                                      7
                                         5



                                                                3
                                                  4




Figure 2: Optimal configuration for 7 items in a circle (overdetermined compatible system
with 15 variables and 18 equations)


illustrated by Figure 2, where the central item’s position is uniquely dictated, for example,
by its contacts (depicted by dashed lines) with items 2 and 5, rendering the equations relative
to its contacts with other surrounding items superfluous.
    One critical question that arises from this strategy is how the information about the
contacts made in an optimal solution could be learned. It occurs that, by way of a straight-
forward analysis of the poor-precision answers found by [8], such knowledge may be acquired
to a high degree of confidence. For that purpose, it must be adopted a value ε ∈ R+ amount-
ing to the minimum distance between the border of two items that should not be regarded
as adjacent and the inequality below has to be tested for all i, j satisfying 1 ≤ i < j ≤ N:
                                q
                                   (cxi − cxj )2 + (cyi − cyj )2 − 2r ≤ ε,                        (2.9)

                                                      5
where the values of ci and cj are taken from the output of [8]. If it holds, then the related
equation fijψ is incorporated into the nonlinear system F . Similarly, the equations fiφ are
originated by an analogous mechanism conducted for the detection of contacts between each
item and the object.
     Bear in mind that the value of ε is crucial to the success of the method and cannot
be dissociated from the quality of the answers given by Algencan. In such configuration,
three are the possibilities for each pair of items: (i) they overlap, (ii) they do not overlap and
are far away from each other, or (iii) they do not overlap but are very close to each other.
Hence, considering a poor-precision result acquired via the resolution of the corresponding
nonlinear model (2.2)–(2.6), contacts between pairs of items will be forced in cases (i) and
(iii). In order to distinguish between cases (ii) and (iii), ε plays a vital role.
     Let ω be the maximum overlapping between any pair of items in a solution to the NLP
model. If ω is such that it were considered a “reasonable” overlapping for the underlying
packing problem by the employed solver, then it is safe to assume that any pair of items
that do not overlap but whose borders are at a distance less than ω may be in contact. In
this manner, ω is a satisfactory initial candidate for ε.
     Starting from this knowledge, as a large number of optimal solutions for packing problems
within circles and squares had already been made publicly available, the value of ε was
empirically adjusted around ω in a way that would correctly identify the contacts in those
instances.
     Once this task has been accomplished, a root of F is looked for utilizing the Newton-
Raphson method. The rationale behind this choice is the expectation that, if initially fed
with a guess x(0) sufficiently close to the true solution x∗ , the algorithm will produce a
sequence {x(k) } quadratically convergent to x∗ (see, for example, [10]). The equations that
describe the iterative process are:

                                     JF (x(k) )d = −F (x(k) )                              (2.10)
                                         x(k+1) = x(k) + d,

where JF is the Jacobian matrix of F .
    We consider two different ways of solving the overdetermined (albeit compatible, as long
as all contacts have been detected correctly) linear system (2.10):
QR decomposition of the Jacobian matrix Due to the absolute lack of information on
    the rank of JF (x(k) ), a variant of the QR method, the QR decomposition with column
    pivoting [11], is calculated. Thanks to its highly desirable numerical stability char-
    acteristics when JF (x(k) ) is not well conditioned, this is the strategy of choice in the
    algorithm developed.
Cholesky’s method applied to the normal equations In spite of its inferior numerical
    properties, the normal equations approach has been more successful in computing x(k+1)
    whenever JF (x(k) ) is found to be rank deficient. Such phenomenon may be justified
    by the realization that, in this situation, there are infinitely many solutions to (2.10),
    among which only one interest us — the one that minimizes the object’s dimensions.

                                                6
      For that reason, a sensible approach is to solve the least squares problem, with the
      new linear system becoming:
                               JFT (x(k) )JF (x(k) )d = −JFT (x(k) )F (x(k) )            (2.11)
      It should be remarked that M = JFT (x(k) )JF (x(k) ) ∈ Rn×n is both symmetric and posi-
      tive semidefinite. More importantly, it is singular, seeing that rank(M) = rank(JF (x(k) ))
      and also that this path is used only when rank(JF (x(k) )) < n. For that reason, to solve
      the linear system (2.11), the Modified Cholesky decomposition [10] is preferred, which
      actually factorizes a slight perturbation of the matrix JFT (x(k) )JF (x(k) ). The vector d
      easily follows by forward and back substitution.
    After each iteration, Newton’s method is checked for convergence, which is characterized
by the verification of x(k+1) = x(k) and constitutes the main stopping criterion. Still, if the
initial value x(0) is too far from the true zero, the method might fail to converge, and a cap
on the number of iterates is made necessary as a secondary stopping criterion.


3     Implementation aspects
In this section the most important practical implementation details are discussed.

3.1    System indetermination
Contrary to the logical intuition that the constructed nonlinear system would be typically
overdetermined, its indetermination was of one the earliest challenges that had to be coped
with. A plausible explanation is the fact that, even on an optimal configuration, there can
be items taking part in less than two contacts, thus contributing with the addition of more
variables than equations to the system (causing it to become undetermined). Those which
exhibit such attribute are named loose items (see Figure 3(a)).
    As a means to overcome this obstacle, a preprocessing routine detects and temporarily
removes all loose items from the set to be packed. The proposed technique is then ordinarily
carried out for the remaining items and only when their optimal placement is determined
(see Figure 3(b)) are the “rattlers” reintroduced into the problem.
    Such job may be thought of as a further optimization problem, just with a largely de-
creased number of variables (proportional to the number of loose items). Let L ⊆ {1, . . . , N}
be the set of indices of loose items and l its cardinality. The variables of the aforementioned
optimization problem are the centre ci ∈ R2 and the radius ri ∈ R for all i ∈ L. The
underneath model therefore follows:
              maximize D
             subject to ri ≥ D for all i ∈ L                                               (3.1)
                        d(ci, cj )2 ≥ (ri + rj )2 for all i, j ∈ L, i 6= j                 (3.2)
                        d(ci, cj )2 ≥ (ri + r)2 for all i ∈ L, j ∈     /L                  (3.3)
                        corresponding non-violation constraints (see Section 2)

                                                 7
                            (a)                                  (b)



Figure 3: Example of arrangement exhibiting system indetermination: (a) greyed items
making less contacts (0 and 1) than the number of equations they introduce; (b) optimal
layout after removing those items.

where d(·, ·) stands for the Euclidean distance and the values of r and cj for each j ∈   / L are
considered constant and are taken from the output of the method for the contracted set (see
Figure 3(b)).
    By solving it with Algencan, two are the possible outcomes: either an optimal packing
of the original set is found (see Figure 4) or, should the reincorporation of the once withdrawn
items fail, it can be concluded that the contacts have been erroneously detected in the first
place and that the method must be re-executed with a more properly estimated ε parameter.




Figure 4: Layout after reintegration of loose items with the loose items centrally placed in
the room available


    If the optimal value D ∗ obtained is such that D ∗ ≥ r, then all loose items have been fit
into the object. It should also be noted that whenever D ∗ > r, their radius is taken as being
equal to r and, as a result, they will be centrally placed in the room available.

                                               8
3.2    Loss of convergence
It has been verified that, for circular objects, there usually exists a neighbourhood of arbi-
trarily close optimal solutions, derived from the mere rotation of the whole set of items in
the interior of the object (see Figure 5).




                            (a)                                (b)



Figure 5: Distinct optimal setups for 3 items in a circle, where (b) is attainable by rotating
the items in (a).

    Since it severely impairs the convergence of Newton’s method, such ill behaviour had to
be avoided by selecting one of the items to have one of its centre’s coordinates unchanged
by the algorithm. Unfortunately, though, none of the heuristics assessed for the selection
of that item showed themselves to be consistently satisfactory. Because of that, each of the
n − l non-loose items is successively iterated to assume this role and the best solution gets
saved.

3.3    Post-optimization overlapping and violation elimination
In order to guarantee that the given answers are eligible for comparison to the best ever
published [16], it is mandatory to first eliminate any overlapping or violations that might
remain. In other words, it should be guaranteed that the arrangements associated with them
are correct under the analytical rigour. The accomplishment of this requirement is achieved
by subjecting the solution to the nonlinear system of equations given by Newton’s method
to scaling.
    Taking the items in pairs, the distance between their centres is evaluated. Let δ be the
minimum of all such values. If δ ≥ 2r, then there are no overlapping constraints being
disobeyed and no adjustments to be made. On the other hand, if δ < 2r, then the items
must be spread out so that δ ≥ 2r holds. A new placement such that d(c′i , c′j ) ≥ 2r for every
i 6= j can be attained by simply making
                                                 2r
                                         c′i =      · ci                                  (3.4)
                                                 δ
                                                 9
for each item i.
    In fact, since it holds true that d(ci , cj ) ≥ δ for every i 6= j, it easily follows that
                                                2r                2r
                              d(c′i , c′j ) =      · d(ci, cj ) ≥    · δ = 2r,                   (3.5)
                                                δ                  δ
which is the intended result.
   As for the eventual violation of the object’s boundaries, there is no option other than
enlarging the object’s dimensions until all items are entirely contained within its boundaries.
For the circular case, for instance, it suffices to make
                                                        q
                                 R′ =       max         (cxi )2 + (cyi )2 + r.                   (3.6)
                                         {i=1,...,N }


    After those post-optimization corrections have been made, it is safe to assert that a
solution with the maximum machine precision has been found. It finally turns out practicable
to draw all the desired comparisons, which are the subject of the next section.
    To end this section, Algorithm 1 provides an overview of the methods introduced for the
circular case.




                                                        10
Algorithm 1 Pseudocode for the circular case
Require: N := number of items
Require: r := item’s radius (if other than 1.0)
Require: T := maximum processing time allotted
Require: K := cap on the number of Newton steps
 1: R∗ ← +∞
 2: while elapsed time ≤ T do
 3:   Run Algencan with its default parameters to solve the nonlinear model (2.2) with feasibility and
      optimality tolerances equal to 10−4 and consider its answer (xnlp , Rnlp ) as an initial guess for Newton’s
      method.
 4:   Temporarily remove all loose items, as detailed in Subsection 3.1, and redeﬁne (xnlp , Rnlp ) accordingly.
 5:   Detect all contacts between items and with the object, as explained in Section 2, and construct an
      appropriate system of nonlinear equations F .
 6:   R̂ ← +∞
 7:   for all non-loose items i do
 8:      k ← 0, (x(0) , R(0) ) ← (xnlp , Rnlp )
 9:      Remove variable cxi from (x(0) , R(0) ) and replace it in F with its value from (xnlp , Rnlp ).
10:      while k < K do
11:         k ←k+1
12:         Solve the Newtonian system (2.10) for F and obtain (x(k) , R(k) ).
13:         if (x(k) , R(k) ) = (x(k−1) , R(k−1) ) then
14:            Break. {Newton’s method converged}
15:         end if
16:      end while
17:      Reintroduce variable cxi to (x(0) , R(0) ), taking its value from (xnlp , Rnlp ).
18:      Update the best computed result (x̂, R̂) (i.e. if R(k) < R̂).
19:   end for
20:   Reintroduce all loose items previously removed, as explained in Subsection 3.1.
21:   Evaluate the minimum distance δ between the centres of each pair of items.
22:   if δ < 2r then
23:      for all items i do
24:         Redeﬁne (ĉxi , ĉyi ) as 2r/δ · (ĉxi , ĉyi ).
25:      end for
         Redeﬁne R̂ as max{i=1,...,N } (ĉxi )2 + (ĉyi )2 + r.
                                             p
26:
27:   end if
28:   Update the best computed result (x∗ , R∗ ) (i.e. if R̂ < R∗ ).
29: end while
30: return (x∗ , R∗ )




Remark. The most noteworthy difference between Algorithm 1 and the method developed
for differently shaped containers is the absence of lines 6, 7, 18 and 19 in the latter variant,
since there is no neighbourhood of arbitrarily close optimal solutions to be tackled in the
first place.




                                                       11
4     Numerical results
All tests were conducted on a 2.4GHz Intel Core 2 Quad with 4GB of RAM memory
and running GNU/Linux operating system. The code, fully written in Fortran 77, was
compiled by the G77 Fortran compiler of GCC with the -O3 optimization directive enabled.
The values of T and K that yielded the results presented later in this section are 5h and
1000, respectively.
    We solved instances with the number of items varying from 1 to 50. Tables 1 and 2 show
the resulting values for the circular object’s radius and the squared object’s side, respectively,
and their confrontation with the best ever reported [16]. Their first column holds the number
of items; the second, the solution found by the developed method; the third, the reference
values from [16]; the fourth, the difference between them; the fifth, the elapsed CPU time
(in seconds).
    It should be noticed that the answers obtained coincide with the values of reference.
More precisely, in 48 of the cases of packing in a circle and in 44 of those of packing in a
square, the results matched to all decimal places, i.e. up to the machine precision, with an
absolute error of less than 10−16 for circles and 10−12 for squares (the difference being due
to the number of digits in the data sets available in [16]). In the other 8 instances where
maximal precision has not been achieved, the absolute error is always of the order of 10−6 .
    Tables 3 and 4 present unpublished results for the packing problems of minimizing the
area and the perimeter of an enclosing rectangle, while Table 5 exhibits unprecedented
solutions for the area minimization of triangular and strip objects. Lastly, Figure 6 illustrates
a few selected solutions.


5     Concluding remarks
This study addressed itself to the problem of packing unitary radius circles within differently
shaped containers with the aim of minimizing its dimensions. The approach developed
builds upon approximate solutions provided by continuous optimization techniques formerly
developed. By pursuing the zero of a nonlinear equations system properly deduced from the
contacts established in a candidate solution, refinement of those approximate results up to
the machine precision were made possible.
    For all studied problems, feasible solutions comparable to the best results already known
were achieved. However, the treatment of packing problems in triangles, rectangles and
strips, whose answers had not been published in the literature before, can be regarded as an
even more remarkable contribution.
    The Fortran 77 source code of the routines implemented during this work and a
complete description of all solutions, each of which being composed of its items’ posi-
tions and a graphical representation of the contacts they make, are available at http:
//www.ime.usp.br/~egbirgin/packing/, as well as the best results given by them.




                                               12
                        (a)                        (b)               (c)




                 (d)                         (e)                           (f)



Figure 6: Optimal layouts for 50 items in a: (a) circle; (b) rectangle, minimizing its area;
(c) rectangle, minimizing its perimeter; (d) square; (e) strip, with fixed length L = 9.5; and
(f) equilateral triangle.




                                             13
# of items      Circle radius         Reference        Diﬀerence      Time
    1        1.0000000000000000   1.0000000000000000    0.0E+00        0.00
    2        2.0000000000000000   2.0000000000000000    0.0E+00        0.11
    3        2.1547005383792515   2.1547005383792515    0.0E+00        0.00
    4        2.4142135623730949   2.4142135623730949    0.0E+00        0.00
    5        2.7013016167040798   2.7013016167040798    0.0E+00        0.09
    6        3.0000000000000000   3.0000000000000000    0.0E+00        0.10
    7        3.0000000000000000   3.0000000000000000    0.0E+00        0.00
    8        3.3047648709624866   3.3047648709624866    0.0E+00        0.05
    9        3.6131259297527527   3.6131259297527532   -4.4E−16      271.82
   10        3.8130256313981246   3.8130256313981246    0.0E+00        0.13
   11        3.9238044001630872   3.9238044001630872    0.0E+00       29.90
   12        4.0296019301161836   4.0296019301161836    0.0E+00       16.43
   13        4.2360679774997898   4.2360679774997898    0.0E+00        0.90
   14        4.3284285548608370   4.3284285548608370    0.0E+00        9.67
   15        4.5213569647061647   4.5213569647061647    0.0E+00       28.79
   16        4.6154255948731944   4.6154255948731944    0.0E+00       72.64
   17        4.7920337483105797   4.7920337483105788    8.9E−16        6.42
   18        4.8637033051562728   4.8637033051562728    0.0E+00        9.62
   19        4.8637033051562728   4.8637033051562728    0.0E+00       12.20
   20        5.1223207369915293   5.1223207369915285    8.9E−16        8.94
   21        5.2523174750102433   5.2523174750102424    8.9E−16       36.89
   22        5.4397189590722146   5.4397189590722137    8.9E−16       86.94
   23        5.5452042225748590   5.5452042225748581    8.9E−16      147.69
   24        5.6516610917654377   5.6516610917654369    8.9E−16       29.95
   25        5.7528243308571163   5.7528243308571154    8.9E−16      464.85
   26        5.8281765369429506   5.8281765369429497    8.9E−16       44.52
   27        5.9063978473941567   5.9063978473941550    1.8E−15     2535.80
   28        6.0149380973715152   6.0149380973715125    2.7E−15    14142.00
   29        6.1385979039781473   6.1385979039781455    1.8E−15      100.01
   30        6.1977410708792275   6.1977410708792258    1.8E−15      267.66
   31        6.2915026221291814   6.2915026221291814    0.0E+00       71.14
   32        6.4294629709501150   6.4294629709501132    1.8E−15      790.47
   33        6.4867381281037089   6.4867031235604333    3.5E−05    14955.90
   34        6.6109570900010040   6.6109570900010031    8.9E−16    13744.63
   35        6.6971710917902456   6.6971710917902438    1.8E−15     3260.99
   36        6.7467537934241761   6.7467537934241752    8.9E−16      259.48
   37        6.7587704831436346   6.7587704831436337    8.9E−16     1092.96
   38        6.9618869652281514   6.9618869652281488    2.7E−15      641.64
   39        7.0578841626240081   7.0578841626240045    3.6E−15      245.79
   40        7.1238464359431282   7.1238464359431246    3.6E−15      273.25
   41        7.2600123286770479   7.2600123286770462    1.8E−15      637.95
   42        7.3469494647914715   7.3467964069427687    1.5E−04     5287.91
   43        7.4199448563412131   7.4199448563412114    1.8E−15     3610.53
   44        7.4980366829952523   7.4980366829952487    3.6E−15     1232.29
   45        7.5729123263675255   7.5729123263675211    4.4E−15     3264.80
   46        7.6501799146936715   7.6501799146936680    3.6E−15      856.59
   47        7.7241700525980201   7.7241700525980184    1.8E−15     2506.63
   48        7.7912714305586714   7.7912714305586679    3.6E−15    12961.80
   49        7.8868709588028691   7.8868709588028647    4.4E−15    14312.55
   50        7.9475152747835143   7.9475152747835107    3.6E−15     1605.08

Table 1: Optimal results for the packing
                                 14      of unitary circles in a circle
# of items       Square side            Reference        Diﬀerence      Time
   1          2.0000000000000000    2.0000000000000000    0.0E+00        0.00
   2          3.4142135623730949    3.4142135623783694   -5.3E−12        0.00
   3          3.9318516525781364    3.9318516525819986   -3.9E−12        0.01
   4          4.0000000000000000    4.0000000000000000    0.0E+00        0.00
   5          4.8284271247461898    4.8284271247356418    1.1E−11        0.01
   6          5.3282011773513762    5.3282011773649129   -1.4E−11        0.48
   7          5.7320508075688776    5.7320508075691876   -3.1E−13        2.29
   8          5.8637033051562746    5.8637033051581451   -1.9E−12        4.56
   9          6.0000000000000000    5.9999999999879998    1.2E−11        0.69
   10         6.7474415232381135    6.7474415232485301   -1.0E−11       43.44
   11         7.0225095034303822    7.0225095034205376    9.8E−12      456.84
   12         7.1449575542752672    7.1449575542971164   -2.2E−11      126.30
   13         7.4631768820241113    7.4630478288597386    1.3E−04        2.96
   14         7.7320508075688776    7.7320508075709107   -2.0E−12       13.44
   15         7.8637033051562764    7.8637033051639973   -7.7E−12      135.58
   16         8.0000000000000000    8.0000000000000000    0.0E+00        0.00
   17         8.5326603474980978    8.5326603474943603    3.7E−12      109.89
   18         8.6564023547027524    8.6564023547027134    3.9E−14       13.93
   19         8.9074609393260822    8.9074609393257855    3.0E−13        5.78
   20         8.9780833528217379    8.9780833528604074   -3.9E−11        5.56
   21         9.3580199588727577    9.3580199588783994   -5.6E−12      758.56
   22         9.4639295431339381    9.4638450909735710    8.4E−05       12.73
   23         9.7274066103125492    9.7274066102921175    2.0E−11     4447.51
   24         9.8637033051562764    9.8637033051186727    3.8E−11      233.46
   25        10.0000000000000000   10.0000000000000000    0.0E+00        0.84
   26        10.3774982039134294   10.3774982039012666    1.2E−11       96.25
   27        10.4799830400508842   10.4799830400439067    7.0E−12      974.71
   28        10.6754536943453164   10.6754536943208187    2.4E−11       80.53
   29        10.8151200175936939   10.8151200176298907   -3.6E−11       21.42
   30        10.9085683308339956   10.9085683308326153    1.4E−12       28.21
   31        11.1934033520469818   11.1934033520763752   -2.9E−11      155.25
   32        11.3819824265232441   11.3819824264966716    2.7E−11      438.73
   33        11.4641016151377571   11.4639440323935258    1.6E−04      115.67
   34        11.7274066103125492   11.7274066102475238    6.5E−11     6428.40
   35        11.8637033051562764   11.8637033052067267   -5.0E−11     1802.77
   36        12.0000000000000000   12.0000000000480007   -4.8E−11       29.29
   37        12.1818588307319349   12.1817863967843891    7.2E−05     6577.27
   38        12.2389635913615287   12.2384376438652254    5.3E−04     6889.47
   39        12.2899151085505363   12.2899151085466070    3.9E−12      112.60
   40        12.6283749264972833   12.6283749265423863   -4.5E−11     2133.86
   41        12.7469384531873313   12.7469384531744172    1.3E−11      198.40
   42        12.8532221454500828   12.8532221454774298   -2.7E−11       67.83
   43        13.0994720835212828   13.0993251411339831    1.5E−04     2055.75
   44        13.1958675394493774   13.1957481262430427    1.2E−04     8522.40
   45        13.3819824265232477   13.3819824265206115    2.6E−12      510.51
   46        13.4641016151377588   13.4639878881361117    1.1E−04      151.07
   47        13.6775877082279198   13.6774298825312073    1.6E−04     4731.81
   48        13.8059970535441412   13.8059970536389738   -9.5E−11     2214.69
   49        13.9484250865937067   13.9484250865204586    7.3E−11     1334.68
   50        14.0124815721935416   14.0100949163104573    2.4E−03    12245.42

Table 2: Optimal results for the packing
                                  15     of unitary circles in a square
   # of items    Rectangle length       Rectangle width        Rectangle area        Time
        1        2.0000000000000000    2.0000000000000000     4.0000000000000000      0.00
        2        4.0000000000000000    2.0000000000000000     8.0000000000000000      0.00
        3        6.0000000000000000    2.0000000000000000    12.0000000000000000      0.00
        4        8.0000000000000000    2.0000000000000000    16.0000000000000000      0.00
        5       10.0000000000000000    2.0000000000000000    20.0000000000000000      0.00
        6        4.0000000000000000    6.0000000000000000    24.0000000000000000      0.34
        7        2.0000000000000000   14.0000000000000000    28.0000000000000000      0.66
        8        8.0000000000000000    4.0000000000000000    32.0000000000000000      1.50
        9        6.0000000000000000    6.0000000000000000    36.0000000000000000      0.01
       10       10.0000000000000000    4.0000000000000000    40.0000000000000000      0.00
       11        8.0000000000000018    5.4641016151377553    43.7128129211020493     11.20
       12        8.0000000000000000    6.0000000000000000    48.0000000000000000      4.40
       13       26.0000000000000000    2.0000000000000000    52.0000000000000000      7.24
       14        5.4641016151377553   10.0000000000000018    54.6410161513775634     12.46
       15        3.7320508075688776   16.0000000000000036    59.7128129211020564      8.70
       16        3.7320508075688776   17.0000000000000036    63.4448637286709314     15.01
       17        5.4641016151377553   12.0000000000000018    65.5692193816530704     31.35
       18        3.7320508075688776   19.0000000000000036    70.9089653438086884     61.10
       19        7.4641016151377562   10.0000000000000018    74.6410161513775705      8.64
       20       14.0000000000000036    5.4641016151377553    76.4974226119285987      0.01
       21       15.0000000000000036    5.4641016151377553    81.9615242270663487      0.02
       22        3.7320508075688776   23.0000000000000036    85.8371685740842025     26.52
       23        5.4641016151377553   16.0000000000000036    87.4256258422040986      8.07
       24        5.4641016151377553   17.0000000000000036    92.8897274573418628     35.01
       25        3.7320508075688776   26.0000000000000071    97.0333209967908488     23.36
       26        5.4641016151377553   18.0000000000000036    98.3538290724796127    114.36
       27        5.4641016151377553   19.0000000000000036   103.8179306876173627     10.10
       28       12.0000000000000036    8.9282032302755123   107.1384387633061834     80.71
       29       20.0000000000000036    5.4641016151377553   109.2820323027551268     82.37
       30        5.4641016151377553   21.0000000000000036   114.7461339178928768     10.10
       31        3.7320508075688776   32.0000000000000071   119.4256258422041128     58.06
       32        5.4641016151377553   22.0000000000000036   120.2102355330306409    176.39
       33       14.0000000000000053    8.9282032302755123   124.9948452238572258   1687.60
       34        7.1961524227066338   18.0000000000000036   129.5307436087194333    140.46
       35       24.0000000000000036    5.4641016151377553   131.1384387633061408     53.59
       36       25.0000000000000071    5.4641016151377553   136.6025403784439334    185.56
       37        5.4641016151377553   25.8612097182042078   141.3082777906558363   2353.71
       38       26.0000000000000071    5.4641016151377553   142.0666419935816691     38.55
       39       27.0000000000000071    5.4641016151377553   147.5307436087194333    301.99
       40        7.1961524227066338   21.0000000000000036   151.1192008768393293    333.47
       41        5.4641016151377553   28.0000000000000071   152.9948452238571974    244.77
       42       22.0000000000000036    7.1961524227066338   158.3153532995459614    285.47
       43       18.0000000000000071    8.9282032302755123   160.7076581449592823    389.22
       44        5.4641016151377553   30.0000000000000071   163.9230484541326973   1447.03
       45        5.4641016151377553   31.0000000000000071   169.3871500692704615    503.78
       46        7.1961524227066338   24.0000000000000036   172.7076581449592254    485.91
       47        5.4641016151377553   32.0000000000000071   174.8512516844081972    520.40
       48       20.0000000000000071    8.9282032302755123   178.5640646055103105   3034.99
       49        5.4641016151377553   33.8612097182042078   185.0210907117578643   5101.41
       50        5.4641016151377553   34.0000000000000071   185.7794549146837255     83.78

Table 3: Optimal results for the packing of16unitary circles in a rectangle (min. L × W )
  # of items    Rectangle length       Rectangle width     Rectangle semiperimeter      Time
      1         2.0000000000000000    2.0000000000000000       4.0000000000000000        0.00
      2         4.0000000000000000    2.0000000000000000       6.0000000000000000        0.00
      3         3.7320508075688776    4.0000000000000000       7.7320508075688776        0.00
      4         4.0000000000000000    4.0000000000000000       8.0000000000000000        0.17
      5         4.0000000000000000    5.4641016151377544       9.4641016151377535        0.24
      6         4.0000000000000000    6.0000000000000000      10.0000000000000000        0.32
      7         5.8612097182041998    5.4641016151377553      11.3253113333419542        1.06
      8         5.4641016151377553    6.0000000000000009      11.4641016151377571        1.50
      9         6.0000000000000000    6.0000000000000000      12.0000000000000000        0.01
     10         7.1961524227066338    6.0000000000000009      13.1961524227066356       44.93
     11         6.0000000000000009    7.4641016151377562      13.4641016151377571        3.62
     12         6.0000000000000000    8.0000000000000000      14.0000000000000000        3.79
     13         7.4626564857803901    7.4632672693142670      14.9259237550946580     1944.55
     14         7.1961524227066338    8.0000000000000018      15.1961524227066356       42.44
     15         8.0000000000000018    7.4641016151377562      15.4641016151377571       14.93
     16         8.0000000000000000    8.0000000000000000      16.0000000000000000       24.32
     17         8.9282032302755123    7.9427193491449888      16.8709225794205011      737.93
     18         8.0000000000000036    8.9282032302755123      16.9282032302755141      287.59
     19         7.4641016151377562   10.0000000000000018      17.4641016151377571        7.37
     20         8.9282032302755123    9.0000000000000036      17.9282032302755141      556.65
     21         9.4337452285295686    9.2209018981307658      18.6546471266603362      113.34
     22         9.9427193491449888    8.9282032302755123      18.8709225794205011      979.18
     23         8.9282032302755123   10.0000000000000036      18.9282032302755141      421.24
     24         9.4641016151377553   10.0000000000000000      19.4641016151377571       86.33
     25        11.0000000000000036    8.9282032302755123      19.9282032302755141      213.47
     26        10.6602540378443891    9.9427193491449888      20.6029733869893761     3528.82
     27        10.6602540378443891   10.0000000000000036      20.6602540378443926       88.10
     28        12.0000000000000036    8.9282032302755123      20.9282032302755141       74.90
     29         9.4641016151377571   12.0000000000000018      21.4641016151377571       20.58
     30        10.6602540378443891   11.0000000000000036      21.6602540378443926      436.24
     31        10.9282032302755141   11.4265717909344140      22.3547750212099281     2237.26
     32        11.9427193491449870   10.6602540378443891      22.6029733869893761     1417.69
     33        12.0000000000000036   10.6602540378443891      22.6602540378443926      214.35
     34        10.9282032302755123   12.0000000000000036      22.9282032302755141      731.71
     35        12.3923048454132676   11.0000000000000036      23.3923048454132712      133.13
     36        10.6602540378443891   13.0000000000000071      23.6602540378443962       82.16
     37        12.3923048454132676   11.8612097182042024      24.2535145636174718     7399.74
     38        11.9841557353269081   12.3924132707237522      24.3765690060506586     2891.91
     39        12.3923048454132676   12.0000000000000036      24.3923048454132712     3329.17
     40        12.9282032302755123   12.0000000000000036      24.9282032302755141      155.32
     41        12.3923048454132676   12.9427193491449888      25.3350241945582582     6254.69
     42        12.3923048454132676   13.0000000000000071      25.3923048454132747     1650.45
     43        13.6029140930960750   12.3923268915991969      25.9952409846952719     1035.43
     44        13.8844501917489893   12.3923048454132712      26.2767550371622605    13131.52
     45        13.9841229965638760   12.3923048454132676      26.3764278419771436     1069.14
     46        14.0000000000000071   12.6602540378443891      26.6602540378443962     1879.21
     47        14.0000000000000071   12.9282032302755123      26.9282032302755212     1281.24
     48        13.0000000000000071   14.1243556529821479      27.1243556529821532     1709.87
     49        12.3923048454132676   15.0000000000000071      27.3923048454132747     7546.82
     50        12.3923048454132712   15.6028097181778964      27.9951145635911658     6366.25

Table 4: Optimal results for the packing of17unitary circles in a rectangle (min. L + W )
      # of items      Triangle side        Time    # of items       Strip length         Time
          1         3.4641016151377545      0.00       1         2.0000000000000000       0.00
          2         5.4641015260409098      0.00       2         1.9999999999999998       0.04
          3         5.4641015582188635      0.05       3         1.9999999999999998       0.02
          4         6.9282031370137620      0.03       4         1.9999999999999998       0.04
          5         7.4641015438602771     54.72       5         2.6959705453537524       0.02
          6         7.4641015587429127    206.36       6         3.3228756555322954       0.00
          7         8.9282031100914168      0.18       7         3.5612494995995996       0.01
          8         9.2938099467443216     12.95       8         3.6887986310766987       0.07
          9         9.4641015510046618    25.109       9         3.9996673748986948       9.17
         10         9.4641015666630892      0.37      10         4.6959705453537524       0.04
         11        10.7300878190524358     13.38      11         5.1224989991991992       0.05
         12        10.9282031596736786      4.22      12         5.3775972621533974       2.42
         13        11.4064957458284422     80.55      13         5.8538814987957917     840.02
         14        11.4641015604162533   1122.57      14         5.9993347497973915    1112.34
         15        11.4641015695434394     24.63      15         6.6959705453537559       0.02
         16        12.7136286310567250   2186.82      16         7.0663958932300979       5.33
         17        12.9282031457004436     49.64      17         7.4525364626094142       7.98
         18        13.2937904231493249    121.93      18         7.8539155052528402     687.63
         19        13.4480543405474720    223.02      19         7.9996778073991033    2515.58
         20        13.4641015644155306     20.57      20         8.6959705453537559      40.77
         21        13.4641015778907409     42.47      21         9.1732901304367189    3185.98
         22        14.6125656032291964    413.39      22         9.4524415753023714      31.15
         23        14.8826696938712466   2117.64      23         9.8537288511462791    2537.63
         24        14.9282031609796402    373.50      24         9.9993623469257145     161.81
         25        15.2938099693721306      1.18      25        10.6959705453537577       0.66
         26        15.4589390002039853   1067.00      26        11.1733168632638993    2878.17
         27        15.4641015656802985      6.78      27        11.4522265853969465     267.37
         28        15.4641015817250107    782.69      28        11.8539308197359858      94.54
         29        16.6056026842964179   2708.93      29        11.9993600450532973     857.99
         30        16.7300878617292312     24.34      30        12.6959705453537595       1.32
         31        16.9282031492725551    158.16      31        13.1733140056536673   10490.33
         32        17.2474929494386764    179.30      32        13.4519215824209422    7042.79
         33        17.4064957212102627    128.48      33        13.8515722749965562     663.65
         34        17.4635536344819791    568.62      34        13.9993894685688876    2806.64
         35        17.4641015734708560     82.36      35        14.6959705453537612       8.50
         36        17.4641015898910545     48.32      36        15.1731171516082881    5723.33
         37        18.5312410691358664   1463.95      37        15.4520220872811613    1503.56
         38        18.7298248517387407    395.28      38        15.8330120530395764     504.22
         39        18.9160916884815435   1210.17      39        15.9999999998085887    1014.63
         40        18.9282031752999664    658.87      40        16.6959705453537595      14.86
         41        19.2938099551359308    639.66      41        17.1729034249762442    6632.41
         42        19.4064957825474025     26.92      42        17.4516358985406050    2548.92
         43        19.4635536523988257   1459.48      43        17.8140606308452512    2577.70
         44        19.4641015803674549   1370.20      44        17.9993696642869736   12212.56
         45        19.4641015941498345     10.92      45        18.6959705453537630       3.66
         46        20.5275000891198900   3295.17      46        19.1726994816344884    1476.64
         47        20.7032882042547612   1837.24      47        19.4518331606560650   14077.38
         48        20.8825408318815278   1526.27      48        19.7495596428938782    6813.48
         49        20.9282031663479380    501.34      49        19.9993724839986804    3527.02
         50        21.2464302653662145    569.27      50        20.6959705453537630       4.96

Table 5: Optimal results for the packing of unitary
                                             18     circles in a triangle and a strip (L = 9.5)
References
[1] R. Andreani, E. G. Birgin, J. M. Martínez, and M. L. Schuverdt, Augmented Lagrangian methods
    under the Constant Positive Linear Dependence constraint qualification, Mathematical Programming
    111 (2008), 5–32.
[2] R. Andreani, E. G. Birgin, J. M. Martínez, and M. L. Schuverdt, On Augmented Lagrangian methods
    with general lower-level constraints, SIAM Journal on Optimization 18 (2007), 1286–1309.
[3] E. G. Birgin, R. Castillo, and J. M. Martínez, Numerical comparison of Augmented Lagrangian algo-
    rithms for nonconvex problems, Computational Optimization and Applications 31 (2005), 31–56.
[4] E. G. Birgin and J. M. Martínez, Structured minimal-memory inexact quasi-Newton method and secant
    preconditioners for Augmented Lagrangian Optimization, Computational Optimization and Applications
    39 (2008), 1–16.
[5] E. G. Birgin, J. M. Martínez, W. F. Mascarenhas, and D. P. Ronconi, Method of sentinels for packing
    items within arbitrary convex regions, Journal of the Operational Research Society 57 (2006), 735–746.
[6] E. G. Birgin, J. M. Martínez, F. H. Nishihara, and D. P. Ronconi, Orthogonal packing of rectangular
    items within arbitrary convex regions by nonlinear optimization, Computers & Operations Research 33
    (2006), 3535–3548.
[7] E. G. Birgin, J. M. Martínez, and D. P. Ronconi, Optimizing the packing of cylinders into a rectangular
    container: a nonlinear approach, European Journal of Operational Research 160 (2005), 19–33.
[8] E. G. Birgin and F. N. C. Sobral, Minimizing the object dimensions in circle and sphere packing problems,
    Computers & Operations Research 35 (2008), 2357–2375.
[9] J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics, vol. 244, Springer–
    Verlag, New York, 2008.
[10] J. E. Dennis Jr. and R. B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear
     Equations, Classics in Applied Mathematics, SIAM Publications, Philadelphia, 1996.
[11] G. H. Golub and C. F. Van Loan, Matrix Computations, The Johns Hopkins University Press, Baltimore,
     1996.
[12] M. Locatelli and U. Raber, Packing equal circles in a square: a deterministic global optimization ap-
     proach, Discrete Applied Mathematics 122 (2002), 139–166.
[13] C. D. Maranas, C. A. Floudas, and P. M. Pardalos, New results in the packing of equal circles in a
     square, Discrete Mathematics 142 (1995), 287–293.
[14] N. Mladenović, F. Plastria, and D. Urošević, Reformulation descent applied to circle packing problems,
     Computers & Operations Research 32 (2005), 2419–2434.
[15] K. J. Nurmela and P. R. Östergård, Packing up to 50 equal circles in a square, Discrete & Computational
     Geometry 18 (1997), 111–120.
[16] E. Specht, Packomania (January 20, 2009), available at http://www.packomania.com.
[17] Y. G. Stoyan, Mathematical methods for geometric design, Advances in CAD/CAM (T. M. R. Ellis and
     O. J. Semenkoc, eds.), Proceedings of PROLAMAT 82, Leningrad and Amsterdam, 1983, pp. 67–86.
[18] Y. G. Stoyan and G. N. Yas’kov, Mathematical model and solution method of optimization problem of
     placement of rectangles and circles taking into account special constraints, International Transactions in
     Operational Research 5 (1998), 45–57.
[19] Y. G. Stoyan and G. N. Yas’kov, A mathematical model and a solution method for the problem of placing
     various-sized circles into a strip, European Journal of Operational Research 156 (2004), 590–600.

                                                      19
[20] Y. G. Stoyan, G. N. Yas’kov, and G. Scheithauer, Packing spheres of various radii into a parallelepiped,
     Technical Report MATH-NM-15-2001, TU, Dresden, 2001.
[21] D. Zhang and A. Deng, An effective hybrid algorithm for the problem of packing circles into a larger
     containing circle, Computers & Operations Research 32 (2005), 1941–1951.
[22] D. Zhang and W. Huang, A Simulated Annealing Algorithm for the Circles Packing Problem, Compu-
     tational Science — ICCS 2004, Lecture Notes in Computer Science, vol. 3036, Springer–Verlag, Berlin
     and Heidelberg, 2004, pp. 206–214.




                                                     20
