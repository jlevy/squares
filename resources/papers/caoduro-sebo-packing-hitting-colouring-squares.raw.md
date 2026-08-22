4
2
0
2

n
u
J

3

]

G
C
.
s
c
[

3
v
5
8
1
2
0
.
6
0
2
2
:
v
i
X
r
a

PACKING, HITTING, AND COLOURING SQUARES

Marco Caoduro ∗ and András Sebő †

Abstract. Given a finite family of squares in the plane, the packing problem asks for the
maximum number ν of pairwise disjoint squares among them, while the hitting problem for
the minimum number τ of points hitting all of them. Clearly, τ ≥ ν. Both problems are
known to be NP-hard, even for families of axis-parallel unit squares.

The main results of this work provide the first non-trivial bounds for the τ /ν ratio
for not necessarily axis-parallel squares. We establish an upper bound of 6 for unit squares
and 10 for squares of varying sizes. The worst ratios we can provide with examples are 3 and
4, respectively. For comparison, in the axis-parallel case, the supremum of the considered
ratio is in the interval [ 3
2 , 4] for squares of varying sizes. The
methods we introduced for the τ /ν ratio can also be used to relate the chromatic number χ
and clique number ω of squares by bounding the χ/ω ratio by 6 for unit squares and 9 for
squares of varying sizes.

2 , 2] for unit squares and [ 3

The τ /ν and χ/ω ratios have already been bounded before by a constant for “fat”
objects, the fattest and simplest of which are disks and squares. However, while disks
have received significant attention, specific bounds for squares have remained essentially
unexplored. This work intends to fill this gap.

1

Introduction

Let F be a finite family of convex sets in the plane. A packing in F is a subfamily of pairwise
disjoint sets in F, a hitting set of F is a set of points which has a non-empty intersection
with each F ∈ F, a colouring of F is a partition of F into packings, and a clique in F is
a pairwise intersecting subfamily in F. The maximum size of a packing in F, the packing
number, is denoted by ν(F) and the minimum size of a hitting set of F, the hitting number,
by τ (F). The maximum size of a clique in F, the clique number, is denoted by ω(F) and
the minimum size of a colouring of F, the chromatic number, by χ(F). For p ∈ R2 the
number of F ∈ F containing p is the degree of p in F and ∆(F) denotes the maximum
degree. Clearly, ν(F) ≤ τ (F) and ∆(F) ≤ ω(F) ≤ χ(F). A family of convex sets is said
to have the Helly property if, for any clique, there exists a point contained in all of them. If
a family F has the Helly property, then ω(F) = ∆(F). Axis-parallel rectangles (and boxes
in arbitrary dimensions) have the Helly property. On the other hand, the property does not
extend to general rectangles, not even to unit squares. Figure 1 shows three unit squares
with ∆ = 2 and ω = 3.

∗Sauder School
marco.caoduro@ubc.ca

of Business, The University

of British Columbia, Vancouver, Canada,

†CNRS, Laboratoire G-SCOP, Univ. Grenoble Alpes, Grenoble, France, andras.sebo@cnrs.fr

1

 
 
 
 
 
 
Figure 1: Three pairwise intersecting unit squares.

The problems of determining the packing and hitting numbers of a given family of
subsets in the plane are proved to be NP-hard already in the particular case of axis-parallel
unit squares [10]. However, there are polynomial-time approximation schemes (PTAS) to
compute these parameters for arbitrary families of squares, even without the constraint of
being axis-parallel [6].

Imai and Asano [16] noticed that the clique number of a family of axis-parallel rect-
angles (equal to the maximum degree of the family) can be computed in linear time, but
determining the chromatic number for such a family is NP-hard. Even though their hardness
reduction does not seem to apply to axis-parallel squares directly, a simple modification of
a result on unit disks of Clark, Colbourn, and Johnson’s [7, Theorem 2.1], shows that this
problem is NP-hard even for the special case of axis-parallel unit squares (see Appendix A).
In this paper, our foci are the τ /ν and χ/ω ratios and not these complexity issues, which,
however, are important since they make the existence of min-max theorems and exact algo-
rithms unlikely unless P=NP.

It is surprising that the most natural bounds relating the packing and hitting num-
bers are wide open even for some of the simplest geometric objects. Our goal is to decrease
this gap for squares. We bound τ from above with a linear function of ν and deduce similar
bounds for ω and χ as well. These bounds are realized by using novel arguments that build
on elementary geometric tools. The phenomenon is reminiscent to the “rounding” idea of
integer programming. Indeed, it consists in “filling holes for free” in reformulations as “cov-
ering” problems, but instead of integrality, the “discrete jump" is due to the forcing rules
of Euclidean geometry. Using less refined and more common techniques, we also extend
the linear bounds to a family of similar convex sets: two convex sets are called similar if
they arise from one another by translations, rotations, and homotheties. Similarity is an
equivalence relation, and squares form an equivalence class. Better results can be proved if
only translations and rotations are allowed, including the special case of unit squares. Ex-
cluding rotations, we get another special case that includes axis-parallel squares, for which
even better results hold (see Table 1).

Note that while linear bounds for various convex sets are known – either through
Pach’s work [20] on the χ/ν ratio or via an extension of his method (Theorem 5) for the τ /ν
ratio – our main achievement lies in providing the first specific tools and non-trivial bounds
for squares. This fills a major gap in the subject: although considerable efforts have been
made to improve the upper and lower bounds for these ratios for disks [7, 15,17], there seem
to be no results specific to squares besides the statement of the relatively easy bounds for
axis-parallel squares [1].

2

translation

translation +
homothety

convex set
τ ≤ 6ν
[8]
τ ≤ 16ν
[18]

translation + τ ≤ 18 ρ2 ν

rotation

Cor. 2

translation + τ ≤ 18 ρ2 ν
homothety +
rotation

Cor. 2

centrally symmetric
τ ≤ 6ν
[8]
τ ≤ 7ν
[8]
τ ≤ 4⌈ρ⌉2ν
Cor. 2
τ ≤ 8⌈ρ⌉2ν
Cor. 2

disk
τ ≤ 4ν − 1
[8]
τ ≤ 7ν − 3
[8]
τ ≤ 4ν − 1
[8]
τ ≤ 7ν − 3
[8]

square
τ ≤ 2ν − 1
[1]
τ ≤ 4ν − 3
[1]
τ ≤ 6ν
Thm. 1
τ ≤ 10ν
Thm. 1

Table 1: τ /ν bounds for a family obtained by translations, rotations, or homotheties of a
convex set A. The slimness ρ(A) of A is defined here as R/r where R is the smallest radius
of a disk containing A and r is the largest radius of a disk contained in A (see Section 2).

The numbers τ , ν, χ, ω can be often interpreted and used as parameters of the

intersection graph:

The intersection graph of a family F of sets, denoted by G(F), is the graph having F
as vertex set and an edge between two vertices if and only if the corresponding sets intersect.
Our notations and terminology for F follow the usual graph theory notations for G(F), that
is, χ(F) = χ(G(F)) and ω(F) = ω(G(F)). Of course, the maximum degree ∆(G(F)) of the
graph G(F) is not the same as the maximum degree ∆(F) of the family F.

A neighbour of F ∈ F is a set F ′ ∈ \{F } such that F ∩ F ′ ̸= ∅. The neighbourhood
N (F ) of F consists of all its neighbours, while the closed neighbourhood is N [F ] := N (F ) ∪
{F }. Given a positive integer D ∈ N, a graph is called D-degenerate if each of its subgraphs
has a vertex of degree at most D. We call a family F of sets D-degenerate if every non-empty
subfamily F ′ ⊆ F contains a set F ′ ∈ F ′ which intersects at most D other sets of F ′, that is,
if its intersection graph is D-degenerate. All vertices of a D-degenerate graph can be deleted
by sequentially deleting a vertex of degree at most D; colouring the vertices in the reverse
order, we see that the graph is D + 1 colourable. Consequently,a D-degenerate family has a
(D + 1)-colouring. Although this is quite a rough, greedy way of colouring, degeneracy is a
frequently used method, often providing the best-known way to colour geometric intersection
graphs [17, 20, 21].

Clearly, deleting N [F ] (F ∈ F), the maximum size of a packing in F decreases by
at least one, and the hitting number decreases by at most τ (N [F ]). This provides an induc-
tive argument-based bounding of the τ /ν ratio, leading to a linear upper bound whenever
τ (N [F ]) can be upper bounded by a constant (see Lemma 2). In close analogy with D-
degeneracy for colouring, we say that a family F is hitting-k-degenerate (k ∈ N) if for every
F ′ ⊆ F there exists F ′ ∈ F ′ such that τ (N [F ′]) ≤ k. Hitting-degeneracy was successfully
employed in Kim, Nakprasit, Pelsmajer, and Skokan [18] and Dumitrescu and Jiang [8] when
dealing with translates of convex bodies (referred to as “greedy decomposition”) and will also
be our main framework for bounding the τ /ν ratio. This framework is far from being opti-
mal, but it is the unique one for most geometric intersection problems. The following lemma
gives a bound on τ (N [F ]) for squares. Its proof, presented in Section 4, is based on novel

3

geometric ideas:

Lemma 1. Let C be a family of unit squares. The neighbours of any square C ∈ C can be
hit by 10 points. Moreover, if the centre of C is left-most among all centres in C, 6 points
suffice.

While the induction by degeneracy is a kind of simple greedy framework, bounding
τ (N [F ]) is a real challenge. The first part of Lemma 1 can be extended to squares of
arbitrary size by selecting a square with minimal size and applying homothety to each of its
neighbours (“local homothety,” see Section 2), allowing us to conclude:

Theorem 1. If C is a family of squares, τ (C) ≤ 10ν(C). Moreover, if the squares have equal
size, τ (C) ≤ 6ν(C).

Finding lower bounds for the ratio τ /ν is also challenging. The only known lower
bound for families of axis-parallel squares is 3/2, achieved by a family of unit squares whose
intersection graph is a vertex disjoint union of 5-cycles; no better lower bound is known for
squares of different sizes. If arbitrary rotations of the squares are allowed, the τ /ν ratio for
unit squares may even be 3, and 4 if squares of different sizes are allowed:

Theorem 2. There exists a family of 9 pairwise intersecting unit squares that cannot be hit
with less than 3 points. Moreover, there exists a family of 13 pairwise intersecting squares
that cannot be hit with less than 4 points.

Pach [20] proved that for any family F of convex sets in the plane, χ(F) ≤ 9q∆(F),
where for each F ∈ F the ratio between the area of the smallest disk Disk(F ) containing
F (outer disk) and the area of F is at most q ∈ R. If C consists of squares, then q = π
2 , so
Pach’s bound is χ(C) ≤ 9 π

2 ∆(C) ≈ 14.14∆(C). This can be essentially improved:

Theorem 3. If C is a family of squares and ∆(C) ≥ 2, χ(C) ≤ 9(∆(C) − 1). Moreover, if
the squares have equal size, χ(C) ≤ 6∆(C).

Other results on the chromatic number of families of convex sets can be found in

Table 2. Recall that for any family F, ∆(F) ≤ ω(F).

We do not know about non-trivial lower bounds for colouring squares. The intersec-
tion graph of unit squares may be a C5 with chromatic number χ = 3 and clique number
ω = 2. However, the 3/2 lower bound cannot be easily kept for higher values of ω: the
best-known bound arises by choosing ω to be divisible by 4, taking each square of the C5
example ω/2 times. In terms of the intersection graph, this is a replication of each vertex
ω/2 times, and an optimal colouring is provided then by taking each of the five maximal
stable sets of C5 ω/4 times, as colour classes, showing χ = 5
4 ω (see [9]). This seems to be
the best example known for squares of varying sizes and not necessarily axis-parallel as well.

The paper is organized as follows. Section 2 introduces the main techniques of
the paper. First, it formalizes the greedy argument that connects hitting degeneracy with
the hitting number and presents a proof of Pach’s bound, which also serves as an initial
example of the “local homothety operation.” Then, a simple and well-known relation is

4

translation

convex set
χ ≤ 3ω − 2
[17]

translation+ χ ≤ 6ω − 6
homothety
translation+
rotation
translation+
homothety+
rotation

[17]
χ ≤ 9q∆
[20]
χ ≤ 9q∆
[20]

centrally symmetric
χ ≤ 3ω − 2
[17]
χ ≤ 6ω − 6
[17]
χ ≤ 9q∆
[20]
χ ≤ 9q∆
[20]

disk
χ ≤ 3ω − 2
[21]
χ ≤ 6ω − 6
[17]
χ ≤ 3ω − 2
[21]

square
χ ≤ 2ω − 1
[21]
χ ≤ 4ω − 3
[1]
χ ≤ 6∆
Thm. 3

χ ≤ 6ω − 6 χ ≤ 9(∆ − 1)

[17]

Thm. 3

Table 2: χ/ω and χ/∆ bounds for translations, rotations, or homotheties of a convex set.

explored between hitting a family of geometric objects and covering a set of points by such
a family. This relation allows us to show some first bounds on the τ /ν ratio, in particular,
a bound for the hitting number (Theorem 5) similar to Pach’s bound for the chromatic
number, and also to point at the incompleteness of this method: while an appropriately
defined covering is always sufficient for defining a hitting set, it is necessary only in the axis-
parallel case. In Section 3, we develop the main tools that essentially improve the “covering
method,” enabling us to turn even some partial coverings into hitting sets, enhancing our
bounds. In Section 4, we use the tools from the previous sections to prove the upper and
lower bounds for hitting (Theorem 1, Theorem 2) and the upper bound for the chromatic
number (Theorem 3). Section 5 concludes the paper with a collection of open questions.

2

Initial framework and basic tools

In this section, we first set the framework of the paper and then gradually build the tech-
niques towards our main results:

Section 2.1 works out necessary details for the use of hitting-degeneracy and shows
a first example of the local homothety operation by shortly presenting Pach’s proof for his
general bound for the chromatic number [20]. Section 2.2 explains the relationship between
the hitting sets of a family of unit balls and sets covering their centres. This transition from
hitting to covering offers a new perspective on the problem and allows us to show a first
bound on the hitting number of squares that will be improved later. Finally, Section 2.3
applies these techniques for bounding the hitting number of convex sets.

2.1 Hitting degeneracy and local homothety

We use a tool similar to D-degeneracy to bound the hitting number of squares. The following
well-known lemma [8, 18] formulates the simple and standard induction step converting
constant size hitting sets of neighbourhoods into a linear bound between τ and ν.

Lemma 2. Let F be a hitting-t-degenerate family of sets. Then τ (F) ≤ tν(F). Moreover,
if τ (F ′) ≤ t0 for any F ′ ⊆ F satisfying ν(F ′) = 1, then τ (F) ≤ t0 + t(ν(F) − 1).

5

Proof. We proceed with the proof of the second statement by induction on ν(F) since then
the first statement follows by substituting t0 := t.
If ν(F) = 1, then τ (F) ≤ t0 by the
condition. Assume now that ν(F) ≥ 2 and that the statements are true for any subfamily
F ′ of F having ν(F ′) < ν(F). Let F ∈ F be given by the condition, that is, N [F ] can be
hit by t points. Any packing I ′ in F − N [F ] has size at most ν(F) − 1 since I ′ ∪ {F } is
a packing in F. Then, since the condition is still satisfied by F − N [F ], by the induction
hypothesis,

τ (F) ≤ τ (F − N [F ]) + τ (N [F ])

≤ t0 + t(ν(F − N [F ]) − 1) + t
= t0 + t(ν(F) − 2) + t
= t0 + t(ν(F) − 1).

The following lemma presents a straightforward connection between degeneracy and
hitting degeneracy. Together with Lemma 1, it will allow us to derive an upper bound on
the chromatic number of squares.

Lemma 3. Any hitting-t-degenerate family of sets F is also (t∆(F) − 1)-degenerate.

Proof. Let F ′ be a subfamily of F. Since, F is hitting-t-degenerate, there is a set F ′ ∈ F ′
such that τ (N [F ′]) ≤ t. We show that F ′ has at most t∆(F) − 1 neighbours. Each of
the points in a hitting set of N [F ′] is contained in at most ∆(F ′) ≤ ∆(F) sets. Hence,
|N [F ′]| ≤ τ (N [F ′])∆(F) ≤ t∆(F) and so |N (F ′)| ≤ t∆(F) − 1.

Now, we present Pach’s result, the proof of which details the local homothety opera-

tion.

Theorem 4 (Pach, 1980 [20]). Let q ∈ R+ and F be a family of convex sets in the plane.
If for each F ∈ F the ratio between the area of the smallest disk Disk(F ) containing F and
the area of F is at most q, then χ(F) ≤ 9q∆(F).

Proof. The chromatic number of any D-degenerate family is bounded by D + 1. Hence, it
is enough to show that F is (9q∆(F) − 1)-degenerate. Let F0 ∈ F be such that Disk(F0)
has the shortest radius among F ∈ F and choose the unity to be the length of this radius.
We check |N (F0)| ≤ 9q∆(F) − 1.

For each F ∈ N (F0), define a new convex set F ′ by picking an arbitrary point
p ∈ F ∩ F0 and applying an appropriate homothety with centre p and ratio λ ≤ 1 so that
the image of the outer disk of F (which coincides with Disk(F ′)) has radius 1. We call this
operation local homothety. Let c0 be the centre of Disk(F0) and note that for all F ∈ N [F0],
each outer disk Disk(F ′), and so F ′, is contained in the disk B of centre c0, and radius 3.

Since, by convexity F ′ ⊆ F , the local homothety operation did not increase the
maximum degree of F. Therefore the disk B is covered by the images {F ′ : F ∈ N [F0]} at
most ∆(F) times. Moreover, the areas of the images {F ′ : F ∈ N [F0]}, each of which is at

6

least π/q by the definition of q, sum up to less than 9π∆(F). These two observations yield
|N (F0)| ≤ |N [F0]| − 1 ≤ 9∆(F )π

π/q − 1 = 9q∆(F) − 1.

Surprisingly, in both the problem of bounding the chromatic numbers of intersection
graphs of geometric objects in terms of their maximum degrees and the problem of bounding
their hitting numbers in terms of their packing numbers, it seems that no approach is
known that takes into consideration the family of objects in a more global way. While we
continue exploiting the well-known greedy framework of degeneracy and hitting-degeneracy
(Lemma 2), often used for bounding the chromatic and hitting numbers of convex sets, we
now also frontally face new challenges for bounding the parameters t and t0. Doing this, our
questioning is not about the mere existence of constant bounds, which are much easier and
follow from Pach’s generic method (Theorems 4 and 5). It is rather inspired by the spirit
of combinatorial optimization, where the goal is to find the best possible constant. The
endeavour to find the best bound leads to geometry problems that are interesting in their
own right and can be addressed using classical results, such as Thales’ Theorem, in novel
ways.

2.2 Relating hitting and covering

In this section, we consider the relation of covering problems to hitting problems for various
geometric objects. These two problems are equivalent for axis-parallel unit squares and the
equivalence is a special case of a general statement about unit balls of normed spaces of
arbitrary dimension.

For an arbitrary norm || ||, a ball is a set of the form

B(c, r) := {x ∈ Rn : ||x − c|| ≤ r} (c ∈ Rn, r ∈ R+).

The point c is called the centre of the ball, r is its radius, and B(c, r) is its boundary. A ball
centred at 0, of radius r is a compact convex set, moreover it is centrally symmetric that is,
for x ∈ B, −x ∈ B. Conversely, it is also true that any centrally symmetric compact convex
set with a non-empty interior is the unit ball for a norm.

We primarily use the l2-norm, also called Euclidean-norm, and the l∞-norm, also
called max-norm; the only distance function we use is dist(x, y) := ||x − y||2, omitting
In two dimensions, a ball B2(c, r) for the Euclidean norm is called a disk of
the index.
radius r and its boundary B2(c, r) is called a circle; similarly, for the max-norm, B∞(c, r)
and B∞(c, r) are an axis-parallel square of side 2r and its boundary. Note the difference
between axis-parallel unit squares B∞(c, 1/2), i.e., 1 × 1 squares, and unit balls B∞(c, 1),
i.e., 2 × 2 squares.

Some further notations will be useful: if X is a set of points, conv(X) denotes their
convex hull; if X = {a, b}, we use use the shorter notation [a, b] := conv(X). For a square
C, l(C) is the length of a side of C, c(C) denotes the centre of C, and given a family of
squares C, c(C) := {c(C) : C ∈ C}.

7

2 such that V ⊆ (cid:83)

Let V ⊆ R2 and || || be a norm. A covering with respect to V is a set B of balls
of radius 1
B∈B B. A set of points A ⊆ V is independent if for any pair
of different points u, v ∈ A, ||u − v|| > 1. The minimum size of a covering, the covering
number, is denoted by ζ(V ), and the maximum size of an independent subset of points by
α(V ). Note that α ≤ ζ since the distance of any two points x, y ∈ B(c, 1/2) is at most 1.
We will mainly use ζ and α for the Euclidean norm l2 or the max-norm l∞ by using the
indices 2 or ∞.

Proposition 1. For any norm and family B of balls of radius 1
τ (B) = ζ(c(B)).

2 , ν(B) = α(c(B)) and

Proof. The first equality follows from the simple fact that P ⊆ B is a packing if and only if
for all p, q ∈ c(P), ||p − q|| > 1. For the second equality note that H is a hitting set of B, if
and only if for each c ∈ c(B) there exists h ∈ H such that ||c − h|| ≤ 1
2 . This means that
the balls of radius 1
2 with centres in H cover c(B).

For the max-norm, we immediately obtain the following result.

Corollary 1. For any family C of axis-parallel unit squares, ν(C) = α∞(c(C)) and τ (C) =
ζ∞(c(C)).

Considering a family of axis-parallel unit squares, the neighbours of any of its squares
can be hit by at most four points (the four vertices), and the ones of a left-most square by
at most two points (the two vertices on the right side). This simple fact can be reformulated
and proved as follows: the centres of all possible axis-parallel unit squares intersecting a
unit square C form an axis-parallel square of size 2 × 2 with centre c(C). Hence, four unit
squares are enough to cover them, and only two suffice if the centre of C is a left-most one (see
Figure 2). By Corollary 1, τ (c(N [C])) = ζ∞(c(N [C])) is at most 4 and 2, respectively. The
greedy induction and the local homothety presented in Section 2.1 can be used to convert
these bounds into τ ≤ 4ν − 3 for axis-parallel squares of arbitrary size and τ ≤ 2ν − 1 for
axis-parallel unit squares [1].

Figure 2: An axis-parallel square and the domain of the centres of its neighbours.

Corollary 1 is not directly applicable to not necessarily axis-parallel squares. We
make a detour through other norms to still apply the second part of Proposition 1 at the

8

Cc(C)c(N[C])price of losing a small constant factor. The inner disk of a unit square C is B2(c(C), 1
its outer disk is B2(c(C),
packing the outer disks, we also pack the correspondent squares.

2 ) and
√
2
2 ). Hitting the inner disks, we also hit the original squares, and

We illustrate now how the hitting number of the neighbours of a unit square can be
bounded with the help of the second part of Proposition 1, establishing hitting-degeneracy.
This bound is weaker than Lemma 1, which will be proved by completing the covering
argument used here with the novel methods of Section 3.

Proposition 2. Let C be a family of unit squares and C0 ∈ C. Then τ (N [C0]) ≤ 12, so
τ (C) ≤ 12ν(C).

Proof. By Lemma 2, the second inequality is a straightforward consequence of the first one.
The centres of any unit square intersecting C0 are clearly contained in a square T of size
√
2 + 1. Denote by B the family of disks we get by replacing each C ∈ N [C0] by its inner
disk B ⊆ C of radius 1
2 . According to Proposition 1, τ (N [C0]) ≤ τ (B) = ζ2(c(B)), in other
words, τ (N [C0]) can be upper bounded by the minimum number of disks of radius 1
2 that
cover T . To prove that 12 such disks are sufficient, it is enough to give these disks. Since
we will prove the better bound 10 with a more powerful method, we just refer to a result of
Nurmela and Östergård. In [19], they provide for 1 ≤ n ≤ 30 the minimum rn of the equal
radii of n disks covering a unit square. Then proportionally,
is the maximum size of a
square that can be covered by disks of radius 1

1
2rn
2 + 1.

√

>

2 , and 1
2r12

To summarize, the hitting and covering problems are equivalent for axis-parallel unit
squares (Corollary 1), but they are not if some of the given unit squares are not axis-parallel.
We overcome this difficulty by covering with the inner disks of the unit squares instead of
the unit squares themselves and packing the outer disks. In this way, the method can be
saved at the price of weaker bounds. The loss can be decreased by showing that the covering
does not have to be perfect: “holes” with certain metric properties can be “patched.” The
main progress of our work is reached by three observations stating that the centres of the
covering disks actually hit more squares than those with centres in the union of the disks.
They also hit the squares whose centres are in the holes if these uncovered territories are
small enough. For example, Figure 3 shows three light (blue1) disks of diameter 1, whose
centres hit each unit square having its centre in the light (blue) region, since it even hits
their inner disks by Corollary 1; however, even if the centre is not in the light (blue) region,
but in the dark (blue) “hole,” as for the represented unit square, the square is hit by one
of the three centres. So the dark (blue) hole can be “patched” (Lemma 4). In Sections 3
and 4, the idea of allowing holes in the cover and covering them with “patches” is further
explored and used to improve the bound offered by Proposition 2.

2.3 A bound on the hitting number of convex sets

In this section, we show how to apply the tools introduced in Sections 2.1 and 2.2 to convex
sets in general. Focusing exclusively on how the covering tool can be used will help us

1The text is meant to be understandable without the colours as well.

9

Figure 3: A “hole” not covered by any of three disks, but “patched”: the three vertices of
the triangle hit all unit squares having their centre in the dark (blue) hole as well.

construct more complex geometric arguments by mixing several tools. At the same time, we
see that such a brute force application of the covering tool already shows a constant bound
for τ /ν for the translates of rotated homothetic copies of a fixed convex set. The rest of the
paper will then enrich this framework with novel geometric arguments, providing essential
improvements for squares.

For a compact convex set K, we can define the slimness of K, denoted by ρ|| ||(K),
as the ratio of the radius of the smallest ball (in norm || ||) containing K and the largest ball
contained in K. If the latter is 0, the ratio is ∞. For the most commonly used Euclidean
and max norms: ρ2(K) denotes the ratio of the radius of the smallest disk containing
K and the largest disk contained in K; similarly, ρ∞(K) is the ratio of the sides of the
smallest axis-parallel square containing K and the largest axis-parallel square contained in
K. Observe that ρ2(K) is invariant under translations, rotations and homothety. Moreover,
since a disk of radius r is contained in a square of size 2r and contained a square of size
√
2 from each other. Pach’s
coefficient q(K) for a convex set K is the quotient of the areas of the outer disk of K, and
K itself, implying q(K) ≤ ρ2(K)2. The slimness is a parameter that has been often used
when studying the packing and hitting number (see, for example, [1] and [6]).

2r, the parameter ρ2(K) and ρ∞(K) are within a factor of

√

The proof of the following theorem is based on the local homothety operation, applied

here to the τ /ν ratio.

Theorem 5. Let F be a family of convex sets in the plane. Then

(i) τ (F) ≤ 9 ρ∞(F)2ν(F).

Moreover, if the sets are centrally symmetric, (ii) τ (F) ≤ 4⌈ρ∞(F)⌉2ν(F), and (iii) τ (F) ≤
2⌈ρ∞(F)⌉2ν(F), if the inner squares are all of the same size.

Proof. We proceed by using local homotheties to deduce hitting-degeneracy (as Pach [20] did
by degeneracy for the chromatic number, see the proof of Theorem 4), and then, applying
Lemma 2. In the proof, we use the max-norm ρ∞(F) = ρ∞, so a ball of radius r ∈ R is an
axis-parallel square of side length 2r. All the squares in this proof are axis-parallel so we
omit this specification.

that the side length of its inner square is 1, and F0 ⊆ B∞(c0, ρ∞

Let F0 ∈ F be a convex set with the smallest inner square and assume for simplicity
2 ) for a c0 ∈ R2. Apply local

10

Rc(R)homotheties: for each F ∈ N (F0) consider a point f ∈ F0 ∩ F and take a homothetic copy
F ′ of F with centre f and ratio λ ≤ 1 so that the image of the inner square of F (which is
the inner square of F ′) is a unit square. Define F ′
0 := F0. Since every F is convex, we have
that:

(a) F ′ ⊆ F ;
(b) f ∈ F0 ∩ F ′, in particular, F0 ∩ F ′ ̸= ∅;
(c) There is a square of side length ρ∞ containing F ′.

By (a), we can hit the sets in N [F0] by hitting N ′ := {F ′ : F ∈ N [F ]}, which can be
achieved, in turn, by hitting their inner squares. Denote the family of these inner squares by
S′. Properties (b) and (c) imply then that all sets in N ′, are contained in B∞(c0, 3
2 ρ∞), and
therefore the centres of the inner squares of S′, all of side length 1, are in B∞(c0, 3
2 (ρ∞ −1))
(Figure 4). By Corollary 1, then hitting all possible inner squares is equivalent to covering
the square B∞(c0, 3

2 (ρ∞ −1)) by unit squares. Hence,

τ (N [F0]) ≤ τ (N ′) ≤ τ (S′) ≤ ζ(B∞(p,

3
2

(ρ∞ −1))).

We immediately get ζ(B∞(c0, 3
trary subfamily of F, we see that it is hitting-9 ρ2

2 (ρ∞ −1))) ≤ ⌈3(ρ∞ −1)⌉2 ≤ 9 ρ2

∞ . Applying this to an arbi-
∞-degenerate, so (i) follows from Lemma 2.

Figure 4: The outer and inner squares of two intersecting convex sets with slimness ρ∞ and
inner unit squares.

The proof of (ii) follows with the only difference that it exploits the fact that the
centres of the inner and outer squares coincide, and the centres of outer squares of sets in
N ′ are all in B∞(c0, ρ∞), the square of centre c0 and side length 2 ρ∞.

If, in addition, the inner squares of the centrally symmetric sets in F have all the
same size, local homothety is not needed anymore, leaving us free to choose F0 ∈ F to

11

B∞(c0,ρ∞2)B∞(c0,32(ρ∞−1))B∞(c0,32ρ∞)cc0B∞(c0,ρ∞)F0Fhave in addition an inner square with a left-most centre. Now the centres of outer squares
are contained in one half of B∞(c0, ρ∞), denote it by M . We get τ (N [F0]) ≤ ζ(M ) ≤
⌈ρ∞⌉⌈2 ρ∞⌉ ≤ 2⌈ρ∞⌉2.

In order to bound the hitting number of translates of rotated homothetic copies of
a fixed convex set K, it is unfortunately not sufficient to substitute its slimness to Theorem
5, since ρ∞ is not invariant under rotation. However, ρ2 is, and using this, the theorem can
be applied. Since ρ∞(K) ≤

2 ρ2(K), this only adds a factor of 2 in the bounds.

√

Corollary 2. Let F be a family of translates of rotated homothetic copies of a fixed convex
set K in the plane. Then

τ (F) ≤ 18 ρ2(K)2ν(F).
The upper bound decreases to 8⌈ρ2(K)⌉2ν(F) when K is centrally symmetric, and further to
4⌈ρ2(K)⌉2ν(F) if K is centrally symmetric and F contains exclusively translates of rotated
copies of K.

These estimates are, of course, rough but do satisfy the modest goal of showing how
local homothety applies to exploiting slimness and how to take advantage of particularities
like central symmetry to sharpen the results. For squares and unit squares, we will be more
meticulous, focusing on obtaining the best bound we can.

3 Filling holes

This section finds “patches” for “holes” uncovered by disks. Patches cover “for free," i.e.,
without using more disks for the covering. A first kind of hole, shown by Figure 3, is discussed
and patched in Section 3.1. Section 3.2 further develops this technique by finding another
set of patches using Thales’ celebrated theorem. Section 3.3 describes how to combine the
previous two covering tools to hit squares intersecting a convex polygon. Finally, Section 3.4
completes the picture by showing one more patch for filling holes.

The initial “covering disks” (Section 2.2) strengthened by these patches allow us to

prove our best hitting/packing ratio (Section 4).

3.1 Filling holes inside triangles

First, we prove the assertion anticipated by Figure 3.

Lemma 4 (Triangular patch). Let a, b, c ∈ R2 be three points at distance at most 1 from
one another. Then any square C of sides at least 1 and centre c(C) in T := conv({a, b, c})
contains at least one point from {a, b, c}.

Proof. By the condition, c(C) ∈ K := T ∩ C. We prove that the polygon K has a vertex
which is a vertex of T .

Suppose for a contradiction that this is not true. Then the vertices of K are vertices
of C or intersections of a side of C and of a side of T , so the vertices of K lie on the sides of

12

C, and actually all of them lie on two intersecting sides [x, y], [y, z] of C since the distance
of any pair of vertices on two distinct parallel sides of C is at least 1, while the distance
of any pair of points in T \ {a, b, c} is strictly smaller than 1. However, among the convex
hulls of pairs of points in [x, y] ∪ [y, z], only [x, z] contains c(C). Since c(C) ∈ K, we have
x, z ∈ K ⊆ T . But dist(x, z) > 1, a contradiction.

3.2 Filling holes outside separating lines

The following equivalence is an immediate consequence of Thales’ Theorem.

Proposition 3. Let a, b be two points on a line L ⊆ R2, q the midpoint of the segment [a, b],
and c a point in R2 \ L. Then there exists a right-angled triangle with a closed subsegment
of the open interval (a, b) as hypotenuse and c as the third vertex if and only if dist(c, q) <
dist(q, a), i.e., c is in the open disk with centre q and radius [q, a].

We say that a line separates two sets if these sets are in two different open half-planes
bordered by the line. The following lemma is still essentially Thales’s theorem, reformulating
and completing the equivalence of Proposition 3 into a form comfortable for hitting sets:

Lemma 5. Let a, b be two points on a line L ⊆ R2, dist(a, b) ≤ 1, let q be the midpoint of
the segment [a, b], and c ∈ R2 \ L. If dist(q, c) ≥ dist(q, a), then each unit square S, c ∈ S
so that L separates c(S) from c, and S ∩ [a, b] ̸= ∅ contains either a or b (Figure 5).

Figure 5: Illustration of Lemma 5.

Proof. Assume for a contradiction that dist(q, c) ≥ dist(q, a), but there exists a unit square
S whose centre is separated from c by L, which meets [a, b], contains c, but neither a nor
b. By the separation and the convexity of S, S ∩ [a, b] is a non-empty, closed subsegment of
the open interval (a, b), and since dist(a, b) ≤ 1, no two parallel sides of S can meet [a, b].

Therefore the half-plane containing c intersects S in a right-angled triangle T ′ :=
conv(a′, b′, c′), with hypotenuse [a′, b′] ⊂ [a, b], and right angle in c′. Applying the if part
of Proposition 3 to the point c′ and the triangle T ′, we have that c′, and consequently
T ′, is contained in the disk with centre q and radius smaller than [q, a]. Since c ∈ T ′,
dist(q, c) < dist(q, a) contradicting the indirect assumption.

13

Laqbcc(S)Figure 6: Illustration of Theorem 6; condition (iii) is required for i = 1.

3.3 Hitting squares using polygons

Combining Lemma 4 and Lemma 5, we get a sufficient condition for hitting each unit square
intersecting a compact set inside a convex polygon and far enough from its vertices. This
tool is presented in the following theorem:

Theorem 6. Let P ⊆ R2 be a convex polygon with vertices denoted by p1,
..., pk and let
p0 ∈ P . For each 1 ≤ i ≤ k, denote by qi the midpoint of the side [pi, pi+1] of P , where
pk+1 := p1. Assume that:

(i) dist(p0, pi) ≤ 1, for any 1 ≤ i ≤ k,

(ii) dist(pi, pi+1) ≤ 1, for any 1 ≤ i ≤ k.

Moreover, let C ⊆ P be a closed set. Then any unit square S intersecting C and satisfying
the condition

(iii) dist(pi, qi) ≤ dist(qi, C), for each 1 ≤ i ≤ k for which c(S) is separated from C by the

line Li ⊃ [pi, pi+1],

is hit by at least one of the points in {p0, p1, ..., pk}.

Proof. First, suppose c(S) ∈ P , and for each 1 ≤ i ≤ k, let Ti := conv({p0, pi, pi+1}). Note
that P = (cid:83)k
i=1 Ti. Therefore there exists i ∈ {1, . . . , k} such that c(S) ∈ Ti, and by the
conditions (i) and (ii) we can apply Lemma 4 to Ti with the result that at least one of
a := p0, b := pi, and c := pi+1 hits S.

Second, assume c(S) /∈ P , and let c ∈ S ∩ C. Since c ∈ P , there exists a side of
the polygon P , say [pi, pi+1] whose line Li separates c(S) and c. Now according to (iii) the
condition of Lemma 5 is satisfied for c, a := pi, b := pi+1, so either pi or pi+1 hits S.

14

c(S)SCp0p1p2p3o4p5p6L13.4 Patch using the triangle inequality

The following lemma strengthens Lemma 5. Together with Lemma 4, it will be used in some
situations to fill in the holes left by the simple reformulations by covers of Proposition 1.

Lemma 6 (Circular patch). Let a, b ∈ R2,
2 − 1 ≤ dist(a, b) ≤ 1, let q be the midpoint
of the segment [a, b], and d := dist(q, a). Then any square of side at least 1 and centre in
B2(q,

√
2
2 − d) contains either a or b (Figure 7 (b)).

√

√

Proof. Assume for a contradiction that there exists a unit square S with centre c(S) in
2 − d), but containing neither a, nor b. Since S contains a disk of radius 1
B2(q,
2 and,
dist(q, c(S)) ≤

2 , we have q ∈ S and so S ∩ [a, b] ̸= ∅.

2 − d ≤ 1

√

2

2

Let L be the line containing [a, b] and let c be a vertex of S separated from c(S) by

L. By Lemma 5 (Thales’ theorem), dist(q, c) < dist(q, a) = d.

Now consider the triangle defined by c(S), q and c (Figure 7(a)). By the triangle

inequality, we have

√
2
2

≤ dist(c(S), c) ≤ dist(c(S), q) + dist(q, c) <

(cid:32) √

2
2

(cid:33)

− d

+ d =

√

2
2

.

This contradiction concludes the proof of the lemma.

Figure 7: Figure (a) illustrates the setup of Lemma 6, while the small (blue) disk of Figure
(b) shows the provided “patch.”

4 Deducing the new bounds for squares

In this section, we prove the main results of the paper: In Section 4.1, we prove the upper
bounds for the τ /ν ratio of unit squares and squares of different sizes (Theorem 1). This is
the most technical part of the paper, and it requires the tools developed in Sections 2 and 3.
In Section 4.2, we provide examples showing the lower bounds for the τ /ν ratio (Theorem
2). Finally, in Section 4.3, we prove the upper bounds for the chromatic number of squares
(Theorem 3): the proof for unit squares uses Lemma 1, while the one for squares is inspired
by an averaging argument used for instance in [2] and [5].

15

c(S)Saba′b′cqLB2(q,√22−d)bB2(a,12)B2(b,12)aB2(q,√22−d)(a)(b)q4.1 Hitting squares

In this section, we first prove the promised upper bounds on the hitting number: Lemma 1
leading to Theorem 1.

Proof of the first part of Lemma 1.

Let C be an arbitrary unit square in R2, and suppose that the origin is in c(C) and the
horizontal and vertical axes are parallel to the sides of C. We want to present 10 points and
apply Theorem 6 to show that they hit all possible neighbours of C. For satisfying conditions
(i) and (ii) we first find a set of 9 points on the circle B2(p0, 1) of centre p0 := c(C) and
radius 1. As a first trial, we can choose these to form a regular 9-gon. However, the
relation of a regular 9-gon to C is not regular, so to satisfy condition (iii) for each possible
S ∈ N (C), slight modifications of the 9-gon are necessary. Since the sides of the regular
9-gon P = conv({p1, . . . , p9}) are significantly smaller than 1, we have a margin to move the
vertices of P on the circle B2(p0, 1) while preserving conditions (i) and (ii). We proceed as
follows:

Move two neighbouring vertices closer together when their midpoint q is too close to
C to satisfy (iii) (happening when the closest point of C is a vertex of P ) while move the
two vertices of a side away from one another when the midpoint q of the side is relatively far
from C. The margin is sufficiently large to easily get points satisfying (iii) without worrying
about rounding errors.

Figure 8: A unit square and the 10 points hitting its neighbours. Any unit square of centre p
with dist(p, pi) ≤ 1, i.e., in the light (blue) disks, is hit by pi, for all i ∈ {0, . . . , 9}. Theorem
6 patches the remaining white zones inside P .

The coordinates of the points we found are given in Figure 8. They obviously satisfy
(i), and we can also see without computation that they satisfy (ii): indeed, it is sufficient
to check that the angles between neighbouring vertices of P are not larger than π/3. They
are all smaller than 1 < π/3, the largest of them is the angle p7p0p8 equal to 0.84.

16

p3p2p1p9p8p7p6p5p4p2(cos(0.74),sin(0.74))p1p3p4p5p6p7p8p9(0,0)(cos(1.39),sin(1.39))(cos(2.19),sin(2.19))(cos(2.72),sin(2.72))(cos(−2.72),sin(−2.72))(cos(−2.19),sin(−2.19))(cos(−1.39),sin(−1.39))(cos(−0.74),sin(−0.74))p0(1,0)p0:=c(C)In Figure 9, we verify (iii): for all i ∈ {1, ..., 9}, dist(pi, qi) < dist(C, qi) (table of the
figure), or, equivalently, B2(qi, dist(pi, qi)) ∩ C = ∅ (drawing of the figure), where qi is the
midpoint of the segment [pi, pi+1] (or [p9, p1], if i = 9).

Figure 9: Checking condition (iii) for 1 ≤ i ≤ 9. The values in the table are rounded to
three decimals.

Hence, by Theorem 6, for any possible unit square S intersecting C, we get that S

is hit by at least one of the points in {p0, p1,. . . , p9}.

Proof of the second part of Lemma 1.

Suppose the squares of the family C (consisting of unit squares) are given in R2, and that
the origin is the left-most centre of a square, denote C such a square, O = c(C). The sides of
C are not necessarily parallel to the axes, causing some complications. The following claim
describes a half-disk containing all centres of possible neighbours of C:
√

Claim 1: All centres of squares in N [C] are in Q := {(x, y) ∈ B2(O,

2) : x ≥ 0}.

Proof of Claim. Let S ∈ N (C) be a square of centre c(S). The distance between the centres
2). Moreover, by the choice
of two intersecting unit squares is at most
of C, c(S) is on the right of the vertical axis, finishing the proof of Claim 1.

