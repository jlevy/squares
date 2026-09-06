                                               How many contacts can exist between oriented squares of various
                                                                           sizes?
                                                                                              Sean Dewar∗
arXiv:2210.10422v2 [math.CO] 25 Oct 2023




                                                                                                Abstract
                                                         A homothetic packing of squares is any set of various-size squares with the same orientation
                                                     where no two squares have overlapping interiors. If all n squares have the same size then we can
                                                     have up to roughly 4n contacts by arranging the squares in a grid formation. The maximum
                                                     possible number of contacts for a set of n squares will drop drastically, however, if the size of
                                                     each square is chosen more-or-less randomly. In the following paper we describe a necessary and
                                                     sufficient condition for determining if a set of n squares with fixed sizes can be arranged into a
                                                     homothetic square packing with more than 2n − 2 contacts. Using this, we then prove that any
                                                     (possibly not homothetic) packing of n squares will have at most 2n − 2 face-to-face contacts if
                                                     the various widths of the squares do not satisfy a finite set of linear equations.

                                           MSC2020: 05B40, 52C15, 52C05
                                           Keywords: square packings, homothetic packings, contact graphs


                                           1        Introduction
                                           Throughout the paper we fix S := {(x, y) : −1 ≤ x, y ≤ 1} to be the standard square and
                                           [n] := {1, . . . , n} to be the first n positive integers. A homothetic copy of a set A ⊂ Rd is any set

                                                                                      rA + p := {rx + p : x ∈ A},

                                           for some scalar r > 0 and some point p ∈ Rd . With this, we define a homothetic packing of n
                                           squares, or homothetic square packing for short, to be any set P = {S1 , . . . , Sn } of homothetic
                                           copies of S where for each distinct pair i, j ∈ [n], the interiors Si◦ and Sj◦ of the sets Si and Sj
                                           respectively are disjoint. Given each square in P is of the form Si = ri S + pi , we can characterise
                                           P uniquely by two types of variables: the positive scalar radii r1 , . . . , rn and the 2-dimensional
                                           real vector centres p1 , . . . , pn . The contact graph G = ([n], E) of P is the (simple) graph where
                                           {i, j} ∈ E if and only if i 6= j and Si ∩ Sj 6= ∅. See Figure 1 for an example of a homothetic square
                                           packing and its corresponding contact graph.
                                                An immediate question one can ask is the following: what is the upper bound on the number of
                                                                                                                                 √
                                           contacts for a homothetic packing of n squares? It is easy to see that roughly 4n − 6 n + 2 contacts
                                               ∗
                                                   School of Mathematics, University of Bristol. E-mail: sean.dewar@bristol.ac.uk


                                                                                                     1
Figure 1: A homothetic square packing with 11 contacts. The edges of its contact graph are
represented by the coloured lines.

can be achieved; given n = n1 n2 squares with the same radii, the homothetic square packing formed
by arranging the squares in a n1 × n2 grid has 4n − 3(n1 + n2 ) + 2 contacts. However it is easy to
see that this type of packing (or any similar packing formed by replacing square blocks of k2 unit
squares with a single square of radii k) forces the radii to satisfy some rational linear constraints.
    What, then, should the maximum number of contacts be for a homothetic square packing if the
radii are picked more-or-less randomly? Although our previous construction proves that around
4n contacts are indeed possible, one very quickly notices that this is not the case if the radii of
the squares are chosen at random. We encourage the reader now to construct n squares of various
widths (whether from paper or other means) and try to arrange them in a way that maximises the
amount of contacts while keeping the squares oriented in the same way. It becomes apparent very
quickly that the most amount of contacts possible is never more than 2n − 2, no matter how the
squares are arranged.
    Our main result of this paper is that the maximum number of contacts achievable by a homo-
thetic packing of n squares will exceed 2n − 2 if and only if the radii of the chosen squares satisfy
some very basic linear constraints.
Theorem 1.1. Let r1 , . . . , rn be positive scalars. Then the following statements are equivalent:
  (i) Every homothetic packing of n squares with radii r1 , . . . , rn has at most 2n − 2 contacts.

 (ii) The only function σ : [n] → {−1, 0, 1} with at least 4 zeroes that satisfies the equation
      Pn
       i=1 σi ri = 0 is the zero function.

   In [1], Connelly, Gortler and Theran proved an analogous result to Theorem 1.1 for disc packings
(the definition of a disc packing being identical to that of a homothetic square packing except with
the square S replaced by the closed unit disc).
Theorem 1.2 ([1]). Let r1 , . . . , rn be positive scalars that are mutually distinct and form an alge-
braically independent set. Then every packing of n discs with radii r1 , . . . , rn has at most 2n − 3
contacts.
   Although similar, Theorems 1.1 and 1.2 do differ in a few specific ways. Connelly, Gortler
and Theran proved Theorem 1.2 by constructing a smooth manifold of disc packings with a given

                                                   2
contact graph, and then showing that any disc packing with algebraically independent radii will be
a regular point of a projection. Our method for homothetic square packings, however, only requires
very simple concepts from geometry and combinatorics. Furthermore, Theorem 1.1 describes both
a sufficient and necessary condition for a set of radii to generate packings with a low amount of
contacts, while Theorem 1.2 only provides a sufficient condition.
    Theorem 1.2 was in recent years also extended to homothetic packings of any convex body
C ⊂ R2 (a compact convex set with non-empty interior), so long as the convex body is also
centrally symmetric (x ∈ C if and only if −x ∈ C), strictly convex (every point on the boundary of
C is contained in a supporting hyperplane of C that intersects C at exactly one point) and smooth
(every point on the boundary of C is contained in exactly one supporting hyperplane of C). Any
such set is also known as a regular symmetric body.

Theorem 1.3 ([3]). For every regular symmetric body C and every positive integer n ∈ N, there
exists a conull1 set of vectors (r1 , . . . , rn ) in Rn>0 so that the following holds: every packing of n
homothetic copies of C with radii r1 , . . . , rn has at most 2n − 2 contacts.

    Although a square is a convex body, it is neither strictly convex nor smooth, and hence is
not covered by Theorem 1.3. In any case, Theorem 1.3 is a noticeably weaker result than both
Theorems 1.1 and 1.2 as it does not describe either a necessary or a sufficient condition for a given
set of radii to only generate packings with low numbers of contacts.
    The paper is structured as follows. In Section 2 we introduce the various types of contacts
a homothetic square packing can have, and use this to define red and blue edge colourings for
a homothetic square packing’s contact graph. In Section 3 we investigate the effect the weak
generic condition (see Definition 3.1) has on the cycles in the induced red and blue subgraphs
of the contact graph. These techniques are then applied to proving Theorem 1.1 in Section 4. In
Section 5 we use Theorem 1.1 to obtain analogous results for square packings that allow for rotated
squares (Corollary 5.2). We conclude the paper in Section 6 by proving that the natural analogue
of Theorem 1.1 cannot be extended to homothetic cube packings
Remark 1.4. A homothetic square packing can be considered to be a bar-and-joint framework in
the normed space (R2 , k · k∞ ) by modelling the centres as points in R2 , the edges as ℓ∞ -norm
distance equalities between points (to simulate squares in contact), and the non-edges as strict
ℓ∞ -norm distance inequalites (to simulate squares not intersecting). Whilst we will avoid using the
language of bar-and-joint framework rigidity theory here, we do direct interested readers to the
work of Kitson and Power for more information about the topic [4].


2        Contact graphs for homothetic square packings
Unless stated otherwise, a homothetic square packing P = {S1 , . . . , Sn } will have contact graph
G = ([n], E), centres p1 , . . . , pn and radii r1 , . . . , rn . We also denote the x- and y-coordinates of a
centre pi to be xi , yi , i.e., pi = (xi , yi ). If two distinct squares Si and Sj are in contact, at least one
of two possible cases holds.
    1
        A set is conull if its complement is a null set, i.e., has Lebesgue measure zero.


                                                               3
  (i) If ri + rj = |xi − xj | ≥ |yi − yj | then Si and Sj have an x-direction contact; equivalently,
      Si and Sj have an x-direction contact if and only if Si ∩ Sj = {(a, t) ∈ R2 : b ≤ t ≤ c} for
      some a, b, c ∈ R with b ≤ c.

 (ii) If ri + rj = |yi − yj | ≥ |xi − xj | then Si and Sj have a y-direction contact; equivalently, Si
      and Sj have a y-direction contact if and only if Si ∩ Sj = {(t, a) ∈ R2 : b ≤ t ≤ c} for some
      a, b, c ∈ R with b ≤ c.

The intersection of Si and Sj will always contain the point
                                                          !                                            !
                     ri (xi − xj )        ri (yi − yj )                rj (xi − xj )        rj (yi − yj )
       pij :=   xi −               , yi −                     =   xj +               , yj +               .   (1)
                        ri + rj              ri + rj                      ri + rj              ri + rj

If two squares have both an x-direction and y-direction contact then Si ∩ Sj = {pij }, and pij will be
a corner of both of Si and Sj . In fact, this is the only way two squares in a homothetic packing can
intersect at a single point. See Figure 2 to see a diagram of the possible types of contact between
two squares.




