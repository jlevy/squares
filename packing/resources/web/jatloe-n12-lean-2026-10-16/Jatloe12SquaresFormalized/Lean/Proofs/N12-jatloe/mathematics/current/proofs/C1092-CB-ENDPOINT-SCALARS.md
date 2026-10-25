# C1092: the five remaining central–boundary endpoint scalars

All constants below are exact rationals. This chapter proves scalar inequalities on two full closed triangles. Its use for actual squares requires the geometric support combination that produces the stated endpoint; no geometric source or multiplier sign is inferred here. The proof uses polynomial expansion and inequalities on one interval, without sampling or subdivision.

## 1. Exact endpoint definitions and result

For 0≤x,y≤1/5 put

    c=(1−x²)/(1+x²), s=2x/(1+x²),
    d=(1−y²)/(1+y²), t=2y/(1+y²),
    κ=cd+st, σ=ct−sd,
    H_p=c+s, H_q=d+t,
    f(x)=(1−c)(2c−1)/c,
    T(x,y)=f(x)−(y−x).

The letters U and L in this chapter specify which value of the second central projection is substituted:

    G_U=H_q−1/2, G_L=(1+t)/2.

The boundary half-angle β is either 0 or 1/3. Set

    h=(1−β²)/(1+β²), b=2β/(1+β²),
    D=ch+sb, B=s(dh+tb), G=s(th−db).

The two boundary support values are

    β=0:   H_pb=(1+c+s)/2, H_qb=(1+d+t)/2;
    β=1/3: H_pb=(5+7c−s)/10, H_qb=(5+7d−t)/10.

In either case define

    S₀=hH_pb+sH_qb+D(h+b)/2.

On the ascending triangle x≤y use

    λ=(h−B)/κ, ω=h,
    I=λ, J=G+λσ, H_delta=(1+κ+σ)/2.

On the descending triangle y≤x use

    λ=(h−B)/(1+σ), ω=B+λ,
    I=λκ, J=G, H_delta=(1+κ−σ)/2.

For ε equal to U or L, the exact endpoint expression is

    E_β,ε=[S₀+λH_delta−2D−I(H_p−1/2)−JG_ε]/ω.     (1)

These are precisely the CB expressions: the first supplying normal has angle p=2 arctan x, and the second has the boundary angle 2 arctan β. In particular the vanishing first cross term has already been removed in (1).

**Theorem 1.** The following five inequalities hold:

| Domain | Boundary half-angle | Projection value | Conclusion |
|---|---:|---|---|
| 0≤x≤y≤1/5 | 0 | U | E_0,U≥T(x,y) |
| 0≤y≤x≤1/5 | 0 | U | E_0,U≥T(x,y) |
| 0≤x≤y≤1/5 | 1/3 | U | E_1/3,U>T(x,y) |
| 0≤x≤y≤1/5 | 1/3 | L | E_1/3,L>T(x,y) |
| 0≤y≤x≤1/5 | 1/3 | L | E_1/3,L>T(x,y) |

For β=0 the inequality is strict except at x=y=0, where equality holds. Both angle-order boundaries, both zero-angle boundaries, and x=1/5 or y=1/5 are included.

## 2. Positive denominators and polynomial normalization

The half-angle formulas give

    c,d,κ≥12/13, 0≤s,t≤5/13, |σ|≤5/13.

Thus κ>0 and 1+σ≥8/13>0. The ascending potential coefficient is ω=h>0. On the descending triangle write ρ=b/h, so ρ is 0 or 3/4. Then

    ω=h[1+s(d+ρt)σ]/(1+σ)>0,                       (2)

because d+ρt≤√(1+ρ²)≤5/4 and consequently

    1+s(d+ρt)σ≥1−125/676=551/676>0.

Define the positive polynomial factors

    C=(1−x²)(1+x²)(1+y²),
    A=C(1−x+y+xy)(1+x−y+xy),

    Q_ρ=(1+x²)²(1+y²)²
         +4x(1−y²)(y−x)(1+xy)
         +8ρxy(y−x)(1+xy),
    D_ρ=CQ_ρ.

