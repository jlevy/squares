Square Packing with Asymptotically Smallest Waste Only Needs Good
Squares

Hong Duc Bui

5
2
0
2

r
p
A
3
1

]

G
C
.
s
c
[

1
v
9
8
4
9
0
.
4
0
5
2
:
v
i
X
r
a

Abstract

We consider the problem of packing a large square with
nonoverlapping unit squares. Let W (x) be the mini-
mum wasted area when a large square of side length x
is packed with unit squares.
In Roth and Vaughan’s
article that proves the lower bound W (x) /∈ o(x1/2), a
good square is defined to be a square with inclination at
most 10−10 with respect to the large square. In this arti-
cle, we prove that in calculating the asymptotic growth
of the wasted space, it suffices to only consider packings
with only good squares. This allows the lower bound
proof in Roth and Vaughan’s article to be simplified by
not having to handle bad squares.

1

Introduction

There has been much research on the problem of packing
unit squares into a large square. Define W (x) to be the
minimum area of the wasted part when packing unit
squares into a large square of side length x. On one
hand, explicit constructions have been claimed in the
literature in [4, 1, 10, 2], which successively improves the
upper bound to W (x) ∈ O(x0.637), W (x) ∈ O(x0.631),
W (x) ∈ O(x0.625), W (x) ∈ O(x0.6) respectively. On
the other hand, [9] proves a lower bound that W (x) /∈
o(x0.5).

In the proof of the lower bound W (x) /∈ o(x0.5) in [9],
a good square was defined to be one with inclination
≤ 10−10 with respect to the large square. The proof of
[9, lemma 4] uses the fact that there isn’t too many bad
squares.

In this article, we prove that it suffices to only con-
sider the case where there are no bad squares, simpli-
fying the proof. Furthermore, if some stronger lower
bound is to be proven, the proof can make use of this
result to avoid having to handle bad squares.

The method used in this article can be generalized to
the case of packing a large quadrilateral with all angles
almost equal to a right angle.

More formally, let W ∗(x) be the smallest wasted area
when a large square of side length x is packed with only
good unit squares.
Theorem 1 W (x) ∈ Θ(W ∗(x)).

The main technical contribution of this article is
an application of the max-flow min-cut theorem to

this problem, and a generalization of the fundamental
lemma in [9] to handle squares far apart.

This article is organized as follows. In section 2, we
formally define the square packing problem and the var-
ious tools we use throughout the article. In section 3, we
prove a combinatorial tool that, given a set of marked
cells on a grid, bounds the total perimeter of rectangles
that contains all these cells in terms of the number of
disjoint paths from these marked cells to the boundary
on a grid.
In section 4, we generalize the fundamen-
tal lemma in [9] to handle squares arbitrarily far apart.
In section 5, we describe a surgery procedure that cuts
away all the bad cells in a packing, and show that the
additional wasted area is sufficiently small. In section 6,
we discuss some open problems that surface from our
work.

2 Notation

2.1 Notations Pertained to the Geometry of Square

Packing

We assume all squares live in an ambient Euclidean
plane R2 with a coordinate axis.

Let S0 be an axis-aligned large square of side length

x.

Definition 2 (Packing) Let S0 be fixed. A collection
of unit squares A = {S1, S2, . . . , Sk} is called a packing
of S0 if the unit squares Si are non-overlapping and
contained inside S0. Define |A| to be the number of
unit squares, so |A| = k.

From now on, S1, S2, . . . will be used to denote unit
squares in a packing. The notation Si is the same as in
[9].

Definition 3 (Si as a set of points) When Si
is
used as a set of points on the plane, we implicitly mean
the set of points on the boundary of the square. Here i
may either be 0 (S0 is the large square), or i > 0.

For i > 0, the set of points on the boundary and inside
i . The set of points on the

the square Si is denoted S∗
boundary and outside the square S0 is denoted S∗
0 .

With this definition, the intersection of S∗

i and S∗

j for

any 0 ≤ i < j ≤ |A| has area 0.

 
 
 
 
 
 
Definition 4 (Wasted area of a packing W (A))
Let W (A) = x2 − |A|, where as above, x is the side
length of S0.

Let us formally define the function W (x) mentioned

in the introduction.

Definition 5 (The waste function W (x)) Let A be
a packing with the largest number of unit squares for a
fixed value of the side length x. Then define the mini-
mum wasted area in packing a square of side length x to
be W (x) = W (A).

Equivalently, W (x) = minA W (A) over all packing A

of a square S0 with side length x.

Definition 6 (Wasted area in any shape) Fix the
large square S0 and a packing A. Let A be a measurable
set on the plane. Then define W (A) = |A \ (S∗
1 ∪
S∗
2 ∪ · · · ∪ S∗
k)|. In words, W (A) is the total area in A
that is inside the large square and not covered by any
unit squares.

0 ∪ S∗

Definition 7 (Angle between two squares) Let
Sa and Sb be squares (either an unit square used for
packing, or the boundary). We say Sa has the same
orientation as Sb if some edge of Sa is parallel to any
edge of Sb. Let θ(Sa, Sb) be the minimum rotation
angle in radian of one of the squares to have the same
orientation as the other. We allow either clockwise or
counterclockwise rotation.

Note that with our definition, θ(Sa, Sb) ≤ π

4 for every

a and b.

Definition 8 (Distance between two objects) Let
p, q be points in the plane and S, T be sets of points
in the plane. Define d(p, q) to be the distance from
p to q and d(S, T ) = mins∈S,t∈T d(s, t) whenever the
minimum exists. Define d(S, p) = d(S, {p}).

When both S and T are closed, and at least one of them
is compact, then d(S, T ) exists.

Definition 9 (The open ball around an object)
For a closed set S in the plane, define

B(S, r) = {point p | d(S, p) < r}.

Definition 10 (Path on a plane) We define a path
on the plane to be a continuous function γ : [a, b] → R2
for real numbers a < b.

Define the image of the path on the plane to be im γ =

{γ(x) | x ∈ [a, b]} ⊆ R2.

Following [9], we define the constant c = 10−10.
We also define a good square according to [9]:

Definition 11 (Good square and bad square)
A unit square Sa ∈ {S1, S2, . . . } is called good if
θ(S0, Sa) ≤ c. It is called bad if it is not good.

Definition 12 (Good packing, W ∗(x) function)
1, . . . , S′
A packing A′ = {S′
k} is called good if all
of the unit squares S′
k are good. Define
1,
W ∗(x) = minA′ W (A′) over all good packings A′ of the
large square S0 with side length x.

. . . , S′

The definition implies W ∗(x) ≥ W (x).

2.2 Notations Pertained to the Combinatorial Tools

Definition 13 (Grid, edge, neighborhood) Define
a n × m grid to be a grid consisting of n × m squares
(which we will call cells) glued side-by-side, such that
there are n rows and m columns. An edge of the grid
is defined to be an edge of any cell.

The neighborhood of a cell is defined to be the set of
cells that shares an edge with that cell. This is also
known in the literature as the 4-neighborhood or von
Neumann neighborhood of the cell. We also say the two
cells to be adjacent.

A cell is said to be on the boundary of the grid if it

has less than four adjacent cells.

See fig. 1 for an illustration. We see that the grid has
(n + 1) × m horizontal edges, n × (m + 1) vertical edges,
and n · m − max(0, n − 2) · max(0, m − 2) boundary cells.

Definition 14 (Rectangle on a grid) Consider
a
n × m grid. A rectangle on the grid is defined to be a
tuple of integers (i, i′, j, j′) such that 1 ≤ i ≤ i′ ≤ n,
1 ≤ j ≤ j′ ≤ n. The cells of that rectangle is defined
to be the set of all cells on row i∗ and column j∗ for
all integers i ≤ i∗ ≤ i′ and j ≤ j∗ ≤ j′. A cell is
contained in the rectangle if it belongs to the set of cells
of the rectangle as above. The cellular perimeter of the
rectangle is defined to be 2 · ((i′ − i + 1) + (j′ − j + 1));
equivalently, this is the number of grid edges that is on
the boundary of the rectangle.

See fig. 2 for an illustration.

We need to distinguish cellular perimeter and perime-
ter because later on there may be confusion if the side
length of each cell is not exactly 1 unit distance. When-
ever clear, we will just say perimeter.

Definition 15 (Bounding rectangle) For a non-
empty set of cells D in a grid, define its bounding rect-
angle to be the rectangle with smallest perimeter and
contains all the cells. It can be proven that this exists
and is unique.

Definition 16 (Path on a grid) Let A be a cell in a
grid. A path from A to the boundary is defined to be a
sequence of cells (P1, P2, . . . , Pk) such that P1 = A, Pk
is on the boundary of the grid, all Pi are different, and
for each integer 1 ≤ i < k, Pi and Pi+1 are adjacent.

Figure 1: Example of a 3 × 4 grid. Some edges are
colored in red, and a boundary cell is colored in blue.

Figure 2: Example of a rectangle on a grid. The rect-
angle is marked in red.

Figure 3: Visualization for the mapping in the proof of
lemma 18.

Definition 17 (8-connectivity of a set of cells)
Let D be a set of cells on a grid. We say a cell is in
the 8-neighborhood of another (different) cell if they
shares a vertex or an edge. We define a 8-connected
component of D to be an equivalence class of
the
equivalence relation generated by the relation “is in the
8-neighborhood of ”. D is said to be 8-connected if it
only has one 8-connected component.

3 Combinatorial Tools

We need some helpers to prove the theorem.

Lemma 18 Let D be a 8-connected set of cells on a
grid with k > 0 cells. Let R be its bounding rectangle.
Then the perimeter of R is no more than 4k.

Proof. Let E be the edges of the grid that forms the
boundary of R. Then the number of edges in E is equal
to the perimeter of R.

Let F be the edges of the cells that forms D, including
duplicates by double-counting edges that belong to two
cells in D. We have |F | = 4k.

We will provide a injective mapping from E to F as

follows.

Consider the edges in E that is on top of R. We
gradually move each of them downwards until they hit
a cell in D. Wherever the edge ends up at, it must
belong to F . So we map the original edge in E to this
edge. See fig. 3 for an illustration.

Perform a similar procedure for the edges in E that is
on the other three sides of R. Because D is 8-connected,
every row and every column has at least one cell in D,
so each edge ends up somewhere instead of moving to
infinity.

Figure 4:
Illustration of merging two rectangles that
have at least a point in common. Here, they have a grid
edge in common, and the total perimeter decreases by
2 after merging.

It is then easy to see that the constructed mapping is
injective. Therefore |E| ≤ |F |, combining with |F | = 4k
□
we’re done.

Observation 1 An alternative way to prove lemma 18
is the following: we start with k separate rectangles
(each covering a cell in D) with perimeter 4 each, then
repeatedly merge the rectangles that have at least a point
in common, noticing that the total perimeter is non-
increasing during the process. Because of 8-connectivity,
the final result must be the bounding rectangle R. See
fig. 4 for an illustration.

Proposition 19 Let M be a collection of cells on a n×
m grid, which we call the marked cells. Then there
exists an integer f ≥ 0 such that:

• For each integer 1 ≤ i ≤ f ,

there is a path
Pi = (Pi,1, Pi,2, . . . , Pi,ki) from a marked cell to the
boundary (that is, Pi,1 ∈ M is marked and Pi,ki is
on the boundary);

• Each cell is used in at most one path.

In other
words, there is no (i, j, i′, j′) such that Pi,j = Pi′,j′
but (i, j) ̸= (i′, j′).

• There is a collection of rectangles {R1, . . . , Rk} of
the grid such that all marked cells is contained in
some rectangle, and their total perimeter is ≤ 4f .

If we compare this with [9], the arguments in the proof
of [9, Lemma 4] can show that the cells in M appears
in either ≥ (cid:112)|M | distinct rows or ≥ (cid:112)|M | distinct
columns, because otherwise there would be less than
(cid:112)|M | · (cid:112)|M | locations which marked cells can be at,
which is a contradiction. This implies by taking the
trivial vertical or horizontal paths along the rows or
columns containing a marked cell, we get f ≥ (cid:112)|M |
distinct paths. Our proof is stronger in that it can relate
the value of f with the total perimeter of the bounding
rectangles.

Proof. We make use of the max-flow min-cut theorem.
This is a very well-known theorem, one proof can be
found in [6].

Construct the flow graph as follows.

For each 1 ≤ i ≤ n and 1 ≤ j ≤ m, construct node
Ai,j and Bi,j. Each cell on row i and column j corre-
sponds to two nodes Ai,j and Bi,j, which we will call
the A-node and B-node of the cell respectively. Besides,
there are source node s and sink node t.

For each cell, connect its A-node to its B-node with

a (directed) edge with capacity 1.

For each cell on the boundary, connect its B-node to

the sink t with an edge with capacity ∞.

For each marked cell, connect the source s to the cell’s

A-node with an edge with capacity ∞.

For each pair of adjacent cells (i, j) and (i′, j′), con-

nect Bi,j to Ai′,j′ with an edge with capacity ∞.

Note that when all edges with capacity < ∞ are re-
moved, there is no path from s to t, therefore the flow
is finite. Since all edge weights are integers, the flow is
an integer, let this be f . Furthermore, there exists a
maximum flow where the amount of flow through each
edge is an integer.

If an algorithm such as Ford-Fulkerson is used to com-
pute the flow, because all edge weights are integral, the
flow value through each edge is also integral. Therefore,
the flow can be decomposed into f unit flows from s
to t, each has weight 1. By taking the cells that corre-
sponds to the edges with capacity 1 along each path, we
get a collection of paths Pi = (Pi,1, . . . , Pi,ki) for each
1 ≤ i ≤ f . By construction, this is a path from Pi,1
(which is a marked cell) to the boundary.

Because each edge from a cell’s A-node to its B-node
has capacity 1, each cell is used in at most one of the
paths Pi, and each path only consist of distinct cells.

From the procedure above, we have constructed a col-
lection of paths {Pi} as required. Now we need to con-
struct the collection of rectangles {Ri}.

By the max-flow min-cut theorem, there is a collec-
tion of edges with total capacity f such that cutting
these edges results in no path from the source s to the
sink t. Because each edge with finite capacity has ca-
pacity 1, there must be f edges being cut; furthermore
each of them connects some cell’s A-node to its B-node.
Let the set of cells corresponding to these cut edges be
C.

Because the edges corresponding to the cells in C is
a cut, for each marked cell, there is no path from that
cell to the boundary that does not contain any cell in
C.

Divide C into 8-connected components, say D1, . . . ,
Dk. For each i, let rectangle Ri be the bounding rect-
angle of Di. Applying lemma 18, the total perimeter of
Ri is no more than 4 (cid:80)k
□

i=1 |Di| = 4f .

Observation 2 This is known as the vertex splitting
technique, which is also described in [7, 5]. It is also
well-known within competitive programming communi-
ties, one reference can be found in [8, Section 8.4.5].

Figure 5: Illustration for proposition 21 (drawing not to
scale, r = 5 in this article).

Constructed as is, the rectangles may have intersec-
tions. The merging procedure described in observation 1
can be used to create a collection of disjoint rectangles,
but this is not needed in the places proposition 19 is
used.

4 Geometric Tools

We make use of the fundamental lemma in [9], which
we copy below.

Lemma 20 Let Sa be a unit square used in the packing,
and Sb either the boundary of the shape being packed or
another unit square. If the distance from Sa to Sb is at
most 1, then there is an open disk of radius 2 containing
Sa such that the area of wasted space in the open disk
is at least c · θ(Sa, Sb).

In short:

Difference in angle leads to wasted space.

Lemma 20 only works for squares that are sufficiently

close, however. We want to generalize it as follows.

Proposition 21 Let Sa and Sb be squares, γ : [0, l] →
R2 be a path on the plane connecting Sa and Sb. Then
there is a constant r > 0 and c′ > 0 such that
W (B(im γ, r)) ≥ c′ · θ(Sa, Sb).

Recall W (−) is the wasted area as defined in defini-
tion 6.

Intuitively, we can imagine drawing a path γ from a
to b, then the statement says that if there is an angle
difference θ(Sa, Sb) between Sa and Sb, the total wasted
area inside the region colored green is at least propor-
tional to θ(Sa, Sb). See fig. 5 for an illustration.

Observation 3 The vertical strip Ti in [9, Lemma 6]
or the vertical line segment L(X) in [9, Lemma 4] is
very similar to a vertical path γ as we use here. Our
proof can be seen as a generalization of the argument
there.

The main idea is the following. Lemma 20 gives us
circles that contains large wasted area. Then we find a

wasted area ≥ c·θ(Sij , Sij+1). Let p be the center of this
disk, so the disk is B(p, 2), and let k ∈ {ij, ij+1} be the
index such that Sk ⊆ B(p, 2). Then d(γ(xj), Sk) < 3
4 , so
d(γ(xj), p) ≤ 2 + 3
4 , so B(p, 2) ⊆ B(γ(xj), 5), therefore
W (B(γ(xj), 5)) ≥ c · θ(Sij , Sij+1).

Taking the sum, we get

n−1
(cid:88)

j=1

W (B(γ(xj), 5)) ≥ c ·

n−1
(cid:88)

j=1

θ(Sij , Sij+1)

≥ c · θ(Si1, Sin) = c · θ(Sa, Sb).

Since for each 1 ≤ j < k < n, d(xj, xk) ≥ 1

2 , for each
point p on the plane, there can be at most 1600 such
points xj in B(p, 5), therefore

(cid:16) n−1
(cid:91)

W

j=1

B(γ(xj), 5)

(cid:17)

≥

c
1600

· θ(Sa, Sb).

This gives the desired conclusion.

□

5 Main Results

Now we return to the square packing problem. Recall
x is the side length of the large square S0.

Proposition 22 There exists a constant c2 > 1 inde-
pendent of x such that: for all packing A, there exists a
good packing A′ such that W (A′) ≤ c2W (A).

Proof. If x ≤ 1, the statement is obvious. We assume
x > 1.

Divide the large square into ⌈x⌉ rows and that many
columns, we get a ⌈x⌉ × ⌈x⌉ grid, each cell is a square
with side length > 1

2 and ≤ 1.

Let the set of marked cells M be the set of cells
that has any (positive area) overlap with a bad square.
Apply proposition 19 on this set M , we get an inte-
ger f ≥ 0, and a collection of paths {Pi}1≤i≤f , where
Pi = (Pi,1, . . . , Pi,ki ). Let Oi,j be the center of cell
Pi,j, and let path γi be the polyline consisting of the
shortest segment from any bad square that has an
overlap with cell Pi,1 to Oi,1, followed by the polyline
Oi,1Oi,2Oi,3 . . . Oi,ki, followed by the shortest segment
from Oi,ki to the boundary of S0.

Apply proposition 21 on each of the path γi, we get

(where c′ and r are as in proposition 21)

f
(cid:88)

i=1

W (B(im γi, r)) ≥ c′ · c · f.

Because each cell Pi,j is only used once and the side
length of each cell is between 1
2 and 1, each point in
(cid:83)f
i=1 B(im γi, r) is covered by Θ(1) of the B(im γi, r),

Figure 6: Illustration for the construction of circles.

sequence of squares (Sj0 = Sa, Sj1, Sj2, . . . , Sjk−1 , Sjk =
Sb) along and near the path, apply lemma 20 on each
consecutive pair (Sji, Sji+1), and get a collection of cir-
cles whose center is roughly along the path γ. See fig. 6
for an illustration.

To prove the total wasted area in the union of the
circles is sufficiently large, we also need that each point
is contained in O(1) circles.

Proof. If there exists any 0 ≤ x ≤ l such that
W (B(γ(x), 1
4 )) ≥ c · θ(Sa, Sb), we are done.
Suppose otherwise. Construct a sequence of real num-
bers {xi} as follows:
let x1 = 0, and for each integer
i ≥ 2, xi is defined to be the largest value of x such
that xi ≥ xi−1 and d(γ(xi−1), γ(xi)) ≤ 1
2 . Because the
domain of γ is compact and γ is continuous, this exists.
Let n be the smallest index such that xn = l, if such

index exists. Otherwise let n = ∞.

For all 1 ≤ j < k < n, d(xj, xk) ≥ 1

2 . Since im γ is
compact, it is bounded. We see n < ∞ by an application
of the pigeonhole principle: say im γ is inside a square of
side length R, divide it into ⌈4R⌉2 small squares of side
length ≤ 1
4 , then no two points (xj, xk) for 1 ≤ j < k <
n can be in the same square, therefore n ≤ ⌈4R⌉2 + 1.
For each 1 ≤ j ≤ n, define index ij ≥ 0 such that
If there are multiple such indices,

d(γ(xj), S∗
ij
pick any; with the exception of i1 = a and in = b.

) < 1
4 .

We show such ij exists: Since we assume for all 0 ≤
x ≤ l then W (B(γ(x), 1
π, there is
at least one square with nonzero intersection area with
B(γ(x), 1

4 )) < c · θ(Sa, Sb) < 1

4

2

4 ).

Next, for each 1 ≤ j < n,

d(S∗
ij

, S∗

ij+1

) ≤ d(S∗
ij

, γ(xj)) + d(γ(xj), γ(xj+1))

)

