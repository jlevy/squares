---
title: "Compactness Theorems for Geometric Packings"
authors:
  - Greg Martin
affiliations:
  - "Department of Mathematics, University of Toronto, Canada M5S 3G3"
arxiv: "math/0005054"
subject: "math.MG"
msc: "52C17 (52C15, 54H99)"
date: "2000"
source_file: "martin-2000-compactness-theorems-geometric-packings.pdf"
---

# Compactness Theorems for Geometric Packings

**Greg Martin**

## Abstract

Moser asked whether the collection of rectangles of dimensions $1 \times \frac{1}{2}$, $\frac{1}{2} \times \frac{1}{3}$, $\frac{1}{3} \times \frac{1}{4}$, ..., whose total area equals 1, can be packed into the unit square without overlap, and whether the collection of squares of side lengths $\frac{1}{2}$, $\frac{1}{3}$, $\frac{1}{4}$, ... can be packed without overlap into a rectangle of area $\frac{\pi^2}{6} - 1$. Computational investigations have been made into packing these collections into squares of side length $1 + \varepsilon$ and rectangles of area $\frac{\pi^2}{6} - 1 + \varepsilon$, respectively, and one can consider the apparently weaker question of whether such packings are possible for every positive number $\varepsilon$. In this paper we establish a general theorem on sequences of geometrical packings that implies, in particular, that the "for every $\varepsilon$" versions of these two problems are actually equivalent to the original tiling problems.

## 1. Introduction

Given a collection $\mathcal{A} = \{A_1, A_2, \ldots\}$ of subsets of $\mathbb{R}^n$, a *packing* of $\mathcal{A}$ into another set $C \subset \mathbb{R}^n$ is a way of fitting each of the sets $A_i$ inside $C$ without overlap. By a *positioning* of a set $A_i$ we mean the image of $A_i$ under a rigid motion of $\mathbb{R}^n$, i.e., some combination of translations, rotations, and reflections. To avoid ambiguity about points on the boundaries of the $A_i$, we say more precisely that these positionings of the $A_i$ must be contained inside $C$ and that their interiors must be pairwise disjoint. One can also speak of *oriented packings*, where the sets $A_i$ may be translated and rotated but not reflected, and also *translated packings*, where the $A_i$ may be translated but neither rotated nor reflected. We also refer to a translated packing as a *parallel packing*, particularly when each set $A_i$ is a *brick* (a product $[x_1, y_1] \times \cdots \times [x_n, y_n]$ of closed intervals). If the union of the repositioned sets $A_i$ is all of $C$, we call the packing a *tiling* of $C$.

It is often difficult to determine whether a particular collection $\mathcal{A}$ can be packed into some target set $C$. One representative example is the collection $\mathcal{A} = \{A_1, A_2, \ldots\}$ where each $A_i$ is a rectangle of dimensions $\frac{1}{i} \times \frac{1}{i+1}$. Since the total area of these rectangles is 1, it is conceivable that $\mathcal{A}$ can tile a unit square (generally or even with a parallel tiling); but this problem, first posed by Moser (see [3] and [2, Section D5]), is unsolved. One can instead ask the apparently weaker question of whether for every positive number $\varepsilon$, the collection $\mathcal{A}$ can be packed inside a square of side length $1 + \varepsilon$ (see for example [1]). A similar situation holds with the collection $\mathcal{A} = \{S_2, S_3, \ldots\}$ where each $S_i$ is a square of side length $\frac{1}{i}$. Conceivably this collection will tile a rectangle of area $\frac{\pi^2}{6} - 1$ (and perhaps even one with dimensions $(\frac{\pi^2}{6} - 1) \times 1$), but it is even unknown whether for every positive number $\varepsilon$ the collection $\mathcal{A}$ can be packed into rectangles with area $\frac{\pi^2}{6} - 1 + \varepsilon$. For both these problems, results of Paulhus [5] shows that $\varepsilon$ can at least be taken smaller than $10^{-9}$.

The purpose of this paper is to show that the weaker "for every $\varepsilon$" versions of these two packing problems are actually equivalent to the stronger tiling versions. Our methods apply in a somewhat more general setting, and we state the following two theorems as representative of what can be deduced. For the first theorem, we use the notation $\lambda C = \{\lambda y : y \in C\}$ for the homothetic expansion/dilation (or simply *homothet*) of $C$ by the constant factor $\lambda > 0$.

**Theorem 1.** *Let $\mathcal{A}$ be a collection of subsets of $\mathbb{R}^n$, and let $C$ be a compact subset of $\mathbb{R}^n$. If for every $\varepsilon > 0$ there exists a packing of $\mathcal{A}$ into the homothet $(1 + \varepsilon)C$, then there exists a packing of $\mathcal{A}$ into $C$ itself. In particular, if there exist packings of $\mathcal{A}$ into closed balls of radius $R + \varepsilon$ for every $\varepsilon > 0$, then there exists a packing of $\mathcal{A}$ into a closed ball of radius $R$. These statements remain true if "packing" is replaced by "oriented packing" or "translated packing".*

We remark that the collection $\mathcal{A}$ may have any cardinality. Of course, the hypothesis that the target set $C$ be compact is equivalent to $C$ being both closed and bounded; both of these conditions on $C$ are necessary. There are obvious counterexamples if $C$ is not required to be closed -- for example, we can take $C$ to be the open unit disk in $\mathbb{R}^2$ and $\mathcal{A}$ to be the collection consisting solely of $\overline{C}$, the closure of $C$. The theorem also fails if $C$ is closed but not bounded: for example, we can again take $\mathcal{A}$ to consist solely of the closed unit disk in $\mathbb{R}^2$, and $C$ to be the closed region $\{(x, y) : 1 \leq x, |y| \leq 1 - 1/x\}$.

