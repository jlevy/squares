# C976: the negative northeast/top pair completes the family

All terminating decimals are exact rationals. The local squares have the same side a>1, and owned points are strict. Excluded points and whole segments may touch a boundary. The proof uses the actual separating axes of the two squares, the genuine upper container wall, and one strict point in the actual left owner. It uses no orientation sampling or side upper bound.

## 1. A local theorem covering the complementary top orientations

**Theorem 1.** Let N and W be disjoint open squares of common side a>1. Suppose N has the strictly negative canonical frame

    u=(c,−s), v=(s,c), c≥s>0, c²+s²=1,

strictly owns M=(.35,−.65), G=(.26,0), and excludes T=(1,−.44). Suppose also that one of the following two alternatives holds.

* **Outer alternative:** N strictly owns X=(0,−.38) and excludes F=(0,−.74).
* **Mixed alternative:** N strictly owns F=(0,−.74) and excludes the complete segment I=[.26,.5]×{−1}.

Suppose W strictly owns O=(0,0), has its closure in y≤1, and excludes Z=(−.72,0). Choose its frame in the first quadrant,

    u_W=(C,S), v_W=(−S,C), C,S≥0, C²+S²=1.

Then S>0 and

    C/S<2/3.                                           (1)

Here a quadrant frame means any frame of the square with u_W in the closed first quadrant; it is not restricted to the canonical half-quadrant. In particular, the conclusion rules out every nonnegative canonical angle of W.

### The forced northeast faces

Write U,V for the lower faces of N and A=U+a, B=V+a for its upper faces. At O both upper bands follow from G, and its lower v band follows from M. Since O is strict in the disjoint W, it is excluded from N and consequently

    U≥0,
    U<min(.26c,.74s),
    V<.35s−.65c<0.                                    (2)

The second bound follows from G and the strict point of N on x=0; in the outer alternative its stronger bound U<.38s implies the one displayed.

In the outer alternative, F has both u bands and its upper v band strict, by X,M,G. The relevant upper-u difference is .35c−.09s≥.26c>0. Therefore F exits lower v. In the mixed alternative, apply the already completed Theorem 1 of `C974-C976-NEGATIVE-UPPER-ANGLE.md` to M,F,G,O,I. Its hypotheses are exactly the local data here; its whole-segment argument includes all tangencies. These two alternatives give respectively

    Outer: V≥−.74c;
    Mixed: V≥.5s−c and 0<s/c<13/25.                    (3)

In particular V≥−c in either alternative.

At T both lower bands follow from M, with differences .65c−.21s≥.44c>0 and .65s+.21c>0. If T exited upper v, (3) would give respectively

    a≤s+.30c≤1.30/sqrt(2)<1,
    a≤.5s+.56c≤sqrt(.5636)<1.

Both are impossible. Thus the common upper-u face is

    A≤c+.44s.                                         (4)

## 2. Only two actual separating normals remain

Suppose, contrary to (1), that the chosen quadrant frame satisfies C/S≥2/3, with S=0 included in this contrary alternative. Equivalently,

    C≥2/sqrt(13)>11/20, 0≤S≤3/sqrt(13)<5/6.            (5)

Let L,K be the lower faces of W and J=L+a its upper u_W face. Strict ownership of O gives

    L<0<J, K<0<K+a.

Set

    d=cC−sS, k=cS+sC>0.

Then d²+k²=1. A separating normal directed from N toward W has negative x component, because G and O are strict. It has positive y component, because N has a strict point on x=0 below O. The separating-axis theorem for the two actual squares therefore leaves only

    −u=(−c,s), or v_W=(−S,C).                          (6)

At S=0 the second vector lacks the required negative x component, so the first is the only genuine possibility; retaining the second in the estimates below does no harm. These are the actual square axes, not a separating direction inferred from a point-only approximation. Their weak support inequalities are

    −u normal:
       U≥dJ−kK                 if d≥0,
       U≥dL−kK                 if d<0;

    v_W normal:
       K≥−kU+dB                if d≥0,
       K≥−kU+dV                if d<0.                 (7)

