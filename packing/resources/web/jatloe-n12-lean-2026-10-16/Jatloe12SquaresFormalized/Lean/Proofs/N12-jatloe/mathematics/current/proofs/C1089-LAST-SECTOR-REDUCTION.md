# C1089: the last sector has ordinary southwest, northwest and northeast pairs

All decimals are exact rationals. Retain the original C1089 marker grouping and the complete component families in `root_next/special_cases/C1089-01-entrance-and-catalogue.txt`, as recorded in C1089-CONTINUOUS-REDUCTION.md. The component families are the output of the existing finite local ownership rule and consistency deletion; this chapter does not replace that retained entrance. Every square named below is an actual original owner, with common side \(1<a\le1.001\), disjoint open interiors, and closure in \([0,4]^2\). Exclusions and separating supports remain weak.

Write \(A=Q4,S=Q5,E=Q6,N=Q7\) for the southwest, southeast, northeast and northwest central squares. Consider the last closed wall-sign sector
\[
 Y_8\ge2,\qquad Y_{10}\le2,\qquad X_{11}\ge2.       \tag{1}
\]
The bottom sign \(X_9>2.04\) and the strict whole bottom segment \([2.26,2.8]\times\{1\}\subset Q9\) are unconditional by Proposition 1 of C1089-CONTINUOUS-REDUCTION.md.

**Theorem.** In every hypothetical configuration in (1), the following strict ownership conclusions hold:

| Actual square | Compulsory original auxiliaries | Additional strict points established here |
|---|---|---|
| A=Q4 | F0,G0 | — |
| S=Q5 | F4,G6 | (2,2),(2,1.5),(2.5,2) |
| E=Q6 | F9,G9 | (3,2.5) |
| N=Q7 | F3,G4 | — |
| Q8 | F1,G1 | (1,2.56) |
| Q9 | F6,G5 | the whole [2.26,2.8]×{1} |
| Q10 | F8,G8 | (3,2),(3,1.44) |
| Q11 | F7,G7 | (2,3),(2.56,3) |

Moreover A has exact original label1025 or9217, Q8 has label2050 or10242, Q9 has exact label32832, Q10 has exact label262400, and Q11 has label131200 or131232. The remaining N labels are16392,16424,24584,24616; the remaining E labels are524800,524832. These are component consequences, not a claim that every combination of the remaining labels is realizable.

## 1. The southeast inward pair and the two rightward pairs

Apply the strict ownership part, Sections 1–4, of C1092-MMMP-CORE-OWNERS.md after simultaneous diagonal transpose \((x,y)\mapsto(y,x)\). The four transformed wall directions are MMMP: the transformed left and bottom directions are supplied by original Q9 and Q8, the transformed right direction by original Q11, and the transformed top direction by original Q10. Their strict wall-sign chords come from C1089-CONTINUOUS-REDUCTION.md §3.

The complete covering rows used there transform to the following actual original covering rows:

| Transposed MMMP row | Actual C1089 row |
|---|---|
| Northwest F and G coverings | Q5 G-cover {G5,G6,G8} and F-cover {F4,F6,F8} |
| Northeast F and G coverings | Q6 G-cover {G6,G7,G9} and F-cover {F5,F7,F9} |
| Top F covering | Q10 G-cover {G6,G8,G9} |

Thus every required row is present in the original C1089 entrance. The two actual inner corner points used by the outward-corner obstructions become (3,1) in original Q1 and (3,3) in original Q2. The southwest corner and its missing marker do not enter these parts of the argument. The two continuously proved mixed-span obstructions and outward-corner obstructions therefore give, in original coordinates,
\[
 F4,G6\in S;\qquad F9,G9\in E;\qquad F8,G8\in Q10. \tag{2}
\]
Only these point conclusions are transferred. No C1092 exact component label is imported.

Since F2 is strict in the actual singleton Q0 and F4 is in S, A's original F-cover forces F0 into A. In the original Q8 family, exclusion of this foreign F0 leaves exactly2050,10242,2058, each containing F1,G1. Hence
\[
 F0\in A,\qquad F1,G1\in Q8.                       \tag{3}
\]

