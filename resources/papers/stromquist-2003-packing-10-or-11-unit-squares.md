# Packing 10 or 11 Unit Squares in a Square

**Authors:** Walter Stromquist, Department of Mathematics, Bryn Mawr College, Bryn Mawr, Pennsylvania, USA (walters@chesco.com)
**Venue:** The Electronic Journal of Combinatorics 10 (2003), #R8
**Year:** 2003
**Source:** https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8
**Archived:** 2026-08-22
**Extraction:** pdfminer.six from the original PDF, cleaned for readability. Raw extraction preserved alongside as `stromquist-2003-packing-10-or-11-unit-squares.raw.md`.

---

## Abstract

Let $s(n)$ be the side of the smallest square into which it is possible to pack $n$ unit squares. We show that $s(10) = 3 + \sqrt{\frac{1}{2}} \approx 3.707$ and that $s(11) \geq 2 + 2\sqrt{\frac{4}{5}} \approx 3.789$. We also show that an optimal packing of 11 unit squares with orientations limited to $0^\circ$ or $45^\circ$ has side $2 + 2\sqrt{\frac{8}{9}} \approx 3.886$. These results prove Martin Gardner's conjecture that $n = 11$ is the first case in which an optimal result requires a non-$45^\circ$ packing.

---

Let $s(n)$ be the side of the smallest square into which it is possible to pack $n$ unit squares. It is known that $s(1) = 1$, $s(2) = s(3) = s(4) = 2$, $s(5) = 2 + \sqrt{\frac{1}{2}}$, and that $s(6) = s(7) = s(8) = s(9) = 3$. For larger $n$, proofs of exact values of $s(n)$ have been published only for $n = 14$, $15$, $24$, $35$, and when $n$ is a square. The first published proof that $s(6) = 3$ is by Kearney and Shiu [3] and the other results are reported in Erich Friedman's dynamic survey [1].

We prove here that $s(10) = 3 + \sqrt{\frac{1}{2}} \approx 3.707$ (Theorem 1) and that $s(11) \geq 2 + 2\sqrt{\frac{4}{5}} \approx 3.789$ (Theorem 2). The 10-square packings in Figure 1 are optimal. The most efficient known packing of 11 squares, shown in Figure 2 and due to Walter Trump, has side about 3.8772 and includes unit squares tilted at about $40.182^\circ$.

> *[Figure 1: Best packings of 10 squares, with $s = 3 + \sqrt{\frac{1}{2}} \approx 3.707$ -- not extractable from PDF]*

> *[Figure 2: Best known packing of 11 squares (tilt $\approx 40.182^\circ$), with $s \approx 3.8772$ -- not extractable from PDF]*

> *[Figure 3: Optimal $45^\circ$ packing for $n = 11$, with $s \approx 3.886$ -- not extractable from PDF]*

In the case of $n = 11$, we also show that any $45^\circ$ packing---that is, one in which the unit squares are tilted only at $0^\circ$ or $45^\circ$ with respect to the bounding square---must have side at least $2 + 2\sqrt{\frac{8}{9}} \approx 3.886$ (Theorem 3). This bound is realized by the packing by Hamalainen [2] in Figure 3. Together, these results establish the truth of Martin Gardner's conjecture in [7], that $n = 11$ is the first case in which non-$45^\circ$ packings are required.

These results were first reported in [4,5,6]. We take the approach that was used in those memoranda and also used in [1] for establishing lower bounds. For rhetorical reasons, we define a *box* to be the interior of any square of side strictly greater than 1. In order to establish a lower bound of the form $s(n) \geq a$, we prove the equivalent statement that $n$ nonoverlapping boxes cannot be packed inside a square with side exactly $a$. For the most part we treat boxes as if they were unit squares, and rely on the extra margin of size to convert equations into inequalities as needed.

## 1 Nonavoidance Lemmas

