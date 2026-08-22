# Packing Unit Squares in Squares: A Survey and New Results

**Authors:** Erich Friedman, Stetson University, DeLand, FL 32723 (efriedma@stetson.edu)
**Venue:** The Electronic Journal of Combinatorics (2009), Dynamic Survey DS7
**Year:** 2009 (revision)
**Source:** https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS7
**Archived:** 2026-08-22
**Extraction:** pdfminer.six from the original PDF, cleaned for readability. Raw extraction preserved alongside as `friedman-ds7-packing-unit-squares-in-squares.raw.md`.

---

> ⚠️ **Contains reconstructed passages.**
> This transcription contains **3** annotated passage(s) where the PDF extraction was
> damaged and text or mathematics was reconstructed or marked unrecoverable. Search this
> file for `GARBLED` and `NOTE` to find them.
> **Any formula near an annotation must be checked against `friedman-ds7-packing-unit-squares-in-squares.raw.md`**, which is the
> unedited extraction and the ground truth for this document.

## Abstract

Let $s(n)$ be the side of the smallest square into which we can pack $n$ unit squares. We present a history of this problem, and give the best known upper and lower bounds for $s(n)$ for $n \leq 100$, including the best known packings. We also give relatively simple proofs for the values of $s(n)$ when $n = 2, 3, 5, 8, 15, 24$, and $35$, and more complicated proofs for $n = 7$ and $14$. We also prove many other lower bounds for various $s(n)$.

## Table of Contents

1. Introduction
2. Previous Results
3. New Packings
4. Technical Lemmas
5. Lower Bounds

Appendix

References

## 1 Introduction

The problem of packing equal circles in a square has been around for some 40 years and has seen much recent progress [2]. The problem of packing equal squares in a square is only recently becoming well known. Results were less plentiful, as the computer-aided methods available for circles did not generalize for squares, until recently when an effective algorithm was found [20]. We give a few packings which improve upon those in the literature, illustrate a technique for obtaining lower bounds, and exhibit the best known packings for less than one hundred squares.

Let $s(n)$ be the side of the smallest square into which we can pack $n$ unit squares. It is clear that $\sqrt{n} \leq s(n) \leq \lceil\sqrt{n}\rceil$, the first inequality coming from area considerations, and the second coming from the facts that $s(n)$ is non-decreasing and $s(n^2) = n$. It is not hard to show that $s(2) = s(3) = 2$. It is a little harder to show that $s(5) = 2 + 1/\sqrt{2}$ [7].

The number of claims far outweighs the number of published results in this area. Gobel says that Schrijver claims that Bajmoczy proved $s(7) = s(8) = 3$ [7]. Walter Stromquist claimed to have proved $s(6) = 3$ and $s(10) = 3 + 1/\sqrt{2}$, and claimed to know how to prove $s(14) = s(15) = 4$ and $s(24) = 5$ [13]. Trevor Green sent me a proof for $s(6) = 3$. None of these proofs were published. Said El Moumni evidently proved $s(7) = s(8) = 3$ and $s(15) = 4$ [12] but no one was aware of this until recently. Finally, in 2002, Kearney and Shiu published a proof of $s(6) = 3$ [9].

In 2003, Stromquist proved $s(10) = 3 + 1/\sqrt{2}$ [18]. In 2005, Nagamochi proved that $s(n^2 - 2) = s(n^2 - 1) = n$ [19]. Also in 2005, Thierry Gensane and Philippe Ryckelynck published an inflation algorithm for finding good packings and found the first computer packing that might be optimal. [20]. There are many other good packings thought to be optimal, but as of yet no proofs. Here we prove the values of $s(n)$ for square $n$ and $n = 2, 3, 5, 7, 8, 14, 15, 24$, and $35$.

Previous results can be found in Section 2. Recent packings appear in Section 3. In Section 4 we prove some technical lemmas that we use in Section 5 to prove the values of $s(n)$ mentioned above. Lists of the best known upper and lower bounds for $s(n)$ are given in the Appendix. Many of the results given are taken from unpublished letters and manuscripts, and private communications.

## 2 Previous Results

Gobel was the first to publish on the subject [7]. He found that $a^2 + a + 3 + \lfloor(a-1)\sqrt{2}\rfloor$ squares can be packed in a square of side $a + 1 + 1/\sqrt{2}$ by placing a diagonal strip of squares at a $45^\circ$ angle. This gives the best known packings for all values of $a$ except for $a = 3$ and $a = 6$ (see Figure 1).

