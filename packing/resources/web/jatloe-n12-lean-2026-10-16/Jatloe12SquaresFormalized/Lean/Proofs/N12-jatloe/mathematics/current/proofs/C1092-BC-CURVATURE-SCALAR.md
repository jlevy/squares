# C1092: a uniform scalar bound for the BC curvature

This chapter supplies a single continuous scalar inequality for the positive-boundary BC support calculation. It is independent of square ownership and does not replace the geometric derivation of that support calculation. Every parameter varies over its full closed interval; no angular subdivision is used.

## 1. Statement

Let

    0≤x,y≤1/5,
    c=(1−x²)/(1+x²), s=2x/(1+x²),
    d=(1−y²)/(1+y²), t=2y/(1+y²),
    κ=cd+st, σ=ct−sd,
    H_p=c+s, H_q=d+t,
    f(x)=(1−c)(2c−1)/c,
    e=y−x−f(x), g_i=H_p−1/2.

For x≤y, set

    H=(1+κ+σ)/2,
    T=(H−g_i−σg_j)/κ,                              (1)

where either

    g_j=H_q−1/2  or  g_j=(1+t)/2.

For y≤x, set

    H=(1+κ−σ)/2,
    T=(H−κg_i−σe)/(1+σ).                           (2)

The two definitions agree when x=y. All denominators are positive: c,d,κ≥12/13 and 1+σ≥8/13.

**Theorem 1.** In every case above,

    T≥5/26,                                        (3)

and

    d[c(1/2+T+e)+s(c+s)]−2t≥34/845>0.              (4)

Consequently a BC scalar whose second derivative at boundary angle zero is

    2t−d[c(1/2+T+e)+s(c+s)]

has second derivative at most −34/845 there, including at x=y=0.

## 2. The lower bound for T

On the full parameter square,

    0≤H_p−1,H_q−1≤4/13,
    0≤f(x)≤11/156.                                 (5)

The first bounds follow because c+s and d+t increase from 1 to 17/13 on these angle intervals. For the last one, write f=3−2c−1/c. Its derivative with respect to c is −2+1/c²<0 for c≥12/13; hence its maximum is f(1/5)=11/156.

Suppose first that x≤y, so σ≥0. The larger of the two possible g_j values is H_q−1/2, since

    (H_q−1/2)−(1+t)/2=d+t/2−1
      =y(1−2y)/(1+y²)≥0.

The value of T is smallest for this larger g_j. With that choice, (1) becomes

    T=1/2−[H_p−1+σ(H_q−1)]/κ.                     (6)

The rotation identities c=dκ+tσ and s=tκ−dσ give

    H_p−1+σ(H_q−1)
      =κ(H_q−1)+(κ−1)+σ(2t−1)
      ≤κ(H_q−1),                                   (7)

because κ≤1 and 2t≤10/13<1. Thus T≥3/2−H_q≥5/26. This covers both possible choices of g_j.

Now suppose y≤x, so σ≤0. Formula (2) becomes

    T=1/2−[κ(H_p−1)+σ(1+e)]/(1+σ).                (8)

The bounds (5) give

    2+e−H_p
      ≥2−1/5−11/156−17/13
       =329/780>0.

Consequently

    κ(H_p−1)+σ(1+e)−(1+σ)(H_p−1)
      =(κ−1)(H_p−1)+σ(2+e−H_p)≤0.                (9)

After division by 1+σ>0, (8) therefore yields T≥3/2−H_p≥5/26. This proves (3) in both orders.

## 3. The curvature margin

Define

    A=c(9/13−x−f(x))+s(c+s).

Using cf(x)=(1−c)(2c−1), s²=1−c² and s−x=cx gives the exact identity

    A−9/13=(1−c)(17/13−c)+c²x≥0.                 (10)

Since 1/2+T≥9/13, e=y−x−f(x), and c≥12/13, it follows that

    d[c(1/2+T+e)+s(c+s)]−2t
      ≥d(A+cy)−2t
      ≥d(9/13+12y/13)−2t
       =[9−40y−9y²−12y³]/[13(1+y²)].              (11)

The numerator on the last line decreases on 0≤y≤1/5 and is at least 68/125. Its positive denominator is at most 338/25. Therefore (11) is at least

    (68/125)/(338/25)=34/845>0.

This proves (4), with a uniform strict margin over the complete parameter domain. ∎
