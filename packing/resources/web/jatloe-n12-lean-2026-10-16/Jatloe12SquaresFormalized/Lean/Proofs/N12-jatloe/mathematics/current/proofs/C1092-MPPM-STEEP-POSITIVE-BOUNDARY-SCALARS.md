# C1092 MPPM: continuous reduction of the three boundary-supplied support cases

All decimals are exact rational numbers. This is a scalar lemma, independent of any ownership inference. Its sole external scalar input is the explicitly stated pair of aligned inequalities (8), now proved in C1092-MPPM-STEEP-POSITIVE-CENTRAL-SCALAR.md; that input is kept separate from the calculations proved here.

## 1. Definitions and exact statement

Put

    p0=2 atan(1/3), alpha=543/500=1.086,
    p0<=p<=pi/4, 0<=q<=pi/4, 0<=beta<=pi/2,
    c=cos p, s=sin p, d=cos q, t=sin q,
    h=cos beta, r=sin beta.

Thus .7<c<=.8, .6<=s<.71, 1.4<=c+s<1.415, and 0<=c-s<=.2. Define

    kC=ch+sr, deltaC=cr-sh,
    kE=dh+tr, deltaE=dr-th,
    k=cd+st,
    C0=alpha s-1, E0=d-.56t-1.                    (1)

The two piecewise support caps are

    FC=deltaC(c+s)+kC alpha s-(kC+deltaC)   if beta>=p,
    FC=.5c deltaC+kC alpha s-(kC-deltaC)    if beta<=p; (2)

    FE=kE E0+deltaE(-d-.4t)                 if beta>=q,
    FE=kE E0-.5d deltaE                     if beta<=q. (3)

The formulas agree at their respective joining angles. Set

    G00=.5[k(h+r)+d(kC+|deltaC|)+s(kE+|deltaE|)]
          -2k-dC0-sE0;                              (4)

    G01=.5[kC(h+r)+h(kC+|deltaC|)+s]
          -2kC-hC0-sFE;                              (5)

    G10=.5[kE(h+r)+d+r(kE+|deltaE|)]
          -2kE-dFC-rE0;                              (6)

    G11=h+r-2-hFC-rFE.                               (7)

**Theorem 1.** Suppose the following two aligned scalar inequalities hold for every p,q in the stated ranges:

    G00(p,q,p)>=0,     G00(p,q,q)>=0.               (8)

Then G01,G10,G11 are nonnegative on their entire stated three-angle domain. The proof below retains all equal-angle and coordinate endpoints. In particular (8) is the precise remaining external input; this chapter does not assume the whole three-angle G00 inequality.

We use the following elementary interpolation fact. If a continuous function is twice differentiable on an interval of length less than pi, satisfies f''+f<=0, and has nonnegative endpoint values, it is nonnegative throughout. Indeed subtract the sine interpolation of the endpoints and apply the one-dimensional maximum principle, or integrate the positive Dirichlet Green kernel for -d^2/dx^2-1. Subdividing at the displayed joining angles is allowed; no derivative condition at a join is needed.

## 2. Elementary E coefficients

For beta>=q, (3) expands exactly as

    FE=P(q)h-Q(q)r,
    P=1-d-.6t^2+.44dt,
    Q=1+t-.44t^2-.6dt.                              (9)

Throughout 0<=q<=pi/4,

    0<=P<.213, 1<=Q<1.188,
    .812<2-Q<=1,
    P+(2-Q)<1.11.                                  (10)

Here are direct proofs of the coefficient bounds. The derivative

    P'=t(1-1.2d)+.44(d^2-t^2)

is nonnegative when d<=5/6. When d>=5/6, use t<.56 and d^2-t^2>=7/18 to obtain P'>-.2(.56)+.44(7/18)>0. Hence P increases from zero to .92-1/sqrt(2)<.213. Also

    Q'=d(1-.88t)-.6+1.2t^2
       >.1-.616t+1.2t^2>0,

since d>.7, 1-.88t>0 and the last quadratic has minimum .1-.616^2/4.8>0. Thus Q increases from 1 to .48+1/sqrt(2)<1.188. Finally, with w=d+t,

    P+2-Q=2-w-.16t^2+1.04dt
            <=1.48-w+.52w^2
            <=2.52-sqrt(2)<1.11.                  (11)

The intermediate quadratic increases on 1<=w<=sqrt(2).

## 3. The aligned C/boundary value

When beta=p, both G01 and G11 equal

    T(p,q)=2c+s-2-alpha cs-s FE(p).                 (12)

We prove the strict conclusion T(p,q)>0 without using (8).

