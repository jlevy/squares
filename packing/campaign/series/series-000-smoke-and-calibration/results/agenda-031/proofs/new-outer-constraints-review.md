# Independent Review of the New Outer-Segment Constraints

Date: 2026-09-08. The capacity-two proof, the exact four-square counterexample, and the
proposed angular exclusion are sound.
This review checked the explicit arguments and supplied rational verifier.

## Capacity and Separator Cuts

In [the capacity-two proof](outer-middle-capacity-two-proof.md), the chord formulas and
their changes of branch agree at every boundary.
The bounds `u-l≥3/5`, `l-L<9/35`, and `U-u<1/4` hold on the stated closed orientation
range.
The proof treats `s=0` separately and includes `s=c`. Its interval overlap has the
strict margin `3/5-59/100=1/100`; the endpoint coverage inequalities are also strict.
The disk-clearance argument correctly separates `s≥1/15` from `s≤1/15` and includes
zero.
Thus every owner contains a closed radius-`ρ=1/1000` disk about at least one of the
two stated piercing points.

The upper-displacement calculation has no reversed inequality.
Its bracket `(3/5)/c-1/2` is nonnegative for `1/√2≤c≤1`. Its final use of `√2>7/5` is
valid because `1/(2√2)=√2/4>7/20`, giving `3/5-1/(2√2)<1/4`.

Two owners must contain different piercing points: a shared point would lie in both
interiors, and an owner containing both points would exclude every other owner.
The attaining axis-aligned pair proves that the capacity is exactly two.

For completeness, order a pair as lower-anchor owner `Q₋`, upper-anchor owner `Q₊`. For
any unit weak separating normal in that order, write

```text
α = max_{x∈Q₋} v·x ≤ β = min_{x∈Q₊} v·x,
r = |v_x|/20 + 3/500,
m = (27/50,48/25),
p₋-m = (9/25,-7/25),   p₊-m = (9/25,7/25).
```

Ownership and the two disks imply

```text
v·m-r ≤ α ≤ β ≤ v·m+r,
v·p₋+ρ ≤ α ≤ β ≤ v·p₊-ρ.
```

The second chain gives `(14/25)v_y≥2ρ`, hence `v_y≥1/280`. Combining the chains on each
side gives

```text
(7/25)v_y ≥  (9/25)v_x-r+ρ,
(7/25)v_y ≥ -(9/25)v_x-r+ρ.
```

Taking their maximum and substituting `r` yields

```text
(7/25)v_y ≥ (31/100)|v_x|-1/200,
56v_y ≥ 62|v_x|-1.                                      (1)
```

Reflection to the right segment reverses the common x-offset and preserves (1). The
argument allows `α=β` throughout, including touching squares.

## Exact Angular Exclusion

For a unit square, reduce its edge orientation modulo `π/2` to `θ∈[-π/4,π/4]`, and
define its **absolute folded half-tangent** by

```text
t = tan(|θ|/2) ∈ [0,√2-1],
c = (1-t²)/(1+t²),   s = 2t/(1+t²),   c≥s≥0.
```

Every side normal with positive y-coordinate has component magnitudes
`(|v_x|,v_y)=(s,c)` or `(c,s)`. Reducing modulo `π/2` relabels the edges; taking the
absolute value records their component magnitudes in the original coordinates.
The sign of `θ` changes the x-signs of the upward normals without changing these two
families. At `t=0`, horizontal normals have `v_y=0` and are already excluded by the disk
bound.

Two squares with disjoint interiors have a weak separating axis among their side
normals.
Orient such an axis from `Q₋` to `Q₊`; the disk bound forces its y-coordinate to
be positive. It must satisfy (1).

For the first normal family, (1) requires

```text
56c-62s+1 ≥ 0
⇔ 55t²+124t-57 ≤ 0.                                    (2)
```

The polynomial in (2) increases strictly on `t≥0`, and

```text
55(49/125)²+124(49/125)-57 = 186/3125 > 0.
```

Therefore this family cannot separate a shared-owner pair when its square has
`t≥49/125`. The second family cannot restore separation, since

```text
(56c-62s+1)-(56s-62c+1) = 118(c-s) ≥ 0.
```

Its left-hand side in (1) has no larger margin than the already negative first-family
margin. Consequently, if both owners have `t≥49/125`, every side-normal candidate from
either square fails (1), contradicting the separating-axis theorem.

**Corollary.** For either outer-middle segment, any two distinct owners include a square
with absolute folded half-tangent strictly less than `49/125`. Equality at the threshold
is excluded.
Vertical reflection preserves `|v_x|` and `v_y`; horizontal reflection swaps
the anchors, and reversing the pair order again preserves these quantities.
Both reflections preserve the folded half-tangents.

## Four-Square Counterexample and Core Scope

[The counterexample](outer-pair-corner-counterexample.md) is valid.
Its retained exact rational verifier passed all assertions during independent review.
The four vertex cycles are unit squares, all vertices lie in `[0,96/25]²`, and all six
listed separating normals and rational gaps match the output.
The two outer squares contain both endpoints of the outer segment.
Their convexity then gives ownership of the entire segment.

The geometric separation proof also holds directly: writing a point of `C₋` as
`P+λu+μv`, with `0≤λ,μ≤1`, gives

```text
s+(c/s)(x-g)-y = λ/s ≥ 0.
```

Thus its part with `x≤1` lies below `A₋` by at least `137/11100`. Reflection gives the
upper separation, and the two corner squares have vertical gap `1202/925`. The outer
pair meets only along its shared boundary.

The verifier checks the corner marks against concentric cores cooriented with their
owners. It obtains

```text
α = 212556/4346575,   β = 1963348/4346575,
core edge clearance = 166045951/3477260000 > 0.
```

The witness also meets the retained nearest-net core convention.
Indeed, `1/25<α<β<1/2`, so the centered mark coordinates have maximum absolute
coordinate less than `23/50`. If `d` is the rotation to a nearest retained net angle,
that review gives `tan|d|≤D=207107/90000000<1/100`. In the rotated core frame, each
absolute coordinate is therefore less than

```text
(23/50)(cos|d|+sin|d|)
≤ (23/50)(1+D)
< (23/50)(101/100)
= 2323/5000 < 9977/20000 = B/2.
```

Both marks remain strictly inside their selected nearest-net cores.
Reflection preserves the estimate.
This argument supplies the selected-core check that the cooriented-core verifier itself
does not perform.

The witness refutes incompatibility based solely on two owners of one outer segment and
distinct owners of the two chosen adjacent corner marks, including selected-core
ownership. Its four squares establish no extension to an eleven-square packing and no
compatibility with additional opposite-side or segment-owner constraints.
The angular corollary is a necessary local condition; it gives no global packing bound
by itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
