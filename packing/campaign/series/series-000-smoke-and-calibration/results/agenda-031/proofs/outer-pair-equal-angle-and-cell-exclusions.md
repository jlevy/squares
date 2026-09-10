# Exact Outer-Pair Exclusions for a Broad Same-Sign Angle Band

Date: 2026-09-08. Status: analytic proof, independently checked.

**Band theorem.** Two distinct owners of the same outer-middle segment cannot have both
signed folded half-tangents in either one of the closed bands

```text
I₊ = [1997/6000, sqrt(2)-1],
I₋ = [1-sqrt(2), -1997/6000].
```

The proof gives a uniform contradiction margin of `501/1000000`. The equal-angle
threshold and the smaller two-angle control cells below give further exact statements.
These results concern angle families and do not give a global packing bound.
The argument is analytic and covers real half-tangents, including irrational values.

Use the constants and ordered lower/upper anchor convention of
[the screen contract](outer-pair-screen-contract-review.md).
In particular,

```text
q = 96/25,   m = (27/50,48/25),
ℓ = 1/10,   δ = 3/500,
A = m_x+ℓ/2 = 59/100.
```

The derivations use necessary inequalities already present in the screen, so they also
prove that its relaxation rejects the stated angles.

## The Equal-Angle Family

Suppose both owners have the same positive folded angle `θ∈(0,π/4]`. Write

```text
c = cos θ,   s = sin θ,   c≥s>0,
u = (c,s),   v = (-s,c).
```

Every ordered separating normal must satisfy `v_y>0` and `56v_y≥62|v_x|-1`. The other
upward normal `u` fails the second condition, since

```text
56s-62c+1 ≤ 1-6c ≤ 1-3sqrt(2) < 0.
```

The downward normals fail the positive-y condition.
Thus only `v` can separate the lower-anchor owner from the upper-anchor owner.

Let `C` be the upper owner’s center.
Its `u` tube slab and the shared separating support give

```text
u·(C-m) ≤ 1/2+ℓc/2+δ,
v·(C-m) ≥ 1/2-ℓs/2-δ.
```

Since `(1,0)=cu-sv`, these imply

```text
C_x ≤ m_x+(c-s)/2+ℓ/2+δ(c+s).
```

Container containment requires `C_x≥(c+s)/2`; therefore

```text
s ≤ A+δ(c+s).                                        (1)
```

For `t=tan(θ/2)`, the exact difference in (1) is

```text
A+δ(c+s)-s
 = (146t²-497t+149)/(250(1+t²)).                       (2)
```

Consequently, putting

```text
t₀ = (497-sqrt(159993))/292,
```

every equal-angle pair with `t₀<t≤sqrt(2)-1` is impossible.
The polynomial in (2) decreases strictly on this range: its derivative is `292t-497<0`,
and its smaller root is `t₀`. It has positive value at zero and value `-4/9` at `t=1/3`,
so `0<t₀<1/3<sqrt(2)-1`.

At `t=1/3`, dividing `-4/9` by `250(1+1/9)` gives the previous difference `-1/625`. At
`t=t₀`, (1) is equality and this argument is unresolved; no feasibility assertion is
made at the threshold.

Reflection in `y=q/2` preserves the left segment, swaps the anchors, and maps an ordered
pair `(t₁,t₂)` to `(-t₂,-t₁)`. It therefore proves the equal negative-angle exclusion as
well. Reflection in `x=q/2` transfers the results between the two outer segments.
Equivalently, equal signed half-tangents with `|t|>t₀` are excluded on either segment.

## A Necessary Inequality for Unequal Positive Angles

Let the two positive folded angles be `θ₁,θ₂`, with

```text
u_i = (c_i,s_i),   w_i = (-s_i,c_i).
```

The same normal-cut argument leaves only `w₁` and `w₂` as possible ordered separators.
For a candidate `w_j`, where `j∈{1,2}`, define

```text
K = c_j c₂+s_j s₂ = cos(θ₂-θ_j) > 0,
J = c_j s₂-s_j c₂ = sin(θ₂-θ_j).
```

The upper owner’s support in this direction is `H₂(w_j)=(K+|J|)/2`. For its center
offset `X=C₂-m`, the tube slab and branch clip give

```text
u₂·X ≤ 1/2+ℓc₂/2+δ,
w_j·X ≥ (K+|J|)/2-ℓs_j/2-δ.
```

