# C1092 MPPM: the actual bottom square bounds a missing-center inward angle

All terminating decimals are exact rationals. Owned points are strict, while
excluded points, real walls, center signs and separating supports permit
equality. The two squares in the local theorem are the actual owners. No upper
side bound or orientation subdivision is assumed.

## 1. A two-square theorem and its exact threshold

**Theorem 1.** Let C and B be disjoint open squares of common side a>1. Suppose
C has a nonpositive canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,

strictly owns

    M=(−.35,−.35), I=(0,−.26), J=(−.26,0),
    X=(−.5,0), T=(−.01,−.54),

and excludes

    O=(0,0), G=(−1,−.4).

Suppose B strictly owns

    S=(0,−1.086), A=(−.26,−1), F=(−.56,−1),

has its closure in y≥−2, and has actual center abscissa X_B≤0. Then

    0<z:=s/(1+c)<α:=1−2√5/5.                       (1)

In particular z<.106. The center condition is imposed on the same actual
square B that owns S,A,F and obeys the real bottom wall.

Write U,V for C's lower faces, and A_C=U+a,H_C=V+a for its upper faces.
At s=0, the strict points I,J already put O in both open coordinate bands,
contrary to its exclusion. Thus s>0. The two u-bands of O follow from I,J,
and its lower v-band follows from M. Therefore O is upper v. At G both upper
bands follow from M. A lower-v exit would give a≤s+.4c≤1.4/√2<1, using
H_C≤0. Consequently

    H_C≤0, V≤−a,
    U≥−c+.4s, A_C≥a−c+.4s,
    U<−.5c.                                          (2)

The last strict inequality is the u-band of the actual point X.

Suppose now z≥α, and put p=arctan(s/c). Define

    Q=1−c+.4s,
    J_0=c+s−1−cs+.4s²=s(Q−z).                       (3)

The exact half-angle identity

    Q−z=−z(z²−2z+1/5)/(1+z²)                       (4)

shows Q≥z and J_0≥0 throughout α≤z≤√2−1. We will contradict actual
separation on every possible face normal. Also α>1/10, so monotonicity of
c+s on 0≤p≤π/4 gives

    c+s>119/101>543/500=1.086.                       (5)

## 2. The full separating-normal cover

Orient every separating unit normal from B toward C. Strict I,S ownership
forces n_y>0. Strict T,F ownership gives

    .55n_x+.46n_y>0.                                 (6)

In particular C's up-left normal −u=(−c,s) is impossible, since its value
in (6) is at most −.09c<0. C's only remaining eligible face normal is
v=(s,c).

Every actual B admits either the nonnegative frame

    w=(h,k), w_perp=(−k,h), h≥k≥0, h²+k²=1,         (7)

or the nonpositive frame

    w=(h,−k), w_perp=(k,h), h≥k≥0, h²+k²=1.         (8)

For (7), the only possible upward B normals are w,w_perp. For (8), the
up-left normal −w=(−h,k) fails (6), again by −.55h+.46k<0. Thus only
w_perp remains in (8). Horizontal endpoints fail n_y>0 but may harmlessly
be retained in the estimates below. Together with v, these are the entire
actual separating-axis cover.

## 3. Nonnegative B: the central source

Use frame (7), and write L,K for B's lower faces and J_B=L+a,D_B=K+a for
its upper faces. Put d_0=543/500. The actual points S,A give

    J_B>−d_0 k, D_B>.26k−h.

The components of v=(s,c) on (7) are sh+ck>0 and ch−sk≥0. Thus

    upper_B(v)>−c A_0−s B_0,
    A_0=1+.086k²−.26hk,
    B_0=.086hk+.26k².

The exact identity

    A_0²+B_0²=1+.246996k²−.52hk≤1                 (9)

uses k≤h. Cauchy's inequality now gives upper_B(v)>−1, whereas (2)
gives lower_C(v)=V≤−a<−1. This source cannot separate.

## 4. Nonnegative B: its upright source

For n=w=(h,k), put λ=ch−sk≥0 and μ=sh+ck>0. Equation (2), together
with strict S ownership, gives

    upper_B(w)−lower_C(w)
       >(.5c)λ+μ−d_0k
       =h(.5c²+s)+k(c−.5cs−d_0).                 (10)

