6
1
0
2

r
p
A
9

]

O
C
.
h
t
a
m

[

2
v
8
6
3
2
0
.
3
0
6
1
:
v
i
X
r
a

A New Result on Packing Unit Squares into a Large
Square

Shuang Wanga, Tian Dong∗

,a,1, Jiamin Lia

aSchool of Mathematics, Jilin University, Changchun, Jilin 130012, China

Abstract

In their 2009 note: Packing equal squares into a large square, Chung and

Graham proved that the wasted area of a large square of side length x is

after maximum number of non-overlapping unit squares

O

x(3+√2)/7 log x
(cid:17)

(cid:16)

are packed into it, which improved the earlier results of Erd˝os-Graham and

Karabash-Soifer. Here we further improve the result to O(x5/8) that also

leads to an improvement of the bound for the dual problem: ﬁnding the min-

imum number of unit squares needed for covering the large square, from x2 +

O

x(3+√2)/7 log x
(cid:17)

(cid:16)

to x2 + O(x5/8).

Key words: packing, covering, wasted area, Taylor’s formula

1. Introduction

In 1975, Erd˝os and Graham [1] investigated the problem of packing a square

of side length x with as many non-overlapping unit squares as possible.

In

other words, the wasted area should be as small as possible. From then on,

5

the problem have already been well studied in the literature [2, 3, 4, 5, 6, 7, 8],

in which [2, 5, 6] focus on the case when x is large enough. Following [5], we

call the problem Packing Waste Problem. Also, there is a dual problem, called

∗Corresponding author
Email addresses: wangshuang@jlu.edu.cn (Shuang Wang), dongtian@jlu.edu.cn (Tian

Dong), jmli@jlu.edu.cn (Jiamin Li)

1Tian Dong was supported by National Natural Science Foundation of China under Grant

No. 11101185 and 11171133.

Preprint submitted to Journal of Combinatorial Theory, Series A

July 1, 2021

 
 
 
 
 
 
Covering Waste Problem in [5], which is concerned with covering the square

with minimium number of unit squares[5, 6, 9, 10, 11, 12].

10

Erd˝os and Graham obtained the ﬁrst estimation of Packing Waste Problem

as O(x7/11) [1]. Later, D. Karabash and A. Soifer in [9] gave the estimation of

Covering Waste Problem as O(x2/3) that was improved in [5] to O(x7/11). In
x(3+√2)/7 log x
(cid:17)

2009, Chung and Graham [6] found the best previous bound O

for both problems.

(cid:16)

15

In this paper we use basic analysis tools to improve the result of Chung and

Graham to O(x5/8) also for both problems.

2. Preliminary

Let A be a closed planar region and S(A) the area of it. We deﬁne two

functions

W (A) = S(A)

sup s(Aλ),

−

W ′(A) = inf s(A′λ)

S(A),

−

where Aλ ⊂
is a union set of unit squares (non-overlapping is not necessary). Specially,

A is a union set of non-overlapping unit squares, and A′λ ⊃

A

20

when A is a square of side length x, we denote W (A), W ′(A) as W (x), W ′(x)

respectively.

To our opinion, the basic task of Packing or Covering Waste Problem is

packing or covering a strip of non-integer width [6], say m. Basic idea for

packing a strip [6] is to pack stacks of non-overlapping unit squares of height

25

m

into the strip as close to being orthogonal as possible (see Fig. 1), namely

⌉

⌈
minimize the angle θ in Fig. 1 which satisﬁes

cos θ + sin θ = m.

m

⌉

⌈

(1)

. Obviously when r = 0, θ = 0 trivially. Otherwise, we let

Let r = m

m

− ⌊

⌋

θ = αmβ + o(mβ). By comparing with the constant term of (1), we have

θ = √2

−

r m−

1/2 + o(m−

1/2).

2

θ

m

⌈m⌉

1

1

Figure 1: Packing a strip of width m.

Similarly, as shown in Fig. 2, we also use stacks of unit squares of height

m

(hereafter we will call the stacks as rectangles of size 1

⌉

⌈
to cover the strip, then angle θ′ in Fig. 2 satisﬁes

m

⌉

× ⌈

for simplicity)

cos θ′

m

⌉

⌈

−

sin θ′ = m.

(2)

We also have θ′ = 0 when r = 0. If not, then

θ′ = √2

−

r m−

1/2 + o(m−

1/2).

Note that when m

, θ and θ′ are less than √2 m−

→ ∞

1/2.

θ′

m

⌈m⌉

1

1

Figure 2: Covering a strip of width m.

30

3

3. Packing Waste Problem

In this section, we will present our main result on Packing Waste Problem

in Theorem 1. For the proof of it, three types of basic shapes are introduced as

follows.

35

Type 1 shape Rectangle T1 has a length x and width x′ (see subﬁgure (a) of

Fig. 3) satisfying x3/4

x′

≤

≤

cx with c

≤

7 a constant.

Type 2 shape Trapezoid T2 has a height of x, a top edge of length x′ (see

subﬁgure (b) of Fig. 3) satisfying x′

2x1/2 and the angle θ between the

∼

right-hand side and a vertical line satisfying 0 < θ < √2x−

1/2.

40

Type 3 shape Trapezoid T3 has a height h

(see subﬁgure (c) of Fig. 3) where a =

1

2 x1/2 and a top edge of length a
is an exact integer.

∼
x1/3 +√2 x1/6

⌊

⌋

The angle θ between the right-hand side and a vertical line satisﬁes 0 <

θ < √2x−

1/2.

x′

a

x′

x

θ

h

θ

x

(a) Type 1 shape.

(b) Type 2 shape.

(c) Type 3 shape.

Figure 3: Three types of basic shapes.

The proof of Theorem 1 will be completed by an induction based on eﬀective

45

packings of these shapes.

Theorem 1. Keep the notations above. Then

(i) W (T1)

(ii) W (T2)

≤

≤

((15 + c)√2 + 38)x5/8.

( 19
2 + 7

2

√2)x5/6.

4

(iii) W (T3)

≤

( 19
4 + 7

4

√2)x1/3.

50

Specially, when T1 is a square of side length x, then W (x)

(16√2 + 38)x5/8.

≤

m2), a rectangle S2 of size m2 ×

