          Dense Packings of Equal Spheres in a Cube
                                           Th. Gensane
              Laboratoire de Mathématiques Pures et Appliquées Joseph Liouville,
                  50, rue F. Buisson, BP 699, 62228 Calais Cedex, FRANCE
                              gensane@lmpa.univ-littoral.fr

           Submitted: Jun 6, 2003; Accepted: May 20, 2004; Published May 27, 2004
                          MR Subject Classification: 52C17, 05B40.


                                               Abstract
          We describe an adaptation of the billiard algorithm for finding dense packings
      of equal spheres inside a domain of the euclidean space. In order to improve the
      convergence of this stochastic algorithm, we introduce systematic perturbations in
      it. We apply this perturbed billiard algorithm in the case of n spheres in a cube
      and display all the optimal and best known packings up to n = 32. We improve
      the previous record packings for all 11 ≤ n ≤ 26 except n = 13, 14, 18. We prove
      the existence of the displayed packings for n = 11, 12, 15, 17, 20, 21, 22, 26, 32, by
      constructing them explicitly. For example, the graph of the conjectured optimal
      packing of twenty-two spheres is composed of five octahedrons and four isolated
      points. We also conjecture that the minimum distance dn between spheres centers
      of the optimal packings is constant in the range 29 ≤ n ≤ 32.


1     Introduction
We first consider the maximum separation problem in a domain K of the euclidean space
E d : how to spread n points p1 , · · · , pn inside K so that the minimum distance is as large
as possible. This formulation is often used by the authors dealing with the disk packing
problem which consists in determining the maximum diameter of n equal non-overlapping
disks contained in K. A discussion about the equivalence between the two problems
can be found in [M]. For other presentations of the subject and related questions, see
[CFG, SK, T, Z]. It appears in the mathematical literature that there is no domain
where the solution of the problem is obvious. Moreover, it is significant that the regular
hexagonal packings of n = k(k+1)
                              2
                                    disks in the equilateral triangle compose the only infinite
family of optimal packings known and proved [O]. We note that [GL1] have presented
conjectured optimal packings, always in the equilateral triangle, for other infinite classes
of n.
     Recently, some progresses have been made in computer aided proofs [GMPW, N02] as
well as in geometric algorithms: the billiard algorithm introduced in [L, LS, GL1, GL2]

the electronic journal of combinatorics 11 (2004), #R33                                        1
opens a comprehensible and efficient way of finding numerical challenger configurations.
Some improvement has also been made in [BDGL]; [GLNO] compare such algorithms
with more classical algorithms.
    We can think of billiard algorithms as stochastic methods. Indeed, the first version of
these algorithms simulates the idealized movement of billiard balls inside a domain, the
initial centers of the balls and their directions being randomly fixed. The so obtained
packings are the fruit of these probabilistic choices.
    In Section 2, we are going to develop the billiard algorithm in a more stochastic way.
The hard spheres do not move along straight lines but randomly around themselves, and
realize in Algorithm 1 a random walk. In Algorithm 2, the magnitude of the stochastic
movements is progressively reduced when the spheres, when growing, yield a rigid posi-
tion. Simultaneous perturbations of all the spheres will be introduced in Algorithm 3; in
Algorithm 4, we alternate those perturbations and Algorithm 2. We finish in Section 3
with some results of sphere packings in a cube and we display all optimal and best known
packings for 2 ≤ n ≤ 32. We show that contrary to the two-dimensional case, our billiard
algorithm and probably the earlier ones are not able to produce all optimal packings with
a good accuracy without using perturbations.
    In the following, we denote by
K ⊂ IRd a convex compact subset and ∂K its boundary,
P = (p1 , · · · , pn ) ∈ Kn a configuration of n points,
d(p, q) the euclidean distance,
B(p, ε) = {q ∈ IRd : d(p, q) < ε} the open ball of radius ε centered at p,
S(p, ε) = ∂B(p, ε) the sphere of radius ε centered at p,
f (P) = mini6=j d(pi , pj ) the minimum mutual distance between the points of P,
dn = maxP f (P) the maximum separation distance of n points in K,
K−r = {x ∈ K : B(x, r) ⊂ K} the inner parallel body of K,
      S