Figure 2: Three possible types of contact between two squares: an x-direction contact represented
by a red edge (left), a y-direction contact represented by a blue edge (middle) and a x- and y-
direction contact represented by a red-blue pair of parallel edges (right). Although the latter type
of contact is represented by two parallel edges, it will still be considered to be a single contact.

    Using this extra information about the edges of the contact graph, we now define Ex , Ey ⊂ E
to be the sets of x-direction and y-direction edges respectively. With this notation, we have that
Ex ∪ Ey = E and Ex ∩ Ey is exactly the set of contacts with a single point in the intersection.
When drawing the contact graph of a homothetic square packing, we shall always represent the
edges in the set Ex \ Ey by a red line, the edges in the set Ey \ Ex by a blue line, and the edges in
the set Ex ∩ Ey by both a red line and a blue line. Importantly, these “double edges” are still only
counted as a single edge in our contact graph. See Figure 2 to see how the different contacts are
represented. Interestingly, the subgraphs ([n], Ex ), ([n], Ey ) must always be triangle-free.

Lemma 2.1. Let P be a homothetic packing of n squares. Then the coloured subgraphs ([n], Ex ),
([n], Ey ) of the contact graph G = ([n], E) are triangle-free.



                                                          4
Proof. It suffices to prove that ([n], Ex ) is triangle-free since rotating P by 90◦ will switch the edges
Ex and Ey . Suppose for contradiction that ([n], Ex ) contains a triangle. By relabelling vertices of
G we may suppose that {1, 2, 3} is a clique in ([n], Ex ) and x1 ≤ x2 ≤ x3 . Since ri + rj = |xi − xj |
for 1 ≤ i < j ≤ 3, all three x1 , x2 , x3 must be distinct, i.e., x1 < x2 < x3 . Hence

                    x2 − x1 = r1 + r2 ,        x3 − x1 = r1 + r3 ,        x3 − x2 = r2 + r3 .

By summing all three equations and halving the result, we have that x3 −x1 = r1 +r2 +r3 . However
this now implies that r2 = 0, contradicting that all radii are positive.

   One special way that one of the graphs ([n], Ex ) or ([n], Ey ) can contain a cycle is for four
squares to share an intersection as seen in Figure 3; if this occurs, we say the four squares share
a corner.




                                  Figure 3: Four squares sharing a corner.

   As we shall soon prove, the only way to generate cliques with more than three vertices is with
four squares sharing a corner. We first need to cover the following famous result of Helly.

Theorem 2.2 (Helly’s theorem; see, for example, [2]). Let C = {C1 , . . . , Cn } be a set of convex
sets in Rd where n ≥ d + 1. If every d + 1 distinct sets in C have a non-empty intersection, then
Tn
  i=1 Ci 6= ∅.

   We require the following two special cases of Theorem 2.2 where the set C contains only homo-
thetic copies of the standard square S.

Lemma 2.3. Let C = {S1 , . . . , Sn } be a set of pairwise-intersecting homothetic copies of S. Then
Tn
 i=1 Si 6= ∅.

Proof. Define πx , πy : R2 → R to be the linear projections where πx (x, y) = x and πy (x, y) = y for
each point (x, y) ∈ R2 . Since the sets in C are pairwise-intersecting, so too are the sets in both
{πx (S1 ), . . . , πx (Sn )} and {πy (S1 ), . . . , πy (Sn )}. By Theorem 2.2, there exists points x′ , y ′ ∈ R such
that x′ ∈ ni=1 πx (Si ) and y ′ ∈ ni=1 πy (Si ). Equivalently, given each square Si is of the form
                T                         T

[ai , bi ] × [ci , di ], we have ai ≤ x′ ≤ bi and ci ≤ y ′ ≤ di . Hence (x′ , y ′ ) ∈ Si for each i ∈ [n].

Lemma 2.4. Let P be a homothetic packing of n squares. If {i, j, k} is a clique in the contact
graph G = ([n], E), then Si ∩ Sj ∩ Sk contains exactly one point.

                                                         5
Proof. By relabelling vertices we may assume that {1, 2, 3} is the clique in G. By Lemma 2.3, the
set S1 ∩ S2 ∩ S3 is non-empty, hence it is sufficient to prove that S1 ∩ S2 ∩ S3 contains at most one
point. If any of the sets S1 ∩ S2 , S1 ∩ S3 or S2 ∩ S3 contain exactly one point then S1 ∩ S2 ∩ S3
contains at most one point. Suppose instead that all three sets S1 ∩ S2 , S1 ∩ S3 and S2 ∩ S3 contain
more than one point. Then each distinct pair Si , Sj has either an x- or y-direction contact, but not
both. By Lemma 2.1, one of these distinct pairs has an x-direction contact and another distinct
pair has a y-direction contact. As the intersection of two perpendicular line segments is either an
empty set or a single point, the set S1 ∩ S2 ∩ S3 contains at most one point.

   The previous two lemmas allow us to characterise the cliques in the contact graph of any given
homothetic square packing.

Lemma 2.5. Let P be a homothetic packing of n squares. Then any clique of the contact graph
G = ([n], E) has size at most 4, and any clique of size 4 will correspond to 4 squares sharing a
corner.

Proof. By relabelling the vertices, suppose that {1, . . . , k} is a clique of G with k ≥ 4. By
Lemmas 2.3 and 2.4, there exists a unique point z in the intersections of the squares S1 , . . . , Sk .
Furthermore, z must lie on the boundary of each square S1 , . . . , Sk by our assumption that P is a
homothetic square packing. The interior of each square Si covers an angle αi of points around z.
For each i ∈ [k], we either have αi = π and z lies on exactly one face of Si , or αi = π/2 and z is a
corner of Si . As ki=1 αi ≤ 2π, we see that k ≤ 4, with equality if and only if S1 , S2 , S3 , S4 share a
                  P

corner.

   Interestingly, no two distinct cliques of size 4 in the contact graph can share three vertices.

Lemma 2.6. Let P be a homothetic packing of n squares. If K, K ′ are two distinct cliques of size
4 in G = ([n], E), then |K ∩ K ′ | ≤ 2.

Proof. By relabelling the vertices of G, we may suppose that K = {1, 2, 3, 4} and K ′ = {1, 2, 3, 5}.
As the sets {1, 2, 3, 4} and {1, 2, 3, 5} are cliques in G, the squares S1 , S2 , S3 , S4 intersect at a point
z and the squares S1 , S2 , S3 , S5 intersect at a point z ′ . Since z, z ′ ∈ S1 ∩ S2 ∩ S3 , it follows from
Lemma 2.4 that z = z ′ . However this implies that z ∈ S4 ∩ S5 , contradicting that G can contain
no cliques of size 5 (Lemma 2.5).

    Before we can deduce more properties of the contact graph, we require the following technical
result regarding the straight-line embedding of the contact graph; i.e., the mapping of G into the
plane where a vertex i is considered to be the point pi and an edge is considered to be the closed
line segment
                                             
                                [pi , pj ] := tpi + (1 − t)pj : t ∈ [0, 1] .

Lemma 2.7. Let P be a homothetic packing of n squares. Choose any edge {i, j} ∈ E and let
pij = (xij , yij ) be the point described in eq. (1). Then the following holds.

  (i) The closed line segment [pi , pj ] is contained in Si ∪ Sj .


                                                      6
 (ii) The set [pi , pj ] \ {pij } is contained in the set Si◦ ∪ Sj◦ (and hence in the interior of Si ∪ Sj ).

(iii) The point pij lies in the interior of the set Si ∪ Sj if and only if {i, j} ∈
                                                                                  / Ex ∩ Ey .

Proof. Fix pi = (xi , yi ) and pj = (xj , yj ). Given a point z = (x, y) ∈ [pi , pij ], we note that
|x − xi | ≤ ri and |y − yi | ≤ ri , with equality in one of these inequalities if and only if z = pij . An
analogous observation can be made for any point in the line segment [pj , pij ], hence (i) and (ii)
hold. It now suffices for us to check whether pij lies in (Si ∪ Sj )◦ .
    First suppose that {i, j} ∈ Ex ∩ Ey . By rotating P we may suppose that xi < xj and yi < yj .
For any t > 0, the point pij + (t, −t) is not contained in Si ∪ Sj as

                  |xij + t − xi | = ri + t > ri      and        |yij − t − yj | = rj + t > rj .

Hence pij does not lie in (Si ∪ Sj )◦ .
   Now suppose, without loss of generality, that {i, j} ∈ Ex \ Ey and xi < xj . Fix
                                      (                                        )
                                          ri |yi − yj |        rj |yi − yj |
                            ε := min ri −               , rj −                     > 0.
                                            ri + rj              ri + rj

Choose any s ∈ (xi − ri , xj + rj ) and t ∈ (−ε, ε). Then the point pij + (s, t) lies in Si ∪ Sj as
xi + ri = xj − rj and

                                                            ri (yi − yj )
                                  |yij + t − yi | ≤ |t| +                 ≤ ri ,
                                                               ri + rj
                                                            rj (yi − yj )
                                  |yij + t − yj | ≤ |t| +                 ≤ rj .
                                                               ri + rj

