                                                Dense periodic packings of tetrahedra with
arXiv:0910.5226v5 [math.MG] 19 Mar 2010




                                                          small repeating units
                                                               Yoav Kallus∗, Veit Elser∗, Simon Gravel†

                                                                                    Abstract
                                                     We present a one-parameter family of periodic packings of regular
                                                 tetrahedra, with the packing fraction 100/117 ≈ 0.8547, that are simple
                                                 in the sense that they are transitive and their repeating units involve only
                                                 four tetrahedra. The construction of the packings was inspired from re-
                                                 sults of a numerical search that yielded a similar packing. We present an
                                                 analytic construction of the packings and a description of their proper-
                                                 ties. We also present a transitive packing √
                                                                                                with a repeating unit of two
                                                 tetrahedra and a packing fraction 139+40369
                                                                                              10
                                                                                                 ≈ 0.7194.


                                          1      Introduction
                                          The optimization problem of packing regular tetrahedra densely in space has
                                          seen invigorated interest over the last few years [3, 4, 5, 6, 7]. This interest has
                                          helped drive up the packing fraction of the densest-known such packings from
                                          0.7174 in 2006 [3] to 0.8503 [7] most recently (see Table 3). These improved
                                          packing fractions have been obtained from more and more complex packings,
                                          with larger and larger repeating units. This trend has led some to conjecture
                                          that the densest packing of tetrahedra might have inherent disorder [6]. The
                                          more restrictive problem of packing tetrahedra transitively — that is, so that
                                          all tetrahedra in the packing are equivalent (a more rigorous definition is given
                                          below) — has been less extensively studied and the densest previously-reported
                                          transitive packing of regular tetrahedra fills only 2/3 of space [3]. Here we
                                          present a one-parameter family of transitive but dense packings of tetrahedra
                                          with the packing fraction 100/117 ≈ 0.8547.
                                              The discovery of this family of dense packings was inspired by the results
                                          of a numerical search, which yielded a dense packing with similar structural
                                          properties to the packing we present. The numerical method used was adapted
                                          from the divide and concur approach to constraint satisfaction problems [2]. The
                                          divide and concur formalism enables us to set up an efficient search through the
                                          parameter space consisting of the positions and orientations of tetrahedra inside
                                          the repeating unit and the translation vectors governing its lattice repetition,
                                              ∗ Laboratory of Atomic and Solid-State Physics, Cornell University, Ithaca, New York 14853
                                             † Department of Genetics, Stanford University School of Medicine, Stanford, California

                                          94305-5120


                                                                                        1
 fundamental                    T0 = conv{ri | i = 1, 2, 3, 4}
 tetrahedron                    r1 = 27       7      10
                                     28 a − 30 b + 39 c
                                     1       9
                                r2 = 4 a − 10 b
                                      1       1       5
                                r3 = 14 a + 10  b + 13  c
                                     3       1      5
                                r4 = 7 a + 10 b − 13 c
 other tetrahedra               T1 = R2 (T0 ) = conv{ 32 (r2 + r3 + r4 ) − r1 , r2 , r3 , r4 }
 in the unit cell               T2 = I(T0 ) = −T0
                                T3 = I(T1 ) = −T1
 space group                    translations by a, b, dx = 21 b + 12 c + xa
 generators                     I = inversion about 0
                                R2 = two-fold rotation about { 14 a + tb | t ∈ R}
 packing fraction               100/117√
 coordinate basis for which     a = (2 √ 7/5, 0, 0)
 tetrahedra are regular         b = (0, 3/2, p0)
 with unit edge length          c = (0, 0, 13 3/14/5)

Table 1: The construction of the dimer-double-lattice family of packings in
terms of the parameter 29/56 ≤ x ≤ 9/14 in a general monoclinic coordinate
basis (a · b = b · c = 0). The packing is generated starting from the fundamental
tetrahedron by the action of the space group. A packing of regular tetrahedra is
obtained when the general monoclinic coordinate basis reduces to the specified
orthogonal coordinate basis.


subject to the constraint that no two tetrahedra overlap. The dynamics involved
in the divide and concur search are highly non-physical, which might explain
why our method was able to discover this dense packing, while earlier methods
involving more physical dynamics were not [5, 6, 7]. In this note we present only
the analytically constructed packing without a full explication of the numerical
method, which will be forthcoming.


2    One-parameter family of dimer-double-lattice
     packings
The first set of packings we report on are naturally described as double lattices of
bipyramidal dimers. A double lattice is the union of two Bravais lattices related
to each other by an inversion operation about some point. In [1], Kuperberg and
Kuperberg used the idea of a double lattice in the Euclidean plane to show that
any planar convex √ body can be packed in an arrangement with a packing fraction
no smaller than 3/2. We naturally extend the idea of the double lattice to the
three-dimensional Euclidean space. The repeating unit of one constituent lattice
is a bipyramidal dimer: two regular tetrahedra sharing a common face. Two
of these dimers with mutually-inverted orientation — a Kuper-pair — form the
repeating unit of the double lattice, which thus has four tetrahedra of distinct
orientations. We state the existence of the packings as Theorem 1.


                                          2