Proof. (i) We partition Type 1 rectangle T1 into a rectangle S1 of size m1 ×
(x
x′, and an integer-sided rectangle T ′1, where
−
m = x3/4, as shown in Fig. 4. It is easy to see that T ′1 can be perfectly
m1, m2 ∼
packed, that is W (T ′1) = 0. Next, we pack S1 and S2 with rectangles of size

55

1

m1⌉

× ⌈

and 1

m2⌉

× ⌈

respectively. Finally, only four regions T2i, i = 1, 2, 3, 4,

at each end of S1 and S2, left unﬁlled which clearly belong to Type 2 with height

about m, a top edge of length m′

2m1/2, and θ < √2m−

1/2.

∼

m1

T21

S1

T22

T ′
1

T1

T23

S2

T24

m2

Figure 4: Packing Type 1 rectangle.

Applying (ii), the wasted area

W (T1)

≤

≤

≤

0 + x

1
2

2

·

·

tan θ + x′

1
2

2

·

·

4

tan θ +

W (T2i)

(x + x′)

·

√2m−

1/2 + 4(

((15 + c)√2 + 38)x5/8.

19
2

+

7
2

i=1
X
√2)m5/6

Specially, when T1 is a square of side length x, W (x)

(16√2 + 38)x5/8.

≤

60

(ii) Now we partition the Type 2 trapezoid T2 into rectangles A1,

, As

· · ·

5

and Type 3 trapezoids B1,

· · ·

and top edge of length integer a. Thus, s

, Bs (see Fig. 5). Each Bi has height h

1

2 x1/2

∼

x′ − a

A1

A2

2x1/2.

∼

a

B1

B2

θ

As

Bs

h

h

h

Figure 5: Packing Type 2 trapezoid.

Let ai be the width of Ai. Then we have x1/2 < ai < (2 + √2)x1/2, 2h <

ai < 2(2 + √2)h. From (i), we obtain W (Ai) = O(h5/8) = O(x5/16), hence

W

s

i=1
[

Ai

! ≤

s

i=1
X

Further, (iii) implies that

W (Ai)

≤

O(x5/16)

·

s = O(x13/16).

W

s

i=1
[

Bi

! ≤

s

i=1
X

W (Bi)

19
4

+

7
4

√2

x1/3

(cid:19)

≤

(cid:18)

s

·

≤

(

19
2

+

7
2

√2)x5/6,

which leads to the wasted area of T2

W (T2)

W

≤

s

i=1
[

+ W

Ai

!

s

i=1
[

Bi

! ≤

(cid:18)

19
2

+

7
2

√2

x5/6.

(cid:19)

(iii) We will partition the Type 3 trapezoid T3 into rectangles C0,

, Ct,

D0,

· · ·

, Dt and F1, triangles E0,

, Et with height h1 =

· · ·

−1/6
x
tan θ ⌋

⌊

height h2 satisfying 0

≤

h2 < h1, as illustrated in Fig. 6. Here t satisﬁes

· · ·
and F2 with

t < h/h1 =

1
2

x1/2

. (cid:18)

1/6

x−
tan θ −

r′

=

(cid:19)
−1/6

where r′ is the decimal part of x

to be

⌊

x1/3 + √2 x1/6

⌋ − ⌊

x2/3 tan θ

2(1

−

r′x1/6 tan θ) ≤

1
2

x2/3 tan θ,

tan θ . The width of Ck, denoted by ck, is set
, and therefore dk, the width of

k)x1/6

x1/3 + (√2

⌋

−

6

 
 
 
 
65

Dk, equals to

x1/3 + (√2

⌊

k)x1/6

⌋

−

+ kh1 tan θ, k = 0,

· · ·

, t. Note that when

h1 > h, then the number of Dk is 0, but the result still holds.

h1
h1

h1
h2

C0
C1

D0
D1

E0
E1

θ

Dt

Et

F2

Ct

F1

Figure 6: Packing Type 3 trapezoid.

1) Obviously, each Ck can be packed perfectly with unit squares, thus

t

t

W

Ck

=

W (Ck) = 0.

!

Xk=0
2) It is easy to see that each Ek can not be packed with unit squares. Thus

[k=0

W

t

t

=

Ek

!

[k=0

Xk=0

1
2

h2
1 tan θ

1
4

≤

x1/3.

3) We will estimate W (

, t, 0 < kh1 tan θ < 1

t
k=0 Dk) as follows. Since d0 is an integer, W (D0) =
=

2 x1/2 tan θ < 1 implies that
+ 1. Let rk be the decimal part of x1/3 + (√2

dk⌉
⌈
k)x1/6.

S

· · ·
k)x1/6

−

0. For k = 1,

x1/3 + (√2

⌊
Then

−

70

⌋

dk
dk⌉

⌈




= x1/3 + (√2

= x1/3 + (√2

k)x1/6

k)x1/6

−

−

−

−

rk + kx−

1/6

kr′ tan θ,

−

(3)

rk + 1.

Next, we will pack Dk with rectangles of size 1



dk⌉

× ⌈

and estimate αk more

accurately than before. By (1), we obtain

dk⌉

⌈

cos αk + sin αk = dk.

(4)

7

 
 
Substitute (4) into (3), we have

(x1/3 + (√2

k)x1/6

−

rk)(1

cos αk) = cos αk + sin αk −

−

−

kx−

1/6 + kr′ tan θ. (5)

Substitute Taylor’s formulae for cos αk, sin αk,

cos αk = 1
−
sin αk = αk −
1/6 + lk2x−






1

k + 1
2 α2
24 α4
1
k + o(α4
6 α3

k + o(α5
k),

k),

into (5) and set αk = lk1x−

1/3 + lk3x−

1/2 + o(x−

1/2). Since 0 <

kr′ tan θ < x−

1/3, we set kr′ tan θ = γkx−

1/3 + o(x−

γk < 1. Comparing the coeﬃcients of terms x0 and x−

we have

1/3), it follows that 0

≤
1/6, on both sides of (5),

αk = √2x−

1/6 + 0

·

x−

1/3 + lk3x−

1/2 + o(x−

1/2).

Since 0

k < 1

2 x2/3 tan θ < √2

2 . Comparing the coeﬃcients of terms x−

2 x1/6, we set k = βkx1/6 + o(x1/6), it follows that
1/3, on both sides of (5),

≤
βk < √2

0

≤

we have

αk = √2x−

1/6 + 0

x−

1/3 +

·

1

rk + γk −
6 βk −
√2(1
βk)
−

5
6

x−

1/2 + o(x−

1/2).

Hence

αk −

|

αk

1| ≤

−

3(1 + √2)x−

1/2, k = 2,

, t.

· · ·

75

We pack Dk as follows. First, we leave a Type 2 trapezoid D11 at the top of

D1. Second, for k = 2,
when bk ≥
Fig. 7). When αk

1

1 ≥

−

, t, we pack Dk

−

· · ·

1 with rectangles of size 1

cos αk−1 . If not, we pack Dk with rectangles of size 1
αk, the wasted region between Dk

× ⌈
1 and Dk consists of

dk
× ⌈
dk⌉

1⌉
−
(see

a triangle Xk1 and trapezoids Xk2, Xk3. The case of αk

−

−
1 < αk can be treated

80

in similar fashion. Last, we leave Type 2 trapezoid Dt1 at the bottom of Dt.

The total wasted area of both ends of rectangles of size 1

, k = 1,

, t,

t

1
2 ·

·

2

k=1 h1 ·

) + O(d5/6
P

is less than
O(d5/6
t
1
S(Xk1) + S(Xk2) + S(Xk3) < 1
O(x1/6)O(x−
1/6)
these joints is bounded by ( 5

≤

12 tan αk < √2

· · ·
2 x1/3. By (ii), W (D11) + W (Dt1)

×⌈

) = O(x5/18). The wasted area between Dk

≤
1 and Dk is
2 (1 + 1 + √2)x1/6 +
( 5
2 + 2√2)x1/6, which implies that the total wasted area of

3(1 + √2)x−

2 (x1/3)2

1/2 + 1

−

·

2 + 2√2)x1/6

t < ( 5
4

·

√2 + 2)x1/3. Thus,

dk⌉

W

t

[k=0

< 0 +

Dk

!

√2
2

x1/3 + O(x5/18) +

5
4

(cid:18)

√2 + 2

x1/3

(cid:19)

7
4

≤

(cid:18)

√2 + 2

x1/3.

(cid:19)

8

 
Xk2

bk

Xk1

Dk−1

αk−1

αk

Dk

Xk3

Figure 7: The wasted region between Dk−1 and Dk.

4) At last, we will estimate W (F1) and W (F2). The height of the rectangle

⌊

≤

≤

× ⌈

f1⌉

x1/3, we pack

x1/3. When 0

unit squares into F1, then

h2 < min(h, h1), and the width of it, denoted by f1, satisﬁes
F1 satisﬁes 0
h2⌋ × ⌊
h2 ≤
f1 ∼
W (F1) < h2 + f1 < 2x1/3. When x1/3 < h2 ≤
of size 1

f1⌋
h, we pack F1 with rectangles

, as shown in Fig. 8, where F11, F12 are Type 2 trapezoids.
Since W (F11) + W (F12) = O(x5/18), the total wasted area of both ends of the
√2
2 x1/3, so W (F1) <
√2x−
2 x1/3 < x1/3. To sum up, W (F1) < 2x1/3. We estimate W (F2)
2 h2 tan θ < 1
8 x1/3.
2 x1/3. Therefore,

2/3, W (F2) < S(F2) < 1
1 tan θ < 1

rectangles of size 1
O(x5/18) + √2

in two cases, too. When 0 < θ < x−

1/2, W (F2) < S(F2) < 1

is less than h

θ < √2x−

f1⌉

× ⌈

2/3

1/6

∼

·

When x−
W (F2) < 1

≤

2 x1/3 which implies W (F )

≤

2 h2
W (F1) + W (F2) < 5

2 x1/3.

85

90

f1

F11

⌈f1⌉

F1

F12

h2

Figure 8: Packing F1 in the case of x1/3 < h2 ≤ h.

9

Now, it follows from 1), 2), 3), 4) that the total wasted area

