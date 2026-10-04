                                            A counterexample to Nagamochi’s scoring
                                            lemma and a new rectangle packing bound
                                                                                 Hakan Karakuş
                                                                        Boğaziçi University, Istanbul, Türkiye
                                                                         hakan.karakus@bogazici.edu.tr
arXiv:2609.37410v1 [math.CO] 29 Sep 2026




                                                                                 September 29, 2026


                                                                                      Abstract
                                                    Let s(N ) denote the smallest side length of a square containing N unit squares
                                                with arbitrary orientations and pairwise disjoint interiors. Nagamochi’s Packing
                                                Unit Squares in a Rectangle (2005) states a rectangle packing bound from which he
                                                deduces two infinite families of exact values: s(k 2 −1) = k and s(k 2 −2) = k for every
                                                integer k ≥ 2. We construct a family of counterexamples, local to a corner of the
                                                container, to the scoring assertion in Nagamochi’s Lemma 1. These counterexamples
                                                show that the published proof of the rectangle bound is incomplete, but do not
                                                disprove the bound itself. We then give an independent proof of a weaker rectangle
                                                bound using a strip measure. This recovers s(k 2 − 1) = k for every integer k ≥ 2
                                                and yields an explicit lower bound for s(N ) that improves strictly on the area bound
                                                for every nonsquare integer N ≥ 8. Our argument does not establish Nagamochi’s
                                                full rectangle bound or the identity s(k 2 − 2) = k.

                                           Keywords. Unit square packing; rectangle packing; unavoidable sets; weighted measures;
                                           packing bounds.


                                           1     Introduction
                                           Finite packing problems ask how small a container of a prescribed shape can be while
                                           accommodating a given number of congruent objects with disjoint interiors. Finding a
                                           dense arrangement provides an upper bound, but proving its optimality requires ruling out
                                           every better arrangement. For equal circles, non-overlap can be expressed through distances
                                           between centers; for squares, orientations introduce additional geometric constraints.
                                              For a positive integer N , let s(N ) denote the smallest side length of a square containing
                                           N unit squares with pairwise disjoint interiors, where the squares may be translated and
                                           rotated independently. Area and the usual grid packing give
                                                                               √               l√ m
                                                                                 N ≤ s(N ) ≤     N .

                                           For N = k 2 , the two bounds coincide, giving s(k 2 ) = k.
                                              This paper revisits a rectangle-packing bound stated by Nagamochi [1], from which
                                           the identities
                                                                           s(k 2 − 2) = s(k 2 − 1) = k

                                                                                           1
were deduced for every integer k ≥ 2. We give a family of counterexamples to a scoring
assertion used in the published proof. We then prove a weaker rectangle bound indepen-
dently; it recovers s(k 2 − 1) = k and yields an explicit lower bound for s(N ) that improves
strictly on the area bound for every nonsquare integer N ≥ 8.
    The square-packing problem considered here goes back at least to Erdős and Graham
[2], who showed that rotated squares can substantially reduce the unused area in large
containers compared with the usual grid construction. Göbel [3] subsequently studied the
problem systematically, and Friedman [4] surveys its history and known results. Friedman
[4, Section 1] also notes that computational methods developed for circle packing did not
readily generalize to squares.
    Among the classical exact results, Göbel [3] obtained s(5) = 2 + √12 , Kearney and
Shiu [5] proved s(6) = s(7) = 3, and Stromquist [6] proved s(10) = 3 + √12 . Friedman [4]
proved or reproved several further individual cases, including N = 8, 14, 15, 24, and 35.
Computational methods have also improved constructions without establishing optimality;
for example, Gensane and Ryckelynck [7] developed an inflation-based method that
improved the best known packings for several values of N .
    One particularly suggestive sequence occurs immediately below perfect squares. Bentz
[8] proved s(13) = 4 and s(46) = 7, and later proved s(22) = 5 and s(33) = 6 [9]. Together
with s(6) = 3, these results establish

                            s(k 2 − 3) = k,       k = 3, 4, 5, 6, 7.

These individual proofs do not establish the identity for all k. Results in the opposite
direction show that the grid construction need not remain optimal further below a perfect
square: Arslanov, Mustafin, and Shangitbayev [10] proved

                                s(k 2 − k) < k,       k ≥ 12.

Thus even near perfect squares, determining when rotations permit a smaller container
remains difficult.
   A rectangle bound stated by Nagamochi [1] would provide two infinite families of exact
values in this near-square regime. For t ≥ 2, write

                                    ∆(t) = t + 1 − ⌈t⌉.

For positive real numbers a and b, let ν(a, b) denote the maximum number of unit squares
with pairwise disjoint interiors that can be packed in some a′ × b′ rectangle with a′ < a
and b′ < b. Nagamochi [1, Theorem 1] states that, for real numbers a, b ≥ 2,

                                ν(a, b) < ab − ∆(a) − ∆(b).                             (1.1)

From this bound, Nagamochi [1, Theorem 2] derives a general lower bound for s(N ) and,
in particular,
                       s(k 2 − 1) = s(k 2 − 2) = k,   k ≥ 2.                     (1.2)
