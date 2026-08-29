On optimal piercing of a square

Bojan Baˇsi´c, Anna Slivkov´a
Department of Mathematics and Informatics, University of Novi Sad,

Trg Dositeja Obradovi´ca 4, 21000 Novi Sad, Serbia

bojan.basic@dmi.uns.ac.rs, anna.slivkova@dmi.uns.ac.rs

Abstract

We treat the following problem: given an n × n square ABCD,
determine the minimum number of points that need to be chosen inside
the square ABCD such that there does not exist a unit square inside
the square ABCD containing none of the chosen points in its interior.
In other words, we are interested to know how to most eﬃciently
“destroy” a square-shaped object of side length n, where “destroying”
is achieved by piercing as few as possible small holes, and the square
is considered “destroyed” if no unpierced square piece of unit side
length can be salvaged. This problem actually belongs to the family
of problems centered about the so-called piercing number : indeed, if
Un denotes the collection of all open unit squares that can be ﬁtted
inside a given n × n square, the value that we are looking for is the
piercing number of the collection Un, denoted by π(Un). We show
that π(Un) = n2 when n (cid:54) 7, and give an upper bound for π(Un) that
is asymptotically equal to 2√
n2, which we believe is asymptotically
3
tight. We then generalize our reasoning in order to obtain a similar
upper bound when ABCD is a rectangle, as well as an upper bound for
π(Ux) when x is not necessarily an integer. Finally, we show that our
results have an application to the problem of packing a given number
of unit squares in the smallest possible square; it turns out that our
results present a general “framework” based on which we are able to
reprove many results on the mentioned problem (originally obtained
independently of each other) and also obtain a new result on packing
61 unit squares.

Mathematics Subject Classiﬁcation (2010): 52C35, 52A35, 52C15,

05B40

Keywords: unit square, piercing, puncturing, packing, arrange-

ment of points

1

1

Introduction

There are several lines of research concerning arrangements of unit squares
with respect to a larger square, such as packing n unit squares in the small-
est possible square [11], or covering the largest possible square with n unit
squares [12]. There are also several lines of research concerning arrangements
of points inside a given square, such as the problem initiated by Moser [18]
to ﬁnd how large the minimum distance determined by n points in a unit
square can be (which is today often researched in its equivalent form of pack-
ing circles in a square [3, Section D1] [23]) or the problem of determining the
area of the largest convex region not containing in its interior any of n points
chosen in a unit square [19, 21].

We hereby study a problem that presents a kind of interplay between
these two classes of problems. In fact, it belongs to a (quite general) family
of problems centered about the so-called piercing number. Namely, given a
collection of ﬁgures F in the Euclidean plane (or, more generally, space),
the piercing number of F , denoted by π(F ), is deﬁned as the minimum
number of points that need to be chosen in such a way that each ﬁgure
from F contains at least one of the chosen points (in other words, how
many “needles” are required to pierce all members of F ). One of the ﬁrst
questions of this kind was asked by Gallai [10, Section III.13]: determine
the smallest integer k such that, given any family of circular disks in the
plane where every two of them have a common point, there exists a set of
k points such that each disk contains at least one of those points; in other
words, the value that is asked for equals supF π(F ), where F ranges over
all the described families of disks. (It is now known that the answer is k = 4,
where the lower bound is due to Gr¨unabum [14], while a proof of the upper
bound had been announced by Danzer in 1954, though the ﬁrst published
proof is due to Stach´o [22]; Danzer himself published [5] a proof in 1986,
though this is not his original proof.) Various other problems of this kind
have been investigated: when the space is d-dimensional, when all the disks
are congruent, when the family consists of translates/homothethic images of
a given (usually convex) ﬁgure etc. (We mention, for example, the result of
Karasev [16], who proved that 3 points are always suﬃcient, and sometimes
necessary, to pierce any family of translates of a compact convex set in the
plane, any two of which have nonempty intersection.) These problem are
usually called Gallai-type problems. A further family of problems that has
attracted quite a lot of attention is the family of the so-called (p, q)-problems.

2

