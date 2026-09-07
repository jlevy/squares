# BC264: One Finite Kernel Family and Its Verification Cost

This source-free design derives the kernel bound in
[H114](../../../../hypotheses/H-114-two-pose-kernel-exclusion.md), proves an obstruction
to every center-polynomial family of total degree at most three, and proposes one
eleven-feature family for a future finite necessary-constraint test.
No coefficients have been fitted, no candidate has been evaluated, and no continuum
certificate is ready.
The larger family avoids the specific cubic obstruction; that is not evidence that it
can exclude eleven squares.

The workflow entry is BC264’s insight-iteration slice in
[Session097](../../../../agent-sessions/session-097-kernel-contract-and-feature-pricing.md).
The author observed the start at 2026-09-07 20:57:51 UTC, with an original hard deadline
of 21:18:00 UTC, under `think-mkik`. This report was developed without reading the
parallel mathematical review.
The parent suggested the nine-square mixed-sign test; the derivation below checks that
suggestion independently.
The [BC265 comparison](bc-265-calibration-extension-design.md) and
[independent alternative](bc-265-calibration-extension-review.md) explain why this
interaction-kernel direction was selected instead of another calibration candidate.

## The Bound and Its Full Domain

Let a *pose* be a closed unit square contained in $[0,L]^2$, specified by its center and
an orientation modulo $\pi/2$. Two distinct poses are *compatible* when their interiors
are disjoint. Edge and corner touching are compatible; positive-area overlap is not.

A symmetric real kernel $K$ satisfies $K-1\succeq0$ when every finite pose list and
every real coefficient list obey

$$
\sum_{i,j} a_i a_j\bigl(K(P_i,P_j)-1\bigr)\ge0.
$$

Suppose $K(P,P)\le b$ for every contained pose and $K(P,Q)\le0$ for every distinct
compatible pair. For any packing of $n>0$ squares, applying the positive-semidefinite
condition to the all-ones coefficients gives

$$
n^2\le\sum_{i,j}K(P_i,P_j)
\le\sum_iK(P_i,P_i)\le nb.
$$

Thus $n\le b$. At the fixed side $L=96/25$, a certificate with $b<11$ excludes eleven
squares at that side.
It does not determine the optimum side or establish the Trump upper bound as optimal.
Positive semidefiniteness only on a sampled matrix and pair signs only almost everywhere
do not satisfy this theorem.

## An Exact Obstruction Before Any Solver

For any $L\ge3$, place nine axis-aligned unit squares at centers $(L/2+i,L/2+j)$, where
$i,j\in\{-1,0,1\}$. They are contained and pairwise compatible, including their legal
touching pairs. This is a generic symbolic control, not a measurement of a scientific
candidate.

Let $a=(1,-2,1)$ and $z_{ij}=a_i a_j$. The tensor second difference annihilates every
center monomial of total degree at most three: at least one coordinate exponent is at
most one. Consequently

$$
\sum_{i,j}z_{ij}\,\phi(P_{ij})=0
$$

for any feature vector whose restriction to this fixed-angle fiber has that degree
bound. Arbitrary orientation-only factors do not change the conclusion.

Assume $K(P,Q)=1+\phi(P)^T R\phi(Q)$ with $R\succeq0$, and put
$v_{ij}=R^{1/2}\phi(P_{ij})$. The positive and negative parts of the dependence give the
same vector:

$$
u=\sum z_{ij}^{+}v_{ij}=\sum z_{ij}^{-}v_{ij}.
$$

Each part has total weight eight: the positive part consists of the four corners with
weight one and the center with weight four; the negative part consists of four edge
centers with weight two.
Every pair across the two parts is distinct and compatible, so its feature inner product
is at most $-1$. Therefore

$$
0\le\|u\|^2
=\sum_{p,q}z_p^+z_q^-\,v_p\mathbin{\cdot}v_q
\le-64,
$$

a contradiction.
Such a family cannot meet the compatible-pair condition for any diagonal
bound, not merely for $b<11$. This rejects total-degree-three center features before an
SDP or separator is built.
It does not reject nonpolynomial features or higher center degrees.

## The Sole Proposed Family

Use centered coordinates $u=x-L/2$, $v=y-L/2$, and define

$$
z=(1,u^2+v^2,u^2v^2,\cos4\theta),\qquad
V_0=(u,v),\qquad V_1=(uv^2,u^2v).
$$

