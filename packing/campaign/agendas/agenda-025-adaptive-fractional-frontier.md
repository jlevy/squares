---
title: "agenda-025 — adaptive fractional frontier above 3.81"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-025
  title: "Adaptive Fractional Frontier Above 3.81"
  updated: '2026-09-05'
  status: active
  objective: >-
    Give one managing agent a disjoint, exact program for the likeliest direct
    improvement to s(11) >= 3.81. Formalize direction-dependent witness sides B_k and
    their verifier, resume the retained 3.82 primal/dual state, and test Massaccesi's
    inset margin only as a seed before unrestricted column generation. A verified rung
    earns immediate exactification; a stalled adaptive core routes to a rational
    angle-cell kernel; segment measures remain tentative until that route is disposed
    and a verifier is priced. This manager owns BC-230 through BC-239, H-070 through
    H-079, and exp-070 through exp-089, but not shared campaign or frontier state.
  items:
  - id: BC-230
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: ready
    priority: 0
    question: >-
      What exact containment theorem and certificate contract allow every angle cell to
      use its own largest safe concentric witness side B_k without leaving an uncovered
      orientation or breaking D4 accounting?
    budget: >-
      210 active minutes: up to 120 minutes of manager authorship, 75 minutes of
      source-distinct review by the floating worker after BC-240 returns it, and 15
      minutes to reconcile the packet. State the closed angle cells, endpoint and seam
      ownership, rational tangent form, strict containment inequality for every member
      of a cell, D4 orbit convention, total mass semantics, and every verifier refusal.
      The contract must reduce exactly to the current single-B theorem. Kill any
      proposal that samples a cell, assumes its worst angle, or omits a symmetry image.
    entry: >-
      BC-219 has frozen the fractional packet and allocated H-070 through H-079 without
      creating a hypothesis prematurely.
    exit: >-
      A proof-ready lemma and soft contract specify every field and quantifier, reproduce
      the current theorem when all B_k agree, and give BC-231 executable positive and
      negative controls.
    bead: think-c678
    workflows: [research-loop]
    depends_on: [BC-219]
    parallel_group: agenda025-theorem
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      Whether direction-dependent cores are a sound strengthening of the exact object,
      rather than a generator heuristic that the verifier cannot decide.
  - id: BC-231
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 12, 17]
    state: blocked
    priority: 0
    question: >-
      Can an exact verifier decide the adaptive-core contract and refuse uncovered
      angles, unsafe cell bounds, missing D4 images, and known-feasible targets?
    budget: >-
      180 active minutes, manager with one implementation worker,
      pipeline-improvement then factual-review. Reuse the existing exact event-cell
      sweep only after BC-230 proves the reduction, extend the interval route, and build
      one standard-library standalone adaptive verifier that does not import sqpack.
      Retain the single-B n=11 and n=12 certificates as positives, Massaccesi n=17 as a
      source control, and the existing known-feasible and optimized-Python refusals.
      Add mutations for a missing angle cell, enlarged B_k, an orbit deletion, and a
      signed weight. Kill on any changed verdict for a retained object or disagreement
      among the three decision routes.
    entry: >-
      BC-230's theorem and field contract are committed and independently readable.
    exit: >-
      The project sweep, interval route, and source-distinct standalone verifier decide
      the generalized object; all retained positives are bit-identical through the
      single-B specialization; every mutation is refused for the named reason; decision
      cost is measured.
    bead: think-7mk4
    workflows: [pipeline-improvement, factual-review]
    depends_on: [BC-230]
    parallel_group: agenda025-theorem
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      A trustworthy decision boundary on which an adaptive 3.8125 run may rely.
  - id: BC-232
    purpose: research
    owner_focus: efficiency
    instances: [11]
    state: ready
    priority: 0
    question: >-
      Can the retained 3.82 primal/dual state be advanced to total covering mass below
      11 or exact packing value at least 11 without restarting the search?
    hypotheses: [H-064]
    budget: >-
      Four CPU-hours inside the first two blocks, manager with one runner,
      research-loop. Resume `bc-200-state-191-50.json` and its exact control hashes.
      Record the exact packing floor and latest row-converged covering objective after
      each cutting iteration. Continue this route only if the width falls by at least
      25 percent over the declared block. A row-converged covering objective below 11
      is a candidate that still needs a rationalizing freeze bridge; a
      `verify_ceiling` packing family of weight at least 11 closes this exact measure
      formulation at 3.82. An intermediate value is a checkpoint, not a verdict.
    entry: >-
      BC-219 has hash-checked the state and the resume command; no newer checkpoint
      supersedes it.
    exit: >-
      A frozen exact certificate, a verified ceiling, or a resumable state with old and
      new bracket widths, cost, and the 25-percent routing decision.
    bead: think-gmdy
    workflows: [research-loop, efficiency-loop]
    depends_on: [BC-219]
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json
    parallel_group: agenda025-bracket
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      Which side of eleven the current one-body formulation reaches at 3.82, or a
      measured reason to stop spending on this checkpoint.
  - id: BC-233
    purpose: research
    owner_focus: insight
    instances: [11, 17]
    state: ready
    priority: 1
    question: >-
      Does an inset-support sweep provide a better seed for n=11 only after its support
      is released into unrestricted column generation?
    budget: >-
      30 active portfolio minutes for the inset screen and at most 90 more active
      portfolio minutes for the unrestricted follow-on, manager with one runner for the
      screens and up to two single-threaded runners for the matched follow-on,
      research-loop. Record the manager's attentive work as agent_minutes and each
      process's actual CPU and command time separately. Reproduce Massaccesi's n=17
      margin semantics first. Sweep the three declared n=11 insets in this runbook at
      identical grid counts and one column round; feed only the best converged seed to
      the unchanged pricing oracle. Split the follow-on equally between that released
      seed and an unseeded control. Continue only if the released run improves the
      control on a verifier-decided mass or a like-for-like bracket. Failure of the
      restricted family refutes nothing.
    entry: >-
      BC-219 freezes the source post, verifier, margin definition, site budget, and
      unrestricted control.
    exit: >-
      The restricted and released trajectories, exact comparable metrics, cost, and a
      keep-or-retire decision that makes no causal claim about wall avoidance.
    bead: think-jbat
    workflows: [research-loop]
    depends_on: [BC-219]
    parallel_group: agenda025-seeding
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      Whether Massaccesi's margin is a useful proposal distribution for this instance,
      not whether inset supports contain the unrestricted optimum.
  - id: BC-234
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      After exact adaptive semantics and controls pass, can they certify 3.8125 and then
      3.815 without changing the target or rationalization rule mid-run?
    budget: >-
      One four-CPU-hour block after BC-231, research-loop. Register the first side and
      exact accept rule before synthesis. Attempt 61/16 = 3.8125 first; open 763/200 =
      3.815 only if the first certifies or removes at least 25 percent of the
      same-support excess over 11. Freeze any mass-below-11 bytes immediately and send
      them to the coordinator. Do not spend the cell proliferating net or margin
      variants after a candidate exists. A scalar attempt at 61/16 with the existing
      single-B instruments may run in block one as a background process without
      waiting for BC-230 and BC-231, under the pre-registered probe in this agenda's
      launch section; its wall or its rung prices the adaptive route before it opens.
    entry: >-
      BC-231 passes, BC-220 or a later coordinator gate creates the allocated
      hypothesis, and the target and scale are frozen.
    exit: >-
      An exact candidate above 3.81, or exact before/after excess and cost deciding
      whether BC-235 opens.
    bead: think-1sv0
    workflows: [research-loop]
    depends_on: [BC-231]
    parallel_group: agenda025-adaptive-run
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      A directly publishable rung or a quantitative verdict on adaptive witness cores.
  - id: BC-235
    purpose: research
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      If square cores stall, can each angle cell be assigned a rational inner kernel
      contained in every unit-square orientation in the cell with less lost area than
      its largest concentric square?
    budget: >-
      150 active minutes, theory and geometry workers, research-loop. Derive the exact
      intersection or a rational inner approximation with a proof of containment and
      quantified area loss. Do not call the intersection polygonal without proof;
      curved or algebraic boundaries require an explicit approximation direction.
      Continue only if the predicted gain clears the adaptive-core result by a declared
      margin.
    entry: >-
      BC-234 is disposed without a candidate and its routing rule opens the kernel
      fallback.
    exit: >-
      A finite rational kernel representation with an exact containment proof and
      enough predicted gain to justify BC-236, or a bounded negative with the obstruction.
    bead: think-ay89
    workflows: [research-loop]
    depends_on: [BC-234]
    parallel_group: agenda025-kernel
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      Whether a strictly richer one-body witness can be represented by a small exact
      verifier.
  - id: BC-236
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 12]
    state: blocked
    priority: 1
    question: >-
      Can the rational angle-cell kernel be swept and interval-checked exactly with the
      existing positive and negative controls and acceptable cost?
    budget: >-
      180 active minutes, manager plus implementation worker,
      pipeline-improvement then factual-review. Build the smallest verifier BC-235's
      representation requires. Accept only exact containment and complete reachable
      center-cell coverage. The n=11 and n=12 retained positives and a known-feasible
      negative must behave as declared. Kill if the decision cost exceeds four times
      the measured square-core control.
    entry: >-
      BC-235 supplies a frozen rational representation and containment proof.
    exit: >-
      Exact positive and negative receipts, a measured cost ratio, and a keep-or-retire
      decision under the four-times rule.
    bead: think-yaf9
    workflows: [pipeline-improvement, factual-review]
    depends_on: [BC-235]
    parallel_group: agenda025-kernel
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      Whether the kernel language is a certifiable instrument rather than a geometric
      sketch.
  - id: BC-237
    purpose: research
    owner_focus: efficiency
    instances: [11]
    state: blocked
    priority: 2
    question: >-
      After the kernel route is disposed, is a piecewise-algebraic segment-measure
      verifier small and cheap enough to build in a later block?
    budget: >-
      90 active minutes, theory-only research-loop. Specify segment-square intersection
      regimes, breakpoints, boundary conventions, exact coefficient domain, independent
      controls, and a branch-count estimate. No implementation opens in this agenda.
      Defer unless the complete verifier fits a measured future block and promises a
      resource language not dominated by kernels.
    entry: >-
      BC-236 has a terminal disposition and the coordinator opens this tentative cell.
    exit: >-
      A costed, falsifiable verifier design and reopen condition, or a recorded reason
      segments add complexity without enough expressive gain.
    bead: think-fw95
    workflows: [research-loop, efficiency-loop]
    depends_on: [BC-236]
    parallel_group: agenda025-kernel
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      A build/no-build decision for the next richer measure language.
  - id: BC-238
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      Does any fractional candidate from this agenda survive frozen-byte exactification,
      source-distinct replay, and falsifying mutations?
    budget: >-
      Up to 75 percent of the block following any candidate, manager plus independent
      reviewer, factual-review. Freeze bytes and SHA-256 before review. Select the
      decision routes by object: a scalar certificate from BC-232 or BC-233 uses
      `decide_certificate` and `minimal_verify.py --unpinned`; an adaptive certificate
      from BC-234 uses the extended project sweep, interval route, and BC-231's
      standalone verifier; and a kernel candidate from BC-236 cannot enter until
      BC-236 leaves both a project and source-distinct decision route. Include
      optimized-Python and malformed-object refusals and report all shared assumptions.
      A BC-232 packing family of weight at least 11 is a method-closure result, not a
      lower-bound candidate for these routes. The coordinator alone may retain or
      promote a result.
    entry: >-
      BC-232, BC-233, BC-234, or BC-236 emits a frozen lower-bound candidate with all
      routes required by its object type, and a coordinator gate diverts it here.
    exit: >-
      A complete candidate packet accepted by all three decision routes, or the smallest
      failing premise and a refusal with no frontier change.
    bead: think-hjoe
    workflows: [factual-review]
    depends_on: [BC-219]
    blocked_on: >-
      A frozen lower-bound candidate from BC-232, BC-233, BC-234, or BC-236, its
      object-specific project and source-distinct routes, and a coordinator gate that
      diverts it to independent exactification.
    parallel_group: agenda025-exactification
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      A result object the central retention gate can judge without trusting its generator.
  - id: BC-239
    purpose: measurement_validation
    owner_focus: process
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      Is every fractional cell classified, its checkpoint and cost preserved, and its
      one earned continuation or retirement condition explicit for portfolio closeout?
    budget: >-
      45 active minutes before BC-225, manager-owned W10 and documentation-pass. Use
      achieved, bounded-negative, time-limited, guard-refused, technical-failure,
      never-opened, or inconclusive; give each continuation a bead and reopen condition;
      validate manager-owned artifacts and submit the terminal packet without editing
      shared ledgers.
    entry: >-
      BC-224 has frozen new instrument work and the manager's final exact runs are done.
    exit: >-
      Agenda-025's outcomes and tbd subtree agree, documentation is checked, and one
      proposed next entry is sent to BC-225 without being executed.
    bead: think-mss2
    workflows: [documentation-pass, review-planning-oversight]
    depends_on: [BC-224]
    parallel_group: agenda025-closeout
    program: n11-adaptive-fractional-frontier
    next_evidence: >-
      The fractional program's honest yield, cost, negative results, and best continuation.
