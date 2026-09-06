                                                  A 64-Rectangle Counterexample to Wegner’s Conjecture
                                                                 and LP Gaps up to 5/2

                                                                                      Aranya Kumar Bal
                                                                               Indian Statistical Institute, Kolkata



                                                                                            Abstract
                                                    Since its formulation in 1965, Wegner’s conjecture has been one of the central open problems
                                                in geometric transversal theory, profoundly influencing research on geometric intersection graphs,
                                                packing and piercing, and approximation algorithms. The recent breakthrough of Ajwani, Gajjala,
arXiv:2607.11318v2 [math.CO] 14 Jul 2026




                                                Raman, and Ray settled the conjecture in the negative by constructing the first counterexample,
                                                consisting of 2196 · 89 axis-parallel rectangles using a package-and-port construction alongside a
                                                computer-assisted proof, and also established an integrality gap of 17891/8064 ≈ 2.21 for the
                                                standard LP relaxation of the Maximum Independent Set of Rectangles problem.
                                                    In this paper, we substantially strengthen this breakthrough by giving an explicit and con-
                                                ceptually simple counterexample using only 64 rectangles. Whereas the previous counterexample
                                                relied on a large construction with a computer-assisted proof, ours is derived from a small geo-
                                                metric gadget with a recursive composition principle alongside a hand-checkable proof, making
                                                the obstruction to Wegner’s conjecture transparent.
                                                    Our construction starts from an eight-rectangle gadget whose independent sets admit an
                                                injective assignment to four ordered labels. Combining four horizontal and four vertical copies
                                                of this gadget yields the 64-rectangle counterexample. Iterating the same horizontal-vertical
                                                                                                                     r
                                                construction produces a recursive family Pr satisfying ν(Pr ) = 42 . Already at the second level,
                                                the standard clique relaxation has value exceeding 2ν(P2 ), while at the third level it achieves
                                                an integrality gap of 73/32, improving on the previous best value of 17891/8064. We further
                                                construct explicit recursive fractional solutions whose values converge to (5/2)ν(Pr ), together
                                                with piercing sets of size exactly (5/2)ν(Pr ) at every level. Consequently, both the clique-LP gap
                                                and the packing-piercing ratio of the recursive family converge to 5/2, yielding rectangle families
                                                with packing-piercing ratios arbitrarily close to 5/2 from below. Finally, by taking disjoint unions
                                                with isolated rectangles, we show that every rational number in [1, 5/2) occurs both as a standard
                                                LP gap for Maximum Independent Set of Rectangles and as a packing-piercing ratio of a suitable
                                                rectangle family.


                                           1    Introduction
                                           Let R be a finite family of closed axis-parallel rectangles in the plane. Write ν(R) for the maximum
                                           size of a pairwise disjoint subfamily and τ (R) for the minimum number of points required to intersect
                                           every rectangle. In 1965, Wegner [Weg65] conjectured that

                                                                                       τ (R) ≤ 2ν(R) − 1.

                                           Over the past six decades, this conjecture has been one of the central open problems in geometric
                                           transversal theory. Beyond its intrinsic appeal, it has profoundly influenced the study of geometric
                                           intersection graphs, rectangle packing and piercing, combinatorial optimization, and approximation
                                           algorithms.

                                                                                                 1
     A considerable body of evidence supported Wegner’s conjecture and suggested that the proposed
bound was essentially best possible. Fon-Der-Flaass and Kostochka [FDFK93] proved that no
universal coefficient below 5/3 is possible, while a construction of Jelínek, reported by Correa,
Feuilloley, Pérez-Lantero, and Soto [CFPLS15], gives τ (R) = 2ν(R) − 4 for every ν(R) ≥ 4. Chen
and Dumitrescu [CD20] further investigated the sharpness of Wegner’s inequality, and Correa et
al. [CFPLS15] studied the special case of diagonal-intersecting rectangles, where the packing-piercing
gap is known to lie between 2 and 4. Together with steadily improving general upper bounds, these
results made the existence of a counterexample appear increasingly unlikely.
     The conjecture was finally settled by Ajwani, Gajjala, Raman, and Ray [AGRR26] in the
negative, who constructed the first counterexample and, in the same work, established an integrality
gap of 17891/8064 > 2.21 for the standard LP relaxation of the Maximum Independent Set of
Rectangles problem. Their construction is both ingenious and highly nontrivial, combining a
recursive package-and-port framework with computational verification via linear programming and
dynamic programming. Inspired by the filter-bed construction of Asplund and Grünbaum [AG60],
it produces a family consisting of 2196 · 89 rectangles. Besides settling a sixty-year-old conjecture,
this breakthrough opened a number of natural questions. Can the failure of Wegner’s conjecture
be witnessed by a substantially smaller explicit construction? Can one replace computational
certification by a direct combinatorial argument? More broadly, can such a construction reveal new
structural insights into rectangle packing, piercing, and LP relaxations?
     In this paper, we answer these questions affirmatively. We present a simple recursive geometric
construction that yields an explicit counterexample using only 64 rectangles, reducing the size
of the first counterexample by several orders of magnitude. More importantly, our construction
replaces computational verification with a direct combinatorial analysis, exposing the underlying
mechanism responsible for the failure of Wegner’s conjecture. This recursive viewpoint also leads to
new structural results on rectangle packing-piercing ratios and LP relaxations that substantially
strengthen the current state of the art. The precise statements of our results are presented in
Section 2.


2    Our contributions
We begin with a conceptually simple counterexample to Wegner’s conjecture. Our construction
is based on an eight-rectangle gadget equipped with four ordered labels, called slots. These slots
regulate how recursive copies interact and provide a direct combinatorial certificate for bounding the
size of independent sets. Combining four horizontal and four vertical copies of the gadget yields an
explicit counterexample with only 64 rectangles.

Theorem 1 (A 64-rectangle counterexample). There is a family R of 64 axis-parallel rectangles
such that
                            ν(R) = 16    and     τ (R) ≥ 32.
Consequently,
                                           τ (R) > 2ν(R) − 1.

    More importantly, the same recursive construction extends to an infinite family of rectangle
systems. Iterating the horizontal–vertical composition produces rectangle families P0 , P1 , P2 , . . .
                      r
satisfying ν(Pr ) = 42 . While only the first nontrivial member P1 is triangle-free, the slot structure
continues to control independent sets at every level. This explicit recursive structure is sufficiently rich
to admit recursive fractional solutions for the standard clique relaxation of Maximum Independent


                                                     2
Set of Rectangles. Already the second level yields a clique-LP value exceeding 2ν(P2 ), while the
third level improves the previous best finite integrality gap.

Theorem 2 (A finite LP gap). For the standard point relaxation, equivalently the clique relaxation,
for Maximum Independent Set of Rectangles,

                                             α∗ (P3 )  73
                                                      ≥ .
                                             ν(P3 )    32

   Beyond improving the best known finite gap, the recursive structure admits a complete asymptotic
analysis. We construct a recursive family of fractional solutions whose values converge to 5/2, together
with explicit piercing sets showing that the same limit is attained by the packing–piercing ratio.

Theorem 3 (The limiting value). For the family Pr constructed in Section 7,

                                       α∗ (Pr )       τ (Pr )  5
                                    lim         = lim         = .
                                   r→∞ ν(Pr )     r→∞ ν(Pr )   2

    Finally, the limiting theorem yields a complete interpolation result. By taking sufficiently many
disjoint copies of a suitable recursive construction and adjoining isolated rectangles, every rational
value below 5/2 can be realized exactly.

Theorem 4 (Interpolation below 5/2). Every rational number t ∈ [1, 5/2) occurs as α∗ (R)/ν(R)
for some finite family R of axis-parallel rectangles. The same is true for the packing–piercing ratio
τ (R)/ν(R).


3    Related work
The quantities ν and τ place Wegner’s conjecture in the classical packing-piercing setting initiated
by Hadwiger and Debrunner [HD57]. The inequality proposed by Wegner [Weg65] is a particularly
sharp form of such a statement for axis-parallel rectangles. Gyárfás and Lehel [GL85] later asked for
a constant bound on τ (R)/ν(R) for rectangle families. Wegner’s conjecture would have answered
this with the asymptotic constant 2.
    The lower-bound side developed more slowly, and for a long time stayed below this threshold.
Fon-Der-Flaass and Kostochka [FDFK93] showed that no universal coefficient below 5/3 can hold.
A construction of Jelínek, reported by Correa, Feuilloley, Pérez-Lantero, and Soto [CFPLS15], gives
τ (R) = 2ν(R) − 4 for every ν(R) ≥ 4, so the leading coefficient 2 would have been sharp if Wegner’s
inequality had held. Ajwani, Gajjala, Raman, and Ray [AGRR26] were the first to cross 2, and their
larger weighted construction also gives the finite standard-LP benchmark 17891/8064 > 2.21. The
recursive family in this paper pushes the lower side further for rectangles: its packing-piercing ratios
and clique-relaxation gaps both tend to 5/2.
    The best general upper bounds for rectangles are much larger. Károlyi [Ká91] proved that a
family of axis-parallel boxes in Rd satisfies an O(ν(log ν)d−1 ) piercing bound; in the plane this
gives O(ν log ν) for rectangles. Correa, Feuilloley, Pérez-Lantero, and Soto [CFPLS15] improved the
rectangle bound to O(ν(log log ν)2 ), using in part small ϵ-net bounds of Aronov, Ezra, and Sharir
[AES10] and the approximation framework of Chalermsook and Chuzhoy [CC09] for maximum
independent set of rectangles. The contrast with higher dimensions is sharp: Tomon [Tom23] proved
that axis-parallel boxes in dimensions d ≥ 3 do not admit any constant bound in terms of ν alone. At
the same time, some structured classes in the plane do have linear behavior: Chudnovsky, Spirkl, and


                                                   3
Zerbib [CSZ17] showed, among other results, that bounded-aspect-ratio rectangles can be pierced by
O(ν) points.
    Two nearby comparisons help locate the obstruction more precisely. On the rectangle side, Correa
et al. [CFPLS15] analyze the case in which all rectangles meet a common diagonal, where the
packing-piercing gap is bounded between 2 and 4. Chen and Dumitrescu [CD20] studied Wegner’s
inequality for axis-parallel rectangles from another direction. These results help explain why the
conjecture was plausible: the obstruction has to be global, and cannot be seen from only a local
rectangle pattern.
    A second comparison comes from axis-parallel segments. Caoduro, Cslovjecsek, Pilipczuk, and
Węgrzycki [CCPW22] proved that every triangle-free intersection graph of n axis-parallel segments
                                                  √
has an independence number at least n/4 + Ω( n), and they gave a matching construction up to
                      √
the constant in the n term. Thus, the triangle-free route has a built-in slack for segments. The
64-rectangle family here reaches the exact n/4 threshold, which is the point at which the same
counting argument disproves Wegner’s rectangle inequality.
    A different connection is algorithmic. Rectangle families are central in approximation algo-
rithms for Maximum Independent Set of Rectangles: Chalermsook and Chuzhoy [CC09] gave an
O(log log n)-approximation framework. Later recursive partitioning methods led to constant-factor
approximations, including the work of Mitchell [Mit22] and the (2 + ϵ)-approximation of Gálvez,
Khan, Mari, Mömke, Reddy, and Wiese [GKM+ 21]. The standard point relaxation for this problem
is equivalent, for rectangle graphs, to the clique relaxation used in this paper.


4    Organization of the paper
Section 5 gives an informal overview of the techniques used in the paper. Section 6 derives the
eight-rectangle configuration from the slot requirements. Section 7 defines the operation that repeats
horizontal and vertical copies, and proves Theorem 1. Sections 8 and 9 develop the fractional
solutions, first through finite weightings on P2 and P3 , and then recursively. Section 10 gives the
matching piercing sets of size (5/2)ν(Pr ). Section 11 proves Theorem 4.


5    Overview of the results
This section sketches the ideas behind the four results, and can be read before the technical sections.
We first collect some of the required notions we will use going forward here, and in the technical
section.
    All rectangles in this paper are closed and axis-parallel. For a finite family R, its intersection
graph G(R) has one vertex for each rectangle and one edge for each intersecting pair. A pairwise
disjoint subfamily of rectangles is exactly an independent set in G(R), so
                                          ν(R) = α(G(R)).
    Axis-parallel rectangles have the Helly property: if every two rectangles in a finite subfamily
