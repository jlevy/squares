Packing 10 or 11 Unit Squares in a Square

Walter Stromquist
Department of Mathematics
Bryn Mawr College, Bryn Mawr, Pennsylvania, USA
walters@chesco.com

Submitted: Nov 26, 2002; Accepted: Feb 26, 2003; Published: Mar 18, 2003
MR Subject Classiﬁcations: 05B40, 52C15

Abstract

Let s(n) be the side of the smallest square into which it is possible pack n unit
4
squares. We show that s(10) = 3 +
5 ≈ 3.789.
We also show that an optimal packing of 11 unit squares with orientations limited to
8
0◦ or 45◦ has side 2+2
9 ≈ 3.886. These results prove Martin Gardner’s conjecture
that n = 11 is the ﬁrst case in which an optimal result requires a non-45◦ packing.

1
2 ≈ 3.707 and that s(11) ≥ 2 + 2

q

q

q

Let s(n) be the side of the smallest square into which it is possible to pack n unit
1
squares. It is known that s(1) = 1, s(2) = s(3) = s(4) = 2, s(5) = 2 +
2, and that
s(6) = s(7) = s(8) = s(9) = 3. For larger n, proofs of exact values of s(n) have been
published only for n = 14, 15, 24, 35, and when n is a square. The ﬁrst published proof
that s(6) = 3 is by Kearney and Shiu [3] and the other results are reported in Erich
Friedman’s dynamic survey [1].

q

We prove here that s(10) = 3 +

≈
3.789 (Theorem 2). The 10-square packings in Figure 1 are optimal. The most eﬃcient
known packing of 11 squares, shown in Figure 2 and due to Walter Trump, has side about
3.8772 and includes unit squares tilted at about 40.182◦.

≈ 3.707 (Theorem 1) and that s(11) ≥ 2 + 2

q

4
5

q

1
2

q

s = 3 +

1
2

≈ 3.707

Figure 1: Best packings of 10 squares

the electronic journal of combinatorics 10 (2003), #R8

1

s ≈ 3.8772

s ≈ 3.886

Figure 2: Best known packing
of 11 squares (tilt ≈ 40.182◦)

Figure 3: Optimal 45◦ packing
for n = 11

In the case of n = 11, we also show that any 45◦ packing—that is, one in which the
unit squares are tilted only at 0◦ or 45◦ with respect to the bounding square—must have
≈ 3.886 (Theorem 3). This bound is realized by the packing by
side at least 2 + 2
H¨am¨al¨ainen [2] in Figure 3. Together, these results establish the truth of Martin Gardner’s
conjecture in [7], that n = 11 is the ﬁrst case in which non-45◦ packings are required.

q

8
9

These results were ﬁrst reported in [4,5,6]. We take the approach that was used in those
memoranda and also used in [1] for establishing lower bounds. For rhetorical reasons, we
deﬁne a box to be the interior of any square of side strictly greater than 1. In order to
establish a lower bound of the form s(n) ≥ a, we prove the equivalent statement that n
nonoverlapping boxes cannot be packed inside a square with side exactly a. For the most
part we treat boxes as if they were unit squares, and rely on the extra margin of size to
convert equations into inequalities as needed.

1 Nonavoidance Lemmas

In this section we present six “nonavoidance lemmas.” Each lemma provides that if the
center of a box is in some region, then the box must have a nonempty intersection with
certain parts of the region’s boundary. Lemmas 1–4 are general in nature, while Lemmas 5
and 6 are needed speciﬁcally for the proofs of Theorems 1 and 2 respectively. The lemmas
are illustrated in Figure 4.

The ﬁrst three lemmas are the same as Lemmas 1–3 in [1].

Lemma 1 Let a ≤ 1 and b ≤ 1. Then any box whose center is in the rectangle [0, a]×[0, b]
must intersect the x-axis, the y-axis, or the point (a, b).

Lemma 2 Let T be a triangle with sides of length at most 1. Then any box whose center
is in the interior of T must contain one of the vertices of T .

the electronic journal of combinatorics 10 (2003), #R8

2

≤1

≤1

≤.

≤1

≤1

(1,

≤.

(1,1)

,1)

.12

.12

1

≤1

≤1

1

≤.

Figure 4: The nonavoidance lemmas

