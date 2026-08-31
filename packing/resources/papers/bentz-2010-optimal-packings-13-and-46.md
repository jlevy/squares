# Optimal Packings of 13 and 46 Unit Squares in a Square

**Authors:** Wolfram Bentz
**Venue:** Electronic Journal of Combinatorics 17 (2010), #R126
**Year:** 2010
**Source:** https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1r126/pdf/
**Archived:** 2026-08-22
**Extraction:** pdfminer.six from the original PDF, cleaned for readability. Raw extraction preserved alongside as `bentz-2010-optimal-packings-13-and-46.raw.md`.

---

> ⚠️ **Contains reconstructed passages.**
> This transcription contains **1** annotated passage(s) where the PDF extraction was
> damaged and text or mathematics was reconstructed or marked unrecoverable. Search this
> file for `GARBLED` and `NOTE` to find them.
> **Any formula near an annotation must be checked against `bentz-2010-optimal-packings-13-and-46.raw.md`**, which is the
> unedited extraction and the ground truth for this document.

Department of Mathematics, Statistics, and Computer Science
St. Francis Xavier University
Antigonish, Nova Scotia, Canada
wbentz@stfx.ca

Submitted: Aug 31, 2009; Accepted: Sep 6, 2010; Published: Sep 13, 2010
Mathematics Subject Classification: 05B40, 52C15

## Abstract

Let $s(n)$ be the side length of the smallest square into which $n$ non-overlapping unit squares can be packed. We show that $s(m^2 - 3) = m$ for $m = 4, 7$, implying that the most efficient packings of 13 and 46 squares are the trivial ones.

---

The study of packing unit squares into a square goes back to Erdos and Graham [2], who showed that large numbers of unit squares can be packed in a way that is surprisingly efficient. Gobel [5] later addressed the problem of finding efficient packings for a given number $n$ of unit squares, and the subject was subsequently published in the popular science literature in various articles by Gardner [4].

Let $s(n)$ be the side length of the smallest square into which $n$ non-overlapping unit squares can be packed. Non-trivial cases for which $s(n)$ is known are $s(m^2 - 1) = s(m^2 - 2) = m$ for $m > 2$ (Nagamochi [7], single values previously shown by Gobel [5], El Moumni [1], and Friedman [3]), $s(5) = 2 + \frac{1}{\sqrt{2}}$ (Gobel [5]), $s(6) = 3$ (Kearney and Shiu [6]), and $s(10) = 3 + \frac{1}{\sqrt{2}}$ (Stromquist [9]). There are moreover non-trivial best packings and lower bounds known for various values of $n$. An introduction to the problem, as well as an overview of the basic techniques used in the following can be found in the survey article by Friedman [3].

We will show $s(m^2 - 3) = m$ for $m = 4, 7$, which implies that the optimal packings of 13 and 46 squares are the trivial ones with all edges of the unit squares either parallel or perpendicular to those of the containing square. While our results strongly suggest that the same formula holds for the intermediate values $m = 5, 6$, no specialized results are currently known in these cases, for which the best established packings are trivial, and the best lower bounds follow from the general formula given in Nagamochi [7].

Following Stromquist, let a *box* be the interior of any square larger than unit size. In our results, we will establish that $m^2 - 3$ squares cannot be packed in a square with side length smaller then $m$ by proving the equivalent statement that it is impossible to pack $m^2 - 3$ boxes in a square of side length $m$. Various configurations of points will be constructed so that each box inside our square will either have to contain one of the points or otherwise be restricted to a small area.

We begin by listing technical lemmas in Section 1. The proofs for $m = 7, 4$ ($n = 46, 13$) are then given in sections 2, 3, respectively.

## 1 Technical lemmas

In this section, we present a range of "non-avoidance" lemmas, as well as various results dealing with boxes of restricted movement. Non-avoidance lemmas state that if the centre of a box is in some region, the box must intersect some part of the region's boundary. The other results draw consequences if a box has its centre in some region without intersecting particular boundary points.

