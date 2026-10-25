# C1092: the positive cycle forces its own angle bounds and center quadrants

All terminating decimals are exact rationals. Every owned point is strictly inside its named actual square. Excluded points and separating support inequalities may be tangent. All squares have the same side a>1. No upper side bound, central center enclosure, or initial boundary-angle bound is assumed.

## 1. Actual hypotheses and conclusion

Let R(x,y)=(4−y,x). Retain the actual last C1092 assignment in the sector charts R⁻ⁱ, with central owners C_i=Q_(4+i), boundary owners

    (B₀,B₁,B₂,B₃)=(Q₉,Q₁₀,Q₁₁,Q₈),

and the actual paired corner in each sector. In every chart the central C strictly owns

    M=(1.65,1.65), U₀=(1,1.74), L₀=(1,1.6), T=(1.74,2),

and the local boundary B strictly owns

    A_B=(2,.914), (1.6,1), (1.74,1), L'=(1.44,1).

The boundary lies in y≥0, and its actual center satisfies B_x≤2, as in the original MPPM entrance. The actual paired corner strictly owns (1,1). The next actual central J, expressed in the current chart, strictly owns E=(2,1.74) and (2.26,1). Assume that all four central canonical angles are positive and that D=(1,2) is outside each local C.

The original strict ownership, disjointness and boundary wall imply all the displayed point facts. The only extra hypothesis in the preceding paragraph is the explicit exclusion of D; its unconditional derivation in an all-positive last assignment is supplied by `C1092-POSITIVE-D-TRANSFER.md`.

**Theorem 1.** These actual hypotheses imply, in every sector,

    0<tan(p_C/2)<1/5,
    |tan(β_B/2)|<1/3,
    L''=(107/75,1) belongs strictly to B,
    X=(1.5,2) belongs strictly to C,
    center(C)_x<1.5<center(C)_y.                       (1)

Here β_B is the canonical signed boundary angle, −π/4≤β_B≤π/4. No ownership assumption is made about P=(2,1).

## 2. The original forced faces

Write u=(c,s), v=(−s,c), U,V for the positive central frame and lower face values. The exact face arguments in Section 5 of `C1092-POSITIVE-ADJACENT-ANGLE.md` use the preceding boundary P only to supply exclusion of D. Therefore the explicit D hypothesis here gives

    V+a≤2c−s,              U+a≤2c+1.74s,
    V≥c−1.6s.                                           (2)

For completeness, D's two u-bands follow strictly from U₀,T and its lower v-band follows from U₀. At E the lower u-band follows from M and the upper v-band from T. A lower-v exit of E would oppose D and imply a≤.26c+s<1; hence E leaves through upper u. At the foreign point (1.6,1), the lower u-band follows from L₀, the upper u-band from M, and the upper v-band from U₀, so it leaves through lower v.

The corner point (1,1) has both upper bands strict. A lower-v exit would oppose D and imply a≤c≤1. Thus

    U≥c+s.                                               (3)

For consecutive positive C,J, (2) rotates into precisely the four face premises of Theorem 1 of `C1092-POSITIVE-ADJACENT-ANGLE.md`. Consequently every central angle initially satisfies

    tan(p/2)<7/32,   c>975/1073>9/10,   s<448/1073<21/50. (4)

The foreign L'=(1.44,1) now has its lower u-band strict by L₀, since .44c−.6s>0 under (4); its upper u-band is strict by M, and its upper v-band by U₀. Hence

    V≥c−1.44s.                                          (5)

The last face, rotated from the next sector, sharpens J's upper-u cap to

    U_J+a≤u_q·R',       R'=(3,1.44).                    (6)

## 3. A second adjacent-central bound

We prove tan(p/2)<1/5 using (4)–(6). Suppose instead p≥p₁:=2 arctan(1/5). Then

    c₁=12/13, s₁=5/13, c₁+s₁=17/13>1.26.

Both p and q are less than p₀:=2 arctan(7/32). Put κ=cos(p−q)>0, τ=|sin(p−q)|. The two strict points T in C and E in J force the same separator orders as in the first adjacent-angle theorem: only forward first normals or downward transverse normals are possible.

The transverse sources are excluded by precisely the estimates of Section 2 of that theorem. They use only C's two upper caps in (2), strict T,E, and c_p+s_p>1.26. That last inequality holds here because p≥p₁. Thus only the first normals u_p,u_q remain.

Set

    ell(t)=1.26 cos t−.56 sin t.

It decreases, and

    ell(p)≤ell(p₁)=308/325<1.                           (7)

