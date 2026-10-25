# C1092: the short direct negative proof by four centers in a disk

Every decimal in this note is an exact rational. Squares are open;
owned points are strict, and excluded points may lie on a face.

## 1. The completed direct branch

**Theorem.** Retain the original C1092 physical setting, the actual
disjoint side-a squares with a>1, and the last MPPM auxiliary assignment

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

If all four canonical central signed half-angles lie in [−1/7,0],
the configuration is impossible.

This proof uses the original actual owners and their container walls.
It requires none of the 431 common-parent coordinate cuts, none of
the incoming maximal-angle histories, no historical center bounds,
and no boundary-angle restriction. The retained paired-corner
inner-point theorem supplies the corner's strict point (1,1).

The whole proof consists of the direct boundary-point theorem, five
forced central faces, a whole-segment intersection, and an exact disk
identity. There is no transport of separating normals between sectors
and no scalar variation estimate in this ending. The independent
stronger center and scalar estimates remain available in
[C1092-DIRECT-NEGATIVE-CYCLE.md](C1092-DIRECT-NEGATIVE-CYCLE.md).

## 2. The exact original-owner geometry

Put R(x,y)=(4−y,x). In the local chart R^(−i), take

    C_i=Q_(4+i),       K_i=Q_i,
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

Every local central square C strictly owns

    M=(1.65,1.65), U₀=(1,1.74), T=(1.74,2), L₀=(1,1.6).

Its corresponding actual boundary B strictly owns

    (2,.914), L=(1.6,1), G₀=(1.74,1).

Theorem 8 of
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md)
applies in each chart: its central half-angle hypothesis is exactly
the stated interval, and the actual corner and boundary walls rotate
with the same chart. Therefore each B strictly owns P=(2,1).

The preceding actual boundary consequently owns the local D=(1,2).
The other points excluded from C have these actual sources:

| Point outside C | Actual source in this local chart |
|---|---|
| D=(1,2) | The preceding boundary's newly proved P |
| G₀=(1.74,1) | The current boundary's original strict auxiliary |
| R₀=(2,1.74) | The next central square's original strict T |
| N=(1.65,2.35) | The preceding central square's original strict M |
| F=(2,2.26) | The preceding central square's original strict T |

In particular every point and the segment used below has one actual
owner. No union of points from different squares is treated as the
interior of a single square.

## 3. Five forced faces and two coarse center caps

Write the local negative canonical normals and open face bands as

    u=(c,−s), v=(s,c),
    c=(1−q²)/(1+q²), s=2q/(1+q²), 0≤q≤1/7,
    U<u·X<U+a,       V<v·X<V+a.

The strict anchors U₀,T and the five exclusions above force

    U≥c−2s,                 U+a≤2c−1.74s,
    V≥c+1.74s,              V+a≤1.65s+2.35c,
                             V+a≤2s+2.26c.              (1)

Here are all the face checks. At D the upper-u and lower-v bands
follow from U₀, while the upper-v band follows from T. Thus D is
lower-u. At q=0 this contradicts U₀'s equal u coordinate already;
retaining zero in the ensuing weak estimates is harmless.

At R₀ both lower bands follow from U₀. Its upper-v band follows
from T, since v(R₀)−v(T)=.26(s−c)≤0. Thus R₀ is upper-u.

At G₀ the lower-u and upper-v bands follow from U₀, using
.74(c+s)>0 and .74(c−s)>0. An upper-u exit together with D's
lower-u exit would give

    a≤.74c+s
      =1−(1−q)(13−87q)/[50(1+q²)]<1,

because 13−87q≥4/7>0. Hence G₀ is lower-v.

At N, the lower-u, upper-u and lower-v bands follow from U₀,T,T,
respectively: the three positive differences are

    .65c−.61s,       .09c+.35s,       .35c−.09s.

Thus N is upper-v. At F the lower-u band follows from T because
.26(c−s)≥0, and the lower-v band follows from U₀. Its upper-u
band follows from U≥u(D), since

    u(F)−U≤u(F)−u(D)=c−.26s≤1<a.

Thus F is upper-v. This proves (1), including all possible face
contacts at the excluded points.

Let (Cₓ,Cᵧ) be the actual center and w=c+s. The two upper faces
at R₀,F and the lower-u/upper-v pair at D,N give, respectively,

    Cₓ≤2+.52cs−aw/2,
    Cᵧ≤2.35−.35s²+.65cs−aw/2.

Since w≤sqrt(2)<3/2, cs≤1/2, and

    (w−1)/2=cs/(w+1),

we obtain the convenient coarse bounds

    Cₓ<1.5+cs[.52−1/(w+1)]≤1.56<2,
    Cᵧ<1.85+cs[.65−1/(w+1)]≤1.975<2.             (2)

These bounds were derived from actual point exclusions, without a
center enclosure or an upper bound on a.

## 4. The actual boundary segment forces strict wall clearance

Let Z be the lowest vertex of the closed central square:

    Z=(Cₓ+a(c−s)/2, Cᵧ−a(c+s)/2).

The lower faces in (1) imply

    Cₓ≥1+.74s²−cs+a(c+s)/2,
    Zₓ≥1+.74s²−cs+ac>1+c−cs.

On q∈[0,1/7], c≥24/25 and cs≤168/625. Consequently

    Zₓ>1+24/25−168/625=1057/625>1.6.              (3)

