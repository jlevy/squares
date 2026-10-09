# n17 Paper Review: Global Optimization and Sum-of-Squares Certificates

**Date:** October 8, 2026. **Status:** Paper and archive reviewed; no solver experiment
run. **Review:** GPT-6 Astra at xhigh for mathematics; GPT-6.1 Sol at medium for archive
and research-record audits.

**Retain this paper as a relevant method source, and keep the shared-centre LP followed
by a small exact SOS pilot as the selected sequence.** The paper supplies an alternative
polynomial description of non-overlap.
It supplies neither an n17 optimality certificate nor evidence that an unrestricted SOS
solve is practical. This review adds no exclusion, admission or bound improvement.
The [verified bracket](../../../packing/frontier/n-017.md) remains
$4.66044275<s(17)\le4.6755300936045509516342148538535054$.

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

## Consequence for the n17 Plan

The paper reinforces the sequence already chosen in the exact-SOS strategy review; it
does not justify restarting the proof architecture.
The full residue of 4,683 orbits differs from the selected difficult stratum of 95
orbits/744 states.

1. Complete the
   [first-eight shared-centre LP contract](https://github.com/jlevy/squares/blob/c3dc6027a66fe396f22953a1d29945420198bdda/docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md),
   owned by `think-dvcs`. Require an exact primal satisfying every row, or exact Farkas
   infeasibility weights.
   Endpoint relaxation calibration does not replace that test.
2. If an exact LP survivor remains, use the conditional successor `think-geid` to freeze
   one triple of its original cell domains.
   Keep all six centre coordinates and all three necessary incircle constraints
   $\|p_i-p_j\|^2\ge1$. Use the existing triple ranking and cheaper exact vertex
   obstruction before attempting SOS orders 2 and 3.
3. Preserve the strategy review’s limits: 10,000 Gram unknowns, two million coefficient
   entries, 300 seconds per eligible order including exact reconstruction, 120 seconds
   fresh checking, 4 GiB sampled RSS, 8 MiB output and 4,096-bit rational coefficients.
   Register the frozen source, basis and controls before executing a target.

A dense preflight already rules out ordinary order 3 under those limits.
For six variables and the three quadratic incircle constraints, before adding cell
facets:

| Dense Coefficient System | Order 2 | Order 3 |
| --- | ---: | ---: |
| Gram unknowns | 490 | 4,788 |
| Coefficient rows | 210 | 924 |
| Matrix entries | 102,900 | 4,424,112 |

These are combinatorial counts, not measured runtimes.
Each linear cell facet adds 28 unknowns at order 2 or 406 at order 3. Full dense order 3
exceeds the two-million-entry cap before any facets.
It needs a separately frozen restricted basis, quotient reduction or sparse
implementation with intermediate-arithmetic preflight.
The incircle-only order-3 map has 12,096 nonzero entries; sparse input storage alone
does not bound fill-in during exact elimination.
Do not construct the forbidden dense system as a fallback.

Accept an exact contradiction only with the original-cell and D4 joins checked.
An exact feasible triple is a relaxation witness.
Numerical infeasibility, failed reconstruction and a resource stop remain unresolved; a
completed failed search retires only its frozen recipe.
Controls must preserve touching and the accepted endpoint, reject corrupted identities
and negative weights, and exercise singular positive semidefinite matrices and resource
stops.

The existing 6–12 agent-hour pilot implementation allowance is a planning estimate, not
a proof-completion forecast.
Certificate existence, useful degree and exactification cost remain unknown.
The paper’s redundant incircle constraint is already represented in exp313/314; its
contribution here is formulation comparison and the explicit certificate-size warning.
Its heuristic symmetry-breaking results do not invalidate exact D4 quotienting.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
