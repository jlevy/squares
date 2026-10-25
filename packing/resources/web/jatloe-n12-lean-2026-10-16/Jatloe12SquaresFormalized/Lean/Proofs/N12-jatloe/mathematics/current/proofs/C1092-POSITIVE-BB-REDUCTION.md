# C1092: the positive boundary–boundary source reduces to two central-angle endpoints

This is a continuous reduction of the BB source case in the actual positive C1092 cycle. All constants are exact rationals. It uses the proved entrance 0<tan(p/2),tan(q/2)<1/5, 0<tan(β/2)<1/3, the actual wall, actual support separations, and the actual center-projection bounds below. It does not sample boundary angles.

## 1. Exact BB support and the two endpoint hypotheses

Let C,J be consecutive actual central squares and B the intervening actual boundary. Suppose B supplies both actual separating normals: v_β separates B from C, and u_β separates B from J. The common side is a>1. Put

    x=tan(p/2), y=tan(q/2),
    c=cos p, s=sin p, d=cos q, t=sin q,
    h=cos β, b=sin β,
    κ=cos(q−p), σ=sin(q−p),
    H_delta=(1+κ+|σ|)/2,
    f(x)=(1−c)(2c−1)/c,
    R₀=y−x−f(x).

Use the actual central projections G_i,L_i and G_j,L_j in their own sector charts. The completed entrance gives

    a/2+s/2≤G_i≤c+s−a/2,
    a/2+t/2≤G_j≤d+t−a/2.                             (1)

Set

    A=h cos(p−β),       B₀=b cos(q−β),
    F=−h sin(p−β),      G=b sin(q−β),
    S=hH(p−β)+bH(q−β)+(h+b)/2,
    H(z)=(1+cos z+|sin z|)/2.

The actual two support inequalities and the physical bottom wall give exactly

    2−A L_i+B₀ L_j+F G_i+G G_j≥aS.                  (2)

For q≥p define

    λ=(A−B₀)/κ, ω=A, I=F+λ, J₀=G+λσ;

for q≤p define

    λ=(A−B₀)/(1+σ), ω=B₀+λ, I=F+λκ, J₀=G.

These arise by adding λ times the actual smaller-angle central separation. In either order,

    ω(L_j−L_i)+I G_i+J₀G_j≥a(S+λH_delta)−2.          (3)

Let

    g_i=c+s−1/2,
    g_j^hi=d+t−1/2,       g_j^lo=1/2+t/2.

For either choice e∈{hi,lo}, define its unit-side scalar numerator

    E_e(β)=S+λH_delta−2−I g_i−J₀ g_j^e+ωR₀.          (4)

The smaller of these two expressions is the correct numerator after maximizing J₀G_j over its interval. At β=p or β=q it coincides with the corresponding CB or BC source, respectively.

**Theorem 1 (two-endpoint reduction).** Suppose the following two bivariate endpoint inequalities hold for the present p,q:

    min_e E_e(p)≥0,                                   (5)
    min_e E_e(q)≥(d+t)(1−κ).                          (6)

Then the actual BB source satisfies

    L_j−L_i>f(x)−(y−x).                               (7)

Hypothesis (5) is exactly the direct CB endpoint at β=p. Hypothesis (6) is the BC endpoint at β=q with the explicit additional slack (d+t)(1−κ). The strengthened endpoint theorem proves these tests separately. The present chapter proves the complete implication (5)–(6) ⇒ (7), including every intermediate boundary angle.

## 2. Positivity of the multipliers

First λ,ω and I are strictly positive on the whole domain. If β≤p, then

    A=h cos(p−β)=[c+cos(p−2β)]/2≥c,
    B₀≤b≤s.

Thus A−B₀≥c−s≥7/13. If β≥p, then A≥h² and B₀≤b, so

    A−B₀≥h²−b≥1−(3/5)²−3/5=1/25>0.

Both denominators defining λ are positive. The assertion for ω follows immediately. If β≥p, F≥0 so I>0. If β≤p, then F≥−s. On an ascending edge λ≥7/13, giving I≥2/13. On a descending edge λ≥7/13 and κ≥12/13, giving I≥19/169.

The upper endpoint g_j^hi is at least g_j^lo, since

    g_j^hi−g_j^lo=d+t/2−1=t(1/2−y)≥0.

Thus I always takes the upper G_i bound in (1), while the sign of J₀ selects the appropriate G_j endpoint. In (3), the resulting coefficient of a is

    S+λH_delta+I/2+|J₀|/2>0.

Dropping a to one therefore gives strictly

    ω[L_j−L_i+R₀]>min_e E_e(β).                       (8)

It is enough to prove that the right side is nonnegative.

## 3. A tangent inequality turns the boundary angle into a concave quadratic

The only part of S which is linear, rather than quadratic, in h,b is h+b. Replace that term by

    (h+b)cos(p−β)≤h+b.

