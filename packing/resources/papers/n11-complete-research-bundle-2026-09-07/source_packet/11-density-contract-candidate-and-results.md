# Full-Size Densities: Contract, Candidate and Next Test

Read the weak-duality contract before interpreting the 56/5 candidate. Necessary finite rows and the completed pair exclusion do not certify almost-everywhere depth. The candidate is specified exactly at the end, so further geometric analysis requires no repository access.

<a id="source-1"></a>

## Source 1: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md`

Snapshot `4d305597a505`, source lines 1-end.

<a id="source-1-bc-242-full-size-density-proof-contract"></a>

### BC-242 Full-Size Density Proof Contract

Status: **author draft complete, with a self-contained weak-duality derivation;
source-distinct theorem review, strong duality, attainment, a singular-mass extension, a
continuum primal certificate, and every numerical BC-243 result remain open.**

This packet supplies BC-242’s (`think-9xxh`) author draft at theorem-contract scope;
coordinator and source-distinct review disposition remain open.
It fixes which finite objects have valid lower- or upper-bound semantics before any
density value is interpreted.
It neither runs BC-243 nor proves a global eleven-square packing theorem.

<a id="source-1-frozen-scope-and-inputs"></a>

#### Frozen scope and inputs

- Official T+0: `2026-09-06T03:31:00Z`.
- Launch commit: `c55726e1e885227f63110131c0a914665175ff89`.
- Preregistration commit: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`.
- Agenda 026 SHA-256:
  `096470755cb056d6dcd9d103d4233819d03f8bff9035e1027d213ca51ab4cb49`.
- Frozen Trump witness SHA-256:
  `3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9`.
- Frozen BC-199 result SHA-256:
  `db124b9956d8051682388cbba3b16772e65406a0003debba1c92b915c0c489a8`.
- Frozen exp-013 result SHA-256:
  `60a4b7c48034b37063509a8a641974ed5eae86dccd056e9cbc6cf2fd7f2f0661`.

The exact Trump placement supplies a retained dual control of mass eleven.
It is an input to the pilot contract, not evidence that a mass-eleven primal density
exists or that all compatible eleven-tuples have been classified.

<a id="source-1-placement-space-and-primal"></a>

#### Placement space and primal

Fix a side length \(L>0\). Let

\[
C_L=[0,L]^2,\qquad Q=[-1/2,1/2]^2,
\]

and let \(\mathbb T_4=\mathbb R/(\pi/2)\mathbb Z\) be the compact angle quotient for a
square. A placement \(p=(c,\theta)\) represents the closed unit square

\[
S_p=c+R_\theta Q.
\]

The admissible placement space is

\[
P_L=\{(c,\theta)\in C_L\times\mathbb T_4:S_p\subseteq C_L\}.
\]

The four corner-containment inequalities are continuous in \((c,\theta)\), so \(P_L\) is
a closed subset of the compact space \(C_L\times\mathbb T_4\). Thus \(P_L\) is compact.
No optimizer-attainment claim follows from that fact alone.

For \(\rho\in L^1_+(C_L)\), define

\[
F_\rho(p)=\int_{S_p}\rho(x)\,dx
\]

and the absolutely continuous covering value

\[
\tau_{\mathrm{ac}}(L)=
\inf\left\{
\int_{C_L}\rho(x)\,dx:
\rho\in L^1_+(C_L),\ F_\rho(p)\geq1\text{ for every }p\in P_L
\right\}.
\]

The normalization is one unit of density mass on every closed full-size placement.
Square boundaries are Lebesgue null, so changing a representative of \(\rho\) on a null
set changes neither feasibility nor objective value.
For \(L\geq1\), the constant density \(\rho\equiv1\) is feasible and has mass \(L^2\);
for \(L<1\), \(P_L\) is empty and the value is zero.
Thus the Trump-side application has a nonempty finite primal problem.

The coverage functional is continuous on \(P_L\). Indeed, if \(p_k\to p\), then the
Lebesgue area of \(S_{p_k}\mathbin\triangle S_p\) tends to zero.
Absolute continuity of the \(L^1\) integral gives

\[
|F_\rho(p_k)-F_\rho(p)|
\leq\int_{S_{p_k}\mathbin\triangle S_p}\rho(x)\,dx\longrightarrow0.
\]

This continuity supports a compact pose-cover proof, but it does not turn a finite
sample into a continuum certificate.

<a id="source-1-almost-everywhere-dual-and-weak-duality"></a>

#### Almost-everywhere dual and weak duality

Let \(w\) be a finite nonnegative Borel measure on \(P_L\). Its closed-square overlap
depth is

\[
d_w(x)=\int_{P_L}\mathbf 1_{S_p}(x)\,dw(p).
\]

The incidence relation \(\{(x,p):x\in S_p\}\) is closed, hence the integrand is Borel
measurable. Call \(w\) dual-feasible when

\[
d_w(x)\leq1\quad\text{for Lebesgue-almost-every }x\in C_L.
\]

Define

\[
\nu_{\mathrm{ae}}(L)=
\sup\{w(P_L):w\text{ is dual-feasible}\}.
\]

<a id="source-1-weak-duality-theorem"></a>

##### Weak-duality theorem

For every primal-feasible \(\rho\) and dual-feasible \(w\),

\[
w(P_L)\leq\int_{C_L}\rho(x)\,dx.
\]

Consequently \(\nu_{\mathrm{ae}}(L)\leq\tau_{\mathrm{ac}}(L)\).

**Proof.** Primal feasibility, nonnegativity, and Tonelli’s theorem give

\[
\begin{aligned}
w(P_L)
&\leq\int_{P_L}F_\rho(p)\,dw(p)\\
&=\int_{C_L}\rho(x)
   \left(\int_{P_L}\mathbf 1_{S_p}(x)\,dw(p)\right)dx\\
&=\int_{C_L}\rho(x)d_w(x)\,dx\\
&\leq\int_{C_L}\rho(x)\,dx.
\end{aligned}
\]

All integrands are nonnegative, so no unproved integrability interchange is hidden in
the argument. \(\square\)

An interior-disjoint packing \(p_1,\ldots,p_m\) yields the atomic measure
\(w=\sum_i\delta_{p_i}\). Outside the finite union of square boundaries, at most one
closed square contains any point.
That union is Lebesgue null, so \(w\) is dual-feasible and has mass \(m\). In
particular, the exact Trump placement supplies the retained lower bound

\[
11\leq\nu_{\mathrm{ae}}(L_{\mathrm{Trump}})
\leq\tau_{\mathrm{ac}}(L_{\mathrm{Trump}}).
\]

This is why `packing/src/sqpack/fractional/ceiling.py`’s pointwise closed-set depth
checker is not a verifier for this dual: it intentionally rejects touching squares,
whereas the theorem ignores only the proved null union of their edges and corners.
It must not be weakened or relabelled; BC-243 needs a separate a.e.-depth instrument.

<a id="source-1-conditional-equality-consequences"></a>

#### Conditional equality consequences

No strong-duality or optimizer-attainment theorem is asserted.
If, in a later result, a primal optimizer \(\rho\) and a dual optimizer \(w\) exist and
have equal objective value, use the exact gap decomposition

\[
\begin{aligned}
\int_{C_L}\rho\,dx-w(P_L)
&=\int_{C_L}\rho(1-d_w)\,dx\\
&\quad+\int_{P_L}(F_\rho-1)\,dw.
\end{aligned}
\]

Both terms on the right are nonnegative, so they vanish separately and give

\[
F_\rho(p)=1\quad w\text{-almost everywhere},
\qquad
\rho(x)(1-d_w(x))=0\quad\text{almost everywhere}.
\]

For the unit-atomic Trump dual these conditions say that each of the eleven retained
placements has coverage exactly one and that \(\rho\) vanishes almost everywhere off the
saturated union.
They do not determine \(\rho\), exclude another compatible eleven-tuple,
or prove the equality classification required by BC-244.

Conversely, any packing of eleven interior-disjoint unit squares forces every
primal-feasible density to have mass at least eleven: sum the eleven coverage
inequalities and use the fact that their overlaps are boundary-null.
Therefore a certified primal mass below eleven would contradict the retained exact
packing and would expose an error in the certificate or frozen inputs.

<a id="source-1-singular-measures-and-boundary-charges"></a>

#### Singular measures and boundary charges

The weak-duality argument above is deliberately restricted to \(\rho(x)\,dx\). Suppose a
later variant admits a finite nonnegative Borel measure \(\mu\) on \(C_L\), with primal
constraints \(\mu(S_p)\geq1\). Tonelli then uses the closed depth against \(\mu\):

\[
\int_{P_L}\mu(S_p)\,dw(p)=\int_{C_L}d_w(x)\,d\mu(x).
\]

Thus the same uncorrected weak-duality inequality is valid only after certifying
\(d_w\leq1\) \(\mu\)-almost everywhere.
A Lebesgue-a.e. depth certificate does not provide that fact.

If an instrument certifies only the open-interior depth

\[
d_w^\circ(x)=\int_{P_L}\mathbf 1_{\operatorname{int}S_p}(x)\,dw(p)\leq1
\quad\mu\text{-almost everywhere},
\]

then the exact identity is

\[
\int_{P_L}\mu(S_p)\,dw(p)
=\int_{C_L}d_w^\circ(x)\,d\mu(x)+B(\mu,w),
\]

where

\[
B(\mu,w)=\int_{P_L}\mu(\partial S_p)\,dw(p)\geq0.
\]

It yields only \(w(P_L)\leq\mu(C_L)+B(\mu,w)\). Recovering the desired bound requires an
exact proof that the boundary term is zero, such as \(\mu(\partial S_p)=0\) for every
admissible placement, or a separately stated and verified replacement inequality.
Wall-supported or other singular mass can charge square boundaries, so it is refused by
this contract absent that theorem.

<a id="source-1-wall-strata-and-stationarity"></a>

#### Wall strata and stationarity

Write the placement-space containment constraints locally as \(h_k(p)\geq0\). If
\(\rho\) is primal-feasible and \(F_\rho(p)=1\), then \(p\) is a global, hence local,
minimum of \(F_\rho\) on \(P_L\). If additional regularity makes \(F_\rho\)
differentiable on a selected feature branch, its first-order condition has the form

\[
\nabla F_\rho(p)-\sum_{k\in A(p)}\lambda_k\nabla h_k(p)=0,
\qquad \lambda_k\geq0,
\]

subject to the applicable constraint qualification; without that qualification the
corresponding Fritz–John form is required.
Hence the derivative belongs to the cone generated by active wall rows.
At a wall placement it need not be zero in the ambient centre-angle coordinates.

On a fixed trigonometric sign branch, put \(r(\theta)=(|\cos\theta|+|\sin\theta|)/2\)
and use

\[
h_\ell=c_x-r,\quad h_r=L-c_x-r,\quad
h_b=c_y-r,\quad h_t=L-c_y-r.
\]

The centre and angle equations are then

\[
\partial_{c_x}F_\rho=\lambda_\ell-\lambda_r,
\qquad
\partial_{c_y}F_\rho=\lambda_b-\lambda_t,
\qquad
\partial_\theta F_\rho=-r'(\theta)
(\lambda_\ell+\lambda_r+\lambda_b+\lambda_t),
\]

with inactive-wall multipliers zero.
At trigonometric or density-feature ties these smooth equations are replaced by the
retained branch or nonsmooth condition below.

For a piecewise density, wall, density-cell, vertex, and edge ties can make \(F_\rho\)
nonsmooth. A valid certificate must retain every tied feature branch or use a proved
nonsmooth Fritz–John or Clarke condition.
The \(L^1\) formulation alone supplies continuity, not differentiability or
stationarity.

<a id="source-1-certified-finite-objects"></a>

#### Certified finite objects

<a id="source-1-exact-dual-lower-object"></a>

##### Exact dual lower object

A finite dual record consists of exact placements \(p_i\in P_L\) and exact weights
\(a_i\geq0\). Its value is \(D=\sum_i a_i\). It is a certified lower bound only when an
exact arrangement certificate proves

\[
\sum_i a_i\mathbf 1_{S_{p_i}}(x)\leq1
\]

on every full-dimensional cell of the square-edge arrangement.
The ignored set must be identified as the finite union of arrangement edges and vertices
and proved Lebesgue null.
Exact containment of each placement is also part of the certificate.
Under those conditions, \(D\leq\nu_{\mathrm{ae}}(L)\leq\tau_{\mathrm{ac}}(L)\).

A nested sequence of such finite families gives monotone nondecreasing lower values only
when the old feasible record embeds unchanged in the new family.
Floating overlap tests, point samples, and a pointwise closed-depth refusal have no
substitute semantics.

<a id="source-1-globally-covered-primal-upper-object"></a>

##### Globally covered primal upper object

A finite primal record specifies a nonnegative integrable density, its exact or
outward-rounded mass \(U\), and a finite exhaustive cover of \(P_L\). Every interior
pose box and every lower-dimensional wall stratum must carry a rigorous lower enclosure
for \(F_\rho\) whose endpoint is at least one.
The enclosure record must state its interval or Lipschitz direction and the hypotheses
used to cross density-cell feature changes.
If one box or stratum is open, \(U\) is not an upper bound.

A density satisfying only sampled placement constraints is a proposer.
The exact infimum obtained by dropping continuum constraints while leaving the density
class unchanged is at most \(\tau_{\mathrm{ac}}(L)\). A practical finite model usually
also restricts the density class, so its sampled optimum has no direction relative to
\(\tau_{\mathrm{ac}}(L)\) without another argument.
In either case, the returned sampled density is not primal-feasible and its mass is
never a certified upper endpoint.
A nested family of globally certified density classes can give monotone nonincreasing
upper values; changing bases, meshes, or unverified coverage guards carries no
monotonicity claim.

<a id="source-1-bc-243-pilot-contract"></a>

#### BC-243 pilot contract

BC-243 remains blocked in this commissioning block because the tree has neither a new
exact a.e.-depth arrangement verifier nor a continuum primal-coverage guard.
The smallest later pilot must use the exact Trump side and perform these independent
checks:

1. Seed the dual with the exact eleven-atom Trump packing and recover \(D=11\). Accept
   edge and corner touching as the refusal control against pointwise closed-depth
   semantics. Perturb a wall-touching placement atom across containment and require
   rejection; perturb an interior placement atom to create positive-area overlap and
   require rejection; reject an overweight full-dimensional arrangement cell; and verify
   every exact containment row.
2. Fit or propose a finite density without assigning upper-bound semantics.
   Include a negative control that passes the sampled constraints but fails a known
   unsampled placement.
   Reject both wall-supported and interior atomic primal mass as outside the absolutely
   continuous measure class unless a separate boundary theorem has first opened the
   singular variant.
3. Attempt a continuum cover over all interior pose boxes and wall strata.
   Report a certified \(U\) only if every pose box or stratum has a certified coverage
   lower endpoint of at least one; otherwise report the one-sided bound \([D,\infty)\)
   when \(D\) itself is valid.
4. Report \([D,U]\) only when both certificates are independently valid.
   Preserve exact values and outward-rounded displays separately.

The exact decision rules are:

- any sound \(D>11\) kills the mass-eleven equality route immediately;
- a weak-duality failure, boundary-semantics failure, or control that fails to reject
  its mutation gives disposition `unsound`;
- a sound one-sided result, or a sound upper endpoint with \(U-11>1/4\) at the
  predeclared priced resolution, gives `sound but quantitatively weak`;
- only a sound interval with the Trump lower control \(D=11\), a genuine continuum upper
  endpoint \(U\leq45/4\), and all controls passing is `close enough to request
  BC-244`.

The final label opens nothing by itself; BC-243 needs a coordinator gate after this
contract is reviewed and committed.

<a id="source-1-draft-satisfied-and-open-obligations"></a>

#### Draft-satisfied and open obligations

Supplied in this author draft:

- compactness of the placement space;
- continuity of coverage for absolutely continuous \(L^1\) densities;
- the Lebesgue-a.e. dual convention and weak-duality proof;
- the validity of an interior-disjoint exact packing as an atomic dual;
- conditional equality consequences without a classification claim;
- the boundary correction required by a singular-measure variant;
- the directions of exact finite dual and continuum-certified primal approximations;
- the wall normal-cone requirement and BC-243 accept or kill semantics.

Open:

- strong duality and primal or dual attainment;
- any admissible singular or wall-supported primal theorem;
- construction of the a.e.-depth verifier and continuum coverage guard;
- every numerical BC-243 pilot value;
- existence of a mass-eleven density and the BC-244 equality classification;
- any global conclusion about eleven squares in the Trump container.

<a id="source-2"></a>

## Source 2: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-113-h-099-trump-support-screen.md`

