# C981: eight ordinary-wall cycles reduced to continuous point and support lemmas

All terminating decimals denote exact rational numbers. Squares are open, have a common side length a>1, and have pairwise disjoint interiors. An owned point is strictly inside its actual square; an excluded point may lie on the boundary. Every separating inequality below allows equality.

This chapter gives complete continuous exclusions of original representatives **2, 28, 30, 37, 43, 69, 103, and 107**. Sections 1–5 first exclude four of these rows with a shared point at (2,2.65). Sections 6–7 improve the positive-angle point lemma: the slightly lower shared point (2,2.62) gives one common ending for seven rows in their original orientation. Section 8 maps representative 107 into exactly the same common geometric hypotheses by transposing the entire configuration. The proof uses genuine wall and corner owners, the retained ordinary-wall center theorem, compulsory-point arguments, and a short two-square angular contradiction. No angle sampling, artificial central owner, or assumption about the center of a square is used.

## 1. An upper square has a compulsory left point

**Theorem 1.** Let Q be a square of side a>1 strictly owning

    M=(2.35,2.35), F=(2.26,3), T=(2.4,3).

Suppose Q excludes

    (2,2.4), (2,3), (3,2.4), (3,3), (3,2.56).

Then Q strictly owns

    X=(2,2.65).                                             (1)

If Q has a positive canonical frame (c,s), with 0≤s≤c and c²+s²=1, its half-angle satisfies

    h=s/(1+c)>7/18.                                        (2)

The square cannot be axial. Both canonical signs, including their diagonal representatives, are covered by the point conclusion.

**Proof.** Convexity gives the strict vertical segment at x=2.35 from height 2.35 to height 3. The horizontal chords of Q at y=2.4 and y=3 are therefore nonempty. The excluded endpoints at x=2 and x=3 put both chord lengths at most one. An axial square would have chord length a>1, so it is impossible.

Write the absolute canonical components c≥s>0. The exact horizontal chord formula at ordinate y, with center ordinate Y, is

    length(y)=min(a/c, max(0,[a(c+s)/2−|y−Y|]/(cs))).       (3)

The plateau length a/c is greater than one. Thus both short chords are outside the plateau. If Y≤2.4, formula (3) bounds the upper support of Q by 2.4+cs≤2.9, contrary to its strict point at height 3. If Y≥3, it bounds the lower support by 3−cs≥2.5, contrary to M. Therefore

    2.4<Y<3.

Translate by (−2,−2.7). The chord lines become y=−.3 and y=.3; their endpoints lie in [0,1]. The owned marker becomes (.35,−.35), the top anchors become (.26,.3),(.4,.3), and the target is (0,−.05).

Let U,V be the lower face coordinates. In a positive frame, u=cx+sy and v=−sx+cy. The bottom-vertex and top-vertex chord endpoints give the four weak bounds

    U≥−.3s,       V≥−.3c−s,
    U+a≤c+.3s,    V+a≤.3c.                               (4)

In a negative frame, u=cx−sy and v=sx+cy, the corresponding bounds are

    U≥−.3s,       V≥−.3c,
    U+a≤c+.3s,    V+a≤s+.3c.                             (5)

For example, in the positive frame the lower chord endpoints are (U+.3s)/c and (−V−.3c)/s; the upper endpoints are (.3c−V−a)/s and (U+a−.3s)/c. This verifies (4) directly. In the negative frame the lower endpoints are (V+.3c)/s and (U+a−.3s)/c, and the upper endpoints are (U+.3s)/c and (V+a−.3c)/s, giving (5).

Both tables imply a≤s+.6c. Put h=s/(1+c). Since a>1,

    (1+h²)(s+.6c−1)=(2/5)(4h−1)(1−h)>0,

so h>1/4. We repeatedly use the exact identity

    c+γs−1=2h(γ−h)/(1+h²).                              (6)

First use the positive frame. The excluded point (3,2.56) is R=(1,−.14) in the translated coordinates. Its lower u-band follows strictly from M, with increment .65c+.21s>0. Its upper v-band follows strictly from F, whose projection exceeds its projection by .74s+.44c>0. Its upper u-band follows from U≥−.3s and

    u(R)−U≤c+.16s<1<a,

using h>1/4 in (6). Therefore R can fail only its lower v-band:

    V≥−s−.14c.

Together with V+a≤.3c, this gives a≤s+.44c. The exact factorization

    (1+h²)(s+.44c−1)=(2/25)(18h−7)(1−h)

proves (2).

At X=(0,−.05), the upper u-band follows from M because u(M)−u(X)=.35c−.30s>0. Its lower v-band follows from M because v(X)−v(M)=.35s+.30c>0. Its upper v-band follows from the original lower bound in (4), since

    v(X)−V≤s+.25c≤1.25/√2<1<a.

