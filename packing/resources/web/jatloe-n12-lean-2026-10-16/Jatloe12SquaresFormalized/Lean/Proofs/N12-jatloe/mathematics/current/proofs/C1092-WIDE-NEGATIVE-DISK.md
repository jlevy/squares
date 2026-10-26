# A wider direct negative disk lemma for C1092

All decimals below are exact rationals. Square ownership is strict;
excluded points and support comparisons permit equality.

## 1. The local theorem

### Theorem 1

Let C and B be distinct open squares of a common side a>1 with
disjoint interiors. Suppose that C has canonical normals

    u=(c,-s),       v=(s,c),
    c=(1-q^2)/(1+q^2),       s=2q/(1+q^2),
    0<=q<=1/4.

Suppose C strictly owns

    U_0=(1,87/50),       T=(87/50,2),

and excludes

    D=(1,2),             L=(8/5,1),
    E=(2,87/50),         N=(33/20,47/20),
    F=(2,113/50).

Suppose the actual B strictly owns L and P=(2,1). Then the center
C_0 of C satisfies

    |C_0-(2,2)|<1/sqrt(2).                        (1)

No center enclosure, boundary-angle bound, or upper bound on a is
needed. The theorem has a point-exclusion premise for D and an actual
whole-owner premise for the horizontal segment from L to P.

## 2. Direct forced faces

Write C's lower face values as U,V. The original point comparisons
force

    U>=c-2s,              U+a<=2c-87s/50,
    V>=c+8s/5,            V+a<=33s/20+47c/20,
                            V+a<=2s+113c/50.       (2)

Here are all alternatives, without any imported center bound.

The excluded D has its upper-u and lower-v bands strict by U_0;
its upper-v band is strict by T. Thus D is lower-u. The excluded
E has both lower bands strict by U_0, and its upper-v band is
strict by T, since v(T)-v(E)=13(c-s)/50>=0. Thus E is upper-u.

At L the lower-u and upper-v bands are strict by U_0, because

    u(L)-u(U_0)=3c/5+37s/50>0,
    v(U_0)-v(L)=37c/50-3s/5>0.

If L exited through upper u, its cap and D's floor would imply

    a<=u(L)-u(D)=3c/5+s
      =1-2(1-q)(1-4q)/[5(1+q^2)]<=1,

a contradiction. Hence L exits through lower v. The endpoint
q=1/4 is included: the last quantity equals 1 there, still less
than a.

At N the lower-u, upper-u, and lower-v bands are strict by
U_0,T,T respectively:

    u(N)-u(U_0)=(65c-61s)/100>0,
    u(T)-u(N)=(9c+35s)/100>0,
    v(N)-v(T)=(35c-9s)/100>0.

These inequalities hold throughout c>=s>=0. Thus N is upper-v.

At F the lower-u band is strict by T and the lower-v band is
strict by U_0. D's lower-u floor also gives

    u(F)-U<=u(F)-u(D)=c-13s/50<=1<a,

so the upper-u band is strict. Hence F is upper-v, completing (2).

If s=0, the forced D lower-u face already contradicts strict U_0
with the same u coordinate. Retaining zero in subsequent weak
estimates is harmless and makes the scalar identities continuous.

## 3. The lowest vertex clears the whole actual boundary segment

Let Z be the lowest vertex of C's closure. Its coordinates in terms
of the center are

    Z_x=C_0x+(a/2)(c-s),
    Z_y=C_0y-(a/2)(c+s).

The two lower-face inequalities in (2) give

    C_0x>=1+(3/5)s^2-cs+(a/2)(c+s),

and consequently

    Z_x>=1+(3/5)s^2-cs+ac
        >1+(3/5)s^2+c-cs>=8/5.                    (3)

The final scalar inequality holds exactly on 0<=q<=1/4:

    1+(3/5)s^2+c-cs-8/5
      =2(1-q)^2(1+q)(1-4q)/[5(1+q^2)^2]>=0.     (4)

Suppose Z_y<=1. This vertex is on the upper-u face. Its cap at E
from (2) yields

    c(Z_x-2)<=s(Z_y-87/50)<=0,

so Z_x<=2. Since T=(87/50,2) is strictly in C, the segment
from Z to T meets y=1 at a point W with

    8/5<W_x<=2.

Every point of the closed segment [L,P] is strict in B, because
its two endpoints are strict in the same open convex square.
Thus W lies in the closure of C and in the interior of B. This
contradicts the disjoint open interiors: an interior neighborhood
of B at a closure point of C necessarily contains a point of C.
The argument includes Z_y=1 and contact at P.

