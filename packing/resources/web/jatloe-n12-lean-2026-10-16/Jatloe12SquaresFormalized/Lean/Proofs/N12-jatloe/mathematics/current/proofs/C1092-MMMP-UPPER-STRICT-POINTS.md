# C1092 MMMP: further strict points from the actual upper owners

Every terminating decimal is an exact rational. All squares are the original actual open squares, with common side 1<a<=1.001 and disjoint interiors. Owned points are strict; excluded points and separating supports may be tangent. No top-origin premise is used.

**Theorem.** Throughout the original MMMP family,

    (2.14,2.5) is strictly in Q6,
    (1.2,2.16) and (1.19,2.2) are strictly in Q7.        (1)

The proof also establishes the following useful angle implication directly from the actual Q7/Q6 pair: if Q7 has a nonpositive canonical angle, its sine magnitude is less than .14.

## 1. Literal starting ownership

The completed northwest center and crosspoint arguments, together with `INWARD-CENTER-DIAGONAL-POINT.md`, give the full strict square

    [1.5,2] x [2,2.5] in the same actual Q7.             (2)

The inward-point corollary and its exact transposed application in `C1092-MMMP-SECOND-INWARD-TIP.md` give

    (1.99,2.54) strictly in Q7.                          (3)

The original northwest marker is also strict in Q7. The southwest and northeast markers remain strict in their distinct actual owners Q4,Q6.

By `C1092-MMMP-NORTHEAST-ANGLE.md`, Q6 has a strictly positive canonical angle. Use the common quarter-turn chart

    (X,Y)=(2-y,x-2),  C=Q7, B=Q6.

Then C owns O=(0,0), A=(-.5,0), D=(0,-.5), and M_C=(-.35,-.35). It excludes G=(.35,-.35), the original southwest marker, and M=(-.35,.35), the northeast marker of B. The actual B owns M,H1=(-1,.26),H2=(-1,.4).

Write B's frame and lower faces as

    u_B=(b,t), v_B=(-t,b), b>=t>0, b^2+t^2=1;  p,q.

The original marker and actual auxiliary deductions of `C1092-MMMP-RIGHT-FAR-AUXILIARY.md` give the four full face inequalities

    p>=-1.086b,  p+a<=t-.4b,
    q>=.4t,     q+a<=b+t.                              (4)

In particular the foreign point (3,2.4) used there is strictly in the actual Q10. Its ownership was deduced from the original Q10 G-covering row and the proved double-span implication, rather than presumed from other squares' absences.

## 2. The northeast point

The target (2.14,2.5) becomes Z=(-.5,.14). Its projections are

    u_B(Z)=-.5b+.14t,  v_B(Z)=.5t+.14b.

All four strict bands follow from (4). Their respective lower bounds are

    u_B(Z)-p       >= a-.1b-.86t,
    p+a-u_B(Z)     >= a-.586b-.14t,
    v_B(Z)-q       >= a-.86b-.5t,
    q+a-v_B(Z)     >= a-.1t-.14b.                      (5)

Each is positive by a>1 and Cauchy--Schwarz, since the four squared coefficient norms are respectively

    .7496, .362996, .9896, .0296,

all strictly less than one. Thus all four target bands are strict, proving the first point in (1).

## 3. The nonpositive northwest angle is small, without a top origin

This section reproduces the applicable positive-neighbor support calculation so its actual premises are explicit. Suppose C has nonpositive canonical frame

    u_C=(d,-r), v_C=(r,d), d>=r>=0, d^2+r^2=1.

Write u,v for its upper faces, so its lower faces are u-a,v-a. Since O is strict, u,v>0. At G the lower u-band and upper v-band follow from O, and its lower v-band follows from D with positive increment .35r+.15d. Therefore G is upper u and

    0<u<=.35(d+r),  v>0,  v-a<-.5d.                   (6)

Only two forward transverse separators can remain between the full actual C and B. Here is the complete elimination of the other face axes. Both orders on C's u-axis fail: C-before-B is contradicted by O and M, while B-before-C fails because

    u-a<=.35(d+r)-a<-.35(d+r)=u_C(M).

The last strict inequality uses .7(d+r)<=.7sqrt(2)<1<a. C-before-B on B's u-axis is contradicted by O and H2, whose u_B projection is -b+.4t<0.

For B-before-C on B's u-axis put

    alpha=bd-tr>=0,  k=br+td>0.

The lower full C support is alpha(u-a)+k(v-a). Using (6) and subtracting the strict B-marker projection -.35b+.35t gives a strict upper bound bF0+tG0, where

    F0=.7-d-.35r^2-.15dr<0,
    G0=-.85+r+.15r^2-.35dr
       <=-.85+r-.20r^2<0.                             (7)

For F0 use d>=1/sqrt(2)>.7; for G0 use d>=r and r<=1/sqrt(2)<5/7. Thus this order fails too. Finally, on either upward transverse normal, the order placing B before C is impossible because M_C and M have the same x-coordinate and their y-coordinates differ by .7. Both normals have strictly positive y component.

The exhaustive remaining possibilities are consequently

    v<=lower_B(r,d),
    upper_C(-t,b)<=q.                                 (8)

