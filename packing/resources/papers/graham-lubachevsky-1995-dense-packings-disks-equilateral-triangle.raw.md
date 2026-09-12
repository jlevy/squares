                                                         Dense Packings of Equal Disks in an Equilateral
                                                              Triangle: From 22 to 34 and Beyond
                                                                                        R. L. Graham
                                                                                      B. D. Lubachevsky
                                                                                 AT&T Bell Laboratories,
arXiv:math/0406252v1 [math.MG] 12 Jun 2004




                                                                               Murray Hill, New Jersey 07974



                                                                                        ABSTRACT


                                                 Previously published packings of equal disks in an equilateral triangle have dealt with up
                                             to 21 disks. We use a new discrete-event simulation algorithm to produce packings for up
                                             to 34 disks. For each n in the range 22 ≤ n ≤ 34 we present what we believe to be the
                                             densest possible packing of n equal disks in an equilateral triangle. For these n we also list the
                                             second, often the third and sometimes the fourth best packings among those that we found.
                                             In each case, the structure of the packing implies that the minimum distance d(n) between
                                             disk centers is the root of polynomial Pn with integer coefficients. In most cases we do not
                                             explicitly compute Pn but in all cases we do compute and report d(n) to 15 significant decimal
                                             digits.
                                                 Disk packings in equilateral triangles differ from those in squares or circles in that for
                                             triangles there are an infinite number of values of n for which the exact value of d(n) is known,
                                             namely, when n is of the form ∆(k) := k(k+1)
                                                                                      2   . It has also been conjectured that d(n−1) = d(n)
                                             in this case. Based on our computations, we present conjectured optimal packings for seven
                                             other infinite classes of n, namely

                                                             n = ∆(2k) + 1, ∆(2k + 1) + 1, ∆(k + 2) − 2, ∆(2k + 3) − 3,

                                                                     ∆(3k + 1) + 2, 4∆(k), and 2∆(k + 1) + 2∆(k) − 1 .

                                             We also report the best packings we found for other values of n in these forms which are larger
                                             than 34, namely, n = 37, 40, 42, 43, 46, 49, 56, 57, 60, 63, 67, 71, 79, 84, 92, 93, 106, 112, 121,
                                             and 254, and also for n = 58, 95, 108, 175, 255, 256, 258, and 260. We say that an infinite
                                             class of packings of n disks, n = n(1), n(2), ...n(k), ..., is tight , if [1/d(n(k) + 1) − 1/d(n(k))] is
                                             bounded away from zero as k goes to infinity. We conjecture that some of our infinite classes
                                             are tight, others are not tight, and that there are infinitely many tight classes.
                                                                                                 2

1    Introduction

    Geometrical packing problems have a long and distinguished history in combinatorial math-
ematics. In particular, such problems are often surprisingly difficult. In this note, we describe
a series of computer experiments designed to produce dense packings of equal nonoverlapping
disks in an equilateral triangle. It was first shown by Oler in 1961 [O] that the densest packing
of n = ∆(k) := k(k+1)
                  2   equal disks is the appropriate triangular subset of the regular hexagonal
packing of the disks (well known to pool players in the case of n = 15). It has also been con-
jectured by Newman [N] (among others) that the optimal packing of ∆(k) − 1 disks is always
obtained by removing a single disk from the best packing for ∆(k), although this statement
has not yet been proved. The only other values of n (not equal to ∆(k)) for which optimal
packings are known are n = 2, 4, 5, 7, 8, 9, 11 and 12 (see Melissen [M1], [M2] for a survey).
    As the number n of packed disks increases, it becomes not only more difficult to prove
optimality of a packing but even to conjecture what the optimal packing might be. In this
paper, we present a number of conjectured optimal packings. These packings are produced on
a computer using a so-called “billiards” simulation algorithm. A detailed description of the
philosophy, implementation and applications of this event-driven algorithm can be found in [L],
[LS]. Essentially, the algorithm simulates a system of n perfectly elastic disks. In the absence
of gravitation and friction, the disks move along straight lines, colliding with each other and the
region walls according to the standard laws of mechanics, all the time maintaining a condition
of no overlap. To form a packing, the disks are uniformly allowed to gradually increase in size,
until no significant growth can occur. Not infrequently, it can happen at this point that there
are disks which can still move, e.g., disk 3 in t7a13 (see Fig. 1.1).
    Every packing of n disks occurring in the literature for n different from ∆(k) and ∆(k) − 1
which has been conjectured or proved to be optimal was also found by our algorithm. These
occur for n = 13, 16, 17, 18, and 19 (see [M1], [MS]). This increases our confidence that the
new packings we obtain are also optimal. The new packings cover two “triangular periods”:
21 = ∆(6) to ∆(7) to ∆(8) = 36.
    In addition, we conjecture optimal packings for seven infinite classes of n, namely, n =
∆(2k)+1, ∆(2k+1)+1, ∆(k+2)−2, ∆(2k+3)−3, ∆(3k+1)+2, 4∆(k), and 2∆(k+1)+2∆(k)−1,
where k = 1, 2.... Each class has its individual pattern of the optimal packings which is different
from patterns for other classes. These were suggested by the preceding packings, and we give
                                                                                                    3




                      5                                                          1


                                                                           5          6
                      2

             4                 7
                                                                           2          3

         1            3             6                             7                             4


                  t7a13                                                    t7a16
0.366025403784439               13 bonds                 0.366025403784439                 16 bonds

             Figure 1.1: Two equivalent but nonisomorphic densest packings of 7 disks.


 packings for some additional values of these forms, namely, n = 37, 40, 42, 43, 46, 49, 56, 57,
 60, 63, 67, 71, 79, 84, 92, 93, 106, 112, 121, and 254, as well as for n = 58, 95, 108, 175, 255,
 256, 258, and 260.
     We say that an infinite class of packings of n disks, n = n(1), n(2), ...n(k), ..., is tight , if
 [1/d(n(k) + 1) − 1/d(n(k))] is bounded away from zero as k goes to infinity. We conjecture
 that some of our infinite classes are tight, others are not, and that there are infinitely many
 tight classes.


 2       The packings

     We performed a small number of runs with n = 21, 27, 28, 35 and 36 disks. In every case,
 the resulting packings were consistent with the existing results (n = ∆(k)) and conjectured
 (n = ∆(k) − 1). The bulk of our efforts concentrated on the other 11 values of n, for 21 ≤ n ≤
 36. These are presented in Figures 3.1 to 3.11.
     To navigate among the various packings presented we will use the labeling system illustrated
 by Fig. 3.1 t22a. Here, n = 22, “a” denotes that the packing is the best we found, “b” would
 be the second best (as in t23b in Fig. 3.2), “c” would be third best, and “d” would be fourth
 best.
                                                                                                                                                                        4

        Small black dots in the packing diagrams are “bonds” whose number is also entered by
  each packing. For example, there are 47 bonds in t22a. A bond between two disks or between
  a disk and a boundary indicates that the distance between them is zero. The absence of a
  bond in a spot where disk-disk or disk-wall are apparently touching each other means that the
  corresponding distance is strictly positive, though perhaps too small for the resolution of the
  drawing to be visible. For example, there is no bond between disk 1 and the left side of the
  triangle in t18a (Fig. 2.2); according to our computations, the distance between disk 1 and the
  side is 0.0048728... of the disk diameter. (Packing t18a was constructed in [M1].) Each disk in
  most of the packings is provided with a label which uniquely identifies the disk in the packing.
  This labeling is nonessential; it is assigned in order to facilitate referencing.



                              4                                                       1                                                       16

                     12           11                                             4            5                                          13        5

                     17           13                                            10        14                                        17        14        11
            14                                 7                       6                              17
                              1                                                      11                                             1         7         10
       3         9                     8            5              8        15                             16               2                                       9
                                                                                              9                                          12        4
  10        2             6                    16       15     7       12        2                    3         13     3        8                              6        15


                 t17a40                                                     t17a42                                                  t17a43