intersect, then all rectangles in that subfamily share a common point. Hence a point that pierces
some rectangles corresponds to a clique in G(R), and piercing R is the same as covering the vertices
of G(R) by cliques.
    We will often use the following observation in this informal form. If G(R) is triangle-free, then
no point of the plane lies in three rectangles. Therefore every piercing point meets at most two
rectangles, and τ (R) ≥ |R|/2. If, in addition, ν(R) ≤ |R|/4, then
                                τ (R) ≥ |R|/2 ≥ 2ν(R) > 2ν(R) − 1.

                                                  4
Thus a triangle-free rectangle graph with independence number at most one quarter of its vertices
gives a counterexample to Wegner’s conjecture.
    We also use the standard clique relaxation. For a graph G, let
                                                                               
                               X                  X                            
               α∗ (G) = max           xv : xv ≥ 0,     xv ≤ 1 for every clique K .
                                                                               
                                 v∈V (G)               v∈K

For rectangle graphs this is the same as the point relaxation, since cliques are exactly the subfamilies
pierced by a single point. The integral optimum is α(G) = ν(R). Every piercing set gives a clique
cover, and summing the LP inequalities over the cliques in such a cover gives

                                           α∗ (G(R)) ≤ τ (R).

5.1   A 64-rectangle counterexample (Theorem 1)
We start with a counting strategy, and then realize a small number of rectangles that realize the
strategy. Suppose a triangle-free rectangle family has n rectangles and no independent set larger
than n/4. Then ν ≤ n/4, while triangle-freeness gives τ ≥ n/2, so

                                     τ ≥ n/2 ≥ 2ν > 2ν − 1,

contradicting Wegner’s bound. Everything therefore reduces to building a triangle-free family that
meets the threshold ν ≤ n/4 exactly.
    The construction starts from a base object of eight rectangles (see Figure 3), drawn against four
reference vertical lines and four reference horizontal lines (these lines become the slots of Section 6).
The eight rectangles are arranged so that every independent set among them can be matched
one-to-one to the four vertical reference lines. This matching guarantees that the independence
number of the base object is at four. From one base object we form four horizontal copies and
four vertical copies, positioned by a scaling rule so that a horizontal copy meets a vertical copy
exactly when their reference lines prescribe it. This doubling produces a triangle-free configuration
of 8 · 8 = 64 rectangles and the matching property lifts to an upper bound of 4 × 4 = 16 on the
independence number (see Figure 4). Since 16 = 64/4, the counting argument fires: ν = 16 while
τ ≥ 32, so τ > 2ν − 1 = 31 and Wegner’s conjecture is violated.

5.2   A finite clique-relaxation gap (Theorem 2)
The subsequent results all depend on the following observation. The clique relaxation value sits
between the packing and piercing numbers,

                                      ν(R) ≤ α∗ (R) ≤ τ (R),

because it relaxes the integral packing from below and is bounded above by any clique cover, in
particular by any piercing set.
    The clique relaxation assigns each rectangle a nonnegative weight so that the weights on any
clique, equivalently, any single piercing point, sum to at most one; its value is the total weight.
On a triangle-free family this relaxation is already visible: every clique is a single rectangle or an
intersecting pair, so giving every rectangle weight 1/2 is feasible, with value n/2 = 2ν. In particular
the 64-rectangle example gives ratio exactly 2, and no more. To pass 2, one has to go deeper into
the construction; and in doing so, we will lose this triangle-freeness and thus have to be more clever.


                                                   5
    Repeating the horizontal-vertical doubling yields a family P0 , P1 , P2 , . . . , where P1 is the coun-
terexample above and the packing number ν(Pr ) grows in a controlled way. The point of the doubling
is that feasibility stays local : any clique either lives inside a single copy, or inside one horizontal copy
meeting one vertical copy. So a weighting is feasible as soon as each copy is feasible on its own and,
at every crossing, the combined weight visible through that crossing stays at most one. Designing
weightings that carry high value while keeping this crossing weight small is a small, hand-checkable
balancing problem. Carried out at the third level, it gives

                                              α∗ (P3 )   73
                                                       ≥    ,
                                              ν(P3 )     32

which exceeds the earlier benchmark 17891/8064.

5.3    The limiting ratio 5/2 (Theorem 3)
The finite gaps are the start of a sequence that converges, and the limit is pinned down from both
sides.
    For the lower side, the crossing condition has a clean reusable form: if a weighting keeps the
weight visible through every vertical reference line at most 1/2, then it can be dropped into every
horizontal and every vertical copy at the next level and the crossings stay feasible automatically, since
1/2 + 1/2 = 1. Among these reusable weightings, a recursive scheme builds ones whose normalized
value climbs toward 5/4. Reusing a value-5/4 weighting at the next level then doubles the ratio, so
α∗ (Pr )/ν(Pr ) → 5/2 from below.
    For the upper side, the same reference lines supply piercing sets. Using the grid of reference-line
intersections, one can pierce Pr with (5/2) ν(Pr ) points, built recursively so that every reference line
carries either two or three chosen points, with the extra point on exactly half of the lines in each
direction. This gives τ (Pr ) ≤ (5/2) ν(Pr ). The same piercing sets also explain why 5/4 is the ceiling
for the reusable weightings: their weight can be charged to the (5/2) ν(Pr ) grid points, each of which
absorbs at most 1/2.
    Since ν ≤ α∗ ≤ τ , both ratios are now squeezed between the two bounds, and

                                       α∗ (Pr )       τ (Pr )   5
                                    lim         = lim         = .
                                   r→∞ ν(Pr )     r→∞ ν(Pr )    2

5.4    Interpolation below 5/2 (Theorem 4)
The last result is a tuning argument. A single isolated rectangle has packing, piercing, and relaxation
value all equal to one, so its ratio is exactly 1. When two families are placed far apart in the plane,
all three quantities add, because disjoint packings combine, no point pierces both regions, and the
relaxation splits into independent programs. These two observations let us dial any ratio downward.
     Fix a rational target t ∈ [1, 5/2). By the previous result some member Pr has ratio above t;
write a = ν(Pr ) and b for the relevant value on Pr . Taking M separated copies of Pr and adding N
isolated rectangles produces a family with ratio (M b + N )/(M a + N ). Solving for N gives a positive
rational multiple of M , so choosing M large enough makes N a positive integer and the ratio equal
to t exactly. The endpoint t = 1 is any nonempty family of pairwise disjoint rectangles. Running
the argument once for the relaxation and once for the piercing number realizes every rational in
[1, 5/2) as each of the two ratios.




                                                     6
6    The eight-rectangle base
We now build the eight-vertex graph F underlying the base drawing P0 . For the moment, a slot
is just one of the labels 0, 1, . . . , q − 1. In the rectangle drawing these labels will correspond to
distinguished vertical or horizontal lines.
     The numerical target comes from the first repetition. If the base object has m vertices and q
slots, then later we will take q horizontal copies and q vertical copies, giving 2qm rectangles. The
board used to bound independent sets has only q 2 positions. To make this board one quarter of the
total size, we need q 2 = 2qm/4, or m = 2q.
     Thus we want 2q vertices whose independent sets can be assigned injectively to q allowed slots.
There is also a geometric restriction: vertices sharing a vertical slot must be nonadjacent, or the
first horizontal-vertical arrangement could create a triangle. In formulas, for the first list system we
require
                                 X(u) ∩ X(v) ̸= ∅ =⇒ uv ∈         / E(F ).
Thus only pairs with disjoint lists are eligible to become edges.
    The slots have a fixed order in the eventual drawing. Since a rectangle that contains two
distinguished vertical lines also contains every distinguished vertical line between them, its X-list
must be an interval of slots. The simplest interval family of the right size consists of the singleton
intervals, the adjacent two-slot intervals, and the full interval. Its size is q + (q − 1) + 1 = 2q, exactly
the target above. The cases q ≤ 3 fail quickly. For q = 1, the two lists are both 0, so their vertices
must be nonadjacent and cannot be injected into one slot. For q = 2, the lists are 0, 1, 01, 01; a
vertex with list 0 together with the two vertices with list 01 gives three pairwise nonadjacent vertices
using only two slots. For q = 3, the four lists 1, 01, 12, 012 all pairwise intersect, so their vertices
must be pairwise nonadjacent; again four vertices cannot be injected into three slots.
    The first useful case is therefore q = 4, where the eight lists are

                                      0, 1, 2, 3, 01, 12, 23, 0123.

We draw these lists in Figure 1. Intersecting intervals are forbidden to be edges; disjoint intervals
can be used as edges if they are needed to control independent sets.




                                                     7
                                    slots
                             vertices          0         1        2         3

                                      C0

                                      C1

                                      C2

                                      C3

                                      UL

                                       Q

                                     UR

                                       T

Figure 1: The first list system. Intersecting intervals cannot be joined by an edge; disjoint intervals
can be joined if needed to control independent sets.

    We write [q] = {0, 1, . . . , q − 1}. If F is a graph and each vertex v has a nonempty list X(v) ⊆ [q],
we say that (F, X) has the Hall property if every independent set I of F admits an injective map
ϕ : I → [q] with ϕ(v) ∈ X(v) for every v ∈ I. For A ⊆ [q], let FX [A] be the subgraph induced by
the vertices whose lists are contained in A.

Lemma 5. The pair (F, X) has the Hall property if and only if α(FX [A]) ≤ |A| for every A ⊆ [q].

Proof. Assume firstS that α(FX [A]) ≤ |A| for every A ⊆ [q]. Let I be an independent set, and let
J ⊆ I. Put SJ = v∈J X(v). Then J is an independent set in FX [SJ ], so |J| ≤ |SJ |. This is exactly
Hall’s condition for choosing distinct representatives from the lists X(v), v ∈ I.
     Conversely, assume that (F, X) has the Hall property. Any independent set in FX [A] has all its
lists contained in A, so its chosen representatives lie in A. Therefore it has size at most |A|.

   We now choose the graph. Name the vertices according to their first list system:

                             v    T   U L UR C0 C1 C2 C3 Q
                            X(v) 0123 01 23 0   1  2  3 12.

As explained above, edges may be added only between vertices with disjoint lists.
     The Hall condition tells us where edges are needed. Looking only at slots 0, 1, the vertices
C0 , C1 , UL are present. Since UL shares a slot with both C0 and C1 , it cannot be adjacent to either.
Therefore we add the edge C0 C1 ; otherwise these three vertices would form an independent set using
only two slots. The same argument for slots 1, 2 and 2, 3 forces C1 C2 and C2 C3 .
     Next look at slots 0, 1, 2. The vertices C0 , C2 , UL , Q would otherwise be independent, so we need
one more edge among pairs with disjoint lists. We add C0 Q. Similarly, looking at slots 1, 2, 3, we
add C3 Q. These two choices close the five-cycle C0 − C1 − C2 − C3 − Q − C0 , while still respecting
the rule that edges use disjoint lists.
     Finally, T uses every slot, so it is isolated. The five-cycle has independence number two. Thus,
without an edge between UL and UR , we could take T , both vertices UL , UR , and an independent
pair from the cycle. That would give an independent set of size five.

                                                    8
    A single edge from one of UL , UR to the cycle does not remove this obstruction. Such an edge
rules out only those independent pairs using one specified cycle vertex, while the five-cycle still has
an independent pair avoiding that vertex. Therefore, if UL and UR are left nonadjacent, one would
need further edges to meet all independent pairs of the cycle. Since the lists 01 and 23 are disjoint,
the single edge UL UR removes the obstruction at once.
    The resulting graph is
                                        F = C 5 ⊔ K2 ⊔ K1 ,
where the five-cycle is C0 − C1 − C2 − C3 − Q − C0 , the edge is UL UR , and the isolated vertex is T .
The largest independent sets in these three components have sizes 2, 1, 1, adding exactly to the four
slots available. The graph is shown in Figure 2.

                                         C0

                                Q                   C1        UL       UR



                                    C3         C2                  T


                              Figure 2: The graph F = C5 ⊔ K2 ⊔ K1 .

Lemma 6. The pair (F, X) has the Hall property, and vertices with a common X-slot are nonadjacent.

Proof. The second statement holds by construction: every edge was added only between vertices
with disjoint X-lists.
    We verify the Hall property using Lemma 5. If |A| ≤ 1, then FX [A] contains at most one vertex.
