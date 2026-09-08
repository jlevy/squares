                            The Center-Area Lemma
Three disjoint unit squares whose centers form a non-obtuse triangle span area at least 12

                                            David R. MacIver
                                           david@drmaciver.com



                                                  Abstract
          Let S1 , S2 , S3 be unit squares, rotated arbitrarily, with pairwise disjoint interiors, and
      let P1 , P2 , P3 be their centers. If the triangle P1 P2 P3 is non-obtuse, its area is at least 12 .
      The constant is attained, and the angle hypothesis is necessary: obtuse center triangles
      can have arbitrarily small area. The proof freezes one owned separating inequality per pair
      of squares, minimizes the area of the center triangle subject to the three frozen constraints,
      converts first-order optimality at the minimum into a reciprocal diagram of contact forces
      in Maxwell’s sense, and closes with an ownership tournament and two scalar inequalities.
      The proof is fully formalized in Lean 4, and the statement is independently confirmed by
      a second machine-checked proof. This paper was produced with a mix of ChatGPT and
      Claude Fable and has not yet been adequately human reviewed.


1    Introduction
Let s(n) denote the side of the smallest square that contains n unit squares with pairwise
disjoint interiors; for the state of the art on this packing problem see Friedman’s dynamic
survey [3], and for the asymptotic regime Erdős and Graham [1]. Lower bounds for s(n) are
counting arguments that track the centers of the packed squares, and their basic pairwise input
is one-dimensional: two centers lie at distance at least 1. The first genuinely two-dimensional
constraint concerns triples of centers, and its natural quantitative form is a lower bound on
the area of the center triangle. This paper proves the sharp such bound.
    Throughout, a unit square is a closed square of side 1, in any orientation, and a family
of unit squares is admissible if their interiors are pairwise disjoint. A triangle is non-obtuse
if all three of its angles are at most π/2; equivalently, for each vertex the squared length of
the opposite side is at most the sum of the squared lengths of the two adjacent sides. (The
formalization reported in Section 9 uses the squared-side-length form.)

Theorem 1.1 (Center-area lemma). Let S1 , S2 , S3 be unit squares in the plane, rotated
arbitrarily and independently, with pairwise disjoint interiors, and let P1 , P2 , P3 be their
centers. If △P1 P2 P3 is non-obtuse, then
                                                                 1
                                           area(P1 P2 P3 ) ≥     2.

    We record at once the pairwise fact used throughout.

Lemma 1.2 (center separation). The centers of two unit squares with disjoint interiors are at
distance at least 1.

Proof. Each unit square contains the open disk of radius 12 about its center in its interior. If
the centers were at distance less than 1, their midpoint would lie in both disks, so the interiors
would meet.



                                                       1
    The constant and the hypotheses are tight, in senses made precise in Section 8. The
constant is attained: three axis-parallel unit squares centered at three vertices of a unit
square are admissible with center triangle of area exactly 12 . The angle hypothesis cannot be
dropped: three axis-parallel squares in a row, the middle one slightly offset, give an obtuse
center triangle of arbitrarily small positive area. Without any angle hypothesis one still has
area(P1 P2 P3 ) ≥ 21 sin θ for every angle θ of the center triangle. And there is no four-center
analogue: four centers in strict convex position can span convex hulls of arbitrarily small area.
The theorem is also exactly the hard part of a natural three-center threshold governing when
three centers of admissible unit squares fit in a w × h rectangle: granted the elementary narrow-
rectangle regime of that threshold, its remaining wide branch is equivalent to Theorem 1.1, so
a first-principles proof of that branch would not bypass the lemma but reprove it.
    The proof runs by contradiction in four layers. Suppose some admissible triple has a
non-obtuse center triangle of area less than 12 , and write D0 < 1 for its doubled area. First,
freeze one separating branch per pair: the separating-axis theorem gives, for each pair of
squares, a separating direction that is, up to sign, a side normal of one of the two squares,
called the owner of the branch; the resulting separating inequality is linear in the two centers,
with fixed unit normal ni and fixed threshold Hi ≥ 1. Second, minimize the doubled area
D = 2 area(P1 P2 P3 ) over center triples satisfying the three frozen linear inequalities together
with non-obtuseness and D ≤ D0 ; the minimum exists, satisfies D ≤ D0 , and has all three
branch inequalities active. Third, first-order optimality at the minimum (a finite Farkas
argument) produces multipliers λi ≥ 0 whose contact forces fi = λi ni close into a triangle
congruent to the center triangle rotated a quarter turn, a reciprocal force diagram in Maxwell’s
sense, and Euler homogeneity converts multipliers into area at the minimum:

                                 2D = λ1 H1 + λ2 H2 + λ3 H3 ,

where each threshold has the explicit form H(t) = (1 + cos t + sin t)/2 ≥ 1, with t ∈ [0, π/4]
the angle between the orientations of the two squares reduced modulo quarter turns. Fourth,
ownership directs each edge of the center triangle away from its owner; a tournament on three
vertices is cyclic or transitive, and each case ends in a short scalar inequality (a symmetric
rational inequality in half-angle cotangents in the cyclic case, an explicit one-variable dual
certificate in the transitive case), forcing 2D ≥ 2 and contradicting D ≤ D0 < 1.
    One distinction governs the language of the entire paper: square contact versus active
frozen branch. The proof never shows that extremal squares touch, and it never moves or
rotates a square. For each pair, one valid separating inequality is selected at the outset and
kept fixed while the centers alone vary; throughout, contact (equivalently, an active branch)
means equality in one of these selected inequalities, never geometric tangency of squares.
    Sections 2–7 give the proof in the order of the plan: the branch formalism, the extremal
configuration, the reciprocal force system with its sine equations, the cyclic case, the transitive
case together with the origin of its certificate, and the assembly of the contradiction; Section 8
establishes sharpness, Section 9 reports the machine verification, and Appendix A proves the
cyclic scalar inequality.


2    Frames, separating branches, and ownership
The main proof replaces the disjointness of each pair of squares—a nonconvex condition—by a
single linear inequality between their centers. This section defines these inequalities (branches),
proves that disjoint squares always admit one whose normal is an axis of one of the two squares
(the owner, Lemma 2.2), and computes the threshold of such a branch: a function H(t) ≥ 1 of
the two frames alone (Lemma 2.3).



                                                2
                                                                2wG (n)
                                          2wF (n)


                                          n
                                                                       Q
                                               Q−P
                                   P



Figure 1: An oriented separating branch. The branch records only one-dimensional data: the
squares project onto the line in direction n to intervals of lengths 2wF (n) and 2wG (n) (support
lines dashed), and inequality (1) separates the interiors of these intervals, hence the interiors
of the squares.

Definition 2.1. A frame is an ordered orthonormal pair F = (e, f ) of vectors in R2 ; the four
unit vectors ±e, ±f are its axes. The unit square with frame F and center P is

                Q(F, P ) = X ∈ R2 : |(X − P ) · e| ≤ 12 , |(X − P ) · f | ≤ 21 .
                            

For a unit vector n, the projected half-width of F in direction n is
                                                    |n · e| + |n · f |
                                       wF (n) =                        ,
                                                            2
so that the orthogonal projection of Q(F, P ) onto a line in direction n is an interval of length
2wF (n) centered at the projection of P . An oriented separating branch for the squares Q(F, P )
and Q(G, Q) is the inequality

                 (Q − P ) · n ≥ H(F, G; n),               H(F, G; n) := wF (n) + wG (n),           (1)

specified by its unit normal n; the number H(F, G; n) is the threshold of the branch.

    A branch is a sufficient condition for disjoint interiors. A linear functional attains its
maximum over a square only on the boundary, so every X ∈ int Q(F, P ) satisfies (X − P ) · n <
wF (n), and every X ∈ int Q(G, Q) satisfies (Q − X) · n < wG (n); a point in both interiors
would give (Q − P ) · n < wF (n) + wG (n), contradicting (1). The condition is only sufficient: a
branch records nothing about the squares beyond their one-dimensional projections onto the
line in direction n (Figure 1).
    Disjointness does not supply an arbitrary branch: it supplies one of a special form.

Lemma 2.2 (Owned separating branch). Two unit squares with disjoint interiors admit an
oriented separating branch (1) whose normal is, up to sign, an axis of one of the two frames.

Proof. Write the squares as Q(F, P ) and Q(G, Q) and form the Minkowski sum K = Q(F, 0) +
Q(G, 0), which by central symmetry of the summands is also the Minkowski difference Q(F, 0)−
Q(G, 0). A point X lies in both interiors exactly when X = P + a = Q + b with a ∈ int Q(F, 0)
and b ∈ int Q(G, 0), that is, exactly when Q − P = a − b ∈ int K. Hence the interiors are
disjoint if and only if Q − P ∈
                              / int K.
    Since (e, f ) is an orthonormal basis, Q(F, 0) = [− 12 , 21 ] e + [− 21 , 12 ] f , and likewise for
