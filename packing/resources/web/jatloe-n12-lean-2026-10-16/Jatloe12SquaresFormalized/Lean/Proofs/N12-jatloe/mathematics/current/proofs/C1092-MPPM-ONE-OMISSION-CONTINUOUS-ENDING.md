# C1092 MPPM: complete exclusion of the one-omission family

Every terminating decimal is an exact rational. We retain the entire original C1092 entrance, its twelve actual open squares of common side 1<a<=1.001, pairwise disjoint interiors, genuine container walls, and closed MPPM center signs. Owned points remain strict; an omitted point, exterior face or separating support may be tangent.

**Theorem.** An original C1092 MPPM configuration cannot have exactly one of the four indicated wall omissions

    F2 absent from Q9, G8 absent from Q10,
    F7 absent from Q11, G1 absent from Q8.

Together with Section7 of `C1092-MPPM-MIXED-WALL-CENTER.md`, this excludes every original MPPM configuration with at least one of these omissions. The no-omission family is a separate obligation.

The proof transports already proved local actual-square arguments only after supplying their full actual premises. In particular it does not identify MPPM with MMMP, or impose the MMMP left-center sign on an MPPM square.

## 1. The normalized actual owners and the repaired dependency entrance

The simultaneous quarter-turn symmetry in Section7 of the mixed-wall theorem normalizes the sole omission to original F2 absent from Q9. Transpose the entire configuration, as in `C1092-MPPM-ONE-OMISSION-UPPER-CORE.md`, and use the following actual names:

    W=original Q5, N=original Q6, S=original Q4,
    E=original Q7, L=original Q9, B=original Q8,
    R=original Q11, T=original Q10,
    K_SE=original Q3, K_NE=original Q2.

The coordinates below are transposed physical coordinates; auxiliary symbols refer to their usual coordinates in that chart. When the coordinates are centered, the same translation (-2,-2) is applied to every actual owner simultaneously.

The upper-core chapter and the independent `C1092-MPPM-ONE-OMISSION-TOP-ORIGIN.md` give all of the following before any right-component hypothesis:

| Actual datum | Genuine source in the normalized original configuration |
|---|---|
| W strictly owns [1.5,2]x[2,2.5], its marker, F5,G3 and (1.39,2.61) | Original Q5's full inward-square conclusion in MIXED-WALL-CENTER |
| W strictly owns (1.99,2.54),(1.19,2.2),(1.15,2.4) | ONE-OMISSION-UPPER-CORE, Theorem2 |
| N exactly owns {F7,G7}, is strictly positive, and owns (2.5,3) | ONE-OMISSION-UPPER-CORE, Theorems1 and3 |
| L strictly owns G1=(1,2.4) and (1,2) | Original Q9's whole transposed mixed bar |
| B strictly owns F6=(2.4,1),G5=(2.26,1) | Original Q8's nonomitted G1 and wall-sign F1 |
| R strictly owns F9=(3,2.26),G9=(3,2.4),(3,2) and {3}x[2,2.4] | Original Q11's wall-sign G7, nonomitted F7, and the proved actual corner transfer |
| T exactly owns {F3,G4}, strictly owns (1.44,3),(2,3) | Original Q10's exact ordinary pair, the mixed-wall advance, and the new one-omission top-origin theorem |
| B has its real bottom wall and center_x(B)>=2 | Original Q8's real left wall and original Y8>=2 after transpose |
| R has its real right wall and center_y(R)>=2 | Original Q11's real top wall and original X11>=2 after transpose |
| K_SE,K_NE have their usual paired points, original corner markers and genuine container walls | Original paired seeds of Q3,Q2 after the same transpose |

The actual W is strictly positive by `C1092-MPPM-ONE-OMISSION-NORTHWEST-SIGN.md`. Its positive frame (d,r),(-r,d) satisfies

    r/d<7/8.                                           (1)

This estimate is the local full-interval conclusion in Theorem2 of the upper-core chapter.

The transposed L retains center_y(L)<=2. Its actual origin, full bar, required strict points and the top origin have all been proved independently with this correct sign. No argument after this section uses L's center coordinate at all.

## 2. The sharp actual northeast cap and its lower tip

Center the common chart at (2,2). Write N's positive frame and faces as

    u_N=(b,t), v_N=(-t,b), b>=t>0, b^2+t^2=1,
    U_N,V_N lower faces, A_N=U_N+a,H_N=V_N+a.

