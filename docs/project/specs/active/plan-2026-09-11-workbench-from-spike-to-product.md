---
title: The Workbench, From Spike to Product
description: Repairing the current workbench and consolidating its live code into a standalone package
author: Claude and Codex agents, for the repository maintainer
---
# Feature: The Workbench, From Spike to Product

**Date:** 2026-09-11

**Updated:** 2026-09-13

**Status:** Active; package foundation and correctness repairs implemented, broad
migration in progress

**Workflow:** W7 pipeline improvement

**Tracking:** `think-ooi2` (product epic), `think-zisr` (standalone package)

**Reviewed baseline:** `6e191a35`, with findings in the
[2026-09-12 workbench stack architecture review](../../reviews/review-2026-09-12-workbench-stack-architecture.md)

## Authority and Implementation Entry Point

This plan is the top-level source of truth for the finished workbench, the required
outcomes, and their delivery order.
The review records findings and resolution evidence; beads carry implementation status,
prerequisites, and closure receipts.
The [annealing](plan-2026-09-11-annealing-as-a-search.md),
[shared-contract](plan-2026-09-09-packing-strategies-as-a-shared-language.md), and
[video](plan-2026-09-07-known-best-atlas-video.md) plans provide detailed contracts and
research or illustration deliverables under this sequence.
They do not independently advance the workbench’s release phase.

Start with `think-5pv0` (refresh the reviewed stack) and `think-a9gt` (consumer and
legacy-task inventory).
These can proceed independently.
Then `think-l9z0` establishes the package shell and source discovery before any repair
introduces new workbench files.
Take the next unblocked implementation task in the current phase; an epic being ready
does not mean its children have passed their prerequisites.

Update this plan when a requirement or phase changes.
When fixing a review finding, update its resolution row with the implementing commit and
check, and close the owning bead with that evidence.
Creating a bead or moving a file does not resolve a finding.

## Outcome

The workbench becomes a standalone browser package at `packages/workbench/`. It owns the
Pack and Animate application, reusable geometry and simulation code, the animation
timeline and rendering, a browser-free Node API, package-local checks, and a
deterministic static build.
Workbench-specific build, benchmark, capture, and Python adapters live inside the same
package. Existing general-purpose `sqpack` libraries remain dependencies.

The package shell starts in Phase 0; broad live-source consolidation starts only after
the evidence, correctness, and strict-new-source checkpoint in Phase 2. Search remains
deferred until the annealing record reports valid distributions and the page and
benchmark use the same packing-validity contract.

## Required Final Outcomes

| Outcome | What the user or maintainer can do | Completion evidence |
| --- | --- | --- |
| O1 — One owned package | Build and maintain the application, numerical core, animation, tests, probes, and workbench-specific tools in `packages/workbench/`. | Package commands run independently; all live consumers have migrated; no production build or command reads the spike tree. |
| O2 — Usable Pack | Choose any `n` in a declared measured range, start from generic or supplied poses, manipulate squares, run, pause, restart, reset, resolve, and replay a visible seed. A known record is optional. | Cases with and without catalogue records work; exactly `n` squares are present; raw and repaired scores match displayed geometry; stale/cancelled runs cannot overwrite current state. |
| O3 — Reusable experiments | Change proposal, contact/force model, annealing or container schedule, repair, objective, and run budget through typed configurations; compare runs under equal work. | Browser and headless callers use one kernel and effective configuration; two strategy variants run through it; receipts retain work, seed, validity and provenance. No better packing is promised as a software acceptance condition. |
| O4 — Clean illustration engine | Replay a trace or author an illustration, seek deterministically, draw SVG, and capture frames/video with explicit timing, arrival, side and rotation. | Drawing a frame needs no solver; seek and capture agree; direct and physically generated motion retain their labels; illustrative frames never acquire numerical assurance. |
| O5 — Experimental Search | Run many Pack trials, cancel with honest partial accounting, inspect the best valid arrangement and outcome distributions, and use calibration/held-out presets. | The same trial matches Pack and headless output; manifests reproduce disjoint-block reports; invalid outcomes never rank; tuning and held-out cohorts are explicit. Search ships after the clean Pack/Animate release boundary. |
| O6 — Clear, accessible UI | Use mode-specific controls and presentation/research layers, readable responsive layout, keyboard interaction and reduced-motion playback. | Browser checks exercise startup, tab switches, focus, transport, labels and representative viewport sizes; the consumer audit dispositions existing UI defects and preserves working behavior. |
| O7 — Reproducible publication and maintenance | Follow a package quickstart, build a static Pages artifact, and verify the deployed workbench under `/squares/workbench/`. | Strict Python/TS/JS floors discover all live source; required CI and full checkpoint pass; source/build identity and post-deploy behavior agree; the explainer link stays under `/squares/`. |

