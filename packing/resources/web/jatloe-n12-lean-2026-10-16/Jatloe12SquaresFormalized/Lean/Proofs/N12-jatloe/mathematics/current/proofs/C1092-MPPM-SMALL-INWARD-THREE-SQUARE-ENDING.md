# C1092 MPPM: a missing-center small inward square, its successor and their shared wall

All terminating decimals are exact rationals. Named squares are the actual
open squares, with common side a>1 and pairwise disjoint interiors. Strict
ownership is distinguished from weak exclusion, real-wall and separating
equalities throughout. No upper bound on a is used in the local theorem.

## 1. The actual three-square statement

**Theorem 1.** Let C have a nonpositive canonical orientation and strictly own

    M_C=(-.35,-.35), I=(0,-.26), J=(-.26,0),
    X=(-.5,0), T=(-.01,-.54),

while excluding O=(0,0) and G=(-1,-.4). Let the actual bottom square B
strictly own

    S=(0,-1.086), A_B=(-.26,-1), F_B=(-.56,-1),

have its closure in y>=-2, and have actual center abscissa X_B<=0.
Let the actual ordinary successor E strictly own

    M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1), Y=(.5,-1),

and exclude

    I, T, G_E=(1,-.4), K0=(1,-1),
    S=(0,-1.086), O_R=(1,0).

Then C,B,E cannot have pairwise disjoint interiors.

The exclusions I,T,S already follow from their strict ownership in the
named different squares. The other exclusions are ordinary point
exclusions; no artificial owner for a missing point is required. In the
original application all have actual strict owners as recorded in Section7.

Use the negative frame of C and the negative frame of E, once established,

    u=(c,-s), v=(s,c),       p=arctan(s/c),
    u_E=(d,-t), v_E=(t,d),   q=arctan(t/d).

Their lower and upper faces are denoted respectively by

    C: U,V; A=U+a,H=V+a,
    E: L,W; J_E=L+a,K_E=W+a.

The proof retains both the actual C--B and actual C--E separations before
testing the actual B--E separation. None of these pairs is replaced by a
different square with the same anchors.

## 2. Reviewed entrance and a sharper successor angle

The axial C case is impossible because strict I,J would put O in C.
The complete actual bottom-square theorem in
C1092-MPPM-INWARD-BOTTOM-ANGLE.md, Theorem1, applies literally to C,B. It gives

    0<x:=s/(1+c)<alpha:=1-2sqrt(5)/5<53/500,
    c>.97, 0<s<.21,                                  (1)

and its direct point-face proof gives

    U>=-c+.4s, A>=a-c+.4s>0,
    V<=-a, H<=0, U<-.5c.                             (2)

Define

    Q=1-c+.4s,
    J0=c+s-1-cs+.4s^2=s(Q-x).

The exact threshold identity of that theorem implies J0<0. We will also
use the elementary stronger quantitative bound

    0<-J0=s^2[(1-s)/(1+c)-.4]<=s^2/10.              (3)

Indeed (1-s)/(1+c)<=1/2 is equivalent to 1-c<=2s, which follows from
1-c=s^2/(1+c) and 0<s<1.

Theorem1 of C1092-MPPM-SMALL-INWARD-SUCCESSOR.md now applies to the actual
C,E. Its complete sign and face proof gives strictly negative E and

    L>=.26t, J_E<=d+t,
    W>=-1.086d, K_E<=t-.4d.                         (4)

In particular

    1<a<=t+.686d,
    t>1/3.                                         (5)

For the second assertion, sin q+.686 cos q increases on the canonical
interval. If t<=1/3 its value is at most

    [1+(343/250)sqrt(2)]/3<518/525<1,

using sqrt(2)<10/7. This contradicts the first inequality in (5).
Since s<.21<1/3<t, we have q>p.

We next prove the new exact upper bound

    q<q0:=2 arctan(1/4),
    d>15/17, t<8/17.                               (6)

Orient a C--E separating normal from C toward E. The marker difference
forces n_x>0, and the strict pair I,Y forces n_y<(25/37)n_x. Both upward
normals v and v_E are therefore ineligible. The only possible sources are
u and u_E. Put

    kappa=cd+st=cos(q-p)>0,
    delta=ct-sd=sin(q-p)>0.

On these two sources, (2),(4) give the following strict lower bounds for
upper_C(n)-lower_E(n):

    F_C=Q+kappa(1-d-t)+delta(1-t+.4d),
    F_E=1-d-t+kappa Q+delta.                        (7)

In each case the coefficient of a replaced by1 is 1+kappa+delta>0.
Thus a>1 makes the comparison strict even if all preceding exits or
separating faces meet with equality.

For fixed p, direct differentiation gives

    dF_C/dq
      =c(d-t)[1-.6(d+t)]+s[d+t-1.2dt]>0           (8)

