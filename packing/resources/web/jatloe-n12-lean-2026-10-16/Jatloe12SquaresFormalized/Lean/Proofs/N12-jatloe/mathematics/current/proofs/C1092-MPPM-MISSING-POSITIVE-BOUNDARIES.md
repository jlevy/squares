# C1092 MPPM: positive boundary envelopes and the complete all-missing cycle

Every terminating decimal is an exact rational number. Owned points are strict interior points; excluded points may lie on faces. The common side satisfies the original bound

    1<a≤1.001.

All boundaries used below belong to actual squares, with their full supports and real container walls. Their orientations are unrestricted. In particular, neither neighboring boundary is replaced by an independently positioned list of excluded points.

The local coordinates are the southwest coordinates centered at (2,2). A positive canonical central frame is

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1.

Its lower faces are U,V and its upper faces are J=U+a,K=V+a. Write c=cos θ, s=sin θ, and L=c+s.

## 1. The positive missing-forward faces

**Lemma 1.** Suppose C strictly owns

    M=(−.35,−.35), P=(−1,−.26), Q=(−1,−.4), H=(−1,−.5),

and excludes

    C0=(−1,−1), D=(−1,0), T=(−.26,0),
    F=(−.56,−1), G=(−.26,−1).

Then

    U≥−c−s,      J≤−.26c,
    V≥.56s−c,    K≤s,                              (1)

and

    13/87<q=s/(1+c)≤sqrt(2)−1,     a≤c+.44s.        (2)

In particular the axis case s=0 is impossible.

**Proof.** At D, both lower bands are strict by P, and the upper-u band is strict by M. The respective increments are .26s, .26c and .65c−.35s≥.30c. Consequently D exits through upper v, giving K≤s.

At C0, both upper bands are strict by H, with increments .5s and .5c. A lower-v exit would combine with K≤s to give a≤c≤1. Hence C0 exits through lower u, and U≥−c−s.

Both lower bands at T are strict: its lower-u increment from P is .74c+.26s, and its lower-v increment from M is .35c−.09s≥.26c. Suppose T exited through upper v, so K≤.26s. At G the lower-u and upper-v bands are strict by P, with increments .74(c−s) and .74(c+s). A lower-v exit would then give a≤c. Thus G would have to exit through upper u, yielding J≤−.26c−s and therefore

    a=J−U≤.74c<1.

This is impossible. T must instead exit through upper u, proving J≤−.26c.

The same two strict bands at G now show that G cannot exit through upper u: that exit would again imply a≤.74c. Hence V≥.26s−c.

At F the upper-v band is strict by P. Its lower-u band follows from J≤−.26c:

    u(F)−U≥a−.30c−s>0,

because

    .30c+s=.65(c+s)−.35(c−s)≤1.30/sqrt(2)<1.

An upper-u exit at F would combine with U≥−c−s to give a≤.44c<1. Thus F exits through lower v, yielding V≥.56s−c. This completes (1).

The two face widths give

    1<a≤.74c+s,       a≤c+.44s.

The exact half-angle factor is

    .74c+s−1=(1−q)(87q−13)/(50(1+q²)).              (3)

Since 0≤q≤sqrt(2)−1<1, strict positivity in (3) gives (2). All face comparisons remain valid when their displayed increments vanish: the comparison point itself is strictly owned. ∎

Let θ0=2 arctan(13/87). Its exact sine and cosine are

    c0=3700/3869, s0=1131/3869, c0+s0=4831/3869.

For θ0<θ≤π/4, monotonicity and these endpoint values give

    c>.7,       .29<s<.71,      cs≤.5,
    c+s>1.248,  0≤c−s<.665,    s/c>.305.            (4)

These deliberately coarse rational inequalities will suffice below.

## 2. Two scalar tools

### 2.1. Widths of an arbitrarily oriented square

For any square orientation e,f and unit normal n, write

    w(n)=|n·e|+|n·f|,

and let k=w((1,0))=w((0,1)). With n=v=(−s,c),

    w(v)≥1,       k+w(v)≥1+c+s.                    (5)

This is the square-width inequality proved in Section 2 of C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md, with c and s interchanged. Its proof allows every orientation, coincident breakpoints and zero coefficients. It also yields

    c k+w(v)≥1+c(c+s),
    s k+w(v)≥1+s(c+s).                             (6)