**Theorem 2.** *Let $\mathcal{A}$ be a collection of subsets of $\mathbb{R}^n$. If there exist packings of $\mathcal{A}$ into bricks of volume $V + \varepsilon$ for every $\varepsilon > 0$, then there exists a packing of $\mathcal{A}$ into a brick of volume $V$. In fact a stronger statement is true: let $\{B_1, B_2, \ldots\}$ be a sequence of bricks in $\mathbb{R}^n$, with the dimensions of the $j$th brick $B_j$ being $b_{j1} \times \cdots \times b_{jn}$. Set $V = \inf_j\{\operatorname{vol} B_j\}$, and assume that $\operatorname{vol} B_j > V$ for every $j$. Suppose that there exists a packing of $\mathcal{A}$ into each brick $B_j$. Then there exists a packing of $\mathcal{A}$ into some brick $B$ with dimensions $b_1 \times \cdots \times b_n$, satisfying $\operatorname{vol} B = V$ and $b_m \leq \limsup_j\{b_{jm}\}$ for each $1 \leq m \leq n$. These statements remain true if "packing" is replaced by "oriented packing" or "translated packing".*

The equivalence of the weak and strong versions of the two packing problems mentioned in the introductory remarks follow as immediate corollaries of Theorem 2:

**Corollary 1.** *Let $\mathcal{A}$ be the collection of rectangles of dimensions $1 \times \frac{1}{2}$, $\frac{1}{2} \times \frac{1}{3}$, $\frac{1}{3} \times \frac{1}{4}$, $\frac{1}{4} \times \frac{1}{5}$, .... Suppose that for every $\varepsilon > 0$, the collection $\mathcal{A}$ can be packed into a square of area $1 + \varepsilon$. Then $\mathcal{A}$ tiles a square of area 1. If the given packings are parallel packings, then $\mathcal{A}$ parallel-tiles a square of area 1.*

**Corollary 2.** *Let $\mathcal{A}$ be the collection of squares of side lengths $\frac{1}{2}$, $\frac{1}{3}$, $\frac{1}{4}$, .... Suppose that for every $\varepsilon > 0$, the collection $\mathcal{A}$ can be packed into a rectangle of area $\frac{\pi^2}{6} - 1 + \varepsilon$. Then $\mathcal{A}$ tiles a rectangle of area $\frac{\pi^2}{6} - 1$. If the given packings are into rectangles of height 1, then $\mathcal{A}$ tiles a rectangle of dimensions $1 \times (\frac{\pi^2}{6} - 1)$. In either case, if the given packings are parallel packings, then $\mathcal{A}$ parallel-tiles the resulting rectangle of area $\frac{\pi^2}{6} - 1$.*

The aforementioned work of Paulhus [5] makes a convincing argument that the "for every $\varepsilon$" versions of these two packing questions have affirmative answers (since obstacles to finding rectangle tilings generally arise from the largest rectangles). In light of Corollaries 1 and 2, it therefore seems likely that tilings (indeed, parallel tilings) do exist in both cases.

As can be inferred from the title of this paper, the methods used to establish Theorems 1 and 2 are topological in nature. The intuitive idea is to convert a sequence of packings of the collection $\mathcal{A}$ in the hypothesized sets into a "limiting packing" of $\mathcal{A}$ into the desired target set. To this end, we will show how the set of packings of $\mathcal{A}$ can be naturally regarded as a topological space, and then use a compactness argument to show the existence of a "limiting packing" of some sort; it then remains to show that this packing is a valid packing into the type of set required by Theorem 1 or 2.

In Section 2 we set the notation to be used throughout this paper and exhibit simple properties of the defined objects that follow easily from elementary point-set topology. Section 3 contains the proofs of Theorems 1 and 2, modulo an important proposition whose proof will be deferred until Section 4 in order to clarify the issues involved in the proofs of the theorems themselves. In Section 5 we remark on some modified versions of Theorems 1 and 2 that can be proved using these methods, without going into the details of the proofs.

## 2. Notation and Basic Topological Facts

The methods that we use are valid for collections $\mathcal{A}$ of subsets of $\mathbb{R}^n$ of any cardinality, but for the sake of notational simplicity we work under the assumption that our collection $\mathcal{A} = \{A_1, A_2, \ldots\}$ is countably infinite. In addition, we argue throughout with the understanding that we are allowing translations, rotations, and reflections and thus permitting the most general kinds of packings; at the beginning of Section 5 we will explain how our arguments extend to the more restrictive classes of oriented packings and parallel packings.

For any subset $C$ of $\mathbb{R}^n$, we denote by $\mathcal{P}(\mathcal{A}, C)$ the set (possibly empty *a priori*) of all packings of $\mathcal{A}$ into $C$. We mention at the outset that translated copies of the target space $C$ are equivalent to each other for the purposes of deciding whether there exists a packing of $\mathcal{A}$ into $C$ -- indeed, there is a natural bijection between the set of packings of $\mathcal{A}$ into $C$ and the set of packings of $\mathcal{A}$ into some translated copy of $C$. Similarly, we may modify the collection $\mathcal{A}$ by replacing each set $A_i$ by any translated copy of $A_i$, and still retain in essence the same set $\mathcal{P}(\mathcal{A}, C)$. For instance, it will often be convenient for us to assume that each set $A_i$ contains the origin in $\mathbb{R}^n$. We also note that if $C$ is a subset of $D$ then certainly $\mathcal{P}(\mathcal{A}, C) \subset \mathcal{P}(\mathcal{A}, D)$.