0.211324865405187                              40 bonds      0.211324865405187                        42 bonds       0.211324865405187                         43 bonds




                              2                                                       2                                                       4

                      3           13                                            16            6                                          15        11

                11            1            9                               14        15           9                                 12        3            1

             14           6                     4                       17           11               13                        9        2         16          6
       15                              8                           8                          12            3                                 7
                     16                                                          7                                          14                                 13
  12        7                 17               5        10     4       1                  5        10                  10            17                5                8


                 t17b36                                                 t17b42ns                                                    t17b42s
0.208735129275750                              36 bonds      0.208735129275750                        42 bonds       0.208735129275750                         42 bonds


  Figure 2.1: The best (t17a40, t17a42, t17a43) and the next-best (t17b36, t17b42ns, t17b42s)
  packings of 17 disks.
                                                                                                 5

    Each disk normally has at least three bonds attached. The polygon formed by these bonds
as vertices contains the center of the disk strictly inside. This is a necessary condition for
packing “rigidity”. In [LS], where the packing algorithm was applied to a similar problem, the
disks without bonds were called “rattlers.” A rattler can move freely within the confines of
the “cage” formed by its rigid neighbors and/or boundaries. (If we “shake” the packing, the
rattler will “rattle” while hitting its cage.) t22a has two rattlers, disks 3 and 5. In the packing
diagrams, all disks, except for the rattlers, are shaded.
    A number with 15 significant digits is indicated for each packing in the figures, e.g., the
number 0.17939 69086 11866 for packing t22a. This number is the disk diameter d(n) which is
measured in units equal to the side of the smallest equilateral triangle that contains the centers
of all disks. For packing t22a such a triangle is the one with vertices at the centers of disks 22,
17, and 12. This unit of measure for d(n) conforms with previously published conventions.
    Sometimes several packings exist for the same disk diameter. An example is t7a13 and
t7a16 in Fig.1.1. Thus, we distinguish such packings by suffixing their labels with the number
of bonds. Other examples are t17a40, t17a42, and t17a43 in Fig. 2.1, t22b42 and t22b50 in
Fig. 3.1. However, even the number of bonds may not distinguish different packings of the
same disk diameter; for example, t17b42ns and t17b42s in Fig. 2.1, where the provisional “ns”
stands for “non-symmetric” and “s” for “symmetric.”
    We point out that the a-packings of 17 and 18 disks that we show have previously been
given by Melissen and Schuur [MS], who also conjecture their optimality.


3    Additional comments
Fig. 3.2:   Two more c-packings for 23 disks that are not shown in the figure were generated:
t23c55.1 and t23c55.2. Both have 55 bonds. t23c55.1 can be obtained by combining the left
side of t23c53 with the right side of t23c57. t23c55.2 is a variant of t23c55.1.


Fig. 3.3:   Disk 20 in t24c56 and in t24c59 is locked in place because its center is strictly
inside the triangle formed by the three bonds of disk 20. In both packings, the distance of the
disk center to the boundary of this enclosing triangle is the distance to the line between bonds
with the left side of the triangle and disk 24, and is 0.0317185... of the disk diameter.


Fig. 3.4:   The given d-packing of 25 disks t25d60 is symmetric with respect to the vertical
axis. An equivalent non-symmetric d-packing t25d53 was also obtained in which all disks are
                                                                                                  6

located in the same places as in t25d60, except for disks 5, 12, 13, 14, 23, and 24. These six
disks form a pattern which is roughly equivalent to that formed by disks 10, 14, 19, 25, 20,
and 22, respectively, in t25b. Disk 24 in t25d53 is a rattler.


Fig. 3.6:    Only one of the two b-packings of 29 disks we found is shown, namely, t29b63.2.
The other b-packing, t29b63.1, differs in the placements of only disks 2, 3, 4, 7 as explained in
Section 4.


Fig. 3.8:    Four a-packings of 31 disks exist; only three are shown in the figure; the fourth
one, t31a81.1, is described in Section 4.


Fig. 3.10:    In t33a, the gap between disk 8 and left side is 0.0017032... of the disk diameter.
In t33c, disk 7 is stably locked by its bonds with 3, 6, and 29. However, the distance from disk
7 center to the line on bonds with disks 3 and 6 is only 0.0002097575.... of the disk diameter.
As a result, the cage of rattler disk 5 in t33c is very tight: the gap between disk 22 and disk 5
or disk 18 and disk 5 does not exceed 4 × 10−9 of the disk diameter.


Fig. 3.11:    In t34a, the small gaps between “almost” touching pairs disk-disk or disk-wall
take on only three values (relative to the disk size): in pairs 20–31, 16–26, 23–27, 18–19, 1–27
the gap is 0.021359..., in pairs left-32, right-29 it is 0.024750..., and in pairs 4–34, 7–22, it is
0.042561... Similarly, there are only three values of gaps in each of t34b, t34c, and t34d.

      t34b: in pairs 18–19, 23–27, 17–28, 20–31, 16–26 the gap is 0.019583...; in pairs
      left-32, right-29 it is 0.022686...; in pairs 4–34, 7–22, it is 0.039035...
      t34c: in pairs 12–17, 22–27, 3–10, 14–21, 4–34. 3–16 the gap is 0.018864...; in pair
      left-15 it is 0.021850...; in pair 19-24 it is 0.037606...
      t34d: in pairs 2–4, 26–32, 15–22, 12–21, 3–16, 7–16 the gap is 0.018681...; in pair
      left-27 it is 0.021637...; in pairs 13–33, 19–30 it is 0.037242...
                                                                                                                         7




                                 3                                                              8

                             9                                                         12           5
                                      10
                11                                                             11               4         3
                             12
                                           14
           1
                                                                               1            18            17
                             15            8
      16         2                                     17             9                                            10
                                                                                       2             14
                                     4
  5        13        18                            7        6     7       16                13                 6        15



                     t18a                                                          t18b36
0.203465240539124                              40 bonds         0.203464834591373                             36 bonds




                             15                                                                 7

                         4           16                                                13           18

                17           13            3                                       4        12           15

            10               5                 6                               2           10             16

      9                              2                 18             8                             9
                     1                                                             14                              3

  7        11                12            14               8     1       6                 17            5             11



                 t18b40                                                            t18b43
0.203464834591373                              40 bonds         0.203464834591373                             43 bonds

Figure 2.2: The best (t18a) and the next best (t18b36, t18b40, t18b43) packings of 18 disks.
                                                                                                                                           8




                                  17                                                                   22

                             15        6                                                          12        15

                         4        8        11                                             1                           3
                                                                                                        9

                   18        19        7            13                                        7                   4
                                                                                19                     11                   14
          14                      16                     21
                         3                     5                                          8                       13
                                                                           5                                                         16
                                                                                                       21
           2                      20                     1
 22                      9                 10                     12   2        6             17                 20         18            10


                              t22a                                                        t22b42
 0.179396908611866                                 47 bonds            0.179132453213560                                  42 bonds




                                  20                                                                   19


                                  19                                                               6         7

                         1                 16
                                                                                      22                              8
                                                                                                        1
                                  13
                         2                 10
                                                                                          20                      12
           11                                            6                      18                      5
                             15        3                                                                                    17
                                                                                                                 10
      8             14                             12         4            16        15            13
                                  18                                                                                             4
 21            7         22                9            17        5    2        3             11        21            14                  9


                         t22b50                                                                    t22c
 0.179132453213560                                 50 bonds            0.178763669382058                                  46 bonds


Figure 3.1: The best (t22a), the next-best (t22b42, t22b50), and the third-best (t22c) packings
of 22 disks.
                                                                                                                                9




                             17                                                                  6

                        22        15                                                       22         7

                   10         8         3                                             19        18         2

              4         11        1          2                                   10        3                    13
                                                                                                     11
              12        16                   5                                   15        20                  12
                                  7                                                                                       9
     6                                                   13             4                            5
                   23                                                                 21
                                       14                                                                            8
19        9                  20                  21           18   14        1                  17        16                   23


                        t23a                                                               t23b
 0.175153309170525                          52 bonds               0.174962364462008                           52 bonds




                              4                                                                  7

                        2         12                                                       21        23

                   15        16         3                                             2         15         5

                        20        19                                             16        20        14         19
              22                                 8
                        18        5                                              3         8         10         17
     11        1                            23           13             13                                                11
                             14                                                                  9
 6        7        17                  10            9        21   12        1        18                  4          22        6


                    t23c53                                                             t23c57
 0.174457630187009                          53 bonds               0.174457630187009                           57 bonds