They ask for piercing numbers of ﬁnite families of sets in the d-dimensional
space, such that among every p members of the family there exist q of them
with a nonempty intersection. One of the most important results for this class
of problems is proved by Alon and Kleitman [1], who showed that, whenever
p, q and d are ﬁxed and p (cid:62) q (cid:62) d + 1, then π(F ) has an upper bound
depending only on (p, q, d). However, exact values of supF π(F ) (for ﬁxed
p, q, d) are known only in some very special cases. Apart from d = 1, when
it is known that p + q − 1 are always suﬃcient and sometimes necessary to
pierce F (proved by Hadwiger and Debrunner [15], in the paper where this
family of problems has actually been introduced), even for (p, q, d) = (4, 3, 2)
it is only known that the supremum is bounded below by 3 (see [4]) and
above by 13 (see [17]). For more information about problems related to the
piercing number, see the surveys [6, 8, 7].

We treat the following problem: given an n × n square ABCD, determine
the minimum number of points that need to be chosen inside the square
ABCD such that there does not exist a unit square inside the square ABCD
containing none of the chosen points in its interior. In other words, if Un
denotes the collection of all open unit squares that can be ﬁtted inside a
given n × n square, we are looking for the value π(Un). The problem can
also be presented in the following way: we are interested to know how to
most eﬃciently “destroy” a square-shaped object of side length n, where
“destroying” is achieved by piercing as few as possible small holes, and the
square is considered “destroyed” if no unpierced square piece of unit side
length can be salvaged. Stated like this, it seems that this problem is quite
applicable in real life. Furthermore, as it will turn out, it also has a direct
application to the already mentioned research problem of packing n unit
squares in the smallest possible square.

The work is divided into sections as follows. In Section 2 we show that
for n ∈ N, n (cid:54) 4, we have π(Un) = n2 (note that n2 is a trivial lower bound
for π(Un), and thus we only need to prove that π(Un) (cid:54) n2). In Section
3 we prove an upper bound for π(Un) asymptotically equal to 2√
n2. Our
3
upper bound actually matches the lower bound n2 for n (cid:54) 7, and thus we
get a corollary that for n (cid:54) 7 we have π(Un) = n2. (This in fact includes the
results from Section 2 as a special case. However, in Section 3 we actually
use some parts of the proof from Section 2, while the construction given
in Section 2 is much more natural and thus we believe that the underlying
idea is simpler to understand if seen on that construction ﬁrst.) In Section

3

4 we show how the upper bound from Section 3 can be easily generalized
to the case when ABCD is a rectangle; we then modify the upper bound
from Section 3 in order to obtain an upper bound for π(Ux) when x is not
necessarily an integer. In Section 5 we show that our results enable us to
reproduce, as a direct consequence, some known results on the square packing
problem (among which is a result that the smallest square in which 46 unit
squares can be packed is the square of side length 7, which has been proved
only recently [2]), and further obtain a new result on packing 61 unit squares.
Finally, in the last section we state a conjecture about asymptotical tightness
of our upper bound for π(Un).

Our techniques remind of some ideas often used in the context of “un-
avoidable points,” a notion developed by Friedman [11] in relation to the
square packing problem; in fact, some of our proofs can be a little bit short-
ened by appealing to some lemmas from there. We instead choose to write
the paper in a completely self-contained way.

2 The case n (cid:54) 4

The construction that proves the case n (cid:54) 4 is actually quite natural, al-
though the proof becomes somewhat technical at some points.

Theorem 1. For n (cid:54) 4, π(Un) = n2.

Proof. Since the n × n square can be divided into n2 interior-disjoint unit
squares, it is clear that π(Un) (cid:62) n2. Let us show that n2 points suﬃce. We
ﬁrst show this for n = 4.

Let the vertices A, B, C, D of the square ABCD have the coordinates
(0, 0), (4, 0), (4, 4) and (0, 4), respectively. We choose 16 points at the fol-
lowing coordinates:

(cid:18)

1 − ε + i

2 + 2ε
3

, 1 − ε + j

(cid:19)

2 + 2ε
3

, 0 (cid:54) i, j (cid:54) 3,

where ε is going to be chosen later. That way, the chosen 16 points represent
a square lattice with the step 2+2ε
. Let P QRS be the square that bounds
this lattice (Figure 1).

3

We need to show that each unit square inside the square ABCD contains
at least one of the chosen points in its interior (for a suitable ε). Let us
ﬁrst consider a unit square whose center is inside the square P QRS. Notice

4

Figure 1: 16 points in 4 × 4 square.

2

3 =

that, for each point inside the square P QRS, there exists at least one of
the chosen 16 points at a distance from the observed point of no more than
√
√
2
2 · 2+2ε
3 (1 + ε). Therefore, if ε is small enough, each circle centered
inside the square P QRS with radius 1
2 contains at least one of the chosen 16
points, and thus the same clearly holds for any unit square whose center is
inside the square P QRS.