First take q<=p. Equation (9) gives

    T=2c+s-2-cs(alpha+P)+s^2Q.                     (13)

For fixed q its derivative with respect to p is at least

    (c-s)[1-1.299(c+s)]+s(2c-1)>0.                 (14)

Indeed the first term is greater than -.168, while the second is greater than .24. If q>=p0, reduce p to q. On the diagonal,

    T(p,p)=2(c+s)-2-2.086cs+.56s^2.                (15)

Its derivative is

    (c-s)[2-2.086(c+s)]+1.12cs>0

on p>=p0: the first term is greater than -.191 and the second is at least .5376. Its value at p0 is exactly 1/3125.

If q<=p0, reduce p instead to p0. Let y=tan(q/2) and z=1/3-y, so 0<=z<=1/3. Exact substitution gives

    12500(1+y^2)^2 T(p0,q)
      =-4(2879y^4-4920y^3+1138y^2+420y-121)
      =400/81-(3760/27)z+(22352/3)z^2
                    -(12976/3)z^3-11516z^4
      >=400/81-(3760/27)z+(14188/3)z^2
      =(14188/3)(z-470/31923)^2+3372800/861921>0.  (16)

The inequality uses z<=1/3 separately in the two negative higher-degree terms.

It remains q>=p. Put j=sin(q-p)>=0. Differentiating the second expression (3) at fixed beta=p yields

    d(FE(p))/dq=-kE(t+.06d)+j(1-d+.06t)<0.         (17)

For example kE>.98, j<.15, t>=.6 and d>.7 give its strict sign directly. Consequently T increases with q, so (15) again supplies a positive lower bound. This proves (12) on all its ranges.

## 4. The G01 inequality

### 4.1. The range beta<=pi/4

On a piece with beta<=p, (5) has the form

    c h^2+s hr+s+A h+B r,

where A,B are constant with respect to beta; their values may change only at beta=q. It follows exactly that

    G01''+G01=c/2+s-(3/2)[c cos(2beta)+s sin(2beta)]
              <=s-c<=0.                          (18)

For 0<=beta<=p the bracket is cos(2beta-p)>=c. On a piece with p<=beta<=pi/4 the quadratic part is instead

    (c-s)h^2+(c+s)hr+s,

and

    G01''+G01=(c+s)/2
       -(3/2)[(c-s)cos(2beta)+(c+s)sin(2beta)]
       <=-(c+s)<0.                               (19)

The bracket equals cos(2beta-p)+sin(2beta-p)>=c+s on this interval. Subdivide at whichever of p and q occur. At beta=q the value is G00(p,q,q), hence is nonnegative by (8). At beta=p it is the strictly positive (12). At beta=0 it is

    1-c-.086s+s[d(1-d)+.06dt]>0,                   (20)

because 1-c-.086s=s(tan(p/2)-.086)>0. The endpoint beta=pi/4 is checked next. Equations (18)--(20) and sine interpolation therefore handle the entire lower interval.

### 4.2. The range beta>=pi/4

Here both relevant signs have been fixed, and (5) becomes

    G01=(c-s)h^2+(c+s)hr+s-Pcal h-Qcal r,
    Pcal=2c+alpha s-1+sP(q),
    Qcal=s(2-Q(q)).                               (21)

Put L=c+s. Equations (10) imply

    0<Pcal<L, 0<=Qcal<=s,
    L-Pcal=s[tan(p/2)-.086-P(q)]>0.                (22)

At beta=pi/4,

    sqrt(2)G01=sqrt(2)L-Pcal-Qcal
       >1-.586c-.782s
       >=1-sqrt(.95492)>0.                        (23)

Here (11) gives Pcal+Qcal<2c+2.196s-1. At beta=pi/2 the value is s-Qcal>=0.

For a proof throughout this upper interval, put z=h/(1+r), so 0<=z<=rho=sqrt(2)-1. Multiplication of (21) by (1+z^2)^2 gives the exact quartic

    (s-Qcal)+2(L-Pcal)z+(4c-2s)z^2
             -2(L+Pcal)z^3+(s+Qcal)z^4.           (24)

Write this quartic in the degree-four Bernstein basis on [0,rho]. Its five coefficients are nonnegative. Explicitly, the first is s-Qcal, the second adds (L-Pcal)rho/2, and the third adds (L-Pcal)rho+(4c-2s)rho^2/6 to the first. These signs follow from (22). The fourth coefficient is

    s-Qcal+1.5(L-Pcal)rho+(2c-s)rho^2
                                      -.5(L+Pcal)rho^3>0: (25)

