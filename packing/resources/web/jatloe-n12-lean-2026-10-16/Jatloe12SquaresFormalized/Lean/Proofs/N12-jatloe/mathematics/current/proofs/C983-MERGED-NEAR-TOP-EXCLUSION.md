# C983: the merged western square cannot own the nearer top auxiliary

Every terminating decimal is an exact rational. Owned points are strictly interior to the actual open square. Excluded points, foreign segments, and separating supports may touch boundaries. The only side cap used below is the original 1<a≤1001/1000.

## 1. A two-square theorem with one genuine foreign segment

**Theorem 1.** No two disjoint open squares N and B of common side 1<a≤1001/1000 can satisfy all the following conditions:

    N strictly owns P=(−.35,−.35), Q=(0,.26), T=(−.26,1),
    N excludes E_N=(.35,.35);

    B strictly owns M=(.35,−.35), D=(.26,0), L=(0,−.26),
    B excludes R=(1,−.26) and the entire segment
    I=[E,F], E=(.26,−1), F=(.8,−1).

The foreign segment must be excluded as a whole. No container wall, center enclosure, or other owner is a premise of this local theorem.

## 2. The long merged square has one exact angle interval

A nonpositive canonical frame u=(C,−S), v=(S,C), C≥S≥0, is impossible for N. Its two strict anchors P,T have v-projection difference

    1.35C+.09S<a≤1001/1000.

As a positive concave function of the angle, the left side has its minimum at an endpoint. The endpoint values 1.35 and 1.44/sqrt(2) both exceed 1001/1000; the latter squared comparison is 1.0368>1.002001.

Therefore N has a strictly positive canonical frame

    u_N=(C,S), v_N=(−S,C), C>S>0, C²+S²=1.

Let U_N,V_N and A_N=U_N+a,B_N=V_N+a be its lower and upper faces, and put p=atan(S/C). At E_N both lower bands follow from P, and its upper v_N-band follows from T, with strict projection increments .7(C+S), .7(C−S), and .65C+.61S. Consequently

    A_N≤.35(C+S).

Strict ownership of T and P then gives

    .65S<.61C,
    1.35C−.09S<a≤1001/1000.

The second displayed expression decreases with p. At S/C=10/13 it equals 16.65/sqrt(269)>1001/1000, because

    16.65²−269(1001/1000)²=7.684231>0.

Thus throughout the proof

    10/13<S/C<61/65<1,
    D_N=C−S>1/25,
    V_N<−.35D_N,
    A_N>S−.26C>0.                                  (1)

For the middle bound, C≥1/sqrt(2)>7/10 and S/C<61/65 give D_N>14/325>1/25. These strict inequalities also exclude both canonical endpoint ambiguities for N.

Any separating unit normal n oriented from N toward B satisfies n_x>0 and n_y<0: apply strict separation to M−P=(.7,0) and L−Q=(0,−.52). The separating-axis theorem for two squares supplies a normal among their actual edge normals. Hence, for a nonnegative canonical B angle q, only −v_N and −v_B need consideration; for a nonpositive canonical B angle −q, only −v_N and u_B need consideration. We retain an axial direction even if it fails the strict cone, which only enlarges the alternatives being excluded.

We repeatedly use, for c≥s≥0 and c²+s²=1,

    K=c+s≥1+.8cs,
    c≥1/sqrt(2)>7/10,
    s≤1/sqrt(2)<5/7,
    s+.26c≤1.26/sqrt(2)<1.                          (2)

The first bound follows from K−1=2cs/(K+1) and K+1<5/2.

## 3. The two ways the actual segment supplies a support line

These elementary face facts will be used with the same actual B and I in every application.

### 3.1. Nonnegative B frame

Take u_B=(c,s), v_B=(−s,c), and let U,V,A=U+a,H=V+a be B's faces. At R its lower u-band follows from M and its upper v-band follows from L. Hence R exits upper u or lower v.

Suppose R is upper u and E is lower u with its lower v-band strict. Then

    A≤c−.26s, U≥.26c−s.

At F its upper v-band follows from M. A lower-u exit of F would imply a≤.2c+.74s≤sqrt(.5876)<1; an upper-u exit would imply a≤.54c<1. Therefore F exits lower v and has both u-bands strict.

On I the upper bands remain strict. Its endpoints exit the two different lower faces and have the opposite lower bands strict. Exclusion of the whole segment therefore forces the lowest vertex onto or above its line:

    sU+cV≥−1.                                      (3)

Indeed, if this lower vertex had ordinate below −1, the interval between the two lower-face crossings on I would be nonempty and strictly inside B. Equality in (3) is the permitted tangency.

### 3.2. Nonpositive B frame

Take instead u_B=(c,−s), v_B=(s,c), with the same face notation. At R both lower bands follow from M,L, so it exits upper u or upper v.

Suppose R is upper v and E is lower v with its upper u-band strict. At E the lower u-band and upper v-band follow from D,M. At F both these bands follow from M. A lower-v exit of F would give

    a≤v_B(R)−v_B(F)=.74c+.2s<1.