Use `(1,0)=(c_j u₂-s₂ w_j)/K` and `c_j=c₂K+s₂J` to obtain

```text
X_x ≤ (c₂-s₂)/2+ℓ/2+δ(c_j+s₂)/K+s₂(J-|J|)/(2K)
    ≤ (c₂-s₂)/2+ℓ/2+δ(c_j+s₂)/K.
```

Combining this with container containment proves the necessary condition

```text
s₂ ≤ A+δ(c_j+s₂)/K                                  (3)
```

for either surviving normal.
The absolute sine term has the displayed nonpositive sign, so dropping it safely weakens
the condition. At equal angles, (3) becomes (1).

## Proof of the Broad Same-Sign Band

Put `T=1997/6000=1/3-1/2000`, and suppose `t₁,t₂∈I₊`. The function `c(t)` decreases and
`s(t)` increases on the positive folded range.
Between `T` and `1/3`, their derivatives have absolute value at most two.
Since `c(1/3)=4/5` and `s(1/3)=3/5`,

```text
c(T) > 4/5,
c_i ≤ c(T) ≤ 801/1000,
s_i ≥ s(T) ≥ 599/1000.
```

Let `θ_low=2 arctan T`. For either candidate `w_j`, the two angles lie in `[θ_low,π/4]`,
so

```text
K = cos(θ₂-θ_j)
  ≥ cos(π/4-θ_low)
  = (c(T)+s(T))/sqrt(2)
  > (1399/1000)/sqrt(2)
  > 989/1000.
```

The final comparison is exact: `1399²-2·989²=959>0`.

Rewrite condition (3) as `F≤0`, where

```text
F = (s₂-59/100)K-δ(s₂+c_j).
```

On the stated bounds, `F` increases with `K` because `s₂-59/100≥9/1000>0`; it increases
with `s₂` because `K≥989/1000>δ`; and it decreases with `c_j`. Consequently,

```text
F ≥ (599/1000-59/100)(989/1000)
     -(3/500)(599/1000+801/1000)
  = 501/1000000 > 0.
```

This contradicts the necessary inequality for both remaining candidate normals.
It proves the positive-band theorem, including its endpoints.
Reflection in `y=q/2` and exchange of the anchor order give `I₋`; reflection in `x=q/2`
gives both bands on the right outer segment as well.
In particular, the simpler bands `[1/3,sqrt(2)-1]` and `[1-sqrt(2),-1/3]` are excluded.

## A Closed Cell Around `(1/3,1/3)`

**Theorem.** Every ordered pair in the real closed cell

```text
t₁,t₂ ∈ [1997/6000,2003/6000]
       = [1/3-1/2000,1/3+1/2000]
```

is impossible for two owners of the same outer segment.
This cell lies inside the positive band and remains an exact control.
The following local bounds give a separate exact contradiction margin for this control.

Put `ε=1/2000`. On this interval, which is contained in `[0,1/2]`, the rational
orientation functions obey

```text
c'(t) = -4t/(1+t²)²,           |c'(t)|≤2,
s'(t) = 2(1-t²)/(1+t²)²,       |s'(t)|≤2.
```

Their values at `1/3` are `4/5` and `3/5`. Thus throughout the closed cell,

```text
s₂ ≥ 3/5-2ε = 599/1000,
c_j+s₂ ≤ 7/5+4ε = 701/500.
```

The exact half-tangent identity gives, for either `j`,

```text
K = 1-2(t₂-t_j)²/((1+t₂²)(1+t_j²))
  ≥ 1-8ε²
  = 499999/500000.
```

Therefore the right side of (3) is at most

```text
59/100+(3/500)(701/500)/(499999/500000)
 = 59/100+4206/499999
 < 599/1000
 ≤ s₂.
```

The strict comparison is rational: `4206000<4499991`. It contradicts (3) for both `j=1`
and `j=2`. All other candidate normals have already been excluded, completing the proof.
The difference between the lower bound for `s₂` and the upper bound in (3) is at least
`293991/499999000>0`, including on the cell boundary.

Horizontal reflection and exchange of the anchor order also exclude the closed cell

```text
t₁,t₂ ∈ [-2003/6000,-1997/6000].
```

These closed-cell conclusions follow from the inequalities above for every pair in the
cells. The broad-band theorem excludes the larger same-sign regions stated at the top.
Mixed-sign angle pairs are outside that theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
