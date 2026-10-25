# C1092 MMMM: a complete continuous three-central-square ending

All terminating decimals are exact rational numbers. This chapter completes the reduction in `C1092-MMMM-CONTINUOUS-REDUCTION.md`, Sections 1–8. It excludes every configuration in the original MMMM entrance, including all of its original auxiliary alternatives. Every square used below is an actual original owner. The common side satisfies a>1; the original upper bound on a is not needed in this ending.

Owned points are strictly inside their stated owners. Excluded points may lie on a face, and separation of two closure supports may be equality. The argument treats whole canonical angle intervals and every separating face axis. No sampled angles or numerical optimization are used as proof.

## 1. The actual points used from the completed reduction

Translate the original coordinates by (−2,−2), and write

    N=Q6, E=Q5, W=Q7.

The following points are strict consequences of the original entrance, proved in the companion reduction:

| Actual owner | Strict points or segment used here |
|---|---|
| N | O=(0,0), X=(.5,0), Y=(0,.5), M_N=(.35,.35) |
| E | M_E=(.35,−.35), (1,−.26), (1,−.4) |
| W | M_W=(−.35,.35), (−.26,1), (−.4,1) |
| Q9, bottom wall | [.22,.39]×{−1} |
| Q8, left wall | {−1}×[.22,.39] |
| Q10, right wall | (1,0) |
| Q11, top wall | (0,1) |
| Q1, southeast corner | (1,−1) |
| Q3, northwest corner | (−1,1) |

Here O is the actual N-owned point proved in Section 8, and X,Y are the crosspoints proved in Section 5. In particular the entire triangle OXY is strict in this same square N. The bar segments come from Section 1, the right and top origins from Section 4, and the corner points from the original paired-corner seeds. The E and W auxiliary pairs were proved in Section 3. Thus every exclusion below has a named different actual owner.

The configuration consisting of these points and actual owners is invariant under simultaneous transposition x↔y, which exchanges E with W, Q9 with Q8, Q10 with Q11, and the two corner owners. Choose a canonical frame for N and transpose the entire configuration if necessary so that

    N: u_N=dx−ry, v_N=rx+dy,
    0≤r≤d, d²+r²=1.

Write its strict bands as

    U<u_N<U+a, V<v_N<V+a.                              (1)

Since O is strict in N,

    U<0, V<0, U+a>0, V+a>0.                            (2)

Axial and diagonal canonical frames are included. Transposition and relabeling of faces do not alter any actual square or point ownership.

## 2. Two genuine short chords force both adjacent angles to be steep

The square E has a nonempty vertical chord at x=.39: convexity between its strict marker, whose x-coordinate is .35, and either strict point at x=1 gives a strict chord point with −1<y<0. Its two endpoints (.39,−1),(.39,0) are excluded by actual Q9 and N, respectively. The latter point lies on the strict segment OX.

The vertical chord of E at x=1 is also nonempty. Its two points (1,−1),(1,0) are excluded by actual Q1 and Q10. Both chords are therefore contained in −1≤y≤0 and have length at most one. The complete transposed argument gives W two horizontal chords at y=.39 and y=1, each contained in −1≤x≤0.

We record the resulting full face table in coordinates convenient for both later pair arguments. Rotate E through a half-turn about O, or first transpose W and then make that half-turn. Denote the resulting actual square by B. In either application it strictly owns

    M=(−.35,.35), H1=(−1,.26), H2=(−1,.4),             (3)

and has nonempty vertical chords at x=−1 and x=−.39, both contained in 0≤y≤1.

Let b≥t≥0, b²+t²=1 be the absolute canonical components of B. An axial square has chord length a>1 at every line meeting its interior, so t>0. If Z is its center x-coordinate, its exact vertical chord length is

    length(x)=min(a/b,
                  max(0,[a(b+t)/2−|x−Z|]/(bt))).       (4)

The plateau a/b is greater than one. Both chords are therefore in the sloping parts of (4). The center lies strictly between −1 and −.39. Indeed, if it lay on or to the left of −1, the chord at −1 would put the right support at most −1+bt≤−.5, contradicting the strict chord at −.39. If it lay on or to the right of −.39, that chord would put the left support at least −.39−bt≥−.89, contradicting the strict chord at −1.

