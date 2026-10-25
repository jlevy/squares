# C1092: the full negative cycle when the boundary points are owned

All decimals denote exact rationals. Owned points are strict in their
actual open square; exclusions and separating faces allow equality.

## 1. Statement and exact scope

**Theorem.** In the original C1092 physical setting and last MPPM
auxiliary assignment, suppose all four central canonical angles are
nonpositive and all four actual boundary owners strictly own their
local points P=(2,1). Then the configuration is impossible.

There is no angle-magnitude restriction in this theorem. Its proof
derives the required angle restriction from two actual foreign points,
then uses a longer actual boundary segment to place every central
center in the same open disk of radius 1/sqrt(2).

The boundary ownership premise is explicit in this local composition.
It is discharged for the entire all-nonpositive sector by the later
adjacent-square theorem in
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md).
That theorem starts from original owners, forces all four corner-transfer
points, and then applies this disk ending without any angle cutoff.

## 2. An unconditional longer boundary segment

Use the same four local charts as the other direct C1092 notes:

    R(x,y)=(4−y,x),       local chart R^(−i),
    C_i=Q_(4+i),
    (B_0,B_1,B_2,B_3)=(Q_9,Q_10,Q_11,Q_8).

The last assignment gives each local B the strict points
(2,.914),(1.6,1),(1.74,1). The next actual central square strictly
owns (2.26,1) and (2,1.74), the images under R of its original
U₀=(1,1.74) and T=(1.74,2). Both points are therefore excluded
from B.

Apply the retained all-orientation wall-reach lemma, reproduced in
Section A.2 of
[C981-RETAINED-CONTINUOUS-LEMMAS.md](C981-RETAINED-CONTINUOUS-LEMMAS.md),
under the simultaneous coordinate change

    (X,Y)=(y,4−x).

Its strict marker and anchor become (.914,2),(1,2.4). Its two
excluded points become (1,1.74),(1.74,2), and the actual bottom
container wall becomes X≥0. The exact parameter checks are

    .82<14/17,
    .74²+.26²=.6152<1,
    .56²+.74²=.8612<1.

The strict conclusion (X,Y)=(1,2.56) gives

    L'=(1.44,1) strictly in B.                       (1)

This conclusion uses no sign or angle hypothesis on any square and
does not assume P is owned. When P is owned, the whole segment
[1.44,2]×{1} belongs strictly to this one actual B.

## 3. A negative sector with its preceding P owned

Write the negative central frame as

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,
    q=s/(1+c),       0≤q≤sqrt(2)−1,
    U<u·X<U+a,       V<v·X<V+a.

The original local C strictly owns U₀=(1,1.74), T=(1.74,2),
M=(1.65,1.65), L₀=(1,1.6). It excludes

    D=(1,2), E=(2,1.74), N=(1.65,2.35), F=(2,2.26).

Here D is supplied by the preceding boundary's owned P. The other
three points are original strict data in the next and preceding
central owners, exactly as in the direct disk proof.

The all-angle negative face comparisons in Section 2 of
[C1092-WIDE-NEGATIVE-DISK.md](C1092-WIDE-NEGATIVE-DISK.md)
give

    U≥c−2s,       U+a≤2c−1.74s,
    V+a≤1.65s+2.35c,       V+a≤2s+2.26c.              (2)

These comparisons use only c≥s≥0. The first two faces give

    1<a≤c+.26s.

The identity c+.26s−1=2q(.26−q)/(1+q²) therefore forces

    0<q<13/50.                                      (3)

The axis case has already been excluded: D and the strict U₀ would
have equal u projections at s=0. Thus (3) is a derived bound, not an
incoming angle assumption.

The new actual point L' in (1) is outside C. Its lower-u and
upper-v bands are strict by U₀, using

    u(L')−u(U₀)=.44c+.74s>0,
    v(U₀)−v(L')=.74c−.44s>0.

If it exited through upper u, its cap and the lower-u floor at D
would imply a≤.44c+s. But

    1−(.44c+s)
      =(1−q)(14−36q)/[25(1+q²)]>0                (4)

throughout (3). Hence L' must be lower-v:

    V≥c+1.44s.                                      (5)

## 4. The full negative disk conclusion

Let (Cₓ,Cᵧ) be the actual center and Z its lowest closed vertex.
Equations (2),(5) give

    Zₓ=Cₓ+a(c−s)/2
       ≥1+.44s²−cs+ac
       >1+.44s²+c−cs>1.44.                         (6)

The last inequality has the exact positive factorization

    1+.44s²+c−cs−1.44
      =(1−q)²(1+q)(14−36q)/[25(1+q²)²]>0,        (7)

valid by (3). If Zᵧ≤1, the upper-u cap at E in (2) gives
c(Zₓ−2)≤s(Zᵧ−1.74)≤0, so Zₓ≤2. The segment from Z to
the strict point T then meets y=1 with abscissa in (1.44,2].
This would put a closure point of C in the actual strict segment
[L',P] inside B, contradicting disjoint open interiors. Therefore

    Cᵧ>1+a(c+s)/2.                                  (8)

The same caps in (2) give Cₓ,Cᵧ<2 without further angle conditions.
For completeness,

    Cₓ≤2+.52cs−a(c+s)/2<2,
    Cᵧ≤2.35−.35s²+.65cs−a(c+s)/2<2.

The first inequality follows from .52cs≤.26<1/2≤(c+s)/2.
For the second, replace a by 1 and subtract 2; the result is

    .35c²+.65cs−(c+s)/2
      ≤.35c+.65s−(c+s)/2=.15(s−c)≤0.

Set Y*=1+(c+s)/2 and X*=[c−2s+1/2+sY*]/c. Equation (8),
a>1, and the lower-u face at D give

    X*<Cₓ<2,       Y*<Cᵧ<2.

Finally the exact identity

    1/2−(2−X*)²−(2−Y*)²
      =4q³(1−q)/[(1+q)²(1+q²)]≥0

puts the center strictly within radius 1/sqrt(2) of (2,2).

Under the theorem's hypotheses this reasoning applies in all four
charts. The charts fix (2,2), so all four physical central centers
lie in that open disk. The four-center argument from
[C1092-DIRECT-NEGATIVE-DISK.md](C1092-DIRECT-NEGATIVE-DISK.md)
forces a pair at distance less than 1, while disjoint side-a squares
require their center distances to be at least a>1. This proves the
theorem for the entire negative canonical sector. ∎

## 5. An intermediate dichotomy and its completed entrance

Combine the local argument above with the missing-point radius theorem
in [C1092-CYCLIC-ENTRANCE.md](C1092-CYCLIC-ENTRANCE.md).
For arbitrary nonpositive central angles, the center in sector i is
proved to lie in the open disk whenever its own P_i is missing, or
whenever P_(i−1) and P_i are both owned. No angle-magnitude condition
is now needed in this dichotomy.

Thus the only sectors outside these proved radius implications have

    P_(i−1) missing,       P_i owned.

If their local D is excluded from C for any other genuine reason,
the disk argument applies to them too. A remaining transition must
therefore allow D strictly in C. This identifies the actual-neighbor
geometry required by this intermediate dichotomy. The subsequent
two-central theorem in
[C1092-NEGATIVE-H-PROPAGATION.md](C1092-NEGATIVE-H-PROPAGATION.md)
supplies a stronger conclusion: all H points, and consequently all P
points, are forced when all four central angles are nonpositive. Thus
the all-nonpositive entrance is now complete, while the local disk
theorem above keeps its explicit two-owned-point hypotheses.