---
# Agenda 025 — Adaptive Fractional Frontier Above 3.81

This child agenda is managed independently under the `think-wess` research epic and
integrated only through [`agenda-024`](agenda-024-post-381-24h-portfolio.md).
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
[`X-016`](../explorations/X-016-after-381-two-managers-one-proof-boundary.md).
The Massaccesi margin is a seed prior, the 3.82 state is resumed rather than
reconstructed, and the two-threshold class language is a retired control rather than a
fallback.

## Frozen local packet

No first-block worker needs the network.
Paths in this section are repository-relative; commands later in the document are run
from `packing/` and therefore omit the leading `packing/`.

### Strategy and retained measurements

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

### Exact implementation seams

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

### Positive, source, and refusal controls

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

## Launch Audit Receipts and Open Instrument Gate

The 2026-09-05 readiness audit used the BC-219 base
`663ca37eb622508d9df00c594b8ef11d2c256f55`. The audit began with every named
implementation, control, and checkpoint path byte-identical to that `origin/main`. It
then repaired the strict-JSON defect in `packing/devtools/run_fractional_colgen.py` and
added its controls in `packing/tests/test_run_fractional_colgen.py`; the superseding
launch manifest in agenda-024 binds those new bytes.
None of these receipts reads or depends on PR #87. The future
`adaptive_minimal_verify.py` and the manager output root are absent as declared rather
than dangling inputs.

