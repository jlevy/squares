Improved packings of n(n − 1)
unit squares in a square

M.Z. Arslanov ∗

S.A. Mustaﬁn

Institute of Information and Computational Technologies
Almaty, Kazakhstan

mzarslanov@hotmail.com sam@ipic.kz

Z.K. Shangitbayev
Almaty Management University
Almaty, Kazakhstan

sh.zhanbek@gmail.com

Submitted: Mar 14, 2019; Accepted: Oct 15, 2021; Published: Nov 5, 2021
c(cid:13) The authors. Released under the CC BY-ND license (International 4.0).

Abstract

Let s(n) be the side of the smallest square into which we can pack n unit squares.
The purpose of this paper is to prove that s(n2 − n) < n for all n (cid:62) 12. Besides, we
show that s(182 − 17) < 18, s(172 − 16) < 17, and s(162 − 15) < 16.
Mathematics Subject Classiﬁcations: 05B40, 52C15

1

Introduction

The problem of packing equal squares in a square has been around for some 40 years [1].
Let s(n) be the side of the smallest square into which we can pack n unit squares. Nag-
amochi [3] proved that s(n2−2) = s(n2−1) = n. It follows from [1] that s(n2−O(n 7
11 )) < n
for big n. From [4] it follows that the 7/11 degree can be reduced to 5/8.

An important question is to ﬁnd the minimum n for which s(n2 − n) < n. For small
n, only s(2) = 2 and s(6) = 3 have been proved, but we dont even know the proof of
s(12) = 4. It was proved in [2] that s(n2 − n − 1) < n for 3 < n < 11. Due to Lars
Cleemann it was known that s(172 − 17) < 17 [2]. Nagamochi in [3] mistakenly says that
the following is proved in [2]

s(n2 − n) < n ∀n (cid:62) 17.

(1)

∗Supported by MSE of Kazakhstan grant GF4 AP05133090.

the electronic journal of combinatorics 28(4) (2021), #P4.22

https://doi.org/10.37236/8586

The truth is that in [2] a sporadic squeezable packing of 272 unit squares in a square
(17,17) is given, proving that s(172 − 17) < 17, but from this it does not follow that
s(182 − 18) < 18 etc. Thus, Nagamochi’s implicit conjecture (1) needs a proof.

We prove the conjecture and even more: s(n2 − n) < n ∀n (cid:62) 12, and, moreover,

s(182 − 17) < 18, s(172 − 16) < 17, s(162 − 15) < 16.

2 Some squeezable packing of rectangles

Let a packing of m unit squares in a rectangle R = (Rx, Ry) be given. We assume that
(Rx − 1)(Ry = 1) < m < RxRy and we can’t pack a unit square in the waste area. This
packing is called squeezable if both sides of a rectangle can be reduced, i.e., for some
δ > 0 there exists a packing of m unit squares in a rectangle (Rx − δ, Ry − δ). The
maximum of such δ > 0 is called the value of squeezing and is denoted by δ(R, m). We
write δ(R, m) = 0 if the packing is not squeezable.

The property of squeezability of a packing for small parameters can be proved rather
simply. However proving this property for large parameters is a non-trivial mathematical
problem. The following obvious formula connects δ(R, m) and s(n):

s(n) = (cid:100)s(n)(cid:101) − δ(((cid:100)s(n)(cid:101), (cid:100)s(n)(cid:101)), n).

If δ((Rx, Ry), m) < 1 then the fact that for integer Rx, Ry

δ((Rx, Ry), m) (cid:54) δ((Rx + 1, Ry), m + Ry − 1)

(2)

can be proved by adding Ry − 1 unit squares to the x-side of a rectangle (Rx, Ry). Figure
1 shows the basic idea for eﬃciently packing unit squares in a square S, where rectangles
C and D are integer and the waste is in rectangles A and B. It is easy to see that if the
packing of unit squares in rectangles A, B is squeezable, then the packing of unit squares
in S is squeezable and

δ(S, ·) (cid:62) min(δ(A, ·), δ(B, ·)).

(3)

