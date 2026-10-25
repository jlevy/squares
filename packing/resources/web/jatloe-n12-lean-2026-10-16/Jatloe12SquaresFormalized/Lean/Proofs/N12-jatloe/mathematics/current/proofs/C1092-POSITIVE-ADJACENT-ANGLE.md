# C1092: a direct positive-angle bound from adjacent actual central squares

Every terminating decimal denotes an exact rational. Owned points are strict; exclusions and all separating inequalities may be weak. The squares have a common side a>1. No upper side bound, center enclosure, or boundary-angle restriction is used in this chapter.

## 1. A two-square theorem with explicit actual faces

Let C and J be two disjoint open squares of side a>1, with positive canonical frames

    u_p=(c_p,s_p), v_p=(−s_p,c_p),
    u_q=(c_q,s_q), v_q=(−s_q,c_q),
    0≤p,q≤π/4.

For either square let U,V denote its lower face values in its own displayed frame. Suppose C strictly owns T=(1.74,2), J strictly owns E=(2,1.74), and their actual faces satisfy

    U_C+a≤u_p·E,       V_C+a≤v_p·D,       D=(1,2),
    U_J+a≤u_q·R,       V_J+a≤v_q·F,       R=(3,1.6), F=(2.26,2).       (1)

**Theorem 1.** Under these hypotheses,

    tan(p/2)<7/32.                                      (2)

The exact C1092 derivation of the four face inequalities (1) is recorded in Section 5. In particular, no choice of an excluded point's face is assumed by resemblance to a previous row or sign.

**Proof.** Suppose p≥p₀:=2 arctan(7/32). Then

    c₀=975/1073, s₀=448/1073,
    s_p≥s₀>5/12, c_p+s_p≥1423/1073>63/50.

Define

    ell(t)=1.26 cos t−.4 sin t.

It decreases on [0,π/4], and

    ell(p)≤ell(p₀)=10493/10730<1.                     (3)

In each order put κ=cos(p−q)>0 and τ=|sin(p−q)|≥0. We retain all four actual possible normal sources.

## 2. The transverse sources are impossible

For any positive canonical first normal u_t, u_t·(E−T)=.26(c_t−s_t)≥0. Thus J-before-C on either first normal is impossible, since both named points are strict. For either positive transverse normal v_t, v_t·(E−T)=−.26(c_t+s_t)<0. Thus C-before-J on that transverse normal is impossible. The only possibilities still needing examination are C-before-J on u_p,u_q, or J-before-C on v_p,v_q.

On v_p, (1) and strict ownership of E by J give

    lower_C(v_p)≤v_p·D−a<v_p·E≤upper_J(v_p),

because

    v_p·(D−E)=.26c_p+s_p≤1.26/sqrt(2)<1<a.

Hence the transverse normal supplied by C cannot separate the two squares.

Consider v_q. If q≤p, then v_q=τu_p+κv_p. Equation (1) implies

    lower_C(v_q)
      ≤τ u_p·E+κ v_p·D−a(κ+τ)
       =v_q·D+τ(c_p−.26s_p)−a(κ+τ)
       <v_q·D−κ.

The strict last inequality uses a>1 and c_p−.26s_p≤1. Also

    κ≥cos(π/4−q)=(c_q+s_q)/sqrt(2)>.26c_q+s_q.

For the final comparison, use c_q≥s_q and sqrt(2)>1.26. Therefore lower_C(v_q)<v_q·E, whereas E is strict in J. This excludes the proposed order on v_q.

If q≥p, then v_q=−τu_p+κv_p. Strict T and (1) give

    lower_C(v_q)
      ≤−τ u_p·T+κ(v_p·D−a)
       =v_q·D−.74c_p τ−aκ
       <v_q·D−κ.

Here the initial inequality is strict when τ>0; the displayed final strict inequality holds also when τ=0 because a>1. The standing p≥p₀ gives

    κ≥cos(π/4−p)=(c_p+s_p)/sqrt(2)
       >1.26/sqrt(2)≥.26c_q+s_q.

Again lower_C(v_q)<v_q·E, so v_q cannot separate the squares. Consequently only the two forward first normals remain.

## 3. The first normal of C is impossible

Suppose upper_C(u_p)≤lower_J(u_p).

If q≥p, write u_p=κu_q−τv_q. Use the upper-u cap for J, strict ownership of E by J, and strict T in C. The necessary inequality is

    aκ<ell(p)−τ(s_q+.14c_q).                         (4)

