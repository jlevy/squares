# C1092 MPPM: a missing-forward negative square strictly orders its actual walls

Every terminating decimal is an exact rational. Owned points are strict
interior points; an excluded point may lie on a face. The common side is
a>1. All coordinates in the local theorems are translated by (-2,-2)
from the original southwest sector. No upper side bound is needed here.

The conclusion of this chapter does not assume that the preceding
ordinary square omits its forward point. In particular, it does not
assume a preceding wall origin and does not assign a missing auxiliary
to another square.

## 1. A negative missing-forward profile without a preceding origin

**Lemma 1.** Let C have canonical frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,

lower faces U,V and upper faces J=U+a,K=V+a. Suppose C strictly owns

    M=(-.35,-.35), P=(-1,-.26), G0=(-1,-.4), H=(-1,-.5),

and excludes

    C0=(-1,-1), W=(-1.086,0), T=(-.26,0),
    the whole segment S=[-.56,-.26] x {-1}.

Then s>0, and

    U>=-1.086c, J<=s-.56c, K<=-.26s,
    q=s/(1+c)>237/763.                              (1)

**Proof.** At C0 the lower-u band follows from H, and its upper u- and
v-bands follow from M and G0. The nonnegative projection increments
are respectively .5s,.65(c-s),.6c. Hence C0 is lower v and

    V>=-c-s.                                       (2)

At W the upper-u band follows from P, and the lower-v band follows
from G0: their increments are .086c+.26s and .4c-.086s>0. Thus W is
lower u or upper v. The latter alternative, K<=-1.086s, would give
from (2) the impossible width a<=c-.086s<=1. Therefore U>=-1.086c.

Both lower bands of T follow strictly from P. An upper-u exit would
give a<=.826c<1. Thus T is upper v and K<=-.26s.

Write A=(-.26,-1), F=(-.56,-1). The lower-u and upper-v bands of A
follow from P. If A were lower v, its face together with the cap at T
would give a<=c. Therefore J<=-.26c+s. In particular
1<a<=.826c+s, so s>0.

Both the lower-u and upper-v bands are strict throughout S, by P.
Suppose J>u(F). Then F must be lower v, while A has its lower-v band
strict. On the line y=-1 the two remaining strict bands are

    x<(J-s)/c, x>(V+c)/s.

The first threshold is in (-.56,-.26], the second in [-.56,-.26).
As the whole actual segment S is excluded, the second threshold must
be at least the first, including possible equality. This gives

    cV-sJ>=-1.                                     (3)

But J>=a-1.086c and V<=-.26s-a yield

    cV-sJ<=.826cs-a(c+s)<.826cs-(c+s)<-1.           (4)

For the last inequality, use cs>0 and

    c+s-1=2cs/(1+c+s)>=2cs/(1+sqrt(2))>.826cs.

The final rational comparison follows by squaring the positive sides
of sqrt(2)<587/413. Equations (3)-(4) contradict each other, so
J<=u(F)=s-.56c.

Finally 1<a<=.526c+s, and

    .526c+s-1=(1-q)(763q-237)/(500(1+q^2)).          (5)

Since 0<=q<=sqrt(2)-1<1, this is positive exactly when q>237/763.
This proves (1), including the exclusion of the axial representative.
All diagonal projection equalities above retain a strict band from the
owned anchor. ∎

Put theta0=2 arctan(237/763). Its exact cosine and sine are

    c0=263000/319169, s0=180831/319169.

Monotonicity on theta0<theta<=pi/4 supplies

    .7<c<.825, .566<s<.71, s^2>.32, cs>.46,
    c^2-s^2<.36.                                   (6)

We also retain c+s-1>.826cs from the proof above.

## 2. A wall that misses its own origin must move upward

**Lemma 2.** Let L be any square of side a>1, with closure contained in
x>=-2. Suppose L strictly owns W=(-1.086,0) and A0=(-1,.26). If it
excludes D=(-1,0), then its center ordinate satisfies

    yL>7/20=.35.                                   (7)

**Proof.** First use the nonnegative frame (d,t),(-t,d), with d>=t>=0.
At D its lower-u, upper-u and upper-v bands follow respectively from
W,A0,W. Hence only its lower-v face can exclude D. Denoting its center
by (xL,yL), this gives

    -t xL+d yL>=t+a/2.

Its real left wall gives xL>=-2+a(d+t)/2. Consequently

    2d(yL-.35)>=a(1+t^2+dt)-2t-.7d
                 >1+t^2+dt-2t-.7d.               (8)

Write z=t/(1+d), so 0<=z<=sqrt(2)-1<5/12. Multiplication of the last
expression by the positive denominator (1+z^2)^2 gives

    (17/10)z^4-6z^3+6z^2-2z+3/10
      >=(7/2)z^2-2z+3/10
       =(7/2)(z-2/7)^2+1/70>0.                   (9)

