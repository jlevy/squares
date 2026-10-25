# C1092 MPPM: the actual upper core with exactly one omitted wall auxiliary

Every terminating decimal is an exact rational. We retain the twelve actual original open squares, their common side 1<a<=1.001, disjoint interiors, genuine container [0,4]^2, full original component lists, and closed MPPM center signs. Every stated owned point is strict. A point excluded from a square may touch its boundary.

This chapter treats exactly one of the four omissions in Section7 of `C1092-MPPM-MIXED-WALL-CENTER.md`. A simultaneous quarter-turn normalizes that omission to F2 absent from original Q9. The other three indicated auxiliaries are then genuinely owned: G8 in Q10, F7 in Q11, and G1 in Q8. The already proved mixed-wall theorem applies before this chapter.

## 1. One simultaneous transpose and its actual owner ledger

Transpose the entire physical configuration by

    (x,y)=(y_original,x_original).

Give the transformed actual owners the following names. These are names for the original squares after this one isometry, not new squares.

| Name in the transposed chart | Original actual owner | Location |
|---|---|---|
| W | Q5 | Northwest central |
| N | Q6 | Northeast central |
| S | Q4 | Southwest central |
| E | Q7 | Southeast central |
| L | Q9 | Left boundary |
| B | Q8 | Bottom boundary |
| R | Q11 | Right boundary |
| T | Q10 | Top boundary |
| K_SW,K_SE,K_NE,K_NW | Q0,Q3,Q2,Q1 | The four corresponding corner owners |

Auxiliary symbols in this chapter denote their usual coordinates in the transposed chart. For example G1=(1,2.4), regardless of its original name. The complete compulsory input ledger is

| Transposed datum | Original datum | Actual source |
|---|---|---|
| F5,G3 in W | G6,F4 in Q5 | MIXED-WALL-CENTER, Theorem1 |
| [1.5,2]x[2,2.5] and (1.39,2.61) in W | [2,2.5]x[1.5,2] and (2.61,1.39) in Q5 | The same theorem, including both crosspoints and its diagonal extension |
| F7,G7 in N | G9,F9 in Q6 | The same theorem |
| L exactly {F0,F1,G1} | Q9 exactly {G2,G5,F6} | The same theorem, exact original label36928 |
| {1}x[1.61,2.4] in L | [1.61,2.4]x{1} in Q9 | The same actual-square bar |
| G0 excluded from L | F2 excluded from Q9 | The normalized omission |
| T exactly {F3,G4} | Q10 exactly {G8,F8} | The same theorem, exact original label262400 |
| (1.44,3) in T | (3,1.44) in Q10 | MIXED-WALL-CENTER, Section3 |
| F9 and {3}x[2.22,2.39] in R | G7 and [2.22,2.39]x{3} in Q11 | The original wall-sign chord |
| G9 in R | F7 in Q11 | There is no second indicated omission |
| G5 and [2.22,2.39]x{1} in B | F1 and {1}x[2.22,2.39] in Q8 | The original wall-sign chord |
| F6 in B | G1 in Q8 | There is no second indicated omission |

The transposed genuine center conditions are

    center_y(L)<=2, center_x(B)>=2,
    center_y(R)>=2, center_x(T)<=2.                    (1)

In particular the first inequality has the opposite direction from the MMMP left-square condition. No conclusion requiring the latter condition is imported below. The point (2,3) in T is not a premise or a conclusion of this chapter.

## 2. The northeast sign and its full face bounds

**Theorem 1.** In the transposed chart N has a strictly positive canonical frame. In centered coordinates obtained by subtracting (2,2), write

    u_N=(b,t), v_N=(-t,b), b>=t>0, b^2+t^2=1,
    U_N,V_N for its lower faces,
    A_N=U_N+a, H_N=V_N+a.

Then

    U_N>=.4t, V_N>=.4b-t,
    A_N<=b+t, H_N<=1.086b,                            (2)
    a<=.686b+t, z_N=t/(1+b)>157/843.                  (3)

The stronger U_N>=.5t also holds.

### 2.1. The actual two-square sign theorem

Apply local Theorem1 of `C1092-MMMP-NORTHEAST-ANGLE.md`, which has no wall, boundary-origin or center premise. In terms of original coordinates its simultaneous chart is

    (X,Y)=(2-x_original,y_original-2), C=Q5, B_local=Q6.

Its entire input table is literal:

| Local datum in that theorem | Original coordinates | Actual owner |
|---|---|---|
| O,A,D in C | (2,2),(2.5,2),(2,1.5) | Q5, the proved strict half-unit rectangle |
| M_C=(-.35,-.35) | (2.35,1.65) | Q5's original marker |
| G=(.35,-.35), excluded from C | (1.65,1.65) | Q4's original marker |
| M=(-.35,.35), strict in B_local and excluded from C | (2.35,2.35) | Q6's original marker |
| F=(-.39,-1), excluded from C | (2.39,1) | Q9's strict whole bar |
| H1,H2 in B_local | F9=(3,2.26), G9=(3,2.4) | Q6, the mixed-wall theorem |
| I=(-.39,0), excluded from B_local | (2.39,2) | Q5's strict rectangle |
| J=(-.39,1), excluded from B_local | (2.39,3) | Q11's actual wall-sign chord |
| W_local=(-1.086,0), excluded from B_local | (3.086,2) | Q10's original marker |
| K=(-1,1), excluded from B_local | (3,3) | Actual paired corner Q2 |
| A=(-.5,0), excluded from B_local | (2.5,2) | Q5's strict rectangle |

This theorem excludes every nonpositive canonical representative of B_local, including the diagonal representative. The local chart differs from the centered transposed chart by a quarter-turn, which preserves the canonical sign after relabeling the two faces. Thus N has the claimed strictly positive angle.

### 2.2. The four actual exterior faces

In centered transposed coordinates N strictly owns

    M=(.35,.35), P=(.26,1), Q=(.4,1),

and excludes

    I=(0,.4), J=(1,.4), C=(1,1), D=(0,1.086).

Their actual distinct owners are W,R,K_NE,T, respectively, by Section1 and the original corner/marker data.

At I the upper u band follows from M, the lower v band from M, and the upper v band from P. Their positive projection gaps are .35b-.05t, .05b+.35t and .6b-.26t. Hence I is lower u and U_N>=.4t.

At J the lower u band follows from M and the upper v band from P. An upper u exit would oppose the face at I with width a<=b<=1. Therefore J is lower v, giving V_N>=.4b-t.

At C both lower bands follow from the strict point M, with a possibly equal v projection only when b=t. An upper v exit would oppose the face at J with width a<=.6b<1. Hence C is upper u and A_N<=b+t.

At D the lower v band follows from M. A lower u exit would oppose the C face with width a<=b-.086t<=1. An upper u exit would oppose the I face with width a<=.686t<1. Thus D is upper v and H_N<=1.086b. This proves all four bounds in (2), with every equality of exterior faces allowed.

The two v faces give the width in (3). Its exact half-angle identity is

    (1+z_N^2)(.686b+t-1)
        =(1-z_N)(843z_N-157)/500.

Because a>1, the left side is positive and z_N>157/843 follows.

Finally I_1=(0,.5) is also strict in actual W. Its upper u band in N follows from M with gap .35b-.15t>0, its lower v band follows from M with gap .15b+.35t>0, and its upper v band follows from P with gap .5b-.26t>0. It is therefore lower u and U_N>=.5t. This strengthening does not change any of the weaker bounds used subsequently. This proves Theorem1.

## 3. Further upper points and the exact scope of the local support transfer

**Theorem 2.** The same actual squares have the strict points

    (1.99,2.54) in W,
    (2.14,2.5) in N,
    (1.2,2.16), (1.19,2.2), (1.15,2.4) in W.          (4)

If W has a nonpositive canonical frame (d,-r),(r,d), then

    d+r<1.13, r<.14, d>.99.                           (5)

Writing A,H for its upper faces in centered transposed coordinates and using N's frame from Theorem1, actual W--N disjointness can then hold only on the single source

    alpha A+kH<=b+t-a,
    alpha=bd-tr>0, k=br+td>0.                         (6)

If W has a positive canonical frame (d,r),(-r,d), it satisfies r/d<7/8.

**Proof.** First apply Corollary3 of `C1084-DUPLICATE-POINT.md` directly in the original chart to Q5. Its strict marker,F4,G6 and its excluded southwest/northeast markers are the literal original data. Its remaining exclusion F6=(2.4,1) is strict in Q9 by the mixed-wall theorem. Its target (2.54,1.99) transposes to the first point of (4).

Sections2--5 of `C1092-MMMP-UPPER-STRICT-POINTS.md` are local calculations on the same two actual upper squares. Their complete inputs here are W's strict rectangle, its original marker, the foreign southwest and northeast markers, N's ordinary top pair, all four bounds (2), the just-proved W point (1.99,2.54), and the already proved W point (1.39,2.61). Each has its distinct actual source in Sections1--2. No boundary center inequality occurs in those calculations. Therefore those sections give the next three points of (4) and (5).

For explicit face transport of the support conclusion, that calculation uses the quarter-turn (X,Y)=(-y,x) from centered transposed coordinates. Its central upper faces are a-H,A; its northeast lower transverse face is U_N. Its equation(11), a(1+k)<=b+t+k(a-H)-alpha A, is consequently exactly (6). The other three face-normal axes and both orders on the retained axis are eliminated in that cited calculation. Thus (6) concerns the full two actual squares, not merely their point hulls.