Theorem 1. There exists a one-parameter family of packings of regular tetra-
hedra, each having packing fraction 110/117. These packings are periodic, with
each unit cell of the lattice containing two bipyramidal dimers. The group of
isometries leaving each packing invariant is a crystallographic space group of
type C2/c (following the classification and notation of [11]) and acts transi-
tively on the individual tetrahedra of the packing.
Proof. We construct each packing by acting on a single regular tetrahedron with
a group of isometries. For a coordinate     √ basis we use
                                                         √ three pair-wise orthogonal
                                                                            p
vectors a, b, and c, of norms |a| = 2 7/5, |b| = 3/2, and |c| = 13 3/14/5.
The initial tetrahedron T0 = conv{ri | i = 1, 2, 3, 4} is the convex hull of four
vertices whose coordinates are given in Table 1; it is a regular tetrahedron of unit
edge length. The group of isometries is the group of crystallographic type C2/c
generated by the translations a, b, and dx = 21 b + 12 c + xa (29/56 ≤ x ≤ 9/14),
by the inversion about the point 0, and by the rotation by 180 degrees about the
axis { 41 a + tb | t ∈ R} [11]. This space group has a point group of order 4 and
its translations generate a centered monoclinic point lattice. The construction
is summarized in Table 1.
    By construction, each tetrahedron in the packing is the image of T0 under
an isometry in the group. We have immediately then that all tetrahedra are
congruent with T0 , that the packing is invariant under the action of the group,
and that the group acts transitively on individual tetrahedra. As the tetrahedra
divide into four orbits of the lattice translations, the packing fraction is given
by                                                  √
                               4 vol(T0 )        4( 2/12)      100
                      φ=                       =             =
                           | det([a, b, dx ])|   |a||b||c|/2   117
    All that is left then to prove the theorem is to verify that the arrangement
of tetrahedra thus constructed is indeed a packing. As the packing is transi-
tive (in the sense that its symmetry group acts transitively on the constituent
tetrahedra), it is enough to check that one tetrahedron, T0 , does not overlap
any other tetrahedron. By means of a closest-lattice-point algorithm such as
the one in [10], we generate a list of all tetrahedra
                                            p          whose centroid is, for any
29/56 ≤ x ≤ 9/14, at a distance less than 3/2 from the centroid of T0 . There
are 46 such tetrahedra. All other tetrahedra have circumspheres which do not
intersect the circumsphere of T0 , and therefore they do not intersect T0 . For
each tetrahedron in the list we can establish the existence of a separating plane
separating it from T0 . Two tetrahedra have no overlap if and only if they are
separated by a plane, and moreover, such a plane always exists which passes
through three of the eight vertices of the two tetrahedra. By exhaustively veri-
fying that one of the finitely many planes that pass through three of the vertices
separates the two tetrahedra, we establish that each tetrahedron in the list can
be separated from T0 .
    Note that the above construction, which uses a specific orthogonal coordinate
basis {a, b, c}, is a special case of a general family of packings of non-regular
tetrahedra that can be obtained using the same construction, but with a general


                                         3
Figure 1: Small portions of one layer and three stacked layers in the dimer-
double-lattice packing given by x = 4/7.


monoclinic coordinate basis (a · b = b · c = 0). Each of these more general
packings is an image of a packing in the original family under an affine map
from a three-parameter family (not counting pure dilation). As the lack of
overlap between tetrahedra and the packing fraction are both affine-invariant,
these are also transitive packings of the same packing fraction.
    By the construction of the double lattice, there is an inversion center that
sends one lattice of dimers into the other. Note that a lattice translation com-
posed with an inversion about a point corresponds to an inversion about a point
related to the original inversion center by half the lattice vector. It follows then
that in any primitive unit cell of the lattice, there are eight such inversion
centers. These eight inversion centers form the vertices of a parallelepiped one-
eighth the volume of the primitive unit cell of the lattice. This parallelepiped
is the equivalent of the “extensive parallelogram” described in [1] whose vertices
are the inversion points that generate the double lattice. As in [1], the paral-
lelepiped is inscribed in the body being packed — the bipyramidal dimer in our
case.
    An interesting feature of the packing is the presence of the free parameter