### 2.2. Sine concavity, including zero endpoint values

We shall use the following elementary continuous fact. If f is twice continuously differentiable on [α,β], β−α<π, and

    f″+f≤0,       f(α)≥0,       f(β)≥0,

then f≥0 throughout the interval. A degenerate interval requires no argument. For a nondegenerate interval, the exact boundary-value identity is

    f(x)=f(α)sin(β−x)/sin(β−α)
         +f(β)sin(x−α)/sin(β−α)
         − integral_α^β G(x,r)[f″(r)+f(r)] dr,

    G(x,r)=sin(min(x,r)−α)sin(β−max(x,r))/sin(β−α).

Every factor in G is nonnegative. The identity follows by differentiating on either side of r=x, or directly from variation of constants. It proves the claim with weak endpoint values, exactly as needed when one of our support gaps is zero at an aligned normal.

## 3. Boundary-center envelopes sharing the same central face

Define

    b*(K)=[a(1.5+.5c(c+s))−K−2c]/s,
    ell*(K)=[K−2s+(a/2)(1+s(c+s))]/c.              (7)

Their denominators are positive by Lemma 1.

**Theorem 2.** Let C satisfy Lemma 1. Let B and L be actual squares of the same side a, with interiors disjoint from C, satisfying the following literal hypotheses:

| Actual square | Strict points | Real wall |
|---|---|---|
| B | B0=(0,−1.086), F2=(−.4,−1) | Closure contained in y≥−2 |
| L | R=(−1.086,0), D=(−1,0) | Closure contained in x≥−2 |

If xB is the x-coordinate of the center of B and yL is the y-coordinate of the center of L, then

    xB≥b*(K),       yL≥ell*(K).                    (8)

The K in both inequalities is the upper-v face of this same actual C.

The proof occupies Sections 4–6. It retains all four signed face normals of both squares in each actual-square separation problem.

## 4. Complete normal lists and the aligned directions

A separating normal directed from B to C must satisfy, by the strict anchor pairs P,B0 and M,F2,

    −nx+.826ny>0,       .05nx+.65ny>0.

These imply

    ny>0,       nx<.826ny.                         (9)

A separating normal directed from C to L must satisfy, by P,D and M,R,

    ny>0,       nx<(175/368)ny.                    (10)

The only signed C face normal in either cone is v=(−s,c). The other upward normal u=(c,s) has nx/ny=c/s≥1, and the remaining signed normals point downward. The axis has already been excluded.

The separating-axis theorem for two squares therefore gives a complete list: v, or an actual boundary face normal pointing northeast or northwest. This remains valid when the closures touch. We prove that no normal on this list can separate if the corresponding strict reverse inequality xB<b*(K) or yL<ell*(K) holds.

### 4.1. Northeast boundary normals

Write n=(h,t), h,t≥0, h²+t²=1, in one of the cones (9)–(10). In particular t>0. Put

    λ=ch+st>0,       μ=ct−sh>0.

For B, the caps J≤−.26c and K≤s imply

    lower_C(n)≤λ(−.26c−a)+μ(s−a).

Subtract n·F2. Since a>1 and λ+μ>0, the result is strictly smaller than

    h[−c+s+.14−.74s²]+t[1−(c+s)+.74cs].            (11)

Both coefficients are negative. The second follows from

    c+s−1=2cs/(1+c+s)≥.8cs.

For the first, the θ-derivative of −c+s+.14−.74s² is

    c+s−1.48cs>0.

Its largest value on [0,π/4] is therefore .14−.37=−.23. Thus lower_C(n)<n·F2<upper_B(n), and this normal cannot separate B and C.

For L, the lower-face bounds U≥−c−s and V≥.56s−c imply

    upper_C(n)≥λ(a−c−s)+μ(a+.56s−c).

Subtract n·D. Again a>1 makes the result strictly larger than

    h[c−s+.44s²]+t[c+s−1−.44cs].                   (12)

Both coefficients are positive on the interval (2). Hence upper_C(n)>n·D>lower_L(n), excluding every northeast normal of L.

### 4.2. The central normal v

