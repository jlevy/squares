# C1089: direct wall and central reductions from the retained original entrance

All decimals in this chapter are exact rationals. The twelve actual open squares have their original common side (1<a\le1.001), pairwise disjoint interiors, and closures in ([0,4]^2). Strict ownership and weak exclusion have their original meanings. No original marker is reassigned. In particular, the missing southwest marker ((.914,1)) is globally excluded; it is not declared to belong to the singleton Q0.

## 1. Retained entrance and the points used

Retain the original-marker groups and the complete component families in `root_next/special_cases/C1089-01-entrance-and-catalogue.txt` of the supplied completed source. The families are the output of the existing finite local ownership rule and consistency deletion. An actual auxiliary vector is any pairwise disjoint choice of one of those twelve component labels. The geometric arguments below use only the stated component consequences; none selects an individual row of the 506-row catalogue or imports a propagated center domain.

The actual owners are:

| Owner | Original marker data |
|---|---|
| Q0 | Singleton ((1,.914)), excluding every other original marker |
| Q1 | Southeast pair ((3,.914),(3.086,1)), with strict inner point ((3,1)) |
| Q2 | Northeast pair ((3.086,3),(3,3.086)), with strict inner point ((3,3)) |
| Q3 | Northwest pair ((1,3.086),(.914,3)), with strict inner point ((1,3)) |
| Q4,Q5,Q6,Q7 | Respectively ((1.65,1.65),(2.35,1.65),(2.35,2.35),(1.65,2.35)) |
| Q8,Q9,Q10,Q11 | Respectively ((.914,2),(2,.914),(3.086,2),(2,3.086)) |

The original singleton lemma also gives Q0 the strict points ((1.12,1),(1.74,1),(1.87,.76)). The two Q0 auxiliary labels are4100 and5124, so Q0 owns F2=(1.6,1) and G2=(1.74,1). The three Q9 labels are32832,294976,32848, so Q9 owns F6=(2.4,1) and G5=(2.26,1).

The following are direct properties of the full original component families:

| Owner | Compulsory F member | Compulsory G member |
|---|---|---|
| Q4 | F0,F2,F4 | G0,G2,G3 |
| Q5 | F4,F6,F8 | G5,G6,G8 |
| Q6 | F5,F7,F9 | G6,G7,G9 |
| Q7 | F1,F3,F5 | G1,G3,G4 |
| Q8 | F0,F1,F3 | G0,G1,G3 |
| Q10 | F8,F9 | G6,G8,G9 |
| Q11 | F3,F5,F7 | G4,G7 |

Each entry means at least one of the listed points belongs to that actual owner. Extra points remain subject to the original complete families and actual disjointness. In particular, no assertion that every auxiliary is owned is used.

## 2. Unconditional bottom sign and advance

**Proposition 1.** Every C1089 configuration has

\[
 X_9>2.04,
 \qquad (2.8,1)\in Q9\quad\hbox{strictly}.                 \tag{1}
\]

For the first conclusion, transpose the wall-center theorem in `WALL-CENTER-AND-C974.md`. The actual Q9 owns its original marker and F6; its two required exclusions are G2 in Q0 and the southeast marker in Q5. Its real bottom wall becomes the theorem's left wall. That theorem gives the stated strict center bound.

For the second, transpose Theorem 4 of `C981-WALL-CYCLES.md`. Its strict marker and anchor are again the original Q9 marker and F6. The three foreign points are ((1.74,1),(1.87,.76)) in actual Q0 and ((2.35,1.65)) in actual Q5. The real bottom wall supplies its wall premise. The theorem gives the strict point in (1). By convexity, the whole segment ([2.26,2.8]\times\{1\}) belongs strictly to Q9. Both conclusions hold for all three original Q9 labels.

As additional reusable consequences, Theorems 1 and 2 of `OTHER-GEOMETRY.md` give strict chords longer than one in Q0 on (x=1.5), and in Q9 on (x=2.5). All their exclusions are the same actual original points just listed. These two chord conclusions alone are not a capacity contradiction.

## 3. The closed wall-direction cover and an immediate exclusion