throughout 0<=q<=pi/4. Both bracketed expressions are positive; at the
diagonal endpoint the second summand remains positive.

For the second expression, write

    F_E=1-A0 d-B0 t,
    A0=1+s-cQ>.97, B0=1-c-sQ=-J0,
    0<B0<.00441.

The bound for A0 follows from

    A0=1-c+c^2+s(1-.4c)>1-.97+.97^2>.97.

If q>=q0, then dF_E/dq=A0 t-B0 d>.97(8/17)-.00441>0.
At q=q0, the two exact endpoint identities are

    1445(1+x^2) F_C(q0)=150-1574x+2740x^2,

    85(1+x^2)^2 F_E(q0)
      =10-90x+154x^2-50x^3-220x^4.                 (9)

Both right sides decrease on 0<=x<=53/500. Their derivatives are
5480x-1574<0 and -90+308x-150x^2-880x^3<0 respectively. Their values at
53/500 are the strictly positive rationals

    174283/12500,
    6571933459/3125000000.

Consequently both sources in (7) fail whenever q>=q0. This proves (6)
without an angle subdivision or a polynomial coefficient table.

## 3. The actual C--B separation fixes the bottom source and its angle

Give B its signed canonical frame

    w=(h,k), z=(-k,h), h>=|k|, h^2+k^2=1,
    beta=arctan(k/h),

and denote its upper w,z faces by J_B,D_B. Its lower z face is D_B-a.
We prove

    -.043<k<.021, h>.999,                          (10)

and, for the actual C--B separation,

    gamma=ck+sh=sin(p+beta)>0,
    lambda=ch-sk=cos(p+beta)>0,
    D_B<=-gamma A+lambda V.                        (11)

Here (11) says that the separating direction is B's own upward normal z.

The complete normal cover and actual support bounds in
C1092-MPPM-INWARD-BOTTOM-ANGLE.md, Sections2--4 and6--8, require only the
data of the present theorem. Their use below does not assume the contrary
large-angle regime considered in that chapter. Specifically:

* Strict I,S give n_y>0 on a B-to-C normal, while T,F_B give
  .55n_x+.46n_y>0. The C normal -u and the negative-B upper-left normal
  are therefore impossible.
* The C normal v is impossible for either sign of B by the exact
  norm comparisons in Sections3 and8 of that chapter. Those comparisons
  use only (2), the strict B marker and anchors, and its genuine bottom wall.
* When k<=0, the upper transverse B face obeys D_B>-1. This follows from
  the actual marker and bottom wall as in Section6 of that chapter and
  contains no inward-angle threshold assumption.

For completeness, the last fact follows by putting l=-k>=0. Marker
ownership gives J_B>1.086l and D_B>-1.086h. The actual wall gives

    D_B>=a+(1.086l^2-2)/h.

If h<=10/11, the marker bound is already greater than -1. If h>=10/11,

    2h+1.086(1-h^2)-2=(1-h)[1.086(1+h)-2]>=0,

so the wall inequality and a>1 give D_B>-1, including the axial endpoint.

### 3.1. Nonnegative B

The only potential B sources are w and z. The full support estimate for w
from the reviewed bottom-angle proof is

    upper_B(w)-lower_C(w)
      >h(.5c^2+s)+k(c-.5cs-1.086).

The first coefficient is positive, and their sum is

    c+s+.5c(c-s)-1.086
      >.97+.5(.97)(.76)-1.086>.25.

Since 0<=k<=h, this source is impossible. Thus the actual source is z,
and (11) follows; both gamma,lambda are positive.

The physical bottom wall and the actual center condition X_B<=0 give

    D_B=-kX_B+hY_B+a/2
      >=-2h+(a/2)[1+h(h+k)].                       (12)

Combining (12) with (11),(2), then strictly replacing a by1, requires

    F=h J0+(1-h)^2/2+k(.5h+B0)<0,
    B0=c-s-c^2+.4cs.                               (13)

This is exactly the wall expression in the earlier proof, rearranged;
it can also be checked directly by expanding (12). Now B0>-.13 because

    B0=c-c^2-s(1-.4c)>=-s(1-.4c)>-.21(.612)>-.13.

As h>=1/sqrt(2)>.7, we have .5h+B0>.22. Since J0<0 and h<=1,
(13) and (3) imply

    0<=k<-J0/.22< (5/11)s^2<.021.                 (14)

### 3.2. Negative B

Write phi=-beta>0. If phi>=p, B's upward normal has C components
sin(phi-p)>=0 and cos(phi-p)>0. Equation(2) gives

    lower_C(z)<-[cos(phi-p)+.5c sin(phi-p)]<=-1.

