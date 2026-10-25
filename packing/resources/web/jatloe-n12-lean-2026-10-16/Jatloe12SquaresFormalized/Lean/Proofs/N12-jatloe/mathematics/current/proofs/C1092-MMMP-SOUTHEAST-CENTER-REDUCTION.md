# C1092 MMMP: the southeast inward square and the mixed bottom wall

All terminating decimals are exact rational numbers. Every square below is an actual open square. Owned points are strict; exclusions, container contacts, and separating supports may be equality. The common side is always a>1; the upper bound a≤1.001 is used only in Theorem 2 through the proved mixed-wall angle theorem.

The first theorem is a three-square consequence of the already proved half-angle crossing and downstream wall obstruction. The second supplies the complementary positive-angle argument for a wall spanning both directions. Their MMMP application is a direct ownership reduction, not yet the final exclusion of MMMP.

## 1. A negative inward square cannot miss the center between the two actual walls

**Theorem 1.** Let C,W,B be pairwise disjoint open squares of common side a>1. Give C the nonpositive canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1.

Suppose C strictly owns

    M=(.35,.35), P=(0,.26), Q=(.26,0),

and excludes N=(−.35,.35). Suppose W strictly owns

    S=(1.086,0), T=(1,.26),

has its closure in x≤2 and has center ordinate at least zero. Suppose B strictly owns

    S_B=(0,1.086), A=(.4,1),

and has its closure in y≤2. Then C strictly owns O=(0,0).

No center condition on B or wall condition on C is assumed. In particular B need not exclude any point on the backward side of its wall origin.

**Proof.** Suppose O is absent from C. Its two u-bands follow strictly from P,Q, and its upper v-band follows from M. Thus, writing U,V for the lower faces,

    0≤V<.26s.                                          (1)

Consequently s>0. The point A is genuinely excluded from C because it is strict in the different actual B.

First R=(1,.4) must also be excluded from C. If it were strict in C, Theorem 1 of `INWARD-EXTENDED-ANCHOR-CENTER.md` would apply to the same actual C,W, with exactly the strict M,P,Q,R, excluded A, wall and center hypotheses displayed here. It would give the forbidden strict O.

The three other bands of R are strict: its lower u-band follows from Q because .74c−.4s>0; its lower v-band follows from Q; and its upper v-band follows from

    v(R)=s+.4c≤.7(c+s)≤.7sqrt(2)<1<a+V.

Hence R is upper u and

    U+a≤c−.4s.                                         (2)

For completeness, we derive the remaining face profile without any auxiliary-label premise. At A the lower v-band follows from M. A lower-u exit would combine with (2) to give a≤.6(c+s)<1. An upper-u exit would, by strict M, require s/c<1/13. But N has both upper bands strictly from M. If it were lower v, (1) would give s/c>35/61; if it were lower u, an upper-u A would give a≤.75c−.65s≤.75. Both are impossible. Thus A is upper v:

    V+a≤c+.4s.                                         (3)

Now a lower-v exit of N would combine with (3) to give

    a≤.65c+.75s≤sqrt(.985)<1.

Therefore N is lower u, and the complete profile is

    U≥−.35(c+s), V≥0,
    U+a≤c−.4s, V+a≤c+.4s.                            (4)

Put z=s/(1+c). By (1), (3), and a>1,

    c+.4s>1,
    c+.4s−1=2z(.4−z)/(1+z²),

so 0<z<.4.

Theorem 1 of `C1092-MMMP-FULL-INWARD-CENTER.md` now applies to the same actual C,W. Its precise inputs are the strict P,Q, V≥0, W's strict S,T, its genuine x≤2 wall and its nonnegative center ordinate. It gives

    U<−z and (z,1) strictly in C.                       (5)

Transpose the entire configuration by (X,Y)=(y,x). The same actual C now has positive frame (c,s),(−s,c), with lower faces L=V,H=U. It has L≥0,H≥−.35(c+s), owns the interchanged P,Q, and owns Z=(1,z) by (5).

It also strictly owns E=(.35,.65). Its lower longitudinal band follows from M, and its upper longitudinal band follows from L≥0 and

    .35c+.65s≤sqrt(.545)<1<a.

Its lower transverse band follows from H+a≤c−.4s, since

    (c−.4s)−(−.35s+.65c)=.35c−.05s<1<a.

Its upper transverse band follows from H≥−.35(c+s), since

    (−.35s+.65c)+.35(c+s)=c≤1<a.

Thus every hypothesis of Lemma 2 of `C1092-MMMP-FULL-INWARD-CENTER.md` holds, taking its actual right wall square to be the transposed B. Indeed B's strict S_B,A become (1.086,0),(1,.4), and its original y≤2 wall becomes X≤2. That lemma excludes the pair. Its full proof uses the two actual normal sources and the continuous scalar Lemmas P and L; it imposes no center sign or backward exclusion on B. We have reached a contradiction using the same three actual owners throughout. Therefore O is strict in C. ∎