The upper-core theorem supplies U_N>=.4t, V_N>=.4b-t and A_N<=b+t. The newly proved strict T origin is O_T=(0,1), genuinely excluded from N. Strict G7=(.26,1) gives its upper u band and lower v band. If O_T were lower u, U_N>=t and A_N<=b+t would give a<=b<=1. Thus it is upper v and H_N<=b. We have the simultaneous actual table

    U_N>=.4t, V_N>=.4b-t,
    A_N<=b+t, H_N<=b.                               (2)

The two v faces imply a<=.6b+t. With z_N=t/(1+b),

    (1+z_N^2)(.6b+t-1)=2(1-z_N)(4z_N-1)/5.

Since a>1,

    z_N>1/4, b<15/17, t>8/17.                       (3)

The point P_N=(.47,.12) is strict in this same actual N. Its four band margins, respectively lower u, upper u, lower v and upper v, follow from (2) with the lower bounds

    a-.53b-.88t,
    a-.47b+.28t,
    a-.88b-.47t,
    a+.28b-.53t.                                     (4)

All are positive. The first uses .53b+.88t<=1.41/sqrt(2)<1 on the canonical interval, because that positive sinusoid increases up to pi/4. The second is at least a-.47. The third uses .88^2+.47^2=.9953<1. The fourth is at least a-.25t, since b>=t. This is the entire local proof of Theorem1 in `C1092-MMMP-NORTHEAST-LOWER-TIP.md`, now with every cap independently supplied in the one-omission family.

Thus (2)--(4), the actual marker M_N=(.35,.35), F7=(.4,1), and the exact ordinary northeast component are available without a right-near hypothesis.

## 3. A short original covering argument excludes the right inward auxiliary

We next prove that R excludes G6=(2.26,2). The transposed original covering rows for the actual E are

    E owns a point of {F4,F6,F8},
    E owns a point of {G5,G6,G8}.                      (5)

These are exactly original Q7's G-covering triple {G3,G1,G4} and F-covering triple {F1,F5,F3}, respectively, after the transpose. They do not require every auxiliary to have an owner.

Suppose G6 were strict in R. The actual B owns G5, so the second row in (5) forces G8 in E. If F8 were absent from E, the first row and actual F6 in B would force F4 in E. The untransformed local theorem `MIXED-SPAN-FOUR-POINTS.md` would then have its strict pair F4,G8 in E and its four exclusions G6 in R, F8 absent by supposition, and G5,F6 in B. This is impossible. Hence F8 is strict in E.

Now apply local Theorem1 of `C1092-MMMP-RIGHT-INNER-EXCLUSION.md` to the actual N,R in centered transposed coordinates. Its complete source map is

| Local premise of that theorem | Actual source here |
|---|---|
| Its central strict M=(.35,.35), B=(.26,1), C=(.4,1) | N's marker,G7,F7 |
| Its central exclusions P=(0,1.086),Z=(0,.5) | Actual T marker and actual W rectangle |
| Its right strict A=(.26,0),S=(1.086,0),D=(1,.4) | G6 in R by supposition, original R marker, genuine G9 in R |
| Its right exclusion F=(1,-.26) | F8 just proved strict in E |

The theorem has no wall or center premise. It contradicts these two full actual squares. Therefore

    G6 is excluded from R.                            (6)

Only one original component row is now filtered. In original coordinates require F7,G7 in Q11 and remove its components meeting G1 in actual Q8, G9 in actual Q6, or F5, whose absence from Q11 is (6) after transpose. The complete original M_11 row leaves exactly

| Original Q11 label and exact points | Exact transposed R label and points |
|---|---|
| 131200={F7,G7} | 524800={F9,G9} |
| 147584={F7,G4,G7} | 525056={F8,F9,G9} |
| 147592={F3,F7,G4,G7} | 787200={F8,F9,G8,G9} |

This is a literal single-owner inspection of the original component list. No joint catalogue or subsequent numerical pruning is used.

## 4. What actual right-near ownership would force

Suppose now that F8 is strict in R. The first row in (5), with F6 already in B, forces F4 in E. If G6 were absent from E, the second row would force G8, and the same mixed-span theorem with strict F4,G8 and excluded G6,F8,G5,F6 would be a contradiction. Thus

    F4,G6 are strict in E.                            (7)

