# Efficient Packing of Unit Squares in a Square

**Authors:** Michael J. Kearney (Department of Electronic and Electrical Engineering, Loughborough University, M.J.Kearney@lboro.ac.uk) and Peter Shiu (Department of Mathematical Sciences, Loughborough University, P.Shiu@lboro.ac.uk)
**Venue:** The Electronic Journal of Combinatorics 9 (2002), #R14
**Year:** 2002
**Source:** https://www.combinatorics.org/ojs/index.php/eljc/article/view/v9i1r14
**Archived:** 2026-08-22
**Extraction:** pdfminer.six from the original PDF, cleaned for readability. Raw extraction preserved alongside as `kearney-shiu-2002-efficient-packing-unit-squares.raw.md`.

---

> ⚠️ **Contains reconstructed passages.**
> This transcription contains **1** annotated passage(s) where the PDF extraction was
> damaged and text or mathematics was reconstructed or marked unrecoverable. Search this
> file for `GARBLED` and `NOTE` to find them.
> **Any formula near an annotation must be checked against `kearney-shiu-2002-efficient-packing-unit-squares.raw.md`**, which is the
> unedited extraction and the ground truth for this document.

## Abstract

Let $s(N)$ denote the edge length of the smallest square in which one can pack $N$ unit squares. A duality method is introduced to prove that $s(6) = s(7) = 3$. Let $n_r$ be the smallest integer $n$ such that $s(n^2 + 1) \leq n + 1/r$. We use an explicit construction to show that $n_r \leq 27r^3/2 + O(r^2)$, and also that $n_2 \leq 43$.

---

## 1. Introduction.

Erdos and Graham [1] initiated the study of packing unit squares in a square by demonstrating that non-trivial packings can result in a wasted area that is surprisingly small. For a square with side length $n + \delta$, where $n$ is an integer and $0 \leq \delta < 1$, they showed by explicit construction that it is possible to have a packing so efficient that the wasted area is $O(n^{7/11})$ for large $n$. By way of contrast, the 'trivial' packing of unit squares gives a wasted area of $(n + \delta)^2 - n^2 > 2\delta n$.

There is now the interesting optimisation problem of packing a given number $N$ of unit squares, especially when $N$ is small, and we denote by $s(N)$ the side length of the smallest square into which one can pack them. Then $s(N)$ is an increasing function with $s(n^2) = n$, so that $\sqrt{N} \leq s(N) \leq \lceil\sqrt{N}\rceil$. The determination of $s(N)$ when $N \neq n^2$ is a rather difficult problem, with only a few values for $s(N)$ having been established for such $N$. For example, it was conjectured that $s(n^2 - n) = n$, but this is known to be false for $n \geq 17$ by an explicit construction; see the recent survey [2] by Friedman, who paid special attention to $s(N)$ with $N \leq 100$. There is a simple proof of the conjecture when $n = 2$, that is $s(2) = 2$, but only claims for the proof of $s(6) = 3$ are reported in [2]. Friedman [2] has proved that $s(7) = 3$, and we introduce a 'duality' method in $\S$2 which delivers a much simplified proof. Indeed, the method enables us to give a reasonably short proof in $\S$3 of

**Theorem 1.** We have $s(6) = 3$.

The determination of $s(n^2 + 1)$ is particularly interesting, and we now set

$$\delta_n = s(n^2 + 1) - n. \tag{1}$$

We remark that $\delta_{n+1} \leq \delta_n$, that is $s\big((n+1)^2 + 1\big) \leq s(n^2 + 1) + 1$, which follows from the consideration of adding $2n + 1$ unit squares forming an 'L' round two sides of the square for an existing packing. There is the trivial lower bound $\delta_n \geq \sqrt{n^2 + 1} - n \approx 1/(2n)$; thus $\delta_n > 1/(3n)$ and the result of Erdos and Graham [1] implies that $\delta_n \ll n^{-4/11}$ as $n \to \infty$. We adopt a simpler version of their constructive argument in $\S$5 to give a slightly inferior bound, but one which is also valid for small values of $n$.

**Theorem 2.** For all $n \geq 1$, we have

