# Suite Shards Receipt (W5 efficiency block, agenda-042, `think-g4n9`)

Lane D of
[`agenda-042`](../../../../agendas/agenda-042-efficiency-block-the-development-cycle.md),
2026-09-23, against `main` at `f5c9c8453`. Measured by a delegated lane from the
`validation-timings-suite-a` and `-suite-b` artifacts of run 35800361316. The per-file
tables are retained beside this receipt:
[`suite-shards-measured.tsv`](suite-shards-measured.tsv) (seconds, tests, file, from
that run’s JUnit) and [`suite-shards-recorded.tsv`](suite-shards-recorded.tsv) (file,
seconds, from `devtools/suite-file-costs.json`). The lead re-counted the 31 files the
record does not name from those two tables.

Source: CI run 35800361316 ("Packing validation") on affe97215’s PR event (GITHUB_SHA
893a49af, the merge ref), jobs suite-a (106989076942) and suite-b (106989076429).
Downloaded each job’s `validation-timings-suite-{a,b}` artifact: JUnit XML (6,995
testcases) + `test-files.json` (per-file cost report), both measured on this exact run.
Cross-checked against `packing/devtools/suite-file-costs.json` (the sharding record).

## 1. Job timings (measured, this run)

| job | job wall | pytest wall | tests | setup (checkout+uv sync) |
| --- | --- | --- | --- | --- |
| suite-a | 173s | 141.53s | 3670 | ~24s (00:04:12→00:04:36) |
| suite-b | 163s | 124.64s | 3325 | ~28s (00:04:14→00:04:42) |
| frontend | 180s | — | — | — |

Note: on **this** head, `frontend` (180s) edges out `suite-a` (173s) as the longest PR
job — the 3.0 and 2.9 minute readings on PR #221 were its *previous* head, `dfbb28dc4`.
suite-a/b remain the two heaviest test-execution jobs and are still the pair this lane
was asked to cover.

## 2. Top files by measured cost (this run, sum of setup+call+teardown, both shards)

Top 10 of 25 (full table in `suite-shards-measured.tsv`):

```
57.06s  66 tests  test_read_fixed_core_calibration_profile.py   (shard A)
52.89s  23 tests  test_wall_owner_parent_inputs.py               (shard B)
33.51s 994 tests  test_schema_validator_equivalence.py            (shard A)
32.07s  23 tests  test_negative_controls.py                      (shard B)
28.89s  96 tests  test_fixed_core_packet_calibration.py          (shard A)
22.69s  27 tests  test_density_face_verifier.py                  (shard A)
22.29s 138 tests  test_fixed_core_packet.py                      (shard B)
19.52s 123 tests  test_validation_cli.py                         (shard B)
14.48s  27 tests  test_admit_threshold_compression.py             (shard B)
14.26s   9 tests  test_stromquist_restricted_orientation_review.py (shard B)
```

Aggregate: 893.2s summed test-seconds / 6,995 tests.
Top 20 individual tests = 125.5s (14.1% of aggregate); top 25 = 147.3s (16.5%). **Not
concentrated** — no ~70%-in-20-tests pattern today (that historical figure, if real,
describes an earlier, already-fixed state; I found no live evidence of it on this run).

**Top individual tests** (JUnit `time`, setup+call+teardown combined; full table in
`suite-shards-measured.tsv`): 12.979s
`test_negative_controls::test_motion_lab_golden_is_not_a_mutation_worker_input` (only
test ≥12s, all setup — see §3), 8.149s
`test_negative_controls::test_generator_owned_prospective_outputs_stay_out_of_mutation_snapshots`,
7.880s
`test_frontier_rigidity_contract::test_catalogue_rigid_is_a_transcription_and_carries_no_judgement`,
7.403s
`test_read_fixed_core_calibration_profile::test_full_profile_reconstructs_every_row_digest_resource_and_sidecar`,
7.152s
`test_n54_source_contract::test_field_receipt_semantic_drift_is_refused_before_digest[...]`,
6.993s `test_fractional_corner_clip::...fails_k4`, 6.942s `test_reachable_tests::...`,
6.084s `test_catalogue_precision::...`, 6.002s
`test_n54_source_contract_independent::...`, 5.887s `test_wall_owner_containment::...`;
long tail down to ~4.3s for #25.

## 3. The per-test ceiling and how close tests sit to it

`QUICK_TEST_WALL_BACKSTOP_SECONDS = 12.0` (`packing/src/sqpack/cli/validate.py`),
enforced via `--durations-min` on the **call** phase only (setup/teardown excluded,
deliberately — a module-scoped fixture “bills its whole cost to whichever test happens
to trigger it first,” so a setup-phase overage moves the module rather than failing the
gate). Tests are *marked* `slow` at a separate, lower 2s threshold.