Let $O(n)$ denote the $n$-dimensional orthogonal group, i.e., the set of all $n \times n$ matrices $\theta$ with real entries such that $\theta^{-1} = \theta^T$. Every rigid motion of $\mathbb{R}^n$ can be identified with an element of the product space $O(n) \times \mathbb{R}^n$ as follows: if $\sigma = (\theta, \xi)$ is an element of $O(n) \times \mathbb{R}^n$, then $\sigma$ acts on a point $x$ of $\mathbb{R}^n$ by the rule $\sigma(x) = \xi + \theta x$. (Throughout this paper we will maintain the notational conventions that elements of $O(n) \times \mathbb{R}^n$ will be denoted by $\sigma$ or $\tau$, and that $\theta$ and $\xi$ will denote the $O(n)$- and $\mathbb{R}^n$-components, respectively, when it is necessary to refer to these components separately.) Certainly these rigid motions $\sigma$ act on subsets $A$ of $\mathbb{R}^n$ as well, and we will write $\sigma(A) = \{\xi + \theta x : x \in A\}$ for the image. Any positioning of the set $A$ in $\mathbb{R}^n$, using translations, rotations, and/or reflections, can be realized as $\sigma(A)$ for some element $\sigma$ of $O(n) \times \mathbb{R}^n$.

Define the topological space $M(\mathbb{R}^n)$ to be the product space $(O(n) \times \mathbb{R}^n)^\infty$, and for any subset $D$ of $\mathbb{R}^n$ define the subspace $M(D) = (O(n) \times D)^\infty$ of $M(\mathbb{R}^n)$. Since every positioning of a set $A$ in $\mathbb{R}^n$ corresponds uniquely to an element $\sigma$ of $O(n) \times \mathbb{R}^n$, the space $M(\mathbb{R}^n)$ parametrizes all possible positionings of the collection $\mathcal{A}$ in $\mathbb{R}^n$, and certain positionings among these will correspond to packings of $\mathcal{A}$ into a target set $C$. More precisely, if $\operatorname{Int} A$ denotes the interior of $A$, we can write

$$\mathcal{P}(\mathcal{A}, C) = \left\{ S = \{\sigma_i\} \in M(\mathbb{R}^n) : \forall i,\; \sigma_i(A_i) \subset C;\; \forall i \neq j,\; \operatorname{Int}(\sigma_i(A_i)) \cap \operatorname{Int}(\sigma_j(A_j)) = \emptyset \right\}. \tag{1}$$

(In general we will let $S$ and $T$ denote elements of $M(\mathbb{R}^n)$ or of its subsets.) As a result, the set $\mathcal{P}(\mathcal{A}, C)$ can be given the subspace topology induced by the product topology on $M(\mathbb{R}^n)$. The key to the proof of Theorem 1 is to exploit this topological structure on $M(\mathbb{R}^n)$ to show that $\mathcal{P}(\mathcal{A}, C)$ is a nonempty subspace under the stated hypotheses, and the proof of Theorem 2 proceeds similarly after a suitable brick $B$ is chosen as the ultimate target set.

We now exhibit several facts, which follow from the definitions of the above notation together with elementary point-set topology, that will be useful to us later. As a final piece of notation, let

$$\Delta_r(x) = \{y \in \mathbb{R}^n : |y - x| < r\}$$

represent the open ball in $\mathbb{R}^n$ of radius $r$ and center $x$.

**Fact 1.** *For any element $\sigma$ of $O(n) \times \mathbb{R}^n$, any point $x$ of $\mathbb{R}^n$, and any positive number $r$, we have $\sigma(\Delta_r(x)) = \Delta_r(\sigma(x))$.*

This follows directly from the fact that the elements $\sigma$ of $O(n) \times \mathbb{R}^n$ correspond to rigid motions (isometries) of $\mathbb{R}^n$, i.e., $|\sigma(y) - \sigma(x)| = |y - x|$ for any points $x, y \in \mathbb{R}^n$.

**Fact 2.** *Each element $\sigma$ of $O(n) \times \mathbb{R}^n$ is a homeomorphism of $\mathbb{R}^n$ onto itself; in particular, $\sigma^{-1}$ is well-defined.*

Certainly $\sigma$, being an isometry, is continuous. Moreover, it is easy to see that if $\sigma = (\theta, \xi)$, then $\tau = (\theta^{-1}, -\theta^{-1}\xi)$ is an element of $O(n) \times \mathbb{R}^n$ which inverts the action of $\sigma$ on $\mathbb{R}^n$. Therefore $\sigma$ is continuously invertible as well, hence a homeomorphism.

**Fact 3.** *For any element $\sigma$ of $O(n) \times \mathbb{R}^n$ and any subset $A$ of $\mathbb{R}^n$, we have $\sigma(\operatorname{Int}(A)) = \operatorname{Int}(\sigma(A))$.*

This is an immediate consequence of the fact that $\sigma$ is a homeomorphism of $\mathbb{R}^n$.

**Fact 4.** *Let $D$ be a subset of $\mathbb{R}^n$, and let $\{x_n\}$ be a sequence of points of $\mathbb{R}^n$, all but finitely many of which belong to $D$. If $\{x_n\}$ converges to some point $x$, then $x \in \overline{D}$.*

**Fact 5.** *Every closed subset of a compact space is itself compact.*

**Fact 6.** *In a compact topological space, every sequence has a convergent subsequence.*

These three statements are simple consequences of elementary point-set topology; see for instance Munkres [4], Sections 2.10, 3.5, and 3.7, respectively.

**Fact 7.** *If $C$ is a compact subset of $\mathbb{R}^n$, then the space $M(C)$ is also compact.*

The orthogonal group $O(n)$ is compact (it is clearly bounded, since each column is a unit vector in $\mathbb{R}^n$ and hence each entry is at most 1 in absolute value; and it is closed since it is the preimage of the identity matrix under the continuous map $\theta \mapsto \theta^T \theta$). Since $M(C) = (O(n) \times C)^\infty$, Fact 7 therefore follows from Tychonov's theorem that arbitrary products of compact spaces are compact (see [4, Section 5.1]). The compactness of these spaces $M(C)$ is crucial to our proofs of Theorems 1 and 2.

