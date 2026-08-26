---
title: Research-Loop Efficiency Infrastructure Plan
description: Data-driven plan for a one-minute Square Packing PR signal and faster research loops
author: Codex, for the project maintainers
date: 2026-08-25
status: active
---
# Feature: Research-Loop Efficiency Infrastructure

**Date:** 2026-08-25 (last measured 2026-08-26)

**Author:** Codex, for the project maintainers

**Status:** Active

**Workflow entry:** W5 `efficiency-loop`

**Primary focus:** Efficiency

## Decision

The required pull-request signal will be a stable `packing-required` check whose work
finishes in about one minute.
It will fan independent tests and validation groups across GitHub Actions jobs and
aggregate their results.
No full macOS duplicate will block every research pull request.

Until every exhaustive group fits the budget, the required lane runs the fast,
high-signal set. Full exact construction tests, all mutation controls, full macOS, and
deep golden remain mandatory at the declared integration boundary and on scheduled or
manual runs. They return to the required pull-request matrix only after sharding or
implementation improvements keep every constituent job inside its budget.

This is W5 efficiency work.
It changes execution, scheduling, and measurement, not the W1–W7 process, scientific
criteria, artifact ownership, or failure semantics.

## Numeric Budgets

| Surface | Warm p50 | p95 | Hard action threshold |
| --- | ---: | ---: | --- |
| Required PR end-to-end | ≤60s | ≤75s | Reject repeated same-revision runs over 90s |
| Required job work | ≤45s | ≤50s | Split or optimize the job |
| Required job including setup | ≤55s | ≤65s | Remove it until repaired |
| Local focused test | ≤20s | ≤30s | Narrow the target or remove repeated work |
| Local fast gate | ≤45s | ≤60s | Profile before adding work |
| Full Linux integration | ≤120s | ≤150s | Open or renew a W5 bead |
| Selected macOS portability smoke | ≤45s | ≤60s | Narrow to the platform contract |
| Full macOS plus deep golden | Informational | Informational | Integration, main, schedule, or manual only |

Hosted-runner time is a service level, not a functional assertion.
Ten repeated runs of one unchanged revision determine whether a new layout meets the
budget.

## Measurement Rules

Every receipt identifies the source and dirty-state identity, command, resolved working
directory, selected surface, platform, worker settings, queue seconds, setup seconds,
work seconds, end-to-end seconds, selected test or control ids, status, termination
reason, and artifact identity.

Reports separate critical-path wall time from total runner- or agent-seconds.
A parallel design succeeds only when it shortens the critical path without omitting
work, hiding a failure, or multiplying total compute beyond the declared limit.

## Measured Baseline

### GitHub Actions: 24 Successful Packing Runs

The sample covers the latest 24 successful `Packing validation` workflows through run
`32926510669`. It spans revisions, so it describes the current service rather than a
controlled before/after experiment.

| Surface | Minimum | p50 | p95 | Maximum |
| --- | ---: | ---: | ---: | ---: |
| Workflow end-to-end | 290s | 346s | 430s | 440s |
| Linux queue | 2s | 3s | 4s | 30s |
| Linux job | 156s | 250.5s | 289s | 378s |
| Linux full-validation step | 136s | 240s | 267s | 367s |
| macOS queue | 2s | 3s | 10s | 29s |
| macOS job | 286s | 342.5s | 425s | 436s |
| macOS full-validation step | 151s | 208s | 276s | 319s |
| macOS deep golden | 76s | 99s | 139s | 146s |

Queueing and setup are not the main problem.
Setup is about 8 seconds at Linux p50 and 15 seconds at macOS p50. Test and validation
work dominate.

The current PR receipt, run `32926510669`, is more severe:

| Work in the current PR | Seconds |
| --- | ---: |
| Linux job | 378 |
| Linux full gate | 366.21 |
| Linux behavioral pytest | 251.26 |
| Linux negative controls | 158.84 |
| Linux soundness perimeter | 53.88 |
| Linux historical regressions | 29.53 |
| Linux Python lint | 20.76 |
| Linux deterministic SVG | 19.76 |
| Linux Trump cones | 16.36 |
| macOS job | 436 |
| macOS duplicate full gate | 318.28 |
| macOS deep golden | 95.89 |

Linux and macOS spent 684.49 runner-seconds repeating the ordinary gate.
macOS then spent another 95.89 seconds on deep golden.
Removing macOS alone would save only 58 seconds from this PR’s critical path and would
leave a 378-second Linux result.
Linux must be split and optimized too.

### Local Pytest

Before the loop-2 exact additions, hosted Linux pytest had a 10.44-second p50 and a
13.60-second p95. The current PR took 251.26 seconds, a 24× regression.
The native-timing correction spike independently reproduced the local bottleneck: its
clean full gate took 327.66 wall-seconds, including 241.96 seconds of behavioral tests
and 167.23 seconds of negative controls running on overlapping branches of the outer
scheduler.

| Test group | Tests | Seconds | Share |
| --- | ---: | ---: | ---: |
| Four exact files | 30 | 212.53 | 93.9% |
| All other tests | 94 | 14.95 | 6.1% |

The exact-test tree accounts for 212.18 pytest seconds:

```text
exact tests — 212.18s
├── test_minus_w_stress.py — 122.47s
│   ├── six curvature parameters — 106.15s
│   ├── uniform rescale — 10.88s
│   └── perturbation — 5.44s
├── test_minus_w_row_jets.py — 54.00s
│   ├── six owner inventories — 32.31s
│   ├── three active inventories — 16.50s
│   └── SAT curvature — 5.19s
├── test_minus_w_sheet.py — 20.92s
└── test_exact_jets.py — 14.70s
```

The 30 tests perform 35 production `active_row_jets` constructions plus three
independent test-only constructions.
The constructor builds dense exact 15×15 jets.
`owner_row_jets` rebuilds the active inventory, and each stress parameter evaluates
three velocities.
One profile recorded 54.4 million calls in an `active_row_jets()` path.
Repeated construction explains nearly all 212 seconds.

### Negative Controls

All 62 controls passed with identical outcomes:

| Workers | Wall seconds | Speedup |
| --- | ---: | ---: |
| 1 | 158.54 | 1.00× |
| 2 | 98.17 | 1.61× |
| 4 | 90.19 | 1.76× |

Two workers are the efficiency knee.
Four save only another 7.98 seconds.
Worker tuning alone cannot meet a one-minute job budget.
Four job-level shards have a 39.64-second theoretical mean before setup.

Forty-nine controls repeat four checker families: 30 ledger, eight synopsis, seven
schema, and four canonical checks.
This is the next target if sharding leaves a long tail.

### Codex Research-Loop Time

The corrected scanner emits `CodexEfficiencyRollup/v2`. It uses event timestamps for
overlap-safe accounting and reads native `task_complete.duration_ms` and
`time_to_first_token_ms` for completed-turn coverage and distributions.
It also counts current `ContextCompaction` items, excludes duration-inconsistent
compressed legacy replays, and freezes live trees at scan start or an explicit
`--through` cutoff.

Response envelope is still not provider inference latency.
It is active time after explicit tools and compaction are removed.
Timed `Reasoning` and `AgentMessage` items are a lower bound; first-token wait measures
only the first response in each completed turn; residual response can include later
model starts, API and client latency, orchestration, suspension, and uninstrumented
gaps.

#### Research Loop 2 Frozen Snapshot

Root `01a03b2a-d50b-7582-8d78-be6d8ebb461d` is frozen through
`2026-08-26T05:05:06.988Z`:

```text
parent active — 5h45m37s
├── response envelope — 3h05m46s (53.75%)
│   ├── timed reasoning/message stream — 1h08m56s (19.94% of active)
│   ├── recorded first-token wait — 57.6s (0.28% of active)
│   └── residual response — 1h55m53s (33.53% of active)
├── delegated-agent wait — 1h24m15s (24.38%)
├── commands — 1h05m55s (19.07%)
├── compaction — 9m04s (2.62%)
└── other explicit tools — 37.5s

recursive tree — 14 sessions
├── recursive agent-time — 11h01m38s
├── active union — 5h45m37s
└── concurrency overlap — 5h16m01s
```

All 87 completed recursive turns have native duration and first-token fields.
Their reported duration totals 10h17m37s; p50 is 3m00.586s, p95 is 14m19.252s, and the
maximum is 2h06m30.237s. The native total differs from the matching event intervals by
only 274 milliseconds.

| Model | Thinking | Completed turns | Responses | Response envelope | First token | Timed stream | Residual |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `gpt-5.6-sol` | xhigh | 83 | 1,981 | 6h43m50s | 7m35s | 3h16m36s | 3h19m39s |
| `gpt-5.6-sol` | max | 4 | 232 | 44m38s | 25.8s | 27m27s | 16m45s |

The recursive tree records 2,213 response events, 288,786,067 input tokens, 280,945,664
cached input tokens, 1,002,754 output tokens, and 370,981 reasoning-output tokens.
The explicit stream comprises 3h23m48s of reasoning items and 20m14s of message items.
The 8m01s total first-token wait is 1.8% of recursive response envelope, so first-token
latency is not the main target.

The first orientation fan-out was effective: 11m22s of agent work completed in a 4m40s
tail.
The long R4, R5, and scope trio used 257m07s of agent-time, required 65 follow-ups,
left 86m35s with no long child active, and ended with a 41–42-minute single-agent tail.
The next delegation experiment therefore uses revision-pinned leaf waves with at most
one corrective follow-up, not another broad agent.

Parent command categories identify 2,493.13 seconds of validation and pytest work, 63.0%
of all command time, plus one 492.11-second CI wait.
Category names are substring heuristics; exact normalized commands establish at least
two ordinary full gates totaling 755.94 seconds, four standard fast gates across parent
and children totaling 552.13 seconds, and three exact-row test runs totaling 435.26
seconds. Canonical revision/surface fingerprints are required before automatic
deduplication.

#### Research Loop 1 Old

Root `01a02fc2-081b-72b1-999a-cd5550629c0c` is terminal at `2026-08-25T15:22:28.182Z`:

| Measure | Value |
| --- | ---: |
| Parent wall envelope | 45h28m27s |
| Parent active | 37h02m09s |
| Parent inactive | 8h26m18s |
| Parent response envelope | 31h24m25s (84.8% of active) |
| Parent first-token wait | 4m17s (0.23% of response envelope) |
| Parent commands | 3h08m46s (8.5% of active) |
| Parent delegated-agent waits | 2h23m25s (6.5% of active) |
| Recursive sessions | 139 |
| Recursive agent-time | 57h07m47s |
| Active union | 37h02m09s |
| Concurrency overlap | 20h05m37s |
| Completed turns | 375; native duration and first-token coverage 100% |
| Compactions | 96 legacy events; duration unavailable |

The scanner rejected one compressed parent-history replay from a legacy child.
Its client duration was 14,051.726 seconds while its local replay interval was 86
milliseconds. After exclusion, recursive reported duration differs from matching event
intervals by 1.101 seconds rather than 14,052.827 seconds.

Loop 1 has no explicit stream-item timing.
Its 12,869 response events record 1,601,149,478 input tokens, 1,558,305,024 cached input
tokens, 5,650,164 output tokens, and 2,068,192 reasoning-output tokens.

