---
title: "Counterexamples to Wegner's Conjecture for Rectangles"
authors:
  - Deepak Ajwani
  - Rishikesh Gajjala
  - Rajiv Raman
  - Saurabh Ray
affiliations:
  - "University College Dublin, Ireland"
  - "Center for Quantum and Topological Systems, New York University Abu Dhabi, UAE"
  - "Indraprastha Institute of Information Technology Delhi, India"
  - "New York University Abu Dhabi, UAE"
arxiv: "2606.17854v2"
subject: "cs.CG"
date: "9 Jul 2026"
source_file: "wegner-counterexamples-rectangles.pdf"
---

# Counterexamples to Wegner's Conjecture for Rectangles

**Deepak Ajwani**, **Rishikesh Gajjala**, **Rajiv Raman**, **Saurabh Ray**

## Abstract

Wegner conjectured in 1965 that every finite family $\mathcal{R}$ of axis-parallel rectangles satisfies $\tau(\mathcal{R}) \leq 2\nu(\mathcal{R}) - 1$, where $\tau(\mathcal{R})$ is the minimum number of piercing points and $\nu(\mathcal{R})$ is the maximum size of a pairwise-disjoint subfamily. We disprove the conjecture by an explicit triangle-free family of 64 rectangles with $\nu = 16$ and $\tau \geq 32$.

More generally, for every $\varepsilon > 0$, we construct triangle-free rectangle families for which the standard clique-LP relaxation for maximum independent set of rectangles has integrality gap at least $5/2 - \varepsilon$. The same families satisfy $\tau(\mathcal{R}) \geq (5/2 - \varepsilon)\nu(\mathcal{R})$. We also prove that, on triangle-free rectangle families, this LP has gap at most 3. Our approach gives an example with axis-parallel segments instead of rectangles with integrality gap tending to 2. We also give a relatively small 4092-rectangle triangle-free family with chromatic number 6 improving the construction of Asplund and Grunbaum (On a coloring problem, Mathematica Scandinavica, 1960) that required more than $10^8$ rectangles.

## 1 Introduction

For a finite family $\mathcal{R}$ of axis-parallel rectangles in the plane, let $\nu(\mathcal{R})$ be the largest size of a pairwise-disjoint subfamily and let $\tau(\mathcal{R})$ be the minimum number of points that pierce all rectangles. Wegner's conjecture [27] asserts the inequality

$$\tau(\mathcal{R}) \leq 2\nu(\mathcal{R}) - 1. \tag{1}$$

It is clear that $\tau(\mathcal{R}) \geq \nu(\mathcal{R})$. In one dimension, i.e., for intervals, the analogous packing-piercing relation is exact: $\tau = \nu$. In two dimensions, i.e., for rectangles, there is a gap between $\tau$ and $\nu$. For example, for a family of rectangles whose intersection graph is a 5-cycle, $\tau = 3$, while $\nu = 2$.

Bounding transversal numbers in terms of packing numbers is well-studied in Discrete Geometry and Graph Theory [21, 4]. Gyarfas and Lehel [18] developed and surveyed such covering and coloring questions for geometric set systems related to intervals, including box graphs and multiple-interval systems, and asked for linear packing-piercing bounds in several of these settings. Karolyi [19] improved earlier general bounds for piercing rectangle families with no $k + 1$ pairwise-disjoint members to an $O(k \log k)$ bound, and Karolyi and Tardos [20] further connected the rectangle problem with point covers for multiple intervals. Fon-Der-Flaass and Kostochka [13] studied the corresponding problem for boxes in higher dimension, giving dimension-dependent transversal bounds. The authors also exhibit a planar rectangle family with $\tau = 5$ and $\nu = 3$, showing that the ratio $\tau/\nu$ can be as large as $5/3$.

Aronov, Ezra, and Sharir [2] proved $\varepsilon$-nets of size $O((1/\varepsilon) \log \log(1/\varepsilon))$ for the Hitting Set problem for axis-parallel rectangles along with related bounds for boxes. Their results hold even when the hitting set must be chosen from a discrete set of points. This implies an integrality gap of $O(\log \log \text{OPT})$ for the LP-relaxation of this problem and also yields a polynomial time $O(\log \log \text{OPT})$-approximation algorithm. Pach and Tardos [23] showed a lower bound of $\Omega((1/\varepsilon) \log \log(1/\varepsilon))$ for discrete $\varepsilon$-nets, and hence a lower bound of $\Omega(\log \log \text{OPT})$ for the natural LP-relaxation of the Hitting Set problem in the discrete setting. This line of work also gives the best general upper bound currently known, $\tau = O(\nu (\log \log \nu)^2)$. Correa, Feuilloley, Perez-Lantero, and Soto [12] studied independent and hitting sets for the structured case of rectangles intersecting a diagonal line. Among other results, they report a construction for which the ratio $\tau/\nu$ is arbitrarily close to 2. However, their example does not violate Wegner's conjecture.

Chudnovsky, Spirkl, and Zerbib [10] obtained piercing results for special families of axis-parallel boxes. Chen and Dumitrescu [9] showed that Wegner's proposed bound, if true, could not be strengthened at $\nu = 4$ by constructing examples with $\nu = 4$ and $\tau = 7$. Tomon [26] showed that for boxes in dimension $d \geq 3$, $\tau$ is not bounded by any linear function of $\nu$. In particular, he showed families with $\tau = \Omega\left(\nu (\log \nu / \log \log \nu)^{d-2}\right)$.

A very closely related problem is the maximum independent set of rectangles (MISR): given a rectangle family, find the largest pairwise-disjoint subfamily. Fowler, Paterson, and Tanimoto [14] proved that this problem and the corresponding covering problem are NP-complete. Chalermsook and Chuzhoy [7] gave a polynomial time $O(\log \log n)$-approximation by rounding the LP relaxation and constructed instances with asymptotic integrality gap $3/2$ for the standard clique-LP relaxation. Chalermsook [6] also gave a simpler $O(\log \log n)$-approximation. Adamaszek and Wiese [1] gave a quasi-polynomial-time approximation scheme (QPTAS) for the weighted problem, and Chuzhoy and Ene [11] obtained an asymptotically faster QPTAS. Mitchell [22] gave the first polynomial-time constant-factor approximation for unweighted MISR that was improved by Galvez, Khan, Mari, Momke, Pittu, and Wiese [15] to a 3-approximation[^1]. For the special case of axis-parallel segments, Caoduro, Cslovjecsek, Pilipczuk, and Wegrzycki [5] proved essentially tight bounds showing that the integrality gap of the LP relaxation approaches 2.

[^1]: There is an unpublished version on arXiv which claims to improve the approximation factor to $2 + \varepsilon$ [16].

