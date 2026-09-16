                                                                 Repeated Patterns of Dense Packings
                                                                     of Equal Disks in a Square
                                                                          R. L. Graham, rlg@research.att.com
                                                                        B. D. Lubachevsky, bdl@research.att.com
arXiv:math/0406394v1 [math.MG] 21 Jun 2004




                                                                                AT&T Bell Laboratories
                                                                           Murray Hill, New Jersey 07974, USA



                                                                                       ABSTRACT

                                                 We examine sequences of dense packings of n congruent non-overlapping disks inside a
                                             square which follow specific patterns as n increases along certain values, n = n(1), n(2), ...n(k), ....
                                             Extending and improving previous work of Nurmela and Östergård [NO] where previous pat-
                                             terns for n = n(k) of the form k2 , k2 − 1, k2 − 3, k(k + 1), and 4k2 + k were observed, we
                                             identify new patterns for n = k2 − 2 and n = k2 + ⌊k/2⌋. We also find denser packings than
                                             those in [NO] for n =21, 28, 34, 40, 43, 44, 45, and 47. In addition, we produce what we
                                             conjecture to be optimal packings for n =51, 52, 54, 55, 56, 60, and 61. Finally, for each
                                             identified sequence n(1), n(2), ...n(k), ... which corresponds to some specific repeated pattern,
                                             we identify a threshold index k0 , for which the packing appears to be optimal for k ≤ k0 , but
                                             for which the packing is not optimal (or does not exist) for k > k0 .

                                             1. Introduction

                                                  In a previous paper [GL1], the authors observed the unexpected occurrence of repeating
                                             “patterns” of dense (and presumably optimal) packings of n equal non-overlapping disks in-
                                             side an equilateral triangle (see Fig. 1.1 for and example). It is natural to investigate this
                                             phenomenon for other boundary shapes. In particular, this was done by the authors [LG1]
                                             for the case of n disks in a circle. However, in contrast to the case of the equilateral triangle
                                             where the patterns appear to persist for arbitrarily large values of n, for the circle the identified
                                             packing patterns cease to be optimal as the number of disks exceeds a certain threshold.
                                                 In this note we describe the situation for the square. In a recent paper, Nurmela and
                                             Östergård [NO] present various conjectured optimal packings of n equal disks in a square for
                                             up to 50 disks. They also point out certain patterns that occur there. By using a packing
                                             procedure different from theirs, we improve on their best packings for n = 21, 28, 34, 40, 43,
                                             44, 45, and 47. We conjecture that these new packings are optimal, as are the new packings
                                             we give for n = 51, 52, 54, 55, 56, 60, and 61.
                                                 We confirm all the repeated patterns mentioned in [NO], specifically, for n = k2 , k2 − 1,
                                             k2 −3, and k(k+1), and we identify two new patterns, namely, for n = k2 −2 and n = k2 +⌊k/2⌋
                                             The latter pattern incorporates the packings of n = 4k2 + k disks as identified in [NO].
                                                 It was found in [NO] that the obvious “square” pattern of packings of n = k2 disks becomes
                                             non-optimal for n > n0 = 36. This was done by presenting a configuration of k2 = 49 disks
                                                                                                      2




Figure 1.1: The conjectured densest packing of n = 256 disks inside an equilateral triangle, a
member of the series n = np (k) = ∆((k + 1)p − 1) + (2p + 1)∆(k) for p = 5 and k = 3, where
∆(m) = m(m + 1)/2. The n − p + 1 = 252 shaded disks can not move (they are “solid”), the
p−1 = 4 non-shaded disks are free to move within their local confines (they are “rattlers”). The
densest packings of n disks for all checked values of the form n = np (k), p = 1, 2, ..., k = 1, 2, ...,
have this pattern consisting of one triangle of side (k + 1)p − 1 and 2p + 1 triangles of side k
with p − 1 rattlers that are “falling off” the larger triangle.


with the diameters larger than m = 1/(k − 1). The latter m is disk diameter in the packing
that obeys the pattern. The standard unit of measure used in most papers on the subject is the
side of the smallest square that contains the centers of disks. We repeat the same procedure
for the other patterns identified both in [NO] and in the present paper. Namely, for each
pattern we state the rule of its formation which allows us to compute the corresponding value
of m = m(n). Then we pinpoint the n0 that belongs to the series and such that the packing
of n0 disks constructed according to the rule is (presumably) optimal, but for which m(n1 )
for the next value n1 > n0 in the series when the packing is also constructed according to the
rule is worse than a certain challenger disk configuration (which may or may not be a solid
packing).
    In this manner, we confirm observation in [NO] that the best packings of n = k2 − 1 disks
loose their characteristic pattern for n ≥ n1 = 48 disks. We also found that although it was
not stated in [NO], the packing of 47 disks presented there (as well as our better packing of
47 disks) challenges the series k2 − 2. Thus, the pattern of the series n = k 2 − 2 becomes
non-optimal for n > n0 = 34, and that of the series n = k2 − 1 for n > n0 = 35. We also
found challenger disk configurations or packings for other patterns for values of n > 50 which
were not identified in [NO]. Namely: n0 = 56 for the series k(k + 1) (with the challenger
n1 = 72), and n0 = 61 for the series k2 − 3 (with the challenger n1 = 78). The situation for the
                                                                                                        3

