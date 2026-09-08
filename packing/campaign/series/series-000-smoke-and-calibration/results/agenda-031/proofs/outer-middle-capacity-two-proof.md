# Outer-Middle Segment Capacity Is Two

Date: 2026-09-08. Status: analytic proof, independently reviewed.
Scope: local ownership capacity; no new packing bound.

Let `q = 96/25`, `δ = 3/500`, and

```text
M = [49/100, 59/100] × {48/25}.
```

Among closed unit squares contained in `[0,q]²` with pairwise disjoint interiors, at
most two have distance at most `δ` from `M`. Two is attained.

The proof establishes a stronger statement for a half-plane.
Its fixed piercing points are rational, so they can also classify ownership branches.

## Two Interior Piercing Points Near a Wall

Set

```text
b = 3/5,     a = 9/10,     z = 7/25,
δ = 3/500,   ε = 3/200,    ρ = 1/1000,
p₋ = (a,-z), p₊ = (a,z).
```

**Lemma.** Every closed unit square `Q ⊂ {x ≥ 0}` meeting `[0,b] × [-δ,δ]` contains `p₋`
or `p₊` in its interior.
At the vertical line `x=a`, the selected point has vertical clearance at least `ε` from
both ends of the chord `Q ∩ {x=a}`. The closed radius-`ρ` disk about that point is
contained in `Q`.

Orientations are taken modulo a quarter turn.
Reflection in `y=0` preserves the half-plane, the rectangle, and the pair of piercing
points. Thus it suffices to use `0 ≤ θ ≤ π/4`. Write `c=cos θ`, `s=sin θ`, so `c≥s≥0`,
and let `g≥0` be the least x-coordinate of the square.
Since the square meets the rectangle, `g≤b`. For some real `h`, its vertices, starting
at the bottom vertex, are

```text
(g+s,h), (g+s+c,h+s), (g+c,h+s+c), (g,h+c).
```

The relative coordinate `X=a-g` lies in `[a-b,a]=[3/10,9/10]` and strictly between `0`
and `c+s`, because `a<1≤c+s`. Thus `x=a` cuts through the horizontal interior of the
square.

Assume first `s>0`. At relative x-coordinate `X`, the lower and upper ordinates, after
subtracting `h`, are

```text
 l(X) = (c/s)(s-X)                 for 0 ≤ X ≤ s,
        (s/c)(X-s)                 for s ≤ X ≤ c+s;

 u(X) = c+(s/c)X                   for 0 ≤ X ≤ c,
        c+s-(c/s)(X-c)             for c ≤ X ≤ c+s.
```

Write `l=l(a-g)` and `u=u(a-g)`. The minimum and maximum ordinates of the part of the
square in `x≤b`, again subtracting `h`, are

```text
L = max(0, (c/s)(g+s-b)),
U = c+(s/c)(b-g).
```

The formula for `U` uses `b-g≤b<c`, which holds because `c≥1/√2>3/5`. The truncated
square is convex, so its y-projection is the whole interval `[h+L,h+U]`. Meeting the
rectangle therefore gives

```text
-δ-U ≤ h ≤ δ-L.                                      (1)
```

Three estimates suffice:

```text
u-l ≥ 3/5,
l-L < 9/35,
U-u < 1/4.                                          (2)
```

### Chord length

The chord length at relative coordinate `X` is

```text
u(X)-l(X) = X/(sc)                 for 0 ≤ X ≤ s,
           1/c                    for s ≤ X ≤ c,
           (c+s-X)/(sc)            for c ≤ X ≤ c+s.
```

This function is concave, so its minimum on `[3/10,9/10]` is at an endpoint.
At `X=3/10`, either the length is `1/c≥1` or it is `(3/10)/(sc)≥3/5`, using `sc≤1/2`. At
`X=9/10`, either the length is `1/c≥1` or

```text
(c+s-9/10)/(sc) > (c+s-1)/(sc)
                       = 2/(c+s+1)
                       ≥ 2/(√2+1)
                       > 3/5.
```

Hence `u-l≥3/5`.

### Lower endpoint displacement

For fixed `s`, the quantity `l-L` is nonincreasing in `g`. This follows directly by
splitting at `g+s=b` and `g+s=a`: its formulas are respectively

```text
(s/c)(a-g-s),
(s/c)(a-g-s)-(c/s)(g+s-b),
(c/s)(b-a).
```

The formulas agree at their boundaries; the first two decrease and the last is constant.
It is therefore enough to set `g=0`.

If `0<s≤b`, then `c≥4/5` and

```text
l-L = s(a-s)/c ≤ a²/(4c) ≤ 5a²/16 = 81/320 < 9/35.
```

If `b<s≤1/√2`, then `s<a` and `c>7/10`. Discarding the nonnegative term `L` gives

```text
l-L ≤ s(a-s)/c < (10/7)b(a-b) = 9/35.
```

Here the numerator estimate follows from

```text
s(a-s)-b(a-b) = (s-b)(a-s-b) ≤ 0,
```

because `s≥b` and `a<2b`. Thus `l-L<9/35` in every case.

### Upper endpoint displacement

If `a-g≤c`, the formulas give `U-u=(s/c)(b-a)<0`. If `a-g≥c`, the expression is
decreasing in `g`, so it is at most its value at zero:

```text
U-u ≤ (ac-1)/s + b s/c
     ≤ (c-1)/s + (3/5)s/c
      = -s/(1+c) + (3/5)s/c
     ≤ s((3/5)/c-1/2)
     ≤ (1/√2)((3/5)√2-1/2)
      = 3/5-1/(2√2)
      < 1/4.
```

