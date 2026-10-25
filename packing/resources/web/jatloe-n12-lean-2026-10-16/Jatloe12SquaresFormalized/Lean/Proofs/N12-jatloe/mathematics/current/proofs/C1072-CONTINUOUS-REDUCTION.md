# C1072: a complete continuous exclusion from four left-side alternatives

All points called owned below are strict points of their one actual square. All decimals are exact. We use the original C1072 owner order

\[
(1,12,16,192,256,512,1024,2048,4096,8192,16384,32768).
\]

Write O=Q₀, C=Q₃, A=Q₄, N=Q₇, L=Q₈, and T=Q₁₁. Thus A,N are the southwest and northwest central squares, L is the actual left-wall square, C is the paired northwest corner, O is the bottom-left singleton, and T is the actual top-wall square.

The entrance is retained from `root_next/twenty_one_cases/C1072-complete-exclusion.txt`, Sections 2–3, in the original completed package: its exact auxiliary label families follow from the existing finite local ownership rule, and its compulsory strict hulls supply the singleton and wall points used here. The present chapter replaces the subsequent propagated-domain and capacity ending. It does not claim to replace or rederive that retained local ownership rule.

## 1. The actual top segment

The strong wall theorem, Theorem 4 of `C981-WALL-CYCLES.md`, applies to T under (X,Y)=(4−y,4−x). Its strict anchors are the original marker (2,3.086) and auxiliary (1.6,3). Its three foreign points are (2.26,3) and (2.13,3.24), both in the actual top-right singleton Q₂, and the northwest marker (1.65,2.35) in N. The actual top wall supplies X≥0.

Consequently T strictly owns (1.2,3). Together with its owned (1.74,3), this gives the full strict segment

\[
[1.2,1.74]\times\{3\}\subset T. \tag{1}
\]

The bottom singleton already supplies

\[
[1.12,1.74]\times\{1\}\subset O. \tag{2}
\]

## 2. Four exhaustive left-side alternatives

The retained original label families are

\[
A:\{1025,8193,1040,8208\},\quad
N:\{2050,8194,2080,8224\},\quad
L:\{1025,2050\}.
\]

Two different actual squares cannot share an auxiliary point. If L has label 1025, it owns (1,1.74),(1,1.6); this forces A to have label 8208. The point (1.74,2) then belongs to A, leaving only N labels 2050 or 2080. If L has label 2050, the reflected argument forces N label 8224, leaving A labels 1025 or 1040. Thus exactly these four necessary alternatives remain:

| Alternative | A label and auxiliary pair | N label and auxiliary pair | L label |
|---|---|---|---|
| I | 8208: (2,1.74),(1.74,2) | 2050: (1,2.26),(1,2.4) | 1025 |
| II | 8208: (2,1.74),(1.74,2) | 2080: (2,2.26),(1,2.4) | 1025 |
| III | 1025: (1,1.74),(1,1.6) | 8224: (2,2.26),(1.74,2) | 2050 |
| IV | 1040: (2,1.74),(1,1.6) | 8224: (2,2.26),(1.74,2) | 2050 |

This four-way deduction uses only the given label families and strict disjointness. Auxiliary assignments elsewhere can only remove rows from this list.

## 3. Both mixed-span alternatives are impossible

The all-angle mixed-span obstruction, Theorem 5 of `C981-WALL-CYCLES.md`, excludes a side-a>1 square owning (2,1.74),(3,1.6), excluding (2.26,2),(3,1.74), and excluding the whole segment [2.26,2.8]×{1}.

For alternative II, apply it to N under the half-turn (x,y)↦(4−x,4−y). The two owned points come from N's pair (2,2.26),(1,2.4). The exclusion (2.26,2) comes from A's strict (1.74,2); the exclusion (3,1.74) comes from the absent auxiliary (1,2.26) in N's exact label. The whole foreign segment is exactly the image of (1), in the actual T. Hence alternative II is impossible.

For alternative IV, apply the same theorem to A under (x,y)↦(4−x,y). The two owned points are its pair (2,1.74),(1,1.6). The point (2.26,2) comes from N's strict (1.74,2), and (3,1.74) comes from the absent auxiliary (1,1.74) in A's exact label. The required whole segment is contained in the image of (2), in the actual O. Hence alternative IV is impossible.

The mixed-span theorem permits every tangency and uses no side upper bound. Both applications retain their exact original-marker exclusions.

## 4. The inward southwest and outward northwest alternative is impossible

Alternative I is the exact x↦4−x reflection of the completed local inward–outward argument in `C1084-DUPLICATE-POINT.md`.

