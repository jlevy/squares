# C1092 MMMP: three central and top-wall ownership conclusions directly from the original entrance

All decimals are exact rationals. Every named owner is one of the original twelve actual open squares, with their common side a>1 and pairwise disjoint interiors. Exclusions remain weak. The proof uses the original complete covering alternatives but no side39 mask closure, moving-marker hull, angle enclosure, or selector history.

## 1. Statement and the few original covering consequences used

Retain the original C1092 marker case and the closed MMMP wall signs

    Y8≥2, X9≥2, Y10≥2, X11≤2.

The complete original F and G families are those of `C1092_shared/01_original_entrance_and_wall_cover.txt`. The labels and point coordinates used below are

| Symbol | Point | Symbol | Point |
|---|---|---|---|
| F1 | (1,2.26) | G1 | (1,2.4) |
| F3 | (1.6,3) | G3 | (1.74,2) |
| F5 | (2,2.26) | G4 | (1.74,3) |
| F7 | (2.4,3) | G5 | (2.26,1) |
| F9 | (3,2.26) | G6 | (2.26,2) |
|  |  | G7 | (2.26,3) |
|  |  | G8 | (3,1.6) |
|  |  | G9 | (3,2.4) |

Every original single-cover label in each of the following rows contains at least one of the three listed points:

| Actual owner | Covering | A compulsory member of this set |
|---|---|---|
| Q7, northwest central | F | {F1,F3,F5} |
| Q7 | G | {G1,G3,G4} |
| Q6, northeast central | F | {F5,F7,F9} |
| Q6 | G | {G6,G7,G9} |
| Q11, top wall | F | {F3,F5,F7} |
| Q10, right wall | G | {G6,G8,G9} |
| Q5, southeast central | G | {G5,G6,G8} |

These seven inclusions are direct properties of the explicit original single-cover lists. They do not select any member of the 55,126-vector family. A point can belong to at most one actual owner, by strict ownership and disjoint interiors.

**Theorem 1.** In every such original MMMP configuration, the actual owners satisfy

    Q7 strictly owns F5 and G3;
    Q6 strictly owns F7 and G7;
    Q11 strictly owns F3 and G4.                       (1)

Moreover Q6 cannot own both G6 and G9. Its exact original combined label is therefore one of

    131200, 196736, 655488,                             (2)

and Q11's exact original label is one of

    16392, 18440.                                     (3)

The structural point conclusions in (1) and the incompatibility of G6,G9 are proved before any exact-label inspection.

## 2. The original wall signs supply every actual foreign chord

The continuous theorem `C1092-WALL-SIGN-CHORD.md` applies directly to the original wall marker, original foreign central marker, actual wall and closed center sign. It gives

    {1}×[2.22,2.39] strictly in Q8,
    [2.22,2.39]×{1} strictly in Q9,
    {3}×[2.22,2.39] strictly in Q10,
    [1.61,1.78]×{3} strictly in Q11.                  (4)

Thus F1,G5,F9,G4 belong respectively to Q8,Q9,Q10,Q11. In particular Q7 excludes F1,G4, so the first two covering rows reduce to

    Q7 owns F3 or F5, and owns G1 or G3.              (5)

## 3. The northwest central must own the inward pair

First Q7 cannot own both F3 and G1. Apply `OUTWARD-CORNER-TWO-GAPS.md` after translation by (2,2) and reflection x↦4−x. Its two outer anchors become F3=(1.6,3), G1=(1,2.4), and its marker becomes the original northwest marker (1.65,2.35). Use parameters r=t=.39. The two excluded gap points become

    (1.61,3) strictly in Q11,
    (1,2.39) strictly in Q8,

by (4), and its excluded outer corner is (1,3), strictly in the original paired corner Q3. The exact distance condition is

    (1−.39)²+(1−.39)²=.7442<1.

All hypotheses belong to actual original owners, so the shared all-angle theorem rules out simultaneous F3,G1 ownership.