**Fact 8.** *If $\mathcal{A} = \{A_1, A_2, \ldots\}$ is a collection of subsets of $\mathbb{R}^n$, each containing the origin, then $\mathcal{P}(\mathcal{A}, C)$ is a subset of $M(C)$.*

We can justify this fact as follows: if $0 \in A$ and $\sigma = (\theta, \xi)$, then $\xi = \xi + \theta(0) \in \sigma(A)$. Thus if $\sigma(A) \subset C$, we must have $\xi \in C$. Fact 8 then follows from the definition (1) of $\mathcal{P}(\mathcal{A}, C)$ by applying this reasoning to each image $\sigma_i(A_i)$.

**Fact 9.** *If $\mathcal{A} = \{A_1, A_2, \ldots\}$ and $\mathcal{C} = \{C_1, C_2, \ldots\}$ are collections of subsets of $\mathbb{R}^n$, then $\mathcal{P}(\mathcal{A}, \bigcap_{k=1}^{\infty} C_k) = \bigcap_{k=1}^{\infty} \mathcal{P}(\mathcal{A}, C_k)$.*

This follows immediately from unfolding the definitions of $\mathcal{P}(\mathcal{A}, \bigcap_{k=1}^{\infty} C_k)$ and $\bigcap_{k=1}^{\infty} \mathcal{P}(\mathcal{A}, C_k)$ using equation (1). In words, Fact 9 states that any packing of $\mathcal{A}$ into the set $\bigcap_{k=1}^{\infty} C_k$ is simultaneously a packing of $\mathcal{A}$ into each set $C_k$.

## 3. Proofs of Theorems 1 and 2

In this section we state the following crucial proposition from which we deduce Theorems 1 and 2:

**Proposition 1.** *Let $C$ be a closed subset of $\mathbb{R}^n$, and let $\mathcal{A}$ be any collection of subsets of $\mathbb{R}^n$. Then the space $\mathcal{P}(\mathcal{A}, C)$ is a closed subset of $M(\mathbb{R}^n)$.*

The proof of Proposition 1, while not tricky, is somewhat long-winded, and therefore we defer it to the next section. Assuming the validity of Proposition 1, we can establish Theorems 1 and 2 by means of the following lemma:

**Lemma 2.** *Let $\mathcal{A} = \{A_1, A_2, \ldots\}$ and $\mathcal{C} = \{C_1, C_2, \ldots\}$ be collections of subsets of $\mathbb{R}^n$. For each $k \geq 1$ define $D_k = \bigcup_{j=k}^{\infty} C_j$, and suppose that $D_1$ is bounded. If there exist packings of $\mathcal{A}$ into $C_j$ for each $j \geq 1$, then there exists a packing of $\mathcal{A}$ into the set $\bigcap_{k=1}^{\infty} \overline{D_k}$.*

The set $\bigcap_{k=1}^{\infty} \overline{D_k}$, which is simply the $\limsup$ of the sets $C_j$ (the set of all points that are contained in infinitely many of the $C_j$), can be compared to the related set $\bigcap_{k=1}^{\infty} \overline{D_k}$. In fact, $\bigcap_{k=1}^{\infty} \overline{D_k}$ is precisely the set of all points $x \in \mathbb{R}^n$ such that every neighborhood of $x$ intersects infinitely many of the $C_j$.

*Proof:* By translating the sets $A_i$ if necessary, we may assume that each $A_i$ contains the origin. By hypothesis, there exists a packing of $\mathcal{A}$ into each $C_j$, so we may choose

$$T_j \in \mathcal{P}(\mathcal{A}, C_j) \subset \mathcal{P}(\mathcal{A}, \overline{D_j}) \subset \mathcal{P}(\mathcal{A}, \overline{D_1})$$

for each $j \geq 1$. The set $\overline{D_1}$ is closed and bounded, hence compact, and so by Fact 7 the space $M(\overline{D_1})$ is also compact. Since the sets $A_i$ all contain the origin, the space $\mathcal{P}(\mathcal{A}, \overline{D_1})$ is contained in $M(\overline{D_1})$ by Fact 8; we know by Proposition 1 that $\mathcal{P}(\mathcal{A}, \overline{D_1})$ is a closed set, and so it is itself compact by Fact 5. Therefore by Fact 6, the sequence $\{T_j\}$ of points in $\mathcal{P}(\mathcal{A}, \overline{D_1})$ has a convergent subsequence. By replacing the sequence $\{T_j\}$ by this subsequence, we may assume that the $T_j$ converge to some element $T \in \mathcal{P}(\mathcal{A}, \overline{D_1})$.

It remains to show that this element $T$ in fact represents a packing of $\mathcal{A}$ into $\bigcap_{k=1}^{\infty} \overline{D_k}$. For each $k \geq 1$, the sequence $T_j$ is contained (except for at most the first $k - 1$ terms) in $\mathcal{P}(\mathcal{A}, \overline{D_k})$. Since this set is closed by Proposition 1, we see by Fact 4 that the limit $T$ is itself an element of $\mathcal{P}(\mathcal{A}, \overline{D_k})$. Because this is true for all $k \geq 1$, Fact 9 implies

$$T \in \bigcap_{k=1}^{\infty} \mathcal{P}(\mathcal{A}, \overline{D_k}) = \mathcal{P}\left(\mathcal{A}, \bigcap_{k=1}^{\infty} \overline{D_k}\right),$$

which establishes the lemma. $\square$

**Proof of Theorem 1:** Since $C$ is compact, it is contained in some ball of radius $R$ centered at the origin, and therefore each set $(1 + \frac{1}{j})C$ is contained in the ball of radius $2R$ around the origin. Therefore under the hypothesis that there exist packings of $\mathcal{A}$ into each set $(1 + \frac{1}{j})C$, we may apply Lemma 2 to conclude that there exists a packing of $\mathcal{A}$ into the set $\bigcap_{k=1}^{\infty} \overline{D_k}$, where we have put