$$\delta_n < \frac{3}{(2n)^{1/3}} + \frac{3}{(2n)^{2/3}}. \tag{2}$$

Only $\delta_1 = 1$ and $\delta_2 = 1/\sqrt{2}$ have been determined; see [2] where the bounds

$$0.5183\ldots \leq \delta_3 \leq 0.7071\ldots \tag{3}$$

are also given. All the packings mentioned in [2] involve squares with side lengths having fractional parts exceeding $\frac{1}{2}$. In $\S$4 we use solutions to the Pell equation $x^2 + 1 = 2y^2$ to give a simple proof that if $\delta > \frac{1}{2}$ then there exists $n$ such that $\delta_n < \delta$. In particular, we show that $\delta_8 < 0.536$ and $\delta_{42} < 0.507$, but the question still remains as to the smallest $n$ such that $\delta_n \leq \frac{1}{2}$. The proof of Theorem 2 shows that $\delta_{55} < \frac{1}{2}$. By finding certain simultaneous Diophantine approximations to real numbers in relation to our construction we show in $\S$6 that this can be further improved to

$$\delta_{43} < \frac{1}{2}. \tag{4}$$

In $\S$4 we also apply such approximations to $\sqrt{2}$ to give a simple proof of the following result: If $\delta > 1/\sqrt{2}$, and $0 < c < 2\delta - \sqrt{2}$, then there are infinitely many $n$ such that $s(n^2 + cn) < n + \delta$. Although our results are inferior to that of Erdos and Graham [1] for large $N$, nevertheless it is instructive to apply number theory to give simple solutions to such problems.

Let $n_r$ be the smallest integer $n$ such that $\delta_n \leq 1/r$, so that estimates for $\delta_n$ can be converted to those for $n_r$. Thus, by the result of Erdos and Graham [1], we have $n_r \ll r^{11/4}$ as $r \to \infty$, and our argument in the proof of Theorem 2 also gives the following result which is valid also for small values of $r$.

**Corollary.** For $r > 1$, we have

$$n_r \leq p(\lceil\tau\rceil) \leq p\!\left(\left\lceil\frac{3r}{2}\right\rceil\right) = \frac{27r^3}{2} + O(r^2), \tag{5}$$

where $p(t) = 4t^3 + 4t^2 + 3t + 1$ and $\tau$ is the real root of $\eta(t) = 1/r$, with

$$\eta(t) = \frac{3}{2t} + \frac{1}{4t^2} - \frac{7}{8t^3} + \frac{5}{8t^5}.$$

From (3) and (4) we have $4 \leq n_2 \leq 43$, and it seems likely that both the bounds are still some distance from the exact value. However, the effort involved in establishing $s(6) = 3$ indicates that it may be tedious to make substantial improvement on the lower bound. Moreover, considering the extremely good simultaneous Diophantine approximations associated with our construction in $\S$6, it appears to us that any improvement on the upper estimate will require a very different arrangement for the unit squares to ours. Thus to improve on these bounds represents an interesting challenge. Using essentially the same ideas, we have also found that $n_3 \leq 239$, $n_4 \leq 625$, $n_5 \leq 1320$, $n_6 \leq 2493$ and $n_7 \leq 4072$.

## 2. Proof of $s(7) = 3$.

We first give our proof of $s(7) = 3$. Since $s(7) \leq s(3^2) = 3$ it suffices to establish that $s(7) \geq 3$. Following Friedman [2], we use the notion of an *unavoidable set* of points in a square $S$, namely a finite set of points so placed that any unit square inside $S$ must contain a member of the set, possibly on its boundary. If we now shrink the square $S$ together with the unavoidable set by a positive factor $\lambda < 1$, then any unit square inside the shrunken square contains an unavoidable point in its interior. Consequently, if a square $S$ with side length $k$ possesses an unavoidable set of $N - 1$ points then $s(N) \geq \lambda k$ for every $\lambda < 1$, and hence $s(N) \geq k$. For the sake of clarity of presentation, we shall omit the shrinking factor $\lambda$ in the following.

> *[Figure 1: The set of 7 unavoidable points -- not extractable from PDF]*