series n = n(k) = k2 + ⌊k/2⌋ (n = 5, 10, 18, 27, 39, 52, 68,...) is more complex: the pattern
exists for 5 ≤ n(k) ≤ 52 as a solid packing and is probably optimal for these n(k) except the
case n = n(3) = 10 which is the subject of several publications ([G], [Sch], [Schl], [Val]). For
n = n(8) = 68 the configuration constructed according to the pattern rule has a slight disk
overlap, i.e., it does not exist as a disk packing, and the overlap persists for all n = n(k) > 68.
    In the geometric packing problem, progress in proving lags that of conjecturing. Thus,
we should warn the reader that almost all our statements are conjectures; they are based on
computer experimentations with the so-called “billiards” simulation algorithm [L], [LS]. In all
series except k2 − 3, the construction rule we found for generating a pattern for a given n is
a finite procedure and m(n) can be expressed as the root of a well-defined polynomial. The
existence of the packing of a given pattern for a fixed n, even if not the pattern’s optimality
(when appropriate), should be considered proven. However, for the series k2 − 3 we have to
resort on an infinite simulation procedure [L], [LS] to construct a pattern for an arbitrary n and
to compute m(n). Hence even the pattern’s existence as a solid packing is a conjecture here.
We point out that some of the proposed methods in the literature attempt to prove a packing
optimal or, at the least, prove that a packing with particular parameters exists. Usually to
fulfill this task, the packing must be actually presented, even if only as a conjecture. Thus,
we try to present our conjectured packings in a verifiable and reproducible form; we provide
14 decimal digits of accuracy for its parameter m and clearly identify the connectivity pattern
(touching disk-disk and disk-wall pairs). Some previous papers provided disk coordinates in
the presented packings. 1 The interested reader can contact the authors directly for the
coordinates (since that would otherwise take up too much space in the paper).

2. Packings

     The parameter m supplied with each packing is the ratio of the disk diameter to the side
length of the smallest square that contains the disk centers. Bonds or contact points mark
disk-disk or disk-boundary contact. In the packing diagrams, bonds are indicated by black
dots. Most of the packings presented are conjectures. This means that a proof is required not
only for their optimality, if any, but even for their existence. Thus, a bond implies a conjecture
that the corresponding distance is zero while the absence of a bond implies a conjecture that
the distance is strictly positive. We placed or did not place a bond between two disks or a disk
and a boundary based on the numerical evidence: the bond was placed when the corresponding
distance was less than 10−12 of the disk diameter. Such a choice of a threshold is supported
by the existence of a well-formed gap between a bond and a no-bond situation: In all cases
when the bond is not present between apparently touching surfaces, the computed distance
is at least 10−7 of the disk diameter, and, except for the packing of 47 disks in Fig.2.6, it is
at least 10−5 . The existence of this gap also testifies to that in all the packings the double
  1
    We were unable to reproduce the best packing of 21 disks for which [MFP] provides the diameter m =
0.27181675 but no other data, e.g. no contact diagram. Our best packing of 21 disks has a smaller diameter
(see Fig. 2.1).
                                                                                               4

precision resolution we employed for the computations sufficed. All solid disks, i.e., those that
can not move, are shaded in the packing diagrams; the non-shaded disks are rattlers— they are
free to move within their confines. Different shadings of disks in some packings and a unique
numerical label for each disk on a diagram are provided to facilitate the discussion, These are
not part of the packings.
                                                                                                                                     5



             1              17            10              14          10              7                 1             18


                                                                                                                                11
   3              18              16                15                          6             22
                                                                                                             21

                                                              2       2              15             16                          5
         21                 13                 9
                                                                                                                  4

   6               8              11                          7       17             13                 3                       14
                                               20                                                                12

   5               4              12                          19      9               8             19                          20


                       21 disks                                                           22 disks
m = 0.27181225535931                                39 bonds       m = 0.26795840155072                               43 bonds

   9                             2                            4       13                           3             8              7
                  11                           5                                    19


        16                            3                  12                18                  2            22             20
                       19
                                               23                                   11
   15                            7                            8       5                            17            16             23
                  13
                                          18                                         9
        22                  20                           1            12                           24            4              14


                  14                           6                                     1
   10                            17                           21      6                            21            15             10


                       23 disks                                                     24 disks (2,2)
m = 0.25881904510252                                56 bonds       m = 0.25433309503025                               56 bonds

   13             3                            8              7       13             3                           8              7
                                 19                                                                19

        18             2                  22             20           5              17                          16             23
                                                                                                   11
                                 11
   5              17                           16             23           18             2                 22             20

                                 9                                                                 9
   12             24                           4              14      12             24                          4              14


                                 1                                                                 1
   6              21                           15             10      6              21                          15             10


                 24 disks (2,3)                                                     24 disks (3,3)
