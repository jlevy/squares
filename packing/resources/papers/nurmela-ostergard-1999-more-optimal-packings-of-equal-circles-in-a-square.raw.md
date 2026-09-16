Discrete Comput Geom 22:439–457 (1999)                                       Discrete & Computational


                                                                     Geometry
                                                                    © 1999 Springer-Verlag New York Inc.




More Optimal Packings of Equal Circles in a Square∗

K. J. Nurmela and P. R. J. Östergård
Department of Computer Science and Engineering,
Helsinki University of Technology,
P.O. Box 5400, FIN-02015 HUT, Finland
{Kari.Nurmela,Patric.Ostergard}@hut.fi


     Abstract. The densest packings of n equal circles in a square have been determined
     earlier for n ≤ 20 and for n = 25, 36. Several of these packings have been proved with the
     aid of a computer. The computer-aided approach is further developed here and the range is
     extended to n ≤ 27. The optimal packings are depicted.



1.    Introduction

We consider the following packing problem: Find the value of rn , the maximum radius
of n nonoverlapping equal circles in a unit square. Another similar problem is that of
finding dn , the maximum possible minimum distance between n points in a unit square.
Actually, it is not difficult to show that these two problems are equivalent and that
rn = dn /(2dn + 2). A packing of circles with maximum radius (and the corresponding
spread of points) is called optimal.
   Solved and unsolved packing problems have been thoroughly discussed in [1], [4],
and [13]. Circle packings in a square have been considered in the mathematical literature
since the early 1960s when the problem was raised by Moser [15]. During the last three
decades, optimality proofs have been published for the following values of n: 1–9 (in [12],
[21], [23], and [25]), 14 (in [30]), 16 (in [28]), 25 (in [29]), and 36 (in [10]). Constructions
of good packings for other values of n have been published in, for example, [5], [7],
[14], [16], [22], [24], and [27].
   Recently, optimal packings for n ≤ 20 were determined and the corresponding values
of dn were obtained as explicit values or as the smallest positive root of a polynomial

    ∗ The research of K. J. Nurmela was supported by the Emil Aaltonen Foundation; the Vilho, Yrjö, and

Kalle Väisälä Foundation; and the Academy of Finland. The research of P. R. J. Östergård was supported by
the Academy of Finland.
440                                                              K. J. Nurmela and P. R. J. Östergård

equation in one variable [2], [3], [19]. The proofs involve extensive use of computers
and cannot be checked by hand. In this paper we verify these old results, enhance the
approach, and extend the number of circles to 27. As usual in computer-aided proofs,
the optimality proofs of packings in this paper consist of very long chains of automated,
relatively simple steps. It is not possible (or reasonable) to list all these steps in this paper.
Instead, we describe the algorithms used with such detail that it should be possible to re-
implement our programs from scratch and verify the computational results. To facilitate
possible re-implementation and further development of the algorithms, the most crucial
data of our computer runs is included in this paper. We would further like to point out that
it is not reasonable to try to automatize the whole proof in one computer program, but
human interaction at different stages should be used; this speeds up the proof and makes
it easier to follow the process. Preliminary results of this research have been published
by the authors in [17].
    Even if we here prove optimality only for packings of at most 27 circles, for larger n
we can still try to find as good packings as possible. In [16] packings of up to 50 circles
are given, some of which are improved in [7]. All of the optimal packings for n ≤ 27
are among those published in [7] and [16].
    In Section 2 the computer-aided method used to prove optimality of packings is
presented. Some statistics of the computer runs—both for the old (n ≤ 20) and the new
cases (with some data in the Appendix)—are given in Section 3, which also contains
pictures of the optimal packings for 21 ≤ n ≤ 27. The paper is concluded in Section 4.


2.     Computer-Aided Proof Method

We here give a comprehensive description of the computer-aided proof procedure used.
The proof procedure is based on that developed by de Groot et al. [2], [19]. All steps of
that method have been modified, some only slightly and some more substantially.


2.1.    Overview of the Method

We consider the problem of spreading n points in a unit square. Initially, we tile the
square in such a way that the maximum distance between two points in a single tile (the
diameter of the tile) is smaller than the minimum distance between points in the best
packing known. Consequently, no two points in an optimal packing can be in the same
tile.
    Next, we consider—up to symmetry—all possible ways of choosing n of the tiles.
For each of these combinations, the area of these tiles that can contain a point is reduced
by considering the areas of other tiles. If this area of a tile completely vanishes in the
process, the combination can be discarded, because it cannot contain an optimal packing.
This leads to elimination of most of the combinations. Additional eliminations can be
made by dividing a combination into subcases, which are eliminated one by one. An
optimal combination is a combination that contains an optimal packing.
    After the elimination process we know combinations of which at least one is optimal,
and for each combination we further know small areas where the points of an optimal
More Optimal Packings of Equal Circles in a Square                                         441


packing should reside. For a combination, we now take the best known packing with the
points within the remaining areas, and prove that there are no better such packings. This
is accomplished by a reduction process. The process—when successful—essentially
shows that the areas where the points must reside in a packing at least as good as the
prescribed packing can be made arbitrarily small and the conjectured packing is thus
best possible and unique within the small areas that we started from. This leads to a finite
number of packings out of which the optimal one(s) can be found.
   In the following we describe each phase of the optimality proof algorithm in more
detail.


2.2.   Finding Initial Combinations