Here s+.25c increases over the canonical interval and has the displayed maximum at c=s. Finally (4), (6), and h>7/18>.35 give

    U+a−u(X)≤c+.35s<1<a,

which forces u(X)>U. All four target bands are strict.

In the negative frame, u(M)−u(X)=.35c+.30s>0 gives the upper u-band. The lower u-band follows from

    U+a−u(X)≤c+.25s<1<a

by h>1/4. The upper v-band follows from v(X)−V≤.25c<1<a. The lower v-band follows from

    V+a−v(X)≤s+.35c≤1.35/√2<1<a.

This proves (1) for the second sign as well. All short-chord endpoints and face exclusions were weak; the resulting ownership is strict because every face-width comparison uses a>1. ∎

## 2. A central square with positive angle contains the same point

The next lemma uses two complete foreign segments. Their ownership cannot be replaced by ownership of endpoints in different squares.

**Theorem 2.** Let N be a square of side a>1 with a nonnegative canonical frame u=cx+sy, v=−sx+cy, where 0≤s≤c and c²+s²=1. Suppose N strictly owns

    O=(0,0), E=(−.5,0), P=(0,.5), M=(−.35,.35).

Suppose it excludes L=(−.35,−.35), the entire wall segment

    S={−1}×[.26,.8],

and the entire segment joining

    A=(0,−.26), D=(.26,0).

Then N strictly owns X=(0,.65).

**Proof.** Denote the lower faces by U,V. At A, both upper bands follow from O; its lower u-band follows from E because .5c−.26s≥.24c>0. Thus A's exclusion forces

    V≥−.26c.                                             (7)

Assume X is excluded. Both its lower bands follow from P. Its upper v-band is strict by (7), since v(X)−V≤.91c<1<a. Its only possible failure is consequently

    p:=U+a≤.65s.                                        (8)

Strict ownership of O gives p>0, so s>0.

At L, both upper bands follow from O. A lower u-face exclusion would combine with (8) to give

    a≤.35c+s≤1.35/√2<1,

which is impossible. Hence

    V≥.35s−.35c.                                        (9)

Consider J=(−1,.26). Its lower v-band follows from E, with increment .5s+.26c>0, and its upper u-band follows from P, whose projection exceeds its projection by c+.24s>0. Its upper v-band follows from (9), because

    v(J)−V≤.65s+.61c≤√(.65²+.61²)=√.7946<1<a.

Therefore

    U≥−c+.26s.                                          (10)

At K=(−1,.8), the lower v-band follows from E, with increment .5s+.8c>0, and the upper u-band follows from P, with difference c−.3s>0. A lower u-face exclusion would give, by (8), a≤c−.15s≤1. Thus K fails its upper v-band:

    V+a≤s+.8c.                                          (11)

Equations (10) and (11) show that every interior point of N on x=−1 would have .26<y<.8, which the entire excluded segment S forbids. Since O is strictly in N at x=0, convexity forces the closure of N to lie in x≥−1. Its exact left support is therefore

    cU−s(V+a)≥−1.                                       (12)

Put H=c+s and t=s/c. Combining (8), (9), and (12) gives

    aH≤1+cs−.35s².                                      (13)

We obtain a contradiction in each of two continuous ranges of t.

### 2.1. The range 2/5≤t≤1

Define H(t)=(1+t)/√(1+t²) and

    f(t)=2/(H(t)+1)−1+(7/20)t.

Since 0≤H'(t)=(1−t)/(1+t²)^(3/2)≤3/5 in this range and H+1≥2,

    f'(t)≥7/20−3/10=1/20>0.

At t=2/5 the positivity of f is equivalent to 57√29>301, whose squared difference is

    57²·29−301²=3620>0.

Thus f(t)>0 throughout the range. Using H−1=2cs/(H+1), this is exactly

    H−1>cs−.35s².

Equation (13) gives aH<H, contradicting a>1.

### 2.2. The range 0<t<2/5

On the line y=x−.26 through A and D, the strict lower v-band and (7) imply x>0, because c>s. The strict upper u-band and (8) imply

    x<.91s/H=.91t/(1+t)<.26.

Every interior intersection with this line would therefore belong to the excluded segment AD. Since the strict point O lies above this line, convexity forces the whole closed square to lie in y−x≥−.26. Its exact support in the direction (−1,1) is

    (s−c)p+HV≥−.26.                                    (14)

Multiply (12), in the form aH≤1+cp−sV, by H and use (14). Since cH−s(c−s)=1, the result is

    aH²≤H+.26s+p≤H+.91s.                                (15)

But the exact identity

    H²−H−.91s=s[s/(1+c)+2c−1.91]