Theorem 1 of C974-C976-CONTINUOUS-REDUCTIONS.md applies directly to actual Q8. Its two exclusions are F0 in A and the northwest marker in N; its strict marker and (1,2.4)=G1 and its real left wall are present. It gives (1,2.56) strictly in Q8. Reflect that wall theorem in both midlines and apply it to actual Q10. The corresponding exclusions are F9 in E and the southeast marker in S, and its far anchor is G8. Thus
\[
 (3,1.44),(3,1.5),(3,1.6)\in Q10.                  \tag{4}
\]
The latter two points follow by convexity with G8=(3,1.6).

Reflect the retained central crosspoint theorem, proved in the appendix of C893-CONTINUOUS-EXCLUSION.md, through y=2. Its marker and two inward auxiliaries become exactly S's marker,F4,G6. Its two foreign central markers become E's and A's actual markers. Its final two exclusions become (3,1.6),(3,1.5), both supplied by Q10 in (4). Hence
\[
 (2,1.5)\in S.                                      \tag{5}
\]

If A omitted G0, its G-cover, with G2 foreign in Q0, would force G3. Reflect Theorem 1 of ELBOW-CROSSPOINT.md through x=2. Its strict anchors are then A's marker,F0,G3; its excluded opposite central marker is N's marker, its omitted outer auxiliary is G0, and its foreign wall marker is Q8's marker. The conclusion is (2,1.5) strictly in A, contradicting (5). Consequently
\[
 F0,G0\in A.                                        \tag{6}
\]

## 2. The actual southeast center and its second crosspoint

Apply the four-actual-square Theorem 3 of C1089-CONTINUOUS-REDUCTION.md in the chart
\[
 (\xi,\eta)=(x-2,2-y).
\]
Its C,W,B,K are exactly S,Q10,Q9,Q1. The complete source table is:

| Local datum | Actual original source |
|---|---|
| C marker, (0,.26),(.26,0) | S marker,F4,G6 from (2) |
| C excludes (-.35,.35) | Southwest marker strictly in A |
| W strict (1.086,0),(1,.26) | Q10 marker,F8 |
| W center ordinate nonnegative | 2−Y10≥0 from (1) |
| W real wall ξ≤2 | Original right wall x≤4 |
| B strict (0,1.086),(.4,1) | Q9 marker,F6 |
| B excludes (-.26,1) | G2=(1.74,1), strictly in Q0 |
| B real wall η≤2 | Original bottom wall y≥0 |
| K strict (1.086,1),(1,1) | (3.086,1),(3,1), strictly in paired Q1 |
| K two real corner walls | Original southeast corner of the container |

Every named owner is distinct. The theorem gives (2,2) strictly in S; its proof also gives (3,2) strictly in actual Q10 before its center argument. No sign or extra point for Q0 was used.

For the second crosspoint, apply the retained crosspoint theorem under \((x,y)\mapsto(y,4-x)\). The strict inputs become S's marker,G6,F4; the two foreign markers are A's and E's. The final excluded pair becomes (2.4,1),(2.5,1), both strict in the single actual Q9 segment. Its target becomes (2.5,2). We have established
\[
 (2,2),(2,1.5),(2.5,2)\in S,
 \qquad (3,2)\in Q10.                              \tag{7}
\]

## 3. A shared consequence of the actual singleton bar

The original compulsory Q0 hull contains
\[
 I_0=[1.12,1.74]\times\{1\},                         \tag{8}
\]
strictly. In particular it supplies [1.2,1.74]×{1}. The marker (.914,1) is globally absent; it is never assigned to Q0.

The following implication will be used in three branches. Suppose A excludes P=(1,1) and G3=(1.74,2). Reflect the outward sign theorem, Theorem 6 of C981-WALL-CYCLES.md, through x=2. Its two strict anchors become A's marker and G0 from (6). Its three excluded points become P, the actual Q8 marker, and G3. Its entire excluded segment becomes [1.2,1.74]×{1}, strictly in actual Q0. Therefore A has strictly positive canonical angle.

In this positive orientation, the outward point theorems have the following complete common source table under the half-turn (x,y)↦(4−x,4−y):

