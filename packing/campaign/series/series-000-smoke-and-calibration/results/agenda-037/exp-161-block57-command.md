# Exp-161 Blocks 5–7 Command

Start at 09:33Z from `packing/`. This is the H-163 Route S target on
[exp-161](../../experiments/exp-161-h163-route-s-threshold-compression.md).
Do not wait for a second reading of the producer.

`--search` is a second phase, not the 09:33Z argv.
The producer writes a receipt only when `build_receipt` returns, omits the dense `A`
from JSON, and passes no HiGHS `time_limit`. Adding `--search` on the first invocation
withholds the encoding receipt until HiGHS returns or the wall kills the process.

## Live Check

Required immediately before `--authorize-target`. A retained JSON is not a live check.
The producer has no `--check`; `--selftest` is the coverage-free producer check.

```bash
cd /workspace/packing
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
uv run --frozen --all-extras --group dev python -m devtools.admit_threshold_compression --check
uv run --frozen --all-extras --group dev python -m devtools.compress_threshold_certificate --selftest
```

Refuse on nonzero exit.
Do not formulate coverage.

Measured: admit `--check` exit 0 in 0.73 s at 2026-09-18T07:00:56Z (historical
`agenda-036/exp-161-admit-check-2026-09-18T0604Z.log` was 3 s, 06:04:57–06:05:00Z).
Producer `--selftest` exit 0 in 0.70 s at 07:01:10Z (historical
`agenda-036/exp-161-producer-selftest-2026-09-18T0611Z.log` was 1 s).

## Encode Coverage (09:33Z)

Scientific wall is three hours from this process, 09:33–12:33Z if started on time.
Blocks 5–7 run until 12:53Z; the extra twenty minutes are for copying the receipt, not
more search. The overnight lease 18:40Z is not this wall.
Timeout is unresolved.

```bash
cd /workspace/packing
set -o pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
timeout --signal=INT --kill-after=30 10800 \
  uv run --frozen --all-extras --group dev python -m devtools.compress_threshold_certificate \
    --authorize-target exp-161 \
    --encode-coverage \
    --source cases/n11_threshold_certificate/certificate.json \
    --expect-source-revision 5ce2839f17b2f5a337260dc3f649e05ab974bd25 \
    --expect-catalog-sha256 8de1d9646efef5c49367b679a78ff20961f7f5c1d43b11ff28b5f9a6b41f0e75 \
    --max-orbits 23 --budget-below 11 --least-charge 1 \
    --output campaign/series/series-000-smoke-and-calibration/results/agenda-036/exp-161-route-s-threshold-compression.json \
  2>&1 | tee campaign/series/series-000-smoke-and-calibration/results/agenda-037/exp-161-encode-coverage.log
```

Copy the JSON to
`campaign/series/series-000-smoke-and-calibration/results/agenda-037/exp-161-encode-coverage.json`
as soon as it exists, before any `--search`. Do not overwrite
`agenda-036/exp-161-producer-authorized-receipt.json` (`encoding_ready`, no
enumeration).

Expect `search_status: encoding_complete`, `coverage_enumerated: true`,
`candidate_created: false`, `coverage_ran: false`, `n_plus: null`,
`generating_account: null`, `selected_orbits: null`. Read
`search.encoding.reachable_cells`, `pareto_row_count`, and `rows_sha256`. Those are
encoding stats, not N+.

`timeout` exit 124, or a missing JSON at 12:33Z, is unresolved.
The producer does not checkpoint.

## Search (second phase)

`--search` without `--encode-coverage` is refused.
`--search` with `--encode-coverage` re-runs `encode_frozen_coverage` in the same
process; the receipt does not store `A`.

Run this only if the encode-only JSON is `encoding_complete` and enough wall remains to
pay a second full enumeration plus HiGHS. Remaining wall after 12:33Z is zero.