Initially, the square is tiled with congruent square or rectangular tiles in such a way
that two points of an optimal packing cannot be in the same tile. This is achieved by
selecting the size of tiles so that the diameter of the tiles is smaller than dn , the distance
between points in the optimal packing (point spread). Points lying on a tile boundary
are considered as part of both tiles (or of all four tiles if the point is on a boundary
crossing). Good lower bounds for dn when n is not too large can be obtained by solving
numerically with desired precision the distance between the points in the best known
(often conjecturally optimal) packing.
    Diameters of tiles and the cases the tilings can be applied to are shown in Table 1. The
tilings that were used in the proofs will be given later for each case together with other
statistics. In practice, it turns out that it is computationally advantageous for the next
steps of the proof procedure to use square tiles (the larger the aspect ratio of the rectangles
of a tiling is, the worse is the result of the elimination procedure to be described). If the
square is tiled into rectangles, it is tiled so that there are fewer tiles in a row than in a
column. (This is essential for the numbering of combinations, discussed below.)
    We denote the total number of tiles by t and consider all possible ways of choosing
n out of t tiles. For a given choice, these n tiles are assumed to contain a point and are

                                     Table 1. Tilings of a square.

                                                                     Maximum
                                                                     number of
                          Tiling            Diameter                   circles
                                       √
                           2×2        √ 2/2 ≈ 0.707106781                4
                           2×3         √13/6 ≈ 0.600925213               5
                           3×3           2/3 ≈ 0.471404521               9
                           3×4         √5/12 ≈ 0.416666667              10
                           4×4       √ 2/4 ≈ 0.353553391                13
                           4×5       √41/20 ≈ 0.320156212               16
                           4×6        13/12
                                       √     ≈ 0.300462606              17
                           5×5       √   2/5 ≈ 0.282842712              20
                           5×6        61/30
                                       √     ≈ 0.260341656              22
                           6×6           2/6 ≈ 0.235702260              27
442                                                           K. J. Nurmela and P. R. J. Östergård

called full; the rest of the tiles are called empty. By taking symmetries into account, we
need not use all possible combinations in the computations: if a set of combinations can
be obtained from each other by rotations and/or reflections, then only one of them is
considered. As the symmetry group of a square, D4 , has order 8 (four axes of reflection
and rotations at every 90◦ ) and the symmetry group of a rectangle, D2 , has order 4 (two
axes of reflection, rotations at every 180◦ ), these orders give the maximum factors by
which the number of cases can be reduced. The exact number of remaining cases can be
calculated using Burnside’s lemma.

Theorem 1. Let G be a group acting on a set X . For g ∈ G let ψ(g) denote
                                                                      P the number
of elements of X fixed by g. Then the number of orbits of G is (1/|G|) g∈G ψ(g).

    Here X is the set of all possible choices of n full tiles, and G is one of the two
aforementioned symmetry groups. Burnside’s lemma plays a central role in counting
and its proof can be found in most books on group theory and combinatorics.
    In the numbering of the combinations we differ slightly from the approach in [2] and
[19]. The combinations are represented as binary strings which are ranked as described
in Section 3. In the next step of the proof algorithm the combinations are considered
in the order of their ranks, and combinations that have a symmetric combination with a
smaller rank are skipped. Contrary to the approach in [2] and [19], all combinations are
ranked, not only those that are not skipped. There are two reasons for this. First, given
a rank of a combination, we can immediately construct the combination without going
through all combinations with smaller ranks. Second, in the next steps we do not have
to start from the first combination; this is especially important if there is a huge number
of combinations and the computations are distributed over several computers.


2.3. Eliminating Combinations

Next we try to eliminate combinations that cannot contain a packing with minimum
distance at least dlow . The value of dlow used in the computations must be sufficiently
smaller than dn so that the elimination process works correctly, see below. We carry out
the elimination by reducing parts of full tiles. The area of a full tile that has not yet
been reduced is called active. Initially the whole area of full tiles of a combination is
active. Throughout the paper, active areas are closed areas. The active area is reduced
by considering the active areas of other full tiles. Since only the active area of a full tile
can contain a point in an optimal packing, a combination can be eliminated if the active
area of a full tile becomes the empty set.
   In [2] and [19] each full tile is quantized into rectangles horizontally and vertically;
in [17] a slightly more efficient approach is described with quantization in only one
direction. In this work we present an even more efficient approach, where no such
subdivision takes place, but the active area of a given full tile is considered as a polygon.
An algorithm that solves the following problem is now needed. (Interestingly, when we
start with convex polygons—squares and rectangles—the polygons stay convex after all
reductions.)
More Optimal Packings of Equal Circles in a Square                                        443

Reducing Polygons. Given two polygons, A and B, and a distance d, reduce B to
another polygon B 0 such that B 00 = B\B 0 is at distance less than d from all points in A.

   Then, if A and B are active areas, B can be reduced to B 0 since a point in B\B 0 would
be at a distance less than d from a point in A. Of course, we would like the area of B 0 to
be as small as possible, but this is no absolute requirement.
   We first prove some basic results which help in developing an algorithm. First, we
note that we need only consider the vertices of A in the following sense.

Lemma 1. If a point P is at a distance less than d from the vertices of a polygon C, it
is at a distance less than d from all points in C.

Proof. Draw a circle of radius d around P. All vertices of the polygon C are within
this circle, and hence this holds for all points in C.

Theorem 2. Assume that B1 , B2 , . . . , Bk are distinct points on the boundary of B, that
Bi Bi+1 for 2 ≤ i ≤ k − 2 are edges of B, and that B1 B2 and Bk−1 Bk lie on edges of B.
If the points Bi , 1 ≤ i ≤ k, are at a distance less than d from all vertices of A, then the
points in the polygon B 00 obtained from these vertices are at a distance less than d from
all points in A.

