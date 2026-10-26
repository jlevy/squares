# C1092: a direct negative cycle from the original actual owners

The scalar argument below is retained as an independent continuous
ending on its stated interval. The complete all-nonpositive sector is
now excluded, without an incoming magnitude bound, by
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md)
and [C1092-NEGATIVE-OWNED-POINTS.md](C1092-NEGATIVE-OWNED-POINTS.md).

All finite decimals are exact rationals. Owned points are strict in an
open square. Excluded points and separating supports allow equality.

## 1. The completed branch

**Theorem 1.** In the original C1092 physical setting, retain the last
MPPM auxiliary assignment

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

If all four canonical central signed half-angles lie in [−1/7,0],
the configuration is impossible.

This is a direct continuous exclusion from the original actual-owner
geometry and the displayed assignment. It uses none of the 431
common-parent coordinate cuts, no incoming maximal-angle history, no
center enclosure from those histories, and no boundary-angle restriction.
The retained paired-corner inner-point theorem is still used.

The earlier direct wall-point theorem supplies the boundary points.
The new ingredients below derive the central centers directly, replace
the boundary support argument by a strict segment intersection, and
retain enough scalar variation to allow a small positive vertical
displacement between adjacent central centers.

This statement concerns precisely the four-angle region [−1/7,0]^4.
It does not assert an exclusion of the remaining positive, mixed, or
steeper negative regions of the last assignment.

## 2. Direct faces and centers

**Lemma 2.** Let an open square C of side a>1 have canonical normals

    u=(c,−s), v=(s,c),
    c=(1−q²)/(1+q²), s=2q/(1+q²), 0≤q≤1/7.

Suppose C strictly owns

    U₀=(1,1.74), T=(1.74,2)

and excludes

    D=(1,2), G₀=(1.74,1), R₀=(2,1.74),
    N=(1.65,2.35), F=(2,2.26).

Then its center (Cₓ,Cᵧ) satisfies

    7/5<Cₓ<38/25,       3/2<Cᵧ<19/10.                 (1)

Write its open face bands as

    U<u·X<U+a,       V<v·X<V+a.

The following actual faces are forced:

    U≥c−2s,                 U+a≤2c−1.74s,
    V≥c+1.74s,              V+a≤1.65s+2.35c,
                             V+a≤2s+2.26c.            (2)

### 2.1. The face alternatives

The angle range gives

    c≥24/25, 0≤s≤7/25, c−s≥17/25,
    c+s≤31/25,       cs≤168/625.                      (3)

The final two functions increase on the indicated angle interval.

At D, comparison with strict U₀ gives the upper u and lower v bands;
comparison with strict T gives the upper v band. Hence D can leave
only through lower u, giving the first inequality in (2). If s=0,
D and U₀ have the same u coordinate, so this conclusion itself is
impossible. Keeping zero in subsequent weak estimates is harmless.

At R₀, comparison with U₀ gives both lower bands. Its upper v band
follows from T, because

    v(R₀)−v(T)=.26(s−c)≤0.

Thus R₀ leaves through upper u.

At G₀, the lower u band follows from U₀, and the upper v band follows
from U₀, since

    u(G₀)−u(U₀)=.74(c+s)>0,
    v(U₀)−v(G₀)=.74(c−s)>0.

An upper-u exit, combined with the lower-u face at D, would imply

    a≤u(G₀)−u(D)=.74c+s
      =1−(1−q)(13−87q)/(50(1+q²))<1.

Here 13−87q≥4/7>0. Thus G₀ leaves through lower v.

At N, the lower u band follows from U₀, the upper u band follows
from T, and the lower v band follows from T:

    u(N)−u(U₀)=.65c−.61s>0,
    u(T)−u(N)=.09c+.35s>0,
    v(N)−v(T)=.35c−.09s>0.

Consequently N leaves through upper v.

At F, the lower u band follows from T and the lower v band follows
from U₀. Its upper u band is also strict: the lower-u face at D gives

    u(F)−U≤u(F)−u(D)=c−.26s≤1<a.

Therefore F leaves through upper v. This proves (2), with strict
comparison points handling every equality of projections.

### 2.2. The lower center bounds

