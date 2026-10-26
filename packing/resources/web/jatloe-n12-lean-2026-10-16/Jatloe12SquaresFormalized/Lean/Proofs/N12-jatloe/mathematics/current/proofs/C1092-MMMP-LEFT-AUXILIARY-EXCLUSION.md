# C1092 MMMP: the inward northwest square excludes the outer left auxiliary

All terminating decimals are exact rationals. Owned points are strict. Exclusions and separating supports may be tangent. The proof concerns the same actual squares throughout and uses no upper side bound.

## 1. A complete two-square obstruction after the center is known

**Theorem 1.** Let C,W be disjoint open squares of common side a>1. Suppose C strictly owns

    O=(0,0), M=(.35,.35), P=(0,.26), Q=(.26,0),
    R=(1,.4),

and excludes

    A=(.4,1), N=(−.35,.35), D=(.35,−.35).

Suppose the actual W strictly owns

    S=(1.086,0), T=(1,.26),

has its closure in x≤2, and has center ordinate Y_W≥0. Then these two squares cannot exist.

The strict center O is a genuine hypothesis here. In the MMMP application it has already been proved for every original alternative in the full-center chapter, before this theorem is used.

## 2. Forced central sign, faces and the actual separating cone

Give C first a nonnegative canonical frame (c,s),(−s,c), c≥s≥0. Write its lower faces as U,V. The foreign T has its lower u-band from Q and both upper bands from R. Hence V≥−s+.26c. The foreign A has both lower bands from M and its upper u-band from R, so V+a≤c−.4s. These opposite faces would give

    a≤.74c+.6s≤sqrt(.9076)<1,

an impossibility. This includes the axial and diagonal endpoints.

Thus C has the strictly negative frame

    u=(c,−s), v=(s,c),
    c≥s>0, c²+s²=1, p=atan(s/c)∈(0,pi/4].       (1)

Continue to denote its lower faces by U,V. Since O is strict, U,V<0. At N its upper u-band and lower v-band follow from O, and its upper v-band follows from M. Thus

    U≥−.35(c+s).

At D the lower u-band and upper v-band follow from O. An upper u exit would combine with the preceding lower face to give a≤.7(c+s)≤.7sqrt(2)<1. Therefore D is lower v, so

    −.35(c−s)≤V<0,
    U+a>c−.4s,                                    (2)

where the second inequality is strict R ownership.

Orient a separating normal n from C toward W. The strict pairs Q,S and R,T give respectively

    .826n_x>0, −.14n_y>0.

Thus n lies in the open fourth quadrant. The separating-axis theorem for the two actual squares leaves only C's own normal u, or W's actual face normal in that quadrant. Represent the latter, including its limiting axes as harmless extra cases, by

    w=(h,−b), w_perp=(b,h),
    h=cos(phi), b=sin(phi), 0≤phi≤pi/2.

Put

    alpha=ch+sb>0, delta=sh−cb.                    (3)

The real wall and center sign of this same W give X_W≤2−a(h+b)/2 and Y_W≥0. Hence its complete lower supports satisfy

    lower_W(w)<2h−[1+h²+hb]/2,                    (4)
    lower_W(u)<2c−[c(h+b)+alpha+|delta|]/2.        (5)

Each strict inequality follows by replacing a by 1 in a positive coefficient. Formula (5) uses the actual width a(alpha+|delta|) in direction u. Thus these are full-square support estimates, not support estimates of a replacement segment.

## 3. The exact common endpoint

Define

    E(p)=[(1−c)²+s(c−.8)]/2.

It is positive on the entire interval (1). With z=s/(1+c), direct substitution gives

    E(p)=z(2z−1)(5z²−2z−1)/[5(1+z²)²]>0.         (6)

Indeed 0<z≤sqrt(2)−1<1/2. Both 2z−1 and 5z²−2z−1 are negative; the latter is at most z/2−1<0.

We also use the elementary sine-interpolation inequality: on [0,L], 0<L<pi, if F''+F≤0 then

    F(t)≥[F(0)sin(L−t)+F(L)sin(t)]/sin(L).       (7)

To verify it, subtract the right side to obtain g with zero endpoint values and g''+g≤0. On any component (r,s) where g<0, integrate against sin(pi(t−r)/(s−r)). Two integrations by parts give

    [1−pi²/(s−r)²] integral(g times that sine)>0,

