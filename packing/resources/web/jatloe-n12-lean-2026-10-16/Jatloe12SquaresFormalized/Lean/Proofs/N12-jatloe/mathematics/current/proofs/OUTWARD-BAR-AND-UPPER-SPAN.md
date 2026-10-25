# An outward bar and an upper span have a common strict point

All decimals are exact rationals. Squares are open and have side a>1. Excluded points and foreign segments may touch a boundary. These local theorems use no container or upper side bound.

## 1. The full bar gives a stronger outward point

**Theorem 1.** Suppose Q has a nonnegative canonical frame u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1. Suppose Q strictly owns

    N=(.35,.35), A=(1,.26),

excludes G=(.26,0), R=(1.086,0), P=(1,1), H=(1.086,1), and excludes the entire segment

    S=[.26,.8]×{1}.

Then, with U,V its lower faces and t=s/(1+c),

    U≥.26c,   V≥−1.086s,
    U+a≤c+s,  V+a≤c−.8s,
    13/87<t<143/500.                                   (1)

Moreover Q strictly owns

    X=(21/40,−1/8)=(.525,−.125).                       (2)

**Proof.** The isolated-point face reduction in Theorem 1 of `C974-C976-DUPLICATE-POINT.md` applies: both endpoints F=(.26,1), T=(.8,1) of S are excluded, and its other point hypotheses are identical. Equations (1)–(4) of that proof give

    U≥.26c,  V≥−1.086s,  U+a≤c+s,  s>.174.             (3)

At F its upper u band follows from A and its lower v band from N. A lower u exclusion, together with the upper u cap in (3), would give a≤.74c<1. Therefore

    V+a≤c−.26s.                                        (4)

We now use the whole segment S. Suppose c+.286s≤1. At T both lower bands are strict by N. A lower-v to upper-v width using (3) would be at most c+.286s≤1, so T must be upper u:

    U+a≤.8c+s.                                         (5)

Consider the closed upper vertex Z=(c(U+a)−s(V+a),s(U+a)+c(V+a)). Equations (3)–(5) give

    Z_x≥.26+c(a−s)>.26,
    Z_x≤.8+s(c+.286s−a)<.8,
    Z_y≥a(c+s)−.826cs>1.                               (6)

For the last inequality, put K=c+s. The exact identity K−1=2cs/(K+1) gives

    K−1≥(2sqrt(2)−2)cs>.826cs

when cs>0; in (6), strictness also follows from a>1. Here s>0 already follows from (3). The strict point N has .26<N_x<.8 and N_y<1. The segment from N to Z crosses S before reaching the closed vertex; such an intermediate point is strict in a convex open square. This contradicts exclusion of S. Thus

    c+.286s>1.

The exact identity c+.286s−1=2t(.286−t)/(1+t²) now gives 0<t<143/500. On this interval T cannot be upper u: (3) would imply a≤.54c+s, whose increasing canonical-angle expression at t=143/500 equals

    13347877/13522450<1.

Hence T is upper v and V+a≤c−.8s. Finally (3) gives 1<a≤.74c+s. The factorization

    .74c+s−1=(1−t)(87t−13)/(50(1+t²))

proves t>13/87 and completes (1).

For X in (2), the upper u and upper v bands follow strictly from A and N:

    u(A)−u(X)=.475c+.385s>0,
    v(N)−v(X)=.175s+.475c>0.

The lower u band follows from U+a≤u(P), because the gap .475c+1.125s is increasing throughout the canonical interval. At t=143/500 its exact value is

    u(P)−u(X)<10796469/10817960<1<a.                    (7)

The lower v band follows from V+a≤v(T). Its gap 1.125c−.275s decreases strictly with angle, and at t=13/87 it equals

    v(T)−v(X)<154059/154760<1<a.                        (8)

The exact margins in (7)–(8) are 21491/10817960 and701/154760. All four bands are therefore strict. ∎

## 2. A vertical upper span reaches the same point

**Theorem 2.** Let Q strictly own

    M=(.35,.35), D=(.26,0), F=(.26,1),

exclude L=(0,.26), P=(0,1), and exclude the entire segment

    B={1}×[.26,.56].

Then its canonical angle is strictly positive, its half-angle is greater than7/18, and Q strictly owns

    Y=(21/40,1/8)=(.525,.125).                         (9)

**Proof.** Denote the segment endpoints by B0=(1,.26), B1=(1,.56), and the lower face coordinates by U,V.

First use the nonpositive frame u=(c,−s), v=(s,c), where c≥s≥0 and c²+s²=1. At L its upper u band follows from D, its lower v band follows from D, and its upper v band follows from F:

    u(D)−u(L)=.26(c+s)>0,
    v(L)−v(D)=.26(c−s)≥0,
    v(F)−v(L)=.26s+.74c>0.

Thus L is lower u. At B0 both lower bands follow from D; its upper v band follows from F, with increment .74(c−s)≥0. Hence B0 is upper u. The opposite faces give a≤u(B0)−u(L)=c≤1. This excludes this entire sign, including the axial and diagonal endpoints.