Finally the proof in Sections2--3 of `C1092-MMMP-NORTHWEST-LEFT-TIP.md` uses exactly the rectangle, long diagonal point, proved N point (2.14,2.5), negative-angle bound (5), and the genuinely foreign left endpoint (1,2.39). This endpoint is strict in the one actual L by Section1. Its positive-angle face proof gives 1<a<=1.35d-.04r, hence r/d<7/8, and its four strict target bands give (1.15,2.4). Every input has now been listed independently of any MMMP left-center sign. This proves Theorem2.

## 4. The northeast outer halfpoint, right origin and exact northeast component

**Theorem 3.** In the transposed chart,

    (2.5,3) is strict in N,
    (3,2) and {3}x[2,2.4] are strict in R,
    N has exactly the pair {F7,G7}.                    (7)

**Proof.** The proof in `C1092-MMMP-RIGHT-ORIGIN.md` consists of two local theorems with no wall-center or top-origin premise. Apply its ordinary-marker halfpoint theorem to N. Its strict marker and ordinary pair are Section1. Its four exclusions F5, the top marker, paired northeast corner and F9 have actual owners W,T,K_NE,R, respectively. This is exactly the source table in that proof, with the roles replaced by the named transposed actual squares. It gives (2.5,3) strict in N.

Theorem7 of `C1092-DIRECT-WALL-POINT.md`, under the map (xi,eta)->(4-eta,4-xi), with b=.914 and ell=1.74, now applies to K_NE and R. The corner's actual paired point and two original marker/wall data are unchanged by the global transpose. Its excluded halfpoint is the N point just proved. R's actual anchor is F9, and its marker and right wall are original genuine data. The conclusion is (3,2) strict in R. Its strict G9 from Section1 gives the entire segment in (7) by convexity.

Suppose N also owned G6=(2.26,2). Translate the whole chart by (-2.26,-2). The strict G6,G7 become O=(0,0),P=(0,1) of Theorem1 in `UNIT-SPAN-BETWEEN-TWO-BARS.md`. Its five excluded points have the actual sources

| Local point | Transposed point | Actual owner |
|---|---|---|
| L_0 | F5=(2,2.26) | W |
| R_0 | F9=(3,2.26) | R |
| L_1 | (2,2.39) | W's strict rectangle |
| R_1 | (3,2.39) | R's wall-sign chord |
| L_2 | (2,2.5) | W's strict rectangle |

The local theorem excludes this ownership of G6.

For completeness the original Q6 component inspection is only a single-owner filter. Require its original F9,G9 and remove the actual foreign original F4,G6 in Q5, F7,G7 in Q11 and F8,G8 in Q10. Its complete original M_6 list leaves exactly

    524800={F9,G9}, 524832={F5,F9,G9}.

The hypothetical extra original F5 is precisely the transposed G6 just excluded. Thus original Q6 is exactly524800, and after transpose N is exactly {F7,G7}, proving (7). No joint vector catalogue is used.

## 5. The actual mixed left square has the opposite forced tilt

**Theorem 4.** In centered transposed coordinates L has a strictly positive canonical frame

    u_L=(d,r), v_L=(-r,d), d>r>0, d^2+r^2=1,
    d+r>5/4.                                          (8)

Let J be its upper u face and V its lower v face. Then

    J<=-.35(d-r), V>=r-.4d,
    J>-d+.4r,
    rJ+dV<=-a(d-r)/2.                                (9)

**Proof.** Reflect the centered transposed chart through x=0. The actual L then owns (1.086,0),(1,-.39),(1,.4), excludes (1,-.4) and the marker (.35,.35), has its actual closure in x<=2 and has center ordinate at most zero by (1). These are exactly all inputs of Theorem1 of `MIXED-WALL-HALFANGLE-CROSSING.md`. That theorem gives its strictly negative frame, d+r>5/4 and lower faces L_0>=.35(d-r), V_0>=r-.4d, L_0<d-.4r.

Under the reflection, L_0=-J and V_0=V in the frame of (8). These are the first three statements of (9). Finally the genuine center ordinate in the unreflected chart is

    r(J-a/2)+d(V+a/2)<=0,

which is exactly the last inequality in (9). The diagonal and axial endpoints have already been excluded by the cited all-angle theorem. This proves Theorem4.

## 6. Scope

All conclusions in this chapter hold in the one normalized omission family before any further ownership selection for the remaining central or wall squares. They supply actual full-square supports, strict target points, and the literal single-owner component reduction. In particular the left square's center inequality has been retained in its correct direction throughout. The missing top origin (2,3) remains a separate obligation unless a subsequent argument bypasses it.
