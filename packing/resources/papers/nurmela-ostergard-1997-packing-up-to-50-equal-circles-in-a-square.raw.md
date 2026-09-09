Discrete Comput Geom 18:111–120 (1997)                                       Discrete & Computational


                                                                      Geometry
                                                                    © 1997 Springer-Verlag New York Inc.




Packing up to 50 Equal Circles in a Square

K. J. Nurmela and P. R. J. Östergård∗
Department of Computer Science, Helsinki University of Technology,
FIN-02150 Espoo, Finland
Kari.Nurmela@hut.fi
Patric.Ostergard@hut.fi



     Abstract. The problem of maximizing the radius of n equal circles that can be packed
     into a given square is a well-known geometrical problem. An equivalent problem is to find
     the largest distance d, such that n points can be placed into the square with all mutual
     distances at least d. Recently, all optimal packings of at most 20 circles in a square were
     exactly determined. In this paper, computational methods to find good packings of more
     than 20 circles are discussed. The best packings found with up to 50 circles are displayed. A
     new packing of 49 circles settles the proof that when n is a square number, the best packing
     is the square lattice exactly when n ≤ 36.



1.    Introduction

The problem to be discussed in this paper is one that many of us have encountered in
everyday life: How many bottles of a given size can be packed into a square box of a
given size and how should this be done? The problem can be geometrically expressed as
follows: determine rn , the maximum radius of n nonoverlapping circles in a unit square.
By solving the latter problem, the former problem is also solved. Namely, the radius of
the bottles is divided by the side of the box and this quotient is compared with the values
in the nonincreasing series rn . The largest n for which rn is greater than the quotient is
the demanded solution.
    There is another equivalent formulation of the problem, which we adopt in this paper:
maximize the minimum distance between n points in a unit square. We denote this value



     ∗ The research of P. R. J. Östergård was supported by the Academy of Finland.
112                                                                K. J. Nurmela and P. R. J. Östergård


by dn , and have the following relation between rn and dn :
                                                 dn
                                       rn =             .
                                              2(dn + 1)
    A packing corresponding to dn (or rn ) is called an optimal packing. For some small
values of n and some n where the optimal packing has a nice structure, exact values of
dn have been proved by hand. Recently exact values of dn were determined for n up to
20 [4] (as explicit values or as the smallest root of a polynomial equation). The proofs
involve extensive use of computers; as of today this is about as far as we can come with
that approach. However, even if we are not able to find the exact values of dn for larger
values of n, we can try to find as good packings as possible, thereby lower-bounding dn .
In this research we try to find such good packings by computer search.
    The paper is outlined as follows. Old results on the problem are surveyed in Section
2. In Section 3 we consider how computers can be used in the search for packings. We
first discuss methods that have been mentioned in the literature; thereafter our approach
is treated in detail. The best packings found are displayed and discussed in Section 4.


2.    Old Results

The problem of packing circles into different geometrical shapes has received much
attention since the seminal work of Fejes Tóth [7]. A recent survey of results and problems
still open can be found in [3]. One of the most natural and most studied of these problems
is that of packing circles in a square.
    This problem was solved for up to nine circles in the 1960s by Graham, Meir and
Schaer; the proofs of these cases have been reported in [12], [18], [20], and [22]. The
proofs for n ≤ 5 are easy, whereas the cases 6 ≤ n ≤ 9 require more elaborate
mathematical tools. For example, for n = 5 we can divide the square into four subsquares
as indicated in Fig. 1. Now at least one square must contain two points
                                                                   √       due to the pigeon-
hole principle, so the length of the diagonals in the subsquares ( 2/2) upper-bounds d5 .
This is also a lower bound, since in the solution in Fig. 1 (which is the only possible√
optimal solution), this is the smallest distance between two points. Thereby d5 = 2/2.
    For n ≥ 10, only the optimal packings of 14 [26], 16 [24], 25 [25], and 36 [10] circles
have been proved by hand.
    Recently, de Groot et al. [5] used computers to find good packings for n ≤ 22. They




                        Fig. 1. Optimal packing of five points in a square.
Packing up to 50 Equal Circles in a Square                                              113