For the first, define H_B=b+t and

    K=H_B-1-.61bt
     =(H_B-1)[1-.305(H_B+1)]>0.                        (9)

Here 1<H_B<=sqrt(2)<10/7. We may weaken p+a<=t-.4b to p+a<=t-.39b. Formula (4) and a>1 then give

    lower_B(r,d)=k p+alpha q
       < k(t-.39b-1)+alpha(H_B-1)
       =-dK+r(t-b-.39-.61t^2)<0.                     (10)

This contradicts v>0. Thus the only possible actual separator is the second one in (8), whose complete C support is

    upper_C(-t,b)=k(a-u)+alpha v.

Using q<=H_B-a, it gives

    a(1+k)<=H_B+k u-alpha v.                           (11)

Put H=d+r and q0=1-.35H. From (6), a>1 and v>0, equation (11) implies

    1<bF+tG0',
    F=1-r q0,  G0'=1-d q0.                            (12)

Both coefficients are positive. Hence F^2+(G0')^2>1. Direct expansion gives the exact identity

    F^2+(G0')^2-1=P(H),
    P(H)=2-2.7H+.8225H^2.                             (13)

On 1<=H<=10/7,

    P'(H)=-2.7+1.645H<=-.35,
    P(1.13)=-2999/4000000<0.

Therefore H<1.13. The function sqrt(1-r^2)+r increases on the entire canonical interval, and at r=.14 its value exceeds .99+.14=1.13 because .9804>.9801. We have proved

    r<.14,  d>.99.                                    (14)

This calculation used only the two upper faces in (4), together with the actual C/B anchors and actual square separation. In particular it used neither p>=-b nor a top-origin point.

## 4. The northwest point in both signs

Return to original coordinates. Write Z=(2.14,2.5) for the proved Q6 point and X=(1.2,2.16) for the desired Q7 point. Since Q6 and Q7 are distinct actual owners, Z is genuinely excluded from Q7.

First let Q7 have a nonnegative frame (d,r),(-r,d). At Z its lower u-band follows from O=(2,2), its lower v-band also follows from O because .5d-.14r>0, and its upper v-band follows from the strict Q7 point (2,2.5), with projection increment .14r>=0. Thus Z is upper u.

Its upper-u face supplies the strict lower u-band of X, because

    u(Z)-u(X)=.94d+.34r
       <=sqrt(.94^2+.34^2)=sqrt(1249/1250)<1<a.       (15)

The upper u-band of X follows from the strict point (1.5,2): the projection increment is .3d-.16r>=.14d>0. Its lower v-band follows from O, with increment .8r+.16d>0. Its upper v-band follows from (1.5,2.5), with increment .34d-.3r>=.04d>0. Hence X is strict in this sign.

Now let Q7 have the negative frame (d,-r),(r,d). Section 3 gives (14). At Z both lower bands follow from O; the u increment satisfies

    .14d-.5r>.14(.99)-.5(.14)=.0686>0.

Its upper v-band follows from the actual second inward tip (1.99,2.54), because

    v(1.99,2.54)-v(Z)=.04d-.15r
       >.04(.99)-.15(.14)=.0186>0.                   (16)

Therefore Z again exits upper u. The lower u-band of X is strict since

    u(Z)-u(X)=.94d-.34r<=.94<1<a.

The upper u-band follows from (1.5,2), with positive increment .3d+.16r. The lower v-band follows from O, since

    v(X)-v(O)=.16d-.8r>.1584-.112=.0464>0.

Its upper v-band follows from (1.5,2.5), with positive increment .3r+.34d. This proves the second point in (1) for the negative sign as well.

The axial case is included in both calculations. Diagonal Q7 in a negative canonical representation is already excluded by (14); in the positive representation the nonnegative proof includes it. Every use of an equal projection is a comparison with an already strict owned point, so no tangency or endpoint has been lost. This completes the all-angle proof. ∎

## 5. A point adapted to the left-wall transfer

The same forced upper-u exclusion of Z proves the additional strict point

    X1=(1.19,2.2) in Q7.                               (17)

For a nonnegative Q7 frame, its lower u-band follows from

    u(Z)-u(X1)=.95d+.3r
       <=sqrt(.95^2+.3^2)=sqrt(.9925)<1<a.

Its upper u-band follows from the strict point (1.5,2.5), with increment .31d+.3r>0. Its lower v-band follows from O, with increment .81r+.2d>0. Its upper v-band follows from the strict diagonal point (1.39,2.61), proved in `INWARD-CENTER-DIAGONAL-POINT.md`, with increment .41d-.2r>=.21d>0.

For the negative frame, Section 3 gives r<.14,d>.99. The lower u-band follows from .95d-.3r<=.95<1<a. Its upper u-band follows from (1.5,2), with positive increment .31d+.2r. The lower v-band follows from O, since

    .2d-.81r>.198-.1134=.0846>0.

The upper v-band again follows from (1.39,2.61), now with positive increment .2r+.41d. Thus (17) is strict in both signs, including the axis and every admissible diagonal representation.

These newly proved points strengthen the actual upper-owner hulls. They do not by themselves assert that the whole MMMP configuration is impossible.