m = 0.25433309503025                                56 bonds       m = 0.25433309503025                               56 bonds


                 Figure 2.1: The densest packings found of 21 to 24 disks
                                                                                                6



  20        3         5         18        25        22         5                  2
                                                                       12                  21
                                                         25
  22    13            24         9            2                                  11
                                                    15             3
                                                                                           24
                                                         17             26
  21        6         12         8        17         8          18                    20
                                                          1             23
                                                                                           19
  11        1         23         4        16        16             4
                                                                                  7
                                                         13
                                                                                           6
  10        7         15        14        19         9          14          10


                25 disks                                      26 disks
m = 0.25000000000000                 60 bonds     m = 0.23873475724122            56 bonds

  12             19                  17             15        25                 16        26

       16                  25                 8          2             28

  13             18                  26                        21                4         23
                                                    27
       1                   4                  2          11             9
                                                                                           13
  22             24                  27              7          5                12

       5                   9              21             19            10
                                                                                           22
  14              3                  23             20         14                 1
       7                   6              11             6              3
                                                                                           18
  15             10                  20              8         24                17


                27 disks                                      28 disks
m = 0.23584952830142                 55 bonds     m = 0.23053549364267            57 bonds


   4        20        28        25        2              12             18                 29
                                                     2          6                 3
       15                  22             14             1              27                 22
  26             10                  18              5         15                 19
       24                  6              19             9              13                 16
  27              1                  29             30         17                 25
       21                  7                  8          8              28                 23
  23              3                  12             24         14                 4
       16                  11                 9          20             11                 26
  13             17                  5               7         10                 21


                29 disks                                      30 disks
m = 0.22688290074421                 65 bonds     m = 0.22450296453109            65 bonds


            Figure 2.2: The densest packings found of 25 to 30 disks
                                                                                                                                                   7



        17               24            20             18            27              28             18         11            23             27

   6            15                 7            11                            20          15             4          14               29
                                                                    26
                                                          19                                       10         22                               2
           28            13                                                         25                                      32
                                            4
                                                                    16
   2            10             30                         31                  26          31            19              6                      9
                                             12                         3                                                        21
   8             1             22                         23                  13          1             12              3                      8
                                            29                      21                                                           30
   9            25                 5                      14                  24          7             16              5                  17


                         31 disks                                                                  32 disks
m = 0.21754729161912                                      55 bonds          m = 0.21308235294443 61 bonds

  28            22             7                 6             4               5                        33                   28            20
                                                                                         34                        22

        32               12            20                           31
                                                      14                           2                     14                 3             12
                                                                                              15
   1            21            15             23                     18                                             9
                                                                              21                        13                       6         31
                                                          19                              1
                                                                                                              18
  11            13            29                 3                  10             30              23                       29            32
                                                          30
                                                                                          4                        10
  16             5             8                 9                  17        25                        16                   24            11
                                                           2
                                                                                         17                        27
  33            27            24             25                     26         8                        26                   19                7


                         33 disks                                                       34 disks (2,4;2,4)
m = 0.21132838414326                                      65 bonds          m = 0.20560464675957                                 80 bonds

   5                          33                      28            20         5                        33                   28            20
                34                          22                                           34                        22

       2                       14                    3             12         21                        13                       6         31
                    15                                                                    1                        9
                                            9
  21                          13                          6         31             2                     14                 3             12
                1                                                                             15
                                            10                                                                     10
  25                          16                      24            11        25                        16                   24            11
                4                                                                         4
                                       18                                                                     18
       30                23                          29            32              30              23                       29            32

                17                          27                                           17                        27
   8                          26                      19                7      8                        26                   19                7


            34 disks (2,5;2,4)                                                          34 disks (3,5;2,4)
m = 0.20560464675957                                      80 bonds          m = 0.20560464675957                                 80 bonds


                     Figure 2.3: The densest packings found of 31 to 34 disks
                                                                                                                               8



  5                    33        28                    20        29                      4         30             6       33
             34                               22                       12

       2                   14            3            12          16                28         14            10           5
                 15
                                                  9                    27
  21                   13            6                 31        7                       17         8         11          35
             1
                                              10                       15
  25                   16        24                    11        1                       25        31         21          13
             4
                                             18                        18
      30              23        29                    32         22                      23        32             3       34

             17                               27                       26
  8                    26        19                        7     19                      2         24             9       20


           34 disks (2,5;2,5)                                          35 disks (2,2)
m= 0.20560464675957                           80 bonds         m= 0.20276360086323 80 bonds

  29         4                   30               6    33        29        4                       30             6       33
                       12                                                                12

   16            28             14           10       5          7     17                           8         11          35
                                                                                         27
                       27
  7          17                      8        11       35         16           28              14            10           5

                       15                                                                15
  1          25                  31           21       13        1     25                          31         21          13

                       18                                                                18
  22         23                  32               3    34        22    23                          32             3       34

                       26                                                                26
  19         2                   24               9    20        19        2                       24             9       20


             35 disks (2,3)                                            35 disks (3,3)
