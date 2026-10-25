# Direct cyclic consequences of a missing C1092 wall point

## 1. Scope and notation

This note starts with the original C1092 markers, the last MPPM auxiliary
assignment, the actual container walls, and the actual disjoint square
owners. It does not assume the long entrance histories or their center
and angle enclosures. A missing wall point means nonmembership in an
open square; equality with a face is included throughout.

The first main conclusion is a necessary displacement of the central
owner in every sector whose boundary owner misses its wall point:

    P not in B  ==>  C_x+C_y>3.                     (1)

This holds for every central orientation and every boundary orientation.
For a nonpositive canonical central angle the stronger bound is
C_x+C_y>63/20. The proof retains each of the three possible actual
boundary-to-central separating-face sources. These are continuous
inequalities, not checks of an angle subdivision.

The coordinates in (1) are the local sector coordinates. In particular,
four simultaneous missing wall points imply the strict cyclic sum

    sum_i (C_ix+C_iy)>12.                           (2)

A separate geometric inequality is needed to contradict (2). This note
does not assume that the opposite weak inequality holds automatically.

Sections 7–11 go further. They put each central center whose boundary
point is missing strictly inside the disk of radius 1/sqrt(2) about
(2,2), for either central sign. Four simultaneous missing wall points
are therefore impossible. This proves that at least one actual boundary
owns its wall point for every central sign combination. It does not yet
prove that ownership propagates to all four sectors.

Work first in the southwest local chart. The common side satisfies a>1.
The actual central square C strictly owns

    M=(33/20,33/20),       U_0=(1,87/50),
    L_0=(1,8/5),          T=(87/50,2),

and excludes the original northwest central marker

    N=(33/20,47/20).

The actual bottom boundary square B strictly owns

    (2,b), (8/5,1), (87/50,1),       b=457/500,

and its closure lies in y>=0. The distinct actual corner K strictly
owns (1,b) and (1,1), and its closure lies in the first quadrant.
All pairwise open interiors are disjoint. Set

    P=(2,1),       H=(1,3/2).

For any square with orthonormal face normals u,v, write its open face
intervals as

    U<u·x<U+a,       V<v·x<V+a.

Thus U,V always denote lower face values, rather than center
coordinates. An actual separating normal from B toward C satisfies
upper_B(n)<=lower_C(n); equality is allowed.

We use the proved all-angle wall-point transfer and scalar support
envelope from Sections 6–7 of C1092-DIRECT-WALL-POINT.md. Their exact
forms needed here are recalled in Section 2. No local counterexample
from Section 10 of that note is promoted to a global packing.

## 2. Consequences of a missing wall point

Assume P is not in B. The contrapositive of the all-angle transfer gives

    H is strictly inside K.                        (3)

Consequently H is outside the distinct actual central C. This is a
strict ownership conclusion for K even when P lies on a face of B.

The boundary square is not axis parallel. Reindex its actual normals as

    u_B=(p,-q),       v_B=(q,p),
    p,q>0,           p^2+q^2=1.

There is no restriction p>=q. Section 9 of the cited note proves

    U_B>=p-q,
    V_B+a<=2q+p,
    p V_B-q(U_B+a)>=0.                             (4)

The last inequality is the actual bottom-wall condition. Eliminating
V_B from (4) yields the useful exact cap

    U_B<=a F(p,q)-(a-1) E,
    F(p,q)=2p-1-pq/(1+p),
    E=2p+p^2/q,       E-F(p,q)=1+p/q>0.            (5)

For example, the immediate eliminated expression is
U_B<=2p+p^2/q-a(1+p/q); it equals (5) by p^2+q^2=1.

Let Z be B's leftmost vertex. It lies on B's two lower faces. The
actual bottom wall and missing-P upper-v cap give

    Z_y>=aq,       q Z_x+p Z_y<=2q+p-a.            (6)

Finally every actual separating normal from B toward C lies in

    n_y>0,       -(50/7)n_y<n_x<(343/500)n_y.       (7)

For completeness, compare the respective strict B and C points
(87/50,1),(87/50,2); (8/5,1),(87/50,2); and
(2,b),(1,8/5). Their differences are (0,1), (7/50,1), and
(-1,343/500). Strict ownership makes their scalar products with a
weak separating normal strictly positive, which proves (7).

### 2.1. An upward support estimate