were later even able to give a computer proof of the best packings with up to 20 circles
[4], [15]. In particular, this ended a series of articles on packings of 10 circles (and
conjectures about the optimality of the respective packings); see [8], [19], [21], [23], and
some further references in [5]. Furthermore, for n up to 27 and for some sporadic values
of n greater than 27, good packings were given by Goldberg in [8].


3.     Computer Search for Packings

Computers have certainly played a central role in many searches for packings. Unfortu-
nately, this is very seldom mentioned and even if it is, only brief details are given. It is
very natural (for a given n) to define the problem as an optimization problem. A solution
of this optimization problem can then be a set of either n scattered points or n centers of
circles in a unit square. We now first take a look at what can be found in the literature
and thereafter discuss our approach.

3.1.    Earlier Approaches

In [5] the problem is considered as a maximizing problem. A solution is a set of centers
of circles in the unit square. The maximum possible radius for circles with these centers
that do not overlap and are within the boundaries of the square is easily calculated by
considering the distances between the points and between the points and the boundaries.
This is then the value that is maximized by moving the centers of the circles.
    The optimization methods used in [5] are the simplex (polytope) algorithm and the
quasi-Newton BFGS algorithm. Further details on the implementation of these methods
are omitted in the paper. For n ≤ 20, they fail to find optimal packings for n = 14, 15, 17.
In the papers where the optimality of packings with n ≤ 20 is proved [4], [15], the authors
report a better performance of a (stochastic) Langevin equation formalism than of the
two aforementioned methods; see also [6].
    Mollard and Payan [13] found good packings of 11, 13, and 14 circles that improved
on the results in [8] by using their own Cabri-Géomètre geometry software. They were
further able to improve the packing of 13 circles by hand.
    Graham and Lubachevsky [9] used an event-driven simulation algorithm to pack
circles in an equilateral triangle. The algorithm simulates the idealized movement of
billiard balls inside a triangular box; the size of the balls is increased slowly until the
movement is blocked.
    Clare and Kepert [2] and Kottwitz [11] found good packings of circles on a sphere
by computer. They did not consider the minimum pairwise distance between points, but
minimized the total potential energy of repulsion. The optimization methods used were
variants of the Fletcher–Powell–Davidon quasi-Newton method [17] and a simple gra-
dient method combined with Newton’s method, respectively. The approximate solutions
then found were refined by identifying the points at minimum pairwise distance and
solving iteratively a system of equations using Newton–Raphson methods. This method
was recently generalized for searching for higher-dimensional spherical codes in [14],
where some packings of [11] were also improved by using simple packing heuristics
combined with simulated annealing.
114                                                          K. J. Nurmela and P. R. J. Östergård

3.2.   Our Approach

Our approach is closely related to that of [2] and [11]. It is based on the minimization
of the energy function
                                              Ã !m
                                        X        λ
                                E=                2
                                                       ,                             (1)
                                      1≤i< j≤n di j

where di j is the distance between points i and j representing the centers of the circles,
λ is a scaling factor to prevent numerical overflows, and m is a positive integer.
   We transform the constrained optimization problem into an unconstrained one by
using the simple coordinate transformation defined as follows:
   Let (xi , yi ) be the center of circle i. Define

                                      xi = sin(x̃i ),
                                      yi = sin( ỹi ),

where x̃i and ỹi range over R. We now have an unconstrained optimization problem in
variables x̃i , ỹi (1 ≤ i ≤ n), where the coordinates of the centers of the circles fulfill
−1 ≤ xi ≤ 1, −1 ≤ yi ≤ 1 as required (the square, of course, need not be a unit square).
   The energy function (1) is twice continuously differentiable (except where two points
coincide). In the optimization we use (for each value of m) a hybrid algorithm that
consists of a simple steepest-descent algorithm with Goldstein–Armijo backtracking
line search in the beginning and a modified Newton method in the end.
   We start with a moderately small value of m (in the range 10 ≤ m ≤ 100) and find
a local optimum of the energy function. Then we double the value of m and repeat the
optimization step. As m tends to infinity, only the smallest distances between the centers
of the circles have an effect on the energy of the configuration. In some cases in this
work we used as large final values for m as 1050 , although optimization can usually be
ended when m reaches 106 . For each n, at least 50 optimization runs were performed
with random initial solutions.
   The scaling factor λ needs to be recalculated from time to time during the optimization
