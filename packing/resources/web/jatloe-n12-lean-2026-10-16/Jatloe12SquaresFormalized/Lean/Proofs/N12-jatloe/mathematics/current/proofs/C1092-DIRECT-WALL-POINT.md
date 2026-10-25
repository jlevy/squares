# A direct C1092 wall-point transfer

Subsequent global completion: the adjacent-central theorem in
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md)
now forces H and P throughout the entire all-nonpositive central
sector, using the actual preceding central owner. Together with the
full-angle owned-point disk theorem, it excludes that whole sector.
The local theorems and local counterexamples below retain their exact
individual scopes.

## 1. Status and exact scope

Starting with the original C1092 markers and the last MPPM auxiliary
assignment, the lemma below forces the missing boundary point `(2,1)` in
every sector whose boundary angle is nonnegative and satisfies the stated
cosine bound. It uses the actual bottom wall, one strict boundary auxiliary
point, and a strict segment in the actual southwest corner owner. It
requires no central center enclosure and no transferred corner point.

Sections 2–5 retain the first transfer and its exact corner-support
obstruction. Sections 6–8 give a stronger proved local result: if the
associated central square has signed half-angle in [-1/7,0], the boundary
point is forced for every boundary orientation. This uses the original
central marker and listed auxiliary assignment, the original northwest
marker exclusion, and the actual corner owner. No boundary-angle or
central-center enclosure is added.

Section 9 proves necessary support cones and face restrictions when the
boundary point is missing. Section 10 gives an exact local three-square
counterexample at positive central half-angle 1/20. All original local
point facts, actual walls, the common side, the local MPPM center sign,
and all three actual pairwise separations hold, yet the boundary point
lies on the boundary square's face. A further actual owner or a cyclic
condition is therefore necessary for a fully general positive-angle
entrance. This is not a twelve-square packing.

The central-angle condition in the stronger proved transfer remains
explicit. This note does not claim that all original C1092 central
angles lie in that interval, or that the entire MPPM entrance has been
replaced.

## 2. Geometric lemma

Let Q be an actual open square of side `a>1`, with closure in `y>=0`,
first normal `u=(c,s)`, and second normal `v=(-s,c)`, where

    c^2+s^2=1,       c>0,       s>=0.

Let `0<b<1` and `1<ell<2`, and assume

    ac>=b.

Suppose Q strictly contains

    M=(2,b),       L=(ell,1),

and its open interior is disjoint from the whole segment

    I={1} x [b,1].

Then Q strictly contains

    P=(2,1).

The segment I may, in particular, be the segment between two strict owned
points of a distinct actual convex owner. No assumption on Q's horizontal
center coordinate is needed.

### Proof

If `s=0`, the first projection of P equals that of M, and the second
projection of P equals that of L. Both satisfy the strict square
inequalities, so P lies in Q.

Now let `s>0`, and write the center as `B=(B_x,B_y)`. Since

    v·M < v·P < v·L,
    u·P > u·M,       u·P > u·L,

all square inequalities for P except its upper u inequality are strict.
If P did not belong to Q, it would therefore satisfy

    u·(P-B)>=a/2.                                     (1)

The actual bottom wall gives

    B_y>=a(c+s)/2.                                    (2)

Let V be Q's leftmost vertex:

    V=(B_x-a(c+s)/2, B_y+a(c-s)/2).

Combining (1),(2) yields

    c V_x
      <=2c+s-(a/2)[1+(c+s)^2]
       =2c+s-a(1+cs).

Because `a>1` and `s>0`,

    c V_x <2c+s-1-cs
           =c-(1-c)(1-s)<c.

Hence

    V_x<1,       V_y>=ac>=b.                          (3)

If `V_y>=1`, put `A=(1,1)`. The upper-u exclusion (1) gives

    u·(A-B)=u·(P-B)-c>=a/2-c>-a/2,

while the strict point L and `A_x<L_x` give
`u·(A-B)<a/2`. Also `v·A>v·M`, so A is strictly above Q's lower v
face. Finally, since V lies on Q's upper v face, (3) gives

    v·(A-B)-a/2
      =v·(A-V)=-s(1-V_x)+c(1-V_y)<0.

Thus all four face inequalities for A are strict, and A lies in Q. This
contradicts `A in I`.

The only remaining possibility is `b<=V_y<1`. The segment joining V to
the strict point L crosses the vertical line `x=1` at a point Z satisfying

    b<Z_y<1.

Here `V_x<1<L_x`, and both inequalities for Z_y follow from
`b<=V_y<1=L_y`. A proper convex combination of a closure point of a
convex open square and a strict interior point is strict interior.
Therefore Z belongs to Q. But `Z in I`, again a contradiction.

Both cases contradict (1). Hence P is strictly inside Q, as claimed.

