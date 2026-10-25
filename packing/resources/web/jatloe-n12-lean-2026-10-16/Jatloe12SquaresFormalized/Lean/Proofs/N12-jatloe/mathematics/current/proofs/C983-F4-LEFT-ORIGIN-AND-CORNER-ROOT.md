# C983 F4: the actual left origin and the surviving missing-corner root

Every decimal is an exact rational. All owned points below are strictly inside the one named actual open square. Excluded points and supports may be tangent. The C983 squares have their original common side 1<a≤1001/1000, disjoint interiors, and closures in [0,4]². The component entrance is `C983-ORIGINAL-OWNERS.txt`, and the necessary F4 component reduction is `C983-F4-CENTRAL-REDUCTION.md`.

Assume throughout that actual merged Q7 owns F4. Thus its remaining label is8208 or8240. No whole C974 ownership pattern is imported. The applications below transport only stated local theorems, with their C983 premises individually supplied.

## 1. A horizontal midpoint of the actual merged owner

**Theorem1.** Let Q be any open square of side a>1. Suppose Q strictly owns

    P=(−.35,−.35), R=(−.35,.35), D=(−.26,0),

and excludes both

    E_−=(.35,−.35), E_+=(.35,.35).

Then X=(−.5,0) is strictly in Q. No wall or upper side bound is required.

**Proof.** Write Q's lower faces as U,V and its upper faces as U+a,V+a. First use a nonnegative canonical frame

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1.

At X its upper u band follows from D, with increment .24c>0. Its lower v band follows from P, with increment .35c+.15s>0; its upper v band follows from R, with increment .35c−.15s≥.20c>0. If X were missing, its only possible exit would therefore give

    U≥−.5c.                                           (1)

At the excluded E_+, the lower u band follows from D, with increment .61c+.35s>0. Its lower v band follows from P, with increment .7(c−s)≥0. Its upper v band follows from R, with increment .7s≥0. Zero increments still give strict bands through the strict comparison points. Finally (1) gives

    u(E_+)−U≤.85c+.35s
                 ≤sqrt(.85²+.35²)=sqrt(.845)<1<a.

Its upper u band would be strict as well. This contradicts exclusion of E_+.

For a nonpositive canonical frame

    u=(c,−s), v=(s,c), c≥s≥0,

X again has its upper u band from D. Its lower and upper v bands follow respectively from P,R, now with increments .35c−.15s>0 and .35c+.15s>0. A failure again gives (1). Use E_− in this sign. Its lower u band follows from D with increment .61c+.35s>0. Its lower v band follows from P with increment .7s≥0, and its upper v band follows from R with increment .7(c−s)≥0. The same bound sqrt(.845)<1<a gives its strict upper u band, another contradiction. Both signs, the axial case, the canonical diagonal and every weak exterior contact have been included. ∎

For C983 apply Theorem1 after translation by (−2,−2). The two western markers and G3 are all strict in the same merged Q7. The excluded E_− and E_+ are the original southeast and northeast markers, strict in actual Q5 and Q6. Consequently

    (1.5,2) is strictly in actual Q7.                  (2)

This proof does not assert the different point (2,1.5) in Q7.

## 2. The actual top square advances to the left

The F4 reduction gives Q11=16392={F3,G4}, and Q6 owns G7 in either of its remaining components131200,131232. Apply Theorem1 of `C974-C976-CONTINUOUS-REDUCTIONS.md` to Q11 under the simultaneous isometry

    (ξ,η)=(4−y,4−x).

Its complete source map is:

| Local theorem datum | Original point or wall | Actual C983 source |
|---|---|---|
| Strict (.914,2) | (2,3.086) | Q11 marker |
| Strict (1,2.4) | (1.6,3) | F3 in Q11 |
| Excluded (1,1.74) | (2.26,3) | G7 in actual Q6 |
| Excluded (1.65,2.35) | (1.65,2.35) | Northwest marker in merged Q7 |
| Closure in ξ≥0 | Original y≤4 | Genuine top container wall |

The resulting strict target is

    (1.44,3) in actual Q11.                            (3)

Together with its original strict F3=(1.6,3), convexity of that same Q11 gives

    (1.5,3) in actual Q11.                             (4)

This argument uses the northwest marker only as a point excluded from Q11. Its ownership in merged Q7 is fully retained.

## 3. The actual northwest corner transfers the left origin

Apply Theorem7 of `C1092-DIRECT-WALL-POINT.md` to the actual pair K=Q4,B=Q8 under

    (X,Y)=(4−y,x), b=.914, ell=1.6.

The exact premises are:

| Local theorem datum | Original point or condition | Actual C983 source |
|---|---|---|
| K owns (1,b) | (.914,3) | Q4 original marker |
| K owns (1,1) | (1,3) | Q4 compulsory paired-corner point |
| K excludes (1,1.5) | (1.5,3) | Strict point (4) of Q11 |
| B owns (2,b) | (.914,2) | Q8 original marker |
| B owns (ell,1) | (1,2.4) | G1 in Q8 |
| K in the first quadrant | Original y≤4 and x≥0 | Genuine corner walls |
| B in Y≥0 | Original x≥0 | Genuine left wall |

The two actual squares have their physical common side a>1 and disjoint interiors. The inequalities 0<b<1 and 1<ell<2 hold. The theorem therefore supplies its strict target (2,1) in the transformed B, or

    (1,2) strictly in actual Q8.                       (5)

Together with the already proved strict (1,2.8) in Q8, this gives the whole strict segment {1}×[2,2.8] in this one actual wall owner.

## 4. If Q1 misses the southwest corner, the three-square theorem applies

Suppose actual Q1 excludes E=(1,1). The inherited missing-corner local lemma is recorded verbatim as a statement, with its primary-source attribution, in Section4 of `C974-ORIGINAL-ENTRANCE.txt`: a square of side greater than one in [0,4]² owning (1,.914) and excluding (.914,1),(.914,2),(1.65,1.65),(1,1) strictly owns (1.82,1),(1.96,.76). This is the named Lemma11 of Bentz (2010), already part of that approved local entrance. Its coordinate-exchanged application to C983 Q1 is literal:

| Untransposed lemma datum | Original point after exchanging coordinates | Actual C983 source |
|---|---|---|
| Strict (1,.914) | (.914,1) | Q1 marker |
| Excluded (.914,1) | (1,.914) | Q0 marker |
| Excluded (.914,2) | (2,.914) | Q9 marker |
| Excluded (1.65,1.65) | (1.65,1.65) | Southwest marker in merged Q7 |
| Excluded (1,1) | (1,1) | Present supposition |
| Closure in [0,4]² | Same square container | Original genuine walls |

Thus this same actual Q1 strictly owns

    (.914,1), (1,1.82), (.76,1.96).                    (6)

Now transport Theorem1 of `C974-THREE-SQUARE-ENDING.md` under

    (ξ,η)=(y−1,x−1),

using the actual three squares

    K=Q1, W=Q8, C=Q4.

Every premise of that local theorem has the following C983 source:

| Theorem datum | Original point or condition | Actual source |
|---|---|---|
| K owns P=(0,−.086), A=(.82,0), S=(.96,−.24) | Three points in (6) | Same actual Q1 |
| K excludes E=(0,0) | (1,1) | Present supposition |
| K has closure in η≥−1 | Original x≥0 | Genuine Q1 wall |
| W owns O=(1,0) | (1,2) | New strict origin (5) in Q8 |
| W owns P_W=(1,−.086) | (.914,2) | Q8 marker |
| W owns R=(1.8,0) | (1,2.8) | Strong actual Q8 bar in the F4 reduction |
| W excludes M=(1.35,.65) | (1.65,2.35) | Northwest marker in actual merged Q7 |
| W excludes F0=(1,.5) | (1.5,2) | New strict Q7 point (2) |
| W excludes F1=(2,.5) | (1.5,3) | New strict Q11 point (4) |
| C owns A_C=(2,0) | (1,3) | Actual Q4 paired-corner point |
| C excludes F1 | (1.5,3) | Same actual Q11 point (4) |
| C has closure in ξ≤3,η≥−1 | Original y≤4,x≥0 | Genuine Q4 corner walls |

These are three of the original twelve actual squares, so their common side and all three pairwise interior separations are physical. The three-square theorem uses M solely as an excluded point; the fact that C983 places that marker in merged Q7 therefore supplies precisely its required premise. The theorem gives a contradiction.

Consequently

    (1,1) is strictly in actual Q1.                    (7)

Since Q0 and Q1 have disjoint interiors, (7) excludes (1,1) from Q0. Apply the same inherited missing-corner lemma without exchanging coordinates to Q0. Its foreign markers (.914,1),(.914,2),(1.65,1.65) belong respectively to Q1,Q8,Q7. Hence

    (1.82,1), (1.96,.76) are strictly in actual Q0.     (8)

## 5. Exact scope

Throughout both remaining F4 merged labels, this chapter proves the actual midpoint (2), top points (3),(4), left origin (5), the exclusion of the entire root where Q1 misses (1,1), and the strengthened singleton points (8) in the surviving root. The transfer in Section4 depends on the complete local Theorem1 in `C974-THREE-SQUARE-ENDING.md`, not on that chapter's C974 owner-family conclusion.

The surviving C983 root has (1,1) strict in Q1 and excluded from Q0. A full contradiction in that root is still required. In particular, neither a strict point (2,1.5) in merged Q7 nor an unconditional bottom origin has been inferred here. This chapter does not claim that either full F4 label, or the F5-only merged label8224, is completely excluded.