**Lemma 1** (Nagamochi [7], Stromquist [8]) A box whose centre is in the rectangle $[0, 1] \times [0, 1]$ and which does not intersect the axes must contain the points $(1, 1)$, $(0.9, 1)$, and $(1, 0.9)$ (and hence the triangle spanned by these points).

**Lemma 2** (Friedman [3], Stromquist [8]) Let $T$ be a triangle with sides of length at most 1. Then any box whose centre is in $T$ must contain one of the vertices of $T$.

**Corollary 3** Let $0 < a, b \leq 1$ and $c$ such that both $c^2 + b^2 \leq 1$ and $(a - c)^2 + b^2 \leq 1$. Then if a box has its centre inside the rectangle $R$ with vertices $H(0, 0)$, $I(0, b)$, $J(a, b)$, $K(a, 0)$, it covers a vertex or the point $L(c, 0)$. In particular, if $b < \frac{\sqrt{3}}{2}$, the box covers a vertex or the midpoint of the line segment $HK$.

*Proof:* The bounds on $a, b$ imply that Lemma 2 is applicable to the triangles $HLI$, $ILJ$, and $JLK$, which form a subdivision of $[0, a] \times [0, b]$. Hence the centre of the box is in one of the triangles, and the result follows. $\square$

**Lemma 4** (Friedman [3], Stromquist [8]) Let $a \leq 1$, $b \leq 1$, and $a + 2b \leq 2\sqrt{2}$, then any box whose centre is in the rectangle $[0, a] \times [0, b]$ must intersect the $x$-axis, the point $(0, a)$ or the point $(a, b)$.

We will usually use Lemma 4 in the cases of $a < 2\sqrt{2} - 2 \approx 0.828$, $b = 1$ and $a = 1$, $b < \sqrt{2} - \frac{1}{2} \approx 0.914$.

**Lemma 5** (Stromquist [8], [9]) Let $2\sqrt{2} - 2 < a < 1$, $0 < b < 1$, and $(a, b)$ within a distance of 1 from $(0, 1)$. Moreover, let $f(a)$ be the infimum of

$$\frac{\cos\theta}{1 + \cos\theta} + \frac{1 - a\cos\theta}{\sin\theta} \tag{1}$$

for $\theta \in (0, \frac{\pi}{4}]$. If $b < f(a)$, then any box whose centre is in the quadrilateral with vertices $(0, 0)$, $(0, 1)$, $(a, 0)$, and $(a, b)$ must intersect the $x$-axis, the point $(0, 1)$ or the point $(a, b)$. Moreover, the infimum of (1) is a minimum and is obtained at a value of $\theta$ satisfying

$$2\cos^3\theta - (2a + 2)\cos^2\theta + (a^2 - 2a + 3)\cos\theta - (1 - a^2) = 0. \tag{2}$$

We will be using Lemma 5 in the cases $a = \frac{\sqrt{3}}{2}$, $b = 0.5$; $a \leq 0.89$, $0.6 < b \leq 0.921$; $a = 0.90$, $b = 0.90$; and $a = 0.96$, $b = 0.76$. Note that $f(a)$ is decreasing in $a$.[^1]

[^1]: In its original form the Lemma states incorrectly that the smallest positive $\theta$ satisfying (2) realizes the minimum of (1). In fact, the minimum values in some of our cases corresponds to the second largest positive root of (2).

**Lemma 6** (Stromquist [8]) Let $L_1$ and $L_2$ be two parallel lines of distance $d \leq 1$, and $B$ a box with its centre between them. Then $B$ must intersect the two lines with a common length of intersection of at least $\min\{1, 2\sqrt{2} - 2d\}$.

We will use the Lemma in the situation of the following corollary, which will be a major technical tool for this article.

