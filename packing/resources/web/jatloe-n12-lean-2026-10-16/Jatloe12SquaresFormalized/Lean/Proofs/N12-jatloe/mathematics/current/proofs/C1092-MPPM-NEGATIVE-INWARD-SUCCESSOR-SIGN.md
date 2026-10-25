# C1092 MPPM: a negative inward square forces its ordinary successor negative

Every terminating decimal in this chapter is an exact rational. All owned
points are strict, while an excluded point may lie on a face and a separating
support inequality may be an equality. The common side is a>1. No side upper
bound, sampled orientation, numerical feasibility conclusion or unproved
ownership of the physical center is used.

## 1. A local theorem that permits either center status

**Theorem 1.** Let C,E be two actual open squares of common side a>1 with
disjoint interiors. Suppose C has the canonical frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,

and write U,V for its lower faces and A=U+a,H=V+a for its upper faces.
Suppose that

    A>=a-c+.26s, H<=.35(c-s),                         (1)

and C strictly owns

    M_C=(-.35,-.35), I=(0,-.26), X=(-.5,0).            (2)

Suppose E strictly owns

    M=(.35,-.35), B0=(.26,-1), B=(.4,-1),
    Y_E=(.5,-1),                                      (3)

and excludes

    I=(0,-.26), G=(1,-.4), R0=(0,-1.086),
    K0=(1,-1), K1=(1,-1.086).                         (4)

Then E has a strictly negative canonical orientation. The hypotheses do
not require O=(0,0) either to belong to C or to be excluded from it.
In the application, K0 and K1 are two genuine points of the same paired
corner, and R0 is the genuine bottom marker. Neither is a surrogate wall
constraint.

## 2. The three forced faces of a putative nonnegative E

Suppose E has frame

    u_E=(d,t), v_E=(-t,d), d>=t>=0, d^2+t^2=1.

Let L,W be its lower faces and J_E=L+a,K_E=W+a its upper faces. We prove

    J_E<=d-.4t, K_E<=-.26d, W>=-d-t.                 (5)

At G, its lower u-band follows from M, its lower v-band from B, and its
upper v-band from M. The respective increments are

    .65d-.05t>=.60d>0, .6(d-t)>=0, .65t+.05d>0.

Therefore G is upper u, giving the first cap in (5). At I, its upper
u-band follows from M, and its lower v-band follows from B. If I were
lower u, the two u-faces would imply a<=d-.14t<=1. Hence I is upper v,
which proves the second cap in (5).

At K0, the lower u-band follows from B and the upper v-band from M.
Thus K0 is lower v or upper u. Suppose it is upper u, so J_E<=d-t.
The point R0 has both upper bands from B0,M. Its lower-v alternative
would give a<=.826d<1, by the second cap of (5). Consequently R0 is
lower u and L>=-1.086t. The two u-faces now give

    1<a<=d+.086t.                                    (6)

In particular t>0. With w=t/(1+d), the exact identity

    d+.086t-1=2w(.086-w)/(1+w^2)

gives w<.086 and therefore t<.172.

Now use the actual lower corner marker K1. Its lower u-band follows
from B, with increment .6d-.086t>=.514d>0. Its upper v-band follows
from M, with increment .736d+.65t>0. Thus K1 is lower v or upper u.
If it were lower v, its opposite cap at I would give

    a<=.826d+t<.826+.172=.998<1.

Therefore K1 is upper u and J_E<=d-1.086t. Combined with L>=-1.086t,
this gives a<=d<=1, a contradiction. The upper-u alternative of K0
is impossible. It must be lower v, completing (5).

We shall use both the upper longitudinal cap and the consequence of the
actual lower transverse face:

    L<=d-.4t-a, K_E>=a-d-t.                         (7)

All rejected alternatives above were weak excluded-face alternatives.
An increment equal to zero still gives a strict band because the anchor
belongs to the open square. Thus all canonical endpoints are included.

## 3. The complete actual C-to-E normal cone

Orient a separating normal n from C toward E. The two strict markers
give n_x>0. Comparing strict X in C with strict Y_E in E gives

    n_x-n_y>0.                                       (8)

