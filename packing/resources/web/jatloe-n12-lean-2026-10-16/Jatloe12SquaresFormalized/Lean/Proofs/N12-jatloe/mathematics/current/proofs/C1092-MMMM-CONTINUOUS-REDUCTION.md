# C1092 MMMM: a continuous reduction from all original ownership alternatives

This chapter starts with the complete original C1092 entrance, including all 55,126 auxiliary alternatives, and the four closed signs

    Y8≥2, X9≥2, Y10≥2, X11≥2.                       (1)

It proves a common geometric core, all four actual wall origins, and the northeast central point without enumerating those vectors or using the 117-operator history. The companion `C1092-MMMM-CONTINUOUS-ENDING.md` starts from these proved consequences and completes the exclusion of the entire original MMMM wall class.

All squares are the original actual owners, have common side a>1, have disjoint open interiors, and have closures in [0,4]². Original marker ownership is strict. Each original corner pair supplies its strict inner corner point. Every auxiliary label is an exact subset, so an auxiliary absent from a square is excluded from that square even if no other square owns it. Every terminating decimal below is an exact rational.

## 1. Wall-sign consequences and the small covering disjunctions

Theorems `C1092-WALL-SIGN-AUXILIARIES.md` and `C1092-WALL-SIGN-CHORD.md` apply directly to (1). They give the following actual strict points and segments:

| Owner | Original marker | Compulsory auxiliary | Compulsory entire strict segment |
|---|---|---|---|
| Q8, left wall | (.914,2) | F1=(1,2.26) | {1}×[2.22,2.39] |
| Q9, bottom wall | (2,.914) | G5=(2.26,1) | [2.22,2.39]×{1} |
| Q10, right wall | (3.086,2) | F9=(3,2.26) | {3}×[2.22,2.39] |
| Q11, top wall | (2,3.086) | G7=(2.26,3) | [2.22,2.39]×{3} |

No auxiliary premise is used to obtain this table.

We use only the following simple disjunctions from the supplied original single-cover lists. Each displayed row means that every allowed subset contains at least one of the named points; it does not say the subset contains only those points.

| Actual owner and covering | At least one compulsory alternative |
|---|---|
| Northeast Q6, F | F5=(2,2.26), F7=(2.4,3), F9=(3,2.26) |
| Northeast Q6, G | G6=(2.26,2), G7=(2.26,3), G9=(3,2.4) |
| Southeast Q5, F | F4=(2,1.74), F6=(2.4,1), F8=(3,1.74) |
| Southeast Q5, G | G5=(2.26,1), G6=(2.26,2), G8=(3,1.6) |
| Northwest Q7, F | F1=(1,2.26), F3=(1.6,3), F5=(2,2.26) |
| Northwest Q7, G | G1=(1,2.4), G3=(1.74,2), G4=(1.74,3) |
| Right wall Q10, G | G6=(2.26,2), G8=(3,1.6), G9=(3,2.4) |
| Top wall Q11, F | F3=(1.6,3), F5=(2,2.26), F7=(2.4,3) |

These eight disjunctions are immediate checks of the corresponding original F and G lists. They are the only covering facts needed for the geometric deductions below.

## 2. The northeast square must own both inward points

**Theorem 1.** Every original MMMM configuration satisfies

    F5=(2,2.26)∈Q6,  G6=(2.26,2)∈Q6               (2)

strictly.

**Proof.** By Section 1, F9 and G7 already belong to different actual wall owners. The first two covering disjunctions therefore reduce to

    Q6 owns F5 or F7, and owns G6 or G9.             (3)

It cannot own both F7 and G9. Apply `OUTWARD-CORNER-TWO-GAPS.md`, translated by (2,2), with r=t=.39. Its three strict anchors would be Q6's original marker (2.35,2.35), F7 and G9. Its excluded points (2.39,3) and (3,2.39) are strictly in Q11 and Q10, respectively. The remaining excluded corner (3,3) is strictly in Q2. This is a contradiction.

Suppose Q6 did not own F5. Then (3) gives F7; the preceding paragraph rules out G9, so (3) also gives G6. Apply `MIXED-SPAN-FOUR-POINTS.md` under the rotation (x,y)↦(4−y,x). Its two strict anchors become G6,F7, and its four excluded points become

    F5=(2,2.26), G7=(2.26,3),
    F9=(3,2.26), G9=(3,2.4).

The first and last are absent from Q6 by the current supposition and preceding deduction; the other two are owned by the actual top and right walls. The mixed-span theorem is contradicted. Hence F5 is owned.

Suppose instead that Q6 did not own G6. Then (3) gives G9, and the outward-pair exclusion gives absence of F7. Apply the same mixed-span theorem under (x,y)↦(x,4−y). Its strict anchors are now F5,G9, and its excluded points are G6,F9,G7,F7. The same reasoning gives a contradiction. Thus G6 is owned as well. ∎

## 3. The adjacent central and wall pairs are compulsory

