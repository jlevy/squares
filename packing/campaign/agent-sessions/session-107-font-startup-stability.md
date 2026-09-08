---
title: session-107 — prepared math startup and publication integration
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-107
  title: Prepared math startup and publication integration
  date: '2026-09-08'
  started_at: '2026-09-08T15:49:00Z'
  branch: codex/math-startup-stability
  goal: Reserve final inline math geometry before font arrival, preserve the intended faces and interactive behavior, and measure parameter startup under a declared observation regime.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: retrospective
    objective: Build and independently check prepared geometry, explicit hydration, and per-target startup for the published explainer.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: null
    started_at: null
    deadline_at: null
    expected_output: A reproducible prepared page with retained positive and negative controls for delayed fonts, wrapping, input, native fallback, and print.
    validation_command: uv run --frozen --all-extras --group dev python -m devtools.report_math_startup --check
    kill_condition: A visible formula using a pending required face, changed reserved geometry, missing math, or invalid fallback blocks promotion.
    fallback: Retain the failing artifact and repair its specific runtime, preparation, or checker defect before proceeding.
    outcome: The default-profile prepared page passed the registered browser and width geometry checks in exp-003. Exp-002 retains the intermediate WebKit readiness failure. Shared runtime hydration, initial certificate visibility, per-target reveal, and deferred heat-map work were integrated; this result does not certify later saved-setting variants.
    evidence:
    - packing/benchmarks/math-startup/experiments/exp-002-webkit-readiness.md
    - packing/benchmarks/math-startup/experiments/exp-003-prepared-geometry.md
    - packing/devtools/prepare_explainer_math.py
    stop_reason: The initial geometry result and its fault controls were retained; the separate startup comparison required an observer-efficiency review.
    next_action: Audit the latency observer and retain its limitations before making a startup-speed claim.
  - workflow: pipeline-improvement
    focus: efficiency
    recording: retrospective
    objective: Test the startup hypothesis and establish a lower-overhead confirmation protocol with shared publication artifacts.
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: The paired full-page observer met the numerical timing rule but showed differential sampling cost and pre-paint anchor measurements.
    budget_minutes: null
    started_at: null
    deadline_at: null
    expected_output: Retained paired reports, an explicit validity disposition, controlled parameter-only observation, and a preregistered fresh-runner comparison.
    validation_command: uv run --frozen --all-extras --group dev python -m devtools.check_math_startup --mode parameters --self-test
    kill_condition: Excessive observer cost, missing or incorrect readouts, or an uncontrolled measurement regime prevents a latency verdict.
    fallback: Preserve the observations under review and require the separately registered parameter-only regime without changing its acceptance threshold.
    outcome: Exp-004 remains under review despite passing its numerical criterion. H-003 registers twelve interleaved pairs at each width on a dedicated Linux runner, with an explicit sampler-cost bound. The parameter-only mode and its fault controls are implemented, and Pages jobs consume one prepared artifact. No parameter-only result is accepted; the subsequent hosted dispatch belongs to the final integration evidence.
    evidence:
    - packing/benchmarks/math-startup/experiments/exp-004-startup-pairs.md
    - packing/benchmarks/math-startup/hypotheses/H-003-parameter-only.md
    - packing/devtools/check_math_startup.py
    - .github/workflows/pages.yml
    stop_reason: The original observation cannot support an unqualified reader-latency claim; its confirmation moved to the preregistered hosted regime.
    next_action: Complete correctness integration before dispatching the fixed H-003 comparison; retain any invalid result without adding samples.
  - workflow: pipeline-improvement
    focus: correctness
    recording: retrospective
    objective: Integrate current main, retain prepared geometry for every saved font setting, validate the combined publication, and close the authorized release with exact evidence.
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: Main advanced during integration, and independent review found that saved sans or system settings discarded prepared boxes while partial coverage could conceal the omission.
    budget_minutes: null
    started_at: null
    deadline_at: null
    expected_output: A reviewed publication with complete saved-setting coverage, exact-source validation and deployment evidence, retained experiment verdicts, and a measured cost receipt.
    validation_command: DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib UV_PROJECT_ENVIRONMENT=/private/tmp/squares-font-review-py314 PYTHON_CPU_COUNT=4 uv run --frozen --all-extras --group dev packing-validate --push --since 25e66d7b --jobs 2 --inner-jobs 1
    kill_condition: Any unsupported font setting, missing reservation, incorrect first exposure, failed required gate, or stale publication artifact blocks release.
    fallback: Retain the failure and source identity, fix the affected contract, and repeat only checks whose evidence the change invalidates.
    outcome: Candidate preparation and affected validation reached d122d19cffb1b59c86ce57a02838f0c70438e978. The complete hosted Packing checkpoint at 25e66d7b passed all 69 Linux steps and four macOS portability steps. The later affected pre-push replay passed all 45 selected steps and 1188 tests in 137.83 seconds. The first hosted comparison and geometry failures remain exp-005 and exp-006. Pages 34274946315 produced valid H-005 observations that pass the numerical rule at both widths, but its H-004 matrix fails three print settings and lacks eight WebKit cells after an earlier first-exposure failure; exp-007 and exp-008 retain those results. The validation-only integration of newer main is committed as de5013d9a2678c9747e368c3d5944df17d08157d, with 123 focused tests passed. Queue recovery and print carrier repairs are still underway, and H-006 is registered before the next dispatch. No merge or deployed verification is claimed.
    evidence:
    - packing/benchmarks/math-startup/hypotheses/H-004-saved-font-settings.md
    - packing/benchmarks/math-startup/README.md
    - packing/tests/test_prepare_explainer_math.py
    - packing/tests/test_pages_workflow.py
    - packing/benchmarks/math-startup/runs/push-9baa6e08-failed.log.gz
    - packing/benchmarks/math-startup/runs/push-9baa6e08-corrections-passed.log.gz
    - packing/benchmarks/math-startup/experiments/exp-005-hosted-parameter-pairs.md
    - packing/benchmarks/math-startup/experiments/exp-006-hosted-font-geometry.md
    - packing/benchmarks/math-startup/hypotheses/H-005-corrected-hosted-startup.md
    - packing/benchmarks/math-startup/experiments/exp-007-queued-hosted-parameter-pairs.md
    - packing/benchmarks/math-startup/experiments/exp-008-queued-hosted-font-geometry.md
    - packing/benchmarks/math-startup/hypotheses/H-006-queued-recovery-startup.md
    - packing/benchmarks/math-startup/runs/packing-validation-34270139620.tar.gz
    - packing/benchmarks/math-startup/runs/push-final-ui-2026-09-08.json.gz
    stop_reason: 'This record closes the candidate preparation and validation checkpoint through the 20:47:43 UTC cost cutoff. The wider release remains unfinished: repair queue recovery and print carriers, validate the affected source and records, retain the H-006 and H-004 results, merge as authorized, and verify deployment.'
    next_action: Finish the queue recovery and print carrier repairs, run the combined affected checks and preregistered H-006 dispatch, retain every result, then complete the authorized PR merge and deployed verification.
  primary_bead: think-qcmi
  status: stopped
  budget:
    wall_minutes: 240
    checkpoint_minutes: 30
    slice_minutes: 30
  stop_conditions:
  - The requested publication repair is independently reviewed, passes its affected and required checkpoint checks, and is verified on the deployed revision.
  - A failed correctness or measurement guard remains a retained failure or limitation; elapsed target time never substitutes for evidence.
  progress:
    metric: Complete reserved math geometry and correct parameter exposure, with latency assessed separately under the registered protocol.
    before: The deployed 33cd4760 font repair removed the visible face swap, but delayed inline math and initially hidden certificate figures still changed the page flow. The control had no prepared math reservations.
    after: Prepared math reserves individual base geometry in all four saved settings and uses linear font positioning. Runtime hydration waits for actual glyph faces, and queued startup prioritizes parameter labels. Candidate d122d19c passes its affected pre-push replay; the full Packing checkpoint passed at 25e66d7b. Hosted H-005 timing is valid and passes its numerical rule, but print geometry and WebKit first exposure fail, so correctness remains failed. Main integration de5013d9 passes 123 focused tests. Queue recovery and print carrier repairs, combined validation, merge and deployment remain open.
  delegations:
  - task: Prepare Squares math geometry and startup scheduling; integrate variant-aware probes and publication CI
    operator: Codex font_pr_history
    status: completed
    recording: retrospective
    outcome: Added publication preparation without making the pure renderer require a browser, reserved individual KaTeX bases, preserved native fallback and print behavior, and integrated probes that exclude dormant font-profile variants while retaining hidden-certificate coverage. Pages retains the complete geometry matrix and shares the prepared artifact.
    evidence:
    - packing/devtools/prepare_explainer_math.py
    - .github/workflows/pages.yml
    files:
    - packing/devtools/render_explainer.py
    - packing/devtools/templates/explainer-shell.html
    - packing/devtools/check_math_faces.py
    - packing/devtools/check_math_loading.py
    - packing/devtools/check_math_startup.py
    - packing/tests/test_pages_workflow.py
    checks:
    - Final bounded handoff passed 54 workflow, loading and startup tests on Python 3.14.7, with zero Ruff and BasedPyright findings over those probes and tests.
    - Full and parameter-only variant controls passed; the face self-test and one default prepared-page loading, early-input and no-JavaScript check passed. These checks are not the final settings matrix or a timing comparison.
    - The snapshot-cap repair excludes only browser report and fixture directories from private mutation workers. Its eighteen focused cases have passing evidence across the initial run and corrected-cache replay; the unchanged cap retains every registered mutation target and linked dependency.
    - The linear-metric repair passed 53 focused preparation and renderer-font tests with clean Ruff and types. The frozen precision artifact passed all 29 local geometry cells and retained fault controls; the instrument manifest records the optional submitted() guard edit during the matrix, which is a no-op on that older artifact.
    uncertainty: The completed implementation handoff does not certify the final publication. Hosted exp-008 retains three print failures and missing WebKit coverage; subsequent repairs and release validation remain coordinator-owned.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Hand off the frozen files and focused evidence for coordinator integration.
  - task: Correct shared KPress readiness and hydration, then preserve geometry across saved font settings
    operator: Codex kpress_font_pipeline
    status: completed
    recording: retrospective
    outcome: Implemented explicit prepared-DOM hydration and actual single-family glyph-load waits, including the independently reproduced WebKit readiness edge. Integrated preparation and selection for custom/system and serif/sans settings, with complete coverage, variant-selection and duplicate-ID checks.
    evidence:
    - vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md
    - packing/benchmarks/math-startup/hypotheses/H-004-saved-font-settings.md
    files:
    - vendor/kpress/src/kpress/format/static/katex/katex-math-runtime.js
    - packing/devtools/prepare_explainer_math.py
    - packing/devtools/render_explainer.py
    - packing/devtools/templates/explainer-shell.html
    - packing/tests/test_prepare_explainer_math.py
    checks:
    - KPress PR 61 and the architecture follow-up PR 64 are merged with their upstream checks green. The integrated pin is 6e173fac962dba3f5413a0f531cbe9c3147c8947; this does not certify Squares' later combined hosted checks.
    - Representative default, custom-sans mobile and system-sans geometry checks passed, including retained controls; these do not replace H-004's complete hosted matrix.
    - Concurrent release preserves the runtime deadline and prevents serial held-font responses from expiring hydration. The queued startup candidate has a passing bounded Chromium geometry, self-test and host check; its final cross-browser publication remains coordinator-owned.
    uncertainty: Host geometry is tied to the prepared page's bundled fonts, metrics, CSS and rendering options. The later queued-node recovery defect and print carrier repair are ongoing follow-ups to this completed runtime and variant handoff.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Hand off the frozen runtime and preparation contracts for final publication validation.
  - task: Retain startup and loading observations, review print behavior, and preserve strict parameter discovery
    operator: Codex caption_rendering
    status: completed
    recording: retrospective
    outcome: Built the normal startup observer and retained fault controls, adapted prepared-page fallback checks, corrected the optical bullet override, and integrated print checks. Final parameter validation rediscovers targets and separately records its cost, preventing late or reclassified targets from disappearing from the result.
    evidence:
    - packing/devtools/check_math_startup.py
    - packing/tests/test_math_startup.py
    - packing/devtools/check_print_layout.py
    files:
    - packing/devtools/check_math_loading.py
    - packing/devtools/templates/explainer-shell.html
    - packing/tests/test_check_print_layout.py
    checks:
    - Retained startup controls cover missing or incorrect outputs, observer hooks, delayed readiness and late parameter discovery; final full and parameter-only control runs passed in the combined focused handoff.
    - Local review at 9baa6e08 used KPress 6e173fa and Python 3.14.7. The PDF is 17 pages, 822557 bytes and 26 embedded font subsets, with no Type3 or unexpected fonts. All seventeen pages passed visual review; body math, sans captions and square bullets were inspected. The independent reproducibility check reported matching exports at 822463 normalized bytes. Menlo remains the previously recorded host-font limitation. This macOS result does not certify the later hosted print-layout run.
    uncertainty: A requestAnimationFrame observation is a paint opportunity, not a compositor presentation timestamp; absolute anchor movement can include unrelated prose reflow.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Hand off controls and final visual-review evidence without promoting the instrumented timing result.
  outputs:
  - packing/benchmarks/math-startup/README.md
  - packing/benchmarks/math-startup/ledger.md
  - packing/benchmarks/math-startup/experiments/exp-002-webkit-readiness.md
  - packing/benchmarks/math-startup/experiments/exp-003-prepared-geometry.md
  - packing/benchmarks/math-startup/experiments/exp-004-startup-pairs.md
  - packing/benchmarks/math-startup/hypotheses/H-003-parameter-only.md
  - packing/benchmarks/math-startup/hypotheses/H-004-saved-font-settings.md
  - packing/devtools/prepare_explainer_math.py
  - packing/devtools/report_math_startup.py
  - vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md
  - packing/benchmarks/math-startup/runs/push-9baa6e08-failed.log.gz
  - packing/benchmarks/math-startup/runs/push-9baa6e08-corrections-passed.log.gz
  - packing/benchmarks/math-startup/experiments/exp-005-hosted-parameter-pairs.md
  - packing/benchmarks/math-startup/experiments/exp-006-hosted-font-geometry.md
  - packing/benchmarks/math-startup/hypotheses/H-005-corrected-hosted-startup.md
  - packing/benchmarks/math-startup/experiments/exp-007-queued-hosted-parameter-pairs.md
  - packing/benchmarks/math-startup/experiments/exp-008-queued-hosted-font-geometry.md
  - packing/benchmarks/math-startup/hypotheses/H-006-queued-recovery-startup.md
  - packing/campaign/resource-usage/codex-task-tree-session-107.yaml
  checks:
  - The 16:19 UTC boundary records a passing records tier in 32.93 seconds and eleven reporting/publication contract tests in 0.41 seconds. These are prior scoped results, not certification of the final tree.
  - The deployed control, intermediate WebKit failure, default-profile geometry acceptance and full-observer paired reports remain in the dedicated math-startup record with source and observation limits.
  - 'Pages implements all four saved settings at both widths in three browsers, four Chromium print settings, alternate-certificate behavior and retained negative controls. Exp-008 retains the actual partial result: sixteen screen settings and the alternate certificate pass, three print settings fail, and WebKit geometry never starts after a first-exposure failure.'
  - KPress PR 61 and PR 64 merged with their checks green. Squares source 25e66d7b pins 6e173fac962dba3f5413a0f531cbe9c3147c8947.
  - The original pre-push selection at 9baa6e08 completed forty-five steps in 1246.67 seconds. All forty-four static steps passed; the behavioral step reported 4324 passed and two failed tests. The failures were the CSS selector-list guard and the mutation snapshot size cap. The failed receipt is retained at packing/benchmarks/math-startup/runs/push-9baa6e08-failed.log.gz; it is not a passing gate.
  - The corrected pre-push replay used --since 9baa6e08 --jobs 2 --inner-jobs 1 with PYTHON_CPU_COUNT=4 and the isolated normal Python 3.14.7 environment. All forty-five selected steps passed in 145.03 seconds, including 889 reachable behavioral tests in 50.28 seconds. Its receipt is committed at packing/benchmarks/math-startup/runs/push-9baa6e08-corrections-passed.log.gz with the corrections in 25e66d7b. This is scoped pre-push evidence, not a completed fast or full checkpoint.
  - Pages run 34270137119 at 25e66d7b failed correctness; its first hosted H-003 timing comparison is numerically rejected and retained as exp-005, with the partial failed H-004 matrix in exp-006. Packing run 34270139620 passed all 69 Linux steps and four macOS portability steps, with no internal Linux skips; its complete receipts are retained in packing/benchmarks/math-startup/runs/packing-validation-34270139620.tar.gz.
  - The local 9baa6e08 PDF review covers seventeen pages, 822557 file bytes and twenty-six embedded font subsets. Reproducibility and visual review passed on the recorded macOS environment. The browser preview was opened as tab 64618; local review is distinct from verifying a deployed Pages revision.
  - The privacy-reduced recursive Codex receipt covers the declared 2026-09-08T15:49:00Z start through the actual 2026-09-08T20:47:43Z cutoff. It reports snapshot_incomplete true with four live sessions and remains a lower bound through that cutoff. Descendant costs are already included; later release work is not included in this receipt.
  - 'full gate: full at 25e66d7bfe4170a6e2166b95df9ff0f407606629: passed (all 69 Linux steps plus four macOS portability steps; source checkpoint only)'
  - The affected pre-push replay against 25e66d7b passed all 45 selected steps and 1188 tests at the candidate committed as d122d19cffb1b59c86ce57a02838f0c70438e978. Its retained receipt, packing/benchmarks/math-startup/runs/push-final-ui-2026-09-08.json.gz, reports 137.83 seconds wall time and 38.61 seconds for the behavioral tests, with four declared CPUs, two outer jobs and one inner job. Its budget band is reported, not reference-enforced.
  - 'The frozen precision artifact passed 29 local geometry cells: three browsers, two widths, four settings, four Chromium print settings and alternate certificate. Maximum movement was 0.9375px and maximum intrinsic-width error 0.234375px. The optional submission-barrier edit made the local matrix use two guard revisions; the artifact lacks that API. This is geometry evidence for that frozen artifact, not final certification of the subsequent scheduled publication.'
  - Pages 34274946315 has exactly twelve complete alternating H-005 pairs per width, all forty-eight observations valid and all sampler fractions below two percent. The paired changes are -13.50 percent at 1280px and -37.57 percent at 390px, with both 95-percent intervals satisfying the unchanged minus-ten-percent rule. Exp-007 declares correctness failed because exp-008 retains print and WebKit failures. The candidate and control identities, controls and raw observations are retained; no observations are replaced.
  - H-006 was registered at 2026-09-08T20:35:40Z before timing the next repaired candidate, preserving the same exact pair count, widths, parameter-only regime and acceptance rule. Its final dispatch and correctness matrix remain pending at this checkpoint.
  - The validation-only main integration at de5013d9a2678c9747e368c3d5944df17d08157d passed 123 focused tests. The pre-installation records floor passed 31 of 69 named steps in 43.02 seconds; math-startup reporter regeneration and drift checking passed after exp-007 and exp-008 were installed. Final source and record changes still require the coordinator's combined affected pre-push replay; this record does not claim it has run.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-107.yaml
  stop_reason: 'Candidate preparation and validation reached the recorded checkpoint through the 20:47:43 UTC cost cutoff. Session107 stops with the release objective still open: queue recovery and print carrier repairs, combined affected validation, final hosted results, authorized merge and deployed verification remain explicit closeout work. No research priority is changed.'
  next_action: Resume think-mq0d for BC-264's existing 30-minute H114 feature and kernel-contract pricing slice, subject to the current allocation and admission requirements. This publication repair does not reprioritize research or authorize a target run.
