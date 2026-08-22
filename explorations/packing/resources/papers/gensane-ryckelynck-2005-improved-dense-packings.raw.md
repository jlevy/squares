Discrete Comput Geom 34:97–109 (2005)
DOI: 10.1007/s00454-004-1129-z

Discrete & Computational

Geometry

© 2004 Springer Science+Business Media, Inc.

Improved Dense Packings of Congruent Squares in a Square

Thierry Gensane and Philippe Ryckelynck

LMPA, Universit´e du Littoral,
50 rue F. Buisson, BP699, 62228 Calais Cedex, France
{gensane,ryckelyn}@lmpa.univ-littoral.fr

Abstract. Let sn be the side of the smallest square into which it is possible to pack n
congruent squares. In this paper we link sn to the supremum of the maximal inﬂation ω(C)
of admissible conﬁgurations C. The computation and the properties of ω(C) and related
functions give rise to an algorithm similar to the billiard approach used to pack congruent
disks or spheres in a bounded domain. We improve the best known packings of n equal
squares for n = 11, 29 and 37, and give an alternative optimal packing of 18 squares.

1.

Introduction

Erd˝os and Graham [2] initiated the problem of maximizing the area sum of packings
of an arbitrary square by unit squares. The present paper deals with the research of the
densest packing of a given number n of unit squares in a larger square. As usual, we
denote by sn the side of the smallest square into which one can pack n unit squares.
√

Kearney and Shiu [7] proved that s6 = s7 = s8 = s9 = 3. Stromsquist [10] showed
that s10 = 3 + 1/
5. Friedman [3] gave an interesting survey,
with emphasis on the technique of “unavoidable” points which allows him to give short
proofs of optimality for n = 2, 3, 5, 8, 15, 24 and 35; he also recorded in two tables the
upper and lower bounds for sn.

2 and s11 ≥ 2 + 4/

√

In the survey [3], Friedman does not give any light on the underlying methods or
algorithms which have been used to produce optimal conﬁgurations. We give here a
heuristic approach similar to the billiard algorithms which have been used in the case
of disk packings by Graham and Lubachevsky [8], [5], see also [1] and [6]. The billiard
approach for sphere packings in a cube is treated in [4].

The billiard algorithm is implicitly based on the fact that, if K is a square, the disk
packing problem is equivalent to the maximal separation problem [9]: how to ﬁnd an

98

Th. Gensane and Ph. Ryckelynck

n-tuple P = ( p1, . . . , pn) ∈ K n which attains

δn = max
P

f (P)

where

f (P) = min

1≤i< j≤n

| pi− pj |.

In fact, the quantity f (P) represents the maximal diameter of n non-overlapping
disks centered at the points pi . Similarly, we deﬁne in Proposition 3 a function ω(C)
which gives the maximal half-diagonal of a conﬁguration C of n non-overlapping squares
contained in the square [−L , L]2. The choice of the half-diagonal as a measure of the
size of C is clear from Remark 4. The adaptation of the billiard algorithm for sphere
packings [4] into an algorithm for squares packing follows mainly from substitution of
the function ω for the function f .

In Section 2 we ﬁx notation, quote simple facts from euclidean geometry and in-
troduce the manifold of admissible conﬁgurations Qn,c. In Sections 3–5 we compute
some necessary functions ϕ, ψ: Qn,c → R+ to deﬁne the function ω and to link sn with
ω. In Section 5 we also introduce the geometric graph associated with any admissible
conﬁguration. In Section 6, we give some hints on the code that we wrote to compute
dense packings. Our results are detailed in Section 7 for the cases n = 11, 17, 18, 29
and 37.

2. Notation

Throughout the paper, n ≥ 2 is a ﬁxed integer and L > 0 is ﬁxed. We denote by B(x, ε) =
{y ∈ R2: d(x, y) < ε} the open ball of radius ε centered at x. The group of displacements
of the plane D ≈ S O(2, R) (cid:13)(cid:14) R2 is diffeomorphic to
. The
displacement g: R2 → R2 with parameters (α, β, η) acts as follows on R2:

(cid:2)
(α, β, η) ∈ R2 × R/2πZ

(cid:1)

g · (x, y) = (α, β, η) · (x, y) = (α + x cos η − y sin η, β + x sin η + y cos η).

The law in the group (D, ◦) is then

(α(cid:18), β (cid:18), η(cid:18)) ◦ (α(cid:18)(cid:18), β (cid:18)(cid:18), η(cid:18)(cid:18)) = (α(cid:18)(cid:18)(cid:18), β (cid:18)(cid:18)(cid:18), η(cid:18) + η(cid:18)(cid:18))

with

