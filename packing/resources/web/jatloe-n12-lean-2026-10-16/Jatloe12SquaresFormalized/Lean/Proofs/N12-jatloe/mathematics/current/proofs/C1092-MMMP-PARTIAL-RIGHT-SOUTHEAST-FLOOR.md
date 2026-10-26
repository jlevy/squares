# C1092 MMMP: the southeast outer arm restores a strict floor and small angle

All terminating decimals are exact rationals. Squares are the actual original open squares, with common side a>1 and disjoint interiors. Owned points are strict. Missing-point exits and closure supports may be equality. Every scalar interval used below is continuous.

**Theorem.** In the original MMMP family, suppose F8 is strictly in actual Q10 and G8 is strictly in actual Q5. Translate by (-2,-2), write E=Q5, and give its positive canonical frame the notation

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1.

Let U,V be its lower faces, A=U+a,H=V+a its upper faces, and z=s/(1+c). Then

    H<=min(0,.12c-.47s),
    A<=c-.26s,
    U>=-s, a<=c+.74s,                            (1)

and the actual whole bottom bar forces

    sA+cH>a(c+s)-1,
    U>(ac-1)/s>-z,
    A>a-z.                                      (2)

The full angle and upper-face consequences are

    s/c<1/3,
    s<1/sqrt(10), c>3/sqrt(10),
    H>[-(1-c)(1-s)+.26s^2]/c>-1/100.             (3)

No sine bound from the opposite G8-exclusion branch is imported here.

## 1. Literal point and bar sources

The theorem `C1092-MMMP-RIGHT-NEAR-BOTTOM-ORIGIN.md` applies because F8 belongs to Q10. It gives a strictly positive original angle for Q5, strict F4,G6 in Q5, and the bottom origin (2,1) strictly in the actual Q9. Universal F6 ownership then puts the whole closed segment from that origin to F6 strictly inside this same open Q9. After translation, the full actual ledger is

| Local datum | Original datum | Actual source |
|---|---|---|
| Strict M=(.35,-.35) | Southeast marker | Q5 |
| Strict I=(0,-.26), D=(.26,0) | F4,G6 | Q5 by the right-near theorem |
| Strict G=(1,-.4) | G8 | Q5 by the present hypothesis |
| Excluded O=(0,0) | (2,2) | Actual Q7 center |
| Excluded F=(1,-.26) | F8 | Actual Q10 by hypothesis |
| Excluded P=(.47,.12) | (2.47,2.12) | Actual Q6 by NORTHEAST-LOWER-TIP, Theorem1 |
| Excluded whole B=[0,.4]x{-1} | [(2,1),(2.4,1)] | Same actual Q9 |

The northeast strict point is unconditional in the original MMMP family, by `C1092-MMMP-NORTHEAST-LOWER-TIP.md`. Its proof uses the actual northeast cap table and does not assume the present conclusion.

## 2. Four forced actual faces

The two u bands of the excluded O follow from strict I,D, and its lower v band follows from strict M. Hence O is upper v:

    H<=0.                                       (4)

At F=(1,-.26), the lower u band follows from D, since its increment is .74c-.26s>=.48c>0. Its upper v band also follows from D. For its lower v band, use V=H-a<=-a and

    s+.26c<=1.26/sqrt(2)<1<a.

The displayed trigonometric bound holds on the entire canonical interval: sin(q)+.26 cos(q) is increasing for 0<=q<=pi/4. Thus F can leave E only through its upper u face, proving

    A<=c-.26s.                                  (5)

At the excluded P=(.47,.12), the lower u band follows from strict I. Its upper u band follows from strict G, with gap

    u(G)-u(P)=.53c-.52s>=.01c>0.

Its lower v band follows from strict G as well, with gap .53s+.52c>0. Consequently P is upper v:

    H<=.12c-.47s.                               (6)

Strict D gives H>-.26s. Combining this with (6) yields

    .21s<.12c,
    s/c<4/7,
    s<4/sqrt(65)<1/2.                           (7)

Finally the left endpoint B0=(0,-1) of the actual excluded bar has both upper bands from strict I. If it were lower v, then V>=-c and (4) would give a=H-V<=c<=1. Thus it is lower u:

    U>=-s.                                      (8)

Equations (5),(8) imply a=A-U<=c+.74s. This proves (1), including every initially possible weak exterior equality.

## 3. The lowest closure vertex lies over the actual bottom bar

The bottom closure vertex of this positive square is

    Z=(cU-sV,sU+cV).

