# Review: Square Packing Research-Loop Efficiency

**Date:** 2026-08-25

**Author:** Codex, for the project maintainers

**Status:** Complete W5 baseline and prioritization record; loop 2 is a live-log
snapshot, not a terminal task receipt

**Reviewed tasks:** Codex task `01a02fc2-081b-72b1-999a-cd5550629c0c`, titled “Square
packing research loop 1 (old),” and task `01a03b2a-d50b-7582-8d78-be6d8ebb461d`, titled
“Square packing research loop 2.”

This is a W5 `efficiency-loop` review with primary focus `efficiency`. It measures the
existing workflow and proposes implementation changes that preserve its scientific,
validation, and record contracts.
It is not a W4 process review.

## Verdict

The required feedback path is too slow, and CI is one of its largest reusable costs.
The current workflow spends about five to seven minutes on every successful packing CI
run because Linux and macOS both execute the full ordinary gate, while macOS also runs
the deep golden again.
The largest step is the 65-control mutation surface, forced to one inner worker on both
hosts.

CI is not the only critical-path problem.
By the corrected frozen loop-2 snapshot, the parent had spent 1h05m55s in commands,
including at least 41m33s of validation and pytest work, and 8m12s waiting for CI. Exact
row-jet groups took 103–181 seconds per invocation, while two ordinary local full gates
totaled 12m36s.

Model and orchestration time are also material, but the logs do not support a single
honest “LLM latency” number.
Loop 2 exposes 3h44m03s of timed model streaming across its recursive task tree and a
further 3h36m24s of residual response time that cannot be assigned solely to inference.
Recorded first-token wait is only 8m01s. Loop 1 is a legacy log: it exposes a 50h17m17s
recursive response envelope but no explicit stream timing.
Any optimization plan that labels either entire envelope as provider inference would
overstate the evidence.

The implementation order is:

1. emit comparable timing artifacts and establish a required Linux PR fast lane;

2. profile and parallelize the negative-control bottleneck under the existing mutation
   and restoration contract;

3. move macOS from a duplicate every-PR full gate to a blocking selected portability
   lane on integration, scheduled, manual, and portability-sensitive triggers;

4. remove repeated exact symbolic row-jet construction under exact equivalence and
   invalidation tests; and

5. use the recursive Codex rollup for recurring W5 reviews of model allocation, context
   reload, delegate tails, local gates, and CI together.

The corresponding staged design is the
[research-loop efficiency plan](../specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md).

## Measurement Contract

[`codex_log_rollup.py`](../../../packing/devtools/codex_log_rollup.py) reads Codex JSONL
by root task id, discovers descendants, removes inherited subagent history, and emits
the versioned `CodexEfficiencyRollup/v2` JSON contract or a compact Markdown tree.
Synthetic fixtures cover native duration and first-token fields, missing and invalid
telemetry, frozen live cutoffs, current and legacy compaction, compressed legacy replay,
live and interrupted turns, model/thinking splits, token totals, command polling, and
recursive overlap.

The clocks are intentionally different:

| Clock | Interpretation |
| --- | --- |
| Parent active | Union of active turns in the coordinating task |
| Recursive agent-time | Sum of all parent and descendant active intervals; parallel work adds agent-seconds |
| Active union | Union of all parent and descendant intervals without double counting |
| Parallel overlap | Recursive agent-time minus active union |
| Response envelope | Active client time after explicit tools and compaction; an upper bound, not server inference latency |
| Timed model stream | Lower bound from explicit `Reasoning` and `AgentMessage` item timing |
| Recorded first-token wait | Sum of native `time_to_first_token_ms` for the first response of completed turns |
| Residual response | Envelope outside timed stream and recorded first-token wait; not provider inference |
| Native turn duration | Client `duration_ms`; reconciled to the matching event interval and never used for overlap |

The scanner counts token-usage events as the most stable client-log proxy for model
responses. That count is not a provider request counter.
Legacy response intervals can include client suspension, dispatch, and uninstrumented
gaps. A live turn ends at its last event and is therefore a lower bound.
Scan start is the default cutoff; `--through` makes a live sample reproducible.

The v2 correction found a replay that survived the first ownership rule because it had a
copied `turn_context`. Its client duration was 14,051.726 seconds while the local replay
interval was 86 milliseconds.
Legacy subagent turns with a native-duration drift greater than max(1 second, 5%) are
now excluded and counted.
Loop 1’s recursive native duration then reconciles to its matching intervals within
1.101 seconds.

## Loop 1: Full Historical Rollup

The final log snapshot is `2026-08-25T15:22:28.182Z`. The root contains 27 turns: 26
complete and one interrupted.

