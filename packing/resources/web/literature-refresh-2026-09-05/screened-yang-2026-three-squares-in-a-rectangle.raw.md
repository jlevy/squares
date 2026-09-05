                                                                     THREE SQUARES IN A RECTANGLE

                                                                                           HAOBO YANG


                                                   Abstract. For x ≥ 1, let G3 (x) be the maximum sum of the side lengths of three pairwise
                                                   interior-disjoint, arbitrarily rotated squares contained in a 1 × x rectangle. We determine this
                                                   function exactly: G3 (x) = x + 21 for 1 ≤ x ≤ 23 , G3 (x) = 2 for 32 ≤ x ≤ 2, G3 (x) = x for
arXiv:2608.13595v2 [math.MG] 27 Aug 2026




                                                   2 ≤ x ≤ 3, and G3 (x) = 3 for x ≥ 3. This completes the n = 3 case of the rectangular square-
                                                   packing question posed by Richard Stanley in a 2021 MathOverflow comment. The values for
                                                   3
                                                   2
                                                      ≤ x ≤ 3 follow from a strip theorem stating that three squares in [0, 1] × [0, H], H ≥ 2,
                                                   have total side length at most H. For x ≥ 3, the formula is immediate because each square
                                                   has side length at most 1. The range 1 ≤ x ≤ 32 is handled by combining the two-square
                                                   theorem with an additional semi-perimeter estimate for a triangle whose two nonhorizontal
                                                   sides have opposite slopes. In particular, the special case x = 2 answers the question asked
                                                   in the MathOverflow post. In connection with Erdős problem #106, we also prove that every
                                                   five-square packing in the unit square with an axis-parallel guillotine cut has total side length
                                                   at most 2.




                                                                                1. Statement and context
                                              For a positive integer n, let f (n) denote the maximum total side length of n interior-disjoint
                                           squares, of arbitrary orientation, packed into a unit square. Erdős conjectured that f (k 2 +1) =
                                           k; this is problem #106 on Bloom’s index of Erdős problems [4]. Erdős and Soifer [3] and,
                                           independently, Campbell and Staton [2] established the lower bound f (k 2 +2c+1) ≥ k+c/k for
                                           integers c with |c| < k, and conjectured that equality holds; Praton [6] showed this generalized
                                           conjecture to be equivalent to Erdős’s original conjecture,  and Singh [7]showed that the original
                                                                                                           2 + 1) − k . Staton and Tyler [8]
                                                                                              P
                                           conjecture is equivalent to the convergence of        k≥1 f  (k
                                           introduced the axis-parallel variant g(n), for which Baek, Koizumi and Ueoro [1] proved the
                                           conjectured formula. The present note concerns a rectangular variant in which rotations are
                                           unrestricted. In a 2021 comment on a MathOverflow question, Richard Stanley asked more
                                           generally for the maximum sum of the side lengths of n squares in a 1 × x rectangle, for any
                                           real x > 1 [5]. We determine this quantity exactly for n = 3 and every x ≥ 1; see Theorem 9.
                                           The main geometric ingredient is the following strip theorem.

                                           Theorem 1 (Strip Theorem). Let H ≥ 2 and let three squares with pairwise disjoint interiors
                                           lie inside the rectangle R = [0, 1] × [0, H]. The squares may be arbitrarily rotated. Then the
                                           sum of their side lengths is at most H.

                                              For H ≥ 3 this is immediate, since each side is at most 1 (see Step 1 below), so the content
                                           of the theorem is the range 2 ≤ H ≤ 3. The case H = 2 is exactly the question asked on
                                           MathOverflow in July 2021 [5]: three interior-disjoint squares in a 1 × 2 rectangle have total
                                           side length at most 2.

                                              2020 Mathematics Subject Classification. 52C15, 52C10.
                                              Key words and phrases. square packing, square packing in rectangles, rotated squares, Erdős problem 106,
                                           enclosing rectangle, semi-perimeter, separating line, guillotine cut.
                                                                                                  1
2                                           HAOBO YANG

Relation to the existing partial answers. A partial answer to the MathOverflow question
introduces two separating lines and bounds each square by the largest square inscribed in
a triangle using Pólya’s formula, but its monotonicity analysis is completed only under an
unproven auxiliary assumption a, d < 3.66 on the line parameters [5]. The proof below keeps
the same separating-line setup and replaces the inscribed-square analysis by elementary semi-
perimeter lemmas for enclosing rectangles (Section 2). This removes all restrictions on the
separating-line slopes and yields the full 1 × H statement.

Sharpness. The threshold H = 2 is sharp: for every 1 ≤ H < 2, the constructions in
Remark 7 have total side length greater than H.

Connection with Erdős problem #106. Corollary 11 shows that every five-square packing
in the unit square with an axis-parallel guillotine cut has total side length at most 2.

Notation. A square of side s with center (x, y) and orientation θ has perpendicular edge
directions u = (cos θ, sin θ) and v = (− sin θ, cos θ). Write
                                                         √
                            ρ = | cos θ| + | sin θ| ∈ [1, 2], w = sρ.
Here w is the side
                √ of the axis-aligned bounding box (both horizontal and vertical sides equal
w), and ρ ∈ [1, 2] measures how much wider than s the square becomes when rotated. For
α ∈ R set
                          ψ(α) = |α cos θ + sin θ| + | − α sin θ + cos θ|,
                                                                 √                       √
so that the width of the square  in the  unit direction  (α, 1)/   1 + α 2 equals s ψ(α)/ 1 + α2 ,
                               √        
and its half-width is s ψ(α)/ 2 1 + α2 (the support function of a square); note ψ(0) = ρ.
   Throughout, the semi-perimeter of a p × q rectangle is p + q. We use repeatedly the elemen-
tary identity
                           span{0, p, p + q} = 21 |p| + |q| + |p + q| ,
                                                                      
                                                                                            (1.1)
where span of a finite set of reals is its maximum minus its minimum, together with the fact
that if p + q + r = 0 then p+ + q+ + r+ = 12 (|p| + |q| + |r|), where x+ = max(x, 0) denotes the
positive part.

                              2. Three semi-perimeter lemmas
Fact 2 (flush enclosing rectangle). Among all rectangles, of any orientation, containing a given
convex polygon, one of minimum perimeter has a side collinear with an edge of the polygon.
Proof. This is the perimeter counterpart of the minimum-area statement obtained by rotating
calipers; compare [9]. For an angle φ, let σ(φ) be the semi-perimeter of the bounding box
of the polygon in the frame rotated by φ. Every enclosing rectangle at angle φ contains
that bounding box, hence has semi-perimeter at least σ(φ); it therefore suffices to locate the
minimum of σ, which exists since σ is continuous and π/2-periodic. By definition σ(φ) is the
sum of the lengths of the orthogonal projections of the polygon onto e1 (φ) = (cos φ, sin φ) and
e2 (φ) = (− sin φ, cos φ). Each such length equals (z − z ′ ) · ej (φ) for the pair z, z ′ of vertices
supporting the polygon in that direction; hence on any arc of angles on which these supporting
vertices do not change, both lengths are linear in (cos φ, sin φ), so σ(φ) = A cos φ + B sin φ and
σ ′′ = −σ < 0 there. Thus σ is strictly concave on such an arc and any interior critical point is
a strict local maximum; the minimum is therefore attained at an angle at which a supporting
vertex changes. At such an angle a supporting line contains an edge of the polygon, so the
corresponding side of the bounding box is collinear with that edge.                                 □
                                THREE SQUARES IN A RECTANGLE                                       3

Lemma 3. Every rectangle containing a right triangle with legs λ, µ ≥ 0 has semi-perimeter
at least λ + µ.
Proof. If λµ = 0 the triangle degenerates to a segment of length λ + µ, and any rectangle
containing it has semi-perimeter at least its diagonal, hence at least λ + µ; assume therefore
λ, µ > 0. By Fact 2 it suffices to check the orientations flush with an edge. Flush with either
     the bounding box is λ × µ, of semi-perimeter λ + µ. Flush with the hypotenuse, of length
leg, p
r = λ2 + µ2 , the box is r × λµ r (base times altitude), and
                   λµ              r2 + λµ − rλ − rµ   (r − λ)(r − µ)
                r+     − (λ + µ) =                   =                ≥ 0,
                     r                     r                 r
since r ≥ max(λ, µ).                                                                              □
Lemma 4. For a, b ∈ R let T (a, b) = conv{(0, 0), (a, 1), (b, 1)} and let C = max(0, a, b) −
min(0, a, b) be its horizontal span, so that C = 21 |a| + |a − b| + |b| by (1.1). Then every
rectangle containing T (a, b) has semi-perimeter at least
                     1 + C − |a|,      and, symmetrically,       1 + C − |b|.
Proof. We prove the first bound; the second follows by symmetry, swapping a and b. Set L =
C − |a|. One checks directly that L is the distance from b to the interval [min(0, a), max(0, a)],
so L ≥ 0.
Case 1: L = 0. Here b lies in the interval [min(0, a), max(0, a)], so the bound reduces to
1 + C − |a| = 1 + L = 1 and a crude estimate suffices. The triangle has one vertex at height
0 and another at height 1, so it contains two points whose distance is at leastp1. Any p × q
rectangle containing
               p        these two points has diagonal at least their distance, so p2 + q 2 ≥ 1.
Since p + q ≥ p2 + q 2 , we conclude p + q ≥ 1 = 1 + L.
Case 2: b on the opposite side of a. By the reflection x 7→ −x if needed we may assume
b < 0 ≤ a, so L = |b|. Since b < 0 ≤ a, the point (0, 1) lies on the top edge between (b, 1)
and (a, 1), so T (a, b) contains the right triangle ∆ = conv{(0, 0), (0, 1), (b, 1)}, whose legs are
1 and L. By Lemma 3, every rectangle containing ∆ has semi-perimeter at least 1 + L; since
T (a, b) ⊇ ∆, the same bound holds for every rectangle containing T (a, b).
Case 3: b on the same side as a. After a reflection we may assume 0 ≤ a < b, so L = b − a.
Write O = (0, 0), P = (a, 1), Q = (b, 1). By Fact 2 we check the three flush orientations.
                               √
   Flush with OP . Let ℓ = a2 + 1 = |OP |, and project onto the unit vector (a, 1)/ℓ along
OP . The images of O = (0, 0), P = (a, 1), Q = (b, 1) are
                                         a2 + 1           ab + 1
                                 0,             = ℓ,             ,
                                            ℓ                ℓ
respectively. Since 0 ≤ a < b we have ab ≥ a2 , hence ab+1
                                                        ℓ  ≥ ℓ, so the images run from 0 up to
ab+1                    2                   2
  ℓ . Using ab + 1 = (a + 1) + a(b − a) = ℓ + aL, the span along OP is
                                 ab + 1   ℓ2 + aL        aL
                                        =          =ℓ+       .
                                    ℓ         ℓ           ℓ
Perpendicular to OP , projecting onto (−1, a)/ℓ, the images of O, P, Q are 0, 0, −L/ℓ; the span
(maximum minus minimum) is therefore L/ℓ. Hence the semi-perimeter is
                             aL L     L(a + 1)
                          ℓ+    + =ℓ+          ≥ 1 + L,
                              ℓ    ℓ     ℓ
                         √
because ℓ ≥ 1 and a + 1 ≥ a2 + 1 = ℓ.
4                                          HAOBO YANG
                              √
   Flush with OQ. Let m = b2 + 1 = |OQ|, and project onto the unit vector (b, 1)/m along
OQ. The images of O, P, Q are 0, (ab + 1)/m, m, with 0 ≤ (ab + 1)/m ≤ m (the upper bound
since ab + 1 ≤ b2 + 1 = m2 , using a ≤ b), so the span along OQ is m. Perpendicular to OQ,
projecting onto (−1, b)/m, the images of O, P, Q are 0, L/m, 0, so that span is L/m. Hence
                           L              √
the semi-perimeter is m + . Since m = b2 + 1 ≥ 1 and m ≥ b ≥ L, both factors in
                          m
                       L                m2 + L − m − mL     (m − 1)(m − L)
                  m+      − (1 + L) =                     =
                       m                       m                     m
                          L
are nonnegative, so m +      ≥ 1 + L.
                          m
   Flush with P Q (the horizontal top edge). The bounding box is [0, b]×[0, 1], of semi-perimeter
b + 1 ≥ L + 1, since b ≥ b − a = L.                                                            □
Lemma 5. Let p, q ≥ 1 and let
                               Tp,q = conv{(0, 0), (−p, 1), (q, 1)}.
Every rectangle containing Tp,q has semi-perimeter at least
                                            p + q + 21 .
Proof. Put C = p + q. By Fact 2, it is enough to check the three orientations flush with an
edge of the triangle.
   Flush with the horizontal edge,
                               p the bounding box has semi-perimeter C + 1. For the edge
from (0, 0) to (−p, 1), put r = p2 + 1. Projection onto (−p, 1)/r gives the three values
                                                1 − pq
                                      0,     r,         ,
                                                   r
and projection onto the perpendicular unit vector (1, p)/r gives 0, 0, C/r. Since pq ≥ 1, the
two projection spans are pC/r and C/r; thus the semi-perimeter of this bounding box is
                                            C(p + 1)
                                                     .
                                               r
Now C ≥ p + 1 ≥ r, while
                                                   1   1
                                       r−p=           ≤ ,
                                                  r+p  2
so
                            C(p + 1)         C                1
                                      − C = (p + 1 − r) ≥ .
                                r             r               2
The orientation flush with the edge from (0, 0) to (q, 1) is symmetric. Hence every flush
bounding box, and therefore every enclosing rectangle, has semi-perimeter at least C + 12 . □

                              3. Proof of the Strip Theorem
   Let the squares be A, B, C, with sides sA , sB , sC , orientations θA , θB , θC and centers ci =
(xi , yi ), and suppose for contradiction that
                                    S := sA + sB + sC > H.
Choose ε > 0 with (1 − ε)S > H, shrink each square by the factor 1 − ε about its center, and
relabel; all the separations below are then strict, so we may argue with strict disjointness and
no touching degeneracies.
                                THREE SQUARES IN A RECTANGLE                                      5

Step 1: a common vertical line. The horizontal projection of a square has length w =
sρ ≥ s; since it must fit in [0, 1], every side satisfies si ≤ 1. In particular S ≤ 3, so for H ≥ 3
we are already done; assume from now on that 2 ≤ H < 3. For each pair,
                                si + sj = S − sk > H − 1 ≥ 1.
If two squares had horizontal projections with disjoint interiors, those projections would occupy
total length si ρi + sj ρj ≤ 1, forcing si + sj ≤ 1, a contradiction. So the three horizontal
projections pairwise overlap; intervals have the Helly property in dimension one, hence there
is a common abscissa x0 : the vertical line x = x0 meets all three squares. Their intersections
with this line are disjoint segments; order the squares along it as A (bottom), B (middle), C
(top).

Step 2: two separating lines. Disjoint compact convex sets can be separated by a line. A
line separating A from B cannot be vertical, since their horizontal projections overlap in an
open set, so its normal can be scaled to (α1 , 1); evaluating on the common vertical line shows
that A lies on the side where α1 x + y is smaller. Likewise a line with normal (α2 , 1) separates
B (below) from C (above).                                                     p
   Consider the pair A, B. Projecting onto the unit normal n1 = (α1 , 1)/ 1 + α12 , the two
squares occupy disjoint intervals, so the gap between their centers is at least the sum of their
half-widths in this direction:
                                             sA ψA (α1 ) + sB ψB (α1 )
                           n1 · (cB − cA ) ≥          p                ,
                                                     2 1 + α12
the right-hand side being the sum of
                                   p the half-widths defined in the Notation.
                                                                     p        Since n1 · (cB −
                                          2                                 2
cA ) = α1 (xB − xA ) + (yB − yA ) / 1 + α1 , multiplying through by 1 + α1 gives
                                    sA            sB
                      yB − yA ≥      2 ψA (α1 ) + 2 ψB (α1 ) − α1 (xB − xA ),                 (3.1)
                                                                p
and the same argument applied to B, C with normal n2 = (α2 , 1)/ 1 + α22 gives
                                    sB            sC
                      yC − y B ≥     2 ψB (α2 ) + 2 ψC (α2 ) − α2 (xC − xB ).                 (3.2)

Step 3: the master inequality. Adding (3.1) and (3.2), the left-hand sides telescope to
yC − yA :
            yC − yA ≥ s2A ψA (α1 ) + s2B ψB (α1 ) + ψB (α2 ) + s2C ψC (α2 ) − X,
                                                            
                                                                                  (3.3)
where
             X := α1 (xB − xA ) + α2 (xC − xB ) = −α1 xA + (α1 − α2 )xB + α2 xC .
Since each square lies in R, its center keeps half a bounding box away from every side: w2i ≤
xi ≤ 1 − w2i and w2i ≤ yi ≤ H − w2i . The vertical bounds give yC − yA ≤ H − 21 (wA + wC ), so
(3.3) becomes
          sA            sB
                                              sC            1
                                                                       
           2 ψA (α1 ) + 2 ψB (α1 ) + ψB (α2 ) + 2 ψC (α2 ) + 2 wA + wC   ≤ H + X.       (3.4)
For X we use the horizontal bounds. Each center satisfies w2i ≤ xi ≤ 1 − w2i , so for any γ ∈ R
the linear form γxi attains its maximum at one of the two endpoints, and in either case
                                                     |γ|wi
                                       γxi ≤ γ+ −          .
                                                       2
We apply this to the three terms of X, namely to −α1 xA , to (α1 − α2 )xB and to α2 xC . Their
coefficients −α1 , α1 − α2 , α2 sum to zero, so by the identity in the Notation the sum of their
6                                           HAOBO YANG

positive parts equals 21 |α1 | + |α1 − α2 | + |α2 | ; write Cα for this quantity. Adding the three
                                                   
bounds therefore gives
                        X ≤ Cα − 12 |α1 |wA + |α1 − α2 |wB + |α2 |wC .
                                                                          
                                                                                             (3.5)
Substituting (3.5) into (3.4) and moving every wi term to the left-hand side, the coefficient of
si there becomes, after wi = si ρi ,
                           KA = 21 ψA (α1 ) + ρA (1 + |α1 |) ,
                                                            

                           KB = 21 ψB (α1 ) + ψB (α2 ) + ρB |α1 − α2 | ,
                                                                      

                           KC = 21 ψC (α2 ) + ρC (1 + |α2 |) ,
                                                            

and we obtain the master inequality
                              KA sA + KB sB + KC sC ≤ H + Cα .                                (3.6)
Step 4: the coefficients are semi-perimeters. At this point the coefficients Ki are purely
algebraic, and nothing in their definition suggests a lower bound. The observation that drives
the proof is that each of them is exactly the semi-perimeter of a bounding box of a triangle
built from α1 , α2 , read in the frame of the corresponding square; Lemmas 3 and 4 then bound
them from below.
   For a bounded set V ⊂ R2 , the bounding box of V in the frame of square i, with axes ui , vi ,
has semi-perimeter span(ui · V ) + span(vi · V ). Applying (1.1) to each of the two spans, one
finds:
       • KA is the semi-perimeter of the bounding box, in the frame of A, of the right triangle
         ∆α1 = conv{(0, 0), (α1 , 0), (α1 , 1)}, whose legs are |α1 | and 1;
       • KB is the semi-perimeter of the bounding box, in the frame of B, of the triangle
         T (α1 , α2 ) of Lemma 4, whose horizontal span is exactly Cα ;
       • KC is the semi-perimeter of the bounding box, in the frame of C, of ∆α2 , whose legs
         are |α2 | and 1.
   We carry out the computation for KA ; the other two are of the same shape. The vertices of
∆α1 have uA -images 0, α1 cos θA , α1 cos θA + sin θA and vA -images 0, −α1 sin θA , −α1 sin θA +
cos θA ; both triples are of the form {0, p, p + q}, so (1.1) applies to each and the two spans add
up to
                     span(uA · ∆α1 ) + span(vA · ∆α1 )
                                                                               
                     = 21 |α1 cos θA | + |α1 sin θA | + | cos θA | + | sin θA |
                                                                                 
                          + 21 |α1 cos θA + sin θA | + | − α1 sin θA + cos θA |
                                                  
                     = 12 |α1 |ρA + ρA + ψA (α1 )
                     = 21 ψA (α1 ) + ρA (1 + |α1 |) = KA .
                                                   

The six absolute values assemble exactly into ρA , |α1 |ρA and ψA (α1 ). Each of these bounding
boxes is a rectangle containing the corresponding triangle, so Lemmas 3 and 4 give
                                       KA ≥ 1 + |α1 |,                                        (3.7)
                                       KC ≥ 1 + |α2 |,                                        (3.8)
                                       KB ≥ 1 + Cα − |α1 |,                                   (3.9)
                                       KB ≥ 1 + Cα − |α2 |.                                 (3.10)
                                    THREE SQUARES IN A RECTANGLE                                     7

Step 5: pairwise lower bounds. Let M = 2 + Cα . Then (3.7) + (3.9) and (3.8) + (3.10)
give KA + KB ≥ M and KB + KC ≥ M ; and since |α1 | + |α2 | ≥ Cα , adding (3.7) and (3.8)
gives KA + KC ≥ M as well. Adding (3.8) to KA + KB ≥ M ,
                                KΣ := KA + KB + KC ≥ M + 1.                                    (3.11)

Step 6: conclusion of the proof. Put ti = 1 − si ≥ 0, so that tA + tB + tC = 3 − S < 3 − H.
From the pairwise bounds of Step 5, each Ki ≤ KΣ − M (subtract the bound on the other two
from KΣ ), and KΣ − M ≥ 1 > 0 by (3.11). Hence
                           X                X
                               Ki si = KΣ −    Ki ti
                                i                   i
                                                                  X
                                          ≥ KΣ − (KΣ − M )            ti
                                                                  i
                                          > KΣ − (KΣ − M )(3 − H)
                                          = M + (H − 2)(KΣ − M ).
Since H − 2 ≥ 0 and KΣ − M ≥ 1, the last expression satisfies
           M + (H − 2)(KΣ − M ) ≥ M + (H − 2) = (2 + Cα ) + (H − 2) = H + Cα .
       P
Thus    i Ki si > H + Cα , contradicting (3.6) and completing the proof.                            □
Remark 6 (Attainment). For every H ∈ [2, 3] the value H is attained: three squares of sides
1, H−1 H−1
    2 , 2 , stacked vertically, have total side length 1 + (H − 1) = H.

Remark 7 (Sharpness of H ≥ 2). The threshold is sharp throughout 1 ≤ H < 2. For
1 ≤ H ≤ 32 , the three-square construction of sides 21 , 12 , H − 12 has total side length H + 21 > H.
For 32 ≤ H < 2, a unit square together with two squares of side 21 , placed side by side above
it, has total side length 2 > H.
Remark 8 (Where each ingredient is used). Convexity gives the separating lines; the square
shape is used through the support function ψ and through the fact that the projection of a
square has length at least its side; the container is used through the wall inequalities. In the
proof of the Strip Theorem, the hypothesis H ≥ 2 is used only in Step 1, to force every pairwise
sum above 1, and in Step 6, where H − 2 ≥ 0. Steps 2–5, including the master inequality and
the coefficient bounds, remain valid for every positive container height once a common vertical
line is available. No angle or slope is restricted at any point.

                          4. Three squares in a 1 × x rectangle
  Let G3 (x) denote the maximum total side length of three interior-disjoint squares, with
arbitrary orientations, contained in a 1 × x rectangle, where x ≥ 1.
Theorem 9. For every x ≥ 1,
                                             
                                             
                                             x + 12 ,   1 ≤ x ≤ 32 ,
                                             
                                                         3
                                                         2 ≤ x ≤ 2,
                                             
                                             2,
                                    G3 (x) =
                                             
                                             
                                             x,         2 ≤ x ≤ 3,
                                             
                                              3,         x ≥ 3.
                                             
8                                            HAOBO YANG

Proof. The upper bounds for x ≥ 32 are immediate from Theorem 1: for 32 ≤ x ≤ 2, enlarge
the container to a 1 × 2 rectangle; for 2 ≤ x ≤ 3, apply the theorem directly; and for x ≥ 3,
each side is at most 1.
  It remains to prove
                               G3 (x) ≤ x + 21    (1 ≤ x ≤ 32 ).
Suppose to the contrary that three squares have sides sA , sB , sC and
                                    S := sA + sB + sC > x + 12 .
As in the proof of Theorem 1, shrink the squares slightly while preserving this strict inequality,
so all separations may be taken strict. Any two of the squares lie in an x × x square, because
[0, 1] × [0, x] ⊆ [0, x]2 . Theorem 12, after scaling, therefore gives
                                       si + s j ≤ x      (i ̸= j).                           (4.1)
If, say, sA + sB ≤ 1, then adding this inequality to the two relevant instances of (4.1) gives
                        2S = (sA + sB ) + (sA + sC ) + (sB + sC ) ≤ 1 + 2x,
contrary to S > x + 12 . Hence every pairwise sum is greater than 1.
  The horizontal projections consequently overlap pairwise in their interiors, so they have a
common abscissa. Order the squares along the corresponding vertical line as A (bottom), B
(middle), and C (top). Steps 2–4 of the proof of Theorem 1 apply verbatim with H replaced
by x. Thus there are real numbers α1 , α2 and coefficients KA , KB , KC satisfying
                                KA sA + KB sB + KC sC ≤ x + Cα ,                             (4.2)
where
                                  Cα = 21 |α1 | + |α1 − α2 | + |α2 | ,
                                                                    

and (3.7)–(3.10) hold. Put
                        LA = KA − 1,       LB = KB − 1,              LC = KC − 1.
We claim that
                                 LA sA + LB sB + LC sC ≥ Cα − 12 .                           (4.3)
   Set p = |α1 | and q = |α2 |. The estimates below are symmetric in (p, sA ) and (q, sC ), so
assume p ≥ q.
   If α1 α2 ≥ 0, then Cα = p, and (3.7)–(3.10) give
                               LA ≥ p,       LB ≥ p − q,         LC ≥ q.
Consequently,
                 LA sA + LB sB + LC sC ≥ (p − q)(sA + sB ) + q(sA + sC ) ≥ p = Cα .
    Suppose next that α1 α2 < 0. Then Cα = p + q, and the same coefficient bounds give
                                 LA ≥ p,       LB ≥ p,        LC ≥ q.
If q ≤ 1, then
                                       q             q            q
           LA sA + LB sB + LC sC ≥ p −     (sA + sB ) + (sA + sC ) + (sB + sC )
                                        2              2            2
                                      q            1        1
                                 ≥ p + ≥ p + q − = Cα − .
                                      2            2        2
                                 THREE SQUARES IN A RECTANGLE                                         9

If q > 1, then after a reflection and, if necessary, interchanging p and q, the triangle T (α1 , α2 )
associated with KB in Step 4 is congruent to the triangle in Lemma 5. Hence KB ≥ Cα + 12 ,
or LB ≥ Cα − 12 . Using also sB ≤ 1 and the strict pairwise inequalities,
                                                               
                                                              1
                    LA sA + LB sB + LC sC ≥ psA + Cα −            sB + qsC
                                                              2
                                                                           1
                                             = p(sA + sB ) + q(sB + sC ) − sB
                                                                           2
                                                        1            1
                                             > p + q − sB ≥ Cα − .
                                                        2            2
This proves (4.3). Therefore
                KA sA + KB sB + KC sC = S + LA sA + LB sB + LC sC > x + Cα ,
contradicting (4.2).
  The matching constructions are axis-parallel. For 1 ≤ x ≤ 23 , use sides 12 , 12 , x − 12 ; for
3                       1 1                                x−1 x−1
2 ≤ x ≤ 2, use sides 1, 2 , 2 ; for 2 ≤ x ≤ 3, use sides 1, 2 , 2 ; and for x ≥ 3, stack three
unit squares. These attain the four displayed values.                                          □
  This completes the n = 3 case of the rectangular square-packing question posed by Richard
Stanley in a 2021 comment on [5].
  By scaling and, if necessary, interchanging the coordinate axes, Theorem 9 determines the
maximum total side length of three squares in every rectangle.
Corollary 10 (Rescaled strip form). Let F3 (u) denote the maximum total side length of three
interior-disjoint squares in [0, u] × [0, 1], where 0 < u ≤ 1. Then
                                                   
                                                   
                                                    3u,     0 < u ≤ 31 ,
                                                   
                                                              1       1
                                                   
                                                              3 ≤ u ≤ 2,
                                                   1,
                                                   
                           F3 (u) = u G3 (1/u) =              1       2
                                                   
                                                    2u,      2 ≤ u ≤ 3,
                                                   1 + u , 2 ≤ u ≤ 1.
                                                   
                                                   
                                                   
                                                         2    3

In particular, F3 (u) ≤ 2u for every 12 ≤ u ≤ 1.

               5. Axis-parallel guillotine cuts in five-square packings
Corollary 11. Let five interior-disjoint squares in the unit square have total side length S5 .
Suppose that the packing admits an axis-parallel guillotine cut, namely, an axis-parallel line
that avoids the interiors of all five squares and separates them into two nonempty subfamilies.
Then S5 ≤ 2.
Proof. After rotating the entire configuration through a right angle if necessary, we may assume
that ℓ is vertical, say ℓ = {x = t}. Reflecting in the vertical midline if necessary, we may further
assume that k squares lie on the left and 5 − k on the right, with k ∈ {1, 2}.
Case 1 + 4. The single left square, of side a, lies in [0, t] × [0, 1] and its horizontal projection
has length at least a, so t ≥ a. The other four squares lie in the right strip [t, 1] × [0, 1], of area
1 − t ≤ 1 − a, and have disjoint interiors, so their areas satisfy
                                          4
                                          X
                                                 b2i ≤ 1 − a.
                                           i=1
10                                             HAOBO YANG

                   P 2   P 2                 qP        √
                                                 b2i ≤ 2 1 − a and
                                      P
By Cauchy–Schwarz,  bi ≤ 4 bi , hence   bi ≤ 2
                                        √
                            S5 ≤ a + 2 1 − a.
Since a ≤ 1 we have 2 − a > 0, so squaring is legitimate and
            √                  √
       a + 2 1 − a ≤ 2 ⇐⇒ 2 1 − a ≤ 2 − a ⇐⇒ 4(1 − a) ≤ (2 − a)2 ⇐⇒ 0 ≤ a2 ,
which holds. Hence S5 ≤ 2.
Case 2 + 3. Let the right strip have width u, so the left one has width 1 − u. The two left
squares contribute at most min 1, 2(1 − u) : each side is at most the strip width, and the
two-square theorem (Theorem 12) in the ambient unit square caps the pair at 1. The three
right squares, in a strip u × 1, contribute at most 3u for u ≤ 31 , at most 1 for 31 ≤ u ≤ 12 , and
at most 2u for u ≥ 21 , by Corollary 10. Then
                                    u ≤ 13 :    S5 ≤ 1 + 3u ≤ 2;
                                1       1
                                3 ≤u≤ 2 :       S5 ≤ 1 + 1 = 2;
                                   u ≥ 12 :     S5 ≤ 2(1 − u) + 2u = 2.                           □
Consequence for Erdős problem #106. Consequently, any five-square packing in the unit
square with total side length greater than 2 admits no axis-parallel guillotine cut. The equality
f (5) = 2 is attributed to Newman through a personal communication to Erdős [4]; we are not
aware of a published proof.

               Appendix A. The two-square theorem and small values
Theorem 12. Two squares with disjoint interiors in the unit square, with sides a and b, satisfy
                                                a + b ≤ 1.
   The result is attributed to Erdős in an early article in a Hungarian journal for secondary-
school students; see the history notes at [4]. We give the following self-contained reconstruction.
Lemma 13 (corner depth). A square Q of side s contained in the first quadrant contains a
point z with zx ≥ s and zy ≥ s; if Q is not axis-parallel, both inequalities are strict.
                                                                                                √
Proof. Reducing the orientation modulo π/2, take θ ∈ [− π4 , π4 ] and ρ = cos θ + | sin θ| ∈ [1, 2].
The horizontal and vertical half-widths of Q are sρ/2, so its center c satisfies cx , cy ≥ sρ/2.
             s
Put z = c + 2ρ (1, 1). Then
                           s
          |(z − c) · u| = 2ρ | cos θ + sin θ| ≤ 2s ,                  s
                                                     |(z − c) · v| = 2ρ | cos θ − sin θ| ≤ 2s ,
so z ∈ Q; and zx , zy ≥ 2s ρ + ρ1 ≥ s by AM–GM, strictly if ρ > 1.
                                   
                                                                                                  □
Proof of Theorem 12. The interiors are disjoint convex sets, so a line px + qy = t separates
the squares; composing with the reflections x 7→ 1 − x and y 7→ 1 − y of the container we
may take p, q ≥ 0 with p + q > 0, and the a-square in px + qy ≤ t. Lemma 13 gives a point
z of the a-square with zx , zy ≥ a, whence t ≥ pzx + qzy ≥ a(p + q). Reflecting the b-square
through the center of the container and applying the lemma gives a point z ′ of the b-square
with zx′ , zy′ ≤ 1 − b, whence t ≤ (1 − b)(p + q). Dividing by p + q gives a + b ≤ 1.     □
Corollary 14. f (3) = 32 and f (4) = 2.
Proof. For three squares of sides a, b, c, summing a+b ≤ 1 over the three pairs gives 2(a+b+c)
                                                                                        qP ≤
                         1
                                                                                            s2i ≤
                                                                               P
3; three squares of side 2 in an L attain it. For f (4), Cauchy–Schwarz gives     si ≤ 2
2, attained by the 2 × 2 grid.                                                                  □
                                  THREE SQUARES IN A RECTANGLE                                           11

                                             References
[1] J. Baek, J. Koizumi and T. Ueoro, A note on the Erdős conjecture about square packing, preprint,
    arXiv:2411.07274 (2024).
[2] C. Campbell and W. Staton, A square-packing problem of Erdős, Amer. Math. Monthly 112 (2005), no. 2,
    165–167.
[3] P. Erdős and A. Soifer, Squares in a square, Geombinatorics 4 (1995), no. 4, 110–114.
[4] T. F. Bloom, Erdős Problem #106, https://www.erdosproblems.com/106, accessed 2026-08-25.
[5] Three squares in a rectangle, MathOverflow question 396776, asked 4 July 2021, https://mathoverflow.
    net/questions/396776.
[6] I. Praton, Packing squares in a square, Math. Mag. 81 (2008), no. 5, 358–361.
[7] A. R. Singh, On a square packing conjecture of Erdős, preprint, arXiv:2601.22163 (2026).
[8] W. Staton and B. Tyler, On the Erdős square-packing conjecture, Geombinatorics 17 (2007), no. 2, 88–94.
[9] G. T. Toussaint, Solving geometric problems with the rotating calipers, Proc. IEEE MELECON ’83, Athens,
    Greece, May 1983.

 Independent scholar
 Email address: hy2899@columbia.edu
