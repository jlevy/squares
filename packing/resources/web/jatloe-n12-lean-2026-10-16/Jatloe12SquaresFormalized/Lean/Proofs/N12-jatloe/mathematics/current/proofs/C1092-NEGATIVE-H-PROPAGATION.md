# C1092: adjacent negative central squares force the corner-transfer point

All terminating decimals in this note are exact rational numbers. Strict
ownership means membership in the actual open square. Exclusions and
separating supports allow equality. The proof uses no angle subdivision,
center enclosure, upper bound on the common side, or incoming boundary
point assumption.

## 1. The two-central theorem

Let R(x,y)=(4−y,x). Let C and J be disjoint actual open squares of the
same side a>1, and put C⁺=R⁻¹(J). Thus C⁺ denotes the local coordinate
copy of the second actual owner. Suppose both local canonical frames
are negative:

    C:  u=(c,−s), v=(s,c),   c≥s≥0, c²+s²=1;
    C⁺ in its own chart:
        u⁺=(d,−t), v⁺=(t,d),   d≥t≥0, d²+t²=1.

Suppose each local square strictly owns

    M=(1.65,1.65), U₀=(1,1.74),
    L₀=(1,1.6),   T=(1.74,2).

Suppose the first square C excludes the three genuine foreign points

    W=(.914,2), F₀=(1,2.26), F=(2,2.26).             (1)

**Theorem 1.** The second square C⁺ strictly owns its local point

    H=(1,1.5).                                      (2)

In particular, the theorem requires no point P in either actual
boundary square and no exclusion of the central point D=(1,2).

## 2. Two unconditional faces of the first central square

Write the strict bands of C as

    U<u·X<U+a,       V<v·X<V+a.

The excluded W has its upper-u band strict by U₀, its lower-v band
strict by L₀, and its upper-v band strict by T. The comparisons are

    u(U₀)−u(W)=.086c+.26s>0,
    v(W)−v(L₀)=.4c−.086s>0,
    v(T)−v(W)=.826s≥0.

The last equality at s=0 is harmless because T is strict. Hence

    U≥u(W)=.914c−2s=:w.                             (3)

The excluded F₀ has its upper-u and lower-v bands strict by U₀:

    u(U₀)−u(F₀)=.52s≥0,
    v(F₀)−v(U₀)=.52c>0.

Consequently it is either lower-u or upper-v. If it is upper-v, then

    V+a≤v(F₀)≤v(F)=2s+2.26c.

If it is lower-u, then U≥u(F₀). At F the lower-u and lower-v bands
are strict by T, since

    u(F)−u(T)=.26(c−s)≥0,
    v(F)−v(T)=.26(c+s)>0.

Its upper-u band is strict as well, because

    u(F)−U≤u(F)−u(F₀)=c≤1<a.

Therefore exclusion of F forces upper-v in this alternative too. In
both alternatives we have the unconditional cap

    V+a≤v(F)=2s+2.26c=:f.                           (4)

Thus (3) and (4) follow from the original three absences in (1), not
from a newly transferred boundary point.

## 3. If H is missing, the second central square has a strong first cap

Assume H is outside C⁺. In its own local frame, its lower-u and
upper-v bands are strict by L₀, and its upper-u band is strict by M:

    u⁺(H)−u⁺(L₀)=.1t≥0,
    v⁺(L₀)−v⁺(H)=.1d>0,
    u⁺(M)−u⁺(H)=.65d−.15t>0.

Hence H can leave only through lower v⁺. If V⁺ is that local lower
face value, then

    V⁺≥t+1.5d.                                     (5)

Now write J=R(C⁺) in the present physical coordinates. Its frame can
be reindexed as

    u_J=(d,−t),       v_J=(t,d).

The strict physical points needed below are

    M_J=(2.35,1.65), U_J=(2.26,1),
    L_J=(2.4,1),     T_J=(2,1.74).

Denote the physical lower face values of J by 𝒰,𝒱, so its strict
bands are 𝒰<u_J·X<𝒰+a and 𝒱<v_J·X<𝒱+a. Because
u_J·R(X)=4d−v⁺·X, (5) gives

    𝒰+a≤2.5d−t=:h.                                 (6)

