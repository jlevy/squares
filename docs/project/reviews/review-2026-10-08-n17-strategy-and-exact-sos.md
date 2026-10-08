# n17 Strategy: Shared Geometry, Exact Certificates and SOS

October 8, 2026. Astra mathematical review for `think-bid9`, using PR404 at `ecb0bf82`,
main at `f0ec5b663`, the frozen metadata and BB lifetime patches, and the primary
sources linked below.
Proposed experiments have not run.

**Complete the first-eight shared-centre LP test, then test a small cycle with exact
nonlinear constraints if the LP survives.** Incorporate external certificates by
measured relevance and complete verification.
Sum-of-squares (SOS) is a credible new way to certify such nonlinear constraints.
It does not currently justify replacing that sequence with a global seventeen-square
semidefinite program.

## What the Evidence Has Changed

The [verified lower bound](../../../packing/frontier/results.yaml) remains
$s(17)>4.66044275$, established here by the October 5 R071 replay.
Its increase over R068 was $0.00000275$; the latest sessions added none.
The outward endpoint ceiling is $4.6755300936045509516342148538535054$, leaving
approximately $0.01508734$. The unchanged charge has only $2.5\times10^{-8}$ further
runway. A global advance needs a stronger charge or a different proof.
The latest main merge changes neither that record nor the admitted n17 ledger.

Three kinds of work have paid off:

- **Exact, scoped exclusions:** Tail A/B removed sixteen states/two symmetry classes.
  PR404 therefore has 60 admissions and 36,768 states/4,683 classes, versus main’s 58
  and 36,784/4,685. These are distance-eight exclusions; the selected distance-two
  residue stays at 95 classes/744 states.
  Exclusions reduce a proof obligation; they raise the lower bound only when a complete
  covering argument composes them.
- **Conditional geometric implications:** regional ownership proved restrictions on 22
  rows at $h=1/512$ and all 25 at $h=2^{-23}$; two-child propagation removed $15/32$ of
  owner6’s half-angle parameter.
  Here $h$ bounds both centre coordinates and $\tau=\tan(\theta/2)$. No theorem places
  every candidate packing in these guards.
  These are useful lemmas awaiting a consumer, not evidence of global capture.
- **Cheap tests of weaker models:** exact diagnostics establish which information was
  lost.
  [Exp313/314](../../../docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md)
  found 102 proper octagon pair cuts and 114 proper disk cuts among 228 relevant pairs,
  but no whole pair-difference domain inside the open unit disk.
  Each pair can survive separately.
  The next question is whether shared centres can satisfy all pairs together.

The unchanged coarse contact-rank filter, whole-square-envelope and four-corner capacity
relaxation all left the 95 classes alive.
The four-corner test guaranteed at most seven owners per window, far below the
contradiction threshold above ten.
Repeated one-context propagation gained nothing; case-preserving propagation gained
$1/64$ in one child and zero in the combined survivor union.
Retire those unchanged operators.
These complete misses justify preserving more joint geometry; they do not refute the
underlying normalization or n11 theorems.
[Session186 evidence and dispositions](../../../docs/project/research/research-2026-10-07-n17-session-186-w3-strategy.md).

## External Evidence and the Two Patch Reviews

