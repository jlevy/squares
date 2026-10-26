# Central crosspoints and a top-only outward extension in C974 and C976

All decimals are exact rationals. Squares are open, and every owned point is strict. Excluded points may lie on the boundary. This file uses only completed continuous lemmas and names the actual owners in every application.

## 1. Every remaining southeast square owns the horizontal crosspoint

After `ELBOW-CROSSPOINT.md`, the two remaining southeast labels in either family are262400 and327936. Both strictly own

    C=(2.5,2).                                           (1)

For label327936, apply Theorem 2 of that file with w=.8. The strict southeast marker, G6=(2.26,2), and F8=(3,1.74) are its three anchors. Actual southwest Q5 owns (2,1.5), and actual bottom Q9 owns (2.8,1). If Q6 excluded C, the theorem would contradict a>1. Therefore C is strict in Q6.

For label262400, use Theorem 1 of `OUTWARD-BAR-AND-UPPER-SPAN.md` in its normalized reflected coordinates. The actual bottom segment, southeast paired corner and right wall give the hypotheses already mapped in that file. Its positive canonical frame has

    U+a≤c+s,   V+a≤c−.8s,   13/87<t<143/500,

where t=s/(1+c). The target corresponding to (1) is C0=(.5,0). Its upper u band follows from A=(1,.26), and its upper v band from N=(.35,.35): the positive increments are .5c+.26s and .15s+.35c. The opposite upper u face gives the strict lower u band, since .5c+s increases over the canonical angle interval and

    .5c+s<515551/540898<1<a.

The opposite upper v face gives the strict lower v band, since

    (c−.8s)−v(C0)=c−.3s<1<a.

Here s>0 follows from the displayed strict half-angle interval. Thus C0, and hence the original C, is strict.

## 2. Every remaining northeast owner of F5 owns the vertical crosspoint

Suppose northeast Q7 owns F5=(2,2.26). It also owns its marker and G7=(2.26,3), by the consolidated reduction. Rotate Theorem 2 of `ELBOW-CROSSPOINT.md` by

    (x,y)↦(4−y,x)

and choose w=.56. Its strict anchors M,D,A become precisely the northeast marker, F5, and G7. Its two excluded points C=(2,1.5) and T=(2.56,1) become respectively

    (2.5,2),  (3,2.56).

The first is strict in actual southeast Q6 by Section 1; the second is strict in actual right wall Q10 by the uniform wall advance. The theorem's impossible third exclusion X becomes (2,2.5). It follows that

    (2,2.5)∈Q7 strictly.                                (2)

This application requires neither the stronger C974 left-wall reach nor any ownership of the northwest marker.

## 3. A top-only square extends past the half-unit point

**Theorem.** Let Q be an open square of side a>1 strictly owning

    M=(.35,.35), A=(.4,1),

and excluding

    L=(0,.26), P=(0,1), X=(.5,0).

Then Q strictly owns H=(.5,1). No container, upper side bound, or foreign segment is needed.

**Proof.** Let U,V denote lower face coordinates. First use a nonnegative canonical frame u=(c,s), v=(−s,c), where c≥s≥0 and c²+s²=1. At H its lower u band follows from A, its lower v band from M, and its upper v band from A:

    u(H)−u(A)=.1c>0,
    v(H)−v(M)=.65c−.15s≥.5c>0,
    v(A)−v(H)=.1s≥0.

Suppose H is not strict. It must be upper u, so U+a≤.5c+s. At P its upper u band follows from A and its lower v band from M. A lower u exclusion would give the impossible width a≤u(H)−u(P)=.5c≤.5. Hence P is upper v, V+a≤c.

At L its upper u band follows from M and its upper v band from A; the increments are .35c+.09s>0 and .74c−.4s≥.34c>0. A lower v exclusion would give a≤v(P)−v(L)=.74c<1. Consequently L is lower u, U≥.26s. The two u faces now yield

    a≤.5c+.74s≤sqrt(.7976)<1,

a contradiction. Thus H is strict for every nonnegative canonical representative, including the axial and diagonal endpoints.

