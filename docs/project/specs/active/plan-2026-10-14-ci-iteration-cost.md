---
title: Predictable CI Feedback and Measured Checkpoints
description: Overnight delivery retrospective and a measured implementation plan for ordinary CI within three minutes
author: Codex, independent Astra review and design
date: 2026-10-14
status: draft
---
# Feature: Predictable CI Feedback and Measured Checkpoints

**Date:** 2026-10-14

**Status:** Reconciled through the coordinating agent’s October 15 delivery snapshot.
The three-minute objective remains open.
This retained draft is for a focused plan PR; it does not carry the implementation or
approval of legacy PR599.

**Workflow entry:** `tbd shortcut new-plan-spec`, using `tbd template plan-spec`; W5
efficiency work and the existing validation-efficiency campaign.
**Tracking:** `think-kxmq`, with the retrospective under `think-d4ub`. The coordinating
agent owns bead updates and extraction of this draft into an isolated checkout.

## Overview

Restore ordinary pull-request feedback to roughly three minutes and stop paying for a
complete checkpoint after each small correction.
Keep fast checks automatic, select expensive checks from their actual inputs, and
require current, source-bound evidence for every merge obligation.
Expensive tests still run; their cost and selection become explicit.

The immediate problem is larger than a few tests crossing the 12-second CALL limit.
The measured quick workload contains almost 18,000 cases, whole-site browser exercises,
repeated complete registry checks, and real nested process tests.
Rebalancing four shards cannot by itself restore the target.
A second problem is repeated validation: the full dispatcher can serialize fast suites
that already passed elsewhere, while the temporary strict workflow repeats ordinary CI
to obtain browser and coverage guarantees that ordinary CI should supply.

This plan extends the existing
[validation-efficiency plan](plan-2026-09-06-validation-efficiency-and-checkpoints.md),
[measurement campaign](../../../../packing/benchmarks/validation-efficiency/README.md),
and retained validation tools.
It does not introduce another scheduler, evidence framework, or permanent duplicate CI
workflow. The required result is a smaller, correctly selected critical path with
auditable coverage.

## Current Delivery and Decisions

This October 15 snapshot supplements the original overnight record below; it does not
turn later successes into passing evidence for earlier failed gates.