---
# Prepared Math Startup and Publication Checkpoint

This owner-directed W7 continuation began at 15:49 UTC on September 8, 2026, under
`think-qcmi`. The [math-startup record](../../benchmarks/math-startup/README.md) owns
its observations, failures and acceptance rules.
The initial four-hour soft target was 19:49 UTC, with intended thirty-minute slices.
Integration, the observer audit and the hosted platform failures carried the work beyond
that target. These three phases remain retrospective; no historical phase deadlines or
completed cycles are reconstructed.
The observed 16:19, 17:01, 18:42 and 19:26 UTC boundaries retain their original meaning.

KPress PRs 61 and 64 are merged, with integrated pin `6e173fa`. The complete Packing
checkpoint passed all 69 Linux steps and four macOS portability steps at `25e66d7b`.
Candidate `d122d19c` has its own passing affected replay: 45 steps, 1188 tests and
137.83 seconds. The later validation-only main integration at `de5013d9` passed 123
focused tests. These results certify their stated sources and selections; final source
and record edits still need the coordinator’s combined affected replay.

The first hosted parameter comparison remains numerically rejected with failed
correctness in
[exp-005](../../benchmarks/math-startup/experiments/exp-005-hosted-parameter-pairs.md),
and its failed partial geometry matrix remains exp-006. The subsequent
[exp-007](../../benchmarks/math-startup/experiments/exp-007-queued-hosted-parameter-pairs.md)
passes H-005’s numerical timing rule at both widths, with valid instrumentation.
The same candidate fails correctness:
[exp-008](../../benchmarks/math-startup/experiments/exp-008-queued-hosted-font-geometry.md)
retains three Chromium print failures, and WebKit’s earlier first-exposure failure
prevents its eight geometry observations.
Both input pages, every available report and the controls remain retained.
The earlier local 29-cell matrix is evidence for its frozen precision artifact, not a
replacement for these hosted failures.

Queue recovery and print carrier repairs are underway.
[H-006](../../benchmarks/math-startup/hypotheses/H-006-queued-recovery-startup.md) was
registered at 20:35:40 UTC before the next dispatch.
Its rule is unchanged; the repaired candidate must establish its own correctness and
timing evidence. The user-level release task continues through the remaining checks,
authorized merge and deployed verification.
As in [Session106](session-106-n26-source-consistency.md), the source preparation and
validation record can reach a terminal checkpoint while those release actions remain
explicit. Both this session and its final phase are stopped, since the wider release
objective is unfinished.

The [recursive resource receipt](../resource-usage/codex-task-tree-session-107.yaml)
uses the actual cutoff 20:47:43 UTC on September 8, 2026. It contains generated,
privacy-reduced totals only.
Four task sessions were live at capture, so the receipt is incomplete and its totals are
lower bounds through that cutoff.
Descendant costs are already included; later release work must not be silently
attributed to this receipt.
Its generated cost block leads the pull request.

The selected research continuation remains `think-mq0d` under BC-264. The synopsis
retains its single canonical selected-entry marker and existing evidence.
This repair creates no mathematical result and does not reprioritize that selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
