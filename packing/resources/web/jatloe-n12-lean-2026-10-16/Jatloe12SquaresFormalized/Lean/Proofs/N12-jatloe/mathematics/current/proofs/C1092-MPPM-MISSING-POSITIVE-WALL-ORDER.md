# C1092 MPPM: a missing-forward positive square strictly orders its actual walls

Every terminating decimal is an exact rational number. Owned points are strict interior points, while an excluded point may touch a face. The common side satisfies the original bound 1<a≤1.001. Local coordinates are the southwest coordinates translated by (−2,−2).

The positive canonical frame of the central square C is

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1.

Its lower faces are U,V and its upper faces are J=U+a,K=V+a. Write c=cos θ, s=sin θ and q=s/(1+c).

The result below does not assume that the preceding central square omits its forward point. In particular, it does not assume a preceding boundary origin. Its two origin alternatives are kept separate until their actual geometric arguments are complete.

## 1. Positive missing-forward faces without a preceding origin

**Lemma 1.** Suppose C strictly owns

    M=(−.35,−.35), P=(−1,−.26), Q=(−1,−.4), H=(−1,−.5),

and excludes

    C0=(−1,−1), C1=(−1.086,−1), W=(−1.086,0),
    T=(−.26,0), F=(−.56,−1), G=(−.26,−1).

Then

    U≥−c−s,     J≤−.26c,
    V≥.56s−c,   K≤1.086s,                         (1)

and

    13/87<q≤sqrt(2)−1,       a≤c+.526s.             (2)

Thus the axis is impossible. This lemma itself needs only a>1.

**Proof.** Both upper bands at C0 are strict by H. Both lower bands at T are strict by P and M: the increments are .74c+.26s and .35c−.09s≥.26c.

Suppose T exited through upper v, so K≤.26s. A lower-v exit at C0 would then give a≤c−.74s≤1. Thus C0 must be lower u, yielding U≥−c−s. At G, the lower-u and upper-v bands are strict by P, with increments .74(c−s) and .74(c+s). A lower-v exit would give a≤c, so G would have to be upper u. Its upper-u face, together with U≥−c−s, gives a≤.74c<1. This contradiction proves

    J≤−.26c.                                      (3)

At W the upper-u band is strict by M, and the lower-v band is strict by P; their increments are .736c−.35s>0 and .086s+.26c>0. Thus W is lower u or upper v. A lower-u exit would combine with (3) to give a≤.826c<1. Hence

    K≤1.086s.                                     (4)

We now rule out the lower-v alternative at C0 without assuming anything about D=(−1,0). That alternative would give

    1<a≤c+.086s.

In half-angle coordinates this requires 0<q<.086, since

    c+.086s−1=2q(.086−q)/(1+q²).

On that interval .826c+s<1, by the exact factor

    .826c+s−1=(1−q)(913q−87)/(500(1+q²))            (5)

and .086<87/913. At C1, the upper-u and upper-v bands are strict by P. Its lower-u band follows from (3):

    u(C1)−U≥a−.826c−s>0.

Consequently C1 must be lower v, so V≥1.086s−c. Together with (4) this would give a≤c≤1. Therefore C0 is lower u after all, and U≥−c−s.

The same two strict bands at G now force it to be lower v, because an upper-u exit would give a≤.74c. At F the upper-v band is strict by P, while the lower-u band follows from

    u(F)−U≥a−.30c−s>0,
    .30c+s≤1.30/sqrt(2)<1.

Its upper-u exit would give a≤.44c. Hence F is lower v and V≥.56s−c. This proves (1).

Finally the two face widths give

    1<a≤.74c+s,       a≤c+.526s.

The first has the factor (3) of C1092-MPPM-MISSING-POSITIVE-BOUNDARIES.md and therefore gives q>13/87. Equal projection increments at the diagonal retain the strict band of the owned anchor. ∎

We shall use the notation

    θ0=2 arctan(13/87),      θ1=2 arctan(3/16).

The first has c0=3700/3869,s0=1131/3869. Therefore the coarse bounds (4) in the preceding positive-boundary chapter remain available:

    c>.7, .29<s<.71, c+s>1.248,
    0≤c−s<.665, s/c>.305.                         (6)

At θ1 the exact values are

    c1=247/265, s1=96/265,
    s1/c1=96/247<sqrt(2)−1,
    (5/9)c1−s1=7/45.                              (7)

## 2. Owning the preceding origin forces a larger positive angle

