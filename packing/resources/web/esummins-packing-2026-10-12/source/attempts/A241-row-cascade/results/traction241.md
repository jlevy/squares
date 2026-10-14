# A241 -- the traction check: k3_02's 20 A100 head-to-head cells, before and after the rows

A238's blind run is the baseline: **0 DEAD / 20 ALIVE**, mean 4.3 s, `kills_by_rule = {}`, max depth 0 --
the toolkit's rules (rule CC, A208 no-room + Lemma POCKET, A206 Rule NS, A230 Rule EPS, A224 Rule SNAP)
all act on Theorem FC's forced cells, and k3_02 had none usable.  Same code, same pages, same wall.

## usable forced cells now (the row cascade's output)

| class | usable / forced | the usable extensions |
|---|---|---|
| `k3_01` | **0** / 4 | — |
| `k3_02` | **0** / 6 | — |
| `k3_03` | **0** / 6 | — |
| `k3_04` | **0** / 6 | — |
| `k3_05` | **0** / 7 | — |
| `k2_00` | **0** / 5 | — |
| `k2_01` | **0** / 6 | — |
| `k2_02` | **0** / 6 | — |
| `k1_00` | **0** / 5 | — |

## the 20 cells

| cell | A100 | A238 blind | A241 with rows | A241 s | killed by | nodes | depth |
|---|---|---|---|---|---|---|---|
| `c0_Y0083` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0179` | refused (tau 7.000000 >= budget 7) | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0721` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0729` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0730` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0731` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0732` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0733` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0778` | refused (tau 7.000000 >= budget 7) | ALIVE | _pending_ | - | — | - | - |
| `c0_Y0779` | refused (tau 7.000000 >= budget 7) | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1042` | FAIL(rc=3) | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1050` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1051` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1111` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1119` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1127` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1135` | FAIL(rc=3) | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1139` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1143` | PASS | ALIVE | _pending_ | - | — | - | - |
| `c0_Y1151` | PASS | ALIVE | _pending_ | - | — | - | - |

**Score: A238 blind 0 DEAD / 20 ALIVE  ->  A241 with rows 0 DEAD / 0 ALIVE (0 of 20 decided).**

