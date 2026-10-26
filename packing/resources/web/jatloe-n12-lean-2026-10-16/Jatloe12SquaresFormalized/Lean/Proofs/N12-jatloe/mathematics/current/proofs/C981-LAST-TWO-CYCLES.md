# C981: the last two cycles and their actual right-wall exclusion

Every terminating decimal is an exact rational. All owned points are strict, while exclusions and support separations allow equality. All squares below have the same side a>1. The positive-central branch later uses the original permitted cap a≤1001/1000, through `C981-OPPOSITE-CENTRAL-ANGLE.md`.

## 1. The actual right-wall square forces the upper square past thirty degrees

**Theorem 1.** Let B be a square with positive canonical frame

    u_B=bx+ty, v_B=−tx+by, 0≤t≤b, b²+t²=1,

strictly owning

    H1=(−1,.26), H2=(−1,.4), M=(−.35,.35),

and excluding the four points

    (−1,0), (−.4,0), (−1,1), (−.4,1).

Let R be a square of the same side, contained in y≤2, strictly owning

    A=(−.4,1), D=(.26,1),

and excluding T=(.4,1). If the interiors of B and R are disjoint, then

    t>1/2.                                               (1)

R has no angle restriction. Its named wall is its genuine outer wall.

**Proof.** The two short vertical chords at x=−1 and x=−.4 give the rotated positive-frame table in the first part of Theorem 1 of `C981-COMMON-CYCLE.md`. If p,q are B's lower faces and H=b+t, it is

    p≥−b, q≥.4t, p+a≤t−.4b, q+a≤H.                    (2)

For completeness, the chord lengths are at most one because their endpoints lie between the excluded heights 0 and 1. The plateau length a/b exceeds one. The center abscissa must lie strictly between the chord lines: either alternative would put the opposite support at distance at most bt≤1/2 from that chord, contrary to the strict points at x=−1 and x=−.35. Both chords are therefore in their respective vertex regions. Their four endpoints give (2), exactly as in the rotated table of the cited proof.

In particular a≤t+.6b. The half-angle factorization from that proof gives

    h=t/(1+b)>1/4, t>8/17, b<15/17.                    (3)

Suppose t≤1/2. We will use the rational bounds

    .47<t≤.5, .86<b<.883,
    23/17<H≤(1+sqrt(3))/2<1.37.                        (4)

Choose R's positive-quadrant frame (c,s), c,s≥0, c²+s²=1, with lower faces U,V. Define

    α=bc+ts>0, β=bs−tc,
    K=H−1−.6bt=(H−1)(.7−.3H)>0.

R's strict anchors give

    U<−.4c+s, U+a>.26c+s,
    V<c−.26s, V+a>c+.4s.                               (5)

At T its lower u-band and upper v-band follow from D. Thus its exclusion has precisely the two possible forms

    U+a≤.4c+s,  or  V≥c−.4s.                           (6)

The real top wall gives

    s(U+a)+c(V+a)≤2.                                   (7)

### 1.1. Only the two positive face normals can separate B from R

On either positive normal (b,t) or (c,s), R-before-B is impossible by comparing R's D with B's H2. On B's transverse normal (−t,b), B-before-R is impossible because

    v_B(H2)−v_B(D)=1.26t−.6b>0

by (3); the reverse is impossible because v_B(A)−v_B(H2)=.6(b−t)>0.

Consider R's transverse normal (−s,c). If β≤0, R's angle is at most B's and c>s. The reverse order is excluded by v_R(A)−v_R(H2)=.6(c−s)>0. For B-before-R, (2) bounds B's maximum support below by

    −β(a−b)+α(a+.4t).

After replacing a>1, subtracting v_R(D)=c−.26s gives a quantity strictly greater than

    cK+s(1.26+t−b−.6t²)>0.

This excludes that order as well. If β≥0, B-before-R is excluded by .6c−1.26s<0, using s/c≥t/b>8/15. For the reverse order, (2) bounds B's minimum support above by

    −β(a−b)+α(H−a)
      <α(H−1)+β(b−1).

After subtracting v_R(A)=c+.4s, the latter expression becomes

    c(t−b−t²)+s(.6+bt−H)<0.

Thus this order also fails. These arguments include β=0. The exhaustive remaining choices are

    p+a≤L_R(b,t),                                      (BU)
    U_B(c,s)≤U.                                        (RU)

