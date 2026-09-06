# BC-232 Leg-02 Microreceipt 001

Status: **terminal technical failure; bounded fresh-stem recovery authorized**

Role: fractional manager `/root/dilation_bound_promotion`\
Cell: BC-232 under `think-6yx2`, exp-070, H-064\
Authorized pre-launch head: `da00905e1deb3056cf7ae15b6b1786b81c93059c`\
Binding commit: `ff9cfe30c66017b8d29afec205111f4d6c83c4f0`\
Replacement authorization: `2026-09-06T11:31:09Z`\
Actual role restart: `2026-09-06T11:35:26Z`

## Active-Time Envelope

This receipt opened the at-most-30-active-minute slice from T+2 to T+2:30, portfolio
minutes 120 through 150. It did not backdate the shared clock: the floating reviewer’s
`2026-09-06T11:38:05Z` restart set the effective start.
The fixed wall authority began at `2026-09-06T08:22:36Z`, targets
`2026-09-06T16:22:36Z`, and ends at the outer deadline `2026-09-06T18:22:36Z`. This is a
partial continuation and promises no arrival at active minute 600.

Leg 02 carries a 105-minute maximum process-wall budget, at most one CPU thread, and the
unchanged BC-232 endpoint labels.
The exact packing-family lower endpoint and the row-converged floating covering endpoint
remain different quantities.
A float crossing proves no bound.

## Frozen Inputs

The pre-launch check at `2026-09-06T11:35:26Z` reproduced these SHA-256 values:

```text
431737c54034c97ed9fdd51bd2991852d793b96b56486df4cfe2c0e9b19f2e7c  bc-232-leg-01.log
f91999b452bf89f49e2d4cda9827efbf57623a4196688b5feba0819bc7e851e2  bc-232-leg-01-state.json
d8c50db8770b12d43baa6d9e2c7384a52a0f250f8cee26b6a036c99b3cb3350e  bc-232-leg-01-summary.json
4cfbdce5cb659d77d652c011854de74ddcad94c903eff30af07bbcb5d8d9cc3f  bc-232-leg-01-family.json
```

The warm input is
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json`
at SHA-256 `f91999b452bf89f49e2d4cda9827efbf57623a4196688b5feba0819bc7e851e2`. Its
retained exact lower endpoint is `21342289572/2055263195`; the only row-converged upper
endpoint is `11.055616942909783` from iteration 0.

## Fresh-Path and Process Receipt

At the same check, all six reserved paths were absent:

```text
bc-232-leg-02.log
bc-232-leg-02-state.json
bc-232-leg-02-summary.json
bc-232-leg-02-family.json
bc-232-leg-02-covering-candidate.json
bc-232-leg-02-covering-bridge-receipt.json
```

An elevated process-table read found no live `devtools.run_fractional_cutting` or
`devtools.freeze_cutting_primal` process.
The focused safe-stop and bridge controls had passed on the authorized head: 12 tests
passed in 0.46 seconds.
The literal leg-02 argv also parsed successfully under Python 3.14.7 without executing
the scientific command.

## Historical One-Shot Command

The manager launched this command exactly once from `packing/`:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 105 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --stop-on-covering-below-n \
  --warm campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-family.json
```

## Launch Identity

The command started once at `2026-09-06T11:36:42Z` in unified execution session `27576`,
as uv PID `64895` and Python 3.14.7 PID `64896`. A process-table sample at
`2026-09-06T11:36:59Z` found both processes live, with the Python worker in state `R`.
The runner reported `stop_on_covering_below_n: true` and reconstructed 27,277 sites,
3,495 orbits, and 13,000 rows from the frozen warm state.

At `2026-09-06T11:39:49Z`, the coordinator found both recorded PIDs absent.
The log existed at zero bytes, with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; the state, summary,
family, candidate, and bridge receipt were absent.
The process had not survived the manager turn.
No scientific iteration or endpoint was retained.
The original stem is a terminal technical failure and must not be reused.

The shared active clock ran from `2026-09-06T11:38:05Z` through the detection at
`2026-09-06T11:39:49Z`, then paused at active minute 121 minutes 44 seconds for process
recovery. The unaffected BC-241 review may finish its already authorized work but cannot
cross the joint gate.

## Bounded Fresh-Stem Recovery

`think-odk9` records the coordinator recovery gate.
At `2026-09-06T11:41:24Z`, all six paths with base `bc-232-leg-02-recovery-01` were
absent and no original process was live.
The recovery keeps every scientific input and parameter fixed, changes only the output
stem, and caps the new process at 101 minutes.
Even if the failed process survived for the entire launch-to-detection interval, the two
process walls together cannot reach the original 105-minute cap.

After this receipt is committed and pushed, the fractional manager must recheck the
fresh paths and acknowledge the recovery before the coordinator launches this command
once from `packing/`:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 101 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --stop-on-covering-below-n \
  --warm campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-recovery-01.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-recovery-01-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-recovery-01-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-recovery-01-family.json
```

If this process also fails operationally, retain the fresh stem and close BC-232 as a
technical failure; no second recovery is authorized.
The bridge, if a safe crossing occurs, uses the correspondingly fresh
`bc-232-leg-02-recovery-01-covering-candidate.json` and
`bc-232-leg-02-recovery-01-covering-bridge-receipt.json` paths exactly once.
Leg 03 remains unauthorized before BC-220.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
