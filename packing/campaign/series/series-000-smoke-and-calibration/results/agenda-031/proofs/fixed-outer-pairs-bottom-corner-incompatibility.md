# Fixed Outer Pairs Exclude Two Distinct Bottom Corner Owners

Date: 2026-09-08. Status: analytic proof.
This result concerns the specified fixed outer squares and the two bottom corner marks.
It makes no claim about other outer placements or eleven-square packings.

Put

```text
q = 96/25,   h = 23/25,   q = 2+2h,
a = 3152/3175,   b = 2336/3175,
d = 1-a = 23/3175,
e = h-b = 117/635,
P = (1+h,b) = (48/25,b).
```

**Theorem.** Two additional unit squares with disjoint interiors cannot contain `(a,b)`
and `(q-a,b)`, respectively, while both are contained in `[0,q]²` and have disjoint
interiors from the fixed lower outer squares

```text
A_L = [0,1] × [h,h+1],
A_R = [q-1,q] × [h,h+1].
```

Consequently the requested six-square partial configuration, which also includes the two
fixed upper outer squares, is impossible.
Containment of a mark in its selected nearest-net `B`-core is stronger than the mark
containment used here.

## A Common Interior Point

We prove that any closed unit square `C` contained in `{x≥0,y≥0}`, containing `m=(a,b)`,
and having disjoint interior from `A_L`, must contain `P` in its interior.

Choose a unit weak separating normal `v` directed from `A_L` toward `C`:

```text
max_{x∈A_L} v·x ≤ min_{x∈C} v·x.
```

Because `0<a<1` and `b<h`, a normal with `v_y≥0` would have `v·m<max_{A_L}v·x`,
contradicting `m∈C`. Thus `v_y<0`. If `v_x≤0`, the displayed separation and `x≥0` on `C`
would imply `y≤h` throughout `C`. This is impossible: a unit square has vertical span at
least one, whereas `C⊂{0≤y≤h}` would have span at most `h<1`. Hence `v_x>0`.

The separating-axis theorem allows the normal to be chosen among the side normals of the
two squares. The strict sign conditions exclude the axis-aligned normals of `A_L`;
therefore it is a side normal of `C`. Write

```text
n = (p,-r),   w = (r,p),
p>0,   r>0,   p²+r²=1.
```

The vectors `n,w` are orthonormal side normals of `C`. For some `k,l`, its support
coordinates describe it exactly as

```text
C = {x : k≤n·x≤k+1,  l≤w·x≤l+1}.
```

Let the coordinates of the mark in these unit intervals be

```text
α = n·m-k ∈ [0,1],   β = w·m-l ∈ [0,1].
```

Separation gives `k≥p-rh`, so

```text
α ≤ p(a-1)+r(h-b) = -pd+re.                           (1)
```

The square’s lowest vertex has y-coordinate `b-r(1-α)-pβ`. Bottom containment therefore
gives

```text
pβ ≤ b-r+rα.                                         (2)
```

Since `P=m+(h+d,0)`, its local support coordinates are

```text
α_P = α+p(h+d),   β_P = β+r(h+d).
```

Both are strictly positive, because `p,r,h+d>0` and `α,β≥0`. For their upper bounds, (1)
gives

```text
α_P ≤ hp+er ≤ sqrt(h²+e²) < 1.
```

The last inequality is exact: `0<e<1/5` and `h²+(1/5)²=554/625<1`.

Combining (1) and (2) gives

```text
pβ_P ≤ b-r+r²e+prh
       = bp²+hr²-r+prh,
```

and hence

```text
p(1-β_P) ≥ p+r-h(1+pr)+ep².                           (3)
```

For positive `p,r` with `p²+r²=1`,

```text
(p+r)/(1+pr) ≥ 2sqrt(2)/3 > h.
```

To verify the first inequality without an angular approximation, put `z=pr≤1/2`:

```text
9(p+r)²-8(1+pr)²
 = 1+2z-8z²
 = (1-2z)(1+4z) ≥ 0.
```

Both sides whose squares are compared are positive.
The second inequality follows from `h²=529/625<8/9`, equivalently `4761<5000`. Thus the
right side of (3) is strictly positive, and `β_P<1`. All four local inequalities are
strict, so `P∈int(C)`. This proof includes a mark on the boundary of `C`, a separating
support gap of zero, and a square touching the bottom wall.

## Reflection and the Forced Marks

Reflect a proposed right owner in `x=q/2`. The reflected square satisfies the common
point lemma for `A_L` and `m=(a,b)`. Since `q/2=1+h`, the reflection fixes `P`.
Therefore the original right owner also contains `P` in its interior.
The left owner contains `P` by the same lemma, contradicting their disjoint interiors.

The alternate bottom-left mark `(b,a)` lies strictly inside `A_L`: `0<b<1` and
`h<a<h+1`. A distinct square with disjoint interior from `A_L` cannot contain a point in
`int(A_L)`, since every point of a closed unit square is a limit of its interior points.
Reflection proves the corresponding statement on the right.
Thus requiring corner owners additional to the fixed outer squares forces exactly the
two marks used in the theorem.

The fixed lower outer squares already satisfy the alternate corner ownership conditions,
including selected-core ownership.
Their orientations are the retained net direction zero, and the alternate mark has local
coordinates `(b,a-h)=(2336/3175,231/3175)`, both strictly between `23/20000` and
`1-23/20000`. Accordingly, this theorem does not show that the fixed outer arrangement
violates the corner-owner condition.
It excludes two further squares taking the specified bottom corner roles.

The contradiction applies to the specified fixed outer arrangement, including selected
nearest-net core ownership and all permitted boundary contacts.
Its proof does not extend the conclusion to arbitrary outer owners.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