Use the positive frame u=(c,s), v=(−s,c). The same anchor comparisons show that L is lower u:

    U≥.26s.                                             (10)

Indeed u(D)−u(L)=.26(c−s)≥0, v(L)−v(D)=.26(c+s)>0, and v(F)−v(L)=−.26s+.74c>0. At B0 its lower u band follows from D and its upper v band from F. If it were upper u, (10) would give a≤c≤1. Consequently

    V≥−s+.26c.                                          (11)

Strict ownership of D gives −.26s>−s+.26c, or s/c>13/37. At P, its upper u band follows from F, its lower v band from D, and its lower u band from D because s−.26c>0. Thus

    V+a≤c.                                              (12)

Suppose s+.44c≤1. At B1 its lower u band is strict by D and its upper v band is strict by F. A lower v exclusion, together with (12), would give a≤s+.44c≤1. Thus B1 must be upper u:

    U+a≤c+.56s.                                         (13)

Consider the closed rightmost vertex Z=(c(U+a)−sV,s(U+a)+cV). Bounds (10)–(13) imply

    Z_x≥a(c+s)−.74cs>1,
    Z_y≥.26+s(a−c)>.26,
    Z_y≤.56+c(s+.44c−a)<.56.                           (14)

The first inequality uses c+s−1≥(2sqrt(2)−2)cs≥.74cs and a>1. The point M is strict, M_x<1, and .26<M_y<.56. Interpolating between M and Z therefore produces a strict point of Q on the forbidden segment B, a contradiction.

Thus s+.44c>1. With t=s/(1+c),

    (1+t²)(s+.44c−1)=(2/25)(18t−7)(1−t)

proves t>7/18, since 0<t≤sqrt(2)−1<1. In particular s/c>252/275.

At the target Y, its lower u band follows from D, its upper u band from F, and its upper v band from M:

    u(Y)−u(D)=.265c+.125s>0,
    u(F)−u(Y)=−.265c+.875s>0,
    v(M)−v(Y)=.175s+.225c>0.

For its remaining lower v band use (12). The gap v(P)−v(Y)=.875c+.525s decreases when s/c≥252/275, because .525−.875(s/c)<0. At t=7/18 its exact value is

    .875c+.525s=14917/14920<1.                          (15)

Thus the opposite upper face in (12) forces V<v(Y). Every band of Y is strict, proving (9). Every inequality at an excluded endpoint or face was weak; both interpolations in the proof occur before the closed vertex, so tangency does not invalidate the contradiction. ∎

## 3. Exact branch exclusion in both C974 and C976

Suppose northeast Q7 in either C974 or C976 has label196736, owning F7,G6,G7 and excluding F5. The top owner has already been reduced to label16392 by `C974-C976-DUPLICATE-POINT.md`. Section 3.1 of `C974-C976-CONTINUOUS-REDUCTIONS.md` applies the all-angle corner-to-wall transfer theorem to actual Q4,Q11 and puts (2,3) strictly in top Q11 in both families. Its required (1,2.5) is strict in actual Q8 by the older wall advance, which does not exclude the northwest marker.

Translate Q7 by (−2,−2) and apply Theorem 2. Its strict marker and owned G6,G7 give M,D,F. The exclusion L is its genuinely omitted F5; P=(2,3) is strict in Q11. The entire required segment is the translation of

    {3}×[2.26,2.56]⊂Q10,

where actual Q10 owns F9 and the uniform strict wall advance (3,2.56). Thus

    (2.525,2.125)∈Q7 strictly.                         (16)

Since G6 belongs to Q7, actual southeast Q6 is forced to the outward label262400, owning F8,G8. Its sign is strictly negative by the outward sign theorem, with the same actual bottom bar and corner sources recorded in Section 3 of `C974-C976-DUPLICATE-POINT.md`. Reflect Theorem 1 through y=2 and translate its coordinates back by (2,2). The required whole bar belongs to actual bottom Q9; G lies in Q7, R lies in Q10, and P,H lie in actual paired southeast corner Q2. Therefore

    (2.525,2.125)∈Q6 strictly.                         (17)

Equations (16)–(17) contradict disjoint interiors. This excludes the complete branch Q7=196736 in both C974 and C976, without restrictions on the remaining auxiliary choices or missing-corner alternative. The C976 top-origin premise is supplied by the genuine two-square transfer just identified, rather than by importing C974's stronger left-wall advance.

## 4. The upper square needs only its marker and outer top point

**Theorem 3.** Let Q have side a>1 and strictly own

    M=(.35,.35), A=(.4,1).

Suppose Q excludes L=(0,.26), P0=(0,1), P1=(1,1), and the entire segment

    B={1}×[.26,.56].

Then Q strictly owns Y=(.525,.125).