Q(G, 0). Thus K is a Minkowski sum of four segments: a centrally symmetric convex polygon
(a zonogon) whose edges are parallel to the four axis directions of F and G. The outward
normal of an edge is a quarter turn of the edge direction, hence the other axis of the same frame;
so the facet normals of K are frame axes. Now K is the intersection of its facet half-planes

                                                      3
{x : x · n ≤ hK (n)}, with n ranging over the outward facet normals and hK (n) = maxx∈K x · n
the support function; so Q − P ∈   / int K forces (Q − P ) · n ≥ hK (n) for some facet normal
n. Support functions add under Minkowski sums, and maxx∈Q(F,0) x · n = wF (n); therefore
hK (n) = wF (n) + wG (n), and (1) holds with this n.

    When the normal of a branch is, up to sign, an axis of one of the two frames, we call
the square with that frame an owner of the branch. Lemma 2.2 says that every disjoint
pair admits an owned branch. The threshold of an owned branch has an explicit form, best
expressed through a notion of distance between frames. The set of axes of a frame is invariant
under rotation by π/2, so a frame determines a point of the circle R/(π/2)Z, its axis direction
modulo quarter turns. For frames F and G, let d4 (F, G) be the geodesic distance between the
corresponding points; it takes values in [0, π/4] and equals the least angle between an axis of
F and an axis of G.

Lemma 2.3 (Threshold of an owned branch). Let F = (e, f ) and G be frames and let n be a
unit vector.

  (i) If n is an axis of F , then wF (n) = 12 .

                                              |n · m| + |det(n, m)|
 (ii) If m is an axis of G, then wG (n) =                           ; in particular wG (n) ≥ 21 for
                                                        2
      every unit n.

(iii) If n is an axis of F and t = d4 (F, G), then

                                                      1 + cos t + sin t
                           H(F, G; n) = H(t) :=                         ≥ 1.                    (2)
                                                             2

Consequently the threshold of an owned branch depends only on the two frames, not on which
frame supplies the axis: whether n is an axis of F or of G, the threshold equals H(d4 (F, G)).

Proof. (i) If n = ±e then |n · e| = 1 and |n · f | = 0; symmetrically for n = ±f .
   (ii) The axes of G are ±m and ±m′ , where         m′ is a quarter turn of                 ′
                                                                            m; then |n · m | =
                                            ′
                                              
|det(n, m)|, so wG (n) = |n · m| + |n · m | /2 = |n · m| + |det(n, m)| /2. (The formula is
independent of the choice of axis m: replacing m by m′ swaps the two terms.) The numbers
a = n · m and b √= n · m′ are the coordinates of n in an orthonormal basis, so a2 + b2 = ∥n∥2 = 1
and |a| + |b| ≥ a2 + b2 = 1, giving wG (n) ≥ 12 .
   (iii) Choose an axis m of G at angle t = d4 (F, G) from n; then |n · m| = cos t and
|det(n, m)| = sin t, so by (i) and (ii)

                                                      1 cos t + sin t
                   H(F, G; n) = wF (n) + wG (n) =       +             = H(t).
                                                      2       2
On [0, π/4] we have cos t + sin t > 0 and (cos t + sin t)2 = 1 + sin 2t ≥ 1, so cos t + sin t ≥ 1
and H(t) ≥ 1.
   The final claim follows from (2) and the symmetry of d4 .

   By (2), ownership carries no metric information: an owned branch has the same threshold
whichever square owns it. Ownership matters for a discrete reason. Two branches owned by
the same square use two axes of a single frame, so their normals are, up to sign, parallel or
perpendicular. This fact closes the transitive case of the main argument.




                                                  4
3      Freezing the branches: the extremal configuration
The proof of Theorem 1.1 is by contradiction: we assume a configuration of admissible squares
whose non-obtuse center triangle has doubled area less than 1. Disjointness is an awkward
condition to minimize over, but each pair of squares certifies its disjointness by an owned
branch (Lemma 2.2), which is a single linear inequality in the centers. We freeze one such
branch per pair and minimize the area of the center triangle subject to the three frozen
inequalities alone. This section constructs the resulting extremal configuration: the minimum
exists, is acute, and has doubled area strictly between 0 and 1; and at the minimum all three
branch inequalities are equalities. The remainder of the proof works exclusively with this
minimizer.

3.1     The minimum exists
Assume, then, that Theorem 1.1 fails: there are admissible unit squares S1 , S2 , S3 whose
centers P1 , P2 , P3 form a non-obtuse triangle with

                                  D0 = 2 area(P1 P2 P3 ) < 1.

By Lemma 1.2 the centers are pairwise at distance at least 1, hence distinct; and three distinct
collinear points give the middle one an angle of π, contradicting non-obtuseness. The centers
are therefore noncollinear, so D0 > 0. Write D = 2 area(P1 P2 P3 ) for the doubled area of a
center triple and

      σ = sign det(P2 − P1 , P3 − P1 ) ∈ {−1, 1},      D = σ det(P2 − P1 , P3 − P1 ) > 0,

evaluated at the original configuration. The sign σ is retained from this configuration through-
out: in the minimization below the objective is the signed determinant σ det(P2 − P1 , P3 − P1 ),
constrained to be nonnegative, and D denotes this quantity.
    Compactness of the feasible set will come from an a priori bound on the sides of feasible
triangles, which rests on one elementary fact about triangles that are non-obtuse, have long
sides, and small area.

Lemma 3.1 (Subcritical triangles). Let XY Z be a triangle that is non-obtuse    √ and has all
sides of length at least 1. Then every altitude of XY Z has length√at least 1/ 2. If moreover
its doubled area is less than 1, then every side has length less than 2 and the triangle is acute.

Proof. Consider the altitude from a vertex A to the opposite side. Since the two base angles
are at most π/2, the foot lies on the side itself, not on its extension. Take coordinates with the
foot at the origin and A = (0, h), h > 0 the altitude, so the base endpoints are B = (−x, 0)
and C = (y, 0) with x, y ≥ 0. The adjacent sides have length at least 1: x2 + h2 ≥ 1 and
y 2 + h2 ≥ 1. The angle at A is at most π/2:

                             0 ≤ (B − A) · (C − A) = −xy + h2 ,

so h2 ≥ xy. If h2 < 21 , then x2 ≥ 1 − h2 > 12 > h2 forces x > h, and likewise y > h, whence
                                          √
xy > h2 , a contradiction. Hence h ≥ 1/ 2.
    Now suppose the doubled area D satisfiesD√ < 1. Each
                                                       √ side times its corresponding altitude
equals D, so each side has length D/h < 1 (1/ 2) = 2. Finally, if some angle were exactly
π/2, the two sides adjacent to it would be legs of length at least 1, giving D = leg × leg ≥ 1.
So every angle is strictly less than π/2.




                                                5
                                                 P3
                                                           n2

                                                                d2
                                    n3 d3
                                                      n1

                                                d1                   P2
                               P1

Figure 2: The frozen system: cyclic edges d1 , d2 , d3 and branch normals n1 , n2 , n3 . Each
branch is a linear inequality (3) in the centers and remains sufficient for separation as the
centers move. The normals are axes of the frozen frames, not functions of the edges, and need
not align with them.

The freeze. For the pairs (S1 , S2 ), (S2 , S3 ), (S3 , S1 ), Lemma 2.2 supplies owned separating
branches. Orient them cyclically: choose the sign of each normal so that the branch for
(Si , Si+1 ) reads off the difference Pi+1 − Pi (the threshold is unchanged, since projected half-
widths are even in the normal). This yields unit normals n1 , n2 , n3 and thresholds H1 , H2 , H3 ,
and for each branch we fix once and for all one owner: a square whose frame has the normal
as an axis. By Lemma 2.3 and (2), each Hi ≥ 1. Now freeze all of this data: frames, normals,
thresholds, and owners are constants from here on. Only the centers vary, subject to

          (P2 − P1 ) · n1 ≥ H1 ,      (P3 − P2 ) · n2 ≥ H2 ,          (P1 − P3 ) · n3 ≥ H3 .   (3)

With the cyclic edges d1 = P2 − P1 , d2 = P3 − P2 , d3 = P1 − P3 (so d1 + d2 + d3 = 0), the
system (3) reads di · ni ≥ Hi for i = 1, 2, 3.
    Two features of (3) carry the whole construction. First, the system remains sufficient for
separation as the centers move: a branch certifies disjoint interiors from projection data of the
two frames alone, and the frames are frozen, so any center triple satisfying (3) yields three
admissible squares. The original configuration is one solution among many; we are free to
minimize. Second, the normals ni are axes of the frozen frames and have no relation to the
edges di beyond the inequalities themselves: ni need not be parallel or perpendicular to di ,
and Figure 2 draws them askew deliberately.

The minimization problem. Branches and area depend only on differences of centers, so
we normalize P1 = 0. Over (P2 , P3 ) ∈ R2 × R2 , minimize

                                     σ det(P2 − P1 , P3 − P1 )

subject to the three branch inequalities (3), the three non-obtuseness inequalities (for each
vertex, the square of the opposite side is at most the sum of the squares of the adjacent sides),
and 0 ≤ D ≤ D0 .

Lemma 3.2 (Existence and geometry of the minimum). The minimum is attained. Every
minimizing configuration satisfies 0 < D ≤ D0 < 1, and its center triangle is acute.

Proof. We show the feasible set is nonempty and compact, and that Lemma 3.1 applies
uniformly across it.
    Nonempty. The original centers, translated so that P1 = 0, are feasible: they satisfy (3)
