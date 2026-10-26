# The actual left origin and the second missing-corner midpoint

All decimals are exact rationals. Every asserted owned point is strict. The owner labels and compulsory original hulls are the retained entrance reproduced in `C974-ORIGINAL-ENTRANCE.txt`; the continuous reductions cited below are applied to the same actual owners.

## 1. The actual top wall supplies the corner exclusion

In both final C974 central pairs, the top square Q11 has exact label16392 and owns its original marker (2,3.086) and F3=(1.6,3). The northeast owner Q7 strictly owns G7=(2.26,3), and the northwest marker (1.65,2.35) is globally absent.

Apply Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md` to Q11 under the simultaneous isometry

    (ξ,η)=(4−y,4−x).

Here is its exact input map:

| Local theorem datum | Original point or wall | Actual source |
|---|---|---|
| Strict (.914,2) | (2,3.086) | Q11 original marker |
| Strict (1,2.4) | (1.6,3) | Q11 F3 |
| Excluded (1,1.74) | (2.26,3) | Strict in distinct Q7 |
| Excluded (1.65,2.35) | (1.65,2.35) | Globally absent northwest marker |
| Wall ξ≥0 | Original y≤4 | Genuine top container wall |

Its target (1,2.56) therefore proves

    (1.44,3) is strictly in actual Q11.                 (1)

Convexity with the strict F3=(1.6,3) now gives

    H=(1.5,3) is strictly in actual Q11.                (2)

This short reach argument does not assume the origin (2,3), any angle sign, or a center estimate.

## 2. The actual northwest corner transfers the left origin

Apply Theorem 7 of `C1092-DIRECT-WALL-POINT.md` with actual corner K=Q4, actual wall B=Q8, and

    (X,Y)=(4−y,x), b=.914, ell=1.6.

Every premise of that all-angle, actual two-square theorem has the following source:

| Local theorem datum | Original point or wall | Actual source |
|---|---|---|
| K owns (1,b) | (.914,3) | Original Q4 marker |
| K owns (1,1) | (1,3) | Compulsory paired-corner point of Q4 |
| K excludes (1,1.5) | (1.5,3) | The strict Q11 point (2) |
| B owns (2,b) | (.914,2) | Original Q8 marker |
| B owns (ell,1) | (1,2.4) | Original strict auxiliary in Q8 |
| K in the first quadrant | Original y≤4,x≥0 | Two genuine corner walls |
| B above Y=0 | Original x≥0 | Genuine left container wall |

The two squares are distinct actual owners, with the original common side a>1 and disjoint open interiors. Since 0<b<1 and 1<ell<2, the theorem applies and gives (2,1) strictly in the transformed B. Returning to original coordinates,

    (1,2) is strictly in actual Q8.                    (3)

Thus the left origin is available uniformly in both final C974 central pairs and in both missing-corner roots. The use of the globally absent marker in Section 1 is only an exclusion from Q11; no segment starting at that absent marker has been introduced.

## 3. The second missing-corner singleton owns its midpoint

The retained C974 entrance splits the missing southwest corner into two exhaustive roots. The first has Q0 excluding E=(1,1). The second has Q0 owning E and Q1 excluding E. In that second root, the retained missing-corner consequence supplies the strict Q1 points

    (.914,1), (1,1.82), (.76,1.96).                    (4)

Use the simultaneous transpose and translation

    (u,v)=(y−1,x−1).

Apply Theorem 1 of `MISSING-CORNER-MIDPOINT.md`, with its actual singleton K=Q1 and wall W=Q8. Its exact hypotheses are:

| Local theorem datum | Original point or condition | Actual source |
|---|---|---|
| K owns (0,−.086),(.82,0),(.96,−.24) | The three points (4) | Same actual Q1 |
| K excludes (0,0) | (1,1) | Present second missing-corner root |
| K lies in v≥−1 | Original x≥0 | Genuine left wall |
| W owns (1,0) | (1,2) | New actual left origin (3) |
| W owns (1,−.086) | (.914,2) | Original Q8 marker |
| W owns (1.8,0) | (1,2.8) | C974 strong Q8 reach, from Theorem 4 of `C981-WALL-CYCLES.md` with its exact source map in Section 3.2 of `C974-C976-CONTINUOUS-REDUCTIONS.md` |
| W excludes (1.35,.65) | (1.65,2.35) | Globally absent northwest marker |
| W excludes (2,0) | (1,3) | Actual paired corner Q4 |
| W excludes (1,.5) | (1.5,2) | Actual Q5 crosspoint, sourced in `C974-C976-SW-SUPPORT-POINT.md`, Section 8 |
| W excludes (2,.5) | (1.5,3) | Strict actual Q11 point (2) |

All required exclusions therefore hold for their literal actual sources. The cited midpoint theorem includes the preceding all-angle sign deductions, so no sign hypothesis is added here. Its strict target (1,−.5) translates back to

    Q1 excludes (1,1)  ⇒  (.5,2) is strictly in Q1.    (5)

The same sign deductions also say that the original canonical angles of Q1 and Q8 are both strictly negative, since the simultaneous transpose reverses their signs.

This is the complete singleton half of the second missing-corner root. To finish that root by a duplicate-point contradiction, one must prove (.5,2) strictly in the distinct actual Q8. The diagonal foreign-segment premise of `BOTTOM-WALL-LOWER-MIDPOINT.md` is not supplied merely by the absent northwest marker: Section 1 has used that marker only as an excluded point. No such segment or further ownership is claimed here.
