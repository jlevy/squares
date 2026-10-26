# C1092 MPPM: a negative forward-owned predecessor supplies a positive successor's halfpoint

Every terminating decimal denotes an exact rational number. Owned points are strict in their named actual open squares. Exclusion permits boundary equality, and separating supports may be equal. The local theorem below uses a common side a>1 and no upper side bound. Its global applications retain the original no-omission, all-four-ordinary MPPM entrance.

There are two separate statements. First, every nonpositive forward-owned ordinary square excludes its preceding wall origin, even when that wall does not own the origin. Second, such a square supplies its positive successor's ordinary halfpoint. The latter argument does not require the successor to exclude its backward inner point. Thus an ordinary/inward overlap is explicitly allowed in the successor.

## 1. A genuine exclusion of the preceding origin

Use the original sector charts R^(-i), where R(x,y)=(4-y,x), and write

    C_i=Q_(4+i), (B_0,B_1,B_2,B_3)=(Q9,Q10,Q11,Q8).

Each C_i is ordinary. Its local strict ordinary points and marker are

    M=(1.65,1.65), U0=(1,1.74), L0=(1,1.6).

The forward point is T=(1.74,2), the wall origin of B_i is P=(2,1), and the preceding wall origin in C_i's chart is D=(1,2).

**Theorem 1.** If C_i has nonpositive canonical orientation and owns T, it excludes D.

If the actual B_(i-1) owns its local P, that strict foreign ownership gives the conclusion immediately. Suppose instead that this actual wall omits P. Its preceding central C_(i-1) cannot omit its forward point, because Corollary3 of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md would then give P in that wall. Nor can C_(i-1) be nonpositive, by the unconditional halfpoint and actual-origin Corollary2 of C1092-MPPM-ORDINARY-NEGATIVE-HALFPOINT.md. Hence C_(i-1) is positive and owns its forward point.

The actual paired-corner transfer, Theorem7 of C1092-DIRECT-WALL-POINT.md, now gives its contrapositive: the paired corner of C_(i-1) strictly owns that sector's H=(1,1.5). Thus H is excluded from C_(i-1). The local two-square Theorem1 of C1092-MIXED-NEGATIVE-DISK.md applies to the actual positive predecessor and the actual nonpositive C_i. Its two squares both have the four strict local points M,U0,L0,T. Its additional predecessor exclusions are H and the original points

    N=(1.65,2.35), W=(.914,2), F0=(1,2.26).

The exact sources in the predecessor's chart are C_(i-2) for N and B_(i-2) for W,F0. These are genuine original strict points of those actual owners, independent of any other forward membership. That local theorem concludes that C_i excludes D. This proves Theorem1 in the missing-wall alternative as well. In particular it assigns no owner to D when D is not strict in the preceding wall.

## 2. The local two-central-square and one-bar statement

Translate a southwest chart by (-2,-2). Let C,E be actual disjoint open squares of common side a>1. Suppose C has the nonpositive frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,

and strictly owns

    M=(-.35,-.35), P0=(-1,-.26), G0=(-1,-.4),
    T=(-.26,0).

Suppose C excludes

    D=(-1,0), N=(-.35,.35).

Suppose E has the nonnegative frame

    e=(d,t), f=(-t,d), d>=t>=0, d^2+t^2=1,

and strictly owns

    M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1),
    I=(0,-.26).

Finally retain an actual open square B, disjoint from C, that strictly owns the whole segment

    [-.56,0] x {-1}.                               (1)

**Theorem 2.** Under these hypotheses E strictly owns Y=(.5,-1).

There is no premise excluding (.26,0) from E, and no premise excluding (0,.26) from C. Those are the potentially reassigned inner points that must not be treated as foreign in a partial-forward cycle.

## 3. The negative predecessor's actual faces and wall clearance

Write U,V for C's lower faces and A=U+a,H=V+a for its upper faces. At D its upper u-band and both v-bands are strict by P0,G0,T. Therefore it is lower u. The point I is strictly in E, so it is excluded from C; its lower u- and v-bands and upper v-band are strict by P0,T, so it is upper u. At N the other three bands follow from P0,T, with increments

    .65c-.61s>=.04c>0, .09c+.35s>0,
    .35c-.09s>=.26c>0.

Consequently

    U>=-c, A<=.26s, H<=.35(c-s).                  (2)

The first two faces imply

    1<a<=c+.26s.

