# C888 and C889: one continuous right-side exclusion

All terminating decimals are exact. Owned points and the complete segments joining owned endpoints lie strictly in their one actual open square. Distinct actual squares have disjoint interiors, and their common side satisfies a>1. The geometric ending below does not use a side upper bound.

## 1. Retained entrance and actual owners

The auxiliary families and compulsory hulls are retained from Sections 2–3 of the original `C888-complete-exclusion.txt` and `C889-complete-exclusion.txt` in `root_next/twenty_one_cases/`. They follow from the existing finite local ownership rule. This chapter replaces the later propagated-domain and capacity ending; it does not replace that retained entrance rule.

The original owner orders are

\[
\begin{array}{c|l}
C888&(1,2,12,16,192,512,1024,2304,4096,8192,16384,32768),\\
C889&(1,2,12,16,192,512,1024,2304,4096,8192,16416,32768).
\end{array}
\]

In both cases write A=Q₅ for the southeast central square, N=Q₆ for the northeast central square, W=Q₇ for the merged southwest/northwest square, B=Q₉ for the bottom-wall square, and R=Q₁₀ for the right-wall square. The actual southeast corner Q₂ is paired in both cases. The actual top-right singleton is Q₃.

The marker distinction is retained exactly: in C888 the original marker (3.086,3) is absent from all squares; in C889 it belongs to R. It never belongs to N in either of these two cases. The argument below uses its absence only in the lower-wall branch, which occurs only in C888.

## 2. The two actual wall segments

The compulsory singleton hull of Q₃ supplies the complete strict segment

\[
\mathcal T=[2.26,2.88]\times\{3\}\subset Q_3. \tag{1}
\]

The bottom square B owns (2,.914),(2.4,1),(2.26,1). Apply Theorem 4 of `C981-WALL-CYCLES.md` after transposing x and y. The required three foreign points are

\[
(1.74,1),\quad(1.87,.76),\quad(2.35,1.65).
\]

The first two are strict in the actual bottom-left singleton Q₀, and the third is A's original marker. The actual bottom wall y≥0 supplies the wall hypothesis. Therefore B strictly owns (2.8,1), and hence

\[
\mathcal B=[2.26,2.8]\times\{1\}\subset B. \tag{2}
\]

These segments have one actual owner each. No segment between unrelated excluded points is used.

## 3. A two-way ownership split

For clarity, auxiliary indices 4,5,8,9,16,18,19 denote, respectively,

\[
(2,1.74),\ (2,2.26),\ (3,1.74),\ (3,2.26),\
(2.26,2),\ (3,1.6),\ (3,2.4).
\]

The exact right-wall families are

\[
C888:\quad 262400,524800,262912,525056,
\]

\[
C889:\quad 524800,525056.
\]

Their auxiliary sets are {8,18}, {9,19}, {8,9,18}, {8,9,19}, respectively. Thus R owns either the lower pair {8,18} or the upper pair {9,19}. C889 permits only the upper pair. Because strict auxiliary ownership is disjoint, the original central families yield the following necessary alternatives:

| Right-wall pair | Forced inward central pair | Only possible auxiliary sets in the other central square |
|---|---|---|
| R owns {8,18} | A owns {4,16} | N: {5,19}, {9,19}, or {5,9,19} |
| R owns {9,19} | N owns {5,16} | A: {4,18}, {8,18}, or {4,8,18} |

Here “owns” allows the additional auxiliaries in the original label. The exact verification is short: in the lower-wall branch the only A labels avoiding 8 and 18 are 65552,65584,66064; all contain 4 and 16. The only N labels then avoiding 16 and the wall pair are 524320,524800,524832, the three displayed sets. In the upper-wall branch the only N labels avoiding 9 and 19 are 65568,65584,65824; all contain 5 and 16. The remaining A labels are 262160,262400,262416. These checks also apply to the smaller C889 families. Any additional shared auxiliary merely removes one of the displayed alternatives.

This is an exhaustive structural split from the retained labels, not a subdivision of orientations or square poses.

## 4. Lower right-wall pair: complete C888 exclusion of this branch

Suppose R owns {8,18}. The square A has its inward marker and pair

\[
(2.35,1.65),\quad(2,1.74),\quad(2.26,2).
\]

Theorem 1 of `C1084-DUPLICATE-POINT.md` applies. Its foreign southwest marker lies in W, its foreign northeast marker lies in N, and its required bottom point (2.4,1) lies in B. Therefore

\[
(2.46,1.99)\in A\quad\text{strictly}. \tag{3}
\]

