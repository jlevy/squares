# C1092 MMMP: the northeast outer halfpoint and the right wall origin

All decimals denote exact rationals. Every owner below is an actual original square, with the common side a>1, strict ownership and pairwise disjoint interiors. This transfer uses no center condition after the original MMMP core owners have been established.

**Theorem.** In every original C1092 MMMP configuration,

    (2.5,3) is strictly in Q6,
    (3,2) is strictly in Q10.

In particular the whole segment {3}×[2,2.39] is strict in Q10.

**Proof.** The MMMP core theorem gives Q6's ordinary top pair F7=(2.4,3), G7=(2.26,3), and the direct wall-sign chord gives F9=(3,2.26) in Q10. Apply Theorem 1 of `ORDINARY-MARKER-HALFPOINT.md`, with d=.086, under the simultaneous rotation and translation

    (xi,eta)↦(2−eta,2+xi).

Its complete actual source table is

| Local datum | Original point | Actual strict owner |
|---|---|---|
| M=(.35,−.35) | (2.35,2.35) | Original marker in Q6 |
| A=(1,−.26) | G7=(2.26,3) | Q6 by the MMMP core theorem |
| B=(1,−.4) | F7=(2.4,3) | Q6 by the same theorem |
| Excluded D=(.26,0) | F5=(2,2.26) | Q7 by the core theorem |
| Excluded R=(1.086,0) | (2,3.086) | Original marker in Q11 |
| Excluded K=(1,−1) | (3,3) | Actual paired corner Q2 |
| Excluded F=(.26,−1) | F9=(3,2.26) | Q10 by the wall-sign chord |

Thus the theorem's target (1,−.5) maps to (2.5,3), strictly in Q6.

Now apply the actual two-square transfer, Theorem 7 of `C1092-DIRECT-WALL-POINT.md`, with its K=Q2 and B=Q10, after the simultaneous map from its standard chart

    (x,y)↦(4−y,4−x),
    b=.914, ell=1.74.

The corner's two required strict points (1,b),(1,1) become its original marker (3.086,3) and compulsory paired point (3,3). Its excluded halfpoint (1,1.5) becomes the just-proved (2.5,3), strictly in the different actual Q6. The boundary's marker (2,b) becomes its original (3.086,2), while its anchor (ell,1) becomes F9=(3,2.26), already strict in Q10. The genuine right wall x≤4 becomes the theorem's bottom wall, and both genuine upper/right walls for Q2 become its first-quadrant conditions. All common-side and actual-disjointness premises are preserved by this isometry.

The transfer gives its (2,1) strictly in the transformed B, namely (3,2) strictly in Q10. Finally convexity joins this new origin to Q10's already strict wall-sign segment {3}×[2.22,2.39], giving the stated whole strict segment. ∎

The point (2,3) in the top wall square is not a premise of either step. Its ownership remains a separate obligation unless established by another theorem.
