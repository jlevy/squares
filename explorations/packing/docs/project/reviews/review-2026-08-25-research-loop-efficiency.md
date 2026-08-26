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
The active loop-2 branch has no pull request and therefore no GitHub Actions wait.
That task still spent 7m18s on one local full gate, 3m53s across two local fast gates,
and 7m15s across three focused exact row-jet test invocations by the reviewed snapshot.
The exact-test group alone took 103–181 seconds per invocation.

Model and orchestration time are also material, but the logs do not support a single
honest “LLM latency” number.
Loop 2 exposes 2h48m26s of timed model streaming across its recursive task tree and a
further 2h58m43s of response-envelope time that cannot be assigned solely to inference.
Loop 1 is a legacy log: it exposes a 50h17m17s recursive response envelope but no
explicit stream timing.
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

[`codex_log_rollup.py`](../../../devtools/codex_log_rollup.py) reads Codex JSONL by root
task id, discovers descendants, removes inherited subagent history, and emits the
versioned `CodexEfficiencyRollup/v1` JSON contract or a compact Markdown tree.
Synthetic fixtures cover current and legacy history, live and interrupted turns,
model/thinking splits, token totals, stream bounds, command polling, and recursive
overlap.

The clocks are intentionally different:

| Clock | Interpretation |
| --- | --- |
| Parent active | Union of active turns in the coordinating task |
| Recursive agent-time | Sum of all parent and descendant active intervals; parallel work adds agent-seconds |
| Active union | Union of all parent and descendant intervals without double counting |
| Parallel overlap | Recursive agent-time minus active union |
| Response envelope | Active client time after explicit tools and compaction; an upper bound, not server inference latency |
| Timed model stream | Lower bound from explicit `Reasoning` and `AgentMessage` item timing |
| Unattributed response | Response envelope outside those timed stream items |

The scanner counts token-usage events as the most stable client-log proxy for model
responses. That count is not a provider request counter.
Legacy response intervals can include client suspension, dispatch, and uninstrumented
gaps. A live turn ends at its last event and is therefore a lower bound.

The first implementation found and removed one legacy replay artifact before these
figures were accepted: three child logs contained 101 compressed parent responses and
14,641,508 input tokens after the best legacy history marker.
Those replayed turns lacked the child-owned `turn_context` and are now excluded by a
regression-tested ownership rule.

## Loop 1: Full Historical Rollup

The final log snapshot is `2026-08-25T15:22:28.182Z`. The root contains 27 turns: 26
complete and one interrupted.

### Parent critical path

| Parent clock | Time | Share or note |
| --- | ---: | --- |
| Wall envelope | 45h28m26.916s | Includes 8h26m17.517s between active turns |
| Active time | 37h02m09.399s | Critical-path denominator |
| Response envelope | 31h24m24.746s | 84.8% of active time; legacy stream timing unavailable |
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

The recursive tree recorded 12,889 token-accounted responses and a 50h17m16.858s
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
| `gpt-5.6-sol` | `max` | 9,907 | 42h06m00.075s | 1,327,678,859 | 1,297,181,312 | 4,605,652 | 1,741,424 |
| **Total** |  | **12,889** | **50h17m16.858s** | **1,604,316,923** | **1,561,282,816** | **5,658,089** | **2,071,303** |

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

This baseline freezes the live tree at `2026-08-26T02:52:45.919Z`. The root had two
complete turns and one live turn, so later work is intentionally absent.

### Parent critical path

| Parent clock | Time | Note |
| --- | ---: | --- |
| Active time | 3h48m27.006s | Live lower bound |
| Response envelope | 2h05m00.179s | Upper-bound client response time |
| Timed model stream | 38m07.764s | Explicit lower bound |
| Unattributed response | 1h26m52.415s | Must not be labeled model inference |
| Delegate waits | 1h08m30.478s | Most delegates overlap other active work |
| Commands | 29m57.422s | Local validation and exact probes dominate |
| Context compaction | 4m33.160s | Timed compaction interval |
| Other explicit tools | 25.767s | Agent control, extension, file change, and MCP |

### Recursive task and model tree

All seven sessions used `gpt-5.6-sol/xhigh`.

```text
root                                  3h48m27s active; 875 responses
├── /root/workflow_orientation           3m00s active;  23 responses
├── /root/tooling_orientation             3m50s active;  20 responses
├── /root/frontier_orientation            4m32s active;  24 responses
├── /root/r4_derivation                 1h38m35s active; 295 responses
├── /root/r5_derivation                 1h20m25s active; 201 responses
└── /root/r4_r5_scope_audit             1h17m30s active; 230 responses

recursive agent-time                  8h16m19s
active union                          3h48m27s
parallel overlap                      4h27m52s
```