The center is

    Cₓ=c(U+a/2)+s(V+a/2),
    Cᵧ=−s(U+a/2)+c(V+a/2).

Use the upper-u and lower-v faces in (2) to obtain

    Cᵧ≥1+.74s²−.26cs+(a/2)(c+s)
       >3/2+.74s²+cs[1/(c+s+1)−13/50]≥3/2.           (4)

Here c+s<3/2, and (c+s−1)/2=cs/(c+s+1).

The two lower faces in (2) give

    Cₓ≥1+.74s²−cs+(a/2)(c+s).

For the expression with a replaced by 1, the exact identity is

    1+.74s²−cs+(c+s)/2−7/5
      =[5−50q+108q²+150q³−45q⁴]/[50(1+q²)²]>0.       (5)

The numerator decreases on [0,1/7]: its derivative is at most
−50+216/7+450/49=−488/49<0. Its value at 1/7 is
1152/2401>0. This proves Cₓ>7/5.

### 2.3. The upper center bounds

The lower-u face at D and upper-v face at N give

    Cᵧ≤2.35−.35s²+.65cs−(a/2)(c+s)<1.9.               (6)

To check the last inequality exactly, replace a by 1. The difference
between 1.9 and the resulting expression is

    [1−6q+10q²+46q³−19q⁴]/[20(1+q²)²]>0.

Indeed 1−6q≥1/7 and 10−19q²>0.

The upper-u face at R₀ and upper-v face at F give

    Cₓ≤2+.52cs−(a/2)(c+s)
       <1.5+cs[.52−1/(c+s+1)]
       ≤1.5+309/15625<1.52.                           (7)

Here (3) gives 1/(c+s+1)≥25/56. The final exact margin is
1/50−309/15625=7/31250>0. Equations (4)–(7)
prove (1). No wall or upper bound on a was used. ∎

## 3. A whole actual boundary segment gives the wall clearance

**Lemma 3.** In the setting of Lemma 2, suppose a different actual
open square B is disjoint from C and strictly owns

    L=(1.6,1), P=(2,1).

Then

    Cᵧ>1+(a/2)(c+s).                                  (8)

No angle, center, or wall hypothesis on B is needed.

Let Z be the lowest vertex of the closure of C:

    Z=(Cₓ+(a/2)(c−s), Cᵧ−(a/2)(c+s)).

From (1),(3) and a>1,

    Zₓ>7/5+17/50=87/50>17/10.

Suppose Zᵧ≤1. The vertex lies on the upper-u face of C, and R₀
is excluded through that face. Therefore

    cZₓ−sZᵧ=U+a≤2c−1.74s,
    c(Zₓ−2)≤s(Zᵧ−1.74)≤0.

Thus Zₓ≤2. Since T=(1.74,2) lies strictly in C, the segment [Z,T]
meets y=1 at a point W with

    1.6<Wₓ≤2.

It follows that W belongs to the closed square C and to the entire
strict segment [L,P] inside B. This is impossible: for two disjoint
open squares, the closure of one cannot meet the interior of the
other. Any such meeting point would, by openness of the second
square, also give a nearby point in both interiors.

This also handles Zᵧ=1 and W=P. Hence Zᵧ>1, which is (8). ∎

## 4. A stronger scalar reserve for four nonnegative parameters

Use the same rational formulas as
[C1092-CYCLES.md](C1092-CYCLES.md), here on the larger nonnegative
interval [0,1/7]. Explicitly,

    Δ=|u−v|,
    G(u,v)=Δ(1+uv−Δ)/[(1+u²)(1+v²)],
    K(u,v)=G(u,v)−(11/20)|c(u)−c(v)|,

    D(h,q)=[2(h−q)²(1+q+2q³)+8(h−q)(q²+q⁴)+4(q³+q⁵)]
             /[(1+h²)(1+q)(1+q²)],

    f_h(q)=D(h,q)−(11/10)[c(q)−c(h)].

All denominators are positive. The proof below establishes the needed
estimates on the full larger interval; it does not extend an earlier
domain merely by reference.

**Lemma 4.** For 0≤q≤h≤1/7,

    f_h(q)≥−(3/8)(h−q).                                (9)