As this holds for any choice of s, t, the point pij lies in (Si ∪ Sj )◦ .

      If four squares do share a corner, then the straight-line embedding of G given by the centres
p1 , . . . , pn will not be planar. Fortunately, this is the only way that planarity can be lost.

Lemma 2.8. Let P be a homothetic packing of n squares. Then the following properties hold for
any pair of edges {i, j}, {k, ℓ} ∈ E that share no vertices.

  (i) The interiors of the sets Si ∪ Sj and Sk ∪ Sℓ are disjoint.

 (ii) If the closed line segments [pi , pj ] and [pk , pℓ ] intersect, then the squares Si , Sj , Sk , Sℓ share a
      corner, the edges {i, j}, {k, ℓ} lie in both Ex and Ey , and the edges {i, k}, {i, ℓ}, {j, k}, {j, ℓ}
      lie in the symmetric difference of Ex and Ey (denoted by Ex △Ey ).

Proof. (i): Suppose for contradiction that the interiors of the sets Si ∪ Sj and Sk ∪ Sℓ are not
disjoint. Let Rij and Rkℓ be the relative interiors of the convex sets Si ∩ Sj and Sk ∩ Sℓ respectively.
Then (Si ∪ Sj )◦ = Si◦ ∪ Sj◦ ∪ Rij and (Sk ∪ Sℓ )◦ = Sk◦ ∪ Sℓ◦ ∪ Rkℓ . Since the interiors of the squares
in P are pairwise disjoint, the sets Si◦ ∪ Sj◦ and Sk◦ ∪ Sℓ◦ must be disjoint. Hence we have, without
loss of generality, that Rij 6= ∅ and Rij ∩ (Sk ∪ Sℓ )◦ 6= ∅. By rotating and translating P if necessary,

                                                       7
we may further assume that Rij = {(s, 0) ∈ R2 : a < s < b} for some a, b ∈ R with a < b. Choose
a sufficiently small scalar ε > 0 such that the open neighbourhood
                                      n                                           o
                               ε
                              Rij := (s, t) ∈ R2 : a < s < b, − ε < t < ε

of Rij is contained in (Si ∪ Sj )◦ . Since Rij intersects (Sk ∪ Sℓ )◦ non-trivially and non-empty open
sets always have positive area,2 the intersection of the open sets Rij  ε and (S ∪ S )◦ is a non-empty
                                                                                   k     ℓ
open set with positive area. Since both Rij and Rkℓ are null sets (i.e., have zero area), it follows
that Rijε \ R (and hence S ◦ ∪ S ◦ ) intersects S ◦ ∪ S ◦ non-trivially, thus forcing a contradiction.
              ij               i     j              k    ℓ
    (ii): By Lemma 2.7(i) we have that [pi , pj ] ⊂ Si ∪ Sj and [pk , pℓ ] ⊂ Sk ∪ Sℓ . By Lemma 2.7(ii)
and Lemma 2.7(iii), {i, j} ∈ Ex △Ey if and only if [pi , pj ] is contained in the interior of the set
Si ∪ Sj , and {k, ℓ} ∈ Ex △Ey if and only if [pk , pℓ ] is contained in the interior of the set Sk ∪ Sℓ .
As shown in (i), the interiors of Si ∪ Sj and Sk ∪ Sℓ are disjoint. Since [pi , pj ] and [pk , pℓ ] are not
disjoint, it follows that {i, j}, {k, ℓ} ∈ Ex ∩ Ey . By Lemma 2.7(ii) and Lemma 2.7(iii), pij (see
eq. (1)) is the unique point in [pi , pj ] not contained in the interior of Si ∩ Sj . Similarly, pkℓ is the
unique point in [pk , pℓ ] not contained in the interior of Sk ∩ Sℓ . Since [pi , pj ] and [pk , pℓ ] intersect
non-trivially but the interiors of Si ∪ Sj and Sk ∪ Sℓ do not, we have pij = pkℓ . Hence {i, j, k, ℓ} is
a clique in G. By Lemma 2.5, the squares Si , Sj , Sk , Sℓ share a corner.
    Suppose for contradiction that {i, k} ∈ Ex ∩ Ey . Then (i, j, k) is a cycle of length 3 in either
([n], Ex ) or ([n], Ey ), contradicting Lemma 2.1. Hence {i, k} ∈ Ex △Ey . By repeating the above
argument we see that the edges {i, ℓ}, {j, k}, {j, ℓ} also lie in Ex △Ey , thus completing the proof.

   Interestingly, Lemma 2.8 also allows us to develop an easy-to-obtain upper bound for the max-
imum number of contacts possible in any homothetic square packing. It is worth mentioning that
                                                                              √
the upper bound is not best possible; indeed, the author believes that 4n − 6 n + 2 is the best-
possible upper bound for the maximum number contacts for a homothetic packing of n squares (the
construction to obtain this upper bound is outlined in Section 1). As far as the author is aware,
the upper bound given below is the lowest known upper bound.

Proposition 2.9. Any homothetic packing of n ≥ 3 squares has at most 4n − 8 contacts.

Proof. Let P be a homothetic square packing with contact graph G = ([n], E) and centres p1 , . . . , pn .
Let A be the set of cliques of size 4 contained in G. Choose any clique K = {i, j, k, ℓ} ∈ A.
By Lemma 2.5, the squares Si , Sj , Sk , Sℓ all share a corner. Without loss of generality we may
suppose {i, j}, {k, ℓ} are the unique edges supported on K that lie in Ex ∩ Ey . Note that if
we remove the edge {i, j}, the two cliques {i, k, ℓ} and {j, k, ℓ} will now form facial triangles in
the straight-line embedding given by the centres of P . For each clique K we now choose an
edge eK ∈ Ex ∩ Ey supported on K and let TK , TK       ′ be the two corresponding facial triangles

that result from the removal of eK . Note that for two distinct cliques K, K ′ ∈ A, the triangles
      ′ , T ′ , T ′ must all be pairwise distinct by Lemma 2.6. Define the subgraph G′ = ([n], E ′ )
TK , TK    K     K′
by setting E := E \ {eK : K ∈ A}. By Lemma 2.8(ii), G′ is planar and the straight-line embedding
               ′

   2
    As all sets in the plane mentioned throughout the paper are Lebesgue-measurable, we define the area of a set by
using the Lebesgue measure on R2 .


                                                        8
given by the vertex map i 7→ pi is a planar embedding. Furthermore, for every K ∈ A the triangles
TK and TK  ′ are facial triangles of G′ with respect to the aforementioned straight-line embedding.

It follows from Euler’s formula that any embedding of a planar graph with n vertices has at most
2n − 4 triangle faces. As every edge eK pairs up two triangles of the embedded graph G′ and no
triangle is paired up more than once, we see that |A| ≤ n − 2. Since G′ is planar, it has at most
3n − 6 edges. Thus |E| = |E ′ | + |A| ≤ (3n − 6) + (n − 2) = 4n − 8 as required.

    Before we close the section, we first mention the following interesting result of Schramm.

Theorem 2.10 ([5]). Let G = ([n], E) be a planar graph with a planar embedding where every
interior face is a triangle, the outer cycle of the embedded graph has length 4, and the only cycle of
length at most 4 that contains vertices inside its interior is the outer cycle. Then G is the contact
graph of a homothetic square packing P .

     Whilst being a very interesting result with a particularly beautiful proof – for example, the proof
involves observing a correspondence between square tilings and a concept known as an extremal
metric – we unfortunately cannot utilise Theorem 2.10 because of two important reasons. Firstly,
Theorem 2.10 only applies to a very specific family of contact graphs: planar graphs with 3n − 7
edges and no “small” cycles containing a vertex in their interior. This assumption can be weakened
to allow for any planar graphs with 3n − 7 edges, however the cost of doing so is that some squares
could potentially have a radius of zero (something we are explicitly not allowing). Secondly, the
union of the squares in the corresponding homothetic square packing will form a rectangle, and so
it is fairly easy to see that the radii cannot satisfy condition (ii) of Theorem 1.1.


3    The weak generic condition
We begin the section with the following definition.

Definition 3.1. The radii of a homothetic square packing are said to satisfy the weak generic
condition if they satisfy condition (ii) of Theorem 1.1.

     It should be noted that almost all choices of radii will satisfy the weak generic condition; indeed
it is sufficient that the radii form an algebraically independent set. In this section we use the weak
generic condition to determine certain properties about cycles in the coloured graphs ([n], Ex ) or
([n], Ey ). We first require the following technical lemma.

Lemma 3.2. Let P be a homothetic packing of n ≥ 6 squares. Suppose that the radii satisfy
the weak generic condition. Further suppose that there exists a cycle (n1 , . . . , nk ) in the coloured
subgraph ([n], Ex ) such that for each i ∈ [k], neither xni−1 < xni < xni+1 nor xni+1 < xni < xni−1
(here we set xn0 = xnk and xnk+1 = xn1 ). Then k = 4 and the four squares Sn1 , Sn2 , Sn3 , Sn4 share
a corner.