The local geometric proof in Sections1,3,4 of `C1092-MMMP-RIGHT-NEAR-BOTTOM-ORIGIN.md` now applies. To make its scope explicit, in centered transposed coordinates its simultaneous quarter-turn is (X,Y)=(-y,x). Its C is this actual E, and its wall W_local is this actual B. Every independent input to that proof is present:

| Input of the right-near sign/origin proof | Actual source here |
|---|---|
| Strict central marker and inward pair | E's original marker and (7) |
| Missing central origin | Strict O=(0,0) in W's actual rectangle |
| Strict right-near point and right origin | F8 and (3,2) in the same actual R |
| The whole right segment {3}x[1.74,2] | Convexity in that same R |
| Strict bottom marker,G5,F6 | The same actual B, Section1 |
| Bottom's real wall and center_x(B)>=2 | The genuine transformed original conditions in Section1 |
| The actual southeast paired corner and its walls | K_SE, the transformed original Q3 |
| Status of G8 relative to E | The two exhaustive owned/absent alternatives, kept separate below |

For clarity about the two alternatives: when G8 is absent from E, the local R=(1,.4) exclusion in Lemma1 of that chapter is supplied by F6=(2.4,1), which is strict in the actual B. Under (X,Y)=(-y,x), G8 instead maps to A0=(.4,1); its absence is retained for the later half-angle argument. The lemma's full-square inward crossing theorem uses precisely B's correct center sign and actual wall, and contradicts the actual short R bar if E had a nonpositive angle. Its subsequent missing-bottom-origin argument uses the genuine paired K_SE corner and local Theorem1 of `C1092-MMMP-DOUBLE-RIGHT-BOTTOM-ORIGIN.md`, with B's actual marker,pair,wall and supposed missing origin. When G8 is strict in E, Theorem1 of `INWARD-OUTER-ARM-HALFPOINT.md` uses the strict E inward pair and G8, foreign F8 in R, foreign center in W and the whole B bar [2.26,2.4]x{1}; its actual corner transfer again gives B's origin. Neither proof uses L or its center.

Consequently, in both alternatives,

    E has strictly positive frame (c,s),(-s,c),
    (2,1) belongs strictly to B.                      (8)

If G8 is absent from E, Section4 of the right-near proof additionally gives

    0<s<.21, c>.97.                                  (9)

Its all-angle half-angle-point argument uses G8 only as an exclusion from E, and the whole actual B bar from its new origin to F6. No right owner for the absent G8 is presumed. In either alternative the actual B now strictly owns

    [0,.4]x{-1} in centered coordinates.              (10)

These are exactly the conditional sign and origin consequences needed in the next two sections. No bottom origin is asserted in the F8-absent branch.

## 5. The alternative with G8 absent from E is impossible

Continue to suppose F8 is in R and now suppose G8 is absent from E. Let A_E,H_E be E's upper faces, U_E=A_E-a,V_E=H_E-a, and z=s/(1+c). Its actual strict points are

    M_E=(.35,-.35), I=(0,-.26), D=(.26,0).

The missing actual W center forces H_E<=0. The absent G8 and (9) force A_E<=c-.4s. Lemma1 of `C1092-MMMP-SOUTHEAST-FLOOR-RIGHT-SIGN.md` uses exactly these same faces, the strict points just listed and the entire actual bar (10). Its closed-vertex argument, including possible contact with the interior of B, proves

    sA_E+cH_E>a(c+s)-1,
    A_E>a-z,
    H_E>-.26s,
    0<z<21/197<.11.                                 (11)

Only the valid floor lemma and, for a nonnegative R, that chapter's Lemma2 excluding the two downward E--R sources will be used.

### 5.1. The actual upper pair has northeast half-angle below one third

Sections2--5 of `C1092-MMMP-NORTHEAST-UPPER-THIRD.md` are a local proof on actual W,N,E. Their complete independent inputs here are W's positive frame and bound (1), its strict rectangle and marker, strict G1 in actual L, the actual E inward pair and (9), and N's full face table (2). All are already established here. The first section's separate MMMP proof of the W sign is unnecessary: the one-omission northwest-sign theorem gives that sign independently.

