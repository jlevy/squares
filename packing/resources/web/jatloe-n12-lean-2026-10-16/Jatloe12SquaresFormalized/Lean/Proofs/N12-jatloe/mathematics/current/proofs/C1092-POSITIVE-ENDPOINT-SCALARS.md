# C1092: continuous scalar estimates at the positive-boundary endpoints

All constants in this chapter are exact rationals. This is a scalar theorem on full closed parameter domains. Its application to actual squares must use the actual support combinations and source directions in the adjoining geometric chapter. No angle sampling, angular subdivision, or center enclosure is used in the proof below.

## 1. Notation and the estimates supplied

Put

    0≤x,y≤1/5, p=2 arctan x, q=2 arctan y,
    c=(1−x²)/(1+x²), s=2x/(1+x²),
    d=(1−y²)/(1+y²), t=2y/(1+y²),
    κ=cd+st=cos(q−p), σ=ct−sd=sin(q−p),
    H_p=c+s, H_q=d+t,
    H_delta=(1+κ+|σ|)/2,
    f(x)=(1−c)(2c−1)/c.

The target on an edge is

    T(x,y)=f(x)−(y−x).                                (1)

The notation E_CC(p), for example, means the exact scalar support combination with the central supplying both normals and the boundary angle set to p. The first letter specifies the B–C vertical source; the second specifies the B–J horizontal source. The formulas are stated explicitly below, so the theorem is independent of any naming convention in earlier chapters.

**Theorem 1.** On the ascending triangle 0≤x≤y≤1/5,

    E_CC(p)≥T(x,y),
    E_BC(0)≥E_CC(p),
    E_BC(q)−H_q(1−κ)/(dκ)≥E_CC(p).                  (2)

On the descending triangle 0≤y≤x≤1/5,

    E_BC(q)−H_q(1−κ)/ω_B≥T(x,y),
    E_BC(0)≥E_BC(q)−H_q(1−κ)/ω_B,
    E_CB(p)≥T(x,y),                                  (3)

where ω_B=c/(1+σ)>0. In particular all the unmodified endpoint expressions in (2)–(3) satisfy the target. The strengthened BC estimates retain the full quadratic slack H_q(1−κ) before division by their positive potential coefficient; this slack is available to the boundary–boundary comparison.

At equal central angles the appropriate formulas agree. Every denominator remains strictly positive at the closed endpoints x=0 or y=0. In the actual positive sector x>0, the function f(x) is strictly positive because c≥12/13>1/2.

## 2. The exact endpoint formulas

On x≤y, define λ_A=(d−s)/κ. Then

    E_CC(p)=
      [d+sH_delta+κH_p/2+λ_A H_delta−2κ
       −λ_A(H_p−1/2)−λ_Aσ(H_q−1/2)]/d.              (4)

For E_BC(q) on this same triangle, put

    λ_Q=(dκ−t)/κ, I_Q=dσ+λ_Q, J_Q=λ_Qσ.

Its formula is

    E_BC(q)=
      [dH_delta+t+H_q/2+λ_Q H_delta−2
       −I_Q(H_p−1/2)−J_Q(H_q−1/2)]/(dκ).           (5)

Finally put λ_0=dc/κ and I_0=−ds+λ_0. The zero-boundary endpoint is

    E_BC(0)=
      [d(1+H_p/2)+λ_0 H_delta−2d
       −I_0(H_p−1/2)−λ_0σ(H_q−1/2)]/(dc).          (6)

On y≤x, put

    λ_B=(dκ−t)/(1+σ), ω_B=t+λ_B=c/(1+σ),
    I_B=dσ+λ_Bκ=(d−s)/(1+σ).

The descending BC endpoint is

    E_BC(q)=
      [dH_delta+t+H_q/2+λ_B H_delta−2
       −I_B(H_p−1/2)]/ω_B.                          (7)