run, because otherwise the cost becomes impractically small, especially with large m.
We adjust λ after each optimization step by setting it equal to the square of the length of
the shortest distance between two points of the packing.
   The packing resulting from the optimization run can be further improved by con-
structing a system of nonlinear equations corresponding to the contacts between the
circles and between the circles and the boundary and by solving that system numeri-
cally. We first sort all the distances between the points into increasing order and find the
location where the distance shows a sudden increase. The distances up to this location
are assumed to be equal, and points very close to the boundary are assumed to be on the
boundary. We then form a system of equations from these assumptions. This procedure
can be done automatically by giving two threshold values, one for the largest admitted
difference between a candidate distance and the shortest distance of the configuration,
and the other for the largest admitted distance between a point and the boundary.
   In most cases the system of equations has a solution, which can be found numerically
using, for example, a modified Newton–Raphson method [1]. However, in a few cases the
Packing up to 50 Equal Circles in a Square                                              115




                                      Fig. 2. Poor local optimum.


gaps between the circles or between the circles and the boundary are so narrow that this
method results in a system of equations for which no solution exists, indicating that one or
more equations should be removed from the system. On the other hand, if some contacts
between circles are not included in the system, the solution of the system may have
circles overlapping. In such cases we can try to make the set of shortest distances more
clearly visible by continuing the optimization to locate the optimum more accurately. If
this strategy fails, we finally remove and add equations through trial and error until a
solvable system representing a nonoverlapping packing is found.
    Sometimes the packing resulting from an optimization run has a circle that is in
contact with the boundary and that can be moved toward the center of the square without
causing overlap with any other circles. In Fig. 2 this situation occurs with the circle
marked with a star. The arrangement, which is a local optimum of the energy function
(1), can be further improved by moving the circle away from the boundary slightly and
then continuing the optimization with a relatively large m.
    Starting with a random initial solution, our implementation of the optimization algo-
rithm performs an optimization run for 50 circles in about 20 minutes of CPU-time on a
current workstation. After the structure of the packing has been detected, the numerical
solution to the corresponding system of equations can be found in a few seconds with a
mathematical software supporting arbitrary-precision numbers.

4.   Best Packings Found

The best packings found for 21 ≤ n ≤ 50 are displayed in Fig. 3. The nine packings for
n = 22, 23, 24(a), 25, 27, 30, 36, 39, and 42 are old [5], [8], [10]—all other packings are
new. The packing for n = 21 improves on the results in [5], and several packings improve
on the results in [8]; see also [3]. There are three different best known packings of 24
circles and three packings of 35 circles. (A similar situation occurs with 17 circles—there
are two different optimal such packings [15].) Only the packings of 25 and 36 circles
have been proved optimal [10], [25].
   In Table 1 we tabulate some properties of the packings. In addition to the diameter d
of the circles, we show the density of the packing (that is, the area of the circles divided
by the area of the square), the number of loose circles in the structure, the total number
of contacts between the circles and between the circles and the boundary, and the order
of the symmetry group [16].
116                                         K. J. Nurmela and P. R. J. Östergård




      Fig. 3. Best known packings for 21 ≤ n ≤ 50.
Packing up to 50 Equal Circles in a Square                                               117




                                             Fig. 3 (continued)



    Some similarities can be found among the best known packings. For n = k 2 − 1,
best known packings of 8, 15, 24, and 35 (but not 48) circles have similar structure. For
n = k 2 − 3, that is also the case for packings of 22, 33, and 46 (but not 13) circles.
Other examples are the cases n = k 2 + k, and n = (2k 2 + k)/2 for k even. For n = k 2 ,
the optimal packing for n ≤ 36 is the square lattice. The new packing for n = 49
found in this work concludes the proof that, for n = k 2 , the square lattice packings are
optimal exactly for n ≤ 36. This disproves a conjecture of Wengerodt (who found denser
packings for n ≥ 64) that the square lattice packings are optimal for n ≤ 49; see [3] and
its references.
    Some packings in Fig. 3 are almost symmetric (for example, the packings of 22, 33,
and 46 circles); the packings are obtained by breaking the symmetry slightly. Two more
examples where an almost symmetric packing is better than the nearby symmetric one
can be found in the packings of 37 and 44 circles in this work. The packing of 37 circles
is interesting for two reasons: it does not contain any corner circles, and 37 is the largest
number of circles for which the best known packing has lower density than that of a
square lattice packing. The packing of 44 circles very much resembles that of 31 circles
and is possibly not optimal.
    In some packings there are very narrow gaps between the circles or between the circles
