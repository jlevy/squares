Packing Unit Squares in a Rectangle

Hiroshi Nagamochi
Department of Applied Mathematics and Physics, Kyoto University
Sakyo, Kyoto-city, Kyoto 606-8501, Japan
nag@amp.i.kyoto-u.ac.jp

Submitted: Sep 29, 2004; Accepted: Jul 8, 2005; Published: Jul 30, 2005.
Mathematics Subject Classi(cid:12)cations: 05B40, 52C15

Abstract

For a positive integer N , let s(N ) be the side length of the minimum square into
which N unit squares can be packed. This paper shows that, for given real numbers
a; b (cid:21) 2, no more than ab − (a + 1 − dae) − (b + 1 − dbe) unit squares can be packed
in any a0 (cid:2) b0 rectangle R with a0 < a and b0 < b. From this, we can deduce that,
for any integer N (cid:21) 4, s(N ) (cid:21) minfd
N c + 1 + 1g. In particular,
N e;
for any integer n (cid:21) 2, s(n2) = s(n2 − 1) = s(n2 − 2) = n holds.

N − 2b

q

p

p

1 Introduction

Packing geometric objects such as circles and squares into another object is one of the
fundamental problems in combinatorial geometry [1, 2, 4]. For a positive integer N, let
s(N) be the side length of the minimum square that can contain N unit squares in the
plane whose interiors do not overlap. The problem of packing unit squares into a square
was initiated by Erd}os and Graham [2]. They prove that, for a large number s, unit
squares can be packed into an s (cid:2) s square so that the wasted area is O(s7=11). This is
surprisingly small compared with the wasted area in the ‘trivial’ packing of N = n2 − n
unit squares in an n (cid:2) n square, where n is an integer more than 1.

[1]. We easily observe that for any positive integer N,

Determining or estimating s(N) is posed as one of the unsolved geometric problems
N (cid:20)
listed by Croft et al.
p
N e, and that for any square number N = n2, s(N) = n. It was conjectured
s(N) (cid:20) d
that s(n2−n) = n holds for integers n (cid:21) 2 (whenever n is small). For n (cid:21) 17, s(n2−n) < n
is demonstrated by an explicit construction (see [3]). Friedman [3] conjectures that, once
s(n2 − k) = n holds for some integers n and k, s((n + 1)2 − k) = n + 1 holds. Determining
s(N) for non-square numbers N seems rather di(cid:14)cult. Currently such s(N) has been
determined only for some limited numbers N < 100 (see [3, 5]). These nontrivial values
for s(N) are based on lower bounds which are established in a particular way for each N.

p

the electronic journal of combinatorics 12 (2005), #R37

1

In this paper, we introduce a lower bound on s(N) that is systematically constructible
for any integer N (cid:21) 4. For two positive real numbers a and b, let (cid:23)(a; b) denote the
maximum number of unit squares that can be packed into the inside of an a0 (cid:2) b0 rectangle
R with a0 < a and b0 < b. A trivial upper bound on (cid:23)(a; b) is (cid:23)(a; b) < ab. In this paper,
we prove the following result.

Theorem 1 For real numbers a; b (cid:21) 2, (cid:23)(a; b) < ab − (a + 1 − dae) − (b + 1 − dbe). 2

In particular, for two integers a (cid:21) b (cid:21) 2, we see that an a (cid:2) b rectangle is the smallest
rectangle with aspect ratio a=b into which ab − 2 unit squares can be packed. Theorem 1
also provides a new lower bound on s(N), determining s(N) for in(cid:12)nitely many new
numbers N.

Theorem 2

(i) For any positive integer N such that N 2 fn2; n2 − 1; n2 − 2g for some

integer n (cid:21) 1, s(N) = n holds.

(ii) For any integer N (cid:21) 4 such that N 62 fn2; n2 − 1; n2 − 2 j

q

p

p

s(N) (cid:21)

N − 2b

N c + 1 + 1 >

N .

integers n (cid:21) 1g,

2

p

Note that our new lower bound in Theorem 2(ii) is strictly stronger than the trivial
N . This paper is organized as follows. After deriving Theorem 2 from
lower bound
Theorem 1 in section 2, we de(cid:12)ne an unavoidable set U in section 3, showing that proving
the unavoidability of U implies Theorem 1.
In section 5, we present a proof for the
unavoidability of U after preparing a series of technical lemmas in section 4. We make
concluding remarks in section 5.

2 Proof of Theorem 2

q

q

q

p

p

p

p

p

p

p

Ne =

N = d
p

