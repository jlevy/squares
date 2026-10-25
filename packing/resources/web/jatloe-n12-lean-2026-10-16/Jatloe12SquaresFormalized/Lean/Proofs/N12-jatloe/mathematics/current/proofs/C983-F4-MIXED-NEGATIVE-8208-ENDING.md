# C983: a nonpositive mixed northeast square is impossible under label 8208

Every decimal is an exact rational. All points and segments described as owned are strict in their one named actual open square. Excluded points, supports, and genuine walls may be tangent. All squares retain their common physical side a>1. The continuous arguments below include their angle endpoints.

**Theorem.** There is no remaining C983 configuration with

    merged Q7=8208={F4,G3},
    northeast Q6=131232={F5,F7,G7},

in which Q6 has a nonpositive canonical angle.

This is an extension of the local calculations in C983-F4-TOP-ONLY-8208-ENDING.md. We give the actual source changes and the one support estimate which must be strengthened; a top-only northeast point is not used as a premise in this mixed branch.

## 1. The actual negative mixed northeast transfer

Use C983-F4-CENTRAL-REDUCTION.md, C983-F4-LEFT-ORIGIN-AND-CORNER-ROOT.md, and C983-F4-MERGED-CENTER.md. Write W=Q7,E=Q5,N=Q6,B=Q9. The original component reduction gives

    E=327936, N=131232, B=32832, Q2=0.

The actual top square is Q11=16392 and the actual right square is Q10=524800. The established strict points include

    (2,3) in Q11;
    (3,2.4),(3,2.56) in Q10;
    (2.5,2) in E;
    (2.42,2.16) in N;
    (2,2) in W;
    (1.82,1),(1.96,.76) in Q0;
    (1,1) in Q1, and excluded from Q0.

The bottom segment [2.26,2.8]×{1} is strict in the same actual B.

Apply the local Theorem 1 of C974-C976-FINAL-ANGLE-REDUCTIONS.md to the actual N after translating by (−2,−2). Its precise input is:

| Local datum | Original point | Actual source |
|---|---|---|
| Strict M=(.35,.35) | (2.35,2.35) | N's original marker |
| Strict F=(0,.26) | F5=(2,2.26) | N, label131232 |
| Strict G=(.26,1) | G7=(2.26,3) | This same N |
| Excluded P=(0,1) | (2,3) | Actual Q11 |
| Excluded D=(.26,0) | G6=(2.26,2) | Actual E |
| Excluded X=(.5,0) | (2.5,2) | Proved strict point in E |
| Nonpositive canonical angle | Same angle | Present branch |

It gives

    (2.5,3) strictly in N.                            (1)

Next apply Theorem 7 of C1092-DIRECT-WALL-POINT.md to the actual pair Q3,Q10 under

    (xi,eta)=(4−y,4−x), b=.914, ell=1.6.

Its corner points (1,b),(1,1) are the original (3.086,3),(3,3) in Q3. Its excluded corner point (1,1.5) is the original (2.5,3), strict by (1) in N. Its wall-square points (2,b),(ell,1) are (3.086,2),(3,2.4), the Q10 marker and G9. The first-quadrant corner walls are the genuine original y≤4,x≤4; the wall-square lower wall is original x≤4. Thus the theorem applies to the two actual disjoint squares and gives

    (3,2) strictly in Q10.                            (2)

This is the right origin required below. No point (2.525,2.125) in N has been assumed.

## 2. The southeast sign and the uniform bounds that survive

Translate by (−2,−2) for the remainder of the local support calculations. The actual W strictly owns

    P=(−.35,−.35), Q=(−.35,.35),
    F=(0,−.26), D_W=(−.26,0), O=(0,0).

The actual E strictly owns

    M=(.35,−.35), D=(.26,0), A=(1,−.26), X=(.5,0),

and excludes F and R=(1,0), with R supplied by (2). These are exactly the premises used in Section 2.1 of C983-F4-TOP-ONLY-8208-ENDING.md. Its sign proof uses neither the northeast label nor a northeast cap point.

In more detail, a nonnegative E would have

    A_E≤c, U_E≥−.26s,
    0<s/(1+c)<13/50, c>4/5, s<1/2.

The strict pairs P,M and Q,M restrict its normal cone to n_x>0,n_y<n_x. The E normals u_E and −v_E fail by the strict W points O,F. For a nonpositive W, its only possible normal fails by the exact expression (9) of that chapter. For a nonnegative W, its two normals and both relative angle orders fail by the exact expressions (10)–(12). Every point, cap, strictness, and relative-angle sign in those calculations is unchanged here. Consequently E is strictly negative for both canonical signs of W.

