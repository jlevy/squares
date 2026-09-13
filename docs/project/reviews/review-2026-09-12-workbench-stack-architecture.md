---
title: Workbench Stack Review and Cleanup Map
description: Review of PRs 125 and 155, with evidence repairs, strict quality gates, and a follow-on standalone package phase
author: Codex with three independent review agents
---
# Workbench Stack Review and Cleanup Map

**Verdict:** Changes required before merge.
Preserve the working browser prototype, rendering toolkit, and research instruments, but
repair the evidence and execution boundaries before promoting them into shared package
APIs.

**Scope:** PR [#155](https://github.com/jlevy/squares/pull/155) at `6e191a35`, stacked
on [#125](https://github.com/jlevy/squares/pull/125). The main baseline is `d507f5c7`.
The current parent head is `0281a508`; the leaf lacks its two latest commits, `ee60689b`
and `0281a508`, and diverges from it at `117d224f`. The local review branch is
`codex/review-workbench-stack`.

**Workflow and tracking:** W10 review-planning-oversight, `think-3kk1`. Three reviewers
used GPT-5.6 Sol at extra-high effort for frontend architecture, physics/benchmark
semantics, and CI/Pages; the coordinator verified findings and integrated the plans.
This phase changes documentation and beads.
Source cleanup, stack integration, experiments, deployment, and the Search tab are
subsequent phases.

The [workbench plan](../specs/active/plan-2026-09-11-workbench-from-spike-to-product.md)
is the governing source for final outcomes and implementation phases.
This review preserves the observed defects and records their resolutions; it does not
maintain an independent roadmap.
`think-m287` tracks the follow-up mapping audit.

## State of the Code

The stack combines atlas expansion, literature intake, numerical experiments,
illustration tools, and a browser application.
Its size alone does not identify which code is expendable.

| Measured at `6e191a35` | Size |
| --- | ---: |
| Stack diff from main | 703 files; 215,405 added and 429 deleted text lines |
| Leaf delta from its common ancestor with #125 | 17 files; 7,365 added and 6 deleted lines |
| Changed literature/archive paths | 301, including 87 binary paths; 122,865 added text lines |
| Tracked files in `packing/devtools/` | 252; 4,871,101 bytes |
| Tracked files in the video spike tree | 218, of which 211 are in v2-transitions |
| `assets/workbench.js` | 7,431 lines |
| v2 generator / main checker / candidate tests | 1,817 / 3,105 / 913 lines |
| Local standalone page build | 4.4 MB, deterministic and self-contained |

The active application lives under
`packing/atlas/known-best/video/spikes/v2-transitions/`. Its location describes its
origin, while its current consumers include site publication, capture, benchmarking, and
direct use.
Moving all of it into the already broad `devtools/` directory would leave the
ownership problem unresolved.

| Area | Keep and develop | Boundary still missing |
| --- | --- | --- |
| Workbench | Pack and Animate, editable poses, force controls, deterministic playback | Separate run configuration, simulation, presentation, and UI state. |
| Python research | Projection, ratchet, basin hopping, structure controls, LP quench | Reusable algorithms are mixed with CLI orchestration in devtools. |
| Rendering | `sqpack.render` models, palette, SVG, rotation, variable container motion | Browser rendering uses a separate implementation; adapters and parity controls are needed. |
| Motion Lab | Typed scenario, pose, evidence, and timeline contracts | Adapt existing semantics into the workbench rather than inventing another frame vocabulary. |
| Strategy/animation schemas | A useful start for data interchange and Python execution | Accepted fields and evidence claims are not fully enforced; browser execution is not implemented. |
| Benchmark | Seeds, numerical checks, repair, reports, CLI runs | The benchmark drives cached animation physics, not a demonstrated shared Pack/Search kernel. |
| GitHub Pages | Existing `/squares/` explainer and workbench build | Project-subpath navigation, declared runtime, and workbench post-deploy checks. |

The raw annealing JSONL blobs have already been removed from the reviewed leaf’s
reachable history. Its retained summary is 99,072 bytes; the largest blob introduced in
the leaf-only history is the 324,582-byte JavaScript source.
A second history cleanup is not justified by the old claim that this PR still carries
185 MB of raw trials.
Source archives and negative research results are not disposable spike code.

## Findings

### R1 — Blocker: imported animation manufactures passing evidence

[animation_from_trace.py](../../../packing/devtools/animation_from_trace.py), lines
148–167, maps `entry.get("feasible", True)` to `NUMERICALLY_CHECKED` and constructs
`CheckSummary(passed=True)` without checking separation or containment.
A schema-valid import with two coincident unit squares at `(0.5, 0.5, 0)` in a side-1
box, repeated at times 0 and 1, exports successfully with `numerically-checked` metadata
and a passing “separating-axis violation at most 1e-9” receipt.

**Fix:** Validate imported geometry and retain the actual check result.
Missing verification remains candidate/illustrative.
Validate record references and provenance at the same boundary.
**Bead:** `think-sdmi`.

### R2 — Blocker: a valid strategy request can silently lose a square

[packing_strategy.py](../../../packing/devtools/packing_strategy.py), lines 116–138,
builds only `round(side)²` grid cells and truncates to `n`, without refusing an
insufficient count. For `n: 5`, a grid phase with
`side: {relative_to: grid, factor: 0.6666666666666666}` returns four squares in a side-2
box. The CLI reports `n=5`, zero violation, and −26.12% excess; the trace labels the
four-square frame feasible.
This is a false packing result from an ordinary schema-valid request.

Related contract mismatches share the same repair boundary: `_structure` loads record
contacts even when `source: random` or `given` is requested; omitted seeds default to
zero despite the schema promising a generated and recorded seed; intermediate container
frames lose their own sides when `run()` applies the final phase side to every frame
(lines 266–282 and 351–359).

**Fix:** Enforce active count and semantic validation at every phase boundary, reject
unsupported options, and carry actual side, seed, parameters, and answer provenance into
the trace. **Bead:** `think-karf`.

### R3 — High: benchmark admission differs between reporting paths

[bench_annealing.py](../../../packing/devtools/bench_annealing.py), lines 422–429,
admits a trial when `not (resolved_overlap > tolerance)`. A NaN therefore passes.
The replay parser supplies NaN for missing resolved fields at lines 621–623. The sweep
at lines 576–596 skips the admission function altogether and ranks every
`resolved_closed` value.

The independent reviewer reproduced both paths: a NaN trial was admitted and reported
with exit zero; an invalid row with overlap 0.5 and score 999 was ranked above a valid
row by `sweep()`. This demonstrates a reporting defect; it does not establish that the
retained resolved summaries contain such rows.

**Fix:** Use one finite, cardinality-aware, pair-and-wall admission rule in run, replay,
report, and sweep. Report rejected trials and refuse empty admitted populations.
**Bead:** `think-1fpa`.

### R4 — Blocker: the leaf’s research record fails the existing gates

The latest hosted
[validation run](https://github.com/jlevy/squares/actions/runs/34705275240) fails on
documentation/provenance and campaign integration.
The new `exp-206` collides with the existing projection experiment.
H-206 through H-211 are absent from the idea index; the new experiments lack numerical
and effort metadata; the ledger and SYNOPSIS disagree with them; an experiment
references unavailable commit `ee27f8e3`. Documentation registration/footer problems are
also present.

The quick behavioral suite reports 4,933 passed, two skipped, and one failure in the
independent SYNOPSIS negative-control check.
The failure is source-related, not a validation time-budget overrun.

**Fix:** Refresh the parent first, repair the collision without renaming the older
experiment, recover accurate provenance, fill metadata from actual evidence, and
regenerate the owning views.
Never invent effort or source fields to satisfy a schema.
**Beads:** `think-5pv0`, then `think-3eha`.

### R5 — Medium: accepted large seeds alias in JavaScript

[workbench.js](../../../packing/atlas/known-best/video/spikes/v2-transitions/assets/workbench.js),
line 4167, multiplies the seed as a JavaScript Number before integer conversion.
`setSeed` accepts the full wrapped unsigned-32-bit range at lines 6437–6442. Seeds
79,049,217 and 29,207,060 produce the same mixed value 3,151,104,992 for base 17 and the
same subsequent random stream.
Recorded campaigns use smaller seed ranges; their contamination has not been
demonstrated.

**Fix:** Define a public seed domain and exact integer mixing, preserve seed-zero
behavior, and test boundary seeds plus browser/headless parity.
**Bead:** `think-dq1l`.

### R6 — High: the compaction negative cannot be reproduced

[exp-209](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-209-h211-the-resolver-is-not-the-ceiling.md),
lines 31–34 and 50–54, says the compaction pass ran inline and was deliberately not
retained. No implementation was found in the reviewed source.
The negative result therefore cannot establish that this class of repair has been
exhausted.

**Fix:** Recover the instrument and controls or annotate the experiment as
unreproducible at its stated scope.
An algorithm can be rejected for adoption while its experimental implementation is
retained for replay.
**Bead:** `think-3hb7`.

### R7 — Medium: the published navigation escapes the project site

[build_workbench_site.py](../../../packing/devtools/build_workbench_site.py), line 67,
injects `href="/"`. From `/squares/workbench/`, this opens the account site’s root, not
the explainer at `/squares/`.

**Fix:** Use a project-relative link and exercise the workbench under the deployed
subpath, including navigation.
**Beads:** `think-5wnw` and existing `think-9x0m`.

### R8 — High: the current checks are below the requested promotion floor

The leaf lacks the parent’s Python spike-floor commit.
Its three browser tsconfigs also disable `noImplicitAny`, `strictNullChecks`,
`noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes` over broad source globs.
The original adoption bead `think-4cwy` is closed, while the strict-flag follow-ups were
left unnamed.

The browser gate runs Biome and TypeScript checks.
It does not run the workbench’s behavioral Playwright checkers; the site builder’s
statement that those checkers run in `packing-validate` is inaccurate.
The main checker passes when run manually.
Passing that manual check does not prevent the next PR from breaking behavior.

The leaf also puts roughly 165 lines of trial/guard JavaScript back inside
`bench_annealing.py` strings (lines 152–317), including geometry and repair logic.
Neither browser lint nor type checking sees that code.
Its new `setSeed`/`seed` API calls are missing from the public declaration, which stays
green because those calls are in strings.
Extract these probes before promoting the API; keep an independently implemented
verifier where it supplies a real cross-check, rather than consolidating away the only
independent check.

**Fix:** Integrate the newer parent and complete the tbd language floors for retained
live code. New package files inherit the strict base with no legacy relaxations.
Retained JavaScript needs checked types and type-aware promise checking; TypeScript also
needs the explicit strict flags and zero-warning lint gate.
Keep Python under Ruff and BasedPyright without a spike-path exemption.
Add small behavioral and configuration negative controls to the existing PR tiers.
Flowmark remains the sole Markdown formatter under this repository’s existing
commit-time policy. **Beads:** `think-4ylo` and `think-kpvc`.

The promotion contract also needs a usable accessibility tree, keyboard operation, and
reduced-motion behavior.
The current template hides the interactive SVG from assistive technology and uses
generic text containers for its labels.
`think-y9pw` owns these repairs and their browser assertions.

### R9 — High: Pages does not declare the Node runtime its builder uses

The
[spike builder](../../../packing/atlas/known-best/video/spikes/v2-transitions/build_candidate.py),
line 1330, calls bare `node` to run KaTeX. The
[Pages workflow](../../../.github/workflows/pages.yml) sets up Python and uv but does
not set up Node.
The Python lockfile’s `nodejs-wheel-binaries` package does not install a
`node` console entry point, so it does not select the executable on PATH. A passing
hosted build therefore depends on the runner image’s ambient Node version.

**Fix:** Pin and explicitly select Node in the Pages build, following the validation
workflow’s existing setup.
Keep the package build and deployment runtime consistent, and check the published
workbench as well as the explainer.
**Beads:** existing `think-l6l4` and `think-9x0m`.

### R10 — High: live optimizer admission can describe a previous state

The follow-up mapping audit found another admission mismatch by source inspection at the
same reviewed revision.
In
[workbench.js](../../../packing/atlas/known-best/video/spikes/v2-transitions/assets/workbench.js),
`optimizeStep` computes contact penetration, changes positions/angles and possibly the
growing square size, then stores that penetration in `o.pen`. `measureOptimizer` (lines
4341–4383) measures the new geometry but uses `o.pen` to admit it as a new best; the
update and call sequence is at lines 4550–4632. The overlap and score therefore need not
refer to the same snapshot.

**Fix:** Validate the exact pose/size/container snapshot returned and retained as best.
Force-step penetration is diagnostic, not admission evidence.
Distinguish a growing sub-unit illustration from a unit-square packing, and geometric
validity from convergence.
Add a step-crossing overlap/rotation/growth regression and a valid control.
This finding has not had a standalone dynamic reproduction in the planning pass.
**Bead:** `think-6hqs`, before shared resolution and the extraction checkpoint.

## Disposition of the Prior Agent’s Notes

The owner supplied a prior-agent handoff on 2026-09-12. Its requested ordering is
retained: repair the record, repair the measurement, add shared resolution, then
consider Search. The following distinctions prevent stale observations becoming new
claims.

| Handoff point | Disposition in the current plans |
| --- | --- |
| Raw overlap had been scored as a packing | Preserve the correction and distinguish unguarded, checked raw, and repaired cohorts. |
| `closed` normalizes against the grid-to-record gap | Keep it beside absolute/relative excess and validity rate; guard the zero-gap case. Different denominators do not explain causality. |
| Best-of-k was a single prefix | Implement disjoint-block distributions, block counts, and uncertainty under `think-4z7d`. |
| Pasted block medians/ranges and exact raw-trial counts | Treat as supplied observations awaiting recovery or exact replay. The Git tree retains summaries, not the raw inputs needed to recalculate them. |
| “n=17 was only run at shake 6” | Incorrect literally: summaries contain five n17/shake-8 inflate cells of 2,000 trials each, all marked unresolved. |
| exp-208’s resolved deep n17 result | Its command and prose claim deeper work, but retained per-cell summaries do not substantiate that resolved deep cohort. Reconcile before accepting or rerunning it. |
| Difficulty increases with n | Replace the broad claim with cell-specific results after reconciliation. n26 clearing the grid does not establish a causal alternative; n29 is also in the set. |
| Median below the grid and no record reached | Keep bounded to the admitted recorded cohorts. These do not rule out untested parameters or methods. |
| Shake 3 suits animation but not measured search tails | Separate presentation defaults from search presets. Do not change Animate’s dial merely to optimize a benchmark. |
| Compaction settles the resolver question | Unsubstantiated until the discarded instrument is recovered; its translation-only scope would still not settle rotating repair. |
| Resolver should give every frame an honest number | Show the score of the geometry actually displayed. Raw and repaired states remain distinct; resolution is an explicit bounded phase/action. |
| Search, Pack, Animate share one engine | Make this an acceptance criterion. The current live and cached simulation paths do not establish that identity. |

The [annealing plan](../specs/active/plan-2026-09-11-annealing-as-a-search.md) owns the
corrections and measurement-gap inventory.
No new benchmark campaign was run for this planning pass.

## Resolution Register

The
[governing workbench plan](../specs/active/plan-2026-09-11-workbench-from-spike-to-product.md)
owns final outcomes and implementation phases.
This register tracks how the reviewed findings are addressed.
All rows below are **open**: mapping is complete, but no source repair is claimed by
this planning pass.

When a repair lands, keep the finding’s baseline text and update its row with the
implementing revision, named check/artifact, and one of: fixed, superseded with
preserved coverage, or explicitly limited with the affected claim withdrawn.
A bead being created or closed without that evidence is not a review resolution.

| Finding | Implementation owner | Governing phase | Required closure evidence | Resolution |
| --- | --- | --- | --- | --- |
| R1 — Imported evidence | `think-sdmi` | 1 | Negative import/export and retained-valid controls; actual validator, tolerance and provenance. | Open |
| R2 — Strategy/count/trace semantics | `think-karf` | 1 | Small-grid rejection/count control, unsupported-field matrix, exact side/time/ID/seed/guidance round trips. | Open |
| R3 — Invalid benchmark admission | `think-1fpa` | 1 | Run/replay/report/sweep reject nonfinite and invalid states; empty-cohort and rejection-count controls. | Open |
| R4 — Record/stack integration | `think-5pv0`, `think-3eha` | 0–1 | Integrated revisions and passing record/provenance/documentation/generated-view checks. | Open |
| R5 — Seed aliases | `think-dq1l` | 1 | Exact mixer/domain, reproduced alias regression and effective-seed browser/headless replay. | Open |
| R6 — Missing compaction instrument | `think-3hb7` | 1 | Recovered committed tool/controls or dated annotation withdrawing the unsupported ceiling claim. | Open |
| R7 — Project-subpath navigation | `think-5wnw`, `think-9x0m`, `think-tn6s` | 2–4 | Served `/squares/` path test, checker negative controls, then a deployed navigation receipt. | Open |
| R8 — Incomplete quality gates | `think-7f3p`, `think-gxxc`, `think-4ylo`, `think-kpvc`, `think-y9pw` | 2 | Checked source/API, strict zero-finding language gates, negative discovery controls, semantic CI and accessibility checks. | Open |
| R9 — Ambient Node runtime | `think-l6l4`, `think-9x0m`, `think-tn6s` | 2–4 | Explicit runtime selection across package/CI/Pages; artifact and deployed revision verification. | Open |
| R10 — Optimizer snapshot mismatch | `think-6hqs`, `think-nals` | 1–2 | Exact returned-pose validation, unit-size semantics, overlap-crossing regression and retained valid-snapshot control. | Open |

Architectural work has explicit owners too: `think-a9gt` inventories consumers before
`think-l9z0` establishes the package foundation; `think-109t` gates broad extraction;
`think-nubm`, `think-w0a1` and `think-ywj4` own kernel/data/timeline; `think-g0lh`
migrates live consumers and `think-cqfc` removes obsolete ones.
`think-uhqw` finishes arbitrary-n Pack; `think-gfqt`, `think-vhgz` and `think-3yma`
deliver experimental Search and calibration.
`think-9sdr` records the clean Pack/Animate merge decision, `think-tn6s` the live
release, and `think-wln2` the final O1–O7 result.
The detailed ordering is maintained only in the plan.

### Standalone package boundary

Use top-level `packages/workbench/`, following the owner’s explicit consolidation
instruction. It is a deliberate change to the repository’s current layout convention.
The package owns all workbench-specific source, tests, probes, build/benchmark/capture
tools, and optional Python adapters.
This location applies to new files introduced during the preceding repair phases too;
existing live files can receive narrow repairs before their migration.
General-purpose `sqpack` libraries remain dependencies.
Update the layout documentation and path-sensitive gates in the same migration; do not
introduce a second workbench source tree under `packing/`.

The
[package boundary](../specs/active/plan-2026-09-11-workbench-from-spike-to-product.md#package-boundary)
owns the proposed source tree: core geometry, simulation, animation, view, app, data,
and public API modules, with package-local tests and probes.

Use one browser/headless simulation implementation and one set of frame contracts.
`Pack` edits a chosen n and runs once; `Search` asks the same run API for many seeds;
`Animate` plays retained or illustrative frames on a deterministic clock.
Calibrate is a future Search preset, not a fourth simulation implementation.

The package imports a versioned catalogue/palette bundle and can start with a generic
packing state without that catalogue.
Python research methods remain in `sqpack` behind explicit adapters, and Rust remains an
optional engine. GitHub Pages receives static build output through the existing site
workflow; it has no Python/Rust service.
The [workbench plan](../specs/active/plan-2026-09-11-workbench-from-spike-to-product.md)
owns the detailed package and strict-floor acceptance checks.

### What to remove, move, or retain

| Material | Disposition |
| --- | --- |
| Active v2 app, styles, templates, and shared browser algorithms | Move into the standalone package with deterministic frame and run-parity checks. |
| Useful geometry, strategy, and trace functions in devtools | General-purpose library functions go to `sqpack`; workbench-specific source and tooling go to `packages/workbench/`. Old-path wrappers are temporary and consumer-backed. |
| Revision-named probes, source-string assertions, duplicate candidate entry points | Audit callers and unique behavioral assertions, replace coverage, then remove under `think-cqfc`. |
| v1 slideshow | Retain until Animate/capture meets its actual consumers; retire overlapping code only after migration. |
| Experimental methods not selected for production | Retain reproducible research tools and negative records in a clearly owned research area. |
| Source papers, raw transcriptions, dated notes, summaries, correction history | Retain. They are evidence, not application clutter. |
| Generated HTML, videos, caches, large raw trial streams | Keep outside Git with reproducible commands or durable artifact references as appropriate. |

Deletion must follow a consumer inventory spanning imports, CLI commands, validation,
capture, Pages, and research reproduction references.
No source file has been declared dead solely because it is large or lives in `spikes/`.

## Validation Evidence and Limits

- Hosted #155 validation is red as described in R4. The
  [Pages build](https://github.com/jlevy/squares/actions/runs/34705275260) passed;
  deployment was skipped because this was a pull request, as intended.
- Local `devtools.build_workbench_site --check` passed on the reviewed source and
  produced the 4.4 MB self-contained page.
  The main workbench checker also passed manually.
  Neither establishes the missing CI integration or a live deployment.
- The coordinator reproduced R1 through the SVG CLI and R2 through the strategy CLI,
  using Python 3.14.7. Independent review reproduced R3 and R5. New source tests and
  repairs are tracked for the implementation phases.
- A full local checkpoint was started at the reviewed source before plan edits, then
  interrupted after more than 30 minutes while research checks were still running.
  It has no completed verdict.
  The document-map schema and generated SYNOPSIS map pass after these edits.
  The documentation checker still reports the existing unmapped annealing-results README
  and eleven missing campaign-document footers, all covered by `think-3eha`. Plan edits
  do not repair those research-record failures.
- The review concentrated on execution boundaries, source organization, experiment
  interpretation, and publishing.
  It did not re-prove archived mathematical claims, rerun the annealing campaign, or
  establish cross-browser numerical equivalence.

Inventory commands are standard Git and text tools: `git diff --shortstat
origin/main...HEAD`, `git diff --numstat`, `git ls-tree -r --long`, and `wc -l` over the
named sources. Fix the revisions above when reproducing the review; moving branch names
are not an immutable baseline.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