Proof. We first note that for the x-coordinates of the cycle (n1 , . . . , nk ) to have the required “zigzag-
ging” property, k must be even (and hence k ≥ 4). By translating and reflecting P , we may assume


                                                     9
that xni = (−1)i rni for each i ∈ [k]. By shifting and reversing the order of the cycle (n1 , . . . , nk ) as
required, we may also suppose that yn1 ≤ yni for all i ∈ [k] and yn2 ≤ ynk . We note that our new
ordering will imply yn1 < yni for all odd i ∈ [k] \ {1}, and yn2 < ynk , as otherwise the interiors of
some of the squares in the packing will intersect.
    Choose any distinct i, j ∈ [k]. We now investigate two cases. In our first case, suppose that
i ≡ j mod 2 and yni ≤ ynj . So that Sni and Snj do not overlap, we must have yni < ynj . As

                                  |xni − xnj | = |rni − rnj | < rni + rnj

and the interiors of the squares Sni and Snj do not intersect, it follows that

                                          yni + rni ≤ ynj − rnj .                                        (2)

For our second case, suppose that {ni , nj } ∈ E and yni − rni ≤ ynj − rnj . As {ni , nj } ∈ Ex , we
have |yni − ynj | ≤ rni + rnj . The following two inequalities, however, cannot hold:

                             yni − rni < ynj − rnj < ynj + rnj < yni + rni                               (3)
                             yni − rni = ynj − rnj < yni + rni = ynj + rnj                               (4)

The inequality given by eq. (3) cannot hold as, given nℓ is the single other vertex adjacent to nj
in the cycle (n1 , . . . , nk ) (ignoring all other edges of the contact graph), the interiors of the two
squares Sni and Snℓ will be forced to intersect so that both have an x-direction contact with Snj .
The inequality given by eq. (4) also cannot hold as it implies rni = rnj , contradicting the weak
generic condition (since n ≥ 6). With this, we are left with 5 cases possible inequalites when
{ni , nj } is an edge in the cycle (n1 , . . . , nk ):
  (i) yni − rni < yni + rni = ynj − rnj < ynj + rnj .

 (ii) yni − rni < ynj − rnj < yni + rni < ynj + rnj .

(iii) yni − rni < ynj − rnj < yni + rni = ynj + rnj .

 (iv) yni − rni = ynj − rnj < yni + rni < ynj + rnj .

 (v) yni − rni = ynj − rnj < ynj + rnj < yni + rni .
    We now use this analysis for the vertices n1 , n2 , nk to obtain some inequalities. By assumption
we have yn1 ≤ yn2 < ynk . First note that, as k is even (and hence k ≡ 2 mod 2), yn2 +rn2 ≤ ynk −rnk
by eq. (2). Suppose that yn2 − rn2 ≤ yn1 − rn1 . As yn1 ≤ yn2 , it follows that yn2 − rn2 ≤ yn2 − rn1 ,
which in turn implies rn1 < rn2 (as rn1 6= rn2 by the weak generic condition). Hence yn1 + rn1 <
yn2 + rn2 , and so the only possible case that can hold is case (v) with j = 1 and i = 2, i.e.,

                            yn1 − rn1 = yn2 − rn2 < yn1 + rn1 < yn2 + rn2 .

However, since yn2 + rn2 ≤ ynk − rnk , this implies yn1 + rn1 < ynk − rnk , contradicting that
{n1 , nk } ∈ Ex . Hence yn1 − rn1 < yn2 − rn2 . Now suppose that ynk − rnk ≤ yn1 − rn1 . As before,
we see that the only possibility is for case (v) to hold with j = 1 and i = k, i.e.,

                            yn1 − rn1 = ynk − rnk < yn1 + rn1 < ynk + rnk .


                                                     10
However, since yn2 + rn2 ≤ ynk − rnk and yn1 − rn1 < yn2 − rn2 , this implies yn2 + rn2 < yn2 − rn2 ,
a contradiction. Hence yn1 − rn1 < ynk − rnk . It follows that for each ℓ ∈ {2, k}, one of cases (i),
(ii), or (iii) holds with i = 1 and j = ℓ. By observing the possible cases for i = 1, j = k, we see
that ynk − rnk ≤ yn1 + rn1 . From this, both cases (i) and (ii) quickly run into a contradiction when
i = 1 and j = 2. Hence case (iii) holds for i = 1 and j = 2, i.e.,
                             yn1 − rn1 < yn2 − rn2 < yn1 + rn1 = yn2 + rn2 .                              (5)

As yn2 + rn2 ≤ ynk − rnk , the only possible case that can hold for i = 1 and j = k is case (i), i.e.,
                             yn1 − rn1 < yn1 + rn1 = ynk − rnk < ynk + rnk .                              (6)
    Now we turn our attention to the vertex n3 . Since 1 ≡ 3 mod 2, we have yn1 < yn3 and
yn1 + rn1 ≤ yn3 − rn3 by eq. (2). Hence yn2 + rn2 ≤ yn3 − rn3 and ynk − rnk ≤ yn3 − rn3 by eqs. (5)
and (6). It follows that case (i) holds for i = 2 and j = 3, and hence
               yn1 − rn1 < yn2 − rn2 < yn1 + rn1 = yn2 + rn2 = ynk − rnk = yn3 − rn3 .                    (7)

From this we observe that the squares S1 , S2 , S3 , Sk share a corner, with {n1 , n2 }, {n3 , nk } ∈ Ex \Ey ,
{n1 , n3 }, {n2 , nk } ∈ Ey \ Ex , and {n1 , nk }, {n2 , n3 } ∈ Ex ∩ Ey .
     Suppose for contradiction that k > 4 (i.e., k ≥ 6). Then, since 2 ≡ 4 mod 2 and yn2 ≤ yn4 , we
have yn2 +rn2 ≤ yn4 −rn4 by eq. (2). Hence by eq. (7), ynk −rnk ≤ yn4 −rn4 . If yn4 −rn4 < ynk +rnk
then |yn4 − ynk | < rn4 + rnk , which, when combined with |xn4 − xnk | < rn4 + rnk , contradicts that
the interiors of Sn4 and Snk are disjoint. Hence ynk + rnk ≤ yn4 − rn4 . Since ynk − rnk < ynk + rnk
and yn3 − rn3 = ynk − rnk (eq. (7)), we have yn3 − rn3 < yn4 − rn4 . As one of cases (i), (ii) and
(iii) must hold for i = 3 and j = 4, we have yn4 − rn4 ≤ yn3 + rn3 . By combining this with the
previous inequality of ynk + rnk ≤ yn4 − rn4 , we have ynk + rnk ≤ yn3 + rn3 . If ynk + rnk = yn3 + rn3
then, since ynk − rnk = yn3 − rn3 (eq. (7)), we would have rn3 = rn4 , contradicting the weak generic
condition. Thus
                                             ynk + rnk < yn3 + rn3 .                                      (8)
Now observe the vertex nk−1 . If yn3 ≤ ynk−1 then by eqs. (2) and (8) we have
                                 ynk + rnk < yn3 + rn3 ≤ ynk−1 − rnk−1

which implies |ynk − ynk−1 | > rnk + rnk−1 , contradicting that {nk−1 , nk } ∈ E. Thus ynk−1 < yn3 ,
and so, since k is even and (k − 1) ≡ 3 mod 2,
                                        ynk−1 + rnk−1 ≤ yn3 − rn3                                         (9)
by eq. (2). By applying eq. (2) with i = 1 and j = k − 1 (since k is even), and then applying the
substitutions from eq. (7), we see that
                                        ynk − rnk ≤ ynk−1 − rnk−1 .                                      (10)
However by combining eqs. (7), (9) and (10) we see that

                        ynk−1 + rnk−1 ≤ yn3 − rn3 = ynk − rnk ≤ ynk−1 − rnk−1
contradicting that rnk−1 > 0. Hence k = 4, completing the proof.

                                                     11
    Using the previous technical result, we now prove that the weak generic condition forces all
cycles in ([n], Ex ) and ([n], Ey ) to either be very long or generated by four squares sharing a corner.

Lemma 3.3. Let P be a homothetic square packing with contact graph G = ([n], E), radii r1 , . . . , rn
and centres p1 , . . . , pn . Suppose that the radii satisfy the weak generic condition. If either of the
graphs ([n], Ex ), ([n], Ey ) contains a cycle (n1 , . . . , nk ) with k ≤ n − 2, then k = 4 and the squares
Sn1 , Sn2 , Sn3 , Sn4 share a corner.

Proof. Without loss of generality, we will assume (n1 , . . . , nk ) is a cycle of ([n], Ex ). We will also
fix that n0 := nk and nk+1 := n1 . By Lemma 2.1, k ≥ 4. Let pi = (xi , yi ) for each i ∈ [n]. Define
the function σ : [n] → {−1, 0, 1}, where for each i ∈ [n] we have:
                            
                            
                            
                            
                            
                              1    if i = nj for some j ∈ [k] and xnj−1 < xnj < xnj+1 ,
                    σi :=    −1 if i = nj for some j ∈ [k] and xnj+1 < xnj < xnj−1 ,
                            
                            
                            0
                            
                                   otherwise.

