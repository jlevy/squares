# C1089: a complete continuous ending for the reverse cyclic wall sector

All decimals are exact rationals. Retain the original C1089 squares, their common side \(1<a\le1.001\), disjoint open interiors, and real container walls. Every owned point below is strict. Exclusions and separating supports may be tangent.

**Theorem.** The complete closed C1089 sector

\[
 Y_8\le2,\qquad Y_{10}\ge2,\qquad X_{11}\le2                 \tag{1}
\]

is impossible. No orientation or propagated center-domain premise is added.

## 1. Retained entrance and compulsory inward southwest pair

The exact original owners, F/G point coordinates, and complete component families are those of C1089-CONTINUOUS-REDUCTION.md, Section 1, retained from the supplied source chapter root_next/special_cases/C1089-01-entrance-and-catalogue.txt. They are consequences of the existing finite local ownership rule (E8) and its stated consistency deletion. This proof does not replace that entrance. It replaces the ending for the whole sector (1), without selecting or enumerating individual twelve-owner vectors.

Use these actual names:

| Name | Actual C1089 owner | Original marker or corner point |
|---|---|---|
| Southwest A | Q4 | (1.65,1.65) |
| Southeast S | Q5 | (2.35,1.65) |
| Northeast E | Q6 | (2.35,2.35) |
| Northwest N | Q7 | (1.65,2.35) |
| Left, bottom, right, top walls | Q8,Q9,Q10,Q11 | (.914,2),(2,.914),(3.086,2),(2,3.086) |
| SE, NE, NW corners | Q1,Q2,Q3 | Strict inner points (3,1),(3,3),(1,3) |
| Southwest singleton | Q0 | (1,.914), with its original compulsory singleton hull |

The globally absent marker (.914,1) is not assigned an owner or used in this ending.

Propositions 1–2 of C1089-CONTINUOUS-REDUCTION.md give

\[
\begin{split}
 &F4=(2,1.74),\ G3=(1.74,2)\in A,\\
 &F0=(1,1.74)\in Q8,\quad F9=(3,2.26)\in Q10,\quad
 G4=(1.74,3)\in Q11,\\
 &[2.26,2.8]\times\{1\}\subset Q9.                         \tag{2}
\end{split}
\]

The last is one whole strict segment of the actual bottom square. Also Q0 strictly owns the whole segment \([1.12,1.74]\times\{1\}\) and the original point (1.87,.76). The top wall's closed center sign supplies the strict segment \([1.61,1.78]\times\{3\}\).

## 2. Northwest ordinary pair and lower left wall

The northwest G-covering alternative is \(\{G1,G3,G4\}\). The last two are foreign by (2), so N owns G1=(1,2.4).

Suppose N omitted F1=(1,2.26). Its F-covering alternative forces F3 or F5. If it omitted F3 too, it would own F5,G1 and exclude G3,F1,G4,F3. The half-turn \((x,y)\mapsto(4-x,4-y)\) in MIXED-SPAN-FOUR-POINTS.md maps its strict points to F5,G1 and its exclusions to exactly G3,F1,G4,F3. This is impossible. Therefore the supposed omission of F1 forces F3.

Use OUTWARD-CORNER-TWO-GAPS.md in the chart \((\xi,\eta)=(2-x,y-2)\), with \(r=.39,t=.26\). Its strict M,A,B are N's marker,F3,G1. Its excluded F is (1.61,3) in Q11's actual wall chord; its excluded G is the hypothesized absent F1; and its excluded K is (1,3) in actual paired corner Q3. The parameter condition is
\[
 (1-.39)^2+(1-.26)^2=.9197<1.
\]
This is also impossible. Hence
\[
 F1,G1\in N.                                               \tag{3}
\]

The complete NW component family now allows only 2050,2058,2082: F1,G1, optionally F3 or F5. The original Q8 family with F0 owned and F1,G1,G3 foreign has exactly label1025. Thus
\[
 Q8:\ F0,G0,\qquad G0=(1,1.6).                            \tag{4}
\]
This is a component-family implication, not an assumption that every auxiliary is covered.

Reflect Theorem 1 of C974-C976-CONTINUOUS-REDUCTIONS.md by \(y\mapsto4-y\). Its actual square is Q8, its strict marker and far point are (.914,2),G0, and its exclusions are F1 in N and the SW marker in A. The real left wall is unchanged. It gives
\[
 (1,1.44)\in Q8,\qquad
 \{1\}\times[1.44,1.74]\subset Q8                         \tag{5}
\]
strictly.