**Theorem 2.** Suppose C satisfies Lemma 1 and also strictly owns D=(−1,0). Let L be an actual square of side a>1, with interior disjoint from C, strictly owning

    W=(−1.086,0), A0=(−1,.26),

with closure in x≥−2, and excluding

    Z=(−1.086,1).

Then

    q>3/16.                                       (8)

The excluded Z will be an actual marker of the upper paired corner. No center sign is used.

**Proof.** Suppose θ≤θ1. By Lemma 1, θ>θ0. A separating normal directed from C to L must have

    nx<0,       ny>0,                             (9)

using the strict pairs D,W and P,A0. In this quadrant the only signed C face normal is v=(−s,c). An actual L face normal in the same quadrant is specified explicitly in each canonical sign below. These are the complete actual-square separating-axis sources.

Use d=cos β,t=sin β with 0≤β≤π/4 for the absolute canonical angle of L. Write A,B for its lower faces and JL=A+a,KL=B+a for its upper faces.

### 2.1. L has the positive frame (d,t),(−t,d)

Because D belongs to the other actual square, L excludes D. At D its lower-u, upper-u and upper-v bands are strict by W,A0,W. Hence

    B≥t,       B<1.086t,                          (10)

the second inequality being strict ownership of W. In particular t>0. The only L normal in (9) is f=(−t,d).

At Z both lower bands are strict by W, so Z is upper u or upper v. We treat both possible exits, including their equality cases.

#### Z is upper v

Then KL≤d+1.086t, and (10) gives a≤d+.086t. Hence, with z=t/(1+d),

    0<z<.086,       d>.98,       t/d<.18.          (11)

Since s/c>.305, we have β<θ. Put

    λ=ct−sd<0,       μ=st+cd>0.

First consider the C normal v. The actual left wall gives

    JL≥[−2+tB+a(d+t)]/d.

Also B≤d+1.086t−a. In the lower support

    lower_L(v)=λ JL+μ B,

eliminating JL leaves coefficient c/d>0 on B. The coefficient of a after both substitutions is λ(d+t)/d−c/d<0. Replacing a by 1 therefore gives the strict bound

    lower_L(v)−s
      <−s(d+t−1)+(ct/d)(d+t−1+.086−z).             (12)

To see its sign, divide by the positive c(d+t−1). The result is at most

    −s/c+t/d+(t/d)(.086−z)/(d+t−1).

The identity d+t−1=2dt/(1+d+t)≥.8dt and (11) give

    t/d+(t/d)(.086−z)/(d+t−1)
       <.18+.086/[.8(.98)²]<.305.                 (13)

The exact last margin is

    .305−.18−.086/[.8(.98)²]=251/19208>0.

Thus lower_L(v)<s<K=upper_C(v); the C normal cannot separate.

For the L normal f, put δ=sd−ct>0 and κ=st+cd>0. The actual central faces and its strict D give

    upper_C(f)=δJ+κK>δ(a−c−s)+κs.

Since f·D=t, while lower_L(f)=B<1.086t, their support difference is strictly greater than

    δ(a−s)−.086t.

From (6),(11),

    δ=cd(s/c−t/d)>.7(.98)(.305−.18)=.08575.

Moreover 1−s>.29 and t<.18. Hence

    δ(a−s)−.086t>.08575(.29)−.086(.18)>0.           (14)

This excludes the other actual normal. The upper-v exit of Z is impossible.

#### Z is upper u

Now JL≤−1.086d+t. The actual wall, together with B≥t, gives

    −2≤d(JL−a)−t(B+a)
          ≤−1−.086d²+dt−a(d+t).

As a>1,

    1+dt−d−t>.086d²,
    ((d+t−1)/d)²>.172.                            (15)

Here 1+dt−d−t=(d+t−1)²/2. If r=t/d≤5/9, the increasing function 1+r−sqrt(1+r²) would give

    (d+t−1)/d≤(14−sqrt(106))/9<371/900.

But

    .172−(371/900)²=1679/810000>0.

The strict radical bound used here follows from sqrt(106)>1029/100. This contradicts (15), proving

    t/d>5/9.                                      (16)

In particular β>θ under the supposed θ≤θ1. Put λ=ct−sd>0 and μ=st+cd>0. For the C normal v, the actual L faces give

    lower_L(v)=λA+μB
       <λ(−1.086d+t−a)+μ(1.086t)
        =1.086s+λ(t−a).                           (17)

By (7),(16),

    λ=d[c(t/d)−s]>d[(5/9)c−s]
       ≥(7/45)d>49/450,