Friedman [2] showed that the centre point $(1, 1)$ in $[0, 2]^2$ is unavoidable, so that $s(2) = 2$. By finding appropriate unavoidable sets he also proved that $s(n^2 - 1) = n$ for $n = 3, 4, 5, 6$. In particular, for the proof of $s(8) = 3$, Friedman constructed an unavoidable set of 7 points, which are essentially the points

$$\left\{\left(\sqrt{2} - \tfrac{1}{2}, 1\right), \left(\tfrac{3}{2}, 1\right), \left(\tfrac{7}{2} - \sqrt{2}, 1\right), \left(\tfrac{3}{2}, \tfrac{3}{2}\right), \left(\sqrt{2} - \tfrac{1}{2}, 2\right), \left(\tfrac{3}{2}, 2\right), \left(\tfrac{7}{2} - \sqrt{2}, 2\right)\right\} \tag{6}$$

in the square $S = [0, 3]^2$; see Figure 1. We omit the proof that these points form an unavoidable set, since it is essentially that given by Friedman, who also gives a more complicated proof for $s(7) = 3$ by considering an 'almost unavoidable set' with 5 points. Our simplified proof makes use of a duality argument based on (6).

We give the colour *green* to the 7 points in (6) and we say that the unavoidable set forms a *green lattice* within $S$. Rotating this lattice by a right-angle about the centre point $(\frac{3}{2}, \frac{3}{2})$, we obtain a *red lattice* with the corresponding 7 red points. With $S$ being a square, the red lattice also forms an unavoidable set, and we may consider it as the dual of the green lattice. The two lattices have the common centre point $(\frac{3}{2}, \frac{3}{2})$, so that there are 13 distinct points in their union. We also classify these 13 points into three types: the centre point $(\frac{3}{2}, \frac{3}{2})$ will be called the C-point, the 8 points furthest away from the C-point will be called the A-points, and the remaining 4 points having distance $\frac{1}{2}$ from the C-point are the B-points. Thus each lattice consists of four A-points, two B-points, and the C-point; see Figure 2. Since each lattice forms an unavoidable set, any unit square contained in $S$ must cover at least one point from each lattice, and we remark that the C-point is both green and red. For a packing, each point in $S$ may be covered by at most one unit square.

> *[Figure 2: The union of two lattices of unavoidable points -- not extractable from PDF]*

**Lemma 1.** Any unit square which covers the C-point must also cover a B-point.

*Proof.* Let the unit square have a diagonal specified by the points $(0, 0)$ and $(1, 1)$. By symmetry, we may assume that the C-point has the coordinates $(x_0, y_0)$ with $0 \leq x_0 \leq y_0 \leq \frac{1}{2}$. The circle with centre the C-point and radius $\frac{1}{2}$ has the equation $(x - x_0)^2 + (y - y_0)^2 = \frac{1}{4}$, so that it intersects the edges of the unit square at the points

$$\left(x_0 \pm \sqrt{\tfrac{1}{4} - y_0^2},\; 0\right), \qquad \left(0,\; y_0 \pm \sqrt{\tfrac{1}{4} - x_0^2}\right),$$

with the two positive signs corresponding to two definite points of intersection. The square of the distance between these two points is at least $x_0^2 + \left(\frac{1}{4} - x_0^2\right) + y_0^2 + \left(\frac{1}{4} - y_0^2\right) = \frac{1}{2}$, which implies that the arc of the circle lying inside the unit square subtends an angle which is at least a right-angle. Since the four B-points are equally spaced on the circle it follows that the unit square must cover at least one B-point. $\square$

In order to pack 7 unit squares into $S = [0, 3]^2$, each square must cover exactly one point in each lattice. Since the C-point belongs to both lattices, it follows at once from Lemma 1 that $S$ cannot have side length less than 3, so that $s(7) = 3$.

## 3. Proof of Theorem 1.