For the first normal u_p of C, if q≥p, the actual cap (6), strict E in J and strict T in C give

    aκ<ell(p)−τ(s_q+.30c_q).                           (8)

When τ>0, s_q+.30c_q>5/13+.27>sqrt(2)−1≥(1−κ)/τ. Equation (7) therefore bounds the right side of (8) strictly below κ. When τ=0 use (7) directly. This excludes this order.

If q≤p, use both upper caps of J. The necessary inequality becomes

    a(κ+τ)<ell(p)+τ(.56c_q+.74s_q).                    (9)

For τ>0 set z=tan((p−q)/2). Since q≤p<p₀,

    z≤sin(p₀−q)/(1+cos p₀)
      =(7/32)c_q−(975/2048)s_q.

The inequality uses monotonicity of sine on the present interval and 1+cos(p−q)≥1+cos p₀. Hence

    .56c_q+.74s_q+z
      ≤(623/800)c_q+(13513/51200)s_q<1,               (10)

because the exact squared norm of these two coefficients is

    1772377553/2621440000<1.

Together with 1−κ=τz and (7), this makes the right side of (9) less than κ+τ. The equal-angle case follows directly from (7).

For the first normal u_q of J, the order q≥p gives a<ell(q)≤ell(p)<1. In the order q≤p, the same strict-support calculation as in Section 4 of the first adjacent-angle theorem gives

    1<A(s_p)c_q+B(s_p)s_q,                            (11)

where

    A(S)=1.26−S+.74S²,
    B(S)=sqrt(1−S²)(1−.74S)−.56.

For S≥s₁, A(S)−1=.74(S−1)(S−13/37)<0, and A(S)>0. If B(S)≤0, (11) already fails. Otherwise B is strictly decreasing, B(2/3)<0, and A is positive and decreasing on [s₁,2/3]. Thus A²+B² decreases wherever B≥0. At S=s₁ the exact values are

    A(s₁)=4161/4225, B(s₁)=424/4225,
    1−A(s₁)²−B(s₁)²=2112/105625>0.                   (12)

Cauchy–Schwarz contradicts (11). Every separating source has failed. Therefore all four central angles satisfy

    0<p<p₁,     c>12/13,     s<5/13,     c+s<17/13.   (13)

## 4. The actual boundary angle has absolute half-angle less than 1/3

Put h=cos|β|, b=sin|β|, so h≥b≥0. Only actual B–C disjointness is used in this section.

Orient a proposed separator from B toward C. The strict difference T−(1.74,1)=(0,1) gives n_y>0. The strict difference L₀−A_B=(−1,.686) gives n_x<.686n_y. Consequently neither direction of C's first normal can separate, and the only C-supplied possibility is v_C=(−s,c).

### 4.1. A positive boundary angle

Suppose β≥β₁:=2 arctan(1/3). Then h≤4/5, b≥3/5 and β>p. The only B-supplied possibility is v_B=(−b,h); its first normal has n_x/n_y≥1 and is excluded by the cone above.

Put κ=cos(β−p), τ=sin(β−p)>0. The exact lower C support in direction v_B is

    lower_C(v_B)=−τ(U+a)+κV.

Use strict T and the D cap in (2), and compare with the strict actual boundary point L'. A necessary separating inequality is

    aκ<h+.44b−.74cτ.

Since a>1, this requires

    h A+b B>0,
    A=1−c+.74cs,
    B=−.3−s+.74s²=−F,   F=.3+s−.74s²>0.             (14)

However 1−c=s²/(1+c)≤(13/25)s² by (13), and

    A−(3/4)F
      =(1−c)−.225+s(.74c−.75)+.555s²
      ≤−.225−.01s+1.075s²
      ≤−.225+1.075(25/169)
       =−223/3380<0.

As b/h≥3/4, equation (14) is impossible.

For the remaining source v_C, the genuine bottom wall gives center(B)_y≥a(h+b)/2 and the original center condition gives center(B)_x≤2. Since β>p, the exact projection width of B in direction v_C is a[cos(β−p)+sin(β−p)]. Therefore

    upper_B(v_C)≥−2s+a[(c−s/2)h+(c+s/2)b].

Compare with lower_C(v_C)=V≤2c−s−a. A necessary condition, weakened using a>1, is

    (c−s/2)h+(c+s/2)b≤2c+s−1.                       (15)

The left side is a positive linear combination of cos β and sin β. It is concave on [β₁,π/4], so its minimum is attained at an endpoint. At β₁ its excess above the right side of (15) is

    1−.6c−1.1s≥3/130>0.