In this section we present six "nonavoidance lemmas." Each lemma provides that if the center of a box is in some region, then the box must have a nonempty intersection with certain parts of the region's boundary. Lemmas 1--4 are general in nature, while Lemmas 5 and 6 are needed specifically for the proofs of Theorems 1 and 2 respectively. The lemmas are illustrated in Figure 4.

The first three lemmas are the same as Lemmas 1--3 in [1].

**Lemma 1.** Let $a \leq 1$ and $b \leq 1$. Then any box whose center is in the rectangle $[0, a] \times [0, b]$ must intersect the $x$-axis, the $y$-axis, or the point $(a, b)$.

**Lemma 2.** Let $T$ be a triangle with sides of length at most 1. Then any box whose center is in the interior of $T$ must contain one of the vertices of $T$.

> *[Figure 4: The nonavoidance lemmas -- not extractable from PDF]*

**Lemma 3.** Let $a$ and $b$ satisfy $a \leq 1$, $b \leq 1$, and $a + 2b \leq 2\sqrt{2}$. Then any box whose center is in the rectangle $[0, a] \times [0, b]$ must intersect the $x$-axis, the point $(0, b)$, or the point $(a, b)$.

We use Lemma 3 mainly in the case of $a = 2\sqrt{2} - 2 \approx .828$, $b = 1$, as shown in Figure 4. The other extreme is $a = 1$, $b = \sqrt{2} - \frac{1}{2} \approx .914$.

We need some preparation for Lemma 4. When $2\sqrt{2} - 2 < a < 1$, define $f(a)$ by

$$f(a) = \frac{\cos\theta^*}{1 + \cos\theta^*} + \frac{1 - a\cos\theta^*}{\sin\theta^*} \tag{1}$$

where $\theta^*$ is the smallest positive value of $\theta$ that satisfies

$$2\cos^3\theta - (2a + 2)\cos^2\theta + (a^2 - 2a + 3)\cos\theta - (1 - a^2) = 0. \tag{2}$$

For values of $a$ in the domain of $f$ we always have $0 < \theta^* < 45^\circ$ and $0 < f(a) < 1$.

**Lemma 4.** Let $a$ and $b$ satisfy $2\sqrt{2} - 2 < a < 1$, $0 < b < 1$, $(a, b)$ within 1 of $(0, 1)$, and $b \leq f(a)$. Then any box whose center is in the quadrilateral with vertices $(0, 0)$, $(0, 1)$, $(a, 0)$, and $(a, b)$ must intersect the $x$-axis, the point $(0, 1)$, or the point $(a, b)$.

We rely on these cases of Lemma 4:

| $a$: | $\frac{1}{2} + \sqrt{\frac{1}{8}} \approx .853$ | $\sqrt{\frac{4}{5}} \approx .894$ | $.96$ |
|------|:---:|:---:|:---:|
| $f(a)$: | $.972$ | $.926$ | $.769$ |
| $\theta^*$: | $39.5^\circ$ | $24.1^\circ$ | $17.7^\circ$ |

> *[Figure 5: Proof of Lemma 4 -- not extractable from PDF]*

*Proof.* If a box avoids both the $x$-axis and the point $(0, 1)$, then its edge might as well touch both as shown in Figure 5. Let $(a, b^*)$ be the point at which the box's top edge meets the line $x = a$. The two triangles marked $*$ are congruent. Since $z + z/\cos\theta = 1$, we have $z = \frac{\cos\theta}{1 + \cos\theta}$ and

$$b^* = \frac{\cos\theta}{1 + \cos\theta} + \frac{1 - a\cos\theta}{\sin\theta}. \tag{3}$$

