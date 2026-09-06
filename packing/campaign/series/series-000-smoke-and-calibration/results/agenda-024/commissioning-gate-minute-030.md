# Agenda 024 Commissioning Gate: Active Minute 30

Status: **passed.** The boundary was `2026-09-06T04:03:15Z`; gate observations were
taken through `04:03:44Z`, and the matched BC-233 launch followed explicit coordinator
GO at `04:03:58Z`.

## Clock and upstream reconciliation

Official T+0 remains `2026-09-06T03:31:00Z`. The only shared-clock pause remains the
pre-process uv-cache refusal from `03:31:00Z` through `03:33:15Z`, so active minute 30
fell at `04:03:15Z`.

During this slice, `origin/main` advanced from
`57135eec465ffd8a143ad8df287c62638d97fa5c` to `6bd136b058b77189ca3e38b1802dbaf559df30e1`
when PR #90 landed. The coordinator froze new launches, fetched the 22-path delta, and
merged it as `a70e002e690725ce4c576caf8c057bee25ff3479`. The only path changed by both
branches was `SYNOPSIS.md`, which merged automatically.
The diff from launch remained empty across both fractional engines, both child agendas,
the retained n=11 controls and warm state, and every named Trump input.
The upstream gate did not pause active time: all four contexts continued their assigned
work and BC-232 continued uninterrupted.

PR #90’s lockfile change adds Playwright and its two support packages; it changes no
numerical dependency version.
The coordinator then committed the measured CI timing repair as
`8cc0af436b0249db8cc8f44e2a6659a573aeda08`. These changes are operational and do not
alter a scientific input.

## BC-232 live receipt

The exact BC-232 process remained live and unchanged as uv PID 84153, Python 3.14.7 PID
84154, and manager session 83011. The coordinator’s boundary sample recorded 30:07
elapsed and 30:00.37 CPU time.
The manager’s later sample recorded 30:22 elapsed and 30:16.33 CPU time.

The only completed row-converged result remained iteration 0:

```text
rows_objective = 11.055617
scaled_total   = 9.907906
```

The latest completed row, iteration 7, was not converged.
Its printed objective `11.012417` is not an upper endpoint.
Its exact scaled total was `43984176092/4477804693`; the best exact lower endpoint
remained `43715381412/4362517039` from iteration 2. At the boundary the mutable state
and log hashes were, respectively,
`3f63a5f1c1a95c24d4db4eecd6ebbfb0c3aaebac400c48333dfd656c5628f353` and
`72883364cca26d960159333326a520ea1330a8a365bfeea3c4ed0bebbe47992a`.

The frozen identities still matched:

```text
8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6  retained warm state
dcc220357eeb7b5a37e775c00fcf5569608ffa77d6ee4796feff026bb3e46f2c  run_fractional_cutting.py
8c35796d7d7d3b3dbfa8eafd29d63078131ebb9d0b921a71c178ff77530eda01  run_fractional_colgen.py
510d3838a40973ec6535e4c7d99198804b8ed88a9c52126c455c97b182651c0f  agenda-025
```

## BC-233 matched launch

All three screen summaries remained strict JSON, converged, zero-exit, and paired with
frozen candidates. The selected `1/2` candidate retained exact mass `11142897/1000000`
and SHA-256 `628d7e55d664c5256a9331b9a68166306a30c275432a997bfe9fab1a9ca0fc5a`. All
eight released/control paths were absent at the boundary.

The manager presented commands identical in side, shrink, grids, inset, direction net,
scale, eight column rounds, 60 row rounds, three rows per direction, thread pins, and
2,520-second deadlines.
The released arm alone carries `--seed-certificate` for the selected candidate; both
commands carry the declared `--seed-map centre`. The coordinator issued GO only after
checking those fields and the fresh stems.

The released arm started once at `04:04:38Z` as session 87066, uv PID 17163, and Python
3.14.7 PID 17164. The control started once at `04:04:39Z` as session 83855, uv PID
17171, and Python 3.14.7 PID 17172. The one-second skew is recorded.
Initial process samples showed both Python processes at approximately 100 percent of one
core. Startup records confirmed the selected seed in the released arm and
`seed_certificate: null` in the control.

## Theorem packets and write scopes

BC-230 had its theorem, schema, specialization, and control-matrix author drafts plus
draft checkpoint and disposition records under the single assigned agenda-025 root.
The fractional manager listed 19 paths before the matched launch, all in that root.

BC-240’s output hashes were
`2ef884c5972d2ac9ed0e9f98a0c4f53f05154e9b69ea08ba22a5f594b9019a74` for
`packing/cases/trump11/isolation-theorem.md` and
`442e4b47f54ae7e7a8573b28123815f67dfacda7ed79b98e07af6463dd81b7df` for its JSON
companion. No scientific command ran after the allowed exact witness and tangent replay.
The packet still claims only labelled, anchored, fixed-side local isolation, the
associated local equality clause, and the local quadratic side estimate.
It makes no global, pose-side, contact-type, or full-radius-replay claim.

The closure manager’s provisional author hashes were
`1537f800e4ec0a96a320a501536a4a16c0ee89bfb941e27d5b9fde05ad2ab90a` for BC-242 and
`4bd32d50a5a5dd51a9da8fd959d7bd05972c58c244302913654f2e83fa0c4e68` for BC-245. The
source-distinct minute-15 findings were resolved: compactness is now proved directly on
the quotient; the Fritz--John normalization distinguishes local parameters from embedded
equality multipliers; and the 64/4,096 axis-forced controls are separated from the
general 512/262,144 typed counts.
Strong duality, attainment, continuum coverage, the producer, replay, leaf closure, and
global capture remain explicitly open.

Every manager confirmed no write outside its assigned scope.
The wrong BC-240 agenda-026 JSON stem remained absent.
The reserved agenda-026 checkpoint was still absent at the boundary.

## Decision

The minute-30 gate passes: the warm state loaded, strict-JSON controls and screen
contracts held, every frozen scientific hash remained stable across upstream
reconciliation, no output stem was reused, and write ownership remained disjoint.
BC-232 continues without reset.
The matched BC-233 processes are the only new numerical launches authorized by this
gate. No other cell or experiment opens.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