(α(cid:18)(cid:18)(cid:18), β (cid:18)(cid:18)(cid:18)) = (α(cid:18), β (cid:18), η(cid:18)) · (α(cid:18)(cid:18), β (cid:18)(cid:18)).

√

√

Given (a, b) ∈ R2 and θ ∈ [0, π/2], we use the notation qa,b,θ,c for the square
centered at (a, b) at angle θ, which has side c
2 and diagonal 2c. This square has the
four vertices (a, b)+c(cos θi , sin θi ), with θi = θ +i(π/2) for i from 1 to 4; its boundary
is denoted as usual by ∂(qa,b,θ,c). For any number c > 0, we denote by Qc the set of
2 in R2, with the topology induced by R2 × S1. The space Qc is locally
squares of side c
compact and simply connected and contractible.

The square q0,0,0,c is deﬁned by the inequality |x| + |y| ≤ c. We ﬁnd the inequality
of a square qa,b,θ,c ∈ Qc by determining gα,β,η ∈ D which maps the square qa,b,θ,c onto
q0,0,0,c. We get (α, β, η) = (−a cos θ − b sin θ, a sin θ − b cos θ, −θ). Then (x, y) ∈
qa,b,θ,c if and only if

|(x − a) cos θ + (y − b) sin θ| + |−(x − a) sin θ + (y − b) cos θ| ≤ c.

Improved Dense Packings of Congruent Squares in a Square

99

We deﬁne hk(qa,b,θ,c) = qa,b,θ,kc to be the homothetic of the square qa,b,θ,c with

respect to its center.

Given g ∈ D, the direct image set g(qa,b,θ,c) = qa(cid:18),b(cid:18),θ (cid:18),c is a square centered at g(a, b);
we use the notation g · q = g(q). We note that D acts simply and transitively on Qc
and Qc/D =
. The boundaries of the squares obtained by those operations are
related by ∂(g · qa,b,θ,c) = g(∂(qa,b,θ,c)) and we have ∂(hk(qa,b,θ,c)) = hk(∂(qa,b,θ,c)).
We deﬁne the manifold of ordered conﬁgurations of n non-overlapping squares of

(cid:1)
q0,0,0,c

(cid:2)

diagonal 2c contained in [−L , L]2 as the set

Qn,c = {C = (q1, . . . , qn) ∈ Qn
c

, qi ⊂ [−L , L]2 for all i and

int(qi ) ∩ int(qj ) = ∅ for i < j}.

When C ∈ Qn,c, we say that C is an admissible conﬁguration.
Finding the real number sn is equivalent to the maximization of c > 0 such that Qn,c

√

is not empty. For L = 1, we note that max{c: Qn,c (cid:22)= ∅} =

2/sn.

We deﬁne the homothetic of an admissible conﬁguration C = (q1, . . . , qn) by hk(C) =
(hk(q1), . . . , hk(qn)), and we note that it makes sense for 0 < k ≤ ω(C)/c where
ω(C)/c ≥ 1.

We deﬁne an embedding of Qn,c into ([−L , L]2 × (R/(π/2)R))n as follows: the
requirements int(qi ) ∩ int(qj ) = ∅ for i < j and qi ⊂ [−L , L]2 are equivalent to
inequalities for the 3n-tuple (ai , bi , θi )1≤i≤n of the shape fκ ((ai , bi , θi )1≤i≤n) ≤ 0 where
the functions fκ , with 1 ≤ κ ≤ 2n2 + 2n, which are easily written down, are continuous
but not C 1. Hence, the manifold Qn,c is compact.

3. Percussion and ψ(C)

We now deﬁne the maximum inﬂation of a conﬁguration of two squares (q (cid:18), q (cid:18)(cid:18)) ∈ Q2
c
with distinct centers: we look at the numbers k > 0 for which hk/c(q (cid:18))∩hk/c(q (cid:18)(cid:18)) is empty.
This deﬁnes an interval of R∗
+, the supremum of which will be denoted by ψ(q (cid:18), q (cid:18)(cid:18)).
This real number is independent of c and we can denote ψ(qa(cid:18),b(cid:18),θ (cid:18),c(cid:18) , qa(cid:18)(cid:18),b(cid:18)(cid:18),θ (cid:18)(cid:18),c(cid:18)(cid:18) ) by
ψ(a(cid:18), b(cid:18), θ (cid:18), a(cid:18)(cid:18), b(cid:18)(cid:18), θ (cid:18)(cid:18)). The following lemma gives the some properties of the func-
tion ψ:

Lemma 1. Given two squares q (cid:18), q (cid:18)(cid:18), with distinct centers, and diagonal 2c, we have
the following:

(a) ψ(q (cid:18), q (cid:18)(cid:18)) = ψ(q (cid:18)(cid:18), q (cid:18)).
(b) q (cid:18) ∩ q (cid:18)(cid:18) = ∅ is equivalent to ψ(q (cid:18), q (cid:18)(cid:18)) > c.
(c) For any g ∈ D, we have ψ(g · q (cid:18), g · q (cid:18)(cid:18)) = ψ(q (cid:18), q (cid:18)(cid:18)).
(d) For any k ∈ R, we have ψ(hk/c(q (cid:18)), hk/c(q (cid:18)(cid:18))) = ψ(q (cid:18), q (cid:18)(cid:18)).

Now, it is clear that hψ(q (cid:18),q (cid:18)(cid:18))/c(q (cid:18)) ∩ hψ(q (cid:18),q (cid:18)(cid:18))/c(q (cid:18)(cid:18)) contains at least one vertex of the
two squares hψ(q (cid:18),q (cid:18)(cid:18))/c(q (cid:18)) and hψ(q (cid:18),q (cid:18)(cid:18))/c(q (cid:18)(cid:18)); if, say, this intersection contains a vertex
of q (cid:18), we say that the square q (cid:18) strikes the square q (cid:18)(cid:18) by inﬂation at k = ψ(q (cid:18), q (cid:18)(cid:18)). We
state for further reference the basic properties of this process:

100

Lemma 2.

Th. Gensane and Ph. Ryckelynck

(a) Given two congruent squares with distinct centers, one of them strikes the other.
(b) The relation “q (cid:18) strikes the square q (cid:18)(cid:18) by inﬂation at k” is not symmetric in q (cid:18)

and q (cid:18)(cid:18).

(c) If q (cid:18) strikes q (cid:18)(cid:18) and q (cid:18)(cid:18) strikes q (cid:18), then hψ(q (cid:18),q (cid:18)(cid:18))/c(q (cid:18)) ∩ hψ(q (cid:18),q (cid:18)(cid:18))/c(q (cid:18)(cid:18)) contains a
common isolated vertex or the seqment joining a vertex of q (cid:18) to a vertex of q (cid:18)(cid:18).

(d) If q (cid:18) strikes q (cid:18)(cid:18) at k and if g ∈ D, then g · q (cid:18) strikes g · q (cid:18)(cid:18) at k.
(e) If q (cid:18) strikes q (cid:18)(cid:18) at k and if λ ∈ R, then hλ · q (cid:18) strikes hλ · q (cid:18)(cid:18) at k.

Lemma 3. Let c, s be two numbers such that c2 + s2 = 1 and cs (cid:22)= 0. Among the four
numbers 1 − c − s, 1 − c + s, 1 + c + s, 1 + c − s, two are greater than one, three are
positive and one is negative, the absolute value of the negative number is less than the
biggest positive number among the three.

Proof. Two of the four numbers 1 − (c + s), 1 + (c + s), 1 − (c − s), 1 + (c − s) are
greater than one. If the two others are negative we would have to say 1 < ε(cid:18)(c + s) and
1 < ε(cid:18)(cid:18)(c − s) with ε(cid:18)2 = ε(cid:18)(cid:18)2 = 1. Let us set c = cos x, s = sin x; the product gives
1 < ε(cid:18)ε(cid:18)(cid:18)(c + s)(c − s) = ε(cid:18)ε(cid:18)(cid:18) cos 2x which is impossible. The remainder of the proof
is straightforward.

Proposition 1. The function ψ(a(cid:18), b(cid:18), θ (cid:18), a(cid:18)(cid:18), b(cid:18)(cid:18), θ (cid:18)(cid:18)) is the maximum of {ψ1, ψ2} where









ψ1 = ψ0

ψ2 = ψ0

(a(cid:18)(cid:18) − a(cid:18)) cos θ (cid:18) + (b(cid:18)(cid:18) − b(cid:18)) sin θ (cid:18)
−(a(cid:18)(cid:18) − a(cid:18)) sin θ (cid:18) + (b(cid:18)(cid:18) − b(cid:18)) cos θ (cid:18)
θ (cid:18)(cid:18) − θ (cid:18)



 ,

(a(cid:18) − a(cid:18)(cid:18)) cos θ (cid:18)(cid:18) + (b(cid:18) − b(cid:18)(cid:18)) sin θ (cid:18)(cid:18)
−(a(cid:18) − a(cid:18)(cid:18)) sin θ (cid:18)(cid:18) + (b(cid:18) − b(cid:18)(cid:18)) cos θ (cid:18)(cid:18)
θ (cid:18) − θ (cid:18)(cid:18)



 ,

and where the function ψ0 is deﬁned by

ψ0(a, b, θ) = min
i=1,...,4

|a| + |b|
|1 − (sgn(a) cos θi + sgn(b) sin θi )|

(cid:8)

= min
i=1,...,4



√

(cid:12)
(cid:12)
(cid:12)1 −

