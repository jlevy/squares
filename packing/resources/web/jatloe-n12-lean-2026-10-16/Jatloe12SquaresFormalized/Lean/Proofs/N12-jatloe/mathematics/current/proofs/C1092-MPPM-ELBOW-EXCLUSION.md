# C1092 MPPM: complete exclusion of every residual elbow

All terminating decimals are exact rational numbers. Every named owner is an actual open square of the common side a>1. Owned points are strict, and excluded points and separating supports allow equality. The local lemmas below use no upper side bound. Their application retains the entire original no-omission MPPM entrance, not a reduced vector catalogue.

We use the already proved two-square entrance in C1092-MPPM-ELBOW-SUCCESSOR.md. Its square C is the southwest residual elbow, in coordinates translated by (−2,−2); its ordinary successor E is the actual southeast central square. That theorem proves E's negative sign and its omission of the forward inner point before any new inference here.

## 1. The complete local entrance and negative successor faces

C has the positive canonical frame u=(c,s), v=(−s,c), with lower faces U,V and upper faces J=U+a,K=V+a. Its strict original marker and elbow anchors are

    M_C=(−.35,−.35), P=(−1,−.26), Q=(−.26,0).

Its exact profile is

    U≥−c−.4s, J≤−.26s,
    V≥.4s−c, K≤.35(c+s), X=(0,−.5) strict in C,      (1)
    c²+s²=1, 0<z:=s/(1+c)<7/50,
    c>24/25, 0<s<7/25, c+s<31/25.

The negative successor has frame u_E=(d,−t), v_E=(t,d), where d≥t>0 and d²+t²=1. Denote its lower faces by L,W and its upper faces by J_E=L+a,K_E=W+a. Its strict points and exclusions from the preceding theorem are

    M=(.35,−.35), A=(.26,−1), B=(.4,−1) strict in E;
    G=(1,−.4), K0=(1,−1), R0=(0,−1.086),
    T=(0,−.26), X=(0,−.5) excluded from E.            (2)

Here X is excluded because it is strict in C. The zero and diagonal representatives were treated in the all-angle successor theorem; keeping the closed canonical bounds d≥t≥0 in the scalar estimates below causes no omission.

**Lemma 1.** The data (1)–(2) force

    L≥.5t, J_E≤d+t,
    W≥−1.086d, K_E≤t−.4d,                           (3)
    1<a≤t+.686d.

**Proof.** At X its upper u-band follows from B, its upper v-band from M, and its lower v-band from A, with positive projection increments

    .4d+.5t, .35t+.15d, .5d−.26t≥.24d.

Thus X is lower u, giving L≥.5t. At G both lower bands are strict by M,A. Its upper u-band follows from

    u_E(G)=d+.4t≤1+.5t<a+L.

Hence G is upper v, K_E≤t−.4d.

At K0 the lower u-band is strict by B and the upper v-band by M; the increments are .6d>0 and .65(d−t)≥0. A lower-v exit would give a≤.6d<1. Therefore K0 is upper u, J_E≤d+t.

At R0 both upper bands are strict by B,A, with increments .4d−.086t≥.314d>0 and .26t+.086d>0. A lower-u exit would oppose K0 and give a≤d−.086t≤1. Thus R0 is lower v, W≥−1.086d. The v-width is now at most t+.686d, proving the last line. It also independently excludes t=0. All exits were weak. ∎

In both local lemmas below we put

    p=arctan(s/c), q=arctan(t/d),
    kappa=cos(p+q)=cd−st>0,
    lambda=sin(p+q)=ct+sd>0.

The marker difference (.7,0) forces every separating normal from C toward E to have positive horizontal component. Consequently the complete actual-normal list is

    u, −v, u_E, v_E.                               (4)

Some entries cease to be eligible at canonical endpoints. Keeping them in the subsequent support calculations is harmless. In particular no vertical sign of a separator is presumed.