Let k,w be the unit-side vertical and v-widths of B. Its real bottom wall gives

    upper_B(v)≥−s xB−2c+(a/2)(c k+w).

If xB<b*(K), then (6) and (7) make the right side strictly greater than K−a=lower_C(v). This excludes v.

For L, let k,w be its unit-side horizontal and v-widths. Its real left wall gives

    lower_L(v)≤2s+c yL−(a/2)(s k+w).

If yL<ell*(K), (6) and (7) make this strictly less than K=upper_C(v). This excludes v in the second separation problem.

### 4.3. Northwest boundary normals and their exact support reductions

Write an actual boundary face normal as

    n=(−h,t)=(−cos φ,sin φ),       0≤φ≤π/2,

and set

    φC=π/2−θ,       δ=st−ch=sin(φ−φC),
    κ=sh+ct=cos(φ−φC)>0.                          (13)

Thus φC∈[π/4,π/2−θ0). The central normal v corresponds to φ=φC, h=s,t=c.

The actual central supports are exactly

    lower_C(n)=δJ+κ(K−a)−a max(δ,0),
    upper_C(n)=δJ+κK+a max(−δ,0).                   (14)

Because n is an actual face normal of the corresponding boundary square, its width in n is a and its horizontal and vertical unit-side widths are h+t. The real walls therefore give

    upper_B(n)≥−h xB−2t+(a/2)(1+t²+ht),
    lower_L(n)≤2h+t yL−(a/2)(1+h²+ht).             (15)

Substituting xB=b*(K) into the first bound and subtracting lower_C(n) gives a coefficient −cδ/s of K. Subtracting the second bound with yL=ell*(K) from upper_C(n) gives a coefficient −sδ/c of K. This determines which actual K bound is permissible in every case; the two envelopes never vary the face K independently.

Here are the resulting lower bounds for the respective support differences. In each row the face substitutions have the indicated sign, so every bound is weak and valid even at δ=0.

| Gap | Range | Permitted central face substitutions |
|---|---|---|
| gB+ | δ≥0 | J≤−.26c, K≤s |
| gB− | δ≤0 | J≥a−c−s, K≥a+.56s−c |
| gL+ | δ≥0 | J≥a−c−s, K≤s |
| gL− | δ≤0 | J≤−.26c, K≥a+.56s−c |

Their exact expressions are

    gB+=a EB+−δ(2/s+.74c),
    EB+=−h(1.5+.5c(c+s))/s
         +.5(1+t²+ht)+κ+δ;                        (16)

    gB−=(a/2)(1+t²+ht)+AB− h+BB− t,
    AB−=a((c+s)/2−1/s)+c/s−.44c²,
    BB−=−as−1+.44cs;                              (17)

    gL+=(a/2)(1+h²+ht)+AL+ h+BL+ t,
    AL+=−ac−1+cs,
    BL+=a((c+s)/2−1/c)+s/c−s²;                    (18)

    gL−=(a/2)(1+h²+ht)+AL− h+BL− t,
    AL−=a(c+s)−.30c²−cs−1.44,
    BL−=−a[(1+s(c+s))/(2c)+s+s²/c]
          +.30cs+s²+1.44s/c.                      (19)

Each of these four expressions is zero at φ=φC, exactly. Sections 5 and 6 prove that each is nonnegative throughout its full stated interval.

If xB<b*(K), its actual northwest support difference is at least gB±+h(b*(K)−xB). This is strictly positive whenever h>0. At h=0 the explicit endpoint in Section 5.1 is positive. If yL<ell*(K), the corresponding difference is at least gL±+t(ell*(K)−yL), strictly positive whenever t>0; at t=0 the endpoint in Section 6.2 is positive. Thus the weak scalar inequalities below suffice to exclude every actual normal, including the aligned and coordinate endpoints.

## 5. The two bottom-boundary scalar inequalities

### 5.1. The interval φC≤φ≤π/2

The expression gB+ in (16) has the form

    (a/2)(1+t²+ht)+A h+B t,

with A,B independent of φ. Consequently

    gB+″+gB+=(3a/2)h(h−t)≤0                       (20)

on this interval, since φC≥π/4. At its endpoints,

    gB+(φC)=0,
    gB+(π/2)=a(1+c+s)−2−.74cs
                >c+s−1−.74cs>0.                  (21)