**Theorem 2.** Every original MMMM configuration satisfies the following strict ownership table:

| Owner | Compulsory pair |
|---|---|
| Q5, southeast central | F8=(3,1.74), G8=(3,1.6) |
| Q6, northeast central | F5=(2,2.26), G6=(2.26,2) |
| Q7, northwest central | F3=(1.6,3), G4=(1.74,3) |
| Q10, right wall | F9=(3,2.26), G9=(3,2.4) |
| Q11, top wall | F7=(2.4,3), G7=(2.26,3) |

**Proof.** The southeast G-disjunction in Section 1 has G5 excluded by Q9 and G6 excluded by Q6. Hence Q5 owns G8. The northwest F-disjunction has F1 excluded by Q8 and F5 excluded by Q6. Hence Q7 owns F3.

The right-wall G-disjunction now has G6 excluded by Q6 and G8 excluded by Q5. Hence Q10 owns G9. The top-wall F-disjunction has F3 excluded by Q7 and F5 excluded by Q6. Hence Q11 owns F7.

We next prove F8 belongs to Q5. Suppose it were absent. If Q5 owned F6, apply the asymmetric outward-corner theorem with r=.39,t=.26 under the map

    (x,y)↦(2+x,2−y).

Its strict anchors would be the southeast original marker (2.35,1.65), F6=(2.4,1), and the just-proved G8=(3,1.6). Its excluded points are (2.39,1), strictly in actual Q9; F8=(3,1.74), absent by supposition; and (3,1), strictly in actual corner Q1. The exact squared-gap sum is .9197<1. This is impossible. Thus F6 would be absent too.

The southeast F-disjunction then forces F4=(2,1.74). Apply the mixed-span theorem in its original orientation. Its strict anchors are F4,G8. Its excluded points are G6 in Q6, F8 absent by supposition, G5 in Q9, and F6 just shown absent. This is again impossible. Hence Q5 owns F8.

Finally transpose that complete southeast argument by (x,y)↦(y,x). This simultaneously exchanges Q5 with Q7, Q9 with Q8, F8 with G4, G8 with F3, F6 with G1, F4 with G3, and the southeast corner with the northwest corner. The two inward northeast points are exchanged within the same actual Q6. All already-proved source facts have their required transposed owners. Thus Q7 owns G4. Every row of the stated table follows. ∎

## 4. Actual right and top advances, and both wall origins

**Theorem 3.** The original actual wall squares satisfy

    {3}×[2,2.56]⊂Q10,
    [2,2.56]×{3}⊂Q11                              (4)

strictly.