This bound can be increased if we note that after squeezing there is a little space
between rectangles A, B. We can give this space to a rectangle with minimal squeezing
value in order to increase that value and thus to increase the evaluation of δ(S, ·).

Let us consider a packing of 26 unit squares in a rectangle (4, 8) (see Figure 2). This

packing is centrally symmetric and the waste is equal to 6.

In Figure 2 we see one of the main ideas for packing unit squares: using of stacks (4, 1)
tilted by an angle α = arcsin(8/17). The main idea for squeezing a packing follows from
it: tilting stacks (4, 1) by an angle α + ε so that the stack (4, 1) is located in a vertical
strip of width 4 − δ, where ε and δ are suﬃciently small. Hereinafter we determine the
orientation of a unit square by a unit vector (x, y) with x > 0, y (cid:62) 0, x2 + y2 = 1 directed
along the side of this unit square. If the bottom vertex of the unit square is at the origin
then the three other vertices have coordinates (x, y), (x − y, y + x), (−y, x) . Note that if

the electronic journal of combinatorics 28(4) (2021), #P4.22

2

C

A

B

D

Figure 1: Scheme of squeezable packing

P
S1 P1

(0, 0)

Figure 2: Squeezable packing of 26 unit squares in a rectangle (4,8)

two points Pt, Pb are taken on the top side and the bottom side of this unit square then
the scalar product (cid:104)Pt − Pb, (x, y)(cid:105) is equal to 1.

Continuing with the example in Figure 2, after increasing the tilt the stack (4, 1) in a
vertical strip of width 4 − δ has orientation (x1, y1), x1 > 0, y1 (cid:62) 0 satisfying the system
of equations

4x1 + y1 = 4 − δ, x2

1 + y2

1 = 1.

To evaluate the squeezing value δ((4, 8), 26), we use the bisection method. The packing
remains centrally symmetric. The distance between the point P = (Px, Py) = (1 −
δ/2, 2 − δ/2) and the upper side of the square S2 intersecting the line x = 1 − δ/2 in
2) y1
the point P1 = (P1x, P1y) = (1 − δ
) is critical. For δ = 0.01
x1
we have x1 = .877695..., y1 = .479219..., Py − P1y = 0.021604 > 0. For δ = 0.02 x1 =
.87312663..., y! = .48749347..., Py − P1y = −0.0061309... < 0. The bisection method gives
evaluation δ((4, 8), 26) > 0.0177702.

