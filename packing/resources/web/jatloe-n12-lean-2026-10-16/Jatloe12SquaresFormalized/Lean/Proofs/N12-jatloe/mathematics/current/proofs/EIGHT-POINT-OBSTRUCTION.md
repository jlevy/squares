# An eight-point obstruction for a square of side greater than one

**New mathematical simplification, 14 October 2026 (America/New_York).**
All terminating decimals below are exact rational numbers. This is a self-contained
lemma, not an angle sample, a numerical infeasibility claim, or a Lean theorem.

## Theorem

An open square of side `a > 1`, with arbitrary position and orientation, cannot
strictly contain both

\[
 M=(.65,.35),\qquad H=(0,.26)
\]

and exclude all six points

\[
 O=(0,0),\quad D=(.5,0),\quad K=(0,1),\quad
 X=(.27,-.04),\quad T_0=(.44,1),\quad T_1=(.74,1).
\]

“Exclude” means outside the **open** square; an excluded point may lie on its
boundary. There is no container assumption, no center assumption, no upper bound
on `a`, and no hypothesis relating this square's angle to another square's angle.

## Two elementary bounds

For `c >= s >= 0`, `c²+s²=1`, one has `c>0`, `c<=1` and `c+s<=sqrt(2)`.
If `0<=p<=q`, then

\[
 pc+qs=\tfrac12(p+q)(c+s)+\tfrac12(p-q)(c-s)
       \le (p+q)/\sqrt2.                                      \tag{A}
\]

For any nonnegative `p,q`, Cauchy–Schwarz gives

\[
 pc+qs\le\sqrt{p^2+q^2}.                                    \tag{B}
\]

Relabeling the four faces of one physical square gives one of the two frames
below. This does not reflect the physical configuration. Let `U,V` be its lower
band endpoints and `A=U+a`, `B=V+a` its upper endpoints. Thus an interior point
satisfies both strict band inequalities. Equal projected coordinates inherit
strictness from an interior comparison point.

## 1. Nonnegative canonical angle

Take `u=(c,s)`, `v=(-s,c)` with `c>=s>=0` and `c²+s²=1`.

**Step 1: two elementary face caps.** At `D`, the lower `u` inequality follows
from `H`, the upper `u` inequality from `M`, and the upper `v` inequality from
`H`. The relevant positive differences are

\[
 u(D)-u(H)=.5c-.26s>0,\quad u(M)-u(D)=.15c+.35s>0,
 \quad v(H)-v(D)=.26c+.5s>0.
\]

Consequently `D` can only exit through the lower `v` face:

\[
 V\ge-.5s.                                                   \tag{1}
\]

At `K`, the two lower inequalities follow from `H`; the upper `u` inequality
follows from `M` because `u(M)-u(K)=.65(c-s)>=0`. Hence

\[
 B\le c.                                                     \tag{2}
\]

**Step 2: use the excluded origin.** Both upper inequalities at `O` follow
from `H`. Therefore `U>=0` or `V>=0`. The latter, together with (2), would give
`a=B-V<=c<=1`. It follows that

\[
 U\ge0.                                                      \tag{3}
\]

**Step 3: the two top points.** Both lower inequalities at `T_1` follow from
`H` in the `u` coordinate and `M` in the `v` coordinate:

\[
 u(T_1)-u(H)=.74c+.74s>0,\qquad
 v(T_1)-v(M)=.65c-.09s>0.
\]

If `T_1` exited through upper `v`, then (1) would give
`a<=c-.24s<=1`. Therefore it exits through upper `u`, and

\[
 A\le.74c+s,\qquad a\le.74c+s.                               \tag{4}
\]

Both lower inequalities at `T_0` likewise follow from
`u(T_0)-u(H)=.44c+.74s>0` and `v(T_0)-v(M)=.65c+.21s>0`.
An upper-`v` exit would give `a<=c+.06s` using (1). Combining four copies
of this bound with (4) gives

\[
 5a\le4.74c+1.24s\le\sqrt{24.0052}<5,
\]

