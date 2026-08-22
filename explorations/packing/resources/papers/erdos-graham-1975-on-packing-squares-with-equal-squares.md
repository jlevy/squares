# On Packing Squares with Equal Squares

**Authors:** P. Erdos and R. L. Graham
**Venue:** Journal of Combinatorial Theory, Series A, 19 (1975) 119--123. This copy is Stanford Computer Science Technical Report STAN-CS-75-483.
**Year:** 1975
**Source:** http://i.stanford.edu/pub/cstr/reports/cs/tr/75/483/CS-TR-75-483.pdf
**Archived:** 2026-08-22
**Extraction:** pdfminer.six from the original PDF (a 1975 typescript scan), cleaned for readability. The extraction quality is poor; many mathematical formulas are garbled or missing. Raw extraction preserved alongside as `erdos-graham-1975-on-packing-squares-with-equal-squares.raw.md`.

---

> ⚠️ **Contains reconstructed passages.**
> This transcription contains **17** annotated passage(s) where the PDF extraction was
> damaged and text or mathematics was reconstructed or marked unrecoverable. Search this
> file for `GARBLED` and `NOTE` to find them.
> **Any formula near an annotation must be checked against `erdos-graham-1975-on-packing-squares-with-equal-squares.raw.md`**, which is the
> unedited extraction and the ground truth for this document.

P. Erdos
Stanford University and The Hungarian Academy of Sciences

R. L. Graham
Stanford University and Bell Laboratories, Murray Hill, New Jersey

STAN-CS-75-483, March 1975

## Abstract

The following problem arises in connection with certain multidimensional stock cutting problems:

How many non-overlapping open unit squares may be packed into a large square of side $\alpha$?

Of course, if $\alpha$ is a positive integer, it is trivial to see that $\alpha^2$ unit squares can be successfully packed. However, if $\alpha$ is not an integer, the problem becomes much more complicated. Intuitively, one feels that for $\alpha = N +$<!-- GARBLED: fractional part garbled in extraction; likely "N + 1/2" or similar --> , say, (where $N$ is an integer), one should pack $N^2$ unit squares in the obvious way and surrender the uncovered border area (which is about <!-- GARBLED: waste expression garbled in extraction; likely proportional to alpha -->) as unusable waste. After all, how could it help to place the unit squares at all sorts of various skew angles?

In this note, we show how it helps. In particular, we prove that we can always keep the amount of uncovered area down to at most proportional to <!-- GARBLED: exponent garbled in extraction; this is alpha^{7/11} -->, which for large $\alpha$ is much less than the linear waste produced by the "natural" packing above.

---

*This research was supported in part by National Science Foundation grant GJ 36473 and by the Office of Naval Research contract NR 044-402. Reproduction in whole or in part is permitted for any purpose of the United States Government.*

---

If two non-overlapping squares are inscribed in a unit square, then the sum of their circumferences is at most 4, the circumference of the unit square. As far as we know, this was first published by P. Erdos and appeared as a problem in a mathematical paper for high school students in Hungary.

A. Beck and M. N. Bleicher [1] proved that if a closed convex curve $\mathcal{C}$ has the property that for every two inscribed non-overlapping similar curves $\mathcal{C}_1$ and $\mathcal{C}_2$, the sum of the circumferences of $\mathcal{C}_1$ and $\mathcal{C}_2$ is not greater than the circumference of $\mathcal{C}$, then $\mathcal{C}$ is either a regular polygon or a curve of constant width.

It is clear that one can inscribe $k^2$ squares into a unit square so that the sum of their circumferences is $4k$. P. Erdos conjectured 40 years ago that if we inscribe $k^2 + 1$ squares into a unit square, the total circumference remains at most $4k$. For $k = 1$, this is true as we have just stated. D. J. Newman [2] proved the conjecture for $k = 2$ but the general case is still unsettled.

Denote by $f(a)$ the maximal sum of circumferences of $a$ non-overlapping squares packed into a unit square. The conjecture we cannot prove is just $f(k^2 + 1) = 4k$. In this note we show $f(\ell) > 4k$ for $\ell = k^2 + o(k)$, (in fact, for $a = k^2 + [ck^{7/11}]$ using just equal squares).<!-- GARBLED: the precise expression in the brackets was garbled in extraction; the reconstructed form follows the cleaner rendering later in the paper --> We do not know as $f(a)$ increases from $4k$ to $4k + 4$ how large the jumps are and where they occur.

Instead of maximizing the circumference sum of packings of a unit square by arbitrary squares, we shall work with the closely related problem of maximizing the area sum of packings of an arbitrary square by unit squares.

For each positive real $\alpha$, define

$$w(\alpha) = \alpha^2 - \sup_P |P|$$

where $P$ ranges over all packings of unit squares into a given square $S(\alpha)$ of side $\alpha$ and $|P|$ denotes the number of unit squares in $P$.

**Theorem.**

$$w(\alpha) = \Theta(\alpha^{7/11}) \tag{1}$$
<!-- NOTE: The theorem statement (equation 1) was not extracted by pdfminer; it is reconstructed here as the well-known result of this paper. The raw extraction shows only "Theorem." followed by "(1)" with no formula between them. -->

*Proof:* We sketch a construction which will prove (1). As usual, the notation $f(x) = \Theta(g(x))$ will denote the existence of two positive constants $c$ and $c'$ such that $cg(x) < f(x) < c'g(x)$ for all sufficiently large $x$.

We begin by packing $S(\alpha)$ with $N^2$ unit squares which form a subsquare $S(N)$ in the lower left-hand corner of $S(\alpha)$ as shown in Fig. 1, where $N =$<!-- GARBLED: unable to reconstruct --> and $\alpha$ is large.

