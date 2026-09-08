                    Counting unit squares by their centers:
                   sharp convex bounds and exact strip laws
                                          David R. MacIver

                                              August 2026


                                                 Abstract
          Nmax counts interior-disjoint unit squares, in any orientation, with all centers in a given
      region. For compact convex K, at most area(K) + wx (K) + wy (K) + 1 = area(K ⊕ Q0 )
      centers fit, Q0 the centered axis-parallel unit square: the trivial axis-parallel bound survives
      arbitrary rotations. Specializing, Nmax (a, b) ≤ (a + 1)(b + 1), with equality for integer a, b.
      The rectangle case uses a weighted boundary score and is fully formalized in Lean 4 over
      mathlib; the convex case uses a cubical clipping √ lemma paying    in ℓ1 boundary
                                                                                      √ length and
      exterior turning. We prove the exact strip law          2     2
                                                            w + h + 1 for w ≤ ( 2 − 1)/2 (also
      formalized),
            √       extended to w ≤ ξ when w2 + h2 < 4; the three-branch threshold     √ T3 (w); and,
      for 1/ 2 ≤ w < 1, exact bands with thresholds τ2r+1 = r/w, τ2r+2 = r/w +√ 1 − w2 . Sharp
      local bounds
              √     include the exact near-wall gap, the corner threshold 1 + 1/(2 2), exactness of
      g(d) = 1 − d2 , and the failure of three natural strengthenings. This paper was produced
      with a mix of ChatGPT and Claude Fable and has not yet been adequately human reviewed.


1    Introduction
How many interior-disjoint unit squares can have all their centers in a prescribed region? A unit
square is closed, of side 1, in any orientation; a family is interior-disjoint if no two interiors meet,
boundary contact allowed; only the centers are constrained, and the squares may protrude from
the region. For a, b ≥ 0 let Nmax (a, b) be the supremum of |F | over finite interior-disjoint families
F of unit squares with all centers in [0, a] × [0, b]; by Theorem 1.2 below every admissible family
has at most (a + 1)(b + 1) members, so the supremum is an attained maximum. Center-count
bounds of this kind serve as pruning rules in computer searches for packing impossibility results.
    The companion function Smax (a, b) is the maximum number of interior-disjoint unit squares
contained in [0, a] × [0, b], and s(n) = inf{t : Smax (t, t) ≥ n} is the side of the smallest square
containing n interior-disjoint unit squares; the study of s(n) goes back to Erdős and Graham [1],
with known exact values and dense packings surveyed and established in [2, 5, 12, 9, 3]. The two
functions are linked, for a, b ≥ 1, by
                                                                              √        √
            Smax (a, b) ≤ Nmax (a − 1, b − 1),       Nmax (a, b) ≤ Smax (a + 2, b + 2),              (1)
and trivially Nmax (a, b) ≥ Smax (a, b): the√
                                            center of a contained square lies at distance ≥ 1/2 from
each side, and a center at distance ≥ 1/ 2 from each side leaves room for the square in every
orientation. These inequalities are the interface to the s(n) literature and are not used further.
    Our first result bounds the count for an arbitrary convex center region. Write Q0 =
[−1/2, 1/2]2 for the axis-parallel unit square centered at the origin, D(x, ρ) for the closed disk
of radius ρ about x, wx (K) and wy (K) for the coordinate widths of a convex set K, and
K ⊕ Q0 = {k + q : k ∈ K, q ∈ Q0 } for the Minkowski sum.
Theorem 1.1 (Convex center count). Let K ⊂ R2 be compact and convex. If N interior-disjoint
unit squares have all their centers in K, then
                       N ≤ area(K ⊕ Q0 ) = area(K) + wx (K) + wy (K) + 1.

                                                     1
    If all squares were axis-parallel, each would be ci + Q0 with ci ∈ K, the squares would be
interior-disjoint subsets of K ⊕ Q0 , and area comparison√would give the bound at√once. A
tilted square centered in K is only contained in K ⊕ D(0, 2/2), and area(K ⊕ D(0, 2/2)) >
area(K ⊕ Q0 ), the excess being π/2 − 1 when K is a point. The content of Theorem 1.1 is that
the axis-parallel bound survives arbitrary independent rotations.
                                                              √     For point sets with pairwise
distances ≥ 1 in convex K, Groemer and Oler proved N ≤ (2/ 3) area(K) + 12 per(K) + 1 [4, 10];
our area coefficient for squares is 1.
Theorem 1.2 (Rectangle center bound). For all a, b ≥ 0, Nmax (a, b) ≤ (a + 1)(b + 1), with
equality when a, b ∈ N, attained by axis-parallel squares centered at the integer grid points.
   The axis-parallel case is folklore-adjacent: ℓ∞ separation of centers plus counting the half-open
unit grid cells meeting the rectangle gives at most √ (⌊a⌋ + 1)(⌊b⌋ + 1). √      √
   For narrow strips we √prove exact laws. Set τ = ( 2−1)/2
                                                         √      and ξ =  (4 √2−2   3)/5, the smaller
                                                                                             √
                   2                                             2
positive root of 5w − 8 2 w + 4 = 0, equivalently of 4 − w + 2w = 2 2, with ξ < 1/ 2.
                                                                                      j√          k
Theorem 1.3 (Very-narrow strip law). If 0 ≤ w ≤ τ and h ≥ 0, then Nmax (w, h) =          w 2 + h2 +
1.
                                                                              √
Corollary 1.4 (First diagonal threshold). If 0 ≤ w ≤ ξ and D = w2 + h2 < 2, then
Nmax (w, h) = ⌊D⌋ + 1.
    We say “n centers fit in [0, w] × [0, h]” to abbreviate Nmax (w, h) ≥ n. Let T3 (w) = inf{h ≥
0 : Nmax (w, h) ≥ 3} for 0 ≤ w < 1.
Theorem 1.5 (Three-center threshold). For 0 ≤ w < 1,
                                 √
                                           2
                                  √4 − w ,
                                              0 ≤ w ≤ ξ,
                                                          √
                        T3 (w) = 2 2 − 2w, ξ ≤ w ≤ 1/ 2,
                                                √
                                   1/w,        1/ 2 ≤ w < 1,
                                 

and the infimum is attained in every branch: three centers fit in [0, w] × [0, h] if and only if
h ≥ T3 (w).
                                          √                      √
Theorem 1.6 (Exact wide bands). Let 1/ 2 ≤ w < 1 and d = 1 − w2 , and define τ1 = 0,
τ2r+1 = r/w for r ≥ 1, and τ2r+2 = r/w + d for r ≥ 0. Then for every n ≥ 1,
                             τn ≤ h < τn+1    =⇒     Nmax (w, h) = n.
    The center-area lemma of [7] (three interior-disjoint unit squares with non-obtuse center
triangle have center-triangle area ≥ 1/2) is used as an input to Theorems 1.5 and 1.6 and is not
reproved here.
    Integer rectangles attain
                        √      the bound of Theorem 1.2. The very-narrow law fails for every
w > ξ at h just below 4 − w2 (details in Section 5). The toolbox of Section 7 collects sharp
local lemmas, several of which show that natural strengthenings of our tools fail.
    Two of the main results, Theorem 1.2 with its sharpness and Theorem 1.3, are machine-
checked end to end in Lean 4, and every closed-form constant and inequality in the paper was
verified by independent numerical audit; see Section 9.
    The proofs run as follows. Theorem 1.2 is proved in Section 3 by charging each square a score,
area inside the rectangle plus weighted boundary trace and covered corners, and showing each
square scores at least 1. Section 4 proves Theorem 1.1 via a cubical clipping lemma: whatever
the region fails to contain of a square it pays for in ℓ1 boundary length and exterior turning
inside the square. Section 5 proves Theorem 1.3 by packing ordered chords along the strip,
then develops rounded neighbourhoods and three positional obstructions that give the narrow
branches of Theorem 1.5 and Corollary 1.4. Section 6 handles the wide branch via the center-area
input, completes Theorem 1.5, and proves Theorem 1.6 with sheared constructions matching the
gap bookkeeping. Section 7 presents the toolbox, Section 8 the open problems, and Section 9 the
Lean validation.

                                                 2
2    Preliminaries
This section fixes terminology and records four elementary facts used throughout: the support-
radius formula, the center-distance lemma, its sharp vertical-gap corollary, and a disjointness
criterion for squares with a common frame.
    A unit square is a closed square of side 1 in the plane, in any orientation. A family of unit
squares is interior-disjoint if no two of its members have intersecting interiors; boundary contact
is allowed. We write c(S) for the center of a square S. Every √
                                                                     unit square S contains its incircle
         1                                                      2
D(c(S), 2 ) and is contained in its circumcircle D(c(S), 2 ). More precisely, for a unit vector e
making angle θ with a side normal of S, the support radius maxp∈S (p − c(S)) · e equals
                                                              h √ i
                                q(θ) = 12 | cos θ| + | sin θ| ∈ 12 , 22 .                            (2)

Lemma 2.1 (Center distance). Two interior-disjoint unit squares have centers at distance at
least 1.

Proof. If the centers were at distance less than 1, the two open incircles of radius 12 would meet,
hence so would the square interiors.

Corollary 2.2 (Vertical gap). Let S1 , S2 be interior-disjoint
                                                           √     unit squares with centers (x1 , y1 )
and (x2 , y2 ). If |x1 − x2 | ≤ w ≤ 1, then |y1 − y2 | ≥ 1 − w2 . The bound is√sharp for every
w ∈ [0, 1]: two unit squares sharing a full edge, with common side direction (w, 1 − w2 ), attain
it.
                                                                                        √
Proof. By Lemma 2.1, (y1 − y2 )2 ≥ 1 − (x1 − x2 )2 ≥ 1 − w2 . For sharpness, set v = (w, 1 − w2 ),
let u be a unit vector perpendicular to v, and take

                            S1 = sv + tu : |s|, |t| ≤ 12 ,
                                 
                                                             S2 = S1 + v.
                                                                  √
The
1   centers  0 and v  satisfy |x1 − x 2 | = w and |y 1 − y 2 | =   1 − w2 . The squares share the edge
                  1
 2 v + tu : |t| ≤ 2 , and their interiors lie in the two opposite open half-planes bounded by that
edge’s line, so they are interior-disjoint.

    Several constructions below assemble squares sharing a single frame; the following criterion
certifies their disjointness once and for all.

Lemma 2.3 (Common-axis criterion). Let S1 , S2 be unit squares with common side axes:
Si = ci + {su + tv : |s|, |t| ≤ 12 } for a fixed orthonormal pair u, v. If |(c1 − c2 ) · u| ≥ 1 or
|(c1 − c2 ) · v| ≥ 1, then the interiors of S1 and S2 are disjoint.

Proof. Suppose |(c1 − c2 ) · u| ≥ 1. The orthogonal projection of int Si onto the u-axis is the
open interval of length 1 centered at ci · u; these two intervals are disjoint, hence so are the
interiors.

    Two properties of Nmax are immediate from the definition and are used without further
comment: Nmax (a, b) = Nmax (b, a), by reflection in the diagonal, and Nmax is nondecreasing in
each argument, since enlarging the rectangle admits every earlier configuration of centers.
√ We record the one-center case: Nmax (w, h) ≥ 1 always, and Nmax (w, h) = 1 exactly when
  w2 + h2 < 1. Indeed,
                   √     when the diagonal is shorter than 1, Lemma 2.1 forbids a second
center,√while when w2 + h2 ≥ 1, the shared-edge pair of Corollary 2.2 with side direction
(w, h)/ w2 + h2 places two centers at distance 1 inside [0, w] × [0, h].




                                                   3
3    The rectangle bound
We prove Theorem 1.2 by charging each square of a packing a score against the rectangle and
summing the charges. The proof does not replace tilted squares by axis-parallel ones: in general
no replacement preserves both the centers and interior-disjointness. For related work on packing
unit squares in a rectangle see Nagamochi [9].
Definition 3.1 (Rectangle score). For a unit square Q and a closed axis-parallel rectangle R set

      σR (Q) = area(Q ∩ R) + 12 length(Q ∩ ∂R) + 41 #{v : v a vertex of R, v ∈ int Q},                 (3)

