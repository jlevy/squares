# n=18 467/100 T-019-Seeded Covering Receipt

Status: **retained**. `s(18) >= 467/100` is T-027. Canonical bytes:
`packing/cases/n18_fractional_certificate/certificate.json`.

Session-139 probe: BC-191 auto `(32, 43, 53)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `467/100`,
`(n, L, B, net) = (18, 467/100, 9977/10000, 181 directions)`.
The unseeded auto grid locked at `18.000000` unconverged.
The seed's row loop crossed below 18 and converged at `17.875567` with
`least_covered = 1` (44 LP rounds, 6853 sites / 920 orbits). The first
`--support-cap 0` invocation then hung in `check_ceiling` on the untruncated
dual and was interrupted after 31 minutes, so `run.json` was not written.
A freeze re-run with `--support-cap 32` wrote the candidate. `declare_least_cell_mass`
then `decide_certificate` accepted both routes at least cell mass
`2000007/2000000`. sha256
`3a11b6303e0663b502b6c1e3fc9d8da285104e199b17022937369bc781479059`.
T-019 at `459/100` is unchanged at n = 17.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 467/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,43,53 --scale 4000000 --support-cap 0 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed.log
```

Freeze (after the untruncated `check_ceiling` hang):

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 467/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,43,53 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-freeze-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-freeze-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-freeze.log
```

Declare then decide:

```bash
uv run --frozen --all-extras --group dev python -m devtools.declare_least_cell_mass \
  campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-certificate.json
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-t019-seed-certificate.json
```

The undeclared freeze bytes are kept beside the declared file as
`n18-467-100-t019-seed-certificate-undeclared.json`. The case copy is the
canonical artifact.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.875567` |
| Artifact mass | `8937839/500000 = 17.875678` |
| Least cell mass | `2000007/2000000` |
| Atoms | 769 |
| Sites / orbits / rows | 6853 / 920 / 11528 |
| Seed sites | 1184 |
| LP rounds | 44 |
| Crossing | stayed below 18; round 10 at `17.818182` |
| Wall (row loop) | 420.5 s |
| Freeze wall | 449.3 s (`--support-cap 32`) |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |
| Decide | RETAINABLE; interval 24 s, exact 9 s; 2,543,909 boxes, stalled 0 |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