and 1−t>.29. Thus

    λ(1−t)>.29(49/450)=1421/45000
                      >.086(96/265)≥.086s.        (18)

The exact middle margin is 1009/2385000. Equations (17)–(18) imply lower_L(v)<s<K, excluding v.

For the L normal f=(−t,d), its coefficient on central u is −λ<0. The upper-u cap of C and its strict D therefore give

    upper_C(f)>λ(a+.26c)+μs.

Since lower_L(f)<1.086t, the support difference is strictly greater than

    (1−.74c)(ct−sd)−.086t.                         (19)

The coefficient c(1−.74c)−.086 is positive for θ≤θ1. Dividing (19) by d and using (16), it exceeds

    (1−.74c)[(5/9)c−s]−43/900.                    (20)

This expression decreases on [0,θ1]. Indeed the derivative of its first term is

    .74s[(5/9)c−s]−(1−.74c)[(5/9)s+c]<0,

using s<.37,c>.93 and 1−.74c≥.26. Its exact value at θ1 is

    (4111/13250)(7/45)−43/900=193/397500>0.         (21)

Thus f also fails to separate. This excludes the upper-u exit and completes the positive canonical sign of L.

### 2.2. L has the negative frame (d,−t),(t,d)

At its excluded D the lower-u, lower-v and upper-v bands are strict by W,W,A0. Hence JL≤−d. If t=0, this upper face and the actual left wall give a≤1, an impossibility. Thus t>0.

At Z the upper-u and lower-v bands are strict by W. Its lower-u band follows from

    u_L(Z)−A≥a−.086d−t>0,

because .086d+t≤1.086/sqrt(2)<1. Consequently Z is upper v, and

    KL≤d−1.086t,
    B≤d−1.086t−a.                                (22)

The only L normal in (9) is n=(−d,t). Since θ+β<π/2, the central coefficients in this direction have signs −cos(θ+β)<0 and sin(θ+β)>0. From J≤−.26c and K>s,

    upper_C(n)>
        cos(θ+β)(a+.26c)+s sin(θ+β).

Strict ownership of W gives lower_L(n)=−JL<1.086d. Their support difference is therefore strictly greater than

    (1−.74c)cos(θ+β)−.086d
       ≥d[(1−.74c)(c−s)−.086]>0,                 (23)

where the last sign follows already from 1−.74c≥.26 and c−s≥151/265.

For the C normal v, put

    λ=−sd−ct<0,       μ=cd−st>0.

The actual left wall now gives

    JL≥a−2/d−(t/d)B.

Eliminating JL in lower_L(v)=λ JL+μB leaves coefficient c/d>0 on B. Use (22); the resulting coefficient of a is λ−c/d<0. Replacing a by 1 and writing z=t/(1+d), r=s/c gives the exact bound

    lower_L(v)−s
       <(ct/d)[.914−d−z+r d z].                   (24)

On 0<z≤sqrt(2)−1 and r≤96/247<sqrt(2)−1,

    d+z−r d z−1
      =z(1−z)[1−z−r(1+z)]/(1+z²)≥0,             (25)

because (1−z)/(1+z)≥sqrt(2)−1>r. Thus the bracket in (24) is at most −.086, proving lower_L(v)<s<K. This excludes the other actual normal.

Both L signs, both positive-sign exits of Z, both actual normal sources, all coordinate endpoints and all weak face equalities have been covered. The supposed θ≤θ1 is impossible, which proves (8). ∎

## 3. The positive boundary envelopes with the larger upper-v cap

Keep the definitions from the already proved positive-boundary chapter:

    b*(K)=[a(1.5+.5c(c+s))−K−2c]/s,
    ell*(K)=[K−2s+(a/2)(1+s(c+s))]/c.              (26)

**Lemma 3.** Suppose C satisfies (1), has 3/16≤q≤sqrt(2)−1, strictly owns M,P, and has 1<a≤1.001. Let B,L be actual squares disjoint from C, with the same side, satisfying

| Square | Strict points | Real wall |
|---|---|---|
| B | (0,−1.086), (−.4,−1) | Closure in y≥−2 |
| L | (−1.086,0), (−1,.26) | Closure in x≥−2 |

Then

    xB≥b*(K),       yL≥ell*(K).                    (27)

Again the same actual central face K occurs in both envelopes.

**Proof.** We give every change needed in the complete proof of Theorem 2, Sections 4–6, of C1092-MPPM-MISSING-POSITIVE-BOUNDARIES.md. The unchanged support identities and scalar intervals from that proof retain their original meaning.

