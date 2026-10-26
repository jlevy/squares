# C1092 MPPM: the centered negative inward angle and its outer-point consequences

Every terminating decimal is exact. Retain the complete actual entrance
of C1092-MPPM-CENTERED-NEGATIVE-INWARD-H-CAP.md. In particular the actual
C=Q4 is nonordinary inward, strictly owns the physical center, and has
negative frame (c,-s),(s,c), c>=s>0. Its actual ordinary successor and
predecessor are E=Q5 and W=Q7. The common side is a>1.

**Theorem 1.** The half-angle of C satisfies

    z_C=s/(1+c)<21/100.                              (1)

**Corollary 2.** The same actual C omits F0. If it owns G0, it strictly
owns (1,1.5), and the actual bottom square Q9 strictly owns (2,1).
Thus the remaining centered negative inward alternatives are:

    F0,G0 both omitted; or
    G0 owned,F0 omitted, with the genuine bottom origin.       (2)

Neither conclusion depends on whether the opposite Q6 is ordinary.

## 1. The actual predecessor profile used in the angle proof

Continue in centered coordinates. The preceding chapter proves

    0<A<=min(.35(c+s),A0), A0=.14c+.5s,
    0<H<=.35(c-s), H<.136,
    D0:=1-A0 satisfies .54<D0<=.86.                 (3)

The proof of Theorem 1 uses only H>0 and H<=.35(c-s) from this line;
the stronger H<.136 is used in Corollary 2.

The actual W data and complete face tables are Sections 2-3 of the
preceding chapter: W strictly owns its marker (-.35,.35) and its pair
(-.26,1),(-.4,1), and excludes the actual top marker Z=(0,1.086) and
the two actual Q3 points C0=(-1,1),C1=(-1,1.086). Denote W's lower
faces by P,Q and upper faces by J_W=P+a,D_W=Q+a.

For its nonnegative frame (b,r),(-r,b), the actual alternatives are

    always D_W<=1.086b+r;
    Z upper v: D_W<=1.086b;
    Z upper u: J_W<=1.086r;
    Z upper u,C0 upper v: D_W<=b+r;
    Z upper u,C0 lower u: D_W<=1.086b+r,
                           r/(1+b)<.086,
                           b+r<29/25.              (4)

For its nonpositive frame (b,-r),(r,b), the actual faces are

    P>=-b-r, J_W>=a-b-r,
    D_W<=1.086b, Q<=1.086b-a.                     (5)

The complete C-to-W normal cone from the same actual marker pair has
n_y>0. C's source -u is defeated by its upper marker cap in (3),
because a-A>.35(c+s), the projection of W's strict marker. Thus C's
only source is v=(s,c). For nonnegative W, the own source (b,r) is
defeated by strict O in C and the nonpositive projection of W's marker.
Only (-r,b) remains. For nonpositive W, its two own upward sources
(r,b),(-b,r) remain. These lists include all weak canonical endpoints.

Suppose for contradiction that z_C>=21/100. Write p=arctan(s/c) and
p0=2 arctan(21/100). The exact endpoint values are

    cos p0=9559/10441, sin p0=4200/10441.

Consequently

    c<=9559/10441,
    s/c>=4200/9559>7/16>2/5,
    c+s>=13759/10441>1.3,
    1-1.086c>=29963/5220500>0.                    (6)

We now exclude both actual W signs without sampling any angle.

## 2. Nonnegative W: its own normal

Put k=cb-sr>=0,j=cr+sb>=0. Its own upward transverse normal (-r,b)
has upper C support j(a-A)+kH. By (3), H>0, and the first row of (4),
the deficit from Q is strictly greater than

    F=1-1.086b-r+jD0
      =1-B0 b-R0 r,                                 (7)

    B0=1.086-s+.14cs+.5s^2,
    R0=1-c+.14c^2+.5cs.

The replacement of a by 1 has positive coefficient 1+j. With
x=s/(1+c), the exact norm identity is

    1-B0^2-R0^2=P0(x)/[250000(1+x^2)^2],             (8)

    P0(x)=-1189749x^4+2308040x^3-2275898x^2
                +863960x-49749.

Its second derivative has negative leading coefficient and negative
discriminant -68169996384192. Thus P0 is strictly concave. Its endpoint
values on the closed interval [21/100,5/12] are

    P0(21/100)=5037642088731/100000000,
    P0(5/12)=106472579/2304.

Both are positive, so P0 is positive everywhere between them. This
interval contains the full C half-angle range now assumed. Cauchy's
inequality gives B0 b+R0 r<1, so (7) is positive. The own W source is
impossible.

## 3. Nonnegative W: C's normal

The exact lower W support on v is jP+kQ.