Fix s, t ∈ [k] to be distinct points where xns ≤ xni ≤ xnt for each i ∈ [k]. By our choice of σ we
must have σns = σnt = 0. As k ≤ n − 2, it follows that the map σ has at least 4 zeroes. We observe
the following property for any i ∈ [k]:
                                     xni+1 − xni    xni − xni−1
                                                  +               = 2σni .
                                    |xni+1 − xni | |xni − xni−1 |

Adding this observation to the fact that (n1 , . . . , nk ) is a cycle of ([n], Ex ), we have that
                 k                     k                                         k                    n
                 X                     X xni+1 − xni                             X                    X
            0=         xni+1 − xni =                          (rni + rni+1 ) =         2σni rni = 2         σi ri .
                 i=1                   i=1
                                             |xni+1 − xni |                      i=1                  i=1

Hence σi = 0 for all i ∈ [n], as the radii satisfy the weak generic condition. This implies that our
cycle is “zigzagging”, i.e., for each i ∈ [k] we have that either xni−1 < xni and xni+1 < xni , or
xni−1 > xni and xni+1 < xni . The result now follows from Lemma 3.2.

   Our next goal of this section is to prove the following: if one of the coloured subgraphs contain
a sufficiently long cycle, then the weak generic condition will imply that the number of edges in
the contact graph is bounded above by 2n − 2. We first need the following technical lemma.

Lemma 3.4. Let P be a homothetic square packing with contact graph G = ([n], E), radii r1 , . . . , rn
and centres p1 , . . . , pn . If the radii of P satisfy the weak generic condition, then G does not contain
the subgraph pictured in Figure 4.

Proof. Let H be the graph pictured in Figure 4. Suppose for contradiction that G contains a copy
of H. Note that, as the radii r1 , . . . , rn satisfy the weak generic condition, the radii r1 , . . . , r6 satisfy
the weak generic condition. Hence without loss of generality we may assume that G contains H
as a spanning subgraph (i.e., n = 6). By relabelling the vertices of G we may assume H has the
vertex labelling described in Figure 4.

                                                          12
                                             1      2     3



                                             4      5     6


           Figure 4: The forbidden subgraph of Lemma 3.4 with vertices labelled 1 to 6.

    As {1, 2, 4, 5} (respectively, {2, 3, 5, 6}) is a clique, by Lemma 2.5 and Lemma 2.8(ii) there exist
exactly two edges supported on {1, 2, 4, 5} (respectively, {2, 3, 5, 6}) that are contained in Ex ∩ Ey ,
and these two edges do not share any vertices. Suppose that {2, 5} ∈ Ex ∩ Ey . Then the edges
{2, 5}, {1, 4}, {3, 6} are contained in Ex ∩Ey and the rest of the edges of H are contained in Ex △Ey .
It follows from Lemmas 2.4 and 2.7 that the point p25 described in eq. (1) is the unique point in the
set S1 ∩ S2 ∩ S4 ∩ S5 and also the unique point in the set S2 ∩ S3 ∩ S5 ∩ S6 . Hence p25 is contained
in every square of P . However this implies G contains a clique of size 6, contradicting Lemma 2.5.
Hence {2, 5} cannot be both an x- and y-direction contact.
    By relabelling the vertices of H, we can assume that the edges {1, 5}, {2, 4}, {2, 6}, {3, 5} are
contained in Ex ∩ Ey and the rest of the edges of H are contained in Ex △Ey . By rotating P we
may assume that {2, 5} ∈ Ey (and hence {2, 5} ∈          / Ex ). Hence the edges of H have the following
colouring:

                                             1      2     3



                                             4      5     6


Note that (2, 4, 5, 6) is a cycle in ([n], Ex ). As the radii of P satisfy the weak generic condition and
4 ≤ n − 2, {2, 4, 5, 6} is a clique in G and {4, 6} ∈ E by Lemma 3.3. However the edge {4, 6} forms
a cycle of length 3 in both ([n], Ex ) and ([n], Ey ), contradicting Lemma 2.1.

   We are now ready to prove the final key lemma of the section.

Lemma 3.5. Let P be a homothetic square packing with contact graph G = ([n], E), radii r1 , . . . , rn
and centres p1 , . . . , pn . Suppose that the radii satisfy the weak generic condition. If either of the
subgraphs ([n], Ex ), ([n], Ey ) contains a cycle (n1 , . . . , nk ) with k ≥ n − 1, then |E| ≤ 2n − 2.

Proof. Without loss of generality, we will assume (n1 , . . . , nk ) is a cycle of ([n], Ex ); this can be
achieved by rotating P by 90◦ if necessary. If n = 4 then |E| ≤ 2n − 2. If n = 5 with |E| > 2n − 2
then G contains two cliques of size 4 sharing 3 vertices, which contradicts Lemma 2.6. Hence we
may assume n ≥ 6.
    Suppose that (n1 , . . . , nk ) has a chord. By Lemmas 2.1 and 3.3, any cycles of ([n], Ex ) or
([n], Ey ) have length 4, n − 1 or n, and any cycle of length 4 is generated by four squares sharing
a corner. So that the chord does not create a forbidden cycle in ([n], Ex ), we must have k = 6 and

                                                   13
the chord must split the cycle into two cycles of length 4, each of which generated by four squares
sharing a corner. However this implies that G contains a copy of the graph pictured in Figure 4,
contradicting Lemma 3.4. Hence the cycle (n1 , . . . , nk ) is chordless in ([n], Ex ). It follows that the
vertex set {n1 , . . . , nk } cannot induce cycles of length 4 in either ([n], Ex ) or ([n], Ey ); any cycle
of length 4 in the subgraph of ([n], Ey ) induced by {n1 , . . . , nk } necessitates a cycle of length 4 in
the subgraph of ([n], Ex ) induced by {n1 , . . . , nk } (Lemma 3.3), contradicting that (n1 , . . . , nk ) is a
chordless cycle of ([n], Ex ). In particular, no four squares in the set {n1 , . . . , nk } can share a corner.
    Let pi = (xi , yi ) for each i ∈ [n]. By relabelling the vertices (but maintaining that the order
(n1 , . . . , nk ) forms a cycle), we will assume that xn1 ≤ xni for all i ∈ [k]. Fix s ∈ [k] to be an index
where xns ≥ xni for all i ∈ [k]. Define the function σ : [n] → {−1, 0, 1}, where for each i ∈ [n] we
have:
                           
                           
                           
                           
                           
                             1     if i = nj for some j ∈ [k] and xnj−1 < xnj < xnj+1 ,
                   σi :=    −1 if i = nj for some j ∈ [k] and xnj+1 < xnj < xnj−1 ,
                           
                           
                           0
                           
                                   otherwise

(here we set n0 = nk and nk+1 = n1 ). We now note four immediate properties of the map σ: (i)
σn1 = σns = 0; (ii) if σni 6= 0, then σni+1 is either 0 or equal to σni ; (iii) if σni = 1 (respectively,
σni = −1) and σni+1 = . . . = σni+m = 0 6= σni+m+1 for some m, then σni+m+1 = 1 (respectively,
σni+m+1 = −1) if m is even and σni+m+1 = −1 (respectively, σni+m+1 = 1) if m is odd; (iv) the map
σ is not constant (i.e., σi = 0 for all i ∈ [n]) as Lemma 3.2 would then imply k = 4, contradicting
that n ≥ 6. As ni=1 σi ri = 0 (this follows from the same methods implemented in Lemma 3.3),
                  P

there exists some a, b ∈ [k] such that σna = 1 and σnb = −1, and σ has at most 3 zeores (due to the
radii satisfying the weak generic condition). It now follows that the number of indices j ∈ [k] where
σnj = 0 must be non-zero and even; to see this, note that as we traverse the cycle (n1 , . . . , nk )
from n1 back to n1 , the map σ switches between 1 and −1 (ignoring any zeroes inbetween) an even
amount of times and only the +1/ − 1 switches generate odd-length strings of zeroes. Since σ can
have at most 3 zeroes, it follows that σ has exactly two zeroes contained in the cycle (n1 , . . . , nk ).
As σn1 = σns = 0 and xn1 ≤ xni for all i ∈ [k], we see that
                                         
                                         
                                         
                                         
                                         
                                          1      if i = nj for some 1 < j < s,
                                  σi =     −1 if i = nj for some s < j ≤ k,
                                         
                                         
                                         0
                                         
                                                 otherwise.

Hence for i ∈ [k] with i 6= 1 we have
                                                            Pi−1
                                  r
                                    ni + (xn1 + rn1 ) +       j=2 2rnj     if 1 < i ≤ s,
                         xn i =                              Pk
                                  r
                                       ni + (xn1 + rn1 ) +    j=i+1 2rnj   if s ≤ i ≤ k.

(Here we are using the convention that bj=a tj = 0 if a > b.) We observe that if a pair {ni , nj }
                                                P