**Corollary 7** Let $0 < b \leq 1$, and $R$ be the rectangle with vertices $(0, 0)$, $(0, 1)$, $(b, 0)$, $(b, 1)$. Then any box whose centre lies inside $R$ without containing any of its vertices intersects the line segments $\{0\} \times [0, 1]$ and $\{b\} \times [0, 1]$ with a common length of intersection of at least $2\sqrt{2} - 2 \approx 0.828$. In addition, if $b > 2\sqrt{2} - 2$ then the box intersects each segment with a length of at least $b - 2\sqrt{2} + 2$.
<!-- NOTE (two reconstructions here, verify against the .raw.md before relying on this corollary):
     1. Segments: the raw extraction reads "{0} x [0, b] and {1} x [0, b]". Rendered here as the
        left and right edges of R, i.e. {0} x [0,1] and {b} x [0,1].
     2. INEQUALITY DIRECTION CHANGED: the raw extraction reads "if 2 sqrt(2) - 2 > b", and this
        transcription states "if b > 2 sqrt(2) - 2". The raw text is column-interleaved so its
        ordering is unreliable, but this is a change to the mathematics and was NOT disclosed in
        the original annotation. Treat the direction as UNVERIFIED.
     The leading claim -- common intersection length at least 2 sqrt(2) - 2 ~ 0.828 -- is
     unambiguous in the raw extraction and is not affected. -->

In the situation of Corollary 7, we will simply refer to the (length of the) intersection of the box with one of the edges of $R$ as being the left, right, up, or down intersection.

## 2 46 Squares

The non-avoidance lemmas can be used directly to prove the following theorem, implying that $s(46) = 7$, and that the optimal packing of 46 is the trivial one. Its proof is surprisingly simple for such a large case, in particular when compared to the case of 13 squares.

**Theorem 8** 46 non-overlapping unit squares cannot be packed in a square of side length less than 7.

*Proof:* Let $S$ be the square $[0, 7]^2$ and consider the collection of 45 points depicted in Figure 1. The points in the lowest row are

$$\left(i, \sqrt{2} - \frac{1}{2}\right) \qquad i = 1, 2, \ldots, 6,$$

and the remaining ones are arranged so that all shown triangles are equilateral of side length 1. Note that the points in the uppermost row have $y$-value

$$\sqrt{2} - \frac{1}{2} + 6 \cdot \frac{\sqrt{3}}{2} > 6.11,$$

and are less than $\sqrt{2} - \frac{1}{2}$ from the upper edge of $S$. Lemma 2 is applicable to the triangles, Lemma 4 to the rectangles, and Lemma 5 to the remaining quadrilateral regions (with $a = \frac{\sqrt{3}}{2}$, $b = \frac{1}{2}$). Thus any box placed inside $S$ must contain one of the points, showing that no more than 45 boxes can be placed in $S$. The result follows. $\square$

> *[Figure 1: Unavoidable set with 45 points -- not extractable from PDF]*

## 3 13 Squares

In this section we will prove the following theorem, implying that $s(13) = 4$.

**Theorem 9** 13 non-overlapping unit squares cannot be packed in a square of side length less than 4.

From now on, let $S$ be the square $[0, 4]^2$, and assume that 13 boxes are packed into $S$. Consider first the configuration of 16 points as shown in Figure 2. Four points have coordinates

$$A(1, 0.914),\quad B(0.914, 1),\quad C(0.914, 2),\quad D(1.65, 1.65)$$

while the remaining ones are obtained through mirroring at the lines $x = 2$, $y = 2$, and $y = x$.

Non-avoidance lemmas apply to all regions, so each box contains at least one point. With 13 boxes and 16 points, at least 10 boxes contain exactly one point. This implies that of the eight points closest to the corners of $S$, at least two are in a box that does not contain another point. We will refer to two such boxes (arbitrarily selected if necessary) as being "corner restricted".

> *[Figure 2: Initial configuration for 13 squares -- not extractable from PDF]*

**Lemma 10** If a box $T$ covers $A(1, 0.914)$ but not any other point in Figure 2, then it contains $(1.12, 1)$, $(1, 1.74)$, and $(1.87, 0.76)$ (and hence the convex hull of these four points).