For any target unit vector (-s,c), where c,s>=0 and c^2+s^2=1, set

    A=cq+sp,       D_*=cp-sq,       t=q/(1+p),
    G_2=A+max(D_*,0)+st-2s,
    T_B=s(2+p/q).

Then

    upper_B(-s,c)>=a G_2+(a-1)T_B.                (8)

Indeed, from the leftmost vertex the edge in direction (p,-q) has
negative target projection, while the edge in direction (q,p) has
projection D_*. The exact support is therefore

    upper_B(-s,c)=-s Z_x+c Z_y+a max(D_*,0).

Eliminate Z_x using (6), and then use Z_y>=aq. The coefficient of
Z_y is c+sp/q>=0. This gives

    upper_B(-s,c)
      >=-s(2q+p-a)/q+(c+sp/q)aq+a max(D_*,0),

which is (8), using t+p/q=1/q. This proof covers both signs of
D_* and the endpoint s=0.

The full-quadrant scalar envelope already proved in Section 6.1 of
C1092-DIRECT-WALL-POINT.md is

    cq+sp+max(cp-sq,0)+s q/(1+p)-3s/2
      >=F(c,s),
    F(c,s)=2c-1-cs/(1+c).                          (9)

Thus

    G_2>=F(c,s)-s/2,
    G_2+T_B=A+max(D_*,0)+s/q>0.                   (10)

The second strict inequality follows from A>0 for a unit target in
the closed first quadrant and p,q>0.

## 3. The missing point fixes the central exit of H

### 3.1. Nonpositive central angle

Write C's canonical normals as

    u_C=(c,-s),       v_C=(s,c),
    c>=s>=0,         c^2+s^2=1.

Three face inequalities for H are strict, because

    u_C·H-u_C·L_0=s/10>=0,
    u_C·M-u_C·H=(65c-15s)/100>0,
    v_C·L_0-v_C·H=c/10>0.

Since H is excluded by (3), it must leave through lower v_C:

    V_C>=s+3c/2.                                  (11)

The original excluded N has only its upper v_C exit available:

    u_C·N-u_C·U_0=(65c-61s)/100>0,
    u_C·T-u_C·N=(9c+35s)/100>0,
    v_C·N-v_C·M=7c/10>0.

Consequently

    V_C+a<=33s/20+47c/20,
    a<=13s/20+17c/20.                             (12)

In particular s=0 is impossible under the missing-P assumption.

### 3.2. Positive central angle

Now write

    u_C=(c,s),       v_C=(-s,c),
    c>=s>0,         c^2+s^2=1.

H's upper u_C inequality is strict by comparison with M, and its
upper v_C inequality is strict by comparison with L_0. Hence only
lower-u_C and lower-v_C exits are possible.

Suppose that H left through lower v_C. Since M is strict,

    v_C·M-v_C·H=(15c-65s)/100>0,

so s/c<3/13. Both lower bands of N are strict: use U_0 for its
lower u_C band and M for its lower v_C band. An upper-u_C exit of
N would require, by the strict point T,

    u_C·N-u_C·T=(-9c+35s)/100>0,

and therefore s/c>9/35. Since 3/13<9/35, N must instead leave
through upper v_C. But the proposed lower-v_C exit of H would then
give

    a<=v_C·N-v_C·H=17c/20-13s/20<=17/20<1,

a contradiction. We have proved the unique exit

    U_C>=c+3s/2.                                  (13)

No positive-angle bound was used. The axis-parallel orientation was
already ruled out in Section 3.1.

## 4. Diagonal displacement for a nonpositive central angle

### Theorem 1

Under the original local ownership hypotheses of Section 1, if P is
missing and the canonical central angle is nonpositive, then

    C_x+C_y>63/20.                                (14)

### Proof

The center projections are U_C+a/2,V_C+a/2. Hence

    C_x+C_y=(c-s)(U_C+a/2)+(c+s)(V_C+a/2).

Strict ownership of M gives U_C+a/2>33(c-s)/20-a/2.
Use this and (11), keeping a weak inequality when c=s. Direct
expansion gives

    C_x+C_y
      >=63/20-s^2/2-4cs/5+a s
       =63/20+s(a-s/2-4c/5).

Here s>0 by (12), and

    s/2+4c/5<=sqrt(89)/10<1<a.

