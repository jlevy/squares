---
title: Validation Parallelism Efficiency Block
date: 2026-09-29
status: in_progress
---
# Validation Parallelism Efficiency Block

**Workflow:** pipeline improvement, efficiency focus.
**Tracking:** `think-xcij` (local allocation) and `think-tddk` (hosted fanout), within
Session 164. The repository owner requested this block while PR 246 completes
certification.

## Problem and Evidence

The published integration checkpoint `5d276119c52b98ac6770b08bc9b1e582746abe02` passed
its local push tier in 856.20 seconds: 51 selected steps, 2,959 passing tests, 6 skips
and 19 deselections.
Pytest took 824.46 seconds for 114 selected test files.
The
[retained log](../../../packing/campaign/agent-sessions/session-164-push-final.log.gz)
is a successful operational baseline, not a repeated performance experiment.

The scheduler defaults to as many outer jobs as CPUs.
Pytest receives `max(1, cpus - jobs + 1)` workers, so the default on this ten-CPU host
gave this large proper subset one worker.
Other checks finished while pytest continued serially.
The existing whole-suite fallback gets a different allocation; subset size must not
silently determine whether the host is used.

Simply allowing two outer jobs is insufficient: another exact-verification step can
itself launch nine subprocesses.
The fix must account for nested pools as well as the number of top-level jobs.
Explicit operator resource choices remain authoritative.

The hosted audit identified two critical paths in retained runs: exhaustive tests and
the serial deferred-check job.
Ordinary PR CI already distributes its work over seven roughly balanced jobs.
Further ordinary-PR fanout is not selected without new evidence.

## Parallel Work and Acceptance

Sol owns local scheduling and its behavioral regressions.
A second Sol lane owns hosted scheduling and partition contracts.
A third reviews resource use, unchanged coverage, failure propagation and integration.
The coordinator owns measurements, research-status records and publication.

The local change must give the reachable pytest selection an exclusive CPU allocation
while allowing independent edit checks to retain their existing concurrency.
It must preserve the selected files and the exact union of non-exhaustive tests,
propagate failures, respect explicit resource overrides, and bound nested pools.
Focused regressions must demonstrate these properties on both a single-CPU host and a
multi-CPU host.

The hosted change assigns whole existing tests and whole validation steps to concurrent
jobs. It does not split a mathematical decision into partial claims.
Every job must use one resolved immutable commit.
A contract must reject missing or duplicate assignments, and the final required job must
fail if any necessary job fails, is cancelled, or skips.
Artifact names must be unique.
Existing per-test mathematical assertions and receipts remain intact.

## Measurement Plan

The separate selector-precision slice is `think-6izq`. It may discard comments and known
benign metadata imports as evidence of a repository walk, but must retain marker-bearing
code strings, including strings passed through subprocess aliases or helpers.
It does not attempt temporary-directory dataflow analysis.
Its selected-file changes require their own positive and conservative-fallback tests;
they are not part of a same-selection scheduler comparison.

Before timing, freeze the affected implementation and the exact selected targets.
Use the maintained [timing instrument](../../../packing/benchmarks/validation_timing.py)
for any paired pytest measurements, with raw output and JUnit identities.
Keep temporary outputs and caches on the external scratch volume.
Do not run competing heavy local work during a timing trial; remote CI and lightweight
review can continue.

The first full candidate run is an operational check: require the unchanged workload to
pass and record elapsed time, worker allocation, skips, and collection counts.
Compare it with the retained successful baseline, naming any source or workload
differences. A single observation supports no general speedup estimate.
A repeated performance claim requires the existing
[campaign protocol](../../../packing/benchmarks/validation-efficiency/README.md), with
predeclared matched pairs, identical test identities and nonoverlapping timing ranges.
Do not repeat long serial runs solely to manufacture a percentage when an operational
result and scheduler regression establish the fix.

Hosted acceptance requires every new job and its required aggregator to pass on the
published candidate.
Record individual job durations and the overall critical path; sum of runner time is a
separate cost. Derived initial ceilings are not fresh timing measurements.
Any remaining indivisible long test is an explicit follow-up, not a reason to omit its
assertions.

## Results

The first local scheduler candidate `1afb75ca6` selected the whole non-exhaustive suite
after a workflow change.
Its pytest phase passed 7,714 tests with 9 skips in 968.77 seconds on ten workers with
`PACK_JOBS=1`. The complete push tier took 1,034.70 seconds and failed one documentation
check because this review was absent from the document map.
The
[failed run log](../../../packing/campaign/agent-sessions/session-164-efficiency-push.log.gz)
retains that result.
The earlier 2,959-test run selected a different workload, so those two walls do not form
a speedup comparison.

