# C1092: D is excluded even after a missing positive wall point

All terminating decimals are exact rationals. Strict ownership is in
an actual open square. Exclusion includes equality on any actual
face. The common side is a>1; there is no upper side bound or angle
magnitude hypothesis.

## 1. The positive-recipient two-central theorem

Let R(x,y)=(4−y,x). Let C,J be two disjoint actual open squares of
side a>1, and write C⁺=R⁻¹(J). Their local canonical frames are
positive:

    C:   u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1;
    C⁺:  u⁺=(d,t),v⁺=(−t,d),d≥t≥0,d²+t²=1.

Suppose each local square strictly owns

    M=(1.65,1.65), U₀=(1,1.74),
    L₀=(1,1.6),   T=(1.74,2),

and C excludes

    H=(1,1.5), N=(1.65,2.35),
    W=(.914,2), F₀=(1,2.26).                       (1)

**Theorem 1.** C⁺ does not strictly own D=(1,2).

The negative-recipient version is Theorem 1 of
[C1092-MIXED-NEGATIVE-DISK.md](C1092-MIXED-NEGATIVE-DISK.md).
The present theorem completes both signs of the recipient without
assuming any boundary P ownership.

## 2. The predecessor's forced faces and two regimes

Write C's bands as U<u·X<U+a, V<v·X<V+a. The positive H face
argument gives

    U≥c+1.5s=:h.                                   (2)

Here is its short complete justification. Both upper bands at H
are strict by L₀. If H were lower-v, strict M would give s/c<3/13.
In that range N has its lower-u, lower-v and upper-u bands strict
by U₀,M,T; for the last comparison use .09c−.35s>0. Thus N would
be upper-v, and a≤.85c−.65s<1. Hence H must be lower-u, as in (2).

At F₀, the lower-u, upper-u and lower-v bands are strict by U₀,T,U₀,
since their relevant projection differences are .52s, .74c−.26s,
and .52c. Therefore

    V+a≤2.26c−s=:f₀.                               (3)

At W, the upper-u and lower-v bands are strict by T,L₀, since
u(T)−u(W)=.826c>0 and v(W)−v(L₀)=.4c+.086s>0. This gives two
exhaustive regimes:

**Regime I:** W is lower-u. Comparison of U≥.914c+2s with the
strict L₀ gives

    s/c<43/200,       c>.97,       s<.22.           (4)

Use f=f₀ in this regime.

**Regime II:** W is upper-v. In this regime use

    V+a≤2c−.914s=:g,
    f=g.                                           (5)

Both regimes allow a point on more than one excluding face. Define
the following exact coefficients according to the applicable regime:

| Regime | A | B |
|---|---|---|
| I | c+s−1−.76cs | c−s−.76c²+.24 |
| II | c+s−1−.5cs−.086s² | c−s−.5c²−.086cs+.24 |

They satisfy

    A≥0 in both regimes;
    B<.74 in Regime I,      B≤.74 in Regime II.      (6)

Indeed c+s−1=2cs/(c+s+1) and 2/(c+s+1)>.8. Therefore
A≥.04cs in I and A≥.3cs−.086s²≥.214cs in II. Also
c−.5c²≤.5 on 0≤c≤1. For B in Regime I, the remaining terms
−.26c²−s give strict inequality B<.74; in II they give B≤.74.
Two additional facts will be used below:

    Regime I:  B≥c−s−.52>.23;                      (7)
    Regime II: As+Bc=1−1.086s−.26c>0.               (8)

Equation (7) follows from (4). Equation (8) is an exact identity
using c²+s²=1, and its strict sign follows from

    .26c+1.086s≤1.346/sqrt(2)<1.

## 3. Actual normals and two immediate source exclusions

Suppose, for contradiction, that C⁺ strictly owns D. Then J
strictly owns P=R(D)=(2,1), T_J=R(T)=(2,1.74), and
M_J=R(M)=(2.35,1.65). Reindex its physical positive frame as

    u_J=(d,t),       v_J=(−t,d).

Strict M,M_J and T,T_J force any separating normal from C toward J
to satisfy n_x>0 and n_x−n_y>0. Among actual face normals this
leaves at most

    u,       −v,       u_J,       −v_J.             (9)

Some of these cease to be eligible at canonical endpoints; retaining
them in the proof creates no extra assumption. Since P,T_J are
strict in J, every nonzero n satisfies

    lower_J(n)<n·P,
    lower_J(n)<n·T_J.                              (10)

The source u is impossible, since

    upper_C(u)=U+a≥c+1.5s+a>2c+s=u·P.

The last inequality uses a>1≥c−.5s. The source −v is also
impossible. In Regime I,

    upper_C(−v)−(−v)·T_J
      ≥a−.52c−s>1−.52−.22>0.

In Regime II the difference is at least

    a−.26c−1.086s>0,

by (8)'s strict scalar bound. Thus only the recipient sources u_J
and −v_J remain. We keep both possible angle orders.

## 4. The source u_J in both angle orders

