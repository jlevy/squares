# C1092 MPPM: a center-owned inward square retaining G0 forces an inward opposite

Every terminating decimal is an exact rational. Owned points are strict
in their named actual open squares. Exterior faces and separating
supports may be equal. All squares have the same side a>1. This chapter
uses no upper side bound, numerical angle sampling, or new owner for an
omitted auxiliary.

## 1. The local two-square theorem

**Theorem 1.** Give an actual square C the negative canonical frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,
    0<=x:=s/(1+c)<=21/100.

Write U,V for its lower faces and A=U+a,H=V+a for its upper faces.
Suppose that C strictly owns

    M_C=(-.35,-.35), I=(0,-.26), X=(-.5,0),          (1)

and satisfies

    A>=a-c+.26s, H<=17/125.                         (2)

Let E have the strictly negative canonical frame

    e=(d,-t), f=(t,d), d>=t>0, d^2+t^2=1,

and strictly own

    M_E=(.35,-.35), B0=(.26,-1), B=(.4,-1),
    Y=(.5,-1).                                      (3)

Suppose E excludes

    I, O_R=(1,0), K0=(1,-1), R0=(0,-1.086),
    O_B=(0,-1),                                     (4)

and is disjoint from the whole segment

    T={1} x [-.56,0].                               (5)

Then C and E cannot have disjoint interiors.

This is the center-owned extension of the local ending in
C1092-MPPM-OUTER-OWNED-INWARD-FAR-ENDING.md. The upper face H is now
permitted to be positive. Its smaller complete angle range supplies
the new positive margin needed for the successor's own normal.

## 2. The actual bar and complete normal list

Write L,K for E's lower faces and J=L+a,D=K+a for its upper faces.
The complete point-and-bar argument in Sections 2-3 of
C1092-MPPM-OUTER-OWNED-INWARD-FAR-ENDING.md uses only (3)-(5) to give

    L>=.26t, J<=d+t, K>=-d, D<=t-.56d,
    z:=t/(1+d)>7/18.                               (6)

In that argument the genuine bottom origin first strengthens the
lower transverse face from -1.086d to -d. If the lower endpoint of
T were upper e, the rightmost closure vertex would have height
strictly between -.56 and 0 and abscissa strictly above 1. Its segment
to the strict marker would cross T strictly inside E. Thus the
endpoint is upper f, and the width inequality a<=t+.44d gives the
strict half-angle bound in (6). None of these steps uses either C's
upper face H or center ownership. They therefore apply unchanged.

Orient a separating normal from C to E. The strict marker pair in
(1),(3) forces n_x>0, and the strict pair X,Y forces n_x>n_y.
The transverse directions v,f have vertical component at least their
horizontal component; their negatives and the negative longitudinal
directions have nonpositive horizontal component. Thus the complete
actual face-normal list left by the separating-axis theorem is

    u, e.                                           (7)

Let p,q be the nonnegative magnitudes of the C,E angles. Since
x<=21/100<7/18<z, we have q>p. Put

    k=cd+st>0, delta=ct-sd>0,
    alpha=1-c+.26s, eta=17/125.

On u the exact support difference upper_C(u)-lower_E(u) is
A-kL-delta K. Use (2), L<=d+t-a and K<=t-.56d-a from (6).
Its lower bound, after replacing a by 1 strictly, is

    F_C=alpha+k(1-d-t)+delta(1-t+.56d).              (8)

On e the exact upper C support is kA-delta V. Since V=H-a<=eta-a,
its difference from L<=d+t-a is strictly greater than

    F_E=1-d-t+k alpha+(1-eta)delta.                 (9)

In both replacements the coefficient of a is 1+k+delta>0. Thus a
positive scalar bound excludes even equality of separating supports.

## 3. The central normal on the full angle interval

The identity and derivative calculation in Section 4 of
C1092-MPPM-OUTER-OWNED-INWARD-FAR-ENDING.md apply to (8) without change:

    F_C=1-cP(q)-sQ(q),
    P=2-d-t+.44dt, Q=d-t+.30+.44t^2,
    P'=-(d-t)[1-.44(d+t)]<=0,
    Q'=-(d+t)+.88dt<0.

At q0=2 arctan(7/18), d0=275/373,t0=252/373, and

    P(q0)=112179/139129<.81,
    Q(q0)=3912973/6956450<.57.

Consequently, on the whole q>=q0 interval,

    F_C>1-.81c-.57s>=1-sqrt(.981)>0.                (10)

The smaller C range in Theorem 1 is included in that full calculation.

## 4. The successor normal with a positive upper-face cap

