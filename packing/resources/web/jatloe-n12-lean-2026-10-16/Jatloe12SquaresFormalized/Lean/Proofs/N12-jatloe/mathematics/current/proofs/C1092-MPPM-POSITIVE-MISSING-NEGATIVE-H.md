# C1092 MPPM: a positive missing-forward predecessor supplies the negative successor's halfpoint

Every terminating decimal is an exact rational. Owned points are strict in their named actual open square; an excluded point may lie on a face. The two squares below have the same side a>1. The local theorem uses neither an upper side bound nor a container wall. Its original application retains the actual corners and walls used to establish the predecessor's face profile.

## 1. A profile version of the positive-to-negative transfer

**Theorem 1.** Let C,E be two actual open squares with disjoint interiors. Suppose C has the nonnegative canonical frame

    u=(c,s), v=(-s,c), c>=s>=0, c^2+s^2=1.

Write U,V for its lower faces and A=U+a,K=V+a for its upper faces. Suppose C strictly owns M_C=(-.35,-.35) and its actual faces satisfy

    U>=-c-s, K<=s+.26c.                             (1)

Suppose E has the nonpositive canonical frame

    e=(d,-t), f=(t,d), d>=t>=0, d^2+t^2=1,

and strictly owns

    M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1),
    I=(0,-.26).                                    (2)

Then E strictly owns

    Y=(.5,-1).                                     (3)

The proof is the continuous Regime I argument from C1092-MIXED-NEGATIVE-H.md, with the actual normal cone supplied by different strict anchors. The complete argument is reproduced here to make the absence of a predecessor forward-point premise explicit.

## 2. The only possible exit of the target

Write L,W for E's lower faces and J=L+a,D=W+a for its upper faces. At Y the lower e- and f-bands follow from strict B1, with increments .1d>0 and .1t>=0. Its upper f-band follows from strict M_E, with increment

    f(M_E)-f(Y)=.65d-.15t>=.5d>0.

Thus if Y were absent from E it would be upper e, giving

    J<=.5d+t=:h.                                    (4)

The other strict anchors in (2) give the simultaneous bounds

    W<.26t-d=:r, D>-.26d=:z.                      (5)

These statements include t=0 because a zero comparison increment with a strict anchor still supplies a strict band.

## 3. The complete actual normal cone

Orient a proposed separating normal from C toward E. The strict marker pair gives n_x>0. Comparing the strict M_C with the strict E point B0 additionally gives

    .61 n_x-.65 n_y>0.                              (6)

Consequently n_y<(61/65)n_x. In particular E's transverse normal f=(t,d), whose second component is at least its first, cannot separate. Its opposite and both negative longitudinal directions have nonpositive first component. The signed transverse normal v of C also has second component at least its first. The separating-axis theorem therefore leaves at most

    u, -v, e.                                      (7)

Any listed direction that fails (6) at a canonical endpoint is harmlessly retained for exclusion. No face normal of an auxiliary hull is substituted for an actual square normal.

Set

    k=cd-st>=0, ell=ct+sd>=0, k^2+ell^2=1.

Thus u=k e+ell f, -v=ell e-k f, and e=k u-ell v. Every support below is the exact support of the same actual square, with only its genuine faces bounded. The coefficient of a before replacement by 1 is positive in every case; hence a nonnegative scalar margin suffices even for a weak separating equality.

## 4. The predecessor's downward normal

From (1), the upper C support in direction -v is at least a-s-.26c. Equations (4)-(5) bound the lower E support by ell(h-a)-kz. Separation would therefore require

    a(1+ell)<=1.26c+1.5s-k(.74d-.5t).              (8)

The difference between 1+ell and the right side is exactly

    1-Pc-Qs,
    P=.52-t+.74t^2+.5dt,
    Q=1-d+.5d^2+.74dt.                              (9)

Here P<=.52 because .74t+.5d<=sqrt(.7976)<1, and Q>=.5>0. If P>=Q, then Pc+Qs<=.52(c+s)<1.

If Q>=P, the function P cos p+Q sin p is nondecreasing for 0<=p<=pi/4: its derivative is Q(cos p-sin p)+(Q-P)sin p>=0. Thus Pc+Qs<1 follows from P+Q<sqrt(2). To verify the latter, put w=d+t and z0=d-t>=0. Directly,

    P+Q=1.52-w+.62w^2-.12w z0
       <=1.52-w+.62w^2
       <=2.76-sqrt(2)<sqrt(2).                      (10)