its last two terms are greater than .7(.17)-.5(2.83)(.072)=.01712. The fifth coefficient is the positive endpoint (1+rho^2)^2G01(pi/4), proved in (23). Nonnegativity of every Bernstein basis function proves (24) nonnegative. This completes G01.

## 5. The C support is largest at a clamped angle

For beta<=p, expansion of (2) gives

    FC=(-c-s+.586cs)h
              +(c-s+.5c^2+alpha s^2)r.             (26)

The two coefficient derivatives with respect to p are

    (c-s)[-1+.586(c+s)]<=0,
    -(c+s)+1.172cs<0.                              (27)

For beta>=p the expansion is

    FC=(-c+s+.086cs-s^2)h
              +[1+.086s^2+cs-(c+s)]r,               (28)

and the derivatives are

    c+s+.086(c^2-s^2)-2cs>0,
    .172cs+(c-s)(c+s-1)>0.                         (29)

Thus for fixed beta the maximum of FC over p0<=p<=pi/4 occurs at

    p*=p0                  if beta<=p0,
    p*=beta                if p0<=beta<=pi/4,
    p*=pi/4                if beta>=pi/4.          (30)

This is solely a scalar bound. It changes no actual square in the geometric application. In (6)--(7), every other term is independent of p and FC has a nonpositive coefficient. Therefore their lower bounds may use (30).

For later reference these two endpoint caps are

    FC=-a0 h+b0 r       at p=p0,
    a0=3496/3125=1.11872, b0=11387/12500=.91096;    (31)

    FC=-.457h+v0r       at p=pi/4,
    v0=1.543-sqrt(2), 0<v0<.129.                  (32)

On the middle interval p*=beta, G10 is exactly G00(beta,q,beta) and is nonnegative by (8). On that same interval G11 is the strictly positive T(beta,q). It remains to check (31) and (32).

## 6. A short uniform E bound for beta<=p0

**Lemma 2.** For all 0<=beta<=p0 and 0<=q<=pi/4,

    FE(beta)<=h-.56r-1+.00032.                    (33)

**Proof.** If q>=beta, put j=sin(q-beta)>=0. The derivative of (3) with respect to q is the expression (17), now with beta fixed. Since j/kE<=t/d,

    (dFE/dq)/kE
      <=t(1/d-2)+.06(1-2d^2)/d<0.                 (34)

Thus this interval is bounded by its aligned value h-.56r-1.

Take q<=beta. Then FE=Ph-Qr. Both P' and Q' are positive by Section 2. When q<=pi/6,

    dFE/dq>=.8P'-.6Q'=g(q),
    g=.8t-.6d-.432dt+.712(d^2-t^2)>0.              (35)

For completeness,

    g''=-.8t+.6d+1.728dt-2.848(d^2-t^2)
          <=-2.248+.928t+5.696t^2<=-.36

on t<=.5. Thus g is concave, and its endpoints are .112 and .756-.408sqrt(3)>0. This proves (35).

For pi/6<=q<=beta<=p0 the correct second derivative is

    d^2FE/dq^2=h P''-r Q''<=-.16.                 (36)

Here P''<=-.2 on 0<=q<=p0. With y=tan(q/2)<=1/3, the exact verification is

    (P''+.2)(1+y^2)^2
       =-(2y/25)(25y^3-44y^2-95y+44)<=0,          (37)

because the parenthesis is at least 44-44/9-95/3=67/9. Also, on q>=pi/6, t>=.5,d>=.8 give

    Q''=t(2.4d-1)-.88+1.76t^2
          >=.92t-.88+1.76t^2>=.02.

This proves (36), since h>=.8. At the aligned endpoint q=beta the left derivative is exactly

    .44h-.6r>=-.008.                              (38)

If this derivative is nonnegative, monotonicity on the lower interval and concavity on the upper interval make the aligned value maximal. Otherwise the concave Taylor bound using even the weaker second-derivative estimate -.1 limits the excess over the aligned value by

    .008^2/(2(.1))=.00032.

Indeed for w=beta-q>=0 the excess is at most .008w-.05w^2. The monotone interval (35) cannot supply a larger maximum than the start of the concave interval. This also covers beta<=pi/6, where the whole range q<=beta is monotone. The three ranges exhaust q, proving (33). ∎

## 7. The G11 endpoint ranges

For beta<=p0, use (31) and (33). Then

    G11>=D(beta)-.00032r,
    D=h+2r-2+a0h^2-(1+b0)hr+.56r^2.               (39)

For z=tan(beta/2) in [0,1/3], exact substitution gives

    (D-1/3125)(1+z^2)^2
      =(1-3z)(3920z^3-14989z^2+3333z+740)/6250
      >=0.                                       (40)