Proof. Take any vertex of A; then it follows from Lemma 1 that this vertex is at a
distance less than d from all points in B 00 . Now take any point in B 00 and apply Lemma 1
again: it follows that this point is at a distance less than d from all points in A. This
completes the proof.

   So, to be able to apply Theorem 2 to reduce the polygon B, we need to find consecutive
vertices of B that are at a distance less than d from all vertices of A. If this holds for all
vertices of B, we get B 0 = ∅ (and so this particular combination is eliminated).
   Furthermore, when the consecutive edges are found, we also need to look at the edges
leading to the outermost vertices to see how far away B1 and Bk can be placed. We then
need to calculate how circles with radius d and centers at the vertices of A cut those
edges.
   In implementing an algorithm for this problem, one should note that (surprisingly,
maybe) the vertices of B that are at a distance less than d from all vertices of A need not
occur in one sequence. Although rare, this anomaly in fact occurred in our computations.
In Fig. 1 an example is given where a point P is at a distance greater than d from exactly
two vertices of a convex polygon, V and V 0 , and these are not adjacent. If this happens,
then one of the sequences is chosen to get B 0 .
   Note that when implementing the polygon reducing algorithm we have to be careful
with the finite precision of the floating point arithmetic. The following two operations
that the finite precision affects occur in the programs:
   1. Is the distance between two points less than dn ?
   2. What are the intersections between a given line (in the form of two points lying
      on the line) and a given circle (with radius dn and a given center point)?
444                                                                K. J. Nurmela and P. R. J. Östergård




                                     Fig. 1. A special case.



    In our computations we used IEEE double-precision floating point arithmetic. The
correctness of answers to the first question is taken care of by the fact that we replace dn
by dlow in the question. (It is important to notice that we do not require the exact answer
to this question, but if we answer yes, that must be the right answer.) In all cases, we
have chosen dlow so that dn − dlow > 10−9 , which is greater than our estimated upper
bound on the inaccuracy of the floating point arithmetic for this problem, e1 = 10−15
(which again exceeds the true inaccuracy).
    The second question comes up in reducing the active area. Figure 2 describes an error
that may occur if the inaccuracy of the computer arithmetic is not dealt with properly.
We use the notation from Theorem 2 and the discussions around it. Again, we remember
that we use dlow instead of dn .
    Let B1 and Bk (everything in this discussion works similarly for Bk ) be the points
between which an edge of the reduced polygon should be inserted if we were to use dn
in the reduction algorithm. However, as we use dlow , we would with exact precision get
the vertex B10 . In Fig. 2 we have drawn an error circle around B10 to show the error area in




                    Fig. 2. Correction needed in the polygon cutting algorithm.
More Optimal Packings of Equal Circles in a Square                                         445




                               Fig. 3. Different situations for correction.



which the point as calculated by the computer will reside. Then the new vertex might be
B100 with, for example, P incorrectly outside the new active area. Therefore, a correction
is necessary.
    Calculations of the radius of the error area gave a rough upper bound of e2 = 10−13 .
Hence dn − dlow > e2 (see above) and B1 is outside the error area. It is then enough to
make a correction in the direction perpendicular to the edge through B1 and B10 by an
amount greater than e2 . We used a correction by 10−10 . The shaded area in Fig. 2 shows
where the new vertex should be placed for correctness. Depending on the directions
of the vertices we get somewhat different situations; the two extremes are depicted in
Fig. 3. Note that in the second of these, we end up outside the permissible area if too
large a correction is made. In that case, it is not difficult to show that the points on the
line through B1 and Bk and on the boundary of the permissible area are at a distance
greater than dn from some point in the active area which is used to get the reduction.
Then, since all points in the same active area are at a distance less than or equal to dlow
from B10 , it follows that after a correction of length less than dn − dlow we are still in the
permissible area (this holds, since e2 < dn − dlow ).
    Note that we get some new active area because of the correction carried out; the im-
portant thing is that we never reduce an area that should not be reduced. The infinitesimal
extra area that is added due to the correction has no noticeable influence on the overall
performance of the algorithm.
    In the reduction process each full tile is considered in turn to reduce the active area of
other full tiles. This process can be accelerated by ruling out pairs of tiles with an active
area that are so far from each other that no reduction can ever take place. After each tile
has been considered, we repeat the whole procedure until an active area becomes empty
and the combination is eliminated or the number of rounds reaches a given number (we
used 20 in most cases). If the maximum number of rounds was achieved, then there is
either an optimal packing with points in the remaining active areas of the combination,
446                                                                K. J. Nurmela and P. R. J. Östergård


or we need some more sophisticated tools to reject the combination. We now discuss
such advanced methods.



2.4.   Eliminating Hard Cases

The previous step may fail to eliminate a combination that cannot contain an optimal
packing especially when there are several good near-optimal packings close to each
other. We can then simply continue the reduction process for some more rounds but this
very seldom leads to the desired result.
   A better approach—following the ideas in [2] and [19]—is to split the problem into
subcases and apply the polygon reduction method to each subcase. This is done by
choosing a full tile and dividing this into several rectangles, which are considered one
by one (as initially containing all the active areas of that full tile). If all cases are not
eliminated, we can do the same procedure for another full file, but now we can initially
remove the rectangles that were eliminated in the previous rounds. This is exemplified
in Fig. 4. This procedure was automatized, mostly using a division of tiles into 15
rectangles. In this way we were able to eliminate all combinations that do not hold an
optimal packing.




                      Fig. 4. Dividing the elimination problem into subcases.