where the middle term is one-dimensional length along the sides of R.
     Interior area counts in full, the boundary trace at weight 12 , and each covered corner at weight
1
4 : the boundary terms compensate the part of Q clipped away by R.

Lemma 3.2 (One-square score). If c(Q) ∈ R, then σR (Q) ≥ 1.
Proof. The plan: reduce to general position by an outward perturbation, identify σR with a
product measure, factor that measure over the four quadrants at the center, and show that each
quadrant contributes at least 14 . Translate so that c(Q) is the origin and write R = [−α, β]×[−γ, δ]
with α, β, γ, δ ≥ 0.
    Step A: reduction to general position. Call the configuration generic if no side line of R
contains a side of Q, no vertex of R lies on ∂Q, and α, β, γ, δ > 0. Suppose the lemma is proved
for generic configurations. In the general case, move each side of R outward by a small generic
amount: the perturbed rectangle Rε ⊇ R is generic. The outward direction matters twice: it
keeps the center inside Rε , and it makes any vanishing side parameters positive, so the quadrant
decomposition below is nondegenerate. Moreover

                                       lim sup σRε (Q) ≤ σR (Q),
                                        ε→0

since the area term converges, and any losses in the limit are boundary or corner terms already
present in σR (Q). Hence σR (Q) ≥ lim supε→0 σRε (Q) ≥ 1, and we may assume the configuration
is generic.
    Step B: product-measure identity. For u < v let

                                      µ[u,v] = λ[u,v] + 12 δu + 21 δv ,

Lebesgue measure on [u, v] plus half-atoms at the endpoints, δt denoting the Dirac mass at t. In
a generic configuration                                   
                               σR (Q) = µ[−α,β] ⊗ µ[−γ,δ] (Q).
Indeed, λ ⊗ λ gives area(Q ∩ R); each product of an endpoint atom with λ gives half the length
of the trace of Q on the corresponding side of R; and each product of two atoms gives 14 at a
vertex of R, which by genericity lies in Q exactly when it lies in int Q.
    Step C: quadrant split. Since α, β, γ, δ > 0, neither factor has an atom at 0, so the coordinate
axes are null for the product measure and the four closed quadrants at the origin contribute
additively. It therefore suffices to show that each quadrant’s part of Q receives mass at least 14 .
    Step D: one quadrant. The restriction of the product measure to the closed positive quadrant
is µ+         +              +                 1
     [0,β] ⊗ µ[0,δ] , where µ[0,t] = λ[0,t] + 2 δt retains only the atom at the outer endpoint. Reflections
in the coordinate axes carry the other three quadrants to this one; they replace (β, δ) by a pair
(u, v) with u ∈ {α, β}, v ∈ {γ, δ}, and Q by a reflected copy, still a unit square centered at the
origin. By the symmetries of that square we may take its angle θ ∈ [0, π/4]; write c = cos θ,
s = sin θ. The part of Q in the closed positive quadrant is then the quadrilateral P with vertices
                                        1                  c − s c + s              1
               O = (0, 0),         A=         ,0 ,      B=           ,      ,     C = 0,      ,
                                           2c                    2     2                  2c

                                                     4
of area exactly 14 (a shoelace computation). The quadrant contribution is the score of P clipped
by the window [0, u] × [0, v]: the area of P ∩ ([0, u] × [0, v]), plus half the length of the trace of P
on each of the lines x = u and y = v inside the window, plus 14 if (u, v) ∈ P . We show this is at
least 14 for all u, v ≥ 0; three cases cover all configurations.
    Case 1: (u, v) ∈ P . The corner atom alone contributes 12 · 12 = 14 .
    Case 2: u ≤ (c − s)/2 and (u, v) above P , that is, v > ( 12 + su)/c. For x ≤ (c − s)/2 the
quadrilateral P is bounded above by the side CB, on the line −xs + yc = 12 , so P meets the
column {0 ≤ x ≤ u} in {0 ≤ y ≤ ( 12 + sx)/c}; the cut at y = v removes nothing, the trace on
y = v is empty, and the corner atom does not act. The score equals
                        Z u 1
                             2 + sx          1 12 + su   u    su2   1
                                                                      + su
                                      dx +     ·       =    +     + 2      ,
                         0      c            2     c     2c    2c     2c

the last summand being the half-weighted trace on the line x = u, of length ( 12 + su)/c. This
expression is increasing in u and at u = 0 equals 1/(4c) ≥ 14 .
    Case 3: the remaining configurations, u > (c − s)/2 and (u, v) ∈      / P . Here the parts of P
outside the window are triangles cut off by the clipping lines, each covered by half of the slice
that cuts it. The part of P to the right of x = u, present when u lies between the abscissae
(c − s)/2 of B and 1/(2c) of A, is a triangle whose
                                                √       base is the vertical slice of P at x = u and
whose horizontal extent is at most 1/(2c) ≤ 2/2 < 1; its area is therefore at most half the
length of its base, which is exactly the credited edge term at x = u. The part of P above y = v
is treated the same way, with vertical extent at most (c + s)/2 < 1. When both cuts act, the
doubly cut corner region is covered twice, which only helps. The edge credits thus repay the
clipped area, and the score is at least area(P ) = 14 .
    Summing the four quadrant contributions gives σR (Q) ≥ 1. The case analysis just completed
is elementary but fiddly; it is carried out in full, with no appeal to pictures, in the Lean
formalization (Section 9).

Proof of Theorem 1.2. Suppose first that a = 0 or b = 0. All centers lie on a segment of length
m = max(a, b), and by Lemma 2.1 they are pairwise at distance at least 1, so there are at most
⌊m⌋ + 1 ≤ (a + 1)(b + 1) of them.
    Now let a, b > 0, put R = [0, a] × [0, b], P
                                               and let Q1 , . . . , QN be interior-disjoint unit squares
with centers in R. Lemma 3.2 gives N ≤ N         i=1 σR (Qi ), and we sum the three kinds of terms
separately. The interiors of the Qi are disjoint, so the area terms total at most area(R) = ab.
On each side of R the traces Qi ∩ ∂R have pairwise disjoint relative interiors, since away from
its endpoints each trace lies in the open square int Qi ; the edge terms therefore total at most
1
2 · 2(a + b) = a + b. Each vertex of R is interior to at most one Qi , so the corner terms total at
most 14 · 4 = 1. Hence
                            N ≤ ab + (a + b) + 1 = (a + 1)(b + 1).
For a, b ∈ N the axis-parallel unit squares centered at the (a + 1)(b + 1) integer points of
[0, a] × [0, b] are interior-disjoint, so Nmax (a, b) = (a + 1)(b + 1).

Remark 3.3. Theorem 1.2, including Lemma 3.2 and the integer-grid sharpness construction, is
fully formalized in Lean 4, as is the very-narrow strip law. Section 9 states exactly what is and
is not machine-checked.


4    The convex bound via cubical clipping
The cubical clipping lemma bounds the area a convex region fails to capture from a unit square
centered in it, charging the loss to boundary length and turning inside the square. Subsection 4.1
proves the lemma; Subsection 4.2 sums it over a packing to prove Theorem 1.1.



                                                    5
4.1   The clipping lemma
Two boundary functionals are needed. For a rectifiable curve Γ let
                                          Z
                                                          
                                 P1 (Γ) =     |dx| + |dy|
                                                Γ

be its ℓ1 length; for a convex body M the set function A 7→ P1 (∂M ∩ A) is a Borel measure
on ∂M . For compact convex C ⊂ R2 with nonempty interior, let κC be the exterior-turning
measure on ∂C, normalized so that κC (∂C) = 2π; when C is a convex polygon, κC places at
each vertex an atom equal to the exterior angle there.
Lemma 4.1 (Cubical clipping). Let S be a unit square with center o, in any orientation, and
let C ⊂ R2 be compact convex with o ∈ C and int C ̸= ∅. Then
                                                                κC (int S)
                          area(S \ C) ≤ 12 P1 (∂C ∩ int S) +               .                      (4)
                                                                    2π
Equivalently, since area(S) = 1,
                                                             κC (int S)
                        area(S ∩ C) + 12 P1 (∂C ∩ int S) +              ≥ 1.
                                                                 2π
    What the region fails to contain of the square, it must pay for in boundary length and turning
inside the square.

Proof. The plan: prove (4) for polygons transverse to S, classifying the components of S \ C as
chord-separated (charged to boundary length through a cap–chord table) or wrapping (at most
one, charged through a wedge inequality), then pass to general C by a dilation centered at o and
outer polygonal approximation.
     Step 1: transverse polygons and the component–arc correspondence. Assume first that C is a
convex polygon transverse to S: no vertex of C lies on ∂S, no edge of C meets ∂S tangentially
or along a segment, and ∂C ∩ ∂S is finite.
     If ∂C ⊂ int S, then κC (int S) = κC (∂C) = 2π, so the right side of (4) is at least 1 ≥ area(S\C)
and we are done. Otherwise, call a maximal subarc of ∂C with relative interior in int S and
endpoints on ∂S a crossing arc; by transversality there are finitely many. By convexity of C ∩ S,
the crossing arcs are in bijection with the components of S \ C: each component U has as free
boundary exactly one crossing arc Γ, with endpoints p, q ∈ ∂S and relative interior in int S.
Nothing below depends on this bijection; a component with several free arcs would be charged
through any one of them.
     Step 2: each component is chord-separated or wrapping. Fix a component U with arc Γ and
endpoints p, q. Since p, q ∈ C and C is convex, [p, q] ⊂ C. Transversality excludes a side of S
lying on the line pq; as p, q ∈ ∂S, the line pq therefore meets S exactly in [p, q]: the segment
[p, q] is the full chord of S on that line. The connected set U is disjoint from C ⊇ [p, q], hence
avoids this full chord and lies strictly on one side of the line pq. Let B be the chordal cap of C
cut off by [p, q] on the side of Γ: the part of C bounded by Γ and the chord. Then B is convex
and U lies on the B-side of the line. Two cases.
     Case (a): o lies weakly on the far side of the line pq from U . Then U is contained in the
straight cap of S cut off by the line pq on the side of U , at signed distance t ≥ 0 from o. Work
in S-aligned coordinates, with the unit normal of the cutting line at angle θ ∈ [0, π/4] from a
side normal of S; set c = cos θ, s = sin θ, a = (c − s)/2, h = (c + s)/2. The cap area A and the
full chord length ℓ are:
                                                    A          ℓ
                                                  1 t         1
                                     0≤t≤a          −
                                                  2 c         c
                                                 (h − t)2 h − t
                                     a≤t≤h
                                                   2sc        sc

                                                    6
The second row is void when s = 0, and the cap is empty for t > h. In both rows A ≤ ℓ/2: in√ the
first row this reads c − 2t ≤ 1, true since c ≤ 1; in the second, h − t ≤ 1, true since h ≤ 2/2.
The chord endpoints are p and q, so ℓ = |p − q|2 and

                          area(U ) ≤ 12 |p − q|2 ≤ 12 |p − q|1 ≤ 12 P1 (Γ),                           (5)

the last step because the total variation of each coordinate along Γ is at least the coordinate gap
between its endpoints. Call a component charged by (5) filled.
    Case (b): o lies strictly on the same side of the line pq as U . That side is the B-side,
and B is the intersection of C with the closed half-plane on that side, so o ∈ B; by convexity
conv{p, o, q} ⊆ B. Call U wrapping. At most one component wraps. Suppose U1 , U2 both wrap,
with arcs Γ1 , Γ2 , chords [pi , qi ], and caps Bi . The arcs are disjoint subarcs of the closed convex
curve ∂C, so they occur in cyclic order and Γ2 lies in the complementary arc of ∂C determined
by Γ1 ; in particular the two chords do not cross. Let H1 be the closed half-plane bounded by the
line p1 q1 that contains B1 . The complementary arc lies in the opposite closed half-plane, hence
so do p2 , q2 , the chord [p2 , q2 ], and therefore the convex cap B2 , whose boundary is Γ2 ∪ [p2 , q2 ].
But wrapping of U1 places o in the interior of H1 , while wrapping of U2 places o ∈ B2 , which
misses the interior of H1 : a contradiction.
    Step 3: the wrapping sector and its arc estimates. Suppose the component U wraps, with