Our constructions are related to and inspired by Asplund and Grunbaum [3] who proved that triangle-free rectangle intersection graphs are 6-colorable and gave a tight example. They also conjecture that for any rectangle intersection graph, the chromatic number $\chi$ is bounded above by $O(\omega)$ where $\omega$ is the size of a maximum clique in the graph. They also show that $\chi = O(\omega^2)$. Chalermsook and Walczak [8] improved the bound to $O(\omega \log \omega)$. The study on graph classes where the chromatic number is upper bounded by a function of the clique number was initiated by Gyarfas [17] (see also [25] for a recent survey on progress in this area). Such graphs are called $\chi$-bounded. Prominently, in this direction, Erdos conjectured that the intersection graphs of segments in the plane are $\chi$-bounded. This was disproved by Pawlik, Kozik, Krawczyk, Lason, Micek, Trotter and Walczak [24] showing that there exist triangle-free intersection graphs of segments with chromatic number $\Omega(\log \log n)$, where $n$ is the number of segments.

### 1.1 Our contribution

Our first contribution is an explicit counterexample to Wegner's conjecture. The instance has 64 rectangles arranged as a $4 \times 4$ grid of eight-rectangle gadgets. It is triangle-free, has $\nu = 16$, and satisfies $\tau \geq 32$; hence

$$\tau \geq 32 > 31 = 2\nu - 1.$$

The same family has clique-LP value at least 32 and integral optimum 16, so it already gives an integrality gap of 2. This shows that the "$-1$" in Wegner's conjecture does not hold. Our main result is stronger, namely that even the factor "2" is incorrect.

**Theorem 1.1.** *For every $\varepsilon > 0$, there is a triangle-free family of axis-parallel rectangles for which the standard LP relaxation with clique constraints for the MISR problem has integrality gap at least $5/2 - \varepsilon$. As a consequence, the same family satisfies $\tau(\mathcal{R}) \geq (5/2 - \varepsilon)\nu(\mathcal{R})$.*

This improves the previous rectangle lower bound for the integrality gap from $2 - o(1)$ [12, 5] to $5/2 - o(1)$. Since the constructed families are triangle-free, no point can pierce three rectangles.

The main gadget we use is called a *package*. This is a modification of the notion of a "filter-bed" used by Asplund and Grunbaum [3]. The only change is that a certain coloring property satisfied by filter-beds relevant for the coloring problem studied in their paper has been replaced by a property more suitable for bounding the sizes of independent sets.

We complement Theorem 1.1 by showing that for triangle-free rectangle families the LP solution can be rounded within a factor 3.

**Theorem 1.2** (Weighted LP-relative 3-approximation). *Let $\mathcal{R}$ be a triangle-free family of axis-parallel rectangles, and let $w : \mathcal{R} \to \mathbb{R}_{\geq 0}$ be nonnegative weights. There is an LP-rounding algorithm that returns an independent set $I \subseteq \mathcal{R}$ with*

$$w(I) \geq \frac{\text{OPT}^w_{\text{LP}}(\mathcal{R})}{3},$$

*where $\text{OPT}^w_{\text{LP}}(\mathcal{R})$ is the optimum value of the weighted clique-LP relaxation. In particular, the weighted integrality gap of the clique-LP on triangle-free rectangle instances is at most 3.*

Thus, for triangle-free rectangle families, integrality gap of the standard clique-LP lies between 5/2 and 3. In particular, any example with gap larger than 3 cannot be triangle-free. The package viewpoint also gives a concise alternate construction yielding the known integrality gap of nearly 2 for axis-parallel segments [5].

**Theorem 1.3** (Segments). *For every integer $k \geq 2$, there is a triangle-free family of $2k(2k - 1)$ axis-parallel segments whose clique-LP has an integrality gap of at least $2 - 1/k$.*

Finally, we show a filter-bed construction which can replace the filter-bed in the construction of Asplund and Grunbaum [3] improving the size of the constructed family significantly. Asplund and Grunbaum described a construction using $12 \cdot (8^8 + 8^7 + \cdots + 8^0) \approx 2.3 \times 10^8$ rectangles and mentioned that they have a "complicated" example with "only" 50000 rectangles, and explicitly ask if a smaller family exists. Our filter-bed plugged into their construction yields a family of size $12 \cdot (4^4 + 4^3 + \cdots + 4^0) = 4092$.

**Theorem 1.4** (Chromatic number). *There is a triangle-free family of 4092 rectangles with chromatic number 6.*

**Paper organization.** Section 2 fixes notation, introduces the clique-LP, and defines packages. Section 3 presents the 64-rectangle counterexample to Wegner's conjecture. Section 4 proves Theorem 1.1 and the LP-relative 3-approximation for triangle-free rectangle families. Section 5 gives the construction of a triangle-free segment family with integrality gap $2 - \varepsilon$ for any $\varepsilon > 0$. Section 6 gives the construction of a triangle-free rectangle family with 4092 rectangles and chromatic number 6. Section 7 lists open problems.

## 2 Preliminaries

All rectangles in this paper are closed axis-parallel rectangles. For a rectangle $R$, write $I_x(R)$ and $I_y(R)$ for its projections on the $x$- and $y$-axes. Rectangle $R_1$ *crosses* rectangle $R_2$ *horizontally* if $I_x(R_2) \subsetneq I_x(R_1)$ and $I_y(R_1) \subsetneq I_y(R_2)$. It crosses $R_2$ *vertically* if $I_x(R_1) \subsetneq I_x(R_2)$ and $I_y(R_2) \subsetneq I_y(R_1)$. We say simply that two rectangles *cross* if one of these two alternatives holds.

The intersection graph $G(\mathcal{R})$ of a rectangle family $\mathcal{R}$ has vertex set $\mathcal{R}$ and an edge between two rectangles iff they intersect. An independent set in $G(\mathcal{R})$ is a pairwise-disjoint subfamily of $\mathcal{R}$. Note that $\nu(\mathcal{R}) = \alpha(G(\mathcal{R}))$.

Axis-parallel rectangles satisfy the Helly property: if a finite subfamily is pairwise intersecting, then all rectangles in the subfamily share a common point. Therefore cliques in $G(\mathcal{R})$ are exactly subfamilies pierced by one point, and the clique constraints for MISR are equivalent to point-depth constraints. We use the LP

$$\text{maximize} \sum_{R \in \mathcal{R}} x_R,$$
$$\text{subject to} \sum_{R \in C} x_R \leq 1 \text{ for every clique } C \text{ of } G(\mathcal{R}), \tag{2}$$
$$0 \leq x_R \leq 1 \text{ for every } R \in \mathcal{R}.$$

This is the standard LP relaxation with clique constraints. For $N$ rectangles, it has an $O(N^2)$ size explicit representation. We need one constraint for each cell in the arrangement of the rectangles which can be efficiently enumerated by a sweep-line algorithm.

