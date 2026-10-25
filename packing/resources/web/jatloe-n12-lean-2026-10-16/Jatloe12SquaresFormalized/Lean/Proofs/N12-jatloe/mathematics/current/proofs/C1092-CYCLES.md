# C1092: a continuous certificate for the enlarged negative cycle

## Status and scope

The scalar theorem below is proved. It proves the exact candidate `Phi` in
`01-C1092-CYCLIC-INEQUALITIES.md`, with horizontal bound `L=11/10`, throughout
`0 <= h <= 1/8`. In particular it includes both difficult negative ranges
`[3/29,13/115]` and `[13/115,7/57]`. It uses two broad regimes, separated at
`h=1/10`, and no subdivision into small angle intervals.

Its application to actual squares requires the geometric entrance stated in
Section 2 of that handoff, or another entrance proving the same upper and
lower support inequalities. The scalar theorem does not assume that entrance
follows from the original C1092 markers. This distinction matters: proving the
scalar theorem alone removes the enlarged negative terminal inequalities,
conditionally on their entrance; it does not by itself replace the historical
incoming geometric deductions.

All numbers are exact rational numbers.

## 1. The scalar theorem

For `|t| <= 1/8` set

    c(t) = (1-t^2)/(1+t^2),   s(t) = 2t/(1+t^2).

Let `0 <= h <= 1/8`, let `q_0=h`, and let `-h <= q_i <= h` for
`i=1,2,3`. Indices are cyclic modulo four. Put

    Delta(u,v) = |u-v|,
    G(u,v) = Delta(u,v)(1+uv-Delta(u,v))
             / ((1+u^2)(1+v^2)).

For `0 <= q <= h` define

    D(h,q) = [2(h-q)^2(1+q+2q^3)
              +8(h-q)(q^2+q^4)+4(q^3+q^5)]
             / [(1+h^2)(1+q)(1+q^2)].

For `q=-r`, `0 <= r <= h`, define

    D(h,-r) = [2h(h-r)+4h^2 r+(1+h^2)r^2]
              / [(1+h^2)(1+r)].

The two formulas agree at zero, and each is nonnegative. Define

    Phi = sum_i {G(q_i,q_(i+1))
                 -(11/10)[max(c(q_i),c(q_(i+1)))-c(h)]}
          +sum_i min(q_i,0)+sum_i D(h,q_i).

**Theorem.** `Phi >= 0`.

### 1.1. Separate the edge cost from the vertex cost

Use the exact identity

    max(A,B) = (A+B+|A-B|)/2.

After summing around the cycle, each vertex occurs in two edges. Therefore

    Phi = sum_i K(q_i,q_(i+1)) + sum_i f_h(q_i),

where

    K(u,v) = G(u,v) -(11/20)|c(u)-c(v)|,
    f_h(q) = D(h,q) -(11/10)[c(q)-c(h)] +min(q,0).

This identity is the useful correlation that the earlier estimate discarded.
The horizontal transport penalty is shared equally between a vertex cost and
an edge variation cost.

### 1.2. Two uniform bounds for the edge cost

Since

    |c(u)-c(v)| = 2|u-v||u+v|/[(1+u^2)(1+v^2)],

we have

    K(u,v) = |u-v| [1+uv-|u-v|-(11/10)|u+v|]
              / [(1+u^2)(1+v^2)].

For fixed `v`, the function

    |u-v| +(11/10)|u+v| -uv

is convex in `u`; for fixed `u`, it is convex in `v`. Its maximum on the
square `[-h,h]^2` is consequently achieved at a corner. The four corner
values give

    |u-v| +(11/10)|u+v| -uv
        <= max(2h+h^2, (11/5)h-h^2).

This argument is also valid at `u=v` and at either zero; no division by
`|u-v|` is needed.

If `h <= 1/10`, both terms on the right are at most `21/100`. Also
`(1+u^2)(1+v^2) <= (101/100)^2`. Hence

    K(u,v) >= (7900/10201)|u-v| >= (3/4)|u-v|.       (1)

If `h <= 1/8`, the two corner expressions are at most `17/64`:
the first increases to `17/64`, and the second increases to
`83/320 <= 17/64`. The denominator is at most `(65/64)^2`. Thus

    K(u,v) >= (3008/4225)|u-v| >= (7/10)|u-v|.      (2)

Both final rational comparisons are strict, but the weak versions suffice.

### 1.3. Vertex bound for `0 <= h <= 1/10`

We prove

    f_h(q) +(1/2)(h-q) >= 0.                      (3)

If `q >= 0`, use `D>=0` and

    c(q)-c(h) = 2(h-q)(h+q)/[(1+h^2)(1+q^2)].

The left side of (3) is at least

    (h-q)[1/2 -(11/5)(h+q)]
      >= (h-q)[1/2 -(22/5)h]
      >= (3/50)(h-q) >= 0.

If `q=-r <= 0`, then

    min(q,0)+(h-q)/2 = -r+(h+r)/2 = (h-r)/2.

The same calculation with `r` instead of `q` gives the lower bound
`(3/50)(h-r) >= 0`. This includes `r=h` and all zero cases.

### 1.4. Nonnegative vertex bound for `h <= 1/8`

For `0 <= q <= h <= 1/8`, we prove

    f_h(q) +(7/15)(h-q) >= 0.                     (4)

Put `z=h-q >=0` and `B=(1+h^2)(1+q^2)>0`. The displayed exact formula
for `D` gives

    B D(h,q)
       >= 2z^2 + 8z q^2/(1+q)
                    +4q^3(1+q^2)/(1+q).