x. The effect of a change in x is to slide fixed layers of the packing relative
one another along the a-direction. These layers are the layer generated by the
translations a and b from the four tetrahedra of the primitive unit cell and the
layers parallel to it. The construction yields a valid packing when the small
protrusions in one layer are staggered to fit into small gaps in the neighboring
layer, which is the case for all 29/56 ≤ x ≤ 9/14 (mod 1). Within this range,
each layer can slide against the neighboring layer without changing the spacing
between the two or creating collisions. It is possible then to obtain equally dense,
non-transitive packings by staggering consecutive layers arbitrarily within the
allowed range.
    We describe next the contacts formed by each dimer in the packing, and they
are illustrated in Figures 1 and 2. Each of the eight vertices of the inscribed par-


                                         4
                                                                            

                                                               


                                                           


                                                       

                                                                            
Figure 2: The contacts on the surface of a dimer shown on a net diagram for
x = 29/56 (left) and x = 9/14 (right): the face-face contacts (gray), whose
centers (black dots) lie on inversion centers, four of which are fixed and four
of which move as a function of x; the four point contacts made regardless of
the value of x (blue squares), all lying on two-fold axes; the four point contacts
formed only for x = 29/56 (purple dots); and the four point contacts formed
only for x = 9/14 (green dots).


allelepiped corresponds to the center of a face-face contact between bipyramids
of opposite orientations, accounting for all contacts between oppositely-oriented
bipyramids. Four of these contacts are within one layer and four of them are
with the layers above and below. The contacts formed between like-oriented
bipyramids vary with the parameter x: for all values of x there are two edge-
edge contacts, a vertex-edge contact and an edge-vertex contact (all of these
contacts occur on two-fold axes and are within one layer); for x = 29/56 there
are four additional edge-edge contacts with dimers in neighboring layers (which
turn into overlaps for x < 29/56); and for x = 9/14 there are instead two
vertex-face contacts and two face-vertex contacts with dimers in neighboring
layers (which again turn into overlaps for x > 9/14). Thus, each dimer makes
respectively twelve, sixteen, or sixteen contacts in the three cases, and corre-
spondingly, each tetrahedron makes eight, ten, or eleven contacts.


3    Simple double-lattice packing
Our numerical search also yielded a packing with two tetrahedra per repeating
unit, which we could identify as a simple double lattice (that√ is a double lattice
of tetrahedra, not of dimers) with packing fraction 139+40 369
                                                               10
                                                                    ≈ 0.7194. We
present therefore a second theorem.
Theorem
      √
           2. There exists a packing of regular tetrahedra having packing fraction
139+40 10
   369    . This packing is periodic, with each unit cell of the lattice contain-


                                        5
 fundamental              T0 = conv{ri | i√= 1, 2, 3, 4}    √
 tetrahedron              r1 = [(433 − 86√ 10)a + (611 − 133 10)b+
                               (188 − 22 √10)c]/246       √
                          r2 = [(111 − 30√ 10)a + (93 − 75 10)b+
                              (−66 − 42 √  10)c]/246       √
                          r3 = [(−85 −√28 10)a + (13 − 29 10)b+
                               (4 + 10 10)c]/246
                                           √                 √
                          r4 = [(179 − 106√ 10)a + (427 − 101 10)b+
                               (−20 − 50 10)c]/246
 other tetrahedron        T1 = I(T0 ) = −T0
 in the unit cell
 space group              translations by a, b, c
 generators               I = inversion
                                    √ about 0
 packing fraction         (139 + 40 10)/369√
 coordinate basis for     a = (1, −(13√− 4 10)/3,√0)
 which tetrahedra are     b = (−(4√ − 10)/3, 3√− 10, −1)
 regular with unit edge   c = (3 − 10, 1, (4 − 10)/3)

Table 2: The construction of the simple-double-lattice packing in a general
triclinic coordinate basis.




Figure 3: Small portions of one layer and three stacked layers in the simple-
double-lattice packing.




                                     6
 Name                              φ                       N      Z̄         Transitive
 Optimal lattice[8]                18/49 ≈ 0.3673          1      14         Yes
 Warp and weft[3]                  2/3 ≈ 0.6666            2      10         Yes
 Welsh[3]                          17/24 √ ≈ 0.7083        34     25.9       No
                                   139+40 10
 Simple double lattice                 369     ≈ 0.7194    2      19         Yes
 Wagon wheels[4]                   0.7786                  18     7.1        No
 Compressed wagon wheels[5]        0.7820                  72     7.6        No
 Disordered wagon wheels[6]        0.8226                  314    7.4        No
 Quasicrystal approximant[7]       0.8503                  656               No
 Dimer double lattice              100/117 ≈ 0.8547        4      8 to 11    Yes

Table 3: Some studied transitive and non-transitive packings of regular tetra-
hedra with packing fraction φ, number of tetrahedra in the repeating unit N ,
and average number of contacts per tetrahedron Z̄ where available.