Write the lower B faces as p,q. The two canonical signs give the complete table

| B frame | Lower p | Upper p+a | Lower q | Upper q+a |
|---|---:|---:|---:|---:|
| u_B=bx+ty, v_B=−tx+by | p≥−b | p+a≤t−.39b | q≥.39t | q+a≤b+t |
| u_B=bx−ty, v_B=tx+by | p≥−b−t | p+a≤−.39b | q≥−t | q+a≤b−.39t |

For completeness, in the positive frame the left-chord endpoints are

    (p+b)/t, (q+a−t)/b,

and the right-chord endpoints are

    (q−.39t)/b, (p+a+.39b)/t.

Putting these four endpoints in [0,1] gives the first row. In the negative frame the left endpoints are

    (q+t)/b, (−b−p)/t,

and the right endpoints are

    (−.39b−p−a)/t, (q+a+.39t)/b.

They give the second row. Thus none of the four faces in either sign has been omitted.

Both rows imply

    1<a≤t+.61b.

Set h=t/(1+b). The exact factorization

    (1+h²)(t+.61b−1)=(1−h)(161h−39)/100

and 0<h≤sqrt(2)−1<1 give

    h>39/161,
    b<12200/13721<.9,
    t>6279/13721>.45.                                  (5)

We also use the elementary canonical bounds

    b>7/10, t≤1/sqrt(2)<5/7,
    1<b+t≤sqrt(2)<10/7.                                (6)

These facts hold separately for both actual adjacent squares, with either sign initially allowed.

## 3. Full-square supports and the standardized central pairs

For a square Q and a direction n, denote its minimum and maximum closure projections by L_Q(n), R_Q(n). If its lower face coordinates are z1,z2 and the components of n in its orthonormal frame are A,B, then

    L_Q(n)=A z1+B z2+a min(A,0)+a min(B,0),
    R_Q(n)=L_Q(n)+a(|A|+|B|).                           (7)

Two disjoint open squares have a weak projection separation on a face-normal axis of one of them. Thus the two directions on each of the two C axes and two B axes form an exhaustive list. Formula (7) is always applied to the original full squares, with their common side a.

Both pair arguments will use a central square C strictly owning

    O=(0,0), D=(0,−.5), A=(−.5,0),
    M_C=(−.35,−.35),                                   (8)

and excluding the other two central markers

    G=(.35,−.35), M=(−.35,.35).                         (9)

The neighboring B owns (3), has one of the two complete face rows in Section 2, and is disjoint from C. The first actual application is the half-turn of (N,E). The second is the transposition followed by the half-turn of (N,W). These maps will be tracked explicitly in Section 7.

Write the upper C faces as u,v, so its lower faces are u−a,v−a. Strict ownership of O gives u,v>0.

## 4. A nonpositive central angle excludes a negative neighbor

First give C the frame

    u_C=dx−ry, v_C=rx+dy,
    0≤r≤d, d²+r²=1.                                   (10)

At G, its lower u-band and upper v-band follow strictly from O, and its lower v-band follows from D, with projection increment .35r+.15d>0. Its actual exclusion therefore gives

    0<u≤.35(d+r), v>0.                                 (11)

In this section suppose B has the negative frame (b,−t). We prove that no separator exists.

### 4.1. Exhaustive reduction to three possible orders

Neither order on C's u-axis is possible. C-before-B is excluded by O and M, since M projects to −.35(d+r)<0. For B-before-C, (11) gives

    u−a≤.35(d+r)−a<−.35(d+r),

because .7(d+r)≤.7sqrt(2)<1<a. The strict point M in B excludes that order too.

On B's u-axis, C-before-B is excluded by O and H2, since u_B(H2)=−b−.4t<0. On either upward transverse normal, B-before-C is excluded by M_C and M: they have the same x-coordinate and their y-coordinates differ by .7. The exhaustive remaining choices are

    p+a≤L_C(b,−t),                                    (L)
    v≤L_B(r,d),                                       (C)
    R_C(t,b)≤q.                                       (B)

