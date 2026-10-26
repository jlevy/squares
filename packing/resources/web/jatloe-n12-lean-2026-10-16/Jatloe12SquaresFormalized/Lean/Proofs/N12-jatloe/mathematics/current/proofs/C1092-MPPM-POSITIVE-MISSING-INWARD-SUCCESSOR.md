# C1092 MPPM: a positive missing-center inward square has a negative successor

Every terminating decimal is an exact rational. All owners below are actual
open squares of a common side a>1. Owned points are strict, and excluded
points and separating supports permit equality. The local theorem uses no
container, center sign, side upper bound or angle catalogue.

## 1. The actual-pair theorem and the inward face profile

**Theorem 1.** Let C and E be disjoint open squares of the same side a>1.
Suppose C has a nonnegative canonical frame

    u=(c,s), v=(-s,c), c>=s>=0, c^2+s^2=1,

strictly owns

    M_C=(-.35,-.35), I=(0,-.26), J=(-.26,0),
    X=(-.5,0), T=(-.01,-.54),

and excludes

    O=(0,0), G0=(-1,-.4), F2=(-.4,-1), N=(-.35,.35).

Suppose E strictly owns

    M=(.35,-.35), B0=(.26,-1), B=(.4,-1), Y_E=(.5,-1),

and excludes

    G=(1,-.4), K0=(1,-1), R0=(0,-1.086).

Then E has no nonnegative canonical representative. Consequently its
canonical angle is strictly negative, with the diagonal representative
also excluded by the proof below.

Write U,V for the lower C faces and A=U+a,H=V+a for its upper faces.
If s=0, the strict points I,J already put O in both open bands. Thus
s>0. At O its lower u-band follows from M_C and its two v-bands from I,J.
Therefore O must be upper u and

    A<=0, U<=-a.                                      (1)

The point

    Y=(0,-.5)

is strict in C. Its lower u and v bands follow from T, with respective
increments .01c+.04s and .04c-.01s>=.03c. Its upper bands follow from I,
with increments .24s and .24c. These comparisons preserve strictness
at every endpoint.

At F2 both upper bands follow from M_C. A lower-u exit, together with
(1), would give a<=.4c+s<=1.4/sqrt(2)<1. Thus F2 is lower v. At G0
its upper u-band follows from M_C, and its lower v-band follows from T.
An upper-v exit would then give a<=.6(c+s)<1. Consequently G0 is lower u.
At N its lower u-band follows from X and its lower v-band from M_C; an
upper-u exit would oppose G0 at width .65c+.75s<=sqrt(.985)<1. Therefore
N is upper v. The complete simultaneous profile is

    U>=-c-.4s,       A>=a-c-.4s, A<=0,
    V>=.4s-c,        H<=.35(c+s),
    I,X,Y strictly in C.                              (2)

In particular all of I,X,Y are excluded from the different actual E.
No point on the physical line x=0 is declared strict merely because O
is excluded: the two halfpoints used here have their own strict proofs.

## 2. A putative nonnegative successor has four forced faces

Suppose E has the nonnegative frame

    u_E=(d,t), v_E=(-t,d), d>=t>=0, d^2+t^2=1.

Use L,W for its lower faces and J_E=L+a,K_E=W+a for its upper faces.
We prove

    J_E<=d-.4t,       W>=-d-t,
    K_E<=-.5d,        L>=-1.086t.                    (3)

At G, the lower u-band follows from M, the lower v-band from B, and the
upper v-band from M. The corresponding projection increments are
.65d-.05t>=.60d, .6(d-t)>=0, and .65t+.05d>0. Thus G is upper u.

At I its upper u-band follows from M and its lower v-band from B. A
lower-u exit would combine with the cap at G to give a<=d-.14t<=1.
Hence I is upper v and initially K_E<=-.26d.

At K0 its lower u-band follows from B and its upper v-band from M. If
it were upper u, J_E<=d-t. The point R0 has both upper bands from B0
and M. Its lower-v alternative would give a<=.826d<1, so R0 would be
lower u and L>=-1.086t. These u-faces would imply

    1<a<=d+.086t.