Indeed

    lower_J(u_p)≤κ(u_q·R−a)−τ v_q·E,

and subtracting u_p·T gives (4). Its right side is at most κ: by (3), s_q≥s_p>5/12, while

    (1−κ)/τ=tan((q−p)/2)≤sqrt(2)−1<5/12

when τ>0. At τ=0 use ell(p)<1=κ directly. This contradicts a>1.

If q≤p, use u_p=κu_q+τv_q and both J caps in (1). The necessary inequality becomes

    a(κ+τ)<ell(p)+τ(.4c_q+.74s_q).                  (5)

For τ>0, set z=tan((p−q)/2). Since p≤π/4,

    z≤(c_q−s_q)/(sqrt(2)+c_q+s_q)
      <(5/12)(c_q−s_q).

Hence, by Cauchy–Schwarz,

    .4c_q+.74s_q+z
      ≤(49/60)c_q+(97/300)s_q
      ≤sqrt(69434)/300<1.                            (6)

Together with (3), this bounds the right side of (5) strictly below κ+τ, because 1−κ=τz. At τ=0, (3) gives the same contradiction directly. Thus u_p is excluded in both angle orders.

## 4. The first normal of J is impossible

Suppose upper_C(u_q)≤lower_J(u_q). If q≥p, the strict point T and the upper-u cap for J already imply

    a<u_q·(R−T)=ell(q)≤ell(p)<1,

which is impossible.

It remains q≤p. Then u_q=κu_p−τv_p. Strict T and C's upper-v cap give

    upper_C(u_q)
      ≥κ u_p·T−τ(v_p·D−a)
       =u_q·T+τ(a−.74s_p).

This inequality is strict because κ>0 and T is strict. Combine it with lower_J(u_q)≤u_q·R−a. After using a>1, the necessary scalar inequality is

    1<ell(q)−τ(1−.74s_p)
      =A(s_p)c_q+B(s_p)s_q,                          (7)

where, for 0≤S≤1/sqrt(2),

    k(S)=1−.74S,
    A(S)=1.26−S+.74S²,
    B(S)=sqrt(1−S²)(1−.74S)−.4.

We show that the last expression in (7) is less than one whenever S≥s₀.

First,

    A(S)−1=.74(S−1)(S−13/37)<0                      (8)

on s₀≤S≤1/sqrt(2), since s₀>13/37. Also A(S)≥1.26−1/sqrt(2)>0. Thus if B(S)≤0, positivity of c_q,s_q immediately gives A(S)c_q+B(S)s_q≤A(S)<1.

Suppose B(S)>0. The function B decreases strictly. At S=2/3,

    B(2/3)=38sqrt(5)/225−2/5<0.

Consequently S<2/3. On [s₀,2/3], A is positive and decreasing because A'(S)=−1+1.48S<0, and B is decreasing. As long as B remains nonnegative, A²+B² therefore decreases. At the rational point s₀, direct substitution gives

    A(s₀)=60459/62234, B(s₀)=35461/155585,
    1−A(s₀)²−B(s₀)²=13323/3111700>0.                (9)

It follows from Cauchy–Schwarz that

    A(S)c_q+B(S)s_q≤sqrt(A(S)²+B(S)²)<1.

This contradicts (7). Every actual separating normal has now been excluded under p≥p₀. The supposition is impossible, proving (2). Equal angles, canonical endpoints, and weak support tangencies have all been included. ∎

## 5. Exact application to the last C1092 assignment

Use the sector charts R⁻ⁱ with R(x,y)=(4−y,x), the actual central owners C_i=Q_(4+i), and actual boundary owners

    (B₀,B₁,B₂,B₃)=(Q₉,Q₁₀,Q₁₁,Q₈).

These are the last MPPM owners identified in Section 6 of `C1092-NEGATIVE-H-PROPAGATION.md`. Each local C strictly owns

    M=(1.65,1.65), U₀=(1,1.74), L₀=(1,1.6), T=(1.74,2).

The actual paired corner owns (1,1), the actual bottom B owns (1.6,1), and the next actual central owns E=(2,1.74). The point D=(1,2) is outside C by the unconditional theorem `C1092-POSITIVE-D-TRANSFER.md`. When the preceding boundary owns its local P=(2,1), this exclusion also follows directly from that actual owner.

For a positive canonical frame, D has both u-bands strict by U₀,T and its lower v-band strict by U₀. Therefore V+a≤2c−s. At E its lower u-band is strict by M, and its upper v-band is strict by T. A lower-v exit would oppose the D cap and give

    a≤v(D)−v(E)=.26c+s<1.

