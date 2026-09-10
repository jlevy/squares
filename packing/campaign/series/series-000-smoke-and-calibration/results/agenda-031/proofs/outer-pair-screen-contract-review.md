# Review of the Fixed-Angle Outer-Pair Screen

Date: 2026-09-08. The proposed screen is a sound necessary-condition test for an ordered
pair of outer-segment owners at the supplied exact rational angles.
A surviving branch certifies feasibility of the stated relaxation; rejecting every
branch proves that the ordered angle pair cannot occur.
This screen is a guarded analytic reader, not a geometric search.

## Input and Domain Contract

Use `q=96/25`, `ℓ=1/10`, `δ=3/500`, `ρ=1/1000`, and the segment midpoint and anchors
from [the outer capacity proof](outer-middle-capacity-two-proof.md).
For the left segment these are

```text
m = (27/50,48/25),
p₁ = m+(9/25,-7/25),   p₂ = m+(9/25,7/25).
```

The angle ordering is part of the contract: `t₁` belongs to the lower-anchor owner and
`t₂` to the upper-anchor owner.
An unordered pair of input angles must cover both anchor assignments.
Enumerating normal signs does not exchange those assignments.

For signed folded rational `t_i`, define the orthonormal basis

```text
c_i = (1-t_i²)/(1+t_i²),   s_i = 2t_i/(1+t_i²),
u_i = (c_i,s_i),          w_i = (-s_i,c_i),
|t_i| ≤ sqrt(2)-1,
h_i = (|c_i|+|s_i|)/2,
H_i(v) = (|v·u_i|+|v·w_i|)/2.
```

The folded-range check can be exact: `t_i²+2|t_i|≤1`. Every supplied normal is unit, so
its support tolerance is `r_v=ℓ|v_x|/2+δ`. An unnormalized replacement would need the
corresponding norm factors on the disk tolerances.

For center `z_i`, the proposed initial domain `D_i` consists of the following closed
half-planes:

```text
h_i ≤ (z_i)_x,(z_i)_y ≤ q-h_i,
|v·(z_i-m)| ≤ H_i(v)+r_v     for v=(1,0),(0,1),u_i,w_i,
|u_i·(z_i-p_i)| ≤ 1/2-ρ,
|w_i·(z_i-p_i)| ≤ 1/2-ρ.
```

The box is exactly container containment for that square orientation.
The two anchor slabs are exactly containment of the closed radius-`ρ` disk about its
assigned anchor. Actual owners satisfy them by the capacity proof.

The tube slabs are necessary: if a point of the square is within `δ` of the segment,
project that witness onto any unit `v` and apply the square and segment support bounds.
The finite collection of directions gives an outer approximation to the center domain
for Euclidean tube intersection; it does not enforce all support directions of the round
tube. Every actual owner center belongs to `D_i`.

## Separating Branches and Completeness

Enumerate `v∈{±u₁,±w₁,±u₂,±w₂}`. For each signed normal, clip the domains to

```text
D₁(v): v·m-r_v-H₁(v) ≤ v·z₁ ≤ v·m+r_v-H₁(v),
D₂(v): v·m-r_v+H₂(v) ≤ v·z₂ ≤ v·m+r_v+H₂(v).
```

For an actual ordered separating pair, put

```text
α = v·z₁+H₁(v),   β = v·z₂-H₂(v),   α≤β.
```

The ownership witnesses give `α≥v·m-r_v` and `β≤v·m+r_v`. Combining those bounds with
`α≤β` gives the two proposed clips, including their signs and support shifts.

If both clipped domains are nonempty, define

```text
L = min_{z₁∈D₁(v)} v·z₁,
U = max_{z₂∈D₂(v)} v·z₂.
```

They are compact, so both extrema are attained.
Because the domains are independent, there exist centers in this branch satisfying weak
separation exactly when

```text
L+H₁(v) ≤ U-H₂(v).                                    (1)
```

The minimizing first center and maximizing second center realize separation when (1)
holds. This is equivalence for the branch relaxation; those centers can still fail the
original Euclidean ownership conditions.

Every pair of squares with disjoint interiors has a weak separating axis among its side
normals. The signs above include its orientation from the lower-anchor owner to the
upper-anchor owner. Thus every actual pair survives at least one branch.
Rejecting all branches proves impossibility for the fixed ordered angles; a surviving
branch remains unresolved as an ownership test.

The preliminary rejections

```text
v_y < 1/280,
56v_y < 62|v_x|-1
```