The case t=0 is immediately impossible; otherwise the half-angle
t/(1+d) would be less than .086, so t<.172 and d>7/10. Now Y would
be strictly inside E: its upper u-band follows from M; its upper
v-band from M because .15d-.35t>.105-.0602>0; its lower u-band follows
from L<=d-t-a<-t; and its lower v-band follows from
W<=-.26d-a. This contradicts strict Y ownership in C. Thus K0 is
lower v, giving W>=-d-t.

At Y its upper u-band follows from M and its lower v-band from B0.
A lower-u exit would give L>=-.5t and hence a<=d+.1t, forcing t<.2.
But the existing v-faces would give a<=t+.74d<.94<1. Therefore Y is
upper v, proving K_E<=-.5d.

Finally R0 has both upper bands as before; its lower-v alternative
would now give a<=.586d<1. Hence L>=-1.086t. This completes (3).
All rejected exits were weak and every band comparison used a strict
anchor.

The opposite v-faces in (3) yield

    1<a<=t+.5d.                                       (4)

Writing q=arctan(t/d), the function sin q+.5cos q increases strictly
on [0,pi/4], and equals 1 at q0=2 arctan(1/3), where (d,t)=(4/5,3/5).
Thus

    q>q0, t>3/5, d<4/5, t/d>3/4.                    (5)

We shall also use the lower cap consequence

    K_E=W+a>=a-d-t,                                (6)

which follows from the actual excluded corner K0. This is a bound on
the same full square E, in addition to its strict marker bounds.

## 3. The complete actual normal list

Let p=arctan(s/c). Orient a separating normal from C toward E. The
strict markers imply n_x>0. The strict points I in C and Y_E in E give

    .5n_x-.74n_y>0,
    n_y<(25/37)n_x.                                  (7)

E's upright face normal u_E is impossible by (5). C's upright normal
u can only be eligible when s/c<25/37<3/4<t/d, hence only when q>p.
The complete remaining actual face-normal list is therefore

    u (only if q>p), -v, -v_E.                       (8)

No other square or polygon normal is introduced. Put

    kappa=cd+st=cos(q-p)>0,
    sigma=ct-sd=sin(q-p).

Every replacement of a by 1 below is strict with a positive coefficient.
Consequently positive or nonnegative displayed lower margins exclude
weak tangential separation as well.

## 4. C's upright normal

For this source q>p, so sigma>0. The exact lower support of E is
kappa L-sigma K_E. Use J_E<=d-.4t, the strict marker bound
K_E>-.35(d+t), and A>=a-c-.4s. The support difference is strictly
greater than

    F_u=1-c-.4s+kappa(1-d+.4t)-.35sigma(d+t)
        =1-c A_u+s B_u,                              (9)
    A_u=2-d-.65t^2-.05dt,
    B_u=t-.65dt-.05d^2.

Here A_u>0, since A_u>=2-1-.325-.025=.65. Also

    1-A_u=t^2[.65-1/(1+d)]+.05dt>0,

using d>7/10 and .65>10/17. Finally (5) gives
B_u>=.35t-.05>.16>0. Thus F_u>=1-A_u>0, because c<=1 and s>=0.
This source cannot separate.

## 5. C's downward normal

The upper C support on -v is a-H. If q>=p, the lower E support is
sigma L-kappa K_E. Using the same two E bounds as in Section 4 gives
the strict lower margin

    1-H+sigma(1-d+.4t)-.35kappa(d+t)
       >=1-.35(c+s)-.35kappa(d+t)
       >=1-.7sqrt(2)>0.                             (10)

If q<=p, put eta=-sigma>=0. The lower E support is instead
-eta J_E-kappa K_E. Its strict marker gives J_E>.35(d-t)>=0 and
K_E>-.35(d+t). The support difference is therefore strictly greater
than the same last positive bound in (10). Equality q=p is included.

## 6. E's downward normal when q>=p

The exact upper support of C on -v_E is sigma A-kappa V. Use (2),
and use (6) to bound E's lower support -K_E by d+t-a. The resulting
strict lower margin is

    F=1-d-t+kappa[1-.35(c+s)]+sigma[1-c-.4s]
     =1-d A_0-t B_0,                                 (11)
    A_0=1.35-c+s-.75s^2-.65cs,
    B_0=2-c-s-.65s^2+.75cs.