The cited Sections2--3 cover both actual E--W normal sources and both relative angle orders, giving the simultaneous faces

    H_W>.92, A_W>=a-d+.4r.

Their Section4 covers both W--N sources, both relative orders, and equality at the threshold. It gives

    1/4<tan(theta_N/2)<1/3.                         (12)

The strict lower bound is (3). Every exterior point in this local proof has its actual owner in Section1; no boundary center is used in its support or polynomial argument.

### 5.2. Every right angle contradicts those same actual owners

The actual R bar and its independent genuine conditions are

    {1}x[-.26,.4] strictly in R,
    closure(R) subset {x<=2}, center_y(R)>=0.          (13)

Its entire strict bar comes from its present F8, its universal G9, and convexity. It is the same actual R in every pair comparison.

For a nonpositive canonical R, the full proof in Sections2--5 of `C1092-MMMP-NEGATIVE-RIGHT-ENDING.md` applies to (9),(11)--(13), N's table (2), its strict marker and F7, and E's strict I,D. Its actual southeast supports first force the right slope magnitude below1/2. The actual northeast/right normal cone then leaves only the two downward sources, and the full face table, real right wall and correctly signed center inequality exclude both whenever tan(theta_N/2)<=1/3. It therefore gives tan(theta_N/2)>1/3, contrary to (12).

For a nonnegative canonical R, Lemma2 of the floor chapter and Sections2--3 of `C1092-MMMP-POSITIVE-RIGHT-ANGLE-REDUCTION.md` apply to precisely the same actual entrance, also using the genuine N point P_N proved in (4). They leave only u_E or u_R for E--R, force the right slope r_R/d_R<1/2, and leave only -v_N for N--R. Sections2--4 of `C1092-MMMP-POSITIVE-RIGHT-ENDING.md` then use the same actual R wall and center with their negative center-y coefficient. They force

    r_R/d_R>5/12.

The E--R source u_R would instead require r_R/d_R<1/3, by the exact numerator margin .1258 in that proof. The other source u_E would require a scalar loss below .11, whereas its actual strict-angle lower bound is

    3027/21125>.14>.11.

Thus both actual sources fail. These cited local support calculations impose no condition on L's center and do not assume G8 in R. Their complete input list is (2)--(4),(9),(11)--(13) and the named actual strict points. Hence they apply literally here to both closed canonical sign domains of R.

This excludes the whole alternative F8 in R with G8 absent from E.

## 6. The alternative with G8 strict in E is also impossible

Still suppose F8 is in R, but now G8 is strict in E. The sign and bottom origin (8) remain valid, while the quantitative bound (9) is not assumed.

The full local proof in Sections2--5 of `C1092-MMMP-PARTIAL-RIGHT-SOUTHEAST-FLOOR.md` has the following exact actual inputs:

| Point or bar in its centered chart | Actual owner or exclusion here |
|---|---|
| M_E=(.35,-.35), I=(0,-.26), D=(.26,0), G=(1,-.4) | Strict in E by (7) and the present G8 hypothesis |
| O=(0,0) | Strict in actual W |
| F=(1,-.26) | Strict F8 in actual R |
| P_N=(.47,.12) | Strict in actual N by (4) |
| The entire [0,.4]x{-1} | Strict in the same actual B by (10) |

The positive E frame is (8). Thus its full forced-face, whole-bar vertex and continuous scalar proofs apply without importing its introductory reference to the MMMP right-near theorem. They give the simultaneous new bounds

    s/c<1/3, s<1/sqrt(10)<.32, c>3/sqrt(10)>.94,
    H_E<=0, H_E>-.26s, H_E>-1/100,
    A_E<=c-.26s,
    sA_E+cH_E>a(c+s)-1,
    A_E>a-z.                                         (14)

These bounds are derived under actual G8 ownership in E, independently of (9).

Sections3--5 of `C1092-MMMP-PARTIAL-RIGHT-NORTHEAST-BOUND.md` now apply to the same W,N,E. Their independent inputs are (14), W's already positive frame and bound (1), its actual rectangle and marker, actual G1 in L, and N's full table (2). The additional strict facts U_E<-.26s and A_E>0 follow from its strict I and (14), respectively. That proof gives H_W>74/75 and the actual G1 lower-u face, then applies the complete local northeast upper-angle proof. Therefore (12) holds in this branch as well.

