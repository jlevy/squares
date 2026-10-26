# C1092: every negative central center lies in the small disk

All terminating decimals are exact rationals. Strict ownership always
refers to an actual open square. Exclusion means failure of strict
ownership and allows equality at an actual face. No upper bound on the
common side and no angle-magnitude assumption are used.

## 1. A missing positive predecessor excludes the next D

Let R(x,y)=(4−y,x). Let C,J be disjoint actual open squares of common
side a>1, and put C⁺=R⁻¹(J). Suppose their local canonical frames are

    C:   u=(c,s),    v=(−s,c),   c≥s≥0, c²+s²=1;
    C⁺:  u⁺=(d,−t), v⁺=(t,d),   d≥t≥0, d²+t²=1.

Suppose each local square strictly owns

    M=(1.65,1.65), U₀=(1,1.74),
    L₀=(1,1.6),   T=(1.74,2),

and C excludes

    H=(1,1.5), N=(1.65,2.35),
    W=(.914,2), F₀=(1,2.26).                       (1)

**Theorem 1.** C⁺ does not strictly own D=(1,2).

This is a two-actual-square theorem. Its conclusion is an exclusion,
including a possible boundary equality. In the original cycle the
H exclusion is supplied by a missing P at C's own actual boundary
owner; the other exclusions are original strict points of actual
foreign squares.

## 2. The positive predecessor faces

Write C's bands as U<u·X<U+a, V<v·X<V+a. At H the two upper bands
are strict by L₀, so H is lower-u or lower-v. If it is lower-v, then

    V≥1.5c−s.

The strict point M then gives .15c−.65s>0, hence s/c<3/13.
In this range N has its lower-u, lower-v and upper-u bands strict,
respectively by U₀,M,T:

    u(N)−u(U₀)=.65c+.61s>0,
    v(N)−v(M)=.70c>0,
    u(T)−u(N)=.09c−.35s>0.

The last inequality follows from 3/13<9/35. Therefore N is upper-v,
and its cap would give

    a≤(2.35c−1.65s)−(1.5c−s)=.85c−.65s<1.

This is impossible. Consequently

    U≥c+1.5s.                                      (2)

The lower-u, upper-u and lower-v bands at F₀ are strict by U₀,T,U₀:

    u(F₀)−u(U₀)=.52s≥0,
    u(T)−u(F₀)=.74c−.26s>0,
    v(F₀)−v(U₀)=.52c>0.

Thus its exclusion forces

    V+a≤2.26c−s=:f₀.                               (3)

At W the upper-u and lower-v bands are strict by T,L₀, because

    u(T)−u(W)=.826c>0,
    v(W)−v(L₀)=.4c+.086s>0.

This leaves two exhaustive regimes:

**Regime I: W is lower-u.** Then U≥.914c+2s. Comparison with the
strict point L₀ gives

    .4s<.086c,    s/c<43/200,    c>.97,    s<.22.    (4)

For c>.97, use c=1/sqrt(1+(s/c)²) and
.97²[1+(43/200)²]<1. The last bound follows already from
s<43/200<.22.

**Regime II: W is upper-v.** Here

    V+a≤2c−.914s=:g.                               (5)

If W lies on two excluding faces, either corresponding regime may
be used. There is no loss from retaining such equalities.

## 3. The actual separating-normal sources

Suppose, for contradiction, that C⁺ strictly owns D. The physical
square J then strictly owns

    P=R(D)=(2,1),       T_J=R(T)=(2,1.74),
    M_J=R(M)=(2.35,1.65).

Reindex its physical frame as

    u_J=(d,−t),       v_J=(t,d).

If a normal n separates C from J, strict M,M_J imply n_x>0.
Strict T,T_J imply n_x−n_y>0. The separating-axis theorem for the
two actual squares therefore leaves only the possible sources

    u=(c,s),       −v=(s,−c),       u_J=(d,−t).       (6)

A listed direction can become ineligible at an axis endpoint;
proving its inequality impossible is still valid. Put

    K=cd−st≥0,       L=ct+sd≥0,       K²+L²=1.

In particular K+L>0, and

    u_J=K u−L v.

The strict points in J give, for every nonzero normal n,

    lower_J(n)<n·P,       lower_J(n)<n·T_J.          (7)

## 4. Two sources are excluded immediately

For the source u, equation (2) gives

    upper_C(u)=U+a≥c+1.5s+a>2c+s=u·P,

because a>1≥c−.5s. This contradicts separation and (7).

For the source −v, compare with (−v)·T_J=2s−1.74c. In Regime I,
equations (3),(4) give

    upper_C(−v)−(−v)·T_J
       ≥a−.52c−s>1−.52−.22>0.

In Regime II, equation (5) gives instead

    upper_C(−v)−(−v)·T_J≥a−.26c−1.086s>0,

since

    .26c+1.086s=.26(c+s)+.826s
       ≤1.346/sqrt(2)<1.

Here c+s≤sqrt(2), s≤1/sqrt(2), and 1.346²=1.811716<2.
Thus neither u nor −v can separate the actual squares.