|a| + |b|

2 sgn(ab) sin(θ + π/4 + i(π/2))






.

(cid:12)
(cid:12)
(cid:12)

(cid:7)




Proof.

(i) Let q (cid:18), q (cid:18)(cid:18) be two squares with distinct centers.

If q (cid:18) strikes by inﬂation q (cid:18)(cid:18), then g1 = (−a(cid:18) cos θ (cid:18) − b(cid:18) sin θ (cid:18), a(cid:18) sin θ (cid:18) −b(cid:18) cos θ (cid:18), −θ (cid:18))

is such that g1 · q (cid:18) = q0,0,0,c and g1 · q (cid:18)(cid:18) = qa,b,θ (say) strikes by inﬂation q0,0,0,c.

Else if q (cid:18)(cid:18) strikes by inﬂation q (cid:18), then g2 = (−a(cid:18)(cid:18) cos θ (cid:18)(cid:18)−b(cid:18)(cid:18) sin θ (cid:18)(cid:18), a(cid:18)(cid:18) sin θ (cid:18)(cid:18) −b(cid:18)(cid:18) cos θ (cid:18)(cid:18),
−θ (cid:18)(cid:18)) is such that g2 · q (cid:18)(cid:18) = q0,0,0,c and g2 · q (cid:18) = qa,b,θ (say) strikes by inﬂation q0,0,0,c.
(ii) We begin with the case θ =0, that is θ (cid:18) =θ (cid:18)(cid:18), or q (cid:18), q (cid:18)(cid:18) parallel. Here direct inspection
(|a| + |b|).

of the percussion process shows that it occurs at ψ(0, 0, 0, a, b, 0) = 1
2

Improved Dense Packings of Congruent Squares in a Square

101

However, the numbers given in our statement are equal to ψ1 = ψ0(a, b, 0) and ψ2 =
= (|a| + |b|)/2.
ψ0(−a, −b, 0) and, in turn, they are equal to (|a| + |b|) min
This shows that the formula ψ = max(ψ1, ψ2) holds in this particular case.

, ∞

1
2

(cid:1)

(cid:2)

(iii) We suppose now that qa,b,θ,c strikes q0,0,0,c by inﬂation at k. Then at least one
vertex of the square hk/c(qa,b,θ,c) belongs to the segment [(sgn(a)k, 0), (0, sgn(b)k)] of
the boundary of hk/c(q0,0,0,c). Let this vertex be (a + k cos θi , b + k sin θi ), where θi is
one of the four angles θ + i(π/2). There exists some real number λ ∈ [0, 1] such that

(a + k cos θi , b + k sin θi ) = (sgn(a)(1 − λ)k, sgn(b)λk).

(S)

This system has the solution

k = (|a| + |b|)

1
1 − (sgn(a) cos(θi ) + sgn(b) sin(θi ))

and

λ =

|b| + sgn(b)|a| sin θi − sgn(a)|b| cos θi
|a| + |b|
Now we observe that the least positive value of k among the four preceding values
obtained for i ∈ {1, . . . , 4}, say i = i0, gives rise truly to a percussion, namely member-
ship of the i0th vertex of hk/c(qa,b,θ,c) to hk/c(q0,0,0,c). Indeed, the other positive values
of k corresponding to i1 (cid:22)= i0 give hk/c(qa,b,θ,c) ∩ hk/c(q0,0,0,c) (cid:22)= ∅. See the left side of
Fig. 1. Hence, the value

.

ψ0(a, b, θ) = (|a| + |b|) min
i=1,...,4

(cid:7)

1
1 − (sgn(a) cos(θi ) + sgn(b) sin(θi ))

(cid:8)

is the least positive number such that hψ0(a,b,θ )/c(qa,b,θ,c) ∩ hψ0(a,b,θ )/c(q0,0,0,c) (cid:22)= ∅.
Hence, when qa,b,θ,c strikes q0,0,0,c by inﬂation at k, we have ψ0(a, b, θ) = ψ(a, b, θ, 0,
0, 0).

(iv) We note, from the previous step, that even when qa,b,θ,c does not strike q0,0,0,c by
inﬂation at ψ0(a, b, θ), the number ψ0(a, b, θ ) remains well deﬁned and is strictly less
than ψ(a, b, θ, 0, 0, 0). Indeed, the hypothesis is merely to be said as: the system (S) has
a solution, for which we get λ /∈ [0, 1]; hence the vertex of hk/c(qa,b,θ,c) that is described
above lies on the straight line joining two vertices of hk/c(q0,0,0,c). Thus, the homothetics
hk(qa,b,θ,c) and hk(q0,0,0,c) are disjoint, so that ψ0(a, b, θ) < ψ(a, b, θ, 0, 0, 0). In that

