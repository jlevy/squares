# C1092 MPPM: continuous wall scalars for a steep positive square and a missing-forward negative successor

This is a pure scalar theorem. Every terminating decimal is an exact rational. All angle intervals, including their endpoints, are treated continuously. The allowance epsilon below retains the unconditional positive cap 1.086 sin(p); no preceding-origin exclusion is hidden in this algebra.

## 1. Definitions and theorem

Put

    p0=2 atan(1/3), q0=2 atan(7/18),
    p0<=p<=pi/4, q0<=q<=pi/4, 0<=beta<=pi/2,
    c=cos p, s=sin p, d=cos q, t=sin q,
    h=cos beta, r=sin beta, Theta=pi/2-q,
    0<=epsilon<=.086.

Write H=h+r and

    ell=ct+sd,
    kC=ch+sr, deltaC=cr-sh,
    kE=th+dr, deltaE=tr-dh,
    WC=kC+|deltaC|, WE=kE+|deltaE|,
    C0=s-1, E0=t-.56d-1.                          (1)

Define the unperturbed C cap

    FC=.5c deltaC+kC s-(kC-deltaC)  if beta<=p,
    FC=deltaC(c+s)+kC s-(kC+deltaC) if beta>=p.     (2)

For alpha=dh-tr=-deltaE and mu=th+dr=kE define

    FE=alpha(d+t-1)+mu E0       if beta<=Theta,
    FE=alpha(1+.26t)+mu E0      if beta>=Theta.    (3)

The formulas agree at their joining angles. Set

    G00=.5[ell H+t WC+s WE]-2ell-t C0-s E0;
    G01=.5[kC H+h WC+s]-2kC-h C0-s FE;
    G10=.5[kE H+t+r WE]-2kE-t FC-r E0;
    G11=H-2-h FC-r FE.                           (4)

The four quantities actually needed are

    G00*=G00-epsilon st;
    G01*=G01-epsilon sh;
    G10*=G10-epsilon st kC;
    G11*=G11-epsilon sh kC.                      (5)

**Theorem 1.** All four quantities in (5) are strictly positive throughout the full closed angle domain.

The endpoint of q has

    d0=275/373, t0=252/373.

The following bounds will be used repeatedly:

    .7<c<=.8, .6<=s<.71, c+s>=1.4;
    .7<d<.738, .675<t<.71, d+t>1.41;
    t^2>.45, dt>.49, d/t<11/10,
    0<ell<=1, 0<kC<=1.                         (6)

They follow from the two displayed angle intervals and their exact endpoints. On pi/4<=beta<=Theta, in addition,

    h^2>.45, r^2>=.5, hr>.49,
    .675<h<.71, .7<r<.738,
    H>1.41, r/h<11/10.                          (7)

## 2. The successor cap and the C maximum

Expand FE as A1 h+B1 r below Theta and A2 h+B2 r above Theta. Direct calculation gives

    A1=1-d-t+.44dt,
    B1=t-d-.56-.44t^2,
    A2=d-t+t^2-.30dt,
    B2=-d-t-.56+.30t^2+dt.                      (8)

Consequently

    FE<=-.19h-.78r       if beta<=Theta,
    FE< .37h-1.32r       if beta>=Theta.         (9)

Indeed A1<1-1.41+.22=-.19. Also B1'=d+t-.88dt>0, so its maximum at pi/4 is exactly -.78. The coefficient A2 decreases, since

    A2'=-(d+t)+2dt-.30(d^2-t^2)<0,

and A2(q0)=51293/139129<.37. Finally

    B2'=(d-t)(d+t-1)+.60dt>0,

so B2<=.09-sqrt(2)<-1.32.

For fixed beta the maximum of FC over p0<=p<=pi/4 is

    -1.16h+.88r              if beta<=p0;
    r-1                     if p0<=beta<=pi/4;
    -.5h+f r                if beta>=pi/4,
    f=1.5-sqrt(2), 0<f<.09.                      (10)

For completeness, below the join beta=p the h,r coefficient derivatives of FC with respect to p are

    (c-s)[-1+.5(c+s)]<=0,  -(c+s)+cs<0.

Above the join they are

    c+s-2cs>0,  (c-s)(c+s-1)>=0.

These prove exactly the clamped maximum (10). Its use is a scalar optimization and never changes an actual square in the application.

## 3. The central/central quantity G00*

The exact width combination W=ell H+t WC+s WE is

    (2ell+2st)h+2sd r       for beta<=p;
    2ell H                 for p<=beta<=Theta;
    2ct h+(2ell+2st)r       for beta>=Theta.      (11)

