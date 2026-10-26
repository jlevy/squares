# C1092 MPPM: the sharp central/central support inequality

Every decimal below is exact. Put

    p0=2 atan(1/3), alpha=1.086,
    p0<=p<=pi/4, 0<=q<=pi/4, 0<=beta<=pi/2,
    c=cos p, s=sin p, d=cos q, t=sin q,
    h=cos beta, r=sin beta,
    k=cd+st,
    kC=ch+sr, deltaC=cr-sh,
    kE=dh+tr, deltaE=dr-th.

The central/central scalar from the three-square support reduction is

    G00=.5[k(h+r)+d(kC+|deltaC|)+s(kE+|deltaE|)]
         -2k-d(alpha s-1)-s(d-.56t-1).             (1)

**Theorem 1.** On the entire stated closed domain,

    G00>=1/3125.                                  (2)

Equality occurs at p=q=beta=p0. In particular this proves both aligned inputs required by C1092-MPPM-STEEP-POSITIVE-BOUNDARY-SCALARS.md.

## 1. The common aligned value

When p=q=beta, exact substitution in (1) gives

    D(p)=2(c+s)-2-2.086cs+.56s^2.                  (3)

The identities c(p0)=4/5,s(p0)=3/5 give D(p0)=1/3125. Also

    D'(p)=(c-s)[2-2.086(c+s)]+1.12cs>0            (4)

on p>=p0. For a fully rational sign bound, use c-s<=.2, c+s<1.415 and cs>=.48. The first term is greater than -.191, while the second is at least .5376. Thus D(p)>=1/3125 throughout.

## 2. The endpoint beta=p

Suppose first q<=p. Expanding the absolute value in (1) gives

    G00(p,q,p)=s-A d-B t,
    A=2c+2.086s-cs-2,
    B=s(1.44-s).                                  (5)

Both A and B are positive. Indeed A(p0)=.3716 and

    A'=(c-s)(2-c-s)+.086c>0.                      (6)

Moreover

    Bc-As=s[2-.56c-2.086s]>0.                     (7)

The function .56c+2.086s increases up to pi/4 and there equals 2.646/sqrt(2)<2. Since A,B>0, the derivative of A cos q+B sin q decreases with q, and (7) is its positive value at q=p. Thus that support increases throughout 0<=q<=p, so (5) is minimized at q=p. Its minimum is the aligned value D(p).

If q>=p, the other absolute-value sign instead gives

    G00(p,q,p)=s-A2 d-B2 t,
    A2=2c+2.086s-1-c(c+s),
    B2=s(1.44-c-s).                               (8)

Again A2,B2>0. For example c>.7,s>=.6,c<=.8,c+s<1.415 give A2>.5196, while c+s<1.44 gives B2>0. The derivative in q of (8) increases, and at q=p equals

    A2s-B2c=s[.56c+2.086s-1]>0.                  (9)

Consequently (8) is also minimized at q=p. We have proved

    G00(p,q,p)>=D(p)>=1/3125                      (10)

for both complete q ranges, including their common boundary.

## 3. The endpoint beta=q

First suppose q<=p. Expansion now gives

    G00(p,q,q)=d-Aq c+Bq s,
    Aq=d(2-d),
    Bq=2-2.086d-1.44t+dt.                         (11)

For fixed q this expression strictly increases with p on the permitted domain. Its derivative is Aq s+Bq c. The elementary bounds

    Aq>=sqrt(2)-.5>.914,
    Bq>=2-sqrt(2.086^2+1.44^2)>-.535

give

    Aq s+Bq c>.914(.6)-.535(.8)=.1204>0.           (12)

If q>=p0, lower p to q and use D(q)>=1/3125. If q<=p0, lower p instead to p0. The remaining function is exactly

    L(q)=1.2-1.8516d+.8d^2-.864t+.6dt.            (13)

On 0<=q<=p0 we have .8<=d<=1 and 0<=t<=.6. Its derivative obeys

    L'=1.8516t-1.6dt-.864d+.6(d^2-t^2)
       <=.5716t-.6t^2-d(.864-.6d)
       <=.5716^2/2.4-.264<0.                     (14)

For the last bound, d(.864-.6d) decreases on [.8,1] and is at least .264. Thus L(q)>=L(p0)=1/3125. This completes q<=p.

Now suppose q>=p. Define

    A3=d(2-d-t)>0,
    B3=1-2.086d+t(d+t-1.44).

The other expansion of (1) is

    G00(p,q,q)=d-A3c+B3s.                         (15)

Its derivative in p is c[A3 tan p+B3]. Since tan p<=t/d,

    A3 tan p+B3<=1-2.086d+.56t
       <=1-1.526/sqrt(2)<0.                      (16)

The middle bound follows because the expression increases with q on [p0,pi/4]. Hence (15) decreases until p=q, where it is D(q). We have proved

    G00(p,q,q)>=1/3125                            (17)

on all angle orders.

## 4. Coordinate endpoints and the full beta interval

At beta=0 or beta=pi/2 the square widths agree, and (1) reduces to

    G00=s[1-(alpha-x)d-.44t],
    x=tan(p/2)>=1/3.                              (18)

Here 0<alpha-x<.753. Cauchy--Schwarz gives

    G00>s[1-sqrt(.753^2+.44^2)]
          >.6(1-.873)=.0762>1/3125.               (19)

For fixed p,q, subdivide the interval in beta at p and q. On each resulting piece the signs of both absolute values are fixed, and G00 has the form

    Astar cos beta+Bstar sin beta+Rstar,
    Rstar=-2k-d(alpha s-1)-s(d-.56t-1)
          =d(1-2c-2.086s)+s(1-1.44t)<0.           (20)

For example c>.7,s>=.6,d>.7 and s<.71 give Rstar<-.44612. Thus

    (G00-1/3125)''+(G00-1/3125)<0                 (21)

on each full piece. All pieces have length at most pi/2. Their endpoint values are nonnegative by (10), (17), and (19). The elementary sine-interpolation inequality therefore gives G00-1/3125>=0 on every piece, retaining the joining and coordinate endpoints. This proves (2) over the complete three-angle domain. The equality assertion follows directly from (3) at p0. ∎

## 5. Exact scalar and geometric consequence

Theorem 1 supplies both aligned hypotheses of the boundary-scalar chapter. That chapter therefore proves G01,G10,G11>=0 everywhere, while the present chapter proves the stronger positive bound (2) for G00. Hence all four scalar modes are nonnegative.

Theorem 1 of C1092-MPPM-STEEP-POSITIVE-THREE-SQUARE-REDUCTION.md proves that the actual three-square configuration in its stated local hypotheses would force one of those same modes to be strictly negative. Thus that configuration is impossible. The strictness comes from the common side a>1, even if an excluded point lies on a face, two faces align, or one scalar mode has a zero coordinate-endpoint value.