The comparison follows because .6c+1.1s increases on 0≤p≤p₁ and takes the value 127/130 at p₁. At π/4 the excess is

    1−(2−sqrt(2))c−s>1−.6c−s≥4/65>0.

Thus (15) fails at both endpoints and throughout the interval. We have proved β<β₁.

### 4.2. A negative boundary angle

Suppose β=−γ with γ≥β₁. Its frame is u_B=(h,−b), v_B=(b,h). The normal v_B has n_x/n_y=b/h≥3/4>.686, so the strict cone already excludes it. Among the B-supplied normals only −u_B=(-h,b) remains.

Put

    α=sin(p+γ)=bc+hs>0,
    Δ=cos(p+γ)=hc−bs>0.

The positivity follows from p<p₁ and γ≤π/4. Since −u_B=−Δu_C+αv_C, strict T and the D cap imply

    lower_C(−u_B)<−h+2b−.74cΔ−aα.

The strict B point L' gives upper_B(−u_B)>−1.44h+b. A separator would therefore require

    aα+.74cΔ<.44h+b.

Dropping a to one produces the necessary inequality

    h F+b G<0,
    F=.3+s−.74s²,
    G=c−.74cs−1≤0.                                    (16)

Because b≤h,

    hF+bG≥h(F+G)=h[(c+s)(1−.74s)−.7]>0.

For the final strict sign one may use the weaker bounds c>.9, s<.42 from (4):

    (c+s)(1−.74s)>(.9+s)(1−.74s)
      =.9+s(.334−.74s)>.9.

This contradicts (16).

For the remaining source v_C, the same real wall and actual center condition give

    upper_B(v_C)≥−2s+a[(c+s/2)h+(c−s/2)b].

Indeed the projection width is a[sin(p+γ)+cos(p+γ)]. The necessary condition is now

    (c+s/2)h+(c−s/2)b≤2c+s−1.                       (17)

Again the left side is concave on [β₁,π/4]. At β₁ its excess is

    1−.6c−.9s≥1/10>0,

and at π/4 its excess is the same positive expression as in Section 4.1. Thus (17) fails. Negative β cannot satisfy γ≥β₁ either.

We have proved

    |tan(β/2)|<1/3,     H_B:=h+b<7/5                 (18)

for every actual boundary, without assuming P belongs to it.

## 5. The sharper wall-owned point

Use the genuine wall reach argument of Section 2 of `C981-RETAINED-CONTINUOUS-LEMMAS.md`, with its elementary constant improved using (18). Here is the full constant change and its application.

In coordinates (X,Y)=(y,4−x), the actual B lies in X≥0 and strictly owns (.914,2) and (1,2.4). The next actual central supplies the two excluded points (1,1.74) and (1.74,2). Reindex B with a nonnegative frame (l,h), l>0,h≥0. Its sum H=l+h equals H_B<7/5. Its lower bands satisfy the genuine left-wall inequality

    lU−h(V+a)≥0.                                       (19)

Set

    w=d₀=1.74,   z=w+5/6=193/75.

The excluded point (1,w) already has both upper bands strict; it must satisfy U≥l+wh or V≥−h+wl. The excluded point (d₀,2) has the lower u-band and upper v-band strict; it must satisfy U+a≤d₀l+2h or V≥−d₀h+2l.

The target (1,z) has both lower bands strict by the owned (1,2.4). If U≥l+wh, the first alternative for (d₀,2) would imply

    a≤(d₀−1)l+(2−w)h<1,

because (d₀−1)²+(2−w)²=.6152<1. Thus V≥−d₀h+2l. The two upper target bands follow from

    (z−w)h≤5/6<1<a,
    (z−2)l+(d₀−1)h<1<a,

the latter using the exact squared coefficient norm 19717/22500<1.

If instead V≥−h+wl, the upper v target band follows from (z−w)l≤5/6<1<a. Were the upper u band to fail, U+a≤l+zh together with (19) would give

    1+(z−w)lh≥a(l+h)>l+h.

But

    H−1=2lh/(H+1)≥(5/6)lh=(z−w)lh

by H<7/5, a contradiction. This includes h=0. Every target band is strict, so returning to the original chart proves

    L''=(107/75,1) belongs strictly to the actual B.  (20)

## 6. The actual central center is above y=1.5

The point L'' is outside C. Its lower u-band is strict by L₀ because

    u(L'')−u(L₀)=(32/75)c−.6s>0

under tan p<5/12. Its upper u-band is strict by M and its upper v-band by U₀. Thus

    V≥c−(107/75)s.                                    (21)