The B→C normal cone is unchanged. For C→L, comparing P with A0=(−1,.26) still gives ny>0, and comparing M with W=(−1.086,0) still gives nx<(175/368)ny. Thus its complete normal list is unchanged. Its northeast comparison may use the actual strict W in place of D: n·W≤n·D for every northeast n, and the lower bound (12) of the preceding chapter for upper_C(n)−n·D is still positive. No ownership of D in L is needed.

For northeast normals of B the new upper face K≤1.086s changes (11) of that proof to

    h[−c+s+.14−.826s²]+t[1−c−s+.826cs]<0.           (28)

The first coefficient is smaller than the already proved negative one. The second is negative because

    c+s−1=2cs/(1+c+s)≥2cs/(1+sqrt(2))>.826cs.        (29)

The exact last comparison is the same one used in the unconditional negative wall-order chapter. The central normal v uses only the square-width inequalities and (26), so its proof is unchanged.

For northwest actual boundary normals write

    n=(−h,k)=(−cos φ,sin φ),
    φC=π/2−θ, δ=sk−ch, κ=sh+ck.

The exact central supports and actual-wall bounds are the ones in (14)–(15) of the preceding chapter. The coefficients of K in the two reduced gaps remain −cδ/s and −sδ/c. Thus the same signed substitutions remain valid. Only the two δ≥0 formulas change; the δ≤0 formulas gB− and gL− are literally unchanged.

For δ≥0, the new bottom gap is

    gB+=a EB+−δ(2/s+.826c),
    EB+=−h(1.5+.5c(c+s))/s
         +.5(1+k²+hk)+κ+δ.                        (30)

It is zero at φC, still satisfies gB+″+gB+=(3a/2)h(h−k)≤0 on [φC,π/2], and now has endpoint

    gB+(π/2)=a(1+c+s)−2−.826cs>0                  (31)

by (29). The proved sine-concavity argument therefore covers its whole interval, including the weak aligned endpoint.

For δ≤0, the coefficients AB−,BB− and the decreasing argument on [0,π/4] are unchanged. The coefficient of a in its endpoint value (25) of the preceding chapter is still nonpositive. We now use the valid intrinsic bound a≤c+.526s from (2), which gives

    sqrt(2) gB−(π/4)≥F1(θ),
    F1(θ)=sqrt(2)(c+.526s)−1.526
              +.06c²+.203cs−.263s².               (32)

The exact second derivative is

    F1″=−sqrt(2)(c+.526s)−.646(c²−s²)−.812cs<0.

At θ1, replacing sqrt(2) by the smaller 7/5 gives the positive rational lower bound

    F1(θ1)>87339/662500>0,

while F1(π/4)=0. Concavity proves F1≥0 on [θ1,π/4]. The old decreasing and sine-concavity arguments now prove gB−≥0 on its complete interval [0,φC]. This is the only change needed in that interval.

For δ≥0, the new left gap is

    gL+=(a/2)(1+h²+hk)+AL+ h+BL+ k,
    AL+=−ac−1+cs+.086s²,
    BL+=a((c+s)/2−1/c)+s/c−s²−.086s³/c.           (33)

It is zero at φC. The old coefficient proof gave its unmodified B1>−.21. Since s³/c≤s²≤.5 and a≤1.001, the new coefficient obeys

    BL+>−.21−.001sqrt(2)−.043>−.26.

The derivative becomes

    gL+′=k[a(c−h−k/2)+1−cs−.086s²]
             +.5a h²+BL+ h.

On φ≥φC, h+k/2≤s+c/2, so c−h−k/2>−.36. Therefore

    gL+′>.09k+.5h²−.26h
          ≥.09k−.0338
          >.09(.7)−.0338=.0292>0.                (34)

The coefficient .09 is justified by

    −1.001(.36)+.5−.043=.09664>.09.

Thus gL+≥0 throughout its interval.

Finally gL−, both of its coefficient bounds, its two derivative/concavity arguments and its strictly positive coordinate endpoint are unchanged. Their hypotheses hold because q≥3/16>13/87. This covers the whole δ≤0 interval.

The proof with xB<b*(K) or yL<ell*(K) then excludes every normal exactly as in the preceding chapter: the aligned gaps receive the strictly positive center-difference term, the h=0 bottom endpoint is positive by (31), and the k=0 left endpoint retains its proved positive value. Consequently (27) holds for arbitrary orientations of the actual B,L. ∎

**Corollary 4.** Under Lemma 3,

    xB+yL>0.                                      (35)

