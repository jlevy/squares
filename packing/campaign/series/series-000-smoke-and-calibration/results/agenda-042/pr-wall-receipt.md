# Pull-Request Wall Receipt (W5 efficiency block, agenda-042, `think-g4n9`)

Lane A of
[`agenda-042`](../../../../agendas/agenda-042-efficiency-block-the-development-cycle.md),
2026-09-23, against `main` at `f5c9c8453`. Measured by a delegated lane with
`devtools.check_pr_wall`, `devtools.read_tier_walls` and the Actions jobs API; the lead
re-checked `SUITE_SHARDS = 2`, commit `38ce5cfdb` and the frontend pair at
`validate.py:3376`.

Measured with `devtools.check_pr_wall` (`--sample`/`--run-id`),
`devtools.read_tier_walls`, `gh api .../jobs` step timings, and
`packing/devtools/gate-budgets.yaml`. Repo state: main = f5c9c8453. All run ids and shas
below are measured facts; interpretation is marked as such.

## 1. Wall vs. 180s and vs. the register’s recorded median

**packing-validation** (aggregator `packing-required`). Register (`pull_request_walls`,
recorded 2026-09-17, n=2): median 175.5s, budget 180s, `enforcement: advisory` under
`think-g4n9`. My sample: last 15 completed PR runs (2026-09-22/23),
`check_pr_wall --sample`:

| kind | n | median (mine) | min | max | vs 180s budget | vs register median (175.5) |
| --- | --- | --- | --- | --- | --- | --- |
| main | 13 | 189s | 162 | 227 | 8/13 over 180s | +13.5s (+7.7%) |
| stacked | 2 | 183s | 175 | 191 | 1/2 over 180s | +7.5s |

**PR #221 final head** `affe97215` = run **35800361316**: **189s**, `frontend` finished
last. Confirmed via `gh api pulls/221` (head_sha match) — this is the run PR #221
reported at 24 of 24 green.

**certificate-page** (aggregator `pages-required`). Register (recorded 2026-09-17, n=2):
median 176s, budget 180s, advisory under `think-g4n9`. My sample, 15 runs:

| kind | n | median (mine) | min | max | vs 180s | vs register median (176) |
| --- | --- | --- | --- | --- | --- | --- |
| main | 14 | 168.5s | 153 | 282 | 4/14 over 180s | -7.5s (flat/slightly better) |
| stacked | 1 | 158s | — | — | under | — |

PR #221 final head, run **35800361306**: **168s**, `typography` finished last.

**Critical-path job frequency**, 15 packing-validation runs: suite-a 8, suite-b 2,
frontend 5 (one run — see below — split), sweeps 1, geometry/typecheck/validate 0. 15
certificate-page runs: typography 9, publish 4 (see §3), geometry 1.

## 2. Critical-path jobs: queue / setup / work

