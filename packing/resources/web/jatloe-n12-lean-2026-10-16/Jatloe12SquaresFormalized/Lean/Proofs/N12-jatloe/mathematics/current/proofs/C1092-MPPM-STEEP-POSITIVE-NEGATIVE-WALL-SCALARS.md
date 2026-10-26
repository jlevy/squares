# C1092 MPPM: four continuous wall-support scalars for a steep positive and a shallow negative square

This chapter is pure algebra. All decimals denote exact rational numbers. Every interval is treated continuously, including its endpoints. The four expressions below are the full-support expressions of one actual boundary square in the companion geometric application.

## 1. Definitions and statement

Put

    p0=2 atan(1/3), q0=atan(3/8),
    p0<=p<=pi/4, 0<=q<=q0, 0<=beta<=pi/2,
    c=cos p, s=sin p, d=cos q, t=sin q,
    h=cos beta, r=sin beta, Theta=pi/2-q.

In particular

    .7<c<=.8, .6<=s<.71, c+s>=1.4,
    d>=8/sqrt(73)>.93, t<=3/sqrt(73)<.36,
    t/d<=3/8, w=t/(1+d)<=3/(8+sqrt(73))<2/11.

Define

    ell=ct+sd,
    kC=ch+sr, deltaC=cr-sh,
    kE=th+dr, deltaE=tr-dh,
    WC=kC+|deltaC|, WE=kE+|deltaE|,
    C0=s-1, E0=.26t-d.                           (1)

The two boundary-direction support caps are

    FC=.5c deltaC+kC s-(kC-deltaC)  if beta<=p,
    FC=deltaC(c+s)+kC s-(kC+deltaC) if beta>=p;    (2)

    FE=-P h-Q r                    if beta<=Theta,
    FE=P2 h+Q2 r                   if beta>=Theta, (3)

where

    P=.74dt-.26t^2,
    Q=1-.74t^2-.26dt, S=1-Q,
    P2=d-.35+.61t^2-.65dt,
    Q2=-1-t+.65t^2+.61dt.                        (4)

Both definitions agree at their joining angle. Set

    G00=.5[ell(h+r)+t WC+s WE]-2ell-t C0-s E0;
    G01=.5[kC(h+r)+h WC+s]-2kC-h C0-s FE;
    G10=.5[kE(h+r)+t+r WE]-2kE-t FC-r E0;
    G11=h+r-2-h FC-r FE.                         (5)

**Theorem 1.** G00 and G10 are nonnegative on the full three-angle domain. G01 and G11 are nonnegative whenever beta>=pi/4.

The application excludes an actual boundary-supplied successor normal when beta<=pi/4 directly from strict anchors. Thus these are precisely all scalar ranges required there.

## 2. The central/central width inequality

The exact width expression

    W=ell(h+r)+t WC+s WE

has the following three forms:

    W=(2ell+2st)h+2sd r             for beta<=p;
    W=2ell(h+r)                    for p<=beta<=Theta;
    W=2ct h+(2ell+2st)r             for beta>=Theta. (6)

Each is a nonnegative linear combination of cos beta and sin beta, so its minimum on its interval is at an endpoint. At beta=0 and beta=pi/2 its value is 2ell+2st.

At beta=p it suffices to check ell(c+s-1)>=st. In fact

    ell(c+s-1)-st>=.4ell-st
       =d[.4s+(t/d)(.4c-s)]
       >=d[s/40+3c/20]>0,                        (7)

because .4c-s<0 and t/d<=3/8.

At beta=Theta use the exact identity

    ell(d+t-1)-st
       =tw[c(1+d-t)-s(d+t)]>=0.                  (8)

The bracket is at least s(1-2t)>0, using c>=s and t<.36. Thus (6)--(8) prove

    W>=2ell+2st.

Substitution in (5) gives

    G00>=t(1-c-.26s)>=0,                         (9)

with a positive coefficient 1-c-.26s>.2-.26(.71)=77/5000. The endpoint t=0 is retained.

## 3. The C cap has a single clamped maximum

For beta<=p, (2) expands as

    FC=(-c-s+.5cs)h+(c-s+.5c^2+s^2)r.

The derivatives of its two coefficients with respect to p are

    (c-s)[-1+.5(c+s)]<=0,
    -(c+s)+cs<0.                                 (10)

For beta>=p, its expansion is

    FC=-(c-s+s^2)h+(1+cs-c-s)r,

whose coefficient derivatives are

    c+s-2cs>0,
    (c-s)(c+s-1)>=0.                             (11)