with 1 ≤ i < j ≤ k is an edge of ([n], Ey ), then either j = i + 1 or i ≤ s ≤ j. Furthermore, the
vertex n1 is adjacent to a vertex ni in ([n], E) if and only if i ∈ {2, k}, and the vertex ns is adjacent
to a vertex nj in ([n], E) if and only if j ∈ {s − 1, s + 1}.

                                                        14
     Fix G′ = (V ′ , E ′ ) to be the subgraph of G induced by V ′ := {n1 , . . . , nk }, and define (V ′ , Ex′ ) and
(V ′ , Ey′ ) to be the corresponding induced coloured subgraphs of G′ . As (n1 , . . . , nk ) is a chordless
cycle of ([n], Ex ), the graph (V ′ , Ex′ ) is a connected cycle with k edges. Since any neighbours of
n1 and ns in (V ′ , Ey′ ) are also their neighbours in (V ′ , Ex′ ), the vertices n1 , ns are isolated vertices
in (V ′ , Ey′ \ Ex′ ), and hence any cycle in (V ′ , Ey′ \ Ex′ ) contains at most |V ′ | − 2 ≤ n − 2 vertices.
As shown prior, (V ′ , Ey′ ) does not contain any cycles of length at most n − 2. Hence the subgraph
(V ′ , Ey′ \ Ex′ ) is a forest with at least 3 connected components (and thus at most k − 3 edges) and
isolated vertices n1 , nk . It now follows that

                              |E ′ | = |Ex′ | + |Ey′ \ Ex′ | ≤ k + (k − 3) = 2k − 3.

Hence if k = n, then |E| = |E ′ | ≤ 2n − 3 and we are done.
    Now suppose instead that k = n−1. Further suppose that the vertex n is adjacent to more than
2 vertices in ([n], Ex ). Then the only possible structure that ([n], Ex ) can take without generating
a cycle of length 3 (contradicting Lemma 2.1), or generating a cycle of length more than 4 and less
than n − 1 is the following graph with n = 7 and vertex n as the centre vertex:


                                                         n




As each cycle of length 4 must generate a clique of size 4 in G, G must contain a copy of the graph
featured in Figure 4, contradicting Lemma 3.4. Hence we may suppose that n is adjacent to at
most two vertices in ([n], Ex ). Furthermore, if n is adjacent to vertices ni , nj ∈ V ′ in ([n], Ex ) with
i < j, then an analysis of the possible cycles in ([n], Ex ) show that n, ni , nj must be contained in a
cycle of 4. As n1 , ns are isolated vertices in the forest (V ′ , Ey′ \ Ex′ ), any cycle of ([n], Ey \ Ex ) has
length at most n − 2 and does not contain n1 , ns . Hence by Lemma 3.3, any cycle of ([n], Ey \ Ex )
has length 4 and is induced by 4 squares. However any cycle in ([n], Ey ) induced by 4 squares
sharing a corner will not be a cycle in ([n], Ey \ Ex ), since exactly two edges of the cycle must also
be contained in Ex . Hence ([n], Ey \ Ex ) is a forest.
    Without loss of generality, one of three possible cases must now hold:

  (i) n is adjacent to neither n1 nor ns in ([n], Ey \ Ex ),

 (ii) n is adjacent to n1 but not ns in ([n], Ey \ Ex ), or

 (iii) n is adjacent to both n1 and ns in ([n], Ey \ Ex ).

First suppose case (i) holds. Since n is adjacent to at most 2 vertices in ([n], Ex ) and ([n], Ey \ Ex )
is a forest with at least cy connected components, we see that

                |E| = |Ex | + |Ey \ Ex | ≤ (n − 1 + 2) + (n − cy ) = 2n − cy + 1 ≤ 2n − 2


                                                        15
and we are done.
    Now suppose case (ii) holds. By a similar counting method to that above, we observe that
either G has at most 2n − 2 edges, or ([n], Ey \ Ex ) has exactly 2 connected components (with ns
as an isolated vertex) and n is adjacent to exactly 2 vertices in ([n], Ex ). Suppose for contradiction
that the latter holds. Let (a, b, c, n) be the cycle of length 4 in ([n], Ex ) that contains n and its
two neighbours a, c. Since the squares Sa , Sb , Sc , Sn share a corner (Lemma 3.3) and the cycle is
ordered (a, b, c, n), we must have σb = 0. As n is not adjacent to ns and (a, b, c) is a path in the
cycle (n1 , . . . , nk ), we have a = n2 , b = n1 , c = nk and xn + rn = xn1 + rn1 . An analysis of the
x-coordinates of the various centres of P show that n is only adjacent to n1 , n2 , nk in G. Since
{n, n2 }, {n, nk } ∈ Ex , the forest ([n], Ey \ Ex ) has at least 3 connected components, contradicting
our earlier assumption.
    Finally, suppose case (iii) holds. As {n1 , n}, {ns , n} ∈ Ey \Ex , we have |xn1 − xn | < rn1 + rn and
|xns − xn | < rns + rn . Using our prior knowledge of the positions of the x-coordinates for vertices
in V ′ , it follows that for each i ∈ [k] \ {1, s} we have

        xn − rn − rni < xn − rn < xn1 + rn1 < xni < xns − rns < xn + rn < xn + rn + rni ,

and so |xn − xni | < rn + rni . Hence n has no neighbours in ([n], Ex ) and |Ex | = n − 1. As
([n], Ey \ Ex ) is a forest, we now see that

                         |E| = |Ex | + |Ey \ Ex | ≤ (n − 1) + (n − 1) = 2n − 2.

This completes the proof.


4    Proof of Theorem 1.1
Before we prove Theorem 1.1, we first require the following two technical lemmas.

Lemma 4.1. Suppose that for a given set of radii r1 , . . . , rn with n ≥ 2, there exists a homothetic
square packing with radii r1 , . . . , rn and k contacts. Then for any choice of rn+1 > 0, there exists
a homothetic square packing with radii r1 , . . . , rn+1 and at least k + 2 contacts.

Proof. Let P = {S1 , . . . , Sn } be a homothetic square packing with contact graph G = ([n], E), radii
r1 , . . . , rn and centres p1 , . . . , pn , where |E| = k. We may assume that G is connected; indeed if
it was not, we could translate one connected component of P until it was in contact with another
and increase the amount of contacts by at least 1. Define the closed set
                              n                                                o
                        X := z ∈ R2 : (rn+1 S ◦ + z) ∩ Si = ∅ for all i ∈ [n] .

Note that for any point z ∈ X, the interior of the set rn+1 S + z will not intersect ni=1 Si , and
                                                                                             S

the set rn+1 S + z will intersect ni=1 Si if and only if z ∈ ∂X. Hence for any z ∈ ∂X, the set
                                         S

{S1 , . . . , Sn , rn+1 S + z} will be a homothetic square packing with at least k + 1 contacts. It follows
that we now need only find a point z ∈ ∂X such that rn+1 S + z is in contact with at least two
squares in P .

                                                    16
    Choose any point z ′ ∈ ∂X. If the square rn+1 S + z ′ is in contact with two or more squares in
P then we are done. Suppose that rn+1 S + z ′ is in contact with exactly one square Si . Given ∂S
is the boundary of the standard square, z ′ is an element of the set C := (ri + rn+1 )∂S + pi . It is
immediate that C ∩ X ◦ = ∅. As the sets C and ∂X are closed, the set C ∩ ∂X is a non-empty closed
subset of C. The boundary of C ∩ ∂X with respect to the ambient space C exists as C 6⊂ ∂X;
indeed if C ⊂ ∂X, then Si would not be in contact with any other square in P , contradicting that
G is connected and n ≥ 2. Choose a point z ∈ C. If z is not contained in C \ ∂X then, since
C ∩ X ◦ = ∅, z ∈/ X and so the set rn+1 S + z will be in contact with Si and intersect the interior of
another square Sj 6= Si . If z is in the interior of C ∩ ∂X with respect to the ambient space C, then
rn+1 S + z is in contact with Si and but it will not intersect any other square in P . Hence if we
choose a point z in the boundary of C ∩ ∂X with respect to the ambient space C, then rn+1 S + z
will be in contact with at least two squares in P .

Lemma 4.2. Let P be a homothetic square packing with contact graph G = ([n], E), radii r1 , . . . , rn
and centres p1 , . . . , pn . Suppose that for some 1 ≤ s ≤ n − 1, the following holds:
        Ps             Pn
  (i)       i=1 ri =       i=s+1 ri ,

 (ii) p1 = (r1 , r1 ) and ps+1 = (rs+1 , −rs+1 ), and
                       Pi−1                                                    Pn
(iii) pi = (ri +           j=1 2rj , ri ) for all 2 ≤ i ≤ s and pi = (ri +      j=s+1 2rj , −ri ) for all s + 2 ≤ i ≤ n.

Then the graph ([n], Ey ) is connected. (See Figure 5 for an example of such a packing.)

Proof. Fix pi = (xi , yi ) for each i ∈ [n]. Define for each i ∈ [n] the closed interval

                                                 Ii := [xi − ri , xi + ri ].

Since si=1 Ii = ni=s+1 Ii , we observe that every interval Ii for i ≤ s must intersect at least one set
        S              S