## 3. Both southwest crosspoints and an independent top origin

The retained central crosspoint theorem, reproduced in full in the appendix of C893-CONTINUOUS-EXCLUSION.md, owns (2,2.26),(2.26,2),(2.35,2.35), excludes (2.35,1.65),(1.65,2.35),(3,2.4),(3,2.5), and concludes strict ownership of (2,2.5).

After the half-turn \((x,y)\mapsto(4-x,4-y)\), its strict anchors are F4,G3 and A's marker. Its four exclusions are the NW marker in N, the SE marker in S, and (1,1.6),(1,1.5), both in the one actual Q8 by (5). Therefore
\[
 (2,1.5)\in A.                                            \tag{6}
\]
Exchange x and y in this whole application. Its strict F4,G3 interchange, its two foreign central markers interchange, and the required lower points become (1.6,1),(1.5,1), both in actual Q0's strict segment. Thus
\[
 (1.5,2)\in A.                                            \tag{7}
\]

Apply ORDINARY-MARKER-HALFPOINT.md to N under the map from its local coordinates
\[
 (\xi,\eta)\longmapsto(2-\xi,2-\eta),\qquad d=.086.
\]

| Local datum | Original point | Actual source |
|---|---|---|
| Strict M,A,B | NW marker,F1,G1 | N |
| Excluded D | G3=(1.74,2) | A |
| Excluded R | (.914,2) | Q8 marker |
| Excluded K | (1,3) | Q3 paired-corner point |
| Excluded F | G4=(1.74,3) | Q11 |
| Concluded Y | (1,2.5) | N |

Thus N strictly owns (1,2.5), and Q3 excludes it. Apply Theorem 7 of C1092-DIRECT-WALL-POINT.md to actual Q3,Q11 after reflection \(y\mapsto4-y\), with \(b=.914,\ell=1.74\). The corner's strict points are its original marker (1,3.086) and inner point (1,3); its excluded H is the new N point. The top's strict points are its own marker and G4. Their real walls supply the theorem's quadrant and bottom-wall premises. It follows that
\[
 (2,3)\in Q11\quad\hbox{strictly}.                         \tag{8}
\]
This top origin precedes every top-label reduction and uses no upper left-wall advance or surrogate owner.

## 4. The southeast and northeast alternatives match the completed local reductions

The southeast F-covering alternative forces F8, because F4 is in A and F6 is in Q9. Its G-covering alternative is G6 or G8, because G5 is in Q9.

If S omitted G8, it would own G6. ELBOW-CROSSPOINT.md Theorem 1 applies to its strict marker,G6,F8 and to its excluded G8, NE marker in E, and right marker in Q10. It would give (2,1.5) in S, contradicting (6). Hence S owns G8. Filtering its original family also excludes the actual foreign F4,G3 in A, F6,G5 in Q9, and F9 in Q10; the last exclusion in particular removes label328448. The remaining family is
\[
 S\in\{262400,\ 327936,\ 327968\}.                         \tag{9}
\]
These mean F8,G8, optionally G6 and then optionally F5.

The original Q10 family with F9 owned and F8,G8 foreign leaves 524800,590336,524928, all owning G9=(3,2.4). The uniform wall theorem, C974-C976-CONTINUOUS-REDUCTIONS.md Theorem 1, reflected through x=2, applies to the right marker,G9, with F8 in S and the NE marker in E excluded. It gives the whole strict right bar
\[
 \{3\}\times[2.26,2.56]\subset Q10.                        \tag{10}
\]

The foreign auxiliaries F4,G3,G4,F8,G8,F9,G9 now have the stated actual owners. The complete original NE component family filtered by these foreign points gives exactly
\[
\begin{array}{lll}
65568=\{F5,G6\},&131104=\{F5,G7\},&196640=\{F5,G6,G7\},\\
65664=\{F7,G6\},&131200=\{F7,G7\},&196736=\{F7,G6,G7\},\\
65696=\{F5,F7,G6\},&131232=\{F5,F7,G7\},&
196768=\{F5,F7,G6,G7\}.
\end{array}                                                   \tag{11}
\]
The top family, with G4 compulsory, consists of F3,G4 with optional F5/G7, or labels also owning F7,G7. These are exactly the small structural disjunctions needed below.

Every local transfer uses this common actual ledger:

| Required datum | Actual C1089 source |
|---|---|
| SW marker,F4,G3 and both crosspoints | A, by (2),(6),(7) |
| SE and NE markers | S and E |
| Foreign NW marker (1.65,2.35) | N, distinct from S and E |
| Whole bottom bar \([2.26,2.8]\times\{1\}\) | Q9, by (2) |
| Whole right bar \(\{3\}\times[2.26,2.56]\) | Q10, by (10) |
| Right original marker | Q10 |
| Top original marker and strict origin (2,3) | Q11, by (8) |
| SE corner points (3,1),(3.086,1) | One actual paired corner Q1 |
| NE inner point (3,3) | Actual paired corner Q2 |
| G2 and (1.87,.76), when deriving the bottom bar | Actual Q0 |

The NW marker is foreign because it belongs to N; its global absence is never assumed. None of the following proofs uses C974's upper left square or either of its missing-corner alternatives.

### 4.1. The top square has exactly F3,G4

If E owns F5,G6 and omits F7, disjointness in (9) forces S=262400. The local proof of Theorem 3 of C974-C976-CONTINUOUS-REDUCTIONS.md applies literally with the ledger: the reflected inward theorem gives (2.46,2.01) in E; the outward sign theorem with the actual Q9 bar,Q1 corner,Q10 marker makes S strictly negative; and the reflected outward point theorem gives the same strict point in S. This removes 65568 and196640 from (11).

Every original top label owning F7 also owns G7. Such a top would force E to own F5,G6 and omit F7, just excluded. Therefore Q11 omits F7 and has one of
\[
 16392,\quad147464,\quad16424,\quad147496,                 \tag{12}
\]
all owning F3,G4, with optional F5/G7.

The rotated mixed-span theorem excludes E=65664 using strict G6,F7 and excluded F5,G7,F9,G9, the last two in Q10. The two point theorems in C974-C976-DUPLICATE-POINT.md exclude E=65696: they put (2.50,2.04) strictly in E and in the forced outward S. Their bottom, corner, right-marker and foreign-central-marker inputs are precisely the common ledger.

If Q11 owned G7, (11) would leave only 65568,65664,65696 for E, all excluded. Thus Q11 omits G7. If it owned F5, it would be16424, and its own strict segment from F5 to its original marker would contain \(\{2\}\times[2.26,3.086]\). The remaining E labels avoiding F5 are131200 and196736, both owning F7,G7. Theorem 1 of C981-COMMON-CYCLE.md applies to E: its excluded (2,2.4),(2,3) belong to this one Q11 segment; (3,2.4),(3,2.56) to Q10; and (3,3) to Q2. It gives (2,2.65) strictly in E and in that top segment, a contradiction. Hence
\[
 Q11=16392=\{F3,G4\}.                                    \tag{13}
\]
This also excludes the optional NW label2058 by actual F3 ownership.

### 4.2. Only two central pairs remain

The remaining local branch exclusions occur in this dependency order. Every row uses the common ledger above; the last column records its additional branch data.

| Alternative eliminated | Complete continuous proof | Additional literal data |
|---|---|---|
| E=131104 | ELBOW-CROSSPOINT.md, Theorem 1 and its quarter-turn, then crossed-elbow Theorem 2 | E owns F5,G7 and omits F7; it obtains (2.5,2),(2.525,2.125). Outward S duplicates the second point; otherwise crossed-elbow uses S's G6,A's (2,1.5),Q9's (2.8,1). |
| E=196736 | OUTWARD-BAR-AND-UPPER-SPAN.md, Theorems 1–2 | E owns F7,G6,G7 and omits F5. Its upper span and forced outward S both own (2.525,2.125), using the actual top origin (8). |
| S=327968 | ELBOW-CROSSPOINT.md, Theorem 3; OUTWARD-BAR-AND-UPPER-SPAN.md, Theorem 3 | S owns marker,G6,F8,F5 and excludes A's (2,1.5), forcing (2.525,2.125). E must omit F5 and has only131200 left, so the upper theorem gives the same point in E. |
| S=262400, E=131200 | OUTWARD-BAR-AND-UPPER-SPAN.md, Theorems 1 and3 | The actual bottom bar gives the S point; top origin,right bar,NE corner give the same point in E. |
| S=262400, E=131232 or196768 | C974-C976-OUTWARD-PAIR.md, local coupled-support theorem | The full bottom bar gives S's angle and two face bounds; E owns marker,F5,G7 and excludes the actual N marker,top origin,NE inner corner. |

For the last row, in \((\xi,\eta)=(x-2,y-2)\), the reflected bar theorem gives the actual S the negative frame and
\[
 13/87<\frac{s}{1+c}<143/500,\quad
 U+a\le c+s,\quad V\ge-c+.8s,\quad(.525,.125)\in S.
\]
These are exactly the coupled-support theorem's premises, proved from the actual bar. Its E exclusions are the marker in N,(2,3) in Q11,(3,3) in Q2.

