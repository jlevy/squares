# A fractional-unavoidable-set certificate for \(s(17) \ge 4.4811\)

**Author:** ChatGPT (GPT-5.6 Pro, OpenAI)  
**Date:** 6 August 2026  
**Status:** Proposed exact computer-assisted proof. The certificate has been reproduced, but it has not yet been independently audited or peer reviewed.

## Abstract

Let \(s(17)\) denote the infimum side length of a square containing 17 pairwise interior-disjoint unit squares. This note gives a finite rational certificate for

\[
s(17) \ge \frac{44811}{10000}=4.4811.
\]

The certificate is a non-negative atomic measure on a square of side \(4.4811\). Its total mass is \(16.9476\), while every unit square contained in the container has mass at least \(1.0003\). Seventeen disjoint unit squares would therefore require more mass than the entire container contains.

The only computer-assisted part is the verification that every translated and rotated unit square receives sufficient mass. That verification is reduced to 181 rational directions and finitely many translation cells. All coordinates, weights, directions, clipping operations and geometric predicates are rational. NumPy is used only for an integer two-dimensional difference array; floating-point values are printed for convenience but are not used to decide any inequality.

## 1. Statement of the theorem

Let \(s(17)\) be the infimum of the side lengths \(L\) for which 17 unit squares can be packed, with pairwise disjoint interiors, into \([0,L]^2\).

> **Theorem.**
> \[
> s(17) \ge L_0:=\frac{44811}{10000}=4.4811.
> \]

The proof uses a fractional version of an unavoidable set.

## 2. Fractional-unavoidable-set lemma

Let

\[
C=[0,L_0]^2,
\]

and let \(\mu\) be a finite non-negative atomic measure on \(C\). Suppose that

1. every unit square \(Q\subset C\), in every position and orientation, satisfies \(\mu(Q)\ge 1\); and
2. \(\mu(C)<17\).

Then \(s(17)\ge L_0\).

### Proof

Assume for contradiction that 17 unit squares fit into a square of side \(L'<L_0\). Scale the entire packing by the factor \(L_0/L'>1\). The container becomes \(C\), and the 17 packed squares now have side length strictly greater than one while retaining pairwise disjoint interiors.

Inside each enlarged square, choose the concentric unit square with the same orientation. Each chosen unit square lies strictly inside its enlarged parent. The chosen squares are therefore pairwise disjoint, including their boundaries, so no atom of \(\mu\) can be counted by two of them.

Every chosen unit square has mass at least one. Their total mass is consequently at least 17, but—because their atom sets are disjoint—it is at most \(\mu(C)<17\). This is a contradiction. \(\square\)

It remains to construct and verify a suitable measure.

## 3. The atomic measure

Put

\[
x_i=\frac12+\frac{34811}{280000}i,
\qquad i=0,\ldots,28.
\]

The candidate atoms are the grid points

\[
p_{ij}=(x_i,x_j).
\]

For an index pair \((i,j)\), let its \(D_4\) orbit be the set of distinct images obtained from the transformations

\[
(i,j)\mapsto(28-i,j),\qquad
(i,j)\mapsto(i,28-j),\qquad
(i,j)\mapsto(j,i),
\]

and their compositions. Thus each listed seed generates all of its distinct rotations and reflections in the square.

Each triplet \((i,j,w)\) below assigns mass \(w/10000\) to every distinct grid point in the corresponding orbit:

```text
(1, 11, 107),
(2, 4, 137),
(2, 9, 214),
(2, 11, 107),
(2, 12, 137),
(3, 4, 3884),
(3, 7, 214),
(3, 8, 913),
(3, 9, 214),
(3, 10, 214),
(3, 11, 1234),
(3, 12, 2189),
(3, 14, 384),
(4, 4, 1961),
(4, 7, 520),
(4, 8, 214),
(4, 9, 1413),
(4, 10, 1234),
(4, 11, 1083),
(4, 13, 137),
(4, 14, 292),
(7, 11, 529),
(7, 12, 33),
(8, 10, 906),
(8, 11, 384),
(8, 12, 351),
(9, 9, 340),
(9, 10, 180),
(9, 11, 204),
(9, 12, 549),
(10, 12, 879),
(10, 13, 201),
(10, 14, 378),
(11, 11, 396),
(11, 12, 622),
(11, 13, 204),
(11, 14, 204),
```

Expanding these orbits produces 268 atoms. Exact integer summation gives

\[
\mu(C)=\frac{169476}{10000}=16.9476<17.
\]

By construction, \(\mu\) is invariant under all eight symmetries of the containing square.

## 4. Reduction to 181 rational directions

We must verify that every unit square in \(C\) receives enough mass. The continuum of orientations is first reduced to a finite rational net.

Let

\[
T=\frac{207107}{500000},
\qquad
d=\frac{T}{180},
\]

and for \(k=0,\ldots,180\), define

\[
t_k=\frac{kT}{180},
\qquad
c_k=\frac{1-t_k^2}{1+t_k^2},
\qquad
s_k=\frac{2t_k}{1+t_k^2}.
\]

Each pair \((c_k,s_k)\) is an exact rational unit vector. Its angle is

\[
\psi_k=2\arctan t_k.
\]

The final two directions bracket \(45^\circ\). For adjacent directions,

\[
\tan\left(\frac{\psi_{k+1}-\psi_k}{2}\right)
 =\frac{t_{k+1}-t_k}{1+t_kt_{k+1}}
 \le d.
\]

