# C1092: a negative central square receives H from either predecessor sign

All terminating decimals are exact rationals. Owned points are strict
in their actual open squares; exclusions and separating supports may
be equalities. There is no angle-magnitude hypothesis or upper bound
on the common side.

## 1. The positive-to-negative two-central theorem

Let R(x,y)=(4−y,x). Let C and J be disjoint actual open squares of
common side a>1, and let C⁺=R⁻¹(J) denote the local copy of the second
owner. Suppose their local canonical frames have the indicated signs:

    C:   u=(c,s),  v=(−s,c),   c≥s≥0, c²+s²=1;
    C⁺:  u⁺=(d,−t), v⁺=(t,d), d≥t≥0, d²+t²=1.

Suppose both local squares strictly own

    M=(1.65,1.65), U₀=(1,1.74),
    L₀=(1,1.6),   T=(1.74,2),

and C excludes

    A=(1,1), W=(.914,2), F₀=(1,2.26).               (1)

**Theorem 1.** C⁺ strictly owns its local point H=(1,1.5).

The theorem has no premise concerning any boundary P or central D.

## 2. The predecessor faces and the three exhaustive regimes

Write C's bands as U<u·X<U+a, V<v·X<V+a. At F₀, the lower-u,
upper-u and lower-v bands are strict, respectively, by U₀,T,U₀:

    u(F₀)−u(U₀)=.52s≥0,
    u(T)−u(F₀)=.74c−.26s>0,
    v(F₀)−v(U₀)=.52c>0.

Hence its exclusion forces the unconditional cap

    V+a≤2.26c−s=:f₀.                               (2)

At A both upper bands are strict by M,L₀, so A is lower-u or
lower-v. At W the upper-u and lower-v bands are strict by T,L₀,
since

    u(T)−u(W)=.826c>0,
    v(W)−v(L₀)=.4c+.086s>0.

Thus W is lower-u or upper-v. These alternatives give three
exhaustive continuous regimes:

**Regime I:** U≥c+s.

**Regime II:** U<c+s and W is lower-u. Here

    U≥.914c+2s=:w,
    s<.086c,       c>.99,       s<.09.              (3)

The angle bounds follow from .914c+2s<c+s and c²+s²=1.

**Regime III:** U<c+s and W is upper-v. Since A cannot be lower-u,
it is lower-v. Therefore

    V≥c−s,       V+a≤2c−.914s=:g,
    1<a≤c+.086s.                                   (4)

Writing q=s/(1+c), the identity

    c+.086s−1=2q(.086−q)/(1+q²)

gives 0<q<.086. In particular

    c>.98,       s<.18.                             (5)

For instance c=1−2q²/(1+q²)>1−2(.086)²>.98,
and s=2q/(1+q²)<.172<.18. If W lies on two excluding faces,
either applicable regime may be used.

## 3. The missing-H cap and the actual normal sources

Suppose H is outside C⁺. Exactly as in Section 3 of
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md),
its other three bands are strict by L₀,M, so it is lower-v⁺.
Reindex the physical frame of J as

    u_J=(d,−t),       v_J=(t,d),

and write its lower bands as 𝒰,𝒱. The missing-H face becomes

    𝒰+a≤2.5d−t=:h.                                 (6)

The physical strict points U_J=(2.26,1), T_J=(2,1.74) imply

    𝒱<d+2.26t=:r,
    𝒱+a>1.74d+2t=:z.                               (7)

The strict marker pair and the strict T,T_J pair force any actual
separating normal from C toward J to satisfy n_x>0 and n_x−n_y>0.
For the two present frames this leaves only

    u=(c,s),       −v=(s,−c),       u_J=(d,−t).       (8)

At an axis endpoint an ineligible listed direction may disappear;
including it in the inequalities below only strengthens the argument.
There are no other sources from either actual square.

Put

    K=cd−st≥0,       L=ct+sd≥0,       K²+L²=1.

The projection relations are

    u=K u_J+L v_J,
    −v=L u_J−K v_J,
    u_J=K u−L v.

## 4. One separating source is impossible in every regime

Consider n=−v. From (2), upper_C(−v)=−V≥a−f₀. From (6),(7),

    lower_J(−v)=L𝒰−K(𝒱+a)≤L(h−a)−Kz.

Separation would imply

    a(1+L)≤1.26c+1.5s−K(.74d−.5t).                (9)

The right side of (9), subtracted from 1+L, equals

    1−Ac−Bs,
    A=.52−t+.74t²+.5dt,
    B=1−d+.5d²+.74dt.                              (10)

We prove Ac+Bs<1 over both complete canonical sectors. First
A≤.52, since .74t+.5d≤sqrt(.7976)<1. Also B≥.5>0.
If A≥B, then

    Ac+Bs≤.52(c+s)≤.52 sqrt(2)<1.

If B≥A, the function A cos θ+B sin θ is nondecreasing for
0≤θ≤π/4, because its derivative is
B(cos θ−sin θ)+(B−A)sin θ≥0. Thus

    Ac+Bs≤(A+B)/sqrt(2).

Write w₁=d+t, z₁=d−t≥0. Directly,

    A+B=1.52−w₁+.62w₁²−.12w₁z₁
        ≤1.52−w₁+.62w₁²
        ≤2.76−sqrt(2)<sqrt(2).