For the descending zero-boundary endpoint put

    λ_Z=dc/(1+σ), I_Z=d(d−s)/(1+σ).

Then

    E_BC(0)=
      [d(1+H_p/2)+λ_Z H_delta−2d
       −I_Z(H_p−1/2)]/λ_Z.                          (8)

For E_CB(p), put

    λ_C=(c−sκ)/(1+σ), ω_C=sκ+λ_C.

Its formula is

    E_CB(p)=
      [c+sH_delta+H_p/2+λ_C H_delta−2
       −λ_Cκ(H_p−1/2)−sσ(1+t)/2]/ω_C.              (9)

The last term uses the lower endpoint (1+t)/2 because σ≤0 in (9). All the other displayed center-projection endpoints have nonnegative multipliers and are the upper values H_p−1/2 and H_q−1/2.

The formulas have positive denominators and the required multiplier signs. Indeed c,d,κ≥12/13, s,t≤5/13, |σ|≤5/13, and 1+σ≥8/13. Thus d−s>0, dκ−t>0 and c−sκ>0. The identities for ω_B and I_B follow from κ²+σ²=1 and cκ−sσ=d. These checks include both zero central angles.

## 3. The ascending central–central endpoint

Put δ=y−x≥0. Direct substitution in (4) gives the exact identity

    E_CC(p)−T(x,y)=δ P_A(x,δ)/D_A(x,y),              (10)

where

    D_A=(1−x²)(1+x²)²(1−y²)(1+y²)(1+x−y+xy)>0.

The polynomial P_A has the following six coefficients:

    P_A=A₀+A₁δ+A₂δ²+A₃δ³+A₄δ⁴+A₅δ⁵,

    A₀=(1+x²)²(x⁸+4x⁶−8x⁵−26x⁴+20x²−8x+1),

    A₁=(1+x²)(5x⁹−x⁸+20x⁷−28x⁶−50x⁵−10x⁴
                  +20x³−20x²+21x−5),

    A₂=2(1+x²)(5x⁸−2x⁷+15x⁶−18x⁵−15x⁴
                   +3x²−8x+4),

    A₃=2(5x⁹−3x⁸+15x⁷−13x⁶+11x⁵−7x⁴
           −15x³+x²−2),

    A₄=(x−1)(5x⁷+x⁶+11x⁵+3x⁴+11x³+11x²−3x+1),
    A₅=(x−1)²(x+1)(1+x²)².

All identities in this chapter are polynomial identities after multiplying by the displayed denominators. The following bounds on the entire interval 0≤x≤1/5 prove their required signs without subdivision:

    A₀≥1−8x+(94/5)x²,
    A₁≥−5+15x,
    A₂≥8−18x,
    A₃≥−9/2, A₄≥−1, A₅≥0.                         (11)

For the first bound, the inner polynomial in A₀ exceeds 1−8x+(94/5)x² because their difference is

    x²[6/5−26x²−8x³+4x⁴+x⁶]
      ≥(12/125)x².

Also 1−8x+(94/5)x² decreases on this interval and is at least 19/125>0. Multiplication by (1+x²)² therefore preserves the stated lower bound.

For the next four bounds, expansion followed by deletion of positive terms gives respectively

    A₁+5−15x
      ≥x[6−25x−30x³−30x⁴−38x⁵−30x⁶−29x⁷−x⁹],

    A₂−8+18x
      ≥2x[1−8x²−12x³−18x⁴−20x⁶−2x⁸],

    A₃+9/2
      ≥[1−60x³−28x⁴−52x⁶−12x⁸]/2,

    A₄+1≥x[4−14x−8x⁴−4x⁶].

Each bracket decreases and is strictly positive at x=1/5. The first bracket equals 1362399/1953125 there; the second equals 216373/390625; the third, including division by two, equals 184313/781250; and the last equals 18546/15625. This proves (11).

Since δ≤1/5,

    −(9/2)δ³−δ⁴≥−(47/50)δ².