Indeed the first summand follows from
`1+q+2q^3 >= 1+q`; the second follows by dropping its nonnegative
extra factor `q^2`; the last summand is retained exactly. Also `B>=1`.
It follows that

    B[f_h(q)+(7/15)z]
      >= z[7/15 -h/5 -(21/5)q +8q^2/(1+q)]
           +4q^3(1+q^2)/(1+q).                  (5)

The bracket decreases when `h` increases. It also decreases with `q` on
`[0,1/8]`, since its derivative with respect to `q` is

    -21/5 + 8q(2+q)/(1+q)^2 < 0.

For example `q(2+q)/(1+q)^2 = 1-(1+q)^(-2) <= 17/81` makes this
strict inequality immediate. Its minimum is therefore at `h=q=1/8`,
where its value is exactly

    7/15 -11/20 +1/9 = 1/36.

Consequently the right side of (5) is nonnegative. This proves (4),
including `q=0`, `q=h`, and `h=0`.

### 1.5. Negative vertex bound for `1/10 <= h <= 1/8`

For `q=-r`, `0 <= r <= h`, we prove the stronger estimate

    f_h(-r)+(7/15)(h+r)
        >= (7/8)(r-1/10)^2 +11/2400 > 0.          (6)

Since

    (1+h^2)(1+r) <= (65/64)(9/8) =585/512 <8/7,
    1+r <= 9/8 <8/7,

the exact negative formula implies

    D(h,-r) >= (7/4)h(h-r)+(7/2)h^2 r+(7/8)r^2.

Furthermore

    (11/10)[c(r)-c(h)]
       <= (11/5)(h-r)(h+r).

Since `-r+(7/15)(h+r)=(7/15)(h-r)-r/15`, these inequalities give

    f_h(-r)+(7/15)(h+r)
      >= (h-r)[7/15 -(9/20)h -(11/5)r]
          +r[-1/15 +(7/2)h^2 +(7/8)r].           (7)

The first bracket is at least

    7/15 -(53/20)(1/8) =13/96 >=2/15.

The constant part of the second bracket is at least

    -1/15 +(7/2)(1/10)^2 =-19/600.

Using also `h>=1/10`, the right side of (7) is at least

    1/75 -(33/200)r +(7/8)r^2
      >= 1/75 -(7/40)r +(7/8)r^2
       = (7/8)(r-1/10)^2 +11/2400.

This proves (6) without further subdivision or an omitted endpoint.

### 1.6. The four-cycle closes

Write `V=sum_i|q_i-q_(i+1)|`. For each `i`, the two paths in the
four-cycle from vertex zero to vertex `i` each have variation at least
`h-q_i`; together they use every edge. Hence

    h-q_i <= V/2.

Since `q_0=h`, summing the other three inequalities gives

    sum_i(h-q_i) <= (3/2)V.                       (8)

If `h<=1/10`, (1), (3), and (8) imply

    Phi >= (3/4)V -(1/2)sum_i(h-q_i) >=0.

If `1/10<=h<=1/8`, (2), (4), (6), and (8) imply

    Phi >= (7/10)V -(7/15)sum_i(h-q_i) >=0.

The intervals overlap at `h=1/10`. This completes the theorem.

## 2. Conditional application to the actual negative square cycle

Suppose an actual four-sector packing supplies the following inequalities,
with `1<a`, `q_0=h`, `|q_i|<=h<=7/57`, local centers
`C_i=(2-X_i,2-Y_i)`, and
`J_i=(2+Y_(i+1),2-X_(i+1))`:

1. The forced central faces and actual boundary support give

       F_i <= 1+max(-q_i,0)-D(h,q_i),
       F_i=(c(h)+s(h))X_i+(c(h)-s(h))Y_i.

2. A forward first normal of an endpoint separates each adjacent pair,
   and the actual displacements satisfy

       0 <= (J_i-C_i)_x <= 11/10,
       (J_i-C_i)_y <=0.

These statements are the support consequences of the geometric entrance in
the handoff. They retain the actual common side `a`; no independent side
variables or point substitutes for the boundary squares are allowed.

If the selected normal has parameter `r_i` equal to one of `q_i,q_(i+1)`,
the two actual square supports sum to `a[1+G(q_i,q_(i+1))]`.
Because `a>=1` and `G>=0`, this is at least `a+G`. Transporting this normal
to `n(h)=(c(h),-s(h))` gives

    n(h)·(J_i-C_i)
       >= a+G(q_i,q_(i+1))
          -(11/10)[max(c(q_i),c(q_(i+1)))-c(h)].

The vertical transport term is nonnegative because `s` increases on the
range, `r_i<=h`, and the vertical displacement is nonpositive. Thus it may
be discarded. The equality-safe support and transport argument also covers
zero angles, equal endpoint angles, and either choice of normal source.

The exact cyclic identity

    sum_i F_i = sum_i n(h)·(J_i-C_i)

and the upper bounds in item 1 now imply

    0 >= 4(a-1)+Phi.

The scalar theorem gives `Phi>=0`, contradicting `a>1`.

Therefore the entrance excludes the whole negative maximal-angle range
`0<=h<=7/57`, including the formerly difficult terminal labels 50 and 51.
The scalar result even allows `h<=1/8`; applying that slight extension to
actual squares still requires checking their geometric entrance on that
extended domain.

## 3. Why the new estimate succeeds

The old proof charged the maximum endpoint cosine independently on every
edge and then weakened every central upper bound to a common coarse value.
The exact maximum identity splits that cost into a vertex term and a
variation term. The retained deficits `D` then pay the vertex term
continuously. A single elementary fact about an anchored four-cycle,
`sum(h-q_i)<=3V/2`, supplies the remaining relation.

The enlarged negative proof consists of an exact decomposition, one convex
corner bound, two vertex estimates, and one cycle inequality. It has no
long rational interval tree and no hidden finite calculation.
