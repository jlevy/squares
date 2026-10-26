# C1092 MPPM: a negative missing-forward predecessor cannot precede a positive forward owner

Every terminating decimal is exact. Owned points are strict interior
points of their actual open squares; exclusions may be weak face exits.
All local squares have one common side a>1. The original application
retains the no-omission OOOO entrance with 1<a<=1.001.

The proof uses a missing actual boundary origin in two ways. Its positive
predecessor forces a shallow boundary angle, by the preceding chapter.
A negative successor strictly owning that origin forces the opposite
angle inequality. Both conclusions concern the same actual boundary.

## 1. A negative recipient of an origin forces a steep boundary

Use coordinates centered at (2,2). Let E,B be actual open squares of
side a>1 with disjoint interiors. The southeast square E has negative
canonical frame and actual faces

    e=(d,-t), f=(t,d), d>=t>0, d^2+t^2=1,
    L_E<e dot Z<J_E=L_E+a,
    K_E<f dot Z<Q_E=K_E+a.

Suppose E strictly owns P=(0,-1), and its simultaneous actual faces
and angle satisfy

    L_E>=.26t, Q_E<=t-.56d,
    .7<d<.825, .566<t<.71, d+t>1.39.             (1)

The actual bottom square B has negative canonical frame

    w=(b,-r), z=(r,b), b>=r>0, b^2+r^2=1,
    L<w dot Z<J=L+a, K<z dot Z<D=K+a,

strictly owns

    M_B=(0,-1.086), A_B=(-.26,-1),

excludes the actual corner point S=(-1,-1.086), and has its entire
closure in y>=-2. Disjointness from E excludes P from B.

**Theorem 1.** These conditions imply

    r/b>1/4.                                     (2)

No condition on a predecessor, either center, or another wall origin
is a premise of this local statement.

## 2. The actual faces and two normal sources

Exactly as in Section 2 of
C1092-MPPM-MISSING-BOUNDARY-SHALLOW-ANGLE.md, the three strict bands
at the missing P force D<=-b. At the foreign S both upper bands are
strict by M_B. A lower-z exit would give a<=r+.086b<1, so S is lower
w. Retain the resulting simultaneous faces and real floor:

    D<=-b, J>=a-b+1.086r,
    rJ-bD<=2-ab,
    D>=a-2/b+(r/b)J.                              (3)

Suppose, for contradiction, that r/b<=1/4. Write beta for the positive
magnitude of B's negative angle. Then

    0<beta<=atan(1/4), b>=4/sqrt(17)>.97,
    0<r<=1/sqrt(17)<.25,
    0<eta=r/(1+b)<=sqrt(17)-4<1/8.                (4)

Write q for E's negative-angle magnitude. From (1),

    v0=t/d>.566/.825=566/825>2/3,
    v0<=1.

In particular q>beta. Define

    k=db+tr=cos(q-beta)>0,
    delta=tb-dr=sin(q-beta)>0.                    (5)

Orient a possible separating normal n from B toward E. The two strict
pairs A_B,P and M_B,P give, respectively, n_x>0 and n_y>0. The
complete signed face-normal list of these two negative canonical
squares therefore leaves only

    f=(t,d), z=(r,b).                             (6)

Their exact decompositions are

    z=-delta e+k f,
    f=delta w+k z.                                (7)

Thus every supporting vertex in the following proof is fixed by its
actual signed coefficient. No other angle-order case is omitted under
the hypothetical slope bound (4).

## 3. B's northeast normal cannot separate

The faces (1) imply J_E>=a+.26t and K_E<=t-.56d-a. Consequently

    lower_E(z)=-delta J_E+kK_E
       <=-a(k+delta)-.26delta t+k(t-.56d).

The strict B marker gives upper_B(z)=D>-1.086b. Its support excess
is therefore strictly greater than

    a(k+delta)-1.086b+.26delta t-k(t-.56d).

The a coefficient k+delta is positive. At a=1 the exact remaining
scalar expands to

    b P0+r Q0,
    P0=d+t-.526-dt-.30t^2,
    Q0=t-d-t^2+.30dt.                             (8)