The cheapest checks produced these receipts from `packing/`:

- the retained state hash is
  `8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6`; the production
  cutting driver loaded side `191/50`, 12,761 sites, 1,657 orbits, and 9,868 rows
  against the declared 181-direction net, then stopped at iteration cap zero;
- the `--help` surfaces for `run_fractional_cutting`, `run_fractional_colgen`,
  `declare_least_cell_mass`, and `decide_certificate` accept every flag used below;
- the integrated contract-seam slice, including the declaration and strict-JSON
  controls, passed 88 tests with two exhaustive tests deselected;
- Massaccesi’s archived verifier returned `CERTIFICATE CONDITIONS VERIFIED` with 168
  atoms, mass `203/12`, and least score `1`; and the source-distinct `check.py` rebuilt
  the control bytes and accepted both its n=11 and n=17 controls;
- `minimal_verify.py --unpinned` accepted the live 1,121-atom scalar n=11 certificate
  with least covered mass `4001/4000` in 48.7 seconds, confirming the independent scalar
  entry point that BC-232 and BC-233 candidates use; and
- zero-budget colgen probes exercised both the unseeded screen and the
  `--seed-certificate ... --seed-map centre` path.
  They stopped before the first LP round, emitted no candidate, and the seeded probe
  loaded 1,121 distinct seed sites.