Equality in (7) includes the allowed touching of the closed squares.

### The left point Z must exit lower u_W

The upper u_W band and lower v_W band of Z follow strictly from O. Its exclusion consequently has only the alternatives

    L≥−.72C, or K+a≤.72S.                             (8)

We rule out the second alternative. It implies K≤.75S−a, where replacing .72 by .75 only weakens the bound.

For the −u normal in (7), the d term is nonnegative in either sign: dJ≥0 for d≥0, and dL>0 for d<0. Hence

    U>k(1−.75S).

Put τ=s/c and τ*=13/37. After division by c, this contradicts (2). Here are the complete scalar details. The affine function

    F(τ)=(S+τC)(1−.75S)

has nonnegative constant term and positive slope. Also

    F(τ*)>(S+C/3)(1−.75S)≥1/3>.26.                    (9)

For the middle inequality use C+S−1≥.8CS and S≤5/6:

    3(S+C/3)(1−.75S)−1
      =(C+S−1)−.75CS+S(2−2.25S)
      ≥.05CS+S/8≥0.

The elementary bound C+S−1≥.8CS follows from

    C+S−1=2CS/(C+S+1), C+S≤sqrt(2)<3/2.

For 0≤τ≤τ*, the affine function F(τ)−.74τ is nonnegative at both endpoints, by (9) and .74τ*=.26. For τ≥τ*, F(τ)>.26. Thus in every case F(τ)≥min(.26,.74τ), contrary to U/c<min(.26,.74τ) and U/c>F(τ).

For the v_W normal, (2)–(3) show in both signs of d that

    K>−.26ck.

Indeed B=V+a≥a−c>0 when d≥0; when d<0, V<0 makes dV>0. Combining this bound with the hypothetical upper-v exit gives

    1<a<.75S+.26ck≤.75(5/6)+.26=.885<1,

another contradiction. Therefore Z must exit lower u_W, and (8) yields

    J≥a−.72C.                                         (10)

The genuine wall of W supplies the second common support bound:

    S J+C(K+a)≤1,
    K≤1/C−a(1+S/C)+.72S.                              (11)

All subsequent estimates use (10)–(11) with their weak equality cases intact.

## 3. The northeast-square separating axis is impossible

For the −u normal, combine (7) with the wall before using (10). Since d+kS/C=c/C, this gives, in both signs of d,

    U≥a(c/C+k−min(d,0))−.72c−k/C.

The upper face (4) gives U≤c+.44s−a. The coefficient of a in their combination is positive. Since a>1, the necessary scalar inequality is therefore

    f(τ,C)<0,                                         (12)

where τ=s/c, η=(1−S)/C=C/(1+S), and

    f(τ,C)=sqrt(1+τ²)+η+S−1.72
                  −τ(1.44−C)−min(C−τS,0).

We prove f>0 throughout (5), for every 0≤τ≤1.

If C≥4/5, put w=1.44−C≤.64. The inequality

    sqrt(1+τ²)−wτ≥sqrt(1−w²)>3/4

and η+S≥1 give f>.03. If 7/10≤C≤4/5, then w≤.74, so the same lower bound is greater than 2/3. Moreover

    η+S−1=C(1−C)/(1+S)≥(.7)(.2)/2=.07.

Thus f>2/3+.07−.72=1/60. Dropping −min(C−τS,0) in both estimates only weakens them.

It remains that 2/sqrt(13)≤C≤7/10. Now S>7/10 and τ0=C/S lies in (0,1). For τ≤τ0, the τ derivative of f is at most

    C−(1.44−C)≤−.04.

For τ≥τ0 it is at least

    2C+S−1.44>2(.55)+.7−1.44=.36.

Thus f is minimized at τ0, where

    f(τ0,C)=g(C)=(2−1.44C)/S+C/(1+S)−1.72.

This g increases on the required interval. Its derivative has the sign of

    2C−1.44+S²/(1+S).