I independently inspected the metadata algorithm and reconstructed its retained result.
Its 35 classes are distinct: 33 reported patterns and two #358 companions.
The #413 union has hypothetical applicability to 2,234 residual classes/17,604 states,
but only **row 23** reaches the hard tail: one class/eight states, mask 1965787. None
reaches the frozen first eight.
Row 33 applies individually to 192/1,520; its marginal after rows 1–32 is 76/608. Rows
15, 19 and 26 are smaller than Tail A/B; excluding those larger assignments does not
prove the smaller patterns impossible.
The D4 containment directions, orbit weights and union accounting are correct.
Five focused controls and a fresh reconstruction passed; no admission follows.
[Contributor’s corresponding comparison](https://github.com/jlevy/squares/issues/413#issuecomment-6064503349).

The later
[row14 correction](https://github.com/jlevy/squares/issues/413#issuecomment-6064272233)
explains the 22 verified/11 computed total.
The
[FULL correction](https://github.com/jlevy/squares/issues/413#issuecomment-6064443079)
leaves unmodified standing-FULL reports for rows 1–2 and #358’s two classes; rows 3–4
used the parallel driver’s node checks and the fast verifier.
The refreshed snapshot retains these corrections; that refresh adds no verification.
Row 23 remains computed/unpublished.
Ask for that package’s availability first.
The estimated 480 GB row33 certificate remains ungenerated and reaches none of the 95.

The #445 patch correctly waits for a node’s own scheduled check **and** its last
selected child’s use before eviction, including reverse IDs within a chunk and failure
paths.
Seven independent controls passed in 0.85 seconds; the writer additionally reports
sixteen old/new receipt matches apart from time.
Its 65-node weak-reference control reduces retained records at chunk boundaries from 32
to one. Pass 1 remains linear in tree size.
This is a useful memory repair, without a demonstrated whole-certificate speedup or
large-tree memory guarantee.

C2’s 480.468-second RSS-monitor stop, missing bootstrap dependencies, and the cold GMP
build’s missing-file/getcwd failures are execution failures, not negative mathematical
results. Native receipt execution remains unverified; the storage/build cause remains
undiagnosed. Keep those repairs bounded beside research.
Retained engineering evidence:
[BB lifetime repair, PR452](https://github.com/jlevy/squares/pull/452) and
[native receipt publication, PR453](https://github.com/jlevy/squares/pull/453).

## What SOS Would Actually Add

Maaz’s [article](https://www.mmaaz.ca/writings/sostactic.html) and
[Sostactic package](https://github.com/mmaaz-git/sostactic) describe numerical SDP
search followed by exact certificate reconstruction and Lean checking.
For constraints $g_i(z)\ge0$ and equalities $h_j(z)=0$, an emptiness certificate can be

$$
-1=\sigma_0(z)+\sum_i\sigma_i(z)g_i(z)+\sum_j\lambda_j(z)h_j(z),
$$

where each $\sigma_i$ is a nonnegative weighted sum of polynomial squares.
An exact identity makes a satisfying point impossible.
Equality multipliers require an explicit adapter or encoding by both signs of each
equality; the package’s documented interface takes inequality constraints.
Restricting multiplier bases preserves soundness of a found identity but can lose
certificates. [Sparse SOS](https://epubs.siam.org/doi/10.1137/050623802) makes such
structure useful; it does not grant completeness to an arbitrary small template.

The following packing encoding is my derivation.
Use centres $c_i=(x_i,y_i)$ and axes $u_i=(a_i,b_i)$, $v_i=(-b_i,a_i)$, with
$a_i^2+b_i^2=1$. Square symmetry permits $a_i,b_i\ge0$ with the closed quarter-turn
chart retained. All four vertices must lie in $[0,L]^2$. For a chosen signed normal $n$
from square $i$'s axes, separation from square $j$ requires

$$
2n\cdot(c_j-c_i)\ge1+\epsilon\,n\cdot u_j+\eta\,n\cdot v_j
\quad\text{for every }\epsilon,\eta\in\{-1,1\}.
$$

The maximum of the four right sides supplies the absolute projection widths.
There are eight signed face-axis alternatives per pair, using either square’s axes.
Thus packing is a finite **disjunction of nonconvex quadratic systems**, with 136 pair
disjunctions. Dropping the alternatives or replacing squares by centre-distance
constraints gives a relaxation.
Boundary equality must remain allowed.
There are 68 real variables at fixed cap, or 69 including $L$, before elimination or
selector variables. Proven coordinate bounds make each closed branch compact; add an
explicit valid ball constraint when invoking an Archimedean SOS convergence argument.
Mere compactness should not be confused with the quadratic module being Archimedean.

Derived dense free-Gram dimensions are $\binom{m+r}{r}$ at order $r$:

| Model | Variables $m$ | Order 2 | Order 3 |
| --- | ---: | ---: | ---: |
| Three centres, incircle necessary conditions | 6 | 28 | 84 |
| Seventeen centres only | 34 | 630 | 7,770 |
| Seventeen centres and rotations, fixed cap | 68 | 2,415 | 57,155 |

These are matrix dimensions, not scalar counts or runtime forecasts; every multiplier
adds another block. The 2,415 block alone has 2,917,320 symmetric entries.
Eliminating rotations with half-angle parameters reduces variables but raises degrees
after positive denominators are cleared.
It does not remove the combinatorial burden.

Existing BB already supplies checked interval branches and exact closure decisions.
The new contribution would be an **SOS leaf using several owners jointly**, possibly
replacing extensive subdivision with one polynomial identity.
B2/B2d improves branch selection without adding this logical strength.
A local SOS lemma near the endpoint is another option, but needs a complete local branch
cover and a separate global localization theorem.

## Numerical SDP to Exact Proof Is the Main Risk

Round a numerical Gram matrix to rationals, then solve the coefficient equations
exactly. That projection can destroy positive semidefiniteness.
[Peyrl–Parrilo](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf)
prove recovery under strict feasibility with sufficient numerical accuracy.
That hypothesis concerns the Gram representation; a visibly positive target does not
automatically supply a well-conditioned Gram matrix in the chosen basis.

At an exact optimum, active contacts and zeros commonly force singular Gram blocks.
Small negative eigenvalues can then reflect either roundoff or genuine invalidity.
Higher precision alone may not solve the problem.
Candidate rational nullspaces and face reduction can help, but their identities and
resulting certificate must be checked exactly.
[Monniaux–Corbineau](https://arxiv.org/abs/1105.4421) specifically address degenerate
certificate generation.
General rational SDPs need not have rational solutions, so rational rounding is a method
with a failure mode, not a theorem of success.

Exact checking itself need not compute algebraic eigenvalues.
The inspected
[Python source](https://raw.githubusercontent.com/mmaaz-git/sostactic/main/python/sos.py)
already checks rational LDL decompositions, including zero-pivot consistency, and
reconstructs weighted squares.
Retain exact coefficient equality, nonnegative weights and independent reconstruction.
Its dense SymPy coefficient matrix and exact row reduction occur before numerical
solving; total affine-system size needs a preflight limit even for six variables.
The
[Lean polynomial development](https://github.com/mmaaz-git/sostactic/blob/main/Sostactic/Polynomials.lean)
also addresses denominator zeros.
The global density argument for rational-function certificates cannot be transplanted
without review to a lower-dimensional constrained set where the denominator may vanish
identically.

The [reported n17 algebraic endpoint](https://github.com/jlevy/squares/issues/419) has
degree 18 in the source catalogue, pending the dedicated intake.
For exact optimality, an SOS proof involving $L-S^*$ needs either arithmetic in the
specified ordered algebraic field or a root variable with its polynomial and isolating
interval. Rational rounding of $S^*$ changes the theorem.
A certificate below one rational threshold is easier to seek, but any finite list of
such thresholds still leaves a gap to $S^*$.
[Nie’s finite-convergence theorem](https://arxiv.org/abs/1206.0319) requires additional
optimality conditions; none has been established for all packing minimizers here.
There is no demonstrated low-degree certificate or finite practical hierarchy level.

Lean checks only the theorem encoded.
Preserve the connection from actual squares, closed boundaries, all branch alternatives
and named cells to the polynomial premises.
Pin and review imported code, reject unresolved goals or extra unapproved axioms, and
retain certificate/checker identity.
A source flag saying `lean_packs` is not a lower bound or local-minimum theorem.

## Bounded Next Tests

First finish the
[existing LP readiness contract](../../../docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md):
same 17 centres (34 coordinates) across all 136 pair hulls, exact endpoint feasibility,
first eight canonical assignments, bounded exact reconstruction.
Accept only a rational primal satisfying every row, or exact Farkas weights $y\ge0$,
$A^Ty=0$, $b^Ty<0$ for the system $Ax\le b$. Eight feasible cases retain those eight;
they do not retire all 95.

For a new SOS pilot, take the first exactly certified LP survivor and freeze one triple
of its original cells before SDP work.
Rank triples by the sum of their three exact pairwise maximum squared centre distances,
smallest first, breaking ties by cell indices.
This selects tight pair domains without asserting a joint obstruction.
The six variables are its centres in the reconstructed polygons $E_i$; require
$\|c_i-c_j\|^2-1\ge0$ for all three pairs.
These are necessary square-packing constraints with no guessed contact pattern.
First run the simpler exact vertex test $\max\sum_{i<j}\|c_i-c_j\|^2<3$; if it succeeds,
keep that proof. Otherwise attempt Putinar order 2, and order 3 only if preflight
permits.

Proposed limits: at most 10,000 scalar Gram unknowns and two million coefficient matrix
entries; 300 seconds end-to-end per eligible order, including exact affine construction,
120 seconds fresh checking, 4 GiB sampled current RSS per process, 8 MiB output and
4,096-bit rational coefficients.
Freeze actual source, controls and commands before registering a target.
Controls include the impossible three-centres-on-a-unit-segment cycle, a feasible
touching triple, an accepted endpoint triple, singular PSD matrices, a corrupted
identity, a negative weight, omitted constraints and a forced resource stop.

Accept only a fresh exact contradiction with the original-cell and D4 joins, or an exact
feasible triple retained as a relaxation witness.
Numerical infeasibility, failed rational reconstruction and resource exhaustion remain
unresolved.
A completed unsuccessful search retires only that frozen basis/degree recipe,
not SOS. A feasible triple retires that triple obstruction.
Any move to four owners, new bases or algebraic coefficients is a new registered slice.

## Allocation and Uncertainty

The estimates below are agent effort for the next reviewable slice, not elapsed proof
completion forecasts.
Parallel work can shorten wall time but does not remove dependencies.

| Priority and Slice | Estimated Effort / Compute | Decision It Can Establish |
| --- | --- | --- |
| 1. Finish first-eight shared-centre LP | 4–8 agent-hours; existing proposed 120-second construction and 120-second fresh-check envelope, to validate in controls | Exact exclusions or exact survivors of a materially stronger shared model. No runtime feasibility yet measured. |
| 2. Row23 package and smallest complete BB replays | 1–3 agent-hours intake before launch; historical contributor C2/C1 checks were 2,220/5,906 seconds, not predictions after changes | One candidate hard-tail class and independently admitted easier classes. Package availability and RSS-monitor repair are prerequisites. |
| 3. One six-variable SOS pilot | 6–12 agent-hours for adapter, exact checker and controls; at most ten target solver minutes plus fresh checking as above | Whether cycle constraints yield a compact new exact obstruction. Certificate existence and exactification are unknown. |
| 4. Exact endpoint intake, then one local lemma | 2–6 agent-hours for packet/root/geometry audit; a separate 1–3 day bounded local-proof study only after that | Endpoint feasibility and possibly local exclusion of improvement; global capture remains missing. |
| 5. New global charge or structural inequality | One 4–8 agent-hour derivation slice before a compute allocation | A changed inequality with a credible global quantifier. Polishing the unchanged charge is exhausted at the scale of the gap. |

Keep direct all17 SOS as a research architecture until a small pilot measures useful
degree, block structure and exactification cost.
Preserve creative alternatives such as SOS-assisted local capture or a new globally
valid charge, but require each to name its missing geometric implication.
Current evidence supports a sequence of informative decisions; it does not support an
optimality-proof ETA.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