The zero-budget probes exposed a handoff defect: a deadline-stopped colgen summary
serialized bare `Infinity` and `NaN` tokens.
Those are not JSON numbers, and `jq` silently translated them to a maximum float and
`null` in the audit.
The follow-up tracked by `think-quwt` now writes `null` for the documented unavailable
solver fields and uses `allow_nan=False` to reject any unexpected non-finite value.
The focused driver suite passed ten tests, including the deadline CLI path and an
unexpected-NaN refusal.

A deadline-stopped BC-233 arm is now safe to preserve and hand off as strict JSON, but
it is still time-limited and ineligible for comparison or BC-233’s scientific exit.
Any future summary containing `Infinity` or `NaN` is a technical failure, not a result.

A reviewer’s timing run on 2026-09-05 (`think-kht8`) executed the BC-233 inset-`1/2`
screen template below unchanged, writing outside the reserved root on a four-core macOS
host: the row loop converged in 25 LP rounds at objective `78/7 = 11.142857`, the
restricted optimum exp-060’s iteration 0 reached on this grid, a 196-atom candidate of
rationalised mass `11142897/1000000` was emitted, and the process took 191.0 s of wall
including its final `check_ceiling` pass, inside the 540 s deadline.
That is a timing receipt for one host, not a scientific result: the candidate was
neither declared, decided, nor retained.