## 3. Direct application to the last MPPM pattern

In each local sector of the last MPPM assignment:

* the bottom boundary owner B owns the original marker `M=(2,457/500)`;
* it owns the listed auxiliary point `L=(8/5,1)`;
* its closure lies above the actual container wall `y=0`;
* the local southwest corner owner owns `(1,457/500)` and `(1,1)`.

The final corner point follows from the retained paired-corner
inner-point theorem. The whole segment between these two corner points
is strictly inside that actual corner owner and consequently disjoint from
B. Thus the lemma applies with

    b=457/500,       ell=8/5.

It proves directly that B owns `(2,1)` whenever

    sin beta>=0,       a cos beta>=457/500.             (4)

One convenient side-independent condition implying (4) is

    0<=tan(beta/2)<=1/8,

because `cos beta>=63/65>457/500` and `a>1`. In this entire continuous
boundary-angle range, no incoming point-deduction history is required to
establish `(2,1)`.

If (4) is valid in all four local sectors, all four boundary squares own
their local points P. The preceding boundary's P becomes

    R^(-1)(2,1)=(1,2)

in the next sector. Hence each central square automatically excludes its
local `D=(1,2)` by distinctness of the actual owners. This removes D as a
separate entrance problem once the four P transfers have been established.

The C1092 positive-cycle theorem already uses this cyclic implication, so
its final geometric statement assumes strict boundary P and central
exclusion of A, but does not separately assume exclusion of D or strict
ownership of `(1,8/5)` by the central square.

## 4. Negative boundary angles: the exact remaining support condition

There is a useful complete reduction for the other sign. It identifies a
single continuous support profile that would suffice for a direct transfer;
it does not assume that profile for the original corner.

Let the boundary square now have canonical normals

    u=(c,-s),       v=(s,c),
    c>=s>0,       c^2+s^2=1.

It still owns `M=(2,b)` and `L=(ell,1)`, and lies above the actual
bottom wall. Let K be its actual southwest corner neighbor, containing
`N=(1,b)` and `A=(1,1)`. Suppose, temporarily, that P is not in B.
Its u projection lies strictly between those of L and M, while its v
projection is larger than both. Consequently its only possible exit is

    v·(P-B)>=a/2.                                     (5)

### 4.1. Every possible separating normal points right and down

Let V be B's leftmost vertex:

    V=(B_x-a(c+s)/2, B_y-a(c-s)/2).

The bottom wall and (5) give

    s V_x<=2s+c-a(1+cs)
           <s-(1-c)(1-s)<=s,

so `V_x<1`. Also, relative to V,

    u·(P-V)<a,       v·(P-V)>=a.

If `V_y>=1`, then `P_x-V_x>0` and `P_y-V_y<=0`, so `c>=s`
would imply `u·(P-V)>=v·(P-V)`, a contradiction. Thus

    V_x<1,       V_y<1.                               (6)

Take any separating face normal of either actual square and orient it
from K toward B. The strict points N in K and M in B have difference
`M-N=(1,0)`, so this normal has positive first component. If its second
component were nonnegative, (6) and the strict corner point A would give

    lower_B(n)<=n·V<n·A<upper_K(n),

contradicting separation. Thus every surviving source normal has the form

    n=(r,-t),       r,t>0,       r^2+t^2=1.             (7)

This reduction includes normals supplied by either square.

### 4.2. The boundary support cap

Define, for `r,t>=0` on the unit circle,

    F(r,t)=2r-1-r t/(1+r)
          =r-t(r+t)/(1+r).                            (8)

For every normal (7), the assumption that P is missing implies

    lower_B(r,-t)<a F(r,t).                           (9)

Here is a direct proof. Write `tau=s/(1+c)`. The leftmost vertex above
has `V_y>=as`, by the actual bottom wall. Equation (5) gives

    s(2-V_x)+c(1-V_y)>=a.

Since `n·u=rc+ts>0`, the exact support at that vertex is

    lower_B(n)=rV_x-tV_y+a min(rs-tc,0).

Eliminate V_x using the previous inequality, then use `V_y>=as`:

    lower_B(n)
      <=a[r(2-c-tau)-ts+min(rs-tc,0)]
         -(a-1)(2r+rc/s).                             (10)

The last subtracted term is strictly positive. It remains to prove

    r(2-c-tau)-ts+min(rs-tc,0)<=F(r,t).                (11)

Put `z=t/(1+r)`, so `0<=z,tau<=1`. After multiplication by
`1+tau^2`, the right side of (11) minus its left side is exactly

    (tau-z)[r tau^2-(1+r)tau+r+t]       if tau>=z,

    (z-tau)[-r tau^2+(1+r+t)tau+1-t]   if tau<=z.

In the first region, the bracket decreases on `[0,1]` and is at least
its value `r+t-1>=0` at one. In the second, the bracket equals

    1-t+tau[1+t+r(1-tau)]>=0.

