# An outward square with a longer actual wall segment

This theorem removes the corner-point exclusion from the outward strict-point theorem. Every decimal is exact. A square is open, a>1, and exclusions allow tangency. No container wall or side upper bound is required.

## 1. Statement

**Theorem.** Let Q be an open square of side a>1. Suppose Q strictly owns

\[
M=(2.35,2.35),\qquad A=(3,2.26),\qquad B=(3,2.4),
\]

and excludes

\[
G=(2.26,2),\quad R=(3.086,2),\quad H=(3.086,3),
\]

and the whole segment

\[
\mathcal S=[2.26,2.86]\times\{3\}.
\]

Then

\[
K=(2.46,1.99)\in Q\quad\text{strictly}.
\]

In particular there is no hypothesis that (3,3) is excluded or belongs to an actual corner square. The longer segment supplies the required support.

## 2. Every nonpositive canonical angle is impossible

Write P=(3,3). If P is excluded from Q, reflect the whole local configuration in y=2 and apply Theorem 6 of `C981-WALL-CYCLES.md`. Its strict anchors are the reflected M and B, its isolated exclusions are the reflected P,R,G, and its required segment [2.26,2.8]×{1} is contained in the reflected 𝒮. That theorem excludes every nonnegative canonical angle after reflection. Thus it excludes every nonpositive canonical angle of the original square, including the axial and diagonal representatives.

It remains to check that owning P cannot restore a nonpositive angle. Translate by (−2,−2), so the points used in this check are

\[
M=(.35,.35),\quad P=(1,1),\quad
T=(.86,1),\quad R=(1.086,0).
\]

Use canonical coordinates u=cx−sy,v=sx+cy, with c≥s≥0,c²+s²=1, and strict bands U<u<U+a,V<v<V+a. Suppose P is strict in Q. The excluded T has both upper bands strictly from P (the v-coordinate can be equal when s=0, which still gives a strict upper band). Its lower-v band follows from M, since

\[
v(T)-v(M)=.51s+.65c>0.
\]

It must therefore fail lower-u:

\[
U\ge .86c-s.
\]

Since M is strict, this implies

\[
.35c-.35s>.86c-s,\qquad s/c>51/65. \tag{1}
\]

Now R has strict lower-u from M and strict upper-v from P. Its lower-v band is also strict, because

\[
v(R)-v(M)=.736s-.35c>0
\]

by (1). Hence R must fail upper-u, and

\[
U+a\le1.086c.
\]

The two u-face bounds imply

\[
a\le.226c+s\le\frac{1.226}{\sqrt2}<1.
\]

The middle inequality follows because .226 cos θ+sin θ increases throughout 0≤θ≤π/4; the last follows from 1.226²=1.503076<2. This contradiction includes s=0, which was already impossible in (1).

Thus a square satisfying the theorem must have a strictly positive canonical angle. The dichotomy was exhaustive: a point is either strictly owned or excluded, with boundary points assigned to the latter case.

## 3. The positive-angle forced faces

Keep the translated coordinates and now use

\[
u=cx+sy,\quad v=-sx+cy,\quad c\ge s>0.
\]

The data are

\[
M=(.35,.35),\ A=(1,.26),\ G=(.26,0),\ R=(1.086,0),
\]

\[
F=(.26,1),\ T=(.86,1),\ H=(1.086,1),\ K=(.46,-.01).
\]

The point G has both upper bands strict from M, and so it fails lower-u or lower-v. Suppose it fails lower-v. The point F has strict upper-u from A and strict lower-v from M. If F failed upper-v, its v-separation from G would give a≤c≤1. Hence F would fail lower-u. The point T has both lower bands strictly from M. If T failed upper-v, its v-separation from G would give a≤c−.6s≤1. Therefore T would fail upper-u. Their two u-face bounds would give a≤.6c<1. This contradiction proves

\[
U\ge.26c. \tag{2}
\]

At R the lower-u band is strict from M and the upper-v band is strict from A. An upper-u exclusion would combine with (2) to give a≤.826c<1. Therefore

\[
V\ge-1.086s. \tag{3}
\]

At H both lower bands are strict from A. An upper-v exclusion would combine with (3) to give a≤c≤1. Therefore

\[
U+a\le1.086c+s. \tag{4}
\]

Equations (2) and (4) imply

\[
1<a\le.826c+s\le.826+s,\qquad s>.174. \tag{5}
\]

These are weak face inequalities at excluded points, obtained from strict comparisons with the owned anchors. No excluded endpoint has been assumed to be a positive distance from a face.

## 4. The target's four strict bands

The two upper bands of K follow directly from A and M:

\[
u(A)-u(K)=.54c+.27s>0,
\qquad
v(M)-v(K)=.36c+.11s>0.
\]

The point T has both lower bands strict from M, so it fails an upper band. If it fails upper-u, then

\[
u(T)-u(K)=.40c+1.01s
\le\frac{1.41}{\sqrt2}<1<a.
\]

The middle inequality again follows by monotonicity on the canonical interval, and 1.41²=1.9881<2. Thus K's lower-u band is strict in this alternative.

If T fails upper-v, then V+a≤c−.86s. With (3),

\[
1<a\le c+.226s.
\]

For the positive half-angle parameter t=s/(1+c), the last strict inequality implies t<.226=113/500. The function .626 cos θ+1.01 sin θ is increasing throughout the canonical interval. At that rational half-angle its exact value is

\[
.626c+1.01s
=\frac{131318303}{131384500}<1,
\]

whose denominator exceeds the numerator by 66197. Hence

\[
u(H)-u(K)=.626c+1.01s<1<a.
\]

Together with (4), this also gives the strict lower-u band of K.

For its lower-v band, if s/c≥1/2 then compare with A:

\[
v(K)-v(A)=.54s-.27c\ge0.
\]

Strict ownership of A supplies the band, including equality in the displayed increment. If s/c<1/2, T cannot fail upper-u: (2) would imply

\[
a\le.6c+s<\frac{2.2}{\sqrt5}<1,
\]

because .6 cos θ+sin θ is increasing up to θ=arctan(1/2), and 2.2²=4.84<5. Thus T fails upper-v. Now (5) gives

\[
v(T)-v(K)=1.01c-.40s
<1.01-.40(.174)=.9404<1<a.
\]

The upper-v face at T therefore implies V<v(K). This establishes the last strict band. All angles, zero-angle alternatives, diagonal representatives, endpoint equalities, and segment tangencies have been included. The theorem is proved.