The quadratic increases on 1<=w<=sqrt(2), and the last strict inequality is 1.38<sqrt(2). Hence (8) is impossible.

## 5. The predecessor's longitudinal normal

The upper C support on u is at least a-c-s. The lower E support is at most k(h-a)+ell r. Separation would require

    a(1+k)<=1.5c-.24ell t.                          (11)

Subtract the right side from 1+k. The exact result is

    1-P1 c-Q1 s,
    P1=1.5-d-.24t^2,
    Q1=t(1-.24d).                                   (12)

Throughout the complete canonical range, d>7/10 and t<5/7. Therefore

    P1<.8,
    Q1<(5/7)(1-.24(7/10))=104/175<.6.

It follows that P1 c+Q1 s<.8c+.6s<=1. Thus (11) is impossible, including k=0 or ell=0.

## 6. The successor's longitudinal normal

The exact upper C support on e is kA-ell V. By (1), it is at least

    k(a-c-s)+ell(a-s-.26c).

Its comparison with L<=h-a would require

    a(1+k+ell)<=1.5d+1.26c ell.                    (13)

The difference between 1+k+ell and this right side is

    1-P2 d-Q2 t,
    P2=1.5-c-s+1.26cs,
    Q2=s-c+1.26c^2.                                 (14)

For w=c+s in [1,sqrt(2)],

    P2=.87-w+.63w^2<=2.13-sqrt(2)<.72,

because the quadratic is increasing on that interval. Also

    Q2-.63=(c-s)[.63(c+s)-1]<=0.

Consequently P2 d+Q2 t<.72d+.63t<=sqrt(.9153)<1. This contradicts (13).

All three actual sources in (7) are impossible. Therefore the assumed missing target has no possible separating line, contrary to disjointness. The target Y is strict in E. Every axial or diagonal canonical representative and every weak exterior face was retained, proving Theorem 1.

## 7. Literal application to the original all-ordinary MPPM entrance

Retain the original no-omission, all-four-ordinary entrance and the actual owner ledger of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md. Normalize a positive ordinary central that omits its forward point to Q4. Its strict ordinary anchors are F0,G0 and its original marker, and it omits G3. The ordinary halfpoint theorem supplies (1,1.5) in this actual Q4 and (2,1) in actual Q9.

Translate by (-2,-2). Set C=Q4 and E=Q5. The fully proved profile in C1092-MPPM-MISSING-POSITIVE-WALL-ORDER.md, Lemma 1, gives

    U>=-c-s, K<=1.086s<=s+.26c.                      (15)

For the final inequality use .086s<=.26c, which holds throughout c>=s>=0. The literal foreign sources of that profile remain the paired Q0 inner point and marker, the actual Q8 marker, the genuine G3 omission, and the entire actual Q9 far bar; no preceding wall origin is assumed.

Now suppose the ordinary successor Q5 owns its forward point F4 and has a nonpositive canonical angle. Its strict points in (2) are exactly

| Local point | Original point | Actual owner |
|---|---|---|
| M_E | Southeast marker (2.35,1.65) | Q5 |
| B0 | G5=(2.26,1) | Q5, ordinary pair |
| B1 | F6=(2.4,1) | Q5, ordinary pair |
| I | F4=(2,1.74) | Q5, the explicit forward-owned hypothesis |

Theorem 1 therefore gives Y=(2.5,1) strictly in Q5. The actual paired-corner transfer, Theorem 7 of C1092-DIRECT-WALL-POINT.md, applied to Q1,Q10 after the usual simultaneous quarter-turn with b=.914 and ell=1.6, then gives

    (3,2) strictly in actual Q10.                    (16)

Its foreign corner halfpoint is precisely the point just proved in Q5. Its strict corner anchors are the original paired Q1 markers/inner point, and its strict boundary anchors are the Q10 marker and G8=(3,1.6); all are prescribed by the original no-omission entrance. Simultaneous quarter-turns give this implication at every sector.

This chapter proves a strict halfpoint and the next actual wall origin at a positive-missing to nonpositive-forward-owned transition. It neither assigns the omitted G3 to another owner nor asserts that this transition has already been excluded.