and the boundary. In the packing of 40 circles, the gap between one of the circles and
the boundary is about 3 · 10−15 times the diameter of the circles. The width of some of
118                                                               K. J. Nurmela and P. R. J. Östergård

                               Table 1. Properties of packings.

                                                Loose                          Order of
         n          d            Density        circles    Contacts         symmetry group

        21     0.271811687     0.753355227        2            40                   1
        22     0.267958402     0.771680112        1            43                   1
        23     0.258819045     0.763631032        0            56                   4
        24     0.254333095     0.774963260        0            56            8(a), 2(b), 2(c)
        25     0.250000000     0.785398163        0            60                   8
        26     0.238734757     0.758469090        2            56                   1
        27     0.235849528     0.772311456        0            55                   2
        28     0.230534597     0.771849233        2            53                   1
        29     0.226882901     0.778906242        1            65                   1
        30     0.224502965     0.792019026        0            65                   2
        31     0.217547292     0.777297479        4            55                   2
        32     0.213082353     0.775450816        2            61                   1
        33     0.211328384     0.788852304        1            65                   1
        34     0.205021908     0.772999930        1            71                   1
        35     0.202763601     0.781227213        0            80            2(a), 2(b), 1(c)
        36     0.200000000     0.785398163        0            84                   8
        37     0.196238101     0.782029274        1            73                   1
        38     0.195342304     0.797042557        0            77                   2
        39     0.194365063     0.811179027        0            80                   4
        40     0.188175077     0.787976383        2            79                   1
        41     0.186099512     0.792723899        1           100                   1
        42     0.184277072     0.798684279        0            90                   2
        43     0.180132785     0.786832179        2            83                   1
        44     0.178639224     0.793842645        4            82                   1
        45     0.175515450     0.787909640        2            87                   1
        46     0.174459361     0.797187132        1            91                   1
        47     0.171107017     0.788007250        2            95                   1
        48     0.169382110     0.790957782        0           101                   1
        49     0.167386077     0.791216990        1           120                   1
        50     0.166454626     0.799679429        0           104                   1



the gaps between the circles in the packing of 47 circles is less than 3 · 10−11 times the
diameter of the circles.
    The system of equations corresponding to the structure of a packing can be reduced
to a polynomial equation—of one variable—that has a zero at the diameter of the circles.
In some cases the polynomials have been constructed [4], but large irregular packings
have so complex polynomials that there is little hope of constructing them. The diameter
of the circles of a large packing can be solved exactly only in special cases.
    Finding a numerical solution to the system of equations corresponding to the proposed
structure of the packing does not guarantee that the structure exists, because of the finite
precision in calculations. The systems of equations in this work were solved numerically
so that the overlaps of, or gaps between, contacting circles in the conjectured structure
are less than 10−33 ; it is thus highly improbable that any of these structures turns out to
be nonexistent.
    The densities of the best known packings of 1–50 circles are plotted in Fig. 4. The
densities of hexagonal and square lattice packings are also shown by dotted lines. The
Packing up to 50 Equal Circles in a Square                                                               119




                                Fig. 4. Densities of best known packings.


density shows a clear tendency to increase as the number of circles increases, although
the densities of all the packings in this work still remain clearly below the density of the
hexagonal lattice packing—which the density approaches as n tends to infinity [7]. An
open question stated in [3] is whether there are any values of n such that dn = dn+1 . We
conclude this paper by conjecturing that there are no such n.


References

1. A. Ben-Israel, A Newton–Raphson method for the solution of systems of equations, J. Math. Anal. Appl.
   15 (1966), 243–252.
