# C1092 MPPM: every nonpositive ordinary central square receives its halfpoint in OOOO

All terminating decimals are exact rationals. Owned points are strict in
their actual open square. Excluded faces and separating supports may
meet with equality. The common side is a>1. The local theorem uses no
upper side bound, container wall, or numerical orientation subdivision.

## 1. A two-square transfer with a marker upper cap

**Theorem 1.** Let C,E be actual open squares with disjoint interiors
and the same side a>1. Suppose C has the nonpositive canonical frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,

with lower faces U,V and upper faces A=U+a,H=V+a. Suppose it strictly
owns M_C=(-.35,-.35), and its actual faces satisfy

    U>=-1.086c, H<=.35(c-s).                        (1)

Suppose E has the nonpositive canonical frame

    e=(d,-t), f=(t,d), d>=t>=0, d^2+t^2=1,

and strictly owns

    M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1),
    I=(0,-.26).                                    (2)

Then E strictly owns Y=(.5,-1).

The source square C is not required to own its forward inner point.
Its marker upper cap in (1) replaces the cap used in
C1092-NEGATIVE-H-PROPAGATION.md. The proof below checks all four
normal/order combinations under exactly the new hypotheses.

## 2. The missing target and exhaustive actual normal list

Write L,K for E's lower faces and J=L+a,D=K+a for its upper faces.
At Y its lower e and f bands follow from B1, with increments .1d>0
and .1t>=0. Its upper f band follows from M_E, with increment
.65d-.15t>=.5d>0. Thus a missing Y is upper e and gives

    J<=h:=.5d+t.                                   (3)

The strict points B0,I also give

    K<r:=.26t-d, D>z:=-.26d.                      (4)

Orient a possible separating normal from C toward E. Their strict
markers force n_x>0. Comparing M_C with B0 also forces

    .61n_x-.65n_y>0.                               (5)

Each positive transverse normal v,f has vertical component at least
its horizontal component, and therefore fails (5). Their negatives
and both negative longitudinal directions have nonpositive horizontal
component. The separating-axis theorem consequently leaves only

    u, e.                                          (6)

Let p,q be the nonnegative magnitudes of the C,E angles, and put

    k=cd+st=cos(q-p)>0,
    delta=ct-sd=sin(q-p), eta=793/500=1.586.

Then u=k e+delta f and e=k u-delta v. The strict C marker also gives

    H>-.35(c+s).                                   (7)

The following elementary scalar bounds will be useful:

    .886^2+.3^2=218749/250000<1,
    eta^2+1=878849/250000<1.9^2,
    .9^2+.26^2=1097/1250<1,
    .9^2+.35^2=373/400<1.                          (8)

## 3. C's longitudinal normal, both relative-angle orders

Suppose first q>=p, so delta>=0. The exact lower E support on u is
kL+delta K. From (1),(3),(4), separation would imply

    a(1+k)<=eta c+s-.24delta t<=eta c+s.            (9)

Since 0<=q-p<=pi/4-p,

    k>=cos(pi/4-p)=(c+s)/sqrt(2)>=.7(c+s).

Thus

    1+k-eta c-s>=1-.886c-.3s
       >=1-sqrt(218749/250000)>0.

This contradicts (9) and a>1.

If q<=p, then delta<=0 and the exact lower support is kL+delta D.
The strict lower bound on D in (4) now gives the valid weak necessary
inequality

    a(1+k)<=eta c+s+delta(.74d-.5t).                (10)

Put gamma=p-q, so k=cos gamma,delta=-sin gamma. Subtract k from
the right side of (10) and expand exactly to obtain

    (eta d+t-1)cos gamma+(.26d-1.086t)sin gamma.

Its first coefficient is less than .9 by (8), and its second is at
most .26. Both trigonometric multipliers are nonnegative, so (8)
bounds this expression strictly below 1. Equation (10) is impossible.
This exhausts C's source, including equality of the two angles.

## 4. E's longitudinal normal when q>=p

Here delta>=0 and the exact upper C support on e is kA-delta V.
From (1) it is at least

    k(a-1.086c)+delta[a-.35(c-s)].

Comparison with L<=h-a would require

    a(1+k+delta)<=1.086kc+.35delta(c-s)+.5d+t.       (11)

Put gamma=q-p. Subtract k+delta from the right side and use
d=c cos gamma-s sin gamma,t=s cos gamma+c sin gamma. The exact
result is

    (eta c+s-1)cos gamma+(1.35c-.85s-1)sin gamma.

The coefficients are less than .9 and at most .35, respectively.
Equation (8) therefore bounds this expression strictly below 1.
This contradicts (11) and a>1, including the aligned case delta=0.

## 5. E's longitudinal normal when q<=p

Put e0=-delta>=0. The exact upper C support is kA+e0H. Using
(1),(7) and L<=h-a, its excess over the lower E support is strictly
greater than

    F=1-.5d-t+k(1-1.086c)-.35e0(c+s)
      =1-Pd-Qt,                                    (12)

    P=.5-c+1.086c^2+.35s(c+s),
    Q=1-s+1.086cs-.35c(c+s).