Its abscissa is positive: by (4),(8),

    Z_x>=-cs+as=s(a-c)>0.                       (9)

The strict D bound H>-.26s and (5) give

    Z_x=c(A-a)-s(H-a)
       <c^2-.26cs+.26s^2+a(s-c)
       <1-.74s^2-.26cs+s-c=:f(s).                (10)

Here c>s by (7), so a>1 justifies the second strict comparison. On 0<=s<=1/2, with c=sqrt(1-s^2),

    f'(s)=1-1.48s-.26c+(.26s^2+s)/c>0.           (11)

Indeed the first three terms are nonnegative from s<=1/2 and c<=1. For s>0 the final term is positive; at s=0 the derivative is .74. This proves strict increase on the whole closed interval.

At its endpoint,

    f(1/2)=(263-113sqrt(3))/200<.4.              (12)

The exact last comparison is 183^2<3(113)^2, namely33489<38307. Equations (7),(9)--(12) therefore prove

    0<Z_x<.4.                                   (13)

We now use the entire bar B in its actual open owner Q9. If Z_y<-1, the segment from strict M to Z crosses y=-1 before reaching Z, with abscissa strictly between0 and.4 by (13) and M_x=.35. Every point before Z on this segment is interior to E, because its four defining bands interpolate a strict point with a closure point. The crossing would lie in both actual square interiors.

If Z_y=-1, then Z itself lies in the strict bar B and hence in the interior of Q9, while it is a closure point of E. A neighborhood inside the open Q9 must meet E, again contradicting disjoint interiors. Thus equality causes no tangent exception. We have proved

    Z_y>-1.                                     (14)

Replacing U,V by A-a,H-a gives the first inequality in (2). Also (4),(14) imply

    U>(ac-1-cH)/s>=(ac-1)/s>-z.

The last strict inequality uses a>1 and (1-c)/s=z. Adding a gives A>a-z and completes (2).

## 4. The coupled floor and northeast point force s/c<1/3

Apply both upper caps (5),(6) to the strict coupled floor (2). They give

    c+s-1
      <a(c+s)-1
      <sA+cH
      <=.53cs+.12c^2-.26s^2.

Consequently, for the positive canonical angle q of E,

    J(q)=c+s-1-.53cs-.12c^2+.26s^2<0.            (15)

Its exact derivative throughout 0<=q<=pi/4 is

    J'(q)=(c-s)[1-.53(c+s)]+.76cs>0.             (16)

The first factor is nonnegative, 1-.53sqrt(2)>0, and the second summand is positive for q>0. At q=0 the first summand is positive as well.

At q0=arctan(1/3), one has c=3/sqrt(10),s=1/sqrt(10), and

    J(q0)=4/sqrt(10)-1.241>0.                    (17)

The exact comparison is 16/10>1540081/1000000. Strict monotonicity of J and (15) imply q<q0. This proves the first three angle assertions in (3) by the usual monotonicity of sine, cosine and tangent on the canonical interval.

## 5. The upper v face is uniformly above -1/100

Keep the actual upper-u cap (5) in the coupled floor, instead of discarding its positive information. From a>1,

    cH>a(c+s)-1-sA
       >=a(c+s)-1-s(c-.26s)
        >c+s-1-cs+.26s^2
         =-(1-c)(1-s)+.26s^2.                    (18)

This is the first lower H bound in (3). Put

    g(s)=[(1-c)(1-s)-.26s^2]/c,
    c=sqrt(1-s^2).

Thus H>-g(s). Direct differentiation gives

    g'(s)=[c^3-1+.48s+.26s^3]/c^3.               (19)

The elementary bound c^3>=1-(3/2)s^2 follows by differentiating c^3+(3/2)s^2-1: its derivative is3s(1-c)>=0 and its value at0 is0. Hence the numerator in (19) is at least

    s[.48-1.5s+.26s^2]>0

for 0<s<=1/sqrt(10)<.32. Therefore g is strictly increasing on the entire needed interval. At its upper endpoint,

    g(1/sqrt(10))=(637sqrt(10)-2000)/1500<1/100.  (20)

The final exact comparison follows from

    10(637)^2=4057690<4060225=(2015)^2.

Combining (18)--(20) gives H>-1/100, proving the last assertion in (3).

All inequalities in this chapter were derived from the stated actual E, N, R, W and bottom owner. In particular the small angle and the lower H cap are proved anew under strict G8 ownership in E. They do not use a G8 exclusion or the earlier s<.21 bound from the other branch.
