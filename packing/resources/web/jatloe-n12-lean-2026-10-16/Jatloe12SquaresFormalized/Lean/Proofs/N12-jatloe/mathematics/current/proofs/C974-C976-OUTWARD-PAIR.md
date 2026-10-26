# A continuous two-square obstruction closes the outward southeast pairs

All decimals are exact rationals. All owned points are strict interior points of the indicated actual open square. Excluded points and separating supports may be tangent. The two squares in the theorem have the same side a>1. There is no upper bound on a.

## 1. The local coupled-support theorem

**Theorem.** Let S and N be disjoint open squares of the same side a>1. Suppose S has a negative canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,

with lower faces U,V, and satisfies

    13/87<t=s/(1+c)<143/500,
    U+a≤c+s,  V≥−c+.8s.                                (1)

Suppose S strictly owns

    M_S=(.35,−.35), Y=(.525,.125).

Suppose N strictly owns

    M_N=(.35,.35), F=(0,.26), G=(.26,1),

and excludes

    L=(−.35,.35), P0=(0,1), P1=(1,1).

Then this configuration is impossible.

The two face bounds in (1) are genuine support hypotheses for S. Section 5 derives them, with the stated angle interval and strict points, from actual owners in C974 and C976.

## 2. The northeast square has a positive frame and two fixed faces

Because Y is strict in S, it is excluded from N. We first show that N has a positive canonical frame and, in that frame, lower faces U_N,V_N satisfying

    U_N≥−.35C+.35S,   V_N+a≤C,                          (2)

where C≥S≥0 and C²+S²=1. The letter S in (C,S) denotes a scalar normal component; the southeast square is identified by its full name where needed below.

First use a nonpositive canonical frame for N, u_N=(C,−S), v_N=(S,C). At P0 the upper u and upper v bands follow from G, while the lower v band follows from M_N. The differences are .26C>0, .26S≥0, and .65C−.35S≥.30C>0. Thus P0 is lower u.

At Y its lower u and upper v bands follow from M_N:

    u_N(Y)−u_N(M_N)=.175C+.225S>0,
    v_N(M_N)−v_N(Y)=−.175S+.225C≥.05C>0.

If Y were upper u, its opposite-face width against P0 would give

    a≤u_N(Y)−u_N(P0)=.525C+.875S≤1.4/sqrt(2)<1.

Therefore Y is lower v. At P1 both lower bands follow from M_N. Its upper v band is strict because the opposite lower face at Y gives

    v_N(P1)−v_N(Y)=.475S+.875C≤sqrt(.99125)<1<a.

Consequently P1 is upper u. Against the lower u face at P0 this gives a≤C≤1, a contradiction. This excludes the nonpositive sign, including its axis and diagonal endpoints.

Use the positive frame u_N=(C,S), v_N=(−S,C). At L its upper u and lower v bands follow from F, while its upper v band follows from G:

    u_N(F)−u_N(L)=.35C−.09S≥.26C>0,
    v_N(L)−v_N(F)=.35S+.09C>0,
    v_N(G)−v_N(L)=.65C−.61S≥.04C>0.

Hence L is lower u and supplies the first bound of (2).

At Y its lower u band follows from F and its upper v band follows from M_N. If it were upper u, the opposite width from L would satisfy

    a≤u_N(Y)−u_N(L)=.875C−.225S≤.875<1.

Thus Y is lower v. At P1 both lower bands follow from M_N; an upper v exclusion would give

    a≤v_N(P1)−v_N(Y)=.875C−.475S≤.875<1.

Therefore P1 is upper u. At P0 its upper u band follows from G and its lower v band from M_N. A lower u exclusion would give width C≤1 opposite P1. Therefore P0 is upper v, establishing the second bound in (2). Every step used weak exterior inequalities and strict anchor comparisons.

## 3. Only two of the four separating axes are possible

Orient any separating unit normal from the southeast square toward N. Its second component must be strictly positive: the strict markers M_S and M_N differ by (0,.7). Weak separation of the closed supports would place their strictly interior projections in strict order.

Moreover, F−Y=(−.525,.135) must have strictly positive projection on such a normal. Of the four possible square-edge axes, this excludes the southeast normal (s,c), since (1) implies

    s/c>1131/3700>3/10,
    (s,c)·(F−Y)=−.525s+.135c<−.0225c<0.

It also excludes the northeast normal (C,S), since

    (C,S)·(F−Y)=−.525C+.135S≤−.39C<0.

The only remaining possible directions are

    n1=(−S,C),   n2=(−c,s).                             (3)

This is exhaustive by the separating-axis theorem for two squares: an axis parallel to a face normal of one of the squares must weakly separate their closed projection intervals whenever their open interiors are disjoint. The strict markers fix the direction of that weak separation.

Put

    d=cC−sS,   k=cS+sC.

Here d>0 and k>0: the angle cap in (1) gives c>s, while C≥S≥0, and s>0.

## 4. Both remaining supports contradict the common side

### 4.1. The northeast transverse normal n1

In the southeast frame n1=−k u+d v. Hence its upper southeast support is

    upper_S(n1)=−kU+d(V+a)
               ≥a(k+d)−k(c+s)+d(−c+.8s),               (4)