arc Γ and endpoints p, q. Write e(φ) = (cos φ, sin φ), let r(φ) = max{ρ ≥ 0 : o + ρe(φ) ∈ S}
be the radial function of S at o, and set m(φ) = | cos φ| + | sin φ|, so that |x − o|1 = r(φ) m(φ)
whenever x = o + r(φ)e(φ) ∈ ∂S. Let α, β be the direction angles of p − o and q − o, and let
δ = ∠poq ∈ [0, π]. Let J be the window of directions pointing from o into the chord [p, q]; it has
angular length δ. Define the closed radial sector

                           W = { o + ρe(φ) : φ ∈ J, 0 ≤ ρ ≤ r(φ) } ⊆ S.

W misses U : for φ ∈ J the ray from o in direction e(φ) meets [p, q] at a point x; the segment
[o, x] lies in the convex set B (both endpoints do), which is disjoint from U ; beyond x the ray lies
strictly on the far side of the line pq, while U lies on the near side. Every point of W therefore
lies in S ∩ C or in a filled component, so
                                                    X
                   area(U ) = 1 − area(S ∩ C) −          area(U ′ ) ≤ 1 − area(W ).
                                                   U ′ filled

   For the arc length: for a convex body M , each coordinate increases along one of the two
boundary arcs between its extremes and decreases along the other, so P1 (∂M ) = 2wx (M ) +
2wy (M ); in particular P1 (∂ · ) is monotone under inclusion of convex sets. Since o lies strictly off
the line pq, the set conv{p, o, q} is a nondegenerate triangle contained in B, and
                                                           
       P1 (Γ) + |p − q|1 = P1 (∂B) ≥ P1 ∂ conv{p, o, q} = |p − o|1 + |o − q|1 + |p − q|1 .

Since p, q ∈ ∂S, this gives

                      P1 (Γ) ≥ |p − o|1 + |o − q|1 = r(α) m(α) + r(β) m(β).                           (6)

    For the turning: ∂B is a closed convex curve of total turning 2π, consisting of Γ, the straight
chord, and corners at p and q with exterior angles εp , εq . The turning along the relative interior
of Γ equals κC (Γ ∩ int S): the vertices of C interior to Γ carry the same exterior angles in B as in
C, and p, q are not vertices of C by transversality. From conv{p, o, q} ⊆ B, the interior angle of
B at p is at least ∠opq, so εp ≤ π − ∠opq; similarly εq ≤ π − ∠oqp. Since ∠opq + ∠oqp = π − δ,

                     κC (Γ ∩ int S) = 2π − εp − εq ≥ ∠opq + ∠oqp = π − δ.                             (7)



                                                    7
   Step 4: the wedge inequality. By the sector bound area(U ) ≤ 1 − area(W ) together with (6)
and (7), the wrapping component obeys area(U ) ≤ 12 P1 (Γ) + κC (Γ ∩ int S)/(2π) once we establish

                                                          π−δ
                      area(W ) + 12 r(α) m(α) + r(β) m(β) +    ≥ 1.                               (8)
                                                            2π
    Write δ =R jπ/2 + u with j ∈ {0, 1, 2} and u ∈ [0, π/2], taking u = 0 if jR = 2. First,
area(W ) = 12 J r(φ)2 dφ, and r2 is π/2-periodic, each full period contributing  1
                                                                                 2  r2 = 14 , one
quarter of area(S). Among windows I of length u ≤ π/2, the integral 12 I r2 is smallest when I
                                                                        R

is centered on a side normal of S, since r2 is even about each side normal and increasing in the
angular distance from it; there r(φ) = 1/(2 cos φ) for |φ| ≤ π/4, and
                                        Z u/2
                                    1            dφ           u
                                    2              2φ
                                                      = 14 tan .
                                         −u/2 4 cos           2

Hence area(W ) ≥ j/4 + 14 tan(u/2). Second, r ≥ 12 , since S contains the disk of radius 12 about
o; and m is π/2-periodic and concave on each period with m(0) = 1, so m(β) = m(α + u), and
minimizing over α in one quadrant (both terms are shifted sines; concavity pushes the minimum
to the endpoints, where one argument is a multiple of π/2) gives

                                m(α) + m(β) ≥ 1 + cos u + sin u.

Substituting these bounds and (π − δ)/(2π) = 12 − j/4 − u/(2π), the left side of (8) minus 1 is at
least                                     u                         u
                          H(u) = 14 tan + cos u + sin u − 1 −           ;
                                           2                         2π
the j-terms cancel exactly: the sector bound contributes j/4 and the turning term −(jπ/2)/(2π) =
−j/4. Now H(0) = H(π/2) = 0, and
                                             u    u
                        H ′′ (u) = 81 sec2     tan − 14 (cos u + sin u) ≤ 0 :
                                             2    2
with z = tan(u/2) ∈ [0, 1], so that sec2 (u/2) = 1 + z 2 , cos u = (1 − z 2 )/(1 + z 2 ), and sin u =
2z/(1 + z 2 ), clearing the positive denominators turns H ′′ ≤ 0 into

                                (1 − z) z 4 + z 3 + 3z 2 + 5z + 2 ≥ 0,
                                                                 


which holds on [0, 1]. A concave function vanishing at both endpoints of [0, π/2] is nonnegative
there, so H ≥ 0 and (8) holds.
    Now sum over the components of S \ C. The crossing arcs are distinct, their relative interiors
are disjoint subsets of ∂C ∩ int S, and arc endpoints carry no P1 -mass; so the charges (5) for
the filled components, together with the charge 12 P1 (Γ) + κC (Γ ∩ int S)/(2π) for the at most one
wrapping component and κC (Γ ∩ int S) ≤ κC (int S), give

                                                                 κC (int S)
                          area(S \ C) ≤ 12 P1 (∂C ∩ int S) +                ,
                                                                     2π
which is (4) for transverse polygons.
    Step 5: general C by centered dilation. Let C be T   compact convex with o ∈ C and int C ̸= ∅.
For λ > 1 set Cλ = o + λ(C − o); then C ⊆ Cλ and λ>1 Cλ = C, so area(S \ Cλ ) increases to
area(S \ C) as λ ↓ 1.
    Fix λ > 1 and choose transverse convex polygons Pn ⊇ Cλ with Pn → Cλ in the Hausdorff
metric; outer polygonal approximants exist, and transversality is achieved by a small perturbation
of their vertices. Each Pn contains o, so (4) holds for Pn . As n → ∞, area(S \ Pn ) → area(S \ Cλ ),
and the coordinate-variation measures defining P1 and the turning measures of convex bodies


                                                    8
converge weakly under Hausdorff convergence, a standard fact of the theory of convex bodies [11].
Since S is closed, the portmanteau upper bound for closed sets gives, allowing extra mass on ∂S,
                     h                     κP (int S) i                     κC (S)
              lim sup 21 P1 (∂Pn ∩ int S) + n           ≤ 21 P1 (∂Cλ ∩ S) + λ      ,
                 n                            2π                              2π
whence area(S \ Cλ ) ≤ 12 P1 (∂Cλ ∩ S) + κCλ (S)/(2π).
   Rescale. The dilation x 7→ o + λ(x − o) maps C onto Cλ and the contracted square
S = o + λ−1 (S − o) onto S; it scales P1 by λ and leaves turning invariant, so
 (λ)


                                      κCλ (S)         λ               κC (S (λ) )
                     1
                     2 P1 (∂Cλ ∩ S) +             =     P1 ∂C ∩ S (λ) +            .
                                        2π            2                   2π
Since o is the center of S, each S (λ) is a compact subset of int S, and as λ ↓ 1 the sets S (λ) increase
with union int S. Monotone convergence for the two boundary measures gives P1 (∂C ∩ S (λ) ) →
P1 (∂C ∩ int S) and κC (S (λ) ) → κC (int S), while λ → 1 and area(S \ Cλ ) ↑ area(S \ C). Passing
to the limit yields (4); no length or turning mass on ∂S enters the bound.

4.2    Proof of the convex bound
Summing the clipping inequality over a packing proves the theorem.

Proof of Theorem 1.1. Suppose first that int K ̸= ∅, and let S1 , . . . , SN be interior-disjoint unit
squares with centers in K. Lemma 4.1 with C = K, in its equivalent form, gives for each i
                                                                      κK (int Si )
                        1 ≤ area(Si ∩ K) + 21 P1 (∂K ∩ int Si ) +                  .
                                                                          2π
Sum over i. Three different measures appear: area on K, ℓ1 length on ∂K, and turning on ∂K,
with total masses area(K), P1 (∂K), and 2π. Each is evaluated on the open sets int Si (for the
first, area(Si ∩ K) = area(int Si ∩ K) because ∂Si is Lebesgue-null), and these sets are pairwise
disjoint, so each of the three sums is at most the corresponding total mass:
                                                 κK (∂K)
               N ≤ area(K) + 12 P1 (∂K) +                = area(K) + 21 P1 (∂K) + 1.
                                                   2π
Around the closed convex curve ∂K each coordinate increases along one of the two arcs between
its extremes and decreases along the other, so its total variation is twice the corresponding width,
and P1 (∂K) = 2wx (K) + 2wy (K). Hence N ≤ area(K) + wx (K) + wy (K) + 1.
    For the Minkowski identity, write Q0 = Ix ⊕ Iy with Ix = [− 12 , 12 ] × {0} and Iy = {0} × [− 12 , 21 ].
Summing K with Ix lengthens every nonempty horizontal section by exactly 1, and the sections
are nonempty over a set of heights of measure wy (K), so area(K ⊕ Ix ) = area(K) + wy (K) by
Cavalieri. Summing with Iy lengthens every nonempty vertical section of K ⊕ Ix by 1 over a set
of abscissae of measure wx (K ⊕ Ix ) = wx (K) + 1, so
                                                         
     area(K ⊕ Q0 ) = area(K) + wy (K) + wx (K) + 1 = area(K) + wx (K) + wy (K) + 1,
matching the bound.
    If int K = ∅, apply the case above to the outer parallel bodies Kε = K ⊕ D(0, ε), ε > 0: the
centers lie in K ⊆ Kε , so N ≤ area(Kε ) + wx (Kε ) + wy (Kε ) + 1, and the right side is continuous
as ε ↓ 0 with limit area(K) + wx (K) + wy (K) + 1.

Remark 4.2 (The score is the clipping budget). For K = [0, a] × [0, b] the theorem recovers
Theorem 1.2 term for term. Along the axis-parallel boundary ∂K the ℓ1 length coincides with
ordinary length, so 12 P1 (∂K ∩ int S) is the edge term of the score (3) at weight 12 ; each corner
of the rectangle carries turning π/2, hence normalized mass (π/2)/(2π) = 14 , the corner weight.
The totals 12 P1 (∂K) = a + b and κK (∂K)/(2π) = 1 reproduce the budget ab + a + b + 1 =
(a + 1)(b + 1) = area(K ⊕ Q0 ). The clipping lemma restricted to rectangles is precisely Lemma 3.2.

                                                      9
Remark 4.3 (Sharpness). For K = [0, a]×[0, b] with a, b ∈ N the bound is attained, by Theorem 1.2.
For generic K it is not: a point K gives the bound 1, which is attained, while a disk of small
radius gives a bound slightly above 1 although a disk of diameter less than 1 holds at most one
center. Theorem 1.1 is thus the exact extension of the integer-rectangle phenomenon to arbitrary
convex center regions, such as tilted strips. For those it supplies pruning bounds in computer
searches that Theorem 1.2 does not reach.


5     Narrow strips: the very-narrow law and three-center obstruc-
      tions
This section proves Theorem 1.3, develops two lemmas about the rounded neighbourhood
Q ⊕ D(0, 12 ) of a unit square, and uses them to prove three positional obstructions, the assembly
theorem
    √ (Theorem 5.10), and Corollary 1.4. Throughout, w denotes the strip width and
d = 1 − w2 .