The last summand is strictly positive. This proves (14), including
the endpoint c=s. Notice that no boundary-to-central separator was
needed in this sign regime.

## 5. Diagonal displacement for a positive central angle

### Theorem 2

Under the original local ownership hypotheses of Section 1, if P is
missing and the canonical central angle is positive, then

    C_x+C_y>3.                                    (15)

There is no restriction on the boundary angle.

### Proof and the three exhaustive actual sources

Use the positive central notation from Section 3.2 and put

    L=c+s,       M_*=c-s,       H_u=c+3s/2,
    S=C_x+C_y=L U_C+M_* V_C+a c.

We use M_* for this nonnegative coefficient, to distinguish it from
the original central marker M. Equation (13) says U_C>=H_u.

Two disjoint actual squares have a weak separating normal parallel
to a face normal of one of them. The cone (7) excludes both downward
central normals and also u_C=(c,s), since c/s>=1>343/500.
Among the boundary normals only v_B=(q,p) and -u_B=(-p,q) point
upward. Thus the following three cases exhaust the actual sources:

    v_C=(-s,c),       v_B=(q,p),       -u_B=(-p,q).

Possible overlap of the cases is harmless. No normal is selected
without accounting for the alternatives.

### 5.1. The central normal v_C

Separation gives V_C>=upper_B(v_C). Equations (8) and (13) yield

    S>=L H_u+M_*[aG_2+(a-1)T_B]+a c.

At a=1 the right side is L H_u+M_*G_2+c. The coefficient of
a-1 is

    c+M_*(G_2+T_B)>0

by (10). Since a>1, again using (10),

    S>L H_u+M_*[F(c,s)-s/2]+c.

Let h=s/(1+c), so 0<h<=sqrt(2)-1. Substitution of
c=(1-h^2)/(1+h^2), s=2h/(1+h^2) gives the exact identity

    L H_u+M_*[F(c,s)-s/2]+c-3
      =h(1-h)(h^3+3h^2-h+1)/(1+h^2)^2>=0.         (16)

Indeed 1-h>0 and h^3+3h^2-h+1>=1-h>0. Thus S>3.

### 5.2. The boundary normal v_B

Write r=q/p. The cone (7) gives

    0<r<343/500<1/sqrt(2)<=c.

In particular p>q and D_*=pc-qs>0. Set A=qc+ps>0.
The lower central support in this direction is A U_C+D_* V_C.
On the boundary side, the actual wall and U_B>=p-q give

    upper_B(v_B)=V_B+a
      >=a(1+r)+q-q^2/p.

Use the exact identity

    L D_*-M_* A=p-q>0

to eliminate V_C and then use U_C>=H_u. It follows that

    S>=(p-q)H_u/D_*
       +M_*[a(1+r)+q-q^2/p]/D_*+a c.             (17)

The coefficient of a in (17) is positive. Let S_1 denote its right
side at a=1, and define

    B_0=c^2-c+s/2.

An exact simplification gives

    S_1-3={B_0(1-r)+M_*r(c-r)
                    +M_*(1+r)(1/p-1)}/(c-rs).   (18)

Every term in its numerator is nonnegative. To check the only less
immediate sign, use 1-c=s^2/(1+c) to obtain

    B_0=s[1/2-cs/(1+c)]>=0,

since 2cs<=1<=1+c. The remaining signs follow from r<c,
r<1, M_*>=0, and p<=1; also c-rs>0. Thus S_1>=3 and,
because a>1 in (17), S>3.

### 5.3. The boundary normal -u_B

Again let A=qc+ps>0 and D_*=pc-qs, now allowing either sign
of D_*. The exact lower central support in direction (-p,q) is

    -D_* U_C+A V_C-a max(D_*,0).

Separation from B therefore gives

    -U_B<=-D_* U_C+A V_C-a max(D_*,0).

Use L A+M_*D_*=p+q>0, then (13) and the cap (5), to find

    S>=(p+q)H_u/A
       -M_*[aF(p,q)-(a-1)E]/A
       +a[c+M_*max(D_*,0)/A].                    (19)

The coefficient of a-1 relative to a=1 is

    c+(M_*/A)[max(D_*,0)-F(p,q)+E]>0,

because E-F(p,q)=1+p/q>0. Consequently it suffices to prove

    J=(p+q)H_u+M_*[max(D_*,0)-F(p,q)]
                  +(c-3)(qc+ps)>=0.             (20)