The coefficient of h is positive. The sum of the two displayed
coefficients equals

    c+s+.5c(c−s)−d_0>0

by (5). Since 0≤k≤h, the last expression in (10) is strictly positive,
whether the coefficient of k is positive or negative. This source is
therefore impossible.

## 5. Nonnegative B: its up-left source

For n=w_perp=(−k,h), the real bottom wall and the actual center sign give

    upper_B(n)=−kX_B+hY_B+a/2
       ≥−2h+(a/2)[1+h(h+k)].                       (11)

Indeed Y_B≥−2+a(h+k)/2 and −kX_B≥0. Put

    γ=ck+sh>0, δ=ch−sk≥0.

Then n=−γu+δv, so (2) gives

    lower_C(n)≤−γ(a−c+.4s)−aδ.

The coefficient of a in the resulting support difference is positive.
Dropping a to 1 is therefore strict, and gives

    upper_B(n)−lower_C(n)>F(φ),
    h=cosφ, k=sinφ, 0≤φ≤π/4,
    F(φ)=1/2+h²/2+hk/2+h(A_1−2)+kB_1,           (12)
    A_1=c+s−cs+.4s²,
    B_1=c−s−c²+.4cs.

Its first endpoint is F(0)=A_1−1=J_0≥0. At the other endpoint,

    F(π/4)=1+(A_1+B_1−2)/√2.

Since

    A_1+B_1=2c−c²+.4s²−.6cs
       ≥(√2−1/2)−3/10=√2−4/5,

we have

    F(π/4)≥2−7√2/5>0.                              (13)

Here 2c−c² is increasing for 1/√2≤c≤1, and cs≤1/2. Direct
differentiation gives the single continuous identity

    F''+F=(3/2)k(k−h)≤0.                            (14)

For completeness, if a twice differentiable f on [0,L], L<π, satisfies
f''+f≤0, then

    f(t)≥[f(0)sin(L−t)+f(L)sin t]/sin L.             (15)

Subtract the right side. If the difference were negative on a component
(r,s), integrate its differential inequality against the positive function
sin(π(t−r)/(s−r)). Two integrations by parts would give

    [1−π²/(s−r)²]∫_r^s g(t)sin(π(t−r)/(s−r))dt>0,

contradicting the nonpositive differential inequality. This proves (15).
Apply it to (12) on [0,π/4]. Equations (13)–(14) and F(0)≥0 imply F≥0
throughout. The strict a>1 step in (12) excludes the source even at the
possible equality endpoint z=α,φ=0. This completes every nonnegative B
orientation.

## 6. Nonpositive B has an upper face strictly above −1

Use frame (8), with lower faces L,K and upper faces J_B=L+a,D_B=K+a.
The actual bottom wall is

    −kJ_B+hK≥−2.

Strict S ownership gives J_B>d_0k and D_B>−d_0h. Hence also

    D_B≥a+(d_0k²−2)/h.                              (16)

The last comparison is strict when k>0; its weak form also covers k=0.

We claim

    D_B>−1.                                         (17)

If h≤10/11, strict marker ownership gives

    D_B>−d_0h≥−543/550>−1.

If h≥10/11, the exact factorization

    2h+d_0(1−h²)−2=(1−h)[d_0(1+h)−2]≥0

holds: the bracket is at least 11403/5500−2>0. Equation (16), with
a>1 retained, now gives D_B>−1 as well. At k=0 the strict inequality
follows directly from a>1 in (16). Thus no axial or diagonal endpoint is
lost. The assertion uses the actual marker and actual wall only.

## 7. Nonpositive B: its own upright source

Put φ=arctan(k/h), so 0≤φ≤π/4. For n=w_perp=(k,h), its components
on C are

    δ=ck−sh=sin(φ−p), λ=ch+sk=cos(φ−p)>0.

If φ≤p, write ε=−δ=sin(p−φ)≥0. From (2),

    lower_C(n)≤−ε(a−c+.4s)−aλ
       <−[λ+Qε].                                   (18)

Because Q≥z and tan((p−φ)/2)≤tan(p/2)=z, the elementary identity
1−cos t=sin t·tan(t/2) gives λ+Qε≥1. Thus lower_C(n)<−1<D_B.