N + 2 − (d

Then we have

N c + 1 + 1 =
p

N − 2b
p
Ne)2 + (b
p

N e. Now assume that
q
p

N c + 1 + 1 and inequality
p

This section shows that Theorem 2 follows from Theorem 1. Any square number N = n2
N + 2 (cid:21)
N − 2b
satis(cid:12)es s(N) = n =
p
Nc + 1 holds.
N is not an integer, for which d
d
p
p
N c + 1 + 1
N − (d
q
Nc + 1 if and
Ne if and only if
N, i.e., n2 (cid:21) N (cid:21) n2 − 2. It is known
p
p

=
N + 2 (cid:21) d
only if
there is an integer n such that
that s(1) = 1 and s(2) = s(3) = s(4) = 2 [4]. Let N (cid:21) 4.

N e. Then by Theorem 1 with a =
Ne)2 − 2 (cid:20) N. This says that N
N e. Thus,
N e. So for any integer N 2 fn2; n2 − 1; n2 − 2g, where n (cid:21) 1 is an integer, we

b = d
unit squares cannot be packed in any square with side length less than d
s(N) (cid:21) d
have s(N) (cid:21) n = d

We (cid:12)rst consider the case where
N e (cid:21) 2, we have (cid:23)(d
p

N − 2b
Ne. A positive integer N satis(cid:12)es
p

Ne = b
N c + 1)2 − 2b
p

p
N + 2 (cid:21) d
p
N e) < (d

Nc + 1 + 1 (cid:21) b
p
N + 2 (cid:21) d

Ne (cid:21) s(N). This proves (i).

N c)2 + 1. Hence

Ne)2 + (b
p

N + 2 (cid:21) n (cid:21)

N e; d

p

p

p

p

p

p

the electronic journal of combinatorics 12 (2005), #R37

2

p

p

p

q

p

p
p

N − 2b

N + 2 < d

We next consider the case where

Nc (cid:21) 2 and (cid:11) =
N c + 1. Note that (cid:11) is a solution to ((cid:11) + k − 1)2 = N − 2k + 1.
N c + 1 − b
Ne. Hence by Theorem 1 with a = b = k + (cid:11) (cid:21) 2, we
N + 2 < d
Note that (cid:11) < 1 since
have (cid:23)(k +(cid:11); k +(cid:11)) < (k +(cid:11))2 −2((cid:11)+1−d(cid:11)e) = (k +(cid:11))2 −2(cid:11) = (k +(cid:11)−1)2 +2k −1 = N.
Therefore, N unit squares cannot be packed in any square with side length less than
N c + 1 + 1. Furthermore, we
k + (cid:11) =

Ne. Let k = b

N − 2b

p

p

p

q

q

q

N − 2b
N − 2b

p

Nc + 1 + 1. Thus, s(N) (cid:21)
q
N c + 1 + 1 >

N − 2

p

see that

N + 1 + 1 =

N . This proves (ii).

p

3 Unavoidable Sets

The conventional method for deriving a lower bound on s(N) [3] is as follows. Suppose
that we wish to show s(N) (cid:21) a. Let R be a square with side length less than a, and U
be a set of some points inside R, where U is called unavoidable if any unit square placed
inside R must contain at least one point from U. If we successfully obtain an avoidable
set U with jUj < N, then we can conclude that jUj + 1 unit squares cannot be packed
inside R, i.e., s(N) (cid:21) s(jUj + 1) (cid:21) a. For example, let N = 2. Take a square R with
side length less than a = 2. Then we easily see that U consisting of the center of R is
unavoidable, and thereby we need a square R with side length at least a = 2 to pack two
unit squares, i.e., s(2) (cid:21) 2. An unavoidable set U with jUj < N over a smaller square
R provides a better lower bound on s(N). Only for few integers N < 100, have such
unavoidable sets been constructed to obtain nontrivial lower bounds on s(N). However,
these constructions are not systematic in terms of N, providing no general lower bound
on s(N) for large N.

In this paper, we use not only points but also other geometric objects such as line
segments and rectangles to de(cid:12)ne our unavoidable set U. Recall that the trivial lower
bound s(N) (cid:21)
N follows from the fact that each unit square consumes at least area 1
from the entire square R, where R can be regarded as an unavoidable set from which unit
square takes score 1.

p

In the xy-plane, a line segment L connecting two points p1 = (x1; y1) and p2 = (x2; y2)
is denoted by L = [p1; p2] or L = [(x1; y1); (x2; y2)]. A rectangle R0 with edges parallel
with x-, y-axes may be written as [x1; x2] (cid:2) [y1; y2] if the four corners of R0 are given by
(x1; y1); (x1; y2); (x2; y1) and (x2; y2) for real numbers x1 (cid:20) x2 and y1 (cid:20) y2.

To prove (cid:23)(a; b) < ab − (a + 1 − dae) − (b + 1 − dbe) for given real numbers a; b (cid:21) 2,
we consider a rectangle R = [0; a] (cid:2) [0; b] in the xy-plane. Let U consist of a rectangle
R(cid:3), four lines Li (i = 1; 2; 3; 4), a set Q of eight points, and a set P of 2dae + 2dbe − 12
points, such that

R(cid:3) = [1; a − 1] (cid:2) [1; b − 1];
L1 = [(0:9; 1); (a − 0:9; 1)]; L2 = [(0:9; b − 1); (a − 0:9; b − 1)];
L3 = [(1; 0:9); (1; b − 0:9)]; L4 = [(a − 1; 0:9); (a − 1; b − 0:9)];
Q = f(0:9; 1); (a − 0:9; 1); (0:9; b − 1); (a − 0:9; b − 1);

the electronic journal of combinatorics 12 (2005), #R37

3

(1; 0:9); (1; b − 0:9); (a − 1; 0:9); (a − 1; b − 0:9)g;

P = f(i; 0:9); (i; a − 0:9) j i = 2; 3; : : : ; dae − 2g

[ f(0:9; j); (b − 0:9; j) j j = 2; 3; : : : ; dbe − 2g:

See Fig. 1.

(0,b)

1+a- | a | - -

(a,b)

Q

P

1+b- | b | - -

Q

P

P

P

Q

Q

P

Q

Q

L3

R*

L2

L1

}}
P