Denote the resulting expression in (4) by \widetilde E_e(β). Its exact loss is

    E_e(β)−\widetilde E_e(β)
      =(h+b)[1−cos(p−β)]≥0.                         (9)

Put ρ=tan β, so 0≤ρ≤3/4. Multiplication by 1+ρ² turns \widetilde E_e into a quadratic in ρ on each interval cut by β=p,q. Indeed

    (1+ρ²)(h+b)cos(p−β)=(1+ρ)(c+sρ),

and every other term is a quadratic combination of h,b. This is the exact tangent bound sqrt(1+ρ²)≥c+sρ, written without radicals.

We prove that each of these quadratics is concave. Put ε_q=sign(q−β), using either adjacent value at an equality. On an ascending edge, the coefficient of ρ² is

    Q₂=s−2+t/2−ε_q d/2+d g_j^e
       −(t/κ)[H_delta−g_i−σg_j^e].                  (10)

The final bracket is positive. Since κ≥12/13, σ≤5/13, c+s≤17/13, and g_j^e≤21/26,

    H_delta−g_i−σg_j^e
      =1+κ/2−(c+s)+σ(1/2−g_j^e)
      ≥6/169>0.                                      (11)

On a descending edge, the quadratic coefficient is instead

    Q₂=s−2+t/2−ε_q d/2+d g_j^e
       −[t/(1+σ)][H_delta−κg_i−σR₀].               (12)

Here σ≤0, R₀≤0, and f(x)≤f(1/5)=11/156. Hence

    H_delta−κg_i−σR₀
      ≥1−21/26−(5/13)(1/5+11/156)
       =179/2028>0.                                  (13)

Consequently, in either order and for either G_j endpoint,

    Q₂≤s−2+t/2+d/2+d(d+t−1/2)
       =s−1+t(1/2+d−t)
      ≤5/13−1+(3/2)(5/13)−25/169
       =−63/338<0.                                   (14)

For the last step, the function (3/2)t−t² increases on 0≤t≤5/13.

Each quadratic is therefore concave. Their pointwise minimum is concave as well: the minimum of concave functions has a convex hypograph. On each of the three boundary-angle intervals cut by p and q, it is enough to check their minimum at the interval endpoints. Thus only

    β=0, p, q, β_max:=2 arctan(1/3)                  (15)

need examination. These are analytic endpoints of three continuous formulas, not angle boxes or sampled cases.

At β=p, (9) has zero loss, so (5) gives the required nonnegativity. At β=q, the loss is exactly (d+t)(1−κ), so (6) gives it. We prove the two remaining endpoints directly below.

## 4. The endpoint β=0

Write

    M=(1−x+y+xy)(1+x−y+xy)>0.

On an ascending edge, J₀=λσ≥0 at β=0, so its minimum uses g_j^hi. Exact substitution into (4) and (9) gives

    \widetilde E_hi(0)
      =(1−x²)(y−x)P_+(x,y)/[(1+x²)²(1+y²)M],         (16)

where

    P_+=1−4y+4y²−y⁴
      +4xy³−4xy²
      +4x²y³+8x²y²+4x²
      +8x³y³−8x³y²+4x³y−4x³
      +x⁴y⁴−x⁴.

Discarding positive terms and bounding the six negative monomials over 0≤x,y≤1/5 proves

    P_+≥1−[4/5+1/625+4/125+4/125+8/3125+1/625]
       =407/3125>0.                                  (17)

On a descending edge, J₀=0 at β=0, so both endpoint choices agree. The exact expression is

    \widetilde E(0)
      =(x−y)P_-(x,y)/[(1+x²)(1−x+y+xy)²],            (18)

where

    P_-=x⁴y²+x⁴+6x³y+4x³+2x²−2xy−4x−y²+1.

Therefore

    P_-≥1−4/5−2/25−1/25=2/25>0.                    (19)

Equations (16)–(19) prove the endpoint sign, including p=q.

## 5. The endpoint β=2 arctan(1/3)

Here ρ=3/4 and β exceeds both central angles. On an ascending edge either G_j endpoint may minimize (4), so both are retained. On a descending edge J₀=b sin(q−β)<0, so only g_j^lo is needed.

Set

    D_+=16(1−x²)(1+x²)²(1+y²)M,
    D_-=16(1−x²)(1+x²)(1+y²)²(1−x+y+xy)².

These denominators are positive. Let N_+^hi,N_+^lo,N_-^lo be the numerators of

    (1+ρ²)\widetilde E_hi=N_+^hi/D_+,
    (1+ρ²)\widetilde E_lo=N_+^lo/D_+,
    (1+ρ²)\widetilde E_lo=N_-^lo/D_-

at ρ=3/4, respectively in the indicated angle orders. The definitions in Sections 1 and 3 determine these polynomials exactly.

The following coefficient bounds give short, uniform proofs of their signs. In the table, an entry is a lower bound for the coefficient of x^j, as a polynomial in 0≤y≤1/5. The coefficients in a column are obtained simply by substituting ρ=3/4 in (4), multiplying by its displayed positive denominator, and collecting powers of x.