More Optimal Packings of Equal Circles in a Square                                      447


2.5.   Proving Optimality and Uniqueness

In the final step of the optimality proof we use the method developed in [17]; see that
paper for the proof of its correctness. It is based on a method used by Schaer to prove
(manually) optimality of the densest packing of nine circles [21]; later Kirchner and
Wengerodt [10], [28]–[30] and de Groot et al. [2], [19] used similar methods (the latter
in computer-aided proofs).
     At this stage of the proof algorithm—having reduced most of the active area in
the combinations that we were not able to eliminate in the previous steps—we know the
(small) regions in which points of an optimal packing can reside. For a given combination,
we take the best known packing with the points within the remaining active areas, and
try to prove that there are no better such packings.
     The task of showing that such a packing with the points in the active areas indeed
exists is in itself a nontrivial task. To do this, we guess (this is often obvious) which
points are at minimum distance from each other and construct the corresponding system
of equations. In this system there is one equation for each pair of points conjecturally
at the minimum distance from each other (stating that their distance from each other
equals the minimum distance). The variables of the system are the minimum distance
and the coordinates of the points. Each point lying on the edge of the square has only one
variable, and points lying in the corners of the square have no variables. If the guessed
packing has symmetries, these provide additional equations.
     In many cases (especially when there are strong symmetries in the solution), the
system can be solved symbolically. The exact values of dn of small optimal packings are
given in Table 2.1 of [13] for n ≤ 20 and in Table 2 for d23 , d24 , d25 , and d27 (clearly,
until we are finished with the results in this paper, we only know that these are minimum
distances corresponding to best known packings). The existence of such packings within
the remaining active areas can be verified easily, because the coordinates of the points
can be computed symbolically. In the cases where the exact values cannot be solved, we
solve the system numerically to get approximate positions of the points of a solution,
pi0 . In these cases, using the interval Newton/bisection program INTBIS [9], we prove
that such a packing really exists with points pi for which |pi0 − pi | < d 0 holds for some
small positive d 0 . We used d 0 = 10−10 .

                                       Table 2. Exact and ap-
                                       proximate values of dn ,
                                            21 ≤ n ≤ 27.

                                       d21 ≈ 0.2718122553 . . .
                                       d22 ≈ 0.2679584015
                                             √     √      ...
                                               6− 2
                                       d23 =
                                                 4√
                                                     2
                                       d24 =       √    √
                                             1+2 2+ 3
                                       d25 = 14
                                       d26 ≈ 0.2387347572
                                             √            ...
                                               89
                                       d27 =
                                              40
448                                                            K. J. Nurmela and P. R. J. Östergård

   In some cases the system of equations is overdetermined and INTBIS cannot be used
directly. In such a case we can try to use geometrical techniques to reduce the system
into a nonoverdetermined system of equations suitable for INTBIS. For the best known
packing of 26 circles, which will turn out to be optimal, we reduced the system into a
single equation in one variable.
   Next we draw congruent error squares (circles are used in [2] and [19], but squares
were indeed used by Schaer and others in [10], [21], and [28]–[30]) of side r around the
points pi0 (which are in the centers of the error squares), such that the active area remaining
from the previous steps of the algorithm is within these squares (this requirement must
also hold if the squares are drawn around the points pi ). For a point on a side, only a
half square is used, and for a point in a corner, a quarter of a square is used. All squares
have the same size and should preferably be as small as possible. It is important that a
square that is around a point in the interior of the unit square fits completely within the
unit square (both with pi0 and pi as a center).
   Finally, an elimination procedure resembling that used earlier to eliminate combina-
tions is started. We used the elimination procedure described and proved in [17], where
each active area is quantized into rectangles in one direction. (It should be possible to
use the polygon reduction algorithm presented here, but the correction step described in
Fig. 2 may introduce some difficulty.) The elimination procedure from [17] can be used
to prove optimality by induction whenever the following theorem can be applied. The
maximal error in calculations is denoted by e. The value of e is comparable with e1 and
e2 discussed in Section 2.3. See [17] for a proof of the theorem.

Theorem 3. Assume that dlow + 2d 0 + e < dn . If the active area around the points pi0
can be reduced by the elimination process (with lower bound dlow ) to fit within squares
of side qr , with 0 < q < 1 (with the points pi0 in the centers), then the guessed packing
with the points pi is the best packing within the original error squares. Furthermore,
there are no other equally good such packings.

   It should be emphasized that the theorem can only guarantee a packing to be best
among packings with the points within the original error squares, that is, to be locally
optimal. If this procedure is applied to several remaining combinations, the best solutions
found have to be compared to find the global optimum (optima).


3.    The Results

This section contains the results of our computer runs. We both verify the results in [2]
and [19] for n ≤ 20 and consider cases up to n = 27. We also provide new proofs for the
cases 6 ≤ n ≤ 9 (the case n = 7 was considered in [17]). Some data from the computer
runs can be found in Table 3, in the Appendix, and electronically in the World Wide Web
at hURL:http://www.tcs.hut.fi/pub/packings/squarei.
    In Table 3, n denotes the number of points and dlow denotes the lower bound on dn