The proof of $s(6) = 3$ is more complicated. Each of the 6 unit squares to be packed in $S$ must cover at least one point from each lattice, so there is at most one unit square which covers two points of the same lattice. If the C-point is not covered then each square must cover precisely one point from each lattice, and we call this *configuration (a)*. If the C-point is covered by a unit square then, by Lemma 1, this square also covers a B-point, which we may assume to be a green point by duality, and we call this *configuration (b)*. It remains to show that these two configurations are impossible when $S$ has side length less than 3, because of the geometric constraints associated with the problem. We shall require the following technical lemmas, the omitted proofs for which involve only elementary coordinate geometry.

**Lemma 2.** Let $U$ be a unit square with centre inside $[0, 1]^2$. Suppose that one corner of $U$ touches the $x$-axis with an edge making an angle $\theta$, and that the point $(0, 1)$ lies on the opposite edge of $U$. Then the points

$$\left(\frac{1 + t^2}{1 + t},\; 1\right) \qquad \text{and} \qquad \left(1,\; \frac{1 + 2t - t^2}{2}\right),$$

where $t = \tan\frac{\theta}{2}$, lie on two of the edges of the square.

**Lemma 3.** Let $V$ be a unit square covering the point $(\frac{3}{2}, \frac{3}{2})$, and suppose that the points $(1, 2)$, $(2, 2)$ and $(2, \frac{3}{2})$ lie on three of the edges of $V$. Then the remaining edge intersects the line $x = 1$ at a height $y \leq \frac{5}{3}$.

Concerning the coordinates displayed in Lemma 2, we remark that, for $0 \leq t \leq 1$,

$$\frac{1 + t^2}{1 + t} \geq 2\sqrt{2} - 2, \qquad \frac{1 + 2t - t^2}{2} \geq \frac{1}{2} \qquad \text{and} \qquad \frac{1 + t^2}{1 + t} + \frac{1 + 2t - t^2}{2} \geq \frac{3}{2}. \tag{7}$$

We now apply Lemma 2 to deal with configuration (a), in which the C-point is not covered, so that each of the 6 unit squares covers exactly one green point and one red point. Take a unit square $U$ which covers a green B-point, and we may assume that its centre is located in region 8 in Figure 2. The square $U$ must cover one of the adjacent red A-points, the one in region 7, say. If $U$ does not cover the point $(1, 1)$ then by Lemma 2 it intersects the line $x = 2$ in such a way that it is impossible to cover the red A-point in region 9 by a second unit square without also covering the red B-point in region 6. To see this we apply Lemma 2 twice, with a rotation of the axis in the second application, so that by the last inequality in (7), the minimum upper intercept on the line $x = 2$ for the unit square concerned will have to be at least $\frac{3}{2}$. Elementary geometric considerations show that any other positioning of the second square will increase the intercept $\frac{3}{2}$. The same argument also shows that if $U$ does cover the point $(1, 1)$ then any unit square covering the green A-point in region 7 and the red B-point in region 4 will intersect the line $y = 2$ in such a way that it is impossible to cover the green A-point in region 1 without also covering the green B-point in region 2. Therefore configuration (a) cannot occur.

In configuration (b), a unit square $V$ covers the C-point and also a green B-point (in region 2, say) so each of the 5 remaining green points must be covered by a unit square. The centre of another unit square $W$ that covers the remaining green B-point will then be located in region 8 in Figure 2. The square $W$ must cover at least one of the adjacent red A-points, the one in region 7, say. If $W$ also covers the point $(1, 1)$, then, by the same argument used in configuration (a), any unit square covering the green A-point in region 7 and the red B-point in region 4 will intersect the line $y = 2$ in such a way that one cannot now cover the green A-point in region 1 without also covering the already covered green B-point in region 2. Thus $W$ cannot cover the point $(1, 1)$; but then, by Lemma 2, a unit square covering the green A-point in region 9 must also cover the red B-point in region 6. Consequently, the following pairings of points must be covered by distinct unit squares: (i) the green A-point in region 7 with the red B-point in region 4, (ii) the two A-points in region 1, (iii) the C-point with the green B-point in region 2, and (iv) the two A-points in region 3. In cases (ii) and (iv), the unit squares concerned must also cover the points $(1, 2)$ and $(2, 2)$ respectively; the argument for this being essentially the same for the fact used to establish $s(2) = 2$, namely that the centre point of a $2 \times 2$ square forms an unavoidable singleton set. The square $V$ covering the C-point and the green B-point in region 2 is now so constrained that it cannot cover any of the points $(1, \frac{3}{2})$, $(1, 2)$, $(2, \frac{3}{2})$, $(2, 2)$. It now follows from Lemma 3, and the fact the red A-point in region 7 is already covered, that the uncovered interval on the line $x = 1$ has length at most $\frac{5}{3} - (\frac{3}{2} - \frac{1}{2}) = \frac{13}{6} - 2 < 2\sqrt{2} - 2$. However, by Lemma 2 and the first inequality in (7), the intercept of the square covering the green A-point in region 7 and the red A-point in region 4 with the line $x = 1$ will require an interval with length at least $2\sqrt{2} - 2$. Therefore configuration (b) also cannot occur, and the proof of $s(6) = 3$ is complete.