This point conclusion does not require ownership of either (.26,0) or (.26,1). In particular the strict span in Theorem 2 is unnecessary for this weaker, unoriented conclusion.

**Proof.** Suppose Y is excluded. Write B0=(1,.26), B1=(1,.56), and let U,V be lower face coordinates.

First use a nonpositive canonical frame u=(c,−s), v=(s,c), with c≥s≥0 and c²+s²=1. At P0 both upper bands follow from A and its lower v band follows from M. Hence P0 is lower u: U≥−s. At Y its lower u and upper v bands follow from M, with increments .175c+.225s>0 and −.175s+.225c≥.05c>0. It is upper u or lower v. Upper u would give

    a≤u(Y)−u(P0)=.525c+.875s≤1.4/sqrt(2)<1.

Thus Y is lower v. At P1 both lower bands follow from M. An upper v exclusion would imply

    a≤v(P1)−v(Y)=.475s+.875c≤sqrt(.99125)<1.

Therefore P1 is upper u, and opposite u faces at P0,P1 give a≤c≤1. This contradiction excludes the entire nonpositive sign under the supposition that Y is missing.

Now take the nonnegative frame u=(c,s), v=(−s,c). The upper v band of Y is strict by M, with difference .175s+.225c>0. It can therefore be lower u, upper u, or lower v.

Suppose first that Y is lower u. At P1 both lower bands follow from M, and its upper u band follows from the opposite lower face at Y because

    u(P1)−u(Y)=.475c+.875s≤1.35/sqrt(2)<1<a.

Thus P1 is upper v. At B0 its lower u band follows from M and its upper v band from A. Its upper u band follows from

    u(B0)−u(Y)=.475c+.135s≤sqrt(.24385)<1<a.

Hence B0 is lower v. These two v faces give a≤v(P1)−v(B0)=.74c<1. Thus Y cannot be lower u.

Suppose next that Y is upper u. At P0 its upper u band follows from A and its lower v band follows from M. If it were lower u, the gap u(Y)−u(P0)=.525c−.875s≤.525 would contradict a>1. Therefore P0 is upper v. At L both upper bands follow from M,A: the positive increments are .35c+.09s and .74c−.4s≥.34c. If L were lower v, its opposite-face gap to P0 would be .74c<1. Hence L is lower u. But then a≤u(Y)−u(L)=.525c−.135s≤.525<1. Thus Y cannot be upper u either.

The only remaining possibility is

    V≥v(Y)=−.525s+.125c.                               (18)

At P1 both lower bands are strict by M. Its upper v exclusion would give a≤.875c−.475s≤.875, so P1 is upper u. At P0 the upper u and lower v bands follow from A,M; a lower u exclusion would give width c≤1 opposite P1. Hence P0 is upper v. At L both upper bands follow from M,A as above; lower v would give width .74c opposite P0, so L is lower u. At B0 its lower u band follows from M and its upper v band from A. Its upper u band is strict because the lower face at L gives u(B0)−U≤c≤1<a. Therefore

    U≥.26s,  V≥−s+.26c,  V+a≤c.                       (19)

The actual whole segment now forces s+.44c>1 by the same explicit vertex argument as Theorem 2. To repeat its short derivation, if s+.44c≤1, B1 has its lower u band from M and upper v band from A. Lower v would give width at most s+.44c opposite the cap V+a≤c, so B1 must be upper u: U+a≤c+.56s. The closed rightmost vertex Z then obeys

    Z_x≥a(c+s)−.74cs>1,
    .26<Z_y≤.56+c(s+.44c−a)<.56.

Here the lower ordinate bound is .26+s(a−c)>.26; s=0 is already impossible from (19), which would give a≤1. Interpolation from strict M crosses B at a strict point before Z, a contradiction.

Thus the half-angle t=s/(1+c) exceeds7/18. But (18) and (19) give

    a≤c−v(Y)=.875c+.525s<14917/14920<1,

by the exact endpoint calculation (15). This final contradiction proves that Y is strict in Q. Every canonical sign and endpoint has been covered, and excluded points and segment contacts were allowed to be tangent. ∎

### A shared strict point for every top-only northeast label

Apply Theorem 3 to northeast Q7 in either C974 or C976 whenever it owns F7=(2.4,3) and excludes F5=(2,2.26). Its marker gives M after translation by (−2,−2); actual top Q11 owns P0=(2,3) by the direct corner transfer, actual northeast corner Q3 owns P1=(3,3), and actual right wall Q10 owns the entire required segment {3}×[2.26,2.56]. Thus

    (2.525,2.125)∈Q7 strictly.                         (20)

If southeast Q6 has outward label262400, its reflected full-bar theorem gives the same strict point. This is impossible. In particular, after the consolidated reductions, the combination

    Q6=262400,  Q7=131200

is impossible in both families. If Q6 has this outward label, its northeast neighbor must therefore own F5. The theorem also reproves the label196736 exclusion without needing its owned G6,G7 span; Theorem 2 retains the additional orientation conclusion for reuse.