2, so c(S) ∈ B2(O,

√

√

Unfortunately, we cannot immediately rely on some half of the 10 hitting points of
the first part of the proof because a square having its centre to the right of the vertical axis
through p0 may have its unique hitting point in the left half-plane.

Let v be the vertex of C in the non-negative quadrant {(x, y) : x > 0, y ≥ 0}. We
call the angle of Ov with the horizontal axis, the angle of C, and denote it ∠(C). The range
of angles to be considered is 0 ≤ ∠(C) < π/2; ∠(C) = π/4 when C is axis-parallel.

We define our hitting set using p0 and five further points on B2(p0, 1), but instead
of p0 = c(C), it is better now to have p0 := (t, 0) for t ∈ R+ chosen later. We fix p0 := (t, 0),
p1 := (t, 1), p3 := (t + 1, 0), p5 := (t, −1), parameterized by t. Figure 10 shows the
introduced hitting points with tentative choices for p2 and p4 for two possible values of t.

17

p0:=c(C)q1q2q3q4q5q6q7q8q9idist(pi,qi)dist(C,qi)1234567890.3190.3290.3620.3690.3620.3690.3190.3290.3890.3990.2620.2710.4090.4120.3890.3990.2620.271The coordinates of p2 and p4 will need a more refined definition depending on the chosen t
and the angle ∠(C).

The neighbours of C having their centre in the region (cid:83)5

2 ) are hit by
{p0, . . . , p5} (Proposition 1). It remains to hit the squares not having their centre in these
disks. We call holes the “triangular regions” of Q \ (cid:83)5
2 ) (see Figure 10). In order
to cover these holes as well, there are two difficulties to overcome:

i=0 B2(pi, 1

i=0 B2(pi, 1

√
2
Figure 10: On the left, the disk B2(O,
2 ) swept by all possible C and the half-disk
Q partitioned in Q≤t and Q>t. In the centre and right, two possible hitting sets with 6
points correspond to different parameter values t. For i ∈ {0, 1, ..., 5}, each light (blue) disk
B2(pi, 1/2) contains all centres of possible unit squares whose inner disk is hit by its centre
pi while the smaller dark (blue) disks represent some of the regions that are patched by
Lemma 6.

First, we have to cover the holes of Q≤t := {(x, y) ∈ Q : 0 ≤ x ≤ t}. The smaller
t is, the smaller the holes of Q≤t are. If t is small enough, these holes can be “patched” by
Lemma 6, as stated in Claim 2. Second, for the squares with centre in Q>t := {(x, y) ∈
Q : x > t}, if the t value is too small, no matter how we fix p2, p3, and p4 on the half-circle
{(x, y) ∈ B2(p0, 1) : x > t} they will not suffice for satisfying condition (iii) of Theorem 6 for
all possible C. We will see, though, that for the maximum value of t computed in Claim 2,
there is a choice of these three points (depending on ∠(C)) such that {p0, p1, ..., p5} hits all
the squares centred in Q>t.

Claim 2: If t =

√

4

4

2−5

, then S ∩ {p0, p1, p5} ̸= ∅ for any unit square S, c(S) ∈ Q≤t.

√

Proof of Claim. Let S ∈ N (C) be a square with centre c(S) and assume for simplicity
that c(S) has a positive vertical coordinate, the other case being symmetric. We show that
{p0, p1} hits S (in the symmetric case, S is hit by {p0, p5}). Since unit squares contain a disk
of radius 1
2 ) ∪ B2(p1, 1
2 ). Apply now Lemma 6 with a = p0,
2−1
b = p1, and consequently d = 1
)
2
contains either p0 or p1, where q is the midpoint of the segment [p0, p1]. Therefore, if the