The sine-concavity fact of Section 2.2 proves gB+≥0 throughout.

### 5.2. The interval 0≤φ≤φC

We first establish two coefficient bounds in (17):

    AB−>.03,       BB−<−1.1624.                   (22)

For the first, put A1=AB− at a=1. The exact half-angle identity is

    50(1+q²)²(A1−1/25)
       =1+40q²−50q³−49q⁴−50q⁵
       =1+q²(40−50q−49q²−50q³).                  (23)

For 0≤q≤1/2, the last bracket is at least −7/2, so the last line is at least 1−(7/2)q²≥1/8>0. Since q≤sqrt(2)−1<1/2 and s>.29,

    AB−> .04−.001/s > .04−1/290 > .03.

Also

    BB−≤−1−.56s<−1.1624,

which proves (22).

For 0≤φ≤π/4 we have h≥t and

    gB−′=a[ht+.5(h²−t²)]−AB− t+BB− h
          <h[a(t+h/2)−1.1624]<0,                  (24)

because t+h/2≤3/(2sqrt(2)) and a≤1.001.

It remains to check the value at π/4 and the short interval after it. The exact value there is

    sqrt(2) gB−(π/4)
       =a[sqrt(2)−1/s+(c−s)/2]
         +(c−s)[1/s−.44c].                        (25)

The coefficient of a is nonpositive. Indeed,

    sqrt(2)s+.5s(c−s)

has derivative sqrt(2)c+.5(c²−s²)−cs>0 on [0,π/4] and equals 1 at π/4. Using the intrinsic upper bound a≤c+.44s from Lemma 1, (25) therefore gives

    sqrt(2) gB−(π/4)≥F(θ),
    F(θ)=sqrt(2)(c+.44s)−1.44
           +.06c²+.16cs−.22s².                   (26)

Its exact second derivative is

    F″=−sqrt(2)(c+.44s)−.56(c²−s²)−.64cs<0.

Moreover

    F(0)=sqrt(2)−1.38>0,       F(π/4)=0.

Concavity gives F≥0 on the entire canonical interval. In particular gB−(π/4)≥0. Equation (24) now proves gB−≥0 on [0,π/4].

On [π/4,φC] we again have

    gB−″+gB−=(3a/2)h(h−t)≤0.

Its endpoint values are gB−(π/4)≥0 and gB−(φC)=0. Section 2.2 proves nonnegativity throughout this interval as well. If φC=π/4, this last interval is degenerate and (25) gives its endpoint directly. This completes both bottom-boundary scalar inequalities.

## 6. The two left-boundary scalar inequalities

### 6.1. The interval φC≤φ≤π/2

We first bound the coefficient BL+ in (18). At a=1, write

    B1=(c+s)/2−c/(1+s)−s².

Its exact derivatives are

    B1′=(c−s)/2+1/(1+s)−2cs,
    B1″=−(c+s)/2−c/(1+s)²−2(c²−s²)<0.             (27)

At the endpoints of the central interval,

    B1(θ0)=−75269266/374229025>−.21,
    B1(π/4)=.5−1/sqrt(2)>−.21.

Hence B1>−.21 throughout. Since a≤1.001 and c≥1/sqrt(2),

    BL+>−.21−.001sqrt(2)>−.22.                    (28)

Differentiate (18) with respect to φ:

    gL+′=a[−ht+.5(h²−t²)]+(ac+1−cs)t+BL+ h
          =t[a(c−h−t/2)+1−cs]+.5a h²+BL+ h.      (29)

The function h+t/2 decreases for φ≥φC≥π/4. Thus

    h+t/2≤s+c/2,       c−h−t/2≥c/2−s>−.36.

Using (4), (28), a≤1.001, and cs≤.5, (29) gives

    gL+′>.13t+.5h²−.22h
          ≥.13t−.0242
          >.13(.7)−.0242=.0668>0.                 (30)

Here t≥c>.7, and .5h²−.22h=.5(h−.22)²−.0242. Therefore gL+ increases from its exact value gL+(φC)=0, proving gL+≥0 throughout.

### 6.2. The interval 0≤φ≤φC

We first establish uniform coefficient bounds in (19):

    AL−>−.75,       BL−<−.46.                     (31)