These commands reproduce the bounded receipts without starting a production run:

```bash
shasum -a 256 \
  campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting --help
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen --help
uv run --frozen --all-extras --group dev python -m devtools.declare_least_cell_mass --help
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate --help
uv run --frozen --all-extras --group dev python \
  resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py
.venv/bin/python3 cases/n11_fractional_certificate/thirdparty/check.py
.venv/bin/python3 cases/n11_fractional_certificate/minimal_verify.py \
  --unpinned cases/n11_fractional_certificate/certificate.json
```

The warm-start receipt uses the production driver with no output paths and an iteration
cap of zero. Its zero total is non-scientific; only the successful state reconstruction
is a preflight result:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 0 --iterations 0 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --warm campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json
```

## Output and checkpoint ownership

BC-219 reserves this manager-only root, but a Git checkout does not materialize an empty
directory. After checking the reservation, the manager creates and tests it from
`packing/`:

```bash
mkdir -p campaign/series/series-000-smoke-and-calibration/results/agenda-025
test -d campaign/series/series-000-smoke-and-calibration/results/agenda-025
test -w campaign/series/series-000-smoke-and-calibration/results/agenda-025
```

Inputs outside that directory are read-only.
Never overwrite `bc-200-state-191-50.json` or a retained certificate.
Both drivers append their progress logs, while state, summary, and candidate paths may
be replaced. Before a launch, require every path in its output stem to be absent.
If a stem already exists, preserve it and allocate the next two-digit leg or a new
descriptive stem; never rerun into the old paths.
Use these stems:

| BC | Required outputs under `results/agenda-025/` |
| --- | --- |
| BC-230 | `bc-230-adaptive-core-contract.md`, `bc-230-control-matrix.md` |
| BC-232 | `bc-232-leg-NN.log`, `bc-232-leg-NN-state.json`, `bc-232-leg-NN-summary.json`, `bc-232-leg-NN-family.json`, `bc-232-disposition.md` |
| BC-233 | `bc-233-screen-INSET.{log,rows,json,candidate.json}`, `bc-233-{released,control}.{log,rows,json,candidate.json}`, `bc-233-disposition.md` |
| BC-231 or later | source and tests in the existing fractional package, `packing/cases/n11_fractional_certificate/adaptive_minimal_verify.py`, plus BC-numbered receipts and candidates here |
| Gate | `gate-hour-NN.md` with disposition, exact paths and hashes, changed-path manifest, wall/CPU cost, receipts and refusals, next slices, and coordinator requests |

Every long runner writes a fresh state or candidate path, an append-only progress log,
and a machine-readable summary.
Hash a frozen candidate before review.
A manager may propose H-070..079 and exp-070..089 in a gate packet, but the coordinator
allocates and creates those shared records before use.

Two driver boundaries matter:

1. `run_fractional_cutting --freeze` writes the best exact **packing family**, even when
   its total is below 11. It does not serialize the current primal site weights.
   If a row-converged covering objective falls below 11, stop that lane, preserve the
   state, and run `devtools.freeze_cutting_primal` on it (the command is in the 61/16
   section below): the bridge regenerates rows to convergence on the state’s sites,
   re-solves the covering program, rationalises the weights the way the column generator
   does, and writes a `least_cell_mass`-null candidate for the declaration bridge and
   the two-route decision.
   The float objective is not a bound certificate, and neither is the bridge’s total
   until `decide_certificate` accepts the frozen bytes.
2. `run_fractional_colgen` has no resume checkpoint.
   `--column-rounds 1` is the fixed grid screen; later rounds add priced site orbits and
   release the support.
   A clock stop can leave logs but no candidate.
   Treat that as time-limited, never as convergence.

## First four hours

The manager owns BC-230 and supervises one BC-232 process plus the matched BC-233
processes, all pinned to one numerical thread; compute processes do not consume agent
slots. The portfolio’s one floating agent starts on closure BC-240 and moves to the
BC-230 review when that 105-minute theorem packet returns.
BC-231 does not open before the theorem is reviewed and frozen at the hour-four gate.

| Active Portfolio Time | Manager / BC-230 | BC-232 process | BC-233 processes |
| --- | --- | --- | --- |
| 0--15 min | Verify packet hashes, create the reserved output root, refuse reused stems, and freeze accept rules and worker write scopes. | Load the JSON state, confirm its 181-direction compatibility, and launch leg 1. | Run the n17 source control; record that published `M` is the doubled margin. Confirm the strict-JSON deadline control, while keeping every deadline stop time-limited and ineligible for comparison. |
| 15--45 min | Draft the lemma, serialized fields, seam rules, scalar specialization, and refusal matrix. | Run leg 1. | Run the three one-round, equal-grid inset screens sequentially; choose only among candidates that were emitted. |
| 45--87 min | Complete the contract and turn every premise into a BC-231 positive or mutation test. | Run leg 1. | Run the selected released seed and unseeded control concurrently for the same 42-minute deadline. |
| 87--105 min | Freeze the author draft for review. | Run leg 1. | Compare only equal-status outputs; run quick refusals and reserve a full decision for any mass below 11. |
| 105--120 min | Hand the frozen draft to the floating reviewer returning from BC-240; supervise the compute lanes. | Finish the 105-minute leg 1, hash its outputs, and prepare the exact leg-2 command. Launch leg 2 only after the T+2 landing. | Freeze the screen, release, control, cost, and keep-or-retire packet; launch nothing new. |
| 120--195 min | The floating reviewer audits theorem scope, seams, scalar specialization, and controls; the manager answers only concrete blockers. | Run leg 2. | No new run; preserve all outputs. |
| 195--225 min | Reconcile the review and all three BC dispositions. | Finish the 105-minute leg 2; report endpoints, convergence, width, cost, and the 30 CPU-minutes still owed before the routing test. | Submit the frozen trajectory and disposition. |
| 225--240 min | Freeze launches and submit `gate-hour-04.md` to the coordinator 15 minutes before the gate. | No new run. | No new run. |

Exp-060’s retained 36-minute run completed nine iterations in 2,255.7 seconds.
Its last iteration cost 146.7 seconds in row generation, 28.9 seconds in the LP, and
246.4 seconds in exact separation.
A 105-minute leg is therefore a scheduling unit, not an iteration promise.
`--rows-rounds 2` follows exp-060’s measured reopen condition; do not restore the old
12-round setting. Two legs spend 210 CPU-minutes.
The hour-four packet must label its width provisional; after the next gate opens, run
one fresh 30-minute leg before applying the pre-registered 25-percent rule.

### BC-232 launch

Run from `packing/`. The first leg reads the retained input and writes four fresh
outputs:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 105 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --warm campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json
```

