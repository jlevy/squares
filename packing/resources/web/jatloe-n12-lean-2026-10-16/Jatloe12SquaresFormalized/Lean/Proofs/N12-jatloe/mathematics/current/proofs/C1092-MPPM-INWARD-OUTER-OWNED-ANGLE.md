# C1092 MPPM: the inward square that still owns its outer point

All terminating decimals are exact rationals. Owned points are strict and
excluded points may lie on the boundary. This chapter treats the genuine
inward alternative that owns G0 but omits F0; it does not replace that
alternative by the different G0-omitted case. The argument uses a whole
strict foreign segment, not independent choices of its endpoint faces.

## 1. A local continuous theorem

**Theorem 1.** Let C be an open square of side a>1. Suppose C strictly owns

    M=(-.35,-.35), I=(0,-.26), J=(-.26,0), G=(-1,-.4),

excludes

    O=(0,0), F=(-1,-.26),

and is disjoint from the whole segment

    S=[B,A], B=(-.4,-1), A=(-.26,-1).

Then C has a strictly negative canonical frame

    u=(c,-s), v=(s,c), c>=s>0, c^2+s^2=1,

and its half-angle satisfies

    0<z:=s/(1+c)<beta:=1-sqrt(13)/5.                 (1)

In particular z<.279. Writing U,V for its lower faces and J_C=U+a,
H_C=V+a for its upper faces, its actual faces obey

    U>=-c+.26s, H_C<=0, V>=-c-.4s.                  (2)

At A there are precisely the following possible exits:

    lower v:  V>=-c-.26s and z<.26;
    upper u:  J_C<=-.26c+s and s/c>1/2.             (3)

The latter alternative is also subject to (1). All inequalities on
excluded faces in (2)-(3) are weak; the angle conclusions are strict.

## 2. The nonnegative canonical sign is impossible

Suppose first that C has frame (c,s),(-s,c), c>=s>=0. At F its two lower
bands follow from the strict point G, and its upper u-band follows from
the strict point J. Consequently F must be upper v, giving

    H_C<=s-.26c.

At B its upper u-band follows from M and its upper v-band from G:

    u(M)-u(B)=.05c+.65s>0,
    v(G)-v(B)=.6(c+s)>0.

Its lower u-band also follows from G, since

    u(B)-u(G)=.6(c-s)>=0.

Thus B must be lower v and V>=.4s-c. The opposite v-faces now give

    a<=.74c+.6s<=sqrt(.9076)<1,

a contradiction. Strict ownership supplies strict bands even when one
displayed projection difference is zero, so this proof includes the
axial and diagonal representatives.

## 3. The negative sign and the two endpoint exits

Use the negative frame in Theorem 1. If s=0, strict I and J already put O
in both open coordinate bands. Thus s>0. The two u-bands of O follow
from I,J, and its lower v-band follows from M. Its only exit is upper v,
so H_C<=0 and V<=-a.

At F, its upper u-band follows from M; its lower v-band follows from G;
and its upper v-band follows from I, since v(I)-v(F)=s>0. Therefore F is
lower u, giving U>=-c+.26s and

    J_C>=a-c+.26s.                                  (4)

At B, its lower u-band and upper v-band follow from G, with projection
increments .6(c+s)>0 and .6(c-s)>=0. An upper-u exit would combine with
the lower-u face at F to give

    a<=.6c+.74s<=sqrt(.9076)<1.

Thus B is lower v and V>=-c-.4s. This proves (2).

At A its lower u-band follows from G and its upper v-band from I. Hence
A is lower v or upper u. If it is lower v, the upper cap H_C<=0 gives

    1<a<=c+.26s.

The identity c+.26s-1=2z(.26-z)/(1+z^2) proves z<.26.

If A is upper u, then J_C<=-.26c+s, and the opposite face at F gives

    1<a<=.74(c+s).

For s/c<=1/2, one has c+s<=3/sqrt(5), whereas
(.74)(3/sqrt(5))<1 because (2.22)^2<5. Therefore s/c>1/2. This proves
the two alternatives (3), with no assumed ownership of either endpoint
by C.

