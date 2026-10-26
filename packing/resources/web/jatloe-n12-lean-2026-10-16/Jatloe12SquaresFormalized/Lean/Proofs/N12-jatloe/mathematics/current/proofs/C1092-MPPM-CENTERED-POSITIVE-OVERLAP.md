# C1092 MPPM: a positive ordinary/inward overlap cannot own the center

All terminating decimals are exact rationals. Retain the original no-omission, all-four-ordinary MPPM entrance and its actual twelve owners. Every owned point is strict; an excluded point may lie on a face. The original common-side range

    1<a<=1.001

is used explicitly below. No angle subdivision or numerical search is used.

**Theorem 1.** Suppose an ordinary central square additionally owns both points of its inward pair. If it has a nonnegative canonical orientation, it does not strictly own O=(2,2).

Normalize that square to C=Q4. Thus the actual strict points of C include its marker, its ordinary pair F0,G0, and its inward pair F4,G3. The conclusion applies to this overlap even though C is ordinary. In particular it does not invoke any theorem whose premise says that C omits an outer ordinary point.

## 1. The shared local entrance

Translate by (-2,-2), and write C=Q4,E=Q5,W=Q7. Suppose for contradiction that O=(0,0) is strict in C, and use its nonnegative frame

    u=(c,s), v=(-s,c), c>=s>=0, c^2+s^2=1.

Write U,V for the lower faces and A=U+a,H=V+a for the upper faces. We have U,V<0<A,H. The strict C points include

    M_C=(-.35,-.35), I=(0,-.26), J=(-.26,0),
    P=(-1,-.26), G=(-1,-.4).

The actual ordinary neighbors have strict points

    E: M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1);
    W: M_W=(-.35,.35), T0=(-.26,1), T1=(-.4,1).

The genuine no-omission walls retain the ordinary pairs and advances in C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md. In particular the actual bottom square Q9 strictly owns (1.44,1). The retained inward crosspoint argument therefore puts X=(-.5,0) in C. This is the same local point inference used in Section1 of C1092-MPPM-CENTERED-POSITIVE-INWARD-ENDING.md; its use here does not require the nonordinary status that was used there to obtain the already-assumed ordinary neighbors.

The two foreign markers force

    0<A<=.35(c-s), 0<H<=.35(c+s).                 (1)

Indeed M_W has its other three bands strict by M_C,O, so it is upper v. At M_E only upper u or lower v remain; lower v would oppose the M_W cap at width at most .7(c+s)<=.7sqrt(2)<1. Thus it is upper u.

The point Y=(0,-.5) is strict in C. Its lower u-band follows from X, both upper bands from O, and its lower v-band follows from (1):

    v(Y)-V>=a-.85c-.35s>=a-sqrt(.845)>0.

The actual inward-center diagonal theorem gives (-.5,-.5) as well. Hence C strictly contains the whole rectangle [-.5,0] x [-.5,0]. The actual E halfpoint Y_E=(.5,-1) follows from ORDINARY-MARKER-HALFPOINT.md, using its marker and ordinary pair and the genuine exclusions I, the bottom marker, the paired southeast corner, and F8 in Q10. The actual paired-corner transfer then gives the right origin (1,0) in Q10.

These are exactly the rectangle, neighboring-square and genuine wall/corner inputs used in Sections2--4 of C1092-MPPM-CENTERED-POSITIVE-INWARD-ENDING.md. No inward tip is among those inputs.

## 2. Consequences that do not use an omitted outer point

For precision, we record the reusable conclusions of those sections and their dependencies.

First, Section2 excludes every nonnegative orientation of E. Its cited local calculation is Sections2--4 of C1092-MMMP-NORTHEAST-ANGLE.md after transposition. It uses the strict rectangle of C, the two E ordinary points and marker, and the actual excluded Q10 short segment, Q9 marker and paired Q1 inner point. It does not use the additional point in that chapter's Section5 or any omitted outer point of C.

Write E's resulting strictly negative frame as

    e=(d,-t), f=(t,d), d>=t>0, d^2+t^2=1,

with lower faces L,K and upper faces J_E,D_E. The face proof in Section2 and the two-source calculation in Section3 of the centered-inward chapter give

    L>=.26t, J_E<=d+t, K>=-1.086d,
    D_E<=t-.4d.                                  (2)