We will also use only the two strict point comparisons

    𝒱<v_J(U_J)=d+2.26t,
    𝒱+a>v_J(T_J)=1.74d+2t.                         (7)

The notation U_J in (7) names the displayed point, whereas the
calligraphic 𝒰 always denotes the lower face value.

## 4. The exhaustive actual separating-axis ledger

Orient a possible separating normal n from C toward J. The strict
markers M and M_J differ by (.7,0), so n_x>0. The strict points
T and T_J differ by (.26,−.26), so n_x−n_y>0.

For either negative canonical frame, the positive transverse normal
has first component no larger than its second component. It cannot
satisfy the second strict cone inequality. The two backwards normals
have nonpositive first component and cannot satisfy the first one.
This includes the axis and 45-degree endpoints.

Thus the only possible actual separating directions are

    u=(c,−s) supplied by C,
    u_J=(d,−t) supplied by J.                        (8)

Let c=cos θ, s=sin θ, d=cos ψ, t=sin ψ with
0≤θ,ψ≤π/4, and put

    k=cd+st=cos(ψ−θ)>0,
    ℓ=ct−sd=sin(ψ−θ).

The exact projection relations are

    u=k u_J+ℓ v_J,
    u_J=k u−ℓ v.

There are therefore exactly four source/order combinations. The next
section proves that all four contradict separation. In every case
the support inequalities remain weak, so possible tangencies are
included.

## 5. Four continuous separator inequalities

Set

    η=1.586=793/500.

Two elementary estimates will be used repeatedly. First,

    (.886)²+(.3)²=218749/250000<1.                   (9)

Second, for nonnegative x,y with x²+y²=1,

    ηx+y≤sqrt(η²+1)<1.9,

because η²+1=878849/250000<902500/250000=(1.9)².
Consequently, for every γ∈[0,π/4],

    .9 cos γ+.26 sin γ
      ≤sqrt((.9)²+(.26)²)
       =sqrt(1097/1250)<1.                          (10)

### 5.1. Normal u supplied by C; ψ≥θ

Here ℓ≥0. Separation would give U+a≤lower_J(u). By (6),(7),

    lower_J(u)=k𝒰+ℓ𝒱
              ≤k(h−a)+ℓ(d+2.26t).

Together with (3), this implies

    (1+k)a≤ηc+s−.24ℓt≤ηc+s.                        (11)

The identity in (11) uses

    k h+ℓ(d+2.26t)=2.5c−s−.24ℓt.

Since 0≤ψ−θ≤π/4−θ,

    k≥cos(π/4−θ)=(c+s)/sqrt(2)≥.7(c+s).

It follows from (9) that

    1+k−(ηc+s)
      ≥1−.886c−.3s
      ≥1−sqrt(218749/250000)>0.

This contradicts (11) and a>1.

### 5.2. Normal u supplied by C; ψ≤θ

Now ℓ≤0. The exact lower support and (6),(7) give

    lower_J(u)=k𝒰+ℓ(𝒱+a)
              ≤k(h−a)+ℓ(1.74d+2t).

Separation and (3) would imply

    (1+k)a≤ηc+s+ℓ(.74d−.5t).                       (12)

Put γ=θ−ψ, so k=cos γ, ℓ=−sin γ and
c=d cos γ−t sin γ, s=t cos γ+d sin γ. The right side of (12),
minus k, is exactly

    (ηd+t−1)cos γ+(.26d−1.086t)sin γ.

The first coefficient is less than .9 by the estimate preceding
(10), and the second is at most .26. Thus (10) shows that the
right side of (12) is less than 1+k, again contradicting a>1.

### 5.3. Normal u_J supplied by J; ψ≤θ

Here ℓ≤0, and the strict point T in C gives V+a>v(T)=1.74s+2c.
Hence the exact upper support obeys

    upper_C(u_J)=k(U+a)−ℓ(V+a)
                ≥k(w+a)−ℓ(1.74s+2c).

Separation would require this support to be at most 𝒰≤h−a.
Consequently

    (1+k)a≤ηd+t+.826ℓs≤ηd+t.                        (13)

