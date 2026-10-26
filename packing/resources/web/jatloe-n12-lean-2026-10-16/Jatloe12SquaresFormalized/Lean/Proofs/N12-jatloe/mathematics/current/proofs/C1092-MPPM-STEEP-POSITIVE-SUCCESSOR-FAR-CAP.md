# C1092 MPPM: the actual far bar caps a positive successor of a steep missing sector

All decimals are exact rationals. All squares below are actual open squares of common side a>1, with disjoint interiors. An exterior point or supporting equality is allowed to be tangent. The whole bar in the theorem has one actual owner in its application.

## 1. Local statement

**Theorem 1.** Let C,E be two such squares. Suppose C has the positive canonical frame

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    p in [2 atan(1/3), pi/4],

strictly owns M_C=(-.35,-.35), and has lower faces U,V and upper faces A=U+a,K=V+a satisfying

    U>=-c-s, A<=0, V>=.56s-c, K<=1.086s.           (1)

Suppose E has the nonnegative canonical frame

    e=(d,t), f=(-t,d), d>=t>=0, d^2+t^2=1,

strictly owns

    M_E=(.35,-.35), B1=(.4,-1),

has lower faces L,Q and upper faces J=L+a,D=Q+a, and satisfies D<=0. Suppose E excludes the whole segment

    {1} x [-.56,-.4].                              (2)

Then

    J<=d-.56t.                                    (3)

No actual wall, boundary-center sign, forward membership of E, or crosspoint in E is a premise of this local theorem.

## 2. The only competing exit and its whole-bar consequence

Put R=(1,-.56), S=(1,-.4). At every point of the segment (2), the lower-e band is strict by B1 and the upper-f band is strict by M_E. At the lower endpoint their corresponding increments are .6d+.44t and .65t+.21d, and both remain strictly positive along the segment.

At S the lower-f band is also strict, by B1, since

    f(S)-f(B1)=.6(d-t)>=0.

Thus S is upper e, so J<=d-.4t. If R is upper e, (3) is proved. Suppose it is not. Its sole remaining exit is then lower f, giving

    Q>=-t-.56d, D>=a-t-.56d.                       (4)

Together with D<=0 this implies 1<a<=t+.56d. Consequently t>0 and, for z=t/(1+d),

    z>11/39,                                      (5)

by the exact factor

    t+.56d-1=(1-z)(39z-11)/(25(1+z^2)).            (6)

There is no unrecorded crossing of the actual bar. On its supporting line, the lower-f exterior interval ends at y=(Q+t)/d, and the upper-e exterior interval begins at y=(J-d)/t. At R the upper-e band is strict, whereas at S the lower-f band is strict. Both thresholds therefore lie in the stated segment, with the appropriate strict endpoint on opposite ends. Since every point of the whole segment is outside E, the thresholds must obey

    (Q+t)/d >= (J-d)/t,
    dJ-tQ<=1.                                     (7)

If the order were reversed, every intermediate y would have all four bands strict. Equality in (7) is retained, so this argument includes a tangency at the rightmost vertex of E.

Substituting J=L+a,Q=D-a and using D<=0 in (7) gives

    L<-(d+t-1)/d=-2z/(1+z)<-11/25=-.44.           (8)

Also (4), D<=0 and a>1 give

    0<=-D<t+.56d-1<=1.56/sqrt(2)-1<.104,
    Q=D-a<-1.                                    (9)

The monotonic maximum in (9) follows from d-.56t>0 on the full canonical interval. The final rational comparison follows by squaring 1.56<1.104 sqrt(2).

## 3. Uniform bands of C and the complete normal list

The stated angle range implies c<=.8 and s>=.6. Equations (1) and a>1 therefore give

    A>1-sqrt(2)>-.415,
    K>1+.56(.6)-.8=.536,
    K<=1.086/sqrt(2)<.768,
    a-K>.232.                                    (10)

These rational comparisons follow by squaring sqrt(2)<1.415 and 1.086<.768 sqrt(2).

The two strict markers have difference (.7,0). Hence any separating normal oriented from C toward E must have positive x-coordinate. Because both frames are nonnegative and C is strictly positive, the only possible actual-square sources are

    u, -v, e, -f.                                (11)

A zero x-coordinate at t=0 would already be excluded by the strict marker pair. In the competing case (4), (5) gives t>0 in any event. Thus (11) is exhaustive.