The other three scalar features are $s=\sin4\theta$, $d=u^2-v^2$, and $w=uv$. The
eleven-dimensional span is the nine center monomials of coordinatewise degree at most
two, together with the two angular features.
The $u^2v^2$ feature is the first missing tensor component in the obstruction.

The family is

$$
\begin{aligned}
K(P,Q)=1
&+z_P^T A z_Q+a_s s_Ps_Q+a_d d_Pd_Q+a_w w_Pw_Q\\
&+\sum_{i,j=0}^{1}B_{ij}\,V_i(P)\mathbin{\cdot}V_j(Q),
\end{aligned}
$$

where $A$ is a rational symmetric $4\times4$ positive-semidefinite matrix, $B$ a
rational symmetric $2\times2$ positive-semidefinite matrix, and $a_s,a_d,a_w$ are
nonnegative rationals.
There are sixteen kernel parameters and the additional rational diagonal bound $b$. This
is an exact parameterization, not a numerical choice of those parameters.

The corresponding full feature matrix is
$R=\operatorname{diag}(A,a_s,a_d,a_w,B\otimes I_2)$, in block order.
A future certificate must supply exact rational positive-semidefinite evidence: for
example, a weighted rational outer-product decomposition, or an exact LDL decomposition
with nonnegative pivots and the required zero residual rows at zero pivots.
Entrywise nonnegativity of $A$ or $B$ is neither required nor a substitute.

This form is invariant under simultaneous container symmetries.
The four entries of $z$ are invariant under $D_4$; $s$, $d$, and $w$ are its three other
one-dimensional representations; both $V_0$ and $V_1$ transform as ordinary
two-dimensional vectors.
Averaging any admissible kernel in this feature span over joint $D_4$ preserves the PSD,
diagonal and pair conditions and produces this block form.
Independently folding the two poses is not permitted.

There is a simple positive control inside this same family.
For a generic nine-node grid, let

$$
\ell_-(u)=(u^2-u)/2,\quad \ell_0(u)=1-u^2,\quad
\ell_+(u)=(u^2+u)/2,
\qquad \psi_{ij}=\ell_i(u)\ell_j(v).
$$

Then $K_{\rm grid}(P,Q)=9\sum_a\psi_a(P)\psi_a(Q)$ has values $9\delta_{PQ}$ on the
grid, and $K_{\rm grid}-1$ has coefficient matrix

$$
9I-J=\sum_{a<b}(e_a-e_b)(e_a-e_b)^T\succeq0,
$$

because $\sum_a\psi_a=1$. It is jointly $D_4$ invariant and belongs to the selected
biquadratic span. This verifies that the nine-grid contradiction no longer applies; it
supplies no non-grid diagonal or pair claim and is not a second proposed family.

## One Future Finite Discriminator

If this family is adopted prospectively, first use only axis-aligned poses.
Take the four translated grids with centers $(a+i,b+j)$, where $i,j\in\{0,1,2\}$ and
$a,b\in\{1/2,L-5/2\}$. Add the centered tight grid from the obstruction and deduplicate
physical poses. This gives at most forty-five poses, forty-five diagonal constraints and
990 unordered pair candidates.
Include a pair inequality only when $|x_i-x_j|\ge1$ or $|y_i-y_j|\ge1$, the exact
compatibility condition for axis-aligned unit squares.
Thus walls and legal touching remain in the control.
This prospective pool has not been constructed or evaluated.

The parent reports that SciPy is already available but no SDP package is declared.
The cheapest first proposer can therefore use an LP outer relaxation of PSD: impose
$v^TAv\ge0$ and $v^TBv\ge0$ for the fixed vectors $e_i$ and $e_i\pm e_j$, together with
$a_s,a_d,a_w\ge0$. These are twenty-three linear necessary PSD inequalities.
A rational Farkas or objective-bound certificate from this relaxation can reject the
family; feasibility supplies neither PSD nor a kernel candidate.
No SDP dependency is justified by this first test.
Its exact dual must retain the nonnegative weighted outer-product decomposition supplied
by these fixed test vectors.

A rational dual obstruction can reject the entire selected family even though only
axis-aligned poses were used.
To make that exit independently checkable, write

$$
M_{ii}=\phi_i\phi_i^T,\qquad
M_{ij}=\tfrac12(\phi_i\phi_j^T+\phi_j\phi_i^T).
$$

For nonnegative rational weights $\alpha_i,\beta_{ij}$ on the diagonal constraints and
proven compatible pairs, respectively, suppose