Figure 3.2: The best (t23a), the next-best (t23b), and the third-best (t23c53, t23c57) packings
of 23 disks.
                                                                                                                            10




                              13                                                              22

                         17        12                                                    7         2

                    11        9         14                                               19        17
                                                                               14                            9
                    6         5          4                                                    24
          24                                      15                      18        1                   12        11
                         21        3                                                          23
     16        19                            2         1             8         3                             20        10
                              10                                                              13
20        22         8                  23        7        18   21        15        6                   5         16        4


                         t24a                                                            t24b
 0.174457630187010                           63 bonds           0.171024411616889                            53 bonds




                              19                                                              19

                         13        23                                                    13        23


                         22         6                                                    22         6
               20
                                             16                                20                            16
                         24        17                                                    24        17
           5                                      11                      5                                       11
                         9         2                                                     9         2
     21        7                             4         3             21        7                             4         3
                              14                                                              14
10        18        15                  12        8        1    10        18        15                  12        8         1


                     t24c56                                                         t24c59
 0.170613243353863                           56 bonds           0.170613243353863                            59 bonds


Figure 3.3: The best (t24a), the next-best (t24b), and the third-best (t24c56, t24c59) packings
of 24 disks.
                                                                                                                                      11




                                  11                                                                 11

                            24         6                                                         5        13

                    20            18         5                                             24        6         16

               14            7         22        10                               12             2        9         17


           16           25              12           21                       3                  8            22         10

     4                            8                        15                         21             18                          25
                    1                           13                        1                                        14

17        3                  9         19             23        2    15           7              4        23             19           20


                            t25a                                                                t25b
 0.169065874417891                               63 bonds            0.167753380810744                              58 bonds




                                  20                                                                 25

                            12         5                                                         7        1

                    10            2         23                                             9         15        17

               19            7         4         21                                   2          8        21        11

          24                     17        18         3                       6                 20        24                 5

     25             22                                     16                         10                            12
                                  9              1                        3                          22                          14

 6        13            8              15             11        14   18           4             19        16            13            23


                            t25c                                                           t25d60
 0.167714758299772                               57 bonds            0.167685455574367                              60 bonds


Figure 3.4: The best (t25a), the next-best (t25b), the third-best (t25c), and a fourth-best
(t25d60) packings of 25 disks.
                                                                                                                                 12




                              16                                                                26

                         9         23                                                      8         15

                    12        11        17                                           21         1         22

               1         10        14         6                                  7          5        23        10

          13        22                  21        3                        3          14        18        16        19
                              7
     25        18                            24        4              13        24         17            12              2
                              20
 8        19        15                  2         26        5    4         9         20          6             25                11


                         t26a                                                              t26b
 0.166738399395271                           63 bonds            0.166732017260692                             63 bonds




                              1                                                                 10

                         16        13                                                      4         6

                    26        12        17                                            2         18         1

               6         5         23        20                                 7          11        19        15

          7         3          15                 14                       22        13                   9         16
                                                                                                5
                                        18
     21        24         4                            19             26         21                            23            8
                                                                                                 3
                                         8
 2        9         25        11                  22        10   25        14          20                 24        12           17


                         t26c                                                              t26d
 0.166698218018074                           63 bonds            0.166695724000574                             62 bonds


Figure 3.5: The best (t26a), the next-best (t26b), the third-best (t26c), and the fourth-best
(t26d) packings of 26 disks.
                                                                                                                          13




                              16                                                            16

                         26        17                                                  26        17

                    29        14        27                                        29        14        27

               15        19        28        23                              15        19        28        23

          13        25        18                  8                     13        25        18                  8
                                        5                                                              5
     24                  11                           2            24                  11                            2
               12                  6         4                               12                  6          4
     21                  10                           3            21                  10                            3
22             20                  9         7            1   22             20                  9         7               1


                         t29a                                                 t29b63.2
 0.152189614060732                           63 bonds         0.152172645377571                            63 bonds




                              22                                                            11

                         15        14                                                  4         27

                    19        17        23                                        3         9         28

               20        29        18        28                              24        6         21        15

          26        24        12                  8                     18        5         25        16        19
                                        5
     25                  11                           2            10                  22                  20
               16                  6          4                              2                   1                   29
     21                  10                           3            12                  14              23
27             13                  9         7            1   26             13                  7               17        8


                         t29c                                                          t29d
 0.152161553910934                           65 bonds         0.152109020552728                            63 bonds

Figure 3.6: The best (t29a), a next-best (t29b63.2), the third-best (t29c), and the fourth-best
(t29d) packings of 29 disks.
                                                                                                                                                 14




                                   1                                                                       18

                              2         24                                                            10        13

                         29        30        15                                                 12         14           29

                   16         4         18        12                                             7         27           15
                                                                                       20                                         21
           11            20                  21        13                                             2         26
                                   8
                                                                                  9         17                                     24
               3         23                  7         27                                                                28
     22                            10                            5            4        23         30            6                           3
                    19                            14                                                                         11
26        9                   28        17                  25       6   22       19        5         25            8                  1         16


                              t30a                                                                   t30b
0.150761500215428                                  73 bonds              0.149057883638389                                    71 bonds




                                   6                                                                       15

                              25        14                                                            21        25

                         24        3         8                                                  19         4            3

                   26         23        18        20                                        1         28        30           10

                         27        29        17         5                                   9                   18           16
              30                                                                                      6
                                                                                  17                                                   11
                         11        4                   10                                                               8
                                             28                                                  12
     13        22                                                9            7        23                  26                  29           20
                              2
                                                  21                                                                 14
15        12        16                  19                  1        7   22       27        2         24                               5         13


                              t30c                                                                   t30d
0.149047199036657                                  68 bonds              0.148951506290246                                    67 bonds


Figure 3.7: The best (t30a), the next-best (t30b), the third-best (t30c), and the fourth-best
(t30d) packings of 30 disks.
                                                                                                                                                15




                                  15                                                                         15

                             21        26                                                               21         26

                        20        22        30                                                    20         22         30

                        13        14        3                                                     13         14          3
               28                                     10                                 28                                       10
                             11        18                                                               11         18
          17        25                          29         24                       17        25                                       24
                                  8                                                                           8         29
     2         16        6                 31         23        7              2         16         6                             23        7
                                                                                                                   31
19        9         12            4              5         27        1    19        9         12         4                   5         27        1


                         t31a79                                                               t31a81.2
0.148543145110506                                79 bonds                 0.148543145110506                                   81 bonds




                                  19                                                                         18

                             9         2                                                                12         25

                        12        16        17                                                          21          7
                                                                                              24
                    4        6         25        28                                                                          2
                                                                                                              30
                                                                                         16        14                   10        9
                31           8         11        13                                                          28
          5                                                20                       27         19                            11        20
                        29        18        14                                                                    15
     27        23                                     22        21             26         3             29                        23        1
                             10        3                                                                           6
1         7         24                          30         26        15   22        17        4          5                   13        31        8


                         t31a82                                                                        t31b
0.148543145110506                                82 bonds                 0.146207330881888                                   71 bonds


Figure 3.8: The best (t31a79, t31a81.2, t31a82) and the next-best (t31b) packings of 31 disks.
                                                                                                                                                        16




                                       15                                                                                6

                                  23        10                                                                      16        14

                             18        29           28                                                         23        29        19

                        7         32        30           11                                                21                  31
                                                                                                                     22                  20
                    9                                                                              32
                                   25           16           27                                                               18
                                                                                                                    25                   2
          20                 12                                       13                      4            9                                      13
                                        19               8
                                                                                                                         8          1
      17            22            31                              6        4             12        30          15                            17        11
                                                 5
                                                                                                                              5
26             14            24        3                     1        2        21   28        27        24           7                  3         10        26


                                  t32a                                                                              t32b
