# C1092 MPPM: ordinary central points remove the neighboring wall's inner auxiliary

All terminating decimals are exact rationals. Retain the actual owners, original component families and closed MPPM signs of C1092-ORIGINAL-ENTRANCE.txt. This chapter is in the no-omission branch of C1092-MPPM-NO-OMISSION-REDUCTION.md. In particular the four actual ordinary wall pairs are

    Q8:F1,G1; Q9:F2,G2; Q10:F8,G8; Q11:F7,G7.

The paired corners retain their strictly owned inner corner points. The common side is 1<a≤1.001, and all interiors are pairwise disjoint.

## 1. A whole-wall-segment exclusion

**Theorem 1.** The following actual-owner implications hold:

    F0 in Q4  implies G3 outside Q8;
    G5 in Q5  implies F4 outside Q9;
    F9 in Q6  implies G6 outside Q10;
    G4 in Q7  implies F5 outside Q11.                 (1)

The premise in each row is only the indicated single ordinary auxiliary; the whole ordinary central pair need not have been proved.

**Proof.** Suppose F0=(1,1.74) is strict in Q4 and G3=(1.74,2) is strict in Q8. The original marker (.914,2) and G3 belong to the same actual open Q8. Their convex hull therefore puts the entire segment

    [1,1.65]×{2}

strictly in Q8, hence outside the closed Q4. Q4 strictly owns F0 and its original marker (1.65,1.65). Its two lower points (1,1) and (1.65,1) are excluded: the first is strict in the actual paired Q0, and the second is on the actual Q9 segment joining F2=(1.6,1) to G2=(1.74,1).

Translate by (−1,−1). Theorem 3 of OTHER-GEOMETRY.md now applies to Q4 with

    r=13/20, h0=37/50, h1=13/20.

Its strict anchors are (0,h0),(r,h1); its two lower excluded points are (0,0),(r,0); and its whole upper excluded segment is [0,r]×{1}. The range 1/2≤r≤2sqrt(2)−2 holds. That theorem gives a contradiction for every orientation and every a>1, including all possible tangencies to the excluded data. This proves the first row.

The simultaneous quarter-turn R(x,y)=(4−y,x) preserves the actual container, entrance and MPPM signs. Its successive images give the remaining three rows. In particular R maps F0 to G5, G3 to F4, Q4 to Q5 and Q8 to Q9. No point from a rotated configuration is added to an unrotated owner. ∎

## 2. The all-four-ordinary central subbranch

Suppose the four actual central ordinary pairs are all strict:

    Q4:F0,G0; Q5:F6,G5; Q6:F9,G9; Q7:F3,G4.          (2)

Then the original component lists and (1) force the four exact boundary labels

    Q8=2050, Q9=4100, Q10=262400, Q11=131200.          (3)

For example Q8 owns F1,G1, while F0,G0 are foreign in Q4 and F3,G4 are foreign in Q7. Theorem 1 additionally excludes G3 from Q8. Filtering the complete original Q8 component list by exactly these facts leaves only2050. The other three rows are its simultaneous rotations. Each paired-corner component has only label0 or a label containing an auxiliary already in one of the actual adjacent ordinary central/wall owners, so the four corner labels are exactly0 as well.

Define the forward inner points by the literal sector table

| Actual central owner | Its ordinary pair | Its forward inner point |
|---|---|---|
| Q4 | F0,G0 | G3=(1.74,2) |
| Q5 | F6,G5 | F4=(2,1.74) |
| Q6 | F9,G9 | G6=(2.26,2) |
| Q7 | F3,G4 | F5=(2,2.26) |

**Corollary 2.** Under (2), at least one central owner excludes its forward inner point.

Indeed, if all four forward points belonged to their indicated owners, every auxiliary would now have its actual owner. The exact assignment would be

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

This is excluded by the complete all-sign theorem C1092-DIRECT-LAST-ASSIGNMENT.md, from the same original MPPM signs and actual corner owners. No preceding reduced-vector catalogue is required. ∎

## 3. Every omitted forward point supplies a genuine wall origin

**Corollary 3.** In the subbranch (2), an owner that omits its forward point forces the following strict points:

| Missing point | Strict central halfpoint | Strict point in the next actual boundary |
|---|---|---|
| G3 outside Q4 | (1,1.5) in Q4 | (2,1) in Q9 |
| F4 outside Q5 | (2.5,1) in Q5 | (3,2) in Q10 |
| G6 outside Q6 | (3,2.5) in Q6 | (2,3) in Q11 |
| F5 outside Q7 | (1.5,3) in Q7 | (1,2) in Q8 |

For the first row apply ORDINARY-MARKER-HALFPOINT.md under the map from its local coordinates (xi,eta) to (2−xi,2+eta), with d=.086. Its actual central square is Q4; its ordinary pair is F0,G0; and its excluded points are the missing G3, the left marker in Q8, the inner corner in Q0, and G2 in Q9. Its strict conclusion is (1,1.5). This excludes that point from actual Q0. The all-angle paired-corner transfer, Theorem 7 of C1092-DIRECT-WALL-POINT.md, now applies with K=Q0, B=Q9, b=.914 and ell=1.6. The strict K anchors are (1,.914),(1,1), and the strict B anchors are (2,.914),F2. Its conclusion is (2,1) in Q9. All other rows are simultaneous quarter-turns of this full source map.

The first theorem is valid even when some central pairs in (2) are absent. The two corollaries describe a further reduction of the all-four-ordinary subbranch. A mixed family of ordinary, inward and elbow central owners remains within the preceding radial reduction until a separate actual-neighbor argument closes it; neither chapter silently identifies that family with the last assignment.