The negative face table gives q≤b−.39t−a<0, whereas strict ownership of O gives R_C(t,b)>0. Thus (B) is impossible.

### 4.2. The central transverse normal cannot separate

Put

    alpha=bd+tr>0, h=br−td.

If h≥0, formula (7) and the two upper faces in the negative table give

    L_B(r,d)=h p+alpha q
       <h(−.39b−1)+alpha(b−.39t−1)
       =d f+r g,

where

    f=1−b+t−t²,
    g=−.39−b−t+bt<0.

The exact cancellation is

    b f+t g=b−1−.39t≤0.

Consequently

    b(d f+r g)=d(b f+t g)+h g≤0.

Thus L_B(r,d)<0, contrary to (C) and v>0.

If h≤0, the full lower support instead is

    L_B(r,d)=h(p+a)+alpha q.

Strict ownership of M gives p+a>−.35(b+t). Combining it with the upper q-face and a>1 gives

    L_B(r,d)
       <−.35h(b+t)+alpha(b−.39t−1)
       =d f2+r g2,

where

    f2=1−b−.65t²−.04bt,
    g2=−.35−.04t²+.65bt−t.

Since 1−b=t²/(1+b)≤.6t²,

    f2≤−.05t²−.04bt<0,
    g2≤−.35−.35t−.04t²<0.

Again L_B(r,d)<0. Both relative-angle orders, including h=0, have been covered; (C) is impossible.

### 4.3. The remaining longitudinal normal cannot separate

Suppose first that h≥0. In (L) the exact lower C support is

    L_C(b,−t)=alpha(u−a)+h(v−a).

Use (11), a>1, and v−a<−.5d from D. After subtracting the projection −.35(b+t) of the strict B marker M, the resulting strict upper bound is bF+tG0, where

    F=.7−d−.35r²−.15dr,
    G0=.85−r−.15r²+.35dr>0.

The latter positivity follows from d≥r and r<5/7. The exact identity

    dF+rG0=.7(d+r)−1<0

gives

    d(bF+tG0)=b(dF+rG0)−hG0<0.

Thus L_C(b,−t) is less than the projection of M, contradicting (L).

It remains that k=td−br>0. The support is now

    L_C(b,−t)=alpha(u−a)−k v.

The lower p-face in the negative table is p≥−b−t. Hence (L) requires

    a(1+alpha)≤b+t+alpha u−k v.

Put H=d+r and q0=1−.35H. By (11), v>0, and a>1,

    1<b+t−alpha q0.                                    (12)

But q0>0 and the canonical orders imply

    2alpha−(b+t)H=(b−t)(d−r)≥0.

Also 1≤H≤10/7 and

    Hq0−.65=(H−1)(.65−.35H)≥0.

Therefore

    b+t−alpha q0
       ≤(b+t)(1−Hq0/2)
       ≤(10/7)(1−.65/2)=27/28<1,

contrary to (12). The negative sign of B is impossible.

## 5. The positive neighbor leaves one exact support inequality and makes the central angle small

Retain the nonpositive central frame (10) and (11), but give B its positive frame (b,t). Put

    alpha=bd−tr≥0, k=br+td>0.                          (13)

The two orders on C's u-axis are impossible by exactly the O,M comparisons in Section 4.1. C-before-B on B's u-axis is excluded by O and H2, since −b+.4t<0. For B-before-C on that axis, the full support is

    L_C(b,t)=alpha(u−a)+k(v−a).

Use (11), a>1, and v−a<−.5d. After subtracting the B-marker projection −.35b+.35t, the strict upper bound is bF0+tG0, where

    F0=.7−d−.35r²−.15dr<0,
    G0=−.85+r+.15r²−.35dr
       ≤−.85+r−.20r²<0.

Here d>7/10 and r<5/7. The strict estimate remains valid if alpha=0, since k>0 and D is strict. Thus this axis fails too. As before, both upward transverse reverse orders are excluded by M_C,M. Only

    v≤L_B(r,d),                                       (C+)
    R_C(−t,b)≤q                                      (B+)

remain.