From `check_pr_wall --run-id` (component sums) and `gh api actions/jobs/<id>` step
timings on run 35800361316 (packing-validation, PR #221 head):

| job | queue | setup | work | wall | slowest step(s) |
| --- | --- | --- | --- | --- | --- |
| frontend | 2s | 49s | 128s | 180s | “Run the frontend source and built-page contracts” (128s, one shell step) |
| suite-a | 2s | 24s | 146s | 173s | “Run required pull-request behavioral shard A” (146s, one step, pytest -n) |
| suite-b | 3s | 30s | 129s | 163s | “Run required pull-request behavioral shard B” (129s) |
| validate | 3s | 33s | 115s | 153s | `packing-validate --checks` (52 selected steps; register puts exact verification + basedpyright largest historically) |
| geometry | 2s | 22s | 115s | 139s | `packing-validate --geometry` (9 steps) |
| typecheck | 3s | 31s | 70s | 105s | basedpyright, one step |
| sweeps | 2s | 19s | 69s | 90s | `packing-validate --sweeps` (4 steps) |

Frontend setup breakdown (step timestamps): checkout 17s, uv+Python 4s, uv sync 2s, Node
24 install 7s, Playwright cache 2s, “npm ci + Chromium apt” (now overlapped) 13s. The
single work step is not broken into sub-steps by CI (`packing-validate --frontend` runs
as one shell invocation), but the register’s own comment on `Step.frontend`
(`packing/src/sqpack/cli/validate.py:3376`) records the hosted split as **Chromium ~59s,
biome ~92s** at `--jobs 2` — i.e. **biome/type-aware-ESLint/tsc, not Chromium, is now
the frontend job’s long pole**.

certificate-page, run 35800361306 (typography critical, 168s total):

| job | queue | setup | work | wall |
| --- | --- | --- | --- | --- |
| typography | 2s | 21s | 102s | 125s |
| geometry | 2s | 20s | 95s | 117s |
| browser-geometry (webkit) | 2s | 60s | 52s | 116s |
| pdf | 2s | 27s | 82s | 113s |
| screen | 1s | 20s | 89s | 112s |
| font-loading (webkit/firefox) | 2s | 44-45s | 44-47s | 78-93s |
| publish | 2s | 1s | 2s | 4s |

## 3. Comparison with think-g4n9 (2026-09-17)

- **Both named frontend candidates are already shipped.** Commit `38ce5cfdb`
  (2026-09-18, “perf(ci): start Chromium early and overlap independent browser work”)
  starts the Chromium step early (`start_early=True` on `Step` “workbench browser
  behavior in Chromium”) and overlaps `npm ci` with the Playwright/Chromium apt install
  in the same shell step (`.github/workflows/packing-validation.yml:579-599`). This
  matches think-g4n9’s “start Chromium first” and “apt fonts … Node setup” candidates
  verbatim.
- **Despite that fix landing, `frontend` still wins the critical-path race in 5/15
  sampled runs** (33%), because the bottleneck moved: think-g4n9 measured “Chromium
  73-82s serialized behind liveness 12-22s”; the current register comment measures
  “Chromium 59.09s, biome 91.69s” at the same `--jobs 2` — biome/tsc is now the longer
  half. think-g4n9’s diagnosis is therefore **stale for frontend**: its fix addressed the
  09-17 bottleneck and was applied, but the job’s new floor is a different step.
- **The third-suite-shard candidate (`SUITE_SHARDS=3`) has not been implemented.**
  `grep SUITE_SHARDS packing/src/sqpack/cli/validate.py` → `SUITE_SHARDS = 2` still.
  This is the candidate that **still hits the current critical path directly**: suite-a
  or suite-b is the critical-path job in 10/15 sampled runs, more often than any other
  job, at 129-146s of pure pytest work each.
- **Wall has grown modestly for packing-validation** (175.5s → 189s median, +7.7%,
  n=2→13) and is essentially flat for certificate-page (176s → 168.5s median).
  Both are within the 1.6-1.8x hosted-runner variance think-g4n9 already documented, not
  a new step-content regression by itself — see queue-driven outliers below.
- **Per-job registry entries are stale relative to live reality** for the jobs that
  aren’t tracked in `pull_request_walls` (only the aggregate wall and `certificate-page`
  per-job list are refreshed there).
  `checks` tier: register `measured_seconds: 75.67` (2026-09-17) vs.
  observed live work ~101-115s (1.4-1.5x, at the drift-rule edge).
  `typecheck`: register already caught and attributed this one — 65.33s → 82.58s, blamed
  on the `5cd610a1a` deep-gate merge widening basedpyright’s include set.

## 4. Top 3 levers by critical-path seconds saved

1. **Third suite shard (`SUITE_SHARDS=3`).** Still think-g4n9’s candidate, still
   unbuilt, still the single most frequent critical-path job (10/15 runs).
   Current suite-a+suite-b work is ~129-146s each after a 2-way pre-collection split; a
   3-way split of the same ~270-290s of combined step-time predicts each shard nearer
   90-100s of work (think-g4n9 itself predicted ~91s at a fast runner, ~145s wall at
   1.8x). Estimated saving: 30-50s off wall on the majority of runs.
   Needs `--suite-c`, a `suite_c` register entry, a third workflow job, and
   `packing-required` picking it up, per the bead’s own scoping.

2. **Split biome/type-aware-ESLint/tsc out of the frontend job’s single work step.**
   think-g4n9’s “split the Chromium step across jobs” candidate targeted the wrong half
   now: Chromium already starts early (59s) and biome/tsc is the current tail (~92s of
   the 117-128s work step observed).
   Giving biome/eslint/tsc its own job (or its own worker slot ahead of Chromium) would
   let the two run genuinely in parallel instead of `--jobs 2` serializing whichever
   finishes second; estimated saving: 30-50s on the ~33% of runs where frontend is
   critical. Not something think-g4n9 named explicitly — this is a new candidate.

3. **Runner-queue exposure on the job that finishes the DAG.** Two measured outliers
   trace directly to a single job’s own queue delay, not its work: run 35777665010
   (packing-validation, 227s) — suite-a queued 38s before starting; run 35780496732
   (certificate-page, 282s) — `publish` (2-4s of real work) queued 29s waiting for a
   runner. This is scheduler contention, not step cost, and it isn’t one of think-g4n9’s
   content-focused candidates.
   No devtools tool currently tracks queue-time percentiles across runs (see tool gap
   below); the two readings above are from ad hoc inspection of individual
   `check_pr_wall --run-id` output.
   A cheap lever worth testing: reducing the total count of concurrently-queued required
   jobs (7 for packing-validation, 13 for certificate-page) so fewer jobs compete for
   the shared `ubuntu-latest` pool at once.

## 5. Off-critical-path PR-surface jobs (cost runner-minutes, not wall)

- **`macos-portability`** (packing-validation): listed `not_gating` in the register, so
  `packing-required` does not wait on it at all.
  Observed 105s (00:04:15-00:06:00 on run 35800361316) — pure runner-minute cost, zero
  wall impact by construction.
- **`pdf`** (certificate-page): gates (not in `not_gating`), but its work (73-97s
  measured/observed) is consistently below `typography`/`geometry`/`screen` (89-115s),
  so it never appeared as the critical-path job across 15 sampled runs even though
  `pages-required` does wait for it.
- **`workbench`, `print-layout`, `font-loading (firefox)`, `scope`, `prepare`**
  (certificate-page): all measured under the typography/geometry/screen band (52-96s),
  same story.

## Tool gap

No devtools tool aggregates queue-time (as opposed to work-time) distributions across
runs or flags a job whose queue delay, not its steps, drove an outlier wall.
`check_pr_wall
--run-id` surfaces one run’s queue/setup/work split, and `--sample` gives per-run
totals, but nothing rolls up “how often does queue time exceed N seconds” the way
`gate-budgets.yaml`’s drift/stale rules do for step content.
The two queue-driven outliers above (§4.3) were found by manually pulling individual
`--run-id` reports, not by a register check.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
