# The Two Research Programs

Selected scientific sections of agendas 025 and 026. Scheduling, ownership metadata and repeated launch logs are omitted; the registered claims appear in file 15. The latest results in files 11 and 12 supersede these programs' earlier launch recommendations.

<a id="source-1"></a>

## Source 1: `packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md`

Snapshot `4d305597a505`, source lines 467-639.

<a id="source-1-agenda-025--adaptive-fractional-frontier-above-381"></a>

### Agenda 025 — Adaptive Fractional Frontier Above 3.81

The [current allocation](03-agenda-024.md#source-1-current-allocation) owns
prospective allocations for L1 (current certificates) and L2 (richer witnesses).
The scalar probe runs independently of adaptive-verifier implementation.
Scientific criteria below remain applicable.
The
[continuation addendum’s scalar command (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/docs/project/handoff-2026-09-06-post-381-t2-t10-continuation.md#scalar-6116-launch)
supersedes the historical scalar invocation below; historical schedules do not authorize
an additional BC-232 final leg.

This child agenda is managed independently under the `think-wess` research epic and
integrated only through [`agenda-024`](03-agenda-024.md#source-1).
Its first block runs BC-230, BC-232, and BC-233 in parallel after BC-219. BC-231 follows
the theorem contract; no adaptive rung is claimable before both are complete.
All minute and hour allocations in this agenda use agenda-024’s active-time accounting
unless they are explicitly CPU budgets, command time limits, or reported wall/CPU costs.
An operational interruption pauses this lane’s research allocation and cannot advance it
through a shared gate.

The workflow entry point is **BC-230 + BC-232 + BC-233 after the coordinator opens
BC-219**. Work from `packing/` with the project interpreter:

```bash
uv run --frozen --all-extras --group dev COMMAND
```

Never use the `python3` on `PATH` for project code.
Set `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, and
`VECLIB_MAXIMUM_THREADS=1` on each optimization runner.
The pinned macOS NumPy build uses Accelerate, so `VECLIB_MAXIMUM_THREADS` is the
operative BLAS limit on this host; the other variables keep the command single-threaded
if the wheel or host changes.
Do not run the four-worker exact sweep while the three first-block runners are live.

The manager owns fractional implementation and the manager artifacts named below.
The coordinator creates or allocates hypotheses and experiments and owns ledgers, agenda
maps, frontier records, schemas, validation configuration, pushes, and retention
decisions. After allocation, the manager may append commands and outcomes to an
experiment in its reserved range without changing its identity or accept rule.
In an isolated worktree it may make local transport commits containing only owned paths;
in a shared checkout it returns an uncommitted patch.
The coordinator integrates either form.
A need to touch another shared surface is a gate request.
Workers may edit only the BC and paths assigned by the manager; they do not operate
`tbd`, commit, push, change an accept rule, or promote a claim.

The input packet and fixed routing rules are in
[`X-016`](05-current-assessment-and-review.md#source-3).
The Massaccesi margin is a seed prior, the 3.82 state is resumed rather than
reconstructed, and the two-threshold class language is a retired control rather than a
fallback.

<a id="source-1-frozen-local-packet"></a>

#### Frozen local packet

No first-block worker needs the network.
Paths in this section are repository-relative; commands later in the document are run
from `packing/` and therefore omit the leading `packing/`.

<a id="source-1-strategy-and-retained-measurements"></a>

##### Strategy and retained measurements

- `packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md`
  fixes ownership, gates, and routing rules.
- `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-060-h-064-n11-fractional-packing-floor.md`
  records the 3.82 run, its costs, and its reopen condition.
- `packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json`
  is the warm state. Its SHA-256 is
  `8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6`. It holds side
  `191/50`, square side `9977/10000`, 12,761 sites, 9,868 rows, nine iterations, and
  best iteration 8.
- `packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-family-191-50.json`
  and
  `packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-summary-191-50.json`
  are the retained exact packing-family and run summary controls.
- `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-063-h-065-n11-near-tight-cell-census.md`
  is diagnostic context only.
- `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md`
  is the retired class-language control.
  Its `11.606445` result and `3.876681` ceiling forbid reopening that formulation as a
  fallback.

The retained 3.82 reading is `9.907905594982566 <= nu* <= tau* <= 11.055616942909815`,
of width `1.147711347927249`. The continuation earns another four-CPU-hour block only
when `new_width <= 0.75 * old_width`, equivalently at width at most
`0.86078351094543675` for this checkpoint.
An upper endpoint counts only from an iteration whose row loop reports
`rows_converged: true`; keep its computational status distinct from the exact
`verify_ceiling` lower endpoint.

<a id="source-1-exact-implementation-seams"></a>

##### Exact implementation seams

- `packing/src/sqpack/fractional/certificate.py` is the current scalar-`B` certificate
  contract and exact event-sweep verifier.
- `packing/src/sqpack/fractional/sweep.py` implements the scalar-`B` event cells.
- `packing/src/sqpack/fractional/interval.py` is the second, interval decision route.
- `packing/src/sqpack/fractional/classcert.py` already supplies exact rational
  angle-cell boundaries (`cell_boundary_tangent`), folded-cell conventions, and the
  squared rational `cos + sin` predicate.
  Its two-threshold optimization result is retired; its cell geometry is reusable.
- `packing/src/sqpack/fractional/cutting.py` and
  `packing/devtools/run_fractional_cutting.py` own the 3.82 cutting state and exact
  packing-family floor.
- `packing/devtools/freeze_cutting_primal.py` is the covering bridge for that state: row
  generation to convergence on the state’s sites, one covering solve, the column
  generator’s rationalisation, and a `least_cell_mass`-null candidate in the retained
  shape. `run_fractional_cutting --seed-certificate` starts a fresh side from the grid
  plus a retained certificate’s atoms, since a warm start only moves upward.
- `packing/src/sqpack/fractional/colgen.py` and
  `packing/devtools/run_fractional_colgen.py` own row/column generation and frozen
  covering candidates.
- `packing/devtools/colgen_checkpoint.py` owns a different, NPZ checkpoint format.
  It cannot read `bc-200-state-191-50.json` and is not BC-232’s resume command.
- `packing/devtools/decide_certificate.py` is the freeze-then-decide retention gate.
  It currently accepts only the unconditional scalar-`B` variant; BC-231 must extend or
  replace that decision boundary before an adaptive object can be retainable.
- `packing/devtools/declare_least_cell_mass.py` fills a scalar candidate’s null
  `least_cell_mass` by a one-worker exact sweep without regenerating the search.
  BC-233 uses this bridge before the two-route decision gate.
- `packing/cases/n11_fractional_certificate/minimal_verify.py` is the current
  standard-library scalar-`B` implementation.
  With `--unpinned`, it is the source-distinct route for a new scalar candidate from
  BC-232 or BC-233. BC-231 must add an adaptive counterpart,
  `adaptive_minimal_verify.py`, that reads the frozen generalized object without
  importing `sqpack`; BC-238 uses it as the source-distinct implementation route.

The current `Certificate`, exact sweep, and interval route all carry one `square_side`.
Adaptive `B_k` is therefore a theorem, serialized-contract, loader, event-sweep,
interval, and mutation-test change.
It is not a generator option.
BC-230 must specify a complete folded cover of `[0, pi/4]`, exact endpoint and seam
rules, the per-cell maximum mismatch, and a rational strict-containment decision.
It must state whether the v1 predicate remains the conservative `B_k(1 + D_k) < 1` or
uses the stronger exactly squared `B_k(cos(delta_k) + sin(delta_k)) < 1`, and prove that
the chosen legacy specialization reproduces every current scalar-`B` verdict.

<a id="source-1-positive-source-and-refusal-controls"></a>

##### Positive, source, and refusal controls

- `packing/cases/n11_fractional_certificate/certificate.json` and
  `packing/cases/n11_fractional_certificate/t-018-proof-card.md` are the live n=11
  positive and its proof/cost record.
- `packing/cases/n12_fractional_certificate/certificate.json` is the live n=12 positive.
- `packing/cases/n11_fractional_certificate/thirdparty/control-n17-massaccesi.json`,
  `build_n17_control.py`, `verify.py`, and `check.py` form the source-distinct n=17
  control.
- `packing/resources/web/n17-lower-bounds-2026/README.md`,
  `massaccesi-linear-programming.html`, `massaccesi-lower-bound-4_5058.html`, and
  `massaccesi-verify-n17-lower-bound-4_5058.py` are the local primary-source packet.
- `packing/cases/n11_fractional_certificate/thirdparty/falsify.py` supplies the signed
  weight and retained scalar refusal controls.
  BC-231 adds adaptive missing-cell, unsafe-`B_k`, seam, and orbit-deletion mutations in
  first-party tests.

Baseline commands from `packing/` are:

```bash
uv run --frozen --all-extras --group dev python -m cases.n11_fractional_certificate
uv run --frozen --all-extras --group dev python -m cases.n12_fractional_certificate
.venv/bin/python3 cases/n11_fractional_certificate/thirdparty/check.py
.venv/bin/python3 cases/n11_fractional_certificate/thirdparty/falsify.py --quick
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  cases/n11_fractional_certificate/certificate.json
```

The proof card measures the optimized standalone n=11 replay at 47.5--67 seconds on one
idle core. The third-party check documents about 30 seconds on an idle core and up to a
minute when contended; the archived raw source replay completed in under five seconds.
The full n=11 falsification table costs about four minutes.
These are retained measurements, not guarantees for an adaptive object.
The n12 independent verifier’s own command-line tail reads a mode name and the
reviewer’s absolute checkout path, so the evidence register’s replay runs through
`cases/n12_fractional_certificate/replay_independent.py`, which loads the retained file
unchanged and takes a certificate path (`think-d7yx`).

<a id="source-2"></a>

## Source 2: `packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md`

Snapshot `4d305597a505`, source lines 913-976.

<a id="source-2-scalar-probe-at-6116-a-pre-registered-first-block-option"></a>

##### Scalar probe at 61/16: a pre-registered first-block option

Nothing between 3.81 and 3.82 has been attempted with the existing single-`B` theorem.
The covering-values register holds `n = 11` reports at 3.82 and 3.85 only, and T-018’s
own ladder went 3.78, 19/5, 381/100, then straight to 3.82. The retained certificate
carries `434547/40000 = 10.863675`, `0.136` below eleven; the vertex-seeded restricted
optimum at 3.82 is `11.055617`, `0.056` above it.
A straight line through those two points crosses eleven near 3.817, so `61/16 = 3.8125`
and `763/200 = 3.815` are plausibly inside the current instrument’s reach before any
adaptive core exists, and BC-234 only reaches 61/16 after BC-230 and BC-231, at least
390 active minutes of theorem and verifier work whose necessity for this rung has not
been measured.

The probe is one background single-core process on instruments that already exist: the
cutting driver from the grid plus the 3.81 atoms carried by `--seed-certificate` (a warm
start cannot move downward), with BC-232’s net, shrink, row budget and thread pins, and
the covering bridge on its state if a row-converged objective falls below eleven.
It is not one of the six cells X-016 opens at `T+0`. The coordinator decides at dispatch
whether to allocate it (`think-8rqf`), gives it a hypothesis and an experiment record in
the reserved ranges, and starts it only once BC-233’s screen has released a core, so the
first-block process count never exceeds three.

The following command is historical.
Use the continuation addendum’s linked scalar command, which adds
`--stop-on-covering-below-n` while preserving the frozen150-minute budget and other
parameters.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 61/16 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 150 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --seed-certificate cases/n11_fractional_certificate/certificate.json --seed-map scale \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-family.json
```

Read it exactly as BC-232: the lower endpoint is the exact `best_scaled_total`, the
computational upper endpoint is the smallest row-converged `rows_objective`. A
`verify_ceiling` family of total at least eleven closes the scalar formulation at 61/16
and prices BC-230 precisely, since an adaptive core must then earn more than the whole
scalar margin at this side.
A wall reached by the 150-minute clock is time-limited and reopens only at the hour-four
gate with its state hashed.
A row-converged objective below eleven runs the bridge on the fresh state:

```bash
uv run --frozen --all-extras --group dev python -m devtools.freeze_cutting_primal \
  --n 11 --state STATE.json --angle-limit 207107/500000 --steps 180 \
  --rows-rounds 2 --rows-per-direction 3 --scale 4000000 \
  --freeze CANDIDATE.json --json CANDIDATE.receipt.json
```

The bridge refuses an unconverged row loop, a rejected program, a rationalised total at
or above eleven, and an existing output path.
Its candidate then takes the scalar route already declared for BC-232 and BC-233: hash,
`declare_least_cell_mass`, hash again, `decide_certificate`, and
`minimal_verify.py --unpinned`. A decided mass below eleven routes to BC-238 and
outranks everything else in the block.

<a id="source-3"></a>

## Source 3: `packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md`

Snapshot `4d305597a505`, source lines 565-614.

<a id="source-3-agenda-026--density-typed-stationarity-and-trump-capture"></a>

### Agenda 026 — Density, Typed Stationarity, and Trump Capture

The [current allocation](03-agenda-024.md#source-1-current-allocation) owns
prospective allocations for L3 (density), L4 (structural arguments), and L5
(falsification). Density feasibility and restricted structural theory may proceed in
parallel; uniform D4 controls alone do not justify a full BC-243 build or BC-244. The
proof contracts and frozen scientific criteria below remain applicable.

This child agenda is managed independently under the `think-j7rm` research epic and
integrated only through [`agenda-024`](03-agenda-024.md#source-1).
Its first block runs BC-240, BC-242, and BC-245 in parallel after BC-219. BC-241 reviews
the local theorem while BC-243 and the typed-backbone controls wait for their
mathematical contracts.
All minute and hour allocations in this agenda use agenda-024’s active-time accounting
unless they are explicitly CPU budgets, command time limits, or reported wall/CPU costs.
An operational interruption pauses this lane’s research allocation and cannot advance it
through a shared gate.

The manager owns closure implementation and named manager artifacts only.
Shared hypotheses, ledgers, agenda maps, frontier records, schemas, validation
configuration, commits, pushes, and retention decisions belong to the coordinator.
A need to touch one of those surfaces is a gate request.

The input packet and fixed routing rules are in
[`X-016`](05-current-assessment-and-review.md#source-3).
The Trump radius is an existing local endpoint to package and review.
The density route must earn weak-dual semantics before numerical optimization, and the
stationary route must price a complete typed language before an n=11 atlas is launched.

For post-T+2 work through T+10, use the
[`continuation addendum` (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/docs/project/handoff-2026-09-06-post-381-t2-t10-continuation.md).
It binds BC-241’s source-distinct controls and narrows BC-243 to an unimplemented,
dual-only 180-active-minute pilot.
Continuum primal coverage remains entirely in BC-244. The completed T+0-to-T+2 packets
stay frozen.

The frozen BC-242 author packet’s combined BC-243 prerequisite—an exact a.e.-depth
verifier and a continuum primal-coverage guard—is an unreconciled commissioning
scheduling statement.
For post-T+2 scheduling, this reviewed agenda and the continuation addendum supersede
only that combined dependency: BC-243 requires the exact a.e.-depth verifier, while
BC-244 owns the continuum primal-coverage guard.
The continuation contract also narrows the author packet’s generic interior-overlap
control. BC-243 rejects the perturbed unit-weight Trump fixture only when its exact
full-dimensional a.e. depth exceeds one; geometric overlap alone is not a rejection
condition for a weighted dual.
The frozen weak-duality proof and every limitation on strong duality, attainment,
singular primals, numerical endpoints, and primal semantics remain unchanged as frozen
evidence.

<a id="source-4"></a>

## Source 4: `packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md`

Snapshot `4d305597a505`, source lines 850-1009.

<a id="source-4-density-proof-contract"></a>

#### Density Proof Contract

Let `C_L = [0,L]^2`. Let `P_L` be the compact placement space of centres and angles
modulo each square’s quarter-turn symmetry for which the corresponding closed unit
square `S_p` lies in `C_L`.

The initial primal is restricted to absolutely continuous measures.
For `rho in L1_+(C_L)`, define

`F_rho(p) = integral over S_p of rho(x) dx`

and

`tau_ac(L) = inf integral over C_L of rho(x) dx`, subject to `F_rho(p) >= 1` for every
`p in P_L`.

For a finite nonnegative Borel measure `w` on `P_L`, define its overlap depth

`d_w(x) = integral over P_L of 1[x in S_p] dw(p)`.

The weak dual requires `d_w(x) <= 1` for Lebesgue-almost-every `x`. Tonelli’s theorem
then gives

`w(P_L) <= integral rho(x) d_w(x) dx <= integral rho(x) dx`.

This is the minimum proof obligation for interpreting a dual value as a lower bound.
No strong-duality or attainment theorem is needed for the kill test.
If either is later used for equality or complementary slackness, prove its topology and
semicontinuity hypotheses separately.

The a.e. convention is essential.
An exact packing of eleven full-size squares with unit atomic weights has depth at most
one away from shared edges and corners, hence is a valid dual of mass eleven.
The existing `packing/src/sqpack/fractional/ceiling.py` uses pointwise depth of closed
sets and deliberately rejects touching squares.
It is therefore the wrong verifier for this dual and must not be weakened or relabelled.
A new a.e.-depth verifier must inspect full-dimensional cells of the exact boundary
arrangement and ignore only a proved measure-zero union of boundaries.

BC-243 must run two distinct overlap controls.
The unit-weight Trump mutation perturbs one interior atom so that exact full-dimensional
a.e. depth exceeds one and must be rejected.
A weighted-overlap fixture whose overlapping placements carry positive rational weights
must be accepted when its summed exact depth is at most one on every full-dimensional
cell. Use two distinct, contained, positive-area-overlapping placements of weight `1/2`
each and no other atoms: their depth is one on the overlap and `1/2` elsewhere.
This distinction tests weighted depth rather than geometric intersection.

The following directions are mandatory:

- A finite exact placement family with a certified a.e. depth bound is dual-feasible and
  supplies a lower bound on `tau_ac(L)`.
- A density that covers only sampled placements is a proposer, not primal-feasible and
  not an upper bound.
- A primal upper bound requires a global continuum proof that `F_rho(p) >= 1` on all of
  `P_L`, including interior pose boxes and wall strata.
- A branch-and-bound cover must prove its interval or Lipschitz enclosure direction and
  refuse a result if any pose box or boundary stratum remains open.
- If singular mass is admitted, prove `mu(boundary S_p) = 0` for every admissible
  placement or state and verify the replacement boundary terms.
  Do not mix singular mass with the a.e. proof above.

BC-243 reports only the one-sided interval `[dual lower bound, infinity)`. Any exact
dual value strictly greater than eleven kills a mass-eleven density immediately, without
a primal instrument.
If the dual pilot does not kill equality, BC-244 separately decides whether to build a
continuum primal-coverage guard.
A mass-eleven primal and the Trump dual would force equality of coverage on the eleven
dual placements and saturation of depth where the primal density is positive, but those
equalities would not classify all compatible eleven-tuples.
BC-244 must still characterize the complete equality set.
If BC-244 opens, its packet must explicitly analyze strong duality and primal and dual
optimizer attainment, or retain each as an unresolved obligation.
Numerical primal-dual agreement cannot replace those proofs.

Before any future exact integration theorem or global optimality claim, every admissible
non-Trump survivor must be represented, priced, and discharged.
The n=11 Lean spike is user-requested assurance, not a Condition 5 validity
prerequisite, and a proof-producing Condition 5 receipt remains optional hardening
unless a later gate promotes it.

For inverse design, a Trump placement on the boundary of `P_L` obeys constrained
stationarity: the derivative of `F_rho` lies in the normal cone generated by active wall
containment constraints with nonnegative multipliers.
It need not have zero unconstrained gradient.
Piecewise densities require feature-cell branches or a stated nonsmooth Fritz–John or
Clarke condition, with wall ties retained.

<a id="source-4-typed-stationarity-proof-contract"></a>

#### Typed-Stationarity Proof Contract

The global program begins with existence.
Bound `L` by the exact candidate side, put angles on the compact quarter-turn quotient,
and use the closed containment and nonoverlap conditions to prove that a better packing,
if one exists, has a minimum.

Represent the feasible set as a finite union of smooth support branches.
For every square pair, a branch records the owner square, one of its two local axes, and
the separation order.
Wall constraints record the responsible corner and wall.
When several axes, features, or corners tie, retain every applicable branch.
Corner-corner contact is a disjunction of support descriptions, not a graph edge with
one distance equation.

Use variables `z = (L, c_1, theta_1, ..., c_n, theta_n)` and include derivatives with
respect to `L` in right and top wall rows.
With branch inequalities `g_j(z) >= 0`, a branch minimum must have nonnegative `alpha`
and `lambda_j`, not all zero, satisfying

`alpha grad L - sum_j lambda_j grad g_j = 0`,

`lambda_j g_j(z) = 0`.

Normalize projectively by `alpha + sum_j lambda_j = 1`. The case `alpha > 0` is the
normal/KKT multiplier branch.
The case `alpha = 0` is the abnormal Fritz–John branch.
A geometry may admit both types; the abnormal case may be omitted only after a
constraint qualification is proved for every affected branch.

Keep three objects distinct:

1. the complete branch constraint list;
2. the geometrically active rows; and
3. the positive multiplier support.

An active row may have zero multiplier.
A rattler may be absent from the positive support.
Neither fact permits deleting its feasibility variables or noncontact inequalities.
Backbone connectedness is not a necessary condition unless separately proved.

The finite object is a typed combinatorial language plus continuous semialgebraic
systems, not a finite list of planar graphs.
It must retain wall identities, contact features, owner axes, separation orders, angle
charts, active rows, zero and positive multiplier states, and rattler attachments.
A single tangent-half-angle chart misses its pole, so use an explicit finite chart
atlas. Canonicalization must transform all of these labels jointly under `D4 x S_n`;
canonical records require exact witness replay.

At exact fixed angles, centre and side constraints may use
`packing/src/sqpack/exact_lp.py::fixed_cell_lp` and exact Farkas certificates.
Interval angle boxes need rigorous coefficient enclosures; a floating realization LP
cannot be extrapolated into a proof.
Every closed branch needs either a certificate that the whole branch is infeasible or an
exhaustive isolation or cover of all its stationary components together with a verified
objective bound on each component.
An exact feasible stationary witness is a candidate within a branch; it cannot close the
branch by itself because another root or component, including a rattler family, may
improve the side. Branch-closing evidence may therefore combine exact LP or Farkas
infeasibility certificates, verified interval exclusions, and exact algebraic or
root-isolation certificates, but it must account for the full branch.

A cap or timeout creates an open-branch receipt, never a completeness claim.

BC-246 passes only if the language reproduces Trump’s 14 pair contacts, 20 wall-corner
incidences, two angle classes, 512 raw feature selections, 128 derivative-distinct
matrices, and the exact exp-013 tangent verdict before it invokes BC-240. BC-247 passes
only if every n=3 quotient stratum and the n=4 grid orbit is recovered, the exact Göbel
n=5 witness is representable, mutation controls fail for the intended reason, and the
n=11 price is derived from named measured combinatorial factors.
The n=5 control alone cannot establish completeness.

<a id="source-5"></a>

## Source 5: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-230-adaptive-core-contract.md`

Snapshot `4d305597a505`, source lines 1-245.

<a id="source-5-bc-230-adaptive-core-theorem-and-certificate-contract"></a>

### BC-230 Adaptive-Core Theorem and Certificate Contract

Status: author checkpoint for source-distinct review under agenda-024. This packet
specifies the theorem and serialized decision boundary; it does not claim that an
adaptive verifier or candidate exists.

Launch base: `c55726e1e885227f63110131c0a914665175ff89`\
Frozen preregistration: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`\
Cell: BC-230 (`think-c678`)

<a id="source-5-the-exact-object"></a>

#### The Exact Object

Fix $n\in\mathbb Z_{\ge 1}$ and $L\in\mathbb Q_{>0}$, and let `C_L = [0,L]^2`. The
resource is a finite nonnegative atomic measure

\[
\mu=\sum_j w_j\delta_{p_j},\qquad p_j\in C_L,\quad w_j\in\mathbb Q_{\ge 0},
\]

on distinct rational sites.
Its nonzero atomic support and weights are invariant under all eight symmetries of
`C_L`. A site on a symmetry axis or at the center occurs once in the serialized atom
list; orbit multiplicity is never added to its mass.
An absent site implicitly has weight zero, so measure-level invariance alone does not
require images of a listed zero-weight point.
The adaptive schema nevertheless treats the explicitly listed site domain as part of its
presentation: a listed zero-weight site must have all of its distinct `D4` images listed
with weight zero, or the entire zero orbit must be omitted.
This is a closed-schema presentation rule, not a premise needed by the counting theorem.
Thus `mu(C_L)` is the sum of the weights at distinct serialized sites, with no orbit
multiplicity.

The direction net is described by rational half-angle tangents

\[
0=t_0<t_1<\cdots<t_K<1,\qquad \alpha_k=2\arctan t_k.
\]

The final two directions straddle the folded endpoint in the following exact sense:

\[
t_{K-1}^2+2t_{K-1}-1<0\le t_K^2+2t_K-1.
\]

For `1 <= k <= K`, define the seam tangent

\[
q_k=\tan\frac{\alpha_{k-1}+\alpha_k}{2}
    =\frac{t_{k-1}+t_k}{1-t_{k-1}t_k},
\]

and set `q_0 = 0`, `q_{K+1} = 1`. The contract requires

\[
0=q_0<q_1<\cdots<q_K<q_{K+1}=1.
\]

This is a complete rational check that the last Voronoi seam lies before the fold and
that the cells below cover exactly `[0,pi/4]`.

Let `beta_k = arctan(q_k)`. The geometric cell closure for direction `k` is

\[
\overline C_k=[\beta_k,\beta_{k+1}].
\]

The ownership cells are

\[
C_0=[\beta_0,\beta_1],\qquad
C_k=(\beta_k,\beta_{k+1}]\quad(1\le k\le K).
\]

Consequently, angle zero belongs to cell `0`, `pi/4` belongs to cell `K`, and each
interior seam belongs to the lower-index cell.
The closures overlap only to prove endpoint bounds; the ownership cells form a disjoint
partition. A verifier must derive these cells.
It may not accept sampled representatives or caller-supplied gaps.

The full-angle tangent of direction `k` is rational:

\[
a_k=\tan\alpha_k=\frac{2t_k}{1-t_k^2}.
\]

For angles with nonnegative finite tangents, define

\[
r(a,q)=\frac{|a-q|}{1+aq}.
\]

This is exactly the tangent of their absolute angular difference.
The maximum mismatch for the closed cell is therefore the rational number

\[
D_k=\max\{r(a_k,q_k),r(a_k,q_{k+1})\}.
\]

The equality follows because absolute angular difference reaches its maximum at an
endpoint of an interval and tangent is increasing on `[0,pi/2)`. In an interior cell,
the two values are the tangents of the adjacent half-gaps.
The formula also handles the axis and folded endpoints without an irrational
representation of `pi/4`.

Each cell carries a positive rational witness side `B_k`. BC-230 chooses the
`legacy-linear-v1` containment rule:

\[
B_k(1+D_k)<1\qquad\text{for every }k.
\]

Its cellwise safe-side supremum is `1/(1+D_k)`. The inequality is strict, so no largest
rational side is attained; a generator may choose its largest proposed rational strictly
below that supremum.
This is the precise meaning of a cell’s “largest safe” side in this contract.

This conservative rule preserves the current scalar decision exactly.
The stronger squared comparison

\[
B_k^2(1+D_k)^2<1+D_k^2
\]

is a sound future contract version, but it is not part of this one.
Indeed, an interior cell’s endpoint mismatch is half an adjacent direction gap, the
first cell has the same form, and the folded-endpoint bracket bounds the last cell’s
other endpoint mismatch.
Because every net direction lies strictly below `pi/2`, these checks give
`0 <= D_k < 1`; on that range `(1+D_k)/sqrt(1+D_k^2)` is increasing and the squared
comparison is the exact worst-endpoint test.
Mixing the two rules under one variant would change the legacy refusal boundary.

<a id="source-5-adaptive-core-lemma"></a>

#### Adaptive-Core Lemma

Let a unit square have orientation `theta`. Reduce it modulo `pi/2` to the unique
`bar_theta` in `[0,pi/2)`, and set

\[
\phi=\min\{\bar\theta,\pi/2-\bar\theta\}\in[0,\pi/4].
\]

This folded angle is unique even when more than one container symmetry realizes it at an
axis or diagonal. Any realizing symmetry gives the same theorem verdict by `D4`
invariance; an implementation uses one fixed `D4` order only to make witness receipts
deterministic. If `phi` belongs to ownership cell `C_k`, the unit square contains, about
the same center and strictly inside its interior, a closed square of side `B_k` and
orientation `alpha_k` in the folded coordinates.

To prove this, put `delta = |phi-alpha_k|`. Since `phi` lies in the closed cell used to
define `D_k`, `tan(delta) <= D_k`. In coordinates aligned with the unit square, the
half-extent of the proposed core along either axis is

\[
\frac{B_k}{2}(\cos\delta+\sin\delta).
\]

For `0 <= delta < pi/2`,

\[
\cos\delta+\sin\delta
=\frac{1+\tan\delta}{\sqrt{1+\tan^2\delta}}
\le 1+\tan\delta
\le 1+D_k.
\]

The strict contract inequality makes this half-extent strictly less than `1/2`. Hence
the closed core lies in the open interior of the unit square.
The conclusion holds at cell seams because the mismatch bound was taken over each closed
cell, even though the ownership rule selects only one of the two neighboring directions.

<a id="source-5-adaptive-fractional-certificate-theorem"></a>

#### Adaptive Fractional-Certificate Theorem

The following conditions imply that `n` unit squares with pairwise disjoint interiors do
not fit in `C_L`:

1. The atoms are distinct, rational, nonnegative, inside `C_L`, and the resulting
   measure is invariant under `D4`.
2. Their total mass is strictly below `n`.
3. The rational net and derived ownership cells satisfy the complete folded-cover
   conditions above.
4. Every cell satisfies `B_k(1+D_k) < 1` under `legacy-linear-v1`.
5. For every `k` and every center `c` for which the closed square `Q(c,alpha_k,B_k)`
   lies in `C_L`, `mu(Q(c,alpha_k,B_k)) >= 1`.

Suppose a packing existed.
Fold each packed square independently by a symmetry of the container, select the unique
owning cell, and apply the adaptive-core lemma.
Undoing the symmetry gives a closed core strictly inside the original square.
The cores are pairwise disjoint because the packed-square interiors are pairwise
disjoint.

`D4` invariance gives each unfolded core the same mass as its folded representative.
Condition 5 gives every core mass at least one.
Nonnegativity and disjointness then give

\[
n\le\sum_{i=1}^n\mu(Q_i)=\mu\!\left(\bigsqcup_i Q_i\right)
\le\mu(C_L)<n,
\]

a contradiction. Under the repository’s bound convention, the certificate establishes
`s(n) >= L`.

Condition 5 is universal over centers.
For atomic measures, the existing exact event sweep can decide it separately at each
pair `(alpha_k,B_k)`: coverage is constant on open center cells, and a boundary can only
add atoms because every weight is nonnegative.
A finite sample of centers is not a decision route.

<a id="source-5-exact-scalar-specialization"></a>

#### Exact Scalar Specialization

Take a current scalar certificate and set every `B_k` to its single `B`. The production
nets have the final seam before `pi/4`, so the largest endpoint mismatch among all
closed cells is exactly

\[
\max_k D_k
=\max_{0\le k<K}\frac{t_{k+1}-t_k}{1+t_kt_{k+1}}
=D,
\]

the current verifier’s largest half-gap tangent.
At the folded endpoint, `beta_K < pi/4 <= alpha_K` by the seam and bracket checks, so
`alpha_K - pi/4 < alpha_K - beta_K`. Its mismatch is therefore no larger than the final
adjacent half-gap.

Since `B > 0`, all per-cell inequalities `B(1+D_k)<1` hold if and only if `B(1+D)<1`.
Condition 5 invokes the same direction list, the same `B`, the same center domains, and
the same atoms as the scalar sweep.
Conditions 1 and 2 are unchanged, and the exact folded-cover check implies the current
net-reaches-`pi/4` condition.

The legacy loader specialization must construct this adaptive object in memory without
rewriting the retained JSON. On the current n=11 and n=12 retained positives, it must
return the same retention verdict, exact total mass, exact least covered mass, and first
worst direction as the scalar verifier.
On the n=17 source control, the underlying scalar and adaptive exact verifiers must both
recompute total `203/12` and least mass `1`, while the retention command must preserve
its current refusal because the source object does not declare `least_cell_mass`. The
archived verifier and source-distinct checker must continue to accept those original
bytes. Every current scalar refusal remains a refusal.
The unchanged scalar route continues to refuse a short legacy net under its current
net-reaches-`pi/4` condition; the adaptive route refuses the corresponding new object
under the complete folded-cover condition.

<a id="source-6"></a>

## Source 6: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-231-next-phases-slice-02.md`

Snapshot `4d305597a505`, source lines 1-end.

<a id="source-6-bc-231-second-implementation-slice"></a>

### BC-231 Second Implementation Slice

BC-231 (`think-7mk4`), W7, 2026-09-06. The coordinator authorized
`19:39:02–20:09:02 UTC`; source and tests stabilized at `19:55 UTC`, following slice-01
commit `184fa6c9`. The [BC-230 contract](04-child-agendas.md#source-5) and
[control matrix (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-230-control-matrix.md) remain unchanged.

The project now loads the bounded adaptive JSON format and exercises the pure F4/F5
cover refusals. This is control-only implementation evidence: H-095 remains
instrument-blocked, and there is no adaptive retention command or target result.

<a id="source-6-implemented-boundary"></a>

#### Implemented Boundary

The new [loader (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/src/sqpack/fractional/adaptive_io.py) enforces the
closed top-level and angle-cell key sets, literal variant/rule/ownership fields, exact
integer types, canonical rational strings, duplicate-key and nonfinite-token refusals,
and the frozen byte, atom, angle-cell, and rational-text limits.
Structural and bounded-format checks finish before angle geometry.
Declared totals and claims must match the parsed instance.
Existing in-memory guards enforce containment, nonnegative distinct atoms, listed-domain
D4 completeness, total mass below `n`, and the axis-core method ceiling.
The committed geometry adapters and scalar loader are unchanged.

`load_bytes` returns an `AdaptiveInput`, not an acceptance result.
Its minimum declaration remains unverified, including null or a subunit rational;
Condition 5 and the later declared-minimum comparison have not run.
`load(path)` reads at most the byte limit plus one and does not provide retention
rereads or artifact binding.

Atom coordinates are container `(x,y)` coordinates.
Angle-cell boundaries are tangents on the folded orientation arc, not center-space
event-cell boundaries.
Existing sweep witness centers remain rotated `(u,v)` coordinates; they must be
converted before a later receipt compares them with container-coordinate witnesses.
This slice creates no decision receipt.

<a id="source-6-controls-and-checks"></a>

#### Controls and Checks

The serialized P4 fixture is the unchanged five-atom control from
[slice 01 (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-231-next-phases-slice-01.md): `L = 6/5`, total mass `7/5`, and core sides
`7/10`, `3/4`, `4/5`. Both project routes still give per-angle-cell minima `6/5`,
`13/10`, `7/5`. The small equal-side scalar fixture also passes after a test-only JSON
serialization. Retained n=11, n=12, and n=17 objects supply geometry and atom-data round
trips only; no full coverage or source replay ran, and their bytes are unchanged.

The [102 new tests (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/tests/test_fractional_adaptive_io.py) include every
required key, the frozen input limits and inclusive byte/rational boundaries, malformed
structures, geometry and measure mutations, and these branch-reachability controls:

- F4 calls the pure validator on `[0,1/3]`, `[1/3,2/3]`, `[2/3,1]`, then reaches named
  gap and overlap refusals by changing the second lower endpoint to `2/5` and `1/4`.
  Patched parser and declaration checks would fail the tests if invoked.
- F5 directly reaches the axis and fold endpoint refusals.
  Its serialized n=12 mutation recomputes every dependent field and reaches the named
  final-seam refusal at `q_K = 164144306/142927847 > 1`. A separate stale mismatch
  mutation takes the earlier declaration-equality branch.
  This ordering requires a loader-side algebraic comparison before complete-cover
  validation; it is not another independent route.

From `packing/`, using Python 3.14 and the frozen environment:

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev python -m pytest -q \
  tests/test_fractional_adaptive_io.py tests/test_fractional_adaptive.py \
  tests/test_fractional_certificate.py tests/test_fractional_interval.py \
  tests/test_fractional_sweep_integer.py tests/test_decide_certificate.py \
  -m 'not exhaustive_exact and not exhaustive_interval and not slow'
```

Result: `254 passed, 22 deselected in 17.44s`. Scoped Ruff and BasedPyright checks on
the two new Python files report zero findings.
The TDD start failed on the missing module; development also caught an invalid
exception-clause spelling and a test that incorrectly treated the required per-cell
`square_side` as unknown.
Both were corrected.
Test duration is not a route-cost measurement.
The coordinator owns snapshot validation and independent review.

<a id="source-6-coordinator-review"></a>

##### Coordinator review

The coordinator independently read the loader, its refusal tests and the BC-230
serialized contract, then replayed the loader and first-slice adaptive tests under
Python 3.14. No finding was identified in this control-only boundary.
The review checked canonical rational spelling, noncoercive integer fields, bounded
reads, declaration order, F4/F5 branch reachability, and the explicit separation between
loading and a coverage or retention verdict.
This does not complete the missing standalone, source-replay, or triad obligations.

<a id="source-6-remaining-work-and-price"></a>

#### Remaining Work and Price

The following are planning estimates in active worker minutes, not measured run costs or
authorization for another slice.
They price the remaining BC-231 contract, not an H-095 target search.

| Remaining obligation | Active minutes |
| --- | --- |
| Independent standard-library checker, its own parser/geometry, and normal versus `-O` controls | 35–55 |
| Three-route orchestration, per-cell receipts, coordinate normalization, byte binding, disagreement and skipped-route refusals | 40–65 |
| Full scalar/source compatibility and legacy-refusal harnesses | 20–35, plus replay runtime |
| T10 independent full-grid fixture generation, frozen witness, and all three routes checking that same witness | 35–75, plus replay runtime |
| Remaining boundary, eight-sector folding, and orbit-stabilizer controls | 20–35 |
| Empty/singleton policy review and any explicitly selected follow-on | 10–20 |
| Independent review, fixes, and focused integration validation | 20–35 |

The working total is **180–320 active minutes plus unpriced full replays**. T10 and the
receipt integration are the largest uncertainties.
Equal verdicts or minima alone do not satisfy T10: its independently frozen angle cell,
direction, container-coordinate center, and mass must be checked by all three routes.
No such witness has been frozen.

The current adapters continue to refuse empty or singleton center domains.
The loader does not reinterpret that refusal as a coverage result, and the all-empty
`least_cell_mass` policy remains unresolved.
The next useful selected slice would commission the standalone route on P4 and the
frozen format mutations; the coordinator must choose it explicitly.
The previously mentioned 180 minutes is neither a completion promise nor automatic
authority to continue.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