The predecessor `5d276119c` passed required packing and page CI and the complete
[deferred checkpoint](https://github.com/jlevy/squares/actions/runs/36630574302). The
published documentation repair `9174140a8` then passed 51 selected push steps and 1,733
tests in 181.36 seconds.
The new
[deferred run 36636552951](https://github.com/jlevy/squares/actions/runs/36636552951)
resolved PR merge commit `0376416ec9ab3220bb87e52888ddb72919d3e861`. All nine workers
and the required aggregate passed on that merge tree.
The wall from run start to the last required job was 1,133 seconds; `screen` completed
last at 1,111 seconds.

| Hosted job | Wall |
| --- | ---: |
| `screen` | 1,111 s |
| `deferred-slow-lane` | 1,015 s |
| `exhaustive-1` | 957 s |
| `exhaustive-2` | 953 s |
| `exhaustive-3` | 858 s |
| `deferred-threshold-1440` | 778 s |
| `deferred-threshold-720-rigidity` | 623 s |
| `deferred-controls-finer` | 621 s |
| `deferred-atlas-grid` | 475 s |
| `resolve-tree` | 17 s |
| `deep-gate-required` aggregate | 32 s |

The resolver and nine workers consumed 123.47 runner-minutes by the reported job walls,
or 124 minutes including the aggregate.
The predecessor checkpoint used approximately 100 runner-minutes including its
aggregate. These are unpaired observations of different source trees and job layouts;
neither difference establishes a speedup or regression caused by the fanout.
The new per-job wall fields still need measurement admission into the budget register.

The broad local push at `91bb57cb2` then failed before the pool-heavy phase.
Its normal phase reported 7,703 passes, 9 skips, 14 failures and 23 setup errors in
300.22 seconds; the full tier stopped at 366.08 seconds.
The
[retained failure log](../../../packing/campaign/agent-sessions/session-164-pool-phase-initial.log)
shows that the pool phase was correctly skipped after the normal phase failed.
The 23 errors came from adding the `pool_heavy` marker to `packing/pyproject.toml`, one
of 19 frozen native proof inputs.
That file’s original Git blob has been restored, and the marker is registered in
`tests/conftest.py`; all 28 native parent-core receipt tests now pass, including the
proof-input check.
The 14 failures were runner-unit mocks inheriting the enclosing gate’s
artifact variables. A test-only fixture clears those inherited variables; 51 runner and
progress tests pass with the parent variables present.
These focused results do not turn the failed `91bb57cb2` gate green.
The repaired frozen candidate `a2b8e696c` passed all 51 selected push steps in 623.04
seconds. Its normal phase passed 7,750 tests with 9 skips in 416.24 seconds; the pool
phase passed its one atlas test, whose call took 132.83 seconds.
Both phases carry the same source and run identity.
The retained
[receipt](../../../packing/campaign/agent-sessions/session-164-pool-phase-passed.log)
records the outcome and allocation.

The CPU-active tail in the first broad run was not identified by its quiet pytest
output. Earlier retained timings show that the whole-atlas composite test can take
1,327.87 seconds in one call while its per-case pool obeys `PACK_JOBS=1`. The later
implementation gives this explicitly marked test a separate serial-pytest phase with the
available CPUs assigned to its existing per-case pool.
Other slow tests remain in the parallel phase, and the mathematical assertions are
unchanged. A collect-only check of the non-exhaustive suite found 7,744 nodes: 7,743
ordinary and one pool-heavy, with no overlap or omission.
The completed split used ten normal pytest workers with `PACK_JOBS=1`, then one pytest
process with `PACK_JOBS=10`. Live receipts also exposed a remaining normal-lane tail: at
most four workers were active during the final 121 seconds and at most two during the
final 62 seconds. `think-ii0r` tracks a measured scheduling follow-up, including
fixture-preserving work stealing or long-first ordering.
This observation alone does not establish which alternative will help.

Main and daily workflow parity, child-pytest progress receipts, and the pool-heavy
allocation are integrated locally.
Explicit event-aware wall sampling is implemented at `902b959b4` but has not yet been
published or measured on a hosted run.
Post-merge wall reporting is integrated under `think-0atx`, with 74 focused tests and
independent review. It refuses missing or duplicate prerequisites, excludes unrelated
jobs, leaves unfinished walls unknown, and identifies the latest completing prerequisite
as the critical endpoint.
The integrated workflow, allocation, receipt and budget contracts previously passed 283
focused tests in 54.36 seconds.

No general speedup is claimed from these operational checks.
The full native external rectangle replay and T-059 complete row-minimum census remain
separate mathematical obligations; changing validation scheduling establishes neither.

### Publication Contract and Concurrent Probe Repair

The subsequent `0ce06bfd9` publication delta passed 1,778 tests but failed two in 263.93
seconds total. The
[failure excerpt](../../../packing/campaign/agent-sessions/session-164-publication-initial.log)
retains both findings.
The single-observation wall entries needed the sampler’s max/min ratio of 1.00, with
runner variance still unknown.
The correction preserves the workflow contract and existing ceilings.

The second failure was a concurrent test race (`think-4u84`). A cache-copy test wrote an
ordinary 1,000,003-byte probe into the live checkout while a different pytest worker
measured its snapshot size.
The failing count exceeded the clean count by exactly that probe size.
The clean snapshot measured 167,549,239 bytes, below the unchanged 167,772,160-byte cap.
No new linked evidence caused the overage.
The repair runs the same probe and copy assertions inside a private source snapshot,
binds its subprocess imports to that snapshot, and checks that the live checkout stays
free of the probe. The concurrent two-worker regression passed both affected tests.
The broader source-headroom task `think-t1lk` remains open.
Publication still requires the repaired integrated push and hosted evidence.

### Independent Review

The first local scheduler candidate gave large narrow pushes exclusive pytest workers
without reserving the load marker.
The corrected scheduler reserves it atomically when free and retains the former
conservative allocation while another gate holds it.
It also refuses missing or extra selector-summary lines, preserves explicit worker
settings, keeps edit failures in the ordered report, and releases the marker on
interruption. Its 28 focused tests and clean lint and type checks cover those controls;
the integrated runs above expose the remaining wall and pool-phase questions.

The separate selector refinement has a narrow coverage claim: it may remove walker
evidence that exists only in comments or in the exact benign
`from importlib.metadata import version` import.
A comparison of the current test roots found precisely two files whose old raw marker
disappears for those reasons.
Review also found dynamic-import attributes, imported helper names, bytes literals, and
helper calls that an initial AST implementation could miss.
The final selector parses and unparses source after removing only the exact benign
metadata-version import, then applies the old marker scan to the executable text.
The 54 focused selector tests, Ruff and BasedPyright passed.
The integrated candidate selected the broad suite after the workflow change.
The repaired pool split has the passing integrated receipt above.

The hosted fanout resolves one immutable commit before workers start.
Each worker checks its checkout against that commit and writes a tree receipt before
validation. Four jobs divide existing deferred Steps without splitting a Step.
Three exhaustive jobs use a whole-file partition that includes new paths through a
stable hash fallback.
The partition contract covers every discoverable test file, so module, class,
parametrized, inherited, and dynamic marker styles remain eligible.
A collect-only integration check found 60 exhaustive nodes split 2, 30, and 28, with no
duplicates or omissions.
The aggregate tests every prerequisite for success, and artifact names include the job
and attempt.
The final focused workflow, shard and budget suite passed 93 tests with Ruff
and BasedPyright clean.
The separate pending-measurement budget contract passed 55 tests.
The first hosted fanout passed on the resolved merge tree named above.
Its worker and aggregate outcomes establish operational coverage for that tree only.

New hosted ceilings are derived from predecessor Step or JUnit times plus setup.
The new deep-gate jobs and whole wall now carry the single hosted observation above; the
sample max/min ratio is 1.00 for that one observation, while runner variance remains
unknown. Existing multi-run slow and screen baselines are preserved.
Main/daily measurements remain pending under `think-0atx`. One run does not establish a
stable performance baseline.
Artifact upload remains advisory and may warn without failing a passing validation job;
the in-job checkout equality test is fail-closed.
For a manual pull-request dispatch, GitHub’s event SHA names the dispatch ref while
workers validate the resolved merge SHA. The tree receipt and custom validated-SHA field
in exhaustive per-file reports name the latter.

## W5 Follow-up: Snapshot Ancestry Accounting

CI run 36655332600 spent 13.45 seconds in the snapshot-accounting control, beyond its
12-second call limit.
This integration issue was handled alongside the T-060 proof lanes, without a broad
local suite. The focused local test took
[6.23 seconds before](../../../packing/campaign/agent-sessions/session-164-validation/snapshot-ancestry-before.txt)
and
[0.74 seconds after](../../../packing/campaign/agent-sessions/session-164-validation/snapshot-ancestry-after.txt)
the accepted change.
These are individual observations during ongoing source intake, not a frozen-tree
benchmark or a claim about hosted runtime.

The first hypothesis, pruning cache directories before traversing them, measured 6.30
seconds and was discarded.
Profiling instead attributed 21.8 of 22.9 instrumented test seconds to 323,185 repeated
path-ancestry comparisons.
The fix constructs the candidate path’s ancestor chain once and looks up each ancestor
in a set of prune roots, rather than reconstructing it for every root.
File-root equality, directory containment and prefix collisions retain their previous
Path semantics.

The equivalence control and original timing test pass; three further controls confirm
linked evidence, registered dependencies and cache exclusion survive real snapshots.
Ruff and BasedPyright pass.
No ceiling, test selection or mathematical acceptance rule was relaxed by the ancestry
optimization. `think-9b01` tracks that fix.
Current-head hosted timing remains to be checked.

The next reviewed proof receipts raised the required snapshot to 167,821,919 bytes,
49,759 bytes above the 160 MiB storage guard, after four measured non-input prunes.
The separate storage adjustment restores roughly 32 MiB of headroom with a 192 MiB
ceiling, retaining all linked proof evidence.
It changes neither copied bytes nor runtime limits; at three workers the ceiling is 576
MiB. The oversized-input refusal still applies.
The existing `think-t1lk` owns durable dependency-aware selection; `think-n2kg` was
consolidated into it rather than maintaining a duplicate task.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