Let us now consider unit squares whose center is not inside the square
P QRS. Suppose that we have such a square that does not contain any of
the chosen 16 points in its interior. We can, w.l.o.g., assume that one of the
following two cases holds:

• two neighboring edges of the considered unit square contain one of the
chosen 16 points each, and in fact ones from the edges of the square
P QRS (Figure 2 left);

• two neighboring vertices of the considered unit square belong to two

neighboring edges of the square ABCD (Figure 2 right).

5

Figure 2: The two possible cases.

Let us ﬁrst deal with the former case. Let KHLG be a unit square and
let its sides HL and HK contain the points P and J (these are two of the
chosen 16 points, from the edges of the square P QRS), respectively. Denote
∠HP J = θ (we can assume θ (cid:54) 45◦). Let M be the foot of the perpendicular
from H to P J, and let H0 be the foot of the perpendicular from G to the
line HM . We shall prove that the vertex G is outside the square ABCD; it
is enough to show HH0 > (1 − ε) + M H. Since also ∠JHM = θ, we evaluate

M H = JH cos θ = JP sin θ cos θ =

2 + 2ε
3

sin θ cos θ.

Further, we have ∠GHH0 = 45◦ − ∠JHM = 45◦ − θ, from which follows
√

HH0 = HG cos ∠GHH0 =

2 · cos(45◦ − θ)

√

=

2(cos 45◦ cos θ + sin 45◦ sin θ) = cos θ + sin θ.

Therefore, we actually need to prove the inequality

cos θ + sin θ − (1 − ε) −

2 + 2ε
3

sin θ cos θ > 0.

(1)

6

Notice that:

cos θ + sin θ − (1 − ε) −

2 + 2ε
3

sin θ cos θ

= cos θ + sin θ − (1 − ε) −

= cos θ + sin θ −

2 − 4ε
3

−

1 + ε
3
1 + ε
3

(sin2 θ + 2 sin θ cos θ + cos2 θ) +

1 + ε
3

(sin θ + cos θ)2.

Zeros of the quadratic function

f (x) = −

1 + ε
3

x2 + x −

2 − 4ε
3

are

x1,2 =

(cid:113)

−1 ±

1 − 4 · 1+ε
3

· 2−4ε
3

−2 · 1+ε
3

√

16ε2 + 8ε + 1

−2(1 + ε)

−3 ±

=

=

3 ∓ (4ε + 1)
2(1 + ε)

,

−3 ± (cid:112)9 − 4(2 − 2ε − 4ε2)
−2(1 + ε)

=

that is, the function f is positive for x ∈ (cid:0) 1−2ε
we have sin θ + cos θ < 2 and sin θ + cos θ (cid:62) sin2 θ + cos2 θ = 1 > 1−2ε
completes the proof in the ﬁrst case.

1+ε , 2(cid:1). Since for 0 (cid:54) θ (cid:54) 45◦
1+ε , this

Let us now consider the second case. Let AK = a, AG = b (where
a2 + b2 = 1). The equation of the line GL is y = a
b x + b. Consider the
perpendicular from the point (1, 1) to the line GL. The equation of this
ax+1+ b
perpendicular is y = − b
a. Solving the system of the last two equations
gives x = 1+ b
a −b
a2+b2 = ab + b2 − ab2 and y = a
b (ab + b2 − ab2) + b =
b + b
a2 + ab − a2b + b, that is, the considered perpendicular intersects the line GL
at the point T with the coordinates (ab + b2 − ab2, a2 + ab − a2b + b). We
claim that GT < 1. Indeed,

= (a+b−ab)b

a

a

2

GT

= (a2 + ab − a2b)2 + (ab + b2 − ab2)2

= a2(a + b − ab)2 + b2(a + b − ab)2 = (a + b − ab)2(a2 + b2)

= (a + b − ab)2;

7

therefore, we need to prove a + b − ab < 1, that is, (1 − a)(1 − b) > 0, which
is clearly true.

From GT < 1 we get that the point (1, 1) lies in the interior of the square

KHLG, and therefore so does the point P , a contradiction.

This completes the proof for n = 4. For n < 4 it is enough to take any
n × n square inside the square in Figure 1 containing n2 of the chosen 16
(cid:4)
points in its interior.

3 An upper bound