### 1.2. The upper-u alternative at T is impossible

Suppose U+a≤.4c+s. The displacement T−M=(.75,.65) has squared length .985<1, so

    U≤u_R(T)−a<u_R(M).

This rules out (RU).

For (BU), first suppose β≤0 and put δ=−β≥0. From (5),

    L_R(b,t)<.4b+t−α+.14δs.

Since p+a≥a−b>1−b, (BU) would require

    1<1.4b+t−α+.14δs
      <1.4(.883)+.5−.86+.14/4=.9112.

Here α≥b>.86 and 0≤δ,s≤t≤.5. This is impossible.

If β≥0, the strict lower bound on V+a in (5) gives

    L_R(b,t)<.4b+t−α−.8βs.

The corresponding necessary upper bound is

    1<1.4b+t−α−.8βs
      =b(1.4−c−.8s²)+t(1−s+.8cs).

The first coefficient is .6−c+.8c²≤.6; the second is at most 1−.2s≤1−.2t<.906. Therefore the right side is less than .6(.883)+.5(.906)=.9828, again impossible.

### 1.3. The lower-v alternative at T excludes (BU)

It remains that V≥c−.4s. If s=0, (7) gives 2≥V+a≥1+a>2. Hence s>0. Write H_R=c+s and z=s/(1+c), so 0<z≤1.

Combining (BU), (7), and V≥c−.4s gives the necessary strict inequality F>0, where

    F=2α−bc+1.4bs−s−s max(β,0)−αH_R.                 (8)

Indeed multiply the lower bound on U from (BU) by s and combine it with (7); the coefficient of V after this substitution is b>0. Replacing a>1 yields exactly (8).

If β≤0, R's angle is at most B's, so 0≤z≤2−sqrt(3)<.27. Using H_R−1=2cs/(H_R+1), one obtains

    F/s=b[1.4−2c²/(H_R+1)]+t(2−H_R)−1.

Both bracketed coefficients are positive. Bounds (4) therefore give

    (1+z²)F/s
      <N1(z):=−.1468−.117z+2.6192z²−.883z³.

N1 is convex on [0,.27], since N1''=5.2384−5.298z>0. Its endpoint values are

    N1(0)=−.1468,
    N1(.27)=−4830409/1000000000.

Hence N1<0 on this entire interval, contradicting F>0.

If β≥0, z≥h>1/4, and (8) becomes

    F/s=bA2+t(2−s)−1,
    A2=1.4−s−2c²/(H_R+1).

One has .15≤A2≤.4. The lower bound uses 2c²/(H_R+1)≤c² and s+c²≤5/4. For the upper bound, multiplying s+2c²/(H_R+1)≥1 by H_R+1 reduces it to c(H_R−1)≥0.

For fixed c,s, the expression bA2+t(2−s) increases with B's angle up to thirty degrees: its derivative is −tA2+b(2−s)≥−.2+.86>0. At thirty degrees use sqrt(3)/2<.87. Thus

    (1+z²)F/s
      <N2(z):=.348−1.87z+2.088z²−.87z³.

The exact derivative identity

    N2'(z)=−2.61(z−.8)²−.1996<0

and N2(1/4)=−83/32000 imply N2(z)<0 for z≥1/4. This excludes (BU) in the second order too.

### 1.4. The lower-v alternative at T excludes (RU)

Assume (RU) instead. If β≤0, (2) gives

    U_B(c,s)≥α(a−b)+β(H−a).

If β≥0, it gives

    U_B(c,s)≥α(a−b)+β(a+.4t).

Combine the appropriate bound with (7) and V≥c−.4s. After replacing a>1, the top support is strictly greater than 2+g. We prove g>0.

For β≤0, direct expansion gives

    g/s=1−z+cA+sB0,
    A=H−1.4−bt<0, B0=t−b−t²<0.

As a function of R's angle φ≤B's angle, its derivative is

    −(1+z²)/2−sA+cB0<−.5+.9(.5)<0,

where A≥−.9. Its minimum is consequently attained when the two angles agree. There g/s=−f(t)/t, with

    f(t)=1+t²+1.4bt−b−2t.

On 8/17≤t≤1/2,

    f'(t)=2t+1.4b+(t−1.4t²)/b−2
           >.94+1.4(.86)−2>0.