These factor identities prove (11), and (10) proves the strict cap (9).

In particular, for B's own first normal, (10) specializes to the exact
formula

    lower_B(c,-s)
      <=2c-a-c(a-c)/s
       =a F(c,s)-(a-1)(2c+c^2/s)<a F(c,s).             (12)

### 4.3. A precise conditional transfer

If the actual corner neighbor K can be shown, using its interaction with
the actual central neighbor, to satisfy

    upper_K(r,-t)>=a F(r,t)
      for every r,t>0 with r^2+t^2=1,                 (13)

then P must belong to B. Indeed (7) exhausts all possible separating
normal sources, and (9),(13) contradict separation in every one of them.

Condition (13) is the matching corner support condition. The retained
all-corner windmill theorem proves a rotated/reflected instance of this
profile when its actual central neighbor has the stated axis-parallel
support bounds. Extending that corner–central implication to the general
rotated C1092 entrance remains a separate problem. The boundary side of
the implication, including its two source alternatives and its strict
margin for `a>1`, is proved above for the entire canonical negative
boundary-angle range.

## 5. Why the actual corner–central interaction is needed

The local marker facts of the corner alone do not imply (13). An exact
example makes the missing coupling concrete.

Set

    a=1001/1000,       c=399/401,       s=40/401,
    w=c+s=439/401.

Let K be the actual square of side a with normals `(c,-s),(s,c)` and
center

    (aw/2, a(1+w)/2).

Its least x coordinate is zero and its least y coordinate is `a/2`.
Its greatest y coordinate is

    a/2+aw=1280279/802000<8/5,

and its greatest x coordinate is `aw<8/5`. Thus its closure lies in
the container, and it avoids all twenty C1092 auxiliary points. It
strictly owns its original two corner markers `(1,457/500)` and
`(457/500,1)`, as well as the strict inner point `(1,1)`. To verify that
last assertion directly, the two centered projections at those three
points are, respectively,

| Point | First centered projection | Second centered projection |
|---|---|---|
| `(1,1)` | `146215439/321602000` | `-12434/4020025` |
| `(1,457/500)` | `148974319/321602000` | `-7128637/80400500` |
| `(457/500,1)` | `118695611/321602000` | `-9384/804005` |

Each absolute value is smaller than `a/2=1001/2000`.

Nevertheless, in the direction `(c,-s)`,

    upper_K(c,-s)=a(c^2-s/2)
                 =a F(c,s)-321321/3216020000
                 <a F(c,s).                          (14)

This is a counterexample to deriving the matching profile from that
corner's isolated marker and wall data. It is not a twelve-square packing:
the disjoint actual central and boundary neighbors have not been supplied.
The missing ingredient in (13) is precisely a constraint imposed by those
actual neighboring squares, rather than another consequence of the
corner's local owned and excluded points alone.

## 6. A corner profile forced by one excluded upper point

The following theorem supplies the full profile (13) from a particularly
simple genuine corner–central interaction.

### Theorem 6

Let K be an open square of side a>1 whose closure lies in the first
quadrant. Suppose that K strictly owns A=(1,1) and excludes H=(1,3/2).
Then, for every c,s>=0 with c^2+s^2=1,

    upper_K(c,-s)>=a F(c,s),
    F(c,s)=c-s(c+s)/(1+c)=2c-1-cs/(1+c).             (15)

The orientation of K is unrestricted. Neither an upper bound for a nor
any marker other than A is a premise of this theorem.

### 6.1. A continuous scalar envelope

For r,t>=0 with r^2+t^2=1, put

    tau=t/(1+r),
    G=ct+sr+max(cr-st,0)+s tau-3s/2.

Then

    G>=F(c,s).                                      (16)

To prove this over the whole two-angle quadrant, write

    r=cos theta, t=sin theta,
    c=cos phi,   s=sin phi,
    0<=theta,phi<=pi/2.

First consider theta+phi<=pi/2. Here

    G=(c+s)r+(c-s)t+s tau-3s/2,

and differentiation with respect to theta gives

    G''=-c(r+t)-s(r-t)+st/(1+r)^2.

If r,s>0, the defining condition cr>=st yields

    G''<=s[-1/r+t/(1+r)^2]<0.

If s=0, directly G''=-c(r+t)<0. Values at r=0 follow by
continuity. Thus G is concave on this interval, and its minimum occurs
at one of its endpoints.

On theta+phi>=pi/2, instead

    G=ct+sr+s tau-3s/2,
    G'=r[c-s J(r)],
    J(r)=[sqrt(1-r^2)-1/(1+r)]/r.

For 0<r<1,

    J'(r)={ (1+2r)/(1+r)^2-1/sqrt(1-r^2) }/r^2<0.

