# A three-anchor elbow forces a crosspoint

All decimals are exact rationals. Ownership is strict interior membership in an open square; exclusions include boundary points.

**Theorem.** Let Q be any open square of side a>1 strictly owning

    M=(2.35,1.65), D=(2.26,2), A=(3,1.74),

and excluding

    N=(2.35,2.35), G=(3,1.6), R=(3.086,2).

Then Q strictly owns X=(2,1.5). No container, upper side bound, or whole foreign segment is required.

**Proof.** Translate by (−2,−2). The strict points are

    M=(.35,−.35), D=(.26,0), A=(1,−.26),

the excluded points are N=(.35,.35), G=(1,−.4), R=(1.086,0), and the target is X=(0,−.5). Let U,V be lower face coordinates.

First choose a nonnegative canonical frame u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1. At N its lower u and lower v bands follow from M, while its upper u band follows from A:

    u(N)−u(M)=.7s≥0,
    v(N)−v(M)=.7c>0,
    u(A)−u(N)=.65c−.61s≥.04c>0.

Thus N is upper v. At G its lower u band follows from M, while both upper bands follow from A:

    u(G)−u(M)=.65c−.05s≥.60c>0,
    u(A)−u(G)=.14s≥0,
    v(A)−v(G)=.14c>0.

Thus G is lower v. The opposite face bounds give

    a≤v(N)−v(G)=.65s+.75c≤sqrt(.985)<1.

Consequently no nonnegative canonical angle is possible, including the axial and positive diagonal representatives.

Use the nonpositive frame u=(c,−s), v=(s,c), where again c≥s≥0. At N its upper u band follows from A and its lower v band from M. Hence it must be lower u or upper v. At G its lower u band follows from M and its upper v band from A. Hence it must be upper u or lower v.

Suppose N is lower u. G cannot be upper u, because that pair of opposite faces would give

    a≤u(G)−u(N)=.65c+.75s≤sqrt(.985)<1.

Therefore G is lower v. At R both lower bands are strict by comparison with D:

    u(R)−u(D)=.826c>0,
    v(R)−v(D)=.826s≥0.

Thus R must be upper u or upper v. The first alternative, together with N lower u, gives

    a≤u(R)−u(N)=.736c+.35s≤sqrt(.664196)<1.

The second, together with G lower v, gives

    a≤v(R)−v(G)=.086s+.4c≤sqrt(.167396)<1.

Both are impossible, so N is upper v. G cannot now be lower v, because that would give a≤−.65s+.75c≤.75. Hence

    U+a≤c+.4s,  V+a≤.35(s+c).                          (1)

For X, both upper bands are strict by the anchor M:

    u(M)−u(X)=.35c−.15s≥.20c>0,
    v(M)−v(X)=.35s+.15c>0.

The lower u band follows from (1) and the opposite-face gap

    (c+.4s)−u(X)=c−.1s≤1<a.

The lower v band follows from the second cap in (1), since

    .35(s+c)−v(X)=.35s+.85c≤sqrt(.845)<1<a.

Thus every target band is strict. All square orientations have been covered by the two canonical signs, and every exclusion has remained a weak face inequality, including tangency and equality in an anchor comparison. ∎

**Corollary.** Under the same hypotheses, Q also strictly owns

    X1=(2.125,1.475).

The proof has already excluded all nonnegative canonical representatives and established (1) in the negative frame. In translated coordinates X1=(.125,−.525). Its two upper bands follow from M, with differences

    u(M)−u(X1)=.225c−.175s≥.05c>0,
    v(M)−v(X1)=.225s+.175c>0.

Its lower bands follow from the same opposite caps (1), because

    (c+.4s)−u(X1)=.875c−.125s≤.875<1<a,
    .35(c+s)−v(X1)=.875c+.225s≤sqrt(.81625)<1<a.

Thus the additional point is strict for every allowed orientation.

## Exact C974 and C976 consequence

Southeast Q6 with label65792 or65824 owns G6=(2.26,2) and F8=(3,1.74), as well as its original marker M. It excludes G8=(3,1.6). The other excluded points N and R belong to the actual northeast Q7 and right wall Q10, respectively. The theorem therefore puts X=(2,1.5) strictly in Q6.