The tree recorded 1,668 responses, 213,736,812 input tokens, 208,243,712 cached input
tokens, 735,081 output tokens, and 272,394 reasoning-output tokens.
Its 5h47m08.677s response envelope splits into 2h48m26.055s of timed model stream and
2h58m42.622s unattributed.

The 4h27m52s overlap shows why parent `agent_wait` cannot be treated as pure waste.
The three long audits ran concurrently and delivered distinct derivation, mutation, and
scope checks. The optimization target is idle tails, duplicate integration, and repeated
orientation, not independent review itself.

The active task repeatedly reloads large workflow, skill, and handoff contracts after
continuations. Token caching makes that cheaper than an uncached prompt, but it does not
remove client latency, context management, or the model work needed to reconstruct the
active slice. A compact freshness-checked resume packet is therefore a measured W5
candidate.

### Local command bottlenecks

The largest parent commands were:

| Command class | Invocations | Total | Maximum |
| --- | ---: | ---: | ---: |
| Full `packing-validate --jobs 2 --inner-jobs 1` | 1 | 7m17.813s | 7m17.813s |
| Exact row-jet pytest group | 2 | 5m31.946s | 3m00.993s |
| Fast `packing-validate` | 2 | 3m53.285s | 3m29.045s |
| Reordered exact pytest group | 1 | 1m43.314s | 1m43.314s |
| Two largest exact inline diagnostics | 2 | 1m54.136s | 58.343s |
| Combined exact pytest and fast gate | 1 | 56.376s | 56.376s |

The exact group contains 17 tests.
Repeated construction through `owner_row_jets()` and `active_row_jets()`, dense exact
15×15 Hessians, and repeated field/symmetry validation are the first profiling targets.
That diagnosis is a code-path hypothesis, not yet an accepted optimization.

The loop-2 branch has no pull request as of this review.
No GitHub Actions run or CI-watch interval appears on its critical path.
CI still matters because every eventual integration pays the same slow workflow and
because local full and fast commands execute much of the identical surface.

## CI Baseline

The workflow in `.github/workflows/packing-validation.yml` runs on every packing pull
request and push to `main`. It starts two jobs:

- Linux runs the complete ordinary gate with `--jobs 2 --inner-jobs 1`.
- macOS repeats that complete gate with the same worker settings, then directly runs the
  focused deep golden.

Across the latest twelve successful runs at the review snapshot, end-to-end duration
was:

```text
4:50, 4:52, 4:53, 5:00, 5:19, 5:45,
5:58, 6:12, 6:15, 6:34, 7:02, 7:10
```

The median is 5m51.5s. Hosted-runner timing should be trended and budgeted, not turned
into a brittle functional assertion.

[Run 32912699602](https://github.com/jlevy/thinking-scratchpad/actions/runs/32912699602)
is the representative step-level receipt:

| Job or step | Time |
| --- | ---: |
| Linux job | 4m37s |
| Linux validation step | 4m27s |
| macOS job | 4m46s |
| macOS full validation | 3m11s |
| macOS focused deep golden | 1m16s |

The Linux validator reported 266.24 seconds total.

| Linux validation step | Time |
| --- | ---: |
| Negative controls | 183.81s |
| Soundness perimeter | 53.63s |
| Historical regressions | 29.73s |
| Deterministic SVG | 19.28s |
| Python quality | 19.00s |
| Trump cones | 16.00s |
| Pytest | 13.38s |
| Schema validation | 11.64s |

The macOS full gate spent 134.63 seconds on negative controls, 32.11 seconds on the
soundness perimeter, 19.00 seconds on historical regressions, 14.91 seconds on SVG,
12.21 seconds on pytest, 11.88 seconds on Trump cones, 11.75 seconds on Python quality,
and 8.74 seconds on schemas.

The mutation runner already supports a thread pool through `PACK_JOBS`, but CI forces
`--inner-jobs 1`. All 65 controls therefore traverse private snapshots serially on both
architectures. This is the largest high-confidence performance opportunity because the
accepted contract can be compared control-for-control under candidate worker settings.

The current macOS lane has caught real problems.
D-272 and D-273 show why a portability lane must remain direct and blocking whenever it
runs. D-320 was a macOS-only deep-golden failure caused by YAML wrapping; semantic YAML
comparison and a dedicated regression now protect that class.
Those facts support a selected portability lane, not deletion of macOS assurance and not
duplication of every platform-neutral check on every pull request.

## Prioritized Efficiency Work

| Priority | Change | Evidence | Preserved guard | Acceptance target |
| --- | --- | --- | --- | --- |
| P0 | Required Linux PR fast lane with structured timing | Successful CI p50 5m51.5s; every PR waits for two full jobs | Fast surface, workflow-contract tests, visible later full assurance | Warm p50 ≤60s, p95 ≤90s |
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

1. `CodexEfficiencyRollup/v1` for named root tasks and their recursive descendants;
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
