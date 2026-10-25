# C983 F5-only: the southeast inward point and five right-wall alternatives

Every terminating decimal is an exact rational. All owned points and segments are strict in one named actual open square. Exclusions and supporting contacts may be tangent. The original common side is 1<a≤1001/1000, and all actual closures remain in [0,4]². Only the single-owner component lists in `C983-ORIGINAL-OWNERS.txt` are used for the discrete deductions below.

Assume that the actual merged square has the last F5-only label

    Q7=8224={F5,G3}.

In particular it strictly owns both western markers (1.65,1.65),(1.65,2.35), as well as F5=(2,2.26),G3=(1.74,2). It excludes F4. An auxiliary excluded from an exact component need not be assigned any other owner.

## 1. Two universal actual wall bars and a merged horizontal point

The original Q8 and Q9 components always own F1,G1 and F6,G5, respectively. Theorem 4 of `C981-WALL-CYCLES.md` gives

    {1}×[2.26,2.8] ⊂ Q8,
    [2.26,2.8]×{1} ⊂ Q9                              (1)

strictly. For the first application the strict marker is (.914,2), the strict auxiliary is G1=(1,2.4), and the three exclusions are (1,1.74),(.76,1.87) in actual singleton Q1 and the northwest marker in actual Q7. The genuine wall is x≥0. For the second apply the same theorem after exchanging the two coordinates: its marker and auxiliary come from Q9, its two singleton exclusions (1.74,1),(1.87,.76) come from actual Q0, its central exclusion is the southeast marker in Q5, and its genuine wall is y≥0. In both cases convexity joins strict points of the same actual wall square.

The local Theorem 1 of `C983-F4-LEFT-ORIGIN-AND-CORNER-ROOT.md` does not require F4. Applied after translation by (−2,−2), its three strict anchors are the two western markers and G3 in Q7, and its two excluded markers are those of actual Q5,Q6. It therefore gives

    (1.5,2) ∈ Q7 strictly.                            (2)

No vertical merged crosspoint or merged center is asserted in this chapter.

## 2. The actual southeast square must own G6

**Theorem 1.** Throughout the F5-only merged branch,

    G6=(2.26,2) ∈ Q5 strictly.                        (3)

**Proof.** Suppose Q5 omits G6. Since it also omits F5, which belongs to Q7, direct inspection of its original single-owner list leaves precisely

    262160={F4,G8},
    262400={F8,G8},
    262416={F4,F8,G8}.                               (4)

The first and third possibilities meet Theorem 7 of `C981-WALL-CYCLES.md`. Its strict M,A,B are Q5's original marker, F4 and G8. Its excluded G is the omitted G6. Its other excluded points are (3,1) in the actual paired southeast corner Q2 and (3.086,2), the actual right-wall marker of Q10. Its whole excluded bottom segment is the second segment in (1), belonging to one actual Q9. That theorem excludes both F4-containing cases, including the case where F8 is owned.

It remains to exclude Q5=262400. Since F8 now belongs to Q5, the original right-wall list reduces to

    524800={F9,G9},
    590336={F9,G6,G9},
    524928={F7,F9,G9}.                               (5)

Thus Q10 owns F9,G9. The original Q6 components avoiding F5,G3,F8,F9,G9 all own F7, by direct inspection of that one list. In particular Q6 strictly owns F7=(2.4,3), and excludes F5. Every original top component avoiding F5,F7 owns F3,G4: the only possibilities are 16392 and 147464. Thus Q11 strictly owns F3=(1.6,3),G4=(1.74,3).