Here 6(1-z)>7/2 was used on the nonnegative z^2 term. This proves (7)
for the nonnegative frame, including t=0.

In the negative frame (d,-t),(t,d), D has its lower-u, lower-v and
upper-v bands strict by W,W,A0. Thus D must be upper u and

    d xL-t yL<=-d-a/2.

If t=0, comparison with the real left wall immediately gives a<=1,
an impossibility. For t>0 the same wall implies

    2t(yL-.35)>=a(1+d^2+dt)-2d-.7t
                 >1+d^2+dt-2d-.7t.               (10)

Its numerator after multiplication by (1+z^2)^2 is

    z[4z^3-(17/5)z^2+3/5]>0,                     (11)

because z>0, z<5/12 and

    3/5-(17/5)(5/12)^2=7/720>0.

Both complete canonical signs have been covered, with the actual
container wall and weak face exits retained. ∎

## 3. The actual bottom square lies to the right of x=-.35

**Theorem 3.** Suppose C has the strict points M,P,H and the face and
angle bounds (1). Let the actual square B be disjoint from C, have the
same side a>1, strictly own

    D_B=(0,-1), F_B=(-.56,-1),

and have closure in y>=-2. Then

    xB>-.35.                                       (12)

**Proof.** Suppose xB<=-.35. A separating normal directed from B to C
satisfies, using strict pairs H,D_B and M,F_B,

    -nx+.5ny>0, .21nx+.65ny>0.

Thus ny>0 and nx<.5ny. The only signed face normal of C in this cone
is -u=(-c,s): the other upward normal v has s/c>.5 by (6). The actual
face normals of B in the cone are either northwest or northeast. In
the northeast case n=(h,t), h,t>=0, h^2+t^2=1 and h/t<.5. This is the
complete list of possible actual-square separating-axis sources.

### 3.1. Northeast normals of B

Set lambda=ch-st<0 and mu=sh+ct>0. The actual faces imply

    lower_C(n)=lambda J+mu V
      <=lambda(a-1.086c)+mu(-.26s-a).

Subtract n.F_B=-.56h-t. Since lambda-mu<0 and a>1, the result is
strictly less than

    h[c-s-.526+.826s^2]+t[1+.826cs-c-s].            (13)

The second bracket is negative by c+s-1>.826cs. For the first, (5)
gives s>1-.526c. Thus it is strictly less than

    s^2[.826-1.526/(1+c)]<0,

where c<.825 and .826(1+.825)=1.50745<1.526. Therefore
lower_C(n)<n.F_B<upper_B(n), excluding every northeast source.

### 3.2. C's own normal -u

Let k be B's unit-side vertical width and w its unit-side width in
-u. The elementary square-width inequality proved in Section 2 of
C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md gives

    s k+w>=1+s(c+s).

The actual bottom wall and supposed x-coordinate give

    upper_B(-u)>=.35c-2s+(a/2)(s k+w).

Also lower_C(-u)=-J<=1.086c-a. Hence their support difference is
strictly greater than

    Fb(theta)=1.5-.736c-2s+.5s(c+s).               (14)

Its derivative is

    Fb'=.736s-2c+cs+.5(c^2-s^2)<-.19744

by (6) and cs<=.5. It decreases throughout the entire closed angle
range, so

    Fb(theta)>=Fb(pi/4)=2-(171/125)sqrt(2)>0.       (15)

The last comparison follows from 2(171)^2<250^2. Thus -u cannot
separate.

### 3.3. Northwest normals of B

Write n=(-h,t)=(-cos(phi),sin(phi)), 0<=phi<=pi/2, and set

    kappa=ch+st>0, sigma=ct-sh=sin(phi-theta).

Because n is an actual face normal of B, its vertical unit-side width
is h+t and its width in n is 1. Its actual wall therefore gives

    upper_B(n)>=.35h-2t+(a/2)(1+t^2+ht).            (16)

When phi>=theta, sigma>=0. From J>=a-1.086c and V<=-.26s-a,

    lower_C(n)=-kappa J+sigma V
      <=-kappa(a-1.086c)+sigma(-.26s-a).

Subtract from (16) and lower a to 1 in its positive coefficient. The
support difference is strictly greater than

    F(phi)=.5+.5t^2+.5ht+A h+B0 t,
    A=c-s-.736+.826s^2,
    B0=c+s-2-.826cs.                               (17)

The theta-derivative of A is -(c+s)+1.652cs<0. Hence
A>=A(pi/4)=-.323. Also B0>-1. Consequently

    F(phi)>.5(1-t)^2+h(.5t-.323).                  (18)