## 5. Source u_J in the two wall-face regimes

The exact support and equations (2),(3) or (5) give

    upper_C(u_J)=K(U+a)−LV
       ≥K(c+1.5s)−Lf+a(K+L),                      (8)

where f=f₀ in Regime I and f=g in Regime II. Since a>1 and K+L>0,
this is strictly larger than the same expression with a replaced
by 1. We compare it with u_J·T_J=2d−1.74t.

### 5.1. Regime I

The exact difference at a=1 is

    K(c+1.5s)−L(2.26c−s)+(K+L)−(2d−1.74t)
       =A d+B t,                                  (9)

where

    A=c+s−1−.76cs,
    B=c−s−.76c²+.24.

Since c+s−1=2cs/(c+s+1) and 2/(c+s+1)>.8,

    A≥.04cs≥0.

Also, by (4),

    B≥c−s−.52>.97−.22−.52=.23>0.

Therefore Ad+Bt≥0. Equation (8) makes the actual support strictly
larger than u_J·T_J, contradicting (7) and separation.

### 5.2. Regime II

This time the exact difference at a=1 is

    K(c+1.5s)−L(2c−.914s)+(K+L)−(2d−1.74t)
       =A d+B t,                                  (10)

where

    A=c+s−1−.5cs−.086s²,
    B=c−s−.5c²−.086cs+.24.

The same identity and s≤c give

    A≥.3cs−.086s²≥.214cs≥0.                        (11)

Moreover

    A+B=2c−.5c²−.586cs−.086s²−.76
       ≥sqrt(2)−.25−.293−.043−.76
       =sqrt(2)−1.346>0.                           (12)

For the inequality, 2c−.5c² is increasing for 1/sqrt(2)≤c≤1,
while cs≤1/2 and s²≤1/2. Since d≥t≥0,

    Ad+Bt=A(d−t)+(A+B)t≥0.

Again the strict a>1 in (8) makes separation impossible. All actual
sources in (6) are excluded, proving Theorem 1. ∎

## 6. Exact original owner ledger

In the original last C1092 assignment use the charts R^(−i), with

    C_i=Q_(4+i),
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

Both C_i and the next C_(i+1), in their own charts, strictly own
M,U₀,L₀,T. In C_i's chart, W and F₀ are the strict points

    R⁻¹(2,.914)=(.914,2),
    R⁻¹(1.74,1)=(1,2.26)

of the preceding actual boundary B_(i−1). The point N=R⁻¹(M)
belongs strictly to the preceding actual central C_(i−1). These
three exclusions require no boundary P premise.

If C_i's own boundary B_i does not strictly own P_i=(2,1), the
all-angle corner transfer, Theorem 7 of
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md), gives
strict H_i ownership in the actual paired corner K_i. Therefore
H_i is outside C_i. Theorem 1 applies whenever C_i is positive and
C_(i+1) is nonpositive. Its conclusion is that the latter central
excludes its own local D_(i+1). Under the common physical chart this
D is R(D)=(2,1); no claim that the missing boundary owns that point
has been inserted into the argument.

## 7. The disk consequence for every nonpositive sector

**Theorem 2.** In the original last C1092 assignment, with arbitrary
canonical signs in the four sectors, every nonpositive central
center lies strictly within radius 1/sqrt(2) of O=(2,2).

The audited theorems
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md)
and [C1092-MIXED-NEGATIVE-H.md](C1092-MIXED-NEGATIVE-H.md)
show that every nonpositive central C_j strictly owns H_j and that
its actual boundary B_j strictly owns P_j. Thus every missing P
belongs to a strictly positive central sector.

Fix a nonpositive C_j. If P_(j−1) is owned by its actual boundary,
then C_j excludes D_j because that point is strictly foreign. If
P_(j−1) is missing, C_(j−1) is strictly positive and its H is
excluded by its actual paired corner. Theorem 1, with the exact
ledger above, again gives D_j outside C_j. These alternatives are
exhaustive, including boundary equality in the missing alternative.

The full-angle local disk argument in Sections 3–4 of
[C1092-NEGATIVE-OWNED-POINTS.md](C1092-NEGATIVE-OWNED-POINTS.md)
now applies to C_j: its own P_j is strictly owned and D_j is
excluded. That local argument requires only the exclusion of D_j,
so it also applies when the exclusion is furnished by Theorem 1.
It uses the unconditional actual boundary point (1.44,1), original
foreign central points, and actual wall clearance to prove

    |center(C_j)−O|<1/sqrt(2).

This proves Theorem 2 for every nonpositive sector in a mixed
cycle. ∎

The missing-point disk theorem in
[C1092-CYCLIC-ENTRANCE.md](C1092-CYCLIC-ENTRANCE.md)
already puts every strictly positive sector with missing P inside
the same open disk. Consequently the only sectors not yet covered
by these radius conclusions are strictly positive centrals whose
own actual boundary P is strictly owned. No conclusion about
their radii, or about completion of the arbitrary-sign cycle, is
claimed here.