We now supply the two actual wall inputs to the upper-square point theorem. Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md`, reflected in x=2, applies to Q10. Its strict anchors are Q10's marker and G9; its two excluded points are F8 in Q5 and the northeast marker in Q6; its genuine wall is x≤4. It gives (3,2.56) strictly in Q10. Consequently

    {3}×[2.26,2.56] ⊂ Q10 strictly.                  (6)

To obtain the top origin, reflect in y=2 and apply Theorem 7 of `C1092-DIRECT-WALL-POINT.md` with actual K=Q4, B=Q11 and parameters b=.914, ell=1.6. The strict K points are the original paired-corner marker (1,3.086) and corner point (1,3). Its excluded point (1,2.5) is strict in the actual Q8 bar (1). The strict B points are Q11's marker (2,3.086) and F3=(1.6,3). The transformed quadrant and wall hypotheses are genuine container walls. The theorem gives

    (2,3) ∈ Q11 strictly.                            (7)

Apply Theorem 3 of `OUTWARD-BAR-AND-UPPER-SPAN.md` to actual Q6. Its strict marker and F7 were just established. Its excluded F5 belongs to Q7, its excluded top origin is (7), its excluded northeast corner point (3,3) belongs to actual paired Q3, and its whole excluded right segment is (6). Hence

    Y=(2.525,2.125) ∈ Q6 strictly.                    (8)

On the other hand, the pure outward Q5 in (4) has strictly negative canonical angle by Theorem 6 of `C981-WALL-CYCLES.md`. Its owned marker and G8, its omitted G6, and the actual Q2 corner, Q10 marker and Q9 bar (1) are exactly that theorem's hypotheses. Reflect Theorem 1 of `OUTWARD-BAR-AND-UPPER-SPAN.md` in y=2. Its owned marker and F8 lie in this same Q5; its omitted G6 is a genuine exclusion; its right marker belongs to Q10; its two bottom-bar points belong to Q9; and its two southeast corner points (3,1),(3.086,1) belong to paired Q2. The just-proved negative angle becomes the required positive angle after reflection. This theorem gives the identical strict point

    Y=(2.525,2.125) ∈ Q5.                             (9)

Equations (8),(9) contradict the disjoint interiors of the two actual central squares. Every possibility in (4) is excluded. This proves (3). ∎

## 3. The remaining single-owner disjunctions

By (3), Q6 and Q10 both omit G6. The original Q6 list, filtered only against the actual Q7 points F5,G3 and actual Q5 point G6, is exactly

    131200={F7,G7},
    524416={F7,G9},
    655488={F7,G7,G9},
    131584={F9,G7},
    524800={F9,G9},
    655872={F9,G7,G9},
    131712={F7,F9,G7},
    524928={F7,F9,G9},
    656000={F7,F9,G7,G9}.                            (10)

In particular every remaining Q6 owns F7 or F9, and G7 or G9. It owns neither F4 nor F8. These are covering disjunctions within one original component list, not assertions that every auxiliary has an owner.

Every original Q10 owns F8 or F9. Hence Q5 cannot own both F8 and F9. Filtering its list against this observation, (3), and the actual Q7 ownership of F5 leaves exactly

    65552={F4,G6},
    327696={F4,G6,G8},
    65792={F8,G6},
    327936={F8,G6,G8},
    65808={F4,F8,G6},
    327952={F4,F8,G6,G8},
    66064={F4,F9,G6}.                               (11)

After G6 is removed, every original Q10 component containing F7 also contains F9. Such a component would exclude both alternatives F7,F9 of Q6 in (10), so it is impossible. The complete necessary right-wall list is therefore

    262400={F8,G8},
    524800={F9,G9},
    262912={F8,F9,G8},
    525056={F8,F9,G9},
    787200={F8,F9,G8,G9}.                           (12)

## 4. Exact five-way owner reduction

Filtering (10),(11) against each individual right-wall alternative gives the following necessary possibilities. No row asserts that arbitrary choices in its cells are jointly feasible.

| Actual Q10 | Possible actual Q5 | Possible actual Q6 | Consequence for Q11 |
|---|---|---|---|
| 262400={F8,G8} | 65552 or 66064 | Any member of (10); if Q5=66064, only 131200,524416,655488 | Retain its original list subject to these actual exclusions |
| 524800={F9,G9} | 65552,327696,65792,327936,65808,327952 | 131200={F7,G7} | Exactly 16392={F3,G4} |
| 262912={F8,F9,G8} | 65552 | 131200,524416,655488 | Retain its original list subject to these actual exclusions |
| 525056={F8,F9,G9} | 65552 or 327696 | 131200={F7,G7} | Exactly 16392={F3,G4} |
| 787200={F8,F9,G8,G9} | 65552 | 131200={F7,G7} | Exactly 16392={F3,G4} |

For the three rows with Q6=131200, both F7 and G7 belong to that actual central square, while F5 belongs to merged Q7. The only original Q11 component avoiding those three points is 16392. This proves the exact top entries in the table directly. All component deductions use only (10)–(12) and the original Q11 list.

## 5. Scope

This chapter proves universal G6 ownership in actual Q5 throughout merged label8224, its seven remaining components (11), the northeast list (10), the five right-wall alternatives (12), and their direct conditional refinements. It also retains the two actual wall bars and the horizontal merged point (1),(2). The full F5-only branch still requires a coupled-square ending. No merged vertical crosspoint, missing bottom origin, favorable angle or new owner for an absent auxiliary has been assumed.