**Proof.** Apply Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md` to Q10 after reflection in x=2. Its strict owned points are the original marker (3.086,2) and G9=(3,2.4). Its two excluded points are F8=(3,1.74), just proved in Q5, and the northeast original marker (2.35,2.35) in Q6. Its wall is the genuine wall x=4. The theorem gives (3,2.56) strictly in Q10, hence also (3,2.5) by convexity with G9.

Apply the same theorem to Q11 under the transport (x,y)↦(y,4−x). Its strict anchors are the original top marker and F7=(2.4,3). Its excluded points are G4=(1.74,3) in Q7 and the northeast marker in Q6. Its genuine top wall gives (2.56,3) strictly in Q11, and hence (2.5,3) as well.

Now use the actual northeast corner Q2 and Theorem 7 of `C1092-DIRECT-WALL-POINT.md`. The following table states both simultaneous transports and every nontrivial datum of that two-square theorem; its parameters are b=.914 and ell=1.6 in each row.

| Target boundary | Transport from that theorem | Corner's strict (1,b),(1,1) | Corner's excluded (1,1.5) | Boundary's strict (2,b),(ell,1) | Conclusion |
|---|---|---|---|---|---|
| Q11 | (x,y)↦(4−x,4−y) | (3,3.086),(3,3) in Q2 | (3,2.5) in Q10 | (2,3.086),(2.4,3) in Q11 | (2,3)∈Q11 |
| Q10 | (x,y)↦(4−y,4−x) | (3.086,3),(3,3) in Q2 | (2.5,3) in Q11 | (3.086,2),(3,2.4) in Q10 | (3,2)∈Q10 |

Both corner quadrant assumptions and boundary wall assumptions are genuine transported container walls. The far wall points used in the exclusions were proved before either origin transfer, so no ownership cycle is presumed. Combining each strict origin with its strict point at 2.56 gives the whole segments in (4). ∎

## 5. Four further strict points in the same northeast square

**Theorem 4.** Every original MMMM configuration has, strictly in its one actual northeast owner Q6,

    (2,2.5), (2.5,2),
    (2.54,2.01), (2.01,2.54).                       (5)

**Proof.** For (2,2.5), apply the complete retained central crosspoint proof in the appendix of `C893-CONTINUOUS-EXCLUSION.md`. Its strict anchors are exactly Q6's original marker, F5 and G6, all proved above. Its excluded southeast and northwest markers have their original different owners. Its two remaining excluded points (3,2.4),(3,2.5) lie strictly in Q10 by Theorem 3. The crosspoint is therefore strict. Diagonal transposition, using instead Q11's (2.4,3),(2.5,3), gives (2.5,2).

For (2.54,2.01), apply Corollary 3 of `C1084-DUPLICATE-POINT.md` after reflection in y=2. Its strict anchors are again the northeast marker, F5 and G6. The three required excluded points are the original northwest marker, original southeast marker, and F7=(2.4,3), which is strictly in actual Q11. The resulting reflected strict point is (2.54,2.01). Diagonal transposition, using G9=(3,2.4) in Q10 for the last exclusion, gives (2.01,2.54). All four points belong to the same actual Q6; no center point (2,2) has been inferred. ∎

## 6. Exact remaining label shape and scope

Intersecting the proved point ownerships with the original exact component lists gives the following compact shape:

| Actual owner | Remaining exact auxiliary form | Possible combined labels |
|---|---|---|
| Q5 | F8,G8, with optional F4 and/or F6 | 262400,262416,262464,262480 |
| Q6 | F5,G6, with optional F4 and/or G3 | 65568,65584,73760,73776 |
| Q7 | F3,G4, with optional G1 and/or G3 | 16392,18440,24584,26632 |
| Q10 | Exactly F9,G9 | 524800 |
| Q11 | Exactly F7,G7 | 131200 |

Optional points in distinct rows remain subject to actual disjoint ownership. No independent choice of all listed options is asserted. This table is a component description of the original entrance after the proved deductions, not a new selection of favorable complete vectors.

The southwest central, left wall, bottom wall and corner owners retain all original restrictions. The common core (2)–(5) and exact wall pairs are proved for every MMMM alternative. Sections 7–8 supply the final strict-point entrance used by the complete continuous ending in the companion chapter.

## 7. Two ordinary halfpoints give the remaining actual wall origins

Theorem 1 of `ORDINARY-RIGHT-HALFPOINT.md` applies to Q5 with its strict marker and F8,G8. Its four exclusions are G6 in Q6, the proved origin (3,2) in Q10, the corner point (3,1) in Q1, and G5=(2.26,1) in Q9. It gives (3,1.5) strictly in Q5. Diagonal transposition gives (1.5,3) strictly in Q7.

The complete actual corner-to-wall source table in that chapter then applies Theorem 7 of `C1092-DIRECT-WALL-POINT.md`. Using Q1 and the first halfpoint gives (2,1) strictly in Q9; using Q3 and the second gives (1,2) strictly in Q8. Therefore the following actual ownership is now unconditional throughout MMMM:

    (1,2)∈Q8, (2,1)∈Q9, (3,2)∈Q10, (2,3)∈Q11,
    (3,1.5)∈Q5, (1.5,3)∈Q7.                            (6)

All points are strict. In particular each central square excludes all four wall origins. Equation (6) by itself does not identify an owner of (2,2). The following separate actual three-square theorem does so.

## 8. The northeast central point has its genuine two-wall entrance

Apply the retained ordinary two-wall center theorem, Section A of `C981-RETAINED-CONTINUOUS-LEMMAS.md`, with the actual squares

    A=Q6, R=Q10, T=Q11.

The full source mapping is literal, without a coordinate transformation:

| Retained theorem premise | Actual MMMM source |
|---|---|
| A owns (2,2.26),(2.26,2),(2.35,2.35) | Q6's inward pair proved in Theorem 1 and its original marker |
| R owns (3.086,2),(3,2.4) | Q10's original marker and G9, proved in Theorem 2 |
| T owns (2,3.086),(2.4,3) | Q11's original marker and F7, proved in Theorem 2 |
| A excludes (2.35,1.65),(1.65,2.35) | The original markers in different actual owners Q5,Q7 |
| R excludes (3,1.74) | F8 strictly in actual Q5 by Theorem 2 |
| T excludes (1.74,3) | G4 strictly in actual Q7 by Theorem 2 |
| R lies in x≤4, T lies in y≤4 | The original genuine right and top container walls |
| A is disjoint from R and T, all have side a>1 | The original packing hypotheses |

The retained theorem has no center or angle premise, no side upper bound, and does not require R and T to be disjoint from one another for its local implication. Its complete continuous face, wall, half-angle and scalar proof is reproduced in the cited companion. It therefore proves the new actual strict ownership

    (2,2)∈Q6.                                           (7)

The optional F4 and G3 points in Q6's remaining exact labels neither supply nor invalidate any premise of this theorem. Equation (7) is derived after the original alternatives have been reduced geometrically; it is not an added center assumption. Together with (5), the whole strict triangle with vertices (2,2),(2.5,2),(2,2.5) belongs to this one actual Q6.

This completes the entrance of `C1092-MMMM-CONTINUOUS-ENDING.md`. Its actual two-chord and three-central-square support argument excludes the whole original MMMM class, including every optional auxiliary label retained here.