These identities have subsequently been cited in the square-packing literature as established
results; see, for example, [4, 8, 9, 10]. The validity of Nagamochi’s proof therefore matters
beyond the individual cases.
    Nagamochi’s proof assigns scores to squares by means of a central area, four weighted
line segments, and weighted points. Lemma 1 of [1] asserts a lower bound on the score
of each square; summing these scores yields the rectangle bound (1.1). These arguments

                                              2
belong to the method of unavoidable sets: one assigns resources to subsets of the container
and shows that every packed square must consume a prescribed amount. Friedman [4,
Sections 4 and 5] surveys constructions using unavoidable points, while Bentz [9, Section 2]
develops continuously varying families of unavoidable point configurations.
    We show that Nagamochi’s scoring assertion is false under the definitions in [1, Section 3].
More precisely, we identify an edge-incidence condition missing from the application of [1,
Lemma 6] in [1, Section 5.5, Case 6], and use it to construct a family of squares whose
scores are less than 1. The construction applies near a corner of every rectangle with side
lengths a > 3 and b > 2 once its parameter is sufficiently small. A further shrink about a
vertex produces a strict configuration in which the contact point lies on an edge different
from the two edges cut by y = 1.
    This counterexample shows that the published proof of (1.1) requires an additional
argument, but it does not disprove the rectangle bound itself. We instead prove the
following weaker bound by a separate method.

Theorem 1.1 (Rectangle bound). For real numbers a ≥ 2 and b ≥ 3,

                                     ν(a, b) < ab − ∆(a).                                 (1.3)

If a, b ≥ 3, applying the same construction in both directions gives

                              ν(a, b) < ab − max{∆(a), ∆(b)}.                             (1.4)

    The proof constructs a finite nonnegative measure adapted to a horizontal strip,
following Nagamochi’s general framework of weighted areas, line segments, and points.
Line mass on complete horizontal segments and point masses of 1/2 compensate for area
outside the strip. The construction and the required geometric estimates are given in
Section 5.
    Among the consequences in Section 6 are an obstruction for integer rectangles and an
explicit lower bound for s(N ) that improves strictly on the area bound for every nonsquare
integer N ≥ 8. In particular, the rectangle bound recovers one of the two near-square
identities in (1.2).

Corollary 1.2. For every integer k ≥ 2, s(k 2 − 1) = k.

    This identity is already stated in [1, Theorem 2(i)]; our contribution is a proof for k ≥ 3
independent of the failed scoring assertion. The case k = 2, namely s(3) = 2, is classical
[4, Theorem 1]. Our argument does not establish the second identity s(k 2 − 2) = k.


2     Nagamochi’s score
We use the enlarged-square formulation given in [1, Section 3, following Lemma 1], and
write σ(S) for Nagamochi’s original score. In this formulation, the container and weighted
supports are unchanged, while the square being scored has side length λ > 1. Thus the
area and line weights carry no additional factors of λ.
    Let R = [0, a] × [0, b], where a, b > 2 are arbitrary real numbers. We use strict
inequalities here so that the eight weighted points in Q below are distinct. The construction
in [1, Section 3 and Figure 1] consists of a central rectangle

                                 R∗ = [1, a − 1] × [1, b − 1],

                                               3
four line segments
                    L1 = [0.9, a − 0.9] × {1}, L2 = [0.9, a − 0.9] × {b − 1},
                                                                                                      (2.1)
                    L3 = {1} × [0.9, b − 0.9], L4 = {a − 1} × [0.9, b − 0.9],

and two sets of weighted points:1
                        Q = {(0.9, j), (a − 0.9, j) : j ∈ {1, b − 1}}
                            ∪ {(i, 0.9), (i, b − 0.9) : i ∈ {1, a − 1}},
                                                                                                      (2.2)
                        P = {(i, 0.9), (i, b − 0.9) : i = 2, . . . , ⌈a⌉ − 2}
                            ∪ {(0.9, j), (a − 0.9, j) : j = 2, . . . , ⌈b⌉ − 2}.
An index range is understood to be empty when its upper endpoint is less than 2. We
have #Q = 8 and #P = 2⌈a⌉ + 2⌈b⌉ − 12, where # denotes cardinality.
   Assign area density 1 to R∗ , line density 1/2 to each Lj , weight 9/20 to each point of
Q, and weight 1/2 to each point of P . The score of a square S ⊆ R is
                                      4
                                   1X                     9          1
       σ(S) = area(S ∩ R∗ ) +            length(S ∩ Lj ) + #(S ∩ Q) + #(S ∩ P ).                      (2.3)
                                   2 j=1                  20         2

Here length denotes Euclidean length. We also use the same score formula for Borel
subsets of R; since all weights are nonnegative, the score is monotone under inclusion. The
four line segments and the eight Q-points together contribute
                           1      9       9                           9
                                                      
                             2 a−   +2 b−                      +8·      = a + b.
                           2      5       5                          20
