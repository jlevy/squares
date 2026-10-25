# C1092 MMMP: an ordinary southeast square beside a missing bottom origin

All terminating decimals are exact rational numbers. Owned points are strict. Exclusions, closure vertices and separating contacts may be equalities. The squares are the original actual open squares, of common side a>1; the angle arguments below cover complete continuous intervals.

**Theorem.** Suppose actual Q5 owns F8=(3,1.74) and G8=(3,1.6). If actual Q9 excludes its bottom origin (2,1), then Q5 has a strictly negative canonical frame. In coordinates translated by (-2,-2), write

    u=(c,-s), v=(s,c), c>=s>0, c^2+s^2=1,
    U,V for its lower faces, A=U+a,H=V+a.

Then Q5 strictly owns G6=(2.26,2), and

    U>=0,
    A<=c+.5s,
    V>=.8s-c,
    H<=.47s+.12c,
    0<s/(1+c)<13/100.                            (1)

If F4 is absent from Q5, the first bound improves to U>=.26s. No ownership of F4 is assumed in the theorem.

This is a conditional reduction of the missing-origin branch. It does not yet assert that the displayed negative profile is impossible.

## 1. Every point and whole bar belongs to an actual owner

Continue in the translated chart and write C=Q5. The stated ordinary pair and its original marker give the strict anchors

    M=(.35,-.35), P=(1,-.26), Q=(1,-.4).          (2)

The following excluded points have literal actual sources:

| Local point | Original point | Actual source |
|---|---|---|
| R=(1,0) | (3,2) | The universal right origin in Q10 |
| K=(1,-1) | (3,1) | The original paired southeast corner Q1 |
| D=(.47,.12) | (2.47,2.12) | Theorem1 of NORTHEAST-LOWER-TIP, in Q6 |
| O=(0,0) | (2,2) | The actual northwest center in Q7 |
| B0=(.26,-1) | G5=(2.26,1) | Universal strict ownership in Q9 |

Here and below the full filename of the cited tip theorem is
`C1092-MMMP-NORTHEAST-LOWER-TIP.md`.

The assumed absence of the bottom origin has two further actual consequences. First, the contrapositive of the paired-corner transfer, Theorem7 of `C1092-DIRECT-WALL-POINT.md`, reflected across x=2, puts

    Y=(1,-.5) strictly in Q1.                    (3)

Its corner inputs are the original (3,.914),(3,1); its boundary inputs are the actual Q9 marker (2,.914) and its universal F6=(2.4,1). Thus Y is excluded from C.

Second, Theorem11 of `C981-WALL-CYCLES.md`, in the chart (X,Y)=(x-2,1-y), applies to actual Q9 with e=.086,r=.4,z=.8. The numerical condition .8<2sqrt(2)-2 follows from 1.4<sqrt(2). Its missing origin therefore forces (2.8,1) strictly into Q9. Convexity with its actual G5 supplies the entire strict bar

    [.26,.8]x{-1} in Q9.                         (4)

The actual original bottom wall is precisely the required wall Y<=1 in that application. Thus both (3) and (4) concern the same original corner and boundary owners throughout.

## 2. A nonnegative southeast angle is impossible

Suppose first that C has frame u=(c,s),v=(-s,c), with c>=s>=0. At the excluded K, its lower-u band follows from M and its two upper bands from Q. The possible equality c=s or s=0 causes no issue because the comparison point is strict. Consequently K is lower v and

    V>=-s-c.

At R both lower bands follow from Q. An upper-v exit would give a<=c<=1, by the lower-v face at K. Hence R is upper u and A<=c.

At D the upper-u band follows from P, since

    u(P)-u(D)=.53c-.38s>=.15c>0.

Its lower-v band follows from M, with increment .47c-.12s>=.35c>0. If D were lower u, its opposed face at R would give a<=.53c-.12s<=.53. Thus D is upper v:

    H<=.12c-.47s.

At Y the lower-u band follows from M and both upper bands from Q. Its only possible exit would be lower v, V>=-s-.5c. The two v faces would imply

    a<=.62c+.53s<=sqrt(.6653)<1,

which is impossible. Thus the entire nonnegative canonical sign, including both endpoints, has been excluded.

## 3. The negative face profile and the genuine inward auxiliary

Give C the negative frame in the theorem. At R its lower-u band follows from M, its upper-u band from P and its lower-v band from P. Therefore

    H<=v(R)=s.                                  (5)

At Y the lower-u band follows from M and its upper-v band from Q. A lower-v exit would combine with (5) to give a<=.5c<1. Thus Y is upper u:

    A<=c+.5s.                                   (6)