The Phase 4 checkpoint delivers O1, O2, O4, O6 and O7 with a reusable single-run core.
Phase 5 completes O3 and O5 and reruns the complete outcome set.
Local Python/Rust services, universal cross-language trajectory identity, new
mathematical discoveries, and unbounded resource support are separate future work; the
browser exposes only the capabilities implemented by its static build.

## Current Baseline

The first conversion plan has mostly landed.
Git history keeps its retired chunk plan; this document now records the work that
remains.

| Surface | State at `6e191a35` |
| --- | --- |
| Browser source | The HTML template, 7,431-line `workbench.js`, 1,099-line stylesheet, and ordinary checker probes are separate files. |
| Browser floor | Biome checks JavaScript and CSS. `tsc` checks the workbench, probes, and Motion Lab as separate global programs with four legacy flags relaxed. That browser floor runs in `packing-validate`; the behavioral workbench scripts do not. |
| Python floor | The retained spike tree is still excluded from Ruff and is outside BasedPyright’s include set. Parent PR #125 removes that exclusion at `ee60689b`, but PR #155’s reviewed head does not contain that commit. Python moved into `devtools` is checked, while JavaScript embedded in its strings remains invisible to the browser floor. |
| Palette | The browser still carries literal copies of the `sqpack.render` palette, shades and angle tolerance. The Phase 0 inventory corrects the earlier statement that generation had landed; `think-fk8h` remains required under `think-w0a1`. |
| Publication | `devtools.build_workbench_site` still invokes the retained spike builder. At this baseline it reproduces a self-contained 4.4 MB page at `/workbench/`. The old unchecked-prototype banner has been replaced by a quiet evidence warning. |
| Product shape | Pack runs one interactive trajectory. Animate plays a range of retained atlas records and illustrative transitions. The page has no Search mode and Pack still depends on atlas transition pairs instead of accepting an independent `n`. |
| Runtime shape | One IIFE owns application state, geometry, two related physics loops, timeline, SVG rendering, facts, controls, and the public API. The cached transition simulator and live optimizer repeat collision, wall, broad-phase, and integration logic. |

One regression crosses the completed extraction boundary: `devtools/bench_annealing.py`
contains `TRIAL_JS` and `GUARD_JS` Python strings.
Its trial string also carries a third separating-axis implementation and the only
current caller of the new seed API. The manually maintained API declaration consequently
omits `setSeed` and `seed` while the browser type check remains green.

## Product Semantics

### Implementation Checkpoint — 2026-09-13

The leaf incorporates PR #125 at `27d2f8cc`. PR #155 now carries the historical record
repairs through `e13ff926`; its required hosted checks, Pages build and browser jobs
pass. The package implementation is being prepared as the third and final PR in this
stack.

The foundation introduces the private `@squares/workbench` workspace, strict module
build, package-local Python adapters and immediate source discovery.
Implemented repairs include animation/strategy admission, canonical benchmark references
and execution receipts, exact uint32 seeds, and post-step optimizer snapshot validation.
The actual page consumes strict API, force-law, navigation, corpus and timeline modules.
Its palette and shades come from `sqpack.render`; the workbench’s separately named 0.5°
angle-clustering input is not the renderer’s 1e-6-radian tolerance.