```bash
cd /workspace/packing
set -o pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
REMAINING=$(( $(date -d '2026-09-18T12:33:00Z' +%s) - $(date +%s) ))
if [ "$REMAINING" -lt 600 ]; then
  echo "no search: remaining wall ${REMAINING}s; timeout is unresolved"
  exit 0
fi
timeout --signal=INT --kill-after=30 "$REMAINING" \
  uv run --frozen --all-extras --group dev python -m devtools.compress_threshold_certificate \
    --authorize-target exp-161 \
    --encode-coverage \
    --search \
    --source cases/n11_threshold_certificate/certificate.json \
    --expect-source-revision 5ce2839f17b2f5a337260dc3f649e05ab974bd25 \
    --expect-catalog-sha256 8de1d9646efef5c49367b679a78ff20961f7f5c1d43b11ff28b5f9a6b41f0e75 \
    --max-orbits 23 --budget-below 11 --least-charge 1 \
    --output campaign/series/series-000-smoke-and-calibration/results/agenda-037/exp-161-search.json \
  2>&1 | tee campaign/series/series-000-smoke-and-calibration/results/agenda-037/exp-161-search.log
```

Do not point `--search` at the registered encode JSON. Keep
`agenda-036/exp-161-route-s-threshold-compression.json` as the encode-only record.

`solve_feasibility_mip` is called with `time_limit_s=None`. The outer `timeout` is the
only bound. Possible `search_status` values after HiGHS: `timeout_unresolved`,
`float_infeasible_unresolved`, `solver_error_unresolved`, `float_incumbent_unverified`.
All are unresolved for H-163. The receipt still has `n_plus: null` and
`candidate_created: false`. `search.float_incumbent.n_plus` is not the accept metric.

## Output Paths