For C≤3/5, use C>.55 and S≥4/5: this numerator is greater than

    −17/50+16/45=7/450>0.

For C≥3/5, use S>7/10: it is greater than

    −6/25+49/170=41/850>0.

At the remaining left endpoint its exact value is

    g(2/sqrt(13))=7sqrt(13)/6−209/50>0.                (13)

The last comparison is equivalent to 175sqrt(13)>627; squaring positive quantities gives the exact margin 175²·13−627²=4996>0. This proves f>0 and contradicts (12). Every value d=0 and every interval endpoint has been included.

## 4. The top-square separating axis is impossible

For S>0 define

    R=(1−η)/S=(1+η²)/(1+η).

The identity

    R−41/50=((η−41/100)²+119/10000)/(1+η)>0

implies, with Δ=1−η−.72S,

    Δ>.10S.                                           (14)

At S=0 one has η=1 and Δ=0; that case will also be checked below.

### The sign d≥0

Use the appropriate lower bound v0 in (3). From (7), (4), and (11),

    K≥a(k+d)−k(c+.44s)+d v0,
    K≤1/C−a(1+S/C)+.72S.

Their positive coefficient of a and a>1 give the necessary inequality

    k(1−c−.44s)+d(1+v0)+Δ<0.                         (15)

In the mixed alternative, write the left side as C A_m+S B_m+Δ, where

    A_m=c+s−c²−.44s²−.5cs,
    B_m=c−s−c²−.5s²+.56cs.

Here A_m>0, because c+s−1≥.8cs gives

    A_m≥.3cs+.56s²>0.

If S=0 the left side of (15) is A_m>0. For S>0, use C/S≥2/3 and (14). The angle bound in (3) implies c≥7/8 and s≤1/2. An exact rearrangement gives

    (2/3)A_m+B_m
      =s(17c/75−1/3)
         +s²(131/150−5/(3(1+c)))
      ≥−27/400−7/1800=−257/3600.

For clarity, the two coefficient bounds here are

    17c/75−1/3≥−27/200,
    131/150−5/(3(1+c))≥−7/450;

then use s≤1/2. It follows that the left side of (15), divided by S, is greater than

    1/10−257/3600=103/3600>0,                         (16)

which is impossible.

In the outer alternative, write the left side of (15) as C A_o+S B_o+Δ, where

    A_o=c+s−.74c²−.44s²−cs,
    B_o=c−s−c²+.30cs.

Again A_o>0, since

    A_o≥.26c²+.56s²−.2cs
        =.1(c−s)²+.16c²+.46s²>0.

At S=0 this already contradicts (15). Suppose S>0 and put ρ=C/S. Because d≥0,

    ρ≥max(2/3,τ), τ=s/c.

If τ≥2/3, then

    ρA_o+B_o+1/10
      ≥τA_o+B_o+1/10
      =sqrt(1+τ²)−1−.44τ+1/10.

The last expression increases for τ≥2/3 and has the strictly positive endpoint

    sqrt(13)/3−179/150>0.                             (17)

If 0≤τ≤2/3, the corresponding lower bound is

    (2/3)A_o+B_o+1/10
      =(5/3)c−s/3−209/150+(6/5)s²−(11/30)cs.

This expression decreases in the canonical angle throughout the interval. Its angular derivative, multiplied by 30/c, is

    −50τ−10+c(72τ−11+11τ²).

If the parenthesized expression is nonpositive, the derivative is negative immediately. Otherwise c≤1 bounds it above by

    11τ²+22τ−21≤−13/9<0.

It is therefore minimized at τ=2/3, where it has the same positive value (17). The strict comparison in (17) is exact: 50sqrt(13)>179 because 2500·13−179²=459>0. This proves that the left side of (15) is positive in the outer alternative too.

### The sign d<0

For the mixed alternative this sign is already impossible: (3) and (5) give τ<13/25<2/3≤C/S. In the outer alternative, (2) gives dV>0. Equations (7), (4), and (11) consequently imply the necessary inequality

    k(1−c−.44s)+Δ<0.                                 (18)

