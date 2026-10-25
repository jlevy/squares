# An inward square with an extended anchor: the genuine wall and its center sign force the center point

All terminating decimals are exact rationals. All owned points are strict, all exclusions and separating supports are weak, and the two squares below are the actual owners. No orientation enclosure, side upper bound, or center bound on the inward square is assumed.

## 1. The two-square theorem

**Theorem 1.** Let C and W be disjoint open squares of common side a>1. Suppose C strictly owns

    M=(.35,.35), P=(0,.26), Q=(.26,0), R=(1,.4),

and excludes A=(.4,1). Suppose W strictly owns

    S=(1.086,0), T=(1,.26),

has its closure in x≤2, and has center ordinate Y_W≥0. Then C strictly owns O=(0,0).

The wall and center sign are hypotheses about the same actual W that owns S and T. They cannot be replaced by the segment joining those points.

## 2. Forced central faces and the exact separator cone

First a nonnegative canonical orientation of C is impossible. In the frame u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1, write the lower faces as U,V and upper faces as U+a,V+a. The foreign point T has its lower u-band from Q and both upper bands from R. Thus T must leave through the lower v-face:

    V≥−s+.26c.

At A both lower bands follow from M. Its upper u-band follows from R, because u(R)−u(A)=.6(c−s)≥0 and R is strict. Hence A leaves through the upper v-face:

    V+a≤c−.4s.

These opposite faces would give

    a≤.74c+.6s≤sqrt(.74²+.6²)=sqrt(.9076)<1,

which is impossible. This includes the axis and diagonal canonical endpoints. We may therefore give C the strictly negative frame

    u=(c,−s), v=(s,c),
    c≥s>0, c²+s²=1, p=atan(s/c)∈(0,π/4].          (1)

Write U,V for its lower faces and A_C=U+a for its upper u-face. Suppose, toward a contradiction, that O is excluded from C. O has its lower u-band from P, upper u-band from Q, and upper v-band from P. Therefore its only possible exit is lower v. Strict Q and R ownership give

    0≤V<.26s,
    A_C>c−.4s.                                      (2)

For completeness, T has its lower u- and v-bands from Q and its upper v-band from R in this frame. Thus it is upper u and A_C≤c−.26s. The latter cap is consistent with (2); the proof below only needs the lower bound on A_C.

Orient any separating unit normal n from C toward W. Strict ownership of Q in C and S in W gives

    n·(S−Q)=.826n_x>0.

Strict ownership of R in C and T in W gives

    n·(T−R)=−.14n_y>0.

Consequently every separating normal belongs to the open fourth quadrant. The separating-axis theorem for two squares now leaves only u=(c,−s) or W's actual face normal in that quadrant. Represent the latter, allowing its limiting axes as harmless extra cases, by

    w=(h,−b), w_perp=(b,h),
    h=cosφ, b=sinφ, 0≤φ≤π/2.                      (3)

Put

    α=ch+sb=cos(p−φ)>0,
    δ=sh−cb=sin(p−φ).

The actual wall and center sign give

    X_W≤2−a(h+b)/2, Y_W≥0.                         (4)

Thus the lower support of W in each of the two possible source directions satisfies

    lower_W(w)≤2h−a[1+h²+hb]/2
               <2h−[1+h²+hb]/2,                    (5)

    lower_W(u)≤2c−a[c(h+b)+α+|δ|]/2
               <2c−[c(h+b)+α+|δ|]/2.              (6)

All coefficients multiplied by a are strictly positive. These are full-square support bounds derived from (4), not extra assumed walls for C.

## 3. A common endpoint scalar and a short interpolation fact

Define

    E(p)=[(1−c)²+s(c−.8)]/2.                       (7)

It is strictly positive for every p in (1). Indeed, put z=s/(1+c). Then 0<z≤sqrt(2)−1<1/2, and direct substitution gives the exact factorization

    E(p)=z(2z−1)(5z²−2z−1)/[5(1+z²)²].           (8)

Both nontrivial factors in the numerator are negative: 2z−1<0 and

    5z²−2z−1≤z/2−1<0.

We will also use the following elementary sine interpolation fact. If a twice continuously differentiable function F on [0,L], with 0<L<π, satisfies F''+F≤0, then

    F(t)≥[F(0)sin(L−t)+F(L)sin t]/sin L.          (9)

For a complete proof, subtract the expression on the right to obtain a function g with g(0)=g(L)=0 and g''+g≤0. If g were negative somewhere, a component (r,s) of its negative set would have length less than π and zero endpoint values. Multiply g''+g≤0 by the positive function sin(π(t−r)/(s−r)) and integrate by parts twice. The integral would equal

    [1−π²/(s−r)²] ∫_r^s g(t)sin(π(t−r)/(s−r))dt>0,

contrary to the nonpositive integrand of the original inequality. This proves (9), including intervals meeting an endpoint. In particular, positive endpoint values in (9) imply F>0 throughout.

## 4. C's own normal cannot separate

Strict R ownership gives upper_C(u)=A_C>c−.4s. Subtract the upper bound (6) from this latter quantity.