because the branches were constructed from them, they are non-obtuse by hypothesis, and
their signed determinant is D0 .

                                                6
   Every feasible triple is a subcritical triangle. Let (P2 , P3 ) be feasible. By Cauchy–Schwarz
and (3), with indices cyclic,

                          ∥Pi+1 − Pi ∥ ≥ (Pi+1 − Pi ) · ni ≥ Hi ≥ 1,

so all three sides are at least 1; in particular the centers are distinct. They are also noncollinear:
for three distinct collinear points, the two edge vectors at the middle point are opposite in
direction, so their inner product is negative and the non-obtuseness inequality at that point
fails. This holds at every feasible point, not merely the original one. Noncollinearity makes
the determinant nonzero, so the constraint 0 ≤ D ≤ D0 tightens to 0 < D ≤ D0 < 1, and D
is the doubled area of the triple. Lemma    √ 3.1 now applies throughout the feasible set: every
feasible triangle has all sides less than 2 and is acute.
√ Compactness. With P1 = 0, the side bounds confine P2 and P3 to the closed ball of radius
  2. The constraints are finitely many non-strict polynomial inequalities, so the feasible set is
closed, hence compact, and nonempty; the continuous objective attains its minimum.
    At a minimizer, feasibility gives 0 < D ≤ D0 < 1 and, by Lemma 3.1 again, acuteness.

   From now on the minimizing configuration means a fixed minimizer from Lemma 3.2; the
symbols Pi , di , D refer to its data, while the frames, normals ni , thresholds Hi , and owners
remain the frozen data of the original counterexample.

3.2    Complete contact
At the minimizing configuration, call a frozen branch active if its inequality in (3) holds with
equality. Activity is equality in a linear inequality on centers and nothing more: it does not
assert that the squares touch, and no square is moved or rotated anywhere in the argument.
This subsection proves that all three branches are active, so that the first-order optimality
analysis to come has all three constraints to work with. The obstruction to descent at a vertex
comes from its active branches only, and the dual description of a single half-plane is the key.

Lemma 3.3 (Half-plane duality). Let n ∈ R2 be a unit vector and let g ∈ R2 satisfy g · v ≥ 0
for every v with n · v ≥ 0. Then g = µn with µ ≥ 0.

Proof. If v ⊥ n then both ±v satisfy n · (±v) = 0 ≥ 0, so g · v ≥ 0 and g · (−v) ≥ 0,
forcing g · v = 0. Thus g is orthogonal to n⊥ , so g = µn for some µ ∈ R, and v = n gives
µ = g · n ≥ 0.

   Two preliminaries make single-vertex variations available. First, the area gradient. Let Jσ
denote rotation through σπ/2, so that Jσ2 = −I and ⟨Jσ u, v⟩ = σ det(u, v). When one vertex
P moves and the other two stay fixed, D is an affine function of P ; its gradient g is the quarter
turn of the opposite edge. Indeed, as a function of P3 ,

                          D = σ det(d1 , P3 − P1 ) = ⟨Jσ d1 , P3 − P1 ⟩,

with gradient Jσ d1 ; as a function of P2 the gradient is −Jσ (P3 − P1 ) = Jσ d3 ; and since D is
translation invariant the three gradients sum to zero, so the gradient in P1 is Jσ d2 . In every
case
                          ∥g∥ = length of the edge opposite P ≥ 1,
the bound being that edge’s own frozen branch together with Cauchy–Schwarz, as in the proof
of Lemma 3.2. Second, the normalization P1 = 0 does not forbid varying P1 : after moving P1 ,
translate all three centers back so that P1 = 0 again. The system (3) and the area depend
only on differences of centers, so feasibility and objective value are unchanged.


                                                  7
Lemma 3.4 (Complete contact). At the minimizing configuration, all three inequalities of (3)
hold with equality: di · ni = Hi for i = 1, 2, 3.

Proof. Form the graph on {P1 , P2 , P3 } in which the branch for a pair, if active, joins its two
vertices; we rule out any vertex of active degree 0 or 1, and since a graph on three vertices
with at most two edges has such a vertex, the graph must be complete. Suppose then that
some vertex P has active degree at most 1, and let g be the gradient of D in P , so ∥g∥ ≥ 1.
Figure 3 shows the two cases.
    Active degree 0. Both branches incident to P have positive slack. Move P to P − tg for
small t > 0: the incident branches are affine in P and keep positive slack, and the third branch
does not involve P . Since D is affine in P ,

                                   D(P − tg) = D − t∥g∥2 ,

which is strictly smaller. For small t the remaining constraints persist: acuteness and D > 0
are open conditions satisfied at the minimizer (Lemma 3.2), and D ≤ D0 persists because D
decreased. This produces a feasible configuration of smaller objective, contradicting minimality.
    Active degree 1. Let the unique active branch incident to P join P to Q, and orient its
normal locally so that it reads (P − Q) · n ≥ H: here H is its frozen threshold, and n is the
frozen normal or its negative, whichever makes the frozen inequality take this form. Activity
says (P − Q) · n = H. Consider any velocity v of P with n · v ≥ 0. Moving P to P + tv
preserves the active branch, since (P + tv − Q) · n = H + t n · v ≥ H; the inactive branch at P
tolerates small motions by positive slack; the third branch does not involve P . If g · v < 0, then
D strictly decreases along this motion, and exactly as in the previous case the open conditions
and the upper bound D ≤ D0 persist for small t, contradicting minimality. Hence g · v ≥ 0 for
every v with n · v ≥ 0, and Lemma 3.3 gives g = µn with µ ≥ 0; since ∥g∥ ≥ 1 and ∥n∥ = 1, in
fact µ ≥ 1.
    With the other two vertices fixed, the map sending a position X of P to the resulting value
of D is affine with gradient g. It takes the value D at X = P , and it takes the value 0 when
X is placed at either of the other two vertices, because the triangle then degenerates and the
determinant vanishes. For an affine function the gradient pairs with a difference of arguments
to give the difference of values, so

                  g · (P − Q′ ) = D − 0 = D          for either other vertex Q′ .

Both vertices qualify, so in particular Q′ = Q, the vertex the active branch joins to P , whichever
of the two it is. Setting r = P − Q, activity gives n · r = H, and therefore

                               D = g · r = µ n · r = µH ≥ 1,

since µ ≥ 1 and H ≥ 1 by (2). This contradicts D ≤ D0 < 1 (Lemma 3.2). Neither degree
0 nor degree 1 can occur, so every vertex has active degree 2 and all three branches are
active.

    Remark (where first-order feasibility is used). Both cases of the proof rest on the same
principle. Take a velocity v at a single vertex that weakly relaxes every active branch there,
meaning n · v ≥ 0 for each locally oriented active normal n. Along the ray P + tv, t > 0 small,
those affine inequalities continue to hold, and every inactive branch stays satisfied by positive
slack. Because the minimizing triangle is acute with 0 < D < 1, the strict conditions D > 0
and acuteness are open and persist, and whenever the area derivative g · v is negative the
bound D ≤ D0 persists as well. So a feasible velocity with negative area derivative yields a
genuinely smaller feasible configuration, which minimality forbids.


                                                8
                                                                    n
                                                                             g = µn
                                P                                    P
                                                                             n·v =0
                               −g


                                    P3                                          P3
                     P1                                       P1
                      active degree 0:                          active degree 1:
                move down the area gradient           the gradient lies on the normal ray

Figure 3: The two ways contact could fail at a vertex P . With no active incident branch, P
moves down the area gradient. With exactly one, first-order minimality over the half-plane
n · v ≥ 0 forces the gradient onto the normal ray, g = µn with µ ≥ 1, and then D = µH ≥ 1.


4      The reciprocal triangle and the sine system
At the minimizing configuration of Lemma 3.2 all three frozen branches are active (Lemma 3.4).
We now convert this first-order information into the central object of the proof: nonnegative
multipliers λ1 , λ2 , λ3 whose forces fi = λi ni close into a quarter-turned copy of the center
triangle, together with the identity 2D = λ1 H1 + λ2 H2 + λ3 H3 . Dotting the force equations
with the normals then reduces the geometry to three scalar equations, whose case analysis
occupies the rest of the paper.
    Throughout we work at the minimizing configuration, with the normalization P1 = 0
in force. Write d1 = P2 − P1 , d2 = P3 − P2 , d3 = P1 − P3 for the cyclic edges, so that
d1 + d2 + d3 = 0 and D = σ det(d1 , d2 ). Let Jσ denote rotation through σπ/2; we use exactly
two facts about it:
                            Jσ2 = −I     and      Jσ u · v = σ det(u, v).
Complete contact says that each frozen inequality of (3) holds with equality,

                              di · ni = Hi ,    Hi ≥ 1      (i = 1, 2, 3),

the lower bound because each frozen branch is owned (Lemma 2.3).

4.1     Farkas multipliers and the reciprocal triangle
First-order optimality under linear constraints is a finite Farkas statement [2]. We isolate the
version we need; the strict dual vector in hypothesis (i) is what makes the generated cone
closed, and our minimization problem supplies it for free.

Lemma 4.1 (Finite Farkas lemma). Let a1 , . . . , am and g be vectors in a Euclidean space.
Suppose

    (i) there is a vector w with ai · w > 0 for every i;

 (ii) every v with ai · v ≥ 0 for all i satisfies g · v ≥ 0.