## 4. Applying Diophantine properties of $\sqrt{2}$.

> *[Figure 3: Construction demonstrating $s(n^2 + 1) < n + \delta$ with $\frac{1}{2} < \delta < 1$ -- not extractable from PDF]*

As many of the packings displayed in [2] show, by rotating by half a right-angle certain squares from the trivial method of packing squares, we may be able to pack one extra square, or even many extra squares. As is to be expected, such an argument applied to a large square for the packing will involve the Diophantine properties associated with $\sqrt{2}$.

A square is a sum of two triangular numbers. More specifically, the identity

$$(t + 1)^2 = \frac{t(t+1)}{2} + \frac{(t+1)(t+2)}{2}$$

shows that a square with side length $t + 1$ is the sum of two 'triangles' formed by unit squares, with the smaller and larger ones given by the triangular numbers on the right-hand side of the equation. We now start with a square formed by four such squares, and insert two 'corridors' with width $\delta$ forming a cross to separate the four squares. We then remove the four smaller triangles from these four squares in the centre of the large square, so that the number of unit squares being removed is $2t(t+1)$ and the region left is a 'ragged square' together with the corridors; see Figure 3. Suppose now that $t$ is so chosen that $2t(t+1) + 1 = k^2$, with $k$ also being an integer. Then a simple calculation shows that a square with side length $k$, slanting at half a right-angle can fit into the ragged square region, provided the width of the corridors satisfies

$$\delta = \frac{k}{\sqrt{2}} - t.$$

Thus, we can have an initial square with side length $n + \delta$, with $n = 2(t+1)$, packing

$$2(t+1)(t+2) + 2t(t+1) + 1 = 4(t+1)^2 + 1 = n^2 + 1$$

unit squares. The Diophantine equation $2t(t+1) + 1 = k^2$ can be rewritten as $(2t+1)^2 + 1 = 2k^2$, to which there are infinitely many solutions. On rewriting the equation as $(\sqrt{2}k + (2t+1))(\sqrt{2}k - (2t+1)) = 1$, we find that

$$\delta = \frac{k}{\sqrt{2}} - t = \frac{1}{2} + \frac{\sqrt{2}k - (2t+1)}{2} = \frac{1}{2} + \frac{1}{2(\sqrt{2}k + 2t + 1)} \to \frac{1}{2} \quad \text{as } t \to \infty,$$

so that we may choose solutions $t$ so large that $\delta$ can be made arbitrarily close to $\frac{1}{2}$ from above. Table 1 gives the first few solutions.

| $t$ | $k$ | $n$ | $\delta$ |
|-----|-----|-----|----------|
| 0   | 1   | 2   | $0.707\ldots$ |
| 3   | 5   | 8   | $0.5355\ldots$ |
| 20  | 29  | 42  | $0.506\ldots$ |
| 119 | 169 | 240 | $0.501\ldots$ |
| 696 | 985 | 1394 | $0.5001\ldots$ |
| 4059 | 5741 | 8120 | $0.50003\ldots$ |

*Table 1*

Recalling our definition for $\delta_n$ in $\S$1, we note that the corresponding values for $\delta$ in Table 1 are upper bounds for $\delta_n$. The bound for $\delta_2$ is attained, and the bound $\delta_8 \leq 0.5355\ldots$ is currently the best known solution, but not yet proved to be optimal; see [2]. The bound $\delta_{42} \leq 0.506\ldots$ is also interesting in that we shall establish in $\S$6 that $\delta_{43} < 0.5$.