The table reduces (11) to131200,131232,196768 and (9) to327936. The latter owns G6 and excludes196768 by disjointness. The only necessary central pairs are therefore
\[
 (S,E)=(327936,131200)\quad\hbox{or}\quad(327936,131232).
                                                               \tag{14}
\]
S owns F8,G6,G8; E owns F7,G7 with optional F5. Q10 is exactly524800 because its G6/F7 alternatives are foreign. These are continuous branch proofs from the retained component entrance, without propagated pose boxes or angle enumeration.

## 5. Additional strict points from actual owners

Crossed-elbow Theorem 2 of ELBOW-CROSSPOINT.md with \(w=.8\) implies
\[
 (2.5,2)\in S.                                           \tag{15}
\]
Its strict anchors are S's marker,G6,F8; the two actual foreign points are A's (2,1.5),Q9's (2.8,1). Exclusion of the target would contradict that theorem.

For E=131200, OUTWARD-BAR-AND-UPPER-SPAN.md Theorem 3 gives (2.525,2.125) in E, using exactly its marker,F7,omitted F5,top origin,NE corner,right bar. For E=131232, C974-C976-CENTRAL-CROSSPOINTS.md Theorem 3 gives (2.42,2.16) in E, using marker,F5,G7 and the excluded N marker,Q11 origin,Q2 corner,Q10 F9.

Relative to (2,2), these are \(K=(\alpha,\beta)\) with
\[
 (\alpha,\beta)=(.525,.125)\quad\hbox{or}\quad(.42,.16).
\]
Each satisfies the entire domain of Theorem 4 of C974-C976-CENTRAL-CROSSPOINTS.md, including the allowed equality \(\alpha=.26+\beta\) for the second. Applied to S, its anchors are marker,G6,F8; its exclusions are A's (2,1.5) and the just established E point. It gives (3,1.5) in S.

Apply the actual SE-corner/bottom-wall Theorem 7 of C1092-DIRECT-WALL-POINT.md under \(x\mapsto4-x\), with \(b=.914,\ell=1.6\), to Q1,Q9. The corner owns (3,.914),(3,1), excludes S's (3,1.5), and has both true corner walls. Q9 owns its marker,F6 and has the true bottom wall. Consequently
\[
 (2,1)\in Q9.                                           \tag{16}
\]

Apply Theorem 1 of C974-C976-SW-SUPPORT-POINT.md to actual A. Its strict anchors are A's marker,F4,G3,(6),(7). Its excluded NW/SE markers are in N,S; its excluded bottom origin is (16); its excluded (1,1.6),(1,1.74) are in Q8. Its whole lower segment \([1.5,1.74]\times\{1\}\) belongs to Q0, and its whole southeast segment \([(2.35,1.65),(2.26,2)]\) belongs to S. No endpoints from different owners are joined. The theorem gives
\[
 (1.27,1.96)\in A.                                      \tag{17}
\]

Finally apply the uniform wall theorem to Q11 under \((x,y)\mapsto(4-y,4-x)\). Its strict inputs are top marker,F3; its exclusions are G7 in E and NW marker in N. The real top wall supplies its wall premise. It gives
\[
 (1.44,3)\in Q11,\qquad [1.44,2]\times\{3\}\subset Q11.
                                                               \tag{18}
\]

## 6. The northwest square has a narrow positive angle and two upper points

Apply Theorem 1 of ORDINARY-LEFT-TOP-OBSTRUCTION.md to actual N in the chart \((\xi,\eta)=(x-1,y-2)\).

| Local point | Original point | Actual source |
|---|---|---|
| Strict M=(.65,.35) | (1.65,2.35) | N marker |
| Strict H=(0,.26) | F1=(1,2.26) | N by (3) |
| Excluded P=(-.086,0) | (.914,2) | Q8 marker |
| Excluded D=(.5,0) | (1.5,2) | A by (7) |
| Excluded D1=(.74,0) | G3=(1.74,2) | A by (2) |
| Excluded K=(0,1) | (1,3) | Q3 paired corner |
| Excluded X=(.27,-.04) | (1.27,1.96) | A by (17) |
| Excluded T0=(.44,1) | (1.44,3) | Q11 by (18) |
| Excluded T1=(.74,1) | G4=(1.74,3) | Q11 by (2) |