For the inward square A, Theorem 1 of that file applies after reflection. Its strict anchors are A's marker (1.65,1.65), and its owned pair (2,1.74),(1.74,2). Its three foreign points before reflection are

\[
(2.35,1.65)\in Q_5,\qquad
(1.65,2.35)\in N,\qquad
(1.6,1)\in O.
\]

Thus

\[
(1.54,1.99)\in A\quad\text{strictly}. \tag{3}
\]

For the outward square N, the reflection gives all of the outward theorem's point premises exactly:

| Standard reflected datum | Original C1072 point | Actual source |
|---|---|---|
| Strict (2.35,2.35) | (1.65,2.35) | N's original marker |
| Strict (3,2.26) | (1,2.26) | N's auxiliary pair |
| Additional sign-lock anchor (3,2.4) | (1,2.4) | N's auxiliary pair |
| Excluded (2.26,2) | (1.74,2) | A |
| Excluded (3.086,2) | (.914,2) | L's original marker |
| Excluded (2.26,3) | (1.74,3) | T |
| Excluded (2.8,3) | (1.2,3) | T, by (1) |
| Excluded (3,3) | (1,3) | C, the paired northwest corner |
| Excluded (3.086,3) | (.914,3) | C's original marker |

The full reflected segment [2.26,2.8]×{3} also belongs to that same T. Reflecting this local configuration in y=2 supplies exactly Theorem 6 of `C981-WALL-CYCLES.md`; it fixes the angle to the positive sign required by the outward theorem. Theorem 2 of `C1084-DUPLICATE-POINT.md` therefore gives

\[
(1.54,1.99)\in N\quad\text{strictly}. \tag{4}
\]

The two actual squares A,N are distinct, so (3)–(4) contradict strict disjointness. Alternative I is impossible.

## 5. The remaining alternative is excluded without a paired southwest corner

Only alternative III remains after the preceding transfers:

\[
A:\ (1.65,1.65),(1,1.74),(1,1.6),
\]

\[
N:\ (1.65,2.35),(2,2.26),(1.74,2),
\]

\[
L:\ (.914,2),(1,2.26),(1,2.4).
\]

The inward theorem applies to N after the half-turn (x,y)↦(4−x,4−y). Its three strict anchors become the standard southeast inward anchors. Its foreign southwest and northeast markers come from the actual Q₆ marker (2.35,2.35) and the actual A marker (1.65,1.65), respectively. Its required bottom point (2.4,1) comes from T's strict (1.6,3). Thus

\[
(1.54,2.01)\in N\quad\text{strictly}. \tag{5}
\]

The outward square A meets the theorem in `OUTWARD-STRONG-BAR.md` after the same half-turn. Unlike the earlier paired-corner application, that theorem requires no exclusion or actual owner for (1,1). The exact data are:

| Standard reflected datum | Original C1072 point or segment | Genuine source |
|---|---|---|
| Strict (2.35,2.35) | (1.65,1.65) | A's original marker |
| Strict (3,2.26) | (1,1.74) | A's auxiliary pair |
| Strict (3,2.4) | (1,1.6) | A's auxiliary pair |
| Excluded (2.26,2) | (1.74,2) | N |
| Excluded (3.086,2) | (.914,2) | L's original marker |
| Excluded (3.086,3) | (.914,1) | The genuinely absent original marker 1 |
| Whole segment [2.26,2.86]×{3} | [1.14,1.74]×{1} | Contained strictly in the actual O segment (2) |

The exact original marker family excludes marker 1 from every square. Its use in this one-square theorem is an exclusion only; no owner is assigned to it. The longer actual O segment is what removes the former need for the corner-point exclusion (1,1).

The outward theorem therefore gives

\[
(1.54,2.01)\in A\quad\text{strictly}. \tag{6}
\]

Equations (5)–(6) contradict the strict disjointness of the two distinct actual squares. Alternative III is impossible.

## 6. Conclusion and scope

The original left-wall and central label families give exactly the four necessary alternatives in Section 2. Sections 3–5 exclude all four by continuous, all-orientation theorems with explicit original-owner mappings. **The entire original C1072 family is therefore excluded.**

The proof uses its actual bottom singleton, actual top-wall advance, actual paired northwest corner, all stated original-marker exclusions, and the indicated strict central and wall auxiliaries. It never replaces the missing southwest marker by a paired corner. No orientation mesh, propagated polygon domain, finite capacity table, or upper bound on the side is used in the geometric ending.