Write (L=Y_8, R=Y_{10}, T=X_{11}). There are eight closed choices (L\ge2) or (L\le2), (R\ge2) or (R\le2), and (T\ge2) or (T\le2). Their union contains every actual configuration, including each midline equality. The bottom direction is already fixed by (1).

`C1092-WALL-SIGN-CHORD.md` applies to each actual wall marker, its foreign original adjacent central marker, and its own real wall. Thus the respective closed signs supply these strict segments:

| Actual wall | Positive center direction | Negative center direction |
|---|---|---|
| Q8 | ({1}\times[2.22,2.39]) | ({1}\times[1.61,1.78]) |
| Q10 | ({3}\times[2.22,2.39]) | ({3}\times[1.61,1.78]) |
| Q11 | ([2.22,2.39]\times\{3\}) | ([1.61,1.78]\times\{3\}) |

In particular they respectively supply F1/F0, F9/F8, and G7/G4. These are consequences of actual center signs; no center sign is inferred from a label without proof.

**Proposition 2.** If (L\le2), then Q4 strictly owns F4,G3, and necessarily (R>2).

Indeed, F0 belongs to Q8 and F2 to Q0, so Q4's F-covering alternative forces F4. If Q4 omitted G3, its G-covering alternative would give G0, because G2 belongs to Q0. Apply `MIXED-SPAN-FOUR-POINTS.md` under reflection (x\mapsto4-x). Its strict A,B become F4,G0, and its four excluded D,H,F,T become G3,F0,G2,F2. The latter three are in Q8,Q0,Q0, while G3 is the hypothesized absence. This is impossible. Hence Q4 owns G3.

If also (R\le2), then Q10 owns F8. The Q5 F-covering alternative, with F6 already in Q9, forces F4 in Q5 as well. This duplicates the strict Q4 point F4 and contradicts disjoint interiors. Therefore both closed sectors (L\le2,R\le2) are impossible, independently of (T). ∎

## 4. A reusable inward-center theorem with all actual wall and corner sources

**Theorem 3.** Let C,W,B,K be pairwise disjoint open squares of common side (a>1). Assume

\[
\begin{array}{ll}
 C:& M=(.35,.35),\ P=(0,.26),\ Q=(.26,0)\quad\hbox{strict};
       \quad N=(-.35,.35)\quad\hbox{excluded};\\
 W:& S=(1.086,0),\ T=(1,.26)\quad\hbox{strict};
       \quad W\subset\{x\le2\},\quad (\operatorname{center}W)_y\ge0;\\
 B:& B_0=(0,1.086),\ A=(.4,1)\quad\hbox{strict};
       \quad B\subset\{y\le2\},\quad F=(-.26,1)\quad\hbox{excluded};\\
 K:& (1.086,1),(1,1)\quad\hbox{strict};
       \quad K\subset\{x\le2,y\le2\}.
\end{array}                                                     \tag{2}
\]

The wall containments refer to closures. Then (O=(0,0)) belongs strictly to C. No angle or center premise is imposed on C,B,K, and N and F need not have the same foreign owner.