*Proof:* This follows as the set stays unavoidable if $A$ is replaced by any of the other points. $\square$
<!-- NOTE (audited 2026-08-31, cases/bentz13/lemma10_audit.py -- verify against the published
     PDF before relying on this lemma as printed):
     The point "(1, 1.74)" is refuted as printed: the axis-aligned box of side 1001/1000
     centred at (1.46, 0.7) lies inside [0,4]^2 and strictly avoids every point of
     (Figure 2 minus A) union {(1, 1.74)} -- an exact escape certificate, so that
     replacement set is NOT unavoidable and the proof line fails for it. Three independent
     lines say the intended point is (1.74, 1): the same box contains (1.74, 1); Section
     3.2's S_A lists (1.4, 1) and (1.74, 1) "by Lemmas 10 and 11", which lie in the hull
     only under the corrected reading; and (1, 1.74) is exactly the y = x mirror of
     (1.74, 1), i.e. the point the symmetric B-covering version of this lemma delivers,
     which is how Section 3.1's alternatives use it. The raw extraction carries the same
     "(1, 1.74)" reading, so whether the transposition is the paper's or the extraction
     pipeline's is undecidable from this repository. Held unresolved with needs_review. -->

We will distinguish two cases of placements of the corner-restricted boxes.

### 3.1 Non-adjacent corner-restricted boxes

Without losing generality we may assume that one of the corner-restricted boxes covers point $A$. In this section we assume that the other corner-restricted box does not cover point $B$. In this situation, regardless of how the second box is placed, a common non-avoidable structure can be created, provided that minor adjustments are performed.

To this end, we will define 10 points and 4 pairs of alternative points. Three points are placed at $(1, 1.74)$, $(2, 1.74)$, and $(1.6, 1)$, while one pair consists of the points $A$ and $B$ from above. The remaining points and pairs are obtained by mirroring along the lines $x = 2$ and $y = 2$.

After one point of each pair of alternatives is chosen, 14 points are placed so that non-avoidability lemmas apply to all but two of the bounded regions in Figure 3 (for readability, the various alternative choices are demonstrated in different corners). The two critical regions are $[1, 2] \times [1.74, 2.26]$ and $[2, 3] \times [1.74, 2.26]$.

Note that each corner-restricted box will contain one point of an alternative pair. From now on assume that, if possible, we will pick a point contained in a corner-restricted box whenever choosing from a pair of alternatives. Note that our assumptions on the placements of the corner-restricted boxes imply that every pair point contained in a corner-restricted box will end up in our configuration.

In addition to these points, each corner-restricted box will contain one of $(1, 1.74)$, $(1.6, 1)$, or their symmetric counterparts by Lemma 10.

> *[Figure 3: One square has its centre in one of the marked regions -- not extractable from PDF]*

Hence four of the 14 points are covered by two boxes. Of the remaining 11 boxes, at least one cannot contain a point and thus its centre is in one of the above regions. By symmetry, we may assume that the centre lies in $[1, 2] \times [1.74, 2.26]$ (asymmetries due to the placement of the corner-restricted boxes will not affect any of the following).

Consider a new configuration of 11 points and four pairs of alternative points. The pairs are the same as in the previous case. Six points are $(1.6, 1)$, $(2.26, 1)$, $(3, 1.6)$, $(1, 1.74)$, $(1.78, 1.74)$, $(2.26, 2)$, and the others are obtained by mirroring at the line $y = 2$. Non-avoidance lemmas apply to all the regions in Figure 4, regardless of which point of an alternative pair is chosen (note that once again in each corner just one alternative is displayed).

> *[Figure 4: One box covers both marked points -- not extractable from PDF]*

For each such choice, the resulting set consists of 15 points, and as before, the corner-restricted boxes contain two points each. In addition, the box that lies with its centre inside $[1, 2] \times [1.74, 2.26]$ contains the points $(1.78, 1.74)$ and $(1.78, 2.26)$ by Corollary 3. Hence six of the 15 points are contained in three boxes, and as the set is unavoidable, only nine more boxes can be packed inside $S$, for a maximum of twelve.

### 3.2 Adjacent corner-restricted boxes