score 0.05

P

score 0.5

score 0.45

score 0.5

L4

Q

Q

P

0.9

(0,0)

(a,0)

Figure 1: An unavoidable set U for a rectangle R = [0; a] (cid:2) [0; b].

Let (cid:21) > 1. We say that R and U are shrunken toward the origin (0; 0) by factor (cid:21)−1
if we map each point (x; y) in R and U to a new point ((cid:21)−1x; (cid:21)−1y). Let (cid:21)−1R and (cid:21)−1U
respectively denote such R and U shrunken by factor (cid:21)−1.

For a given unit square S inside (cid:21)−1R and an object K 2 fQ; P; L1; L2; L3; L4; R(cid:3)g,

we de(cid:12)ne score (cid:27)(S; K) of S by K as follows.

(cid:15) (cid:27)(S; R(cid:3)) =(the area of the intersection of S and R(cid:3)) (cid:2)(cid:21)2,

(cid:15) (cid:27)(S; Li) =(the sum of length of the intersection of S and line segment Li)(cid:2)0:5 (cid:2) (cid:21),

(cid:15) (cid:27)(S; Q) =(the number of points in Q contained in S)(cid:2)0:45, and

(cid:15) (cid:27)(S; P ) =(the number of points in P contained in S)(cid:2)0:5.

De(cid:12)ne

(cid:27)(S) = (cid:27)(S; R(cid:3)) + (cid:27)(S; L1) + (cid:27)(S; L2) + (cid:27)(S; L3) + (cid:27)(S; L4) + (cid:27)(S; Q) + (cid:27)(S; P ):
Note that the total score from Li (i = 1; 2; 3; 4) and Q is 2(a − 1:8) (cid:2) 0:5 + 2(b − 1:8) (cid:2)
0:5+8(cid:2)0:45 = a+b. Then the total score from U is (a−2)(b−2)+a+b+dae−3+dbe−3 =
ab − (a + 1 − dae) − (b + 1 − dbe). In what follows, we prove that U is an unavoidable set
in the following sense.

the electronic journal of combinatorics 12 (2005), #R37

4

Lemma 1 Any unit square S inside (cid:21)−1R satis(cid:12)es (cid:27)(S) > 1.

2

We show that Theorem 1 follows from Lemma 1. Assume that N 0 unit squares are
packed inside (cid:21)−1R. Each of the N 0 unit squares has (cid:27)(S) > 1 by Lemma 1 and the total
score of U is ab−(a+1−dae)−(b+1−dbe). Then we have N 0 < ab−(a+1−dae)−(b+1−dbe)
for any factor (cid:21)−1 < 1, i.e., (cid:23)(a; b) < ab − (a + 1 − dae) − (b + 1 − dbe), as required.

A square S with side length (cid:21) is called a (cid:21) (cid:2) (cid:21) square. For a notational convenience to
prove Lemma 1, we consider packing (cid:21) (cid:2) (cid:21) squares with (cid:21) > 1 into the original rectangle
R = [0; a] (cid:2) [0; b], instead of considering (cid:21)−1R and (cid:21)−1U. In this case, each Li contributes
to (cid:27)(S) by 0.5 per length and R(cid:3) by 1 per area while each point in Q (resp., P ) contributes
to (cid:27)(S) by 0.45 (resp., 0.5). It su(cid:14)ces to show that any (cid:21) (cid:2) (cid:21) square S with (cid:21) 2 (1; 1:01]
has (cid:27)(S) > 1 over the original R and U.

4 Technical Lemmas

In this section, we prepare some technical lemmas in order to establish a proof of Lemma 1
in the next section. Let (cid:21) 2 [1; 1:01] for a technical reason to prove the lemmas in this
section.

p