| Model | Thinking | Responses | Response envelope | First-token wait |
| --- | --- | ---: | ---: | ---: |
| `gpt-5.6-sol` | max | 9,887 | 42h06m00s | 12m58s |
| `gpt-5.6-sol` | xhigh | 1,168 | 4h06m27s | 2m36s |
| `gpt-5.6-sol` | high | 191 | 52m40s | 50.0s |
| `gpt-5.6-terra` | low | 849 | 1h40m02s | 8m56s |
| `gpt-5.6-terra` | medium | 199 | 26m46s | 1m10s |
| `gpt-5.6-luna` | low | 557 | 1h03m05s | 3m00s |
| `gpt-5.6-luna` | medium/max | 18 | 2m17s | 15.3s |

Historical model assignments are confounded by task role.
They motivate the paired mechanical-routing experiment but do not prove that a lower
model or thinking level would complete matched work faster at the same correction rate.

## Ranked Implementation Queue

| Rank | Work | Owner | Baseline | Expected result | Allocation |
| ---: | --- | --- | ---: | ---: | ---: |
| 0 | Fast required lane and stable aggregator | `think-l7hi` | 346s p50 | ≤60s p50 | 0.5 day |
| 1 | Split Linux tests and controls across jobs | `think-l7hi`, `think-rthe` | 251s tests; 159s controls | every shard ≤45s | 1 day |
| 2 | Reuse exact row-jet inventory | `think-kdil` | 212.53s exact | 30–45s | 1 day |
| 3 | Revision-keyed validation receipts | `think-3mkx` | 1,743s repeated | ≥50% reduction | 0.5 day |
| 4 | Joined recurring efficiency report | `think-xuk8` | manual | one command | 0.5 day |
| 5 | Leaf delegation and model-routing test | `think-5zgv` | 65 follow-ups; 41m tail | ≤20; ≤20m | 0.5 day |

Ranks 0–2 are the first implementation checkpoint.
Ranks 3–5 may run as disjoint spikes, but they do not delay the one-minute CI work.

## Spike 0: Immediate Fast Required Lane

1. Register an `exhaustive_exact` pytest marker.

2. Mark only the slow constructor and evaluator nodes in the 212-second profile.
   Keep cheap exact algebra, branch, error, and field-mismatch tests required.

3. Make `packing-validate --fast` run `pytest tests -m 'not exhaustive_exact'`.

4. Leave default and full discovery unchanged at all 131 current tests.

5. Keep negative-runner unit tests, workflow contracts, selection manifests, schemas,
   lint, and cheap scientific smoke checks required.

6. Move the monolithic 62-control run and exhaustive exact group to integration, `main`,
   scheduled, and manual assurance until their shards meet the budget.

7. Replace job-name-specific branch protection with a stable `packing-required`
   aggregator.

Expected immediate effect: behavioral pytest falls from 251 seconds to about 15–20
seconds. The required validation step should finish within 35 seconds and the warm
workflow within 45–60 seconds.

### Spike 0 Implementation Receipt

Session 020 implemented the bounded version under `think-b784`:

- pull requests run the Linux fast validator and report `packing-required`;

- pushes to `main`, manual dispatches, and the weekly schedule retain complete Linux,
  complete macOS, exhaustive exact tests, all controls, and the macOS deep golden;

- exactly four measured slow modules declare `exhaustive_exact`;

- full pytest collects 131 tests, while the fast selection runs 101 and deselects the
  same 30 exhaustive exact tests; and

- the full negative-control step uses its measured two-worker knee.

The first local required command finished in 32.90 wall-seconds.
Its only failures were the expected stale synopsis and generated ledger caused by
opening session 020. After those records were reconciled, the same command passed in
27.38 seconds; its 101-test behavioral branch used 13.39 seconds, Python quality used
11.92 seconds, schemas used 9.83 seconds, and bead validation used 9.61 seconds.
Those branches overlap under the two-worker outer scheduler.

The direct two-worker control step passed all 62 controls in 100.32 seconds, versus the
158.54-second one-worker baseline.
This removes 58.22 seconds from the integration branch without changing the PR lane or
mutation inventory.