In this section we assume that one box covers point $A$ and the other covers point $B$. We will refer to these boxes as $T_A$ and $T_B$, respectively. We will first show that due to their proximity, one box covers an extended area. The following Lemma follows analogously to Lemma 10.

**Lemma 11** In the situation of Lemma 10, assume that a box $T$ does cover point $A$, but does not cover $B$, $C$, or $D$, and, in addition, does not cover the point $(1, 1)$. Then the box contains the points $(1.82, 1)$ and $(1.96, 0.76)$.

Now of the two corner-restricted boxes $T_A$ and $T_B$, at most one of them covers the point $(1, 1)$, and hence Lemma 11 (or its symmetric version) applies to the other one. Without loss of generality, we may assume this to be the box $T_B$.

Unlike in the case of two non-adjacent corner-restricted boxes, different configurations need to be constructed for various subcases. However, there is a common set of points that can be included in all of them. Let

$$S_A = \{A, (1.13, 1), (1.4, 1), (1.74, 1), (1.87, 0.76)\},$$

$$S_B = \{B, (1, 1.13), (1, 1.82), (0.76, 1.96)\}$$

By Lemmas 10 and 11, the points in $S_A$, $S_B$ are covered by $T_A$ and $T_B$, respectively.

Consider the set

$$S_A \cup S_B \cup \{(2.5, 1), (3, 1)\} \cup (\{1, 2, 3\} \times \{1.82, 2.36, 3.09\})$$

(see Figure 5). Non-avoidance lemmas apply to all regions with the exception of the four rectangular ones bounded by the points in $\{1, 2, 3\} \times \{1.82, 2.36, 3.09\}$. We will refer to this regions as $R_1$, $R_2$, $R_3$, and $R_4$, numbered clockwise from the top left.

> *[Figure 5: Configuration with four critical regions -- not extractable from PDF]*

The above list contains only 10 points that are not already covered by $T_A$ or $T_B$ (note that $(1, 1.82)$ is listed twice) and hence in order to pack 13 boxes into $S$, there must be a box $T'$ not containing any point.

We will now go through the potential placements of $T'$ into the critical regions and will construct (occasionally after restricting to subcases) "small enough" unavoidable sets of points. Here "small enough" means that the number of points not known to be covered by already placed boxes and the number of those placed boxes is smaller than 13.

By Corollary 3 in the cases $b = 0.73$ ($R_1$, $R_2$) and $b = 0.54$ ($R_3$, $R_4$), $T'$ will contain the midpoints of the longer edges of its corresponding region. We will refer to these sets of midpoints as $S_1, \ldots, S_4$, respectively, and will include them in our non-avoidable sets.

#### 3.2.1 The centre of $T'$ lies in region $R_1$

Consider the following set of 18 points:

$$S_A \cup S_B \cup S_1 \cup \{(2.5, 1), (3, 1), (2, 1.82), (3, 1.82), (2.3, 2.5), (3, 2.5), (1, 3), (2.3, 3), (3, 3)\}$$

If we add an additional "sliding point" $Z$ on the line segment $\{1\} \times [2.36, 2.92]$, these points are non-avoidable regardless of the actual placement of $Z$ (see Figure 6; for $Z$ having a high $y$-value, this follows from Lemma 5 with $a \leq 0.96$, $b = 0.76$).

> *[Figure 6: Case $R_1$, including a "sliding" point -- not extractable from PDF]*

Now by Corollary 7, $T'$ has a left intersection of at least 0.09. Hence either $T'$ contains $(1, 3)$ or intersects $\{1\} \times [2.45, 2.91]$. In both cases (with an appropriately placed $Z$), there are nine points which are not covered by $T_A$, $T_B$, or $T'$, and the set is small enough.

#### 3.2.2 The centre of $T'$ lies in the region $R_2$

We will consider two subcases:

1. $T'$ covers $(2, 2.72)$

   The following is a small enough non-avoidable set (Figure 7):

   $$S_A \cup S_B \cup (S_2 \cup \{(2, 2.72)\}) \cup \{(2.5, 1), (3.1, 1), (2.5, 1.6), (1.6, 1.95), (3.1, 2), (1, 2.72), (1, 3), (1.8, 3)\}$$