Lemma 2 Let S be a (cid:21) (cid:2) (cid:21) square with (cid:21) 2 [1; 1:01]. For a line L with distance h 2
2 − 1)=2) from the center of S, let c be the length of the intersection of S and L (see
[0; (
Fig. 2(a)). Then c (cid:21) (cid:21) or c > 1.

Proof: Let L intersect edges e1 and e2 of S. If e1 and e2 are not adjacent, then c (cid:21) (cid:21).
We consider the case where e1 and e2 are adjacent. We can assume that (cid:21) = 1 to estimate
the minimum c. Let (cid:18) denote the angle made by L and e2, where 0 < (cid:18) (cid:20) (cid:25)=4 is assumed
without loss of generality. Let t = tan((cid:18)=2), where 0 < t = tan((cid:18)=2) (cid:20)
2 − 1 for
(cid:18) 2 (0; (cid:25)=4]. Then we have

p

c = −h

(1 + t2)2
2t(1 − t2)

+

(1 + t2)(1 + 2t − t2)
4t(1 − t2)

;

which is a decreasing function of h for a (cid:12)xed t. Hence it su(cid:14)ces to show that f (h; t) =
−2h(1 + t2)2 + (1 + t2)(1 + 2t − t2) − 4t(1 − t2) is nonnegative for h = (
2 − 1)=2. We
have

p

p

f (

2 − 1
2

; t) = (t + 1 −
p

p

p

2)2(−
p
p

2t2 + (2 + 2

p

By the concavity of g(t) = −
mean g(t) > 0 (0 < t (cid:20)

2t2 + (2 + 2
2 − 1). Hence f ((

p

2)t + 2 +
2 − 1)=2; t) (cid:21) 0 and c > 1.

2, g(0) > 0 and g(

p

p

2)t + 2 +

2):

p

2 − 1) > 0

2

Lemma 3 Let S be a (cid:21) (cid:2) (cid:21) square with (cid:21) 2 [1; 1:01] such that one corner of S touches
the x-axis and S is entirely above the x-axis. For a line L : y = h with h 2 (0:5;
2 − 0:5),
let c be the length of the intersection of S and L (see Fig. 2(b)). Then c (cid:21) (cid:21) or c > 1.

p

the electronic journal of combinatorics 12 (2005), #R37

5

L

e
1

θ

e

2

S

c

(a)

h

L

e

2
θ

e
1

h

c

S

θ

(b)

Figure 2: (a) Illustration for Lemma 2; (b) Illustration for Lemma 3.

Proof: Let L intersect edges e1 and e2 of S. We consider the case where e1 and e2 are
adjacent (otherwise c (cid:21) (cid:21)). By h > 0:5, both e1 and e2 are not touching the x-axis.
We can assume that (cid:21) = 1 to estimate the minimum c. Let (cid:18) be angle made by L and
e2, where 0 < (cid:18) (cid:20) (cid:25)=4 is assumed without loss of generality. Let t = tan((cid:18)=2), where
0 < t = tan((cid:18)=2) (cid:20)

2 − 1) for (cid:18) 2 (0; (cid:25)=4]. Then we have

p

c = −(h − 1)

(1 + t2)2
2t(1 − t2)

+

2t(1 − t + t2 − t3)
2t(1 − t2)

;

which is a decreasing function of h for a (cid:12)xed t. To prove the lemma, it su(cid:14)ces to show
that f (h; t) = −(h − 1)(1 + t2)2 + 2t − 2t2 + 2t3 − 2t4 − 2t + 2t3 (cid:21) 0 for h =
2 − 0:5. We
see that

p

p

f (

2 − 0:5; t) = (t + 1 −
p

p

2)2(−(1 + 2
p
p

By the concavity of g(t) = −(1 + 2
mean g(t) > 0 (0 < t <

2)t2 + (2
2 − 1). Therefore f (

p

2 + 2)t + 1, g(0) > 0 and g(
2 − 0:5; t) (cid:21) 0 and c > 1.

p

2)t2 + (2

p

2 + 2)t + 1):

p

2 − 1) > 0

2

Lemma 4 Let S be a (cid:21) (cid:2) (cid:21) square with (cid:21) 2 [1; 1:01], and e1 and e2 be two adjacent
edges of S that meet at a corner v of S. For a point p1 on e1 and a point p2 on e2 with
p1 6= v 6= p2, let c be the length of the line segment L = [p1; p2], and d be the area of the
triangle enclosed by L and line segments [p1; v] and [v; p2] (see Fig. 3). Then 0:5c > d. 2

p

Proof: Let h and ‘ be the lengths of the line segments [p1; v] and [v; p2], respectively. Then
h2 + ‘2 and d = h‘=2. To prove c=2 > d, it su(cid:14)ces to show that h2 + ‘2 − h2‘2 > 0.
c =
Since h; ‘ 2 (0; (cid:21)], we have h2 + ‘2 − h2‘2 = (h − ‘)2 + h‘(2 − h‘) (cid:21) h‘(2 − (cid:21)2) > 0. 2

the electronic journal of combinatorics 12 (2005), #R37

6

e

2

p
2

v

T
d

cL

S

e1

p
1

Figure 3: Illustration for Lemma 4.

Lemma 5 Let S be a (cid:21) (cid:2) (cid:21) square with (cid:21) 2 [1; 1:01] such that one corner of S touches
the x-axis and S is entirely above the x-axis, c > 0 be the length of the intersection of S
and line L : y = 1, and d be the area of the triangle enclosed by S and L (see Fig. 4(a)).
Then d + 0:5c > 0:5.

Proof: Let (cid:18) 2 (0; (cid:25)=4] be the angle made by an edge of S and the x-axis, and t =
tan((cid:18)=2). We obtain d = c2 (cid:2) t(1 − t2)=(1 + t2)2. We denote c and d for (cid:21) = 1 by (cid:22)c and (cid:22)d.
Then we have 1−(cid:22)c = (cid:22)d = (t−t2)=(1+t), for which (cid:22)d+0:5(cid:22)c = 1−(cid:22)c+0:5(cid:22)c = 0:5+0:5(1−(cid:22)c) >
0:5. Now consider the case of (cid:21) > 1. Since (cid:21) − 1 is small, we can write c = (cid:22)c + x and
d = ((cid:22)c + x)2 (cid:2) t(1 − t2)=(1 + t2)2 = (cid:22)d + (2(cid:22)c + x2) (cid:2) t(1 − t2)=(1 + t2)2 for some number
x > 0. Then d + 0:5c = (cid:22)d + 0:5(cid:22)c + 0:5x + (2(cid:22)c + x2) (cid:2) t(1 − t2)=(1 + t2)2 (cid:21) (cid:22)d + 0:5(cid:22)c > 0:5. 2

θ

d

c

S

θ

(a)

1

c`{ p`

x=1

d

c

θ

(b)

(2,0.9)

1

x=2

Figure 4: (a) Illustration for Lemma 5; (b) Illustration for Lemma 6.

the electronic journal of combinatorics 12 (2005), #R37

7

Lemma 6 Let S be a (cid:21) (cid:2) (cid:21) square with (cid:21) 2 [1; 1:01] such that one corner of S touches
the x-axis and S is entirely above the x-axis. Assume that two adjacent edges e1 and e2
of S intersect line L : y = 1, point (1; 1) is not in S, point (2; 0:9) is on an edge e2 of S.
Let c be the length of the intersection of S and L, d be the area of the triangle enclosed
by S and L, and p0 = (1; 1 − c0) be the crossing point of e1 and line x = 1 (see Fig. 4(b)).
Then d + 0:5c + 0:5 − 0:5c0 > 1 holds.

2

Proof: For values d, c, −c0 for a (cid:21) (cid:2) (cid:21) square S with (cid:21) > 1, we can get smaller d, c,
−c0 choosing a (cid:21)0 (cid:2) (cid:21)0 square S with 1 (cid:20) (cid:21)0 < (cid:21). Then we only consider the case of
(cid:21) = 1. Let (cid:18) 2 (0; (cid:25)=2] be the angle made by e1 and L : y = 1. By calculation, we have
d = t(1 − t)=(1 + t), c = (t + t2)=(1 + t), and c0 = 2t(t(1 − t)2 − 0:2t)=(1 − t2)2. To have
c0 > 0 (i.e., to keep (1; 1) outside S), t(1 − t)2 − 0:2t > 0 (i.e., t < 1 −
0:2) must hold.
Note that c = 1 − d holds. To prove d + 0:5c + 0:5 − 0:5c0 > 1, it su(cid:14)ces to show that
d > c0, i.e.,

p

t(1 − t)
1 + t

>

2t(t(1 − t)2 − 0:2t)
(1 − t2)2

;

(0 < t < 1 −

0:2):

p

For this, we show f (t) = (1 − t)2(1 − t2) − 2(t(1 − t)2 − 0:2t) (cid:21) 0. We have f (t) =
(1 − t)2(2 − (1 + t)2) + 0:4t, which is positive for 0 < t (cid:20)
2 − 1. On the other hand, for
0:2 < 0:56, we have (1 − 0:41)2(2 − (1 + 0:56)2) + 0:4 (cid:1) 0:41 > 0.
0:41 <
This completes the proof of the lemma.

2 − 1 < t < 1 −

p

p

p

2

5 Proof of Lemma 1

Throughout this section, S denotes a (cid:21) (cid:2) (cid:21) square with (cid:21) 2 (1; 1:01] that is entirely
contained in a given a (cid:2) b rectangle R = [0; a] (cid:2) [0; b]. We prove that (cid:27)(S) > 1, from
which Lemma 1 follows. We distinguish the following seven cases:

Case-1: S is contained completely inside R(cid:3) = [1; a − 1] (cid:2) [1; b − 1].

Case-2: S is not completely contained inside R(cid:3), the center of S is inside R(cid:3), S does not
contain any point in Q as its interior point, and there is no line segment Li 2 U
that intersects two nonadjacent edges of S.

Case-3: The center of S is inside R(cid:3), S does not contain any point in Q as its interior

point, and there is a line segment Li that intersects two nonadjacent edges of S.

Case-4: The center of S is inside R(cid:3), and S contains a point in Q as its interior point.

Case-5: The center of S belongs to the rectangle [0; 1] (cid:2) [0; 1].

Case-6: The center of S belongs to the rectangle [1; a−1](cid:2)[0; 1], and line y = 1 intersects

two adjacent edges of S.

the electronic journal of combinatorics 12 (2005), #R37

8

Case-7: The center of S belongs to the rectangle [1; a−1](cid:2)[0; 1], and line y = 1 intersects

two nonadjacent edges of S.

The case where the center of S belongs to one of the rectangles [a − 1; a] (cid:2) [0; 1],
[0; 1] (cid:2) [b − 1; b] and [a − 1; a] (cid:2) [b − 1; b] can be treated analogously with Case-5. Also
the case where the center of S belongs to one of the rectangles [1; a − 1] (cid:2) [b − 1; b],
[0; 1] (cid:2) [1; b − 1] and [a − 1; a] (cid:2) [1; b − 1] can be treated in a similar way of Cases-6 and 7.
In Case-1, we easily see that (cid:27)(S) (cid:21) (cid:27)(S; R(cid:3)) = (cid:21)2 > 1 holds. The rest of the cases

will be discussed in the subsequent subsections.

5.1 Case-2
In this case, S is not completely contained inside R(cid:3), the center of S is inside R(cid:3), S does
not contain any point in Q as its interior point, and there is no line segment Li 2 U that
intersects two nonadjacent edges of S. Then there is a line segment Li 2 U that intersects
two adjacent edges of S, cutting out from S a triangle Ti that is not covered by R(cid:3) (see
Fig. 5). For each of all those line segments Li, let di be the area of the triangle Ti, and ci
be the length of the intersection of Li and S (some of these triangles may be overlapping,
as illustrated by S3 in Fig. 5). By Lemma 4, we have 0:5ci − di > 0 for all such Li. This
implies that (cid:27)(S; Li) = 0:5ci compensates the loss di in (cid:27)(S; R(cid:3)). Thus (cid:27)(S) is not less
than that of a (cid:21) (cid:2) (cid:21) square S which is completely contained in R(cid:3). Therefore, (cid:27)(S) > 1.

S3

S2

S1

Figure 5: Illustration for (cid:21) (cid:2) (cid:21) squares in Case-2.

5.2 Case-3
In this subsection, we consider the case where the center of S is inside R(cid:3), S does not
contain any point in Q as its interior point, and there is a line segment Li that intersects
two nonadjacent edges of S. The length of the intersection of Li and S is at least (cid:21) > 1.
Then if there are two such line segments Li and Li0, then (cid:27)(S) (cid:21) (cid:27)(S; Li) + (cid:27)(S; Li0) (cid:21)
(cid:21) (cid:2) 0:5 (cid:2) 2 > 1. Assume that there is exactly one such line segment Li, which cuts out
from S an quadrangle uncovered by R(cid:3). From the above observation using Lemma 4,

the electronic journal of combinatorics 12 (2005), #R37

9

we can assume that there is no other line segment Lj 2 U that cuts out from S an
uncovered triangle Tj. Since the center is in R(cid:3) and (cid:27)(S; R(cid:3)) (cid:21) 0:5(cid:21)2, we have (cid:27)(S) (cid:21)
(cid:27)(S; R(cid:3)) + (cid:27)(S; Li) (cid:21) 0:5(cid:21)2 + 0:5(cid:21) > 1.

5.3 Case-4
In this case, the center of S is inside R(cid:3), S contains a point in Q as its interior point.
We show that this case can be reduced to Case-2. Assume that S contains point (1; 0:9)
(the case where S contains other point in Q can be treated analogously). To estimate
the minimum (cid:27)(S), we temporarily replace the point (1; 0:9) with line segment L0 =
[(1; 0:9); (1; 0)], setting the score of L0 per length to be 0.5 (note that the total score of
L0 is 0.45, the same as that of point (1; 0:9)). If S contains other points in Q, we replace
each of them in a similar manner. With this modi(cid:12)cation, the score of S never increases
and the argument in Case-2 can be applied, indicating (cid:27)(S) > 1.

5.4 Case-5

We start with the following lemma to handle Cases-5, 6 and 7.

Lemma 7 Let S be a (cid:21) (cid:2) (cid:21) square with (cid:21) 2 (1; 1:01] that is entirely contained in R.
Assume that the center of S belongs to the rectangle [0; a] (cid:2) [0; 1]. Then

(i) The length c of the intersection of S and line L : y = 0:9 is more than 1.

(ii) If the center of S belongs to the square [0; 1] (cid:2) [0; 1], then S contains three points

(1; 1) and (1; 0:9); (0:9; 1) 2 Q as its interior points.

(iii) S contains at least one point in Q [ P .

(iv) (cid:27)(S; R(cid:3)) > 0.

Proof: (i) If L intersects two nonadjacent edges of S, then c (cid:21) (cid:21) > 1. Assume that L
intersects two adjacent edges of S. If the center is below L then we only have to consider
the case where one corner of S touches the x-axis, and in this case c > 1 follows from
Lemma 3 with h = 0:9. In the other case (i.e., the center of S is situated between L and
line y = 1), c > 1 holds by Lemma 2 with h = 0:1.

(ii) It is known that any unit square inside the (cid:12)rst quadrant whose center is in
[0; 1] (cid:2) [0; 1] contains the point (1; 1) (for example, see [3]). Then S contains (1; 1) as
its interior point since (cid:21) > 1. We show that S contains (1; 0:9) (we can show that S
contains (0:9; 1) analogously). By (i), S contains one of the points (0; 0:9) and (1; 0:9).
Assume that S contains (0; 0:9) but not (1; 0:9). This can occur only when one corner of
S attaches the y-axis at the point (0; 0:9). Let e and e0 be the edges of S that are not
incident to the point (0; 0:9). Since any point on e and e0 has distance at least (cid:21) > 1 from
the (0; 0:9), S must contain (1; 0:9) as its interior point.

(iii) Immediate from (i) and (iii).

the electronic journal of combinatorics 12 (2005), #R37

10

(iv) We easily see that (cid:27)(S; R(cid:3)) > 0 holds from (cid:21) > 1 if the center of S belongs to the

rectangle [1; a − 1] (cid:2) [0; 1]; (cid:27)(S; R(cid:3)) > 0 holds from (ii) otherwise.

2

In Case-5, the center of S belongs to the rectangle [0; 1] (cid:2) [0; 1]. Then by Lemma 7(ii)
S contains (1; 0:9); (0:9; 1) 2 Q and line segments [(1; 0:9); (1; 1)] and [(0:9; 1); (1; 1)], and
thereby (cid:27)(S) (cid:21) (cid:27)(S; R(cid:3)) + 0:45 (cid:2) 2 + 0:1 (cid:2) 2 (cid:2) 0:5 > 1.

5.5 Case-6

In this case, the center of S belongs to the rectangle [1; a − 1] (cid:2) [0; 1], and line y = 1
intersects two adjacent edges e1 and e2 of S. Let L0 be the line segment obtained as the
intersection of line y = 1 and S, c be the length of L0, and d be the area of the triangle
T enclosed by L0, e1 and e2.

We (cid:12)rst assume that S contains a point in P and none of points (0:9; 1); (a−0:9; 1) 2 Q.
Then L0 is contained in L1. To estimate the minimum of d + 0:5c in this case, we can
assume that one corner of S touches the x-axis. Assume that triangle T is contained
in R(cid:3). Since S contains T , L0 and a point in P , we have (cid:27)(S) (cid:21) d + 0:5c + 0:5 > 1
by Lemma 5. Even if T has an intersection with L2, (cid:27)(S) > 1 still holds by applying
Lemma 4 to the triangle T 0 enclosed by L2 and S.

We next consider the case where S contains a point in P and at least one of points
(0:9; 1); (a − 0:9; 1) 2 Q (say (0:9; 1)). Then S contains line segment [(0:9; 1); (1; 1)] and
hence (cid:27)(S) (cid:21) (cid:27)(S; R(cid:3)) + 0:5 + 0:45 + 0:05 > 1.

We now consider the case where S contains no point in P . Then, by Lemma 7(iii), S
contains at least one of points (1; 0:9); (a − 1; 0:9) 2 Q. Assume that S contains (1; 0:9)
(the case that S contains (a − 1; 0:9) can be treated analogously). If S contains point
(0:9; 1), then it contains line segments [(0:9; 1); (1; 1)] and [(1; 0:9); (1; 1)], and (cid:27)(S) (cid:21)
(cid:27)(S; R(cid:3)) + (0:45 + 0:1 (cid:2) 0:5) (cid:2) 2 > 1 holds. Similarly if S contains (a − 1; 0:9), then we
can show that S contains line segments [(a − 1; 0:9); (a − 1; 1)] and [(a − 0:9; 1); (a − 1; 1)],
implying (cid:27)(S) (cid:21) 1. Then assume that S contains none of points (0:9; 1) and (a − 1; 0:9).
If S contains point (minf2; a − 1g; 0:9) then (cid:27)(S) (cid:21) 0:45 (cid:2) 2 + d + 0:5c > 1 by Lemma 5.
Assume further that S does not contain point (minf2; a − 1g; 0:9); a (cid:21) 3 is assumed (the
case of a < 3 can be treated analogously). To estimate the minimum (cid:27)(S) in this case,
we can assume that one corner of S touches the x-axis and point (2; 0:9) is on an edge of
S. If point (1; 1) is in S, then (cid:27)(S; L3) + (cid:27)(S; Q) (cid:21) 0:5 and (cid:27)(S) (cid:21) d + 0:5c + 0:5 > 1
by Lemma 5. Assume that (1; 1) is not in S. Let p0 = (1; 1 − c0) be the crossing point
of line segment [(1; 0:9); (1; 1)] and an edge of S, where line segment [p0; (1; 1)] is not
covered by S. Note that (cid:27)(S; L1) = 0:5c and (cid:27)(S; L3) + (cid:27)(S; Q) = 0:5 − 0:5c0. Then
(cid:27)(S) (cid:21) d + 0:5c + 0:5 − 0:5c0, which is greater than 1 by Lemma 6.

5.6 Case-7

Finally we consider the case where the center of S belongs to the rectangle [1; a−1](cid:2)[0; 1],
and line y = 1 intersects two nonadjacent edges e1 and e2 of S. Let L0 be the line segment

the electronic journal of combinatorics 12 (2005), #R37

11

obtained as the intersection of line y = 1 and S, and c be the length of L0. Then c (cid:21) (cid:21) > 1
since y = 1 intersects two nonadjacent edges of S. If L0 is contained in L1 (i.e., S contains
none of (0:9; 1); (a − 0:9; 1) 2 Q) and S contains a point in P , then (cid:27)(S) (cid:21) 0:5c + 0:5 > 1.
We next consider the case where S contains one of (0:9; 1); (a − 0:9; 1) 2 Q.
If S
contains both (0:9; 1) and (a − 0:9; 1), then L1 is entirely contained in S, implying (cid:27)(S) (cid:21)
(cid:27)(S; R(cid:3)) + (0:45 + 0:05) (cid:2) 2 > 1. Assume that S contains (0:9; 1) but not (a − 0:9; 1) (the
other case can be treated analogously). By Lemma 7(iii), S contains (2; 0:9) or (1,0.9).
In any case, S contains line segment [(0:9; 1); (1; 1)] and point (2; 0:9) (or line segment
[(1; 0:9); (1; 1)]), indicating (cid:27)(S) (cid:21) (cid:27)(S; R(cid:3)) + 0:5 + 0:5 > 1.

We (cid:12)nally consider the case where L0 is contained in L1 and S contains no point in P .
Then by Lemma 7(iii) S contains (1; 0:9) or (a − 1; 0:9); We assume that (1; 0:9) is in
S (the other case can be treated analogously). If S contains (1; 1), then it also contains
line segment [(1; 0:9); (1; 1)] and satis(cid:12)es (cid:27)(S) (cid:21) 0:5c + 0:5 > 1. Hence the remaining
case is that S contains (1; 0:9) but none of (1; 1) and (minf2; a − 1g; 0:9) (see Fig. 6).
To estimate the minimum (cid:27)(S) in this case, we can assume that S touches the x-axis
(allowing it to violate the condition that y = 1 intersects two nonadjacent edges of S).
Now y = 1 intersects two adjacent edges of S and this case has already been discussed in
Case-6.

y=1

S

Figure 6:
(minf2; a − 1g; 0:9) in Case-7.

Illustration for the case where S contains (1; 0:9) but none of (1; 1) and

This completes the proof of Lemma 1.

6 Concluding Remarks

In this paper, we have established a nontrivial upper bound on the number of unit squares
that can be packed into a rectangle with given side lengths. With this bound, we have
derived a stronger lower bound on s(N) and determined that s(n2 − 1) = s(n2 − 2) = n
for all integers n (cid:21) 2. Our unavoidable set U can be seen as a modi(cid:12)cation of the entire
area R so that the total score becomes less than the area of R by replacing the boundary
part of R with a set of points and line segments with appropriate scores. This technique

the electronic journal of combinatorics 12 (2005), #R37

12

can be easily applied to the problem of packing unit squares into other types of convex
polygons such as regular k-gons (k (cid:21) 3) by modifying the de(cid:12)nition of endpoints in Q
and their scores.

Acknowledgment

We would like to express our gratitude to the anonymous referees whose suggestions
contributed to improving the written style. This research was partially supported by
a Scienti(cid:12)c Grant in Aid from the Ministry of Education, Culture, Sports, Science and
Technology of Japan.

References

[1] H. T. Croft, K. J. Falconer, and R. K. Guy, Unsolved Problems in Geometry, Springer

Verlag, Berlin (1991) 108{114.

[2] P. Erd}os and R. L. Graham, On packing squares with equal squares, J. Combin.

Theory Ser. A, 19 (1975) 119{123.

[3] E. Friedman, Packing unit squares in squares: A survey and new results, The Elec-

tronic Journal of Combinatorics, Dynamic Surveys (#DS7), (2000).

[4] F. G¨obel, Geometrical packing and covering problems, in Packing and Covering in
Combinatorics, A. Schrijver (ed.), Math Centrum Tracts, 106 (1979) 179{199.

[5] M. J. Kearney and P. Shiu, E(cid:14)cient packing of unit squares in a square, The Elec-

tronic Journal of Combinatorics, 9 (2002) (#R14).

the electronic journal of combinatorics 12 (2005), #R37

13

