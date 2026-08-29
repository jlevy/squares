5
2
0
2

t
c
O
0
2

]
T
G
.
h
t
a
m

[

1
v
7
0
7
7
1
.
0
1
5
2
:
v
i
X
r
a

Square-section braid groups and
Higman-Neumann-Neumann extensions

Omar Alvarado-Gardu˜no and Jes´us Gonz´alez

October 21, 2025

Abstract

For positive integers n, p and q with pq − n > 0, let UC(n, p × q) denote the con-
figuration space of n unlabelled hard unit squares in the rectangle [0, p] × [0, q], and let
Bn(p × q) denote the corresponding fundamental group.
It is known that, as pq − n
becomes large, UC(n, p × q) starts capturing homotopical properties of the classical con-
figuration space of n unlabelled pairwise-distinct points in the plane. At the start of
this approximation process, UC(pq − 1, p × q) is homotopy equivalent to a wedge of
(p − 1)(q − 1) circles, while the only other general families of spaces UC(n, p × q) known
to be aspherical are UC(n, p × 2) for p ≥ n, and UC(pq − 2, p × q). The fundamental
groups of the former family are known to be responsible for the “right-angled” relations
in Artin’s classical braid groups. We prove that the fundamental groups of the latter
family have a minimal presentation all whose relators are commutators. In particular,
after explaining how B2p−2(p × 2) arises as the right-angled Artin group (RAAG) associ-
ated to a certain meta-edge, we show that B3p−2(p × 3) is a Higman-Neumann-Neumann
extension of the RAAG associated to the corresponding meta-square. We provide a
geometric interpretation of the latter fact in terms of Salvetti complexes.

2020 Mathematics Subject Classification: 05C25, 20F05, 20F36, 20F65, 55R80, 57M07.
Keywords and phrases: Configurations of hard squares, Tietze transformation, right-angled Artin

group, Higman-Neumann-Neumann extension.

1

Introduction

Configuration spaces of points are pivotal in Mathematics and their applications across science.
From a purely theoretical perspective, much of their interest originates from a well known the-
orem of Fox and Neuwirth ([17]) stating that the classical configuration space UConf(R2, n) of
n unlabelled distinct points in the plane classifies Artin’s braid group Bn on n strands. More
recently, there has been an increasing interest in systems of particles with actual geometry
due to their applications outside pure mathematics. For instance, in topological robotics, con-
figuration spaces of geometric particles (CSGP) have been used in the design of algorithms
for collision-free motion planning of autonomous agents in constrained environments ([24]).
Likewise, in soft condensed matter, CSGP have applications in entropy-driven self-assembly

1

 
 
 
 
 
 
processes ([11]) whereas, in statistical mechanics, physicists have studied CSGP to gain knowl-
edge about how specific changes in system parameters (like packing density) correspond to
topological shifts and phase transitions in matter.

Remark 1.1. By examining structural and thermodynamic properties as functions of the
packing density, physicists have identified different phases in CSGP. In particular, configura-
tion spaces of 2-dimensional hard (i.e. non-overlapping) objects have been shown to undergo
through sophisticated melting processes ([9]). In the case of hard squares (modeled in part by
Definition 1.2 below), a solid phase is characterized by a widespread 4-fold symmetric crys-
talline structure whereas, in liquid and gas phases, there is a lack of spatial periodicity. Now,
while no sharp difference has been observed between a gas and a liquid phase, the melting
process is particularly interesting as it involves in fact three phases, where a tetratic phase
holding in a narrow density window separates a solid phase from an isotropic liquid phase. In
this relatively brief tetratic phase, hard squares can drift but they still assemble structures
with a 4-fold symmetry that decays slowly with distance.

Motivated by their subtle topological aspects, mathematicians have began to study CSGP
([3, 4, 5, 6, 7, 13, 21, 23]). The configuration spaces we address in this paper were first studied
systematically in mathematical terms by Alpert in [3].

Definition 1.2 (Section 2 of [3]). For positive integers n, p, q with n ≤ pq, C(n, p × q) stands
for the configuration space of n labelled closed non-overlapping unit squares, whose sides are
parallel to the canonical axes, and lie inside the rectangle Rp,q := [0, p] × [0, q]. We stress the
fact that the non-overlapping condition does not exclude the possibility that unit squares touch
each other at their boundaries, or touch the boundary of Rp,q —so, in physics terminology,
these are hard squares. The n-th symmetric group acts freely on C(n, p × q) by permutation
of the labelled squares, and the corresponding orbit space, denoted by UC(n, p × q), is referred
to as the unlabelled configuration space of n hard squares in Rp,q.

Note that UC(n, p × q) is contractible when min(p, q) = 1. We thus assume p ≥ q ≥ 2
from now on, so that UC(n, p × q) is path-connected ([8, Subsection 3.2]). As explained in
the introductory section of [8], the fundamental group

Bn(p × q) := π1(UC(n, p × q))

can be thought of as a (p, q)-approximation of Bn := π1(UConf(R2, n)). It has been observed
that the spaces UC(n, p × q) would in general fail to be aspherical ([22, Theorem 3.2]), yet a
few notable exceptions are known (Proposition 1.3 below), and we focus on describing their
homotopy types through the corresponding fundamental groups Bn(p × q).

Proposition 1.3 ([8, Theorems 1.4 and 1.5], [4, page 2597] and [5, Theorem 3.6]). Spaces
UC(n, p × q) of the following three types are aspherical:

(1) UC(n, p × 2) for n ≤ p.

(2) UC(pq − 1, p × q).

(3) UC(pq − 2, p × q).

2

The homotopy type of spaces of types (1) and (2) in Proposition 1.3 have recently been
described (see Remark 1.5 below). The main result in this paper is a description of the
homotopy type of all spaces of type (3). Such a task is attained in Theorem 2.2 below
through an explicit presentation of the corresponding fundamental group. The following
standard constructions will be convenient for our purposes. Details can be found in [12].

Definition 1.4. For a simple connected graph Γ, let ∆(Γ), Sal(Γ) and RAAG(Γ) stand,
respectively, for the flag (clique) complex, the Salvetti complex and the right-angled Artin
group (RAAG) determined by Γ. Thus Sal(Γ) is the polyhedral power (S1)∆(Γ), a classifying
space for RAAG(Γ).

Remark 1.5. The description of the homotopy type of a space of type (2) in Proposition 1.3
is straightforward. Namely, let Nℓ stand for the graph with ℓ vertices and no edges. Then, as
shown in [8, Theorem 1.4], Bpq−1(p × q) ∼= RAAG(N(p−1)(q−1)), the free non-abelian group of
rank (p − 1)(q − 1), so UC(pq − 1, p × q) ≃ Sal(N(p−1)(q−1)), the wedge of (p − 1)(q − 1) copies
of the circle S1. The homotopy type of a space of type (1) in Proposition 1.3 can be given
on similar grounds, though details are slightly more involved due to the presence of higher
dimensional cells. Indeed, for n ≤ p, Bn(p × 2) ∼= RAAG(Gn) so UC(n, p × 2) ≃ Sal(Gn),
where Gn is the graph obtained from the complete graph on n − 1 vertices after removing the
edges of a maximal linear tree ([8, Theorem 1.1]). In particular, the homotopy dimension of
UCn(p × 2) is hdim(UCn(p × 2)) = ⌊n/2⌋.

u1
•

•
vk

u2
•

•
vk−1

· · ·

· · ·

uk−1
•

•
v2

uk
•

•
v1

Figure 1: The bipartite graph Ek. Edge thickness suggests “v-families” of edges. Since ui and
vi are vertices of degree i, these families are dually reorganized by turning Ek upside down.

Remark 1.6. The homotopy type of a space of type (3) in Proposition 1.3 is known for
q = 2 ([8, Theorem 1.5]). We review the answer for comparison purposes. For a non-negative
integer k, let Ek stand for the bipartite graph depicted in Figure 1 with vertices ui and vi, for
1 ≤ i ≤ k, and an edge ei,j joining ui and vj whenever i + j > k. Additionally, for a graph
Γ, let k + Γ stand for the graph obtained by adding k isolated vertices to Γ. For instance,
E0 = ∅ and 0 + Γ = Γ. Then B2(2 × 2) ∼= RAAG(N1) = Z, so UC(2, 2 × 2) ≃ Sal(N1) = S1
while, for p ≥ 3, B2p−2(p × 2) ≃ RAAG(3 + Ep−3). In particular hdim(UC(2p − 2, p × 2)) = 2
with UC(2p − 2, p × 2) a union of 2-torii. For instance UC(6, 4 × 2) ≃ (S1 × S1) ∨ UC(4, 3 × 2)
and UC(4, 3 × 2) ≃ W

3 S1.

Remark 1.7. As shown in [8, Theorem 1.1], the isomorphism Bn(p × 2) ∼= RAAG(Gn) holds
true in the extended range n ≤ 2p−5 (though asphericity of UC(n, p×2) is not asserted in the
extended range). This leaves us with a situation that matches, at the fundamental-group level,

3

the lack of sharp differences between liquid and gas phases, as well as the existence of a brief
tetratic phase (Remark 1.1). Indeed, all spaces UC(n, p×2) with n ≤ 2p−5 are π1-isomorphic,
and are thus said to have a (π1-indistinguishable) liquid-gas topology. The few remaining
spaces UC(n, p × 2) with 2p − 4 ≤ n ≤ 2p − 1 are then said to have a (π1-indistinguishable)
tetratic topology. As reviewed above, the first two tetratic topologies, namely the cases with
n = 2p−1 and n = 2p−2, are encoded by the graphs Np−1 and 3+Ep−3, respectively, through
RAAG-Sal constructions. The point here is that, while Remark 1.5 says that the description of
B2p−1(p × 2) extends in a straightforward way to Bpq−1(p × q), our main results (Theorems 2.2
and 2.5 below) show that the q ≥ 3 case of the second tetratic topology (i.e. spaces of type
(3) in Proposition 1.3) retains only a subtle amount of the RAAG features we have reviewed
in this introductory section. Details are spelled out in the next section.

2 Main results

Definition 2.1. A group is said to be simple commutator-related provided it admits a finite
presentation whose relators are commutators [a, b] := aba−1b−1 of elements a and b —neither
of which is assumed to be a generator in the given presentation. Such a presentation is said
to be a simple commutator-related structure of G.

Note that a RAAG is nothing but a group with a simple commutator-related structure

whose relators are commutators of actual generators in the given structure.

Theorem 2.2. For p, q ≥ 3, the aspherical space UC(pq − 2, p × q) has torsion-free homology
and homotopy dimension given by

hdim(UC(pq − 2, p × q)) =






1,
2,

p = q = 3;
otherwise.

The fundamental group Bpq−2(p×q) has a simple commutator-related structure with β1 genera-
tors and β2 relators —we stress that all relators are commutators— where β1 := (p−1)(q−1)+1
and

β2 :=

(p2 + 1)(q2 + 1) − pq(2p + 2q + 3) + 7(p + q − 1)
2

are, respectively, the first and second Betti numbers of UC(pq − 2, p × q).

Generators and relators for the presentation of Bpq−2(p × q) in Theorem 2.2 are spelled

out in Section 4. Although technical, the presentation is as efficient as possible.

Corollary 2.3. The presentation of Bpq−2(p × q) in Theorem 2.2 has the minimal possible
number of generators and relators. Explicitly, any finite presentation (whether or not of simple
commutator-related type) of Bpq−2(p × q) must have at least β1 generators and β2 relators.

Proof. Given the torsion-free assertion in Theorem 2.2, this is a standard consequence of the
Hurewicz theorem in dimension 1 and of Hopf’s formula (see Exercise 5 at the bottom page
46 of [10]).

4

Tietze transformations can be applied to a given simple commutator-related group in the
hope of identifying a new basis in terms of which a RAAG structure arises. This is what
happens in all instances reviewed in Remark 1.6, as well as in a few additional instances with
min(p, q) = 3 of Theorem 2.2 (see Examples 2.4 below). Although the idea fails to identify a
RAAG structure in Bpq−2(p × q) for general p, q ≥ 3, it leads us to a description (Theorem 2.5
below) of Bpq−2(p × q), for min(p, q) = 3, as an HNN extension of the RAAG associated to
a (literally) squared version of the graph in Figure 1. Before spelling out the answer, it is
In what follows we write
convenient to illustrate the situation in a few exceptional cases.
G = Fk to mean that G is a free non-abelian group of rank k, while the more specific notation
G = F (x1, . . . , xk) is used to indicate a set of generators.
Examples 2.4. Recall from Remark 1.6 the isomorphism B2p−2(p × 2) ∼= RAAG (3 + Ep−3),
valid for p ≥ 3. Concerning B3p−2(p × 3), the methods in this paper yield:

1. For p = 3, B7(3 × 3) ∼= RAAG(5) = F5, while B4(3 × 2) ∼= RAAG(3) = F3.

2. For p = 4, B10(4 × 3) ∼= RAAG

(cid:18)

(cid:19)

• • + 3
• •

, while B6(4 × 2) = RAAG

(cid:18)

(cid:19)

• + 3
•

.

3. For p = 5, B13(5 × 3) ∼= RAAG

•

•

•

•

•

•

•

•

!

+ 1

, while B8(5 × 2) = RAAG

!
.

•
• + 3
•
•

Item 1 is just too small, but items 2 and 3 already suggest the key pattern. Namely, if
we think of the graph Ep−3 in the case q = 2 as a “p-meta-edge”, then the graph relevant
for q = 3 would be a “p-meta-square”. Yet, some subtleties are still missing in Examples 2.4.
Namely, there is indeed a generator vp of B3p−2(p × 3) corresponding to the copy of F1 that
splits off from B13(5 × 3). However, for p ≥ 6, this generator turns out to be related to several
of the remaining generators. So, it is more illuminating to write item 3 in Examples 2.4 in
the form

B13(5 × 3) ∼= RAAG

•

•

•

•

• !
•

•

•

⋆ φ5 ,

namely, as the (trivial) HNN extension of a RAAG resulting from adding a stable letter v5
that conjugates the trivial subgroup 1 to itself via φ5 : 1 ! 1. Cases p = 6 in Figure 2 and
p = 7 in Figure 3 preserve this form, except that the subgroups conjugated by vp are no longer
trivial but free. All cases p ≥ 8 have fully general characteristics. The case p = 8 is depicted
in Figure 4.

Theorem 2.5. For p ≥ 5 and q = 3, there is an isomorphism

B3p−2(p × 3) ∼= RAAG(Sp−3) ⋆ φp

expressing B3p−2(p × 3) as the HNN extension of the RAAG associated to the graph Sp−3 with
respect to the isomorphism φp : RAAG(Xp−3) ! RAAG(Yp−3), where:

1. Sp−3 is the “square-type” bipartite graph with vertices xi, x′

i, y′

i and yi for 1 ≤ i ≤ p − 3,

and the following two types of edges:

5

 
 
 
B16(6 × 3) ∼= RAAG




















x′
2

•

x′
1

•

x3

•

•

x2

x′
3
•

y′
1
•

•

x1

•

y3




















y′
2

•

•

y′
3

y1

•

•

y2

⋆ φ6

Figure 2: B16(6 × 3) is the HNN extension of the indicated “square-type” RAAG with respect
) ! F (y1, y′
. So, the
to the isomorphism φ6 : F (x1, x′
1
1
hold in B16(6 × 3). Note that the subgroup generated
= y′
relations v6x1v−1
= y1 and v6x′
1v−1
6
6
1
, respectively) is free, as the subgraph generated by these two
(by y1 and y′
by x1 and x′
1
1
vertices has no edges.

) given by φ6(x1) = y1 and φ6(x′
1

) = y′
1

• Whenever i + j > p − 3, there are four edges: one between xi and x′

j, one between

i and y′
x′

j, one between y′

i and yj, and one between yi and xj.

• Whenever i + j < p − 5, there are two edges: one between xi and x′

j, and one

between y′

i and yj.

2. RAAG(Xp−3) and RAAG(Yp−3) are the full subRAAGs of RAAG(Sp−3) associated to
induced subgraphs Xp−3 and Yp−3 of Sp−3. Here Xp−3 is induced by the vertices xi and
i with 1 ≤ i ≤ p − 5.
i with 1 ≤ i ≤ p − 5, while Yp−3 is induced by the vertices yi and y′
x′
3. The isomorphism φp : RAAG(Xp−3) ! RAAG(Yp−3) is determined by φp(xi) = yp−i−4

and φp(x′
i

) = y′

p−i−4, for 1 ≤ i ≤ p − 5.

A classifying space for an HNN extension can be constructed as a mapping torus ([18,

Example 1B.13]), so:

ιY −- RAAG(Yp−3).
Corollary 2.6. Consider the inclusions RAAG(Xp−3)
For p ≥ 6, UC(3p − 2, p × 3) is homotopy equivalent to the mapping-cylinder realization (say,
using Salvetti complexes) of the graph of groups

ιX,−! RAAG(Sp−3)

RAAG(Xp−3)

ιX

ιY ◦φp

RAAG(Sp−3).

Although geometrically appealing, the 3-dimensional mapping torus in Corollary 2.6 is not

efficient homotopicaly speaking, as hdim(UC3p−2(p × 3)) ≤ 2 (Theorem 2.2).

6

(cid:53)
(cid:53)
(cid:40)
(cid:40)
B19(7 × 3) ∼= RAAG


























x′
4

•

•

x′
3

•

x′
2

•

x′
1

x4

•

x3

•

x2

•

•

x1

y′
1

•

•

y′
2

•

y′
3

•

y′
4

y1

•

y2

•

y3

•

•

y4


























⋆ φ7

Figure 3: The first subgroup under conjugation is generated by x1, x2, x′
1
second one is generated by y′
1
between these vertices. The isomorphism φ7 : F (x1, x2, x′
by φ7(xi) = y3−i and φ7(x′
i
rest of the generators via the relations v7xiv−1
7

, while the
, y1 and y2. They are again free due to the lack of edges
) is now given
, for i = 1, 2, so the stable generator v7 is related to the
iv−1
7

= y3−i and v7x′

) ! F (y1, y2, y′

(1 ≤ i ≤ 2).

and x′
2

) = y′

1, x′
2

1, y′
2

, y′
2

= y′

3−i

3−i

B22(8 × 3) ∼= RAAG































x′
5

•

•

x′
4

•

x′
3

•

x′
2

•

x′
1

x5

•

x4

•

x3

•

x2

•

•

x1

y′
1

•

•

y′
2

•

y′
3

•

y′
4

•

y′
5

y1

•

y2

•

y3

•

y4

•

•

y5































⋆ φ8

1, x′

2, x′
3

= y4−i and v8x′

Figure 4: The domain of the isomorphism φ8 defining the HNN extension is generated by
, while the codomain is generated by the corresponding “y” elements. The
x1, x2, x3, x′
isomorphism is determined by φ8(xi) = y4−i and φ8(x′
, for 1 ≤ i ≤ 3, which correspond
) = y′
i
to relations v8xiv−1
(1 ≤ i ≤ 3) in B22(8 × 3). These relations
8
4−i
together with the stable letter v8 must then be added to the RAAG presentation of the
indicated graph to yield a presentation for B22(8 × 3). The two “unexpected” RAAG-type
1y1 correspond to the two thick edges. The
commutation relations x1x′
= y′
1
former one, for instance, is forced from the fact that v8x1v−1
.
= y′
= y3 commutes with v8x′
8
3
In particular, neither the domain nor the domain of φ8 are free; they are instead RAAGs
associated to the induced subgraphs.

1x1 and y1y′

1v−1
8

iv−1
8

= y′

= x′

4−i

1

7

4

3

2

1

•

•

•

•
1

•

•

•

•
2

•

•

•

•
3

•

•

•

•
4

•

•

•

•
5

•

•

•

•
6

Figure 5: The graph Γ6,4. Fill in the 15 loops with solid squares to get the complex Puz6,4.

3 Discrete configuration space

For a CW complex X with cells e, the discrete configuration space DConf(X, n) of n non-
colliding labelled cells of X is the subcomplex of X n consisting of the cells

(e1, . . . , en) := e1 × · · · × en

satisfying ei ∩ ej = ∅ for i ̸= j. The corresponding unordered discrete configuration space
UDConf(X, n) is the quotient complex of DConf(X, n) by the cellular free action of the sym-
metric group Σn on n letters that permutes cell coordinates. The cell of UDConf(X, n) given
by the Σn-orbit of (e1, . . . , en) is denoted by {e1, . . . , en}. For X = Γ a graph, this construction
was first studied in Abrams’ Ph.D. thesis ([2]).

Theorem 3.1 ([2]). For a graph Γ, DConf(Γ, n) and UDConf(Γ, n) are aspherical (only the
former space might fail to be path-connected, but even so all of its components are aspherical).

Let Γp,q be the 1-skeleton of the cube complex Puzp,q obtained by restricting to [1, p]×[1, q]

the standard 2-dimensional cube-complex structure on the plane. See Figure 5.

Proposition 3.2 ([4]). DConf(Puzp,q, n) sits inside C(n, p × q) as a strong Σn-equivariant
deformation retract. In particular UDConf(Puzp,q, n) ∼= UC(n, p × q).

Observe that UDConf(Γp,q, n) is a subcomplex of UDConf(Puzp,q, n), and they share a com-
mon 1-skeleton. Indeed, any cell {e1, . . . , en} of UDConf(Puzp,q, n) outside UDConf(Γp,q, n)
has dimension at least 2, as one of the cell ingredients ei would have to be an actual square
of Puzp,q. So, just as UDConf(Γp,q, n), UDConf(Puzp,q, n) is path-connected. In fact

UDConf(Γp,q, n) = UDConf(Puzp,q, n), which is at most 2-dimensional if n ≥ pq − 2,

(1)

for then there is no room for a square-type cell ingredient ei, nor for three or more edge-type
cell ingredients ei. In particular, Theorem 3.1, Proposition 3.2 and (1) give the asphericity
of UC(n, p × q) noted in Proposition 1.3 when n ≥ pq − 2. Likewise, (1) and Proposition 3.2
yields the estimate

hdim(UC(pq − 2, p × q)) ≤ 2
relevant for Theorem 2.2 (see also Lemma 3.3 below). The sharpness of this estimate for
max(p, q) > min(p, q) ≥ 3 will follow once we argue the homological assertions in Theorem 2.2.

(2)

8

The discrete Morse theoretic method in [14, Theorem 2.5] was applied in [8] to the cubical
homotopy model UDConf(Puzp,q, n) of UC(n, p × q) in order to produce a raw presentation
of the fundamental group Bn(p × q). In the case of interest for us, namely n = pq − 2 so
(1) holds, this is done in terms of the gradient field on UDConf(Γp,q, pq − 2) constructed by
Farley-Sabalka with respect to a certain maximal tree Tp,q for Γp,q. Details are spelled out in
[8, Subsection 2.2], from which Lemma 3.3 below follows by direct counting. In addition, the
presentation for Bpq−2(p × q) summarized in Proposition 3.4 below is easily extracted from
the discussion in [8, Section 4] using the notation in [8, Example 4.5].

Lemma 3.3. For p ≥ q ≥ 3, Farley-Sabalka’s discrete gradient field on the homotopy model
UDConf(Γp,q, pq − 2) of UC(pq − 2, p × q) has ci critical cells of dimension i, where

c0 = 1,

c1 = 3(p − 1)(q − 1) − 2,

c2 =

 (p − 1)(q − 1)
2

!

− (p − 2)(q − 2)

and ci = 0 for i ̸= 0, 1, 2.

The harmless assumption p ≥ q in Lemma 3.3, immaterial for the given conclusion, is
relevant for the choosing of the maximal tree Tp,q and, thus, for the actual gradient field on
UDConf(Γp,q, pq − 2), as well as for the resulting presentation of Bpq−2(p × q) described next.

Proposition 3.4. For p ≥ q ≥ 3, the group Bpq−2(p × q) is presented with generators aℓ,i, bℓ,i
and cℓ,i, for 1 ≤ ℓ ≤ q − 1 and 1 ≤ i ≤ p − 1, and relators

cℓ,iaℓ+1,jb−1

a1,1 and cq−1,1.
ℓ,i c−1
bℓ,iaℓ,jb−1
ℓ,j ,
ℓ,i b−1
ℓ+1,j,
[cℓ,i , aℓ+1,j],
[cℓ,i , aλ,j],

for 1 ≤ ℓ ≤ q − 1, 1 ≤ i < j ≤ p − 1.
for 1 ≤ ℓ ≤ q − 2, 1 ≤ i ≤ p − 1, 1 ≤ j ≤ p − i.
for 1 ≤ ℓ ≤ q − 2, i, j ∈ {3, 4, . . . , p − 1}, p + 2 ≤ i + j.
for 2 ≤ ℓ + 1 < λ ≤ q − 1, i, j ∈ {1, 2, . . . , p − 1}.

(3)
(4)

(5)

4 Simple commutator-related structure

Assuming p ≥ q ≥ 3, in this section we describe a process of Tietze transformations that
leads to a reduction/simplification of generators/relations in the presentation of Bpq−2(p × q)
in Proposition 3.4. Key portions of this process have been suggested by computer exploration.
Use the relators in (5) with i = j = 1 and the relators in (4) with i = 1 to eliminate,

respectively, cℓ,1 and cℓ,j for 2 ≤ j via the substitutions

cℓ,1 = bℓ+1,1bℓ,1a−1

ℓ+1,1,
cℓ,j = bℓ,1aℓ,jb−1
ℓ,1 ,

for 1 ≤ ℓ ≤ q − 2 (because of (3), cq−1,1 is negligible),
for 1 ≤ ℓ ≤ q − 1 and 2 ≤ j ≤ p − 1.

(6)

For instance, after applying the substitutions in (6), relators in (4) take the form

bℓ,iaℓ,jb−1

ℓ,i bℓ,1a−1

ℓ,j b−1
ℓ,1

or, after a cyclic shift, aℓ,jb−1

ℓ,i bℓ,1a−1

ℓ,j b−1

ℓ,1 bℓ,i,

9

ℓ,i bℓ,1]. Note that the latter form of
which can be written down as the commutator [aℓ,j , b−1
the relator can equivalently be written down as [aℓ,j , b−1
ℓ,1 bℓ,i]. This type of manipulations will
be used without further notice in what follows. We get a presentation of Bpq−2(p × q) with
generators aℓ,i and bℓ,i with 1 ≤ ℓ ≤ q − 1 and 1 ≤ i ≤ p − 1, and relators

bℓ,1a−1

[aℓ,j , b−1
ℓ,1 b−1
ℓ,1 aℓ+1,jb−1

ℓ+1,1aℓ+1,jb−1
bℓ,1aℓ,ib−1

a1,1,
ℓ,1 bℓ,i],
ℓ+1,jbℓ+1,1,
ℓ,i b−1
ℓ+1,j,
ℓ,1 , aℓ+1,j],
ℓ+1,1 , aλ,j],
ℓ,1 , aλ,j],