But f(1/2)=1/4−3sqrt(3)/20<0. Therefore g>0.

For β≥0, the expansion is

    g/s=1−z−cC+sK,
    C=1.4−b+t−.6t².

C increases with t, so C<.884 at t≤1/2; also K≥30/289>.1 by (3). It follows that

    (1+z²)g/s
      >N3(z):=.116−.8z+1.884z²−z³.

For 0≤z≤1/2, this is at least .116−.8z+1.384z², a strictly positive quadratic whose discriminant is −34/15625. For 1/2≤z≤1, put w=z−1/2∈[0,1/2]. Then

    N3(z)=.062+.334w+.384w²−w³
          ≥.062+.276w>0.

Thus g>0 in this order as well. Equation (7) is contradicted in every possible separator and every forced-face alternative. The supposition t≤1/2 is impossible, proving (1). All comparisons with actual square supports were weak until the explicit use of a>1 or a strict anchor. ∎

## 2. The central square with negative angle forces the opposite inequality

**Theorem 2.** Let C have nonpositive canonical frame

    u_C=dx−ry, v_C=rx+dy, 0≤r≤d, d²+r²=1.

Suppose C strictly owns

    O=(0,0), E=(−.5,0), D_C=(0,−.5), M_C=(−.35,−.35),

and excludes

    G=(.35,−.35), D=(.26,0), J=(.26,−1).

Let B have a positive canonical frame (b,t), strictly own M=(−.35,.35), H1=(−1,.26), H2=(−1,.4), and exclude P=(−.4,1), K0=(−1,1). If the two squares have disjoint interiors, then

    t<1/2.                                               (9)

This theorem needs no wall and no upper bound on a.

**Proof.** The conclusion is immediate if t<1/2, so suppose t≥1/2. Write C's upper face values as u,v. Strict ownership of O gives u,v>0. At G the lower u-band and upper v-band follow from O, and the lower v-band follows from D_C. Therefore

    u≤.35(d+r).                                         (10)

Put α=bd−tr≥0 and k=br+td>0. The separating-axis reductions of Theorem 3 of `C981-COMMON-CYCLE.md` apply without its final steep-angle assumption. We give the needed details, including the present point P=(−.4,1), which is weaker than the point at x=−.5 used there.

On C's u-normal, C-before-B is impossible by comparing O and M. The reverse is impossible because (10) gives C's lower u-face less than M's projection: the possible gap is at most .7(d+r)<1<a. On B's u-normal, C-before-B is impossible by comparing O and H2. For the reverse, the lower C-support is α(u−a)+k(v−a). Use (10), a>1, and v−a<−.5d from D_C. After subtracting u_B(M), the resulting strict upper bound is bF0+tG0, where

    F0=.7−d−.35r²−.15dr<0,
    G0=−.85+r+.15r²−.35dr
        ≤−.85+r−.20r²<0.

Thus this axis also fails. On either upward transverse normal, B-before-C is ruled out by the two markers, whose y-coordinates differ by .7. The only possible separators are

    v≤L_B(r,d),                                        (CV)
    U_C(−t,b)≤V_B,                                     (BV)

where U_B,V_B denote B's lower faces when used without a support argument.

We first prove V_B+a>b+.4t. Under (BV), strict ownership of E gives V_B>.5t, and hence V_B+a>.5t+a>b+.4t. Under (CV), failure of the desired inequality would give

    L_B(r,d)<k(−b+.26t)+α(b+.4t−1).

Its expansion is df+rg, with

    f=1−b−.74t²−.6bt<0,
    g=−1+t+.6t²−.74bt≤−1+t−.14t²<0.

Here 1−b≤.6t² and b≥t. This would contradict v>0 and (CV). Thus the asserted strict upper v-band holds at P.

At P, its lower u-band follows from H1 and its lower v-band from M. Its exclusion therefore forces U_B+a≤t−.4b. At K0, its two lower bands follow from H2 and its upper u-band from M; consequently V_B+a≤b+t. These upper faces exclude (CV), since

    L_B(r,d)<−dK1+rG1<0,
    K1=b+t−1−.6bt=(b+t−1)(.7−.3(b+t))>0,
    G1=t−b−.4−.6t²<0.

Only (BV) remains. Its exact support inequality is

    a(1+k)≤b+t+ku−αv.                                  (11)