Indeed (1+2r)/(1+r)^2<1 and 1/sqrt(1-r^2)>1.
As theta increases, r decreases, so c-sJ(r) is nonincreasing.
Therefore G' can change sign only from positive to negative. The
minimum of G on this second interval is again at an endpoint. The
degenerate endpoint cases follow by continuity.

It remains to inspect only theta=0, theta=pi/2, and
theta=pi/2-phi. The first two values are both c-s/2. If

    kappa=(c+s)/(1+c),

then 1/2<=kappa<=1, and consequently c-s/2>=c-s kappa=F.
The bound kappa>=1/2 follows from c+2s>=1: for example,
c+s>=1 already suffices.

At the middle endpoint r=s,t=c,

    G=1-3s/2+sc/(1+s).

With z=s/(1+c), so 0<=z<=1, direct substitution of
c=(1-z^2)/(1+z^2), s=2z/(1+z^2) gives the exact identity

    G-F(c,s)=z^3(3-z)/[(1+z)(1+z^2)]>=0.

This proves (16) on the entire continuous quadrant.

We will also use

    1-kappa=(1-s)/(1+c)<=c/2.                        (17)

For c>0, use 1-s=c^2/(1+s) and
2c<=(1+s)(1+c). The latter follows already from
1+c>=2c and 1+s>=1. For c=0, (17) is immediate.

### 6.2. Exact support and the two possible upper faces

Every nonaxis orientation of K admits face normals

    u=(r,t), v=(-t,r),      r,t>0,      r^2+t^2=1.

There is no requirement r>=t. Write its lower face values as U,V:

    U<u·x<U+a,       V<v·x<V+a.

For the target direction n=(c,-s), set

    d=cr-st,       e=ct+sr.

Since n=d u-e v, its exact upper support is

    S=upper_K(n)=dU-eV+a max(d,0).                   (18)

The actual x wall gives

    rU-t(V+a)>=0.                                  (19)

Since H-A=(0,1/2), both lower face inequalities for H are strict.
Therefore exclusion of H implies at least one of

    U+a<=r+3t/2,       V+a<=-t+3r/2.                (20)

We cover both alternatives, retaining their possible overlap.

If the first inequality in (20) holds, (19) gives
V<=(r/t)U-a. Substitution in (18), followed by its upper bound
for U, gives

    S>=-(s/t)U+a[e+max(d,0)]
      >=aG+(a-1)s(r/t+3/2)
      >=aF.

The displayed identity uses 1/t-tau=r/t. It is valid for either
sign of d.

Now suppose the second inequality in (20) holds and d>=0.
From (19), U>=(t/r)(V+a). Thus

    S>=-(s/r)V+ad(1+t/r)
      >=a[c(r+t)+s(r-t)]+s(t/r-3/2).

Subtracting aG in this sign regime gives exactly

    S-aG>=s[t/r-tau+(a-1)(3/2-tau)]>=0.

Here t/r>=tau and 0<=tau<=1. This proves S>=aF in this
case too. This exact difference avoids assigning an unjustified sign
to the upper face value -t+3r/2.

Finally suppose the second inequality in (20) holds and d<0.
Strict ownership of A gives U<r+t, so (18) yields

    S>d(r+t)-e(-t+3r/2-a)=L+(a-1)e,
    L=c-s+(1-r/2)e.

The condition cr<st implies e>=c. Indeed

    e-c=r[s-cr/(1+t)]>=0.

Also F<=c, and, using (17),

    L-F=(1-r/2)e-s(1-kappa)
        >=c/2-s(1-kappa)>=0.

Consequently S>aF. This completes the nonaxis corner cases for
c,s>0.

If s=0, the x width of a square is at least a, and its least x
coordinate is nonnegative, so upper_K(1,0)>=a. If c=0,
strict ownership of A implies min_K y<1, and hence
upper_K(0,-1)>-1>-a=aF(0,1).

It remains to handle an axis-parallel corner. Write its lower coordinates
as k,h>=0. Since A is strict, x=1 lies strictly in its horizontal
interval. The excluded point H therefore forces h+a<=3/2. Its
rightmost x coordinate is k+a>=a, so

    S>=ac-s(3/2-a)
      >=a(c-s/2)>=aF.

The middle inequality has difference 3s(a-1)/2>=0. This proves
Theorem 6 for every orientation and every target direction.

## 7. All-angle boundary transfer from the corner profile

### Theorem 7

Let B and K be distinct open squares of the same side a>1 with disjoint
interiors. Suppose B's closure lies in y>=0, K's closure lies in the
first quadrant, and, for some 0<b<1 and 1<ell<2,

    B strictly owns (2,b), (ell,1);
    K strictly owns (1,b), (1,1) and excludes (1,3/2).

Then B strictly owns P=(2,1). Neither square has an angle restriction.