Then g = m
          P
             i=1 λi ai for some λ1 , . . . , λm ≥ 0.
                    P
Proof. Let K = { i λi ai : λi ≥ 0}, the convex cone    P generated by the ai . We first show K is
closed. Set c = minP   a
                     i i · w > 0 and   suppose   x k =  i λi,k ai → x with all λi,k ≥ 0. Dotting with
w gives xk · w ≥ c i λi,k , and the left side converges, so the coefficient sums are bounded.


                                                  9
The coefficient vectors (λ1,k , . . . , λm,k ) therefore have a convergent subsequence, whose limit is
a nonnegative coefficient vector representing x. Hence x ∈ K.
    Now suppose g ∈  / K. Separating the point g from the closed convex set K yields v and β
with x · v ≥ β for all x ∈ K and g · v < β. Since 0 ∈ K, β ≤ 0. If some x0 ∈ K had x0 · v < 0,
then tx0 ∈ K for all t > 0 and tx0 · v → −∞, contradicting the lower bound; so x · v ≥ 0 on
all of K. In particular ai · v ≥ 0 for every i, yet g · v < β ≤ 0, contradicting (ii).

   We apply the lemma in explicit coordinates. With P1 = 0, let x = (P2 , P3 ) ∈ R4 and define
the branch functions
              b1 (x) = P2 · n1 ,       b2 (x) = (P3 − P2 ) · n2 ,       b3 (x) = (−P3 ) · n3 ,
so that the frozen inequalities (3) read bi (x) ≥ Hi . Each bi is linear in x — not merely affine
— and this is the point of the normalization P1 = 0: linearity is used twice below, once for the
strict dual vector and once for Euler homogeneity. The gradients are the constant vectors
                      a1 = (n1 , 0),        a2 = (−n2 , n2 ),        a3 = (0, −n3 ),
and we write g for the gradient at the minimizer of the objective x 7→ σ det(P2 , P3 ), the
doubled signed area, whose value there is D.
     We check the two hypotheses of Lemma 4.1. For (ii), let v ∈ R4 satisfy ai · v ≥ 0 for
i = 1, 2, 3. By linearity, bi (x + tv) = bi (x) + t ai · v ≥ Hi for all t ≥ 0, so the three branch
constraints hold along the entire ray. Acuteness (Lemma 3.2) and D > 0 hold strictly at the
minimizer, so both persist for small t > 0. If g · v < 0, then for small t > 0 the point x + tv
is still acute, still has positive doubled area, and has strictly smaller objective value — in
particular still at most D0 — so it is feasible and beats the minimum. This contradiction shows
g · v ≥ 0. For (i), take w = x itself, the uniform dilation direction: linearity gives ai · x = bi (x),
and complete contact gives bi (x) = Hi ≥ 1 > 0. Lemma 4.1 therefore produces
                           g = λ1 a1 + λ2 a2 + λ3 a3 ,          λ1 , λ2 , λ3 ≥ 0.
Define the forces fi = λi ni .
   The multiplier equation lives in R4 ; we resolve it into plane components. From ∇a det(a, b) =
−Jb and ∇b det(a, b) = Ja,Pthe gradient of σ det(P2 , P3 ) has components ∇P2 = −Jσ P3 and
∇P3 = Jσ P2 . Reading g = i λi ai in the two components:
             −Jσ P3 = λ1 n1 − λ2 n2 = f1 − f2 ,            Jσ P2 = λ2 n2 − λ3 n3 = f2 − f3 .
Since P1 = 0 we have d1 = P2 and d3 = −P3 , so these are the first and third of the equations
                    Jσ d1 = f2 − f3 ,          Jσ d2 = f3 − f1 ,      Jσ d3 = f1 − f2 ,            (4)
and the middle one follows from d1 + d2 + d3 = 0, since the three right-hand sides also sum to
zero; the vanishing of both sums is the consistency check on the resolution.
     Equations (4) say that f1 , f2 , f3 are the vertices of a triangle whose sides are the sides of
the center triangle rotated through a quarter turn, while each vertex fi lies on the ray from
the origin through the frozen normal ni , at distance λi (Figure 4). This is a reciprocal diagram
in Maxwell’s classical sense [6]: the multipliers are contact forces along the frozen normals,
and the force polygon closes. This quarter-turned copy of the center triangle, pinned to the
three normal rays, is the central object of the proof.
     The multipliers convert area into thresholds. The objective is homogeneous of degree 2 in
x and each bi is homogeneous of degree 1 — the second use of linearity. Euler’s identity gives
g · x = 2D, and ai · x = bi (x) = Hi at contact, so
                                        3
                                        X
                        2D = g · x =           λi ai · x = λ1 H1 + λ2 H2 + λ3 H3 .                 (5)
                                         i=1


                                                      10
                                P3               f2 = λ2 n2
                                                                     Jσ d3
                           d3                       Jσ d1                    f1 = λ1 n1
                                       d2
                      P1                                       O Jσ d2
                                            f3 = λ3 n3
                                d1          P2              force plane
                           center plane

Figure 4: The reciprocal diagram. Left: the center triangle with cyclic edges d1 , d2 , d3 . Right:
the force plane. The points fi = λi ni lie on the rays spanned by the frozen normals, and by
(4) the sides of the triangle f1 f2 f3 are the quarter-turned edges Jσ di .


Since 0 < D ≤ D0 < 1 at the minimizer, the remaining task of the entire paper is to prove
λ1 H1 + λ2 H2 + λ3 H3 ≥ 2: by (5) this forces D ≥ 1, the desired contradiction.

4.2    The sine system and the owner tournament
The reciprocal equations are vector equations; the case analysis needs scalars. Dotting with
the normals produces them. Define the oriented sines

               s1 = σ det(n1 , n2 ),         s2 = σ det(n2 , n3 ),        s3 = σ det(n3 , n1 ).

Since Jσ2 = −I, the first equation of (4) is equivalent to d1 = Jσ (f3 − f2 ). Dot with n1 , use
Jσ u · v = σ det(u, v), and use the contact equality d1 · n1 = H1 :

      H1 = d1 · n1 = Jσ (f3 − f2 ) · n1 = λ3 σ det(n3 , n1 ) − λ2 σ det(n2 , n1 ) = λ2 s1 + λ3 s3 .

The second and third equations yield, in identical fashion, the other two lines of the sine
system
            H1 = λ2 s1 + λ3 s3 ,   H2 = λ3 s2 + λ1 s1 ,    H3 = λ1 s3 + λ2 s2 .          (6)
    One case dies immediately.
Proposition 4.2 (Nonpositive sine). If si ≤ 0 for some i, then λ1 + λ2 + λ3 ≥ 2, and
consequently λ1 H1 + λ2 H2 + λ3 H3 ≥ 2.
Proof. The oriented sine of two unit vectors lies in [−1, 1]; in particular every si ≤ 1. Suppose
first s3 ≤ 0. In the first equation of (6) drop the nonpositive term λ3 s3 and bound s1 by 1:

                                     H1 = λ2 s1 + λ3 s3 ≤ λ2 s1 ≤ λ2 .

In the second, bound both sines by 1: H2 = λ3 s2 + λ1 s1 ≤ λ1 + λ3 . Since H1 , H2 ≥ 1 this
P λ2 ≥ 1Pand λ1 + λ3 ≥ 1, hence λ1 + λ2 + λ3 ≥ 2. As every Hi ≥ 1 and every λi ≥ 0,
gives
   i λi Hi ≥   i λi ≥ 2. The cases s1 ≤ 0 and s2 ≤ 0 reduce to this one by cyclic relabeling:
shifting the vertex labels cyclically shifts every index by one, leaves σ unchanged, and preserves
the displayed form of (6) (see the relabeling conventions at the end of this section).

Standing assumption. From here through Section 6 we assume s1 , s2 , s3 > 0. The three
normals then occur in positive cyclic order: each consecutive pair (n1 , n2 ), (n2 , n3 ), (n3 , n1 ) is
positively oriented for the orientation σ.
   The surviving case is organized by ownership. The freeze of Section 3 fixed, for each pair of
squares, a branch and a choice of its owner. Direct each edge of the center triangle away from

                                                      11
the owner of its branch. The result is a tournament on three vertices, and a tournament on
three vertices has exactly two forms up to isomorphism: a directed 3-cycle, or a transitive order
with a source S of out-degree 2, a middle vertex M , and a sink T of in-degree 2 (Figure 5).
There are eight possible owner assignments — the fixed owner of each branch is one or the
other square of its pair — and cyclic relabeling together with reflection reduces them to these
two geometries. Section 5 closes the cyclic case, in which the normals wind once around
the circle. Section 6 closes the transitive case, in which the source owns two branches and
one frame supplies two perpendicular normals. Section 7 assembles the three cases into the
contradiction.

                               3                                 T




                      1                   2           S                       M
                          cyclic owners                   transitive owners

Figure 5: The two owner tournaments on three vertices, up to cyclic relabeling and reflection:
a directed cycle (left) and a transitive order with source S, middle M , sink T (right). Each
arrow points from the owner of a branch to the other vertex of that center-triangle edge; it is
not the direction of the branch normal.

    The reductions just invoked, and those of the next two sections, permute vertex labels;