> *[Figure 1: Gobel's diagonal strip packings for $s(5) = 2 + 1/\sqrt{2}$, $s(10) = 3 + 1/\sqrt{2}$, $s(27) \leq 5 + 1/\sqrt{2}$, $s(38) \leq 6 + 1/\sqrt{2}$, $s(52) \leq 7 + 1/\sqrt{2}$, $s(67) \leq 8 + 1/\sqrt{2}$, $s(84) \leq 9 + 1/\sqrt{2}$ -- not extractable from PDF]*

By unrotating some rotated squares in the corner, we get some alternate packings for $n = 10$, $67$, and $84$. (see Figure 2). David Cantell noticed in 2005 that alternative packings exist for $n = 27$, $38$, $52$, and $84$ using a minimum number of rotated squares (see Figure 2) [17].

> *[Figure 2: Alternative packings for $s(10) = 3 + 1/\sqrt{2}$, $s(67) \leq 8 + 1/\sqrt{2}$, $s(84) \leq 9 + 1/\sqrt{2}$, $s(27) \leq 5 + 1/\sqrt{2}$, $s(38) \leq 6 + 1/\sqrt{2}$, $s(52) \leq 7 + 1/\sqrt{2}$, $s(84) \leq 9 + 1/\sqrt{2}$ -- not extractable from PDF]*

It is clear that $n + 2\lfloor s(n) \rfloor + 1$ squares can be packed in a square of side $s(n) + 1$ by packing $n$ squares inside a square of side $s(n)$ and putting the other squares in an "L" around it. The first four packings in Figure 2 are of this form. Packings not containing an "L" of squares we will call primitive packings. From now on, we will only illustrate primitive packings.

Gobel also found that if integers $a$ and $b$ satisfied $a - 1 < b/\sqrt{2} < a + 1$, then $2a^2 + 2a + b^2$ squares can be packed inside a square of side $a + 1 + b/\sqrt{2}$. This is accomplished by placing a $b \times b$ square of squares at a $45^\circ$ angle in the center. This gives the best known packings for $28$, $40$, $65$, and $89$ squares (see Figure 3). Adding an "L" around the packing of 65 squares gives the best known packing of 82 squares. The packing for $n = 40$ is rigid.

> *[Figure 3: Centered diagonal block packings for $s(28) \leq 3 + 2\sqrt{2}$, $s(40) \leq 4 + 2\sqrt{2}$, $s(65) \leq 5 + 5/\sqrt{2}$, $s(89) \leq 5 + 7/\sqrt{2}$ -- not extractable from PDF]*

Charles Cottingham, who improved some of Gobel's packings for $n \leq 49$, was the first to use diagonal strips of width 2 [6]. Soon after he produced a packing of 19 squares with a diagonal strip of width 2, Robert Wainwright improved Cottingham's packing slightly (see Figure 4) [4]. In 2002, David Cantrell found some alternative packings for 19 squares [14].

> *[Figure 4: Packing for $s(19) \leq 3 + 4\sqrt{2}/3$ -- not extractable from PDF]*

In 1980, Evert Stenlund improved many of Cottingham's packings, and provided packings for $n \leq 100$ [6]. His packing of 66 squares uses a diagonal strip of width 3 (see Figure 5). In this packing, the diagonal squares touch only the squares in the upper right and lower left corners. Adding an "L" to this packing gives the best known packing of 83 squares.

> *[Figure 5: Packing for $s(66) \leq 3 + 4\sqrt{2}$ -- not extractable from PDF]*

The best known packings for many values of $n$ are more complicated. Many seem to require packing with squares at angles other than $0^\circ$ and $45^\circ$. In 1979, Walter Trump improved Gobel's packing of 11 squares (see Figure 6). Many people have independently discovered this packing. The original discovery has been incorrectly attributed to Gustafson and Thule [11]. The middle squares are tilted about $40.182^\circ$, and there is a small gap between these squares. This packing is also rigid.

> *[Figure 6: Packing for $s(11) < 3.8771$ -- not extractable from PDF]*

In 1980, Hamalainen improved on Gobel's packing of 18 squares (see Figure 7) [6]. In 1981, Mats Gustafson found an alternative optimal packing of 18 squares (see Figure 7). The middle squares in these packings are tilted by an angle of $\arcsin((\sqrt{7} - 1)/4) \approx 24.295^\circ$. In 2002, David Cantrell found another alternative packing (see Figure 7) [14] that is useful in building the best known packing for $n = 68$ (see Figure 11). In 2004, the computer program of Gensane and Ryckelynck found yet another alternative packing (see Figure 7) [20].

> *[Figure 7: Four alternative packings for $s(18) \leq (7 + \sqrt{7})/2$ -- not extractable from PDF]*

In [3], Erdos and Graham define $W(s) = s^2 - \max\{n : s(n) \leq s\}$. Thus $W(s)$ is the wasted area in the optimal packing of unit squares into an $s \times s$ square. They show (by constructing explicit packings) that $W(s) = O(s^{7/11})$. In [10], it is mentioned that Montgomery has improved this result to $W(s) = O(s^{(3-\sqrt{3})/2 + \varepsilon})$ for every $\varepsilon > 0$.

In [10], Roth and Vaughan establish a non-trivial lower bound for $W(s)$. They show that if <!-- GARBLED: floor function notation lost in extraction; likely $s(s - \lfloor s \rfloor) > 1/6$ --> then <!-- GARBLED: floor function notation lost in extraction; likely $W(s) \geq 10^{-100}\sqrt{s \lvert \lfloor s \rfloor - s + 1/2 \rvert}$ or similar -->. This implies that $W(s)$ is not $O(s^\alpha)$ when $\alpha < 1/2$.

It was conjectured that $s(n^2 - n) = n$ whenever $n$ is small. The smallest known counterexample of this conjecture, due to Lars Cleemann, is $s(17^2 - 17) < 17$. That is, 272 squares can be packed into a square of side 17 in such a way that the square can be squeezed together slightly (see Figure 8). Three squares are tilted by an angle of $45^\circ$, and the other tilted squares are tilted by an angle of $\arctan(8/15)$.

> *[Figure 8: Packing showing $s(272) < 17$ -- not extractable from PDF]*

## 3 New Packings

We can generalize the packings in Figure 3 by placing the central square a little off center. We can pack $2a^2 + 2a + b^2$ squares in a rectangle with sides $a + 1/2 + b/\sqrt{2}$ and $a + 3/2 + b/\sqrt{2}$. Adding a column of squares to the side of this, we get a packing of $2a^2 + 4a + b^2 + 1$ squares in a square of side $a + 3/2 + b/\sqrt{2}$. This gives the best known packings for 26 and 85 squares (see Figure 9).

> *[Figure 9: Packings for $s(26) \leq (7 + 3\sqrt{2})/2$, $s(85) \leq 11/2 + 3\sqrt{2}$ -- not extractable from PDF]*

Note that a diagonal strip of width 2 or 3 must be off center in order to be optimal. Otherwise one could place at least as many squares by not rotating them.

Stenlund also modified a diagonal strip of width 4 to pack 87 squares. In 2002, David Cantrell changed the angles slightly to give a minutely better packing (see Figure 10) [14]. There is a thin space between two of the diagonal strips. Compare this with the packing of 19 squares in Figure 4.

> *[Figure 10: Packing for $s(87) < 9.8520$ -- not extractable from PDF]*

In 2002, David Cantrell found packings of 53 and 68 squares that are slightly better than Gobel's (see Figure 11) [14].

> *[Figure 11: Packings for $s(53) < 7.8231$, $s(68) \leq 15/2 + \sqrt{7}/2$ -- not extractable from PDF]*

In 1980, Pertti Hamalainen improved Gobel's packing of 17 squares using a different arrangement of squares at a $45^\circ$ angle. But in 1998, John Bidwell, an undergraduate student at the University of Hawaii, improved this packing (see Figure 12) [1]. It is the smallest example where the best known packing contains squares at three different angles.

Also in 1998, I improved the best known packing of 29 squares using a modified diagonal strip of width 2. A few months later, Bidwell improved my packing slightly [1]. In 2005, David Cantrell used a completely different idea to find a better packing [17]. But in 2004, the computer program of Thierry Gensane and Philippe Ryckelynck found what now stands as the best known packing for 29 squares (see Figure 12) [20]. This packing contains squares at no less than 6 different angles.

> *[Figure 12: Packings for $s(17) < 4.6756$, $s(29) < 5.9344$ -- not extractable from PDF]*

In 1997, I generalized Stenlund's packing of 41 squares in Figure 4 to give packings of 70 and 88 squares using strips of width 2. In 2002, David Cantrell modified these packings to give the best known packings (see Figure 13) [14].

> *[Figure 13: Packings for $s(70) < 8.9121$, $s(88) < 9.9018$ -- not extractable from PDF]*

In 1997, I modified a diagonal strip of 2 squares to get a packing of 54 squares based on Wainwright's packing of 19 squares in Figure 4. In 2002, David Cantrell used his alternative packings of 19 squares to improve the packing for 54 squares [14]. He further improved this packing in 2005 (see Figure 14) [17].

In 1997, I modified a diagonal strip of 4 squares to get a packing of 69 squares. In 2002, David Cantrell improved this to produce the best known packing of 69 squares (see Figure 14) [14].

> *[Figure 14: Packings for $s(54) < 7.8488$, $s(69) < 8.8562$ -- not extractable from PDF]*

In 2002, David Cantrell used a completely new idea to find the best known packing of 39 squares (see Figure 15) [14].

We can generalize the packings in Figure 7 to provide the best known packings of 86 squares (see Figure 15). The angle of the tilted squares is the same as in that Figure.

> *[Figure 15: Packings for $s(39) < 6.8189$, $s(86) \leq (17 + \sqrt{7})/2$ -- not extractable from PDF]*

In 1997, I improved the packing for 37 squares using a modified diagonal strip of width 3. In 2002, David Cantrell improved this slightly (see Figure 16) [14]. The slanted squares are tilted at angles of approximately $42.086^\circ$ and $45^\circ$. Adding an "L" to this packing of 37 squares gives the best known packing of 50 squares.

In 1979, Charles Cottingham found a packing of 41 squares that was only improved in 2005 by David Cantrell (see Figure 16). [17]

In 2002, David Cantrell found the first packing of 55 squares in a square of side less than 8 [14]. He then improved this packing in 2005. (see Figure 16) [17].

Also in 2005, David Cantrell found the first packing of 71 squares in a square of side less than 9. (see Figure 16) [17].

In 2009, Karoly Hajba found the first known packing of 51 squares in a square of side less than $7 + 1/\sqrt{2}$. (see Figure 16) [16].

> *[Figure 16: Packings for $s(37) < 6.5987$, $s(41) < 6.9473$, $s(55) < 7.9871$, $s(71) < 8.9633$, $s(51) < 7.7044$ -- not extractable from PDF]*

Finally, we make the following conjecture:

**Conjecture 1.** If $s(n^2 - k) = n$, then $s((n+1)^2 - k) = n + 1$.

That is, if omitting $k$ squares from an $n \times n$ square does not admit a smaller packing, then the same will be true for omitting $k$ squares from any larger perfect square packing. This is true of all the best known packings.

## 4 Technical Lemmas

**Lemma 1.** Any unit square inside the first quadrant whose center is in $[0,1]^2$ contains the point $(1,1)$.

*Proof:* It suffices to show that a unit square in the first quadrant that touches the $x$-axis and $y$-axis contains the point $(1,1)$. If the square is at an angle $\theta$, it contains the points $(\sin\theta, 0)$ and $(0, \cos\theta)$ (see Figure 17). The two other corners of the square, $(\cos\theta, \cos\theta + \sin\theta)$ and $(\cos\theta + \sin\theta, \sin\theta)$, lie on the line $y - \sin\theta = -\cot\theta\,(x - \sin\theta - \cos\theta)$. In particular, when $x = 1$,

$$y = \frac{\sin^2\theta - \cos\theta\,(1 - \sin\theta - \cos\theta)}{\sin\theta} = \frac{(1 - \sin\theta)(1 - \cos\theta) + \sin\theta}{\sin\theta} \geq 1. \qquad\square$$

> *[Figure 17 -- not extractable from PDF]*

**Lemma 2.** Let $0 < x \leq 1$, $0 < y \leq 1$, and $x + 2y < 2\sqrt{2}$. Then any unit square inside the first quadrant whose center is contained in $[1, 1+x] \times [0, y]$ contains either the point $(1, y)$ or the point $(1+x, y)$.

*Proof:* It suffices to show that a unit square $u$ whose center is contained in $[1, 1+x] \times [0, y]$ that contains the points $(1, y)$ and $(1+x, y)$ on its boundary contains a point on the $x$-axis. This is true if $(1, y)$ and $(1+x, y)$ lie on the same side of $u$. If $u$ is at an angle $\theta$, then the lowest corner of the square is

$$(1 + x + (1 - x\sin\theta)\sin\theta - \cos\theta,\; y - (1 - x\sin\theta)\cos\theta - \sin\theta)$$

(see Figure 18). This point lies outside the first quadrant when $f(\theta) = \cos\theta + \sin\theta - x\sin\theta\cos\theta > y$. Since the critical points of $f(\theta)$ are

$$f'(\theta) = (\cos\theta - \sin\theta)[1 - x(\cos\theta + \sin\theta)],$$

$$(\cos\theta, \sin\theta) = (1/\sqrt{2}, 1/\sqrt{2}) \quad\text{and}\quad (\cos\theta, \sin\theta) = \left(\frac{1 \pm \sqrt{2x^2 - 1}}{2x},\; \frac{1 \mp \sqrt{2x^2 - 1}}{2x}\right).$$

Checking these 3 values and the endpoints, the global minimum of $f(\theta)$ occurs at $\theta = 45^\circ$. Therefore, when $y < \sqrt{2} - x/2$, $u$ contains some point of the $x$-axis. $\square$

> *[Figure 18 -- not extractable from PDF]*

**Lemma 3.** If the center of a unit square $u$ is contained in $\triangle ABC$, and each side of the triangle has length no more than 1, then $u$ contains $A$, $B$, or $C$.

*Proof:* The diagonals of $u$ divide the plane into 4 regions, labeled clockwise as $R_1$, $R_2$, $R_3$, and $R_4$ (see Figure 19). These regions are closed, and intersect only on the diagonals. The points $A$, $B$, and $C$ cannot all be on one side of either one of these diagonals, for then $\triangle ABC$ would not contain the center of $u$. Thus either both $R_1$ and $R_3$ contain vertices of the triangle, or both $R_2$ and $R_4$ do. In either case, two vertices of $\triangle ABC$ are closest to two opposite sides of $u$. Since the distance between these vertices is no more than 1, $u$ must contain at least one of these points. $\square$

> *[Figure 19 -- not extractable from PDF]*

**Lemma 4.** If the center of a unit square $u$ is contained in the rectangle $R = [0,1] \times [0, 0.4]$, then $u$ contains a vertex of $R$.

*Proof:* Let $A = (0,0)$, $B = (0, 0.4)$, $C = (1,0)$, and $D = (1, 0.4)$. It suffices to show that any $u$ that contains $A$ and $B$ on its boundary and whose center is in $R$ contains either $C$ or $D$ (see Figure 20). This is clearly the case if $A$ and $B$ lie on the same side of $u$. When $\theta = 45^\circ$, $u$ contains both $C$ and $D$. It is easy to see that when $\theta < 45^\circ$, $u$ contains $D$, and when $\theta > 45^\circ$, $u$ contains $C$. $\square$

> *[Figure 20 -- not extractable from PDF]*

**Lemma 5.** If a unit square has its center below the line $y = 1$, and is entirely above the $x$-axis, then the length of the intersection of the line $y = 1$ with the square is at least $2\sqrt{2} - 2$.

*Proof:* Let $L$ be the line $y = 1$. Since the center of the square is below $L$, 2 or fewer corners of the square are above $L$. If 2 corners are above $L$, then $L$ intersects 2 opposite sides of the square, and therefore the intersection has length at least 1. If none of the corners are above $L$, 2 corners sit on the $x$-axis, and the length of the intersection is exactly 1. We therefore assume 1 corner is above $L$. In this case, the intersection is made smaller by moving the square downwards until one of the corners is touching the $x$-axis.

If the square makes an angle $\theta$ with the $x$-axis, the vertical line segment in Figure 21 has length $(\sin\theta + \cos\theta - 1)$, so the length of the intersection with $L$ is

$$D = (\sin\theta + \cos\theta - 1)(\tan\theta + \cot\theta) = \frac{\sin\theta + \cos\theta - 1}{\sin\theta\cos\theta}.$$

This is minimized when $dD/d\theta = (\sin\theta - \cos\theta)(1 - \cos\theta)(1 - \sin\theta) / (\cos^2\theta\,\sin^2\theta) = 0$, which occurs at $\theta = 45^\circ$. Thus $D \geq 2\sqrt{2} - 2$. $\square$

> *[Figure 21 -- not extractable from PDF]*

**Lemma 6.** If a unit square has its center in the region $[0,1]^2$, does not contain either of the points $(0,1)$ and $(1,1)$, and is entirely above the $x$-axis, then the square covers some point $(0, y)$ for $1/2 \leq y \leq 1$ and some point $(1, y)$ for $1/2 \leq y \leq 1$.

*Proof:* Lowering the square until it touches the $x$-axis lowers any points of intersection with the $y$-axis. Moving the square right until it touches the point $(1,1)$ makes any intersection with the $y$-axis smaller. We will show that any such square touching the $x$-axis and the point $(1,1)$ covers some point $(0, y)$ for $1/2 \leq y \leq 1$. The rest of the lemma follows from symmetry.

If $x$ is the distance in Figure 22, then $\sin\theta + x\cos\theta = 1$, or $x = (1 - \sin\theta)/\cos\theta$. This means the $x$-intercept of the square is

$$1 + x\sin\theta - \cos\theta = 1 + \tan\theta\,(1 - \sin\theta) - \cos\theta.$$

Therefore the left corner of the square is $(1 + \tan\theta\,(1 - \sin\theta) - \cos\theta - \sin\theta,\; \cos\theta)$. This means the largest $y$-intercept of the square is

$$D = \cos\theta - \tan\theta\,(1 + \tan\theta\,(1 - \sin\theta) - \cos\theta - \sin\theta) = \frac{\cos^3\theta + \sin\theta\,(1 - \cos\theta)(1 - \sin\theta)}{\cos^2\theta}.$$

Since $dD/d\theta = (1 - \cos\theta - \sin\theta)(1 - \sin\theta)/\cos^3\theta < 0$, the minimum value of $D$ is the limit of $D$ as $\theta$ approaches $90^\circ$, which is $1/2$ by L'Hopital's Rule. $\square$

> *[Figure 22 -- not extractable from PDF]*

**Lemma 7.** If a unit square has its center in the region $[0,1]^2$, does not contain either of the points $(0,1)$ or $(1,1)$, and is entirely above the $x$-axis, then the square covers either the point $(0, \sqrt{2} - 1/2)$ or the point $(1, \sqrt{2} - 1/2)$.

*Proof:* Lemma 2 shows that the center of the square cannot have $y$-coordinate less than or equal to $\sqrt{2} - 1/2$ without covering one of these points. Lemma 4 shows that the center of the square cannot have $y$-coordinate more than $\sqrt{2} - 1/2$ without covering one of these points. $\square$

## 5 Lower Bounds

To show that $s(n) \geq k$, we will modify a method used by Walter Stromquist [13]. We will find a set $P$ of $(n-1)$ points in a square $S$ of side $k$ so that any unit square in $S$ contains an element of $P$ (possibly on its boundary). Shrinking these by a factor of $(1 - \varepsilon/k)$ gives a set $P'$ of $(n-1)$ points in a square $S'$ of side $(k - \varepsilon)$ so that any unit square in $S'$ contains an element in $P'$ in its interior. Therefore no more than $(n-1)$ non-overlapping squares can be packed into a square of side $(k - \varepsilon)$, and $s(n) > k - \varepsilon$. Since this is true for all $\varepsilon > 0$, we must have $s(n) \geq k$.

We call $P$ a set of unavoidable points in $S$. We now prove lower bounds on $s(n)$ by showing that certain sets of points are unavoidable.

**Theorem 1.** $s(2) = s(3) = 2$.

*Proof:* Consider a unit square $u$ in $[0,2]^2$. Since the center of $u$ is either in $[0,1]^2$ or $[0,1] \times [1,2]$ or $[1,2] \times [0,1]$ or $[1,2]^2$, Lemma 1 shows that $u$ contains the point $(1,1)$. That is, the set $P = \{(1,1)\}$ is unavoidable in $[0,2]^2$ (see Figure 23). $\square$

> *[Figure 23: Unavoidable set for $s(2) \geq 2$ -- not extractable from PDF]*

**Theorem 2.** $s(5) = 2 + 1/\sqrt{2}$.

*Proof:* The set $P = \{(1,1),\, (1, 1 + 1/\sqrt{2}),\, (1 + 1/\sqrt{2}, 1),\, (1 + 1/\sqrt{2}, 1 + 1/\sqrt{2})\}$ is unavoidable in $[0, 2 + 1/\sqrt{2}]^2$. This follows from Lemma 1 if the center of the square is in a corner, from Lemma 2 if it is near a side, and from Lemma 3 if it is in a triangle (see Figure 24). $\square$

> *[Figure 24: Unavoidable set for $s(5) \geq 2 + 1/\sqrt{2}$ -- not extractable from PDF]*

**Theorem 3.** $s(8) = 3$.

*Proof:* The set $P = \{(0.9, 1),\, (1.5, 1),\, (2.1, 1),\, (1.5, 1.5),\, (0.9, 2),\, (1.5, 2),\, (2.1, 2)\}$ is unavoidable in $[0,3]^2$ by Lemmas 1, 2, and 3 (see Figure 25). $\square$

> *[Figure 25: Unavoidable set for $s(8) \geq 3$ -- not extractable from PDF]*

**Theorem 4.** $s(15) = 4$.

*Proof:* The set

$P = \{(1,1),\, (1.6, 1),\, (2.4, 1),\, (3,1),\, (1, 1.8),\, (2, 1.8),\, (3, 1.8),\, (1, 2.2),\, (2, 2.2),\, (3, 2.2),\, (1,3),\, (1.6, 3),\, (2.4, 3),\, (3,3)\}$

is unavoidable in $[0,4]^2$ by Lemmas 1, 2, 3, and 4 (see Figure 26). $\square$

> *[Figure 26: Unavoidable set for $s(15) \geq 4$ -- not extractable from PDF]*

**Theorem 5.** $s(24) = 5$.

*Proof:* The set

$P = \{(1,1),\, (1.7, 1),\, (2.5, 1),\, (3.3, 1),\, (4,1),\, (1, 1.7),\, (2, 1.7),\, (3, 1.7),\, (4, 1.7),\, (1, 2.5),\, (1.5, 2.5),\, (2.5, 2.5),\, (3.5, 2.5),\, (4, 2.5),\, (1, 3.3),\, (2, 3.3),\, (3, 3.3),\, (4, 3.3),\, (1,4),\, (1.7, 4),\, (2.5, 4),\, (3.3, 4),\, (4,4)\}$

is unavoidable in $[0,5]^2$ by Lemmas 1, 2, and 3 (see Figure 27). $\square$

> *[Figure 27: Unavoidable set for $s(24) \geq 5$ -- not extractable from PDF]*

**Theorem 6.** $s(35) = 6$.

*Proof:* The set

$P = \{(1, 0.9),\, (2, 0.9),\, (3, 0.9),\, (4, 0.9),\, (5, 0.9),\, (1, 1.725),\, (1.5, 1.725),\, (2.5, 1.725),\, (3.5, 1.725),\, (4.5, 1.725),\, (5, 1.725),\, (1, 2.55),\, (2, 2.55),\, (3, 2.55),\, (4, 2.55),\, (5, 2.55),\, (1, 3.375),\, (1.5, 3.375),\, (2.5, 3.375),\, (3.5, 3.375),\, (4.5, 3.375),\, (5, 3.375),\, (1, 4.2),\, (2, 4.2),\, (3, 4.2),\, (4, 4.2),\, (5, 4.2),\, (1,5),\, (1.6, 5),\, (2.4, 5),\, (3,5),\, (3.6, 5),\, (4.4, 5),\, (5,5)\}$

is unavoidable in $[0,6]^2$ by Lemmas 1, 2, and 3 (see Figure 28). $\square$

> *[Figure 28: Unavoidable set for $s(35) \geq 6$ -- not extractable from PDF]*

The proofs that $s(7) = 3$ and $s(14) = 4$ are a little harder. We find sets of points which are almost unavoidable, which force squares into certain positions. We use Lemmas 5, 6, and 7 to show that certain regions are covered, and find sets of unavoidable points for the rest of the square.

**Theorem 7.** $s(7) = 3$.

*Proof:* If 7 unit squares are packed in a square of side $3 - \varepsilon$, at most 5 squares cover the 5 points in the almost unavoidable set shown in Figure 29. Therefore at least two squares have their centers in the regions containing question marks.

> *[Figure 29: Almost unavoidable set for $s(7) \geq 3$ -- not extractable from PDF]*

There are 2 possible placements of these 2 squares up to rotation and reflection. Figure 30 shows these possibilities. The shaded trapezoids show points that must be covered by squares in those regions because of Lemmas 5, 6, and 7. Actually, we have drawn the trapezoids with a $y$ value of $1/2$ in Lemma 6 because this is the worst case in what follows. Each diagram shows a set of 3 additional unavoidable points. $\square$

> *[Figure 30: Two cases for the proof of $s(7) = 3$ -- not extractable from PDF]*

**Theorem 8.** $s(14) = 4$.

*Proof:* If 14 unit squares are packed in a square of side $4 - \varepsilon$, at most 12 squares cover the 12 points in the almost unavoidable set shown in Figure 31. Therefore at least two squares have their centers in the regions containing question marks.

> *[Figure 31: Almost unavoidable set for $s(14) \geq 4$ -- not extractable from PDF]*

There are 5 possible placements of these 2 squares up to rotation and reflection. Figure 32 shows the 5 possibilities.

> *[Figure 32: Five cases for the proof of $s(14) = 4$ -- not extractable from PDF]*

Each diagram also shows a set of 11 additional unavoidable (or almost unavoidable) points. Some of these cases have additional cases, and these are shown in Figure 33. $\square$

> *[Figure 33: Subcases for the proof of $s(14) = 4$ -- not extractable from PDF]*

The other lower bounds known are probably not sharp. For example, Trevor Green has shown [8]:

**Theorem 9.** $s(n^2 + 1) \geq 2\sqrt{2} - 1 + \dfrac{n(n-1)^2 + (n-1)\sqrt{2n}}{n^2 + 1}$.

**Theorem 10.** $s(n^2 + \lfloor n/2 \rfloor + 1) \geq 2\sqrt{2} + 2(n-2)/\sqrt{5}$.

And Walter Stromquist has shown [18]:

**Theorem 11.** $s(11) \geq 2 + 4/\sqrt{5}$.

Unavoidable sets illustrating some of the lower bounds on $s(n)$ are shown in Figure 34.

> *[Figure 34: Unavoidable sets for $s(17) \geq (40\sqrt{2} + 19)/17$, $s(19) \geq 6\sqrt{2} - 4$ -- not extractable from PDF]*

## Appendix

Table 1 contains the best known upper bounds on $s(n)$ for $n \leq 100$. For each primitive packing, the Figure and the Author are given.

<!-- NOTE (important): the "Optimal?" column below was NOT read from the extraction. The
     column header exists in the original, but pdfminer interleaved the table columns and
     the per-row values were lost. The transcriber INFERRED each entry from the theorems
     proved in the body of this survey plus Nagamochi's s(n^2-1)=s(n^2-2)=n and the trivial
     s(n^2)=n. Treat this column as a reconstruction, not as the survey's own data.
     The same applies to both appendix tables (53 and 29 rows), which were reassembled by
     cross-referencing interleaved column extractions against the prose.
     Note also that this survey predates later results (e.g. Bentz proved s(13)=4 in 2010),
     so blanks here mean "not proved as of this revision", not "still open today". -->

| $n$ | $s(n)$ | Optimal? | Figure | Author |
|-----|--------|----------|--------|--------|
| 1 | 1 | Yes | | |
| 2--4 | 2 | Yes | | |
| 5 | $2 + 1/\sqrt{2} \approx 2.7072$ | Yes | Figure 1 | Gobel |
| 6--9 | 3 | Yes | | |
| 10 | $3 + 1/\sqrt{2} \approx 3.7072$ | Yes | Figure 1 | Gobel |
| 11 | $\approx 3.8771$ | | Figure 6 | Trump |
| 12--13 | 4 | | | |
| 14--16 | 4 | Yes | | |
| 17 | $\approx 4.6756$ | | Figure 12 | Bidwell |
| 18 | $(7 + \sqrt{7})/2 \approx 4.8229$ | | Figure 7 | Hamalainen |
| 19 | $3 + 4\sqrt{2}/3 \approx 4.8857$ | | Figure 4 | Wainwright |
| 20--22 | 5 | | | |
| 23--25 | 5 | Yes | | |
| 26 | $(7 + 3\sqrt{2})/2 \approx 5.6214$ | | Figure 9 | Friedman |
| 27 | $5 + 1/\sqrt{2} \approx 5.7072$ | | Figure 1 | Gobel |
| 28 | $3 + 2\sqrt{2} \approx 5.8285$ | | Figure 3 | Gobel |
| 29 | $\approx 5.9344$ | | Figure 12 | Gensane/Ryckelynck |
| 30--33 | 6 | | | |
| 34--36 | 6 | Yes | | |
| 37 | $\approx 6.5987$ | | Figure 16 | Cantrell |
| 38 | $6 + 1/\sqrt{2} \approx 6.7072$ | | Figure 1 | Gobel |
| 39 | $\approx 6.8189$ | | Figure 15 | Cantrell |
| 40 | $4 + 2\sqrt{2} \approx 6.8285$ | | Figure 3 | Gobel |
| 41 | $\approx 6.9473$ | | Figure 16 | Cantrell |
| 42--46 | 7 | | | |
| 47--49 | 7 | Yes | | |
| 50 | $\approx 7.5987$ | | | |
| 51 | $\approx 7.7044$ | | Figure 16 | Hajba |
| 52 | $7 + 1/\sqrt{2} \approx 7.7072$ | | Figure 1 | Gobel |
| 53 | $\approx 7.8231$ | | Figure 11 | Cantrell |
| 54 | $\approx 7.8488$ | | Figure 14 | Cantrell |
| 55 | $\approx 7.9871$ | | Figure 16 | Cantrell |
| 56--61 | 8 | | | |
| 62--64 | 8 | Yes | | |
| 65 | $5 + 5/\sqrt{2} \approx 8.5356$ | | Figure 3 | Gobel |
| 66 | $3 + 4\sqrt{2} \approx 8.6569$ | | Figure 5 | Stenlund |
| 67 | $8 + 1/\sqrt{2} \approx 8.7072$ | | Figure 1 | Gobel |
| 68 | $15/2 + \sqrt{7}/2 \approx 8.8229$ | | Figure 11 | Cantrell |
| 69 | $\approx 8.8562$ | | Figure 14 | Cantrell |
| 70 | $\approx 8.9121$ | | Figure 13 | Cantrell |
| 71 | $\approx 8.9633$ | | Figure 16 | Cantrell |
| 72--78 | 9 | | | |
| 79--81 | 9 | Yes | | |
| 82 | $6 + 5/\sqrt{2} \approx 9.5356$ | | | |
| 83 | $4 + 4\sqrt{2} \approx 9.6569$ | | | |
| 84 | $9 + 1/\sqrt{2} \approx 9.7072$ | | Figure 1 | Gobel |
| 85 | $11/2 + 3\sqrt{2} \approx 9.7427$ | | Figure 9 | Friedman |
| 86 | $(17 + \sqrt{7})/2 \approx 9.8229$ | | Figure 15 | Friedman |
| 87 | $\approx 9.8520$ | | Figure 10 | Cantrell |
| 88 | $\approx 9.9018$ | | Figure 13 | Cantrell |
| 89 | $5 + 7/\sqrt{2} \approx 9.9498$ | | Figure 3 | Gobel |
| 90--97 | 10 | | | |
| 98--100 | 10 | Yes | | |

*Table 1. Best known upper bounds for $s(n)$*

Table 2 contains the best known non-trivial lower bounds on $s(n)$ for $n \leq 85$, along with the Author.

| $n$ | $s(n) \geq$ | Figure | Author |
|-----|-------------|--------|--------|
| 2--3 | 2 | Figure 23 | Gobel |
| 5 | $2 + 1/\sqrt{2} \approx 2.7071$ | Figure 24 | Gobel |
| 6 | 3 | | Kearney/Shiu |
| 7 | 3 | Figure 29 | Friedman |
| 8 | 3 | Figure 25 | Friedman |
| 10 | $3 + 1/\sqrt{2} \approx 3.7071$ | | Stromquist |
| 11--12 | $2 + 4/\sqrt{5} \approx 3.7888$ | | Stromquist |
| 13 | $\approx 3.8437$ | | Friedman |
| 14 | 4 | Figure 31 | Friedman |
| 15 | 4 | Figure 26 | Friedman |
| 17--18 | $(40\sqrt{2} + 19)/17 \approx 4.4452$ | Figure 34 | Green |
| 19--20 | $6\sqrt{2} - 4 \approx 4.4852$ | Figure 34 | Friedman |
| 21 | $\approx 4.7438$ | | Friedman |
| 22 | $2\sqrt{2} + 2 \approx 4.8284$ | | Green |
| 23 | 5 | | Nagamochi |
| 24 | 5 | Figure 27 | Friedman |
| 26--27 | $2\sqrt{2} + (27 + 2\sqrt{10})/13 \approx 5.3918$ | | Green |
| 28--30 | $2\sqrt{2} + 6/\sqrt{5} \approx 5.5117$ | | Green |
| 31 | $\approx 5.6415$ | | Green |
| 34 | 6 | | Nagamochi |
| 35 | 6 | Figure 28 | Friedman |
| 37--39 | $2\sqrt{2} + (113 + 10\sqrt{3})/37 \approx 6.3506$ | | Green |
| 40--41 | $2\sqrt{2} + 8/\sqrt{5} \approx 6.4061$ | | Green |
| 47--48 | 7 | | Nagamochi |
| 50--53 | $2\sqrt{2} + (101 + 3\sqrt{14})/25 \approx 7.3174$ | | Green |
| 62--63 | 8 | | Nagamochi |
| 65--68 | $2\sqrt{2} + 71/13 \approx 8.2899$ | | Green |
| 79--80 | 9 | | Nagamochi |
| 82--85 | $2\sqrt{2} + (288 + 12\sqrt{3})/41 \approx 9.2667$ | | Green |

*Table 2. Best known lower bounds for $s(n)$*

## References

[1] J. Bidwell, 1998, private communication.

[2] H. T. Croft, K. J. Falconer, and R. K. Guy, *Unsolved Problems in Geometry*, Springer Verlag, Berlin (1991) 108--110.

[3] P. Erdos and R. L. Graham, On Packing Squares with Equal Squares, *J. Combin. Theory Ser. A* 19 (1975) 119--123.

[4] M. Gardner, "Mathematical Games", *Scientific American* (Oct 1979, Nov 1979, Mar 1980, Nov 1980).

[5] M. Gardner, *Fractal Music, Hypercards and More . . .*, W. H. Freeman and Company, New York, 289--306.

[6] M. Gardner, 1998, private communication.

[7] F. Gobel, Geometrical Packing and Covering Problems, in *Packing and Covering in Combinatorics*, A. Schrijver (ed.), Math Centrum Tracts 106 (1979) 179--199.

[8] T. Green, 2000, private communication.

[9] M. Kearney and P. Shiu, Efficient Packing of Unit Squares in a Square, *Elect. J. Comb.* 9 #R14 (2002).

[10] K. F. Roth and R. C. Vaughan, Inefficiency in Packing Squares with Unit Squares, *J. Combin. Theory Ser. A* 24 (1978) 170--186.

[11] "Problem Ronden", *Ronden* (Apr 1980, Sep 1980, Dec 1980)

[12] S. El Moumni, Optimal Packings of Unit Squares in a Square, *Studia Sci. Math. Hungar.* 35 (1999), no. 3--4, 281--290.

[13] W. Stromquist, "Packing Unit Squares Inside Squares III", unpublished manuscript, 1984.

[14] D. W. Cantrell, 2002, private communication.

[15] E. Friedman, "Erich's Packing Center", http://www.stetson.edu/~efriedma/packing.html.

[16] K. Hajba, 2009, private communication.

[17] D. W. Cantrell, 2005, private communication.

[18] W. Stromquist, Packing 10 or 11 Unit Squares in a Square, *Elect. J. Comb.* 10 #R8 (2003).

[19] H. Nagamochi, Packing Unit Squares in a Rectangle, *Elect. J. Comb.* 12 #R37 (2005).

[20] T. Gensane and P. Ryckelynck, Improved Dense Packings of Congruent Squares in a Square, *Discrete Comput. Geom.* 34 (2005) 97--109.