has a strictly positive right side. Indeed, canonical c>7/10 gives 1−c=s²/(1+c)≤.6s², while s/(1+c)≥s/2. Also 0<s<t<.4. Thus the bracket is at least

    .09+.5s−1.2s²>.09>0.

This contradicts (15) and a>1. Both ranges have been excluded, so the assumed missing target was impossible. ∎

## 3. A negative central square cannot separate from such a steep positive neighbor

For a square Q and a unit direction n, write L_Q(n), U_Q(n) for the minimum and maximum projections of its closure. Two disjoint open squares have a weak support separation on one of their four face-normal axes.

**Theorem 3.** Let C and B be disjoint squares of common side a>1 with canonical frames

    C: (d,−r),  0≤r≤d, d²+r²=1;
    B: (b,t),   0≤t≤b, b²+t²=1.

Suppose C strictly owns

    O=(2,2), D=(2,1.5), E=(1.5,2), M_C=(1.65,1.65),

and excludes G=(2.35,1.65). Suppose B strictly owns

    M_B=(1.65,2.35), H₁=(1,2.26), H₂=(1,2.4),

and excludes P=(1.5,3), K=(1,3). Then

    t/(1+b)≤7/18.                                       (16)

In fact the proof rules out equality as well. We need only the displayed weak version to combine it with Theorem 1.

**Proof.** Suppose t/(1+b)≥7/18. Then

    t≥252/373>.48,  b≤275/373.                           (17)

Write lower and upper face values with superscripts − and +. At G, C's lower u-band and upper v-band follow from O; its lower v-band follows from D, with increment .35r+.15d>0. Therefore

    U_C^+≤2.35d−1.65r.                                  (18)

Set

    u=U_C^+−2(d−r),  v=V_C^+−2(d+r).

Strict center membership and (18) give

    u>0,  v>0,  u≤.35(d+r).                              (19)

### 3.1. All separating directions except two are impossible

On C's u-axis, C-before-B is impossible by comparing O with M_B: the difference is .35(d+r)>0. The reverse order is impossible because (18) and a>1 give

    U_C^-<2.35d−1.65r−1<1.65d−2.35r,

using .7(d+r)≤.7√2<1, whereas M_B is strict in B.

On B's u-axis, C-before-B is impossible from O and H₂, whose projections differ by b−.4t>0. For the reverse order put

    α=bd−tr≥0,  k=br+td>0.

The lower C support along (b,t) is αU_C^-+kV_C^-. Use (18), a>1, and the strict point D to bound it above by

    α(2.35d−1.65r−1)+k(2r+1.5d).

After subtracting the projection 1.65b+2.35t of M_B, the bound is bF₀+tG₀, where

    F₀=.7−d−.35r²−.15dr<0,
    G₀=−.85+r+.15r²−.35dr
       ≤−.85+r−.20r²<0.

Here d>7/10 and r<5/7. Thus this separator is impossible as well. The strict inequality in the support bound remains valid when α=0 because k>0 and D is strict.

On either upward transverse axis, B-before-C is ruled out by the markers M_C,M_B, which have equal x coordinates and y coordinates differing by .7. The exhaustive remaining choices are therefore

    V_C^+≤L_B(r,d),                                      (CV)
    U_C(−t,b)≤V_B^-.                                    (BV)

### 3.2. The two foreign top points force the two upper faces of B

First,

    V_B^+>3b−1.5t.                                      (20)

If (BV) holds, strict ownership of E gives V_B^->2b−1.5t, and (20) follows after adding a>1≥b. If (CV) holds and (20) fails, then

    L_B(r,d)=kU_B^-+αV_B^-
       <k(b+2.26t)+α(3b−1.5t−1).

Subtracting the center projection 2(d+r) yields df+rg, where

    f=1−b−.74t²−.5bt≤−.14t²−.5bt<0,
    g=−1+t+.5t²−.74bt≤−1+t−.24t²<0.

The first estimate uses 1−b≤.6t²; the second uses b≥t. This contradicts (CV) and strict ownership of O, proving (20).

At P=(1.5,3), the lower u-band follows from H₁, the lower v-band follows from M_B, and the upper v-band is (20). Its exclusion forces

    U_B^+≤1.5b+3t.                                      (21)

At K=(1,3), the lower u- and v-bands follow from H₂. The upper u-band follows from M_B because their projection difference is .65(b−t)≥0. Its exclusion forces

    V_B^+≤3b−t.                                         (22)

Now (CV) is impossible. Use (21)–(22) minus a>1 in the lower support kU_B^-+αV_B^-. After subtracting 2(d+r), the upper bound is

    −dK₀+rG₁,
    K₀=b+t−1−bt/2=(b+t−1)(3−b−t)/4>0,
    G₁=t−b−1/2−t²/2≤−1/2.

It is strictly negative. Thus only (BV) remains.

