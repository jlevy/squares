# Agenda 025 T+2-to-T+4 Fractional Manager Gate

Status: **recovery process terminal; BC-232 remains provisional; no bridge, leg 03, or
joint T+4 crossing is authorized.**

Role: fractional manager `/root/dilation_bound_promotion`, `max` reasoning\
Cell: BC-232 under exp-070 and H-064\
Recovery source baseline: `9a93b2ea0b34701304e311aa080ddd31d3c70e88`\
Raw-output preservation commit: `0b6ca57627887863a29ad54f2fbbebb8e4690800`\
Read-only inspection head: `f9ba790a2a60b990d20261cc2645595d78740dcc`

This packet occupies Agenda 025’s required T+4 manager path, but it is not an active
minute-240 receipt. The credited shared clock stands at active minute `124:14` and
remains held for recovery and integration.
The numerical process continued during the credit interruption; its measured process
cost belongs to BC-232, while that interval does not establish active agent time.

## Recovery Identity and Clock Boundary

The coordinator launched the one authorized fresh-stem recovery from `packing/` at
`2026-09-06T11:47:39Z` in unified execution session `36339`, as uv PID `72209` and
Python 3.14.7 PID `72291`. It used the literal command in
`bc-232-leg-02-microreceipt-001.md`: the retained leg-01 state, unchanged scientific
arguments, `--stop-on-covering-below-n`, a configured `--minutes 101`, and the
`bc-232-leg-02-recovery-01` output stem.
The command exited zero after five iterations and stopped as
`deadline reached before iteration 5`.

The last observation before the credit interruption was `2026-09-06T11:50:09Z`, at
active minute `124:14`. The first recovered coordinator observation was
`2026-09-06T16:07:05Z`. The user excluded that conservative 4-hour, 16-minute, 56-second
interval from the wall allowance.
The amended eight-hour target is `2026-09-06T20:39:32Z`; the amended ten-hour outer
boundary is `2026-09-06T22:39:32Z`. Recovery and integration after the first observation
do not backdate the shared clock.

## Retained Outputs

The four recovery outputs parse as strict finite JSON where applicable.
Commit `0b6ca576` preserves their complete contents in this directory:

| Output | Bytes |
| --- | ---: |
| `bc-232-leg-02-recovery-01.log` | 1,692 |
| `bc-232-leg-02-recovery-01-state.json` | 5,753,682 |
| `bc-232-leg-02-recovery-01-summary.json` | 5,246 |
| `bc-232-leg-02-recovery-01-family.json` | 93,719 |

The cumulative comparison uses the unchanged leg-01 evidence at the source baseline
`9a93b2ea`, in the same directory:

```text
bc-232-leg-01.log
bc-232-leg-01-state.json
bc-232-leg-01-summary.json
bc-232-leg-01-family.json
```

The recovery state contains 30,413 sites, 14,441 rows, and all five iteration records.
It was serialized before iteration 4’s selected additions: its last record has
`added: 0`, an empty note, and an empty top-level stop, while the terminal summary
records 62 selected orbits and the deadline stop.
This is the runner’s pre-addition checkpoint boundary, not evidence of a restart or
corrupted output.

## Process Cost and Cooperative Overrun

The summary’s timing scope begins at the runner’s main entry and ends immediately before
summary serialization.
It excludes import and uv startup, the final summary write, and teardown.

| Measurement | Seconds | Clock form |
| --- | ---: | ---: |
| Loop wall | `7172.188873416046` | 1:59:32.188873 |
| Driver wall before summary | `7278.912243166007` | 2:01:18.912243 |
| Loop CPU | `7140.585076` | 1:59:00.585076 |
| Driver CPU before summary | `7247.051695` | 2:00:47.051695 |

The state and log mtimes are `2026-09-06T13:47:13.687606Z` and `2026-09-06T13:47:14Z`.
The family and summary mtimes are approximately `2026-09-06T13:48:58.996Z`. From the
second-resolution launch receipt to the summary mtime, observed elapsed wall time is
approximately 7,280 seconds, or 2 hours 1 minute 20 seconds.

The configured 101-minute value equals 6,060 seconds.
Loop wall exceeded it by `1112.188873416046` seconds, and recorded driver wall exceeded
it by `1218.912243166007` seconds.
The setting is therefore a cooperative deadline, not a hard process cap.
The runner completed the current operation and terminal exact-family verification before
it wrote the final outputs.
This packet reports the runner’s two measured CPU fields at their recorded scope; it
does not infer final OS CPU from wall time.