Lemma 3 Let a and b satisfy a ≤ 1, b ≤ 1, and a + 2b ≤ 2
2. Then any box whose
center is in the rectangle [0, a] × [0, b] must intersect the x-axis, the point (0, b), or the
point (a, b).

√

We use Lemma 3 mainly in the case of a = 2

Figure 4. The other extreme is a = 1, b =

We need some preparation for Lemma 4. When 2

√

2 − 1
2

2 − 2 ≈ .828, b = 1, as shown in
≈ .914.
√

2 − 2 < a < 1, deﬁne f (a) by

√

f (a) =

cos θ∗
1 + cos θ∗ +

1 − a cos θ∗
sin θ∗

where θ∗ is the smallest positive value of θ that satisﬁes

2 cos3 θ − (2a + 2) cos2 θ + (a2 − 2a + 3) cos θ − (1 − a2) = 0.

(1)

(2)

For values of a in the domain of f we always have 0 < θ∗ < 45◦ and 0 < f (a) < 1.

Lemma 4 Let a and b satisfy 2
2 − 2 < a < 1, 0 < b < 1, (a, b) within 1 of (0, 1), and
b ≤ f (a). Then any box whose center is in the quadrilateral with vertices (0, 0), (0, 1),
(a, 0), and (a, b) must intersect the x-axis, the point (0, 1), or the point (a, b).

√

We rely on these cases of Lemma 4:

q

≈ .853

1
2 +

a:
f (a):
θ∗:

1
8
.972
39.5◦

q

4
5

≈ .894
.926
24.1◦

.96
.769
17.7◦

the electronic journal of combinatorics 10 (2003), #R8

3

L
e
m
m
a
 
2
8
2
8
L
e
m
m
a
 
3
L
e
m
m
a
 
2
L
e
m
m
a
 
4
L
e
m
m
a
 
6
7
5
9
6
L
e
m
m
a
 