m= 0.20276360086323 80 bonds                                   m= 0.20276360086323 80 bonds

  32         1         20        23           33       12        13    11                34        12         36          29


  14         9         25        13               8        6     6                  21                   7                27
                                                                       4                      3                       8
  24         11        19        22               7    31        18                 10                  20                33
                                                                       5                      35                  9
  34         36        35        10           21       18        17                                                       32
                                                                                    31                  24
                                                                       1                                          28
                                                                                              30
  28         17        27            2        29           5     2              19                       14               37


  30         3             4     26           15       16        22    23                25        15         16          26


                      36 disks                                                      37 disks
m= 0.20000000000000                           84 bonds         m= 0.19623810145141                            73 bonds


                  Figure 2.4: The densest packings found of 34 to 37 disks
                                                                                                                                   9


  26             15                      35                 7     13                    9                  23                 38
        5                  25                      18                        17                  19                  25
  8              17                      10                14     15                   35                  26                 20
       31                  27                       13                       39                  28                  22
  37             38                      33                30     27                    7                  4                  34
        2                  16                      12                        33                  24                  29
  36             3                       21                11     32                   37                  10                 31
       32                  29                          4                     12                  30                  1
  22             1                       9                 34     3                     6                  16                 36
                                                                             5                   21                  11
  28    20            23            19             6       24     14                   18                  2                  8


                 38 disks                                                              39 disks
m= 0.19534230412691                                77 bonds     m= 0.19436506316151 80 bonds

  18        35         26            25            28              14             36                   1        34        3
                                                           17
                                                                                            31
       16                       7             36                             27                            15                 23
  31             32                                        11     17                   18        29                  38
                            9                          1                     16                            11
       27                                                                                                                     6
  34             10                      30                33     4                    30        20                  2
       39                   38                      37                       13                            32                 12
  19             24                       3                 5     37                   40        35                  9
        4                   22                      13                       19                            22                 41
  21             20                       2                29     25                   28        26                  24
       40                   6                          8                     33                            39                 21
  15             23                      14                12     7                    5          8                  10


                 40 disks                                                              41 disks
m= 0.18817552201832 85 bonds                                    m= 0.18609951184812 100 bonds

       35                  34                          1          7          35            1      22                 38
  2              23                      11                 8                                              21                 6
       24                  28                       13                  8         26             43                  20
  21             31                      12                 3                                              15                 13
                                                                  37         27         25
       14                  41                       42                                            23                  3
  27             32                      6                 33                      16                      12                 24
                                                                        34
       36                  40                       30                                           31                  18
  17             7                       20                29     2          29         30                 42                 11
       4                   18                       25                                           40                  14
  5              16                      22                19     33          4         19                 5              32
       10                  37                       39                                           39                  36
  9              38                      15                26     9          10         17                 41                 28


                 42 disks                                                              43 disks
m= 0.18427707211710                                90 bonds     m= 0.18019113545743                              85 bonds


             Figure 2.5: The densest packings found of 38 to 43 disks
                                                                                                                                                   10


        13        38        31            7         19        6                 9        21            15         19         33            25

   14        11        43        15           40                      40            13           28          14        29            11
                                                              16

        41        34         2                       30                    6              4            43         39                       34
                                          22                                                                                  1
                                                              37
   12        10        44        18                  27                             23
                                                                      10                         44         35        30                       2
                                              36              4                                                               26
   5         33        32         1                  3                              16
                                                                      27                         3          41         7                   17
                                              29              26                                                              22
                                                                                    31
   21        39        20         9                  23               12                         36         24        37                   38
                                              17              28                                                                 5
                                                                                    8
   35        25         8        24                  42               45                         20         42        18                   32


                      44 disks                                                                45 disks
m = 0.17863924567120                                82 bonds       m = 0.17571631417559 94 bonds

   40        28        22        34           12         36           17            30           36         37        24                   46
                                                                                                                              42
        38        9         13        33                      39           27            2            38
                                                    30                                                                 3                   45
                                                                                                             29               18
   29        10        8         7            44              5       6             41
                                                                                                  26                   44                  19
                                                     35
                                                                                         11                  1                22
   23        46        27        21            6              20      33
                                                                                                      16               4                   34
                                                     25                         12
                                                                                                             14                   9
   45        32        16        19           24              42      10                  40
                                                                                                                       8                   20
                                                     15                         32                     25
                                                                                                                              15
   3         18        37        2            41              1       21                  35                     13
                                                                                                                                           47
                                                     4                              7                  28               43
   17        31        26        11           14              43      31                  23                     39                   5


                      46 disks                                                                47 disks
m = 0.17445936087241 91 bonds                                      m = 0.17126830721141 94 bonds

         10                 45                 42             13      29                     3                   32          1            13
   4              23              15                 18                         12                    46
                                                                                                                      24
         20                 48                46              33      27                  35                                               47
                                                                                                            18               25
   27             43              24                 38                         38
                                                                                                     40               37
         14                                                           19                                                                       2
                            8                 40              39                         15                 44                   9
   37              6              26                 35                        43                    16                7
                                                                                                                                           22
             7              17                44              29                         4                   6               42
                                                                      26
   11             34                  3                  5                                           20               34
                                                                                45                                                         21
             9              1                  30             32                                            10                   8
                                                                      49                  17
                  41              21                                                                                  41
   25                                                    2                      11                    23                                       5
                            22                19                                                                             30
         36                                                   31      48                  14                     36
   16             12              47                 28                         33                    39               31                 28


                      48 disks                                                                49 disks