Thus E must leave through upper u, giving U+a≤2c+1.74s.

The foreign (1.6,1) has its lower u-band strict by L₀, since their u-projection difference is .6(c−s)≥0. Its upper u-band is strict by M, and its upper v-band is strict by U₀. Hence it leaves through lower v:

    V≥c−1.6s.

Apply the same conclusions in the next sector, and rotate that entire actual square into the present chart. Its lower-v face at (1.6,1) becomes the upper-u face at R=(3,1.6); its upper-u face at E becomes the upper-v face at F=(2.26,2). Its strict T becomes the strict E in J. These are exactly the four caps and two strict points in (1).

Thus whenever two consecutive central canonical angles are positive, the unconditional D exclusions and Theorem 1 give the first central half-angle bound tan(p/2)<7/32. In particular, all four central squares satisfy this bound in the actual all-positive last assignment, whether or not their corresponding boundary P points are owned.

This chapter proves a direct entrance improvement. The later `C1092-POSITIVE-QUADRANT-BOOTSTRAP.md` sharpens the central half-angle to 1/5 and derives the actual central quadrants and a boundary-angle bound from these premises. The smaller half-angle 7/64 and completion of the all-positive cycle require a further actual support argument.

## 6. A positive sector which misses H is also in the central disk

**Theorem 2.** In the original last C1092 assignment, let C have positive canonical angle with tan(p/2)<7/32. Suppose D=(1,2) is outside C. If H=(1,1.5) is outside C, then the actual center of C lies strictly in the disk of radius 1/sqrt(2) about (2,2).

Its own P need not be missing or owned. No boundary-angle or center hypothesis is used. The unconditional theorem `C1092-POSITIVE-D-TRANSFER.md` supplies this D premise in every actual last-assignment sector.

**Proof.** Write c=cos p,s=sin p. In particular

    c>9/10, 0<s<21/50.

We first recall the all-angle forced exit of H, which uses only the original strict C points and the foreign northwest central marker N=(1.65,2.35). H's upper u-band is strict by M, and its upper v-band is strict by L₀. If H left through lower v, strict M would imply s/c<3/13. Both lower bands of N are strict, by U₀ and M. An upper-u exit of N would require, by strict T,

    −.09c+.35s>0,

contradicting 3/13<9/35. Thus N would leave through upper v, and the two opposite v-faces at H,N would imply a≤.85c−.65s<1. This is impossible. Therefore

    U≥c+1.5s.                                          (10)

The unconditional actual boundary advance in Section 2 of `C1092-NEGATIVE-OWNED-POINTS.md` puts L'=(1.44,1) strictly inside the actual bottom B, so L' is outside C. Its lower u-band is strict by L₀ because

    u(L')−u(L₀)=.44c−.6s>0;

here tan p<448/975<11/15. Its upper u-band is strict by M and its upper v-band is strict by U₀. Hence

    V≥c−1.44s.                                         (11)

The assumed exclusion of D gives its forced upper-v exit V+a≤2c−s, as in Section 5. Together with (11),

    a≤c+.44s.                                          (12)

Let δu,δv be the two orthogonal projections of the actual center minus (2,2). Equations (10)–(12), strict L₀, and the D cap give

    a/2−c−.5s≤δu<a/2−c−.4s<0,
    a/2−c+.56s≤δv≤s−a/2<0.

The final signs follow respectively from (12) and s<.42<1/2<a/2. Put

    A=c+.5s−a/2, B=c−.56s−a/2.

Both are positive: (12) gives A≥c/2+.28s>0 and B≥c/2−.78s>.45−.78(.42)>0. Thus

    |center(C)−(2,2)|²≤A²+B²
      <(c+.5s−.5)²+(c−.56s−.5)².                     (13)

The strict inequality uses a>1 and positivity of A,B. The exact difference between the final expression and 1/2 is

    s²[2/(1+c)−1.4364]+.06s(1−2c)<0.                 (14)

Indeed c>1/2 implies 2/(1+c)<4/3<1.4364 and 1−2c<0. Equations (13)–(14) prove the strict disk conclusion. Every excluded point may be tangent to C, and no strictness has been inferred from its exclusion. ∎

In the actual all-positive last assignment, the unconditional D exclusions and Theorem 1 supply the premises of Theorem 2 at every sector. Consequently every sector which does not strictly own H is in the central disk. A further actual support argument is still needed for the complementary positive sectors which strictly own H.