### 3.3. The surviving support correlation gives a rational contradiction

The exact full-square support is

    U_C(−t,b)=2(b−t)+k(a−u)+αv.

Combining (BV) with (22) gives

    a(1+k)≤b+t+ku−αv.

Since a>1, (19) implies

    1<b+t−kq=bF+tG₂,                                    (23)
    H=d+r, q=1−.35H,
    F=1−rq, G₂=1−dq.

Both F and G₂ are nonnegative. By Cauchy–Schwarz, (23) forces F²+G₂²>1. Direct expansion gives

    F²+G₂²−1=P(H),
    P(H)=2−2.7H+.8225H².

For 1≤H≤10/7 the derivative P'(H)=−2.7+1.645H is at most −.35, so P is decreasing. Since

    P(1.13)=−2999/4000000<0,

we obtain H<1.13. The function √(1−r²)+r is increasing on the canonical interval, and at r=.14 its cosine exceeds .99. Hence

    r<.14, d>.99, q>.6045.                              (24)

The elementary estimate 1−d≤.6r² now gives

    F≤1−.6045r,
    G₂=.35+(1−d)−.35r²+.35dr
       ≤.35+.25r²+.35r≤.35+.385r.                       (25)

Also F≥1−r>.86 and G₂<.4039. For fixed d,r, the function

    √(1−t²)F+tG₂

strictly decreases for t≥.48 within the canonical interval. Its derivative is G₂−tF/√(1−t²)<0 because

    tF≥.48·.86=.4128>.4039≥bG₂.

Apply this monotonicity at the exact lower endpoint (17) and then use (25):

    bF+tG₂
      ≤(275F+252G₂)/373
      ≤[275+252·.35+(-275·.6045+252·.385)r]/373
      ≤1816/1865<1,

because −275·.6045+252·.385=−69.2175<0. This contradicts (23). No equality at a separating support or excluded point was discarded. ∎

## 4. Exact geometric entrance for the four original rows

The source is `../original-handoff/03-C981-SHARED-WALL-CYCLES.md`. The following are the exact auxiliary sets of the varying owners; auxiliary indices retain that source's numbering.

| Original representative | Q2 | Q5 | Q6 | Q7 | Q10 | Q11 |
|---|---|---|---|---|---|---|
| 2 | ∅ | {4,16} | {7,17} | {5,13} | {9,19} | {3,14} |
| 28 | ∅ | {4,16,18} | {7,17} | {5,13} | {9,19} | {3,14} |
| 43 | ∅ | {4,8,16,18} | {7,17} | {5,13} | {9,19} | {3,14} |
| 103 | {18} | {4,16} | {7,17} | {5,13} | {9,19} | {3,14} |

All four have the common strict markers and singleton consequences in the source. In particular Q5 owns (2.35,1.65), Q6 owns (2.35,2.35), Q7 owns (1.65,2.35), Q8 owns (.914,2), Q9 owns (2,.914), Q10 owns (3.086,2), and Q11 owns (2,3.086). The marker (1.65,1.65) is globally absent. The actual paired corners Q3,Q4 strictly own (3,3),(1,3), respectively.

The auxiliary sets have the following literal geometric content:

    Q5: (2,1.74), (2.26,2);
    Q6: (2.4,3), (2.26,3);
    Q7: (2,2.26), (1.74,2);
    Q8: (1,2.26), (1,2.4);
    Q9: (2.4,1), (2.26,1);
    Q10: (3,2.26), (3,2.4);
    Q11: (1.6,3), (1.74,3).

All further strict points used below are proved consequences of these actual owners.

### 4.1. The left segment, center, and two central crosspoints

Theorem 4 of `C981-WALL-CYCLES.md` applies to Q8, using its actual left wall, the foreign singleton point (.76,1.87) in Q1, the foreign (1,1.74) in Q1, and the Q7 marker (1.65,2.35). It gives the strict point (1,2.8). Consequently the whole segment

    {1}×[2.26,2.8] is strict in Q8.                      (26)

Apply the retained ordinary two-wall center theorem after reflection in x=2, with its central square A=Q7, right-wall square R=Q8, and top square T=Q11. In the theorem's coordinates the required data map as follows:

| Center-theorem datum | Actual point or owner |
|---|---|
| A(2,2.26),(2.26,2),(2.35,2.35) | Q7(2,2.26),(1.74,2),(1.65,2.35) |
| R(3.086,2),(3,2.4) | Q8(.914,2),(1,2.4) |
| T(2,3.086),(2.4,3) | Q11(2,3.086),(1.6,3) |
| A excludes (2.35,1.65),(1.65,2.35) | Globally absent (1.65,1.65); Q6(2.35,2.35) |
| R excludes (3,1.74) | Q1(1,1.74) |
| T excludes (1.74,3) | Q6(2.26,3) |