Here is a complete two-regime proof of this scalar inequality.
Keep B_0=c^2-c+s/2>=0, and set

    t=q/(1+p),       0<t<1,
    C_1=1-c-s(c-1/2),
    X=-c+(c+1/2)s=-M_*+s(c-1/2).

If D_*>=0, substitution of F(p,q) from (5) and
c^2+s^2=1 gives exactly

    J=M_*(1-t)+B_0p+C_1q.                         (21)

If C_1>=0, all three terms are nonnegative. If C_1<0, fix c,s
and increase the boundary angle beta, with p=cos(beta),
q=sin(beta), on its interval D_*>=0. Each term on the right
side of (21) is nonincreasing: t increases, p decreases, and q
increases. Hence its minimum on that interval is at D_*=0. At
that endpoint it agrees with the expression in the next regime.

If D_*<=0, the exact expression is instead

    J=M_*(1-t)+Xp+B_0q.

Write rho=1-t and use p=(1-t^2)/(1+t^2),
q=2t/(1+t^2). Then

    (1+t^2)J
      =rho{s(c-1/2)(1+t)-M_*t rho}+2B_0t.         (22)

The defining condition D_*<=0 is
c(1-t^2)<=2st, so

    rho<=2st/[c(1+t)].

The already proved inequality B_0>=0 is equivalently

    M_*<=2c(c-1/2).

Since c>=1/sqrt(2)>1/2 and 0<t<1, these give

    M_*t rho
      <=2M_*t^2s/[c(1+t)]
      <=4(c-1/2)t^2s/(1+t)
      <=s(c-1/2)(1+t).

The last step uses 2t<=1+t. Both summands in (22) are therefore
nonnegative. This proves (20) for D_*<=0 and also supplies the
transition value needed for (21). Thus (20) holds on the full
continuous orientation quadrant. Equation (19), with a>1,
now proves S>3 in this last actual source case.

All three sources have been covered, completing Theorem 2.

## 6. Actual four-sector consequence and remaining global step

Let R(x,y)=(4-y,x). In the chart R^(-i), use

    C_i=Q_(4+i),       K_i=Q_i,
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

These are exactly the owner identifications verified in Section 8.2
of C1092-DIRECT-WALL-POINT.md. The original northwest marker is
owned, respectively, by Q_7,Q_4,Q_5,Q_6; hence its exclusion
in each local C_i is an actual distinct-owner exclusion. All local
strict anchors and actual container walls used above are carried by
the same quarter-turn chart.

For every i, a missing local P_i forces (1). If m of the four
central canonical angles are nonpositive and all four wall points
are missing, Theorems 1–2 give the sharper sum

    sum_i(C_ix+C_iy)>12+3m/20.                     (23)

The displacement statement is therefore proved without a boundary
angle bound, a central center enclosure, or an assumption that the
adjacent central gap has a preferred sign.

Equation (23) is a necessary condition, not yet a complete contradiction
for arbitrary mixed or positive central angles. The remaining task is
to combine this displacement with the actual adjacent central and
preceding boundary supports, or prove a suitable global replacement
for it. A point-only exclusion of D=(1,2) is not silently substituted
for the actual preceding boundary square. The three-square example
in the cited note remains compatible with this theorem: its central
center has coordinate sum strictly greater than 3.

## 7. A strict radius bound in a negative missing-point sector

The next result uses one more original auxiliary exclusion,

    F_0=(1,113/50) is outside C.                    (24)

This is an actual owner exclusion in every local chart: the preceding
boundary owns F_0 because its original strict point (87/50,1)
becomes R^(-1)(87/50,1)=(1,113/50). In particular (24) does not
depend on whether that preceding boundary owns its additional P.

### Theorem 3

Under the original local hypotheses, suppose P is missing and C has
a nonpositive canonical angle. Its center satisfies

    |C-(2,2)|<1/sqrt(2).                           (25)

The theorem covers the entire nonpositive canonical angle interval.
It has no boundary-angle hypothesis and requires only a>1, with no
upper bound on a.

### Proof

Use the notation of Section 3.1. The two comparisons with a strict point

    u_C·U_0-u_C·F_0=13s/25>=0,
    v_C·F_0-v_C·U_0=13c/25>0