W (T3)

0 +

≤

1
4

x1/3 + (

7
4

√2 + 2)x1/3 +

5
2

x1/3 = (

19
4

+

7
4

√2)x1/3

which completes the induction step. For x

100, W (T1)

(1 + c)x. Because

≤

≤

7, (1 + c)x3/8 < 48 < 15√2 + 38 < (15 + c)√2 + 38, W (T1)

(1 + c)x <

c

≤

((15 + c)√2 + 38)x5/8, the proof of the initial step of the induction is completed.

≤

95

4. Covering Waste Problem

Similarly, we can obtain the result of Covering Waste Problem. Note that

in type 3 shape Trapezoid T3, a top edge of length a is modiﬁed, a =

√2 x1/6

.

⌋

Theorem 2. Keep the notations above. Then

x1/3

⌊

−

100

(i) W ′(T1)

(ii) W ′(T2)

(iii) W ′(T3)

≤

≤

≤

((15 + c)√2 + 38)x5/8.

2

2 + 7
( 19
4 + 7
( 19

4

√2)x5/6.

√2)x1/3.

Specially, when T1 is a square of side length x, then W ′(x)

(16√2 + 38)x5/8.

≤

Proof.

105

(i) This can be proved in a similar argument to the one of (i) of Theorem 1.