### Parent critical path

| Parent clock | Time | Share or note |
| --- | ---: | --- |
| Wall envelope | 45h28m26.916s | Includes 8h26m17.517s between active turns |
| Active time | 37h02m09.399s | Critical-path denominator |
| Response envelope | 31h24m24.746s | 84.8% of active time; legacy stream timing unavailable |
| Recorded first-token wait | 4m16.530s | 0.23% of response envelope |
| Commands | 3h08m46.361s | 8.5% of active time |
| Delegate waits | 2h23m24.870s | 6.5% of active time; some delegates ran concurrently |
| Other explicit tools | 5m33.422s | Agent control, extension, file change, and MCP |
| Context compactions | 77 events | Legacy logs do not expose a reliable duration |

The 8h26m inactive gap is task suspension between turns, not a gate or model call.
It should not be included in an edit-to-signal service-level target.

### Recursive task tree

The root has 138 direct child sessions and no grandchildren in the discovered logs.

```text
loop 1 root: 37h02m09s parent active
└── 138 child sessions
    ├── recursive agent-time: 57h07m47s
    ├── active union:          37h02m09s
    └── parallel overlap:      20h05m37s
```

The equality between parent active and active union means the child work stayed inside
the coordinating task’s active envelope.
The additional 20h05m37s is useful parallel work or parallel overhead; it is not another
20 hours of wall-clock delay.

The longest child sessions were:

| Agent path | Active time | Model/thinking signal |
| --- | ---: | --- |
| `/root/h010_tooling_design` | 2h19m35s | Predominantly `gpt-5.6-sol/max` |
| `/root/h010_source_reconstruction` | 1h59m28s | Predominantly `gpt-5.6-sol/max` |
| `/root/h041_repair_checker` | 1h07m46s | `gpt-5.6-sol/max` |
| `/root/h026_exact_branch_audit` | 48m54s | `gpt-5.6-sol/max` |
| `/root/d168_mechanical_check` | 30m57s | `gpt-5.6-terra/low`; 7m36s commands and 2m26s wait |
| `/root/pr24_process_review` | 30m45s | `gpt-5.6-sol/max` |
| `/root/h026_tooling_inventory` | 28m00s | `gpt-5.6-sol/max` |
| `/root/pr24_schema_review` | 27m37s | `gpt-5.6-sol/max` |
| `/root/overnight_operations_audit` | 26m07s | `gpt-5.6-sol/xhigh` |
| `/root/validation_timeout_policy_audit` | 24m47s | `gpt-5.6-sol/high` then `max`; 6m38s wait |

The two longest parent turns lasted 7h31m15s and 7h21m56s. Their response envelopes were
6h01m21s and 6h38m32s; explicit delegate waits were 39m22s and 29m08s, and commands were
49m24s and 13m32s. Large multi-hour turns make compaction, repeated orientation, and
recovery harder to distinguish from useful reasoning.

### Model and thinking rollup

The recursive tree recorded 12,869 token-accounted responses and a 50h17m16.858s
response envelope. The tree has no explicit model-stream timing, so the envelope column
is the only available client-side upper bound.

| Model | Thinking | Responses | Response envelope | Input | Cached input | Output | Reasoning output |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `gpt-5.6-luna` | `low` | 557 | 1h03m05.497s | 27,551,726 | 25,110,528 | 122,808 | 17,864 |
| `gpt-5.6-luna` | `medium` | 10 | 1m45.168s | 549,248 | 425,472 | 4,889 | 1,699 |
| `gpt-5.6-luna` | `max` | 8 | 32.022s | 266,080 | 225,280 | 1,056 | 96 |
| `gpt-5.6-terra` | `low` | 849 | 1h40m01.609s | 72,390,896 | 69,798,400 | 253,024 | 59,841 |
| `gpt-5.6-terra` | `medium` | 199 | 26m46.328s | 11,198,153 | 10,672,384 | 72,230 | 13,898 |
| `gpt-5.6-sol` | `high` | 191 | 52m39.624s | 13,612,896 | 12,673,280 | 94,510 | 41,723 |
| `gpt-5.6-sol` | `xhigh` | 1,168 | 4h06m26.535s | 151,069,065 | 145,196,160 | 503,920 | 194,758 |
| `gpt-5.6-sol` | `max` | 9,887 | 42h06m00.075s | 1,324,511,414 | 1,294,203,520 | 4,597,727 | 1,738,313 |
| **Total** |  | **12,869** | **50h17m16.858s** | **1,601,149,478** | **1,558,305,024** | **5,650,164** | **2,068,192** |