Ij for j ≥ s + 1. Choose any i ∈ [s − 1] and let j ∈ [n] be the largest index such that Ii ∩ Ij 6= ∅;
by our previous observation we note that j ≥ s + 1. Suppose that xi + ri ≥ xj + rj . If j = n, then
i = s, contradicting that i ∈ [s − 1]. If j < n then Ii ∩ Ij+1 6= ∅ as xi + ri ≥ xj + rj = xj+1 − rj+1 ,
contradicting the maximality of j. Hence xi +ri < xj +rj . Since xi+1 −ri+1 = xi +ri , it follows that
Ij ∩ Ii+1 6= ∅. From this we can deduce that for each i ∈ [n] where i ≤ s − 1, there exists j ∈ [n] such
that j ≥ s + 1 and {i, j}, {i + 1, j} ∈ Ey . By a similar technique we can show that for each j ∈ [n]
where s + 1 ≤ j ≤ n − 1, there exists i ∈ [n] where i ≤ s such that {i, j}, {i, j + 1} ∈ Ey . With
this we can construct two paths P1 , P2 ∈ ([n], Ey ) such that P1 contains every vertex 1 ≤ i ≤ s and
at least one vertex j ≥ s + 1, and P2 contains every vertex s + 1 ≤ j ≤ n and at least one vertex
i ≤ s. Hence the graph ([n], Ey ) is connected.

    With this we are finally ready to prove Theorem 1.1.

Proof of Theorem 1.1. Suppose that (ii) holds, i.e., the radii satisfy the weak generic condition.
Let P be a homothetic square packing with contact graph G = ([n], E), radii r1 , . . . , rn and centres
p1 , . . . , pn . If either ([n], Ex ) or ([n], Ey ) contains a cycle with at least n−1 vertices, then |E| ≤ 2n−2


                                                             17
Figure 5: An example of the construction from Lemma 4.2. The radii of the squares on the top
row from left to right are r1 = 1, r2 = 1.5, r3 = 2.5, r4 = 2 and r5 = 3, and the radii of the squares
on the bottom row from left to right are r6 = 2, r7 = 3, r8 = 5. As can be seen, the graph ([n], Ey )
for this homothetic square packing is connected.


by Lemma 3.5. Suppose that any cycle in either ([n], Ex ) or ([n], Ey ) has length at most n − 2. By
Lemmas 2.1 and 3.3, every cycle in ([n], Ex ) (respectively, ([n], Ey )) has length 4 and is generated
by 4 squares sharing a corner. Let C1x , . . . , Ckx ⊂ Ex and C1y , . . . , Cky ⊂ Ey be the cycles of ([n], Ex )
and ([n], Ey ) labelled so that for each 1 ≤ i ≤ k we have Cix ∩ Ciy = {ei , fi } for some edges ei , fi ;
this corresponds to the cycles Cix and Ciy being generated by the same 4 squares sharing a corner.
Define Ex′ := Ex \ {e1 , . . . , ek } and Ey′ := Ey \ {f1 , . . . , fk }. It is immediate that E = Ex′ ∪ Ey′ and
both ([n], Ex′ ) and ([n], Ey′ ) are trees, and so

                             |E| ≤ |Ex′ | + |Ey′ | ≤ (n − 1) + (n − 1) = 2n − 2.

Hence (i) holds.
    Now suppose (ii) does not hold; i.e., there exists a map σ : [n] → {−1, 0, 1} with ni=1 σi ri = 0
                                                                                               P

and σn0 6= 0, σn1 = . . . = σn4 = 0 for distinct vertices n0 , . . . , n4 ∈ [n]. By reordering the indices
we may assume that σ1 , . . . , σs = 1, σs+1 , . . . , σn−t = −1 and σn−t+1 , . . . , σn = 0 for some s ≥ 1
and t ≥ 4. With this reordering we have si=1 ri = i=s+1
                                                             Pn−t
                                                                    ri . By Lemma 4.1, it is sufficient to
                                               P

consider the case where t = 4; if there exists homothetic square packing with at least 2(n − t + 4)− 1
contacts using only the first n − t + 4 radii, then there exists a homothetic square packing with at
least 2n − 1 contacts using all the radii.




                                                      18
    For each 1 ≤ i ≤ n, set pi = (xi , yi ), where
                                
                                
                                
                                
                                
                                  r1                       if i = 1,
                                  ri + i−1
                                
                                         j=1 2rj           if 2 ≤ i ≤ s,
                                
                                      P
                                
                                
                                
                                
                                r
                                
                                                           if i = s + 1,
                                   s+1
                          xi :=        Pi−1
                                
                                
                                
                                
                                  ri + j=s+1   2rj         if s + 2 ≤ i ≤ n − 4,
                                
                                  −ri                      if i = n − 3 or i = n − 2,
                                
                                
                                
                                
                                
                                r + Ps 2r
                                
                                                           if i = n − 1 or i = n,
                                
                                        i      j=1   j

                               
                               r
                                i           if 1 ≤ i ≤ s or i = n − 3 or i = n − 1,
                       yi :=
                               −r          if s + 1 ≤ i ≤ n − 4 or i = n − 2 or i = n.
                                    i

The family P = {ri S +pi : i ∈ [n]} now defines a homothetic square packing with contact graph G =
([n], E); see Figure 6 for an example of the construction. First note that Ex \ Ey contains the paths
(n−3, 1, . . . , s, n−1) and (n−2, s+1, . . . , n−4, n), hence |Ex \Ey | ≥ n−2. By Lemma 4.2, the graph
([n], Ey ) restricted to the vertices 1, . . . , n−4 is connected, and hence has at least n−5 edges. There
are also 6 extra edges in ([n], Ey ); {1, n−2}, {s+1, n−3}, {s, n}, {n−4, n−1}, {n−2, n−3}, {n−1, n}.
Hence |Ey | = n − 5 + 6 = n + 1. It now follows that |E| ≥ 2n − 1, and so (i) does not hold.




Figure 6: An example of the construction from Theorem 1.1 with 17 > 2 · 9 − 2 contacts. The
construction is possible because the sum of the radii for the middle three squares on the top row
(from left to right; 1, 1.5, 2.5) is equal to the sum of the radii for the middle two squares on the
bottom row (from left to right; 2, 3), and the radii sum equality does not use the radii of at least
four squares. The four squares that are not involved in the summation are then placed on the left
and right to form the two cliques of size 4.



5    Square packings allowing rotations and face-to-face contacts
Throughout the paper we have only been interested in homothetic square packings. In this section
we will relax the condition that each square is a homothetic copy of S. A similar copy of S

                                                         19
is a set rRθ S + p, where r > 0, p ∈ R2 , θ ∈ [0, π/2) and Rθ is the 2 × 2 matrix representing
anticlockwise rotation of the plane by θ radians. With this, we define a packing of n squares,
or square packing for short, to be a set P = {S1 , . . . , Sn } of similar copies of S with pairwise
disjoint interiors. The centres, radii and angles of a square packing P = {S1 , . . . , Sn } with
Si = ri Rθi S + pi for each i ∈ [n] will be the vectors p1 , . . . , pn , positive scalars r1 , . . . , rn and the
angles θ1 , . . . , θn respectively.
    Interestingly, the amount of contacts of a packing of n squares is not bounded by 2n − 2 even
when the radii do not satisfy any polynomial equation with rational coefficients.

Proposition 5.1. For each n ≥ 5, there exists a packing of n squares with algebraically independent
radii and more than 2n − 2 contacts.

Proof. Fix P = {S1 , . . . , Sn } to be the square packing with radii r, centres p and angles θ defined
as follows:
                                      √
  (i) r1 := 1/3, r3 := 2/3, rn := 2 2/3 and ri := 1 otherwise.

 (ii) θn := π/4 and θi := 0 otherwise.

 (iii) p1 := (−1/3, 1/3), p2 := (−1, −1), p3 := (2/3, −2/3), p4 := (1, 1), for each 5 ≤ i ≤ n − 1 we
       have
                                              
                                              (i − 4 + 4/3, −1)     if i is odd,
                                      pi :=
                                              (i − 3, 1)            if i is even,

      and pn = (−4/3, 4/3).

See Figure 7 (left) for the described square packing P with n = 7. We note that P has 2n − 1
contacts. Furthermore, for small perturbations of the vector r where r1 is decreased, we can always
form a square packing similar to that indicated in Figure 7 (right), which will also always have
2n − 1 contacts. Hence there exists a packing of n squares with algebraically independent radii and
2n − 1 contacts.

    Because of Proposition 5.1, we shall restrict which type of contacts we are interested in. Let
P = {S1 , . . . , Sn } be a square packing with Si = ri Rθi S + pi for each i ∈ [n]. We say that the
distinct squares Si and Sj have a face-to-face contact if the set Si ∩ Sj is a line segment [z, z ′ ]
with z 6= z ′ . It is important to note that if the vertex pair {i, j} describe a face-to-face contact,
then θi = θj . Another useful observation is the following: if P is a homothetic square packing
with contact graph G = ([n], E), then the face-to-face contacts of P are exactly the edges in the
symmetric difference of Ex and Ey .