5.1   The very-narrow law
Proposition 5.1 (Ordered strip bound). For 0 ≤ w < 1 and h ≥ 0, Nmax (w, h) ≤ ⌊h/d⌋ + 1.
Consequently, if n − 1 ≤ h < nd then Nmax (w, h) = n.

Proof. Order the centers by height. Consecutive centers differ by at most w horizontally, hence
by at least d vertically by Corollary 2.2; with n centers, h ≥ (n − 1)d. For the second claim,
h < nd forbids n + 1 centers, while h ≥ n − 1 admits the vertical chain of n axis-parallel unit
squares centered at unit spacing on a vertical line, interior-disjoint by Lemma 2.3.

   The diagonal chain below is the lower-bound construction for Theorem 1.3; it is stated as a
lemma because Corollary 1.4 and the three-center threshold constructions of the next section
reuse it.
                                                               j√        k
Lemma 5.2 (Diagonal chain). For all w, h ≥ 0, Nmax (w, h) ≥       w2 + h2 + 1.
                 √
Proof. Let D = w2 + h2 . If D = 0 take one square. Otherwise let e = (w, h)/D and give every
square a side direction parallel to e. Place centers at ke for 0 ≤ k ≤ ⌊D⌋; they lie on the segment
from (0, 0) to (w, h), hence in [0, w] × [0, h]. Any two of the squares have common side axes and
centers separated by |k − k ′ | ≥ 1 along the axis e, so they are interior-disjoint by Lemma 2.3;
consecutive squares share a full edge.
                                                                      √
Lemma 5.3 (Short-offset chord). A line at distance at most τ = ( 2 − 1)/2 from the center of
a unit square meets it in a segment of length at least 1.

Proof. Rotate so that the line is vertical at abscissa x from the center, with 0 ≤ x ≤ τ , and the
square makes angle θ ∈ [0, π/4] with the axes; write c = cos θ, s = sin θ.
    If x ≤ (c − s)/2, the line crosses the pair of opposite sides of the square nearest to horizontal
and the chord has length 1/c ≥ 1.
    Otherwise s > 0 (at θ =0 the first case covers all x ≤ √τ < 1/2), and 2the chord cuts a corner,
with length (c + s)/2 − x /(sc). Put u = c + s ∈ [1, 2], so sc = (u − 1)/2. The function
                                          √                      √                       √
u 7→ (u − u2 + 1)/2 is decreasing on [1, 2], with minimum ( 2 − 1)/2 = τ at u = 2; hence

                            c+s           u − u2 + 1
                                 − sc =              ≥ τ ≥ x,
                              2               2
                                 
which rearranges to (c + s)/2 − x /(sc) ≥ 1.



                                                 10
                                        √
Proof of Theorem 1.3. Let D = w2 + h2 . Lemma 5.2 gives Nmax (w, h) ≥ ⌊D⌋ + 1. For
the upper bound, suppose n ≥ 2 interior-disjoint unit squares S0 , . . . , Sn−1 have centers
P0 , . . . , Pn−1 ∈ [0, w] × [0, h], ordered so that y0 ≤ · · · ≤ yn−1 ; write c = |Pn−1 − P0 | and
Y = yn−1 − y0 . Since P0 , Pn−1 ∈ [0, w] × [0, h] we have c ≤ D, so it suffices to prove c ≥ n − 1.
For n = 2 this is Lemma 2.1, so assume n ≥ 3 and let ℓ be the line through P0 and Pn−1 . The
plan: each middle center lies within distance τ of ℓ, so its square cuts a chord of length at least 1
on ℓ, and these chords pack disjointly between two half-chords of the end squares.
     Step 1 (feet on the segment). By Corollary 2.2 consecutive vertical gaps are at least d, so for
0 < i < n − 1 we have yi − y0 ≥ d and Y ≥ 2d. Horizontal coordinates differ by at most w, so

            (Pi − P0 ) · (Pn−1 − P0 ) ≥ (yi − y0 ) Y − w2 ≥ 2d2 − w2 = 2 − 3w2 > 0,
                   √
using w ≤ τ < 1/ 3, and symmetrically (Pn−1 − Pi ) · (Pn−1 − P0 ) > 0. Hence the perpendicular
foot of each middle center on ℓ lies on the segment [P0 , Pn−1 ].
     Step 2 (offsets at most τ ). The triangle P0 Pi Pn−1 lies in a w × Y rectangle, so its area is at
most wY /2, and the distance ri from Pi to ℓ satisfies ri ≤ wY /c ≤ w ≤ τ , using c ≥ Y .
     Step 3 (chords). The line ℓ passes through the centers of the two end squares; each contains
its incircle, so each meets ℓ in a chord through its center whose half-chord pointing toward the
other end square has length at least 1/2. Each middle square Si meets ℓ in a chord of length at
least 1 by Lemma 5.3, since ri ≤ τ . As ri < 1/2, this chord passes through the interior of Si
and contains the perpendicular foot of Pi (the foot lies in the incircle of Si ), hence a point of
[P0 , Pn−1 ].
     Step 4 (disjointness of the chords). For every square of the family, ℓ lies at distance less than
1/2 from its center (ri ≤ τ < 1/2 for the middle squares, 0 for the end squares), whereas a line
containing a side of a unit square lies at distance exactly 1/2 from its center. So ℓ contains no
side of any of the squares, and the intersection of ℓ with each square is a chord whose relative
interior lies in the open square. The open squares are pairwise disjoint, so the relative interiors
of the n chords are pairwise disjoint.
     Step 5 (packing). Each middle chord is connected, its relative interior is disjoint from the
two inward half-chords, and it contains a point of [P0 , Pn−1 ]; hence it lies between the inner
endpoints of the two half-chords. Summing lengths along ℓ,
                                      1                 1
                                c ≥   2 + (n − 2) · 1 + 2   = n − 1.

Thus n − 1 ≤ c ≤ D, so Nmax (w, h) ≤ ⌊D⌋ + 1.

Remark√5.4 (Sharpness in w). For every ξ < w < 1 the conclusion of √  Theorem 1.3√fails at h just
             2
below √4 − w : there ⌊D⌋ + 1 =                        fit, at height 2 2 − 2w < 4 − w2 when
                               √ 2, yet three centers √
                                       2
w ≤ 1/ 2 and at height 1/w < 4 − w when w > 1/ 2 (Theorem 1.5). On the bounded range
D < 2 the law nevertheless extends to all w ≤ ξ: this is Corollary 1.4, proved in Section 5.3.

5.2   Rounded neighbourhoods
                         √
Write ν(x) = min{2, 2 2 − 2x}. The two lemmas of this subsection turn interior-disjointness
from a unit square Q into metric information about the neighbourhood K = Q ⊕ D(0, 12 ): no
                                                             √
other center lies in int K, and every line at distance x ≤ 1/ 2 from the center of Q crosses K in
a segment of length at least ν(x).

Lemma 5.5 (Rounded exclusion). Let Q be a unit square with center O and K = Q ⊕ D(0, 12 ).
If a unit square Q′ is interior-disjoint from Q, then c(Q′ ) ∈
                                                             / int K.

Proof. For a unit vector u let hQ (u) = supp∈Q (p − O) · u, the support radius of Q from O, and
likewise hQ′ from P = c(Q′ ); by (2), hQ′ (u) ≥ 1/2. The body K has support radius hQ (u) + 1/2


                                                 11
from O. Suppose P ∈ int K. Since Q is centrally symmetric about O, so is K, and central
symmetry licenses the absolute value in

              |(P − O) · u| < hQ (u) + 12 ≤ hQ (u) + hQ′ (u)         for every unit u.

But Q and Q′ are interior-disjoint convex bodies, so some line separates them: there is a
unit vector u0 and t ∈ R with (p − O) · u0 ≤ t on Q and (p − O) · u0 ≥ t on Q′ . Then
t ≥ hQ (u0 ) and, since Q′ is centrally symmetric about P , (P − O) · u0 − hQ′ (u0 ) ≥ t, whence
(P − O) · u0 ≥ hQ (u0 ) + hQ′ (u0 ) — a contradiction.

Lemma 5.6 (Rounded chord). Let Q be a unit square centered at the origin and K = Q⊕D(0, 12 ).
              √
For 0 ≤ x ≤ 1/ 2, every line at distance x from the origin meets K in a segment of length at
least ν(x).

Proof. The plan: parametrize ∂K, classify which pair of boundary pieces the line meets, and
reduce each case by concavity to endpoint and kink checks.
    Setup. Rotate so that the line is vertical at abscissa x ≥ 0 and the square makes angle
θ ∈ [0, π/4] with the axes; write c = cos θ, s = sin θ, a = (c − s)/2, h1 = (c + s)/2. The vertices
of Q are ±A and ±B with A = (a, h1 ) and B = (h1 , −a). Since Q = conv{±A, ±B},

                    K = conv D(A, 12 ) ∪ D(−A, 12 ) ∪ D(B, 21 ) ∪ D(−B, 12 ) ,
                                                                              


so ∂K consists of four circular arcs and the four tangent segments obtained by translating the
sides of Q outward by 1/2. The vertical section of K at abscissa x ≥ 0 runs between an upper
and a lower profile, whose consecutive pieces are: for the upper profile, the shifted top side
y = (1 + sx)/c for x ≤ a − s/2, the arc of D(A, 21 ) for a − s/2 ≤ x ≤ a + c/2, and the shifted
upper-right side y = (1 − cx)/s beyond; for the lower profile, the arc of D(−A, 12 ) for x ≤ s/2 − a
(nonempty only if c ≤ 2s), the shifted bottom side y = (sx − 1)/c for s/2 − a ≤ x ≤ h1 + s/2,
and the arc of D(B, 12 ) beyond.
                              √
     Case list. For x ≤ 1/ 2 the possible (upper, lower) profile pairs are exactly (top, bottom),
(arc A, arc −A), (arc A, bottom), (upper-right, bottom) and (arc A, arc B); the fourth occurs
only when c ≤ 3s, the fifth only when c ≥ 3s, and the pair (upper-right, arc B) never occurs in
this range, its two range conditions being incompatible.
     Reduction. Let V (x) be the length of the vertical section of K at x. On each case interval V
is concave, being a sum of concave
                                 √        arc terms and linear side terms; ν is concave and linear on
each side of its kink at x = 2 − 1. Hence on each case interval  √ it suffices to verify V ≥ ν at the
endpoints and, when it lies in the interval, at the kink x = 2 − 1. We use this reduction in all
five cases.
     Case (top, bottom). V = 2/c ≥ 2 ≥ ν.
     Case (upper-right,
                  √          bottom). Here V = (1 − cx)/s + (1 − sx)/c = (c + s − x)/(cs).      √ Put
u=c+     s ∈  [1,   2], so  2cs =  u2 − 1. Two direct checks cover the whole range 0 ≤ x ≤ 1/ 2. (i)
       √
V ≥ 2 2 − 2x: after √      clearing denominators the coefficient
                                                            √     1 − 2cs of x is nonnegative,
                                                                                         √      so the
worst point √  is x = 1/ 2, where the claim reduces to 2 u − (u2 − 1) ≥ 1, i.e. u( 2 − u) ≥ 0.
(ii) For x ≤√ 2 − 1, V ≥ √     2 reduces to x ≤ u − (u2 − 1), whose right side is decreasing in u with
minimum 2 − 1 at u = 2.                                                                        √
     Case (arc A, arc −A). This pair requires x ≤ s/2 − a, hence c ≤ 2s and x ≤ s/2 < 2 − 1,
so ν = 2 on the case interval. From c ≤ 2s, sin√2θ ≥ 4/5, so u2 = 1 + sin 2θ ≥ 9/5 > 25/16 and
u ≥ 5/4. At the left endpoint x = 0, V = u + u2 − 1 ≥ 54 + 34 = 2. At the right endpoint the
pair degenerates into (arc A, bottom), treated next.
     Case (arc A, bottom). Here
                                        1 − sx
                     q
V = g(x) := h1 + 14 − (x − a)2 +                 on max{a− 2s , 2s −a} ≤ x ≤ min{a+ 2c , h1 + 2s }.
                                           c


                                                 12