$$D_k = \bigcup_{j=k}^{\infty} (1 + \tfrac{1}{j})C. \tag{2}$$

All that remains to establish the theorem is to show that $\bigcap_{k=1}^{\infty} \overline{D_k}$ is contained in $C$; in other words, we need to show that for every $x \notin C$, there exists some $k \geq 1$ such that $x \notin \overline{D_k}$.

If $x \notin C$ then, since $C$ is compact (hence closed), there exists a positive number $\varepsilon$ such that $\Delta_\varepsilon(x) \cap C = \emptyset$. We claim that

$$\text{for every } j > 2|x|\varepsilon^{-1}, \quad \Delta_{\varepsilon/2}(x) \cap (1 + \tfrac{1}{j})C = \emptyset. \tag{3}$$

To see this, suppose that there did exist a point $y$ in $\Delta_{\varepsilon/2}(x) \cap (1 + \frac{1}{j})C$. Since $y \in (1 + \frac{1}{j})C$, if we set $z = (1 + \frac{1}{j})^{-1}y$ then $z \in C$, and by our choice of $\varepsilon$ we therefore have $|x - z| \geq \varepsilon$. On the other hand, since $y \in \Delta_{\varepsilon/2}(x)$,

$$|x - z| \leq |x - y| + |y - z| < \frac{\varepsilon}{2} + |y - (1 + \tfrac{1}{j})^{-1}y| = \frac{\varepsilon}{2} + \frac{|y|}{j + 1}.$$

The fact that $y \in \Delta_{\varepsilon/2}(x)$ forces $|y| < |x| + \varepsilon/2$, and so

$$|x - z| < \frac{\varepsilon}{2} + \frac{|x| + \varepsilon/2}{j + 1} < \frac{\varepsilon}{2} + \frac{|x| + \varepsilon/2}{2|x|/\varepsilon + 1} = \varepsilon$$

by our choice of $j$. This contradiction establishes equation (3).

If we set $k = \lfloor 2|x|\varepsilon^{-1} \rfloor + 1$, we see from equation (3) and the definition (2) of $D_k$ that $\Delta_{\varepsilon/2}(x) \cap D_k = \emptyset$, which implies that $x \notin \overline{D_k}$ as desired. This establishes the theorem. $\square$

**Proof of Theorem 2:** First we make some reductions in the problem. By translating each set $A_i$ if necessary we may assume that each $A_i$ contains the origin. Similarly, by translating each brick $B_j$ if necessary, we may assume that each $B_j$ is contained in the positive orthant of $\mathbb{R}^n$ and has one vertex at the origin, that is, $B_j = [0, b_{j1}] \times \cdots \times [0, b_{jn}]$. Next, by passing to a suitable subsequence of the $B_j$, we may also assume that $\operatorname{vol} B_j$ decreases monotonically to $V$. At this point we make the assumption that the dimensions $b_{jm}$ of the bricks $B_j$ are bounded uniformly in $j$ and $m$; at the end of the proof we will show why this assumption is legitimate. By passing once again to a suitable subsequence of the $B_j$, we may therefore assume that for each $1 \leq m \leq n$ the sequence $\{b_{jm}\}$ converges to some number $b_m$, say.

Since the $b_{jm}$ are uniformly bounded, the sets $B_j$ are all contained in a single bounded region of $\mathbb{R}^n$, and thus we may apply Lemma 2 to conclude that there exists a packing of the set $\mathcal{A}$ into $\bigcap_{k=1}^{\infty} \overline{D_k}$, where we have put $D_k = \bigcup_{j=k}^{\infty} B_j$. The theorem will therefore be established if we can demonstrate that the intersection $\bigcap_{k=1}^{\infty} \overline{D_k}$ is contained in the brick $B = [0, b_1] \times \cdots \times [0, b_n]$. For any natural numbers $k$ and $m$ with $1 \leq m \leq n$, define $d_{km} = \sup_{j \geq k}\{b_{jm}\}$. Then for $j \geq k$ it is clear that $B_j$ is contained in the closed set $[0, d_{k1}] \times \cdots \times [0, d_{kn}]$, and so $\overline{D_k}$ is contained in the same closed set. Consequently,

$$\bigcap_{k=1}^{\infty} \overline{D_k} \subset \bigcap_{k=1}^{\infty} \left([0, d_{k1}] \times \cdots \times [0, d_{kn}]\right) = [0, \inf_k\{d_{k1}\}] \times \cdots \times [0, \inf_k\{d_{kn}\}]$$
$$= [0, \limsup_j\{b_{j1}\}] \times \cdots \times [0, \limsup_j\{b_{jn}\}] = [0, b_1] \times \cdots \times [0, b_n] = B.$$

This establishes the theorem, modulo the assumption that the $b_{jm}$ are uniformly bounded. This assumption does not hold for a general collection of bricks of bounded volume, as the simple example $[0, n] \times [0, 1/n]$ in $\mathbb{R}^2$ demonstrates. However, in the most natural case -- where at least one of the sets $A_i$ has nonempty interior -- we will be able to deduce from the existence of a packing of $\mathcal{A}$ into each brick $B_j$ that the $b_{jm}$ are uniformly bounded. In the contrary (less interesting) case, it will also be possible to reduce to the situation where the $b_{jm}$ are uniformly bounded by a somewhat different method.

**Case 1.** *At least one of the sets $A_i$ has nonempty interior.*

Choose an integer $k$ such that the set $A_k$ has nonempty interior, and then choose $\eta > 0$ such that $A_k$ contains some open ball of radius $\eta$. Since there exists a packing of $\mathcal{A}$ into each brick $B_j$, we see in particular that each $B_j$ contains some open ball of radius $\eta$. Certainly then the dimensions $b_{j1}, \ldots, b_{jn}$ of each brick $B_j$ must satisfy $b_{jm} \geq \eta$ for each $1 \leq m \leq n$, and so for each $j \geq 1$ and $1 \leq m \leq n$,

