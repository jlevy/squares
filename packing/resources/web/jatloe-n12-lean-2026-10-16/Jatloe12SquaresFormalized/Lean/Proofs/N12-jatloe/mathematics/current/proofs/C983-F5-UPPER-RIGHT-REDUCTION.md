# C983 F5-only: the final upper-right entrance and exclusion of negative F8-only southeast squares

Every terminating decimal is exact. Owned points and segments remain strict in their named actual open squares, and exclusions permit tangency. The original side, actual walls and pairwise interior separations are retained.

The completed `C983-F5-TWO-RIGHT-AUXILIARIES-ENDING.md` leaves only

    W=Q7=8224={F5,G3},
    R=Q10=524800={F9,G9},
    N=Q6=131200={F7,G7},
    T=Q11=16392={F3,G4}.                          (1)

The southeast square E=Q5 has one of the six components displayed in Section 6 of that chapter. This chapter gives a common actual northeast entrance for all six and excludes two of the southeast components whenever their angle is negative.

## 1. The complete actual right bar and northeast points

The exact R component in (1) owns its original marker and G9 and excludes F8. Reflect Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md` in x=2 and apply it to this actual R. Its two strict anchors are precisely that marker and G9; its two exclusions are F8 omitted by its exact component and the northeast marker strictly in N. Its wall is the genuine x≤4. Hence

    (3,2.56) ∈ R strictly.                        (2)

This argument uses the exact exclusion of F8 from R and does not require F8 to have another owner. In particular it applies even to a southeast component which also omits F8. Convexity with the universal strict R origin (3,2) and its strict F9 gives

    {3}×[2,2.56] ⊂ R strictly.                    (3)

The universal top origin (2,3) belongs strictly to T; the northeast corner point (3,3) belongs strictly to paired Q3. Actual N strictly owns its marker and F7 and excludes F5, which belongs to W. The upper-square theorem, Theorem 3 of `OUTWARD-BAR-AND-UPPER-SPAN.md`, therefore applies using the whole sub-bar {3}×[2.26,2.56] of (3), and gives

    Y=(2.525,2.125) ∈ N strictly.                  (4)

The universal southeast crosspoint (2.5,2) is strict in E. Apply the top-only extension theorem in Section 3 of `C974-C976-CENTRAL-CROSSPOINTS.md` to N. Its owned marker,F7 and excluded F5,top origin,southeast crosspoint have exactly those actual sources. It gives

    (2.5,3) ∈ N strictly.                         (5)

Finally apply Theorem 1 of `TOP-ONLY-LEFT-POINT.md` to N, translated by (−2,−2). Its strict M,G,Y are N's original marker, G7 and (4). Its four exclusions are F5 in W, the top origin in T, the northeast corner in Q3, and the whole sub-bar {3}×[2.26,2.56] in R. Consequently

    (2,2.62) ∈ N strictly.                        (6)

Every source in (2)–(6) is universal across the six remaining southeast components; no merged F4 point is used.

## 2. A common full northeast face table

Translate by (−2,−2). Choose N's downward-right quadrant frame, allowing a relabeling of its original positive canonical frame as in Section 2 of `C983-F4-FULL-8240-ENDING.md`:

    u_N=(d,−r), v_N=(r,d), d,r>0, d²+r²=1.

Write its lower faces P,Q and upper faces J=P+a,H=Q+a. The complete two-sign face tables proved in Sections 2–3 of `TOP-ONLY-LEFT-POINT.md`, with the actual sources just supplied, give

    P≥−r, Q≥.26d,
    J≤d−.56r, H≤d+r,
    Q<.62d.                                      (7)

The last strict inequality is the new actual point (6). All four weak faces are complete-square faces, including the whole-bar argument in that source. If N originally has positive canonical frame (c_N,s_N),(−s_N,c_N), the precise relabeling is d=s_N,r=c_N, P=−(V_N+a),J=−V_N,Q=U_N,H=U_N+a. If N originally has negative sign, retain its canonical frame. Thus (7) covers both signs of the actual N.

The two opposite widths imply

    1<a≤d+.44r, 1<a≤.74d+r.

The exact half-angle factorizations, also displayed in Section 2 of the cited right-side ending, therefore give

    2 arctan(13/87)<p<2 arctan(11/25),
    p=angle(d,r).                                (8)

In particular the strictly positive lower endpoint is retained in every subsequent use of the profile.

## 3. Negative F8-only southeast components are impossible

**Theorem 1.** Under (1), if E has negative canonical angle, it cannot have either component

    65792={F8,G6}
    or 327936={F8,G6,G8}.                         (9)

**Proof.** Suppose (9). In the translated chart E strictly owns

    M=(.35,−.35), D=(.26,0), A0=(1,−.26),
    X=(.5,0),

by its original marker, G6,F8 and the universal southeast crosspoint. It excludes I=(0,−.26) by its exact F4 omission; this exclusion does not require I to lie in W. It excludes Y=(.525,.125) by (4), the right origin R0=(1,0) in actual R, and the whole actual Q9 bar [.26,.8]×{−1}.

Give E its assumed negative frame (c,−s),(s,c), c≥s>0. The local Theorem 1 of `C983-F4-BAR-ANGLE-REDUCTION.md` applies literally with (alpha,beta)=(.525,.125): every one of its strict anchors, two isolated exclusions and whole-bar hypotheses is supplied above. It proves

    U_E≥.26s, V_E≥.8s−c,
    H_E=V_E+a≤.525s+.125c.                         (10)

At the foreign R0, E's lower u band follows from D, its upper u band from A0, and its lower v band from A0. Thus it is necessarily upper v, giving H_E≤s. Combining the two v-face bounds in (10),

    1<a≤(9/8)c−(11/40)s.

That expression decreases over the positive canonical interval and equals 94083/94120<1 at half-angle7/48. Therefore

    0<s/(1+c)<7/48,
    c>2255/2353, 0<s<672/2353.                    (11)

The full actual right-side contradiction in Sections 2–8 of `C983-F4-FULL-8240-ENDING.md` now applies with these same actual E,N,R. Its entire local input list has the following present sources:

| Input to that continuous three-square proof | Present actual source |
|---|---|
| Negative E frame and its U,V,H,angle bounds | Equations (10),(11) and H_E≤s just proved |
| E owns M,D,A0,X | Marker,G6,F8 and universal southeast crosspoint |
| E excludes I,Y,R0 and the complete bottom bar | Exact F4 omission from E, equation (4), actual R origin, actual Q9 bar |
| N owns marker,G7,Y,(0,.62),(.5,1) | Original N component and equations (4)–(6) |
| N excludes F5,top origin,NE corner and whole right sub-bar | Actual W,T,Q3,R as in Section 1 |
| Both signs of N represented by its complete face table | Equations (7),(8) |
| R owns origin and (1,.56) in this chart | Universal right origin and (2) |
| R's genuine x≤2 wall in this chart | Original actual right container wall x≤4 |

The proof in those sections uses only this local input list. The old merged-label source was used there to establish the southeast sign; here the sign is the explicit hypothesis of the present theorem, and (10),(11) have been proved from the exact omission of F4 by E itself. No F4 ownership in W is imported.

The cited continuous proof excludes every pair of actual separating axes for E–R and N–R, in both N signs and both relative angle orders, by its stated full supports and real right wall. Its conclusion is the impossibility of these three actual squares. This contradicts (9), proving the theorem. ∎

## 4. Exact remaining signs and components

The remaining necessary southeast alternatives can consequently be organized as follows:

| Exact actual E component | Remaining canonical sign |
|---|---|
| 65552={F4,G6}, 327696={F4,G6,G8} | Strictly negative, by `C983-F5-INWARD-SIGN.md` |
| 65792={F8,G6}, 327936={F8,G6,G8} | Strictly positive, by Theorem 1 and the axial exclusion in the next paragraph |
| 65808={F4,F8,G6}, 327952={F4,F8,G6,G8} | Retain both signs until further argument |

For the middle row, a zero-angle square cannot satisfy the true F4 exclusion: both upper bands follow from strict D=(.26,0), its lower v band follows from strict M=(.35,−.35), so F4 forces U_E≥0. Its foreign right origin, using D and owned F8, forces A_E≤1. This gives a≤1. Thus no axial representative was left between the excluded negative and the remaining positive signs.

These are reductions for the final actual geometry (1). The common northeast points and faces (2)–(8), the actual merged center, left/top/right origins, and the already proved Q1-owned southwest corner are now available in every row. A final contradiction for all rows is still required.