### Proof

Theorem 6 supplies the support profile (15) for K. Also
I={1} x [b,1] is strictly inside K.

If B is axis parallel, P takes its x coordinate from the strict point
(2,b) and its y coordinate from the strict point (ell,1), so it is
strict in B. Otherwise choose its actual face normals in the form

    u=(p,-q), v=(q,p),      p,q>0,      p^2+q^2=1.

Such a choice is possible for every nonaxis square. No restriction
p>=q is made: a square of positive canonical angle is represented by
reindexing and changing the sign of one of its original normals.

The u projection of P lies strictly between the u projections of
(ell,1) and (2,b), while its v projection exceeds both. Thus, if P
were missing, its only possible exit would be

    V_B+a<=v·P=2q+p.                                (21)

Let Z be B's leftmost vertex. With its center denoted by B_0,

    Z=(B_0x-a(p+q)/2, B_0y-a(p-q)/2).

This vertex lies on B's lower u and lower v faces. The actual bottom
wall gives Z_y>=aq. From (21),

    q(2-Z_x)+p(1-Z_y)>=a,

and therefore

    q Z_x<=2q+p-a(1+pq)
          <q-(1-p)(1-q)<=q.

Hence Z_x<1.

In fact Z_y<b. If Z_y>=1, let A=(1,1). Its lower u inequality
is strict because

    u·(A-Z)=p(1-Z_x)+q(Z_y-1)>0.

Its lower v inequality follows from (21):

    v·A=v·P-q>=V_B+a-q>V_B,

since a>1>q. Both upper inequalities are strict by comparison with
the strict point (ell,1). Thus A would belong to B, contrary to
its ownership by K.

If instead b<=Z_y<1, the segment from the closure point Z to the
strict point (ell,1) crosses x=1 at a strict point of B whose
height lies strictly between b and 1. This contradicts I being
strictly in K. Both alternatives are impossible, proving Z_y<b.

Orient any possible separating normal n from K toward B. Since the
strict points (1,b) in K and (2,b) in B differ by (1,0), n_x>0.
If n_y>=0, then Z_x<1 and Z_y<b<1 give

    lower_B(n)<=n·Z<n·(1,1)<upper_K(n),

which contradicts separation. Consequently every possible separating
normal has the form n=(c,-s), with c,s>0 and c^2+s^2=1.

The exact boundary support estimate of Section 4.2 now applies over
the full orientation quadrant p,q>0. Its proof did not use p>=q:
its half-angle tau=q/(1+p) is simply in (0,1). Explicitly,

    lower_B(c,-s)
      <=a[c(2-p-tau)-sq+min(cq-sp,0)]
           -(a-1)(2c+cp/q)
       <aF(c,s).

The two exact factor identities in Section 4.2 prove the last inequality
on all 0<=tau<=1. But Theorem 6 gives
upper_K(c,-s)>=aF(c,s). Thus no normal from either actual square
can separate them, a contradiction to their disjoint interiors.
The supposition that P is missing is impossible. This proves Theorem 7.

## 8. Original central ownership supplies the required upper point

### Theorem 8: a direct local C1092 entrance

In the original C1092 physical setting, assume the last auxiliary
assignment in the source chapter. Work in any of its four local charts.
If the local central square C has canonical normals

    u_C=(p,-q), v_C=(q,p),
    p>=q>=0, p^2+q^2=1,       0<=q/(1+p)<=1/7,       (22)

then the associated local bottom boundary square strictly owns (2,1),
regardless of the angles of that boundary square and its corner neighbor.

This conclusion uses no center enclosure, no long point-deduction
history, and no hypothesis on any other central angle.

### 8.1. The central square strictly owns H=(1,3/2)

The original marker and last auxiliary assignment give strict points

    M=(33/20,33/20),       U=(1,87/50),
    T=(87/50,2),           L=(1,8/5)

in C. The original northwest central marker

    N=(33/20,47/20)

belongs to a distinct actual central square, so it is outside C.

The only possible exit of N from C is upper v_C. Indeed,

    u_C·N-u_C·U=(65p-61q)/100>=p/25>0,
    u_C·T-u_C·N=(9p+35q)/100>0,
    v_C·N-v_C·M=7p/10>0.

Thus, writing V_C for C's lower v_C face value,

    V_C+a<=v_C·N.                                  (23)

For H, three inequalities follow directly from the owned points:

    u_C·H-u_C·L=q/10>=0,
    u_C·M-u_C·H=(65p-15q)/100>=p/2>0,
    v_C·L-v_C·H=p/10>0.

Each comparison gives a strict square inequality even if the first
difference is zero, because the comparison point L is strict.

For the remaining lower v_C inequality, (22) gives

    v_C·N-v_C·H=13q/20+17p/20<=499/500<1<a.         (24)