### Four-CPU-Hour Budget

Leg 1’s last live process sample supplies only a CPU lower bound of `6290.95` seconds.
Adding recovery’s measured driver CPU gives a cumulative lower bound of `13538.001695`
CPU seconds. This deliberately omits leg 1’s unobserved terminal tail, the failed
original leg-02 process, recovery startup, summary serialization, and teardown.

Against the frozen 14,400-second budget, at most `861.998305` CPU seconds, or 14 minutes
21.998305 seconds, can remain.
The literal 30-minute leg 03 would exceed that upper bound by at least `938.001695`
seconds. The earlier plan to retain a 30-minute final leg is no longer compatible with
the frozen four-CPU-hour cap.
This manager gives leg 03 a **NO-GO**; the coordinator must dispose the budget
inconsistency before any prospective continuation.

## Cumulative Bracket

The frozen interpretation takes the maximum exact `best_scaled_total` as the lower
endpoint and the smallest `rows_objective` among rows with `rows_converged: true` as the
computational upper endpoint.

| Quantity | Leg 01 | Recovery 01 | Cumulative |
| --- | --- | --- | --- |
| Exact lower endpoint | `21342289572/2055263195` at iteration 10 | `21101380004/2114368269` at iteration 0 | `21342289572/2055263195 = 10.38421240837721516246...` |
| Row-converged upper endpoint | `11.055616942909783` at iteration 0 | None | `11.055616942909783` |

The cumulative width is `0.67140453453256783753999204953407439382...`. Relative to the
retained initial width `1.147711347927249`, this is a `41.500575406428...` percent
reduction. It is below the declared threshold `0.86078351094543675`, but the rule also
requires the full four-CPU-hour evidence budget.
The exact terminal CPU total is unavailable, so this packet does not issue the
25-percent routing verdict.

All five recovery row solves were unconverged:

| Iteration | `rows_objective` | `rows_converged` |
| ---: | ---: | --- |
| 0 | `11.003820224719098` | `false` |
| 1 | `10.999999999999936` | `false` |
| 2 | `11.00000000000002` | `false` |
| 3 | `10.99999999999993` | `false` |
| 4 | `11.000000000000014` | `false` |

The two displayed floats below eleven do not open the covering bridge and prove no
bound.

## Exact Family Replay

The manager loaded the retained recovery family with `CeilingCertificate.from_record`
and reran the existing `verify_ceiling` checker under the project’s Python 3.14
interpreter. The replay returned:

| Field | Exact replay |
| --- | --- |
| `proved` | `false` |
| Failures | `K3 total weight at least n` only |
| Total weight | `21101380004/2114368269` |
| Maximum depth | `1` |
| Arrangement vertices | `2607444` |
| Vertices decided exactly | `64` |
| Regime | `net`, D4-symmetric |

The exact maximum-depth guard passes, but total weight is below eleven.
The family does not close the one-body formulation.
The result reproduces the summary and family provenance fields exactly.

At `2026-09-06T16:17:42Z`, both reserved bridge paths remained absent:

```text
bc-232-leg-02-recovery-01-covering-candidate.json
bc-232-leg-02-recovery-01-covering-bridge-receipt.json
```

An elevated host process-table sample at `2026-09-06T16:15:41Z` found no live
`devtools.run_fractional_cutting`, `devtools.freeze_cutting_primal`, or matching
recovery-stem process.

## Manager Disposition

The recovery process and its four raw outputs are terminal.
BC-232 remains a **provisional, time-limited checkpoint**: it produced neither a safe
covering crossing nor a verified ceiling, and the full four-CPU-hour precondition cannot
be reconstructed from the available CPU evidence.
H-064 and exp-070 receive no new mathematical verdict.

No bridge, exactification, new search, leg 03, successor cell, or shared-record
promotion is authorized from this packet.
The coordinator owns the BC-232 budget and state disposition, the joint BC-220 gate,
tbd, indexing, commits, and pushes.
The shared research clock remains held at active minute `124:14`; this packet does not
claim T+4.

This manager created only
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/gate-hour-04.md`.
It did not edit the original microreceipt or raw outputs and made no tbd mutation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