0.145102169183849                                            76 bonds               0.144984727468812                                    72 bonds




                                       28                                                                                11

                                  12         2                                                                      20        17

                              16           30                                                                  24        7         21
                                                     14
                        32                                                                              14           8        3          5
                                  26            3            27
               18                                                                                  9                               18        12
                                  10        29                                                                      19
                                                             8                                                            13
          17            23                                            22                       32          30                       26            2
                                       21           31
     15        19             6                                  13        4             15                         25        6                        23
                                                                                                       1                                 16
                                            25
20        11            1         24                         5        7        9    22        4                28        10        31             27        29


                                  t32c                                                                              t32d
0.144651911950450                                            71 bonds               0.144616419018845                                    77 bonds

Figure 3.9: The best (t32a), the next-best (t32b), the third-best (t32c), and the fourth-best
(t32d) packings of 32 disks.
                                                                                                                                                 17




                                   4                                                                         4

                              3         16                                                              3         16

                         10        15        28                                                    10        15          28

                     5        33        22        18                                          5         33        22          18

                8        30        23        13        25                                8         30        23          13           25

          19             29        17          14          32                       19            29         17              14            32

     20         21                         1           2         11            20        21                              1            2         11
                              6                                                                         6
12         31        26                9       27           24        7   12        31         26                9           27            24        7


                              t33a                                                                 t33b75
0.143447408371201                                   79 bonds              0.143447385418276                                       75 bonds




                                   4                                                                         13

                              3         16                                                              21        31

                         10        15        28                                                         20           8
                                                                                               1                             15
                     5        33        22        18
                                                                                                            23
                                                                                                   6                 26               10
                8        30        23        13        25                                22

                                                                                    11        5         7         29          12           16
          19             29        17          14          32
     20         21                         1                     11            30        9         18        3           32           24        25
                              6                        2
12         31        26                9       27           24        7   28        27        14        2         17              4        19        33


                         t33b79                                                                         t33c
0.143447385418276                                   79 bonds              0.143309997215537                                       74 bonds


Figure 3.10: The best (t33a), the next-best (t33b75, t33b79), and the third-best (t33c) packings
of 33 disks.
                                                                                                                                               18




                                   10                                                                        10

                              25        11                                                              25           11

                         8         12        3                                                     8         12           3

                    24        30        14        15                                          24        30           14        15

               19        28        13        6         20                                19        28        13           6         20

          32        18        17                  31        29                      32        18        17                     31        29
                                                                                                                     2
                                         2
     23        27        1                             16        26            23        27         1                               16        26
                                                                                                                     33
                                        33
21        4         34        5                   22        7         9   21        4         34             5                 22        7         9


                              t34a                                                                     t34b
0.142869646754496                                  84 bonds               0.142867647681844                                     83 bonds




                                   11                                                                        11

                              28        20                                                              28           20

                         17        10        24                                                    17        10           24

                    15        12        3         19                                          15        12           3         19

               27        22        21        16        30                                27        22        21           16        30

          2         4         34        14         7        5                       2         4         34           14         7        5

     25        26        32         9             18            23             25        26        32            9             18         23
8         29        13        33         31             6             1   8         29        13        33            31             6             1


                              t34c                                                                     t34d
0.142866887845831                                  84 bonds               0.142866698669904                                     83 bonds


Figure 3.11: The best (t34a), the next-best (t34b), the third-best (t34c), and the fourth-best
(t34d82) packings of 34 disks.
                                                                                               19

4      Conjectures for individual packings

      Each packing diagram we give can imply several different statements:

    (I) There exists a valid configuration of nonoverlapping disks with all pairwise distances
       marked by bonds equal to zero, and those not marked by bonds strictly positive, and
       with disk diameter equal to the indicated value with a relative error of less than 10−14 .

 (II) The configuration is rigid: no disk or set of disks except for rattlers can be continuously
       displaced from the indicated positions without overlaps.

(III) The configurations are correctly ranked. That is, the a-packing really is optimal, the
       b-packing is second best, etc.

     We believe (I) and (II) are correct. As to (III), we hope the statement is correct with
respect to the a-packings. In other words, we believe these are the optimal packings. We are
less confident for the lower ranked packings. For example, if someone finds a new packing
in between our c- and d-packings, we will not be astounded. We provide these mainly for
comparison purposes, and to serve as benchmarks for other packing algorithms.
     It would also not be surprising to discover a nonisomorphic packing to one we have presented
which has exactly the same disk diameter and the same number of bonds (e.g., as in t17b42ns
and t17b42s in Fig. 2.1).


5      Conjectures for infinite classes

      Dense packings in an equilateral triangle seem to “prefer” to form blocks of dense triangles
and arrangements that are nearly so. In this section we describe seven infinite classes where
we think we have found the optimal packings. Each class has its individual pattern of the
optimal packings, which is different from the patterns for other classes. However, since they
are the result of the particular packings we found, which themselves are only conjectured to
be optimal, then the general conjectures have even less reliability. We still think they might
serve as useful organizers for the maze of published dense packings.


4∆(k). The best packing (we found) of 24 = 4∆(3) disks in Fig. 3.3 consists of four triangles,
each with ∆(3) = 6 disks. The best packings of 12 disks (in [M1]) in Fig. 5.1, and even 4 disks in
Fig. 4.1 have the same form. The packings we obtained while experimenting with 40 = 4∆(4)
                                                                                                        20




                                                                                    2



                  3                                                            8         6



                                                                           7                 1
                  4

         1                 2                                       4                5               3



              t4a                                                                  t8a
0.577350269189626          9 bonds                            0.343070330817254                  18 bonds

                  Figure 4.1: The best packing of 4 disks (t4a) and 8 disks (t8a).


  and 60 = 4∆(5) disks (see Fig. 5.2), and also with 84 = 4∆(6) and 112 = 4∆(7) disks have
  the same structure as well.
                                                                           1 √
     A simple analysis of the patterns obtained implies that d(4∆(k)) = 2k−2+  3
                                                                                 .
     If we fit members of class 4∆(.) within the boundaries of the triangular periods, i.e., among
  members of the class ∆(.), then every other period has exactly one n of the form 4∆(k) lying
  almost exactly at the middle of the period.


  2∆(k + 1) + 2∆(k) − 1.        For each k there are k + 1 distinct best packings: two for 7 disks
  (Fig. 1.1), three for 17 disks (Fig. 2.1), four for 31 disks (three of these four are shown in
  Fig. 3.8), and five for 49 disks (four of these five are shown in Fig. 5.3).
                                                                                                                                   21




                   8                                             11                                             3

              11       6                                    7         4                                     6       11

          7                 2                                                                           5       1        12
                   1                                        12        3
                                                    6                         2                     2           7             4
          3                10                                    10
      4            5            9               5       1                 8       9             9       13           8            10

              t11a                                      t12a                                                t13a
0.275255128608411 22 bonds 0.267949192431123 30 bonds 0.251813236653061 30 bonds


    Figure 5.1: The best packings of 11 disks (t11a), of 12 disks (t12a), and of 13 disks (t13a).




                       t40a                                                                      t60a
    0.129331793710034               108 bonds                                         0.102753265449690             154 bonds


                   Figure 5.2: The best packings of 40 disks (t40a) and 60 disks (t60a).
                                                                                                                                                                            22




                                            23                                                                                          23
                                       37        34                                                                                37        34
                                  20        48        9                                                                    20           48        9
                             19        43        28        33                                                         19           43        28        33

                             40        17        49        10                                                         40           17        49        10
                    46                                              38                                          46                                           38
                                  1         18        41                                                                       1        18        41
               27        7                                     35        45                                27        7                                  35        45
                                       16        8                                                                                 16        8
          24        5        44                            3        39        22                      24        5         44                                 39        22
                                            11                                                                                          11        3
     30        14       36        12              31           21        13        26            30        14        36        12                       21        13        26
                                                                                                                                             31
2         42        6        25             4          15           29        32        47   2        42        6         25        4              15        29        32        47


                             t49a130                                                                             t49a132.2