The root itself used only `gpt-5.6-sol`: 7,772 `max` responses and 597 `xhigh`
responses. The recursive table shows that cheaper settings were used for some bounded
child work, but `sol/max` still accounts for 76.9% of responses and 83.8% of the
response envelope. That is a routing opportunity only for mechanical roles with explicit
contracts; it is not evidence to lower the model used for mathematical judgment or
integration.

### Commands and gates

The parent’s largest normalized command categories were:

| Category | Invocations | Timed segments | Total |
| --- | ---: | ---: | ---: |
| Legacy `test.sh` | 318 | 352 | 30m10s |
| Unattributed command polling | 0 | 172 | 27m55s |
| Full `packing-validate` | 37 | 74 | 22m34s |
| `tbd` | 931 | 934 | 22m32s |
| Explicit CI watch | 43 | 79 | 20m33s |
| Other `uv` commands | 152 | 157 | 7m49s |
| Inline Python diagnostics | 168 | 168 | 7m41s |
| Negative controls | 39 | 39 | 6m03s |
| BasedPyright | 64 | 64 | 4m44s |
| Repository and log inspection | 1,554 | 1,554 | 4m23s |
| Fast `packing-validate` | 16 | 16 | 3m50s |
| `git push` | 101 | 102 | 3m29s |
| Direct pytest | 41 | 41 | 2m02s |

Legacy polling reconstructs continuation segments when a process id is available.
The remaining 27m55s cannot be assigned to an originating command because the initial
call is absent from those log fragments.

CI watching is a clear repeated tax, but it is smaller than the combined local gate and
test surface. The 931 `tbd` calls and 1,554 inspection calls are individually cheap;
their larger cost is likely the model/context work surrounding them, which remains
inside the response envelope and cannot be timed independently from this log format.

## Loop 2: Live Research Rollup

This baseline freezes the live tree through `2026-08-26T05:05:06.988Z`. The root had ten
complete turns and one live turn, so later records are intentionally absent.

### Parent critical path

| Parent clock | Time | Note |
| --- | ---: | --- |
| Wall envelope | 6h00m48.180s | Includes 15m10.864s between active turns |
| Active time | 5h45m37.316s | Live lower bound and share denominator |
| Response envelope | 3h05m46.166s | 53.75%; upper-bound client response time |
| Timed reasoning and message stream | 1h08m55.964s | 19.94%; explicit lower bound |
| Recorded first-token wait | 57.566s | 0.28%; first response of ten completed turns |
| Residual response | 1h55m52.636s | 33.53%; must not be labeled model inference |
| Delegate waits | 1h24m14.954s | 24.38%; much overlaps child work |
| Commands | 1h05m54.949s | 19.07%; validation and CI dominate |
| Context compaction | 9m03.713s | 2.62%; nine timed current-format items |
| Other explicit tools | 37.534s | Agent control, extension, file change, and MCP |

### Recursive task and model tree

The recursive tree contains fourteen sessions:

```text
parent active                         5h45m37s
├── recursive agent-time             11h01m38s
├── active union                       5h45m37s
└── parallel overlap                   5h16m01s
```

All 87 completed recursive turns contain native duration and first-token fields.
Their reported duration totals 10h17m36.872s, differs from matching event intervals by
274 milliseconds, has a 3m00.586s p50 and 14m19.252s p95, and reaches 2h06m30.237s at
the maximum.

| Model | Thinking | Turns | Responses | Response envelope | First token | Reasoning | Message | Residual |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `gpt-5.6-sol` | `xhigh` | 83 | 1,981 | 6h43m49.749s | 7m34.859s | 2h58m49.460s | 17m46.222s | 3h19m39.208s |
| `gpt-5.6-sol` | `max` | 4 | 232 | 44m37.693s | 25.779s | 24m58.986s | 2m28.254s | 16m44.674s |

The tree records 2,213 response events, 288,786,067 input tokens, 280,945,664 cached
input tokens, 1,002,754 output tokens, and 370,981 reasoning-output tokens.
Native first-token wait is only 1.8% of the 7h28m27.442s recursive response envelope.
The larger targets are 3h44m02.922s of explicit stream work and 3h36m23.882s of residual
response time.

The 5h16m01s overlap shows why parent `agent_wait` cannot be treated as pure waste.
The three long audits ran concurrently and delivered distinct derivation, mutation, and
scope checks. The optimization target is idle tails, duplicate integration, and repeated
orientation, not independent review itself.

The orientation trio reduced 11m22s of agent work to a 4m40s tail.
The broad R4, R5, and scope trio used 257m07s of agent-time, received 65 follow-ups and
25 messages, left 86m35s with no long child active, and ended with a 41–42-minute
single-agent tail. More broad agents would add integration work; the next test uses
bounded leaf waves.