## 2. A positive inward square cannot miss the center beside the wide wall

**Theorem 2.** Let C,W be disjoint open squares of common side 1<a≤1.001. Give C the nonnegative canonical frame

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1.

Suppose C strictly owns M,P,Q from Theorem 1 and excludes A=(.4,1). Suppose the actual W strictly owns S=(1.086,0) and the whole segment

    {1}×[−.4,.39],

excludes E_W=(1,.4), N_W=(.35,−.35), has its closure in x≤2, and has center ordinate at least zero. Then C strictly owns O=(0,0).

The absent E_W is an explicit premise. Strict ownership of the displayed bar alone cannot replace it.

### 2.1. Forced faces, the small-angle regime, and the actual wall angle

Suppose O is absent. Its upper u-band follows from M, and its two v-bands follow from P,Q. Writing e,V for C's lower faces gives

    0≤e<.26s, V<−.26s.                                (6)

In particular s>0. The point A has both lower bands strictly from M,Q. Its upper u-band follows from

    u(A)=.4c+s≤1.4/sqrt(2)<1<a+e.

Thus A is upper v and

    V+a≤c−.4s.                                         (7)

Put z=s/(1+c), so c+sz=1 and −s+cz=−z. If z≥.39, the point R=(1,.39) is strict in C: its lower u-band follows from Q; its upper u-band follows from c+.39s≤1<a+e; its upper v-band follows from P because s/c>.13; and its lower v-band follows from (7) and

    v(R)−V>1−.61c−.6s≥1−sqrt(.7321)>0.

This contradicts the actual strict W bar. Hence z<.39.

If s+.4c≥.6, the point Z=(1,z) on that same strict bar has its lower u-band from Q, upper u-band from u(Z)=1<a+e, and upper v-band from P. Its lower v-band follows from (7) and the identity

    c−.4s+z−1=z(.6−s−.4c)≤0.

Thus it too would be strict in C. We are left with

    s+.4c<.6, s<21/100, c>97/100.                      (8)

For the second bound, the function s+.4sqrt(1−s²) increases on the canonical interval. At s=.21 its cosine exceeds .975, so its value exceeds .6. The third bound follows from the second.

Reflect the hypotheses about W across the x-axis and apply Theorem 1 of `MIXED-WALL-HALFANGLE-CROSSING.md`. Its three strict anchors become S,(1,−.39),(1,.4), its excluded points become (1,−.4),(.35,.35), and its center ordinate becomes nonpositive. The theorem therefore gives W, in our present chart, the strictly positive frame

    w=(b,t), w_perp=(−t,b),
    b>t>0, b²+t²=1, h=b+t>5/4.

In particular

    t>9/32>7/25.                                      (9)

Let L,H be W's lower faces and put

    alpha=bc+ts, delta=tc−bs.

Equations (8),(9) give alpha>0 and delta>0. Strict ownership of (1,−.4) and the genuine wall/center inequalities give

    L<b−.4t,
    H+a≥−2t+a(1+th)/2>J,
    J=−2t+(1+th)/2.                                 (10)

Indeed center_x(W)≤2−ah/2 and center_y(W)≥0, and H+a=−t center_x(W)+b center_y(W)+a/2.

Orient a separating normal from C to W. The strict pair Q,S has positive horizontal displacement and equal ordinates, so n_x>0. The complete list of actual square normals in that open half-plane is

    u, −v, w, −w_perp.                                (11)

We rule out each by its full-square support. No hull substitution is made.

### 2.2. C's longitudinal normal

By (10),

    lower_W(u)=alpha L−delta(H+a)
               <alpha(b−.4t)−delta J=c A_0+s B_0,

where the exact coefficients satisfy

    A_0=b(b−.4t)−tJ,
    1−A_0=t[1/2+.4b−t+(th)/2],
    B_0=t(b−.4t)+bJ
       =b/2+bt(h/2−1)−.4t².                         (12)

Since h>1, b≥t and t<1/sqrt(2)<5/7, the bracket in (12) is greater than

    1/2+.4b−t/2≥1/2−t/10>3/7.

Also h≤sqrt(2)<2 gives B_0≤1/2. Therefore

    lower_W(u)<1−(3/7)ct+s/2
               <1−57/5000,                          (13)

where

    (3/7)(97/100)(7/25)−(21/100)/2=57/5000.

But upper_C(u)=e+a>1. The direction u cannot separate.

### 2.3. C's transverse normal

The components of −v=(s,−c) in W's frame are −delta,−alpha. The actual wall and center sign consequently imply

    lower_W(−v)≤2s−a[sh+alpha+delta]/2.