used. The tiling is also given (see Table 1). The total number of combinations considered
and the number of combinations remaining after the initial elimination procedure (dis-
More Optimal Packings of Equal Circles in a Square                                                    449

                                 Table 3. Data from the computer runs.

n       dlow       Tiling        T            T0                   Optimal combinations

 6   0.6009252      3×3             16         6     See Appendix
 7   0.5358983      3×3              8         2     9 111110101
 8   0.5176380      3×3              3         1     4 111101111
 9   0.4999999      3×3              1         1     0 111111111
10   0.4212795      4×4           1051         1     4344 1011110100101101
11   0.3982073      4×4            567         1     1967 1101101101101101
12   0.3887301      4×4            252         1     718 1011110110111101
13   0.3660960      4×4             77         2     153 1111110110111101
14   0.3489152      4×5           9808         8     18913 11110111100001111101
15   0.3410813      4×5           3912         1     13053 11111101001011011111
16   0.3333333      4×5           1253         1     4350 11111111000011111111
17   0.3061539      5×5         136080         7     719321 1111110101010101010111011 (2 packings)
18   0.3004626      5×5          60645         2     286655 1101110101110111010111011
19   0.2895419      5×5          22475        14     70479 1110110111111001011111101
20   0.2866116      5×5           6814         2     17356 1110110111111011011111101
21   0.2718122      5×6        3578729        60     7132215 111111101000101110101011111101
                                                     7153939 111111011101000101011011111101
                                                     7159934 111111011100000111011011111101
22   0.2679584      5×6        1465113        8      2607260 111111110100010111011011111101
23   0.2588190      6×6      288873270       34      See Appendix
24   0.2543330      6×6      156484440      124      See Appendix
25   0.2499999      6×6       75112674      136      See Appendix
26   0.2387347      6×6       31784172     1008      92355986 111011101101111011101101011011110101
27   0.2358495      6×6       11772390      162      See Appendix




cussed in Section 2.3 of the proof algorithm) are denoted by T and T 0 , respectively. The
combinations remaining are listed in the Appendix. After the more advanced eliminating
procedure (Section 2.4) only the optimal combinations remained.
    The optimal combinations (both the rank and the binary string, when there are not too
many) are given in the last column of Table 3. In the binary strings the first digit denotes the
leftmost, lowermost tile (1 for full tile, 0 for empty tile). The next digits represent the rest
of the bottom row of the tiling and the rest of the rows are   ¡ ¢represented in the same way such
that the last few digits denote the top row. There are nt possible such strings, where t is
the number of tiles in the tiling. These strings are ranked in inverse lexicographic order so
that the first string is 11 · · · 1100 · · · 00
                                             ¡ ¢and the last 00 · · · 0011 · · · 11; the rank of the first
string is 0 and the last string has rank nt −1. For example, in a 3×3 tiling the combination
111101111 means a configuration where the center tile is empty and the other tiles are full.
The rank of this combination is 4, because there are four other combinations (111111110,
111111101, 111111011, 111110111) before this combination. For efficient ranking and
unranking algorithms, see, for example, [26].
    For the cases 10 ≤ n ≤ 20, the number of remaining combinations after the first
elimination process (Section 2.3) is in some cases smaller than that in [2] and [19]. We
have checked that all our remaining combinations are among those remaining in that
study. There is a misprint in [2] and [19]: the number of initial combinations for n = 12
is incorrect (267) since they indeed used 252 combinations in their search [20].
450                                                           K. J. Nurmela and P. R. J. Östergård

    The part of the proof procedure that is most time-consuming is the initial elimination
part of the proof algorithm (Section 2.3). In [2] and [19] about 3 CPU-hours of computa-
tion time was used for the most difficult cases for n ≤ 20. The number of combinations
increases rapidly for n ≥ 21. Consequently, there is also a rapid increase in CPU-time
needed. The four cases with 23 ≤ n ≤ 26 required as much as several CPU-months
of computation time on a Sun Sparcstation 2 workstation when using the elimination
process described in [17]. Since d27 is just slightly greater than the diameter of the tiles
(see Tables 1 and 2), the elimination method in [17] cannot be used for n = 27 without
large computing resources. Even the increasing computing power in the foreseeable near
future does not help much. However, using the polygon reduction algorithm described
in Section 2.3, we were able to speed up the search remarkably, and the first (and most
time-consuming) elimination stage for all cases n ≤ 27 was completed in a month of
CPU-time.
    In some cases there are several combinations that lead to an optimal packing. For
n = 6, 23, 24, 25, 27 the optimal packings have points that lie exactly on the border
between two or four tiles. Different combinations then converge to the optimal packings
from different directions. For n = 21 the direction of the tiling constitutes the difference
between the first and the last two combinations (there are two of these due to a large area
within which a loose circle can move). The same phenomenon does not occur for other
tilings where the number of rows and columns are not equal, as the optimal packings in
those cases are diagonally symmetric (n = 14, 15, 16) or nearly symmetric (n = 22).
    The optimality proof outlined in Section 2.5 worked out well for all cases except
n = 21. We first suspected that the guessed packing is not optimal but it later turned
out that the algorithm for the optimality proof discussed in Section 2.5 simply does
not converge due to long chains of interactions and feedbacks between the error areas.
However, starting from error squares of side 0.002, the following results are sufficient to
get an optimality proof by induction (a complete proof is longish and therefore left out;
it follows the approach in [17]). Consider the point corresponding to the circle very close
to the border in Fig. 5. Divide the error square around that point into two rectangles:
                 7