5
.
7
8
8
)
(
2
(
2
,
.
9
)
.
8
9
4
 
 
(0,1)

*

z/cos θ

1-a cos θ
   sin θ

(a,b*)

1-a cos θ

z

*

a cos  θ

θ

Figure 5: Proof of Lemma 4

Proof. If a box avoids both the x-axis and the point (0, 1), then its edge might as well
touch both as shown in Figure 5. Let (a, b∗) be the point at which the box’s top edge
meets the line x = a. The two triangles marked * are congruent. Since z + z/ cos θ = 1,
we have z = cos θ

1+cos θ and

b∗ =

cos θ
1 + cos θ +

1 − a cos θ
sin θ

√

.

(3)

If we ﬁx a in the range 2
2 − 2 < a < 1 and limit θ to the ﬁrst quadrant, then the right
side of (3) has a unique minimum, which occurs when θ < 45◦ and b∗ < 1. (To verify this,
note that b∗ is large when θ ≈ 0, below 1 when θ = 45◦, and decreasing to 1 when θ = 90◦,
and that the derivative doesn’t have enough roots for there to be multiple minima below
45◦.) Setting db∗/dθ = 0, leads to equation (2) above. Therefore f (a) is the minimum
value of b∗.

If (a, b) is within 1 of (0, 1) but below (a, f (a))—and hence below (a, b∗) whatever the
2

value of θ—then (a, b) is clearly inside the box.

Lemma 5 Let P be the pentagon with vertices (1, 0), (1, 1), (2, 1), (2.12, .9), and (2.12, 0).
Then any box whose center is in the interior of P must intersect the x-axis, the segment
from (1, 0.788) to (1, 1), or the segment form (2, 1) to (2.12, .90).

Proof. By Lemma 1, any counterexample must include a point to the left of x = 1 and
a point to the right of x = 2. Without loss of generality, the box’s boundary touches the
x axis and includes the point (1, .788) as shown in Figure 6. Let θ be the angle of the box
with the x axis, as shown.

If θ ≤ tan−1(1.2) ≈ 50.2◦, then the box must contain the point (2, 1). To see this,
we calculate the x-coordinate of the point (x, 1) at which the box’s upper-right boundary
crosses the line y = 1:

the electronic journal of combinatorics 10 (2003), #R8

x = 1 +

.212
tan θ +

sin θ + cos θ − 1
sin θ cos θ

.

(4)

4

(1,1)

(1,.788)

(2,1)

(2.12,.9)

θ

Figure 6: Proof of Lemma 5

The last term is the length of the box’s intersection with the line y = 1, and it exceeds
.828 for any ﬁrst-quadrant value of θ, so when tan θ ≤ 1.2 we have

x > 1 +

.212
1.2

+ .828 > 2.004,

forcing the point (2, 1) to be inside the box.

If tan−1(1.2) < θ ≤ sin−1(.9) ≈ 64.2◦, then the box contains the point (2.12, .9). To see
this, we compute the x-coordinate of the point at which the box’s upper-right boundary
intersects the line y = .9. We obtain

x = 1 +

.112
tan θ +

sin θ + cos θ − .9
sin θ cos θ

.

(5)

This function reaches its minimum at θ ≈ 52.6◦, when x = 2.1256, so the box’s right
boundary always passes to the right of (2.12, .9).

If sin−1(.9) < θ we need to calculate the coordinates (x, y) of the box’s rightmost

vertex:

x = 1 +
y = sin θ.

1
sin θ + cos θ −

.788
tan θ

Since .9 < y < 1, the vertex is to the right of the critical segment if (x − 2)/(1 − y) > 1.2.
Some calculation shows that

1 − cos θ
sin θ + .212
When sin θ > .9 the ﬁrst term on the right is at least .6 and the second term is at least
2
1, so the lemma is proved.

1 + sin θ
sin θ cos θ

x − 2
1 − y =

.

the electronic journal of combinatorics 10 (2003), #R8

5

q

Lemma 6 Let a =
vertices at (1, 0), (1, 1), (1 + 1
2
or one of the vertices.

4
5

≈ .894. Then any box whose center is in the pentagon with
a, 1.12), (1 + a, 1), and (1 + a, 0) must intersect the x-axis

Proof. We may assume that any counterexample involves a box touching the x-axis as
in Figure 7. If D(θ) is the length of the intersection of the box with the line y = 1, then

D(θ) =

=

1
sin θ +
√
2

1
cos θ
1 + sin 2θ − 2

−

1
sin θ cos θ

.

sin 2θ

(cid:16)

√

(cid:17)

5

5 − 2

2 sin−1

≈ 15.9◦; then D(θ0) = a.

Let θ0 = 1
− θ0 then
D(θ) > a and the box must intersect (1, 1) or (1 + a, 1). We can therefore assume that
θ0 ≤ θ ≤ π
− θ0. In this case cos θ + sin θ > 1.12, so the box includes a point above
2
y = 1.12. We may assume that the box touches the point (1 + a, 1) and has its apex to
the right of the line x = 1 + 1
a, as shown in the ﬁgure. Now the y coordinate at which
2
the top of the box intersects the line x = 1 + 1
2
s

If θ < θ0 or θ > π
2

a is given by

0

1

1 +

@D(θ) −

A tan θ,

1
5

which by direct computation is equal to 1.1277... when θ = θ0, and increases with θ.
Therefore the box intersects the line above the point (1 + 1
a, 1.12), and must include that
2
2
point.

(1+a/2,1.12)

(1,1)

(1+a,1)

θ

Figure 7: Proof of Lemma 6

the electronic journal of combinatorics 10 (2003), #R8

6

2 Ten Squares

Theorem 1 Ten pairwise nonintersecting boxes cannot exist in the interior of a square
of side s = 3 +

q

1
2.

q

1

2 and let S be the square [0, s]2. Deﬁne ten points
Proof. In this section, ﬁx s = 3 +
A, B, . . . , J as shown in Figure 8. We set A = (1, 1), B = (.97, s
2), and place
the other points symmetrically in S. Each of the regions outlined in the ﬁgure is covered
by one of Lemmas 1, 2, or 4 (with a ≈ .853, b = .97). It follows that these ten points are
unavoidable in the sense of [1], meaning that any box inside S must contain one of the
points. If ten boxes are packed in S, each must contain exactly one of them. We name
the boxes for the points they contain—A-box, B-box, etc.

2), I = (1.4, s

C

D

I

J

B

A

H

E

F

G

Figure 8: Each box contains one of these ten points

The key to the proof is to show that the H-box also contains some point on the short
segment from (2, 1) to (2.12, .9). We will prove this fact and then show why it matters.
1. The points remain unavoidable if B is replaced by B0 = (.75, s − 1.96). Therefore,
the point B0 is contained in the B-box. (We now use Lemma 4 with a = .96, b = .75.)

C

D

I

J

B'

A'

A''

H

E

F

G

C

D

I

J

B'

A'

A''

H

E

F

G

Figure 9: A-box contains one of A0, A00

Figure 10:
then H-box contains H0=(2,1)

If A-box contains A00,

the electronic journal of combinatorics 10 (2003), #R8

7

B

*
*

*

*

*

*

*

*

Figure 11: H-box must touch seg-
ment

Figure 12: No room for I-box and
J-box

2. If, now, A is replaced by the two points A0 = (1, s − 2.92) and A00 = (1.2, 1), the
points remain unavoidable (Figure 9). It follows that the A-box must contain at
least one of the points A0, A00. Note that s − 2.92 < .788.

3. If the A-box contains A00 = (1.2, 1), then the points A, A00, B0, C through G, I, J,
and (2, 1) form an unavoidable set (Figure 10). All of these are denied to the H-box
except for (2, 1), so the H-box contains (2, 1). (This step uses Lemma 3.)

4. If the A-box contains A0 = (1, s−2.92), then the entire segment from A0 to A (which
includes the segment from (1, .788) to (1, 1)) is denied to the H-box, as are points B
through G, I, and J. Figure 11 shows a partition of S in which Lemma 5 applies to
one of the regions. From this ﬁgure, we see that the H-box must touch the segment
from (2, 1) to (2.12, .9).

In either case, the H-box must contain some point on the indicated segment.
In
Figure 12 the point of intersection is marked with an asterisk. Seven other asterisks mark
other points which must be contained in the B-, D-, F-, and H-boxes by symmetrical
arguments. We do not know the locations of these points exactly, but we can tell that
each asterisk is within 1 of the center of the square and within 1 of each of the two
asterisks nearest to it. Each of the heavy line segments connects two asterisks that must
be in the same box.

Now, the thirteen points in Figure 12—the eight asterisks, the points A, C, E, G, and
the center of the square—clearly form an unavoidable set. All but the center are denied
to the I- and J-boxes, and those two boxes cannot both contain the center. This shows
2
that the 10-box packing is impossible.

the electronic journal of combinatorics 10 (2003), #R8

8

F

E

H

G

A

I

J

D

C

B

Figure 13: Ten points to avoid
and how to avoid them

Figure 14: Twelve points for
Theorem 2

3 Eleven Squares
q

Theorem 2 Let s = 2 + 2
inside a square of side s.

4
5

≈ 3.789. Then eleven non-intersecting boxes cannot exist

q

4

5 and let S = [0, s]2. Consider the ten points in
Proof. For this proof, ﬁx s = 2 + 2
Figure 13. Four of these points have coordinates (1, 1), ( s
, s
2), and
2
the rest are placed symmetrically. The vertical distance between the rows of points is
s
≈ .894. The triangles in the ﬁgure are all congruent, and the sloping sides
2
have length 1.

2), ( 1
, s

, 1), ( 3
2

− 1 =

2 + s

− s
4

q

4
5

4

Nonavoidance lemmas apply to all of the regions shown except for the rectangles at the
top and bottom. If 11 boxes are to be packed into the square, at least one of them must be
placed in one of those rectangles, roughly as shown in the ﬁgure (up to symmetry). From
Lemmas 4 and 6 we can see that this box must contain all three of the points marked
“A” in Figure 14:

8
>><
>>:

(1, .9)
( s
q
2
(1 +

A =

, .9) ≈ (1.894, .9)

1
5

, 1.12) ≈ (1.447, 1.12)

There are nine other points in Figure 14:

s

2

) ≈ (2.889, 1.894)