Kr = x∈K B(x, r) the outer parallel body (or tubular neighborhood) of K,
prK (p) the nearest point in K to p ∈ IRd (the existence of which is guaranteed by the
convexity of K),
UK the uniform law of probability on K.
    We recall the following definition found in [D]: to any configuration P, we associate
an unoriented simple graph G = G(P) whose vertices are the points pi of P and whose
edges are the segments pi pj with d(pi , pj ) = f (P). A vertex pi is called isolated if there
is no edge containing pi .


2     A stochastic algorithm
We now assume that K is an erosion-similar body, see [M, p.75]: there is an r0 > 0 such
that for all r ∈ [0, r0 [, there exists a composition Sr of a rotation, a homothety and a
translation which gives Sr (K) = Kr . It is shown [M, p.78] that under this assumption, the
maximum separation problem and the disk packing problem are equivalent. It is therefore



the electronic journal of combinatorics 11 (2004), #R33                                     2
the same to consider the move of the points pi inside K or the move of the hard spheres
S(pi , f (P)/2) of the associated packing in Kf (P)/2 .
   Classical billiard algorithms contain statements which compute the directions of the
various spheres before and after the shocks. In contrast, our procedures do not include
explicit calculations of those directions.
   We consider two types of sphere motion.
   The first one consists of a random walk of the n spheres. The spheres move one after
the other, if a center pi is moved to z ∈  / K the procedure Random Walking displaces
pi to prK (z). If a displaced sphere overlaps another one, the move is not executed. We
formalize this through the following algorithm: the variable Na is the number of move
attempts, the real number ε represents the maximal magnitude of the moves, α is the
common radius of the n spheres (which is constant during the whole procedure).
     • Algorithm 1: Procedure Random Walking(P, Na , ε, α)
     For k from 1 to Na do:
       •Choose randomly (or sequentially) a point pi in P
       •Choose z following UB(pi ,ε)
       •If z ∈
             / K then z := prK (z)
       •If minj6=i d(z, pj ) ≥ α ,then pi := z
   After running the procedure Random Walking(P, Na , ε, α) with α = f (P), we
obtain a new configuration P such that f (P) ≥ α; the packing associated to P is better
than the initial packing if the walk allows to improve the smallest distance between the
centers pi .
   We are now able to give an algorithm similar to the first phase given in [BDGL]: first,
the configuration P is randomly chosen in Kn , the real number ε1 is the initial value of ε
in Random Walking, ε2 is the threshold of the procedure.
    • Algorithm 2: Procedure Stochastic Billiard(P, ε1 , ε2 , Na )
     ε = ε1
     α = f (P)
     While ε > ε2 do:
       •Random Walking(P, Na , ε, α)
       •If f (P) > α then ε := 2 ∗ ε and α := f (P) else ε := ε/2.
   The diameter f (P) of the spheres is increased throughout the procedure Stochastic
Billiard as is plainly shown by the last statement α := f (P) in Algorithm 2.
   The second type of motions is a simultaneous perturbation of all the spheres. Those
perturbations will be used in a systematic way before the packings become too rigid.
   Let us begin with some definitions. As usual, we consider that a configuration P is
locally optimal if
                   ∃ε > 0 , ∀Q ∈ Kn , (∀i : d(qi , pi ) < ε) ⇒ f (Q) ≤ f (P) .
    The billiard algorithms (we now include in that class the procedure Stochastic Bil-
liard) lead to configurations which are sometimes locally optimal but in any case solid in

the electronic journal of combinatorics 11 (2004), #R33                                  3
the following sense: it is impossible to improve the minimum distance of the configura-
tion by moving some spheres of the associated packing, one after the other and without
overlaps (a same sphere of center pi can be moved several times).
    Our aim in Algorithm 4 is to produce locally optimal packings, taking into account the
degree of freedom of the graph G(P) as defined in [D]. In fact, we hope that our algorithm
will be able to realize a discretization of a path h in the set of solid configurations. More
precisely, we can think of h as a continuous map from [0, 1] to Kn which satisfies:
    • h(0) = P,
    • for each t ∈ [0, 1], h(t) = (h1 (t), · · · , hn (t)) is a solid configuration,
    • f ◦ h is an increasing map,
    • h(1) is a locally optimal configuration.
    A solid configuration P = P0 (or a quasi-solid in the algorithm) will be alternately per-
turbed by the procedure With Perturbations and improved by the procedure Stochas-
tic Billiard. If the new packing P is better, we increase the magnitude ε. If an endeavour
ends in failure, we restore the previous position P0 and decrease ε. The variable f actor
gives the threshold ε/f actor (we have used in practice f actor = 105 , it is also possible
to fix for instance the ratio ε/f actor to 10−12 in the call of Stochastic Billiard ). The
procedure With Perturbations generates a sequence P1 , P2 , · · · , Pm of quasi-solid con-
figurations with f (Pi+1 ) > f (Pi ). This sequence can be considered as a discretization of a
path of solid configurations, although we know that the existence of the continuous map
h is far from being proved.
     • Algorithm 3: Procedure Perturbation(P, ε)
     For i from 1 to n do:
       • Choose z following UB(pi ,ε)
       • If z ∈ K then pi := z else pi := prK (z)

    • Algorithm 4: Procedure With Perturbations(P, ε1 , ε2 , f actor)
     ε := ε1
     P0 := P
     α0 := f (P).
     While ε > ε2 do
        • Perturbation(P, ε)
        • Stochastic Billiard(P, ε, ε/f actor, Na )
        • If f (P) > α0 then α0 := f (P) and ε := 2 ∗ ε,
                        else P := P0 and ε := ε/2


3     Dense packings of equal spheres in a cube
The problem of packing n congruent spheres in a unit cube C was raised apparently in
1966 in [S1]. It is shown in that paper that any optimal configuration contains at least
one point on every face of C (in fact, the same is true for any parallelotope). The author


the electronic journal of combinatorics 11 (2004), #R33                                     4
also gave the solutions for n = 2, 3, 4, 5, 6, 8, 9, the case n = 10 have been treated in [S2].
These results are the only ones of optimality proved in the cube.
    By investigating among the various possible symmetric packings, [Go] described good
packings up to twenty-seven spheres. In fact, our computations have shown that all these
packings except for n = 13, 14, 18, 27 are not optimal; we are confident in the optimality
of these four surviving cases.
    How have we proceeded? It appears that the procedure With Perturbations gives
good approximations of local optima. Nevertheless, certain solid configurations calculated
by our procedures are both non-locally optimal and tantalizingly rigid (the most difficult
computations were for n = 12, 25 and 28). So, we intend to execute the procedure With
Perturbations on packings which are not too rigid and close to a global optimum.
    In order to find such packings, we have sampled results obtained by the procedure
Stochastic Billiard with small values for the parameters Na and ε2 (for instance Na =
600, ε2 = 10−6 and always ε1 = 0.1). The best packing obtained during the sample
becomes the starting point of the procedure With Perturbations. In this second phase,
and up to thirty-two points, the values Na = 800, ε1 = 0.1, ε2 = 10−12 and f actor = 105
have often given very good results: except for n = 28, all results in Table 2 have been
several times obtained with twelve decimal digits of accuracy.
    In the following and relatively to n points, we will denote by P (n) the best configuration
found. For convenience, we will give the coordinates of the points pi in the cube [−1, 1]3 .
But as usual, the values f (P (n) ) will be given relatively to a unit cube.
    We are aware that the earlier billiard algorithms should have found many of the config-
urations below if they had been simply adapted to the three-dimensional case. Similarly,
our algorithm Stochastic Billiard produces, without using systematic perturbations, all
optimal and best known disk packings in the square given by [NO1, BDGL]. Nevertheless,
the procedure With Perturbations appears to us indispensable in the three-dimensional
case for n = 12, 19, 21, 25, 28. The two following examples illustrate that the acceleration
of the convergence given by Algorithm 4 is unquestionable.
     For n = 12, a sample of 10000 runs of Stochastic Billiard(P, 0.1, 10−12 , 2000) has
just given six digits of f (P (12) ). These calculations have lasted 20 hours on a computer at
CPU 800 MHz. The algorithm With Perturbations applied to one of the good packings
given by the sample gives six new digits in 30 minutes.
     For n = 21, 250 runs of Stochastic Billiard√and one hour of calculations are
needed to obtain just two digits of f (P (21) ) = 3(1 + 3)/2. Then, the algorithm With
Perturbations gives in one hour the twelve first digits of this number.
    We finish our discussion by considering the cases for which the perturbations are not
necessary. We display in Table 1, for n ≥ 11, the frequency of obtaining f (P (n) ) with
twelve digits of accuracy, running Stochastic Billiard and the necessary average time
to reach them.
    Let us finally precise that the association of a small sample of Stochastic Billiard
with one run of With Perturbations gives the best found packing of 24 spheres in 4
minutes instead of 40 minutes when we do not use perturbations.



the electronic journal of combinatorics 11 (2004), #R33                                      5
                    n             11        14         15         16      17      18
                                   1         1            1         1      1      3
                Frequency         140        2            50       40      5      4
                  Time         13 min      11 s     10 min      7 min     50 s   12 s
                    20           22         23        24          26       27     32
                      1            1         1            1         1      1      1
                      5           20         25           50       25      10     2
                   1 min        5 min     3 min     40 min 12 min 5min           1min

   Table 1: Frequency of obtaining f (P (n) ) with Algorithm 2 and average CPU time.

    For each value of n, we have tried to give an exact value of the conjectured minimum
distance dn . For some best packings, the theorem of Pythagoras is sufficient to find
an equation verified by dn . In that case and for n = 15, 17, 21, 22, 32, the packing is
completely described and we know that the packing associated to the displayed graph
actually exists.
    In any case, the graphs suggested by the computer experiments lead us to conjecture
a set of polynomial equations verified by the coordinates of centers pi . Those equations
are far from being easily solved, and it is sometimes possible, like in [GMPW], to reduce
the order of the system by taking into consideration the symmetries of the configuration
and using a Gröbner basis package. For n = 11, 12, 20, 26, the reduction has been made
with Mathematica and we also obtain a proof that the displayed graph corresponds to an
existing packing; see below the case n = 11 for more details. When the reduction fails,
we do not dispose of such a proof.
    It is clear that our experiments have given configurations of points the coordinates of
which are decimal numbers with, say, 12 digits. An exact calculation with 24 digits of
accuracy gives the exact value of x = f (P (n) )2 . Now, the graph of the configuration has
often just only one edge and we need to conjecture where are the true contacts of the
optimal packing close to P (n) . Inspired by [BDGL, p.6], we have adopted the following
rule :
               pi pj is an edge of the displayed graph iff d2 (pi , pj ) − x < 10−12 .
It is then possible to convince oneself that there does not exist other bonds if, for instance,

                                   d2 (pi , pj ) − x ∈
                                                     / [10−12 , 10−6 ].

For the cases n = 16, 19, 23, 24, 25, 28, we have effectively obtained [10−12 , 10−6] with an
exact calculation as clear-cut bond identification interval.
    We will use ellipsis dots to finish the decimal expansion of any mathematical quantity,
as for instance a root of a polynomial. Otherwise, the numbers calculated with a computer
will be displayed without ellipsis dots and rounded.
• Cases n = 2 to n = 6, see [S1] and Figure 1 .
• Case n = 7, Figure 1. A configuration P with f (P) = 1.00091 · · · is proposed in [S1].
But in [S2], Schaer made clear that this result is not optimal and that d7 is approximately
1.001089825. We confirm this result and give in Figure 1 the graph of P (7) in C and its

the electronic journal of combinatorics 11 (2004), #R33                                       6
associated packing in Cf (P (7) )/2 which, to our knowledge, have not been published yet.
The graph suggests that the configuration is mirror-symmetric. Our experimental result
incites us to construct a configuration P with p1 = (1, −1, 1), p2 = (1 − a, 1, 1 − a),
p3 = (−1, a − 1, 1 − a), p4 = (−1, 1, b), p5 = (1 − a, a − 1, −1), p6 = (b, 1, −1) and√ p7 =
                                 2            2             2
(−1, −b, −1). The equalities d (p1 , p5 ) = d (p5 , p6 ) = d (p4 , p6 ) give b = 1−a−   2
                                                                                    √ a + 4a
                       q                                                                √
and a = − √43 + 12 40 3
                        + √163 . This explicit configuration has f (P) = −4+ √10+4
                                                                                 3
                                                                                      3
                                                                                         =
                                                                                        (7)
1.00108924549..., which confirms the result of Schaer and leads us to conjecture that P
is optimal.
• Cases n = 8 to n = 10, see [S2] and Figure 2.
• Case n = 11, Figure 2. Here is the first best packing found having an isolated point; in
fact, it can be placed in the nearest corner and then be transformed into a non-isolated
point. The configuration admits the same symmetry than P (7) . After observing the
graph of P (11) , we define a configuration P of eleven points having p1 = (0, 0, b − 1),
p2 = (−1, 1, −1), p3 = (−1, 1, a − 1), p4 = (c, 1, 1), p5 = (1, d, e), p6 = (1, −1, 1). We get
a polynomial system of five equations of five unknowns that we have reduced using the
Groebner package: f (P (11) ) = a2 = 0.710116382462... where a is the smallest positive root
of the polynomial

         58417408 − 226465792 a + 365612032 a2 − 279190528 a3 + 208614656 a4−
 121983488 a5 − 77183232 a6 + 107515648 a7 − 983968 a8 − 28612736 a9 + 4587840 a10+
             3356352 a11 − 768432 a12 − 167776 a13 + 47376 a14 − 432 a15 + a16 .            (1)

The numbers b, c, d, e are expressed in terms of a:
                     √                     √
                b = a2 − 2, c = −1 + 2 −1 + a, d = f1 (a), e = f2 (a)

where f1 (a) and f2 (a) are well-defined but two large to be displayed. Then, with a
sufficient accuracy in approximating the root of (1), we obtain bounds for b, c, d, e which
show that the points pi are effectively in the cube. Hence, we conclude that the graph of
the constructed configuration P is actually the displayed graph.
• Cases n = 12 to n = 14, Figure 2. Goldberg said in [Go]: “it seems likely that
the best arrangements for thirteen spheres and twelve spheres may be obtained by the
omission of the appropriate number of spheres from the arrangement 14{(1, 4), 4, (1, 4)}”.
The last notation means that the best packing of fourteen spheres is composed of three
layers, that in the first and last layers there is a sphere surrounded by four equally-spaced
spheres, and that four equally-spaced spheres are in the middle layers. Our experiments
have confirmed the results for thirteen and fourteen spheres, but have slightly improved
                                            (12)                           (13)        (14)
the
√ packing of twelve spheres with f (P ) = 0.707106806467 > f (P ) = f (P ) =
  2/2 = 0.707106781186.... In fact, Figure 2 shows a deformation of a packing of twelve
spheres considered by Goldberg. The best configuration found has two mirror-symmetries.
We define a configuration P of twelve points determined by the points p1 = (−1, a, −1),


the electronic journal of combinatorics 11 (2004), #R33                                      7
p2 = (1 − b, 1, −1) on the first layer, the points p3 = (−c, 1 − d, −c), p4 = (1, 0, −e) on the
middle layer and p5 = (1, 1, 1) on the upper layer. The seven other points of P are the
symmetric points of p1 , · · · , p5 with respect to the planes z = x and y = 0. Here again we
have reduced the √ system of five equations verified by a, b, c, d, e and we have found that
    (12)
f (P ) = a = 2 + 2 e + e2 /2 where e is the smallest positive root of
20736 − 289996001280 e + 18856111537152 e2 − 5278350124032 e3 − 24149235663104 e4−
  53456543995392 e5 + 53709113612800 e6 − 96309967256832 e7 + 392889686770016 e8−
527857748339840 e9 + 366748643612160 e10 − 178047190379584 e11 + 76496366573008 e12−
   28444213296800 e13 + 7469161581088 e14 − 1213853566576 e15 + 158772078097 e16−
           43401479624 e17 + 12816535716 e18 − 2258516680 e19 + 277237126 e20−
                      33924440 e21 + 3309476 e22 − 154056 e23 + 2401 e24.                  (2)
Like for n = 11, we have expressed the real numbers a, b, c, d in terms of e and we conclude
that the graph of P corresponds to an existing packing.
• Case n = 15, Figure 3. Our computations have given f (P (15) ) = 0.625 = 5/8. The
configuration is mirror-symmetric, and symmetric with respect to the center O = p1
which is an isolated point. The edges of the graph are obtained from a duplication of the
path ((−1, 0), (−1/4, 1), (1, 1), (1, −1/4), (0, −1)) on each face of the cube.
• Case n = 16, Figure 3. The best packing found of sixteen spheres has a three-fold
symmetry with respect to a diagonal of the cube. It is clearly obtained by tightening
a symmetric packing. We have not succeeded to reduce the system of 8 equations of 8
unknowns given by our graph. Nevertheless, the resolution of this system with Newton’s
method confirms the coordinates of points.
• Case n = 17, Figure 3. The first best packing found having a sphere touching √     twelve
other spheres. The configuration is easy to describe and we get f (P (17) ) = 3 2/7.
• Case n = 18, Figure 3. We confirm the configuration already given by [Go] in which
the optimal configuration of six points in the square appears on three horizontal layers.
• Case n = 19, Figure 3. The best configuration found of nineteen points is not symmetric
and has six isolated points.
• Case n = 20, Figure 3. The best packing found has six isolated points (two in the heart
of the cube), the rigid structure is generated by the central symmetry with respect to 0,
a mirror symmetry and four points
                           (20)
                                  √ (a, −1, 1), (1, −b, 1), (−1, −1, c), (−d, −1, −a). The
computations lead to f (P ) = 2(1 − d)/2 where d is the smallest positive root of
                             83 − 324 x − 318 x2 + 156 x3 + 3 x4 = 0.                      (3)
For completeness, we give c = (357 − 683 d + 147 d2 + 3 d3)/304, b = (1−d)/2, a = 1−c−d
and finally after solving (3), we get
                                                          s
                                            √     √           79
                             f (P (20) ) = 7 2 + 4 6 − 2 46 + √ .
                                                               3

the electronic journal of combinatorics 11 (2004), #R33                                      8
• Case n = 21, Figure 4. The best packing found admits a central sphere touching twelve
other spheres which are slightly inside the cube. By considering the symmetries of the
graph and the three points√p1 = (1, −1, 1), p2 = (1 − a, 0, b) and p3 = (b, 1 − a, 0), we
obtain f (P (21) ) = 3/(2 + 2 3).
• Case n = 22, Figure 4. The marvelous best configuration of twenty-two points of
the figure 4, is composed of five
                                √ congruent octahedrons and four isolated points. It is
                       (22)
easy to find that f (P ) = 3 2/8, which is realized for instance by p1 = (3/4, 0, 0)
and p2 = (1, 1/4, 1). The packing has three-fold symmetry with respect to any principal
diagonal of the cube.
• Case n = 23, Figure 4. The best configuration found is mirror-symmetric with a central
isolated point.
• Case n = 24, Figure 4. The first best configuration found with eight isolated points.
• Case n = 25, Figure 4. More and more complexity appears in the sequence of optimal
configurations.
• Cases n = 26 and n = 27, Figure 4 and 5. The cubic lattice of twenty-seven spheres
given by [Go] appears to be optimal in our computations. If we take out the central sphere,
there remains a non-solid configuration of twenty-six points: the centers of each face and
the middles of each edge can be displaced in order to separate the centers pi . But if all
the spheres except the corners are directly displaced towards the center O, we just obtain
0.5005 · · · as minimum distance. In fact, our experiments have given 0.501074021252.
Thus, the deformation of the cubic lattice which gives the best packing found of twenty-
six points is more subtle: the point (1, 0, 1) is moved by staying inside a face of the cube
to (1 − a, 0, 1), the point (0, 0, 1) is displaced to (−c, c, 1 − b), the displacements of the
other points are similar. We find
                                            1√
                            f (P (26) ) =      1 + a2 = 0.501074021252...                 (4)
                                            2
where a is the smallest positive root of the polynomial −16 + 288 a − 728 a2 + 904 a3 −
609 a4 + 208 a5 − 2 a6 − 24 a7 + 7 a8 .
• Cases n = 28 to n = 32, Figure 5 and 6. The coordinates of the points of P (32) are either
±1 or ± 13 . Four spheres inside the cube have twelve spheres touching them. We conjecture
                                                       √
after computations that d29 = d30 = d31 = d32 = 2/3 = 0.471404520791.... Thus, it
appears impossible to take out three points from the very regular configuration of thirty-
two points, in order to obtain a non-solid configuration. On the contrary, it is possible to
obtain that d28 < d32 by taking out four points from P (32) and it seems that our algorithm
has given a complex deformation of such a configuration with f (P (28) ) = 0.471410634842.




the electronic journal of combinatorics 11 (2004), #R33                                     9
                         n=2                               n=3




                         n=4                               n=5




                         n=6                               n=7

       Figure 1: Optimal packings for 2 ≤ n ≤ 6 and best known packing for n = 7.

the electronic journal of combinatorics 11 (2004), #R33                             10
                         n=8                               n=9




                         n = 10                            n = 11




                         n = 12                           n = 13, 14

  Figure 2: Optimal packings for 8 ≤ n ≤ 10 and best known packings for 11 ≤ n ≤ 14.


the electronic journal of combinatorics 11 (2004), #R33                            11
                         n = 15                               n = 16




                         n = 17                               n = 18




                         n = 19                               n = 20

                        Figure 3: Best known packings for 15 ≤ n ≤ 20.


the electronic journal of combinatorics 11 (2004), #R33                  12
                         n = 21                               n = 22




                         n = 23                               n = 24




                         n = 25                               n = 26

                        Figure 4: Best known packings for 21 ≤ n ≤ 26.



the electronic journal of combinatorics 11 (2004), #R33                  13
                 Figure 5: Best known packings for n = 27 and 29 ≤ n ≤ 32.




                            Figure 6: Best known packing for n = 28




the electronic journal of combinatorics 11 (2004), #R33                      14
   We finish this paper with the table of the maximum separation distance dn of n
points in a unit cube. By using the same perturbed billiard algorithm in the unit ball
K = B(0, 1), we have obtained a similar list of results up to n = 40. We display it in [G].

      n                dn                        Value        Reference   # of rattlers
      1                √2                   2.000000000000...
      2                √3                   1.732050807568...
      3                √2                   1.414213562373...   [S1]
      4               √ 2                   1.414213562373...   [S1]
      5               √5/2                  1.118033988749...   [S1]
      6             q
                     3 2/4                  1.060660171779...   [S1]
                         √ √
      7  (−4 + 10 + 4 3)/ 3                 1.001089824549...   [S2]
      8         q
                     1                      1.000000000000...   [S1]
      9             (3)/2                   0.866025403784...   [S1]
     10            3/4                      0.750000000000...   [S2]
     11          see (1)                    0.710116382462...                  1
     12          see
                   √ (2)                    0.707106806467...
     13            √2/2                     0.707106781186...   [Go]
     14              2/2                    0.707106781186...   [Go]
     15            5/8                      0.625000000000...                  1
     16            √                        0.606667120726
     17          3√ 2/7                     0.606091526731...
     18             13/6                    0.600925212577...   [Go]
     19                                     0.578209612716                     6
         √      √        q
     20 7 2 + 4 6 − 2 46 + √793             0.554761174904...                  6
                        √
     21       3/(2√+ 2 3)                   0.549038105677...
     22           3 2/8                     0.530330085890...                  4
     23                                     0.523539214257                     1
     24                                     0.517638090205                     8
     25                                     0.505135865094                     3
     26          see (4)                    0.501074021252...
     27            1/2                      0.500000000000...   [Go]
     28            √                        0.471410634842                     2
     29            √2/3                     0.471404520791...
     30            √2/3                     0.471404520791...
     31            √2/3                     0.471404520791...
     32              2/3                    0.471404520791...

             Table 2: Maximum separation distance of n points in a unit cube



the electronic journal of combinatorics 11 (2004), #R33                                   15
References
[BDGL]      D. Boll, J. Donovan, R. L. Graham and B. D. Lubachevsky, Improving dense
            packings of equal disks in a square, Electron. J. Combin. 7 (2000), #R46.

[CFG]       H. T. Croft, K. J. Falconer and R. K. Guy, Unsolved Problems in Geometry,
            Springer Verlag, Berlin, 1991.

[D]         L. Danzer, Finite point-sets on S 2 with minimum distance as large as possible,
            Discrete Math. 60 (1986), 3–66.

[G]         Th. Gensane, Dense packings of equal spheres in a larger sphere: a list of result,
            in Les Cahiers du LMPA J. Liouville 188, June 2003.

[Go]        M. Goldberg, On the densest packing of equal spheres in a cube, Math. Mag.
            44 (1971), 198–208.

[GL1]       R. L. Graham and B. D. Lubachevsky, Dense packings of equal disks in an
            equilateral triangle: from 22 to 34 and beyond, Electron. J. Combin. 2 (1995),
            #A1.

[GL2]       R. L. Graham and B. D. Lubachevsky, Repeated patterns of dense packings of
            equal disks in a square, Electron. J. Combin. 3 (1996), #R16.

[GLNO]      R. L. Graham, B. D. Lubachevsky, K. J. Nurmela, and P.R. J. Östergård,
            Dense packings of congruent circles in a circle, Discrete Math. 181 (1998),
            139–154.

[GMPW] C. de Groot, M. Monagan, R. Peikert, and D. Wurtz, Packing circles in a
       square: a review and new results, in System Modeling and Optimization (Proc.
       15th IFIP Conf. Zurich 1991), Lecture Notes in Control and Information Sci-
       ence, Springer-Verlag, Berlin 180, 45–54, 1992.

[L]         B. D. Lubachevsky, How to simulate billiards and similar systems, J. Comput.
            Phys. 94 (1991), 255–283.

[LS]        B. D. Lubachevsky and F. H. Stillinger, Geometric properties of random disk
            packings, J. Statist. Phys. 60 (1990), 561–583.

[M]         H. Melissen, Packing and Covering with Circles, Ph.D. thesis, University of
            Utrecht, 1997.

[NO1]       K. J. Nurmela and P. R. J. Östergård, Packing up to 50 equal circles in a
            square, Discrete Comput. Geom. 18 (1997), 111–120.

[N02]       K. J. Nurmela, P. R. J. Östergård, More optimal packings of equal circles in a
            square, Discrete Comput. Geom. 22 (1999), 439–457.


the electronic journal of combinatorics 11 (2004), #R33                                    16
[O]         N. Oler, A finite packing problem, Canad. Math. Bull. 4 (1961), 153–155.

[S1]        J. Schaer, On the densest packing of spheres in a cube, Canad. Math. Bull. 9
            (1966), 265–270, 271–274, 275–280.

[S2]        J. Schaer, The densest packing of ten congruent spheres in a cube, in Intuitive
            geometry (Szeged, 1991), Colloq. Math. Soc. János Bolyai 63 (1994), 403–424.
            K. Böröczky and G. Fejes Tóth (Eds.), North-Holland, Amsterdam.

[SK]        E.B. Saff, A.B.J. Kuijlaars, Distributing many points on a sphere, Math. In-
            telligencer 10 (1997), 5–11.

[T]         T. Tarnai, Spherical circle-packing in nature, practice and theory, Struct.
            Topology 9 (1984), 39–58.

[Z]         Y.M. Zhou, Arrangements of Points on the Sphere, Ph.D. thesis, University of
            South Florida, 1995.




the electronic journal of combinatorics 11 (2004), #R33                                 17
