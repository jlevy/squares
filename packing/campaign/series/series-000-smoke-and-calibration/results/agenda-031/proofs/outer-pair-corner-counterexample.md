# Outer Pair and Two Corner Owners Coexist

Date: 2026-09-08. Status: exact rational counterexample, independently checked.
Scope: four-square local ownership compatibility at `q=96/25`; no eleven-square packing
is asserted.

Two distinct owners of the left outer-middle segment can coexist with two other squares
owning a bottom-left and a top-left corner mark.
The corner marks lie in the interiors of the concentric `B=9977/10000` cores of their
unit squares. Consequently, a four-owner incompatibility using only these ownership
conditions is false.

## Four Rational Squares

Let

```text
q = 96/25,
a = 3152/3175,    b = 2336/3175,
c = 35/37,       s = 12/37,       g = 4/5,
P = (g,s),       u = (c,-s),      v = (s,c).
```

Since `c²+s²=1`, the following are unit squares:

```text
A₋ = [0,1] × [23/25,48/25],
A₊ = [0,1] × [48/25,73/25],
C₋ = P + [0,1]u + [0,1]v,
C₊ = {(x,q-y) : (x,y) ∈ C₋}.
```

The lower corner square has vertices

```text
(g,s), (g+c,0), (g+c+s,c), (g+s,c+s)
```

and center `(531/370,47/74)`. Its coordinate ranges are

```text
4/5 ≤ x ≤ 383/185 < 96/25,
0 ≤ y ≤ 47/37 < 96/25.
```

Its reflection and both axis-aligned squares are also contained in `[0,q]²`.

Both `A₋` and `A₊` contain the whole segment

```text
M = [49/100,59/100] × {48/25}
```

on their common boundary.
Their distances from `M` are therefore zero, meeting the `3/500` ownership threshold.
The lower and upper piercing points `(9/10,41/25)` and `(9/10,11/5)` lie in their
respective interiors, each with a contained radius-`1/1000` disk.

## Corner Ownership and Separation

For the bottom-left mark `m₋=(a,b)`, its coordinates in the lower corner square are

```text
α = u·(m₋-P) = 212556/4346575,
β = v·(m₋-P) = 1963348/4346575.
```

The concentric `B` core is obtained by restricting both coordinates to `[e,1-e]`, where
`e=(1-B)/2=23/20000`. Here

```text
e < α < β < 1/2 < 1-e,
min(α,β,1-α,1-β) - e = 166045951/3477260000 > 0.
```

Thus `m₋` lies strictly inside that core.
Reflection proves that `m₊=(a,q-b)` lies strictly inside the core of `C₊`, with exactly
the same clearance.

Every point of `C₋` satisfies

```text
y ≤ s + (c/s)(x-g).
```

In particular, its part in `x≤1` has

```text
y ≤ s + (c/s)(1-g) = 403/444,
23/25 - 403/444 = 137/11100 > 0.
```

Hence `C₋` is disjoint from both outer squares.
Reflection proves the corresponding separation for `C₊`. The two corner squares have
disjoint vertical coordinate ranges, with gap

```text
q - 2(c+s) = 1202/925 > 0.
```

The outer squares have disjoint interiors and share only their horizontal boundary.
All six pairs therefore have disjoint interiors.

An independent exact separating-axis calculation from the four vertices returns the
following unit normals and projection gaps.
The sign of a normal is immaterial.

| Pair | Unit Normal | Projection Gap |
| --- | --- | --- |
| `A₋`, `A₊` | `(0,1)` | `0` |
| `A₋`, `C₋` | `(-35/37,12/37)` | `137/34225` |
| `A₋`, `C₊` | `(0,1)` | `601/925` |
| `A₊`, `C₋` | `(0,1)` | `601/925` |
| `A₊`, `C₊` | `(35/37,12/37)` | `137/34225` |
| `C₋`, `C₊` | `(12/37,35/37)` | `8414/6845` |

## Consequence and Limits

The count pattern “two left outer-middle owners, one distinct bottom-left corner owner,
one distinct top-left corner owner” is geometrically realizable, including the stronger
core-interior corner ownership requirement.

Selected mark identities matter even for this fixed axis-aligned outer pair.
The other bottom-left mark `(b,a)` lies strictly inside `A₋`, so a distinct corner owner
cannot contain it in its interior.
The analogous top-left mark `(b,q-a)` lies strictly inside `A₊`. Both separate corner
owners in this witness must therefore select the mark with x-coordinate `a`.

A subsequent global exclusion must use additional conditions, such as compatibility with
opposite-side corner owners or other segment owners.
No exclusion of such extensions follows from the present four-square calculation.
In particular, the construction neither supplies an eleven-square packing nor rules out
a more constrained ownership pattern.

The retained exact verifier checks unit edge lengths and orthogonality, container
containment, all six pairwise separating axes, both corner marks against the `B` cores,
and both segment endpoint memberships using rational arithmetic.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