It gives a strictly positive canonical frame \(u=(l,h),v=(-h,l)\) for N, with
\[
 \frac23<\frac hl<\frac8{11},\qquad
 U\ge-.086l,\quad V\ge-.27h-.04l,
\]
and the strict points
\[
 Z=(1.28,3)\in N,\qquad Z'=(1.4,3)\in N.                  \tag{19}
\]
These faces and angles follow from the displayed actual inputs; the theorem excludes all nonpositive representatives and covers axis,diagonal and tangency endpoints.

## 7. A nonnegative northeast angle duplicates a northwest point

If E=131232 has nonnegative canonical angle, the reflected cap Lemma 2 and actual top-wall Corollary 3 of C974-C976-FINAL-ANGLE-REDUCTIONS.md apply literally. The strict F5,G7 are in E; the excluded G6 is in S; Q11 has its marker,F3 and real wall. They give (1.27,3) in Q11. The actual strict segment from there to (2,3) contains Z' from (19), a contradiction.

If E=131200 has nonnegative canonical angle, Theorem 1 and Corollaries 2–3 of TOP-ONLY-LEFT-POINT.md apply to its strict marker,G7,(2.525,2.125). The exclusions are its omitted F5,actual top origin,actual NE corner,and whole right bar (10). They give (2,2.62),(2.026,3) in E. The one-wall corner-reach theorem, OTHER-GEOMETRY.md Theorem 5, then applies to Q11 with its strict origin (2,3), these two foreign E points,and real upper wall. Its chart is \((2-x,y-3)\), with \(p=.38,q=.026,r=.8\); all exact parameter checks are in TOP-ONLY-LEFT-POINT.md Corollary 4. It gives (1.2,3) in Q11. The actual strict segment to (2,3) again contains Z', contradicting (19).

Thus both nonnegative northeast alternatives, including the axial and diagonal representatives, are impossible.

## 8. A negative northeast angle contradicts the actual northwest/top support

E has a strictly negative canonical frame. Apply Theorem 1 of C976-NEGATIVE-NE-TOP-ENDING.md to the actual pair E,Q11 in \((\xi,\eta)=(x-2,y-3)\). Its common strict E anchors are M=(.35,-.65), the NE marker, and G=(.26,0), G7. Its excluded T=(1,-.44) is (3,2.56) in Q10.

For label131200, TOP-ONLY-LEFT-POINT.md Theorem 1 gives the strict X=(0,-.38), originally (2,2.62), in E for every canonical sign. Its excluded F=(0,-.74) is its omitted F5. These are precisely the outer alternative of the local negative-NE/top theorem.

For label131232, its strict F is F5. Its whole excluded segment \([.26,.5]\times\{-1\}\) is exactly the actual S segment from G6 to (2.5,2), by (15). This supplies the mixed alternative, without a fictitious segment.

The same Q11 owns the local origin by (8), has closure in \(\eta\le1\), and excludes Z=(-.72,0) because (1.28,3) is strict in N by (19). The negative-NE/top theorem forces every first-quadrant frame \((C,S),(-S,C)\) of Q11 to satisfy
\[
 S>0,\qquad C/S<2/3.                                    \tag{20}
\]
It rules out every nonnegative canonical top angle. For the remaining angle \(-\beta\), the first-quadrant normal is \((\sin\beta,\cos\beta)\), so
\[
 0<\tan\beta<2/3.                                       \tag{21}
\]

Now apply Theorem 2 of ORDINARY-LEFT-TOP-OBSTRUCTION.md to actual N,Q11 in \((x-1,y-2)\). Its N angle,lower faces,strict M,Z were proved in Section 6. Its strict top A0,O,P0 are (1.44,3),(2,3),(2,3.086), all in Q11. Its excluded T=(1.26,1) is G7, strict in E. Its real wall is \(\eta\le2\). That complete two-square support theorem excludes every nonpositive top angle with \(|\tan\beta|\le2/3\), including all actual separator tangencies. It contradicts (21).

This completes the whole closed sector (1). Every foreign segment belongs to its named actual owner, every coordinate change is simultaneous, and the southwest singleton remains the original singleton throughout. ∎

## 9. Exact scope within C1089

The four sectors excluded in C1089-CONTINUOUS-REDUCTION.md and the reverse cyclic sector proved here leave only \((++-),(+-+),(-++)\), in the order \((Y_8-2,Y_{10}-2,X_{11}-2)\). Their full MMMP endings must be supplied with literal C1089 corner sources before the entire C1089 family is declared complete. This theorem is independent of those unfinished sector endings.