Thus C's transverse normal v=(s,c) cannot separate. Its two oppositely
signed normals have nonpositive horizontal component. The complete
signed face-normal list left by the separating-axis theorem is

    u, u_E, -v_E.                                    (9)

The source u_E is already impossible. Indeed strict I in C gives

    upper_C(u_E)>u_E(I)=-.26t,

whereas (7) and a>1 give

    lower_E(u_E)=L<-.4t<=-.26t.

This argument uses the actual I and does not use a center-ownership
premise. We treat the two remaining sources over the full angle domain.

Set

    k=cd-st=cos(p+q)>=0,
    j=ct+sd=sin(p+q)>=0,

where p,q are the nonnegative canonical angle magnitudes. In particular
1+k+j>0, including both canonical endpoint representatives.

## 4. C's own normal is impossible on the entire domain

On n=u, the exact lower E support is kL-jK_E. Use (1),(7). Its deficit
from C's upper support A is at least

    a(1+k+j)-c+.26s-k(d-.4t)-j(d+t),

and is therefore strictly greater than

    F=1-c+.26s+k(1-d+.4t)+j(1-d-t)
      =1-B_q c+A_q s,                               (10)

where the exact coefficients are

    B_q=2-d-t+.6dt,
    A_q=.26+d-t-1+.6t^2.                            (11)

We prove F>0 without restricting p. Let w=t/(1+d), so
0<=w<=sqrt(2)-1<5/12.

First suppose 0<=w<=1/10. Then t<=1/5 and d> .98, so A_q>.04>0.
Also

    d+t-1=2dt/(1+d+t)>=.8dt,
    0<B_q<=1-.2dt<=1.                              (12)

If t>0, (10) gives F>=1-B_q>0. If t=0, the face chain in Section 2
already contradicts a>1: the lower v-face W>=-1 and upper v-face
K_E<=-.26 would give a<=.74. Thus this endpoint supplies no exception.

Now suppose 1/10<=w<=sqrt(2)-1. Direct expansion gives the exact
positive-denominator identity

    1-B_q^2-A_q^2
      =-P(w)/[2500(1+w^2)^2],                       (13)

    P(w)=27569w^4-30600w^3+22458w^2-6600w+169.

The second derivative

    P''(w)=330828w^2-183600w+44916

is strictly positive for every real w: its leading coefficient is
positive and its discriminant is -25728921792<0. Hence P is strictly
convex. Its two exact endpoint values on the larger closed interval
[1/10,5/12] are

    P(1/10)=-2942631/10000,
    P(5/12)=-1340191/20736.

Convexity puts every intermediate value below the line joining these
two negative values. Thus P(w)<0 on this whole interval. By (13),
B_q^2+A_q^2<1. Cauchy's inequality in (10) now gives

    B_q c-A_q s<=sqrt(B_q^2+A_q^2)<1,

so F>0. The strict a coefficient preceding (10) excludes weak support
equality as well. C's source cannot separate for any canonical angle.

## 5. E's downward normal is impossible on the entire domain

On n=-v_E=(t,-d), the exact upper C support is jA+k(a-H). The lower
E support is -K_E<=d+t-a. Substituting (1) gives a deficit strictly
greater than

    G=1-d-t+j(1-c+.26s)+k[1-.35(c-s)]
      =1-P_p d-Q_p t,                               (14)

again because the coefficient of a before dropping a to 1 is 1+j+k>0.
Here

    P_p=.35c^2+.65cs-c-.26s^2-s+1,
    Q_p=c^2-.61cs-c+.35s^2+s+1.                    (15)

The two elementary identities

    Q_p-P_p=(c-s)(.65c-.61s)+2s>=0,
    Q_p=(1-c)+c^2+.35s^2+s(1-.61c)>0               (16)

show that P_p cos q+Q_p sin q is nondecreasing throughout
0<=q<=pi/4. If P_p>=0 this follows from Q_p>=P_p and cos q>=sin q;
if P_p<0 it follows directly from Q_p>0. Its maximum is consequently
(P_p+Q_p)/sqrt(2).

