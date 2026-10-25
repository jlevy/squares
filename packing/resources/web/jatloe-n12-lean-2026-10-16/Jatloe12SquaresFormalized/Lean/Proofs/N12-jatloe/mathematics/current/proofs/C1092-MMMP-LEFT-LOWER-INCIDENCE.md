# C1092 MMMP: a lower incidence in the left wall forces the southwest bottom anchor

All terminating decimals are exact rationals. The squares are the actual original open squares, their common side satisfies 1<a<=1.001, and their interiors are disjoint. Ownership is strict; exclusion allows boundary contact.

**Theorem.** In the whole original MMMP family, if the actual left wall Q8 strictly owns F0=(1,1.74), then the actual southwest square Q4 strictly owns F2=(1.6,1).

This is an implication between actual owners. It neither presumes that every auxiliary has an owner nor assigns the top-wall origin.

## 1. The original covering alternatives

The original F-covering row for Q4 requires at least one of F0,F2,F4. Under the theorem's hypothesis F0 belongs to the different actual Q8. Suppose, for a contradiction, that F2 is absent from Q4. Then

    F4=(2,1.74) is strict in Q4.                         (1)

The original G-covering row for Q4 requires at least one of G0,G2,G3. The MMMP core-owner theorem places G3=(1.74,2) strictly in the actual northwest Q7. We distinguish only whether G2 is inside Q4.

## 2. If G2 is owned, the elbow theorem gives a duplicate strict point

Suppose G2=(1.74,1) is strict in Q4. Apply the theorem in `ELBOW-CROSSPOINT.md` under the simultaneous quarter-turn

    T(x,y)=(y,4-x).

Its complete source ledger is as follows.

| Standard datum | Image under T | Actual source |
|---|---|---|
| Strict M=(2.35,1.65) | (1.65,1.65) | Original Q4 marker |
| Strict D=(2.26,2) | F4=(2,1.74) | Q4 by (1) |
| Strict A=(3,1.74) | G2=(1.74,1) | Present case |
| Excluded N=(2.35,2.35) | (2.35,1.65) | Original Q5 marker |
| Excluded G=(3,1.6) | F2=(1.6,1) | Contrary absence from Q4 |
| Excluded R=(3.086,2) | (2,.914) | Original Q9 marker |

The theorem therefore puts the image of X=(2,1.5), namely

    T(X)=(1.5,2),

strictly in Q4. The complete MMMP center-crosspoint theorem already puts this same point strictly in the different actual Q7. This contradicts disjoint interiors. Hence G2 is absent from Q4 under the contrary hypothesis.

## 3. If G2 is absent, the mixed span is impossible

The G-covering row now forces G0=(1,1.6) strictly into Q4. Apply `MIXED-SPAN-FOUR-POINTS.md` under reflection S(x,y)=(4-x,y). Its complete strict/excluded data become

| Standard datum | Image under S | Actual source |
|---|---|---|
| Strict A=F4=(2,1.74) | F4=(2,1.74) | Q4 by (1) |
| Strict B=G8=(3,1.6) | G0=(1,1.6) | Q4 by its covering row |
| Excluded D=G6=(2.26,2) | G3=(1.74,2) | Actual Q7 |
| Excluded H=F8=(3,1.74) | F0=(1,1.74) | Actual Q8, by hypothesis |
| Excluded F=G5=(2.26,1) | G2=(1.74,1) | Absent by Section 2 |
| Excluded T=F6=(2.4,1) | F2=(1.6,1) | Contrary absence from Q4 |

The cited all-angle theorem excludes precisely this actual square. Both alternatives for G2 have therefore contradicted the supposition that F2 is absent. This proves the theorem.

## 4. The exact remaining left-wall components

The separate theorem `C1092-MMMP-LEFT-FAR-AUXILIARY.md` proves that Q8 strictly owns G1=(1,2.4). It already owns F1=(1,2.26) by the wall-sign chord. The actual Q7 owns G3; the actual Q11 owns F3 and G4. Filtering the original combined list M8 by these literal incidences leaves

    2050, 2051, 3075, 3079.

They have the following meanings:

| Label | Exact F subset | Exact G subset |
|---|---|---|
| 2050 | {F1} | {G1} |
| 2051 | {F0,F1} | {G1} |
| 3075 | {F0,F1} | {G0,G1} |
| 3079 | {F0,F1,F2} | {G0,G1} |

The last possibility is impossible even without the theorem: the squared distance between its two strict points F2 and G1 is

    |F2-G1|^2=.6^2+1.4^2=58/25=2.32,

whereas any two points of a square of side a<=1.001 have squared distance at most

    2a^2<=2(1001/1000)^2=1002001/500000<58/25.

Thus the exact original left-wall component is one of 2050,2051,3075. In the latter two cases the theorem proved above forces F2 into the actual Q4. The first component excludes F0 and hence permits the ordinary left-wall advance; the other two cases still require a geometric ending. No such ending is claimed here.