Use the nonpositive frame u=(c,−s), v=(s,c). Both lower bands of H follow from A, so an excluded H must be upper u or upper v. At P the upper u band follows from A, the upper v band from A, and the lower v band from M: their increments are .4c>0, .4s≥0, and .65c−.35s≥.30c>0. Therefore P is lower u, U≥−s. If H were upper u, the opposite width would be a≤.5c≤.5. Thus

    V+a≤v(H)=.5s+c.                                     (3)

At X its lower u band follows from M and its upper v band from M, with increments .15c+.35s>0 and .35c−.15s≥.20c>0. Its lower v band is strict by the cap (3), because

    v(H)−v(X)=c≤1<a.

Therefore the excluded X must be upper u, U+a≤.5c. At L its upper u band follows from M and its upper v band from A:

    u(M)−u(L)=.35c−.09s≥.26c>0,
    v(A)−v(L)=.4s+.74c>0.

Its lower u band follows strictly from the opposite cap at X, since

    u(X)−u(L)=.5c+.26s≤sqrt(.3176)<1<a.

Thus L is lower v. Together with (3) this gives

    a≤v(H)−v(L)=.5s+.74c≤sqrt(.7976)<1,

again impossible. Both canonical signs and their axis and diagonal limits are covered. Every exterior face inequality was weak, and each target band obtained from an owned anchor or an opposite face was strict. ∎

## 4. Exact top-only northeast and right-wall consequences

Suppose the remaining northeast label is131200. Translate by (−2,−2) and apply the theorem in Section 3. The strict marker and F7 give M,A. The omitted F5 gives L; the actual top origin (2,3) in Q11 gives P; Section 1 supplies X=(2.5,2) strictly in actual Q6. Hence

    (2.5,3)∈Q7 strictly.                                (4)

The actual right wall Q10 then owns its origin:

    (3,2)∈Q10 strictly.                                 (5)

For completeness, apply Theorem 7 of `C1092-DIRECT-WALL-POINT.md` under the simultaneous map

    (ξ,η)=(4−y,4−x).

Its actual K is the northeast paired corner Q3, and its actual B is right wall Q10. The parameter values are b=.914 and ell=1.6. The strict point mapping is:

| Local datum | Original owner and point |
|---|---|
| K owns (1,b) | Q3 owns (3.086,3) |
| K owns (1,1) | Q3 owns (3,3) |
| K excludes (1,1.5) | Q7 owns (2.5,3), by (4) |
| B owns (2,b) | Q10 owns (3.086,2) |
| B owns (ell,1) | Q10 owns G9=(3,2.4) |
| First-quadrant and bottom-wall conditions | The transformed genuine container walls |

The two squares have the common side a>1 and disjoint interiors. The theorem gives local (2,1) in B, which is precisely (3,2) in the original Q10. This uses the actual corner and wall, and is valid in both C974 and C976.

## 5. The right origin transfers to a lower southeast point

**Theorem 2.** Let Q have side a>1 and strictly own

    M=(.35,−.35), D=(.26,0), A=(1,−.26).

Suppose Q excludes

    C=(0,−.5), Y=(.525,.125), R=(1,0).

Then Q strictly owns S=(1,−.5).

**Proof.** First use a nonnegative canonical frame u=(c,s), v=(−s,c), c≥s≥0. At Y the lower u and upper u bands follow from D,A, and the lower v band follows from M:

    u(Y)−u(D)=.265c+.125s>0,
    u(A)−u(Y)=.475c−.385s≥.09c>0,
    v(Y)−v(M)=−.175s+.475c≥.30c>0.

Thus Y is upper v, V+a≤−.525s+.125c. For S, its lower u band follows from M and its upper u and upper v bands from A. The required increments are .65c−.15s≥.5c>0, .24s≥0, and .24c>0. The remaining lower v band follows from the opposite upper cap, since

    v(Y)−v(S)=.475s+.625c≤sqrt(.61625)<1<a.

Therefore S is strict for this entire canonical sign. This part did not need the two other exclusions.

Use the nonpositive frame u=(c,−s), v=(s,c). At Y its lower u and lower v bands follow from D, and its upper u band follows from A:

    u(Y)−u(D)=.265c−.125s≥.14c>0,
    v(Y)−v(D)=.265s+.125c>0,
    u(A)−u(Y)=.475c+.385s>0.