For x=s/(1+c), the exact identity

    c+.26s-1=2x(.26-x)/(1+x^2)

therefore gives

    0<x<13/50, c>.87, s<.49.                     (3)

The axial case is impossible already because D and strict P0 would have equal u-projection. The displayed rational cosine and sine bounds follow from the endpoint x=13/50, at which they are 2331/2669 and 1300/2669.

Let F=(-.56,-1), strict in the same actual B as (1). Its lower u-band and upper v-band in C follow from P0, with positive increments .44c+.74s and .74c-.44s. If F were upper u, (2) would give a<=.44c+s. But

    1-(.44c+s)=(1-x)(14-36x)/[25(1+x^2)]>0

throughout (3). Thus F is lower v and

    V>=-c-.56s.                                   (4)

The lowest closed vertex of C is Z=A u+V v. Its abscissa satisfies

    Z_x>=ac-1+.44s^2-cs>c-1+.44s^2-cs>-.56.       (5)

For the last inequality the exact difference is

    c-.44+.44s^2-cs
      =(1-x)^2(1+x)(14-36x)/[25(1+x^2)^2]>0.

If Z_y<=-1, (2) gives c Z_x<=s(Z_y+.26)<=0, so Z_x<=0. The segment from Z to the strict C point T then meets y=-1 with abscissa in (-.56,0]. That point is in the actual strict B segment (1), a contradiction. This reasoning also includes Z_y=-1: a closure point of C in the open B would force the two open interiors to intersect. Hence Z_y>-1.

Write (X_C,Y_C) for the actual center of C. We have proved

    Y_C>-1+a(c+s)/2.

Together with U=cX_C-sY_C-a/2>=-c and a>1, this yields

    Y_C>Y_*=-1+(c+s)/2,
    X_C>X_*=-1+[1/2+sY_*]/c.                     (6)

Neither (2) nor this wall-clearance proof used the potentially reassigned point (0,.26). The genuine foreign marker N supplied the needed upper transverse cap.

## 4. The successor's only missing-halfpoint face

Write L,K for E's lower faces and J=L+a,Q=K+a for its upper faces. At Y its lower e-band and upper f-band are strict from B1. Hence an excluded Y is upper e or lower f.

Suppose it were upper e, so J<=.5d-t. Strict M_E would then give .15d-.65t>0, or t/d<3/13. In this range the foreign C marker M has its upper e-band and both f-bands strict in E. These follow from I,B0,I, respectively, and the remaining comparison is

    .09d-.35t>0,

because 3/13<9/35. Thus M would be lower e, giving L>=-.35(d+t). The opposed width would be

    a<=.85d-.65t<1,

a contradiction. Therefore a missing Y can only be lower f:

    K>=-d-.5t, Q>=a-d-.5t.                        (7)

This proof includes t=0. In that endpoint the same lower-band equality with the strict ordinary anchor already makes a missing Y impossible; it is harmless to retain (7) in all subsequent support estimates.

## 5. The exhaustive actual separating normals

Orient every separating normal from C toward E. Their strict markers give n_x>0, and the strict pair T,I gives n_x-n_y>0. Among all signed face normals of the two actual squares, the only possibilities are

    u, e, -f.                                     (8)

A direction becoming ineligible at an axial or diagonal endpoint can still be retained for exclusion. Set

    k=cd-st>0, ell=ct+sd>0.

The strict positivity follows from c>s and d>=t>=0 under (3). The exact changes of frame are

    u=k e-ell f, e=k u+ell v, -f=ell u-k v.

All three support arguments below preserve the coefficient of the same actual side a until its sign has been checked.

### 5.1. E's longitudinal normal: retain the anchor offset

The exact upper C support, (6), and a>1 give

    upper_C(e)>dX_*+tY_*+(k+ell)/2
               =(1-c)(d kappa-t),
    kappa=(1-x)/(1+x)>0.                           (9)

The identity in (9) is exact. The strict E point I gives lower_E(e)<-.26t. Therefore the support difference is strictly greater than

    (1-c)d kappa+t(c-.74)>0,                       (10)

since 0<c<1 and c>.87. This excludes e for the entire nonnegative E angle domain. In particular no bound on E's half-angle, and no exclusion of its backward inner point, was needed.

### 5.2. C's longitudinal normal: the full positive-angle scalar

The exact lower E support and (7) give

    lower_E(u)=kL-ell Q
       <-.26kt-ell(a-d-.5t).