If N's set is {5,19}, it owns (2,2.26),(3,2.4) and excludes (3,2.26). It also excludes (2.26,2), which is strict in A. Reflect in y=2 and apply Theorem 5 of `C981-WALL-CYCLES.md`, the all-angle mixed-span obstruction. The required whole foreign segment comes from the reflected subsegment [2.26,2.8]×{3} of (1). Thus this alternative is impossible.

In either of the other two N alternatives, N owns the outward pair {9,19}. Apply the theorem of `OUTWARD-STRONG-BAR.md` with the following exact data:

| Theorem datum | Actual C888 source |
|---|---|
| Strict (2.35,2.35) | N's original marker |
| Strict (3,2.26),(3,2.4) | N's pair {9,19} |
| Excluded (2.26,2) | A |
| Excluded (3.086,2) | R's original wall marker |
| Excluded (3.086,3) | The genuinely absent original marker 5 |
| Whole [2.26,2.86]×{3} | Strictly contained in (1), in Q₃ |

No actual owner is assigned to the absent marker. It is used only as its genuine original exclusion. The theorem permits N's additional ownership of auxiliary 5 in the set {5,9,19}; it does not require that point to be excluded. It gives

\[
(2.46,1.99)\in N\quad\text{strictly}. \tag{4}
\]

The duplicate point (3)–(4) contradicts the disjointness of A and N. This excludes every lower-wall alternative.

## 5. Upper right-wall pair: complete exclusion in both C888 and C889

Suppose R owns {9,19}. The square N has its inward marker and pair

\[
(2.35,2.35),\quad(2,2.26),\quad(2.26,2).
\]

Reflect in y=2 and apply the inward theorem. Its required foreign central markers are (1.65,2.35) in W and (2.35,1.65) in A. Its required upper point (2.4,3) lies in the actual Q₃ segment (1). Therefore

\[
(2.46,2.01)\in N\quad\text{strictly}. \tag{5}
\]

If A's set is {4,18}, it owns (2,1.74),(3,1.6) and excludes (3,1.74). It excludes (2.26,2), which belongs to N, and it excludes the full actual bottom segment (2). These are exactly the hypotheses of the all-angle mixed-span obstruction, Theorem 5 of `C981-WALL-CYCLES.md`. This alternative is impossible.

In either remaining A alternative, it owns the outward pair {8,18}. The sign lock, Theorem 6 of `C981-WALL-CYCLES.md`, applies with A's marker and auxiliary (3,1.6), the isolated exclusions (3,1),(3.086,2),(2.26,2), and the whole bottom segment (2). It fixes A's canonical angle as strictly negative. Reflect in y=2 and apply the outward Theorem 2 of `C1084-DUPLICATE-POINT.md`. Its six excluded points before reflection have the following sources:

| Original excluded point | Actual owner |
|---|---|
| (2.26,2) | N |
| (3.086,2) | R |
| (2.26,1),(2.8,1) | B, by (2) |
| (3,1),(3.086,1) | The actual paired southeast corner Q₂ |

The strict reflected anchors come from A's original marker and (3,1.74). The theorem and sign lock do not require exclusion of auxiliary 4, so the extra ownership in {4,8,18} is allowed. The conclusion is

\[
(2.46,2.01)\in A\quad\text{strictly}. \tag{6}
\]

Equations (5)–(6) contradict the disjointness of A and N. This excludes every upper-wall alternative.

The changed C889 corner marker causes no loss of a needed premise here: this branch uses the paired southeast corner's two points at y=1. It does not require exclusion of (3.086,3) from R or assign that point to a nonexistent paired northeast corner.

## 6. Completed families and the precise non-transfer to C893

The lower and upper right-wall pairs exhaust the C888 entrance. The upper pair exhausts the C889 entrance. **Both original families C888 and C889 are therefore completely excluded** by the two wall segments, the all-angle mixed-span theorem, the inward strict-point theorem, and the appropriate outward strict-point theorem.

Every continuous theorem used includes zero and diagonal canonical angles and permits tangency at excluded points. Every whole segment comes from its one actual square. The resulting contradiction is a strict point in two distinct actual squares; it needs no capacity update or orientation mesh.

This chapter does not apply the lower-wall argument to C893. There the outward northeast square itself owns (3.086,3), violating an explicit hypothesis of the stronger outward theorem. That ownership distinction must be handled separately. It is not removed by the fact that the three families have the same central target indices.

The separate chapter `C893-CONTINUOUS-EXCLUSION.md` supplies that different argument: its new theorem retains the corner marker as strictly owned and forces one of two points which are both strict in the southeast square. Thus its complete C893 ending does not reuse the invalid exclusion.