Indeed

    Q_ρ=(1+x²)²(1+y²)²[1+s(d+ρt)σ],                (3)

which proves positivity of D_ρ. The two linear factors in A are each at least 4/5. Every denominator used below is therefore strictly positive throughout its stated closed domain.

Let r denote the smaller half-angle and z the nonnegative half-angle difference:

    ascending:  r=x, z=y−x;
    descending: r=y, z=x−y.

In either case r,z≥0 and r+z≤1/5. Define five numerator polynomials by the following exact identities:

| Name | Domain and expression | Exact identity |
|---|---|---|
| N_A0 | ascending, β=0, U | E_0,U−T=N_A0/A |
| N_D0 | descending, β=0, U | E_0,U−T=N_D0/D_0 |
| N_AU | ascending, β=1/3, U | E_1/3,U−T=N_AU/(5A) |
| N_AL | ascending, β=1/3, L | E_1/3,L−T=N_AL/(10A) |
| N_DL | descending, β=1/3, L | E_1/3,L−T=N_DL/(10D_3/4) |

Here each numerator is expressed in r,z by the preceding substitution. Substitution in (1) and collection of powers of z give degree five for the three ascending numerators and degree nine for the two descending numerators. The remaining proof supplies continuous lower bounds for all their coefficients and then groups powers of z using r+z≤1/5.

## 3. Coefficient bounds on the whole interval

Write each numerator as N=Σ p_j(r)z^j. The following table contains all bounds required in the proof. An empty position means that the coefficient is zero because the degree is five.

| j | N_A0 | N_D0 | N_AU | N_AL | N_DL |
|---:|---|---|---|---|---|
| 0 | (7/2)r² | (7/2)r² | 18/25 | 36/25 | 4−14r |
| 1 | 1−4r−3/50 | 1+4r−23r²−27r⁴ | 5−31r | 10−48r | −12 |
| 2 | −4 | −2−13r | −21 | −20−37r | 0 |
| 3 | 0 | 0 | 0 | 0 | −6 |
| 4 | 0 | 0 | −3 | −5 | 0 |
| 5 | −1 | −3/5 | −5 | −10 | −40 |
| 6 |  | −12 |  |  | −210 |
| 7 |  | −8 |  |  | −74 |
| 8 |  | 0 |  |  | 0 |
| 9 |  | 0 |  |  | 0 |

Every entry is a lower bound valid for every 0≤r≤1/5. We verify the table explicitly next. Terms described as deleted in these verifications have nonnegative coefficients; their deletion therefore gives a lower bound on this interval.

### 3.1. The five constant coefficients

The exact constant coefficients use only three short polynomials:

    q₀=r⁶−2r⁵+r⁴+8r³+3r²−6r+3,
    q₁=2−r+22r²−r³−37r⁴−24r⁵+3r⁶−4r⁷,
    q₂=4−2r+29r²+23r³−49r⁴−73r⁵−4r⁶−8r⁷.

Direct expansion of (1) at z=0 gives

    N_A0: p₀=2r²(1+r²)q₀,
    N_D0: p₀=2r²(1+r²)³q₀,
    N_AU: p₀=(1−3r)(1+r²)q₁,
    N_AL: p₀=(1−3r)(1+r²)q₂,
    N_DL: p₀=(1−3r)(1+r²)³q₂.                      (4)

On the full interval,

    q₀≥3−6/5−2/3125=5623/3125>7/4.

Also q₁≥2−r and q₂≥4−2r. To check these last two statements, it is enough respectively to observe

    r+37r²+24r³+4r⁵≤1/5+37/25+24/125+4/3125<22,

    49r²+73r³+4r⁴+8r⁵
      ≤49/25+73/125+4/625+8/3125<29.

The omitted terms 3r⁶ in q₁ and 23r³ in q₂ are nonnegative. Since 1−3r≥2/5, (4) gives all five constant-coefficient bounds. For the last one use

    (1−3r)(4−2r)=4−14r+6r²≥4−14r.

### 3.2. The first two coefficients of N_A0