The theorem uses only the genuine outer walls of its two wall squares. It gives

    (2,2)∈Q7.                                            (27)

Its complete retained continuous proof, including its wall lemma, is reproduced in the companion `C981-RETAINED-CONTINUOUS-LEMMAS.md`; this is a derived center, not an extra entrance premise.

Apply the all-angle central crosspoint lemma in the appendix of `C893-CONTINUOUS-EXCLUSION.md`, first after reflection in x=2. Its four foreign points become the missing southwest marker, the actual Q6 marker, and (1,2.4),(1,2.5), both in Q8 by (26). Thus

    (2,2.5)∈Q7.                                          (28)

The retained wall-reach lemma, applied to Q11 under (X,Y)=(4−y,4−x), uses its marker, (1.6,3), and the foreign (2.26,3) in Q6 and (2,2.26) in Q7. With (w,d₀,z)=(1.74,1.74,2.56), it gives

    (1.44,3)∈Q11,

and hence (1.5,3)∈Q11. The exact wall-lemma checks are .82<14/17, .74²+.26²=.6152<1, and .56²+.74²=.8612<1. Apply the crosspoint lemma a second time, now transporting its coordinates by (x,y)↦(4−y,x). The two foreign wall points become (1.6,3),(1.5,3), both in Q11; its other foreign points are again the missing marker and the Q6 marker. This gives

    (1.5,2)∈Q7.                                          (29)

### 4.2. The actual upper-wall origin and right-wall point

The paired corner Q4 strictly owns (1,3). It excludes (1,2.8) in Q8 and (1.74,3) in Q11. Theorem 5 of `OTHER-GEOMETRY.md`, using the real left wall after rotating the corner configuration, applies with

    (p,q,r)=(.74,.2,.6).

Indeed p²+q²=.5876<1, p²+r²=.9076<1, and q+r=.8<2√2−2. The resulting point is (1,3.6), so the actual corner owns the whole segment {1}×[3,3.6].

Apply the wall-origin Theorem 9 of `OTHER-GEOMETRY.md` to Q11 in coordinates (X,Y)=(2−x,y−3). Its actual marker is (0,.086), its owned (1.6,3) becomes (.4,0), its real top wall becomes Y≤1, and Q4's strict segment becomes {1}×[0,.6]. Therefore

    (2,3)∈Q11.                                           (30)

Finally, apply the retained wall-reach lemma to Q10 after reflection in x=2. The owned data are its marker and (3,2.4). The first exclusion is (3,1.74), which is outside its exact auxiliary set in all four rows. The second is (2.26,2), strictly owned by Q5. Again use (w,d₀,z)=(1.74,1.74,2.56). It follows that

    (3,2.56)∈Q10,
    (3,2.5)∈Q10.                                         (31)

In particular this derivation is unavailable in representative 29, where Q10 actually owns (3,1.74). That representative is not included in this chapter's conclusion.

## 5. Completion of representatives 2, 28, 43, and 103

Theorem 1 applies to the actual upper central square Q6. Its two top anchors and marker are literal owned points in the table above. Its five exclusions are supplied respectively by

| Theorem 1 exclusion | Actual strict source |
|---|---|
| (2,2.4) | Q7, between (27) and (28) |
| (2,3) | Q11, by (30) |
| (3,2.4) | Original auxiliary 19 in Q10 |
| (3,3) | Actual paired corner Q3 |
| (3,2.56) | Q10, by (31) |

Consequently Q6 strictly owns X=(2,2.65). If its canonical angle is positive, its half-angle exceeds 7/18.

If Q7 has a nonnegative canonical angle, translate by (−2,−2) and apply Theorem 2. Its four owned data are (27), (29), (28), and its actual marker. Its isolated exclusion is the globally absent southwest marker. Its whole wall segment is (26). Its other whole excluded segment is

    [(2,1.74),(2.26,2)],

strictly owned by the one actual square Q5 because Q5 owns auxiliary points 4 and 16 in every row of the table. Thus Q7 also strictly owns X, contradicting its disjointness from Q6. Therefore Q7 has a strictly negative canonical representative; an axial or diagonal positive representative has already been excluded.

Now rotate the full actual configuration by

    (x,y)↦(4−y,x),

and write C=Q7, B=Q6. Their strict and excluded points match Theorem 3 exactly:

| Working-coordinate datum | Actual original point |
|---|---|
| C: O=(2,2) | Q7(2,2) |
| C: D=(2,1.5) | Q7(1.5,2) |
| C: E=(1.5,2) | Q7(2,2.5) |
| C: M_C=(1.65,1.65) | Q7(1.65,2.35) |
| C excludes G=(2.35,1.65) | Globally absent (1.65,1.65) |
| B: M_B=(1.65,2.35) | Q6(2.35,2.35) |
| B: H₁=(1,2.26), H₂=(1,2.4) | Q6(2.26,3),(2.4,3) |
| B excludes P=(1.5,3) | Q10(3,2.5), by (31) |
| B excludes K=(1,3) | Q3(3,3) |

