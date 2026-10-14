---
title: Predictable CI Feedback and Reusable Checkpoint Evidence
description: Overnight delivery retrospective and a measured implementation plan for ordinary CI within three minutes
author: Codex, independent Astra review and design
date: 2026-10-14
status: draft
---
# Feature: Predictable CI Feedback and Reusable Checkpoint Evidence

**Date:** 2026-10-14

**Status:** Local quick-test selection and this plan are being integrated in
[PR599](https://github.com/jlevy/squares/pull/599). The remaining architecture is a
draft for implementation review.
Investigation and a systematic fix are authorized by the repository owner; no
three-minute feedback result has been established.

**Workflow entry:** `tbd shortcut new-plan-spec`, using `tbd template plan-spec`; W5
efficiency work and the existing validation-efficiency campaign.
**Tracking:** `think-kxmq`; local quick selection is `think-gg64`, and the trajectory
timing follow-up is `think-dat0`. The coordinating agent owns bead updates and PR599
integration.

## Overview

Restore ordinary pull-request feedback to roughly three minutes and stop paying for a
complete checkpoint after each small correction.
Keep fast checks automatic, select expensive checks from their actual inputs, and
require current or demonstrably reusable evidence for every merge obligation.
Expensive tests still run; their cost and selection become explicit.

The immediate problem is larger than a few tests crossing the 12-second CALL limit.
The measured quick workload contains almost 18,000 cases, whole-site browser exercises,
repeated complete registry checks, and real nested process tests.
Rebalancing four shards cannot by itself restore the target.
A second problem is repeated validation: the full dispatcher can serialize fast suites
that already passed elsewhere, while the temporary strict workflow repeats ordinary CI
to obtain browser and coverage guarantees that ordinary CI should supply.
A later PR604 local push exposed a separate problem: broad heuristic selection included
slow tests in the default local loop and ran them serially.
After 700.49 seconds, the reachable test phase had printed only 13% progress and was
explicitly interrupted.

This plan extends the existing
[validation-efficiency plan](plan-2026-09-06-validation-efficiency-and-checkpoints.md),
[measurement campaign](../../../../packing/benchmarks/validation-efficiency/README.md),
and retained validation tools.
It does not introduce another scheduler, evidence framework, or permanent duplicate CI
workflow. The required result is a smaller, correctly selected critical path with
auditable coverage.

## Goals

- Explain the overnight delay using actual run and delivery evidence, separating elapsed
  intervals, observed work, inferred causes, and unknowns.
- Restore the existing ordinary-feedback target: median at most 150 seconds and an
  operational p95 ceiling of 180 seconds, measured from workflow creation through
  required feedback completion, including queueing and setup.
- Preserve every meaningful scientific, behavioral, browser, refusal, custody, and
  publication obligation.
  Skips, missing results, and failed aggregate gates remain visible.
- Make expensive checks automatic when their inputs change and available through
  explicit full checkpoints and the daily backstop.
- Reuse successful unchanged-input evidence without misrepresenting it as fresh
  execution or converting a failed run into a passing one.
- Require every addition to account for its recurring CI cost before that cost becomes
  the next developer’s default wait.
- Diagnose a deadline failure from retained progress and process evidence before
  launching another expensive attempt.
- Make the default local push run the cheap floor and reachable quick behavior.
  Report affected slow obligations separately, with deliberate execution and complete
  coverage required before merge.

## Non-Goals

Scientific bounds, numerical tolerances, publication versions, and test assertions are
outside this change.
The independent atlas-width request has its own branch and review.
This plan does not raise timing ceilings, silently remove tests, declare runner variance
from similar ratios, or treat a manual label as unlimited authorization for a long gate.

The ordinary-feedback target is separate from the duration of an explicitly selected
expensive checkpoint.
A change to a shared mathematical consumer can legitimately require a long checkpoint
before merge; its cost must be stated when selected.

## Background and Retrospective

### Evidence and accounting

The repository retains the compact
[campaign retrospective](../../../../packing/benchmarks/validation-efficiency/retrospective-2026-10-14.json).
The raw API records live outside Git in the maintainer’s closeout archive,
`/Users/levy/wrk/github/squares/.codex/regularization-closeout-evidence-2026-10-13/`:

- `ci-iteration-retrospective-2026-10-14.json`: GitHub metadata and job/step boundaries
  for ten runs and eleven pull requests, plus the actual frontend timing artifact.
- `ci-iteration-latest-38597483408.json`: the subsequent read of the completed strict
  run.

These are read-only API observations, not inferred billed cost.
The same external archive holds the four-shard cost cohorts, JUnit receipts, runtime
checkout bindings and independent reviews A–L; these raw files are not checkout
dependencies.

The table below uses UTC and API workflow start/end intervals.
Those intervals overlap; adding them would not measure user waiting time, billed runner
time, CPU time, or agent effort.
A workflow event’s head SHA is not necessarily its actual checkout: the normal frontend
artifact below identifies a merge checkout different from the event head.
Reuse must verify runtime identity.

Public run links make the observations independently inspectable while bulk logs stay
outside Git. Workflow job metadata remains distinct from the runtime and JUnit evidence
needed to accept a reused result.

### Overnight chronology

| UTC milestone | Observation | Interpretation |
| --- | --- | --- |
| Oct 13, 22:39–22:54 | The site-changelog plan commit preceded creation of [PR590](https://github.com/jlevy/squares/pull/590) at 22:54:16. Feature commits continued at 01:45 and 01:58 on Oct 14. | Work began before the later CI closeout. There is no separately metered implementation interval. |
| Oct 14, 02:57:39–45 | [511](https://github.com/jlevy/squares/pull/511), [530](https://github.com/jlevy/squares/pull/530), [548](https://github.com/jlevy/squares/pull/548), [549](https://github.com/jlevy/squares/pull/549), [559](https://github.com/jlevy/squares/pull/559), and [580](https://github.com/jlevy/squares/pull/580) merged to `aeef99ef`. | The starting handoff covered multiple completed changes, rather than one unfinished PR. |
| 02:57:56–03:23:39 | [Main run 38503790618](https://github.com/jlevy/squares/actions/runs/38503790618) took 25m43s and failed the slow lane. Other workers succeeded; regularized views spent 674s in its command and 709s in its job. | A failed checkpoint with separately useful worker evidence. |
| 06:15:46–06:43:15 | [Deferred run 38521183965](https://github.com/jlevy/squares/actions/runs/38521183965) took 27m29s and concluded success. Regularized views used 652s in its command and 687s in its job; the retained aggregate recorded 687s against a 450s advisory ceiling. | Functional success did not prove the performance budget. Selected-source checkout logs are required alongside the API event SHA. |
| 07:18:57–59 | [585](https://github.com/jlevy/squares/pull/585), [587](https://github.com/jlevy/squares/pull/587), and [591](https://github.com/jlevy/squares/pull/591) merged to `9f48ccc8`. | A separate delivery block before the n=17 follow-up. |
| 06:33–08:35:46 | [PR592](https://github.com/jlevy/squares/pull/592) had reviews on five successive heads and merged at 08:35:46. | Scientific review and conflict resolution were real work. Their duration cannot be inferred from CI duration alone. |
| 10:14:04–10:41:59 | [PR590 deferred checkpoint 38548121070](https://github.com/jlevy/squares/actions/runs/38548121070) took 27m55s; all ten workers and its aggregate passed. | This was final delivery evidence for PR590. Its elapsed interval differs from the gate tool’s own clock. |
| 10:47:29 onward | PR590 merged; [live verification 38552030866](https://github.com/jlevy/squares/actions/runs/38552030866) checked 4,182 published expectations. | The original site change was delivered while the later CI repair remained open. Status reporting should distinguish those facts. |
| About 10:08 onward | The coordinator reports starting the PR599 follow-up before PR590 delivery completed; [PR599](https://github.com/jlevy/squares/pull/599) was created at 10:30:11. | The work overlapped. It is incorrect to add both blocks as consecutive delays. |
| 11:18:06–11:52:32 | [Full run 38555598547](https://github.com/jlevy/squares/actions/runs/38555598547), head `472…`, took 34m26s and failed atlas/schema CALL ceilings. The integration command consumed 1,890s; the other eleven workers succeeded. | This exposed real cost defects, but also paid for broad independent work. |
| 12:38:31–13:29:22 | [Full run 38565361504](https://github.com/jlevy/squares/actions/runs/38565361504), head `e709…`, took 50m51s. Four CALL ceilings failed at 14.13, 13.67, 12.51, and 13.42s. Functional JUnit failures/errors were zero; the integration gate reported 2,866.49s. | The failed result remains failed. Separately successful unchanged-input workers can support scoped evidence reuse. |
| 14:25:34–14:42:21 | [Strict run 38580395126](https://github.com/jlevy/squares/actions/runs/38580395126), head `1c5…`, took 16m47s; one shard reached its 900s deadline, and new receipt/coverage/integrity defects also surfaced. | Building the new enforcement path introduced defects that required correction. The timeout’s cause was not recovered. |
| 14:43:21–14:50:33 | [Strict run 38583046153](https://github.com/jlevy/squares/actions/runs/38583046153), head `54b3…`, took 7m12s. A collection test took 21.78s; A/B also failed old relative baselines. Four complete wall observations were 292.49/325.55/282.04/234.55s. | Valid cost observations from a failed gate; they are not passing performance proof. |
| 15:12:50–15:29:31 | [Strict run 38587347972](https://github.com/jlevy/squares/actions/runs/38587347972), head `fecca…`, took 16m41s, failed three CALL ceilings, and lost shard D at 900s. | The second unrecovered deadline justified progress journals. Journaling itself did not fix its unknown cause. |
| 16:00:28–16:08:46 | [Strict run 38594336170](https://github.com/jlevy/squares/actions/runs/38594336170), head `58b6…`, took 8m18s. A failed a 14.45s pool CALL and its 335s wall ceiling at 339.70s; B used 384.18s against 360s. C/D passed at 289.65/231.76s. | Repacking and individual optimizations had not restored the ordinary target. |
| 16:00:32–16:09:12 | [Normal run 38594344872](https://github.com/jlevy/squares/actions/runs/38594344872) concluded success after 8m40s. Its frontend job took 505s, including a 427s gate. | Normal success was neither a three-minute result nor proof of the strict browser workload. |
| 16:22:08–16:30:56 | [Strict run 38597483408](https://github.com/jlevy/squares/actions/runs/38597483408), head `08d23c06…`, took 8m48s and failed A/B/C. D and the negative-control job succeeded. The coordinator’s detailed log audit reports four further marginal CALL failures and A/B/C whole-wall failures. | Another isolated correction and repack had not stabilized the workload. This result prompted the batch diagnosis instead of another blind full replay. |

The coordinator reports roughly 65 minutes for the final PR590 continuation and roughly
25 minutes of publication observation, but these are overlapping workflow-level
observations, not agent-time accounting.
Review, analysis, token usage, billed hours, and time specifically lost to storage were
not separately metered.
The external scratch volume was full, preventing heavy local reproduction; its exact
contribution to elapsed delay is unknown.

The initial handoff’s claim that an approximately uniform 1.35 ratio established machine
variance is unsupported.
Similar ratios can arise from host effects, workload changes, shared setup, or
measurement boundaries.
The handoff also mentioned a 647s regularized-views observation; the retained run above
has a distinct 687s job/aggregate observation.
Preserve each with its boundary rather than reconcile them by assumption.

### What prolonged the work

| Finding | Evidence and effect | Correction |
| --- | --- | --- |
| Default work grew beyond its architectural budget. | The measured `58b6…` quick cohort contains 17,903 cases in 765 measured modules; the inventory contains 788 modules. Existing historical shard assignments and timing records no longer described that workload. | Admit new default work by inclusive recurring cost, measure the actual assignment, and optimize or explicitly select expensive integration work. |
| Ordinary and strict browser workloads differed. | On head `54b3…`, both collected 17,891 identities. Normal CI skipped 257, strict CI 47: 210 additional Chromium-dependent cases passed only in the strict cohort. | Put required browser capability and skip refusal into ordinary CI. Green must mean the declared workload executed. |
| Successive broad checkpoints followed individual failures. | Two full PR599 runs paid 34m26s and 50m51s before the whole quick cost surface and its assignment were addressed together. | Freeze a batch scope, profile the complete expensive tail, and run focused equivalence checks before one new checkpoint. |
| Full dispatch repeated fast integration work. | The full integration topology can run four quick suites serially; the observed `e709…` integration command spent 2,869s while eleven independent workers succeeded. Existing merge-tree reuse applies more narrowly than all checkpoint entry points. | Consume trustworthy existing fast partition evidence and run only invalidated obligations. Preserve a deliberate cold full mode. |
| New enforcement infrastructure had correctness bugs. | Review H found physical collection/JUnit identity mismatches, including parameter `::` handling, and a decimal-corner parsing defect. Review I confirmed their corrections. | Review collector and receipt semantics independently; use pytest’s actual identities and refusal controls before relying on a new gate. |
| CALL-only diagnosis missed inclusive cost. | An eager fixture initially hid atlas production from a CALL timer. Browser state and page-generation work also appears in expensive setup phases. | Measure setup/call/teardown and subprocess work; preserve real state isolation while removing duplication. |
| A deadline gave insufficient diagnosis. | The `1c5…` A and `fecca…` D timeouts lacked a complete cost report or a recoverable last executing node. | Flush lifecycle events and retain worker/process diagnostics before the deadline. Do not infer a cause or retry blindly. |
| Coordination became part of the delay. | The coordinator reports one-failure-at-a-time diagnosis, frequent long analysis, repeated manual evidence updates, and gate coordination. Those intervals were not metered. | Keep one generated evidence index, carry prior review coverage across deltas, and report delivered product separately from remaining certification work. |

Reviews also prevented regressions: the lazy-fixture finding, collector identity fixes,
and decimal parser correction were substantive.
The lesson is to preserve independent review while reducing redundant replay and manual
narration, not to label every review as waste.

### Where the current time goes

The four complete `58b6…` reports contain 4,388.119 seconds of summed pytest phase time.
Four four-core jobs each launch four xdist workers: `outer jobs = 1` and
`inner jobs = 1` do **not** mean one pytest worker.
Inner jobs constrain nested production pools.
Dividing the measured phase total by sixteen worker slots gives an idealized 274.26
seconds before setup and scheduling overhead.
This is occupied phase time, not CPU accounting or a prediction for the next revision;
it nevertheless rules out a 180-second solution based only on repartitioning the
unchanged observed workload.

The top five modules account for 19.5% of that phase time, the top twenty for 44.3%, and
the top eighty for 73.2%. The largest include `test_results_register.py` (270.60s),
`test_site_glyphs.py` (226.82s), `test_overview.py` (128.13s),
`test_confirm_gupta_records.py` (122.34s), and `test_site_head.py` (108.77s). These are
module totals across many cases, not individual CALL failures.
Optimize shared work before deciding that all cases in an expensive module belong in a
deeper lane.

In the normal run’s actual frontend artifact, the site-table-layout step took 425.06s,
the workbench browser step 182.49s, the browser floor 112.76s, and its liveness checks
42.76s. These steps overlap and must not be added as wall time.
The layout execution reported 418 passes and six skips, followed by four serial timing
checks. Recorded setup phases included 109.25s for the homepage keyboard fixture and
99.63s for the atlas-address fixture.
Source inspection shows that these fixtures perform real browser-state sequences; the
phase names alone do not prove that all their time is duplicate rendering.

The strict `58b6…` shards spent 68–93s before their gate steps.
Full-history checkout took 33–45s in those jobs.
Successful C/D shards then spent roughly 37–41s on fresh receipt collection.
These are distinct optimization opportunities.
Eliminating repeated collection and unnecessary setup is useful, but cannot account for
the whole workload excess.

### PR604 local push: broad selection included slow tests

The later `packing-validate --push` observation is retained under
`local_push_observations` in
[the existing retrospective record](../../../../packing/benchmarks/validation-efficiency/retrospective-2026-10-14.json).
Its command, progress log, native sample and disposition remain in the local closeout
archive as `news604-live-pytest-command.txt`, `news604-correctedgate.log`,
`news604-live-pytest-sample.txt` and `news604-canonical-gate-disposition.json`. This is
local macOS evidence, separate from the hosted CI cohorts above.

| Measurement | Observed result |
| --- | --- |
| Selection | 608 of 791 test files, including 584 under `packing/tests` and 24 under `packages/workbench/tests`. |
| Execution | One pytest process, without xdist. The normal lane used `not exhaustive_exact and not pool_heavy`, which includes slow tests. The pool-heavy phase did not start. |
| Duration and outcome | Explicit SIGINT after 700.49s in the reachable phase; 743.74s for the dispatcher. Last printed progress was 13%. Final result counts are unavailable. The dispatcher exited 1. |
| Other checks | 67 prerequisites completed: 66 passed; the release-impact check failed because a no-public-change declaration included seven inputs unchanged from the baseline. A later focused repair passed 18 tests in 8.19s. |
| Process evidence | The macOS native sample shows active `gmpy2` rational arithmetic. Python stack attachment was denied, so the precise active test is unknown. |
| Limits | The interruption preceded the configured 900s step ceiling. Observed free scratch space stayed above the 150 MiB pause floor; no internal-storage fallback was used. |

This exposed excessive default work in the local pre-push heuristic.
Conservative import closure and repository-walker/dynamic-import selection can produce a
broad selection; the retained command does not break the 608 files down by selection
reason. It selected less than the full 791-file inventory, so this observation does not
prove that the whole-suite fallback fired or quantify false-positive selection.
The run measures serial execution of a broad selection that retained slow behavior; its
incomplete output does not attribute elapsed time between quick and slow cases.
Active arithmetic rules out describing the sampled interval as a collection hang; it
does not identify every expensive test or explain the hosted 900s failures.

The 66 prerequisite passes and the later 18-test release-impact repair are useful scoped
evidence. Neither completes the interrupted behavioral phase or turns the canonical push
gate green. No full-suite duration can be inferred from 13% progress.
The fix belongs in local selection and workload placement, with conservative coverage
preserved; it is not a hosted CI regression claim, a 900s bypass or a reason to raise
the ceiling.

### PR604 trajectory timing follow-up

`think-dat0` tracks the Workbench trajectory failure in
[run 38630350596, attempt 1](https://github.com/jlevy/squares/actions/runs/38630350596/attempts/1):
the step into 324 using `bodies` took 412.2ms against the strict 400ms limit; its
1,807,280 retained array bytes passed the 4MB limit.
The timer surrounds synchronous trajectory construction, and cache hits report the
original construction time.
It excludes page build and browser startup, but the checker does not identify the
original build instant or establish a cold/warm boundary.
Three site workers can overlap two Workbench browser owners on the documented four-CPU
runner. This permits contention; it does not prove the cause of the failed sample.

The follow-up should retain all six samples and their configuration on success and
failure, then enforce the same limits in a short phase with exclusive browser resource
ownership. Keep all functional checks in automatic CI, and test failure propagation and
non-overlap. Do not retry samples, take a minimum, or substitute cache-lookup time.
The bounded diagnosis is retained as `pr599-integration/think-dat0-trajectory-timing.md`
in the external archive above.
This is remaining measurement work, not a production scheduler change in PR599 or a
measured improvement.

## Current Stabilization Batch

News and Explanations are delivered: PR604 merged as `16ea3bd06`, and its main
deployment passed 4,243 live expectations.
The remaining work here is CI stabilization, not an unpublished News feature.
PR602 subsequently merged as `9b32da04d`, adding 24 results and the reviewed intake
material. PR599 preserves that main’s publication history and pins, keeps its three
complete-module cost admissions, and reserves the site-only successor v0.7.2 for the
public guide and bundled code-font correction.

The `77152fb83` hosted cohort exposed three ordinary-suite failures: a non-tier CLI flag
was not classified, and two release-generator format checks failed.
The strict cohort also found that literal `ℝ` in site code fell back outside the bundled
font. Focused repairs retain the existing thresholds and glyph refusal controls.
They require the final combined source gate; an earlier isolated pass is not that gate.

The measured optimization candidates are kept separate:

| Candidate | Evidence and disposition |
| --- | --- |
| VE007: one Gupta fact admission per plan | The thin-driver arithmetic reduction was 11.97%, below the declared 15%. The receipts also lack the complete CLI provenance. Rejected and withdrawn. |
| VE010: Gupta plan plus fixture batching | The thin-driver cohort showed 20.60%, but a separate full-provenance CLI cohort had overlapping ranges despite six functional passes. The generated report rejects it. Both interpreter cohorts and the slow candidate observation remain; all three routine source files are restored. |
| VE008: one paper visit for two probes | The full actual oracle refused one figure field, 0.371 versus 0.372, after 130.667s. All 68 credit rows and the other 62-figure fields matched. No timing samples ran. The routine optimization is withdrawn; source, driver, reports and the earlier bootstrap failures are retained. |
| VE009: one complete test publication | Withdrawn on design and maintenance grounds. Both fresh 184-result oracles passed all 470 checks; single inclusive observations were 110.380s local and 149.098s shared, including a 91.151s serial controller barrier. Direct producers remain fresh, actual consumers split across two shards, and roughly 500 transport/lifecycle lines have no established benefit. Zero paired samples; no numerical screen verdict or CI opt-in. Source and all oracles are retained. |
| VE011: guarded native receipt copies | Rejected and withdrawn. The separate native oracle and all six paired observations passed; inclusive control/candidate medians were 39.1359s/37.6866s, a 3.70% reduction with overlapping ranges. All native receipts and source variants are retained, including the 62.6207s candidate. The test helper and five copy controls are restored to the pre-experiment implementation. |

The
[existing campaign report](../../../../packing/benchmarks/validation-efficiency/report.md)
uses original full-provenance receipts and JUnit.
Thin-driver and standalone-oracle observations remain separately identified.
Exact multi-node/module targets use the existing experiment contract’s new list form;
every command token and complete JUnit identity set must match.
This is a representation correction, not a changed criterion.

The retained nine-house profile is diagnostic only and receives no gate credit.
Rejected hypotheses do not justify retrying, deleting a field, moving fixture work
outside the timer, changing markers or raising a ceiling.
The three-minute objective remains unproved.

The next producer-profile slice is tracked as `think-xoiw`. It follows stabilization
rather than expanding this branch and will inspect repetition within the existing
producer boundary before proposing any implementation.

## Design

### One coverage plan, existing execution surfaces

Extend the existing validation plan to produce an executable list of obligations with a
reason and cost estimate.
Each obligation ends in one of four explicit states: executed successfully, reused from
accepted evidence, failed, or unresolved.
A required aggregate succeeds only when all required obligations are discharged.
Missing or unexpectedly skipped work is unresolved.

Use the existing stable required context and workflow aggregation.
Do not add another permanent whole-suite workflow.
Fold the useful browser-capability, exact collection, and receipt guarantees from
`enforced-quick.yml` into ordinary validation, then retire its duplicate execution after
equivalent coverage is demonstrated.

| Surface | Selection | Evidence and budget |
| --- | --- | --- |
| Local edit and push | Existing cheap floor plus reachable quick behavior; unknown dependencies expand quick selection and retain all affected deeper obligations. | Print selection reasons, actual workers and deferred obligations. Local quick success is not complete merge evidence. |
| Ordinary PR feedback | All genuinely fast checks, cheap scientific/refusal contracts, required browser smoke coverage, and inexpensive affected behavior. | Existing 150s target and 180s operational ceiling; total workflow critical path includes setup. |
| Affected expensive checks | Automatically selected when a declared consumer, input, fixture, toolchain, policy, or relevant test changes. | Explicit obligations with measured per-step ceilings; run beside ordinary feedback and block merge when required. |
| Explicit checkpoint | Complete unresolved obligations, or a deliberately requested cold full run. | Print selected work and expected cost before launch. Evidence reuse is labeled. |
| Scheduled backstop | Daily complete independent execution, including expensive controls and browser coverage. | Detect missing dependency contracts and timing drift. It does not replace current affected pre-merge proof. |

This makes the existing rule “refresh invalidated checkpoint evidence” executable.
It requires a policy clarification in `development.md`: a final checkpoint may be a
verified union of successful current and unchanged-input results.
It is not automatically a new invocation of every producer.
OR-13 still requires every fast check on the automatic surface; expense alone does not
authorize deferral. OR-17 requires explicit cost and selection for long work.

Measure placement at the real executable assurance boundary, including shared production
and setup. A hundred inexpensive assertions over a costly browser-state sequence are one
expensive integration obligation with many observations; they are not a reason to
discard the observations or move unrelated cheap tests from the same module.
Keep separable cheap contracts automatic and retain the complete measured integration
obligation in its selected lane.
Deferral needs evidence that the required work remains expensive after reasonable
duplication removal, not merely a large module total.

### Keep the default local push bounded

The PR599 implementation runs the reachable subset of `QUICK_TESTS`
(`not exhaustive_exact and not slow`) alongside the existing cheap checks.
`packing-validate --push --include-reachable-slow` explicitly includes selected slow
tests. The standalone selector supports `--lane quick`, `--lane slow` and `--lane all`,
with quick as the default.
The normal/pool-heavy split remains within each selected lane; progress receipts carry
the lane, actual marker and excluded categories.

This local default is implemented; the broader obligation planner and evidence reuse
below remain proposed.
Every quick test still runs automatically in CI. No speedup or three-minute result is
established: excluding slow tests alone cannot make an oversized quick workload cheap.

Plan reachable slow tests as separate obligations.
Execute them through a deliberately selected local deeper run or the required affected
CI lane, with the reason, expected cost, actual worker topology and coverage destination
printed before execution.
A slow marker alone never discharges an obligation.
Required affected slow tests must execute or qualify for accepted evidence reuse before
merge; unexecuted work remains unresolved, even if the local quick run passes.
Keep exhaustive coverage in its existing checkpoint contract.

Preserve conservative selection for unknown inputs, parse failures, dynamic imports,
repository walkers and global harness changes.
Broaden both quick selection and the set of deeper obligations when dependency knowledge
is incomplete; never reinterpret an unknown path as unrelated.
Record each selection reason so the next broad selection can be diagnosed.
Narrow a fallback only after an explicit input contract and mutation controls prove
coverage. Do not raise time ceilings or suppress failed or incomplete results to
accommodate the current behavior.

### Input contracts and trustworthy reuse

Begin at step or test-module granularity.
Reuse is allowed only for a reviewed dependency contract covering:

- Production consumers and their transitive code imports.
- Input files, directory/glob membership, and added, removed, or renamed entries.
- Test code, fixtures, helpers, selection rules, runtime capabilities, and expected
  collection identities.
- Dependency locks, interpreter/tool versions, environment settings that affect
  behavior, and relevant workflow/policy code.

Existing `reachable_tests.py` is explicitly a pre-push heuristic.
Its import graph and conservative fallback are useful inputs, but it cannot simply
become the authoritative CI selector.
Dynamic imports, unowned paths, parsing failure, or unknown input effects select the
whole affected family.
Global selection/harness changes select all families.
Start with a bounded, well-understood family and widen only after mutation tests prove
invalidation.

Extend `verified_merge_tree.py` and the current receipt checker rather than create a
second evidence service.
Accepted evidence must identify the trusted same-repository workflow, actual runtime
checkout and source/base relationship, declared inputs, selected and observed node
identities, toolchain/capabilities, and complete outcomes.
Failed or expired artifacts, unknown schemas, missing nodes, unexpected skips, or
untrusted provenance are refused.
Use Git for repository identity and diffs; do not hardcode source commit/blob identities
as correctness criteria or invent source checksum registries.

A successful worker within a failed aggregate may remain valid semantic evidence if its
actual inputs, harness, and outcome are independently verified.
The failed aggregate remains failed.
A complete pytest report from a performance-failed run may supply a cost observation; it
is not passing gate evidence.
Assignment or concurrency changes invalidate wall comparability even if they do not
invalidate scientific results.

The 174 registered negative-control boundaries follow the same consumer/input rules.
Changed controls must run on the current revision; changed harness semantics require the
complete control surface.
An unknown command dependency selects its complete control family.
The ten schema controls used during PR599 are a scoped historical selection, not a
permanent generic substitute for all controls.

### Restore browser coverage without duplicate fan-out

Ordinary CI must assign every required browser case to a job with the pinned Chromium
and Node environment, or fail for missing capability.
The observed 210 extra normal skips must disappear as unexplained omissions.
The remaining known optional omissions stay enumerated as omissions, with reason and
owner; they are never counted as passes.

Use collected metadata/capabilities and the maintained family inventory to place tests,
rather than hardcode a list of 210 historical identities.
New browser tests must either acquire a valid placement automatically or fail the
coverage contract. Keep cheap real browser smoke checks automatic; select measured
expensive navigation/layout matrices by their actual shared CSS, JavaScript, page
producer, assets, and data inputs.
Shared browser source can legitimately invalidate a whole family.

Record the canonical collection during the pytest execution already being performed.
The xdist controller can compare worker collections and write physical source paths plus
pytest’s own JUnit identity mapping.
Compare planned and observed results without a second complete collection per shard.
Preserve refusal tests for duplicate/missing nodes, class names, parameter text
containing `::`, mismatched roots, worker collection failure, and interrupted runs.
Benchmark this instrumentation’s overhead too.

### Remove repeated work before moving it

Use the existing experiment campaign for bounded component comparisons.
Register each hypothesis, preserve all assertions and real boundary behavior, and
validate outputs before comparing cost.
Use at least three alternating control/candidate observations for an exploratory result;
report median and range.
Do not call that a confirmed speedup.
A stronger statistical claim needs the campaign’s confirmatory design.
Failed attempts and contrary samples remain in the record; cold/warm or
different-capability regimes stay separate.

Initial hypotheses, not established optimizations:

1. **Page and browser fixtures:** profile producer generation, browser startup,
   navigation, state changes, and waits within the 425s layout step.
   `site_renders.py` already caches within each worker, so another local cache may
   accomplish nothing. Build immutable producer output once per actual input set where
   safe, then give mutation cases private copies and browser cases fresh required state.
   Preserve genuine resize, startup, keyboard, and sequencing checks.
2. **Repeated complete registry setup:** measure immutable fixture preparation in
   results-register and Gupta-record tests.
   Share validated immutable templates only where each mutation still obtains an
   isolated mutable copy and executes the real consumer/refusal path.
   Keep custody, atomic-write, and malformed-input behavior.
3. **Recursive collection and CLI imports:** measure fresh-interpreter import cost and
   actual nested pytest startup separately from the tested operation.
   Avoid loading unrelated application modules or plugins where their absence is part of
   a proved equivalent execution.
   Do not replace the real fresh process or worker failure with a mock.
4. **Topology and receipts:** remove redundant fresh collection, reuse valid parallel
   fast partition evidence in checkpoint entry points, and retain full history only
   where the job’s provenance contract requires it.
   Keep pinned tool versions and validate cache keys; measure checkout and installation
   separately before proposing new runner infrastructure.
5. **Within-shard scheduling:** the installed xdist loadfile scheduler inherits
   loadscope’s default ordering by number of cases, rather than measured file cost.
   Test deterministic cost-first collection order with the existing
   `--no-loadscope-reorder` option before introducing a custom scheduler.
   Keep each file together and retain inherited crash/requeue behavior.
   Its refill threshold is two pending cases: large first files do not universally
   receive a second file at startup, despite the scheduler’s general prefill comment.
   Verify complete identical worker collections, exact normal execution coverage,
   deterministic unknown-cost placement, crashes, and requeues.
   Compare tail utilization and total allocated cost; do not claim improvement from a
   scheduling simulation alone.

The coordinator’s subsequent read-only `cProfile` run supplies one concrete candidate: a
successful full schema audit reread 963 datasets to print their declared schema names
after substantive validation had already loaded their metadata.
Its instrumented run reported 2,609 YAML loads and 23.155s total; these are profiled
observations, not a baseline suitable for a speedup claim.
Retaining first-pass metadata may remove duplicate work while preserving diagnostic
order and output. The malformed-input regression returns before that success-only
reporting path, so this candidate cannot by itself explain or fix that failing control.
Review and measure both paths.

Treat setup/call/teardown and subprocess cost as part of the test’s inclusive cost.
Moving work into a fixture to escape a CALL ceiling is not an optimization.
Retain the current CALL limits while adding inclusive measurements to placement and
regression decisions.

### Immediate stabilization bridge

The latest
[strict run 38597483408](https://github.com/jlevy/squares/actions/runs/38597483408),
head `08d23c06…`, completed with three further A-shard CALL failures: malformed coverage
through the full schema gate (12.90s), deterministic audit output across two fresh CLI
processes (12.31s), and actual xdist worker-collection failure followed by serial
collection (12.27s). The coordinator’s log audit also reports C’s split-grid/repeat/gap
audit at 12.12s. A/B/C whole walls were 358.85/426.04/420.36s against 335/360/360s.
These are reported failures, not evidence that the checks are inherently slow.
The preceding pool correction did not produce another CALL failure in A; D and the
negative-control job succeeded.

Batch-profile these controls and the rest of the measured expensive tail before making
another assignment change.
Preserve the full schema mutation, two fresh interpreters, actual worker failure, serial
fallback, split-grid/repeat/gap decisions, and adjacent cheap unit/refusal controls.
If a bounded optimization cannot make a genuinely expensive integration control reliably
quick, give that exact measured control a documented deeper placement and retain its
complete assertions.

Initially run any newly deferred small group on every PR in an existing suitable job; do
not invent a special PR599 exemption.
Before narrowing it to affected-input selection, implement and test its input contract.
Fresh collection and JUnit must prove that every newly or changed deferred node actually
ran, including both outcomes of the worker-failure parameter group.
A new slow marker alone cannot discharge coverage.

A focused current-head deeper execution can prove these controls without a thirty-minute
full replay. It cannot repair the failed strict run’s verdict or discharge a whole-shard
wall failure. The batch change still needs fresh ordinary/default evidence and any other
invalidated obligations.
Moving four marginal cases will not solve the measured 18,000-case architecture by
itself.

### Cost admission and timeout policy

Every added or expanded test family declares its expected invocation frequency, measured
inclusive cost, runner shape, input owner, and intended placement.
The report estimates recurring allocated runner time and critical-path impact
separately. Unknown cost is a measurement obligation, never permission to omit the new
test. Reuse hit rate can reduce a forecast only after it is observed.

As an initial review trigger, an addition exceeding two seconds of estimated default
critical path or five percent of its family’s measured cost requires an explicit
cost/placement decision.
These are review triggers, not automatic test-removal thresholds.
The whole 180-second budget remains the final constraint.
A case crossing a CALL threshold receives an inclusive-cost diagnosis; a new timing
baseline cannot be chosen merely because it makes the result pass.
The existing campaign’s allocation guard also applies to scheduler experiments: report
increased runner allocation instead of presenting wall reduction alone as efficiency.

Extend the retained flushed lifecycle journal to expensive pytest surfaces that
currently lose the last active phase.
Include worker/process identity and bounded diagnostic snapshots or stack dumps before
terminating. Reports distinguish setup pending, CALL pending, teardown pending, failed
setup, truncated evidence, and completed outcomes.
Missing completion is never inferred success.
Keep the current deadline unless measured required work supports a reviewed change; the
two 900-second failures remain unexplained until evidence establishes their cause.

Do not automatically retry functional, coverage, or performance failures.
A documented infrastructure failure can justify one separately recorded retry; keep the
original receipt. Before long local work, check the required external scratch volume and
space. If unavailable, use a focused hosted reproduction rather than silently falling
back to internal storage or launching a whole checkpoint.

## Implementation Plan

### Phase 1: Account for the current workload and remove measured duplication

The coordinator creates small child beads under `think-kxmq`, links the existing
browser-capability, timeout, and storage work, and gives each implementation owner a
disjoint write set. This plan, the compact campaign record and the local quick-test
selector are now being integrated in PR599. The remaining architecture and measured
performance work stay separate implementation slices; integration does not mark them
complete. The atlas-width delivery retains its own product and review record.

| Slice | Owned files and responsibility | Reviewable completion |
| --- | --- | --- |
| Retrospective and cost report | Existing `packing/benchmarks/validation_timing.py` and validation-efficiency campaign results; generated report from retained run/job/artifact data. | Reproduce this timeline and cost attribution; distinguish unavailable measurements and failed gate observations. |
| Execution and collection receipts | `packing/devtools/suite_files.py`, `check_enforced_quick.py`, and their tests. | One actual collection supplies canonical identities, outcomes, lifecycle progress, and capability omissions; malformed/interrupted evidence fails closed. |
| Browser workload | `packing/tests/site_renders.py` and explicitly assigned homepage/atlas/layout fixture modules. | Component profiles and one measured equivalence-preserving improvement; no weakened state transitions, assertions, or timing semantics. |
| Python integration workload | Explicitly assigned registry/Gupta/CLI fixture and consumer modules. | Batch disposition of expensive controls, measured setup/import reductions where feasible, and exact current execution of any deeper controls. |

Do not let multiple workers edit the central workflow or validation planner
concurrently. Independent review checks semantic equivalence, source/data ownership,
evidence refusal behavior, and whether cost moved rather than disappeared.
Run focused component experiments beside delivery; avoid a full checkpoint for each
local hypothesis.

### Phase 2: Enforce selection, reuse, and the ordinary budget

One owner integrates planner and workflow changes after the component interfaces are
agreed.

| Component | Existing implementation to extend | Required behavior |
| --- | --- | --- |
| Obligation plan and local push | `packing/src/sqpack/cli/validate.py`, `packing/devtools/reachable_tests.py` and their existing tests | Default local cheap floor plus reachable quick behavior; explicit affected slow obligations, selection reasons and worker counts; conservative unknown-input expansion; no unresolved merge obligations hidden by local success. |
| Evidence acceptance | `packing/devtools/verified_merge_tree.py` and the current receipt checker | Runtime checkout and capability verification, changed-test invalidation, trusted artifact custody, and separate semantic/cost evidence. |
| Negative controls | Existing control registry and runner | Derive affected control families from actual consumers; select all on unknown dependencies or global harness changes. |
| CI integration | `.github/workflows/packing-validation.yml`, `deep-gate.yml`, and `enforced-quick.yml` | Ordinary browser coverage, one stable aggregate, selected expensive work, explicit checkpoint cost, removal of duplicate fan-out when safe. |
| Publication | Existing Pages scope/producer graph and workflow | Reuse its established input contracts where valid; retain actual produced-asset checks and published-site verification. |
| Policy and budgets | `development.md`, `operating-rules.md`, budget declarations, and existing wall-report tools | One documented tier model, inclusive cost admission, unchanged ceiling history, and executable evidence-union checkpoint semantics. |

Run the proposed merge-obligation selector in shadow mode first, comparing its coverage
with actual execution.
The implemented local quick selector does not provide that reuse guarantee.
Introduce reuse for one bounded family with complete invalidation controls.
Expand only when unknown-input fallback and output equivalence are demonstrated.
Planner failure selects conservative execution or fails the aggregate; it never creates
a green empty plan.

## Testing Strategy and Acceptance

- Reproduce cost summaries from retained raw reports without editing their verdicts,
  assignment history, or measurement boundaries.
  Keep unmeasured modules visible.
- Mutation-test input contracts: change a consumer, transitive helper, fixture, data
  file, glob membership, lockfile, browser capability, policy, and test identity.
  Each must select the appropriate obligation.
  Unknown and deleted/renamed inputs must fail closed or expand selection.
- For local push, compare collected node identities: quick execution and separately
  required slow obligations must be disjoint and together cover the reachable
  non-exhaustive selection.
  Test mixed source/data changes, quick pool-heavy cases, unknown inputs, parse failures
  and global harness changes; preserve the exhaustive checkpoint obligation.
  Prove that ordinary CI still executes all quick cases and that missing slow evidence
  blocks the required merge aggregate.
- Reproduce the PR604 changed-path selection without running its entire workload.
  Report per-reason file counts, selected quick/slow identities and actual concurrency.
  Verify the new default on bounded semantic controls before one measured local run;
  retain the interrupted observation as incomplete rather than a performance baseline.
- Refuse forged, expired, failed, incomplete, wrong-runtime, wrong-root, unexpectedly
  skipped, or mismatched-collection evidence.
  Test classes and parameter text containing `::`; test worker collection failure
  separately from an honestly empty selection.
- Verify browser coverage against actual ordinary JUnit and required capabilities.
  Resolve the observed 210 Chromium omissions; retain justified optional omissions as
  explicit non-passes.
- Validate each performance candidate against the original semantic assertions before
  timing. Use the existing campaign’s paired design; retain contrary results.
  No claim of confirmed improvement from a single successful hosted run.
- Demonstrate that a docs-only correction reuses eligible unchanged consumer evidence, a
  changed test executes currently, and a shared mathematical or browser input
  invalidates all affected families.
  A failed sibling must not be relabeled by a reused successful worker.
- Capture at least twenty naturally occurring comparable ordinary PR runs for median and
  operational p95 reporting; with twenty observations, report the nearest-rank p95 and
  the sample count. Preserve queue, setup, gate, and artifact timings separately while
  retaining total elapsed time.
  Canceled or incomplete runs are reported, not assigned zero duration.
  Broader affected-checkpoint runs have their own declared cost and remain visible.
- Accept the ordinary-feedback objective only when median is at most 150s and observed
  p95 at most 180s without coverage loss.
  Follow the existing budget re-enforcement prerequisite as well; do not manufacture
  twenty expensive runs solely to fill a chart.
- Demonstrate a timeout receipt that identifies unfinished work and preserves diagnostic
  uncertainty. A clean later run does not close the unexplained 900-second failure by
  itself.

## Rollout and Coordination

Keep current delivery and this architecture change separately legible.
Report which product is live, which checks failed, and which obligations remain.
The original site delivery must not disappear behind a later CI repair status.

Use a source freeze for each validation batch.
Reuse reviewed unchanged source coverage across deltas and refresh affected reviews.
Generate a single evidence index rather than repeatedly copying timings into several
manual records. Before launching an expensive checkpoint, show the selected obligations,
invalidation reasons, expected cost, and available reused evidence; this satisfies the
existing selection rule without another approval ceremony.

Roll back a faulty selector to conservative complete-family execution while retaining
its diagnostics. Do not roll back browser capability or missing-result refusal to make a
workflow green. Retire the temporary strict workflow only after the ordinary workflow
proves equivalent execution and evidence acceptance on the same relevant inputs.

## Open Questions

- Which browser fixture sub-operations dominate the two largest setup phases, and how
  much is safely shareable immutable production?
  The recorded phase totals do not answer that yet.
- Which three initial families have sufficiently explicit inputs to justify reuse first?
  Select from measured cost and dependency clarity, not only apparent runtime.
- How much of observed startup can be removed without weakening provenance, pinned
  toolchain availability, or required browser capability?
- What caused the two unrecovered 900-second deadlines?
  The new journal improves the next observation; there is no established root cause yet.
- Which existing optional browser/PDF/native omissions are intentional product
  boundaries, and which need a capability-equipped selected lane?
  Keep each disposition explicit.

## References

- [Operating rules](../../../../operating-rules.md), especially OR-13, OR-14, OR-16,
  OR-17, and OR-18.
- [Validation loops](../../../../development.md#validation-tiers) and the
  [existing efficiency plan](plan-2026-09-06-validation-efficiency-and-checkpoints.md).
- [Validation-efficiency campaign](../../../../packing/benchmarks/validation-efficiency/README.md),
  the retained home for hypotheses, measurement design, and results.
- [Site-changelog closeout plan](plan-2026-10-13-site-changelog.md) and
  [PR599](https://github.com/jlevy/squares/pull/599), including independent reviews H–L
  and run-specific evidence.
- [Review K](https://github.com/jlevy/squares/pull/599#pullrequestreview-5520950386) and
  [Review L](https://github.com/jlevy/squares/pull/599#pullrequestreview-5521145558),
  which distinguish source approval, runtime limitations, and remaining hosted proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