Therefore

    C_0y>1+(a/2)(c+s).                            (5)

No orientation or position information about B was used beyond its
actual strict segment and its disjointness from C.

## 4. Direct upper-center bounds and the radius identity

We need only C_0x,C_0y<2, rather than narrow center boxes. The upper-u
and upper-v caps at E,F give

    C_0x<=2+(13/25)cs-(a/2)(c+s)<2.               (6)

Indeed (13/25)cs<=13/50<1/2<=(c+s)/2, and a>1.

The lower-u floor at D and upper-v cap at N give

    C_0y<=47/20-(7/20)s^2+(13/20)cs
                                  -(a/2)(c+s)<2. (7)

For the last inequality, replace a by 1 and subtract 2. The result is

    (7/20)c^2+(13/20)cs-(c+s)/2
      <=(7/20)c+(13/20)s-(c+s)/2
       =3(s-c)/20<=0.

We used c^2<=c and cs<=s; these hold throughout the canonical
quadrant. The strict a>1 makes (7) strict even at an equality in
these scalar estimates. Thus (6),(7) actually hold on the entire
negative canonical angle interval once the indicated faces are known.

Define the reference coordinates

    Y_*=1+(c+s)/2,
    X_*=[c-2s+1/2+sY_*]/c.

Equation (5), a>1, and the lower-u floor at D imply

    C_0y>Y_*,       C_0x>X_*.

Together with (6),(7), both actual coordinates and both reference
coordinates are below 2. Increasing either coordinate toward 2
strictly decreases its squared deficit. Hence

    |C_0-(2,2)|^2<(2-X_*)^2+(2-Y_*)^2<=1/2.       (8)

The final inequality follows from the exact rational identity

    1/2-(2-X_*)^2-(2-Y_*)^2
      =4q^3(1-q)/[(1+q)^2(1+q^2)]>=0.            (9)

For direct checking, the reference coordinates simplify to

    X_*=(q^3+7q^2+q+3)/[2(q+1)(1+q^2)],
    Y_*=(q^2+2q+3)/[2(1+q^2)].

This proves Theorem 1 through q=1/4. Formula (9) itself holds
beyond that interval; the proved lower-v face at L and the vertex
inequality (4), not the radius identity, determine this theorem's
present angle range.

## 5. Exact C1092 application and the remaining transition

In the four charts R^(-i), R(x,y)=(4-y,x), put

    C_i=Q_(4+i),
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

Suppose the central angle in sector i is nonpositive with magnitude
q_i<=1/4. If both B_(i-1) and B_i own their local P, every premise
of Theorem 1 follows from an actual named owner:

| Local datum | Actual owner and source |
|---|---|
| Strict U_0,T in C_i | Original last auxiliary assignment |
| D excluded from C_i | R^(-1) of the preceding B_(i-1)'s strict P |
| L excluded from C_i and strict in B_i | Original local B_i auxiliary |
| P strict in B_i | Stated boundary-point ownership |
| E excluded from C_i | R of the next C_(i+1)'s original T |
| N excluded from C_i | R^(-1) of the preceding C_(i-1)'s original marker |
| F excluded from C_i | R^(-1) of the preceding C_(i-1)'s original T |

Thus C_i's center lies in the disk (1). If all four central angles
are nonpositive with q_i<=1/4 and all four P_i are owned, the
four-center disk argument in C1092-CYCLIC-ENTRANCE.md gives an
immediate contradiction. This is a wider conditional central ending,
not an assertion that all four P_i are already forced on this range.

Combine this theorem with the missing-point radius theorem in that
file. Under q_i<=1/4, a central center is proved to lie inside the
disk whenever its own P_i is missing, or whenever both its preceding
P_(i-1) and its own P_i are owned. Consequently the only sectors
not yet covered by a radius proof are precisely

    P_(i-1) missing,       P_i owned.              (10)

This distinction is necessary: the wall segment at B_i does not by
itself supply the different point D from B_(i-1). The all-sign theorem
in C1092-CYCLIC-ENTRANCE.md supplies at least one owned P, but it
does not eliminate transitions (10). No such elimination is assumed
in the local theorem or its application above.

**Subsequent completion.** The longer actual boundary segment in
[C1092-NEGATIVE-OWNED-POINTS.md](C1092-NEGATIVE-OWNED-POINTS.md)
removes the incoming magnitude restriction from the consecutive-owned
disk argument. The adjacent-central theorem in
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md)
forces every P when all four central signs are nonpositive. Thus the
all-negative transitions discussed in this earlier local reduction
have now been eliminated, and the entire all-negative sector is closed.