Thus F exits upper u and has its lower v-band strict. The entire segment now avoids the two face crossings only if B's lowest vertex satisfies

    −sA+cV≥−1.                                     (4)

This is the same elementary whole-segment argument, now for the upper-u and lower-v faces. It again includes tangency and derives a support from the actual segment, rather than assuming an additional wall.

## 4. Nonnegative B angle: its own normal cannot separate

Assume B has the frame of Section 3.1. If −v_B separated N from B, strict ownership of P in N would give

    H< v_B(P)=−.35(c−s)≤0.                          (5)

If R were lower v, then H≥a−s−.26c>0 by (2), a contradiction. Thus R is upper u. If E were lower v, then

    a=H−V<−.35(c−s)+.26s+c
      =.65c+.61s≤sqrt(.7946)<1,

also a contradiction. Its other two bands follow from D,M, so E is lower u with its lower v-band strict. Equation (3) applies.

Using (5), A≤c−.26s and a>1 in (3) gives

    aK<1+1.35cs−.26s²−.35c².                       (6)

But by (2) the difference between K and the right side is at least

    .35c²+.26s²−.55cs
      =.26(c−s)²+.09c²−.03cs
      ≥.26(c−s)²+.06c²>0.

This contradicts (6). Thus B's own normal never separates in this entire sign.

## 5. Nonnegative B angle: the N-normal cannot separate

### 5.1. The order 0≤q≤p

Put k=cos(p−q)>0 and h=sin(p−q)≥0. The lower B-support in direction −v_N is

    hU−kH.

A separator would require

    hU−kH>.35D_N,                                  (7)

because V_N<−.35D_N. Strict ownership of L gives U<−.26s≤0. Therefore the lower-v alternative at R, which would give H>0 as above, is impossible. Hence A≤c−.26s.

If E were lower v, then V≥−.26s−c. Combine this with (7), U<−.26s and a>1. The resulting necessary inequality is

    k(c−1)+.26s(k−h)−.35D_N>0.                     (8)

It has a uniform negative upper bound. Since k−h=D_N c+(C+S)s, its left side equals

    D_N(.26cs−.35)
      +s²[.26(C+S)−k/(1+c)].

Here cs≤1/2, C+S≤sqrt(2), and k≥C≥1/sqrt(2), so this is at most

    −.22D_N+.005sqrt(2)
      <−.22/25+.0075=−13/10000<0.

This contradicts (8). E is consequently lower u with its lower v-band strict, and (3) follows.

Combining (3), (7) and U≤c−.26s−a now gives

    a(S+ck)<k+S(c−.26s)−.35cD_N.                   (9)

The difference between the left coefficient S+ck and the right side of (9) is

    D_N c(c−.65)
      +S[(1−c)²+s(c−.74)]>0.                      (10)

The first term is positive. The bracket is nonnegative when c≥.74. When c<.74, its first term exceeds .26²=.0676 and its second term exceeds −.04·.75=−.03, so it is positive as well. Since a>1, (10) contradicts (9).

### 5.2. The order p≤q≤π/4

In this order sin(p−q)≤0. The lower support is

    sin(p−q)A−cos(p−q)H.

Because A>u_B(D)=.26c>0, positive separation from −V_N>.35D_N forces H<0. Thus R is upper u. E cannot exit lower v, because that would give

    a<c+.26s≤78/[5sqrt(269)]<1.

For this bound, q≥p>atan(10/13), the expression c+.26s decreases in q on this interval, and 78²<25·269. Hence E is lower u and (3) applies.

Using H<0 and A≤c−.26s in (3) gives

    aK<1+cs−.26s².

But K−1≥.8cs and s/c>10/13 give

    K−[1+cs−.26s²]≥s(.26s−.2c)>0.

This is the final contradiction for nonnegative B angles. The equality q=p is covered by both displayed arguments without a division by sin(p−q).

## 6. Nonpositive B angle: the N-normal cannot separate

Now give B the frame of Section 3.2, and set

    h=sin(p+q)>0, k=cos(p+q)>0.

The positivity of k follows from p<π/4 and q≤π/4. A separator −v_N would require

    hU−kH>.35D_N.                                  (11)

### 6.1. R exits upper u

Here A≤c+.26s. Strict ownership of D gives H>.26s, so the difference between the lower B-support and .35D_N is strictly less than

    h(c−1)+.26s(h−k)−.35D_N.

The exact identity for this expression is

    S(1−c)(.52−.48c−s)
      +D_N[s(.74c+.26s−1)−.35].                   (12)

The second bracket is at most −.35, since .74c+.26s≤1. If the first bracket is positive, then c>7/10 implies that both s and the bracket .52−.48c−s are less than 23/125; also 1−c=s²/(1+c)≤s² and S≤1. If it is nonpositive, it needs no positive upper bound. Thus (12) is always strictly less than

    (23/125)³−.35/25<0.

This contradicts (11).

### 6.2. R exits upper v

Here H≤s−.26c. At s=0 this contradicts the strict point D, which requires H>0; thus s>0 in this subcase. At E the lower u and upper v bands follow from D,M. If E exited upper u, A≤.26c+s and H>.26s would give

    hU−kH<.26S+h(s−1)<0.