## 2. A far right point and the actual left segment forbid the elbow

**Theorem 2.** In addition to (1)–(2), suppose C excludes the entire segment

    S=[R,H], R=(−1.086,0), H=(−1,.26),                (5)

and E excludes F=(1,−.56). Then C and E cannot have disjoint interiors.

The segment in (5) is genuinely one segment in the hypothesis. In the application it lies strictly in the actual left boundary square. No owner for the isolated point F is needed by this local statement.

### 2.1. The far point forces q>2 arctan(3/10)

At F both lower bands follow strictly from M,A; their increments are .65d+.21t>0 and .74t+.44d>0. Thus F is upper u or upper v. An upper-u exit, together with L≥.5t, would give

    1<a≤d+.06t.

The exact half-angle identity would then force 0<tan(q/2)<.06, and hence t<.12. But Lemma 1 gives a≤t+.686d<.806<1, a contradiction. Therefore F is upper v. We have sharpened (3) to

    K_E≤t−.56d, 1<a≤t+.526d.                         (6)

The function sin q+.526 cos q is strictly increasing on [0,pi/4], since its derivative is at least .474 cos q>0. At q0=2 arctan(3/10) it equals

    (60+.526·91)/109=53933/54500<1.

Thus q>q0, so

    d≤91/109, t≥60/109,
    kappa>12/25, lambda>11/20,
    d+t−1>19/50.                                    (7)

For kappa, use c>24/25,s<7/25,d≥t and d≥1/sqrt(2):

    kappa>(17/25)d≥17/(25sqrt(2))>12/25,

where 17²>2·12². Also p+q<pi/2, so lambda≥sin q=t≥60/109>11/20. The last bound follows from d+t increasing on the canonical interval and its value 151/109 at q0.

### 2.2. Three normals give direct positive margins

For the direction u, (3),(6) give

    lower_E(u)=kappa L+lambda W
       ≤kappa(d+t−a)+lambda(t−.56d−a).

Since upper_C(u)=J≥a−c−.4s, the support difference is strictly greater than

    F_u=1−c−.4s+kappa(1−d−t)
                                  +lambda(1−t+.56d). (8)

For fixed q its exact p derivative is

    dF_u/dp=s−.4c+lambda(d+t−1)
                                  +kappa(1−t+.56d).

Here 1−t+.56d≥1−.44/sqrt(2)>17/25. By (7),

    dF_u/dp>−2/5+(11/20)(19/50)+(12/25)(17/25)
             =677/5000>0.

At p=0,

    F_u=d+t−1−.44dt≥.36dt>0,

using d+t−1=2dt/(1+d+t)≥.8dt. Thus u cannot separate.

For −v, use K≤.35(c+s) and the bounds L≤d+t−a, W≥−1.086d. The support difference is strictly greater than

    F_{−v}=1−.35(c+s)+kappa(1−1.086d)
                                      +lambda(1−d−t).

Since d≤91/109, the kappa term is nonnegative. Therefore

    F_{−v}≥1−.35(31/25)−(sqrt(2)−1)
             >481/3500>0,

where sqrt(2)<10/7 was used in the final rational bound. This excludes −v.

For v_E, the upper support of C is lambda J+kappa K. Use J≥a−c−.4s and K≥a+.4s−c, and subtract W≤t−.56d−a. The resulting margin is strictly greater than

    F_{v_E}=1+(kappa+lambda)(1−c)
                          +.4(kappa−lambda)s−t+.56d.

Because |kappa−lambda|≤1, t≤d≤1 and s<7/25,

    F_{v_E}≥1−.4s−.44>56/125>0.

All coefficients of a replaced by 1 are positive. The three strict support contradictions include every touching-support equality.

### 2.3. The actual segment supplies the last support bound