2, (1 − δ

+ 1−x1
x1y1

+ 1
x1

Figure 3 shows a more complex example, a centrally symmetric squeezable packing of

the electronic journal of combinatorics 28(4) (2021), #P4.22

3

S7

P8
P7

S9

S8

P6

S6

P5

P3

S3

S4

S5

P2

P4
P1

S2

P0

S1

(0, 0)

Figure 3: Squeezable packing of 64 unit squares in a rectangle (6,12)

64 unit squares in a rectangle (6,12). Four unit squares: S3, S6 and their symmetric ones
have not the orientation ( 35
37, 12
37) nor (1, 0). Hereinafter we denote points and squares by
the same indices in diﬀerent ﬁgures without losing accuracy.

In this packing the left vertex of S2 is on a side of S1. The square S3 is placed so
that the right vertices of squares S2, S5, and the top vertex of S4 are on the sides of S3.
Vertices of the squares S8, S7, S9 are on sides of S6. Calculations show that there is a
small distance between S3 and S6, which guarantees squeezability of the given packing.

To calculate the squeezing value δ((6, 12), 64), take δ = 0.004 and deﬁne the existence
of a packing 64 unit squares in a rectangle (6 − δ, 12 − δ). The distance between the right
vertex of S3 and the top side of S6 should be not less than 1.

Table 1 contains calculations with δ = 0.004.
Calculations with δ = 0.005 give (cid:104)P8 − P5, (x2, y2)(cid:105) = 0.999617371807702270, i.e., the
squares S3, S6 intersect. The bisection method gives evaluation δ((6, 12), 64) > .00490823.
A packing of 58 unit squares in a rectangle (6,11-2/35) can be obtained by removing
one stack (6,1) in Figure 3 and lifting up by 37/35 all the squares that are below this

the electronic journal of combinatorics 28(4) (2021), #P4.22

4

Object
δ
Orientation (x1, y1)
of stack (6,1)
P0

P1
P2
P3

Orientation
(x2, y2) of S3
P4

P5
P6
P7

P8
Orientation
(x3, y3) of S6
Distance between P5
and top side of S6

Formulae or system of equations

1 + x2
y2

1 = 1, 6y1 + x1 = 6 − δ

P0 = (−2 + δ/2,

(2 − δ/2) x1
y1

+ 2
y1

+ 1−y1
x1y1

)

P1 = P0 + (x1 + y1, y1 − x1)
P2 = (δ/2 − 1, 4 − δ/2)
P3 = (3 − 3y1 − δ
2 ,
− (3−3y1−δ/2)x1
+ 4
y1
y1
2 + y2
x2

2 = 1.,

)

(cid:104)P2 − P3, (−y2, x2)(cid:105) = 1
P4 = (cid:104)P1, (x2, y2)(cid:105) · (x2, y2)+
+(cid:104)P2, (y2, −x2)(cid:105) · (y2, −x2)
P5 = P4 + (x2 + y2, y2 − x2)

P6 = ( 1

2 δ, 5 − 1

2 δ)

P7 = (3 − δ/2, −(3 − δ/2)x1/y1)+
+5(0, 1/y1) + 2(−y1, x1)
P8 = (1 − δ/2, 5 − δ/2)

3 + y2
x2

3 = 1.,

(cid:104)P6 − P7, (−y3, x3)(cid:105) = 1
(cid:104)P8 − P5, (x3, y3)(cid:105)

Numerical value
0.004
(.328061226490,
.94465646225)
(-1.998,2.989621361)

(-0.725282311,3.6062165968)
(-0.998,3.998)
(.1640306130, 4.177378839)

(.390085325,.92077871336)

(-1.0972231,3.76378828)

(0.213640902,4.29448167498)
(0.002,4.998)
(1.108687,4.9079035)

(0.998,4.998)
(.5062565099,.862382946)

1.00378910536129684

Table 1: Calculations with δ = 0.004.

stack. Similar calculations give the evaluation of the squeezing value δ((6, 11), 58) >
0.01681735886.

Consider a more diﬃcult problem of a squeezable packing of 43 unit squares in a rect-
angle (5,10). In Figure 4 six unit squares S1, S4, S9, S10, S11, S12 have not the orientation
13, 12
( 5

13) nor (1, 0).
The square S1 has a vertex on the side of the rectangle (5,10), one on a side of S2,
and one on a side of S3. The right vertex of S1 is on the bottom side of S4. S4 is tilted so
that the bottom right vertex of S3 is on the left side of S4 and the top vertex of the stack
(3, 1) is on the right side of S4. The left vertex of S5 is on the side of S6. The squares S9,
S10 are tilted by the same angle so that the vertex of S8 is on the side of S9, the vertex
of S5 is on the bottom side of S9, and the vertex of S7 is on the bottom side of S10. The
squares S11, S12 form a rectangle (2,1). The right vertex of S12 is on the right side of a
rectangle (5,10). The vertex of S13 is on the top side of S11. The bottom sides of S11 and
S12 are parallel to the line connecting the right vertices of S9 and S10. The vertex of S14
is on the bottom side of S15. Calculations show that there is a small distance 0.0055111...
between the bottom side of the rectangle (2, 1) = S11 ∪ S12 and the line connecting the

the electronic journal of combinatorics 28(4) (2021), #P4.22

5

S13

S11 S12
S10

S9

S7

S8

S5

S4

S2

S6

S3

S1

S15

S14

Figure 4: Squeezable packing of 43 unit squares in a rectangle (5,10)

right vertices of S9 and S10. This guarantees squeezability of the given packing.

Calculation of the squeezing value δ((5, 10), 43) gives the evaluation δ((5, 10), 43) >
0.0009652493. This packing plays an important role in the squeezable packing of 132 unit
squares in a square (12,12). Below we show the evaluation of δ((12, 12), 132). From this
evaluation one can obtain the evaluation of δ((5, 10), 43). Analogous calculations give the
evaluation of the squeezing value δ((5, 9), 38) > 0.020403.

Table 2 contains the evaluations of the squeezing values of some rectangles.

Rectangle R n
26
43
38
64 > 0.004908231774819
58

δ(R, n)
> 0.01777021751
> 0.0009652493
> 0.020403

(4,8)
(5,10)
(5,9)
(6,12)
(6,11)

> 0.01681735886

Table 2. Evaluations of squeezing value of some rectangles

To prove conjecture (1), we need the following lemma.

Lemma 1. For any k (cid:62) 3 there exists a squeezable packing of 4k2 + 6k − 2 unit squares
in a rectangle (2k, 2k + 4) (the waste is equal to 2k + 2).

the electronic journal of combinatorics 28(4) (2021), #P4.22

6

The proof is technically simple and can be understood from Figure 5, showing a
centrally symmetric squeezable packing of 86 unit squares in a rectangle (8, 12). For
an arbitrary k (cid:62) 3, the centrally symmetric packing in the upper half of a rectangle
(2k, 2k + 4) consists of 2 staircases. A staircase with orientation (1,0) having k(k+1)
unit
squares, and a staircase with orientation (x1, y1) = ( 4k2−1
4k2+1 ) that has (3k−1)(k+2)
unit
4k2+1,
squares. The top vertex of Sk+1 has ordinate

4k

2

2

yk+1 = −

4k2
4k2 − 1

+ (k + 2)

4k2 + 1
4k2 − 1

+ (k − 1)

4k
4k2 + 1

<

< −

4k2
4k2 − 1

+ (k + 2)

4k2 + 1
4k2 − 1

+ (k − 1)

4k
4k2 − 1

= k + 2 −

2(k − 2)
4k2 − 1

< k + 2,

i.e., Sk+1 is in rectangle (2k, 2k + 4). The top vertex of S0 has ordinate

4k2
4k2 − 1

+

4k2 − 1
4k2 + 1

= 2 +

1
4k2 − 1

−

2
4k2 + 1

< 2,

i.e., S0 does not intersect the staircase with orientation (1,0). Each square Sj, 1 (cid:54) j (cid:54) k
intersects the vertical line x = k − j in the point

(k − j, j ·

1 − x1
x1y1

+ (k − j)

y1
x1

+

j
x1

).

The ordinate of this point satisﬁes

j ·

1 − x1
x1y1

+ (k − j)

y1
x1

+

j
x1

= 1 + j +

1
2

·

j · (−4k2 + 4k + 1) + 2k
k(4k2 − 1)

< 1 + j,

i.e., none of the Sj, 1 (cid:54) j (cid:54) k intersects the staircase with orientation (1,0). We see
that there is a positive distance between the two staircases. Therefore, this packing is
squeezable. The lemma is proved.

3

Improved squeezable packing of some squares

As mentioned in the introduction, in [3] Nagamochi mistakebly says that in [2] it is proved
that

s(n2 − n) < n ∀n (cid:62) 17.

(4)

Thus he implicitly formulates the conjecture (4). For the proof of this conjecture we use
lemma 1 as follows.

For even n (cid:62) 14 we use Figure 1 with rectangles A = (12, 6), B = (n − 10, n − 6), C =

(10, n − 6), D = (n − 12, 6).

For odd n (cid:62) 13 we use Figure 1 with rectangles A = (10, 5), B = (n − 9, n − 5), C =

(9, n − 5), D = (n − 10, 5).

Thus the conjecture (4) is proved for n (cid:62) 13.
For the proof of this conjecture for n = 12 see Figure 6.

the electronic journal of combinatorics 28(4) (2021), #P4.22

7

y = k + 2

y = j + 1

S1

y = 2

S0

Sk+1

Sj

(0,0)

Figure 5: Squeezable packing of 4k2 + 6k − 2 unit squares in a rectangle (2k, 2k + 4)

The packing in Figure 6 is obtained from the squeezable packing in rectangles (8,4),
(5,10). In the packing in (5,10) we tilt the angular squares S1, S2 by an angle arcsin(10/26)
so that the bottom vertex of S1 has an integer y-coordinate and S2 has intruded space in
the rectangle (8,4). From the packing in (8,4) we remove two right top squares and move
to the left by 1/20 unit squares tilted by an angle arcsin(8/17) so that the bottom vertex
of S3 is on the side of S4. The small distance between S2 and S5 makes the packing in
Figure 6 squeezable.

Thus we have proved that

s(n2 − n) < n ∀n (cid:62) 12.

To evaluate δ((12, 12), 132), take δ = 0.002. The origin is in the right bottom vertex of
the integer rectangle (7, 8). The bottom side of (12,12) has y-coordinate −4 + δ, the right
side of (12,12) has x-coordinate 5 − δ.
Table 2 contains the calculations.

the electronic journal of combinatorics 28(4) (2021), #P4.22

8

Object
δ
Orientation (x1, y1)
of stack (4,1)
P0
Orientation (x2, y2)
of stack (5,1)
P1 = (P1x, P1y)

Lower ordinate of
intersection S2
with line x = 0
Orientation (x3, y3)

of square S6
P2
P3
Orientation (x4, y4)
of square S9
P4

P5

P6

P7

P8
Orientation (x5, y5)
of squares S14, S15
P9 = (P9x, P9y)

P10 = (P10x, P10y)

P11 = (P11x, P11y)
Distance between P11

and segment [P9, P10]

Formulae or system of equations

1 + x2
y2

1 = 1, y1 + 4x1 = 4 − δ

P0 = (4/x1 − 1/y1 + x1/y1 − 5, 0)

2 + x2
y2

2 = 1, 5y2 + x2 = 5 − δ

P1 = ((2 − 2x2 − δ) · y1/x1 + 2 · y2,
−2 + δ) + P0

Y1 = P1y + P1x · x2
y2

x2
y2

=

3 + y2
x2

3 = 1,
(x2+y2−y3)
Y1+4/y2+y2−x2−4+x3+y3
P2 = (x3 + y3, 4 − x3)

P3 = (x2 + 2y2, Y1 + 5
y2
4 + y2
x2
4 = 1,

+ y2 − 2x2)

(cid:104)P3 − (1, 4), (y4, −x4)(cid:105) = 1
P4 = (1, 6
−
y2

+ (P1x − 1) x2
y2

−2 + δ + 1−y2
x2y2
P5 = P4 + (x2 + y2, y2 − x2)

)

(cid:104)(P6 − P2), (x4, y4)(cid:105) = 1
(cid:104)(P6 − P4), (y2, −x2)(cid:105) = 1
P7 = P6 + (x2 + y2, y2 − x2)

P8 = P3 + (2y2, 2/y2 − 2x2)

5 + y2
x2

5 = 1,

(cid:104)P8 − (2, 6), (y5, −x5)(cid:105) = 2
P9 = (cid:104)P5, (x5, y5)(cid:105) · (x5, y5)+
+(cid:104)(2, 6), (−y5, x5)(cid:105) · (−y5, x5)
+(x5 + y5, y5 − x5)
P10 = (cid:104)P7, (x5, y5)(cid:105) · (x5, y5)+
+(cid:104)(2, 6), (−y5, x5)(cid:105) · (−y5, x5)
+(x5 + 2y5, y5 − 2x5)
P11 = (4 − δ, 7)
(P9y−P10y)·(P11x−P9x)
((P9y−P10y)2+(P9x−P10x)2)
− (P9x−P10x)·(P11y−P9y)
√

((P9y−P10y)2+(P9x−P10x)2)

√

−

Numerical value
0.002
(.881413748866,
0.4723450045357421)
(-.712894713,0)
(.386451637219073...,
.9223096725561...)
(1.788247541,-1.998)

-1.248716749

(.1523435...,

.98832760...)

(1.140671137,3.847656465)
(2.231070982,4.321862330)
(.39947627...,
0.9167435347...)
(1,5.055655408)

(2.30876131,
5.5915134434)
(1.897035430423,
4.608883990)
(3.20579674042318,
5.14474202553891)
(4.075690327,5.717428128)
(.4235421115...,
.905876415...)
3.22807975740513
6.26558985540152)