The last sign follows from h≥S and s<.74. This contradicts (11). Therefore E exits lower v with its upper u-band strict, so (4) applies.

Use (11) to bound U below in (4). Since ch−sk=S>0, and H≤s−.26c, this yields

    ahK<h+S(s−.26c)−.35sD_N.                      (13)

The difference between hK and the right side is

    S[.26c+(1−c)(1−2s)]
      +D_N s(K−.65)>0.                            (14)

The second term is nonnegative. The first bracket is positive for s≤1/2. For s≥1/2, (2) gives the exact lower bound

    .26c−(1−c)(2s−1)
      >.182−(3/10)(3/7)>0.

Thus (14) contradicts (13) and a>1. Both possible exits of R have been exhausted, so −v_N cannot separate in this sign either.

## 7. Nonpositive B angle: its own normal cannot separate

The only remaining direction is u_B. Its N-support satisfies, by (1),

    upper_N(u_B)=kA_N−hV_N
      >k(S−.26C)+.35hD_N>0.                       (15)

Thus a separator requires U>0.

If R exits upper v, then E cannot exit upper u: that exit would give

    U≤.26c+s−a<1.26/sqrt(2)−1<0.

Equation (4) therefore applies. But H≤s−.26c and U>0 give

    −sA+cV<cs−.26c²−K<−1,

because

    K−1−cs+.26c²≥c(.26c−.2s)≥.06c²>0.

This contradicts (4).

Finally suppose R exits upper u, so U≤c+.26s−a. If s/c≥3/5, the decreasing expression c+.26s is at most

    289/[50sqrt(34)]<1,

because 289²<2500·34. This gives U<0, again impossible.

For s/c≤3/5 put τ=S/C and z=s/c. Subtract .26s from the lower bound in (15). After division by the positive cC², the resulting exact expression is

    1.35τ−.35τ²−.26
      +z(.09−.09τ−1.26τ²).                        (16)

For 10/13≤τ≤61/65 the coefficient of z is negative. Therefore (16) is at least

    f(τ)=1.296τ−1.106τ²−.206.

This quadratic is concave and positive at both endpoints:

    f(10/13)=11533/84500,
    f(61/65)=19108/528125.

It is positive throughout their entire interval. Hence (15) gives upper_N(u_B)>.26s, whereas strict ownership of L in B gives U<u_B(L)=.26s. This contradicts separation.

Every actual normal in both B signs has now been excluded. All whole-segment supports were proved from the same actual I, with weak tangencies retained. The axial and diagonal B endpoints were included throughout. This completes Theorem 1. ∎

## 8. Exact C983 application and ownership consequence

The already proved chapters `C983-MERGED-TOP-EXCLUSION.md` and `C983-MERGED-RIGHT-EXCLUSION.md` reduce the actual merged western Q7 to

    8192,8208,8224,8240,24608.

Suppose Q7 owns G4=(1.74,3). Its exact label must then be 24608, so it also owns F5=(2,2.26) and G3=(1.74,2).

The original top labels avoiding G4 and F5 all own F7=(2.4,3) and G7=(2.26,3). Consequently northeast Q6 excludes F5,F7,G7. Each of its original labels avoiding those points owns F9=(3,2.26). The original right-wall labels avoiding F9 are exactly262400 and327936, both owning F8=(3,1.74) and G8=(3,1.6). Southeast Q5 therefore excludes F8,G8 as well as F5 in Q7 and F9 in Q6. The only original Q5 label with these absences is

    65552={F4=(2,1.74), G6=(2.26,2)}.

These are short subset deductions in the given original local families, not a selection of one twelve-owner vector or an assumption that all auxiliaries are owned.

Actual Q9 owns (2,.914), F6=(2.4,1) and G5=(2.26,1) under every original bottom label. Actual singleton Q0 strictly owns (1.74,1),(1.87,.76). Apply the transposed wall advance, Theorem 4 of `C981-WALL-CYCLES.md`, using those two genuine foreign Q0 points and the original southeast marker in Q5. Its real bottom wall gives (2.8,1) strict in Q9. Convexity of this same actual Q9 therefore gives

    [2.26,2.8]×{1} strictly in Q9.

Apply Theorem 1 to N=Q7 and B=Q5 after translation by (−2,−2). The strict P,Q,T in N are its southwest marker, F5 and G4. Its excluded E_N is the northeast marker, strictly in actual Q6. The strict M,D,L in B are its southeast marker, G6 and F4. The excluded R is F8, strictly in actual Q10. The whole excluded I is precisely the strict segment just proved in the one actual Q9. The physical common side and disjoint interiors are the original ones. All local hypotheses are therefore satisfied, giving a contradiction.

Thus the entire merged G4 branch is excluded. The necessary original C983 merged-owner family is now exactly

    8192,8208,8224,8240.

These four remaining possibilities own G3 and may additionally own F4 and/or F5. The whole C983 family still requires their further continuous ending; Theorem 1 does not claim that remaining obligation is complete.