$$
\sum_i\alpha_i=1,\qquad
M=\sum_i\alpha_i M_{ii}+\sum_{ij}\beta_{ij}M_{ij}\succeq0.
$$

The weighted inequalities imply

$$
b\ge1+\sum_{ij}\beta_{ij}+\langle M,R\rangle
\ge1+\sum_{ij}\beta_{ij}.
$$

Thus $\sum\beta_{ij}\ge10$ proves $b\ge11$. Full-matrix PSD is a sufficient certificate
format; a later implementation may equivalently verify the exact joint-$D_4$ projection
blockwise, but may not silently weaken the dual condition.
The nine-clique control uses $\alpha_i=1/9$, $\beta_{ij}=2/9$ and yields $b\ge9$, with
$M=(\sum_i\phi_i)(\sum_i\phi_i)^T/9$.

The independent reader must reconstruct the fixed poses, exact features and each claimed
compatibility, then verify the weights, normalization and PSD identity.
Neither solver status nor a sampled eigenvalue is acceptance.
An exact obstruction closes this family.
A feasible LP relaxation, an unresolved result or a timeout is inconclusive and ends
this proposed discriminator.
Any later SDP, additional constraints or degree change requires a new decision.
Only a rational kernel candidate with actual PSD evidence could justify continuum
pricing.

## What a Complete Continuum Proof Would Cost

The exact domain is compact but not a simple pair box.
Use $t\in[0,1]$ as a full quarter-turn chart, retaining both equivalent endpoints, with
$C_t=(1-t^2)/(1+t^2)$, $S_t=2t/(1+t^2)$, and $h_t=(C_t+S_t)/2$. Each center satisfies
$h_t\le x,y\le L-h_t$. The angular features are rational:

$$
\cos4\theta=\frac{1-28t^2+70t^4-28t^6+t^8}{(1+t^2)^4},\qquad
\sin4\theta=\frac{8t-56t^3+56t^5-8t^7}{(1+t^2)^4}.
$$

For two poses, let $\Delta$ be their center difference.
Their interiors are disjoint exactly when one of the eight signed separating-axis
inequalities holds:

$$
\sigma n\mathbin{\cdot}\Delta\ge
\frac{1+|\cos(\theta-\varphi)|+|\sin(\theta-\varphi)|}{2},
$$

where $\sigma\in\{-1,1\}$ and $n$ runs through the two unit edge axes of each square.
In the quarter-turn chart the cosine difference is nonnegative; splitting the sign of
the sine difference gives at most sixteen closed branches.
Touching is the equality case.
Branch overlaps and duplicate orientation endpoints do not permit omitting any branch.

A complete verifier must prove $b-K(P,P)\ge0$ on the three-variable contained-pose
domain, and $-K(P,Q)\ge0$ on all sixteen six-variable compatible-pair branches.
Clearing the strictly positive angular denominators gives the following conservative
tensor degree bounds:

- Diagonal: degrees at most $(4,4,16)$ in $(u,v,t)$, or 425 tensor coefficients per box.
- Pair: degrees at most $(2,2,8,2,2,8)$, or 6,561 tensor coefficients per box.

These are symbolic size bounds, not generated coefficients or measured performance.
They do not bound the number of boxes.
A sign proof over a surrounding box alone is usually inappropriate: the box includes
overlapping pairs on which the desired sign need not hold.
A complete proof must retain the wall and separating-axis constraints, through an exact
domain parameterization or independently checked constrained polynomial certificates.
Zero margins on touching strata can defeat plain Bernstein subdivision and may require
exact boundary factors.
The current low-dimensional Bernstein tools are not a ready six-dimensional continuum
checker.

The smallest useful future investment is therefore the finite discriminator, not a
general hierarchy. A planning estimate is thirty author-minutes for a narrowly scoped
rational PSD/constraint instrument and controls, thirty independent review-minutes, and
fifteen minutes for protocol integration: about seventy-five agent-minutes before a
separately declared run.
A prospective run could cap its proposer at sixty seconds and its independent exact
certificate check at sixty seconds, once each.
These are proposed ceilings, not measurements or authority to launch; dependencies and
solver availability have not been inventoried here.