If $G(\mathcal{R})$ is triangle-free, every clique has size at most two, and hence $x_R = 1/2$ for every $R$ is feasible for the LP. Thus $\text{LP}(\mathcal{R}) \geq |\mathcal{R}|/2$ whenever $G(\mathcal{R})$ is triangle-free. The same observation gives a piercing lower bound: in a triangle-free rectangle family, no point lies in three rectangles, so every piercing point hits at most two rectangles and therefore $\tau(\mathcal{R}) \geq |\mathcal{R}|/2$.

We now define the main gadget in our constructions called a *package*. It is inspired by the "filter-bed" construction of Asplund and Grunbaum [3].

**Definition 2.1** (Horizontal packages). A *horizontal $(n, k)$-package* consists of a bounding rectangle $\Omega$, called its *container*, a family $\mathcal{R}$ of $n$ rectangles contained in $\Omega$, and $k$ pairwise-disjoint vertical slabs $\Pi_1, \ldots, \Pi_k \subseteq \Omega$, called *ports*. A rectangle *crosses* port $\Pi_j$ if it horizontally crosses $\Pi_j$. For $R \in \mathcal{R}$, let $\sigma(R) = \{j : R \text{ crosses } \Pi_j\}$. The following five properties are required.

(P0) For every $R \in \mathcal{R}$ and every $j \in [k]$, either $R$ crosses $\Pi_j$ or $R \cap \Pi_j = \emptyset$.

(P1) Every rectangle crosses at least one port.

(P2) For each port $\Pi_j$, the rectangles crossing $\Pi_j$ are pairwise disjoint.

(P3) The intersection graph $G(\mathcal{R})$ is triangle-free.

(P4) For every $Y \subseteq [k]$, if $R[Y] = \{R \in \mathcal{R} : \sigma(R) \subseteq Y\}$, then $\alpha(R[Y]) \leq |Y|$.

If a rectangle $R$ in the package crosses a port $\Pi$ of the package, we say that $R$ *uses* the port $\Pi$. We call the set of ports used by a rectangle its *port set*.

A *vertical $(n, k)$-package* is obtained by a $90°$ clockwise rotation of a horizontal package. In this case the ports are horizontal slabs in the container, and rectangles in the package cross the ports vertically.

## 3 A 64-rectangle counterexample

In this section, we construct a relatively small collection of rectangles which violate Wegner's conjecture. We generalize the construction in the next section where we also prove things more formally. The main gadget we use is the horizontal $(8, 4)$-package shown in Figure 1 and its vertical version obtained by a clockwise $90°$ rotation. The shaded vertical slabs in Figure 1 are the four ports. The formal coordinate construction of the package appears as the case $m = 2$ of the general construction in Section 4. This is a simplified version of the "filter-bed" construction of Asplund and Grunbaum [3].

> *[Figure 1: A horizontal $(8, 4)$-package. The intersection graph is $C_5 \mathbin{\dot{\cup}} K_2 \mathbin{\dot{\cup}} K_1$. -- not extractable from PDF]*

> *[Figure 2: The $4 \times 4$ grid composition. Shaded rectangles denote the ports. -- not extractable from PDF]*

It is easy to visually check that properties (P0), (P1), (P2) and (P3) in Definition 2.1 are satisfied. To verify Property (P4), we do a case analysis based on the size of the set $Y$ of allowed ports. If no port is allowed, i.e., $|Y| = 0$, clearly $|R[Y]| = 0$ as well. If $|Y| = 1$, depending on which port is allowed, $R[Y]$ contains exactly one of $A$, $B$, $C$ or $D$ and thus has size 1. Suppose now that $|Y| = 2$. If $Y = \{\Pi_1, \Pi_2\}$ the available rectangles are $A$, $B$, $P$, with $A$ intersecting $B$. The case for $Y = \{\Pi_3, \Pi_4\}$ is symmetric. For $Y = \{\Pi_2, \Pi_3\}$ the available rectangles are $B$, $C$ and $E$. However, $B$ and $C$ are adjacent, and hence the independent set size is 2. For the remaining three two-port choices, the set of available rectangles has size 2 and therefore has independence number at most 2. Suppose now that three ports are allowed i.e., exactly one port is blocked. If $\Pi_1$ or $\Pi_4$ are blocked, the intersection graph of the available rectangles consists of a four-vertex path along with an isolated vertex -- which has an independence number of 3. If $\Pi_2$ or $\Pi_3$ are blocked, the intersection graph has four vertices of which two are adjacent -- which also has an independence number of 3. Finally, if $|Y| = 4$ i.e., all four ports allowed, all rectangles in the package are available and their intersection graph is $C_5 \mathbin{\dot{\cup}} K_2 \mathbin{\dot{\cup}} K_1$, whose independence number is $2 + 1 + 1 = 4$. Thus the largest independent set using only $t$ of the four ports has size at most $t$.

We now construct a grid using scaled and translated copies of this package. We take four horizontal copies $H_1, \ldots, H_4$ and four vertical rotated copies $V_1, \ldots, V_4$ and place them so that, for every pair $(i, j) \in \{1, 2, 3, 4\}^2$, port $j$ of $H_i$ horizontally crosses the container of $V_j$ and port $i$ of $V_j$ vertically crosses the container of $H_i$. Figure 2 shows the construction. For simplicity, we only show the containers of the packages and not the rectangles inside them.

The resulting family has $4 \cdot 8 + 4 \cdot 8 = 64$ rectangles. Note that for each pair $(i, j)$, all rectangles using port $j$ of $H_i$ intersect all rectangles using port $i$ of $V_j$ and these are the only intersections between rectangles from distinct packages. Property (P2) ensures that the intersection graph of the family of 64 rectangles is triangle-free which means that for this family $\tau \geq 64/2 = 32$. Next, note that for any pair $(i, j)$ any independent set of the rectangles cannot contain a rectangle using port $j$ in $H_i$ as well as a rectangle using port $i$ in $V_j$ as any two such rectangles intersect. Thus, an independent set can either use port $j$ of $H_i$ or port $i$ of $V_j$ but not both. Thus, over all 8 packages, the total number of ports used is at most 16. By property (P4) of packages, for this family of rectangles $\nu \leq 16$. Conversely, each horizontal $(8, 4)$-package contains the independent set $\{U, P, A, C\}$ of size 4; taking such a set in each of the four horizontal packages (and no vertical-package rectangles) gives an independent set of size 16, since distinct horizontal packages have disjoint containers. Hence $\nu = 16$.

Thus we have $\tau > 2\nu - 1$ contradicting Wegner's conjecture. The same instance also has LP value at least $64/2 = 32$ and integral optimum of 16, so its integrality gap is 2. A more formal version of the above intuitive proof appears in Theorem 4.1.