The same point is already strict in actual southwest Q5. Here is its complete independent source mapping. Apply the retained central crosspoint lemma, reproduced in the appendix of `C893-CONTINUOUS-EXCLUSION.md`, under the half-turn (x,y)↦(4−x,4−y). Its three strict anchors become Q5's original southwest marker and the always-owned pair F4=(2,1.74), G3=(1.74,2). Its excluded southeast and northwest markers become, respectively, the northwest marker (globally absent in C974, owned by Q8 in C976) and the southeast marker in Q6. Its other required excluded points become (1,1.6),(1,1.5), both strict in the actual Q1 singleton segment {1}×[1.12,1.74]. The strict conclusion becomes exactly X=(2,1.5).

This is a duplicate strict point in two distinct actual owners. Hence southeast labels65792 and65824 are impossible in both C974 and C976. The only remaining southeast labels are

    262400,327936,327968,

and all three own G8=(3,1.6). The last two also own G6; the last additionally owns F5. This structural consequence retains the exact local ownership entrance and makes no assertion about a label whose G8 point is owned.

## A second exact transfer to the northeast elbow

Apply the full theorem and its corollary under the quarter-turn (x,y)↦(4−y,x). A northeast square with label131104 owns its marker, F5=(2,2.26), and G7=(2.26,3). The theorem's three excluded points become the northwest marker, F7=(2.4,3), and the top marker (2,3.086). These are genuinely excluded from this exact northeast owner in both C974 and C976. Therefore it has a strictly negative canonical representative and owns both

    (2.5,2),  (2.525,2.125).                            (2)

Suppose its southeast neighbor has the outward label262400. The actual bottom bar, actual southeast paired corner and right wall provide all hypotheses of the reflected Theorem 1 in `OUTWARD-BAR-AND-UPPER-SPAN.md`, after the established outward sign lock. In particular G6 is excluded from that southeast square by its exact label; this use does not require assigning G6 to the northeast square. That theorem gives the same second point in (2) strictly in the southeast square, a contradiction.

If instead the southeast square has a nonnegative canonical angle and owns G6, its marker, G6 and F8 already put the first point (2.5,2) strictly inside it. In coordinates translated by (−2,−2), the target is K=(.5,0). Its lower u and upper v bands follow from D=(.26,0), its upper u band from A=(1,−.26), and its lower v band from M=(.35,−.35):

    u(K)−u(D)=.24c>0,
    v(D)−v(K)=.24s≥0,
    u(A)−u(K)=.5c−.26s≥.24c>0,
    v(K)−v(M)=−.15s+.35c≥.20c>0.

This again contradicts (2). Since the northeast elbow owns F5, southeast label327968 is also disallowed by strict ownership. Thus, whenever northeast Q7 has label131104, the only surviving southeast possibility at this intermediate stage is label327936 with a strictly negative canonical representative. The next theorem excludes it as well, using the actual southwest crosspoint and bottom-wall advance.

## A crossed-elbow obstruction with three isolated exclusions

**Theorem 2.** Let 1/2≤w≤4/5. No open square of side a>1 can strictly own

    M=(2.35,1.65), D=(2.26,2), A=(3,1.74)

while excluding all three points

    X=(2.5,2), C=(2,1.5), T=(2+w,1).

No original-marker exclusion, wall, side upper bound, or whole foreign segment is required.

**Proof.** Translate by (−2,−2). The points are M=(.35,−.35), D=(.26,0), A=(1,−.26), X=(.5,0), C=(0,−.5), and T=(w,−1).

In a nonnegative canonical frame u=(c,s), v=(−s,c), all four strict bands of X follow from D,A,M by the four comparisons displayed just above. Hence this entire sign is impossible.

Use a nonpositive frame u=(c,−s), v=(s,c), c≥s≥0 and c²+s²=1. At X its lower u and lower v bands follow from D, with increments .24c>0 and .24s≥0, while its upper u band follows from A, with increment .5c+.26s>0. It must therefore be upper v:

    V+a≤.5s.                                             (3)

