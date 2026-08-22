0
0
0
2

y
a
M
5

]

G
M
.
h
t
a
m

[

1
v
4
5
0
5
0
0
0
/
h
t
a
m
:
v
i
X
r
a

COMPACTNESS THEOREMS FOR GEOMETRIC PACKINGS

GREG MARTIN

Abstract. Moser asked whether the collection of rectangles of dimensions 1 × 1
2 × 1
3 ,
1
3 × 1
4 , . . . , whose total area equals 1, can be packed into the unit square without overlap,
and whether the collection of squares of side lengths 1
4 , . . . can be packed without
overlap into a rectangle of area π2
6 − 1. Computational investigations have been made into
packing these collections into squares of side length 1 + ε and rectangles of area π2
6 − 1 + ε,
respectively, and one can consider the apparently weaker question of whether such packings
are possible for every positive number ε. In this paper we establish a general theorem on
sequences of geometrical packings that implies, in particular, that the “for every ε” versions
of these two problems are actually equivalent to the original tiling problems.

3 , 1

2 , 1

2 , 1

1. Introduction
Given a collection A = {A1, A2, . . . } of subsets of Rn, a packing of A into another set C ⊂ Rn
is a way of ﬁtting each of the sets Ai inside C without overlap. By a positioning of a set Ai
we mean the image of Ai under a rigid motion of Rn, i.e., some combination of translations,
rotations, and reﬂections. To avoid ambiguity about points on the boundaries of the Ai, we
say more precisely that these positionings of the Ai must be contained inside C and that their
interiors must be pairwise disjoint. One can also speak of oriented packings, where the sets
Ai may be translated and rotated but not reﬂected, and also translated packings, where the
Ai may be translated but neither rotated nor reﬂected. We also refer to a translated packing
as a parallel packing, particularly when each set Ai is a brick (a product [x1, y1]×· · ·×[xn, yn]
of closed intervals). If the union of the repositioned sets Ai is all of C, we call the packing
a tiling of C.

i × 1

It is often diﬃcult to determine whether a particular collection A can be packed into some
target set C. One representative example is the collection A = {A1, A2, . . . } where each
Ai is a rectangle of dimensions 1
i+1 . Since the total area of these rectangles is 1, it is
conceivable that A can tile a unit square (generally or even with a parallel tiling); but this
problem, ﬁrst posed by Moser (see [3] and [2, Section D5]), is unsolved. One can instead ask
the apparently weaker question of whether for every positive number ε, the collection A can
be packed inside a square of side length 1 + ε (see for example [1]). A similar situation holds
with the collection A = {S2, S3, . . . } where each Si is a square of side length 1
i . Conceivably
this collection will tile a rectangle of area π2
6 − 1 (and perhaps even one with dimensions
( π2
6 − 1) × 1), but it is even unknown whether for every positive number ε the collection
A can be packed into rectangles with area π2
6 − 1 + ε. For both these problems, results of
Paulhus [5] shows that ε can at least be taken smaller than 10−9.

The purpose of this paper is to show that the weaker “for every ε” versions of these two
packing problems are actually equivalent to the stronger tiling versions. Our methods apply

1991 Mathematics Subject Classiﬁcation. 52C17 (52C15, 54H99).

1

 
 
 
 
 
 
2

GREG MARTIN

in a somewhat more general setting, and we state the following two theorems as representative
of what can be deduced. For the ﬁrst theorem, we use the notation λC = {λy : y ∈ C} for
the homothetic expansion/dilation (or simply homothet) of C by the constant factor λ > 0.
Theorem 1. Let A be a collection of subsets of Rn, and let C be a compact subset of Rn.
If for every ε > 0 there exists a packing of A into the homothet (1 + ε)C, then there exists
a packing of A into C itself. In particular, if there exist packings of A into closed balls of
radius R + ε for every ε > 0, then there exists a packing of A into a closed ball of radius R.
These statements remain true if “packing” is replaced by “oriented packing” or “translated
packing”.

We remark that the collection A may have any cardinality. Of course, the hypothesis that
the target set C be compact is equivalent to C being both closed and bounded; both of
these conditions on C are necessary. There are obvious counterexamples if C is not required
to be closed—for example, we can take C to be the open unit disk in R2 and A to be the
collection consisting solely of ¯C, the closure of C. The theorem also fails if C is closed but
not bounded: for example, we can again take A to consist solely of the closed unit disk in
R2, and C to be the the closed region {(x, y) : 1 ≤ x, |y| ≤ 1 − 1/x}.
Theorem 2. Let A be a collection of subsets of Rn. If there exist packings of A into bricks
of volume V + ε for every ε > 0, then there exists a packing of A into a brick of volume V .
let {B1, B2, . . . } be a sequence of bricks in Rn, with
In fact a stronger statement is true:
the dimensions of the jth brick Bj being bj1 × · · · × bjn. Set V = inf j{vol Bj}, and assume
that vol Bj > V for every j. Suppose that there exists a packing of A into each brick Bj.
Then there exists a packing of A into some brick B with dimensions b1 × · · · × bn, satisfying
vol B = V and bm ≤ lim supj{bjm} for each 1 ≤ m ≤ n. These statements remain true if
“packing” is replaced by “oriented packing” or “translated packing”.

The equivalence of the weak and strong versions of the two packing problems mentioned

in the introductory remarks follow as immediate corollaries of Theorem 2:
Corollary 1. Let A be the collection of rectangles of dimensions 1 × 1
4 × 1
2, 1
5,
. . . . Suppose that for every ε > 0, the collection A can be packed into a square of area
1 + ε. Then A tiles a square of area 1. If the given packings are parallel packings, then A
parallel-tiles a square of area 1.

3 × 1

2 × 1

4, 1

3, 1

Corollary 2. Let A be the collection of squares of side lengths 1
for every ε > 0, the collection A can be packed into a rectangle of area π2
tiles a rectangle of area π2
tiles a rectangle of dimensions 1 × ( π2
packings, then A parallel-tiles the resulting rectangle of area π2

4 , . . . . Suppose that
6 − 1 + ε. Then A
6 − 1. If the given packings are into rectangles of height 1, then A
6 − 1). In either case, if the given packings are parallel
6 − 1.

2, 1

3, 1

The aforementioned work of Paulhus [5] makes a convincing argument that the “for ev-
ery ε” versions of these two packing questions have aﬃrmative answers (since obstacles to
ﬁnding rectangle tilings generally arise from the largest rectangles). In light of Corollaries 1
and 2, it therefore seems likely that tilings (indeed, parallel tilings) do exist in both cases.

As can be inferred from the title of this paper, the methods used to establish Theorems 1
and 2 are topological in nature. The intuitive idea is to convert a sequence of packings of the
collection A in the hypothesized sets into a “limiting packing” of A into the desired target

COMPACTNESS THEOREMS FOR GEOMETRIC PACKINGS

3

set. To this end, we will show how the set of packings of A can be naturally regarded as a
topological space, and then use a compactness argument to show the existence of a “limiting
packing” of some sort; it then remains to show that this packing is a valid packing into the
type of set required by Theorem 1 or 2.

In Section 2 we set the notation to be used throughout this paper and exhibit simple prop-
erties of the deﬁned objects that follow easily from elementary point-set topology. Section 3
contains the proofs of Theorems 1 and 2, modulo an important proposition whose proof will
be deferred until Section 4 in order to clarify the issues involved in the proofs of the theorems
themselves. In Section 5 we remark on some modiﬁed versions of Theorems 1 and 2 that
can be proved using these methods, without going into the details of the proofs.

2. Notation and Basic Topological Facts
The methods that we use are valid for collections A of subsets of Rn of any cardinality, but
for the sake of notational simplicity we work under the assumption that our collection A =
{A1, A2, . . . } is countably inﬁnite. In addition, we argue throughout with the understanding
that we are allowing translations, rotations, and reﬂections and thus permitting the most
general kinds of packings; at the beginning of Section 5 we will explain how our arguments
extend to the more restrictive classes of oriented packings and parallel packings.

For any subset C of Rn, we denote by P(A, C) the set (possibly empty a priori ) of all
packings of A into C. We mention at the outset that translated copies of the target space
C are equivalent to each other for the purposes of deciding whether there exists a packing
of A into C—indeed, there is a natural bijection between the set of packings of A into C
and the set of packings of A into some translated copy of C. Similarly, we may modify the
collection A by replacing each set Ai by any translated copy of Ai, and still retain in essence
the same set P(A, C). For instance, it will often be convenient for us to assume that each
set Ai contains the origin in Rn. We also note that if C is a subset of D then certainly
P(A, C) ⊂ P(A, D).

Let O(n) denote the n-dimensional orthogonal group, i.e., the set of all n × n matrices θ
with real entries such that θ−1 = θT . Every rigid motion of Rn can be identiﬁed with an
element of the product space O(n) × Rn as follows: if σ = (θ, ξ) is an element of O(n) × Rn,
then σ acts on a point x of Rn by the rule σ(x) = ξ + θx. (Throughout this paper we will
maintain the notational conventions that elements of O(n) × Rn will be denoted by σ or τ ,
and that θ and ξ will denote the O(n)- and Rn-components, respectively, when it is necessary
to refer to these components separately.) Certainly these rigid motions σ act on subsets A
of Rn as well, and we will write σ(A) = {ξ + θx : x ∈ A} for the image. Any positioning of
the set A in Rn, using translations, rotations, and/or reﬂections, can be realized as σ(A) for
some element σ of O(n) × Rn.

Deﬁne the topological space M(Rn) to be the product space (O(n) × Rn)∞, and for any
subset D of Rn deﬁne the subspace M(D) = (O(n)×D)∞ of M(Rn). Since every positioning
of a set A in Rn corresponds uniquely to an element σ of O(n) × Rn, the space M(Rn)
parametrizes all possible positionings of the collection A in Rn, and certain positionings
among these will correspond to packings of A into a target set C. More precisely, if Int A
denotes the interior of A, we can write

P(A, C) =

S = {σi} ∈ M(Rn) : ∀i, σi(Ai) ⊂ C;
(cid:8)

∀i 6= j, Int(σi(Ai)) ∩ Int(σj(Aj)) = ∅

(1)

.
(cid:9)

4

GREG MARTIN

(In general we will let S and T denote elements of M(Rn) or of its subsets.) As a result,
the set P(A, C) can be given the subspace topology induced by the product topology on
M(Rn). The key to the proof of Theorem 1 is to exploit this topological structure on
M(Rn) to show that P(A, C) is a nonempty subspace under the stated hypotheses, and
the proof of Theorem 2 proceeds similarly after a suitable brick B is chosen as the ultimate
target set.

We now exhibit several facts, which follow from the deﬁnitions of the above notation
together with elementary point-set topology, that will be useful to us later. As a ﬁnal piece
of notation, let

∆r(x) = {y ∈ Rn : |y − x| < r}

represent the open ball in Rn of radius r and center x.
Fact 1. For any element σ of O(n) × Rn, any point x of Rn, and any positive number r, we
have σ(∆r(x)) = ∆r(σ(x)).
This follows directly from the fact that the elements σ of O(n) × Rn correspond to rigid
motions (isometries) of Rn, i.e., |σ(y) − σ(x)| = |y − x| for any points x, y ∈ Rn.
Fact 2. Each element σ of O(n) × Rn is a homeomorphism of Rn onto itself; in particular,
σ−1 is well-deﬁned.

Certainly σ, being an isometry, is continuous. Moreover, it is easy to see that if σ = (θ, ξ),
then τ = (θ−1, −θ−1ξ) is an element of O(n) × Rn which inverts the action of σ on Rn.
Therefore σ is continuously invertible as well, hence a homeomorphism.
Fact 3. For any element σ of O(n) × Rn and any subset A of Rn, we have σ(Int(A)) =
Int(σ(A)).
This is an immediate consequence of the fact that σ is a homeomorphism of Rn.
Fact 4. Let D be a subset of Rn, and let {xn} be a sequence of points of Rn, all but ﬁnitely
many of which belong to D. If {xn} converges to some point x, then x ∈ ¯D.

Fact 5. Every closed subset of a compact space is itself compact.

Fact 6. In a compact topological space, every sequence has a convergent subsequence.

These three statements are simple consequences of elementary point-set topology; see for
instance Munkres [4], Sections 2.10, 3.5, and 3.7, respectively.
Fact 7. If C is a compact subset of Rn, then the space M(C) is also compact.

The orthogonal group O(n) is compact (it is clearly bounded, since each column is a unit
vector in Rn and hence each entry is at most 1 in absolute value; and it is closed since it is
the preimage of the identity matrix under the continuous map θ 7→ θT θ). Since M(C) =
(O(n) × C)∞, Fact 7 therefore follows from Tychonov’s theorem that arbitrary products of
compact spaces are compact (see [4, Section 5.1]). The compactness of these spaces M(C)
is crucial to our proofs of Theorems 1 and 2.
Fact 8. If A = {A1, A2, . . . } is a collection of subsets of Rn, each containing the origin,
then P(A, C) is a subset of M(C).

COMPACTNESS THEOREMS FOR GEOMETRIC PACKINGS

5

We can justify this fact as follows: if 0 ∈ A and σ = (θ, ξ), then ξ = ξ + θ(0) ∈ σ(A). Thus
if σ(A) ⊂ C, we must have ξ ∈ C. Fact 8 then follows from the deﬁnition (1) of P(A, C) by
applying this reasoning to each image σi(Ai).
Fact 9. If A = {A1, A2, . . . } and C = {C1, C2, . . . } are collections of subsets of Rn, then
P(A,

∞
k=1 P(A, Ck).

∞
k=1 Ck) =

T

T

This follows immediately from unfolding the deﬁnitions of P(A,
using equation (1). In words, Fact 9 states that any packing of A into the set
simultaneously a packing of A into each set Ck.

T

T

∞
k=1 Ck) and

∞
k=1 P(A, Ck)
∞
k=1 Ck is

T

3. Proofs of Theorems 1 and 2

In this section we state the following crucial proposition from which we deduce Theorems 1
and 2:
Proposition 1. Let C be a closed subset of Rn, and let A be any collection of subsets of
Rn. Then the space P(A, C) is a closed subset of M(Rn).

The proof of Proposition 1, while not tricky, is somewhat long-winded, and therefore we defer
it to the next section. Assuming the validity of Proposition 1, we can establish Theorems 1
and 2 by means of the following lemma:
Lemma 2. Let A = {A1, A2, . . . } and C = {C1, C2, . . . } be collections of subsets of Rn. For
∞
j=k Cj, and suppose that D1 is bounded. If there exist packings of
each k ≥ 1 deﬁne Dk =
A into Cj for each j ≥ 1, then there exists a packing of A into the set

∞
k=1
∞
k=1 Dk, which is simply the lim sup
The set
of the sets Cj (the set of all points that are contained in inﬁnitely many of the Cj). In fact,
¯Dk is precisely the set of all points x ∈ Rn such that every neighborhood of x intersects

¯Dk can be compared to the related set

¯Dk.

∞
k=1

S

T

T

T

∞
k=1

inﬁnitely many of the Cj.
T

Proof: By translating the sets Ai if necessary, we may assume that each Ai contains the
origin. By hypothesis, there exists a packing of A into each Cj, so we may choose

Tj ∈ P(A, Cj) ⊂ P(A, ¯Dj) ⊂ P(A, ¯D1)
for each j ≥ 1. The set ¯D1 is closed and bounded, hence compact, and so by Fact 7 the
space M( ¯D1) is also compact. Since the sets Ai all contain the origin, the space P(A, ¯D1) is
contained in M( ¯D1) by Fact 8; we know by Proposition 1 that P(A, ¯D1) is a closed set, and
so it is itself compact by Fact 5. Therefore by Fact 6, the sequence {Tj} of points in P(A, ¯D1)
has a convergent subsequence. By replacing the sequence {Tj} by this subsequence, we may
assume that the Tj converge to some element T ∈ P(A, ¯D1).

It remains to show that this element T in fact represents a packing of A into

¯Dk.
For each k ≥ 1, the sequence Tj is contained (except for at most the ﬁrst k − 1 terms) in
P(A, ¯Dk). Since this set is closed by Proposition 1, we see by Fact 4 that the limit T is itself
an element of P(A, ¯Dk). Because this is true for all k ≥ 1, Fact 9 implies

∞
k=1

T

T ∈

∞

\k=1

P(A, ¯Dk) = P

A,

(cid:18)

∞

\k=1

¯Dk(cid:19)
,

which establishes the lemma.

6

GREG MARTIN

Proof of Theorem 1: Since C is compact, it is contained in some ball of radius R centered
at the origin, and therefore each set (1 + 1
j )C is contained in the ball of radius 2R around the
origin. Therefore under the hypothesis that there exist packings of A into each set (1 + 1
j )C,
¯Dk,
we may apply Lemma 2 to conclude that there exists a packing of A into the set
where we have put

∞
k=1

T

Dk =

∞

[j=k

(1 + 1

j )C.

(2)

All that remains to establish the theorem is to show that
words, we need to show that for every x /∈ C, there exists some k ≥ 1 such that x /∈ ¯Dk.

¯Dk is contained in C; in other

∞
k=1

T

If x /∈ C then, since C is compact (hence closed), there exists a positive number ε such

that ∆ε(x) ∩ C = ∅. We claim that

for every j > 2|x|ε−1, ∆ε/2(x) ∩ (1 + 1

j )C = ∅.

(3)

To see this, suppose that there did exist a point y in ∆ε/2(x) ∩ (1 + 1
if we set z = (1 + 1
On the other hand, since y ∈ ∆ε/2(x),

j )C,
j )−1y then z ∈ C, and by our choice of ε we therefore have |x − z| ≥ ε.

j )C. Since y ∈ (1 + 1

|x − z| ≤ |x − y| + |y − z| <

ε
2

+ |y − (1 + 1

j )−1y| =

ε
2

+

|y|
j + 1

.

The fact that y ∈ ∆ε/2(x) forces |y| < |x| + ε/2, and so

|x − z| <

ε
2

+

|x| + ε/2
j + 1

<

ε
2

+

|x| + ε/2
2|x|/ε + 1

= ε

by our choice of j. This contradiction establishes equation (3).

If we set k = ⌊2|x|ε−1⌋ + 1, we see from equation (3) and the deﬁnition (2) of Dk that

∆ε/2(x) ∩ Dk = ∅, which implies that x /∈ ¯Dk as desired. This establishes the theorem.

Proof of Theorem 2: First we make some reductions in the problem. By translating each
set Ai if necessary we may assume that each Ai contains the origin. Similarly, by translating
each brick Bj if necessary, we may assume that each Bj is contained in the positive orthant
of Rn and has one vertex at the origin, that is, Bj = [0, bj1] × · · · × [0, bjn]. Next, by passing
to a suitable subsequence of the Bj, we may also assume that vol Bj decreases monotonically
to V . At this point we make the assumption that the dimensions bjm of the bricks Bj are
bounded uniformly in j and m; at the end of the proof we will show why this assumption
is legitimate. By passing once again to a suitable subsequence of the Bj, we may therefore
assume that for each 1 ≤ m ≤ n the sequence {bjm} converges to some number bm, say.

Since the bjm are uniformly bounded, the sets Bj are all contained in a single bounded
region of Rn, and thus we may apply Lemma 2 to conclude that there exists a packing of
∞
the set A into
j=k Bj. The theorem will therefore be
¯Dk is contained in the brick
established if we can demonstrate that the intersection
B = [0, b1] × · · · × [0, bn]. For any natural numbers k and m with 1 ≤ m ≤ n, deﬁne
dkm = supj≥k{bjm}. Then for j ≥ k it is clear that Bj is contained in the closed set

¯Dk, where we have put Dk =

∞
k=1

∞
k=1

T

T

S

COMPACTNESS THEOREMS FOR GEOMETRIC PACKINGS

7

[0, dk1] × · · · × [0, dkn], and so ¯Dk is contained in the same closed set. Consequently,

∞

∞

¯Dk ⊂

[0, dk1] × · · · × [0, dkn]

\k=1

(cid:1)

=

\k=1 (cid:0)
0, inf k{dk1}
(cid:2)
0, lim supj{bj1}
(cid:2)

0, inf k{dkn}
(cid:2)
× · · · ×
=
= [0, b1] × · · · × [0, bn] = B.

× · · · ×

(cid:3)

(cid:2)

(cid:3)

(cid:3)
0, lim supj{bjn}

(cid:3)

This establishes the theorem, modulo the assumption that the bjm are uniformly bounded.
This assumption does not hold for a general collection of bricks of bounded volume, as the
simple example [0, n] × [0, 1/n] in R2 demonstrates. However, in the most natural case—
where at least one of the sets Ai has nonempty interior—we will be able to deduce from the
existence of a packing of A into each brick Bj that the bjm are uniformly bounded. In the
contrary (less interesting) case, it will also be possible to reduce to the situation where the
bjm are uniformly bounded by a somewhat diﬀerent method.
Case 1. At least one of the sets Ai has nonempty interior.

Choose an integer k such that the set Ak has nonempty interior, and then choose
η > 0 such that Ak contains some open ball of radius η. Since there exists a packing of
A into each brick Bj, we see in particular that each Bj contains some open ball of radius
η. Certainly then the dimensions bj1, . . . , bjn of each brick Bj must satisfy bjm ≥ η for
each 1 ≤ m ≤ n, and so for each j ≥ 1 and 1 ≤ m ≤ n,

0 < bjm =

vol Bj
bj1 . . . bj,m−1bj,m+1 . . . bjn
since we have reduced to the case where the vol Bj are monotonically decreasing. This
shows that the bjm are indeed uniformly bounded.
Case 2. All of the Ai have empty interiors.

vol B1
ηn−1 ,

≤

We claim that if there exists a packing of A into each brick Bj = [0, bj1] ×· · ·×[0, bjn],
jn]
jm = min{bjm, diam B1}. If we can justify this assertion, the
jm are certainly uniformly bounded

then there also exists a packing of A into the smaller brick B′
where we have deﬁned b′
theorem is established in this case as well since the b′
by diam B1.

j1] × · · · × [0, b′

j = [0, b′

For a collection A of sets with empty interiors, the packing condition that the po-
sitionings of the sets Ai must have disjoint interiors is no condition at all; in other
words, there exists a packing of the entire collection A into C if and only if there exists
individual positionings of each set Ai into C. Moreover, we can modify any positioning
σi(Ai) into the brick Bj so that it becomes a positioning of Ai into B′
j, by taking the ro-
tated/reﬂected set θi(Ai) and translating it just enough to lie the positive orthant of Rn.
More precisely, if σi = (θi, ξi) is such that σi(Ai) ⊂ Bj, then we deﬁne σ′
i) where
the mth coordinate ξ′

i = (θi, ξ′

im of the vector ξ′
ξ′
im =

i ∈ Rn is given by
inf{t ∈ πi(θi(Ai))}

(cid:12)
here πi denotes the projection map in the ith coordinate from Rn to R.
(cid:12)

The fact that σ′

from the deﬁnition of the ξ′

i(Ai) is contained in the positive orthant of Rn follows immediately
im. Also, we are assuming that Ai contains the origin, and

;
(cid:12)
(cid:12)

8

GREG MARTIN

so ξi is an element of σi(Ai); since σi(Ai) is contained in the positive orthant, it follows
that ξ′
im ≤ ξim, and consequently σ′
i(Ai) is contained in the brick Bj. Finally, since Ai
contains the origin it is clear that ξ′
im ≤ diam Ai, and since there exists a packing of A
into B1 we certainly have diam Ai ≤ diam B1. Therefore σ′
i(Ai) is indeed contained in
the brick B′
j.

Making this modiﬁcation for each set Ai results in a packing of the entire collection
A into the smaller brick B′
j (again, the assumption that the Ai have empty interiors
means that we do not need to worry about the relative positionings of the various Ai).
As remarked earlier, this justiﬁes the assumption that the dimensions of our bricks are
uniformly bounded, since we may replace Bj by B′

j throughout.

This completes the proof of the theorem.

In summary, we have established Theorems 1 and 2 modulo a proof of Proposition 1; this

proof will be the subject of the following section.

4. Proof of Proposition 1
Proposition 1 is essentially a consequence of the fact that the action on Rn of the space
of rigid motions O(n) × Rn is continuous. The following two lemmas, which give concrete
statements of the continuity of this action, will enable us to establish Proposition 1. We
note that the space O(n) × Rn can in fact be regarded as a metric space, inheriting as it
does the standard metric from Rn2
× Rn: if σ = (θ, ξ) and σ′ = (θ′, ξ′) are two elements of
O(n) × Rn, then the distance between them is
n

n

n

1/2

d(σ′, σ) =

|θ′ − θ|2 + |ξ′ − ξ|2

1/2

(cid:0)

(cid:1)

=

(cid:18)

Xl=1

Xm=1

(θ′

lm − θlm)2 +

(ξ′

m − ξm)2

Xm=1

,

(cid:19)

(4)

considering θ and θ′ here simply as n2-tuples of real numbers rather than elements of O(n).
Lemma 3. Let y be a point in Rn and U be an open subset of Rn. Suppose that σ is an
element of O(n) × Rn such that σ(y) ∈ U. Then there exists a positive real number δ such
that, for every σ′ ∈ O(n) × Rn satisfying d(σ′, σ) < δ, we have σ′(y) ∈ U.
Proof: For any y ∈ Rn and any pair τ = (θ, ξ), τ ′ = (θ′, ξ′) of elements of O(n) × Rn, we
have

|τ (y) − τ ′(y)| = |ξ + θy − ξ′ − θ′y| ≤ |ξ − ξ′| + |(θ − θ′)y|,

(5)

We certainly have |ξ − ξ′| ≤ d(τ, τ ′) by the deﬁnition (4) of the metric d. On the other hand,
all entries of the matrix θ − θ′ are also at most d(τ, τ ′) in absolute value, while the entries of
the vector y are at most |y| in absolute value. Therefore each entry of (θ − θ′)y is bounded
by n|y|d(τ, τ ′) in absolute value, and so the inequality (5) becomes the upper bound

|τ (y) − τ ′(y)| ≤ d(τ, τ ′) +

n

(cid:18)

Xm=1 (cid:0)

n|y|d(τ, τ ′)

1/2

2

(cid:19)

(cid:1)

= (n3/2|y| + 1)d(τ, τ ′)

(6)

(we have made no eﬀort to obtain a strong constant in the inequality).

Now if σ is an element of O(n) × Rn such that σ(y) lies in the open set U, then there
exists some positive number ε such that ∆ε(σ(y)) ⊂ U. If we set δ = ε(n3/2|y| + 1)−1, then

COMPACTNESS THEOREMS FOR GEOMETRIC PACKINGS

9

for any σ′ ∈ O(n) × Rn such that d(σ′, σ) < δ, the upper bound (6) tells us that

|σ′(y) − σ(y)| ≤ (n3/2|y| + 1)d(σ′, σ) < ε,

and therefore σ′(y) ∈ ∆ε(σ(y)) ⊂ U as desired.

Lemma 4. Let U1 and U2 be open subsets of Rn. Suppose that σ1 and σ2 are elements
of O(n) × Rn such that σ1(U1) ∩ σ2(U2) 6= ∅. Then there exists a positive real number δ
such that, for every σ′
2, σ2) < δ, we have
1(U1) ∩ σ′
σ′
Proof: Since σ1(U1) and σ2(U2) are open sets that are not disjoint, we can choose a point
x ∈ Rn and a positive number ε such that ∆ε(x) ⊂ σ1(U1) ∩ σ2(U2). Using Fact 2 we may
set y1 = σ−1

2 (x), so that ∆ε(y1) ⊂ U1 and ∆ε(y2) ⊂ U2; we also set

2 ∈ O(n) × Rn satisfying d(σ′

1 (x) and y2 = σ−1

1, σ1) < δ and d(σ′

2(U2) 6= ∅.

1, σ′

δ =

ε
n3/2 max{|y1|, |y2|} + 1
i ∈ O(n) × Rn such that d(σ′

,

Then for i = 1 or 2, for any σ′
us that

|σ′
i(yi) − x| = |σ′
i(yi)) = σ′

i(∆ε(yi)) ⊂ σ′

so that x ∈ ∆ε(σ′
an element of σ′

1(U1) ∩ σ′

i(yi) − σi(yi)| ≤ (n3/2|yi| + 1)d(σ′

i, σi) < ε,

2(U2), which is therefore nonempty as desired.

i(Ui) by Fact 1. In particular, this shows that x is

i, σi) < δ the upper bound (6) tells

Proof of Proposition 1: Let T = {τi} be a point in M(Rn) \ P(A, C). From the deﬁni-
tion (1) of P(A, C), one of the following two cases must hold.

Case 1. There exists a k ≥ 1 such that τk(Ak) 6⊂ C.
Choose a point x ∈ τk(Ak) \ C, and set y = τ −1

k (x) ∈ Ak (using Fact 2). Applying
Lemma 3 with σ = τk and U = Rn \ C, we see that there exists a positive number δ
such that, for every σ′ ∈ O(n) × Rn satisfying d(σ′, τk) < δ, we have σ′(y) ∈ Rn \ C,
that is, σ′(y) /∈ C.

Now deﬁne the open neighborhood S of T in M(Rn) by

S =

S = {σi} ∈ M(Rn) : d(σk, τk) < δ
(cid:8)

.
(cid:9)

For every S ∈ S, we see that σk(y) /∈ C by our choice of δ. On the other hand, certainly
σk(y) ∈ σk(Ak), and so S is not a packing of A into C. Since this is true for any S ∈ S,
we see that S ⊂ M(Rn) \ P(A, C).
Case 2. There exist positive integers k 6= l such that Int(τk(Ak)) ∩ Int(τl(Al)) 6= ∅.

Applying Lemma 4 with σ1 = τk, σ2 = τl, U1 = Int(Ak), and U2 = Int(Al), we see that
2 ∈ O(n) × Rn satisfying

1, σ′

there exists a positive real number δ such that, for every σ′
d(σ′
2, τl) < δ, we have
1(Ak)) ∩ Int(σ′

1, τk) < δ and d(σ′
Int(σ′

1(Int(Ak)) ∩ σ′

2(Al)) = σ′

2(Int(Al)) 6= ∅

(here we have used Fact 3). Now deﬁne the open neighborhood S of T in M(Rn) by

S =

S = {σi} ∈ M(Rn) : d(σk, τk) < δ and d(σl, τl) < δ
(cid:8)

.
(cid:9)

For every S ∈ S, we see that Int(σk(Ak)) ∩ Int(σl(Al)) 6= ∅ by our choice of δ, and so
S is not a packing of A with disjoint interiors. Since this is true for any S ∈ S, we see
that S ⊂ M(Rn) \ P(A, C).

10

GREG MARTIN

In either case we see that M(Rn) \ P(A, C) contains an open neighborhood S of T , which

shows that M(Rn) \ P(A, C) is an open set, i.e., P(A, C) is a closed subset of M(Rn).

5. Generalizations of Theorems 1 and 2

We end by brieﬂy discussing some extensions of Theorems 1 and 2 that can be established
by the methods of this paper. First, in the statements of these two theorems we have
claimed that “packings” may be replaced by “oriented packings”. This is true because the
positionings allowed in oriented packings (translations and rotations, but not reﬂections)
are parametrized by O(n)+ × Rn, where O(n)+ is the index-2 subgroup of O(n) consisting
of the orthogonal matrices of determinant 1. Because this subgroup O(n)+ is a compact
space in its own right, the analogous statement to Fact 7 for M+(C) = (O(n)+ × C)∞ is
also true, and thus all of the arguments of this paper go through for oriented packings upon
simply replacing M(C) by M+(C) at each occurrence. In the case of translated packings,
where neither rotations nor reﬂections are allowed, we can similarly replace each occurrence
of M(C) by C ∞ and the arguments proceed unchanged (if we like, we can think of the space
C ∞ as ({In} × C)∞, where {In} is the compact subgroup of O(n) consisting only of the
identity matrix).

It is clear that many variations on Theorems 1 and 2 could be stated by changing the
sequence of sets into which A can be packed. The important thing is for this sequence
Cj (which is a shrinking sequence of homothets in Theorem 1, and a sequence of bricks of
¯Dk to
varying dimensions in Theorem 2) to have enough structure for the limiting set
∞
j=k Cj as deﬁned in the statement of Lemma 2. This limiting
be identiﬁed, where Dk =
set would be easy to determine if the Cj were ellipsoids or simplices of varying dimensions,
just to name two possible applications.

∞
k=1

S

T

Finally we note two ways in which the hypotheses of Theorems 1 and 2 can be weakened.
Instead of requiring that the collection A can be packed into each set Cj, we can require
only that for each j ≥ 1 the contracted collection (1 − 1
j )A2, . . . } can
be packed into Cj. This is actually easily seen to be equivalent to the current statements
of Theorems 1 and 2. However, we obtain genuinely stronger theorems by weakening the
hypothesis in the following way: for every j ≥ 1, we require only that the ﬁnite collection
{A1, . . . , Aj} can be packed into the set Cj. We leave the details of this variation to the
reader.

j )A = {(1 − 1

j )A1, (1 − 1

Acknowledgements. The author acknowledges the support of Natural Sciences and Engineering Research
Council grant number A5123. The author would also like to thank Mark Hamilton for his comments on a
preliminary version of this paper.

References

[1] K. Ball, On packing unequal squares, J. Combin. Theory Ser. A 75 (1996), no. 2, 353–357.
[2] H. T. Croft, K. J. Falconer, and R. K. Guy, Unsolved problems in geometry, Springer-Verlag, New York,

1994.

[3] A. Meir and L. Moser, On packing of squares and cubes, J. Combinatorial Theory 5 (1968), 126–134.
[4] J. R. Munkres, Topology: a ﬁrst course, Prentice-Hall Inc., Englewood Cliﬀs, N.J., 1975.
[5] M. M. Paulhus, An algorithm for packing squares, J. Combin. Theory Ser. A 82 (1998), no. 2, 147–157.

Department of Mathematics, University of Toronto, Canada M5S 3G3
E-mail address: gerg@math.toronto.edu