If B has positive canonical angle, Theorem 1 gives its half-angle >7/18, whereas Theorem 3 excludes that range. A quarter-turn preserves the signed canonical angle, so these two angle statements concern the same physical orientation.

It remains that B has negative canonical angle. Apply the retained complete negative/negative two-square theorem reproduced in `C981-RETAINED-CONTINUOUS-LEMMAS.md`. Its C data are O,D,M_C and the same missing G above. Its B data are M_B,H₂ and the three exclusions

    (1.6,3), (1,3), (.914,2).

Under the stated rotation these three points are the genuine original points (3,2.4) in Q10, (3,3) in Q3, and (2,3.086) in Q11. The retained theorem covers every negative/negative relative angle order and every weak support tangency. It yields a contradiction.

Every orientation choice for both actual central squares has now been excluded. This completes all four original representatives. ∎

### Scope of Sections 1–5

The seven exclusions in `C981-WALL-CYCLES.md` and the four proved so far cover eleven of the seventeen target representatives:

    2,24,26,28,39,43,59,71,103,105,108.

The six representatives not yet concluded at this stage are

    29,30,37,69,104,107.

Their missing implications are concrete. Representative 29 lacks the right-wall reach used in Theorem 1. Representatives 30,37,69 do not supply the whole Q5 segment required in Theorem 2. Representatives 104,107 do not have the ordinary-wall center entrance used in (27), because their top-wall ownership is different. No center, segment, or wall point from the four completed rows is imported into those six alternatives.

## 6. A slightly lower shared point removes the diagonal-segment premise

**Corollary 4.** Under every hypothesis of Theorem 1, Q strictly owns

    X₀=(2,2.62).                                         (32)

**Proof.** Retain the translated coordinates, face tables, and half-angle bounds in that proof. Now X₀=(0,−.08). In the positive sign its upper u- and lower v-bands follow from M with positive differences .35c−.27s and .35s+.27c. The other two bands follow from

    v(X₀)−V≤s+.22c≤1.22/√2<1<a,
    U+a−u(X₀)≤c+.38s<1<a.

The last inequality uses h>7/18>.38 and identity (6). In the negative sign the upper u-band follows from M with difference .35c+.27s>0. The other three bounds are

    U+a−u(X₀)≤c+.22s<1<a,
    v(X₀)−V≤.22c<1<a,
    V+a−v(X₀)≤s+.38c≤1.38/√2<1<a.

Here h>1/4>.22 suffices for the first. Thus all bands of X₀ are strict in both signs. ∎

**Theorem 5.** Let N have side a>1 and a nonnegative canonical frame u=cx+sy, v=−sx+cy, where 0≤s≤c and c²+s²=1. Suppose N strictly owns

    O=(0,0), E=(−.5,0), P=(0,.5), M=(−.35,.35),

and excludes the two points

    L=(−.35,−.35), R=(.35,.35),

and the entire segment

    S={−1}×[.26,.8].

Then N strictly owns X₀=(0,.62). No exclusion at (0,−.26), and no foreign diagonal segment, is required.

**Proof.** Write U,V for the lower faces. At R, both lower bands follow from O: its v-projection is .35(c−s)≥0. Its upper v-band follows from M, whose projection is larger by .7s≥0. Thus its exclusion forces

    U+a≤.35(c+s).                                        (33)

At L, both upper bands follow strictly from O. If it failed its lower u-band, then U≥−.35(c+s), and (33) would give a≤.7(c+s)≤.7√2<1. Consequently

    V≥.35s−.35c.                                        (34)

The target's two lower bands follow from the strict point P. Its upper v-band follows from (34), since

    v(X₀)−V≤.97c−.35s≤.97<1<a.

Assume its upper u-band fails, and put p=U+a. Then

    0<p≤.62s,                                           (35)

where p>0 follows from O. Hence s>0.

The two endpoints J=(−1,.26), K=(−1,.8) of S now force the same wall faces as in Theorem 2. For completeness, J's lower v-band follows from E, its upper u-band from P, and its upper v-band follows from

    v(J)−V≤.65s+.61c≤√.7946<1<a.

It must therefore satisfy U≥−c+.26s. At K, the lower v-band follows from E, and the upper u-band follows from P because c−.3s>0. A lower u-face exclusion would combine with (35) to give

    a≤c−.18s≤1,

which is impossible. Therefore

    U≥−c+.26s,  V+a≤s+.8c.                              (36)