Snapshot `4d305597a505`, source lines 71-end.

<a id="source-2-exp-113--a-fixed-support-ceiling-screen"></a>

### exp-113 — A Fixed-Support Ceiling Screen

The screen returned an exact finite-row optimum of $56/5=11.2$, independently replayed
once. H-099 remains unresolved.
The known feasible mass-eleven average and this finite-row upper certificate place the
fixed-support supremum in $[11,56/5]$; they do not exhibit an a.e.-feasible weighting of
mass $56/5$.

The prospective protocol was committed as `b3046532`, with record-view corrections at
`cc18f64c`; all 31 record checks passed before target access.
The producer ran once from clean `e70458a9`, returned exit code 0, and used two solves
with 6 and 8 pivots.
Twenty distinct necessary rows survived the fixed sequence.
The separate checker also returned exit code 0. The
[independent review (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/independent-review.md)
records its scope and shared foundations.

The producer process took 19.69 seconds wall and 17.36 seconds CPU; the worker reported
19.561851 seconds wall and 17.245133 seconds CPU. The separate replay took 9.10 seconds
wall and 9.06 seconds CPU. Their summed process wall time is 28.79 seconds and CPU time
is 26.42 seconds; operator attention and review prose time are not measured or included
in those totals. The output replay finished within its lease; final review formatting
ended at 21:01:02, twelve seconds after the review deadline.
No target or replay allowance was extended.

<a id="source-2-retained-prospective-protocol"></a>

#### Retained Prospective Protocol

The prospective protocol selected one invocation of the independently reviewed
[BC-254 instrument (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-target-readiness-independent-review.md).
It authorized neither a geometric-support search nor a complete arrangement build.
Experiment 112 remains reserved for the separate H-092 transport; this experiment does
not replace that work.

The instrument and H-099 readiness are retained at `e70458a9`. The target ran in an
immutable checkout of that revision after the protocol was committed.
The command used the existing frozen project interpreter with `PYTHONPATH=src`, avoiding
an editable-package reinstall from the isolated checkout.
The known-packing source control yields 88 labelled images, 60 distinct placements,
eight orbits, and exact uniform mass 11. No optimized target was used to select the
support, rows, arithmetic, cap, or criterion.

<a id="source-2-frozen-decision-and-retention"></a>

#### Frozen Decision and Retention

The screen starts at zero in the exact LP with the negative identity active basis.
It uses the fixed initial row sequence, checks the first certificate before any
conditional extension, and permits no replacement grid, basis, solver, or placement.
The file checker independently reconstructs support preimages, determinant incidences,
positive neighborhoods, and the rational upper inequality; it does not run an optimizer.
Shared sequence generation is not independent execution-history attestation.

- If the separate replay verifies an upper bound of eleven, reject H-099 on exactly this
  support. The known feasible average rules out an upper bound below eleven; such an
  output is a failed control, not a stronger result.
- If the finite-row optimum exceeds eleven, leave H-099 unresolved.
  Finite rows do not establish almost-everywhere depth, so there is no dual
  mass-above-eleven claim.
- A capped, invalid, unreplayable, or incomplete run leaves H-099 unresolved and retains
  the actual refusal and unchecked remainder.
  Do not label it a mathematical negative.

Retain stdout as `packet.json` and stderr as `run.log` in the declared result directory,
then retain separate file-checker output as `replay.json` and its costs as `replay.log`.
Record the actual exit status and process wall/CPU in this experiment, including startup
outside the internal worker clock.
A failed producer may leave empty stdout; that is not a certificate and must not be sent
to mathematical acceptance.
No new checksum manifest is needed for these same-tree artifacts.

The independent review and coordinator disposition are retained in the same PR #101.
Nothing here changes the global unit-square packing bound or the source certificate.

<a id="source-3"></a>

## Source 3: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-115-h-105-fixed-candidate-pair-obstruction.md`

Snapshot `4d305597a505`, source lines 70-end.

<a id="source-3-exp-115--a-pair-test-of-the-fixed-candidate"></a>

### exp-115 — A Pair Test of the Fixed Candidate

H-105 is rejected: all 134 eligible pairs have exact separating axes, and the sole
independent file replay verified every one.
There is no pair witness, omitted pair or new LP row.
H-099 and the candidate’s full almost-everywhere feasibility remain unresolved; the
$[11,56/5]$ fixed-support supremum bracket is unchanged.

The prospective protocol was committed at `a40b40d3` after all 31 record checks passed
in 17.05 seconds. The producer then ran once from clean `cf299e6c`, returned exit 0, and
used 1.05 seconds wall and 1.03 seconds CPU. Its worker reported 0.899715459 seconds
wall and 0.893114 seconds CPU. The independently dispatched reader ran once from the
same clean source at 22:08:08–22:08:09 UTC, returned exit 0, and used 0.75 seconds wall
and 0.73 seconds CPU; its worker reported 0.603746042 seconds wall and 0.600491 seconds
CPU. Summed process costs are **1.80 seconds wall and 1.76 seconds CPU**, not agent
attention. Neither invocation was repeated or exceeded its separate cap.

The
[independent review (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/exp-115-h-105-fixed-candidate-pair-obstruction/independent-review.md)
records the complete pair ordering, exact input binding and independent certificate
reasoning, including its shared arithmetic/source-validation limits.
The next assessment prices complete positive-area-face verification of these unchanged
weights. Another incomplete pair-style screen is not a substitute for that obligation.

<a id="source-3-retained-prospective-protocol"></a>

#### Retained Prospective Protocol

This prospectively frozen experiment tests
[H-105](15-registered-mathematical-questions.md#source-14), not H-099. The
coordinator accepted the independent source/toy review at `cf299e6c`, which freezes both
the producer and checker.
No target construction or target binding roundtrip ran during instrument development or
review.

The parent is
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json`
at the same `cf299e6c` revision; its accepted outcome was first retained at `a105f729`.
The source is `packing/cases/trump11/packing.py`, named `trump11-v1`. Both target entry
points bind its exact algebraic side, canonical orbit ordering, 60 placement keys, eight
unchanged rational weights and the $56/5$ parent label.
The parent LP proof, row generation and pivot history are not replayed.
Git provenance and the accepted parent review supply that prerequisite.

The sole producer runs from a clean immutable `cf299e6c` checkout after this protocol is
committed and its record checks pass.
Retain stdout as `packet.json` and stderr plus the process timer as `run.log` in the
declared result directory.
After successful complete output, the independent reviewer runs once from that same
frozen source revision:

```bash
PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_full_size_density_pair_separator PAIR_PACKET --parent PARENT_PACKET --timeout-seconds 30
```

`PAIR_PACKET` is the retained producer file and `PARENT_PACKET` the frozen parent path.
Retain reader stdout as `replay.json`, stderr and process costs as `replay.log`, and the
independent scope review beside them.
Both CLIs bound worker startup and computation; their internal alarms also guard direct
worker invocation. The 30-second limits are caps, not target-runtime measurements.

Accept H-105 only for an independently checked strict positive-area overweight witness,
including the canonical separated prefix.
The executable’s `candidate-refuted` decision therefore **accepts the obstruction
hypothesis**. Reject H-105 only if all 134 eligible pairs have independently checked
separating axes. Timeout, incomplete output, failed source binding or failed replay
leaves it unresolved, with the actual guard or process failure retained instead of an
invented negative. A failed producer receives refusal review only, not another target
invocation.

A witness refutes only exp-113’s fixed weight assignment.
It does not refute H-099, change the $[11,56/5]$ supremum bracket or yield a packing
bound. No pair obstruction would still leave higher-order overlap unchecked.
The next possible branch after a witness is a separately priced full-support
off-boundary cut and bounded same-support ceiling update; after no pair obstruction, it
is complete positive-area-face verification of the unchanged weights.
Neither branch is funded here.

<a id="source-4"></a>

## Source 4: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-post-screen-next-discriminator.md`

Snapshot `4d305597a505`, source lines 206-end.

<a id="source-4-next-step-complete-face-verification-2026-09-06"></a>

#### Next Step: Complete Face Verification, 2026-09-06

This dated section supersedes the earlier pair-build recommendation for future
allocation; it does not rewrite that prospective design.
The coordinator reports that exp-115 completed all 134 eligible pairs with separately
checked separating axes and no witness.
H-105 is rejected only at its exact pair-obstruction scope.
H-099 and the unchanged exp-113 candidate’s a.e. feasibility remain unresolved.

This is source-only assessment `think-pg9k`, opened at `2026-09-06T22:09:48Z`; the
coordinator shortened its finalization boundary to `2026-09-06T22:19:32Z`. No new target
construction, binding, line or face enumeration, row, LP, test, or timing run occurred.
The recommendation is a complete face verifier, with independently reconstructed
coverage, not a higher-order overlap filter.

<a id="source-4-domain-and-boundary-semantics"></a>

##### Domain and Boundary Semantics

Freeze the same exact side, 60 distinct placements, source/orbit ordering, and eight
weights as exp-113. Keep all geometry and arithmetic in its certified real number field.
Validate containment, unit geometry, nonnegative rational weights, and source identity
before calculating depth.

For this fixed candidate only, omit zero-weight squares from the arrangement but retain
them in source metadata.
Its 36 positive placements contribute at most 144 supporting lines; adding the four
container walls gives at most 148 before exact deduplication.
These are combinatorial bounds from retained weights, not measured target line counts.

The finite union of these lines has Lebesgue area zero.
On each component of its complement inside the open container, every positive square’s
membership is constant, so weighted depth is constant.
Closed-square and interior-square indicators agree off their boundaries.
The required maximum is over these positive-area faces, not over closed arrangement
vertices. Excess confined to an edge or vertex is not an a.e. violation.
No global configuration-space capture is involved.

<a id="source-4-producer-probe-every-open-boundary-segment"></a>

##### Producer: Probe Every Open Boundary Segment

Use the following complete finite procedure, without floating screens:

1. Form every positive square’s infinite supporting lines and the four walls.
   For exact identity, divide each nonzero line triple by its first nonzero normal
   coefficient. Retain its incident square/edge labels; coincident lines are one
   geometric line, not extra weighted placements.
2. Clip each line to the closed container using exact line/wall intersections.
   Retain point contacts as a classified boundary case, but generate probes only from
   positive-length clipped segments.
   Split those segments at every intersection with a distinct nonparallel supporting
   line inside the segment.
   Include both container endpoints, deduplicate concurrent intersections exactly, and
   sort along an injective coordinate using algebraic order, not coefficient-tuple
   order.
3. For each pair of successive distinct cut points, take its midpoint $m$. It is on
   exactly its own geometric line: an equality with another line is a failed
   completeness guard. Choose a nonzero normal $n$ to its own line.
   For every other affine line form $g(x,y)=ax+by-c$, put $D_g(n)=an_x+bn_y$. Choose a
   positive rational displacement $\delta$ satisfying $|\delta D_g(n)|<|g(m)|/2$
   whenever $D_g(n)\ne0$. Exact sign and rational enclosure provide such a value; forms
   constant along the displacement need no bound.
4. Check $m+\delta n$ and $m-\delta n$. Keep each strictly interior container point; a
   wall segment has only one inward probe.
   Verify that retained probes lie on no positive supporting line.
   At each, compute depth by exact oriented edge tests and rational weight summation.
   Retain a positive rational neighborhood margin when depth exceeds one; otherwise
   continue through every segment and side.

Completeness follows from the bounded line arrangement: every positive-area face has a
nondegenerate open boundary segment in its closure.
Splitting at all intersections visits such a segment, and the bounded normal
displacement reaches its adjacent face without crossing any other line.
Thus every face is represented.
Repeated probes of the same face are harmless and need no face-identity machinery.
Container corners, coincident edges, parallel lines, and concurrent crossings do not
justify skipping their adjacent positive-area regions.

<a id="source-4-independent-replay-a-different-complete-enumeration"></a>

##### Independent Replay: A Different Complete Enumeration

A positive packet must not be accepted by checking only its supplied probes or counts.
Recommend an independently written vertical-slab sweep for the reader, reconstructing
the source through the existing direct D4 maps and rebuilding its own supporting lines.
It must not call the producer’s clipping, cut-list, or probe generator.

Collect $0$, the container side, all vertical-line coordinates, and the x-coordinates of
every nonparallel supporting-line intersection within the horizontal container range.
Including intersections whose y-coordinate is outside the container merely
overpartitions; it avoids an unnecessary event-filtering premise.
Include the horizontal walls in that construction.
Sort and deduplicate exactly.

For each open interval between successive x-events, choose its midpoint.
Intersect each positive square’s interior with that vertical line, obtaining an empty
set or one open y-interval.
Clip to the container, sort all interval endpoints, and sweep their rational weights,
grouping equal endpoints before evaluating each nonempty open y-band.
Endpoints themselves are not scored.
Independent determinant checks at band interior points supply negative witnesses when
needed.

All active endpoint formulas and their ordering are fixed between x-events: changes
require a vertical supporting line or an intersection already in the event set.
Consequently every positive-area face appears in at least one inspected slab/band.
An exceptional x-line has area zero and cannot be the sole location of an a.e.
violation. This supplies a second completeness argument, not just a second call to the
producer’s enumeration.

Both routes still share the exact field kernel and retained original source.
Original packing validation also uses its accepted geometric validator.
These shared foundations must remain explicit.
Complete independent regeneration can validate a compact result receipt; counts alone
are not a standalone portable proof.
If only a negative witness is returned, its exact positive-area box can be checked
directly without finishing either exhaustive route.

<a id="source-4-reuse-and-control-matrix"></a>

##### Reuse and Control Matrix

Reuse the reviewed source binding, exact square validation, canonical rational parser,
bounded file reader, and process/refusal interfaces from the support and pair tools.
Reuse `NumberField.sign` and `enclose` for exact signs and rational margins.
The
[Stromquist clipping implementation](12-restricted-orientations.md#source-1)
is a reference for equality handling, not a reason to import a case module into the
reusable library or alter its frozen source control.

Two existing routines are not drop-in complete a.e. checkers:

- `fractional.ceiling.maximum_depth` solves a closed-pointwise problem in a rational
  placement model. Its vertex maximum must not be relabelled as an a.e. maximum.
- `full_size_density.support_ceiling.necessary_row` checks all support boundaries,
  including zero-weight ones.
  Positive-only face probes can legitimately hit those omitted lines.
  Keep that accepted row guard unchanged; use a separate fixed-weight depth helper.
  A returned face point is not automatically a full-support LP row.

| Control | Required behavior |
| --- | --- |
| One square and a disjoint unit-weight packing | Exact a.e. maximum one, including boundary-touching placements |
| Edge/corner contacts whose closed depth exceeds one | Accept a.e. feasibility; do not score the contact itself |
| Overlapping pairs, equality at depth one, and the existing common-interior $2/5$ triple | Distinguish strict excess, equality, and a genuine violation invisible to pair filtering |
| Coincident supporting lines, parallel families, concurrent crossings, wall-coincident edges, and repeated event coordinates | Preserve every adjacent open region without zero-division or duplicated geometric weights |
| A rational sliver and non-target degree-eight rotated squares | Preserve narrow positive-area regions with exact order and signs |
| A zero-weight boundary passing through a probe | Same candidate depth and verdict after adding or removing that zero-weight placement |
| Original exact Trump packing and its D4 uniform average, when separately commissioned as source controls | Known a.e. depth at most one; do not presume an unmeasured exact maximum for the uniform average |
| Missing event, omitted segment side or slab, reordered/equal endpoint events, altered source/weight, invalid radius, and malformed packet | Refuse a false complete receipt or independently detect its omitted excess |

Tests must include handcrafted expected answers, a producer-independent negative
witness, and cases where only a small interior face violates depth.
Agreement between two programs without these known answers does not establish
completeness.

<a id="source-4-cost-first-slice-and-disposition"></a>

##### Cost, First Slice, and Disposition

Let $P$ be the number of positive placements and $M$ the distinct line count including
walls. The facet route has $O(M^2)$ cut segments/probes and a straightforward
$O(M^2(M+P))$ bound on exact field operations for clearance and membership checks.
The slab reader has $O(M^2)$ x-slabs; direct square-interval construction and endpoint
sweeps cost $O(M^2P\log P)$ exact operations.
These are operation-count estimates, not bit-complexity or wall-time bounds.
Algebraic division, coefficient growth, near-coincident events, and root-interval
refinement can dominate.

Implementation effort and target producer/replay costs remain unknown.
Exp-115’s reported 1.05-second producer and 0.75-second reader do not price an
arrangement. Do not inherit its 30-second caps or promise this verifier will fit them.
Set new finite process, event-count, memory, and serialized-output limits after control
costs are measured; hitting a limit remains unresolved, never complete feasibility.

The smallest useful funding request is **one 30-active-minute author slice followed by a
separately commissioned 15-minute independent review**, both control-only.
Build the complete facet procedure for small exact unit-square families, its strict
depth witness, and the degeneracy controls above.
Retain actual wall/CPU, operation counts, first obstruction, and remaining
implementation work.
Do not add target bindings or run the target during that slice.
The reviewer audits the completeness argument and controls; it does not accept global
readiness without the independent complete reader.
Price that reader and bounded packet integration from the first slice’s evidence rather
than assigning a fabricated total completion estimate here.

After both routes pass review and a new prospective target is frozen, complete checked
depth at most one for these weights would supply mass $56/5>11$ under H-099’s existing
BC-243 soundness requirements.
An independently checked excess would invalidate only these weights, leaving H-099
unresolved and permitting a separately priced exact-cut proposal.
A partial positive sweep, timeout, or disagreement proves neither outcome.
No reweighting, support extension, new row, LP, or new research allocation is authorized
by this assessment.

## Exact Candidate and Necessary-Row Data

Source: `packing/campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json` at `4d305597a505ebfbe85f1851fa7148374661e622`; selected mathematical fields, JSON whitespace normalized.

Use the zero-based original square labels and exact corner formulas in file 09. In order, take the D4 orbits of original squares **0, 2, 4, 7, 10, 8, 6, 9**. The original-square classes are `{0,1,3}`, `{2}`, `{4,5}`, `{7}`, `{10}`, `{8}`, `{6}`, `{9}`. Generate D4 by `R(x,y)=(U-y,x)` and `F(x,y)=(U-x,y)`, deduplicating geometric squares exactly. There are 60 distinct placements, with orbit sizes `[4,8,8,8,8,8,8,8]`. Give EACH DISTINCT MEMBER of an orbit its corresponding `primal` weight below. This specifies the entire mass-56/5 candidate without a separate geometry file. Its 36 positive-weight placements still require complete a.e.-depth verification.

Each row-point coordinate is a list of coefficients of `1,u,...,u^7`, lowest degree first, in the degree-eight field defined in file 09. `radius` is a retained positive neighborhood witness: an open L-infinity box around the point, contained in the container with constant incidence. The finite LP is `max sizes·a` subject to `A a <= 1, a >= 0`. The exact multipliers satisfy `A^T lambda >= sizes`, `lambda >= 0`, and `sum lambda = 56/5`. A row coefficient counts distinct placements of that orbit containing the point in their interiors. This upper certificate is necessary-row evidence, not an enumeration of all faces. When implementing geometry, use cyclic corners from file 09; the original JSON's canonical corner sets were sorted sets, not polygon perimeter order.

```json
{
  "bound": "56/5",
  "primal": [
    "1",
    "0",
    "2/5",
    "1/10",
    "0",
    "1/10",
    "3/10",
    "0"
  ],
  "multipliers": [
    "4/5",
    "0",
    "0",
    "16/5",
    "0",
    "0",
    "0",
    "16/5",
    "0",
    "0",
    "8/5",
    "0",
    "0",
    "0",
    "0",
    "0",
    "0",
    "0",
    "4/5",
    "8/5"
  ],
  "rows": [
    {
      "coefficients": [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "point": [
        [
          "1/2",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0"
        ],
        [
          "1/2",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0"
        ]
      ],
      "radius": "25211763301/1000000000000"
    },
    {
      "coefficients": [
        0,
        1,
        1,
        0,
        1,
        0,
        0,
        0
      ],
      "point": [
        [
          "1/2",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0"
        ],
        [
          "1/2",
          "17/8",
          "-1/4",
          "15/8",
          "1/2",
          "3/8",
          "-5/4",
          "5/8"
        ]
      ],
      "radius": "1274653406441693/409600000000000000"
    },
    {
      "coefficients": [
        0,
        1,
        1,
        2,
        1,
        0,
        0,
        0
      ],
      "point": [
        [
          "1/2",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0"
        ],
        [
          "1",
          "37/8",
          "-5",
          "35/8",
          "8",
          "15/8",
          "-15/2",
          "25/8"
        ]
      ],
      "radius": "316210392251653/51200000000000000"
    },
    {
      "coefficients": [
        0,
        0,
        2,
        2,
        2,
        0,
        0,
        0
      ],
      "point": [
        [
          "43/80",
          "73/80",
          "-87/80",
          "-53/80",
          "9/16",
          "23/80",
          "-5/16",
          "1/16"
        ],
        [
          "79/80",
          "289/80",
          "-471/80",
          "431/80",
          "141/16",
          "119/80",
          "-125/16",
          "53/16"
        ]
      ],
      "radius": "206209366090863/32000000000000000"
    },
    {
      "coefficients": [
        0,
        1,
        1,
        2,
        1,
        0,
        1,
        1
      ],
      "point": [
        [
          "43/80",
          "73/80",
          "-87/80",
          "-53/80",
          "9/16",
          "23/80",
          "-5/16",
          "1/16"
        ],
        [
          "119/80",
          "199/80",
          "-311/80",
          "561/80",
          "125/16",
          "-111/80",
          "-85/16",
          "43/16"
        ]
      ],
      "radius": "28031283962529/64000000000000000"
    },
    {
      "coefficients": [
        0,
        0,
        0,
        0,
        0,
        8,
        0,
        0
      ],
      "point": [
        [
          "317/400",
          "987/400",
          "-53/400",
          "-87/400",
          "63/80",
          "757/400",
          "-35/16",
          "59/80"
        ],
        [
          "381/400",
          "1541/400",
          "-1629/400",
          "59/400",
          "399/80",
          "851/400",
          "-75/16",
          "137/80"
        ]
      ],
      "radius": "975994965520111/128000000000000000"
    },
    {
      "coefficients": [
        0,
        0,
        0,
        0,
        1,
        0,
        2,
        2
      ],
      "point": [
        [
          "327/400",
          "947/400",
          "-843/400",
          "53/400",
          "173/80",
          "717/400",
          "-45/16",
          "79/80"
        ],
        [
          "361/400",
          "771/400",
          "-1549/400",
          "729/400",
          "419/80",
          "581/400",
          "-75/16",
          "147/80"
        ]
      ],
      "radius": "12865921026463/1280000000000000"
    },
    {
      "coefficients": [
        1,
        2,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "point": [
        [
          "5/8",
          "37/32",
          "-5/4",
          "35/32",
          "2",
          "15/32",
          "-15/8",
          "25/32"
        ],
        [
          "5/8",
          "37/32",
          "-5/4",
          "35/32",
          "2",
          "15/32",
          "-15/8",
          "25/32"
        ]
      ],
      "radius": "25716081650503/4096000000000000"
    },
    {
      "coefficients": [
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "point": [
        [
          "5/16",
          "37/64",
          "-5/8",
          "35/64",
          "1",
          "15/64",
          "-15/16",
          "25/64"
        ],
        [
          "5/8",
          "37/32",
          "-5/4",
          "35/32",
          "2",
          "15/32",
          "-15/8",
          "25/32"
        ]
      ],
      "radius": "1502242063393307/409600000000000000"
    },
    {
      "coefficients": [
        0,
        1,
        1,
        1,
        1,
        0,
        0,
        0
      ],
      "point": [
        [
          "5/16",
          "37/64",
          "-5/8",
          "35/64",
          "1",
          "15/64",
          "-15/16",
          "25/64"
        ],
        [
          "15/16",
          "111/64",
          "-15/8",
          "105/64",
          "3",
          "45/64",
          "-45/16",
          "75/64"
        ]
      ],
      "radius": "67713558844419/40960000000000000"
    },
    {
      "coefficients": [
        0,
        1,
        1,
        0,
        1,
        0,
        2,
        2
      ],
      "point": [
        [
          "5/8",
          "37/32",
          "-5/4",
          "35/32",
          "2",
          "15/32",
          "-15/8",
          "25/32"
        ],
        [
          "15/16",
          "111/64",
          "-15/8",
          "105/64",
          "3",
          "45/64",
          "-45/16",
          "75/64"
        ]
      ],
      "radius": "12912061158213/10240000000000000"
    },
    {
      "coefficients": [
        0,
        0,
        0,
        0,
        0,
        0,
        2,
        2
      ],
      "point": [
        [
          "15/16",
          "111/64",
          "-15/8",
          "105/64",
          "3",
          "45/64",
          "-45/16",
          "75/64"
        ],
        [
          "15/16",
          "111/64",
          "-15/8",
          "105/64",
          "3",
          "45/64",
          "-45/16",
          "75/64"
        ]
      ],
      "radius": "108133203255789/204800000000000000"
    },
    {
      "coefficients": [
        0,
        0,
        0,
        0,
        0,
        4,
        2,
        0
      ],
      "point": [
        [
          "15/16",
          "111/64",
          "-15/8",
          "105/64",
          "3",
          "45/64",
          "-45/16",
          "75/64"
        ],
        [
          "5/4",
          "37/16",
          "-5/2",
          "35/16",
          "4",
          "15/16",
          "-15/4",
          "25/16"
        ]
      ],
      "radius": "1779219549610889/819200000000000000"
    },
    {
      "coefficients": [
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0
      ],
      "point": [
        [
          "5/32",
          "37/128",
          "-5/16",
          "35/128",
          "1/2",
          "15/128",
          "-15/32",
          "25/128"
        ],
        [
          "25/32",
          "185/128",
          "-25/16",
          "175/128",
          "5/2",
          "75/128",
          "-75/32",
          "125/128"
        ]
      ],
      "radius": "7936782566605966741/1677721600000000000000"
    },
    {
      "coefficients": [
        0,
        0,
        2,
        2,
        0,
        0,
        0,
        0
      ],
      "point": [
        [
          "5/32",
          "37/128",
          "-5/16",
          "35/128",
          "1/2",
          "15/128",
          "-15/32",
          "25/128"
        ],
        [
          "5/4",
          "37/16",
          "-5/2",
          "35/16",
          "4",
          "15/16",
          "-15/4",
          "25/16"
        ]
      ],
      "radius": "262201203456328651/1374389534720000000000"
    },
    {
      "coefficients": [
        1,
        1,
        0,
        0,
        1,
        0,
        0,
        0
      ],
      "point": [
        [
          "15/32",
          "111/128",
          "-15/16",
          "105/128",
          "3/2",
          "45/128",
          "-45/32",
          "75/128"
        ],
        [
          "5/8",
          "37/32",
          "-5/4",
          "35/32",
          "2",
          "15/32",
          "-15/8",
          "25/32"
        ]
      ],
      "radius": "397856988022234167161/879609302220800000000000"
    },
    {
      "coefficients": [
        0,
        1,
        1,
        2,
        2,
        0,
        0,
        0
      ],
      "point": [
        [
          "15/32",
          "111/128",
          "-15/16",
          "105/128",
          "3/2",
          "45/128",
          "-45/32",
          "75/128"
        ],
        [
          "35/32",
          "259/128",
          "-35/16",
          "245/128",
          "7/2",
          "105/128",
          "-105/32",
          "175/128"
        ]
      ],
      "radius": "94866248304348462992617/17592186044416000000000000"
    },
    {
      "coefficients": [
        0,
        0,
        0,
        0,
        1,
        1,
        2,
        2
      ],
      "point": [
        [
          "25/32",
          "185/128",
          "-25/16",
          "175/128",
          "5/2",
          "75/128",
          "-75/32",
          "125/128"
        ],
        [
          "35/32",
          "259/128",
          "-35/16",
          "245/128",
          "7/2",
          "105/128",
          "-105/32",
          "175/128"
        ]
      ],
      "radius": "808214241830964814509/351843720888320000000000"
    },
    {
      "coefficients": [
        0,
        0,
        0,
        2,
        0,
        2,
        2,
        2
      ],
      "point": [
        [
          "25/32",
          "185/128",
          "-25/16",
          "175/128",
          "5/2",
          "75/128",
          "-75/32",
          "125/128"
        ],
        [
          "5/4",
          "37/16",
          "-5/2",
          "35/16",
          "4",
          "15/16",
          "-15/4",
          "25/16"
        ]
      ],
      "radius": "60813430386139076457/87960930222080000000000"
    },
    {
      "coefficients": [
        0,
        0,
        0,
        0,
        0,
        4,
        2,
        2
      ],
      "point": [
        [
          "15/16",
          "111/64",
          "-15/8",
          "105/64",
          "3",
          "45/64",
          "-45/16",
          "75/64"
        ],
        [
          "35/32",
          "259/128",
          "-35/16",
          "245/128",
          "7/2",
          "105/128",
          "-105/32",
          "175/128"
        ]
      ],
      "radius": "1391566139930973605147/175921860444160000000000"
    }
  ],
  "orbit_original_square_representatives": [
    0,
    2,
    4,
    7,
    10,
    8,
    6,
    9
  ],
  "orbit_sizes": [
    4,
    8,
    8,
    8,
    8,
    8,
    8,
    8
  ],
  "uniform_feasible_control_weights": [
    "3/4",
    "1/8",
    "1/4",
    "1/8",
    "1/8",
    "1/8",
    "1/8",
    "1/8"
  ]
}
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