If we fix $a$ in the range $2\sqrt{2} - 2 < a < 1$ and limit $\theta$ to the first quadrant, then the right side of (3) has a unique minimum, which occurs when $\theta < 45^\circ$ and $b^* < 1$. (To verify this, note that $b^*$ is large when $\theta \approx 0$, below 1 when $\theta = 45^\circ$, and decreasing to 1 when $\theta = 90^\circ$, and that the derivative doesn't have enough roots for there to be multiple minima below $45^\circ$.) Setting $db^*/d\theta = 0$, leads to equation (2) above. Therefore $f(a)$ is the minimum value of $b^*$.

If $(a, b)$ is within 1 of $(0, 1)$ but below $(a, f(a))$---and hence below $(a, b^*)$ whatever the value of $\theta$---then $(a, b)$ is clearly inside the box. $\square$

**Lemma 5.** Let $P$ be the pentagon with vertices $(1, 0)$, $(1, 1)$, $(2, 1)$, $(2.12, .9)$, and $(2.12, 0)$. Then any box whose center is in the interior of $P$ must intersect the $x$-axis, the segment from $(1, 0.788)$ to $(1, 1)$, or the segment from $(2, 1)$ to $(2.12, .90)$.

*Proof.* By Lemma 1, any counterexample must include a point to the left of $x = 1$ and a point to the right of $x = 2$. Without loss of generality, the box's boundary touches the $x$-axis and includes the point $(1, .788)$ as shown in Figure 6. Let $\theta$ be the angle of the box with the $x$-axis, as shown.

> *[Figure 6: Proof of Lemma 5 -- not extractable from PDF]*

If $\theta \leq \tan^{-1}(1.2) \approx 50.2^\circ$, then the box must contain the point $(2, 1)$. To see this, we calculate the $x$-coordinate of the point $(x, 1)$ at which the box's upper-right boundary crosses the line $y = 1$:

$$x = 1 + \frac{.212}{\tan\theta} + \frac{\sin\theta + \cos\theta - 1}{\sin\theta\cos\theta}. \tag{4}$$

The last term is the length of the box's intersection with the line $y = 1$, and it exceeds $.828$ for any first-quadrant value of $\theta$, so when $\tan\theta \leq 1.2$ we have

$$x > 1 + \frac{.212}{1.2} + .828 > 2.004,$$

forcing the point $(2, 1)$ to be inside the box.

If $\tan^{-1}(1.2) < \theta \leq \sin^{-1}(.9) \approx 64.2^\circ$, then the box contains the point $(2.12, .9)$. To see this, we compute the $x$-coordinate of the point at which the box's upper-right boundary intersects the line $y = .9$. We obtain

$$x = 1 + \frac{.112}{\tan\theta} + \frac{\sin\theta + \cos\theta - .9}{\sin\theta\cos\theta}. \tag{5}$$

This function reaches its minimum at $\theta \approx 52.6^\circ$, when $x = 2.1256$, so the box's right boundary always passes to the right of $(2.12, .9)$.

If $\sin^{-1}(.9) < \theta$ we need to calculate the coordinates $(x, y)$ of the box's rightmost vertex:

$$x = 1 + \frac{1}{\sin\theta} + \cos\theta - \frac{.788}{\tan\theta}$$

$$y = \sin\theta.$$

Since $.9 < y < 1$, the vertex is to the right of the critical segment if $(x - 2)/(1 - y) > 1.2$. Some calculation shows that

$$\frac{x - 2}{1 - y} = \frac{1 - \cos\theta}{\sin\theta} + \frac{.212(1 + \sin\theta)}{\sin\theta\cos\theta}.$$

When $\sin\theta > .9$ the first term on the right is at least $.6$ and the second term is at least $1$, so the lemma is proved. $\square$

**Lemma 6.** Let $a = \sqrt{\frac{4}{5}} \approx .894$. Then any box whose center is in the pentagon with vertices at $(1, 0)$, $(1, 1)$, $(1 + \frac{1}{2}a, 1.12)$, $(1 + a, 1)$, and $(1 + a, 0)$ must intersect the $x$-axis or one of the vertices.

*Proof.* We may assume that any counterexample involves a box touching the $x$-axis as in Figure 7. If $D(\theta)$ is the length of the intersection of the box with the line $y = 1$, then

$$D(\theta) = \frac{1}{\sin\theta} + \frac{1}{\cos\theta} - \frac{1}{\sin\theta\cos\theta} = \frac{\sin\theta + \cos\theta - 1}{\sin\theta\cos\theta}.$$

> *[Figure 7: Proof of Lemma 6 -- not extractable from PDF]*

Let $\theta_0 = \frac{1}{2}\sin^{-1}(5 - 2\sqrt{5}) \approx 15.9^\circ$; then $D(\theta_0) = a$. If $\theta < \theta_0$ or $\theta > \frac{\pi}{2} - \theta_0$ then $D(\theta) > a$ and the box must intersect $(1, 1)$ or $(1 + a, 1)$. We can therefore assume that $\theta_0 \leq \theta \leq \frac{\pi}{2} - \theta_0$. In this case $\cos\theta + \sin\theta > 1.12$, so the box includes a point above $y = 1.12$. We may assume that the box touches the point $(1 + a, 1)$ and has its apex to the right of the line $x = 1 + \frac{1}{2}a$, as shown in the figure. Now the $y$-coordinate at which the top of the box intersects the line $x = 1 + \frac{1}{2}a$ is given by

$$1 + \left(D(\theta) - \sqrt{\frac{1}{5}}\right)\tan\theta,$$

which by direct computation is equal to $1.1277\ldots$ when $\theta = \theta_0$, and increases with $\theta$. Therefore the box intersects the line above the point $(1 + \frac{1}{2}a, 1.12)$, and must include that point. $\square$

## 2 Ten Squares

**Theorem 1.** Ten pairwise nonintersecting boxes cannot exist in the interior of a square of side $s = 3 + \sqrt{\frac{1}{2}}$.

*Proof.* In this section, fix $s = 3 + \sqrt{\frac{1}{2}}$ and let $S$ be the square $[0, s]^2$. Define ten points $A, B, \ldots, J$ as shown in Figure 8. We set $A = (1, 1)$, $B = (.97, \frac{s}{2})$, and place the other points symmetrically in $S$. Each of the regions outlined in the figure is covered by one of Lemmas 1, 2, or 4 (with $a \approx .853$, $b = .97$). It follows that these ten points are unavoidable in the sense of [1], meaning that any box inside $S$ must contain one of the points. If ten boxes are packed in $S$, each must contain exactly one of them. We name the boxes for the points they contain---A-box, B-box, etc.

> *[Figure 8: Each box contains one of these ten points -- not extractable from PDF]*

The key to the proof is to show that the H-box also contains some point on the short segment from $(2, 1)$ to $(2.12, .9)$. We will prove this fact and then show why it matters.

1. The points remain unavoidable if $B$ is replaced by $B' = (.75, s - 1.96)$. Therefore, the point $B'$ is contained in the B-box. (We now use Lemma 4 with $a = .96$, $b = .75$.)

> *[Figure 9: A-box contains one of $A'$, $A''$ -- not extractable from PDF]*

> *[Figure 10: If A-box contains $A''$, then H-box contains $H' = (2, 1)$ -- not extractable from PDF]*

2. If, now, $A$ is replaced by the two points $A' = (1, s - 2.92)$ and $A'' = (1.2, 1)$, the points remain unavoidable (Figure 9). It follows that the A-box must contain at least one of the points $A'$, $A''$. Note that $s - 2.92 < .788$.

3. If the A-box contains $A'' = (1.2, 1)$, then the points $A$, $A''$, $B'$, $C$ through $G$, $I$, $J$, and $(2, 1)$ form an unavoidable set (Figure 10). All of these are denied to the H-box except for $(2, 1)$, so the H-box contains $(2, 1)$. (This step uses Lemma 3.)

4. If the A-box contains $A' = (1, s - 2.92)$, then the entire segment from $A'$ to $A$ (which includes the segment from $(1, .788)$ to $(1, 1)$) is denied to the H-box, as are points $B$ through $G$, $I$, and $J$. Figure 11 shows a partition of $S$ in which Lemma 5 applies to one of the regions. From this figure, we see that the H-box must touch the segment from $(2, 1)$ to $(2.12, .9)$.

> *[Figure 11: H-box must touch segment -- not extractable from PDF]*

> *[Figure 12: No room for I-box and J-box -- not extractable from PDF]*

In either case, the H-box must contain some point on the indicated segment. In Figure 12 the point of intersection is marked with an asterisk. Seven other asterisks mark other points which must be contained in the B-, D-, F-, and H-boxes by symmetrical arguments. We do not know the locations of these points exactly, but we can tell that each asterisk is within 1 of the center of the square and within 1 of each of the two asterisks nearest to it. Each of the heavy line segments connects two asterisks that must be in the same box.

Now, the thirteen points in Figure 12---the eight asterisks, the points $A$, $C$, $E$, $G$, and the center of the square---clearly form an unavoidable set. All but the center are denied to the I- and J-boxes, and those two boxes cannot both contain the center. This shows that the 10-box packing is impossible. $\square$

## 3 Eleven Squares

> *[Figure 13: Ten points to avoid and how to avoid them -- not extractable from PDF]*

> *[Figure 14: Twelve points for Theorem 2 -- not extractable from PDF]*

**Theorem 2.** Let $s = 2 + 2\sqrt{\frac{4}{5}} \approx 3.789$. Then eleven non-intersecting boxes cannot exist inside a square of side $s$.

*Proof.* For this proof, fix $s = 2 + 2\sqrt{\frac{4}{5}}$ and let $S = [0, s]^2$. Consider the ten points in Figure 13. Four of these points have coordinates $(1, 1)$, $\left(\frac{s}{2}, \frac{s}{2}\right)$, $\left(1, \frac{s}{2}\right)$, $\left(\frac{3}{2}, 1\right)$, and the rest are placed symmetrically. The vertical distance between the rows of points is $\frac{s}{2} - 1 = \sqrt{\frac{4}{5}} \approx .894$. The triangles in the figure are all congruent, and the sloping sides have length 1.

Nonavoidance lemmas apply to all of the regions shown except for the rectangles at the top and bottom. If 11 boxes are to be packed into the square, at least one of them must be placed in one of those rectangles, roughly as shown in the figure (up to symmetry). From Lemmas 4 and 6 we can see that this box must contain all three of the points marked "A" in Figure 14:

$$A = \begin{cases} (1, .9) \\ \left(\frac{s}{2}, .9\right) \approx (1.894, .9) \\ \left(1 + \sqrt{\frac{1}{5}}, 1.12\right) \approx (1.447, 1.12) \end{cases}$$

There are nine other points in Figure 14:

$$B = (s - 1, 1) \approx (2.789, 1)$$
$$C = \left(s - .9, \frac{s}{2}\right) \approx (2.889, 1.894)$$
$$D = (s - 1, s - 1) \approx (2.789, 2.789)$$
$$E = \left(\frac{s}{2}, s - .9\right) \approx (1.894, 2.889)$$
$$F = (1, s - 1) \approx (1, 2.789)$$
$$G = (.8, 1.85)$$
$$H = (1.5, 2.1)$$
$$I = (2.1, 2.1)$$
$$J = (2.1, 1.5)$$

Nonavoidance lemmas apply to all of the regions in this figure. Since three of the twelve points are in one box, there cannot be eleven nonintersecting boxes. This completes the proof of Theorem 2. $\square$

The argument in Figure 14 is not rigid; any point in the figure could be moved by a small amount in almost any direction without causing the argument to fail. The critical distances are all in Figure 13.

### 45-degree packings

We now apply the same technique to the case of $45^\circ$ packings. By considering only boxes that are oriented at $0^\circ$ or $45^\circ$ to the axes ("$0^\circ$ and $45^\circ$ boxes") we can prove stronger forms of some of our lemmas. In particular:

**Lemma 7.** Let $T$ be a triangle, and suppose that the component of any side of $T$ in the direction of any unit vector making an angle of $0^\circ$ or $45^\circ$ with either axis is at most 1. Then any $0^\circ$ or $45^\circ$ box whose center is in the interior of $T$ must contain one of the vertices of $T$.

**Lemma 8.** If $(a, b) = (1, .8)$ or $(a, b) = \left(\frac{2}{3}\sqrt{2}, 2\sqrt{2} - 2\right)$, then any $0^\circ$ or $45^\circ$ box whose center is in the quadrilateral with vertices $(0, 0)$, $(0, 1)$, $(a, 0)$, and $(a, b)$ must intersect the $x$-axis, the point $(0, 1)$, or the point $(a, b)$.

The proofs are easier than in the general case and are omitted. With these more powerful lemmas, we can justify a larger value of $s$ in the following theorem, which is enough to settle Martin Gardner's conjecture.

**Theorem 3.** Let $s = 2 + \frac{4}{3}\sqrt{2} \approx 3.886$. Then eleven non-intersecting boxes cannot exist inside a square of side $s$, if each box has orientation $0^\circ$ or $45^\circ$ with respect to the square.

*Proof.* Now fix $s = 2 + \frac{4}{3}\sqrt{2}$ and let $S = [0, s]^2$. Consider ten points defined exactly as in Figure 13---four of these points have coordinates $(1, 1)$, $\left(\frac{s}{2}, \frac{s}{2}\right)$, $\left(1, \frac{s}{2}\right)$, $\left(\frac{3}{2}, 1\right)$---but with the new value of $s$. If eleven boxes are to be packed into the square, one of them will have to avoid the marked points. This is impossible for a box with $0^\circ$ orientation.

The interior sloping lines now have length $\sqrt{\frac{10}{9}}$, but their components in the direction of a $45^\circ$ unit vector are at most 1, so Lemma 7 applies to the triangles in the figure. It follows that a $45^\circ$ box that avoids the points must be (up to symmetry) in approximately the position shown in Figure 13. This box must contain three points like those marked "A" in Figure 14, but now they have these coordinates:

$$A = \begin{cases} (1, s - 3) \approx (1, .886) \\ \left(\frac{s}{2}, s - 3\right) \approx (1.943, .886) \\ (1.5, 1.3) \end{cases}$$

The other nine points in Figure 14 become

$$B = (s - 1, 1) \approx (2.886, 1)$$
$$C = \left(s - .8, \frac{s}{2}\right) \approx (3.086, 1.943)$$
$$D = (s - 1, s - 1) \approx (2.886, 2.886)$$
$$E = \left(\frac{s}{2}, s - .8\right) \approx (1.943, 3.086)$$
$$F = (1, s - 1) \approx (1, 2.886)$$
$$G = (.8, s - 2) \approx (.8, 1.886)$$
$$H = (1.7, 2.2)$$
$$I = (2.2, 2.2)$$
$$J = (2.2, 1.7).$$

Again these 12 points form an unavoidable set in the context of $45^\circ$ packings, and since three of them are in one box, there cannot be 11 nonintersecting boxes. This completes the proof of Theorem 3 and establishes the truth of Martin Gardner's conjecture. $\square$

## References

1. Erich Friedman, "Packing Unit Squares in Squares: A Survey and New Results," *The Electronic Journal of Combinatorics* 7 (2002), Dynamic Survey DS#7.

2. Pertti Hamalainen, correspondence, April 20, 1980.

3. Michael J. Kearney and Peter Shiu, "Efficient packing of unit squares in a square," *The Electronic Journal of Combinatorics* 9 (2002), #R14.

4. Walter Stromquist, "Packing unit squares inside squares, I (six unit squares)," Daniel H. Wagner, Associates Memorandum, September 11, 1984.

5. ------, "Packing unit squares inside squares, II (ten unit squares)," DHWA Memorandum, October 15, 1984.

6. ------, "Packing unit squares inside squares, III (Cases with $n \leq 65$ and Martin Gardner's conjecture for $n = 11$)," DHWA Memorandum, November 15, 1984.

7. Martin Gardner, "Mathematical Games" in *Scientific American*, October 1979. (See also November 1979, March 1980, and November 1980.)