Fig. 1. The percussion process.

102

Th. Gensane and Ph. Ryckelynck

case the percussion occurs “later,” at

ψ1 = ψ0(−a cos θ − b sin θ, a sin θ − b cos θ, −θ) > ψ2 = ψ0(a, b, θ ),

see the right side of Fig. 1.

(v) We consider the displacement g1 and g2 already deﬁned in (i). We obtain the two
numbers ψ0(g1 · qa(cid:18)(cid:18),b(cid:18)(cid:18),θ (cid:18)(cid:18) ) and ψ0(g2 · qa(cid:18),b(cid:18),θ (cid:18) ). Since one of the two squares strikes the
other, and by Lemma 1(c), we have ψ(a(cid:18), b(cid:18), θ (cid:18), a(cid:18)(cid:18), b(cid:18)(cid:18), θ (cid:18)(cid:18)) = max{ψ1, ψ2}.

Remark 1. The function ψ0 can be extended by continuity on (0, 0) × [0, π/2] if we
set ψ0(0, 0, θ) = 0 and, correspondingly, the function ψ(a(cid:18), b(cid:18), θ (cid:18), a(cid:18)(cid:18), b(cid:18)(cid:18), θ (cid:18)(cid:18)) can be
extended to the case where (a(cid:18), b(cid:18)) = (a(cid:18)(cid:18), b(cid:18)(cid:18)) by setting ψ(a, b, θ (cid:18), a, b, θ (cid:18)(cid:18)) = 0.

Remark 2. From Lemma 3, it follows that the function ψ0(a, b, θ ) is well deﬁned
since the set in Proposition 1 contains three numbers, except when θ = 0 mod π in
which case this set is equal to { 1
, ∞}. Now the eight values which appear in the two
2
underlying sets in ψ1, ψ2 contain the value ∞ at most twice, six positive values, and
moreover can be all distinct.

Remark 3. We note an analogy between the formula of Proposition 1 and the deﬁnition
of the Hausdorff distance between compact sets A, B ⊂ Rd :

h(A, B) = max{g(A, B), g(B, A)}

where

g(A, B) = sup
a∈A

inf
b∈B

d(a, b).

The function ψ(q (cid:18), q (cid:18)(cid:18)), which is positive, symmetric and satisﬁes ψ(q, q) = 0, is not
however a semi-distance; the triangle inequality fails as shown in the following example.
If q1 = (0, 0, π/4), q2 = (1, 0, 0) and q3 = (10, 0, 0), then we ﬁnd

ψ(q1, q2) + ψ(q2, q3) < 5.08 < 5.85 < ψ(q1, q3).

Corollary. The function ψ: Q2
c
of which are the couples (q (cid:18), q (cid:18)(cid:18)) with q (cid:18) ∩ q (cid:18)(cid:18) = ∅, is open.

→ R+ is continuous, and the subset of Q2

c, the elements

We deﬁne the continuous function ψ: Qn,c → R+ by
ψ(C) = min

ψ(ai , bi , θi , aj , bj , θj ).

1≤i< j≤n

4. Conﬁnement and ϕ(C)

Given a square qa,b,θ,c ∈ Q1,c, we are looking for the biggest homothetic square qa,b,θ,k
contained in [−L , L]2. We might look at the numbers k > 0 for which hk/c(q) ⊂
[−L , L]2; this condition deﬁnes an interval of R∗
+, the supremum of which will be
(cid:2)
k, qa,b,θ,k ⊂ [−L , L]2
denoted by ϕ(a, b, θ) = sup

(cid:1)

.

Proposition 2. The function ϕ(a, b, θ) is continuous on Q1,c and deﬁned by
= L − max{|a| , |b|}
max{|cosθ| , |sin θ|}

ϕ(a, b, θ) = min{L − a, L − b, L + a, L + b}
max{|cos(θ)|, |cos(θ + π/2)|}

.

Improved Dense Packings of Congruent Squares in a Square

103

Proof. Let (a, b) ∈ [−L , L]2 and recall that θi = θ + i(π/2). The number ϕ(a, b, θ )
is well deﬁned and is the biggest value of k such that −L ≤ a + k cos(θi ) ≤ L and
−L ≤ b + k sin(θi ) ≤ L for all i; these inequalities show that ϕ(a, b, θ ) is equal to

(cid:7)

min

min
cos(θi )>0

L − a
cos(θi )

, min
sin(θi )>0

L − b
sin(θi )

, min
cos(θi )<0

L + a
− cos(θi )

, min
sin(θi )<0

L + b
− sin(θi )

(cid:8)

.

We observe that for any θ we have
1
cos(θi )

min
cos(θi )>0

= min

sin(θi )>0

1
sin(θi )
1
− sin(θi )

= min

cos(θi )<0