At the left endpoint the value of V agrees, by continuity of the profiles, with its value in the
adjacent case — (top, bottom) if c ≥ 2s, (arc A, arc −A) if c ≤ 2s — where the bound is proved;
at the right endpoint likewise with (upper-right,
                                     √            bottom) (c ≤ 3s) or (arc A, arc B) √(c ≥ 3s). It
remains to check the kink: whenever 2 − 1 lies in the case interval, we must verify g( 2 − 1) ≥ 2.
At the extreme angles of the θ-range in which this happens, the inequality
                                                                        √          degenerates to
2/c ≥ 2 and to (3 − 4c)/(2c) ≥ 0, the latter at the angle θ1 defined by 2 − 1 =√   a + c/2, where
c = cos θ1 = 0.7468 . . . < 3/4. In the interior of the θ-range the inequality g( 2 − 1) ≥ 2 is
verified numerically — the margin exceeds 0.007 on a dense grid of angles, and 0.008 away from
the endpoint angles — and it is proved symbolically only at the two endpoint angles; no fully
symbolic proof of the interior range is q
                                        known.          q                                     √
    Case (arc A, arc B). Here V = c + 4 − (x − a) + 14 − (x − h1 )2 on h1 + s/2 ≤ x ≤ 1/ 2;
                                          1          2
                                                √              √      √
the interval is nonempty only when c√+ 2s ≤ 2, i.e.√s ≤ (2 2 − 3)/5 = ξ/2, which forces
c ≥ 0.975. On the interval x ≥ 1/2 > 2 − 1, so ν = 2 2 − 2x and we check the two endpoints.
At the left endpoint x = h1 + s/2,
                                                       q
                                 V + 2x = 52 c + 2s + 14 − 49 s2 ,

which is increasing in s — its derivative exceeds 2 − 5s
                                                       2c −
                                                            √ 9s/4 2 > 0 on the range — with
                                                              1/4−9s /4
            √                                          √
value 3 > 2 2 at s = 0. At the right endpoint x = 1/ 2 the two square roots  √ are at√least 0.37
and 0.45 respectively and c ≥ 0.975, giving V + 2x ≥ 0.975 + 0.37 + 0.45 + 2 > 2 2. (These
decimal constants are rigorous but coarse interval bounds.)
    In every case V (x) ≥ ν(x).
                                                                √               √            √
    The bound ν is exact: at θ = π/4 the section length equals 2 2 − 2x for 1/(2 2) ≤ x ≤ 1/ 2,
and at θ = 0 it equals 2 for x ≤ 1/2.

5.3    Three-center obstructions
Three obstructions show that a narrow rectangle holding three centers must be large; a corner-
counting assembly then yields Theorem 5.10, from which Corollary 1.4 follows.
                                                            √
Proposition 5.7 (Same-side obstruction). Let 0 ≤ w ≤ 1/ 2. If three interior-disjoint unit
squares have centers
             √       A = (0, 0), C = (0, h) and B = (x, y) with 0 ≤ x ≤ w and 0 ≤ y ≤ h, then
h ≥ min{2, 2 2 − 2w} = ν(w).

Proof. Let QB be the square centered at B and KB = QB ⊕ D(0, 12 ). By Lemma 5.5 neither A
                                                                                          √
nor C lies in int KB . The vertical line ℓ through A and C is at distance x ≤ w ≤ 1/ 2 from B,
so by Lemma 5.6 it meets KB in a segment σ of length at least ν(x) ≥ ν(w), as ν is nonincreasing.
The point (0, y) lies in KB : the horizontal chord of QB through√B has half-length at least 1/2, so
the distance from (0, y) to QB is at most max{0, x − 21 } ≤ 1/ 2 − 12 < 12 . Since KB ⊇ D(B, 1)
and x < 1, the line ℓ meets int KB , so the relative interior of σ lies in int KB and contains neither
A nor C. Thus A and C lie on ℓ, outside the relative interior of σ, weakly on opposite sides of
the point (0, y) ∈ σ; hence σ ⊆ [A, C] and h = |AC| ≥ ν(w).
                                                            √
Lemma 5.8 (Staircase obstruction). Let 0 ≤ w ≤ 1/ 2 and w2 + h2 < 4. If three interior-
disjoint unit squares have centers
                              √       A = (0, y), B = (x, 0), C = (w, h) with 0 ≤ x ≤ w and
0 ≤ y ≤ h, then h + 2w ≥ 2 2.
                                                 √
Proof. Put t = h − y, u = w − x, c = |BC| = h2 +√u2 , and let r be the distance from A to the
line BC. We prove c + 2r ≤ h + 2w and c + 2r ≥ 2 2.




                                                 13
    From |AC| ≥ 1 (Lemma
                       √     2.1) with A − C = −(w, t) we get w2 + t2 ≥ 1, so t ≥ d; also
u ≤ w ≤ d, since w ≤ 1/ 2. Twice the area of the triangle ABC is xt + wy = wh − ut ≤ wh − ud,
so r ≤ (wh − ud)/c. Define
                                     p
                    F (u) = (h + 2w) h2 + u2 − (h2 + u2 ) − 2wh + 2ud.

Then F (0) = 0 and

                                 (h + 2w) u
                       F ′ (u) = √          − 2u + 2d ≥ 2(d − u) ≥ 0,
                                    h2 + u2
using u ≤ d; hence F (u) ≥ 0, which rearranges to

                                            2(wh − ud)
                             c + 2r ≤ c +              ≤ h + 2w.                              (9)
                                                c
   The foot of the perpendicular from A to the line BC lies on the segment [B, C]:

                              (A − C) · (B − C) = wu + th ≥ 0,
         (A − B) · (C − B) = hy − xu ≥ y 2 − xu ≥ 1 − x2 − xu ≥ 1 − 2w2 ≥ 0,
                                             √
using h ≥ y, |AB| ≥ 1 and x, u ≤ w   √ ≤ 1/ 2.
     Moreover r ≤ wh/c ≤ w ≤ 1/ 2, since c ≥ h. Let KA be the rounded neighbourhood of
the square centered at A.  √ By Lemma 5.5 neither B nor C lies in int KA , and by Lemma 5.6 —
applicable since r ≤ 1/ 2 — the line BC meets KA in a segment of length at least ν(r); the
segment contains the foot, which lies in D(A, 1) ⊆ KA . As in Proposition 5.7, B and C lie on
the line, outside the relative √
                               interior of the segment, weakly on opposite sides of the foot;
                                                                                          √ hence
                                  2     2
c = |BC| ≥ ν(r). Since c ≤ h + w < 2, the branch ν(r) = 2 is impossible, so c ≥ 2 2 − 2r,
i.e.                                                   √
                                            c + 2r ≥ 2 2.                                     (10)
                                              √
Combining (9) and (10) gives h + 2w ≥ 2 2.
                                                                  √
Lemma 5.9 (Opposite-corner obstruction). Let 0 ≤ w ≤ 1/ 2 and w2 + h2 < 4. If three
interior-disjoint unit squares have√centers at O = (0, 0), C = (w, h) and a third point P = (x, y)
of [0, w] × [0, h], then h + 2w ≥ 2 2.
                      √
Proof. Write D = w2 + h2 < 2 and let r be the distance from P to the line OC. We may
assume hx ≥ wy: otherwise apply the point reflection through the center of the rectangle,
which swaps O and C, keeps P in the rectangle, and replaces hx − wy by its negative. Then
r = (hx − wy)/D.                              √                            √
     From |OP | ≥ 1 and y ≥ 0 we get y ≥ 1 − x2 , so hx − wy ≤ hx − w 1 − x2 ; the right side
is increasing in x on [0, w], so hx − wy ≤ w(h − d) and r ≤ w(h − d)/D. The case u = w of the
staircase computation (F (w) ≥ 0, valid since u ≤ d throughout [0, w]) gives

                                             2w(h − d)
                            D + 2r ≤ D +               ≤ h + 2w.
                                                D
    The foot of the perpendicular from P to the line OC lies on the segment [O, C]: (P − O) ·
(C − O) = xw + yh ≥ 0 and (P − C) · (O − C)√= w(w − x) + h(h − y) ≥ 0 for P ∈ [0, w] × [0, h].
Moreover r ≤ w(h − d)/D ≤ wh/D ≤ w ≤ 1/ 2. As in Lemma 5.8, the rounded neighbourhood
          √ centered at P gives D√= |OC| ≥ ν(r); since D < 2 the branch ν(r) = 2 is√impossible,
of the square
so D ≥ 2 2 − 2r, i.e. D + 2r ≥ 2 2. Combining the two displays gives h + 2w ≥ 2 2.
                                                                     √
Theorem √   5.10 (Narrow three-center obstruction). Let 0 ≤ w ≤ 1/ 2. If w2 + h2 < 4 and
h + 2w < 2 2, then Nmax (w, h) ≤ 2.

                                               14
Proof. Suppose three interior-disjoint unit squares have centers in [0, w] × [0, h]. Replace the
rectangle by the axis-parallel bounding  √  box of the three centers and translate it to√[0, w′ ] × [0, h′ ]:
then w′ ≤ w and h′ ≤ h, so w′ ≤ 1/ 2, w′2 + h′2 < 4 and h′ + 2w′ ≤ h + 2w < 2 2 — the strict
hypotheses persist — and every side of [0, w′ ] × [0, h′ ] contains a center. Each case below ends in
a contradiction. √
    Since w′ ≤ 1/ 2 < 1, no horizontal side contains two centers: they would be at distance at
most w′ < 1, contradicting Lemma 2.1.
    Suppose some vertical side contains centers at both of its endpoints. After a reflection the
centers include√ (0, 0) and   (0, h′ ), and the third lies in [0, w′ ] ×√[0, h′ ], so Proposition 5.7 gives
h ≥ min{2, 2 2 − 2w }; but h′ < 2 (from h′2 < 4) and h′ < 2 2 − 2w′ — a contradiction. (If
 ′                       ′

w′ = 0, all three centers lie on one vertical side and its endpoints are centers, so this case applies.)
    Otherwise, a center not at a corner of the box lies on at most one side, and three centers
cover four sides, so at least one center lies at a corner. If two centers lie at corners, they lie either
on a common vertical side — the previous case — or at opposite corners, since two corners on
a common horizontal side are excluded by w′ √           < 1; after a reflection the centers
                                                                                         √ include (0, 0)
        ′  ′                             ′      ′                           ′       ′
and (w , h ), and Lemma 5.9 gives h + 2w ≥ 2 2, contradicting h + 2w < 2 2. If exactly one
center lies at a corner, reflect so that it is (w′ , h′ ); the remaining two centers must cover the sides
                                                                    ′ ′                    ′            ′
x = 0 and y = 0, one each, giving centers (0, y), (x, 0),
                                                 ′        ′
                                                               √ (w , h ) with 0 ≤ x ≤ w , 0 ≤ y ≤ h —
the configuration of Lemma 5.8, whence h + 2w ≥ 2 2, again a contradiction.

Proof of Corollary 1.4. Lemma 5.2 gives Nmax (w, h) ≥ ⌊D⌋ + 1. If D < 1, any two centers in
[0, w] × [0, h] would be at distance at most D < 1, contradicting Lemma 2.1, so Nmax√(w, h) √
                                                                                            =1=
⌊D⌋ + 1. Let 1 ≤ D < 2; it remains to√show Nmax (w, h) ≤ 2. The constant
                                                                       √     √ξ = (4  2 − 2   3)/5
                                    2
                     √ root of 5w − 8√ 2 w + 4 = 0 (the roots
is the smaller positive                                        √ are (4 2 ± 2 3)/5), equivalently
the smaller root√of 4 − w2 + 2w √     = 2 2; the function w 7→ 4 −√w2 + 2w is increasing on [0,√ξ],
so w ≤ ξ gives
             √     4 − w2 + 2w ≤ 2 2. Since D < 2 we have h < 4 − w2 , hence h + 2w < 2 2;
and ξ < 1/ 2. Theorem 5.10 yields Nmax (w, h) ≤ 2.