Write q for E's angle. For p>=q, put

    k=cos(p-q), h=sin(p-q)>=0.

For q>=p use k=cos(q-p), h=sin(q-p)>=0. Always k>=1/sqrt(2)>.7. In the second order, p>=2 atan(1/3) and q<=pi/4 give the stronger bounds

    k>=7/(5sqrt(2))>.98,
    h<=1/(5sqrt(2))<.15.                          (12)

We now exclude all four actual sources using the same faces (8)--(10).

## 4. Every actual source fails in the competing case

### 4.1. The C normal u

If p>=q, then u=k e+h f, so

    lower_E(u)=kL+hQ<-.44k-h<=-.44<A.

The penultimate inequality follows from .44 cos r+sin r>=.44 for 0<=r<=pi/4; its derivative cos r-.44 sin r is positive.

If q>=p, then u=k e-h f. Equations (8),(9),(12) give

    lower_E(u)=kL-hD<-.44k+.104h
       < -.44(.98)+.104(.15)=-.4156<A.

Thus u cannot separate in either angle order.

### 4.2. The E normal e

If p>=q, then e=k u-h v and

    upper_C(e)=kA-hV=kA+h(a-K)>-.415k+.232h>=-.415>L.

If q>=p, then e=k u+h v, and

    upper_C(e)=kA+hK>-.415k+.536h>=-.415>L.

Again both orders fail.

### 4.3. The C normal -v

If p>=q, then -v=h e-k f, whence

    lower_E(-v)=hL-kD<-.44h+.104k<=.104<a-K.

If q>=p, then -v=-h e-k f. The strict marker of E gives J>e(M_E)=.35(d-t)>=0. Therefore

    lower_E(-v)=-hJ-kD<.104k<=.104<a-K.

The source -v is impossible.

### 4.4. The E normal -f

If p>=q, then -f=-h u-k v. Since A<=0,

    upper_C(-f)=-hU-kV=h(a-A)+k(a-K)
                   >.232k>.232(.7)=.1624>-D.

If q>=p, then -f=h u-k v. Equations (10),(12) instead give

    upper_C(-f)=hA+k(a-K)
       >-.415h+.232k
       >-.415(.15)+.232(.98)=.16511>-D.

This excludes the final source. Equal angles are covered by either displayed order, and all final comparisons are strict independently of any weak exterior face.

All possible separating axes in (11) have failed. The two actual squares would have intersecting interiors, a contradiction. Thus the competing lower-f alternative at R cannot occur without an upper-e exit, and (3) follows. ∎

## 5. Actual OOOO application and the missing-crosspoint reduction

Retain the original OOOO no-omission entrance. Let C=Q4 be positive and omit its forward G3. Its unconditional missing-positive profile supplies (1), and its original strict marker is M_C after translation by (-2,-2).

If C additionally omits X=(1.5,2), then that omitted point has its lower-u band strict by G0, its lower-v band strict from K<=1.086s and a>1, and its upper-v band strict from V>=.56s-c. Therefore X is upper u:

    A<=-.5c.

Together with U>=-c-s, this yields a<=.5c+s. The factor (3) of C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md therefore gives the strict angle implication

    p>2 atan(1/3).                                (13)

Take the actual successor E=Q5 and suppose it has positive canonical angle. Its universal positive upper-u cap in its own quarter-turn chart is exactly D<=0 in the present common chart, whether it owns or omits its forward F4. Its strict M_E and B1 are the actual southeast marker and F6. The segment (2), after translation, is the genuine actual Q10 segment from (3,1.44) to G8=(3,1.6). Its endpoint (3,1.44) is the already established no-omission ordinary-wall advance; its endpoint G8 is an original strict point of Q10. Convexity puts the whole segment in that one actual open owner.

Thus Theorem 1 applies literally and gives the strengthened face

    upper_e(Q5)<=d-.56t                            (14)

in centered coordinates. No next-forward point is assumed foreign, and Q5's own crosspoint is not needed for (14).

The full actual C/E/Q9 obstruction under (13)--(14), when Q5 additionally owns its local crosspoint, is now proved in C1092-MPPM-STEEP-POSITIVE-THREE-SQUARE-REDUCTION.md using the companion CENTRAL-SCALAR and BOUNDARY-SCALARS chapters. The present theorem supplies its far-cap step; no crosspoint premise has been added to this theorem itself.
