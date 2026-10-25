# An ordinary right-hand central pair forces its lower halfpoint

All terminating decimals are exact rationals. Owned points are strict; excluded points may lie on a face. The theorem requires no wall, upper side bound, center bound, or neighboring-square approximation.

**Theorem 1.** Let Q be an open square of side a>1. Suppose Q strictly owns

    M=(2.35,1.65), A=(3,1.74), B=(3,1.6),

and excludes

    D=(2.26,2), R=(3,2), K=(3,1), F=(2.26,1).

Then Q strictly owns Y=(3,1.5).

**Proof.** Translate by (−2,−2). The owned points become M=(.35,−.35), A=(1,−.26), B=(1,−.4); the excluded points become D=(.26,0), R=(1,0), K=(1,−1), F=(.26,−1); and the target is Y=(1,−.5). Write U,V for lower face coordinates.

First use a nonnegative canonical frame u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1. At K its lower u-band follows from M, and both upper bands follow from B:

    u(K)−u(M)=.65(c−s)≥0,
    u(B)−u(K)=.6s≥0,
    v(B)−v(K)=.6c>0.

Thus K is lower v, so V≥−s−c. Both lower bands of R are strict, by M and B. An upper v exit for R would give opposed-face width a≤v(R)−v(K)=c≤1. Therefore R is upper u:

    U+a≤c.

At D the upper u-band follows from A and the lower v-band from M, with increments .74c−.26s>0 and .35c+.09s>0. A lower u exit for D would now give a≤.74c<1. Consequently D is upper v:

    V+a≤−.26s.                                        (1)

The lower u-band of Y follows from M, and its two upper bands follow from B, with increments .65c−.15s>0, .1s≥0, and .1c>0. Its remaining lower v-band follows from (1), because

    v(D)−v(Y)=.74s+.5c≤sqrt(.7976)<1<a.

Thus Y is strict throughout this canonical sign.

Use next a nonpositive frame u=(c,−s), v=(s,c), again with c≥s≥0. At R its lower u-band follows from M, its upper u-band follows from B, and its lower v-band follows from B. Hence R is upper v:

    V+a≤s.                                            (2)

At K its lower u-band follows from M and its upper v-band follows from M, with increments .65(c+s)>0 and .65(c−s)≥0. If K were lower v, (2) would give a≤c≤1. Therefore

    U+a≤c+s.                                          (3)

At Y the lower u-band follows from M, the upper v-band from B, and the lower v-band follows from (2), because v(R)−v(Y)=.5c<1<a. Suppose Y were nevertheless excluded. Its only remaining exit is upper u, so

    U+a≤c+.5s.                                        (4)

At D the upper u-band and lower v-band follow from M: their increments are .09c+.35s>0 and .35c−.09s>0. A lower u exit would contradict (4), since

    u(Y)−u(D)=.74c+.5s≤sqrt(.7976)<1<a.

Thus D is upper v, V+a≤.26s. At F its upper v-band follows from M, and its lower v-band follows from this cap because v(D)−v(F)=c≤1<a. If F were lower u, (3) would imply a≤u(K)−u(F)=.74c<1. Hence F must be upper u:

    U+a≤.26c+s.

But the strict anchor B then requires

    c+.4s<.26c+s,
    .74c<.6s≤.6c,

which is impossible. Therefore (4) cannot hold, and Y's upper u-band is strict too. The two canonical signs include every square orientation, including the axial and diagonal endpoints, and every exterior face inequality was weak. ∎

## Actual MMMM consequence

In the original MMMM core of `C1092-MMMM-CONTINUOUS-REDUCTION.md`, Q5 has the three strict anchors M,A,B. Its excluded D lies in actual Q6; R is the actual Q10 origin proved in that chapter; K lies in actual corner Q1; and F is the actual Q9 compulsory auxiliary G5. Thus (3,1.5) is strictly in Q5. Diagonal transposition gives (1.5,3) strictly in Q7.

These two actual halfpoints transfer the remaining two wall origins through their respective actual corners. Apply Theorem 7 of `C1092-DIRECT-WALL-POINT.md` with b=.914 and ell=1.74:

| Target owner | Simultaneous transport | Corner's strict (1,b),(1,1) | Corner's excluded (1,1.5) | Boundary's strict (2,b),(ell,1) | Strict conclusion |
|---|---|---|---|---|---|
| Q9 | (x,y)↦(4−x,y) | (3,.914),(3,1) in Q1 | (3,1.5) in Q5 | (2,.914),(2.26,1) in Q9 | (2,1)∈Q9 |
| Q8 | (x,y)↦(y,4−x) | (.914,3),(1,3) in Q3 | (1.5,3) in Q7 | (.914,2),(1,2.26) in Q8 | (1,2)∈Q8 |

The walls, corner quadrants, common side, and disjoint interiors are exactly the original ones under each displayed symmetry. Both halfpoints were proved before these transfers. Together with the previously proved Q10 and Q11 origins, all four actual MMMM wall origins are now strict.