The coefficient of a in AL− is positive, so AL− exceeds its value A1 at a=1. Its derivative admits the exact factorization

    A1′=cs[.6−2(c−s)/(1+c+s)]>0.                  (32)

The last sign follows from (4): 2(c−s)<1.33<.6(2.248). At the lower endpoint,

    A1(θ0)=−278903821/374229025>−.75.

This proves the first bound in (31).

The coefficient of a in BL− is negative, so BL− is at most its value B1 at a=1. In half-angle coordinates,

    B1+.46=−P(q)/[25(1−q²)(1+q²)²],
    P(q)=24q⁶−162q⁵+299q⁴−114q³+76q²−12q+1.       (33)

For 0≤q≤1/2,

    P(q)=(1−6q)²
           +q²(40−114q+299q²−162q³+24q⁴)
         ≥(1−6q)²+q²(40−114q+218q²+24q⁴)>0.       (34)

The final sign follows from

    40−114q+218q²
       =218(q−57/218)²+5471/218>0;

at q=0, P(0)=1. The denominator in (33) is positive on our interval. This proves the second bound in (31).

For π/4≤φ≤φC, differentiation and (31) give

    gL−′<−ht+.5(h²−t²)+.75t−.46h.

Here t≥h>0. Dividing by t and using h²/t≤h gives

    gL−′/t<.75−.5(h+t)−.46h/t
             <.75−.624−.1403=−.0143<0,            (35)

because h+t≥c+s>1.248 and h/t≥s/c>.305. Since gL−(φC)=0, we have gL−≥0 on [π/4,φC], and in particular gL−(π/4)≥0. This also holds when the interval is degenerate.

We now prove ordinary concavity of gL− on [0,π/4]. Put

    P0=−AL−/a,       Q0=−BL−/a.

The first inequality in (31) and a>1 give P0<.75. The already established value gL−(π/4)≥0 gives

    P0+Q0≤sqrt(2).

Consequently, for h≥t,

    P0 h+Q0 t≤.75(h−t)+sqrt(2)t
                   ≤h²−t²+2ht.                  (36)

For completeness, the last inequality is an elementary one-angle inequality. Set D0=h−t, L0=h+t. Then D0∈[0,1], L0∈[1,sqrt(2)], D0²+L0²=2. The difference between its right and left sides is

    D0[L0−.75+1/sqrt(2)]
       −(sqrt(2)−L0)(L0+1/sqrt(2)).

Using sqrt(2)−L0=D0²/(sqrt(2)+L0) and

    (L0+1/sqrt(2))/(sqrt(2)+L0)≤3/4,

this difference is at least

    D0[L0−.75+1/sqrt(2)−.75D0]
       ≥D0[1/sqrt(2)−1/2]≥0.

This proves (36), including D0=0.

The exact second derivative now satisfies

    gL−″=a(t²−h²−2ht)−AL− h−BL− t≤0.              (37)

At the remaining endpoint,

    gL−(0)=a(1+c+s)−.30c²−cs−1.44
             >c+s−.44−.30c²−cs
             >1.248−.44−.30−.5=.008>0.            (38)

Concavity on [0,π/4], together with (38) and gL−(π/4)≥0, proves gL−≥0 there. Equations (35)–(38) cover its complete interval. This finishes the scalar proof for L.

Sections 4–6 have excluded every possible actual-square normal under xB<b*(K) or yL<ell*(K), with the strict endpoints explicitly supplied by (21) and (38). Thus Theorem 2 is proved. ∎

## 7. The strict local center sum

**Corollary 3.** Under Theorem 2,

    xB+yL>0.                                      (39)

**Proof.** Add the two envelopes (7)–(8). The coefficient of K is 1/c−1/s≤0. Therefore K≤s allows substitution of s for K as a lower bound. The coefficient of a in the resulting expression is positive, so a>1 gives a strict inequality, including the diagonal case c=s. Exact simplification gives

    xB+yL>
      [2c+s−2+s²−cs]/(sc)
       =s(c+s−1)/(c(1+c))>0.                      (40)

The identity used in the equality is

    2c+s−2+s²−cs=s²(c+s−1)/(1+c).

