# C1092 MMMP: a lower northeast tip and a sharper southeast bar bound

All terminating decimals below are exact rational numbers. Owned points are strictly inside their stated actual open squares; exclusions and contacts with closure supports may be equality. The local statements use side a>1 and entire canonical angle intervals. No finite angle sampling is involved.

## 1. A strict point from the complete northeast face table

**Theorem 1.** In every original MMMP configuration, the actual northeast Q6 strictly owns

    K=(2.47,2.12).

**Proof.** Use the chart (X,Y)=(2-y,x-2) and the positive canonical frame

    u=(b,t), v=(-t,b), b>=t>0, b^2+t^2=1.

The actual Q6 face theorem `C1092-MMMP-NORTHEAST-TOP-CAP.md` gives its lower faces p,q the bounds

    p>=-b, p+a<=t-.4b,
    q>=.4t, q+a<=b+t.                              (1)

The target is Z=(-.12,.47) in this chart. Its two projections are

    u(Z)=-.12b+.47t, v(Z)=.12t+.47b.

Each of its four bands is strict. For the lower u band, the upper p cap gives

    u(Z)-p>=a+.28b-.53t>=a-.25t>0.

For the upper u band, the lower p bound gives

    p+a-u(Z)>=a-.88b-.47t
               >=a-sqrt(.88^2+.47^2)
                =a-sqrt(.9953)>0.                 (2)

For the lower v band, the upper q cap gives

    v(Z)-q>=a-.53b-.88t
               >=a-1.41/sqrt(2)>0.                (3)

To justify the second comparison in (3), the function .53 cos(theta)+.88 sin(theta) increases throughout 0<=theta<=pi/4: its derivative is .88 cos(theta)-.53 sin(theta)>=.35 cos(theta)>0. Its maximum is therefore 1.41/sqrt(2), whose square is 19881/20000<1.

Finally,

    q+a-v(Z)>=a-.47b+.28t>=a-.47>0.

Thus Z, and hence the original K, is strict in the same actual Q6. Every face in (1) was already derived from the genuine Q7, Q10, Q11 and Q2 owners, including the universal top origin; no additional northeast point is presumed here. ∎

## 2. A complete negative-angle point-and-bar theorem

**Theorem 2.** Let C be an open square of side a>1 with canonical frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1.

Suppose C strictly owns

    M=(.35,-.35), D=(.26,0), A=(1,-.26),

and excludes F=(0,-.26), K=(.47,.12), and every point of

    I=[.26,.8] x {-1}.

Writing U,V for its lower faces, one necessarily has

    U>=.26s,
    V>=.8s-c,
    V+a<=.47s+.12c,
    s/(1+c)<13/100.                               (4)

The theorem uses the whole excluded segment I, which can be the strict segment of one other actual square.

### 2.1. Three forced face bounds

The lower u and v bands of K follow from strict D. Their projection increments are

    .21c-.12s>=.09c>0,
    .21s+.12c>0.

Its upper u band follows from strict A, with projection gap .53c+.38s>0. Therefore its only possible exit is upper v:

    V+a<=.47s+.12c.                                (5)

Both upper bands of F follow from D. Its lower v band is strict by (5), since

    .47s+.38c<=sqrt(.47^2+.38^2)=sqrt(.3653)<1<a.

Thus F is lower u:

    U>=.26s.                                      (6)

At B=(.26,-1), the lower u band follows from D and the upper v band follows from M. Its upper-u alternative would combine with (6) to give

    a<=.26c+.74s<=sqrt(.6152)<1.

It must therefore leave through the lower v face:

    V>=.26s-c.                                    (7)

The other endpoint T=(.8,-1) has its lower u and upper v bands from M, with strict gaps .45c+.65s and .65c-.45s>=.20c. Thus its only alternatives are upper u and lower v. The next step excludes the first alternative by the whole bar.

### 2.2. An upper-u exit at the far endpoint would cross the actual bar

Suppose U+a<=.8c+s. Together with (6), it gives

    1<a<=.8c+.74s.

