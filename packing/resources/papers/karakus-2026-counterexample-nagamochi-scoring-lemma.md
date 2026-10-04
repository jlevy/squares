# A counterexample to Nagamochi's scoring lemma and a new rectangle packing bound

**Authors:** Hakan Karakuş (Boğaziçi University, Istanbul, Türkiye)
**Venue:** arXiv preprint, arXiv:2609.37410v1 [math.CO], 15 pages, 4 figures
**Year:** 2026 (v1 submitted 29 Sep 2026 12:44:05 UTC; the paper is dated September 29, 2026)
**Source:** https://arxiv.org/abs/2609.37410 (PDF: https://arxiv.org/pdf/2609.37410v1)
**Licence:** CC BY 4.0, as stated on the arXiv abstract page
**Archived:** 2026-10-02 (accessed 2026-10-02, 06:39 UTC); PDF SHA-256 `39ae2ae44f063e6555240c4a246b47f687578c57196b70a9f5d66953d5cf6513`
**Extraction:** `pdftotext -layout` (Poppler 24.02.0) from the original PDF, preserved alongside as `karakus-2026-counterexample-nagamochi-scoring-lemma.raw.md`. This cleaned copy was written from the author's LaTeX source in the arXiv e-print of v1 (`main.tex`, SHA-256 `c2244b032d6847ed27647a69383096cd5a8ce644d0c8b6bad473f6aca741c70a`; not retained), with every equation, theorem and reference number read off the PDF. Cross-references are written as the PDF prints them. The four TikZ drawings are described rather than reproduced; the PDF is the authority for them. Nothing was reconstructed, so this file carries no `GARBLED` or `NOTE` annotation.

---

**Abstract.** Let $s(N)$ denote the smallest side length of a square containing $N$ unit squares with arbitrary orientations and pairwise disjoint interiors. Nagamochi's *Packing Unit Squares in a Rectangle* (2005) states a rectangle packing bound from which he deduces two infinite families of exact values: $s(k^2-1) = k$ and $s(k^2-2) = k$ for every integer $k \geq 2$. We construct a family of counterexamples, local to a corner of the container, to the scoring assertion in Nagamochi's Lemma 1. These counterexamples show that the published proof of the rectangle bound is incomplete, but do not disprove the bound itself. We then give an independent proof of a weaker rectangle bound using a strip measure. This recovers $s(k^2-1) = k$ for every integer $k \geq 2$ and yields an explicit lower bound for $s(N)$ that improves strictly on the area bound for every nonsquare integer $N \geq 8$. Our argument does not establish Nagamochi's full rectangle bound or the identity $s(k^2-2) = k$.

**Keywords.** Unit square packing; rectangle packing; unavoidable sets; weighted measures; packing bounds.

## 1 Introduction

Finite packing problems ask how small a container of a prescribed shape can be while accommodating a given number of congruent objects with disjoint interiors. Finding a dense arrangement provides an upper bound, but proving its optimality requires ruling out every better arrangement. For equal circles, non-overlap can be expressed through distances between centers; for squares, orientations introduce additional geometric constraints.

For a positive integer $N$, let $s(N)$ denote the smallest side length of a square containing $N$ unit squares with pairwise disjoint interiors, where the squares may be translated and rotated independently. Area and the usual grid packing give

$$\sqrt{N} \leq s(N) \leq \left\lceil\sqrt{N}\right\rceil.$$

For $N = k^2$, the two bounds coincide, giving $s(k^2) = k$.

This paper revisits a rectangle-packing bound stated by Nagamochi [1], from which the identities

$$s(k^2-2) = s(k^2-1) = k$$

were deduced for every integer $k \geq 2$. We give a family of counterexamples to a scoring assertion used in the published proof. We then prove a weaker rectangle bound independently; it recovers $s(k^2-1)=k$ and yields an explicit lower bound for $s(N)$ that improves strictly on the area bound for every nonsquare integer $N \geq 8$.

The square-packing problem considered here goes back at least to Erdős and Graham [2], who showed that rotated squares can substantially reduce the unused area in large containers compared with the usual grid construction. Göbel [3] subsequently studied the problem systematically, and Friedman [4] surveys its history and known results. Friedman [4, Section 1] also notes that computational methods developed for circle packing did not readily generalize to squares.

Among the classical exact results, Göbel [3] obtained $s(5) = 2+\frac{1}{\sqrt{2}}$, Kearney and Shiu [5] proved $s(6) = s(7) = 3$, and Stromquist [6] proved $s(10) = 3+\frac{1}{\sqrt{2}}$. Friedman [4] proved or reproved several further individual cases, including $N = 8,14,15,24,$ and $35$. Computational methods have also improved constructions without establishing optimality; for example, Gensane and Ryckelynck [7] developed an inflation-based method that improved the best known packings for several values of $N$.

One particularly suggestive sequence occurs immediately below perfect squares. Bentz [8] proved $s(13) = 4$ and $s(46) = 7$, and later proved $s(22) = 5$ and $s(33) = 6$ [9]. Together with $s(6) = 3$, these results establish

$$s(k^2-3) = k,\qquad k = 3,4,5,6,7.$$

These individual proofs do not establish the identity for all $k$. Results in the opposite direction show that the grid construction need not remain optimal further below a perfect square: Arslanov, Mustafin, and Shangitbayev [10] proved

$$s(k^2-k) < k,\qquad k \geq 12.$$

Thus even near perfect squares, determining when rotations permit a smaller container remains difficult.

A rectangle bound stated by Nagamochi [1] would provide two infinite families of exact values in this near-square regime. For $t \geq 2$, write

$$\Delta(t) = t+1-\lceil t\rceil.$$