show that F_0's upper-u_C and lower-v_C inequalities are strict;
only its lower-u_C and upper-v_C exits remain. If it left through
upper v_C, the forced lower-v_C exit of H from (11) would imply

    a<=v_C·F_0-v_C·H=19c/25<1,

a contradiction. Thus

    U_C>=c-113s/50.                               (26)

Write the two projections of the center displacement C-(2,2) as
delta_u,delta_v. Equations (11),(12),(26) and strict ownership of
U_0 give

    a/2-c-13s/50<=delta_u<a/2-c+13s/50,
    a/2-s-c/2<=delta_v<=7(c-s)/20-a/2<0.           (27)

The final strict sign follows from a>1 and c-s<=1.

Put

    A=c+13s/50-a/2,       B=s+c/2-a/2.

The side bound a<=17c/20+13s/20 from (12) gives

    A>=23c/40-13s/200>0,
    B>=3c/40+27s/40>0,
    a<=3c/2<2c.

In particular the upper endpoint for delta_u in (27) is at most
A: this is precisely a<=2c. Its lower endpoint is -A.
Thus |delta_u|<=A. Likewise (27) gives |delta_v|<=B.
Since a>1 and A,B>0,

    |C-(2,2)|^2
      <=A^2+B^2
       <(c+13s/50-1/2)^2+(s+c/2-1/2)^2.           (28)

Here is an exact continuous proof that the final expression is less
than 1/2 for every c>=s>=0 on the unit circle. Set r=s/c in [0,1]
and define

    A_0(r)=5/4+(38/25)r+(2669/2500)r^2,
    B_0(r)=3/2+(63/50)r.

Expanding the proposed squared bound shows that it is equivalent to

    A_0(r)<B_0(r)sqrt(1+r^2).

Both sides are positive. Their squared difference has the following
exact expansion in nonnegative factors:

    B_0(r)^2(1+r^2)-A_0(r)^2
      =(11/16)(1-r)^4
       +(273/100)r(1-r)^3
       +(1827/625)r^2(1-r)^2
       +(29403/31250)r^3(1-r)
       +(793791/1562500)r^4>0.                    (29)

At each r in [0,1] at least one displayed term is strictly positive.
Thus the scalar bound holds throughout the interval, and (28)
proves (25).

## 8. Excluding the all-negative cycle of four missing wall points

### Theorem 4

In the original last C1092 assignment, all four boundary points cannot
be missing simultaneously if all four canonical central angles are
nonpositive. At least one actual B_i strictly owns its local P_i.

### Proof

Suppose all four P_i are missing. Theorem 3 applies in all four
charts, using the original preceding-boundary ownership for (24).
Each quarter-turn chart fixes the physical point O=(2,2). Therefore
all four actual central centers lie strictly in the disk of radius
1/sqrt(2) about O.

Four points strictly inside that disk have a pair at distance less
than 1. If one point is O, this is immediate. Otherwise order their
polar arguments about O. One consecutive angular gap is at most
pi/2. For that pair with radii r_1,r_2<1/sqrt(2), the cosine rule
gives

    distance^2=r_1^2+r_2^2-2r_1r_2 cos(gap)
              <=r_1^2+r_2^2<1.

On the other hand, each open side-a square contains its open
concentric disk of radius a/2. Distinct actual central squares have
disjoint interiors, so their centers have pairwise distance at least
a>1. This contradicts the pair just obtained.

This is a genuine global obstruction using all four actual central
owners. It excludes the all-negative case of four missing wall points;
it does not assert that a single missing point is impossible, that
every wall point is forced once one is owned, or that the arbitrary
positive or mixed-sign cycle is already closed.

## 9. A stronger positive diagonal inequality

### Theorem 5

In the setting of Theorem 2, the stronger inequality is

    C_x+C_y>2+c+s/(2c).                            (30)

It holds for every positive canonical central angle and every
boundary orientation. As before all three actual separating-face
sources are retained.

### Proof

Keep the notation of Section 5, and put

    k=c-1+s/(2c)=B_0/c>=0.

We strengthen each of the three already established estimates by k.
Their strictly positive coefficients of a-1 are unchanged, so it
suffices to refine their a=1 scalar bounds.

For the central source v_C, the excess in (16), denoted by Delta,
satisfies the exact identity

    Delta-k
      =h^3(1-2h-h^2)(1+2h-h^2)
          /[(1-h^2)(1+h^2)^2]>=0.                 (31)

