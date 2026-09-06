# BC-232 Retained-State Fractional-Cutting Disposition

Status: **time-limited leg-01 checkpoint** under exp-070 and H-064. The one authorized
process is terminal; leg 2 was not launched before the landing.

Launch base: `c55726e1e885227f63110131c0a914665175ff89`\
Frozen preregistration: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`\
Cell: BC-232 (`think-gmdy`)\
Experiment: exp-070, H-064

## Launch Identity

The retained input
`packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json`
had SHA-256 `8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6`. The
runner reconstructed 12,761 sites, 1,657 orbits, and 9,868 rows against the
181-direction net.

From `packing/`, the manager launched exactly:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 105 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --warm campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json
```

It started at `2026-09-06T03:33:15Z` as uv PID 84153 and Python 3.14.7 PID 84154 in
execution session 83011. The command was never restarted or rebased.

## Frozen Interpretation

The lower endpoint is the maximum exact `best_scaled_total`. The computational upper
endpoint is the smallest floating `rows_objective` among iterations whose
`rows_converged` field is true.
These labels are not interchangeable.

A `verify_ceiling` family of exact total at least eleven closes this one-body method at
side `191/50`; it is not a lower-bound certificate.
A row-converged objective below eleven stops the lane and opens the declared covering
bridge on the preserved state; the float crossing itself proves no bound.
Neither event authorizes a rerun into the same stem.
The preregistered 25-percent width rule remains unavailable until the full four-CPU-hour
budget has been spent.

## Unused Leg-02 Continuation

The following command is the exact agenda-025 continuation with only the warm input and
four output stems advanced from leg 01 to leg 02. It has **not** been launched; all four
leg-02 paths remain absent, and only a post-landing coordinator gate may authorize it.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 105 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --warm campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-family.json
```

## T+2 Result

The original execution session exited zero after 14 iterations and stopped as
`deadline reached before iteration 14`. Its timed loop recorded `6560.285289000021`
seconds. From the second-resolution launch time `2026-09-06T03:33:15Z` to the terminal
file timestamp `2026-09-06T05:24:41Z`, observed command wall was approximately 6,686
seconds (111 minutes 26 seconds), including warm loading and terminal verification.

The final exact lower endpoint is iteration 10’s
`21342289572/2055263195 ≈ 10.384212408377215`. The frozen family contains 768 placements
and has exact maximum depth `1`. `verify_ceiling` reports `proved: false` solely because
`K3 total weight at least n` fails: the exact family total is below eleven.
It therefore improves the retained lower endpoint but does not close the formulation.

Iteration 0 remains the only row-converged solve, so the computational upper endpoint is
`11.055616942909783`. No converged row fell below eleven, and the covering bridge did
not open. The provisional bracket width is approximately `0.671404534532568`, 58.4994
percent of the retained width `1.147711347927249` and a 41.5006-percent reduction.
Although that width is below the declared `0.86078351094543675` threshold, the routing
rule cannot fire until the full four-CPU-hour evidence budget has been spent.
H-064 and exp-070 therefore receive a promising intermediate checkpoint, not a verdict.

Iteration 13 is retained as deadline-tail evidence.
Its row loop stopped as `deadline reached after 0 rounds`, was not converged, and
produced row objective `11.003477019645144`; it is not an upper endpoint.
The terminal summary records its 150 selected orbits, while the state was written before
that selection was installed and records `added: 0`, an empty note, 27,277 sites, and an
empty top-level stop string.
The state is strict JSON and remains a valid pre-addition resume checkpoint; this
serialization order must not be mistaken for a restart or for the terminal stop class.

Final process CPU time is unavailable because the runner does not record it and the PID
exited between read-only process-table samples.
The last live sample at `2026-09-06T05:24:29Z` recorded `104:50.95` CPU in state `R`;
this is a lower bound, not an estimate.
Both original PIDs were absent at the next sample.

All three JSON outputs parse strictly and contain no `NaN` or `Infinity`. The four
terminal SHA-256 values are:

```text
431737c54034c97ed9fdd51bd2991852d793b96b56486df4cfe2c0e9b19f2e7c  bc-232-leg-01.log
f91999b452bf89f49e2d4cda9827efbf57623a4196688b5feba0819bc7e851e2  bc-232-leg-01-state.json
d8c50db8770b12d43baa6d9e2c7384a52a0f250f8cee26b6a036c99b3cb3350e  bc-232-leg-01-summary.json
4cfbdce5cb659d77d652c011854de74ddcad94c903eff30af07bbcb5d8d9cc3f  bc-232-leg-01-family.json
```

The exact leg-02 command above is the only declared continuation.
It remains unused, all four of its stems remain absent, and no successor or covering
bridge launched.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