4.12345766036105
5.81959341362795

(3.998,7)
1.000648944...

Table 2: Calculations for δ = 0.002.

the electronic journal of combinatorics 28(4) (2021), #P4.22

9

S18

P11

S17

S16

P10

S15

P8

S13

P9

S14

P5

S10

P4

P7

S12

P6

S9

P3

S11

S8

P2

S6

S7

P0

(0, 0)

S2

S5

S1

P1

S3

S4

Figure 6: Squeezable packing of 132 unit squares in a square (12,12)

Calculations with δ = .0021 give the distance 0.9999866543 between the bottom
left vertex of S18 and the segment [P9, P10]. The bisection method gives the evaluation
δ((12, 12), 132) > 0.00209798269, i.e., s(132) < 11.99790201731.

Analogous calculations give evaluations

δ((5, 10), 43) > 0.0009652493, δ((5, 9), 38) > 0.020403

δ((13, 13), 156) > 0.0059576, s(156) < 12.9940424.

Calculations with C = (10, 8), D = (3, 6), A = (11, 6), B = (4, 8) in Figure 1 give

δ((14, 14), 182) > 0.01681735886, s(142 − 14) < 13.98318264114.

For the square (15, 15) we have δ((15, 15), 210) (cid:62) min(δ((5, 9), 38), δ((11, 6), 58)) >