$$0 < b_{jm} = \frac{\operatorname{vol} B_j}{b_{j1} \cdots b_{j,m-1} \, b_{j,m+1} \cdots b_{jn}} \leq \frac{\operatorname{vol} B_1}{\eta^{n-1}},$$

since we have reduced to the case where the $\operatorname{vol} B_j$ are monotonically decreasing. This shows that the $b_{jm}$ are indeed uniformly bounded.

**Case 2.** *All of the $A_i$ have empty interiors.*

We claim that if there exists a packing of $\mathcal{A}$ into each brick $B_j = [0, b_{j1}] \times \cdots \times [0, b_{jn}]$, then there also exists a packing of $\mathcal{A}$ into the smaller brick $B'_j = [0, b'_{j1}] \times \cdots \times [0, b'_{jn}]$ where we have defined $b'_{jm} = \min\{b_{jm}, \operatorname{diam} B_1\}$. If we can justify this assertion, the theorem is established in this case as well since the $b'_{jm}$ are certainly uniformly bounded by $\operatorname{diam} B_1$.

For a collection $\mathcal{A}$ of sets with empty interiors, the packing condition that the positionings of the sets $A_i$ must have disjoint interiors is no condition at all; in other words, there exists a packing of the entire collection $\mathcal{A}$ into $C$ if and only if there exists individual positionings of each set $A_i$ into $C$. Moreover, we can modify any positioning $\sigma_i(A_i)$ into the brick $B_j$ so that it becomes a positioning of $A_i$ into $B'_j$, by taking the rotated/reflected set $\theta_i(A_i)$ and translating it just enough to lie in the positive orthant of $\mathbb{R}^n$. More precisely, if $\sigma_i = (\theta_i, \xi_i)$ is such that $\sigma_i(A_i) \subset B_j$, then we define $\sigma'_i = (\theta_i, \xi'_i)$ where the $m$th coordinate $\xi'_{im}$ of the vector $\xi'_i \in \mathbb{R}^n$ is given by

$$\xi'_{im} = -\inf\{t : t \in \pi_m(\theta_i(A_i))\};$$

here $\pi_m$ denotes the projection map in the $m$th coordinate from $\mathbb{R}^n$ to $\mathbb{R}$.

The fact that $\sigma'_i(A_i)$ is contained in the positive orthant of $\mathbb{R}^n$ follows immediately from the definition of the $\xi'_{im}$. Also, we are assuming that $A_i$ contains the origin, and so $\xi_i$ is an element of $\sigma_i(A_i)$; since $\sigma_i(A_i)$ is contained in the positive orthant, it follows that $\xi'_{im} \leq \xi_{im}$, and consequently $\sigma'_i(A_i)$ is contained in the brick $B_j$. Finally, since $A_i$ contains the origin it is clear that $\xi'_{im} \leq \operatorname{diam} A_i$, and since there exists a packing of $\mathcal{A}$ into $B_1$ we certainly have $\operatorname{diam} A_i \leq \operatorname{diam} B_1$. Therefore $\sigma'_i(A_i)$ is indeed contained in the brick $B'_j$.

Making this modification for each set $A_i$ results in a packing of the entire collection $\mathcal{A}$ into the smaller brick $B'_j$ (again, the assumption that the $A_i$ have empty interiors means that we do not need to worry about the relative positionings of the various $A_i$). As remarked earlier, this justifies the assumption that the dimensions of our bricks are uniformly bounded, since we may replace $B_j$ by $B'_j$ throughout.

This completes the proof of the theorem. $\square$

In summary, we have established Theorems 1 and 2 modulo a proof of Proposition 1; this proof will be the subject of the following section.

## 4. Proof of Proposition 1

Proposition 1 is essentially a consequence of the fact that the action on $\mathbb{R}^n$ of the space of rigid motions $O(n) \times \mathbb{R}^n$ is continuous. The following two lemmas, which give concrete statements of the continuity of this action, will enable us to establish Proposition 1. We note that the space $O(n) \times \mathbb{R}^n$ can in fact be regarded as a metric space, inheriting as it does the standard metric from $\mathbb{R}^{n^2} \times \mathbb{R}^n$: if $\sigma = (\theta, \xi)$ and $\sigma' = (\theta', \xi')$ are two elements of $O(n) \times \mathbb{R}^n$, then the distance between them is

$$d(\sigma', \sigma) = \left(|\theta' - \theta|^2 + |\xi' - \xi|^2\right)^{1/2} = \left(\sum_{l=1}^{n} \sum_{m=1}^{n} (\theta'_{lm} - \theta_{lm})^2 + \sum_{m=1}^{n} (\xi'_m - \xi_m)^2\right)^{1/2}, \tag{4}$$

considering $\theta$ and $\theta'$ here simply as $n^2$-tuples of real numbers rather than elements of $O(n)$.

**Lemma 3.** *Let $y$ be a point in $\mathbb{R}^n$ and $U$ be an open subset of $\mathbb{R}^n$. Suppose that $\sigma$ is an element of $O(n) \times \mathbb{R}^n$ such that $\sigma(y) \in U$. Then there exists a positive real number $\delta$ such that, for every $\sigma' \in O(n) \times \mathbb{R}^n$ satisfying $d(\sigma', \sigma) < \delta$, we have $\sigma'(y) \in U$.*

*Proof:* For any $y \in \mathbb{R}^n$ and any pair $\tau = (\theta, \xi)$, $\tau' = (\theta', \xi')$ of elements of $O(n) \times \mathbb{R}^n$, we have

$$|\tau(y) - \tau'(y)| = |\xi + \theta y - \xi' - \theta' y| \leq |\xi - \xi'| + |(\theta - \theta')y|. \tag{5}$$

We certainly have $|\xi - \xi'| \leq d(\tau, \tau')$ by the definition (4) of the metric $d$. On the other hand, all entries of the matrix $\theta - \theta'$ are also at most $d(\tau, \tau')$ in absolute value, while the entries of the vector $y$ are at most $|y|$ in absolute value. Therefore each entry of $(\theta - \theta')y$ is bounded by $n|y| d(\tau, \tau')$ in absolute value, and so the inequality (5) becomes the upper bound

$$|\tau(y) - \tau'(y)| \leq d(\tau, \tau') + \left(\sum_{m=1}^{n} \left(n|y| d(\tau, \tau')\right)^2\right)^{1/2} = (n^{3/2}|y| + 1) d(\tau, \tau') \tag{6}$$

(we have made no effort to obtain a strong constant in the inequality).

Now if $\sigma$ is an element of $O(n) \times \mathbb{R}^n$ such that $\sigma(y)$ lies in the open set $U$, then there exists some positive number $\varepsilon$ such that $\Delta_\varepsilon(\sigma(y)) \subset U$. If we set $\delta = \varepsilon(n^{3/2}|y| + 1)^{-1}$, then for any $\sigma' \in O(n) \times \mathbb{R}^n$ such that $d(\sigma', \sigma) < \delta$, the upper bound (6) tells us that

$$|\sigma'(y) - \sigma(y)| \leq (n^{3/2}|y| + 1) d(\sigma', \sigma) < \varepsilon,$$