A consists of 16   of the original area and is close to the border; B consists of the rest
of the area (and contains the point). Now if A is the only initial active area around that
point, the reduction procedure eliminates one of the active areas completely and thus
there cannot be a solution with a point in A. On the other hand if B is the only active
area, the convergence required in Theorem 3 is achieved (the requirement that the active
area has to fit within a square of side qr still holds, so the error area is allowed to reach
the edge between A and B after elimination).
    The optimal packings for 21 ≤ n ≤ 27 are depicted in Fig. 5 and the corresponding
values of dn are given in Table 2. In a recent paper of Maranas et al. [11], it is claimed
that there is a packing of 21 circles with d ≈ 0.27181675; in view of the results of this
paper, that value is erroneous.


4.    Conclusions

It can always be argued whether results obtained by computers (and which cannot be
checked by hand) should be trusted. Evidence of correctness of the results here are,
More Optimal Packings of Equal Circles in a Square                                       451




                              Fig. 5. Optimal packings for 21 ≤ n ≤ 27.


however, provided by at least the following facts. First, all packings of at most 20 circles
that were proved optimal in [2] and [19] turned out to be optimal in this study also. Second,
all optimal packings of 21–27 circles are among those reported in [7] and [16]. Third,
the square lattice packing of 25 circles has earlier been proved optimal by Wengerodt
[29]. Furthermore, the manual proofs that have been published are in some cases, such
as in [30], so complicated that the authors find them in practice less convincing and more
error-prone than a computer-aided proof, where each step is relatively simple.
    With massive computer power and further development of the algorithms, it should
be possible to proceed beyond 27 circles. In at least three ways, the search gets more
difficult and time-consuming when the number of circles grows:
   1. The initial number of combinations grows rapidly.
   2. An increasing number of combinations remaining after the initial elimination has
      to be considered using methods from Section 2.4.
   3. A straightforward proof of optimality as described in Section 2.5 may fail and
      methods similar to that used for the packing of 21 circles in this paper may become
      necessary.
452                                                               K. J. Nurmela and P. R. J. Östergård


   (Note that the growth discussed is not monotonic.) For the first item, there is the
following possible strategy. The square is first subdivided into two (halves) or more
parts. Packings of points into these areas are then calculated and combined to reduce the
number of initial combinations.
   The approach in the paper can with minor modifications be used for packings in others
geometrical objects. These results (primarily for packings in an equilateral triangle and
a circle, see [6] and [8]) will be discussed in forthcoming papers [18].


Appendix

The ranks of the combinations remaining after the initial elimination procedure discussed
in Section 2.3 are listed here. Due to the large number of combinations in the case n = 26,
these are not included; the combinations can be obtained from the authors or from the
World Wide Web at hURL:http://www.tcs.hut.fi/pub/packings/squarei, where files
with the results for all 6 ≤ n ≤ 27 are available.
    For n = 6 and n = 25 we have more than one remaining combinations with the
property that all of these lead to the optimal packing. The number of optimal combinations
for n = 6, 23, 24, 25, 27 can be calculated using Burnside’s lemma (Theorem 1). For
example, for n = 25 the number of combinations is the number of ways of choosing one
of each of the tiles with letters A, B, C, D, E, F, G, H, and I in Fig. 6 (all other tiles are full
tiles) taking symmetries into account. To avoid the abundance of optimal combinations,
it would maybe have been more appropriate to choose another tiling in these cases, such
as 5 × 7.

n = 6:
Optimal combinations:
8, 11, 18, 23, 35, 41.




                         Fig. 6. Possible optimal combinations for n = 25.
More Optimal Packings of Equal Circles in a Square                              453

n = 7:
9, 13.
n = 8:
4.
n = 9:
0.
n = 10:
4344.
n = 11:
1967.
n = 12:
718.
n = 13:
153, 397.
n = 14:
18913, 19405, 19734, 31543, 32175, 32643, 34063, 34967.
n = 15:
13053.
n = 16:
4350.
n = 17:
531789, 548782, 548793, 574897, 575732, 575742, 719321.
n = 18:
203480, 286655.
n = 19:
35318, 35620, 37440, 68967, 69269, 70479, 70546, 70551, 70787, 71089, 93269, 95301,
150179, 151350.
n = 20:
17356, 45944.
n = 21:
3929891, 6771475, 6778408, 6778425, 6779664, 6782996, 6942984, 6978773,
454                                                K. J. Nurmela and P. R. J. Östergård