Every angle in \([0,45^\circ]\) is therefore within an angular error \(\varepsilon<d\) of one of these 181 rational directions. The symmetry of \(\mu\) and \(C\) reduces every square orientation to this range.

Now set

\[
b=\frac{9973}{10000}=0.9973.
\]

Suppose a unit square has one orientation and a concentric square of side \(b\) has an orientation differing by \(\varepsilon\). The smaller square is contained in the unit square whenever

\[
b(\cos\varepsilon+\sin\varepsilon)\le 1.
\]

For the direction net above,

\[
\begin{aligned}
b(\cos\varepsilon+\sin\varepsilon)
&\le b(1+\varepsilon)\\
&<b(1+d)\\
&=\frac{899635478111}{900000000000}\\
&<1.
\end{aligned}
\]

Consequently, every unit square contains a concentric \(b\)-square at one of the 181 rational directions. It is enough to prove that every such \(b\)-square contained in \(C\) has mass at least one.

## 5. Exact verification of every translation

Fix one rational direction \((c_k,s_k)\). For a centre \((x,y)\), use coordinates aligned to the moving \(b\)-square:

\[
U=c_kx+s_ky,
\qquad
V=-s_kx+c_ky.
\]

The set of centres for which the \(b\)-square remains inside \(C\) is a rational quadrilateral in \((U,V)\)-space.

For an atom \(p\), write its transformed coordinates as \((p_U,p_V)\). The atom belongs to the moving square exactly when

\[
|U-p_U|\le \frac b2,
\qquad
|V-p_V|\le \frac b2.
\]

Thus, in centre space, each atom contributes its weight on an axis-aligned rectangle. The total mass is constant on every open cell cut out by the finitely many rational event lines

\[
U=p_U\pm\frac b2,
\qquad
V=p_V\pm\frac b2.
\]

The accompanying verifier constructs all event coordinates exactly, accumulates the rectangle weights in an integer two-dimensional difference array, and checks every event cell that can meet the allowed centre quadrilateral. Its clipping calculations use `fractions.Fraction`. The cell test deliberately includes a slight superset of feasible cells, which is conservative: checking an extra low-scoring cell could reject a valid certificate, but cannot incorrectly validate one.

It is sufficient to check open cells. On an event boundary, atom membership is defined by closed inequalities, so the boundary score cannot be smaller than the score in an adjacent open cell.

Across all 181 rational directions, the exact minimum score found is

\[
\min_Q\mu(Q)=\frac{10003}{10000}=1.0003.
\]

The reduction in Section 4 therefore proves that **every unit square contained in \(C\) has mass at least \(1.0003\)**.

## 6. The contradiction

Suppose 17 unit squares could be packed into a container of side \(L'<L_0\). Apply the scaling argument from Section 2 and choose the 17 concentric unit subsquares. Their atom sets are pairwise disjoint, while each has mass at least \(1.0003\). Hence

\[
17.0051
=17\cdot1.0003
\le \sum_{i=1}^{17}\mu(Q_i)
\le \mu(C)
=16.9476,
\]

which is impossible.

Therefore

\[
\boxed{s(17)\ge\frac{44811}{10000}=4.4811}.
\]

## 7. Reproduction

Place [`verify_n17_lower_bound_4_4811.py`](verify_n17_lower_bound_4_4811.py) alongside this note and run:

```bash
python verify_n17_lower_bound_4_4811.py
```

The script requires Python 3 and NumPy. A successful run ends with:

```text
atoms = 268
total_weight = 169476/10000 = 16.9476
angle_net_size = 181
b*(1+d) = 899635478111/900000000000 = 0.999594975679 < 1
minimum_score = 10003/10000 = 1.0003 at k=0
CERTIFICATE CONDITIONS VERIFIED.
By the scaling argument: s(17) >= 44811/10000 = 4.4811.
```

No floating-point result is trusted by the proof. The displayed decimal values are informational; the assertions use exact rational values and integer scores. The largest possible accumulated score is tiny relative to the range of the signed 64-bit integers used by NumPy.

## 8. Status and audit boundary

This is a compact, reproducible certificate rather than a claim that a general-purpose optimiser has exhaustively searched all packings. The measure is topology-independent: it applies to every position and orientation of every unit square inside the proposed container.

The certificate and verifier have been rerun successfully, and the mathematical reduction has been checked for internal consistency. They have **not** yet been audited through an independent implementation or peer review. In particular, a serious external review should examine:

- the scaling and disjointness argument;
- the angular-net containment inequality;
- the completeness and conservatism of the event-cell enumeration; and
- the transcription of the 37 orbit seeds and their weights.

Until that has happened, this result should be described as a **proposed new computer-assisted lower bound**.

## Acknowledgement

This certificate was developed during Sam Burns's *Squarl* project, an experimental investigation of the \(n=17\) square-packing problem. Sam supplied the project context, commissioned the investigation, and is publishing the certificate and verifier for scrutiny.

## Reference for the preceding bound

Erich Friedman, “Packing Unit Squares in Squares: A Survey and New Results”, *Electronic Journal of Combinatorics*, Dynamic Survey 7. The survey records

\[
s(17)\ge\frac{40\sqrt2+19}{17}\approx4.445208382054341.
\]

- Survey: <https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html>
- Squarl source repository: <https://github.com/sam-bee/squarl>
