# C976: the actual left pair forces a steep negative top angle

All decimals are exact rationals. The two actual squares have common side a>1. Owned points are strict; excluded points, segments, and separating supports may touch boundaries. The proof treats a whole interval of top angles with two exact support inequalities.

## 1. The local theorem

**Theorem 1.** Let N and W be disjoint open squares of common side a>1. Suppose N has positive canonical frame

    u_N=(l,h), v_N=(−h,l), l≥h>0, l²+h²=1,
    h/l>21/65,

with lower faces U,V and upper faces A=U+a, B=V+a. Suppose

    B≤l, V≥−.27h−.04l,                               (1)

and N strictly owns

    P=(−.086,0), M=(.65,.35), H=(0,.26), Z=(.25,1).

Suppose N excludes the complete segment

    I=[E,F], E=(−.24,−.13), F=(0,−.26).

Suppose W has closure in y≤2, strictly owns

    A0=(.44,1), O=(1,1), P0=(1,1.086),

and excludes T=(1.26,1). Then W cannot have a nonpositive canonical angle whose magnitude satisfies |tan β|≤2/3.

Write such a hypothetical W frame instead as

    u_W=(C,S), v_W=(−S,C),
    C,S≥0, C²+S²=1, 0≤C/S≤2/3.                       (2)

This is the quarter-turned orthonormal frame for the nonpositive canonical angle. In particular S≥4/5, C≤3/5, and C+S≤7/5. Let its lower faces be U_W,V_W and its upper faces A_W,B_W.

First (1) implies

    1<a≤1.04l+.27h,  h/l<8/11.                       (3)

For the angle cap, (1.04+.27τ)/sqrt(1+τ²) decreases when τ≥8/11 and its value at 8/11 is 13.6/sqrt(185)<1. Thus (3) is strict.

Any separating normal oriented from N toward W has positive first component, by A0−Z=(.19,0), and second component greater than (21/65) times its first component, by A0−M=(−.21,.65). Among the actual square-edge normals, only u_N and u_W can meet this cone. We may retain u_W even when C=0; proving that this extra direction fails is harmless.

Put

    α=lC+hS>0, β=lS−hC>0.                            (4)

The strict sign of β follows from h/l<8/11 and S/C≥3/2 when C>0; at C=0 it is immediate.

## 2. The right excluded point is necessarily below W

At T its lower u_W band and upper v_W band follow from O. Thus it exits upper u_W or lower v_W.

Suppose first A_W≤1.26C+S. The W-supplied separator would require U_W≥upper_N(u_W). But

    U_W≤u_W(T)−a<u_W(M),

because |T−M|²=.61²+.65²=.7946<1. This contradicts strict ownership of M by N.

For the N-supplied separator, u_N=αu_W−βv_W, so strict ownership of O by W gives

    lower_W(u_N)<α[u_W(T)−a]−β(C−S)
                   <1.26l+h−α−.26βS.

Strict ownership of M by N then makes separation possible only if

    lF_C+hG_C>0,
    F_C=.35−C+.26C²,
    G_C=.65−S+.26CS.                                (5)

This cannot happen. If C/S≤43/130, then

    u_W(T)−u_W(P0)=.26C−.086S≤0,

contrary to P0 being strict below A_W. Otherwise

    C>43/sqrt(18749)>31/100.

Throughout 31/100≤C≤3/5 one has G_C≤−.0252<0. Moreover F_C+(21/65)G_C decreases with C. Indeed

    F_C'=−1+.52C,
    G_C'=(C+.26−.52C²)/S≤43/40,

so its derivative is at most −4429/13000<0. At C=.31, use S>.95 to get

    F_C+(21/65)G_C
      <.064986−(21/65)(.22343)
       =−23397/3250000<0.

Since h/l>21/65 and G_C<0, this contradicts (5). Both possible separators fail under the upper-u_W alternative. Consequently T must exit lower v_W:

    V_W≥C−1.26S.                                   (6)

The genuine upper wall is

    S(U_W+a)+C(V_W+a)≤2.                            (7)

No artificial wall or center estimate is used in (7).

## 3. The small left-angle part needs only two strict points

First suppose h/l≤1/3. Combining (6)–(7), the lower W-support in direction u_N is strictly less than

    W_*=(2α−l(C+1))/S+1.26l−α.                      (8)

Subtracting the strict N-marker projection .65l+.35h gives

    W_*−u_N(M)
      =l[(C−1)/S+.61−C]+h(1.65−S)
      ≤l[1.16−C−S/(1+C)−S/3]
      ≤−(8/75)l<0.

Here C+S/(1+C)≥1 follows by squaring S/(1+C)≥1−C, and S≥4/5. Thus the u_N separator is impossible.

For the u_W separator, strict ownership of M and Z gives

    upper_N(u_W)>αu_N(M)+βv_N(Z).

