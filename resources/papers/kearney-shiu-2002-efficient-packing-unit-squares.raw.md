E(cid:14)cient packing of unit squares in a square

Michael J Kearney and Peter Shiu
Department of Electronic and Electrical Engineering, Loughborough University
Loughborough, Leicestershire LE11 3TU, United Kingdom
M.J.Kearney@lboro.ac.uk
Department of Mathematical Sciences, Loughborough University
Loughborough, Leicestershire LE11 3TU, United Kingdom
P.Shiu@lboro.ac.uk

Submitted: June 1, 2001; Accepted: February 11, 2002.
MR Subject Classi(cid:12)cations: 05B40, 52C15

Abstract
Let s(N ) denote the edge length of the smallest square in which one can pack
N unit squares. A duality method is introduced to prove that s(6) = s(7) = 3.
Let nr be the smallest integer n such that s(n2 + 1) (cid:20) n + 1=r. We use an
explicit construction to show that nr (cid:20) 27r3=2 + O(r2), and also that n2 (cid:20) 43.

1. Introduction.

Erd}os and Graham [1] initiated the study of packing unit squares in a square by demon-
strating that non-trivial packings can result in a wasted area that is surprisingly small.
For a square with side length n + (cid:14), where n is an integer and 0 (cid:20) (cid:14) < 1, they showed
by explicit construction that it is possible to have a packing so e(cid:14)cient that the wasted
area is O(n7=11) for large n. By way of contrast, the ‘trivial’ packing of unit squares
gives a wasted area of (n + (cid:14))2 − n2 > 2(cid:14)n.

p

p

N (cid:20) s(N ) (cid:20) d

There is now the interesting optimisation problem of packing a given number N of
unit squares, especially when N is small, and we denote by s(N ) the side length of the
smallest square into which one can pack them. Then s(N ) is an increasing function with
s(n2) = n, so that
N e. The determination of s(N ) when N 6= n2 is
a rather di(cid:14)cult problem, with only a few values for s(N ) having been established for
such N . For example, it was conjectured that s(n2 − n) = n, but this is known to be
false for n (cid:21) 17 by an explicit construction; see the recent survey [2] by Friedman, who
paid special attention to s(N ) with N (cid:20) 100. There is a simple proof of the conjecture
when n = 2, that is s(2) = 2, but only claims for the proof of s(6) = 3 are reported
in [2]. Friedman [2] has proved that s(7) = 3, and we introduce a ‘duality’ method
in x2 which delivers a much simpli(cid:12)ed proof. Indeed, the method enables us to give a
reasonably short proof in x3 of
Theorem 1. We have s(6) = 3.

the electronic journal of combinatorics 9 (2002), #R14

1

The determination of s(n2 + 1) is particularly interesting, and we now set

(cid:0)

(cid:1)

(cid:14)n = s(n2 + 1) − n:
(n+1)2 +1

(1)
(cid:20) s(n2 +1)+1, which follows from the
We remark that (cid:14)n+1 (cid:20) (cid:14)n, that is s
consideration of adding 2n + 1 unit squares forming an ‘L’ round two sides of the square
for an existing packing. There is the trivial lower bound (cid:14)n (cid:21)
n2 + 1 − n (cid:24) 1=2n;
thus (cid:14)n > 1=3n and the result of Erd}os and Graham [1] implies that (cid:14)n (cid:28) n−4=11 as
n ! 1. We adopt a simpler version of their constructive argument in x5 to give a
slightly inferior bound, but one which is also valid for small values of n.
Theorem 2. For all n (cid:21) 1, we have

p

Only (cid:14)1 = 1 and (cid:14)2 = 1=

(cid:14)n <

3
(2n)1=3 +

3
(2n)2=3

:

p

2 have been determined; see [2] where the bounds

0(cid:1)5183 : : : (cid:20) (cid:14)3 (cid:20) 0(cid:1)7071 : : :

(2)

(3)

