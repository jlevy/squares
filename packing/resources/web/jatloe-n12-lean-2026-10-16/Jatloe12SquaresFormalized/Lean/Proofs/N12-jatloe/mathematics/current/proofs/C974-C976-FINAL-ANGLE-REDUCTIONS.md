# Further continuous reductions for the last two C974/C976 pairs

Every decimal is an exact rational. Owned points are strictly in their named open square. An excluded point or segment may touch the boundary. The squares in each actual application have the original common side a>1 and their closures remain in [0,4]². No numerical orientation sampling is used below.

The completed preceding reductions leave southeast Q6=327936 and northeast Q7 equal to 131200 or 131232. Both actual wall origins (2,1) in Q9 and (2,3) in Q11 are already proved in `C974-C976-CENTRAL-CROSSPOINTS.md`.

## 1. A negative mixed northeast square reaches the top crosspoint

**Theorem 1.** Let N be an open square of side a>1 with nonpositive canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1.

Suppose it strictly owns M=(.35,.35), F=(0,.26), G=(.26,1), and excludes P=(0,1), D=(.26,0), X=(.5,0). Then H=(.5,1) is strictly in N.

**Proof.** Write U,V for its lower faces. At P both upper bands follow from G, and its lower v band follows from M. The respective coordinate differences are .26c>0, .26s≥0, and .65c−.35s≥.30c>0. Thus

    U≥−s.                                                (1)

At D the lower u band follows from F and the upper v band from G. Its upper u band is strict because

    u(D)−U≤.26c+s≤1.26/sqrt(2)<1<a.

Consequently D is lower v:

    V≥.26s.                                              (2)

Both lower bands at H follow from G, with differences .24c>0 and .24s≥0. If H were upper u, (1) would imply a≤.5c≤.5, impossible. If H were excluded at all, it would therefore be upper v:

    V+a≤.5s+c.                                          (3)

At X its lower u band follows from M, and its upper v band follows from M. The differences are .15c+.35s>0 and .35c−.15s≥.20c>0. Its lower v band follows strictly from (3), since the opposite-face gap v(H)−v(X)=c≤1<a. The exclusion of X therefore forces U+a≤.5c. Together with (1) this gives

    a≤.5c+s.                                             (4)

The function (.5+τ)/sqrt(1+τ²), where τ=s/c∈[0,1], is increasing on that interval and is exactly one at τ=3/4. Thus (4) and a>1 force τ>3/4. But (2)–(3) give a≤c+.24s. The function (1+.24τ)/sqrt(1+τ²) decreases for τ≥3/4, and its value at that endpoint is

    4/5+(.24)(3/5)=118/125<1.

This contradiction proves H strictly. The argument includes s=0 and c=s; in fact (4) already excludes s=0. All exclusions were weak. ∎

## 2. A positive mixed northeast square forces a longer actual top segment

We record explicitly the part of the shallow-cap theorem needed for the transfer, so that no unused foreign segment is assumed.

**Lemma 2.** Let a square C of side a>1 have nonpositive canonical frame u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1. Suppose it strictly owns F=(−.26,0), A=(0,−.74), and excludes B=(−.26,−1). Then every point of the compact set

    R={ (x,y): −.26≤x≤0, −.0345≤y≤0,
                 (x+.26)²+(y+1)²≤1 }

is strictly in C.

**Proof.** At B its lower u band follows from F, its upper u band follows from A, and its upper v band follows from F. For the middle comparison,

    u(A)−u(B)=.26(c−s)≥0.

Thus B is lower v, V≥−.26s−c. If Y=(x,y) lies in R, its lower u band follows from F because (x+.26)c−ys≥0; its upper u band follows from A because −xc+(y+.74)s≥0. Its lower v band follows from A, since

    v(Y)−v(A)=xs+(y+.74)c
       ≥(.48−.0345)c>0.

Finally

    v(Y)−V≤(x+.26)s+(y+1)c
       ≤sqrt((x+.26)²+(y+1)²)≤1<a.

So its upper v band is also strict. The circular boundary is included because a>1. ∎

This is precisely the negative-frame argument of Theorem 14 in `C981-WALL-CYCLES.md`; it needs neither that theorem's additional excluded origin nor its full vertical foreign segment.

**Corollary 3.** In either C974 or C976, if actual Q7=131232 has a nonnegative canonical angle, then actual Q11 strictly owns (1.27,3).

**Proof.** Apply the isometry (x,y)↦(2−x,y−3). It changes the nonnegative canonical angle of Q7 into the nonpositive canonical angle of Lemma 2. The three data have the following exact owners.