## 4. The whole segment excludes every z>=beta

It remains to bound the upper-u alternative in (3). Suppose z>=beta.
The exact identities

    Q=1-c+.26s,
    Q-z=-z(z^2-2z+12/25)/(1+z^2),
    c+s-1-cs+.26s^2=s(Q-z)                          (5)

show Q>=z on beta<=z<=sqrt(2)-1. Indeed the roots of the quadratic in
(5) are 1-sqrt(13)/5 and 1+sqrt(13)/5.

Let Z=J_C u+Vv be C's lowest closure vertex. By (4) and V<=-a,

    Z_y=-sJ_C+cV
        <=-a(c+s)+cs-.26s^2
        <-1-[c+s-1-cs+.26s^2]<=-1.                (6)

The first strict inequality retains a>1. Thus equality at z=beta is
excluded as well.

On the actual line y=-1, the lower-v face meets at

    x_l=(V+c)/s>=-.4,

and the upper-u face meets at

    x_r=(J_C-s)/c<=-.26.

Equation (6) is exactly the inequality x_l<x_r. Choose any x strictly
between x_l and x_r. Then (x,-1) lies on S and has both v>V and u<J_C.
Its other two coordinate bands are strict throughout S: the lower
u-band follows from G, because u(B)>u(G), and the upper v-band follows
from I, because v(A)<v(I). Consequently (x,-1) is strictly inside C,
contrary to C being disjoint from S. This proves (1) and Theorem 1.

## 5. Literal original no-omission MPPM application

Retain the complete original entrance, the actual twelve owners and the
no-omission wall pairs in C1092-MPPM-NO-OMISSION-REDUCTION.md. Normalize
the inward central owner as Q4. If Q4 owns F4,G3,G0 and omits F0 and
the physical point (2,2), translate by (-2,-2). The local strict
M,I,J,G become respectively the actual SW marker,F4,G3,G0; the excluded
F is the genuine F0 omission. The segment S has endpoints F2,G2, both
strictly in the one actual bottom square Q9. Its entire closed segment
is therefore strict in Q9 and disjoint from the different actual Q4.
Every hypothesis of Theorem 1 is literal. No wall-center condition or
additional owner for an omitted point is used by this application.

Simultaneous quarter-turns give the corresponding result at the other
three sectors. This is a proved angle and face reduction of the
outer-point-owned inward branch. It does not assert that its center is
owned or that the whole OOOI/OIOI family is yet excluded.

## 6. A strict outer halfpoint and the actual bottom origin

**Corollary 2.** Under Theorem 1, C strictly owns Z=(-1,-.5). In the
original application of Section 5 this gives

    (1,1.5) strictly in Q4,
    (2,1) strictly in the actual bottom square Q9.     (7)

Indeed beta=1-sqrt(13)/5<1/3, since 13>100/9. The function
sin p+.5cos p increases strictly on the canonical interval and equals
1 at p=2 arctan(1/3). Thus the strict angle bound (1) gives

    s+.5c<1.

At Z the lower v-band follows from V<=-a<-1<v(Z)=-s-.5c, and its
upper v-band follows from G, with projection difference .1c>0. Its
lower u-band follows from G, with difference .1s>0; its upper u-band
follows from M, with difference .65c-.15s>=.5c>0. Every band is
strict, proving Z in C.

For the second point in (7), apply the all-angle paired-corner transfer
in C1092-DIRECT-WALL-POINT.md, Theorem 7, to the actual pair K=Q0 and
B=Q9, with b=.914 and ell=1.6. The actual SW corner Q0 strictly owns
(1,.914) and (1,1), is contained in the real first-quadrant walls, and
excludes (1,1.5) because it is strict in the different actual Q4.
The actual bottom square Q9 strictly owns (2,.914) and F2=(1.6,1),
and obeys the genuine bottom wall. The common side is a>1. These are
exactly that theorem's hypotheses, so its conclusion is the strict
bottom origin (2,1) in Q9. No assertion about the ownership of an
omitted auxiliary is used.