The reporter joins explicit seed/status/work manifests, keeps failed and unfinished
slots in disjoint blocks, checks source/reference/budget agreement, and reports
denominated rates and conditional distributions.
The historical-summary inventory documents missing raw inputs and the exact disputed
cells; it does not recreate them.
See the review’s
[cohort reconciliation](../../reviews/review-2026-09-12-workbench-stack-architecture.md#retained-cohort-reconciliation--2026-09-13).

These repairs do not complete Phase 3. Most legacy app, painter and simulation code
still lives in the retained script and inherits four documented compiler relaxations.
After typed boundaries were introduced, its strict audit reports 1,246 diagnostics; that
inventory must reach zero before `think-4ylo` or merge readiness closes.
The next disjoint migration slices are colour/view helpers, shared geometry/contact,
cached trajectories, live optimizer, painter, then the app/controller.
The package build still reads the retained spike until those consumers move under
`think-g0lh`. The focused accessibility checks also need a durable behavioral CI entry
point before `think-y9pw` closes.
Arbitrary-n Pack, shared bounded Resolve, trace editing/capture, Search/calibration and
actual release remain open under the phases below.

### Mode Contracts

The product has three aspects with one set of computational building blocks:

- **Pack** accepts one `n`, one seed, one starting arrangement, and one parameter set.
  It runs a single trajectory and supports direct manipulation.
  `n` is independent of the presence of an atlas transition pair; the supported resource
  envelope is explicit and tested.
- **Search** asks Pack’s browser-free trial function for many seeded runs and summarizes
  validity, best-of-k, and the outcome distribution.
  It does not have its own physics engine.
  Search ships only after the annealing plan’s measurements and resolver are in order.
- **Animate** presents imported records and deterministic trajectories on a timeline.
  Retained record poses remain authoritative at integer frames.
  Any simulated motion between them is labelled illustrative and cannot create numerical
  evidence.

The older unbuilt **Calibrate** concept becomes a set of Search presets, such as a
parameter sweep over cases with known records.
There is no Calibrate tab, controller, or loop engine.

## Package Boundary

Use top-level `packages/workbench/`, as the owner explicitly requested on 2026-09-12.
This is a deliberate exception to the existing rule placing code under `packing/`. The
migration must update that layout rule and all path-sensitive tooling together.
All new workbench-specific source belongs here; neither `packing/devtools/` nor the
spike tree is a second home for the application.
Contract repairs may edit existing live files in place, but every newly introduced
workbench file starts in this package with lint, type, and test discovery wired in the
same change. Phase 3 completes the migration; it is not a reason to scatter temporary
modules elsewhere during Phases 1 and 2.

The target package has these ownership boundaries:

```text
packages/workbench/
  package.json
  src/
    core/          geometry, packing metrics, resolver, seeded random streams
    simulation/    one step kernel, force laws, trajectory and live-run adapters
    animation/     timeline, interpolation, playback and reduced-motion policy
    view/          SVG stage, facts, gap bar and accessible descriptions
    app/           state, controls and Pack/Animate tab composition
    data/          versioned import validation and normalized frame adapters
    api/           browser and browser-free public entry points
  tests/           unit, contract, parity and deterministic-frame checks
  probes/          browser behavior probes grouped by public contract
  tools/           workbench build, benchmark, capture and optional Python adapters
```

The package build bundles typed or checked modules into a self-contained page.
The build must resolve module dependencies explicitly; independent source files must not
depend on accidental concatenation order.
Write new reusable modules in TypeScript.
A migrated legacy fragment may remain checked JavaScript only while it has complete
JSDoc types and passes the same strict compiler flags.
Each source file enters a package-local type-check program.

### Source Floor

The closed `think-4cwy` adoption recorded four flags relaxed for the legacy global
programs. `think-4ylo` owns their removal from retained live workbench code and requires
them for every promoted module: `noImplicitAny`, `strictNullChecks`,
`noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes`. The package also inherits
the strict base flags, including `noImplicitOverride`, `noImplicitReturns`,
`noFallthroughCasesInSwitch`, and consistent filename casing.

Biome formats and checks all TypeScript, JavaScript, JSON, and CSS with zero warnings.
Its type-domain promise rules cover TypeScript.
If any checked JavaScript remains, a focused type-aware ESLint overlay enforces
`no-floating-promises`, `no-misused-promises`, and `await-thenable`, because Biome does
not enforce those rules for JavaScript.
Gate configuration tests enumerate every live source extension and fail when a source,
test, or probe is outside lint or type coverage.

No slice may add `any`, `@ts-ignore`, a global rule switch, a relaxed compiler flag, or
a source exclusion to make the gate pass.
Package-local Python adapters use typed records and pass the project’s Ruff and
BasedPyright gates at zero findings and warnings.
Extend Python source discovery to `packages/workbench/`; a file outside `packing/` must
not escape the floor.

### Browser-Free API

The Node entry point has no DOM dependency and exposes the same numerical operations the
browser uses:

- validate and normalize a frame or starting arrangement
- measure walls, pair gaps, deepest overlap, and required container side
- resolve an overlapping arrangement without claiming an improvement
- advance one seeded simulation and collect a trajectory
- run one Pack trial and return its receipt

The browser supplies clocks, events, SVG nodes, and paint scheduling through adapters.
The command-line benchmark calls this entry point directly, so it measures simulation
cost without loading Playwright or copying physics into a probe.

### Simulation Boundary

One pure step kernel owns contact detection, wall forces, broad-phase selection, force
accumulation, and integration.
The cached Animate trajectory and the live Pack run use separate adapters because their
state machines differ: Animate targets a retained end frame and collects samples; Pack
supports growth, open-ended execution, and a held square.
Search calls the Pack adapter repeatedly.
The adapters must not reimplement the kernel.

### Data and Evidence Boundary

The package never reaches into `atlas/`, `campaign/`, witnesses, or Python solver
modules by relative path.
A package-local assembler may use general-purpose `sqpack` APIs to validate those
sources and emit a versioned JSON input.
Catalogue export is an explicit integration step; the built browser and ordinary
headless trial API do not require Python.
The package rejects unknown versions, nonfinite geometry, wrong square counts, unstable
identities, unsupported evidence values, and missing provenance before rendering or
simulation.

Reuse the Motion Lab contract’s useful invariants:

- stable, ordered square IDs; finite centers and angles; and a finite positive container
  side
- explicit frame kind, solver phase, evidence status, and typed overlays
- separate scenario-runner and capability declarations, so the UI exposes only
  operations a scenario supports
- declared limits for square count, sweeps, and time budget rather than silent clamps

The normalized package frame uses radians and stable IDs.
Legacy workbench arrays in degrees enter through an adapter.
Motion Lab’s Python quench, snapping implementation, and evidence records remain
separate scientific components.
Shared JavaScript geometry is adopted only after common contract vectors prove parity
across the workbench, Motion Lab, and the Python verifier.

## Ordered Delivery

The phase numbers below govern implementation.
The research and contract plans retain their local section names for detail.
A task may start only after its own blocker dependencies pass; parent membership alone
does not enforce this ordering.
Implementation started on 2026-09-13 via the `implement-beads` shortcut.
The parent refresh is complete at `27d2f8cc`: PR #125 `0281a508` is integrated with PR
#155 `6e191a35` and planning commit `24bca6ae`. The refreshed records gate passes Ruff
and schema checks and reproduces only the documented campaign/documentation failures,
owned by `think-3eha`. Earlier prototype accomplishments remain in the baseline and are
audited before being redone.

### Phase 0: Establish the Integration and Package Foundation

| Bead | Deliverable | Done when |
| --- | --- | --- |
| `think-5pv0` | Refresh the leaf from the current PR #125 parent. | Record parent/leaf revisions; include `ee60689b` and `0281a508` or verified equivalents; preserve #155 records and reproduce its known failures before repairs. |
| `think-a9gt` | Inventory sources, consumers, unique assertions and legacy tasks. | Every build, CI, capture, benchmark, documented CLI and research reproduction route has a move/retain/replace/remove disposition and a task owner. |
| `think-l9z0` | Create the small root package shell and immediate gate coverage. | Locked package scripts and strict source discovery cover real TS and Python shell inputs plus the existing JS controls; no package JavaScript is introduced before its promise overlay; layout rules, hooks and validation selection cover the new root; deliberately missed source/config fixtures fail. |

Refresh and inventory are independent.
The shell depends on both.
The completed
[consumer inventory](../../reviews/review-2026-09-13-workbench-consumer-inventory.md)
records 211 v2 files, 23 Python entry points and 180 probes with replacement owners.
It also requires `think-g0lh` to replace the incomplete Pages input list with the actual
catalogue, witnesses, rendering, fonts, assembler, package source and lockfile inputs.
Record annotations can proceed after refresh; source repairs that introduce workbench
files use the shell.
This separates a minimal destination from the later migration of the live application.

### Phase 1: Repair Evidence and Executable Contracts

| Bead | Deliverable | Done when |
| --- | --- | --- |
| `think-3eha` | Repair campaign integration and provenance (R4). | Unique experiment IDs, actual numerical/effort fields, source references, index, footers and generated views pass their existing gates; unavailable historical evidence is annotated, never invented. |
| `think-sdmi` | Validate animation imports (R1). | Coincident/out-of-bounds/nonfinite/wrong-count imports cannot acquire checked status; a valid retained control carries the actual validator/tolerance/provenance. |
| `think-karf` | Enforce strategy and trace semantics (R2). | Grid phases preserve exactly `n`; unsupported sources/fields fail; effective seed/config, per-frame side/time/identity and guidance ancestry survive execution/export. |
| `think-1fpa` | Apply one admission rule to run/replay/report/sweep (R3). | Missing/nonfinite/invalid results never rank; empty admitted populations are explicit; all attempts and rejection causes are counted. |
| `think-dq1l` | Define exact seed semantics (R5). | Boundary seeds and the reproduced alias pair behave under the declared integer mix; effective seed receipts and browser/headless replay agree. |
| `think-6hqs` | Validate the live optimizer’s exact returned snapshot (R10). | Post-step poses/angles/size are checked before ranking; best receipts retain the checked geometry; growth and convergence are not confused with unit-square feasibility. |
| `think-4z7d` | Repair distribution reporting and durable inputs. | Disjoint blocks, uncertainty, rates and work reproduce from a manifest; prefix observations stay labelled; missing raw inputs remain a declared limitation. |
| `think-jdgu` | Reconcile the n17/deep-cohort and difficulty narrative. | Every statement names the actual retained parameter cell and resolved status, or is annotated unsupported; normalized and absolute comparisons cannot imply a causal size result. |
| `think-3hb7` | Recover or disposition the compaction instrument (R6). | Committed instrument/controls reproduce the result, or the historical negative is marked unreproducible and no longer used to settle the resolver question. |

Record repair and geometry/strategy repairs have separate deliverables and can run in
parallel. Distribution reporting follows admission repair and record reconciliation;
narrative correction follows the reporter.
Historical claims may be dispositioned without a new campaign.
A new measured round requires its own hypothesis, budget, inputs and acceptance rule
under the annealing plan.

### Phase 2: Repair Behavior and Establish Strict Module Gates

| Bead | Deliverable | Done when |
| --- | --- | --- |
| `think-7f3p` | Remove remaining executable JS/HTML literals (R8). | Trial, guard, build and probe programs are ordinary checked package files; shared runtime calls replace copied simulation, with independent verification preserved where useful. |
| `think-gxxc` | One public API/type contract (R8). | Runtime and declarations agree, including `setSeed`/`seed`; negative key/shape controls fail the normal gate. |
| `think-4ylo` | Establish the full tbd Python and TS/JS gate; complete graduation during Phase 3. | Every new module passes strict compiler/lint/promise checks immediately. After live-source migration, Ruff/BasedPyright and compiler/lint/promise checks have zero findings across all retained live code, with no broad exclusions, suppressions or legacy flag inheritance. |
| `think-nals` | Shared validity and bounded Resolve. | Raw and repaired states remain separate; finite/count/pair/wall checks agree; repair succeeds only after post-validation and reports stalled/budget/nonfinite outcomes honestly. |
| `think-y9pw` | Accessible stage and controls. | Current descriptions, focus, keyboard manipulation/transport and reduced-motion behavior pass served-page assertions. |
| `think-kpvc` | Measured behavioral PR coverage (R8). | Startup, run/reset, modes, validity, seed replay and frame provenance reach the appropriate existing tiers; a broken behavior fails CI, and the builder’s inaccurate gate claim is corrected. |
| `think-109t` | Correctness and strict-new-source checkpoint. | The refreshed commit, executable repairs, semantic checks and strict new-source gates pass. The remaining legacy typing inventory is explicit; final graduation belongs to `think-4ylo`, before merge readiness. |

The Python parent-floor change is integrated, not recreated.
The closed browser-floor adoption bead `think-4cwy` remains historical; `think-4ylo`
owns all remaining strict flags.
Fast checks join PR validation as soon as the source appears.
Measure slower capture/trajectory checks before assigning their tier.

The 2026-09-13 strict audit measured 1,030 errors in the legacy workbench and 249 in 124
probe files. Most are implicit types, nullable DOM references and unchecked indexes.
Typing and coherent module extraction therefore proceed together; a separate pass adding
1,279 local annotations before moving the same code would preserve its poor boundaries.
This revises the original sequencing, not the final floor: `think-109t` no longer waits
for `think-4ylo`; final migration `think-g0lh` precedes `think-4ylo`, which explicitly
blocks `think-9sdr`. Existing legacy lists may only shrink.
New modules never inherit their relaxed flags, and behavior/assurance repairs remain
prerequisites for broad extraction.

Pages runtime (`think-l6l4`) and project-subpath navigation (`think-5wnw`) can be
repaired alongside these tasks.
Their final integration is checked after the package build moves.

### Phase 3: Consolidate the Live Package

`think-zisr` groups these slices.
Each promoted domain is strict TypeScript, with explicit imports and an executable
contract at its caller boundary.
Promote core/API, data/simulation, view/timeline, then application wiring and probes;
the build consumes the package bundle throughout.
`think-4ylo` closes only after the last retained source has graduated, before the Phase
4 merge-readiness checkpoint.
Each executable child is blocked by the repair checkpoint or by children that already
depend on it; the epic’s own blockers are not the scheduling mechanism.

| Bead | Deliverable | Depends on |
| --- | --- | --- |
| `think-nubm` | One DOM-free geometry/simulation kernel, typed configuration and Pack/trajectory adapters. | `think-109t` |
| `think-w0a1` | Versioned frame, strategy, catalogue/palette and IO adapters. | `think-109t` |
| `think-ywj4` | Pure timeline, view and capture adapters; explicit arrival and evidence. | `think-w0a1` |
| `think-6qxx` | Versioned proposal/force/schedule/repair/objective interfaces, mechanism registry and declared capabilities. | `think-nubm`, `think-w0a1` |
| `think-883t` | Strategy/trace import, editing, replay and export in the app. | `think-6qxx`, `think-ywj4` |
| `think-8cti`, `think-rdee` | Mode composition and start/transport controls, preserving verified prototype behavior. | Kernel plus the applicable timeline/data adapter |
| `think-iqvm` | Direct illustration versus physically generated trajectory choice and receipts. | Timeline and mode composition |
| `think-tcns` | Repeatable headless throughput benchmark with work counters. | `think-nubm` |
| `think-g0lh` | Switch app, build, capture, probes and tools to package sources; migrate consumers. | App/trace/mode adapters, runtime and navigation repairs |

The kernel receipt separates **feasibility**, **termination**, and **stationarity**. It
records arithmetic, timestep, configuration, steps/work, final motion residuals and
termination reason. A feasible state at a work limit is not necessarily converged.
A stationary label needs a declared threshold/window, with continuation controls after
forcing decays. The benchmark reports warmup, repetitions, source/runtime/host and
effective configuration; throughput alone proves neither feasibility nor convergence.

**Package acceptance:** build, lint, typecheck, tests and headless benchmark run from
the package directory; Node imports need no DOM; fixed-seed metrics/frames agree before
and after each extraction slice.
Browser and Node use the same implementation.
Python projection and browser contact physics agree only on declared shared invariants
unless their algorithm definitions are actually equivalent.

Data adapters reject unknown versions, nonfinite poses, count/identity/time errors,
unsupported capabilities and false evidence.
Generic Pack does not require catalogue data.
Drawing and replay need no solver.
The root Pages workflow receives deterministic, self-contained output under
`packing/site/workbench/`; it does not own application source.
Quickstart, package scripts, input formats and optional dependencies are documented with
the migration.

### Phase 4: Finish Pack, Remove Obsolete Consumers, and Release

| Bead | Deliverable | Done when |
| --- | --- | --- |
| `think-uhqw` | Complete arbitrary-n Pack. | Generic and supplied starts work without an atlas pair; optional record start, effective seed, direct manipulation, import/export and cancellation obey O2 within measured limits. |
| `think-cqfc` | Retire obsolete sources after migration. | The Phase 0 inventory proves each old entry point and duplicate/revision assertion is replaced or unused; no live consumer reads the spike tree. |
| `think-9x0m` | Implement post-deploy verification. | The checker passes against a served package artifact and rejects wrong/missing/stale output; it is wired after deployment without depending on an actual merge to be implemented. |
| `think-9sdr` | Record Pack/Animate merge readiness. | O1/O2/O4/O6/O7, review dispositions, package gates, record checks, hosted required checks and the full checkpoint pass on one integrated revision. |
| `think-tn6s` | Execute release and verify the live page. | After the merge decision, the validated artifact is deployed and the published source identity, startup and `/squares/` navigation pass; retain the URL/revision/check receipt. |

`think-9sdr` depends on migrated consumers, arbitrary-n Pack, direct animation, headless
benchmark, Pages fixes/checker, and evidence reconciliation.
It produces a concrete merge decision.
`think-tn6s` follows it; a live success receipt is never required before the checker can
be implemented. Pull requests build/test and do not deploy.

The inventory must disposition current UI work too: responsive stage/controls, facts and
source layers, numeric formatting, gap-bar labels, mode-state persistence and stale
checker/instrument paths.
Preserve delivered behavior, fix confirmed defects in this phase, and explicitly
identify optional additions.
A legacy bead’s unchecked description is not proof that its feature is absent; verify
before reimplementing it.
The release checkpoint cannot pass with an unassigned required outcome.

Retain archives, negative results and reproducible research instruments.
Temporary old-path wrappers require a named live consumer and a retirement condition.
Git retains discarded prototype code; neither a flat devtools move nor a second package
tree constitutes consolidation.
Search remains unavailable at this release boundary.

### Phase 5: Complete Experimental Search and Calibration

| Bead | Deliverable | Done when |
| --- | --- | --- |
| `think-gfqt` | Bounded experimental multi-run scheduler. | Configurations from `think-6qxx` vary proposal, force/contact model, annealing/container schedule, repair and objective; repeated Pack runs report progress, cancellation and exact work/seed manifests without blocking interaction. |
| `think-vhgz` | Search tab over that scheduler. | Best valid poses, rates, status counts, disjoint-block distributions and replay/export agree with headless output; empty or interrupted cohorts are explicit. |
| `think-3yma` | Calibration and held-out presets. | Campaign manifest fixes tuning/held-out partitions before execution; configuration-level distributions and individual best poses are distinguished; replay preserves the partition. |
| `think-wln2` | Final end-to-end acceptance. | Every O1–O7 journey passes, documentation matches the product, required/full checks pass, and the released revision has a live smoke receipt. |

`think-gfqt` starts after Phase 4 readiness and the corrected reporter/registry;
`think-vhgz` follows it, calibration follows Search, and final acceptance follows both
calibration and release verification.
The existing research harness `think-k2fr`, hypothesis work `think-a87q`, and later
sweeps `think-fj07` consume these contracts rather than adding another engine.
Research run authorization and pre-registration remain separate from shipping the
instruments.

The objective always reports absolute side for valid geometry.
Reference-relative metrics require an identified finite reference and a positive
grid-to-reference gap; omit or reject undefined normalization.
State whether feasible but nonstationary runs can rank; invalid and cancelled results
cannot. Terminal-status counts remain separate from validity counts.
Compare completed work over fixed seed blocks, and preserve unsuccessful blocks in
budget-success statistics.

### Legacy Task Reconciliation

`think-a9gt` owns reconciliation, not speculative bulk closure.
It records one of: verified delivered, superseded with a named successor, required
repair in a phase above, or explicitly deferred feature/research work.
A superseded bead is closed as superseded, never as implemented.

| Existing scope | Current owner/disposition |
| --- | --- |
| `think-fk8h` palette and `think-izpq` phase timing | Verify retained implementation; preserve it through data/timeline extraction. |
| `think-vi3v`, `think-gnl7`, closed `think-4cwy` | Preserve parent/adoption changes; strict completion is `think-4ylo`. |
| `think-tmqs` manual behavior gates | Current implementation owner is `think-kpvc`. |
| `think-kbwb` initial seed API | Verify the introduced API; remaining exact mixing and declaration work belongs to `think-dq1l` and `think-gxxc`. |
| `think-gjcl` duplicated collision logic | Consolidation owner is `think-nubm`; preserve any unique regression assertion. |
| `think-x406`, `think-tn0j`, `think-i15w`, `think-ekst`, `think-lmf5`, `think-2c3z` | Inventory live consumers and unique checks in Phase 0; migrate coverage in Phase 3 and retire obsolete code under `think-cqfc`. |
| `think-6wd6`, `think-dpyh`, `think-cz99`, `think-xp8b`, `think-67b5`, `think-4bgm`, `think-hk37`, `think-2m96` | Verify the refreshed UI; required layout/state/metric defects join O2/O6 acceptance, while additional layers or visual options get an explicit disposition. |
| `think-wffa` older Calibrate proposal | Preserve its held-out requirements in `think-3yma`; one Search preset implementation. |
| `think-3quo`, `think-cttv`, `think-0rgh` | Feasible-path experiments, full atlas films, and optional local scientific backends remain separately tracked supporting work; no automatic projection on every paint or backend dependency in the static build. |

## Completion and Review Tracking

The
[review resolution register](../../reviews/review-2026-09-12-workbench-stack-architecture.md#resolution-register)
maps R1–R10 to the tasks above and records their actual repair evidence.
Keep the original finding text as the reviewed baseline; append the source revision,
checks and resulting disposition when it changes.
tbd is authoritative for live task status.
This plan owns required outcomes and ordering, including any decision to defer scope.

Close `think-zisr` only after its implementation children and package acceptance pass.
Close the Pages epic after observed release verification.
Close product delivery only after `think-wln2` verifies O1–O7; completing the narrower
Phase 4 release does not imply Search is delivered.
No unresolved required outcome may survive merely as an unnamed follow-up in prose.

## Risks and Controls

| Risk | Control |
| --- | --- |
| Extraction changes the published picture or timing | Fixed-seed frame comparisons, retained workbench probes, and deterministic capture at each slice |
| A shared kernel erases real differences between Pack and Animate | Share numerical primitives and the step kernel; keep mode-specific adapters and receipts |
| Browser and benchmark results drift | One DOM-free API, browser/Node parity vectors, and one exact seed contract |
| Invalid geometry acquires evidential status | Versioned import validation plus frame-level evidence and provenance checks |
| “Arbitrary n” hides an accidental resource limit | Declare, measure, expose, and test the supported envelope; reject values outside it |
| Cleanup deletes a unique check or reproduction route | Consumer inventory, replacement assertion, and full validation before each deletion slice |

Run the full `packing-validate` tier and the documentation guidelines pass at each phase
boundary. Fast package checks join the pull-request surface as soon as their source is
introduced.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