The cubic is concave on this interval: its second derivative is -29978+23520z<0. Its endpoint values are 740 and 8930/27, both positive. Consequently, since r<=.6,

    G11>=.00032(1-r)>=.000128=2/15625>0.            (41)

For beta>=pi/4 use (32) and (9):

    G11=h+r-2+.457h^2-(v0+P)hr+Qr^2.              (42)

Set A=.457, B=-(v0+P), C=Q. The bounds are -.342<B<=0 and 1<=C<1.188. Direct differentiation gives

    G11''+G11=(A+C)/2-2
             -(3/2)(A-C)cos(2beta)-(3/2)B sin(2beta)<0. (43)

Indeed A-C<0 and cos(2beta)<=0, so that term is nonpositive; the remaining upper bound is (.457+1.188)/2-2+1.5(.342)<0. At beta=pi/4 the value is T(pi/4,q)>0, and at beta=pi/2 it is Q-1>=0. Sine interpolation proves G11>=0 on this whole range. Together with Section 5, this completes G11.

## 8. The G10 endpoint ranges

### 8.1. The range beta<=p0

Use (31). If q<=beta, direct expansion of (6) gives

    G10=P1d+Q1t+r,
    P1=1+hr-2h-r-FC,
    Q1=r^2-1.44r<=0.                              (44)

This decreases with q on [0,beta]. If P1>=0, its derivative -P1t+Q1d is nonpositive. If P1<0, that derivative increases with q and its endpoint value is nonpositive because

    P1-h(r-1.44)=1-.56h-r-FC
        =1+.55872h-1.91096r>=.3004>0.              (45)

The last expression decreases with beta and has the stated value at p0. Therefore (44) is at least its value at q=beta, which is exactly D(beta)>=1/3125 by (40).

If q>=beta, the expansion is instead

    G10=P2d+Q2t+r,
    P2=h(h+r)-2h-r-FC,
    Q2=r(h+r-1.44),    -.44r<=Q2<=0.               (46)

When P2>=0, the expression is at least r(1-.44/sqrt(2))>0 if r>0; at r=0 the term P2d=(a0-1)d is positive.

Suppose P2<0. At q=beta the q-derivative equals

    r[-.55872h+1.91096r].                          (47)

If the bracket is nonnegative, the derivative increases afterwards, since P2,Q2<0. Thus again the minimum is the aligned value D(beta)>0.

If the bracket is negative, set w=r/h. Then w<.293 and h>.959, the latter following from .959^2(1+.293^2)<1. An exact rearrangement gives

    P2+.7r=h[h(1+w)-.88128-1.21096w]
       >h[.07772-.25196(.293)]>0.                 (48)

Consequently -.7r<P2<0 and -.44r<=Q2<=0. Cauchy--Schwarz in (46) now gives

    G10>r[1-sqrt(.7^2+.44^2)]>0.                  (49)

Here r cannot vanish because P2<0. This proves the entire lower endpoint range.

### 8.2. The range beta>=pi/4

Now q<=beta. Substituting (32) into (44) gives

    P1=1+hr-1.543h-(2.543-sqrt(2))r,
    Q1=r^2-1.44r<0.                               (50)

We first prove P1>Q1. Put w=h/r in [0,1]. Then

    (h+r)=(1+w)/sqrt(1+w^2)>=1+.4w.               (51)

Squaring proves this because the numerator difference is

    w(1.2-.16w-.8w^2-.16w^3)>=.08w.

Thus

    (P1-Q1)/r=w(h+r-1.543)+sqrt(2)-1.103
       >-.543^2/1.6+.311>0.                      (52)

If P1>=0 the derivative -P1t+Q1d is negative. If P1<0, use P1>Q1 and d>=t to reach the same weak sign. Hence G10 is minimized at q=pi/4. There its value is

    (1/sqrt(2))[1+hr+r^2-1.543h-Cstar r],
    Cstar=3.983-2sqrt(2)<sqrt(2).                  (53)

The beta-derivative of the bracket is

    h^2-r^2+2hr+1.543r-Cstar h
       >=r(1.543-r)+h(2r-Cstar)>0,                (54)

since r>=1/sqrt(2). Its minimum is therefore the beta=pi/4 endpoint, whose value is

    2sqrt(2)-2.763>0.                             (55)

This completes G10 and hence Theorem 1. Every subdivision used a full interval, an exact coefficient sign, or a positive polynomial identity; no angle samples or replacement-square feasibility assumptions enter the proof. ∎