| Work | Observed outcome | Remaining obligation |
| --- | --- | --- |
| Product delivery | [PR617](https://github.com/jlevy/squares/pull/617) delivered live 0.7.5. [PR618](https://github.com/jlevy/squares/pull/618) merged as `fc2ceae7` with 43 green checks, including [Deep 38726327460](https://github.com/jlevy/squares/actions/runs/38726327460). [Main Packing 38730161853](https://github.com/jlevy/squares/actions/runs/38730161853) and [Pages 38730161845](https://github.com/jlevy/squares/actions/runs/38730161845) passed; 0.7.6 is live. | These are delivered releases and complete checkpoint results, not three-minute performance proof. The local gate took 430.55s. |
| Closure delivery | [PR619](https://github.com/jlevy/squares/pull/619), head `3a00b004` on `fc2ceae7`, passed [ordinary Packing 38735580267](https://github.com/jlevy/squares/actions/runs/38735580267), [Pages 38735580297](https://github.com/jlevy/squares/actions/runs/38735580297) and [selected Deep 38735581202](https://github.com/jlevy/squares/actions/runs/38735581202). It merged as `31eaf6333c5d5b6b3d111241768cdd3d30982588` at 13:01:21 UTC on October 15. | [Main Pages 38739226771](https://github.com/jlevy/squares/actions/runs/38739226771) deployed successfully, but `verify-deployment` is in progress; [main Packing 38739227037](https://github.com/jlevy/squares/actions/runs/38739227037) is pending in this snapshot. The release claim remains withheld until verified deployment evidence is recorded. |
| Legacy CI branch | PR599 retains the investigation and strict-gate failures. Later [strict run 38665027001](https://github.com/jlevy/squares/actions/runs/38665027001) still failed four shard walls and eight CALL ceilings. | Extract small independently reviewed changes; ordinary green runs do not waive a selected strict failure. This plan PR will not import the large legacy implementation. |
| Upper-report checkpoint | The large producer/checker prototype was retired for disproportionate maintenance and recurring cost. The smaller same-workflow alternative remains unactivated. | A duplicate full-family job does not improve feedback. Any future activation must coincide with measured individual slow-operation placement and mandatory relevant-head coverage, while retaining fast negative guards. |
| Deferred-worker reuse (`think-2fp7`) | The bounded regularized-views candidate reached 88 focused passing tests. D1 optional-proof handling, D2 lookup timeout and E2 retry-history controls were corrected. | **Retired on E1 source provenance.** Head-commit consistency was only a partial check. Available native metadata could not authoritatively bind an arbitrary PR workflow’s executed merge source after PR associations disappeared. No production change or hosted speedup is claimed. |
| Live fast-proof safety (`think-3d1m`, F1) | Review found the same unauthenticated artifact-name boundary in the existing fast-proof verifier on main `fc2ceae7`. Removal of the automatic skip, old producer/lookup and dead code is in progress. | This is an active production safety fix. Main may repeat more fast work; assertions and ceilings stay intact, and no PR speedup is claimed. The retired candidate’s D/E findings are dispositions of unpublished work, not fixed production bugs. |
| Witness optimization | VE017 remains paused after automatic approval review denied execution. | Direct human authorization and a coordinated uncontended lane are required before measurement resumes. The external volume had 77 MiB free; broad disk work is held, with no internal-disk fallback. |

The closure’s broad local run took 729.90s and reported 10,930 passes, 49 skips, one
xfail, two stale-expectation failures and Ruff findings.
The two repaired cases passed in an isolated check in 1.86s. The identical-AST
comparison concerned only the generator’s Unicode spelling, not the repaired test code.
Neither observation makes the broad run pass or identifies its sole cause.
Separate real paper pipeline defects were corrected: a command omitted `--update`, and a
later PDF artifact had 23 pages against an unchanged 22-page limit.
Compacting only the lower paper’s printed history gaps restored 22 pages with all text
retained. Preserve those diagnoses separately from timing and stale-expectation
observations.

The duplicate regularized worker gives a bounded cost observation, not a reuse license.
Logs and Git commit metadata establish that PR618’s actual merge checkout `d66a6410` and
landed `fc2ceae7` shared tree `ead1cea5ba2e700ca6819f6bcef8b1bec8c9170e`. Their commands
took 324s and 541s, but their actual Ubuntu image builds were `20261012.334.1` and
`20261004.327.1`. The historical proof is refused.
Even safe reuse would have saved command allocation while retaining checkout/install and
leaving the longest slow lane on the critical path.
Extending provenance machinery for that saving was rejected; the patch and review fixes
remain research evidence only.

The new observations are preserved in the retrospective JSON’s dated follow-up, with
links to hosted runs and the retained candidate receipts.
Workflow elapsed intervals, local gate walls, isolated test times and overlapping agent
work remain distinct.
There is still no reliable total for agent effort, billed compute or time attributable
solely to storage.

### October 15 checkpoint follow-up

The earlier snapshot above remains a record of what was known at the time.
PR619 subsequently passed both main workflows and the deployed-site audit, which checked
4,460 expectations. Site 0.7.7, infographic 0.6.1 and lower-bounds paper 0.4.7 are live.

PR620 head `cf9003e0` passed its ordinary Packing and Pages workflows and all three
independent current-head reviews.
The selected
[full checkpoint 38744311408](https://github.com/jlevy/squares/actions/runs/38744311408)
failed: all ten dedicated Linux workers and macOS passed, but the integration job took
40m17s, including 2,301.62s in the validation command.
Its four quick shards passed every functional assertion and failed seven strict
12-second CALL limits.
The three-minute objective is still open.

The four shard Steps consumed 1,177.37s serially.
The largest other Step was the site layout exercise at 283.35s. These are command
measurements from this run, not a total for billed compute or agent effort.
Native job fan-out could reduce the serial wait, but would not itself fix a single
expensive test.

The next correction is grouped by cause: `think-2equ` covers repeated register/report
work, `think-n5ry` covers the drawing refusal and browser forwarding tests, and
`think-e2z4` covers native scheduling and its recurring cost.
Preserve the existing assertions, timing limits, negative controls and input isolation.
Measure scoped fixes before selecting another complete checkpoint; do not repeat the
whole run for each individual edit.

The selected scheduling change adds one native `integration-suites` worker alongside the
residual integration job.
It runs the same four quick Steps serially, with the existing four-process loadfile
recipe, two inner workers and 900-second subprocess deadlines.
Its initial run retained the strict 12-second CALL guard; the later policy decision
below changes that verdict.
The complementary integration command skips exactly those four Steps; the native
aggregate requires both owners.
Ordinary pull-request setup and commands stay unchanged.

This adds one history/submodule checkout, environment synchronization, Node/browser
bootstrap and timing upload per complete checkpoint, with no extra test execution.
Four separate workers would add three more setup cycles to save only about 53 seconds in
the recorded shape: the residual work was about 1,124 seconds and the four shards about
1,177 seconds. That is a scheduling projection, excluding setup and runner variation,
rather than a measured speedup.
The existing whole-checkpoint and full-tier ceilings stay unchanged.
The selected `--only` command has no named-tier verdict, as opposed to the named
ordinary PR suite commands; its worker and whole-checkpoint costs remain explicitly
accounted for.

Normal pytest failed-test retention recovered external scratch to about 733 MiB without
manual deletion. The cleanup bead is closed; broad builds still need a space preflight.
VE017 remains unexecuted pending direct human authorization.

### October 15 second-checkpoint follow-up

Head `15548357` groups the input-loading, drawing, forwarding and native-scheduling
repairs. Independent senior and security reviews cleared all 28 changed paths.
Its [ordinary Packing run](https://github.com/jlevy/squares/actions/runs/38756777827)
then failed on one different report case: the Mishapolk register-plan test passed its
assertions but took 47.56 seconds of CALL time, beyond the enforced 45-second PR guard.
The other ordinary owners passed, including frontend and macOS. The
[selected complete checkpoint](https://github.com/jlevy/squares/actions/runs/38756833833)
was still running when this follow-up was recorded.
These are matching-head observations, not a successful checkpoint or merge clearance.

The coordinator also chose an unnecessarily conservative local pre-push allocation:
effective Python CPUs 2, two outer jobs and one inner worker.
All 67 prerequisite Steps passed, but the whole quick suite used one pytest worker and
had reached only about 23% after 800.4 seconds.
The coordinator interrupted it rather than repeating that allocation; the parent exited
130 and its supervised child exited -15. The retained partial run is incomplete
evidence, not a passing local gate.
Future local selections must account for the effective pytest worker count as well as
the outer scheduler settings.

`think-2equ` tracks diagnosis of the newly exposed report cost.
The assertions, admissions and timing limits remain unchanged while that diagnosis runs.
The three-minute objective remains open; a source review cannot establish hosted runtime
or complete test coverage.

The completed checkpoint subsequently passed every dedicated worker and residual
integration. Its four-suite owner failed six CALL limits: five complete report-admission
cases and the forwarder refusal matrix.
Actual JUnit comparison preserves every previous quick node and skip reason and adds 16
passing regression cases; it establishes coverage for this scheduling change, not a
successful gate.
Residual integration took 1,054.30 command seconds, while the four suite
Steps totaled 1,041.54 seconds on their separate owner.
The longest owner was the slow lane at 1,665 job seconds, including setup.
These observations are not a controlled speedup estimate.

Five exact measured report nodes now use that existing slow lane, preserving their
complete bodies and fast refusal tests.
The forwarder test instead removes repeated work: eight complete production-check calls
replace 64, retaining every old address and all 45 single-field corruption assertions.
Its scoped local run passed six tests; the repaired call took 0.64 seconds in one
observation.
This grouped correction requires fresh ordinary CI and a complete checkpoint
at its new reviewed head, including execution of all five moved nodes without skips.

### October 15 third-checkpoint follow-up

[Full run 38763716551](https://github.com/jlevy/squares/actions/runs/38763716551) at
`43ee60f6f2f729384fdf91dc34ae58e05169aa03` failed its four-suite owner and aggregate.
Residual integration, all ten dedicated Linux owners and macOS passed.
The quick suite passed its functional assertions but reported eleven CALL costs from
12.39 to 27.72 seconds.
Its four Steps totaled 1,602.66 seconds, compared with 1,041.54 seconds at `15548357`;
these are overlapping-workflow component sums, not workflow elapsed time or billed
compute.

The two artifacts share 18,198 successful JUnit nodes.
Among 590 nodes previously taking one to three seconds, the median inclusive duration
ratio was 1.636; among 172 previously taking three to twelve seconds, it was 1.622.
These include setup and teardown.
Unrelated modules and all four shards moved upward, so the comparison does not establish
one new parser regression or its host cause.
The atlas-addressability test is a separate outlier: 0.571 to 27.723 seconds.
Its source can charge the first caller for loading all 324 witnesses and materializing
complete drawing frames just to read their sides.
Cold-cache attribution needs separate measurement; moving that work to setup would not
remove it.

The correction makes completed calls of at least 12 and less than 45 seconds advisory on
hosted full/main and scheduled runs, as they already were on ordinary PRs.
The 45-second hard backstop, 900-second child deadlines, full-tier and workflow wall
policies remain unchanged.
Local runs and explicit strict or budget-enforced runs retain 12-second enforcement.
All tests and assertions remain selected; no additional slow markers or workers are
introduced. This policy revision avoids treating one uncalibrated hosted reading as an
attributable regression.
It saves no test execution and does not establish the three-minute goal.
The implementation uses the existing tracked advisory declaration, with a separate CALL
scope, and focused refusal tests; it adds no timing service or evidence framework.
Fresh matching-head validation remains required before merge.

The final timing-policy and selection follow-up uses incremental evidence.
The full `43ee60f6` run completed the unchanged scientific implementations: its
slow-lane receipt has 241 passing tests and no skips, including all five moved report
cases. Its aggregate remains failed because of the recorded CALL timing verdicts.
That is not relabeled as a successful checkpoint.
A separate strong review found no reason to repeat that complete scientific run solely
for selection, reporting and timing-policy changes.

The integrated head must pass ordinary CI, including the selector, attribution,
gate-budget and validation-CLI controls.
These cover hosted events, strict/local enforcement, malformed policy, functional
failures and the 45-second backstop.
Any scientific input, dependency or execution change introduced during integration
requires its affected deeper checks.
Required native post-merge coverage remains enabled; incremental evidence does not
replace it or claim a fresh full-checkpoint pass.

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
- Remove duplicate execution only where source identity and complete outcomes are
  established. A source-provenance gap requires execution; it does not justify another
  evidence framework by default.
- Require every addition to account for its recurring CI cost before that cost becomes
  the next developer’s default wait.
- Diagnose a deadline failure from retained progress and process evidence before
  launching another expensive attempt.

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

The investigation retained GitHub metadata and job/step boundaries for ten runs and
eleven pull requests, plus the actual frontend timing artifact, in the
[retrospective audit record](../../reports/ci-iteration-retrospective-2026-10-14.json).
The subsequent completed
[run 38597483408](https://github.com/jlevy/squares/actions/runs/38597483408) is also
included in the chronology below.
The original records came from read-only GitHub API calls; they contain raw observations
rather than inferred billed cost.
The JSON distinguishes the later coordinating-agent snapshot from those original API
records. The coordinator also retained the four-shard cost cohorts, JUnit receipts,
runtime checkout bindings, and independent reviews A–L in the same closeout evidence
directory.

The table below uses UTC and API workflow start/end intervals.
Those intervals overlap; adding them would not measure user waiting time, billed runner
time, CPU time, or agent effort.
A workflow event’s head SHA is not necessarily its actual checkout: the normal frontend
artifact below identifies a merge checkout different from the event head.
Reuse must verify runtime identity.

The linked audit record is retained with this plan under `docs/project/reports/`. It
preserves the original API observations and labels the later delivery/status
reconciliation separately.
Bulk logs remain outside Git; the public run links make the hosted observations
independently inspectable.

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
| 12:38:31–13:29:22 | [Full run 38565361504](https://github.com/jlevy/squares/actions/runs/38565361504), head `e709…`, took 50m51s. Four CALL ceilings failed at 14.13, 13.67, 12.51, and 13.42s. Functional JUnit failures/errors were zero; the integration gate reported 2,866.49s. | The failed result remains failed. Successful worker observations remain useful evidence, but do not authorize reuse without source provenance. |
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
| Full dispatch repeated fast integration work. | The full integration topology can run four quick suites serially; the observed `e709…` integration command spent 2,869s while eleven independent workers succeeded. The existing merge-tree skip later exposed a source-provenance defect (F1). | Remove the unsafe skip. Prefer native same-workflow prerequisite results and measured producer improvements; preserve deliberate cold full execution. |
| New enforcement infrastructure had correctness bugs. | Review H found physical collection/JUnit identity mismatches, including parameter `::` handling, and a decimal-corner parsing defect. Review I confirmed their corrections. | Review collector and receipt semantics independently; use pytest’s actual identities and refusal controls before relying on a new gate. |
| CALL-only diagnosis missed inclusive cost. | An eager fixture initially hid atlas production from a CALL timer. Browser state and page-generation work also appears in expensive setup phases. | Measure setup/call/teardown and subprocess work; preserve real state isolation while removing duplication. |
| A deadline gave insufficient diagnosis. | The `1c5…` A and `fecca…` D timeouts lacked a complete cost report or a recoverable last executing node. | Flush lifecycle events and retain worker/process diagnostics before the deadline. Do not infer a cause or retry blindly. |
| Coordination became part of the delay. | The coordinator reports one-failure-at-a-time diagnosis, frequent long analysis, repeated manual evidence updates, and gate coordination. Those intervals were not metered. | Keep one generated evidence index, carry prior review coverage across deltas, and report delivered product separately from remaining certification work. |

Reviews also prevented regressions: the lazy-fixture finding, collector identity fixes,
and decimal parser correction were substantive.
The lesson is to preserve independent review while reducing redundant replay and manual
narration, not to label every review as waste.

### Where the original measured time went

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

## Design

### One coverage plan, existing execution surfaces

Use the existing validation selections and native workflow dependencies to state what
must run and why. A required aggregate must consume every selected prerequisite; missing
or unexpectedly skipped work cannot count as success.
Do not implement a second obligation ledger or per-node evidence service.
The retired prototypes showed that integrity machinery can cost more than the duplicate
work it proposes to remove.

Use the existing stable required context and workflow aggregation.
Do not add another permanent whole-suite workflow.
Fold the useful browser-capability, exact collection, and receipt guarantees from
`enforced-quick.yml` into ordinary validation, then retire its duplicate execution after
equivalent coverage is demonstrated.

| Surface | Selection | Evidence and budget |
| --- | --- | --- |
| Local edit and push | Existing cheap floor plus reachable changed behavior; unknown dependencies retain the current conservative fallback. | Immediate diagnostics. Local heuristic selection is not complete merge evidence. |
| Ordinary PR feedback | All genuinely fast checks, cheap scientific/refusal contracts, required browser smoke coverage, and inexpensive affected behavior. | Existing 150s target and 180s operational ceiling; total workflow critical path includes setup. |
| Affected expensive checks | Automatically selected when a declared consumer, input, fixture, toolchain, policy, or relevant test changes. | Explicit obligations with measured per-step ceilings; run beside ordinary feedback and block merge when required. |
| Explicit checkpoint | Complete the selected required work, or a deliberately requested cold full run. | Print selected work and expected cost before launch; retain native prerequisite outcomes. |
| Scheduled backstop | Daily complete independent execution, including expensive controls and browser coverage. | Detect missing dependency contracts and timing drift. It does not replace current affected pre-merge proof. |

Native same-workflow dependencies are the preferred boundary for required evidence and
partial retries.
Cross-run deferred reuse is not an accepted extension of current policy;
the regularized-worker attempt was retired on provenance.
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

### Input contracts and evidence boundaries

Begin selection at step or test-module granularity.
A reviewed dependency contract must cover:

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

Use existing pytest collection/outcome tools and native workflow success where they
already establish the required facts.
Same-repository labels, matching head metadata, and a successful aggregate do not by
themselves bind an arbitrary executed merge tree.
The existing fast-step artifact shortcut has the same live safety gap and is being
removed under F1 (`think-3d1m`). It cannot serve as precedent for a new deferred
capability.
Reconsider cross-run reuse only with a bounded authoritative source proof and
a measured benefit large enough to justify its maintenance.
No new reusable-workflow, attestation service or generic provenance system is planned.

Failed, expired, incomplete or unexpectedly skipped evidence remains refused.
Use Git for repository identity and diffs; do not invent source checksum registries.
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
4. **Topology and receipts:** remove redundant fresh collection, consume native
   same-workflow prerequisite results, and retain full history only where the job’s
   provenance contract requires it.
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

### Historical stabilization evidence

At the October 14 review,
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

If activating the proposed native upper-report worker, establish its mandatory
same-workflow owner and conservative input selection before moving the operation.
Activate that new owner and placement atomically after a bounded trial; do not
permanently duplicate an unchanged full family on every PR and call it a speed fix.
An individually measured operation can instead use the existing slow behavioral lane,
which already runs in complete, main and daily checkpoints.
Preserve its complete assertions and fast negative guards, and record the exact node and
measurement in the existing slow-marker registry.
For PR620, the coordinator requires a successful matching-head complete checkpoint
before merge and must inspect those exact nodes as executed, without skips.
The optional Deep label is not a protected PR prerequisite.
Reuse collection and outcome evidence from the actual execution; a second full
collection needs its own cost justification.
A slow marker alone cannot discharge coverage.

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
disjoint write set. The source plan and changes live outside PR599 and the atlas-width
branch until explicitly integrated.

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

### Phase 2: Enforce measured selection and the ordinary budget

One owner integrates planner and workflow changes after the component interfaces are
agreed.

| Component | Existing implementation to extend | Required behavior |
| --- | --- | --- |
| Selection | `packing/src/sqpack/cli/validate.py` and existing path/dependency tools | Explicit family/input contracts and selection reasons; preserve conservative unknown-input fallback without a new ledger. |
| Required evidence | Existing native job dependencies and pytest outcome tools | Same-workflow required coverage, complete outcomes and honest partial retries. Cross-run deferred reuse is retired. |
| Negative controls | Existing control registry and runner | Derive affected control families from actual consumers; select all on unknown dependencies or global harness changes. |
| CI integration | `.github/workflows/packing-validation.yml`, `deep-gate.yml`, and `enforced-quick.yml` | Ordinary browser coverage, one stable aggregate, selected expensive work, explicit checkpoint cost, removal of duplicate fan-out when safe. |
| Publication | Existing Pages scope/producer graph and workflow | Reuse its established input contracts where valid; retain actual produced-asset checks and published-site verification. |
| Policy and budgets | `development.md`, `operating-rules.md`, budget declarations, and existing wall-report tools | One documented tier model, inclusive cost admission, unchanged ceiling history, and explicit checkpoint selection. |

Trial one bounded selection against actual execution before changing automatic
membership. Expand only after unknown-input fallback, complete coverage and inclusive
cost are demonstrated.
Selection failure runs the complete relevant family or fails the aggregate; it never
creates a green empty selection.

### Next bounded slices and their cost tests

1. Complete the live F1 safety fix (`think-3d1m`): remove the automatic fast-proof skip,
   its artifact producer/lookup and dead code.
   Require actual execution through the existing gate.
   Record any increased post-merge allocation without relaxing an assertion or ceiling;
   this fix does not satisfy the PR feedback target.
2. Complete main Packing and deployed-site verification for PR619’s merged
   `31eaf6333c5d5b6b3d111241768cdd3d30982588`. Record verified publication evidence
   before making the release claim.
   This is delivery closeout, not acceptance of the three-minute objective.
3. Extract this retrospective and plan in a focused PR under `think-d4ub`, leaving PR599
   code and retired prototype sources out.
   Keep the compact observations and public run links; retain bulk logs externally.
4. Resume VE017 only after direct human authorization and sufficient external space.
   First test semantic equivalence; then use predeclared uncontended paired measurements
   with cold fixture production included.
   A rejected or paused experiment is not a speedup.
5. If measurements still justify upper-report placement, trial the existing native
   same-workflow alternative.
   Count scope calculation, checkout/install, collection, fixture setup, command,
   artifacts, aggregate serialization and worker allocation.
   Keep automatic membership unchanged until the mandatory owner and individually
   measured placement change can activate together.

Every addition must state its affected and unaffected invocation frequencies, source and
test maintenance, inclusive worker allocation, and critical-path effect.
The retired reuse patch illustrates the bar: about 213 net Python runtime lines, 477
test lines, 37 workflow lines and four API reads still bought only a possible
non-critical-path allocation saving, while leaving source provenance unresolved.
The larger upper-report prototype also added a checker and repeated setup/collection.
Neither is a deployment recommendation.
Prefer removing repeated work inside an existing producer when the same assertions and
isolation can be preserved.
Accept a candidate only after its declared semantic and cost criteria pass; do not count
a predicted reuse hit rate or move fixture cost outside the timer.

## Testing Strategy and Acceptance

- Reproduce cost summaries from retained raw reports without editing their verdicts,
  assignment history, or measurement boundaries.
  Keep unmeasured modules visible.
- Mutation-test input contracts: change a consumer, transitive helper, fixture, data
  file, glob membership, lockfile, browser capability, policy, and test identity.
  Each must select the appropriate obligation.
  Unknown and deleted/renamed inputs must fail closed or expand selection.
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
- Demonstrate that a changed test executes currently and a shared mathematical or
  browser input selects all affected families.
  A failed sibling remains failed.
  Require authoritative executed-source binding before proposing any new cross-run
  reuse.
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
invalidation reasons, expected cost, and native prerequisite results; this satisfies the
existing selection rule without another approval ceremony.

Roll back a faulty selector to conservative complete-family execution while retaining
its diagnostics. Do not roll back browser capability or missing-result refusal to make a
workflow green. Retire the temporary strict workflow only after the ordinary workflow
proves equivalent execution and evidence acceptance on the same relevant inputs.

## Open Questions

- Which browser fixture sub-operations dominate the two largest setup phases, and how
  much is safely shareable immutable production?
  The recorded phase totals do not answer that yet.
- Which single measured operation can be improved or selected more cheaply using the
  existing surfaces? A new job, collector or provenance layer needs its own cost case.
- How much of observed startup can be removed without weakening provenance, pinned
  toolchain availability, or required browser capability?
- What caused the two unrecovered 900-second deadlines?
  The new journal improves the next observation; there is no established root cause yet.
- Which existing optional browser/PDF/native omissions are intentional product
  boundaries, and which need a capability-equipped selected lane?
  Keep each disposition explicit.

### October 15 News Selection Follow-up

The News backfill exposed two causes of unnecessary local validation work.
Its two YAML files had no declared owner, so the push selector chose all 67
prerequisites. The Markdown PR template also matched the blanket `.github/`
suite-configuration rule and selected every quick test file.
The local run was interrupted after about five minutes as external scratch reached 32
MiB free.
This is incomplete validation, not a performance baseline or a successful gate.

Bead `think-k178` assigns the exact News files to the existing schema and synopsis
validators through `Step.known_inputs`. Those validators remain unconditional; the new
field records ownership without pretending their dependencies are fully enumerated.
Unknown files still select the full offered tier.
The PR-template exception is exact; actual and unknown workflow changes remain
conservative. Selection controls cover both files, unknown neighbors, literal path
matching, owner inclusion and restricted step universes.
The existing attribution report uses the same ownership declarations.

This change adds no validation job or deadline.
Its controls require hosted validation while local disk-heavy work is paused.
A measured reduction in iteration time remains to be established on the existing
validation surface.

## References

- [Operating rules](../../../../operating-rules.md), especially OR-13, OR-14, OR-16,
  OR-17, and OR-18.
- [Validation loops](../../../../development.md#validation-tiers) and the
  [existing efficiency plan](plan-2026-09-06-validation-efficiency-and-checkpoints.md).
- [Validation-efficiency campaign](../../../../packing/benchmarks/validation-efficiency/README.md),
  the retained home for hypotheses, measurement design, and results.
- [Site-changelog delivery (PR590)](https://github.com/jlevy/squares/pull/590) and
  [PR599](https://github.com/jlevy/squares/pull/599), including independent reviews H–L
  and run-specific evidence.
- [Review K](https://github.com/jlevy/squares/pull/599#pullrequestreview-5520950386) and
  [Review L](https://github.com/jlevy/squares/pull/599#pullrequestreview-5521145558),
  which distinguish source approval, runtime limitations, and remaining hosted proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