Here t>=s>.566. If t>=.646, the right side is nonnegative. If
.566<t<.646, it is greater than

    .5(.354)^2-.04=.022658>0.

At the endpoint t=1,h=0 the strict B0>-1 in (18) still supplies
F>0. Thus every source with phi>=theta fails.

When phi<=theta, sigma<=0. The strict marker M gives
K>-.35(c+s). Thus

    lower_C(n)=-kappa J+sigma K
      <=-kappa(a-1.086c)-.35(c+s)sigma.

The support difference is strictly greater than the expression F in
(17), now with

    A=c-.736+.736s^2-.35cs,
    B0=-2+s+.35c^2-.736cs.                         (19)

The bounds (6) give

    A>.7-.736+.736(.32)-.175=.02452>0.

For B0, the function s-.35s^2 increases on 0<=s<=.71, so

    B0=-1.65+(s-.35s^2)-.736cs
       <-1.65+[.71-.35(.71)^2]-.736(.46)
        =-1.454995<-7/5.

Therefore

    F'=ht+.5(h^2-t^2)-At+B0 h
       <h(t+h/2-7/5)<0,

using t+h/2<=sqrt(5)/2<7/5. Its minimum on 0<=phi<=theta is at
phi=theta. Direct substitution in (19) gives

    F(theta)=Fb(theta)>0.

Every actual normal source, both relative-angle orders and all normal
endpoints have now been excluded. The supposed xB<=-.35 is impossible,
proving (12). ∎

## 4. The strict local order, without a preceding-origin assumption

**Theorem 4.** Suppose C satisfies all hypotheses of Lemma 1. Let B,L
be two actual squares of side a>1, with interiors disjoint from C and
from each other. In addition to Theorem 3's hypotheses, let B strictly
own (0,-1.086),(-.4,-1). Let L strictly own W=(-1.086,0),A0=(-1,.26)
and have its closure in x>=-2. Then

    xB+yL>0.                                       (20)

**Proof.** The physical point D=(-1,0) is either strict in C or is not.
If it is strict in C, it is excluded from L. Lemma 2 gives yL>.35,
while Theorem 3 gives xB>-.35. Their sum is strictly positive.

If D is excluded from C, the complete Lemma 1 of
C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md applies to C: it retains the
same actual bar and gains U>=-c and q>7/18. Its Theorem 2 applies to
the same actual B, giving xB>-.2.

It remains to prove yL>.2 in this second case. If yL<=.2, Lemma 2
implies that D must be strict in L. Theorem 3 of that earlier chapter
then applies literally to this C and L and gives yL>.2, a contradiction.
Thus yL>.2, which again proves (20). This exhaustive dichotomy never
assigns D an owner when it is missing. ∎

## 5. Literal original OOOO application

Retain the original no-omission MPPM entrance and the all-four-ordinary
case of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md. Suppose Q4 omits its
forward G3 and has nonpositive canonical angle. In the local chart:

| Local datum | Literal source |
|---|---|
| M,P,G0 in C=Q4 | SW marker,F0,G0, the actual ordinary pair |
| H in C | (1,1.5), the proved missing-forward ordinary halfpoint |
| C0 excluded | Actual Q0 owns its inner corner (1,1) |
| W excluded from C, strict in L=Q8 | Actual left marker (.914,2) |
| T excluded | The stated G3 omission by Q4 |
| Whole S excluded from C | Actual Q9 owns its advanced (1.44,1) and G2=(1.74,1) |
| D_B,F_B in B=Q9 | Actual bottom origin (2,1), supplied by Q4's missing-forward transfer, and the same advanced point |
| Additional strict B anchors | Actual bottom marker (2,.914) and F2=(1.6,1) |
| A0 in L=Q8 | Actual F1=(1,2.26) from the no-omission wall pair |
| Real B,L walls | Original y>=0 and x>=0, translated to -2 |

The bottom advance is supplied by ordinary Q5's G5, using Section 5 of
C1092-MPPM-NONORDINARY-ISOLATION.md. All segments have one actual owner.
Theorem 4 therefore proves

    center(Q9)_x+center(Q8)_y>4.                    (21)

No assumption about Q7's forward F5 was made. All simultaneous
quarter-turns of this local order are valid with the actual owner cycles
(Q4,Q5,Q6,Q7) and (Q8,Q9,Q10,Q11). The zero angle has already been
excluded by Lemma 1, and the diagonal endpoint was retained throughout.

This chapter proves the stated strict wall-center order for every
nonpositive missing-forward ordinary square in OOOO. It does not by
itself assert an order for an ordinary square that owns its forward
point or for the positive missing-forward regime, and does not claim
completion of the remaining partial-forward cycles.
