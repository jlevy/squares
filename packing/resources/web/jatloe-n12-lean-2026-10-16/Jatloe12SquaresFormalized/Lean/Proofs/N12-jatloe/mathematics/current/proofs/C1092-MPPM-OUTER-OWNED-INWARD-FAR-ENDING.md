# C1092 MPPM: a missing-center inward owner retaining G0 forces an inward opposite

All terminating decimals are exact rationals. Owned points are strict in
their named actual open squares. An excluded point may touch a face, and
separating supports may be equal. All squares have the same side a>1.
No numerical search, upper side bound, or new owner for an omitted point
is used in this chapter.

## 1. A local two-square ending

**Theorem 1.** Let C,E be actual open squares with disjoint interiors.
Give C the negative canonical frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,
    0<=x:=s/(1+c)<=279/1000.

Write U,V for its lower faces and A=U+a,H=V+a for its upper faces.
Suppose that

    A>=a-c+.26s, H<=0,                              (1)

and C strictly owns

    M_C=(-.35,-.35), I=(0,-.26), X=(-.5,0).           (2)

Suppose E has a strictly negative canonical frame

    u_E=(d,-t), v_E=(t,d), d>=t>0, d^2+t^2=1,

strictly owns

    M=(.35,-.35), B0=(.26,-1), B=(.4,-1),
    Y_E=(.5,-1),                                    (3)

and excludes

    I, O_R=(1,0), K0=(1,-1), R0=(0,-1.086),
    O_B=(0,-1).                                     (4)

Finally suppose that the whole segment

    T={1} x [-.56,0]                                (5)

is disjoint from E. Then C and E cannot have disjoint interiors.

The application supplies (5) inside the one actual right-wall square.
The two physical origins in (4) have separate proved actual owners.

## 2. The bottom origin and the whole right bar force a steep successor

Write L,K for E's lower faces and J=L+a,D=K+a for its upper faces.
Theorem 1 of C1092-MPPM-NEGATIVE-SUCCESSOR-BAR-PROFILE.md applies to
(3)-(5), using the subsegment {1} x [-.4,0]. It gives the simultaneous
faces

    L>=.26t, J<=d+t, K>=-1.086d, D<=t-.4d.          (6)

At the additionally excluded O_B, both upper bands follow strictly
from B0: the projection increments are .26d and .26t. Its lower-u
alternative would give L>=t and therefore a<=d<=1, by (6). Thus
O_B must be lower v. We have the stronger actual face

    K>=-d, D>=a-d.                                  (7)

Let F=(1,-.56), the lower endpoint of (5). Its two lower bands follow
from M and B0, with positive increments .65d+.21t and .74t+.44d.
Thus F is upper u or upper v. Suppose it is upper u, J<=d+.56t.
Together with L>=.26t this gives

    1<a<=d+.30t,
    0<z:=t/(1+d)<3/10,                              (8)

using d+.30t-1=2z(.30-z)/(1+z^2).

The rightmost closure vertex Z=J u_E+D v_E has coordinates

    Z_x=dJ+tD, Z_y=-tJ+dD.

Use J>=a+.26t and D<=t from (6) to obtain

    Z_y<=t(d-a)-.26t^2<0.                           (9)

Using instead J<=d+.56t and (7) gives

    Z_y>=-t(d+.56t)+d(a-d)
         >-.56+d(1-t-.44d).                         (10)

The function sin q+.44cos q is strictly increasing throughout
0<=q<=pi/4, because its derivative is at least .56cos q>0.
At q=2 arctan(3/10) it is exactly 2501/2725<1. Thus (8) makes the
last term in (10) positive, proving -.56<Z_y<0.

The two lower bounds on J,D also give

    Z_x>=a(d+t)-.74dt>d+t-.74dt>1,                 (11)

because

    d+t-1=2dt/(1+d+t)>=.8dt>.74dt.