+ d(γ(xj+1), S∗
1
4

1
2

+

+

ij+1

<

1
4
= 1.

Therefore d(Sij , Sij+1) < 1.

If θ(Sij , Sij+1) = 0 then W (B(γ(xj), 5)) ≥ 0 = c ·
θ(Sij , Sij+1). Otherwise, at least one of Sij or Sij+1 is
an unit square, apply lemma 20, there is an open disk
with radius 2 containing either Sij or Sij+1 and have

therefore

6.3 Other Algorithmic Considerations

W (A) ≥ W

(cid:16)

f
(cid:91)

i=1

B(im γi, r)

(cid:17)

W (B(im γi, r))

≥

≥

1
Θ(1)

f
(cid:88)

i=1

c′ · c · f
Θ(1)

.

From the application of proposition 19 above, we also
get a collection of rectangles {R1, . . . , Rk} that contains
all the marked cells. Use these rectangles, modify A into
A′ as follows. First, delete all unit squares completely
contained in (cid:83)
i Ri, this way all bad squares are deleted.
Then, pack as many axis-aligned unit squares with in-
tegral vertex coordinates as possible.

Note that this packing procedure can only create

wasted space along the perimeter of Ri.

Because the side length of each cell is between 1
2 and
1, for each rectangle Ri, its perimeter is between 1
2 and
1 times its cellular perimeter. We know from proposi-
tion 19 that the total cellular perimeter of Ri is ∈ O(f ),
so the total perimeter of Ri is also ∈ O(f ).

Therefore the additional wasted area introduced by
the modification procedure is ∈ O(f ), so W (A′) ≤
W (A) + O(f ). Since W (A) ∈ Ω(f ), we get the desired
□
result.

Now we can prove theorem 1.

Proof. As mentioned after definition 12, W (x) ≤
□
W ∗(x). Proposition 22 implies W ∗(x) ≤ c2W (x).

6 Discussion

6.1 Generalization of the Wasted Area Along Path

Proposition

The construction in proposition 19 can be explicitly im-
plemented. In doing so, notice that the amount of flow
through each edge is either 0 or 1, therefore the max-
imum flow can also be found if the edges with capac-
ity ∞ are set to have capacity 1 instead. If the Dinic
algorithm is used to compute the flow, the constructed
flow graph has O(nm) vertices and O(nm) edges, there-
fore the time complexity is O((nm)3/2) according to [5,
Theorem 1]. Alternatively, because the flow value is
O(n + m), the simpler Edmonds–Karp algorithm [3] or
any implementation of the Ford–Fulkerson method [6]
would have time complexity O(nm(n + m)).

A simpler algorithm to find disjoint paths in propo-
sition 19 is to perform multi-source BFS from marked
cells to the boundary, greedily pick the shortest path
found each time, while avoiding cells that already be-
long to some path. Let f ′ be the number of disjoint
paths found by this method, then f ′ ≤ f . While this
method does not provide any guarantee of optimality
(it may happen that there is no collection of rectan-
gles with total perimeter ≤ 4f ′ covering all the marked
cells, see section 7.1), numerical experiments suggests
the conjecture f ′ ∈ Ω(f ). We find this likely because of
the special structure of the grid.

In implementing the merging procedure described in
observation 1, because the perimeter of each rectangle
is at most 2(n + m), and the perimeter increases by at
least 2 after a merge step with another rectangle that is
not completely contained inside, the merging procedure
terminates after at most n+m iterations. Each iteration
can be implemented in O(nm), therefore the total time
complexity is O(nm(n + m)).

It would be interesting to investigate whether there
is any algorithm taking less than cubic time for each of
the problems above when n ∈ Ω(m).

How small can r be in proposition 21? We guess that r
can be made arbitrarily small.

7 Conclusion

Conjecture 1 Let Sa and Sb be squares. Let γ : [0, l] →
R2 be a path on the plane connecting Sa and Sb. Then
there is a constant c′ > 0 such that for all r > 0,
W (B(im γ, r)) ≥ c′ · min(1, r2) · θ(Sa, Sb).

To prove this would require proving a stronger version

of lemma 20, however.

6.2 Strengthening of the Result

We have shown that only good squares (i.e.
squares
with tilt bounded by a constant) need to be considered
to compute the asymptotic growth of the wasted area.
Nonetheless, the tilt in the proposed packing methods
[4, 1, 10] is in fact much smaller, O(x−ϵ) for some ϵ >
0. Can the bound on the tilt be sharper, for example
O(1/ log x) or even O(x−ϵ) for some ϵ > 0?

We prove a relation between arbitrary packing and good
packing of a large square, therefore anyone proving a
lower bound on W (x) in the future similar to [9] only
need to consider good packings.

Acknowledgements

The author would like to thank some friends for insight-
ful discussion and finding some typos.

References

[1] F. Chung and R. Graham. Packing equal squares into a
large square. Journal of Combinatorial Theory, Series
A, 116(6):1167–1175, Aug. 2009.

[2] F. Chung and R. Graham. Efficient packings of unit
squares in a large square. Discrete & Computational
Geometry, 64(3):690–699, Apr. 2019.

[3] J. Edmonds and R. M. Karp. Theoretical improve-
ments in algorithmic efficiency for network flow prob-
lems. Journal of the ACM, 19(2):248–264, Apr. 1972.

[4] P. Erd¨os and R. Graham. On packing squares with
equal squares. Journal of Combinatorial Theory, Series
A, 19(1):119–123, 1975.

[5] S. Even and R. E. Tarjan. Network flow and test-
ing graph connectivity. SIAM Journal on Computing,
4(4):507–518, Dec. 1975.

[6] L. R. Ford and D. R. Fulkerson. Maximal flow through a
network. Canadian Journal of Mathematics, 8:399–404,
1956.

[7] L. R. Ford and D. R. Fulkerson. Flows in Networks.

Princeton University Press, Dec. 1963.

[8] S. Halim, F. Halim, and S. Effendy. Competitive pro-
gramming 4: The new lower bound of programming con-
tests in the 2020s. Lulu Press, 2018.

[9] K. Roth and R. Vaughan.

Inefficiency in packing
squares with unit squares. Journal of Combinatorial
Theory, Series A, 24, 3 1978.

[10] S. Wang, T. Dong, and J. Li. A new result on packing

unit squares into a large square, 2016.

Appendix

7.1 Example Grid where Greedy Multi-source BFS

Gives Suboptimal Result

Consider the grid depicted in fig. 7, where the marked
cells are colored green or blue. Multi-source BFS al-
gorithm would first greedily find the paths to the blue
cells, then it would not be able to find any additional
paths to the green cells. However, if the 8 paths marked
red are removed to create paths to the green cells first,
more cells would be created.
It can be seen that in
this case greedy BFS algorithm finds f ′ = 24 disjoint
paths, but there is no collection of rectangles with total
perimeter 4f ′ = 96 covering all the marked cells.

Figure 7: Example grid where greedy multi-source BFS
algorithm gives f ′ disjoint paths and 4f ′ is less than the
minimum total perimeter of bounding rectangles.