m = 0.16938210954876                               101 bonds       m = 0.16738607686833                                     120 bonds


                  Figure 2.6: The densest packings found of 44 to 49 disks
                                                                                                                                      11



   25             49                  7                  19           37              24            8        28        49        19
        3                   50                 11              47           22
   29             39                  41                              30          46                     44                 5
                                                     34
        21                  35                                              17                  1                 47             32
                                               6               2
   32             14                                                  39          21                         4              29
                                      17             40
        5                                                                   38              20                    31             13
                                               28              36
                            30                                        36          35                     48                 45
   13             27                                     1
                                      26                                    50              41                    18
        46                                                     43                                                                15
                            38                  4                     43              2                  27
   9              20                                                                                                        51
                                      16                 33
        23                                                                  3               42                    40             25
                            31                 22                     16          14
   37             42                                           48                                        10                 11
                                      44                                    34
        24                                           15                                         9                 12             23
   45             18             8             12              10      6          26                     7                  33


                   50 disks                                                           51 disks
m = 0.16645462588286                                104 bonds       m = 0.16561837431260 99 bonds

   46             14                  8              52                38        49                     45        6         43
                                                                                           22                                    12
        47                  2                  23              5
                                                                            47                               34        7
   19             30                  36             32                           21
                                                                       3                        20                               16
        18                  51                 1               24                                                           14
                                                                            17                           28
   27             3                   41             16
                                                                      11          18        24                    50             41
        6                   44                 22              31
                                                                            48                           13                 15
   20             17                  45             25               42          54            9                 25             27
        12                  48                 37              42           40                                              52
                                                                                                         26
   28             10                  13             49               36          44            2                 39             51
        11                  38                 4               21           37                                              46
                                                                                                             1
   39             50                  29             43               29          10        31                    19             30
        7                   26                 9               40           5                            35                  4
   33             35                  15             34                8          23        33                    53             32


                   52 disks                                                           54 disks
m = 0.16538623796964 105 bonds                                      m = 0.15913951630719 115 bonds

   16        37                  39        7         2        19            21                  8                 33             31
                       46                                              7          35                     52                 16
        3                             10             49                     56              53                    45              6
   13         11            45                 26              50     49          48                     46                 51
        20                            41             31                     1                   3                 19             27
   52         44            34                 47              6      28          38                     37                 29
        51                            1              12                     36              50                    13             47
   43         27            28                 5               9      30          34                         9              23
        48                            35             25                     10              40                    39             15
   40             4         36                 15              22     32          26                     54                 42
        54                            33             42                     43              25                    41             17
   14         23            17                 53              32     20          12                         2               5
        55                            30             38                     55                  4                 18             24
   8          24            29                 21              18     11          22                     14                 44


                   55 disks                                                           56 disks
m = 0.15755574752972                                113 bonds       m = 0.15615650046215 119 bonds


 Figure 2.7: The densest packings found of 50 to 52, and 54 to 56 disks
                                                                                                                                                                                  12


                               2                     18                 23                27      30         2         19           57         11        40         33
              46
                                        32                    49                 45                                                                                          58
                      31                                                                               12        51           37          43        18
                                                     11                 57                20                                                                       59
             41                16
                                                              43                  1               13        46         10           26         29        15                   3
                      44                    50
                                                                        24                51                                                                       42
             14                10                     56                         39               27        24            6         52         48        53                  17
                      19                    4                      25
             15                                                                           28                                                                       28
                               29                         8                 33
                      47                    38                     9                 34           32        23         34            1         60        16                  20
             36                53                         6                 55                                                                                     39
                      3                     59                     22                     21      49        38         45            8         61        22                  21
             30                54                     26                         58                                                                                54
                      37                    5                           35                17      5          7         55           31         9         36                  56
                                                              52                 60                                                                                47
              48          13            7            12                 42                40      14        35            4         41         44        25                  50


                                    60 disks                                                                               61 disks
          m = 0.14950565404867                                              129 bonds          m = 0.14854412669518                                       121 bonds

             55                    57        58                        60        61       62            62                    52                9                  13        17
                      56                                  59                                      25                  6               23                 29
             47                    49        50                        52        53       54                71                28                60                 70
                      48                                  51                                      61                  54                 35               12                 66
               40                   42           43                44        45       46                57                      5              37                  10
                       41                                                                         21              22                  11                 53                  45
                                                          36                                                31                39                15                 14
             32                    34        35                        37        38       39
                      33                                                                          24                  58                 55               46                  7
                                                          28                                            20                    49               44                  38
             24                    26        27                        29        30       31
                      25                                                                          18              51                  48                 65                  19
                                                          20                                                41                36                68                 30
             16                    18        19                        21        22       23      32                  3                  50               47                 72
                      17
                                                      12                                                    1                 27                2                  63
                  9         10              11                     13        14       15          69              16                  59                  4                  43
                       2                                      5                                             42                34                40                 26
              1                    3             4                      6        7        8       56                  67                  8               33                 64


                      62 disks (3,7;2,5)                                                                                   72 disks
           m = 0.14569394327531 140 bonds                                                      m = 0.13549029317569 169 bonds
                      not the best packing                                                              not the best packing

                      16                32                        48             64               51        53        57        61        65        69        73        77
              8                24                    40                 56                72                                                                                 76
                                                                                                       55        59        63        67        71        75        78
                      15                31                        47             63
              7                23                    39                 55                71      7         14        21        28        35        42        49             72
                      14                30                        46             62                                                                                 74
              6                22                    38                 54                70      6         13        20        27        34        41        48             68
                      13                29                        45             61                                                                                 70
              5                21                    37                 53                69      5         12        19        26        33        40        47             64
                      12                28                        44             60                                                                                 66
              4                20                    36                 52                68      4         11        18        25        32        39        46             60
                      11                27                        43             59                                                                                 62
              3                19                    35                 51                67      3         10        17        24        31        38        45             56
                      10                26                        42             58                                                                                 58
              2                18                    34                 50                66      2         9         16        23        30        37        44             52
                      9                 25                        41             57                                                                                 54
              1                17                    33                 49                65      1         8         15        22        29        36        43             50


                                    72 disks                                                                               78 disks
           m = 0.13541666666667 152 bonds                                                      m = 0.12933240481510                                       155 bonds
                      not the best packing                                                              not the best packing