are also given. All the packings mentioned in [2] involve squares with side lengths having
fractional parts exceeding 1
2 . In x4 we use solutions to the Pell equation x2 + 1 = 2y2
to give a simple proof that if (cid:14) > 1
2 then there exists n such that (cid:14)n < (cid:14). In particular,
we show that (cid:14)8 < 0(cid:1)536 and (cid:14)42 < 0(cid:1)507, but the question still remains as to the
smallest n such that (cid:14)n (cid:20) 1
2 . By (cid:12)nding
certain simultaneous Diophantine approximations to real numbers in relation to our
construction we show in x6 that this can be further improved to

2 . The proof of Theorem 2 shows that (cid:14)55 < 1

(cid:14)43 < 1
2
p

:

(4)

p

In x4 we also apply such approximations to
2 to give a simple proof of the following
2, then there are in(cid:12)nitely many n such that
result: If (cid:14) > 1=
s(n2 +cn) < n+(cid:14). Although our results are inferior to that of Erd}os and Graham [1] for
large N , nevertheless it is instructive to apply number theory to give simple solutions
to such problems.

2 and 0 < c < 2(cid:14) −

p

Let nr be the smallest integer n such that (cid:14)n (cid:20) 1=r, so that estimates for (cid:14)n can
be converted to those for nr. Thus, by the result of Erd}os and Graham [1], we have
nr (cid:28) r11=4 as r ! 1, and our argument in the proof of Theorem 2 also gives the
following result which is valid also for small values of r.
Corollary. For r > 1, we have

(cid:16)h

nr (cid:20) p([(cid:28) ]) (cid:20) p

i(cid:17)

3r
2

=

27r3
2

+ O(r2);

where p(t) = 4t3 + 4t2 + 3t + 1 and (cid:28) is the real root of (cid:17)(t) = 1=r, with

(cid:17)(t) =

3
2t +

1
4t2

− 7

8t3 +

5
8t5

:

the electronic journal of combinatorics 9 (2002), #R14

(5)

2

From (3) and (4) we have 4 (cid:20) n2 (cid:20) 43, and it seems likely that both the bounds
are still some distance from the exact value. However, the e(cid:11)ort involved in establishing
s(6) = 3 indicates that it may be tedious to make substantial improvement on the lower
bound. Moreover, considering the extremely good simultaneous Diophantine approxi-
mations associated with our construction in x6, it appears to us that any improvement
on the upper estimate will require a very di(cid:11)erent arrangement for the unit squares
to ours. Thus to improve on these bounds represents an interesting challenge. Using
essentially the same ideas, we have also found that n3 (cid:20) 239, n4 (cid:20) 625, n5 (cid:20) 1320,
n6 (cid:20) 2493 and n7 (cid:20) 4072.

2. Proof of s(7) = 3.
We (cid:12)rst give our proof of s(7) = 3. Since s(7) (cid:20) s(32) = 3 it su(cid:14)ces to establish that
s(7) (cid:21) 3. Following Friedman [2], we use the notion of an unavoidable set of points in
a square S, namely a (cid:12)nite set of points so placed that any unit square inside S must
contain a member of the set, possibly on its boundary. If we now shrink the square S
together with the unavoidable set by a positive factor (cid:21) < 1, then any unit square
inside the shrinked square contains an unavoidable point in its interior. Consequently,
if a square S with side length k possesses an unavoidable set of N − 1 points then
s(N ) (cid:21) (cid:21)k for every (cid:21) < 1, and hence s(N ) (cid:21) k. For the sake of clarity of presentation,
we shall omit the shrinking factor (cid:21) in the following.

3

=

2

y

y

3=
2

=

1

y

3

=

x

-

2

1
2

x

3=
2

=

x

7 -
2

2

Figure 1. The set of 7 unavoidable points.