The full continuous angle bounds (1), together with dt<=1/2 and
t^2<=1/2, give

    P0>1.39-.526-.5-.15=.214.

Because t-t^2 decreases for t>1/2,

    Q0=(t-t^2)-d(1-.30t)
       >(.71-.71^2)-.825(1-.30(.566))
        =-.479015>-.48.

Using r/b<=1/4, (8) is consequently greater than

    b[.214-.48/4]=.094b>0.                       (9)

Thus upper_B(z)>lower_E(z), excluding this actual source.

## 4. E's northeast normal cannot separate

The actual upper B support is delta J+kD. Use the final wall inequality
in (3), then its lower J face. The coefficient identity
delta+kr/b=t/b gives

    upper_B(f)>=k(a-2/b)+(t/b)J
       >=a(k+t/b)-2k/b-t+1.086tr/b.               (10)

E strictly owns P, so its actual lower f face satisfies

    lower_E(f)=K_E<-d.                            (11)

The support excess in (10),(11) is strictly greater, after decreasing
a to 1 in the positive coefficient k+t/b, than

    G=k+t/b-2k/b-t+1.086tr/b+d
      =-d(1-b)+(t/b)[1-b+br-.914r]
      =(dr/b)g(beta,v0),                          (12)

where eta is as in (4) and

    g(beta,v0)=v0(b-.914)+eta(v0-b).               (13)

The remaining scalar is strictly positive on the complete closed
rectangle

    0<=beta<=atan(1/4), 2/3<=v0<=1.

First, it increases with v0 because b-.914+eta>0 by (4). For fixed
v0, its beta derivative is exactly

    g_beta=(v0-b)/(1+b)+r(eta-v0).                (14)

The coefficient of v0 in (14) is 1/(1+b)-r>1/2-1/4>0. Thus (14)
is at most its value at v0=1:

    g_beta<=eta^2+r(eta-1)
            <=eta^2+eta(eta-1)
             =eta(2eta-1)<0                      (15)

for beta>0. The second inequality uses r>=eta and eta-1<0. At beta=0
the derivative is nonpositive and the same endpoint monotonicity holds.

Consequently the minimum of (13) on the entire rectangle occurs at
v0=2/3 and beta=atan(1/4). Its exact value is

    g(atan(1/4),2/3)=30/sqrt(17)-1819/250>0.      (16)

There is a small but strictly positive exact reserve:

    7500^2-17(1819)^2=1063>0.                     (17)

All quantities compared in taking squares are positive. Equations
(12)--(17), with dr/b>0, prove upper_B(f)>lower_E(f). This excludes
the second and last actual source in (6), contradicting disjointness.
The supposed r/b<=1/4 is therefore impossible, proving Theorem 1.
Both the quarter-slope endpoint and all weak face or wall contacts
were retained. ∎

## 5. The literal actual negative-recipient profile

The profile (1) is a direct quarter-turn of Lemma 1 of
C1092-MPPM-MISSING-NEGATIVE-WALL-ORDER.md. We record the map so that
ownership of P is not confused with the exclusion used in a different
stronger negative profile.

In that lemma's southwest coordinates (xi,eta), use

    (x,y)=(-eta,xi).

Its negative frame (d,-t),(t,d) becomes f,-e. Hence its three faces

    U>=-1.086d, J<=t-.56d, K<=-.26t

become, respectively,

    K_E>=-1.086d, Q_E<=t-.56d, L_E>=.26t.          (18)

The first bound is retained here only for the source record. Theorem 1
used the last two. The lemma's half-angle bound is

    t/(1+d)>237/763.

The exact endpoint has d0=263000/319169 and t0=180831/319169. The
lemma's displayed consequences give .7<d<.825 and .566<t<.71. Since
cos q+sin q increases for 0<=q<=pi/4, they also give

    d+t>(263000+180831)/319169>1.39.              (19)