### Local command bottlenecks

The largest exact parent commands were:

| Command class | Invocations | Total | Maximum |
| --- | ---: | ---: | ---: |
| Full `packing-validate --jobs 2 --inner-jobs 1` | 2 | 12m35.939s | 7m17.813s |
| CI wait | 1 | 8m12.106s | 8m12.106s |
| Exact row-jet pytest group | 2 | 5m31.946s | 3m00.993s |
| Standard fast gate across parent and children | 4 | 9m12.127s | 4m53.372s |
| Reordered exact pytest group | 1 | 1m43.314s | 1m43.314s |
| Two largest exact inline diagnostics | 2 | 1m54.136s | 58.343s |

Session 017’s terminal gate on the loop-2-based branch passed in 284.29 wall-seconds.
Fast behavioral tests consumed 213.97 seconds and negative controls 138.04 seconds; the
outer scheduler overlapped them, so their sum is not the gate wall time.
The session-019 correction spike produced a second clean current-branch receipt: 327.66
wall-seconds, with 241.96 seconds in behavioral tests, 167.23 seconds in negative
controls, 41.60 seconds in the soundness perimeter, and 22.93 seconds in historical
regressions. That branch contains 62 controls, while representative CI run 32912699602
contains 65. The two receipts confirm the bottleneck but are not a strict before/after
comparison; revision and exact control inventory must travel with every benchmark.

The exact group contains 17 tests.
Repeated construction through `owner_row_jets()` and `active_row_jets()`, dense exact
15×15 Hessians, and repeated field/symmetry validation are the first profiling targets.
That diagnosis is a code-path hypothesis, not yet an accepted optimization.

Command categories are substring heuristics and may classify a composite command by an
embedded tool name. The exact totals above come from normalized commands.
Equivalent calls with different `--directory` spelling remain separate until the
revision-keyed surface fingerprint in `think-3mkx` lands.

## CI Baseline

The workflow in `.github/workflows/packing-validation.yml` runs on every packing pull
request and push to `main`. It starts two jobs:

- Linux runs the complete ordinary gate with `--jobs 2 --inner-jobs 1`.

- macOS repeats that complete gate with the same worker settings, then directly runs the
  focused deep golden.

Across the latest 24 successful workflows through run `32926510669`, end-to-end time
ranges from 290 to 440 seconds, with 346-second p50 and 430-second p95. Linux job p50 is
250.5 seconds; macOS job p50 is 342.5 seconds.
Queue p50 is three seconds on each host, so the executed work dominates.

Run `32926510669` records:

| Job or step | Time |
| --- | ---: |
| Linux job | 378s |
| Linux full validation | 366.21s |
| Linux pytest | 251.26s |
| Linux negative controls | 158.84s |
| Linux soundness perimeter | 53.88s |
| macOS job | 436s |
| macOS duplicate full validation | 318.28s |
| macOS focused deep golden | 95.89s |

Linux and macOS spent 684.49 runner-seconds repeating the ordinary gate, and macOS then
spent another 95.89 seconds on deep golden.
Removing macOS alone would leave the 378-second Linux result.

The current exact additions are the new Linux bottleneck.
Hosted Linux pytest rose from a 10.44-second historical p50 to 251.26 seconds.
A local profile assigns 212.53 seconds to thirty exact tests and only 14.95 seconds to
the other ninety-four.
Negative controls take 158.54 seconds at one worker, 98.17 at two, and 90.19 at four;
two workers are the local efficiency knee, while job-level shards are required for the
one-minute path.

The current macOS lane has caught real problems.
D-272 and D-273 show why a portability lane must remain direct and blocking whenever it
runs. D-320 was a macOS-only deep-golden failure caused by YAML wrapping; semantic YAML
comparison and a dedicated regression now protect that class.
Those facts support a selected portability lane, not deletion of macOS assurance and not
duplication of every platform-neutral check on every pull request.

## Prioritized Efficiency Work