Friedman [2] showed that the centre point (1; 1) in [0; 2]2 is unavoidable, so that
s(2) = 2. By (cid:12)nding appropriate unavoidable sets he also proved that s(n2 − 1) = n
for n = 3; 4; 5; 6.
In particular, for the proof of s(8) = 3, Friedman constructed an
unavoidable set of 7 points, which are essentially the points

p

p

p

f(

2 − 1

2 ; 1); ( 3

2 ; 1); ( 7

2 −

2; 1); ( 3

2 ; 3

2 ); (

2 − 1

2 ; 2); ( 3

2 ; 2); ( 7

2 −

p

2; 2)g

(6)

3

the electronic journal of combinatorics 9 (2002), #R14

in the square S = [0; 3]2; see Figure 1. We omit the proof that these points form an
unavoidable set, since it is essentially that given by Friedman, who also gives a more
complicated proof for s(7) = 3 by considering an ‘almost unavoidable set’ with 5 points.
Our simpli(cid:12)ed proof makes use of a duality argument based on (6).

2 ; 3

We give the colour green to the 7 points in (6) and we say that the unavoidable set
forms a green lattice within S. Rotating this lattice by a right-angle about the centre
point ( 3
2 ), we obtain a red lattice with the corresponding 7 red points. With S being a
square, the red lattice also forms an unavoidable set, and we may consider it as the dual
of the green lattice. The two lattices have the common centre point ( 3
2 ), so that there
are 13 distinct points in their union. We also classify these 13 points into three types:
the centre point ( 3
2 ) will be called the C-point, the 8 points furthest away from the
C-point will be called the A-points, and the remaining 4 points having distance 1
2 from
the C-point are the B-points. Thus each lattice consists of four A-points, two B-points,
and the C-point; see Figure 2. Since each lattice forms an unavoidable set, any unit
square contained in S must cover at least one point from each lattice, and we remark
that the C-point is both green and red. For a packing, each point in S may be covered
by at most one unit square.

2 ; 3

2 ; 3

2=y

3=y
2

1=y

1

4

7

A

B

A

3

2

B

B

8

C

3

6

3

A

B

A

q

9

1=x

3=x
2

2=x

Figure 2. The union of two lattices of unavoidable points.

Lemma 1. Any unit square which covers the C-point must also cover a B-point.
Proof. Let the unit square have a diagonal speci(cid:12)ed by the points (0; 0) and (1; 1). By
symmetry, we may assume that the C-point has the coordinates (x0; y0) with 0 (cid:20) x0 (cid:20)
y0 (cid:20) 1
2 has the equation (x − x0)2 +
(y − y0)2 = 1

2 . The circle with centre the C-point and radius 1

4 , so that it intersects the edges of the unit square at the points

q

q

(x0 (cid:6)

1
4 − y2

0 ; 0);

(0; y0 (cid:6)

1
4 − x2

0 );

the electronic journal of combinatorics 9 (2002), #R14

4

with the two positive signs corresponding to two de(cid:12)nite points of intersection. The
0) = 1
square of the distance between these two points is at least x2
2 ,
which implies that the arc of the circle lying inside the unit square subtends an angle
which is at least a right-angle. Since the four B-points are equally spaced on the circle
it follows that the unit square must cover at least one B-point.

0)+y2