CI’s own report for this run: `(11007 CPU lower bounds < 6s ... hidden)` and `(11010
durations < 12s hidden)` — **zero tests reported a call-phase duration ≥ 12s**. Closest
observed call-phase times (re-running top files locally with CI’s own scheduling, §5)
topped out at **5.00s**; the only test whose raw JUnit total nears 12s does so on
**setup**, not call (a shared fixture it happens to build first) — the accepted,
documented failure mode, not a live risk.
Retained suite sits at ≤ ~42% of the ceiling.

The “~20 tests once carried ~70% of the tier” figure in OR-13 (measured 2026-09-05) is
**not corroborated** by this run’s data (top 20 = 14.1% today) — likely a past,
already-remediated state; flagging as unverified-on-current-data.

## 4. Sharding mechanism and staleness

`packing/devtools/suite_files.py`: `--suite-shard K/N` assigns each **file** (not test)
to a shard via greedy longest-first bin-packing over `suite-file-costs.json`’s recorded
per-file seconds; a file the record doesn’t name falls back to `crc32(path) mod N` (no
cost awareness). `devtools.suite_files show` on the current record: **325 files, shard 1
= 272.87s, shard 2 = 272.87s — perfectly balanced by construction**, from a greedy LPT
packing.

**Staleness, measured:**
- Record’s `recorded_from`: run 35175474610, 2026-09-17T02:43 UTC. Last edit to
  `suite-file-costs.json`: commit `c4f0660d`, 2026-09-16. That’s ~6 days / ~95 commits
  touching `packing/tests` before affe97215 (2026-09-22).
- **31 test files added since then are entirely absent from the record** (confirmed by
  lookup) and fall back to the unbalanced crc32 hash.
  On this run they carried 39.4s combined (16 files/22.57s in shard A, 15 files/16.87s
  in shard B) — a real, if modest, skew (shard A got 34% more of that unrecorded cost
  than shard B, on nearly the same file count).
- **Ratio of recorded to measured, top files** (recorded seconds vs this run’s measured
  seconds, for the 324 files present in both):
  - `test_read_fixed_core_calibration_profile.py`: rec 40.12s → mea 57.06s (**1.42x**)
  - `test_wall_owner_parent_inputs.py`: rec 23.32s → mea 52.89s (**2.27x**)
  - `test_schema_validator_equivalence.py`: rec 14.46s → mea 33.51s (**2.32x**)
  - `test_negative_controls.py`: rec 12.80s → mea 32.07s (**2.50x**)
  - `test_fixed_core_packet_calibration.py`: rec 17.74s → mea 28.89s (**1.63x**)
  - **Aggregate over all 324 common files: recorded 545.09s → measured 853.57s, ratio
    1.57x.**
- This uniform ~1.4–2.6x growth across nearly every file (not a handful of outliers)
  looks more like **runner-speed variance** than per-file regression — the project’s own
  bead (`is-01m2psbsfbsn9s7tm0nm3eggab`) already documents hosted-runner speed varying
  “about 1.6-1.8x on identical code.”
  Can’t separate noise from real growth without a same-day re-record (out of scope
  here); reporting as a measured ratio, not a cause.
- **Shard balance today**: job wall A 173s/B 163s (ratio 1.06); pytest wall A 141.53s/B
  124.64s (ratio 1.14); measured cost sum A 465.6s/B 427.4s (ratio 1.09). Mild,
  consistent skew toward A (~10-17s) even though the record claims *exact* balance — all
  of the live skew is drift the record can’t see.

## 5. Cheap-win investigation

Ran the top files with `--durations`, **matching CI’s actual `--dist=loadfile`
scheduling** — default `-n` scheduling scatters one file’s tests across workers and
makes module-fixture costs look up to 4x inflated as an artifact of assignment, not a
real cost.

- **`test_read_fixed_core_calibration_profile.py`** (57s/66 tests) — confirmed
  subprocess-heavy: dozens of `subprocess.run` calls invoking the real CLI per test
  (`test_running_reader_origin_and_cli_copy_refusal` 5.00s call,
  `test_real_binder_nested_and_supervisor_duration_controls[...]` 3-4s each).
  Local `-n 4 --dist=loadfile`: 66 tests/14.31s wall, nothing near the ceiling, but
  ~0.86s/test average is almost all subprocess start/CLI-parse overhead repeated per
  test. **Genuine speedup candidate**: batching or in-process CLI invocation would cut
  most of this file’s cost — it’s dozens of small subprocess spawns, not one bad
  fixture.
- **`test_wall_owner_parent_inputs.py`** (53s/23 tests) — 45.00s serial, no
  `@pytest.fixture` in the file at all; cost spreads evenly 1.4-4.5s/test across real
  subprocess + timing-simulation tests (clock/deadline/publication races).
  **No fixture win available** — would need per-test redesign (fake clock instead of
  real sleeps) to shrink, a bigger, riskier change than a config tweak.