The identity uses v(T)−v(W)=.826s. Since
0≤θ−ψ≤π/4−ψ, we have k≥.7(d+t). Applying (9) with d,t
in place of c,s gives 1+k>ηd+t, contradicting (13).

### 5.4. Normal u_J supplied by J; ψ≥θ

Here ℓ≥0. The cap (4) gives V≤f−a, and therefore

    upper_C(u_J)=k(U+a)−ℓV
                ≥kw−ℓf+a(k+ℓ).

Separation and (6) would imply

    (1+k+ℓ)a≤ηd+t+ℓ(1.086s+.26c).                 (14)

The identity in (14) uses v(F)−v(W)=1.086s+.26c.
Put γ=ψ−θ. After subtracting k+ℓ, the right side of (14)
becomes exactly

    (ηc+s−1)cos γ+(1.26c−.5s−1)sin γ.

The first coefficient is less than .9, and the second is at most .26.
By (10), the right side of (14) is less than 1+k+ℓ, a contradiction.

All four possibilities in (8) are impossible. Two disjoint open
squares must have an actual separating face normal, so the assumption
that H is outside C⁺ was false. H is strictly in C⁺. This proves
Theorem 1. ∎

## 6. Exact original C1092 owner mapping

In the last MPPM auxiliary assignment use the four local charts R⁻ⁱ:

    C_i=Q_(4+i), K_i=Q_i,
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

Indices on these three cyclic owner families are taken modulo four.
Each C_i has the four strict anchors of Theorem 1. The actual owner
ledger for the first central square in any chart is

| Local excluded point of C_i | Actual strict owner | Original fact in that owner's chart |
|---|---|---|
| W=(.914,2) | B_(i−1) | R⁻¹(2,.914)=(.914,2) |
| F₀=(1,2.26) | B_(i−1) | R⁻¹(1.74,1)=(1,2.26) |
| F=(2,2.26) | C_(i−1) | R⁻¹T=(2,2.26) |

These are original markers or listed auxiliary points in their actual
owners. In particular, neither W nor F₀ requires a previously proved
P transfer. All owners in this ledger are distinct from C_i and
C_(i+1) when used in the four-sector configuration.

The next physical central square is R(C_(i+1) in its local chart).
Its displayed strict points M_J,U_J,L_J,T_J are precisely the R
images of M,U₀,L₀,T. The normal cone in Section 4 therefore compares
strict points in two genuine, distinct central owners.

## 7. The entire all-negative original sector is excluded

**Theorem 2.** In the original C1092 physical setting with the last
MPPM auxiliary assignment, the four central canonical angles cannot
all be nonpositive. There is no angle-magnitude restriction.

Indeed, apply Theorem 1 to each adjacent ordered pair C_i,C_(i+1).
Every central square strictly owns its local H=(1,1.5). Its distinct
actual corner square K_i therefore excludes H. Each K_i strictly
owns its original marker (1,.914) and the paired-corner inner point
(1,1), and lies in the local first quadrant. Each B_i strictly owns
(2,.914),(1.6,1) and lies above its actual local bottom wall.

The all-angle boundary transfer, Theorem 7 of
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md), now forces
every local P=(2,1) strictly in its actual B_i. This uses no boundary
angle hypothesis.

Finally apply the complete full-angle all-negative owned-point theorem
in [C1092-NEGATIVE-OWNED-POINTS.md](C1092-NEGATIVE-OWNED-POINTS.md).
Its original wall extension gives each B_i the strict segment
[1.44,2]×{1}; the preceding P supplies the current D exclusion.
The direct local argument then puts all four central centers strictly
inside the disk of radius 1/sqrt(2) about (2,2). The four-center disk
argument contradicts their actual disjointness for a>1.

This proves Theorem 2 directly from the original actual owners and
the retained paired-corner inner-point theorem. The result covers
the full continuous negative canonical sector, including all axis
and 45-degree endpoints, and replaces any entrance angle history for
that sector. It does not assert that positive or mixed central signs
are covered by this all-negative conclusion. ∎