No credible total wall-clock price for the complete continuum proof is available without
a rational candidate and its margins or boundary factors.
That missing price is a readiness blocker, not a reason to assume a two-hour universal
proof. Even after a finite candidate with exact PSD evidence, fund at most a separate
thirty-minute source-free continuum-contract assessment before any verifier build.
Kill that continuation if it cannot specify a finite complete domain cover or exact
constrained certificate with independent checking and bounded controls.
The finite obstruction exit remains useful without such a continuum engine, but rejects
only this feature family, not H114 in general or any packing bound.

## Handoff and Evidence

The proved new result is the mixed-sign obstruction for all total-degree-three center
feature spans on a fixed-angle fiber.
The eleven-feature family, rational pool and dual format are prospective designs.
No scientific executable, source constructor, candidate evaluation, SDP, test suite, or
geometry computation was run.
No experiment or hypothesis ID was allocated.
Only this report was written; the documentation pass keeps definitions, scope and the
unresolved continuum price explicit.
Flowmark is the only requested mechanical check.
The coordinator owns independent mathematical admission and any later registration.

## Independent Reader Review After the Build

This separate `think-ebh1` review began at the observed clock 2026-09-07 21:48:15 UTC,
after the producer froze at 21:45:55 and the independently authored reader froze at
21:46:33. Its hard deadline is 22:00 UTC. The first-pass design and its no-execution
statement above remain historical evidence for that earlier allocation.
This review read the complete [reader](../../../../../devtools/check_kernel_axis_lp.py),
its [tests](../../../../../tests/test_check_kernel_axis_lp.py), the frozen producer for
wire consistency, [H125](../../../../hypotheses/H-125-biquadratic-two-pose-kernel.md),
and the post-freeze admission contract.

**GO for this reader’s finite objective-certificate soundness and source-free
readiness.** No mathematical or implementation blocker was found.
This does not authorize a scientific invocation or accept H125.

The reader independently forms $M=\sum_i\alpha_i\phi_i\phi_i^T+\sum_{i<j}\beta_{ij}
(\phi_i\phi_j^T+\phi_j\phi_i^T)/2$. Its invariant block is the full $4\times4$ submatrix
$M_A$. For the two vector copies, it sums both spatial coordinates and forms
$T_{rs}=\operatorname{tr}(M^V_{rs})$. Consequently the vector contribution is
$\langle T,B\rangle$, with no extra factor of one-half.
The symmetrization factor one-half is already present in each pair term.
The mixed-vector control, whose exact $T$ is
$\left(\begin{smallmatrix}34&62\\62&106\end{smallmatrix}\right)$, exercises this
distinction. The three scalar contributions are checked separately.

Exact Schur elimination rejects negative pivots and rejects a zero pivot with a nonzero
remaining row. Positive pivots update the symmetric residual matrix using exact rational
arithmetic. Together with nonnegative scalar projections, these checks imply
$\langle M,R\rangle\ge0$ for every coefficient matrix in the fixed family.
The reader also requires $\alpha\ge0$, $\sum\alpha=1$, positive sparse $\beta$ and the
exact identity $\texttt{bound}=1+\sum\beta$. Thus its accepted certificate proves the
lower bound derived above.

The frozen seven-key packet carries no direction multipliers or supplied matrices.
The earlier admission’s proposed reconstruction of all twenty-three test-direction
decompositions is unnecessary for this admitted direct-PSD format: the reader
reconstructs the projection from the weights and checks its PSD exactly.
The twenty-three directions remain the frozen proposer’s necessary LP inequalities, not
additional premises of the objective certificate.
This clarification preserves the earlier proposal while recording the implementation
actually reviewed.

Source binding is complete at the code level.
The reader independently generates the four translated tight grids and the centered
grid, deduplicates by exact coordinates, sorts them, and fixes the side at $96/25$. The
packet must match the entire roster, including zero-weight poses.
Each selected pair must have $|x_i-x_j|\ge1$ or $|y_i-y_j|\ge1$; equality correctly
admits touching. Unweighted pairs need not appear in the sparse dual.
Every listed unit square must satisfy the closed containment inequalities.
The eleven-feature order, including the repeated one and angular zero on this axis
fiber, matches the frozen family.

The parser requires the seven exact top-level keys and exact sparse-entry keys,
canonical rational strings, native integer indices excluding booleans, sorted distinct
poses and sorted distinct pairs with $i<j$. It rejects duplicate JSON keys,
floating-point JSON values and constants, excessive nesting and nonregular inputs.
The file reader admits at most 2 MiB; the algebra admits at most forty-five poses and
990 sparse pairs, 128-bit source rationals, 4,096-bit certificate rationals and
32,768-bit accumulated arithmetic.
These refusal bounds do not substitute for the external whole-child timeout.
The producer’s stricter 4,096-bit arithmetic limit can cause an inconclusive
reconstruction but does not create a reader acceptance gap.