Orient a separator from S toward C. The strict point Q=(−.26,0) of C compared with R forces n_x>0, and its strict point P=(−1,−.26) compared with H forces n_y<0. The separating-axis theorem for a square and a segment therefore leaves just the following two possibilities:

    the C normal −v=(s,−c);
    the segment normal n=(.26,−.086).                 (9)

These are actual square or segment normals, not normals to an artificially enlarged region. Each is retained with weak support separation. For the first source, the maximum of −v on S is −1.086s, since .26c−.086s>0. Thus it gives

    K≤1.086s.                                       (10)

For the second source put

    alpha=.26c−.086s>0, gamma=.26s+.086c>0.

The constant value of n·X on S is −.28236. The minimum n-projection of C is alpha U−gamma K. Hence this source gives

    alpha U−gamma K≥−.28236.                         (11)

We show that either (10) or (11) rules out the remaining separator u_E between C and E.

### 2.4. The transverse C source in (9)

Under (10), upper_C(u_E)=kappa J−lambda V and L≤d+t−a show that the support difference is strictly greater than

    F=1−d−t+kappa(1−c−.4s)+lambda(1−1.086s)
      =1−A0 d−B0 t,                                 (12)

where

    A0=2−c−s+.086s²+.4cs,
    B0=1−c+s+.086cs−.4s².

On the full range (1), A0≥19/25 and B0<7/20. The latter follows from

    B0≤1−24/25+7/25+.086(7/25)=.34408<.35.

Consequently, for q≥q0,

    dF/dq=A0 t−B0 d
       >d[(19/25)(60/91)−7/20]=(55/364)d>0.

At q=q0 the exact half-angle expression is

    F=(10z+3)(750−3380z+2879z²−3550z³)
                         /[13625(1+z²)²].            (13)

Its numerator is positive on 0≤z≤7/50: indeed 750−3380z≥1384/5>0 and 2879−3550z≥2382>0. Thus (12) is positive and u_E cannot separate in this segment-normal alternative.

### 2.5. The oblique segment source in (9)

Now use (11). From K≤(alpha U+.28236)/gamma,

    upper_C(u_E)=a(kappa+lambda)+kappa U−lambda K
       ≥a(kappa+lambda)+(kappa−lambda alpha/gamma)U
                                      −.28236lambda/gamma.

The exact coefficient identity is

    kappa gamma−lambda alpha=.086d−.26t<0,           (14)

using t/d≥60/91. Also J≤−.26s in (1) gives U≤−a−.26s. Substitute this upper bound in the negative-coefficient term. After subtracting L≤d+t−a, replacing a by 1 makes the support difference strictly smaller. Multiplying by gamma>0 gives the exact lower margin

    G=gamma(1−d−t−.26s kappa)
              +lambda(gamma+alpha+.26s alpha−.28236)
      =gamma−A1 d−B1 t,                             (15)

where

    A1=.086c+.56472s−.346cs−.174s²,
    B1=.36836c−.346+.1924s−.174cs+.346s².

The coefficient of a before its replacement is lambda(1+alpha/gamma)+1>0, so the strict inequality just used is valid throughout the domain.

We have A1>2/25. Indeed

    A1≥.086c+s(.56472−.346−.174·.28)
       =.086c+.17s>.086(24/25)>.08.

For B1 use c≤1−s²/2 in its positive .36836c term and c≥24/25 in −.174cs. This gives

    B1≤.02236+.02536s+.16182s²
       ≤1317109/31250000<43/1000.

Hence on q≥q0,

    dG/dq=A1 t−B1 d
       >d[(2/25)(60/91)−43/1000]
       =(887/91000)d>0.

At q=q0, direct rational substitution gives

    G=[129105z⁴−478247z³+68175z²+45828z+645]
                                      /[340625(1+z²)²]. (16)

The numerator is positive on 0≤z≤7/50 because

    68175−478247z≥61021/50>0.

Group its middle two terms as z²(68175−478247z); all remaining terms are nonnegative, and its constant is 645. Thus (15) is positive. The remaining u_E source is impossible in this alternative too.