ing two tetrahedra. The group of isometries leaving the packing invariant is a
crystallographic space group of type P 1̄ and acts transitively on the individual
tetrahedra of the packing.
    The proof of this theorem proceeds equivalently to the proof of Theorem
1. The vertices of the initial tetrahedron T0 are given in Table 2 in terms
of a triclinic coordinate basis which is also given in Table 2. The group of
isometries we use to construct the packing is generated by translation by the
three vectors a, b, and c and by inversion about the origin. This is a space
group of crystallographic type P 1̄, with a point group of order 2 and a triclinic
lattice [11]. Figure 3 shows a portion of the packing.
    The simple-double-lattice packing again has eight inversion centers per prim-
itive cell at the vertices of a parallelepiped. However, in this case only five of the
vertices are on the surface of the tetrahedron. Each tetrahedron in the packing
is in contact with nineteen others.


4    Discussion
In Table 3, we compare the packings presented here to other studied packings
of regular tetrahedra. Both packings are denser than the densest previously-
reported transitive packing, a double lattice presented by Conway and Torquato
(which we call the "warp-and-weft" packing due to the interweaving arrange-
ment of its tetrahedra) [3], and the dimer double lattice is denser than any
previously-reported packing.
    The results presented go against the recent trend of ever-growing repeating
units in densest-known packings and demonstrate that a large repeating unit is
not a necessary property of a dense packing of regular tetrahedra. It is curious
that previous simulations, utilizing a more physical search dynamic [5, 6, 7],
yielded dense packings that were either disordered, had quasicrytalline order, or
had crystalline order characterized by a very large repeating unit, and were not


                                          7
able to find the denser class of structures presented here, (reminiscent perhaps
of Kurt Vonnegut’s ice-nine, a fictional phase of water that is more stable, but
kinetically unreachable).
    Our results yield the surprising situation wherein the densest-known packing
of icosahedra is now sparser than the corresponding packing of tetrahedra, a
solid which just four years ago was a prime candidate for a counterexample
of a conjecture by Ulam that the sphere is the sparsest-packing convex solid
[3]. As the packing can be generally extended to any tetrahedron in a three-
parameter family generated by deformations of the monoclinic coordinate basis,
if any tetrahedron provides a counterexample of Ulam’s conjecture, it is not a
tetrahedron of that family.
    The regular tetrahedron is no longer outcast, as it long was, from the re-
spectable family of convex polyhedra whose largest-achieved packing density is
realized by a transitive arrangement. While there are some convex solids whose
maximum packing density clearly cannot be achieved by a transitive arrange-
ment (the convex Schmitt-Conway-Danzer polyhedron can tile space, but only
in aperiodic and non-transitive ways [9]), the majority of regular and semi-
regular polyhedra have been to-date packed most densely in transitive packings
[5]. Whether this situation is accidental, the result of bias favoring the discovery
of transitive packings, or a more fundamental property governing the packing
of a certain class of solids is still an open question.
    This work was supported by grant NSF-DMR-0426568.


References
[1] G. Kuperberg and W. Kuperberg, Double-lattice packings of convex bodies
    in the plane, Discrete and Compu. Geom. 5 (1), 389 (1990).
[2] S. Gravel and V. Elser, Divide and concur: a general approach to constraint
    satisfaction, Phys. Rev. E 78, 036706 (2008).
[3] J. H. Conway and S. Torquato, Packing, tiling and covering with tetrahedra,
    Proc. Natl. Acad. Sci. USA 103, 10612 (2006).
[4] E. R. Chen, A dense packing of regular tetrahedra, Discrete and Compu.
    Geom. 5 (2), 214 (2008).
[5] S. Torquato and Y. Jiao, Dense packings of the Platonic and Archimedean
    solids, Nature 460, 876 (2009).
[6] S. Torquato and Y. Jiao, Dense packings of polyhedra:            Platonic and
    Archimedean solids, Phys. Rev. E 80, 041104 (2009).
[7] A. Haji-Akbari, M. Engel et al., Disordered, quasicrystalline and crystalline
    phases of densely packed tetrahedra, Nature 462, 773 (2009).
[8] D. J. Hoylman, The densest lattice packing of tetrahedra, Bull. Amer. Math.
    Soc. 76, 135 (1970).

                                         8
[9] L. A. Danzer, "A family of 3D-spacefillers not permitting any periodic or
    quasiperiodic tiling", in Aperiodic ’94, eds. G. Chapuis and W. Paciorek,
    World Scientific, Singapore, pp. 11-17 (1994).
[10] E. Agrell et al., Closest point search in lattices, IEEE Trans. Inform. Theory
    48, 2201 (2002).
[11] N. D. Mermin, The space groups of icosahedral quasicrystals and cubic,
    orthorhombic, monoclinic, and triclinic crystals, Rev. Modern Phys. 64, 3
    (1992).




                                        9