| Priority | Change | Evidence | Preserved guard | Acceptance target |
| --- | --- | --- | --- | --- |
| P0 | Required Linux PR fast lane with structured timing | Successful CI p50 346s and p95 430s; every PR waits for two full jobs | Fast surface, workflow-contract tests, visible later full assurance | Warm p50 ≤60s, p95 ≤75s |
| P0 | Profile and parallelize negative controls | 183.81s Linux and 134.63s macOS; CI forces one worker | Exact 65 ids, mutations, diagnostics, restoration, stable output, timeouts | Reproducible same-result reduction sufficient for full Linux p50 ≤90s |
| P0 | Selected blocking macOS portability lane | Duplicate full gate plus 76s deep check on every PR | Direct failure when invoked; `main`, scheduled, manual, and explicit portability triggers | Remove macOS from unrelated PR critical path without losing integration evidence |
| P0 | Profile and reuse exact row-jet construction | Focused group repeats at 103–181s; exact probes at 20–58s | Exact rows, gradients, Hessians, field/symmetry failures, stresses, scales | At least 5× repeated-edit speedup after cold and invalidation checks |
| P1 | Emit joined Codex, local-gate, and CI efficiency records | Current evidence required manual joins | Versioned schemas, reviewed compact records, no raw private logs | One repeatable W5 report with medians and regression deltas |
| P1 | Freshness-checked resume packet | Repeated large contract reloads; high cached input totals | Definitive docs remain authoritative; packet fails closed on identity change | Lower retained-result latency without higher correction rate |
| P1 | Role-aware model/thinking allocation | Loop 2 is entirely `sol/xhigh`; loop 1 is dominated by `sol/max` | Frontier judgment and integration retain frontier settings | Mechanical-role improvement measured by latency and correction rate |
| P2 | Batch repeated record and inspection calls | Loop 1 has 931 `tbd` and 1,554 inspection calls | Same bead, ledger, and document outcomes | Fewer calls and context reloads at the same retained result |

The lane policy and the validator scheduler should be implemented separately.
That keeps the organizational change reversible while the underlying full gate becomes
faster for local, integration, and scheduled use.

## Recurring Efficiency Infrastructure

A recurring W5 sample should consume, not duplicate, these sources:

1. `CodexEfficiencyRollup/v2` for named root tasks and their recursive descendants;

2. structured `packing-validate` JSON with revision, platform, selected surface,
   workers, per-step seconds, and total seconds;

3. GitHub workflow/job timing artifacts for recent comparable runs; and

4. declared soft budgets and change from the prior median.

Run it after a clocked research session, after a material gate-surface change, and on a
scheduled sample. Open or renew W5 work only for a measured budget miss or regression
with a named equivalence guard.
Retain the compact reviewed summary and relevant run links; do not commit raw prompts,
reasoning text, complete JSONL logs, or private command histories.

The first reusable piece—the recursive Codex scanner—is implemented in this change.
The repository-level join, CI timing artifact, and scheduler are plan work, not claims
of completed infrastructure.

## Framework Fit and Limitations

AgentSession/v2 can record this session correctly as W5 `efficiency-loop` with focus
`efficiency`. It intentionally represents type through ordered workflow phases rather
than a separate free-form session-type field.
That is sufficient to make sessions classifiable and visible in the generated ledger.

One repository check currently assumes the numerically latest session always owns the
scientific cold-start handoff, even when the latest session is a non-scientific W5
cycle.
Session 017 must therefore repeat the unchanged `BC-010` / `think-1s0h` scientific
next action while separately naming its Efficiency backlog.
The duplication is harmless but shows that session logging and scientific handoff
selection are coupled more tightly than the general framework description suggests.

The session schema cannot encode thousands of model responses, recursive task trees,
overlapping agent-seconds, command excerpts, or token histories without becoming a
private telemetry archive.
The scanner JSON and this dated review are linked evidence instead.

Current Codex logs also do not provide:

- complete server-side inference latency;

- explicit stream timing for legacy tasks;

- an originating command for every orphaned legacy poll;

- a reliable duration for every legacy compaction; or

- a repository-native recurring scheduler and CI timing-history schema.

These limits constrain the labels used in this review.
They do not prevent a trustworthy W5 baseline or the CI, validation, and exact-test
changes above.

## Reproduction

From `explorations/packing/`:

```shell
uv run --frozen python -m devtools.codex_log_rollup \
  --sessions-root ~/.codex/sessions \
  --through 2026-08-26T05:05:06.988Z \
  --root-id 01a02fc2-081b-72b1-999a-cd5550629c0c \
  --root-id 01a03b2a-d50b-7582-8d78-be6d8ebb461d \
  --format markdown

uv run --frozen pytest -q tests/test_codex_log_rollup.py
uv run --frozen ruff check devtools/codex_log_rollup.py \
  tests/test_codex_log_rollup.py
uv run --frozen basedpyright devtools/codex_log_rollup.py \
  tests/test_codex_log_rollup.py
```

The Markdown command prints a recursive session → model → thinking tree by default.
Add `--include-turns` for session → turn → model → thinking detail, or use JSON for
programmatic aggregation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