These two coefficients satisfy the following uniform canonical bounds:

    0<A_0<=.65, B_0>0, A_0+B_0<=1.4.                (12)

For the upper bound on A_0, put h=c+s<=sqrt(2). Since cs>=s^2,

    c-s+.75s^2+.65cs
       >=(1-2s^2)/sqrt(2)+1.4s^2
       =1/sqrt(2)+(1.4-sqrt(2))s^2>=.7.

Subtracting from 1.35 proves A_0<=.65. For positivity, use s^2<=cs,
c<=1 and s<5/7 to obtain

    A_0>=1.35-c+s-1.4cs>=.35-.4s>9/140>0.

Also B_0>=2-c-s+.1s^2>=2-sqrt(2)>0. Finally

    A_0+B_0=1.35+2(1-c)-1.4s^2+.1cs
             <=1.35-.2s^2+.1cs<=1.4,

where 2(1-c)=2s^2/(1+c)<=1.2s^2 and cs<=1/2.

If A_0>B_0, then d A_0+t B_0<=(d+t)A_0<=.65sqrt(2)<1.
If A_0<=B_0, the function A_0 cos q+B_0 sin q is nondecreasing on
the whole canonical interval: its derivative B_0 cos q-A_0 sin q is
nonnegative because d>=t>=0. Its maximum is therefore
(A_0+B_0)/sqrt(2)<=1.4/sqrt(2)<1. In both alternatives F>0. This
argument holds on the entire angle domain, without a polynomial table
or angle subdivision.

## 7. E's downward normal when q<=p

Put eta=-sigma>=0. Now the exact upper C support is
-eta U-kappa V. Use U<=-a and V<=.35(c+s)-a, together with (6).
The support difference is strictly greater than

    1+eta+kappa-d-t-.35kappa(c+s)
       >=1-d-t+kappa[1-.35(c+s)].                    (13)

Since 0<=q<=p<=pi/4,

    kappa>=cos(pi/4-q)=(d+t)/sqrt(2).

The bracket in (13) is positive and is at least 1-.35sqrt(2).
Consequently (13) is at least

    1-(d+t)(1.35-1/sqrt(2))
       >=2-1.35sqrt(2)>0.                            (14)

This includes q=p and every canonical endpoint. Every source in (8)
is impossible, contradicting disjointness. Theorem 1 follows.

## 8. Literal original no-omission MPPM application

Normalize the inward owner as Q4 and translate by (-2,-2). Suppose Q4
omits G0 and the physical center (2,2), and has positive canonical
angle. The strict M_C,I,J are its marker,F4,G3. The strict X=(1.5,2)
is proved in C1092-MPPM-NO-OMISSION-REDUCTION.md, Section 1. The strict
tip T=(1.99,1.46) is C1084-DUPLICATE-POINT.md, Corollary 3, under
R^3(x,y)=(y,4-x): its two foreign markers are the actual NW and SE
markers, and its third exclusion is precisely the genuine G0 omission.

The excluded local F2 and N are respectively actual F2 in Q9 and the
actual NW marker in Q7. No ownership of F0 is assumed or discarded.

The ordinary successor is the one actual Q5, whose F6,G5 ownership is
already proved by the inward covering reduction. Its strict M,B0,B
are its marker,G5,F6. ORDINARY-MARKER-HALFPOINT.md gives its strict
Y_E=(2.5,1) under (xi,eta)->(2-eta,2-xi), with d=.086 in that theorem.
The four exclusions required there are F4 in Q4, the bottom marker in
Q9, the inner SE corner in Q1, and F8 in actual Q10. The three excluded
points G,K0,R0 in the present theorem are G8 in Q10, the same actual
Q1 inner point, and the Q9 marker. The C points I,Y are automatically
excluded from Q5 by strict ownership in the different actual Q4.

Thus every hypothesis is literal and Theorem 1 proves that Q5 must
have strictly negative canonical angle. Quarter-turns give the same
result in the other sectors. This is a successor-sign reduction, not
an assertion that the whole missing-center inward branch is closed.
