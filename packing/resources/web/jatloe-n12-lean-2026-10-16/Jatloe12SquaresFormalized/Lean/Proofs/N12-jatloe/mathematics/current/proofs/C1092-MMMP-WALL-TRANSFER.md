# C1092 MMMP: an actual top-wall advance and the left-wall origin

All terminating decimals are exact rationals. This chapter retains the original twelve actual squares, their common side a>1, their disjoint open interiors, their real container walls, and the closed MMMP center signs. Strict points are always in the named actual owner. No angle or historical center restriction is added.

## 1. Statement

**Theorem 1.** Every original MMMP configuration satisfies

    (1.44,3) strictly in Q11,
    (1,2) strictly in Q8.                             (1)

Consequently its actual top and left squares strictly contain the entire segments

    [1.44,1.78]×{3} in Q11,
    {1}×[2,2.39] in Q8.                             (2)

The proof uses the direct original ownership reduction in `C1092-MMMP-CORE-OWNERS.md`. In particular, that theorem has already established F3=(1.6,3) in Q11, G7=(2.26,3) in Q6, and F5=(2,2.26) in Q7. The wall-sign chord theorem has established [1.61,1.78]×{3} in Q11 and {1}×[2.22,2.39] in Q8. None of those facts depends on either conclusion in (1).

## 2. The top wall advances past the corner halfpoint

Apply the complete all-orientation wall-reach lemma in Section A.2 of `C981-RETAINED-CONTINUOUS-LEMMAS.md` to the one actual square Q11, in coordinates

    (X,Y)=(4−y,4−x).

Its real top wall y≤4 becomes X≥0. Its two strict anchors and two genuine exclusions become

| Datum | Original point and actual source | Transformed point |
|---|---|---|
| Strict marker | (2,3.086) in Q11 | (.914,2) |
| Strict anchor | F3=(1.6,3) in Q11 | (1,2.4) |
| Excluded wall point | G7=(2.26,3) in Q6 | (1,1.74) |
| Excluded inner point | F5=(2,2.26) in Q7 | (1.74,2) |

The lemma's exact parameters are (w,d0,z)=(1.74,1.74,2.56). Their required inequalities are

    z−w=.82<14/17,
    (d0−1)²+(2−w)²=.6152<1,
    (z−2)²+(d0−1)²=.8612<1.

Thus (1,2.56) in the transformed chart is strict in Q11. In the original chart it is (1.44,3). By convexity with the already strict top chord, the whole first segment in (2) is strict. In particular,

    H_top=(1.5,3) strictly belongs to Q11.            (3)

It is therefore excluded from the different actual northwest corner Q3.

## 3. The actual northwest corner transfers the left-wall origin

Use Theorem 7 of `C1092-DIRECT-WALL-POINT.md` with its boundary B=Q8 and corner K=Q3, under the simultaneous map from that theorem's chart to the original chart

    (x,y)↦(y,4−x).

The parameters are b=.914 and ell=1.74; in particular 0<b<1 and 1<ell<2. Every required datum has the following actual source:

| Standard datum | Original point | Actual source |
|---|---|---|
| B owns (2,b) | (.914,2) | Original marker in Q8 |
| B owns (ell,1) | (1,2.26) | Direct wall-sign chord in Q8 |
| K owns (1,b) | (.914,3) | Original corner marker in Q3 |
| K owns (1,1) | (1,3) | Original paired-corner inner point in Q3 |
| K excludes (1,1.5) | (1.5,3) | Strict point of Q11 from (3) |

The standard lower wall y≥0 is the genuine original left wall x≥0. The standard first-quadrant constraint on K becomes the two genuine original constraints x≥0 and y≤4. B and K are distinct actual squares of the original common side and have disjoint interiors.

The all-angle transfer theorem therefore gives its strict target (2,1) in B. Its original image is (1,2), proving the second assertion of (1). Convexity with the already strict endpoint (1,2.39) proves the second segment in (2). No premise that Q8 owns G1=(1,2.4) has been used. ∎

## 4. Scope

These are direct facts for the whole original MMMP sector. The left midpoint remains valid when G1=(1,2.4) belongs to another square or is unowned. A further central or support contradiction is still required to exclude MMMP; this chapter does not infer the central point (2,2) from the wall origins alone.