The lemma does not require exclusion of the preceding origin. Thus
the extra strict P used in Theorem 1 is fully compatible with all
premises of (18); no stronger profile requiring P's exclusion has
been imported.

## 6. The negative-missing to positive-owned edge is impossible

**Corollary 2.** In the original no-omission OOOO family, an ordinary
central with negative angle that omits its forward point cannot be
immediately followed by a positive ordinary central that owns its
forward point.

**Proof.** Simultaneously rotate the entire actual owner table so that
the alleged edge is Q7 followed by Q4. Thus actual Q7 is negative and
omits F5=(2,2.26), while actual Q4 is positive and owns G3=(1.74,2).
Corollary 3 of
C1092-MPPM-NEGATIVE-MISSING-POSITIVE-SHARED-WALL.md then gives the
strict actual ownership

    (2,3) belongs to Q7.                           (20)

In particular the different actual boundary Q11 omits its local
origin (2,3). Corollary 2 of
C1092-MPPM-MISSING-BOUNDARY-SHALLOW-ANGLE.md applies to that same
boundary and proves that its canonical angle is negative with

    tan(beta_Q11)<1/4.                            (21)

For the opposite inequality in Theorem 1, use the half-turn chart

    (x,y)=(2-X,2-Y)

on the original container coordinates (X,Y). The actual squares in
Theorem 1 are E=Q7 and B=Q11. All its strict points, omitted points,
profile inputs and walls have the following literal sources:

| Local datum | Original actual source |
|---|---|
| E marker (.35,-.35) | Q7 marker (1.65,2.35) |
| E ordinary points (.26,-1),(.4,-1) | G4=(1.74,3), F3=(1.6,3), strict in Q7 |
| E outer halfpoint (.5,-1) | (1.5,3), strict in Q7 from its F5 omission |
| E exclusion of forward (0,-.26) | F5 omitted from Q7, with no new owner assigned |
| E exclusion of corner (1,-1) | (1,3), strict in actual Q3 |
| E exclusion of wall marker (0,-1.086) | Actual Q11 marker (2,3.086) |
| E excluded whole {1} x [-.56,-.26] | One actual Q8 bar from F1=(1,2.26) to its strict advance (1,2.56) |
| E strict P=(0,-1) | The actual Q7 ownership (20) |
| B strict M_B=(0,-1.086), A_B=(-.26,-1) | Q11 marker and G7=(2.26,3) |
| B excluded S=(-1,-1.086) | (3,3.086), strict in actual Q2 |
| Entire real B floor y>=-2 | Original Q11 top wall Y<=4 |

The entire Q8 bar has one actual owner: its original F1 and its
ordinary wall advance (1,2.56) are both strict in Q8, and convexity
supplies their full segment. That advance is unconditional in OOOO
and uses the actual Q4 ordinary point F0. It does not require a Q8
origin.

The first seven rows supply exactly the local negative missing-forward
lemma after the quarter-turn in Section 5. They give every face and
angle in (1). Row eight supplies its separate strict P. The remaining
rows are precisely B's strict anchors, foreign corner point and actual
wall. The half-turn preserves the common side and canonical sign.
Theorem 1 therefore gives tan(beta_Q11)>1/4, contradicting (21).
This proves Corollary 2 without any assumed wall origin. ∎

## 7. Consequence for all nonpositive-to-positive-owned edges

**Corollary 3.** No nonpositive ordinary central in OOOO can be
immediately followed by a positive forward-owned ordinary central.

If the nonpositive predecessor omits its forward point, its axial
case is impossible by the missing-negative profile, and Corollary 2
applies. If it owns that point, the complete actual edge is already
excluded by
C1092-MPPM-NEGATIVE-OWNED-POSITIVE-OWNED-EXCLUSION.md, whose scope
includes its axial endpoint. These are the two exhaustive strict
membership alternatives for that designated predecessor. No omitted
point has been assigned to another square in this dichotomy.

The statement concerns the actual signed edge and its recipient's
strict forward membership. Other sign or membership transitions retain
their own separately proved scopes.