| Artifact | Path |
| --- | --- |
| Registered encode receipt | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-036/exp-161-route-s-threshold-compression.json` |
| Encode log / copy | `.../agenda-037/exp-161-encode-coverage.log` and `.../exp-161-encode-coverage.json` |
| Search receipt (only if phase two runs) | `.../agenda-037/exp-161-search.json` |
| Prior authorized default (leave) | `.../agenda-036/exp-161-producer-authorized-receipt.json` |
| Prior admit log (leave) | `.../agenda-036/exp-161-admit-check-2026-09-18T0604Z.log` |

## Accept Rule

Confirm H-163 only at **N+ <= 23** with budget < 11, least charge >= 1 from agreeing
exact event-cell and interval routes, source-distinct manifest replay, and all five
[X-032](../../../../explorations/X-032-route-s-threshold-compression.md) confirmation
clauses:

1. Admitted decompressor from U025, N+ <= 23.
2. Nonnegative rational weights, D4 tying, exact budget < 11.
3. Both coverage routes accept the closed-core domain and agree on least charge >= 1.
4. Source-distinct replay of manifest, reconstructed certificate, and result.
5. **generating_account**: a short generating account of the retained orbit pattern, not
   a restatement of N+. `selected_orbits` must equal N+.

This producer path cannot meet clauses 1, 3, 4, or 5. It never emits a candidate, never
runs `devtools.decide_threshold_certificate`, and leaves `generating_account` null.
Blocks 5–7 therefore cannot accept.

Refute only with an exact infeasibility certificate that no N+ <= 23 family member meets
the frozen constraints.
Float HiGHS infeasibility is not that certificate.

Timeout is unresolved, never rejected.
`timeout_unresolved` and a killed encode are the same verdict.

Blocked (no scientific verdict) if the live `--check` fails,
`--authorize-target exp-161` is missing, or a candidate is built by any path other than
the admitted decompressor.

These admission-control manifest SHA-256 values cannot confirm, including by
decompressing them and running coverage:

- `53fbe28bd6dd022600515663ea1e3609ed2bd36a83e69e350b4bb3b45d7b7176` (full T-025)
- `007b394f48b0b11565ca87d09ad961258534c426bfd623a3e9bfc15aa6495e8a` (synthetic
  23-orbit)
- `194f1f9f47fc94e7f945920c38a4efdb43476719eba025ea446a1d7b91fde27e` (rejected 24-orbit)

The authorized default receipt already records those three under
`forbidden_control_manifests`.

## Time and Memory

U025 (from the authorized receipt and a coverage-free inventory load): 119 orbits (79
point + 40 threshold), 904 certificate atoms, 181 directions, budget
`685457679/62500000`. Event geometry is larger than the certificate: 1544 event atoms
(584 points + 960 threshold sites; every threshold orbit is 8 members of 3 sites).

`encode_frozen_coverage` loops all 181 directions.
Each direction allocates a dense `uint8` matrix of shape `(reachable_cells, 119)`,
paints 79 point-orbit grids plus 320 threshold-member count grids, `unique_rows`, then
`pareto_minimal_rows` on `vstack(old_pareto, new_unique)`. That last step is a Python
loop over rows.

Planning probes of `direction_coverage_rows` and one-direction `pareto_minimal_rows` on
this machine (not `--encode-coverage`, not `--search`, not stacked across the net):

| Direction | Grid | Reachable cells | Unique rows | Pareto rows | Rows s | Pareto s | RSS |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 (`0`) | 1242² | 1026169 | 19319 | 398 | 3.4 | 3.2 | 0.49 GiB |
| 45 (`207107/2000000`) | 2882² | 5947837 | 64191 | 1869 | 40.9 | 48.4 | 2.40 GiB |
| 90 (`207107/1000000`) | 2882² | 5852681 | 64024 | 2244 | 42.4 | 58.8 | 2.40 GiB |
| 180 (`207107/500000`) | 2882² | 5709041 | 38124 | 491 | 41.0 | 8.8 | 2.40 GiB |

Dense `A` for one diagonal direction is about 5.9e6 × 119 bytes ≈ 0.70 GiB before
unique; peak RSS 2.40 GiB is that matrix plus copies.
`--encode-coverage` holds one direction at a time, so expect **about 2.4 GiB**, not 181
copies.

Dir 0 is the cheap axis-aligned outlier.
The other 180 half-tangents look like directions 45–180: about 40 s of unique plus 9–60
s of Pareto, **50–100 s per direction**, **2.5–5 h** for 180 directions if stacked
Pareto stays in that band.
`encode_frozen_coverage` was not run; stacked `old_pareto` can grow and make late Pareto
slower than the one-direction times.
Treat **3 h as plausible and 6 h as the upper end**. The 3-hour scientific wall may
expire during enumeration.
That is unresolved.

`--search` after a complete encoding: 119 binary indicators, 119 continuous weights,
Pareto rows as `A w >= 1`, budget < 11, cardinality <= 23. The constraint matrix is
`float64` of shape `(pareto_row_count, 238)`. One-direction Pareto fronts were 398–2244
rows (~0.4–2 MB). The 181-direction front is unmeasured; even 50 000 rows are about 95
MB. HiGHS time is unmeasured.
The CLI does not pass `time_limit_s`. Do not start `--search` unless encode-only
finished with more than about ten minutes of wall, and still expect the follow-up to
re-spend the encoding cost before HiGHS starts.

T-025 two-route retention is about ninety seconds on three workers
(`cases/n11_threshold_certificate`). That cost is for a later decompressed candidate,
not this encode. T-018 piercing timed out in event-cell encoding at 20 s (5 directions)
and 180 s (9 directions) on 1121 sites; encoding, not HiGHS, was the cost there too.

Live `--check` / `--selftest` are under a second.
The authorized default (`encoding_ready`, no enumeration) was 1 s at 06:11Z.

If a retained 8-direction stacked-Pareto rate is wanted before spending the wall on 181
directions, that measurement belongs in the producer: pass `direction_indices` through
to `encode_frozen_coverage` and write `encoding_record`. The library already accepts
`direction_indices`; the CLI does not.
Do not replace that with a one-off `-c`. The 09:33Z command above is still the
181-direction `--encode-coverage` target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