The quadratic is increasing for 1≤w₁≤sqrt(2), and its last
comparison uses 1.38<sqrt(2). Hence Ac+Bs<1 in this case as well.
Equation (9) is impossible for a>1. This removes −v for all three
regimes at once.

## 5. Regime I: the lower-u face at A

### 5.1. Source u

Using U≥c+s and (6),(7), separation on u would imply

    a(1+K)≤1.5c−.24Lt.                              (11)

Here K h+Lr=2.5c+s−.24Lt. The difference between 1+K and
the right side of (11) is

    1−A₁c−B₁s,
    A₁=1.5−d−.24t²<.8,
    B₁=t(1−.24d)<104/175<.6.

Indeed d>7/10 and t<5/7 throughout the canonical sector.
Therefore A₁c+B₁s<.8c+.6s≤1, a contradiction.

### 5.2. Source u_J

The exact upper support and (2) give

    upper_C(u_J)=K(U+a)−LV
                ≥K(c+s)−Lf₀+a(K+L).

Separation and (6) would imply

    a(1+K+L)≤1.5d+1.26cL.                          (12)

Subtract its right side from 1+K+L. The result is

    1−A₂d−B₂t,
    A₂=1.5−c−s+1.26cs,
    B₂=s−c+1.26c².

With w₂=c+s∈[1,sqrt(2)],

    A₂=.87−w₂+.63w₂²≤2.13−sqrt(2)<.72.

The quadratic increases on that interval. Also

    B₂−.63=(c−s)[.63(c+s)−1]≤0.

Consequently

    A₂d+B₂t≤.72d+.63t≤sqrt(.9153)<1.

This contradicts (12). Together with Section 4, Regime I has no
possible separator.

## 6. Regime II: the shallow lower-u face at W

Here U≥w=.914c+2s and the explicit bounds (3) apply.

### 6.1. Source u

Separation on u and (6),(7) would give

    a(1+K)≤1.586c−s−.24Lt≤1.586.                   (13)

But K=cd−st>.99·.7−.09=.603, so 1+K>1.603.
This contradicts (13).

### 6.2. Source u_J

Using U≥w and (2), separation on u_J would imply

    a(1+K+L)≤1.586d+t+L(.26c−.086s).              (14)

The difference between 1+K+L and this right side equals

    1−A₃d−B₃t,
    A₃=1.586−c−s+.26cs−.086s²,
    B₃=1+s−c+.26c²−.086cs.

From (3), A₃<.596<.60 and B₃<.36. Hence

    A₃d+B₃t≤.60d+.36t≤sqrt(.4896)<1,

contradicting (14). Section 4 already removed the third source.

## 7. Regime III: the shallow upper-v face at W

Now the cap V+a≤g=2c−.914s and bounds (5) hold. The strict point
T gives U+a>u(T)=1.74c+2s.

### 7.1. Source u

Comparing that strict upper support with the upper bound for
lower_J(u) from (6),(7), separation would imply

    aK<.76c−s−.24Lt.                               (15)

However

    K+.24Lt−.76c+s
      =c[d+.24t²−.76]+s[1−t+.24dt]>0.

The second bracket is nonnegative. In the first, use t²=1−d²:
d−.24d²−.52 increases for 0≤d≤1, so for d>.7 it is greater
than .7−.24(.7)²−.52=.0624. Thus K is already larger than the
right side of (15), contradicting a>1 and K≥0.

### 7.2. Source u_J

The strict T band and upper-v cap at W give

    upper_C(u_J)≥K u(T)−L g+aL.

Separation and (6) would imply

    a(1+L)≤.76d+t+.826Ls.                           (16)

By (5), 1−.826s>0 and

    c(1−.826s)>.98(1−.826·.18)>.83.

Since L=sd+ct≥ct,

    1+L−[.76d+t+.826Ls]
      ≥1−.76d−.17t
      ≥1−sqrt(.6065)>0.

This contradicts (16). Section 4 removes −v here too.

All regimes and all actual normal sources have been excluded.
Therefore H cannot be outside C⁺: it is strict in that actual
central owner. This proves Theorem 1. ∎

## 8. Consequence for every negative central in an arbitrary sign cycle

The owner mapping is the same as in Section 6 of
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md):
W and F₀ are strict in the actual preceding boundary B_(i−1),
from its original marker and auxiliary point. The additional
excluded A=(1,1) belongs to the actual paired corner K_i by the
retained paired-corner inner-point theorem. No P premise is used.

**Corollary.** In the original last C1092 MPPM assignment, every
central square with nonpositive canonical angle strictly owns its
local H=(1,1.5), regardless of the signs of the other three centrals.
Its corresponding actual boundary square therefore strictly owns
its local P=(2,1).

To prove the corollary, consider that negative central's actual
predecessor. If the predecessor is nonpositive, apply the completed
negative-to-negative theorem. If it is nonnegative, apply Theorem 1
above. At zero either theorem is available. In both cases the strict
H lies in the negative central; its distinct corner owner excludes H.
Theorem 7 of
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md) then forces P
in the actual boundary square for every boundary orientation.

Thus a missing P in the original four-sector assignment can occur
only at a strictly positive central angle. This is a proved global
restriction obtained from actual adjacent owners, not a terminal
angle history or an assumed sign propagation. It does not by itself
force P at the remaining positive centrals. ∎