Consequently P_A is bounded below by the single polynomial

    Q=1−8x+(94/5)x²+(−5+15x)δ+(353/50−18x)δ².       (12)

Set u=5x, v=5δ, w=1−u−v. These three numbers are nonnegative and sum to one because x+δ=y≤1/5. The exact homogeneous identity

    1250Q=
      u²(190u+190v+690w)
      +u(173v²+1750vw+1750w²)
      +v²(353v+1603w)+2500vw²+1250w³              (13)

has only positive coefficients. Its value is strictly positive throughout the triangle. Thus P_A>0, and (10) proves the first estimate in (2), strictly when x<y and with equality at x=y.

## 4. The ascending BC endpoint at zero

The exact difference between (6) and (4) is

    E_BC(0)−E_CC(p)=2x P_0(x,δ)/D_0,

    D_0=(1+x²)²(1−y²)(1−x+y+xy)(1+x−y+xy)>0,
    δ=y−x.

The polynomial P_0 has the compact expansion

    P_0=x(1+x²)⁴
      +2(1+x²)²(2x⁴+3x²−4x+1)δ
      +2(1+x²)(3x⁵+5x³−6x²+2x−2)δ²
      +2(1+x²)(2x⁴+x²+1)δ³
      +x(x+1)²(x²−2x+3)δ⁴.                          (14)

The last two coefficients are nonnegative. The coefficient inside the δ² term is at least −2, since 2x−6x²≥0 here. Also 1−4x+3x²>0. Dropping positive terms therefore gives

    P_0≥(1+x²)[x+2(1−4x+3x²)δ−4δ²]
       ≥(1+x²)[x+(2/5)δ]≥0.                        (15)

For the second step use δ≤1/5−x: the coefficient left after factoring δ is at least

    2−8x+6x²−4(1/5−x)
      =6/5−4x+6x²≥2/5.

This proves the second estimate in (2), including x=0.

## 5. The strengthened ascending BC endpoint at q

The strengthened expression in (2) has the exact difference

    E_BC(q)−H_q(1−κ)/(dκ)−E_CC(p)
      =−2δ(1+xy)P_6(x,y)/D_6,                       (16)

where δ=y−x and

    D_6=(1+x²)²(1−y²)
          (1−x+y+xy)²(1+x−y+xy)²>0.

Write P_6=Σ(j=0,...,6) p_j(y)x^j. Its seven coefficient polynomials are

    p₀=−y⁴−2y²+4y−1,
    p₁=2y⁴+4y³+8y²−4y−2,
    p₂=3y⁴−8y³−10y²+4y+3,
    p₃=−4y⁴−8y³+40y²+8y−4,
    p₄=−3y⁴+24y³+26y²−28y−3,
    p₅=2y⁴+20y³−16y²−20y+6,
    p₆=y⁴−14y²+4y+1.

On the full square 0≤x,y≤1/5, p₀≤−1/5, while p₁,p₃,p₄ are negative. Directly deleting their negative terms gives the respective upper bounds −1028/625, −4/5 and −221/125. The other three coefficient bounds are

    p₂≤2378/625, p₅≤3852/625, p₆≤1126/625.

Consequently

    P_6≤−1/5+2378/15625+3852/1953125+1126/9765625
       =−446489/9765625<0.                           (17)

Equation (16) proves the last estimate in (2), with the entire requested quadratic slack retained.

## 6. The strengthened descending BC endpoint

Put δ=x−y≥0. The exact identity for (7) is

    E_BC(q)−H_q(1−κ)/ω_B−T(x,y)
      =δ P_B(y,δ)/D_B,

    D_B=(1−x²)(1+x²)(1+y²)³>0.                       (18)