Each piece is a positive sine-cosine combination and is concave. It therefore suffices to check its interval endpoints. At beta=p or Theta its value is respectively 2ell(c+s) or 2ell(d+t), both at least 2.8ell. At beta=0 or pi/2 it is 2ell+2st, also greater than 2.8ell because

    ell/(st)=c/s+d/t<4/3+11/10=73/30<5/2.

Thus W>=2.8ell. Substitution into (4) gives

    G00>=s+t-2st+.56sd-.6ell>.0492.             (12)

Here s,t>1/2 make s+t-2st decreasing in either variable. Hence it is at least sqrt(2)-1>.414; moreover sd>.42 and ell<=1. These yield .414+.56(.42)-.6=.0492 exactly. Since epsilon st<=.043, (12) proves G00*>.0062.

## 4. The boundary/central quantity G10*

For beta<=Theta, exact expansion yields

    G10=t[hH-2h-r-FC]+dr(H-1.44)+r.              (13)

For beta>=Theta it instead gives

    G10=t[1+hr-2h-r-FC]+dr(r-1.44)+r.            (14)

### 4.1. The interval beta<=p0

Use (10), and put

    A=hH-.84h-1.88r, B=r(H-1.44)<0.

Then G10>=tA+dB+r. If A>=0, the bound B>=-.44r and d<.75 give G10>=tA+.67r. When r>=.1 this is at least .067. When r<=.1, h>.99 and

    A>=.16-r^2-.89r>=.16-.99r,

so G10>.675(.16-.99r)+.67r>=.108.

If A<0, use d,t<.75 to get

    G10>psi=.75-.63h-1.49r+1.5hr.