The last weak inequality holds on the full angle order: with
r=phi-p in [0,pi/4-p],

    tan(r/2)<c/2,

as shown directly in Section7 of the bottom-angle theorem. It also follows
from

    tan((pi/4-p)/2)=(c-s)/(sqrt(2)+c+s)<c/2.

This contradicts D_B>-1. Hence 0<phi<p, proving the positive component
signs and the exact source formula (11).

Using A>=a-c+.4s and V<=-a in (11), together with D_B>-1, gives

    cos(p-phi)+Q sin(p-phi)<1,
    Q<tan((p-phi)/2).                              (15)

On the other hand

    Q-.4 tan p=(1-c)(1-.4s/c)>0,
    tan(.4p)<=.4 tan p.

The second inequality is convexity of tan on this nonnegative interval.
Equation(15) therefore yields phi<p/5. Since p=2 arctan x<2x<.212,

    0<-k=sin phi<.0424<.043.                       (16)

Together, (14),(16) prove (10): in particular
.999^2+.043^2<1, so h>.999 in both signs. All closed canonical endpoints
were included in the eliminated sources; the remaining inequalities are
strict consequences of the actual square separation.

## 4. The complete B--E normal cover and common estimates

Orient a separating normal from B toward E. The actual pair A_B,B0 forces
n_x>0, and the marker pair S,M_E forces

    .35n_x+.736n_y>0.                              (17)

For k>=0, B's normal z has nonpositive x component and -z fails (17),
since .35k-.736h<0. Thus only w remains from B. For k<0, both w and z
remain. E's two right-facing normals are u_E and v_E. All its other
normals and all other B normals have been excluded. We must therefore
treat exactly

    w, u_E, v_E; and also z when k<0.              (18)

Set

    nu=dh-tk=cos(q+beta),
    eta=th+dk=sin(q+beta).

Equations(1),(5),(6),(10) give nu>0 and the convenient rational estimates

    eta>7/25, lambda>24/25,
    .88<d<=1, 1/3<t<.48,
    h>.999, -.043<k<.021.                          (19)

For example eta>(.999)/3-.043=.29>7/25, and
lambda>.97(.999)-.21(.021)>.96. Also
nu>.88(.999)-.48(.021)>0. These estimates are used only after the exact
angle reductions, on the same actual B.

### 4.1. The B source w

The components of w in E are nu,eta>0. By (4) and a>1,

    lower_E(w)=nu L+eta W<h X0+k Y0,
    X0=1-d-t+.6dt,
    Y0=t-d-1+.6d^2.

Strict S ownership gives J_B>-1.086k. Moreover

    X0=dt[.6-2/(1+d+t)]<-dt/5<-1/17,              (20)

using d+t<sqrt(2)<3/2 and dt>(15/17)(1/3)=5/17.
Equation(5) gives

    Y0+1.086
      >1.086-1.686d+.6d^2
       =(1-d)(1.086-.6d)>=0.

The same quantity is less than .48-.88+.6+.086<.3. Therefore, for
either sign of k,

    lower_E(w)-upper_B(w)
      <hX0+k(Y0+1.086)
      <-.999/17+.021(.3)<-1/20.                   (21)

This source cannot separate.

### 4.2. The E source u_E

The actual C--B relation (11) and (2) give D_B<-lambda a, because
gamma,A are positive. Thus B's lower transverse face obeys

    D_B-a<-a(1+lambda).

Consequently

    upper_B(u_E)=nu J_B-eta(D_B-a)
      >-1.086nu k+a eta(1+lambda)
      >-(1.086)(.021)+(7/25)(49/25)
       =262997/500000>1/2.                         (22)

When k<0 the marker term is positive, so the same displayed lower bound
remains valid. But (4),(6) give

    lower_E(u_E)=L<d+t-1<6/17<1/2.

This is a contradiction on u_E.

## 5. The E source v_E

Put

    Delta0=1-t-.6d>0.                              (23)

Indeed sin q+.6cos q increases throughout the canonical interval and
equals1 exactly at q0; use (6). The upper B support on v_E is
eta J_B+nu D_B, whereas (4) gives

    lower_E(v_E)=W<t-.4d-1.

### 5.1. Nonnegative B

The strict a>1 step in (12) gives

    D_B>-1+.5hk>=-1+.49k.

To see the first inequality directly, at a=1 the difference from
-1+.5hk is (h-1)(h-3)/2>=0. The strictness follows from the positive
coefficient of a in (12).

Using the marker bound J_B>-1.086k, the exact support difference is
strictly greater than

    Delta0+d(1-h)+k Z0,
    Z0=.49dh+t(1-1.086h)-k(.49t+1.086d).           (24)

The coarse rational estimates in (19) prove

    Z0>.49(.88)(.999)-.086(.48)
          -.021[.49(.48)+1.086]>1/3.