## 4 Instances with larger integrality gap

We now generalize the idea in Section 3 so that the integrality gap of the LP approaches $5/2$. The argument in the grid proof remains unchanged; what changes is the package construction so that the rectangles to port ratio approaches $5/2$. We first prove that this ratio is the integrality gap we obtain from the grid construction.

**Theorem 4.1** (Grid composition). *Given a horizontal $(n, k)$-package, we can build a triangle-free family $F$ of $2nk$ rectangles with $\alpha(F) \leq k^2$ and $\tau(F) \geq nk$. This implies that the integrality gap of the LP for the MISR problem with clique constraints is at least $n/k$.*

*Proof.* Let $\mathcal{P}$ be the given $(n, k)$-horizontal package and let $\mathcal{P}^{\perp}$ be the vertical package obtained by a clockwise $90°$ rotation of $\mathcal{P}$. Place $k$ horizontal copies $H_1, \ldots, H_k$ of $\mathcal{P}$ with disjoint containers stacked vertically, and $k$ vertical copies $V_1, \ldots, V_k$ with disjoint containers placed side by side. Scale and translate the copies so that, for every $(i, j) \in \{1, 2, \ldots, k\}^2$, port $j$ of $H_i$ horizontally crosses port $i$ of $V_j$. Note that this forces the $x$-range of the container of $V_j$ to be a proper subset of the $x$-range of the port $j$ in $H_i$ and similarly the $y$-range of the container of $H_i$ must be a proper subset of the $y$-range of the port $i$ in $V_j$. By Property (P0), since each rectangle either crosses a port or is disjoint from it, this has two implications: i) all rectangles using port $j$ in $H_i$ intersect all rectangles using port $i$ in $V_j$ and ii) these are the only intersections among rectangles belonging to distinct packages -- the remaining intersections are between rectangles within a package. Let $F$ denote the set of all rectangles in all the packages. Since there are $2k$ packages with $n$ rectangles each, $|F| = 2nk$.

We next observe that $F$ is triangle-free. To see this note that by property (P3) of packages, the rectangles within a single package do not form a triangle. Since the distinct rectangles belonging to distinct horizontal packages do not intersect and similarly rectangles belonging to distinct vertical packages do not intersect, any triangle in the intersection graph must involve two rectangles from a horizontal package $H_i$ and one from a vertical package $V_j$ or vice-versa (two from $V_j$ and one from $H_i$). Assume that two of the rectangles belong to $H_i$, the other case being analogous. This leads to a contradiction since the only rectangles in $H_i$ that may intersect rectangles in $V_j$ are those that use the port $j$ of $H_i$ and rectangles in a package which use the same port must be pairwise disjoint by property (P2) of packages.

Next, we show that any independent set $I \subseteq F$ has size at most $k^2$. For each horizontal package $H_i$, let $Y_i^H$ be the set of ports of $H_i$ used by rectangles of $I \cap H_i$. By property (P4) of Definition 2.1, $|I \cap H_i| \leq |Y_i^H|$. Similarly, for each vertical package $V_j$, $|I \cap V_j| \leq |Y_j^V|$ where $Y_j^V$ denotes the set of ports of $V_j$ used by rectangles of $I \cap V_j$. For every pair $(i, j) \in \{1, 2, \ldots, k\}^2$, we cannot have both $j \in Y_i^H$ and $i \in Y_j^V$, since any rectangle in $H_i$ using port $j$ intersects any rectangle in $V_j$ using port $i$. Thus, the total number of used ports over all packages is at most the number of cells: $\sum_i |Y_i^H| + \sum_j |Y_j^V| \leq k^2$. Consequently $|I| \leq \sum_i |Y_i^H| + \sum_j |Y_j^V| \leq k^2$.

Since $F$ is a triangle-free family, any point in the plane pierces at most two rectangles, implying that $\tau(F) \geq |F|/2 = nk$. Also the uniform vector $x_R = 1/2$ is feasible for the LP with clique constraints and has value $nk$, while the integral optimum, as argued above, is at most $k^2$. The integrality gap is therefore at least $nk/k^2 = n/k$. $\square$

**Package construction.** We now construct $(n, k)$-packages with $n/k$ approaching $5/2$ for large $k$. The idea is to use disjoint vertically separated copies of five-cycles. Each $C_5$ contributes five rectangles but only two units of "independent-set capacity". The horizontal extents of the rectangles within each five-cycle are chosen carefully so that, even after many cycles are stacked together, the package still satisfies the port-restricted bound (P4). All other package properties are nearly immediate from the construction.

Fix an integer $m \geq 2$ and set $k = 2m$. The package has $k$ ports and $n = 5m - 2$ rectangles. Its container is $\Omega_m = [0, 8m + 3] \times [0, 5m]$, and its ports are $\Pi_j = [4j - 1, 4j] \times [0, 5m]$ for $j = 1, \ldots, 2m$. For a nonempty consecutive interval $[a, b] \subseteq [2m]$, define $X[a, b] = [4a - 3, 4b + 2]$. A rectangle with horizontal span $X[a, b]$ crosses exactly the ports $\Pi_a, \Pi_{a+1}, \ldots, \Pi_b$ and is separated by a positive gap from every other port. The package contains the following rectangles: three initial rectangles $U$, $P$, $Q$ along with five rectangles $A_i$, $B_i$, $C_i$, $D_i$, $E_i$ for each $i = 1, \ldots, m - 1$. The $x$- and $y$-ranges of the rectangles are shown in the table below.

| rectangle | $x$-range | $y$-range |
|-----------|-----------|-----------|
| $U$ | $X[1, 2m]$ | $[1, 2]$ |
| $P$ | $X[1, m]$ | $[3, 4]$ |
| $Q$ | $X[m+1, 2m]$ | $[3, 4]$ |
| $A_i$ | $X[i, i]$ | $[5i+1, 5i+4]$ |
| $B_i$ | $X[i+1, m]$ | $[5i+3, 5i+4]$ |
| $C_i$ | $X[m+1, m+i]$ | $[5i+3, 5i+4]$ |
| $D_i$ | $X[m+i+1, 2m]$ | $[5i+1, 5i+4]$ |
| $E_i$ | $X[i+1, m+i]$ | $[5i+1, 5i+2]$ |

Note that $n = 5(m - 1) + 3$, $k = 2m$ and $n/k = 5/2 - 2/k$. The intersection graph of the rectangles has the following connected components each placed in a disjoint horizontal band: the isolated vertex $U$, the edge $P - Q$ and a 5-cycle $A_i - B_i - C_i - D_i - E_i - A_i$ for each $i = 1, \ldots, m - 1$. This can be easily verified from the coordinates in the above table. Figure 3 shows the constructions for $m = 4$.