For positive real numbers $a$ and $b$, let $\nu(a,b)$ denote the maximum number of unit squares with pairwise disjoint interiors that can be packed in some $a'\times b'$ rectangle with $a' < a$ and $b' < b$. Nagamochi [1, Theorem 1] states that, for real numbers $a,b \geq 2$,

$$\nu(a,b) < ab-\Delta(a)-\Delta(b). \tag{1.1}$$

From this bound, Nagamochi [1, Theorem 2] derives a general lower bound for $s(N)$ and, in particular,

$$s(k^2-1) = s(k^2-2) = k,\qquad k \geq 2. \tag{1.2}$$

These identities have subsequently been cited in the square-packing literature as established results; see, for example, [4, 8, 9, 10]. The validity of Nagamochi's proof therefore matters beyond the individual cases.

Nagamochi's proof assigns scores to squares by means of a central area, four weighted line segments, and weighted points. Lemma 1 of [1] asserts a lower bound on the score of each square; summing these scores yields the rectangle bound (1.1). These arguments belong to the method of unavoidable sets: one assigns resources to subsets of the container and shows that every packed square must consume a prescribed amount. Friedman [4, Sections 4 and 5] surveys constructions using unavoidable points, while Bentz [9, Section 2] develops continuously varying families of unavoidable point configurations.

We show that Nagamochi's scoring assertion is false under the definitions in [1, Section 3]. More precisely, we identify an edge-incidence condition missing from the application of [1, Lemma 6] in [1, Section 5.5, Case 6], and use it to construct a family of squares whose scores are less than $1$. The construction applies near a corner of every rectangle with side lengths $a > 3$ and $b > 2$ once its parameter is sufficiently small. A further shrink about a vertex produces a strict configuration in which the contact point lies on an edge different from the two edges cut by $y = 1$.

This counterexample shows that the published proof of (1.1) requires an additional argument, but it does not disprove the rectangle bound itself. We instead prove the following weaker bound by a separate method.

**Theorem 1.1 (Rectangle bound).** *For real numbers $a \geq 2$ and $b \geq 3$,*

$$\nu(a,b) < ab-\Delta(a). \tag{1.3}$$

*If $a,b \geq 3$, applying the same construction in both directions gives*

$$\nu(a,b) < ab-\max\{\Delta(a),\Delta(b)\}. \tag{1.4}$$

The proof constructs a finite nonnegative measure adapted to a horizontal strip, following Nagamochi's general framework of weighted areas, line segments, and points. Line mass on complete horizontal segments and point masses of $1/2$ compensate for area outside the strip. The construction and the required geometric estimates are given in Section 5.

Among the consequences in Section 6 are an obstruction for integer rectangles and an explicit lower bound for $s(N)$ that improves strictly on the area bound for every nonsquare integer $N \geq 8$. In particular, the rectangle bound recovers one of the two near-square identities in (1.2).

**Corollary 1.2.** *For every integer $k \geq 2$, $s(k^2-1) = k$.*

This identity is already stated in [1, Theorem 2(i)]; our contribution is a proof for $k \geq 3$ independent of the failed scoring assertion. The case $k = 2$, namely $s(3) = 2$, is classical [4, Theorem 1]. Our argument does not establish the second identity $s(k^2-2) = k$.

## 2 Nagamochi's score

We use the enlarged-square formulation given in [1, Section 3, following Lemma 1], and write $\sigma(S)$ for Nagamochi's original score. In this formulation, the container and weighted supports are unchanged, while the square being scored has side length $\lambda > 1$. Thus the area and line weights carry no additional factors of $\lambda$.

Let $R = [0,a]\times[0,b]$, where $a,b > 2$ are arbitrary real numbers. We use strict inequalities here so that the eight weighted points in $Q$ below are distinct. The construction in [1, Section 3 and Figure 1] consists of a central rectangle

$$R^* = [1,a-1]\times[1,b-1],$$

four line segments

$$\begin{aligned} L_1 &= [0.9,a-0.9]\times\{1\}, & L_2 &= [0.9,a-0.9]\times\{b-1\},\\ L_3 &= \{1\}\times[0.9,b-0.9], & L_4 &= \{a-1\}\times[0.9,b-0.9], \end{aligned} \tag{2.1}$$

and two sets of weighted points:¹

$$\begin{aligned} Q &= \{(0.9,j),(a-0.9,j):j \in \{1,b-1\}\}\\ &\quad{}\cup\{(i,0.9),(i,b-0.9):i \in \{1,a-1\}\},\\[3pt] P &= \{(i,0.9),(i,b-0.9):i = 2,\ldots,\lceil a\rceil-2\}\\ &\quad{}\cup\{(0.9,j),(a-0.9,j):j = 2,\ldots,\lceil b\rceil-2\}. \end{aligned} \tag{2.2}$$

An index range is understood to be empty when its upper endpoint is less than $2$. We have $\#Q = 8$ and $\#P = 2\lceil a\rceil+2\lceil b\rceil-12$, where $\#$ denotes cardinality.

Assign area density $1$ to $R^*$, line density $1/2$ to each $L_j$, weight $9/20$ to each point of $Q$, and weight $1/2$ to each point of $P$. The score of a square $S \subseteq R$ is

$$\sigma(S) = \operatorname{area}(S\cap R^*)+\frac{1}{2}\sum_{j = 1}^{4}\operatorname{length}(S\cap L_j)+\frac{9}{20}\#(S\cap Q)+\frac{1}{2}\#(S\cap P). \tag{2.3}$$

Here $\operatorname{length}$ denotes Euclidean length. We also use the same score formula for Borel subsets of $R$; since all weights are nonnegative, the score is monotone under inclusion. The four line segments and the eight $Q$-points together contribute

$$\frac{1}{2}\left(2\left(a-\frac{9}{5}\right)+2\left(b-\frac{9}{5}\right)\right)+8\cdot\frac{9}{20} = a+b.$$

