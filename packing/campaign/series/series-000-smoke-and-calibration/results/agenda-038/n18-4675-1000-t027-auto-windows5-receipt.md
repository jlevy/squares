# n=18 187/40 T-027-Seeded Auto Window-5 Covering Receipt

Status: **retained**. `s(18) >= 187/40` is T-028. Canonical bytes:
`packing/cases/n18_fractional_certificate/certificate.json`. The previous
T-027 bytes sit at `certificate-467-100.json`.

Session-140 rank-5 probe: BC-191 auto grids `(32, 43, 53)` unioned with T-027's
769 atom sites scaled from `467/100` to `187/40` (`4675/1000` in the queue),
plus `--seed-windows 5`, `(n, L, B, net) = (18, 187/40, 9977/10000, 181
directions)`. Seed sites 1169. The row loop never crossed 18 and converged at
`17.879034` with `least_covered = 1` (38 LP rounds, 6837 sites / 921 orbits).
`declare_least_cell_mass` then `decide_certificate` accepted both routes at
least cell mass `4000013/4000000`. sha256
`9507659fa55a48869f060bff07e8d0e4f088cf70320f571afdca1bb460d9bb7b`.
T-027 at `467/100` remains the previous n=18 rung. This retain does not
confirm H-218: n=18 is off that sweep.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 4675/1000 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n18_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5.log
```

The seed path was T-027's live pointer at run time (`467/100`, 769 atoms).
The live pointer now holds T-028.

Declare then decide:

```bash
uv run --frozen --all-extras --group dev python -m devtools.declare_least_cell_mass \
  campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-certificate.json
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-certificate.json
```

The case copy is the canonical artifact.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.879034` |
| Artifact mass | `35758287/2000000 = 17.8791435` |
| Least cell mass | `4000013/4000000` |
| Atoms | 725 |
| Sites / orbits / rows | 6837 / 921 / 9607 |
| Seed sites | 1169 |
| LP rounds | 38 |
| Crossing | stayed below 18 |
| Wall | 319.6 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |
| Decide | RETAINABLE; interval 23 s, exact 5 s; 2,684,845 boxes, stalled 0 |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