Thus V+a≤.525s+.125c. At C its upper u band follows from A and its upper v band from D. Its lower v band follows from that cap because

    v(Y)−v(C)=.525s+.625c≤sqrt(.66625)<1<a.

Consequently C is lower u, U≥.5s. At R both lower bands follow from D,A. If R were upper u, the opposite width would give a≤c−.5s≤1. It is therefore upper v:

    V+a≤s.

The target S has its lower u band from M and its upper v band from A. Its lower v band follows from the displayed cap, with opposite gap .5c<1. An upper u exclusion would give

    a≤u(S)−U≤c≤1.

This is impossible, so S is strict also in the negative sign. Both axis and diagonal endpoints are included, and exterior contacts remained weak throughout. ∎

### The exact remaining mixed/top-only pair

In the remaining pair Q6=327936, Q7=131200, use Theorem 2 after translation by (−2,−2). Its three anchors are strict in Q6. Its excluded C=(2,1.5) belongs to Q5, its Y=(2.525,2.125) belongs to Q7 by the upper-square point theorem, and its R=(3,2) belongs to Q10 by Section 4. Therefore

    (3,1.5)∈Q6 strictly.                                (6)

Apply the actual corner-to-wall Theorem 7 of `C1092-DIRECT-WALL-POINT.md` under (ξ,η)=(4−x,y), with K=Q2, B=Q9, b=.914, ell=1.6. The paired southeast corner supplies local (1,b),(1,1), and excludes local (1,1.5) because of (6). The bottom wall Q9 supplies local (2,b),(1.6,1), from its marker and F6=(2.4,1). The genuine walls give the required first-quadrant and bottom-wall conditions. Thus

    (2,1)∈Q9 strictly.                                 (7)

Both (6) and (7) hold in C974 and C976. They are consequences for these actual squares, without assigning a new owner to any auxiliary point.

## 6. The outward southeast pair also gives the bottom origin

If Q6 has label262400, the reflected outward theorem already gives the two lower face bounds U≥.26c and V≥−1.086s in its positive normalized coordinates, with strict anchors N=(.35,.35), A=(1,.26). The point S0=(1,.5) has both lower bands from A. Its upper bands are strict by

    u(S0)−U≤.74c+.5s≤sqrt(.7976)<1<a,
    v(S0)−V≤.086s+.5c≤sqrt(.257396)<1<a.

After reflection and translation this is again (3,1.5) strictly in actual Q6. The exact Q2/Q9 corner transfer just given yields (2,1) strictly in Q9. At this stage the bottom origin is established for three of the four central pairs then remaining. The pair Q6=327936, Q7=131232 is covered by the later parameterized transfer in Section 8.

## 7. An all-angle lower point in the northeast mixed elbow

**Theorem 3.** Let N have side a>1 and strictly own

    M=(.35,.35), F=(0,.26), G=(.26,1).

Suppose N excludes

    L=(−.35,.35), P0=(0,1), P1=(1,1), B=(1,.26).

Then N strictly owns K=(.42,.16).

**Proof.** In a nonnegative canonical frame u=(C,S), v=(−S,C), C≥S≥0, the point L has its upper u and lower v bands from F and its upper v band from G. The corresponding increments are .35C−.09S≥.26C>0, .35S+.09C>0, and .65C−.61S≥.04C>0. Thus

    U≥−.35C+.35S.                                      (8)

At P0 its upper u band follows from G and its lower v band from M. Suppose it were lower u, U≥S. Both lower bands of P1 follow from M; an upper u exclusion would give width C≤1 opposite P0. Hence P1 would be upper v. At B its lower u band follows from M and its upper v band from G. Its upper u band would be strict because

    u(B)−U≤C−.74S≤1<a.

Thus B would be lower v. But the opposite v width from B to P1 is .74C<1, a contradiction. Therefore

    V+a≤C.                                             (9)

The target's lower u band follows from F, with increment .42C−.10S≥.32C>0, and its upper v band follows from M, with increment .07S+.19C>0. Its upper u band follows from (8), because

    u(K)−U≤.77C−.19S≤.77<1<a.

Its lower v band follows from (9), because

    C−v(K)=.84C+.42S≤sqrt(.882)<1<a.

Thus K is strict throughout the nonnegative sign.

