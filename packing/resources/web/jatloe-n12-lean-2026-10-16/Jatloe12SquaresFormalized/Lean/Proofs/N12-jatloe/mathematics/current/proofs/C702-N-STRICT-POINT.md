# C702: the northwest square contains the closing point

All terminating decimals in this file denote exact rational numbers. A square is open, its side is a>1, and an excluded point may lie on its boundary. No side upper bound or container wall is used in the theorem below.

## 1. Statement

**Theorem N.** Suppose an open square Q of side a>1 strictly owns

\[
P=(-.086,0),\qquad M=(.65,.35),\qquad H=(0,.26),
\]

and excludes the points and complete segments

\[
D=(.5,0),\qquad K=(0,1),
\]

\[
\mathcal T=[.2,.74]\times\{1\},
\qquad
\mathcal V=[S,L],\quad S=(-.24,-.13),\quad L=(0,-.26).
\]

Then Q strictly contains

\[
Z=(.30,-.07).
\]

The theorem concerns the actual complete segments, including their endpoints. Their exclusion is the only interaction with neighbouring squares required here.

## 2. Coordinate convention and the segment observation

Every square admits one of the two canonical orthonormal coordinate systems

\[
u=cx+sy,\quad v=-sx+cy
\qquad\hbox{or}\qquad
u=cx-sy,\quad v=sx+cy,
\]

where c²+s²=1 and c≥s≥0. In either system write its four strict bands as

\[
U<u<U+a,\qquad V<v<V+a.
\]

Thus an excluded point with three strict bands must fail the remaining band, weakly. Equality at a supporting line is retained throughout. At s=0 the strict owned points P,M force D into both coordinate intervals, a contradiction. We may therefore assume s>0.

We use one elementary segment observation. Suppose a segment joins an excluded point S which fails only the lower-u band to an excluded point L which fails only the lower-v band. Suppose its line has equation

\[
\alpha u+\beta v=k,\qquad \alpha,\beta>0.
\]

If the entire segment is excluded, necessarily

\[
\alpha U+\beta V\ge k. \tag{1}
\]

Indeed, in these coordinates S lies weakly left of u=U and strictly above v=V, while L lies strictly right of u=U and weakly below v=V. Both endpoints are strictly below the upper-v band or left of the upper-u band, respectively. If the corner (U,V) were strictly below the displayed line, the segment would pass through u>U,v>V before reaching L; this portion would also satisfy both upper bands. It would meet the open square. Equality in (1) is exactly the possible corner tangency and is allowed.

## 3. Negative canonical sign

Use u=cx−sy and v=sx+cy, and write τ=s/c.

If τ≤3/7, the excluded point D has all four strict bands directly from P and M: its lower bands exceed those of P, its upper-v coordinate is below that of M, and

\[
u(M)-u(D)=.15c-.35s\ge0.
\]

Consequently

\[
\tau>3/7. \tag{2}
\]

The target Z has strict lower-u and upper-v bands from P and M. Its lower-v band is strict as well, because

\[
v(Z)-v(P)=.386s-.07c>0
\]

by (2). If τ≤5/6, its upper-u band follows from M, since

\[
u(M)-u(Z)=.35c-.42s\ge0.
\]

It remains to treat τ>5/6. Suppose, for a contradiction, that Z fails the upper-u band, so

\[
U+a\le u(Z).
\]

Then K has a strict lower-u band: the function .30c+1.07s is increasing on the canonical interval and hence

\[
u(Z)-u(K)=.30c+1.07s
\le\frac{1.37}{\sqrt2}<1<a.
\]

Together with U≤u(Z)−a, this gives u(K)>U. The upper-u band of K is strict from M, since u(M)−u(K)=.65(c+s)>0, and its lower-v band is strict from H. Therefore the exclusion of K forces

\[
V+a\le c. \tag{3}
\]

On the other hand, L has both strict u bands from P and M: in particular