Adding the central area and the P -point contributions, the total score available in the
container is
                (a − 2)(b − 2) + (a + b) + (⌈a⌉ + ⌈b⌉ − 6) = ab − ∆(a) − ∆(b).                        (2.4)
Figure 1 shows the full construction in a rectangle with symbolic side lengths a and b.
   Lemma 1 of [1], in the equivalent formulation just described, requires
                                                                                    101
                  σ(S) > 1       whenever S ⊆ R has side length 1 < λ ≤                 .             (2.5)
                                                                                    100
This is the local assertion on which the published rectangle bound rests. Choose a packing
of M = ν(a, b) unit squares in an a′ × b′ rectangle with a′ < a and b′ < b, and uniformly
enlarge it inside R. The enlarged squares can then be shrunk slightly about their centers,
retaining a common side length 1 < λ ≤ 101/100 and making the closed squares pairwise
disjoint. If (2.5) were valid, summing their scores would give
                                          M
                                          X
                              ν(a, b) <         σ(Si ) ≤ ab − ∆(a) − ∆(b),
                                          i=1

by (2.4). This explains the intended deduction of (1.1) from the scoring assertion.
    We next examine the missing edge-incidence condition in Section 3. The counterexample
in Section 4 then uses only a small neighborhood of one corner, where the other weighted
supports contribute nothing.
   1
    For P , we follow [1, Figure 1], correcting the interchange of a and b in two coordinates of the printed
definition.


                                                      4
                     b
                                Q    P     P       P    P      P Q
                            Q                                        Q
                            P                  L2                    P

                            P                                        P
                                L3             R∗              L4
                            P                                        P
                                               L1
                            Q                                        Q
                                Q    P     P       P    P      P Q

                     0                                                   a

Figure 1: Nagamochi’s scoring construction in a general rectangle, drawn schematically from [1,
Section 3, Figure 1]. The central region has area density 1, the four segments have line density
1/2, the Q-points have weight 9/20 each, and the P -points have weight 1/2 each.


3     The missing edge-incidence condition
The issue occurs in [1, Section 5.5, Case 6]. We consider a > 3 and b > 2, the range used
for the counterexample below. In Case 6, the center of S lies in [1, a − 1] × [0, 1], and the
line y = 1 intersects two adjacent edges e1 and e2 of S. After symmetry and the preceding
reductions, S contains (1, 0.9), contains no point of P , and contains neither (0.9, 1) nor
(a − 1, 0.9). To estimate the score in this case, the argument considers a limiting contact
configuration with one corner of S on the x-axis and (2, 0.9) on an edge of S. It then
handles the case (1, 1) ∈ S separately and invokes [1, Lemma 6] when (1, 1) ∈   / S.
    However, [1, Lemma 6] requires that the point (2, 0.9) lie on the designated edge e2 ,
one of the two adjacent edges intersected by the line y = 1, as shown in [1, Figure 4(b)].
Contact with an arbitrary edge need not give this incidence. This suggests examining an
almost axis-parallel square for which contact with (2, 0.9) occurs on a third edge, distinct
from the two cut by y = 1, as shown in Figure 2.

                                                             y=1
                                                             y = 0.9

                                                        (2, 0.9)



                                                             y=0

Figure 2: The counterexample idea, shown schematically with separations exaggerated. The
line y = 1 cuts two adjacent edges, while (2, 0.9) lies on another edge.

   Our counterexample is designed to contain (1, 0.9), of weight 9/20, while capturing
nearly one unit of the weighted line y = 1. A sufficiently small concentric shrink moves
the boundary point (2, 0.9) outside while preserving (1, 0.9) inside and keeping the side
length greater than 1. Since the shrunken square lies inside the original square, none of

                                               5
the remaining score contributions can increase. The two dominant contributions are then
close to
                                         9    1    19
                                           + = .
                                        20 2       20
With a sufficiently small upper cap and a short intersection with the vertical weighted line,
this square can have total score less than 1. In the next section, we make this construction
explicit.


4     Constructing a counterexample
Fix arbitrary real numbers a > 3 and b > 2. We now restrict attention to squares near the
lower-left corner of R = [0, a] × [0, b]. Specifically, consider squares S satisfying

              S ⊆ [0, 3) × [0, 2),        max x < a − 1,               max y < b − 1.   (4.1)
                                          (x,y)∈S                      (x,y)∈S

The only weighted points that can meet such a square are

                  Q0 = {(0.9, 1), (1, 0.9)} ⊆ Q,             P0 = {(2, 0.9)} ⊆ P.

The segments L2 and L4 , on y = b − 1 and x = a − 1, are also disjoint from S. Thus the
complete score (2.3) reduces in this neighborhood to
                    1              1              9         1
 σ(S) = area(S∩R∗ )+ length(S∩L1 )+ length(S∩L3 )+ #(S∩Q0 )+ #(S∩P0 ). (4.2)
                    2              2              20        2