Expansion and deletion of nonnegative terms give

    p₁≥1−4r−r²−10r⁴−23r⁸−r¹⁰
       ≥1−4r−3/50,

    p₂≥−4+r(8−4r²−44r⁶−4r⁸)≥−4.                 (5)

For the first bound, 1/25+10/625+23/390625+1/9765625<3/50. The bracket in the second line is positive even after r is replaced by 1/5 in each subtracted term.

### 3.3. The first two coefficients of N_D0

The exact first coefficient is

    p₁=(1+r²)²[1+4r−23r²+52r³−26r⁴+12r⁵
                    +102r⁶+44r⁷−23r⁸+16r⁹+r¹⁰].

The bracket is at least 1+4r−23r²−27r⁴, since 23r⁸≤r⁴. This latter polynomial is at least

    1−(3/5)r−27r⁴≥1−3/25−27/625>4/5>0.

Multiplying it by (1+r²)²≥1 preserves its lower bound. This proves the table's p₁ entry.

For the second coefficient, deletion of nonnegative terms gives

    p₂≥−2(1+r²)(1+5r+26r³+19r⁹)≥−2−13r.           (6)

For the last inequality, expand the expression being subtracted. Beyond 2+10r, its terms are

    2r²+62r³+52r⁵+38r⁹+38r¹¹
      =r(2r+62r²+52r⁴+38r⁸+38r¹⁰)≤3r,

because the bracket is less than 3 at r=1/5.

### 3.4. The first two coefficients at β=1/3 on the ascending triangle

For N_AU, expansion and deletion give

    p₁≥5−17r−63r²−78r⁴−87r⁸−5r¹⁰≥5−31r,

    p₂≥−20−92r³−72r⁴−178r⁷−20r⁹≥−21.             (7)

For the first line use 63r+78r³+87r⁷+5r⁹<14; for the second use 92/125+72/625+178/78125+20/1953125<1.

For N_AL the corresponding estimates are

    p₁≥10−29r−66r²−105r³−116r⁴−87r⁵−14r⁸−10r¹⁰
       ≥10−48r,

    p₂≥−20−30r−64r³−474r⁴−56r⁷−40r⁹
       ≥−20−37r.                                   (8)

The last steps follow from

    66/5+105/25+116/125+87/625+14/78125+10/1953125<19,

    64/25+474/125+56/15625+40/390625<7.

### 3.5. The first two coefficients of N_DL

The exact first coefficient is (1+r²)² times

    −12+43r−166r²+131r³+114r⁴+45r⁵+128r⁶
        +1749r⁷+70r⁸+192r⁹+10r¹⁰.

Since 43r−166r²≥(49/5)r, we obtain

    p₁≥−12−24r²−12r⁴+(49/5)r
       ≥−12+r(49/5−24/5−12/125)≥−12.              (9)

For the second coefficient deletion of nonnegative terms gives

    p₂≥(1+r²)(8−84r+341r²−160r⁵−406r⁷)>0.          (10)

Indeed

    8−84r+341r²=341(r−42/341)²+964/341>2,

whereas 160r⁵+406r⁷≤160/3125+406/78125<1.

### 3.6. All remaining coefficients

The following short lower expressions result from expansion and deletion of nonnegative terms. They give all the remaining entries of the table in Section 3.

For N_A0:

    p₃≥4−4r−12r⁵−34r⁶−6r⁸>0,
    p₄=2r²(1−r²)(2r³−r²+6r+3)≥0,
    p₅=−(1−r²)²(1+r²)≥−1.                         (11)

The last bound uses (1−r²)²(1+r²)=1−r²−r⁴+r⁶≤1.

For N_D0, p₃,p₈,p₉ have nonnegative coefficients, and

    p₄≥2(1+9r−20r²−8r⁴)≥0,
    p₅≥2(3−14r−11r²−6r³)≥−3/5,
    p₆≥−6−30r≥−12,
    p₇≥−8.                                         (12)

For N_AU:

    p₃≥20−20r²−11r⁵−142r⁶−30r⁸>0,
    p₄≥−2−12r⁴≥−3,
    p₅≥−5.                                         (13)

