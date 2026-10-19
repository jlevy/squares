# n17 Paper Review: Global Optimization and Sum-of-Squares Certificates

**Date:** October 8, 2026. **Status:** Three sources and extraction quality reviewed;
analytical reductions derived; no solver experiment run.
**Review:** GPT-6 Astra at xhigh for mathematics; GPT-6.1 Sol at medium for archive and
research-record audits.

The square-packing problem asks for $s(17)$, the minimum side length of a square
containing 17 unit squares.
Each unit square may rotate independently; their interiors must be disjoint, and
touching is allowed.
A verified construction gives an upper bound on $s(17)$; an exclusion proof gives a
lower bound by ruling out every packing below a specified side length.

The accepted construction has an exact algebraic side length $S^*$, the certified root
of the catalogue’s degree-18 polynomial.
The displayed upper bound is a rational outward ceiling on $S^*$, not its exact value.
Optimality, $s(17)=S^*$, remains open.
The [verified bracket](../../../packing/frontier/n-017.md) is unchanged:
$4.66044275<s(17)\le4.6755300936045509516342148538535054$.

The current exclusion strategy uses a finite cover: finitely many closed centre domains
that together contain every candidate placement in a specified case.
A cell is one domain in that cover; a residual cell case is one the earlier exact tests
have not excluded. Proving such a case impossible removes it from the residue.
A global exclusion also needs complete coverage and the joins between cases, including
square symmetries (the rotations and reflections denoted D4).

**Keep the first-eight shared-centre LP as the next entry, then use an exact
weighted-vertex screen before a small SOS pilot.** An LP is a linear program: it tests
linear constraints or optimizes a linear objective.
The packing paper supplies a polynomial non-overlap model; the Blekherman–Parrilo–Thomas
book supplies positivity and optimization theory; Laplagne addresses singular
sum-of-squares (SOS) recovery.
Astra’s new derivation shows that the weighted screen subsumes every possible exclusion
from the specified order-2 SOS recipe without a quadratic ball.
This is an analytical result, with no target run, exclusion, admission or bound
improvement.

## Source and Archive