0.114520634618068                                              130 bonds                     0.114520634618068                                          132 bonds




                                            2                                                                                           23
                                       42        30                                                                                37        34
                                  6         14        24                                                                   20           48        9
                             25        36        5         27                                                         19           43        28        33
                         4        12        44        7         46                                                    40           17        49        10
                                                                                                                46                                           38
                     31           11        16        1         40                                                             1        18        41
               15                                                        19                                27        7                                            45
                             3         8         18        17                                                                      16        8         35
          29        21                                              43        20                      24        5         44                                 39        22
                                  35        41        49                                                                                11        3
     32        13       39                                     28        48        37            30        14        36        12                       21        13        26
                                       38        10                                                                                          31
47        26        22       45                        33            9        34        23   2        42        6         25        4              15        29        32        47


                             t49a133                                                                             t49a132.3
0.114520634618068                                              133 bonds                     0.114520634618068                                          132 bonds


                              Figure 5.3: Four (out of the five existing) best packings of 49 disks.
                                                                                                                    23



                                  5                                                         6

                             10        4                                                23 36
                                                                                      13 39         2
                        29        37        1
                                                                                     46 22 49 40
                   7         16        18        30                                21 34 48 14 54
              12        22        31        35        8                          15 17 53 47 10               4
                                                                               42 41 45     1       50 27 52
          3        36        20        17        33        21
                                                                              38 12 55 32       5       31 19 33
     28                 27                  2                   19
              26                  15                  25                     25 26 11 8 24               43 37      9
                                                                                                    7
     14                 24                  6               11                20    29    56             18        44
23            13                  9               32                 34   28     35    30           3         51        16


                         t37a                                                          t56a
0.132739196122383                                 84 bonds                0.105229325597427              133 bonds

                    Figure 5.4: The best packings of 37 disks (t37a) and 56 disks (t56a).


     There are three different numbers of bonds in these packings; the smallest number of bonds
is in the packing with a rattler, then k − 2 packings each of which has a “cavity” and the same
number of bonds, and finally one more packing without a rattler or a cavity with the largest
number of bonds. The four triangles, two small and two large, that illustrate the expression
2∆(k + 1) + 2∆(k) − 1, can be seen in the packings with a rattler (t17a40, t31a79, t49a130).
The two larger triangles are defective: both coalesce a corner disk (disk 6 in t17a40, disk 4 in
t31a79, disk 4 in t49a130). Packing t31a81.2 is obtained from t31a79 by the left larger triangle
acquiring its corner disk 4 and pushing disks 31 and 29 from the left side of the other large
triangle down into the cavity formed . If we push only disk 31, we obtain a packing t31a81.1
(not shown). If we push all three disks 31, 29, 10 into the cavity (and rotate the resulting
structure to recover the symmetry with respect to the vertical axis), we obtain the fourth best
packing t31a82.
                                                                                     1 √
     A simple analysis of the patterns obtained implies that d(2∆(k+1)+2∆(k)−1) = 2k−1+ 3
                                                                                          .
Our experiments with 71 = 2∆(6) + 2∆(5) − 1 disks produced the same patterns for the best
packing.
     If we fit the members of class 2∆(k + 1) + 2∆(k) − 1 into the boundaries of the triangular
                                                                                                                                        24



                        16                                           16                                          3

                12           14                              12           14                                 7        13

               15                 8                         15                 8                         6       16        1
                         5                                            5
         11                       4                    11                          2                4                 14
                    6                                            6                                           8
                                          2                                4                                                       15
          10                 7                         10                          3                10                12
   13               9                 3       1   13             9        7            1       11            2                 9         5


          t16a33.1                                      t16a33.2                                             t16b
0.216227269309782                     33 bonds 0.216227269309782                   33 bonds 0.215843184970192                  32 bonds


        Figure 5.5: The best (t16a33.1, t16a33.2) and the next-best (t16b) packings of 16 disks.


   periods, as we did for the class 4∆(k), we find that every other period has exactly one n of
   the form 2∆(k + 1) + 2∆(k) − 1 which lies almost exactly in the center of the period. Thus,
   classes 2∆(k + 1) + 2∆(k) − 1 and 4∆(k) are “parity-complementary” to each other. Beginning
   with the second triangular period 3 to 6, each period has exactly one term of one or the other
   class; even periods contain terms of the class 4∆(k) and odd periods contain terms of the class
   2∆(k + 1) + 2∆(k) − 1.
        The pattern of one of the parity-complementary class pair can be obtained from the pattern
   of the other class by a simple transformation. For example if we eliminate the eight bottom
   disks 2, 42, 6, 25, 15, 29, 32, 47, and the rattler 4 in t49a130 (Fig. 5.3), we obtain the pattern
   of t40a (Fig. 5.2).


   ∆(2k) + 1.                As we noted earlier, ∆(m) densely packed disks in an equilateral triangle form
   a perfect hexagonal lattice with m disks on a side. When m = 2k is even, the structure
   with ∆(2k) + 1 disks adjusts itself to one extra disk as follows. The top 2k − 1 rows remain
   packed hexagonally, and the bottom row ripples to accommodate 2k + 1 disks instead of 2k.
   In this ripple of the bottom row, the 1st, 3rd, ... (2k + 1)th disk beginning from the left corner
   remain attached to the bottom, while the 2nd, 4th, ... 2kth disk rise and attach themselves
   to 2nd, 4th, ... 2kth disks respectively, of the row above. Thus, k − 1 rigid cages are formed.
   The k − 1 disks of the row above to which no disk is attached from below fall off into these
   cages and become rattlers. The first seven terms of the class ∆(2k) + 1 are: t4a (k = 1, no
   rattlers since k − 1 = 0, see Fig. 4.1), t11a (constructed in [M1] with one rattler; see Fig. 5.1),
                                                                                                                                                                25



                                        35                                                                                14
                                   32        27                                                                      12        37
                              20        26        37                                                            16        40        15
                         22        30        19        18                                                  31        27        36        45
                    36        41        13        14        42                                        38        34        20        32        26
               28        16        44        21        25        24                              35        19        21        13        42        29
          34        45        17        12        38                  8                     39        43        22        18        33                  8
                                                            5                                                                                  5
     43                  39                  11                           2            24                  17        23        11                           2
               33                  15                  6         4                               41                                      6         4
     29                  31              10                               3            46                  25              10                               3
40             23                  46                  9         7            1   28             44                  30                  9         7                 1


                               t46a                                                                   t46b106.2
0.117209943988839                                          106 bonds              0.117208402974392                                          106 bonds

                Figure 5.6: The best (t46a) and a next-best (t46b106.2) packings of 46 disks.


t22a (see Fig. 3.1) with two rattlers, t37 and t56 (Fig 5.4) with 3 and 4 rattlers, respectively,
t79a (194 bonds, 5 rattlers, d(79) = 0.0871159038791759), and t106a (267 bonds, 6 rattlers,
d(106) = 0.0742982999063026). We do not reproduce the diagrams here for the latter two
packings; their patterns are identical to the class description given above.


∆(2k + 1) + 1.                          When m = 2k + 1, k = 1, 2..., the odd parity of m causes a more complex
adjustment to the extra disk. The bottom row ripples in a non-symmetric way; the ripple
creates k cages for rattlers and a cavity; see t29a (Fig. 3.6) for k = 3.
     Notice that packing t29b63.2 (Fig. 3.6) has almost the same structure as t29a, except for
the cage that consists of disks 2, 3, 7, 9, 6, 5, and 8, is depressed and disk 4 in t29b63.2 is not a
rattler, and a nonrattler 6 in t29a becomes a rattler in t29b63.2. The same two modifications
exist for k = 4 (i.e., n = 46), and the modification with the depressed cage, t46b106.2, is
again inferior (Fig. 5.6). Beginning with k = 5 (i.e., n = 67), while both modifications exist,
they exchange their roles: the depressed one becomes the best, t67a161.2, while the other one
becomes the inferior one, t67b (Fig. 5.7). For example, t92a228.2 is the modification with
the depressed cage, while t92b is the other one (Fig. 5.8). The same pattern is displayed by
packing t121a307.2 (307 bonds, 6 rattlers, d(121) = 0.0691630188894699), for which we omit
                                                                                                                                                                      26



                                       49                                                                                        24
                                  29        37                                                                              67        42
                             62        39        14                                                                    23        45        56
                           13     19        28 54                                                                     26 60           37    57
                          42 17        60        56    61                                                        19    28        61        43 36
                     43    58     23        50 51           25                                              38        41 46           35    18     39
                15        16 65        36        47    57           32                                 59        31    54        44        49 34        17
           33        21    40     18        24 41           64           67                       52        16        12 64           13    47     14        55
          45    27        63 12        31        55        48                 8                  62 30           33    53        29        20 51                  8
                                                                    5                                                                                   5
     44              52           34 20               11                          2         25  66 50 21 40 48 11                                                     2
               46          38                                   6        4                                                                         6         4
     59              53           35              10                              3          27    63    65    10                                                     3