Here p₄=(1−r²)(20r⁵−12r⁴+53r³+34r²+7r−2). Its displayed lower bound is valid whether the bracket is negative or nonnegative. The expression p₅ is five times the p₅ in (11).

For N_AL:

    p₃≥r(35−234r²−44r⁵−60r⁷)≥0,
    p₄≥−4(1+3r²+6r⁴)≥−5,
    p₅≥−10.                                        (14)

Here p₄=4(1−r²)(10r⁵−6r⁴+9r³−3r²+r−1); the same sign observation proves its lower bound. The expression p₅ is ten times the p₅ in (11).

Finally, for N_DL:

    p₃≥−6+r²(306−1150r²−3350r⁴−636r⁶)≥−6,
    p₄≥12+r(290−159r−1950r²−4990r⁴−670r⁶)≥0,
    p₅≥82−275r−1468r²−231r³−3518r⁴≥−40,
    p₆≥−88−532r−137r²−1154r³≥−210,
    p₇≥−74+149r−70r²≥−74,                          (15)

and p₈,p₉ have nonnegative coefficients. Each final scalar inequality in (11)–(15) follows on the whole interval by bounding a subtracted monomial r^j by 5^(−j); in the two bracketed expressions in (15), this gives respectively a positive number and a number greater than 172. No restriction to an open interval is used.

## 4. Grouping the ascending numerator at zero

The first column of the coefficient table gives

    N_A0≥(7/2)r²+z[1−4r−3/50−4z−z⁴].

Since r+z≤1/5 and z⁴≤1/625,

    N_A0≥(7/2)r²+(173/1250)z≥0.                    (16)

The right side is positive unless r=z=0. Thus the first inequality of Theorem 1 holds, with precisely the stated possible equality.

## 5. Grouping the descending numerator at zero

First group the linear and quadratic powers of z. Their coefficient table entries imply

    p₁+zp₂
      ≥1+4r−23r²−27r⁴−(1/5−r)(2+13r)
       =3/5+(17/5)r−10r²−27r⁴
      ≥3/5.                                        (17)

For the last step factor the nonconstant terms as

    r(17/5−10r−27r³)≥0.

The remaining possibly negative coefficients give

    N_D0≥(7/2)r²
           +z[3/5−(3/5)z⁴−12z⁵−8z⁶]
         ≥(7/2)r²+(9292/15625)z
         ≥(7/2)r²+(59/100)z≥0.                     (18)

Again equality is possible only at r=z=0. This proves the second inequality.

## 6. The upper projection at β=1/3 on the ascending triangle

The coefficient table gives

    N_AU≥18/25+z[5−31r−21z−3z³−5z⁴].

Because r+z≤1/5,

    5−31r−21z−3z³−5z⁴
      ≥5−31/5−3/125−5/625=−154/125>−5/4.

Consequently

    N_AU≥18/25−(5/4)z≥47/100>0.                    (19)

This proves the third inequality, including both ends of the ascending triangle.

## 7. The lower projection at β=1/3 on the ascending triangle

Here 20+37r≤20+37/5<48. Hence

    p₁+zp₂≥10−48r−(20+37r)z
            ≥10−48(r+z)≥2/5.

The table therefore yields

    N_AL≥36/25+z[2/5−5z³−10z⁴]
         ≥36/25+(43/125)z>0.                        (20)

This proves the fourth inequality. In particular either projection endpoint is valid for the ascending β=1/3 scalar estimate; the geometric chapter may select the one dictated by its multiplier.

## 8. The lower projection at β=1/3 on the descending triangle

Finally the last column of the table gives

    N_DL≥4−14r−12z−6z³−40z⁵−210z⁶−74z⁷.

Since 4−14r−12z≥4−14(r+z)≥6/5 and z≤1/5,

    N_DL≥6/5−6/125−40/3125−210/15625−74/78125
         =87876/78125>1>0.                          (21)

This proves the fifth inequality and completes Theorem 1. All denominator, coefficient, and grouping estimates hold on the full closed parameter domains, so zero angles, equal angles, and endpoint tangencies in any subsequent geometric application require no limiting argument.