At D the upper-u band follows from P, and its lower-v band from M. A lower-u exit would combine with (6) to give

    a<=.53c+.62s<=sqrt(.6653)<1.

Hence

    H<=.47s+.12c.                               (7)

We next show that J=(.26,0), the original G6, is strict in this actual C. If it were absent, Theorem1 of `ORDINARY-MARKER-HALFPOINT.md` would apply with d=.086. Its three strict anchors are exactly (2); its four excluded points are the hypothesized absent J, the original actual right marker (1.086,0) in Q10, K in Q1, and B0 in Q9. It would put Y strictly in C, contradicting (3). Thus J is indeed strict.

To establish U>=0 without assigning an owner to F4, let F=(0,-.26). If F is strict in C, then O has both v bands from F,J and its upper-u band from M. Its actual exclusion in Q7 forces O to be lower u, U>=0.

If F is absent from C, its upper-u band follows from M and its upper-v band from J. A lower-v exit would combine with (7) to give

    a<=.47s+.38c<=sqrt(.3653)<1.

Therefore F is lower u, and U>=.26s>=0. This proves the claimed first bound in either exhaustive ownership alternative.

## 4. The whole bottom bar fixes the lower v face

At its excluded left endpoint B0=(.26,-1), the lower-u band follows from strict J, and its upper-v band from M. An upper-u exit would contradict strict Q: it would imply

    c+.4s<.26c+s,
    .74c<.6s<=.6c.

Thus B0 is lower v and

    V>=.26s-c.                                  (8)

Let T=(.8,-1), the other endpoint of the actual bar (4). Its lower-u and upper-v bands follow from M, with positive increments .45c+.65s and .65c-.45s. If T were upper u, then

    A<=.8c+s.

Strict Q would require .2c<.6s, so the angle magnitude would exceed arctan(1/3).

Consider the lowest closed vertex of C,

    Z=(cA+sV,-sA+cV).

The already proved U>=0 and (8) imply

    Z_x>=ac+.26s^2-cs>c+.26s^2-cs>=.33>.26.      (9)

For the last bound, use cs<=1/2 and

    1-c=s^2/(1+c)<=.6s^2,

valid because c>=1/sqrt(2)>2/3. They give
c+.26s^2-cs>=.5-.34s^2>=.33.

The proposed upper-u exit at T and (7) give

    Z_x<=.8+s(1.12c-.33s-a)<.8.                  (10)

Indeed 1.12c-.33s decreases strictly with the negative angle magnitude. At arctan(1/3) it equals 3.03/sqrt(10)<1, since 3.03^2<10. It is therefore less than1 in the present strict angle regime, and a>1.

Also U>=0 and (7) give

    Z_y<=-a(c+s)+.47cs+.12c^2<-1.               (11)

For the final comparison define

    J(theta)=c+s-1-.47cs-.12c^2.

Its derivative is

    J'=(c-s)[1-.47(c+s)]+.24cs>0

throughout arctan(1/3)<=theta<=pi/4. Here .47sqrt(2)<1, and the last term is positive. At the left endpoint,

    J=4/sqrt(10)-1.249>0,

because 10(1.249)^2=15.60001<16. This proves (11).

By (9)--(11), the segment from strict M to Z crosses y=-1 before reaching Z, at an abscissa strictly between .26 and .8. Every point before the closure vertex on this segment is in the interior of C: its four strict linear bands follow by interpolation from M. The crossing therefore lies strictly both in C and in the actual Q9 bar (4), a contradiction.

The upper-u alternative for T has failed. Its only remaining exit is lower v, which proves

    V>=.8s-c.                                   (12)

The proof has used the complete actual bar, rather than the two endpoint exclusions.

## 5. The exact final angle interval and scope

Combining (7),(12),

    a<=1.12c-.33s.                               (13)

The right side decreases strictly over the whole canonical interval. At half-angle z=13/100 its value is exactly

    1.12(9831/10169)-.33(2600/10169)
      =253818/254225<1.

Since a>1, (13) forces z<13/100, completing all conclusions in (1).

The axial negative endpoint was already covered by the nonnegative-sign contradiction, so s>0. Every face exit used above was weak; strict positivity came from actual owned comparison points, a>1, or the displayed strict scalar margins. No endpoint tangency was discarded.

For the remaining original right component Q10=524800, this theorem supplies a concrete profile whenever its southeast neighbor owns F8,G8 and the bottom origin is absent. It retains actual ownership of the additional G6, the whole Q9 bar and the strict paired-corner halfpoint Y. A subsequent contradiction must use these same owners and faces; the conditional negative profile alone is not a completed exclusion of that remaining branch.
