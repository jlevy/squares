# C1092 MPPM: an elbow forces a negative ordinary successor

All terminating decimals are exact rationals. Strict ownership means interior membership in the named open square. Excluded points and separating supports allow equality. This chapter retains the complete original no-omission MPPM entrance and uses the actual-owner cover in C1092-MPPM-NONORDINARY-ISOLATION.md. No reduced ownership-vector catalogue is assumed.

## 1. A local two-square theorem

**Theorem 1.** Let C,E be open squares of the same side a>1 with disjoint interiors. Suppose C satisfies Lemma 1 of C1092-MPPM-NONORDINARY-ISOLATION.md: it strictly owns

    (−.35,−.35), (−1,−.26), (−.26,0),

and excludes

    (−.35,.35), (−1,−.4), (−1.086,0),
    (0,−.26), (−.4,−1).

Suppose E strictly owns

    M=(.35,−.35), A=(.26,−1), B=(.4,−1),

and excludes

    G=(1,−.4), K0=(1,−1), R0=(0,−1.086).             (1)

Then E has a strictly negative canonical angle and excludes T=(0,−.26). No wall, center bound or upper side bound is needed for this local theorem.

Write C's positive frame and faces as

    u=(c,s), v=(−s,c), c²+s²=1,
    U<u·X<J=U+a, V<v·X<K=V+a.

The preceding lemma gives

    U≥−c−.4s, J≤−.26s,
    V≥.4s−c, K≤.35(c+s), X=(0,−.5) strict in C,      (2)
    0<z:=s/(1+c)<7/50.

In addition to c>24/25 and s<7/25, we shall use

    c+s<31/25.                                      (3)

Indeed c+s increases on the canonical interval and at z=7/50 equals 3151/2549<31/25.

We first exclude all nonnegative canonical angles of E. Choose its frame

    u′=(d,t), v′=(−t,d), d≥t≥0, d²+t²=1,

and denote its lower faces by L,W and its upper faces by J_E=L+a, K_E=W+a. Let p,q be the ordinary nonnegative angles of C,E.

### 1.1. The ordinary successor's forced outer cap

At G the lower-u and both v-bands are strict, by M and B:

    u′(G)−u′(M)=.65d−.05t≥.60d>0,
    v′(G)−v′(B)=.6(d−t)≥0,
    v′(M)−v′(G)=.65t+.05d>0.

Therefore G is upper u, so

    L≤d−.4t−a.                                      (4)

Strict M and B also give the independent bounds

    W>−.35(d+t)−a,   W<−d−.4t.                       (5)

Set

    kappa=cos(q−p)=cd+st>0,
    sigma=sin(q−p)=ct−sd.

The strict marker difference from C to E is (.7,0). Consequently any separating normal toward E has positive horizontal component. The exhaustive actual face-normal list is therefore

    u, u′, −v, −v′.                                 (6)

When t=0 a listed transverse direction with zero horizontal component is already excluded by the strict marker comparison. It is harmless to retain it in the inequalities below. Reverse normals and the other transverse directions have nonpositive horizontal component and cannot separate.

## 2. The two longitudinal normals fail

### 2.1. The direction u when q≤p

Here sigma≤0. Equations (4),(5) give

    lower_E(u)=kappa L−sigma W
       ≤kappa(d−.4t−a)+sigma(d+.4t).

The maximum of C in this direction is J≥a−c−.4s. Their support difference is strictly greater than

    F=1+kappa−c−.4s−kappa d+.4kappa t
                                      −sigma(d+.4t). (7)

Compare this with F2 in equation (13) of C1092-MPPM-NONORDINARY-ISOLATION.md. Their exact difference is

    F−F2=sigma(1−d−.14t)≥0.                          (8)

In fact 0≤tan(q/2)≤tan(p/2)<7/50 implies d+.14t≥1 by the exact half-angle identity used there, while sigma≤0. The completed derivative proof of F2≥0 applies on this same closed angle range. Thus u cannot separate in this order.

### 2.2. The direction u when q≥p

Now sigma≥0. Equations (4),(5) instead give

    lower_E(u)=kappa L−sigma(W+a)
       ≤kappa(d−.4t−a)+.35sigma(d+t).

The support difference from J is strictly greater than

    F=1−c−.4s+kappa(1−d+.4t)
                                      −.35sigma(d+t). (9)

Here q may range all the way to pi/4; no unproved small-angle restriction on E is imposed. Put w=tan(q/2), h=w−z. Then

    0<z<7/50<3/20, 0≤h, z+h=w≤sqrt(2)−1<5/12.

The exact positive-denominator identity is

    F=N/[10(1+z²)(1+w²)²],                           (10)