Suppose Zᵧ≤1. The vertex Z lies on C's upper-u face, so the cap
at R₀ in (1) gives

    cZₓ−sZᵧ=U+a≤2c−1.74s,
    c(Zₓ−2)≤s(Zᵧ−1.74)≤0.

Hence Zₓ≤2. The segment joining Z to the strict point T=(1.74,2)
meets y=1 at a point W with 1.6<Wₓ≤2. This includes the case
Zᵧ=1, where W=Z.

By convexity W belongs to the closure of C. But the whole segment
[L,P]=[1.6,2]×{1} is strictly inside the single actual boundary B.
Thus W lies in the closure of C and the interior of B, impossible
for two squares with disjoint open interiors. Indeed an open
neighborhood of W inside B would meet the interior of C as well.

It follows that Zᵧ>1, or

    Cᵧ>1+a(c+s)/2.                                  (4)

No orientation or center hypothesis on B was used in this argument.

## 5. An exact disk identity

Define two reference coordinates, depending only on q,

    Y*=1+(c+s)/2=(q²+2q+3)/[2(1+q²)],
    X*=[c−2s+1/2+sY*]/c
       =(q³+7q²+q+3)/[2(q+1)(1+q²)].

Equation (4) and a>1 give Cᵧ>Y*. The lower-u face at D gives

    cCₓ−sCᵧ≥c−2s+a/2,

and therefore Cₓ>X*, since c>0 and s≥0. Together with (2),

    X*<Cₓ<2,       Y*<Cᵧ<2.                         (5)

The required scalar computation is the exact factorization

    1/2−(2−X*)²−(2−Y*)²
      =4q³(1−q)/[(1+q)²(1+q²)]≥0.                  (6)

Every factor sign is immediate on [0,1/7]. Since both positive
coordinate deficits in (5) are strictly smaller than the reference
deficits, (6) implies

    |(Cₓ,Cᵧ)−(2,2)|²<1/2.                          (7)

The strictness comes from a>1 and the actual segment clearance;
it remains strict when the scalar factor in (6) vanishes.

## 6. Four actual central centers cannot fit

All four quarter-turn charts fix O=(2,2), so (7) puts all four
physical central centers in the open disk of radius 1/sqrt(2)
about O.

Four points in this disk have a pair at distance less than 1. If
one point is O this is immediate. Otherwise order their polar
arguments. One consecutive angular gap is at most pi/2. For that
pair, with radii r₁,r₂<1/sqrt(2), the cosine rule gives

    distance²=r₁²+r₂²−2r₁r₂ cos(gap)
             ≤r₁²+r₂²<1.

Each actual open side-a square contains its open concentric disk
of radius a/2. Disjoint interiors therefore require every pair of
central centers to be at distance at least a>1. This contradicts
the pair just found, completing the theorem.

The proved direct scope is [−1/7,0]^4 in the stated last assignment.
Other angle regions and the preceding ownership reduction remain
separate obligations. A different proved disk theorem, in
[C1092-CYCLIC-ENTRANCE.md](C1092-CYCLIC-ENTRANCE.md), handles sectors
whose own boundary point is missing at either central sign; it proves
that four boundary points cannot all be missing, without claiming
that this alone finishes the full assignment.

## 7. The exact boundary-point threshold enlarges the direct region

The rational cutoff 1/7 was convenient for the first proof. The same
original geometry gives a slightly larger exact continuous region.
Put

    α=(13−sqrt(58))/37.

Then 1/7<α<1/4.

**Corollary.** In the theorem's original last assignment, all four
central signed half-angles cannot lie in [−α,0]. This exclusion is
again direct from the original owners and walls, with no historical
center or angle enclosure.

**Proof.** In each sector use the negative frame from Section 3,
now with 0≤q≤α. The original central square strictly owns
M,U₀,L₀,T and excludes N. The same comparisons as before force
N through upper v, so

    V+a≤1.65s+2.35c.

For H=(1,1.5), the lower-u, upper-u and upper-v bands are strict
by comparison with L₀,M,L₀, respectively. Their nonnegative or
positive projection differences are

    u(H)−u(L₀)=.1s≥0,
    u(M)−u(H)=.65c−.15s≥.5c>0,
    v(L₀)−v(H)=.1c>0.

For the remaining lower-v band, the exact identity is

    v(N)−v(H)−1=.85c+.65s−1
      =−(37q²−26q+3)/[20(1+q²)]≤0.              (8)

The two roots of the numerator are
(13−sqrt(58))/37 and (13+sqrt(58))/37. The upward quadratic is
nonnegative for 0≤q≤α. Thus v(N)−v(H)≤1<a, which gives
V<v(H). In particular H is strict even at q=α, when (8) is an
equality.

The distinct actual corner K therefore excludes H. The all-angle
Theorem 7 of
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md)
forces P strictly into B. This works in all four sectors and
therefore also supplies every preceding-boundary exclusion D.

Now apply Theorem 1 of
[C1092-WIDE-NEGATIVE-DISK.md](C1092-WIDE-NEGATIVE-DISK.md).
Its full local disk proof is valid for 0≤q≤1/4, so all four
applications are valid here. Each uses its actual B segment from
(1.6,1) to P and its actual preceding boundary as the owner of D.
All four central centers lie strictly within radius 1/sqrt(2) of
(2,2). Section 6 supplies the contradiction.

This corollary uses the separately proved wider vertex inequality;
it does not extend the numerical q≤1/7 estimates in Sections 3–4
without proof. It states the exact larger direct region obtained
from the original H-completion inequality. ∎