| Half-turned outward datum | Source in the original configuration |
|---|---|
| Strict southwest marker,F0 | A, by (6) |
| Excluded G3 | The present exclusion from A |
| Excluded (.914,2) | Q8's original marker |
| Excluded (1.74,1),(1.2,1) | One actual Q0 segment (8) |
| Excluded (1,1) | The present exclusion from A |
| Excluded (.914,1) | Globally absent original marker |

Consequently Theorem 2 of C1084-DUPLICATE-POINT.md gives
\[
 (1.54,2.01)\in A;                                  \tag{9}
\]
Theorem 1 of C974-C976-DUPLICATE-POINT.md gives
\[
 (1.50,2.04)\in A;                                  \tag{10}
\]
and Theorem 1 of OUTWARD-BAR-AND-UPPER-SPAN.md, using the whole same actual bar rather than just its endpoints, gives
\[
 (1.475,2.125)\in A.                                \tag{11}
\]
All three theorems require P and (.914,1) only as individual exclusions. No common corner owner is needed for those two points.

## 4. The northwest square must own F3

N excludes F1,G1, already strict in Q8. Its original covers therefore give F3 or F5, and G3 or G4. Suppose N omitted F3. Then N owns F5.

First suppose N owns G3. Theorem 1 of C1084-DUPLICATE-POINT.md under the half-turn has N's strict marker,F5,G3 as its inward anchors. Its three exclusions become E's marker, A's marker, and F3, the present absence from N. It gives
\[
 K=(1.54,2.01)\in N.                                \tag{12}
\]
Apply INNER-CORNER-INWARD-POINT.md to A after translation by (1,1), with k=.54,q=1.01. Its strict diagonal marker is A's actual marker. Its five exclusions are the globally absent (.914,1), the strict Q0 point (1.12,1), the Q8 marker (.914,2), G3 in N, and K in N. That theorem prevents A from also owning P=(1,1). Thus A excludes both P and G3, and (9) duplicates (12), a contradiction.

It remains that N omits G3 and therefore owns G4. Apply ELBOW-CROSSPOINT.md, Theorem 1 and its point corollary, under diagonal transpose. Its strict anchors become N's marker,F5,G4. Its excluded marker is E's, its omitted auxiliary is F3, and its foreign wall marker is Q11's. It gives
\[
 X=(1.5,2),\qquad Y=(1.475,2.125)\quad\hbox{strictly in }N.
                                                               \tag{13}
\]
If A owned G3, reflect the crossed-elbow Theorem 2 of ELBOW-CROSSPOINT.md through x=2, using w=.8. Its strict anchors become A's marker,F0,G3. Its three excluded points become X from (13), (2,1.5) from the actual S in (7), and (1.2,1) from the actual Q0 bar. This is impossible. Hence A excludes G3.

INNER-CORNER-FOUR-EXCLUSIONS.md now applies to A after translation by (1,1): its four exclusions are (.914,1) globally absent, (1.12,1) in Q0, (.914,2) in Q8, and X in N. It gives P excluded from A. Equation (11) therefore puts Y strictly in A, contradicting (13). Both alternatives are impossible. Thus
\[
 F3\in N.                                           \tag{14}
\]

## 5. The northwest square must own G4

Suppose N omitted G4. Its G-cover and foreign G1 force G3 into N. If it omitted F5 as well, apply MIXED-SPAN-FOUR-POINTS.md under diagonal transpose: its strict pair becomes G3,F3, and its excluded four points become F5,G4,F1,G1. The first two are the hypothetical absences, and the latter two are strict in actual Q8. This contradiction forces F5 into N too.

Reflect Theorem 2 of C974-C976-DUPLICATE-POINT.md through x=2. Its strict marker,F5,G6,F7 become N's marker,F5,G3,F3. Its excluded G7 becomes the hypothesized absent G4; its two excluded central markers belong to E and A. Thus
\[
 K=(1.50,2.04)\in N.                                \tag{15}
\]
Apply INNER-CORNER-INWARD-POINT.md to A after translation by (1,1), now with k=.50,q=1.04. Its five exclusions are supplied by the globally absent marker, Q0's (1.12,1), Q8's marker, and the genuine N points G3,K. Hence P=(1,1) is excluded from A. The common implication (10), since G3 is also foreign to A, duplicates (15). Therefore N cannot omit G4, and
\[
 F3,G4\in N.                                        \tag{16}
\]