Every interior intersection of N with x=−1 would now have .26<y<.8, contrary to the excluded whole segment S. Since O is strict and has x=0, convexity forces the entire closed square into x≥−1. Its exact left support gives

    cU−s(V+a)≥−1.

With H=c+s, (34)–(35) imply

    aH≤1+cp−sV≤1+.97cs−.35s².                           (37)

The opposite strict scalar inequality holds throughout the nonzero canonical sector:

    H−1+.35s²>.97cs.                                    (38)

Indeed put h=s/(1+c), so 0<h≤√2−1<1/2. Exact multiplication yields

    (1+h²)²[H−1+.35s²−.97cs]
      =2h[.03−.30h+1.97h²−h³].

Since h<1/2, the bracket is bounded below by the strictly positive quadratic

    .03−.30h+1.47h²
      =(147/100)(h−5/49)²+18/1225>0.

Equations (37)–(38) contradict a>1. The zero-sine case was already impossible under the assumed target failure (35). Thus X₀ is strict for every allowed angle and every allowed tangency. ∎

## 7. One common ending also closes representatives 30, 37, and 69

The three additional rows have the following exact auxiliary sets:

| Original representative | Q5 | Q6 | Q7 | Q10 | Q11 |
|---|---|---|---|---|---|
| 30 | {8,18} | {7,17} | {5,13} | {9,19} | {3,14} |
| 37 | {8,16,18} | {7,17} | {5,13} | {9,19} | {3,14} |
| 69 | {8,18} | {7,17} | {4,5,13} | {9,19} | {3,14} |

The original marker masks, common singleton consequences, Q8 auxiliary set {1,11}, Q9 auxiliary set {6,15}, and the empty auxiliary sets of Q3,Q4 are identical to those used in Section 4. In particular, the entire derivations (26)–(30) use unchanged actual data and apply without modification. They give the genuine Q7 center, both Q7 crosspoints, the genuine Q8 segment, and the genuine Q11 origin.

The right-wall reach (31) also holds in all three rows. Q10 owns its marker and (3,2.4), excludes (3,1.74) because auxiliary 8 belongs to Q5, and excludes (2.26,2) because auxiliary 16 is outside its exact set {9,19}. In representative 37 the latter point is strictly in Q5; in representatives 30 and 69 it is globally unowned. The wall-reach theorem requires only its exclusion from Q10, so both situations satisfy exactly the same premise. No strict owner for the globally unowned point is asserted.

Theorem 1 and Corollary 4 therefore give

    X₀=(2,2.62)∈Q6,

and a positive canonical Q6 half-angle >7/18, for all seven rows of this chapter.

If Q7 has a nonnegative canonical angle, translate it by (−2,−2) and apply Theorem 5. Its four strict data are its derived center and crosspoints together with its marker. Its two isolated exclusions are the globally absent southwest marker and the actual northeast marker in Q6. Its whole excluded segment is the actual Q8 segment (26). Hence X₀ also belongs strictly to Q7, a contradiction. This argument uses no Q5 auxiliary point and therefore applies uniformly to all seven rows, including representative 69 where Q7 itself owns (2,1.74).

Thus Q7 has strictly negative canonical angle. Rotate the actual configuration by (x,y)↦(4−y,x), exactly as in Section 5. If Q6 has positive canonical angle, Theorem 3 contradicts the half-angle bound from Theorem 1. If Q6 has negative canonical angle, the retained complete negative/negative theorem applies with exactly the same Q10 corner and Q11 marker exclusions listed in Section 5. An axial Q6 is already excluded by its two short chords. These alternatives exhaust all orientations and prove the three additional row exclusions. ∎

### Scope of Sections 1–7

At the stage of Sections 1–7, these results and `C981-WALL-CYCLES.md` continuously exclude fourteen of the seventeen target representatives:

    2,24,26,28,30,37,39,43,59,69,71,103,105,108.

The three representatives still outside these endings are

    29,104,107.

Representative 29 lacks the right-wall reach used to force the steep Q6 angle; representatives 104 and 107 have a different top-wall assignment and lack the ordinary-wall center entrance used here. These were the remaining actual geometric obligations at that stage. Section 8 below closes 107, and `C981-LAST-TWO-CYCLES.md` closes 29 and 104; none is inferred by extending an owner mapping beyond its exact hypotheses.

## 8. Transposition puts representative 107 in the same common family

The common proof in Section 7 does not use any particular auxiliary set for the southeast central owner. Its required actual data are those of the central square Q7, the upper square Q6, the left wall Q8, the right wall Q10, the left-anchored top wall Q11, the two genuine paired upper corners, and the retained lower-left singleton seed. Representative 107 supplies all of these data after one symmetry of the whole configuration.

Let τ(x,y)=(y,x), and label the transposed actual squares as follows:

| Transposed label | Original actual owner in row 107 |
|---|---|
| Q̃0 | Q1 |
| Q̃1 | Q0 |
| Q̃2 | Q4 |
| Q̃3 | Q3 |
| Q̃4 | Q2 |
| Q̃5 | Q7 |
| Q̃6 | Q6 |
| Q̃7 | Q5 |
| Q̃8 | Q9 |
| Q̃9 | Q8 |
| Q̃10 | Q11 |
| Q̃11 | Q10 |

Here Q̃i means τ applied to the indicated original square. Their exact transposed auxiliary sets are

| Owner | Exact transposed auxiliary set |
|---|---|
| Q̃0 | {2,12} |
| Q̃1 | {0,10} |
| Q̃2 | {18} |
| Q̃3 | ∅ |
| Q̃4 | ∅ |
| Q̃5 | {4,8,16} |
| Q̃6 | {7,17} |
| Q̃7 | {5,13} |
| Q̃8 | {1,11} |
| Q̃9 | {6,15} |
| Q̃10 | {9,19} |
| Q̃11 | {3,14} |

For example, original auxiliary points 4,16 in Q5 transpose to 13,5 in Q̃7; original points 9,19 in Q6 transpose to 17,7 in Q̃6; original points 7,17 in Q11 transpose to 19,9 in Q̃10; and original points 8,18 in Q10 transpose to 14,3 in Q̃11. The two extra transposed southeast assignments—auxiliary 18 in the corner Q̃2 and auxiliary 8 in Q̃5—change none of the common proof's premises.

The marker masks transpose to exactly the same common C981 marker pattern. In particular, the missing southwest marker remains missing. The original singleton seed (1.87,.76) in Q0 becomes (.76,1.87) in Q̃1, so Theorem 4 of `C981-WALL-CYCLES.md` gives the genuine Q̃8 segment {1}×[2.26,2.8]. The two paired upper corners Q̃3,Q̃4 strictly own (3,3),(1,3).

For clarity, the ordinary-center deduction in this application concerns original **Q5**, not original Q7. Apply the retained center theorem directly under reflection (x,y)↦(x,4−y). Its central square is original Q5, its right-wall square is original Q10, and its bottom-wall square is original Q9. The exact data are:

| Center-theorem input after this reflection | Actual original datum in row 107 |
|---|---|
| Central anchors (2,2.26),(2.26,2),(2.35,2.35) | Q5(2,1.74),(2.26,2),(2.35,1.65) |
| Right marker and anchor (3.086,2),(3,2.4) | Q10(3.086,2),(3,1.6) |
| Top marker and anchor (2,3.086),(2.4,3) | Q9(2,.914),(2.4,1) |
| Central excluded (2.35,1.65),(1.65,2.35) | Q6(2.35,2.35); globally missing (1.65,1.65) |
| Right excluded (3,1.74) | Q6(3,2.26) |
| Top excluded (1.74,3) | Q0(1.74,1) |

Both wall owners have the actual reflected outer container walls. Thus the theorem gives (2,2) strictly in original Q5, equivalently in Q̃7. The common crosspoint and corner arguments of Section 4 consequently apply to the transposed configuration exactly as stated; no center of original Q7 is asserted.

In particular, the right-wall advance for Q̃10 uses its genuine marker and top anchor, with the foreign points (3,1.74) and (2.26,2). In original coordinates these are (1.74,3) and (2,2.26), both strictly in original Q7. It gives (3,2.56) in Q̃10, equivalently (2.56,3) in original Q11. The top-origin argument for Q̃11 gives (2,3) in Q̃11, equivalently (3,2) in original Q10, using the actual paired corner Q2 and the actual bottom segment of Q9.

Every input to the Section 7 proof is now supplied by an identified actual owner. Corollary 4 and Theorem 5 either duplicate the strict point (2,2.62) in Q̃6,Q̃7, or force their two signs into the already excluded support alternatives. Therefore representative 107 is impossible. The reflection changes angle signs together with all the points and walls; the proof covers both signs in the transposed coordinates, so no orientation is lost. ∎

### Combined current C981 scope

This chapter, `C981-WALL-CYCLES.md`, and `C981-LAST-TWO-CYCLES.md` give independently audited continuous exclusions of all seventeen target representatives:

    2,24,26,28,29,30,37,39,43,59,69,71,103,104,105,107,108.

The last chapter supplies the two additional endings for **29 and 104**, using the actual right-wall square and both central-angle signs. Representative 104 has auxiliary 14 owned by its actual Q11; after transposition the new right-wall square therefore owns auxiliary 8. The low right-wall exclusion used in this chapter is unavailable, exactly as in representative 29. The new ending retains that ownership distinction and does not infer a point by similarity with row 107.