> *[Figure 3: The case $m = 4$ of the general construction: the horizontal $(18, 8)$-package. -- not extractable from PDF]*

**Proposition 4.2.** *For every $m \geq 2$, the construction above is a horizontal $(5m - 2, 2m)$-package.*

*Proof.* Every rectangle with an $x$-range $X[a, b]$ crosses exactly $\Pi_a, \ldots, \Pi_b$ and is disjoint from the other ports; this gives (P0). Every listed port interval is nonempty, so every rectangle crosses at least one port satisfying property (P1). Property (P3) is satisfied since the intersection graph is $(m - 1)C_5 \mathbin{\dot{\cup}} K_2 \mathbin{\dot{\cup}} K_1$ which is triangle-free. Property (P2) is also easy to verify. Fix a port $\Pi_j$. Rectangles belonging to different 5-cycles lie in vertically disjoint bands. Also $U$ and $P$, $Q$ lie in bands of their own disjoint from others. Inside one 5-cycle, the only pairs of rectangles sharing a port are $(B_i, E_i)$ and $(C_i, E_i)$, and both pairs are vertically disjoint. Thus all rectangles crossing any fixed port are pairwise disjoint. It remains to check the property (P4). First take a consecutive block of ports $J = [r, s] \subseteq [2m]$, and let $R(J)$ be the rectangles whose port set is contained in $J$. If $s < m$, only singleton rectangles $A_i$ can lie in $J$, so $\alpha(R(J)) \leq |J|$.

Assume $m \leq s < 2m$. If $r > m + 1$, $J$ does not contain the port set of any rectangle. Otherwise, the part of the $i$-th cycle contained in $J$ has independence number at most $\mathbf{1}_{\{i \geq r-1\}} + \mathbf{1}_{\{i \leq s-m\}}$. The first term accounts for the possible left side $(A_i, B_i)$, and the second for the possible middle-right side $(C_i, E_i)$; no $D_i$ is present because $s < 2m$. Summing over $i$ and adding the possible rectangle $P$ when $r = 1$, we get $\alpha(R(J)) \leq (m - 1) + (s - m) + 1 = s$ if $r = 1$, and $\alpha(R(J)) \leq (m - r + 1) + (s - m) = s - r + 1$ if $2 \leq r \leq m + 1$. Thus $\alpha(R(J)) \leq |J|$.

Finally let $s = 2m$. If $r > m + 1$, only suffix rectangles $D_i$ can appear, so there are at most $2m - r + 1 = |J|$ of them. If $r \leq m + 1$, then the $i$th cycle contributes at most $1 + \mathbf{1}_{\{i \geq r-1\}}$: one unit for the right side $(C_i, D_i)$, and a second unit only when the left side $(A_i, B_i, E_i)$ is also available. The rectangles in $\{U, P, Q\}$ contribute 2 when $r = 1$ since the independence number of $\{U, P, Q\}$ is 2, and contribute 1 when $2 \leq r \leq m + 1$, because only $Q$ is available. Hence $\alpha(R(J)) \leq (m - 1) + (m - 1) + 2 = 2m$ if $r = 1$, and $\alpha(R(J)) \leq (m - 1) + (m - r + 1) + 1 = 2m - r + 1$ if $2 \leq r \leq m + 1$. Again $\alpha(R(J)) \leq |J|$.

For an arbitrary set of ports $Y \subseteq [2m]$, decompose $Y$ into maximal consecutive blocks $J_1, \ldots, J_q$. Any rectangle whose port set is contained in $Y$ has port set contained in one of these blocks. Rectangles assigned to different blocks have disjoint $x$-projections, because a missing port separates the blocks. Therefore the independence numbers add, and $\alpha(R[Y]) = \sum_h \alpha(R(J_h)) \leq \sum_h |J_h| = |Y|$. This proves (P4). $\square$

Combining Theorem 4.1 with Proposition 4.2, and using $n = 5m - 2$ and $k = 2m$, we get an integrality gap of $n/k = 5/2 - 1/m$. This proves Theorem 1.1.

**Theorem 1.1.** *For every $\varepsilon > 0$, there is a triangle-free family of axis-parallel rectangles for which the standard LP relaxation with clique constraints for the MISR problem has integrality gap at least $5/2 - \varepsilon$. As a consequence, the same family satisfies $\tau(\mathcal{R}) \geq (5/2 - \varepsilon)\nu(\mathcal{R})$.*

**Corollary 4.3.** *For every $\delta > 0$, there is a triangle-free family of rectangles so that the integrality gap of the standard LP-relaxation for the vertex cover problem is at least $\frac{8}{5} - \delta$.*

*Proof.* The LP-relaxation of the vertex cover problem for any family $\mathcal{R}$ of rectangles is:

$$\min_{\{x_R : R \in \mathcal{R}\}} \left\{ \sum_{R \in \mathcal{R}} x_R : x_A + x_B \geq 1, \forall \{A, B\} \in G(\mathcal{R}),\; x_R \geq 0 \right\}.$$

Setting $x_R = 1/2$ for all $R \in \mathcal{R}$ yields a feasible solution with objective value $|\mathcal{R}|/2$. The proof of Theorem 1.1 constructs a triangle-free family of $n$ rectangles such that the maximum independent set has size at most $\frac{n}{2(5/2 - \varepsilon)} = \frac{n}{5 - 2\varepsilon}$ for any $\varepsilon > 0$. In the same family the vertex cover therefore has size at least $\text{OPT} := n - \frac{n}{5 - 2\varepsilon} = \frac{4 - 2\varepsilon}{5 - 2\varepsilon} n$, while the optimal solution to the vertex cover LP is at most $n/2$, since $x_R = 1/2$ for all $R$ is feasible. The integrality gap is therefore $\frac{(4 - 2\varepsilon)n/(5 - 2\varepsilon)}{n/2} = \frac{8 - 4\varepsilon}{5 - 2\varepsilon} \geq \frac{8}{5} - \delta$ for sufficiently small $\varepsilon$. $\square$

We next show that the integrality gap of triangle-free rectangle families cannot be more than 3. In fact, we show that this upper bound holds even for the weighted problem of computing a maximum weight independent set. Thus to obtain significantly larger integrality gap, one needs to explore families with larger max-clique sizes. For a family of rectangles $\mathcal{R}$, let $\text{OPT}^w_{\text{LP}}(\mathcal{R})$ denote the optimal solution value of the LP relaxation (2) for the maximum independent set problem on $\mathcal{R}$.

**Theorem 1.2** (Weighted LP-relative 3-approximation). *Let $\mathcal{R}$ be a triangle-free family of axis-parallel rectangles, and let $w : \mathcal{R} \to \mathbb{R}_{\geq 0}$ be nonnegative weights. There is an LP-rounding algorithm that returns an independent set $I \subseteq \mathcal{R}$ with*