Figure 2.8: The densest packings found of 60 and 61 disks and inferior packings of 62, 72, and
78 disks
                                                                                                                            13




                                                                    3                             8
                        2                         1
                                                                                   5                             10


                                      5                             2                             7

                                                                                   4                             9

                        4                         3
                                                                    1                             6



                                 5 disks                                          10 disks
          m = 0.70710678118655                    12 bonds   m = 0.41666666666667                                21 bonds
                                                                             not the best packing


                                 2            9                     2              5                  9

                    7
                                                                                                                 12
                                                                             6               1
                                                      5
                                 6
                    3                                                                                            3
                                                                    7             10
                                          4
                                                                                                  11

                    8             1                   10        13                 4                             8


                                 10 disks                                         13 disks
            m = 0.42127954398390 21 bonds                    m = 0.36609600769643 25 bonds


                                                               59            25         57        1        75 65 54
                                                                        19        15
               4                      9                14
                                                               40            37         8             71 73
                                                                                             35                        43
                            3             10                            46        13                             53
                                                               24             3        72              5
                                                                                             78             39         60
                                                                        47        74
               5                      1                2       10            36        41             56          44
                                                                        9         66         30             45         67
                            13            16                   23             6        70             17          2
                                                                        42        16         49            22          21
               15                     7                17      77            50        34          48            61
                                                                        62        33        14             27          64
                            18            11                   55             7        69          76            11
                                                                        32        63         51            12          26
                                                               52            29        31          58             4
               6                     12                8
                                                                    38            18         68            20          28

                                 18 disks                                         78 disks
            m = 0.30046260628867 38 bonds                           m = 0.13046077259640
                                                                         not a rigid packing


Figure 2.9: The densest packings of 5, 10, 13, and 18 disks, an inferior packing of 10 disks,
and a challenger configuration of 78 disks
                                                                                                         14

3. Series of packings with similar patterns

n = k2 . The packings of this series have an obvious square pattern with disk diameter
m = 1/(k − 1). The pattern is optimal for n = 1, 4, 9, and 16, and probably 25 and 36. For
k1 = 7 this yields value of m = 1/6 which is smaller than the experimental diameter of the
challenger packing of 49 disks in Fig. 2.6.

n = k2 − 1 . The pattern can be viewed as a square of (k − 1)2 disks arranged in straight
rows and columns into which one row and one column of “shifted” disks are inserted. A
“shifted” row or column each has k − 1 disks. In the diagrams for k = 5 (n = 24, Fig. 2.1)
and k = 6 (n = 35, Fig. 2.4), the “straight” disks are shaded more heavily than the “shifted”
ones. Several equivalent packings are obtained by inserting the shifted row and column in
different places among the straight ones. A pair of insertion position (i, j), 2 ≤ i, j ≤ k − 1,
identifies the packing, e.g., in packing of 24 disks (2,3) (Fig. 2.1), the shifted row is the second
and the shifted column is the third (counting from the top left corner). Among the (k − 2)2
packings thus obtained, there are many congruent pairs. The pattern is fully developed at
n = 8 (one packing) and remains optimal for n = 15 (one packing), n = 24 (three equivalent
packings), and n = n0 = 35 (three equivalent packings). For n1 = 48 the pattern looses its
optimality, which can be shown as follows. The angle at the center of disk 13 in packing (2,2)
of 24 disks q(see Fig. 2.1 ) in the triangle formed by centers of disks 13, 19 and 3 is 15o with
                   √