We have exhausted every square normal in (4) and every actual segment source in (9). This proves Theorem 2. No isolated endpoint was used in place of the whole segment in (5). ∎

## 3. A previous wall origin also forbids the elbow

**Theorem 3.** Under (1)–(2), suppose C additionally excludes D=(−1,0). Then C and E cannot have disjoint interiors. No far point F and no foreign segment are needed in this theorem.

**Proof.** At D the lower u, upper u and lower v bands are strict by P=(−1,−.26) and Q=(−.26,0). Their increments are .26s>0,.74c>0,.26c>0. Thus D is upper v, so

    K≤s.                                            (17)

Retain all four faces (3) and the complete separator list (4). We exclude them directly for every canonical negative q, without imposing the lower bound q>q0 from Theorem 2.

### 3.1. The successor normal u_E

By (17), J≥a−c−.4s and L≤d+t−a, the support difference is strictly greater than

    F=1−d−t+kappa(1−c−.4s)+lambda(1−s)
      =1−A d−B t,

where

    A=2−c−s+.4cs, B=1−c+s−.4s².

The exact half-angle identity is

    1−A²−B²
      =4z(15−59z+55z²−75z³)/[25(1+z²)²]>0.         (18)

Indeed z>0, 15−59z≥337/50>0, and 55−75z≥89/2>0 on z≤7/50. Cauchy–Schwarz therefore gives A d+B t≤sqrt(A²+B²)<1. Hence F>0 and u_E cannot separate.

### 3.2. The C normal u

Using the original cap K_E≤t−.4d from Lemma 1 yields the margin

    F_u=1−c−.4s+kappa(1−d−t)
                                   +lambda(1−t+.4d). (19)

Its exact p derivative is

    dF_u/dp=s−.4c+lambda(d+t−1)
                                   +kappa(1−t+.4d).

This derivative is positive on the whole q range. To verify it continuously, split at q0=2 arctan(3/10).

If q≤q0, then d≥91/109 and t≤60/109, so

    kappa>(24/25)(91/109)−(7/25)(60/109)
             =1764/2725>16/25,
    1−t+.4d≥427/545>39/50.

Dropping the nonnegative s and lambda(d+t−1) terms gives

    dF_u/dp>−2/5+(16/25)(39/50)=62/625>0.

If q≥q0, use kappa>12/25, lambda>11/20 and d+t−1>19/50 as in (7). Also 1−t+.4d≥1−.6/sqrt(2)>57/100. Thus

    dF_u/dp>−2/5+(11/20)(19/50)+(12/25)(57/100)
             =413/5000>0.

At p=0 the value in (19) is d+t−1−.6dt≥.2dt≥0. Since the actual p is strictly positive, (19) is strictly positive for all q, including a zero limiting endpoint. This excludes u.

### 3.3. The two remaining transverse normals

For −v, replace the earlier upper-v cap .35(c+s) by the stronger s in (17). The resulting margin is

    F_{−v}=1−s+kappa(1−1.086d)+lambda(1−d−t).

Using kappa≤1,d≤1,lambda≤1 and sqrt(2)<10/7 gives

    F_{−v}≥1−7/25−.086−(sqrt(2)−1)
             >719/3500>0.

For v_E, the lower faces of C and the cap K_E≤t−.4d give

    F_{v_E}=1+(kappa+lambda)(1−c)
                            +.4(kappa−lambda)s−t+.4d
             ≥1−.4s−.6>36/125>0.

This excludes both remaining normals. Every support difference was made strictly smaller by replacing a>1 by 1 with a positive coefficient. All four actual source directions therefore fail, proving Theorem 3. ∎

## 4. Literal application: an elbow would force an opposite inward owner

Assume Q4 is a residual elbow in the complete original no-omission MPPM entrance. The earlier isolation and successor theorems give

    Q5 ordinary F6,G5, strictly negative and omitting F4;
    Q7 ordinary F3,G4.

