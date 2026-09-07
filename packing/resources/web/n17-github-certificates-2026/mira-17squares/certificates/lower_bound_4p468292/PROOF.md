# Proof interface for `s(17) > 4.468292`

Let `s(17)` be the least side length of a square containing 17 pairwise
interior-disjoint unit squares, with arbitrary orientations. This package
proves

\[
\boxed{s(17)>\frac{4\,468\,292}{1\,000\,000}=4.468292}.
\]

The proof exhibits 16 rational points and exactly certifies that every unit
square contained in `[0,4.468292]^2` contains at least one of them strictly in
its interior. Seventeen interior-disjoint squares would then require 17
distinct interior witnesses, which is impossible.

## 1. Pose coordinates and single-point leaves

A unit square is represented by its center `(x,y)` and

```text
t = tan(theta),  -1 <= t <= 1.
```

For a rational point `p=(px,py)`, put `dx=px-x` and `dy=py-y`. The point is
strictly inside the square exactly when

```text
4 (dx + t dy)^2   < 1 + t^2,
4 (-t dx + dy)^2 < 1 + t^2.
```

For a Cartesian pose box, the checker interval-bounds the two
linear-bilinear expressions over the whole box. It uses the minimum `|t|` in
the interval on the right-hand side. After clearing positive denominators,
every comparison is an exact integer comparison.

The axis-aligned half-extent of the square is

```text
h(t) = (1+|t|)/(2 sqrt(1+t^2)).
```

The same exact denominator-clearing method proves when an entire pose box is
infeasible because it violates containment in the outer square.

## 2. Strict triangle-piercing lemma

The certificate adds one exact leaf type implementing a strict form of a
classical square-piercing lemma.

**Lemma.** Let `A,B,C` be three points whose pairwise distances are all
strictly below 1. Every unit square whose center lies strictly inside triangle
`ABC` contains at least one of `A,B,C` strictly in its interior.

**Proof.** Put the square center at the origin and rotate coordinates so the
square is `[-1/2,1/2]^2`. Its two diagonals divide the plane into right, top,
left, and bottom closed cones. Because the origin is strictly inside triangle
`ABC`, the three vertices are not contained in either closed half-plane bounded
by either diagonal. Among the four cones this forces two vertices into opposite
cones. If neither of
those two vertices is in the square interior, then in the right/left case their
`x`-coordinates differ by at least 1, and in the top/bottom case their
`y`-coordinates differ by at least 1. Their Euclidean distance is therefore at
least 1, contradicting the strict side-length hypothesis. Thus one of the three
vertices is in the square interior. ∎

For a triangle leaf, the checker verifies exactly:

1. all three squared side lengths are `< 10^14`, since point coordinates have
   denominator `10^7`;
2. all four corners of the center rectangle satisfy the three strict oriented
   edge inequalities for the triangle.

The second condition puts the entire center rectangle strictly inside the
triangle, because each oriented-edge expression is affine and its minimum on a
rectangle occurs at a corner. The square orientation interval is irrelevant to
this leaf.

## 3. Certificate language

The certificate is a preorder tree with one byte per node:

```text
0       entire pose box is infeasible
1..16   the corresponding point covers the entire pose box
17      split the x interval at its exact midpoint
18      split the y interval at its exact midpoint
19      split the t interval at its exact midpoint
20..37  the corresponding fixed triangle pierces every pose in the box
```

The verifier starts with

```text
1/2 <= x,y <= 4.468292-1/2,  -1 <= t <= 1.
```

It rejects every false leaf, unknown opcode, early end of file, exhausted
dyadic grid, non-full binary tree, or trailing byte. Thus the accepted leaves
cover the complete pose space.

## 4. Packing consequence

Assign to each packed square one point certified to lie strictly in its
interior. Interior-disjoint squares cannot share an interior point, so this
would inject 17 squares into a 16-point set. Contradiction.

The feasible packing parameter space is compact and the containment and
non-overlap constraints are closed. Hence the optimum is attained. Since no
packing exists at side exactly `4.468292`, the strict bound follows.
