Volume 23 (2023)

Homology of configuration spaces
of hard squares in a rectangle

HANNAH ALPERT
ULRICH BAUER
MATTHEW KAHLE
ROBERT MACPHERSON
KELLY SPENDLOVE

ATGAlgebraic&GeometricTopologymspmsp

Algebraic & Geometric Topology 23:6 (2023) 2593–2626
DOI: 10.2140/agt.2023.23.2593
Published: 7 September 2023

Homology of configuration spaces
of hard squares in a rectangle

HANNAH ALPERT
ULRICH BAUER
MATTHEW KAHLE
ROBERT MACPHERSON
KELLY SPENDLOVE

We study ordered configuration spaces C.nI p; q/ of n hard squares in a p (cid:2) q
rectangle, a generalization of the well-known “15 puzzle”. Our main interest is in
the topology of these spaces. Our first result describes a cubical cell complex and
proves that it is homotopy equivalent to the configuration space. We then focus on
determining for which n, j , p, and q the homology group Hj ŒC.nI p; q/(cid:141) is nontrivial.
We prove three homology-vanishing theorems, based on discrete Morse theory on
the cell complex. Then we describe several explicit families of nontrivial cycles,
and a method for interpolating between parameters to fill in most of the picture for
“large-scale” nontrivial homology.

55R80; 57Q70, 82B26

1 Introduction

We study the ordered configuration space of n squares in a p (cid:2) q rectangle, which we
denote by C.nI p; q/. The case n D 15 and p D q D 4 corresponds to the famous “15
puzzle”. This puzzle was apparently invented by Noyes Palmer Chapman, a postmaster
in Canastota, New York, in 1874; see Sonneveld and Slocum [12]. Already by 1879, the
puzzle had been analyzed mathematically by Johnson and Story [10]. They showed that
it is not possible, for example, for any sequence of moves to transpose the pieces labeled
14 and 15. Their observation is really a topological one, namely that the configuration
space has two connected components.

A natural discrete model for the 15 puzzle is the graph G15, which we describe as
follows. The vertices are the aligned positions of the puzzle, corresponding to the 16!

© 2023 MSP (Mathematical Sciences Publishers). Distributed under the Creative Commons Attribution
License 4.0 (CC BY). Open Access made possible by subscribing institutions via Subscribe to Open.

2594

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

permutations of the 15 pieces and the one hole, and we have an edge between every
pair of positions that differ by sliding a piece into the hole.

If we allow arbitrary positions for nonoverlapping squares, then the configuration space
for the 15 puzzle is more than 1–dimensional; for instance, there is a three-parameter
family of ways to slide horizontally the three pieces in the bottom row. Nevertheless, as
a special case of our results here, the configuration space of the 15 puzzle deformation
retracts to a one-dimensional subspace homeomorphic to G15.

Having a cell complex structure allows for computing many topological invariants
directly. For example, the Betti number ˇ1 can be computed by counting the number
of 0–cells f0 D 16! and 1–cells f1 D 24 (cid:1) 15! of G15, using the fact that ˇ0 D 2, and
applying the 1–dimensional Euler formula f0 (cid:0) f1 D ˇ0 (cid:0) ˇ1.
In the more general setting, we describe a cubical complex X.nI p; q/ and show it is
always a deformation retract of the configuration space C.nI p; q/. Applying discrete
Morse theory on this complex allows us to establish some necessary conditions on
where nontrivial homology can appear.
In the following, we always assume that p; q (cid:21) 1, 0 (cid:20) n (cid:20) pq, and j (cid:21) 0. We also
sometimes use a “large-scale” parametrization, by defining x D n=pq and y D j =pq.
The quantity x has a physical interpretation as “density”, describing the area ratio in
the rectangular region that is occupied by squares.

Theorem 1.1 (homology vanishing theorem) We have:

(1)

(2)

If j > pq (cid:0) n, then Hj ŒC.nI p; q/(cid:141) D 0.
If j > n, then Hj ŒC.nI p; q/(cid:141) D 0.
If j > pq=3, then Hj ŒC.nI p; q/(cid:141) D 0.

(3)
Equivalently, on the large scale, if Hj ŒC.nI p; q/(cid:141) ¤ 0 then y (cid:20) min˚1 (cid:0) x; x; 1

(cid:9).

3

The cubical cell complex model allows us to do exact computations for small examples.
We include a table of Betti numbers in Section 7. Based in part on our computations,
we conjecture the following.

Conjecture 1.2 If Hj ŒC.nI p; q/(cid:141) ¤ 0, then

n
pq (cid:0) n; n (cid:0) 8n2
j (cid:20) min
9pq

; pq
4

o
:

Equivalently, we conjecture that if Hj ŒC.nI p; q/(cid:141) ¤ 0, then

y (cid:20) min

n
1 (cid:0) x; x (cid:0) 8
9

x2; 1
4

o

:

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2595

In Section 6, we describe several families of explicit nontrivial cycles, and a method for
interpolating between parameters. We almost show that if y (cid:20) min˚1 (cid:0) x; x (cid:0) 8
(cid:9)
9 x2; 1
4
there exist n, j , p, and q such that Hj ŒC.nI p; q/(cid:141) ¤ 0. Instead we prove an analogous
statement with a piecewise linear approximation of the parabola y D x (cid:0) 8
9 x2. Let S
be the set of points on the parabola defined by
(cid:19) ˇ
ˇ x D 3
ˇ
4k
(cid:1) 2 S. Let I be the closed interval

x; x (cid:0) 8
9

; k (cid:21) 1

S D

(cid:26)(cid:18)

x2

(cid:27)

:

(cid:1) 2 S and (cid:0) 3
8

; 1
4

Note that (cid:0) 3
4

; 1
4

I D f.x; y/ j 0 (cid:20) x (cid:20) 1 and y D 0g:

If .x; y/ is any rational
Theorem 1.3 (large-scale homology nonvanishing theorem)
point in the convex hull of S [ I , then there exist n, p, q, and j such that x D n=pq,
y D j =pq, and Hj ŒC.nI p; q/(cid:141) ¤ 0.

Theorem 1.3 might suggest the right necessary conditions for nontrivial homology,
rather than Conjecture 1.2. We do not currently know of any instance of n, j , p, and
q where Hj ŒC.nI p; q/(cid:141) ¤ 0 and .x; y/ lies outside of the convex hull of S [ I .

A summary of our main results is illustrated in Figure 1. Although we have made some
headway, completely resolving the following question is left as future work.

Question 1.4 What are necessary and sufficient conditions on .nI j I p; q/ for

Hj ŒC.nI p; q/(cid:141) ¤ 0?

; 3
16

We note that Conjecture 1.2 is only about necessary conditions for nontrivial homology,
but at the moment we do not have a good conjecture for necessary and sufficient
conditions. The conditions in Conjecture 1.2 by themselves are not sufficient. For
example, (cid:0) 1
(cid:1) is a point in the blue region of Figure 1, corresponding to n D p D q D 4
4
and j D 3. However, it is not true that we have homology whenever n=pq D 1
4 and
j =pq D 3
16 , even when n is arbitrarily large. Suppose that p D 2 and q D 8k for
some k (cid:21) 1, and n D 4k; then we cannot get nontrivial homology with j D 3k.
The largest j where we will see nontrivial homology is j D 2k; by the homotopy
equivalence mentioned below, this follows from Theorem 1.2(3) in Alpert, Kahle, and
MacPherson [2].

In recent years, there has been increased interest in similar kinds of configuration
spaces; see Alpert [1], Baryshnikov, Bubenik, and Kahle [3], and Carlsson, Gorham,
Kahle, and Mason [6] for some earlier work on configuration spaces of disks. Plachta

Algebraic & Geometric Topology, Volume 23 (2023)

2596

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

y D 1 (cid:0) x

y D x

q
p
=
j
D
y

y D 1
3

y D 1
4

y D x (cid:0) 8

9 x2

x D n=pq

Figure 1: A summary of our main results. The axes are x D n=pq and
y D j =pq. We show that if .x; y/ is outside the shaded region bounded by
y D 1 (cid:0) x, y D x, and y D 1
3 , then Hj ŒC.nI p; q/(cid:141) D 0. We show conversely
that for every rational point .x; y/ in the blue part of the shaded region, there
exist n, j , p, and q such that x D n=pq, y D j =pq, and Hj ŒC.nI p; q/(cid:141) ¤ 0.
Each of the blue dots represents a point .x; y/ where we computed that
Hj ŒC.nI p; q/(cid:141) ¤ 0, with n (cid:20) 6.

recently studied configuration spaces of squares in a rectangle [11], using affine Morse–
Bott theory, smooth flows, and graphs associated with such configurations. As one
application, he showed that under certain conditions the configuration space which
we denote by C.nI p; q/ is connected. We note that our dimensions of the rectangle,
p and q, are always positive integers, but he studies the more general framework where
they may be positive real numbers.

What we study here is closely related to the recent paper [2] on configuration spaces of
hard disks in an infinite strip, which we now briefly discuss. Let config.n; w/ denote
the configuration space of n disks of unit diameter in an infinite strip of width w. While
we do not prove it here, it is not hard to check that C.nI p; q/ is homotopy equivalent
to config.n; w/ if q (cid:21) n and p D w. So the configuration spaces of hard squares in a
rectangle we study here are a generalization of the configuration spaces of hard disks
in an infinite strip.

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2597

Motivated by the notion of phase transitions for hard-spheres systems, definitions are
suggested in [2] for homological solid, liquid, and gas regimes. The definitions apply
here as well.
Let Conf.nI R2/ denote the (ordered) configuration space of points in the plane. We
say that .nI j I p; q/ is

(cid:15) in the homological solid regime if

Hj ŒC.nI p; q/(cid:141) D 0;

(cid:15) in the homological gas regime if the inclusion map i W C.nI p; q/ ! Conf.nI R2/

induces an isomorphism on homology

i(cid:3) W Hj ŒC.nI p; q/(cid:141) ! Hj ŒConf.nI R2/(cid:141); and

(cid:15) in the homological liquid regime otherwise.

We are mainly concerned with the boundary between trivial and nontrivial homology,
ie separating the solid regime from liquid and gas.
It will also be interesting to
better understand the boundary between the homological liquid and gas regimes, as
summarized in the following question.

Question 1.5 What are necessary and sufficient conditions on .nI j I p; q/ for the
inclusion map i W C.nI p; q/ ! Conf.nI R2/ to induce an isomorphism on homology
i(cid:3) W Hj ŒC.nI p; q/(cid:141) ! Hj ŒConf.nI R2/(cid:141)?

Acknowledgments

Alpert was supported by NSF-DMS 1802914 during work on this project. Bauer
gratefully acknowledges support from the German Research Foundation (DFG) through
the Collaborative Research Center SFB/TRR 109 Discretization in geometry and
dynamics. Kahle gratefully acknowledges the support of NSF-DMS 2005630, NSF-
DMS 1839358, and NSF-CCF 1839358. Spendlove was partially supported by the NSF
Graduate Research Fellowship Program under grant DGE-1842213 and by EPSRC
grant EP/R018472/1.

2 Definitions and notation

The configuration space C.nI p; q/ of n unit squares in a p (cid:2) q rectangle can be written
as a subspace of R2n by keeping track of the coordinates of the centers of the squares.
(cid:3) in R2. Accordingly,
We select our p (cid:2) q rectangle to be the set (cid:2) 1
2

; p C 1
2

; q C 1
2

(cid:3) (cid:2) (cid:2) 1
2

Algebraic & Geometric Topology, Volume 23 (2023)

2598

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

we define C.nI p; q/ to be the set of all points .x1; y1; : : : ; xn; yn/ 2 R2n such that

(cid:15) 1 (cid:20) xk (cid:20) p and 1 (cid:20) yk (cid:20) q for all 1 (cid:20) k (cid:20) n, and
(cid:15) jxk (cid:0) x`j (cid:21) 1 or jyk (cid:0) y`j (cid:21) 1 for all 1 (cid:20) k < ` (cid:20) n.

Note that the boundaries of the unit squares can intersect each other or the edges of the
rectangle.

; 1
2

We will be working with two ways to draw a grid on the rectangle; these two grids can be
thought of as dual to each other, or as offset by (cid:0) 1
(cid:1). One grid is the integer coordinate
2
grid. The set of possible positions of the center of one square is Œ1; p(cid:141) (cid:2) Œ1; q(cid:141), which
we can think of as having vertices at the points where both coordinates are integers,
edges between vertices at distance 1, and .p (cid:0) 1/.q (cid:0) 1/ square 2–cells. We refer to
these integer points as coordinate grid vertices, to the edges as coordinate grid edges,
and to the squares as coordinate grid squares. Together we refer to the coordinate grid
vertices, edges, and squares as coordinate grid cells.

The other grid is the p (cid:2) q grid on the rectangle itself. Thinking of the rectangle as a
p (cid:2)q chessboard, we refer to the unit square centered at each coordinate grid vertex as a
board square. For each coordinate grid cell, there is a corresponding rectangle of board
squares given by taking the union of all unit squares for which the center lies on that
coordinate grid cell, as shown in Figure 2. The rectangle corresponding to a coordinate
grid vertex is a single board square, the rectangle corresponding to a coordinate grid
edge is a pair of adjacent board squares, and the rectangle corresponding to a coordinate
grid square is a 2 (cid:2) 2 rectangle of board squares.

Let G.nI p; q/ be the space .Œ1; p(cid:141) (cid:2) Œ1; q(cid:141)/n with its standard cubical complex structure.
Here the letter G stands for grid. We can think of this space as the set of configurations
of labeled squares in the rectangle where the squares are allowed to overlap. As a

Figure 2: The coordinate grid vertices, at points with integer coordinates, are
the centers of the board squares. Here a coordinate grid edge is shown with
its corresponding rectangular piece.

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2599

Figure 3: An illustration of the cell complex X.2I 2; 2/. The vertices of the
complex are labeled by their corresponding configurations with integer coor-
dinates. Note that in this simple case, the cell complex X.2I 2; 2/ equals the
configuration space C.2I 2; 2/, while in general the cell complex X.nI p; q/
is only a subspace of the configuration space C.nI p; q/.

cubical complex, each cell of G.nI p; q/ corresponds to an n–tuple in which each
entry is a coordinate grid cell. We can draw the cell of G.nI p; q/ by drawing the n
corresponding rectangles of board squares. We refer to such a picture as a rectangle
arrangement, and we refer to the n rectangles as pieces in the arrangement. Any list
of n rectangles of board squares of sizes 1 (cid:2) 1, 1 (cid:2) 2, 2 (cid:2) 1, and 2 (cid:2) 2 is the rectangle
arrangement of some cell of G.nI p; q/.

We define X.nI p; q/ to be the subcomplex of G.nI p; q/ consisting of all cells of
G.nI p; q/ that are fully contained in C.nI p; q/. Here the letter X stands for complex,

Figure 4: Any configuration where no two squares touch the same board
square is in the cell of X.nI p; q/ corresponding to the rectangle arrangement
that shows which board squares each square touches.

Algebraic & Geometric Topology, Volume 23 (2023)

2600

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

because X.nI p; q/ is the main cell complex that we work with throughout the paper. It
is quick to check that X.nI p; q/ is equal to the set of cells in which the corresponding
rectangle arrangement has none of its pieces overlapping. Given a configuration in
C.nI p; q/, we can check whether it is in X.nI p; q/ by looking at each unit square in
the configuration and drawing the rectangle of board squares that it intersects, as shown
in Figure 4. If these rectangles are disjoint, then the configuration is in X.nI p; q/, and
it is in the cell corresponding to the rectangular arrangement that we have just drawn.

3 Homotopy equivalence of the configuration space and

complex

The ambient cubical complex G.nI p; q/ has three kinds of cells: some cells are
fully contained in C.nI p; q/ and together form X.nI p; q/, some cells are partially in
C.nI p; q/, and some cells are disjoint from C.nI p; q/. We will define a deformation
retraction from C.nI p; q/ to X.nI p; q/ by considering the cells of G.nI p; q/ that are
partially in C.nI p; q/ one at a time. To do this, we define local coordinates on each
of these cells and give a criterion in those local coordinates for which points are in
C.nI p; q/ and which points are not.
.bxcCdxe/. In other words, we have
We define a function snapW R ! R by snap.x/ D 1
2
snap.k/ D k for all k 2 Z, and if x 2 .k; kC1/, then snap.x/ D kC 1
2 . We can also define
snapW Rd ! Rd for any dimension d, by applying snap to each coordinate separately.
If z D .x1; y1; : : : ; xn; yn/ 2 R2n is a point in the complex G.nI p; q/, then snap.z/
is the barycenter of the unique cubical cell of G.nI p; q/ whose interior contains z.
Geometrically, if .xi; yi/ is the center of a unit square, then snap.xi; yi/ is the center
of the corresponding rectangle of the board squares that it touches. Note that snap
is idempotent, snap.snap.z// D snap.z/, and z is a barycenter of some grid cell in
G.nI p; q/ if and only if z D snap.z/.

3.1 Containment of cells in the configuration space

We can check whether a given cell of G.nI p; q/ has empty intersection with C.nI p; q/
by looking at pairs of pieces, case by case, in its corresponding rectangle arrangement.
Figure 5 shows which pairs of pieces prevent a cell from having any configurations in
C.nI p; q/; in each case, the barycenter of the corresponding cell is not a configuration
in C.nI p; q/. For each pair of pieces, there is no way to fit a unit square in the interior
of each piece while keeping the two unit squares disjoint. (Two unit squares can fit if

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2601

Figure 5: If the unit squares at the centers of the rectangular pieces overlap,
then the corresponding cell in G.nI p; q/ does not contain any configurations
in C.nI p; q/. The darker gray indicates where the two pieces overlap, and
the black dots give the centers of the pieces.

they touch the boundaries of the rectangles, but the resulting configuration is in the
boundary of the specified open cell, not inside it.)

Figure 6 shows the four remaining ways for two pieces in a rectangle arrangement to
overlap; for these, the corresponding cell is partially in C.nI p; q/, and the barycenter is
a configuration in C.nI p; q/. The following lemma summarizes how to check whether
a given cell of G.nI p; q/ is partially in C.nI p; q/.

Lemma 3.1 Let z D snap.z/ D .x1; y1; : : : ; xn; yn/ 2 G.nI p; q/ be the barycenter of
an open cell (cid:27) of G.nI p; q/. Then:

(1) (cid:27) has a nonempty intersection with C.nI p; q/ if and only if its barycenter z lies
in the configuration space C.nI p; q/, or equivalently, the `1 distance between
.x`; y`/ and .xk; yk/ is at least 1 for all 1 (cid:20) k < ` (cid:20) n:

max.jx` (cid:0) xkj ; jy` (cid:0) ykj/ (cid:21) 1:
(2) (cid:27) is fully contained in C.nI p; q/, and hence a cell of X.nI p; q/, if and only if ,
for all 1 (cid:20) k < ` (cid:20) n, the corresponding pieces do not overlap, or equivalently,

bmax.xk; x`/c > dmin.xk; x`/e

or

bmax.yk; y`/c > dmin.yk; y`/e:

Figure 6: If a given cell of G.nI p; q/ is partially contained in C.nI p; q/, then
some pair of overlapping pieces in the rectangle arrangement must overlap in
one of the four ways shown. The darker gray indicates where the two pieces
overlap, and the black dots give the centers of the pieces.

Algebraic & Geometric Topology, Volume 23 (2023)

2602

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

Proof To check the first claim, we observe that if any point z 2 (cid:27) is in C.nI p; q/,
then snap.z/ 2 C.nI p; q/ as well. This is because for any x1; x2 2 R, if x2 (cid:0) x1 (cid:21) 1,
then snap.x2/ (cid:0) snap.x1/ (cid:21) 1 as well.
For the second statement, note that piece k covers the board squares with centers
in Œbxkc; dxke(cid:141) (cid:2) Œbykc; dyke(cid:141), and piece ` covers the board squares with centers
in Œbx`c; dx`e(cid:141) (cid:2) Œby`c; dy`e(cid:141). The two pieces overlap if and only if the intervals
Œbxkc; dxke(cid:141) and Œbx`c; dx`e(cid:141) overlap and the intervals Œbykc; dyke(cid:141) and Œby`c; dy`e(cid:141)
also overlap.

We say that a subcomplex of a regular CW complex is a full subcomplex if it is maximal
with respect to its vertex set.

Corollary 3.2 The complex X.nI p; q/ is a full subcomplex of the ambient cubical
complex G.nI p; q/.

An equivalent description for when an open cell (cid:27) is partially in C.nI p; q/ can be
obtained from examining the cases in Figure 6. Let b D .i1; j1; : : : ; in; jn/ 2 G.nI p; q/
be the barycenter of (cid:27), and note that the coordinates ik and jk are half-integers. Then
(cid:27) is partially in C.nI p; q/ if and only if

(1)

(2)

for all k and ` we have max.ji` (cid:0) ikj ; jj` (cid:0) jkj/ (cid:21) 1, and
there is a pair k; ` such that
(a)
(b)
(c)

ji` (cid:0) ikj D 1 and jj` (cid:0) jkj < 1, and ik and i` are not integers, or
jj` (cid:0) jkj D 1 and ji` (cid:0) ikj < 1, and jk and j` are not integers, or
ji` (cid:0) ikj D jj` (cid:0) jkj D 1 and none of ik, i`, jk, and j` are integers.

3.2 Membership in the configuration space using local coordinates

(cid:1)2n

; 1
2

. Not every point in (cid:0)(cid:0) 1
2

The next lemma specifies how to use local coordinates to check, for an open cell
partially in C.nI p; q/, whether a given point in the cell is in C.nI p; q/. Given an open
cell (cid:27) of G.nI p; q/, we can specify the points z 2 (cid:27) in terms of the local coordinates
z (cid:0) snap.z/ 2 (cid:0)(cid:0) 1
corresponds to a point in
2
the cell, because for each coordinate of the barycenter snap.z/ that is an integer, the
corresponding coordinate in z (cid:0) snap.z/ is zero.
Let b be the barycenter of cell (cid:27), and let I.(cid:27)/ be the set of indices of noninteger coor-
(cid:1)I.(cid:27)/
dinates of b. The number of elements of I.(cid:27)/ is the dimension of (cid:27) . Let (cid:0)(cid:0) 1
2
denote the coordinate subspace of (cid:0)(cid:0) 1
given by letting the I.(cid:27)/ coordinates vary
; 1
2
2
and requiring the remaining coordinates (corresponding to the integer coordinates in b)
to be zero. We have z 2 (cid:27) if and only if z (cid:0)b 2 (cid:0)(cid:0) 1
, in which case b D snap.z/.
2

(cid:1)I.(cid:27)/

; 1
2

; 1
2

; 1
2

(cid:1)2n

(cid:1)2n

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2603

A point of G.nI p; q/ is in C.nI p; q/ if and only if no two of the n specified squares
intersect. Thus, we check the local coordinates for two of the n squares at a time to see
whether those two squares overlap.

Lemma 3.3 Let (cid:27) be an open cell of G.2I p; q/ that is partially in C.2I p; q/, and let
z D .x1; y1; x2; y2/ be a point in the interior of (cid:27) . Then .x1; y1; x2; y2/ 2 C.2I p; q/
if and only if one of the following conditions holds:

(cid:15) jsnap.x2/ (cid:0) snap.x1/j D 1 and .x2 (cid:0) snap.x2// (cid:0) .x1 (cid:0) snap.x1// is zero or has

the same sign as snap.x2/ (cid:0) snap.x1/, or

(cid:15) jsnap.y2/ (cid:0) snap.y1/j D 1 and .y2 (cid:0) snap.y2// (cid:0) .y1 (cid:0) snap.y1// is zero or has

the same sign as snap.y2/ (cid:0) snap.y1/.

In the fourth case in Figure 6, where the two pieces are 2 (cid:2) 2 rectangles intersecting
at one board square, either condition in the lemma may hold, so the intersection of
C.nI p; q/ with the cell of G.2I p; q/ is the union of solutions to two linear inequalities.
In the other three cases, the centers of the two pieces have only one coordinate that
differs by 1, so the intersection of C.nI p; q/ with the cell is the set of solutions to one
linear inequality.

Proof A point .x1; y1; x2; y2/ is in C.2I p; q/ if and only if either jx2 (cid:0) x1j (cid:21) 1
or jy2 (cid:0) y1j (cid:21) 1. Note that the function snap is weakly order-preserving, meaning
that x2 (cid:0) x1 (cid:21) 0 implies snap.x2/ (cid:0) snap.x1/ (cid:21) 0. Thus, by symmetry of x1 and x2
as well as .x1; x2/ and .y1; y2/, it suffices to show that x2 (cid:0) x1 (cid:21) 1 if and only if
both snap.x2/ (cid:0) snap.x1/ D 1 and .x2 (cid:0) snap.x2// (cid:0) .x1 (cid:0) snap.x1// (cid:21) 0. The latter
condition straightforwardly implies the former.
Conversely, x2(cid:0)x1 (cid:21) 1 clearly implies snap.x2/(cid:0)snap.x1/ (cid:21) 1. Further, the assumption
that (cid:27) is only partially in C.2I p; q/ rules out the case snap.x2/ (cid:0) snap.x1/ > 1, as in
this case we would necessarily have bsnap.x2/c > dsnap.x1/e, and Lemma 3.1 would
imply that (cid:27) is fully contained in C.2I p; q/. Thus we get snap.x2/ (cid:0) snap.x1/ D 1
and .x2 (cid:0) snap.x2// (cid:0) .x1 (cid:0) snap.x1// (cid:21) 0 as desired.

3.3 Construction of the deformation retraction

The next lemma gives the main step in constructing the deformation retraction from
C.nI p; q/ to X.nI p; q/.

Lemma 3.4 Let (cid:27) be an open cell of G.nI p; q/ that is partially in C.nI p; q/. Then
we have that @(cid:27) \ C.nI p; q/ is a deformation retract of (cid:27) \ C.nI p; q/.

Algebraic & Geometric Topology, Volume 23 (2023)

2604

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

Proof Let z D .x1; y1; : : : ; xn; yn/ be a point in the open cell (cid:27). If we want to
check whether z is in C.nI p; q/, then Lemma 3.3 gives a set of inequalities on the
local coordinates z (cid:0) snap.z/ D .u1; v1; : : : ; un; vn/ within the open cell (cid:27) that we can
evaluate. For each pair of pieces k; ` in the rectangle arrangement for (cid:27) , the lemma
specifies zero, one, or two inequalities of the form

(cid:15) uk (cid:21) u` or uk (cid:20) u`,
(cid:15) vk (cid:21) v` or vk (cid:20) v`.

The case of zero inequalities comes from the case where the two rectangular pieces do
not intersect. The case of one inequality comes from the case where they intersect in
one of the first three ways shown in Figure 6. And, the case of two inequalities comes
from the fourth case in Figure 6, where the pieces are both 2 (cid:2) 2 squares and they have
one board square in common; in this case, the local coordinate z (cid:0) snap.z/ needs to
satisfy either or both of the two inequalities. Together, we refer to the inequalities
from the lemma as the inequalities associated to (cid:27). Note that the above inequalities are
stated for local coordinates, but at the same time, the coordinates of the barycenter

b D .i1; j1; : : : ; in; jn/

satisfy the same set of inequalities, even strictly. This property will be crucial for our
argument.

(cid:1)2n

; 1
2

We define the deformation retraction as follows. Let (cid:21) be large enough that .1=(cid:21)/b is
in (cid:0)(cid:0) 1
; we can take (cid:21) D 2.p C q/. Let m be the coordinate projection of .1=(cid:21)/b
; 1
2
2
(cid:1)I.(cid:27)/
onto (cid:0)(cid:0) 1
, that is, for each integer coordinate of b, we set the corresponding
2
coordinate of m to be zero. Since m is a positively scaled version of b, it inherits
the magical quality of satisfying all of the inequalities associated to (cid:27) , and since b
satisfies all those inequalities strictly, (cid:0)m has the magical quality of violating all of the
inequalities associated to (cid:27) . (Note that every coordinate appearing in the inequalities
associated to (cid:27) is in I.(cid:27)/.) Thus the point b C m in (cid:27) is in the configuration space
C.nI p; q/, while the point b (cid:0) m is not.

The deformation retraction now pushes every point z 2 (cid:27) outward along a ray from
b (cid:0) m until it hits @(cid:27). In other words, the vector from b (cid:0) m to z is given by z (cid:0) b C m,
so as time t increases from 0, we set

zt D z C t.z (cid:0) b C m/;
until we reach the maximum t for which z C t.z (cid:0) b C m/ is in (cid:27) , and then the
point no longer moves. Formally, we can define Tz to be the positive value such that

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2605

z C Tz.z (cid:0) b C m/ 2 @(cid:27) . (Because (cid:27) is a cube and hence star-shaped around any
interior point, for any point in (cid:27) and any nonzero vector within (cid:27) starting at that point,
there is a unique nonnegative multiple of that vector that reaches @(cid:27).) If d is the
distance within (cid:27) from b (cid:0) m to C.nI p; q/, then the vector z (cid:0) b C m from b (cid:0) m
to z has length at least d, and any vector from z to @(cid:27) has length at most diam.(cid:27)/, so
Tz (cid:20) .1=d/ diam.(cid:27)/ (cid:20) 2n=d .

Using this notation, the deformation retraction is defined as

F W (cid:27) \ C.nI p; q/ (cid:2)

i

! (cid:27) \ C.nI p; q/;

h
0; 2n
d
.z; t/ 7! z C min.t; Tz/.z (cid:0) b C m/:

We still need to check that if z 2 C.nI p; q/, then zt 2 C.nI p; q/ for all t, in order to
ensure that the homotopy remains in (cid:27) \ C.nI p; q/. This is equivalent to checking that

zt (cid:0) b D .z (cid:0) b/ C t.z (cid:0) b C m/ D .1 C t/.z (cid:0) b/ C tm

satisfies a sufficient collection of the inequalities associated to (cid:27). We claim that
zt (cid:0) b satisfies every one of the inequalities that z (cid:0) b satisfies; since this collection
of inequalities is sufficient for z to be in C.nI p; q/, it is also sufficient for zt to be in
C.nI p; q/. Indeed, the inequalities are linear with no constant term, so given two points
satisfying the inequalities, any linear combination of them with positive coefficients
also satisfies the inequalities. Because z (cid:0) b satisfies a sufficient set of inequalities and
m satisfies all of the inequalities associated to (cid:27), this implies that .1 C t/.z (cid:0) b/ C tm
also satisfies the same set of inequalities as z (cid:0) b. Thus, zt is in C.nI p; q/ for every
t (cid:20) Tz, and the map F that we have defined is indeed a deformation retraction from
(cid:27) \ C.nI p; q/ to @(cid:27) \ C.nI p; q/.

Putting all the cells together, we obtain a deformation retraction from C.nI p; q/ to
X.nI p; q/.

Theorem 3.5 The subcomplex X.nI p; q/ is a deformation retract of the configuration
space C.nI p; q/.

Proof Order the cells (cid:27) of G.nI p; q/ that are partially in C.nI p; q/ so that their
dimensions are nonincreasing. Then, cell by cell in order, we use Lemma 3.4 to
obtain a deformation retraction from (cid:27) \ C.nI p; q/ to @(cid:27) \ C.nI p; q/. Concatenating
these deformation retractions gives a deformation retraction from C.nI p; q/ to the set
X.nI p; q/ of cells completely contained in C.nI p; q/.

Algebraic & Geometric Topology, Volume 23 (2023)

2606

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

4 Discrete Morse theory

In this section, we describe a discrete gradient vector field on X.nI p; q/, in the sense
of Forman’s discrete Morse theory [7], and characterize its critical cells. The analysis
of which cells are critical is based on what we call the apex of a cell. The apex of a
cell, as shown in Figure 7, is the 0–dimensional face that is obtained by replacing each
piece by its upper-right corner square — in particular, the apex of any 0–dimensional
cell is that 0–cell itself. We use discrete Morse theory to collapse our cell complex so
that among the cells remaining, at most one cell has any given apex.

Theorem 4.1 There is a discrete gradient vector field on X.nI p; q/ with the properties:

(1) Every matched pair consists of two cells with the same apex.

(2) Among the cells with a given apex, at most one cell is critical (unmatched ).

(3) The matching is Sn–equivariant: if cells e1 and e2 are a matched pair, and we
apply the same permutation to the labels in the rectangle arrangements of e1
and e2, then the two resulting cells are also a matched pair.

The proof relies on constructing what we call the apex graph, which facilitates the
enumeration of all the cells with a given apex. In Lemmas 4.2 and 4.3 we prove the
basic properties of the apex graph, and in Lemma 4.4 we define the matching for
Theorem 4.1 in the language of the apex graph. After that, it is straightforward to finish
the proof of Theorem 4.1.

Given any rectangle arrangement, we describe the locations of the pieces according to
the coordinates of their upper-right corner squares, so we say that a piece is at .i; j / if

Figure 7: The apex of a rectangle arrangement replaces each piece by its
upper-right corner. The correspondence does not depend on the labels of the
pieces, so the labels are not shown.

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2607

Figure 8: To find the apex graph, we place one vertex for each direction that
a piece in the apex can extend, and draw edges between directions where the
pieces cannot extend simultaneously.

its upper-right corner is in column i (from left to right) and row j (from bottom to top)
of our p (cid:2) q rectangle. (Alternatively, the center of the upper-right board square has
coordinates .i; j / in the plane.) Giving the coordinates of each piece is the same as
specifying the apex of our cell. To distinguish cells with the same apex, we need to
specify, for each piece, whether it has height 1 or 2 and whether it has width 1 or 2. Not
all these possibilities give rise to valid rectangle arrangements, because some pieces
may overlap or hang off the board. For each possible apex, we construct the apex graph
to record these possible conflicts, as shown in Figure 8.

The apex graph has at most two vertices per piece. If our apex has a piece at .i; j /,
then we let (cid:0)i (cid:0) 1
; j (cid:1) — the center of the left edge of the .i; j / board square — be a
2
vertex of the apex graph if and only if the piece at .i; j / can have width 2 in some cell
with that apex, that is, if i > 1 and there is no piece at .i (cid:0) 1; j /. Similarly, we let
(cid:1) — the center of the lower edge of the .i; j / board square — be a vertex if
(cid:0)i; j (cid:0) 1
2
and only if there is a piece at .i; j /, we have j > 1, and there is no piece at .i; j (cid:0) 1/.

The edges of the apex graph record which of the width 2 or height 2 options would
conflict with each other. A piece at .i; j / can have width 2 or height 2 but not both
when there are no pieces at .i (cid:0) 1; j / and .i; j (cid:0) 1/, but there is a piece at .i (cid:0) 1; j (cid:0) 1/.
In this case we draw an edge between the vertices (cid:0)i (cid:0) 1
/. The other
2
possible conflict is between pieces at .i; j / and .i (cid:0) 1; j C 1/. If there is no piece at
.i (cid:0) 1; j /, then the .i; j / piece may have width 2, and the .i (cid:0) 1; j C 1/ piece may have
height 2, but not both simultaneously. In this case we draw an edge between (cid:0)i (cid:0) 1
; j (cid:1)
2
(cid:1). These two types of edges give all the edges in the apex graph.
and (cid:0)i (cid:0) 1; j C 1
2

; j (cid:1) and .i; j (cid:0) 1
2

Lemma 4.2 Each apex graph is a disjoint union of path graphs.

Algebraic & Geometric Topology, Volume 23 (2023)

2608

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

Figure 9: Cells with a given apex correspond to independent sets in the apex
graph; we select the vertices corresponding to the directions where the apex
pieces extend. Here, the vertices in the independent set are drawn filled, and
the other vertices are drawn empty.

Proof The two types of edges have the same slope and length when drawn on the
coordinate lattice. Any graph that can be drawn in this way is a disjoint union of paths.
Note that some of the paths may be single vertices.

Lemma 4.3 The set of cells with a given apex is in bijection with the set of independent
sets in its apex graph. One cell is a face of another if and only if the independent set
corresponding to the first cell under this bijection is a subset of the independent set
corresponding to the second cell.

Proof For a cell with a given apex, we find the corresponding subset of vertices in the
apex graph by considering each piece in the associated rectangle arrangement, say at
(cid:1)
; j (cid:1) if the piece has width 2, and selecting vertex (cid:0)i; j (cid:0) 1
.i; j /, selecting vertex (cid:0)i (cid:0) 1
2
2
if it has height 2, as in Figure 9. The construction guarantees that these are in fact
vertices of the apex graph and that no two of them share an edge.

For the converse, suppose that we have an independent set in the apex graph. We
select our pieces to have width 2 and/or height 2 according to which vertices are in
the independent set, and we want to check whether the pieces overlap or hang off the
board. Consider the .i; j / piece. It cannot hang off the board or overlap with a piece at
.i (cid:0) 1; j / or .i; j (cid:0) 1/, because the vertices corresponding to those possibilities are not
in the apex graph. It cannot overlap with a piece at .i (cid:0) 1; j (cid:0) 1/ because that would
mean choosing both vertices (cid:0)i (cid:0) 1
(cid:1), which would be adjacent. And,
; j (cid:1) and (cid:0)i; j (cid:0) 1
2
2
it cannot overlap with a piece at .i (cid:0) 1; j C 1/, because that would mean choosing both
vertices (cid:0)i (cid:0) 1
(cid:1), which would be adjacent. Symmetrically, by
2
swapping the roles of the two pieces, we see that the piece at .i; j / also cannot overlap

; j (cid:1) and (cid:0)i (cid:0) 1; j C 1
2

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2609

with the pieces at .i C 1; j /, .i; j C 1/, .i C 1; j C 1/, or .i C 1; j (cid:0) 1/. This exhausts
all the possibilities for how two pieces of width and height at most 2 might overlap,
and shows that we have a bijection.

For the second property, suppose that cells e and f have the same apex. Then f is a
face of e if and only if every piece of width 2 in f also has width 2 in e, and every
piece of height 2 in f also has height 2 in e. This is equivalent to the condition that the
independent set corresponding to f is a subset of the independent set corresponding
to e.

Thinking of the cells as independent sets in the apex graph suggests how to think about
pairing them up. The dimension of a cell is equal to the number of vertices in the
independent set corresponding to that cell. So, if cells e and f have the same apex,
then f is a face of e with dim f D dim e (cid:0) 1 if and only if the independent set of f is
a subset of the independent set of e and the two sets differ by one vertex. When two
independent sets differ by one vertex, we say that they are adjacent.

Lemma 4.4 Given a disjoint union of paths, there is a matching on the set of indepen-
dent sets such that every matched pair of independent sets are adjacent and at most one
independent set is unmatched.

Proof We start by proving the statement for one connected path of k vertices. We
express the independent sets as binary strings of length k with no consecutive 1’s,
so that 0 indicates that the vertex in that position is not part of the independent set,
and 1 indicates that the vertex is part of the independent set. The matching is defined
recursively. For k D 1 the strings are 0 and 1, which we match as a pair. For k D 2 the
strings are 00, 01, and 10; we match 00 with 10 and leave 01 unmatched. For k > 2,
each string begins with 00, 10, or 010. We match the strings beginning with 00 to the
strings beginning with 10 such that each matched pair differs only in the first bit. Then,
for the strings beginning with 010 we ignore the first three bits and use the matching
for the k (cid:0) 3 case.

The result is that for k (cid:17) 1 mod 3 all strings are matched, for k (cid:17) 0 mod 3 the only
unmatched string consists of repeating copies of 010, and for k (cid:17) 2 mod 3 the only
unmatched string consists of repeating copies of 010 followed by 01 at the end. This
proves the lemma for the case of one path.

For several disjoint paths, we select some ordering on them. Given an independent
set, if its restriction to each path agrees with the unmatched independent set from

Algebraic & Geometric Topology, Volume 23 (2023)

2610

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

0 1 0 0 1

0 1 0 0 1

0 1 0 0 0 1 0

0 1 0 1 0 1 0

Figure 10: Given an independent set on a disjoint union of paths, to find
its match we select the first component that is not critical, ignore any 010
prefixes, and flip the first bit of the remainder.

the one-path case, we leave it unmatched. Otherwise, we find the first path P where
this is not true. To find the matching independent set, we keep all the other paths as
they are and alter the set on P to be the matching set from the one-path case, as in
Figure 10. There is an unmatched independent set if and only if none of the paths has
1 mod 3 vertices, and in this case the unmatched set corresponds to repeating 010 on
each path.

To finish the proof of Theorem 4.1, we need to check that the matching we have just
defined determines a discrete gradient vector field with the properties we are looking for.

Proof of Theorem 4.1 The discrete vector field is defined as follows. Given a cell,
we find its apex and the apex graph. Encoding the original rectangle arrangement as
an independent set in the apex graph (Lemma 4.3), we find the matching independent
set (Lemma 4.4) if there is one, and decode to get another cell with the same apex.
Properties (1) and (3) are automatic from the construction, and Property (2) is a
consequence of Lemma 4.4.

We still need to check that the discrete vector field is gradient. We want to show that
there does not exist a cycle of cells e1; f1; e2; f2; : : : ; er ; fr ; er C1 D e1 such that every
ei and fi are a matched pair (where, in particular, ei is a face of fi), and every fi is a
face of eiC1 with dim fi D dim eiC1 (cid:0) 1. We observe that because fi is a face of eiC1,
if the apex of eiC1 is not equal to the apex of fi, then it differs by moving some piece
one square left or down. Every pair ei and fi have the same apex, so as the sequence
continues, the apex keeps moving leftward and downward, making it impossible to
have a cycle unless all cells in it have the same apex.

Thus we may assume that the cells e1; f1; : : : ; er ; fr all have the same apex. We can
encode these cells as independent sets in the apex graph. To go from e1 to f1, we
delete one vertex v from the independent set of e1, and to go from f1 to e2, we add
one vertex w to the independent set of f1. Remembering the ordering of the paths and

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2611

e1

. . .

f1

. . .

e2

. . .

v

v w

. . .

. . .

w

. . .

Figure 11: In a sequence of cells with the same apex, alternating between two
consecutive dimensions, with consecutive pairs alternating between matched
and incident, the corresponding independent sets look more and more like the
unmatched set, and thus cannot cycle.

vertices in the apex graph, we observe that up until v, the independent set for f1 agrees
with the unmatched independent set, so any added vertices there would destroy the
property of being an independent set. Thus w cannot be at or before v. If the vertex
immediately after v is on the same path, then w can be that vertex. But w cannot be
anywhere else after v, because if so, then the matching independent set to e2, which
we have supposed is f2, would have v added rather than a vertex subtracted — it would
have the wrong dimension — giving a contradiction unless w is immediately after v.
Thus we cannot have a cycle e1; f1; : : : ; er ; fr ; er C1 D e1, because each successive
item agrees more and more with the unmatched set, as in Figure 11: the independent
set of e1 agrees before v, the independent set of f1 agrees through v, the independent
set of e2 agrees through w, and so on. So, our discrete vector field is gradient and has
all three desired properties.

We prove one last theorem in this section, which helps with assessing the dimension of
critical cells in the following section. For the following, we divide each unit square in
the p (cid:2) q grid into two half-squares by drawing a diagonal line from the upper-right to
the lower-left corner.

Theorem 4.5 There is a function r that assigns a set of half-squares to each vertex of
the apex graph , with the properties:

(1) For any vertex v, the set r .v/ has four half-squares if v is the only vertex of
a path , three half-squares if v is the first or last vertex of a path , and two
half-squares otherwise.

(2) The sets r .v/ are disjoint for all v.

Algebraic & Geometric Topology, Volume 23 (2023)

2612

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

Figure 12: Each vertex is assigned the two half-squares it touches. If vertex v
has neighbors in both directions, then r .v/ contains only these two half-squares.

Proof Recalling that we can draw each vertex of the apex graph as the midpoint of an
edge between a square occupied by an apex piece and an unoccupied square, we set
r .v/ to contain both of the half-squares that v touches, as in Figure 12.

We think of the vertices as ordered first by the sum of coordinates and then by the
column coordinate, so that the ordering starts in the lower-left corner and goes right
and down along diagonals. If v is the first or last vertex of a path, we need to find
another half-square to add to r .v/. There are several cases, shown in Figure 13:

(1)

(2)

(3)

(4)

(5)

If v is the first vertex of a path and is on a vertical edge, we add in the remainder
of the square to the left of v.
If v is the last vertex of a path and is on a horizontal edge, we add in the remainder
of the square below v.
If v is the first vertex of a path and is on a horizontal edge and there is no vertex on
the preceding (above-left) edge, we add in the remainder of the square above v.
If v is the last vertex of a path and is on a vertical edge and there is no vertex
on the following (below-right) edge, we add in the remainder of the square to
the right of v.
If v is the first vertex of a path and is on a horizontal edge and there is a
(nonadjacent) vertex on the preceding edge, we add the half-square to the left
of the square below v.

Figure 13: For the first vertex of a path, rules (1), (3), and (5) specify how
to add a third half-square; the (cid:2) symbol indicates an absence of vertex. The
third picture also shows an instance of rule (6). For the last vertex of a path,
rules (2), (4), and (6) are analogous.

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2613

Figure 14: If the only vertex of a path is on a vertical edge, rules (1) and (4)
or rules (1) and (6) assign four half-squares to that vertex. If the vertex is on
a horizontal edge, rules (2) and (3) or rules (2) and (5) are analogous.

(6)

If v is the last vertex of a path and is on a vertical edge and there is a (nonadjacent)
vertex on the following edge, we add the half-square below the square to the left
of v.

In the case where v is the only vertex of the path, if v is on a vertical edge, then either
rules (1) and (4) or rules (1) and (6) apply, as shown in Figure 14, and if v is on a
horizontal edge, then either rules (2) and (3) or rules (2) and (5) apply, so that r .v/ has
four half-squares in total. This completes the definition of r .v/.

We need to check that no half-square has been assigned twice. To do this, we consider
the assignment from the point of view of each square. Consider a square that is occupied
by a piece in the apex arrangement. It may have vertices on its left or lower edges. If
it has both vertices, then half of the square is assigned to each vertex. If it has one
vertex, then all of the square is assigned to that vertex, by rule (3) or rule (4). If it has
no vertex, then none of the rules assign that square to any vertex.

Similarly, consider a square that is unoccupied in the apex arrangement. It may have
vertices on its right or upper edges. If it has both vertices, then half of the square
is assigned to each vertex. If it has one vertex, then all of the square is assigned to
that vertex, by rule (1) or rule (2). (Note that rules (1) and (2) cannot apply to an
unoccupied square with both vertices, because in this case the two vertices would
be adjacent.) If our unoccupied square has no vertices, then we divide the square in
half. The lower-right half gets assigned by rule (5) to the same vertex (if any) as the
half-square to its right, and the upper-left half gets assigned by rule (6) to the same
vertex (if any) as the half-square above it.

In each case, only one rule can apply to each half-square, so each half-square can be
assigned to only one vertex.

Algebraic & Geometric Topology, Volume 23 (2023)

2614

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

5 Homology-vanishing theorems

The existence of the cell complex X.nI p; q/ and the discrete gradient on it allow us to
establish a number of homology-vanishing results.

Theorem 5.1 If j > pq (cid:0) n, then Hj ŒC.nI p; q/(cid:141) D 0.

Proof This is almost immediate from the homotopy equivalence C.nIp; q/ (cid:24)X.nIp; q/.
Consider the dimensions of the cells in X.nI p; q/. A cell is indexed by a collection of
n nonoverlapping rectangular pieces in a p (cid:2) q grid. A 1 (cid:2) 1 piece contributes 0 to the
dimension of the cell, a 1 (cid:2) 2 or 2 (cid:2) 1 piece contributes 1, and a 2 (cid:2) 2 piece contributes
2. The total area of the pieces is at most pq. So the largest dimension of a cell is at
most pq (cid:0) n. By the definition of cellular homology, there is no homology above the
dimension of the cell complex itself, so Hj ŒC.nI p; q/(cid:141) D 0 for j > pq (cid:0) n.

Theorem 5.2 If j > n, then Hj ŒC.nI p; q/(cid:141) D 0.

Proof This follows from the properties of the discrete gradient described in Section 4.
Every cell is indexed by a collection of nonoverlapping rectangular pieces, and each
piece is one of 1 (cid:2) 1, 1 (cid:2) 2, 2 (cid:2) 1, or 2 (cid:2) 2. The analysis of the gradient shows that there
are no critical cells indexed by a collection of pieces including a 2 (cid:2) 2 piece. (When
such a cell is encoded as an independent set in the apex graph as in Lemma 4.3, the
2 (cid:2) 2 piece corresponds to two vertices of the independent set that are consecutive but
not adjacent. However, the proof of Lemma 4.4 implies that in a critical cell, the first
vertex of each path is never part of the corresponding independent set.) Hence the
dimension of a critical cell is at most n.

Theorem 5.3 If j > 1

3 pq, then Hj ŒC.nI p; q/(cid:141) D 0.

3 k vertices in the first case, and has 1

Proof This follows from Theorem 4.5. A critical cell corresponds to an independent set
that on each path looks like 010 : : : 010 or 010 : : : 01 depending on whether the number
of vertices in the path is 0 or 2 mod 3. The dimension of the critical cell is the number
of vertices in the independent set. If the path has k vertices, then the independent set
has 1
3
For a path of k vertices, the theorem allocates half-squares with a total area of k C 1 to
.k C 1/
the vertices of the path. The independent set for that path contributes at most 1
3
to the dimension of the critical cell. Thus, in total, the dimension of the critical cell
is at most one third of the total area allocated to all the paths in the apex graph, and
thus is at most 1

.k C 1/ vertices in the second case.

3 pq.

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2615

Putting together Theorems 5.1, 5.2, and 5.3, we have proved Theorem 1.1.

Theorem 1.1 (homology vanishing theorem) We have:

(1)

(2)

If j > pq (cid:0) n, then Hj ŒC.nI p; q/(cid:141) D 0.
If j > n, then Hj ŒC.nI p; q/(cid:141) D 0.
If j > pq=3, then Hj ŒC.nI p; q/(cid:141) D 0.

(3)
Equivalently, on the large scale, if Hj ŒC.nI p; q/(cid:141) ¤ 0 then y (cid:20) min˚1 (cid:0) x; x; 1

(cid:9).

3

6 Nontrivial homology

In this section, our main aim is to prove Theorem 1.3. We give several explicit con-
structions of nontrivial cycles, and then a method for interpolating between parameters.

Lemma 6.1 The points (cid:0) 1
2

; 1
4

(cid:1) and (cid:0) 3
4

; 1
4

(cid:1) are attainable.

Proof Figure 15 shows a cycle in H1ŒC.2I 2; 2/(cid:141). More precisely, the figure illustrates
a piecewise-linear map i W S 1 ! C.2I 2; 2/, where we linearly interpolate at constant
speed between the positions shown. Then if Œ(cid:27)(cid:141) is a generator of H1.S 1/, the cycle we
are describing is the image i(cid:3).Œ(cid:27)(cid:141)/.

To show that this cycle is nontrivial, consider the map f W C.2I 2; 2/ ! S 1, where one
takes the angle the line from the center of square 1 to the center of square 2 makes

Figure 15: A nontrivial cycle in H1ŒC.2I 2; 2/(cid:141). This realizes the point
.x; y/ D (cid:0) 1

(cid:1).

; 1
4

2

Algebraic & Geometric Topology, Volume 23 (2023)

2616

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

Figure 16: A nontrivial cycle in H1ŒC.3I 2; 2/(cid:141). This realizes the point
.x; y/ D (cid:0) 3

(cid:1).

; 1
4

4

with the x–axis. In other words, define

.x2 (cid:0) x1; y2 (cid:0) y1/:

f .x1; y1; x2; y2/ D

1
p.x2 (cid:0) x1/2 C .y2 (cid:0) y1/2
The composition f ı i is a degree-one map S 1 ! S 1, and in particular the induced
map .f ı i /(cid:3) is an isomorphism on H1. So then i must be injective on H1.
Similarly, Figure 16 shows a cycle in H1ŒC.3I 2; 2/(cid:141). The figure illustrates a piecewise-
linear map i W S 1 ! C.3I 2; 2/, and the cycle we are interested in is the image. This also
represents a nontrivial cycle in H1ŒC.3I 2; 2/(cid:141). Indeed, we have a natural projection
map to C.2I 2; 2/ where one forgets the coordinates of the third square, and then the
argument above shows that the image of the cycle is still nontrivial in this projection.

The following lemma will be superseded later in this section by a stronger result, but we
present the lemma and proof as a warmup, and we will also reuse the main construction
in its proof later.

Lemma 6.2 The point

.x; y/ D

is attainable for every k (cid:21) 1.

(cid:19)

(cid:18) k
k2

; k (cid:0) 1
k2

D

(cid:19)

(cid:18) 1
k

; 1
k

(cid:0) 1
k2

Proof Consider first Figure 17. We illustrate a 2 (cid:2) 2 square and a 1 (cid:2) 1 square orbiting
each other in a 3 (cid:2) 3 grid, as in Figure 15. We can then put two 1 (cid:2) 1 squares inside the

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2617

Figure 17: A 2 (cid:2) 2 square and a 1 (cid:2) 1 square orbiting each other in a 3 (cid:2) 3 grid.

2 (cid:2) 2 square, and these can orbit each other independently. So, together these motions
describe a map i W T 2 ! C.3I 3; 3/. This map is illustrated in Figures 18 and 19. By
induction, we can embed a .k(cid:0)1/–dimensional torus realizing a nontrivial cycle in
C.kI k; k/ for every k (cid:21) 2.

The same argument as before gives that this represents a nontrivial class in H2ŒC.3I 3; 3/(cid:141).
Indeed, compose with a map f W C.3I 3; 3/ ! T 2 D S 1 (cid:2) S 1 which assigns to the first
coordinate the angle between the line segment from the center of square 1 to the center
of square 2 and the x–axis. Similarly, the map assigns to the second coordinate the
angle between the line segment from the center of square 1 to the center of square 3
and the x–axis. This is a degree-one map T 2 ! T 2. The induced map .f ı i /(cid:3) is an
isomorphism on homology, and so i(cid:3) is injective.

Figure 18: A map T 2 ! C.3I 3; 3/. The light gray and dark gray squares
orbit each other inside the blue 2 (cid:2) 2 square as in Figure 15, while the black
and blue squares orbit each other independently as in Figure 17.

Algebraic & Geometric Topology, Volume 23 (2023)

2618

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

Figure 19: Another view of the map i W T 2 ! C.3I 3; 3/ visualized in
Figure 18. The image of the fundamental class of the torus is a nontrivial
cycle in H2ŒC.3I 3; 3/(cid:141).

By Lemma 6.2, there are infinitely many points realized on the parabola y D x (cid:0) x2.
The following lemma improves on that result, showing that there are infinitely many
points realized on the parabola y D x (cid:0) 8
9 x2.

Lemma 6.3 The point

is attainable for every k (cid:21) 1.

.x; y/ D

(cid:18) 3
4k

; 3
4k

(cid:0) 1
2k2

(cid:19)

Proof The case k D 1 is already covered by Lemma 6.1. For any k (cid:21) 2, we can
embed a .k(cid:0)1/–dimensional torus in C.kI k; k/. Now consider the configuration space
C.3kI 2k; 2k/. We can divide the 2k (cid:2) 2k grid into four k (cid:2) k grids. Inside each, we
use k squares to embed a .k(cid:0)1/–torus as in the proof of Lemma 6.2. This describes
a .3k(cid:0)3/–torus, and the three k (cid:2) k squares can orbit each other in the 2k (cid:2) 2k grid,
giving one more dimension. So putting it all together, we have a .3k(cid:0)2/–torus. This

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2619

Figure 20: A map T 4 ! C.6I 4; 4/. The three pairs of squares orbit each
other in three 2 (cid:2) 2 squares, and these three 2 (cid:2) 2 squares orbit each other in
the 4 (cid:2) 4 square, as in Figure 16. The image of this map gives a nontrivial
cycle in H4ŒC.6I 4; 4/(cid:141), realizing the point .x; y/ D (cid:0) 3

(cid:1).

; 1
4

8

realizes the point

; 3k (cid:0) 2
4k2
The case k D 2 is illustrated in Figure 20, and the case k D 3 in Figure 21.

(cid:0) 1
2k2

.x; y/ D

; 3
4k

(cid:18) 3k
4k2

(cid:18) 3
4k

(cid:19)
:

D

(cid:19)

Lemma 6.4 The point .x; 0/ is attainable for every rational x with 0 (cid:20) x (cid:20) 1.

Indeed, suppose x is a rational point in Œ0; 1(cid:141), and write x D a=b, where a is
Proof
a nonnegative integer, b is a positive integer, and a (cid:20) b. Set n D ab and p D q D b.
By assumption, we have a (cid:20) b, so n (cid:20) pq and the configuration space C.nI p; q/ is
nonempty, so H0ŒC.nI p; q/(cid:141) ¤ 0.

Finally, we show that we can rationally interpolate between all the points we have
described. Let S be the set of points
(cid:26)(cid:18) 3
4k

(cid:19) ˇ
ˇ k (cid:21) 1
ˇ

(cid:0) 1
2k2

; 3
4k

S D

(cid:27)
:

Figure 21: A map T 7 ! C.9I 6; 6/, realizing the point .x; y/ D (cid:0) 1

4

; 7
36

(cid:1).

Algebraic & Geometric Topology, Volume 23 (2023)

2620

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

Let I be the closed interval

I D f.x; y/ j 0 (cid:20) x (cid:20) 1 and y (cid:21) 0g:

If .x; y/ is any rational
Theorem 1.3 (large-scale homology nonvanishing theorem)
point in the convex hull of S [ I , then there exist n, p, q, and j such that x D n=pq,
y D j =pq, and Hj ŒC.nI p; q/(cid:141) ¤ 0.

Proof By Cartheodory’s theorem, if .r1; r2/ is in the convex hull of S [ I , then
.r1; r2/ is in the convex hull of three points of S [ I . Write .r1; r2/ as a rational convex
combination of these three points, ie

.r1; r2/ D (cid:21)1.u1; v1/ C (cid:21)2.u2; v2/ C (cid:21)3.u3; v3/

with

.u1; v1/; .u2; v2/; .u3; v3/ 2 S [ I ,

(1)
(2) 0 (cid:20) (cid:21)1; (cid:21)2; (cid:21)3 (cid:20) 1 with (cid:21)1 C (cid:21)2 C (cid:21)3 D 1, and
(3) (cid:21)1; (cid:21)2; (cid:21)3 all rational.

By the previous lemmas, .ui; vi/ is realizable as a nontrivial homology class for hard
squares in a square for i D 1; 2; 3. Let ni, pi, and ji be such that ui D ni=p2
i and
vi D ji=p2

i for i D 1; 2; 3. Let (cid:21)i D ai=bi for i D 1; 2; 3. Set

then let

P D p1p2p3; B D b1b2b3; R D PB;

N D r1R2

and J D r2R2:

If we can find a nontrivial class in

HJ ŒC.N I R; R/(cid:141);

we are done.
Partition the R (cid:2) R square into B2 smaller squares, each of dimension P (cid:2) P . In a (cid:21)1
3 of them), we realize .u1; v1/
fraction of these smaller squares (ie in (cid:21)1B2 D a1b1b2
as follows. Further partition each P (cid:2) P square into p2
3 squares, of dimension
p1 (cid:2) p1. In each of these squares, we can place n1 squares and can then describe a
ŒC.n1I p1; p1/(cid:141). So in total, we place
map from a torus giving a nontrivial class in Hj1

2p2

2b2

.a1b1b2

2b2
3

/.p2

2p2
3

/n1 D .(cid:21)1B2/

(cid:18) P 2
p2
1

(cid:19)

n1 D (cid:21)1

(cid:19)

(cid:18) n1
p2
1

.P 2B2/ D (cid:21)1u1R2

squares, and get a map from the torus of dimension

.a1b1b2

2b2
3

/.p2

2p2
3

/j1 D .(cid:21)1B2/

(cid:18) P 2
p2
1

(cid:19)

j1 D (cid:21)1

(cid:19)

(cid:18) j1
p2
1

.P 2B2/ D (cid:21)1v1R2:

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2621

Similarly, in a (cid:21)2 fraction of these P (cid:2) P squares we can realize .u2; v2/ by dividing
3 smaller squares of dimension p2 (cid:2) p2, and in a (cid:21)3 fraction of the P (cid:2) P
up into p2
squares we realize .u3; v3/.

1p2

Altogether, we have used

(cid:21)1u1R2 C (cid:21)2u2R2 C (cid:21)3u3R2 D r1R2 D N

squares, and defined an embedded torus of dimension

(cid:21)1v1R2 C (cid:21)2v2R2 C (cid:21)3v3R2 D r2R2 D J:

This describes a cycle in

HJ ŒC.N I P; P /(cid:141);
as desired. The cycle is nontrivial as before — we can compose with a map to T j such
that the composed map T j ! T j has degree one.

7 Betti number computations for small n; p; q

We compute the Betti numbers ˇj ŒC.nI p; q/(cid:141) for n (cid:20) 6 and p (cid:20) q (cid:20) n. These are
provided in Table 1. Another view of the Betti numbers for n D 6 and j D 2 with p
and q varying is illustrated in Figure 22. Finally, in Table 2 we record information
about the size of the complex X.nI p; q/ in the form of its f –vector .f0; f1; f2; : : : /,
where fi is the number of i–dimensional cells in X.nI p; q/. All of our computations
are using coefficients in the prime field Z=2Z.

For our computations we employ three different software packages, and we dedicate
a small section to each one. The first is a Python/Sage Jupyter notebook which
uses the discrete Morse vector field of Section 4. The second is a branch of the
pyCHomP package, available at [9] specifically for computing the Betti numbers for
these configuration spaces. The third is the DIPHA package with a custom script to
build the configuration cell complex. Finally, note that in the case when n D q the
configuration space C.nI p; q/ is homotopy equivalent to the configuration space of
disks in a strip addressed in [2]; in this case, one can use the Salvetti complex to
compute the Betti numbers as done in [2].

7.1 Discrete Morse theory Sage notebook

Using the discrete gradient vector field from Section 4, we compute the collapsed
Morse chain complex for X.nI p; q/ as follows. The idea is first to find the critical

Algebraic & Geometric Topology, Volume 23 (2023)

2622

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

n p q

ˇ0

ˇ1

ˇ2

ˇ3

ˇ4 ˇ5

2 2 2
3 2 2
3 2 3
3 3 3
4 2 2
4 2 3
4 2 4
4 3 3
4 3 4
4 4 4
5 2 3
5 2 4
5 2 5
5 3 3
5 3 4
5 3 5
5 4 4
5 4 5
5 5 5
6 2 3
6 2 4
6 2 5
6 2 6
6 3 3
6 3 4
6 3 5
6 3 6
6 4 4
6 4 5
6 4 6
6 5 5
6 5 6
6 6 6

1
2
1
1
24
1
1
1
1
1
2
1
1
1
1
1
1
1
1
720
1
1
1
1
1
1
1
1
1
1
1
1
1

0
0
0
2
0
0
6
11
29
11
0
40
110
67
249
169
71
35
35
0
80

0
0
0
0
0
0
0
0
0
6
0
0
0
0
0
40
62
146
50
0
0
0
90
0
0

0
1
2
0
7
0
0
3
0
0
49
0
31
0
12
0
0
6
0
6
122
0
161
0
111
0
68
0
0
10
0
10
0
10
0
10
24
10
0
0
2241
0
351 1790
0
351 1160
0
457
458
0
2174
0
15
714 1429
0
15
80
780
714
15
457
441
30
15
1541 30
85
15
1066 275
85
15
465 394
85
15
225 875
85
15
225
85
15

0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
274 120

Table 1: The Betti numbers of C.nI p; q/ for 2 (cid:20) n (cid:20) 6. The homological
liquid regime is indicated in bold.

cells and then to compute their boundaries in the Morse complex. However, it turns
out that most of this process depends very little on p and q. Thus, in order to compute
for various p and q without duplicating effort, we first compute the Morse complex for
X.nI n; n/. The Morse complex of each X.nI p; q/ for 1 (cid:20) p and q (cid:20) n turns out to be a
subcomplex of the Morse complex for X.nI n; n/, obtained by selecting only the critical
cells for which the apex is in the p (cid:2) q rectangle. This is because of the properties of

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2623

n D 6; j D 2

q

0

0

8

7

6

0

5

4

0

0

3

0

2

1

0

0

0

0
0

0

0

0

0

0

0

0

0

0
0
1

1160 714

85

1160 714

85

1160 714

85

1790 714

85

85

85

85

85

80 2174 441

85

85

85

85

85

85

85

85

85

85

85

85

85

85

85

85

0

0

0

0
0
2

457 2174 714 714 714 714

0

0

0
0
3

80 1790 1160 1160 1160

0

0
0
4

0

0
0
5

0

0
0
6

0

0
0
7

0

0
0
8

p

Figure 22: Another view of the Betti numbers. Let n D 6 and j D 2, and let
p and q be the horizontal and vertical axes. Then the solid regime is in the
lower-left, the gas regime is in the upper-right, and the liquid regime (in bold)
is in between. If p (cid:21) n, then the inclusion map C.nI p; q/ ,! C.nI p C 1; q/
induces an isomorphism on homology. Similarly, if q (cid:21) n then the inclusion
map C.nI p; q/ ,! C.nI p; q C 1/ induces an isomorphism on homology.

our discrete gradient vector field. Namely, we know that if a cell’s apex fits into a p (cid:2) q
rectangle, so does every boundary cell of that cell (the apex takes upper-right corners,
and the p (cid:2) q rectangle grows from the lower-left). Together with the fact that every
two paired cells have the same apex, this implies that the X.nI p; q/ Morse complex
is a subcomplex of the X.nI p0; q0/ Morse complex whenever p (cid:20) p0 and q (cid:20) q0. The
construction of the discrete gradient vector field guarantees that no apex that skips a
row or column can be the apex of a critical cell — this is because every apex graph
with an isolated vertex has an even number of independent sets — so the X.nI n; n/
Morse complex is sufficiently large to contain the Morse complexes for all X.nI p; q/.

Thus, the code computes as follows. First, we list all ways of placing n squares
in an n (cid:2) n grid. Then, we check which of these arrangements are the apex of a
critical cell. For each critical cell, we compute its boundary in the Morse complex by

Algebraic & Geometric Topology, Volume 23 (2023)

2624

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

n p q

2 2 2
3 2 2
3 2 3
3 3 3
4 2 3
4 2 4
4 3 3
4 3 4
4 4 4
5 2 3
5 2 4
5 2 5
5 3 3
5 3 4
5 3 5
5 4 4
6 3 3

f0

f1

f2

f3

f4

f5

f6

f7

f8

4

72

18
624

144
1560
264
4464
11 520
76 608
402 336

16
24
252
1512
672
4800
10 080
48 960
209 664
840
18 000
109 200
50 400
42 8400

12
24
120
504
360
1680
3024
11 880
43 680
720
14 280
6720
17 520
141 600
30 240
2160
55 200
15 120
95 040
234 720
735 840
360 360 1 887 600 3 979 800 4 322 880 2 561 160
524 160 2 882 880 6 448 200 7 538 400 4 928 640 1 793 280 345 240 33 120 1440
60 480

3120
79 200
22 080
600 600

1488
5184
56 448
393 120

120
720
19 536
206 232

1680
114 960

38 040
800 400

2688
56 640

96
7728

181 440

161 280

40 320

5280

576

960

24

Table 2: The f –vectors for X.nI p; q/ for small n, p, and q.

applying discrete gradient flow to its original boundary in X.nI n; n/. Doing this for
every critical cell gives all boundary coefficients for the Morse complex of X.nI n; n/,
computed as integers with signs. Then we restrict to smaller p (cid:2)q rectangles, producing
subcomplexes of the Morse complex. For each p and q, we compute the Betti numbers
from the ranks of the boundary matrices and the dimensions of the chain groups;
because the matrices have integer entries, to specify the coefficient field for homology,
we only need to specify the field for the rank computation, which can be done over Q
or modulo any choice of prime. The Sage notebook is available online.1

We found that the code runs quickly for n (cid:20) 5 and agrees with our other computation
methods; for n (cid:20) 6 it becomes slow and would require more speed optimization.

7.2 PyCHomP

We briefly review the computations involved in pyCHomP, which may be used to
compute the homology of X.nI p; q/ with Z=2Z coefficients.

Let .P; (cid:20)/ be the total order with P D f0; 1g and 0 (cid:20) 1. As X.nI p; q/ is a subcomplex
of G.nI p; q/, there is an order-preserving map (cid:23) from the face poset .G.nI p; q/; (cid:20)/

1https://gist.github.com/ubauer/87e7ee1462966127e9837c4747829a4a

Algebraic & Geometric Topology, Volume 23 (2023)

Homology of configuration spaces of hard squares in a rectangle

2625

to .P; (cid:20)/ given by

(cid:23).(cid:27)/ D

(cid:26)0
1

if (cid:27) 2 X.nI p; q/;
if (cid:27) 62 X.nI p; q/.

In order to construct the map (cid:23), we use Lemma 3.1 to determine whether a cell belongs
to the cubical complex X.nI p; q/. The complex G.nI p; q/ together with the map (cid:23)
defines a P –graded cell complex; see [8]. PyCHomP uses iterated algebraic–discrete
Morse theory to reduce G.nI p; q/ to a (chain-homotopy equivalent) P –graded cell
complex .A.nI p; q/; (cid:22)/ characterized by the condition that @Aj(cid:22)(cid:0)1.p/ D 0 for p 2 P .
This condition implies that the j –dimensional Betti number of X.nI p; q/ is precisely
the number of j –dimensional cells in (cid:22)(cid:0)1.0/; see [8, Example 4.30] for more detail.

Theorems 5.1–5.3 suggest that speedups can be obtained for any code which computes
homology starting from the complex X.nI p; q/ by not considering cells above a certain
dimension. The branch of pyCHomP available at [9] incorporates these speedups;
pyCHomP is able to compute the Betti numbers for all the examples in Table 1. A
Jupyter notebook which sets up the computation of Betti numbers for X.nI p; q/ is
available online.2

7.3 DIPHA

Finally, we describe the homology computation of X.nI p; q/ using DIPHA, a software
package for computing persistent homology in a distributed setting [4; 5]. DIPHA
supports the computation of persistent homology for lower star filtrations of cubical
grids such as G.nI p; q/. The data determining a lower star filtration is a real-valued
function f on the vertices of G.nI p; q/, ie the integer points in .Œ1; p(cid:141) (cid:2) Œ1; q(cid:141)/n. The
filtration then consists of the full subcomplexes of the ambient cube complex G.nI p; q/
induced by sublevel sets f (cid:0)1.(cid:0)1; t(cid:141) of the function f .

Our computations make use of the fact that X.nI p; q/ is a full subcomplex of the
ambient cube complex G.nI p; q/ (see Corollary 3.2). In other words, the complex
X.nI p; q/ is determined by the set of all configurations in C.nI p; q/ with integer
coordinates. Thus, it suffices to enumerate all permutations of all n–element subsets
of the p (cid:2) q possible integer coordinates for the cubes. The input to DIPHA consists
of the characteristic function of this set as a subset of all vertices of G.nI p; q/. A
Mathematica file for generating the input to DIPHA is available online.3

2https://github.com/kellyspendlove/pyCHomP/blob/config/doc/config/ConfigSpacePaper.ipynb
3https://gist.github.com/ubauer/01934ad494eeb6e9ef66ca14e0301fe9

Algebraic & Geometric Topology, Volume 23 (2023)

2626

H Alpert, U Bauer, M Kahle, R MacPherson and K Spendlove

References

[1] H Alpert, Restricting cohomology classes to disk and segment configuration spaces,

Topology Appl. 230 (2017) 51–76 MR Zbl

[2] H Alpert, M Kahle, R MacPherson, Configuration spaces of disks in an infinite strip,

J. Appl. Comput. Topol. 5 (2021) 357–390 MR Zbl

[3] Y Baryshnikov, P Bubenik, M Kahle, Min-type Morse theory for configuration spaces

of hard spheres, Int. Math. Res. Not. 2014 (2014) 2577–2592 MR Zbl

[4] U Bauer, M Kerber, J Reininghaus, DIPHA, a distributed persistent homology

algorithm (2014) Available at https://github.com/DIPHA/dipha

[5] U Bauer, M Kerber, J Reininghaus, Distributed computation of persistent homology,
from “Proceedings of the 16th workshop on algorithm engineering and experiments
(ALENEX ’14)”, SIAM, Philadelphia, PA (2014) 31–38 Zbl

[6] G Carlsson, J Gorham, M Kahle, J Mason, Computational topology for configuration

spaces of hard disks, Phys. Rev. E 85 (2012) art. id. 011303

[7] R Forman, Morse theory for cell complexes, Adv. Math. 134 (1998) 90–145 MR Zbl
[8] S Harker, K Mischaikow, K Spendlove, A computational framework for connection

matrix theory, J. Appl. Comput. Topol. 5 (2021) 459–529 MR Zbl

[9] S Harker, K Spendlove, pyCHomP (computational homology project with python bind-
ings) (2020) https://github.com/kellyspendlove/pyCHomP/tree/config

[10] W W Johnson, W E Story, Notes on the “15” puzzle, Amer. J. Math. 2 (1879) 397–404

MR Zbl

[11] L Plachta, Configuration spaces of squares in a rectangle, Algebr. Geom. Topol. 21

(2021) 1445–1478 MR Zbl

[12] D Sonneveld, J Slocum, The 15 puzzle: how it drove the world crazy, Solcum Puzzle

Foundation, Beverly Hills, CA (2006)

Department of Mathematics and Statistics, Auburn University
Auburn, AL, United States
Department of Mathematics, Technical University of Munich
Munich, Germany
Department of Mathematics, Ohio State University
Columbus, OH, United States
School of Mathematics, Institute for Advanced Study
Princeton, NJ, United States
Mathematical Institute, University of Oxford
Oxford, United Kingdom

hcalpert@auburn.edu,
rdm@ias.edu, kelly.spendlove@gmail.com

mail@ulrich-bauer.org,

mkahle@math.osu.edu,

Received: 20 November 2020

Revised: 4 October 2021

Geometry & Topology Publications, an imprint of mathematical sciences publishers

msp

ALGEBRAIC & GEOMETRIC TOPOLOGY
msp.org/agt

EDITORS

PRINCIPAL ACADEMIC EDITORS

John Etnyre
etnyre@math.gatech.edu
Georgia Institute of Technology

Kathryn Hess
kathryn.hess@epfl.ch
École Polytechnique Fédérale de Lausanne

BOARD OF EDITORS

Julie Bergner University of Virginia

jeb2md@eservices.virginia.edu

Robert Lipshitz University of Oregon
lipshitz@uoregon.edu

Steven Boyer Université du Québec à Montréal

Norihiko Minami Nagoya Institute of Technology

cohf@math.rochester.edu

Tara E. Brendle University of Glasgow

Indira Chatterji

tara.brendle@glasgow.ac.uk
CNRS & Université Côte d’Azur (Nice)
indira.chatterji@math.cnrs.fr

Alexander Dranishnikov University of Florida
dranish@math.ufl.edu
Corneli Dru¸tu University of Oxford

cornelia.drutu@maths.ox.ac.uk

Tobias Ekholm Uppsala University, Sweden
tobias.ekholm@math.uu.se

nori@nitech.ac.jp
Andrés Navas Universidad de Santiago de Chile

andres.navas@usach.cl
Thomas Nikolaus University of Münster

nikolaus@uni-muenster.de

Robert Oliver Université Paris 13

bobol@math.univ-paris13.fr

Birgit Richter Universität Hamburg

Jérôme Scherer

birgit.richter@uni-hamburg.de
École Polytech. Féd. de Lausanne
jerome.scherer@epfl.ch
Princeton University
szabo@math.princeton.edu

Ulrike Tillmann Oxford University

tillmann@maths.ox.ac.uk

Mario Eudave-Muñoz Univ. Nacional Autónoma de México

Zoltán Szabó

David Futer

mario@matem.unam.mx
Temple University
dfuter@temple.edu

John Greenlees University of Warwick

Maggy Tomova University of Iowa

john.greenlees@warwick.ac.uk

maggy-tomova@uiowa.edu

Ian Hambleton McMaster University

ian@math.mcmaster.ca
Hans-Werner Henn Université Louis Pasteur
henn@math.u-strasbg.fr
Daniel Isaksen Wayne State University

isaksen@math.wayne.edu
Christine Lescop Université Joseph Fourier

lescop@ujf-grenoble.fr

Nathalie Wahl University of Copenhagen

wahl@math.ku.dk

Chris Wendl Humboldt-Universität zu Berlin

wendl@math.hu-berlin.de
Daniel T. Wise McGill University, Canada

daniel.wise@mcgill.ca

See inside back cover or msp.org/agt for submission instructions.
The subscription price for 2023 is US $650/year for the electronic version, and $940/year ( C $70, if shipping outside the US)
for print and electronic. Subscriptions, requests for back issues and changes of subscriber address should be sent to MSP.
Algebraic & Geometric Topology is indexed by Mathematical Reviews, Zentralblatt MATH, Current Mathematical Publications
and the Science Citation Index.

Algebraic & Geometric Topology (ISSN 1472-2747 printed, 1472-2739 electronic) is published 9 times per year and continu-
ously online, by Mathematical Sciences Publishers, c/o Department of Mathematics, University of California, 798 Evans Hall
#3840, Berkeley, CA 94720-3840. Periodical rate postage paid at Oakland, CA 94615-9651, and additional mailing offices.
POSTMASTER: send address changes to Mathematical Sciences Publishers, c/o Department of Mathematics, University of
California, 798 Evans Hall #3840, Berkeley, CA 94720-3840.

AGT peer review and production are managed by EditFlow® from MSP.

PUBLISHED BY

mathematical sciences publishers

nonprofit scientific publishing
http://msp.org/
© 2023 Mathematical Sciences Publishers

ALGEBRAIC & GEOMETRIC TOPOLOGY

Volume 23

Issue 6 (pages 2415–2924)

2023

An algorithmic definition of Gabai width

RICKY LEE

Classification of torus bundles that bound rational homology circles

JONATHAN SIMONE

A mnemonic for the Lipshitz–Ozsváth–Thurston correspondence

ARTEM KOTELSKIY, LIAM WATSON and CLAUDIUS ZIBROWIUS

New bounds on maximal linkless graphs

RAMIN NAIMI, ANDREI PAVELESCU and ELENA PAVELESCU

Legendrian large cables and new phenomenon for nonuniformly thick knots

ANDREW MCCULLOUGH

Homology of configuration spaces of hard squares in a rectangle

HANNAH ALPERT, ULRICH BAUER, MATTHEW KAHLE, ROBERT MACPHERSON and
KELLY SPENDLOVE

Nonorientable link cobordisms and torsion order in Floer homologies

SHERRY GONG and MARCO MARENGON

2415

2449

2519

2545

2561

2593

2627

A uniqueness theorem for transitive Anosov flows obtained by gluing hyperbolic plugs

2673

FRANÇOIS BÉGUIN and BIN YU

Ribbon 2–knot groups of Coxeter type

JENS HARLANDER and STEPHAN ROSEBROCK

Weave-realizability for D –type

JAMES HUGHES

Mapping class groups of surfaces with noncompact boundary components

RYAN DICKMANN

2715

2735

2777

Pseudo-Anosov homeomorphisms of punctured nonorientable surfaces with small stretch factor

2823

SAYANTAN KHAN, CALEB PARTIN and REBECCA R WINARSKI

Infinitely many arithmetic alternating links

MARK D BAKER and ALAN W REID

Unchaining surgery, branched covers, and pencils on elliptic surfaces

TERRY FULLER

Bifiltrations and persistence paths for 2–Morse functions

RYAN BUDNEY and TOMASZ KACZYNSKI

2857

2867

2895

A

L

G

E

B

R

A

I

C

&

G

E

O

M

E

T

R

I

C

O

P

O

L

O

G

Y

T

2

0

2

3

V

o

l

.

2

3

,

I

s

s

u

e

6

(

p

a

g

e

s

2

4

1

5

–

2

9

2

4

)