where

    N=40z²(1+z²)²+h A1(z)+h² A2(z)+h³ A3(z)+h⁴ A4(z),
    A1(z)=160z⁵−z⁴+186z³+26z+1,
    A2(z)=240z⁴−3z³+112z²−z+6,
    A3(z)=160z³−3z²−14z−1,
    A4(z)=40z²−z−20.

For 0≤z≤3/20 the following elementary coefficient bounds hold:

    A1≥1, A2≥29/5, A3≥−16/5, A4≥−81/4.

For A1, group 26z−z⁴=z(26−z³)≥0. For A2, dropping its positive terms leaves 6−z−3z³≥46719/8000>29/5. For A3 the lower bound −1−14z−3z²≥−1267/400>−16/5 suffices. For A4 use −20−z≥−403/20>−81/4. Since h≤5/12, it follows that

    A2+h A3+h² A4
       ≥29/5−(5/12)(16/5)−(25/144)(81/4)
       =913/960>0.

Consequently

    N≥40z²(1+z²)²+h+(913/960)h²>0.                  (11)

This proves (9) positive throughout q≥p and rules out u.

### 2.3. The direction u′ in both relative orders

If q≥p, C's support is kappa J+sigma K. Equations (2),(4) show that the difference from E's minimum L is strictly greater than

    F1=1+kappa+sigma−d+.4t
                   −(kappa+sigma)c−.4(kappa−sigma)s.

At q=p this is 2(1−c)≥0, and for fixed p its derivative is

    dF1/dq=t+.4d+(kappa−sigma)(1−c)
                                  +.4(kappa+sigma)s>0.

Here 0≤q−p≤pi/4, so kappa−sigma≥0. This is the same exact derivative as in the preceding two-elbow theorem, and its sign remains valid on the entire present enlarged q interval.

If q≤p, C's support is kappa J+sigma V. Using V≤.35(c+s)−a and (4) yields precisely F3 in equation (15) of that theorem. The completed derivative bound 421/3125>0 applies because both angles are then below 2 arctan(7/50). Thus this source fails too. Each replacement of a by 1 above is strict because its coefficient is positive.

## 3. The two transverse normals fail

### 3.1. The direction −v

Equation (2) gives

    upper_C(−v)=−V≥a−.35(c+s)>.35(c+s),

where .7(c+s)≤.7sqrt(2)<1 was used. The last expression is exactly (−v)·M, and M is strict in E. Therefore this normal cannot separate.

### 3.2. The direction −v′ when q≤p

Since sigma≤0,

    upper_C(−v′)=sigma U−kappa V
      ≥a(kappa−sigma)−.26sigma s−.35kappa(c+s).

Strict M in E gives lower_E(−v′)<.35(d+t). The difference is strictly greater than

    kappa[1−.7(c+s)]−sigma[1+.35c−.09s]>0,           (12)

using (3), sigma≤0 and c≥s. Thus this order is impossible without using either additional exclusion K0 or R0.

### 3.3. The direction −v′ when q≥p: the corner's two exits

At K0 the lower-u and upper-v bands are strict by A and B, with increments .74d>0 and .6t≥0. Therefore K0 is upper u or lower v.

First suppose K0 is upper u, J_E≤d−t. At R0 both upper bands are strict:

    u′(A)−u′(R0)=.26d+.086t>0,
    v′(M)−v′(R0)=.736d−.35t≥.386d>0.

Hence R0 is lower u or lower v. A lower-v exit, combined with strict A, requires .26t<.086d. A lower-u exit instead gives

    1<a≤d+.086t,

and therefore tan(q/2)<.086<1/10. This also implies t/d<20/99<43/130. In both alternatives we have proved

    t/d<43/130, d>47/50, t<8/25.                    (13)

For the last rational comparisons one can square the positive quantities: 130²−(47/50)²(130²+43²)=833459/2500>0, and (8/25)²(130²+43²)−43²=44311/625>0.

In the current order q≥p, kappa≥d>47/50 and 0≤sigma≤t<8/25. Equations (2) and strict M give the following lower bound for the support difference:

    upper_C(−v′)−lower_E(−v′)
      >kappa[1−.7(c+s)]+sigma[1−1.35c−.05s].        (14)

The first bracket is at least 1−.7(31/25)=33/250. The second is at least −.364=−91/250. Thus (13) gives

    (14)≥(47/50)(33/250)−(8/25)(91/250)
          =19/2500>0.

It remains that K0 is lower v. Then W≥−d−t, and hence

    lower_E(−v′)=−(W+a)≤d+t−a.

The same C support bound now gives the margin

    upper_C(−v′)−lower_E(−v′)
      >1+kappa+sigma−1.35kappa(c+s)
                                      −sigma(2c−.6s). (15)

