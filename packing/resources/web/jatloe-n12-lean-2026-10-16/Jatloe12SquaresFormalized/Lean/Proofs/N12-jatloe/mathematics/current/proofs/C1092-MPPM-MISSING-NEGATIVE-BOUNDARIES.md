# C1092 MPPM: an ordinary missing-forward square separates the two neighboring boundary centers

Every terminating decimal is an exact rational number. Owned points are strict interior points. An excluded point or segment may touch a face. All squares mentioned in a local theorem have the same side a>1. No upper side bound is needed in this chapter.

The local coordinates in Sections 1–4 are the southwest coordinates centered at (2,2). A negative canonical frame is

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1.

Its lower faces are U,V and its upper faces are J=U+a,K=V+a.

## 1. The preceding boundary origin forces a steep negative angle

**Lemma 1.** Let C have the negative frame above. Suppose C strictly owns

    M=(−.35,−.35), P=(−1,−.26), L0=(−1,−.4), H=(−1,−.5),

and excludes

    C0=(−1,−1), D=(−1,0), T=(−.26,0),
    the whole segment [−.56,−.26]×{−1}.

Then s>0, and

    U≥−c,       J≤s−.56c,       K≤−.26s,             (1)

    7/18<q=s/(1+c)≤sqrt(2)−1.                        (2)

**Proof.** At C0 the lower-u band follows from H, and both upper bands follow from M and L0. The corresponding increments are .5s, .65(c−s), and .6c. Thus

    V≥−s−c.                                         (3)

At D the upper-u and lower-v bands follow strictly from P and L0. Its only possible exits are lower u and upper v. An upper-v exit combined with (3) would give a≤c≤1. Hence U≥−c.

Both lower bands of T are strict by P: their increments are .74c−.26s≥.48c and .74s+.26c. An upper-u exit would now give a≤.74c<1. Therefore K≤−.26s.

Write G=(−.26,−1). Its lower-u and upper-v bands follow from P, with increments .74(c+s) and .74(c−s). A lower-v exit would give a≤c from the cap at T. Consequently

    J≤u(G)=−.26c+s.                                 (4)

In particular 1<a≤.74c+s, which excludes s=0.

It remains to improve (4) using the whole excluded segment. Put F=(−.56,−1). Its lower-u and upper-v bands are strict by P, with increments .44c+.74s and .74c−.44s. Suppose J>u(F). Then F must be lower v. At G the lower-v band is strict, since its failure was already excluded by a≤c. Along [F,G] the lower-u and upper-v bands remain strict. The two remaining strict bands at a point (x,−1) are

    x<(J−s)/c,       x>(V+c)/s.

The first threshold lies in (−.56,−.26] and the second in [−.56,−.26). Since no point of the whole segment can belong to C, the second threshold must be at least the first. This yields

    cV−sJ≥−1.                                       (5)

But J≥a−c and V≤−.26s−a imply

    cV−sJ≤.74cs−a(c+s)<.74cs−(c+s)<−1.              (6)

The last inequality follows from cs>0 and

    c+s−1=2cs/(1+c+s)≥.8cs.

This contradicts (5), including equality of the two segment thresholds. Hence J≤s−.56c, proving (1).

Finally,

    1<a=J−U≤.44c+s,

and the exact half-angle identity is

    .44c+s−1=(1−q)(36q−14)/(25(1+q²)).              (7)

On the canonical interval q≤sqrt(2)−1<1, its strict positivity is exactly q>7/18. This proves (2). ∎

Let θ be the ordinary angle with c=cos θ and s=sin θ. Set θ0=2 arctan(7/18). At this endpoint,

    c0=275/373, s0=252/373, c0+s0=527/373.

Throughout the interval supplied by Lemma 1 we shall use the elementary rational bounds

    .7<c<.738,       .675<s<.71,
    .45<s²≤.5,      c²<.55,       cs>.49,
    c+s>1.41,       0≤c−s<.062.                    (8)

They follow directly by monotonicity on θ0<θ≤π/4 and the displayed endpoint values. In particular s/c>252/275>.826.

## 2. A square-width inequality

For any unit normal n and any square orientation e,f, define its unit-side width

    w(n)=|n·e|+|n·f|,

and let k=w((1,0))=w((0,1)). For n=(−c,s),

    w(n)≥1,        k+w(n)≥1+c+s.                   (9)