(7)
(8)

for 1 ≤ ℓ ≤ q − 1, 2 ≤ i < j ≤ p − 1,
for 1 ≤ ℓ ≤ q − 2, 2 ≤ j ≤ p − 1,
for 1 ≤ ℓ ≤ q − 2, 2 ≤ i ≤ p − 1, 1 ≤ j ≤ p − i,
for 1 ≤ ℓ ≤ q − 2, i, j ∈ {3, 4, . . . , p − 1}, p + 2 ≤ i + j,
for 2 ≤ ℓ + 1 < λ ≤ q − 1, 1 ≤ j ≤ p − 1,
(12)
for 2 ≤ ℓ + 1 < λ ≤ q − 1, 2 ≤ i ≤ p − 1, 1 ≤ j ≤ p − 1. (13)

(11)

(10)

(9)

[bℓ,1aℓ,ib−1
[bℓ+1,1bℓ,1a−1

[bℓ,1aℓ,ib−1

Next, replace the generators bℓ,i having 1 ≤ ℓ ≤ q − 1 and 2 ≤ i ≤ p − 1 by corre-
ℓ,1 bℓ,i. (In terms of Tietze transformations, this means we add
sponding generators Bℓ,i := b−1
generators Bℓ,i and relators Bℓ,ib−1
ℓ,i bℓ,1, and then eliminate the generators bℓ,i via substitutions
bℓ,i = bℓ,1Bℓ,i.) With these operations, relators with ℓ = j = 1 in (10) can be written as
B−1

1,1a2,1, which allows us to eliminate generators B1,i via the substitutions

2,1b1,1a1,ib−1

1,1b−1

1,i b−1

B1,i = b−1

1,1b−1

2,1b1,1a1,ib−1

1,1a2,1,

for 2 ≤ i ≤ p − 1.

Likewise, relators in (9) can be written as bℓ,1a−1
generators Bℓ+1,j via the substitutions

ℓ+1,1aℓ+1,jb−1

ℓ,1 B−1

ℓ+1,j

, allowing us to eliminate

Bℓ+1,j = bℓ,1a−1

ℓ+1,1aℓ+1,jb−1
ℓ,1 ,

for 1 ≤ ℓ ≤ q − 2, 2 ≤ j ≤ p − 1.

We are then left with a presentation of Bpq−2(p×q) with generators aℓ,i and bℓ,1 for 1 ≤ ℓ ≤ q−1
and 1 ≤ i ≤ p − 1, and relators

bℓ,1aℓ,ib−1

ℓ,1 aℓ+1,1bℓ−1,1a−1
2,1b1,1a−1

1,i b−1

b1,1a1,ib−1

1,1a2,ja−1

bℓ,1aℓ,ib−1

ℓ,1 aℓ+1,jbℓ−1,1a−1

ℓ,i aℓ,1b−1

[a1,j , b−1

1,1b−1
[aℓ,j , bℓ−1,1a−1
ℓ,i aℓ,1b−1
1,1b2,1b1,1a−1

2,1b1,1a1,ib−1
ℓ,1 aℓ,ib−1
ℓ,1 b−1
ℓ−1,1b−1
2,j a2,1b−1
ℓ,1 b−1

1,1a2,1],
ℓ−1,1],
ℓ+1,1,
1,1b−1
2,1,
ℓ+1,1,

ℓ+1,jaℓ+1,1b−1

ℓ−1,1a−1

for 2 ≤ i < j ≤ p − 1,

for 2 ≤ ℓ ≤ q − 1, 2 ≤ i < j ≤ p − 1,

for 2 ≤ ℓ ≤ q − 2, 2 ≤ i ≤ p − 1,

for 2 ≤ i ≤ p − 2, 2 ≤ j ≤ p − i,

(14)

(15)

(16)

(17)

for 2 ≤ ℓ ≤ q − 2, 2 ≤ i ≤ p − 2, 2 ≤ j ≤ p − i, (18)

together with those in (7) and (11)–(13), which have no change under the indicated Tietze
transformations. Note that (14) and (15) come from (8), whereas (16)–(18) come from (10).
For the next round of Tietze transformations, set uℓ := bℓ,1 for 1 ≤ ℓ ≤ q − 1 and replace
ℓ aℓ+1,1. In addition,
the generators aℓ+1,1 (1 ≤ ℓ ≤ q − 2) by corresponding generators vℓ := u−1
set A1,i := a1,i for 2 ≤ i ≤ p − 1, and replace the generators aℓ,i with 2 ≤ ℓ ≤ q − 1 and
ℓ−1aℓ,i. This yields a presentation for
2 ≤ i ≤ p − 1 by corresponding generators Aℓ,i := v−1
Bpq−2(p × q) with generators

ℓ−1u−1

Aℓ,i for 1 ≤ ℓ ≤ q − 1 and 2 ≤ i ≤ p − 1 (because of (7), a1,1 is negligible),
uℓ for 1 ≤ ℓ ≤ q − 1, together with vℓ for 1 ≤ ℓ ≤ q − 2,

(19)

10

and relators

1 u−1

[A1,j , u−1

2 u1A1,iv1],
[uℓ−1vℓ−1Aℓ,j , uℓ−1Aℓ,iu−1
ℓ−1],
ℓ−1u−1
ℓ u−1
ℓ+1,
2 u1A1,iv1 , A2,j],
ℓ−1A−1
ℓ+1,ju−1
ℓ u−1
ℓ+1,

ℓ,i u−1

for 2 ≤ i < j ≤ p − 1,

for 2 ≤ ℓ ≤ q − 1, 2 ≤ i < j ≤ p − 1,

for 2 ≤ ℓ ≤ q − 2, 2 ≤ i ≤ p − 1,

for 2 ≤ i ≤ p − 2, 2 ≤ j ≤ p − i,

(20)

(21)

(22)

(23)

for 2 ≤ ℓ ≤ q − 2, 2 ≤ i ≤ p − 2, 2 ≤ j ≤ p − i,

(24)

uℓuℓ−1vℓ−1Aℓ,ivℓuℓ−1A−1

[u−1
1 u−1
uℓuℓ−1vℓ−1Aℓ,ivℓAℓ+1,juℓ−1A−1
ℓ,i u−1

and those coming from (11)–(13) which, after the indicated transformations, become

[A1,i , v1A2,ju1],
[uℓ−1vℓ−1Aℓ,i , vℓAℓ+1,juℓ],
[uℓ+1uℓv−1
ℓ u−1
ℓ
[u1A1,iu−1
1

, uλ−1vλ−1Aλ,j],

, uλ−1vλ−1],

, uλ−1vλ−1],

ℓ u−1

ℓ

[uℓ+1uℓv−1

[u1A1,iu−1
1
[uℓuℓ−1vℓ−1Aℓ,iu−1

ℓ

, uλ−1vλ−1Aλ,j],

for i, j ∈ {3, 4, . . . , p − 1}, p + 2 ≤ i + j,

for 2 ≤ ℓ ≤ q − 2, i, j ∈ {3, 4, . . . , p − 1}, p + 2 ≤ i + j,

for 2 ≤ ℓ + 1 < λ ≤ q − 1,

for 2 ≤ ℓ + 1 < λ ≤ q − 1, 2 ≤ j ≤ p − 1,

for 3 ≤ λ ≤ q − 1, 2 ≤ i ≤ p − 1,

for 3 ≤ λ ≤ q − 1, 2 ≤ i ≤ p − 1, 2 ≤ j ≤ p − 1,

[uℓuℓ−1vℓ−1Aℓ,iu−1

ℓ

, uλ−1vλ−1Aλ,j],

for 3 ≤ ℓ + 1 < λ ≤ q − 1, 2 ≤ i ≤ p − 1, 2 ≤ j ≤ p − 1.

, uλ−1vλ−1],

for 3 ≤ ℓ + 1 < λ ≤ q − 1, 2 ≤ i ≤ p − 1,

(25)

(26)

(27)

(28)

(29)

(30)

(31)

(32)

Note that, in view of (27), (29) and (31), relators (28), (30) and (32) simplify, respectively,
, Aλ,j]. Example 4.1 below
to [uℓ+1uℓv−1
illustrates aspects of the latter presentation for q = 3, and completes the proof of Theorem 2.2
in that case.

, Aλ,j] and [uℓuℓ−1vℓ−1Aℓ,iu−1
ℓ

, Aλ,j], [u1A1,iu−1
1

ℓ u−1
ℓ

Example 4.1. Assume q = 3, so that there are no relators (22) or (24), and the previous
description is that of a simple commutator related structure. By direct counting we see that
the presentation has 2p−1 generators and 2(p−3)(p−2) relators (note that the sets of relators
(26)–(32) are also empty for q = 3). The dimension-1 case of the Hurewicz theorem then gives
H1(UC3p−2(p × 3)) ∼= Z2p−1, while the discussion around (1) shows that H2(UC3p−2(p × 3))
is torsion-free, say of rank β2, and that the Euler characteristic of UC3p−2(p × 3) is given
by χ = β2 − 2(p − 1). On the other hand, Lemma 3.3 and [16, Corollary 3.5] show that
χ = 1 − (6p − 8) + (cid:16)2(p−1)
− p + 2. The last two equalities yield β2 = 2(p − 3)(p − 2) which,
as noted above, is the number of relators in the simple commutator-related presentation.
Specializing to the case p = q = 3, we get B7(3 × 3) = F5, as asserted in Example 2.4.1.
In particular UC(7, 3 × 3) is homotopy equivalent to a wedge of 5 circles. However, for
p > q = 3, hdim(UC(pq − 2, p × q)) = 2, which is forced from (2) and the non-triviality of the
corresponding 2-dimensional homology group.

(cid:17)

2

In the rest of the section we assume p ≥ q ≥ 4. By (22), relators (24) can be expressed
or, equivalently, as commutator-type re-

= Aℓ+1,juℓ−1A−1

ℓ,i u−1

ℓ−1A−1

ℓ+1,j

ℓ,i u−1
ℓ−1

as relations uℓ−1A−1
lators

) · A−1
holding in the same range of values for ℓ, i and j as that indicated in (24). We then use a final
round of Tietze transformations in order to simplify the only one type of relators that have

Aℓ+1,j · (uℓ−1A−1

ℓ+1,j · (uℓ−1A−1

ℓ,i u−1
ℓ−1

ℓ,i u−1
ℓ−1

)−1,

(33)

11

not yet been written down as commutators, namely relators (22). Explicitly, the case i = 2 of
relators (22) allows us to recursively eliminate all generators uℓ+1 with ℓ = q − 2, q − 3, . . . , 2
(in that order) via the substitutions

uℓ+1 = uℓuℓ−1vℓ−1Aℓ,2vℓuℓ−1A−1

ℓ,2 u−1

ℓ−1u−1
ℓ

.

(34)

Any such substitution applied on a relator that has already been written down as a com-
mutator does not change the commutator characteristic1. Furthermore, for a fixed value of
ℓ ∈ {2, 3, . . . , q−2}, direct verification gives that a relator uℓuℓ−1vℓ−1Aℓ,ivℓuℓ−1A−1
ℓ u−1
ℓ+1
with 3 ≤ i ≤ p − 1 is transformed under the substitution in (34) into (the uℓuℓ−1vℓ−1 conjugate
of) the relator Aℓ,ivℓuℓ−1A−1

or, equivalently, the commutator-type relator

ℓ−1u−1

ℓ,i u−1

ℓ,i Aℓ,2u−1

ℓ−1v−1

ℓ A−1
ℓ,2

vℓuℓ−1 · A−1

ℓ,i Aℓ,2 · u−1

ℓ−1v−1
ℓ

· A−1

ℓ,2 Aℓ,i.

Consequently this last round of Tietze transformations renders a simple commutator-related
presentation of Bpq−2(p × q) having β1 := (p − 1)(q − 1) + 1 generators, namely u1, u2 and vℓ
for 1 ≤ ℓ ≤ q − 2, as well as Aℓ,i for 1 ≤ ℓ ≤ q − 1 and 2 ≤ i ≤ p − 1, and by direct counting
β2 := p2q2 + p2 + q2 − 2pq2 − 2p2q − 3pq + 7p + 7q − 6

> 0

2

relators (see Table 1, where the reported number of relators of type (22) takes into account
the relators that are eliminated during the last round of Tietze transformations). The fact
that β1 and β2 agree with the corresponding Betti numbers of UCpq−2(p × q) follows from an
arithmetic verification that is identical to the one used in Example 4.1. This completes the
proof of Theorem 2.2.

Table 1: Number of relators by type

type

(20)

(21)

amount

(p−3)(p−2)
2

(p−3)(p−2)(q−2)
2

(22)
(p − 3)(q − 3)

(23)

(24)=(33)

(p−3)(p−2)
2

(p−3)(p−2)(q−3)
2

type

(25)

(26)

(27)

(28)

amount

(p−3)(p−2)
2

(p−3)(p−2)(q−3)
2

(q−3)(q−2)
2

(p−2)(q−3)(q−2)
2

(29)
(p − 2)(q − 3)

type

amount

(30)
(p − 2)2(q − 3)

(31)

(p−2)(q−4)(q−3)
2

(32)
(p−2)2(q−4)(q−3)
2

5 Commutators and conjugations: The HNN extension

In this section we organize the presentation of B3p−2(p × 3) in Example 4.1. Start by using
the simplified notation u and v for the generators u1 and v1 in (19). Additionally, replace the

1The resulting substituted commutator might be trivial, i.e., of the form [a, a]. But the minimality of the

final presentation (Corollary 2.3) will prevent such a possibility.

12

generator u2 by a new generator w := u−1u2u. In these terms, relators (20)–(32) simplify to
the four types of relators

[w−1A1,iv , A1,j],
[w−1A1,iv , A2,j],
[vA2,ju , A2,i],
[vA2,ju , A1,i],

for 2 ≤ i < j ≤ p − 1,
for 2 ≤ i ≤ p − 2, 2 ≤ j ≤ p − i,
for 2 ≤ i < j ≤ p − 1,
for i, j ∈ {3, 4, . . . , p − 1}, p + 2 ≤ i + j,

(35)
(36)
(37)
(38)

where relators in (37) have been written down as u-conjugates of those in (21). For example,
with p = 4, this presentation yields the first assertion in Example 2.4.2 after the generator
:= vA2,3u.
A1,2 is replaced by A′
Actually, since the first assertion in Example 2.4.1 is covered by Example 4.1, we will assume
p ≥ 5 throughout this section. Additionally, for elements x and y of a given group, we will
use the notation x & y as a substitute of the commutation relation [x, y] = 1. Likewise, when
the notation x & y is used as a relator, we mean [x, y].

:= w−1A1,2v, and the generator A2,3 is replaced by A′

1,2

2,3

The easy verification of the following result is left as an exercise for the reader.

Lemma 5.1. Assume a2, a3, . . . , ak−1 and b2, b3 . . . , bk−1 are elements of a given group and
set a1 = 1 = bk. For 2 ≤ i ≤ k − 1, choose elements

i a±1
Then ai & bj for 2 ≤ i < j ≤ k − 1 if and only if Ai & Bj for 2 ≤ i < j ≤ k − 1.

i−1} and Bi ∈ {b±1

Ai ∈ {a±1

i−1a±1
i

i+1b±1
i

i b±1

i+1}.

, a±1

, a±1

, b±1

, b±1

i

i

We apply Lemma 5.1 with k = p in the following situations.

• Set ai := w−1A1,iv and bj := A1,j, so that relators (35) can be written in the form

w−1A1,2v & A−1
1,i−1A1,iv & A−1

1,j A1,j+1,
1,j A1,j+1,

v−1A−1

for 2 < j ≤ p − 1,
for 3 ≤ i < j ≤ p − 1.

(39)

• Relators (36) can be written in the form [w−1A1,iv , A2,p+1−j] for 2 ≤ i < j ≤ p − 1 or,

by setting ai := w−1A1,iv and bj := A2,p+1−j, in the form

w−1A1,2v & A2,p+1−jA−1
1,i−1A1,iv & A2,p+1−jA−1

2,p−j,
2,p−j,

v−1A−1

for 2 < j ≤ p − 1,
for 3 ≤ i < j ≤ p − 1.

• Set ai := A2,i and bj := vA2,ju, so that relators (37) can be written in the form

2,i−1

A2,iA−1
A2,iA−1

2,i−1

& vA2,p−1u,
& vA2,j+1A−1

2,j v−1,

for 2 ≤ i < p − 1,
for 2 ≤ i < j ≤ p − 2.

(40)

(41)

• Relators (38) can be written in the form [vA2,p+1−iu , A1,j] for 2 ≤ i < j ≤ p − 1 or, by

setting ai := vA2,p+1−iu and bj := A1,j, in the form

vA2,p+2−iA−1

vA2,p−1u & A−1
2,p+1−iv−1 & A−1

1,j A1,j+1,
1,j A1,j+1,

for 2 < j ≤ p − 1,
for 3 ≤ i < j ≤ p − 1.

(42)

13

As indicated in Lemma 5.1, here we set A1,p = 1 = A2,1. All together, we get:

Corollary 5.2. For 1 ≤ i ≤ p − 3, consider the elements α(i), β(i), γ(i) and δ(i) given by

• α(i) := A2,p−i−1A−1

2,p−i−2

(recall A2,1 = 1),

• β(i) :=






w−1A1,2v,
v−1A−1

1,p−i−2A1,p−i−1v,

i = p − 3;
1 ≤ i ≤ p − 4,

• γ(i) := A−1

1,i+2A1,i+3 (recall A1,p = 1),

• δ(i) :=






vA2,p−1u,
vA2,i+3A−1

2,i+2v−1,

i = p − 3;
1 ≤ i ≤ p − 4.

Then B3p−2(p × 3) is presented by generators u, v, w, A1,i and A2,i for 2 ≤ i ≤ p − 1, and
commutation relations α(i) & β(j), β(i) & γ(j), γ(i) & δ(j) and δ(i) & α(j) holding for
i, j ∈ {1, 2, . . . , p − 3} whenever i + j > p − 3.

Proof. The asserted commutator relations α(i) & β(j), β(i) & γ(j), γ(i) & δ(j) and δ(i) & α(j)
are those in (40), (39), (42) and (41), respectively.

Lemma 5.3. The following relations hold in B3p−2(p × 3):

(i) α(i)α(i + 1) · · · α(p − 3) = A2,p−i−1, for 1 ≤ i ≤ p − 3.

(ii) v−1δ(p − 4)vα(1)α(2) · · · α(p − 3) = A2,p−1.

(iii) γ(p − 3)−1γ(p − 4)−1 · · · γ(i)−1 = A1,i+2, for 1 ≤ i ≤ p − 3.

(iv) γ(p − 3)−1γ(p − 4)−1 · · · γ(1)−1vβ(p − 4)−1v−1 = A1,2.

(v) α(p − 3)−1α(p − 4)−1 · · · α(1)−1v−1δ(p − 4)−1δ(p − 3) = u.

(vi) γ(p − 3)−1γ(p − 4)−1 · · · γ(1)−1vβ(p − 4)−1β(p − 3)−1 = w.

(vii) vβ(p − i − 4)v−1 = γ(i), for 1 ≤ i ≤ p − 5.

(viii) vα(p − i − 4)v−1 = δ(i), for 1 ≤ i ≤ p − 5.

Extensive calculations based on Tietze transformations led the authors to realize that the
commutation relations in Corollary 5.2 and relations (vii) and (viii) in Lemma 5.3 capture
a description of B3p−2(p × 3) as an HNN RAAG-extension. For the sake of brevity, such a
fact will be proved below through a direct argument that avoids the use of a long sequence of
Tietze transformations. In what follows Hp stands for the group presented by generators V ,
A(i), B(i), C(i) and D(i), for 1 ≤ i ≤ p − 3, and relators/relations

A(i) & B(j), B(i) & C(j), C(i) & D(j), D(i) & A(j), for i, j ∈ {1, . . . , p − 3}, i + j > p − 3, (43)
(44)
V B(p − i − 4)V −1 = C(i) and V A(p − i − 4)V −1 = D(i), for 1 ≤ i ≤ p − 5.

14

Theorem 5.4. The group morphism θ : Hp ! B3p−2(p×3) given by θ(V ) = v, θ(A(i)) = α(i),
θ(B(i)) = β(i), θ(C(i)) = γ(i) and θ(D(i)) = δ(i) for 1 ≤ i ≤ p − 3 is a well-defined
isomorphism.

Proof. Corollary 5.2 and relations (vii) and (viii) in Lemma 5.3 show that θ is well-defined.
We show that θ is an isomorphism by constructing its inverse. Consider the elements of Hp

Θ(A2,p−i−1) := A(i)A(i + 1) · · · A(p − 3), for 1 ≤ i ≤ p − 3,

Θ(A2,p−1) := V −1D(p − 4)V A(1)A(2) · · · A(p − 3),
Θ(A1,i+2) := C(p − 3)−1C(p − 4)−1 · · · C(i)−1, for 1 ≤ i ≤ p − 3,
Θ(A1,2) := C(p − 3)−1C(p − 4)−1 · · · C(1)−1V B(p − 4)−1V −1,

Θ(u) := A(p − 3)−1A(p − 4)−1 · · · A(1)−1V −1D(p − 4)−1D(p − 3),
Θ(w) := C(p − 3)−1C(p − 4)−1 · · · C(1)−1V B(p − 4)−1B(p − 3)−1,
Θ(v) := V.

(45)
(46)
(47)
(48)
(49)
(50)
(51)

Relations (I)–(VIII) below follow directly from definitions (45)–(51), with relations (44) rele-
vant for the verification of (IV) and (VIII) when i ≤ p − 5.

(I) Θ(A2,p−i−1)Θ(A2,p−i−2)−1 = A(i), for 1 ≤ i ≤ p − 4.

(II) Θ(A2,2) = A(p − 3).

(III) Θ(w)−1Θ(A1,2)Θ(v) = B(p − 3).

(IV) Θ(v)−1Θ(A1,p−i−2)−1Θ(A1,p−i−1)Θ(v) = B(i), for 1 ≤ i ≤ p − 4.

(V) Θ(A1,i+2)−1Θ(A1,i+3) = C(i), for 1 ≤ i ≤ p − 4.

(VI) Θ(A1,p−1)−1 = C(p − 3).

(VII) Θ(v)Θ(A2,p−1)Θ(u) = D(p − 3).

(VIII) Θ(v)Θ(A2,i+3)Θ(A2,i+2)−1Θ(v)−1 = D(i), for 1 ≤ i ≤ p − 4.
The point then is that Corollary 5.2, relations (43) and relations (I)–(VIII) imply that elements
(45)–(51) determine a well defined morphism Θ : B3p−2(p × 3) ! Hp sending α(i), β(i), γ(i)
and δ(i), for 1 ≤ i ≤ p − 3, into A(i), B(i), C(i) and D(i), respectively.
In particular
Θ ◦ θ = 1. On the other hand, the equality θ ◦ Θ = 1 follows directly from relations (i)–(vi)
in Lemma 5.3.

We close the section by noticing that the group Hp is an HNN extension of a RAAG. Let
G be a group presented through a set of generators G and a set of relators R, and assume that
H1 and H2 are isomorphic subgroups of G. Choose an isomorphism φ : H1 ! H2 and let v ̸∈ G
be a new generator symbol. The HNN extension of G with respect to φ, denoted by G ⋆ φ, is
the group presented through generators G ∪ {v} and relators R ∪ {vhv−1 = φ(h) : h ∈ H1}. As
shown in [19], the obvious map G ! G ⋆ φ is a monomorphism. Note that, by construction,
the resulting subgroups H1 and H2 of G ⋆ φ are v-conjugated (in G ⋆ φ).

In dealing with HNN extensions of RAAGs, the following fact proves to be handy:

15

Lemma 5.5. Let G be an induced subgraph of the graph Γ, and let H be the subgroup of
RAAG(Γ) generated by the vertices of G. Then H = RAAG(G).

Proof. This is a standard property and we include proof details for completeness. The graph
inclusion G ,! Γ determines a group morphism ι : RAAG(G) ! RAAG(Γ). Since G is an
induced subgraph of Γ, the rule

v 7!






v,
1,

v is vertex of G;
otherwise,

determines a group morphism π : RAAG(Γ) ! RAAG(G) satisfying π ◦ ι = 1. In particular
ι is monic and sets the asserted isomorphism RAAG(G) ∼= Im(ι) = H.

Let Sp−3 be the graph with vertices A(i), B(i), C(i) and D(i) for 1 ≤ i ≤ p − 3 and,
whenever i + j > p − 3, four edges, one between A(i) and B(j), one between B(i) and C(j),
one between C(i) and D(j), and one between D(i) and A(j). Of course, in RAAG notation,
these edges account for relators (43). For instance, since the set of relators (44) is empty when
p = 5, Theorem 5.4 gives B13(5 × 3) ∼= H5 = RAAG(S2 + 1), which recovers the first assertion
in Example 2.4.3 as well as Theorem 2.5 for p = 5. The situation for p ≥ 6 will be fully
parallel once conjugation relations (44) are taken into account through the use of a suitable
HNN extension.

Proof of Theorem 2.5. Let Xp−3 (respectively, Yp−3) be the induced subgraph of Sp−3 gener-
ated by vertices A(i) and B(i) for 1 ≤ i ≤ p − 5 (respectively, C(i) and D(i) for 1 ≤ i ≤ p − 5).
Consider the bijection of vertices φ : V (Xp−3) ! V (Yp−3) given by

φ(B(p − i − 4)) = C(i) and φ(A(p − i − 4)) = D(i), for 1 ≤ i ≤ p − 5.

Turn φ into an isomorphism of graphs by adding to Xp−3 and to Sp−3 (respectively, to Yp−3
and to Sp−3) an edge between A(i) and B(j) (respectively, between C(i) and D(j)) whenever
i + j < p − 5. Let Sp−3, Xp−3 and Yp−3 be the resulting graph and induced subgraphs. The
proof conclusion then follows from Theorem 5.4 by noticing that the new edges amount to
commutativity relations [A(i), B(j)] = 1 and [C(i), D(j)] = 1, for i + j < p − 5 which, at any
rate, are forced by (44).

6 Epilogue: (Not) Highly subdivided graphs

Undoubtedly, discrete configuration spaces are foundational in our results. Yet, the graph we
are interested in, namely Γp,q, is far from being sufficiently subdivided, which means that the
homotopy type of the discrete configuration space UDConf(Γp,q, n) is not guaranteed to agree
with that of the regular (point-wise) configuration space UConf(Γp,q, n) (see [2, Theorem 2.1]).
Actually both topologies differ in general. For instance, for p ≥ 2, the first Betti number of
UDConf(Γp×2, 2p − 2) is 2p − 3 (Remark 1.6), whereas the results in [20, Subsection 3.2] yield
H1(UConf(Γp×2, 2p − 2)) = Z.

Despite intrinsic differences between discrete and point-wise configuration space models,
the form of our results fits within general properties of (classical) graph braid groups. For

16

instance, on a computational perspective, it is striking to remark that the first Betti number
reported in Theorem 2.2 agrees with that found by Ko-Park in [20, Subsection 3.2] for the
point-wise configuration space UConf(Γp,q, n) for any n ≥ 2. Theoretical coincidences are
also notable. For one, H∗(UDConf(Γp,q, pq − 2)) is torsion-free, which matches the point-wise
fact proved in [20, Corollary 3.6] for planar graphs (such as Γp,q). Likewise, we have proved
that π1(UDConf(Γp,q, pq − 2)) is a simple commutator-related group, which aligns with [20,
Conjecture 4.9]. Furthermore, closely related to the simple commutator-related property is the
possibility of having a graphical description, as disjoint circuits, of the factors in commutator
relators. Such a situation has been shown to hold for UConf(Γ, 2) when Γ is planar (see [20,
Theorem 4.8] and [15, Theorem 5.6 and Conjecture 5.7]). This property also arises for the
simple commutator-related group Bpq−2(p × q). Details will be spelled out elsewhere.

The similarities/differences between discrete and point-wise configuration spaces make it
clear that the study of the former ones, whether or not their homotopy type agree with that
of the latter ones, is an interesting and rich subject of research. See for instance [1].

References

[1] Aaron Abrams, David Gay, and Valerie Hower. Discretized configurations and partial

partitions. Proc. Amer. Math. Soc., 141(3):1093–1104, 2013.

[2] Aaron David Abrams. Configuration spaces and braid groups of graphs. ProQuest LLC,

Ann Arbor, MI, 2000. Thesis (Ph.D.)–University of California, Berkeley.

[3] Hannah Alpert. Discrete configuration spaces of squares and hexagons. J. Appl. Comput.

Topol., 4(2):263–280, 2020.

[4] Hannah Alpert, Ulrich Bauer, Matthew Kahle, Robert MacPherson, and Kelly Spendlove.
Homology of configuration spaces of hard squares in a rectangle. Algebr. Geom. Topol.,
23(6):2593–2626, 2023.

[5] Hannah Alpert, Matthew Kahle, and Robert MacPherson. Configuration spaces of disks

in an infinite strip. J. Appl. Comput. Topol., 5(3):357–390, 2021.

[6] Hannah Alpert, Matthew Kahle, and Robert MacPherson. Asymptotic Betti numbers for
hard squares in the homological liquid regime. Int. Math. Res. Not. IMRN, (10):8240–
8263, 2024.

[7] Hannah Alpert and Fedor Manin. Configuration spaces of disks in a strip, twisted alge-

bras, persistence, and other stories. Geom. Topol., 28(2):641–699, 2024.

[8] Omar Alvarado-Gardu˜no, Jes´us Gonz´alez, and Matthew Kahle. A combinatorial genesis
of the right-angled relations in Artin’s classical braid groups. Preprint available from
https://doi.org/10.48550/arXiv.2504.12201.

[9] Joshua A. Anderson, James Antonaglia, Jaime A. Millan, Michael Engel, and Sharon C.
Glotzer. Shape and symmetry determine two-dimensional melting transitions of hard
regular polygons. Phys. Rev. X, 7:021001, Apr 2017.

17

[10] Kenneth S. Brown. Cohomology of groups, volume 87 of Graduate Texts in Mathematics.

Springer-Verlag, New York-Berlin, 1982.

[11] Debojit Chanda, Thomas G. Mason, and Manas Khan. Orientational dynamics governs
the pathways of entropic crystallization of brownian squares. Preprint available from
https://doi.org/10.48550/arXiv.2405.07352.

[12] Ruth Charney. An introduction to right-angled Artin groups. Geom. Dedicata, 125:141–

158, 2007.

[13] Kenneth Deeley. Configuration spaces of thick particles on a metric graph. Algebr. Geom.

Topol., 11(4):1861–1892, 2011.

[14] Daniel Farley and Lucas Sabalka. Discrete Morse theory and graph braid groups. Algebr.

Geom. Topol., 5:1075–1109, 2005.

[15] Daniel Farley and Lucas Sabalka. Presentations of graph braid groups. Forum Math.,

24(4):827–859, 2012.

[16] Robin Forman. A discrete Morse theory for cell complexes.

In Geometry, topology,
& physics, Conf. Proc. Lecture Notes Geom. Topology, IV, pages 112–125. Int. Press,
Cambridge, MA, 1995.

[17] R. Fox and L. Neuwirth. The braid groups. Math. Scand., 10:119–126, 1962.

[18] Allen Hatcher. Algebraic topology. Cambridge University Press, Cambridge, 2002.

[19] Graham Higman, B. H. Neumann, and Hanna Neumann. Embedding theorems for groups.

J. London Math. Soc., 24:247–254, 1949.

[20] Ki Hyoung Ko and Hyo Won Park. Characteristics of graph braid groups. Discrete

Comput. Geom., 48(4):915–963, 2012.

[21] Rob Kusner, W¨oden Kusner, Jeffrey C. Lagarias, and Senya Shlosman. Configuration
spaces of equal spheres touching a given sphere: the twelve spheres problem. In New
trends in intuitive geometry, volume 27 of Bolyai Soc. Math. Stud., pages 219–277. J´anos
Bolyai Math. Soc., Budapest, 2018.

[22] Leonid Plachta. Geometric aspects of configuration spaces of thick particles in a rectangle.

Unpublished.

[23] Leonid Plachta. Configuration spaces of squares in a rectangle. Algebr. Geom. Topol.,

21(3):1445–1478, 2021.

[24] A. Varava, J.F. Carvalho, D. Kragic, and F.T. Pokorny. Free space of rigid objects:
caging, path non-existence, and narrow passage detection. The International Journal of
Robotics Research, 40:1049–1067, 2021.

18

Mathematics Department
Center for Research and Advanced Studies
Av. I.P.N n´umero 2508, San Pedro Zacatenco, Mexico City 07000, Mexico.
oalvarado@math.cinvestav.mx
jesus.glz-espino@cinvestav.mx and jesus@math.cinvestav.mx

19