The last sign follows from s>0 and c+s>1. The two boundary squares have never been optimized against different central positions: both bounds used the one actual upper face K. ∎

## 8. Exact actual-owner map and the complete all-missing contradiction

Retain the original no-omission MPPM entrance and the all-four-ordinary branch of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md. The actual ordinary pairs are

    Q4:F0,G0; Q5:F6,G5; Q6:F9,G9; Q7:F3,G4,

and the actual boundary pairs are

    Q8:F1,G1; Q9:F2,G2; Q10:F8,G8; Q11:F7,G7.

The four paired corners retain their strict inner points. Suppose all four central forward points are omitted:

    G3 outside Q4,  F4 outside Q5,
    G6 outside Q6,  F5 outside Q7.                 (41)

The actual halfpoint/corner transfers in Corollary 3 of the ordinary-central reduction then give all four strict boundary origins.

For C=Q4, translate by (−2,−2). Its literal sources are the following.

| Local datum | Actual datum and owner | Established source |
|---|---|---|
| M,P,Q in C | SW marker,F0,G0 in Q4 | Original marker and ordinary pair |
| H in C | (1,1.5) in Q4 | ORDINARY-MARKER-HALFPOINT.md, with the exact map in the ordinary-central reduction |
| T excluded from C | G3 outside Q4 | Its own omission in (41) |
| C0 excluded from C | (1,1) strictly in Q0 | Actual paired-corner inner point |
| D excluded from C and strict in L | (1,2) strictly in Q8 | The preceding Q7 omission and its actual corner transfer |
| F,G excluded from C | (1.44,1),G2=(1.74,1) strictly in Q9 | Actual Q9 advance supplied by ordinary Q5's G5, and the owned boundary G2 |
| B0,F2 strict in B | Bottom marker,F2 strictly in Q9 | Original marker and actual ordinary boundary pair |
| R strict in L | Left marker strictly in Q8 | Original marker |
| Real B and L walls | Q9 closure in y≥0; Q8 closure in x≥0 | Original container |

The Q9 advance is Section 5 of C1092-MPPM-NONORDINARY-ISOLATION.md. Its segment to G2 lies strictly in that one actual Q9. This chapter needs its two endpoints for the positive case; the negative theorem uses the same whole segment. The upper side bound a≤1.001 is part of the original entrance.

The simultaneous actual quarter-turn

    R(x,y)=(4−y,x)

maps every row of this table to the next central owner and its two actual neighboring boundaries. It preserves the original MPPM entrance and the side bound. Thus each of the four central owners has the complete local data needed here or in C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md.

**Theorem 4.** The all-four-ordinary, all-four-missing subbranch (41) is impossible for every choice of the four canonical angle signs.

**Proof.** Number the central sectors cyclically as C_i=R^i(Q4), i=0,1,2,3. Let B_i=R^i(Q9) and L_i=R^i(Q8). Coordinates in sector i are obtained by applying R^(−i) about (2,2) and then translating (2,2) to the origin. Define

    z_i = the x-coordinate of center(B_i) in sector i.

Since the actual L_i is the same square as B_(i−1), the y-coordinate of its center in sector i is −z_(i−1); indices are taken modulo 4.

If C_i has nonnegative canonical angle, Lemma 1 first excludes the axis, and Corollary 3 gives

    z_i−z_(i−1)>0.

If C_i has nonpositive canonical angle, Lemma 1 and Theorems 2–3 of C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md apply to the same actual source table. They exclude the axis and give the respective local center bounds xB>−.2 and yL>.2. Their sum gives the identical inequality

    z_i−z_(i−1)>0.

The diagonal representations cause no ambiguity: either applicable canonical frame gives the stated strict inequality. Summing over the four sectors yields

    0 = sum_i [z_i−z_(i−1)] > 0,

a contradiction. This uses the same actual boundary center on each adjacent pair of sectors, and it includes all tangencies allowed by the weak face bounds. ∎

The retained original entrance and component rules are unchanged. This chapter completes the all-forward-missing alternative within the four-ordinary branch. The all-forward-owned alternative was already excluded by C1092-DIRECT-LAST-ASSIGNMENT.md. A mixture of owned and omitted forward points remains a separate actual-owner obligation until a transition theorem closes it.
