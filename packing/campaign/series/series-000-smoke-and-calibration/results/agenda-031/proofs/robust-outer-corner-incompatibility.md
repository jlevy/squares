# A Robust Outer-Corner Incompatibility

Date: 2026-09-08. Status: analytic proof by GPT-6 Astra, max, with mechanical arithmetic
and algebra replay by GPT-5.6 Sol, extra high.
The [retained replay](../robust-outer-corner-arithmetic.json) checks 23 rational
inequalities and two polynomial identities.
It does not independently prove the geometric separation and support-function lemmas
used below.

This strengthens the fixed-axis partial-pattern exclusion.
It does not exclude the outer squares themselves or prove an eleven-square packing
bound.

Put `q = 96/25`, `h = 23/25`, `a = 3152/3175`, `b = 2336/3175`, `d = 1-a = 23/3175`,
`e = h-b = 117/635`, and `epsilon = 1/1000`. Set `H = h+epsilon`, `E = e+epsilon`, and
`P = (48/25,b)`. Let

```text
R_L = [epsilon,1-epsilon] x [h+epsilon,h+1-epsilon],
R_R = reflection of R_L in x=q/2.
```

**Claim.** Suppose two contained unit squares `A_L'` and `A_R'` contain `R_L` and `R_R`,
respectively.
Two further interior-disjoint contained unit squares cannot contain `(a,b)`
and `(q-a,b)`, respectively, while avoiding both outer squares.
In fact, every unit square `C` in the positive quadrant which contains `(a,b)` and whose
interior avoids `R_L` contains the closed disk of radius `1/100` about `P` in its
interior.

## The Common Disk

Choose a unit separating-axis normal `v` directed from `R_L` to `C`. Since `a` lies
strictly between the rectangle’s vertical sides and `b` is below its bottom, `v_y >= 0`
would give `max(R_L,v) > v.(a,b)`, a contradiction.
Thus `v_y < 0`.

If `v_x <= 0`, write `v=(-p,-r)`, where `p>=0` and `r>0`. Mark containment and
separation give `p(a-epsilon) <= rE`. Since `C` lies in `x>=0`, separation then puts all
of `C` below

```text
y <= H + epsilon p/r <= H + epsilon E/(a-epsilon) < 1.
```

The last bound follows from `H<37/40`, `E<1/5`, `a-epsilon>9/10` and
`37/40 + 1/4500 < 1`. A unit square has vertical span at least one, so this is
impossible. Hence `v_x>0` and `v_y<0`. Such a normal is not a side normal of the
axis-aligned rectangle, so the separating-axis theorem selects a side normal of `C`.

Write `n=(p,-r)`, `w=(r,p)`, with `p,r>0` and `p^2+r^2=1`. In these coordinates `C` is
`[k,k+1] x [l,l+1]`. Let `alpha=n.(a,b)-k` and `beta=w.(a,b)-l`, both in `[0,1]`.
Separation and bottom containment give

```text
alpha <= -p(d-epsilon)+rE,
p beta <= b-r+r alpha.
```

Because `P=(a,b)+(h+d,0)`, its local coordinates are

```text
alpha_P = alpha+p(h+d),
beta_P = beta+r(h+d).
```

First obtain uniform positive lower bounds.
The two inequalities above imply `b >= r-r^2 E`. Since `E<1/5`, the function `r-r^2 E`
increases on `[0,1]`. If `r>=9/10`, it would exceed `369/500>b`; therefore `r<9/10` and
`p>2/5`. Also `alpha>=0` gives `r >= p(d-epsilon)/E > 1/80`, because `32(d-epsilon)>E`,
equivalently `151/3175 > 33/1000`. Consequently

```text
alpha_P > (2/5)h = 46/125 > 1/100,
beta_P > h/80 = 23/2000 > 1/100.
```

For the first upper bound,

```text
alpha_P <= Hp+Er <= sqrt(H^2+E^2)
        < sqrt(1433/1600) < 19/20 < 99/100.
```

Combining the two support inequalities gives the second upper bound:

```text
p(1-beta_P) >= p+r-H(1+pr)+E p^2.
```

For `z=pr<=1/2`,

```text
9(p+r)^2-8(1+pr)^2 = (1-2z)(1+4z) >= 0,
```

so `(p+r)/(1+pr) >= 2sqrt(2)/3 > 47/50 > H`. Since `(1+pr)/p>=1`,

```text
1-beta_P > 47/50-H = 19/1000 > 1/100.
```

All four signed distances from `P` to the sides of `C` exceed `1/100`. The claimed
closed disk is therefore in `int(C)`. The proof permits mark containment and
inter-square contact on the boundary.

## Reflection and Perturbations

Reflection in `x=q/2` fixes `P` and gives the same common disk for every right corner
owner. Two such additional owners overlap in an open disk, so cannot be
interior-disjoint.

The alternate marks `(b,a)` and `(q-b,a)` are strictly inside `R_L` and `R_R`. Thus an
additional owner cannot take either alternate mark; the two marks in the claim are
forced for those additional roles.
This does not require the outer squares themselves to relinquish their existing
corner-owner roles.

For a useful sufficient perturbation condition, any convex outer square at Euclidean
Hausdorff distance at most `epsilon` from the corresponding fixed axis square contains
the rectangle inset by `epsilon`. Indeed, its support in each unit direction is at least
the axis square’s support minus `epsilon`, while every point of the inset rectangle lies
at least `epsilon` behind all of the axis square’s support lines.
Applying this in every direction proves containment.
Hence the exclusion covers such perturbations of both fixed lower outer squares, subject
to the stated packing and additional-owner assumptions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