Let θ,ψ∈[0,π/4] be the angles of C,J and put

    K=cd+st=cos(ψ−θ)>0,
    L=|ct−sd|=|sin(ψ−θ)|≥0.

### 4.1. If ψ≥θ

Then u_J=K u+L v. From (2) and strict T,

    upper_C(u_J)
      =K(U+a)+L(V+a)
      ≥K(h+a)+L v(T).

Subtract u_J·P=K u(P)+L v(P). The resulting lower bound is

    K(a−c+.5s)+L(c+.26s)>0.                        (11)

The first term is strictly positive because K>0 and a>1; the
second is nonnegative. By (10), u_J cannot separate the squares.

### 4.2. If ψ≤θ

Now u_J=K u−L v. Equations (2),(3) or (5) give

    upper_C(u_J)≥Kh−Lf+a(K+L).

At a=1 the difference from u_J·P=2d+t is exactly

    Kh−Lf+(K+L)−(2d+t)
      =Ad+(.74−B)t.                               (12)

Both terms on the right are nonnegative by (6). Since a>1 and
K+L>0, the actual support is strictly greater than u_J·P. This
also excludes u_J. Equal angles are covered by either argument.

## 5. The source −v_J in both angle orders

### 5.1. If ψ≥θ

Then −v_J=L u−K v, so

    upper_C(−v_J)≥Lh−Kf+a(K+L).

At a=1, its difference from (−v_J)·T_J=2t−1.74d is exactly

    Lh−Kf+(K+L)−(2t−1.74d)=At+Bd.                (13)

In Regime I this is positive by A≥0 and (7). In Regime II,
the order ψ≥θ gives t/d≥s/c. Thus (6),(8) give

    At+Bd≥(d/c)(As+Bc)>0.                          (14)

The actual a>1 only increases the support. This contradicts (10).

### 5.2. If ψ≤θ

Here −v_J=−L u−K v. Use strict L₀ and V≤f−a to get

    upper_C(−v_J)≥aK−L u(L₀)−Kf.

Comparison with T_J yields

    upper_C(−v_J)−(−v_J)·T_J
      ≥K[a+v(T_J)−f]+L[u(T_J)−u(L₀)].            (15)

The second bracket is c+.14s>0. The first is a−.52c−s in
Regime I and a−.26c−1.086s in Regime II. Both are strictly
positive by the estimates already used in Section 3. Since K>0,
the difference in (15) is strictly positive. Again (10) excludes
the proposed separator.

Every actual face-normal source in (9) has now been ruled out.
The actual squares cannot be disjoint while J strictly owns P.
Equivalently C⁺ excludes D. This proves Theorem 1. ∎

## 6. Exact global D transfer

**Theorem 2.** In the original last C1092 assignment, every central
square excludes its local D, for arbitrary canonical signs.

Fix a sector j. If the preceding actual boundary owns its local P,
that point is the genuine foreign D_j in the current chart, so D_j
is excluded.

If the preceding boundary misses P, the predecessor-sign H theorems
show that the preceding central must be strictly positive. The
contrapositive of the all-angle paired-corner transfer gives H
strictly in that preceding sector's actual corner, and hence H
outside its central. More explicitly, for that predecessor C_i,
its local W_i,F₀_i belong strictly to B_(i−1), while its local N_i
belongs strictly to C_(i−1). With i=j−1, these actual owners are
respectively B_(j−2) and C_(j−2). Thus it has all exclusions in (1).
These are original owner facts, with no P premise.

If the recipient central is positive, apply Theorem 1. If it is
nonpositive, apply its already proved counterpart in
[C1092-MIXED-NEGATIVE-DISK.md](C1092-MIXED-NEGATIVE-DISK.md).
Either theorem supplies precisely D_j excluded. The two boundary
ownership alternatives are exhaustive, including equality at a
boundary face in the missing alternative. This proves Theorem 2. ∎

## 7. Direct angle entrance for the entire all-positive sector

**Corollary.** In an all-positive original last C1092 cycle,

    0<tan(θ_i/2)<7/32 for all four central sectors.  (16)

No boundary P ownership hypothesis is required in this corollary.

Indeed Theorem 2 supplies D excluded at every central. For a positive
central, D upper-v and the original E exclusion force

    V+a≤2c−s,       U+a≤2c+1.74s.

The original actual point (1.6,1) is lower-v. Apply these genuine
faces to each consecutive positive pair. Their quarter-turn images
are exactly the four actual caps in Theorem 1 of
[C1092-POSITIVE-ADJACENT-ANGLE.md](C1092-POSITIVE-ADJACENT-ANGLE.md).
That theorem needs the caps themselves, so it applies equally when
D was supplied by the present two-central exclusion instead of by
a boundary owner. It gives (16) at every sector.

The result completes the D and central-angle entrance for the full
all-positive sector, including cycles with missing P. It does not
assert that the boundary P points are all owned or that the remaining
all-positive cyclic obstruction has already been completed.