But d<0 implies τ>C/S≥2/3 and S>c. If 1−c−.44s≥0, (14) immediately contradicts (18). If it is negative, use 0<k≤1 and (14) to obtain

    k(1−c−.44s)+Δ>1−.9c−.44s.

The function .9c+.44s decreases for τ≥2/3, and at that endpoint it equals

    179/(50sqrt(13))<1,

by the same exact margin459. Hence (18) is impossible as well.

Both actual separating normals in (6) have now been ruled out. This proves Theorem 1. The sign d=0 was included in the first sign; the canonical diagonal endpoint c=s, the axial top angle S=0, and every weak support tangency were all retained. ∎

## 5. Exact C976 ownership and the completed contradiction

The retained local ownership reduction and the completed continuous exclusions leave only

    Q6=327936,
    Q7=131200 or131232.

The nonnegative canonical sign of each northeast alternative has already been excluded in Section 7 of `C976-MERGED-LEFT-ENDING.md`, using the actual left owner. Thus actual Q7 is strictly negative in both remaining pairs.

Apply Theorem 1 in coordinates (x−2,y−3), with N=Q7 and W=Q11. Every local datum has the following precise source.

| Local datum | Original datum | Exact source or actual owner |
|---|---|---|
| M=(.35,−.65) | Northeast marker (2.35,2.35) | Actual Q7 in both labels |
| G=(.26,0) | G7=(2.26,3) | Actual Q7 in both labels |
| Excluded T=(1,−.44) | (3,2.56) | Established strict right-wall point in actual Q10 |
| Outer X=(0,−.38) | (2,2.62) | Actual Q7=131200 by Theorem 1 and Corollary 2 of `TOP-ONLY-LEFT-POINT.md` |
| Outer excluded F=(0,−.74) | F5=(2,2.26) | Excluded by Q7's exact label131200; no separate owner is assumed |
| Mixed F=(0,−.74) | F5=(2,2.26) | Strict in actual Q7=131232 |
| Mixed whole I | [(2.26,2),(2.5,2)] | Both endpoints strict in the same actual Q6=327936, by its label and the completed southeast crosspoint theorem |
| O=(0,0) in W | (2,3) | Established strict top origin in actual Q11 |
| Excluded Z=(−.72,0) | (1.28,3) | Actual Q8 by Corollary 2, Section 5 of `C976-LEFT-UPPER-POINTS.md` |
| W's actual wall y≤1 | Original y≤4 | Original container wall for the closure of Q11 |

The entire segment I is strict in Q6 by convexity of that one open square. In the outer alternative the F5 exclusion is preserved exactly as an exclusion, without importing an owner. N and W are the actual distinct squares, so their separating axes in the proof are legitimate actual-square supports.

Finally combine Theorem 1 with the already completed Theorem 1 of `C976-LEFT-TOP-ANGLE.md`. The latter proves that if Q11 has a nonpositive canonical angle −β, then

    tan β>2/3.                                        (19)

If Q11 has a nonnegative canonical angle δ, choose its quadrant frame with C=cos δ, S=sin δ. Then C/S≥1, or S=0. This contradicts Theorem 1 directly.

If Q11 has a strictly negative canonical angle −β, choose its other quadrant axis, C=sin β and S=cos β. In this frame C/S=tan β. Equation (19) again contradicts Theorem 1, which requires C/S<2/3. The equality tan β=2/3 is excluded by both complete endpoint arguments, and the zero angle was included above.

Every orientation of actual Q11 is therefore impossible. Both last exact northeast labels have been eliminated, and **the full retained C976 family is excluded by continuous actual-square geometry**. This conclusion retains the existing finite local ownership entrance; it replaces the remaining geometric ending rather than asserting a new proof of that entrance. The extra northwest marker used to obtain Z belongs to Q8 in C976 and is absent in C974, so this final family conclusion is not transferred to C974.