- **`test_negative_controls.py`** (32s/23 tests) — **initially looked like a
  session-fixture win**: naive `-n 4` showed the `control_snapshot` module fixture
  rebuilding 4x (~10s each) because default scheduling scatters the file.
  **Retracted** after matching CI’s real `--dist=loadfile`: fixture builds exactly once
  (7.15s), rest is two genuinely expensive repo-scanning tests (4.18s, 3.98s). Already
  using the correct pattern; not a cheap win.
- Team already tried and **rejected** the obvious global fix: `validate.py`’s own
  comment records `--dist=loadscope` at 318.54s vs 302.70s default (+5.2%), `worksteal`
  at 323.69s (+6.9%) for the whole lane.
  A blanket scheduling change is a net loss even though it would help isolated files
  like the one above pre-correction; any fix for a genuinely repeated fixture must be
  file-scoped (e.g. on-disk memoized snapshot), not a global `--dist` change.
- **`test_schema_validator_equivalence.py`** (33.5s/994 tests) checked too: no problem —
  994 cheap parametrized cases (~0.03s avg) plus 2 legitimately larger ones; cost
  matches test count, nothing to fix.

## 6. Third shard (think-g4n9 / bead `is-01m2psbsfbsn9s7tm0nm3eggab`)

Bead’s own prediction (measured in a prior spike, “attic/wall at 21642ed8”): 3rd shard ≈
91s end-to-end on a fast runner, ≈ 145s wall at 1.8x runner variance — vs.
5 hosted reads of the 2-shard wall at 194/189/178/166/216s against OR-14’s 180s target.

Setup/work split measured this run: **each job pays ~24-28s of fixed setup** (checkout +
submodules + `uv sync`) before its first test runs; suite-a’s pytest phase itself is
141.53s, suite-b’s is 124.64s (266.17s combined).
Splitting that combined pytest work three ways (~88.7s/shard) plus the same ~25-28s
setup gives an estimated **~114-120s per shard job**, vs.
today’s 163-173s — a **~50-55s cut to the critical path**, consistent with the bead’s
~145s prediction at typical runner variance.
The added job costs one more concurrent runner-slot and ~25-28s of *duplicated* setup in
aggregate CI-minutes (not wall-clock, since jobs run in parallel) — a real but small
tax, and it stays entirely on the PR surface (re-sharding, not deferring), so it needs
no OR-13 justification.

Setup is ~15-17% of each job’s current wall; it does not scale away by adding shards, so
returns from a 4th shard would be smaller still (Amdahl: fixed ~25s floor per job).

## 7. Top 3 levers by CI seconds saved on the critical path

1. **Third suite shard (structural, ~50-55s off the critical path, estimated from
   measured setup/work split).** Classification: **speedup** — same tests, same
   coverage, redistributed across one more parallel job.
   No OR-13 justification needed (nothing leaves the PR surface).
   Cost: one more runner-slot, ~25-28s of duplicated setup work in aggregate minutes.
   Already scoped as `think-g4n9`/bead `is-01m2psbsfbsn9s7tm0nm3eggab`.
2. **Refresh `suite-file-costs.json` from a fresh multi-run cohort (mechanical, closes a
   measured 1.09-1.14x shard skew and stops 31 unrecorded files from landing on an
   unweighted hash).** Classification: **speedup** — pure rebalancing, zero coverage
   change, cheap (one `devtools.suite_files record` run over a fresh cohort of hosted
   runs). Smaller win (~10-17s) than #1 but nearly free and currently silently rotting (6
   days stale, 31 files blind to it, aggregate recorded-vs-measured ratio 1.57x on the
   324 files it does track).
3. **De-subprocess the CLI-invocation-heavy test files**
   (`test_read_fixed_core_calibration_profile.py` 57s/66 tests,
   `test_fixed_core_packet_calibration.py` 28.9s/96 tests, `test_fixed_core_packet.py`
   22.3s/138 tests — ~108s combined, 12% of the 893s aggregate), converting per-test
   `subprocess.run` CLI calls to in-process calls where the test doesn’t specifically
   need process-boundary semantics.
   Classification: **speedup** — keeps coverage, but is real engineering work
   (correctness risk: some of these tests may exist specifically to test the process
   boundary) and its savings are the least certain of the three; needs a
   source-by-source read to know which tests can safely move in-process.
   No OR-13 justification needed (nothing leaves the PR surface).

None of the three levers proposes moving a test off the PR surface; OR-13 is not in play
for this set.
A global xdist `--dist` change was checked and is already known to be a net
loss (see §5) — do not re-propose it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