To prove it positive put delta=q−p, so 0≤delta≤pi/4−p, and set

    A0=1.35(c+s)−1>0, B0=2c−.6s−1>0.

The right side of (15) is 1−G(delta), where

    G(delta)=A0 cos(delta)+B0 sin(delta).

This function increases throughout the stated interval. Indeed

    B0(c+s)−A0(c−s)
       =.65+.10s²+1.4cs−2s
       ≥.65−2(7/25)=.09>0,

which gives B0/A0>tan(pi/4−p)≥tan(delta), so G′(delta)>0. At the upper endpoint the exact value is

    sqrt(2) G(pi/4−p)=1.95+1.4c²+.1cs−2c.

Its difference from 1.35 is

    (1−c)(.6−1.4c)+.1cs≤.1s<7/250.

Therefore G(delta)<(1.35+.028)/sqrt(2)<(7/5)/sqrt(2)<1. This proves (15) positive and excludes the final transverse source.

The four normals in (6) have now all failed. This excludes every nonnegative canonical orientation of E, including zero, the positive diagonal and all relative-angle equalities.

## 4. A negative successor cannot own the forward inner point

The surviving canonical frame is u′=(d,−t), v′=(t,d), with d≥t≥0. Suppose T=(0,−.26) were strict in E. Then X=(0,−.5) would satisfy all four strict bands of E:

    u′(X)−u′(T)=.24t≥0,
    v′(T)−v′(X)=.24d>0,
    u′(B)−u′(X)=.4d+.5t>0,
    v′(X)−v′(A)=.5d−.26t≥.24d>0.

But (2) already puts X strictly in C, contradicting disjoint interiors. Thus T is excluded from E. The zero and diagonal representations were included in the preceding sign exclusion; choosing a negative representative introduces no unhandled endpoint. This proves Theorem 1. ∎

## 5. Exact no-omission maps and the wall-origin consequence

If Q4 is a residual elbow, the actual-neighbor theorem in C1092-MPPM-NONORDINARY-ISOLATION.md forces Q5 to have its ordinary pair F6,G5. Translate by (−2,−2) and set C=Q4,E=Q5. The full hypothesis table for C is already given in that chapter. E's three strict anchors are the actual SE marker,G5,F6. Its excluded G,K0,R0 are, respectively,

    G8=(3,1.6) strict in actual Q10,
    (3,1) strict in actual paired corner Q1,
    (2,.914) strict in actual Q9.

Thus Theorem 1 applies to the actual C,E without any assumed ownership of F4. Its conclusion is that Q5 has a strictly negative canonical angle and excludes F4=(2,1.74).

Apply ORDINARY-MARKER-HALFPOINT.md to this actual Q5 under the explicit map from that theorem's local coordinates

    (xi,eta) -> (2−eta,2−xi), d=.086.

Its strict ordinary anchors become F6,G5 and its SE marker. The four exclusions D,R,K,F become, respectively, the just-proved missing F4, the actual bottom marker (2,.914) in Q9, the actual paired SE corner (3,1) in Q1, and F8=(3,1.74) in Q10. In particular its R is the genuine bottom marker already denoted R0 in the present translated two-square theorem. Therefore

    (2.5,1) is strict in actual Q5.

Theorem 7 of C1092-DIRECT-WALL-POINT.md now applies after the same simultaneous quarter-turn: its actual paired corner is Q1, its actual boundary is Q10, and its marker/anchor parameters are b=.914, ell=1.6. The corner's required excluded halfpoint is the point just proved in Q5; its strict anchors are the original paired marker and inner corner. The boundary's strict anchors are the original right marker and G8. Its genuine right wall is the transported bottom wall. The strict conclusion is

    (3,2) in Q10.

This application does not require all four central squares to be ordinary. The literal ordinary-halfpoint and paired-corner-transfer inputs have just been supplied from the one residual elbow, its actual ordinary successor and the no-omission wall pairs.

Simultaneous quarter-turns give the full table:

| Residual elbow owner | Ordinary successor has strictly negative angle | Forward point excluded from that successor | Strict point forced in the actual boundary |
|---|---|---|---|
| Q4 | Q5 | F4 | (3,2) in Q10 |
| Q5 | Q6 | G6 | (2,3) in Q11 |
| Q6 | Q7 | F5 | (1,2) in Q8 |
| Q7 | Q4 | G3 | (2,1) in Q9 |

These are actual point owners and genuine angular restrictions. The chapter completes this local successor theorem and the four origin implications. A further cyclic or actual-neighbor argument is still required to exclude every isolated-elbow or all-ordinary arrangement.