If |A| = 2, the possible induced subgraphs are

                                              A    FX [A]
                                              01 C0 C1 ⊔ UL
                                              12 C1 C2 ⊔ Q
                                              23 C2 C3 ⊔ UR
                                              02  C0 ⊔ C 2
                                              03  C0 ⊔ C 3
                                              13 C1 ⊔ C3 .

Each has independence number at most two. If |A| = 3, the vertex T is not present; the available part
of the five-cycle has independence number at most two, and at most one of UL , UR is present. Thus the
independence number is at most three. Finally, α(F ) = α(C5 ) + α(K2 ) + α(K1 ) = 2 + 1 + 1 = 4.

    The first list system is enough to control the crossings in the 64-rectangle family, but it does not
record all the information needed for the next round. When a copy is made after swapping the two
coordinates, the old horizontal guide lines become vertical guide lines for that copy. Thus the base
drawing should also record which horizontal guide lines pass through each rectangle. We encode this
information by a second list system Y .
    The requirements on Y are gentler than the requirements on X. For X, sharing a slot had
to force nonadjacency, because X controls the mixed intersections in the first horizontal-vertical
arrangement. For Y , we only ask that independent sets can choose distinct horizontal slots. Adjacent


                                                         9
vertices may therefore share a horizontal slot, because they never have to be assigned slots at the
same time.
    This turns the choice of Y into a small assignment problem: how should four horizontal slots be
spent on the three components of F ? A largest independent set uses at most one vertex from the
isolated component, at most one endpoint of UL UR , and at most two vertices from the five-cycle.
This suggests one slot for T , one shared slot for UL , UR , and two slots for the five-cycle. Put T on
slot 3, and put both UL and UR on slot 2.
    It remains to place the five-cycle on slots 0 and 1. If every cycle vertex were forced to a single
one of these two slots, then some nonadjacent pair would be forced to share a slot. We instead
leave one cycle vertex flexible. For the present labeling, put the adjacent pair C0 , Q on slot 0 and
the adjacent pair C1 , C2 on slot 1. The remaining vertex C3 is adjacent to one vertex in each pair,
namely Q and C2 . If C3 is selected and both slots 0 and 1 are already occupied, then the other
selected cycle vertices must be C0 and C1 , but those two are adjacent. Thus giving C3 the choice 01
lets it avoid whichever slot is already used.
    Thus the second list system is

                                 v   T    UL UR C0 C1 C2 C3 Q
                               Y (v) 3     2  2 0  1  1 01 0.

Lemma 7. The pair (F, Y ) has the Hall property.

Proof. Let I be an independent set. If T ∈ I, assign it to slot 3. Since UL UR is an edge, at most
one of UL , UR lies in I; assign it to slot 2 if present. The remaining vertices of I lie on the five-cycle,
so there are at most two of them. The vertices forced to slot 0, namely C0 , Q, are adjacent, and the
vertices forced to slot 1, namely C1 , C2 , are adjacent. The only vertex with a choice is C3 , whose list
is 01. If C3 is present and another selected cycle vertex has already used one of slots 0, 1, assign
C3 to the other slot; if C3 is the only selected cycle vertex, assign it to either slot. This gives an
injective assignment for every independent set.

Proposition 8. The graph F has a rectangle realization with four distinguished vertical lines and
four distinguished horizontal lines such that the lines passing through each rectangle are exactly the
lists X and Y .

Proof. Work in the square [0, 30]2 . Use the following eight rectangles, drawn in Figure 3:




                                                    10
                               3                           T



                               2                UL                  UR




                               1                     C1        C2

                                                                         C3
                                       C0

                               0
                                                           Q

                                       0             1         2          3


Figure 3: The eight rectangles realizing F . The dashed vertical lines give the X-lists, and the dashed
horizontal lines give the Y -lists.


                                                x-interval y-interval
                                           T      [0, 30]   [26, 28]
                                           UL     [0, 16]   [20, 22]
                                           UR    [14, 30]   [20, 22]
                                           C0      [0, 8]    [2, 10]
                                           C1     [6, 16]    [8, 14]
                                           C2    [14, 24]    [8, 14]
                                           C3    [22, 30]    [2, 12]
                                           Q      [6, 24]    [0, 4].
Let the distinguished vertical lines be ξ = (3, 11, 19, 27) and the distinguished horizontal lines be
η = (3, 11, 21, 27). Reading off containment in the displayed intervals gives exactly the lists X and
Y . We shall also use the following small separation fact: every distinguished line is either at least
one unit inside the relevant interval, or at least one unit outside it. This is immediate from the table.
    Checking interval overlap in both coordinates, the intersecting pairs are UL UR and

                                   C0 C1 , C1 C2 , C2 C3 , C3 Q, QC0 .

These are precisely the edges of F .


7    Repeating horizontal and vertical copies
The eight-rectangle drawing has two kinds of information. The rectangles themselves give the graph
F , while the distinguished lines give the two list systems X and Y . We now turn the preceding
design into coordinates: one drawing with such data produces a larger drawing with the same kind
of data.
      Suppose a rectangle family P is drawn inside [0, L]2 with q distinguished vertical lines ξ0 < ξ1 <
· · · < ξq−1 and q distinguished horizontal lines η0 < η1 < · · · < ηq−1 . The list X(R) records the
vertical lines contained in R, and Y (R) records the horizontal lines contained in R. We assume both
list systems have the Hall property. We also assume the same separation used in Proposition 8:

                                                          11
each marker line is at least one unit inside or at least one unit outside every relevant interval, and
consecutive marker lines are at least one unit apart in each direction.
   Set M = L + 1. For a rectangle R = [x1 , x2 ] × [y1 , y2 ] in P , define a horizontal copy in row i by

                            Hi (R) = [M x1 , M x2 ] × [M ξi + y1 , M ξi + y2 ],

and define a vertical copy in column j by

                            Vj (R) = [M ξj + y1 , M ξj + y2 ] × [M x1 , M x2 ].

The vertical copy is a transposed copy of R. Let C(P ) be the family of all rectangles Hi (R) and
Vj (R), where R ∈ P and i, j ∈ [q]. We call this the crossbar operation. All these rectangles lie in
[0, L′ ]2 , where L′ = M L + L. The same spacing makes the row blocks pairwise disjoint and the
column blocks pairwise disjoint, so distinct horizontal copies do not meet one another, and distinct
vertical copies do not meet one another. Thus C(P ) has 2q|P | rectangles.
    For the base drawing, the first crossbar P1 = C(P0 ) is the 64-rectangle family shown in Figure 4.

                       V0                   V1                    V2                V3




            H3




            H2




            H1




            H0




Figure 4: The 64 rectangles of P1 = C(P0 ). Blue rectangles are the four horizontal copies of P0 , and
orange rectangles are the four transposed vertical copies. The long gaps have been compressed and
the copied strips enlarged to make all rectangles visible.



                                                    12
   Figure 5 gives a clearer drawing of the same 64-rectangle graph. It uses compact coordinates that
keep the horizontal and vertical copy structure visible and leave room for the marker-grid overlay in
Figure 12. The formal recursion is still the coordinate construction just defined.

                     V0                     V1                    V2                  V3
                                                                                                b


                                                                                                3
                                                                                                2
        H3                                                                                      1
                                                                                                0




                                                                                                3
                                                                                                2
        H2                                                                                      1
                                                                                                0




                                                                                                3
                                                                                                2
        H1                                                                                      1
                                                                                                0




                                                                                                3
                                                                                                2
        H0                                                                                      1
                                                                                                0



             t     0 1   23                0 1   23              0 1   23           0 1   23



Figure 5: A fatter drawing of the same graph as Figure 4. The compact coordinates keep the Hi
and Vj copies visible; the dashed lines show the marker grid used again in Figure 12. In column Vj ,
                                                                             ′
the labels below the drawing give t, so the vertical marker lines are named ξ(j,t) ; in row Hi , the right
                                                          ′
labels give b, so the horizontal marker lines are named η(i,b) .

   For the coordinate construction defining C(P ), the reason for the scaling is that each old marker
used to index a row or column has been expanded to a whole block of length L in the relevant
coordinate. This makes the crossing rule exact, and we prove it formally as a lemma.
Lemma 9 (Crossing rule). For rectangles R, S ∈ P and slots i, j ∈ [q],
                          Hi (R) ∩ Vj (S) ̸= ∅    ⇐⇒       j ∈ X(R) and i ∈ X(S).
Proof. The x-interval of Vj (S) lies inside the block [M ξj , M ξj + L]. If j ∈ X(R), then ξj lies at
least one unit inside the x-interval of R, so [M x1 , M x2 ] contains the whole block [M ξj , M ξj + L].

                                                      13
If j ∈
     / X(R), the same separation makes [M x1 , M x2 ] disjoint from that block. Thus the two new
rectangles overlap in the x-coordinate exactly when j ∈ X(R).
    The y-coordinate is the same argument with S in place of R: the y-interval of Hi (R) lies inside
the block [M ξi , M ξi + L], while the y-interval of Vj (S) is the scaled x-interval of S. They overlap
exactly when i ∈ X(S). Together, the two coordinates carry the two slot tests separately, giving the
claimed equivalence.

   The new drawing also has marker lines. Each old marker has been expanded to a block that
contains a copy of the old drawing, so a new marker is labelled by two pieces of data: the old block,
and the old marker inside that block. Index the new markers by ordered pairs in [q] × [q] and set
                                  ′                            ′
                                 ξ(j,t) = M ξj + ηt ,         η(i,t) = M ξi + ηt .

They are ordered lexicographically by the first coordinate.
    The formulas for the new lists now come directly from the coordinates. The rectangle Hi (R)
is stretched in the x-direction, so whenever R contained the old vertical marker j, the copy Hi (R)
contains the whole new block over j, and hence all markers (j, t). This gives X ′ (Hi (R)) = X(R) × [q].
In the y-direction, the same rectangle lives only in row i, and inside that row it sees the old horizontal
markers of R; this gives Y ′ (Hi (R)) = {i} × Y (R). The vertical copies are transposed, so the same
reading swaps the old horizontal and vertical directions. Altogether,
                         X ′ (Hi (R)) = X(R) × [q],          Y ′ (Hi (R)) = {i} × Y (R),
                          X ′ (Vj (R)) = {j} × Y (R),        Y ′ (Vj (R)) = X(R) × [q].

The entry X ′ (Vj (R)) = {j} × Y (R) is the point where old horizontal data becomes new vertical
data. This is the precise place where the second list system is used.
    The same one-unit separation is preserved: after scaling by M = L + 1, every old one-unit margin
becomes a gap of length at least L + 1, and inserting a copy of the old [0, L]2 drawing still leaves
room on the required side of each new marker. The marker spacing is preserved as well. Inside one
old block it is the old spacing among the markers ηt ; between consecutive old blocks it is at least
M (ξj+1 − ξj ) − L ≥ 1. Thus the construction can be repeated1 .
    We now show that the repetition preserves the Hall properties.
Lemma 10. If both (P, X) and (P, Y ) have the Hall property, then both (C(P ), X ′ ) and (C(P ), Y ′ )
have the Hall property.
Proof. We prove the statement for X ′ . Let I be an independent set in C(P ). First consider a fixed
vertical copy Vj (P ). Since (P, Y ) has the Hall property, the rectangles of I ∩ Vj (P ) can be assigned
distinct old Y -slots. If Vj (S) receives the old slot t ∈ Y (S), place it in the new slot (j, t). Here Y is
used to choose distinct inner positions in the column j.
    Now consider a fixed horizontal copy Hi (P ). Since (P, X) has the Hall property, the rectangles