**Proof.** Add (26)–(27), use K≤1.086s in its nonpositive coefficient, and use a>1 in its positive coefficient. The exact resulting lower bound is

    xB+yL>
      s(c+s−1)/(c(1+c))−.086(c−s)/c
       =N(q)/(1−q²),                              (36)

    N(q)=−2q³+2.086q²+.172q−.086.

For 0≤q≤1/2,

    N′(q)=q(4.172−6q)+.172>0.

At the permitted lower endpoint,

    N(3/16)=1639/256000>0.

The denominator in (36) is positive. Thus the local sum is strictly positive, also at either diagonal representative. ∎

## 4. A preceding origin need not belong to L in the excluded-origin case

Suppose instead that D=(−1,0) is excluded from C. Lemma 1 of C1092-MPPM-MISSING-POSITIVE-BOUNDARIES.md now gives the stronger cap K≤s and all the original positive-boundary faces and angle bounds. Its two envelope conclusions remain valid when L strictly owns W,A0 instead of W,D.

Here is the complete source adjustment. The C→L cone ny>0 is now supplied by the strict pair P,A0. The second cone inequality is still supplied by M,W. For a northeast normal n=(h,k), the previous positive lower bound for upper_C(n)−n·D gives

    upper_C(n)>n·D≥n·W>lower_L(n).

All its other normal calculations use only the actual left wall, the actual square widths and those central faces; none uses ownership of D in L. Thus its entire proof, including the four northwest scalar intervals and their strict endpoints, applies unchanged. Corollary 3 of that chapter yields

    xB+yL>0.                                      (37)

This argument makes no assertion about whether D is owned by L or is absent from all owners. Its exclusion from C is the only origin hypothesis in this case.

## 5. The unconditional positive missing-forward order

**Theorem 5.** Let C satisfy Lemma 1. Let actual squares B,L of the same side have interiors disjoint from C and satisfy the hypotheses in the table of Lemma 3. Suppose L additionally excludes Z=(−1.086,1). Then

    xB+yL>0.                                      (38)

No preceding-origin assumption is required.

**Proof.** The physical point D=(−1,0) is either strict in C or is not. If it is not, Section 4 proves (38). If it is, actual disjointness excludes it from L. Theorem 2 then forces q>3/16, so Lemma 3 and Corollary 4 prove (38). These alternatives include all boundary positions of D. Every actual square and the same central face K are retained within each argument. ∎

## 6. Literal original OOOO application

Retain the original no-omission MPPM entrance and its all-four-ordinary branch. Suppose Q4 omits its forward G3 and has nonnegative canonical angle. Translate the physical configuration by (−2,−2). The local data have the following actual sources.

| Local datum | Literal actual source |
|---|---|
| M,P,Q in C=Q4 | Original SW marker,F0,G0, the actual ordinary pair |
| H in C | Strict (1,1.5) supplied by the proved missing-forward halfpoint theorem |
| C0,C1 excluded from C | Inner (1,1) and the original outer marker (.914,1), both strict in paired Q0 |
| W excluded from C, strict in L=Q8 | Actual left marker (.914,2) |
| T excluded from C | Its stated missing G3 |
| F,G excluded from C | Strict (1.44,1) and G2=(1.74,1) in actual Q9 |
| Strict B points | Actual Q9's bottom marker (2,.914) and F2=(1.6,1) |
| A0 strict in L | Actual Q8 owns F1=(1,2.26) |
| Z excluded from L | The original outer marker (.914,3), strict in actual paired Q3 |
| Real B,L walls | Original y≥0 and x≥0, respectively |

The Q9 advance is supplied by ordinary Q5's G5 through Section 5 of C1092-MPPM-NONORDINARY-ISOLATION.md. The halfpoint is Corollary 3 of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md. No point called missing is assigned to another owner here. In particular, no claim about Q7's forward F5 or the ownership of D=(1,2) occurs in this ledger.

Theorem 5 gives the strict original-coordinate inequality

    center(Q9)_x+center(Q8)_y>4.                    (39)

All simultaneous quarter-turns preserve this complete actual-owner map. Combining this theorem with C1092-MPPM-MISSING-NEGATIVE-WALL-ORDER.md therefore gives the same strict local wall-center order for every missing-forward ordinary sector, for all canonical signs, without a preceding-origin hypothesis.

The all-missing cycle was already completed by the earlier positive-boundary chapter. This stronger local theorem also applies inside mixed forward-ownership cycles. Such cycles still require their forward-owned sectors to be connected by a further actual-owner argument; no global closure of that remaining obligation is asserted here.