Both factors in the numerator are nonnegative for
0<=h<=sqrt(2)-1; the denominator is positive. This proves (30)
for that source.

For the boundary source v_B, subtract k from (18). Since
p=1/sqrt(1+r^2), exact simplification gives

    S_1-3-k
      ={M_*/(c-rs)}
         {r[1-r-s/(2c)]+(1+r)[sqrt(1+r^2)-1]}.    (32)

Here M_*>=0 and c-rs>0. As s/c<=1, the braced expression is
at least

    r(1/2-r)+(1+r)[sqrt(1+r^2)-1]>0.

To prove this last assertion for every r>0, compare the positive
quantities sqrt(1+r^2) and (1+r/2+r^2)/(1+r). The difference
of their squares, after multiplying by (1+r)^2, is exactly

    (1+r^2)(1+r)^2-(1+r/2+r^2)^2
      =r(4r^2-r+4)/4>0.

The quadratic is positive, for instance because its discriminant is
1-64<0. This proves (32) is nonnegative and hence (30).

Finally consider -u_B and the scalar J of (20). Keep
A=qc+ps, D_*=pc-qs, and t=q/(1+p). The following exact
differences are simpler than a separate estimate of J:

    J-kA=M_*[1-t+kp-sq],          if D_*>=0,
    J-kA=M_*[1-t-(1-s/(2c))p],   if D_*<=0.        (33)

In the second regime let r_c=s/c. The condition D_*<=0 is

    r_c>=p/q=(1-t^2)/(2t).

Using p=(1-t)(1+t)/(1+t^2), the second bracket in (33) equals

    (1-t)[t^2-t+(r_c/2)(1+t)]/(1+t^2)
      >=(1-t)^3(1+3t)/[4t(1+t^2)]>=0.            (34)

All denominators are positive. In the first regime the bracket
1-t+kp-sq is nonincreasing as the boundary angle increases:
t increases, p decreases, q increases, and k,s>=0. Its minimum
is therefore at D_*=0, where (34) applies. This proves J>=kA
in both regimes. Equation (19) and its positive a-1 coefficient
complete (30) for the final actual source.

## 10. The radius bound for a positive missing-point sector

Besides F_0=(1,113/50), retain the original auxiliary exclusion

    B_L=(8/5,1) is outside C.

The owner of B_L is the actual B in the same sector; the owner of
F_0 is the actual preceding boundary, as explained in Section 7.
These two exclusions are original ownership facts, independent of
whether either boundary owns its additional P.

### Theorem 6

Under the original local hypotheses, suppose P is missing and C has
a positive canonical angle. Then

    |C-(2,2)|<1/sqrt(2).                           (35)

There is no boundary-angle restriction and no upper bound on a.

### 10.1. Direct face and center bounds

The excluded B_L is forced through lower v_C. Indeed,

    u_C·B_L-u_C·L_0=3(c-s)/5>=0,
    u_C·M-u_C·B_L=(c+13s)/20>0,
    v_C·L_0-v_C·B_L=3(c+s)/5>0.

The comparison points are all strict in C. The excluded F_0 is
forced through upper v_C, because

    u_C·F_0-u_C·L_0=33s/50>0,
    v_C·F_0-v_C·U_0=13c/25>0,
    u_C·T-u_C·F_0=(37c-13s)/50>0.

Consequently

    V_C>=c-8s/5,       V_C+a<=113c/50-s,
    a<=63c/50+3s/5.                               (36)

Let delta_u,delta_v be the two projections of C-(2,2) in its
positive canonical frame. The forced H lower-u face (13), strict
ownership of L_0, and (36) imply

    a/2-c-s/2<=delta_u<a/2-c-2s/5<0,
    a/2-c+2s/5<=delta_v<=13c/50+s-a/2.             (37)

For the final strict sign in the first line, use (36):
a/2-c-2s/5<=-37c/100-s/10<0.

Put

    A=c+s/2-a/2>0,
    A_1=c+s/2-1/2,
    B_1=c-2s/5-1/2,
    D_1=13c/50+s-1/2.

The positivity of A follows from (36), which gives
A>=37c/100+s/5>0. We now distinguish only the sign of delta_v.

### 10.2. Nonnegative second center projection