Expand (9) exactly as

    F_E=1-A_p d-B_p t,
    A_p=1-c alpha+(1-eta)s,
    B_p=1-s alpha-(1-eta)c.                         (11)

The full closed half-angle interval x<=21/100 gives

    c>=9559/10441>.91,
    0<=s<=4200/10441<.41,
    0<=alpha<.09+.26(.41)<.2.

It follows that A_p>.8 and

    B_p<1-.864(.91)=.21376<.214.

On q>=q0 we have t/d>=252/275>.9. Differentiate (11), holding p fixed:

    partial F_E/partial q=A_p t-B_p d
       >[.8(.9)-.214]d=.506d>0.                   (12)

Thus the whole successor interval is bounded by its lower endpoint.
Direct rational half-angle substitution there gives the exact identity

    F_E(q0)=N(x)/[46625(1+x^2)^2],
    N(x)=7966-41525x+63010x^2+48725x^3-115216x^4.   (13)

This numerator is strictly decreasing throughout 0<=x<=21/100:

    N'(x)=-41525+126020x+146175x^2-460864x^3
       <=-41525+126020(.21)+146175(.21)^2
       =-3445793/400<0.

Its exact endpoint value is

    N(21/100)=56291499901/25000000>2200.             (14)

Also 1+x^2<21/20 throughout that closed interval, so

    46625(1+x^2)^2<46625(21/20)^2
       =822465/16<52000.

Equations (12)-(14) prove the uniform bound

    F_E>11/260>0.                                  (15)

Both actual sources (7) are impossible. The complete closed C interval,
the diagonal E endpoint and all exterior face contacts are included.
This proves Theorem 1.

## 5. Literal original center-owned application

Retain the original no-omission MPPM entrance and normalize a genuinely
nonordinary inward owner to Q4. Suppose Q4 owns the physical center
(2,2) and its outer G0. Its angle is strictly negative by the completed
centered nonnegative ending. The two actual centered negative theorems

    C1092-MPPM-CENTERED-NEGATIVE-INWARD-H-CAP.md,
    C1092-MPPM-CENTERED-NEGATIVE-INWARD-ANGLE.md

give H<17/125, x<21/100, genuine omission of F0, the strict point
(1,1.5) in Q4, and the strict bottom origin (2,1) in actual Q9.
The lower face A>=a-c+.26s is also established in the cap chapter,
Section 1. Equivalently it follows directly from the three strict
bands of the omitted F0: its upper u-band follows from the Q4 marker,
its lower v-band from owned G0, and its upper v-band from owned F4.

Translate all actual points and owners by (-2,-2), and set C=Q4,E=Q5.
The inward-neighbor reduction supplies strict (1.5,2) in Q4 and the
ordinary pair F6,G5 in Q5. The all-angle ordinary halfpoint theorem
supplies strict (2.5,1) in that same Q5. Its strict anchors are the
Q5 marker,G5,F6; its actual exclusions are F4 in Q4, the Q9 marker,
the Q1 inner corner, and F8 in Q10. These are exactly (1),(3).

The universal negative-inward successor-sign theorem makes E strictly
negative, and the actual paired-corner transfer at Q1,Q10 gives the
strict right origin (3,2) in Q10. Thus the exclusions (4) have the
following literal sources:

| Local point | Original point | Actual strict owner |
|---|---|---|
| I | F4=(2,1.74) | Q4 |
| O_R | (3,2) | Q10, transferred from the Q5 halfpoint |
| K0 | (3,1) | Q1 |
| R0 | (2,.914) | Q9 |
| O_B | (2,1) | Q9, from the centered negative angle corollary |

Suppose now that the opposite Q6 is ordinary, so it owns F9,G9.
The ordinary-central reduction excludes G6 from actual Q10, and the
ordinary wall-reach theorem gives (3,1.44) strictly in that same Q10.
Its exact map is the one in Section 6 of
C1092-MPPM-OUTER-OWNED-INWARD-FAR-ENDING.md: the strict anchors are
the Q10 marker and G8, and the exclusions are F9 in Q6 and the proved
G6 omission from Q10. Together with the actual Q10 origin (3,2), this
gives the whole strict segment [(3,1.44),(3,2)] in Q10. Its translate
is precisely (5), disjoint from the different actual E.

Every hypothesis of Theorem 1 is now supplied by a proved actual owner
or a genuine omission. Its contradiction excludes ordinary Q6.

**Corollary 2.** A no-omission genuinely inward owner that contains the
physical center and owns its outer G point has an inward opposite.
Simultaneous quarter-turns preserve this literal conclusion. In
particular the sole inward owner in OOOI must omit both of its outer
F,G points. This chapter does not assign either omitted point a new
owner or claim the remaining both-outer-omitted ending.