The factor .8 is valid on the whole canonical domain since
1+d+t<=1+sqrt(2)<5/2. Join the strict marker M=(.35,-.35) to Z.
Every point on that segment except possibly Z is strict in E. Its
crossing of x=1 occurs strictly before Z by (11), and its height is
strictly between -.56 and 0 by (9)-(10). It therefore lies on T and
strictly inside E, contrary to (5). No closure vertex was declared
strict in this argument.

Consequently F is upper v. With (7), this proves

    D<=t-.56d, 1<a<=t+.44d.                         (12)

The exact factorization

    t+.44d-1=-1.44(z-7/18)(z-1)/(1+z^2)

and 0<z<1 give

    z>7/18.                                         (13)

In particular the equality angle in (13) is excluded by a>1, not by
discarding a tangent face alternative.

## 3. Every actual separating normal is accounted for

Orient a separating normal from C toward E. The strict markers in
(2)-(3) force n_x>0. The strict pair X,Y_E further gives n_x>n_y.
Thus neither transverse normal v=(s,c) nor v_E=(t,d) can separate:
each has its vertical component at least its horizontal component.
Their opposite signs and the negative longitudinal normals have
nonpositive horizontal components. The complete actual face-normal
list left by the separating-axis theorem is exactly

    u, u_E.                                         (14)

Let p,q be the nonnegative magnitudes of the C,E angles. Equations
(1),(13) and 279/1000<7/18 give q>p. Put

    k=cd+st=cos(q-p)>0,
    delta=ct-sd=sin(q-p)>0,
    alpha=1-c+.26s.

The upper C support on u is A. Its lower E support on this direction
is kL+delta K. From (1),(6),(12), their difference is strictly greater
than

    F_C=alpha+k(1-d-t)+delta(1-t+.56d).              (15)

On u_E the exact upper C support is kA-delta V. Since H<=0 gives
V<=-a, subtracting L<=d+t-a gives a difference strictly greater than

    F_E=1-d-t+k alpha+delta.                         (16)

In both calculations the coefficient of a before replacing it by 1
is 1+k+delta>0. Therefore a positive scalar margin excludes a weak
separating-support equality as well.

## 4. The central normal has a positive margin on the whole angle interval

The exact expansion of (15) is

    F_C=1-c P(q)-s Q(q),
    P(q)=2-d-t+.44dt,
    Q(q)=d-t+.30+.44t^2.                             (17)

Both coefficient functions are nonincreasing for 0<=q<=pi/4. Indeed

    P'(q)=-(d-t)[1-.44(d+t)]<=0,
    Q'(q)=-(d+t)+.88dt<0,                            (18)

where d+t<=sqrt(2)<3/2 and dt<=1/2 justify the signs. At
q0=2 arctan(7/18), the exact coordinates and coefficients are

    d0=275/373, t0=252/373,
    P(q0)=112179/139129<.81,
    Q(q0)=3912973/6956450<.57.

Because q>q0 and c,s>=0, (17)-(18) and Cauchy's inequality give

    F_C>1-.81c-.57s
         >=1-sqrt(.81^2+.57^2)
         =1-sqrt(.981)>0.                           (19)

This bound covers every C angle in the local statement and the full
successor interval through the diagonal endpoint.

## 5. The successor normal has a positive continuous margin

Rewrite (16) exactly as

    F_E=1-A_p d-B_p t,
    A_p=1+s-c alpha, B_p=1-c-s alpha.               (20)

The half-angle bound x<=279/1000 implies c>.85 and 0<=s<.52.
For example the extremal rational values are

    c>=922159/1077841>.85,
    s<=558000/1077841<.52.

Consequently 0<=alpha<.15+.26(.52)<.29, so

    A_p>.71, B_p<.15.

For q>=q0 one has t/d>=252/275>.9. Differentiating (20) gives

    partial F_E/partial q=A_p t-B_p d
       >[.71(.9)-.15]d=.489d>0.                    (21)

It remains to check the complete C interval at q=q0. Direct rational
half-angle substitution gives the exact identity

    F_E(q0)=N(x)/[9325(1+x^2)^2],
    N(x)=2450-10175x+12602x^2+7875x^3-23900x^4.     (22)