7036389, 7037996, 7122790, 7132215, 7132220, 7132223, 7147036, 7153939,
7154276, 7159934, 7166315, 7169398, 7169412, 7172310, 7172536, 7206322,
8793230, 8840763, 8841405, 8998420, 8998425, 8998483, 8998500, 8998703,
8999059, 9085920, 9087527, 9098296, 9098351, 9110869, 9258071, 12370515,
12372558, 12377804, 12378895, 12577163, 12578818, 12635785, 13038882,
13101492, 13102572, 13102573, 13108095, 13110516, 13126099, 13138475,
13139799, 13210460, 13211530, 13212500, 13213545, 13219788.
n = 22:
2607260, 3555400, 3557910, 4897651, 4899141, 5212141, 5231020, 5241328.
n = 23:
Optimal combinations:
1697836485, 1697836486, 1697836849, 1697836850, 1697849277, 1697850277,
1697850278, 1698043692, 1698043693, 1698828945, 1698828946, 1698829309,
1698829310, 1698847924, 1698848925, 1698954824, 1698986790, 1699122784,
1713852466, 1713854468.
Other combinations:
1227864664, 1227864665, 1227864672, 1227864673, 1228158594, 1690426781,
1690428330, 1690448464, 1695146683, 1695175284, 1695224203, 1695738516,
1695841476, 1710688358.
n = 24:
Optimal combinations (a):
881862520, 881862521, 881862528, 881862529, 881868594, 881868601, 881868602,
881877103, 881877104, 881892016, 882183430, 882183431, 882183438, 882183439,
882195859, 882195860, 882195867, 882195868, 882214357, 882214358, 882214365,
882214366, 882239097, 882239098, 882239105, 882679031, 882679038, 882679039,
882688912, 882688919, 882707410, 882707417, 882707418, 882728517, 883175899,
887507595, 887507602, 887526100, 888019145.
Optimal combinations (b):
878173088, 878173089, 878173096, 878173097, 878299058, 878299059, 878299066,
878299067.
Optimal combinations (c):
880216063.
Other combinations:
871779778, 871779779, 871779786, 871779787, 871905748, 871905749, 871905756,
871905757, 877220329, 877220330, 877220693, 877220694, 877226764, 877226765,
877227765, 877227766, 877235112, 877235113, 877236113, 877236114, 877250607,
877250608, 877252609, 877252610, 877259089, 877259090, 877259453, 877259454,
877265524, 877265525, 877266525, 877266526, 877273872, 877273873, 877274873,
More Optimal Packings of Equal Circles in a Square                       455

877274874, 877289367, 877289368, 877291369, 877415269, 877415270, 877415633,
877415634, 877428060, 877428061, 877429061, 877429062, 877446404, 877446405,
877447405, 877447406, 877471727, 877473729, 877492789, 877492790, 877493153,
877493154, 877505580, 877505581, 877506581, 877523924, 877523925, 877524925,
877524926, 877549247, 877551249, 877733220, 877733584, 877761807, 877762808,
877810740, 877811104, 877839327, 878091190, 878091554, 878217160.
n = 25:
Optimal combinations:
397525108, 397525109, 397525116, 397525117, 397525199, 397525200, 397525207,
397525208, 397527039, 397527046, 397527047, 397527402, 397527403, 397527410,
397527411, 397530040, 397530041, 397530396, 397530397, 397530404, 397530405,
397536322, 397537314, 397537315, 397537322, 397537323, 397580342, 397580343,
397580350, 397580351, 397586416, 397586423, 397586424, 397594925, 397594926,
397696076, 397696077, 397696084, 397696085, 397696167, 397696168, 397696175,
397696176, 397700966, 397700967, 397700974, 397700975, 397701330, 397701331,
397701338, 397701339, 397709468, 397709469, 397709476, 397709477, 397709832,
397709833, 397709840, 397709841, 397722105, 397722106, 397722113, 397723106,
397723107, 397723114, 397736522, 397736523, 397736530, 397736531, 397748951,
397748952, 397748959, 397767449, 397767450, 397767457, 397767458, 397792189,
397792190, 397792197, 397814042, 397814043, 397814050, 397814051, 397826471,
397826472, 397826479, 397844969, 397844970, 397844977, 397844978, 397869709,
397869717, 398015287, 398015294, 398015295, 398015378, 398015385, 398015386,
398018917, 398018924, 398019281, 398019288, 398027419, 398027426, 398027427,
398027783, 398027790, 398027791, 398037515, 398038516, 398054473, 398054480,
398054481, 398064354, 398064361, 398082852, 398082859, 398103959, 398131993,
398132000, 398132001, 398141874, 398141881, 398160372, 398160379, 398334945,
400825517, 400825524, 400825881, 400825888, 400834026, 400834383, 400834390,
400951029, 400969527, 401151969.
n = 27:
Optimal combinations:
32827518, 32827519, 32827882, 32827883.
Other combinations:
11783292, 14671315, 19701872, 20569553, 21804726, 21824433, 29939496,
30198184, 30198308, 30198314, 30235506, 30401840, 30428174, 30428537,
30428538, 30431597, 32419659, 32801185, 32826168, 32827473, 32827525,
32827759, 32827837, 32827888, 32827889, 32830942, 37858000, 37858005,
37858076, 37858718, 37859293, 37859360, 37861136, 37873580, 37873586,
37892923, 37892989, 38006988, 38031367, 38038236, 38043318, 38043322,
38043327, 38043328, 38053740, 38054381, 38725757, 38726399, 38726639,
38726763, 38726769, 38729253, 38729758, 38729822, 38900428, 38902239,
38902786, 38903499, 38903862, 38903863, 38903869, 38906858, 38906903,
38906922, 38909183, 38909188, 38911003, 38911008, 38911009, 38912364,
456                                                                      K. J. Nurmela and P. R. J. Östergård

38913930, 39034219, 39266825, 39271567, 39526894, 39561298, 39561299,
39561662, 39561663, 39564358, 39564722, 39817431, 39817555, 39853312,
39892044, 39892168, 39910367, 39960930, 39978985, 39980273, 39980637,
39980700, 39980824, 39980860, 40322546, 40467208, 51742232, 51742874,
51743237, 51743516, 51745298, 51746297, 51761437, 51775338, 51777079,
51864810, 51891144, 51896599, 51907129, 51910101, 51915523, 51916461,
51919332, 51920337, 51923397, 51925654, 51925663, 51927474, 51927478,
51927483, 51927769, 51927908, 51927919, 51927947, 51928839, 51930249,
51940744, 51940751, 51940810, 51940817, 51942987, 51943381, 51943416,
51943417, 51943423, 51943588, 51943601, 51944746, 51944966, 52609913,
52752840, 52757321, 52770186, 52786395, 52797910, 53410640, 53444104,
53701587, 53701985, 53703778, 53704575, 53704581, 53704751, 53704759,
53705036, 54178411, 84270113, 87655593.

