# A shorter corner reach excludes the three forced near-wall points

All terminating decimals denote exact rational numbers. Owned points are strict; exclusions and container supports allow equality. The proof covers every square orientation continuously and uses only the one stated actual wall.

## 1. The theorem

**Theorem 1.** No open square R of side a>1 whose closure lies in x≤1 can strictly own

    P=(.086,0), B=(0,.26), C=(0,.8)

while excluding all four points

    D0=(.02,0), D1=(.02,.02), D2=(−.04,.11), E=(.22,1).

Compared with Theorem 7 of `OTHER-GEOMETRY.md`, the needed corner abscissa is only .22. No upper side bound, other container wall, or orientation premise is needed.

## 2. Nonnegative canonical angles

Use the frame u=(c,s), v=(−s,c), where c≥s≥0 and c²+s²=1. Let U,V be the lower face coordinates. At D0 the upper u, lower v and upper v bands are strict by P,P,C, respectively. Its only possible exit is therefore lower u:

    U≥.02c.                                             (1)

Both lower bands of E are strict by P. An upper-u exit would give

    a≤.20c+s≤1.20/sqrt(2)<1,

because .20 cos θ+sin θ increases on the canonical interval. Thus E exits upper v:

    V+a≤c−.22s.                                        (2)

The genuine right wall now implies

    1≥c(U+a)−sV
      ≥a(c+s)+.02c²−cs+.22s².

It suffices to prove that

    Φ=c+s−1−cs+.02c²+.22s²>0.                          (3)

Put t=s/(1+c), so 0≤t≤sqrt(2)−1<1/2. Exact substitution gives

    50(1+t²)²Φ=P(t):=1−58t²+200t³−99t⁴.                (4)

For 0≤t≤3/10, the last two terms satisfy

    200t³−99t⁴≥(1703/10)t³.

Let r=1160/5109. The following exact identity proves the lower cubic strictly positive:

    1−58t²+(1703/10)t³
      =260843/78305643
       +(1703/10)(t−r)²(t+r/2)>0.                     (5)

For 3/10≤t≤1/2, differentiate (4):

    P'(t)=t(−116+600t−396t²)>0.

Indeed the parenthesized concave quadratic has values 709/25 and 85 at the two endpoints, so it is positive on that whole interval. Hence

    P(t)≥P(3/10)=3781/10000>0.                         (6)

Equations (5) and (6) prove (3) over the entire canonical domain, including t=0. The wall inequality is therefore impossible since a>1.

## 3. Nonpositive canonical angles

Use instead u=(c,−s), v=(s,c), with the same c≥s≥0, and put τ=s/c. The point D0 has both u bands and its upper v band strict by P and C. Thus it must exit lower v:

    V≥.02s.                                             (7)

Suppose first τ≥5/6. The u projection of E lies strictly between those of C and B:

    u(E)−u(C)=.22c−.20s≥.02c>0,
    u(E)−u(B)=.22c−.74s<0.

Its lower v band is strict by P. Therefore E exits upper v, and (7) would give

    a≤c+.20s≤7/sqrt(61)<1.                              (8)

The middle bound is the value at τ=5/6: (1+.20τ)/sqrt(1+τ²) decreases for τ≥5/6. Its strict comparison is 49<61. Thus τ<5/6.

If 0≤τ≤1/4, D1 has both u bands strict by P,C. Its v projection is also strictly between theirs, since

    v(D1)−v(P)=c(.02−.066τ)>0,
    v(D1)≤.04c<.8c=v(C).

This puts D1 strictly in R, contrary to exclusion.

If 1/4≤τ<5/6, the same argument uses D2. Its u projection lies strictly between those of C,P:

    u(D2)−u(C)=c(−.04+.69τ)>0,
    u(D2)<0<u(P).

Its v projection lies strictly between those of P,C:

    v(D2)−v(P)=c(.11−.126τ)>0,
    v(D2)<.11c<.8c=v(C).

Thus D2 is strict in R, another contradiction. The two intervals overlap at τ=1/4 and exhaust τ<5/6. The high-angle interval includes the diagonal. Together with Section 2, this treats every orientation, axis, diagonal, and exterior tangency. ∎
