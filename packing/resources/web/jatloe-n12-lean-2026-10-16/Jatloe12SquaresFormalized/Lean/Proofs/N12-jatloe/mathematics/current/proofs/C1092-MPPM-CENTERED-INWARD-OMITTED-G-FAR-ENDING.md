# C1092 MPPM: a centered inward owner omitting G0 cannot have an ordinary opposite

Every terminating decimal is an exact rational. All named squares are the
actual open squares, with common side a>1 and pairwise disjoint interiors.
Owned points are strict. An excluded point, a wall contact, or a separating
support may meet with equality. No numerical orientation sample or upper
side bound is used.

**Theorem 1.** In the original no-omission MPPM entrance, suppose the
nonordinary inward Q4 strictly owns O=(2,2), has negative canonical angle,
and omits G0. Then F9 is omitted from the actual opposite Q6. In particular
Q6 cannot be ordinary.

The proof does not assume or conclude a bottom origin for this branch. The
stronger lower u-face supplied by the actual G0 omission replaces that
premise. Section 1 first proves the required far-bar fact for an actual
negative ordinary successor without a bottom-origin hypothesis.

## 1. A whole far bar caps the successor without a bottom origin

Work in centered coordinates and use the negative frame

    u_E=(d,-t), v_E=(t,d), d>=t>0, d^2+t^2=1.

Write L,K for E's lower faces and J=L+a,D=K+a for its upper faces.
Retain the actual negative-successor profile proved in
C1092-MPPM-NEGATIVE-SUCCESSOR-BAR-PROFILE.md:

    L>=.26t, J<=d+t,
    K>=-1.086d, D<=t-.4d.                         (1)

Its strict marker is M=(.35,-.35). Suppose additionally that the whole
segment

    T={1} x [-.56,0]                               (2)

is disjoint from E. Its application below places T strictly inside the
one actual right square. We prove

    D<=t-.56d,
    1<a<=t+.526d,
    z_E:=t/(1+d)>237/763.                           (3)

Let F=(1,-.56). Its two lower bands are strict from E's actual strict
marker M and actual strict anchor B0=(.26,-1), with increments
.65d+.21t and .74t+.44d. Thus F is upper u or upper v.

Suppose it is upper u. Then J<=d+.56t, which with (1) gives

    1<a<=d+.30t, 0<z_E<3/10,                      (4)

because d+.30t-1=2z_E(.30-z_E)/(1+z_E^2).

The rightmost closure vertex Z=J u_E+D v_E has coordinates

    Z_x=dJ+tD, Z_y=-tJ+dD.

The lower bound J>=a+.26t and the weaker upper bound D<=t from (1)
give

    Z_y<=t(d-a)-.26t^2<0.                          (5)

The supposed upper-u face at F and the actual lower face K in (1)
give the other bound

    Z_y>=ad-1.086d^2-dt-.56t^2
         >-.56+d(1-t-.526d).                      (6)

The function sin q+.526cos q is increasing on the full canonical
interval, since its derivative is at least .474cos q>0. At
q=2 arctan(3/10) its exact value is

    60/109+.526(91/109)=53933/54500<1.

Thus (4)-(6) prove -.56<Z_y<0 throughout the alleged alternative.
The same actual lower faces give

    Z_x>=a(d+t)-.826dt>d+t-.826dt>1.               (7)

For the last strict sign use dt>0 and

    d+t-1=2dt/(1+d+t)
          >=2dt/(1+sqrt(2))>.826dt.

The rational comparison follows from sqrt(2)<587/413; the squared
margin is 3431/170569>0.

Join the strict marker M to the closure vertex Z. Every point of this
segment except possibly Z is strict in E. By (7), its crossing of x=1
occurs strictly before Z. By (5)-(6) and the marker height -.35, the
crossing has height strictly between -.56 and 0. This is a strict point
of E on T, contradicting (2). No closure vertex was asserted to be an
owned point, and the argument includes all possible tangent faces at F.

Therefore F is upper v and D<=t-.56d. Combining this with the actual
lower bound K>=-1.086d gives a<=t+.526d. The exact identity

    t+.526d-1
      =(1-z_E)(763z_E-237)/[500(1+z_E^2)]          (8)