we fix the bookkeeping once. Under a relabeling of the vertices, σ is recomputed from the
new vertex order. Any branch whose ordered pair of centers is reversed by the relabeling is
reoriented: its normal changes to −n, while its threshold and its owner are unchanged. With
these conventions the contact equalities di · ni = Hi and the sine system (6) keep their displayed
form under every relabeling used in the case analysis. For a cyclic shift this is immediate:
every index shifts by one, σ is unchanged, and no branch is reversed. For the transposition
of P2 and P3 , σ flips and all three branches are reversed; the sign flips cancel in pairs, the
sines s1 and s2 are exchanged while s3 is fixed, and both systems again keep their form. Every
relabeling we use is a composition of these two.


5    Cyclic owners
We now settle the cyclic tournament: each center owns the branch to the next center in cyclic
order. The outcome is Proposition 5.2, λ1 + λ2 + λ3 ≥ 2, and hence λ1 H1 + λ2 H2 + λ3 H3 ≥ 2,
the bound the main proof requires. The route is geometric: the three normals wind once
around the circle, and the directed gaps between them, in half-angle cotangent coordinates,
obey a single algebraic constraint. The coordinates express the thresholds through one rational
function, and the constraint turns the sine system (6) into a weighting identity for λ1 + λ2 + λ3 ;
a scalar inequality, proved in Appendix A, finishes the case. The geometry lives here; the
algebra lives in the appendix.
    By the relabeling conventions of Section 4 we may assume that Pi owns branch i, the
branch joining Pi to Pi+1 (indices mod 3, here and throughout). Each square then supplies
exactly one normal: ni is an axis of the frame at Pi , while the other square of that pair,
centered at Pi+1 , supplies the axis ni+1 of the next branch. The standing assumption of
Section 4 remains in force: s1 , s2 , s3 > 0.




                                                12
                                 P3
                                                                     n2
                                                                                 γ1
                                                                                           n1
                                                                          γ2
                                                                                     γ3
                     P1                       P2
                                                                          n3

Figure 6: The cyclic case. Left: each center owns the branch to the next center; the arrows
point from owner to other vertex and are not the directions of the normals. Right: the normals
wind once around the circle, with directed gaps γi positive, less than π, and summing to 2π.

Gaps. Let γi be the directed angle from ni to ni+1 , measured in the orientation selected
by σ, so that si = σ det(ni , ni+1 ) = sin γi and ni · ni+1 = cos γi . Strict positivity of the sines
places each γi strictly in (0, π), and this strictness is what pins the winding: following the
three gaps returns the direction to n1 , so γ1 + γ2 + γ3 is a multiple of 2π, and it lies strictly
between 0 and 3π, hence
                                        γ1 + γ2 + γ3 = 2π.
The normals wind exactly once around the circle (Figure 6).

Half-angle cotangents. Since each half-gap γi /2 lies in (0, π/2), the half-angle cotangents
                                      γ1                      γ2                     γ3
                            u = cot      ,         v = cot       ,        w = cot
                                      2                       2                      2
are positive coordinates for the gaps. The half-gaps sum to π, so the cotangent addition
formula gives
                        uv − 1      γ
                                       1   γ2           γ3 
                               = cot     +      = cot π −      = −w,
                        u+v          2     2              2
and clearing the positive denominator u + v gives

                                              uv + vw + wu = 1.                                         (7)

Expanding (u + v)(u + w) = u2 + (uv + vw + wu), the constraint (7) yields the identity

                      (u + v)(u + w) = 1 + u2                 (and its cyclic variants).
                                                         (1 + q) max{1, q}
Lemma 5.1. With the cyclic factor F (q) =                                  ,
                                                               1 + q2
                   1 + |cos γi | + sin γi
            Hi =                          ,        H1 = F (u),        H2 = F (v),         H3 = F (w).
                             2
Proof. Branch i is owned by the frame at Pi , and ni is one of its axes, so that frame contributes
half-width 12 (Lemma 2.3). The other frame of the pair, at Pi+1 , has ni+1 as an axis, so the
other-frame width formula of Lemma 2.3 gives
                          1 |ni · ni+1 | + |det(ni , ni+1 )|   1 + |cos γi | + sin γi
                   Hi =     +                                =                        ,
                          2                2                             2
using |det(ni , ni+1 )| = si = sin γi > 0.
    For the second claim, substitute the half-angle formulas: with q = cot(γ/2),

                                                2q                        q2 − 1
                                 sin γ =             ,        cos γ =            .
                                              1 + q2                      1 + q2

                                                         13
Two regimes. If q ≤ 1, then γ ≥ π/2, so |cos γ| = (1 − q 2 )/(1 + q 2 ) and

              1 + |cos γ| + sin γ  1 (1 + q 2 ) + (1 − q 2 ) + 2q   1+q
                                  = ·                2
                                                                  =        = F (q),
                       2           2            1+q                 1 + q2

since max{1, q} = 1. If q ≥ 1, then |cos γ| = (q 2 − 1)/(1 + q 2 ) and

             1 + |cos γ| + sin γ  1 (1 + q 2 ) + (q 2 − 1) + 2q   q(1 + q)
                                 = ·                            =          = F (q),
                      2           2            1 + q2              1 + q2

since max{1, q} = q. Applying this with q = u, v, w at γ = γ1 , γ2 , γ3 gives the three threshold
formulas.

The weighting identity. The sine system (6) expresses the thresholds in the multipliers;
to extract λ1 + λ2 + λ3 we seek weights on H1 , H2 , H3 under which each λi collects a constant
coefficient. The cotangent coordinates supply them:

                    2(λ1 + λ2 + λ3 ) = H1 (u + w) + H2 (u + v) + H3 (v + w).                    (8)

The pairing here is rigid: H1 carries u + w, H2 carries u + v, H3 carries v + w, and the
assignment is forced by which equations of (6) contain each λi ; permuting the weights destroys
the identity.
    To prove (8), first express the sines in the coordinates. In positive cyclic order the
oriented sines are the sines of the gaps, si = sin γi , so the half-angle formulas and the identity
(u + v)(u + w) = 1 + u2 with its cyclic variants give
                       2u                           2v                         2w
          s1 =                  ,      s2 =                  ,   s3 =                   .
                 (u + v)(u + w)               (v + w)(v + u)             (w + u)(w + v)

Now substitute (6) into the right-hand side of (8) and collect the coefficient of each multiplier.
The multiplier λ1 appears in the equation for H2 (term λ1 s1 , weight u + v) and in the equation
for H3 (term λ1 s3 , weight v + w), so its coefficient is
                                                        2u   2w
                         s1 (u + v) + s3 (v + w) =         +    = 2.
                                                       u+w w+u
The coefficients of λ2 and λ3 are the cyclic images of this computation and equal 2 as well.
This proves (8).

Proposition 5.2. In the cyclic case λ1 + λ2 + λ3 ≥ 2, and hence

                                    λ1 H1 + λ2 H2 + λ3 H3 ≥ 2.

Proof. By (8) and Lemma 5.1,

                 2(λ1 + λ2 + λ3 ) = F (u)(u + w) + F (v)(u + v) + F (w)(v + w).

The numbers u, v, w are positive and satisfy (7), so Lemma A.1 (Appendix A) bounds the
right-hand side below by 4; hence λ1 + λ2 + λ3 ≥ 2. Since λi ≥ 0 and Hi ≥ 1 for each i,

                         λ1 H1 + λ2 H2 + λ3 H3 ≥ λ1 + λ2 + λ3 ≥ 2.




                                                  14
6    Transitive owners
We close the transitive case: when the owner tournament has a source, that source owns two
branches, so both of their normals are axes of a single frame. This one discrete fact makes
the case rigid. Perpendicularity of the two source normals collapses the sine system to a
one-parameter family indexed by an angle t ∈ (0, π/2), and a triangle inequality on the frame
circle together with an explicit dual certificate delivers the bound λ1 H1 + λ2 H2 + λ3 H3 ≥ 2
required by Section 4.
    By the relabeling conventions of Section 4 we may label the vertices P1 = S, P2 = M ,
P3 = T : the source, middle, and sink of the tournament. The source owns the branches
S → M and T → S, with normals n1 and n3 ; the middle owns the branch M → T , with
normal n2 . The standing assumption s1 , s2 , s3 > 0 remains in force, and the relabeling keeps
the contact equalities and the sine system (6) in their displayed form.
    Ownership now does its work. The normals n1 and n3 are both, up to sign, axes of the
source’s frame, so they are parallel or perpendicular. If they were parallel then s3 = σ det(n3 , n1 )
would vanish, contrary to s3 > 0; so n1 ⊥ n3 , hence det(n3 , n1 ) = ±1, and positivity forces

                                               s3 = 1.

Thus (n1 , n3 ) is an orthonormal basis with det(n3 , n1 ) = σ. Writing n2 = a n1 + b n3 and
expanding the determinants in this basis gives s1 = σ det(n1 , n2 ) = −b and s2 = σ det(n2 , n3 ) =
−a, so
                               s21 + s22 = a2 + b2 = ∥n2 ∥2 = 1.
Since s1 , s2 > 0, there is a unique t ∈ (0, π/2) with

                          s3 = 1,      s1 = c = cos t,      s2 = s = sin t.