The replacement of a by 1 has coefficient 1+k>0, so (12) remains
strict even when e0=0. With x=s/(1+c), direct rational substitution
gives the exact coefficient-norm identity

    1-P^2-Q^2=N(x)/[125000(1+x^2)^2],
    N(x)=-763737x^4+1016750x^3-126776x^2
                              -16750x+29263.       (13)

The complete canonical range has 0<=x<=sqrt(2)-1<5/12. Throughout
this interval,

    1016750-763737x>=2794105/4>0,

and therefore

    N(x)>=29263-126776(5/12)^2-16750(5/12)
          =2467/9>0.                              (14)

Thus P^2+Q^2<1, and Cauchy's inequality makes F>0. E's second angle
order is impossible as well.

Every actual normal in (6) has failed for both relative orders.
All coefficients of a in the strict replacements are positive:
1+k in (9),(10),(12), and 1+k+delta in (11). Axial and diagonal
canonical representatives, equality of angles and all exterior face
contacts were retained. Hence the alleged missing Y contradicts
disjointness, proving Theorem 1.

## 6. The predecessor faces in the original OOOO family

Retain the original all-four-ordinary, no-omission MPPM entrance.
Normalize a nonpositive ordinary predecessor to C=Q4 and translate by
(-2,-2). Its original strict points include

    M_C=(-.35,-.35), P0=(-1,-.26), G0=(-1,-.4).

Its actual left marker W=(-1.086,0) is foreign in Q8, and its actual
northwest marker N=(-.35,.35) is foreign in Q7. We verify (1) through
the exhaustive literal alternatives for the forward point T=(-.26,0).

If T is strict in C, its exclusion of W is lower u: W's upper-u
band follows from P0, its lower-v band from G0, and its upper-v
band from T. The three increments are .086c+.26s, .4c-.086s>0,
and .826s>=0. Thus U>=-1.086c.

At N the lower-u band follows from P0, the upper-u band from T,
and the lower-v band from T. Their increments are

    .65c-.61s>=.04c>0,
    .09c+.35s>0,
    .35c-.09s>=.26c>0.

Therefore N is upper v and H<=.35(c-s). This proves (1) in the
forward-owned case without assuming any other forward ownership.

If T is omitted from C, Lemma 1 of
C1092-MPPM-MISSING-NEGATIVE-WALL-ORDER.md gives

    U>=-1.086c, H<=-.26s<=.35(c-s).

Every literal input of that lemma is available in OOOO: C's missing
forward point gives its ordinary halfpoint; the actual paired Q0 and
left marker give its exclusions; and the ordinary Q5's G5 supplies the
actual Q9 far bar. That lemma does not require a preceding origin or
an owner for the omitted T. Thus (1) holds in this alternative too.

## 7. Every nonpositive central halfpoint and its actual wall origin

**Corollary 2.** In the whole original no-omission OOOO family, every
ordinary central square with nonpositive canonical angle strictly
owns its ordinary outer halfpoint and supplies the next actual wall
origin. There is no premise on any other central angle or on its
forward-point ownership.

Normalize the central square in question to E=Q5. If it omits F4,
the ordinary-marker halfpoint theorem already gives (2.5,1) in Q5.
Its exact strict anchors are the Q5 marker,G5,F6; its exclusions are
the genuine F4 omission, Q9 marker, Q1 inner corner and F8 in Q10.

Suppose instead F4 is strict in Q5. Then the strict points (2) are
exactly the Q5 marker,G5,F6,F4. Its actual predecessor Q4 is ordinary.
If that predecessor is nonpositive, Section 6 verifies Theorem 1,
which gives the same Q5 halfpoint.

If the predecessor is positive and omits G3, use the complete theorem
C1092-MPPM-POSITIVE-MISSING-NEGATIVE-H.md. Its actual source map
requires only this positive missing-forward predecessor and the
nonpositive forward-owned Q5, precisely the present alternative.

If the predecessor is positive and owns G3, Theorem 1 of
C1092-MIXED-NEGATIVE-H.md applies directly to the two actual ordinary
forward-owned squares Q4,Q5. Its only predecessor exclusions are
(1,1) in Q0, (.914,2) in Q8 and F1=(1,2.26) in Q8. All are strict
in their named actual original owners, regardless of the other two
central forward points. It again gives (2.5,1) strictly in Q5.

This exhausts the predecessor sign and actual forward membership.
The actual paired-corner transfer at Q1,Q10, with b=.914,ell=1.6,
then gives (3,2) strictly in Q10. Its foreign halfpoint is the point
just proved in Q5, its strict corner anchors are original in Q1,
and its boundary anchors are the Q10 marker and G8. Both real walls
are retained. Simultaneous quarter-turns prove the corollary for all
four sectors.

In particular every actual wall origin is available in an all-
nonpositive OOOO configuration, even when forward ownership is mixed.
The remaining mixed-forward cyclic contradiction is a separate
obligation; this halfpoint transfer does not assume its conclusion.