(ii) This can be proved in a similar argument to the one of (ii) of Theorem

1.

(iii) We consider a coverage of Type 3 trapezoid T3 with rectangles Ck, Dk, k =

1,

· · ·

, t, with height h1 =

−1/6
x
tan θ′

⌊

⌋

and a rectangle F1 with height h2 satisfying

110

0

h2 < h1. The width of Ck, denoted by ck, is set to be

x1/3

√2 x1/6

⌋ −
, and therefore the width of Dk, denoted by dk, is equal

−

⌊

width of F1, denoted by f1, equals to a + h tan θ′ and 0

+ kh1 tan θ′, k = 1,

⌋

· · ·

, t. It is easy to verify that the
2 x2/3 tan θ′. Set

t < 1

≤

≤
x1/3

⌊
to

−
x1/3

⌊

−

(√2 + k)x1/6

⌋

(√2 + k)x1/6

10

Ek = Dk \

T3, k = 1,

, t, F2 = F1 \

T3 (see Fig. 9), then

T3 =

W ′(T3)

≤

· · ·

Ck

t

[k=1
t

t

Dk

[k=1
t

!

[

F1 \   

t

!

[

W ′(Ck) +

S(Ek) + W ′

t

Ek

[k=1

Dk

Xk=1

[k=1

F2

,

!

!

[

+ W ′(F1) + W ′(F2).

!

Xk=1

h1
h1

h1
h2

C1
C2

D1
D2

E1
E2

θ

Dt

Et
F2

Ct

F1

Figure 9: Covering Type 3 trapezoid.

115

1) Obviously,

t
k=1 W ′(Ck) = 0.

t

2)

t
P
k=1 S(Ek) =

P

3) We estimate W ′(

Xk=1

h2
1 tan θ′

1
2
t
k=1 Dk) as follows. For k = 1,

x1/3.

1
4

≤

Dk with rectangles of size 1

dk⌉
(iii) of Theorem 1, we can obtain

× ⌈

S

· · ·
and estimate αk more accurately. Similar to

, t, we want to cover

αk −

|

αk

1| ≤

−

3(1 + √2)x−

1/2, k = 2,

, t.

· · ·

120

When rectangles of size 1

of Dt. Second, for k = t,

We cover Dk as follows. First, we leave Type 2 trapezoid Dt1 at the bottom
dk⌉
× ⌈
1, we cover

, 2, we cover Dk with rectangles of size 1
dk⌉
× ⌈
there are a triangle Xk1 and trapezoids Xk2, Xk3 between Dk

× ⌈
1 with rectangles of size 1

cover the right lower point of Dk

, as shown in Fig. 10. When αk

−
1 and Dk needed

1 ≥

αk,

Dk

1⌉

· · ·

dk

−

−

−

.

−

to be solved further in the following. As shown in the ﬁgure, bk is the bottom

edge of Xk3. The case of αk

−

1 < αk can be treated similarly. At last, we leave

Type 2 trapezoid D11 at the top of D1.

11

 
 
 
Xk2

αk−1

Dk−1

bk

Xk3
Xk1

αk

Dk

Figure 10: The wasted area between Dk−1 and Dk for covering.

The total wasted area of both ends of the rectangles of size 1

1,

· · ·

, t, is less than

2, W ′(D11) + W ′(Dt1)
P

t

1
2 ·

2
k=1 h1 ·
·
) + O(d5/6
O(d5/6
1
≤

t

12 tan αk < √2

, k =
2 x1/3. By (ii) of Theorem
) = O(x5/18). It is easy to see that

dk⌉

× ⌈

ck

1 −

−

ck, the height of Xk2, is an exact integer. Let the bottom edge of Xk2

be b′k2. We cover Xk2 with rectangles of size (ck
area between Dk
1/2 + 1

b′k2⌉
1 and Dk is S(Xk1) + W ′(Xk2) + S(Xk3) < 1

√2)x−
that the total wasted area of these joints is bounded by ( 5

2 (1+1+√2)x1/6 +O(x1/6)O(x−

3(1 +
( 5
2 +2√2)x1/6, which implies
2 + 2√2)x1/6
t <

. The wasted

2 (x1/3)2

1 −

1/6)

× ⌈

ck)

≤

−

−

·

·

( 5
4

√2 + 2)x1/3. Thus,

W ′

t

[k=0

< 0 +

Dk

!

√2
2

x1/3 + O(x5/18) +

5
4

(cid:18)

√2 + 2

x1/3

(cid:19)

7
4

≤

(cid:18)

√2 + 2

x1/3.

(cid:19)

125

4)At last, W ′(F1) + W ′(F2) < 5

2 x1/3. The proof is similar to 4) of (iii) of

Theorem 1.

By 1), 2), 3), 4), we obtain the total wasted area

