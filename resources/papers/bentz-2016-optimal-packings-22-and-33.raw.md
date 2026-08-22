6
1
0
2

n
u
J

2
1

]

O
C
.
h
t
a
m

[

1
v
6
4
7
3
0
.
6
0
6
1
:
v
i
X
r
a

Optimal Packings of 22 and 33 Unit Squares in a Square

Wolfram Bentz
Department of Physics and Mathematics
University of Hull
United Kingdom
W.Bentz@hull.ac.uk

October 20, 2018

Abstract

Let s(n) be the side length of the smallest square into which n non-overlapping unit squares can be
packed. In 2010, the author showed that s(13) = 4 and s(46) = 7. Together with the result s(6) = 3
by Keaney and Shiu, these results strongly suggest that s(m2 − 3) = m for m ≥ 3, in particular for the
values m = 5, 6, which correspond to cases that lie in between the previous results.

In this article we show that indeed s(m2 − 3) = m for m = 5, 6, implying that the most efﬁcient
packings of 22 and 33 squares are the trivial ones. To achieve our results, we modify the well-known
method of sets of unavoidable points by replacing them with continuously varying families of such sets.

1 Introduction

The study of packing unit squares into a square goes back to Erdös and Graham [3], who examined the
asymptotic packing efﬁciency as the side length of the containing square increased towards inﬁnity. Göbel
[6] was the ﬁrst to show that particular packings are optimal for a given non-square number of unit squares.
The search for good packings for given number of unit squares was addressed in the popular science litera-
ture in various articles by Gardner [5].

Let s(n) be the side length of the smallest square into which n non-overlapping unit squares can be
packed. Non-trivial cases for which s(n) is known are s(m2 − 1) = s(m2 − 2) = m for m ≥ 2 (Nagamochi
[8], single values previously shown by Göbel [6], El Moumni [2], and Friedman [4]), s(5) = 2+ 1
2 (Göbel
2
[6]), s(6) = 3 (Kearney and Shiu [7]), s(10) = 3 + 1
2 (Stromquist [10]), s(13) = 4, and s(46) = 7
2
(Bentz [1]). There are moreover non-trivial best packings and lower bounds known for various values of
n. Examples on many of these results and the underlying techniques used are given in the survey article by
Friedman [4].

√

√

In [7] and [1], it was shown that s(m2 − 3) = m for m = 3, 4, 7. These results suggested that the
holds for the intermediate values m = 5, 6. We will show this result in this article, by adopting the proof
15 + 1 ≈ 4.87298 and
for m = 7 from [1]. Previously, the best lower bounds in these cases are s(22) ≥
24 + 1 ≈ 5.89898, and follow from a general result in Nagamochi [8].
s(33) ≥

√

√

As the trivial (or “chess board”) packings show that s(22) ≤ 5, and s(33) ≤ 6, it it sufﬁces to establish
the opposite inequality. Let a box be the interior of any square with side length s satisfying 1 < s ≤ 1.01.
Following Stromberg, we will establish that m2 − 3 squares cannot be packed in a square with side length
smaller then m by proving the equivalent statement that it is impossible to pack m2 − 3 boxes in a square
of side length m.

1

 
 
 
 
 
 
In order to do so, we will adopt the previously used method of unavoidable points to continuously vary-
ing sets of such points. We will introduce this modiﬁcation in Section 2, in addition to given several technical
lemmas. The optimality proofs for m = 6, 5 (n = 33, 22) are then given in sections 3, 4, respectively.

2 Continuously changing unavoidable conﬁgurations

Optimality proofs for square packing utilize arguments based on resource starvation. Subsets of a containing
square are associated with numerical resources in such a way that each packed box uses up a certain amount
of resources (by intersecting the subset corresponding with the resource). The overall amount of resource
available limits the number of boxes that can be packed.

The proofs in [6] and many later publications are based on ﬁnite number of points, each of which has
resource value 1. In [2], resources were associated with line segments, such that the length of intersection
between a box and the line segment determined the amount of resource allocated to the box. A more complex
conﬁguration in [8] uses a combined system of (weighted) points, line segments, and a rectangular area.

Our arguments will use a two-tier approach. We will ﬁrst start out with systems of points containing too
many resources for a direct proof. A new technical result (Theorem 8) will allow us to use the ﬂexibility
in our initial systems to show that any potential packing must contain a local abundance of boxes. We will
use this local “over-concentration" of boxes to obtain a contradicting in combination with a second resource
system based on a line segment.

We will start by stating several “non-avoidance” lemmas, which guarantee that a box will intersect

particular type of subsets in its vicinity.

Lemma 1 (Friedman [4], Stromquist [9]) Let T be a triangle with sides of length at most 1. Then any box
whose centre is in T must contain one of the vertices of T .

Lemma 2 (Friedman [4], Stromquist [9]) Let a ≤ 1, b ≤ 1, and a + 2b ≤ 2
centre is in the rectangle [0, a] × [0, b] must intersect the x-axis, the point (0, a) or the point (a, b).

2, then any box whose

√

We will use Lemma 2 in the cases of a < 2

√

2 − 2 ≈ 0.828, b = 1 and a = 1, b <

√

2 − 1

2 ≈ 0.914.

Lemma 3 (Stromquist [9], [10]) Let 2
(0, 1). Moreover, let f (a) be the inﬁmum of

√

2 − 2 < a < 1, 0 < b < 1, and (a, b) within a distance of 1 from

cos θ
1 + cos θ

+

1 − a cos θ
sin θ

(1)

for θ ∈ (0, π
4 ]. If b < f (a), then any box whose centre is in the quadrilateral with vertices (0, 0), (0, 1), (a, 0),
and (a, b) must intersect the x-axis, the point (0, 1) or the point (a, b). Moreover, the inﬁmum of (1) is a
minimum and is obtained at a value of θ satisfying

2 cos3 θ − (2a + 2) cos2 θ + (a2 − 2a + 3) cos θ − (1 − a2) = 0.

(2)

We will be using Lemma 3 in the case a = 1
2

√

3, b = 0.5.

Lemma 4 (Nagamochi [8]) If l is a line that lies within a distance of (
then l will intersect B with a length of more than 1.

√

2 − 1)/2 of the centre of a box B,

Lemma 5 (Stromquist [9]) Let L1 and L2 be two parallel lines of distance d ≤ 1, and B a box with its
centre between them. Then B must intersect the two lines with a common length of intersection of at least
min{1, 2

2 − 2d}.

√

2

The following lemma extends Lemma 3 to values of a smaller than 2

√

2 − 2.

√

Lemma 6 Let 0 < a < 2
2 − 2, 0 < b ≤ 1, and (a, b) within a distance of 1 from (0, 1). Then any box
whose centre is in the quadrilateral Q with vertices (0, 0), (0, 1), (a, 0), and (a, b) must intersect the x-axis,
the point (0, 1) or the point (a, b).

Proof: If b ≤ 1
2 then the distance from (0, 0) to (a, b) is less than 1 and so the line segment between these
points divides Q into two triangles, all of whose sides have length at least one. The result now follows from
Lemma 1.

2 ), and from (0, 1) to (a, 1

So assume that b > 0.5 and that the box B does not intersect (0, 1) or the x-axis. Now the two line
2 ) divide Q into three triangles, such that Lemma 1 is
2 ). In the ﬁrst