0.01681735886, i.e., s(210) < 14.98318264114.

For the square (16, 16) we have δ((16, 16), 241) > min(δ((5, 10), 43), δ((12, 6), 64)) >

0.0009652493, i.e., s(162 − 15) < 15.9990347507.

More careful analysis when we use the space between rectangles (5,10) and (12,6) gives

δ((16, 16), 241) > 0.00404996, i.e., s(162 − 15) < 15.99595004.

Calculations with A = (12, 6), B = (6, 11), C = (11, 11), D = (5, 6) give

δ((17, 17), 172 − 16) > 0.0049082317748, s(172 − 16) < 16.9950917682252.

the electronic journal of combinatorics 28(4) (2021), #P4.22

10

Notice that this squeezable packing of a square (17,17) contains one unit square more
than in [2].

Calculations with A = (13, 6), B = (6, 12), C = (12, 12), D = (5, 6) give

δ((18, 18), 182 − 17) (cid:62) 0.0049082317748, s(182 − 17) < 17.9950917682252.

Table 4 contains the evaluations of the squeezing values and the upper bounds of s(n)

for new n.

n
132
156
182
210
241
273
307

s(n)
s(122 − 12) < 11.99790201731
s(132 − 13) < 12.9940424
s(142 − 14) < 13.98318264114
s(152 − 15) < 14.98318264114
s(162 − 15) < 15.99595004.
s(172 − 16) < 16.9950917682252
s(182 − 17) < 17.9950917682252