Figure 3 shows these local supports.

                               y

                                      L3
                                                        R∗

                          1          Q0
                                          Q0            P0        L1


                                                                           x
                           0               1            2
 Figure 3: The relevant part of Nagamochi’s scoring construction near the lower-left corner.

    Choose
                                1
                        0<t≤      ,     t < min{10(a − 3), b − 2}.                     (4.3)
                               50
The second condition keeps the construction away from the opposite weighted supports.
For every such rectangle, admissible values of t exist arbitrarily close to 0. Let Kt be the
contact square with vertices
                                9                 1
                                                                            
                        A= 2−     t, 0 ,   B = 2 + t, 1 ,
                               10                 10                                   (4.4)
                               1                   9
                                            
                        C = 1 + t, 1 + t , D = 1 − t, t ,
                               10                 10

                                                    6
listed in cyclic order. Its consecutive edge vectors (t, 1) and (−1, t) are perpendicular and
have equal length. Its side length therefore satisfies
                                                    s
                                   √                          1     101
                           1 < λt = 1 + t2 ≤            1+        <     .                   (4.5)
                                                             2500   100
All its coordinates are nonnegative, and
                       t
        max x = 2 +      < min{3, a − 1},               max y = 1 + t < min{2, b − 1}.      (4.6)
      (x,y)∈Kt        10                            (x,y)∈Kt

Thus Kt satisfies (4.1).
     At height y = 0.9, its horizontal cross-section is [1 − t2 , 2] × {0.9}; see (A.1). Hence
(1, 0.9) is in its interior and (2, 0.9) lies on AB. The vertex B lies exactly on y = 1, which
simplifies the calculation. Appendix A shows that Kt contains exactly one Q0 -point, that
its intersections with L1 and L3 have lengths 1 + t2 and t, and that its area inside R∗ is
t(1 + t2 )/2. Its full score includes the mass 1/2 of the boundary point (2, 0.9). Subtracting
this contribution gives
                                           1    19      1      1
                                 σ(Kt ) − =        + t + t2 + t3 .                           (4.7)
                                           2    20      2      2
The polynomial on the right is strictly increasing for t > 0 and equals 242551/250000 at
t = 1/50. Therefore,
                                                     1    242551
                             σ(Kt \ P0 ) = σ(Kt ) − ≤              < 1.                      (4.8)
                                                     2    250000
For each fixed t, shrink Kt about its center by a factor less than 1 and sufficiently close
to 1, obtaining a square St whose side length remains greater than 1 and whose interior
still contains (1, 0.9). Since St ⊆ Kt◦ , it avoids P0 and satisfies σ(St ) ≤ σ(Kt \ P0 ) < 1. Its
side length is also less than 101/100 by (4.5), so it contradicts (2.5).
     To exhibit the missing contact configuration, shrink Kt about A by a factor less than 1
and sufficiently close to 1, preserving (1, 0.9) in the interior and keeping the side length
greater than 1. The point (2, 0.9) remains in the relative interior of the image of AB. The
images of B and D lie below y = 1, while the image of C remains above it. Thus y = 1
cuts the images of BC and CD, and the contact edge is different from both. In particular,
it is not the designated edge e2 required by [1, Lemma 6]. The concentric shrink supplies
the score counterexample; the shrink about A serves only to exhibit the missing edge
incidence.


5     A strip measure for rectangles
We prove Theorem 1.1 without invoking the scoring assertion or the technical lemmas of
[1]. Following the same principle of assigning weights to areas, line segments, and points
as in [1, Section 3], we construct a finite nonnegative measure adapted to a horizontal
strip. Its total mass is ab − ∆(a), while the interior of every square of side length slightly
greater than 1 has measure greater than 1.
    Fix a ≥ 2 and b ≥ 3, set R = [0, a] × [0, b], and define
                       H = [0, a] × [1, b − 1],
                      L− = [0, a] × {1},
                      L+ = [0, a] × {b − 1},
                      W = {(j, 4/5), (j, b − 4/5) : j = 1, . . . , ⌈a⌉ − 1}.

                                                7
Assign area density 1 to H, line density 1/2 to each of L− and L+ , and point mass 1/2 to
each point of W . For a Borel set E ⊆ R, define
                              1                  1                 1
    µ(E) = area(E ∩ H) +        length(E ∩ L− ) + length(E ∩ L+ ) + #(E ∩ W ).            (5.1)
                              2                  2                 2
Here area is two-dimensional Lebesgue measure, and length on each supporting line is
one-dimensional Lebesgue measure. The two rows of W are distinct and each contains
⌈a⌉ − 1 points. Thus µ is a finite nonnegative measure, with total mass
                                       a a 1
                   µ(R) = a(b − 2) +    + + (2⌈a⌉ − 2) = ab − ∆(a).                       (5.2)
                                       2 2 2
Figure 4 shows the construction. For each packed square S, we estimate µ(S ◦ ), the mass
in its interior.

                          b
                                  W        W    W        W   W      W
                     b−1
                                                    L+

                                                    H

                                                    L−
                         1
                                  W        W    W        W   W      W

                         0                                                  a