2 , to conclude that any unit square with centre in B2(q,

2 , this is true if c(S) ∈ B2(p0, 1

√

18

Op0p1p5p2p3p4Op0p1p5p2p3p4p5OB2(O,√22)Q>tQ≤tintersection point of B2(p0, 1
), then {p0, p1}
intersects every square S with c(S) ∈ Q≤t, provided that the following two conditions are
satisfied:

2 ) with the vertical axis is contained in B2(q,

2−1
2

√

t2 +

(cid:32)

1
2

−

(cid:114) 1
4

(cid:33)2

(cid:32) √

− t2

≤

(cid:33)2

2 − 1
2

;

dist(p1, (0,

√

2))2 = t2 + (

√

2 − 1)2 ≤

1
4

.

The maximum of t under the first condition is

, and for this value, the second

condition is also satisfied, finishing the proof of Claim 2.

√

√

4

2−5

4

Once the value of t is fixed, we proceed by defining the remaining points of the

hitting set. This definition will depend on the angle ∠(C):

Claim 3: There exists p2 ∈ B2(0, 1) such that if 0 ≤ ∠(C) ≤ π
4 ,

dist(

p1 + p2
2

, p2) ≤ dist(

p1 + p2
2

, C),

dist(

p3 + p2
2

, p2) ≤ dist(

p3 + p2
2

, C).

Similarly, there exist p′

2, where the same holds if π

4 ≤ ∠(C) < π

2 , replacing p2 by p′
2.

Proof of Claim. To prove the claim, increase ∠(C) from 0 to π
4 , continuously: the union of
the points of the changing squares C is denoted by C1 (Figure 11(a)); C1 is a well-defined
closed set. Note also that moving the candidate for p2 from p3 to p1 on B2(p0, 1), the
segment [p2, p3] increases, and [p1, p2] decreases. The two disks having these segments as
diameters – denote these open disks by D23, D12 – also increase and decrease respectively.

Figure 11: Representation of the sets C1 and C2.

The assertion of Claim 3 for squares of ∠(C) ≤ π

4 is then clearly equivalent to the

following:

There exists a point p2 for which both D23 and D12 are disjoint from C1.

19

p3p3p′2p2p0p0p1p1C1C2c(C)c(C)(a)(b)D12D23D12′D2′3Indeed, then

dist(

dist(

p1 + p2
2
p2 + p3
2

, p2) ≤ dist(

, p2) ≤ dist(

p1 + p2
2
p2 + p3
2

, C1) ≤ dist(

, C1) ≤ dist(

p1 + p2
2
p2 + p3
2

, C),

, C).

Similarly, increasing ∠(C) from π

With the t value provided by Claim 2, p2 := (t+cos(0.82), sin(0.82)) verifies these properties.
2 ” actually
2 := (t + cos(0.92), sin(0.92)),
2] are both disjoint of C2, finishing the proof

means ∠(C) = 0 with our formal definition (Figure 11(b)). If p′
the open disks with diameters [p′
of Claim 3.

2 C “sweeps” C2, where “∠(C) = π

2, p3] and [p1, p′

4 to π

Now, we can define the two sets hitting the neighbours of C according to ∠(C). Recall
2−5

that we fixed p1 := (t, 1), p5 := (t, −1), p0 := (t, 0), p3 := (t + 1, 0), where t =
and we defined p2 and p′
the possibilities for C. Denote p4 the reflection of p2 to the horizontal axis, and p′
reflection of p′
0 ≤ ∠(C) ≤ π

,
2 to satisfy Claim 3 under two different conditions that cover all
4 the
4, p5} if

2. We show that all neighbours of C are hit by H1 := {p0, p1, p2, p3, p′
4 , and by H2 := {p0, p1, p′

4 ≤ ∠(C) < π
2 :

2, p3, p4, p5} if π

√

√

4

4

If S ∈ N (C), then by Claim 1, c(S) ∈ Q. If furthermore c(S) ∈ Q≤t, then we get
from Claim 2 that already the 3-element subset {p0, p1, p5} is hitting. Otherwise c(S) ∈ Q>t.
We partition C into C≤t := {(x, y) ∈ C : x ≤ t} and C>t := {(x, y) ∈ C : x > t}. In Claim 4,
we consider the case S ∩ C>t ̸= ∅, and in Claim 5, the alternative case S ∩ C ⊆ C≤t. This
will conclude the proof of the lemma.

Claim 4: If a unit square S ∈ N (C) satisfies c(S) ∈ Q>t and S ∩ Ct ̸= ∅, then S is hit by
H1 if 0 ≤ ∠(C) ≤ π

4 , and by H2 if π

4 ≤ ∠(C) < π
2 .

Proof of Claim. We assume 0 ≤ ∠(C) ≤ π
2 is the same
by symmetry. We define P1 := conv(H1), a hexagon with the peculiarity that two sides are
collinear since p0 is contained in [p1, p5], and apply Theorem 6 considering P = P1, p0 = p0,
and C = C>t. Observe that p0 plays the double role of corner of P1 and “centre” in condition
(i). Clearly, C>t ⊆ P1 and conditions (i) and (ii) are satisfied. We continue by checking the
other conditions in (iii):

4 , since the case with π

4 ≤ ∠(C) < π

Note that c(S) is on the same side of the line L5 = L0 containing [p5, p0], and [p0, p1].
Therefore, looking at the additional assertion of Theorem 6 we need to check (iii) only for
the indices in I := {1, 2, 3, 4}. Since 0 ≤ ∠(C) ≤ π
4 , Claim 3 makes sure that (iii) holds
for i = 1, and i = 2. However, the angle of the vertex of C which is in the quadrant
{(x, y) : x > 0, y ≤ 0} is |∠(C) − π
4 , and by symmetry this luckily means that (iii)
holds for i = 3 and i = 4. So it holds for all i ∈ I, and therefore the assertion of Theorem 6
can be applied, that is, S is hit by H1 = {p0, p1, p2, p3, p′

4, p5} and the claim is proved.

2 | ≥ π

Claim 5: If a unit square S ∈ N (C) satisfies c(S) ∈ Q>t and S ∩ C ⊆ C≤t, then S is hit
4 ≤ ∠(C) < π
by H1 if 0 ≤ ∠(C) ≤ π
2 .

4 , and by H2 if π

20

Proof of Claim. Let S ∈ N (C) be a square satisfying the hypothesis of the statement. First,
if S intersect any of the segments [a, b] for a, b two consecutive points in (p1, p2, p3, p′
4, p5) if
0 ≤ ∠(C) ≤ π
4 , or in (p1, p′
2 , then we can apply Lemma 5 and,
since we verified already in Claim 4 that

2, p3, p4, p5) if π

4 ≤ ∠(C) < π

dist(

a + b
2

, a) ≤ dist(

a + b
2

, C),

we may conclude that S is hit by H1 or H2, depending on ∠(C). The same conclusion can
be drawn if c(S) is contained in B2(p0, 1
2 ) ∪ B2(p5, 1

2 ).
Otherwise, assume that S ∩ conv({p1, p2, p3, p′
p4, p5}) = ∅, depending on ∠(C), and c(S) ̸∈ B2(p0, 1
S ∩C ⊆ C≤t closest to c(S). In this case, we show that dist(c, c(S)) >
this contradicts that S is a unit square.

4, p5}) = ∅, or S ∩ conv({p1, p′
2 ) ∪ B2(p5, 1

2, p3,
2 ). Let c be the point of
√
2
2 . Since c, c(S) ∈ S,

Consider the segment [c(S), c] ⊆ S. It intersects the vertical line lt := {(x, y) : x = t}
because lt separates the points c and c(S). Moreover, due to the fact that S does not
intersect the polygon conv({p1, p2, p3, p′
2, p3, p4, p5})
if π
2 , this intersection is either above p1 or below p5. We can assume that it
crosses lt above p1 (the other case is symmetric). Under this assumption, c(S) has a vertical
coordinate larger than 1 and so the horizontal line h := {(x, y) : y = 1} separates c and
c(S). We denote by q the intersection point between [c(S), c] and h (Figure 12).

4, p5}) if 0 ≤ ∠(C) ≤ π