| j | Ascending, high endpoint | Ascending, low endpoint | Descending, low endpoint |
|---:|---|---|---|
| 0 | 3+10y−101y² | 3+y−51y² | 3−y−27y² |
| 1 | 18+44y | 18+47y | 20+42y |
| 2 | −96+132y−156y³ | −96+84y | −124 |
| 3 | −312y−328y³ | −256y−240y³ | 0 |
| 4 | −36 | −34 | 0 |
| 5 | 0 | 0 | −68 |
| 6 | 0 | 0 | −116 |
| 7 | −263 | −256 | −25 |
| 8 | 0 | 0 | 0 |
| 9 | 0 | 0 | 0 |

Here are explicit checks of the nonconstant and potentially delicate bounds; they also provide a compact way to verify the coefficient table without a long polynomial listing.

For the ascending high column, the exact coefficients of degrees 0 and 1 are

    3+10y−100y²+106y³−3y⁴−16y⁵,
    18+88y−208y²−40y³+94y⁴−24y⁵.

Their displayed lower bounds follow from 1−3y²−16y³>0 and 44−208y−40y²−24y⁴>0. The coefficients of degrees 2 and 3 equal

    −96+132y+96y²−156y³+256y⁴+32y⁵,
    30−312y+208y²−328y³+50y⁴+24y⁵.

The coefficient of degree 4 is at least 10−216y−312y³−74y⁴>−36, and that of degree 7 at least −254−208y²−24y⁵>−263. The remaining coefficients are nonnegative: their respective lower bounds for degrees 5,6,8,9 are

    190−24y−302y⁴,
    64−96y²−224y⁴−32y⁵,
    19−50y−50y³,
    16(1−y⁴).

For the ascending low column, the first two exact coefficients are

    3+y−50y²+33y³+15y⁴−16y⁵,
    18+80y−144y²−80y³−18y⁴−24y⁵.

The second coefficient's stated bound uses

    33−144y−80y²−18y³−24y⁴>0.

The next two coefficients exceed −96+84y and −256y−240y³, respectively. Degree 4 exceeds 10−198y−28y²−294y³−110y⁴>−34, and degree 7 exceeds −254−48y²−24y⁵>−256. Degrees 5,6,8,9 have the positive lower bounds

    190−16y−190y⁴,
    64−128y²−128y⁴−32y⁵,
    19−59y,
    16(1−y⁴).

For the descending low column, the exact constant coefficient is

    3−y−3y²−100y³−81y⁴−35y⁵−39y⁶+16y⁷,

which is at least 3−y−27y². Its degree-1 coefficient has all positive terms and begins 20+42y. The degree-2 coefficient is at least

    −105−45y−211y²−124y³−65y⁴−143y⁵−16y⁷>−124.

Degree 3 is at least

    64−240y−140y²−336y³−364y⁴−96y⁵−160y⁶>0,

and degree 4 is positive. Degree 5 is at least −68. Degree 6 exceeds −43−347y−17y²−324y³>−116. The degree-7 coefficient is

    −4(1+y²)(4y⁴−6y³+17y²+6y+4)>−25.

All of these endpoint comparisons use only 0≤y≤1/5.

Now combine the table rows using 0≤x≤1/5. In the ascending high column, the positive term (132−312x)y can be discarded. The remaining losses contributing to x² total at most

    96+(156+328/5)/125+36/25+263/3125<100.

In the ascending low column, discard (84−256x)y≥0; the analogous loss is at most

    96+48/125+34/25+256/3125<98.

In the descending low column, the loss is at most

    124+68/125+116/625+25/3125<125.

Consequently the three exact numerator polynomials have the lower bounds

    N_+^hi≥3+18x+10y+44xy−100x²−101y²,
    N_+^lo≥3+18x+y+47xy−98x²−51y²,
    N_-^lo≥3+20x−y+42xy−125x²−27y².                 (20)

Each right side is concave in either variable with the other held fixed. Its minimum on the entire box 0≤x,y≤1/5 therefore occurs at a box vertex. Checking those four vertices gives respectively

    N_+^hi≥24/25,   N_+^lo≥29/25,   N_-^lo≥43/25.   (21)

This proves the final endpoint strictly, on the entire box and hence on both actual angle triangles.

## 6. Completion of the BB reduction

Sections 4–5 establish the two outer endpoints in (15) unconditionally. Hypotheses (5)–(6), together with the exact loss (9), establish the inner endpoints. Section 3's concavity argument now proves min_e \widetilde E_e(β)≥0 for every intermediate positive boundary angle. Since E_e≥\widetilde E_e, inequality (8) proves (7).

This completes the BB source reduction. Only the two explicitly displayed bivariate endpoint inequalities remain to be supplied by the companion endpoint theorem; the whole positive boundary-angle interval and every G_j sign choice are proved here. ∎
