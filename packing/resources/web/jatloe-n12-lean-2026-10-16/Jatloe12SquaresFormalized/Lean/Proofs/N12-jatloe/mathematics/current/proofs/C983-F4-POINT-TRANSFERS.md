# C983: actual F4 supplies the southeast point transfers

All terminating decimals are exact rationals. Squares are open, with common side a>1 in the applications. Every stated exclusion permits boundary contact. These local theorems hold for every canonical orientation and require no upper side bound or container wall.

## 1. A horizontal crosspoint from the inward auxiliary and one bottom-bar point

**Theorem 1.** Let Q be an open square of side a>1 strictly owning

    M=(.35,−.35), D=(.26,0), A=(1,−.26).

Suppose it excludes

    F=(0,−.26), T=(.5,−1).

Then it strictly owns X=(.5,0).

**Proof.** In either canonical frame take c≥s≥0 and c²+s²=1. Write the strict bands as U<u<U+a, V<v<V+a.

For u=cx+sy, v=−sx+cy, all four bands of X follow from the strict anchors. The lower u, upper u, lower v and upper v comparisons are respectively

    u(X)−u(D)=.24c>0,
    u(A)−u(X)=.5c−.26s≥.24c>0,
    v(X)−v(M)=.35c−.15s≥.20c>0,
    v(D)−v(X)=.24s≥0.

This includes s=0 and c=s.

Use now u=cx−sy, v=sx+cy. If X were excluded, its lower u and lower v bands would follow from D, with increments .24c>0 and .24s≥0. Its upper u band follows from A, with increment .5c+.26s>0. Therefore

    V+a≤.5s.                                            (1)

At F both upper bands follow from D:

    u(D)−u(F)=.26(c−s)≥0,
    v(D)−v(F)=.26(c+s)>0.

Its lower v band is strict by (1), since

    .5s−v(F)=.5s+.26c≤sqrt(.3176)<1<a.

Thus F is lower u, giving U≥.26s.

At T the lower u band follows from M and its upper v band follows from D, with increments .15c+.65s>0 and c−.24s≥.76c>0. Its lower v band is strict by (1), because

    .5s−v(T)=c≤1<a.

Consequently T is upper u, U+a≤.5c+s. The two u faces imply

    a≤.5c+.74s≤sqrt(.7976)<1,

which is impossible. Thus X is strict in the negative sign as well. Every exterior inequality was weak, and every band comparison was strict through its owned anchor or a>1. ∎

## 2. An extra upper auxiliary gives the common upper point

**Theorem 2.** Let Q have side a>1 and strictly own the three anchors of Theorem 1 and also B=(0,.26). If Q excludes F=(0,−.26), then it strictly owns

    Y=(.525,.125).

**Proof.** In the positive canonical frame the lower u, upper u, lower v and upper v bands follow respectively from D,A,M,B. Their increments are

    .265c+.125s>0,
    .475c−.385s≥.09c>0,
    .475c−.175s≥.30c>0,
    .525s+.135c>0.

For the negative frame, the lower u, upper u and lower v bands follow from D,A,M, with increments

    .265c−.125s≥.14c>0,
    .475c+.385s>0,
    .175s+.475c>0.

At F its lower u band follows from B, its upper u band from A, and its upper v band from B. The corresponding increments are .52s≥0, c>0 and .52c>0. Hence the actual exclusion of F forces V≥−.26c. The remaining upper v band of Y is strict because

    v(Y)−V≤.525s+.385c≤sqrt(.42385)<1<a.

This covers both signs and their endpoints. ∎

## 3. The exact actual C983 applications

Suppose merged Q7 owns F4=(2,1.74); this includes both remaining labels 8208 and 8240. Its always-owned G3=(1.74,2), southwest marker, and northwest marker retain their one actual owner.

Every original Q5 component avoiding F4 owns F8=(3,1.74), by direct inspection of `C983-ORIGINAL-OWNERS.txt`. Thus F8 is strict in actual southeast Q5. Whenever this Q5 also owns G6=(2.26,2), apply Theorem 1 after translating by (−2,−2):

| Local input | Actual C983 source |
|---|---|
| M,D,A strict | Q5's southeast marker, G6 and F8 |
| F excluded | F4 strictly in merged Q7 |
| T excluded | (2.5,1) strictly in Q9's bottom bar |

The whole bottom bar [2.26,2.8]×{1} belongs strictly to actual Q9. Its original labels all own F6,G5; the transposed strong wall advance, Theorem 4 of `C981-WALL-CYCLES.md`, uses the actual Q0 points (1.74,1),(1.87,.76), Q5's southeast marker, and Q9's genuine bottom wall. These are exactly the sources already established in `C983-MERGED-INWARD-ALTERNATIVE.md`, Section 1. Convexity supplies (2.5,1) in that same owner.

Consequently

    Q7 owns F4 and Q5 owns G6
        ⇒ (2.5,2) is strictly in actual Q5.              (2)

If Q5 additionally owns F5=(2,2.26), Theorem 2 has the same genuine excluded F4 and gives

    (2.525,2.125) strictly in that same actual Q5.        (3)

Neither (2) nor (3) assumes that merged Q7 owns (2,1.5). Its northwest marker is an owned point and is never used as an exclusion from Q7.

## 4. A small-angle consequence when the southeast square omits G8

Under the preceding F4 hypothesis, suppose Q5 owns F8,G6 and excludes G8=(3,1.6). Its original excluded northeast marker belongs to Q6, and its excluded right-wall marker belongs to Q10. Theorem 1 of `ELBOW-CROSSPOINT.md` applies literally to Q5. In coordinates translated by (−2,−2) it proves a strictly negative canonical frame u=cx−sy, v=sx+cy and the weak upper faces

    U+a≤c+.4s, V+a≤.35(c+s).                           (4)

At F4=(0,−.26), both upper bands follow from strict G6=(.26,0). Its lower v band is strict by (4), because

    .35(c+s)−v(F4)=.35s+.61c≤sqrt(.4946)<1<a.

Thus F4 is lower u, U≥.26s. Combining with (4),

    1<a≤c+.14s.

For h=s/(1+c), the exact identity

    c+.14s−1=2h(.14−h)/(1+h²)

therefore gives

    0<h<7/50,
    s<700/2549<7/25,
    c>2451/2549>24/25.                                (5)

This is a proved necessary small negative angle, not yet a contradiction. The same actual square also owns (2,1.5) and (2.125,1.475) by the cited elbow theorem; those points belong to Q5 here and have not been assigned to merged Q7.

## 5. Scope

These theorems supply stronger actual-point entrances for the two remaining C983 F4 labels. They are reusable local implications and do not by themselves close either whole label. The remaining F5-only label 8224 is not included in their F4 applications. A complete remaining-family support contradiction is still required.