We finally give one optimal combination for each of the cases not listed in Table 3:

n = 6:           8                  111101010
n = 23:          1697836485         111011101011111001000010110101111011
n = 24(a):       881862520          111011111011110011000000111011111011
n = 24(b):       878173088          111011111011000000111011110011111011
n = 24(c):       880216063          111011111011000000111011101011111011
n = 25:          397525108          111011111011111011000000111011111011
n = 27:          32827518           111011101101111011101101111011101101


References

 1. H. T. Croft, K. J. Falconer, and R. K. Guy, Unsolved Problems in Geometry, Springer-Verlag, New York,
    1991.
 2. C. de Groot, M. Monagan, R. Peikert, and D. Würtz, Packing circles in a square: a review and new results,
    in P. Kall (ed.), System Modelling and Optimization (Proc. 15th IFIP Conf., Zürich, 1991), pp. 45–54,
    Lecture Notes in Control and Information Sciences, Vol. 180, Springer-Verlag, Berlin, 1992.
 3. C. de Groot, R. Peikert, and D. Würtz, The Optimal Packing of Ten Equal Circles in a Square, IPS Research
    Report 90-12, ETH, Zürich, 1990.
 4. L. Fejes Tóth, Lagerungen in der Ebene, auf der Kugel und im Raum, 2nd edn., Springer-Verlag, Berlin,
    1972.
 5. M. Goldberg, The packing of equal circles in a square, Math. Mag. 43 (1970), 24–30.
 6. R. L. Graham and B. D. Lubachevsky, Dense packings of equal disks in an equilateral triangle: from 22
    to 34 and beyond, Electron. J. Combin. 2 (1995), A1, 39pp.
 7. R. L. Graham and B. D. Lubachevsky, Repeated patterns of dense packings of equal disks in a square,
    Electron. J. Combin. 3 (1996), R16, 17 pp.
 8. R. L. Graham, B. D. Lubachevsky, K. J. Nurmela, and P. R. J. Östergård, Dense packings of congruent
    circles in a circle, Discrete Math. 181 (1998), 139–154.
 9. R. B. Kearfott and M. Novoa, III, Algorithm 681: INTBIS, a portable interval Newton/bisection package,
    ACM Trans. Math. Software 16 (1990), 152–157.
10. K. Kirchner and G. Wengerodt, Die dichteste Packung von 36 Kreisen in einem Quadrat, Beiträge Algebra
    Geom. 25 (1987), 147–159.
11. C. D. Maranas, C. A. Floudas, and P. M. Pardalos, New results in the packing of equal circles in a square,
    Discrete Math. 142 (1995), 287–293.
12. H. Melissen, Densest packing of six equal circles in a square, Elem. Math. 49 (1994), 27–31.
More Optimal Packings of Equal Circles in a Square                                                           457

13. H. Melissen, Packing and Covering with Circles, Ph.D. thesis, University of Utrecht, 1997.
14. M. Mollard and C. Payan, Some progress in the packing of equal circles in a square, Discrete Math. 84
    (1990), 303–307.
15. L. Moser, Problem 24 (corrected), Canad. Math. Bull. 3 (1960), 78.
16. K. J. Nurmela and P. R. J. Östergård, Packing up to 50 equal circles in a square, Discrete Comput. Geom.
    18 (1997), 111–120.
17. K. J. Nurmela and P. R. J. Östergård, Optimal packings of equal circles in a square, Proceedings of the
    Eighth International Conference on Graph Theory, Combinatorics, Algorithms, and Applications, in press.
18. K. J. Nurmela and P. R. J. Östergård, Packing congruent circles in an equilateral triangle, in preparation.
19. R. Peikert, Dichteste Packungen von gleichen Kreisen in einem Quadrat, Elem. Math. 49 (1994), 16–26.
20. R. Peikert, private communication.
21. J. Schaer, The densest packing of nine circles in a square, Canad. Math. Bull. 8 (1965), 273–277.
22. J. Schaer, On the packing of ten equal circles in a square, Math. Mag. 44 (1971), 139–140.
23. J. Schaer and A. Meir, On a geometric extremum problem, Canad. Math. Bull. 8 (1965), 21–27.
24. K. Schlüter, Kreispackung in Quadraten, Elem. Math. 34 (1979), 12–14.
25. B. L. Schwartz, Separating points in a square, J. Recreational Math. 3 (1979), 195–204.
26. D. W. Stanton and D. E. White, Constructive Combinatorics, Springer-Verlag, New York, 1986.
27. G. Valette, A better packing of ten circles in a square, Discrete Math. 76 (1989), 57–59.
28. G. Wengerodt, Die dichteste Packung von 16 Kreisen in einem Quadrat, Beiträge Algebra Geom. 16
    (1983), 173–190.
29. G. Wengerodt, Die dichteste Packung von 25 Kreisen in einem Quadrat, Ann. Univ. Sci. Budapest. Eötvös
    Sect. Math. 30 (1987), 3–15.
30. G. Wengerodt, Die dichteste Packung von 14 Kreisen in einem Quadrat, Beiträge Algebra Geom. 25
    (1987), 25–46.

Received February 11, 1998, and in revised form December 17, 1998.