2. B. W. Clare and D. L. Kepert, The closest packing of equal circles on a sphere, Proc. Roy. Soc. London
   Ser. A 405 (1986), 329–344.
3. H. T. Croft, K. J. Falconer, and R. K. Guy, Unsolved Problems in Geometry, Springer-Verlag, New York,
   1991.
4. C. de Groot, M. Monagan, R. Peikert, and D. Würtz, Packing circles in a square: a review and new results,
   in P. Kall (ed.), System Modelling and Optimization (Proc. 15th IFIP Conf., Zürich, 1991), pp. 45–54,
   Lecture Notes in Control and Information Sciences, Vol. 180, Springer-Verlag, Berlin, 1992.
5. C. de Groot, R. Peikert, and D. Würtz, The optimal packing of ten equal circles in a square, IPS Research
   Report 90-12, ETH, Zürich, 1990.
6. C. de Groot, D. Würtz, M. Hanf, K. H. Hoffmann, R. Peikert, and Th. Koller, Stochastic optimization—
   efficient algorithms to solve complex problems, in P. Kall (ed.), System Modelling and Optimization (Proc.
   15th IFIP Conf., Zürich, 1991), pp. 546–555, Lecture Notes in Control and Information Sciences, Vol.
   180, Springer-Verlag, Berlin, 1992.
120                                                                     K. J. Nurmela and P. R. J. Östergård

 7. L. Fejes Tóth, Lagerungen in der Ebene, auf der Kugel und im Raum, 2nd edn., Springer-Verlag, Berlin,
    1972.
 8. M. Goldberg, The packing of equal circles in a square, Math. Mag. 43 (1970), 24–30.
 9. R. L. Graham and B. D. Lubachevsky, Dense packings of equal disks in an equilateral triangle: from 22 to
    34 and beyond, Electron. J. Combin. 2 (1995), A1, 39 pp.
10. K. Kirchner and G. Wengerodt, Die dichteste Packung von 36 Kreisen in einem Quadrat, Beiträge Algebra
    Geom. 25 (1987), 147–159.
11. D. A. Kottwitz, The densest packing of equal circles on a sphere, Acta Cryst. Sect. A 47 (1991), 158–165.
12. H. Melissen, Densest packing of six equal circles in a square, Elem. Math. 49 (1994), 27–31.
13. M. Mollard and C. Payan, Some progress in the packing of equal circles in a square, Discrete Math. 84
    (1990), 303–307.
14. K. J. Nurmela, Constructing spherical codes by global optimization methods, Research Report A32, Digital
    Systems Laboratory, Helsinki University of Technology, 1995.
15. R. Peikert, Dichteste Packungen von gleichen Kreisen in einem Quadrat, Elem. Math. 49 (1994), 16–26.
16. B. I. Rose and R. D. Stafford, An elementary course in mathematical symmetry, Amer. Math. Monthly 88
    (1981), 59–64.
17. L. E. Scales, Introduction to Non-Linear Optimization, Macmillan, London, 1985.
18. J. Schaer, The densest packing of nine circles in a square, Canad. Math. Bull. 8 (1965), 273–277.
19. J. Schaer, On the packing of ten equal circles in a square, Math. Mag. 44 (1971), 139–140.
20. J. Schaer and A. Meir, On a geometric extremum problem, Canad. Math. Bull. 8 (1965), 21–27.
21. K. Schlüter, Kreispackung in Quadraten, Elem. Math. 34 (1979), 12–14.
22. B. L. Schwartz, Separating points in a square, J. Recreational Math. 3 (1970), 195–204.
23. G. Valette, A better packing of ten circles in a square, Discrete Math. 76 (1989), 57–59.
24. G. Wengerodt, Die dichteste Packung von 16 Kreisen in einem Quadrat, Beiträge Algebra Geom. 16 (1983),
    173–190.
25. G. Wengerodt, Die dichteste Packung von 25 Kreisen in einem Quadrat, Ann. Univ. Sci. Budapest. Eötvös
    Sect. Math. 30 (1987), 3–15.
26. G. Wengerodt, Die dichteste Packung von 14 Kreisen in einem Quadrat, Beiträge Algebra Geom. 25 (1987),
    25–46.

Received April 24, 1995, and in revised form June 14, 1995.
