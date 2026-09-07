# Mathematical Review Packet: Resolving Eleven Squares

This packet asks for a deep mathematical review of the square-packing research program,
its progress through Agenda 024, and the strategies most likely to produce meaningful
new results. The highest-value outcome is a creative argument that closes the remaining
gap and determines the exact value of `s(11)`.

The research snapshot is Git revision `4d305597a505ebfbe85f1851fa7148374661e622`, dated
2026-09-06, after the merge of PR 101. The folder contains **19 files**, including this
brief. Related source materials are assembled into dossiers so the review can proceed
without sharing the repository.

## The Mathematical Target

Let `s(n)` be the infimum of the sides of square containers holding `n` closed unit
squares with pairwise disjoint interiors.
Each unit square may rotate and translate independently.
Touching is legal. The current certified bracket is

$$
L_* = \frac{38100\sqrt{8100042893309449}}{899996306539}
\le s(11)\le U,
$$

where `L_* = 3.810025723614703…` and `U = 3.877083590022814…`. The remaining gap is
approximately `0.067057866408`. The exact Trump construction attains `U`. Its geometry
and local theorem are supplied below, but a global optimality proof is still missing.

The preferred conjecture is `s(11)=U`. Assess it critically.
A rigorously verified smaller packing would also be a decisive result.
Useful intermediate outcomes include a substantial lower-bound improvement, a structural
theorem that excludes a meaningful part of configuration space, a proved limitation that
redirects effort, or a complete reduction that makes the final global exclusion
practical.

## Review Request

Please use the included evidence to develop your own mathematical judgment before
accepting the current agenda’s ranking.
Investigate these connected questions:

1. **What has the research actually earned?** Separate global packing bounds, local
   theorems, relaxation bounds, exact finite computations, numerical evidence and
   implementation readiness.
   Identify any argument whose scope is overstated or whose premises do not support its
   claimed strategic payoff.
2. **What could close the entire gap?** Seek a specific argument for all feasible
   eleven-square configurations.
   Possibilities include a sharp resource inequality with equality classification, a
   geometric reduction to a small family, a configuration-level integrality argument, or
   a global capture theorem that joins the existing local Trump result.
   These are prompts, not a required menu.
3. **Which relaxation barriers are real, and at what scope?** Determine whether a
   proposed obstruction applies only to frozen sites, weights, net spacing, a witness
   shape, the one-square additive relaxation, or the full geometric problem.
   Consider changing the mathematical object when an established ceiling demands it.
4. **Can existing machinery make a new idea testable?** The packet describes exact
   number-field geometry, separating-axis cells, exact and numerical LPs, quenching,
   tangent cones, event sweeps, interval verification, density support tests and
   proposed complete face/angle methods.
   Identify what can be reused and the smallest missing mathematical or computational
   component.
5. **What should be pursued next?** Rank a small set of directions by expected
   mathematical value and the specificity of their mechanism.
   Distinguish a useful small bound increment from a route capable of exact resolution.
   Challenge the existing allocation when the evidence supports a better choice.

For your strongest proposal, write the central lemma or certificate with explicit
quantifiers, domains and boundary conventions.
Give as much proof as you can.
Identify the first unresolved implication, the simplest falsifier or decisive
calculation, and how a successful result would connect to `s(11)=U` or to a better
packing. Do not substitute a list of method names for an argument.

A useful review deliverable contains an assessment of progress, a ranked strategy, a
developed best argument, and concrete next investigations with success and stop
conditions. Label proved deductions, plausible conjectures and heuristic expectations
separately. If an idea fails, retain the obstruction and the scope at which it fails.
There is no need to operate the repository’s task tracker or execute its historical
dispatch instructions.

## Reading Order and File Map

Start with files 01 and 02 for current scientific status and the available machinery.
Read files 07–13 for the actual proof mechanisms and remaining obligations.
Files 03–06 and 15 provide the agenda and strategic context to assess.
File 14 records why several promising search reductions did not yet yield a proof; file
16 supplies foundations and source lemmas.

