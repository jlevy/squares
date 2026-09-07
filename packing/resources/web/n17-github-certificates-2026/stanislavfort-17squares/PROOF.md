# Proof interface

This note states the mathematics that the certificate checkers verify. It is
intended to make the repository independently auditable without requiring the
search procedure that found the points.

## 1. Pose parameterization

A unit square is represented by its center `(x,y)` and orientation `theta`.
Because a square is invariant under rotation by `pi/2`, it suffices to use

```text
t = tan(theta),   -1 <= t <= 1.
```

Let

```text
c = 1/sqrt(1+t^2),   s = t/sqrt(1+t^2).
```

For a point `p=(px,py)` write `dx=px-x`, `dy=py-y`. The point lies strictly
inside the unit square exactly when both square-frame coordinates have absolute
value below `1/2`:

```text
4 (dx + t dy)^2       < 1 + t^2,
4 (-t dx + dy)^2      < 1 + t^2.
```

These are the two strict witness inequalities checked by the certificate.

## 2. Containment in the outer square

For `|t| <= 1`, the axis-aligned half-extent of a rotated unit square is

```text
h(t) = (1 + |t|) / (2 sqrt(1+t^2)).
```

A pose `(x,y,t)` is contained in `[0,L]^2` only if

```text
h(t) <= x <= L-h(t),
h(t) <= y <= L-h(t).
```

The certificate works over the initial center box

```text
1/2 <= x,y <= L-1/2,   -1 <= t <= 1
```

and permits an `infeasible` leaf only when exact arithmetic proves that the
entire pose box violates at least one containment requirement.

For a `t` interval, `h(t)` is increasing in `|t|` on `[0,1]`. Thus the minimum
half-extent over the interval occurs at the minimum `|t|`; clearing positive
denominators gives the exact integer inequality used by all checkers.

## 3. Witness leaves

A pose-space box is a Cartesian product of intervals in `x`, `y`, and `t`.
For a fixed rational witness point, the checker interval-bounds

```text
dx + t dy
-t dx + dy
```

over the whole box. The bilinear products attain their extrema at interval
corners, so the bounds are rigorous.

For the right-hand side `1+t^2`, the checker uses the minimum `|t|` in the
`t` interval. Therefore a witness leaf is accepted only if the two *strict*
interior inequalities hold for every pose in that complete box.

All comparisons are performed after exact denominator clearing with integers.

## 4. Tree semantics

The certificate is a preorder encoding with one byte per node:

```text
0       entire box is infeasible
1..16   corresponding rational point covers the entire box
17      split x at the exact midpoint
18      split y at the exact midpoint
19      split t at the exact midpoint
```

Starting from the complete pose box, a split replaces a box with its two closed
midpoint children. Their union is the parent. Consequently, if every leaf is
valid, every feasible pose is covered by at least one of the 16 points.

The verifiers also reject early EOF, unknown opcodes, exhausted dyadic grids,
non-full trees, and trailing data.

## 5. From piercing to packing

Suppose 17 pairwise interior-disjoint unit squares were contained in the outer
square. The certificate says that each one contains at least one of the 16
witness points *strictly in its interior*. Two interior-disjoint squares cannot
share the same interior witness. Hence 17 such squares would require at least
17 distinct witness points, contradiction.

Therefore no packing exists at

```text
L = 4456575/1000000 = 4.456575.
```

Finally, the feasible packing parameter space can be taken compact and the
non-overlap/containment constraints are closed, so if a packing existed with
infimum exactly `L`, a minimizing packing would exist at `L`. Since the
certificate excludes one there,

```text
s(17) > 4.456575.
```