To see the second inequality, vary the square angle over one period of length π/2. Between consecutive zeros of the four trigonometric factors inside the absolute values, the sum k+w(n) has second derivative equal to its negative and is positive. It is therefore concave on each such closed interval, and its minimum occurs at an endpoint. At any endpoint either k=1 and w(n)=c+s, or w(n)=1 and k=c+s. This proves (9), including all coincident breakpoints.

Since 0≤c,s≤1, (9) also gives

    s k+w(n)≥1+s(c+s),
    c k+w(n)≥1+c(c+s).                             (10)

These inequalities allow the neighboring square to have any orientation.

## 3. The bottom boundary must have center x>−.2

**Theorem 2.** Suppose C has the strict points M,P and the frame range (2) and faces (1) of Lemma 1. Let B be an actual square of the same side a>1, with interior disjoint from C, strictly owning

    B0=(0,−1.086), F2=(−.4,−1),

and with closure contained in y≥−2. Then the x-coordinate of the center of B is strictly greater than −.2.

**Proof.** Suppose instead that xB≤−.2. A separating normal directed from B to C must satisfy, by their strict points P,B0 and M,F2,

    −nx+.826ny>0,       .05nx+.65ny>0.

Consequently ny>0 and nx<.826ny. The only signed face normal of C in this cone is −u=(−c,s): its other upward normal v=(s,c) has s/c>.826. An actual face normal of B in the cone is either northwest, n=(−h,t), or northeast, n=(h,t), with h,t≥0, h²+t²=1. In the northeast case h/t<.826. This is the complete list furnished by the separating-axis theorem for the two actual squares, also when their closures touch.

### 3.1. Northeast normals of B

Let n=(h,t) lie in the stated cone. Set λ=ch−st<0 and μ=sh+ct>0. From J≥a−c and V≤−.26s−a,

    lower_C(n)=λJ+μV
       ≤λ(a−c)+μ(−.26s−a).

Since λ−μ<0 and a>1, subtracting n·F2 yields a quantity strictly less than

    h[c−s−.6+.74s²]+t[1+.74cs−(c+s)].              (11)

The first bracket is less than .062−.6+.37<0. The second is negative because c+s−1≥.8cs. Thus lower_C(n)<n·F2<upper_B(n), excluding every such normal.

### 3.2. The normal −u of C

Let k and w be the unit-side vertical width of B and its width in direction −u. Its bottom wall and the supposed center bound give

    upper_B(−u)≥.2c−2s+(a/2)(s k+w).

On the other hand lower_C(−u)=−J≤c−a. By (10) their support difference is strictly greater than

    Fb(θ)=1.5−.8c−2s+.5s(c+s).                     (12)

The exact derivative is

    Fb′=.8s−2c+cs+.5(c²−s²)<−.282,

where (8) gives the displayed uniform bound. Hence its minimum is at θ=π/4, where

    Fb(π/4)=2−(7/5)sqrt(2)>0.

The normal −u cannot separate.

### 3.3. Northwest normals of B

Write n=(−h,t)=(−cos φ,sin φ), 0≤φ≤π/2, and put

    κ=ch+st>0,       σ=ct−sh=sin(φ−θ).

Because n is an actual face normal of B, its vertical unit-side width is h+t and its width in n is 1. Thus

    upper_B(n)≥.2h−2t+(a/2)(1+t²+ht).              (13)

If φ≥θ, then σ≥0 and

    lower_C(n)=−κJ+σV
       ≤−κ(a−c)+σ(−.26s−a).

Subtract this from (13). Its coefficient of a is positive, so the support difference is strictly greater than

    F(φ)=.5+.5t²+.5ht+A h+B t,                     (14)
    A=c−s−.8+.74s²,
    B=c+s−2−.74cs.

At φ=θ, direct substitution gives F(θ)=Fb(θ)>0. At φ=π/2,

    F(π/2)=c+s−1−.74cs>0.

We verify positivity throughout the interval, not merely at these endpoints. On θ≤φ≤π/4, the coefficient A is at most its value at θ0: its θ-derivative is −c−s+1.48cs<0, and

    A(θ0)=−1393281/3478225<−.4.

Also B>−.96. Consequently

    F′=ht+.5(h²−t²)−At+Bh
       >.49+.4(.675)−.96(.738)=161/3125>0.          (15)

On π/4≤φ≤π/2, the exact identity is

    F″+F=(3/2)h(h−t)≤0.                            (16)

A twice differentiable function with f″+f≤0 on an interval of length less than π and positive endpoint values is positive throughout. For completeness, if it first reached zero at α, then f′(α)≤0; the variation-of-constants formula

    f(x)=f′(α)sin(x−α)
            + integral_α^x sin(x−r)[f″(r)+f(r)] dr