B = (s − 1, 1) ≈ (2.789, 1)
C = (s − .9,
D = (s − 1, s − 1) ≈ (2.789, 2.789)
E = (
F = (1, s − 1) ≈ (1, 2.789)
G = (.8, 1.85)
H = (1.5, 2.1)

, s − .9) ≈ (1.894, 2.889)

2

s

the electronic journal of combinatorics 10 (2003), #R8

9

I = (2.1, 2.1)
J = (2.1, 1.5)

Nonavoidance lemmas apply to all of the regions in this ﬁgure. Since three of the twelve
points are in one box, there cannot be eleven nonintersecting boxes. This completes the
2
proof of Theorem 2.
The argument in Figure 14 is not rigid; any point in the ﬁgure could be moved by a
small amount in almost any direction without causing the argument to fail. The critical
distances are all in Figure 13.

45◦ packings. We now apply the same technique to the case of 45◦ packings. By
considering only boxes that are oriented at 0◦ or 45◦ to the axes (“0◦ and 45◦ boxes”) we
can prove stronger forms of some of our lemmas. In particular:

Lemma 7 Let T be a triangle, and suppose that the component of any side of T in the
direction of any unit vector making an angle of 0◦ or 45◦ with either axis is at most 1.
Then any 0◦ or 45◦ box whose center is in the interior of T must contain one of the
vertices of T .

Lemma 8 If (a, b) = (1, .8) or (a, b) = ( 2
2 − 2), then any 0◦ or 45◦ box whose
3
center is in the quadrilateral with vertices (0, 0), (0, 1), (a, 0), and (a, b) must intersect
the x-axis, the point (0, 1), or the point (a, b).

2, 2

√

√

The proofs are easier than in the general case and are omitted. With these more
powerful lemmas, we can justify a larger value of s in the following theorem, which is
enough to settle Martin Gardner’s conjecture.

Theorem 3 Let s = 2 + 4
2 ≈ 3.886. Then eleven non-intersecting boxes cannot exist
3
inside a square of side s, if each box has orientation 0◦ or 45◦ with respect to the square.

√

√

Proof. Now ﬁx s = 2+ 4
3

2 and let S = [0, s]2. Consider ten points deﬁned exactly as
in Figure 13—four of these points have coordinates (1, 1), ( s
, s
2)—but
2
with the new value of s. If eleven boxes are to be packed into the square, one of them
will have to avoid the marked points. This is impossible for a box with 0◦ orientation.

2), ( 1
, s

, 1), ( 3
2

2 + s

− s
4

4

The interior sloping lines now have length

10
9 , but their components in the direction
of a 45◦ unit vector are at most 1, so Lemma 7 applies to the triangles in the ﬁgure. It
follows that a 45◦ box that avoids the points must be (up to symmetry) in approximately
the position shown in Figure 13. This box must contain three points like those marked
“A” in Figure 14, but now they have these coordinates:

q

8
><

>:

A =

(1, s − 3) ≈ (1, .886)
( s
2
(1.5, 1.3)

, s − 3) ≈ (1.943, .886)

the electronic journal of combinatorics 10 (2003), #R8

10

The other nine points in Figure 14 become

s

s

2

) ≈ (3.086, 1.943)