Let us now reﬁne the methods from the previous section in order to obtain
an upper bound that we believe is quite strong. We ﬁrst prove a lemma that
will be useful.

Lemma 2. Let the points U and V be chosen on two neighboring edges, say
GK and GL, of a unit square KHLG, such that U V < 1. Let W be the third
vertex of the equilateral triangle U V W , where the point W is on the same
side of the line U V as the point H. Then the point W lies in the interior of
the square KHLG.

Proof. It is enough to show that the point W is in the same open halfplanes
as the points V and U with respect to the lines KH and LH, respectively
(Figure 3). And indeed, this directly follows from the observations V W < 1
(cid:4)
and U W < 1, respectively.

Figure 3: Picture for Lemma 2.

8

Let us now show the main result of this section.

Theorem 3. For any n ∈ N,

π(Un) (cid:54) n

(cid:18)(cid:24) 2
√
3

√

(n + 1 − 2

(cid:25)

(cid:19)

2)

+ 1

.

(2)

Proof. Let the vertices A, B, C, D of the square ABCD have the coordinates
(0, 0), (n, 0), (n, n) and (0, n), respectively. We shall ﬁrst place an equilateral
triangular lattice in the square ABCD, as sketched in Figure 4.

Figure 4: Equilateral triangular lattice.

The lattice is deﬁned as follows:

i) the side length of the equilateral triangle that generates this lattice is

1 − δ, where δ is a small enough positive number;

ii) the bottom left point is at the coordinates ( 3
4,

4 here
is not really important, the proof would be completely the same for any
number from the interval ( 1
2, 1); on the other hand, the motivation for

2) (the value 3

2 − 1

√

9

√

2 − 1

2 comes from the fact that this is the largest number
the value
such that the inequality (4) further in the proof holds for all δ > 0 and
0 (cid:54) θ (cid:54) 45◦);

iii) all the points in the bottom “row” are on a line parallel to the x-axis

(and the same holds for further rows);

iv) the number of rows is determined so that the y-coordinate of the points

in the top row is greater than or equal to n − (

√

2 − 1

2).

To state it in a more formal (but possibly less clear) way: we arrange

points in a total of

+ 1 rows (the number of rows follows from

(cid:108) n−2(

√

2− 1
2 )

(cid:109)

√
3
2 (1−δ)

the requirements ii) and iv) and the fact that the distance between two
2 (1 − δ)); in the jth row from the bottom there are
successive rows equals
n points having the coordinates

√

3

(cid:16) 3
4

+ i(1 − δ),

√

2 −

1
2

+ (j − 1)

√

3
2

(cid:17)

(1 − δ)

, 0 (cid:54) i (cid:54) n − 1

if j is odd, and

(cid:16) 3
4

−

1 − δ
2

+ i(1 − δ),

√

2 −

1
2

+ (j − 1)

√
3
2

(cid:17)

(1 − δ)

, 0 (cid:54) i (cid:54) n − 1

if j is even.

Since lim
δ→0

we have

√

2− 1
2 )