If 0≤φ≤p, so δ≥0, the resulting difference is

    G_1(φ)=c(h−1)+s[(h+b)/2−.4].                  (10)

As a function of φ this is concave, since

    G_1''=−(c+s/2)h−(s/2)b<0.

Its endpoint values are

    G_1(0)=s/10>0, G_1(p)=E(p)>0.

It is therefore strictly positive throughout that whole order interval.

If p≤φ≤π/2, so δ≤0, the same difference is

    G_2(φ)=c(h+b−1)+s[(b−h)/2−.4].                (11)

Again it is concave:

    G_2''=−(c−s/2)h−(c+s/2)b<0.

Its endpoint values are G_2(p)=E(p)>0 and G_2(π/2)=s/10>0. Hence it too is positive throughout. In either order, (6) is strictly below c−.4s and therefore below upper_C(u). The direction u cannot separate the two actual squares.

## 5. The actual wall square's normal cannot separate

The frame components of w relative to C are α,δ. By (2), the upper support of C is bounded as follows.

### 5.1. The order 0≤φ≤p

Here δ≥0, so

    upper_C(w)=αA_C+δ(V+a)
              >α(c−.4s)+δ
              =hA_1+bB_1,                          (12)

where

    A_1=c²−.4cs+s,
    B_1=cs−.4s²−c.

Subtract the upper bound (5) from the last expression in (12). The difference is

    F_1(φ)=1/2+h²/2+hb/2+h(A_1−2)+bB_1.          (13)

Its endpoint values are

    F_1(0)=s(1−s−.4c)>0,
    F_1(p)=E(p)>0.                                 (14)

For the first sign, the function s+.4c increases on the canonical interval, since its derivative is c−.4s>0. Its maximum there is 1.4/sqrt(2)<1.

Every linear combination of h and b has second derivative equal to its negative. Direct differentiation of (13) therefore gives the especially simple identity

    F_1''+F_1=(3/2)b(b−h)≤0                       (15)

on 0≤φ≤p≤π/4. Apply (9) on the single interval [0,p]. Both endpoints in (14) are positive, so F_1 is strictly positive throughout. The lower support of W is consequently below the upper support of C, excluding this source in the entire first order.

### 5.2. The order p≤φ≤π/2

Now δ≤0. Using the upper bound V<.26s in (2), with the sign of δ retained, gives

    upper_C(w)=αA_C+δV
              >α(c−.4s)+.26sδ
              =hA_2+bB_2,                          (16)

where

    A_2=1−.74s²−.4cs≤1,
    B_2=.74cs−.4s²≥.34cs≥0.

The corresponding difference from (5) is

    F_2(φ)=1/2+h²/2+hb/2+h(A_2−2)+bB_2.          (17)

Its derivative has the exact expression

    F_2'=(h²−b²)/2−hb+(2−A_2)b+B_2h.

The two displayed coefficient bounds imply

    F_2'≥1/2−b(h+b−1)
         ≥3/2−sqrt(2)>0,                           (18)

since 0≤b≤1 and 0≤h+b−1≤sqrt(2)−1. Thus F_2 increases on the entire interval, and

    F_2(φ)≥F_2(p)=E(p)>0.

This excludes W's normal in the second order as well. Both normal sources, including every actual W orientation and their possible axial limits, have been exhausted. Missing O was impossible, proving Theorem 1. ∎

## 6. Direct application to the original C1092 MMMP sector

**Corollary 2.** In the original MMMP sector, if the actual northwest central Q7 owns G1=(1,2.4), then it strictly owns (2,2).

**Proof.** Use the direct original conclusions of `C1092-MMMP-CORE-OWNERS.md`: Q7 owns F5=(2,2.26) and G3=(1.74,2); Q11 owns F3=(1.6,3); Q8 owns F1=(1,2.26). Set C=Q7 and W=Q8 and apply the simultaneous chart

    (ξ,η)=(2−x,y−2).

The complete source ledger is

| Theorem datum | Original point | Actual strict owner |
|---|---|---|
| M=(.35,.35) | (1.65,2.35) | Original marker in Q7 |
| P=(0,.26) | F5=(2,2.26) | Q7 by the core theorem |
| Q=(.26,0) | G3=(1.74,2) | Q7 by the core theorem |
| R=(1,.4) | G1=(1,2.4) | Q7 by this corollary's explicit hypothesis |
| Excluded A=(.4,1) | F3=(1.6,3) | Q11 by the core theorem |
| S=(1.086,0) | (.914,2) | Original marker in Q8 |
| T=(1,.26) | F1=(1,2.26) | Q8 by the wall-sign theorem |

The transformed real wall is ξ≤2, and the transformed center condition is η_W≥0, exactly the original MMMP sign Y8≥2. The common side and actual disjointness are unchanged. Thus Theorem 1 puts its O=(0,0), which is the original point (2,2), strictly in Q7. ∎

The corollary is conditional only on the one stated G1 ownership; it does not assume that Q8 owns G1 or any farther left-wall auxiliary. Other MMMP ownership alternatives remain separate obligations.