Here q/p<=7/24. The expression (13q+17p)/20 increases with the
angle on this interval, since its derivative is (13p-17q)/20>0.
At the endpoint q/(1+p)=1/7, one has p=24/25, q=7/25, and
the expression is exactly 499/500. Combining (23),(24) gives
V_C<v_C·H. All four inequalities are strict; H belongs to C.

### 8.2. Actual owner mapping and the boundary conclusion

Let R(x,y)=(4-y,x). In the chart R^(-i), put

    C_i=Q_(4+i),      K_i=Q_i,
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

The corresponding actual data are:

| Local index i | Central C_i | Corner K_i | Boundary B_i | Owner of excluded local N | Actual image of local H | Actual image of local P |
|---|---|---|---|---|---|---|
| 0 | Q_4 | Q_0 | Q_9 | Q_7 | (1,3/2) | (2,1) |
| 1 | Q_5 | Q_1 | Q_10 | Q_4 | (5/2,1) | (3,2) |
| 2 | Q_6 | Q_2 | Q_11 | Q_5 | (3,5/2) | (2,3) |
| 3 | Q_7 | Q_3 | Q_8 | Q_6 | (3/2,3) | (1,2) |

Every entry is an actual owner transported by the same chart. Each K_i
owns local (1,b) from its original paired corner markers and local
(1,1) from the retained paired-corner inner-point theorem. Since C_i
strictly owns local H and C_i,K_i are distinct, K_i excludes H.
Its actual container walls place its closure in the local first quadrant.

Each B_i owns local (2,b) from its original marker and local
(8/5,1) from the displayed auxiliary assignment. Its closure lies
above the local bottom wall. Theorem 7 therefore applies with

    b=457/500,       ell=8/5,

and proves strict ownership of local P.

If all four local central signed half-angles lie in [-1/7,0], all
four applications hold simultaneously. In particular each central
square then excludes its local D=(1,2): that point is the preceding
boundary's strict P after the same quarter-turn transport. More
generally, a proved P transfer in sector i gives the D exclusion
in sector i+1, with indices modulo four.

The condition on the central angle is sufficient, not asserted to
cover every original auxiliary-pattern realization. The result removes
the P and cyclic D point-transfer tasks throughout that entire continuous
four-central-angle region; it does not by itself supply the center
and relative-center inequalities needed for the cycle theorem.

The example in Section 5 is consistent with this new result. Its
isolated corner contains H, and therefore does not satisfy Theorem 6.
The additional exclusion here comes from the original actual central
owner, rather than an added condition on the isolated corner.

### 8.3. Exact coverage of the retained original angle domains

The documented common 431-cut parent does not already remove every
nonpositive angle outside (22). Section 2 of the retained chapter
wall_geometry_next/13_final_MPPM23_ordered_histories.txt explicitly
retains the possible maximal bins

    {0,...,10} union {40,...,63}.

For a raw first-quadrant half-angle t in bin k>=40, the canonical
negative half-angle has magnitude (1-t)/(1+t). Consequently the
negative bins 40,...,47 together cover magnitudes

    1/7<=|canonical half-angle|<=3/13,

with every magnitude strictly above 1/7 outside Theorem 8's sufficient
range. Bin 47 shares its endpoint 1/7 with the covered range. The
later retained maximal-angle histories, rather than the original local
marker assignment or Theorem 8, handle those steeper ranges. Likewise,
Theorem 8 does not include positive central angles. These are coverage
statements about the retained domains, not assertions that any surviving
domain row is realized by a global packing.

## 9. Exact consequences of a missing boundary point

Theorems 6–7 also give a useful unconditional alternative, without an
angle condition on C:

    if the local B misses P=(2,1), then the actual local K
    strictly owns H=(1,3/2).                         (25)

Indeed, if H were outside K, all premises of Theorem 7 would hold and
would force P inside B. The complement of an open square includes its
boundary, so this contrapositive proves strict ownership in (25), not
merely closure membership. The actual central neighbor therefore
excludes H.

Here are corresponding proved reductions for the three actual square
pairs. They remain necessary conditions and do not assert a contradiction.
Every normal is oriented from the first named owner toward the second:

| Actual pair | Necessary cone for every separating normal |
|---|---|
| K toward B | n_x>0 and n_y<0 |
| B toward C | n_y>0 and -(50/7)n_y<n_x<(343/500)n_y |
| K toward C | n_y>0 and n_x>-(3/13)n_y |

The first row is proved in Theorem 7 before its final use of the corner
profile. For the second row, compare the strict pairs
(87/50,1) in B with (87/50,2) in C,
(8/5,1) in B with (87/50,2) in C, and
(2,457/500) in B with (1,8/5) in C.
Their respective differences are (0,1), (7/50,1), and
(-1,343/500). For the third row, use H in K and the strict
points (1,8/5),(33/20,33/20) in C. Their differences from H
are (0,1/10),(13/20,3/20). Strict owned points lie strictly
on their respective sides of a weak support separator, which makes
all these normal inequalities strict. These arguments retain all face
normal sources from both actual squares.