The corrected complete gate proved the deferred side of the partition: all 30 exhaustive
exact tests passed in 254.16 seconds.
The concurrent core branch then stopped on `Errno 28` because the macOS host had only
359 MiB free; it was not a test assertion failure.
The same 101-test core passed alone in 15.26 seconds.
This receipt does not count as a clean full-gate sample, but it confirms both selected
halves and reinforces that exact row-jet reuse is the next integration-speed target.

A one-worker retry avoided the constrained host’s concurrent temporary-space peak and
passed all 33 complete-gate steps in 533.42 seconds.
Exhaustive exact tests used 231.55 seconds, controls used 83.63 seconds, and soundness
used 38.17 seconds. This serial receipt proves the complete integration surface; it is
not the default worker layout or a pull-request latency target.

The first hosted result, run `32941767003` at commit `ccc1bb5`, passed in 46 seconds end
to end:

| Hosted PR component | Seconds |
| --- | ---: |
| Workflow end to end | 46 |
| Linux `validate` job | 37 |
| Checkout, setup, and locked sync inside the job | 11 |
| Required fast-validation step | 24 |
| `packing-required` job | 2 |
| macOS portability | skipped |

The preceding revision required 310 seconds for Linux and 601 seconds for the macOS
tail. The first spike sample therefore reduces the Linux job by 88.1% and the PR tail by
92.3%. It meets the 60-second target, but the ten-run p50/p95 acceptance sample remains
open under `think-l7hi`.

If later hosted samples exceed one minute because of work rather than queueing, the next
smallest action is to split lint and behavioral work into two required jobs before
adding the larger exact or control matrices.

Go only if full discovery still contains 131 tests, fast exclusion equals the checked-in
slow-node manifest, every required item appears once, ten warm runs meet the 60/75
second p50/p95 budget, and full integration surfaces remain direct failures.
Stop if a test disappears from both surfaces or if the required lane exceeds 90 seconds
twice on the same revision without queue evidence.

## Spike 1: Job-Level GitHub Actions Parallelism

The steady-state Linux design is a matrix.
The aggregator waits for every required matrix result and fails unless every result
succeeds.

| Job group | Shards | Target work | Selection contract |
| --- | ---: | ---: | --- |
| `pytest-core` | 1 | 10–15s | All non-exhaustive nodes exactly once |
| `pytest-exact` | 6 initially | ≤45s each | Checked-in node-id LPT manifest |
| `negative-controls` | 4 | ≤45s each | Deterministic control-id manifest |
| `validation` | 4 | ≤45s each | Canonical validator-step manifest |
| `packing-required` | 1 aggregator | <5s | All prerequisites succeeded |

The 15 work jobs run concurrently.
At about 55 seconds including setup, their 13.75 runner-minutes are close to the current
13.57 runner-minutes spent on one 378-second Linux job plus one 436-second macOS job.
Existing compute is spent in parallel instead of serially and twice across operating
systems.

The four validation shards are:

- `validation-soundness`: soundness perimeter with two inner workers;

- `validation-history-quality`: historical, SVG, and Python quality with three outer
  workers;

- `validation-exact`: small-n, Trump cones, independent LP, and schemas; and

- `validation-remainder`: every remaining ordinary step.

The manifest proves that their disjoint union is the canonical ordinary-step set.
Pytest and controls are excluded because dedicated jobs own them.

The exact suite needs duration-balanced node ids, not file-level shards.
After Spike 2, collapse exact assurance to one job if its p95 stays under 45 seconds.

The control runner needs `--format json`, deterministic `--shard-index` and
`--shard-count`, a checked-in longest-processing-time-first assignment, and a test that
the shard union equals all 62 ids with no duplicates.
Use one worker inside each of four jobs first.

Go after ten fixed-revision dispatches if every work job has p95 at most 50 seconds,
end-to-end p50 at most 60 seconds, end-to-end p95 at most 75 seconds, and queue p95 at
most 20 seconds. Reconsider fan-out if runner-minutes exceed 2.5× without at least a 3×
wall improvement.

