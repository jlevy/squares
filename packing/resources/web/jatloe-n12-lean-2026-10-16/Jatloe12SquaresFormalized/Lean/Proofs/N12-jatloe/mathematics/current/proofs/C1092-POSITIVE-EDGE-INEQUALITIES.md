# C1092: two continuous positive-edge inequalities

This supplies the two scalar inequalities used in
`C1092-POSITIVE-CYCLE.md`. There are two cases, the two possible orders of
consecutive actual central angles. Both polynomial signs below hold on
the entire square of allowed half-angles. Their proofs use direct
coefficient estimates; they require no interval partition, enumeration of
angle bins, or numerical evaluation.

## 1. Definitions and statement

Set

    h=7/64,       A_*=1001/1000,
    c(t)=(1-t^2)/(1+t^2),       s(t)=2t/(1+t^2),
    w(t)=c(t)+s(t),
    f(t)=(1-c(t))(2c(t)-1)/c(t)
        =2t^2(1-3t^2)/[(1+t^2)(1-t^2)].

For `0<=x,y<=h`, abbreviate

    c=c(x), s=s(x), C=c(y), S=s(y), w=c+s, W=C+S,
    kappa=cC+sS,       sigma=cS-sC.

Thus if `p=2 arctan x` and `q=2 arctan y`, then
`kappa=cos(q-p)` and `sigma=sin(q-p)`.

For `x<=y` put

    H_+=(1+kappa+sigma)/2,
    lambda_+=c/kappa-s,

    B_+(x,y)=[(3/2)w+lambda_+ H_+-2
                -lambda_+(w-1/2)
                -c(sigma/kappa)(W-1/2)
                -(5/4)s(y-x)]/c.

For `y<=x` put

    H_-=(1+kappa-sigma)/2,
    lambda_-=(c-s kappa)/(1+sigma),
    omega=s kappa+lambda_-,

    B_-(x,y)=[(3/2)w+lambda_- H_--2
                -lambda_- kappa(w-1/2)
                -s sigma(C+(2/5)S-A_*/2)
                -(A_* s/c+s/6)(x-y)]/omega.

**Two-edge theorem.** Throughout the respective closed triangles,

    B_+(x,y) >= f(x)-(y-x)          if 0<=x<=y<=h,       (1)
    B_-(x,y) >= f(x)+(11/10)(x-y)   if 0<=y<=x<=h.       (2)

Both are strict away from the diagonal `x=y`; on the diagonal their two
sides agree. Also `f(x)>0` for every `0<x<=h`.

Every denominator is positive. Indeed `c>s>=0`, `kappa>0`,
`1+sigma>0`, and therefore `lambda_+`, `lambda_-`, and omega are
positive. These assertions also follow directly from the rational
denominator factorizations in the next section.

## 2. Two polynomial identities with positive denominators

Use the following auxiliary polynomials:

    a_0=1+x^2,       b_0=1+y^2,
    M=(1+xy)^2-(x-y)^2
      =(1-x^2)(1-y^2)+4xy,
    N=2(y-x)(1+xy),
    T=(1-x^2)a_0^2 b_0^2+2xMN.

They give

    kappa=M/(a_0 b_0),       sigma=N/(a_0 b_0),
    T=a_0^3 b_0^2(c+s kappa sigma)>0.                  (3)

For the last sign, `|kappa sigma|<=1` implies
`c+s kappa sigma>=c-s>0`. Also `M>0`, since `x,y<1` and
`x,y>=0`. Consequently

    D_+=2(1-x^2)a_0 b_0 M>0,
    D_-=1500(1-x^2)a_0 b_0 T>0.                       (4)

The following are exact rational identities:

    B_+(x,y)-f(x)+(y-x)=(y-x) P_+(x,y)/D_+,           (5)
    B_-(x,y)-f(x)-(11/10)(x-y)=(x-y) P_-(x,y)/D_-.    (6)

For completeness, the full polynomials in these two identities are given
below as coefficients of powers of x. That is, the entry in row i is
`[x^i]P`, and `P=sum_i x^i [x^i]P`. The identities can be checked simply
by substituting the rational definitions from Section 1, multiplying by
the positive denominators (4), and collecting powers of x and y.

### The ascending polynomial P_+

| i | Coefficient of x^i |
|---:|---|
| 0 | `2-8y+8y^2-2y^4` |
| 1 | `-9+4y-4y^2+4y^3+5y^4` |
| 2 | `2-32y+28y^2-8y^3+2y^4` |
| 3 | `-4-12y-28y^2+12y^3` |
| 4 | `-6-16y-20y^2-32y^3+2y^4` |
| 5 | `13-8y+16y^2-16y^3-5y^4` |
| 6 | `2-2y^4` |

### The descending polynomial P_-