Finally use Sections2--5 of `C1092-MMMP-PARTIAL-RIGHT-ENDING.md`, not its global MMMP joining statement. Its entire actual entrance is now available:

* E's strict D,G, positive bounds and coupled floor in (14);
* R's whole strict bar, real wall and correct center sign (13);
* N's strict marker,F7,P_N, the four faces (2), and the interval (12).

The strict pairs D_E to (1,0)_R and G_E to F8_R put every E--R separating normal in the open upper-right quadrant. In the nonpositive R sign the complete local proof eliminates its own upward source, forces its slope magnitude below1/2, and then excludes both remaining N--R sources by the actual face table and real wall. In the nonnegative R sign it again forces slope below1/2 and reduces N--R to -v_N. That source forces r_R/d_R>5/12. The right-supplied E--R source instead forces r_R/d_R<5/12 by its exact .1412 margin. For the last E-supplied source, the full-interval scalar loss increases with the right angle and is strictly greater than

    2609/21125>.12,

whereas separation requires a loss below

    z(1-s)<272/2425<.113.

Both closed signs, every source, and all joining-angle equalities are therefore excluded by that local proof. It uses exactly the three actual owners in the displayed input list, so no fourth owner, incorrect left-center inequality, or independently placed copy is introduced.

This excludes the remaining F8-in-R alternative. With Section5,

    F8 is excluded from R.                            (15)

The three exact component alternatives in Section3 consequently leave only

    R=524800={F9,G9}

in transposed notation, or original Q11=131200={F7,G7}.

## 7. The sole actual right component forces a large northeast angle

The local wall-advance theorem, Theorem1 of `C974-C976-CONTINUOUS-REDUCTIONS.md`, reflected through x=2, applies to this same R. Its strict marker and G9 are original actual data, its excluded F8 is (15), its other excluded point is N's original northeast marker, and its wall is the genuine right wall. It gives

    (3,2.56) strictly in R.

With R's already proved origin, this yields the entire actual strict bar

    {3}x[2,2.56] in R.                               (16)

No southeast sign or bottom origin has been retained from the excluded F8 branches.

In centered transposed coordinates apply local Theorem3 of `OUTWARD-BAR-AND-UPPER-SPAN.md` to N. Its strict marker and A=(.4,1) are N's original marker and F7. Its excluded L=(0,.26),P0=(0,1),P1=(1,1) have actual owners W,T,K_NE, respectively. Its entire excluded bar {1}x[.26,.56] is the one actual R bar (16). It therefore gives

    (.525,.125) strictly in N.                       (17)

Local Theorem1 of `TOP-ONLY-LEFT-POINT.md` now applies to that same N. Its strict marker,G=(.26,1) and Y=(.525,.125) are the actual N marker,G7 and (17); its three excluded points are the same W point, T origin and K_NE paired point, and its full foreign bar is again (16). Section2 of that local proof yields

    U_N>=.26t, V_N>=.56b-t,
    A_N<=b+t, H_N<=b.

The valid earlier U_N>=.4t from (2) remains available. Thus the full actual table is

    U_N>=.4t, V_N>=.56b-t,
    A_N<=b+t, H_N<=b.                               (18)

The two v faces imply 1<a<=t+.44b. The exact half-angle identity is

    (1+z_N^2)(t+.44b-1)=2(18z_N-7)(1-z_N)/25.

It follows over the entire canonical interval that

    z_N>7/18,
    t>252/373, b<275/373, t/b>252/275.                (19)

This is precisely the local point/bar proof in Sections1--3 of `C1092-MMMP-SOLE-RIGHT-NORTHEAST-REACH.md`, with its top-origin input supplied by the new one-omission theorem. Its proof contains no left-center or southeast premise.

## 8. The final two actual upper squares cannot separate

We reproduce the positive-sign part of the local continuous ending so the final dependence is explicit. W's positive frame is

    u_W=(d,r), v_W=(-r,d), d>=r>0, d^2+r^2=1,

and write A,H for its upper faces. Its strict rectangle gives

    A>.5r>0, H>.5(d+r)>=.5,
    A-a<0, H-a<0.                                   (20)

By (1),(19), its angle p is below N's angle theta. Put

    alpha=bd+tr>0, beta=td-br>0,
    alpha+beta>=1.                                   (21)