1
− cos(θi )
1
max{|cos(θ)|, |cos(θ + π/2)|}

.

=

= min

sin(θi )<0

This allows us to simplify the previous values of ϕ(a, b, θ) and to obtain
Proposition 2.

Note that ϕ(a, b, θ) is deﬁned on the boundary by ϕ(a, b, θ ) = 0 if a = ±L or

b = ±L. Finally, we deﬁne the continuous function ϕ: Qn,c → R+ by

ϕ(C) = min
1≤i≤n

ϕ(ai , bi , θi ) = min
1≤i≤n

min{L − ai , L − bi , L + ai , L + bi }
max{|cosθi |, |sinθi |}

.

5. Maximal Inﬂation ω(C) and the Graph of C

Now, we relate numbers sn with the preceding functions. Summed up, the previous results
show that:

Proposition 3. The function ω: Qn,c → R+ deﬁned by
ω(C) = min{ψ(C), ϕ(C)}
is well deﬁned and continuous. Moreover, for every C ∈ Qn,c, the homothetic hc(cid:18)/c(C),
where c(cid:18) = ω(C), is an admissible conﬁguration. If C ∈ Qn,c is a global maximizer for
ω, then we have ω(C) =

√

2L/sn.

Now, to any admissible conﬁguration C = (qi ) ∈ Qn,c of n congruent squares qi =
(ai , bi , θi ), we can associate a geometric graph (cid:21)(C) = (X, U ). Let C be a conﬁguration
of n squares qi centered at qi0 and with vertices qik = qi0 + c(cos θik, sin θik) with
θik = θi + k(π/2) for k = 1, . . . , 4. The graph (cid:21)(C) = (V, E) is non-oriented and
bipartite: the set V is the union of

(cid:16)

(cid:18)

Vc = {ql0}

and Vs = {qlm}m(cid:22)=0 ∩

∂[−L , L]2 ∪

(∂qi ∩ ∂qj )

.

(cid:17)

i< j

In other words, the vertices in Vc are the centers of the squares qi , those in Vs are the
points qik belonging either to ∂qi ∩ ∂qj for some j (cid:22)= i or to ∂[−L , L]2. Now, for any
indices i < j, if the set ∂qi ∩ ∂qj is not empty, then it contains one (or two) vertex v of
some square, we add v to Vs and add also two (or four) edges qi0v and vqj0 in E.

104

Th. Gensane and Ph. Ryckelynck

Fig. 2. Homotopic optimal packings of six squares and their graphs.

Remark 4. Whenever E (cid:22)= ∅, at least half of all the edges in E have length equal to
ω(C), while the remaining ones have length less than ω(C).

The following easy proposition links some of the previous deﬁnitions:

Proposition 4. Let C = (qi ) ∈ Qn,c and let i be a ﬁxed integer. We consider the
following three properties:

(i) There is no edge in the graph (cid:21)(C) which starts at qi0.
(ii) ψ(C) < inf1≤ j≤n, j(cid:22)=i {ψ(qi , qj )}.
(iii) There exists an homotopy Ht : [−L , L]2 → [−L , L]2 such that Ht (qj ) = qj for
all j (cid:22)= i and t ∈ [0, 1], and H1(qi ) (cid:22)= qi , and such that Ht (C) is admissible for
all t ∈ [0, 1].

We have (i) ⇔ (ii) and (ii) ⇒ (iii).

The implication (iii) ⇒ (ii) is false. For instance, for each square qi of the optimal
packing of six congruent squares displayed in Fig. 2, (ii) is false. However, (iii) is true
for the three upper squares.

When properties (i) and (ii) hold, we say that qi is isolated in C.
If the graph (cid:21)(C) is connected, then for all k, qk is not isolated. However, the converse
does not hold as is shown on the right of Fig. 2. We note ﬁnally that throughout an
homotopy of conﬁgurations, neither the number of vertices nor the number of edges of
the graph (cid:21)(C) remain constant.

If the graph does not encode homotopic information, it is however still well-suited to

visualize contacts between squares.

6. An Algorithm to Produce Dense Conﬁgurations

We denote by UK the uniform law of probability in the compact subset K of R2.

The code we have used to produce dense conﬁgurations has been implemented in
the language C and executed on a computer at CPU 800 MHz. It relies on four main
procedures that we now describe. The whole program is in fact a stochastic perturbed
walk through the manifolds Qn,c, with varying c.

Improved Dense Packings of Congruent Squares in a Square

105

Let C = (q1, . . . , qn) be a starting admissible conﬁguration of Qn,c—where c =
ω(C)—the ﬁrst procedure, RandomWalking, realizes some moves of randomly choosen
squares qi ; these moves are done whenever the displaced square qi does not strike the
other squares nor the boundary of [−1, 1]2. The procedure then returns a new admissible
conﬁguration C(cid:18) ∈ Qn,c(cid:18) with c(cid:18) ≥ c. The larger the number Na, the greater the chance
of separating the squares.