For later use, (10) and u,v>0 give the scalar reduction

    1<bF+tG2,
    H_C=d+r, q0=1−.35H_C,
    F=1−rq0, G2=1−dq0.                                 (12)

Both F,G2 are nonnegative. Cauchy–Schwarz and b²+t²=1 imply F²+G2²>1. The exact expansion is

    F²+G2²−1=2−2.7H_C+.8225H_C².

This polynomial decreases on [1,10/7], and its value at 1.13 is −2999/4000000. Hence H_C<1.13. Since sqrt(1−r²)+r increases on the canonical interval and sqrt(1−.14²)>.99,

    r<.14, d>.99.                                      (13)

We now use the two actual exclusions D,J. At D both lower bands follow from O, so D must fail an upper band. At J its lower u-band and upper v-band follow from O, so it must fail upper u or lower v. If neither point failed upper u, their two opposite v-faces would give a≤d≤1. Therefore

    u≤.26d+r.                                          (14)

Combining (11), (14), and v>0 gives

    1<bF1+tG3,
    F1=1−r+.26dr+r²,
    G3=1−d+.26d²+dr.

By (13),

    F1>.86, 0≤G3<.41,
    F1≤1−.74r+r²,
    G3≤.26+r+.34r².                                    (15)

The last estimate uses 1−d≤.6r². On the supposed range t≥1/2, the function sqrt(1−t²)F1+tG3 decreases with t, because its derivative is G3−tF1/sqrt(1−t²)<.41−.43<0. At t=1/2 use sqrt(3)/2<.867 in (15). It follows that

    bF1+tG3
      <.997−.14158r+1.037r².

The quadratic is convex on [0,.14]; its two endpoint values are .997 and

    .997504=15586/15625<1.

This contradicts the strict lower bound 1. Thus t<1/2, proving (9). The calculation includes r=0 and all weak support tangencies. ∎

## 3. The central square with small positive angle does the same

**Theorem 3.** Let C have positive canonical frame

    u_C=dx+ry, v_C=−rx+dy,
    0≤r<8/25, d≥r, d²+r²=1.

Suppose C strictly owns

    O=(0,0), E=(−.65,0), D_C=(0,−.5), M_C=(−.35,−.35),

excludes B0=(−.35,.35), G=(.35,−.35), and excludes the entire segment joining

    D=(.26,0), P=(0,.26).

Let B satisfy the strict point and four-point exclusion premises on B in Theorem 1. If the interiors of B and C are disjoint, then

    t<1/2.                                               (16)

No wall or upper side bound is used once r<8/25 has been established.

**Proof.** Suppose t≥1/2. Put H_C=d+r and H=b+t. Then d>.947, H_C<1.27, and B's angle is strictly greater than C's. If C's upper faces are u,v, the exclusions B0,G give

    0<u≤.35(d−r), 0<v≤.35(d+r), v>.65r.                (17)

Indeed B0 is forced upper v by M_C and O. If G failed lower v, the opposite v-faces would give a≤.7(d+r)<1; hence it is upper u. The final strict bound in (17) is the projection of E.

Write α=bd+tr>0 and k=td−br>0. As in Theorem 2, both orders on C's u-axis fail: O and H2 rule out C-before-B, and the cap on u in (17) rules out the reverse by a gap at most .7(d−r)<1. On B's u-axis, O and H2 again exclude C-before-B. For the reverse, bound the lower C-support by using u≤.35(d−r), a>1, and v−a<−.5d from D_C. After subtracting u_B(M), the strict upper bound has coefficients

    F0=.7−d−.35r²+.15dr
        <.7−.947+.15(.32)<0,
    G0=−.85−r+.15r²+.35dr
        <−.85+.15(.32)²+.35(.32)<0.

This excludes the reverse order. Both upward transverse reverse orders are excluded by the two markers. Thus only (CV) or (BV), in the notation of Theorem 2, can remain.

The chord table (2) gives under (CV)

    v≤L_B(−r,d)<−dK+rG4,
    K=H−1−.6bt,
    G4=b−t+.4+.6t².

The first inequality need only be weak; the strict estimate on the right follows from a>1. Combined with v>.65r, it requires

    dK<rJ0, J0=b−t−.25+.6t².