would keep it nonpositive up to the right endpoint, a contradiction. Applying this fact to (16), with (15) and the positive value at π/2, proves F>0.

It remains to take φ≤θ, so σ≤0. The strict marker M gives K>−.35(c+s). Hence

    lower_C(n)=−κJ+σK
       ≤−κ(a−c)−.35(c+s)σ.

Again subtracting from (13) gives a support difference strictly greater than the expression (14), now with

    A=c−.8+.65s²−.35cs,
    B=−2+s+.35c²−.65cs.                            (17)

The bounds (8) give A>7/400>0 and B<−177/125<−7/5. Therefore

    F′=ht+.5(h²−t²)−At+Bh
       <h(t+h/2−7/5)<0,                            (18)

since t+h/2≤sqrt(5)/2<7/5. Its minimum on [0,θ] is therefore F(θ)=Fb(θ)>0.

Every possible actual-square normal has now been excluded. This contradicts disjoint interiors, proving xB>−.2. All normal and relative-angle endpoints were retained; the strict inequalities arise from a>1 or the strict anchors. ∎

## 4. The left boundary must have center y>.2

**Theorem 3.** Suppose C has the same strict points, frame range and faces as in Theorem 2. Let L be an actual square of side a>1, disjoint from C, strictly owning

    R=(−1.086,0), D=(−1,0),

and with closure contained in x≥−2. Then the y-coordinate of its center is strictly greater than .2.

**Proof.** Suppose yL≤.2. A separating normal directed from C to L must satisfy

    ny>0,       nx<(175/368)ny,                     (19)

by comparing the strict pair P,D and the strict pair M,R. The only possible C face normal is again −u. Actual L normals can be northwest or northeast; in the northeast case h/t<175/368<s/c.

### 4.1. Northeast normals of L

Let n=(h,t), λ=ch−st<0, μ=sh+ct>0. Use U≤s−.56c−a and the strict bound K>−.35(c+s). The upper support of C satisfies

    upper_C(n)=λU+μK
       >λ(s−.56c−a)−.35(c+s)μ.

After subtracting n·D and replacing a by 1 in its positive coefficient −λ, the resulting lower bound is

    h[.44−c+.21s²+.65cs]
       +t[s−.65s²−.35+.21cs].                       (20)

Both brackets are positive by (8); respective lower bounds are

    .44−.738+.21(.45)+.65(.49)=.115,
    .675−.65(.5)−.35+.21(.49)=.1029.

Thus upper_C(n)>n·D>lower_L(n), excluding these normals.

### 4.2. The normal −u of C

With k,w the unit-side horizontal and −u widths of L, its real left wall and the supposed center bound give

    lower_L(−u)≤2c+.2s−(a/2)(c k+w).

Also upper_C(−u)=−U≥a−s+.56c. By (10), the support difference is strictly greater than

    Fl(θ)=1.5−1.44c−1.2s+.5c(c+s).                 (21)

Its derivative satisfies

    Fl′=1.44s−1.2c−cs+.5(c²−s²)<−.2576

by (8). Hence

    Fl(θ)≥Fl(π/4)=2−(33/25)sqrt(2)>0.              (22)

This excludes −u.

### 4.3. Northwest normals of L

Write n=(−h,t), φ,κ,σ as in Section 3.3. Since it is an actual L face normal,

    lower_L(n)≤2h+.2t−(a/2)(1+h²+ht).              (23)

When φ≥θ, the bounds on U,K imply

    upper_C(n)=−κU+σK
       ≥κ(a−s+.56c)−.35(c+s)σ.

Subtracting (23), and lowering a to 1 in its positive coefficient, gives a support difference strictly greater than

    G(φ)=.5+.5h²+.5ht+A h+B t,                     (24)
    A=c−1.44−.21s²−.65cs,
    B=s−.65s²−.55+.21cs.

Here A<−1.11 and B>−.1 by (8). Moreover, on φ≥θ>θ0,

    h+t/2≤c0+s0/2=401/373<1.08.

Indeed cos φ+(sin φ)/2 decreases on this entire interval. Consequently

    G′=−ht+.5(h²−t²)−At+Bh
       >t(1.11−h−t/2)+.5h²−.1h
       >.03t−1/200
       >61/4000>0.                                 (25)

The quadratic estimate used here is .5h²−.1h=.5(h−.1)²−1/200. Therefore G has its minimum at φ=θ, where G(θ)=Fl(θ)>0.