The scientific CLI is only `--input PATH`. It has no synthetic source, side or threshold
override. The separate caller-bound synthetic API cannot return
`scientific_family_refuted=true`. A certificate below eleven is refused by the
scientific path, and the error path prints only stderr and exits two.

The independent checks used the project Python 3.14 interpreter:

| Check | Result | Outer wall | User CPU | System CPU |
| --- | --- | --- | --- | --- |
| Reader’s focused pytest suite | 55 passed; pytest reported 0.13 seconds | 0.58 seconds | 0.33 seconds | 0.10 seconds |
| Ruff check | Zero findings | 0.11 seconds | 0.02 seconds | 0.03 seconds |
| Ruff format check | Both files already formatted | 0.05 seconds | 0.02 seconds | 0.01 seconds |
| BasedPyright | Zero errors, warnings or notes | 1.26 seconds | 1.74 seconds | 0.22 seconds |

The tests forbid the scientific constructor.
They cover the exact nine-bound control, threshold refusal, block-trace factors,
singular PSD, altered duals, negative scalar projection, full source mutations,
touching, overlap, normalization, lexical limits, input bytes and fixed-CLI refusal.
No scientific source agreement, positive scientific CLI invocation, target solve or
target packet was evaluated.
Those remain prospective conditions, not missing evidence hidden by the control count.
No code or test file was edited during this review.

For the proposed later protocol, allow one fixed producer under an external sixty-second
TERM deadline and a separately disclosed two-second KILL grace.
Only an actual producer exit zero and a complete packet with bound at least eleven may
trigger the one independent reader, under the same external limits.
Accept a family refutation only after actual reader exit zero and a complete receipt
with `status=verified_objective_bound`, the fixed source and side, `minimum_bound=11`,
bound at least eleven, `projected_psd_verified=true`, `scientific_family_refuted=true`,
and `new_packing_bound=false`. Any other result remains unresolved.
No retry or target-informed repair follows.
The KILL grace means this is not a strict sixty-second total-runtime promise.

## Conditional Scope of an Axis-Only Obstruction

A source-free review on September7,22:28:34–22:33:23 UTC (289 seconds) establishes
the following conditional extension, checked by the coordinator. Exp129 never ran;
there is no biquadratic obstruction to promote yet.

Let $\mathcal B=\operatorname{span}\{u^iv^j:0\le i,j\le2\}$. Suppose an enriched
kernel has $K-1=\psi(P)^TQ\psi(Q)$, with $Q\succeq0$, and every axis restriction
$\psi_j(u,v,0)$ lies in $\mathcal B$. Writing those restrictions as $F\eta$ gives
the PSD axis coefficient matrix $F^TQF$ in the basis
$\eta=(1,r,p,d,w,V_0,V_1)$ defined above. Jointly average this axis kernel over
container $D_4$. PSD, the same diagonal bound and all compatible-pair inequalities
survive, including touching. The enriched family need not itself be closed under
symmetry, and no independent folding is allowed.

This representation has three trivial copies, two distinct scalar characters and
two standard-vector copies. Its invariant PSD cone is exactly $A_3\succeq0$,
$B_2\succeq0$, $a_d,a_w\ge0$, with vector block $B_2\otimes I_2$: eleven
coefficient parameters in a nine-dimensional feature span. H125 realizes every
such axis kernel by choosing $A_4=\operatorname{diag}(A_3,0)$ and $a_s=0$;
on axes its four invariant features are $(1,r,p,1)$.

Consequently, a sound **axis-only objective certificate** for H125 proving
$b\ge1+\sum\beta\ge11$ would also exclude $b<11$ in every enriched kernel just
described. Exact rational certificate data bound real PSD coefficients, not merely
rational ones. Angular features vanishing on axes or restricting into this particular
span cannot evade that certificate. Axis features outside the span are not covered.

The qualification is essential: arbitrary full-angle nonexistence within H125 would
not transfer. The matrix realizing the averaged axis kernel need not satisfy its
full-angle constraints. This conditional statement neither supplies the missing
objective certificate nor decides H125; the unconditional cubic obstruction remains
a separate result. No feature expansion or additional allocation follows from it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