4 , or conv({p1, p′

4 ≤ ∠(C) < π

Figure 12: Representation of the centre of a square that is not hit by any point in H1.

Now, it is easy to see that, dist(c(S), q) > dist(c(S), p1) > 1

inequality comes from the assumption c(S) ̸∈ B2(p1, 1
√
2
2 ) lies below the horizontal line {(x, y) : y =
q ∈ h and c ∈ C ⊂ B2(O,

2 ). Moreover, dist(q, c) ≥ 1 −

2 where the second
√
2
2 since

√
2
2 }. Finally,
√
2
2

.

√

2
2

>

dist(c(S), c) = dist(c(S), q) + dist(q, c) >

1
2

+ 1 −

21

p5ltOcc(S)p1qhProof of Theorem 1.

Let S be a square minimizing l(S′), S′ ∈ S, and for the simplicity of the notations, choose
l(S′) = 1 to be of unit length.

Now for each square Q ∈ N (S), fix a point p ∈ Q ∩ S and let Q′ be a unit square
containing p and completely contained in Q (see Figure 13), and let N ′ := {Q′ : Q ∈ N (S)}.
We say that Q and Q′ correspond to one another. Clearly, each Q′ ∈ N ′ still intersects S,
and for each point hitting a subset of N ′, the same point hits all the corresponding sets in
N (S) (local homothety, like in the proof of Theorems 4 and 5).

Since {S} ∪ N ′ contains only unit squares, by Lemma 1 τ (N [S]) ≤ τ (N ′) ≤ 10.
Since we can iterate this procedure to any subfamily of S, we proved that S is hitting-10-
degenerate, and Lemma 2 concludes the proof of the first statement of Theorem 1.

Figure 13: Transformation of the squares in N (S).

The proof of the second statement is analogous and even simpler since now we
directly have only unit squares, so by the second part of Lemma 1, there exists a square S
with the property τ (N [S]) ≤ 6. Therefore, S is now hitting-6-degenerate, and we conclude
by Lemma 2 again.

4.2 Lower bound for hitting

We continue now with the proof of the lower bound stated in Theorem 2:

Proof of Theorem 2. The proof describes a family of unit squares with ν = 1 and τ = 3 and
one of squares of arbitrary sides with ν = 1 and τ = 4. The constructions borrow ideas
of [4] for unit disks or [8] for translations of a triangle.

Start by Figure 14 (a), and note that the three squares of the figure can be hit by
two points only if one of these points is a vertex of the triangle formed by one side of each.

Add now a small shift of each of the two squares at each vertex as (b) shows for one
of the three vertices. Six squares are added in this way, altogether, we mean a family of nine
squares in the example (b). We have τ = 3 for this family, since deleting any vertex of the
triangle (as proved to be necessary) we need two more vertices.

The same holds for the six squares of two different sizes with ν = 1 of (c), so we have

22

SpQQ(cid:48)Figure 14: Pairwise intersecting squares, i.e., ν = 1, and τ = 2 (a), τ = 3 (b), (c).

τ = 3 for the same reason, and we use this to continue the construction with more squares
for having τ = 4 while keeping ν = 1.

Figure 15: 13 pairwise intersecting squares with ν = 1, and τ = 4.

To this end, Figure 15 adds three more layers to Figure 14 (c). Figure 15 (a) contains
Figure 14(a), but each of the three squares of the latter is completed to a chain of 3 squares
containing one another. From the largest to the smallest, we refer to these squares as the
pink, red, and orange square. Each colour forms a triangle, and the six squares belonging to
any pair of colours form a drawing “isomorphic” to Figure 14(c). (Mainly: the intersections
of different pairs of squares of the same colour are disjoint from one another.) Therefore,
the 6 squares of any two colours cannot be hit by less than 3 points. It follows that none of
the intersection points of the largest pink squares can be in a hitting set of size three since
it does not hit any smaller (red or orange) square. Therefore a hitting set of size three must
contain one point of each pink square.

Now add three smaller squares that will be referred to as the green squares, touching
each of the three pink squares at a point, one of them in the midpoint of a side. A green
square intersecting the pink squares in {a1, b1, c1} is drawn on Figure 15 (b). The other
two are symmetric and intersect the pink squares in {a2, b2, c2} and {a3, b3, c3}, respectively.
Since we also have to hit these green squares, from the conclusion of the previous paragraph,
we get that the only hitting sets of size 3 are {a1, b2, c3} and the six different symmetric
versions of it.

Finally, we have obtained three squares of each of the four colours, and we proceed
by adding a thirteenth square that intersects the pink squares at points {a′, b′, c′}, as shown
in Figure 15 (c). These three points can be chosen to be distinct from a1, b1, c1, a2, b2, c2,
a3, b3, and c3. Thus, the last added square intersects all the previous ones, but it is not hit

23

(a)(b)(c)c3b2c2b3c1(a)(b)(c)b1a1a2a3a(cid:48)b(cid:48)c(cid:48)by any of the six hitting sets described before, obliging a fourth point for the hitting set.

Taking disjoint copies of the 13 squares of Figure 15, and of the 9 of Figure 14 (b),

we immediately obtain the following result:

Corollary 3. There exists families of squares with arbitrarily large values of ν such that
τ = 4ν, and also of squares of equal size such that τ = 3ν.

4.3 Colouring squares

In this section, we colour families of squares to bound their chromatic number for a proof
of Theorem 3. The framework we use is a well-known averaging argument (see [2, 5]), which
calls for the simple statement of Lemma 7. Our proof of this lemma turned out to require
more effort than one could guess at first sight:

Let R and S be two squares in the plane, we say that R and S are crossing if R ∩ S

is non-empty and does not contain any of the eight vertices of the two squares.

Lemma 7. Given two crossing squares, each of them contains the centre of the other.

Proof. Let R and S be two crossing squares, p ∈ R ∩ S, and suppose for a contradiction
that c(S) /∈ R. Then the segment [p, c(S)] crosses the boundary of R in a side of R, let
[u, v] be this side, where u and v are vertices of R, and L the line that contains [u, v]. Since
S contains neither u nor v, L ∩ S is a non-empty subsegment of the open interval (u, v),
denote its endpoints by u′ and v′. We distinguish two cases:

Figure 16: The two kinds of crossing intersections.

Case a: The segment [u′, v′] joins two intersecting sides of S (Figure 16(a)).

Then the intersection of S with the half-plane limited by L and not containing c(S)
is a right-angled triangle u′v′w, where w is a vertex of S. So w is separated from c(S) by
L, that is, w is on the same side of L as R.

Now by the only if part of Proposition 3 applied to a = u, b = v, and c = w, w lies
in the open half-disk with diameter [u, v]. However, this half-disk is fully contained in R,
and contains the vertex w of S, contradicting that R and S are crossing.

Case b: The segment [u′, v′] joins two parallel sides of S (Figure 16(b)).

24

uuvvwu(cid:48)v(cid:48)u(cid:48)v(cid:48)c(S)c(S)RR(a)(b)w(cid:48)t(cid:48)LLThen L separates c(S) and two vertices t′ and w′ of S. Assume that t′ lies on the
same side of S as u′, and w′ on the same side as v′. Both t′ and w′ are in the same half-plane
bounded by L, as R, and also in the same half-plane as R, bounded by the line through the
side of R parallel to L, since otherwise dist(u′, t′) ≥ l(R) or dist(v′, w′) ≥ l(R) respectively,
contradicting l(S) ≤ dist(u′, v′) < l(R).

Furthermore, at least one of two vertices t′ and w′ of S must also be in the intersection
of the half-spaces limited by the two parallel sides of R perpendicular to L, containing R.
Then t′ or w′ is in R, contradicting that R and S are crossing. Indeed, if t′ and w′ are
in different half-spaces not containing R then dist(t′, w′) = l(S) > l(R), which is the same
contradiction again; or if they are in the same half-space not containing R then either
dist(u′, t′) or dist(v′, w′) would be strictly larger than dist(u′, v′) ≥ l(S).

Proof of Theorem 3

To prove the first part of Theorem 3, we adapt the averaging argument used by Asplund
and Grünbaum in [2], exhibited in an elegant way by Chalermsook and Walczak [5, Lemma
3].

Let S be a family of squares, G := G(S) the intersection graph of S, n := |S|. Each
point of a square can be contained in at most ∆(S) − 1 other squares with some strict
inequalities at the borders (for example, the left-most point that is a vertex of a square
cannot be contained in any other square).

For each square R ∈ S and R′ ∈ N (R), counting twice the pairs (v, R′), if v is a
vertex of R and v ∈ R′ and only once if v is the centre of R and v ∈ R′, we get at most
(2 × 4 + 1) times the maximum degree of these vertices minus one, for each square. Adding
these numbers for all squares, the sum we get is strictly less than 9n(∆(S) − 1).

This sum counts each edge of G at least twice because if two squares have a vertex-
intersection, then there exists a pair (v, R), such that v is a vertex of one of them, R is the
other and v ∈ R, and this pair is counted twice; if they have a crossing intersection, then by
Lemma 7 applied twice, both centres are in the intersection. Hence, 2|E(G)| < 9n(∆(S)−1),
and therefore the minimum degree of G is strictly less than 9(∆(S) − 1). Applying this to
any subgraph, we get that G is k-degenerate with k < 9(∆(S) − 1), and hence 9(∆(S) − 1)-
colourable.

To prove the second part of the theorem, let now S be a family of unit squares.
Lemma 1 implies that S is hitting-6-degenerate. Then, by Lemma 3, S is also (6∆(S) − 1)-
degenerate and therefore 6∆(S)-colourable.

Note that both parts of Theorem 3 rely on degeneracy, applying two distinct methods
though: an averaging argument for squares of different sizes and Lemma 1 specifically for
unit squares. While both techniques are applicable to both cases, the results differ in
efficiency. For arbitrary squares, Lemma 1 yields an upper bound of 10∆, whereas the
averaging argument provides the tighter bound 9(∆ − 1) of Theorem 3. However, when
considering unit squares, the averaging argument does not straightforwardly improve the

25

9(∆ − 1) bound, whereas the more sophisticated Lemma 1 yields the better bound 6∆ with
the exception of ∆ = 2, when clearly 9(∆ − 1) < 6∆.

5 Conclusion and open questions

In this paper, we provided the best linear bounds we could for the hitting number of squares
in the plane: Theorem 1 provides the upper bounds, and Theorem 2 the lower bounds, both
proved in Section 4. These establish the worst τ /ν ratio in the interval [3, 6] for unit squares
and in [4, 10] for squares in general. Finding the right value remains elusive even for the
special case when ν = 1, meaning that the squares are pairwise intersecting. Grünbaum [14]
mentioned that any family of pairwise intersecting translates and rotations of a fixed convex
set can be hit by a constant number of points, depending on the convex object. For the
particular case of unit disks, H. Hadwiger and H. Debrunner [15] provided an exact result
showing that any family of pairwise intersecting unit disks can be hit by 3 points and that
3 points are sometimes necessary. For unit squares 3 points are necessary by Theorem 2,
and it is not difficult to show that 4 points are sufficient. We wonder if this bound can be
improved or if a better lower bound can be achieved. We ask the following questions:

Question 1. Can every family of pairwise intersecting unit squares be hit by 3 points?

Question 2. Is there a family of squares with τ

ν > 4?

We also wonder whether the best examples for Question 2 can be realized with ∆ = 2.

The bounds for the hitting number we established are based on hitting-degeneracy
(Lemma 2). The greedy local induction of this approach is almost tight: Figure 17 presents
a unit square S with τ (N [S]) = 7; moreover, removing the two squares strictly to the left
of c(S) we have an example of a unit square with left-most centre and τ (N [S]) = 5, which
shows the limits of this method. Nevertheless, there is no reason to think the bounds of
Theorem 1 cannot be improved with other methods.

Figure 17: A unit square with seven pairwise disjoint neighbours.

26

We would also like to draw attention to two open problems on axis-parallel squares.
We pointed out in Table 1 that τ ≤ 4ν − 3 for axis-parallel squares and τ ≤ 2ν − 1 for axis-
parallel unit squares. It is not known whether these two bounds are tight, and, surprisingly,
the best-known lower bound is only 3/2, simply achievable with a cycle of five unit squares.
We ask a question analogous to Question 2 in the axis-parallel case:
Question 3. Is there a family of axis-parallel squares with τ

ν > 3
2 ?

In 1965, Wegner [23] conjectured that for any family of axis-parallel rectangles,
τ ≤ 2ν −1. Almost sixty years later, this conjecture is still open. Actually, no constant upper
bound for the τ /ν ratio for axis-parallel rectangles is known. Having only the weaker bound
τ ≤ 4ν − 3 for axis-parallel squares, Wegner’s conjecture remains a frustrating challenge
even in this special case.

If the Helly property does not hold, the chromatic number is often easier to upper
bound by the maximum degree, not necessarily equal to the clique number. Nevertheless,
the obvious inequality ∆ ≤ ω immediately implies a bound in terms of ω as well. We wonder
how big the gap between ω and ∆ can be for squares:

Question 4. What is the maximum size of a family of pairwise intersecting squares (or unit
squares) with ∆ = 2?

For squares, analogous questions to Question 3 can be asked about the chromatic
number as well. In the literature, we could not find any lower bound on the ratio χ
ν better
than 3
2 neither for translations and homotheties of a fixed convex set nor for their trans-
lates and rotations. Families of axis-parallel squares and (not necessarily axis-parallel) unit
squares are two particular examples of these families. We ask the following questions:

Question 5. Is there a family of axis-parallel squares, or not necessarily axis-parallel unit
squares, with χ

ω > 3
2 ?

Finding the right value of sup χ

ω for squares is also an open problem in the particular
case ω = 2, that is, when the intersection graph is triangle-free. Perepelitsa [21, Corollary
8] showed that any triangle-free family of axis-parallel squares is 3-colourable. Her result
follows directly from Grötzsch’s theorem [13], once observed that the intersection graph of
such a family is planar. Allowing the squares to rotate, this property is lost, but this change
may not significantly impact the chromatic number. A method similar to the one used by
Perepelitsa [21] can be used to prove 6-colourability.

Question 6. What is the smallest k such that any triangle-free family of squares is k-
colourable?

“Triangle-free” means ω ≤ 2 here. According to Theorem 3, the answer to Question 6

is between 3 and 9 under the weaker condition ∆ ≤ 2.

Acknowledgements

Marco Caoduro was supported by a Natural Sciences and Engineering Research Council of
Canada Discovery Grant [RGPIN-2021-02475].

27

References

[1] R. Ahlswede and I. Karapetyan. Intersecting graphs of rectangles and segments. LNCS,

4123:1064–1065, 2006.

[2] E. Asplund and B. Grünbaum. On a coloring problem. Math. Scand., 8:181–188, 1960.

[3] T. Biedl and G. Kant. A better heuristic for orthogonal graph drawings. Computational

Geometry, 9(3):159–180, 1998.

[4] A. Biniaz, P. Bose, and Y. Wang. Simple linear time algorithms for piercing pairwise
intersecting disks. In Proceedings of the 33rd Canadian Conference on Computational
Geometry, CCCG 2021, pages 228–236, 2021.

[5] P. Chalermsook and B. Walczak. Coloring and maximum weight independent set of
rectangles, pages 860–868. Society for Industrial and Applied Mathematics, 2021.

[6] T. M. Chan. Polynomial-time approximation schemes for packing and piercing fat

objects. Journal of Algorithms, 46(2):178–189, 2003.

[7] B. N. Clark, C. J. Colbourn, and D. S. Johnson. Unit disk graphs. Discrete Mathematics,

86(1):165–177, 1990.

[8] A. Dumitrescu and M. Jiang. Piercing translates and homothets of a convex body.

Algorithmica, 61:94–115, 2011.

[9] A. Dumitrescu and M. Jiang. Coloring translates and homothets of a convex body.

Contributions to Algebra and Geometry, 53:365–377, 2012.

[10] R. J. Fowler, M. S. Paterson, and S. L. Tanimoto. Optimal packing and covering in the

plane are NP-complete. Information Processing Letters, 12:133–137, 1981.

[11] M.R. Garey, D.S. Johnson, and L. Stockmeyer. Some simplified NP-complete graph

problems. Theoretical Computer Science, 1(3):237–267, 1976.

[12] A. Gräf, M. Stumpf, and G. Weißenfels. On coloring unit disk graphs. Algorithmica,

20:277–293, 1998.

[13] H Grötzsch. Ein Dreifarbensatz für dreikreisfreie Netze auf der Kugel, Wiss. Z. Martin-

Luther-Universität, Halle-Wittenberg, Math. Nat. Reihe, 8:109–120, 1959.

[14] B. Grünbaum. On intersections of similar sets. Portugaliae mathematica, 18(3):155–164,

1959.

[15] H. Hadwiger and H. Debrunner. Ausgewählte Einzelprobleme der kombinatorischen

Geometrie in der Ebene. Enseignement Math, 2:56–89, 1955.

[16] H. Imai and T. Asano. Finding the connected components and a maximum clique of an
intersection graph of rectangles in the plane. Journal of Algorithms, 4:310–323, 1981.

28

[17] S. J. Kim, A. Kostochka, and K. Nakprasit. On the chromatic number of intersection
graphs of convex sets in the plane. The Electronic Journal of Combinatorics, 11, 2004.

[18] S. J. Kim, K. Nakprasit, M. J. Pelsmajer, and J. Skokan. Transversal numbers of

translates of a convex body. Discrete Mathematics, 306(18):2166 – 2173, 2006.

[19] K.J. Nurmela and P.R.J. Östergård. Covering a square with up to 30 equal circles.

WorkingPaper HUT-TCS-A62, Helsinki University of Technology, 2000.

[20] J. Pach. Decomposition of multiple packing and covering. 2. Kolloquium über Diskrete

Geometrie, pages 169–178, 1980.

[21] I.G. Perepelitsa. Bounds on the chromatic number of intersection graphs of sets in the

plane. Discrete Mathematics, 262:221 – 227, 2003.

[22] L.G. Valiant. Universality considerations in VLSI circuits.

IEEE Transactions on

Computers, C-30(2):135–140, 1981.

[23] G. Wegner. Über eine kombinatorisch-geometrische Frage von Hadwiger und Debrun-

ner. Israel J. Math, 3:187–198, 1965.

A NP-hardness for axis-parallel unit squares

The main problems we study in this paper are already NP-hard for the simplest objects, axis-
parallel unit squares, justifying approximation algorithms and bounds between packing and
hitting numbers or clique and the chromatic numbers instead of computing these numbers
exactly or proving min-max theorems. We started the introduction with pointers to most of
the hardness results, but we did not find any reference for the NP-hardness of the colouring
problems or the maximum independent set problem of unit squares. This Appendix fills this
gap.

We summarize the missing statements in the following theorem. The proofs are easy
using the ideas for unit disk graphs of Clark, Colburn, and Johnson [7] further developed
by Gräf, Stumpf and Weißenfels [12], because the graphs used by these articles can be
represented as intersection graphs of axis-parallel unit squares as well.

Theorem 7. The k-colourability of axis-parallel unit squares is NP-complete for any fixed
k ∈ N, k ≥ 3, and so is the existence of an independent set of unit squares larger than a
given size.

Proof. Let k ∈ N, k ≥ 3 and let us reduce first the k-colourability of a graph – a well-known
NP-complete problem [11] – to the k-colourability of axis-parallel unit squares. The main
gadget of the reduction is a particular family of squares used to replace the edges of the
graph. We introduce it and then overview its application.

Note that the “chain of diamonds" of the graph in Figure 18 (a) forces the endpoints
x and y to have the same colour in any 3-colouration. This graph can be straightforwardly

29

realized with unit squares forming a horizontal or vertical “strip” as long as necessary (Fig-
ure 18 (b)). Furthermore, in Figure 18 (a) each thick (red) edge in the middle can be
replaced by a (k − 1)-clique which is the intersection graph of Figure 18 (b) with the dark
(red) squares in the middle replaced by k − 1 squares with the same intersections and inter-
secting one another (it can be k − 1 copies of the same square like on the right of Figure 19).
We will call this set of squares a k-chain of unit squares.

Furthermore, for an edge of a graph drawn in the plane alternating between horizon-
tal and vertical segments, not crossing any other edge, each horizontal and vertical segment
can be replaced by a k-chain, and the endpoint of a chain can be identified by the starting
point of the next one as in Figure 19. The obtained graph is still an k-chain. Clearly, the
endpoints x and y of a k-chain have the same colour in any k-colouration.

Figure 18: (a) A 3-chain forcing vertices x and y to have the same colour in every 3-coloration
(b) Unit square representation of a 3-chain.

Add now a point z to this figure, and join it only to y: we know then that x and
z must have different colours in any colouration (see Figure 19). A family of unit squares
whose intersection graph is a k-chain with such an additional vertex and edge will be called
an k-chain-edge of unit squares.

Figure 19: From left to right: an edge of G, a k-chain-edge, and a k-chain-edge of unit
squares.

Having noticed the realizability of k-chains as intersection graphs of unit squares, we

can now mimic the proof of [7] or, more generally, of [12] to finish the proof:

In the same way as [7] does for unit disks, the 3-colourability of a planar graph with
maximum degree 3 – already an NP-hard problem [11] – can be reduced to the 3-colourability
of unit square graphs in polynomial time, using 3-chains of unit squares. Indeed, according
to [22], each planar graph G of maximum degree three can be drawn in the plane without
crossing edges in such a way that each edge consists of at most four horizontal or vertical

30

xyXY(a)(b)xzk−1XYZxyzsequences. This embedding can be realized in polynomial time [3]. It follows then easily from
the above observations that each edge can be replaced by a 3-chain-edge of unit squares,
and the 3-colourability of the constructed family of unit squares is equivalent to that of G.

Now, for arbitrary k ≥ 3 (also allowing equality, i.e., the k = 3 case is reconsidered,
the above discussion serves merely the pedagogical reasons for introducing some of the ideas
and the main square-specific gadgets) and graph G, we reduce the colouring problem of G
to the colouring problem of unit squares.

For this, the essential part of the work has already been done by Gräf, Stumpf and
Weißenfels [12]: they show that a graph G′ = (V ′E′) drawn in the plane can be constructed
from G in polynomial time (we will use it as a black box, but for an approximate illustration
see Figure 20), where V ′ is partitioned into a path Pv for each v ∈ V (G), a set T of degree
two vertices, and sets Vu indexed by the elements u ∈ U of a set U verifying the following
properties:

(i) Contracting Gu (Figure 20 left) for each u ∈ U , the new vertices, denote them xu
(u ∈ U ) are of degree 4, and all the edges of the obtained graph are horizontal or
vertical. Denote by H the resulting graph drawn in the plane (Figure 20 right).

(ii) If in H all edges of the path Pv (v ∈ V (G)) are contracted for each v ∈ V (G),
furthermore, splitting off the two edges incident to t ∈ T , that is, replacing them by
one edge between the two endpoints different from v, and doing the same with the
opposite edges incident with xu (u ∈ U ) in the planar drawing of H (and therewith
losing planarity), we get back G.

Each edge e = xz ∈ E(G) (x, y ∈ V (G)) corresponds to a path between x and z in H
whose edges are a set Fe of edges in G′.

(iii) Replacing each horizontal and each vertical line of G′ by a k-chain, but for one edge
in each Fe a k-chain-edge, the constructed graph G′′ is k-colourable if and only if G is
k-colourable.

Figure 20: On the left, the graph isomorphic to all the graphs Gu (u ∈ U ), the (red) disks
represent k − 2 cliques. On the right, a representation of a portion of H. The vertices
x, y ∈ V (G) are replaced with two paths Px, Py ⊂ V ′ of size dG(x) and dG(y), respectively.

Figure 20 illustrates the graphs that make possible to prove these properties.

31

GuPxPyuu′tk−2Then [12] continue by realizing k-chains and k-chain-edges as intersection graphs of
unit disks, and substitute these for the edges of H. By (i) all edges of H are horizontal or
vertical, and this ensures that the substitution can be done.

Now, k-chains and k-chain-edges of unit squares replace unit disks (Figure 18); the
endpoint of a chain can be identified by the starting point of the next one, again as in Fig-
ure 19, and clearly, this does not take more computational time than the disk version. Thus,
a unit square graph is constructed in polynomial time, whose k-colourability is equivalent
to that of G.

32