Geometrically, the identity Jσ u · v = σ det(u, v) of Section 4 gives c = s1 = Jσ n1 · n2 , so t is
the angle between Jσ n1 and n2 .
   Write
              A = H(d4 (S, M )),       B = H(d4 (M, T )),      C = H(d4 (T, S)),
where H is the owned-branch threshold (2), and d4 (S, M ) abbreviates the frame distance
between the frames at S and M . All three branches are owned, and by Lemma 2.3 the
threshold of an owned branch depends only on the two frames of its pair, not on which frame
supplies the axis. This independence is what the identification needs: the branch joining T to
S is owned by S, not by T , yet its threshold is still H(d4 (T, S)). Hence

                               H1 = A,        H2 = B,       H3 = C,

and A, B, C ≥ 1 by (2).
    The source geometry determines A explicitly. Since Jσ n1 is a unit vector perpendicular
to n1 , we have Jσ n1 = ±n3 , so the axes of the source’s frame point along n1 modulo
quarter turns; and n2 is an axis of the frame at M making angle t with Jσ n1 . Therefore
d4 (S, M ) = min{t, π/2 − t}, which need not equal t. But cos x + sin x is symmetric under
x 7→ π/2 − x, so the threshold formula is unambiguous:
                                                    1+c+s
                               A = H min{t, π2 − t} =      .
                                                       2
    Substituting s3 = 1, s1 = c, s2 = s and H1 = A, H2 = B, H3 = C into the sine system (6)
yields the transitive system

                     A = cλ2 + λ3 ,       B = cλ1 + sλ3 ,       C = λ1 + sλ2 .                    (9)

                                                 15
               M                           n2     J σ n1
                                                  t
                                                            n1
       S                  T
       source, middle, sink
                                                   n3
                                 θM

                                                G(x) = H(x) − 1 is increasing, concave,
                               R/(π/2)Z         and subadditive. The frame-circle triangle
                                                inequality gives A + 1 ≤ B + C.
                          θS              θT

Figure 7: The transitive case. Top left: the owner tournament with source S, middle M , sink
T ; each arrow points from the owner of a branch to the other vertex of its edge, not along
the branch normal. Top right: the source-owned normals n1 ⊥ n3 , with n2 at angle t from
Jσ n1 . Bottom: the three frames on the frame circle R/(π/2)Z; since G = H − 1 is increasing,
concave, and subadditive, the triangle inequality for d4 gives A + 1 ≤ B + C (Lemma 6.1).


The remaining task is the bound Aλ1 + Bλ2 + Cλ3 ≥ 2.
   The first ingredient is a triangle inequality among the three thresholds, measured in excess
over the universal lower bound 1.

Lemma 6.1 (Frame excess). A + 1 ≤ B + C.

Proof. We extend G = H − 1 to an increasing concave function vanishing at 0, deduce
subadditivity, and apply the triangle inequality for d4 .
     On [0, π/4] set
                                                   cos x + sin x − 1
                              G(x) = H(x) − 1 =                      .
                                                           2
Then G(0) = 0, G′ (x) = (cos x − sin x)/2 ≥ 0 with equality exactly at x = π/4, and
G′′ (x) = −(cos x + sin x)/2 < 0; so G is increasing and concave on [0, π/4]. Extend G to [0, ∞)
by the constant value G(π/4) on [π/4, ∞). Because G′ (π/4) = 0, the extension is C 1 : the
graph flattens tangentially rather than with a corner, and the derivative of the extension is
nonnegative and nonincreasing on all of [0, ∞). The extension is therefore still increasing and
concave. The extension is needed because the sum of two frame distances below can be as
large as π/2.
     A nonnegative increasing concave function G on [0, ∞) with G(0) = 0 is subadditive.
Indeed, for x, y ≥ 0 with x + y > 0, concavity along the segment from 0 to x + y gives
              x                 y             x                  y             x
  G(x) = G           (x + y) +       ·0 ≥           G(x + y) +         G(0) =       G(x + y),
               x+y             x+y            x+y                x+y           x+y
                             y
and symmetrically G(y) ≥ x+y   G(x + y); adding the two gives G(x) + G(y) ≥ G(x + y). The
case x = y = 0 is trivial.
   Since d4 is a metric on the frame circle, d4 (S, M ) ≤ d4 (S, T ) + d4 (T, M ). Monotonicity
and subadditivity of the extension now give
                                                           
          A − 1 = G(d4 (S, M )) ≤ G d4 (S, T ) + d4 (T, M )
                                 ≤ G(d4 (S, T )) + G(d4 (T, M )) = (C − 1) + (B − 1),

which rearranges to A + 1 ≤ B + C.

                                                 16
   The second ingredient is an identity. It is stated in the half-angle variable

                                                         1 − r2               2r
                     r = tan(t/2) ∈ (0, 1),         c=          ,      s=          ,
                                                         1 + r2             1 + r2
in which every quantity in sight becomes rational. The certificate data are

                   r                    1 + r + r2                  r(1 − r)(3 − 2r + 2r2 − r3 )
       α=                    ,     β=              ,        K=                                   .
            (1 + r)(1 + r2 )             2(1 + r)                            2(1 + r2 )2

Lemma 6.2 (Transitive dual certificate). Under the transitive system (9),

                   Aλ1 + λ2 + λ3 − 2 = α(C − 1) + β(B + C − A − 1) + K.                              (10)

Consequently Aλ1 + λ2 + λ3 ≥ 2.

   The multipliers enter the right side of (10) only through the two slacks C−1 and B+C−A−1;
the constant K depends on t alone. That is the point of the certificate: it writes the target,
minus 2, as a nonnegative combination of quantities already known to be nonnegative, plus a
nonnegative constant.

Proof. After substituting (9) and the r-parametrization, (10) becomes an identity of polynomi-
als; the mechanical checking recipe is given in the subsection below. Every term on the right
is nonnegative: α, β ≥ 0 by inspection, since r ∈ (0, 1); C − 1 ≥ 0 by (2); B + C − A − 1 ≥ 0
by Lemma 6.1; and K ≥ 0 because r(1 − r) > 0 on (0, 1), while 2r + r3 ≤ 3 on [0, 1] gives
3 − 2r + 2r2 − r3 ≥ 2r2 ≥ 0. Hence the left side of (10) is nonnegative.

Proposition 6.3. In the transitive case, λ1 H1 + λ2 H2 + λ3 H3 ≥ 2.

Proof. Using H1 = A, H2 = B, H3 = C, then B, C ≥ 1 with λ2 , λ3 ≥ 0, and finally Lemma 6.2,

             λ1 H1 + λ2 H2 + λ3 H3 = Aλ1 + Bλ2 + Cλ3 ≥ Aλ1 + λ2 + λ3 ≥ 2.

6.1   Where the certificate comes from
Identity (10) can be checked in a few lines of computer algebra or by a patient hand computation.
This subsection records the exact recipe, then derives α, β, and K, so that the certificate reads
as the dual solution of a small linear program rather than as a rational accident.
    Checking recipe. Form the difference of the two sides of (10). Substitute B = cλ1 + sλ3
and C = λ1 + sλ2 into the slacks, and eliminate λ3 via the first equation of (9), λ3 = A − cλ2 .
Only the first equation is used for elimination; the second and third enter solely through B
and C in the slacks. Then substitute
                        1 − r2             2r                  1+c+s   1+r
                   c=          ,    s=          ,        A=          =        ,
                        1 + r2           1 + r2                  2     1 + r2

together with the displayed formulas for α, β, K. Every denominator divides 2(1 + r)(1 + r2 )2 ,
which is positive; clearing it leaves a polynomial in r and the remaining multipliers λ1 , λ2 ,
which expands to zero.
   Derivation. The certificate draws on two nonnegative slacks: C − 1 (owned thresholds are
≥ 1) and B + C − A − 1 (Lemma 6.1). We seek coefficients α, β making

                      Aλ1 + λ2 + λ3 − 2 − α(C − 1) − β(B + C − A − 1)




                                                 17
independent of the multipliers modulo the first equation of the system. Eliminating λ3 as in
the recipe, the coefficient of λ1 in this expression is A − α − (1 + c)β and the coefficient of λ2
is (1 − c) − sα − s(1 − c)β. Setting both to zero gives the linear system

                         α + (1 + c)β = A,        sα + s(1 − c)β = 1 − c,

whose solution, after the half-angle substitution, is the displayed α and β. What remains is a
constant in the multipliers; factored, it is exactly K. The one thing that could still have failed
is the sign of that constant, and K ≥ 0 on (0, 1) as checked in the proof of Lemma 6.2. The
certificate is thus the dual solution of a small linear program: (α, β) is the combination of the
two slacks whose multiplier dependence matches the target exactly, and K is the unmatched
constant.


7    Proof of the main theorem
The pieces are in place. It remains to check that the three cases treated by Propositions 4.2, 5.2
and 6.3 exhaust all possibilities, and to convert their common conclusion λ1 H1 +λ2 H2 +λ3 H3 ≥
2 into the contradiction.

