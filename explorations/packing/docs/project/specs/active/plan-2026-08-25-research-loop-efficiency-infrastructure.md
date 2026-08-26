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

The rollups come from `CodexEfficiencyRollup/v1`. Response envelope is not provider
inference latency. It includes dispatch, suspension, and gaps without explicit log
events. Timed model stream is the lower bound exposed by `Reasoning` and `AgentMessage`
event timing.

#### Research Loop 2 Frozen Snapshot

Root `01a03b2a-d50b-7582-8d78-be6d8ebb461d` was sampled at `2026-08-26T03:42:41.980Z`:

```text
parent active — 4h33m02s
├── response envelope — 2h28m34s (54.4%)
│   ├── timed model stream — 49m37s
│   └── unattributed response time — 1h38m57s
├── delegated-agent wait — 1h20m33s (29.5%)
│   ├── overlapped by active child work — 1h03m12s
│   └── no child active — 17m41s
├── commands — 36m16s (13.3%)
├── compaction — 7m10s (2.6%)
└── other explicit tools — 29s

recursive tree — 10 sessions
├── recursive agent-time — 9h11m11s
├── active union — 4h33m19s
└── concurrency overlap — 4h37m52s
```

The task used `gpt-5.6-sol/xhigh` for all 1,832 response events.
Its recursive response envelope was 6h19m12s and its timed model stream was 3h03m54s. It
recorded 235,313,516 input tokens, 229,095,936 cached input tokens, 807,418 output
tokens, and 298,261 reasoning tokens.
Input caching was 97.4%; context reloading is not the first target.

The first orientation fan-out was efficient: 11m22s of agent work completed in a 4m40s
active tail, saving about 6m41s versus serial execution.
The later broad trio was not balanced:

| Delegate | Active time | Turns |
| --- | ---: | ---: |
| R4 | 98m35s | 18 |
| R5 | 80m25s | 24 |
| Scope | 78m07s | 25 |

Together they used 257m07s of agent-time over a 140m26s active union.
There were 65 follow-up calls and 25 messages.
The last delegate finished 41 minutes after R4 and 42 minutes after R5. More broad
agents would increase integration load; shorter, revision-pinned leaf tasks are the
useful form of additional parallelism.

Repeated validation is also measurable:

| Repeated logical surface | Runs | Command seconds |
| --- | ---: | ---: |
| Full gate | 2 | 755.94 |
| Standard fast gate | 4 | 552.13 |
| Exact row group | 3 | 435.26 |

These totals require a canonical key because equivalent calls sometimes differ only by
`--directory` spelling.

#### Research Loop 1 Old

Root `01a02fc2-081b-72b1-999a-cd5550629c0c` recorded:

| Measure | Value |
| --- | ---: |
| Parent wall envelope | 45h28m27s |
| Parent active | 37h02m09s |
| Parent inactive | 8h26m18s |
| Parent response envelope | 31h24m25s |
| Parent commands | 3h08m46s |
| Parent delegated-agent waits | 2h23m25s |
| Recursive sessions | 139 |
| Recursive agent-time | 57h07m47s |
| Active union | 37h02m09s |
| Concurrency overlap | 20h05m37s |
| Turns | 390: 27 parent, 363 child |
| Compactions | 96: 77 parent |

It recorded 12,889 response events, 1,604,316,923 input tokens, 1,561,282,816 cached
input tokens, 5,658,089 output tokens, and 2,071,303 reasoning tokens.
Cached inputs were 97.3%.

| Model | Thinking | Response events | Response envelope |
| --- | --- | ---: | ---: |
| `gpt-5.6-sol` | max | 9,907 | 42h06m |
| `gpt-5.6-sol` | xhigh | 1,168 | 4h06m27s |
| `gpt-5.6-sol` | high | 191 | 52m40s |
| `gpt-5.6-terra` | low | 849 | 1h40m02s |
| `gpt-5.6-terra` | medium | 199 | 26m46s |
| `gpt-5.6-luna` | low | 557 | 1h03m05s |
| `gpt-5.6-luna` | medium/max | 18 | 2m17s |

`gpt-5.6-sol` accounts for 87.4% of response events and 93.6% of response envelope.
Historical assignments are confounded by task role, so they do not prove that a lower
model would complete the same work faster or with the same correction rate.

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

4. Leave default and full discovery unchanged at all 124 tests.

5. Keep negative-runner unit tests, workflow contracts, selection manifests, schemas,
   lint, and cheap scientific smoke checks required.

6. Move the monolithic 62-control run and exhaustive exact group to integration, `main`,
   scheduled, and manual assurance until their shards meet the budget.

7. Replace job-name-specific branch protection with a stable `packing-required`
   aggregator.

Expected immediate effect: behavioral pytest falls from 251 seconds to about 15–20
seconds. The required validation step should finish within 35 seconds and the warm
workflow within 45–60 seconds.

Go only if full discovery still contains 124 tests, fast exclusion equals the checked-in
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

The command consumes `CodexEfficiencyRollup/v1`, adds normalized command keys and
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

- [x] Profile 24 CI runs, current exact tests, negative-control worker counts, and both
  named Codex loops (`think-vcr4`).

- [ ] Land the fast required lane, marker manifest, and aggregator (`think-l7hi`).

- [ ] Land GitHub Actions matrices and union/disjoint tests (`think-l7hi` and
  `think-rthe`).

- [ ] Land immutable row-jet reuse and before/after receipts (`think-kdil`).

- [ ] Land dedicated two-worker full controls and four CI shards (`think-rthe`).

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