Figure 4: The strip measure in a rectangle. The two rows of point masses have integer abscissae
strictly between 0 and a, at heights 4/5 and b − 4/5.


Proposition 5.1. Every square S ⊆ R of side length 1 < λ ≤ 101/100 satisfies µ(S ◦ ) > 1.
    The upper bound 101/100 is a convenient choice, also used in [1]. We first establish
elementary geometric estimates. They play roles analogous to the chord and cap estimates
in [1, Lemmas 2–5], but the proofs below are independent of those assertions.
Lemma 5.2 (Estimates near a horizontal boundary). Let S ⊆ {y ≥ 0} be a square of side
1 < λ ≤ 101/100 whose center has height at most 1. Then the following hold.
                               √        √
  (i) For every r satisfying 3−2 2 < r < 2 − 12 ,

                                    length(S ◦ ∩ {y = r}) > 1.

 (ii) For A = area(S ∩ {y ≥ 1}) and ℓ = length(S ◦ ∩ {y = 1}),
                                                ℓ       λ
                                           A+     ≥ λ2 − .
                                                2       2

Proof. Up to reflection and relabeling of the sides, use an orientation 0 ≤ θ ≤ π/4. Let

                       h = sin θ + cos θ        and      p = sin θ cos θ.

                                                8
For θ > 0, the horizontal chord length at height z above the lowest vertex is
                             z
                              ,
                                          0 < z < λ sin θ,
                             p
                             
                             
                             
                              λ
                             
                 w(z) =              ,     λ sin θ ≤ z ≤ λ cos θ,                              (5.3)
                             
                              cos θ
                              λh − z
                             
                             
                             
                                     ,    λ cos θ < z < λ(sin θ + cos θ) = λh.
                                 p
                             


Proof of (i). Let zc denote the height of the center of S. Since S ⊆ {y ≥ 0}, the vertical
distance from the center of S to its lowest point gives zc ≥ λh/2. By hypothesis, zc ≤ 1.
    If θ = 0, then h = 1, so λ/2 ≤ zc ≤ 1. The lower and upper sides of S therefore have
heights
                     λ        λ    1                        λ
                zc − ≤ 1 − < < r              and      zc + ≥ λ > 1 > r,
                     2        2    2                        2
respectively. Thus the line y = r crosses the two vertical sides of S, and the resulting
chord has length λ > 1.
    Suppose henceforth that θ > 0. Let
                                                         λh
                                             z0 = zc −
                                                          2
be the height of the lowest vertex of S. Since
                                             λh
                                                ≤ zc ≤ 1,
                                              2
the relative height of the line y = r above this vertex,
                                                              λh
                                         r − z0 = r − zc +       ,
                                                               2
ranges between
                               λh
                              z− = +r−1      and     z+ = r.
                                2
Both values lie strictly between 0 and λh. Since the chord profile (5.3) is concave on
its support, it is enough to check these two endpoint positions. We first record two
trigonometric bounds.                 √
    We use p = (h2 − 1)/2 and 1 ≤ h ≤ 2, which give
                                            √      1
                                         h−p≥ 2 − > r,                                  (5.4)
                                                   2
                                          √
                                 h           2−1
                                   −p≥             > 1 − r.                             (5.5)
                                 2            2
                                                                  √
Both expressions
       √         on the left are decreasing functions of h on [1,  2], so their minima occur
at h = 2.
   Since z− < λh/2 ≤ λ cos θ, the height z− lies in the lower triangle or the plateau.
Hence
                                              !
                      z−   1      h
                     
                         >          + r − 1 > 1 by (5.5), 0 < z− < λ sin θ,
                          p    p   2
                     
          w(z− ) =                                                                             (5.6)
                          λ
                               > λ > 1,                              λ sin θ ≤ z− ≤ λ cos θ.
                     
                     
                     
                         cos θ

                                                   9
                                √       √
   Similarly, λ sin θ ≤ 101/(100 2) < 3−2 2 < z+ , so the height z+ lies in the plateau or
the upper triangle. Thus
                     
                         λ
                             > λ > 1,               λ sin θ ≤ z+ ≤ λ cos θ,
                     
                     
                     
                       cos θ
                     
            w(z+ ) =  λh − z     h−r                                                    (5.7)
                              +
                     
                               >     > 1 by (5.4), λ cos θ < z+ < λh.
                           p        p
                     


   Both endpoint chords have length greater than 1, proving (i).
Proof of (ii). Since zc ≤ 1 and the highest point has height zc + λh/2 ≥ λh > 1, the line
y = 1 intersects the square at or above its center. It therefore either cuts two opposite
sides or bounds an upper triangular cap.
    If the line cuts two opposite sides, the chord profile (5.3) gives
                                                                                  !
                  λ              λ2     λ               λ2     λ      λh
             ℓ=       ,       A=    −       (1 − zc ) ≥    −       1−    .
                cos θ            2    cos θ             2    cos θ     2
Consequently,
                                     !
                      ℓ       λ                 λ
                   A + − λ2 −            ≥           (λ sin θ + cos θ − 1) ≥ 0,
                      2       2              2 cos θ