then gives (3), since 0<z_E<=sqrt(2)-1<1 and a>1. This establishes
the entire far-bar profile without a bottom origin.

## 2. The local two-square statement and all actual normal sources

Let C have frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,
    0<=x:=s/(1+c)<=21/100.

Write U,V and A=U+a,H=V+a for its lower and upper faces. Suppose

    A>=a-c+.4s, H<=eta:=17/125,                    (9)

and C strictly owns M_C=(-.35,-.35) and X=(-.5,0).
Let E have the actual profile and strict points used in Section 1,
including Y_E=(.5,-1). We show that C,E cannot be disjoint if (2)
holds. These are local square assumptions; neither center membership
nor an owner for an omitted point is needed inside this local proof.

Orient a separating normal from C toward E. Their strict markers force
n_x>0. Their strict pair X,Y_E forces n_x>n_y. Both transverse upward
normals (s,c),(t,d) fail this second inequality; the opposite transverse
normals and both negative longitudinal normals fail the first. The
separating-axis theorem therefore leaves exactly the two actual sources

    u=(c,-s), u_E=(d,-t).                           (10)

The zero and diagonal representatives are included in these comparisons.
Put p=arctan(s/c),q=arctan(t/d). From (3),(9),

    q>q0:=2 arctan(237/763)>p,
    k=cd+st=cos(q-p)>0,
    delta=ct-sd=sin(q-p)>0,
    alpha=1-c+.4s.                                 (11)

In direction u the exact lower E support is kL+delta K. Using
J<=d+t, D<=t-.56d and (9), the support difference is strictly greater
than

    F_C=alpha+k(1-d-t)+delta(1-t+.56d).             (12)

In direction u_E the exact upper C support is kA-delta V. Using
V=H-a<=eta-a and L<=d+t-a, its difference from the lower E support
is strictly greater than

    F_E=1-d-t+k alpha+delta(1-eta).                 (13)

In both calculations, the coefficient of a before replacing it by 1 is
1+k+delta>0. Thus a>1 makes the comparison strict even if every stated
face and candidate separation is an equality.

## 3. The C source fails on the entire successor interval

The exact expansion of (12) is

    F_C=1-c P(q)-s Q(q),
    P(q)=2-d-t+.44dt,
    Q(q)=d-t+.16+.44t^2.                            (14)

Both coefficient functions are nonincreasing on 0<=q<=pi/4:

    P'(q)=-(d-t)[1-.44(d+t)]<=0,
    Q'(q)=-(d+t)+.88dt<0.                          (15)

Here d+t<=sqrt(2)<3/2 and dt<=1/2 justify every sign. At q=q0,

    d0=263000/319169, t0=180831/319169,

    P(q0)=83006368003/101868850561<.82,
    Q(q0)=284563739488/509344252805<.56.            (16)

For reference, the exact positive differences from .82 and .56 are
26304472851/5093442528050 and 3345210414/2546721264025, respectively.
Equations (11),(14)-(16) and Cauchy's inequality give

    F_C>1-.82c-.56s
         >=1-sqrt(.82^2+.56^2)
          =1-sqrt(.986)>0.                         (17)

This excludes C's source on the whole interval q0<q<=pi/4.

## 4. The E source has a positive continuous margin

Rewrite (13) exactly as

    F_E=1-A_p d-B_p t,
    A_p=1+(1-eta)s-c alpha,
    B_p=1-(1-eta)c-s alpha.                        (18)

On the entire closed interval 0<=x<=21/100,

    c>=9559/10441>.91,
    0<=s<=4200/10441<.41,
    0<=alpha<.09+.4(.41)=.254<.26.

Consequently A_p>.74 and B_p<1-.864(.91)<.22. Also q>=q0 implies
t/d>=180831/263000>.68. Differentiating (18) therefore gives

    partial F_E/partial q=A_p t-B_p d
       >[.74(.68)-.22]d=.2832d>0.                 (19)