6     The three-center threshold and exact wide bands
This section proves Theorems 1.5 and 1.6. Constructions come first: Section 6.1 builds the
two sheared families consumed by the wide threshold of Section 6.2, by the third branch of
Theorem 1.5, and by the band lower bounds.

6.1    Two sheared constructions
Both families place every square in one tilted frame and separate centers along a shared side
axis, so that Lemma 2.3 certifies disjointness.

Proposition 6.1 (Two-column odd chain). Let 0 < w ≤ 1 and let r ≥ 1 be an integer. If
h ≥ r/w then Nmax (w, h) ≥ 2r + 1.
                √
Proof. Let s = 1 − w2 and give every square the orthonormal side directions u = (w, s),
v = (−s, w). Place r + 1 left-column centers Lk = (0, k/w) for 0 ≤ k ≤ r and r right-column
centers Rk = (w, s + k/w) for 0 ≤ k ≤ r − 1. All 2r + 1 centers lie in [0, w] × [0, r/w]: the left
column tops out at r/w and the right at s + (r − 1)/w ≤ r/w, since sw ≤ 1.
    By Lemma 2.3 it suffices to separate each pair of centers by at least 1 along u or v. A
same-column difference is (0, m/w) with 1 ≤ |m| ≤ r, and |(0, m/w) · v| = |m| ≥ 1. A cross-
column difference is Rl − Lk = (w, s + m/w) with m = l − k. If m = 0, its projection on u is
w2 + s2 = 1. If m > 0, its projection on u is 1 + ms/w ≥ 1. If m < 0, its projection on v is
−sw + (s + m/w)w = m, of absolute value at least 1. Hence the 2r + 1 squares are interior-disjoint
and Nmax (w, h) ≥ 2r + 1.


                                                    15
Proposition 6.2 (Two-row sheared grid). Let 0 < s ≤ 1 and let q ≥ 1 be an integer. Then
                               q − 1 p             
                          Nmax         + 1 − s2 , s ≥ 2q.
                                   s
In particular, for 0 < w ≤ 1 and every integer r ≥ 0,
                                          r p        
                                Nmax w,     + 1 − w2 ≥ 2r + 2.
                                          w
                 √
Proof. Let γ = 1 − s2 , u = (γ, s), v = (−s, γ) and H = (1/s, 0), so that u, v are orthonormal
and H · v = −1. Give every square the side directions u, v and place the 2q centers ku + mH for
k ∈ {0, 1}, 0 ≤ m ≤ q − 1. Their horizontal coordinates kγ + m/s lie in [0, γ + (q − 1)/s] and
their vertical coordinates ks in [0, s].
    A difference of distinct centers is Ku+M H with K ∈ {0, ±1}, |M | ≤ q−1 and (K, M ) ̸= (0, 0).
If M = 0 then |(Ku) · u| = |K| = 1. If M =        ̸ 0 then, since u · v = 0 and H · v = −1,
|(Ku + M H) · v| = |M | ≥ 1. Each pair of centers is thus separated by at least 1 along a
common side√axis, and Lemma 2.3 gives the first bound. Taking s = w and q = r + 1 yields
Nmax (r/w + 1 − w2 , w) ≥ 2r + 2; the symmetry Nmax (a, b) = Nmax (b, a) yields the second.

6.2   The wide threshold
                                    √
The upper bound in the wide range 1/ 2 ≤ w < 1 rests on one imported result.
Theorem 6.3 (Center-area lemma [7]). If three interior-disjoint unit squares have centers
P1 , P2 , P3 and the triangle P1 P2 P3 is non-obtuse, then its area is at least 1/2.
    The companion paper [7] proves this by analysing an area-minimising configuration through
the reciprocal triangle of its contact forces, and carries a complete Lean formalization of the
result. We use it as a black box.
                                                         √
Lemma 6.4 (Obtuse triples in a wide strip). Let 1/ 2 ≤ w < 1 and let A, B, C be points of a
vertical strip of width w with pairwise distances at least 1 and (A − B) · (C − B) ≤ 0 (the triangle
ABC is right or obtuse at B; degenerate triples included). Then the vertical span of {A, B, C},
the difference between the largest and smallest ordinate, is at least 1/w.
Proof. We show that the vertical deviations of A and C from B have opposite signs and sum
to at least 1/w. Write u = A − B = (α, p) and v = C − B = (β, q), so u · v ≤ 0 and |u|, |v| ≥ 1;
membership√ in the strip gives |α|, |β|, |α − β| ≤ w. Put a = √
                                                              |α|, b = |β|, P = |p|, Q = |q|
and d√= 1 − w2 . From α2 + p2 ≥ 1 and a ≤ w we get P ≥ 1 − a2 ≥ d > 0, and likewise
Q ≥ 1 − b2 ≥ d.
    Step 1: p and q have opposite signs. Suppose pq > 0. Then u · v = αβ + pq ≤ 0 forces
αβ ≤ −pq < 0, so α and β have opposite signs, a + b = |α − β| ≤ w < 1, and pq ≤ −αβ = ab.
But then                   p         p
                             1 − a2 1 − b2 ≤ P Q = pq ≤ ab,
and squaring gives a2 + b2 ≥ 1, contradicting a2 + b2 ≤ (a + b)2 < 1.
    So A and C lie on opposite sides of the horizontal line through B, and the vertical span is at
least P + Q. It remains to prove P + Q ≥ 1/w; we split on the sign pattern √ of α, β.
                                                                                2
   √Step 2: αβ√ ≤ 0. Then a + b = |α − β| ≤ w. By concavity of t 7→ 1 − t , the minimum
           2         2
of 1 − a + 1 − b over a, b ≥ 0 with a + b ≤ w is attained at (a, b) =√(w, 0): for fixed sum
a + b = t concavity puts the minimum at the endpoint (t, 0), and 1 + 1 − t2 decreases in t.
Hence                               p           p                      1
                        P +Q ≥        1 − a2 + 1 − b2 ≥ 1 + d ≥          ,
                                                                      w
the last step being w(1 + d) ≥ 1, equivalently (1 − w) w2 (1 + w) − (1 − w) ≥ 0, which holds on
                                                                            
   √
[1/ 2, 1).

                                                16
                                                                               2    2
          √ αβ ≥ 0.
    Step 3:          √ Now u · v ≤ 0 gives P Q = −pq ≥ αβ =2 ab.2 If a + b ≤ 1, then
P + Q ≥ 1 − a2 + 1 − b2 , whose minimum over {0 ≤ a, b ≤ w, a + b ≤ 1} is w + d, attained
at {a, b} = {w, d}: the function decreases in each variable, so the minimum lies either where
one variable equals w (forcing the other ≤ d and the value ≥ d + w) or on the arc a2 + b2 = 1
                                                        2                              2
      √ b ∈ [d, w], where the value is a + b and (a + b) = 1 + 2ab2≥ 1 2+ 2wd = (w + d) because
with a,
             2
t 7→ t 1 − t attains its minimum on [d, w] at the endpoints. If a + b ≥ 1, then a, b ∈ [d, w], so
|a − b| ≤ w − d and

(P +Q)2 = P 2 +Q2 +2P Q ≥ (1−a2 )+(1−b2 )+2ab = 2−(a−b)2 ≥ 2−(w−d)2 = (w+d)2 ,

using w2 +d√2 = 1. In both cases P +Q ≥ w+d ≥ 1/w, since w(w+d)−1 = wd−d2 = d(w−d) ≥ 0
for w ≥ 1/ 2.
                                               √
Theorem 6.5 (Wide sheared threshold). Let 1/ 2 ≤ w < 1. If h < 1/w then Nmax (w, h) ≤ 2;
moreover Nmax (w, 1/w) ≥ 3.

Proof. Suppose three interior-disjoint unit squares have centers in [0, w] × [0, h] with h < 1/w.
The centers have pairwise distances at least 1 (Lemma 2.1) and lie in a vertical strip of width
w. If some labelling of the centers as A, B, C has (A − B) · (C − B) ≤ 0, Lemma 6.4 makes
their vertical span at least 1/w > h, impossible for centers in [0, w] × [0, h]. Otherwise every
angle of the center triangle is acute, so Theorem 6.3 gives area at least 1/2, while a triangle
contained in [0, w] × [0, h] has area at most wh/2 < 1/2: a contradiction. Hence Nmax (w, h) ≤ 2.
Proposition 6.1 with r = 1 gives Nmax (w, 1/w) ≥ 3.

6.3   Proof of Theorem 1.5
                                                      p           √
The three branches
           √       of T
                      √3 agree at the crossovers:
                                           √           4 − ξ 2 = 2 2 − 2ξ by the defining equation
of ξ, and 2 2 − 2w = 2 = 1/w at w = 1/ 2.

Proof of Theorem 1.5. Since Nmax (w, ·) is nondecreasing, it suffices to show that h < T3 (w)
forbids a third center and that Nmax (w, T3 (w)) ≥ 3.           √
    Obstructions.
      √              Let h < T3 (w). For w ≤ ξ: then h < 4√− w2 , so w2 + h2 < 4; and since
w 7→ √  4 − w2 + 2w is increasing
                                √ on [0, ξ] (its derivative
                                                    √       2 − w/ 4 − w2 is positive for w <√1) with
value 2 2 at ξ, also h+2w < 4 − w +2w   2
                                          √ ≤ 2 2. Theorem√5.10 applies, as√w ≤ ξ < 1/√ 2, and
gives Nmax (w, h) ≤ 2. For ξ ≤ w ≤ 1/ 2: then h + 2w√< 2 2; moreover 2 2 − 2w ≤ 4 − w2
                                                       2
on this range, √since after
                         √ squaring  √ this reads 5w √− 8 2 w + 4 2≤ 0, 2which holds between the
roots ξ and (4 2 + 2√ 3)/5 > 1/ 2. Hence h < 4 − w2 , so w + h < 4, and Theorem 5.10
applies again. For 1/ 2 ≤ w < 1: Theorem 6.5 gives N√        max (w, h) ≤ 2.            √
    Constructions at the threshold. For w ≤ ξ and h = 4 − w2 : the diagonal is w2 + h2 =√2,
so the diagonal
             √     chain (Lemma 5.2) gives Nmax (w, h) ≥ ⌊2⌋ + 1 = 3. For ξ ≤ w ≤             √ 1/ 2
and h = 2 2 √   − 2w: give all three squares the diagonal     √ side directions e1 √ = (1, 1)/ 2 and
e2 = (−1, 1)/ 2, √    with centers A = (0,√    0), B = (w,√ 2 − w), C = (0, 2 2 − 2w); these
lie in [0, w] × √
                [0, 2 2 − 2w], since 0 ≤ 2√− w ≤ 2 2 − 2w. The consecutive           √     differences
                                                                                              √
B − A = (w, 2 − w) and C − B = (−w, 2 − w) have projections√(w + 2 − w)/ 2 = 1
on e√1 and on e2 respectively, and the√outer difference C − A = (0, 2 2 − 2w) has projection
2 − 2 w ≥ 1 on each ei , since w ≤ 1/ 2. Each pair of centers is separated by at least   √ 1 along a
common √  side axis, so the squares are interior-disjoint by Lemma    2.3 and N max (w, 2 2 − 2w) ≥ 3.
For 1/ 2 ≤ w < 1 and h = 1/w: Proposition 6.1 with r = 1.
    Thus for every 0 ≤ w < 1, three centers fit in [0, w] × [0, h] if and only if h ≥ T3 (w), and the
infimum T3 (w) = inf{h : Nmax (w, h) ≥ 3} is attained in every branch.




                                                 17
6.4    Proof of Theorem 1.6
      √                         √
Fix 1/ 2 ≤ w < 1 and d = 1 − w2 , and recall the thresholds τ1 = 0, τ2r+1 = r/w for r ≥ 1,
and τ2r+2 = r/w + d for r ≥ 0. The sequence (τn ) is strictly increasing, since 0 < d < 1/w, so
the bands [τn , τn+1 ) partition [0, ∞).

