# C983: the merged square must own an inward point

All coordinates and terminating decimals are exact. Every owned point is strictly inside its stated actual square; excluded points and separating supports may be tangent. The proof retains the original C983 marker grouping and exact component families reproduced in `C983-ORIGINAL-OWNERS.txt`. It uses no enumeration of twelve-owner vectors or angle samples.

## 1. A common owner chain when F5 is absent from the merged square

**Theorem 1.** In C983, suppose the actual merged western square Q7 excludes F5=(2,2.26). Then

    F8=(3,1.74)∈Q5,
    F9=(3,2.26), G9=(3,2.4)∈Q10,
    F3=(1.6,3), G4=(1.74,3)∈Q11                     (1)

strictly.

**Proof.** The previous merged-square reductions give Q7 ownership of G3=(1.74,2) and exclusion of F3,G6,G4. Every original bottom-wall Q9 label owns F6=(2.4,1) and G5=(2.26,1). Its strict marker, the actual singleton Q0 points (1.74,1),(1.87,.76), and the foreign southeast marker give the stronger reach (2.8,1) by Theorem 4 of `C981-WALL-CYCLES.md`, transposed. Thus the actual Q9 owns the entire strict bar

    [2.26,2.8]×{1}.                                    (2)

Suppose F8 were absent from Q5. The original Q5 labels are then

    65552,65584,66064,66096,262160,327696,327728.

Every displayed label except 262160 owns F4=(2,1.74) and G6=(2.26,2). The actual short-bar implication in `INWARD-SHORT-BAR-POINT.md`, Section 4, would force F5 into Q7, contradicting this theorem's hypothesis. Label 262160 owns F4,G8 and excludes G6,F8. Theorem 5 of `C981-WALL-CYCLES.md` excludes it using the same actual bar (2). Hence Q5 owns F8.

The only original right-wall labels avoiding F8 are

    524800,524928,590336.

All three own F9,G9. Consequently the northeast Q6 excludes F9,G9 and also G3 in Q7. Direct inspection of its original component list gives the two covering disjunctions

    Q6 owns F5 or F7,
    Q6 owns G6 or G7.                                  (3)

Suppose Q11 owned F7=(2.4,3). Every original top label containing F7 also contains G7=(2.26,3). Thus (3) forces F5,G6 into Q6 and excludes F7 from it. Because G6 now belongs to Q6 and F8 to Q5, the remaining Q5 labels are just

    262400={F8,G8}, 262416={F4,F8,G8}.

The complete inward–outward duplicate-point argument applies with the following actual sources. The inward theorem in `C1084-DUPLICATE-POINT.md`, Theorem 1, reflected in y=2, puts (2.46,2.01) strictly in Q6. Its anchors are Q6's northeast marker and F5,G6; its exclusions are the southeast marker in Q5, northwest marker in Q7, and F7 in Q11.

Theorem 6 of `C981-WALL-CYCLES.md` forces actual Q5 to have a strictly negative canonical angle. Its strict anchors are Q5's southeast marker and G8. Its exclusions are G6 in Q6, the paired corner point (3,1) in Q2, the right-wall marker in Q10, and the whole actual bar (2). Reflect Theorem 2 of `C1084-DUPLICATE-POINT.md` in y=2. Its strict anchors become Q5's marker and F8; its exclusions are G6 in Q6, the right-wall marker in Q10, the two bar endpoints in Q9, and (3,1),(3.086,1) in the actual paired corner Q2. The just-proved angle supplies its sign premise. It therefore puts the same (2.46,2.01) strictly in Q5.

The two distinct actual central squares cannot share that strict point. Thus Q11 cannot own F7. Its original labels avoiding F7 are exactly

    16392,16424,147464,147496,

all containing F3,G4. This proves (1). Optional F4 in Q5 was retained throughout and was not changed into an exclusion. ∎

## 2. The corner point supplied by that actual top owner

Under Theorem 1, the left-wall Q8 strictly owns (1,2.8). Apply Theorem 4 of `C981-WALL-CYCLES.md` to Q8's original marker and G1=(1,2.4). Its excluded F0=(1,1.74) and (.76,1.87) lie in actual singleton Q1; its excluded northwest marker lies in actual Q7. This supplies the claimed reach, independently of any top-square angle or center.

Paired northwest corner Q4 strictly owns (1,3). Apply Theorem 5 of `OTHER-GEOMETRY.md` to this actual Q4 under

    (ξ,η)=(1−x,y−3).

The theorem's strict origin is the paired-corner point. Its excluded F=(−.6,0) comes from F3=(1.6,3) in actual Q11 by Theorem 1; its excluded H=(0,−.2) comes from the just-proved (1,2.8) in actual Q8. The transformed upper wall η≤1 is the genuine original top container wall. Choose

    p=.2, q=.6, r=.22.

The exact parameter checks are

    p²+q²=.4<1,
    p²+r²=.0884<1,
    q+r=.82<2sqrt(2)−2,

the last following from (141/100)²<2. Hence

    (.78,3)∈Q4 strictly.                               (4)

No surrogate corner or inferred ownership of an unassigned point was used.

## 3. The label with neither inward point is impossible

**Theorem 2.** In every original C983 configuration, actual merged Q7 owns at least one of F4=(2,1.74), F5=(2,2.26).

**Proof.** Suppose it owned neither. It then meets the hypotheses of Theorem 6 of `OTHER-GEOMETRY.md` after

    (ξ,η)=(2−x,y−2).

Its strict anchors (.35,±.35) are the two original western central markers, both in Q7. The four excluded chord endpoints (0,±.26),(1,±.26) are the images of F4,F5, excluded by the current supposition, and F0,F1, strictly in actual Q1,Q8. The extra excluded whole segment from (1.086,0) to (1,.26) is the image of the segment from Q8's original marker (.914,2) to its F1=(1,2.26). Both endpoints belong strictly to the same actual Q8. That theorem therefore supplies, in the original coordinates,

    (.98,2), (.98,2.02), (1.04,2.11)∈Q7 strictly.       (5)

Theorem 1 and Section 2 apply because F5 is absent. Transform the actual left-wall Q8 by

    (ξ,η)=(1−x,y−2).

Every datum of `SHORTER-CORNER-WALL-OBSTRUCTION.md`, Theorem 1, now has an actual source:

| Local datum | Original point or wall | Actual source |
|---|---|---|
| Strict P=(.086,0) | (.914,2) | Q8's original marker |
| Strict B=(0,.26) | (1,2.26) | Q8's F1 |
| Strict C=(0,.8) | (1,2.8) | Section 2, in the same Q8 |
| Excluded D0=(.02,0) | (.98,2) | Q7 by (5) |
| Excluded D1=(.02,.02) | (.98,2.02) | Q7 by (5) |
| Excluded D2=(−.04,.11) | (1.04,2.11) | Q7 by (5) |
| Excluded E=(.22,1) | (.78,3) | Actual corner Q4 by (4) |
| Closure in ξ≤1 | Original x≥0 | Q8's genuine left container wall |

That complete continuous wall obstruction is impossible. This proves Theorem 2. ∎

## 4. Updated exact scope

The previous three merged-owner exclusions eliminated F3,G6,G4. They left exactly 8192,8208,8224,8240. Theorem 2 now eliminates 8192, which owns only G3. The remaining necessary merged labels are

    8208={F4,G3},
    8224={F5,G3},
    8240={F4,F5,G3}.

Theorem 1 and its proved actual corner reach also hold in the first remaining label 8208. A complete ending for these three labels is still needed. This chapter is the complete exclusion of the no-inward-point branch and does not use the unproved remaining family ending.