and therefore $\sigma'(y) \in \Delta_\varepsilon(\sigma(y)) \subset U$ as desired. $\square$

**Lemma 4.** *Let $U_1$ and $U_2$ be open subsets of $\mathbb{R}^n$. Suppose that $\sigma_1$ and $\sigma_2$ are elements of $O(n) \times \mathbb{R}^n$ such that $\sigma_1(U_1) \cap \sigma_2(U_2) \neq \emptyset$. Then there exists a positive real number $\delta$ such that, for every $\sigma'_1, \sigma'_2 \in O(n) \times \mathbb{R}^n$ satisfying $d(\sigma'_1, \sigma_1) < \delta$ and $d(\sigma'_2, \sigma_2) < \delta$, we have $\sigma'_1(U_1) \cap \sigma'_2(U_2) \neq \emptyset$.*

*Proof:* Since $\sigma_1(U_1)$ and $\sigma_2(U_2)$ are open sets that are not disjoint, we can choose a point $x \in \mathbb{R}^n$ and a positive number $\varepsilon$ such that $\Delta_\varepsilon(x) \subset \sigma_1(U_1) \cap \sigma_2(U_2)$. Using Fact 2 we may set $y_1 = \sigma_1^{-1}(x)$ and $y_2 = \sigma_2^{-1}(x)$, so that $\Delta_\varepsilon(y_1) \subset U_1$ and $\Delta_\varepsilon(y_2) \subset U_2$; we also set

$$\delta = \frac{\varepsilon}{n^{3/2} \max\{|y_1|, |y_2|\} + 1}.$$

Then for $i = 1$ or $2$, for any $\sigma'_i \in O(n) \times \mathbb{R}^n$ such that $d(\sigma'_i, \sigma_i) < \delta$ the upper bound (6) tells us that