Leg 2 changes `--warm` to the leg-01 state and every output stem to `leg-02`. After each
leg, require a zero exit and the fresh state, summary, family, and log paths named by
the command. A missing output or an unreadable state is a technical failure, not a
scientific result and not permission to rerun into the same stem.

Take the maximum exact `best_scaled_total` seen so far as the lower endpoint and the
smallest float `rows_objective` from an iteration with `rows_converged: true` as the
computational upper endpoint.
Preserve those different evidential labels.
Stop immediately on a `verify_ceiling` packing family of total at least 11; that closes
the current one-body formulation at 3.82. Also stop on a row-converged objective below
11, preserve the state, and run the covering bridge on that state; the float crossing is
a candidate for that bridge, not a bound.
Do not apply the width rule at the hour-four gate after only 210 CPU-minutes.
After the frozen additional 30-minute leg, continue only if
`new_width <= 0.75 * old_width`, which here means width at most `0.86078351094543675`; a
larger width retires this checkpoint until its recorded reopen condition changes.

### BC-233 launch

Massaccesi defines `M` as **twice** the one-sided empty margin.
The project driver’s `--inset` is the one-sided margin because its grid spans
`L - 2*inset`. Thus the published final `M = 15513/10000` maps to `--inset 15513/20000`.
At n=11, screen this declared set:

1. `1/2`, the project control;
2. `2962983/4505800`, the published final margin scaled by `L_n11/L_n17`; and
3. `15513/20000`, the published absolute one-sided margin.

All three use grid counts `25,34,41`, one column round, scale 4,000,000, and a
540-second deadline.
Pass the scale explicitly: this driver defaults to 200,000 even though the library and
NPZ checkpoint driver use 4,000,000. The template is:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --grid-counts 25,34,41 --inset INSET \
  --angle-limit 207107/500000 --direction-steps 180 --scale 4000000 \
  --column-rounds 1 --max-rounds 60 --rows-per-direction 3 \
  --deadline-seconds 540 \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-233-screen-INSET.log \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-233-screen-INSET.rows \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-233-screen-INSET.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-233-screen-INSET.candidate.json
```

Replace `/` in the filename stem with `-`. A screen is eligible only when the process
exits zero, its summary is strict JSON, its final row loop reports convergence, and its
candidate path exists.
Rank eligible screens by the exact rational `total_mass` in the candidate bytes; record
every ineligible run and stop BC-233 if none remains.
Hash the selected candidate before using it as a seed.

Run that candidate as `--seed-certificate ... --seed-map centre` with the control inset
`1/2`, `--column-rounds 8`, and `--deadline-seconds 2520`. Run the unseeded control with
the same arguments and deadline but no `--seed-certificate`. Use fresh `released` and
`control` output stems.
`centre` preserves the seed at the same side; `scale` is equivalent here but leaves the
intent less clear.

If either follow-on emits total mass below 11, do not rerun the generator: a clocked
rerun can stop after a different round and would no longer decide the candidate that
crossed the threshold.
Hash the raw candidate, fill its null `least_cell_mass` with the existing one-worker
declaration bridge, hash the resulting bytes, and then decide that path:

```bash
shasum -a 256 \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/CANDIDATE.json
uv run --frozen --all-extras --group dev python -m devtools.declare_least_cell_mass \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/CANDIDATE.json
shasum -a 256 \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/CANDIDATE.json
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/CANDIDATE.json
```

Any fully decided mass below 11 routes immediately to BC-238 and outranks the seed
comparison. Otherwise, the seed earns one continuation block only if both arms have
strict summaries, emit candidates after the same number of completed column rounds with
the same stopping class, and the released candidate’s exact rational `total_mass` is
strictly smaller than the control’s. That is an exploratory search-routing result, not
theorem evidence or a causal claim about the margin.
Equal or larger exact mass retires the seed.
A lower float LP objective, unequal stopping status, deadline stop, or failed inset
screen is unresolved and earns no continuation.

### Scalar probe at 61/16: a pre-registered first-block option

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

## Development and gate validation

BC-231 must leave this source-distinct decision surface for BC-238:

```bash
.venv/bin/python3 cases/n11_fractional_certificate/adaptive_minimal_verify.py \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/CANDIDATE.json
```

The standalone program may use only the Python standard library, must parse the frozen
adaptive object independently, and must not import `sqpack` or call either project
decision route. A candidate cannot enter BC-238 until this command and the project sweep
and interval routes agree on the retained positives and all adaptive mutations.

For a scalar candidate from BC-232 or BC-233, the existing source-distinct route is:

```bash
.venv/bin/python3 cases/n11_fractional_certificate/minimal_verify.py \
  --unpinned \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/CANDIDATE.json