It suffices to check the whole C interval at q=q0. Direct rational
half-angle substitution gives

    F_E(q0)=N(x)/[39896125(1+x^2)^2],              (20)

    N(x)=-100862498x^4+7307500x^3+70750700x^2
                        -30508000x+3946998.

This polynomial decreases throughout 0<=x<=21/100. To verify that
claim without sampling, its derivatives are

    N'(x)=-403449992x^3+21922500x^2
                            +141501400x-30508000,
    N''(x)=-1210349976x^2+43845000x+141501400.

On the full interval,

    N''(x)>=141501400-1210349976(21/100)^2
             =110156207573/1250>0,

while

    N'(21/100)=-445284265739/125000<0.

Thus N' is increasing to a negative endpoint, and N is decreasing.
Its exact endpoint value is

    N(21/100)=26597011638231/50000000>500000.        (21)

Moreover 1+x^2<21/20 and

    39896125(21/20)^2=703767645/16<50000000.

Equations (19)-(21) prove the uniform strict margin

    F_E>1/100>0.                                   (22)

This defeats the last actual source in (10). Sections 1-4 prove the
local two-square ending, with the full canonical endpoints and weak
support contacts retained.

## 5. Literal original source map and Theorem 1

Retain the original no-omission MPPM entrance and the hypotheses of
Theorem 1. Translate every actual square by (-2,-2) and set

    C=Q4, E=Q5, R=Q10.

The full centered negative inward angle and face results are
C1092-MPPM-CENTERED-NEGATIVE-INWARD-ANGLE.md, Theorem 1, and
C1092-MPPM-CENTERED-NEGATIVE-INWARD-H-CAP.md, Theorem 1. They give
x<21/100 and H<17/125. Since G0 is omitted, its forced lower-u face
from C1092-MPPM-NEGATIVE-INWARD-SUCCESSOR-SIGN.md, Section 6.1, is
U>=-c+.4s. Thus every face in (9) holds, with the stronger strict
versions where already proved. C's strict marker is original, and
X=(1.5,2) is the inward crosspoint in the no-omission reduction,
Section 1, equation (3a).

That same no-omission reduction gives the actual ordinary pair
F6,G5 in Q5. The negative-inward successor-sign theorem makes this
same E strictly negative. Its strict halfpoint (2.5,1) is the literal
ordinary-marker halfpoint application recorded in that theorem: its
strict anchors are the Q5 marker,G5,F6, and its exclusions are F4 in
Q4, the actual Q9 marker, the actual Q1 inner corner and F8 in Q10.
The paired-corner transfer, Theorem 7 of C1092-DIRECT-WALL-POINT.md,
then puts (3,2) strictly in the actual Q10, using the same actual Q1,
the original Q10 marker, G8 and the real right wall, with b=.914,
ell=1.6. This is the genuine right origin used in the profile (1).

The remaining profile sources are exactly those in
C1092-MPPM-NEGATIVE-SUCCESSOR-BAR-PROFILE.md: its strict E marker,
G5,F6 and halfpoint, its foreign F4 in Q4, its foreign right origin
and G8 in Q10, the actual Q1 inner corner and the actual Q9 marker.
Thus (1) is the profile of this E, independent of a bottom origin.

Suppose now that F9 belongs to the opposite Q6. Theorem 1 of
C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md excludes G6 from Q10 using
only this single actual F9 premise. The actual wall-reach map in
Section 5 of C1092-MPPM-NONORDINARY-ISOLATION.md then uses Q10's
strict original marker and G8, its two exclusions F9 and G6, and
the real right wall. It gives (3,1.44) strictly in Q10. The strict
segment joining this point to the already proved strict right origin
(3,2) is contained in the one actual R. It is exactly T in (2).

All local hypotheses are now supplied by the named actual owners.
The two-square ending contradicts disjointness, so F9 is omitted.
An ordinary Q6 would own F9,G9 and is consequently impossible.
This proves Theorem 1. Simultaneous quarter-turns give the same
conclusion in every central sector.

In particular this closes the centered negative, both-outer-omitted
branch whenever its opposite is ordinary. Its actual bottom origin
has not been asserted. If the opposite is inward, the required far
right bar has not been supplied by this chapter, and that case remains
subject to its own actual inward geometry.