> *[Figure 4: Construction demonstrating $s(n^2 + cn) < n + \beta$ with $\frac{1}{\sqrt{2}} < \beta < 1$ -- not extractable from PDF]*

Next we let $\delta > 1/\sqrt{2}$ and $0 < c < 2\delta - \sqrt{2}$. For such values of $\delta$ and $c$, the interval

$$\frac{c + \sqrt{2}}{2} < \beta < \delta \tag{8}$$

is non-empty. Take a square with side length $2t + 1$, and remove the four 'triangular' corners formed by $t(t+1)/2$ unit squares. The resulting shape is a ragged square, slanted at half a right-angle to the original square, formed with $(2t+1)^2 - 2t(t+1) = 2t^2 + 2t + 1$ unit squares, and this ragged square lies inside a square with side length $(t+1)\sqrt{2}$; see Figure 4. On writing

$$(t+1)\sqrt{2} = n + \beta,$$

with $n$ being the integer part, so that $\beta$ is the fractional part, we find that

$$n^2 = \left((t+1)\sqrt{2} - \beta\right)^2 = 2(t^2 + 2t + 1) - 2\sqrt{2}\beta(t+1) + \beta^2 = 2t^2 + 2t(2 - \sqrt{2}\beta) + O(1). \tag{9}$$

Thus the number of unit squares being packed into a square with side length $n + \beta$ is

$$2t^2 + 2t + 1 = n^2 + 2t(\sqrt{2}\beta - 1) + O(1) = n^2 + \sqrt{2}n(\sqrt{2}\beta - 1) + O(1) = n^2 + n(2\beta - \sqrt{2}) + O(1).$$

Finally, since $\sqrt{2}$ is irrational, there are arbitrarily large $t$ such that the value of $\beta$ in (9) satisfies (8) so that this number here exceeds $n^2 + cn$. Obviously, for all the packings in this section, the wasted area is of order $O(n)$.

## 5. Proof of Theorem 2.

We first consider those $n$ having the form

$$n = p(t - 1), \quad \text{where } p(t) = 4t^3 + 4t^2 + 3t + 1, \tag{10}$$

and proceed to show that, for such $n$, one can pack $n^2 + 1$ unit squares in a square with side length $n + \delta$, where $\delta = \delta(t)$ will be specified later.

> *[Figure 5: Construction used in the proof of Theorem 2 -- not extractable from PDF]*

We partition the square with side length $n + \delta$ into two rectangles, each with the same side width $n + \delta$, and the smaller rectangle $R$ having height $m + \delta$, with

$$m = 2t^2 - t.$$

The larger rectangle has height $n - m$ and we pack it trivially using $(n - m)n$ unit squares, so that it remains to show that $mn + 1$ unit squares can be packed into $R$.

We first partition $R$ into a parallelogram $P$ and two trapezia $T$, $T'$ of equal size on either side of $P$; see Figure 5. The packing of $T$ consists of columns of width 1 and heights $m - jt$, with $j = 0, 1, \ldots, 2t - 2$, so that the number of unit squares being packed is $t^2(2t - 1)$. This packing then defines an angle

$$\theta = \tan^{-1}\frac{1}{t}$$

for the slant side of $T$. We then pack the parallelogram $P$ with slanting columns of length $m + 1$ and width 1, with the first column touching the leading corners of the unit squares in $T$. Observe that, since $m + 1 = 2t^2 - t + 1 > (2t - 1)\sqrt{t^2 + 1} = (2t - 1)\csc\theta$, the sloping column touches all the leading corners, extending slightly above the uppermost corner as shown in Figure 5. The value of $\delta$ can now be derived from the equation

$$(m + 1)\cos\theta + \sin\theta = m + \delta,$$

giving

$$\delta = \delta(t) = \frac{1}{\sqrt{t^2 + 1}} + \frac{t}{\sqrt{t^2 + 1}\left(\sqrt{t^2 + 1} + t\right)} + \frac{t}{\sqrt{t^2 + 1}\left(\sqrt{t^2 + 1} + t\right)^2}.$$