$$|\sigma'_i(y_i) - x| = |\sigma'_i(y_i) - \sigma_i(y_i)| \leq (n^{3/2}|y_i| + 1) d(\sigma'_i, \sigma_i) < \varepsilon,$$

so that $x \in \Delta_\varepsilon(\sigma'_i(y_i)) = \sigma'_i(\Delta_\varepsilon(y_i)) \subset \sigma'_i(U_i)$ by Fact 1. In particular, this shows that $x$ is an element of $\sigma'_1(U_1) \cap \sigma'_2(U_2)$, which is therefore nonempty as desired. $\square$

**Proof of Proposition 1:** Let $T = \{\tau_i\}$ be a point in $M(\mathbb{R}^n) \setminus \mathcal{P}(\mathcal{A}, C)$. From the definition (1) of $\mathcal{P}(\mathcal{A}, C)$, one of the following two cases must hold.

**Case 1.** *There exists a $k \geq 1$ such that $\tau_k(A_k) \not\subset C$.*

Choose a point $x \in \tau_k(A_k) \setminus C$, and set $y = \tau_k^{-1}(x) \in A_k$ (using Fact 2). Applying Lemma 3 with $\sigma = \tau_k$ and $U = \mathbb{R}^n \setminus C$, we see that there exists a positive number $\delta$ such that, for every $\sigma' \in O(n) \times \mathbb{R}^n$ satisfying $d(\sigma', \tau_k) < \delta$, we have $\sigma'(y) \in \mathbb{R}^n \setminus C$, that is, $\sigma'(y) \notin C$.

Now define the open neighborhood $\mathcal{S}$ of $T$ in $M(\mathbb{R}^n)$ by

$$\mathcal{S} = \left\{S = \{\sigma_i\} \in M(\mathbb{R}^n) : d(\sigma_k, \tau_k) < \delta\right\}.$$

For every $S \in \mathcal{S}$, we see that $\sigma_k(y) \notin C$ by our choice of $\delta$. On the other hand, certainly $\sigma_k(y) \in \sigma_k(A_k)$, and so $S$ is not a packing of $\mathcal{A}$ into $C$. Since this is true for any $S \in \mathcal{S}$, we see that $\mathcal{S} \subset M(\mathbb{R}^n) \setminus \mathcal{P}(\mathcal{A}, C)$.

**Case 2.** *There exist positive integers $k \neq l$ such that $\operatorname{Int}(\tau_k(A_k)) \cap \operatorname{Int}(\tau_l(A_l)) \neq \emptyset$.*

Applying Lemma 4 with $\sigma_1 = \tau_k$, $\sigma_2 = \tau_l$, $U_1 = \operatorname{Int}(A_k)$, and $U_2 = \operatorname{Int}(A_l)$, we see that there exists a positive real number $\delta$ such that, for every $\sigma'_1, \sigma'_2 \in O(n) \times \mathbb{R}^n$ satisfying $d(\sigma'_1, \tau_k) < \delta$ and $d(\sigma'_2, \tau_l) < \delta$, we have

$$\operatorname{Int}(\sigma'_1(A_k)) \cap \operatorname{Int}(\sigma'_2(A_l)) = \sigma'_1(\operatorname{Int}(A_k)) \cap \sigma'_2(\operatorname{Int}(A_l)) \neq \emptyset$$

(here we have used Fact 3). Now define the open neighborhood $\mathcal{S}$ of $T$ in $M(\mathbb{R}^n)$ by

$$\mathcal{S} = \left\{S = \{\sigma_i\} \in M(\mathbb{R}^n) : d(\sigma_k, \tau_k) < \delta \text{ and } d(\sigma_l, \tau_l) < \delta\right\}.$$

For every $S \in \mathcal{S}$, we see that $\operatorname{Int}(\sigma_k(A_k)) \cap \operatorname{Int}(\sigma_l(A_l)) \neq \emptyset$ by our choice of $\delta$, and so $S$ is not a packing of $\mathcal{A}$ with disjoint interiors. Since this is true for any $S \in \mathcal{S}$, we see that $\mathcal{S} \subset M(\mathbb{R}^n) \setminus \mathcal{P}(\mathcal{A}, C)$.

In either case we see that $M(\mathbb{R}^n) \setminus \mathcal{P}(\mathcal{A}, C)$ contains an open neighborhood $\mathcal{S}$ of $T$, which shows that $M(\mathbb{R}^n) \setminus \mathcal{P}(\mathcal{A}, C)$ is an open set, i.e., $\mathcal{P}(\mathcal{A}, C)$ is a closed subset of $M(\mathbb{R}^n)$. $\square$

## 5. Generalizations of Theorems 1 and 2

We end by briefly discussing some extensions of Theorems 1 and 2 that can be established by the methods of this paper. First, in the statements of these two theorems we have claimed that "packings" may be replaced by "oriented packings". This is true because the positionings allowed in oriented packings (translations and rotations, but not reflections) are parametrized by $O(n)^+ \times \mathbb{R}^n$, where $O(n)^+$ is the index-2 subgroup of $O(n)$ consisting of the orthogonal matrices of determinant 1. Because this subgroup $O(n)^+$ is a compact space in its own right, the analogous statement to Fact 7 for $M^+(C) = (O(n)^+ \times C)^\infty$ is also true, and thus all of the arguments of this paper go through for oriented packings upon simply replacing $M(C)$ by $M^+(C)$ at each occurrence. In the case of translated packings, where neither rotations nor reflections are allowed, we can similarly replace each occurrence of $M(C)$ by $C^\infty$ and the arguments proceed unchanged (if we like, we can think of the space $C^\infty$ as $(\{I_n\} \times C)^\infty$, where $\{I_n\}$ is the compact subgroup of $O(n)$ consisting only of the identity matrix).

It is clear that many variations on Theorems 1 and 2 could be stated by changing the sequence of sets into which $\mathcal{A}$ can be packed. The important thing is for this sequence $C_j$ (which is a shrinking sequence of homothets in Theorem 1, and a sequence of bricks of varying dimensions in Theorem 2) to have enough structure for the limiting set $\bigcap_{k=1}^{\infty} \overline{D_k}$ to be identified, where $D_k = \bigcup_{j=k}^{\infty} C_j$ as defined in the statement of Lemma 2. This limiting set would be easy to determine if the $C_j$ were ellipsoids or simplices of varying dimensions, just to name two possible applications.

Finally we note two ways in which the hypotheses of Theorems 1 and 2 can be weakened. Instead of requiring that the collection $\mathcal{A}$ can be packed into each set $C_j$, we can require only that for each $j \geq 1$ the contracted collection $(1 - \frac{1}{j})\mathcal{A} = \{(1 - \frac{1}{j})A_1, (1 - \frac{1}{j})A_2, \ldots\}$ can be packed into $C_j$. This is actually easily seen to be equivalent to the current statements of Theorems 1 and 2. However, we obtain genuinely stronger theorems by weakening the hypothesis in the following way: for every $j \geq 1$, we require only that the finite collection $\{A_1, \ldots, A_j\}$ can be packed into the set $C_j$. We leave the details of this variation to the reader.

## Acknowledgements

The author acknowledges the support of Natural Sciences and Engineering Research Council grant number A5123. The author would also like to thank Mark Hamilton for his comments on a preliminary version of this paper.

## References

[1] K. Ball, On packing unequal squares, *J. Combin. Theory Ser. A* 75 (1996), no. 2, 353--357.

[2] H. T. Croft, K. J. Falconer, and R. K. Guy, *Unsolved problems in geometry*, Springer-Verlag, New York, 1994.

[3] A. Meir and L. Moser, On packing of squares and cubes, *J. Combinatorial Theory* 5 (1968), 126--134.

[4] J. R. Munkres, *Topology: a first course*, Prentice-Hall Inc., Englewood Cliffs, N.J., 1975.

[5] M. M. Paulhus, An algorithm for packing squares, *J. Combin. Theory Ser. A* 82 (1998), no. 2, 147--157.

---

*1991 Mathematics Subject Classification.* 52C17 (52C15, 54H99).

*Department of Mathematics, University of Toronto, Canada M5S 3G3*
*E-mail address:* gerg@math.toronto.edu