Corollary 5.2. Let r1 , . . . , rn be positive scalars that satisfy the weak generic condition. Then every
packing of n squares with radii r1 , . . . , rn has at most 2n − 2 face-to-face contacts. Furthermore, if
a given square packing has 2n − 2 face-to-face contacts, then it is a homothetic square packing with
no four squares sharing a corner.


                                                       20
Figure 7: (Left): The square packing with 2n − 1 contacts described in Proposition 5.1 for n = 7.
(Right): A square packing with 2n − 1 contacts which can be formed from the square packing on
the left by perturbing the values of the radii. All the squares except the top left square maintain
their original orientation, while the top left square simply needs to rotate slightly to maintain the
necessary 2n − 1 contacts.


Proof. Let P be a square packing with radii r1 , . . . , rn , centres p1 , . . . , pn and angles θ1 , . . . , θn .
Define the equivalence relation ∼ on [n] by setting i ∼ j if and only if θi = θj , and set ñ1 , . . . , ñm to
be the equivalence classes of [n]. Each square packing P (ñi ) := {Sj : j ∼ ni } is homothetic, hence
each has at most 2|ñi | − 2 contacts by Theorem 1.1. Since there can be no face-to-face contacts
between P (ñi ) and P (ñj ) when i 6∼ j, we have that P has at most mi=1 (2|ñi |−2) = 2n−2m ≤ 2n−2
                                                                     P

face-to-face contacts.
    Suppose that P has 2n − 2 face-to-face contacts. Then m = 1 and P is a homothetic square
packing with |Ex △Ey | = 2n − 2. As E ⊃ Ex △Ey and |E| ≤ 2n − 2 (Theorem 1.1), we have
E = Ex △Ey , i.e., Ex and Ey are disjoint sets. Hence P has no four squares sharing a corner, as
this would imply the intersection Ex ∩ Ey is non-empty.


6      Failure of the natural analogue of Theorem 1.1 for homothetic
       cube packings
For this section we fix the standard cube to be the set C := {(x, y, z) : −1 ≤ x, y, z ≤ 1}. We can
analogously define the concept of a homothetic cube packing to be a set P = {C1 , . . . , Cn } of
homothetic copies of C with pairwise disjoint interior. Similarly we define the centres p1 , . . . , pn ∈
R3 and radii r1 , . . . , rn > 0 to be the values such that Ci = ri C + pi for each i ∈ [n], and define the
contact graph G = ([n], E) by setting {i, j} ∈ E if and only if i 6= j and Ci ∩ Ci 6= ∅. Given two
cubes Ci and Cj in contact with centres pi = (xi , yi , zi ), pj = (xj , yj , zj ) and radii ri , rj respectively,
at least one of the following three possibilities hold:

    (i) ri +rj = |xi −xj | ≥ max{|yi −yj |, |zi −zj |}, in which case we say Ci and Cj have a x-direction
        contact,


                                                       21
 (ii) ri +rj = |yi −yj | ≥ max{|xi −xj |, |zi −zj |}, in which case we say Ci and Cj have a y-direction
      contact,

(iii) ri +rj = |zi −zj | ≥ max{|xi −xj |, |yi −yj |}, in which case we say Ci and Cj have a z-direction
      contact.

An obvious question now is: can we extend our results for homothetic square packings to homothetic
cube packings? Before begin looking into this question in more detail, we need to understand what
the analogous amount of contacts should be. If each subgraph of the contact G = ([n], E) of P
formed by either the x-, y- or z-direction contact edges has no cycles, then G can have at most
3n − 3 edges. Hence we would (naively) expect that randomly chosen radii will force the number of
contacts to be bounded by 3n − 3. However it is easy to see that this bound must fail for sufficiently
large n.

Proposition 6.1. Let n ≥ 7 and choose any n positive scalars r1 , . . . , rn . Then there exists a
homothetic packing of n cubes with radii r1 , . . . , rn and more than 3n − 3 contacts.

Proof. Let n = 8k + ℓ for some ℓ ∈ {0, . . . , 7}, and choose any set of positive scalars r1 , . . . , rn .
Choose some R > 0 such that 4ri < R for each i ∈ [n]. For each i ∈ [n], define the unique
non-negative integers ai , bi that are the quotient and remainder of i divided by 8 respectively, i.e.,
i = 8ai + bi . With this we define
                                        
                                        
                                        
                                        
                                        
                                          (ri + ai R, ri , ri )              if bi = 0
                                        
                                          (ri + ai R, ri , −ri )             if bi = 1
                                        
                                        
                                        
                                        
                                        
                                        
                                          (ri + ai R, −ri , ri )             if bi = 2
                                        
                                        
                                        
                                        
                                        
                                        
                                        (r + a R, −r , −r )
                                        
                                                                             if bi = 3
                                            i       i        i       i
                                pi :=
                                        
                                        
                                        
                                        
                                          (−ri + ai R, ri , ri )             if bi = 4
                                        
                                          (−ri + ai R, ri , −ri )            if bi = 5
                                        
                                        
                                        
                                        
                                        
                                        
                                          (−ri + ai R, −ri , ri )            if bi = 6
                                        
                                        
                                        
                                        
                                        
                                        
                                        (−r + a R, −r , −r )
                                        
                                                                             if bi = 7.
                                                i       i        i       i

Let P = {C1 , . . . , Cn } be the homothetic cube packing where Ci = ri C + pi for each i ∈ [n]. Two
distinct cubes Ci , Cj are in contact if and only if ai = aj , hence
                                    !               !
                                   8    ℓ            n + ℓ(ℓ − 8) + 6
                           |E| =     k+   = 3n − 3 +                  .                               (11)
                                   2    2                    2

If n ≥ 11 then |E| > 3n − 3 since ℓ(ℓ − 8) + 6 ≥ −10. For small values of n we can substitute the
corresponding remainder ℓ into eq. (11): if n = 7 then ℓ = 7 and |E| = 3n; if n = 8 then ℓ = 0 and
|E| = 3n + 4; if n = 9 then ℓ = 1 and |E| = 3n + 1; if n = 10 then ℓ = 2 and |E| = 3n − 1. Hence
P has more than 3n − 3 contacts when n ≥ 7.

    As the complete graph with n ≤ 6 vertices has at most 3n − 3 edges, Proposition 6.1 cannot
be improved. However, the homothetic packing of n cubes described in Proposition 6.1 will always

                                                            22
have less than 12(n/8) < 3n − 3 face-to-face contacts (i.e., a contact where the intersection is a
2-dimensional convex set). This leads one to wonder: is the natural analogue to Theorem 1.1 true
if we restrict to face-to-face contacts? Unfortunately, this too can fail for very general choices of
radii.

Proposition 6.2. Let n ≥ 4 and r1 ≥ . . . ≥ rn > 0. If r4 + . . . + rn < r3 , then there exists a
homothetic packing of n cubes with radii r1 , . . . , rn and at least 4n − 11 face-to-face contacts (and
hence more than 3n − 3 face-to-face contacts when n ≥ 9).

Proof. We begin by defining the homothetic cube packing P = {C1 , . . . , Cn } with radii r1 , . . . , rn
and centres p1 , . . . , pn . Fix

                  p1 = (−r1 , 0, −r1 ),    p2 = (r2 , 0, −r2 ),    p3 = (r3 + rn , 0, r3 ).

Define s4 = r4 − r3 and si = ri + i−1 k=4 2rk − r3 for i > 4. We now fix pi = (−ri + rn , si , ri ) for all
                                     P

i ≥ 4. With this we fix Ci = ri C + pi for each i ∈ [n].
    Let E be the set of pairs {i, j} where the cubes Ci and Cj have a face-to-face contact. Then
                                                                   
       E = {1, 2}, {2, 3} ∪ {i, j} : i ∈ {1, 2, 3}, 4 ≤ j ≤ n ∪ {i, i + 1} : 4 ≤ i ≤ n − 1 ,

and hence P has 2 + 3(n − 3) + n − 4 = 4n − 11 face-to-face contacts.

Acknowledgement
The author was supported by the Heilbronn Institute for Mathematical Research and the Austrian
Science Fund (FWF): P31888.


References
[1] R. Connelly, S. Gortler, L. Theran, Rigidity of sticky disks, Proceedings of the Royal Society A
    475:2222 (2019). https://doi.org/10.1098/rspa.2018.0773

[2] L. Danzer, B. Grünbaum, V. Klee, Helly’s theorem and its relatives, In: Proceedings of
    Symposia in Pure Mathematics 7, American Mathematical Society (1963) pp. 101–180.
    https://doi.org/10.1090/pspum/007

[3] S. Dewar, Homothetic packings of centrally symmetric convex bodies, Geometriae Dedicata
    216:11 (2022). https://doi.org/10.1007/s10711-022-00675-w

[4] D. Kitson, S.C. Power, Infinitesimal rigidity for non-Euclidean bar-joint frameworks, Bulletin of
    the London Mathematical Society 46 (2014) pp. 685–697. https://doi.org/10.1112/blms/bdu017

[5] O. Schramm, Square tilings with prescribed combinatorics, Israel Journal of Mathematics 84
    (1993) pp. 97–118. https://doi.org/10.1007/BF02761693



                                                    23