For theta=arcsin(s) in the canonical interval, the expression on the right increases on 0<=theta<=arctan(1/3) and has endpoint 3.14/sqrt(10)<1. Therefore

    theta>arctan(1/3).                             (8)

Let A_C=U+a and H_C=V+a. The closed bottom vertex of C is

    Z=(c A_C+s V, -s A_C+c V).

Its abscissa is strictly between the bar endpoints. Equations (6),(7) imply

    Z_x>=a c-.74cs+.26s^2
        >c-.74cs>=1/sqrt(2)-.37>.26.              (9)

The supposed upper-u bound at T and (5) imply

    Z_x<=.8-.33s^2+s(1.12c-a)
        <.8+s(1.12c-.33s-1)<.8.                  (10)

For the final sign, 1.12 cos(theta)-.33 sin(theta) decreases for every positive theta. At arctan(1/3) its value is 3.03/sqrt(10)<1, so (8) proves the claim.

The ordinate is below the bar. The same bounds give

    Z_y<=-a(c+s)+.47cs+.12c^2-.26s^2.

Set

    J(theta)=c+s-1-.47cs-.12c^2+.26s^2.

On arctan(1/3)<=theta<=pi/4, its derivative is

    J'=(c-s)[1-.47(c+s)]+.76cs>0,

because .47sqrt(2)<1 and cs>0. Its value at the lower endpoint is

    4/sqrt(10)-1.223>0;

the exact last comparison follows from 16/10>1495729/1000000. Hence Z_y<-1.

The strict point M has .26<M_x<.8 and M_y>-1. By (9),(10), the segment from M to the closure vertex Z crosses I at an abscissa strictly between .26 and .8 and before reaching Z. Every point before Z on this segment is strictly inside C: each of the four linear defining bands interpolates a strict value at M with a weak closure value at Z. This contradicts exclusion of the whole I. It also handles all initially permitted edge or vertex tangencies.

Therefore T is lower v and

    V>=.8s-c.                                     (11)

### 2.3. A single exact endpoint gives the small half-angle

Combining (5),(11) gives

    1<a<=1.12c-.33s.                              (12)

The right side decreases strictly with theta throughout the positive canonical interval. At the half-angle z=s/(1+c)=13/100 its components are

    c=9831/10169, s=2600/10169,

and the exact value in (12) is

    253818/254225<1.

Thus z<13/100. Equations (5),(6),(11) supply the other conclusions in (4). The zero-angle case was retained in every face comparison, and is included in the necessary closed lower endpoint in (4). ∎

## 3. Literal application when the actual bottom origin is missing

**Corollary 3.** In the original MMMP family, suppose actual Q5 owns G6=(2.26,2) and F8=(3,1.74), excludes F4=(2,1.74), has a nonpositive original canonical angle, and actual Q9 excludes its bottom origin (2,1). Then the face bounds (4), translated by (2,2), hold for this actual Q5, and its negative half-angle is less than13/100.

Indeed, the marker of Q5 and its owned G6,F8 are precisely M,D,A after translation by (-2,-2). The excluded F is the stipulated actual F4 omission. Theorem 1 puts K strictly in the different actual Q6, so K is a genuine exclusion from Q5.

The universal bottom-pair theorem gives strict (2,.914),G5=(2.26,1),F6=(2.4,1) in the same actual Q9. Apply the wall-origin-alternative theorem (`C981-WALL-CYCLES.md`, Theorem11) in the local chart (X,Y)=(x-2,1-y). Its actual square is Q9, its real wall is Y<=1, its strict points are (0,.086),(.4,0), and its missing origin is (0,0). Taking z=.8 is valid because .8<2sqrt(2)-2. The theorem yields (2.8,1) strictly in Q9. Convexity with G5 therefore gives the whole strict bar

    [2.26,2.8] x {1}

in that one actual square. Its translation is exactly I, excluded from Q5 by disjointness. Theorem 2 now applies with every source explicitly accounted for.

This is a necessary continuous bound for the stated residual branch. It does not assert a bottom origin or the final MMMP contradiction, and it does not replace the full bar by unrelated endpoint exclusions.