## 6. The actual top origin and top reach

The positive top sign already supplies G7 in Q11. Filtering its original component family by the actual foreign F3,G4 in N leaves only131200 and131232, both containing F7,G7. In particular
\[
 F7,G7\in Q11.                                      \tag{17}
\]

Reflect ORDINARY-MARKER-HALFPOINT.md through y=2, using d=.086. Its strict ordinary anchors become E's marker,F9,G9. Its four exclusions become G6 in S, the actual Q10 marker, the strict northeast inner corner (3,3) in Q2, and G7 in Q11. It therefore gives
\[
 (3,2.5)\in E.                                      \tag{18}
\]

Apply Theorem 7 of C1092-DIRECT-WALL-POINT.md under the half-turn, with b=.914 and ell=1.6, to the actual pair Q2,Q11. The paired corner's required two anchors are (3,3.086),(3,3); its excluded height is (3,2.5) from E. The actual top square's two strict anchors are its original marker (2,3.086) and F7=(2.4,3), and its real top wall supplies the bottom-wall premise after half-turn. The theorem gives
\[
 (2,3)\in Q11.                                      \tag{19}
\]

Finally apply the uniform wall Theorem 1 of C974-C976-CONTINUOUS-REDUCTIONS.md under (x,y)↦(y,4−x). Its tested square is Q11; its strict inputs are the top marker,F7; its exclusions are G4 in N and the northeast marker in E. The real top wall is present. It gives
\[
 (2.56,3)\in Q11,
 \qquad [2,2.56]\times\{3\}\subset Q11              \tag{20}
\]
strictly. No top origin was assumed in the preceding step (18).

## 7. Exact component consequences and one final extra-label removal

Filter each retained original component family by the strict auxiliaries now assigned to the other actual owners. This gives

| Owner | Remaining original labels before the last removal |
|---|---|
| A | 1025,9217,9249 |
| S | 65552,73744,65584,73776 |
| E | 524800,524832 |
| N | 16392,16424,24584,24616 |
| Q8 | 2050,10242 |
| Q9 | 32832 |
| Q10 | 262400 |
| Q11 | 131200,131232 |

These are direct filters of individual original component lists; no catalogue of joint vectors is used. For Q10 the genuine foreign F9,G9 in E and G6 in S remove every other original label. For Q9 its two optional additions F4 and G8 are respectively strict in S and Q10. For Q8, F0 in A and F3 in N leave exactly the stated pair.

If A had label9249, it would own F0,G0,G3,F5. Reflect Theorem 3 of ELBOW-CROSSPOINT.md through x=2. Its strict anchors are then A's marker,F0,G3,F5, and its required excluded crosspoint (2,1.5) is strict in actual S by (7). It gives Y=(1.475,2.125) strictly in A.

By disjointness N would exclude F5. Apply Theorem 3 of OUTWARD-BAR-AND-UPPER-SPAN.md with the simultaneous coordinate map from its local chart
\[
 (\xi,\eta)\longmapsto(2-\xi,2+\eta).
\]
Its strict marker and outer top anchor become N's marker and F3. Its exclusions L,P0,P1 become respectively F5 in A, the top origin (2,3) in Q11, and the northwest inner corner (1,3) in paired Q3. Its whole excluded segment becomes {1}×[2.26,2.56], strictly in the one actual Q8 by (3) and its wall advance. The all-angle conclusion is the same strict Y in N. This duplicate point is impossible, so label9249 is removed from A.

This proves every assertion of the theorem. All conditional point exits used in the shared theorems allow tangent exclusions; strict ownership comes from their strict anchors and a>1. The corner point (1,1) was only excluded in the individual contradiction branches that explicitly establish its absence from A. It has not been assigned an owner in the surviving configuration. ∎

## 8. Exact remaining obligation

This chapter is a continuous reduction of the final sector, not its complete ending. The actual southwest singleton retains its original horizontal strict bar (8), and its absent marker remains (.914,1). The remaining ordinary central pairs and the genuine inward southeast center in (7) require one final support or strict-point contradiction before the whole C1089 family is declared simplified.