Adding the central area and the $P$-point contributions, the total score available in the container is

$$(a-2)(b-2)+(a+b)+(\lceil a\rceil+\lceil b\rceil-6) = ab-\Delta(a)-\Delta(b). \tag{2.4}$$

Figure 1 shows the full construction in a rectangle with symbolic side lengths $a$ and $b$.

> *[Figure 1 (PDF page 5): a rectangle with corners $0$ and sides $a$, $b$; the shaded central rectangle $R^*$; the four thick segments $L_1$, $L_2$ (horizontal) and $L_3$, $L_4$ (vertical); the eight points labelled $Q$ at the segment ends; and rows of points labelled $P$ along all four sides. Drawing not reproduced.]*
>
> **Figure 1:** Nagamochi's scoring construction in a general rectangle, drawn schematically from [1, Section 3, Figure 1]. The central region has area density $1$, the four segments have line density $1/2$, the $Q$-points have weight $9/20$ each, and the $P$-points have weight $1/2$ each.

Lemma 1 of [1], in the equivalent formulation just described, requires

$$\sigma(S) > 1\quad\text{ whenever }S \subseteq R\text{ has side length }1 < \lambda \leq \frac{101}{100}. \tag{2.5}$$

This is the local assertion on which the published rectangle bound rests. Choose a packing of $M = \nu(a,b)$ unit squares in an $a'\times b'$ rectangle with $a' < a$ and $b' < b$, and uniformly enlarge it inside $R$. The enlarged squares can then be shrunk slightly about their centers, retaining a common side length $1 < \lambda \leq 101/100$ and making the closed squares pairwise disjoint. If (2.5) were valid, summing their scores would give

$$\nu(a,b) < \sum_{i = 1}^{M}\sigma(S_i) \leq ab-\Delta(a)-\Delta(b),$$

by (2.4). This explains the intended deduction of (1.1) from the scoring assertion.

We next examine the missing edge-incidence condition in Section 3. The counterexample in Section 4 then uses only a small neighborhood of one corner, where the other weighted supports contribute nothing.

¹ For $P$, we follow [1, Figure 1], correcting the interchange of $a$ and $b$ in two coordinates of the printed definition.

## 3 The missing edge-incidence condition

The issue occurs in [1, Section 5.5, Case 6]. We consider $a > 3$ and $b > 2$, the range used for the counterexample below. In Case 6, the center of $S$ lies in $[1,a-1]\times[0,1]$, and the line $y = 1$ intersects two adjacent edges $e_1$ and $e_2$ of $S$. After symmetry and the preceding reductions, $S$ contains $(1,0.9)$, contains no point of $P$, and contains neither $(0.9,1)$ nor $(a-1,0.9)$. To estimate the score in this case, the argument considers a limiting contact configuration with one corner of $S$ on the $x$-axis and $(2,0.9)$ on an edge of $S$. It then handles the case $(1,1) \in S$ separately and invokes [1, Lemma 6] when $(1,1) \notin S$.

However, [1, Lemma 6] requires that the point $(2,0.9)$ lie on the designated edge $e_2$, one of the two adjacent edges intersected by the line $y = 1$, as shown in [1, Figure 4(b)]. Contact with an arbitrary edge need not give this incidence. This suggests examining an almost axis-parallel square for which contact with $(2,0.9)$ occurs on a third edge, distinct from the two cut by $y = 1$, as shown in Figure 2.