Proof of Theorem 1.6. Upper bounds: h < τm forbids m centers. Let m ≥ 2 and suppose m
interior-disjoint unit squares have centers in [0, w] × [0, h]; order the centers by height, with
consecutive vertical gaps g1 , . . . , gm−1 ≥ 0. Any two centers differ horizontally by at most
w ≤ 1, so gi ≥ d by Corollary 2.2. Each consecutive triple of centers lies in a translate of
[0, w] ×√[0, gi + gi+1 ], so Theorem 6.5 forces gi + gi+1 ≥ 1/w; this is where the hypothesis
w ≥ 1/ 2 enters. Set u          √i = gi − d ≥ 0 and c0 = 1/w − 2d, so that ui + ui+1 ≥ c0 for each i, and
c0 ≥ 0 since 2wd = 2w 1 − w2 ≤ 1. Summing ui + ui+1 ≥ c0 over the ⌊(m − 1)/2⌋ disjoint gap
pairs (g1 , g2 ), (g3 , g4 ), . . . , and discarding the leftover excess um−1 ≥ 0 when m − 1 is odd, gives
               m−1                      m−1                      
               X                        X                      m−1 1     
         h ≥          gi = (m − 1)d +          ui ≥ (m − 1)d +        − 2d = τm .
                                                                2   w
                i=1                      i=1

Indeed, at m = 2r + 1 the right-hand side is 2rd + r(1/w − 2d) = r/w = τ2r+1 , and at m = 2r + 2
it is (2r + 1)d + r(1/w − 2d) = r/w + d = τ2r+2 . Hence h < τm implies Nmax (w, h) ≤ m − 1.
     Lower bounds: Nmax (w, τn ) ≥ n. For n = 1 this is trivial. For n = 2 and τ2 = d: the
shared-edge pair of Corollary 2.2, with common side direction (w, d) and centers (0, 0) and (w, d),
sits at opposite corners of [0, w] × [0, d]. For n = 2r + 1 with r ≥ 1: Proposition 6.1 places 2r + 1
centers at height r/w = τ2r+1 . For n = 2r + 2 with r ≥ 1: Proposition 6.2 places 2r + 2 centers
at height r/w + d = τ2r+2 .
     For τn ≤ h < τn+1 , the lower bound and monotonicity of Nmax (w, ·) give Nmax (w, h) ≥ n,
while the upper bound with m = n + 1 gives Nmax (w, h) ≤ n.

Remark 6.6. The odd thresholds and every band’s lower half are elementary, resting only on
the constructions of Section 6.1 and Corollary 2.2. Each band’s upper half for n ≥ 2 consumes
Theorem 6.5, and hence Theorem 6.3, through the consecutive-triple estimate, so only the n = 1
band is fully elementary. With the center-area lemma proved in [7] all bands are unconditional,
and the band upper bounds are formalized in Lean on top of the formalized center-area lemma
(Section 9).

6.5    The wide branch recovers the center-area lemma
Proposition 6.7. Assume   √ the two narrow branches of Theorem 1.5 together with the wide-
branch obstruction: if 1/ 2 ≤ w < 1 and three centers fit in [0, w] × [0, h], then h ≥ 1/w. Then
Theorem 6.3 follows.
                                                                                                 √
Proof. We first show that a non-obtuse triangle with long sides and a side of length at least 2
has area at least 1/2, then trap a putative counterexample in a thin rectangle and rule it out
branch by branch.                                                 √
    Step 1: a triangle with all sides at least 1, longest side c ≥ 2, and no obtuse angle has area
at least 1/2. Let r be the altitude onto the longest side. The base angles are non-obtuse, so the
foot of the altitude lies in the base, splitting c = u + v with u, v ≥ 0; the other two sides give
u2 + r2 ≥ 1 and v 2 + r2 ≥ 1. In coordinates with the apex at the origin and the base horizontal,
the vectors from the apex to the base endpoints are (−u, −r) and (v, −r), so non-obtuseness at
the apex √ gives r2 ≥ uv. If r2 < 1/2,√then u2√ , v 2 > 1/2, whence uv > 1/2 > r2 , a contradiction;
so r ≥ 1/ 2 and the area is cr/2 ≥ 2 · (1/ 2)/2 = 1/2.
    Step 2: a counterexample lies in a thin rectangle. Suppose Theorem 6.3 fails: three interior-
disjoint unit squares whose centers form a non-obtuse triangle of area less than 1/2. All sides are


                                                   18
                                                                       √            √
at least 1 (Lemma 2.1), and by Step 1 the longest side satisfies c < 2, so c ∈ [1, 2). Let r be
the altitude onto the longest side; its foot again lies in the base, so the three centers lie in an
r × c rectangle with rc = 2 area < 1; in particular r < 1/c ≤ 1 ≤ c.
     Step 3: both branches refute it. After a rigid motion of the configuration,
                                                                     √           the three centers
lie in [0, r] ×√
               [0, c] with√r < 1, so three
                                      √ centers fit there.
                                                         √ If r < 1/√ 2, the
                                                                          √ narrow
                                                                               √ branches    √ give
c ≥ T3 (r) ≥ 2, since       4 − r 2 ≥  2 on [0, ξ] and 2  2 − 2r ≥ 2  2 −  2 =   2 on [ξ, 1/   2] —
                     √        √
contradicting c < 2. If 1/ 2 ≤ r < 1, the wide-branch obstruction gives c ≥ 1/r, contradicting
rc < 1.

    The wide branch of Theorem 1.5 is therefore not merely the easiest route to its third case:
given the narrow branches, it is equivalent to the center-area input, the 1/w law being the
center-area phenomenon in another form.


7     A toolbox of sharp local bounds
The results of this section arose as candidate strengthenings of the tools above; each is sharp,
several in the deflating sense that the obvious estimate cannot be improved. Throughout,
q(t) = (cos t + sin t)/2 is the support radius of (2), and (t)+ = max{t, 0}.

7.1   The exact near-wall gap
Consider two interior-disjoint unit squares packed against a wall: both lie in the half-plane
                                                                                            √
{Y ≥ 0}, with centers at heights y1 ≤ y2 . Containment forces yi ≥ 1/2, and for 1/2 ≤ y ≤ 1/ 2
the frame of a wall-feasible square can deviate from axis alignment by at most
                                                      √   π
                                    α(y) = arcsin     2y − ,
                                                             4
                                                    √
the angle determined by q(α(y)) = y; for y ≥ 1/ 2 every orientation is feasible, and we set
α(y) = π/4 there. Let Γ(y1 , y2 ) be the infimum of the horizontal center gap |x1 − x2 | over such
pairs. A direction (cos φ, sin φ) with 0 ≤ φ < π/2 makes angle min{φ, π/2 − φ} with the nearest
side normal of the axis-parallel frame, and rotating the frame by up to α(y) toward the direction
leaves residual angle (min{φ, π/2 − φ} − α(y))+ ; so the least support
                                                                      of a wall-feasible square at
height y in that direction is my (φ) = q (min{φ, π/2 − φ} − α(y))+ , and
                                n             my1 (φ) + my2 (φ) − (y2 − y1 ) sin φ o
               Γ(y1 , y2 ) = max 0,     inf                                         .          (11)
                                      0≤φ<π/2                cos φ

Indeed, interior-disjoint convex bodies are weakly separated by a line, whose unit normal may be
taken as (cos φ, sin φ) after reflections, and projecting the center displacement onto that normal
gives |x1 − x2 | cos φ ≥ my1 (φ) + my2 (φ) − (y2 − y1 ) sin φ. Conversely, a common frame attaining
both least supports at the minimizing φ, displaced horizontally so that the two supporting lines
coincide, realizes the infimum.
                                                                      √
Theorem 7.1 (Exact shallow-wall gap). Let 1/2 ≤ y1 ≤ y2 ≤ 1/ 2 and δ = y2 − y1 , and put
                                       q                         q
                            s = y1 − 12 − y12 ,       c = y1 + 12 − y12 ,

so that s = sin α(y1 ), c = cos α(y1 ). Then
                                               √
                                                1 − δ2,    δ ≤ s,
                                 Γ(y1 , y2 ) =
                                                1 − δs ,   δ ≥ s,
                                                    c


                                                 19
attained by giving both squares
                              √ the common frame angle min{α(y1 ), arcsin δ}. The wall improves
on the free incircle bound 1 − δ 2 exactly when δ > s:
                                   1 − δs 2                 δ − s 2
                                              − (1 − δ 2 ) =            .
                                       c                         c
                                                             √
Proof. Write ai = α(yi ), so a1 ≤ a2 ≤ π/4 and δ ≤ 1/ 2 − 1/2; we minimize the objective of
(11) on the four subintervals cut by a1 , a2 , π/4.
    On [0, a1 ] both least supports equal 1/2 and the objective is sec φ − δ tan φ, with √ derivative
(sin φ − δ)/ cos2 φ; its minimum is at φ = arcsin δ when δ ≤ s = sin a1 , with value 1 − δ 2 , and
at φ = a1 when δ ≥ s, with value (1 − δs)/c.
    On [a1 , a2 ] the addition formulas and c + s = 2y1 give my1 (φ) = q(φ − a1 ) = A1 cos φ + y1 sin φ
with A1 = (c − s)/2, so the objective is A1 + (y1 − δ) tan φ + 12 sec φ, increasing because
                              √
y1 − δ = 2y1 − y2 ≥ 1 − 1/ 2 > 0.
    On [a2 , π/4] the objective is likewise A1 + A2 + (y1 + y2 − δ) tan φ with A2 = (cos a2 − sin a2 )/2,
increasing because y1 + y2 − δ = 2y1 > 0.
    For φ ∈ [π/4, π/2) the√    two supports sum to at least 1, and (1 − δ sin φ)/ cos φ ≥ 1 because
tan(φ/2) ≥ tan(π/8) > 1/ 2 − 1/2 ≥ δ; this never beats the value 1 at φ = 0.
    The objective is continuous, equal to (1 − δs)/c at a1 from either side, so the infimum is the
branch value√stated; the displayed identity, a direct computation from c2 + s2 = 1, confirms
(1 − δs)/c ≥ 1 − δ 2 , so each branch minimum is global on its range of δ. The frame at angle
φ0 = min{a1 , arcsin δ} is feasible for both squares (φ0 ≤ a1 ≤ a2 ) and attains both least supports
at the minimizing angle, so the common-frame configuration of (11) attains the infimum.
                                                               √
Remark 7.2 (Optimized wall-band gap). For 1/2 ≤ h ≤ 1/ 2 let γ(h) = min1/2≤y1 ≤y2 ≤h Γ(y1 , y2 ),
the least gap over a wall band of height h. Both branches√of Theorem 7.1 decrease in y2 , so y2 = h;
parametrizing y1 = q(a) with s = sin a, c = cos a = 1 − s2 and optimizing the constrained
branch (1 − δs)/c, the minimum occurs at the unique root of

                            (1 − s2 )3/2 − s3                                s2 (c − s)
                h = 2s +                      ,     giving     γ(h) = c −               .
                                    2                                             2
At h = 0.7 the optimal s = 0.10435686 . . . is the root in (0.104, 0.105) of the sextic

                          50s6 − 275s4 + 70s3 + 475s2 − 280s + 24 = 0,

and γ(0.7) = 0.98969271 . . .; these constants are machine-verified, while the uniqueness and
branch-membership claims above are stated with√ compressed justification. Even the free bound
already prunes on this band: δ ≤ 0.2, so Γ ≥ 0.96 > 0.9797.

7.2    The corner threshold
                                                      1
Theorem 7.3 (Corner threshold). Let C∗ = 1 + 2√         2
                                                          . Among unit squares contained in the
quarter plane [0, ∞) with pairwise disjoint interiors, at most one can have its center in [0, C]2
                    2

for any C < C∗ ; and at C = C∗ two such centers are possible.
Proof. Suppose two squares contained in [0, ∞)2 with disjoint interiors have centers cA , cB ∈
[0, C]2 . Write f (t) = cos t + sin t, let αA , αB ∈ [0, π/4] be their frame deviations from the axes,
and put σi = f (αi ); containment forces both coordinates of each center to be at least σi /2, the
square’s support q(αi ) in the coordinate directions. By the separating axis theorem some unit
side normal u of one square, say A, is a separating direction; then ∥u∥1 = σA , the support of A
in direction u is 1/2, and the support of B is f (δ)/2, where δ ∈ [0, π/4] is the frame distance.
Both coordinates of each center lie in [min(σA , σB )/2, C], so with H(δ) = (1 + f (δ))/2,
                                                                           min(σA , σB ) 
             H(δ) ≤ |(cB − cA ) · u| ≤ ∥u∥1 ∥cB − cA ∥∞ ≤ σA C −                            ,
                                                                                 2

                                                   20