by (1). Its lower northeast support is V_N≤C−a by (2). Separation along n1 would consequently imply

    a(1+k+d)≤k(c+s)+d(c−.8s)+C.                        (5)

At a=1, the left side minus the right side of (5) is

    1−A C−B S,
    A=2−c−s+.2cs,
    B=1−c+s−.2s².                                      (6)

Its positivity follows from a single continuous norm estimate. With t=s/(1+c), exact substitution of c=(1−t²)/(1+t²), s=2t/(1+t²) gives

    1−A²−B²
      =4t(20−66t+40t²−75t³)/(25(1+t²)²)>0.             (7)

For completeness, 0<t<143/500<3/10. The polynomial in parentheses decreases on [0,3/10], since its derivative is −66+80t−225t²≤−42<0. At t=3/10 its value is71/40>0. Thus (7) is strict. Cauchy–Schwarz and C²+S²=1 now give

    A C+B S≤sqrt(A²+B²)<1.

So (6) is positive already at a=1. The factor 1+k+d is positive, and a>1 makes the left side of (5) still larger. This contradicts (5).

### 4.2. The southeast longitudinal normal n2

Separation along n2 is equivalent to

    U≥upper_N(u),

where u=(c,−s) is the southeast longitudinal normal. Its components in the northeast frame are d and −k, so (2) gives

    upper_N(u)=d(U_N+a)−kV_N
      ≥a(d+k)+.35d(S−C)−kC.                            (8)

Combining this with U≤c+s−a from (1), separation would imply

    a(1+d+k)+.35d(S−C)−kC−c−s≤0.                      (9)

At a=1 the displayed expression is

    1−A0 c−B0 s,
    A0=1−C−S+.35C²+.65CS,
    B0=2−C+S−.65S²−.35CS.                              (10)

We have A0≤.35. Indeed, C+S−1=2CS/(C+S+1)≥.8CS, and therefore

    A0−.35=1−C−S−.35S²+.65CS
           ≤−.15CS−.35S²≤0.

Also

    A0+B0=1.35+(1−C)²+.3CS<1.35+.09+.15<1.6,

because C≥1/sqrt(2)>.7 and CS≤.5. Since c≥s≥0,

    A0 c+B0 s=A0(c−s)+(A0+B0)s
              ≤.35c+1.25s.

This last expression increases with the southeast angle throughout the canonical interval. At the larger half-angle t=3/10 it equals

    .35(91/109)+1.25(60/109)=2137/2180<1.               (11)

Thus the expression (10) is positive. Increasing a from1 only adds the positive term (a−1)(1+d+k), so (9) is impossible.

Both axes (3) have been excluded. The two actual squares therefore cannot have disjoint interiors. This proves the theorem. All orientation boundaries and support equalities have been included; no angular subdivision or numerical center enclosure is involved. ∎

## 5. Exact common application to C974 and C976

Suppose the southeast owner Q6 has its remaining outward label262400. The established outward sign theorem puts it in a strictly negative canonical frame. Apply Theorem 1 of `OUTWARD-BAR-AND-UPPER-SPAN.md` in coordinates (ξ,η)=(x−2,2−y). Its actual inputs are the strict southeast marker and F8; the excluded G6; the actual right marker in Q10; the paired southeast-corner points in Q2; and the entire bottom segment [2.26,2.8]×{1} strictly in Q9. The exact label supplies the exclusion of G6 even when no owner is assigned to that auxiliary.

That theorem gives the half-angle interval in (1), the strict point Y=(2.525,2.125), and the upper-u bound U+a≤c+s. On returning to translated original coordinates (x−2,y−2), its upper transverse cap becomes the lower southeast face bound V≥−c+.8s in (1). Its other strict anchor is exactly M_S=(.35,−.35).

The earlier top-only common-point contradiction already excludes Q7=131200 opposite this outward southeast square. Thus its northeast neighbor has one of the two exact labels

    131232 or196768.

Both strictly own F5=(2,2.26) and G7=(2.26,3), and their original northeast marker. These are F,G,M_N of the theorem after translation by (−2,−2). Its three genuine exclusions are:

| Local excluded point | Original source in C974 | Original source in C976 |
|---|---|---|
| L=(−.35,.35) | Globally absent northwest marker (1.65,2.35) | The same marker, strictly owned by distinct Q8 |
| P0=(0,1) | (2,3) strictly in actual Q11 | (2,3) strictly in actual Q11 |
| P1=(1,1) | (3,3) strictly in actual paired corner Q3 | The same actual paired-corner point |

The top origin in both columns is the completed actual Q4/Q11 transfer of `C974-C976-CONTINUOUS-REDUCTIONS.md`, Section 3.1. No stronger left-wall reach is substituted in C976. The two central squares share the physical side a>1 and have disjoint interiors in the original problem, exactly as the theorem requires.

The local coupled-support theorem now contradicts either outward pair. Consequently **the southeast label262400 is impossible throughout both C974 and C976**. The only remaining southeast label is327936, owning F8,G6,G8. Pairwise disjointness then also removes northeast196768, since that label owns the same G6. The residual central possibilities are exactly

    (Q6,Q7)=(327936,131200) or(327936,131232).

This eliminates both outward branches by one continuous two-square support argument. It does not yet claim the final contradiction for the two displayed mixed southeast branches.