n−2(
√
3
2 (1−δ)

= 2√
3

√

(n + 1 − 2

2), which is clearly not an integer,

(cid:32)(cid:38)

√

2 − 1
2)
n − 2(
√
3
2 (1 − δ)

lim
δ→0

(cid:39)

(cid:33)

+ 1

=

(cid:24) 2
√
3

√

(n + 1 − 2

2)

(cid:25)

+ 1.

(3)

3

√

(n + 1 − 2

Therefore, for δ small enough, the total number of chosen points equals
n(cid:0)(cid:6) 2√
2)(cid:7) + 1(cid:1) (note that this is precisely the right-hand side of
(2)). Also note that, for δ small enough, if further points were added to any
of the rows (following the same pattern), they would be outside the square
ABCD. Let us show that there indeed does not exist a unit square inside
the square ABCD containing none of the chosen points in its interior.

Suppose the opposite:

let KHLG be a unit square inside the square
ABCD such that none of the chosen points are in its interior. We can,
w.l.o.g., assume that one of the following three cases holds:

10

• two neighboring edges of the square KHLG contain one of the chosen
points each, where both of these points simultaneously belong to the
bottom or to the top row;

• two neighboring edges of the square KHLG contain one of the chosen
points each, where not both of these points simultaneously belong to
the bottom or to the top row;

• two neighboring vertices of the square KHLG, say K and G, belong
to two neighboring edges of the square ABCD, and furthermore, the
one of the chosen points that is in the relevant corner lies between the
lines KH and GL.

The third case may need some explanation. By “the one of the chosen points
that is in the relevant corner” we mean the following: the “relevant corner”
is the one where the two edges of the square ABCD on which the points K
and G lie meet (e.g., if K ∈ AB and G ∈ AD, then the “relevant corner” is
bottom-left); the point that is required to be between the lines KH and GL
is the leftmost or the rightmost point in the bottom or the top row, whichever
of these is determined by the “relevant corner” (e.g., if the “relevant corner”
is top-left, then the leftmost point in the top row should be between the lines
KH and GL). Note that we can indeed assume this additional constraint
in the third case, since if it does not hold, then the square KHLG can be
moved to fall under one of the ﬁrst two cases.

Having the deﬁnition of the third case cleared, we note that it leads to
a contradiction in the same way as in the corresponding part in Theorem 1
(the one that is shown in Figure 2 right), verbatim. Assume now the second
case. Let U and V be two of the chosen points such that U ∈ GK, V ∈ GL.
By Lemma 2, the third vertex W of the equilateral triangle U V W lies in the
interior of the square KHLG. However, we note that the point W is either
also one of the chosen points, or lies outside the square ABCD (the latter
possibility could happen if U and V are the leftmost or the rightmost points
of two consecutive rows; we here recall that δ could be arbitrarily small).
One way or another, we reach a contradiction. That leaves only the ﬁrst
case.

Note that, in the ﬁrst case, if the center of the square KHLG is in the
strip between the bottom and the top row, we reach a contradiction in the
same way as in the second case. Therefore, assume that the center of the
square KHLG lies below the bottom or above the top row. We shall follow

11

the lines of thought from Theorem 1 (we here have the picture that is like
the one shown in Figure 2 left). We evaluate

M H = JP sin θ cos θ = (1 − δ) sin θ cos θ;

HH0 = cos θ + sin θ.

Therefore, the inequality corresponding to (1) (that we need to prove) is

cos θ + sin θ −

(cid:18)√

2 −

(cid:19)

1
2

− (1 − δ) sin θ cos θ > 0.

(4)

Notice that:

cos θ + sin θ −

(cid:18)√

2 −

(cid:19)

1
2

− (1 − δ) sin θ cos θ

= cos θ + sin θ −

(cid:18)√

2 −

(cid:19)

1
2

−

1 − δ
2
(cid:18)√

(sin2 θ + 2 sin θ cos θ + cos2 θ) +

2 − 1 +

(cid:19)

δ
2

−

1 − δ
2

(sin θ + cos θ)2,

1 − δ
2

= cos θ + sin θ −

We know cos θ+sin θ (cid:62) 1 (because θ is nonnegative). Let us check what is the
maximal possible value of cos θ + sin θ. Since (cos θ + sin θ)(cid:48) = − sin θ + cos θ,
equating this with 0 shows that the extrema are reached for θ = ± π
4 = ±45◦;
in particular, the local maximum (which is also the global maximum) is
reached for θ = 45◦ (which indeed satisﬁes our constraint θ (cid:54) 45◦) and
2, and since the quadratic
equals
function

2. Therefore, since 1 (cid:54) cos θ + sin θ (cid:54)

√

√

g(x) = −

x2 + x −

2 − 1 +

(cid:18)√

1 − δ
2

(cid:19)

δ
2

has negative leading coeﬃcient, in order to ﬁnish the proof it is enough to
2) > 0. And indeed:
check that g(1) > 0 and g(

√

g(1) = −

√

g(

2) = −

1 − δ
2

1 − δ
2

+ 1 −

√

2 + 1 −

δ
2

=

√

2 −

· 2 +

√

2 + 1 −

3
2

δ
2

√

−

2 > 0;

=

δ
2

> 0.

This completes the proof.

(cid:4)

12

10
4
n
110
16
upper bound
20
14
n
upper bound 132 156 182 224 255 288 323 360 399 440

7
49
17

6
36
16

5
25
15

9
90
19

8
72
18

1
1
11

2
4
12

3
9
13

Table 1: Upper bounds for π(Un) for n (cid:54) 20.

The exact upper bounds from Theorem 3 for n (cid:54) 20 are calculated in

Table 1. These values give the following corollary.

Corollary 4. For n (cid:54) 7,

π(Un) = n2.

4 Some versions of the problem

We here mention some versions of the problem for which the results follow
by slight alterations of the reasoning presented so far.

First, we can ask the same questions for rectangles ABCD instead of
squares. Let Um,n denote the collection of all open unit squares than can be
ﬁtted inside a given m × n rectangle. Then π(Um,n) stands for the minimum
number of points that need to be chosen inside an m×n rectangle ABCD such
that there does not exist a unit square inside the rectangle ABCD containing
none of the chosen points in its interior. A straightforward modiﬁcation of
the proof of Theorem 3 gives the following result.

Theorem 5. For each m, n ∈ N,

π(Um,n)

(cid:54) min

(cid:26)

m

(cid:18)(cid:24) 2
√
3

√

(n + 1 − 2

(cid:25)

(cid:19)

2)

+ 1

, n

(cid:18)(cid:24) 2
√
3

√

(m + 1 − 2

(cid:25)

(cid:19)(cid:27)

2)

+ 1

.

Of course, the lower bound for π(Um,n) is mn. Since (cid:6) 2√

2)(cid:7) +
1 = n for each n (cid:54) 7, we have an interesting corollary that this lower bound
is matched for all the rectangles whose one side is of length at most 7, no
matter how long the other side is! In other words:

(n + 1 − 2

3

√

13

Corollary 6. If min{m, n} (cid:54) 7, then

π(Um,n) = mn.

Let us now ﬁnd an upper bound for π(Ux) when x is not necessarily an

integer.

Theorem 7. For any x > 0,

π(Ux) (cid:54)






(cid:98)x(cid:99)

(cid:18)(cid:22) 2
√
3

√

(x + 1 − 2

(cid:23)

(cid:19)

2)

+ 2

,

if {x} <

1
2

;

(cid:98)x(cid:99)

(cid:18)(cid:22) 2
√
3

√

(x + 1 − 2

(cid:23)

(cid:19)

2)

+ 2

+

(cid:106) 2√

3






√

(x + 1 − 2

2

(cid:107)

2)

+ 2




,

if {x} (cid:62) 1
2

.

(Hereby {x} denotes the fractional part of x, that is, {x} = x − (cid:98)x(cid:99).)

Proof. The proof is basically the same as the proof of Theorem 3. We high-
light only the necessary modiﬁcations.

√

2 − 1

2), where c is chosen so that c > 1

2 , which is, for δ small enough, smaller than 1

We construct an equilateral triangular lattice with the step 1 − δ as in
the proof of Theorem 3, but with the bottom left point at the coordinates
2 and {x} < c < 1. Therefore,
(c,
for δ small enough, the ﬁrst row, as well as all the odd rows, consist of (cid:98)x(cid:99)
points. The leftmost point in the second row has the x-coordinate equal to
c − 1−δ
2 but can be arbitrarily
close to 1
2 (since c can be chosen arbitrarily close to 1). Therefore, if δ is
small enough and c is close to 1, the x-coordinates of the ﬁrst (cid:98)x(cid:99) points from
the second row are in the intervals (i, i + 1
2), where i ranges from 0 to (cid:98)x(cid:99) − 1,
and actually can be made arbitrarily close to i + 1
2. These are actually all
points from the second row if and only if x − ((cid:98)x(cid:99) − 1 + 1
2) < 1, that is, if and
only if {x} < 1
2; otherwise, the second row has one more point. The same
holds for the fourth, the sixth etc., that is, for all even rows. Altogether, if d
denotes the number of rows, the total number of chosen points equals (cid:98)x(cid:99)d
if {x} < 1
2 (d rows
with (cid:98)x(cid:99) points each, plus one additional point in each of (cid:98) d

2 (d rows with (cid:98)x(cid:99) points each), and (cid:98)x(cid:99)d + (cid:98) d

2 (cid:99) if {x} (cid:62) 1
2 (cid:99) rows).

14

√

√

2√
3

(x + 1 − 2

(x + 1 − 2

2) is not an integer, but equals (cid:6) 2√

That leaves only to calculate d, the number of rows. As in (3), we have
2)(cid:7) + 1
that, for δ small enough, the number of rows equals (cid:6) 2√
2)(cid:7) + 2 if
if
2√
2) is an integer. These two formulas actually can be uniﬁed by
3
concluding that the number of rows equals (cid:4) 2√
2)(cid:5) + 2. Together
with the conclusion at the end of the previous paragraph, we are now able
to calculate the total number points, which gives exactly the upper bound
(cid:4)
from the statement of the theorem.