Proof of Theorem 1.1. Suppose the theorem fails: there are unit squares S1 , S2 , S3 with pair-
wise disjoint interiors whose centers P1 , P2 , P3 form a non-obtuse triangle of area less than 12 .
Write D0 for its doubled area, so D0 < 1. Freeze one owned branch per pair and minimize
doubled area as in Lemma 3.2: a minimizing configuration exists, is acute, and satisfies
0 < D ≤ D0 < 1. By Lemma 3.4 all three frozen branches are active there, so the Farkas
multipliers λ1 , λ2 , λ3 ≥ 0 exist and satisfy the Euler identity (5),

                                  2D = λ1 H1 + λ2 H2 + λ3 H3 .

   We claim this sum is at least 2. The oriented sines s1 , s2 , s3 admit exactly three possibilities:
some si ≤ 0; all si > 0 with cyclic owner tournament; all si > 0 with transitive owner
tournament. The list is exhaustive: when every sine is positive, directing each edge of
the center triangle away from its owner yields a tournament on three vertices, and such a
tournament is either a directed cycle or transitive; the relabeling conventions of Section 4
bring either geometry into the displayed form treated there, leaving thresholds and owners
unchanged. In the first case Proposition 4.2 gives λ1 H1 + λ2 H2 + λ3 H3 ≥ 2; in the cyclic case
Proposition 5.2 gives the same bound; in the transitive case Proposition 6.3 does. The claim
holds in every case.
    By (5), then, 2D ≥ 2, so D ≥ 1. This inequality concerns the doubled area of the
minimizing configuration, not of the assumed counterexample; but Lemma 3.2 bounds precisely
that quantity by D ≤ D0 < 1. The two bounds are incompatible, so no counterexample exists:
every admissible configuration with a non-obtuse center triangle satisfies area(P1 P2 P3 ) ≥ 12 .


8    Sharpness and the limits of the statement
Theorem 1.1 is best possible in every direction: the constant 12 is attained, the angle hypothesis
cannot be dropped, and the statement does not extend to four centers. This section records
these three boundaries, together with the correct bound when the angle hypothesis is dropped
entirely.

Proposition 8.1 (Equality). The constant 12 in Theorem 1.1 is attained.



                                                 18
Proof. Take axis-parallel unit squares centered at (0, 0), (1, 0), and (0, 1). The first two share
only the edge on the line x = 12 , the first and third share only the edge on y = 12 , and the last
two share only the corner ( 12 , 21 ); the interiors are pairwise disjoint. The center triangle is right
isosceles with legs of length 1: non-obtuse, of area exactly 12 .

   The angle hypothesis is not an artifact of the proof. Without it the center-triangle area
can be made arbitrarily small.

Example 8.2 (Obtuse degeneration). Fix 0 < ε < 12 and take axis-parallel unit squares
centered at (0, 0), (1, ε), and (2, 0). Their projections to the horizontal axis are the intervals
[− 12 , 12 ], [ 12 , 32 ], [ 32 , 25 ], whose interiors are pairwise disjoint, so the squares have pairwise disjoint
interiors. The center triangle has area 12 |det (1, ε), (2, 0) | = ε. There is no contradiction
with Theorem 1.1: at the middle vertex the angle between (−1, −ε) and (1, −ε) has cosine
proportional to ε2 − 1 < 0, so the triangle is obtuse there.

    For arbitrary center triangles the correct general statement replaces the constant by a
factor recording how far the triangle is from degenerate.

Proposition 8.3 (All-angle bound). Let S1 , S2 , S3 be unit squares with pairwise disjoint
interiors and centers P1 , P2 , P3 . Then for every angle θ of the center triangle,
                                                                 1
                                          area(P1 P2 P3 ) ≥      2 sin θ,

and in particular this holds for the largest angle.

Proof. Suppose first that the centers are not collinear, and let a, b be the lengths of the two
sides adjacent to θ. By Lemma 1.2 both are at least 1, so

                                   area(P1 P2 P3 ) = 21 ab sin θ ≥       1
                                                                         2 sin θ.

If the centers are collinear, every angle is 0 or π, the right side is 0, and the inequality holds
trivially.

    The obtuse degeneration makes sin θ small only by making an angle obtuse; under the
hypothesis of Theorem 1.1 the theorem beats Proposition 8.3 by removing the angle factor
entirely.
    Finally, no four-center analogue exists. The natural candidate quantity is the area of
the convex hull of four centers in strict convex position (all four turn determinants of the
cyclic boundary order strictly positive, so that the quadrilateral is genuinely two-dimensional),
and no positive lower bound holds for it, even for axis-parallel unit squares that are pairwise
disjoint as closed sets.

Proposition 8.4 (Four-center hull infimum). Over all quadruples of unit squares with pairwise
disjoint interiors whose centers are in strict convex position, the infimum of the area of the
convex hull of the centers is 0. This holds even restricted to axis-parallel unit squares that are
pairwise disjoint as closed sets. The infimum is not attained.

Proof. Fix L > 1 and ε > 0, and take axis-parallel unit squares centered at

                  p0 = (0, 0),        p1 = (L, ε),        p2 = (2L, −ε),            p3 = (3L, 0).

The horizontal projections of the squares are intervals of length 1 centered at 0, L, 2L, 3L;
since L > 1, consecutive centers are more than 1 apart, so these intervals are pairwise disjoint
and the closed squares are pairwise disjoint.


                                                         19
    In the cyclic order p0 , p2 , p3 , p1 the four turn determinants are
                                                                    
                    det(p2 − p0 , p3 − p2 ) = det (2L, −ε), (L, ε) = 3Lε,
                                                                    
                    det(p3 − p2 , p1 − p3 ) = det (L, ε), (−2L, ε) = 3Lε,
                                                                        
                    det(p1 − p3 , p0 − p1 ) = det (−2L, ε), (−L, −ε) = 3Lε,
                                                                        
                    det(p0 − p1 , p2 − p0 ) = det (−L, −ε), (2L, −ε) = 3Lε,

all strictly positive, so the four centers are in strict convex position with counterclockwise
boundary order p0 , p2 , p3 , p1 . (The cyclic order matters: in the order p0 , p1 , p2 , p3 the turn deter-
minants are −3Lε, +3Lε, +3Lε, −3Lε, not all of one sign, so that quadrilateral is not convex.)
The shoelace formula in the boundary order sums the vertex cross products over consecutive              
pairs; the two terms involving p0 = (0, 0)      vanish, while det(p 2 , p3 ) = det  (2L,   −ε), (3L, 0)  =
3Lε and det(p3 , p1 ) = det (3L, 0), (L, ε) = 3Lε. Hence

                     area conv{p0 , p1 , p2 , p3 } = 12 | 0 + 3Lε + 3Lε + 0 | = 3Lε,

which tends to 0 as ε → 0 with L fixed. The infimum is not attained: a quadrilateral in strict
convex position has positive area.


9    Lean validation
The proof of Theorem 1.1 is complete as written: every mathematical step appears in the
preceding sections, and no step defers to a machine computation. The formalization reported
here is independent verification, not an ingredient. The theorem has been machine-checked
twice, by two unrelated proofs.

The reciprocal development. The proof of this paper is formalized in Lean 4 [4] over
mathlib [5] in roughly four thousand lines of dedicated modules, organized to mirror the paper
section by section:

Module                                    Paper counterpart
FixedBranches                             owned separating branches (Section 2)
Extremal                                  the compact minimum (Section 3)
CompleteContact, FirstVariation           complete branch contact (Section 3)
Farkas, Stationarity                      the Farkas lemma and reciprocal equations (Section 4)
Forces and its conclusions                the sine system and nonpositive-sine case (Section 4)
Cyclic, CyclicGeometry                    the cyclic case (Section 5 and Appendix A)
Transitive, TransitiveGeometry            the transitive case (Section 6)
OwnerConclusion                           the eight owner assignments reduced to the two tournaments
Proof                                     assembly (Section 7)

The public statement is CenterAreaLemma.Reciprocal.center area lemma reciprocal, for-
mulated for closed unit squares given by orthonormal side normals, with pairwise disjoint
interiors and non-obtuseness expressed as the three squared-side-length inequalities. The
development contains no sorry and uses no axioms beyond the standard classical and quotient
principles already present in mathlib.

An independent second proof. The statement is also verified by an entirely different
machine-checked proof: a corner-trap localization argument, which normalizes one square
to be axis-parallel, localizes the other two centers near a corner of its rounded exclusion
neighbourhood, and closes with a large family of local algebraic estimates. That development

                                                    20
runs to 44,389 lines of Lean (the import closure of its localization argument) with no sorry; its
top-level theorem, CenterAreaLemma.center area lemma from axis aligned normalized,
proves the statement of CenterAreaLemma.center area lemma without invoking the reciprocal
development. The two proofs share no mathematical content beyond elementary facts, so the
theorem has independent verification along two unrelated routes.

A cautionary counterexample. The corner-trap route began with a natural simplification
that turned out to be wrong, and the formal development preserves the refutation. Replace the
two moving squares by the center-only relaxation: each center must merely avoid the rounded
exclusion neighbourhood of the fixed square. A first attempt classified all bad relaxed pairs
(mutual distance ≥ 1, non-obtuse with the origin, area < 12 ) into six coordinate-local side and
corner blocks up to the symmetries of the square. That classification is false: the pair
                                      1
                                                C0 = − 19      4
                                                                
                              B0 = 20   ,1 ,             20 5,