Inserting this lower bound in (6)–(7) gives a contradiction as soon as the following expression is positive:

    E0=C+S−1+S²(.4lh−.65h²)
                  −CS(.61+.4h²+.65lh).              (9)

It is uniformly positive. On 21/65<h/l≤1/3,

    .4lh−.65h²
      =l²(h/l)[.4−.65(h/l)]>1/20,
    .61+.4h²+.65lh≤169/200.

For the first bound use l²≥9/10, h/l>8/25, and .4−.65(h/l)≥11/60. The second uses h²≤1/10 and lh≤3/10. Also

    C+S−1=2CS/(C+S+1)≥(5/6)CS.

Therefore

    E0≥−(7/600)CS+(1/20)S²
       ≥−7/1200+4/125=157/6000>0.                  (10)

Both separators are excluded throughout the small left-angle part, including h/l=1/3.

## 4. The actual lower segment gives one support line

It remains to treat h/l≥1/3. Define

    α0=.13l+.24h>0, β0=.24l−.13h>0, δ0=.0624.

We claim that exclusion of the whole actual segment I gives

    α0U+β0V≥−δ0.                                   (11)

At E both upper bands follow from P,H. A lower-v exit would, with B≤l, give a≤1.13l−.24h. This expression decreases with the angle and at h/l=1/3 is 3.15/sqrt(10)<1. Thus E has its lower v band strict and exits lower u.

At F both upper bands follow from M,H. If F exits lower u, combine U≥−.26h with the lower V-bound in (1). Then

    α0U+β0V+δ0
      ≥.0528l²−.0934lh+.0351h²>0.                  (12)

Indeed, after division by l², the quadratic decreases for 0≤h/l≤3/4 and its value at 3/4 is 399/160000>0; (3) lies in that interval.

Otherwise F has its lower u band strict and exits lower v. The segment line is .13x+.24y=−δ0, or α0u+β0v=−δ0. Its endpoints exit through the different lower faces and have their opposite lower bands strict. All their upper bands are strict, and remain strict on the segment. If (11) failed, a nonempty interval between the two lower-face crossings would lie in N, contrary to exclusion of I. Equality in (11) is precisely the permitted lower-corner tangency. This proves the claim in every case.

Since V≤l−a, equation (11) implies the strict lower bound

    A>1+[β0(1−l)−δ0]/α0.                           (13)

## 5. The left-square normal cannot separate

The W-support is still strictly below W_* in (8). Put w=tan(|β|/2); by (2), 0≤w<1/3. The exact expression in (8) becomes

    W_*=.26l+h+[2w²/(1+w²)]
                     [h−l(1−w)/(1+w)].             (14)

For h/l≤1/2, it is at most .26l+h. For h/l≥1/2, it is at most .16l+1.2h, using (1−w)/(1+w)≥1/2 and 2w²/(1+w²)≤1/5.

Multiplying the difference between (13) and the first of these bounds by α0 gives

    f0=.37l+.11h−.3024−.0338l²−.0624lh.

On 1/3≤h/l≤1/2 this decreases with the angle. Its derivative is

    −.37h+.11l+.0676lh−.0624(l²−h²)<0:

the first two terms are nonpositive, lh≤2/5, and l²−h²≥3/5. At h/l=1/2,

    f0=.17sqrt(5)−.3544>49/2500>0.

For h/l≥1/2 the corresponding difference is

    f1=.37l+.11h−.3504+.0272l²−.0644lh.

This also decreases with the angle, since

    f1'=−.37h+.11l−.0544lh−.0644(l²−h²)<0.

At the larger endpoint h/l=8/11 it is

    f1=(99sqrt(185)−1344)/3700>0,

because 99²·185−1344²=6849>0. Thus (13) is strictly larger than the appropriate bound in (14). The u_N separator is impossible on the entire remaining interval.

## 6. The top-square normal cannot separate

Set

    k0=β α0−α β0=.13S−.24C.

Equation (11) gives

    upper_N(u_W)
      ≥a(α+β)+(k0 V−δ0α)/α0.                       (15)

If k0≥0, insert V≥−.27h−.04l. If k0≤0, insert V≤l−a. In either case, combining the resulting bound with the proposed separator U_W≥upper_N(u_W), the real wall (7), and (6), and then lowering a>1 to one, gives respectively the necessary strict inequalities

    E_lo<0 or E_hi<0,                               (16)

where

    E_lo=S[(α+β)α0−δ0α+k0(−.27h−.04l)]
           +α0[C²−1.26CS+C+S−2],

    E_hi=S[(α+β)α0−δ0α+k0(l−1)]
           +α0[C²−1.26CS+C+S−2].                   (17)

The coefficients of a before it was lowered are positive: in the first case it is α0[S(α+β)+C+S], and in the second this same quantity minus Sk0. Thus (16) follows with the stated strictness also at k0=0.