Define

    H_B=b+t,
    K=H_B−1−.61bt
      =(H_B−1)[1−.305(H_B+1)]>0.                      (14)

The positivity follows from 1<H_B≤sqrt(2)<10/7. The positive face table gives

    L_B(r,d)=k p+alpha q
       <k(t−.39b−1)+alpha(H_B−1)
       =−dK+r(t−b−.39−.61t²)<0.

This excludes (C+). The only possible separator is (B+). Its exact full C support is

    R_C(−t,b)=k(a−u)+alpha v.

Using q≤H_B−a, the retained necessary inequality is

    a(1+k)≤H_B+k u−alpha v.                            (15)

We now extract a uniform continuous consequence of (15). With H=d+r and q0=1−.35H, (11), a>1 and v>0 give

    1<bF+tG,
    F=1−r q0, G=1−d q0.                               (16)

Both F,G are positive. Cauchy–Schwarz and b²+t²=1 force F²+G²>1. Direct expansion gives the exact scalar polynomial

    F²+G²−1=P(H),
    P(H)=2−2.7H+.8225H².                               (17)

For 1≤H≤10/7,

    P'(H)=−2.7+1.645H≤−.35,
    P(1.13)=−2999/4000000<0.

Thus P(H)>0 requires H<1.13. The function sqrt(1−r²)+r increases on the entire canonical interval 0≤r≤1/sqrt(2), and

    sqrt(1−.14²)+.14>.99+.14=1.13,

because 1−.14²=.9804>.99²=.9801. Consequently

    r<.14, d>.99.                                      (18)

This is the audited H-polynomial calculation, here derived from the actual two-chord face table and the complete separator list. Its application did not assume a small central angle in advance.

## 6. A small nonnegative central angle also forces a positive neighbor and one separator

Now give the standardized central square C the positive frame

    u_C=dx+ry, v_C=−rx+dy,
    0≤r<.14, d>.99, d²+r²=1.                          (19)

It retains the strict anchors (8), genuine exclusions (9), and upper faces u,v. These imply

    0<u≤.35(d−r),
    0<v≤.35(d+r), v>.5r.                              (20)

Indeed, at G the lower u-band and upper v-band follow from O, and the lower v-band follows from D because .15d−.35r>0. Thus G is upper u. At M the upper u-band and lower v-band follow from O, and the lower u-band follows from A because .15d+.35r>0. Thus M is upper v. The strict last inequality in (20) is the projection of A.

The two orders on C's u-axis are impossible by comparing O,M and using .7(d−r)<1<a, exactly as in Section 4.1. On either sign of B's u-axis, C-before-B is excluded by O and H2. Both upward transverse reverse orders are excluded by M_C,M. We examine the three remaining possibilities for each sign.

### 6.1. The negative sign of B is impossible

Suppose B has frame (b,−t). Set

    alpha=bd−tr>0, k=br+td>0.

The only possible orders are

    p+a≤L_C(b,−t),                                    (L−)
    v≤L_B(−r,d),                                      (C−)
    R_C(t,b)≤q.                                       (B−)

The negative face table gives q≤b−.39t−a<0; strict O excludes (B−).

For (L−), formula (7) gives

    L_C(b,−t)=alpha(u−a)−k v.

Since p≥−b−t, this would require

    a(1+alpha)≤b+t+alpha u−k v.

Equations (20) and a>1 yield the strict necessary inequality

    1<bF+tG,
    F=1.35−d−.35dr−.85r²,
    G=1+r−.85dr+.35r².                                (21)

For 0≤r<.14, one has 0<F≤.36 and G≥1. Holding d,r fixed, the expression sqrt(1−t²)F+tG is increasing over 0≤t≤1/sqrt(2), because its derivative is

    G−tF/sqrt(1−t²)≥G−F>0.

Furthermore 1−d=r²/(1+d)≤.6r² and d>.99 give

    F+G
      =1.35+(1−d)+r(1−1.2d)−.5r²
      ≤1.35−.188r+.1r²≤1.35.

Consequently

    bF+tG≤(F+G)/sqrt(2)≤1.35/sqrt(2)<1,

since 1.35²<2. This contradicts (21) and excludes (L−).