```

A `verify_ceiling` packing family from BC-232 does not have this schema and must not be
sent to either certificate verifier.
Its exact weight-at-least-11 verdict closes BC-232’s formulation, but it is not a
lower-bound candidate and does not enter BC-238.

The fast contract-seam slice is:

```bash
uv run --frozen --all-extras --group dev python -m pytest -q \
  tests/test_fractional_classcert.py \
  tests/test_fractional_cutting.py \
  tests/test_colgen_checkpoint.py::test_a_resumed_run_continues_rather_than_restarting \
  tests/test_run_fractional_colgen.py::test_a_deadline_stop_leaves_the_table_and_no_candidate \
  tests/test_run_fractional_colgen.py::test_deadline_before_first_round_writes_strict_json \
  tests/test_run_fractional_colgen.py::test_summary_json_refuses_unexpected_non_finite_values \
  tests/test_declare_least_cell_mass.py \
  tests/test_decide_certificate.py \
  tests/test_freeze_cutting_primal.py \
  tests/test_run_fractional_cutting.py \
  -m 'not exhaustive_exact and not exhaustive_interval'
```

The planning spike on 2026-09-05 passed 83 tests with two exhaustive tests deselected:
1.45 seconds in pytest and 1.84 seconds wall on this checkout.
The integrated readiness slice passed 88 tests with two exhaustive tests deselected in
3.52 seconds of pytest time.
With the two test files the 2026-09-05 review added, the same slice passed 94 tests with
two deselected in 4.24 seconds of pytest time on the reviewer’s macOS host.
This proves only that the existing seams are green; it is the baseline BC-231 must
preserve.

For adaptive implementation, add focused tests in
`tests/test_fractional_certificate.py`, `tests/test_fractional_interval.py`,
`tests/test_fractional_sweep_integer.py`, and `tests/test_decide_certificate.py`, with
generator/serialization tests in `tests/test_run_fractional_colgen.py`. Run the exact
positive replays and both exhaustive marker groups at the gate, serialized away from
optimization workers.
Before handing changed code to the coordinator, run:

```bash
uv run --frozen --all-extras --group dev packing-validate --edit
```

The coordinator runs the push or full tier after integration.
A candidate is not a result until frozen bytes pass the central two-route decision,
source-distinct replay, mutations, hash re-read, and coordinator retention decision.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