Both quantities in (17) are positive, as proved by the continuous polynomial certificate in Section 7. This excludes u_W and completes the proof of Theorem 1. ∎

## 7. Two bivariate quartics on complete rectangles

This section proves the signs just used and records the entire algebraic certificate. Put

    r=h/(1+l), w=C/(1+S),
    l=(1−r²)/(1+r²), h=2r/(1+r²),
    C=2w/(1+w²), S=(1−w²)/(1+w²).

On the current left-angle range, r>4/25. Equation (3) is equivalent to

    2+27r−102r²>0.

The polynomial decreases for r≥4/25 and equals −127/26569 at r=53/163. Therefore

    4/25≤r≤53/163.                                  (18)

For E_hi its sign condition k0≤0 says C/S≥13/24. Thus w≥1/4. The cap C/S≤2/3 gives w≤(sqrt(13)−3)/2<10/33. For E_lo one has C/S≤13/24 and hence w≤13/50. It suffices to prove

    E_hi>0 on [4/25,53/163]×[1/4,10/33],
    E_lo>0 on [4/25,53/163]×[0,13/50].              (19)

These rectangles cover their respective complete sign domains and are not angle subdivisions.

Let P_hi=10000(1+r²)²(1+w²)² E_hi and similarly define P_lo. Exact substitution in (17) gives the two full polynomial identities

    P_hi=4(w−1)[
       650r⁴w³−4181r⁴w²−3531r⁴w
       −5762r³w³+762r³w²+5086r³w+3362r³
       +1100r²w³+4800r²w²+2600r²w−1100r²
       −2062rw³+2262rw²−814rw−338r
       −650w³+481w²−169w],

    P_lo=2(w−1)[
       2626r⁴w³−2140r⁴w²−3492r⁴w−1326r⁴
       −11875r³w³−123r³w²+9227r³w+7075r³
       +3500r²w³+15700r²w²+8700r²w−3500r²
       −4475rw³+2877rw²−2573rw−325r
       −1326w³+840w²−408w+26].                     (20)

Here is a compact exact coefficient verification for the signs of these quartics. For either rectangle [a,b]×[c,d] in (19), expand

    P(a+(b−a)u,c+(d−c)v)=Σ q_kl u^k v^l,

and define its degree-(4,4) Bernstein coefficients by the rational formula

    B_ij=Σ(k≤i,l≤j) q_kl
                 binom(i,k)binom(j,l)/[binom(4,k)binom(4,l)].

Then the exact polynomial identity is

    P=Σ(i,j=0,...,4) B_ij binom(4,i)binom(4,j)
                  u^i(1−u)^(4−i)v^j(1−v)^(4−j).   (21)

Substitution of the rational endpoints (19) and the explicit polynomials (20) gives the following lower bounds. Each entry bounds all five coefficients in the indicated row, j=0,...,4.

| i | B_ij for P_hi | B_ij for P_lo |
|---:|---:|---:|
| 0 | ≥200 | ≥174 |
| 1 | ≥204 | ≥242 |
| 2 | ≥180 | ≥230 |
| 3 | ≥115 | ≥178 |
| 4 | ≥3/10 | ≥77 |

For clarity, the exact smallest coefficients in the most delicate last row are

    P_hi: 271661855034224/837155581516881>3/10,
    P_lo: 17028128160128427/220597425312500>77.

All these statements are rational coefficient inequalities from the displayed definition of B_ij. They are coefficients of the full continuous polynomial identity (21), not values at sampled angles. Every Bernstein basis function is nonnegative on 0≤u,v≤1 and their sum is one. Hence P_hi≥3/10 and P_lo≥77 throughout their respective rectangles, including their boundaries. The common denominator defining them is positive, so (19) follows.

## 8. Actual C976 application

Use coordinates (x−1,y−2), and take N=Q8 and W=Q11. The completed theorem `C976-LEFT-UPPER-POINTS.md` gives N's strictly positive angle with h/l>21/65, its strict P,M,H,Z, and its two faces (1). The original singleton Q1 strictly owns both endpoints of I, so the whole segment is genuinely excluded from N. The point Z is the newly proved strict point (1.25,3) of Q8.

The actual top square Q11 strictly owns A0=(1.44,3), O=(2,3), and its original marker P0=(2,3.086). Its true box wall is y≤4, which becomes y≤2. The point T=(2.26,3)=G7 belongs strictly to actual Q7 for either of the two remaining northeast labels131200 and131232. Thus every hypothesis of Theorem 1 is supplied by the same actual squares and their established strict hulls.

Consequently, in either remaining C976 pair,

    Q11 nonpositive canonical angle ⇒ |tan β_Q11|>2/3.

This is a continuous obstruction for the actual Q8/Q11 pair. A full C976 contradiction still requires the complementary consequence of its actual northeast/top pair; no such consequence is assumed in this chapter.