If delta_v>=0, equations (37) give

    0<-delta_u<=A<A_1,
    0<=delta_v<=13c/50+s-a/2<D_1.

Thus

    |C-(2,2)|^2<A_1^2+D_1^2<1/2.                 (38)

Here is an exact scalar verification of the last inequality. With
r=s/c in [0,1], define

    A_+(r)=2669/2500+(38/25)r+(5/4)r^2,
    B_+(r)=63/50+(3/2)r.

Expansion shows that A_1^2+D_1^2<1/2 is equivalent to
A_+(r)<B_+(r)sqrt(1+r^2). Both sides are positive, and

    B_+(r)^2(1+r^2)-A_+(r)^2
      ={2798939(1-r)^4
          +14536356r(1-r)^3
          +19679184r^2(1-r)^2
          +6820056r^3(1-r)
          +3175164r^4}/6250000>0.                (39)

Every coefficient is positive, and at least one summand is nonzero
at every point of [0,1]. This proves (38).

### 10.3. Nonpositive second center projection

If delta_v<=0, set

    x=-delta_u>0,       y=-delta_v>=0,
    L=c+s,             M_*=c-s,
    J_0=2-c-s/(2c).

Here J_0>=1/2>0, because c<=1 and s/c<=1. Equation (37)
and a>1 give

    x<=A_1,       y<=B_1.

The strengthened diagonal theorem (30) is exactly

    Lx+M_*y<J_0.                                  (40)

We claim the two continuous scalar bounds

    2J_0 A_1<=L,       2J_0 B_1<=M_*.              (41)

They imply immediately

    x^2+y^2<=A_1x+B_1y
             <=(Lx+M_*y)/(2J_0)<1/2,

which proves (35) in the remaining sign case. If B_1<0, the
case itself is impossible, so the use of y<=B_1 has no hidden
negative-bound issue.

For completeness, both inequalities in (41) have exact elementary
proofs on the full canonical interval. Put h=s/(1+c), where
0<=h<=sqrt(2)-1<1/2. Direct substitution gives

    L-2J_0 A_1
      =h[1+3h(1-h)+7h^3+8h^4]
             /[(1+h)(1+h^2)^2]>=0.               (42)

For the second one,

    M_*-2J_0 B_1
      =h R(h)/[5(1-h^2)(1+h^2)^2],
    R(h)=3-8h+6h^2+32h^3-29h^4-40h^5.            (43)

Let z=2h in [0,1]. The exact positive expansion

    R(h)=3(1-z)^5+11z(1-z)^4
          +(31/2)z^2(1-z)^3+(29/2)z^3(1-z)^2
          +(155/16)z^4(1-z)+(23/16)z^5>0          (44)

proves the sign in (43). Its endpoint values are also positive.
Equations (42)–(44) prove (41), completing Theorem 6.

## 11. An all-sign global obstruction to four missing wall points

### Theorem 7

In the original last C1092 assignment, at least one of the four actual
boundary owners B_i strictly owns its local P_i. This holds for every
choice of the four canonical central angles and every choice of the
boundary and corner angles.

### Proof

If all four P_i were missing, each actual central center would lie
strictly in the disk of radius 1/sqrt(2) about the physical point
O=(2,2): use Theorem 3 for a nonpositive central angle and Theorem 6
for a positive one. Every extra point used in those theorems is an
original strict point of the same or preceding actual boundary owner,
so no P_i was assumed in proving these radii.

Apply the four-center disk argument from Theorem 4. Two of the
centers would be less than 1 apart, whereas the actual disjoint
side-a central squares require center separation at least a>1.
This is a contradiction.

The conclusion is a simultaneous four-sector statement. It is stronger
than a conditional local transfer and includes mixed central signs.
The remaining P/D entrance question is now propagation: starting
with a boundary that owns P, prove that a later sector cannot lose
its P while retaining all the actual adjacent-owner supports, or
derive a direct contradiction from such a transition. That further
step is not claimed here.

**Subsequent all-negative completion.**
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md)
proves that two adjacent nonpositive central angles force the next
central to own H, hence its boundary to own P. Applying this in all
four sectors and then using the full-angle owned-point disk theorem
excludes the entire all-nonpositive configuration. Thus the general
propagation question above remains relevant to positive and mixed
signs; no unresolved all-negative transition is being asserted.