0 +( 1
4

0+( 1
4

In order to pack 7 unit squares into S = [0; 3]2, each square must cover exactly one
point in each lattice. Since the C-point belongs to both lattices, it follows at once from
Lemma 1 that S cannot have side length less than 3, so that s(7) = 3.

−x2

−y2

3. Proof of Theorem 1.
The proof of s(6) = 3 is more complicated. Each of the 6 unit squares to be packed in S
must cover at least one point from each lattice, so there is at most one unit square which
covers two points of the same lattice. If the C-point is not covered then each square
must cover precisely one point from each lattice, and we call this con(cid:12)guration (a). If the
C-point is covered by a unit square then, by Lemma 1, this square also covers a B-point,
which we may assume to be a green point by duality, and we call this con(cid:12)guration (b).
It remains to show that these two con(cid:12)gurations are impossible when S has side length
less than 3, because of the geometric constraints associated with the problem. We
shall require the following technical lemmas, the omitted proofs for which involve only
elementary coordinate geometry.
Lemma 2. Let U be a unit square with centre inside [0; 1]2. Suppose that one corner
of U touches the x-axis with an edge making an angle (cid:18), and that the point (0; 1) lies
on the opposite edge of U . Then the points

(cid:16)

1 + t2
1 + t

(cid:17)
;

; 1

(cid:16)

1; 1 + 2t − t2
2

(cid:17)
;

where

t = tan

;

(cid:18)

2

lie on two of the edges of the square.

Lemma 3. Let V be a unit square covering the point ( 3
points (1; 2), (2; 2) and (2; 3
intersects the line x = 1 at a height y (cid:20) 5
3 .

2 ), and suppose that the
2 ) lie on three of the edges of V . Then the remaining edge

2 ; 3

Concerning the coordinates displayed in Lemma 2, we remark that, for 0 (cid:20) t (cid:20) 1,

1 + t2
1 + t

p

(cid:21) 2

2 − 2;

1 + 2t − t2
2

(cid:21) 1
2

and

1 + t2
1 + t +

1 + 2t − t2
2

(cid:21) 3
2

:

(7)

We now apply Lemma 2 to deal with con(cid:12)guration (a), in which the C-point is not
covered, so that each of the 6 unit squares covers exactly one green point and one red
point. Take a unit square U which covers a green B-point, and we may assume that its
centre is located in region 8 in Figure 2. The square U must cover one of the adjacent
If U does not cover the point (1,1) then by
red A-points, the one in region 7, say.
Lemma 2 it intersects the line x = 2 in such a way that it is impossible to cover the red

the electronic journal of combinatorics 9 (2002), #R14

5

A-point in region 9 by a second unit square without also covering the red B-point in
region 6. To see this we apply Lemma 2 twice, with a rotation of the axis in the second
application, so that by the last inequality in (7), the minimum upper intercept on the
line x = 2 for the unit square concerned will have to be at least 3
2 . Elementary geometric
considerations show that any other positioning of the second square will increase the
intercept 3
2 . The same argument also shows that if U does cover the point (1,1) then any
unit square covering the green A-point in region 7 and the red B-point in region 4 will
intersect the line y = 2 in such a way that it is impossible to cover the green A-point in
region 1 without also covering the green B-point in region 2. Therefore con(cid:12)guration (a)
cannot occur.

In con(cid:12)guration (b), a unit square V covers the C-point and also a green B-point
(in region 2, say) so each of the 5 remaining green points must be covered by a unit
square. The centre of another unit square W that covers the remaining green B-point
will then be located in region 8 in Figure 2. The square W must cover at least one of the
adjacent red A-points, the one in region 7, say. If W also covers the point (1,1), then,
by the same argument used in con(cid:12)guration (a), any unit square covering the green
A-point in region 7 and the red B-point in region 4 will intersect the line y = 2 in such
a way that one cannot now cover the green A-point in region 1 without also covering
the already covered green B-point in region 2. Thus W cannot cover the point (1; 1);
but then, by Lemma 2, a unit square covering the green A-point in region 9 must also
cover the red B-point in region 6. Consequently, the following pairings of points must be
covered by distinct unit squares; (i) the green A-point in region 7 with the red B-point
in region 4, (ii) the two A-points in region 1, (iii) the C-point with the green B-point in
region 2, and (iv) the two A-points in region 3. In cases (ii) and (iv), the unit squares
concerned must also cover the points (1,2) and (2,2) respectively; the argument for this
being essentially the same for the fact used to establish s(2) = 2, namely that the centre
point of a 2(cid:2)2 square forms an unavoidable singleton set. The square V covering the
C-point and the green B-point in region 2 is now so constrained that it cannot cover
any of the points (1; 3
2 ); (2; 2). It now follows from Lemma 3, and the fact
the red A-point in region 7 is already covered, that the uncovered interval on the line
x = 1 has length at most 5
2 − 2. However, by Lemma 2
and the (cid:12)rst inequality in (7), the intercept of the square covering the green A-point in
region 7 and the red A-point in region 4 with the line x = 1 will require an interval with
2 − 2. Therefore con(cid:12)guration (b) also cannot occur, and the proof of
length at least 2
s(6) = 3 is complete.

2 ); (1; 2); (2; 3
p

2 ) = 13

2 − 1

2 < 2

3 − (

6 −

p

p

p

the electronic journal of combinatorics 9 (2002), #R14

6

4. Applying Diophantine properties of

2.

p

As many of the packings displayed in [2] show, by rotating by half a right-angle certain
squares from the trivial method of packing squares, we may be able to pack one extra
square, or even many extra squares. As is to be expected, such an argument applied to a
large square for the packing will involve the Diophantine properties associated with
2.

p

k ·

k

d

=

k -
2

t

1+t

1+t

Figure 3. Construction demonstrating s(n2 + 1) < n + (cid:14) with

1
2

< (cid:14) < 1.

A square is a sum of two triangular numbers. More speci(cid:12)cally, the identity

(t + 1)2 =

t(t + 1)
2

+

(t + 1)(t + 2)
2

shows that a square with side length t + 1 is the sum of two ‘triangles’ formed by unit
squares, with the smaller and larger ones given by the triangular numbers on the right-
hand side of the equation. We now start with a square formed by four such squares,
and insert two ‘corridors’ with width (cid:14) forming a cross to separate the four squares. We
then remove the four smaller triangles from these four squares in the centre of the large
square, so that the number of unit squares being removed is 2t(t + 1) and the region left
is a ‘ragged square’ together with the corridors; see Figure 3. Suppose now that t is so
chosen that 2t(t + 1) + 1 = k2, with k also being an integer. Then a simple calculation
shows that a square with side length k, slanting at half a right-angle can (cid:12)t into the
ragged square region, provided the width of the corridors satis(cid:12)es

(cid:14) =

k
p

2

− t:

Thus, we can have an initial square with side length n + (cid:14), with n = 2(t + 1), packing

2(t + 1)(t + 2) + 2t(t + 1) + 1 = 4(t + 1)2 + 1 = n2 + 1

the electronic journal of combinatorics 9 (2002), #R14

7

unit squares. The Diophantine equation 2t(t + 1) + 1 = k2 can be rewritten as (2t +
1)2 + 1 = 2k2, to which there are in(cid:12)nitely many solutions. On rewriting the equation
as (

2k + (2t + 1))(

p

p

2k − (2t + 1)) = 1, we (cid:12)nd that
p

(cid:14) =

k
p

2

− t =

1
2

+

2k − (2t + 1)
2

=

1
2

+

2(

p

1

2k + 2t + 1)

! 1
2

as

t ! 1;

so that we may choose solutions t so large that (cid:14) can be made arbitrarily close to 1
2
from above. Table 1 gives the (cid:12)rst few solutions.

t

k

n

(cid:14)

0

3

8

5

1

2

20

29

0(cid:1)707 : : :
0(cid:1)5355 : : :
0(cid:1)506 : : :
42
240 0(cid:1)501 : : :
169
985 1394 0(cid:1)5001 : : :
696
4059 5741 8120 0(cid:1)50003 : : :

119

Table 1

Recalling our de(cid:12)nition for (cid:14)n in x1, we note that the corresponding values for (cid:14)
in Table 1 are upper bounds for (cid:14)n. The bound for (cid:14)2 is attained, and the bound
(cid:14)8 (cid:20) 0(cid:1)5355 : : : is currently the best known solution, but not yet proved to be optimal;
see [2]. The bound (cid:14)42 (cid:20) 0(cid:1)506 : : : is also interesting in that we shall establish in x6
that (cid:14)43 < 0(cid:1)5.

( +t

2)1

2 2
t

+ t
2

+

1

2 +t

1

Figure 4. Construction demonstrating s(n2 + cn) < n + (cid:12) with

1p
2

< (cid:12) < 1.

the electronic journal of combinatorics 9 (2002), #R14

8

Next we let (cid:14) > 1=

p

2 and 0 < c < 2(cid:14) −

p

2. For such values of (cid:14) and c, the interval

p

c +
2

2

< (cid:12) < (cid:14)

(8)

is non-empty. Take a square with side length 2t + 1, and remove the four ‘triangular’
corners formed by t(t+1)=2 unit squares. The resulting shape is a ragged square, slanted
at half a right-angle to the original square, formed with (2t+1)2 −2t(t+1) = 2t2 +2t+1
unit squares, and this ragged square lies inside a square with side length (t + 1)
2; see
Figure 4. On writing

p

p

(t + 1)

2 = n + (cid:12);

with n being the integer part, so that (cid:12) is the fractional part, we (cid:12)nd that
p

p

p

n2 = ((t + 1)

2 − (cid:12))2 = 2(t2 + 2t + 1) − 2

2(cid:12)(t + 1) + (cid:12)2 = 2t2 + 2t(2 −

(9)

2(cid:12)) + O(1):

Thus the number of unit squares being packed into a square with side length n + (cid:12) is
p

p

p

p

2t2+2t+1 = n2+2t(

2(cid:12)−1)+O(1) = n2+

2n(

2(cid:12)−1)+O(1) = n2+n(2(cid:12)−

2)+O(1):

p

2 is irrational, there are arbitrarily large t such that the value of (cid:12) in (9)
Finally, since
satis(cid:12)es (8) so that this number here exceeds n2 + cn. Obviously, for all the packings
in this section, the wasted area is of order O(n).

5. Proof of Theorem 2.
We (cid:12)rst consider those n having the form

n = p(t − 1); where p(t) = 4t3 + 4t2 + 3t + 1;

(10)

and proceed to show that, for such n, one can pack n2 + 1 unit squares in a square with
side length n + (cid:14), where (cid:14) = (cid:14)(t) will be speci(cid:12)ed later.

/
T

m + d

K · (m+1)

T

P

n + d

Figure 5. Construction used in the proof of Theorem 2.

the electronic journal of combinatorics 9 (2002), #R14

9

We partition the square with side length n + (cid:14) into two rectangles, each with the

same side width n + (cid:14), and the smaller rectangle R having height m + (cid:14), with

m = 2t2 − t:

The larger rectangle has height n − m and we pack it trivially using (n − m)n unit
squares, so that it remains to show that mn + 1 unit squares can be packed into R.

We (cid:12)rst partition R into a parallelogram P and two trapezia T , T 0 of equal size
on either side of P ; see Figure 5. The packing of T consists of columns of width 1 and
heights m−jt, with j = 0; 1; : : : ; 2t −2, so that the number of unit squares being packed
is t2(2t − 1). This packing then de(cid:12)nes an angle

(cid:18) = tan−1 1
t

for the slant side of T . We then pack the parallelogram P with slanting columns of length
m+1 and width 1, with the (cid:12)rst column touching the leading corners of the unit squares
in T . Observe that, since m + 1 = 2t2 − t + 1 > (2t − 1)
t2 + 1 = (2t − 1)cosec (cid:18), the
sloping column touches all the leading corners, extending slightly above the uppermost
corner as shown in Figure 5. The value of (cid:14) can now be derived from the equation

p

(m + 1) cos (cid:18) + sin (cid:18) = m + (cid:14);

giving

(cid:14) = (cid:14)(t) =

1p

t2 + 1

p

+

t2 + 1(

t
p
t2 + 1 + t)

p

+

t2 + 1(

t
p
t2 + 1 + t)2

:

In particular, we have the asymptotic expansion

(cid:14)(t) =

3
2t +

1
4t2

− 7
8t3

− 1

4t4 + O

(cid:16)

(cid:17)
;

1
t5

t ! 1;

and also the explicit bound (cid:14)(t) < (cid:17)(t), where (cid:17)(t) is given by (5). We place further
columns adjacent to the (cid:12)rst column, so that all together K columns are packed into
the parallelogram P , leaving the trapezium T 0 to be packed in the same way as that
for T . With n being speci(cid:12)ed by (10), we need to set K = n − 4t + 3 in order to have
the total number of unit squares inside R being K(m + 1) + 2t2(2t − 1) = mn + 1. The
total length of the projection of the K columns onto the side width of the rectangle R
together those of the two trapezia is given by

f (t) = 4t + (K − 1) sec (cid:18) + cos (cid:18) − (m + 1) sin (cid:18):

It can be veri(cid:12)ed that, for all t (cid:21) 1,

0 < f (t) − n =

1
t

− 3

8t2 + O

(cid:17)

(cid:16)

1
t3

< (cid:14)(t);

the electronic journal of combinatorics 9 (2002), #R14

10

so that the choice of n = p(t − 1) = 4t3 − 8t2 + 7t − 2 in (10) is admissible. Moreover,
for such n, we have

2n < (2t − 1

3 )3 <

(cid:16)

2t − 2t
6t + 1

(cid:17)3

(cid:16)

=

3
2t + 1

3

4t2

(cid:17)3

(cid:16)

<

(cid:17)3

3
(cid:17)(t)

so that

(cid:14)n (cid:20) (cid:14)(t) < (cid:17)(t) <

3
(2n)1=3

;

which is sharper than the estimate (2). If n does not have the form in (10) then we
choose t so that p(t − 1) < n < p(t). The estimate (2) then follows from (cid:14)n (cid:20) (cid:14)p(t−1) (cid:20)
(cid:14)(t), together with the new upper bound for n in terms of t and the full use of (cid:14)(t) < (cid:17)(t).
The theorem is proved, and we note that setting t = 3 we (cid:12)nd that (cid:14)55 < 1
2 . We remark
that the wasted area associated with this construction is O(n2=3).

The proof of the Corollary proceeds as follows. Let t0 = t0(r) be the smallest t

satisfying

(cid:17)(t) < 3

1
4t2

(cid:20) 1
r

:

2t +
Then (cid:14)n < 1=r for n = p(t0 − 1) and hence, recalling the de(cid:12)nition of nr in x1, nr (cid:20)
p(t0 −1). The value for t0 is given by [(cid:28) ]+1, where (cid:28) is the positive root of the quadratic
equation 4t2 = 6tr + r, that is

(cid:28) =

3r
2

+ (cid:15);

with

(cid:15) =

p

r
9r2 + 4r + 3r

:

Since 1=7 < (cid:15) < 1=6, it follows that t0 = [3r=2] + 1. A slightly stronger statement comes
from choosing (cid:28) to be the real root of (cid:17)(t) = 1=r.

the electronic journal of combinatorics 9 (2002), #R14

11

6. A construction for (cid:14)43 < 1
2 .
As noted in x5 we have (cid:14)55 < 1
2 , so that n2 (cid:20) 55. By re(cid:12)ning the construction, we can
improve this to n2 (cid:20) 43. The improved construction is similar to that used in the proof
of Theorem 2, but di(cid:11)ers in respect of the packing of the trapezia because n is not of
the chosen form.

T

5.43

36 ·

16

P

5.15

/
T

28 ·

43

28

Figure 6. Construction demonstrating s(432 + 1) < 43 + 1
2 .

As before, we (cid:12)rst partition the square into two rectangles, each with length n + (cid:14),
2 . With m = 15, it follows that the larger rectangle has height 28,
2 . We then pack 1204 = 43(cid:2)28 unit squares

with n = 43 and (cid:14) = 1
and the smaller one R has height y0 = 15 + 1
trivially in the larger rectangle.

We next partition R into two trapezia T and T 0 with equal size at opposite ends
of R, leaving a parallelogram P ; see Figure 6. We pack P with rectangular columns,
each of which is made from 16(cid:2)1 unit squares, so that the angle (cid:18) each column makes
with the long side of R is given by the equation

cos (cid:18) =

y0
16 + tan (cid:18)

;

so that

(cid:18) = 0(cid:1)3205 : : : :

We can pack 576 = 16(cid:2)36 unit squares by forming 36 columns within P , which now
has length 36 sec (cid:18) = 37(cid:1)932 : : : . Let the lengths of parallel sides for T be x0 and
x1 = x0 + y0 tan (cid:18). Then, since T and T 0 are the same, we need to have
x0 = 0(cid:1)210 : : : :

x0 + x1 + 36 sec (cid:18) = 43 + 1
2 ;

so that

The four corners for T can be given the coordinates (0; 0); (x1; 0); (0; y0); (x0; y0), so that
the longest side has the equation y(x0 − x1) = y0(x − x1). Now, for y = 1; 4; 7; 10; 13,
the corresponding approximate values for x are 5(cid:1)024; 4(cid:1)028; 3(cid:1)032; 2(cid:1)036; 1(cid:1)040. Thus,
we may pack T with unit squares in 13 rows, with 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1
squares in the corresponding rows; that is 35 unit squares can be packed in T . The
total number of unit squares packed inside the square is thus given by

43(cid:2)28 + 36(cid:2)16 + 2(cid:2)35 = 1850 = 432 + 1:

Optimising the above computations further, we (cid:12)nd that (cid:14)43 (cid:20) 0(cid:1)4888 : : : .

the electronic journal of combinatorics 9 (2002), #R14

12

Using similar ideas, one may show that n3 (cid:20) 239, n4 (cid:20) 625, n5 (cid:20) 1320, n6 (cid:20)
2493 and n7 (cid:20) 4072. The relevant parameters for these constructions are given in
Table 2, where T and T 0 are now the numbers of squares being packed into the trapezia
concerned. Note that the larger solutions are not symmetric with respect to the packing
of the trapezia.

r

2

3

4

5

6

7

n m K

43

239

625

15

30

67

36

225

604

T

35

98

430

1320 119 1295 855

T 0

35

98

374

826

2493 158 2460 1448 1307

4072 217 4034 2120 2093

Table 2

These results provide upper bounds for nr and hence (cid:14)n. In Figure 7 we plot the
bound for (cid:14)n together with the weaker bound indicated by Theorem 2. The further opti-
misation obviously leads to slight improvements for the upper bounds for the particular
values considered.

1

d

0.1

10

d = 3(2n)-1/3 + 3(2n)-2/3 

100

1000

10000

n

Figure 7. Log-log plot of bounds for (cid:14)n.

The above suggests that the limit

−(cid:12) = lim
n!1

log (cid:14)n
log n

exists, and our explicit construction implies that 1
3 (cid:20) (cid:12) (cid:20) 1, while the result of Erd}os
and Graham [1] shows the lower bound can be improved slightly to (cid:12) (cid:21) 4=11. The
existence and the exact value of (cid:12) remain to be established.

the electronic journal of combinatorics 9 (2002), #R14

13

References.

[1] P. Erd}os and R. L. Graham, \On packing squares with equal squares", J. Combin.

Theory, Ser. A, 19 (1975) 119-123.

[2] E. Friedman, \Packing unit squares in squares: A survey and new results", The

Electronic Journal of Combinatorics, Dynamic Surveys (]DS7),
http://www.combinatorics.org/Surveys/ds7.html (2000) 25pp.

the electronic journal of combinatorics 9 (2002), #R14

14