W ′(T3)

0 +

≤

x1/3 +

1
4

7
4

(cid:18)

√2 + 2

x1/3 +

(cid:19)

x1/3 =

5
2

19
4

+

7
4

(cid:18)

√2

x1/3.

(cid:19)

The proof of the induction step is omitted.

12

 
References

[1] P. Erd¨os, R. L. Graham, On packing squares with equal squares, J. Combin.

130

Theory Ser. A 19 (1975) 119–123.

[2] K. F. Roth, R. C. Vaughan, Ineﬃciency in packing squares with unit

squares, J. Combin. Theory Ser. A 24 (1978) 170–186.

[3] W. Stromquist, Packing unit squares inside squares i, ii, iii, unpublished

manuscripts.

135

URL http://www.walterstromquist.com/publications.html

[4] W. Stromquist, Packing 10 or 11 unit squares in a square, Electron. J.

Combin. 10 (2003) #R8.

[5] D. Karabash, A. Soifer, Note on covering a square with equal squares,

Geombinatorics 18 (2008) 13–17.

140

[6] F. Chung, R. Graham, Packing equal squares into a large square, J. Com-

bin. Theory Ser. A 116 (2009) 1167–1175.

[7] E. Friedman, Packing unit squares in squares: A survey and new results,

Electron. J. Combin. (2009) #DS7.

[8] W. Bentz, Optimal packings of 13 and 46 unit squares in a square, Electron.

145

J. Combin. 17 (2010) #R126.

[9] D. Karabash, A. Soifer, A sharp upper bound for cover-up squares, Geom-

binatorics 16 (2006) 219–226.

[10] A. Soifer, Covering a square of side n + ε with unit squares, J. Combin.

Theory Ser. A 113 (2006) 380–388.

150

[11] E. Friedman, D. Paterson, Covering squares with unit squares, Geombina-

torics 15 (2006) 130–137.

[12] J. Januszewski, A note on covering a square of side length 2 + ε with unit

squares, Amer. Math. Monthly 19 (2009) 174–178.

13