> *[Figure 2 (PDF page 5): a slightly tilted square between the lines $y = 0$ and $y = 1$, with the dashed line $y = 0.9$; the line $y = 1$ cuts the square's two upper adjacent edges, while the marked point $(2, 0.9)$ lies on its right-hand edge. Drawing not reproduced.]*
>
> **Figure 2:** The counterexample idea, shown schematically with separations exaggerated. The line $y = 1$ cuts two adjacent edges, while $(2,0.9)$ lies on another edge.

Our counterexample is designed to contain $(1,0.9)$, of weight $9/20$, while capturing nearly one unit of the weighted line $y = 1$. A sufficiently small concentric shrink moves the boundary point $(2,0.9)$ outside while preserving $(1,0.9)$ inside and keeping the side length greater than $1$. Since the shrunken square lies inside the original square, none of the remaining score contributions can increase. The two dominant contributions are then close to

$$\frac{9}{20}+\frac{1}{2} = \frac{19}{20}.$$

With a sufficiently small upper cap and a short intersection with the vertical weighted line, this square can have total score less than $1$. In the next section, we make this construction explicit.

## 4 Constructing a counterexample

Fix arbitrary real numbers $a > 3$ and $b > 2$. We now restrict attention to squares near the lower-left corner of $R = [0,a]\times[0,b]$. Specifically, consider squares $S$ satisfying

$$S \subseteq [0,3)\times[0,2),\qquad \max_{(x,y) \in S}x < a-1,\qquad \max_{(x,y) \in S}y < b-1. \tag{4.1}$$

The only weighted points that can meet such a square are

$$Q_0 = \{(0.9,1),(1,0.9)\} \subseteq Q,\qquad P_0 = \{(2,0.9)\} \subseteq P.$$

The segments $L_2$ and $L_4$, on $y = b-1$ and $x = a-1$, are also disjoint from $S$. Thus the complete score (2.3) reduces in this neighborhood to

$$\sigma(S) = \operatorname{area}(S\cap R^*)+\frac{1}{2}\operatorname{length}(S\cap L_1)+\frac{1}{2}\operatorname{length}(S\cap L_3)+\frac{9}{20}\#(S\cap Q_0)+\frac{1}{2}\#(S\cap P_0). \tag{4.2}$$

Figure 3 shows these local supports.

> *[Figure 3 (PDF page 6): axes $x$ and $y$ with ticks at $1$ and $2$; the shaded corner of $R^*$ above $y = 1$ and right of $x = 1$; the segments $L_1$ (from $(0.9, 1)$ rightwards) and $L_3$ (from $(1, 0.9)$ upwards); the two points of $Q_0$ at $(0.9, 1)$ and $(1, 0.9)$; and the point $P_0$ at $(2, 0.9)$. Drawing not reproduced.]*
>
> **Figure 3:** The relevant part of Nagamochi's scoring construction near the lower-left corner.

Choose

$$0 < t \leq \frac{1}{50},\qquad t < \min\{10(a-3),b-2\}. \tag{4.3}$$

The second condition keeps the construction away from the opposite weighted supports. For every such rectangle, admissible values of $t$ exist arbitrarily close to $0$. Let $K_t$ be the contact square with vertices

$$\begin{aligned} A &= \left(2-\frac{9}{10}t,0\right), & B &= \left(2+\frac{1}{10}t,1\right), \\ C &= \left(1+\frac{1}{10}t,1+t\right), & D &= \left(1-\frac{9}{10}t,t\right), \end{aligned} \tag{4.4}$$

listed in cyclic order. Its consecutive edge vectors $(t,1)$ and $(-1,t)$ are perpendicular and have equal length. Its side length therefore satisfies

$$1 < \lambda_t = \sqrt{1+t^2} \leq \sqrt{1+\frac{1}{2500}} < \frac{101}{100}. \tag{4.5}$$

All its coordinates are nonnegative, and

$$\max_{(x,y) \in K_t}x = 2+\frac{t}{10} < \min\{3,a-1\},\qquad \max_{(x,y) \in K_t}y = 1+t < \min\{2,b-1\}. \tag{4.6}$$

Thus $K_t$ satisfies (4.1).

At height $y = 0.9$, its horizontal cross-section is $[1-t^2,2]\times\{0.9\}$; see (A.1). Hence $(1,0.9)$ is in its interior and $(2,0.9)$ lies on $AB$. The vertex $B$ lies exactly on $y = 1$, which simplifies the calculation. Appendix A shows that $K_t$ contains exactly one $Q_0$-point, that its intersections with $L_1$ and $L_3$ have lengths $1+t^2$ and $t$, and that its area inside $R^*$ is $t(1+t^2)/2$. Its full score includes the mass $1/2$ of the boundary point $(2,0.9)$. Subtracting this contribution gives

$$\sigma(K_t)-\frac{1}{2} = \frac{19}{20}+t+\frac{1}{2}t^2+\frac{1}{2}t^3. \tag{4.7}$$

The polynomial on the right is strictly increasing for $t > 0$ and equals $242551/250000$ at $t = 1/50$. Therefore,

$$\sigma(K_t\setminus P_0) = \sigma(K_t)-\frac{1}{2} \leq \frac{242551}{250000} < 1. \tag{4.8}$$

For each fixed $t$, shrink $K_t$ about its center by a factor less than $1$ and sufficiently close to $1$, obtaining a square $S_t$ whose side length remains greater than $1$ and whose interior still contains $(1,0.9)$. Since $S_t \subseteq K_t^\circ$, it avoids $P_0$ and satisfies $\sigma(S_t) \leq \sigma(K_t\setminus P_0) < 1$. Its side length is also less than $101/100$ by (4.5), so it contradicts (2.5).

To exhibit the missing contact configuration, shrink $K_t$ about $A$ by a factor less than $1$ and sufficiently close to $1$, preserving $(1,0.9)$ in the interior and keeping the side length greater than $1$. The point $(2,0.9)$ remains in the relative interior of the image of $AB$. The images of $B$ and $D$ lie below $y = 1$, while the image of $C$ remains above it. Thus $y = 1$ cuts the images of $BC$ and $CD$, and the contact edge is different from both. In particular, it is not the designated edge $e_2$ required by [1, Lemma 6]. The concentric shrink supplies the score counterexample; the shrink about $A$ serves only to exhibit the missing edge incidence.

## 5 A strip measure for rectangles

We prove Theorem 1.1 without invoking the scoring assertion or the technical lemmas of [1]. Following the same principle of assigning weights to areas, line segments, and points as in [1, Section 3], we construct a finite nonnegative measure adapted to a horizontal strip. Its total mass is $ab-\Delta(a)$, while the interior of every square of side length slightly greater than $1$ has measure greater than $1$.

Fix $a \geq 2$ and $b \geq 3$, set $R = [0,a]\times[0,b]$, and define

$$\begin{aligned} H &= [0,a]\times[1,b-1],\\ L_- &= [0,a]\times\{1\},\\ L_+ &= [0,a]\times\{b-1\},\\ W &= \{(j,4/5),(j,b-4/5):j = 1,\ldots,\lceil a\rceil-1\}. \end{aligned}$$

Assign area density $1$ to $H$, line density $1/2$ to each of $L_-$ and $L_+$, and point mass $1/2$ to each point of $W$. For a Borel set $E \subseteq R$, define

$$\mu(E) = \operatorname{area}(E\cap H)+\frac{1}{2}\operatorname{length}(E\cap L_-)+\frac{1}{2}\operatorname{length}(E\cap L_+)+\frac{1}{2}\#(E\cap W). \tag{5.1}$$

Here $\operatorname{area}$ is two-dimensional Lebesgue measure, and $\operatorname{length}$ on each supporting line is one-dimensional Lebesgue measure. The two rows of $W$ are distinct and each contains $\lceil a\rceil-1$ points. Thus $\mu$ is a finite nonnegative measure, with total mass

$$\mu(R) = a(b-2)+\frac{a}{2}+\frac{a}{2}+\frac{1}{2}(2\lceil a\rceil-2) = ab-\Delta(a). \tag{5.2}$$

Figure 4 shows the construction. For each packed square $S$, we estimate $\mu(S^\circ)$, the mass in its interior.

> *[Figure 4 (PDF page 8): a rectangle with sides $a$ and $b$; the shaded strip $H$ between heights $1$ and $b-1$; the thick lines $L_-$ at height $1$ and $L_+$ at height $b-1$; and two rows of points labelled $W$ at heights $4/5$ and $b - 4/5$. Drawing not reproduced.]*
>
> **Figure 4:** The strip measure in a rectangle. The two rows of point masses have integer abscissae strictly between $0$ and $a$, at heights $4/5$ and $b-4/5$.

**Proposition 5.1.** *Every square $S \subseteq R$ of side length $1 < \lambda \leq 101/100$ satisfies $\mu(S^\circ) > 1$.*

The upper bound $101/100$ is a convenient choice, also used in [1]. We first establish elementary geometric estimates. They play roles analogous to the chord and cap estimates in [1, Lemmas 2–5], but the proofs below are independent of those assertions.

**Lemma 5.2 (Estimates near a horizontal boundary).** *Let $S \subseteq \{y \geq 0\}$ be a square of side $1 < \lambda \leq 101/100$ whose center has height at most $1$. Then the following hold.*

*(i) For every $r$ satisfying $\frac{3-\sqrt{2}}{2} < r < \sqrt{2}-\frac{1}{2}$,*

$$\operatorname{length}(S^\circ\cap\{y = r\}) > 1.$$

*(ii) For $A = \operatorname{area}(S\cap\{y \geq 1\})$ and $\ell = \operatorname{length}(S^\circ\cap\{y = 1\})$,*

$$A + \frac{\ell}{2} \geq \lambda^2-\frac{\lambda}{2}.$$

*Proof.* Up to reflection and relabeling of the sides, use an orientation $0 \leq \theta \leq \pi/4$. Let

$$h = \sin\theta + \cos\theta\qquad\text{ and }\qquad p = \sin\theta\cos\theta.$$

For $\theta > 0$, the horizontal chord length at height $z$ above the lowest vertex is

$$w(z) = \begin{cases} \dfrac{z}{p}, & 0 < z < \lambda \sin\theta,\\[6pt] \dfrac{\lambda}{\cos\theta}, & \lambda \sin\theta \leq z \leq \lambda \cos\theta,\\[6pt] \dfrac{\lambda h-z}{p}, & \lambda \cos\theta < z < \lambda (\sin\theta+\cos\theta) = \lambda h. \end{cases} \tag{5.3}$$

*Proof of (i).* Let $z_c$ denote the height of the center of $S$. Since $S \subseteq \{y \geq 0\}$, the vertical distance from the center of $S$ to its lowest point gives $z_c \geq \lambda h/2$. By hypothesis, $z_c \leq 1$.

If $\theta = 0$, then $h = 1$, so $\lambda/2 \leq z_c \leq 1$. The lower and upper sides of $S$ therefore have heights

$$z_c-\frac{\lambda}{2} \leq 1-\frac{\lambda}{2} < \frac{1}{2} < r \qquad\text{ and }\qquad z_c+\frac{\lambda}{2} \geq \lambda > 1 > r,$$

respectively. Thus the line $y = r$ crosses the two vertical sides of $S$, and the resulting chord has length $\lambda > 1$.

Suppose henceforth that $\theta > 0$. Let

$$z_0 = z_c-\frac{\lambda h}{2}$$

be the height of the lowest vertex of $S$. Since

$$\frac{\lambda h}{2} \leq z_c \leq 1,$$

the relative height of the line $y = r$ above this vertex,

$$r-z_0 = r-z_c+\frac{\lambda h}{2},$$

ranges between

$$z_- = \frac{\lambda h}{2}+r-1\qquad\text{and}\qquad z_+ = r.$$

Both values lie strictly between $0$ and $\lambda h$. Since the chord profile (5.3) is concave on its support, it is enough to check these two endpoint positions. We first record two trigonometric bounds.

We use $p = (h^2-1)/2$ and $1 \leq h \leq \sqrt{2}$, which give

$$h-p \geq \sqrt{2}-\frac{1}{2} > r, \tag{5.4}$$

$$\frac{h}{2}-p \geq \frac{\sqrt{2}-1}{2} > 1-r. \tag{5.5}$$

Both expressions on the left are decreasing functions of $h$ on $[1,\sqrt{2}]$, so their minima occur at $h = \sqrt{2}$.

Since $z_- < \lambda h/2 \leq \lambda\cos\theta$, the height $z_-$ lies in the lower triangle or the plateau. Hence

$$w(z_-) = \begin{cases} \dfrac{z_-}{p} > \dfrac{1}{p}\left(\dfrac{h}{2}+r-1\right) > 1\text{ by (5.5)}, & 0 < z_- < \lambda \sin\theta,\\[6pt] \dfrac{\lambda}{\cos\theta} > \lambda > 1, & \lambda \sin\theta \leq z_- \leq \lambda \cos\theta. \end{cases} \tag{5.6}$$

Similarly, $\lambda\sin\theta \leq 101/(100\sqrt{2}) < \frac{3-\sqrt{2}}{2} < z_+$, so the height $z_+$ lies in the plateau or the upper triangle. Thus

$$w(z_+) = \begin{cases} \dfrac{\lambda}{\cos\theta} > \lambda > 1, & \lambda \sin\theta \leq z_+ \leq \lambda \cos\theta,\\[6pt] \dfrac{\lambda h-z_+}{p} > \dfrac{h-r}{p} > 1\text{ by (5.4)}, & \lambda \cos\theta < z_+ < \lambda h. \end{cases} \tag{5.7}$$

Both endpoint chords have length greater than $1$, proving (i).

*Proof of (ii).* Since $z_c \leq 1$ and the highest point has height $z_c+\lambda h/2 \geq \lambda h > 1$, the line $y = 1$ intersects the square at or above its center. It therefore either cuts two opposite sides or bounds an upper triangular cap.

If the line cuts two opposite sides, the chord profile (5.3) gives

$$\ell = \frac{\lambda}{\cos\theta},\qquad A = \frac{\lambda^2}{2}-\frac{\lambda}{\cos\theta}(1-z_c) \geq \frac{\lambda^2}{2}-\frac{\lambda}{\cos\theta}\left(1-\frac{\lambda h}{2}\right).$$

Consequently,

$$A+\frac{\ell}{2}-\left(\lambda^2-\frac{\lambda}{2}\right) \geq \frac{\lambda}{2\cos\theta}(\lambda\sin\theta+\cos\theta-1) \geq 0,$$

because $\lambda\sin\theta+\cos\theta \geq \sin\theta+\cos\theta \geq 1$. This also covers the axis-parallel orientation $\theta = 0$.

If the line creates an upper triangular cap, the chord profile (5.3) and $p > 0$ give

$$\ell = \frac{z_c+\lambda h/2-1}{p} \geq \frac{\lambda h-1}{p},\qquad A = \frac{\ell}{2}\left(z_c+\frac{\lambda h}{2}-1\right) \geq \frac{(\lambda h-1)^2}{2p}.$$

Consequently,

$$A+\frac{\ell}{2}-\left(\lambda^2-\frac{\lambda}{2}\right) \geq \frac{\lambda}{2p}(\lambda-h+p) \geq 0,$$

because $2p = h^2-1$ and $\lambda-h+p > 1-h+p = (h-1)^2/2 \geq 0$. $\square$

For a square $S \subseteq R$ satisfying the lemma's hypotheses, taking $r = 4/5$ in Lemma 5.2(i) shows that $S^\circ\cap\{y = 4/5\}$ is an open interval of length greater than $1$. Its set of abscissae is an open interval of length greater than $1$ contained in $[0,a]$, and hence contains an integer in $\{1,\ldots,\lceil a\rceil-1\}$. Thus $S^\circ$ contains at least one weighted point of $W$, contributing $1/2$ to $\mu(S^\circ)$.

*Proof of Proposition 5.1.* Let $z_c$ be the height of the center of $S$.

*Centers near the bottom or top.* Suppose first that $z_c \leq 1$. Its maximum height is at most

$$z_c+\frac{\lambda}{\sqrt{2}} \leq 1+\frac{101\sqrt{2}}{200} < 2 \leq b-1.$$

Thus $S$ cannot lose weighted area through the top of $H$; its area contribution is exactly $A$ from Lemma 5.2(ii). Lemma 5.2(i) supplies a weighted point in the interior, contributing mass $1/2$. Combining the two estimates gives

$$\mu(S^\circ) \geq \lambda^2-\frac{\lambda}{2}+\frac{1}{2} = 1+(\lambda-1)\left(\lambda+\frac{1}{2}\right) > 1.$$

Reflection in $y = b/2$ proves the same assertion when $z_c \geq b-1$.

*Centers in the strip.* It remains to consider $1 \leq z_c \leq b-1$. Call a horizontal boundary of $H$ a *proper cut* if $S$ has positive area on both sides of that line. Every proper cut either removes a triangular cap or meets the interiors of two opposite sides of $S$.

For a triangular cap with side lengths $u,v \leq \lambda$ measured along two adjacent sides of $S$, let $D$ be its area and $\ell$ its base length. Then

$$\frac{D}{\ell} = \frac{uv}{2\sqrt{u^2+v^2}} \leq \frac{\sqrt{uv}}{2\sqrt{2}} \leq \frac{\lambda}{2\sqrt{2}} < \frac{1}{2}. \tag{5.8}$$

Thus the line mass $\ell/2$ more than compensates for the lost area.

If every proper cut is triangular, compensate every triangular loss using (5.8). The area and line contributions are at least $\lambda^2 > 1$.

If exactly one proper cut is not triangular, its chord has length at least $\lambda$. The center is on the retained side, so at most half the square's area is lost through that boundary. Compensating any triangular loss at the other boundary gives

$$\mu(S^\circ) \geq \frac{\lambda^2}{2}+\frac{\lambda}{2} > 1.$$

If both proper cuts are nontriangular, their line contributions alone total at least $\lambda > 1$.

These cases include $b = 3$, when a square can cross both horizontal boundaries of the strip. They also account for tangencies, since only proper cuts require compensation. This completes the proof. $\square$

*Proof of Theorem 1.1.* Let $M = \nu(a,b)$, and choose an $a'\times b'$ rectangle with $a' < a$ and $b' < b$ admitting a packing of $M$ unit squares. Choose $\lambda$ sufficiently close to $1$ that

$$1 < \lambda \leq \frac{101}{100},\qquad \lambda a' < a,\qquad \lambda b' < b.$$

Uniformly scaling the packing by $\lambda$ gives squares $S_1,\ldots,S_M$ of side $\lambda$ with pairwise disjoint interiors inside $R$. By additivity and nonnegativity of $\mu$, Proposition 5.1, and (5.2),

$$M < \sum_{i = 1}^{M}\mu(S_i^\circ) = \mu\left(\bigcup_{i = 1}^{M}S_i^\circ\right) \leq \mu(R) = ab-\Delta(a).$$

This proves (1.3). When $a,b \geq 3$, rotating the construction gives $M < ab-\Delta(b)$ as well. Taking the stronger of the two inequalities yields (1.4). $\square$

## 6 Consequences for rectangle and square packings

For integer target side lengths, the correction $\Delta$ equals $1$, giving the following obstruction.

**Corollary 6.1 (Integer rectangles).** *Let $m,n \geq 2$ be integers. No $m'\times n'$ rectangle with $m' < m$ and $n' < n$ can contain $mn-1$ unit squares with pairwise disjoint interiors.*

*Proof.* By interchanging the two directions, assume $n \geq m$. If $n \geq 3$, Theorem 1.1 with $a = m$ and $b = n$ gives $\nu(m,n) < mn-\Delta(m) = mn-1$. If $m = n = 2$, the smaller rectangle is contained in a square of side $\max\{m',n'\} < 2$, which cannot contain three unit squares by the classical identity $s(3) = 2$ [4, Theorem 1]. $\square$

*Proof of Corollary 1.2.* Taking $m = n = k$ in Corollary 6.1 shows that $k^2-1$ unit squares cannot fit in a square of side less than $k$. The $k\times k$ grid with one square removed gives the reverse inequality, so $s(k^2-1) = k$. $\square$

The rectangle theorem also gives an explicit lower bound for every nonsquare integer $N \geq 8$.

**Corollary 6.2 (A general lower bound).** *Let $N \geq 8$ be a nonsquare integer. Then*

$$s(N) \geq \frac{1}{2}+\sqrt{N-\lfloor\sqrt{N}\rfloor+\frac{1}{4}} > \sqrt{N}. \tag{6.1}$$

*Proof.* Let $k = \lfloor\sqrt{N}\rfloor$. Since $N$ is a nonsquare integer, $k^2 < N \leq (k+1)^2-1$. By Theorem 1.1, any $t \geq 3$ satisfying $t^2-\Delta(t) = N$ gives $s(N) \geq t$. On the interval $k < t \leq k+1$, we have $\Delta(t) = t-k$, so this equation becomes $t^2-t+k = N$. The positive root of this quadratic is

$$t = \frac{1}{2}+\sqrt{N-k+\frac{1}{4}}.$$

The inequalities for $N$ give

$$\left(k-\frac{1}{2}\right)^2 < N-k+\frac{1}{4} \leq \left(k+\frac{1}{2}\right)^2$$

and therefore $k < t \leq k+1$. Hence $\lceil t\rceil = k+1$, and by construction

$$t^2-\Delta(t) = t^2-t+k = N.$$

We also have $t \geq 3$: for $N = 8$, the formula gives $t = 3$, while for $N > 8$ the nonsquare assumption implies $k \geq 3$ and hence $t > k \geq 3$. If $N$ unit squares could be packed in a square of side less than $t$, then Theorem 1.1, applied with $a = b = t$, would give

$$N \leq \nu(t,t) < t^2-\Delta(t) = N,$$

a contradiction. Thus $s(N) \geq t$.

Finally, since $t > k$,

$$t^2 = N+t-k > N,$$

and hence $t > \sqrt{N}$. $\square$

For $N = n^2-1$ with $n \geq 3$, the lower bound in (6.1) is exactly $n$. Thus the family in Corollary 1.2 also occurs at the endpoints of this general bound.

## 7 Concluding remarks

Section 4 gives a local family violating the scoring assertion in [1, Lemma 1]. The family applies near a corner of every rectangle with $a > 3$ and $b > 2$ once the parameter is sufficiently small. Shrinking the same contact square about a vertex produces a strict configuration exhibiting the missing edge-incidence condition in the application of [1, Lemma 6]. The published derivation of the rectangle bound and its consequences therefore requires a correction or an additional argument; the family is not itself a packing that violates those bounds.

The strip measure provides a partial replacement for Nagamochi's theorem. For $a,b \geq 3$, it yields the correction $\max\{\Delta(a),\Delta(b)\}$ in place of $\Delta(a)+\Delta(b)$. Its consequences include the integer-rectangle obstruction, the lower bound (6.1), and an independent proof of

$$s(k^2-1) = k.$$

Thus one of the two nontrivial infinite near-square families stated in [1, Theorem 2] is recovered without the disputed scoring assertion. The present argument does not establish or disprove Nagamochi's full rectangle bound, the identity

$$s(k^2-2) = k,$$

or the stronger general lower bound stated in [1, Theorem 2].

This leaves a natural geometric question. The strip measure charges only one pair of opposite sides of the container and has total mass $ab-\Delta(a)$; after rotation it gives the corresponding correction in the other direction. Can the two boundary corrections be combined without creating a square of mass at most $1$? For a square container $[0,k]^2$, such a construction would need total mass $k^2-2$ rather than the $k^2-1$ supplied by the present strip measure. A successful construction of this kind could provide a new route toward the unresolved part of Nagamochi's claimed bound.

More broadly, the issue illustrates the difficulty of rigorous lower bounds in square packing. Numerical and geometric constructions can often suggest very efficient arrangements, whereas an optimality proof must control every possible translation and orientation. Weighted measures and unavoidable-set arguments remain useful precisely because they turn this global packing problem into local geometric inequalities, but the counterexample here shows that the incidence conditions underlying those inequalities must be tracked carefully.

**Use of AI tools.** AI tools were used during exploratory work, for symbolic and numerical checks, and for language and typesetting assistance. All mathematical arguments and calculations appearing in the article were independently checked by the author.

## A Calculations for the counterexample

We verify the contact-square score (4.7) used in Section 4. Throughout this appendix, $a > 3$, $b > 2$, and $t$ satisfies (4.3). The square $K_t$ has vertices (4.4), with edge directions $B-A = C-D = (t,1)$ and $D-A = C-B = (-1,t)$.

**Weighted point contributions.** Parametrize $AB$ by $A+s(t,1)$, where $0 \leq s \leq 1$. At height $y = 0.9$, we have $s = 9/10$, giving the right endpoint

$$\left(2-\frac{9}{10}t\right)+\frac{9}{10}t = 2.$$

Similarly, on $DC$, parametrized by $D+s(t,1)$, the same height gives $s = 9/10-t$ and the left endpoint

$$\left(1-\frac{9}{10}t\right)+t\left(\frac{9}{10}-t\right) = 1-t^2.$$

Both parameter values lie strictly between $0$ and $1$, so the chord is

$$K_t\cap\{y = 0.9\} = [1-t^2,2]\times\{0.9\}. \tag{A.1}$$

Thus $(1,0.9)$ lies in $K_t^\circ$, and $(2,0.9)$ lies on $AB$. Moreover,

$$\min_{(x,y) \in K_t}x = 1-\frac{9}{10}t \geq \frac{491}{500} > 0.9,$$

so the point column $x = 0.9$ is disjoint from $K_t$. Together with (4.6), this excludes all remaining weighted points. Hence

$$\#(K_t\cap Q_0) = 1,\qquad \#(K_t\cap P_0) = 1, \tag{A.2}$$

and the total point contribution is $9/20+1/2$.

**Intersection with the horizontal weighted line.** The vertex $B$ lies on $y = 1$. On the opposite edge $DC$, the parametrization $D+s(t,1)$ reaches this height at $s = 1-t$. Its abscissa is

$$\left(1-\frac{9}{10}t\right)+t(1-t) = 1+\frac{1}{10}t-t^2.$$

The full chord lies within $L_1$, giving

$$K_t\cap L_1 = \left[1+\frac{1}{10}t-t^2,2+\frac{1}{10}t\right]\times\{1\}. \tag{A.3}$$

Subtracting the endpoints yields

$$\operatorname{length}(K_t\cap L_1) = 1+t^2. \tag{A.4}$$

The left endpoint lies strictly to the right of $x = 1$, since $t/10-t^2 > 0$. In particular, $(1,1)$ is outside $K_t$.

**Intersection with the vertical weighted line.** The upper intersection with $x = 1$ lies on $DC$. Its first coordinate equals $1$ when

$$1-\frac{9}{10}t+st = 1,\qquad s = \frac{9}{10},$$

giving height $0.9+t$. The lower intersection lies on $AD$, parametrized by $A+s(-1,t)$. Its first coordinate equals $1$ when

$$2-\frac{9}{10}t-s = 1,\qquad s = 1-\frac{9}{10}t,$$

giving height $t(1-9t/10) < t \leq 1/50 < 0.9$. Since $L_3$ starts at height $0.9$ and extends beyond $0.9+t$, it follows that

$$K_t\cap L_3 = \{1\}\times[0.9,0.9+t],\qquad \operatorname{length}(K_t\cap L_3) = t. \tag{A.5}$$

**Area inside the central region.** The upper vertex $C$ lies to the right of $x = 1$, as does the full chord (A.3). Together with (4.6), this shows that the portion above $y = 1$ is entirely inside $R^* = [1,a-1]\times[1,b-1]$. It is a triangle with base $1+t^2$ and height $t$, so

$$\operatorname{area}(K_t\cap R^*) = \frac{t}{2}(1+t^2). \tag{A.6}$$

**The contact-square score.** Substituting (A.2), (A.4), (A.5), and (A.6) into (4.2) gives

$$\sigma(K_t) = \frac{9}{20}+\frac{1}{2}+\frac{1}{2}(1+t^2)+\frac{t}{2}+\frac{t(1+t^2)}{2} = \frac{29}{20}+t+\frac{1}{2}t^2+\frac{1}{2}t^3.$$

Subtracting the boundary point's mass $1/2$ yields (4.7).

## References

[1] Hiroshi Nagamochi, *Packing Unit Squares in a Rectangle*, The Electronic Journal of Combinatorics **12**(1) (2005), Research Paper 37, 13 pp. doi:10.37236/1934.

[2] Paul Erdős and Ronald L. Graham, *On Packing Squares with Equal Squares*, Journal of Combinatorial Theory, Series A **19**(1) (1975), 119–123. doi:10.1016/0097-3165(75)90099-0.

[3] F. Göbel, *Geometrical Packing and Covering Problems*, in *Packing and Covering in Combinatorics*, A. Schrijver (ed.), Mathematical Centre Tracts **106** (1979), 179–199.

[4] Erich Friedman, *Packing Unit Squares in Squares: A Survey and New Results*, The Electronic Journal of Combinatorics, Dynamic Survey 7, version of August 14, 2009. doi:10.37236/28.

[5] Michael J. Kearney and Peter Shiu, *Efficient Packing of Unit Squares in a Square*, The Electronic Journal of Combinatorics **9**(1) (2002), Research Paper 14. doi:10.37236/1631.

[6] Walter Stromquist, *Packing 10 or 11 Unit Squares in a Square*, The Electronic Journal of Combinatorics **10**(1) (2003), Research Paper 8. doi:10.37236/1701.

[7] Thierry Gensane and Philippe Ryckelynck, *Improved Dense Packings of Congruent Squares in a Square*, Discrete & Computational Geometry **34**(1) (2005), 97–109. doi:10.1007/s00454-004-1129-z.

[8] Wolfram Bentz, *Optimal Packings of 13 and 46 Unit Squares in a Square*, The Electronic Journal of Combinatorics **17**(1) (2010), Research Paper 126. doi:10.37236/398.

[9] Wolfram Bentz, *Optimal Packings of 22 and 33 Unit Squares in a Square*, arXiv:1606.03746 [math.CO] (2016).

[10] M. Z. Arslanov, S. A. Mustafin, and Z. K. Shangitbayev, *Improved Packings of $n(n-1)$ Unit Squares in a Square*, The Electronic Journal of Combinatorics **28**(4) (2021), Paper 4.22. doi:10.37236/8586.