| i | Coefficient of x^i |
|---:|---|
| 0 | `1350+1050y^2-1950y^4-1650y^6` |
| 1 | `-12506-8812y-24915y^2-39218y^3-25512y^4-6406y^5-3503y^6` |
| 2 | `26962-603y+45850y^2+19194y^3-55168y^4-9003y^5-2056y^6` |
| 3 | `-34015+11400y-82242y^2+28782y^3-32439y^4-54618y^5-13012y^6` |
| 4 | `42718-21003y+42724y^2-45606y^3+1688y^4-15003y^5-22318y^6` |
| 5 | `-27015+78206y-27648y^2+95206y^3-9051y^4-7000y^5-18018y^6` |
| 6 | `-25288-119397y+31124y^2-115194y^3+108094y^4+33003y^5-20318y^6` |
| 7 | `33991-83400y-85830y^2-76782y^3-159633y^4+78618y^5-11012y^6` |
| 8 | `3956+45003y-67750y^2+45606y^3-95762y^4-8997y^5-56y^6` |
| 9 | `-8503+2606y-19509y^2-7988y^3-13509y^4-10594y^5-2503y^6` |
| 10 | `-1650-4950y^2-4950y^4-1650y^6` |

## 3. A single coefficient bound proves P_+ positive

Write `P_+=sum a_(ij)x^i y^j`. Its constant term is 2. On
`0<=x,y<=h`, every positive nonconstant monomial can be discarded in a
lower bound, while a negative monomial is at least `a_(ij)h^(i+j)`.
Thus

    P_+(x,y) >=2-sum_(a_(ij)<0) |a_(ij)| h^(i+j).

The coefficient table above gives exactly

    sum_(a_(ij)<0) |a_(ij)| h^(i+j)
       =1104177754213861201/576460752303423488.

It follows that

    P_+(x,y)
      >=48743750392985775/576460752303423488>0.         (7)

This proves the ascending polynomial sign on the whole square. Equations
(4),(5), with `y-x>=0`, prove (1).

## 4. Three coefficient bounds prove P_- positive

Write `P_-=sum b_(ij)x^i y^j`. Retain the two positive monomials
`1350` and `26962x^2`; discard all other positive monomials. Group the
negative coefficients by their x degree:

    C_0=sum_(b_(0j)<0) |b_(0j)| h^j,
    C_1=sum_(b_(1j)<0) |b_(1j)| h^j,
    C_2=sum_(i>=2,b_(ij)<0) |b_(ij)| h^(i-2+j).

For `0<=x,y<=h`, each negative monomial in the third group is at least
`-|b_(ij)|x^2 h^(i-2+j)`. Therefore

    P_-(x,y)>=1350-C_0-C_1 x+(26962-C_2)x^2.           (8)

Direct sums of the displayed integer coefficients give

| Sum | Exact value | Convenient strict upper bound |
|---|---|---:|
| C_0 | `9685694025/34359738368` | 1 |
| C_1 | `949905181458335/68719476736` | 14000 |
| C_2 | `38417241444314847738978481449/9671406556917033397649408` | 4000 |

Using these three rational comparisons in (8),

    P_-(x,y)>=1349-14000x+22962x^2.                    (9)

The derivative of the right side is `-14000+45924x`; at `x=h`
it is `-143633/16<0`. It is therefore negative throughout `[0,h]`.
The quadratic is decreasing there, so its minimum is its value at h:

    1349-14000h+22962h^2=189321/2048>0.                (10)

This proves the descending polynomial sign on the whole square. Equations
(4),(6), with `x-y>=0`, prove (2).

At `x=y`, identities (5),(6) prove equality without division by an angle
increment. Finally, the displayed formula for f and
`0<h<1/sqrt(3)` give `f(x)>0` whenever `0<x<=h`. This completes the
two-edge theorem.

## 5. Why these two inequalities close an actual cyclic problem

The potential construction in `C1092-POSITIVE-CYCLE.md` proves
`L_(i+1)-L_i>=B_+(x_i,x_(i+1))` on ascending edges and the analogous
inequality with `B_-` on descending edges. It uses the smaller actual
angle's separating normal, which is valid for either original source
normal because the central displacement has positive horizontal and
nonpositive vertical coordinates.

On a closed cycle, the sum of ascending increments equals the sum of
descending increments. Denote the common nonnegative value by V. The
two-edge theorem then gives

    0=sum_i(L_(i+1)-L_i)
       >=sum_i f(x_i)+(11/10)V-V
       =sum_i f(x_i)+(1/10)V.

The geometry forces every `x_i>0` when `a>1`, so the right side is
positive. The two fixed polynomial estimates thus replace every
all-positive central-angle bin in `0<=x_i<=7/64` by one continuous
cycle theorem.