> *[Figure 7: Case $R_2$ (1.) -- not extractable from PDF]*

2. $T'$ does not cover $(2, 2.72)$

   Then the left intersection of $T'$ is smaller than 0.37. By Lemma 7 the right intersection of $T'$ must be at least 0.45, which implies that $T'$ contains the point $(3, 2.64)$. A small enough unavoidable set is the given by (Figure 8)

   $$S_A \cup S_B \cup (S_2 \cup \{(3, 2.64)\}) \cup \{(2.5, 1), (3, 1), (2, 1.82), (3, 1.82), (1, 2.36), (1.5, 2.36), (1, 3), (1.8, 3), (3, 3)\}.$$

#### 3.2.3 The centre of $T'$ lies in the region $R_3$

Consider the unavoidable set (Figure 9)

$$S_A \cup S_B \cup (S_3 \cup \{(3, 2.10)\}) \cup \{(2.3, 1), (3.05, 1), (1.8, 1.8), (3, 1.86), (1, 2.14), (2, 2.14), (1, 3), (1.5, 3), (2.3, 3), (3.1, 3)\}$$

Note that as the right intersection of $T'$ is at least 0.28, $T'$ covers $(3, 2.10)$. In addition, either its left intersection exceeds 0.32 or its right intersection exceeds 0.50. Hence $T'$ also covers one of $(2, 2.14)$ or $(3, 1.86)$, and the set is small enough.

> *[Figure 8: Case $R_2$ (2.) -- not extractable from PDF]*

> *[Figure 9: Case $R_3$ -- not extractable from PDF]*

#### 3.2.4 The centre of $T'$ lies in region $R_4$

As in the previous case, we have that $T'$ covers $(1, 2.10)$ and $(2, 2.10)$. A small enough unavoidable set is given by (Figure 10)

$$S_A \cup S_B \cup (S_4 \cup \{(1, 2.10), (2, 2.10)\}) \cup \{(2.5, 1), (3.1, 1), (2.4, 1.6), (3.1, 2), (2.4, 2.5), (0.9, 3), (1.7, 3), (2.5, 3), (3.1, 3)\}.$$

By 3.1 and cases 3.2.1 to 3.2.4, Theorem 9 follows.

> *[Figure 10: Case $R_4$ -- not extractable from PDF]*

## Acknowledgment

The author would like to thank the anonymous referee for his helpful suggestions.

## References

[1] S. El Moumni, Optimal Packings of Unit Squares in a Square, *Studia Sci. Math. Hungar.* 35 (1999), no. 3-4, 281-290.

[2] P. Erdos and R. L. Graham, On Packing Squares with Equal Squares, *J. Combin. Theory Ser. A* 19 (1975) 119-123.

[3] E. Friedman, Packing unit squares in squares: A survey and new results, *The Electronic Journal of Combinatorics*, Dynamic Surveys (#DS7) (version of Aug 14, 2009)

[4] M. Gardner, "Mathematical Games", *Scientific American* (Oct 1979, Nov 1979, Mar 1980, Nov 1980).

[5] F. Gobel, Geometrical Packing and Covering Problems, in *Packing and Covering in Combinatorics*, A. Schrijver (ed.), Math Centrum Tracts 106 (1979) 179-199.

[6] M. Kearney and P. Shiu, Efficient Packing of Unit Squares in a Square, *Elect. J. Comb.* 9 #R14 (2002).

[7] H. Nagamochi, Packing Unit Squares in a Rectangle, *Elect. J. Comb.* 12 #R37 (2005).

[8] W. Stromquist, "Packing Unit Squares Inside Squares I, II, III", unpublished manuscripts, 1984-5; http://www.walterstromquist.com/publications.html.

[9] W. Stromquist, Packing 10 or 11 Unit Squares in a Square, *Elect. J. Comb.* 10 #R8 (2003).