In particular, we have the asymptotic expansion

$$\delta(t) = \frac{3}{2t} + \frac{1}{4t^2} - \frac{7}{8t^3} - \frac{1}{4t^4} + O\!\left(\frac{1}{t^5}\right), \qquad t \to \infty,$$

and also the explicit bound $\delta(t) < \eta(t)$, where $\eta(t)$ is given by (5). We place further columns adjacent to the first column, so that all together $K$ columns are packed into the parallelogram $P$, leaving the trapezium $T'$ to be packed in the same way as that for $T$. With $n$ being specified by (10), we need to set $K = n - 4t + 3$ in order to have the total number of unit squares inside $R$ being $K(m + 1) + 2t^2(2t - 1) = mn + 1$. The total length of the projection of the $K$ columns onto the side width of the rectangle $R$ together those of the two trapezia is given by

$$f(t) = 4t + (K - 1)\sec\theta + \cos\theta - (m + 1)\sin\theta.$$

It can be verified that, for all $t \geq 1$,

$$0 < f(t) - n = \frac{1}{t} - \frac{3}{8t^2} + O\!\left(\frac{1}{t^3}\right) < \delta(t),$$

so that the choice of $n = p(t - 1) = 4t^3 - 8t^2 + 7t - 2$ in (10) is admissible. Moreover, for such $n$, we have

$$2n < \left(2t - \frac{1}{3}\right)^3 < \left(2t - \frac{2t}{6t + 1}\right)^3 = \left(\frac{3}{2t + \frac{1}{3}}\right)^{-3} \cdot \frac{1}{4t^2} \cdot \ldots$$
<!-- GARBLED: unable to reconstruct the chain of inequalities exactly as displayed; the conclusion follows -->

so that

$$\delta_n \leq \delta(t) < \eta(t) < \frac{3}{(2n)^{1/3}},$$

which is sharper than the estimate (2). If $n$ does not have the form in (10) then we choose $t$ so that $p(t - 1) < n < p(t)$. The estimate (2) then follows from $\delta_n \leq \delta_{p(t-1)} \leq \delta(t)$, together with the new upper bound for $n$ in terms of $t$ and the full use of $\delta(t) < \eta(t)$. The theorem is proved, and we note that setting $t = 3$ we find that $\delta_{55} < \frac{1}{2}$. We remark that the wasted area associated with this construction is $O(n^{2/3})$.

The proof of the Corollary proceeds as follows. Let $t_0 = t_0(r)$ be the smallest $t$ satisfying

$$\eta(t) < \frac{3}{2t} + \frac{1}{4t^2} \leq \frac{1}{r}.$$

Then $\delta_n < 1/r$ for $n = p(t_0 - 1)$ and hence, recalling the definition of $n_r$ in $\S$1, $n_r \leq p(t_0 - 1)$. The value for $t_0$ is given by $\lceil\tau\rceil + 1$, where $\tau$ is the positive root of the quadratic equation $4t^2 = 6tr + r$, that is

$$\tau = \frac{3r}{2} + \varepsilon, \qquad \text{with} \quad \varepsilon = \frac{r}{\sqrt{9r^2 + 4r} + 3r}.$$

Since $1/7 < \varepsilon < 1/6$, it follows that $t_0 = \lfloor 3r/2 \rfloor + 1$. A slightly stronger statement comes from choosing $\tau$ to be the real root of $\eta(t) = 1/r$.

## 6. A construction for $\delta_{43} < \frac{1}{2}$.

As noted in $\S$5 we have $\delta_{55} < \frac{1}{2}$, so that $n_2 \leq 55$. By refining the construction, we can improve this to $n_2 \leq 43$. The improved construction is similar to that used in the proof of Theorem 2, but differs in respect of the packing of the trapezia because $n$ is not of the chosen form.

> *[Figure 6: Construction demonstrating $s(43^2 + 1) < 43 + \frac{1}{2}$ -- not extractable from PDF]*