> *[Figure 1 -- not extractable from PDF]*

The remaining uncovered area can be decomposed into two rectangles, each having width $\beta = \alpha - N$ and lengths $\geq N$.

Next, we pack a rectangle $R(\beta, \gamma)$ of sides $\beta$ and $\gamma$ with $\gamma = \Theta(\alpha)$, $\beta = \Theta(\alpha^{8/11})$ as follows.

Let $n = [\beta]$. Place adjacent parallel rectangles $R(1, n+1)$, each formed from $n + 1$ unit squares, tilted at the appropriate angle $\theta$ so that all $R(1, n+1)$'s touch both the top and bottom edges of $R(\beta, \gamma)$. Furthermore, place these so that $D = \Theta(\alpha^{2/11})$ (see Fig. 2). Note that $D' = \Theta(\alpha^{4/11})$.
<!-- NOTE: Throughout the proof, asymptotic expressions of the form Theta(alpha^{n/11}) were partially garbled in extraction. The exponents n/11 have been reconstructed where the pattern was identifiable. Variable names (beta, gamma, theta, eta) were garbled to various ASCII characters and have been reconstructed from context. -->

> *[Figure 2 -- not extractable from PDF]*

An easy calculation shows that $\theta = \Theta(\alpha^{-4/11})$ and so, each of the small shaded right triangles on the border of $R$ has area $O(\alpha^{-4/11})$.<!-- GARBLED: unable to reconstruct --> The total area of the triangles is therefore <!-- GARBLED: unable to reconstruct -->.

There are, in addition, two right trapezoids $T$ with base $\beta$ and vertical sides $D$ and $D'$ which have not been covered up to this point. We next describe how to pack $T$.

Let $m = [\alpha^{4/11}]$. Starting from the right-hand side of $T$, partition $T$ into as many right trapezoids $T_1, T_2, \ldots, T_r$ as possible, where the base of each $T_k$ is $m$ (see Fig. 3).

> *[Figure 3 -- not extractable from PDF]*

Thus, $r = \Theta(\alpha^{4/11})$ and $X'$ has area <!-- GARBLED: unable to reconstruct -->. If the vertical sides of $T_k$ are $\eta_k$ and $\eta_{k+1}$, let $h_k = [\eta_k - \alpha^{2/11}]$.<!-- GARBLED: the formula for h_k was partially garbled; reconstructed from identifiable pattern -->

Pack the bottom subrectangle $R(m, h_k)$ of $T_k$ with $m h_k$ unit squares in the natural way (as shown in Fig. 4) and let $T'_k$ denote the remaining uncovered subtrapezoid of $T_k$.

> *[Figure 4 -- not extractable from PDF]*

Now, for $s_k = [\eta_k] - h_k$, pack $T'_k$ with rectangles $R(1, s_k + 1)$ as shown in Fig. 4. Here, each $R(1, s_k + 1)$ touches both the top and bottom edges of $T'_k$ as well as the adjacent $R(1, s_k + 1)$'s. As before, the uncovered border right triangles on $T'_k$ have total area <!-- GARBLED: unable to reconstruct -->. The total area of the triangular regions between adjacent $R(1, s_k + 1)$'s is also <!-- GARBLED: unable to reconstruct --> since the sum of the angles at the top vertices is $\Theta(\alpha^{-1/11})$. Finally, the uncovered triangle $X'$ has area <!-- GARBLED: unable to reconstruct -->.

Since $r = \Theta(\alpha^{4/11})$<!-- GARBLED: bound on total uncovered area in T was garbled --> then the total uncovered area in $T$ is <!-- GARBLED: unable to reconstruct -->.

Hence the total uncovered area of $S(\alpha)$ is just $\Theta(\alpha^{7/11})$ and the theorem is proved. $\square$

The previously mentioned assertion that

$$f(k^2 + ck^{7/11}) > 4k$$

follows immediately. It is rather annoying that we do not at present have any nontrivial lower estimate for $w(\alpha)$. Indeed we cannot even rule out the possibility that $w(\alpha) = O(1)$. Perhaps the correct bound is $O(\alpha^{1/2})$.

In the same spirit the following questions can be asked. Let $\mathcal{C}$ be a closed convex curve of circumference 1. Inscribe $k$ non-overlapping curves in $\mathcal{C}$ which are all similar to $\mathcal{C}$. Denote by $f(\mathcal{C}, k)$ the maximum of the sum of the circumferences of these curves. If $\mathcal{C}$ is a parallelogram or a triangle then clearly $f(\mathcal{C}, j^2) = j$.<!-- GARBLED: the raw extraction rendered this as "f(C, j^2) = 1" but the value must be j by the scaling argument in the next sentence --> All that is needed is that $\mathcal{C}$ can be covered with $j^2$ copies of $\mathcal{C}$. We do not know for which figures other cases of exact coverings are possible for other values of $k$ although for every $k$, there are $\mathcal{C}$'s which have an exact covering into $k$ parts, e.g., a rectangle. The following questions can be posed: For which $\mathcal{C}$ is the growth of $f(\mathcal{C}, k)$ the slowest? Could this $\mathcal{C}$ be a circle? Which $\mathcal{C}$ permit exact coverings? Which $\mathcal{C}$ permit exact coverings with congruent curves similar to $\mathcal{C}$? For such $\mathcal{C}$, let $1 < n_1 < n_2 < \ldots$ be the integers for which such an exact covering is possible. What can be said about these sequences? For example, can $n_k = o(k^2)$?

## References

[1] A. Beck and M. N. Bleicher, Packing convex sets into a similar set, *Acta Math. Acad. Sci. Hungar.* 22 (1972) 283-303.

[2] D. J. Newman (personal communication).