When φ≤θ, use U≤s−.56c−a and V≤−.26s−a instead. Their signs give

    upper_C(n)=−κU+σV
       ≥κ(a−s+.56c)+σ(−.26s−a).

The support difference is strictly greater than (24) with

    A=c+s−1.44−.30s²−cs,
    B=s−c−s²+.30cs−.2.                             (26)

Now A>−.7 and B<−.5 by (8). Hence

    G′<−ht+.5(h²−t²)+.7t−.5h
       =h(h/2−1/2)+t(.7−h−t/2)<0.                 (27)

For 0<φ≤θ we have h≥c≥1/sqrt(2)>.7, so the last sign follows directly; at φ=0 the strict B<−.5 gives G′<0 as well. The minimum on [0,θ] is again G(θ)=Fl(θ)>0.

This excludes the complete list (19) of actual-square normals. The supposed bound yL≤.2 is impossible, and Theorem 3 follows. ∎

## 5. Exact source map and the completed all-missing negative subbranch

Retain the original no-omission MPPM entrance and the all-four-ordinary branch of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md. Thus the actual central ordinary pairs are

    Q4:F0,G0; Q5:F6,G5; Q6:F9,G9; Q7:F3,G4.

Every owner has its original marker and the actual paired corners retain their inner corner points. The exact boundary pairs are

    Q8:F1,G1; Q9:F2,G2; Q10:F8,G8; Q11:F7,G7.

For the southwest local square C=Q4, translate by (−2,−2). The actual sources for Lemma 1 are as follows.

| Local datum | Actual original datum | Source |
|---|---|---|
| M,P,L0 strict in C | SW marker,F0,G0 in Q4 | Original marker and ordinary pair |
| T excluded from C | G3 outside Q4 | The missing-forward hypothesis |
| H strict in C | (1,1.5) in Q4 | ORDINARY-MARKER-HALFPOINT.md, exactly as mapped in Corollary 3 of the ordinary-central reduction |
| C0 excluded from C | (1,1) in Q0 | Actual paired-corner inner point |
| D excluded from C | (1,2) in Q8 | Origin supplied when the preceding Q7 omits its forward F5 |
| [−.56,−.26]×{−1} excluded from C | [1.44,1.74]×{1} in Q9 | The actual Q9 advance (1.44,1) and its owned G2; both strict in this one actual square |

The last advance follows from G5 in ordinary Q5 by Section 5 of C1092-MPPM-NONORDINARY-ISOLATION.md. The theorem needs only this shorter actual bar; no segment joining distinct owners is used. The own missing-forward hypothesis also gives the strict next origin (2,1) in Q9, by the complete actual-corner transfer in Corollary 3 of the ordinary-central reduction.

For Theorem 2, its actual B is Q9, with strict B0,F2 equal to the bottom marker and F2. Its real bottom wall is y≥0 before translation. Thus a negative Q4 under these hypotheses forces

    center(Q9)_x>1.8.                               (28)

For Theorem 3, its actual L is Q8, with strict R,D equal to the left marker and the preceding origin just recorded. Its real left wall is x≥0. Thus the same negative Q4 forces

    center(Q8)_y>2.2.                               (29)

Both statements use the same actual square C and retain all its faces. They do not replace a boundary square by an abstract list of excluded points.

**Corollary 4.** Suppose all four ordinary central owners omit their forward points. Then two consecutive central owners cannot both have nonpositive canonical angle. In particular, the entire all-four-nonpositive subbranch is impossible.

**Proof.** All four omissions give all four actual boundary origins by the mapped halfpoint/corner transfers. Lemma 1 rules out a zero canonical angle, so any hypothesized nonpositive owner has the strictly negative frame and conclusions of Sections 1–4.

Suppose first that Q4 and Q5 are both nonpositive. Applying Theorem 2 to Q4 gives (28). Apply the whole Theorem 3 source map to Q5 under the actual quarter-turn R(x,y)=(4−y,x), with local coordinates taken before that turn. Its actual preceding boundary L is Q9. Its local center coordinate yL is 2−center(Q9)_x, so Theorem 3 gives

    center(Q9)_x<1.8,

contradicting (28). Every other consecutive pair is the simultaneous quarter-turn of this exact argument. No center sign, auxiliary ownership or square is imported from a different assignment. ∎

The retained original component families and the common no-omission entrance have not been replaced here. This chapter closes the stated all-missing negative subbranch, and also excludes each consecutive nonpositive pair when all four origins are supplied. It does not yet exclude the all-missing patterns with separated negative angles, nor cases in which some forward points remain owned. Those require the remaining actual central-cycle argument.