hence C ≥ min(σA , σB )/2 + H(δ)/σA .                        √
    If σA ≤ σB , then H(δ) ≥ 1 and C ≥ σA /2 + 1/σA ≥ 2 > C∗ by AM–GM. Otherwise
α := αA > β := αB ; the frame distance is α − β or min{α + β, π/2 − α − β}, each at least α − β
(using α ≤ π/4), and f increases on [0, π/4], so H(δ) ≥ (1 + f (α − β))/2 and
                                                   f (β) 1 + f (α − β)
                              C ≥ F (α, β) :=           +              .
                                                     2      2f (α)
For fixed α, ∂ 2 (2F )/∂β 2 = −f (β) − f (α − β)/f (α) < 0, so F is concave in β and minimized at
an endpoint of [0, α]:
                            1              1                        f (α)     1      √
          F (α, 0) = 1 +         ≥ 1 + √ = C∗ ,          F (α, α) =       +       ≥ 2,
                          2f (α)         2 2                          2     f (α)
               √
using f (α) ≤ 2 and AM–GM. In every case C ≥ C∗ , which proves the bound.
    At C = C∗ , take the axis-parallel square centered at (1/2, 1/2) and the square at frame angle
π/4 centered at (C∗ , C∗ ), both contained√in the √
                                                  quarter plane. The center displacement
                                                                                √         projects
onto the diagonal direction to (C∗ − 12 ) 2 = ( 2 + 1)/2, exactly the sum 2/2 + 1/2 of the
two supports in that direction, so the squares touch along a common supporting line and have
disjoint interiors.

7.3    Exact gap, angle bound, and three failures
                                                                                        √
Corollary 2.2 forces two squares at vertical center gap d ∈ [0, 1] apart horizontally by 1 − d2 ,
which is exactly what their incircles already force. One might hope the squares themselves force
more; they do not.
Proposition 7.4 (Exact horizontal gap). For d ∈ [0, 1] let g(d) be the infimum of |x1 − x2 | over
pairs of interior-disjoint
              √            unit squares with centers (x1 , y1 ) and (x2 , y2 ) satisfying |y1 − y2 | = d.
Then g(d) = 1 − d2 , and the infimum is attained.
Proof. The lower bound is Corollary 2.2 with the coordinate
                                                        √ roles exchanged. The shared-
edge pair of√that corollary with common side direction ( 1 − d2 , d) has |y1 − y2 | = d and
|x1 − x2 | = 1 − d2 .
    Any improvement on the incircle contraction must therefore retain orientation or contact
information beyond the two coordinate gaps.
Proposition 7.5 (Quantitative angle bound). Let T be the triangle on the centers of three
interior-disjoint unit squares and γ its angle at a specified vertex. Then area(T ) ≥ 12 sin γ.
Proof. The two sides adjacent to the specified vertex have lengths a, b ≥ 1 by Lemma 2.1, so
area(T ) = 12 ab sin γ ≥ 21 sin γ; collinear triples give 0 ≥ 0.
   This degrades gracefully from the non-obtuse value 1/2 of Theorem 6.3 as γ → π, which is
what a branch-and-bound prover needs when non-obtuseness cannot be certified; by contrast,
the next three natural strengthenings all fail.
Proposition 7.6 (Four-center hull infimum is zero). For every ε > 0 there are four pairwise
disjoint axis-parallel unit squares whose centers are in strictly convex position with convex-hull
area less than ε.
Proof. Fix L > 1 and η > 0, and center axis-parallel unit squares at
                     p0 = (0, 0),   p1 = (L, η),   p2 = (2L, −η),     p3 = (3L, 0).
The closed horizontal projections [xi − 12 , xi + 12 ] are pairwise disjoint, so the squares are pairwise
disjoint. In the cyclic order p0 , p2 , p3 , p1 every turn has cross product 3Lη > 0, so the centers
are in strictly convex position, and the shoelace formula gives hull area 3Lη, less than ε for η
small.

                                                   21
   No hull-area analogue of the center-area lemma holds for four centers, even for axis-parallel
squares: non-obtuseness does essential work at three centers.
Remark 7.7 (No uniform second-layer gap). One might hope that a square in the wall band
(1/2 ≤ y ≤ 0.7) and a square in a second layer above it (center height at least 1.2) are forced
apart horizontally by a positive amount. They are not: the axis-parallel squares centered at
(1/2, 1/2) and (1/2, 3/2) satisfy the layer constraints and touch edge to edge with horizontal gap
0. (For center gaps δ < 1 an exact pointwise formula follows from (11) with the upper square
unconstrained; it is uniformity over the layers that fails.)

Proposition 7.8 (No chord-distribution surplus). Let 0 < D < 1, let S be a unit square whose
sides make angle θ ∈ (0, π/4] with the axes (available by the square’s symmetries; θ = 0 is
incompatible with the hypothesis below), and write c = cos θ, s = sin θ. Let ℓ1 , ℓ2 be vertical lines
at distance D from one another with the center of S between them, at distances t1 , t2 from the
center (t1 + t2 = D), and suppose each line cuts a corner triangle off S: (c − s)/2 ≤ ti ≤ (c + s)/2.
Then the chord lengths li = length(ℓi ∩ S) satisfy
                                √                                       √
                   l1 + l2 ≥ 2( 2 − D)        and      max{l1 , l2 } ≥ 2 − D,

both attained simultaneously by the square with θ = π/4 centered midway between the lines.
                              √
Proof. Put p = c + s ∈ (1, 2], so cs = (p2 − 1)/2. In the coordinates with the center of S at
the origin, a vertical line at corner-cutting distance t crosses the two sides through the extreme
vertex (p/2, (s − c)/2), at heights differing by (p/2 − t)(c/s + s/c) = (p/2 − t)/(cs); the hypothesis
on t places both crossings on those sides. Summing over the two lines,

                                           p−D       2(p − D)
                                  l1 + l2 =      =             ,
                                            cs         p2 − 1

whose p-derivative is −2 (p − D)2 + 1 − D2 /(p2 − 1)2 < 0; so the sum is minimized over
                                             
                      √                 √
orientations at p = 2, with value 2( 2 − D), and the larger chord is at least half of it.
The
 √ square with θ = π/4  √ centered midway between the lines has t1 = t2 = D/2 and chords
( 2/2 − D/2)/(1/2) = 2 − D, attaining both bounds.
               √
  √ For D  ≥ 1/  2, sliding that square between the lines realizes every split of the fixed total
2( 2 − D) between l1 and l2 , so nothing more can be extracted from the pair of chord lengths
alone.


8    Open problems
Three questions remain open.
Question 8.1. Determine T4 , the exact threshold at√which a fourth center fits, for
                                                                                √ all w < 1, and
more generally the full band structure for w < 1/ 2. Theorem 1.6 covers 1/ 2 ≤ w < 1, and
Theorem 1.3 covers everything for w ≤ τ .
Question 8.2. Is Nmax (a, b) = (⌊a⌋ + 1)(⌊b⌋ + 1) whenever a − ⌊a⌋ and b − ⌊b⌋ are sufficiently
small? Theorem 1.2 gives the upper bound (a + 1)(b + 1); the question is whether the integer-grid
maximum is locally rigid.
Question 8.3. For which convex K is the bound of Theorem 1.1 within an additive constant of
sharp? The proof loses nothing for integer rectangles; quantifying the slack for tilted strips would
sharpen its use as a pruning rule.




                                                 22
9    Lean validation
Two of the paper’s main results are machine-checked end to end in Lean 4 over mathlib [8, 6].
The source repository carries a small Lean library, PaperProofs, of wrapper theorems restating
those results in the forms used in the paper, together with the underlying formal development.

Formalized. The rectangle center bound (Theorem 1.2) is SquareFacts.CenterBound.
card le of rotated unit square centers: for any finite index type, centers in the rectangle,
unit direction vectors, and pairwise-disjoint open rotated squares, #ι ≤ (a + 1)(b + 1). The
development proves the one-square inequality (Lemma 3.2) in centered coordinates as a
product-measure statement (RotatedSquare, QuadrantScore, RectangleScore, and supporting
files, about 4,600 lines), and the integer-grid sharpness construction separately (Sharpness).
The wrapper PaperProofs.Nmax.paper rectangle center bound restates the bound, and
PaperProofs.Nmax.paper nmax rectangle integer assembles bound and sharpness into the
exact value Nmax (a, b) = (a + 1)(b + 1) for a, b ∈ N, in the project’s finite-packing presentation
(an explicit witness family together with the finite-family upper bound). The exact very-narrow
strip law (Theorem 1.3) is SquareFacts.WideStrip.nmaxValue very narrow strip, restated
as PaperProofs.Nmax.paper very narrow strip law. The band upper bounds of Theorem 1.6
are formalized on top of a formalized proof of the center-area lemma (companion development
[7]); the bridge theorem axisAlignedCentralCompactBranch from imported of the namespace
SquareFacts.ElementaryObstructions (file CenterAreaBridge) imports CenterAreaLemma.
center area lemma and discharges the geometric hypothesis, so those results are also
unconditional in Lean.

Not formalized. The convex Minkowski bound (Theorem 1.1), the cubical clipping lemma
(Lemma 4.1) behind it, and the toolbox of Section 7 are supported by the prose proofs and by
independent numerical audit only.

Build status. The complete development (the formal libraries and the wrappers) was rebuilt
end to end on 2026-08-09 with Lean v4.29.1 and mathlib v4.29.1 (8,367 build jobs). It contains no
sorry, and #print axioms on the wrapper theorems reports only the standard classical axioms
(propext, Classical.choice, Quot.sound).


Acknowledgments
This paper belongs to a larger machine-assisted project on square packing, and substantial
computer assistance went into its production. Large-language-model agents carried out the search
for proofs and counterexamples, drafted the arguments, and wrote the Lean 4 formalizations over
mathlib [8, 6] of Theorem 1.2, Theorem 1.3, the band upper bounds of Theorem 1.6, and the
center-area lemma [7] on which those bounds depend. Every closed-form constant and inequality
in the paper was subjected to an automated numerical audit, and every argument was also
checked by hand. Any remaining errors are the author’s responsibility.


References
 [1] P. Erdős and R. L. Graham, On packing squares with equal squares, J. Combin. Theory
     Ser. A 19 (1975), 119–123.

 [2] E. Friedman, Packing unit squares in squares: a survey and new results, Electron. J. Combin.,
     Dynamic Survey DS7 (2009).



                                                23
 [3] T. Gensane and P. Ryckelynck, Improved dense packings of congruent squares in a square,
     Discrete Comput. Geom. 34 (2005), 97–109.

 [4] H. Groemer, Über die Einlagerung von Kreisen in einen konvexen Bereich, Math. Z. (1960).

 [5] M. J. Kearney and P. Shiu, Efficient packing of unit squares in a square, Electron. J. Combin.
     9 (2002), #R14.

 [6] L. de Moura and S. Ullrich, The Lean 4 theorem prover and programming language, in:
     Automated Deduction – CADE 28, Lecture Notes in Comput. Sci., Springer, 2021.

 [7] D. R. MacIver, A reciprocal-force proof of the center-area lemma, in preparation.

 [8] The mathlib Community, The Lean mathematical library, in: Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs (CPP 2020), ACM,
     2020.

 [9] H. Nagamochi, Packing unit squares in a rectangle, Electron. J. Combin. 12 (2005), #R37.

[10] N. Oler, An inequality in the geometry of numbers, Mathematika (1961).

[11] R. Schneider, Convex Bodies: The Brunn–Minkowski Theory, 2nd ed., Cambridge University
     Press, 2014.

[12] W. Stromquist, Packing 10 or 11 unit squares in a square, Electron. J. Combin. 10 (2003),
     #R8.




                                               24