Put H=1/7, z=h−q, and B=(1+h²)(1+q²). The exact nonnegative
formula for D gives

    B(1+q)[f_h(q)+(3/8)z]≥P(z,q),                     (10)

where

    P(z,q)=z[(3/8)(1+q)−(22/5)q(1+q)+8q²−(1+q)z/5]
             +4q³(1+q²).

For completeness, the first term of BD is at least 2z², its second
is at least 8zq²/(1+q), and the third is exactly
4q³(1+q²)/(1+q). The cosine difference contributes
−(11/5)z(h+q), and B(3/8)z≥(3/8)z.
Multiply by 1+q and use h=q+z to obtain (10).

For fixed q, P is concave in z on [0,H−q], so its minimum is at
an endpoint. At zero it is 4q³(1+q²)≥0. At the other endpoint,
direct expansion gives

    P(H−q,q)
      =(7840q⁵+392q³+8617q²−1758q+97)/1960
      ≥(17/4)q²−(9/10)q+49/1000
      =(17/4)(q−9/85)²+23/17000>0.

The coefficient comparison is termwise for q≥0:
1231/280>17/4, 879/980<9/10, and 97/1960>49/1000;
the cubic and quintic coefficients are positive. Thus P≥0 on the
whole two-parameter domain, including q=h and q=0. This proves (9).

For the edges, the exact cosine identity gives

    K(u,v)=|u−v|[1+uv−|u−v|−(11/10)(u+v)]
                /[(1+u²)(1+v²)].

The function |u−v|+(11/10)(u+v)−uv is convex in each variable
separately. On [0,H]² its maximum is therefore at a corner and
is at most

    max((21/10)H,(11/5)H−H²)=3/10.

Since the denominator is at most (50/49)²,

    K(u,v)≥(16807/25000)|u−v|≥(2/3)|u−v|.             (11)

Now let q₀=h=max_i qᵢ, with 0≤qᵢ≤h≤1/7, cyclic modulo four, and put

    V₀=Σ|qᵢ−qᵢ₊₁|.

The exact maximum identity gives

    Φ=Σ{G(qᵢ,qᵢ₊₁)
          −(11/10)[max(c(qᵢ),c(qᵢ₊₁))−c(h)]}
        +ΣD(h,qᵢ)
      =ΣK(qᵢ,qᵢ₊₁)+Σf_h(qᵢ).

The two paths from the maximal vertex to each other vertex give

    Σ(h−qᵢ)≤(3/2)V₀.

Thus (9),(11) yield the reserve

    Φ≥(2/3−9/16)V₀=(5/48)V₀.                         (12)

This estimate also includes V₀=0 and h=0. ∎

## 5. Closing the cycle with the directly proved center boxes

Work in four charts related by R(x,y)=(4−y,x). Let Cᵢ have the local
data of Lemma 2, parameter qᵢ, and a corresponding distinct Bᵢ
as in Lemma 3. Assume all these are actual pairwise interior-disjoint
squares of the common side a>1. Relabel the cyclic starting index
so q₀=h=max qᵢ.

Write the local center of Cᵢ as (2−Xᵢ,2−Yᵢ). The next central
center in its chart is

    Jᵢ=(2+Yᵢ₊₁,2−Xᵢ₊₁).

Lemma 2 gives directly

    0<Jᵢₓ−Cᵢₓ<11/10,
    −1/2<Jᵢᵧ−Cᵢᵧ<1/50.                              (13)

In fact the horizontal lower bound is 29/50.

### 5.1. Upper support

Put c=c(h), s=s(h), w=c+s, d=c−s, and

    Fᵢ=wXᵢ+dYᵢ.

The lower-u face at D and Lemma 3 give

    c(qᵢ)Xᵢ−s(qᵢ)Yᵢ≤c(qᵢ)−a/2,
    Yᵢ<1−(a/2)[c(qᵢ)+s(qᵢ)].

Eliminate with positive multipliers w and
w s(qᵢ)+d c(qᵢ), and replace a by 1 in the upper bound. The same
exact identity as C1092-NEGATIVE-GEOMETRY.md §5 gives

    Fᵢ≤1−D(h,qᵢ).                                    (14)