With C=Q4,E=Q5 and translation by (−2,−2), the left segment S in Theorem 2 is precisely the segment joining the original left marker (.914,2) to F1=(1,2.26). Both endpoints lie strictly in the same actual Q8, so its entire segment is strict in Q8 and excluded from the closure of Q4. The complete point table (2) is the one already checked in C1092-MPPM-ELBOW-SUCCESSOR.md.

Suppose opposite Q6 owned F9=(3,2.26). Theorem 1 of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md then excludes G6 from actual Q10. Its original right marker and G8=(3,1.6) are already strict by the no-omission entrance, and F9 is strict in Q6. The exact ordinary-wall advance in Section 5 of C1092-MPPM-NONORDINARY-ISOLATION.md therefore applies to this actual Q10 and gives

    (3,1.44) strictly in Q10.

This point becomes F=(1,−.56) in Theorem 2, a genuine exclusion from Q5. Theorem 2 now contradicts the actual Q4–Q5 disjointness. We have proved

    F9 is excluded from Q6.                          (20)

The complete three-alternative central cover leaves only the inward pair in Q6: both its ordinary and residual-elbow alternatives require F9. Consequently

    F5,G6 are strict in actual Q6.                    (21)

This step uses the original cover only; it does not infer that every auxiliary has an owner.

## 5. The inward owner supplies the origin that completes the contradiction

By isolation Q7 already owns its ordinary pair F3,G4. Equation (21) puts F5 in the distinct actual Q6, so Q7 omits its forward inner point F5.

Apply ORDINARY-MARKER-HALFPOINT.md to the actual Q7 under the explicit map from its local coordinates

    (xi,eta) -> (2+eta,2+xi), d=.086.

Its strict marker and ordinary anchors become the NW marker,G4,F3. Its excluded D,R,K,F become, respectively,

    F5 in Q6;
    the original top marker (2,3.086) in Q11;
    the strict paired NW corner (1,3) in Q3;
    F1=(1,2.26) in Q8.

Thus (1.5,3) is strict in actual Q7. It is consequently excluded from the actual paired corner Q3. Apply Theorem 7 of C1092-DIRECT-WALL-POINT.md to the actual Q3,Q8 under the simultaneous rotation (x,y) -> (y,4−x) of its southwest-corner/bottom-wall chart. The marker parameter is b=.914 and the ordinary boundary anchor parameter is ell=1.6. Its required corner exclusion is exactly (1.5,3); its corner strict anchors, left-wall marker, G1=(1,2.4) and real left wall all belong to the stated actual owners. This yields

    (1,2) strictly in Q8.                            (22)

No source from an independently rotated configuration has been adjoined. The entire transfer is to the one physical Q3 and Q8.

The point (22) becomes D=(−1,0) in the original translated Q4 chart. Theorem 3 therefore excludes the actual Q4–Q5 pair. This is the required contradiction.

The physical quarter-turn R(x,y)=(4−y,x) preserves the complete original no-omission entrance and MPPM signs. Rotating the whole proof excludes each of the other three residual-elbow positions, with the corresponding actual segment, far wall and paired-corner sources. Therefore:

**Theorem 4.** No central owner in the complete original no-omission MPPM family has its residual elbow alternative. Every actual central owner has either its ordinary pair or its inward pair. Every genuinely nonordinary owner is inward and has both cyclic neighbors ordinary.

Up to simultaneous quarter-turn, the remaining cyclic type arrangements are consequently

    OOOO, OOOI, OIOI,

where an owner with both pairs is counted as O and I here means genuinely nonordinary. The present theorem completely removes all elbow arrangements, including the previously possible E O I O pattern. A separate continuous ending remains necessary for these ordinary/inward cyclic types; the all-four-forward-point exact last assignment is already excluded by its completed direct theorem.