cos 15o = .5 2 + 3. Similar angles are the same in all the packings of the series which easily
                          q       √
implies m = 1/(k − 3 + 2 + 3). For k1 = 7 this yields value of m = 0.168581424 which is
smaller than the experimental diameter of the challenger packing of 48 disks in Fig. 2.6.

n = k2 − 2 . This pattern is similar to the pattern of series k2 − 1, only here there are two
shifted rows and two shifted columns. The (non-optimal) packing of 62 disks depicted in Fig.
2.8, shows this pattern for k = 8. There are (k − 3)(k − 4)/2 possible ways to insert a pair of
shifted rows (i1 , i2 ) because of the restrictions 1 < i1 < i2 < k and similarly for the columns
(j1 , j2 ). Hence, there are ((k − 3)(k − 4)/2)2 possible different index sets (i1 , i2 ; j1 , j2 ) for each
of which we can construct an equivalent packing. Many of these are congruent. The pattern
is fully developed at k = 5 (n = 23, one packing) and remains optimal for q              only one more
                                                                                                  √
value k = k0 = 6 (n0 = 34, four equivalent packings.). Here m = 1/(k − 5 + 2 2 + 3). For
k = k1 = 7 this yields value m = 0.1705406887 which is smaller than that of the challenger
packing of n1 = 47 disks in Fig. 2.6.

n = k2 − 3 . This pattern is represented by conjectured dense packings of 22, 33, 46, and
61 disks (Figs. 2.1, 2.3, 2.6, 2.8). A feature of the pattern is a (shaded more heavily on
the pictures) densely packed “straight” square of (k − 3)3 disks in the bottom left corner. It
follows that the pattern is not optimal for k ≥ 10 (n ≥ 97) because the “straight” square
itself isn’t. However, even for a smaller n = n1 = 78 we were able to get a disk configuration
                                                                                                15

that challenges the pattern as presented in Fig. 2.8, although this configuration is a not fully
formed solid disk packing (see Fig. 2.9).
    Looking at the (non-optimal) packing of 78 disks (see Fig. 2.8), the pattern can be further
described as three alternating columns at the right and three alternating rows at the top with
one rattler at the top right corner. In each of the three additional rows and the three additional
columns, most disks are not touching each other. The exceptions are pairs 42-49 in the bottom
additional row, 73-77 in the top additional row and 76-72 in the right additional column (Fig.
2.8). Also there is almost full contact for pairs of disks between adjacent additional rows
and columns, except for the pair 42-75 which are not touching between the first and second
additional rows. These features are identical in all the packings of the pattern.
    Each such packing can be obtained by “tightening” a certain configuration C described as
follows: In C, disks 77 and 76 are not touching each other but all disks in additional rows
and columns are touching their neighbors. (C is not a solid packing.) We take C as an initial
condition for the “billiards” packing algorithm [L], [LS]. To “tighten” the configuration, the
“billiards” algorithm allows the disks to move chaotically in the square without overlaps while
their diameter increases at a common rate until no further growth is possible. It is remarkable,
that for each n = k2 − 3, k = 5, 6, 7, 8 and 9, this chaotic negotiation always converges
(independently of the initial velocities) to the described pattern with parameter m identical to
double precision in all runs involving the same n. Moreover, when instead of the configuration
C, we start with a random initial configuration and zero initial diameters of the disks, the
same configuration with the same precision results in the runs that achieve the largest m, -
but only for k = 5, 6, 7 and 8, excluding value k = 9. Also, for k = 4 (n = 13) which seems
to be the smallest n for which the pattern may exist, both methods, the one beginning with a
zero-diameter random configuration and the one beginning with the configuration C, lead to
the same packing which, however, deviates somewhat from the described pattern, see Fig. 2.9

n = k(k + 1) . The pattern consists of k + 1 alternating columns with k disks each, see, e.g.,
the packing of 30 disks in Fig. 2.2. Following the path of disks 2, 12, 6, 18, 3, 29 in this
packing, we come to the expression k cos α for the horizontal side of the square that contains
the disk centers, where the angle α = α(k) is that at the vertex 2 in the triangle 12, 2, 6. The
vertical side of the square is k − 1 + sin α, where the latter expression results from the path 12,
2, 5, 30, 24, 7. Equating these two expressions for the side we determine from the resulting
                                  √
equation: cos α(k) = (k2 − k + 2k)/(k2 + 1) and m = (k cos α(k))−1 .
    Looking again at the packing of 30 disks in Fig. 2.2, circles 1 and 2 are separated by a
                                                             √
non-negative distance because α(k) ≤ 30o or cos α(k) ≥ 3/2 for k = 5. The latter inequality
holds and the pattern exists as a solid packing of non overlapping disks only for k ≥ 4, i.e., for
n = 20, 30, 42, 56, 72,....
    We show that the packing of the pattern is not optimal for n ≥ n1 = 72 as follows. We