Give it the negative frame

    u_E=(c,−s), v_E=(s,c), c≥s>0.

Theorem 1 of C983-F4-BAR-ANGLE-REDUCTION.md applies with its other stated parameter pair

    (alpha,beta)=(.42,.16).

Its excluded K=(.42,.16) is the actual strict mixed-NE point (2.42,2.16) in N; the strict anchors, excluded F, and whole foreign bottom segment are the actual points stated above. Thus

    U_E≥.26s, V_E≥.8s−c, H_E≤.42s+.16c,
    0<s/(1+c)<3/20.                                  (3)

Here U_E,V_E are lower faces, and A_E=U_E+a,H_E=V_E+a are upper faces. The endpoint calculation for this actual parameter pair is

    c=391/409, s=120/409,
    (29/25)c−(19/50)s=10199/10225<1.

The actual R in (2) also forces H_E≤s: its lower u band follows from D and its upper u and lower v bands follow from A. Therefore the bounds needed throughout the support proofs are

    c>391/409>19/20, 0<s<120/409<3/10,
    U_E≥.26s>0, H_E≤s, H_E>.5s.                     (4)

The last inequality uses strict X in E.

## 3. The bottom midpoint exclusion transfers without alteration

The actual Q0 seed (1.96,.76), the W point F4, the E marker,G6,F8, the actual bottom bar and marker, and the bounds (4) are precisely all the inputs used in Section 3 of C983-F4-TOP-ONLY-8208-ENDING.md.

If C=(2,1.5) were strict in B, it would be excluded from E. In the translated chart, its two upper bands and H_E≤s force U_E≥.5s. The target S=(3,1.5) then has three strict E bands, and failure of its upper u band would give a≤c≤1. Hence S would be strict in E. The B marker and its putative C also give the strict bottom origin by convexity.

The strict pair C∈B,S∈E forces n_x>0 for a B-to-E separator. Its two E normals fail respectively against B's point (2.8,1) and the bound V_E<s−1<−.7. For a nonnegative B, one normal fails by that same point; the other fails if tan(p_B)≤.54. In the remaining interval, the three actual foreign points

    (.35,.65) in E, (0,.74) in W, (−.04,−.24) in Q0

in the B-origin chart force exactly the face alternatives (23)–(26) of the cited chapter. Their impossible widths are sqrt(4721/5000) and .98.

For a nonpositive B its first normal again fails by the actual bar endpoint. Its second normal has E-frame components alpha=ct−sd and k=st+cd. For alpha<0 the full lower E support is below −.665, whereas strict C in B has projection at least −.5. For alpha≥0, the exact support difference is (28) of that chapter, and its continuous upper bound (29) remains strictly negative solely from c>.95,s<.3. Thus every actual normal fails in either relative-angle order.

All these coarse bounds are present in (4). Therefore the identical local support argument gives

    (2,1.5) is excluded from actual B.                (5)

This conclusion assigns no strict owner to that point.

## 4. The outer southeast point: the larger cap and its replacement estimate

Suppose E excludes S=(3,1.5), or S=(1,−.5) in the translated chart. Exactly as in Section 4 of the cited top-only ending, its only possible exit is upper u. The negative-frame bounds give

    A_E≤c+.5s,
    0<U_E<c+.5s−1<eta,
    eta=42/409.                                      (6)

The function c+.5s increases on 0≤s/(1+c)≤3/20, since its angle derivative is .5c−s>.175>0. At the endpoint in Section 2 its value minus one is exactly 42/409. As before, the same supposition gives

    C=(0,−.5) strictly in E.                          (7)

Its lower u band follows from U_E<c+.5s−1≤.5s, its upper u band follows from D since .26c−.5s>.097>0, and both v bands follow from D and H_E≤s with opposite gap s+.5c<.8<1.

The actual W exclusions are still

    F_+=(0,.26), L=(−1,.26), J=(−1,−.4).

F_+ is its omitted F5, L is actual Q8's F1, and J is actual Q1's G0. Strict P,M and F,C again give n_x>0,n_y<0. The only candidate normals are −v_W,u_E for nonnegative W and u_W,u_E for nonpositive W.

For a nonnegative W, the same exact face comparisons give

    V_W≥−.5d, A_W≤.26r, H_W≤r+.26d,
    r>132/493>.26.

Its own normal fails by

    lower_E(−v_W)<2d eta<.26d<upper_W(−v_W),