Berthold, Kamp, Mexi, Pokutta and Pólik,
[arXiv:2605.04850v1](https://arxiv.org/abs/2605.04850v1), *Out-of-the-Box Global
Optimization for Packing Problems: New Models and Improved Solutions*, was submitted May
6, 2026. Its
[original PDF](../../../packing/resources/papers/berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems.pdf)
and
[unedited extraction](../../../packing/resources/papers/berthold-kamp-mexi-pokutta-polik-2026-out-of-the-box-packing-problems.raw.md)
were already archived September 8. The 32-page, 933,101-byte PDF matches a fresh v1
download exactly; a fresh `pdftotext -layout` extraction also matches the retained text.
The
[acquisition manifest](../../../packing/resources/web/annealing-methods-audit-2026-09-08/README.md)
records both hashes.
The
[October 8 audit](../../../packing/resources/web/annealing-methods-audit-2026-09-08/n17-relevance-audit-2026-10-08.json)
records the comparisons and supplement inspection.
A duplicate copy or reconstructed transcription would add no source evidence.

## Additional Sources and Extraction Quality

Blekherman, Parrilo and Thomas, editors, *Semidefinite Optimization and Convex Algebraic
Geometry* (2013), is available as an
[author-hosted PDF](https://www.mit.edu/~parrilo/sdocag/MO13-Blekherman-Parrilo-Thomas.pdf).
Laplagne’s *Facial reduction for exact polynomial sum of squares decompositions*,
[arXiv:1810.04215v1](https://arxiv.org/abs/1810.04215v1), was submitted October 9, 2018.
The
[source and quality packet](../../../packing/resources/web/n17-sos-sources-2026-10-08/README.md)
records their identities and limitations.

Both originals and unedited `pdftotext -layout` extractions were retained before
analysis. All 487 book pages and all 19 Laplagne pages produced nonempty text.
Raw formulas contain 2,785 and 15 control glyphs respectively, as well as flattened
powers and indices. Zero replacement characters does not establish formula fidelity.
Astra checked consequential statements against rendered original pages.
Laplagne’s original TeX was also acquired and compared without execution; it resolves
the raw glyph ambiguities.
Neither source has a whole cleaned mathematical transcription.
The 18.2 MB book and its full raw text remain outside Git under OR-18; the small
Laplagne PDF, raw text and original TeX are retained in the archive.

Book locators below use printed pages; the packet maps them to PDF pages, accounting for
omitted blank pages.
Laplagne’s printed and PDF page numbers coincide.

## What the Paper Establishes

The paper uses SCIP and FICO Xpress, with Farkas-based polygon separation (§6) and an
S-lemma containment formulation for circles in ellipses (§5). It does not present a
square-packing SOS certificate.
Table 2 contains no square-in-square incumbent improvement.
For polygon instances with $n\ge6$, dual bounds generally remain at the area bound;
median gaps are 9.9–15.2% (§6.2, p. 20). Numerical polishing (§3.3) is distinct from an
independently checked exact optimality proof.

The S-lemma concerns one quadratic implication under its stated interior-feasibility
assumption. It gives no automatic reduction of square packing’s multiple constraints and
separation alternatives to one small semidefinite program.

The public
[supplement](https://github.com/DominikKamp/Packing/tree/27f71632d8655ae4b6a049410a401976748b94e3)
contains numerical coordinates and visualizations.
At the inspected revision its complete tree contains no solver models, verification
tools or optimality certificates, despite the paper’s model-availability statement.
Its n17 square witness reports $R=4.676812769745167$, numerically worse than the
retained endpoint; we have not verified its feasibility.
Both inner and outer square side lengths equal $\sqrt2$ times their circumradii, so
scaling the inner square to unit side makes the container side exactly $R$.

## How Square Packing Can Be Encoded for SOS

The following specialization and size counts are mathematical derivations from the
paper’s model and the existing
[exact-SOS strategy review](https://github.com/jlevy/squares/blob/64a24101d423e5eafeab5c5b9e543430eb46cabf/docs/project/reviews/review-2026-10-08-n17-strategy-and-exact-sos.md).
They are not a new computational result.

Write a unit square’s centre as $p_i=(x_i,y_i)$ and its axes as $u_i=(a_i,b_i)$,
$v_i=(-b_i,a_i)$, with $a_i^2+b_i^2=1$ and $a_i,b_i\ge0$. The closed quarter-turn chart
covers every square orientation.
Containment in $[0,L]^2$ requires

$$
\tfrac12(a_i+b_i)\le x_i,y_i\le L-\tfrac12(a_i+b_i).
$$

For each pair, take its eight inward face normals $n_k$ and offsets
$s_k=n_k\cdot p_{\operatorname{owner}(k)}-\frac12$. Lemma 3 and equations (6.1)–(6.5),
pp. 16–18, give non-overlap through existential multipliers:

$$
\lambda_k\ge0,\qquad \sum_k\lambda_k=1,\qquad
\sum_k\lambda_kn_k=0,\qquad \sum_k\lambda_ks_k\ge0.
$$

These conditions exclude a common interior point and allow touching.
Preserve the weak final inequality and zero multipliers.
A positive separation margin would discard legal contacts.
These geometric multipliers describe feasible packing; they are not themselves a proof
that the whole packing system is infeasible.

| Encoding at Fixed $L$ | Real Variables | Polynomial Structure |
| --- | ---: | --- |
| Centres and cosine/sine coordinates | 68 | 17 circle equalities and 136 eight-way separating-axis disjunctions; each branch is quadratic |
| Farkas form after eliminating normals and offsets | 1,156 | 68 pose variables and 1,088 pair multipliers; maximum degree 3 |
| Farkas form with two dot-product lifts per square | 1,190 | Maximum degree 2, retaining the lifts’ defining equalities |

The paper’s raw square specialization has 1,344 variables including $R$, before
presolve. Lifting reduces degree by adding variables; it does not establish convexity.
Complete separation coverage is required whether using existential Farkas multipliers or
explicit branch alternatives.

An SOS polynomial is a sum of squares of polynomials, so it is nonnegative at every real
point. One searches for it through a Gram representation $\sigma(z)=m(z)^TQm(z)$, where
$m$ lists monomials and $Q$ is a symmetric positive semidefinite (PSD) matrix:
$w^TQw\ge0$ for every real vector $w$. Coefficient matching imposes linear equations on
$Q$; optimizing subject to those equations and PSD constraints is a semidefinite program
(SDP). Relaxation order $r$ caps the total degree of each term in the certificate at
$2r$, limiting the monomial basis and the search size.

An SOS emptiness certificate for $g_i(z)\ge0$ and $h_j(z)=0$ can have the form

$$
-1=\sigma_0(z)+\sum_i\sigma_i(z)g_i(z)+\sum_j\tau_j(z)h_j(z),
$$

where every $\sigma_i$ has an exactly checked nonnegative weighted-square decomposition.
The contradiction follows by evaluating the exact identity at a supposed satisfying
point. This is the connection to
[Sostactic](https://www.mmaaz.ca/writings/sostactic.html): numerical search proposes a
certificate, followed by exact reconstruction and checking of the encoded theorem.

## Why Encoding Is Easier Than Certification

At dense relaxation order 2, 68 variables require a Gram matrix of dimension
$\binom{70}{2}=2415$, with 2,917,320 independent symmetric entries before multiplier
blocks. Six variables require dimension 28. The full Farkas model is larger still.
Pairwise constraints do not automatically give useful sparse blocks: all 136 pairs
connect every square’s pose block to every other.
Preserving an equivalent packing model while removing pair constraints requires proving
them redundant. Dropping constraints instead produces a weaker necessary relaxation; an
exact contradiction remains sound.
A restricted certificate template can be sound when successful while remaining
inconclusive when unsuccessful.

Exactifying a numerical semidefinite solution is a separate obstacle.
Rational projection onto coefficient identities can destroy positive semidefiniteness.
[Peyrl–Parrilo](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf)
give recovery conditions involving strict feasibility and sufficient accuracy.
Active contacts can force singular Gram blocks.
Retain exact identities and exact positive-semidefinite or weighted-square checks,
including zero-pivot cases.
Convergence arguments also need their stated hypotheses, such as an Archimedean
quadratic module; compact geometry alone gives no useful degree or runtime estimate.

At the working cap $U=1169/250=4.676$, the accepted endpoint already gives a feasible
packing. An SOS contradiction at $U$ must concern specified residual cells.
Exact optimality needs a theorem such as $L-S^*\ge0$, with $S^*$ represented exactly, or
a complete strict-sublevel refutation.
Finitely many rational thresholds below $S^*$ leave a gap.
Neither solver infeasibility flags nor approximate endpoint coordinates close it.

## What the Book Adds

Theorems 3.127–3.128 (p. 112) use an equality ideal and a **preordering**, which permits
products of inequality generators, for infeasibility certificates.
Theorems 3.136 and 3.138 (p. 115) give strictly positive representations on compact
sets, with Putinar’s smaller quadratic module requiring the additional Archimedean
hypothesis. These results provide no practical degree or runtime bound for our
fixed-degree template.

Section 3.4.4 and Exercise 3.140 (pp.
116–117) give a sharp-bound warning: $1-x^2$ has no representation
$\sigma_0+\sigma_1(1-x^2)^3$ on $[-1,1]$, whereas adding any positive constant permits
one. Approximation toward an optimum need not produce the exact endpoint certificate.
Theorems 3.43–3.44 (pp.
70–71) tie rational SOS to rational PSD Gram matrices and require strict feasibility for
the stated rounding/projection recovery guarantee.

The structural reductions have specific scopes: Theorem 3.94 (p. 92) trims a fixed SOS
polynomial using its Newton polytope; Example 3.99 (p. 95) uses established equalities;
§3.3.6 (p. 100) averages an invariant convex certificate problem.
They do not justify guessed contact equations, trimming all multipliers from the support
of $-1$, or imposing D4 symmetry on an asymmetric cell triple.

## What Laplagne Adds

Lemma 3.1 and Proposition 3.2 (pp.
5–6) justify restricting a PSD Gram matrix to an exactly known face: $v^TQv=0$ implies
$Qv=0$. An exact real zero of a fixed SOS polynomial supplies such an equation.
Proposition 3.4 and Lemmas 3.6–3.7 (pp.
6–8) give algebraic-trace and singular-block restrictions for rational Gram matrices.
Approximate eigenvectors do not certify a face.

The rational-entry restriction in §3.4 and Algorithm 1 (pp.
8–11) can lose solutions; “not found” is inconclusive.
Theorem 4.1 treats two squares over an odd-degree extension; Theorem 5.1 (pp.
14–15) gives a rational polynomial that is SOS over $\mathbb Q(\sqrt[3]{2})$ but not
over $\mathbb Q$. Rational input does not guarantee rational exactification of a
selected representation.
This does not prove that our rational infeasibility system lacks some rational
Positivstellensatz certificate.

For the pilot’s $-1$ identity, a zero of an input constraint does not force its
multiplier to vanish.
An endpoint outside the selected cells supplies no face restriction.
For a later identity $L-S^*=\sigma_0+\sum_i\sigma_i g_i+\sum_j\tau_jh_j$, a verified
feasible endpoint forces $\sigma_0$ to vanish and forces $\sigma_i$ to vanish only where
$g_i>0$. An active $g_i=0$ gives no such multiplier condition.
A constrained zero need not satisfy unconstrained stationary equations: $p(x)=x$ on
$x\ge0$ has multiplier 1 and derivative 1 at its zero.

## An Exact Face Reduction for the Cell Pilot

For the selected three-centre case, let $E_i$ be the original exact convex polygonal
domain allowed for centre $p_i$, retaining any point or segment domain.
Its defining inequalities give a nonempty product domain $P=E_1\times E_2\times E_3$.
Every unit square contains a disk of radius $1/2$ centred at its own centre.
Disjoint square interiors therefore require disjoint disk interiors: $\|p_i-p_j\|\ge1$,
hence $g_k=q_k-1\ge0$, with $q_k=\|p_i-p_j\|^2$, for each of the three pairs.
These incircle constraints are necessary; satisfying them need not keep the squares from
overlapping. Refuting this relaxation excludes the square case, while a feasible centre
triple alone does not establish a packing.

**The following is Astra’s new mathematical derivation, not a packing exclusion or a
result claimed by either source.** Let $z=(p_1,p_2,p_3)\in\mathbb R^6$, with $F$ affine
cell inequalities $\ell_f\ge0$ defining $P$ and the three incircle generators $g_k$.
Assume distinct centre indices, no equality multipliers and no additional nonlinear
generator.

At Putinar order $r\ge2$, write

$$
-1=\sigma_0+\sum_{f=1}^F\sigma_f\ell_f+\sum_{k=1}^3\sigma_k g_k,
\qquad \deg\sigma_0\le2r,\quad \deg\sigma_f,\deg\sigma_k\le2r-2.
$$

Its homogeneous degree-$2r$ part is

$$
0=(\sigma_0)_{2r}+\sum_{k=1}^3(\sigma_k)_{2r-2}q_k.
$$

Leading homogeneous parts of SOS polynomials are SOS. Every summand is globally
nonnegative, so each vanishes identically.
Each $q_k$ is a nonzero polynomial; hence $\deg\sigma_0\le2r-2$ and
$\deg\sigma_k\le2r-4$. The facet multipliers retain their degree ceiling.
PSD forces the eliminated Gram rows, columns and cross-degree entries to vanish,
preserving the entire stated truncated ansatz.

| Reduced System | Order 2 | Order 3 |
| --- | ---: | ---: |
| Symmetric Gram unknowns | $31+28F$ | $490+406F$ |
| Coefficient rows through remaining maximum degree | 84 | 462 |
| Unknowns at $F=12$ | 367 | 5,362 |
| Dense entries at $F=12$ | 30,828 | 2,477,244 |

The unreduced six-variable order-3 system still has 4,424,112 entries before facets.
The reduced system passes the two-million-entry count for $F\le9$; $F=9$ gives 1,914,528
entries and $F=10$ gives 2,102,100. Count the actual facets, including added bounds.
Twelve facets still exceed the cap; other exact reductions require separate preflight.
These are size calculations, not runtimes or target results.

## An Exact Weighted-Vertex Screen Before SOS

At order 2 the incircle multipliers are constants $\alpha_k\ge0$. Any contradiction
therefore implies $\sum_k\alpha_k g_k\le-1$ throughout $P$. Write $A=\sum_k\alpha_k$.
Since $P$ is nonempty, $A=0$ cannot satisfy that inequality, so $A>0$. Dividing by $A$
gives normalized weights $\bar\alpha_k=\alpha_k/A$ and margin $\varepsilon=1/A>0$. For
every product vertex $v$, define $G_{vk}=q_k(v)-1$ and seek normalized weights, written
again as $\alpha$:

$$
\alpha\ge0,\qquad \mathbf1^T\alpha=1,\qquad
G\alpha\le-\varepsilon\mathbf1,\qquad\varepsilon>0.
$$

A nonnegative weighted sum of squared distances is convex, so its maximum on $P$ occurs
at a product vertex.
These exact finite inequalities extend throughout $P$ and directly contradict the three
incircle necessities.
Success excludes the triple without SOS reconstruction.

Conversely, exact weights

$$
\beta\ge0,\qquad\mathbf1^T\beta=1,\qquad G^T\beta\ge0
$$

rule out a strict weighted certificate: multiply any candidate vertex bounds by $\beta$
to obtain $0\le\alpha^TG^T\beta\le-\varepsilon$. They consequently rule out **every
order-2 contradiction in the stated no-ball, no-equality ansatz**. This mixture is not a
physical packing or a feasible triple.
Numerical failure remains unresolved.
The existing equal-weight check is the cheapest first slice; it tests only one point in
the weight simplex.

At the existing 36-vertices-per-cell ceiling, the weighted LP has at most 46,656 vertex
rows and four variables including the margin.
Reconstruct every original cell vertex and row exactly; retain point and segment
domains, touching, and D4 joins.
A positive certificate requires the usual composition/admission review.

## Archimedeanness and a Conditional Ball Recipe

Linear coordinate bounds can establish an Archimedean module without an additional
quadratic generator.
For $l\le x\le u$, $u>l$ and $u+l\ge0$,

$$
u^2-x^2=\frac{(u-x)^2}{u-l}(x-l)
+\frac{(x-l)^2}{u-l}(u-x)+(u+l)(u-x).
$$

For the necessary centre bounds at $U=4.676$, use $l=1/2$ and $u=522/125$;
$6u^2=1634904/15625<105$. Sum these identities and the positive remainder to obtain
$105-\|z\|^2$ in the module.
The bound rows must be present or derived as exact nonnegative combinations of the cell
facets; compactness alone is insufficient.
Loose positive-width bounds also cover degenerate cells.

After an exact weighted-screen obstruction, a separately frozen generator
$B=R_2-\|z-z_0\|^2\ge0$ is a plausible order-2 successor.
Fix a rational centre $z_0$ and rational squared radius $R_2$. Prove the radius valid on
the entire original product domain, for example by exact maxima at each cell’s vertices.
Its negative leading quadratic part invalidates the preceding face reduction and
strengthens the truncated certificate cone while preserving geometry.
With twelve affine facets and one ball, unrestricted order 2 has **854 Gram unknowns and
179,340 dense entries**. Passing these counts establishes eligibility only.
The ball recipe needs a distinct preregistration; it cannot be added silently.

## Consequence for the n17 Plan

The full residue of 4,683 orbits differs from the selected difficult stratum of 95
orbits/744 states. The source review changes the conditional pilot contract:

1. Complete the
   [first-eight shared-centre LP contract](https://github.com/jlevy/squares/blob/c3dc6027a66fe396f22953a1d29945420198bdda/docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md),
   owned by `think-dvcs`. Require an exact primal satisfying every row, or exact Farkas
   infeasibility weights.
   Endpoint calibration does not replace that test.
2. If a certified LP survivor remains, `think-geid` freezes one triple of original cell
   domains using the existing exact ranking.
   Run the equal-weight vertex check, then the exact weighted-vertex screen.
   An exact mixture obstruction retires the specified no-ball order-2 SOS recipe for
   that triple.
3. Make the face reduction reviewable before implementing an SDP: verify generator
   shapes, the reduced-to-original Gram embedding and exact exposing identities.
   Exact Gaussian moments can expose the top blocks; at order 3 the matrices have
   dimensions 56 and three copies of 21, totalling 4,459 entries.
   Check their coefficient-map identities and rational LDL factors; no numerical
   integration is needed.
   Include corrupted exposure and cross-degree controls.
4. Only then freeze an eligible SOS successor, such as the ball-augmented order-2 recipe
   or reduced order 3 when its actual facet count permits it.
   Keep all six centre coordinates, all three incircle necessities and the
   original-cell/D4 joins.

Preserve the strategy review’s ceilings: 10,000 Gram unknowns, two million coefficient
entries, 300 seconds per eligible order including exact reconstruction, 120 seconds
fresh checking, 4 GiB sampled RSS, 8 MiB output and 4,096-bit rational coefficients.
Sparse input storage does not bound fill-in during exact elimination.
Register the frozen source, basis, all generators and controls before target execution.

Accept an exact contradiction only with the original-cell and D4 joins checked.
An exact feasible triple is a relaxation witness.
Numerical infeasibility, failed reconstruction and a resource stop remain unresolved; a
completed failed search retires only its frozen recipe.
Controls must preserve touching and the accepted endpoint, reject corrupted identities
and negative weights, and exercise singular positive semidefinite matrices and resource
stops. Add exact weighted-primal and mixture checks, full vertex reconstruction, and a
guard that rejects the no-ball reduction when a quadratic ball or equality term appears.

The existing 6–12 agent-hour pilot implementation allowance is a planning estimate, not
a proof-completion forecast.
Certificate existence, useful degree and exactification cost remain unknown.
The paper’s redundant incircle constraint is already represented in exp313/314; its
contribution here is formulation comparison and the explicit certificate-size warning.
Its heuristic symmetry-breaking results do not invalidate exact D4 quotienting.

The source reading covers the cited book sections and Laplagne’s relevant arguments, not
the whole book. No Maple computations or independent irreducibility proof were replayed.
The flagged derivative and parameter inconsistencies were not used as unchecked
premises. Generic algebraic root finding, arbitrary facial reduction and algebraic-field
certificate support remain deferred.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