**Proof.** First Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md`, in the simultaneous chart taking its ((x,y)) to ((y-2,2-x)), applies to B. Its owned marker and far point become (B_0,A); its two excluded points become F and M. M is strict in the different actual square C. It therefore gives

\[
 (.56,1)\in B,\qquad (.5,1)\in B                 \tag{3}
\]

strictly, the second conclusion following by convexity with A. In particular K excludes ((.5,1)).

Apply Theorem 7 of `C1092-DIRECT-WALL-POINT.md` to the actual pair K,W, under the simultaneous map from its chart

\[
 (\xi,\eta)\longmapsto(2-\eta,2-\xi),
 \qquad b=.914,\quad\ell=1.74.
\]

Its K-points ((1,b),(1,1)) become precisely the two strict K-points in (2); its excluded upper point becomes ((.5,1)) from (3); and its B-points ((2,b),(\ell,1)) become S,T in the same actual W. The two genuine walls of K and the wall of W become the required quadrant and bottom wall. Thus

\[
 (1,0)\in W\quad\hbox{strictly}.                    \tag{4}
\]

The wall-sign chord theorem, reflected in the line (x=1/2) after its standard translation by ((-1,-2)), applies to W with its excluded point M in C. It gives ({1}\times[.22,.39]\subset W). Convexity with (4) now gives the whole strict foreign segment

\[
 I=\{1\}\times[0,.39]\subset W.                    \tag{5}
\]

Every orientation of C has a nonnegative or a nonpositive canonical representative. For a nonnegative representative, Theorem 1 of `C1092-MMMP-INWARD-CENTER.md` applies to the strict M,P,Q, to the two foreign points A and ((.56,1)) in B, and to the actual whole segment (5). It directly gives strict O, including the axial and diagonal endpoints.

If C owns ((1,.4)), Theorem 1 of `INWARD-EXTENDED-ANCHOR-CENTER.md` gives strict O for all canonical signs. Its actual wall owner is the same W of (2), and A is in B. Thus it remains only the strictly negative canonical frame

\[
 u=(c,-s),\quad v=(s,c),\quad c\ge s>0,\quad c^2+s^2=1,
\]

with C excluding both O and ((1,.4)). Let U,V be its lower face coordinates. The continuous face argument of Proposition 3 in `C1092-MMMP-INWARD-CENTER.md` uses just the strict M,P,Q, and the excluded ((1,.4),A,N), to give

\[
 U\ge-.35(c+s),\quad V\ge0,\quad
 U+a\le c-.4s,\quad V+a\le c+.4s,
 \quad0<z:=s/(1+c)<.4.                              \tag{6}
\]

For clarity, this use stops before that proposition's exact-label inspection; no label is assumed for C. The four face conclusions follow respectively by excluding N's lower-v alternative with the width bound (sqrt{.985}<1), by the two strict u-bands of O, and by the upper-u and upper-v alternatives forced at ((1,.4)) and A. All of these use only the displayed actual points.

Theorem 1 of `C1092-MMMP-FULL-INWARD-CENTER.md` applies to this same C and W and proves the strict half-angle point ((z,1)\in C). Transpose the entire local configuration. The actual C now has positive frame ((c,s),(-s,c)), lower faces (L=V,H=U), the strict points P,Q interchanged, and the strict point ((1,z)). It also contains (E=(.35,.65)) in this transposed chart: the four strict bands follow from (6) and

\[
 .35c+.65s\le\sqrt{.545}<1,
 \quad .35c-.05s<1,
 \quad v(E)+.35(c+s)=c\le1<a.
\]

(The lower u-band follows directly from the transposed strict M.) The same actual B becomes a right-wall square with strict ((1.086,0),(1,.4)), and its real wall is (x\le2). Consequently Lemma 2 of the full-center chapter applies to C and B and contradicts their disjointness. It requires no sign of B's center. The full support proof there treats both actual square-normal sources and every relative angle, so its application introduces no new orientation hypothesis.

Thus the negative alternative with missing O is impossible too. All exclusions and actual separating supports may be tangent, while strictness in the cited support contradictions comes from (a>1). This proves the theorem. ∎

## 5. The sector with two opposed inward central owners is impossible

**Theorem 4.** The whole closed C1089 sector

\[
 L\ge2,\qquad R\le2,\qquad T\le2                    \tag{7}
\]

is impossible.

**Proof of the ownership entrance.** The actual wall chords give F1 in Q8, F8 in Q10 and G4 in Q11. Q9 owns F6,G5. The southeast F-covering row therefore forces F4 in Q5. If Q5 omitted G6, its G-covering row would force G8; the untransformed mixed-span theorem then applies with strict F4,G8 and excluded G6,F8,G5,F6. Hence Q5 owns G6 as well.

For the northwest owner, the proof of Section 3 of `C1092-MMMP-CORE-OWNERS.md` applies literally. Its complete inputs are only Q7's two original covering rows, the actual left upper and top left chords in (7), and the strict corner point ((1,3)) in Q3. The outward-corner theorem with the two .39 gaps excludes simultaneous F3,G1; the two reflected mixed-span arguments then force F5,G3 in Q7. No NE ownership or unproved wall origin is part of that deduction.

The southwest F-covering row now has F2 in Q0 and F4 in Q5, so Q4 owns F0. Its G-covering row has G2 in Q0 and G3 in Q7, so Q4 owns G0. Finally the left-wall G-covering row has G0,G3 foreign to Q8, so Q8 owns G1=(1,2.4). We have proved the exact strict facts

\[
 F4,G6\in Q5;\qquad F5,G3\in Q7;\qquad
 F0,G0\in Q4;\qquad G1\in Q8.                        \tag{8}
\]

**Two applications to actual squares.** Apply Theorem 3 first in the chart ((\xi,\eta)=(x-2,2-y)), then in ((\xi,\eta)=(y-2,2-x)). The full source table is:

| Local theorem datum | Southeast application | Northwest application |
|---|---|---|
| Actual C,W,B,K | Q5,Q10,Q9,Q1 | Q7,Q11,Q8,Q3 |
| C's M,P,Q | SE marker,F4,G6 | NW marker,G3,F5 |
| C excludes N | SW marker in Q4 | SW marker in Q4 |
| W's S,T | Right marker,F8 | Top marker,G4 |
| W's center ordinate ≥0 | (2-Y_{10}\ge0) | (2-X_{11}\ge0) |
| W's wall (\xi\le2) | Original (x\le4) | Original (y\le4) |
| B's (B_0,A) | Bottom marker,F6 | Left marker,G1 |
| B excludes F | G2 strictly in Q0 | F0 strictly in Q4 |
| B's wall (\eta\le2) | Original (y\ge0) | Original (x\ge0) |
| K's ((1.086,1),(1,1)) | ((3.086,1),(3,1)) in Q1 | ((1,3.086),(1,3)) in Q3 |
| K's two corner walls | Original southeast container corner | Original northwest container corner |
| Original point corresponding to O | ((2,2)) | ((2,2)) |

Every square in either column is an actual distinct owner; each required strict point precedes the application. The theorem therefore puts ((2,2)) strictly in both Q5 and Q7. This contradicts their disjoint interiors and proves the entire sector (7), with all boundary equalities included. ∎

## 6. The all-positive sector has the complete MMMM ending

**Theorem 5.** The whole closed C1089 sector (L\ge2,R\ge2,T\ge2) is impossible.

The point-covering inclusions used in Sections 1–5 of `C1092-MMMM-CONTINUOUS-REDUCTION.md` are exactly the corresponding rows of Section 1 here. Its foreign wall chords follow from Section 3 above. Its strict corner points and all later actual corner-to-wall transfers use Q1,Q2,Q3; that reduction never uses Q0 or the absent marker ((.914,1)). Thus its continuous outward-corner and mixed-span arguments give

\[
 Q5:\ F8,G8;\quad Q6:\ F5,G6;\quad Q7:\ F3,G4;
 \quad Q10:\ F9,G9;\quad Q11:\ F7,G7.
\]

The same actual right and top wall advances give their origins; the same inward crosspoint lemmas give Q6 the strict points ((2.5,2),(2,2.5)); and the same ordinary SE/NW halfpoint arguments, through Q1/Q3, give the bottom and left origins. Finally its Section 8 applies the retained ordinary two-wall center theorem to the actual triple Q6,Q10,Q11 and gives strict ((2,2)\in Q6).

These are precisely the full actual inputs of `C1092-MMMM-CONTINUOUS-ENDING.md`: its inward square N is Q6, its two neighboring ordinary squares are Q5,Q7, its bottom and left strict bars are in Q9,Q8, and its SE/NW corner points are in Q1,Q3. That complete support theorem excludes the configuration for all canonical signs and actual separator directions. Its proof contains no Q0 datum. Thus the missing outer SW marker causes no change in any premise, and the entire sector is excluded. ∎

## 7. Exact current scope

Sections 3,5,6 exclude four of the eight closed wall-direction sectors: both with (L\le2,R\le2), the sector (L\ge2,R\le2,T\le2), and the all-positive sector. The remaining four sectors are ( (++-),(+-+),(-++),(-+-)) in the order ((L,R,T)). The first three have the MMMP continuous ownership geometry under simultaneous symmetries; the last is the reverse cyclic arrangement with Q4's inward F4,G3 from Proposition 2. No conclusion that these remaining sectors are already impossible is made here. They require their complete actual-owner endings before C1089 as a whole is closed.