66             26          30           22                  9            7            1   32    22    15    58                                     9         7             1



                          t67a161.2                                                                                     t67b
     0.0952213722318656                                    161 bonds                       0.0952208239815187                                    161 bonds


                    Figure 5.7: A best (t67a161.2) and the next-best (t67b) packings of 67 disks.


 the diagram here.
      Labels t29b63.2, t46b106.2, t67a161.2, t92a228.2, and t121a307.2 have the suffix 2 in
 them because there exist equivalent packings t29b63.1, t46b106.1, t67a161.1, t92a228.1, and
 t121a307.1, respectively. The latter differ from the former in the placement of only 4 disks.
 An easy way to explain this is to look at the second term of the class n = ∆(2k + 1) + 1 for
 n = 16 disks (Fig. 5.5). In this case both modifications exist and both deliver the optimum,
 t16.a33.1 and t16.a33.2. They differ in the placement of disks 2, 3, 4, and 7.
      The side rattler disk 15 in t16b can be considered a precursor for the side rattler 29 in
 t29d. The same side-rattler pattern was observed in lower ranked packings for k = 4 (n = 46),
 k = 5 (n = 67), k = 6 (n = 92), and k = 7 (n = 121).
      Classes ∆(2k) + 1 and ∆(2k + 1) + 1 are a parity complementary pair, similar to the pair
 of classes 4∆(k) and 2∆(k + 1) + 2∆(k) − 1 considered above.


 ∆(k + 2) − 2.                  While the optimal packings of ∆(k + 2) − 1 disks are always (apparently)
 perfectly hexagonal with a single disk removed, the removal of two disks from a hexagonal
 arrangement is never optimal. The first two terms t4a and t8a (Fig. 4.1) suggest no common
                                                                                             27




           t92a228.2                                                   t92b
0.0801405249366249          228 bonds                   0.0801398309712360         228 bonds


        Figure 5.8: A best (t92a228.2) and the next-best (t92b) packings of 92 disks.


pattern. Looking at the next case t13a (Fig. 5.1) suggests the pattern for k ≥ 3 of a packed
triangle ∆(k) at the top, supported by two sparse rows of disks, each of which lacks a disk
compared to what would be there in a perfect hexagonal packing. The top-∆(k)-plus-two-
sparse-rows packing indeed exists for any k ≥ 3 and is rigid. In particular, the pattern appears
again in the best packings for k = 4 (t19a in Fig. 5.11).
   However, the optimality of this pattern does not continue for k > 4, as can be seen in
Fig. 3.5 where the best packing t26a has a different pattern. The top-∆(k)-plus-two-sparse-
rows pattern is not even among the top four packings for n = 26. The pattern for t26a and
t26b persists for the next term (see t34a and t34b in Fig. 3.11) but then roles become reversed
for 43 disks (see t43a and t43b in Fig. 5.10). Will the pattern of packing t43a remain optimal
for larger values of k? Unfortunately, our algorithm fails to obtain stable packings for 53 (or
larger values of ∆(k + 2) − 2) disks.


∆(3k + 1) + 2 =∆(3k − 1) + (2k + 1)∆(2).         30 = ∆(5) + 5∆(2) and packing t30a (Fig. 3.7)
can be viewed as a ∆(5) triangle on top from which disk 8 fell off and became a rattler,
supported by five triangles ∆(2) from below; t30a is the second term of the class. To produce
                                                                                            28




               t42a                                                    t63a
0.125451671189752          108 bonds                    0.100080300212798             165 bonds

           Figure 5.9: The best packings of 42 disks (t42a) and of 63 disks (t63a).


this structure for the next value of k we add two triangles ∆(2) on the bottom and three more
layers of disks to enlarge the top triangle to become a ∆(8) (and, in general, this procedure
is repeated for larger values of k). Indeed our experiments with n = 57 (k = 3) and n = 93
(k = 4) did produce this structure in the best packings (see t57a and t93a in Fig. 5.12). For
k = 1 we have n = 12, a degenerate case with no rattlers. The number of rattlers in this
packing for general k is k − 1.


∆(2k + 3) − 3 =∆(2k) + (2k + 1)∆(2).       The first term is packing t12a (Fig. 5.1) which also
belongs to class 4∆(.). The second term is packing t25a (Fig. 3.4) which can be viewed as
a ∆(2k) triangle on top supported by 2k + 1 alternating ∆(2) triangles below. This pattern
of the second term, whose description also fits the first term, is more apparent in the third
and fourth terms (see t42a and t63a shown in Fig. 5.9). According to our experiments the
next terms t88a and t117a do not continue this pattern but give way to patterns which are
somewhat similar to those of the class ∆(k + 2) − 2 considered above. (We omit diagrams for
both t88a and t117a.)
                                                                                             29

6      How good are the packings?

      Let us compare the values of the best packings with the only bound currently available,
namely one based on the inequality of Oler [O]. This inequality has the following form (see [FG]
for a simple proof): Let K be a compact, convex subset of E2 with area A(K) and perimeter
P (K). If p(K) denotes the maximum number of points that can be placed in K so that any
pair has mutual distance at least 1, then the following inequality holds:
                                          2      1
(1)                               p(K) ≤ √ A(K) + P (K) + 1 .
                                           3     2
Inverting (1) and applying it with p(K) = n and K being an equilateral triangle of side length
L(n), we obtain
                                            1      √
(2)                               L(n) ≥      (−3 + 8n + 1) := t(n) .
                                            2
      In Fig 6.1 we plot the difference

                                           δ(n) := L(n) − t(n)

versus n for selected values of n ≤ 121. A dot with a circle around it indicates that the
corresponding value has been proved to be optimal; a dot without a surrounding circle or an
open square indicates that the value is only conjectured to be optimal. For up to 37 disks
there were only four values which did not fall into one of our infinite classes, namely, n = 18,
23, 32, and 33; those are indicated by open squares. The values which have been associated
with classes are connected by lines, with a distinct type of line for each class.
      We should point out that for each n, the value of the largest disk diameter d(n) and the
value of L(n) are reciprocally related, i.e., d(n)L(n) = 1. Thus, L( k(k+1)
                                                                        2   ) = k − 1 for k ≥ 1.
If our conjecture for n = ∆(k) + 1 = k(k+1)
                                        2   + 1 is correct then it would follow that
                                      k(k + 1)        2
                                                
                          lim δ                + 1 ≤ √ − 1 = 0.1547 . . . .
                         k→∞             2             3
   Using the explicit values for d(4∆(k)) and d(2∆(k + 1) + 2∆(k) − 1) given in Section 5,
                                 √                                              √
we have L(4∆(k)) = 2k − 2 + 3 and L(2∆(k + 1) + 2∆(k) − 1) = 2k − 1 + 3, from
which it follows that both limk→∞ δ(4∆(k)) and limk→∞ δ(2∆(k + 1) + 2∆(k) − 1) are at most
√
  3 − 3/2 = 0.2321 . . . with the distance between kth term and the limit being of the order
of 1/k.
      We conjecture that for each of the classes n = ∆(2k) + 1, ∆(2k + 1) + 1, and ∆(3k + 1) + 2
the value of δ(n) is bounded away from zero. In fact, we believe that for any fixed c > 0,
                                                                                                30

the value of δ(∆(k) + c) is bounded away from zero. In other words, packings of ∆(k) disks
are so tight that any attempt to accommodate even one additional disk noticeably worsens
the packing in that L(n) increases by at least some positive amount independent of n. In this
sense the packings for the class ∆(k) are “tight”.
   On the other hand, we believe that after any fixed positive number of disks are added to