First suppose Z is upper v. The strict W marker and (4) give

    lower_W(v)<c f_z-s g_z,                         (9)

    f_z=1.086b^2+.35r^2-.35br-b,
    g_z=.35b^2+.736br-r.

If g_z<0, the bound s/c<=1 gives

    f_z-(s/c)g_z<=f_z-g_z
       =(b-r)(.736b-.35r-1)<=0.

If g_z>=0, (6) gives f_z-(s/c)g_z<=f_z-.4g_z. Put w=r/(1+b),
so 0<=w<5/12. Direct expansion gives

    f_z-.4g_z
      =[4865w^4+5222w^3-1230w^2-1222w-135]
                                         /[2500(1+w^2)^2].     (10)

For this entire interval,

    4865w^3+5222w^2
       <=2174725/1728<1260.

Therefore the numerator in (10) is at most

    -135+38w-1230w^2<=-135+38(5/12)=-715/6<0.

Thus (9) is strictly negative in either alternative, below H>0.

Suppose now Z is upper u and C0 is upper v. The exact support bound
from (4), after the strict a replacement, is

    lower_W(v)<c F0-s F1,
    F0=.5(b+r-1)^2+.086r^2<.13,
    F1=r^2+b-r-.086br.                             (11)

In fact F1>=.457. To see this, use br<=1/2 and
b-r=(1-2r^2)/(b+r)>=(1-2r^2)/sqrt(2). The resulting lower bound

    (1-2r^2)/sqrt(2)+r^2-.043

is minimized at r^2=1/2 and equals .457. Thus (6) makes (11) less
than c[.13-.4(.457)]<0.

If C0 is instead lower u, the last row of (4) gives

    lower_W(v)<c G0-s G1,
    G0=.086+.5(b+r-1)^2<.0988,
    G1=r^2+b-r.

Here r<.172 and b>.98, so G1>.808. The support is therefore less
than c[.0988-.4(.808)]<0. This exhausts the three actual face rows
and the second nonnegative-W normal. Hence nonnegative W is impossible.

## 4. Nonpositive W: C's normal when phi<=p

Now let W have frame (b,-r),(r,b), and use (5). Put

    k=cb+sr>0, delta=cr-sb,

where phi=arctan(r/b). Suppose first phi<=p, so e=-delta>=0.
Its lower support on v is eP+kQ. The strict W marker bounds
P<-.35(b+r), and (5) bounds Q. After dropping a to 1 strictly,

    lower_W(v)<c f_l-s g_l,                         (12)

    f_l=1.086b^2+.35br+.35r^2-b,
    g_l=.35b^2-.736br+r>0.

The last sign follows directly from g_l=.35b^2+r(1-.736b)>0.
By (6), it suffices to prove f_l-(7/16)g_l<0. Its exact identity is

    f_l-(7/16)g_l=P_l(w)/[8000(1+w^2)^2],           (13)

    P_l(w)=15463w^4-17752w^3-3726w^2+3752w-537,
    w=r/(1+b), 0<=w<5/12.

The quadratic P_l'' is convex and has endpoint values

    P_l''(0)=-7452, P_l''(5/12)=-235409/12.

Thus P_l''<=-7452 throughout the whole interval. The tangent bound
for this uniformly concave polynomial, with h=w-1/4, is

    P_l(w)<=-12505/256-(7569/16)h-3726h^2
             <=-1593639/47104<0.                  (14)

The final constant is the exact maximum of that quadratic. This
proves (13) negative on the entire canonical domain. Consequently
(12) is negative, contradicting H>0.

## 5. Nonpositive W: C's normal when phi>=p

Now delta>=0. The exact face bound from (5) gives

    lower_W(v)<c f_r-s g_r,
    f_r=.086b^2+.5(b+r-1)^2,
    g_r=b^2-.086br-b+r>=0.                         (15)

As in the preceding cap chapter, g_r>=r(.914-r/2)>=0. The assumed
angle order and (6) give w=r/(1+b)>=21/100. The relevant exact
identity on [21/100,5/12] is

    f_r-(7/16)g_r=P_r(w)/[4000(1+w^2)^2],           (16)

    P_r(w)=4844w^4-19801w^3+10812w^2-3199w+344.

The quadratic P_r'' is convex. Its endpoint values are

    P_r''(21/100)=-952269/1250,
    P_r''(5/12)=-106721/6.

Hence P_r''<0 throughout this interval. Also

    P_r'(21/100)=-274547791/250000<0,
    P_r(21/100)=-311715017/12500000<0.

It follows successively that P_r' is negative and P_r is negative
on the entire interval. By (6), (15) is therefore negative as well.
C's normal has failed in both angle orders, including their equality.

## 6. Nonpositive W: the upward left-facing normal