Therefore for fixed beta the maximum of FC over p0<=p<=pi/4 occurs at p=p0 if beta<=p0, at p=beta if p0<=beta<=pi/4, and at p=pi/4 if beta>=pi/4. The endpoint values are

    FC=-1.16h+.88r               at p=p0;
    FC=r-1                      at p=beta;
    FC=-.5h+f r                 at p=pi/4,
    f=1.5-sqrt(2), 0<f<.09.                      (12)

In G10 and G11 every other term is independent of p, and FC has a nonpositive coefficient. Consequently these clamped values provide valid scalar lower bounds. They do not change any actual square in the application.

## 4. The G10 inequality

For beta<=Theta, direct expansion gives

    G10=t[h(h+r-2)-FC-.26r]+dr(h+r-1).            (13)

If beta<=p0, use the first cap in (12), and put

    A=h(h+r-.84)-1.14r, B=r(h+r-1)>=0.

Then G10>=tA+dB. If A>=0 this is nonnegative. If A<0, use t/d<=3/8. For z=tan(beta/2)<=1/3 the exact identity is

    (B+3A/8)(1+z^2)^2
      =[138z^4-1121z^3+650z^2-21z+12]/200>0.    (14)

Indeed the numerator is at least

    (829/3)z^2-21z+12
      =(829/3)(z-63/1658)^2+38469/3316>0,

using z<=1/3 in its negative cubic term. This proves the first range. For p0<=beta<=pi/4, the middle cap in (12) makes G10 exactly G00 with p=beta, already nonnegative by (9).

It remains beta>=pi/4. Put H=h+r, u=h/r in [0,1], and eta=f+.26<.35. For beta<=Theta, (13) and (12) give

    G10/(dr)>=H-1+(t/d)[u(H-1.5)-eta].            (15)

The bracket is negative, and t/d<=min(3/8,u). If u<=3/8, (15) is at least

    (1+u)sqrt(1+u^2)-1-1.5u^2-eta u
      >=u(1-eta-1.5u)>7u/80.                    (16)

If u>=3/8, use H>=11/sqrt(73)>32/25 and t/d<=3/8 in (15). This gives

    G10/(dr)>119/800-33u/400>=53/800>0.           (17)

For beta>=Theta, the other width sign instead gives

    G10>=t A_*+d B_*,
    A_*=1+hr-1.5h-eta r,
    B_*=r(r-1)<=0.                               (18)

Here A_*=1-h(1.5-r)-eta r>1-.71(.8)-.35=.082. The angle order gives t/d>=u, while u<=3/8. Thus G10/d>=uA_*+B_*. This is r times the aligned expression in (16), and is nonnegative. These ranges prove G10 everywhere, including coordinate endpoints by continuity.

## 5. Two elementary successor coefficient facts

The coefficients (4) satisfy

    0<=P<.3, 0<=S<.2, P>=S,
    P-S=t(.48d-t)>=0.                            (19)

These follow from d<=1,t<.36,t/d<=3/8. We also need

    1/3<P2<=.65, P2'<0, Q2'<0.                  (20)

To prove the derivative signs on 0<=q<=q0, observe

    P2'=-t+1.22dt-.65(d^2-t^2)
       <=.22t-.65(55/73)<0.

Moreover

    Q2''=1.3-2.6t^2+t(1-2.44d)
         >=1.3-2.6(.36)^2-1.44(.36)>0.

Thus Q2' increases and is bounded above by its endpoint value

    Q2'(q0)=[259/4-8sqrt(73)]/73<0.

The last sign follows by squaring 259/4<8sqrt(73). Since P2(0)=.65, its upper bound follows. Its lower bound follows directly from

    P2>d-.35-.65t>.93-.35-.65(.36)=.346>1/3.

All these are continuous bounds. In particular Q2<=-1 and

    R=1-.61d-.65t>0,
    1+Q2=-tR.                                   (21)

## 6. The G11 inequality for beta>=pi/4

Use the final C cap in (12), and set u=h/r in [0,1]. Define

    K(u)=(1+u)sqrt(1+u^2)-1-1.5u^2-fu.

For beta<=Theta, the exact result is

    G11/r^2>=K(u)+P u-S.                         (22)

For fixed u, the q-dependent part is

    P u-S=dt(.74u-.26)-t^2(.26u+.74).

Its second derivative is

    -2[(.74u-.26)sin(2q)+(.26u+.74)cos(2q)]<0.   (23)

Indeed the bracket is at least [-.26(48)+.74(55)]/73=1411/3650>0. The minimum in q therefore lies at an endpoint of 0<=q<=min(q0,atan u).

At q=atan u the two boundary/central successor directions align, so (22) is G10, already nonnegative. At q=0 it is K(u). The elementary bound

    sqrt(1+u^2)>=1+.4u^2, 0<=u<=1,              (24)