Explicitly the expression before subtracting D is

    2c−w[1−s(qᵢ)]/c(qᵢ)+s c(qᵢ)−c s(qᵢ)=1−D(h,qᵢ).

No imported center or boundary enclosure is needed for (14).

### 5.2. Lower support and the small vertical transport cost

A second normal of either adjacent central square has projection
on Jᵢ−Cᵢ of absolute value less than

    (7/25)(11/10)+1/2=101/125<1.

A forward first normal has projection greater than −7/50. Since
disjoint side-a squares need separating support at least a>1 in
some side-normal direction, only a forward first normal of one
endpoint can separate the pair.

If its parameter rᵢ is qᵢ or qᵢ₊₁, the exact sum of the two support
radii is a[1+G(qᵢ,qᵢ₊₁)]. Transport this normal to n(h)=(c(h),−s(h)).
The horizontal loss is at most

    (11/10)[max(c(qᵢ),c(qᵢ₊₁))−c(h)].

By (13), the additional vertical loss is at most

    (1/50)[s(h)−s(rᵢ)]≤(1/25)(h−rᵢ),                 (15)

because 0≤s'(q)≤2 on the parameter interval. For arbitrary choices
of the endpoint source,

    Σ(h−rᵢ)
      ≤Σ[h−min(qᵢ,qᵢ₊₁)]
      =Σ(h−qᵢ)+V₀/2≤2V₀.

The total extra cost in (15) is therefore at most (2/25)V₀.

### 5.3. The contradiction

The chart identity gives

    Σn(h)·(Jᵢ−Cᵢ)=ΣFᵢ.

Combining the actual lower supports, (14), and the definition of Φ,

    0≥4(a−1)+Φ−(2/25)V₀
      ≥4(a−1)+(29/1200)V₀>0,                           (16)

where the second inequality is (12). This contradiction closes the
cycle. Equal angles, zero variation, ties for the maximum, both
endpoint normal sources, and touching square boundaries are included.

## 6. Exact application to the original last assignment

Use the actual owners and charts

    Cᵢ=Q₄₊ᵢ, Kᵢ=Qᵢ,
    (B₀,B₁,B₂,B₃)=(Q₉,Q₁₀,Q₁₁,Q₈),
    local chart R^(−i).

The displayed original assignment makes every Cᵢ strictly own local

    (1.65,1.65), (1,1.74), (1.74,2), (1,1.6),

and makes every Bᵢ strictly own local (1.6,1), (1.74,1), and (2,.914).
All four qᵢ≤1/7, so
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md),
Theorem 8, proves local (2,1) strictly inside each actual Bᵢ.
That theorem uses the original actual corner owner, its two genuine
walls, and the retained paired-corner point; it makes no assumption
about the boundary or corner orientation.

Every exclusion in Lemma 2 now has a named actual owner:

| Local excluded point | Its actual strict owner | Source |
|---|---|---|
| D=(1,2) | Bᵢ₋₁ | Quarter-turn of the proved boundary point |
| G₀=(1.74,1) | Bᵢ | Original auxiliary assignment |
| R₀=(2,1.74) | Cᵢ₊₁ | R applied to the next local T |
| N=(1.65,2.35) | Cᵢ₋₁ | R^(−1) applied to the preceding local central marker |
| F=(2,2.26) | Cᵢ₋₁ | R^(−1) applied to the preceding local T |

The whole segment [L,P] used in Lemma 3 lies strictly in the same
actual Bᵢ. Hence all hypotheses of Sections 2–5 hold directly, and
(16) proves Theorem 1.

## 7. What this replaces, and the remaining scope

The branch in which all four central signed half-angles lie in
[−1/7,0] now has a complete direct ending from the original last
assignment. It needs none of the historical central center boxes,
relative-center boxes, boundary-angle intervals, moving boundary
points, or directed geometric updates used by the older entrance.

The full negative-terminal theorem in the earlier chapters remains
useful for sign-mixed configurations in a negative maximal-angle
range. The new result is stronger about its entrance and narrower
about its sign domain. Positive or mixed central angles, negative
half-angle magnitudes above 1/7, and reduction to the last auxiliary
assignment remain separate obligations. No assertion about those
unproved branches is used here.