This numerator is decreasing throughout 0<=x<=279/1000, because

    N'(x)=-10175+25204x+23625x^2-95600x^3
       <=-10175+25204(.279)+23625(.279)^2
       =-10432723/8000<0.

At the endpoint its exact value is

    N(279/1000)=6183383005091/10000000000>600.        (23)

Also 1+x^2<27/25, whence

    9325(1+x^2)^2<9325(27/25)^2=271917/25<11000.

Equations (21)-(23) prove the uniform margin

    F_E>3/55>0.                                     (24)

Both actual sources in (14) have failed. This proves Theorem 1,
including the closed C bound, the diagonal E endpoint and all weak
face or separating contacts.

## 6. The exact original outer-owned inward consequence

Retain the complete original no-omission MPPM entrance. Normalize a
nonordinary inward owner to Q4, and suppose it owns G0 and omits F0
and the physical center (2,2). Translate every actual owner and point
by (-2,-2), and set C=Q4,E=Q5.

C1092-MPPM-INWARD-OUTER-OWNED-ANGLE.md, Theorem 1 and Corollary 2,
give the strictly negative frame, the faces (1), and

    0<x<1-sqrt(13)/5<279/1000,
    (1,1.5) strict in Q4,
    (2,1) strict in actual Q9.                      (25)

The strict marker and I in (2) are Q4's marker and F4. Its strict
X=(1.5,2) and the actual ordinary pair F6,G5 in Q5 follow from
C1092-MPPM-NO-OMISSION-REDUCTION.md, Section 1. The all-angle ordinary
halfpoint theorem gives Y_E=(2.5,1) in this same Q5. Its complete
map uses the Q5 marker,G5,F6 as strict anchors and F4 in Q4, the Q9
marker, the Q1 inner corner and F8 in Q10 as exclusions.

C1092-MPPM-NEGATIVE-INWARD-SUCCESSOR-SIGN.md, Section 6.2, then
proves the actual E negative without imposing center ownership on C.
The halfpoint and actual paired-corner transfer in
C1092-DIRECT-WALL-POINT.md, Theorem 7, applied to Q1,Q10 with
b=.914 and ell=1.6, give O_R=(3,2) strictly in Q10. The point O_B
in (4) is the strict Q9 origin already supplied in (25). The two
other exclusions K0,R0 are the actual Q1 inner corner and Q9 marker.
Thus all points in (2)-(4) have their literal actual sources.

Suppose now that the opposite Q6 is ordinary, so it owns F9,G9.
The ordinary-central reduction excludes G6 from the actual Q10.
The ordinary wall-reach map of
C1092-MPPM-NONORDINARY-ISOLATION.md, in coordinates
(xi,eta)=(4-x,4-y), uses the actual Q10 marker and G8 as strict
anchors and F9 in Q6 and the genuine Q10 omission of G6 as exclusions.
Its standard target (1,2.56) becomes (3,1.44), strictly in Q10.
Together with the strict Q10 origin (3,2), this gives the whole
closed segment [(3,1.44),(3,2)] strictly in the one actual Q10.
It is exactly (5) after translation and is disjoint from Q5.

Theorem 1 now gives a contradiction. Therefore the opposite Q6
cannot be ordinary. The completed no-omission reduction and elbow
exclusion leave only an inward opposite Q6. Simultaneous quarter-turns
give the same conclusion for every sector.

**Corollary 2.** Every no-omission inward owner that omits the physical
center has an inward opposite owner. This chapter proves the
G0-owned/F0-omitted alternative. The complementary G0-omitted
alternative for each angle sign is proved in
C1092-MPPM-SMALL-INWARD-SUCCESSOR.md and
C1092-MPPM-POSITIVE-MISSING-INWARD-FAR-ENDING.md.

In particular the lone inward owner in an OOOI pattern must own the
center. The completed nonnegative center-owned ending then forces its
angle to be strictly negative. The center-owned negative OOOI ending
and the remaining OIOI alternatives are separate obligations; this
chapter does not claim to close them.