follows by squaring. It gives

    K(u)>=u[1-f-1.1u+.4u^2]>=u(.3-f)>=0.

For the remaining endpoint q=q0, necessarily u>=3/8. Here

    P=771/3650>.21, S=129/730<.18.

Equations (22),(24) yield

    G11/r^2>-.18+1.12u-1.1u^2+.4u^3.

This cubic increases: its derivative has minimum 67/600>0. At u=3/8 its value is 681/6400>0. Thus every endpoint needed by (23) is nonnegative.

For beta>=Theta, instead

    G11/r^2>=K(u)-P2u-Q2-1.                     (25)

By (20) the right side increases with q. Its admissible lower endpoint is q=atan u, where again it is the aligned G10 value. This proves G11 on its complete required domain.

## 7. The G01 inequality for beta>=pi/4

This last mode retains the actual p rather than clamping it. Put L=c+s and use the coordinate

    z=h/(1+r), 0<=z<=rho=sqrt(2)-1<5/12.

For either linear form FE, write

    G01=(c-s)h^2+Lhr+s-Ah-Br.

Multiplication by (1+z^2)^2 gives the exact polynomial

    T(z)=(s-B)+2(L-A)z+(4c-2s)z^2
                   -2(L+A)z^3+(s+B)z^4.         (26)

### 7.1. The range pi/4<=beta<=Theta

Here A=2c+s-1-sP and B=s(1+S). The coefficient 2(L-A)=2(1-c+sP) is positive. Also

    T'''(z)=-12(L+A)+24(s+B)z<0                 (27)

throughout [0,rho]. In fact L+A=3c+2s-1-sP>2.087 and s+B=s(2+S)<1.562, so the right side is less than -12(2.087)+24(1.562)(5/12)<0.

Consequently T' is concave and T'(0)>0. Its nonnegative set is an interval containing zero, so T can have no interior strict minimum. Its minimum on any subinterval is at an endpoint.

The current z interval is [w,rho]. At beta=Theta, G01 is exactly G00, nonnegative by (9). At beta=pi/4, (19) gives FE<=-r. Substitution in (5) then yields

    G01>=c+s-[2(c+s)-1]/sqrt(2)
          >=3/sqrt(2)-2>0.                       (28)

Both endpoints of T are therefore nonnegative, and (27) proves the whole first interval.

### 7.2. The range Theta<=beta<=pi/2

Now 0<=z<=w, A=2c+s-1+sP2, and B=s(2+Q2). The polynomial coefficients a0,...,a4 in (26) satisfy

    a0=stR,
    a1=2s(x-P2), x=s/(1+c)>=1/3,
    a2=4c-2s>0,
    a3=-2(L+A), a4=s+B>0.                       (29)

For a4, use Q2>=-1-t>-1.36. Furthermore

    (L+A)/s=3c/s+2+P2-1/s<=21/4,                (30)

because c/s<=4/3, P2<=.65, and 1/s>=sqrt(2)>1.4.

If q=0 this interval has only its aligned endpoint, already covered by (9). Suppose q>0. Write T in the degree-four Bernstein basis on [0,w]. Its first four coefficients are

    b0=a0,
    b1=a0+a1 w/4,
    b2=a0+a1 w/2+a2 w^2/6,
    b3=a0+3a1 w/4+a2 w^2/2+a3 w^3/4.            (31)

By x>=1/3, P2>1/3, a2>0 and (30), each b_i/(st), 0<=i<=3, is bounded below by

    B_*(q)=R+3(1/3-P2)/[2(1+d)]
                       -21t^2/[8(1+d)^3].       (32)

For b1 and b2, replacing their smaller multiples of the negative number 1/3-P2 by the coefficient 3/2 only weakens the bound. The extra last term in (32) is negative, so it also weakens their bounds and the b0 bound.

In w=t/(1+d), (32) has the exact expression

    B_*=[61-130w-203w^2-390w^3-545w^4-525w^6]
                          /[400(1+w^2)]>0.       (33)

Every nonconstant coefficient of the numerator is negative. Since 0<=w<2/11, its numerator is at least its value at 2/11,

    49062029/1771561>27.

Thus the first four Bernstein coefficients are positive. The fifth is T(w), the aligned G00 endpoint, and is nonnegative by (9). All Bernstein basis functions are nonnegative on [0,w]. This proves T>=0, and hence G01>=0, on the final interval.

Sections 2,4,6,7 prove every assertion of Theorem 1. The only angle subdivisions were the genuine signed-support changes p and Theta and the fixed coordinate midpoint pi/4. All intervals, joins and weak-support endpoints were retained; no sampled feasibility statement enters the proof.