which contradicts `a>1`. Thus

\[
 A\le.44c+s,\qquad a\le.44c+s.                               \tag{5}
\]

**Step 4: the lower-right point.** Both upper inequalities at `X` hold, since

\[
 u(M)-u(X)=.38c+.39s>0,\qquad v(H)-v(X)=.30c+.27s>0.
\]

An exit through lower `u` would give `U>=.27c-.04s`; then (5) and (A) give

\[
 a\le.17c+1.04s\le1.21/\sqrt2<1.
\]

So `X` exits through lower `v`, giving `V>=-.27s-.04c`. With (2),

\[
 a\le1.04c+.27s.                                             \tag{6}
\]

Adding (5) and (6) and applying (B) now yields

\[
 2a\le1.48c+1.27s\le\sqrt{3.8033}<2,
\]

again impossible.

## 2. Nonpositive canonical angle

Take `u=(c,-s)`, `v=(s,c)` with the same `c>=s>=0`, `c²+s²=1`.

**Step 1: the origin and upper corner.** At `O`, lower `u` follows from `H`,
upper `u` from `M` because `.65c-.35s>0`, and upper `v` from `H`. Thus

\[
 V\ge0.                                                      \tag{7}
\]

At `K`, upper `u` follows from `H` and lower `v` follows from `H`. An upper-`v`
exit would give `B<=c`, contrary to `a>1` and (7). Hence

\[
 U\ge-s.                                                     \tag{8}
\]

**Step 2: four alternatives collapse to one.** At `D`, lower `u` follows
from `H` and upper `v` from `M`, so

\[
 A\le.5c\quad\hbox{or}\quad V\ge.5s.                         \tag{9}
\]

At `T_0`, upper `u` follows from `M`, and lower `v` follows from `M` because
`.65c-.21s>0`. Therefore

\[
 U\ge.44c-s\quad\hbox{or}\quad B\le c+.44s.                  \tag{10}
\]

Three of the four combinations of (9) and (10) are impossible:

* `V>=.5s` and `B<=c+.44s` give `a<=c-.06s<=1`.
* `A<=.5c` and `U>=.44c-s` give
  `a<=.06c+s<=1.06/sqrt(2)<1` by (A).
* `V>=.5s` and `U>=.44c-s`, together with strict ownership of `H`, give
  `25s<13c` and `22c<37s`. Thus `550c<925s<481c`, impossible since `c>0`.

The remaining combination is

\[
 A\le.5c,\qquad B\le c+.44s.
\]

By (8), this also gives

\[
 a\le.5c+s.                                                  \tag{11}
\]

**Step 3: use the lower-right point.** At `X`, lower `u` and upper `v`
follow from `H`, with strict differences `.27c+.30s` and `.30c-.27s`.
An upper-`u` exit, together with (8), would give

\[
 a\le.27c+1.04s\le1.31/\sqrt2<1.
\]

Thus `V>=.27s-.04c`. The upper-`v` cap from Step 2 gives

\[
 a\le1.04c+.17s.                                             \tag{12}
\]

Adding (11) and (12) yields the final contradiction

\[
 2a\le1.54c+1.17s\le\sqrt{3.7405}<2.
\]

Both signs have been excluded. The axis `s=0` and diagonal `s=c` were included;
none of the arguments divided by `s` or `c-s`. All face exclusions were weak,
so every legitimate tangency is included. This proves the theorem. ∎

## Exact arithmetic checks

The seven strict squared comparisons used above are

```
4.74² + 1.24² = 24.0052 < 25
1.21² = 1.4641 < 2
1.48² + 1.27² = 3.8033 < 4
1.06² = 1.1236 < 2
1.31² = 1.7161 < 2
1.54² + 1.17² = 3.7405 < 4
550 > 481
```

`../checks/check_new_obstruction.py` checks these comparisons, the projection
differences, and the actual C1089 coordinate map with rational arithmetic.
That program is an arithmetic audit of this written proof, not a replacement
for its geometric reasoning or a proof-assistant verification.