By (6), upper_C(−v)=−V>.26s. The exact identity

    sh+alpha+delta=ch+2st≥c

shows that their support difference is strictly greater than

    c/2−1.74s
      >(97/100)/2−1.74(21/100)
      =299/2500>0.                                  (14)

The coefficient of a is positive, so replacing a by 1 in this estimate was in the direction favorable to separation. Thus −v cannot separate.

### 2.4. W's longitudinal normal

The components of w in C's frame are alpha,delta, both positive. Strict M gives V+a>.35(c−s)≥0. Hence

    upper_C(w)=alpha(e+a)+delta(V+a)>alpha.

Using (10), the support difference is greater than

    alpha−(b−.4t)=b(c−1)+t(s+.4)
                  >−.03+.4(.28)=41/500>0.            (15)

Here b≤1,c>.97 and t>.28. Thus w cannot separate.

### 2.5. W's transverse normal

The components of −w_perp=(t,−b) in C's frame are delta,−alpha. Equations (6),(10) give

    upper_C(−w_perp)>delta+.26s alpha,
    lower_W(−w_perp)=−(H+a)<2t−(1+th)/2.

Their difference is greater than the exact expression

    J_1−t(1−c)−bs(1−.26c)+.26ts²,
    J_1=(1+th)/2−t
       =[(1−t)²+bt]/2≥1/4.                          (16)

The last inequality uses b≥t. Moreover t(1−c)<.03 and bs(1−.26c)<.21·.75. Dropping the last nonnegative term in (16) therefore leaves the strict margin

    1/4−.03−.21·.75=1/16>0.                         (17)

Thus −w_perp cannot separate either. All four actual sources in (11) have been excluded, contradicting disjoint interiors. Missing O was impossible. This proves Theorem 2, including both canonical endpoints through the preceding face and bar reductions. ∎

## 3. Literal MMMP application and the remaining ordinary-bottom branch

**Corollary 3.** In the original MMMP sector, suppose Q5 owns F4=(2,1.74), G6=(2.26,2), and Q10 owns G8=(3,1.6). Then:

1. Q5 has a strictly positive canonical angle in the original chart.
2. Q5 excludes F6=(2.4,1).
3. Q9 strictly owns F6=(2.4,1), as well as its already proved G5=(2.26,1).

**Proof.** The completed northwest-center theorem gives (2,2) strictly in the different actual Q7. Thus Q5 excludes it. Apply the simultaneous quarter-turn chart

    (xi,eta)=(2−y,x−2).

The exact source ledger is

| Local datum | Original point or condition | Actual source |
|---|---|---|
| C's M,P,Q | Southeast marker, G6,F4 | Q5, by the stated hypotheses |
| Excluded N=(−.35,.35) | Northeast marker (2.35,2.35) | Original Q6 |
| W's S,T | Bottom marker (2,.914), G5 | Q9, with G5 from the direct wall-sign chord |
| W's x≤2 and nonnegative center ordinate | Original y≥0 and X9≥2 | Actual original MMMP Q9 |
| B's S_B,A | Right marker (3.086,2), G8 | Q10, by the stated hypothesis |
| B's y≤2 | Original x≤4 | Actual original Q10 |
| Theorem 2's N_W=(.35,−.35) | Southwest marker (1.65,1.65) | Original Q4 |
| Missing O | (2,2) | Strict in Q7 by the full-center theorem |

A quarter turn preserves canonical orientation sign modulo the square's quarter-turn symmetry. Therefore Theorem 1 excludes every nonpositive original angle of Q5, proving assertion 1.

If Q5 owned F6, it would own the local R=(1,.4). The actual C,W and excluded A in the table would then satisfy `INWARD-EXTENDED-ANCHOR-CENTER.md`, Theorem 1, with no angle restriction. That theorem would put O strictly in Q5, again impossible. This proves assertion 2.

Suppose Q9 did not own F6. Every member of Q9's original F-covering list contains at least one of F2,F4,F6. The actual Q5 owns F4, so Q9 must own F2=(1.6,1). Convexity with its directly proved strict wall-sign endpoint (2.39,1) gives

    [1.6,2.39]×{1} strictly in Q9.

In the displayed chart this is precisely the one actual W segment {1}×[−.4,.39]. Its missing F6 is the explicit excluded E_W=(1,.4), and the source table supplies the other exclusion, wall and center condition. Theorem 2 now gives O strictly in Q5 for its remaining positive angle, a contradiction. Hence F6 is strict in Q9, proving assertion 3. ∎

This reduction uses only a single compulsory original F-covering row. It does not infer that every auxiliary has an owner, and it does not need any exact combined-label enumeration. The surviving case has an actual ordinary bottom pair F6,G5. Its exclusion requires a further argument involving the remaining actual owners; no conclusion about that case is asserted here.