For n=(-b,r), the exact upper C support is either

    k(a-A)+delta H          if delta>=0,
    k(a-A)+(-delta)(a-H)   if delta<=0.

The additional term in either line is nonnegative because 0<H<a,
by (3). The lower W support is -J_W<=b+r-a. Thus the difference is
strictly greater than

    F=1-b-r+kD0
      =1-(1-cD0)b-(1-sD0)r.                        (17)

The squared norm of its two coefficients is

    (1-cD0)^2+(1-sD0)^2=2-2(c+s)D0+D0^2.

By (3),(6), c+s>1.3 and .54<D0<=.86. The function
D0^2-2.6D0 is decreasing on that whole range. Hence the squared norm
is less than or equal to

    2-2.6(.54)+(.54)^2=.8876<1.

Cauchy's inequality makes (17) positive for every W angle. This
source is impossible without any further relative-angle subdivision.

## 7. Nonpositive W: the upward right-facing normal

For n=(r,b), first suppose phi>=p, so delta>=0. Its upper C support
is delta A+kH>0. But (5),(6) give

    lower_W(n)=Q<1.086b-1<=1.086c-1<0.

Thus this source fails in that angle order.

Suppose phi<=p and put e=-delta>=0. Its upper C support is
e(a-A)+kH>eD0. Using (5) again, the support difference is strictly
greater than

    F=1-1.086b+eD0=1-B b-R r,
    B=1.086-sD0>0, R=cD0>0.                       (18)

If s<=1/2, then

    D0-1.086s=1-.14c-1.586s>=.067>0.

At phi=p, the derivative of B cos phi+R sin phi is
Rc-Bs=D0-1.086s>0. Since B,R>0, the derivative remains positive
for every 0<=phi<=p. Therefore (18) is minimized at phi=p, where
it equals 1-1.086c>=29963/5220500>0.

If s>=1/2, then (3) sharpens to .54<D0<.66: indeed
D0=1-.14c-.5s<.75-.14(.7)=.652. The squared coefficient norm in
(18) satisfies

    B^2+R^2=1.086^2-2.172sD0+D0^2
            <=1.179396-D0(1.086-D0).

The concave quadratic D0(1.086-D0) is at least .28116 on the closed
interval [.54,.66], by its two endpoints .29484 and .28116. Hence
B^2+R^2<=.898236<1, and Cauchy's inequality makes (18) positive.
This includes s=1/2 and exhausts the last actual source.

Every strict replacement of a by 1 in Sections 2-7 has positive
coefficient: 1+j in (7), k or j+k in the C-normal comparisons,
1+k in (17), and 1+e in (18). All other uses of strictness come
from actual owned points or from H>0. Thus no tangency or canonical
endpoint is omitted. The contradiction to z_C>=21/100 proves
Theorem 1.

## 8. The actual outer halfpoint when either outer anchor is owned

Combine Theorem 1 with the preceding chapter's H<17/125. Suppose C
strictly owns at least one of

    F0=(-1,-.26), G0=(-1,-.4)

in centered coordinates. We prove that P=(-1,-.5) is strict in C.
Its lower u-band follows from the owned outer anchor, with positive
increment .24s or .1s. Its upper u-band follows from C's marker,
with increment .65c-.15s>=.5c>0. Its upper v-band follows from
the same outer anchor, with increment .24c or .1c.

For the remaining lower v-band, use V=H-a. The function
sin p+.5cos p is strictly increasing on the canonical interval.
At p0 its exact value is 17959/20882. Consequently

    v(P)-V=a-H-s-.5c
       >1-17/125-17959/20882
        =10381/2610250>0.                           (19)

Thus P is strictly inside the same actual C.

If F0 belonged to this nonordinary C, G0 would be omitted. But G0
lies strictly between F0 and P on their vertical segment. Convexity
would put G0 strictly in C, a contradiction. Therefore F0 is
omitted in every centered negative nonordinary inward case.

If G0 is owned, P=(1,1.5) is strict in original coordinates. Apply
the actual paired-corner transfer, Theorem 7 of
C1092-DIRECT-WALL-POINT.md, to K=Q0 and B=Q9, with b=.914 and ell=1.6.
The actual Q0 strictly owns (1,.914),(1,1), is contained in the real
first-quadrant walls, and excludes (1,1.5) because the different
actual Q4 owns it. The actual Q9 strictly owns (2,.914),F2=(1.6,1)
and obeys the genuine bottom wall. The transfer therefore gives
(2,1) strictly in Q9. This proves Corollary 2 and its exact scope.

The case omitting both F0,G0 has not been assigned either outer
anchor or this conditional bottom origin. It remains separate until
an actual-owner argument supplies further information.