The penultimate inequality uses `s≤1/√2`, `c≥1/√2`, and the nonnegativity of the
bracket. The final inequality follows from `√2>7/5`.

### Interior, orientation endpoints, and equality cases

The vertical clearance requirement for `(a,±z)` is equivalent to membership of `h` in
the corresponding closed interval

```text
I₋ = [-z-u+ε, -z-l-ε],
I₊ = [ z-u+ε,  z-l-ε].
```

These intervals overlap because

```text
u-l ≥ 3/5 > 2z+2ε = 59/100.
```

Their union contains the whole interval in (1), because

```text
l-L+δ+ε < 9/35+3/500+3/200 = 1947/7000 < 7/25,
U-u+δ+ε < 1/4+3/500+3/200 = 271/1000 < 7/25.
```

Thus at least one piercing point lies on the chord at vertical distance at least `ε`
from each endpoint.
Since `x=a` lies strictly between the square’s extreme x-coordinates,
that point belongs to `int(Q)`.

For `θ=0`, the square is `[g,g+1]×[h,h+1]`, with `0≤g≤b`. Here `x=a` is strictly between
its vertical sides, `l=L=0`, and `u=U=1`. The same interval argument applies directly
without dividing by `s`. For `θ=π/4`, all denominators in the preceding formulas are
positive, the middle interval of the chord formula has length zero, and the formulas
agree at its endpoint.
Thus this endpoint is included.
Every boundary intersection with the target rectangle and every equality in the square
containment hypothesis is retained.
The conclusion is still interior containment because the displayed margins are strict.

### Euclidean disk clearance

Write the selected piercing point as

```text
p = (g+s,h) + λ(c,s) + μ(-s,c),   0<λ,μ<1.
```

The four distances from `p` to the square’s edge lines are `λ`, `1-λ`, `μ`, and `1-μ`.
Since both `p±ε(0,1)` belong to `Q`,

```text
λ, 1-λ ≥ εs,    μ, 1-μ ≥ εc.
```

If `s≥1/15`, these are all at least `ρ=1/1000`, using `ε=3/200` and `c≥s`. If `s≤1/15`,
the horizontal margins give

```text
a-g = cλ+s(1-μ) ≥ a-b = 3/10,
g+c+s-a = c(1-λ)+sμ ≥ 1-a = 1/10.
```

Because `0≤μ≤1` and `c≤1`, it follows that

```text
λ ≥ (3/10-s)/c ≥ 7/30,
1-λ ≥ (1/10-s)/c ≥ 1/30.
```

The other two distances are at least `εc≥ε/√2>ρ`. Thus all four edge-line distances are
at least `ρ`, and the closed radius-`ρ` disk is contained in `Q`. This reasoning also
covers `s=0`. ∎

## E.4 Ownership Corollary and Sharpness

If `dist(Q,M)≤δ`, compactness supplies `p∈Q` and `r∈M` with `|p-r|≤δ`. After translating
`y` by `-48/25`,

```text
0 ≤ p_x ≤ 59/100+3/500 = 149/250 < 3/5,
|p_y| ≤ 3/500.
```

The lemma applies. Every owner of the left outer-middle segment contains, in its
interior, at least one of

```text
(9/10, 41/25), (9/10, 11/5).
```

No two squares of a packing can contain the same point in their interiors.
Hence at most two squares own that segment.
Reflection in `x=q/2` proves the same bound for the right outer-middle segment, using

```text
(147/50, 41/25), (147/50, 11/5).
```

Two owners exist on the left:

```text
Q₁ = [0,1] × [23/25,48/25],
Q₂ = [0,1] × [48/25,73/25].
```

Both are contained in `[0,96/25]²`, their interiors are disjoint, and both contain the
entire segment `M` on their common boundary.
Their reflections give the right-hand witness.
Thus the capacity two is sharp, including the permitted touching case.

## Consequence for the Next Branch Constraint

The two outer-middle E.4 labels each have capacity two.
Every one of the other eight labels has capacity four, and four is attained there by the
four axis-aligned unit squares with a common vertex at the segment midpoint.
Those eight midpoints have both coordinates in `[1,q-1]`, so all four squares are
contained.

For an outer-middle label with two assigned owners, the two owners must occupy different
piercing-point classes.
An owner containing both piercing points excludes every other owner of that label.
This gives an explicit geometric disjunction in addition to the capacity inequality.

Let `v` be any unit separating normal ordered from the owner of the lower piercing point
to the owner of the upper point.
Their radius-`ρ` disks and shared ownership of the horizontal segment give

```text
v_y ≥ 1/280,
56 v_y ≥ 62|v_x|-1.
```

For the first inequality, the difference of the piercing points is `(0,14/25)` and its
projection must be at least `2ρ`. For the second, the piercing points have offsets
`(9/25,±7/25)` from the left segment midpoint, and the shared-support radius is
`r_v=|v_x|/20+3/500`. Thus

```text
(9/25)v_x-(7/25)v_y ≤ r_v-ρ,
(9/25)v_x+(7/25)v_y ≥ -r_v+ρ.
```

Combining them yields `(7/25)v_y≥(31/100)|v_x|-1/200`. The right reflection changes the
sign of both x-offsets, leaving the final inequalities unchanged.
These cuts retain weak separation and touching.
The two-point lemma supplies no nonexistence statement for eleven-square packings by
itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
