# C702: a strict point in the southwest central square

This chapter proves an all-orientation consequence in the last C702 ownership configuration. Every decimal below is an exact terminating rational. Owned points are strictly inside their actual open square; excluded points may lie on its boundary. No numerical angle sampling or center enclosure is used.

Together with Theorem N in C702-N-STRICT-POINT.md, this gives a complete shared-point contradiction for the last C702 alternative. The earlier reduction in C702-CONTINUOUS-REDUCTION.md handles the other alternatives.

## 1. The point theorem

**Theorem 1.** Let A be an open square of side a>1. Suppose A strictly owns

\[
M=(1.65,1.65),\quad P=(2,1.74),\quad D=(1.74,2),
\quad E=(1.5,2),\quad F=(2,1.5).
\]

Suppose it excludes

\[
L=(1,1.65),\quad B=(1.65,1),\quad
N=(1.65,2.35),\quad R=(2.35,1.65),
\]

and the **whole segment**

\[
S=[K,R],\qquad K=(2.05,2.05).
\]

Then A strictly owns

\[
\boxed{X=(1.30,1.93)}.
\]

The segment hypothesis concerns one actual foreign square in the application. Excluding its endpoints separately would be a weaker hypothesis and is not substituted for it.

### 1.1. Two forced lower faces

Use first the nonnegative canonical frame

\[
u=(c,s),\qquad v=(-s,c),\qquad c\ge s\ge0,\qquad c^2+s^2=1,
\]

and write U,V for the lower band coordinates of A.

The point B has both upper bands strict by the owned M. Suppose B were lower-u, so U≥u(B). Both lower bands of N are strict by M. Its upper u-band would also be strict, since

\[
u(N)-u(B)=1.35s\le1.35/\sqrt2<1<a.
\]

Thus N would be upper-v. At R, the lower u-band is strict by M and the upper v-band is strict by D:

\[
v(D)-v(R)=.61s+.35c>0.
\]

Furthermore

\[
u(R)-u(B)=.7c+.65s
\le\sqrt{.7^2+.65^2}=\sqrt{.9125}<1<a,
\]

so its upper u-band would also be strict. Hence R would have to be lower-v. These two v-face bounds imply

\[
a\le v(N)-v(R)=.7(c+s)\le.7\sqrt2<1,
\]

a contradiction. Therefore

\[
V\ge c-1.65s. \tag{1}
\]

The point L has its upper u-band and lower v-band strict by M. An upper-v exclusion would combine with (1) to give

\[
a\le v(L)-v(B)=.65(c+s)<1.
\]

Consequently

\[
U\ge c+1.65s. \tag{2}
\]

For the negative canonical frame

\[
u=(c,-s),\qquad v=(s,c),\qquad c\ge s\ge0,
\]

apply the coordinate exchange (x,y)↦(y,x) to this face argument. Its hypotheses are invariant: P and D, E and F, L and B, and N and R exchange. The segment S was not used. The resulting forced faces are

\[
U\ge c-1.65s=u(L),\qquad V\ge c+1.65s=v(B). \tag{3}
\]

### 1.2. Two alternatives from the whole foreign segment

Put w=(.8,.6). The segment S lies on w·z=2.87. A square and a disjoint closed segment can be weakly separated along a square-edge normal u or v, or along the segment normal w. This statement includes tangency: the difference of the closed square and the segment has only the corresponding three edge directions. Its supporting inequalities determine whether the origin lies in its interior. If it did, the open square would meet the segment. Thus one of the stated axes supplies a weak separation.

The direction placing the whole square above the segment in its u-coordinate is impossible: K is strictly above the lower u-face by comparison with E in either canonical sign. The corresponding v-direction is impossible by comparison with F in the positive frame or M in the negative frame. The direction placing A above the segment in w is impossible because the owned M has w·M=2.31<2.87.

In the positive frame, separation with A below the segment in v is impossible, since

\[
v(D)-v(R)=.61s+.35c>0.
\]

In the negative frame, it would imply V+a≤v(R); (3) then gives

\[
a\le v(R)-v(B)=.65c+.7s\le\sqrt{.9125}<1.
\]

Therefore at least one of these alternatives holds:

\[
U+a\le u(K), \tag{4}
\]

or

\[
\operatorname{upper}_A(w)\le2.87. \tag{5}
\]

The actual first separating inequality may be stronger, using the minimum u-coordinate of the two segment endpoints. Only (4) is needed.

### 1.3. Positive canonical angles

The upper u-band of X is strict by E:

\[
u(E)-u(X)=.20c+.07s>0.
\]

Its lower v-band is strict by F:

\[
v(X)-v(F)=.70s+.43c>0.
\]

Its upper v-band is strict by (1), since

\[
v(X)-V\le v(X)-v(B)
=.93c+.35s
\le\sqrt{.93^2+.35^2}=\sqrt{.9874}<1<a.
\]

If (4) holds, the lower u-band follows from