of I ∩ Hi (P ) can be assigned distinct old X-slots. Think of such an assignment as choosing an outer
column j for each selected horizontal rectangle.
    Fix a column j. Let                              [
                                            Aj =          X(S).
                                                   Vj (S)∈I

The same vertical rectangles also block rows, and this blocking is measured by their old X-lists.
The rectangles of I ∩ Vj (P ) are independent inside the old graph, so the Hall property for X gives
  1
    For the first step, this bookkeeping has a very nice and concrete graph-level picture, and we record that in
Section A, which shows the sixteen crossings of P1 and the complete bipartite pieces that appear inside them.


                                                        14
|I ∩ Vj (P )| ≤ |Aj |. If i ∈ Aj , then some selected Vj (S) has i ∈ X(S). By Lemma 9, no selected
horizontal rectangle in row i can be assigned to column j, since that assignment would mean
j ∈ X(R) and would create an intersection.
     Thus the selected horizontal rectangles assigned to column j can come only from the q − |Aj |
rows outside Aj . The old X-assignment is injective inside each horizontal copy, so there is at most
one such rectangle from each row. There are already |I ∩ Vj (P )| occupied slots among the q slots
(j, 0), . . . , (j, q − 1), so at least q − |I ∩ Vj (P )| remain free. Since q − |Aj | ≤ q − |I ∩ Vj (P )|, the
horizontal rectangles assigned to column j can be placed into these free inner slots. This is allowed
because X ′ (Hi (R)) = X(R) × [q]: once Hi (R) has been assigned to column j, it may use any inner
slot (j, t). Doing this for every j injects all of I into the X ′ -slots.
     The proof for Y ′ is the same with the roles of horizontal and vertical copies interchanged; the
formulas for Y ′ are obtained from the formulas for X ′ by making exactly that coordinate swap.
Equivalently, the column-by-column assignment above becomes a row-by-row assignment, with old
X- and Y -slots interchanged.
    Starting with the base drawing P0 from Proposition 8, define
                                               Pr+1 = C(Pr ).
Let qr be the number of slots in each direction for Pr . Then
                                                                         r
                                   q0 = 4,       qr+1 = qr2 ,     qr = 42 .
By Lemma 10, every Pr has the Hall property in both directions.
Proposition 11. For every r ≥ 0, α(Pr ) = qr and |Pr | = 2r+1 qr .
Proof. The Hall property gives α(Pr ) ≤ qr . For the reverse inequality, notice that Pr+1 contains qr
pairwise disjoint horizontal copies of Pr . Taking a maximum independent set in each of these copies
gives α(Pr+1 ) ≥ qr α(Pr ). Since α(P0 ) = α(F ) = 4 = q0 , induction gives α(Pr ) = qr for all r.
    The size formula follows from |P0 | = 8 = 2q0 and |Pr+1 | = 2qr |Pr |.
Proof of Theorem 1. The first repeated drawing P1 has
                                             |P1 | = 2 · 4 · 8 = 64
rectangles. By Proposition 11, ν(P1 ) = α(P1 ) = q1 = 16.
    It remains to check triangle-freeness. A triangle cannot lie inside one copy, because P0 is the
triangle-free graph C5 ⊔ K2 ⊔ K1 . Distinct horizontal copies are disjoint from one another, and
distinct vertical copies are disjoint from one another. Hence any remaining triangle would have two
rectangles from one copy and one rectangle from a copy in the other direction.
    Suppose two rectangles Hi (R1 ), Hi (R2 ) in the same horizontal copy both meet a rectangle
Vj (S). By Lemma 9, both old rectangles R1 and R2 have j in their X-lists. By Lemma 6, they
are nonadjacent in the base graph, so their horizontal copies do not intersect. The case with two
rectangles in one vertical copy is identical. Therefore P1 is triangle-free.
    Since no point can lie in three rectangles of a triangle-free rectangle family, every piercing point
meets at most two rectangles. Thus
                                                     64
                                           τ (P1 ) ≥    = 32.
                                                     2
But 2ν(P1 ) − 1 = 31, so τ (P1 ) > 2ν(P1 ) − 1. The exact value of τ (P1 ) is not needed for this
conclusion; the lower bound 32 already crosses the conjectured threshold.
    This is the only place where the repeated family is used through triangle-freeness. The later
levels retain the recursive slot data and the identity ν(Pr ) = qr , which are the features used for the
LP and piercing results below.

                                                      15
8     Finite LP gaps
The same separation into local copies and mixed crossings also makes the LP checks small. We work
with the clique relaxation from Section 5; for rectangle families, this is the standard point relaxation.
The guiding idea is to judge a weighting on one copy by two features at once: the total value it
contributes, and the amount of clique weight that can be seen through each slot when another copy
crosses it. The latter quantities will be defined below as loads. A high-value weighting is useful only
if its exposed loads can be paired with small enough loads from the copy crossing it.
     The first repeated family P1 already gives a feasible LP value equal to 2ν(P1 ): since P1 is
triangle-free, assigning weight 1/2 to every rectangle is feasible and has value 32 = 2ν(P1 ). At the
next level there is a short hand-checkable weighting whose value is strictly larger than 2ν(P2 ). We
describe this weighting before the larger P3 construction, because it shows the mechanism in its
smallest form.
     We first set up the bookkeeping used to check feasibility when weights are placed on horizontal
and vertical copies.
     For a nonnegative weight vector w on a rectangle family P , write w(K) for the sum of the weights
on a clique K. If P has x-slots and y-slots, the rectangles using a fixed x-slot s form the x-slot class
of s. Define

            Xw (s) = max{w(K) : K is a clique and every rectangle in K uses x-slot s},

             Yw (t) = max{w(K) : K is a clique and every rectangle in K uses y-slot t},
and

        Zw (s, t) = max{w(K) : K is a clique and every rectangle in K uses both slots s, t}.

We call these numbers the x-load at s, the y-load at t, and the joint load at (s, t), respectively. The
empty clique is allowed in these maxima and has weight zero.

Lemma 12. Let P be one of the recursive rectangle families, and put weights hi on the horizontal
copies Hi (P ) and weights vj on the vertical copies Vj (P ) inside C(P ). Assume that each hi and vj
is feasible on its own copy. If
                                         Xhi (j) + Xvj (i) ≤ 1
for every pair i, j, then the resulting weight vector on C(P ) is clique-feasible.
     Moreover, if X ′ denotes the x-load function of the resulting weight vector, then for the new x-slot
(j, t) in C(P ),                                                              
                           X ′ (j, t) ≤ max Yvj (t), max Xhi (j) + Zvj (i, t) .
                                                                             
                                                        i

Proof. Distinct horizontal copies are disjoint from one another, and distinct vertical copies are
disjoint from one another. Hence every clique in C(P ) is either contained in one copy, or lies in
Hi (P ) ∪ Vj (P ) for a unique pair i, j. The local cliques are feasible by assumption. In the mixed case,
Lemma 9 says that the horizontal part is contained in the old x-slot class for j, and the vertical part
is contained in the old x-slot class for i. Thus its weight is at most Xhi (j) + Xvj (i).
    For the displayed bound, a clique in the new x-slot (j, t) is either wholly inside Vj (P ), giving the
term Yvj (t), or has a horizontal part inside some Hi (P ). In the second case its horizontal part lies in
the old x-slot class for j. Its vertical part, if present, lies in the old joint slot class for (i, t); if it is
absent, the empty clique contributes zero to Zvj (i, t).


                                                      16
    The lemma also suggests a useful compression. In P1 , the x-slots are pairs (a, b) ∈ [4]2 . The first
coordinate records the old block, while the second coordinate records which base slot lies inside that
block. The weightings below treat the old blocks uniformly, so their loads depend only on the second
coordinate. We call this coordinate the final digit of the slot. In P2 = C(P1 ), the horizontal and
vertical copies of P1 are indexed by the sixteen slots of P1 , and the final digit of a copy means the
final digit of its index.
    This convention keeps the finite checks small. Although there are sixteen copies of P1 in each
direction inside P2 , the weightings below have only four types, according to this final digit.
    The two subsections below have different roles. The first gives a direct feasible weighting on P2
with value larger than 2ν(P2 ). The second constructs a more evenly distributed vector on P2 , whose
x-loads are all at most 1/2; placing that vector in every copy at the next level gives the P3 gap from
Theorem 2. The one-copy load checks used in both subsections are collected in Section B.

8.1    A first gap above 2
We begin with a feasible vector on P2 whose value is already larger than 2ν(P2 ). The ingredients
are six weightings of P1 .
    Let C = {C0 , C1 , C2 , C3 , Q} be the five-cycle in the base graph, and let U = {UL , UR }. Inside
a copy of P1 , there are four horizontal copies of P0 and four vertical copies of P0 . We use a small
class of weightings chosen to follow the distinctions made by the final-digit checks. The horizontal
half contributes in the same way to every final digit. In the vertical half, digits 0 and 1 see the
five-cycle part, digit 2 sees the pair UL , UR , and digit 3 sees T . This suggests four weights: let h be
the weight on every rectangle in the horizontal half of P1 ; in the vertical half, let c be the weight on
the five-cycle vertices C, let u be the weight on the two vertices in U, and let t be the weight on T .
    The four horizontal copies contribute 4·8h, while the four vertical copies contribute 4·5c+4·2u+4t.
Thus such a weighting has total value

                                         32h + 20c + 8u + 4t.

    With these four weights, the relevant x-loads are easy to read. For a slot (a, b) of P1 , only the
final digit b matters. If b = 0 or 1, the vertical vertices using that old horizontal slot form a path of
two possible edges in the five-cycle. A clique using the slot either lies wholly in that vertical copy,
giving weight at most 2c, or also uses one horizontal rectangle, giving weight at most h + c. Thus

                                   X(0) = X(1) = max{h + c, 2c}.

The same reasoning for the pair UL , UR gives

                                       X(2) = max{h + u, 2u},

and the slot containing only T gives
                                             X(3) = h + t.
    So the choice of profiles becomes a small load-budget problem. When a horizontal copy of final
digit b faces a vertical copy of final digit d in P2 , Lemma 12 asks that the d-load of the horizontal
profile and the b-load of the vertical profile add to at most one.
    The table below can be found by working backwards from this budget. The first useful place
to look is the high-value end of this four-parameter class. The uniform horizontal weight may be
set to h = 1/2, and cannot be made larger, because each horizontal copy contains edges. The same
reasoning lets us set the five-cycle weight to c = 1/2. We keep t = 0, since T spends the final-digit-3

                                                   17
budget and contributes only four rectangles. The remaining useful dial is u, which changes the
final-digit-2 load. This leads to the one-parameter family

                                     (h, c, u, t) = (1/2, 1/2, u, 0).

For 0 ≤ u ≤ 1/4, which is the range used below, this family has value 26 + 8u and load vector

                           (X(0), X(1), X(2), X(3)) = (1, 1, 1/2 + u, 1/2).

Thus it spends the full budget in final digits 0 and 1, spends only half the budget in final digit 3,
and leaves a tunable amount in final digit 2. Trying to use this family in the vertical copies of P2
immediately forces the horizontal rows with final digits 0 and 1 to be zero. The row with final digit
3 may carry load 1/2 in every digit, giving the balanced profile B below. The row with final digit 2
is where the remaining freedom lies.
    The row with final digit 2 must now mediate between these choices. In two columns it should
use half the budget, so only the choice u = 0 from the high-value family fits opposite it. In one
column it should use little budget, so the largest choice from the same family fits. In the remaining
column it should use an intermediate amount. The first two requirements set the first two entries
to 1/2, and the largest choice u = 1/4 sets the last entry to 1/4. The middle entry may be any
value between 1/4 and 1/2; changing it only shifts digit-2 weight from the row profile to the middle
vertical profile. We take the midpoint, giving the target

                                        ℓ = (1/2, 1/2, 3/8, 1/4).

Pushing the four weights under these caps gives (h, c, u, t) = (1/4, 1/4, 1/8, 0): the cap in final digit
3 permits h = 1/4 with no weight on T ; then the caps in final digits 0, 1 permit c = 1/4, and the
cap in final digit 2 permits u = 1/8. This is the profile A. Now a vertical column of final digit d
has remaining budget 1 − ℓd , where ℓd is the dth entry of ℓ. Since the high-value family contributes
1/2 + u in row 2, we need u ≤ 1/2 − ℓd . Hence digits 0 and 1 force u = 0, digit 2 allows u = 1/8,
and digit 3 allows u = 1/4. These are the profiles C, D, E.
    The six profiles below record this solution. A bare number in the table means that every rectangle
in that half receives that weight; omitted parts receive weight zero.


       name horizontal half       vertical half     value (X(0), X(1), X(2), X(3))
        O         0                     0             0          (0, 0, 0, 0)
        A        1/4        C : 1/4, U : 1/8, T : 0  14     (1/2, 1/2, 3/8, 1/4)
        B        3/8                  1/8            16     (1/2, 1/2, 1/2, 1/2)                   (8.1)
        C        1/2         C : 1/2, U : 0, T : 0   26       (1, 1, 1/2, 1/2)
        D        1/2        C : 1/2, U : 1/8, T : 0  27       (1, 1, 5/8, 1/2)
        E        1/2        C : 1/2, U : 1/4, T : 0  28       (1, 1, 3/4, 1/2).

    In the last column, X(b) denotes an upper bound on Xw (a, b) for any first digit a; the bound
depends only on the final digit b. For the displayed profiles, these bounds are exactly the numbers
given by the formulas above. For instance, profile A has (h, c, u, t) = (1/4, 1/4, 1/8, 0), and hence
X(2) = h + u = 3/8. Profile E has (h, c, u, t) = (1/2, 1/2, 1/4, 0), and hence X(2) = h + u = 3/4.
    Each of the six weightings is feasible on P1 . Feasibility on P1 is immediate from triangle-freeness:
every clique is a vertex or an edge, and every edge in the listed supports has total weight at most
one. The mixed table below shows how the local bounds spend the available slack.
    In Figure 6, b denotes the final digit of the horizontal copy index and d denotes the final digit of
the vertical copy index.

                                                   18
                    profile assignment                         mixed clique sums
                             0 1 2       3                   d = 0, 1     d=2        d=3
                horizontal O O A         B       b = 0, 1     0+1         0+1        0+1
                 vertical    C C D       E        b=2       1/2 + 1/2 3/8 + 5/8    1/4 + 3/4
                                                  b=3       1/2 + 1/2 1/2 + 1/2    1/2 + 1/2

Figure 6: Bookkeeping for the P2 weighting. The final digits are the four base slot types, and the
right panel records how the chosen profiles spend the mixed-clique load budget in Proposition 13.

    We now show that P2 actually beats 2.

Proposition 13. The second recursive family satisfies

                                             α∗ (P2 )   137
                                                      ≥     > 2.
                                             ν(P2 )      64

Proof. In a horizontal copy Hi (P1 ) of P2 , place the weightings

                                                O, O, A, B

when the final digit of i is 0, 1, 2, 3, respectively. In a vertical copy Vj (P1 ), place

                                                C, C, D, E

when the final digit of j is 0, 1, 2, 3, respectively.
    Local cliques are feasible by the discussion above. For a mixed clique between Hi (P1 ) and Vj (P1 ),
let b be the final digit of i and d the final digit of j. By Lemma 12, it is enough to check the following
sums:
                                           d = 0, 1       d=2       d=3
                                b = 0, 1    0+1           0+1       0+1
                                                                                                      (8.2)
                                 b = 2 1/2 + 1/2 3/8 + 5/8 1/4 + 3/4
                                 b = 3 1/2 + 1/2 1/2 + 1/2 1/2 + 1/2.
Every entry is at most one, so the whole weight vector is clique-feasible.
   Each final digit occurs four times among the sixteen copies. The total weight is therefore

                              4(14) + 4(16) + 8(26) + 4(27) + 4(28) = 548.

By Proposition 11, ν(P2 ) = q2 = 256. Hence

                                          α∗ (P2 )   548   137
                                                   ≥     =     .
                                          ν(P2 )     256    64



8.2    A finite gap above the previous bound
For the next finite improvement, we need a vector that can be placed in every horizontal and every
vertical copy of P2 inside P3 . The previous weighting beats 2 by matching heavier profiles with
lighter profiles in particular final digits. That is enough for one level. A reusable vector needs a
uniform cap instead: every old x-slot class should contribute at most 1/2, so that a mixed clique in
P3 sees at most 1/2 + 1/2.


                                                     19
   The same level P2 contains such a vector. Its total value is smaller than the one in the previous
subsection, but the uniform 1/2 bound on its x-loads makes it reusable.
   We use four simpler weightings on P1 , together with the zero profile, which we denote by 0; again,
omitted parts receive weight zero. The profiles R, S are used in horizontal copies, while U, V are
used in vertical copies; the table is arranged so that the mixed clique sums and the new x-loads can
both be checked from the final digit:
    name                        definition                      value (X(0), X(1), X(2), X(3))
     R           horizontal half: 1/4; vertical C : 1/4          13      (1/2, 1/2, 1/4, 1/4)
      S          horizontal half: 1/2; vertical half: 0          16      (1/2, 1/2, 1/2, 1/2)
     U                 vertical C : 1/2; all else: 0             10            (1, 1, 0, 0)
     V    vertical C : 1/2, U : 1/4, T : 0; horizontal half: 0   12         (1, 1, 1/2, 0).
                                                                                              (8.3)
For U and V we shall also use
                              1
            YU (t), YV (t) ≤ ,        ZU ≤ (1/2, 1/2, 0, 0),   ZV ≤ (1/2, 1/2, 1/4, 0),       (8.4)
                              2
where the entries of ZU and ZV are again indexed by the final digit of the x-slot, uniformly in the
y-slot. These bounds follow from the same one-copy check as before, recorded in Section B. In a
vertical copy, fixing a y-slot fixes an old X-slot in the base, because Y ′ (Vj (R)) = X(R) × [4]; vertices
using one old X-slot are independent.
    In Figure 7, b denotes the final digit of the horizontal copy index and d denotes the final digit of
the vertical copy index.
            profile assignment              mixed clique checks             new x-load checks
                     0 1 2       3                d = 0, 1 d = 2, 3              Vj = U Vj = V
        horizontal 0 0 R         S       b = 0, 1    1        1         b = 0, 1 ≤ 1/2     ≤ 1/2
         vertical    U U V       V        b=2       1/2      3/4         b=2     ≤ 1/2     ≤ 1/2
                                          b=3       1/2      1/2         b=3     ≤ 1/2     ≤ 1/2

Figure 7: Bookkeeping for the reusable vector A2 . The profile assignment is shown on the left. The
two checks record the mixed-clique bounds inside P2 and the uniform 1/2 bound on the new x-loads.

Lemma 14. There is a clique-feasible weight vector A2 on P2 with total value 292 such that
XA2 (s) ≤ 1/2 for every x-slot s of P2 .
Proof. In the horizontal copies of P1 inside P2 , place
                                                  0, 0, R, S
according to final digit 0, 1, 2, 3. In the vertical copies, place
                                               U, U, V, V.
The value is
                                  4(13) + 4(16) + 8(10) + 8(12) = 292.
   Feasibility follows from Lemma 12 and the table
                                                   d = 0, 1 d = 2, 3
                                       b = 0, 1       1        1
                                                                                                      (8.5)
                                        b=2          1/2      3/4
                                        b=3          1/2      1/2

                                                      20
where b is the final digit of the horizontal copy and d is the final digit of the vertical copy. For
example, the entry 3/4 is XR (2) + XV (2) ≤ 1/4 + 1/2.
    It remains to bound the new x-loads. Fix a new x-slot (j, t) of P2 . If the clique is wholly inside
the vertical copy Vj (P1 ), the load is at most 1/2 by (8.4). If the clique has a horizontal part, the
second part of Lemma 12 and the bounds above give

                                                   Vj = U    Vj = V
                                        b = 0, 1   ≤ 1/2     ≤ 1/2
                                                                                                        (8.6)
                                         b=2         1/2       1/2
                                         b=3         1/2      1/2.

Here the entries are the resulting upper bounds. For b = 0, 1 the horizontal term is zero and the
vertical term is at most 1/2 by (8.4); the remaining entries come from 1/2 + 0, 1/4 + 1/4, 1/2 + 0,
and 1/2 + 0. Every entry is at most 1/2.

Proof of Theorem 2. Form P3 = C(P2 ), and put one copy of the vector A2 from Lemma 14 in every
horizontal and every vertical copy of P2 . Local cliques are feasible. A mixed clique meets one
horizontal copy and one vertical copy, and by Lemma 14 each side contributes at most 1/2 to the
relevant old x-slot class. Thus every mixed clique has weight at most one.
    The total value is
                                  2q2 · 292 = 2 · 256 · 292 = 149504.
Since ν(P3 ) = q3 = 65536,
                                         α∗ (P3 )   149504  73
                                                  ≥        = .
                                         ν(P3 )     65536   32
Finally, compared with the bound of [AGRR26, Theorem 15],
                                         73 17891    505
                                            −      =      > 0.
                                         32   8064   8064



9    Fractional solutions approaching 5/2
The vector A2 from Lemma 14 leaves us with a useful clue. Its total value gives the finite gap at
P3 , but the more important feature is the uniform bound XA2 (s) ≤ 1/2. Once a weighting has this
half-load property, it can be placed in every horizontal and every vertical copy at the next level:
every mixed clique then sees at most 1/2 from each side.
     This suggests the question for the rest of the section. Can the half-load property be propagated
while the normalized value keeps growing? If we can build, on each Pr , a half-load weighting whose
normalized value tends to 5/4, then putting it in every copy of Pr+1 gives ratios tending to 5/2.
     At first it may seem that such a recursion has to remember every slot at every level. The
construction has a simpler trace. In the base slots, split

                                       L = {0, 1},        H = {2, 3}.

For a slot of Pr+1 , written as an ordered pair (j, t) of old slots, its class is the class of the inner slot
t. Thus every level has two equally large slot classes, low and high. The finite constructions above
used the whole final digit; the limiting construction only needs this low/high information.


                                                     21
    This split is already visible in the profile that starts the recursion. The five-cycle vertices of P0
use only the horizontal slots 0 and 1. When those vertices are placed in vertical copies, old horizontal
slots become new x-slots. Thus the first source of fractional weight naturally lives on the low x-side
and leaves the high x-side empty. The recursion keeps exploiting this simple imbalance: low slots
carry weight, high slots provide room, and the next crossing only needs to know which of these two
situations it is seeing.
    For a weighting w on Pr , write Xw (L) for the maximum of Xw (s) over low x-slots s, and define
Xw (H) similarly. We use the same convention for Yw . For joint loads, Zw (L, H) means the maximum
of Zw (s, t) over low x-slots s and high y-slots t. Rows of a displayed Z-matrix are indexed by the
x-class, and columns by the y-class.
    The next lemma records the old crossing calculation after this compression. It is the only formal
bookkeeping needed in the section: once the loads are known in the two classes, the next level can
be checked without remembering the individual slots.

Lemma 15. Let P = Pr . Suppose that hL , hH and vL , vH are feasible weightings on P . In C(P ),
place hb in each horizontal copy whose index has class b, and place vd in each vertical copy whose
index has class d. If
                                      Xhb (d) + Xvd (b) ≤ 1
for all b, d ∈ {L, H}, then the resulting weighting on C(P ) is feasible.
    Moreover, its new class loads satisfy

                               Xf′ ≤ max{Yvd (f ), Xhb (d) + Zvd (b, f )},
                                       b,d

                                Ye′ ≤ max{Yhb (e), Xvd (b) + Zhb (d, e)},
                                       b,d

and
                                   ′
                                  Zf,e ≤ max{Zhb (d, e) + Zvd (b, f )},
                                             b,d

where b, d, e, f ∈ {L, H}. Here Xf′ is the maximum new x-load over slots of class f , and Ye′ and Zf,e
                                                                                                   ′

are interpreted similarly.

Proof. The feasibility statement is Lemma 12, after taking the maximum over all slots in the relevant
classes.
    The bound for X ′ is also the bound from Lemma 12, again maximized over the two slot classes.
The bound for Y ′ is the same argument with the two coordinates interchanged. For the joint load,
fix a new x-slot (j, t) and a new y-slot (i, u). A clique using both slots has a horizontal part using
the old joint slot class (j, u) and a vertical part using the old joint slot class (i, t). Empty parts
contribute zero, so the displayed upper bound follows after passing to the classes of i, j, t, u.

    Since Pr is obtained by a horizontal-vertical construction, every Pr with r ≥ 1 is invariant under
swapping the two coordinates. If w is a weighting on such a Pr , let wT denote the weighting obtained
by this swap. The coordinate swap sends horizontal copies to vertical copies and interchanges the
two marker systems. Thus wT has the same total value; its X- and Y -loads are interchanged, and
its Z-matrix is transposed. We will also use scalar multiples of weightings, with all weights and all
loads scaled by the same factor.
    We now describe the four jobs that the recursion keeps separate. A profile has normalized value
a if its total weight is aqr . The table below should be read as a list of promises a weighting makes to
the next round: how much total value it carries, and how much clique weight can be seen through
low and high slots.

                                                   22
    The profile Mr is the carrier. It is the one we can place everywhere at the next level, because
its x-load is at most 1/2 in both classes. The profile Cr is the stable source of weight described
above: it has value 5/8, puts weight on the low x-side, and leaves the high x-side empty. The profile
Rr softens a carrier by lowering the high x-load, and Dr carries extra value while keeping enough
control in the joint loads. The recursion moves weight through these three supporting shapes until it
returns to a larger value for the M -profile.

                           profile      X                Y        Z
                                                            1/2 1/2
                             M       (1/2, 1/2)      (1, 1)
                                                           1/2 1/2
                                                            1/2 1/2
                              R      (1/2, 1/4) (1/2, 1/2)
                                                           1/4 1/4                              (9.1)
                                                            1/2 1/2
                              C        (1, 0)   (1/2, 1/2)
                                                            0   0
                                                            1/2 1/2
                              D       (1, 3/4) (1/2, 1/2)            .
                                                            1/4 1/4
The entries in the X- and Y -columns are ordered as (L, H).

Lemma 16. There is a profile C1 on P1 with normalized value 5/8 and with the C-bounds in (9.1).
The zero vector on P1 serves as M1 , R1 , D1 .

Proof. In each of the four vertical copies of P0 inside P1 , give weight 1/2 to the five-cycle vertices
C = {C0 , C1 , C2 , C3 , Q}, and give weight zero to every other rectangle. The total value is
                                                  1       5
                                         4·5·       = 10 = q1 .
                                                  2       8
This weighting is feasible: positive weight appears only inside vertical copies of the five-cycle, and
every clique in a five-cycle has at most two vertices.
    Only the old Y -slots 0 and 1 occur among these weighted vertices, so the high x-class has
load zero. In a low x-slot, the possible weighted vertices in one vertical copy form either the path
C0 − Q − C3 or the path C1 − C2 − C3 ; every clique in either path has weight at most one. Thus
XC1 ≤ (1, 0).
    Fixing a y-slot in a vertical copy fixes an old X-slot of the base configuration. By Lemma 6, the
base vertices using one old X-slot are independent, so such a clique contains at most one weighted
vertex. This gives YC1 ≤ (1/2, 1/2). If both an x-slot and a y-slot are fixed, the same argument
gives at most one weighted vertex; in the high x-class there is no weighted vertex at all. This gives
the displayed Z-bounds for C. The zero vector plainly satisfies the remaining profile bounds.

     With the four profiles in hand, the recursive move is easy to state before checking. The source
Cr is preserved. A diluted copy of Mr , paired with a half-weight transposed copy of Cr , makes the
more balanced helper Rr+1 . A half-weight Cr and the old Dr make the next D-profile. Finally,
Rr , Cr , Dr are assembled into the next carrier Mr+1 . The figure records the roles of the four moves;
the precise low/high placement in horizontal and vertical copies is given immediately afterward.




                                                    23
                                                  preserve source
                                  Cr                                    Cr+1

                             1       1 T            soften M            Rr+1
                             2 M r , 2 Cr


                              1                     carry value
                              2 Cr ,   DrT                              Dr+1


                            Rr , Cr , Dr           build carrier        Mr+1

Figure 8: The four moves in the recursive fractional construction. The diagram shows which old
profiles feed each new profile; the exact low/high horizontal-vertical placement is given in (9.2).

Lemma 17. Assume that, on Pr with r ≥ 1, there are profiles Mr , Rr , Cr , Dr satisfying (9.1),
with normalized values mr , rr , c, dr , where c = 5/8. Then there are profiles Mr+1 , Rr+1 , Cr+1 , Dr+1
satisfying the same bounds on Pr+1 , with c unchanged and
                           mr + c                 dr  3c              rr + c + dr
                   rr+1 =          ,    dr+1 =       + ,     mr+1 =               .
                              2                   2   4                    2
Proof. The four profiles at level r + 1 are obtained by placing level-r profiles in the low and high
classes of horizontal and vertical copies as follows:
                       output    (hL , hH )         (vL , vH )   normalized value
                        Cr+1       (0, 0)        (CrT , CrT )             c
                               1         1       1 T 1 T
                        Rr+1 ( 2 Mr , 2 Mr ) ( 2 Cr , 2 Cr )        (mr + c)/2                      (9.2)
                        Dr+1  ( 12 Cr , 21 Cr ) ( 12 CrT , DrT )    dr /2 + 3c/4
                        Mr+1      (0, Rr )         (Cr , Dr )     (rr + c + dr )/2.
The value column follows because each of the two slot classes contains qr /2 copy indices in each
direction.
    It remains to check feasibility and the new load bounds. Applying Lemma 15 to the bounds
in (9.1) gives the following table. In the mixed-load column, rows are horizontal-copy classes and
columns are vertical-copy classes, both ordered as L, H.
    For instance, the row producing Mr+1 is the payoff. Low horizontal copies are left empty, high
horizontal copies receive Rr , low vertical copies receive Cr , and high vertical copies receive Dr . The
mixed loads are                                               
                                           0+1         0+1
                                                                 ,
                                          1/2 + 0 1/4 + 3/4
so no mixed clique exceeds one. The tight high-horizontal/high-vertical entry is
                                   XR (H) + XD (H) = 1/4 + 3/4 = 1.
The new x-loads ask for a different check. The vertical-only contribution is at most 1/2. If the clique
also has a horizontal part, then the high-horizontal/high-vertical case uses the joint-load bound of
Dr :
                               XR (H) + ZD (H, f ) ≤ 1/4 + 1/4 = 1/2
for f ∈ {L, H}. The other high-horizontal case, with a low vertical copy, uses the empty high x-side
of Cr :
                               XR (L) + ZC (H, f ) ≤ 1/2 + 0 = 1/2.
Low horizontal copies contribute nothing. Hence every new x-load is at most 1/2, which is the
half-load property needed for the next round. The table records the same check for all four outputs.

                                                   24
                        output     mixed loads          X′             Y′            Z′
                                                                                       
                                     1/2 1/2                                      1/2 1/2
                           C                         (1, 0)     (1/2, 1/2)             
                                     1/2 1/2                                       0    0
                                                                                       
                                     1/2 1/2                                      1/2 1/2
                           R                       (1/2, 1/4)   (1/2, 1/2)             
                                     1/2 1/2                                      1/4 1/4
                                                                                       
                                     3/4 1/2                                      1/2 1/2
                           D                        (1, 3/4)    (1/2, 1/2)             
                                     3/4 1/2                                      1/4 1/4
                                                                                       
                                       1   1                                      1/2 1/2
                          M                        (1/2, 1/2)      (1, 1)              .
                                      1/2 1                                       1/2 1/2

   Every entry in the mixed-load column is at most one, so all four output profiles are feasible. The
remaining columns are exactly the required profile bounds. This proves the recursive step.

   At this point the geometric part of the recursion is complete: every profile needed at level r + 1
has been made from profiles at level r. What remains is to follow the total values around this loop.

Proposition 18. For every r ≥ 1, there is a feasible profile Mr on Pr with XMr (s) ≤ 1/2 for every
x-slot s and with normalized value
                                                 5 30r + 55 + 5(−1)r
                                          mr =     −                 .
                                                 4        2r+5
Proof. Begin with the profiles from Lemma 16 and apply Lemma 17 repeatedly. The values satisfy

                            mr + 5/8                    dr  15                      rr + 5/8 + dr
                   rr+1 =            ,         dr+1 =      + ,           mr+1 =                   ,
                               2                        2   32                            2
with m1 = r1 = d1 = 0. The second recurrence gives
                                                      
                                         15          1
                                    dr =      1 − r−1 .
                                         16        2

Combining this with rr = (mr−1 + 5/8)/2 gives the two-step recurrence2
                                                1       15   15
                                          mr+1 = mr−1 +    − r+4 .
                                                4       16 2
It remains only to check the closed form. The displayed formula for mr holds at r = 1 and r = 2,
and substituting it into this two-step recurrence gives the same formula at level r + 1. The X-load
bound is part of the M -profile bounds.

    Finally, the point of the M -profile is that it can be used uniformly in the next crossbar. This
also gives us the lower bound.
   2
    The two-step form has a simple meaning in the profile loop. The carrier profile M does not make the next carrier
directly: it first passes through the helper profile R, and that R is used one round later to build a new M . Thus, after
dr has been written explicitly, the values of M advance by two levels at a time. The even and odd levels approach the
same limit along slightly different tracks; this is the source of the alternating term in the displayed formula.




                                                           25
Proposition 19. For every r ≥ 1,
                                   α∗ (Pr+1 )  5 30r + 55 + 5(−1)r
                                              ≥ −                  .
                                   ν(Pr+1 )    2        2r+4
Consequently,
                                                        α∗ (Pr )  5
                                             lim inf             ≥ .
                                              r→∞       ν(Pr )    2
Proof. Place a copy of the profile Mr from Proposition 18 in every horizontal and every vertical
copy of Pr inside Pr+1 = C(Pr ). Local cliques are feasible. A mixed clique meets one horizontal
copy and one vertical copy, and each side contributes at most 1/2 to the relevant old x-slot class.
Hence every mixed clique has weight at most one.
   There are 2qr copies, each carrying total weight mr qr . Since qr+1 = qr2 , the total weight is
2mr qr+1 . By Proposition 11, ν(Pr+1 ) = qr+1 , so the ratio is at least 2mr , which is the displayed
bound.

     Since α∗ (Pr ) ≤ τ (Pr ) for rectangle families, this also gives
                                                         τ (Pr )  5
                                              lim inf            ≥ .
                                               r→∞       ν(Pr )   2
This proves the lower-bound half of Theorem 3. The next section gives the matching piercing sets,
showing that this recursive family cannot exceed 5/2.


10      The matching upper bound
The previous section built large fractional packings. We now show that the same recursive family
has piercing sets of the matching asymptotic size. The upper bound comes from using the same
lines that were built into the construction: all chosen points will be intersections of the vertical and
horizontal marker lines.
    For a rectangle R ∈ Pr , write Xr (R) and Yr (R) for the vertical and horizontal marker slots
contained in R. The marker-grid point (s, t) is the intersection of vertical marker s and horizontal
marker t, and it lies in R exactly when

                                       s ∈ Xr (R) and t ∈ Yr (R).

Thus a set S ⊆ [qr ] × [qr ] gives a piercing set for Pr if
                                                            
                                         S ∩ Xr (R) × Yr (R) ̸= ∅

for every R ∈ Pr .
    A well-chosen grid set can pierce one level. To pass to the next level, we keep one additional
piece of information: how many chosen points lie on each marker. If there are q vertical markers
and the target size is (5/2)q, then the average number of chosen points on a vertical marker is 5/2,
and the same average holds for the horizontal markers. Since these counts are integral, the natural
shape is that every marker carries either two or three chosen points, with the extra point assigned to
exactly half of the markers in each direction. For S ⊆ [q] × [q], define

                         dxS (s) = |{t : (s, t) ∈ S}|,        dyS (t) = |{s : (s, t) ∈ S}|.

These are the numbers of chosen grid points on a vertical marker and on a horizontal marker.

                                                         26
    At the next crossbar step, it matters which markers carry the third point. A horizontal copy and
a vertical copy must contribute the same number of local choices inside their common cell, so that
the choices can be paired. We therefore keep two patterns, allowing the third points to be placed on
one half of the markers or on the other half.
    The base case is small enough to see directly. The two patterns below each have ten chosen
entries. Rows are indexed by the vertical slot and columns by the horizontal slot:
                                                                      
                                   1 0 1 1                   1 0 0 1
                                 0 1 1 0                 1 1 1 0
                         M0 =   1 1 1 0 ,
                                                   M1 =  0 1 0 1 .
                                                                         

                                   1 0 0 1                   0 1 1 1

Let S0δ be the set of entries equal to one in M δ .

                                             S00                             S01
                                    0        1          2   3            0   1     2        3

                               0                                     0

                               1                                     1

                               2                                     2

                               3                                     3



Figure 9: The two base marker-grid patterns. A dot in row s and column t means that the marker-grid
point (s, t) is chosen.

    Figure 10 places both patterns directly on the base drawing. The same dots appear in Figure 9;
the geometric picture shows them as points in the plane, while the grid picture records the row and
column counts. Each panel should be read separately: either one of these two dot sets is already a
piercing set.

                              S00                                                               S01


          3                   T                                          3                      T


          2         UL                  UR                               2         UL                     UR




          1          C1                 C2                               1             C1                 C2

                                                   C3                                                          C3
               C0                                                             C0
          0                                                              0
                              Q                                                                 Q

               0          1         2               3                         0             1         2         3


Figure 10: Both base marker-grid patterns placed on the base drawing, shown in separate panels.
Each panel is a piercing set for the eight base rectangles.

                                                                27
    The patterns must also meet the rectangles while keeping the right row and column counts. The
full check is short; one possible choice of a point for each rectangle is

                                      R point in S00 point in S01
                                      T    (0, 3)       (0, 3)
                                      UL   (0, 2)       (1, 2)
                                      UR   (2, 2)       (3, 2)
                                      C0   (0, 0)       (0, 0)
                                      C1   (1, 1)       (1, 1)
                                      C2   (2, 1)       (2, 1)
                                      C3   (3, 0)       (3, 1)
                                      Q    (2, 0)      (1, 0).

Each displayed point lies in X0 (R) × Y0 (R). If

                                            ε0 (s) = s         (mod 2),

then the row and column counts of the two patterns satisfy

                                     dxS δ (s) = dyS δ (s) = 2 + 1ε0 (s)=δ .
                                        0            0


Thus every row and every column contains either two or three chosen points, and exactly half of the
slots receive the third point.
    The recursive statement is the following.

Lemma 20. For every r ≥ 0, there is a balanced map

                                              εr : [qr ] → {0, 1},

where balanced means that each value occurs qr /2 times. There are also two marker-grid piercing
sets Sr0 , Sr1 ⊆ [qr ] × [qr ] such that, for every s ∈ [qr ] and δ ∈ {0, 1},

                                     dxS δ (s) = dyS δ (s) = 2 + 1εr (s)=δ .
                                        r            r


In particular, |Srδ | = (5/2)qr .

    The proof idea is to build the next pattern cell by cell. Consider one cell in the next crossbar
arrangement, where a horizontal copy Hi meets a vertical copy Vj . A point chosen in the horizontal
copy has local form (j, b): it uses outer column j and an old horizontal slot b. A point chosen in the
vertical copy has local form (i, t): it uses outer row i and an old horizontal slot t after the coordinate
swap. A new marker-grid point inside that cell records both local choices by

                                    (j, b), (i, t)       7−→     ((j, t), (i, b)).

The figure records this pairing step. The proof will choose the two old patterns in each copy so that
the available (j, b) choices and (i, t) choices come in equal numbers for every pair (i, j); once that
happens, any bijection gives the needed marker-grid points.




                                                          28
                                                                                     new outer cell (j, i)
  from a horizontal copy Hi
      local point (j, b)
                                   pair b with t         new marker-grid point
                                  inside the cell            ((j, t), (i, b))    b                    inner (t, b)
   from a vertical copy Vj
      local point (i, t)
                                                                                                  t


Figure 11: How one paired local choice becomes a marker-grid point at the next level. In the new
grid, the outer coordinates are (j, i) and the inner coordinates are (t, b).

    The first repeated family shows the rule in action. The pairing rule produces forty marker-grid
points, shown in Figure 12 on the fatter realization from Figure 5. The inner coordinates in this
picture are old horizontal slots, whose marker positions are η = (1.4, 3.6, 7.5, 9.5). Thus the new
x-slot (j, t) is drawn at 30j + 5 + ηt , and the new y-slot (i, b) is drawn at 30i + 5 + ηb . This is the
coordinate rule from Figure 11, now placed directly on the rectangles.




                                                    29
               V0                       V1                       V2                       V3
                                                                                                        b



                                                                                                        3
                                                                                                        2
 H3                                                                                                     1
                                                                                                        0




                                                                                                        3
                                                                                                        2
 H2                                                                                                     1
                                                                                                        0




                                                                                                        3
                                                                                                        2
 H1                                                                                                     1
                                                                                                        0




                                                                                                        3
                                                                                                        2
 H0                                                                                                     1
                                                                                                        0




      t      0 1    2 3               0 1    2 3               0 1    2 3               0 1    2 3



Figure 12: The first recursive piercing pattern S10 overlaid on the fatter 64-rectangle drawing. The
black dots are the forty marker-grid points produced by the pairing rule; the dashed lines show the
marker-grid lines x = 30j + 5 + ηt and y = 30i + 5 + ηb , labelled by t below the drawing and by b on
the right.

    The picture suggests the induction. At each level there will again be two piercing patterns.
Numerically, what has to be preserved is the same two-or-three count on every vertical and horizontal
marker.
    Here and in the proof, ⊕ denotes addition modulo two. The pattern choices in the proof are
arranged so that, inside each cell (i, j), the horizontal and vertical sides receive their extra local
choice under the same condition, namely εr (i) ⊕ εr (j) = δ.



                                                   30
Proof. For r = 0, take ε0 (s) = s (mod 2). The witness table above shows that both displayed
patterns pierce P0 , and the row and column counts give the required formula for dx and dy .
    Assume the statement at level r, and put q = qr . Fix δ ∈ {0, 1}. The new pattern will be
assembled one pair of copies at a time. In the horizontal copy with index i, use the old pattern

                                               ϕi = δ ⊕ εr (i),

and in the vertical copy with index j, use the old pattern

                                               ψj = δ ⊕ εr (j).

   Fix a horizontal index i and a vertical index j. Let
                                                                                    ψ
                         Ai,j = {b : (j, b) ∈ Srϕi },        Bi,j = {t : (i, t) ∈ Sr j }.

The row and column counts give

                                |Ai,j | = 2 + 1εr (j)=ϕi = 2 + 1εr (i)⊕εr (j)=δ ,

and
                                |Bi,j | = 2 + 1εr (i)=ψj = 2 + 1εr (i)⊕εr (j)=δ .
Thus Ai,j and Bi,j have the same size. This equality is the point of the choices of ϕi and ψj : the
local choices available from the two copies have been counted by the same ⊕-condition and can
now be matched. Choose an arbitrary bijection βi,j : Ai,j → Bi,j . For each b ∈ Ai,j , put the new
marker-grid point                                              
                                         (j, βi,j (b)), (i, b)
       δ . Doing this over all choices of i and j defines S δ .
into Sr+1                                                   r+1
    The points are distinct. For a fixed pair (i, j), the values of b are distinct and the map βi,j is
injective. Points from different pairs have different outer coordinates.
    Now let Hi (R) be a horizontal rectangle in Pr+1 . The old pattern Srϕi pierces R, so it contains a
point (j, b) with j ∈ Xr (R) and b ∈ Yr (R). The paired point ((j, βi,j (b)), (i, b)) lies in Hi (R), because

                    Xr+1 (Hi (R)) = Xr (R) × [q],            Yr+1 (Hi (R)) = {i} × Yr (R).
                                                                                    ψ
For a vertical rectangle, use the same pairing in the other direction. If Sr j pierces R at a point (i, t),
then t ∈ Bi,j , so there is a b ∈ Ai,j with βi,j (b) = t. The resulting point ((j, t), (i, b)) lies in Vj (R),
using
                     Xr+1 (Vj (R)) = {j} × Yr (R),        Yr+1 (Vj (R)) = Xr (R) × [q].
        δ
Hence Sr+1 pierces every rectangle of Pr+1 .
   Define
                                    εr+1 (j, t) = εr (j) ⊕ εr (t).
                                       δ                                                      ψ
Fix a new x-slot (j, t). Its count in Sr+1 is the number of indices i for which (i, t) ∈ Sr j . By the old
count for the horizontal marker t, this is

                          2 + 1εr (t)=ψj = 2 + 1εr (j)⊕εr (t)=δ = 2 + 1εr+1 (j,t)=δ .

The calculation for a new y-slot (i, b) is identical, with i and b in place of j and t.
    Finally, εr+1 is balanced. For each fixed j, exactly half of the values of t make εr (j) ⊕ εr (t) equal
to zero, and half make it equal to one, because εr is balanced. This completes the induction.

                                                        31
   The size formula follows by summing the x-counts:
                                              X                            qr  5
                                  |Srδ | =             dxS δ (s) = 2qr +      = qr .
                                                         r                 2   2
                                             s∈[qr ]




    The same marker-grid patterns also explain why the number 5/4 is the ceiling for the reusable
half-load profiles from the previous section. The profiles Mr were built so that every x-slot carries
load at most 1/2. The piercing patterns show that this condition already imposes the right upper
bound on their possible total value.

Proposition 21 (The half-load bound). Let w be a nonnegative weighting on Pr such that Xw (s) ≤
1/2 for every x-slot s of Pr . Then w(Pr ) ≤ (5/4)qr .

Proof. Choose one of the marker-grid piercing sets Srδ from Lemma 20. For each rectangle of positive
weight, choose one point of Srδ that pierces it, and assign the rectangle to that point. This is possible
because Srδ pierces Pr .
    Fix a marker-grid point (s, t) ∈ Srδ . All rectangles assigned to this point contain the same point
of the plane, so they form a clique. They also all use the x-slot s. By the definition of Xw (s), the
total weight assigned to (s, t) is at most Xw (s) ≤ 1/2. Summing over the |Srδ | = (5/2)qr chosen
marker-grid points gives w(Pr ) ≤ (1/2)(5/2)qr = (5/4)qr .

    Thus the value reached in Proposition 18 is the largest possible asymptotic value for any half-load
weighting. When such a weighting is placed in both the horizontal and vertical copies at the next
crossbar step, this 5/4 ceiling becomes the 5/2 endpoint in Theorem 3.

Proposition 22. For every r ≥ 0,
                                                                5
                                                       τ (Pr ) ≤ qr .
                                                                2
Consequently,
                                   τ (Pr )   5                       α∗ (Pr )  5
                                           ≤                 and              ≤ .
                                   ν(Pr )    2                       ν(Pr )    2

Proof. By Lemma 20, either set Srδ gives (5/2)qr marker-grid points that pierce Pr . Thus τ (Pr ) ≤
(5/2)qr . By Proposition 11, ν(Pr ) = qr , giving the first ratio bound. The LP bound follows from
α∗ (Pr ) ≤ τ (Pr ).

Completion of Theorem 3. Proposition 19 gives

                                                             α∗ (Pr )  5
                                               lim inf                ≥ .
                                                 r→∞         ν(Pr )    2

Since α∗ (Pr ) ≤ τ (Pr ), this also gives

                                                             τ (Pr )  5
                                                lim inf              ≥ .
                                                  r→∞        ν(Pr )   2

The upper bounds in Proposition 22 give the reverse inequalities for both limsups. Therefore both
limits exist and equal 5/2.




                                                              32
11    Interpolation
We end with a small adjustment argument. The recursive families give ratios arbitrarily close to
5/2. If a desired rational value t is below 5/2, we may first choose a family whose ratio is above t,
and then lower the ratio by adding isolated rectangles. An isolated rectangle contributes one to the
packing number, one to the piercing number, and one to the fractional packing optimum. Thus it
has ratio exactly one, and adding many such rectangles lets us tune an existing ratio downward.
   We shall use this only for separated disjoint unions. If two families A and B are placed in far
apart regions of the plane, then
                                       ν(A ⊔ B) = ν(A) + ν(B),
                                      τ (A ⊔ B) = τ (A) + τ (B),
and
                                    α∗ (A ⊔ B) = α∗ (A) + α∗ (B).
For ν, maximum disjoint subfamilies from the two sides can be combined, and any disjoint subfamily
splits into its two parts. For τ , no point can hit rectangles on both sides once the two regions are
separated. For α∗ , every clique lies entirely in one side, so the clique relaxation splits into two
independent linear programs.

Proof of Theorem 4. Let X denote either α∗ or τ . We first consider a rational number t with
1 < t < 5/2. By Theorem 3, there is a member Pr of the recursive family such that

                                             X(Pr )
                                                    > t.
                                             ν(Pr )

For X = α∗ this follows directly from the first limit in Theorem 3; for X = τ it follows from the
second. Write
                                    a = ν(Pr ),    b = X(Pr ).
Here a is a positive integer. Also, b is rational: for X = τ it is an integer, and for X = α∗ it is the
optimum of a finite linear program with rational coefficients.
    Take M separated copies of Pr and add N further isolated rectangles, also placed far away from
all the copies and from one another. By the additivity just discussed, the resulting family has ratio
                                               Mb + N
                                                      .
                                               Ma + N
We want this to equal t. Solving for N gives
                                                    b − ta
                                           N =M            .
                                                     t−1
Since b/a > t and t > 1, the factor (b − ta)/(t − 1) is positive. It is also rational, so we choose M
large enough that N is a positive integer. Then the separated union R of these M copies of Pr and
these N isolated rectangles satisfies
                                             X(R)
                                                    = t.
                                             ν(R)
    Finally, the endpoint t = 1 is obtained by any nonempty family of pairwise disjoint isolated
rectangles. Applying the argument once with X = α∗ and once with X = τ proves both assertions.



                                                  33
12     Conclusion
Ajwani, Gajjala, Raman, and Ray [AGRR26] recently gave the first counterexample to Wegner’s
conjecture and the finite LP benchmark discussed above. The construction here takes that develop-
ment in a more compact and recursive direction. Its starting point is an eight-rectangle base whose
independent sets are controlled by a few ordered slots, while the geometry remains triangle-free.
The slot lists bound independent sets, the disjointness rules give the triangle-free 64-rectangle
arrangement, and the second list system carries the information needed for later recursive levels.
    This turns the 64-rectangle counterexample into the first level of a recursive family. The same
horizontal-vertical arrangement that proves Wegner’s conjecture false also creates the regularity
needed to support fractional weightings and to construct piercing sets. At the finite level, this gives a
clique-relaxation gap larger than the Ajwani-Gajjala-Raman-Ray benchmark. In the limit, the lower
and upper arguments meet: weights are controlled by slot loads, while piercing sets are controlled by
marker-grid pairings. Together they show that the recursive family has a precise limiting value,

                                       α∗ (Pr )       τ (Pr )  5
                                    lim         = lim         = .
                                   r→∞ ν(Pr )     r→∞ ν(Pr )   2

The interpolation argument then turns this limiting behavior into exact finite realizations of every
rational value below 5/2 as each of these two ratios.
    Several natural questions remain. On the packing-piercing side, Gyárfás and Lehel [GL85] asked
for a constant bound on τ (R)/ν(R) for rectangle families. The known lower side has moved from the
5/3 barrier of Fon-Der-Flaass and Kostochka [FDFK93], through the examples reported by Correa,
Feuilloley, Pérez-Lantero, and Soto [CFPLS15] with τ (R) = 2ν(R) − 4, past the first counterexample
of Ajwani, Gajjala, Raman, and Ray [AGRR26], and now to the limit 5/2 for the recursive family
constructed here. This value is the endpoint proved for our construction; the global supremum for
all rectangle families remains open. Known general upper bounds are still much larger, with the
current line including the O(ν(R)(log log ν(R))2 ) bound of Correa, Feuilloley, Pérez-Lantero, and
Soto [CFPLS15].
    On the algorithmic side, the standard point relaxation for Maximum Independent Set of Rectangles
has long been tied to approximation algorithms, beginning with the framework of Chalermsook
and Chuzhoy [CC09]. Recent algorithms achieve better constant factors, including the (2 + ϵ)
approximation of Gálvez, Khan, Mari, Mömke, Reddy, and Wiese [GKM+ 21]. The lower bound here
shows that the standard point, equivalently clique, relaxation cannot by itself certify approximation
factors below 5/2. It would be interesting to determine the true integrality gap of this relaxation, to
find smaller finite examples with large gap, and to understand which parts of the crossbar mechanism
are essential.

AI usage acknowledgment The authors used OpenAI’s Codex to format parts of the text and
generate the figures. The final draft was reviewed by the authors.


References
[AES10]     Boris Aronov, Esther Ezra, and Micha Sharir. Small-size ϵ-nets for axis-parallel rectangles
            and boxes. SIAM Journal on Computing, 39(7):3248–3282, January 2010.

[AG60]      E. Asplund and B. Grünbaum. On a Coloring Problem. Mathematica Scandinavica,
            8:181–188, December 1960.


                                                   34
[AGRR26] Deepak Ajwani, Rishikesh Gajjala, Rajiv Raman, and Saurabh Ray. A Counterexample
         to Wegner’s Conjecture for Axis-Parallel Rectangles, 2026.

[CC09]     Parinya Chalermsook and Julia Chuzhoy. Maximum independent set of rectangles. In
           Proceedings of the Twentieth Annual ACM-SIAM Symposium on Discrete Algorithms,
           page 892–901. Society for Industrial and Applied Mathematics, Jan 2009.

[CCPW22] Marco Caoduro, Jana Cslovjecsek, Michał Pilipczuk, and Karol Węgrzycki. Independence
         number of intersection graphs of axis-parallel segments, 2022.

[CD20]     Ke Chen and Adrian Dumitrescu. On Wegner’s inequality for axis-parallel rectangles.
           Discrete Mathematics, 343(12):112091, December 2020.

[CFPLS15] José Correa, Laurent Feuilloley, Pablo Pérez-Lantero, and José A. Soto. Independent
          and hitting sets of rectangles intersecting a diagonal line: Algorithms and complexity.
          Discrete & Computational Geometry, 53(2):344–365, Jan 2015.

[CSZ17]    Maria Chudnovsky, Sophie Spirkl, and Shira Zerbib. Piercing axis-parallel boxes, 2017.

[FDFK93] D. G. Fon-Der-Flaass and A. V. Kostochka. Covering boxes by points. Discrete
         Mathematics, 120(1-3):269–275, September 1993.

[GKM+ 21] Waldo Gálvez, Arindam Khan, Mathieu Mari, Tobias Mömke, Madhusudhan Reddy,
          and Andreas Wiese. A (2 + ϵ)-approximation algorithm for maximum independent set
          of rectangles, 2021.

[GL85]     A. Gyárfás and J. Lehel. Covering and coloring problems for relatives of intervals.
           Discrete Mathematics, 55(2):167–180, July 1985.

[HD57]     H. Hadwiger and H. Debrunner. Über eine Variante zum Hellyschen Satz. Archiv der
           Mathematik, 8(4):309–313, October 1957.

[Ká91]     Gy. Károlyi. On point covers of parallel rectangles. Periodica Mathematica Hungarica,
           23(2):105–107, October 1991.

[Mit22]    Joseph S. B. Mitchell. Approximating maximum independent set for rectangles in the
           plane. In 2021 IEEE 62nd Annual Symposium on Foundations of Computer Science
           (FOCS), page 339–350. IEEE, February 2022.

[Tom23]    István Tomon. Lower bounds for piercing and coloring boxes. Advances in Mathematics,
           435:109360, December 2023.

[Weg65]    G. Wegner. Über eine kombinatorisch-geometrische Frage von Hadwiger und Debrunner.
           Israel Journal of Mathematics, 3(4):187–198, December 1965.




                                               35
A     Graph schematics for the first crossbar
This appendix records three schematic pictures for the first repeated family P1 = C(P0 ). The first
marks the crossings in the rectangle drawing, the second enlarges one crossing of each type, and the
third keeps only the graph structure that appears inside those crossings.
    Figure 13 repeats the compressed drawing of P1 from Figure 4. A crossing is one of the highlighted
squares where a horizontal copy strip and a vertical copy strip meet. These sixteen crossings are the
geometric source of the 4 by 4 board used in the graph schematic below.

                            V0              V1               V2              V3



                   H3




                   H2




                   H1




                   H0




Figure 13: The sixteen crossings in the first crossbar. Each highlighted square is where one horizontal
copy strip and one vertical copy strip meet.




                                                  36
    Figure 14 enlarges one crossing of each type. The type is determined only by the two slot-class
sizes |Xj | and |Xi |; these are the two numbers shown in the board and in the complete-join schematic
below.

                                      K3,3                           K3,4




                                    H0 with V0                     H1 with V0

                                      K4,3                           K4,4




                                    H0 with V1                     H1 with V1



Figure 14: Four enlarged crossings, one of each size type. The colors match the board colors used in
Figure 15.

   We now pass from the geometry of the highlighted crossings to the graph structure inside them.
For a slot a ∈ [4], write
                                Xa = {R ∈ P0 : a ∈ X(R)}.
In the part of the drawing where Hi (P0 ) crosses Vj (P0 ), the crossing rule says that the new edges
are exactly the complete bipartite graph between Hi (Xj ) and Vj (Xi ). Since |X0 | = |X3 | = 3 and
|X1 | = |X2 | = 4, only four sizes can occur. Here

      X0 = {C0 , UL , T },   X1 = {C1 , Q, UL , T },        X2 = {C2 , Q, UR , T },   X3 = {C3 , UR , T }.

The figure below colors the 4 by 4 board by these four types and then draws one representative
schematic for each type, recording each complete bipartite graph as a shaded block instead of drawing
all its edges. A labeled copy of F is included as a key for the small unlabeled copies. The yellow
vertices in the representative panels are the slot classes that form the complete join. We also mark
the independent set I0 = {T, UL , C0 , C2 } in red. In the representative panels the red mark is put
only on the horizontal side.




                                                       37
                                       crossings
                                 V0    V1    V2        V3

                          H3    3×3 4×3 4×3 3×3                                     base graph F

                                                                                              T
                          H2    3×4 4×4 4×4 3×4
                                                                                         UL       UR
                          H1    3×4 4×4 4×4 3×4
                                                                                         C1       C2
                          H0    3×3 4×3 4×3 3×3
                                                                                   C0                  C3

                               Hi (Xj ) joined to Vj (Xi )                                    Q




                                              K3,3                                K3,4
                                          complete                            complete
                                            join                                join

                                  |Xj | = 3          |Xi | = 3        |Xj | = 3          |Xi | = 4


                                              K4,3                                K4,4
                                          complete                            complete
                                            join                                join

                                  |Xj | = 4          |Xi | = 3        |Xj | = 4          |Xi | = 4



Figure 15: A schematic view of the complete bipartite pieces between horizontal and vertical copies
in P1 . Yellow marks the slot classes that are joined; red marks the base independent set on the
horizontal side.

    The red vertices give the matching lower-bound witness for α(P1 ) = 16. Take these four vertices
in each of the four horizontal copies and take no vertices from the vertical copies. The horizontal
copies are pairwise disjoint, and the chosen vertices are independent inside each copy of F , so this
gives an independent set of size 4 · 4 = 16. The opposite inequality is the board-counting argument
proved in Proposition 11; the schematic here is meant to make the witness and the complete joins at
the crossings visible.


B     One-copy profile checks
This appendix records the finite checks used in Section 8. The checks all take place inside P1 .
Since P1 is triangle-free, every clique is either a single rectangle or an edge. Thus, for each profile,
feasibility and the slot loads can be checked by inspecting vertices and edges.
    For a profile w on P1 , let Xw (b) denote the maximum of Xw (a, b) over the first digit a. The
profiles used for the first P2 gap have the following values and final-digit x-loads:

                    profile w(P1 ) maxK w(K) (Xw (0), Xw (1), Xw (2), Xw (3))
                      O       0        0                (0, 0, 0, 0)
                      A      14       1/2         (1/2, 1/2, 3/8, 1/4)
                      B      16       3/4         (1/2, 1/2, 1/2, 1/2)
                      C      26        1             (1, 1, 1/2, 1/2)
                      D      27        1             (1, 1, 5/8, 1/2)
                      E      28        1             (1, 1, 3/4, 1/2).

Here maxK w(K) is the maximum over cliques K of P1 ; in particular, each listed profile is feasible.



                                                                 38
   The reusable vector A2 uses the following four profiles:

                  profile w(P1 ) maxK w(K) (Xw (0), Xw (1), Xw (2), Xw (3))
                    R      13       1/2         (1/2, 1/2, 1/4, 1/4)
                    S      16        1          (1/2, 1/2, 1/2, 1/2)
                    U      10        1                (1, 1, 0, 0)
                    V      12        1              (1, 1, 1/2, 0).

   For U and V we also use y-loads and joint loads. For this table only, write
                          bw (b) = max{Zw ((a, b), t) : a ∈ [4], t ∈ [4]2 }.
                          Z

Then
                        profile maxt Yw (t) (Z
                                             bw (0), Z
                                                     bw (1), Zbw (2), Z
                                                                      bw (3))
                          U        1/2              (1/2, 1/2, 0, 0)
                          V        1/2            (1/2, 1/2, 1/4, 0).
These are exactly the bounds used in (8.4).




                                                 39
