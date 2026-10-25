# C983 F5-only: the actual left origin whenever the northeast owns G7

All owned points are strict in the one named actual open square. Exclusions allow tangency. The side, disjointness and container conditions remain those of the original C983 configuration. Assume merged Q7=8224 and the reductions of `C983-F5-CENTRAL-REDUCTION.md` and `C983-F5-LOWER-RIGHT-EXCLUSION.md`.

**Theorem.** If G7=(2.26,3) belongs to actual Q6, then

    (1.44,3),(1.5,3) ∈ Q11,
    (1,2) ∈ Q8,
    (1,1) ∈ Q1,
    (1.82,1),(1.96,.76) ∈ Q0                     (1)

strictly. In particular Q0 excludes (1,1), and {1}×[2,2.8] belongs strictly to the one actual Q8.

The only remaining northeast alternative not covered by the theorem is Q6=524416={F7,G9}; it occurs only with Q10=262912. The theorem covers both other northeast labels, 131200={F7,G7} and 655488={F7,G7,G9}.

## 1. Top ownership and the two wall transfers

After the lower-right exclusion, actual Q6 always owns F7. In the present G7 case, Q11 must omit F7,G7 as well as F5 in actual Q7. Direct inspection of the original Q11 list therefore leaves exactly

    Q11=16392={F3,G4}.                             (2)

Apply the local wall advance, Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md`, to Q11 under (ξ,η)=(4−y,4−x). Its owned marker (.914,2) becomes the actual Q11 marker (2,3.086); its owned (1,2.4) becomes F3=(1.6,3) in (2). Its excluded (1,1.74) becomes G7=(2.26,3) in actual Q6, and its excluded central marker becomes the northwest marker (1.65,2.35), strictly owned by merged Q7. Its wall ξ≥0 is the genuine original top wall y≤4. It gives (1.44,3) strictly in Q11. Convexity with its strict F3 gives (1.5,3) in the same Q11.

Now use actual paired northwest corner Q4 and actual Q8 in Theorem 7 of `C1092-DIRECT-WALL-POINT.md`, under

    (X,Y)=(4−y,x), K=Q4, B=Q8,
    b=.914, ell=1.6.

Its K points (1,b),(1,1) are the original Q4 marker (.914,3) and paired-corner point (1,3). Its excluded K point (1,1.5) is the just-proved (1.5,3) in Q11. Its B marker (2,b) is the Q8 marker (.914,2), and its B point (ell,1) is G1=(1,2.4), present in every original Q8 component. The actual quadrant and wall conditions are original y≤4,x≥0 and original x≥0, respectively. The physical common side and disjointness are retained. The theorem therefore gives

    (1,2) ∈ Q8 strictly.                           (3)

The universal strong left bar already gives (1,2.8) strictly in Q8. Convexity supplies the full strict segment {1}×[2,2.8] in this same actual square.

## 2. The southwest corner belongs to Q1

The entire actual-square proof in Section 4 of `C983-F4-LEFT-ORIGIN-AND-CORNER-ROOT.md` now transfers literally. To make its independence of F4 explicit, its complete actual inputs are:

| Input to that section | Source in the present F5-only branch |
|---|---|
| Original Q0,Q1,Q8,Q9 markers | The unchanged original actual owners |
| Southwest and northwest markers in Q7 | Both original merged markers, retained in label8224 |
| (1.5,2) strictly in Q7 | The universal horizontal midpoint from Section 1 of `C983-F5-CENTRAL-REDUCTION.md` |
| (1,2),(1,2.8) strictly in Q8 | Equation (3) and the universal actual left bar |
| (1.5,3) strictly in Q11 | Section 1 above |
| (1,3) strictly in Q4 | The original paired northwest corner point |
| Original walls and all three pairwise separations of Q1,Q8,Q4 | Their genuine container and packing conditions |

For completeness, the implication is as follows. If Q1 excluded (1,1), the retained missing-corner point lemma, with coordinates exchanged, would give (1,1.82),(.76,1.96) strictly in that same Q1, in addition to its marker (.914,1). Transport the complete three-square local theorem from `C974-THREE-SQUARE-ENDING.md` by (ξ,η)=(y−1,x−1), taking K=Q1,W=Q8,C=Q4. Its K anchors become exactly those three strict points; its missing K origin is the temporary missing (1,1). Its three strict W points come from (.914,2),(1,2),(1,2.8). Its W exclusions come from the northwest marker in Q7, the horizontal point (1.5,2) in Q7 and the top point (1.5,3) in Q11. Its C anchor is (1,3), and its C exclusion is the same point (1.5,3). Its floor and corner walls are the actual transformed x≥0,y≤4 conditions. Thus all hypotheses of that actual three-square theorem hold and give a contradiction.

Consequently (1,1) is strict in Q1. Disjointness excludes it from Q0. The same retained missing-corner point lemma, without exchanging coordinates, now applies to Q0: its strict marker is (1,.914), its foreign markers (.914,1),(.914,2),(1.65,1.65) belong to Q1,Q8,Q7, and its missing corner is (1,1). It gives (1.82,1),(1.96,.76) strictly in the same actual Q0. This proves every assertion in (1). ∎

## 3. Scope

This chapter imports no F4 hypothesis from the earlier chapter's title: each local point source and every actual owner used in its argument is displayed above. It supplies a strengthened actual left and singleton entrance when G7 belongs to Q6. Neither a bottom-wall origin nor a vertical merged midpoint is asserted here, and the one remaining G7-absent northeast component remains outside this conditional theorem.