∆(k) disks, any other fixed number of disks can be added without substantial “damage” to
δ(n) (asymptotically). Thus, for example, it would seem that if limk→∞ δ(n(k)) exists for each
of the class n(k) = ∆(2k) + 1, ∆(2k + 1) + 1, and ∆(3k + 1) + 2 (and the limits probably do
exist), then all three limits are equal. In this sense the classes ∆(2k) + 1, ∆(2k + 1) + 1, and
∆(3k + 1) + 2 are “loose”.
   Similarly, the classes n = ∆(k + 2) − 2 and ∆(2k + 3) − 3 are “loose” in the sense that
we can add one disk to the best (conjectured) packing without noticeable change of δ(n) for
sufficiently large n. This follows from the fact that limk→∞ δ(∆(k) − p) → 0 for p fixed. The
latter limit is obvious by noticing that a lower-bounding packing for ∆(k) − p disks when k is
sufficiently large is simply the densest packing of ∆(k) disks with p disks removed; for such a
packing, δ is asymptotically 0.
   Formally, we say that an infinite class of packings of n disks, n = n(1), n(2), ...n(k), ..., is
loose, if limk→∞[δ(n(k) + 1) − δ(n(k))] = 0. Because we believe this limit exists for any class
we consider, each class has to be either tight or loose.
   We further conjecture that the classes 4∆(k) and 2∆(k + 1) + 2∆(k) − 1 are tight, similar
to the class ∆(k).
   Are there other tight classes? Here is our argument in favor of the existence of a countable
infinity of distinct tight classes. We believe that if each densest packing of n disks for n =
n(1), n(2),...n(k),.., consists of a fixed number, say r, of densely packed triangles ∆(.), then
δ(n(k) + 1) − δ(n(k)) is bounded away from zero as k goes to infinity.
   Thus, we have the following task: for each r from some infinite set find a sequence
n(1), n(2),...n(k),.., so that the densest packing of n(k) disks for all k has the “same pat-
tern” and consists of exactly r densely packed triangles. Note that a priori we are not able to
define what the “same pattern” is (and hence we have no formal definition of what a “class”
is); but after producing a class the pattern is usually clear.
   Let us consider a two-parameter family of numbers n = np (k), p = 1, 2..., k = 1, 2..., of
                                                                                                  31

the form

(3)          np (k) = ∆((k + 1)(p + 1) − 2) + k = ∆((k + 1)p − 1) + (2p + 1)∆(k) .

Two equal expressions for np (k) are given in (3). The second expression suggests r = 2(p + 1)
triangles. If we take, for example, k = p = 2, we get n2 (2) = 30 disks and r = 6. The
conjectured t30a (Fig 3.7) indeed consists of 6 densely packed triangles, if we attach rattler 8
to the top triangle ∆(5). Take now 58 = n2 (3). The pattern of our experimental packing t58a
(Fig 6.2) looks like t30a (Fig 3.7) with 6 triangles again (with the rattler attached to the top
triangle).
      Thus, just as t30a is a member of the class ∆(3k − 1) + (2k + 1)∆(2) for k = 2, t58a is
(perhaps) a member of the class ∆(4k − 1) + (2k + 1)∆(3) for k = 2. The pattern of the kth
packing of this class is composed of 2(k + 1) densely packed triangles. Is this class tight or
loose? We believe it is loose because ∆(4k − 1) + (2k + 1)∆(3) = ∆(3k + 1) + 2, and a class of
the form “∆(.) + const” is always loose (we think). Incidentally, the number of the triangles
in the class is unbounded with k.
      However, if (as we believe) the sequence of densest packings np (k), k = 1, 2, 3, ... for fixed
p = 2 can be continued with all packings having the same pattern of six triangles, then t58a
might also be a member of the class ∆(2k + 1) + 5∆(k) for k = 3. The next term in the latter
class would be the densest packing of n = n2 (4) = ∆(9) + 5∆(4) = 95 disks. Our experiments
with 95 disks, indeed, produced the desired pattern of six triangles in the densest packing t95a
(Fig. 6.2). This reinforces our suspicion that the class n2 (k), k = 1, 2, ..., exists in which each
densest packing consists of six densely packed triangles. The class n2 (k), k = 1, 2, ..., should
be tight because each densest packing in it consists of a fixed number of triangles.
      By increasing p we are moving into a different class, which is again tight if the conjecture
above is correct. Thus, for p = 3 we have the sequence n3 (1) = 22, n3 (2) = 57, n3 (3) =
108, n3 (4) = 175, .... Packings t22a (Fig 3.1), t57a (Fig 5.12) indeed each consist of 2(p + 1) = 8
densely packed triangles. Our experiments with 108 and 175 disks yield the same pattern in
the best packings (Fig 6.2) so the class n3 (k) probably exists too. In the same way, the class
np (k), k = 1, 2, ... exists for any fixed index p and has a distinct pattern with r = 2(p + 1)
triangles and p − 1 rattlers.
      If this is correct, then Figure 6.2 can be seen as the 2 × 2 submatrix for 2 ≤ p ≤ 3 and
3 ≤ k ≤ 4 of the matrix of dense packings of np (k) disks where 1 ≤ k, p ≤ ∞. By traversing a
                                                                                                32

row or a column of this matrix we obtain a distinct infinite class of packings. Our conjecture
is that each row class is tight and each column class is loose.
   This matrix contains three infinite classes conjectured in Section 5: the row at p = 1 is the
class 4∆(k), the column at k = 1 is the class ∆(2p) + 1, and the column at k = 2 is the class
∆(3p + 1) + 2 = ∆(3p − 1) + (2p + 1)∆(2).
   The conjecture about the full matrix is also reinforced by the fact that k and p in (3) are
unique for each given value of n = np (k). This can be easily seen using the first expression for
np (k) in (3). To further test our matrix conjecture, we generated the list of all n of the form
n = np (k) for n ≤ 300. These are: 4, 11, 12, 22, 24, 30, 37, 40, 56, 57, 58, 60, 79, 84, 93, 95,
106, 108, 112, 137, 138, 141, 144, 172, 174, 175, 180, 192, 196, 211, 220, 254, 255, 256, 258,
260, 264, and 280. Some increments in this increasing sequence are small. Specifically, in each
following subsequence increments do not exceed 2: (11, 12), (22, 24), (56, 57, 58, 60), (93, 95),
(106, 108), (137, 138), (172, 174, 175), and (254, 255, 256, 258, 260).
   Now, take for example, 255 = n7 (2) and 256 = n5 (3). These are two “almost” equal
numbers of disks. However according to the matrix conjecture they should produce different
patterns of densest packings: the pattern for 255 should consist of one large and 15 small
triangles with 6 rattlers and the pattern for 256 of one large and 11 small triangles and 4
rattlers. Similarly, the matrix conjecture prescribes specific patterns for the densest packing of
the other numbers of disks n of this sequence, e.g., 254 = n11 (1), 258 = n3 (5), and 260 = n2 (7).
   One might think it would be a stress test for both the matrix conjecture and our packing
procedure to try to pack these numbers of disks. Note that many of the packings for smaller
values in the sequences above have been generated (as discussed above) and they all conform
to the matrix conjecture. Thus, we experimented with packing n = 254, 255, 256, 258, and
260 disks. Recall that the procedure of packing has no idea, so to say, of the desirable packing.
Starting with random initial conditions the disks perform chaotic movements, they collide with
each other and with the boundaries millions of times and each collision evaluation is subject
to roundoff error.
   The experiments turned out to be not so difficult. (Case of 53 disks proved to be harder.)
As expected, the best packing of 254 disks has the pattern of its class ∆(2k)+1 with 10 rattlers
(d(254) = 0.0467170396481042, 679 bonds; we omit the diagram). Fig.6.3 shows the patterns
of packings t255a, t256a, t258, and t260a. These too are consistent with formula (3).        Note
that because of the large number of disks in the packings the scale of drawing in Fig.6.3 is
                                                                                                                                                                                              33

 small and bonds are not seen. The pictures with a larger scale (omitted here) show that all
 the bonds exist in right places.


  δ(n)