, s − .8) ≈ (1.943, 3.086)

B = (s − 1, 1) ≈ (2.886, 1)
C = (s − .8,
D = (s − 1, s − 1) ≈ (2.886, 2.886)
E = (
F = (1, s − 1) ≈ (1, 2.886)
G = (.8, s − 2) ≈ (.8, 1.886)
H = (1.7, 2.2)
I = (2.2, 2.2)
J = (2.2, 1.7).

2

Again these 12 points form an unavoidable set in the context of 45◦ packings, and since
three of them are in one box, there cannot be 11 nonintersecting boxes. This completes
2
the proof of Theorem 3 and establishes the truth of Martin Gardner’s conjecture.

References

1. Erich Friedman, “Packing Unit Squares in Squares: A Survey and New Results,”

The Electronic Journal of Combinatorics 7 (2002), Dynamic Survey DS#7.

2. Pertti H¨am¨al¨ainen, correspondence, April 20, 1980.

3. Michael J. Kearney and Peter Shiu, “Eﬃcient packing of unit squares in a square,”

The Electronic Journal of Combinatorics 9 (2002), #R14.

4. Walter Stromquist, “Packing unit squares inside squares, I (six unit squares),”

Daniel H. Wagner, Associates Memorandum, September 11, 1984

5. ——, “Packing unit squares inside squares, II (ten unit squares),” DHWA Memo-

randum, October 15, 1984.

6. ——, “Packing unit squares inside squares, III (Cases with n ≤ 65 and Martin
Gardner’s conjecture for n = 11),” DHWA Memorandum, November 15, 1984.

7. Martin Gardner, “Mathematical Games” in Scientiﬁc American, October 1979. (See

also November 1979, March 1980, and November 1980.)

the electronic journal of combinatorics 10 (2003), #R8

11