\[
u(K)-u(X)=.75c+.12s\le\sqrt{.5769}<1<a.
\]

Suppose (5) holds. If s/c≥1/11, K has its upper v-band strict by E, because

\[
v(E)-v(K)=.55s-.05c\ge0.
\]

Both its lower bands were checked above. Since K is excluded, it must then be upper-u, giving (4).

It remains to consider s/c<1/11. The frame components of w are

\[
r=.8c+.6s>0,\qquad t=.6c-.8s>0.
\]

If X failed its lower u-band, U≥u(X). Strict ownership of E and a>1 give

\[
\operatorname{upper}_A(w)=r(U+a)+t(V+a)
>r(u(X)+1)+t\,v(E).
\]

The last expression minus 2.87 is exactly

\[
.8c+.6s+.118s^2-.176cs-.63. \tag{6}
\]

Here c>11/\sqrt{122}>11/12 and (.6−.176c)s≥0, so (6) is greater than .8(11/12)−.63>0. This contradicts (5) and proves the final strict band.

### 1.4. Negative canonical angles

The upper u-band of X is strict by E:

\[
u(E)-u(X)=.20c-.07s\ge.13c>0.
\]

Its upper v-band is strict by D:

\[
v(D)-v(X)=.44s+.07c>0.
\]

If (4) holds, strict ownership of F forces s/c<1/11; otherwise

\[
u(F)-u(K)=.55s-.05c\ge0
\]

would contradict (4). In this range the lower u-band follows from

\[
u(K)-u(X)=.75c-.12s\le.75<1<a,
\]

and the lower v-band is strict by M:

\[
v(X)-v(M)=.28c-.35s>0.
\]

Now assume (5). The frame components of w are

\[
r=.8c-.6s>0,\qquad t=.8s+.6c>0.
\]

If X failed its lower v-band, then V≥v(X), U≥u(L) by (3), and a>1 give

\[
\operatorname{upper}_A(w)>r\,u(L)+t\,v(X)+r+t.
\]

The right side minus 2.87 is exactly

\[
1.4c+.2s+.072s^2+.404cs-.912. \tag{7}
\]

It is positive, since c≥1/\sqrt2>.7, so 1.4c>.98>.912, and the remaining terms are nonnegative. This contradicts (5).

If X failed its lower u-band, use U≥u(X), V≥v(B) from (3), and a>1 to get

\[
\operatorname{upper}_A(w)>r\,u(X)+t\,v(B)+r+t.
\]

The right side minus 2.87 is

\[
1.4c+.2s+.838s^2-.534cs-1.23. \tag{8}
\]

For an exact positivity certificate, put

\[
q=\frac{s}{1+c}\in[0,\sqrt2-1]\subset[0,5/12].
\]

Multiplication of (8) by 500(1+q²)² yields

\[
p(q)=85-334q+446q^2+734q^3-1315q^4.
\]

For z=12q/5∈[0,1], its exact Bernstein expansion is

\[
p(q)=\sum_{j=0}^4\binom4j b_j z^j(1-z)^{4-j},
\]

where

\[
(b_0,b_1,b_2,b_3,b_4)=
\left(85,\frac{1205}{24},\frac{12235}{432},
\frac{112715}{3456},\frac{761525}{20736}\right).
\]

Every coefficient is strictly positive, and the Bernstein basis sums to one. Hence (8)>0 throughout the canonical interval, contradicting (5).

All four bands of X are strict in both canonical signs. Zero angle, both diagonal endpoints, and all permitted tangencies at excluded points are included. This proves Theorem 1. ∎

## 2. Exact C702 owner mapping

The earlier continuous reduction leaves the configuration in which W=Q₇ owns auxiliary 5 at (2,2.26), with exact Q₇ label 65568. Set A=Q₆ and let Q₈ be the actual northwest/left-wall square.

The five strict anchors of Theorem 1 belong to A. The excluded L and B belong to the actual singleton squares Q₁ and Q₀. The point N=(1.65,2.35) is the Q₈ marker, and R=(2.35,1.65) belongs to W.

Apply the half-turn of Theorem A in MERGED-RIGHT-PATTERN-4.md to W. Its strict anchors are

\[
(2.35,2.35),\quad(2,2.26),\quad(2.26,2).
\]

The four reflected exclusions are

\[
(3,2.35),\quad(3,2.26),\quad(2.26,3),\quad(2.35,3).
\]

The first pair comes from the actual upper-right singleton Q₄ and the second from the actual top-right singleton Q₃, using their strict singleton segments. Therefore K=(2.05,2.05) is strictly in W. Since K and R belong to this one actual convex open square, their whole closed segment is strict in W and excluded from A.

Theorem 1 consequently proves

\[
\boxed{(1.30,1.93)\in Q_6}
\]

strictly in the last C702 configuration. Theorem N in C702-N-STRICT-POINT.md proves the same point strictly in the distinct actual Q₈, completing the contradiction. Thus every original C702 auxiliary alternative is excluded continuously.