For the nonpositive frame u=(C,−S), v=(S,C), P0 has its upper u and upper v bands from G, and its lower v band from M. It must be lower u: U≥−S. Both lower bands of P1 follow from M. An upper u exclusion would give width C≤1 opposite P0, so P1 is upper v:

    V+a≤C+S.                                           (10)

At K its lower u band follows from F and its upper v band from M, with increments .42C+.10S>0 and .19C−.07S≥.12C>0. Its upper u band follows from the lower face at P0:

    u(K)−U≤.42C+.84S≤1.26/sqrt(2)<1<a.

If S/C≥5/21, its lower v band follows directly from F, because .42S−.10C≥0. If S/C≤5/21, then S≤5/21 and (10) gives the opposite gap

    (C+S)−v(K)=.84C+.58S
                  ≤.84+.58(5/21)=1027/1050<1<a.

So the remaining band is strict also in this interval. The two closed angle alternatives cover every negative canonical angle, including equality at their shared endpoint, and the axial and diagonal limits have been included. ∎

### Exact northeast consequence

Northeast label131232 owns exactly the three anchors used above, as well as F7. Translate by (−2,−2). The excluded L is the northwest marker, absent in C974 and in distinct Q8 in C976. P0 is the actual Q11 top origin; P1 is the actual Q3 corner point; B is F9 in the actual right wall Q10. Hence

    (2.42,2.16)∈Q7 strictly.                            (11)

This conclusion uses no side upper bound or wall-angle hypothesis.

## 8. A parameterized southeast transfer needs no right origin

The extra right-origin premise in Theorem 2 can be dropped. The following stronger statement also accommodates the new point (11).

**Theorem 4.** Let

    .4≤α≤.55, .1≤β≤.2,
    .26+β≤α, α+β≤.74.

Suppose a square Q of side a>1 strictly owns

    M=(.35,−.35), D=(.26,0), A=(1,−.26),

and excludes C=(0,−.5) and K=(α,β). Then Q strictly owns S=(1,−.5).

**Proof.** In a positive canonical frame u=(c,s), v=(−s,c), K has its lower u band from D, its upper u band from A and its lower v band from M. Indeed the first increment is (α−.26)c+βs>0; the second is at least (.74−α−β)c≥0; and the third is at least (.70+β−α)c≥.25c>0. Thus K is upper v.

The target S has its lower u band from M and its upper u and upper v bands from A. Its remaining lower v band follows from the opposite cap at K, since

    v(K)−v(S)=(1−α)s+(β+.5)c
               ≤sqrt(.6²+.7²)=sqrt(.85)<1<a.

For a negative frame u=(c,−s), v=(s,c), K again has its lower u, lower v and upper u bands from D,D,A. In particular its lower u increment is at least (α−.26−β)c≥0. Hence K is upper v.

At C its upper u and upper v bands follow from A and D. Its lower v band follows from the cap at K, since

    v(K)−v(C)=αs+(β+.5)c
               ≤sqrt(.55²+.7²)=sqrt(.7925)<1<a.

Therefore C is lower u, U≥.5s. The target S has its lower u band from M and its upper v band from A. Its upper u band follows from u(S)−U≤c≤1<a. Its lower v band follows from the upper cap at K, since

    v(K)−v(S)=(α−1)s+(β+.5)c≤.7<1<a.

All four target bands are strict in both signs. Parameter-boundary equalities are safe because they compare against strict owned anchors. This also covers both canonical angle endpoints and all exterior tangencies. ∎

### The bottom origin in every remaining central configuration

For northeast131200, use the point K=(.525,.125) from its completed upper-square point theorem. For northeast131232, use K=(.42,.16) from Theorem 3. Both parameter pairs satisfy Theorem 4; for the latter .26+β=α exactly, which its strict-anchor argument explicitly permits.

In either case the three southeast anchors are strict in actual Q6=327936, C=(2,1.5) is strict in actual Q5, and the indicated K is strict in actual Q7. Theorem 4 therefore puts (3,1.5) strictly in Q6. The exact actual Q2/Q9 corner transfer in Section 5 then gives

    (2,1)∈Q9 strictly                                  (12)

in both remaining central configurations, for both C974 and C976. No right-origin premise is needed for this universal bottom-origin conclusion.