Comparison with upper_C(u)=A>=a-c would require the support excess to be nonpositive. But that excess is strictly greater than the following scalar, obtained by decreasing a to 1 in the positive coefficient 1+ell:

    F=1+ell-c-ell d-.5ell t+.26kt
      =1-Pc-Rs,
    P=1-t+.5t^2+.74dt,
    R=1-d+.5dt-.74t^2.                             (11)

Put y=t/(1+d), so 0<=y<=sqrt(2)-1<5/12. Direct substitution gives

    1-P^2-R^2
      =2y[325-1647y+3425y^2-1250y^3]
           /[625(1+y^2)^2].                        (12)

The cubic bracket is positive on this full domain. Indeed

    3425-1250y>=17425/6,

and therefore it is at least

    (17425/6)(y-4941/17425)^2+3188423/34850>0.      (13)

Thus P^2+R^2<=1, with equality allowed only at y=0. Cauchy's inequality gives F>=0. The strictly positive coefficient of a>1, or the strict owned-anchor bound on L, then makes the actual support excess positive even at that endpoint. Hence u cannot separate.

### 5.3. E's downward transverse normal: use the actual marker cap

By (2),(7),

    upper_C(-f)>=ell(a-c)+k[a-.35(c-s)],
    lower_E(-f)=-Q<=d+.5t-a.

Their excess is strictly greater than

    1+k+ell-d-.5t-ell c-.35k(c-s)
       =1-P1 d-R1 t,                              (14)

after replacing a by 1 in the positive coefficient 1+k+ell, where

    P1=1-c-s+.65cs+.35c^2,
    R1=1.5-c+s-.35cs-.65s^2.

The whole predecessor range (3) gives P1<.4. To see this, the term s(.65c-1) is nonpositive, while 1-c+.35c^2 decreases for .87<c<=1; at c=.87 it equals .394915<.4.

Also

    R1<.63+.6955s-.65s^2
       <=652837/800000<.82.                        (15)

The maximum in (15) is the exact completed-square maximum of that quadratic. Since d,t>=0,

    P1d+R1t<.4d+.82t<=sqrt(.8324)<1.

Thus (14) is positive, excluding -f. This replaces an upper cap at a potentially reassigned auxiliary by the actual neighboring-marker cap and is valid for every positive successor angle.

All actual sources in (8) have been excluded. This contradicts disjointness under the supposed missing Y and proves Theorem2.

## 6. The literal original transfer

**Corollary 3.** In the original no-omission OOOO family, if a nonpositive ordinary C_i owns its forward point, then the next ordinary C_(i+1) strictly owns its ordinary outer halfpoint, regardless of that successor's sign or its backward inner membership. The next actual wall B_(i+1) therefore owns its local origin P.

A nonpositive successor already has its halfpoint by C1092-MPPM-ORDINARY-NEGATIVE-HALFPOINT.md. A successor omitting its forward point already has it by the ordinary-marker halfpoint theorem. In the remaining alternative the successor is positive and owns its forward point, so normalize C_i=Q4 and C_(i+1)=Q5. Theorem1 supplies the genuine D exclusion of C=Q4. The unconditional nonpositive halfpoint theorem gives (1,1.5) in C and hence the actual bottom origin (2,1) in Q9. The genuine ordinary advance puts (1.44,1) in that same Q9. These two strict points supply the whole actual segment (1).

Every local input of Theorem2 has the following literal source:

| Local datum | Original point or actual source |
|---|---|
| C's M,P0,G0,T | Q4 marker,F0,G0 and its explicit forward G3 |
| C excludes D=(-1,0) | Theorem1, with no invented owner in the missing-wall case |
| C excludes N=(-.35,.35) | The actual Q7 marker |
| E's M_E,B0,B1,I | Q5 marker,G5,F6 and its explicit forward F4 |
| Whole [-.56,0] x {-1} in B | Actual Q9 points (1.44,1),(2,1) |

It follows that Y=(2.5,1) is strict in Q5. The actual paired-corner transfer, with Q1 and Q10, b=.914 and ell=1.6, now gives (3,2) in Q10. All hypotheses of that transfer are original strict Q1/Q10 anchors or the halfpoint just proved. Simultaneous quarter-turns give every sector of the corollary.

The result removes the backward-inner exclusion from the negative-to-positive halfpoint transfer. It does not yet settle a negative predecessor that omits its own forward point, nor does it assert a wall-center order for a forward-owned sector. Those remaining alternatives keep their actual ownership distinctions.