As before, we first partition the square into two rectangles, each with length $n + \delta$, with $n = 43$ and $\delta = \frac{1}{2}$. With $m = 15$, it follows that the larger rectangle has height 28, and the smaller one $R$ has height $y_0 = 15 + \frac{1}{2}$. We then pack $1204 = 43 \times 28$ unit squares trivially in the larger rectangle.

We next partition $R$ into two trapezia $T$ and $T'$ with equal size at opposite ends of $R$, leaving a parallelogram $P$; see Figure 6. We pack $P$ with rectangular columns, each of which is made from $16 \times 1$ unit squares, so that the angle $\theta$ each column makes with the long side of $R$ is given by the equation

$$\cos\theta = \frac{y_0}{16 + \tan\theta},$$

so that

$$\theta = 0.3205\ldots\,.$$

We can pack $576 = 16 \times 36$ unit squares by forming 36 columns within $P$, which now has length $36\sec\theta = 37.932\ldots$. Let the lengths of parallel sides for $T$ be $x_0$ and $x_1 = x_0 + y_0\tan\theta$. Then, since $T$ and $T'$ are the same, we need to have

$$x_0 + x_1 + 36\sec\theta = 43 + \tfrac{1}{2}, \qquad \text{so that} \quad x_0 = 0.210\ldots\,.$$

The four corners for $T$ can be given the coordinates $(0, 0)$, $(x_1, 0)$, $(0, y_0)$, $(x_0, y_0)$, so that the longest side has the equation $y(x_0 - x_1) = y_0(x - x_1)$. Now, for $y = 1, 4, 7, 10, 13$, the corresponding approximate values for $x$ are $5.024$, $4.028$, $3.032$, $2.036$, $1.040$. Thus, we may pack $T$ with unit squares in 13 rows, with 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1 squares in the corresponding rows; that is 35 unit squares can be packed in $T$. The total number of unit squares packed inside the square is thus given by

$$43 \times 28 + 36 \times 16 + 2 \times 35 = 1850 = 43^2 + 1.$$

Optimising the above computations further, we find that $\delta_{43} \leq 0.4888\ldots$.

Using similar ideas, one may show that $n_3 \leq 239$, $n_4 \leq 625$, $n_5 \leq 1320$, $n_6 \leq 2493$ and $n_7 \leq 4072$. The relevant parameters for these constructions are given in Table 2, where $T$ and $T'$ are now the numbers of squares being packed into the trapezia concerned. Note that the larger solutions are not symmetric with respect to the packing of the trapezia.

| $r$ | $n$ | $m$ | $K$ | $T$ | $T'$ |
|-----|-----|-----|-----|-----|------|
| 2   | 43  | 15  | 36  | 35  | 35   |
| 3   | 239 | 30  | 225 | 98  | 98   |
| 4   | 625 | 67  | 604 | 430 | 374  |
| 5   | 1320 | 119 | 1295 | 855 | 826  |
| 6   | 2493 | 158 | 2460 | 1448 | 1307 |
| 7   | 4072 | 217 | 4034 | 2120 | 2093 |

*Table 2*

These results provide upper bounds for $n_r$ and hence $\delta_n$. In Figure 7 we plot the bound for $\delta_n$ together with the weaker bound indicated by Theorem 2. The further optimisation obviously leads to slight improvements for the upper bounds for the particular values considered.

> *[Figure 7: Log-log plot of bounds for $\delta_n$ -- not extractable from PDF]*

The above suggests that the limit

$$-\beta = \lim_{n \to \infty} \frac{\log\delta_n}{\log n}$$

exists, and our explicit construction implies that $\frac{1}{3} \leq \beta \leq 1$, while the result of Erdos and Graham [1] shows the lower bound can be improved slightly to $\beta \geq 4/11$. The existence and the exact value of $\beta$ remain to be established.

## References.

[1] P. Erdos and R. L. Graham, "On packing squares with equal squares", *J. Combin. Theory, Ser. A*, 19 (1975) 119--123.

[2] E. Friedman, "Packing unit squares in squares: A survey and new results", *The Electronic Journal of Combinatorics*, Dynamic Surveys (#DS7), http://www.combinatorics.org/Surveys/ds7.html (2000) 25pp.