## Spike 2: Exact Row-Jet Reuse

Implement an immutable `RowJetInventory` or equivalent narrow value in
`cases/n5/minus_w_row_jets.py`:

1. Build active rows once per `NumberField` identity and stratum.

2. Materialize both validated owner views from that inventory.

3. Pass the inventory into stress and path evaluation.

4. Reuse one construction across the three stress velocities.

5. Return fresh mappings or immutable views.

6. Keep a cold, no-reuse path for assurance and profiling.

Do not use an unbounded `@cache` that retains stateful field instances or returns a
mutable dictionary.

Compare three cold and five warm samples.
Require exact ordered labels, source keys, values, gradients, every 15×15 Hessian, owner
projections, stresses, sheet values, and scale records.
Distinct fields must never share elements; incompatible-field and asymmetric-Hessian
failures remain active; mutating a returned view cannot affect a later result.

The profile predicts 38 constructions falling to six, removing about 182 seconds and
putting the exact group near 30–45 seconds.
Keep the implementation if warm median is at most 45 seconds, p95 is at most 55 seconds,
and all guards match.
Stop if the group exceeds 60 seconds or any serialized coefficient changes.

## Spike 3: Negative-Control Sharding

First give the full/integration control step a dedicated two-worker setting.
Do not raise the shared inner-worker count.
Three paired runs must return the same ordered 62 ids, diagnostics, restoration state,
and timeout/interruption behavior.
Keep two workers if median is at most 105 seconds and the outer gate does not regress.

Then add four deterministic job shards.
Prove exact union, empty intersection, expected mutation-to-diagnostic matching, private
source trees, fresh bytecode caches, bounded cleanup, and clean source bytes after every
outcome.

Keep the design only if every shard p95 is at most 45 seconds.
If one checker family remains a long tail, batch the 49 repeated checker invocations
behind a checker-core API instead of adding more inner workers.

## Spike 4: Revision-Keyed Validation Receipt

Add one sentinel keyed by:

```text
source identity
+ dirty-state identity
+ selected surface
+ platform
+ worker settings
+ resolved program and normalized arguments
```

Normalize an equivalent `uv run --directory` call and resolved working-directory call to
one logical key. Never merge different surfaces, revisions, platforms, worker settings,
or dirty states.

One agent owns a key and publishes start, heartbeat, terminal status, timings, and
artifact identity. Other agents may reuse only that exact key.
A failed, canceled, stale, or incomplete receipt never satisfies a later request.

Keep the sentinel if a comparable research slice reduces duplicate validation
command-seconds by at least 50%, blocked wait is at most 30 seconds when the coordinator
has independent work, and deliberate failure injection reaches every consumer.

## Sub-Agent Efficiency Experiment

Loop 2 already used substantial delegation.
The next experiment changes task shape, not simply agent count:

- at most three concurrent leaf agents;

- one immutable revision and one named artifact or read-only question per assignment;

- checkpoint by minute 12 and final response by minute 20;

- at most one corrective follow-up per assignment;

- one parent integration pass after the wave; and

- validation owned by the revision-keyed sentinel.

Keep the design if follow-ups fall from 65 to at most 20, elapsed first-start to
last-end falls from 227 minutes to at most 170, the final tail is at most 20 minutes,
and total agent-time stays within 10% of 257 minutes with the same retained artifacts
and checks.

Model routing is a separate paired experiment.
Randomize 12 matched inventory, log, schema, or formatting tasks between
`gpt-5.6-sol/xhigh` and a lower-cost `terra` or `luna` setting.
Use the same validator and a blinded integrator.
Approve the lower route only if paired median valid latency is at least 30% lower,
rejection or correction rises no more than five percentage points, and checks are
identical. Mathematical derivation, adversarial review, and final integration remain on
frontier reasoning.

## Recurring Efficiency Infrastructure

Extend the scanner and add:

```shell
uv run --frozen python -m devtools.packing_efficiency report \
  --codex-root <task-id> \
  --github-workflow packing-validation \
  --local-receipt <path>
```

The command consumes `CodexEfficiencyRollup/v2`, adds normalized command keys and
critical-path versus overlap attribution, fetches GitHub queue/job/step timings, reads
local validation receipts, emits versioned JSON plus Markdown, compares p50 and p95 with
the prior fixed-revision sample, and opens or renews W5 work for a 20% regression or
hard-budget miss.

Run it after every clocked research session longer than one hour, after a validation
surface moves by at least ten seconds, weekly against GitHub history, and before closing
a W5 optimization bead.
Commit only reviewed aggregates, never raw prompts, private JSONL, hidden reasoning, or
access tokens.

## Assurance Contracts

- Every test node, validator step, and control id belongs to exactly one declared
  surface.

- The aggregator fails when a prerequisite is skipped, canceled, or failed.

- Full and fast discovery are checked against manifests.

- An invoked macOS check is direct and blocking.

- Integration, main, scheduled, and manual assurance retain full Linux, full exact, all
  controls, full macOS, and deep golden.

- Structured artifacts preserve ordered ids, diagnostics, status, and source identity.

- Caches include every semantic input and retain a cold path.

- A speed claim uses repeated samples of one unchanged revision.

## Framework Fit and Limits

AgentSession/v2 already classifies this work.
Sessions use W5 `efficiency-loop` with focus `efficiency`. Each follow-up session gets
its own sequential log, and bounded delegates are recorded there.

AgentSession/v2 is intentionally too small for thousands of model events, recursive task
intervals, token histories, CI samples, and per-command timings.
Those belong in versioned scanner and validation receipts linked from the session.
Expanding the session record to contain raw telemetry would make handoffs noisy and risk
committing private logs.

GitHub Actions cannot access local `~/.codex/sessions`. Weekly CI can measure GitHub
surfaces; a local post-session command must produce the scrubbed Codex aggregate.
The repository also has no recurring efficiency scheduler yet; `think-xuk8` owns that
gap.

## Implementation Checklist

- [x] Deliver the recursive Codex scanner and initial loop review (`think-ma71`).

- [x] Correct native timing, frozen cutoffs, compaction counts, and legacy replay
  ownership (`think-lpum`, `think-p0bs`, and `think-oi60`).

- [x] Profile 24 CI runs, current exact tests, negative-control worker counts, and both
  named Codex loops (`think-vcr4`).

- [x] Implement and locally validate the fast required lane, exact-module marker
  contract, and aggregator (`think-b784` under `think-l7hi`).

- [ ] Land GitHub Actions matrices and union/disjoint tests (`think-l7hi` and
  `think-rthe`).

- [ ] Land immutable row-jet reuse and before/after receipts (`think-kdil`).

- [x] Give the full negative-control step its measured dedicated two-worker setting
  (`think-b784` under `think-rthe`).

- [ ] Land four deterministic negative-control CI shards (`think-rthe`).

- [ ] Land canonical validation receipts and sentinel (`think-3mkx`).

- [ ] Run the bounded leaf-agent and model-routing experiments (`think-5zgv`).

- [ ] Add the joined recurring report and regression trigger (`think-xuk8`).

- [ ] Run ten fixed-revision CI samples and publish the p50/p95 decision.

## References

- [Dated efficiency review](../../reviews/review-2026-08-25-research-loop-efficiency.md)

- [Development guide](../../../../development.md)

- [Workflow contracts](../../../../SYNOPSIS.md#workflow-entry-contracts)

- [Agent-session guide](../../../../campaign/agent-sessions/README.md)

- [Prior engineering efficiency review](../../reviews/review-2026-08-23-engineering-loops-and-efficiency.md)

- [Current PR CI receipt](https://github.com/jlevy/thinking-scratchpad/actions/runs/32926510669)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