contrary to g''+g≤0. The interval length is less than pi, so the displayed sign is strict. This proves (7), including components meeting an endpoint.

## 4. C's own normal is impossible

Subtract the right side of (5) from the strict lower bound c−.4s for upper_C(u) in (2).

For 0≤phi≤p the difference is

    G1(phi)=c(h−1)+s[(h+b)/2−.4].

It is concave, with endpoint values G1(0)=s/10>0 and G1(p)=E(p)>0.

For p≤phi≤pi/2 the difference is

    G2(phi)=c(h+b−1)+s[(b−h)/2−.4].

It is also concave, since its h,b coefficients are c−s/2>0 and c+s/2>0. Its endpoint values are G2(p)=E(p)>0 and G2(pi/2)=s/10>0.

Thus (5) is strictly below upper_C(u) in both whole relative-angle intervals. This source cannot separate C,W.

## 5. W's own normal is impossible

### 5.1. The case 0≤phi≤p

Here delta≥0. From (2) and a>1 the full upper support obeys

    upper_C(w)=alpha(U+a)+delta(V+a)
       >alpha(c−.4s)+delta[1−.35(c−s)]
       =hA1+bB1,                                   (8)

where

    A1=c²−.75cs+s+.35s²,
    B1=.65cs−.4s²−c+.35c².

Its difference from the right side of (4) is

    F1(phi)=1/2+h²/2+hb/2+h(A1−2)+bB1.

The endpoint identities are

    F1(0)=s(1−.75c−.65s)>0,
    F1(p)=E(p)>0.                                  (9)

The first is strictly positive because .75c+.65s≤sqrt(.75²+.65²)=sqrt(.985)<1. Direct differentiation gives

    F1''+F1=(3/2)b(b−h)≤0

on 0≤phi≤p≤pi/4. Applying (7) and the two strict endpoint signs in (9) proves F1(phi)>0 on this whole interval. Thus lower_W(w)<upper_C(w).

### 5.2. The case p≤phi≤pi/2

Here delta≤0. Since V<0, the exact support in this order satisfies

    upper_C(w)=alpha(U+a)+delta V
       >alpha(c−.4s)=hA2+bB2,                       (10)

where

    A2=c²−.4cs≤1,
    B2=cs−.4s²≥.6cs≥0.

The difference from (4) is

    F2(phi)=1/2+h²/2+hb/2+h(A2−2)+bB2.

Its derivative has the lower bound

    F2'=(h²−b²)/2−hb+(2−A2)b+B2h
       ≥1/2−b(h+b−1)
       ≥3/2−sqrt(2)>0.                             (11)

At phi=p it equals E(p)>0. Hence F2 is positive on this entire interval too, excluding W's normal.

Both actual normal sources, both relative-angle orders and all canonical endpoints have been handled. No separator exists, contrary to disjoint interiors. This proves Theorem 1. ∎

## 6. The actual MMMP conclusion

**Corollary 2.** In the whole original MMMP sector,

    G1=(1,2.4) is excluded from the actual Q7.

Use the simultaneous chart (xi,eta)=(2−x,y−2), with C=Q7,W=Q8. The complete owner map is

| Local datum | Original datum | Actual source |
|---|---|---|
| O | (2,2) | Full MMMP inward-center theorem |
| M,P,Q | NW marker, F5,G3 | Original marker and core-owner theorem |
| Hypothesized R | G1=(1,2.4) | Contrary ownership in Q7 |
| Excluded A | F3=(1.6,3) | Actual Q11 |
| Excluded N | (2.35,2.35) | Actual Q6 marker |
| Excluded D | (1.65,1.65) | Actual Q4 marker |
| S,T | (.914,2), F1=(1,2.26) | Actual Q8 marker and wall-sign chord |
| Wall x≤2 | Original x≥0 | Actual Q8 container wall |
| Y_W≥0 | Original Y8≥2 | Original closed MMMP sign |

Every datum precedes this corollary. In particular the full-center theorem proves O for all original alternatives, including the present hypothetical G1 owner. Theorem 1 excludes that hypothesis.

Combined with `C1092-MMMP-TOP-AUXILIARY-EXCLUSION.md`, G1 belongs to neither Q7 nor Q11 in any original MMMP configuration. This statement does not assign G1 to another square: auxiliary points are not all required to be owned. The complete final-sector contradiction still requires a further actual-owner argument.