(x + 1 − 2
√

(x + 1 − 2

(x + 1 − 2

√

√

3

3

3

5 An application to the square packing prob-

lem

√

let s(n) denote the side length of the smallest
For a positive integer n,
square into which n unit squares can be packed. Trivial bounds for s(n)
n(cid:101). The cases in which the exact values of s(n) are
are
known, and some bounds for other cases, are summarized in a dynamic sur-
vey by Friedman [11].

n (cid:54) s(n) (cid:54) (cid:100)

√

The following proposition makes a connection between our problem and

the square packing problem.
Proposition 8. For any x > 0, no more than π(Ux) unit squares can be
packed in a square of side length x.
Proof. Let a square of side length x be given. Choose π(Ux) points in its
interior such that there does not exist a unit square inside the given square
containing none of the chosen points in its interior. Therefore, if more than
π(Ux) unit squares were packed inside the given square, there would exist
two of them containing in their interiors the same point among the chosen
π(Ux) points, that is, their interiors would have a nonempty intersection,
(cid:4)
which is a contradiction.

In other words, the proposition states

s(π(Ux) + 1) > x

(5)

for any x > 0. This inequality can be used to reprove the following results.

Theorem 9. The values of s(n) for some values of n are as given in Table
2.

15

s(n) originally proved by
n
8
3
15 4
23 5
24 5
34 6

Bajm´oczy, by [13]
El Moumni [9]
Nagamochi [20]
Friedman [11]
Nagamochi [20]

n
35 6
46 7
47 7
48 7

s(n) originally proved by
Friedman [11]
Bentz [2]
Nagamochi [20]
Nagamochi [20]

Table 2: Values of s(n) proved in Theorem 9.

Proof. We show only s(46) = 7. The other proofs are completely analogous.

For each small enough ε > 0 we evaluate

and

(cid:98)7 − ε(cid:99) = 6

((7 − ε) + 1 − 2

√

(cid:23)

2)

= 5.

(cid:22) 2
√
3

Therefore, Theorem 7 now enables us to evaluate

π(U7−ε) (cid:54) 6 · (5 + 2) +

(cid:23)

(cid:22) 5 + 2
2

= 42 + 3 = 45.

The function s is nondecreasing, and thus (5) gives

s(46) = s(45 + 1) (cid:62) s(π(U7−ε) + 1) > 7 − ε.

Since the above inequality holds for each small enough ε > 0, we deduce

s(46) (cid:62) 7.

On the other hand, 46 unit squares can be easily packed in a square of side
(cid:4)
length 7. This proves s(46) = 7.

Finally, for those values of n for which no exact value of s(n) is known,
obtaining some (nontrivial) upper and lower bounds on it is an interesting
research direction. The list of the best known such bounds is compiled in the
already mentioned survey [11]. By the approach from the present paper, we
were able to improve the lower bound for s(61) (until now no nontrivial lower
bound on s(61), that is, better than s(61) (cid:62)

61 ≈ 7.8102, was known).

√

16

Theorem 10. We have

√
s(61) (cid:62) 7

2

√

3

+ 2

2 − 1 ≈ 7.8906.

Proof. The idea is the same as in the proof of the previous theorem. For
each small enough ε > 0 we evaluate

(cid:36)

√
7

3

2

√

+ 2

(cid:37)

2 − 1 − ε

= 7

and
(cid:36)

2
√
3

(cid:32)(cid:32)

√
7

3

2

which leads to

√

+ 2

2 − 1 − ε

(cid:33)

√

+ 1 − 2

(cid:36)

(cid:33)(cid:37)
2

=

(cid:32)

√
3
7

2

2
√
3

(cid:33)(cid:37)

− ε

= 6,

π(U 7

√

√
3
2 +2

2−1−ε) (cid:54) 7 · (6 + 2) +
√

√
This implies s(61) (cid:62) 7
3
2 + 2
theorem.

2 − 1 in the same way as in the previous
(cid:4)

(cid:23)

(cid:22) 6 + 2
2

= 56 + 4 = 60.

6 A conjecture about asymptotical tightness

For the end, let us say that, though exact formula for π(Un) (or π(Ux)) may
not be easy to ﬁnd, we believe that the upper bound (2) is asymptotically
tight.

Conjecture. For n → ∞, we have

π(Un) ∼

2
√
3

n2.

Acknowledgments

The authors would like to thank the anonymous referee for valuable com-
ments, which helped to improve the content of the paper.

The ﬁrst author was supported by the project 174006 of the Ministry of
Education, Science and Technological Development of Serbia, and the second
author by the project 174013 of the same Ministry.

17

References

[1] N. Alon & D. J. Kleitman, Piercing convex sets and the Hadwiger-

Debrunner (p, q)-problem, Adv. Math. 96 (1992), 103–112.

[2] W. Bentz, Optimal packings of 13 and 46 unit squares in a square,

Electron. J. Combin. 17 (2010), Research Paper #R126, 11 pp.

[3] H. T. Croft & K. J. Falconer & R. K. Guy, Unsolved Problems in Ge-

ometry, Springer-Verlag, New York, 1994.

[4] L. Danzer, Ungel¨oste Probleme, Nachtrag zu Nr. 15, Elem. Math. 12

(1957), 62.

[5] L. Danzer, Zur L¨osung des Gallaischen Problems ¨uber Kreisscheiben in
der euklidischen Ebene, Studia Sci. Math. Hungar. 21 (1986), 111–134.

[6] L. Danzer & B. Gr¨unbaum & V. Klee, Helly’s theorem and its relatives,
in: V. Klee (ed.), Convexity, American Mathematical Society, Provi-
dence, Rhode Island, 1963, pp. 101–180.

[7] J. Eckhoﬀ, A survey of the Hadwiger-Debrunner (p, q)-problem,

in:
B. Aronov & S. Basu & J. Pach & M. Sharir (eds.), Discrete and Compu-
tational Geometry: The Goodman-Pollack Festschrift, Springer-Verlag,
Berlin, 2003, pp. 347–377.

[8] J. Eckhoﬀ, Helly, Radon, and Carath´eodory type theorems,

in:
P. M. Gruber & J. M. Wills (eds.), Handbook of Convex Geometry,
Vol. A, North-Holland, Amsterdam, 1993, pp. 389–448.

[9] S. El Moumni, Optimal packings of unit squares in a square, Studia Sci.

Math. Hungar. 35 (1999), 281–290.

[10] L. Fejes T´oth, Lagerungen in der Ebene, auf der Kugel und im Raum,

Springer-Verlag, Berlin, 1953.

[11] E. Friedman, Packing unit squares in squares: a survey and new results,

Electron. J. Combin., Dynamic Survey #DS7.

[12] E. Friedman & D. A. Paterson, Covering squares with unit squares,

Geombinatorics 15 (2006), 130–137.

18

[13] F. G¨obel, Geometrical packing and covering problems, in: A. Schrijver
(ed.), Packing and Covering in Combinatorics, Mathematisch Centrum,
Amsterdam, 1979, pp. 179–199.

[14] B. Gr¨unbaum, On intersections of similar sets, Portugal. Math. 18

(1959), 155–164.

[15] H. Hadwiger & H. Debrunner, ¨Uber eine Variante zum Hellyschen Satz,

Arch. Math. (Basel) 8 (1957), 309–313.

[16] R. N. Karasev, Transversals for families of translates of a two-
dimensional convex compact set, Discrete Comput. Geom. 24 (2000),
345–353.

[17] D. J. Kleitman & A. Gy´arf´as & G. T´oth, Convex sets in the plane with

three of every four meeting, Combinatorica 21 (2001), 221–232.

[18] L. Moser, Problem 24, Canad. Math. Bull. 3 (1960), 78.

[19] W. O. J. Moser, Problems on extremal properties of a ﬁnite set of
points, in: J. E. Goodman, & E. Lutwak & J. Malkevitch & R. Pol-
lack (eds.), Discrete Geometry and Convexity, Ann. New York Acad.
Sci. 440 (1985), pp. 52–64.

[20] H. Nagamochi, Packing Unit Squares in a Rectangle, Elect. J. Comb.

12 (2005), Research Paper #R37, 13 pp.

[21] J. Pach & G. Tardos, Piercing quasi-rectangles—on a problem of Danzer

and Rogers, J. Combin. Theory Ser. A 119 (2012), 1391–1397.

[22] L. Stach´o, A Gallai-f´ele k¨orlet¨uz´esi probl´ema megold´asa, Mat. Lapok 32

(1981/84), 19–47.

[23] P. G. Szab´o & M. Cs. Mark´ot & T. Csendes & E. Specht & L. G. Casado
& I. Garc´ıa, New Approaches to Circle Packing in a Square, Springer,
New York, 2007.

19