Here psi'(0)=.01 and

    psi'''=-.63r+1.49h-6(h^2-r^2)<-.19,

because h^2-r^2>=.28. Thus psi' is concave and, being positive at zero, cannot create an interior minimum of psi. The minimum is at an endpoint. Those endpoint values are psi(0)=.12 and psi(p0)=.072. Every subcase gives G10>.0492.

### 4.2. The interval p0<=beta<=pi/4

The middle maximum in (10) makes (13) exactly G00 with p replaced by beta. This lies in its proved domain, so G10>.0492 by (12).

### 4.3. The interval pi/4<=beta<=Theta

Use the last maximum in (10). In (13) both coefficients of t,d are negative. Bounds (7) give

    h(H-1.5)-(1+f)r>=-.09h-1.09r,
    r(H-1.44)>=-.03r.

Therefore d,t<.75 imply

    G10>.16r-.0675h>=.0925r>.06475.

### 4.4. The interval beta>=Theta

The corresponding t coefficient in (14) is

    A*=1+hr-1.5h-(1+f)r<0.

For h>0 this follows from

    1-r+h(r-1.5)
      =h[h/(1+r)+r-1.5]<0;

use h/(1+r)<=sqrt(2)-1<.415 and r<=1. At h=0, A*=-f<0 directly. The d coefficient is also negative. Thus

    G10>psi*=.75+.75hr-1.125h+.75r^2-.8975r.

On beta>=pi/4 its derivative is positive: after discarding a nonnegative .75h^2 term it is at least

    r(1.125-.75r)+h(1.5r-.8975)>0.

The endpoint value is

    psi*(pi/4)=1.5-2.0225/sqrt(2)>.064025.

These intervals prove G10>.0492 everywhere. Since epsilon st kC<=.043, G10*>.0062.

## 5. The boundary/boundary quantity G11*

The perturbation admits the uniform bound

    epsilon sh kC
      =epsilon h(cs h+s^2r)<=.043hH<=.045hH.     (15)

The last inequality is strict when h>0; at h=0 both sides vanish and the positive endpoint bounds below remain valid.

### 5.1. The interval beta<=p0

Use the first bounds in (9),(10), then (15). This gives

    G11*>H-.885-.335r^2-.735hr
          >=H-.885-1.07hr
           =H-.35-.535H^2.

Here r<=h and 1<=H<=1.4. The final quadratic is concave and its endpoint values are .115 and .0014. Thus this whole interval is strictly positive.

### 5.2. The interval p0<=beta<=pi/4

The corresponding bound is

    g=2h+r-2.045-.855hr+.825r^2.                 (16)

It is concave. Indeed

    g''=-2h-r+1.65 cos(2beta)+1.71 sin(2beta).

The last two terms decrease on this interval, since their derivative in 2beta is at most -1.65(.96)+1.71(.28)<0. Their maximum is 2.1036, while 2h+r>=3/sqrt(2)>2.12. Hence g''<0. The endpoint values are .0416 and 3/sqrt(2)-2.06>.06. This proves positivity.

### 5.3. The interval pi/4<=beta<=Theta

The first FE bound still applies. Before the perturbation the lower bound is

    H-2+.5h^2+.10hr+.78r^2>.074

by (7). Since hH<=1 on beta>=pi/4, (15) loses less than .045. Thus G11*>.029.

### 5.4. The interval beta>=Theta

Use the second FE bound in (9). A lower bound after (15) is

    g=H-1.545+.865r^2-.505hr.                    (17)

Its second derivative is -H+1.73 cos(2beta)+2.02hr<0. In fact cos(2beta)<=0, and H>=1+.8hr, so this is at most -1+1.22hr<=-.39. The minimum is therefore at pi/4 or pi/2, where the values are sqrt(2)-1.365>.045 and .32. This finishes G11*.

## 6. The central/boundary quantity G01*

There are two exact forms, according to beta relative to p:

    G01=c h(h-2)+s[1+hr-2r-h-FE]+h      if beta<=p;
    G01=c h(H-2)+s[r(H-2)-h-FE]+h       if beta>=p. (18)

First we give unperturbed bounds below Theta; their reserves exceed the perturbation epsilon sh<.06106.

### 6.1. The interval beta<=p0

The first bound in (9) gives

    G01>=c A+s B+h,
    A=h(h-2)<0,
    B=1+hr-1.22r-.81h>0.

The last sign follows from 1+hr>=h+r and r/h<=3/4: B>=.19h-.22r>=.025h. Hence c<=.8 and s>=.6 give

    G01>=g=.8h^2+.6hr+.6-1.086h-.732r.

This g is concave on [0,p0]. Its second derivative is bounded above by

    h^2[1.6v^2-1.485v-.2425], v=r/h in [0,3/4],

using h>=.8 in the two positive linear terms of g''. The bracket is a convex quadratic with negative values -.2425 and -.45625 at its endpoints, so it is negative throughout. The endpoint values of g are .314 and .092. Therefore G01>=.092 and G01*>0.

### 6.2. The interval p0<=beta<=pi/4

After replacing FE by -.19h-.78r, the first expression in (18) increases with p when p>=beta. Its coefficient B is positive because

    B>=1.48-2.03/sqrt(2)>0.

For p<=beta the second expression decreases with p. To check this, set A=h(H-2)<0 and B=r(H-1.22)-.81h; its derivative divided by c is at most

    -(r/h)A+B=.78r-.81h<0.

Thus the minimum over p occurs at p=beta. Its value is at least

    g=2h+r-2-.81hr+.78r^2.

Here g''=-2h-r+1.56 cos(2beta)+3.24hr<0, using 2h+r>2.1, cos(2beta)<=.28 and hr<=.5. Its endpoint values are .092 and 3/sqrt(2)-2.015>.105. Consequently G01>=.092 and G01*>0.

### 6.3. The interval pi/4<=beta<=Theta

Use the same second expression and FE bound. It decreases in p: its derivative divided by c is at most

    -A+B=h[(r/h-1)(H-1.22)-.03]<-.01h,

by (7). Its minimum is therefore at p=pi/4, giving

    g=h+[H^2-2.81h-1.22r]/sqrt(2).               (19)

This g increases on [pi/4,pi/2-q0]. Its second derivative is negative by (7), and the derivative at the right endpoint is

    -275/373+14931863/[13912900 sqrt(2)]>.011.

For the last inequality use 14931863/13912900>1.07, 1/sqrt(2)>.7 and 275/373<.738. Thus g>=g(pi/4)=3/sqrt(2)-2.015>.106, and the perturbation again leaves a positive result.

### 6.4. The interval beta>=Theta

We include the perturbation directly. The second bound in (9), epsilon<.09 and (18) give

    G01*>=c A+s B+h,
    A=h(H-2)<=0,
    B=r(H-.68)-1.46h.                            (20)

If B>=0 and h>0 this is at least h[1-.8(2-H)]>=.2h>0. If h=0 it is at least .32s>0.

If B<0, use c<=.8 and s<.71 in (20). With u=h/r in [0,1] the result is at least r J(u), where

    J(u)=(.8u+.71)(1+u)/sqrt(1+u^2)
                    -1.6366u-.4828.             (21)

For 0<=u<=1/4, the square-root ratio is at least 1, giving J>=.2272-.8366u>=.01805. For 1/4<=u<=1,

    J''=(.62u^2-4.53u+.89)/(1+u^2)^(5/2)<0.

The numerator decreases on [1/4,1] and at 1/4 equals -.20375. Thus J has its minimum at an endpoint. The already checked endpoint 1/4 is positive, while

    J(1)=1.51sqrt(2)-2.1194>.01574,

using sqrt(2)>1.414. Therefore (20) is positive in every remaining case. This proves G01* and completes Theorem 1.

All proofs used one fixed continuous triangle or angle interval, elementary concavity, and exact rational bounds. The positive quantities in (5) are the four possible supports of the same boundary square in the companion application; they are not independently chosen angle samples.