\[
u(M)-u(L)=.65c-.61s\ge.04c>0.
\]

Its upper-v band is strict from H, so its exclusion forces

\[
V\ge-.26c. \tag{4}
\]

Equations (3)–(4) give

\[
a\le1.26c<\frac{7.56}{\sqrt{61}}<1,
\]

because τ>5/6 implies c<6/√61 and 7.56²=57.1536<61. This contradiction establishes the remaining band of Z. The negative canonical sign is complete.

## 4. Positive sign: a first angle bound from the actual top segment

Now use u=cx+sy and v=−sx+cy. Put A=U+a and B=V+a. The excluded point D has its lower-u, upper-u and upper-v bands strictly from P,M, so

\[
V\ge-.5s. \tag{5}
\]

The point K has strict lower-u and lower-v bands, and its upper-u band follows from

\[
u(M)-u(K)=.65(c-s)\ge0.
\]

Thus

\[
B\le c. \tag{6}
\]

Let T₀=(.2,1), T₁=(.74,1), the endpoints of the excluded top segment. Both endpoints have both lower bands strictly from P. In particular

\[
v(T_1)-v(P)=c-.826s\ge.174c>0.
\]

If T₁ failed upper-v, (5) would give a≤c−.24s<1. Hence T₁ must fail upper-u:

\[
A\le.74c+s. \tag{7}
\]

Suppose τ=s/c≤9/13. Then u(M)−u(T₀)=.45c−.65s≥0, so T₀ must fail upper-v:

\[
B\le c-.2s. \tag{8}
\]

The complete segment exclusion now implies

\[
As+Bc\le1. \tag{9}
\]

To check this directly, if As+Bc>1 then

\[
\frac{c-B}{s}<\frac{A-s}{c}.
\]

By (7)–(8) this is a nonempty interval inside [.2,.74]. Every point (x,1) in that interval has both upper bands strict, and the whole top segment already has both lower bands strict. Such a point would lie in Q, contrary to its exclusion. This also shows why possible line or vertex tangency gives the weak inequality (9).

But M is strict and a>1, so (5) yields

\[
As+Bc>c+.15cs+.35s^2. \tag{10}
\]

The right side is larger than one throughout 0<τ≤9/13. For a complete exact check, set t=s/(1+c). The monotonic relation τ=2t/(1−t²), together with 9/13<400/561, gives 0<t<8/25. The identity

\[
c+.15cs+.35s^2-1
=\frac{t\left(3-6t-3t^2-20t^3\right)}{10(1+t^2)^2}
\]

has positive numerator, since its parenthesized polynomial is decreasing and at t=8/25 equals 367/3125>0. Equations (9)–(10) are contradictory. Therefore

\[
\tau>9/13. \tag{11}
\]

In this sector T₀ cannot fail upper-v: otherwise (5) would give a≤c+.3s, whereas this expression is decreasing for τ>9/13 and at the endpoint equals

\[
\frac{157}{10\sqrt{250}}<1
\quad\left(157^2=24649<25000\right).
\]

Consequently

\[
A\le.2c+s. \tag{12}
\]

## 5. The actual left segment sharpens the angle bound

The point S has both upper bands strictly: its upper-u band follows from P, and its upper-v band follows from H because

\[
v(H)-v(S)=.39c-.24s\ge.15c>0.
\]

It cannot fail lower-v. Such a failure, together with (6), would imply

\[
a\le1.13c-.24s<1.
\]

For example, (11) gives c<13/√250<5/6, so the displayed right side is less than 113/120. Therefore S fails only lower-u.

The point L has both upper bands strictly from M,H, so it fails lower-u or lower-v. We claim it must fail lower-u. If it did not, it would fail only lower-v and would give V≥−.26c. By (6),

\[
a\le1.26c,\qquad c>50/63. \tag{13}
\]

The actual line through S and L has equation

\[
.13x+.24y=-.0624.
\]

Its two coefficients in the present u,v coordinates are