If φ≥p, (2) instead gives

    lower_C(n)<−[λ+.5cδ].                           (19)

Here λ+.5cδ≥1. To check the complete interval, put t=φ−p. Then

    tan(t/2)≤(c−s)/(√2+c+s)<c/2,

since

    c(√2+c+s)−2(c−s)
       ≥c[c−(2−√2)]>0.

The same elementary half-angle identity proves the claimed bound,
including t=0. Equation (17) again rules out this source. This treats
both whole angle orders without any subdivision of the canonical range.

## 8. Nonpositive B: the central source

For n=v=(s,c), its components on B are

    η=sh−ck=sin(p−φ), λ=ch+sk=cos(p−φ)>0.

If p≥φ, then η≥0. Since J_B>d_0k≥0 and D_B>−1,

    upper_B(v)=ηJ_B+λD_B>−λ≥−1.                   (20)

Suppose instead φ>p, and write ε=−η>0. The actual far point F gives

    L<−.56h+k.

If k≤.56h then L<0, and again

    upper_B(v)=−εL+λD_B>−λ≥−1.

If k≥.56h, retain the strict marker bound D_B>−d_0h. Then

    upper_B(v)>ε(.56h−k)−d_0λh=−cA_2−sB_2,
    A_2=1+.086h²−.56hk,
    B_2=.56h²+.086hk.

The exact identity

    A_2²+B_2²=1+.492996h²−1.12hk
       ≤1−.134204h²<1                              (21)

gives upper_B(v)>−1 by Cauchy's inequality. In every case lower_C(v)
is at most −a<−1, so v cannot separate. Sections 2–8 exhaust all actual
normal sources. The assumption z≥α was impossible, proving Theorem 1. ∎

## 9. Literal no-omission MPPM application

**Corollary 2.** Retain the original no-omission MPPM entrance. Suppose Q4
owns its inward pair F4,G3, excludes G0=(1,1.6), and excludes the common
center O=(2,2). If Q4 has nonpositive canonical orientation, then its
negative half-angle magnitude satisfies (1).

**Proof.** Apply Theorem 1 to the actual owners C=Q4 and B=Q9, translated
by (−2,−2). The complete point ledger is

| Local datum | Original point | Actual source |
|---|---|---|
| M | (1.65,1.65) | Original marker in Q4 |
| I | F4=(2,1.74) | Hypothesized inward pair in Q4 |
| J | G3=(1.74,2) | Hypothesized inward pair in Q4 |
| X | (1.5,2) | No-omission reduction, Section 1, equation (3a) |
| T | (1.99,1.46) | Rotated inward point theorem described below |
| Excluded G | G0=(1,1.6) | This corollary's stated omission from Q4 |
| Excluded O | (2,2) | This corollary's stated missing-center premise |
| S | (2,.914) | Original marker in Q9 |
| A | G2=(1.74,1) | Actual no-omission Q9 pair |
| F | (1.44,1) | Actual Q9 wall reach in the no-omission reduction |

For T, apply Corollary 3 of C1084-DUPLICATE-POINT.md under the simultaneous
quarter-turn R³(x,y)=(y,4−x). Its three strict anchors become the SW marker,
G3,F4. Its three exclusions become the NW marker, the SE marker, and exactly
G0. The first two have distinct actual original owners, while G0 is the
explicit omission. Its strict conclusion (2.54,1.99) becomes
(1.99,1.46), proving the ledger entry without an additional wall premise.

The bottom reach used in the last row is already a direct consequence of
the inward no-omission reduction: Q5 owns F6,G5; actual Q9 owns its original
marker and F2; its two foreign wall-reach points are G5 in Q5 and F4 in Q4.
Thus (1.44,1) is genuinely in Q9. No point from a union of owners is used
as a segment endpoint. The true bottom wall becomes y≥−2, and the original
MPPM sign X9≤2 becomes the center condition X_B≤0. All hypotheses of
Theorem 1 have therefore been checked literally. ∎

The corollary concerns the G0-omitted inward branch. An inward square that
owns G0 and omits F0 has not been assigned G0's lower face or the strict
point T here. Its separate geometric obligation is unchanged. The present
result is an angle reduction, not by itself a proof of center ownership.