It remains to exclude (C−). Its exact lower B support is

    L_B(−r,d)=−k(p+a)+alpha q.

Use p+a>−.35(b+t), supplied by the strict marker M, and q≤b−.39t−a. Then

    L_B(−r,d)
       <.35k(b+t)+alpha(b−.39t−1)
       =d f+r g,

where

    f=1−b−.65t²−.04bt,
    g=.35+.04t²−.65bt+t.                              (22)

We prove d f+r g<.5r, contradicting (20). Since b>.7,

    1−b=t²/(1+b)<.59t²,
    f<−.06t²−.04bt<0.

If g≤.5 the desired inequality is immediate. If g>.5, use d>.99, r<.14, and b>.7 to obtain

    d f+r(g−.5)
       <−.99(.06t²+.04bt)
           +.14(−.15+t+.04t²−.65bt)
       =−.021+.14t−.0538t²−.1306bt
       <−.021+.04858t−.0538t².                        (23)

The final quadratic is negative for every real t. Its leading coefficient is negative and its discriminant is exactly

    .04858²−4(.0538)(.021)
       =−5397959/2500000000<0.

Thus (C−) is impossible as well. This excludes the full negative sign of B, including all of its relative angles and all support tangencies.

### 6.2. The positive sign leaves only B's own transverse normal

B therefore has positive frame (b,t). Put

    alpha=bd+tr>0, k=td−br>0.                          (24)

The second positivity follows from t>.45, d>.99, b<.9, r<.14. For the remaining B-before-C order on B's u-axis,

    L_C(b,t)=alpha(u−a)+k(v−a).

Use u≤.35(d−r), a>1, and v−a<−.5d from D. After subtracting the strict B-marker projection −.35b+.35t, the upper bound is bF0+tG0, where

    F0=.7−d−.35r²+.15dr<0,
    G0=−.85−r+.15r²+.35dr<0.

For example F0<.7−.99+.15(.14)<0, while G0<−.85+.15(.14²)+.35(.14)<0. Thus this axis cannot separate. The only remaining orders are

    v≤L_B(−r,d),                                      (C++)
    R_C(−t,b)≤q.                                      (B++)

For (C++), use the positive face table and define K as in (14). The exact expansion is

    L_B(−r,d)
       =k p+alpha q
       <k(t−.39b−1)+alpha(b+t−1)
       =−dK+r(b−t+.39+.61t²).

Together with v>.5r, this would imply

    dK<rJ,
    J=b−t−.11+.61t².                                 (25)

This is impossible on the whole domain (5), (19). First H_B=b+t>1.34: the function sqrt(1−t²)+t increases on the canonical interval, t>.45, and sqrt(1−.45²)>.89. As a function of H_B,

    K=H_B−1−.305(H_B²−1)

has derivative 1−.61H_B>0 for 1≤H_B≤10/7. Therefore

    K>K(1.34)=.097342>.095,
    dK>.99(.095)=.09405.

On the other hand b<.9, t>.45 and t²≤1/2 give

    J<.9−.45−.11+.305=.645,
    rJ<.14(.645)=.0903.

The exact gap between these two rational bounds is .00375=3/800, contrary to (25). Hence (C++) is excluded.

Only (B++) remains. Its exact full C support is

    R_C(−t,b)=k(a−u)+alpha v.

With q≤b+t−a, the necessary inequality is therefore

    a(1+k)≤b+t+k u−alpha v.                            (26)

This completes the continuous separator analysis for the small nonnegative central angle.

## 7. Apply the two pair results to the same actual northeast square

For the first pair apply the half-turn

    J(x,y)=(−x,−y)

to the actual (N,E). The central square C=J(N) has the nonpositive frame (10), strict points (8), and exclusions (9) supplied by actual J(W),J(E). The square B=J(E) has (3) and the complete chord table from Section 2. Its two possible signs are exhaustive.

Section 4 excludes its negative sign. Thus E has positive canonical components (b_E,t_E), with the bounds (5)–(6). Section 5 gives

    r<.14, d>.99,
    alpha_E=b_E d−t_E r≥0,
    k_E=b_E r+t_E d>0.                                (27)