\[
\alpha=.13c+.24s>0,\qquad
\beta=.24c-.13s>0.
\]

The complete exclusion of [S,L] and the segment observation (1) imply

\[
\alpha U+\beta V\ge-.0624.
\]

Combining this with (6), (12), and U=A−a,V=B−a gives

\[
a(.37c+.11s)
\le(.13c+.24s)(.2c+s)+(.24c-.13s)c+.0624
\]

\[
=.3284-.026s^2+.048cs\le.3524=\frac{881}{2500}. \tag{14}
\]

But (11) implies s>9/√250>14/25, while (13) gives c>50/63. Hence

\[
.37c+.11s
>\frac{37}{126}+\frac{77}{1250}
=\frac{881}{2500}+\frac{449}{157500}.
\]

Since a>1, this contradicts (14). This proves the claim: L fails lower-u, and therefore U≥−.26s. With (12),

\[
a\le.2c+1.26s. \tag{15}
\]

The right side is strictly increasing throughout 0≤θ≤π/4. At the rational half-angle t=19/50, where

\[
(c,s)=\left(\frac{2139}{2861},\frac{1900}{2861}\right),
\]

its exact value is 14109/14305<1. Since a>1, (15) forces

\[
t>19/50. \tag{16}
\]

## 6. The target is strict in the positive sign

The lower-u, upper-u, and upper-v bands of Z follow directly from P and M:

\[
u(Z)-u(P)=.386c-.07s>0,
\]

\[
u(M)-u(Z)=.35c+.42s>0,
\]

\[
v(P)-v(Z)=.386s+.07c>0.
\]

For the remaining lower-v band, use (6). The expression 1.07c+.30s is decreasing once τ>9/13. By (16),

\[
c-v(Z)=1.07c+.30s
<\frac{285873}{286100}<1<a.
\]

Thus V=B−a≤c−a<v(Z). All four target bands are strict. This completes the positive canonical sign and Theorem N.

## 7. Exact C702 owner mapping and the resulting contradiction

Translate the actual northwest merged square N=Q₈ by (x,y)↦(x−1,y−2). The data of Theorem N are supplied as follows.

| Theorem datum | Original strict point or segment | Actual owner |
|---|---|---|
| P=(-.086,0) | (.914,2) | N=Q₈, original left-wall marker |
| M=(.65,.35) | (1.65,2.35) | N=Q₈, original northwest central marker |
| H=(0,.26) | (1,2.26) | N=Q₈, auxiliary F₁ in label 2050 |
| D=(.5,0) | (1.5,2) | A=Q₆, established strict central crosspoint |
| K=(0,1) | (1,3) | Q₅, established strict point of the paired northwest corner |
| Top segment 𝒯 | [1.2,1.74]×{3} | T=Q₁₁; its new strict point (1.2,3) and owned (1.74,3) |
| Left segment 𝒱 | [(.76,1.87),(1,1.74)] | V=Q₁, its original singleton seed and owned F₀ |

The new top point (1.2,3) is proved with all original exclusions and the actual top wall in Section 3 of `C702-CONTINUOUS-REDUCTION.md`. Every excluded segment is contained strictly in its one stated actual owner. Every such owner is distinct from N. Thus Theorem N gives

\[
(1.30,1.93)\in N\quad\text{strictly}. \tag{17}
\]

The southwest-square theorem in `C702-DUPLICATE-POINT.md` gives the same strict point in A=Q₆. Since A and N are distinct actual squares, (17) contradicts the disjointness of their open interiors.

Together with the auxiliary reduction in Section 1 of `C702-CONTINUOUS-REDUCTION.md`, this excludes all original C702 auxiliary alternatives. The proof is continuous in angle and uses no orientation mesh, pose enumeration, side upper bound, or replacement of an actual neighbour by a fictitious square. The additional wall and corner completions in that reduction file remain valid reusable consequences; the present final contradiction needs only its top-wall completion.