0.5

                 7
                   .•. . . . 16
          2...... . . . .•. . . . . . .. . . .29
          •                                  22
                                                        ..•. . . . . . ..
                                                                          . . . ..46
                                                                                  .•. . . . . .
                                      . . . . .•. .. ...  ...  ...    •
                                                                     .... .. .. .. .. .. .. .... . . . . . . . . . .67                               92.
                    11..•.  . . . . .
                                                                                                 ..•.. . .. .. ...•.... .... .... .... .... ...                                  n=∆(2k+1)+1
                                                                                                                               .. .. .... .. .. .. .. • . . . . . . . . . . . . . . . . . ..121
                                                                                                                                                          .. .
                                      18                            37                                               . .. . ..
0.4                      ..
                                               23                                               56                                   •               .. .. .. .. .. .. .. .                 . ..•
                       ..
                   ...•.                                   32                                       •                              79                   •                •
                 ... .                •                                                          57                                                                   106 n=∆(2k)+1
              ... 8 . 17                                   •                                                                                          93
          4•                                            30                                                                               n=∆(3k+1)+2
                              •. .                         •31
                            13 . 25
                                        .           • 33                                •
                             • •19        .                                           49                                  •
0.3            • 12 . 24                                                    42                                                    n=2∆(k+1)+2∆(k)-1
               5                                 .
                                                   •.                         •                                         71
                                                     •. .                 •                                            n=∆(2k+3)-3
                                                                        40                               •63  •                              •
                                                    26 .                                               60                                                                        •
                                                              .                                                                            84                               112            n=4∆(k)
                                                                 •. .
                        •                                     34 .
                        9                                                      •.
0.2                                                              43 n=∆(k+2)-2
                          •
                         14
                                   •                                                               • proved
                                  20
                                            •                                                      • conjectured and in a class
                                           27          •                                             conjectured and not in a class yet
0.1                                                   35           •
                                                                  44             •
                                                                                54              •               •
                                                                                               65                                 •                 •                n=∆(k+1)-1
                                                                                                               77                90                104                 •
                                                                                                                                                                      119

           3 6 10 15 21 28 36                                       45           55             66               78                91               105                  120
 0        •• • • • • • •                                             •            •              •                •                 •                •                    •
          1                                                                                                                                                                        n=∆(k)


                                  20                         40                         60                          80                       100                         120

                                                                   n, number of disks packed


 Figure 6.1: Discrepancy between side length of the triangle and its lower bound for different
 n.
                                                                                           34




            t58a                                               t95a
0.103809894100183     151 bonds                  0.0791578042660103       256 bonds




              t108a                                                t175a
  0.0736689924964931     287 bonds                    0.0569014905693285       479 bonds


Figure 6.2: The best packings of 58 disks (t58a), 95 disks (t95a), 108 disks (t108a), and 175
disks (t175a).
                                                                                          35




               t255a                                                 t256a
0.0465999333293566         693 bonds                  0.0465050212813994         703 bonds




               t258a                                                 t260a
0.0463515918933559         719 bonds                  0.0462256883510349         733 bonds

Figure 6.3: The best packings of 255 disks (t255a), 256 disks (t256a), 258 disks (t258a), and
260 disks (t260a).
                                                                                                                                                                36




                                        41                                                                                   5
                                   33        43                                                                         7         42
                              21        15        7                                                                2         36        38
                         38        9         12        8                                                      20        41        11        23
                    6         42        36        32        10                                           21        30        40        10        15
               13        27        3         24        28        2                                  43        12        32        16        37        33
          5         17        16        26        1         18        19                       14        31        17                  6         25        28
                                                                                                                             34
     40        39        31        4         25             22         23                 24        1         35                            26        27        29
35        11        29        30        14         34            20             37   22        13        4         39        19        18        9         3         8


                               t43a                                                                                 t43b
0.125004280307977                                       108 bonds                    0.125003232541680                                       108 bonds




                                        28                                                                                   43

                                        24                                                                              15        42
                               6              36                                                                   13        1         26
                         4         39        8         35                                                     21        9         4         29
                    42        20        16        3         30                                           30        10        16        11        23
               13        23        12        14        1         41                                 36        20        25        17        28        24
          31        22        19        27        18        9         33                       6         8         2         14        3         41        19
     2         40        34        43        29        11        26        37             22        31        40                           18         39        37
                                                                                                                             35
17        15        25        5         7         21        38        32        10   34        38        33         5              12            27        32        7


                               t43c                                                                                 t43d
0.125002529873623                                       108 bonds                    0.125002234829571                                       106 bonds


Figure 5.10: The best (t43a), the next-best (t43b), the third-best (t43c) and the fourth-best
(t43d) packings of 43 disks.
                                                                                                                                                                37




                          7                                                           10                                                  1

                      8        19                                                4         7                                         17           6

                  1       18        2                                       11        13       15                               16        2            3
             10       6        4        16                             14        19                 1                      10        19       12           18
                                                                                           5
        11        12            3            14                   12         2                           8             5        7             8            13
                                                                                           6
   13         9           5         15            17         17        16        18                 9        3    14       9         11               4         15

                      t19a                                                   t19b                                                   t19c
0.200321458983439 45 bonds 0.200200894290590 45 bonds 0.200186574270937 45 bonds


   Figure 5.11: The best (t19a), the next best (t19b), and the third best (t19c) packings of 19
   disks.




                                t57a                                                                                   t93a
  0.104447019187802                                    143 bonds                                        0.07978572868437232                           240 bonds

                          Figure 5.12: The best packings of 57 disks (t57a) and 93 disks (t93a).
                                                                                                   38

7       Discussion

       While a finite number of patterns for infinite classes have been tentatively identified to date
(two one-parameter patterns known or conjectured previously joined by several such patterns
in Sec.5 and a two-parameter “matrix” pattern in Sec.6) a countable infinity of such patterns
and classes probably exists. Furthermore, each value of n may well be a member of one or
more such classes. Thus, the values n = 18, 23, 32, and 33, which were not placed into classes
in this paper, may well be members of as yet unidentified classes of packings with complex
patterns. In fact, a fixed value of n may be on the paths of many, possibly infinitely many,
such classes. 12 disks gives an example of this: it is on the path of the class 4∆(k) and it is
also the first term of the classes ∆(3k + 1) + 2 and ∆(2k + 3) − 3. As the value of n increases
along the path of a class, “hesitations” of the best pattern may occur, wherein several different
nonequivalent patterns coexist among the rigid packings and compete for the title of the best.
A resolved case of such hesitation occurs for the class ∆(2k + 1) + 1 where for k ≥ 5 (n ≥ 67)
two equivalent best patterns finally emerge (at least according to our experiments). We were
not able to confirm by experiments the winning pattern for the class ∆(k + 2) − 2. Will such
hesitation always be resolved in favor of one of the competing patterns in a finite initial segment
of the path?


References

[CFG]         H. T. Croft, K. J. Falconer and R. K. Guy, Unsolved Problems in Geometry, Springer
              Verlag, Berlin, 1991, 107–111.

[FG]          J. H. Folkman and R. L. Graham, A packing inequality for compact convex subsets
              of the plane, Canad. Math. Bull. 12 (1969), 745–752.

[L]           B. D. Lubachevsky, How to simulate billiards and similar systems, J. Computational
              Physics 94 (1991), 255–283.

[LS]          B. D. Lubachevsky and F. H. Stillinger, Geometric properties of random disk pack-
              ings, J. Statistical Physics 60 (1990), 561–583.

[M1]          J. B. M. Melissen, Densest packings for congruent circles in an equilateral triangle,
              Amer. Math. Monthly 100 (1993), 916–925.
                                                                                           39

[M2]   J. B. M. Melissen, Optimal packings of eleven equal circles in an equilateral triangle,
       Acta Math. Hung. 65 (1994), 389–393.

[MS]   J. B. M. Melissen and P. C. Schuur, Packing 16, 17 or 18 circles on an equilateral
       triangle, Disc. Math. (to appear).

[N]    D. J. Newman, private communication.

[O]    N. Oler, A finite packing problem, Canad. Math. Bull. 4 (1961), 153–155.