Thus (24) is positive, including k=0 because Delta0>0. This defeats v_E
for every nonnegative B.

### 5.2. Negative B

Write l=-k>0. We have J_B>1.086l and D_B>-1, and now
nu=dh+tl, eta=th-dl. The exact support difference is strictly greater than

    Delta0+d l^2[1/(1+h)-1.086]
               +t l(1.086h-1).                  (25)

Since 0<l<.043, h>.999, t>1/3 and d<=1, expression(25) is greater than

    Delta0+l[-.586(.043)+(1/3)(1.086(.999)-1)]
      =Delta0+(233/75000)l>0.                     (26)

Here 1/(1+h)>=1/2 justifies the negative quadratic estimate; the factor
1.086h-1 is positive, so multiplying its lower bound by t>1/3 preserves
the direction. Thus v_E is impossible for negative B as well.

## 6. The remaining B source z for negative B

Only k<0 requires this final source. Its components on E are -eta,nu,
so

    lower_E(z)=-eta J_E+nu W
      <-eta-nu(1-t+.4d),                           (27)

using J_E=L+a>a from (4) and W<=t-.4d-a.
In this sign beta=-phi with 0<phi<p<q. Therefore

    nu=cos(q-phi)>=cos q=d>15/17,
    1-t+.4d>15/17.

Together with (19), (27) gives

    lower_E(z)<-[7/25+(15/17)^2]
       =-1-423/7225<-1<D_B=upper_B(z).             (28)

This source also fails. The list(18) is exhausted, contradicting the
actual B--E separation. Theorem1 is proved. In particular, the proof
does not depend on whether the opposite central owner is ordinary or
inward, or on whether any wall origin is owned. ∎

## 7. Literal no-omission MPPM conclusion

**Corollary 2.** In the original no-omission MPPM family, suppose Q4 owns
F4,G3 and excludes G0. If Q4 has nonpositive canonical angle, it strictly
owns the common point O=(2,2).

**Proof.** Suppose O excluded and translate all coordinates by(-2,-2).
Take the actual owners

    C=Q4, E=Q5, B=Q9.

The complete local source ledger is as follows.

| Local datum | Original point and actual source |
|---|---|
| C marker,I,J | SW marker,F4=(2,1.74),G3=(1.74,2), strictly in Q4 |
| C X | (1.5,2), strict in Q4 by NO-OMISSION-REDUCTION equation(3a) |
| C T | (1.99,1.46), strict in Q4 by C1084 Corollary3 under the clockwise quarter-turn |
| Excluded G | G0=(1,1.6), the explicit omission in this corollary |
| Excluded O | The contrary missing-center assumption |
| B S | Original bottom marker(2,.914), strict in Q9 |
| B A_B | G2=(1.74,1), strict in actual no-omission Q9 |
| B F_B | (1.44,1), the actual Q9 reach in NO-OMISSION-REDUCTION Section1 |
| E marker,B0,B1 | SE marker,G5=(2.26,1),F6=(2.4,1), all strict in Q5 |
| E Y | (2.5,1), strict in Q5 by ORDINARY-MARKER-HALFPOINT |
| Excluded G_E | G8=(3,1.6), strict in Q10 |
| Excluded K0 | (3,1), strict in actual paired corner Q1 |
| Excluded O_R | (3,2), strict in Q10 by the actual paired-corner transfer |

The inward-neighbor conclusion F6,G5 in Q5 is equation(3) of
C1092-MPPM-NO-OMISSION-REDUCTION.md. In the C1084 tip application, its two
neighboring-marker exclusions are the original NW and SE markers, and
its third exclusion is exactly the omitted G0. The Q5 halfpoint theorem
uses the actual foreign F4 in Q4, the actual bottom marker in Q9, the
paired-corner inner point in Q1 and actual F8 in Q10. That halfpoint and
the same actual Q1 give the Q10 origin through Theorem7 of
C1092-DIRECT-WALL-POINT.md. These are exactly the checked source maps in
the reviewed small-successor chapter; no new ownership is inferred here.

The actual Q9 wall reach uses its marker and F2, with the two excluded
points G5 in Q5 and F4 in Q4, as proved in the no-omission reduction.
The genuine bottom wall becomes y>=-2, and the original MPPM sign X9<=2
becomes X_B<=0. Thus every hypothesis of Theorem1 holds for the named
three actual owners, a contradiction. ∎

Simultaneous quarter-turns give the same conclusion in each central
sector. This removes the entire nonpositive, missing-center inward branch
in which the corresponding outer G auxiliary is omitted, including its
previously surviving OIOI continuation. The genuinely different
outer-G-owned and positive-inward cases are not inferred from this
corollary; their stated ownership and face premises must be retained.