| File | Contents |
| --- | --- |
| [01 Research progress](01-research-progress.md) | Exact current bracket, broader results, progress and negative results, current unresolved questions, and routes toward global closure. |
| [02 Tooling and machinery](02-tooling-and-machinery.md) | Mathematical algorithms, representations, inputs/outputs, implementation status and assurance boundaries. |
| [03 Agenda 024](03-agenda-024.md) | The complete requested agenda, including its current allocation and retained historical material. |
| [04 Child agendas](04-child-agendas.md) | Scientific portions of agendas 025/026, adaptive witness theorem and current adaptive implementation boundary. |
| [05 Current assessment](05-current-assessment-and-review.md) | Research-sequence plan, adversarial senior review and corrections that determine the current allocation. |
| [06 Alternative strategies](06-alternative-strategies.md) | Contributed arguments about richer witnesses, density equality, integrality, stationarity and global capture, with corrections. |
| [07 Standalone 3.81 proof](07-standalone-381-proof.md) | Full theorem, proof, continuum-to-finite reduction, all 1,121 atoms and an embedded independent standard-library verifier. |
| [08 Dilation limit](08-dilation-limit.md) | Full proof of the strongest recorded lower endpoint, including the strict-family/weak-limit distinction. |
| [09 Trump construction and local proof](09-trump-construction-and-local-proof.md) | Every exact corner formula, the local theorem and proof, branch structure, quantitative constants and later independent-review scope. |
| [10 Fractional barriers](10-fractional-barriers-and-negatives.md) | Fixed-net/core ceilings, conditional certificate reasoning, the 3.82 bracket and exact shrinking/angle-class negatives. |
| [11 Density dossier](11-density-contract-candidate-and-results.md) | Primal/dual measure contract, latest finite-support and pair results, complete face-verification proposal, exact candidate and necessary-row LP data. |
| [12 Restricted orientations](12-restricted-orientations.md) | Concrete point/domain obligations, completed exact-angle tests and the remaining continuous-angle certificate design. |
| [13 Typed global structure](13-typed-global-structure.md) | Branch-cover and Fritz–John arguments, singular and flexible cases, symmetry and leaf-closing obligations. |
| [14 Search and near-tight evidence](14-search-and-near-tight-evidence.md) | Quench mechanisms, basin/terminal-component traps, census results and the released-support seed experiment. |
| [15 Registered questions](15-registered-mathematical-questions.md) | H-036 and H-093–105 with original claims, domains, accept rules and present interpretation. |
| [16 Background and literature](16-mathematical-background-and-literature.md) | Problem/cell/number-field foundations, notation, literature survey and Stromquist’s relevant lemmas and proofs with source-gap annotations. |
| [17 Source catalogue](17-source-catalogue.md) | Exact source paths and selected line ranges, provenance, packaging rules and reproduction command. |
| [18 Trump diagram](18-trump-packing.svg) | Exact construction/contact diagram. |

## Current Evidence That Changes the Reading

The latest allocation and the Session 089 results supersede the old launch schedules.
The selected Session 089 work did **not** move the packing bounds.

- The scalar target `61/16 = 3.8125` remains unopened.
  The adaptive route has completed two control slices, with a full target-capable
  verifier still conditional.
- The density support screen gives an exact **finite-row** optimum `56/5`; the true
  fixed-support almost-everywhere optimum is only bracketed by `[11,56/5]`. All 134
  overweight pairs were checked without finding a strict overlap.
  Three-way or higher excess depth remains unresolved.
- The seven restricted-orientation auxiliary clauses were verified at **exactly** 0° and
  45°. Their continuous-neighborhood extension has not been proved.
- Trump’s quantitative local radius is `0.004042573485` in the stated labelled, anchored
  33-coordinate sup norm.
  Its constants depend on retained computational records; the later reviewer did not
  independently rerun the entire radius generator.
  Nothing here supplies global capture into that ball.

Further qualifications matter when reading the historical sources.
The degree-eight Trump endpoint is not a proved obstruction to unavoidable-set
arguments. A fixed scalar-core ceiling is not a ceiling on every richer witness theorem.
A feasible mass-above-eleven density dual at `U`, if eventually verified, would obstruct
a mass-eleven equality density at `U`; it would not disprove Trump optimality or density
certificates below `U`. H-092/exp112 is reported in handoffs but its separate transport
is absent at the frozen source revision, so it is not independently supplied evidence.
File 10 also flags an angular-net transfer missing from one historical two-class ceiling
deduction; review that inference before reusing its quoted exact threshold.

## Offline Use and Evidence Boundary

All definitions, central proof arguments, current candidate geometry and strategic
context needed for this review are in the folder.
File 07 is independently executable: copy its Python fence to `verify_claim.py` and run
`python verify_claim.py 07-standalone-381-proof.md` with CPython 3.12 or later.
It reads the full certificate from the same document and needs only the standard
library.

The other code excerpts specify mechanisms or exact formulas; they are not a packaged
installation of `sqpack`. Large branch/modulus receipts and raw search streams are
omitted, and their reported outcomes retain explicit verification limits.
A strategic review can use those scoped outcomes as premises or identify which must be
independently re-established for a proposed proof.
It must not claim to have replayed them from this packet.

Relative links stay inside the folder.
Repository paths in backticks and links labelled “source archive” identify provenance or
optional implementation details.
They are not requests to retrieve the full repository.
Historical source statements remain dated; the editorial context in files 01 and 02
explains the current reading.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