segments from (0, 0) to (a, 1
applicable to each of them. By our assumption, the box B must contain either (a, b) or (a, 1
case, the lemma holds, so assume that B contains (a, 1

2 ).
As the centre of B is contained in Q, it is also contained in the larger rectangle R with corners (0, 0),
(a, 0), (a, 1), and (0, 1). Applying Lemma 2 to R yields that B contains (a, 1). As (a, b) lies on the line
(cid:3)
segment from (a, 1

2 ) to (a, 1), it is contained in B.

We will use the lemma for a = 0.8, 0.4 ≤ b ≤ 1.

Lemma 7 Let l be a line and P a point with a distance of more than 0.51 from l. If a box B covers P such
that P and the center of B lie on opposite sides of l, than B intersect l with a length of intersection that
exceeds 1.

Proof: The midpoint of B must lie within 0.505
from the line l. As this value is less than (

√

2 of P , and hence within a distance of 0.505

2 − 1)/2, the results follows from Lemma 5.

√

√

2 − 0.51
(cid:3)

Consider a square S of side length l in the Euclidean plane (which in our cases we will take to be
[0, m] × [0, m] for m ∈ {5, 6}). A set of points P ⊂ S is called unavoidable if every box B ⊆ S contains
one of the points in P . In practice, we show unavoidability of P by dividing S into several regions Si, so
that by one of our unavoidability lemmas, any box with midpoint in Si must either intersect a point in P or
the boundary of S. If S contains an unavoidable set of t points, it follows that no more than t boxes can be
packed into S, and hence s(t + 1) ≥ l.

Figure 1 depicts an unavoidable set of points for the square [0, 6] × [0, 6]. The points in the lowest row

are

√

(cid:18)

i,

2 −

(cid:19)

1
2

i = 1, 2, . . . , 5,

and the remaining ones are arranged so that all shown triangles are equilateral of side length 1. Lemma 1 is
applicable to the triangles, Lemma 2 to the rectangles, and Lemma 3 to the remaining quadrilateral regions
(with a =

√

3

2 , b = 1
2 ).

Figure 1 is a variant of conﬁgurations used to show that s(46) = 7 in [1] and to derive a lower bound on
s(11) in [10]. As the unavoidable set consists of 33 points, it demonstrates the (known) result that s(34) = 6.

Note that the conﬁguration in Figure 1 contains a degree of ﬂexibility. For example, we can obtain a
different unavoidable conﬁguration by deleting one of the points closest to the left hand side of the square
and instead adding a different point a small amount further to the right. If there exists a packing of 33 boxes,
then each of them must contain exactly one point in each conﬁguration, and hence one box must contain
both the deleted and added point (and the line segment between them), an argument that has appeared in
several previous proofs. The next theorem shows that this approach can be generalized to situations in which
more than one point is moved at one time.

Theorem 8 Let S be a square with a packing P of boxes, I = [a, b], t ∈ N, and fk : I → S a collection of
continuous mappings, for 1 ≤ k ≤ t. Suppose further that

3

Figure 1: An unavoidable sets with 33 points

1. for each i ∈ I, Fi = {fk(i)|1 ≤ k ≤ t} is an unavoidable set of points;
2. if for some 1 ≤ k ≤ t, fk(a) is not contained in a box of P, then fk(i) = fk(a) for all i ∈ I.
3. if for some 1 ≤ k, l ≤ t, k (cid:54)= l, fk(a) and fl(a) lie in the same box of P, then fk(i) = fk(a) for all

i ∈ I.

Then for all 1 ≤ k ≤ t, the image fk(I) will either lie entirely within one box, or completely outside any
box.

If fk(a) is not contained in any box, then fk is constant. Hence for the theorem to be wrong, there
Proof:
must be 1 ≤ k ≤ t, i ∈ I, such that fk(a) lies in some box Bk while fk(i) /∈ Bk. Assume that this is indeed
the case.

As boxes are open and fk is continuous, it follows that there is a smallest such i(cid:48) ∈ I for which fk(i(cid:48))
lies outside Bk. Minimizing over all indices, we may assume w.l.o.g. that i(cid:48) is the smallest value of i for
which any fs(i) lies outside the box containing fs(a).

Now, as Fi(cid:48) is an unavoidable set of points, there exist a 1 ≤ l ≤ k, necessarily with l (cid:54)= k, such that
fl(i(cid:48)) ∈ Bk. Boxes are open, therefore there exist an (cid:15) > 0 such that fl(i(cid:48) − (cid:15)) ∈ Bk. By the minimality
of i(cid:48), it follows that fl(a) ∈ Bk. However, now fl(a), fk(a) ∈ Bk, and so fk is constant by condition 3.,
(cid:3)
contradicting that fk(i(cid:48)) /∈ Bk. The result follows.

3 The best possible packing of 33 unit squares

Theorem 9 33 non-overlapping unit squares cannot be packed in a square of side length less than 6.

Proof: Let S be the square [0, 6]2 and assume by way of contradiction that there is a packing P of
33 boxes into S. Consider the collection of 33 red points and 33 blue points depicted in Figure 2. The red
points are the points from Figure 2, while the blue points are obtained from the red ones by mirroring along
the line y = 3. It follows that both red and blue points form unavoidable sets of points. Hence each box in
P will contain exactly one red and blue point.

We will apply Theorem 8 twice. In the ﬁrst instance we choose our values fk(i) so that Fa is the set of
red points from Figure 2, while in the second case the start conﬁguration will be the set of blue points. We
will give an informal description of the other values of fi(k) by describing the “movement" of the points
conﬁguration. Many of our movement will move an entire row of equally-colored points from Figure 2.

4

Figure 2: Two unavoidable sets with 33 points each

We will denote the red rows and blue rows by r1, . . . , r6, and b1, . . . , b6, respectively, where the rows are
numbered from bottom to top. For any two such rows r, r(cid:48), we denote by v(r, r(cid:48)) their vertical distance.

We ﬁrst note that as every red point and every blue points lies in exactly one box of P, the second and

third condition of Theorem 8 are automatically full-ﬁlled.

Now consider a simultaneous vertical movement of a row ri. Such a move will preserve the unavoidabil-
√
ity of the points conﬁguration as long as, whenever they are deﬁned, v(ri, ri−1) ≤ 1
3
2
and in addition, the vertical distance from r1 and r6 to the top or bottom edge of S, respectively, is at most
√

3, v(ri, ri+1) ≤ 1
2

√

2 − 1
2 .

With regard to a given conﬁguration, for i = 2, . . . , 5, let m1 = v(r1, r2), mi = max{v(ri, ri+1), v(ri, ri−1)},

for i = 2, . . . , 5, and m6 = v(r6, r5). Clearly, for i = 1, . . . , 6, there exists a unique conﬁguration Fi that
minimizes mi and that is reachable from Fa by vertical movement of rows, such that unavoidability is pre-
served throughout. Let y1, . . . , y6 be the second coordinate values of the points in the i-th row in Fi (the
exact values of yi can be easily calculated, but are not needed). As

(cid:18)√

2

2 −

(cid:19)

1
2

+ 2 · 0.8 + 3 ·

√

1
2

3 > 6,

we note that in Fi, we have v(ri, ri−1), v(ri, ri+1) ≤ 0.8, wherever deﬁned.

Now consider Fi for i = 2, 4, 6. Here the the i-th row contains 6 points, and we may move the i-th row
horizontally to to the left and right, provided the distances to all “critical" points in the adjacent rows stays
within 1. As the adjacent rows have a vertical distance of less than 0.8, it is easy to check that this allows for
a movement of at least 0.1 to either side. In addition, in this situation, we may move the left-most point of
any such row horizontally to the right, until it reaches the point (1, yi). This maximal reﬂection is possible,
as the distance to the adjacent row is less than 2

2 − 2 ≥ 0.8.
We now proceed as follows. We move the point conﬁguration to one of the Fi. If the i-th row contains
5 points, we note that one of the points occupies the point (1, yi). If the i-th row contains 6 points, we
move the row 0.1 to the left and back to the right. Finally, move the left-most point of row i from (0.5, yi)
to (1, yi) and back, and note that this point, combining both movements, has moved over the line segment
from (0.4, yi) to (1, yi). We repeat this procedure for all Fi.

√

By Theorem 8, the line segments [0.4, 1]×{yi} for i ∈ {2, 4, 6} lie within the same box of P. Moreover,
as these sets are the result of movement from different points of the base conﬁguration, they, as well as the
point sets {(1, yi)} from the movement of the 5-point rows lie in different boxes.

5

We now repeat this procedure for the blue points, noting that we obtain the same values yi as in the case
of the red points. The blue points will have a 6-point row where the red points have a 5-point row and vice
versa. We can conclude that for i ∈ {1, 3, 5}, the line segment [0.4, 1] × {yi} lies within one box of P.

Hence, taking both conﬁgurations together, the segments [0.4, 1] × {yi} lie each in one box of P for
i = 1, . . . , 6. Moreover, these segments all lie in different boxes as the points (1, yi) are all within the
movement of different points from the red base conﬁguration.

√

√

2 − 1

It follows that in P, there are 6 distinct boxes B1, . . . , B6 such that Bi covers (0.4, yi). Now let l be the
line segment from (
2 , 6). We are interested in the length of the intersection of Bi and
l. If the midpoint of Bi lies on the same side of l as (0.4, yi), then this intersection exceeds 1 by Lemma
5 (with d =
2 ). If the midpoint of Bi lies on l or on the side of l opposite from (0.4, yi), then the
intersection has length larger than 1 by Lemma 7. Hence all six boxes intersect l with a length larger than 1.
However, the length of l is 6, for a contradiction.

2 , 0) to (

2 − 1

2 − 1

√

Hence 33 boxes cannot be packed in a square of side length 6 and so s(33) ≥ 6.

(cid:3)

Corollary 10 The trivial packing is optimal for packing 33 unit squares in a square, and we have that
s(33) = 6.

4 The best possible packing of 22 unit squares

Theorem 11 22 non-overlapping unit squares cannot be packed in a square of side length less than 5.

Proof: Let S be the square [0, 5]2, and assume, by way of contradiction, that there exist a pack-
ing P of 22 boxes into S. Consider the conﬁguration of 22 red and 23 blue points shown in Figure 3.
Together, the points of both colours are exactly the elements the set {0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5} ×
{0.9, 1.7, 2.5, 3.3, 4.1}. We will denote the rows of red and blue points by r1, . . . , r5, and b1, . . . , b5, with
numbering from bottom to top, and we let y1, . . . , y5 be the value of their second coordinate.

Figure 3: Unavoidable conﬁgurations of 22 red and 23 blue points

By the same basic argument as applied to Figure 2 we can show that both the set of red points and the
set of blue points form unavoidable sets. It follows that each red points lies in exactly one box from P. In

6

the case of the blue points, either exactly one blue point is not contained in a box of P or exactly one box
of P contain two blue points. In the latter case, the two blue points that lie in the same box must be within
a distance of each other that is smaller than the diagonal of a maximal size box, which is 1.01
2. Thus, by
the symmetry in our blue point conﬁguration, we may assume that all blue points with ﬁrst coordinate value
lower than 2 lie in a box of P that does not contain any other blue points.

√

As in the proof of Theorem 9, we will apply Theorem 8 twice, with the red and blue points as the respec-
tive starting conﬁgurations. Once again we describe the function fk informally in terms of the movement
of points. In the case of the red points, we will ﬁrst move r2 and r4 (i.e. the red rows containing 5 points)
horizontally a distance of 0.1 to the left and back, followed by a movement of the left-most point in each
such row horizontally to the right until it reaches a ﬁrst coordinate value of 1. These movement preserve
unavoidablility, as the vertical distance between adjacent rows is 0.8 in all cases. As in Theorem 9 we record
that different boxes of P contain the line segments [0.4, 1] × {1.7} and [0.4, 1] × {3.3}, and that these boxes
must also be different from the boxes containing the (stationary) points (1, 0.9), (1, 2.5), and (1, 4.1).

For the blue points, we want repeat these movement with rows b1, b3, and b5. However, we need to
modify our procedure, as Theorem 8 requires the a blue point remains stationary if it does not lie in a box of
P or is in a box of P that contains a different blue point. If row ri, i ∈ {1, 3, 5} does not contain such point,
we move it horizontally a distance of 0.1 and back to its original position. We then move its leftmost point
horizontally from (0.5, yi) to (1, yi). In case that ri does contain such point, we just move its leftmost point
from (0.5, yi) to (1, yi). We note that the last case can only happen for one of the rows b1, b3, b5, because if
there are two such exceptional blue points, they must lie in the same box, and hence (due to the size of the
boxes) in either the same or adjacent rows.

By Theorem 8 the trajectory of each of the leftmost points of b1, r2, b3, r4, b5 lies completely within a
box of P. Moreover each of these trajectories intersects a different red point from the initial conﬁguration,
and hence the trajectories lie within different boxes.

We can conclude that there are 5 boxes B1, . . . , B5 in P such that the line segments [0.4, 1] × {yi} lie
completely within Bi, except that at most one of B1, B3, B5 might only cover the line segment [0.5, 1]×{yi}.
2 } × [0, 5]. As in Theorem 9 we can check that if Bi contains [0.4, 1] ×
{yi}, it intersect l with a length of intersection that exceeds 1. As l has length 5, one of B1, B3, B5 does not
cover the entire line segment from [0.4, 1] × {yi}. We consider 2 cases:

Let l be the line segment {

2 − 1

√

√

√

√

2 − 1

2 − 1

2 − 1

2 − 1

2 − 1

1. First assume that B3 does not completely cover [0, 4] × {y3}. As there was at most one exceptional
It follows that
√
2 , 3). In

row, B1, B2, B4, and B5 all intersect l with a length of intersection exceeding 1.
B3 ∩ l ⊆ {
2 , 2) and (
2 } × (2, 3), and so B3 does not cover the points (
Figure 4, these two points are depicted in green.
Let m be the midpoint of B3. The location of m is constraint as follows: m must lie on the right side
of l and separated from it by a distance of at least 1
2 , for otherwise the length of intersection
2
of B3 and l would exceed 1 by either Lemma 5 or Lemma 4. As B3 does not cover (
2 , 2) or
√
(
2 , 3), m cannot be within a distance of 0.5 from either of these points. Finally, as B3 covers
[0.5, 1] × {y3}, the distance from m to (0.5, y3) must be smaller than half the diagonal of a maximal
2. Figure 4 shows the remaining possible locations of m as a shaded
box, i.e. smaller than 0.505
area. The area is bounded by line and circle segments that intersect in 4 points with approximate
coordinates (1.12, 2.5 ± 0.05), (1.2, 2.5 ± 0.1).
An easy calculation shows that the entire area is within a distance of 0.5 from the point (1.5, y3) =
(1.5, 2.5). In Figure 4, this distance is indicated by a circle. It follows that B3 also covers the point
(1.5, 2.5). Hence in our initial conﬁguration of points, the box B3 covers two blue points, namely
those at (0.5, 2.5) and (1.5, 2.5). However, this contradict our assumption that all blue points with a
second coordinate value smaller than 2 do not share a box with another blue point.

2 − 1

√

√

2. Assume that for one i ∈ {1, 5}, Bi does not cover the entire line segment [0.4, 1]×{yi}. By symmetry,

7

Figure 4: The midpoint of the box B3 must lie in the shaded area

√

we may assume that this is the case for i = 1. Then Bi covers [0.4, 1] × {yi} for i = 2, . . . , 5, and,
as in the previous case, this implies that each such Bi intersects the line segment l with a length of
intersection larger than 1. It follows that the point (
2 , 1) is denied to B1. This point is depicted
green in Figure 5.
Let m be the midpoint of B1. As before we can conclude that m lies on the opposite side of l from
√
the point (0.5,
2
√
of ( 1
2 − 1
2 ,
The resulting area is depicted in Figure 5 and lies completely within a distance of 1
√
2 − 1
2 , 1).
(
contradiction.

2 from the point
2 , 1) lies in B1. However, the point is denied to B1, for a

2
2 ). These constraints intersect at approximately (1.13, 0.56) and (1.13, 1.24).

2 from l, but within a distance of 0.505

2 ), with a distance of at least 1

It follows that (

2 − 1

2 − 1

2 − 1

2 − 1

√

√

√

In either case we get a contradiction. It follows that the packing P does not exists, and hence s(22) ≥ 5. (cid:3)

Corollary 12 The trivial packing is optimal for packing 22 unit squares in a square, and we have that
s(22) = 5.

References

[1] W. Bentz, Optimal Packings of 13 and 46 Unit Squares in a Square Electronic Journal of Combina-

torics 17 (2): #R126, 2010.

[2] S. El Moumni, Optimal Packings of Unit Squares in a Square, Studia Sci. Math. Hungar. 35 (1999),

no. 3-4, 281-290.

[3] P. Erdös and R. L. Graham, On Packing Squares with Equal Squares, J. Combin. Theory Ser. A 19

(1975) 119-123.

[4] E. Friedman, ï£¡ï£¡Packing unit squares in squares: A survey and new resultsï£¡ï£¡, The Electronic

Journal of Combinatorics, Dynamic Surveys (#DS7) (version of Aug 14, 2009)

[5] M. Gardner, “Mathematical Games", Scientiﬁc American (Oct 1979, Nov 1979, Mar 1980, Nov 1980).

8

Figure 5: The midpoint of the box B1 must lie in the shaded area

[6] F. Göbel, Geometrical Packing and Covering Problems, in Packing and Covering in Combinatorics,

A. Schrijver (ed.), Math Centrum Tracts 106 (1979) 179-199.

[7] M. Kearney and P. Shiu, Efﬁcient Packing of Unit Squares in a Square, Elect. J. Comb. 9 #R14 (2002).

[8] H. Nagamochi, Packing Unit Squares in a Rectangle, Elect. J. Comb. 12 #R37 (2005).

[9] W. Stromquist, “Packing Unit Squares Inside Squares I, II, III", unpublished manuscripts, 1984-5;

http://www.walterstromquist.com/publications.html.

[10] W. Stromquist, Packing 10 or 11 Unit Squares in a Square, Elect. J. Comb. 10 #R8 (2003).

9