$$w(I) \geq \frac{\text{OPT}^w_{\text{LP}}(\mathcal{R})}{3},$$

*where $\text{OPT}^w_{\text{LP}}(\mathcal{R})$ is the optimum value of the weighted clique-LP relaxation. In particular, the weighted integrality gap of the clique-LP on triangle-free rectangle instances is at most 3.*

*Proof.* Let $x^*$ be an optimal solution to the weighted clique-LP, that is obtained from LP-relaxation (2) by replacing the objective function by $\sum_{R \in \mathcal{R}} w_R x_R$. Then,

$$\text{OPT}^w_{\text{LP}} = \sum_{R \in \mathcal{R}} w_R x^*_R.$$

Compute a 6-coloring $\mathcal{R}_1, \ldots, \mathcal{R}_6$ of the triangle-free rectangle intersection graph -- the proof of Asplund and Grunbaum that triangle-free rectangle intersection graphs are 6-colorable directly yields a polynomial time algorithm [3]. For each color class, define

$$\mu_i = \sum_{R \in \mathcal{R}_i} w_R x^*_R.$$

Since each color appears in exactly five of the $\binom{6}{2} = 15$ pairs of colors, there is a pair $i < j$ such that

$$\mu_i + \mu_j \geq \frac{1}{15} \sum_{i < j} (\mu_i + \mu_j) = \frac{5}{15} \sum_{i=1}^{6} \mu_i = \frac{\text{OPT}^w_{\text{LP}}}{3}.$$

Let $\mathcal{R}' = \mathcal{R}_i \cup \mathcal{R}_j$. The graph $G[\mathcal{R}']$ is bipartite. Consider the weighted stable-set LP on $G[\mathcal{R}']$:

$$\max \sum_{R \in \mathcal{R}'} w_R y_R \quad \text{s.t.} \quad y_R + y_S \leq 1 \text{ for every edge } RS \in E(G[\mathcal{R}']), \quad 0 \leq y_R \leq 1.$$

The restriction of $x^*$ to $\mathcal{R}'$ is feasible and has value $\mu_i + \mu_j$. Since $G[\mathcal{R}']$ is bipartite, this LP is integral. Therefore it has an integral optimum, which is an independent set of weight at least $\frac{1}{3} \text{OPT}^w_{\text{LP}}$. $\square$

## 5 Integrality gap for axis-parallel segments

We now give an alternate construction which yields the same integrality-gap lower bound for axis-parallel segments as in [5]. It is interesting to note that the construction is similar to that in [5] but arrived at from a different perspective. By Theorem 4.1, it suffices to construct a package of horizontal segments whose segments to ports ratio tends to 2. Fix $k \geq 2$. For each $i = 1, \ldots, k - 1$, take two horizontal segments $L_i$ and $R_i$ with $\sigma(L_i) = \{1, \ldots, i\}$ and $\sigma(R_i) = \{i + 1, \ldots, k\}$. Place $L_i$ and $R_i$ on the line $y = i$ so that they intersect in the gap between the ports $\Pi_i$ and $\Pi_{i+1}$. Finally add one more segment $U$ on the line $y = 0$ with $\sigma(U) = \{1, \ldots, k\}$. Thus the package has $2k - 1$ segments. Figure 4 shows the construction for $k = 5$.

> *[Figure 4: A $(9, 5)$-package formed by horizontal segments. -- not extractable from PDF]*

Properties (P0), (P1), (P2) and (P3) of packages hold by construction and are easy to check. Property (P4) holds trivially when $Y = \emptyset$. It is also easy to verify when $Y$ contains all $k$ ports: any independent set may contain $U$ and at most one segment from each pair $(L_i, R_i)$ for $i = 1, \ldots, k - 1$ and thus has size at most $k$. Assume now that $Y$ is non-empty but does not contain all ports. In this case $U \notin R[Y]$. Let $r \geq 0$ be the largest number so that $Y$ contains the first $r$ ports and similarly let $s \geq 0$ be the largest number so that $Y$ contains the last $s$ ports. Since we assumed that $Y$ does not contain all ports, $r + s < k$ and therefore $|Y| \geq r + s$. In this case, note that $R[Y]$ contains exactly the first $r$ segments in $L_1, \ldots, L_{k-1}$ and the last $s$ segments in $R_1, \ldots, R_{k-1}$ and therefore has size exactly $r + s$. This implies that property (P4) holds: $\alpha(R[Y]) \leq |R[Y]| = r + s \leq |Y|$.

Applying the grid composition of Theorem 4.1 to this package yields the following.

**Theorem 1.3** (Segments). *For every integer $k \geq 2$, there is a triangle-free family of $2k(2k - 1)$ axis-parallel segments whose clique-LP has an integrality gap of at least $2 - 1/k$.*

For comparison, the family obtained in [5] has size $4k^2$ with integrality gap $\frac{2k^2}{k^2 + 3k - 2} = 2 - 6/k + O(1/k^2)$. So, for the same integrality gap, our construction is slightly smaller.

## 6 Smaller triangle-free family with chromatic number 6