Suppose Q7 did not own F5. Then (5) gives F3, so it cannot own G1 and must own G3. Apply the six-point theorem `MIXED-SPAN-FOUR-POINTS.md` under the simultaneous transformation

    (x,y)↦(y,x).

The two strict points of that theorem become G3,F3. Its four excluded points become F5,G4,F1,G1, respectively. The first and fourth are the present hypothesized absences from Q7; the middle two are strict in Q11,Q8. This is a contradiction. Therefore Q7 owns F5.

Suppose instead Q7 did not own G3. Then (5) gives G1; simultaneous F3 ownership is already impossible. Apply the same six-point theorem under the half-turn (x,y)↦(4−x,4−y). Its two owned points become F5,G1, and its four excluded points become G3,F1,G4,F3. Again all four are genuinely excluded from Q7. This contradiction proves G3 ownership. We have established

    F5,G3 strictly in Q7.                            (6)

Every canonical angle is included by the two cited all-angle point theorems; no angle branch has been selected.

## 4. The northeast central owns its two top auxiliaries

Since F5 belongs to Q7 and F9 to Q10, the northeast F-covering row forces

    F7 strictly in Q6.                                (7)

The top-wall F row now has F5,F7 excluded by their actual owners, so

    F3 strictly in Q11.                               (8)

Suppose Q6 excluded G7. Its G-covering row gives G6 or G9.

If it owns G6 but excludes G9, apply `MIXED-SPAN-FOUR-POINTS.md` under the quarter turn R(x,y)=(4−y,x). The owned pair becomes G6,F7. The four excluded points become F5,G7,F9,G9. Here F5 and F9 are strict in Q7,Q10, while G7 and G9 are the current absences. This case is impossible.

It remains that Q6 owns G9. Apply `OUTWARD-CORNER-TWO-GAPS.md` directly after translation by (2,2), with

    r=.26, t=.39.

Its strict points are the original northeast marker, F7 and G9. Its excluded first gap point is G7, the hypothesized absence from Q6. The second gap point is (3,2.39), strictly in Q10 by (4). The excluded corner (3,3) is strict in original paired corner Q2. The exact condition is

    (1−.26)²+(1−.39)²=.9197<1.

This case is impossible as well. Hence

    G7 strictly in Q6.                               (9)

Together, (6)–(9) prove every strict ownership statement in (1).

## 5. A short covering argument removes the remaining triple label

Suppose Q6 owned both G6 and G9. The right-wall G-covering row and disjoint ownership would then force G8 into Q10. But G5 is already in Q9 by (4). The southeast central Q5 would therefore exclude all three of G5,G6,G8, contrary to its original compulsory G-covering row. Thus Q6 cannot own both G6 and G9.

For the exact labels, the original northeast F list, after excluding the actual foreign F3,F5,F9 and requiring F7, contains only the single-point F subset {F7}. The original northeast G list, after requiring G7 and excluding actual foreign G3,G4, contains just

    {G7}, {G6,G7}, {G7,G9}, {G6,G7,G9}.

The last set was just excluded by the three-owner covering argument. Since F7 has bit128 and G6,G7,G9 have G-bits64,128,512, the three remaining combined labels are exactly (2).

For Q11, actual foreign F5,F7 and strict F3 leave just {F3} in its original F list. Actual foreign G7 and strict G4 leave {G4} or {G1,G4} in its original G list. These are the two labels in (3).

Thus this entire ownership conclusion is a consequence of two shared continuous point obstructions, one direct wall-sign chord theorem, and the seven elementary original covering inclusions. None of the 740 historical side39 removals is used as a premise. ∎

## 6. Scope

This theorem replaces the northeast and top-wall ownership part of the old MMMP side39 entrance, directly from the original marker case. It does not yet exclude the whole MMMP sector. The remaining actual southwest, southeast and left/right wall owners retain all their original alternatives consistent with (1)–(3).