Combine (21) with U≥c+s from (3). For the actual center C₀,

    (C₀)_y=s(U+a/2)+c(V+a/2)
      ≥1−(32/75)cs+a(c+s)/2
      >1−(32/75)cs+(c+s)/2
       =1.5+cs[1/(1+c+s)−32/75].                     (22)

Here c+s≤17/13, so the bracket is at least

    13/30−32/75=1/150>0.

Consequently (C₀)_y>1.5.

## 7. The strict central crosspoint and the other center coordinate

Consider X=(1.5,2). Its lower u-band is strict by L₀, since the projection difference is .5c+.4s>0. Its upper u-band is strict by T. Its lower v-band is strict by M, with difference .15s+.35c>0.

It remains to check upper v. Write C₀=(x,y). The upper-u cap at E=(2,1.74) and (22) give

    cx+sy≤2c+1.74s−a/2,      y>1.5.

Consequently

    v(X)−v(C₀)
      <.5(c+s)+.24s²/c−as/(2c).

The deficit of the right side from a/2 is

    [a(c+s)−c(c+s)−.48s²]/(2c)>0.                    (23)

Indeed, with H=c+s,

    H(1−c)=s²H/(1+c)≥s²/2,

and a>1 makes aH−cH−.48s² strictly positive. Hence X's upper v-band is strict as well. This proves X is strictly owned by the actual C.

Apply this conclusion simultaneously in all sectors. The next actual central's strict X becomes the genuine foreign point E'=(2,1.5) in the present chart. At E' the lower u-band is strict by M, with difference .35c−.15s>0, and the upper v-band is strict by T. A lower-v exit would oppose D and imply

    a≤v(D)−v(E')=.5c+s≤11/13<1.

Thus E' must exit through the upper u-face:

    U+a≤2c+1.5s.                                      (24)

Equations (22) and (24) finally give

    c(C₀)_x+s(C₀)_y≤2c+1.5s−a/2,
    (C₀)_x<2−a/(2c)<1.5.

This completes all assertions of Theorem 1. The proof keeps every actual normal source, allows weak tangencies throughout, and obtains strict ownership only from strict band comparisons. ∎

## 8. Scope of the bootstrap

Together with the all-positive D-exclusion theorem, this is an unconditional entrance theorem for the actual all-positive last C1092 assignment. It applies whether or not any P=(2,1) belongs to its boundary square. The central quadrants, sharper central and boundary angle bounds, and new owned points are conclusions of the actual geometry.

This chapter does not yet prove the central radius-1/sqrt(2) disk for positive squares which own H=(1,1.5), nor the smaller half-angle 7/64 used by the earlier positive-cycle theorem. A final actual B–next-central support argument is still needed for that ending.

## 9. Sharper negative boundary angles once P is owned

**Theorem 2.** Under Theorem 1's hypotheses, suppose the actual B also strictly owns P=(2,1). If its canonical angle is negative, then

    |tan(β_B/2)|<1/8.                                  (25)

**Proof.** Put β_B=−γ, h=cos γ, b=sin γ, and suppose γ≥γ₀:=2 arctan(1/8), so b/h≥16/63. We may retain the weaker central bounds c>9/10, s<21/50 from (4). As in Section 4.2, the only possible sources are −u_B, v_B and v_C. The source −u_B was excluded there for every 0≤γ≤π/4, independently of its assumed lower bound.

For v_B=(b,h), set α=sin(p+γ), Δ=cos(p+γ), both positive. Then

    lower_C(v_B)=αU+ΔV
      ≤α(2c+1.74s−a)+Δ(2c−s−a).

But upper_B(v_B)>v_B(P)=2b+h. Dropping a to one gives the necessary inequality

    hF+bG>0,
    F=(1−c)(1−s)−.26s²<.1,
    G=−c+s−s²−.26cs<−.48.

It follows that

    F+(b/h)G<.1−.48(16/63)<0,

a contradiction.

For v_C, the exact wall support gives the necessary condition (17). Its left side is concave on γ₀≤γ≤π/4. At γ₀, where (h,b)=(63/65,16/65), its excess above the right side is

    1−(51/65)c−(83/130)s.

The subtracted expression increases with p up to p₀=2 arctan(7/32). At that endpoint its deficit from one is exactly

    1428/69745>0.

At γ=π/4, the excess is

    1−(2−sqrt(2))c−s>1−.6c−s≥40/1073>0,

again using p≤p₀ for the last bound. Thus (17) fails at both endpoints and throughout the interval. Every source has been excluded, so γ<γ₀. ∎

The all-P theorem, when supplied by the actual completed H-to-P composition, therefore upgrades the negative boundary branch of (18) to (25). This refinement makes no claim about a positive boundary angle.