are sound for that ordered separator by
[the reviewed anchor cuts](new-outer-constraints-review.md).
Their failure tests must be strict.
Equality remains admissible.
Reflection to the right segment preserves these cuts.

Exact rational clipping must retain lower-dimensional domains: a point or a line segment
is nonempty and may realize a touching configuration.
Zero polygon area, or fewer than three distinct vertices, is not an emptiness
certificate. Half-plane boundaries and equality in (1) must survive.

## Exact Controls

These controls use the angle ordering stated above.

| Ordered Half-Tangents | Required Outcome | Evidence |
| --- | --- | --- |
| `(1/4,1/4)` | Survives | Contained touching pair below |
| `(-1/4,-1/4)` | Survives | Contained touching pair below |
| `(-1/4,1/4)` | Survives | Pair touching at `m`, below |
| `(1/3,1/3)` | All branches rejected | Exact clipped-domain contradiction below |
| `(-1/3,-1/3)` | All branches rejected | Reflection of the preceding contradiction |

For either sign `σ∈{-1,1}`, set

```text
c = 15/17,   s = σ·8/17,
u = (c,s),   w = (-s,c),
Q₁ = m+[0,1]u+[-1,0]w,
Q₂ = m+[0,1]u+[0,1]w.
```

Their signed half-tangents are both `σ/4`. The squares meet along the common side
`m+[0,1]u` and have disjoint interiors.
Each contains `m`, so its distance from the outer segment is zero.
Their x-coordinates are at least `27/50-8/17=59/850>0`; their x-coordinates are at most
`27/50+23/17<q`, and their y-coordinates lie in `[48/25-23/17,48/25+23/17]⊂(0,q)`.

The anchors’ coordinates in the displayed `u,w` frame are

| Sign | Lower Anchor in `Q₁` | Upper Anchor in `Q₂` |
| --- | --- | --- |
| `σ=1` | `(79/425,-177/425)` | `(191/425,33/425)` |
| `σ=-1` | `(191/425,-33/425)` | `(79/425,177/425)` |

Every edge distance is at least `33/425>ρ`. Thus these witnesses satisfy the anchor disk
constraints directly as well as true segment ownership.

For `(-1/4,1/4)`, take the preceding `σ=-1` square `Q₁` and reflect it in `y=48/25` to
obtain `Q₂`. The lower square lies in `y≤48/25`, the upper in `y≥48/25`, and they meet
at `m`. The same containment and anchor-clearance bounds apply.
Their respective folded half-tangents are `-1/4` and `1/4`.

For the negative control `(1/3,1/3)`, use

```text
c = 4/5,   s = 3/5,
u = (c,s),   w = (-s,c),
r_u = 23/500,   r_w = 9/250.
```

The only normal surviving the preliminary cuts is `w`. The normal `u` has
`56u_y-62|u_x|+1=-15<0`; the other two normals have negative y-coordinate.
For a center of the upper owner in the `w` branch, put

```text
k = u·z₂-1/2,   l = w·z₂-1/2.
```

The `u` tube slab gives `k≤u·m+r_u`, and the branch clip gives `l≥w·m-r_w`. Left-wall
containment requires

```text
ck-sl ≥ s,
```

because the square’s least x-coordinate is `ck-s(l+1)`. The first two bounds would
therefore require

```text
s ≤ c(u·m+r_u)-s(w·m-r_w)
  = m_x+cr_u+sr_w
  = 27/50+(4/5)(23/500)+(3/5)(9/250)
  = 374/625.
```

But `s=3/5=375/625`. The clipped upper domain is empty, with contradiction gap `1/625`.
This control lies below the steep-angle threshold `49/125`, so it checks the domain
clipping in addition to the preliminary angular test.
Reflection in `y=48/25`, with the anchor order exchanged, proves rejection of
`(-1/3,-1/3)`.

## Margins in the Separate Fixed-Outer Proof

The [common-point proof](fixed-outer-pairs-bottom-corner-incompatibility.md) has uniform
slack in its two upper local-coordinate bounds.
Its inequalities give `α_P<19/20` and `β_P<74/75`: for the first, compare
`554/625<361/400`; for the second, use `2sqrt(2)/3>14/15` and `14/15-23/25=1/75` in that
proof’s equation (3).

Those margins support attempting a quantitative stability estimate for perturbations of
the fixed outer squares.
An explicit neighborhood would also need uniform lower coordinate clearances and control
of the separating-normal sign argument under perturbation.
No perturbation radius is established here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