Procedure 1: RandomWalking(C, Na, ε, c)

For k from 1 to Na do:

Choose randomly (or sequentially) a square qi = qai ,bi ,θi ,c in C
Choose (a, b) following UB((ai ,bi )i ,ε)∩[−1,1]2 and θ following UB(θi ,ε)
Set z := qa,b,θ,c
If minj(cid:22)=i ψ(z, qj ) ≥ c and ϕ(z) ≥ c then qi := z

Next procedure BilliardOfSquares iterates the previous procedure; the amplitude ε
of the random moves is adapted through the run: at the beginning the squares are small
because one of them is close to the boundary or because two squares are close to each
other; then it is still possible that the squares realize big leaps. After a few steps of the
loop, procedure RandomWalking does not succeed in improving ω(C) and one needs
to decrease the amplitude ε in order to accelerate the calculations. Next, the value of ε
follows the success or failure of procedure RandomWalking. The real number ε2 is the
threshold of the procedure.

Procedure 2: BilliardOfSquares (C, ε1, ε2, Na)

ε = ε1
c = ω(C)
While ε > ε2 do:

RandomWalking(C, Na, ε, c)
If ω(C)> c then c := ω(C) and ε := 2 ∗ ε else ε := ε/2

(cid:20)

n

√

(cid:19)√

2/(

With procedure 2 we are now able to ﬁnd good squares packings by sampling a large
number of runs with different random starting conﬁgurations. Often, this billiard algo-
rithm gives jammed packings with ω(C) close to
+ 1) when the conﬁguration
obtained has just the angle θ = 0. When the optimal packing for a given n contains more
than two angles as in the case n = 17, the chance of ﬁnding a good approximation of
the conﬁguration by procedure BilliardOfSquares becomes weak. Nevertheless, when
procedure 2 gives a jammed packing topologically close to the optimal, it is possible
to approach it with the third and fourth procedures. The fourth procedure, WithPertur-
bation, attempts to ﬁnd a path toward a better conﬁguration and this has to be done by
slightly shaking the jammed conﬁgurations with procedure 3. As procedure 2, procedure
WithPerturbations regulates the amplitude ε of the moves which is also the amplitude
of the perturbations. During the same process, a conﬁguration C0 after being perturbed
is improved with procedure BilliardOfSquares which gives rise to a new conﬁguration
C. If ω(C) > ω(C0), we keep C by setting C0 = C. In the other case, we restore the old
conﬁguration C0.

106

Th. Gensane and Ph. Ryckelynck

Procedure 3: Perturbation(C, ε)

For i from 1 to n do:

Choose (a, b) following UB((ai ,bi )i ,ε)∩[−1,1]2 and θ following UB(θi ,ε)
Set (ai , bi ) = (a, b) and θi = θ

Let c = ω(C)
For i from 1 to n do: qi = qai ,bi ,θi ,c

Procedure 4: WithPerturbations(C, ε1, ε2, factor, Na)

ε := ε1
C0 := C
c0 := ω(C)
While ε > ε2 do

Perturbation(C, ε)
BilliardOfSquares(C, ε, ε/factor, Na)
If ω(C) > c0 then c0 := ω(C), C0 := C and ε := 2 ∗ ε
else C := C0 and ε := ε/2

It is quite surprising that the program behaves like its disk packing version [4]. Of
course, the procedures seems to be “attracted” by conﬁgurations with angle θ = 0 which
are rarely good. Nevertheless, after running procedure BilliardOfSquares(C, 0.1, 10−8, 1000)
some thousand times on random conﬁgurations, we have obtained some good starting
conﬁgurations C∗ for procedure WithPerturbations. The new results that we list have
been obtained with the call of WithPerturbations(C∗, 0.1, 10−12, 1.5, 1000).

7. Some New Results

Case n = 5 and n = 10. Our experiments conﬁrm easily the optimal packing of ﬁve
squares and the best known packing of ten squares, see [3] and [10] for these cases.
Case n = 11. The best known packing is due to Trump and apparently to many other
people. In [3] we ﬁnd that s11 ≤ 3.8772 for a packing given in Fig. 3. We have obtained
this packing several times with s11 = 3.87708359 . . ., a result which is slightly better.
We have also calculated that the cosine of the angle θ of the ﬁve central squares is a real
root z0 of the irreducible polynomial over Q(

2):

√

√

80z8 − 128

2z7 − 32z6 + 144

√

2z5 + 72z4 − 112

√

2z3 + 40z2 − 12

√

2z − 7.

√