present another regular pattern of packings of k(k + 1) disks; for k = 8 this alternative pattern
is depicted in the second row and second column in Fig. 2.8 (with one rattler). The alternative
                                                                                              16

pattern exists for all values of n for which the main pattern exists. The diameter m̄ = m̄(k)
                                                                                   √
of a disk in the alternative pattern is given by m̄(k) = 1/((k + 1/2) cos β(k) + ( 3/2) sin β(k))
where (in the example in Fig. 2.8) β(k) for k = 8 is the angle at disk 56 in the triangle 67, 56,
42. As before, we equate the horizontal and vertical sides of the square: k cos β +cos(β +π/3) =
(k − 1) sin(β + π/3) + sin β. From this equation we easily determine β = β(k) and then we
find that m̄ > m for all n ≥ n1 = 72 (but m̄ < m for n = 20, 30, 42, and 56). Note that the
alternative packing, although it is better than the packing of the pattern for n = 72 disks, is
not optimal. For example, for 72 disks we found experimentally a disk configuration with an
irregular structure (not shown) that is better than both the main or the alternative pattern.

n = k2 + ⌊k/2⌋ . The pattern, as exemplified by cases k = 5 (n = 27, Fig. 2.2) and k = 6
(n = 39, Fig. 2.5), consists of k + 1 alternating columns, odd columns having k disks each and
even columns having k − 1 disks each. As before, with α denoting the angle, say, at disk 15 in
the triangle 7, 15, 10 in the packing of 27 disks in Fig. 2.2, we compute the side-length of the
square obtained in two different ways: k cos α = 2(k − 1) sin α. From this equation we easily
determine cos α(k) and then m = 1/(k cos α(k)). The pattern exists when, as in the example
of 27 disks (Fig. 2.2), disks 12 and 13 are separated by a non-negative distance. This occurs
when sin α(k) ≥ 1/2. Thus, the pattern exists only for k = 2, 3, 4, 5, 6, and 7 (n = 5, 10, 18,
27, 39, and 52) and those packings (shown in Figs 2.9, 2.2, 2.5, and 2.8) are, indeed, optimal,
except the case of n = 10: proved [GMPW] for n = 5, 10, 18 and conjectured for n = 27, 39,
and 52.
    For k ≥ 8 the “ideal” pattern yields overlaps in pairs of disks. The overlap increases with
k. For k = 8 (n = 68) the overlap is less than 1% of the disk diameter so it is naturally to
expect that the optimal packing will be a small deviation from the main pattern. Experiments,
indeed show that best configurations are of this sort. Unfortunately, none of them is a solid
packing, because it becomes very difficult to find exactly in which pairs the disks are touching,
and not merely just very close to each other.

References

[CFG]      H. T. Croft, K. J. Falconer and R. K. Guy, Unsolved Problems in Geometry, Springer
           Verlag, Berlin, 1991, 107–111.

[GMPW] C. de Groot, M. Monagan, R. Peikert, and D. Wurtz, Packing circles in a square:
       a review and new results, in System Modeling and Optimization (Proc. 15th IFIP
       Conf. Zurich 1991), 45–54.

[FG]       J. H. Folkman and R. L. Graham, A packing inequality for compact convex subsets
           of the plane, Canad. Math. Bull. 12 (1969), 745–752.
                                                                                         17

[GL1]    R. L. Graham and B. D. Lubachevsky, Dense packings of equal disks in an equilateral
         triangle: from 22 to 34 and beyond, The Electronic Journ. of Combinatorics 2
         (1995), #A1.

[GLNO]   R. L. Graham, B. D. Lubachevsky, K. J. Nurmela, and P. R. J. Östergård, Packing
         congruent circles in a circle by stochastic optimization methods, (In preparation.)

[G]      M. Goldberg, The packing of equal circles in a square, Math. Mag. 43 (1970), 24–30.

[L]      B. D. Lubachevsky, How to simulate billiards and similar systems, J. Computational
         Physics 94 (1991), 255–283.

[LG1]    B. D. Lubachevsky and R. L. Graham, Dense packings of 3k(k+1)+1 equal disks in
         a circle for k = 1,2,3,4, and 5 (Submitted for publication.)

[LS]     B. D. Lubachevsky and F. H. Stillinger, Geometric properties of random disk pack-
         ings, J. Statistical Physics 60 (1990), 561–583.

[MFP]    C. D. Maranas, C. A. Floudas, P. M. Pardalos, New results in the packing of equal
         circles in a square, Discrete Mathematics 142 (1995), 287–293.

[NO]     K. J. Nurmela and P. R. J. Östergård, Packing up to 50 equal circles in a square,
         Discrete & Computational Geometry, submitted.

[O]      N. Oler, A finite packing problem, Canad. Math. Bull. 4 (1961), 153–155.

[Sch]    J. Schaer, On the packing of ten equal circles in a square, Math. Mag. 44 (1971),
         139–140.

[Schl]   K. Schlüter, Kreispackung in Quadraten, Elem. Math. 34 (1979), 12–14.

[Val]    G. Valette, A better packing of ten circles in a square, Discrete Math. 76 (1989),
         57–59.