For t≥1/2, K increases with b+t and satisfies K≥.35sqrt(3)−.5>.106. Also J0 decreases with t and is at most sqrt(3)/2−.6<.267. Therefore dK>.947(.106)=.100382 while rJ0<.32(.267)=.08544. This is impossible. Only (BV) remains, with the exact inequality

    a(1+k)≤H+ku−αv.                                    (18)

At D its lower u- and upper v-bands follow from O, and its lower v-band follows from D_C. Therefore u≤.26d. At P both lower bands follow from O, so its exclusion gives the exhaustive alternatives

    u≤.26r,  or  v≤.26d.                               (19)

### 3.1. The first alternative

If u≤.26r, equations (17)–(18) give

    1<bF+tG5,
    F=1+r−.26r²−.65dr,
    G5=1−d+.26dr−.65r².

Here F≥1, 0≤G5≤.0832, and

    F≤1+.389r−.26r²≤1.097856.

The last expression increases on 0≤r≤.32; it uses d>.94. The estimate G5≤.26r follows from 1−d≤.6r². For t≥1/2, sqrt(1−t²)F+tG5 decreases. Thus

    bF+tG5
      <.87(1.097856)+.5(.0832)
       =778699/781250<1,

contradicting the necessary strict inequality.

### 3.2. The second alternative

Suppose v≤.26d. On the line x+y=.26 the two upper band inequalities, together with u≤.26d and v≤.26d, imply 0<x<.26. Thus every interior intersection with the line would lie in the actual excluded segment DP. Since O lies below the line, convexity forces the closed C into x+y≤.26. Its exact support gives

    H_C u+(d−r)v≤.26.                                  (20)

The identity

    k(d−r)+αH_C=H

and v>.65r yield from (18)–(20)

    1<bF+tG6,
    F=1+r−.91r/H_C,
    G6=.26+(1−d)−.91r/H_C.

Put q=.91/H_C>.71. Since 1−d≤.6r²,

    bF+tG6
      ≤b+.26t+r(.29b−.71t)+.6tr²
      ≤b+.26t+r(.29b−.518t)
      ≤b+.26t−.0067r.

The last bound uses t≥.5 and b≤sqrt(3)/2<.87. The function sqrt(1−t²)+.26t decreases on this range and is less than .867+.13=.997 at its lower endpoint. This is the final contradiction. Therefore t<1/2, as asserted. ∎

## 4. Completion of original representatives 29 and 104

The source is `../original-handoff/03-C981-SHARED-WALL-CYCLES.md`. All point and segment consequences invoked here were proved from the retained local ownership entrance; no center has been added as a new premise.

### 4.1. Representative 29 in its original orientation

Its varying exact auxiliary sets are

    Q5={4,16,18}, Q6={7,17}, Q7={5,13},
    Q10={8,9,19}, Q11={3,14};

Q2,Q3,Q4 have empty auxiliary sets, and its other four exact sets are the common ones in original Section 3. The common entrance proofs in Sections 4.1–4.2 of `C981-COMMON-CYCLE.md`, which do not use the unavailable right-wall point (3,2.56), give

    (2,2),(1.5,2),(2,2.5) strictly in Q7,
    {1}×[2.26,2.8] strictly in Q8,
    [2.26,2.8]×{1} strictly in Q9,
    [1.44,2]×{3} strictly in Q11.

In particular (2,3) is a derived strict point of the actual top-wall square. The actual northeast corner Q3 strictly owns (3,3).

Rotate the whole configuration by (x,y)↦(4−y,x), and then translate by (−2,−2). Use the actual squares

    C=Q7, B=Q6, A=Q5, R=Q10.

The upper square B has exactly the common marker and two anchors in Theorem 1. Its four short-chord exclusions have the following genuine sources.

| Working-coordinate exclusion | Original strict source |
|---|---|
| (−1,0) | Q11: (2,3) |
| (−.4,0) | Q7: (2,2.4), on its strict central segment |
| (−1,1) | Q3: (3,3) |
| (−.4,1) | Q10: (3,2.4), auxiliary 19 |

The square R strictly owns (−.4,1),(.26,1), supplied respectively by its original auxiliaries 19 and 8. It excludes T=(.4,1), which is the original point (3,1.6), auxiliary 18, strictly owned by Q5. Its actual wall x≤4 becomes y≤2. Thus Theorem 1 applies whenever B has positive canonical angle and gives t>1/2.