The second lower bound L>=-.01d+.54t in that chapter used its extra inward tip. That lower bound is not used here. Each bound in (2) uses only the inputs already supplied above: I, the actual right origin, actual Q1 inner point, actual Q9 marker, and G8 in actual Q10. Section3's two possible separating normals are u,e; the strict C point Y and strict E point Y_E exclude the upward transverse E normal, and (1) excludes C's downward transverse normal. Its exclusion of the alternative G8 upper-u face uses neither the omitted-point premise nor the extra tip.

Put k=cd-st>=0 and j=ct+sd>0. Section4 of that chapter uses only (1),(2), strict A>0 and a>1. It excludes the source u and leaves the exact necessary source inequality

    kA+j(a-H)<=L<=d+t-a.                          (3)

For completeness, (3) gives

    1<d(1-sq0)+t(1-cq0), q0=1-.35(c+s)>0.

The squared coefficient norm minus one is

    2-2.7(c+s)+.8225(c+s)^2.

This quadratic decreases on 1<=c+s<=sqrt(2), and its value at 1.13 is -2999/4000000. Consequently

    c+s<1.13, s<.14, c>.99.                       (4)

The transverse width in (2) gives t+.686d>1, hence

    z=t/(1+d)>157/843>.186.

From (3), strict A>0 and a>1,

    H>1-(d+t-1)/j>=1-(1-z)/(c+s).

On (4), c+s>=1+.92s. The exact calculation

    z-.186+s(.08888-.6072s)>0

then yields

    H>.186+.66s.                                  (5)

This reproduces the only lower-face conclusion needed from Section4 and shows explicitly that its derivation never used an outer omission or the extra tip.

## 3. The ordinary point supplies the small cap directly

The present overlap has the additional strict ordinary point P=(-1,-.26). Therefore

    U<u(P)=-c-.26s,
    A<a-c-.26s<=1.001-c-.26s<.011.                (6)

On (4),

    .14c-.5s>.14(.99)-.5(.14)=.0686>.011.

Thus (6) supplies the stronger-than-needed cap

    0<A<.14c-.5s.                                 (7)

In the nonordinary centered-inward proof, its Section5 obtained this cap from an extra strict southeast point and an inward tip arising from omitted G0. Here the actual ordinary point P and the stated side upper bound supply (7) directly. No tip or G0 omission is asserted.

## 4. The same actual predecessor contradiction

Sections6--8 of C1092-MPPM-CENTERED-POSITIVE-INWARD-ENDING.md prove the following local implication on the exact hypotheses (4),(7), strict O in C, and the actual ordinary W points:

    H<.136+s.                                     (8)

Its only additional excluded W points are (0,1.086),(.26,1) in actual Q11 and (-1,1),(-1,1.086) in actual paired Q3. All are original strict points of those owners here. That proof exhausts both canonical signs of the same actual W and every actual separating normal. Its positive-W part uses only the small C cap and angle range; its negative-W part ends with the exact quartic estimate (36)--(37) of that chapter. Neither part uses C's nonordinary status, its inward tip, or an omitted outer point once (4),(7) are supplied. Thus (8) applies literally to the present overlap.

Equations (5),(8) are incompatible, since

    (.186+.66s)-(.136+s)=.05-.34s
       >.05-.34(.14)=3/1250>0.

This contradiction proves Theorem1, including the axial C representative and all possible weak exterior contacts.

## 5. Scope and literal sector map

The argument uses three actual central squares C,E,W. It never assumes anything about the opposite central's forward or inward ownership. The ordinary pairs of E,W are part of the OOOO premise. The two inward points of C and O are explicit hypotheses; the extra ordinary P and the original upper side bound supply the substitute cap (6). In particular the theorem is not an assertion that an ordinary/inward overlap is itself impossible: a nonnegative overlap is proved here to exclude the center.

Simultaneously rotate the entire proof by R(x,y)=(4-y,x). The four inward pairs to which the conclusion applies are

| Actual ordinary owner | Its additional inward pair |
|---|---|
| Q4 | F4,G3 |
| Q5 | F4,G6 |
| Q6 | F5,G6 |
| Q7 | F5,G3 |

The ordinary-point premise P and both actual neighbors, wall squares and paired corners rotate with their roles. No point from a separately rotated configuration is added to a fixed unrotated owner.