The exact sum is

    P_p+Q_p=1.35+2(1-c)-1.26s^2+.04cs.             (17)

Since c>=1/sqrt(2)>.7, one has 2/(1+c)<20/17<1.26. Using
1-c=s^2/(1+c) and cs<=1/2 in (17) gives

    P_p+Q_p<=1.37<sqrt(2).

Thus G>=1-1.37/sqrt(2)>0. This excludes E's downward source, including
the diagonal endpoint. Every source in (9) has failed, contrary to
disjointness. This proves Theorem 1.

## 6. Literal applications to the original inward owner

Retain the complete original no-omission MPPM entrance and normalize a
nonordinary inward owner as C=Q4. Translate by (-2,-2). Its strict
M_C,I are its actual marker,F4, and the strict X is the crosspoint
(1.5,2) proved in C1092-MPPM-NO-OMISSION-REDUCTION.md, Section 1.
The same theorem forces the one actual ordinary successor E=Q5 to own
F6,G5, which are B,B0 in (3).

The strict halfpoint Y_E=(2.5,1) follows from
ORDINARY-MARKER-HALFPOINT.md under (xi,eta)->(2-eta,2-xi), with d=.086.
Its strict anchors are E's marker,G5,F6. Its four exclusions are F4 in
C, the Q9 bottom marker, the actual Q1 inner corner, and F8 in actual
Q10. Thus every hypothesis in (3) is actual. The excluded G is G8 in
Q10; R0 is the actual Q9 marker; K0,K1 are the actual Q1 inner corner
and its marker (3,.914). No unproved point of the corner is used.

There are two particularly useful ways to supply (1).

### 6.1. The center belongs to the negative inward owner

Suppose O=(2,2) is strict in Q4 and use its nonpositive canonical frame.
Strict O gives U,V<0<A,H. At the foreign SE marker (.35,-.35), the
lower u-band and upper v-band follow from O, and the lower v-band
follows from M_C with increment .7s>=0. Thus this marker is upper u.
At the foreign NW marker (-.35,.35), its upper u-band and lower
v-band follow from O. Its lower-u alternative would oppose the
already forced upper-u face and give a<=.7(c+s)<=.7sqrt(2)<1.
Therefore the NW marker is upper v. Explicitly,

    0<A<=.35(c+s), 0<H<=.35(c-s).                  (18)

This verifies the upper bound in (1), including every face equality.

If G0=(-1,-.4) is omitted, both of its upper bands follow from M_C.
Its lower-v exit would oppose H<=.35(c-s) and give

    a<=.75c+.65s<=sqrt(.985)<1.

Consequently it is lower u, U>=-c+.4s, which is stronger than (1).
If G0 is owned, nonordinariness means F0=(-1,-.26) is omitted. At F0
its upper u-band follows from M_C, its lower v-band from G0, and its
upper v-band from I. Their increments are .65c+.09s, .14c, and s,
respectively. Therefore F0 is lower u and U>=-c+.26s. This supplies
(1) in the second actual alternative as well. Theorem 1 proves that
the actual ordinary Q5 is strictly negative in either alternative.

### 6.2. The center is missing from the negative inward owner

Theorem 1 of C1092-MPPM-INWARD-OUTER-OWNED-ANGLE.md supplies (1) when
Q4 owns G0 and omits F0,O: it gives U>=-c+.26s and H<=0, and
0<=.35(c-s). Its center-omission angle bound is not needed here.

For the G0-omitted negative inward profile,
C1092-MPPM-INWARD-BOTTOM-ANGLE.md supplies U>=-c+.4s and H<=0,
again stronger than (1). The other strict points and actual E data
have exactly the same sources as above. Thus the present theorem
applies literally to both missing-center profiles too, without
borrowing a strict O, a second halfpoint in C or an ownership of
the omitted outer auxiliary.

This chapter proves the successor sign. It does not claim that all
center-owned negative inward configurations or the remaining opposite
inward configurations have already been excluded.