The strict markers (-.35,.35) in W and (.35,.35) in N force the x component of a W-to-N separating normal to be positive. The other right-pointing normals -v_W,-v_N have nonpositive products with the strict displacement from O in W to the N marker. The complete remaining sources are u_W and u_N.

Their full lower N supports satisfy

    lower_N(u_N)=U_N<=b+t-a<sqrt(2)-1<.5,
    lower_N(u_W)=alpha U_N-beta H_N<.5,               (22)

because H_N>=a+.56b-t>0 by (18).

### 8.1. Two actual foreign points fix W's two upper-face lower bounds

The southwest marker S_0=(-.35,-.35), strictly in actual S, has both upper W bands by strict O. If it were lower u, then A>=a-.35(d+r)>.5. With H>.5 from (20), this would defeat both sources in (22), including the factor alpha+beta>=1 for the N-supplied source. Therefore it must be lower v:

    H>=a-.35d+.35r.                                  (23)

The point B_0=(-1,.4), strictly in the actual L, has its upper u and lower v bands from strict O. If it were upper v, then H<=r+.4d; together with (23), this would give

    a<=.75d+.65r<=sqrt(197/200)<1.

Hence B_0 is lower u and

    A>=a-d+.4r.                                      (24)

Both bounds apply to this one actual W.

### 8.2. W's own normal is impossible

If u_W separated, (18),(21) would imply

    A<=alpha(b+t-a)-beta(a+.4b-t).

Together with (24) and the positive coefficient of a>1, this would require

    F_2=1-K_2d-L_2r<0,
    K_2=2-b-t+.6bt, L_2=b-t+.6t^2.                  (25)

For theta>=theta0=2 arctan(1/3), both coefficients are positive and decreasing. Their derivatives are (b-t)[-1+.6(b+t)] and -t-b+1.2bt, respectively. Their values at theta0 are111/125 and52/125. Hence

    K_2d+L_2r<=sqrt(K_2^2+L_2^2)
               <=sqrt(601)/25<1,

contrary to (25). The whole needed interval is included because (19) is stronger than theta>theta0.

### 8.3. N's own normal is impossible

For u_N, the full support inequality and (23)--(24) would instead require

    F=1-b-t+alpha(1-d+.4r)
             +beta(1-.35d+.35r)<0.                  (26)

Direct expansion gives

    F=1-bK-tL,
    K=2-d+r-.65r^2-.75dr>=1,
    L=1.35-d-r-.75r^2+.65dr<=.35.                    (27)

For the first inequality use

    K-1=(1-d)+r(1-.65r-.75d)>=0,
    .65r+.75d<=sqrt(197/200)<1.

For the second use d+r-1=2dr/(1+d+r), giving

    L-.35=dr[.65-2/(1+d+r)]-.75r^2<=0.

Thus, holding p fixed, partial_theta F=tK-bL>=t-.35b>0 on the entire required interval. It suffices to evaluate F at theta_*=2 arctan(7/18), where b=275/373,t=252/373. Put w=tan(p/2), so d=(1-w^2)/(1+w^2), r=2w/(1+w^2). The exact identity is

    20*373*(1+w^2)^2 F(theta_*,p)
       =196+778w+w^2(8732-2618w-20884w^2).            (28)

The actual canonical interval is contained in 0<=w<=1/2. On that entire enlarged interval the bracket is at least

    8732-2618/2-20884/4=2202>0.

Every denominator is positive. Consequently F(theta,p)>=F(theta_*,p)>0, contradicting (26). No separating normal remains for these two actual squares.

## 9. Completion

The original one-omission entrance supplied the actual full upper core. The new mixed-wall/corner theorem supplied its previously missing top origin with the correct left-center sign. Both F8-in-R alternatives were then excluded by local continuous proofs whose entire point, bar, face and genuine right/bottom center premises were supplied here. The sole remaining actual R extended its bar, forcing (18)--(19), and the two actual upper squares now give the final contradiction.

Thus the normalized single omission is impossible. The same simultaneous quarter-turns used in the mixed-wall theorem carry it to each of the other three possible single omissions. Two or more omissions were already impossible because they put (2,2) strictly in two distinct actual central owners. Every original MPPM configuration with an indicated omission is therefore excluded. The argument has retained actual owners, whole strict bars, both closed canonical signs, and all weak contacts throughout.