because λ sin θ + cos θ ≥ sin θ + cos θ ≥ 1. This also covers the axis-parallel orientation
θ = 0.
   If the line creates an upper triangular cap, the chord profile (5.3) and p > 0 give
                                                                           !
             zc + λh/2 − 1   λh − 1                  ℓ      λh      (λh − 1)2
          ℓ=               ≥        ,             A=   zc +    −1 ≥           .
                   p           p                     2       2         2p
Consequently,                                 !
                             ℓ       λ                 λ
                          A + − λ2 −              ≥       (λ − h + p) ≥ 0,
                             2       2                 2p
because 2p = h2 − 1 and λ − h + p > 1 − h + p = (h − 1)2 /2 ≥ 0.
    For a square S ⊆ R satisfying the lemma’s hypotheses, taking r = 4/5 in Lemma 5.2(i)
shows that S ◦ ∩{y = 4/5} is an open interval of length greater than 1. Its set of abscissae is
an open interval of length greater than 1 contained in [0, a], and hence contains an integer
in {1, . . . , ⌈a⌉ − 1}. Thus S ◦ contains at least one weighted point of W , contributing 1/2
to µ(S ◦ ).
Proof of Proposition 5.1. Let zc be the height of the center of S.
Centers near the bottom or top. Suppose first that zc ≤ 1. Its maximum height is at most
                                              √
                                λ         101 2
                          zc + √ ≤ 1 +            < 2 ≤ b − 1.
                                 2          200
Thus S cannot lose weighted area through the top of H; its area contribution is exactly A
from Lemma 5.2(ii). Lemma 5.2(i) supplies a weighted point in the interior, contributing
mass 1/2. Combining the two estimates gives
                                λ 1                  1
                                                                      
                          ◦     2
                     µ(S ) ≥ λ − + = 1 + (λ − 1) λ +   > 1.
                                2 2                  2

                                                  10
Reflection in y = b/2 proves the same assertion when zc ≥ b − 1.
Centers in the strip. It remains to consider 1 ≤ zc ≤ b − 1. Call a horizontal boundary of
H a proper cut if S has positive area on both sides of that line. Every proper cut either
removes a triangular cap or meets the interiors of two opposite sides of S.
    For a triangular cap with side lengths u, v ≤ λ measured along two adjacent sides of S,
let D be its area and ℓ its base length. Then
                                                √
                           D         uv           uv    λ     1
                              = √ 2         ≤ √ ≤ √ < .                               (5.8)
                            ℓ    2 u +v   2     2 2    2 2    2

Thus the line mass ℓ/2 more than compensates for the lost area.
    If every proper cut is triangular, compensate every triangular loss using (5.8). The
area and line contributions are at least λ2 > 1.
    If exactly one proper cut is not triangular, its chord has length at least λ. The center
is on the retained side, so at most half the square’s area is lost through that boundary.
Compensating any triangular loss at the other boundary gives

                                                   λ2 λ
                                       µ(S ◦ ) ≥     + > 1.
                                                   2  2
    If both proper cuts are nontriangular, their line contributions alone total at least λ > 1.
    These cases include b = 3, when a square can cross both horizontal boundaries of the
strip. They also account for tangencies, since only proper cuts require compensation. This
completes the proof.
Proof of Theorem 1.1. Let M = ν(a, b), and choose an a′ × b′ rectangle with a′ < a and
b′ < b admitting a packing of M unit squares. Choose λ sufficiently close to 1 that
                                       101
                           1<λ≤            ,         λa′ < a,         λb′ < b.
                                       100