Strict ownership of A gives s−.26c<.5s, hence

    s/c<.52.                                             (4)

At C both upper bands follow strictly from D:

    u(D)−u(C)=.26c−.5s>0,
    v(D)−v(C)=.26s+.5c>0,

using (4). Its lower v band follows from the opposite cap (3), since

    .5s−v(C)=.5(c+s)≤1/sqrt(2)<1<a.

Thus C must be lower u, so U≥.5s.

At T the lower u band follows from M, with increment (w−.35)c+.65s>0, and the upper v band follows from D, with increment c−(w−.26)s≥.46c>0. Its lower v band is strict by (3), because

    .5s−v(T)=c+(.5−w)s≤1<a.

Hence T is upper u, U+a≤wc+s. The two u faces now give

    a≤wc+.5s≤.8c+.5s≤sqrt(.89)<1,

which is impossible. Both canonical signs, axis and diagonal limits, and every weak exterior equality have been included. ∎

### Completion of the northeast label131104 branch

Under this northeast label, the earlier quarter-turn theorem gives X=(2.5,2) strictly in actual Q7. If the southeast square has label262400 it was already excluded by the duplicate point (2.525,2.125). Every other remaining southeast label owns G6, hence has the three strict anchors M,D,A of Theorem 2. Actual Q5 owns C=(2,1.5) by the exact retained-crosspoint mapping above. Actual bottom Q9 owns T=(2.8,1) by the strong wall theorem with the actual Q0 singleton. Thus all three exclusions of Theorem 2 come from genuine different owners, and Theorem 2 excludes the remaining southeast square.

Consequently northeast label131104 is impossible in both C974 and C976, with no assumption about either missing-corner alternative or any top-origin point. This removes the intermediate two-square configuration entirely.

## An additional upper anchor gives the common point directly

**Theorem 3.** Suppose a square Q of side a>1 strictly owns

    M=(2.35,1.65), D=(2.26,2), A=(3,1.74), F=(2,2.26),

and excludes C=(2,1.5). Then Q strictly owns Y=(2.525,2.125).

**Proof.** Translate by (−2,−2), so Y=(.525,.125), F=(0,.26), and the other points have the coordinates used in Theorem 2.

In a nonnegative canonical frame u=(c,s), v=(−s,c), all four strict target bands follow from D,A,M,F:

    u(Y)−u(D)=.265c+.125s>0,
    u(A)−u(Y)=.475c−.385s≥.09c>0,
    v(Y)−v(M)=−.175s+.475c≥.30c>0,
    v(F)−v(Y)=.525s+.135c>0.

In a nonpositive canonical frame u=(c,−s), v=(s,c), the lower u, upper u and lower v bands follow from D,A,M:

    u(Y)−u(D)=.265c−.125s≥.14c>0,
    u(A)−u(Y)=.475c+.385s>0,
    v(Y)−v(M)=.175s+.475c>0.

At C=(0,−.5), its lower u band follows from F, its upper u band from A, and its upper v band from F:

    u(C)−u(F)=.76s≥0,
    u(A)−u(C)=c−.24s≥.76c>0,
    v(F)−v(C)=.76c>0.

Hence C is lower v. The remaining target upper v band follows from

    v(Y)−v(C)=.525s+.625c≤sqrt(.66625)<1<a.

Thus Y is strict in both canonical signs, including all axis and diagonal boundaries. ∎

### Elimination of southeast label327968

This label owns the three southeast anchors and F5=(2,2.26), so Theorem 3 applies with the actual southwest Q5 crosspoint C=(2,1.5). It gives (2.525,2.125) strictly in southeast Q6.

The northeast neighbor must exclude F5 by disjointness. After the earlier reductions its only remaining label is131200, which owns F7. Theorem 3 of `OUTWARD-BAR-AND-UPPER-SPAN.md`, with the actual top origin, paired northeast corner, and complete right-wall segment, puts the same point strictly in northeast Q7. This is impossible. Thus southeast label327968 is eliminated in both C974 and C976, leaving only

    Q6=262400 or327936.