The numerator has only five coefficients:

    P_B=B₀+B₁δ+B₂δ²+B₃δ³+B₄δ⁴,

    B₀=(y+1)(1+y²)²(y⁵−y⁴+8y³−y+1),
    B₁=2(y+1)(1+y²)²(2y⁴−2y³+13y²−y−2),
    B₂=2(1+y²)(3y⁶+15y⁴+12y³+5y²+8y+1),
    B₃=2(2y⁷+9y⁵+4y⁴+8y³+6y²+5y+2),
    B₄=(1+y²)³.

The last three coefficients are positive. Set K=(y+1)(1+y²)²>0. Then

    P_B≥K[1−y−y⁴−2δ(2+y+2y³)]
       ≥K[1−y−y⁴−2(1/5−y)(2+y+2y³)]
        =K[1/5+(13/5)y+2y²−(4/5)y³+3y⁴]
       ≥K/5>0.                                      (19)

The first step retains only lower bounds for B₀,B₁; the second uses δ≤1/5−y and 2+y+2y³>0. The final sign holds because 2y²−(4/5)y³≥0. This proves the first inequality in (3), with strict inequality when x>y.

## 7. The descending BC endpoint at zero

The difference between (8) and the strengthened expression in (18) factors as

    E_BC(0)−E_BC(q)+H_q(1−κ)/ω_B
      =2(1−x+y+xy)²
         [(x−y)²+y²+2xy³+x²y⁴]/D_B≥0.              (20)

Every factor has its displayed sign on the whole parameter square. This proves the second inequality in (3) directly, with no additional coefficient estimates.

## 8. The descending CB endpoint at p

The exact expression (9) satisfies

    E_CB(p)−T(x,y)=(x−y)P_C(x,y)/D_C,               (21)

where

    D_C=(1−x²)(1+x²)⁴(1+y²)³(c+sκσ)>0.

Indeed c+sκσ≥c−s|σ|≥131/169>0. Although its definition uses the rational trigonometric expressions, D_C becomes a polynomial after the cancellations already specified in Section 1.

Here is an explicit compact coefficient certificate for P_C. Define

    P_C=1+Σ(j=0,...,10) x^j S_j(y)
           −Σ(j=0,...,10) x^j R_j(y),

with the following nonnegative coefficient polynomials. This table is the full exact numerator identity, not a list of sampled values.

| j | R_j(y) | S_j(y) |
|---|---|---|
| 0 | y⁴+y⁶ | y² |
| 1 | 4 | 6y+8y²+8y³+4y⁴+2y⁵ |
| 2 | 8y | 7+13y²+24y³+9y⁴+8y⁵+3y⁶ |
| 3 | 8+24y²+4y⁵ | 8y+4y³+8y⁴ |
| 4 | 8y+16y³+10y⁴+2y⁶ | 14+6y² |
| 5 | 8+8y⁵ | 44y+36y³+16y⁴ |
| 6 | 22+72y+88y³+2y⁶ | 22y²+42y⁴+8y⁵ |
| 7 | 56y+40y²+36y³+88y⁴ | 24+20y⁵ |
| 8 | 39y²+37y⁴+16y⁵ | 1+24y+16y³+3y⁶ |
| 9 | 4+2y+8y²+12y³+4y⁴+10y⁵ | 0 |
| 10 | (1+y²)³ | 0 |

Because every R_j has nonnegative coefficients, its entire sum is maximized on 0≤x,y≤1/5 at x=y=1/5. Direct rational addition gives

    Σ x^j R_j(y)≤144234680326/152587890625<1.

All S_j are nonnegative, so

    P_C≥8353210299/152587890625>0.                   (22)

This proves the last inequality in (3), strictly when x>y. The coefficient estimate actually holds on the full square; only the endpoint's definition and sign of x−y require the descending triangle.

Sections 3–8 prove every assertion of Theorem 1. The denominators are positive, the diagonal equalities are retained, and the proofs include both zero endpoints. The displayed factorizations and homogeneous identities establish the estimates continuously over the complete domains. ∎