since 2eta=84/409<13/50. Its E-normal support obeys precisely the two whole-interval bounds from (39)–(42) of the cited chapter:

    upper_W(u_E)>.106476 for .26<r≤.6,
    upper_W(u_E)>.11856 for .6≤r≤1/sqrt(2).

Both exceed the new eta. The smaller exact margin is

    .106476−42/409=387171/102250000>0.                (8)

Those bounds use only c>.95,s<.3 and the displayed W faces, so the larger cap in (6) creates no other change.

For a nonpositive W, the same complete face comparisons at F_+,C,J give

    H_W≤.26d, A_W≤.5r, r/d>9/35, r>.39.              (9)

In particular s<.3<r. Put

    k=cd+sr>0, h=cr−sd>0.

The support along the E normal again exceeds the same concave endpoint bounds (49)–(51) of the cited chapter. Thus it is greater than .11715, and the new exact margin is

    .11715−42/409=118287/8180000>0.                  (10)

It remains to replace the earlier crude estimate for the W normal, because the cap eta has increased. Retain the exact S-face inequality in (6) and strict X, which gives H_E>.5s. They give

    lower_E(u_W)=kU_E−hH_E
       <k(c+.5s−1)−.5sh.                            (11)

The difference between the right side and the strict W-point projection u_W(F)=.26r expands exactly as

    d[.5(c−1)²+.5cs]
       +r[.5s²−s+.5cs−.26].                        (12)

By r>.39 and d²+r²=1,

    d<.921,

because 1−.39²=.8479<.921²=.848241. Since c>.95 and c≤1, the first bracket in (12) is nonnegative and less than .00125+.5s. The second is at most .5s²−.5s−.26<0. It follows on the whole interval 0<s<.3 that (12) is strictly less than

    .921(.00125+.5s)+.39(.5s²−.5s−.26)
      =−.10024875+.2655s+.195s²
      <−.10024875+.2655(.3)+.195(.3)²
      =−2439/800000<0.                               (13)

The quadratic increases for s≥0, so its displayed endpoint bounds the entire interval. Thus lower_E(u_W)<.26r<upper_W(u_W), excluding the final actual normal.

Both signs of W and all their possible separating directions have been exhausted. The missing-S supposition is impossible:

    (3,1.5) strictly belongs to actual E.              (14)

The temporary point C in (7) was used only in the contradiction and only with its actual conditional owner E.

## 5. The bottom origin and the actual three-square ending

Apply Theorem 7 of C1092-DIRECT-WALL-POINT.md under (xi,eta)=(4−x,y), with actual corner Q2 and wall B=Q9, b=.914,ell=1.6. The original strict Q2 points (3,.914),(3,1) give its two corner anchors, and (14) gives its excluded (3,1.5). The original Q9 marker (2,.914) and F6=(2.4,1) give its wall-square anchors. Its first-quadrant and bottom-wall hypotheses are the genuine original x≤4,y≥0. Therefore

    (2,1) is strictly in actual B.                    (15)

Now apply the local Theorem 1 of C974-THREE-SQUARE-ENDING.md under (xi,eta)=(x−1,y−1), with K=Q0,W_local=B,C_local=Q2. Its full source ledger is:

| Local requirement | Actual C983 source |
|---|---|
| K owns (0,−.086),(.82,0),(.96,−.24) | Q0 owns (1,.914),(1.82,1),(1.96,.76) |
| K excludes (0,0) and has lower wall eta≥−1 | Proved Q0-missing root and original y≥0 |
| W_local owns (1,0),(1,−.086),(1.8,0) | Origin (15), actual Q9 marker and strong bottom advance |
| W_local excludes (1.35,.65) | Actual E marker (2.35,1.65) |
| W_local excludes (1,.5) | Direct exclusion (5) from this Q9 |
| W_local excludes (2,.5) | Strict E point (14) |
| C_local owns (2,0) and excludes (2,.5) | Q2 owns (3,1), while (3,1.5) is strict in E |
| C_local has walls xi≤3,eta≥−1 | Genuine original Q2 walls x≤4,y≥0 |

All three squares are actual members of the packing. Their common side and pairwise disjoint interiors are physical. The local theorem needs only the two stated exclusions from W_local; it does not require a strict owner of its point (1,.5). Thus (5) supplies precisely that premise. The theorem gives a contradiction and completes the claimed branch exclusion.

## 6. Remaining component scope

Together with C983-F4-TOP-ONLY-8208-ENDING.md, the only remaining possibility under merged label8208 is its mixed northeast component131232 with a strictly positive canonical angle. The axis is included in the nonpositive exclusion just proved. This chapter does not exclude that positive branch, label8240, or the F5-only merged label8224.