Uniformly scaling the packing by λ gives squares S1 , . . . , SM of side λ with pairwise disjoint
interiors inside R. By additivity and nonnegativity of µ, Proposition 5.1, and (5.2),
                           M                   M
                                                           !
                                 µ(Si◦ ) = µ         Si◦
                           X                   [
                     M<                                        ≤ µ(R) = ab − ∆(a).
                           i=1                 i=1

This proves (1.3). When a, b ≥ 3, rotating the construction gives M < ab − ∆(b) as well.
Taking the stronger of the two inequalities yields (1.4).


6     Consequences for rectangle and square packings
For integer target side lengths, the correction ∆ equals 1, giving the following obstruction.

Corollary 6.1 (Integer rectangles). Let m, n ≥ 2 be integers. No m′ × n′ rectangle with
m′ < m and n′ < n can contain mn − 1 unit squares with pairwise disjoint interiors.

Proof. By interchanging the two directions, assume n ≥ m. If n ≥ 3, Theorem 1.1 with
a = m and b = n gives ν(m, n) < mn − ∆(m) = mn − 1. If m = n = 2, the smaller
rectangle is contained in a square of side max{m′ , n′ } < 2, which cannot contain three
unit squares by the classical identity s(3) = 2 [4, Theorem 1].

                                                     11
Proof of Corollary 1.2. Taking m = n = k in Corollary 6.1 shows that k 2 − 1 unit squares
cannot fit in a square of side less than k. The k × k grid with one square removed gives
the reverse inequality, so s(k 2 − 1) = k.
  The rectangle theorem also gives an explicit lower bound for every nonsquare integer
N ≥ 8.

Corollary 6.2 (A general lower bound). Let N ≥ 8 be a nonsquare integer. Then
                                             s
                                 1                    √    1 √
                          s(N ) ≥ +              N − ⌊ N⌋ + > N.                      (6.1)
                                 2                         4
                  √
Proof. Let k = ⌊ N ⌋. Since N is a nonsquare integer, k 2 < N ≤ (k + 1)2 − 1. By
Theorem 1.1, any t ≥ 3 satisfying t2 − ∆(t) = N gives s(N ) ≥ t. On the interval
k < t ≤ k + 1, we have ∆(t) = t − k, so this equation becomes t2 − t + k = N . The positive
root of this quadratic is                  s
                                       1               1
                                  t= + N −k+ .
                                       2               4
The inequalities for N give
                                        2                         2
                                    1                   1      1
                                                          
                               k−            <N −k+       ≤ k+
                                    2                   4      2
and therefore k < t ≤ k + 1. Hence ⌈t⌉ = k + 1, and by construction

                                t2 − ∆(t) = t2 − t + k = N.

   We also have t ≥ 3: for N = 8, the formula gives t = 3, while for N > 8 the nonsquare
assumption implies k ≥ 3 and hence t > k ≥ 3. If N unit squares could be packed in a
square of side less than t, then Theorem 1.1, applied with a = b = t, would give

                                N ≤ ν(t, t) < t2 − ∆(t) = N,

a contradiction. Thus s(N ) ≥ t.
   Finally, since t > k,
                                        t2 = N + t − k > N,
                √
and hence t >       N.
   For N = n2 − 1 with n ≥ 3, the lower bound in (6.1) is exactly n. Thus the family in
Corollary 1.2 also occurs at the endpoints of this general bound.


7    Concluding remarks
Section 4 gives a local family violating the scoring assertion in [1, Lemma 1]. The family
applies near a corner of every rectangle with a > 3 and b > 2 once the parameter is
sufficiently small. Shrinking the same contact square about a vertex produces a strict
configuration exhibiting the missing edge-incidence condition in the application of [1,
Lemma 6]. The published derivation of the rectangle bound and its consequences therefore
requires a correction or an additional argument; the family is not itself a packing that
violates those bounds.

                                                   12
    The strip measure provides a partial replacement for Nagamochi’s theorem. For a, b ≥ 3,
it yields the correction max{∆(a), ∆(b)} in place of ∆(a) + ∆(b). Its consequences include
the integer-rectangle obstruction, the lower bound (6.1), and an independent proof of
                                      s(k 2 − 1) = k.
Thus one of the two nontrivial infinite near-square families stated in [1, Theorem 2] is
recovered without the disputed scoring assertion. The present argument does not establish
or disprove Nagamochi’s full rectangle bound, the identity
                                      s(k 2 − 2) = k,
or the stronger general lower bound stated in [1, Theorem 2].
    This leaves a natural geometric question. The strip measure charges only one pair
of opposite sides of the container and has total mass ab − ∆(a); after rotation it gives
the corresponding correction in the other direction. Can the two boundary corrections
be combined without creating a square of mass at most 1? For a square container [0, k]2 ,
such a construction would need total mass k 2 − 2 rather than the k 2 − 1 supplied by the
present strip measure. A successful construction of this kind could provide a new route
toward the unresolved part of Nagamochi’s claimed bound.
    More broadly, the issue illustrates the difficulty of rigorous lower bounds in square
packing. Numerical and geometric constructions can often suggest very efficient arrange-
ments, whereas an optimality proof must control every possible translation and orientation.
Weighted measures and unavoidable-set arguments remain useful precisely because they
turn this global packing problem into local geometric inequalities, but the counterexample
here shows that the incidence conditions underlying those inequalities must be tracked
carefully.

Use of AI tools. AI tools were used during exploratory work, for symbolic and numerical
checks, and for language and typesetting assistance. All mathematical arguments and
calculations appearing in the article were independently checked by the author.


A     Calculations for the counterexample
We verify the contact-square score (4.7) used in Section 4. Throughout this appendix,
a > 3, b > 2, and t satisfies (4.3). The square Kt has vertices (4.4), with edge directions
B − A = C − D = (t, 1) and D − A = C − B = (−1, t).

Weighted point contributions. Parametrize AB by A + s(t, 1), where 0 ≤ s ≤ 1. At
height y = 0.9, we have s = 9/10, giving the right endpoint
                                         9     9
                                           
                                    2−      t + t = 2.
                                         10    10
Similarly, on DC, parametrized by D + s(t, 1), the same height gives s = 9/10 − t and the
left endpoint
                                   9         9
                                               
                             1− t +t           − t = 1 − t2 .
                                  10        10
Both parameter values lie strictly between 0 and 1, so the chord is
                           Kt ∩ {y = 0.9} = [1 − t2 , 2] × {0.9}.                    (A.1)

                                            13
Thus (1, 0.9) lies in Kt◦ , and (2, 0.9) lies on AB. Moreover,
                                               9     491
                                min x = 1 −       t≥     > 0.9,
                              (x,y)∈Kt         10    500

so the point column x = 0.9 is disjoint from Kt . Together with (4.6), this excludes all
remaining weighted points. Hence

                           #(Kt ∩ Q0 ) = 1,           #(Kt ∩ P0 ) = 1,                     (A.2)

and the total point contribution is 9/20 + 1/2.

Intersection with the horizontal weighted line. The vertex B lies on y = 1. On
the opposite edge DC, the parametrization D + s(t, 1) reaches this height at s = 1 − t. Its
abscissa is
                                   9                   1
                                    
                             1 − t + t(1 − t) = 1 + t − t2 .
                                  10                  10
The full chord lies within L1 , giving
                                       1             1
                                                              
                          Kt ∩ L1 = 1 + t − t2 , 2 + t × {1}.                              (A.3)
                                       10           10
Subtracting the endpoints yields

                                   length(Kt ∩ L1 ) = 1 + t2 .                             (A.4)

The left endpoint lies strictly to the right of x = 1, since t/10 − t2 > 0. In particular, (1, 1)
is outside Kt .

Intersection with the vertical weighted line. The upper intersection with x = 1
lies on DC. Its first coordinate equals 1 when
                                      9                         9
                                1−      t + st = 1,       s=      ,
                                     10                        10
giving height 0.9 + t. The lower intersection lies on AD, parametrized by A + s(−1, t). Its
first coordinate equals 1 when
                                    9                             9
                              2−      t − s = 1,       s=1−         t,
                                   10                            10
giving height t(1 − 9t/10) < t ≤ 1/50 < 0.9. Since L3 starts at height 0.9 and extends
beyond 0.9 + t, it follows that

                  Kt ∩ L3 = {1} × [0.9, 0.9 + t],         length(Kt ∩ L3 ) = t.            (A.5)

Area inside the central region. The upper vertex C lies to the right of x = 1, as
does the full chord (A.3). Together with (4.6), this shows that the portion above y = 1 is
entirely inside R∗ = [1, a − 1] × [1, b − 1]. It is a triangle with base 1 + t2 and height t, so
                                                   t
                                   area(Kt ∩ R∗ ) = (1 + t2 ).                             (A.6)
                                                   2

                                               14
The contact-square score. Substituting (A.2), (A.4), (A.5), and (A.6) into (4.2) gives

                    9  1 1      2   t t(1 + t2 )   29      1    1
          σ(Kt ) =    + + (1 + t ) + +           =    + t + t2 + t3 .
                   20 2 2           2     2        20      2    2
Subtracting the boundary point’s mass 1/2 yields (4.7).


References
 [1] Hiroshi Nagamochi, Packing Unit Squares in a Rectangle, The Electronic Journal of
     Combinatorics 12(1) (2005), Research Paper 37, 13 pp. doi:10.37236/1934.

 [2] Paul Erdős and Ronald L. Graham, On Packing Squares with Equal Squares, Journal
     of Combinatorial Theory, Series A 19(1) (1975), 119–123.
     doi:10.1016/0097-3165(75)90099-0.

 [3] F. Göbel, Geometrical Packing and Covering Problems, in Packing and Covering in
     Combinatorics, A. Schrijver (ed.), Mathematical Centre Tracts 106 (1979), 179–199.

 [4] Erich Friedman, Packing Unit Squares in Squares: A Survey and New Results, The
     Electronic Journal of Combinatorics, Dynamic Survey 7, version of August 14, 2009.
     doi:10.37236/28.

 [5] Michael J. Kearney and Peter Shiu, Efficient Packing of Unit Squares in a Square,
     The Electronic Journal of Combinatorics 9(1) (2002), Research Paper 14.
     doi:10.37236/1631.

 [6] Walter Stromquist, Packing 10 or 11 Unit Squares in a Square, The Electronic
     Journal of Combinatorics 10(1) (2003), Research Paper 8. doi:10.37236/1701.

 [7] Thierry Gensane and Philippe Ryckelynck, Improved Dense Packings of Congruent
     Squares in a Square, Discrete & Computational Geometry 34(1) (2005), 97–109.
     doi:10.1007/s00454-004-1129-z.

 [8] Wolfram Bentz, Optimal Packings of 13 and 46 Unit Squares in a Square, The
     Electronic Journal of Combinatorics 17(1) (2010), Research Paper 126.
     doi:10.37236/398.

 [9] Wolfram Bentz, Optimal Packings of 22 and 33 Unit Squares in a Square,
     arXiv:1606.03746 [math.CO] (2016).

[10] M. Z. Arslanov, S. A. Mustafin, and Z. K. Shangitbayev, Improved Packings of
     n(n − 1) Unit Squares in a Square, The Electronic Journal of Combinatorics 28(4)
     (2021), Paper 4.22. doi:10.37236/8586.




                                          15