There are also short exact face restrictions. Reindex B as in Theorem 7,
with normals (p,-q),(q,p), p,q>0 and lower faces U_B,V_B.
The corner point A=(1,1) can leave B only through lower u:
its two upper bands are strict by comparison with (ell,1), and
(21) puts it strictly above the lower v face because a>q.
Thus

    U_B>=p-q,
    V_B+a<=2q+p,
    pV_B-q(U_B+a)>=0,

where the last inequality is the actual bottom wall. Eliminating U_B,V_B
gives

    a(p+q)<=1+pq.                                   (26)

For a nonpositive central angle, (25) makes H leave C only through
lower v_C: its other three bands are strict by the comparisons in
Section 8.1. The original northwest marker N still leaves only through
upper v_C throughout the full canonical nonpositive range. Hence

    a<=17p/20+13q/20.                               (27)

This includes the contradiction of Section 8 when q/(1+p)<=1/7.

For a nonnegative central frame (p,q),(-q,p), the point H has both
upper bands strict, so its exit is lower u or lower v. The point N
has both lower bands strict, so its exit is upper u or upper v.
An upper-u exit of N requires

    q/p>9/35,                                      (28)

because the strict point T=(87/50,2) has
u_C·N-u_C·T=(-9p+35q)/100.
If instead N exits upper v, H cannot exit lower v: that would give

    a<=v_C·N-v_C·H=17p/20-13q/20<=17/20<1.

Thus in this latter positive-angle regime H is forced lower u.
These reductions are genuine consequences of actual ownership, but
they do not by themselves close the remaining positive-angle interaction.

## 10. Exact limit of an unrestricted local three-square entrance

The original three local owners, even with all their original marker
and auxiliary absences and all three actual separating supports, do not
force P for every positive central angle. The following exact example
shows why a further actual owner or a cyclic constraint is necessary.
It is a three-square example only, not a twelve-square packing and not
a counterexample to any of the completed cycle theorems.

### 10.1. Exact squares

Put

    a=10001/10000,       p=399/401,       q=40/401.

Use an axis-parallel K, a central C with normals
(p,q),(-q,p), and a boundary B with normals (p,-q),(q,p).
Their centers are

    K_0=(10001/20000, 16972799/16000000),
    C_0=(1792463/1200000, 33/20),
    B_0=(240812019/160400000, 4390439/8020000).        (29)

All squares have this one common side, and
1<a<1001/1000. The signed canonical half-angles of C and B are
respectively 1/20 and -1/20. In particular C is outside the
nonpositive hypothesis of Theorem 8.

For a point X and a square S with its indicated unit normals u,v,
define the inward face margin

    m_S(X)=a/2-max(|u·(X-S_0)|,|v·(X-S_0)|).

The strictly owned local points and minimum margins are:

| Square | Required strict points | Minimum inward face margin |
|---|---|---|
| K | (1,457/500), (457/500,1), (1,1) | 1/10000 |
| C | (33/20,33/20), (1,87/50), (1,8/5), (87/50,2) | 610441/160400000 |
| B | (2,457/500), (8/5,1), (87/50,1) | 52/2005 |

Every listed margin is strictly positive. Directly, C's four respective
margins in the order (marker, (1,87/50), (87/50,2), (1,8/5))
are

    55265599/160400000, 2850441/160400000,
    4243277/24060000,   610441/160400000.

These equalities verify all required strict ownership without a limiting
or numerical argument.

### 10.2. Walls, MPPM sign, and actual separation

K's exact coordinate ranges are

    0<=x<=10001/10000,
    8971999/16000000<=y<=24973599/16000000.

For C and B the coordinate half-width is

    aw/2=4390439/8020000,       w=p+q.

Subtracting and adding this value to the coordinates in (29) gives
strictly positive lower coordinates for C and upper coordinates below
4 for both squares. For B the lower y coordinate is exactly zero.
Thus all three closures lie in [0,4]^2, with their required actual
corner and bottom walls. The local MPPM tangent-center condition also
holds:

    B_0x=240812019/160400000<2.

Their actual support gaps are

    lower_B(p,-q)-upper_K(p,-q)=0,
    lower_C(p,q)-upper_K(p,q)=0,
    lower_C(q,p)-upper_B(q,p)
       =66517763/9648060000>0.                      (30)

Each direction is a face normal of an actual member of the corresponding
pair. Hence the three open interiors are pairwise disjoint. The two weak
equalities are legitimate support separations for open squares.