Asplund and Grunbaum [3] proved that the chromatic number of any triangle-free family of axis-parallel rectangles is at most 6. They also showed that this is tight by constructing a triangle-free family of $12 \cdot (8^8 + 8^7 + \cdots + 8^0) / (8 - 1) \approx 2.3 \times 10^8$ rectangles whose proper coloring requires 6 colors. The main gadget they used is a "filter-bed" which is simply a package (as defined in Definition 2.1) with the property (P4) replaced by the following coloring property (P4'): for any proper 5-coloring of rectangles in the package, the rectangles using one of the ports have at least 3 different colors. Asplund and Grunbaum [3] use the filter-bed to construct a family of rectangles, with a combination of a hierarchical tree-like structure and a grid structure to force any proper coloring of the family to use at least 6 colors. Asplund and Grunbaum remark that they found another construction which was "quite complicated" but has only about 50000 rectangles. They however did not describe the construction. We improve on their bound by simply replacing the filter-bed in their construction by the new filter-bed shown in Figure 5. This immediately reduces the number of rectangles in the construction to $12 \cdot (4^4 + 4^3 + 4^2 + 4^1 + 4^0) / (4 - 1) = 4092$. It only remains to prove that the filter-bed in Figure 5 satisfies the required properties.

> *[Figure 5: Modified filter-bed with 12 rectangles and 4 ports. -- not extractable from PDF]*

**Proposition 6.1.** *The gadget shown in Figure 5 satisfies properties (P0), (P1), (P2), (P3) of packages as well as the coloring property (P4').*

*Proof.* Properties (P0), (P1), (P2) and (P3) are immediate from visual inspection. It remains to prove the coloring property.

Suppose, for a contradiction, that there is a proper 5-coloring in which every port sees at most two colors. Since $T$ uses all four ports, the color of $T$ appears on every port; call this color 0. This implies that for each port $j$, the colors seen by the port are contained in $S_j := \{0, s_j\}$ for some $s_j \neq 0$. If a rectangle uses the interval of ports $[a, b]$, then its color lies in $S_a \cap \ldots \cap S_b$. Thus such a rectangle has color 0, unless $s_a = s_{a+1} = \ldots = s_b$, in which case the only possible nonzero color is this common value.

Let $P$ denote the event $s_1 = s_2$, and let $Q$ denote the event $s_3 = s_4$. We first show that $P$ and $Q$ cannot both hold. Consider the 5-cycle $A - E - H - J - F - A$, and write $p = s_1 = s_2$ and $q = s_3 = s_4$. If $p = q$, then all vertices of this odd cycle have colors in $\{0, p\}$, impossible in a proper coloring. If $p \neq q$, then $F$ is forced to have color 0. Hence its neighbors $A$ and $J$ are forced to have colors $p$ and $q$, respectively. Then $E$ is forced to have color 0 because it is adjacent to $A$, and $H$ is forced to have color 0 because it is adjacent to $J$. This contradicts the proper coloring of the edge $EH$.

Next, $P$ and $Q$ cannot both fail. If $P$ fails, then $B$ is forced to have color 0. If $Q$ fails, then $I$ is forced to have color 0. This contradicts the edge $BI$. Hence exactly one of $P$ and $Q$ holds.

Suppose first that $P$ holds and $Q$ fails. Since $Q$ fails, $I$ is forced to have color 0. The edge $IL$ forces $L$ to have the nonzero color $s_2 = s_1$. The edge $LK$ then forces $K$ to have color 0. The edge $KG$ forces $G$ to have a nonzero color, but $G$ uses ports 2, 3, 4 and $s_3 \neq s_4$, so $G$ is forced to have color 0, a contradiction.

Finally suppose that $Q$ holds and $P$ fails. Since $P$ fails, $B$ is forced to have color 0. The edge $BH$ forces $H$ to have the nonzero color $s_3$. Also, $C$ uses ports 1, 2, 3 and $s_1 \neq s_2$, so $C$ is forced to have color 0. The edge $CJ$ forces $J$ to have the nonzero color $s_4$. But $Q$ says $s_3 = s_4$, contradicting the proper coloring of the edge $HJ$. This proves the proposition. $\square$

As mentioned before, using the construction of Asplund and Grunbaum with their filter-bed replaced by the gadget in Figure 5, we get the following. The proof below is an adaptation of the proof of Asplund and Grunbaum [3] with only minor changes.

**Theorem 1.4** (Chromatic number). *There is a triangle-free family of 4092 rectangles with chromatic number 6.*

*Proof.* Asplund and Grunbaum [3] showed that every triangle-free rectangle family is 6-colorable. It is therefore enough to construct a triangle-free family which is not 5-colorable. The construction idea is exactly the same as the one used in [3] with a slight change in the way we describe it.

The family has a hierarchical structure mimicking a complete rooted 4-ary tree $T$ with depth 4. At depth $d \in \{0, 1, 2, 3, 4\}$, there are $4^d$ nodes. The internal nodes in the tree correspond to horizontal filter-beds (defined analogously to horizontal packages) and the leaves correspond to vertical filter-beds (again defined analogously to vertical packages). For any node $N$ in the tree, denote the filter-bed corresponding to $N$ as $\text{filter-bed}(N)$ and its container as $\text{container}(N)$. We place these packages so that the following conditions are satisfied:

1. The containers of all filter-beds corresponding to nodes in $T$ at the same depth have the same $y$-range and disjoint $x$-ranges.

2. For any non-root node $C$ and its parent $P$, if $C$ is $i$th child of $P$ then the $x$-range of $\text{container}(C)$ is contained in the $x$-range of the $i$th port $\Pi_i$ of $\text{filter-bed}(P)$.

3. For any leaf $L$ in $T$, the $y$-range of the port $\Pi_i$ of $\text{filter-bed}(L)$ contains the $y$-range of internal nodes at depth $i - 1$ for all $i \in \{1, 2, 3, 4\}$.

It is easy to see that there is a placement satisfying the above constraints (see [3] for details). First note that the total number of rectangles in the construction is 12 times the number of nodes in the tree since each node corresponds to a filter-bed with 12 rectangles. This is $12 \cdot (1 + 4 + 4^2 + 4^3 + 4^4) = 4092$.

We first check that the constructed family is triangle-free. Each filter-bed is clearly triangle-free. Distinct filter-beds at the same depth have disjoint $x$-ranges, and horizontal filter-beds at different internal depths have disjoint $y$-ranges, so those pairs are disjoint. A leaf (vertical) filter-bed can meet a horizontal filter-bed only when the latter lies on that leaf's root-to-leaf path, and by (P0) such intersections occur only through the corresponding pair of ports. Since rectangles using a fixed port are pairwise disjoint (P2), no triangle can use rectangles from two different filter-beds. Hence the whole family is triangle-free.

We now claim that the intersection graph of the rectangles in the construction above is not 5-colorable. For contradiction assume that there is a 5-coloring. By property (P4') for every package in the construction, there is one port so that the rectangles using that port use at least 3 colors -- we call such a port *tricolored*. The main idea is to show that there exists a pair $(H, V)$ where $H$ is a horizontal filter-bed and $V$ is a vertical filter-bed such that a tricolored port $p$ of $H$ horizontally crosses a tricolored port $q$ of $V$. Then, all rectangles using $p$ in $H$ intersect all rectangles using $q$ in $V$ and thus they together must use 6 colors, contradicting the 5-colorability assumption. Now, note that there exists a root to leaf path $v_1 - v_2 - v_3 - v_4 - v_5$ so that for any $i \in \{1, 2, 3, 4\}$ if $v_{i+1}$ is the $j$th child of $v_i$ then the $j$th port of $\text{filter-bed}(v_i)$ is tricolored. Now consider $\text{filter-bed}(v_5)$ which is vertical and note that its $k$th port is crossed by a tricolored port of $v_k$. Since one of the ports of $v_5$ must be tricolored, we obtain the pair $(H, V)$ with the desired properties. The proof follows. $\square$

## 7 Conclusion and open problems

We have given a simple construction that disproves Wegner's conjecture and shows that the standard LP relaxation with clique constraints for MISR has integrality gap at least $5/2 - \varepsilon$ for every $\varepsilon > 0$. Several questions remain open.

- What is the true supremum of $\tau(\mathcal{R})/\nu(\mathcal{R})$ for axis-parallel rectangle families $\mathcal{R}$?

- What is the exact integrality gap of the LP for MISR?

- Is there a finite package with rectangles to port ratio exactly $5/2$ or larger?

## Acknowledgements

Constructions of the initial counterexamples relied heavily on trial and error. OpenAI's GPT-5.5 Pro was used extensively to search for suitable constructions, often by generating code for these searches and for auxiliary verification in Lean. Once promising constructions emerged, the authors distilled the ideas into clear, concise, human-readable proofs. The authors also used integer programs generated by GPT-5.5 Pro to verify optimality of the constructions; however, the correctness of the proofs does not rely on these auxiliary verifications. OpenAI Codex was also used for drawing the figures and for initial drafts of several portions of the text. Anthropic's Claude Pro was used to identify typographical errors. All mathematical proofs and the final text were reviewed and rewritten by the authors.

## References

[1] Anna Adamaszek and Andreas Wiese. Approximation schemes for maximum weight independent set of rectangles. In *Proceedings of the 54th IEEE Annual Symposium on Foundations of Computer Science (FOCS)*, pages 400--409. IEEE Computer Society, 2013.

[2] Boris Aronov, Esther Ezra, and Micha Sharir. Small-size $\epsilon$-nets for axis-parallel rectangles and boxes. *SIAM Journal on Computing*, 39(7):3248--3282, 2010.

[3] Edgar Asplund and Branko Grunbaum. On a coloring problem. *Mathematica Scandinavica*, 8:181--188, 1960.

[4] Claude Berge. *Hypergraphs: Combinatorics of Finite Sets*, volume 45 of *North-Holland Mathematical Library*. North-Holland, Amsterdam, 1989.

[5] Marco Caoduro, Jana Cslovjecsek, Michal Pilipczuk, and Karol Wegrzycki. On the independence number of intersection graphs of axis-parallel segments. *Journal of Computational Geometry*, 14(1):144--156, 2023.

[6] Parinya Chalermsook. Coloring and maximum independent set of rectangles. In Leslie Ann Goldberg, Klaus Jansen, R. Ravi, and Jose D. P. Rolim, editors, *Approximation, Randomization, and Combinatorial Optimization. Algorithms and Techniques -- 14th International Workshop, APPROX 2011, and 15th International Workshop, RANDOM 2011, Princeton, NJ, USA, August 17--19, 2011. Proceedings*, volume 6845 of *Lecture Notes in Computer Science*, pages 123--134. Springer, 2011.

[7] Parinya Chalermsook and Julia Chuzhoy. Maximum independent set of rectangles. In *Proceedings of the Twentieth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA)*, pages 892--901. SIAM, 2009.

[8] Parinya Chalermsook and Bartosz Walczak. Coloring and maximum weight independent set of rectangles. In Daniel Marx, editor, *Proceedings of the 2021 ACM-SIAM Symposium on Discrete Algorithms, SODA 2021, Virtual Conference, January 10--13, 2021*, pages 860--868. SIAM, 2021.

[9] Ke Chen and Adrian Dumitrescu. On Wegner's inequality for axis-parallel rectangles. *Discrete Mathematics*, 343(12):112091, 2020.

[10] Maria Chudnovsky, Sophie Spirkl, and Shira Zerbib. Piercing axis-parallel boxes. *The Electronic Journal of Combinatorics*, 25(1):P1.70, 2018.

[11] Julia Chuzhoy and Alina Ene. On approximating maximum independent set of rectangles. In *Proceedings of the 57th IEEE Annual Symposium on Foundations of Computer Science (FOCS)*, pages 820--829. IEEE Computer Society, 2016.

[12] Jose R. Correa, Laurent Feuilloley, Pablo Perez-Lantero, and Jose A. Soto. Independent and hitting sets of rectangles intersecting a diagonal line: Algorithms and complexity. *Discrete & Computational Geometry*, 53(2):344--365, 2015.

[13] Dmitry G. Fon-Der-Flaass and Alexandr V. Kostochka. Covering boxes by points. *Discrete Mathematics*, 120(1--3):269--275, 1993.

[14] Robert J. Fowler, Michael S. Paterson, and Steven L. Tanimoto. Optimal packing and covering in the plane are NP-complete. *Information Processing Letters*, 12(3):133--137, 1981.

[15] Waldo Galvez, Arindam Khan, Mathieu Mari, Tobias Momke, Madhusudhan Reddy Pittu, and Andreas Wiese. A 3-approximation algorithm for maximum independent set of rectangles. In *Proceedings of the 2022 ACM-SIAM Symposium on Discrete Algorithms (SODA)*, pages 894--905. SIAM, 2022.

[16] Waldo Galvez, Arindam Khan, Mathieu Mari, Tobias Momke, Madhusudhan Reddy, and Andreas Wiese. A $(2+\epsilon)$-approximation algorithm for maximum independent set of rectangles. *CoRR*, abs/2106.00623, 2021.

[17] Andras Gyarfas. Problems from the world surrounding perfect graphs. *Applicationes Mathematicae*, 19(3--4):413--441, 1987.

[18] Andras Gyarfas and Jeno Lehel. Covering and coloring problems for relatives of intervals. *Discrete Mathematics*, 55(2):167--180, 1985.

[19] Gyula Karolyi. On point covers of parallel rectangles. *Periodica Mathematica Hungarica*, 23(2):105--107, 1991.

[20] Gyula Karolyi and Gabor Tardos. On point covers of multiple intervals and axis-parallel rectangles. *Combinatorica*, 16(2):213--222, 1996.

[21] Jiri Matousek. *Lectures on Discrete Geometry*, volume 212 of *Graduate Texts in Mathematics*. Springer, New York, 2002.

[22] Joseph S. B. Mitchell. Approximating maximum independent set for rectangles in the plane. In *Proceedings of the 62nd IEEE Annual Symposium on Foundations of Computer Science (FOCS)*, pages 339--350. IEEE Computer Society, 2021.

[23] Janos Pach and Gabor Tardos. Tight lower bounds for the size of epsilon-nets. *Journal of the American Mathematical Society*, 26(3):645--658, 2013.

[24] Arkadiusz Pawlik, Jakub Kozik, Tomasz Krawczyk, Michal Lason, Piotr Micek, William T. Trotter, and Bartosz Walczak. Triangle-free intersection graphs of line segments with large chromatic number. *Journal of Combinatorial Theory, Series B*, 105:6--10, 2014.

[25] Alex Scott and Paul Seymour. A survey of $\chi$-boundedness. *Journal of Graph Theory*, 95(3):473--504, 2020.

[26] Istvan Tomon. Lower bounds for piercing and coloring boxes. *Advances in Mathematics*, 435:109360, 2023.

[27] Gerd Wegner. Uber eine kombinatorisch-geometrische Frage von Hadwiger und Debrunner. *Israel Journal of Mathematics*, 3:187--198, 1965.