| Lemma datum | Original point | Actual owner |
|---|---|---|
| F=(−.26,0) | G7=(2.26,3) | Q7, label131232 |
| A=(0,−.74) | F5=(2,2.26) | Q7, label131232 |
| Excluded B=(−.26,−1) | G6=(2.26,2) | Distinct Q6, label327936 |

Thus the whole compact cap R is strict in the reflected Q7, and excluded from the reflected actual top square Q11. The latter has closure in y≤1 and strictly owns P=(0,.086) and D=(.4,0), images of its original top marker (2,3.086) and F3=(1.6,3). Theorem 15 of `C981-WALL-CYCLES.md`, with exactly those two strict anchors, wall, and complete foreign cap, gives T=(.73,0) strictly in that reflected Q11. Its inverse image is (1.27,3), as claimed. That theorem proves the conclusion continuously for both signs of the top square and includes all cap tangencies. ∎

## 3. The exact orientation alternative for the mixed northeast label

For Q7=131232, translate Theorem 1 by (2,2). Its owned M,F,G are the actual northeast marker, F5,G7. Its three exclusions are P=(2,3) in Q11, D=G6 in Q6, and X=(2.5,2) in Q6. Therefore a nonpositive canonical angle of Q7 puts (2.5,3) strictly in Q7. Apply the actual corner-to-wall transfer, Theorem 7 of `C1092-DIRECT-WALL-POINT.md`, under (x,y)↦(4−y,4−x): its paired corner is actual Q3, its wall is actual Q10, its b is .914, and its ell is 1.6. The new point excludes the theorem's H from Q3. It follows that (3,2) is strict in Q10.

Together with Corollary 3 this is an exhaustive continuous alternative:

    Q7 nonpositive ⇒ (2.5,3)∈Q7 and (3,2)∈Q10;
    Q7 nonnegative ⇒ (1.27,3)∈Q11.

An axis angle is harmless in both implications; indeed the actual F5,G7 anchors already put the excluded top origin into an axis-parallel Q7, so that angle is itself impossible. The entire segment [1.27,2]×{3} is strictly in the single actual top owner in the second branch. This last assertion uses its established strict origin (2,3).

For Q7=131200 the first branch's two strict points (2.5,3)∈Q7 and (3,2)∈Q10 were established without any orientation assumption in `C974-C976-CENTRAL-CROSSPOINTS.md`.

## 4. A small negative-angle interval for the southeast square

**Theorem 4.** In either remaining actual pair, if Q6 has nonpositive canonical frame u=(c,−s), v=(s,c), c≥s≥0, its half-angle satisfies

    t=s/(1+c)<3/20.                                     (5)

**Proof.** Use coordinates translated by (−2,−2). The actual southeast Q6 strictly owns M=(.35,−.35), D=(.26,0), A=(1,−.26). It excludes C=(0,−.5), which belongs to Q5, and it excludes the actual northeast strict point K=(α,β), where

    (α,β)=(.525,.125) for Q7=131200,
    (α,β)=(.42,.16) for Q7=131232.

The complete negative-sign face argument in Theorem 4 of `C974-C976-CENTRAL-CROSSPOINTS.md` gives

    U≥.5s,   V+a≤αs+βc.                                (6)

The actual bottom wall Q9 strictly owns T=(.8,−1). At T its lower u band follows from M with difference .45c+.65s>0, and its upper v band follows from M with difference .65c−.45s≥.20c>0. An upper u exclusion, together with (6), would imply

    a≤.8c+.5s≤sqrt(.89)<1.

So T must be lower v, V≥.8s−c. With (6),

    a≤(1+β)c+(α−.8)s.                                  (7)

Each right side is strictly decreasing as the canonical angle increases, since 1+β>0 and α−.8<0. At t=3/20 one has c=391/409 and s=120/409. Its two exact values are respectively

    (9/8)c−(11/40)s = 3255/3272<1,
    (29/25)c−(19/50)s = 10199/10225<1.

Thus a>1 and (7) force (5). The zero-angle case is included; this theorem asserts only the interval, not its feasibility. ∎

## 5. Scope

These lemmas strengthen the geometry of the last two exact central pairs. They do not alone give the final contradiction for C974 or C976. The cap belongs to the actual northeast owner; every wall transfer uses its actual adjacent paired corner; the bottom point in Theorem 4 belongs to one actual Q9. In particular, no new long right-wall segment beyond the already established height2.56 has been assumed.