Under J, the upper faces of C are

    u=−U, v=−V,

where U,V are the original actual N faces in (1). The exact retained inequality (15) becomes

    alpha_E V−k_E U≥a(1+k_E)−H_E,
    H_E=b_E+t_E.                                      (28)

For the second pair use

    JT(x,y)=(−y,−x)

on the actual (N,W). The same N becomes a standardized central square with positive frame (19); its upper face coordinates are now

    u=−V, v=−U.                                       (29)

The strict anchors (8), exclusions (9), and B points and chords are again literal images of the actual-owner table in Section 1. The angle bound needed in (19) is precisely (27), already proved using the first pair.

Section 6 excludes the negative sign of B=JT(W), leaving its positive sign with components (b_W,t_W). Equivalently the original W has negative canonical sign. Define

    alpha_W=b_W d+t_W r>0,
    k_W=t_W d−b_W r>0,
    H_W=b_W+t_W.                                      (30)

The retained inequality (26), with the face identification (29), gives

    alpha_W U−k_W V≥a(1+k_W)−H_W.                     (31)

Equations (28) and (31) are simultaneous statements about the same original N faces U,V. They do not concern two independently chosen central squares. Every transported pair has common side a and disjoint interiors because it is a rigid image of actual owners.

## 8. Cancellation gives the exact positive margin

Since a>1, (28) and (31) imply the strict inequalities

    alpha_E V−k_E U>D_E,
    alpha_W U−k_W V>D_W,                              (32)

where

    D_E=1+k_E−H_E
       =1−b_E+b_E r−t_E(1−d),
    D_W=1+k_W−H_W
       =1−b_W−b_W r−t_W(1−d).

Multiply the first inequality in (32) by alpha_W>0, the second by k_E>0, and add. The U-coordinate cancels exactly:

    (alpha_E alpha_W−k_E k_W)V
       >alpha_W D_E+k_E D_W.                          (33)

The coefficient has the exact simplification

    alpha_E alpha_W−k_E k_W
       =b_E b_W−t_E t_W≥0,                            (34)

using d²+r²=1 and the canonical inequalities b_E≥t_E, b_W≥t_W. By (2), V<0. Thus the left side of (33) is nonpositive, even when the coefficient in (34) vanishes.

The right side is uniformly positive. Bounds (5)–(6), (18) give

    alpha_W>(7/10)(99/100)=693/1000,
    D_E>1−.9−(5/7)(.01)=13/140,
    D_W>1−.9−.9(.14)−(5/7)(.01)=−29/875.             (35)

Moreover 0<k_E≤1: it is the dot product of the two unit vectors (b_E,t_E) and (r,d). Whether D_W is nonnegative or negative, (35) consequently implies

    k_E D_W>−29/875.

Therefore

    alpha_W D_E+k_E D_W
       >(693/1000)(13/140)−29/875
       =4369/140000>0.                                (36)

Equations (33)–(36) are contradictory. Hence the original MMMM configuration does not exist.

## 9. Scope and boundary check

The companion reduction proves the entrance of Section 1 from the complete original C1092 ownership alternatives and the four closed MMMM wall signs. This ending makes no additional auxiliary choice. It uses the actual NE center point only after that point has been proved in its named owner, and it uses the bottom and left bars only as the actual whole strict segments supplied by their wall owners.

The initial square N may be axial or diagonal. Both signs of each adjacent square are considered; the axial adjacent cases are excluded by their actual short chords. Every relative-angle sign in the nonpositive/negative pair is covered, including equality. The later strict relative-angle comparison is deduced from t>.45 and r<.14. Each possible separating normal and both separation directions are either retained explicitly or excluded by the stated full-square support and strict-point comparisons. Weak face exclusions and closure contacts are permitted throughout. Strict ownership and a>1 supply the strict final inequalities.

Thus the entire original MMMM class, not merely a subset of its 55,126 auxiliary alternatives, has a complete continuous geometric exclusion. The original simultaneous container symmetries then exclude every sign label in its MMMM orbit as specified in `C1092-ORIGINAL-ENTRANCE.txt`, Section 3.