We first exclude a nonpositive angle of B. An axial B is already impossible by its two short chords. If C has nonnegative canonical angle, Theorem 2 of `C981-COMMON-CYCLE.md` applies in the original orientation. Its whole diagonal foreign segment belongs to the actual Q5, through auxiliaries 4 and 16; its whole wall segment belongs to Q8. It gives the strict point (2,2.65) in C. The negative-sign part of Theorem 1 of the same chapter puts that point in B using only its four short-chord exclusions. Its fifth right-wall exclusion is used exclusively for the positive-sign branch, so it is not imported here. This is a duplicate strict point.

If both C and B have strictly negative canonical angles, apply the retained negative/negative two-square theorem in `C981-RETAINED-CONTINUOUS-LEMMAS.md`, after the same rotation. Its three foreign B points are, in the present translated coordinates,

    (−.4,1), (−1,1), (−1.086,0).

Their actual original sources are (3,2.4) in Q10, (3,3) in Q3, and (2,3.086) in Q11. Its central exclusions are supplied by the missing southwest marker. This excludes the other negative-B alternative. Consequently B has strictly positive canonical angle, and Theorem 1 gives t>1/2.

If C has nonpositive canonical angle, all premises of Theorem 2 hold. In particular its two new foreign points have the exact sources

| Theorem 2 exclusion | Original strict source |
|---|---|
| D=(.26,0) | Q5: (2,1.74), auxiliary 4 |
| J=(.26,−1) | Q1: (1,1.74), retained singleton consequence and auxiliary 0 |

The theorem gives t<1/2, a contradiction.

It remains that C has positive canonical angle. Apply the two audited theorems of `C981-OPPOSITE-CENTRAL-ANGLE.md` to actual A,C, with the owner table in its Section 3. This uses the original permitted 1<a≤1001/1000 and proves r<8/25. The same positive-C point lemma cited above gives (2,2.65) in original Q7, which becomes the strict point E=(−.65,0). Its other crosspoint supplies D_C=(0,−.5). The entire diagonal DP belongs strictly to actual A=Q5. All other strict anchors and exclusions of Theorem 3 are the actual two central markers and the genuinely missing southwest marker. Thus Theorem 3 gives t<1/2, contradicting Theorem 1 once again.

All canonical angle choices have been excluded. Representative 29 therefore has a complete continuous exclusion.

### 4.2. Representative 104 after transposing the entire configuration

Transpose every point and actual square by (x,y)↦(y,x), and use the relabeling

    (Q̃0,Q̃1,Q̃2,Q̃3,Q̃4,Q̃5,Q̃6,Q̃7,Q̃8,Q̃9,Q̃10,Q̃11)
      =(Q1,Q0,Q4,Q3,Q2,Q7,Q6,Q5,Q9,Q8,Q11,Q10).

The exact auxiliary sets are

    Q̃0={2,12}, Q̃1={0,10}, Q̃2={18}, Q̃3=Q̃4=∅,
    Q̃5={4,16}, Q̃6={7,17}, Q̃7={5,13},
    Q̃8={1,11}, Q̃9={6,15}, Q̃10={8,9,19}, Q̃11={3,14}.

These are exactly the strict and excluded data used in Section 4.1. The single changed source is auxiliary 18: the excluded R point (3,1.6) is now strictly owned by the actual paired corner Q̃2=Q4 rather than by A=Q̃5. Theorem 1 uses its exclusion from R only. Neither central theorem uses ownership of this point by A.

Every common entrance remains valid. In particular the derived ordinary center belongs to Q̃7, which is actual original Q5. No center is asserted in original Q7. Apply the same rotation and translation to these relabeled squares. Theorems 1–3 and the negative-B alternatives apply without any alteration, giving the same contradiction. This completes representative 104.

## 5. Combined current C981 scope

The seven continuous exclusions in `C981-WALL-CYCLES.md`, the eight in `C981-COMMON-CYCLE.md`, and the two proved here cover all seventeen original targets:

    2,24,26,28,29,30,37,39,43,
    59,71,103,104,105,107,69,108.

The final two rows use the actual common side cap only in the positive-C angle reduction. The negative-C ending and the right-wall theorem require only a>1. Each whole foreign segment retains one named actual owner, all tangencies are allowed, and the missing marker remains unowned. No finite geometric enumeration or angle subdivision is used in these continuous endings.
