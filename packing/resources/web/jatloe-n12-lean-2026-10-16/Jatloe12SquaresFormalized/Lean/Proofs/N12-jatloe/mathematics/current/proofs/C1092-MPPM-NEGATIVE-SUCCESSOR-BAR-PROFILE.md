# C1092 MPPM: the actual right bar fixes the negative successor's outer face

Every terminating decimal is an exact rational. Owned points are strict,
excluded points may be tangent, and a is the common side with a>1. The
whole segment below belongs to one actual foreign square. No independently
chosen endpoint owners or numerical angle samples are used.

## 1. The local profile

**Theorem 1.** Let E be an actual open square of side a>1 with strictly
negative canonical frame

    u=(d,-t), v=(t,d), d>=t>0, d^2+t^2=1.

Write L,K for its lower faces and J=L+a,D=K+a for its upper faces.
Suppose E strictly owns

    M=(.35,-.35), B0=(.26,-1), B=(.4,-1),             (1)

excludes the points

    I=(0,-.26), O_R=(1,0), K0=(1,-1),
    R0=(0,-1.086),                                  (2)

and is disjoint from the whole segment

    T={1} x [-.4,0].                                 (3)

Then its simultaneous actual faces satisfy

    L>=.26t, J<=d+t,
    K>=-1.086d, D<=t-.4d.                          (4)

Consequently

    1<a<=t+.686d,
    t/(1+d)>157/843.                                (5)

The theorem does not require a strict physical center or a particular
orientation of the inward owner that supplies the excluded point I.

## 2. Three point exclusions give the preliminary faces

At I, the upper u-band follows from M and the lower v-band follows from
B. Thus I is lower u or upper v. Suppose first that it is upper v, so
D<=-.26d. At K0, its lower u-band follows from B and its upper v-band
from M. A lower-v exit there would give a<=.74d-t<1. Therefore K0 is
upper u and J<=d+t.

The point R0 has both upper bands from B0,M. Its lower-v alternative
would give a<=.826d<1, so R0 is lower u and L>=1.086t. This would
give a<=d-.086t<=1. Thus the assumed exit of I is impossible and

    L>=.26t.                                        (6)

At O_R, both lower bands follow from M,B. Its upper-u alternative
would oppose (6) and give a<=d-.26t<=1. Thus O_R is upper v and
D<=t. At K0 the same two strict bands used above still hold. A
lower-v exit would now give a<=d<=1, so K0 is upper u. Finally R0
has the same two upper bands; a lower-u exit would again give
a<=d-.086t<=1. It must be lower v. We have proved

    L>=.26t, J<=d+t, K>=-1.086d, D<=t.             (7)

All comparison increments that may vanish are compared with strict
anchors, so the corresponding bands remain strict at a diagonal
canonical endpoint as well.

## 3. The rightmost closure vertex excludes the wrong G8 face

Let G=(1,-.4), the lower endpoint of T. Its two lower bands follow
from M,B. Suppose G is upper u. Then J<=d+.4t. Along with (6),

    1<a<=d+.14t.                                    (8)

The usual exact half-angle identity gives

    z=t/(1+d)<.14, t<.28.                           (9)

Let Z=Ju+Dv be the rightmost closure vertex of the same actual E.
Its coordinates are

    Z_x=dJ+tD, Z_y=-tJ+dD.                         (10)

By (7), J>=a+.26t and D<=t, so

    Z_y<=-t(a+.26t)+dt
         =t(d-a)-.26t^2<0.                         (11)

For its lower bound, use J<=d+.4t and D>=a-1.086d from (7). Then

    Z_y>=-t(d+.4t)+d(a-1.086d)
         >d-1.086-dt+.686t^2
         >=-.086-t-.314t^2
         >-.3906176>-.4.                            (12)

Here d>=d^2=1-t^2 and dt<=t justify the second inequality. The last
exact endpoint is -.086-.28-.314(.28)^2=-.3906176, and (9) makes
the displayed estimate strict.

On the other hand, the two lower bounds on J,D give

    Z_x>=a(d+t)-.826dt>d+t-.826dt.                  (13)

Since d+t<1.28 by (9),

    d+t-1=2dt/(1+d+t)>(50/57)dt>.826dt.             (14)

Thus Z_x>1, while (11)-(12) put Z_y strictly between -.4 and 0.

The segment from the strict E marker M=(.35,-.35) to its closure
vertex Z has every point except possibly Z strictly inside E. Since
M_x<1<Z_x, it crosses x=1 at a point strictly before Z. The crossing
height lies strictly between -.4 and 0 because both endpoint heights
do. This produces a point of T strictly inside E, a contradiction
to (3). This argument uses the whole actual segment and treats the
closure vertex without assigning strict ownership to that vertex.

Therefore G cannot be upper u. Its two strict lower bands force it
to be upper v, giving D<=t-.4d. Together with (7), this is (4).
The transverse width gives the first inequality in (5). Writing
z=t/(1+d), its exact factorization is

    t+.686d-1
      =[-1.686z^2+2z-.314]/(1+z^2)
      =-1.686(z-157/843)(z-1)/(1+z^2).

The canonical interval has z<1, so strict positivity requires
z>157/843. This completes the theorem on the entire angle domain.

## 4. Literal no-omission inward application

Normalize a nonordinary inward owner to Q4. The no-omission reduction
forces the actual ordinary successor E=Q5 to own G5,F6, which are
B0,B after translation by (-2,-2). Its strict marker is M. The
excluded I is actual F4 in the inward Q4. The points K0,R0 are the
actual Q1 inner corner and the actual Q9 bottom marker.

The ordinary-marker halfpoint theorem gives (2.5,1) strictly in E,
using its ordinary pair and marker, and the foreign F4, bottom
marker, inner corner and actual Q10 F8. Apply the actual paired-corner
transfer, Theorem 7 of C1092-DIRECT-WALL-POINT.md, to Q1 and Q10,
with b=.914 and ell=1.6. It gives (3,2) strictly in Q10. This is
O_R in (2). The lower endpoint (3,1.6) of the translated segment T
is G8, strict in the same actual Q10 by the no-omission entrance.
Convexity therefore makes the whole closed segment T strict in Q10
and disjoint from E. Every hypothesis of Theorem 1 is literal.

The preceding successor-sign theorem
C1092-MPPM-NEGATIVE-INWARD-SUCCESSOR-SIGN.md supplies the strictly
negative E orientation for every negative inward profile covered
there, whether the center belongs to Q4 or is omitted, and whether
G0 is omitted or is owned while F0 is omitted. The present theorem
therefore supplies the same face table (4) and angle bound (5) in all
of those actual alternatives. No inward tip or omitted-point owner
has entered this additional profile.