We have found it by eliminating with Maple a system of 14 polynomial equations, the
2 is the side of the squares, z = cos(θ), z(cid:18) = sin(θ),
unknowns of which are: s = c
(ai , bi ) are the coordinates of the ﬁve tilted squares and α > 0 is the distance between
the two upper detached squares. The distance between the two dashed sides in Fig. 3
gives the crucial relation

s =

√

2

4z

2 + 5z − z(cid:18)

.

Improved Dense Packings of Congruent Squares in a Square

107

Fig. 3.

s11 < 3.877084.

The other equations are obtained by the requirement that some vertices qik belong to
sides of other squares or to the boundary of [−L , L]2. An approximation of the root z0
conﬁrms the values given by our algorithm.
Case n = 17. Friedman [3] reports on Bidwell’s discovery of the packing displayed
in Fig. 4 with s17 < 4.6755. However, this rounded value seems to be false, since two
distinct investigations of this packing lead us to the value

s17 = 4.6755300960455.

On one hand, the program described in Section 6 leads to Fig. 4 with the previous value
of s17. On the other hand, a model similar to that given in the case n = 11 yields
a polynomial system of four equations of degree 7 in c1 = cos(θ1), c2 = cos(θ2),
s1 = sin(θ1), s2 = sin(θ2), where θ1, θ2 are the distinct tilted angles; solving it with 20
digits of accuracy has given the same value for s17.
Case n = 18. H¨am¨al¨ainen and Gustafson quoted in [3] have found two different packings
7)/2. We conﬁrm this value with an alternative packing, displayed in
with s18 ≤ (7 +

√

Fig. 4.

s17 < 4.675531.

108

Th. Gensane and Ph. Ryckelynck

Fig. 5.

s18 ≤ 4.822876.

Fig. 6.

s29 ≤ 5.934342.

Fig. 5. It is of interest to note that six squares are isolated and six can be displaced by
small translations.
Case n = 29. We have found two packings better than Bidwell’s best known pack-
ing. They realize s29 < 5.9648, see Figs. 6 and 7. The upper bound becomes s29 ≤
5.934342. Figure 6 displays a packings with squares at six different angles: 19.01◦
(one square), 23.37◦ (one square), 24.67◦ (three squares), 24.74◦ (three squares), 26.82◦
(seven squares) and 45◦ (fourteen remaining). It appears to us impossible to ﬁnd such a
packing without a computer-aided method!
Case n = 37. Friedman [3] has found a nice packing with just one tilted angle and
s37 < 6.6213. Our best packing improves this bound and we ﬁnd s37 ≤ 6.603236. This
packing contains squares at ﬁve different angles and also six isolated squares.

Contrarily to the cases n = 11, 17 and 18, the algebraic models for the dense packings
of 29 and 37 squares displayed in Figs. 6–8 are too complex to be numerically solved.
However, we have veriﬁed with a sufﬁcient accuracy that the upper bounds for s29 and
s37 are effective. An interesting discussion of “the existence problem” for disk packings
is given in [1].

Fig. 7.

n = 29, ω(C) ≤ 5.958702.

Fig. 8.

s37 ≤ 6.603236.

Improved Dense Packings of Congruent Squares in a Square

109

References

1. D. Boll, J. Donovan, R. L. Graham, and B. D. Lubachevsky, Improving dense packings of equal disks in

a square, Electron. J. Combin. 7 (2000), #R46.

2. P. Erd˝os and R. L. Graham, On packing squares with equal squares, J. Combin. Theory Ser. A 19 (1975),

119–123.

3. E. Friedman, Packing unit squares in squares: a survey and new results, Electron. J. Combin. 7 (2000),

#DS7.

4. Th. Gensane, Dense packings of equal spheres in a cube, Report No. 188, Cahiers du L.M.P.A, June 2003.
5. R. L. Graham and B. D. Lubachevsky, Dense packings of equal disks in an equilateral triangle: from 22

to 34 and beyond, Electron. J. Combin. 2 (1995), #A1.

6. R. L. Graham, B. D. Lubachevsky, K. J. Nurmela, and P. R. J. ¨Osterg˚ard, Dense packings of congruent

circles in a circle, Discrete Math. 181 (1998), 139–154.

7. M. Kearney and P. Shiu, Efﬁcient packing of unit squares in a square, Electron. J. Combin. 9 (2002), #R14.
8. B. D. Lubachevsky, How to simulate billiards and similar systems, J. Comput. Phys. 94 (1991), 255–283.
9. H. Melissen, Packing and covering with circles, Ph.D. thesis, Utrecht University, 1997.
10. W. Stromquist, Packing 10 or 11 unit squares, Electron. J. Combin. 10 (2003), #R8.

Received April 8, 2004, and in revised form May 19, 2004. Online publication October 20, 2004.