Nevertheless,

    upper_B(q,p)=2q+p=(q,p)·(2,1),                  (31)

and P satisfies the other three bands strictly, so P lies on B's upper
v face and is not in B. Also

    m_K(1,3/2)=1/10000>0.

Thus the forced alternative (25) holds exactly as proved.

### 10.3. All original marker and auxiliary absences

For completeness, label the two markers of corner owner Q_i by
Q_ia,Q_ib in the order in the original table. The full original marker
list is

| Original owner | Marker or markers |
|---|---|
| Q_0 | (1,b), (b,1) |
| Q_1 | (3,b), (d,1) |
| Q_2 | (3,d), (d,3) |
| Q_3 | (1,d), (b,3) |
| Q_4 | (33/20,33/20) |
| Q_5 | (47/20,33/20) |
| Q_6 | (47/20,47/20) |
| Q_7 | (33/20,47/20) |
| Q_8 | (b,2) |
| Q_9 | (2,b) |
| Q_10 | (d,2) |
| Q_11 | (2,d) |

Here b=457/500,d=1543/500. The auxiliary labels used below have
exactly the source coordinates:

| j | F_j | G_j |
|---|---|---|
| 0 | (1,87/50) | (1,8/5) |
| 1 | (1,113/50) | (1,12/5) |
| 2 | (8/5,1) | (87/50,1) |
| 3 | (8/5,3) | (87/50,2) |
| 4 | (2,87/50) | (87/50,3) |
| 5 | (2,113/50) | (113/50,1) |
| 6 | (12/5,1) | (113/50,2) |
| 7 | (12/5,3) | (113/50,3) |
| 8 | (3,87/50) | (3,8/5) |
| 9 | (3,113/50) | (3,12/5) |

K owns no auxiliary point. Indeed its largest x coordinate is less than
8/5 and its largest y coordinate is less than 8/5. Every auxiliary
point has either x>=8/5 or y>=8/5. The same coordinate bounds show
that K excludes every original marker other than its two prescribed
corner markers.

All remaining absences can be checked with very small outer face
enclosures. For C, its exact unnormalized face intervals are

    184589559/400000 < 399x+40y < 345005599/400000,
    23884871/60000   < -40x+399y < 47947277/60000.

Consequently C lies in the simpler open enclosure

    461<399x+40y<863,       398<-40x+399y<800.       (32)

For B, its exact intervals are

    150643961/400000 < 399x-40y < 311060001/400000,
    779599/10000     < 40x+399y < 479,

so B lies in

    376<399x-40y<778,       77<40x+399y<479.         (33)

In the following table, lower u or upper u means that the point lies
on or beyond that face of the enclosing rectangle (32) or (33), and
likewise for v. Each entry follows by direct substitution into the
displayed integer linear forms.

| Square and violated enclosing face | Original foreign markers | Unowned auxiliary points |
|---|---|---|
| C: lower u | Q_0a,Q_0b,Q_8 | none |
| C: upper u | Q_1a,Q_1b,Q_2a,Q_2b,Q_5,Q_6,Q_10,Q_11 | F_4,F_5,F_6,F_7,F_8,F_9,G_5,G_6,G_7,G_8,G_9 |
| C: lower v | Q_9 | F_2,G_2 |
| C: upper v | Q_3a,Q_3b,Q_7 | F_1,F_3,G_1,G_4 |
| B: lower u | Q_0a,Q_0b,Q_3a,Q_3b,Q_8 | F_0,F_1,G_0,G_1 |
| B: upper u | Q_1a,Q_1b,Q_2a,Q_2b,Q_5,Q_6,Q_10 | F_6,F_7,F_8,F_9,G_5,G_6,G_7,G_8,G_9 |
| B: upper v | Q_4,Q_7,Q_11 | F_3,F_4,F_5,G_3,G_4 |

This accounts for every original marker outside the tested owner and
every auxiliary point absent from its assigned mask. In particular C
excludes the genuine northwest marker Q_7, and the exact local masks
are K:0, C:9217, B:4100. The other three corner inner points
(3,1),(3,3),(1,3) are also outside all three squares by the same
enclosures, while (1,1) is outside C and B.

### 10.4. The precise remaining global input

This example satisfies all the original local point facts, the common
side interval, actual walls, the local MPPM center sign, and all three
actual square separations. Thus a theorem using only those local
premises cannot force P in the positive-central regime. Another actual
owner or a genuinely cyclic support condition is necessary.

A concrete globally sourced condition violated by this example is the
central exclusion of D=(1,2). In fact

    m_C(D)=7010441/160400000>0.

The actual preceding boundary's strict local P would imply that exclusion
after rotation. This identifies a precise cyclic point-transfer task that
the local triple does not resolve. The example does not assert that
adding D alone would exclude every remaining local configuration, and
no positions are supplied for the other nine original owners.