δ(((cid:100)s(n)(cid:101), (cid:100)s(n)(cid:101)), n)
δ((12, 12), 132) > 0.00209798269
δ((13, 13), 156) > 0.0059576
δ((14, 14), 182) > 0.01681735886
δ((15, 15), 210) > 0.01681735886
δ((16, 16), 241) > 0.00404996
δ((17, 17), 172 − 16) > 0.0049082317748
δ((18, 18), 182 − 17) > 0.0049082317748

Table 4. Evaluations of squeezing values and upper bounds of s(n) for new n

References

[1] P. Erd˝os and R. L. Graham, On packing squares with equal squares, J. Combin.

Theory Ser. A, 19 (1975) 119-123.

[2] E. Friedman, Packing unit squares in squares: A survey and new results, Elect. J.
Combin., Dynamic Survey # DS7 (1998, last version 2009). DOI: https://doi.org/
10.37236/28

[3] Nagamochi H., Packing unit squares in a rectangle, Elect. J. Combin., 12 (2005),

#R37. DOI: https://doi.org/10.37236/1934

[4] Shuang Wang, Tian Dong, Jiamin Li, A New Result on Packing Unit Squares into a

Large Square, arXiv:1603.02368 [math.CO]

the electronic journal of combinatorics 28(4) (2021), #P4.22

11