is a relaxed bad pair lying in none of the six blocks, and the file Counterexample.lean certifies
this. The relaxation loses exactly the information the localization needs: which side of the
actual tilted square does the excluding. We record the counterexample because the failed
claim was plausible enough to survive informal scrutiny for some time; it is a concrete instance
of why machine verification earns its keep here.

Paper-statement wrappers. A library PaperProofs, kept in the same repository as this
paper, restates Theorem 1.1 in the paper’s exact logical form (unit squares by orthonormal side
normals, disjointness of interiors, non-obtuseness as the three squared-side-length inequalities,
area as the halved absolute shoelace determinant) and derives it from each entry point:
       PaperProofs.paper center area lemma from CenterAreaLemma.center area lemma,
                  PaperProofs.paper center area lemma reciprocal from
                CenterAreaLemma.Reciprocal.center area lemma reciprocal.

The wrappers are thin by design; their value is the machine-checked confirmation that
the theorem proved formally is the theorem asserted here, with every project-level defi-
nition unfolded. PaperProofs also formalizes the all-angle bound of Proposition 8.3 as
PaperProofs.paper all angle bound.

Build status. The complete development (both proofs, the wrapper library, and all support-
ing modules) was rebuilt end to end on 2026-08-09 with Lean v4.29.1 and mathlib v4.29.1, in
8,367 build jobs. No sorry occurs anywhere in the build, and #print axioms on the wrapper
theorems and on the corner-trap entry points reports only propext, Classical.choice, and
Quot.sound.

What is not formalized. The equality construction, the obtuse degeneration example, and
the four-center hull infimum are not formalized. Each is an explicit construction requiring
interior computations of concrete squares. Every step of the proof of Theorem 1.1 itself is
covered.


Acknowledgments
This work relied on substantial computer assistance. The proof was developed alongside its
Lean formalization, and AI-based tools were used both in the formal development and in
drafting this paper. The mathematics was checked independently of that assistance, by hand
and by the Lean proof checker.

                                               21
A      The cyclic scalar inequality
This appendix proves the scalar inequality to which the cyclic case of the owner tournament
was reduced. It is pure algebra: the proof uses nothing from the rest of the paper, and the
rest of the paper uses nothing from this appendix beyond the statement below.

Lemma A.1. Let u, v, w > 0 satisfy uv + vw + wu = 1, and set

                                             (1 + q) max{1, q}
                                   F (q) =                     .
                                                   1 + q2
Then
                      F (u) (u + w) + F (v) (u + v) + F (w) (v + w) ≥ 4.

    The pairing matters: F (u) carries the factor u + w, F (v) carries u + v, and F (w) carries
v + w. This is the pairing produced by the weighting identity of the cyclic case. The sum is
invariant under the cyclic relabeling (u, v, w) 7→ (v, w, u), which permutes its three terms.

Proof. We first use the constraint to replace each denominator 1 + q 2 by a product of pairwise
sums, then split into two cases: when u, v, w ≤ 1 a single weighted Cauchy–Schwarz estimate
suffices, and when one variable exceeds 1 three termwise estimates with visibly nonnegative
errors reduce the claim to u + 1/u ≥ 2.
    Structural reductions. The constraint gives

                        (u + v)(u + w) = u2 + uv + uw + vw = 1 + u2

together with its cyclic variants (v + w)(v + u) = 1 + v 2 and (w + u)(w + v) = 1 + w2 . Dividing,
the three terms become
                           (1 + u) max{1, u}                           (1 + v) max{1, v}
          F (u)(u + w) =                     ,        F (v)(u + v) =                     ,
                                 u+v                                         v+w
                                                 (1 + w) max{1, w}
                              F (w)(v + w) =                       ,
                                                       w+u
so, writing R for their sum, we must prove R ≥ 4. At most one of u, v, w exceeds 1: if two
of them did, their product alone would exceed uv + vw + wu = 1. Since the sum R and the
constraint are invariant under cyclic relabeling, two cases remain: either u, v, w ≤ 1, or u > 1
and v, w < 1.
    Case 1: u, v, w ≤ 1. Here max{1, q} = 1 in every term, so
                                      1+u   1+v   1+w
                                 R=       +     +     .
                                      u+v v+w w+u
Substitute U = 1 − u, V = 1 − v, W = 1 − w and T = U + V + W , so U, V, W ∈ [0, 1). Each
term exceeds 1 by a controlled amount,
                                  1+u     1−v    V
                                      −1=     =
                                  u+v     u+v   u+v
and cyclically, so
                                        V   W   U
                               R−3=       +   +    .
                                       u+v v+w w+u
In the new variables the constraint reads

 1 = (1 − U )(1 − V ) + (1 − V )(1 − W ) + (1 − W )(1 − U ) = 3 − 2T + (U V + V W + W U ),


                                                 22
that is,
                                U V + V W + W U = 2(T − 1).
Moreover T > 0: if U = V = W = 0 then u = v = w = 1 and uv + vw + wu = 3 ̸= 1. This
strict positivity is what makes the Cauchy–Schwarz denominator below positive.
    Assume first U, V, W > 0. The Engel form of the Cauchy–Schwarz inequality (write each
           2
term as V / V (u + v) , and cyclically) gives

                                     (U + V + W )2                 T2
                R−3 ≥                                        =              ,
                           V (u + v) + W (v + w) + U (w + u)   4T − T 2 − 2
where the denominator simplifies by substituting u = 1 − U , v = 1 − V , w = 1 − W and using
U V + V W + W U = 2(T − 1):

   V (u + v) + W (v + w) + U (w + u) = V (2 − U − V ) + W (2 − V − W ) + U (2 − W − U )
                                       = 2T − (U 2 + V 2 + W 2 ) − (U V + V W + W U )
                                       = 2T − T 2 − 2 · 2(T − 1) − 2(T − 1)
                                                                 

                                       = 4T − T 2 − 2.

The denominator is a sum of three nonnegative terms, not all zero because T > 0, hence
positive. Finally
                        T 2 − (4T − T 2 − 2) = 2(T − 1)2 ≥ 0,
so T 2 /(4T − T 2 − 2) ≥ 1 and R − 3 ≥ 1, as required. If one of U, V, W vanishes, its term in
R − 3 vanishes as well; applying the same estimate to the remaining two terms leaves both the
numerator T 2 and the denominator 4T − T 2 − 2 unchanged, since the missing summand of
each is zero, and the conclusion is the same.
    Case 2: u > 1, v, w < 1. Now max{1, u} = u while max{1, v} = max{1, w} = 1, so
                                     u(1 + u)   1+v   1+w
                               R=             +     +     .
                                      u+v       v+w w+u
We bound the first and third terms by estimates whose errors are visibly nonnegative:
      u(1 + u)     1−v   v(1 − v)(u − 1)                    1+w  1  w(u − 1)
               −u−     =                 ≥ 0,                   − =          ≥ 0.
       u+v         1+v   (u + v)(1 + v)                     w+u u   u(w + u)

For the first: u(1+u)     u(1−v)                1−v               u(1+v)−(u+v)
                u+v − u = u+v , and subtracting 1+v leaves (1 − v) (u+v)(1+v) = (1 −
     v(u−1)
v) (u+v)(1+v) . The second is a direct computation.
    For the middle term, write the constraint as u(v + w) + vw = 1. Then

           1 + v 2 − (v + w)(1 + v) = u(v + w) + vw + v 2 − (v + w)(1 + v)
                                    = (v + w)(u + v − 1 − v) = (u − 1)(v + w) > 0,

so 1 + v 2 > (v + w)(1 + v); since all four quantities are positive, cross-multiplying gives
                                      1+v   (1 + v)2
                                          ≥          .
                                      v+w    1 + v2
Furthermore
                                  (1 + v)2 1 − v
                                           +         ≥ 2,
                                   1 + v2     1+v
because clearing the positive denominators leaves the excess
                         (1 + v)2 1 − v          2v 2 (1 − v)
                                 +      − 2 =                   ≥ 0.
                          1 + v2   1+v        (1 + v 2 )(1 + v)

                                               23
Combining the four estimates,

                                1 − v (1 + v)2   1      1
                    R ≥ u+           +      2
                                               +   ≥ u + + 2 ≥ 4,
                                1+v    1+v       u      u
the last step by u + 1/u ≥ 2.


References
 [1] P. Erdős and R. L. Graham. On packing squares with equal squares. J. Combin. Theory
     Ser. A, 19:119–123, 1975.

 [2] J. Farkas. Theorie der einfachen Ungleichungen. J. Reine Angew. Math., 124:1–27, 1902.

 [3] E. Friedman. Packing unit squares in squares: a survey and new results. Electron. J.
     Combin., Dynamic Survey DS7 (version of 2009). doi:10.37236/28.

 [4] L. de Moura and S. Ullrich. The Lean 4 theorem prover and programming language. In
     Automated Deduction – CADE 28, volume 12699 of Lecture Notes in Computer Science,
     pages 625–635. Springer, 2021.

 [5] The mathlib community. The Lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs (CPP 2020), pages
     367–381. ACM, 2020.

 [6] J. C. Maxwell. On reciprocal figures and diagrams of forces. Philos. Mag. (4), 27:250–261,
     1864.




                                              24
